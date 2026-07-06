---
name: publish-learning-lecture
description: Publish one quality-approved lecture from its draft package into the mapped numbered learning directory, create missing directories through files, update the section index, and record the published path without overwriting protected content.
---

# Publish Learning Lecture

## Purpose

Move one reviewed lecture from draft state into the correct learning directory.

Only lectures with `QUALITY_PASSED` may be published.

## Required reading

1. Read the root `AGENTS.md`.
2. Read `config/learning-domain-map.yml`.
3. Read the section manifest and selected lecture entry.
4. Read `quality-review.md` and confirm `QUALITY_PASSED`.
5. Read the final draft `lecture.md`.

## Preconditions

Stop when:

- quality review is missing or failed;
- manifest validation is not `VALID`;
- the draft lecture is missing or empty;
- the target root directory cannot be resolved;
- publication would silently overwrite different protected content;
- the lecture contains unresolved secrets or private paths.

## Resolve the target directory

Use this order:

1. lecture-level `target_root_directory` when explicitly present;
2. section-level `target_root_directory` from the manifest;
3. domain mapping from `config/learning-domain-map.yml`;
4. fallback strategy from the mapping file.

For an unmapped domain:

1. inspect existing numbered root directories;
2. choose the next available two-digit prefix;
3. create `<prefix>_<SanitizedDomainName>` through the published files;
4. add the new mapping to `config/learning-domain-map.yml`;
5. record the decision in the section report.

## Publication layout

Publish to:

```text
<target-root-directory>/<section-id>/<lecture-id>-<slug>.md
```

Create or update:

```text
<target-root-directory>/<section-id>/index.md
```

Git does not store empty directories. A directory is considered created when
its lecture or index file is written.

## Published lecture metadata

Ensure the published file starts with YAML frontmatter containing:

```yaml
lecture_id:
course:
section:
topic:
domain:
status: PUBLISHED
source_manifest:
source_bundle:
quality_score:
quality_review:
published_at:
```

Preserve the approved lecture body. Do not shorten or summarize it during
publication.

## Section index

The section `index.md` must include:

- course and section title;
- ordered list of published lectures;
- relative Obsidian links;
- lecture status;
- one-sentence scope description.

Keep manifest order. Do not duplicate links when the publisher is rerun.

## Idempotency and conflicts

When the target file already exists:

- if it is identical to the approved draft, reuse it and report idempotent
  success;
- if it differs and is marked approved or published, stop and report a conflict;
- never replace it silently.

## Manifest updates

After successful publication, set:

```yaml
status: PUBLISHED
published_path: <repository-relative-path>
```

Record the quality score and publication path in the section report.

## Completion

Before returning:

1. Confirm the published file exists and is non-empty.
2. Confirm the section index links to it.
3. Confirm links are repository-relative and Obsidian-compatible.
4. Confirm the draft remains available for traceability.
5. Confirm no unrelated files changed.
6. Inspect the Git diff.
