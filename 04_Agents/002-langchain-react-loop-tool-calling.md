---
type: daily-review-note
topic: Layer 1 ReAct Loop with LangChain Tool Calling
area: Agents
date: 2026-05-10
tags:
  - agents
  - react-loop
  - langchain
  - tool-calling
  - bind-tools
  - defensive-prompting
  - langsmith
  - ollama
  - model-switching
  - ai-platform-engineering
status: active-review
review:
  - 2026-05-11
  - 2026-05-13
  - 2026-05-17
  - 2026-05-24
  - 2026-06-09
---

# Daily Review Note: Layer 1 ReAct Loop with LangChain Tool Calling

## 1. Core idea

### Source-based explanation

Ця лекція реалізує **перший знятий шар abstraction** для AI agent: agent loop пишеться вручну, але все ще використовуються LangChain primitives.

Source implementation будує e-commerce shopping assistant, який відповідає на питання:

```text
What is the price of a laptop after applying a gold discount?
```

Agent має два tools:

```python
def get_product_price(product: str) -> float
```

і:

```python
def apply_discount(price: float, discount_tier: str) -> float
```

Ключова ідея: LangChain не “сам виконує агента магічно”. У цьому layer ми самі пишемо loop:

```text
messages -> LLM with bound tools -> tool_calls? -> execute tool -> append ToolMessage -> repeat -> final answer
```

### Additional backend / production context

Це схоже на мінімальний orchestration engine:

- LLM = decision maker;
- Python tool = domain service / adapter;
- tool registry = command registry;
- `ToolMessage` = result event / command result;
- loop = workflow runtime.

### Assumptions

- Нотатка базується на наданому transcript Section 5 і файлі `1_agent_loop_langchain_tool_calling.py`.
- Production-коментарі винесені окремо і не приписуються source, якщо source цього прямо не каже.

### Unknowns

- Unknown / Not confirmed from source: точні internals `init_chat_model`, `bind_tools`, `ToolMessage` для кожного provider.
- Unknown / Not confirmed from source: які саме LangChain версії були використані, якщо не дивитися в dependency lock.

---

## 2. Why it matters

### Source-based explanation

Цей layer показує, що LangChain дає корисні abstractions, але agent loop все одно можна зрозуміти як звичайний код:

1. Ініціалізувати model.
2. Описати tools через Python functions + `@tool`.
3. Привʼязати tools до model через `bind_tools`.
4. Надіслати system + human messages.
5. Отримати від LLM structured `tool_calls` або final answer.
6. Виконати tool у application code.
7. Додати результат назад через `ToolMessage`.
8. Повторити цикл.

LangChain корисний тут тому, що зменшує boilerplate:

- не треба вручну писати JSON schemas для tools;
- є typed message objects;
- є common interface для chat models;
- model provider можна змінити string-based способом через `init_chat_model`, якщо provider integration installed.

### Additional backend / production context

Для AI Platform Engineer це важливо, бо production agent — це не тільки prompt. Це runtime loop із:

- state management;
- external tool execution;
- tracing;
- failure handling;
- model/provider portability;
- evaluation перед model switch.

---

## 3. How it works

### Source-based explanation

#### Step 1 — Environment loading

```python
from dotenv import load_dotenv
load_dotenv()
```

Завантажує environment variables з `.env`. У transcript це використовується для OpenAI API key і LangSmith tracing configuration.

#### Step 2 — Imports

```python
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable
```

Source пояснює:

- `init_chat_model` — utility function для ініціалізації chat model через string;
- `tool` — decorator, який перетворює Python function у LangChain tool;
- `SystemMessage` — system prompt wrapper;
- `HumanMessage` — user input wrapper;
- `ToolMessage` — wrapper для tool result;
- `traceable` — LangSmith tracing decorator.

#### Step 3 — Constants

```python
MAX_ITERATIONS = 10
MODEL = "qwen3:1.7b"
```

