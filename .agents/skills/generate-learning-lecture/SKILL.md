---
name: generate-learning-lecture
description: Generate or repair exactly one detailed, self-contained production-oriented lecture from a validated section manifest and assigned sources. Apply the lecture depth contract and return the draft for independent review.
---

# Generate Learning Lecture

## Purpose

Generate or repair exactly one technical lecture.

This skill does not grant final quality approval. It produces a draft that must
be evaluated by `review-learning-lecture`.

## Required reading

Before working:

1. Read the root `AGENTS.md`.
2. Read `prompts/master-learning-prompt.md`.
3. Read `prompts/lecture-depth-contract.md`.
4. Read the validated section manifest.
5. Locate the requested lecture entry.
6. Read only sources assigned to that lecture.
7. Read prerequisite summaries when necessary.
8. In repair mode, read `quality-review.md` and address every required fix.

## Required inputs

- lecture ID;
- validated manifest path;
- mode: `GENERATE` or `REPAIR`;
- in repair mode, the path to the failed quality review.

## Preconditions

Stop when:

- the manifest does not exist or is not `VALID`;
- the lecture ID is absent;
- assigned source files do not exist;
- prerequisites are incomplete;
- the target contains protected approved or published content;
- repair would ignore a blocking review defect.

A complete existing draft may be reused only when it has a current
`quality-review.md` with `QUALITY_PASSED`.

## 1. Build the content plan

Before drafting, create an internal content plan from the manifest entry:

- central topic;
- primary concepts;
- secondary and deferred concepts;
- required source ranges;
- concept coverage contract;
- required code walkthrough;
- required production concerns;
- version-sensitive claims requiring verification.

If the assigned scope violates the atomic scope rules, do not hide the problem
with a shallow overview. Return a blocking manifest issue.

## 2. Source analysis

Determine:

- which lecturer claims are correct, outdated, incomplete, or ambiguous;
- which explanations must be added as supplementary material;
- which code actually demonstrates the topic;
- which sensitive values require replacement;
- which claims need official verification.

Do not treat transcript claims as verified facts automatically.

## 3. Depth requirements

Follow the complete depth contract.

In particular:

- explain every primary concept with definition, purpose, internal mechanics,
  lifecycle, example, limitations, alternatives, failure modes, testing, and
  observability implications;
- do not use a one-row table as the complete explanation of a primary concept;
- trace the important execution flow with concrete input and output types;
- explain important framework behavior instead of saying the framework handles
  it automatically;
- clearly identify concepts deferred to later lectures;
- make the lecture self-contained for its declared scope.

Target 3,000–7,000 words for most focused or code-heavy lectures. A lecture
below 2,500 words requires a specific completeness justification in
`generation-report.md`. Do not add filler; narrow or split the scope when needed.

## 4. Code requirements

For assigned or supplementary code:

- preserve the source technology as primary;
- explain responsibility, inputs, outputs, order of calls, framework behavior,
  error paths, sync or async implications, and production limitations;
- provide a line-group walkthrough for the central example;
- show a testing approach;
- distinguish original, corrected, and supplementary code;
- never claim successful execution without running the command.

When no lecturer code is assigned, create and label a coherent supplementary
example large enough to demonstrate the central topic.

## 5. External verification

For version-sensitive claims:

- use official documentation, specifications, official repositories, or release
  notes when access is available;
- do not fabricate citations;
- mark unverified claims explicitly;
- record consulted sources in the generation report.

## 6. Draft output

Set lecture status to `GENERATION_IN_PROGRESS` and write:

```text
_artifacts/drafts/<lecture-id>/
├── lecture.md
├── recall-sheet.md
├── quiz.md
└── generation-report.md
```

`generation-report.md` must include:

- lecture ID and generation mode;
- source ranges and files used;
- concept coverage matrix;
- primary, secondary, and deferred concepts;
- official sources consulted;
- assumptions and corrections;
- supplementary material added;
- unverified claims;
- code execution status;
- omitted material and rationale;
- approximate word count;
- depth-contract self-check;
- repair findings addressed, when applicable;
- known limitations.

## 7. Generator self-check

Before returning:

1. Confirm all primary concepts satisfy their coverage contract.
2. Confirm the end-to-end flow contains concrete data transformations.
3. Confirm the central code example has a walkthrough.
4. Confirm security, observability, testing, and failure sections explain
   mechanisms rather than only naming terms.
5. Confirm every assigned source range is covered or explicitly omitted.
6. Confirm the lecture is not an outline or recall sheet disguised as a lecture.
7. Confirm links, Markdown, code fences, and Mermaid blocks are valid.
8. Confirm all four required files exist and are non-empty.
9. Inspect the Git diff.

If draft creation succeeds, set:

```yaml
status: DRAFT_GENERATED
```

Do not set `QUALITY_PASSED`. Return the draft to the independent reviewer.

If generation fails, set `GENERATION_FAILED`, record the exact reason, and stop.
