---
type: daily-review-note
topic: Deep Agent Skills: progressive disclosure, middleware and Remotion example
area: Agents
date: 2026-06-07
tags:
  - deep-agents
  - agent-skills
  - progressive-disclosure
  - langchain
  - langsmith
  - remotion
  - middleware
  - context-engineering
  - ai-platform-engineering
status: active-review
review:
  - 2026-06-08
  - 2026-06-10
  - 2026-06-14
  - 2026-06-21
  - 2026-07-07
source_type: mixed
source_confidence: high
verification_status: partially-verified
official_sources_checked:
  - LangChain Deep Agents overview
  - LangChain Deep Agents skills documentation
  - LangChain Deep Agents GitHub repository
  - LangChain Deep Agents skills.py source code
  - Remotion Agent Skills documentation
  - Remotion GitHub repository
---

# Daily Review Note: Deep Agent Skills і progressive disclosure

## 1. Основна ідея

### Пояснення на основі джерела

Матеріал пояснює agent skills на прикладі LangChain Deep Agents. Ідея skills: не тримати всі інструкції, best practices, scripts і reference docs у system prompt постійно. Замість цього agent бачить короткі metadata skills і читає повні інструкції тільки тоді, коли конкретна skill релевантна задачі.

Source подає три рівні розуміння skills:

1. використати skill як user через Deep Agents CLI;
2. подивитися execution trace в LangSmith і зрозуміти, що саме потрапляє в LLM context;
3. відкрити source code `skills.py` і побачити, як LangChain Deep Agents реалізують progressive disclosure.

Ключова ідея: skill mechanism — це context engineering pattern, який дає agent доступ до domain knowledge без постійного роздування context window.

### Перевірено проти офіційних джерел

Офіційна LangChain документація підтверджує, що skills packaging domain expertise у reusable directories, а agent на startup отримує summary і читає contained files тільки коли вони relevant. Документація також прямо називає progressive disclosure і описує три стадії: discovery, read, execute.

### Додатковий backend / production context

Agent skill можна сприймати як lazy-loaded plugin documentation:

```text
metadata у prompt завжди
-> повний SKILL.md тільки when needed
-> supporting files тільки when needed
```

Це схоже на production service, який не вантажить усі configuration profiles, runbooks і reference docs у memory, а тримає index і читає потрібні artifacts on demand.

---

## 2. Чому це важливо

### Пояснення на основі джерела

Якщо завантажувати всі instructions для всіх skills одразу, system prompt швидко стане великим і дорогим. Багато інструкцій будуть нерелевантні конкретній задачі, але все одно займуть tokens і можуть впливати на model behavior.

Skills вирішують це через progressive disclosure:

- на старті agent знає names, descriptions і locations skills;
- коли user task збігається з skill description, agent читає `SKILL.md`;
- якщо `SKILL.md` посилається на supporting files, agent читає їх додатково;
- LLM сама вирішує, які skill files треба прочитати.

### Додатковий backend / production context

Це важливо для AI Platform Engineering, бо skills дають контрольований спосіб масштабувати agent knowledge:

- не переписувати system prompt для кожного domain;
- мати reusable skill libraries;
- version skills як files/artifacts;
- робити skills read-only у production;
- мати tenant/project/user-specific skills;
- зменшувати token cost і context pollution.

---

## 3. Як це працює

### Пояснення на основі джерела

#### 3.1 Рівень 1: використання skill через CLI

У lecture показано приклад із Remotion skill. Remotion описаний як open-source package для створення videos with React/code. User встановлює Remotion skill і запускає Deep Agents CLI. Після цього agent може побачити available skills і використати Remotion skill для створення video або GIF.

Офіційна Remotion documentation підтверджує, що Remotion maintains Agent Skills для best practices у Remotion projects і що їх можна встановити командою:

```bash
npx skills add remotion-dev/skills
```

#### 3.2 Рівень 2: tracing через LangSmith

У lecture tracing використовується, щоб побачити, що саме потрапляє в LLM call. Спочатку agent має тільки skill metadata: name, description і path. Повний content skill ще не завантажений.

Коли user просить створити Remotion GIF/video, LLM бачить metadata і вирішує прочитати relevant `SKILL.md` через filesystem tool. Потім може прочитати supporting files, наприклад rules або assets, якщо вважає їх потрібними.

#### 3.3 Рівень 3: source code `skills.py`

Офіційний `skills.py` підтверджує, що `SkillsMiddleware` завантажує skills from backend sources і injects them into the system prompt using progressive disclosure: metadata first, full content on demand.

