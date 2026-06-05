---
type: daily-review-note
topic: Deep Agents: planning, subagents, context isolation and filesystem context management
area: Agents
date: 2026-06-05
tags:
  - deep-agents
  - agents
  - subagents
  - planning
  - context-engineering
  - filesystem
  - langchain
  - claude-code
  - ai-platform-engineering
status: active-review
review:
  - 2026-06-06
  - 2026-06-08
  - 2026-06-12
  - 2026-06-19
  - 2026-07-05
source_type: mixed
source_confidence: high
verification_status: partially-verified
official_sources_checked:
  - LangChain Deep Agents overview
  - LangChain Deep Agents context engineering docs
  - LangChain Deep Agents blog
  - Anthropic Claude Code subagents docs
  - Anthropic Claude Code settings docs
---

# Daily Review Note: Deep Agents

## 1. Основна ідея

### Пояснення на основі джерела

Deep agents у наданому матеріалі описані як agents, здатні працювати з long-horizon tasks: складними, багатоетапними задачами, які потребують багато iterations, пошуку, обробки проміжних результатів, context management і можливого delegation.

Source протиставляє shallow agents і deep agents:

- shallow agent зазвичай працює як ReAct/tool-calling loop і підходить для коротких задач із малою кількістю iterations;
- deep agent має додаткові механізми для довгих задач: planning tool, subagents, filesystem і великий system prompt.

У матеріалі прикладами deep agents названо coding agents і research agents: Claude Code, Cursor CLI, LangChain Deep Agents, deep research style agents.

### Перевірено проти офіційних джерел

Офіційна LangChain документація описує Deep Agents як agent harness для complex tasks із built-in capabilities для task planning, file systems for context management, subagent-spawning і long-term memory. LangChain blog також формулює чотири ключові характеристики deep agents: detailed system prompt, planning tool, subagents, file system.

### Додатковий backend / production context

Deep agent — це не просто “розумніший prompt”. Це application-layer architecture поверх LLM:

```text
LLM + tools + planning + delegated workers + context storage + context compression + governance
```

Для backend / AI Platform Engineering важливо думати про deep agents як про distributed workflow runtime, де LLM є decision engine, але reliability залежить від state management, permissions, observability, retries, context hygiene і tool boundaries.

---

## 2. Чому це важливо

### Пояснення на основі джерела

ReAct-style agent може деградувати на довгих задачах через context bloat. Кожен tool call, observation і проміжний результат додаються до context window. Чим довша робота, тим більший ризик:

- context pollution;
- context contradiction;
- context confusion;
- вищої latency;
- більшої token cost;
- гіршої якості відповідей.

Deep agents намагаються вирішити це через explicit planning, isolated subagents і filesystem-backed context management.

### Перевірено проти офіційних джерел

LangChain docs підтверджують, що Deep Agents мають built-in mechanisms для managing context across long-running sessions. Документація описує context compression, offloading large tool inputs/results to filesystem, summarization, context isolation with subagents і long-term memory.

### Додатковий backend / production context

Для production це важливо тому, що long-running agent без context discipline поводиться як сервіс без backpressure, storage strategy і observability. Він може працювати, але з часом стане дорогим, повільним і нестабільним.

---

## 3. Як це працює

### Пояснення на основі джерела

#### 3.1 Shallow agent

Shallow agent у матеріалі — це спрощена назва для ReAct/tool-calling loop:

```text
LLM decides
-> tool call
-> tool execution
-> observation
-> next LLM decision
-> repeat until answer
```

Такий agent корисний для задач із невеликою кількістю steps. Але для deep research або coding tasks він може накопичувати забагато context.

#### 3.2 Deep agent

Deep agent має ті самі базові ідеї tool loop, але додає механізми для довшої роботи:

1. **Planning tool / To-do list** — agent явно веде список задач, позначає status і адаптує plan.
2. **Subagents** — agent делегує focused tasks спеціалізованим workers.
3. **Context isolation** — subagent працює у власному context window і повертає compact result.
4. **Filesystem** — agent зберігає проміжні результати, notes, artifacts або large outputs поза active context.
5. **Detailed system prompt** — agent отримує правила поведінки, tool usage і workflow guidance.

#### 3.3 Planning tool

Source підкреслює, що deep agents використовують explicit planning, а не тільки implicit chain-of-thought. Planning часто виглядає як динамічний to-do list:

```text
pending -> in_progress -> completed
```

Agent може оновлювати plan між execution steps. Це допомагає не втрачати direction на long-horizon tasks.

