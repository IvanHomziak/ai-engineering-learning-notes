---
type: daily-review-note
topic: RAG: Embeddings, Vector Databases and Retrieval
area: RAG
date: 2026-05-15
tags:
  - rag
  - retrieval
  - embeddings
  - vector-databases
  - vector-stores
  - text-splitting
  - chunking
  - langchain
  - pinecone
  - ai-platform-engineering
status: active-review
review:
  - 2026-05-16
  - 2026-05-18
  - 2026-05-22
  - 2026-05-29
  - 2026-06-14
source_type: transcript
source_confidence: medium
---

# Daily Review Note: RAG — Embeddings, Vector Databases and Retrieval

## 1. Core idea

### Source-based explanation

Retrieval Augmented Generation, або RAG, — це техніка, яка дозволяє LLM відповідати на питання на основі великого або приватного набору documents, не вставляючи весь document у prompt.

Проблема з джерела: є великий document, наприклад книга, фінансовий документ або інший приватний файл. User хоче поставити питання, відповідь на яке знаходиться в конкретному paragraph або small section. LLM не знає приватні дані, бо не була trained on them.

Naive solution: вставити весь document у prompt. Це погано масштабується через:

1. hard token limit;
2. needle-in-the-haystack problem;
3. higher cost;
4. higher latency.

RAG solution:

1. split document into chunks;
2. find chunks relevant to user query;
3. augment prompt with only relevant chunks;
4. send query + relevant context to LLM;
5. generate answer grounded on selected context.

У source RAG розкладено так:

- **Retrieval** — знайти relevant chunks.
- **Augmentation** — додати ці chunks у prompt.
- **Generation** — передати augmented prompt у LLM і згенерувати відповідь.

### Additional backend / production context

RAG — це не “LLM знає документ”. Це runtime architecture:

```text
Document ingestion -> chunking -> embeddings -> vector database -> query embedding -> retrieval -> prompt augmentation -> LLM answer
```

Для AI Platform / LLM Infrastructure це важливо, бо RAG додає data plane поруч із inference plane: ingestion, indexing, retrieval, ranking, context assembly, observability, cost control.

### Assumptions

- Нотатка базується тільки на наданому transcript Section 9.
- Зовнішні джерела, LangChain/Pinecone документація і research papers не перевірялись.
- Твердження про long-context models, token limits, Pinecone, LangChain abstractions і embedding behavior беруться тільки з source.

### Unknowns

- Unknown / Not confirmed from source: exact token limits конкретних LLM providers.
- Unknown / Not confirmed from source: exact Pinecone API/classes/configuration.
- Unknown / Not confirmed from source: exact LangChain class names and current package paths for document loaders, text splitters, vector stores, retrieval QA chain.
- Unknown / Not confirmed from source: exact embedding model used in implementation.
- Unknown / Not confirmed from source: exact distance metric used for vector similarity.

---

## 2. Why it matters

### Source-based explanation

RAG потрібен, коли треба question-answering over large/private data:

- large book;
- large financial document;
- private internal data;
- potentially many documents;
- query where answer exists only in a specific paragraph/chunk.

LLM не може відповісти на приватні documents, якщо вона не отримала relevant context у prompt. Вставляти весь document у prompt неефективно й дорого.

RAG робить LLM response більш focused: замість entire book model отримує only relevant paragraph або кілька paragraphs.

### Additional backend / production context

Для backend/system design це важливо, бо RAG вирішує не тільки “knowledge problem”, а й operational problem:

- зменшує prompt size;
- знижує cost per request;
- зменшує latency;
- дозволяє працювати з private/internal data;
- масштабується на multiple documents;
- дає контроль над тим, який context потрапляє в LLM.

Але RAG переносить складність у retrieval pipeline: якість chunks, embeddings, search і context selection напряму впливає на answer quality.

---

## 3. How it works

### Source-based explanation

#### Step 1 — Load documents

Source вводить LangChain document loaders як abstraction для читання documents із різних sources:

- Google Drive;
- Notion notebooks;
- file system;
- PDFs;
- PowerPoint або інші files, які можна представити як text.

У LangChain terminology document — це обʼєкт, який holds text.

#### Step 2 — Split text into chunks

Для long text треба split into smaller chunks. Source називає text splitters abstraction, яка допомагає split text into chunks.

Chunking може бути naive або complex. Source підкреслює, що chunking має depth:

- як саме split document;
- по яких tokens/segments split;
- як зберегти semantically related content;
- як chunk code repository vs normal document;
- що робити з dynamic user documents.

#### Step 3 — Create embeddings

Embedding — це vector representation text. Vector — це sequence of numbers.

Embedding model приймає text/object і повертає array of numbers, який представляє цей object у high-dimensional vector space.

Source mental model:

```text
text in -> embedding model -> vector out
```

Good embedding model розміщує semantically similar texts close together у vector space. Source приклад: sentences про large coffee різними словами або навіть різними languages мають бути close together, якщо meaning similar.

#### Step 4 — Store vectors in vector database

Vector database зберігає embeddings/vectors і дозволяє швидко знайти closest vectors до query vector.

Source називає Pinecone як приклад vector database/vector store.

#### Step 5 — Embed the user query

Коли user ставить question, query також перетворюється на vector через embedding model.

```text
user query -> embedding model -> query vector
```

#### Step 6 — Retrieve relevant chunks

System шукає closest vectors до query vector. Closest vectors represent chunks, які semantically close до query і мають high probability containing answer.

#### Step 7 — Augment prompt

Relevant chunks додаються до prompt як context:

```text
Question: <user question>
Context: <retrieved relevant chunks>
Instruction: use this context to answer
```

#### Step 8 — Generate answer

LLM отримує query + relevant context і генерує answer. У source це має зменшити token limit problem, needle-in-the-haystack problem, cost і latency порівняно з stuffing entire document.

---

## 4. Backend analogy

### Source-based explanation

Source описує RAG як pipeline, де document split into chunks, chunks embedded into vectors, vectors stored in vector database, query embedded, similar chunks retrieved, prompt augmented, LLM generates answer.

### Additional backend / production context

Backend analogy:

| RAG concept | Backend / distributed systems analogy |
|---|---|
| Document loader | ingestion adapter / connector |
| Document | normalized data record with text |
| Text splitter | batch preprocessor / parser |
| Chunk | indexed searchable unit |
| Embedding model | feature extraction service |
| Vector | numeric feature representation |
| Vector database | specialized search index |
| Query embedding | query normalization / feature extraction |
| Retrieval | search/read path |
| Relevant chunks | candidate records |
| Prompt augmentation | request enrichment |
| LLM generation | response synthesis service |

Mental model:

```text
RAG = search system + LLM synthesis layer.
```

Це ближче до backend search architecture, ніж до “model training”.

---

## 5. Production relevance

### Source-based explanation

Source highlights why naive full-document prompting is problematic:

1. Hard token limit.
2. Needle-in-the-haystack problem: long prompts reduce effectiveness.
3. Cost grows with prompt size.
4. Latency grows with prompt size.

Source also highlights RAG drawbacks:

- requires preprocessing;
- chunking is non-trivial;
- different document types need different chunking strategies;
- searching mechanism is required;
- retrieved chunks may not be relevant enough;
- sometimes additional context is needed.

### Additional backend / production context

#### Reliability risks

- Bad chunking can split answer across chunks.
- Retrieval can return irrelevant chunks.
- Relevant chunk may be missing from top results.
- LLM may answer beyond provided context.
- Private data may be stale if index is not refreshed.
- Multi-document retrieval can mix conflicting context.

#### Security risks

- Private documents require access control before retrieval.
- User should retrieve only chunks they are authorized to see.
- Retrieved context can contain sensitive data.
- Prompt injection can exist inside documents.
- Logs/traces must not leak private chunks.

#### Performance / cost risks

- Embedding large corpora costs compute/API calls.
- Vector database storage and query cost can grow with documents/chunks.
- Too many chunks in prompt increases token cost and latency.
- Re-indexing strategy matters for frequently changing documents.

