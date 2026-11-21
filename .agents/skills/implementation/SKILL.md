---
name: implementation
description: "Implement a feature or software change according to the requirements, design and existing conventions; keep the diff small, safe and verifiable. Use when there is enough context to change code."
---
# Implement software changes

## When to use
- Adding/changing behavior, API, UI, data access, integration or tooling.
- Continuing work once the requirements and key decisions are clear.

## When not to use
- The defect is not understood or the problem is not reproduced → `bug-investigation`.
- The task is only to assess an existing diff, without changing code → `code-review`.

## Process
1. Search related memory and read the existing files/flow before editing.
2. Determine the acceptance criteria, contract and the scope of affected files.
3. Draft a short plan for multi-step changes; use `implementation-plan.md` when useful.
4. Make the smallest complete change; keep existing style, naming, architecture and dependencies.
5. Handle loading/error/empty state, validation, authorization, retry and idempotency as appropriate to the task type.
6. Do not leave mocks, TODOs or fake fallbacks as production behavior unless explicitly requested.
7. Run local checks after each risky change; update tests together with the behavior.
8. Use `testing-validation` to finish verification, then review the diff.

## Rules
- Do not delete the user's uncommitted changes or overwrite out-of-scope files on your own initiative.
- Do not add secrets to source, logs, test fixtures or memory.
- Do not claim a command/test was run if it was not executed.
- If the environment lacks dependencies/access rights, do as much as possible and state clearly what could not be verified.
- If the requirements change significantly after work starts, update the scope and plan before continuing.

## Completion criteria
- The change meets the acceptance criteria, has appropriate tests/verification, the diff contains nothing out of scope, and limitations are stated clearly.
