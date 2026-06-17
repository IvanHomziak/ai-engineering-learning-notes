---
type: daily-review-note
topic: LangChain glossary: chat models, messages, documents, splitting, memory
area: LangChain
date: 2026-06-08
tags:
  - langchain
  - chat-models
  - messages
  - document
  - recursive-character-text-splitter
  - short-term-memory
  - langgraph
  - context-engineering
  - rag
status: active-review
review:
  - 2026-06-09
  - 2026-06-11
  - 2026-06-15
  - 2026-06-22
  - 2026-07-08
source_type: mixed
source_confidence: high
verification_status: partially-verified
official_sources_checked:
  - LangChain Models documentation
  - LangChain Messages documentation
  - LangChain RecursiveCharacterTextSplitter documentation
  - LangChain Document reference
  - LangChain Short-term memory documentation
  - LangGraph Persistence documentation
---

# Daily Review Note: LangChain glossary core concepts

## 1. Основна ідея

### Пояснення на основі джерела

Section 23 пояснює базові building blocks LangChain: chat models, messages, `RecursiveCharacterTextSplitter`, `Document`, token/context handling і memory. Ці поняття потрібні, щоб розуміти, як LangChain будує LLM applications: від простого model call до RAG, tool calling, structured output і conversational memory.

Головна mental model:

```text
ChatModel приймає messages
-> повертає AIMessage
-> messages можуть містити tool calls, metadata, multimodal content
-> documents використовуються для RAG/retrieval workflows
-> text splitters готують documents/chunks
-> memory/checkpointers зберігають conversation state між turns
```

### Перевірено проти офіційних джерел

Офіційна LangChain документація підтверджує основні claims: chat models мають standard interface, підтримують invocation methods, tool calling, structured output і multimodal capabilities залежно від provider/model; messages є fundamental unit of context; `Document` є контейнером для text + metadata у retrieval workflows; `RecursiveCharacterTextSplitter` recommended for generic text і splits by separator list; short-term memory у LangChain agents базується на message history і checkpointer.

### Додатковий backend / production context

Для backend engineer LangChain primitives — це contracts між шарами системи:

- `ChatModel` — outbound client до LLM provider;
- `Message` — transport/event object для conversation state;
- `Document` — DTO для retrieval/RAG layer;
- text splitter — preprocessing stage;
- checkpointer — persistence mechanism для stateful workflows;
- trimming/summarization — context budget control.

---

## 2. Чому це важливо

### Пояснення на основі джерела

Без цих primitives легко плутати різні рівні abstraction:

- text prompt vs structured message history;
- model output vs application tool execution;
- document chunk vs chat message;
- token limit workaround vs memory persistence;
- provider capability vs LangChain abstraction.

Transcript правильно пояснює, що сучасні chat models працюють краще з list of messages, а не тільки з одним raw string. Він також правильно підкреслює, що long conversations і large documents впираються в context/token limits.

### Додатковий backend / production context

У production LangChain application ці primitives визначають:

- schema boundaries;
- observability granularity;
- retry/timeout behavior;
- cost control;
- memory lifecycle;
- RAG chunking quality;
- tool-call auditability;
- provider portability.

---

## 3. Як це працює

### Пояснення на основі джерела

#### 3.1 Chat models

`ChatModel` — основний LangChain interface для interaction із modern chat-oriented LLMs.

Input може бути:

- single string;
- list of message dictionaries;
- list of message objects: `SystemMessage`, `HumanMessage`, `AIMessage`, `ToolMessage`.

Output у chat model зазвичай — `AIMessage`, а не raw string.

Офіційно підтверджені key methods:

- `invoke()` — повертає complete response;
- `stream()` — streams output chunks as generated;
- `batch()` — sends multiple requests efficiently;
- `bind_tools()` — makes tools available to model;
- `with_structured_output()` — wraps model for structured response.

#### 3.2 Tool calling

Tool calling означає, що model може повернути request to call a tool. Важливо: model не виконує tool сама. Якщо model використовується standalone, developer має execute requested tool і повернути result у model. Якщо використовується agent abstraction, agent loop handles orchestration.

Типовий flow:

```text
HumanMessage
-> AIMessage with tool_calls
-> application executes tool
-> ToolMessage with tool result
-> model produces final AIMessage
```

#### 3.3 Structured output

Structured output дозволяє отримати response у schema-based format: Pydantic model, `TypedDict` або JSON Schema. Official docs кажуть, що provider support і methods vary: `json_schema`, `function_calling`, `json_mode`.

Це важливо для backend integration, бо downstream code не має парсити arbitrary prose.

#### 3.4 Messages

Messages — core unit of context у LangChain. Вони містять:

- role;
- content;
- optional metadata.

Основні message types:

