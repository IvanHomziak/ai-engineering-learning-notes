---
type: daily-review-note
topic: Core Architecture of AI Agents: Agent Loop, Tools, Function Calling, ReAct
area: Agents
date: 2026-05-10
tags:
  - agents
  - agent-loop
  - react
  - function-calling
  - langchain
  - ollama
  - tools
  - langsmith
  - ai-platform-engineering
status: active-review
review:
  - 2026-05-11
  - 2026-05-13
  - 2026-05-17
  - 2026-05-24
  - 2026-06-09
---

# Daily Review Note: Core Architecture of AI Agents

## 1. Core idea

### Source-based explanation

AI agent у цьому матеріалі пояснюється як система, що виконує **agent loop**: модель отримує user query, вирішує чи потрібно викликати tool, application code виконує tool, результат повертається назад у контекст моделі як observation, і цикл повторюється до final answer.

У section будуються три рівні одного й того самого e-commerce shopping assistant agent:

1. **LangChain tool calling layer** — використання LangChain primitives: `@tool`, `init_chat_model`, `bind_tools`, `ToolMessage`, message objects.
2. **Raw function calling layer** — без LangChain, напряму через Ollama SDK, з ручними JSON schemas для tools.
3. **Raw ReAct prompt layer** — без function calling і без LangChain: tools описані plain text у prompt, tool calls парсяться regex, history накопичується в scratchpad.

Приклад задачі агента: відповісти на питання користувача: `What is the price of a laptop after applying a gold discount?`

Tools у source code:

- `get_product_price(product: str) -> float`
- `apply_discount(price: float, discount_tier: str) -> float`

### Additional backend / production context

Ментальна модель для backend engineer: agent loop — це не магія, а orchestration loop з такими етапами:

```text
request -> LLM decision -> tool dispatch -> tool result -> context update -> next LLM decision -> final response
```

Це схоже на workflow engine / saga-like orchestration, але decision step делегований LLM.

### Assumptions

- Нотатка базується на transcript + наданих файлах `README.md`, `1_agent_loop_langchain_tool_calling.py`, `2_agent_loop_raw_function_calling.py`, `3_raw_react_prompt.py`, `pyproject.toml`.
- Висновки про production наведені окремо як backend / production context.

### Unknowns

- Unknown / Not confirmed from source: точна реалізація internal agent loop у LangChain `create_agent` або інших frameworkʼах.
- Unknown / Not confirmed from source: чи Claude Code, Gemini CLI, Codex, Devin реалізують саме такий самий loop у деталях. Transcript стверджує, що agent loop є основою таких систем, але внутрішні реалізації не підтверджені в source.

---

## 2. Why it matters

### Source-based explanation

Ця section важлива, бо вона знімає abstraction layers:

- спочатку agent виглядає як high-level LangChain abstraction;
- потім видно, що LangChain приховує tool schemas, message routing, tool dispatch і provider abstraction;
- потім видно, що навіть function calling можна замінити prompt-only ReAct pattern + regex parsing + scratchpad.

Головна навчальна ціль: зрозуміти, що agent — це цикл reasoning/action/observation, а не окрема “магічна” сутність.

### Additional backend / production context

Для AI Platform / LLM Infrastructure engineer це важливо з трьох причин:

1. **Debuggability** — треба розуміти, де зламався flow: model decision, tool schema, argument parsing, tool execution, observation injection, final answer.
2. **Portability** — LangChain abstraction дозволяє простіше міняти model provider, але raw SDK підхід дає більше контролю.
3. **Operational safety** — якщо agent може викликати tools, тоді tool execution стає production boundary: потрібні validation, authorization, retries, timeouts, rate limits, audit logs.

### Unknowns

- Unknown / Not confirmed from source: конкретні latency, cost, reliability характеристики LangChain vs raw Ollama implementation.

---

## 3. How it works

### Source-based explanation

Agent loop у матеріалі описаний як while loop / ReAct loop:

1. User задає питання.
2. LLM отримує prompt із системними правилами, query і tool definitions.
3. LLM вирішує:
   - або повернути final answer;
   - або вибрати tool і arguments.
4. Application code виконує вибраний tool.
5. Tool result стає observation.
6. Observation додається назад у context/history/scratchpad.
7. Loop повторюється до final answer або до `MAX_ITERATIONS`.

У LangChain implementation:

```python
llm = init_chat_model(f"ollama:{MODEL}", temperature=0)
llm_with_tools = llm.bind_tools(tools)
ai_message = llm_with_tools.invoke(messages)
tool_calls = ai_message.tool_calls
```

У raw function calling implementation:

```python
response = ollama_chat_traced(messages=messages)
ai_message = response.message
tool_calls = ai_message.tool_calls
```

У raw ReAct implementation:

```python
final_answer_match = re.search(r"Final Answer:\s*(.+)", output)
action_match = re.search(r"Action:\s*(.+)", output)
action_input_match = re.search(r"Action Input:\s*(.+)", output)
```

### Three implementations compared

| Layer | Tool representation | LLM output | Parsing | Tool execution | History / observation |
|---|---|---|---|---|---|
| LangChain tool calling | `@tool` decorated functions | structured `tool_calls` | `ai_message.tool_calls[0]` | `tool.invoke(tool_args)` | append `ToolMessage` |
| Raw function calling | manual JSON schemas | structured `tool_calls` | `tool_call.function.name`, `tool_call.function.arguments` | direct function call `tool_to_use(**tool_args)` | append raw `{role: "tool"}` dict |
| Raw ReAct prompt | plain text tool descriptions in prompt | raw text with `Thought`, `Action`, `Action Input` | regex | direct function call `tools[tool_name](*args)` | append growing scratchpad string |

### Additional backend / production context

Production-grade agent loop should normally have:

- max iteration guard;
- tool registry allowlist;
- argument validation before tool execution;
- tool-level timeout;
- clear error handling for unknown tool names;
- structured logs/traces per iteration;
- protection against tool result hallucination;
- policy layer for sensitive tools.

The source code already includes `MAX_ITERATIONS = 10` and unknown-tool checks in the loop. More advanced controls are not shown in source.

---

## 4. Backend analogy

### Source-based explanation

The source frames agent execution as a loop where LLM decides the next action, application code executes the selected tool, and the result is fed back as observation.

### Additional backend / production context

Backend analogy:

```text
Controller / API endpoint
  -> Agent Orchestrator
      -> LLM decision call
      -> Tool dispatcher
          -> domain service / external API / DB lookup
      -> Observation appended to context
      -> Repeat until final response
```

Mapping:

| Agent concept | Backend / distributed systems analogy |
|---|---|
| User query | inbound API request |
| Agent loop | orchestration loop / workflow engine |
| Tool | application service, adapter, client, command handler |
| Tool schema | API contract / DTO schema |
| Tool call | command invocation |
| Observation | command result / event / service response |
| Scratchpad | accumulated workflow state |
| `MAX_ITERATIONS` | circuit breaker / loop safety guard |
| LangSmith tracing | distributed tracing / observability |

---

## 5. Production relevance

### Source-based explanation

The source explicitly uses:

- LangSmith tracing via `@traceable`;
- local model via Ollama and `qwen3:1.7b`;
- optional OpenAI setup in environment;
- `.env` for API keys and LangSmith tracing settings;
- `uv` for environment setup;
- `pyproject.toml` and `uv.lock` for dependencies and exact versions.

### Additional backend / production context

Production risks and concerns:

#### Reliability

- Agent may loop without final answer; source uses `MAX_ITERATIONS = 10`.
- Model may select wrong tool or wrong arguments.
- Tool may return default fallback like `0` for unknown product; this can hide errors.
- Raw ReAct regex parsing can fail if model output format drifts.

#### Security

- Tool execution is a trust boundary. Never expose arbitrary function execution.
- Tool registry must be allowlisted.
- Tool arguments must be validated before execution.
- Prompt-only ReAct is fragile against prompt injection because the model follows text formatting instructions, not strict structured protocol.
- Secrets in `.env` must never be committed. Transcript states keys shown in video would be revoked, but the safe engineering practice is still: never commit real API keys.

#### Performance / cost

- Each loop iteration may call the LLM again.
- More tool calls mean more latency.
- Larger scratchpad/message history increases token usage.
- Local Ollama avoids external API cost but shifts cost to local compute and model quality constraints.

#### Observability

- Trace each LLM call, tool call, tool result, and final answer.
- In production, store correlation IDs and request IDs across agent iterations.
- LangSmith is used in the source for tracing, but exact production telemetry architecture is Unknown / Not confirmed from source.

#### Version-sensitive

