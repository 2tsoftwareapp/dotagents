---
name: requirements-discovery
description: "Clarify the problem, affected users, scope, constraints and acceptance criteria before implementing a feature or behavior change. Use when the request is unclear, for a new feature, or for a change that affects business logic."
---
# Requirements discovery

## When to use
- A new feature, a business-behavior change, or a request with multiple possible interpretations.
- You need to confirm scope, exceptions, input/output data or acceptance criteria.

## When not to use
- Fixing a clearly reproduced defect with a specific fix request → `bug-investigation`.
- A very small, low-risk technical task that does not change user-facing behavior.

## Process
1. Read the original request and search related memory before settling on a direction.
2. Check the current behavior in code, UI, API, documentation and tests where available.
3. Establish: the problem to solve, user groups/actors, main flows, states, data, business rules, exceptions, and out-of-scope items.
4. Write acceptance criteria as testable behavior; prefer Given/When/Then where suitable.
5. Record assumptions and open questions. Ask the user only when the answer could significantly change the design, scope or risk; otherwise state assumptions explicitly.
6. Use `.agents/template/software/feature-spec.md` if the feature is large enough to need a reviewable spec.
7. Move to `solution-design` when architecture decisions are needed or many components are affected.

## Rules
- Distinguish confirmed requirements from assumptions.
- Do not turn a solution suggested by the user into a mandatory requirement when the actual goal is still unclear.
- Cover error states, loading/empty states, authorization and retry/reload capability where relevant.
- Do not write a spec longer than needed to implement and test.

## Completion criteria
- There is a clear goal, in-scope/out-of-scope, acceptance criteria and key constraints.
- Remaining unknowns are stated explicitly, or the necessary questions have been asked.

## Related templates
`.agents/template/software/feature-spec.md`
