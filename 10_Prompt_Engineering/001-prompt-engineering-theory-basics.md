---
type: daily-review-note
topic: Prompt Engineering Theory Basics: Prompts, Shot Prompting, CoT, ReAct, Context Engineering
area: Prompt Engineering
date: 2026-05-12
tags:
  - prompt-engineering
  - llm-basics
  - zero-shot
  - few-shot
  - chain-of-thought
  - react-prompting
  - context-engineering
  - system-prompts
  - ai-platform-engineering
status: active-review
review:
  - 2026-05-13
  - 2026-05-15
  - 2026-05-19
  - 2026-05-26
  - 2026-06-11
source_type: transcript
source_confidence: medium
---

# Daily Review Note: Prompt Engineering Theory Basics

## 1. Core idea

### Source-based explanation

Цей матеріал пояснює базову теорію prompt engineering:

- LLM можна спрощено розуміти як language model, що прогнозує наступне слово/token на основі попереднього context.
- Prompt — це input, який задає model задачу, контекст, дані та очікуваний output.
- Prompt складається з чотирьох компонентів: instruction, context, input data, output indicator.
- Zero-shot prompting — запит без прикладів.
- One-shot / few-shot prompting — запит із одним або кількома прикладами очікуваного output.
- Chain-of-thought prompting — підхід, де model спрямовується на проміжні reasoning steps для multi-step задач.
- ReAct prompting поєднує reasoning і acting: model думає, вибирає дію, отримує observation і продовжує.
- Context engineering — еволюція prompt engineering: важливо не лише написати static prompt, а динамічно зібрати правильний context.
- System prompt має бути не надто vague і не надто over-specific; потрібна “золота середина”.

### Additional backend / production context

Для backend / AI Platform engineer prompt — це не просто текст. Це runtime contract між application і model.

Prompt впливає на:

- output consistency;
- tool selection;
- hallucination risk;
- latency і token cost;
- security boundaries;
- debugging complexity;
- evaluation quality.

### Assumptions

- Нотатка базується тільки на наданому transcript Section 11.
- Зовнішні links у матеріалі не перевірялись окремо.
- Історичні/фінансові/модельні claims із transcript не розширюються.

### Unknowns

- Unknown / Not confirmed from source: точна кількість training words для GPT-3.
- Unknown / Not confirmed from source: точна кількість downloads prompt `hwchase17/react` або stars у згаданому GitHub repo на поточну дату.
- Unknown / Not confirmed from source: точні internal system prompts Claude Code, Cursor, Devin; transcript посилається на leaked prompts, але їх достовірність не підтверджена тут.

---

## 2. Why it matters

### Source-based explanation

Prompt engineering потрібен, щоб краще керувати поведінкою LLM:

- instruction задає задачу;
- context зменшує guessing;
- examples у few-shot prompting спрямовують style/format/output;
- chain-of-thought покращує multi-step reasoning tasks;
- ReAct дає pattern для agents, які можуть reasoning + act через tools/external data;
- context engineering вирішує проблему dynamic context у agents, coding assistants і long-running workflows;
- system prompts задають identity, scope, boundaries і general behavior.

### Additional backend / production context

У production LLM systems prompt design напряму впливає на reliability. Слабкий prompt може призвести до:

- inconsistent output format;
- wrong tool calls;
- hallucinated facts;
- unsafe actions;
- excessive token usage;
- prompt injection exposure;
- degraded agent performance через irrelevant/contradictory context.

---

## 3. How it works

### Source-based explanation

#### 3.1 Language model mental model

Language modeling у матеріалі пояснюється як задача прогнозування наступного word/token на основі попередньої sequence.

Спрощено:

```text
previous words/context -> probability distribution over next word -> chosen next word -> repeat
```

LLM — це language model, навчений на великому обсязі data. Коли ми даємо prompt, model генерує відповідь word/token by word/token, прогнозуючи найбільш імовірне продовження в context.

#### 3.2 Prompt components

