---
type: daily-review-note
topic: Model Context Protocol (MCP): архітектура, tool calling, сервери та клієнти
area: Agents
date: 2026-06-04
tags:
  - mcp
  - model-context-protocol
  - agents
  - tool-calling
  - mcp-server
  - mcp-client
  - mcp-host
  - ai-platform-engineering
  - llm-infrastructure
status: active-review
review:
  - 2026-06-05
  - 2026-06-07
  - 2026-06-11
  - 2026-06-18
  - 2026-07-04
source_type: transcript
source_confidence: medium
---

# Daily Review Note: Model Context Protocol (MCP)

## 1. Основна ідея

### Пояснення на основі джерела

Model Context Protocol, або MCP, у цьому матеріалі пояснюється як стандартний шар інтеграції для того, як AI-додатки отримують контекст, інструменти, ресурси й prompts від зовнішніх систем.

Проблема: якщо agent має працювати зі Slack, Gmail, database queries або іншими external systems, developer зазвичай пише custom tools під конкретний AI-додаток. Якщо потім таку саму функціональність треба використати в Cursor, Windsurf, Cloud Desktop, GitHub Copilot або іншому assistant, доведеться повторно писати інтеграції.

MCP додає abstraction layer:

```text
AI application / MCP host
-> MCP client
-> MCP protocol
-> MCP server
-> tools / resources / prompts / external systems
```

Ідея: реалізувати функціональність один раз як MCP server, після чого будь-який MCP-compatible host зможе підключитися до цього server.

### Додатковий backend / production context

MCP у цій лекції варто сприймати не як можливість самої LLM, а як **інтеграційний протокол для AI applications**. Це схоже на adapter/gateway layer між agent orchestration і реальним виконанням tools.

```text
Agent orchestration stays in host/application.
Tool execution moves behind MCP server boundary.
```

Тобто agent вирішує, **коли** і **який** tool потрібен, а MCP server відповідає за те, **як** цей tool реально виконати.

### Припущення

- Нотатка побудована тільки на наданому transcript Section 17.
- External MCP documentation не перевірялась у цій нотатці.
- Усі твердження про популярність MCP, підтримку vendors, майбутні registry/discovery/OAuth або ChatGPT support трактуються як source claims і version-sensitive.

### Невідомо / не підтверджено джерелом

- Unknown / Not confirmed from source: актуальні деталі офіційної MCP specification.
- Unknown / Not confirmed from source: точна поведінка transport mechanisms: stdio, SSE, SSH, Docker або remote deployment.
- Unknown / Not confirmed from source: актуальний support status у ChatGPT, Cursor, Windsurf, Cloud Desktop, GitHub Copilot або інших products.
- Unknown / Not confirmed from source: точні method names і schemas для `list_prompts`, `get_prompt`, `list_tools`, `call_tool`, `list_resource_templates`, `progress_notification`.

---

## 2. Чому це важливо

### Пояснення на основі джерела

MCP важливий тому, що він прибирає потребу писати одну й ту саму custom integration для кожного AI-додатку окремо.

Без MCP:

```text
Tool implementation for Cursor
Tool implementation for Windsurf
Tool implementation for Cloud Desktop
Tool implementation for GitHub Copilot
Tool implementation for every custom agent
```

З MCP:

```text
One MCP server exposing capability
Many MCP-compatible hosts can connect to it
```

У source використовується аналогія з USB-C: MCP server схожий на зовнішній пристрій, який можна підключити до різних AI applications, якщо вони підтримують protocol.

MCP також змінює місце виконання tools. У vanilla LangChain-style agent tools зазвичай виконуються всередині application/agent runtime. У MCP tool call надсилається до MCP server, і саме server виконує tool.

### Додатковий backend / production context

Для AI Platform Engineering це важливо, бо MCP вводить чисте розділення відповідальностей:

- host/application обробляє user interaction і orchestration;
- client відповідає за protocol communication;
- server володіє tools/resources/prompts і execution;
- external systems залишаються за server-side integration boundary.

Це може покращити:

- повторне використання integrations між різними agents;
- незалежне розгортання MCP servers;
- окреме масштабування tool execution;
- кращу observability навколо tool servers;
- стандартизацію AI integrations;
- governance та access control, якщо це правильно реалізовано.

---

## 3. Як це працює

### Пояснення на основі джерела

#### 3.1 LLM не виконує tools напряму

Source нагадує, що LLM — це token generators. Вони генерують text/tokens. Вони не можуть напряму шукати в web, робити database queries, надсилати emails або виконувати Python functions.

Ці додаткові можливості реалізуються в **application layer** software engineers.

Tool calling flow:

```text
User asks question
-> LLM receives query + available tools
-> LLM outputs a tool call in provider-specific format
-> application parses tool call
-> application executes external code/tool
-> application sends tool result back to LLM
-> LLM generates final answer or another tool call
```

Source підкреслює: tool calling не працює 100%, бо LLM є statistical token predictors, але часто працює достатньо добре для agentic applications.

#### 3.2 Навіщо потрібен MCP

Якщо tools custom-written всередині одного AI-додатку, вони tightly coupled до цього додатку. MCP вирішує це через exposing tools through an MCP server, щоб multiple MCP hosts могли reuse the same capability.

#### 3.3 Архітектурні компоненти MCP

| Компонент | Значення на основі джерела |
|---|---|
| MCP host | AI application, який підтримує MCP: IDE, assistant або specialized agent |
| MCP client | Component всередині host, який говорить з одним MCP server |
| MCP server | Server/wrapper/interface, який exposes tools, resources and prompts |
| Tools | Model-controlled functions, які AI може invoke |
| Resources | Application-controlled data, exposed to the AI system |
| Prompts | User-controlled templates for common interactions |
| Protocol | Standard language/methods між MCP client і MCP server |

#### 3.4 Відношення client/server

Source каже, що існує **1-to-1 connection між одним MCP client і одним MCP server**. Якщо host хоче підключитися до multiple MCP servers, він має multiple MCP clients всередині host.

```text
MCP host
  -> MCP client A -> MCP server A
  -> MCP client B -> MCP server B
  -> MCP client C -> MCP server C
```

#### 3.5 Initialization flow

Коли application стартує:

1. MCP host стартує.
2. MCP client ініціалізує connection до MCP server.
3. MCP server підтверджує client.
4. MCP server exposes available capabilities.
5. Client отримує список available tools/resources/prompts.
6. Application пізніше може augment user queries цими available tools.

У source explanation це відбувається ще до user interaction.

#### 3.6 Runtime tool calling flow with MCP

Коли user надсилає query:

1. User надсилає query до AI application / MCP host.
2. Host знає available tools з MCP server initialization.
3. Host надсилає user query + available tools до LLM.
4. LLM повертає або answer, або tool call.
5. Якщо є tool call, host/client надсилає tool call і arguments до MCP server.
6. MCP server виконує tool.
7. MCP server повертає tool result до MCP client/host.
8. Host надсилає original query + tool result назад до LLM.
9. LLM повертає final answer або просить інший tool call.
10. Host повертає final answer до user.

#### 3.7 Що expose MCP servers

MCP servers expose три primary interfaces:

1. **Tools** — model-controlled functions, які invoke when needed.
2. **Resources** — application-controlled data, exposed to AI, static або dynamic.
3. **Prompts** — user-controlled templates for common interactions.

#### 3.8 Варіанти реалізації MCP server

Source називає такі варіанти:

- вручну створити MCP server у Python або Node.js;
- використати AI tools/generators для створення MCP servers;
- використати community-built open-source MCP servers;
- використати official MCP servers/integrations, які підтримують companies.

Source advice: не reinvent the wheel. Перед створенням third-party integration MCP server треба перевірити, чи vendor уже надає готовий server.

#### 3.9 Як можуть запускатися MCP servers

Source says MCP servers can run:

- локально через standard input/output channel;
- remotely via server-sent events або SSH;
- як Docker containers.

Exact implementation details are not provided in the transcript.

#### 3.10 Sampling і composability

Source mentions sampling: MCP server can request the host AI system to generate a completion for a prompt. Source says this is powerful but has security and privacy implications.

