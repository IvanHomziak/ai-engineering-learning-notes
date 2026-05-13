---
type: daily-review-note
topic: Function Calling / Tool Calling для LLM-агентів
area: Agents
date: 2026-05-13
tags:
  - agents
  - function-calling
  - tool-calling
  - structured-output
  - react-prompt
  - llm-tools
  - ai-platform-engineering
status: active-review
review:
  - 2026-05-14
  - 2026-05-16
  - 2026-05-20
  - 2026-05-27
  - 2026-06-12
source_type: transcript
source_confidence: medium
---

# Щоденна нотатка для повторення: Function Calling / Tool Calling для LLM-агентів

## 1. Основна ідея

### Пояснення на основі джерела

Function calling, або tool calling у матеріалі, — це здатність LLM повертати **структурований виклик функції**, а не тільки звичайний текст.

Замість ReAct prompt, де модель пише текст у такому стилі:

```text
Thought: ...
Action: get_weather
Action Input: Paris
Observation: ...
```

function calling дозволяє моделі повернути структурований обʼєкт із:

```text
назвою функції
аргументами функції
```

Після цього application code парсить структуровану відповідь і виконує відповідну function/tool у коді застосунку.

У джерелі function calling подано як production-орієнтовану еволюцію ReAct prompt, бо JSON-подібний structured output легше парсити, ніж free-form text через regular expressions.

### Додатковий backend / production context

Function calling найкраще розуміти як механізм вибору команди за допомогою моделі:

```text
User request -> LLM вибирає tool + args -> application валідовує -> application виконує tool -> tool result повертається в LLM/application
```

LLM **не виконує** функцію. Вона лише пропонує function call. Backend виконує реальну дію.

### Припущення

- Нотатка базується тільки на наданому transcript з Section 8: Function Calling.
- Зовнішня документація не перевірялась для цієї нотатки.
- Claims про vendors/models трактуються як version-sensitive.

### Невідоме / не підтверджено джерелом

- Unknown / Not confirmed from source: точний response format для кожного provider.
- Unknown / Not confirmed from source: точний schema syntax для OpenAI, Anthropic, Google або інших vendors.
- Unknown / Not confirmed from source: чи кожна актуальна модель конкретного vendor підтримує function calling.

---

## 2. Чому це важливо

### Пояснення на основі джерела

Raw ReAct prompting потужний, але fragile. Джерело каже, що достатньо, щоб LLM згенерувала один неправильний token, і parser може зламатися, особливо якщо application покладається на regex parsing.

Function calling покращує це тим, що змушує модель повертати structured function call у спеціальній частині response. Це полегшує application або framework доступ до полів напряму, без parsing natural language.

Джерело називає дві головні можливості:

1. Підключення LLM до external tools.
2. Отримання structured output від LLM.

### Додатковий backend / production context

Для AI agents function calling важливий, бо перетворює ambiguous text output на більш machine-readable contract.

Production impact:

- менше parsing failures, ніж у raw ReAct text;
- чистіша інтеграція з application services;
- простіша validation function name і arguments;
- краща сумісність із typed downstream objects;
- кращий фундамент для tool-using agents.

---

## 3. Як це працює

### Пояснення на основі джерела

Процес, описаний у джерелі:

1. Developer надає model function definitions.
2. Function definitions містять names, parameters і descriptions.
3. Model отримує user request.
4. Model вирішує, чи потрібно викликати function.
5. Якщо потрібно, model повертає structured object із function name і arguments.
6. Application парсить object.
7. Application виконує реальну function.
8. Application може повернути function result назад у LLM і продовжити flow.

Приклад із джерела:

```text
User: What's the weather in Paris?
Available function: get_current_weather
Model output: function call with location=Paris and unit=Fahrenheit or Celsius
Application: executes get_current_weather(...) and sends result back
```

Джерело каже, що це надійніше за ReAct prompt parsing, бо response структурований, а не free-form text.

### Додатковий backend / production context

Production implementation зазвичай має додати:

- allowlist callable tools;
- argument validation;
- schema validation;
- authorization checks;
- timeouts і retries;
- idempotency для side-effecting tools;
- audit logs;
- tracing model decision і tool execution;
- fallback behavior, якщо model повертає invalid tool args.

Function calling дає чистіший protocol, але не знімає відповідальність із backend.

---

## 4. Backend аналогія

### Пояснення на основі джерела

Function calling описаний як ситуація, де model повертає structured function name і arguments, які application code може виконати.

