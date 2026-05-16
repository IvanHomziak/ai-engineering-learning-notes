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
source_type: mixed
source_confidence: medium
verified_against_external_sources: 2026-05-16
external_sources:
  - arXiv 2210.03629: ReAct: Synergizing Reasoning and Acting in Language Models
  - LangChain documentation: tools and tool calling
  - LangSmith documentation: traceable decorator / custom instrumentation
  - Ollama documentation: tool calling
---

# Щоденна нотатка для повторення: Core Architecture of AI Agents

## 1. Основна ідея

### Пояснення на основі джерела

AI agent у цьому матеріалі пояснюється як система, що виконує **agent loop**: model отримує user query, вирішує чи потрібно викликати tool, application code виконує tool, результат повертається назад у context model як observation, і цикл повторюється до final answer.

У section будуються три рівні одного й того самого e-commerce shopping assistant agent:

1. **LangChain tool calling layer** — використання LangChain primitives: `@tool`, `init_chat_model`, `bind_tools`, `ToolMessage`, message objects.
2. **Raw function calling layer** — без LangChain, напряму через Ollama SDK, з ручними JSON schemas для tools.
3. **Raw ReAct prompt layer** — без function calling і без LangChain: tools описані plain text у prompt, tool calls парсяться regex, history накопичується в scratchpad.

Приклад задачі agent: відповісти на питання user: `What is the price of a laptop after applying a gold discount?`

Tools у source code:

- `get_product_price(product: str) -> float`
- `apply_discount(price: float, discount_tier: str) -> float`

### External documentation verification

External verification confirms the ReAct paper is from **2022** on arXiv (`2210.03629`), not 2023. The earlier note had left the date contradiction unresolved; this version resolves it: the transcript’s “2023” claim should be treated as inaccurate for the paper publication/preprint date.

External docs also support the general implementation framing: LangChain tools can be created from Python functions and bound to chat models, while raw provider SDKs require provider-specific request/response handling.

### Додатковий backend / production context

Ментальна модель для backend engineer: agent loop — це не магія, а orchestration loop з такими етапами:

```text
request -> LLM decision -> tool dispatch -> tool result -> context update -> next LLM decision -> final response
```

Це схоже на workflow engine / saga-like orchestration, але decision step делегований LLM.

### Припущення

- Нотатка базується на transcript + наданих файлах `README.md`, `1_agent_loop_langchain_tool_calling.py`, `2_agent_loop_raw_function_calling.py`, `3_raw_react_prompt.py`, `pyproject.toml`.
- External verification використано для виправлення ReAct date і уточнення general framework/tool-calling behavior.
- Висновки про production наведені окремо як backend / production context.

### Невідоме / не підтверджено джерелом

- Unknown / Not confirmed from source: точна реалізація internal agent loop у LangChain `create_agent` або інших frameworks.
- Unknown / Not confirmed from source: чи Claude Code, Gemini CLI, Codex, Devin реалізують саме такий самий loop у деталях. Transcript стверджує, що agent loop є основою таких систем, але внутрішні реалізації не підтверджені в source.

---

## 2. Чому це важливо

### Пояснення на основі джерела

Ця section важлива, бо вона знімає abstraction layers:

- спочатку agent виглядає як high-level LangChain abstraction;
- потім видно, що LangChain приховує tool schemas, message routing, tool dispatch і provider abstraction;
- потім видно, що навіть function calling можна замінити prompt-only ReAct pattern + regex parsing + scratchpad.

Головна навчальна ціль: зрозуміти, що agent — це цикл reasoning/action/observation, а не окрема “магічна” сутність.

### Додатковий backend / production context

Для AI Platform / LLM Infrastructure engineer це важливо з трьох причин:

1. **Debuggability** — треба розуміти, де зламався flow: model decision, tool schema, argument parsing, tool execution, observation injection, final answer.
2. **Portability** — LangChain abstraction дозволяє простіше міняти model provider, але raw SDK підхід дає більше контролю.
3. **Operational safety** — якщо agent може викликати tools, тоді tool execution стає production boundary: потрібні validation, authorization, retries, timeouts, rate limits, audit logs.

---

## 3. Як це працює

### Пояснення на основі джерела

Agent loop у матеріалі описаний як while loop / ReAct loop:

1. User задає питання.
2. LLM отримує prompt із system rules, query і tool definitions.
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

### Порівняння трьох реалізацій

