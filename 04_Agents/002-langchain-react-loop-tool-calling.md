---
type: daily-review-note
topic: Layer 1 ReAct Loop з LangChain Tool Calling
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

# Щоденна нотатка для повторення: Layer 1 ReAct Loop з LangChain Tool Calling

## 1. Основна ідея

### Пояснення на основі джерела

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

### Додатковий backend / production context

Це схоже на мінімальний orchestration engine:

- LLM = decision maker;
- Python tool = domain service / adapter;
- tool registry = command registry;
- `ToolMessage` = result event / command result;
- loop = workflow runtime.

### Припущення

- Нотатка базується на transcript Section 5 і файлі `1_agent_loop_langchain_tool_calling.py`.
- Production-коментарі винесені окремо і не приписуються source, якщо source цього прямо не каже.

### Невідоме / не підтверджено джерелом

- Unknown / Not confirmed from source: точні internals `init_chat_model`, `bind_tools`, `ToolMessage` для кожного provider.
- Unknown / Not confirmed from source: які саме LangChain versions були використані, якщо не дивитися dependency lock.

---

## 2. Чому це важливо

### Пояснення на основі джерела

Цей layer показує, що LangChain дає корисні abstractions, але agent loop усе одно можна зрозуміти як звичайний код:

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

### Додатковий backend / production context

Для AI Platform Engineer це важливо, бо production agent — це не тільки prompt. Це runtime loop із:

- state management;
- external tool execution;
- tracing;
- failure handling;
- model/provider portability;
- evaluation перед model switch.

---

## 3. Як це працює

### Пояснення на основі джерела

#### Step 1 — Environment loading

```python
from dotenv import load_dotenv
load_dotenv()
```

Завантажує environment variables із `.env`. У transcript це використовується для OpenAI API key і LangSmith tracing configuration.

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
- `SystemMessage` — wrapper для system prompt;
- `HumanMessage` — wrapper для user input;
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

System prompt містить strict rules:

- не дозволяти LLM вигадувати product price;
- змусити спочатку викликати `get_product_price`;
- викликати `apply_discount` тільки після отримання price;
- не рахувати discount самостійно;
- якщо user не вказав discount tier — запитати tier, а не припускати.

Transcript каже, що ці правила були додані після спостереження, що open-weight model може hallucinate price.

#### Step 9 — Loop execution

```python
for iteration in range(1, MAX_ITERATIONS + 1):
    ai_message = llm_with_tools.invoke(messages)
    tool_calls = ai_message.tool_calls
```

На кожній iteration:

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

## 4. Backend аналогія

### Пояснення на основі джерела

Source implementation явно має:

- tool functions;
- tool registry;
- model invocation;
- structured tool call extraction;
- function execution;
- observation append;
- final answer condition;
- max iteration guard.

### Додатковий backend / production context

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

### Пояснення на основі джерела

Source highlights several production-relevant points:

1. **Tracing:** `@traceable(name="LangChain Agent Loop")` wraps the whole loop.
2. **Tool tracing:** LangChain `@tool` makes tool execution visible in LangSmith trace according to transcript.
3. **Token/runtime/cost visibility:** transcript says nesting under one trace helps inspect tokens, runtime and cost.
4. **Defensive prompting:** strict rules reduce hallucinated prices and unsupported assumptions.
5. **Model switching:** `init_chat_model` makes switching model/provider convenient.
6. **Model switching is not enough:** transcript shows a model switch can produce insufficient behavior, so evaluation/benchmarking is needed before switching models.

### Додатковий backend / production context

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

Source functions silently return `0` for unknown product or unknown discount tier:

```python
prices.get(product, 0)
discount_percentages.get(discount_tier, 0)
```

For a toy example this is acceptable. In production this is risky because wrong input can become a valid-looking price instead of an explicit domain error.

---

## 6. Key terms

### Пояснення на основі джерела

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

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що `bind_tools` виконує tools.
   - Він тільки exposes tools to the model. Application code still executes the selected tool.

2. Не додавати `ToolMessage`.
   - Without tool result in context, next LLM call не знає observation.

3. Припускати, що model не буде guess.
   - Source додає strict defensive rules, бо model може hallucinate price або calculate by itself.

4. Treating model switch as safe by default.
   - Transcript clearly shows model switch can produce insufficient result.

5. Ignoring multiple tool calls.
   - Source processes only first tool call for simplicity. Real systems may need multi-call handling.

6. Letting loop run without a guard.
   - Source uses `MAX_ITERATIONS = 10`.

