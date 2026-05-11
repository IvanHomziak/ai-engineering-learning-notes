---
type: daily-review-note
topic: Layer 2 Raw Function Calling with Ollama JSON Schemas
area: Agents
date: 2026-05-11
tags:
  - agents
  - raw-function-calling
  - ollama
  - json-schema
  - tool-calling
  - langchain-abstractions
  - langsmith
  - ai-platform-engineering
status: active-review
review:
  - 2026-05-12
  - 2026-05-14
  - 2026-05-18
  - 2026-05-25
  - 2026-06-10
---

# Daily Review Note: Layer 2 Raw Function Calling with Ollama JSON Schemas

## 1. Core idea

### Source-based explanation

Layer 2 показує той самий e-commerce agent loop, але без LangChain chat model, LangChain `@tool`, LangChain message objects і LangChain `ToolMessage`.

Замість цього використовується:

- raw Ollama Python SDK;
- manual JSON schemas для tools;
- plain Python functions;
- manual `tools_dict` для dispatch;
- raw message dictionaries з ролями `system`, `user`, `tool`;
- manual LangSmith tracing через `@traceable`.

Головна ідея: LangChain abstraction приховує значну частину integration boilerplate. Коли LangChain прибрати, developer сам відповідає за tool schemas, provider-specific message format, SDK calls, tool dispatch і tracing.

### Additional backend / production context

Це корисний exercise для AI Platform Engineer, бо production AI systems часто потребують розуміння нижнього рівня abstraction. Якщо framework ламається, маєш розуміти, що реально відбувається:

```text
LLM request + tools schema -> structured tool_calls -> app dispatch -> tool result -> tool message -> next LLM request
```

### Assumptions

- Нотатка базується тільки на transcript Section 6 і наданому файлі `2_agent_loop_raw_function_calling.py`.
- Production-рекомендації нижче позначені окремо як additional backend / production context.

### Unknowns

- Unknown / Not confirmed from source: повна формальна специфікація Ollama tool JSON schema.
- Unknown / Not confirmed from source: точна поведінка Anthropic/OpenAI/Gemini schemas у деталях, бо source лише порівнює conceptually.
- Unknown / Not confirmed from source: чи всі Ollama models однаково добре підтримують function calling.

---

## 2. Why it matters

### Source-based explanation

Layer 2 відповідає на питання: **що LangChain робив за нас у Layer 1?**

У Layer 1:

```python
@tool
def get_product_price(product: str) -> float:
    ...
```

LangChain автоматично генерував tool schema з:

- function name;
- docstring;
- type hints;
- arguments.

У Layer 2 це треба писати вручну:

```python
tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Look up the price of a product in the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product name, e.g. 'laptop', 'headphones', 'keyboard'",
                    },
                },
                "required": ["product"],
            },
        },
    }
]
```

Це показує cost of abstraction removal: контроль більший, але коду, vendor-specific details і maintenance більше.

### Additional backend / production context

Це типова trade-off у platform engineering:

| Approach | Benefit | Cost |
|---|---|---|
| LangChain abstraction | швидше розробляти, менше boilerplate, простіше switch provider | менше контролю, залежність від framework behavior |
| Raw SDK | повний контроль, видно provider-specific behavior | більше schema/message boilerplate, важче portability, більше integration bugs |

---

## 3. How it works

### Source-based explanation

#### Step 1 — Environment and imports

```python
from dotenv import load_dotenv
load_dotenv()

import ollama
from langsmith import traceable
```

LangChain imports прибрані. Залишається:

- `ollama` — raw Python SDK для Ollama;
- `traceable` — ручне трасування LangSmith;
- `load_dotenv` — environment variables.

#### Step 2 — Constants

```python
MAX_ITERATIONS = 10
MODEL = "qwen3:1.7b"
```

`MAX_ITERATIONS` — loop guard.

`MODEL` — локальна Ollama model, яку використовує source.

#### Step 3 — Tools as plain Python functions

```python
@traceable(run_type="tool")
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"    >> Executing get_product_price(product='{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)
```

Тут уже немає LangChain `@tool`. Function залишається звичайною Python function, але обгорнута `@traceable(run_type="tool")`, щоб LangSmith бачив її як tool run.

```python
@traceable(run_type="tool")
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers: bronze, silver, gold."""
    print(f"    >> Executing apply_discount(price={price}, discount_tier='{discount_tier}')")
    discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentages.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)
```

Цей function застосовує discount tier. У source: `bronze = 5`, `silver = 12`, `gold = 23`.

#### Step 4 — Manual JSON schemas

```python
tools_for_llm = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Look up the price of a product in the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product name, e.g. 'laptop', 'headphones', 'keyboard'",
                    },
                },
                "required": ["product"],
            },
        },
    },
]
```

