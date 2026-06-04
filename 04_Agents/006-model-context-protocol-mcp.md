---
type: daily-review-note
topic: Model Context Protocol (MCP): architecture, tool calling, servers and clients
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

## 1. Core idea

### Source-based explanation

Model Context Protocol, або MCP, у цьому матеріалі пояснюється як standardization layer для того, як AI applications отримують context, tools, resources і prompts від зовнішніх систем.

Основна проблема: якщо agent має вміти працювати зі Slack, Gmail, database queries або іншими external systems, developer зазвичай пише custom tools під конкретну AI application. Якщо потім цю саму functionality треба використати в Cursor, Windsurf, Cloud Desktop, GitHub Copilot або іншому assistant, доведеться писати багато окремих integrations.

MCP додає abstraction layer:

```text
AI application / MCP host
-> MCP client
-> MCP protocol
-> MCP server
-> tools / resources / prompts / external systems
```

Ідея: implement functionality once as an MCP server, then let any MCP-compatible host connect to it.

### Additional backend / production context

MCP у цій лекції треба думати не як про model feature, а як про **integration protocol for AI applications**. Це схоже на adapter/gateway layer між agent orchestration і real tool execution.

Backend mental model:

```text
Agent orchestration stays in host/application.
Tool execution moves behind MCP server boundary.
```

### Assumptions

- Нотатка побудована тільки на наданому transcript Section 17.
- External MCP documentation не перевірялась у цій нотатці.
- Усі claims про popularity, vendor support, future registry/discovery/OAuth або ChatGPT support трактуються як source claims і version-sensitive.

### Unknowns

- Unknown / Not confirmed from source: current official MCP specification details.
- Unknown / Not confirmed from source: exact transport semantics for stdio, SSE, SSH, Docker or remote deployment.
- Unknown / Not confirmed from source: exact support status in ChatGPT, Cursor, Windsurf, Cloud Desktop, GitHub Copilot or other products.
- Unknown / Not confirmed from source: exact method names and schemas for `list_prompts`, `get_prompt`, `list_tools`, `call_tool`, `list_resource_templates`, `progress_notification`.

---

## 2. Why it matters

### Source-based explanation

MCP matters because it avoids writing the same custom integration repeatedly for every AI application.

Without MCP:

```text
Tool implementation for Cursor
Tool implementation for Windsurf
Tool implementation for Cloud Desktop
Tool implementation for GitHub Copilot
Tool implementation for every custom agent
```

With MCP:

```text
One MCP server exposing capability
Many MCP-compatible hosts can connect to it
```

Source uses the analogy of USB-C: an MCP server is like an external device that can be plugged into different AI applications if they support the protocol.

MCP also changes where tool execution happens. In a vanilla LangChain-style agent, tools usually execute inside the application/agent runtime. With MCP, the tool call is sent to the MCP server, and the server executes the tool.

### Additional backend / production context

This is important for AI Platform Engineering because MCP introduces a clean separation:

- host/application handles user interaction and orchestration;
- client handles protocol communication;
- server owns tools/resources/prompts and execution;
- external systems remain behind server-side integration boundaries.

This can improve:

- reuse across agents;
- deployment independence;
- scaling tool execution separately;
- observability around tool servers;
- standardization of AI integrations;
- governance and access control if implemented correctly.

---

## 3. How it works

### Source-based explanation

#### 3.1 LLMs do not execute tools

Source reminds that LLMs are token generators. They output text/tokens. They do not directly search the web, query databases, send emails, or execute Python functions.

Those extra capabilities are implemented in the **application layer** by software engineers.

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

Source emphasizes: tool calling does not work 100% because LLMs are statistical token predictors, but it works well enough for many agentic applications.

#### 3.2 Why MCP is needed

If tools are custom-written inside one AI application, they are tightly coupled to that application. MCP solves this by exposing tools through an MCP server, so multiple MCP hosts can reuse the same capability.

#### 3.3 MCP architecture components

Source identifies these components:

| Component | Source-based meaning |
|---|---|
| MCP host | AI application that supports MCP, e.g. IDE/assistant/specialized agent |
| MCP client | Component inside the host that talks to one MCP server |
| MCP server | Server/wrapper/interface exposing tools, resources and prompts |
| Tools | Model-controlled functions the AI can invoke |
| Resources | Application-controlled data exposed to the AI system |
| Prompts | User-controlled templates for common interactions |
| Protocol | Standard language/methods between MCP client and MCP server |

#### 3.4 Client/server relationship

Source says there is a **1-to-1 connection between one MCP client and one MCP server**. If a host wants to connect to multiple MCP servers, it has multiple MCP clients inside the host.

```text
MCP host
  -> MCP client A -> MCP server A
  -> MCP client B -> MCP server B
  -> MCP client C -> MCP server C
```

#### 3.5 Initialization flow

When the application starts:

