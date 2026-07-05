---
name: start-learning-section
description: Start or resume processing a complete course section. Create and validate its manifest when needed, then generate the remaining lectures one by one in manifest order and preserve progress for later runs.
---

# Start Learning Section

## Command

```text
$start-learning-section
_sources/inbox/<section-id>
```

## Required instructions

Before acting, read:

- root `AGENTS.md`;
- `.agents/skills/plan-course-section/SKILL.md`;
- `.agents/skills/generate-learning-lecture/SKILL.md`;
- source-bundle `context.md` when present.

Use repository-relative paths. The source bundle must be inside the opened
repository. Do not modify source materials.

## Workflow

1. Validate the source directory and ignore dependency or build directories.
2. Resolve `section_id`, domain, manifest path, and section-report path.
3. Load the matching manifest, or call `plan-course-section` to create it.
4. Require manifest `validation_status: VALID`; otherwise report the blocking
   issues and stop.
5. Change valid `PLANNED` lectures to `READY_FOR_GENERATION`.
6. In manifest order, select the first incomplete lecture whose prerequisites
   are satisfied.
7. Set it to `GENERATION_IN_PROGRESS` and call
   `generate-learning-lecture` for that lecture ID.
8. Continue only when the lecture returns `DRAFT_GENERATED` and all required
   files exist and are non-empty.
9. Repeat steps 6–8 until no ready lecture remains.
10. Finalize the section report and set `section_status: DRAFTS_GENERATED` when
    every lecture is `DRAFT_GENERATED` or `SKIPPED`.

## Resume behavior

Do not rewrite valid completed drafts. For `GENERATION_IN_PROGRESS`, inspect the
existing output and either finish it safely or mark the section blocked. Running
the same command again must continue from the first incomplete lecture.

## Required lecture output

```text
_artifacts/drafts/<lecture-id>/
├── lecture.md
├── recall-sheet.md
├── quiz.md
└── generation-report.md
```

Maintain progress in:

```text
_artifacts/section-reports/<section-id>-generation-report.md
```

## Stop conditions

Stop and report the exact reason when the source bundle or manifest is invalid,
a source file or prerequisite is missing, an existing protected artifact would
be overwritten, sensitive data cannot be handled safely, or lecture validation
fails.

Do not run lectures in parallel. Do not publish drafts.

If execution ends because of tool or context limits, preserve current statuses
and report `SECTION_GENERATION_PARTIAL`; the next invocation resumes the work.