Це manual representation tool contract для LLM. У source прямо сказано: це те, що LangChain `@tool` генерував автоматично з function signature і docstring.

Другий schema описує `apply_discount`:

- `price` має type `number`;
- `discount_tier` має type `string`;
- обидва required.

#### Step 5 — Ollama auto-generation note

Source code notes:

```python
# Ollama can also auto-generate these schemas if you pass the functions
# directly as tools ... However, this requires your docstrings to follow
# the Google docstring format.
```

Важливо: це стосується Ollama behavior. Source підкреслює, що vendor-specific behavior відрізняється.

#### Step 6 — Manual traced LLM call

```python
@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(messages):
    return ollama.chat(model=MODEL, tools=tools_for_llm, messages=messages)
```

Без LangChain tracing не приходить автоматично на такому рівні abstraction. Тому автор створює wrapper function і вручну ставить `@traceable`.

#### Step 7 — Manual tool registry

```python
tools_dict = {
    "get_product_price": get_product_price,
    "apply_discount": apply_discount,
}
```

У LangChain version registry будувався через tool objects і `t.name`. Тут mapping пишеться вручну.

#### Step 8 — Raw messages

```python
messages = [
    {
        "role": "system",
        "content": (...),
    },
    {"role": "user", "content": question},
]
```

LangChain `SystemMessage` і `HumanMessage` прибрані. Використовуються plain dictionaries, які відповідають Ollama SDK expected format.

Source каже, що в інших vendors naming/format може відрізнятись, наприклад role naming.

#### Step 9 — Raw agent loop

```python
for iteration in range(1, MAX_ITERATIONS + 1):
    response = ollama_chat_traced(messages=messages)
    ai_message = response.message
    tool_calls = ai_message.tool_calls
```

Тут `response` — Ollama response, не LangChain `AIMessage`.

#### Step 10 — Final answer condition

```python
if not tool_calls:
    print(f"\nFinal Answer: {ai_message.content}")
    return ai_message.content
```

Якщо `tool_calls` empty — agent завершує loop і повертає content.

#### Step 11 — Tool call parsing

```python
tool_call = tool_calls[0]
tool_name = tool_call.function.name
tool_args = tool_call.function.arguments
```

У Ollama object structure інша, ніж у LangChain. Тут access іде через attributes:

```text
tool_call.function.name
tool_call.function.arguments
```

У source також сказано, що Ollama response не має `tool_call_id`, на відміну від LangChain flow.

#### Step 12 — Direct function call

```python
tool_to_use = tools_dict.get(tool_name)
if tool_to_use is None:
    raise ValueError(f"Tool '{tool_name}' not found")

observation = tool_to_use(**tool_args)
```

Без LangChain `tool.invoke(...)`. Tool виконується як звичайна Python function з unpacked keyword arguments.

#### Step 13 — Append raw tool message

```python
messages.append(ai_message)
messages.append(
    {
        "role": "tool",
        "content": str(observation),
    }
)
```

Без `ToolMessage`. Observation додається як raw dict із role `tool`.

---

## 4. Backend analogy

### Source-based explanation

Layer 2 показує той самий agent loop, але з raw SDK і manual contracts.

### Additional backend / production context

Backend analogy:

| Raw function calling code | Backend analogy |
|---|---|
| `tools_for_llm` JSON | OpenAPI-like contract / command schema |
| `ollama.chat(...)` | direct vendor SDK call |
| `tools_dict` | command handler registry |
| `tool_call.function.name` | command name selected by decision service |
| `tool_call.function.arguments` | command payload / DTO |
| `tool_to_use(**tool_args)` | command handler invocation |
| `{"role": "tool", "content": ...}` | result event/message added to workflow history |
| manual `@traceable` | manual instrumentation / spans |

This is similar to writing an integration adapter by hand instead of using a framework-level abstraction.

---

## 5. Production relevance

### Source-based explanation

Source explicitly shows these production-relevant concerns:

1. Without LangChain, schemas are manual.
2. Ollama schema conventions differ from other vendors.
3. Ollama can accept Python functions directly, but only with Google-style docstrings for auto-parsing.
4. Without LangChain, messages are provider-specific dicts.
5. Without LangChain, tracing LLM calls must be added manually.
6. Vendor switching without LangChain has high development cost.
7. Function calling still returns structured function name + arguments, but application executes the tool.

### Additional backend / production context

#### Reliability risks

- Manual schemas can drift from actual Python function signatures.
- Required fields in schema may not match runtime function args.
- Vendor-specific response shape can break parser code.
- No `tool_call_id` in this flow can make correlation harder.
- Silent default `0` for unknown product/tier can produce wrong business answer.

