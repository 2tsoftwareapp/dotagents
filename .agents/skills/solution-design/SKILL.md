---
name: solution-design
description: "Design the technical solution, data flow, API contract, schema changes, trade-offs and architecture decisions before implementation. Use for multi-component features, architecture changes, integrations or risky migrations."
---
# Solution design

## When to use
- Changes across multiple modules/services or across the boundaries between FE, API and data.
- Adding dependencies, changing the data model, API contract, auth flow, async flow or architecture.
- Several options with significant trade-offs.

## When not to use
- A local fix or an obvious change that needs no architecture choice.

## Process
1. Read existing memory/ADR and verify the related decisions still hold.
2. Survey the architecture, patterns and contracts in use; avoid designing from file names without reading the code.
3. Identify components, request/event flows, data sources, states, errors, timeout/retry, idempotency and trust boundaries where relevant.
4. Compare at least the reasonable options, selection criteria and trade-offs. Do not create a token comparison table when only one option is realistic.
5. Use `technical-design.md` for designs affecting many components. Use `adr.md` when a decision has long-term value or is hard to reverse.
6. Use `implementation-plan.md` when you need to split the work into ordered steps with dependencies and verification criteria.
7. Define the test, rollout, migration and rollback strategy matching the risk.
8. Continue to implementation once the key decisions are clear; small tasks do not need to wait for a formal document.

## Rules
- Follow existing conventions and dependencies unless there is evidence a change is needed.
- Every proposed contract change must identify its consumers and backward compatibility.
- For data, distinguish schema, existing data, backfill and application behavior during the transition period.
- Do not add technology/dependencies just to solve a small problem.

## Completion criteria
- The main flow, failure modes, risks, decisions and verification approach are clear enough to implement.
- Every necessary ADR has been recorded, or the reason for not creating one is stated.

## Related templates
- `.agents/template/software/technical-design.md`
- `.agents/template/software/adr.md`
- `.agents/template/software/implementation-plan.md`
