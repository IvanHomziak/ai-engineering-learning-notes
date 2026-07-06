# Lecture Quality Remediation Plan

## 1. Problem statement

Generated lectures can satisfy the required Markdown structure while remaining
too shallow to function as self-contained learning material.

Observed failure pattern:

- many independent concepts compressed into one lecture;
- one-row table definitions instead of internal-mechanics explanations;
- generic execution-flow lists without concrete data transformations;
- code shown without a line-group walkthrough;
- security, observability, testing, and failure modes reduced to checklists;
- files marked complete because they exist and are non-empty;
- no independent reviewer between generation and completion.

The result is closer to an outline or recall sheet than a full technical lecture.

## 2. Root causes

1. Manifest validation checked source coverage but not cognitive scope.
2. The generation prompt requested many sections but had no enforceable depth
   contract.
3. The generator reviewed its own output.
4. Quality validation focused on file existence and Markdown correctness.
5. Sequential section generation encouraged short lectures to complete the whole
   run.
6. Publication was not linked to a measurable quality threshold.

## 3. Target state

Each lecture must be:

- atomic in scope;
- technically correct;
- self-contained for its declared topic;
- detailed enough to explain internal mechanics;
- grounded in assigned transcript and code;
- production-oriented;
- independently reviewed;
- repaired when quality fails;
- published only after passing quality thresholds.

## 4. Implemented remediation

### 4.1 Depth contract

Add `prompts/lecture-depth-contract.md` with:

- atomic scope rules;
- concept explanation contract;
- execution-flow contract;
- code walkthrough requirements;
- depth heuristics;
- self-containment test;
- production-depth criteria;
- quality thresholds.

### 4.2 Stronger manifest

Update `plan-course-section` to record:

- primary, secondary, and deferred concepts;
- concept coverage contracts;
- unique draft and publication paths;
- target numbered root directory;
- explicit deferred and excluded material;
- atomic-scope validation.

### 4.3 Stronger generation

Update `generate-learning-lecture` to:

- read the depth contract;
- reject over-broad scopes;
- explain every primary concept deeply;
- provide concrete input-to-output execution flows;
- provide code walkthroughs;
- record concept coverage and approximate word count;
- return a draft without self-approving quality.

### 4.4 Independent quality review

Add `review-learning-lecture` with a 100-point rubric:

- correctness: 20;
- explanation depth: 20;
- self-containment: 15;
- source coverage: 15;
- code explanation: 10;
- production value: 10;
- structure: 5;
- traceability: 5.

Required total: at least 85/100, with minimum critical-category thresholds.

### 4.5 Repair loop

Update `start-learning-section` to:

1. generate one lecture;
2. run independent review;
3. return exact repair requirements;
4. repair the lecture;
5. review again;
6. allow no more than two repair attempts;
7. block the section when quality still fails.

### 4.6 Controlled publication

Add `publish-learning-lecture` and `config/learning-domain-map.yml`.

Only `QUALITY_PASSED` lectures are published to:

```text
<numbered-root-directory>/<section-id>/<lecture-id>-<slug>.md
```

The workflow creates a missing section directory through its lecture and
`index.md` files. For an unmapped domain it creates the next available numbered
root directory and updates the mapping.

## 5. Existing draft migration

Existing drafts must not remain implicitly trusted.

For each lecture currently marked `DRAFT_GENERATED` without a passing
`quality-review.md`:

1. keep the existing files unchanged initially;
2. set status to `QUALITY_REVIEW_IN_PROGRESS`;
3. run `review-learning-lecture` against the original sources;
4. set `QUALITY_PASSED` when it meets all thresholds;
5. otherwise set `QUALITY_FAILED` and create exact repair requirements;
6. run repair mode with at most two attempts;
7. publish only after a passing review.

Do not discard useful existing content. Repair it in place with a traceable
review history.

## 6. Publication mapping

Default root directories:

| Domain | Root directory |
|---|---|
| LangChain | `01_LangChain/` |
| Python | `02_Python/` |
| RAG | `03_RAG/` |
| Agents / LangGraph | `04_Agents/` |
| LLM Gateway | `05_LLM_Gateway/` |
| Spring AI | `06_Spring_AI/` |
| AI Platform | `07_AI_Platform/` |
| Production LLM | `08_Production_LLM/` |
| Interview preparation | `09_Interview_Preparation/` |

A course section receives its own subdirectory and `index.md`.

## 7. Acceptance criteria

The remediation is successful when:

- a broad ecosystem topic is split or explicitly limited to secondary context;
- a shallow 1,000–2,000-word lecture with many sections fails review;
- primary concepts include internal mechanics and concrete examples;
- code examples include a traceable walkthrough;
- production sections describe mechanisms rather than lists;
- every published lecture has `quality-review.md` with `QUALITY_PASSED`;
- every published lecture is stored in the correct root directory;
- missing section directories are created automatically;
- repeated workflow runs do not duplicate or overwrite published files;
- interrupted runs resume from the first incomplete state.

## 8. Test scenario

Use `langchain-section-03` as the first regression test.

1. Run `$start-learning-section _sources/inbox/langchain-section-03`.
2. Verify the manifest does not combine all ecosystem products as equally
   primary concepts.
3. Generate the first lecture.
4. Run independent review.
5. Confirm a shallow lecture is rejected with precise repair requirements.
6. Confirm the repaired lecture reaches at least 85/100.
7. Confirm publication under:

```text
01_LangChain/langchain-section-03/
```

8. Confirm `index.md` contains the published lecture link.
9. Run the command again and confirm idempotent resume behavior.

## 9. Non-goals

This change does not:

- automatically merge generated content into `master`;
- remove source materials;
- claim that length alone guarantees quality;
- require every minor term to become a separate lecture;
- publish a lecture that has not passed review.