Source also says an application/agent can be both MCP client and MCP server, enabling composable multi-layer agentic applications.

---

## 4. Backend-аналогія

### Пояснення на основі джерела

MCP standardizes how AI applications connect to tools/resources/prompts. Він decouples host orchestration from tool execution.

### Додатковий backend / production context

| MCP concept | Backend / distributed systems analogy |
|---|---|
| MCP host | API gateway / frontend application / orchestrator |
| MCP client | typed client / connector / protocol adapter |
| MCP server | integration service / tool gateway / adapter service |
| Tool | command handler / service operation |
| Resource | read model / document/data endpoint |
| Prompt | reusable request template / workflow template |
| Tool call | RPC command / service request |
| Tool result | service response / observation |
| MCP protocol | integration contract / interoperability protocol |
| Multiple clients per host | multiple outbound service clients |
| Server-side tool execution | decoupled service execution boundary |

Mental model:

```text
MCP = standardized RPC-like integration layer for AI tools, resources and prompts.
```

Але на відміну від звичайного RPC, одна сторона — це AI host, який показує capabilities LLM як context/tool choices.

---

## 5. Production relevance / значення для production

### Пояснення на основі джерела

Source claims MCP дає кілька архітектурних переваг:

- plug-and-play integrations across MCP-compatible hosts;
- lower coupling to any one LLM vendor or AI app builder;
- tool execution decoupled from agent/application runtime;
- possible easier debugging, logging, cost tracking and scaling;
- ability to update MCP server independently from agent;
- possibility of dynamic tool discovery if host reinitializes tools periodically;
- community and official MCP servers reduce duplicated work.

Source also mentions security risks:

- community MCP servers can create supply-chain attack risk;
- malicious server could pretend to be an official integration;
- future verification of official servers would help mitigate this;
- sampling has security and privacy implications;
- authentication and OAuth 2.0 support are discussed as future/near-future improvements in the transcript.

### Додатковий backend / production context

#### Reliability

MCP не прибирає agent failure modes. Він переносить частину проблем у distributed integration boundaries:

- MCP server unavailable;
- client/server protocol mismatch;
- tool schema drift;
- tool timeout;
- partial failure during multi-tool workflow;
- stale tool list after server update;
- LLM selects wrong tool or wrong args.

#### Security

Treat MCP servers as external code and external trust boundaries:

- use allowlisted MCP servers;
- verify official/vendor-provided servers;
- review community server source code;
- restrict tool permissions;
- avoid exposing destructive actions by default;
- require user confirmation for high-impact actions;
- apply least privilege to credentials used by MCP servers;
- audit tool calls and tool results;
- isolate local MCP servers if they can access filesystem/secrets.

#### Observability

Trace both host-side and server-side operations:

```text
user query
-> available tools sent to LLM
-> selected tool name and args
-> MCP client request
-> MCP server execution
-> external API/database call
-> tool result
-> final LLM response
```

#### Scalability

Decoupling tool execution into MCP servers can enable independent scaling:

- run servers as separate processes/services;
- deploy frequently used servers independently;
- scale heavy tools separately from host application;
- isolate resource-intensive integrations.

#### Maintainability

MCP server can version and own integration logic separately from agent orchestration code. This is cleaner than embedding every tool implementation inside every AI application.

### Version-sensitive / may require verification

The transcript contains multiple claims that can change quickly:

- MCP popularity and ecosystem size;
- ChatGPT support for MCP;
- exact product support in Cursor, Windsurf, Cloud Desktop, GitHub Copilot;
- registry/discovery roadmap;
- official server verification roadmap;
- OAuth 2.0/session-token support;
- supported transports and exact protocol methods.

These must be verified against current MCP specification and vendor documentation before production decisions.

### Potential issue

Transcript contains repeated “NCP” wording in places where context clearly indicates MCP. This note normalizes it to MCP.

Transcript also mentions “ECS” and “LinkedIn/Linkchain/Long chain” likely as transcription errors for X/Twitter and LangChain. This note does not rely on those exact words as factual claims.

---

## 6. Ключові терміни

### Пояснення на основі джерела