`MAX_ITERATIONS = 10` — heuristic guard, щоб agent loop не крутився безкінечно. Transcript прямо каже, що `10` не має спеціального значення, це просто обмеження.

`MODEL = "qwen3:1.7b"` — локальна Ollama model, яку автор використовує в цьому section.

#### Step 4 — Tools

```python
@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"    >> Executing get_product_price(product='{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)
```

Цей tool повертає ціну продукту з in-memory dictionary. Якщо продукт не знайдений — повертає `0`.

```python
@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers: bronze, silver, gold."""
    print(f"    >> Executing apply_discount(price={price}, discount_tier='{discount_tier}')")
    discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentages.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)
```

Цей tool застосовує discount tier. `gold` = `23%`, тому для `1299.99` результат має бути `1000.99`.

Source підкреслює: function name, docstring, argument types і return type важливі, бо вони передаються LLM у tool metadata.

#### Step 5 — Agent function and tracing

```python
@traceable(name="LangChain Agent Loop")
def run_agent(question: str):
```

`@traceable` створює LangSmith trace scope для всього agent loop.

#### Step 6 — Tool registry

```python
tools = [get_product_price, apply_discount]
tools_dict = {t.name: t for t in tools}
```

`tools` передається model через `bind_tools`.

`tools_dict` потрібен для dispatch: LLM повертає tool name, application code знаходить відповідний Python object і виконує його.

#### Step 7 — Model initialization and tool binding

```python
llm = init_chat_model(f"ollama:{MODEL}", temperature=0)
llm_with_tools = llm.bind_tools(tools)
```

`init_chat_model` ініціалізує chat model за string. `bind_tools(tools)` прикріплює tool definitions до model call, щоб LLM могла повернути structured tool call.

Version-sensitive: exact provider string format і supported providers залежать від LangChain/provider package versions.

#### Step 8 — Defensive prompting

```python
messages = [
    SystemMessage(
        content=(
            "You are a helpful shopping assistant. "
            "You have access to a product catalog tool "
            "and a discount tool.\n\n"
            "STRICT RULES — you must follow these exactly:\n"
            "1. NEVER guess or assume any product price. "
            "You MUST call get_product_price first to get the real price.\n"
            "2. Only call apply_discount AFTER you have received "
            "a price from get_product_price. Pass the exact price "
            "returned by get_product_price — do NOT pass a made-up number.\n"
            "3. NEVER calculate discounts yourself using math. "
            "Always use the apply_discount tool.\n"
            "4. If the user does not specify a discount tier, "
            "ask them which tier to use — do NOT assume one."
        )
    ),
    HumanMessage(content=question),
]
```

Purpose of strict rules:

- не дозволити LLM вигадувати price;
- змусити спочатку викликати `get_product_price`;
- змусити викликати `apply_discount`, а не рахувати discount самостійно;
- не дозволити agent припускати discount tier, якщо user його не вказав.

Transcript каже, що ці правила були додані після спостереження, що open-weight model може hallucinate price.

#### Step 9 — Loop execution

```python
for iteration in range(1, MAX_ITERATIONS + 1):
    ai_message = llm_with_tools.invoke(messages)
    tool_calls = ai_message.tool_calls
```

На кожній ітерації:

- agent надсилає всю history у LLM;
- LLM повертає або tool call, або final content.

#### Step 10 — Final answer condition

```python
if not tool_calls:
    print(f"\nFinal Answer: {ai_message.content}")
    return ai_message.content
```

Якщо tool calls немає — agent вважає, що LLM має final answer.

#### Step 11 — Tool selection

```python
tool_call = tool_calls[0]
tool_name = tool_call.get("name")
tool_args = tool_call.get("args", {})
tool_call_id = tool_call.get("id")
```

Source intentionally бере тільки перший tool call для простоти. Transcript зазначає, що LLM може повернути multiple tool calls, але приклад форсить one tool per iteration.

