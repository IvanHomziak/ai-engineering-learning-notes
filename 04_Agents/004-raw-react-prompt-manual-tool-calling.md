---
type: daily-review-note
topic: Layer 3 Raw ReAct Prompt: Manual Tool Calling Without Function Calling
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

# Daily Review Note: Layer 3 Raw ReAct Prompt: Manual Tool Calling Without Function Calling

## 1. Core idea

### Source-based explanation

Layer 3 показує найнижчий рівень agent implementation у цьому section: agent працює **без LangChain tool abstraction** і **без function calling API**.

Замість structured `tool_calls` модель отримує великий ReAct prompt і повинна відповісти plain text у форматі:

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

### Additional backend / production context

Ментальна модель:

```text
LLM is not calling tools.
LLM is emitting a text protocol.
Application parses the protocol and executes tools.
```

Це схоже на дуже крихкий text-based RPC protocol, де model output є command string, а Python application — command executor.

### Assumptions

- Нотатка базується на transcript Section 7 і наданому файлі `3_raw_react_prompt.py`.
- Production-коментарі явно відокремлені від source-based explanation.

### Unknowns

- Unknown / Not confirmed from source: повна prompt engineering theory за ReAct prompt, бо transcript відсилає до Theory section, але її зміст тут не надано.
- Unknown / Not confirmed from source: точна історична першість LangChain ReAct agent implementation поза твердженнями в transcript.
- Unknown / Not confirmed from source: фактична кількість downloads prompt `hwchase17/react` на поточну дату; source згадує понад 7 million downloads, але це не перевірялося окремо.

---

## 2. Why it matters

### Source-based explanation

Цей layer важливий, бо показує foundation function calling:

- function calling дає structured API response;
- ReAct prompt робить схожу логіку через plain text protocol;
- tool descriptions вставляються прямо в prompt;
- tool names вставляються прямо в prompt;
- scratchpad зберігає history agent actions and observations;
- regex parsing замінює structured response parsing.

Source позиціонує ReAct prompt як фундамент agent behavior: LLM використовується як reasoning engine, який вирішує, яку дію виконати далі.

### Additional backend / production context

Для AI Platform / LLM Infrastructure engineer це важливо, бо:

1. Дає розуміння, що agentic behavior може бути реалізований без спеціального API.
2. Показує, чому function calling зʼявився як надійніший structured layer поверх prompt-only agents.
3. Пояснює failure modes agentів: format drift, hallucinated observations, parsing failure, wrong tool args, infinite loop.
4. Допомагає дебажити навіть сучасні agents, бо під structured abstractions все одно є decision loop.

---

## 3. How it works

### Source-based explanation

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
- `inspect` потрібен для отримання function metadata: signature і docstring.
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

#### Step 4 — Generate dynamic tool descriptions

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
- `getattr(tool_function, "__wrapped__", tool_function)` — бере original function, якщо вона обгорнута decorator-ом `@traceable`.
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

```python
react_prompt = f"""
STRICT RULES — you must follow these exactly:
1. NEVER guess or assume any product price. You MUST call get_product_price first to get the real price.
2. Only call apply_discount AFTER you have received a price from get_product_price. Pass the exact price returned by get_product_price — do NOT pass a made-up number.
3. NEVER calculate discounts yourself using math. Always use the apply_discount tool.
4. If the user does not specify a discount tier, ask them which tier to use — do NOT assume one.

Answer the following questions as best you can. You have access to the following tools:

{tool_descriptions}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action, as comma separated values
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{question}}
Thought:"""
```

Prompt містить:

- strict rules;
- tool descriptions;
- allowed tool names;
- expected response format;
- user question placeholder;
- initial `Thought:` marker.

Важливо: source каже, що tools тепер “live inside the prompt as plain text”. LLM не отримує structured function calling schema.

#### Step 7 — Raw Ollama call without tools

```python
@traceable(name="Ollama Chat", run_type="llm")
def ollama_chat_traced(model, messages, options):
    return ollama.chat(model=model, messages=messages, options=options)
```

Тут немає `tools=...`. Source comment прямо каже: agency comes from prompt above and regex parsing below.