- `SystemMessage` — instructions/context для model behavior;
- `HumanMessage` — user input;
- `AIMessage` — model output, including text, tool calls, metadata;
- `ToolMessage` — result of tool execution.

Order matters. Для coherent conversation message history має зберігати правильну sequence. Tool call messages мають бути paired з відповідними tool results.

#### 3.5 Multimodal content

Messages можуть містити не тільки text. Official docs підтверджують support for content blocks, including multimodal content, але capability залежить від underlying model/provider.

Висновок: не можна припускати, що будь-який model підтримує images/audio/video. Це provider/model-specific.

#### 3.6 `RecursiveCharacterTextSplitter`

`RecursiveCharacterTextSplitter` — generic text splitter, який намагається split text by separators in order until chunks are small enough. Default separator list:

```python
["\n\n", "\n", " ", ""]
```

Це прагне тримати paragraphs, sentences і words разом якомога довше. Але це heuristic, а не гарантія semantic correctness.

Ключові parameters:

- `chunk_size`;
- `chunk_overlap`;
- `length_function`;
- `is_separator_regex`.

#### 3.7 `Document`

`Document` — LangChain object for retrieval workflows. Він зберігає:

- `page_content`: string text;
- `metadata`: arbitrary metadata dictionary;
- optional `id`.

Important correction: `Document` не призначений для chat I/O. Для conversation input/output треба використовувати message types.

#### 3.8 Token/context handling

Transcript пояснює три older summarization strategies: stuff, map-reduce, refine. Концептуально вони корисні, але як current LangChain guidance їх треба використовувати обережно: official docs сьогодні більше акцентують short-term memory, trimming, deleting, summarization middleware і LangGraph checkpointers.

Актуальні memory/context patterns в official docs:

- trim messages;
- delete messages;
- summarize messages;
- custom strategies;
- use checkpointer to persist conversation state.

#### 3.9 Memory і co-reference resolution

Transcript правильно пояснює проблему: LLM call є stateless, якщо application не передає conversation history. Щоб model зрозуміла “him”, “that”, “same” або “previous one”, application має передати relevant history або summary.

LangChain/LangGraph вирішують це через state, messages і checkpointers.

#### 3.10 LangGraph checkpointers

Official docs кажуть: LangGraph persistence saves graph state as checkpoints. Checkpointer uses `thread_id` as primary key for storing/retrieving checkpoints. Для production recommended database-backed checkpointer.

Official docs mention checkpointer libraries:

- in-memory for experimentation;
- SQLite for local workflows;
- Postgres for production;
- Azure Cosmos DB for Azure production use cases.

---

## 4. Перевірено проти офіційних джерел

| Твердження | Статус | Джерело перевірки | Рішення |
|---|---|---|---|
| Chat models are standard interface for provider integrations | confirmed | LangChain Models docs | використано |
| `invoke`, `stream`, `batch` are key invocation methods | confirmed | LangChain Models docs | використано |
| `bind_tools` makes tools available and model may return tool calls | confirmed | LangChain Models docs | використано |
| Standalone model tool calls require developer to execute tools; agent loop can handle orchestration | confirmed | LangChain Models docs | використано |
| `with_structured_output` supports schemas such as Pydantic, `TypedDict`, JSON Schema | confirmed | LangChain Models docs | використано |
| Messages contain role/content/metadata and standardize provider interaction | confirmed | LangChain Messages docs | використано |
| `ToolMessage.tool_call_id` must match AI tool call id | confirmed | LangChain Messages docs | використано |
| `RecursiveCharacterTextSplitter` splits by default separators `\n\n`, `\n`, space, empty string | confirmed | LangChain recursive splitter docs | використано |
| `Document` stores text and metadata for retrieval workflows, not chat I/O | confirmed | LangChain Document reference | використано |
| Short-term memory uses message history and checkpointers | confirmed | LangChain Short-term memory docs | використано |
| In production, use database-backed checkpointer | confirmed | LangChain Short-term memory docs | використано |
| “Most LLMs nowadays have 4K token limit” | outdated | current model context windows vary widely | виключено як актуальний факт |
| `load_summarize_chain` with `stuff`, `map_reduce`, `refine` is current recommended memory approach | unsupported / likely legacy framing | current docs emphasize middleware/checkpointers | позначено як legacy/course framing |
| Gemini 1.5 Pro 1M token context from transcript | version-sensitive | not verified for current availability | не використано як stable fact |
| Package names in transcript like “link chain llama” | potential transcript artifact | official package names vary | не використано |

Висновок: нотатка є **partially verified**. Core LangChain primitives verified. Claims про exact model token limits, older summarize-chain APIs і model-specific examples не включені як актуальні production facts.

---

## 5. Backend-аналогія

### Пояснення на основі джерела

LangChain objects можна сприймати як typed contracts для LLM application.

### Додатковий backend / production context

