# `dotagents` — Workflow and memory framework for AI coding agents

The goal is to turn memory into a **knowledge base that can be searched, verified, updated and version-controlled**, instead of dumping everything automatically.

> ### ⚡ One-Prompt Setup
>
> Pick the prompt that fits your need and send it to your AI coding agent (Claude Code, Cursor, Windsurf, Roo-Code, Omp, Codex...):
>
> #### 🌐 Prompt 1: Global setup (run once per machine)
> Set up the `~/.agents/` framework as the shared baseline, skill set and global memory for every project:
>
> ````markdown
> Install the global `dotagents` framework on this machine:
>
> 1. Run the following bash snippet to download and install safely into ~/.agents:
> ```bash
> bash -euo pipefail -c '
>   TMP_DIR="$(mktemp -d)"
>   trap "rm -rf \"$TMP_DIR\"" EXIT
>   git clone --depth 1 https://github.com/truongnat/dotagents.git "$TMP_DIR"
>   "$TMP_DIR/.agents/scripts/init-global.sh"
>   chmod +x ~/.agents/scripts/*.sh ~/.agents/scripts/*.py
>   ~/.agents/scripts/doctor.sh
> '
> ```
> 2. Make sure your agent configuration reads `~/.agents/AGENTS.md` as Global Instructions.
> 3. Summarize the check results from doctor.sh.
> ````
>
> #### 📁 Prompt 2: Project setup (run inside each repository)
> Initialize a local `.agents/` structure and `AGENTS.md`, and detect the technical stack of the project:
>
> ````markdown
> Integrate the `dotagents` framework into the current repository:
>
> 1. Run the following bash snippet to download and install safely:
> ```bash
> bash -euo pipefail -c '
>   TMP_DIR="$(mktemp -d)"
>   trap "rm -rf \"$TMP_DIR\"" EXIT
>   git clone --depth 1 https://github.com/truongnat/dotagents.git "$TMP_DIR"
>   "$TMP_DIR/.agents/scripts/init-project.sh" .
>   chmod +x .agents/scripts/*.sh .agents/scripts/*.py
>   ./.agents/scripts/doctor.sh
> '
> ```
> 2. Open `.agents/rules/project.md` and, based on the current codebase (package.json, Cargo.toml, go.mod, README, etc.), fill in: technical stack, test/build/lint commands and the main business conventions.
> 3. Re-run `./.agents/scripts/doctor.sh` and summarize which files were integrated.
> ````
## 1. Design principles
1. **Single source of truth:** keep rules, skills, MCP config, tools, scripts, templates and memory in `.agents/`.
2. **Search before you work:** for any significant technical task, search project memory first and global memory second; read the matching entry and verify it still holds for the current code and dependencies.
3. **Store only knowledge with long-term value:** favor hard-to-spot root causes, resolved failures, architecture decisions, conditional workarounds, recurring errors and proven procedures.
4. **Evidence beats narrative:** memory states how to verify the claim, the applicable scope/version and the related sources.
5. **Start with Markdown + Git:** use `rg`/`grep` first. Add vector search, a database or a memory service only when a benchmark shows the current search is not enough.
6. **Never store secrets:** no tokens, passwords, private keys, personal data or logs containing sensitive information in memory.
7. **Consistent language:** prose defaults to English; technical identifiers and structured metadata stay in English. Detailed rules live in `.agents/rules/language.md`.
8. **Clear output boundary:** chat carries only a short summary (Executive Summary); every detailed report that follows a template must be written to a Markdown file (`.md`) under `~/.agents/outputs/<project>/reports/` per `rules/deliverables-and-reporting.md`, never dumped into the repository.
9. **Canonical engineering philosophy (The Zen of GitHub):** shape behavior and code quality on 14 core principles: practicality beats purity, anything added dilutes everything else, half measures are as bad as nothing at all, and design for failure. Details in `.agents/rules/engineering-philosophy.md`.

## 2. Structure

