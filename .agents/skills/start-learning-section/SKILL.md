---
name: start-learning-section
description: Start or resume processing a complete course section. Create and validate its manifest, generate lectures sequentially, independently review and repair them, then publish quality-approved lectures into mapped numbered learning directories.
---

# Start Learning Section

## Command

```text
$start-learning-section
_sources/inbox/<section-id>
```

## Required reading

Before acting, read:

- root `AGENTS.md`;
- `prompts/lecture-depth-contract.md`;
- `.agents/skills/plan-course-section/SKILL.md`;
- `.agents/skills/generate-learning-lecture/SKILL.md`;
- `.agents/skills/review-learning-lecture/SKILL.md`;
- `.agents/skills/publish-learning-lecture/SKILL.md`;
- `config/learning-domain-map.yml`;
- source-bundle `context.md` when present.

Use repository-relative paths. Do not modify source materials.

## Workflow

1. Validate the source bundle.
2. Resolve section ID, domain, manifest path, target root directory, and section
   report path.
3. Load the matching manifest, or call `plan-course-section` to create it.
4. Require `validation_status: VALID`.
5. Change valid `PLANNED` lectures to `READY_FOR_GENERATION`.
6. Process the first incomplete lecture in manifest order.
7. Generate, review, repair when necessary, publish, then continue to the next
   lecture.
8. Finish only when every non-skipped lecture is `PUBLISHED`.

## Lecture state machine

```text
PLANNED
-> READY_FOR_GENERATION
-> GENERATION_IN_PROGRESS
-> DRAFT_GENERATED
-> QUALITY_REVIEW_IN_PROGRESS
-> QUALITY_PASSED
-> PUBLISHED
```

Failure paths:

```text
QUALITY_FAILED -> REPAIR -> QUALITY_REVIEW_IN_PROGRESS
GENERATION_FAILED -> SECTION_GENERATION_BLOCKED
```

## Generation and review loop

For each lecture:

1. Verify prerequisites are `PUBLISHED` or otherwise satisfied by the manifest.
2. Call `generate-learning-lecture` in `GENERATE` mode.
3. Set `QUALITY_REVIEW_IN_PROGRESS`.
4. Call `review-learning-lecture`.
5. When review returns `QUALITY_PASSED`, call `publish-learning-lecture`.
6. When review returns `QUALITY_FAILED`, increment `repair_attempts` and call
   `generate-learning-lecture` in `REPAIR` mode with `quality-review.md`.
7. Review the repaired lecture again.
8. Allow at most two repair attempts.
9. After two failed repairs, set lecture status `QUALITY_FAILED`, set section
   status `SECTION_GENERATION_BLOCKED`, record exact reasons, and stop.

Do not let the generator approve its own lecture. The independent review result
is authoritative for publication.

## Quality gate

A lecture may continue only when:

- total quality score is at least 85/100;
- every critical category meets its minimum threshold;
- no critical factual, security, source-coverage, or code defect remains;
- `quality-review.md` explicitly states `QUALITY_PASSED`.

A file that merely contains all expected headings is not complete.

## Publication

After `QUALITY_PASSED`:

1. Resolve the target root directory from the manifest or domain map.
2. Create the section subdirectory through its files when it is missing.
3. Publish the approved lecture to:

```text
<target-root-directory>/<section-id>/<lecture-id>-<slug>.md
```

4. Create or update the section `index.md`.
5. Record `published_path` and set lecture status `PUBLISHED`.

Do not remove the draft package after publication.

## Required draft package

```text
_artifacts/drafts/<lecture-id>/
├── lecture.md
├── recall-sheet.md
├── quiz.md
├── generation-report.md
└── quality-review.md
```

## Section report

Maintain:

```text
_artifacts/section-reports/<section-id>-generation-report.md
```

After each state change record:

- lecture ID and current status;
- quality score and repair count;
- generated and published paths;
- blocking defects;
- source and verification warnings;
- code execution result.

## Resume behavior

On rerun:

- do not regenerate `PUBLISHED` lectures;
- validate and reuse `QUALITY_PASSED` drafts that have not yet been published;
- continue repair for `QUALITY_FAILED` when attempts remain;
- inspect `GENERATION_IN_PROGRESS` output before resuming;
- continue from the first incomplete lecture.

## Completion

When every non-skipped lecture is `PUBLISHED`:

1. set `section_status: PUBLISHED`;
2. verify every published path and section index;
3. recheck source coverage;
4. finalize the section report;
5. inspect the Git diff;
6. stop.

If tool or context limits interrupt execution, preserve states and report
`SECTION_GENERATION_PARTIAL`. The same command must resume the workflow.
