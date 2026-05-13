---
type: daily-review-note
topic: Layer 2 Raw Function Calling з Ollama JSON Schemas
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

# Щоденна нотатка для повторення: Layer 2 Raw Function Calling з Ollama JSON Schemas

## 1. Основна ідея

### Пояснення на основі джерела

Layer 2 показує той самий e-commerce agent loop, але без LangChain chat model, LangChain `@tool`, LangChain message objects і LangChain `ToolMessage`.

Замість цього використовується:

- raw Ollama Python SDK;
- manual JSON schemas для tools;
- plain Python functions;
- manual `tools_dict` для dispatch;
- raw message dictionaries з ролями `system`, `user`, `tool`;
- manual LangSmith tracing через `@traceable`.

Головна ідея: LangChain abstraction приховує значну частину integration boilerplate. Якщо прибрати LangChain, developer сам відповідає за tool schemas, provider-specific message format, SDK calls, tool dispatch і tracing.

### Додатковий backend / production context

Це корисна вправа для AI Platform Engineer, бо production AI systems часто потребують розуміння нижнього рівня abstraction. Якщо framework ламається, треба розуміти, що реально відбувається:

```text
LLM request + tools schema -> structured tool_calls -> app dispatch -> tool result -> tool message -> next LLM request
```

### Припущення

- Нотатка базується тільки на transcript Section 6 і файлі `2_agent_loop_raw_function_calling.py`.
- Production-рекомендації нижче позначені окремо як additional backend / production context.

### Невідоме / не підтверджено джерелом

- Unknown / Not confirmed from source: повна формальна специфікація Ollama tool JSON schema.
- Unknown / Not confirmed from source: точна поведінка Anthropic/OpenAI/Gemini schemas у деталях, бо source лише порівнює conceptually.
- Unknown / Not confirmed from source: чи всі Ollama models однаково добре підтримують function calling.

---

## 2. Чому це важливо

### Пояснення на основі джерела

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

Це показує cost of abstraction removal: контроль більший, але більше коду, vendor-specific details і maintenance.

### Додатковий backend / production context

Це типовий trade-off у platform engineering:

| Approach | Benefit | Cost |
|---|---|---|
| LangChain abstraction | швидше розробляти, менше boilerplate, простіше switch provider | менше контролю, залежність від framework behavior |
| Raw SDK | повний контроль, видно provider-specific behavior | більше schema/message boilerplate, важча portability, більше integration bugs |

---

## 3. Як це працює

### Пояснення на основі джерела

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

#### Step 3 — Tools як plain Python functions

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

Manual JSON schema — це representation tool contract для LLM. У source прямо сказано: це те, що LangChain `@tool` генерував автоматично з function signature і docstring.

Перший schema описує `get_product_price`:

- function name: `get_product_price`;
- description: lookup price in catalog;
- required argument: `product`;
- product type: `string`.

Другий schema описує `apply_discount`:

- `price` має type `number`;
- `discount_tier` має type `string`;
- обидва required.

#### Step 5 — Ollama auto-generation note

Source code зазначає, що Ollama може auto-generate schemas, якщо передати Python functions напряму як tools. Але для цього docstrings мають відповідати Google docstring format.

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

Source каже, що в інших vendors naming/format може відрізнятись.

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

## 4. Backend аналогія

### Пояснення на основі джерела

Layer 2 показує той самий agent loop, але з raw SDK і manual contracts.

### Додатковий backend / production context

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

Це схоже на написання integration adapter вручну замість використання framework-level abstraction.

---

## 5. Production relevance

### Пояснення на основі джерела

Source явно показує такі production-relevant concerns:

1. Without LangChain, schemas are manual.
2. Ollama schema conventions differ from other vendors.
3. Ollama can accept Python functions directly, but only with Google-style docstrings for auto-parsing.
4. Without LangChain, messages are provider-specific dicts.
5. Without LangChain, tracing LLM calls must be added manually.
6. Vendor switching without LangChain has high development cost.
7. Function calling still returns structured function name + arguments, but application executes the tool.

### Додатковий backend / production context

#### Reliability risks

- Manual schemas можуть drift від actual Python function signatures.
- Required fields у schema можуть не відповідати runtime function args.
- Vendor-specific response shape може зламати parser code.
- Відсутність `tool_call_id` може ускладнити correlation.
- Silent default `0` для unknown product/tier може створити wrong business answer.

