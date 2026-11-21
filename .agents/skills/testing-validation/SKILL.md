---
name: testing-validation
description: "Choose and run appropriate tests for a software change; confirm acceptance criteria, regression, typecheck, lint and build with real evidence. Use before concluding a task is complete."
---
# Testing and verification

## When to use
- After implementing or fixing a bug; when you need to design a test strategy or verify a change.

## When not to use
- Explaining a concept that is not tied to code.
- An incident still needs stabilizing first; follow `incident-response`, then verify under control.

## Process
1. Read existing tests, package/config scripts and project conventions; do not guess commands.
2. Match tests to acceptance criteria and risks. Cover happy path, boundaries, negative paths, error states and regression across the affected surface.
3. For small changes, run targeted tests first. For broad changes, extend to integration, typecheck, lint and build as appropriate.
4. For API/UI, verify contracts and state mapping; for async flows, consider retry, duplicate events, timeouts and post-reload state where relevant.
5. If a test fails, determine whether the change or the environment caused it; return to `bug-investigation` if the cause is unclear.
6. Record the exact command, pass/fail, skipped tests and reasons. Do not infer a successful build from passing unit tests.
7. Use `test-plan.md` when scope/risk calls for a reviewable test plan.

## Rules
- Do not weaken tests or delete assertions just to make the pipeline green without justification.
- Do not ignore failing tests without reporting them.
- Do not use a single snapshot in place of important business assertions.
- If tests cannot be run, do the static inspection you can and state clearly which risks remain unverified.

## Completion criteria
- The appropriate checks have run and results are recorded accurately; anything that could not be checked has a clear reason/impact.

## Related templates
`.agents/template/software/test-plan.md`
