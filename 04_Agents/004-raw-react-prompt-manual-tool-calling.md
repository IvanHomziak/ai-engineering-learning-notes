---
type: daily-review-note
topic: Layer 3 Raw ReAct Prompt: ручний tool calling без function calling
area: Agents
date: 2026-05-12
tags:
- agents
- react-prompt
- manual-tool-calling
- raw-agent-loop
- regex-parsing
- scratchpad
- ollama
- langsmith
- prompt-engineering
- ai-platform-engineering
status: active-review
review:
- 2026-05-13
- 2026-05-15
- 2026-05-19
- 2026-05-26
- 2026-06-11
---

# Щоденна нотатка для повторення: Layer 3 Raw ReAct Prompt — ручний tool calling без function calling

## 1. Основна ідея

### Пояснення на основі джерела

Layer 3 показує найнижчий рівень реалізації agent у цьому section: agent працює **без LangChain tool abstraction** і **без function calling API**.

Замість structured `tool_calls` model отримує великий ReAct prompt і має відповісти plain text у форматі:

```text
Thought: ...
Action: ...
Action Input: ...
Observation: ...
...
Final Answer: ...
```

Application code потім:

1. читає raw text output від LLM;
2. через regex шукає `Final Answer` або `Action` + `Action Input`;
3. виконує відповідний Python tool;
4. додає реальний `Observation` у scratchpad;
5. повторює loop.

Це демонструє, що function calling можна концептуально відтворити через prompt engineering + parsing + tool dispatch.

### Додатковий backend / production context

Ментальна модель:

```text
LLM не викликає tools.
LLM генерує text protocol.
Application парсить protocol і виконує tools.
```

Це схоже на крихкий text-based RPC protocol, де model output є command string, а Python application — command executor.

### Припущення

- Нотатка базується на transcript Section 7 і файлі `3_raw_react_prompt.py`.
- Production-коментарі явно відокремлені від source-based explanation.

### Невідоме / не підтверджено джерелом

- Unknown / Not confirmed from source: повна prompt engineering theory за ReAct prompt, бо transcript відсилає до Theory section, але її зміст тут не надано.
- Unknown / Not confirmed from source: точна історична першість LangChain ReAct agent implementation поза твердженнями transcript.
- Unknown / Not confirmed from source: фактична кількість downloads prompt `hwchase17/react` на поточну дату.

---

## 2. Чому це важливо

### Пояснення на основі джерела

Цей layer важливий, бо показує foundation function calling:

- function calling дає structured API response;
- ReAct prompt робить схожу логіку через plain text protocol;
- tool descriptions вставляються прямо в prompt;
- tool names вставляються прямо в prompt;
- scratchpad зберігає history agent actions and observations;
- regex parsing замінює structured response parsing.

Source позиціонує ReAct prompt як фундамент agent behavior: LLM використовується як reasoning engine, який вирішує, яку дію виконати далі.

### Додатковий backend / production context

Для AI Platform / LLM Infrastructure engineer це важливо, бо:

1. Показує, що agentic behavior можна реалізувати без спеціального API.
2. Пояснює, чому function calling зʼявився як надійніший structured layer поверх prompt-only agents.
3. Пояснює failure modes agentів: format drift, hallucinated observations, parsing failure, wrong tool args, infinite loop.
4. Допомагає дебажити сучасні agents, бо під structured abstractions усе одно є decision loop.

---

## 3. Як це працює

### Пояснення на основі джерела

#### Step 1 — Imports

```python
import re
import inspect
from dotenv import load_dotenv

load_dotenv()

import ollama
from langsmith import traceable
```

- `re` потрібен для regex parsing raw text output.
- `inspect` потрібен для отримання metadata functions: signature і docstring.
- `ollama` використовується напряму, без function calling tools.
- `traceable` використовується для LangSmith tracing.

#### Step 2 — Tools залишаються Python functions

```python
@traceable(run_type="tool")
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog."""
    print(f"    >> Executing get_product_price(product='{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)
```