Prompt складається з чотирьох частин:

| Component | Source-based meaning |
|---|---|
| Instruction | Що model має зробити |
| Context | Додаткова інформація для кращого розуміння задачі |
| Input data | Дані, які model має обробити |
| Output indicator | Сигнал, що model має почати відповідь або в якому форматі відповідати |

#### 3.3 Zero-shot prompting

Zero-shot prompt — це prompt без прикладів. Model покладається на preexisting knowledge і instruction.

Перевага: простий і швидкий.

Обмеження з source:

- менше control;
- accuracy може бути нижчою;
- output може не відповідати очікуваному format/style;
- model більше “guessing”.

#### 3.4 One-shot / few-shot prompting

One-shot — один приклад очікуваного output.

Few-shot — кілька прикладів очікуваного output.

Source показує приклад з image description: коли model отримує приклади типу “blue dog”, “red dog”, “green dog”, вона вчиться, що color має бути частиною output.

#### 3.5 Chain-of-thought prompting

Chain-of-thought prompting спрямовує model розбити складну задачу на intermediate reasoning steps.

Source пояснює два варіанти:

- zero-shot CoT: додати щось на кшталт “let’s think step by step”;
- few-shot CoT: дати приклад подібної задачі з reasoning steps і answer.

#### 3.6 ReAct prompting

ReAct = reasoning + acting.

Pattern:

```text
Thought -> Action -> Observation -> Thought -> Action -> Observation -> Final Answer
```

Source пояснює, що ReAct дозволяє model не лише міркувати, а й діяти через external sources/tools. Code/application бере action з model output, виконує його і повертає observation назад у prompt/context.

#### 3.7 Prompt engineering quick tips

Source дає три практичні tips:

1. Додавай context.
2. Формулюй clear, non-ambiguous task.
3. Ітеруй prompt: test output -> refine prompt -> repeat.

#### 3.8 Context engineering

Context engineering — це не просто написання static prompt. Це dynamic system, який збирає correct and relevant context з різних sources:

- developer-provided context;
- user input;
- previous interactions;
- tool calls;
- external data.

Source вказує типові problems:

- context window growth;
- higher cost;
- higher latency;
- degraded agent performance;
- context poisoning;
- context confusion;
- context clash.

#### 3.9 System prompt engineering

Source описує system prompt як важливий context engineering mechanism.

Good system prompt не має бути:

- too vague: недостатньо signal, undefined boundaries;
- too specific: hardcoded logic, rigid flowcharts, maintenance nightmare.

Кращий підхід: clear identity, scope, boundaries, reasoning framework, general principles.

---

## 4. Backend analogy

### Source-based explanation

Prompt задає model задачу й context. ReAct prompt задає protocol взаємодії: reasoning, action, observation, final answer.

### Additional backend / production context

Backend analogy:

| Prompt Engineering concept | Backend / distributed systems analogy |
|---|---|
| Prompt | API request contract to model |
| Instruction | Command / use-case intent |
| Context | Request metadata + domain state |
| Input data | Request payload |
| Output indicator | Response schema / output protocol |
| Few-shot examples | Contract examples / golden samples |
| Chain-of-thought | Decomposition strategy / execution plan |
| ReAct | Workflow loop with command execution |
| Observation | Tool/service response appended to workflow state |
| System prompt | Runtime policy / service configuration |
| Context engineering | Dynamic request enrichment layer |

Mental model:

```text
Prompt engineering = designing the model contract.
Context engineering = building the runtime system that assembles the right contract per request.
```

---

## 5. Production relevance

### Source-based explanation

The transcript highlights these production-relevant ideas:

- vague prompts lead to inconsistent behavior;
- missing context makes model guess;
- examples reduce creative freedom and guide output;
- agents can degrade when context grows;
- context poisoning can introduce hallucination into future context;
- context confusion happens when unnecessary context influences response;
- context clash happens when context parts contradict each other;
- system prompts evolve iteratively as models and agents evolve.