### Додатковий backend / production context

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
| Що реалізує Layer 1? | Manual ReAct-style agent loop із LangChain primitives для model, tools, messages і tracing. |
| Що робить `@tool` у цьому source? | Перетворює Python function у LangChain tool, використовуючи function name, docstring і type hints як tool metadata. |
| Що робить `bind_tools(tools)`? | Прикріплює tool definitions до chat model, щоб model могла повертати structured tool calls. |
| Чи LLM виконує tool? | Ні. LLM повертає tool call; application code виконує tool. |
| Для чого `ToolMessage`? | Щоб передати actual tool result назад у message history. |
| Що таке `observation`? | Result returned by executing the selected tool. |
| Навіщо `MAX_ITERATIONS`? | Щоб запобігти unbounded agent loops. |
| Чому prompt забороняє guessing prices? | Щоб змусити model call `get_product_price` замість hallucinating a price. |
| Чому prompt забороняє manual discount calculation? | Щоб force tool usage і зменшити arithmetic/hallucination risk. |
| Чому processing only `tool_calls[0]` — simplification? | Modern models можуть return multiple tool calls, але приклад forces one tool per iteration. |
| Чому easy model switching недостатній? | New model може behave worse for the same agent task; його треба benchmark/evaluate. |
| Production issue with returning `0` for unknown product? | Invalid input може silently convert into valid-looking answer. |

---

## 9. Interview Q&A

### Q1: Як працює LangChain tool calling у цьому прикладі?

**Answer:** Python functions decorated with `@tool`, collected into a list, bound to chat model using `bind_tools`, після чого model може return structured `tool_calls`. Application code читає tool call, знаходить tool у `tools_dict`, invokes it і appends result as `ToolMessage`.

### Q2: Яка роль `ToolMessage`?

**Answer:** `ToolMessage` carries real result of tool execution back into model context. Це дозволяє next LLM call reason over actual observation instead of guessing.

### Q3: Навіщо `tools_dict`?

**Answer:** Model returns tool name as data. `tools_dict` maps that name to actual executable Python tool object so application can dispatch the call.

### Q4: Що таке defensive prompting у цій lecture?

**Answer:** System prompt дає strict rules: never guess product price, call `get_product_price` first, only then call `apply_discount`, do not calculate discount manually, and ask for missing discount tier instead of assuming one.

### Q5: Чому model switching convenient but dangerous?

**Answer:** LangChain makes provider/model switching easy through strings, але model behavior може змінитися. Transcript показує, що switching to another model can produce insufficient answer, тому потрібні evaluations.

### Q6: Від чого захищає `MAX_ITERATIONS`?

**Answer:** It limits loop iterations if model keeps calling tools або fails to produce final answer.

### Q7: Різниця між `bind_tools` і tool execution?

**Answer:** `bind_tools` exposes tool schemas to model. Tool execution happens later in application code after model returns a tool call.

### Q8: Production flaw у toy tools?

**Answer:** Unknown product або discount tier returns `0`, що може hide input errors і produce misleading output. Production code should return explicit domain errors.

### Q9: Чому docstrings і type hints важливі?

**Answer:** Source каже, що LangChain uses function name, docstring, argument information and return type metadata to format tool information for the model.

### Q10: Як evaluate model switch для цього agent?

**Answer:** Run benchmark dataset covering normal, ambiguous, invalid, and edge-case user queries; measure tool selection accuracy, argument correctness, final answer correctness, latency, token usage, cost, and failure cases.

---

## 10. Self-check

Answer without looking:

1. Які два tools у source code?
2. Що дає `@tool`?
3. Чому створюється `tools_dict`?
4. Що робить `bind_tools`?
5. Що стається, коли `ai_message.tool_calls` empty?
6. Чому code appends both `ai_message` and `ToolMessage`?
7. Чому processed only `tool_calls[0]`?
8. З чим допомагає `tool_call_id`?
9. Навіщо `MAX_ITERATIONS = 10`?
10. Чому model switching недостатній для production?

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

## 11. Міні-практика

### Практика на основі джерела

Запусти LangChain layer:

```bash
uv run python 1_agent_loop_langchain_tool_calling.py
```

Потім перевір:

1. First iteration: model should call `get_product_price` with `product='laptop'`.
2. Second iteration: model should call `apply_discount` with price from previous observation and `discount_tier='gold'`.
3. Third iteration: model should return final answer without tool calls.

### Додатковий backend / production context task

Make the toy implementation more production-like:

1. Replace `prices.get(product, 0)` with explicit error for unknown product.
2. Replace `discount_percentages.get(discount_tier, 0)` with explicit error for unknown tier.
3. Add validation before invoking a tool.
4. Add a test query without discount tier and verify that the agent asks for the tier instead of assuming it.
5. Create a small evaluation table with 10 queries and expected tool sequence.

### Unknowns

- Unknown / Not confirmed from source: exact LangSmith trace IDs, exact runtime, exact token usage and cost for your machine/provider.
- Unknown / Not confirmed from source: whether every model/provider string accepted by `init_chat_model` supports function calling in your installed environment.