```python
@traceable(run_type="tool")
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers: bronze, silver, gold."""
    print(f"    >> Executing apply_discount(price={price}, discount_tier='{discount_tier}')")
    price = float(price)
    discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentages.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)
```

У Layer 3 ці functions не передаються в model через `tools=`. Вони існують тільки в application code.

#### Step 3 — Tool registry

```python
tools = {
    "get_product_price": get_product_price,
    "apply_discount": apply_discount,
}
```

Це allowlist / registry. Коли regex витягне `Action`, application перевірить, чи така дія є в `tools`.

#### Step 4 — Dynamic tool descriptions

```python
def get_tool_descriptions(tools_dict):
    descriptions = []
    for tool_name, tool_function in tools_dict.items():
        original_function = getattr(tool_function, "__wrapped__", tool_function)
        signature = inspect.signature(original_function)
        docstring = inspect.getdoc(tool_function) or ""
        descriptions.append(f"{tool_name}{signature} - {docstring}")
    return "\n".join(descriptions)
```

Line-by-line:

- `descriptions = []` — накопичує text descriptions для tools.
- `for tool_name, tool_function in tools_dict.items()` — проходить по registry.
- `getattr(..., "__wrapped__", ...)` — бере original function, якщо вона обгорнута decorator-ом `@traceable`.
- `inspect.signature(original_function)` — отримує function signature, наприклад `(product: str) -> float`.
- `inspect.getdoc(tool_function) or ""` — бере docstring.
- `descriptions.append(...)` — формує один text line для tool.
- `"\n".join(descriptions)` — обʼєднує всі tool descriptions в один string для prompt.

#### Step 5 — Tool descriptions and names

```python
tool_descriptions = get_tool_descriptions(tools)
tool_names = ", ".join(tools.keys())
```

`tool_descriptions` містить name + signature + docstring.

`tool_names` містить тільки список доступних action names:

```text
get_product_price, apply_discount
```

#### Step 6 — ReAct prompt

Prompt містить:

- strict rules;
- tool descriptions;
- allowed tool names;
- expected response format;
- user question placeholder;
- initial `Thought:` marker.

Ключове: tools тепер “live inside the prompt as plain text”. LLM не отримує structured function calling schema.

#### Step 7 — Raw Ollama call без tools

```python
@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(model, messages, options):
    return ollama.chat(model=model, messages=messages, options=options)
```

Тут немає `tools=...`. Agency виникає з prompt і regex parsing.

#### Step 8 — Runtime prompt і scratchpad

```python
prompt = react_prompt.format(question=question)
scratchpad = ""
```

- `prompt` — ReAct prompt із runtime user question.
- `scratchpad` — history agent execution, initially empty.

#### Step 9 — Loop with full prompt

```python
for iteration in range(1, MAX_ITERATIONS + 1):
    full_prompt = prompt + scratchpad
```

На кожній ітерації LLM отримує один великий text prompt:

```text
base ReAct prompt + all previous Thought/Action/Observation history
```

#### Step 10 — Stop token

```python
options={"stop": ["\nObservation"], "temperature": 0}
```

`stop: ["\nObservation"]` зупиняє model перед тим, як вона згенерує власну hallucinated observation. Реальний observation має вставити application після tool execution.

#### Step 11 — Raw LLM output

```python
output = response.message.content
```

У Layer 3 немає `AIMessage` object і `tool_calls`. Є тільки text.

#### Step 12 — Final answer parsing

```python
final_answer_match = re.search(r"Final Answer:\s*(.+)", output)
```

Якщо LLM написала `Final Answer: ...`, loop завершується.

#### Step 13 — Action parsing

```python
action_match = re.search(r"Action:\s*(.+)", output)
action_input_match = re.search(r"Action Input:\s*(.+)", output)
```

Якщо final answer немає, code шукає action protocol у raw text.

#### Step 14 — Parse and normalize args

```python
raw_args = [x.strip() for x in tool_input_raw.split(",")]
args = [x.split("=", 1)[-1].strip().strip("'\"") for x in raw_args]
```