| Термін | Значення |
|---|---|
| MCP | Model Context Protocol; standardization layer для context/tools/resources/prompts між AI applications і servers |
| MCP host | AI application, який підтримує MCP, наприклад IDE, desktop assistant або custom agent |
| MCP client | Component всередині host, який communicates with one MCP server |
| MCP server | Server, який exposes tools, resources and prompts in standardized way |
| Tool | Model-controlled function, яку AI може invoke through MCP server |
| Resource | Application-controlled data, exposed to AI system |
| Prompt | User-controlled template for common interactions |
| Tool calling | Mechanism, де LLM outputs tool name and arguments instead of directly performing action |
| Observation / tool result | Result returned after tool execution |
| Stdio | Local standard input/output channel mentioned as local server transport |
| SSE | Server-sent events, mentioned as remote transport option |
| Sampling | MCP server requesting host AI system to generate a completion for a prompt |
| Composability | Ability for application/agent to be both MCP client and MCP server |
| Supply-chain attack | Risk from malicious or fake MCP servers/integrations |

---

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що LLM виконує tools напряму.
   - Source says LLMs generate tokens; tool execution is external application/server code.

2. Вбудовувати кожен tool у кожен AI-додаток.
   - Source says this leads to repeated integrations; MCP solves this with a standard server interface.

3. Плутати model з AI application.
   - Source distinguishes model from host applications like Cursor/Cloud Desktop.

4. Думати, що MCP server exposes тільки tools.
   - Source says MCP servers expose tools, resources and prompts.

5. Припускати, що один MCP client може говорити з багатьма MCP servers.
   - Source says there is a 1-to-1 connection between an MCP client and MCP server.

6. Повторно реалізовувати third-party MCP servers без перевірки готових варіантів.
   - Source recommends checking official/community servers first.

### Додатковий backend / production context

7. Blindly trusting community MCP servers.
   - Review source, permissions, credentials and data access.

8. Giving MCP tools destructive permissions by default.
   - Avoid delete/send/purchase/write capabilities unless explicitly needed and guarded.

9. No observability across host/client/server boundary.
   - Debugging MCP failures requires traces across all layers.

10. No versioning for MCP server capabilities.
   - Dynamic tool discovery can break clients if contracts change without compatibility discipline.

---

## 8. Flashcards / картки для повторення

Q: Яку проблему вирішує MCP?
A: MCP дозволяє не переписувати ті самі integrations для tools/resources/prompts окремо під кожен AI-додаток, а expose їх через standard MCP server.

Q: Чи LLM виконує tools напряму?
A: Ні. LLM повертає tool call; actual tool виконує application/server code.

Q: Що таке MCP host?
A: Це AI application, який підтримує MCP і може бути augmented external tools, resources або prompts.

Q: Що таке MCP client?
A: Це component всередині host, який communicates with an MCP server.

Q: Що таке MCP server?
A: Це standardized wrapper/interface, який exposes tools, resources and prompts для MCP-compatible hosts.

Q: Які три primary interfaces expose MCP servers?
A: Tools, resources і prompts.

Q: Де відбувається tool execution у MCP flow за source?
A: У runtime MCP server, а не всередині host application.

Q: Який client/server cardinality claim у source?
A: Один MCP client connects to one MCP server; multiple servers require multiple clients inside the host.

Q: Чому MCP порівнюють з USB-C?
A: Тому що compatible server можна plug into different AI applications, якщо вони підтримують protocol.

Q: Який major security risk у community MCP servers?
A: Supply-chain risk: malicious або fake servers можуть steal data або run harmful code.

Q: Що таке sampling у source?
A: Capability, де MCP server requests the host AI system to generate a completion for a prompt.

Q: Яка головна architectural benefit MCP?
A: MCP decouples agent orchestration from reusable tool/resource/prompt execution services.

---

## 9. Interview Q&A / питання для співбесіди

### Q1: Що таке MCP?

**Відповідь:** MCP, або Model Context Protocol, — це protocol для стандартизації того, як AI applications підключаються до external tools, resources і prompts через MCP servers.

### Q2: Навіщо потрібен MCP, якщо agents уже підтримують tools?