Механіка:

1. `before_agent` loads skills metadata before agent execution.
2. Metadata зберігається в agent state як `skills_metadata`.
3. Якщо `skills_metadata` вже є в state, load skipped.
4. Sources loaded in order; later sources override earlier ones when skill names conflict.
5. Перед model call middleware appends skills section to system prompt.
6. LLM отримує available skills і instructions how to use skills.
7. LLM сама вирішує, чи треба читати full `SKILL.md` через `read_file`.

#### 3.4 Що таке `SKILL.md`

Офіційна LangChain docs каже, що skill — це directory з `SKILL.md`. Файл має YAML frontmatter з `name` і `description`, після чого йдуть markdown instructions.

Приклад структури:

```text
skills/
└── remotion-best-practices/
    ├── SKILL.md
    ├── rules/
    └── assets/
```

`description` особливо важливий: під час discovery agent бачить саме description і на його основі вирішує, чи skill підходить до task.

#### 3.5 Progressive disclosure

Progressive disclosure у Deep Agents складається з трьох стадій:

1. **Discovery** — middleware scans configured skill paths, parses frontmatter і injects names/descriptions into system prompt.
2. **Read** — якщо skill matches task, agent читає full `SKILL.md` через `read_file`.
3. **Execute** — agent follows skill instructions і читає supporting files only as needed.

Important correction: у transcript звучить “dynamic disclosure”, але official docs/source code використовують термін **progressive disclosure**. У нотатці використовується official term.

---

## 4. Перевірено проти офіційних джерел

| Твердження | Статус | Джерело перевірки | Рішення |
|---|---|---|---|
| Deep Agents is an open-source agent harness | confirmed | LangChain Deep Agents overview, GitHub repo | використано |
| Deep Agents skills package workflows, best practices, scripts, reference docs and templates | confirmed | LangChain skills docs | використано |
| Agent gets skill summary on startup and reads contained files only when relevant | confirmed | LangChain skills docs | використано |
| Skill is directory with `SKILL.md` and YAML frontmatter `name`/`description` | confirmed | LangChain skills docs | використано |
| Progressive disclosure has discovery/read/execute stages | confirmed | LangChain skills docs | використано |
| `SkillsMiddleware` loads metadata and injects it into system prompt | confirmed | `skills.py` source code | використано |
| Sources are loaded in order and later sources override earlier same-name skills | confirmed | `skills.py` source code, LangChain docs | використано |
| Remotion maintains Agent Skills and install command is `npx skills add remotion-dev/skills` | confirmed | Remotion Agent Skills docs | використано |
| “dynamic disclosure” is the official term | corrected | LangChain docs/source use “progressive disclosure” | виправлено на progressive disclosure |
| Deep Agents CLI exact executable names and flags from transcript | unknown | not fully verified against current CLI docs in this pass | не включено як stable fact |
| Anthropic Claude Sonnet 4.6 from transcript | version-sensitive / unknown | not checked as current model availability | не використано як factual claim |
| Claude Code, Cursor CLI, Gemini CLI, Manus are closed source | partially verified / product claim | not fully checked for all products | використано обережно як source framing, не як official fact |

Висновок: нотатка є **partially verified**. Core claims щодо LangChain Deep Agents skills і Remotion skills підтверджені official docs/source code. Product-specific CLI/model claims із transcript не зафіксовані як stable facts.

---

## 5. Backend-аналогія

### Пояснення на основі джерела

Skills працюють як selective knowledge loading. Agent не тримає повні інструкції всіх skills у prompt. Він тримає index і читає деталі тільки коли task цього потребує.

### Додатковий backend / production context

| Agent skills concept | Backend analogy |
|---|---|
| Skill metadata | Service registry entry / plugin manifest |
| `SKILL.md` frontmatter | Plugin descriptor / routing metadata |
| Skill description | Routing key / capability description |
| Supporting files | Runbooks, templates, scripts, reference docs |
| Progressive disclosure | Lazy loading / on-demand dependency loading |
| `SkillsMiddleware` | Request middleware / context injector |
| `skills_metadata` in state | Cached capability registry |
| Source override order | Configuration layering: base -> user -> project -> team |
| Read-only skills | Immutable production config / managed library |

Mental model:

```text
Skill = reusable domain-specific capability package.
SkillsMiddleware = indexer + prompt injector.
LLM = router that decides whether to read the full skill.
```

---

## 6. Production relevance / значення для production

### Пояснення на основі джерела

Skills зменшують context load, бо agent отримує тільки metadata, а full instructions читає on demand. Це допомагає масштабувати agent knowledge без величезного static system prompt.