Це перетворює comma-separated text у list args. Якщо LLM повернула `key=value`, code відкидає key і бере value.

#### Step 15 — Execute tool або return tool error observation

```python
if tool_name not in tools:
    observation = f"Error: Tool '{tool_name}' not found. Available tools: {list(tools.keys())}"
else:
    observation = str(tools[tool_name](*args))
```

Якщо action name не в registry — observation стає error message. Якщо tool існує — виконується Python function.

#### Step 16 — Update scratchpad

```python
scratchpad += f"{output}\nObservation: {observation}\nThought:"
```

Це додає model output, real observation і новий `Thought:` marker для наступної ітерації.

---

## 4. Backend аналогія

### Пояснення на основі джерела

Layer 3 реалізує manual protocol:

```text
Prompt text -> LLM text output -> regex parser -> tool registry -> Python execution -> scratchpad append -> repeat
```

### Додатковий backend / production context

| ReAct component | Backend analogy |
|---|---|
| ReAct prompt | text-based protocol specification |
| `Action` | command name |
| `Action Input` | command payload |
| regex parser | protocol parser |
| `tools` dictionary | command handler registry / allowlist |
| Python function | command handler / domain service |
| `Observation` | command result / event result |
| scratchpad | workflow state / execution log |
| stop token | output boundary / protocol delimiter |
| `MAX_ITERATIONS` | loop guard / circuit-breaker-like safety limit |

Це схоже на mini workflow runtime, де model генерує commands як text, а application їх інтерпретує.

---

## 5. Production relevance

### Пояснення на основі джерела

Source демонструє такі production-relevant mechanics:

1. Без function calling LLM output є raw text.
2. Raw text треба парсити вручну.
3. Regex parsing fragile, якщо model не дотримується format.
4. Stop token не дає model вигадати `Observation`.
5. Scratchpad зберігає history tool choices і observations.
6. Tool descriptions треба вручну inject у prompt.
7. Function metadata можна генерувати динамічно через `inspect`.
8. Tool execution залишається відповідальністю application.

### Додатковий backend / production context

#### Reliability risks

- LLM може не дотриматися required text format.
- Regex може витягнути wrong action або wrong action input.
- Comma-separated parsing ламається для complex arguments.
- Scratchpad може рости й збільшувати token usage.
- Wrong stop token може дозволити hallucinated observations.
- Model може згенерувати invalid tool name.
- Tool може отримати wrong argument count або invalid types.

#### Security risks

- Text protocol може бути prompt-injected.
- User input може спробувати вплинути на `Action` або `Observation` formatting.
- Не виконуй arbitrary tool names із model output.
- Тримай registry allowlisted.
- Validate arguments before tool execution.
- Не expose sensitive tool descriptions, якщо це не потрібно.

#### Performance risks

- Кожна iteration відправляє full prompt + scratchpad знову.
- Token usage росте з кожним step.
- Regex retries/failures можуть додавати latency.
- Local model behavior може бути inconsistent залежно від model quality.

#### Observability concerns

Trace має фіксувати:

- full prompt або sanitized prompt;
- raw model output;
- regex parsing result;
- selected tool;
- parsed args;
- observation;
- final answer;
- parse failures.

### Version-sensitive

Ця нотатка version-sensitive, бо:

- Ollama SDK response shape може змінитися.
- `options={"stop": [...]}` behavior provider/model/runtime-specific.
- LangSmith `@traceable` behavior може залежати від package version.
- Model adherence to ReAct format залежить від model capability і prompt.

### Potential issue

1. Transcript дублює lecture title/content для `36. Generating Dynamic Tool Descriptions in Python`.
2. Source code comment каже `# --- Tools (LangChain @tool decorator) ---`, але code використовує `@traceable`, не LangChain `@tool`; ймовірно leftover comment.
3. Raw argument parser використовує comma split, що fragile для complex inputs.
4. `get_product_price` повертає `0` для unknown product; toy example, risky in production.
5. `apply_discount` повертає no-error result для unknown discount tier через `0` discount; toy example, risky in production.

