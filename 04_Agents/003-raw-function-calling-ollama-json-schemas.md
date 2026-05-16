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
source_type: mixed
source_confidence: medium
verified_against_external_sources: 2026-05-16
external_sources:
  - Ollama documentation: Tool calling capability
  - LangChain documentation: Tool calling and tool abstraction
  - LangSmith documentation: traceable decorator / custom instrumentation
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

### External documentation verification

Перевірка Ollama docs підтвердила загальну ідею: tool calling у raw Ollama SDK передбачає передачу `tools` у chat call, model повертає `tool_calls`, application виконує відповідні functions, а result потім додається назад у conversation як tool message.

Важлива correction: у documented Ollama examples tool-result message містить `role: "tool"`, `content` і `tool_name`. У попередній версії нотатки tool result був описаний тільки як `{role: "tool", content: ...}`. Для production/raw SDK code краще орієнтуватися на documented shape з `tool_name`, якщо поточна версія SDK його очікує.

### Додатковий backend / production context

Це корисна вправа для AI Platform Engineer, бо production AI systems часто потребують розуміння нижнього рівня abstraction. Якщо framework ламається, треба розуміти, що реально відбувається:

```text
LLM request + tools schema -> structured tool_calls -> app dispatch -> tool result -> tool message -> next LLM request
```

### Припущення

- Нотатка базується на transcript Section 6 і файлі `2_agent_loop_raw_function_calling.py`.
- External verification використано для уточнення Ollama message shape і status of framework abstractions.
- Production-рекомендації нижче позначені окремо як additional backend / production context.

### Невідоме / не підтверджено джерелом

- Unknown / Not confirmed from source: повна формальна специфікація Ollama tool JSON schema в усіх версіях SDK.
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

У Layer 2 це треба писати вручну через tool schema / JSON-like function description.

Це показує cost of abstraction removal: контроль більший, але більше коду, vendor-specific details і maintenance.

### Додатковий backend / production context

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

#### Step 2 — Tools як plain Python functions

```python
@traceable(run_type="tool")
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)
```

```python
@traceable(run_type="tool")
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers: bronze, silver, gold."""
    discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentages.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)
```

Тут немає LangChain `@tool`. Function залишається звичайною Python function, але обгорнута `@traceable(run_type="tool")`, щоб LangSmith бачив її як tool run.

#### Step 3 — Manual JSON schemas

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

#### Step 4 — Ollama auto-generation note

Source code зазначає, що Ollama може auto-generate schemas, якщо передати Python functions напряму як tools. Але для цього docstrings мають відповідати Google docstring format.

External verification: current Ollama docs також показують, що Python functions можуть передаватися як tools напряму. Деталі docstring parsing/version behavior залишаються version-sensitive.

#### Step 5 — Manual traced LLM call

```python
@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(messages):
    return ollama.chat(model=MODEL, tools=tools_for_llm, messages=messages)
```

Без LangChain tracing не приходить автоматично на такому рівні abstraction. Тому автор створює wrapper function і вручну ставить `@traceable`.

#### Step 6 — Manual tool registry

```python
tools_dict = {
    "get_product_price": get_product_price,
    "apply_discount": apply_discount,
}
```

У LangChain version registry будувався через tool objects і `t.name`. Тут mapping пишеться вручну.

#### Step 7 — Raw messages

```python
messages = [
    {"role": "system", "content": (...)},
    {"role": "user", "content": question},
]
```

LangChain `SystemMessage` і `HumanMessage` прибрані. Використовуються plain dictionaries, які відповідають Ollama SDK expected format.

#### Step 8 — Raw agent loop

```python
response = ollama_chat_traced(messages=messages)
ai_message = response.message
tool_calls = ai_message.tool_calls
```

`response` — Ollama response, не LangChain `AIMessage`.

#### Step 9 — Tool call parsing

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

#### Step 10 — Direct function call

```python
tool_to_use = tools_dict.get(tool_name)
if tool_to_use is None:
    raise ValueError(f"Tool '{tool_name}' not found")

observation = tool_to_use(**tool_args)
```

Без LangChain `tool.invoke(...)`. Tool виконується як звичайна Python function з unpacked keyword arguments.

#### Step 11 — Append raw tool message

Source transcript описував raw tool result як dict із `role: "tool"` і `content`. External docs показують documented version із `tool_name`:

```python
messages.append({
    "role": "tool",
    "content": str(observation),
    "tool_name": tool_name,
})
```

Production recommendation: use the provider-documented message shape for your installed SDK version.

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
| `{"role": "tool", "content": ..., "tool_name": ...}` | result event/message added to workflow history with correlation metadata |
| manual `@traceable` | manual instrumentation / spans |

---

## 5. Production relevance

### Пояснення на основі джерела

Source явно показує такі production-relevant concerns:

1. Without LangChain, schemas are manual.
2. Ollama schema conventions differ from other vendors.
3. Ollama can accept Python functions directly, but docstring conventions are version-sensitive.
4. Without LangChain, messages are provider-specific dicts.
5. Without LangChain, tracing LLM calls must be added manually.
6. Vendor switching without LangChain has high development cost.
7. Function calling still returns structured function name + arguments, but application executes the tool.