1. MCP host starts.
2. MCP client initializes connection to MCP server.
3. MCP server acknowledges the client.
4. MCP server exposes available capabilities.
5. Client learns available tools/resources/prompts.
6. Application can later augment user queries with available tools.

This happens before user interaction in the source explanation.

#### 3.6 Runtime tool calling flow with MCP

When user sends a query:

1. User sends query to AI application / MCP host.
2. Host knows available tools from MCP server initialization.
3. Host sends user query + available tools to LLM.
4. LLM returns either answer or tool call.
5. If tool call exists, host/client sends tool call and arguments to MCP server.
6. MCP server executes the tool.
7. MCP server returns tool result to MCP client/host.
8. Host sends original query + tool result back to LLM.
9. LLM returns final answer or requests another tool call.
10. Host returns final answer to user.

#### 3.7 What MCP servers expose

MCP servers expose three primary interfaces:

1. **Tools** — model-controlled functions invoked when needed.
2. **Resources** — application-controlled data exposed to AI, static or dynamic.
3. **Prompts** — user-controlled templates for common interactions.

#### 3.8 MCP server implementation options

Source lists these options:

- manually create MCP server in Python or Node.js;
- use AI tools/generators to create MCP servers;
- use community-built open-source MCP servers;
- use official MCP servers/integrations maintained by companies.

Source advice: do not reinvent the wheel. Before building a third-party integration MCP server, check whether the vendor already provides one.

#### 3.9 Running MCP servers

Source says MCP servers can run:

- locally via standard input/output channel;
- remotely via server-sent events or SSH;
- as Docker containers.

Exact implementation details are not provided in the transcript.

#### 3.10 Sampling and composability

Source mentions sampling: MCP server can request the host AI system to generate a completion for a prompt. Source says this is powerful but has security and privacy implications.

Source also says an application/agent can be both MCP client and MCP server, enabling composable multi-layer agentic applications.

---

## 4. Backend analogy

### Source-based explanation

MCP standardizes how AI applications connect to tools/resources/prompts. It decouples host orchestration from tool execution.

### Additional backend / production context

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

But unlike normal RPC, one side is an AI host that exposes capabilities to an LLM as context/tool choices.

---

## 5. Production relevance

### Source-based explanation

Source claims MCP gives several architectural advantages:

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

### Additional backend / production context

#### Reliability

MCP does not remove agent failure modes. It moves some of them into distributed integration boundaries:

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

## 6. Key terms

### Source-based explanation

| Term | Meaning |
|---|---|
| MCP | Model Context Protocol; standardization layer for context/tools/resources/prompts between AI applications and servers |
| MCP host | AI application that supports MCP, e.g. IDE, desktop assistant or custom agent |
| MCP client | Component inside host that communicates with one MCP server |
| MCP server | Server exposing tools, resources and prompts in standardized way |
| Tool | Model-controlled function AI can invoke through MCP server |
| Resource | Application-controlled data exposed to AI system |
| Prompt | User-controlled template for common interactions |
| Tool calling | Mechanism where LLM outputs tool name and arguments instead of directly performing action |
| Observation / tool result | Result returned after tool execution |
| Stdio | Local standard input/output channel mentioned as local server transport |
| SSE | Server-sent events, mentioned as remote transport option |
| Sampling | MCP server requesting host AI system to generate a completion for a prompt |
| Composability | Ability for application/agent to be both MCP client and MCP server |
| Supply-chain attack | Risk from malicious or fake MCP servers/integrations |

---

## 7. Common mistakes

### Source-based explanation

1. Thinking LLMs execute tools directly.
   - Source says LLMs generate tokens; tool execution is external application/server code.

2. Embedding every tool into every AI application.
   - Source says this leads to repeated integrations; MCP solves this with a standard server interface.

3. Confusing model with AI application.
   - Source distinguishes model from host applications like Cursor/Cloud Desktop.

4. Thinking MCP server only exposes tools.
   - Source says MCP servers expose tools, resources and prompts.

5. Assuming one MCP client can talk to many MCP servers.
   - Source says there is a 1-to-1 connection between an MCP client and MCP server.

6. Reinventing third-party MCP servers.
   - Source recommends checking official/community servers first.

### Additional backend / production context

7. Trusting community MCP servers blindly.
   - Review source, permissions, credentials and data access.

8. Giving MCP tools destructive permissions by default.
   - Avoid delete/send/purchase/write capabilities unless explicitly needed and guarded.

9. No observability across host/client/server boundary.
   - Debugging MCP failures requires traces across all layers.

10. No versioning for MCP server capabilities.
   - Dynamic tool discovery can break clients if contracts change without compatibility discipline.

---

## 8. Flashcards

Q: What problem does MCP solve?
A: It avoids rewriting the same tool/resource/prompt integrations separately for every AI application by exposing them through a standard MCP server.

Q: Does an LLM execute tools directly?
A: No. The LLM outputs a tool call; application/server code executes the actual tool.