---

## 6. Key terms

### Пояснення на основі джерела

| Term | Meaning |
|---|---|
| ReAct prompt | Prompt format, який керує Thought / Action / Action Input / Observation / Final Answer behavior |
| Thought | Model reasoning step у text output |
| Action | Tool/function name, який model пропонує виконати |
| Action Input | Input string для selected action |
| Observation | Реальний result tool execution, який application додає назад |
| Scratchpad | Accumulated history of thoughts, actions, inputs and observations |
| Regex parsing | Витягування `Action`, `Action Input` або `Final Answer` із raw text output |
| Stop token | Generation boundary, який зупиняє model перед hallucinated observation |
| Tool description | Text із function signature і docstring, injected into prompt |
| `inspect.signature` | Python function для читання function signature |
| `inspect.getdoc` | Python function для читання docstring |
| `__wrapped__` | Attribute для доступу до original function behind decorator wrapper |
| Manual tool calling | Application parses model text and invokes Python function itself |

---

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що function calling обовʼязковий для agents.
   - Source показує, що ReAct prompt може реалізувати agent behavior без function calling.

2. Думати, що model знає Python functions автоматично.
   - Tool descriptions треба передати в prompt, бо LLM inherently не знає application functions.

3. Дозволяти model генерувати `Observation`.
   - Source використовує stop token, щоб application вставляв real tool result.

4. Забути scratchpad.
   - Без scratchpad наступна iteration не знає previous actions and observations.

5. Сприймати regex parsing як reliable.
   - Source code comment прямо каже, що це fragile, якщо LLM не дотримується format.

6. Плутати `tool_descriptions` і `tool_names`.
   - `tool_descriptions` містить signature/docstring; `tool_names` — тільки allowed action names.

### Додатковий backend / production context

7. Використовувати raw ReAct для high-risk production actions.
   - Prompt-only tool selection слабший за structured, validated protocols.

8. Не мати schema validation для action inputs.
   - Comma splitting недостатній для real domain inputs.

9. Не обмежувати scratchpad size.
   - Long-running loops можуть перевищити context/cost limits.

10. Логувати full prompts із secrets.
   - Якщо tool descriptions або user inputs містять sensitive data, traces треба sanitize.

---

## 8. Flashcards

| Question | Answer |
|---|---|
| Про що Layer 3? | Про реалізацію agent без function calling через ReAct prompt, regex parsing і scratchpad. |
| Що замінює structured `tool_calls`? | Raw text output із `Action` і `Action Input`. |
| Навіщо import `re`? | Щоб парсити `Final Answer`, `Action` і `Action Input` із raw LLM text. |
| Навіщо import `inspect`? | Щоб витягнути function signatures і docstrings для dynamic tool descriptions. |
| Що таке `tool_descriptions`? | String із tool names, signatures і docstrings, injected into ReAct prompt. |
| Що таке `tool_names`? | Comma-separated list allowed action names, injected into prompt. |
| Що таке scratchpad? | Growing text history model output, real observations і наступного `Thought:` marker. |
| Навіщо stop token `\nObservation`? | Щоб model не hallucinate observation до того, як application вставить real tool result. |
| Що відбувається, якщо знайдено `Final Answer`? | Loop повертає parsed final answer. |
| Що відбувається, якщо знайдено `Action`? | Application парсить tool name/input і виконує matching tool. |
| Чому raw ReAct fragile? | Він залежить від exact text format і коректної роботи regex parsing. |
| Головний lesson Layer 3? | Function calling — structured version behavior, який можна приблизно відтворити через prompt protocol + parser + tool executor. |

---

## 9. Interview Q&A

### Q1: Що таке ReAct prompt?

**Answer:** Це prompt format, який змушує model reason and act через повторювані `Thought`, `Action`, `Action Input` і `Observation`, доки вона не видасть `Final Answer`.

### Q2: Чим Layer 3 відрізняється від Layer 2?

