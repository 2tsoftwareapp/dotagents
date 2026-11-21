# Software development templates

Choose a template by risk level and work stage; do not treat these as mandatory paperwork for every change. The matching skills live in `.agents/skills/` and describe how to create/verify the output.

| Template | Suggested skill | Use when |
|---|---|---|
| `feature-spec.md` | `requirements-discovery` | Clarify the problem, scope, and acceptance criteria |
| `implementation-plan.md` | `solution-design`, `implementation` | The change needs to be split into steps and verified |
| `technical-design.md` | `solution-design` | Designing multiple components or data flows |
| `test-plan.md` | `testing-validation` | Risks/test cases need review first |
| `bug-investigation.md` | `bug-investigation` | Reproduce, hypothesize, find root cause, and fix |
| `code-review.md` | `code-review` | Record a review with many findings |
| `security-review.md` | `security-review` | Changes to auth, sensitive data, or trust boundaries |
| `release-checklist.md` | `release-deployment` | Prepare rollout, smoke test, rollback |
| `adr.md` | `solution-design` | Architecture decisions with long-term impact |
| `incident-postmortem.md` | `incident-response` | Summarize after an incident is stabilized |
| `handoff.md` | `handoff-retrospective` | Switch session/agent or hand off a task |
| `retrospective.md` | `handoff-retrospective` | Capture lessons with concrete action items |
| `memory-evaluation.md` | `memory-curation` | Measure memory retrieval/usage effectiveness |

Templates in `.agents/template/` are the source of truth. When initializing a document for a task, follow the storage standard in `../../rules/deliverables-and-reporting.md`:
- Long-lived project documents (ADR, feature-spec): store in the repo (`docs/adr/`, `docs/specs/`).
- Review, audit, bug investigation, and handoff reports: by default store at `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<type>-<topic>-<rev>.md`. Do not create junk files at the project root.

> **Chat vs. File separation:** All detailed content per template must be written to a **Markdown file (`.md`)**. Do not paste the template verbatim into chat; chat only carries a brief conclusion, key blockers, and the path of the file created.
