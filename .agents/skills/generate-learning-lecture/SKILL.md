---
name: generate-learning-lecture
description: Generate exactly one detailed production-oriented technical lecture from a validated course-section manifest, assigned transcript fragments, relevant code, tests, configurations, and verified external sources. Use for one specific lecture ID. Return the validated result to the calling workflow.
---

# Generate Learning Lecture

## Purpose

Generate exactly one technical learning lecture.

This skill always processes one lecture ID. When called by
`start-learning-section`, it returns control after validation so the
orchestrator can continue with the next lecture.

## Required inputs

The caller must provide:

- lecture ID;
- validated manifest path.

Optional inputs:

- questions requiring special attention;
- personal learning objective;
- requested output path override.

## Required reading

Before generating the lecture:

1. Read the root `AGENTS.md`.
2. Read `prompts/master-learning-prompt.md`.
3. Read the specified manifest.
4. Locate the requested lecture entry.
5. Read only transcript sources assigned to that lecture.
6. Read only code, tests, and configuration assigned to that lecture.
7. Read short prerequisite summaries only when necessary.

## Preconditions

Stop with a clear error if:

- the manifest does not exist;
- manifest `validation_status` is not `VALID`;
- the lecture ID is absent;
- the lecture status is not `READY_FOR_GENERATION` or `GENERATION_IN_PROGRESS`;
- assigned source files do not exist;
- a prerequisite is incomplete;
- the target directory contains an approved or published artifact;
- an existing complete draft would be overwritten.

When a complete draft already exists and passes validation, return it as an
existing successful result instead of rewriting it.

## Source analysis

Before writing:

1. Check whether the assigned source material matches the lecture title.
2. Identify unrelated material.
3. Identify sensitive values and replace them with placeholders.
4. Identify factual and version-sensitive claims.
5. Distinguish lecturer statements, verified facts, assumptions, corrections,
   and additional explanatory material.
6. Determine whether supplied code actually demonstrates the lecture topic.

## External verification

For version-sensitive technical claims:

- use current official documentation when internet access is available;
- prefer specifications, official documentation, official repositories, and
  official release notes;
- do not fabricate citations;
- mark claims as unverified when verification is unavailable;
- explicitly describe outdated or incorrect lecturer statements.

## Code handling

For every relevant code example:

- explain responsibility and execution flow;
- identify framework behavior and hidden lifecycle behavior;
- identify production limitations;
- preserve the original implementation language;
- do not silently modify lecturer-provided code;
- separate original code, corrected code, and additional examples;
- run safe local validation when the project provides an executable build;
- never claim code was tested when it was not executed.

## Lecture generation

Follow all requirements from:

`prompts/master-learning-prompt.md`

Generate a complete Ukrainian-language lecture focused on the central topic
defined in the manifest.

Before writing files, set the lecture workflow status to:

```yaml
status: GENERATION_IN_PROGRESS
```

## Output location

Write the draft under:

`_artifacts/drafts/<lecture-id>/`

Create:

```text
_artifacts/drafts/<lecture-id>/
├── lecture.md
├── recall-sheet.md
├── quiz.md
└── generation-report.md
```

`generation-report.md` must include:

- lecture ID;
- source files and exact ranges used;
- code, test, and configuration files used;
- official sources consulted;
- assumptions;
- corrections;
- unverified claims;
- code execution status;
- omitted material;
- known limitations;
- validation result.

## Validation

Before returning:

1. Verify the lecture follows the master-prompt structure.
2. Confirm only the requested lecture was generated.
3. Check that sensitive data was not copied.
4. Check relative links and referenced source paths.
5. Check Markdown code fences.
6. Check Mermaid blocks for obvious syntax errors.
7. Check that code execution status is accurate.
8. Check that corrections and assumptions are explicit.
9. Confirm all four required draft files exist and are non-empty.
10. Inspect the Git diff.

If validation succeeds, set:

```yaml
status: DRAFT_GENERATED
```

If validation fails, set:

```yaml
status: GENERATION_FAILED
```

Record the reason in `generation-report.md` and return a blocking result to the
caller.

## Completion behavior

After processing the requested lecture:

- summarize files created or reused;
- report assumptions and corrections;
- report failed or skipped checks;
- return the lecture ID, status, and output path to the caller;
- do not publish the lecture.

When invoked directly, stop after this one lecture.
When invoked by `start-learning-section`, allow the caller to continue only when
the lecture status is `DRAFT_GENERATED`.