#### Step 12 — Tool dispatch and observation

```python
tool_to_use = tools_dict.get(tool_name)
if tool_to_use is None:
    raise ValueError(f"Tool '{tool_name}' not found")

observation = tool_to_use.invoke(tool_args)
```

Application code виконує tool і отримує observation.

#### Step 13 — Feed result back into context

```python
messages.append(ai_message)
messages.append(
    ToolMessage(content=str(observation), tool_call_id=tool_call_id)
)
```

Це критичний момент agent loop: LLM має побачити, що вона вирішила зробити tool call, і який реальний результат повернув tool.

#### Step 14 — Loop failure condition

```python
print("ERROR: Max iterations reached without a final answer")
return None
```

Якщо за `MAX_ITERATIONS` немає final answer — loop завершується помилкою.

---

## 4. Backend analogy

### Source-based explanation

Source implementation явно має:

- tool functions;
- tool registry;
- model invocation;
- structured tool call extraction;
- function execution;
- observation append;
- final answer condition;
- max iteration guard.

### Additional backend / production context

Backend mapping:

| Agent code | Backend analogy |
|---|---|
| `run_agent(question)` | application service / use-case handler |
| `tools_dict` | command handler registry |
| `@tool` function | domain service / adapter method |
| `bind_tools(tools)` | exposing command contracts to decision layer |
| `llm_with_tools.invoke(messages)` | remote decision service call |
| `ai_message.tool_calls` | command request / intent from decision layer |
| `tool_to_use.invoke(tool_args)` | command execution |
| `ToolMessage` | command result appended to workflow state |
| `MAX_ITERATIONS` | safety guard / circuit breaker style limit |
| LangSmith trace | distributed trace / workflow trace |

---

## 5. Production relevance

### Source-based explanation

Source highlights several production-relevant points:

1. **Tracing:** `@traceable(name="LangChain Agent Loop")` wraps the whole loop.
2. **Tool tracing:** LangChain `@tool` makes tool execution visible in LangSmith trace according to transcript.
3. **Token/runtime/cost visibility:** transcript says nesting under one trace helps inspect tokens, runtime and cost.
4. **Defensive prompting:** strict rules reduce hallucinated prices and unsupported assumptions.
5. **Model switching:** `init_chat_model` makes switching model/provider convenient.
6. **Model switching is not enough:** transcript shows a model switch can produce insufficient behavior, so evaluation/benchmarking is needed before switching models.

### Additional backend / production context

#### Reliability risks

- LLM may call the wrong tool.
- LLM may pass wrong arguments.
- LLM may never return final answer.
- Agent may exceed max iterations.
- Returning `0` for unknown product/tier can hide business errors.

#### Security risks

- Tool execution is a trust boundary.
- Never let arbitrary model output execute arbitrary code.
- Use allowlisted tools only.
- Validate `tool_name` and `tool_args` before execution.
- Avoid committing `.env` secrets.

#### Performance / cost risks

- Every iteration is another model call.
- More messages/history increase tokens.
- Tool calls may add latency.
- A weaker local model may require more defensive prompting and more iterations.

#### Evaluation requirement

Model portability is only an engineering convenience. It does not prove correctness.

Before switching model in production, benchmark at least:

- tool selection accuracy;
- argument correctness;
- final answer correctness;
- latency;
- token/cost profile;
- failure rate;
- behavior on ambiguous inputs;
- behavior when tools return errors.

### Version-sensitive

`init_chat_model`, provider string syntax, `bind_tools`, structured `tool_calls`, and provider support for function calling are version-sensitive. Verify against installed LangChain integration packages and model provider behavior.

### Potential issue

The source functions silently return `0` for unknown product or unknown discount tier:

```python
prices.get(product, 0)
discount_percentages.get(discount_tier, 0)
```

For a toy example this is acceptable. In production this is risky because wrong input can become a valid-looking price instead of an explicit domain error.