| LangChain concept | Backend analogy |
|---|---|
| `ChatModel` | HTTP/gRPC client до external provider |
| `Message` | Event/message envelope |
| `SystemMessage` | Policy/config message |
| `HumanMessage` | Request payload from user |
| `AIMessage` | Response DTO with metadata |
| `ToolMessage` | Result event from external service/tool |
| `Document` | Retrieval DTO / indexed content record |
| Metadata | Headers/tags for filtering and tracing |
| Text splitter | ETL chunking stage |
| Checkpointer | Durable workflow state store |
| Trimming | Retention policy |
| Summarization | Log compaction / state compression |

---

## 6. Production relevance / значення для production

### Пояснення на основі джерела

LangChain abstractions допомагають build applications across providers без переписування всього application logic. Але capabilities залежать від конкретного model/provider.

### Додатковий backend / production context

Production concerns:

- **Provider portability**: standard interface helps, but provider-specific parameters still exist.
- **Timeouts/retries**: configure `timeout` and `max_retries`; official docs note automatic retries for network errors, rate limits and 5xx.
- **Tool calls**: log tool name, args, result, tool_call_id.
- **Structured output**: validate schema; do not trust generated JSON blindly.
- **Chunking**: bad chunking causes poor retrieval quality.
- **Metadata**: weak metadata makes filtering/debugging harder.
- **Memory**: long histories need trimming/summarization; otherwise cost and latency grow.
- **Persistence**: in-memory checkpointer is not production durability.
- **Security**: messages/tool outputs can contain sensitive data; avoid leaking secrets into prompts and traces.

---

## 7. Ключові терміни

| Термін | Значення |
|---|---|
| `ChatModel` | LangChain interface для chat-oriented model calls |
| `invoke()` | Метод для complete model response |
| `stream()` | Метод для incremental output chunks |
| `batch()` | Метод для multiple requests |
| `bind_tools()` | Attach tools to model so it may request tool calls |
| `with_structured_output()` | Wrapper for schema-shaped model output |
| `SystemMessage` | Message with model instructions/context |
| `HumanMessage` | Message representing user input |
| `AIMessage` | Model response message with content, metadata, tool calls |
| `ToolMessage` | Tool execution result sent back to model |
| `Document` | Retrieval object with `page_content` and `metadata` |
| `RecursiveCharacterTextSplitter` | Generic splitter using hierarchical separators |
| Short-term memory | Conversation history/state within a thread/session |
| Checkpointer | LangGraph persistence component that saves graph state |
| Trimming | Removing part of message history to fit context budget |
| Summarization | Replacing older history with compact summary |

---

## 8. Типові помилки

### Пояснення на основі джерела

1. Плутати old-style LLM string input із modern chat model message input.
2. Очікувати raw string від chat model замість `AIMessage`.
3. Думати, що model сама executes tools.
4. Плутати `Document` і `Message`.
5. Вважати recursive splitting semantically perfect.
6. Надсилати всю history без context budget strategy.
7. Вважати in-memory checkpoint production persistence.

### Додатковий backend / production context

8. Не логувати `usage_metadata` і token cost.
9. Не валідувати structured output schema.
10. Не зберігати metadata для chunks.
11. Не враховувати provider-specific behavior для system messages, multimodal input і structured output.
12. Видаляти old messages без перевірки valid message sequence, особливо коли є tool calls.

---

## 9. Flashcards / картки для повторення

Q: Що повертає LangChain chat model після `invoke()`?
A: Зазвичай `AIMessage`, а не raw string.

Q: Чим `Message` відрізняється від `Document`?
A: `Message` використовується для chat/model I/O, а `Document` — для retrieval/RAG workflows.

Q: Навіщо потрібен `ToolMessage`?
A: Щоб передати model результат виконання tool і повʼязати його з original tool call через `tool_call_id`.

Q: Що робить `bind_tools()`?
A: Робить tools доступними model, щоб вона могла повернути tool calls.

Q: Що робить `with_structured_output()`?
A: Налаштовує model на response у визначеній schema: Pydantic, `TypedDict` або JSON Schema.

Q: Як працює `RecursiveCharacterTextSplitter`?
A: Він пробує split text за separators in order, починаючи з більших semantic units, поки chunks не стануть достатньо малими.

Q: Чому token limit не можна вирішувати тільки збільшенням context window?
A: Великий context збільшує cost, latency і ризик context pollution.

Q: Що таке co-reference resolution у memory context?
A: Здатність зрозуміти, що “him”, “that” або “same” посилаються на попередні entities у conversation history.

Q: Для чого потрібен checkpointer?
A: Щоб persist graph/agent state як checkpoints і відновлювати conversation/workflow state через `thread_id`.

Q: Чому `load_summarize_chain`/`map_reduce` треба сприймати обережно?
A: Це корисне course framing, але current LangChain memory docs акцентують middleware, trimming, summarization і LangGraph checkpointers.

