# Report publishing and deliverable management standard

Every analysis, review, audit, bug investigation, planning or handoff task must follow the storage structure and publishing conventions below. Never create loose report files of unclear origin inside the repository.

---

## 1. Document classification: in-tree vs out-of-tree

Not every document the agent produces belongs in the Git repository. Draw the line clearly:

| Group | Document types | Storage location | Git management |
|---|---|---|---|
| **In-tree (project documents)** | ADRs, business specs (`feature-spec`), long-lived architecture documents, project memory | `docs/adr/`, `docs/specs/`, `.agents/memory/entries/` | Committed with the code in the PR/MR |
| **Out-of-tree (reports & artifacts)** | Diff/PR review reports, security audits, bug investigations, test evidence, machine run logs, session handoffs | `~/.agents/outputs/<project-name>/` | **Never committed to git** (unless the project defines its own report directory) |

---

## 2. Standard storage structure for reports (out-of-tree)

When you produce a report, assessment or artifact that is not a long-lived source document, the default location is:
`~/.agents/outputs/<project-name>/` (or a dedicated directory defined in `project.md`).

```text
~/.agents/outputs/<project-name>/
├── reports/         # Every Markdown report (code review, security audit, bug investigation, postmortem)
├── artifacts/       # Binary evidence (UI screenshots, PDF, Excel matrix, exported files)
├── testresults/     # Test logs, benchmarks, automated test output, execution traces
└── notes/           # Scratch technical notes, temporary data analysis for the session
```

> **Safety rule:** never dump temporary report files, screenshots or Excel test files into the repository root (`./report.md`, `./review.md`, `./evidence.png`). It dirties `git status`, risks committing junk into git history and causes merge conflicts between branches.

---

## 3. Report file naming convention

Report file names must follow this identifying structure:

```text
YYYY-MM-DD-<report-type>-<topic>-<revision/task-id>.md
```

Where:
- `YYYY-MM-DD`: report date in ISO form (for example `2026-10-26`).
- `<report-type>`: the work type, matching the template:
  - `code-review` (source, PR or MR review)
  - `security-review` (safety and security assessment)
  - `bug-investigation` (root cause analysis of a defect)
  - `feature-spec` (feature specification)
  - `test-plan` (test plan)
  - `release-checklist` (release checklist)
  - `incident-postmortem` (incident summary)
  - `handoff` (work handoff between sessions or agents)
- `<topic>`: a short name describing the feature or scope (kebab-case, for example `auth-jwt-refresh`, `export-excel-boundary`).
- `<revision/task-id>`: the PR/MR number, revision or ticket ID (for example `mr381`, `pr12-rev1`, `issue240`).

### Valid examples:
- `~/.agents/outputs/my-app/reports/2026-10-26-code-review-mr381-rev01.md`
- `~/.agents/outputs/my-app/reports/2026-10-26-bug-investigation-token-refresh-loop.md`
- `~/.agents/outputs/my-app/artifacts/2026-10-26-ui-test-evidence-login.png`

### Forbidden names:
- `report.md`, `review.md`, `output.md`, `test.md`, `result.md`, `final.md` (easily overwritten, meaningless when looking back through history).

---

## 4. Content standards for a report (deliverable)

Every Markdown report you publish must meet these standards:

1. **Metadata header:** at the top of the file:
   - Creation date, project name, report target (MR/PR/branch/commit).
   - Author (agent / reviewer).
2. **Executive Summary (conclusion first):**
   - Put the main conclusion at the top of the file: `PASS`, `FAIL`, `BLOCKED` or `APPROVED / REQUEST_CHANGES`.
   - Summarize impact and risk in one table or a short paragraph, so the reader gets the point without reading the whole file.
3. **Findings traceability:**
   - Every defect or finding carries an ID: `F-01`, `F-02`...
   - Severity: `Critical`, `High`, `Medium`, `Low`, `Suggestion`.
   - **Exact file path with line numbers:** `src/auth/token.ts:45-52` (never abbreviated as `.../token.ts`).
   - Actual evidence: the failing snippet, the runtime log, the real test output (no speculation).
4. **Verification evidence:**
   - State the commands actually run, the test environment and the verification result.
   - Clearly separate checks that RAN (verified) from checks that are PROPOSED (not run).

---

## 5. Chat communication convention

After the deliverable file is written successfully, the agent's chat message must follow these rules:

- **Short and tight (Executive Summary):**
  - Summarize the conclusion and the main behavior in 3–5 bullet points.
  - Lead with blockers or serious risks, if any.
  - **Give the full path** to the report file so the user can open it:
    ```markdown
    📄 **Detailed report:** `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<topic>-<rev>.md`
    ```
- **Never:**
  - Paste the whole report file into chat.
  - Paste test logs hundreds of lines long into chat (write them to `testresults/` or the matching artifact file instead).
  - Reprint the entire template table skeleton into chat.