#### Observability concerns

Track:

- document source;
- chunk IDs;
- embedding model version;
- retrieval query;
- retrieved chunk scores/ranks;
- prompt size;
- answer quality;
- missing-answer cases;
- latency per stage: embedding, vector search, LLM generation.

#### Testing / evaluation

RAG quality should be evaluated with known questions and expected source chunks:

- did retrieval find the right chunk?
- did LLM use the retrieved chunk?
- did answer stay grounded?
- did system refuse when context is insufficient?
- did access control filter unauthorized chunks?

### Version-sensitive / may require verification

- Claims about “1 million or 2 million token limit” are model/provider/time-sensitive.
- Pinecone and LangChain APIs are version-sensitive.
- Embedding model quality and multilingual similarity behavior depend on the specific embedding model.
- Vector distance/search behavior depends on vector DB configuration and metric.

### Potential issue

Source sometimes says “Retrieval Augmentation Generation” / “retrieval augmentation generation”. The common expansion is often written as “Retrieval-Augmented Generation”, but this note does not correct the source beyond using the provided RAG meaning.

---

## 6. Key terms

### Source-based explanation

| Term | Meaning |
|---|---|
| RAG | Retrieval + Augmentation + Generation technique for answering with relevant external context |
| Retrieval | Finding relevant chunks for user query |
| Augmentation | Adding retrieved chunks into prompt/context |
| Generation | LLM produces answer using augmented prompt |
| Document loader | LangChain abstraction for loading text data from different sources |
| Document | Text-holding abstraction in LangChain terminology |
| Text splitter | Tool/abstraction for splitting long text into chunks |
| Chunk | Smaller text segment produced from document splitting |
| Embedding | Vector representation of text/object |
| Vector | Sequence/list of numbers |
| Embedding model | Model that converts text/object into vector |
| Vector space | High-dimensional space where vectors represent semantic meaning |
| Vector database | Database that stores vectors and finds closest vectors efficiently |
| Vector store | Storage/search layer for embeddings; source mentions Pinecone |
| Query vector | Embedding of the user question |
| Relevant chunks | Chunks whose vectors are close to query vector |
| Needle-in-the-haystack problem | Long context can make LLM less effective at finding relevant detail |

---

## 7. Common mistakes

### Source-based explanation

1. Stuffing the entire document into prompt.
   - Source says it does not scale because of token limits, cost, latency and reduced effectiveness.

2. Thinking long context window fully solves the problem.
   - Source says even large context windows can be less effective for very long prompts.

3. Ignoring chunking quality.
   - Source says chunking has depth and different documents require different strategies.

4. Assuming retrieved chunks are always relevant.
   - Source says relevant chunks may not be relevant enough and additional context may be needed.

5. Treating embeddings as magic.
   - Source explains embeddings as vectors where semantic similarity is represented by closeness.

### Additional backend / production context

6. No access control in retrieval.
   - Dangerous for private/internal documents.

7. No index freshness strategy.
   - Answers can be based on stale chunks.

8. No retrieval evaluation.
   - You cannot know if failures are retrieval failures or generation failures.

9. Logging raw private context.
   - Can leak sensitive data through traces/logs.

10. Sending too many retrieved chunks.
   - Reintroduces cost, latency and context confusion problems.

---

## 8. Flashcards

Q: What problem does RAG solve?
A: It helps LLM answer questions over large or private documents without putting the entire document into the prompt.

Q: What are the three parts of RAG?
A: Retrieval, Augmentation and Generation.

Q: Why is full-document prompting weak?
A: It hits token limits, increases cost/latency and can make the LLM less effective on long context.

Q: What is a chunk?
A: A smaller text segment created by splitting a larger document.

Q: What is an embedding?
A: A vector representation of text or another object.

Q: What is a vector?
A: A sequence/list of numbers.

Q: What does a good embedding model do?
A: It places semantically similar texts close together in vector space.

