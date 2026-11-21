# `.agents/` — source of truth

This directory holds the repository's workflow, rules, extension points, scripts, templates and long-term memory.

- `AGENTS.md`: the baseline working contract for the agent.
- `rules/`: engineering philosophy (The Zen of GitHub in `engineering-philosophy.md`), software development standard, memory policy, security safety, language and the reporting standard (`deliverables-and-reporting.md`); customize `project.md` per repository.
- `skills/`: capabilities per task type, registered with the agent in use.
- `mcp/`: MCP configuration and permission guidance.
- `tools/`: helper tools with deterministic behavior.
- `scripts/`: automation for global initialization (`init-global.sh`), project initialization (`init-project.sh`), health checks (`doctor.sh`), memory search (`search-memory.sh`), and the self-learning skill distillation toolset (`skill-distiller.py`, `promote-skill.py`).
- `template/`: reusable Markdown templates for each engineering phase.
- `memory/`: a knowledge base that can be searched and version-controlled.
- `outputs/`: storage for reports, artifacts and test results outside the worktree, per `~/.agents/outputs/<project>/`.

Do not assume a tool auto-discovers every directory. Register skills/MCP or configure an adapter for the instruction file using that agent's own mechanism.
