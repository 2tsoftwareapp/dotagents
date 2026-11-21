# Software development process

Match the process to the risk and honor the core principles in `rules/engineering-philosophy.md`: practicality beats purity, half measures are as bad as nothing at all, design for failure, and anything added dilutes everything else.

## Phase 1 — Understand the problem

- Summarize the problem and the expected outcome.
- Search existing memory, code and documentation before proposing a solution.
- Identify users/actors, current behavior, desired behavior, constraints and acceptance criteria.
- Flag what is unknown; never invent business rules.

## Phase 2 — Plan

- Check the affected modules, contracts, data flows, tests, migrations and consumers.
- Choose the smallest consistent implementation; prefer the practical option and reuse existing repo patterns (*Practicality beats purity*).
- Avoid over-engineering: no new abstraction, helper or wrapper without a real need (*Anything added dilutes everything else*).
- Split high-risk work into reviewable steps; list the files and modules you expect to change.
- Design for failure: consider compatibility, permissions, error paths, observability, rollback and operational impact.

## Phase 3 — Design when needed

- Record API/schema/event changes and responsibility boundaries.
- State the important alternatives and why the final one won.
- Use an ADR for decisions with long-term architectural impact.
- Link the design to source files and acceptance criteria.

## Phase 4 — Implement

- Follow the project's existing patterns, unless that pattern is the confirmed cause of the defect.
- Keep the change scope clear; avoid unrelated refactoring (minimal diff).
- Clean cutover: migrate every caller, remove dead code and temporary shims, leave no unfinished `TODO: implement` (*Half measures are as bad as nothing at all*).
- Add or update tests together with the behavior change.
- For data changes, define migration, compatibility, backfill and rollback where applicable.

## Phase 5 — Verify

- Run the most relevant automated checks: unit, integration, e2e, lint, type check, build, migration checks or a reproducible manual scenario.
- Check acceptance criteria and the important error and edge paths, not just the happy path (*Design for failure*).
- Performance is a required feature: a feature is done only when it runs fast, does not leak memory and does not create N+1 queries (*It’s not fully shipped until it’s fast*).
- Report the commands and results, the checks you skipped, the assumptions and the remaining risks.

## Phase 6 — Review and release

- Review the diff for correctness, regression risk, security, logging, compatibility and accidentally added secrets.
- Update documentation, config, migrations and release notes when needed.
- For high-risk deployment changes, state the rollout, the health signals and the rollback conditions.

## Phase 7 — Capture and hand off

- Create or update durable memory in `memory/entries/` when it meets the memory policy.
- Update or supersede old entries to avoid fragmenting knowledge.
- Hand off briefly: what behavior changed, the affected areas and files, the verification results, the limits and the memory you updated.

## Choosing the minimum template

| Work type | Suggested template |
|---|---|
| Small bug | Bug investigation + related tests; memory if there is a reusable lesson |
| Feature | Feature spec + implementation plan + test plan |
| Refactor touching many components | Implementation plan + technical design + test plan |
| Architecture decision | ADR, plus a technical design if needed |
| High-risk release or migration | Implementation plan + test plan + release checklist |
| Production incident | Postmortem after mitigation and stabilization |
| End of session with work unfinished | Handoff |

## Output convention: short chat vs deliverable file (template)

Keep the two output channels strictly separate so the conversation context stays clean:

1. **Deliverable file channel (mandatory when a template is used):**
   - Every report or document based on a template (`feature-spec.md`, `technical-design.md`, `implementation-plan.md`, `test-plan.md`, `bug-investigation.md`, `code-review.md`, `security-review.md`, `release-checklist.md`, `adr.md`, `incident-postmortem.md`, `handoff.md`, `retrospective.md`) **must be written to a Markdown file (`.md`)**.
   - **Standard storage location per `rules/deliverables-and-reporting.md`:**
     - Long-lived project documents: inside the repo (`docs/adr/`, `docs/specs/`, `.agents/memory/entries/`).
     - Review, audit, bug investigation, postmortem and handoff reports: by default outside the worktree at `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<type>-<topic>-<rev>.md` so `git status` stays clean (unless the project defines its own directory in `project.md`). Never scatter junk files into the repository root (`./report.md`, `./review.md`).
   - The deliverable file holds the full detail: template sections, tables, findings with `F-xx` IDs, code file paths plus line numbers, the commands that were run and the relevant logs.
2. **Chat channel (summary only):**
   - The chat message is the Executive Summary for the user.
   - Chat content contains only:
     - The main results in 3–5 bullets.
     - The most important blockers, risks or findings, if any.
     - The **full path** to the deliverable file so the user can check the detail.
   - **Never** copy and paste the whole report or print an entire long template skeleton into the chat window.