#### 3.4 Subagents

Subagents — це спеціалізовані agents для focused tasks. Вони можуть мати власний system prompt, description, tool set і permissions.

Головна цінність subagents: вони ізолюють context. Main agent не отримує всі проміжні search results, logs, file contents або tool outputs. Він отримує condensed final response.

#### 3.5 Context flow із subagents

Source описує такий flow:

```text
main agent thread
-> main agent creates delegation prompt
-> subagent starts with fresh context
-> subagent runs its own tool loop
-> subagent returns condensed response
-> main agent continues with cleaner context
```

Це зменшує context bloat у main conversation.

#### 3.6 File system

Source описує file system як ключовий механізм context engineering. Agent може search/read/write/edit files і використовувати files як persistent working memory.

У матеріалі згадані tools на кшталт `read`, `write`, `edit`, `glob`, `grep`, а для LangChain Deep Agents — `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep`.

Функція filesystem у deep agent:

- записувати context у persistent storage;
- зберігати проміжні результати поза active context window;
- вибірково retrieving relevant context через search/read tools;
- зменшувати over-retrieval і context pollution.

---

## 4. Перевірено проти офіційних джерел

| Твердження | Статус | Джерело перевірки | Рішення |
|---|---|---|---|
| Deep Agents мають capabilities для planning, file systems, subagents і memory | confirmed | LangChain Deep Agents overview | використано |
| Простий loop із tool calling може бути shallow для довгих задач | confirmed | LangChain Deep Agents blog | використано |
| Чотири характеристики deep agents: detailed system prompt, planning tool, subagents, file system | confirmed | LangChain Deep Agents blog | використано |
| LangChain Deep Agents мають built-in `write_todos` | confirmed | LangChain Deep Agents overview | використано |
| LangChain Deep Agents використовують built-in filesystem tools `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep` | confirmed | LangChain context engineering docs | використано |
| Subagents працюють у власному isolated context і повертають summary/result | confirmed | LangChain context engineering docs; Anthropic Claude Code subagents docs | використано |
| Claude Code custom subagents мають custom system prompt, specific tool access і independent permissions | confirmed | Anthropic Claude Code subagents docs | використано |
| Subagents завжди можуть створювати nested subagents | corrected | Anthropic Claude Code docs says subagents cannot spawn other subagents | виправлено: не узагальнювати nested delegation |
| Claude Code є “leading coding agent” | unknown | офіційне джерело не підтверджує market ranking | виключено як факт |
| Deep agents можуть працювати minutes/hours/days | partially confirmed | концептуально узгоджується з long-running agents, але конкретні duration claims не підтверджені для всіх products | використано обережно як source claim, не як universal fact |

Висновок: нотатка є **partially verified**. Ключові architectural claims підтверджені офіційними LangChain і Anthropic docs, але claims про market leadership, vendor ranking і конкретні product capabilities не включені як факти.

---

## 5. Backend-аналогія

### Пояснення на основі джерела

Deep agent схожий не на один method call, а на довгий workflow, який має план, worker delegation, shared storage і context management.

### Додатковий backend / production context

| Deep agent concept | Backend / distributed systems analogy |
|---|---|
| Main agent | Workflow orchestrator / coordinator |
| Planning tool | Task tracker / execution plan / workflow state |
| To-do list | Durable checklist / state machine progress |
| Subagent | Worker service / specialized executor |
| Subagent context isolation | Separate worker memory / isolated execution context |
| Filesystem | Shared workspace / artifact store / temporary durable state |
| `glob` / `grep` | Search/indexing over workspace artifacts |
| Context compression | Log compaction / snapshotting / summarization |
| Detailed system prompt | Policy + runbook + operating contract |
| Human-in-the-loop | Manual approval gate |

Mental model:

```text
Deep agent = LLM-driven workflow orchestrator with planning, delegated workers, artifact storage and context control.
```

---

## 6. Production relevance / значення для production

### Пояснення на основі джерела

Deep agents важливі для задач, які не вкладаються в один prompt або кілька simple tool calls: coding, research, repository analysis, debugging, large-context investigation, multi-step implementation.

Source вказує, що проблема deep tasks зводиться до context engineering: agent має мати right context, але не повинен забивати context window шумом.

### Додатковий backend / production context

Production risks:

- **Context bloat**: agent накопичує надто багато intermediate outputs.
- **Context pollution**: нерелевантні logs/search results впливають на decision quality.
- **Context contradiction**: різні проміжні findings конфліктують.
- **Runaway cost**: довгі runs генерують багато token usage.
- **Latency**: long-running multi-agent execution може бути повільним.
- **Permission risk**: filesystem/write/edit/shell tools можуть змінити критичні файли.
- **Debuggability**: без tracing важко зрозуміти, який subagent або tool зіпсував result.
- **State leakage**: shared filesystem або memory можуть переносити stale context у наступні runs.

Production controls:

- обмеження tool permissions;
- separate sandbox або worktree для code changes;
- structured task plan із visible progress;
- logs/traces для main agent і subagents;
- cost/token budgets;
- human approval для destructive operations;
- clear artifact structure у filesystem;
- tests і verification steps перед final answer.

---

## 7. Ключові терміни

| Термін | Значення |
|---|---|
| Deep agent | Agent для complex, multi-step або long-horizon tasks |
| Shallow agent | Простий ReAct/tool-calling agent, придатний для коротших задач |
| Long-horizon task | Задача з багатьма steps, iterations і проміжними artifacts |
| Planning tool | Tool для явного task decomposition і tracking progress |
| To-do list | Динамічний план роботи agent |
| Subagent | Спеціалізований worker agent для focused task |
| Context isolation | Виконання subtask в окремому context window |
| Context bloat | Надмірне накопичення tokens у context window |
| Context rot | Деградація якості через noise, contradictions або irrelevant context |
| Filesystem | Workspace для зберігання проміжних files/artifacts/context |
| Offloading | Перенесення великих inputs/results із active context у storage |
| Summarization | Стиснення старої conversation history у compact summary |

---

## 8. Типові помилки

### Пояснення на основі джерела

1. Думати, що будь-який ReAct agent автоматично є deep agent.
   - Source пояснює, що простий loop із tool calling може бути shallow для довгих задач.

2. Покладатися тільки на implicit reasoning без explicit plan.
   - Deep agents використовують planning tool / to-do list.

3. Тримати всі search results, logs і file contents у main context.
   - Subagents і filesystem потрібні саме для context isolation і context management.

4. Делегувати subagent нечітке завдання.
   - Subagent бачить тільки prompt/context, який йому передав main agent.

5. Давати subagent надто широкий tool access.
   - Claude Code docs показують, що subagents можуть мати specific tool access і permissions.

### Додатковий backend / production context

6. Не мати cost/token budget для long-running run.
7. Не ізолювати filesystem/write operations.
8. Не логувати tool calls і subagent outputs.
9. Не мати verification stage після code changes.
10. Використовувати subagents для задач, де потрібна часта інтерактивна взаємодія з user.

---

## 9. Flashcards / картки для повторення

Q: Чим deep agent відрізняється від shallow ReAct agent?
A: Deep agent має механізми для long-horizon tasks: planning, subagents, context isolation, filesystem і detailed system prompt. Shallow agent здебільшого виконує простий tool-calling loop.

Q: Навіщо deep agent потрібен planning tool?
A: Щоб явно розбити complex task на steps, tracking progress і адаптувати план під час execution.

Q: Яка головна користь subagents?
A: Вони виконують focused work в isolated context і повертають main agent компактний результат замість усіх проміжних outputs.

Q: Чому context bloat небезпечний?
A: Він збільшує cost і latency, а також може спричинити context pollution, contradiction і degradation якості рішень.

Q: Для чого deep agents використовують filesystem?
A: Щоб зберігати large outputs, notes, artifacts і intermediate results поза active context window та вибірково читати потрібне.

Q: Що таке context isolation?
A: Це виконання subtask в окремому context window, щоб не забруднювати main conversation.

Q: Який corrected claim важливий щодо Claude Code subagents?
A: Не можна узагальнювати, що subagents можуть spawn nested subagents; Anthropic docs зазначають, що subagents cannot spawn other subagents.

Q: Коли subagent може бути поганим вибором?
A: Коли задача потребує frequent back-and-forth, shared context або quick targeted change.

Q: Який production ризик має filesystem у deep agents?
A: Надто широкі read/write permissions можуть призвести до витоку secrets або небезпечних file modifications.

Q: Що означає offloading у Deep Agents?
A: Великі inputs або tool results переносяться у filesystem/backend, а в active context залишається reference або preview.

---

## 10. Interview Q&A / питання для співбесіди

### Q1: Що таке deep agent?

**Відповідь:** Це agent для complex, multi-step або long-horizon tasks, який використовує planning, subagents, context management і filesystem/artifact storage.

### Q2: Чому простий ReAct agent може бути insufficient для deep tasks?