---

## 6. Key terms

### Source-based explanation

| Term | Meaning |
|---|---|
| `init_chat_model` | LangChain utility for creating chat model from provider/model string |
| `@tool` | LangChain decorator that converts Python function into a tool |
| `bind_tools` | Method that attaches tool definitions to a chat model |
| `SystemMessage` | Message object for system-level agent instructions |
| `HumanMessage` | Message object for user input |
| `ToolMessage` | Message object carrying actual tool result back to the model |
| `tool_calls` | Structured model output describing which tool to call and with what args |
| `observation` | Actual result returned by tool execution |
| `tools_dict` | Registry mapping tool name to executable tool object |
| `MAX_ITERATIONS` | Loop guard preventing unbounded execution |
| defensive prompting | Prompt rules that reduce guessing, hallucination, and unsafe assumptions |
| LangSmith trace | Trace view for observing model calls, tool calls, latency, tokens and cost |
| model switch | Changing model/provider string while keeping agent code mostly unchanged |

---

## 7. Common mistakes

### Source-based explanation

1. Thinking `bind_tools` executes tools.
   - It does not. It exposes tools to the model. Application code still executes the selected tool.

2. Not appending `ToolMessage`.
   - Without tool result in context, the next LLM call does not know the observation.

3. Assuming the model will not guess.
   - Source adds strict defensive rules because the model may hallucinate price or calculate by itself.

4. Treating model switch as safe by default.
   - Transcript explicitly shows a model switch can produce insufficient result.

5. Ignoring multiple tool calls.
   - Source processes only first tool call for simplicity. Real systems may need multi-call handling.

6. Letting loop run without a guard.
   - Source uses `MAX_ITERATIONS = 10`.

### Additional backend / production context

7. Returning default `0` instead of domain error.
   - This can create silent data corruption in user-facing answer.

8. No structured validation of tool arguments.
   - Production tools should validate product names, discount tiers, numeric ranges, and required arguments.

9. No retry/timeout policy.
   - Not shown in source. Production tools and model calls need timeouts and retry strategy.

10. No automated evaluation before model switch.
   - Manual trace inspection is useful but not enough for production rollout.

---

## 8. Flashcards

| Question | Answer |
|---|---|
| What does Layer 1 implement? | A manual ReAct-style agent loop using LangChain primitives for model, tools, messages, and tracing. |
| What does `@tool` do in this source? | It turns a Python function into a LangChain tool using function name, docstring and type hints as tool metadata. |
| What does `bind_tools(tools)` do? | It attaches tool definitions to the chat model so the model can return structured tool calls. |
| Does the LLM execute the tool? | No. The LLM returns a tool call; application code executes the tool. |
| What is `ToolMessage` used for? | It sends the actual tool result back into the message history. |
| What is `observation`? | The result returned by executing the selected tool. |
| Why does the code use `MAX_ITERATIONS`? | To prevent unbounded agent loops. |
| Why does the prompt forbid guessing prices? | To force the model to call `get_product_price` instead of hallucinating a price. |
| Why does the prompt forbid manual discount calculation? | To force tool usage and reduce arithmetic/hallucination risk. |
| Why is processing only `tool_calls[0]` a simplification? | Modern models may return multiple tool calls, but the example forces one tool per iteration. |
| Why is easy model switching not enough? | A new model may behave worse for the same agent task; it must be benchmarked/evaluated. |
| What is the production issue with returning `0` for unknown product? | It can silently convert an invalid input into a valid-looking answer. |

---

## 9. Interview Q&A

### Q1: How does LangChain tool calling work in this example?

**Answer:** Python functions are decorated with `@tool`, collected into a list, bound to the chat model using `bind_tools`, and then the model can return structured `tool_calls`. Application code reads the tool call, finds the tool in `tools_dict`, invokes it, and appends the result as `ToolMessage`.

### Q2: What is the role of `ToolMessage`?

