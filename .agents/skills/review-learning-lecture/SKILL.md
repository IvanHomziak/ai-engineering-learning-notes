---
name: review-learning-lecture
description: Independently review one generated lecture for correctness, explanation depth, self-containment, source coverage, code quality, and production value. Produce a scored quality report and exact repair requirements. Do not assume the generator's self-check is correct.
---

# Review Learning Lecture

## Purpose

Evaluate one generated lecture independently from the generation step.

The reviewer must decide whether the lecture is a complete learning module, not
merely whether headings and files exist.

## Required reading

1. Read the root `AGENTS.md`.
2. Read `prompts/master-learning-prompt.md`.
3. Read `prompts/lecture-depth-contract.md`.
4. Read the section manifest and the selected lecture entry.
5. Read the assigned transcript ranges, code, tests, and configuration.
6. Read the generated `lecture.md` and `generation-report.md`.

Do not trust the generator's claims about coverage, execution, verification, or
completeness without checking them.

## Output

Write:

```text
_artifacts/drafts/<lecture-id>/quality-review.md
```

The report must contain:

- lecture ID;
- review attempt number;
- final score;
- category scores;
- critical defects;
- missing explanations;
- source coverage gaps;
- factual or version-sensitive concerns;
- code walkthrough gaps;
- production-depth gaps;
- exact required repairs;
- final status.

## Review procedure

### 1. Atomic scope

Check whether the lecture has one central topic and a manageable set of primary
concepts. Fail the lecture when independent technologies are compressed into a
shallow ecosystem summary while being presented as fully covered.

### 2. Technical correctness

Check definitions, execution flow, API behavior, code, diagrams, alternatives,
and version-sensitive claims. Prefer official sources when verification is
available. A critical factual error is an automatic failure.

### 3. Explanation depth

For each primary concept verify:

- definition;
- problem solved;
- internal mechanics;
- lifecycle or execution sequence;
- inputs and outputs;
- worked example;
- limitations;
- alternatives;
- failure modes;
- testing and observability implications.

A table row or one short paragraph does not satisfy this requirement.

### 4. Self-containment

Assess whether a Senior Java Engineer new to the technology can understand the
fundamental topic and implement the example without searching for foundational
explanations elsewhere.

Fail when the lecture repeatedly names concepts without explaining how they
work.

### 5. Source coverage

Map the lecture back to every assigned transcript range and relevant source
file. Identify omitted, distorted, duplicated, or incorrectly deferred
material.

### 6. Code explanation

When code applies, verify:

- responsibilities and data types are explained;
- the call sequence is traceable;
- framework behavior is explained;
- error paths and production limitations are covered;
- testing is actionable;
- original and supplementary code are distinguished.

### 7. Production depth

Security, reliability, observability, and testing must describe concrete
mechanisms. Lists of terms or metrics without placement, meaning, detection, or
recovery do not pass.

### 8. Depth heuristic

Record approximate word count. A lecture below 2,500 words requires convincing
scope-based justification. A lecture with many required sections and fewer than
2,000 words normally fails explanation depth and self-containment.

Do not pass padded or repetitive content merely because it is long.

## Scoring

Score out of 100:

| Category | Maximum |
|---|---:|
| Technical correctness | 20 |
| Explanation depth | 20 |
| Self-containment | 15 |
| Source coverage | 15 |
| Code explanation | 10 |
| Production value | 10 |
| Structure and readability | 5 |
| Traceability and verification | 5 |

Use `N/A` for code only when neither assigned nor supplementary code is useful;
redistribute those 10 points proportionally across depth, self-containment, and
production value.

## Pass criteria

Set `QUALITY_PASSED` only when:

- total score is at least 85/100;
- correctness is at least 16/20;
- depth is at least 16/20;
- self-containment is at least 12/15;
- source coverage is at least 12/15;
- code explanation is at least 8/10 when applicable;
- production value is at least 8/10;
- no critical factual, security, source-coverage, or publication defect remains.

Otherwise set `QUALITY_FAILED`.

## Repair requirements

For every failure, provide precise edits rather than generic advice.

Good repair instruction:

```text
Expand the LCEL section with the concrete Runnable sequence from input dict to
ChatPromptValue, BaseMessage list, AIMessage, and StrOutputParser output. Explain
operator overloading for `|`, show the resulting composition object, and add a
failure path for parser errors.
```

Bad repair instruction:

```text
Add more detail.
```

The reviewer does not rewrite the lecture. It returns the repair contract to
`generate-learning-lecture`.