**Відповідь:** Через context bloat: кожен tool result додається в context, що збільшує cost, latency і ризик context pollution.

### Q3: Які чотири характеристики deep agents підтверджує LangChain blog?

**Відповідь:** Detailed system prompt, planning tool, subagents і file system.

### Q4: Як subagents допомагають із context management?

**Відповідь:** Вони виконують роботу у власному context window і повертають main agent тільки final report або summary.

### Q5: Чим filesystem корисний для deep agents?

**Відповідь:** Він дозволяє зберігати large outputs, artifacts і working notes поза active context, а потім retrieve потрібні fragments.

### Q6: Який trade-off subagents?

**Відповідь:** Вони ізолюють context, але додають orchestration overhead, latency і ризик погано сформульованого delegation prompt.

### Q7: Який security ризик має deep agent із filesystem tools?

**Відповідь:** Agent може прочитати sensitive files або змінити критичні files, якщо permissions не обмежені.

### Q8: Чому planning tool не є просто UX decoration?

**Відповідь:** Він стабілізує long-running execution, дає agent явний task state і допомагає уникати втрати direction.

### Q9: Що треба логувати в production deep agent?

**Відповідь:** User request, plan updates, tool calls, subagent invocations, filesystem writes/reads, cost, latency, errors і final verification steps.

### Q10: Коли краще не використовувати subagent?

**Відповідь:** Коли задача коротка, потребує частого user interaction або сильно залежить від повного context main conversation.

---

## 11. Самоперевірка

1. Чому ReAct/tool-calling loop може стати shallow architecture?
   - Через context bloat і відсутність механізмів для long-horizon planning/context isolation.

2. Які чотири характеристики deep agents називає LangChain blog?
   - Detailed system prompt, planning tool, subagents, file system.

3. Як subagent захищає main context?
   - Він працює у власному context window і повертає compact result.

4. Що бачить subagent на старті?
   - Не всю main conversation, а delegation prompt і свій configured context; деталі залежать від implementation.

5. Чому filesystem важливий для context engineering?
   - Він дозволяє записувати context у storage і вибірково retrieve потрібні fragments.

6. Що таке under-retrieval?
   - Agent не знаходить усю relevant information для task.

7. Що таке over-retrieval?
   - Agent тягне в context надто багато noise.

8. Який production control потрібен для write/edit tools?
   - Permissions, sandboxing/worktree isolation і human approval для risky operations.

9. Що означає partially verified у цій нотатці?
   - Ключові architecture claims перевірені, але vendor ranking і деякі product-specific claims не включені як факти.

10. Який corrected claim треба запамʼятати?
   - Не узагальнювати nested subagents: Claude Code docs says subagents cannot spawn other subagents.

---

## 12. Міні-практичне завдання

Спроєктуй minimal deep agent для аналізу production incident у Java/Spring Boot microservice.

Опиши коротко:

1. Який planning tool / to-do list потрібен?
2. Які subagents ти створиш?
   - log-analysis subagent;
   - code-inspection subagent;
   - database-impact subagent;
   - test-reproduction subagent.
3. Які tools має отримати кожен subagent?
4. Які files/artifacts треба писати у filesystem?
5. Що має повернути кожен subagent у compact final report?
6. Які permissions треба заборонити?
7. Який final verification step має виконати main agent?

Production angle: обовʼязково додай cost/token budget, timeout, trace ID propagation і audit log для tool calls.

---

## 13. Невідомо / не підтверджено

- Unknown / Not confirmed from official source: що Claude Code є “leading coding agent” або “top coding agent”. Це оцінне market claim, не технічний факт.
- Unknown / Not confirmed from official source: точна внутрішня implementation architecture Claude Code поза тим, що описано в official docs.
- Unknown / Not confirmed from official source: чи всі vendors реалізують deep research agents однаково.
- Unknown / Not confirmed from official source: конкретні guarantees щодо runtime duration minutes/hours/days для кожного product.
- Unknown / Not confirmed from official source: точна behavior of Cursor CLI або Gemini CLI у контексті deep agents, бо в цій verification pass вони не перевірялись.

---

## 14. Version-sensitive моменти

- Deep Agents SDK APIs, tool names і model examples можуть змінюватися.
- Claude Code subagent behavior, permissions, built-in agents і available tools можуть змінюватися.
- Context compression thresholds у LangChain Deep Agents є version-sensitive.
- Model provider strings у docs є version-sensitive і не повинні сприйматися як stable architecture principle.
- Product claims про Claude Code, Cursor, Gemini CLI або ChatGPT research мають перевірятися перед production decision.