**Відповідь:** Без MCP tools часто custom-built всередині одного app. MCP дозволяє expose capability once as a server і reuse її across multiple MCP-compatible hosts.

### Q3: Яка різниця між MCP host, client і server?

**Відповідь:** Host — це AI application. Client lives inside the host and speaks MCP. Server exposes tools, resources and prompts and executes tool calls.

### Q4: Як tool calling працює з MCP?

**Відповідь:** Host sends user query and available tools to the LLM. If the LLM returns a tool call, MCP client sends it to MCP server, server executes it, and result goes back to host/LLM.

### Q5: Де в MCP відбувається tool execution?

**Відповідь:** According to the source, tool execution happens in MCP server, which decouples tools from the host application runtime.

### Q6: Що можуть expose MCP servers?

**Відповідь:** Tools, resources і prompts.

### Q7: Яка ключова різниця між vanilla LangChain-style tools і MCP flow?

**Відповідь:** У vanilla LangChain-style agents tools часто execute inside application runtime. У MCP tool execution delegated to MCP server over a standard protocol.

### Q8: Які production risks має MCP?

**Відповідь:** Server unavailability, protocol mismatch, tool schema drift, wrong tool calls, supply-chain attacks, over-permissioned tools, credential leakage і weak observability.

### Q9: Чому не варто reinvent MCP servers?

**Відповідь:** Source says many community or official servers may already exist. Reusing/reviewing them can save work, but security review is still required.

### Q10: Що таке sampling і чому це sensitive?

**Відповідь:** Sampling lets an MCP server ask the host AI system for a completion. Source says it is powerful but has security and privacy implications.

---

## 10. Самоперевірка

Дай відповідь без підглядання:

1. Яку проблему вирішує MCP?
2. Чому LLM насправді не виконує actions?
3. Яка роль MCP host?
4. Яка роль MCP client?
5. Яка роль MCP server?
6. Які три primary things expose MCP servers?
7. Що відбувається під час initialization?
8. Де відбувається tool execution у MCP flow?
9. Чому decoupling tool execution корисний?
10. Які security risks згадує source?

Очікувані відповіді:

1. MCP standardizes reusable integrations, so tools/resources/prompts can be implemented once and used across MCP-compatible AI apps.
2. LLMs generate tokens; external application/server code performs actions.
3. MCP host — це AI application, який підтримує MCP і використовує MCP clients.
4. MCP client — host-side component, який connects to one MCP server.
5. MCP server exposes and executes tools and exposes resources/prompts.
6. Tools, resources і prompts.
7. Host/client connects to server; server acknowledges and exposes available capabilities.
8. У runtime MCP server.
9. Це покращує reuse, scaling, debugging, deployment independence and separation of orchestration from execution.
10. Supply-chain attacks, malicious fake servers, sampling privacy/security implications і need for future authentication/verification.

---

## 11. Міні-практичне завдання

### Практика на основі джерела

Намалюй MCP runtime flow:

```text
User
-> MCP Host / AI Application
-> LLM receives query + available tools
-> LLM returns tool call
-> MCP Client sends call to MCP Server
-> MCP Server executes tool
-> MCP Server returns result
-> Host sends result back to LLM
-> LLM returns final answer
-> User receives answer
```

Потім поясни у 5 реченнях, чим це відрізняється від vanilla agent, де tools execute inside the app.

### Додатковий backend / production context task

Спроєктуй minimal MCP server readiness checklist:

1. What tools/resources/prompts does it expose?
2. Which credentials does it need?
3. Which actions are read-only vs write/destructive?
4. What user confirmation is required?
5. How are tool calls logged and audited?
6. How are errors and timeouts returned to the host?
7. How is the server versioned?
8. How will you verify the server is official/trusted?

### Невідомо / не підтверджено джерелом

- Unknown / Not confirmed from source: exact MCP wire format and current official protocol methods.
- Unknown / Not confirmed from source: exact current product support for MCP across named AI applications.
- Unknown / Not confirmed from source: exact authentication/session support status.
- Unknown / Not confirmed from source: exact security model for sampling.