```text
~/.agents/                         # Global: how to work, reusable knowledge
├── AGENTS.md
├── skills/
├── rules/
├── mcp/
├── tools/
├── scripts/
├── template/
├── outputs/                       # Standard report storage outside the worktree
│   └── <project>/
│       ├── reports/               # Review, audit, bug investigation, postmortem reports
│       ├── artifacts/             # Screenshots, PDF, Excel test matrix
│       ├── testresults/           # Test logs, benchmarks, traces
│       └── notes/                 # Temporary technical notes for a session
└── memory/
    ├── INDEX.md
    ├── entries/{bugfixes,decisions,patterns,workflows,environment}/
    └── archive/YYYY/

<repo>/
├── AGENTS.md                      # Entry point where the agent reads the standards
└── .agents/                       # Project-specific rules, templates, memory, tools
    ├── AGENTS.md
    ├── rules/project.md
    └── memory/...
```

In this template set, custom configuration lives under `.agents/`; the root `AGENTS.md` is the **entry point/adapter** that lets the agent discover and read those instructions.

### Global vs project split

- **Global:** shared ways of working, patterns reused across repositories, universal pitfalls.
- **Project:** repository architecture, business conventions, local decisions, bugfixes tied to specific code or dependencies, project-specific test/build/deploy commands.
- Never promote project memory to global automatically. Promote only after removing internal details and confirming the knowledge is reusable.
- Project-specific rules take precedence inside the project, but never override security requirements or higher-priority instructions.

## 3. Installation

### Global

1. Run the global installer: `./.agents/scripts/init-global.sh` (installs into `~/.agents/` by default and does not overwrite existing files unless you pass `--force`).
2. Configure your agent to read `~/.agents/AGENTS.md` using that tool's own global instruction mechanism. **Not every agent reads `~/.agents/` automatically**; `.agents/` is a storage convention, not an auto-loading mechanism shared by all tools.
3. Run `~/.agents/scripts/doctor.sh` to check system health.

### Per project

1. Run the initializer: `./.agents/scripts/init-project.sh <repository-directory>`.
2. Fill in `.agents/rules/project.md`: stack, verification commands, architecture and local constraints.
3. Run `./.agents/scripts/doctor.sh` to check.
4. Run `git status` to confirm you only commit the right files. Never put credentials or sensitive data in the repository.

### Integrating other tools

If your tool does not read `AGENTS.md`, use that tool's own instruction/config file as a short adapter pointing at the same `.agents/` source. Avoid maintaining several independent rule sets. Use symlinks only when the tool and operating system support them reliably.

## 4. How skills and templates work together

The framework ships lifecycle skills: requirements discovery, solution design, implementation, bug investigation, testing, code review, security review, release/deployment, incident response, refactoring, memory curation, self-learning skill distillation (`self-learning-loop`) and handoff/retrospective. See `.agents/skills/README.md` to pick a skill per task.

- **Skill** describes the process, triggers and completion criteria.
- **Template** defines the document/output format for when you actually need one.
- **Rule** states constraints that apply across the board.
- **Self-learning loop:** after each round that fixes a mistake or solves a new problem, the agent extracts the lesson, checks for duplicates and creates a skill draft via `skill-distiller.py` and `promote-skill.py`.

Never load every skill at once. Pick the relevant one; small tasks use the short path, large or high-risk tasks go through the full verification gates. Skills are auto-discovered only when the agent supports them and the directory is configured correctly; dropping files into `.agents/skills/` does not guarantee that every tool has loaded them.

## 5. Standard workflow

```text
Classify the task
  → Search memory (project → global)
  → Read the matching entry and verify it is still current
  → Investigate / design / implement
  → Run the relevant verification
  → Update memory or distill a new skill via self-learning-loop
  → Review the diff, check memory state and hand off
```

Details live in `.agents/AGENTS.md`, `.agents/rules/memory-policy.md` and `.agents/rules/software-development.md`.

## 6. Measure effectiveness, do not judge by feel

Build a small benchmark of 10–20 questions/tasks you have actually faced, and decide up front which entry should have been found. Measure:

- **Recall@5:** share of cases where the right memory appears in the first 5 results.
- **Precision@5:** share of results in the top 5 that were genuinely useful.
- **Adoption rate:** share of relevant tasks where the agent applied the right memory.
- **Stale-memory rate:** share of retrieved memories that are outdated or contradicted by current evidence.
- **Outcomes:** investigation time, success rate and recurrence of the same failure.

Record results with `.agents/template/software/memory-evaluation.md`. Upgrade the search engine only when the data shows `rg` + taxonomy + metadata is not enough.