#### Step 8 — Build runtime prompt and scratchpad

```python
prompt = react_prompt.format(question=question)
scratchpad = ""
```

- `prompt` — ReAct prompt з runtime user question.
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
response = ollama_chat_traced(
    model=MODEL,
    messages=[{"role": "user", "content": full_prompt}],
    options={"stop": ["\nObservation"], "temperature": 0},
)
```

`stop: ["\nObservation"]` важливий: він зупиняє model перед тим, як вона згенерує власну hallucinated observation. Реальний observation має вставити application після tool execution.

`temperature: 0` використовується для більш consistent output.

#### Step 11 — Raw LLM output

```python
output = response.message.content
```

У Layer 3 немає `AIMessage` object і немає `tool_calls`. Є тільки text.

#### Step 12 — Final answer parsing

```python
final_answer_match = re.search(r"Final Answer:\s*(.+)", output)
if final_answer_match:
    final_answer = final_answer_match.group(1).strip()
    return final_answer
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
tool_name = action_match.group(1).strip()
tool_input_raw = action_input_match.group(1).strip()

raw_args = [x.strip() for x in tool_input_raw.split(",")]
args = [x.split("=", 1)[-1].strip().strip("'\"") for x in raw_args]
```

Це перетворює comma-separated text у list args. Якщо LLM повернула `key=value`, code відкидає key і бере value.

#### Step 15 — Execute tool or return tool error observation

```python
if tool_name not in tools:
    observation = f"Error: Tool '{tool_name}' not found. Available tools: {list(tools.keys())}"
else:
    observation = str(tools[tool_name](*args))
```

Якщо action name не в registry — observation стає error message.

Якщо tool існує — виконується Python function.

#### Step 16 — Update scratchpad

```python
scratchpad += f"{output}\nObservation: {observation}\nThought:"
```

Це додає:

- model thought/action/action input;
- real observation;
- новий `Thought:` marker для наступної ітерації.

Саме scratchpad дає agent memory між loop iterations.

---

## 4. Backend analogy

### Source-based explanation

Layer 3 реалізує manual protocol:

```text
Prompt text -> LLM text output -> regex parser -> tool registry -> Python execution -> scratchpad append -> repeat
```

### Additional backend / production context

Backend mapping:

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

This is like building a mini workflow runtime where the model emits commands as text and the application interprets them.

---

## 5. Production relevance

### Source-based explanation

Source demonstrates several production-relevant mechanics:

1. Without function calling, LLM output is raw text.
2. Raw text must be parsed manually.
3. Regex parsing is fragile if model does not follow format.
4. Stop token prevents model from inventing `Observation`.
5. Scratchpad stores history of tool choices and observations.
6. Tool descriptions must be injected into prompt manually.
7. Function metadata can be generated dynamically with `inspect`.
8. Tool execution remains application responsibility.

### Additional backend / production context

#### Reliability risks

- LLM may not follow the required text format.
- Regex may extract wrong action or wrong action input.
- Comma-separated parsing fails for complex arguments.
- Scratchpad can grow and increase token usage.
- Wrong stop token can allow hallucinated observations.
- Model may emit invalid tool name.
- Tool may receive wrong argument count or invalid types.

#### Security risks

- Text protocol can be prompt-injected.
- User input may try to influence `Action` or `Observation` formatting.
- Never execute arbitrary tool names from model output.
- Keep registry allowlisted.
- Validate arguments before tool execution.
- Do not expose sensitive tool descriptions if not needed.

#### Performance risks

- Every iteration sends full prompt + scratchpad again.
- Token usage grows with every step.
- Regex retries/failures can add latency.
- Local model behavior may be inconsistent depending on model quality.

#### Observability concerns

Trace should capture:

- full prompt or sanitized prompt;
- raw model output;
- regex parsing result;
- selected tool;
- parsed args;
- observation;
- final answer;
- parse failures.

### Version-sensitive

This note is version-sensitive because:

- Ollama SDK response shape may change.
- `options={"stop": [...]}` behavior is provider/model/runtime-specific.
- LangSmith `@traceable` behavior may vary by package version.
- Model adherence to ReAct format depends on model capability and prompt.

### Potential issue

1. Transcript duplicates lecture title/content for `36. Generating Dynamic Tool Descriptions in Python`.
2. Source code comment says `# --- Tools (LangChain @tool decorator) ---`, but code uses `@traceable`, not LangChain `@tool`; likely leftover comment.
3. Raw argument parser uses comma split, which is fragile for complex inputs.
4. `get_product_price` still returns `0` for unknown product; toy example, risky in production.
5. `apply_discount` returns no-error result for unknown discount tier by using `0` discount; toy example, risky in production.