#### Security risks

- Tool name from model output must be allowlisted through `tools_dict`.
- Tool arguments must be validated before function execution.
- Never expose arbitrary Python functions to LLM-controlled dispatch.
- Tool schemas should not expose sensitive internal capabilities.

#### Performance / cost risks

- Every loop iteration is an LLM call.
- Provider-specific manual integration increases maintenance cost.
- Bigger schemas/messages increase prompt size.
- Local Ollama avoids external API call cost but uses local compute and model quality can vary.

#### Observability concerns

- Raw SDK calls require manual instrumentation.
- Trace should include iteration number, model response, selected tool, arguments, observation, and final answer.
- Without framework help, trace consistency becomes developer responsibility.

### Version-sensitive

This note is version-sensitive because:

- Ollama SDK response objects and `tool_calls` structure may change.
- Ollama support for passing Python functions directly as tools depends on SDK behavior.
- LangSmith `@traceable` behavior may vary by package version.
- Provider-specific tool schema formats are not guaranteed to be identical.

### Potential issue

Source transcript says Ollama documentation does not clearly define all details of the JSON schema. Treat the exact schema requirements as provider-specific and verify against current Ollama docs/source before production use.

Another potential issue: source code has a comment `# --- Tools (LangChain @tool decorator) ---`, but actual code no longer uses LangChain `@tool`; it uses `@traceable`. This is likely a leftover comment.

---

## 6. Key terms

### Source-based explanation

| Term | Meaning |
|---|---|
| Raw Function Calling | Agent implementation using structured tool calls without LangChain abstractions |
| Ollama SDK | Python SDK used to call Ollama directly |
| JSON schema | Manual tool contract describing function name, description, parameters, required args |
| `tools_for_llm` | List of tool schemas passed into `ollama.chat` |
| `@traceable(run_type="tool")` | LangSmith decorator used to trace tool functions manually |
| `@traceable(run_type="llm")` | LangSmith decorator used to trace raw LLM call wrapper |
| `tools_dict` | Manual mapping from tool names to executable Python functions |
| `tool_call.function.name` | Ollama-specific way to read selected function name |
| `tool_call.function.arguments` | Ollama-specific way to read function arguments |
| observation | Tool execution result passed back into agent context |
| raw message dict | Provider-specific message object with `role` and `content` |
| provider-specific format | Different vendors may expect different schema/message structures |

---

## 7. Common mistakes

### Source-based explanation

1. Assuming LangChain `@tool` is just syntactic sugar.
   - Source shows it hides schema generation and vendor-specific formatting.

2. Assuming all providers use the same tool schema.
   - Transcript says Ollama and Anthropic schemas differ.

3. Assuming Ollama function auto-conversion works with any docstring.
   - Source says it requires Google-style docstrings.

4. Keeping LangChain-style message assumptions when using raw SDK.
   - Raw Ollama uses dicts and its own response shape.

5. Trying to use `tool.invoke(...)` after removing LangChain tools.
   - In raw version, tools are plain functions and are called directly.

6. Forgetting manual tracing.
   - Without LangChain, source adds `ollama_chat_traced` manually.

### Additional backend / production context

7. Schema drift.
   - Function signature changes but JSON schema does not.

8. Weak argument validation.
   - Model-produced `tool_args` should not be trusted blindly.

9. Inconsistent provider adapters.
   - Raw code often grows into scattered vendor-specific logic unless isolated behind clean interfaces.

10. Treating raw SDK code as simpler.
   - It can be simpler for one provider, but more expensive once multiple providers, tracing, retries, schemas and evals are needed.

---

## 8. Flashcards

| Question | Answer |
|---|---|
| What is Layer 2 about? | Implementing the same agent loop without LangChain objects, using raw Ollama SDK and manual JSON tool schemas. |
| What replaces LangChain `@tool`? | Plain Python functions plus manual JSON schemas in `tools_for_llm`. |
| What does LangChain `@tool` hide according to source? | JSON schema generation from function name, docstring, type hints and arguments. |
| What replaces `llm_with_tools.invoke(...)`? | `ollama.chat(...)` wrapped in `ollama_chat_traced`. |
| What replaces `SystemMessage` and `HumanMessage`? | Raw dictionaries with `role` and `content`. |
| What replaces `ToolMessage`? | Raw dictionary with `role: "tool"` and `content` equal to the observation. |
| How is selected tool name read in Ollama response? | Through `tool_call.function.name`. |
| How are tool arguments read in Ollama response? | Through `tool_call.function.arguments`. |
| How is the tool executed in raw version? | By calling the Python function directly: `tool_to_use(**tool_args)`. |
| Why is vendor switching harder without LangChain? | Tool schemas, message formats, SDK calls and response shapes can differ by provider. |
| Why is manual JSON schema risky? | It can drift from real function signatures and create runtime bugs. |
| What is the main lesson of Layer 2? | Function calling is structured API behavior, not magic; LangChain mainly reduces integration boilerplate. |