**Answer:** Layer 2 використовує structured function calling з Ollama. Layer 3 повністю прибирає function calling: model output — plain text, а application парсить tool intent через regex.

### Q3: Навіщо application потрібен `inspect`?

**Answer:** Щоб через `inspect.signature` і `inspect.getdoc` зібрати tool descriptions із Python functions і inject їх у prompt.

### Q4: Для чого scratchpad?

**Answer:** Scratchpad зберігає prior model outputs і real tool observations, щоб наступна iteration мала execution history.

### Q5: Чому stop token важливий?

**Answer:** Він зупиняє LLM перед генерацією `Observation`, бо observation має бути real result application tool execution, а не hallucination.

### Q6: Чому regex parsing risky?

**Answer:** Якщо model не дотримується exact expected format, regex може fail або витягнути wrong data, що призведе до wrong tool execution або loop failure.

### Q7: Чи LLM знає tools автоматично?

**Answer:** Ні. Code injects tool names, signatures і docstrings into prompt, щоб model могла reason about available tools.

### Q8: Яка роль `tools` dictionary?

**Answer:** Він мапить parsed action names на executable Python functions і працює як allowlist для tool execution.

### Q9: Як Layer 3 approximate function calling?

**Answer:** Prompt просить model output tool name і arguments як text; regex їх parses; application code виконує tool і додає observation.

### Q10: Чи варто використовувати raw ReAct style напряму в production?

**Answer:** Тільки дуже обережно і зазвичай не для high-risk actions. Для production потрібні stronger validation, structured outputs, guardrails, tracing, timeouts і policy checks.

---

## 10. Self-check

Answer without looking:

1. Які два Python modules додаються в Layer 3 і навіщо?
2. Чому function calling прибрали?
3. Що inject у `{tool_descriptions}`?
4. Що inject у `{tool_names}`?
5. Навіщо `get_tool_descriptions` використовує `__wrapped__`?
6. Що запобігає `stop: ["\nObservation"]`?
7. Що regex шукає першим: final answer чи action?
8. Як action inputs перетворюються у function args?
9. Що стається, якщо parsed tool name не в `tools`?
10. Чому scratchpad завершується `Thought:`?

Expected answers:

1. `re` для regex parsing і `inspect` для читання function metadata.
2. Щоб показати, як agent/tool calling працює через raw prompt engineering без structured tool API.
3. Tool name + function signature + docstring для кожного tool.
4. Allowed action names: `get_product_price, apply_discount`.
5. Щоб отримати original function behind `@traceable` wrapper.
6. Вона не дає model hallucinate tool result.
7. Спочатку перевіряється `Final Answer`.
8. Через split comma-separated text і stripping optional `key=` prefixes та quotes.
9. Observation стає error message із available tools.
10. Щоб підказати model продовжити reasoning у наступній iteration.

---

## 11. Міні-практика

### Практика на основі джерела

Запусти Layer 3:

```bash
uv run python 3_raw_react_prompt.py
```

Перевір expected behavior:

1. First LLM output містить `Action: get_product_price` і `Action Input: laptop`.
2. Application виконує `get_product_price` і додає real `Observation`.
3. Second iteration вибирає `apply_discount`.
4. Application виконує discount tool.
5. Later iteration повертає `Final Answer`.

Потім тимчасово прибери або зламай stop token:

```python
options={"temperature": 0}
```

Перевір, чи model починає генерувати власний `Observation`.

### Додатковий backend / production context task

Покращ safety:

1. Замінити regex-only parsing на stricter parser logic.
2. Validate number of args per tool before execution.
3. Замінити silent `0` defaults explicit errors.
4. Додати max scratchpad size або iteration-level token budget.
5. Додати test cases, де model emits malformed action format.

### Unknowns

- Unknown / Not confirmed from source: exact output text on every model run.
- Unknown / Not confirmed from source: whether Qwen3 1.7B always follows the ReAct format consistently.
- Unknown / Not confirmed from source: exact LangSmith trace contents for your local execution.
