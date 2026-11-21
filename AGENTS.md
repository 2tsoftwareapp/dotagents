# Repository agent instruction entry point

Before doing significant technical work:

1. Read `~/.agents/AGENTS.md` if the file exists and is reachable; it is the user's global working standard.
2. Read `.agents/AGENTS.md` and the applicable files in `.agents/rules/`.
3. Read `.agents/rules/project.md` for this repository's architecture, verification commands and local constraints.
4. Read `.agents/skills/README.md` to pick the right skill; load only the relevant `SKILL.md` instead of the whole skill library.
5. When working in a nested directory, follow the nearest `AGENTS.md` while staying consistent with the instructions above.

The `.agents/` directory is the source of truth for this repository's workflow, templates, scripts and custom memory. Do not create a second, independent rule set detached from this source.
