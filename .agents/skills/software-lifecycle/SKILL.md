---
name: software-lifecycle
description: "Orchestrate the software development lifecycle from request classification through implementation, verification, review, release and memory distillation. Use when the user asks to build a feature, fix a bug, refactor, change architecture or complete a multi-step software task."
---
# Software development lifecycle orchestration

## When to use
- The task has many steps or may affect multiple components.
- You need to pick the right skill and template without loading the entire process unnecessarily.

## When not to use
- A purely explanatory question that requires no repository change.
- A tiny edit with an obvious process; still follow memory search, verification and appropriate diff review.

## Process
1. Read `.agents/AGENTS.md`, the applicable rules and `.agents/skills/README.md`.
2. Classify the size: **small** (local change, low risk), **medium** (multiple files or new behavior), **large/high risk** (architecture, auth, data, migration, security, production).
3. For significant technical tasks, search memory first per `.agents/rules/memory-policy.md`; search project first, global second. Verify entries against the current code and version.
4. Choose skills from the table in `.agents/skills/README.md`. Load only the relevant skills; you can chain several skills in work order.
5. Choose a matching template. Templates are sources for creating documents, not files to edit directly. If you produce a document, copy the template to the document location per repository conventions.
6. Make the change within scope; do not expand the requirements without a reason.
7. Run appropriate verification, review the diff, address important findings, then decide whether memory/handoff/release is needed.
8. Report the outcome clearly, the commands run, the checks not run, assumptions and remaining risks.

## Process selection rules
- Bug → `bug-investigation` → `testing-validation` → `code-review` → `memory-curation` if there are reusable lessons.
- Feature → `requirements-discovery` → `solution-design` when needed → `implementation` → `testing-validation` → `security-review` if there is risk surface → `code-review`.
- Refactor → `refactoring` → `testing-validation` → `code-review`.
- Release → `release-deployment`; when an incident is ongoing, prioritize `incident-response`.
- Unfinished task or session change → `handoff-retrospective`.

## Quality gates
- Do not move from requirements to implementation while the goal/acceptance criteria remain ambiguous in a way that could significantly change the solution.
- Do not consider a task done just because the code was edited; you need appropriate verification evidence or a stated limitation.
- Do not run destructive commands, production migrations or deployment actions with real impact without clear permission/authorization.
- Do not require a spec document for small edits; avoid formal processes that create no value.

## Output
- **Deliverable file (when using a template):** All detailed template content (plan, spec, review, audit, etc.) must be written to a Markdown file (`.md`) in the repo.
- **Chat report:** Only a short summary: what was done, verification evidence, main blockers/findings and the deliverable file path; do not paste the whole template content into chat.