Q: What does a vector database do?
A: It stores vectors and finds closest vectors to a query vector.

Q: What is prompt augmentation in RAG?
A: Adding retrieved relevant chunks into the prompt as context.

Q: What is the main production risk in retrieval?
A: The system may retrieve irrelevant, stale, unauthorized or insufficient chunks.

---

## 9. Interview Q&A

### Q1: What is RAG?

**Answer:** RAG is a pattern where the system retrieves relevant chunks from external/private data, augments the prompt with those chunks, and asks the LLM to generate an answer grounded in that context.

### Q2: Why not put the whole document into the prompt?

**Answer:** It does not scale: token limits, higher cost, higher latency and reduced effectiveness on very long contexts.

### Q3: What are embeddings used for in RAG?

**Answer:** Embeddings convert chunks and user queries into vectors so the system can search for semantically similar chunks.

### Q4: What is a vector database?

**Answer:** A database/index that stores embeddings and can efficiently return vectors closest to a query vector.

### Q5: What is chunking and why is it hard?

**Answer:** Chunking splits large documents into smaller segments. It is hard because chunks must preserve useful semantic context and different content types may need different strategies.

### Q6: What does retrieval return?

**Answer:** Relevant chunks whose vectors are close to the query vector and likely contain the answer.

### Q7: What are typical RAG failure modes?

**Answer:** Bad chunking, irrelevant retrieval, missing relevant chunk, stale index, unauthorized context, conflicting chunks and LLM hallucination beyond context.

### Q8: How would you evaluate a RAG system?

**Answer:** Use known questions with expected source chunks and answers. Measure whether retrieval found correct chunks, whether generation used them, and whether answer stayed grounded.

### Q9: What production controls are needed for private data RAG?

**Answer:** Access control before retrieval, context filtering, secure logs/traces, index freshness, auditability and prompt-injection protection for document content.

### Q10: Is RAG model training?

**Answer:** No. Based on the source, RAG provides relevant context at runtime; it does not train the LLM on private data.

---

## 10. Self-check

Answer without looking:

1. What does RAG stand for in the source explanation?
2. Why does full-document prompt stuffing not scale?
3. What is the role of chunking?
4. What is an embedding model?
5. Why embed the user query?
6. What does the vector database return?
7. What does prompt augmentation mean?
8. What are the main RAG drawbacks mentioned in source?
9. Why does private data make RAG useful?
10. What should be observed in production RAG pipeline?

Expected answers:

1. Retrieval, Augmentation, Generation.
2. Token limits, needle-in-the-haystack, cost and latency.
3. Split large documents into smaller searchable pieces.
4. A model that converts text/object into vector representation.
5. To compare the query vector with chunk vectors and find relevant chunks.
6. Closest/relevant vectors and their associated chunks.
7. Adding retrieved chunks to the prompt as context.
8. Preprocessing/chunking complexity, need for search mechanism, possible irrelevant chunks, need for additional context.
9. LLM is not trained on private documents, so relevant private context must be retrieved at runtime.
10. Source documents, chunks, embedding model, retrieved ranks/scores, prompt size, latency and answer quality.

---

## 11. Mini practice task

### Source-based practice

Draw this RAG flow as a simple diagram:

```text
Large document
-> split into chunks
-> embed chunks
-> store vectors in vector database
-> user question
-> embed question
-> retrieve closest chunks
-> augment prompt with chunks
-> LLM generates answer
```

Then explain in 5 sentences why this is better than sending the entire document to the LLM.

### Additional backend / production context task

Design a minimal production checklist for private-document RAG:

1. How will you chunk documents?
2. How will you track document/chunk IDs?
3. How will you enforce user access control before retrieval?
4. How will you detect stale embeddings?
5. What will you log without leaking sensitive data?
6. What test questions prove retrieval works?

### Unknowns

- Unknown / Not confirmed from source: exact LangChain implementation classes and APIs.
- Unknown / Not confirmed from source: exact Pinecone setup.
- Unknown / Not confirmed from source: exact embedding model and vector distance metric.