This material is version-sensitive because LangChain, Ollama SDK, model tool-calling behavior, and LangSmith tracing APIs can change. The provided `pyproject.toml` declares dependencies including `langchain`, `langchain-ollama`, `langchain-openai`, `python-dotenv`, `black`, and `isort`, but behavior should be verified against installed versions in the actual environment.

### Potential issue

The source material contains a date inconsistency around ReAct:

- Transcript says the ReAct paper appeared in 2023.
- README says ReAct pattern comes from Yao et al. 2022.

This note does not resolve that contradiction using external sources. Treat the exact publication date as Unknown / Not confirmed from source.

---

## 6. Key terms

### Source-based explanation

| Term | Meaning in this material |
|---|---|
| Agent | LLM-driven loop that can decide whether to call tools or return final answer |
| Agent loop | Repeated cycle: reason, choose action/tool, execute, observe, repeat |
| ReAct loop | Thought / Action / Observation style loop used to implement agents |
| Tool | Python function exposed to the model as an action the application can execute |
| Tool call | Model output indicating which tool to run and with which arguments |
| Observation | Actual result returned by the executed tool |
| Scratchpad | Accumulated reasoning/action/observation history in raw ReAct implementation |
| Function calling | Structured model capability for returning tool calls instead of plain text only |
| JSON schema | Structured tool description used in raw function calling implementation |
| `@tool` | LangChain decorator that wraps Python functions as tools |
| `bind_tools` | LangChain method used to attach tools to the chat model |
| `ToolMessage` | LangChain message type used to send tool results back into the conversation |
| `MAX_ITERATIONS` | Guard preventing infinite agent loop |
| LangSmith | Tracing platform used in source code via `@traceable` |
| Ollama | Local model runtime used in the section |
| `qwen3:1.7b` | Local model name configured in the provided code |

---

## 7. Common mistakes

### Source-based explanation

1. Thinking that LangChain agent abstraction is the whole agent.
   - Source shows the same agent can be built with LangChain, raw function calling, or raw ReAct prompt.

2. Forgetting that LLM does not execute tools.
   - The model decides which tool to call; application code executes the function.

3. Letting the model guess product prices or discounts.
   - Source prompt explicitly forbids guessing price, calculating discounts manually, or assuming missing discount tier.

4. Ignoring `MAX_ITERATIONS`.
   - Without a loop guard, an agent can fail to terminate.

5. Treating raw ReAct parsing as robust.
   - Source code comments explicitly call regex parsing fragile if the LLM does not follow the format.

6. Assuming function calling removes all risk.
   - Function calling structures tool calls, but tool authorization, validation, and failure handling still belong to application code.

### Additional backend / production context

7. Returning `0` for unknown product can be dangerous.
   - In a real e-commerce system, unknown product should likely produce a domain error, not a price of zero.

8. Executing tools without validation is unsafe.
   - Validate product names, discount tiers, numeric ranges, and allowed tool names.

9. Not tracing tool calls makes failures hard to debug.
   - Agent failures are multi-step. Logs need iteration number, model output, selected tool, args, observation, and final answer.

---

## 8. Flashcards

| Question | Answer |
|---|---|
| What is the core idea of an AI agent in this section? | An agent is an LLM-driven loop that reasons, selects tools, executes them through application code, observes results, and repeats until final answer. |
| Does the LLM execute the tool itself? | No. The LLM selects the tool and arguments; application code executes the actual function. |
| What is an observation? | The real result returned by a tool execution and fed back into the agent context. |
| What does `MAX_ITERATIONS` protect against? | Infinite or excessively long agent loops. |
| What does LangChain `@tool` hide? | Tool wrapping and schema generation from function signature/docstring. |
| What does `bind_tools()` do in the source code? | It attaches available tools to the chat model. |
| What is the raw function calling layer meant to show? | What LangChain hides: manual JSON schemas, raw SDK calls, message routing, and tool dispatch. |
| What is the raw ReAct layer meant to show? | How an agent can work without function calling by using prompt format, regex parsing, and scratchpad. |
| Why is regex parsing fragile in raw ReAct? | Because it depends on the LLM following the exact text format. |
| Why is `stop=["\nObservation"]` used in raw ReAct? | To stop the model before it invents the observation, so the application can inject the real tool result. |
| Why are the discount percentages non-obvious in the example? | So the model cannot reliably guess and must use the tools. |
| What is the main production risk of tool-using agents? | Tool execution is a trust boundary and needs validation, authorization, tracing, and failure handling. |

---