### Додатковий backend / production context

Production benefits:

- менший prompt size;
- нижчий token cost;
- менше context pollution;
- reusable domain instructions;
- простіше versioning skill libraries;
- можливість project/user/tenant-specific skills;
- краща maintainability порівняно з monolithic system prompt.

Production risks:

- skill description надто vague → agent не активує потрібну skill;
- overlapping descriptions → agent вибирає wrong skill;
- skill body надто великий → progressive disclosure втрачає сенс;
- writable shared skills → agent може пошкодити common knowledge base;
- untrusted skills → prompt injection, malicious scripts, data exfiltration;
- too many skills → selection quality degrades;
- stale skill files → agent follows outdated runbooks.

Controls:

- keep frontmatter concise;
- make `description` specific and task-oriented;
- keep `SKILL.md` focused;
- move detailed reference docs into supporting files;
- make shared skills read-only;
- require human approval for writes;
- validate skill frontmatter;
- audit reads/writes and tool calls;
- version skills with PR review.

---

## 7. Ключові терміни

| Термін | Значення |
|---|---|
| Agent skill | Reusable directory з domain knowledge, workflows, scripts або templates |
| `SKILL.md` | Main markdown file skill із YAML frontmatter і instructions |
| Frontmatter | YAML metadata на початку `SKILL.md`, включно з `name` і `description` |
| Progressive disclosure | Pattern, де agent бачить metadata first і читає full content only when relevant |
| Discovery | Stage, де middleware знаходить skills і extracts metadata |
| Read | Stage, де agent читає full `SKILL.md` через `read_file` |
| Execute | Stage, де agent follows instructions і читає supporting files as needed |
| `SkillsMiddleware` | LangChain middleware, який loads skills metadata and injects prompt section |
| `skills_metadata` | Agent state field зі списком loaded skill metadata |
| Skill source | Backend path, де зберігаються skill directories |
| Source override | Later skill source overrides earlier same-name skill |
| Remotion | Tool/package ecosystem for creating videos programmatically with React/code |

---

## 8. Типові помилки

### Пояснення на основі джерела

1. Думати, що full skill content завжди завантажується в system prompt.
   - Official docs кажуть, що agent бачить summary і читає contained files тільки when relevant.

2. Плутати discovery і activation.
   - Discovery adds metadata. Activation/read happens when agent decides skill matches task.

3. Робити vague `description` у frontmatter.
   - Agent вирішує, чи читати skill, на основі description.

4. Класти все в один великий `SKILL.md`.
   - Supporting files краще читати only as needed.

5. Вважати “dynamic disclosure” official term.
   - Official term у LangChain docs/source: progressive disclosure.

### Додатковий backend / production context

6. Давати skills write access у shared production library.
7. Не робити review skills як code/config.
8. Не логувати, які skills були discovered/read/executed.
9. Не перевіряти skills на prompt injection.
10. Створювати багато overlapping skills замість кількох well-scoped skills.

---

## 9. Flashcards / картки для повторення

Q: Що таке agent skill?
A: Це reusable directory з `SKILL.md` і optional supporting files, яка дає agent domain knowledge, workflows або best practices.

Q: Навіщо потрібне progressive disclosure?
A: Щоб не завантажувати всі skill instructions у system prompt, а читати full content тільки коли skill релевантна задачі.

Q: Які три стадії progressive disclosure у Deep Agents?
A: Discovery, Read, Execute.

Q: Що agent бачить на discovery stage?
A: Skill metadata: name, description і path/location, але не весь content skill.

Q: Чому `description` у `SKILL.md` критично важливий?
A: Agent використовує description, щоб вирішити, чи skill підходить до user task.

Q: Яку роль виконує `SkillsMiddleware`?
A: Він loads skills metadata from sources і injects skills section into system prompt.

Q: Що підтверджує `skills.py` про source override?
A: Sources loaded in order, and later sources override earlier same-name skills.

Q: Що було corrected у transcript?
A: Термін “dynamic disclosure” замінено на official term “progressive disclosure”.

Q: Для чого Remotion skill у прикладі?
A: Щоб дати agent best practices для створення Remotion video/GIF з React/code.

Q: Який production risk має writable shared skill library?
A: Agent або malicious input може змінити shared instructions і вплинути на інших users/agents.

---

## 10. Interview Q&A / питання для співбесіди

### Q1: Що таке agent skills у Deep Agents?

**Відповідь:** Це reusable packages з domain instructions, workflows, reference docs, scripts або templates, які agent може читати on demand.