| Layer | Tool representation | LLM output | Parsing | Tool execution | History / observation |
|---|---|---|---|---|---|
| LangChain tool calling | functions, decorated через `@tool` | structured `tool_calls` | `ai_message.tool_calls[0]` | `tool.invoke(tool_args)` | append `ToolMessage` |
| Raw function calling | manual JSON schemas | structured `tool_calls` | `tool_call.function.name`, `tool_call.function.arguments` | direct function call `tool_to_use(**tool_args)` | append raw tool message; verify provider-required fields like `tool_name` |
| Raw ReAct prompt | plain text tool descriptions у prompt | raw text із `Thought`, `Action`, `Action Input` | regex | direct function call `tools[tool_name](*args)` | append growing scratchpad string |

### Додатковий backend / production context

Production-grade agent loop зазвичай має мати:

- max iteration guard;
- tool registry allowlist;
- argument validation before tool execution;
- tool-level timeout;
- clear error handling for unknown tool names;
- structured logs/traces per iteration;
- protection against tool result hallucination;
- policy layer for sensitive tools.

Source code already includes `MAX_ITERATIONS = 10` and unknown-tool checks in the loop. More advanced controls are not shown in source.

---

## 4. Backend аналогія

### Пояснення на основі джерела

Source frames agent execution as a loop where LLM decides the next action, application code executes the selected tool, and the result is fed back as observation.

### Додатковий backend / production context

```text
Controller / API endpoint
  -> Agent Orchestrator
      -> LLM decision call
      -> Tool dispatcher
          -> domain service / external API / DB lookup
      -> Observation appended to context
      -> Repeat until final response
```

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

### Пояснення на основі джерела

Source explicitly uses:

- LangSmith tracing через `@traceable`;
- local model via Ollama and `qwen3:1.7b`;
- optional OpenAI setup in environment;
- `.env` для API keys і LangSmith tracing settings;
- `uv` для environment setup;
- `pyproject.toml` і `uv.lock` для dependencies and exact versions.

### External documentation verification

Current docs confirm this area is version-sensitive: LangChain, LangSmith and Ollama all expose concrete APIs whose request/response shapes and package paths can evolve. Keep implementation notes tied to the actual installed dependency versions.

### Додатковий backend / production context

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

Corrected: Source material had a date inconsistency around ReAct. External verification confirms ReAct arXiv paper identifier `2210.03629`, i.e. 2022. Treat transcript’s “2023” reference as inaccurate for the paper/preprint date.

---

## 6. Key terms

### Пояснення на основі джерела

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

## 7. Типові помилки

### Пояснення на основі джерела

1. Думати, що LangChain agent abstraction — це весь agent.
   - Source показує, що same agent можна побудувати з LangChain, raw function calling або raw ReAct prompt.

2. Забувати, що LLM не виконує tools.
   - Model decides which tool to call; application code executes the function.

3. Дозволяти model guess product prices or discounts.
   - Source prompt explicitly forbids guessing price, calculating discounts manually, or assuming missing discount tier.

4. Ігнорувати `MAX_ITERATIONS`.
   - Without loop guard, agent can fail to terminate.

5. Treating raw ReAct parsing as robust.
   - Source code comments explicitly call regex parsing fragile if LLM does not follow the format.

6. Assuming function calling removes all risk.
   - Function calling structures tool calls, but tool authorization, validation, and failure handling still belong to application code.

### Додатковий backend / production context

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
| Яка core idea AI agent у цій section? | Agent — це LLM-driven loop, який reasons, selects tools, executes them through application code, observes results, and repeats until final answer. |
| Чи LLM виконує tool сама? | Ні. LLM selects tool and arguments; application code executes actual function. |
| Що таке observation? | Real result returned by tool execution and fed back into agent context. |
| Від чого захищає `MAX_ITERATIONS`? | Infinite або excessively long agent loops. |
| Що приховує LangChain `@tool`? | Tool wrapping і schema generation from function signature/docstring. |
| Що робить `bind_tools()` у source code? | It attaches available tools to chat model. |
| Що показує raw function calling layer? | What LangChain hides: manual JSON schemas, raw SDK calls, message routing, and tool dispatch. |
| Що показує raw ReAct layer? | How agent can work without function calling through prompt format, regex parsing, and scratchpad. |
| Чому regex parsing fragile у raw ReAct? | Because it depends on LLM following exact text format. |
| Яка corrected date для ReAct paper? | External verification confirms arXiv 2210.03629, i.e. 2022. |
| Навіщо `stop=["\nObservation"]` у raw ReAct? | To stop model before it invents observation, so application can inject real tool result. |
| Main production risk of tool-using agents? | Tool execution is a trust boundary and needs validation, authorization, tracing, and failure handling. |