Q: What is an MCP host?
A: An AI application that supports MCP and can be augmented with external tools, resources or prompts.

Q: What is an MCP client?
A: The component inside the host that communicates with an MCP server.

Q: What is an MCP server?
A: A standardized wrapper/interface that exposes tools, resources and prompts to MCP-compatible hosts.

Q: What are the three primary interfaces exposed by MCP servers?
A: Tools, resources and prompts.

Q: Where does tool execution happen in the MCP flow described in the source?
A: In the MCP server runtime, not inside the host application.

Q: What is the source's client/server cardinality claim?
A: One MCP client connects to one MCP server; multiple servers require multiple clients inside the host.

Q: Why is MCP compared to USB-C?
A: Because a compatible server can plug into different AI applications that support the protocol.

Q: What is a major security risk with community MCP servers?
A: Supply-chain risk from malicious or fake servers that can steal data or run harmful code.

Q: What is sampling in the source?
A: A capability where the MCP server requests the host AI system to generate a completion for a prompt.

Q: What is the main architectural benefit of MCP?
A: It decouples agent orchestration from reusable tool/resource/prompt execution services.

---

## 9. Interview Q&A

### Q1: What is MCP?

**Answer:** MCP, or Model Context Protocol, is a protocol for standardizing how AI applications connect to external tools, resources and prompts through MCP servers.

### Q2: Why do we need MCP if agents already support tools?

**Answer:** Without MCP, tools are often custom-built inside one app. MCP lets developers expose a capability once as a server and reuse it across multiple MCP-compatible hosts.

### Q3: What is the difference between MCP host, client and server?

**Answer:** Host is the AI application. Client lives inside the host and speaks MCP. Server exposes tools, resources and prompts and executes tool calls.

### Q4: How does tool calling work with MCP?

**Answer:** The host sends user query and available tools to the LLM. If the LLM returns a tool call, the MCP client sends it to the MCP server, server executes it, and the result goes back to the host/LLM.

### Q5: Where does tool execution happen in MCP?

**Answer:** According to the source, tool execution happens in the MCP server, which decouples tools from the host application runtime.

### Q6: What can MCP servers expose?

**Answer:** Tools, resources and prompts.

### Q7: What is the key difference between vanilla LangChain-style tools and MCP flow?

**Answer:** In vanilla LangChain-style agents, tools often execute inside the application runtime. In MCP, tool execution is delegated to an MCP server over a standard protocol.

### Q8: What are MCP production risks?

**Answer:** Server unavailability, protocol mismatch, tool schema drift, wrong tool calls, supply-chain attacks, over-permissioned tools, credential leakage and weak observability.

### Q9: Why should you not reinvent MCP servers?

**Answer:** Source says many community or official servers may already exist. Reusing/reviewing them can save work, but security review is still required.

### Q10: What is sampling and why is it sensitive?

**Answer:** Sampling lets an MCP server ask the host AI system for a completion. Source says it is powerful but has security and privacy implications.

---

## 10. Self-check

Answer without looking:

1. What problem does MCP solve?
2. Why are LLMs not actually performing actions?
3. What is the role of MCP host?
4. What is the role of MCP client?
5. What is the role of MCP server?
6. What are the three primary things MCP servers expose?
7. What happens during initialization?
8. Where does tool execution happen in the MCP flow?
9. Why is decoupling tool execution useful?
10. What security risks does the source mention?

Expected answers:

1. It standardizes reusable integrations so tools/resources/prompts can be implemented once and used across MCP-compatible AI apps.
2. LLMs generate tokens; external application/server code performs actions.
3. The AI application that supports MCP and uses MCP clients.
4. The host-side component that connects to one MCP server.
5. The server that exposes and executes tools and exposes resources/prompts.
6. Tools, resources and prompts.
7. Host/client connects to server; server acknowledges and exposes available capabilities.
8. In the MCP server runtime.
9. It improves reuse, scaling, debugging, deployment independence and separation of orchestration from execution.
10. Supply-chain attacks, malicious fake servers, sampling privacy/security implications, and need for future authentication/verification.

---

## 11. Mini practice task

### Source-based practice

Draw the MCP runtime flow:

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

Then explain in 5 sentences how this differs from a vanilla agent where tools execute inside the app.

### Additional backend / production context task

Design a minimal MCP server readiness checklist:

1. What tools/resources/prompts does it expose?
2. Which credentials does it need?
3. Which actions are read-only vs write/destructive?
4. What user confirmation is required?
5. How are tool calls logged and audited?
6. How are errors and timeouts returned to the host?
7. How is the server versioned?
8. How will you verify the server is official/trusted?

### Unknowns

- Unknown / Not confirmed from source: exact MCP wire format and current official protocol methods.
- Unknown / Not confirmed from source: exact current product support for MCP across named AI applications.
- Unknown / Not confirmed from source: exact authentication/session support status.
- Unknown / Not confirmed from source: exact security model for sampling.