## 9. Interview Q&A

### Q1: What is an agent loop?

**Answer:** Agent loop is a repeated execution cycle where an LLM receives the user query and current context, decides whether to return an answer or call a tool, the application executes the selected tool, appends the tool result as observation, and repeats until final answer or max-iteration limit.

### Q2: What is the difference between LLM reasoning and tool execution?

**Answer:** The LLM decides the next action and produces either final text or a tool call. The actual tool execution happens in application code, not inside the model.

### Q3: Why does LangChain help in agent implementation?

**Answer:** In the provided source, LangChain provides `@tool`, `init_chat_model`, `bind_tools`, typed messages, and `ToolMessage`, reducing manual schema writing and message-format boilerplate.

### Q4: What do you lose when removing LangChain but keeping function calling?

**Answer:** You must manually define tool JSON schemas, manually call the SDK, manually route messages, manually dispatch tools, and manually represent tool results in message history.

### Q5: What do you lose when removing function calling too?

**Answer:** You lose structured tool calls. The model emits plain text, and the application must parse `Action` and `Action Input` manually, which is fragile.

### Q6: Why is scratchpad needed in ReAct?

**Answer:** Scratchpad stores previous Thought / Action / Observation steps so the model can see what already happened and decide the next action.

### Q7: Why is `MAX_ITERATIONS` necessary?

**Answer:** Because the LLM may repeatedly call tools or fail to produce final answer. The guard prevents unbounded loops, runaway latency, and cost growth.

### Q8: What are production concerns for tool-using agents?

**Answer:** Validate tool args, allowlist tools, enforce timeouts, handle unknown tools, trace every iteration, protect secrets, rate-limit calls, and avoid letting the model execute arbitrary actions.

### Q9: Why is raw ReAct useful for learning if modern models support function calling?

**Answer:** It exposes the underlying mechanism: the model follows a prompt format, the app parses action intent, executes tools, and feeds observations back. It makes the agent architecture explicit.

### Q10: What should you say if asked whether this source proves exact internals of modern coding agents?

**Answer:** Unknown / Not confirmed from source. The transcript claims the loop is foundational, but it does not provide implementation details of Claude Code, Gemini CLI, Codex, or Devin.

---

## 10. Self-check

Answer without looking:

1. What are the three implementations built in this section?
2. What is the role of `ToolMessage` in the LangChain implementation?
3. What does the raw function calling implementation require that LangChain hides?
4. Why does raw ReAct need regex?
5. What is an observation?
6. Why is `stop=["\nObservation"]` important in raw ReAct?
7. Why should the application, not the model, execute tools?
8. What production issue can happen if unknown product returns `0`?
9. Why does the source use non-obvious discount percentages?
10. What does `MAX_ITERATIONS = 10` protect against?

Expected answers:

1. LangChain tool calling, raw function calling with Ollama, raw ReAct prompt with regex/scratchpad.
2. It sends real tool result back into the conversation context.
3. Manual JSON schemas, raw SDK calls, message dicts, direct tool dispatch.
4. Because tool calls are emitted as raw text, not structured API fields.
5. Tool execution result returned to the LLM context.
6. It prevents the model from hallucinating the tool result before the app injects the real observation.
7. Because tools are real application actions and must be controlled, validated, and audited by application code.
8. It may silently produce wrong business result instead of failing fast.
9. To force tool usage instead of model guessing.
10. Infinite or runaway agent loops.

---

## 11. Mini practice task

### Source-based practice

Run the three provided files and compare the same question across implementations:

```bash
uv run python 1_agent_loop_langchain_tool_calling.py
uv run python 2_agent_loop_raw_function_calling.py
uv run python 3_raw_react_prompt.py
```

Question used in source:

```text
What is the price of a laptop after applying a gold discount?
```

Expected tool flow from source:

```text
get_product_price("laptop") -> 1299.99
apply_discount(1299.99, "gold") -> 1000.99
final answer
```

### Additional backend / production context task

Modify the tools to fail explicitly for unknown inputs:

- unknown product should not return `0` silently;
- unknown discount tier should not apply `0%` silently;
- agent should receive a clear error observation.

Then observe whether the agent can recover or whether it returns a bad answer.

### Unknowns

- Unknown / Not confirmed from source: exact expected terminal output for every run on every local model environment.
- Unknown / Not confirmed from source: whether `qwen3:1.7b` will behave identically across machines, Ollama versions, and prompts.