#### Security risks

- Tool name з model output має бути allowlisted через `tools_dict`.
- Tool arguments треба validate перед function execution.
- Не expose arbitrary Python functions для LLM-controlled dispatch.
- Tool schemas не мають expose sensitive internal capabilities.

#### Performance / cost risks

- Кожна loop iteration — це LLM call.
- Provider-specific manual integration збільшує maintenance cost.
- Bigger schemas/messages збільшують prompt size.
- Local Ollama уникає external API cost, але використовує local compute, і model quality може vary.

#### Observability concerns

- Raw SDK calls потребують manual instrumentation.
- Trace має включати iteration number, model response, selected tool, arguments, observation і final answer.
- Без framework help trace consistency стає developer responsibility.

### Version-sensitive

Ця нотатка version-sensitive, бо:

- Ollama SDK response objects і `tool_calls` structure можуть змінитися.
- Ollama support для passing Python functions directly as tools залежить від SDK behavior.
- LangSmith `@traceable` behavior може vary by package version.
- Provider-specific tool schema formats не гарантовано identical.

### Potential issue

Source transcript каже, що Ollama documentation не clearly define all details of JSON schema. Treat exact schema requirements as provider-specific і verify against current Ollama docs/source before production use.

Інший potential issue: source code має comment `# --- Tools (LangChain @tool decorator) ---`, але actual code вже не використовує LangChain `@tool`; він використовує `@traceable`. Це likely leftover comment.

---

## 6. Key terms

### Пояснення на основі джерела

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

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що LangChain `@tool` — це лише syntactic sugar.
   - Source показує, що він приховує schema generation і vendor-specific formatting.

2. Думати, що всі providers використовують однакову tool schema.
   - Transcript каже, що Ollama і Anthropic schemas differ.

3. Думати, що Ollama function auto-conversion працює з будь-яким docstring.
   - Source каже, що потрібен Google-style docstrings.

4. Зберігати LangChain-style message assumptions при використанні raw SDK.
   - Raw Ollama використовує dicts і власну response shape.

5. Намагатися використовувати `tool.invoke(...)` після видалення LangChain tools.
   - У raw version tools — plain functions і викликаються напряму.

6. Забути manual tracing.
   - Без LangChain source додає `ollama_chat_traced` вручну.

### Додатковий backend / production context

7. Schema drift.
   - Function signature змінюється, а JSON schema — ні.

8. Weak argument validation.
   - Model-produced `tool_args` не можна blindly trust.

9. Inconsistent provider adapters.
   - Raw code часто перетворюється на scattered vendor-specific logic, якщо не ізолювати його clean interfaces.

10. Treating raw SDK code as simpler.
   - Для одного provider це може бути simple, але стає expensive, коли є multiple providers, tracing, retries, schemas і evals.

---

## 8. Flashcards

| Question | Answer |
|---|---|
| Про що Layer 2? | Про реалізацію того самого agent loop без LangChain objects, через raw Ollama SDK і manual JSON tool schemas. |
| Що замінює LangChain `@tool`? | Plain Python functions плюс manual JSON schemas у `tools_for_llm`. |
| Що приховує LangChain `@tool` according to source? | JSON schema generation із function name, docstring, type hints і arguments. |
| Що замінює `llm_with_tools.invoke(...)`? | `ollama.chat(...)`, обгорнутий у `ollama_chat_traced`. |
| Що замінює `SystemMessage` і `HumanMessage`? | Raw dictionaries з `role` і `content`. |
| Що замінює `ToolMessage`? | Raw dictionary з `role: "tool"` і `content`, рівним observation. |
| Як читається selected tool name в Ollama response? | Через `tool_call.function.name`. |
| Як читаються tool arguments в Ollama response? | Через `tool_call.function.arguments`. |
| Як виконується tool у raw version? | Через direct Python call: `tool_to_use(**tool_args)`. |
| Чому vendor switching складніший без LangChain? | Tool schemas, message formats, SDK calls і response shapes можуть відрізнятися між providers. |
| Чому manual JSON schema risky? | Вона може drift від real function signatures і створити runtime bugs. |
| Головний lesson Layer 2? | Function calling — structured API behavior, не magic; LangChain переважно зменшує integration boilerplate. |

---

## 9. Interview Q&A

### Q1: Яку проблему демонструє Layer 2?