### Q2: Чому skills кращі за великий static system prompt?

**Відповідь:** Вони зменшують context size: у prompt потрапляє metadata, а full instructions читаються тільки when relevant.

### Q3: Що таке progressive disclosure?

**Відповідь:** Це pattern, де information відкривається agent поступово: metadata first, full `SKILL.md` on demand, supporting files only as needed.

### Q4: Як `SkillsMiddleware` працює на high level?

**Відповідь:** Він scans skill sources, parses `SKILL.md` frontmatter, stores metadata in agent state і injects skill info into system prompt before model calls.

### Q5: Який minimum structure має skill?

**Відповідь:** Directory з `SKILL.md`, де є YAML frontmatter з `name` і `description`, а нижче — markdown instructions.

### Q6: Хто вирішує, чи читати full skill instructions?

**Відповідь:** LLM/agent decides based on skill metadata and task context; окремого dedicated activation mechanism у LangChain docs не описано.

### Q7: Який trade-off skills?

**Відповідь:** Вони економлять context, але якість залежить від accurate descriptions, non-overlapping skill design і правильних permissions.

### Q8: Які observability events треба логувати для skills?

**Відповідь:** Discovered skills, selected skill, `SKILL.md` reads, supporting file reads, tool calls, errors, token cost і final result.

### Q9: Який security risk має skill із scripts?

**Відповідь:** Skill може містити executable helper scripts; без sandboxing/permissions це ризик malicious execution або data leakage.

### Q10: Чому source override order важливий?

**Відповідь:** Later sources can override earlier same-name skills, що корисно для layering, але може створити unexpected behavior без governance.

---

## 11. Самоперевірка

1. Яку проблему вирішують agent skills?
   - Вони дозволяють lazy-load domain knowledge без великого static system prompt.

2. Які три стадії progressive disclosure?
   - Discovery, Read, Execute.

3. Що містить `SKILL.md`?
   - YAML frontmatter з `name`/`description` і markdown instructions.

4. Чому `description` має бути specific?
   - Agent використовує description для deciding whether a skill applies.

5. Що робить `before_agent` у `SkillsMiddleware`?
   - Loads skills metadata before agent execution and stores it in state.

6. Що відбувається, якщо `skills_metadata` already present?
   - Loading is skipped according to `skills.py`.

7. Як працює source override?
   - Later sources override earlier skills with same name.

8. Чому Remotion skill не треба завантажувати повністю на кожний prompt?
   - Бо full instructions потрібні тільки для Remotion-related tasks.

9. Який production control потрібен для shared skills?
   - Read-only permissions, PR review, validation and audit logs.

10. Що було виправлено порівняно з transcript wording?
   - Використано official term progressive disclosure замість “dynamic disclosure”.

---

## 12. Міні-практичне завдання

Спроєктуй skill для Java/Spring Boot incident analysis agent.

Створи sketch структури:

```text
skills/
└── spring-boot-incident-analysis/
    ├── SKILL.md
    ├── references/
    │   ├── log-patterns.md
    │   ├── kafka-failure-modes.md
    │   └── database-transaction-checklist.md
    └── scripts/
        └── parse-trace-ids.py
```

У `SKILL.md` опиши:

1. `name`;
2. `description`, за яким agent зрозуміє, коли skill релевантна;
3. step-by-step workflow;
4. коли читати кожен reference file;
5. які destructive actions заборонені;
6. які artifacts agent має записати після analysis.

Production angle: додай правила read-only для shared skill files, audit log для кожного file read/script execution і human approval для будь-яких write operations у repo.

---

## 13. Невідомо / не підтверджено

- Unknown / Not confirmed from official source: exact current Deep Agents CLI executable names and flags shown in transcript.
- Unknown / Not confirmed from official source: current availability of the exact Anthropic model name mentioned in transcript.
- Unknown / Not confirmed from official source: whether all named coding agents implement skills with the same mechanism.
- Unknown / Not confirmed from official source: exact LangSmith environment variables from transcript, because this note focused on skills middleware and not LangSmith setup.
- Unknown / Not confirmed from official source: current default skills installed by Deep Agents CLI in every environment.

---

## 14. Version-sensitive моменти

- Deep Agents CLI commands and installation flow can change.
- LangSmith tracing environment variables can change.
- `SkillsMiddleware` internals can change.
- `SKILL.md` frontmatter specification can evolve.
- Remotion skills installation flow can change.
- Model names and provider strings from examples are version-sensitive.
- Security behavior for executable skill scripts depends on backend, permissions and sandbox configuration.
