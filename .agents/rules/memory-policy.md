# Memory policy

## What is worth storing?

Create or update an entry when at least one of these is true:

- You confirmed a hard-to-spot root cause and a fix worth reusing.
- You found an error pattern or workaround likely to recur.
- You made an architecture or product decision with long-term impact.
- A framework, infrastructure or repository quirk made investigation significantly expensive.
- You validated a procedure worth repeating.

**Do not** create an entry for routine edits, obvious information available elsewhere, unverified guesses, one-off results, or generic task summaries with no reusable lesson.

## Mandatory quality bar

Every memory in `active` state must answer:

1. **When is this knowledge useful?** Symptoms, trigger conditions, scope, environment and version.
2. **What is actually known?** The confirmed cause or decision; separate fact from hypothesis.
3. **What should be done?** Short, concrete steps with the important alternatives and risks.
4. **What is the evidence?** Tests, commands or observable evidence and their results.
5. **Where are the sources?** File paths, issue/PR/commit, documentation or other durable sources.

If it cannot answer these, set `status: needs-review` or do not store the entry.

## File names and metadata

- File name: `YYYY-MM-DD-<type>-<short-topic>.md`.
- One topic per file; prefer updating an existing entry over creating a duplicate.
- Required frontmatter fields: `schema_version`, `id`, `title`, `type`, `scope`, `status`, `created`, `updated`, `verified_on`, `confidence`, `tags`, `applies_to`, `sources`, `related`, `supersedes`.
- Allowed `type` values: `bugfix`, `decision`, `pattern`, `workflow`, `environment`.
- Allowed `scope` values: `global`, `project`.
- Allowed `status` values: `active`, `needs-review`, `superseded`, `archived`.
- Allowed `confidence` values: `high`, `medium`, `low`.
- Dates use ISO `YYYY-MM-DD`. Use `schema_version` when the template structure changes; keep content history in Git instead of tracking `v1`, `v2` in every file name.

## Lifecycle

- `active`: evidence checked and the entry holds within its declared scope.
- `needs-review`: useful hint but not verified enough, or no longer known to apply.
- `superseded`: a newer entry replaces the old one; link to the replacement.
- `archived`: kept for historical lookup but excluded from default search.
- When dependencies, the environment or architectural assumptions change, review the affected entries.
- Move an entry to `archive/YYYY/` only when it is outdated, superseded or no longer useful for daily work; never archive just because the directory is large.

## Security and privacy

Never store credentials, secrets, private keys, access tokens, customer personal data or raw sensitive logs. Mask information in examples and use fake values. A local Markdown file is still a data store: apply the same access and repository policy you would apply to code.

## Search and deduplication

- Search by exact error or symbol, symptom, subsystem/file and probable cause.
- Search project memory before global memory.
- Read the metadata and surrounding explanation before applying a result.
- If a new finding overlaps an existing entry, improve that entry and update `updated`/`verified_on` instead of creating another file.
- Avoid a giant `INDEX.md`. The index is only a navigation page for high-value entries; the whole corpus must stay machine-searchable.