---

## 6. Key terms

### Source-based explanation

| Term | Meaning |
|---|---|
| ReAct prompt | Prompt format that drives Thought / Action / Action Input / Observation / Final Answer behavior |
| Thought | Model reasoning step represented as text in prompt output |
| Action | Tool/function name the model says should run |
| Action Input | Input string for selected action |
| Observation | Real result returned by tool execution and appended by application |
| Scratchpad | Accumulated history of thoughts, actions, inputs and observations |
| Regex parsing | Extracting `Action`, `Action Input`, or `Final Answer` from raw text output |
| Stop token | Generation boundary that stops model before hallucinating observation |
| Tool description | Text generated from function signature and docstring, injected into prompt |
| `inspect.signature` | Python function used to read function signature |
| `inspect.getdoc` | Python function used to read docstring |
| `__wrapped__` | Attribute used to access original function behind decorator wrapper |
| Manual tool calling | Application parses model text and invokes Python function itself |

---

## 7. Common mistakes

### Source-based explanation

1. Assuming function calling is required for agents.
   - Source shows ReAct prompt can implement agent behavior without function calling.

2. Assuming model knows Python functions automatically.
   - Source says tool descriptions must be propagated into prompt because LLM inherently does not know application functions.

3. Letting model generate `Observation`.
   - Source uses stop token so application injects real tool result.

4. Forgetting scratchpad.
   - Without scratchpad, next iteration does not know previous actions and observations.

5. Treating regex parsing as reliable.
   - Source code comment explicitly says it is fragile if LLM does not follow format.

6. Confusing `tool_descriptions` with `tool_names`.
   - `tool_descriptions` includes signature/docstring; `tool_names` is only allowed action names.

### Additional backend / production context

7. Using raw ReAct for high-risk production actions.
   - Prompt-only tool selection is weaker than structured, validated protocols.

8. No schema validation for action inputs.
   - Comma splitting is not enough for real domain inputs.

9. Not bounding scratchpad size.
   - Long-running loops can exceed context/cost limits.

10. Logging full prompts with secrets.
   - If tool descriptions or user inputs contain sensitive data, traces must be sanitized.

---

## 8. Flashcards

| Question | Answer |
|---|---|
| What is Layer 3 about? | Implementing an agent without function calling by using ReAct prompt, regex parsing and scratchpad. |
| What replaces structured `tool_calls`? | Raw text output containing `Action` and `Action Input`. |
| Why is `re` imported? | To parse `Final Answer`, `Action`, and `Action Input` from raw LLM text. |
| Why is `inspect` imported? | To extract function signatures and docstrings for dynamic tool descriptions. |
| What is `tool_descriptions`? | A string containing tool names, signatures and docstrings injected into the ReAct prompt. |
| What is `tool_names`? | Comma-separated list of allowed action names injected into the prompt. |
| What is scratchpad? | Growing text history of model output, real observations and next `Thought:` marker. |
| Why use stop token `\nObservation`? | To prevent the model from hallucinating the observation before the application inserts the real tool result. |
| What happens if `Final Answer` is found? | The loop returns the parsed final answer. |
| What happens if `Action` is found? | The application parses the tool name/input and executes the matching tool. |
| Why is raw ReAct fragile? | It depends on the model following exact text format and on regex parsing working correctly. |
| What is the main lesson of Layer 3? | Function calling is a structured version of a behavior that can be approximated with prompt protocol + parser + tool executor. |

