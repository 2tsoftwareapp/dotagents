# Global development standard: the SPARC methodology (sparc-coder)

Every agent and session follows **SPARC** (Specification, Pseudocode, Architecture, Refinement, Completion) by default, along with the engineering philosophy in `rules/engineering-philosophy.md`, the language standard in `rules/language.md` and the quality control process below.

| Phase | Meaning |
|-------|---------|
| **S** | Goals, scope, acceptance criteria, edge cases (`requirements.md`, or a short summary for small fixes) |
| **P** | Sketch the logic/branches before writing complex code |
| **A** | Repo patterns, architectural boundaries, risks (`context.md` when needed) |
| **R** | TDD-first, minimal diff, error handling |
| **C** | Verification with evidence — PASS / FAIL / BLOCKED / NOT VERIFIED |

**Depth (decide yourself, do not print it in chat):** small fix → inline S/C; medium feature → a trimmed file gate; large feature / new business area → full gate + `sdlc-*` fleet (section 10). Do not ask the user "which process" when the task already implies it. Depth never waives the approval gate in section 0.

**Knowledge sources (in order):** requirements + attached files → SPARC artifacts in the repo → project rules → repo/project memory (`scripts/search-memory.sh`, see section 1) → ai-memory (`memory_query` → `memory_read_page`) → technical knowledge and codebase via XERJ (`xerj_search` / `xerj_def` / `xerj_code_search`) → domain MCP when a ticket/MR is needed → ask the user.

---

## 0. Execution gate — todo checklist and approval (mandatory)

Every task that **changes state** (code, config, files, data, external systems) must pass this gate before execution:

1. **Write the todo checklist** right after analyzing the request, before touching anything: each item is one verifiable action, in order, with in-scope / out-of-scope stated. Small fix: a 2–3 line checklist.
2. **Present the checklist and stop for user approval.** Do not start changing anything before it is approved.
3. When the user requests changes → **update the checklist → present the changed part for approval again**, then execute.
4. While executing, tick each item against **real evidence**; if a blocker appears or the scope has to move beyond the checklist → stop and ask for additional approval; never widen the scope on your own.
5. Handoff: report per-item status against the checklist (`PASS / FAIL / BLOCKED / NOT VERIFIED`) with the commands you ran and the ones you did not run.
6. **Gate exemptions:** lookup questions, explanations and pure information reads that change no state.
7. `sdlc-*` fleet: background agents never stop to ask the user; the **parent** owns the checklist approval and delegates only approved scope (including the checklist in the brief).
8. This gate is a standing delegation from the user and is not one of the "pointless manual approval processes" banned by `rules/engineering-philosophy.md`.

## 1. Requirement analysis

- Read the request closely; establish the goal, expected behavior and change scope.
- Check specs, documents, business rules and the current code.
- Trace the business flow end-to-end when the change touches it; not just a single module.
- Analyze dependencies, side effects and backward compatibility.
- Identify ambiguities and contradictions; prefer verifying them from the project yourself.
- Do not implement while an open point can still change the outcome.
- **Search memory before proposing a solution** (significant technical tasks): summarize the problem into keywords; run `scripts/search-memory.sh "<keywords>"` — **project/repo memory first, global second**; if the script is missing, run `rg -n -i "<term>" .agents/memory "$HOME/.agents/memory"` and skip `archive/` on the first pass. Read every matching entry in full (prefer `status: active`) and check it against the current code and version. Never fabricate results or claim you searched when you did not.

## 2. Build the requirement checklist

- `requirements.md` for a feature or significant change (small fix: bullets in the reply are enough).
- REQ-xx checkboxes, in/out scope, verifiable acceptance criteria.
- The requirement checklist is **part of the todo checklist presented in section 0**; move on to architecture and planning only after the user approves.

## 3. Build the context checklist

- Trace code, data flow and existing patterns; `context.md` for a new subsystem or high risk.
- Reuse repo patterns; record technical decisions briefly.
- Approve before plan/implement when using the full gate.
- For large codebase lookups or AST definitions, prefer `xerj_def` / `xerj_search` to get exact `file:line` and symbols instead of flooding context with raw `grep`.

## 4. Definition of Done (DoD)

- `dod.md`: concrete verification commands (test, lint, build), regressions, UI when relevant.
- Do not add requirements outside scope.

## 5. Task checklist

- `tasks.md`: TASK-xx, linked REQ, ordering, status checkboxes.
- Every task carries a DoD; no "do everything" task.
- Present the task list through the section 0 gate before implementing; run only the approved tasks.

## 6. Implementation

- Follow the todo checklist approved in section 0 and `tasks.md`; use pseudocode for complex logic.
- Read `~/.agents/skills/karpathy-guidelines/SKILL.md` before editing code.
- TDD-first when the repo has tests; minimal diff; no refactoring outside scope.
- Mark a task **completed** only with evidence (tests run).
- Wiki notes: `ai-memory-durable-pages` skill plus an explicit user request — never call `memory_write_page` on your own.
- Reference coding: when facing an unfamiliar library/API or hitting the same error twice, use `xerj-code` (`xerj_code_search`) to look up the canonical solution from the reference repository corpus before writing code.
- Blocker or scope change → stop, return to the section 0 gate for additional approval, inform the user.

## 7. Verification & self-review

- Check against requirements + DoD; run the real commands.
- PASS / FAIL / BLOCKED / NOT VERIFIED — never PASS without verification.
- Summary: changed, verified, risks (bullets).

## 8. Commit & delivery

- No commit/push/MR unless the user asks.
- Commit messages follow the repo convention.

## 9. Optimization rules

- Small fix: a trimmed 2–3 line checklist per section 0, still needs approval, still needs verification.
- Large feature: full gate + approval.
- Do not re-ask for information you already have; no long abstract documents.
- Do not read the whole repo; expand along dependencies.
- No scope creep; correctness and maintainability beat speed.

---

## 10. Fleet, skills & MCP (when delegating or on large tasks)

| Role | Agent `~/.agents/agents/…` | Output |
|---------|------------------------------|--------|
| Spec | `sdlc-requirements-analyst` | `requirements.md` |
| Context | `sdlc-context-architect` | `context.md` |
| Plan | `sdlc-planner` | `tasks.md`, `dod.md` |
| Code | `sdlc-implementer` | code, tests |
| Verify | `sdlc-verifier` | vs `dod.md` |
| Review / ship / debug / security | `sdlc-code-reviewer`, `sdlc-ship-readiness`, `sdlc-debugger`, `sdlc-security-auditor` | per `AGENT.md` |

Playbook: `~/.agents/agents/_shared/SKILLS-MCP.md`. Meta-skill: `using-agent-skills`. Implementation: `test-driven-development` + `karpathy-guidelines`. MCP: read memory and tickets first; verification means local/CI commands and is never replaced by MCP.

**Picking a skill:** read `skills/README.md` to classify the task and choose the relevant skill; load only the chosen `SKILL.md`, not the whole set. Skills explain how to work; templates standardize output; rules define mandatory requirements.

---

## 11. Reporting and review — deliverable files

- Any review, audit, analysis or synthesis request whose output is a report **must produce a file**, even when there are no findings. A chat reply alone does not replace the deliverable. Quick questions and ordinary discussion need no file.
- Layout, file naming, storage location, evidence rules, verification evidence and the chat handoff format are defined once in `rules/deliverables-and-reporting.md`. Follow that file; do not restate the rules here, so the two cannot drift apart.