### Додатковий backend / production context

| Function calling concept | Backend analogy |
|---|---|
| Function definition | API/command schema |
| Function name | Command name / handler key |
| Function arguments | Request DTO / command payload |
| Tool choice by LLM | Routing decision |
| Application execution | Service method / adapter invocation |
| Tool result | Service response / event result |
| Feeding result back to LLM | Workflow state update |
| Structured JSON output | Machine-readable integration contract |

Mental model:

```text
Function calling = LLM створює typed command request; backend валідовує і виконує його.
```

---

## 5. Production relevance

### Пояснення на основі джерела

Джерело стверджує, що function calling більш production-grade, ніж raw ReAct prompting, тому що:

- output структурований;
- він уникає regex parsing;
- його легше парсити;
- він зменшує random formatting errors;
- він дає надійніше tool usage;
- він може зменшити token usage, бо model не мусить виводити verbose reasoning steps.

Джерело також називає один drawback: **opaque reasoning process**. Model може повернути тільки final function name і arguments, не пояснюючи, чому вона їх вибрала.

### Додатковий backend / production context

#### Reliability

Function calling зменшує format errors, але не гарантує correctness. Model все ще може:

- вибрати wrong function;
- передати wrong arguments;
- пропустити required fields;
- hallucinate values;
- викликати tools у wrong order;
- не викликати потрібний tool.

#### Security

Tool execution — це trust boundary:

- ніколи не виконуй arbitrary function names із model output;
- валідовуй усі arguments;
- обмежуй tools за user permissions;
- не expose sensitive internal functions;
- додавай human approval для high-risk actions.

#### Observability

Окремо trace:

- model input;
- available tool definitions;
- selected function name;
- arguments;
- validation result;
- tool latency;
- tool result;
- final answer.

#### Cost/performance

Джерело стверджує, що function calling може бути легшим за tokens, ніж ReAct, бо не потребує verbose reasoning text. Але production cost залежить від:

- кількості loop iterations;
- розміру tool schemas;
- розміру context;
- provider/model;
- tool latency.

### Version-sensitive / may require verification

Матеріал містить claims, які залежать від version/provider:

- function calling was introduced by OpenAI in 2023;
- big vendors' state-of-the-art models generally support function calling;
- vendors have “perfected” function calling;
- function calling is the de facto standard;
- function calling is more deterministic/reliable than ReAct prompting.

Ці твердження можуть бути directionally useful, але їх треба перевіряти по current provider docs і target model behavior перед production use.

---

## 6. Key terms

### Пояснення на основі джерела

| Term | Meaning |
|---|---|
| Function calling | Здатність model повертати structured function call з name і arguments |
| Tool calling | Альтернативний термін, який у джерелі використовується взаємозамінно з function calling |
| Function definition | Metadata, яку дають model: function name, parameters, descriptions |
| Structured output | Machine-readable output, наприклад JSON-like fields, а не plain text |
| ReAct prompt | Prompt pattern із Thought/Action/Observation text loop |
| Regex parsing | Parsing free-form text через regular expressions; у джерелі подано як fragile |
| External tool | Function/API поза LLM, який application code може виконати |
| Opaque reasoning | Model повертає function call без intermediate rationale |
| Schema | Опис очікуваних function arguments і structure |

---

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що ReAct prompt parsing є production reliable.
   - Джерело каже, що один wrong token може зламати regex parsing.

2. Думати, що function calling означає, що LLM виконує function.
   - Джерело каже, що application виконує реальну function після parsing model output.

3. Сприймати function calling тільки як agent tooling.
   - Джерело також каже, що його можна використовувати для structured output extraction.

4. Очікувати full reasoning.
   - Джерело каже, що reasoning часто opaque; developer бачить function name і arguments.

### Додатковий backend / production context

5. Не валідовувати function arguments.
   - Structured не означає safe або correct.

6. Expose too many tools.
   - Більше tools може збільшити wrong-tool selection risk і security exposure.

7. Не мати tool authorization.
   - Різні users не повинні мати однаковий доступ до actions за замовчуванням.

8. Не мати fallback для invalid tool calls.
   - Production systems потребують retry, clarification, safe failure або human handoff.

9. Не мати evaluation для tool-call accuracy.
   - Потрібні tests для function selection і argument correctness.

---

## 8. Flashcards

Q: Що таке function calling?
A: Здатність LLM повертати structured function call із function name і arguments замість тільки plain text.