**Answer:** `ToolMessage` carries the real result of a tool execution back into the model context. It lets the next LLM call reason over the actual observation instead of guessing what happened.

### Q3: Why is `tools_dict` needed?

**Answer:** The model returns a tool name as data. `tools_dict` maps that name to the actual executable Python tool object so the application can dispatch the call.

### Q4: What is defensive prompting in this lecture?

**Answer:** The system prompt gives strict rules: never guess product price, call `get_product_price` first, only then call `apply_discount`, do not calculate discount manually, and ask for missing discount tier instead of assuming one.

### Q5: Why is model switching convenient but dangerous?

**Answer:** LangChain makes provider/model switching easy through strings, but model behavior can change. The transcript shows that switching to another model can produce an insufficient answer, so evaluations are required.

### Q6: What does `MAX_ITERATIONS` protect against?

**Answer:** It limits the number of loop iterations if the model keeps calling tools or fails to produce final answer.

### Q7: What is the difference between `bind_tools` and tool execution?

**Answer:** `bind_tools` exposes tool schemas to the model. Tool execution happens later in application code after the model returns a tool call.

### Q8: What is a production flaw in the toy tools?

**Answer:** Unknown product or discount tier returns `0`, which can hide input errors and produce misleading output. Production code should return explicit domain errors.

### Q9: Why are docstrings and type hints important here?

**Answer:** Source says LangChain uses function name, docstring, argument information and return type metadata to format tool information for the model.

### Q10: How would you evaluate a model switch for this agent?

**Answer:** Run a benchmark dataset covering normal, ambiguous, invalid, and edge-case user queries; measure tool selection accuracy, argument correctness, final answer correctness, latency, token usage, cost, and failure cases.

---

## 10. Self-check

Answer without looking:

1. What are the two tools in the source code?
2. What does `@tool` give us?
3. Why is `tools_dict` created?
4. What does `bind_tools` do?
5. What happens when `ai_message.tool_calls` is empty?
6. Why does the code append both `ai_message` and `ToolMessage`?
7. Why is only `tool_calls[0]` processed?
8. What does `tool_call_id` help with?
9. Why is `MAX_ITERATIONS = 10` used?
10. Why is model switching not enough for production?

Expected answers:

1. `get_product_price` and `apply_discount`.
2. It wraps Python functions as LangChain tools and uses metadata such as name, docstring and type hints.
3. To map model-returned tool name to executable tool object.
4. It attaches tool definitions to the chat model.
5. The agent treats `ai_message.content` as final answer and returns it.
6. To preserve the model decision and the real tool result in context.
7. For simplicity; multiple tool calls are possible but not handled in this toy loop.
8. It links the tool result to the original tool call, especially useful for tracing/debugging.
9. To stop runaway loops.
10. Because different models may behave differently and must be evaluated for the specific use case.

---

## 11. Mini practice task

### Source-based practice

Run the LangChain layer:

```bash
uv run python 1_agent_loop_langchain_tool_calling.py
```

Then inspect:

1. First iteration: model should call `get_product_price` with `product='laptop'`.
2. Second iteration: model should call `apply_discount` with price from previous observation and `discount_tier='gold'`.
3. Third iteration: model should return final answer without tool calls.

### Additional backend / production context task

Make the toy implementation more production-like:

1. Replace `prices.get(product, 0)` with explicit error for unknown product.
2. Replace `discount_percentages.get(discount_tier, 0)` with explicit error for unknown tier.
3. Add validation before invoking a tool.
4. Add a test query without discount tier and verify that the agent asks for the tier instead of assuming it.
5. Create a small evaluation table with 10 queries and expected tool sequence.

### Unknowns

- Unknown / Not confirmed from source: exact LangSmith trace IDs, exact runtime, exact token usage and cost for your machine/provider.
- Unknown / Not confirmed from source: whether every model/provider string accepted by `init_chat_model` supports function calling in your installed environment.