**Answer:** Він демонструє, що LangChain abstracts away під час tool-calling agents: tool schema generation, message formatting, SDK invocation, tool dispatch format і tracing integration.

### Q2: Чим raw function calling відрізняється від LangChain tool calling?

**Answer:** У LangChain tools decorated with `@tool`, bound with `bind_tools`, invoked through `tool.invoke`, а observations надсилаються через `ToolMessage`. У raw Ollama schemas пишуться manually, `ollama.chat` викликається напряму, tool calls парсяться з Ollama response objects, tools викликаються як Python functions, а observations append як raw dicts.

### Q3: Навіщо JSON schemas?

**Answer:** LLM потрібні structured descriptions available tools: function name, description, parameters, types і required arguments. Це дозволяє model return structured tool calls.

### Q4: Чому documentation clarity важлива?

**Answer:** Без clear formal schema definition developers мають infer required schema shape з examples або source code, що збільшує integration risk.

### Q5: Чому provider portability дорога без LangChain?

**Answer:** Different providers можуть мати різні schema formats, role names, SDK request shapes і response structures. Switching providers може вимагати rewrite integration code.

### Q6: Яка роль `tools_dict`?

**Answer:** Він maps model-selected tool names to actual Python functions, щоб application code міг execute selected tool.

### Q7: Що таке observation у raw implementation?

**Answer:** Це result executing Python function selected by model. Observation converts to string і appends to messages as `tool` role message.

### Q8: Чому потрібен manual tracing?

**Answer:** Без LangChain model abstractions LangSmith не обгортає raw Ollama call automatically, тому source створює `ollama_chat_traced` з `@traceable(run_type="llm")`.

### Q9: Який production risk від manual JSON schemas?

**Answer:** Schema drift: Python function signature може змінитися, а JSON schema лишиться stale, causing wrong arguments, missing required fields or runtime errors.

### Q10: Головний lesson removing LangChain у Layer 2?

**Answer:** LangChain не magic; він standardizes common integration tasks. Removing it exposes raw mechanics і maintenance cost provider-specific implementation.

---

## 10. Self-check

Answer without looking:

1. Який file implements Layer 2?
2. Які imports залишаються після removing LangChain objects?
3. Що замінює `@tool`?
4. Що таке `tools_for_llm`?
5. Що робить `ollama_chat_traced`?
6. Чому `tools_dict` написаний вручну?
7. Як читати selected tool name в Ollama response?
8. Як execute selected tool?
9. Що замінює `ToolMessage`?
10. Чому provider switching складніший у raw SDK code?

Expected answers:

1. `2_agent_loop_raw_function_calling.py`.
2. `load_dotenv`, `ollama`, `traceable`.
3. Plain Python functions плюс manual JSON schemas і `@traceable` для tracing.
4. List manual JSON schemas describing tools for the LLM.
5. Wraps `ollama.chat(...)` і traces it as an LLM call in LangSmith.
6. Бо немає LangChain tool objects із `.name`; mapping потрібен для dispatch.
7. `tool_call.function.name`.
8. `tool_to_use(**tool_args)`.
9. Raw dict: `{"role": "tool", "content": str(observation)}`.
10. Бо schemas, message roles, SDK calls і response structures provider-specific.

---

## 11. Міні-практика

### Практика на основі джерела

Запусти Layer 2:

```bash
uv run python 2_agent_loop_raw_function_calling.py
```

Перевір expected loop:

```text
Iteration 1: get_product_price(product='laptop') -> 1299.99
Iteration 2: apply_discount(price=1299.99, discount_tier='gold') -> 1000.99
Iteration 3: no tool calls -> final answer
```

Потім переглянь LangSmith trace і підтвердь:

- trace name is `Ollama Agent Loop`;
- LLM call is `Ollama Chat`;
- tool calls are traced separately;
- observation is appended as raw `tool` role message.

### Додатковий backend / production context task

Покращ raw implementation safety:

1. Add validation that `tool_name` is allowlisted.
2. Validate `tool_args` against expected argument names.
3. Replace silent `0` defaults with explicit errors.
4. Add a small test list with valid and invalid queries.
5. Add a comment explaining where schema drift can happen.

### Unknowns

- Unknown / Not confirmed from source: exact LangSmith trace output on your machine.
- Unknown / Not confirmed from source: exact Ollama SDK response object structure in future versions.
- Unknown / Not confirmed from source: whether the same JSON schema works unchanged across other providers.