### Additional backend / production context

#### Reliability

Prompt must be tested like code:

- regression prompts;
- golden datasets;
- expected output format;
- failure cases;
- ambiguity tests;
- tool-call correctness tests.

#### Observability

Track:

- prompt version;
- context sources;
- final assembled prompt/messages;
- model output;
- token usage;
- latency;
- tool calls;
- parse/validation failures.

#### Security

Prompt/context can be attack surface:

- prompt injection;
- malicious instructions inside retrieved context;
- leaking hidden system prompt;
- over-exposing tool descriptions;
- user-provided context overriding policy.

#### Cost/performance

Context engineering affects:

- input tokens;
- output tokens;
- latency;
- model choice;
- cost per request;
- cacheability.

#### Maintainability

Avoid system prompts that are:

- giant flowcharts;
- duplicated instruction blocks;
- contradictory rules;
- impossible edge-case enumerations;
- unversioned text blobs.

### Version-sensitive / may require verification

The material contains claims about model training scale, public prompt downloads, stars in repositories, vendor/model behavior and external agent prompts. These are time-sensitive or source-sensitive and should be verified before being reused as factual claims outside this learning note.

---

## 6. Key terms

### Source-based explanation

| Term | Meaning |
|---|---|
| Language model | Model that predicts next word/token based on prior sequence/context |
| LLM | Large language model trained on a large amount of data |
| Prompt | Input given to AI model to produce output |
| Instruction | Task the model should perform |
| Context | Additional information that helps model understand the task |
| Input data | Data the model processes to complete the task |
| Output indicator | Signal or format showing that response is expected |
| Zero-shot prompting | Prompting without examples |
| One-shot prompting | Prompting with one example |
| Few-shot prompting | Prompting with multiple examples |
| Chain-of-thought | Prompting method that encourages intermediate reasoning steps |
| ReAct | Reasoning + Acting pattern with thought/action/observation loop |
| Observation | Result from action/tool/external source |
| Context engineering | Dynamic selection and assembly of relevant context for LLM calls |
| Context poisoning | Bad/hallucinated context enters future context and degrades system |
| Context confusion | Irrelevant context influences response |
| Context clash | Contradictory context parts conflict |
| System prompt | High-level instruction/context that defines model role, boundaries and behavior |

---

## 7. Common mistakes

### Source-based explanation

1. Writing prompts without context.
   - Model guesses missing assumptions.

2. Using vague tasks.
   - Example from source: “improve the user experience” is too broad.

3. Assuming zero-shot is always enough.
   - It gives less control and relies on model preexisting knowledge.

4. Adding too many rigid rules into system prompt.
   - Source says this treats LLM like deterministic state machine and creates maintenance problems.

5. Making system prompt too vague.
   - Model lacks actionable guidance and boundaries.

6. Ignoring iteration.
   - Prompt quality improves through testing outputs and refining prompt.

### Additional backend / production context

7. No prompt versioning.
   - Makes regressions hard to debug.

8. No evaluation dataset.
   - You cannot know whether prompt changes improved or broke behavior.

9. Mixing policy, task, examples and user data chaotically.
   - Increases contradiction and prompt injection risk.

10. Sending all available context.
   - Causes cost/latency growth and can degrade answer quality.

---

## 8. Flashcards

Q: What is a prompt in this source?
A: Input given to an AI model to guide it toward producing an output.

Q: What are the four prompt components?
A: Instruction, context, input data, and output indicator.

Q: What is zero-shot prompting?
A: Asking the model to perform a task without providing examples.

Q: What is few-shot prompting?
A: Providing a small number of examples so the model can imitate the expected pattern.

Q: What is one-shot prompting?
A: A subset of few-shot prompting with exactly one example.

Q: What is chain-of-thought prompting?
A: Prompting that guides the model to solve complex tasks through intermediate reasoning steps.

Q: What does ReAct combine?
A: Reasoning and acting: the model reasons, chooses actions, observes results, and continues.