---

## 9. Interview Q&A

### Q1: What is the ReAct prompt?

**Answer:** It is a prompt format that instructs the model to reason and act through repeated `Thought`, `Action`, `Action Input`, and `Observation` steps until it can produce `Final Answer`.

### Q2: How does Layer 3 differ from Layer 2?

**Answer:** Layer 2 uses structured function calling from Ollama. Layer 3 removes function calling entirely. The model outputs plain text, and the application parses tool intent with regex.

### Q3: Why does the application need `inspect`?

**Answer:** It uses `inspect.signature` and `inspect.getdoc` to build tool descriptions from Python functions and inject them into the prompt.

### Q4: What is scratchpad used for?

**Answer:** Scratchpad stores prior model outputs and real tool observations so the next iteration has execution history and can decide the next step.

### Q5: Why is the stop token important?

**Answer:** It stops the LLM before it generates `Observation`, because observation should be the real result of application tool execution, not model hallucination.

### Q6: Why is regex parsing risky?

**Answer:** If the model does not follow the exact expected format, regex may fail or extract wrong data, causing wrong tool execution or loop failure.

### Q7: Does the LLM know the tools automatically?

**Answer:** No. The code injects tool names, signatures and docstrings into the prompt so the model can reason about available tools.

### Q8: What is the role of `tools` dictionary?

**Answer:** It maps parsed action names to executable Python functions and acts as an allowlist for tool execution.

### Q9: How does Layer 3 approximate function calling?

**Answer:** The prompt asks the model to output a tool name and arguments as text; regex parses them; application code executes the tool and appends observation.

### Q10: Would you use this raw ReAct style directly in production?

**Answer:** Only with caution and usually not for high-risk actions. It is useful for learning and controlled cases, but production systems need stronger validation, structured outputs, guardrails, tracing, timeouts and policy checks.

---

## 10. Self-check

Answer without looking:

1. What two Python modules are added in Layer 3 and why?
2. Why is function calling removed?
3. What is injected into `{tool_descriptions}`?
4. What is injected into `{tool_names}`?
5. Why does `get_tool_descriptions` use `__wrapped__`?
6. What does `stop: ["\nObservation"]` prevent?
7. What does regex search for first: final answer or action?
8. How are action inputs converted into function args?
9. What happens when parsed tool name is not in `tools`?
10. Why does scratchpad end with `Thought:`?

Expected answers:

1. `re` for regex parsing and `inspect` for reading function metadata.
2. To show how agent/tool calling works from raw prompt engineering without structured tool API.
3. Tool name + function signature + docstring for each tool.
4. Allowed action names: `get_product_price, apply_discount`.
5. To access the original function behind `@traceable` wrapper.
6. It prevents the model from hallucinating the tool result.
7. It first checks for `Final Answer`.
8. By splitting comma-separated text and stripping optional `key=` prefixes and quotes.
9. Observation becomes an error message listing available tools.
10. To cue the model to continue reasoning in the next iteration.

---

## 11. Mini practice task

### Source-based practice

Run Layer 3:

```bash
uv run python 3_raw_react_prompt.py
```

Verify the expected behavior:

1. First LLM output contains `Action: get_product_price` and `Action Input: laptop`.
2. Application executes `get_product_price` and appends real `Observation`.
3. Second iteration selects `apply_discount`.
4. Application executes discount tool.
5. Later iteration returns `Final Answer`.

Then temporarily remove or break the stop token:

```python
options={"temperature": 0}
```

Observe whether the model starts generating its own `Observation`.

### Additional backend / production context task

Improve safety:

1. Replace regex-only parsing with stricter parser logic.
2. Validate number of args per tool before execution.
3. Replace silent `0` defaults with explicit errors.
4. Add max scratchpad size or iteration-level token budget.
5. Add test cases where model emits malformed action format.

### Unknowns

- Unknown / Not confirmed from source: exact output text on every model run.
- Unknown / Not confirmed from source: whether Qwen3 1.7B always follows the ReAct format consistently.
- Unknown / Not confirmed from source: exact LangSmith trace contents for your local execution.