---

## 9. Interview Q&A

### Q1: What problem does Layer 2 demonstrate?

**Answer:** It demonstrates what LangChain abstracts away when implementing tool-calling agents: tool schema generation, message formatting, SDK invocation, tool dispatch format and tracing integration.

### Q2: How does raw function calling differ from LangChain tool calling?

**Answer:** In LangChain, tools are decorated with `@tool`, bound with `bind_tools`, invoked through `tool.invoke`, and observations are sent via `ToolMessage`. In raw Ollama, schemas are manually written, `ollama.chat` is called directly, tool calls are parsed from Ollama response objects, tools are called as Python functions, and observations are appended as raw dicts.

### Q3: Why are JSON schemas needed?

**Answer:** The LLM needs structured descriptions of available tools: function name, description, parameters, types and required arguments. This lets the model return structured tool calls.

### Q4: Why does the source say documentation clarity matters?

**Answer:** Because without a clear formal schema definition, developers must infer required schema shape from examples or source code, which increases integration risk.

### Q5: Why is provider portability expensive without LangChain?

**Answer:** Different providers may have different schema formats, role names, SDK request shapes and response structures. Switching providers can require rewriting integration code.

### Q6: What is the role of `tools_dict`?

**Answer:** It maps model-selected tool names to actual Python functions so application code can execute the selected tool.

### Q7: What is an observation in this raw implementation?

**Answer:** It is the result of executing the Python function selected by the model. The observation is converted to string and appended to messages as a `tool` role message.

### Q8: Why is manual tracing needed?

**Answer:** Without LangChain model abstractions, LangSmith does not automatically wrap the raw Ollama call, so the source creates `ollama_chat_traced` with `@traceable(run_type="llm")`.

### Q9: What production risk comes from manual JSON schemas?

**Answer:** Schema drift: the Python function signature can change while the JSON schema remains stale, causing wrong arguments, missing required fields or runtime errors.

### Q10: What is the key lesson from removing LangChain in Layer 2?

**Answer:** LangChain is not magic; it standardizes common integration tasks. Removing it exposes the raw mechanics and the maintenance cost of provider-specific implementation.

---

## 10. Self-check

Answer without looking:

1. What file implements Layer 2?
2. What imports remain after removing LangChain objects?
3. What replaces `@tool`?
4. What is `tools_for_llm`?
5. What does `ollama_chat_traced` do?
6. Why is `tools_dict` written manually?
7. How do we read selected tool name in Ollama response?
8. How do we execute the selected tool?
9. What replaces `ToolMessage`?
10. Why is provider switching harder in raw SDK code?

Expected answers:

1. `2_agent_loop_raw_function_calling.py`.
2. `load_dotenv`, `ollama`, `traceable`.
3. Plain Python functions plus manual JSON schemas and `@traceable` for tracing.
4. A list of manual JSON schemas describing tools for the LLM.
5. Wraps `ollama.chat(...)` and traces it as an LLM call in LangSmith.
6. Because there are no LangChain tool objects with `.name`; mapping is needed for dispatch.
7. `tool_call.function.name`.
8. `tool_to_use(**tool_args)`.
9. A raw dict: `{"role": "tool", "content": str(observation)}`.
10. Because schemas, message roles, SDK calls and response structures are provider-specific.

---

## 11. Mini practice task

### Source-based practice

Run Layer 2:

```bash
uv run python 2_agent_loop_raw_function_calling.py
```

Verify the expected loop:

```text
Iteration 1: get_product_price(product='laptop') -> 1299.99
Iteration 2: apply_discount(price=1299.99, discount_tier='gold') -> 1000.99
Iteration 3: no tool calls -> final answer
```

Then inspect LangSmith trace and confirm:

- trace name is `Ollama Agent Loop`;
- LLM call is `Ollama Chat`;
- tool calls are traced separately;
- observation is appended as raw `tool` role message.

### Additional backend / production context task

Improve raw implementation safety:

1. Add validation that `tool_name` is allowlisted.
2. Validate `tool_args` against expected argument names.
3. Replace silent `0` defaults with explicit errors.
4. Add a small test list with valid and invalid queries.
5. Add a comment explaining where schema drift can happen.

### Unknowns

- Unknown / Not confirmed from source: exact LangSmith trace output on your machine.
- Unknown / Not confirmed from source: exact Ollama SDK response object structure in future versions.
- Unknown / Not confirmed from source: whether the same JSON schema works unchanged across other providers.