Q: Що таке tool calling?
A: Інший термін для function calling, який у джерелі використовується взаємозамінно.

Q: Чому function calling надійніший за raw ReAct prompting?
A: Він повертає structured data, які легше парсити, ніж free-form text через regex.

Q: Чи виконує LLM функцію?
A: Ні. LLM повертає function call; application code виконує реальну function.

Q: Що developer надає model?
A: Function definitions із names, parameters і descriptions.

Q: Які дві головні можливості function calling названі в джерелі?
A: Підключення LLM до external tools і отримання structured output.

Q: Який головний drawback згадано в джерелі?
A: Opaque reasoning: model може не пояснювати, чому вибрала конкретну function і arguments.

Q: Чому regex parsing fragile?
A: Маленька formatting/token помилка може зламати parsing і agent execution.

Q: Що production code має зробити перед tool execution?
A: Validate function name, arguments, permissions і safety constraints.

Q: Яка backend mental model?
A: Function calling — це typed command request, згенерований LLM і виконаний backend.

---

## 9. Interview Q&A

### Q1: Що таке function calling в LLM?

**Answer:** Function calling — це здатність model повертати structured function call із function name і arguments, щоб application code міг виконати відповідний external tool.

### Q2: Чим function calling відрізняється від ReAct prompting?

**Answer:** ReAct prompting генерує plain text типу `Action` і `Action Input`, який часто парситься regex. Function calling генерує structured fields, які легше і безпечніше парсити.

### Q3: Чи function calling автоматично виконує backend code?

**Answer:** Ні. Model тільки вибирає function і arguments. Application валідовує і виконує actual code.

### Q4: Яку інформацію треба надати model?

**Answer:** Function definitions: names, parameters, argument descriptions і tool descriptions.

### Q5: Які головні переваги?

**Answer:** Structured parsing, менше formatting errors, надійніше tool usage, простіша integration і potential token savings порівняно з verbose ReAct traces.

### Q6: Який головний trade-off?

**Answer:** Opaque reasoning. Model може не показувати, чому вибрала конкретну function або arguments, що ускладнює debugging/auditing.

### Q7: Які failure modes залишаються?

**Answer:** Wrong tool selection, invalid arguments, hallucinated values, missing fields, unauthorized actions, tool timeout і bad tool result handling.

### Q8: Як production systems мають обробляти function calls?

**Answer:** Через tool allowlists, schema validation, authorization, retries/timeouts, tracing, audit logs і evaluation datasets для tool-call accuracy.

---

## 10. Self-check

Answer without looking:

1. Яку проблему function calling вирішує порівняно з raw ReAct prompt parsing?
2. Що LLM повертає у function calling?
3. Хто виконує actual function?
4. Які дві головні capabilities названі в джерелі?
5. Чому function calling може використовувати менше tokens, ніж ReAct?
6. Що означає opaque reasoning?
7. Що треба validate перед tool execution?
8. Які claims є version-sensitive?

Expected answers:

1. Він уникає fragile free-text/regex parsing завдяки structured function call data.
2. Function name і arguments у structured response area.
3. Application/backend code.
4. External tool integration і structured output.
5. Він не мусить emit verbose reasoning/Thought traces.
6. Model дає function name/args, але не intermediate rationale.
7. Tool name, arguments, permissions, safety constraints і schema conformity.
8. Claims про vendor support, reliability, de facto standards і exact history of function calling.

---

## 11. Міні-практика

### Практика на основі джерела

Напиши коротку comparison table:

| Aspect | ReAct prompt | Function calling |
|---|---|---|
| Output format | Plain text | Structured function call |
| Parsing | Regex/text parsing | Field access / JSON-like parsing |
| Reliability | More fragile | More reliable according to source |
| Reasoning visibility | More visible | More opaque |
| Tool execution | Application executes | Application executes |

### Додатковий backend / production context task

Спроєктуй validation flow перед виконанням tool, вибраного model:

```text
model tool call
-> check tool name is allowlisted
-> validate arguments against schema
-> check user authorization
-> apply timeout/retry policy
-> execute tool
-> log trace/audit event
-> return observation/result
```

Потім застосуй його до прикладу:

```text
get_current_weather(location="Paris", unit="Celsius")
```

Опиши, що може зламатися на кожному step.

### Unknowns

- Unknown / Not confirmed from source: exact provider-specific response fields.
- Unknown / Not confirmed from source: exact JSON schema format for each vendor.
- Unknown / Not confirmed from source: exact current reliability of function calling for any specific model.
