---
name: refactoring
description: "Restructure code to improve clarity, reduce coupling or improve maintainability without intentionally changing external behavior. Use when the user asks for a refactor, cleanup or technical-debt reduction."
---
# Safe refactoring

## When to use
- Splitting modules, improving abstractions, removing duplication, restructuring code or reducing technical debt.

## When not to use
- Changing business behavior is the main goal → `requirements-discovery` and `implementation`.
- The cause of the defect is not understood → `bug-investigation`.

## Process
1. Search existing memory, conventions and tests; define the behavior that must stay the same.
2. Identify the specific structural problem to improve and how you will judge the result.
3. Run suitable baseline tests/benchmarks before changing anything when possible.
4. Split the refactor into small steps, each reviewable and verifiable.
5. Preserve the public contract, error semantics, ordering, persistence behavior and side effects unless a change is explicitly required.
6. Avoid combining a broad refactor with feature changes, which makes regressions hard to distinguish.
7. Run `testing-validation`, review the diff and compare behavior before/after.
8. Write an ADR or memory only when the choice/pattern has long-term value.

## Rules
- “Cleaner code” is not enough if it increases complexity or adds unnecessary abstraction.
- Do not delete tests just because a new implementation makes old tests fail; determine whether the test protects behavior or implementation details.
- If a behavior change turns out to be necessary, split it into an explicit decision/commit/work item.

## Completion criteria
- The structure is improved per the stated goal, behavior is preserved through verification and the diff does not mix in out-of-scope changes.