Q: What is context engineering?
A: Dynamically assembling the correct and relevant context for an LLM call.

Q: What is context poisoning?
A: When hallucinated or bad context enters future context and degrades the system.

Q: What is the system prompt Goldilocks idea?
A: A good system prompt should be neither too vague nor too specific; it should give just enough guidance.

---

## 9. Interview Q&A

### Q1: What is prompt engineering?

**Answer:** Prompt engineering is designing the model input so the LLM has clear task instructions, enough context, relevant input data and an expected output signal.

### Q2: What are the main components of a prompt?

**Answer:** Instruction, context, input data and output indicator.

### Q3: When is zero-shot prompting useful?

**Answer:** When the task is simple, broad, or the model likely has enough prior knowledge. It is fast but gives less control.

### Q4: Why use few-shot prompting?

**Answer:** To guide the model with examples of the desired output style, structure or reasoning pattern.

### Q5: What is the difference between chain-of-thought and ReAct?

**Answer:** Chain-of-thought focuses on intermediate reasoning steps. ReAct combines reasoning with actions and observations from external tools or sources.

### Q6: Why is context engineering important for agents?

**Answer:** Agents accumulate user inputs, tool results and prior interactions. Wrong or excessive context can increase cost, latency and degrade performance.

### Q7: What are common context failure modes?

**Answer:** Context poisoning, context confusion, context clash and context window growth.

### Q8: What is a bad system prompt?

**Answer:** One that is either too vague to guide behavior or too rigid and over-specified, causing brittle behavior and maintenance issues.

### Q9: What production practices should prompt changes follow?

**Answer:** Version prompts, evaluate on test cases, track latency/cost/output quality, and monitor failures after rollout.

### Q10: Why should prompt engineering be iterative?

**Answer:** Because model output reveals where the prompt is unclear; each iteration refines task, context, specificity and expected output.

---

## 10. Self-check

Answer without looking:

1. What is the simplified mental model of an LLM from this source?
2. What are the four components of a prompt?
3. What is the main limitation of zero-shot prompting?
4. How does few-shot prompting reduce model freedom?
5. What does chain-of-thought add?
6. What does ReAct add on top of reasoning?
7. Why is context engineering more than prompt engineering?
8. What are context poisoning, confusion and clash?
9. Why can too-specific system prompts be bad?
10. Why can too-vague system prompts be bad?

Expected answers:

1. It predicts the next word/token based on context.
2. Instruction, context, input data, output indicator.
3. Less control and more reliance on model guessing/preexisting knowledge.
4. It provides examples the model can imitate.
5. Intermediate reasoning steps.
6. Actions/tools and observations from external sources.
7. Because real systems dynamically assemble context from many sources.
8. Poisoning = bad context contaminates future context; confusion = irrelevant context affects output; clash = contradictory context conflicts.
9. They hardcode brittle logic and become maintenance nightmares.
10. They provide insufficient signal and produce inconsistent behavior.

---

## 11. Mini practice task

### Source-based practice

Take this vague prompt:

```text
Improve the user experience of this e-commerce website.
```

Rewrite it using the four prompt components:

1. Instruction
2. Context
3. Input data
4. Output indicator

Then create:

- one zero-shot version;
- one one-shot version;
- one few-shot version.

Compare which one gives the most targeted output.

### Additional backend / production context task

Design a small prompt evaluation table for an AI support assistant:

| Test case | Prompt version | Expected behavior | Actual behavior | Pass/Fail | Notes |
|---|---|---|---|---|---|

Include at least:

- ambiguous user request;
- missing context;
- irrelevant context;
- contradictory context;
- prompt injection attempt;
- request requiring tool use.

Goal: treat prompt changes like production code changes.

### Unknowns

- Unknown / Not confirmed from source: exact behavior of any specific model on these prompts.
- Unknown / Not confirmed from source: exact best prompt for any production system without evaluation.
- Unknown / Not confirmed from source: whether leaked prompt repositories accurately represent current production system prompts.
