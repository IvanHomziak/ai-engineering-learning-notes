---
name: generate-learning-lecture
description: Generate exactly one detailed production-oriented technical lecture from an approved course-section manifest, assigned transcript fragments, relevant code, and verified external sources. Use only when a specific lecture ID is provided. Never generate multiple lectures.
---

# Generate Learning Lecture

## Purpose

Generate exactly one technical learning lecture.

Never generate more than one lecture during a single invocation.

## Required inputs

The user must provide:

- lecture ID;
- approved manifest path.

Optional inputs:

- questions requiring special attention;
- personal learning objective;
- requested output path override.

## Required reading

Before generating the lecture:

1. Read the root `AGENTS.md`.
2. Read `prompts/master-learning-prompt.md`.
3. Read the specified approved manifest.
4. Locate the requested lecture entry.
5. Read only the transcript sources assigned to that lecture.
6. Read only relevant code and configuration files assigned to that lecture.
7. Read prerequisite lecture summaries only when necessary.

## Preconditions

Stop with a clear error if:

- the manifest does not exist;
- the lecture ID is absent;
- the lecture status is not approved for generation;
- assigned source files do not exist;
- the output file already exists with `APPROVED` or `PUBLISHED` status.

## Source analysis

Before writing:

1. Check whether the source material matches the lecture title.
2. Identify unrelated material.
3. Identify sensitive values and replace them with placeholders.
4. Identify factual and version-sensitive claims.
5. Distinguish lecturer statements, verified facts, assumptions, corrections, and additional explanatory material.
6. Determine whether the supplied code actually demonstrates the lecture topic.

## External verification

For version-sensitive technical claims:

- use current official documentation when internet access is available;
- prefer specifications, official documentation, official repositories, and official release notes;
- do not fabricate citations;
- when a claim cannot be verified, mark it as unverified;
- explicitly describe outdated or incorrect lecturer statements.

## Code handling

For every relevant code example:

- explain its responsibility and execution flow;
- identify framework behavior and hidden lifecycle behavior;
- identify production limitations;
- preserve the original implementation language;
- do not silently modify lecturer-provided code;
- clearly separate original code, corrected code, and additional examples;
- run safe local validation when the project provides an executable build;
- never claim that code was tested when it was not executed.

## Lecture generation

Follow all requirements from:

`prompts/master-learning-prompt.md`

Generate a complete Ukrainian-language lecture focused on the central topic
defined in the manifest.

## Output location

Write the draft under:

`_artifacts/drafts/<lecture-id>/`

At minimum create:

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
- code and configuration files used;
- official sources consulted;
- assumptions;
- corrections;
- unverified claims;
- code execution status;
- omitted material;
- known limitations.

## Validation

Before completing:

1. Verify that the lecture follows the master-prompt structure.
2. Confirm that only the requested lecture was generated.
3. Check that sensitive data was not copied.
4. Check relative links and referenced source paths.
5. Check Markdown code fences.
6. Check Mermaid blocks for obvious syntax errors.
7. Check that code execution status is accurate.
8. Check that corrections and assumptions are explicit.
9. Inspect the Git diff.

## Stop condition

After generating and validating the requested lecture:

1. summarize the files created;
2. report assumptions and corrections;
3. report failed or skipped validations;
4. stop.

Do not generate the next lecture.
Do not publish the lecture automatically.
