---
name: memory-curation
description: "Find, verify, create, update or replace Markdown memory after solving a problem or finishing work with reusable lessons. Use before significant technical tasks and when closing a task."
---
# Technical memory curation

## When to use
- Before a bug/feature/refactor/migration to look for similar solutions.
- After verifying a root cause, decision, workaround or process that can be reused.
- When you find duplicate, outdated or conflicting memory.

## When not to use
- The work produces no durable knowledge and there is no suitable memory that needs updating.
- You only have unverified hypotheses; you may create a `needs-review` entry if it still has value, but you must state the missing evidence.

## Search-first process
1. Build 2–4 keyword clusters from the symptoms, error message, subsystem, cause and desired behavior.
2. Search project memory first, then global. Skip archive first; search archive only when no result is good enough.
3. Read the full candidate entry; verify `status`, scope, stack/version, `verified_on`, source and applicability conditions.
4. Compare with the current code, tests and documentation. Do not apply memory just because keywords match.

## Distillation process
1. Store only reusable content: a hard-to-spot root cause, a recurring bug, a decision, a dependency/environment pitfall or a conditional workaround.
2. Look for an existing entry first; update it if it covers the same problem. Avoid near-duplicate memory.
3. Use `.agents/template/memory/memory-entry.md`; record the summary, applicability conditions, evidence, root cause/decision, resolution, verification and source links.
4. Set `status: active` only after verification; if an important part remains unverified, use `needs-review` and say so.
5. Update `updated`/`verified_on` from actual events; do not change dates to make an entry look new.
6. If an old entry is no longer correct, mark it `superseded` and link the replacement. Archive only when it must leave regular search.
7. Update `memory/INDEX.md` when an entry is high value or frequently consulted; do not turn the index into a copy of the whole corpus.
8. Do not write secrets, personal data, tokens, sensitive raw logs or information that must not be stored.

## Rules
- Search project memory before global memory; do not skip the project scope.
- Apply an entry only after checking it against the current code, tests and version.
- Prefer updating an existing entry over creating a near-duplicate.
- Set `status: active` only with verification evidence; otherwise use `needs-review` and state what is missing.
- Never store secrets, personal data, tokens or raw sensitive logs, even inside examples.

## Entry quality checklist
- Understandable without reading the whole original conversation.
- States clearly when it applies and when it does not.
- Has evidence/sources and repeatable verification steps.
- Has valid metadata and does not duplicate another entry.

## Completion criteria
- Valuable memory has been created/updated at the right scope, or a reason for not storing it has been established; do not claim completion if the file was not written.

## Related templates
- `.agents/template/memory/memory-entry.md`
- `.agents/template/software/memory-evaluation.md`