---

## 9. Interview Q&A

### Q1: Що таке agent loop?

**Answer:** Agent loop — repeated execution cycle, де LLM receives user query and current context, decides whether to return answer or call tool, application executes selected tool, appends tool result as observation, and repeats until final answer or max-iteration limit.

### Q2: Різниця між LLM reasoning і tool execution?

**Answer:** LLM decides next action and produces either final text or tool call. Actual tool execution happens in application code, not inside model.

### Q3: Чому LangChain допомагає в agent implementation?

**Answer:** In provided source, LangChain provides `@tool`, `init_chat_model`, `bind_tools`, typed messages, and `ToolMessage`, reducing manual schema writing and message-format boilerplate.

### Q4: Що втрачаємо, коли прибираємо LangChain, але залишаємо function calling?

**Answer:** Треба manually define tool JSON schemas, manually call SDK, manually route messages, manually dispatch tools, and manually represent tool results in message history.

### Q5: Що втрачаємо, коли прибираємо і function calling?

**Answer:** We lose structured tool calls. Model emits plain text, and application must parse `Action` and `Action Input` manually, which is fragile.

### Q6: Навіщо scratchpad у ReAct?

**Answer:** Scratchpad stores previous Thought / Action / Observation steps so model can see what already happened and decide next action.

### Q7: Навіщо `MAX_ITERATIONS`?

**Answer:** Because LLM may repeatedly call tools or fail to produce final answer. Guard prevents unbounded loops, runaway latency, and cost growth.

### Q8: Які production concerns для tool-using agents?

**Answer:** Validate tool args, allowlist tools, enforce timeouts, handle unknown tools, trace every iteration, protect secrets, rate-limit calls, and avoid letting model execute arbitrary actions.

### Q9: Чому raw ReAct корисний для навчання, якщо modern models support function calling?

**Answer:** It exposes underlying mechanism: model follows prompt format, app parses action intent, executes tools, and feeds observations back. It makes agent architecture explicit.

### Q10: Що сказати, якщо питають, чи source доводить exact internals modern coding agents?

**Answer:** Unknown / Not confirmed from source. Transcript claims loop is foundational, but it does not provide implementation details of Claude Code, Gemini CLI, Codex, or Devin.

---

## 10. Self-check

Answer without looking:

1. Які три implementations built in this section?
2. Яка роль `ToolMessage` у LangChain implementation?
3. Що raw function calling implementation requires that LangChain hides?
4. Чому raw ReAct needs regex?
5. Що таке observation?
6. Яка corrected date для ReAct paper?
7. Чому application, not model, should execute tools?
8. Яка production issue може статися, якщо unknown product returns `0`?
9. Чому source uses non-obvious discount percentages?
10. Від чого protects `MAX_ITERATIONS = 10`?

Expected answers:

1. LangChain tool calling, raw function calling with Ollama, raw ReAct prompt with regex/scratchpad.
2. It sends real tool result back into conversation context.
3. Manual JSON schemas, raw SDK calls, message dicts, direct tool dispatch.
4. Because tool calls are emitted as raw text, not structured API fields.
5. Tool execution result returned to LLM context.
6. 2022 / arXiv 2210.03629.
7. Because tools are real application actions and must be controlled, validated, and audited by application code.
8. It may silently produce wrong business result instead of failing fast.
9. To force tool usage instead of model guessing.
10. Infinite or runaway agent loops.

---

## 11. Міні-практика

### Практика на основі джерела

Запусти три надані files і порівняй same question across implementations:

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

### Додатковий backend / production context task

Modify tools to fail explicitly for unknown inputs:

- unknown product should not return `0` silently;
- unknown discount tier should not apply `0%` silently;
- agent should receive a clear error observation.

Then observe whether agent can recover or whether it returns a bad answer.

### Unknowns

- Unknown / Not confirmed from source: exact expected terminal output for every run on every local model environment.
- Unknown / Not confirmed from source: whether `qwen3:1.7b` will behave identically across machines, Ollama versions, and prompts.