### External documentation verification

Ollama docs confirm provider-specific raw shape matters. The raw SDK flow is not a universal standard: tool schema, tool call response shape and tool result message shape should be verified against the exact SDK/provider version.

### Додатковий backend / production context

#### Reliability risks

- Manual schemas можуть drift від actual Python function signatures.
- Required fields у schema можуть не відповідати runtime function args.
- Vendor-specific response shape може зламати parser code.
- Missing `tool_name` in tool result messages can make provider behavior/correlation worse if SDK expects it.
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
- Raw tool-result message shape, including `tool_name`, should be verified against current Ollama SDK docs.

### Potential issue

Corrected: попередня версія нотатки описувала raw tool result only as `{role: "tool", content: ...}`. External docs show a `tool_name` field in tool-result messages. Для production note тепер вказано documented shape with `tool_name`.

Source code має comment `# --- Tools (LangChain @tool decorator) ---`, але actual code вже не використовує LangChain `@tool`; він використовує `@traceable`. Це likely leftover comment.

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
| `tool_name` | Provider-documented metadata linking tool result message to executed tool |
| raw message dict | Provider-specific message object with `role`, `content`, and sometimes provider-required fields |
| provider-specific format | Different vendors may expect different schema/message structures |

---

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що LangChain `@tool` — це лише syntactic sugar.
   - Source показує, що він приховує schema generation і vendor-specific formatting.

2. Думати, що всі providers використовують однакову tool schema.
   - Transcript каже, що Ollama і Anthropic schemas differ.

3. Думати, що Ollama function auto-conversion працює з будь-яким docstring.
   - Source каже, що потрібен Google-style docstrings; exact behavior version-sensitive.

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

10. Ignoring provider-documented message fields.
   - Example: missing `tool_name` in Ollama tool-result message can break or degrade raw SDK behavior depending on version.

---

## 8. Flashcards

Q: Про що Layer 2?
A: Про реалізацію того самого agent loop без LangChain objects, через raw Ollama SDK і manual JSON tool schemas.

Q: Що замінює LangChain `@tool`?
A: Plain Python functions плюс manual JSON schemas у `tools_for_llm`.

Q: Що приховує LangChain `@tool` according to source?
A: JSON schema generation із function name, docstring, type hints і arguments.

Q: Що замінює `llm_with_tools.invoke(...)`?
A: `ollama.chat(...)`, обгорнутий у `ollama_chat_traced`.

Q: Що замінює `SystemMessage` і `HumanMessage`?
A: Raw dictionaries з `role` і `content`.

Q: Що треба додавати в Ollama tool-result message за external docs?
A: `role: "tool"`, `content` і `tool_name`.

Q: Як читається selected tool name в Ollama response?
A: Через `tool_call.function.name`.

Q: Як читаються tool arguments в Ollama response?
A: Через `tool_call.function.arguments`.

Q: Як виконується tool у raw version?
A: Через direct Python call: `tool_to_use(**tool_args)`.

Q: Чому vendor switching складніший без LangChain?
A: Tool schemas, message formats, SDK calls і response shapes можуть відрізнятися між providers.

Q: Чому manual JSON schema risky?
A: Вона може drift від real function signatures і створити runtime bugs.

Q: Головний lesson Layer 2?
A: Function calling — structured API behavior, не magic; LangChain переважно зменшує integration boilerplate.

---

## 9. Interview Q&A

### Q1: Яку проблему демонструє Layer 2?

**Answer:** Він демонструє, що LangChain abstracts away під час tool-calling agents: tool schema generation, message formatting, SDK invocation, tool dispatch format і tracing integration.

### Q2: Чим raw function calling відрізняється від LangChain tool calling?

**Answer:** У LangChain tools decorated with `@tool`, bound with `bind_tools`, invoked through `tool.invoke`, а observations надсилаються через `ToolMessage`. У raw Ollama schemas пишуться manually, `ollama.chat` викликається напряму, tool calls парсяться з Ollama response objects, tools викликаються як Python functions, а observations append як raw dicts.

### Q3: Навіщо JSON schemas?

**Answer:** LLM потрібні structured descriptions available tools: function name, description, parameters, types і required arguments. Це дозволяє model return structured tool calls.

### Q4: Яка correction після перевірки Ollama docs?

**Answer:** Tool result message should include `tool_name` along with `role: "tool"` and `content`, based on documented Ollama examples.

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
9. Що external docs додають до raw tool-result message?
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
9. `tool_name` in addition to `role: "tool"` and `content`.
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
- observation is appended as raw tool role message;
- raw Ollama message shape matches current docs, including `tool_name` if required.

### Додатковий backend / production context task

Покращ raw implementation safety:

1. Add validation that `tool_name` is allowlisted.
2. Validate `tool_args` against expected argument names.
3. Replace silent `0` defaults with explicit errors.
4. Add `tool_name` to the tool result message if using documented Ollama shape.
5. Add a comment explaining where schema drift can happen.

### Unknowns

- Unknown / Not confirmed from source: exact LangSmith trace output on your machine.
- Unknown / Not confirmed from source: exact Ollama SDK response object structure in future versions.
- Unknown / Not confirmed from source: whether the same JSON schema works unchanged across other providers.
