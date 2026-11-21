# Skills — task-scoped capabilities

A skill describes **how to carry out one kind of work**; a template describes **the output to produce**; a rule states **what is mandatory**. Do not mix these three roles, and do not load every skill for each task.

## Orchestration skill

- `software-lifecycle/SKILL.md` — classify the task, choose skills/templates, check quality gates.

## Software lifecycle map

| Phase/situation | Primary skill | Templates you may use |
|---|---|---|
| Clarify a feature | `requirements-discovery` | `feature-spec.md` |
| Design/API/data/architecture | `solution-design` | `technical-design.md`, `adr.md`, `implementation-plan.md` |
| Write or change code | `implementation` | `implementation-plan.md` when needed |
| Bug investigation | `bug-investigation` | `bug-investigation.md` |
| Refactor while preserving behavior | `refactoring` | `test-plan.md` when needed |
| Test and verify | `testing-validation` | `test-plan.md` |
| Review a diff | `code-review` | `code-review.md` |
| Auth, sensitive data, trust boundary | `security-review` | `security-review.md` |
| Release/deploy/migration | `release-deployment` | `release-checklist.md` |
| Incident affecting a live service | `incident-response` | `incident-postmortem.md` once stable |
| Find/update/distill memory | `memory-curation` | `memory-entry.md`, `memory-evaluation.md` |
| Self-learning, distill skills after a turn/task | `self-learning-loop` | `.agents/template/skill/SKILL.md` |
| Handoff or retrospective | `handoff-retrospective` | `handoff.md`, `retrospective.md` |

## Sample process chains

- **Bug:** `memory-curation` (search first) → `bug-investigation` → `testing-validation` → `code-review` → `memory-curation` (distill if useful).
- **Feature:** `memory-curation` (search first) → `requirements-discovery` → `solution-design` if needed → `implementation` → `testing-validation` → `security-review` if there is risk → `code-review` → `memory-curation`.
- **Refactor:** `memory-curation` (search first) → `refactoring` → `testing-validation` → `code-review`.
- **Release:** `release-deployment` → after an incident, `incident-response` → `handoff-retrospective`/`memory-curation` when there are lessons.

## Skill authoring conventions

- Each skill is a directory holding a `SKILL.md` with YAML frontmatter containing `name` and `description`; `name` must match the directory name and use kebab-case.
- Write the prose in English per `rules/language.md`; keep technical names and structured fields unchanged.
- Each skill states: when to use it, when not to use it, the process, the rules, the completion criteria and the related templates/references.
- Required headings, enforced by `scripts/validate-skills.sh`: `## When to use`, `## When not to use`, `## Rules`, `## Completion criteria`, plus one process section whose heading ends in "process" (for example `## Process` or `## Handoff process`). Extra domain sections are allowed in addition to these.
- Make triggers specific enough that an agent can select a skill from its description without loading the full content.
- Keep skills focused; long or deep content belongs in `references/` instead of bloating `SKILL.md`.

## Compatibility note

Having a `skills/` directory does not mean every coding agent will discover skills automatically. The agent must support the Agent Skills format and be configured with the right directory. Some tools require their own skills directory; in that case use a verified adapter or symlink, but keep `.agents/skills/` as the canonical source in this repository.