---

## 10. Interview Q&A / питання для співбесіди

### Q1: Що таке `ChatModel` у LangChain?

**Відповідь:** Це standard interface для interaction із chat-oriented LLM providers. Він приймає message history або string і зазвичай повертає `AIMessage`.

### Q2: Які key methods має chat model?

**Відповідь:** `invoke`, `stream`, `batch`, а також declarative wrappers на кшталт `bind_tools` і `with_structured_output`.

### Q3: Що таке `AIMessage`?

**Відповідь:** Це model response object, який може містити text, content blocks, tool calls, token usage і provider metadata.

### Q4: Чому `ToolMessage` важливий?

**Відповідь:** Він повертає результат tool execution назад model і має `tool_call_id`, який повʼязує result із конкретним tool call.

### Q5: Чим `Document` відрізняється від chat message?

**Відповідь:** `Document` — це retrieval object для RAG/chunking/vector stores. Chat messages — це conversation I/O для model.

### Q6: Який trade-off має `RecursiveCharacterTextSplitter`?

**Відповідь:** Він простий і generic, намагається зберегти semantic units, але це heuristic і не гарантує perfect semantic chunks.

### Q7: Як LangChain handles long conversation memory?

**Відповідь:** Через message state, checkpointers, trimming, deleting, summarization middleware і custom strategies.

### Q8: Що використовувати для production memory persistence?

**Відповідь:** Database-backed checkpointer, наприклад Postgres або інший supported saver; in-memory варіант підходить для experimentation.

### Q9: Який risk має structured output?

**Відповідь:** Schema-constrained output все одно треба validate; provider support і method behavior можуть відрізнятися.

### Q10: Що треба логувати для production LLM calls?

**Відповідь:** model/provider, input/output tokens, latency, retries, tool calls, tool results, errors, `thread_id`, message IDs і structured parsing errors.

---

## 11. Самоперевірка

1. Чому chat model input краще представляти як messages?
   - Бо messages preserve roles, history, system instructions, tool results і multimodal content.

2. Що повертає `invoke()`?
   - Complete model response, зазвичай `AIMessage`.

3. Коли потрібен `ToolMessage`?
   - Після tool execution, щоб model отримала result.

4. Що має `Document`?
   - `page_content`, `metadata`, optionally `id`.

5. Який default separator order у `RecursiveCharacterTextSplitter`?
   - `\n\n`, `\n`, space, empty string.

6. Чому recursive splitting — heuristic?
   - Він базується на characters/separators, а не на guaranteed semantic understanding.

7. Що робити з long message history?
   - Trim, delete, summarize або custom-process before model call.

8. Для чого checkpointer використовує `thread_id`?
   - Для storing/retrieving checkpoints for a conversation/workflow thread.

9. Що було outdated у transcript?
   - Claim, що більшість LLM мають ~4K token limit nowadays.

10. Який current correction щодо memory?
   - Current LangChain docs emphasize short-term memory patterns, middleware and LangGraph checkpointers, not only legacy summarization chains.

---

## 12. Міні-практичне завдання

Спроєктуй minimal architecture для LangChain-based support assistant, який відповідає на питання по internal docs.

Опиши:

1. Які inputs будуть `Messages`, а які — `Documents`.
2. Як ти chunk-неш documents через `RecursiveCharacterTextSplitter`.
3. Які metadata додаси до кожного `Document`.
4. Як будеш використовувати `bind_tools()` для retrieval/search tool.
5. Яку schema задаси через `with_structured_output()` для final answer.
6. Як будеш зберігати short-term memory через checkpointer.
7. Яку trimming/summarization strategy застосуєш при довгих conversations.

Production angle: додай timeout/retry policy, token budget, tracing через LangSmith, redaction sensitive data і validation structured output.

---

## 13. Невідомо / не підтверджено

- Unknown / Not confirmed from official source: exact current behavior of all provider-specific system message handling.
- Unknown / Not confirmed from official source: current status of old `load_summarize_chain` APIs in every package/version.
- Unknown / Not confirmed from official source: exact token limits of models mentioned in transcript.
- Unknown / Not confirmed from official source: package names distorted by transcript artifacts such as “Linkchain”, “LinkedIn”, “Landgraaf”.
- Unknown / Not confirmed from official source: whether every provider supports the same structured output method.

---

## 14. Version-sensitive моменти

- LangChain package paths and imports can change.
- Model names and context windows are version-sensitive.
- Provider support for tool calling, structured output and multimodality varies.
- `with_structured_output()` methods depend on provider capabilities.
- LangGraph checkpointer libraries and production recommendations can evolve.
- Memory middleware APIs can change.
- Legacy summarize chain APIs may move, change or be deprecated.
