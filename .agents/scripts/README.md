# Helper scripts

Operational and integrity-check tooling for the dotagents framework:

### 1. Health checks & validation
- `doctor.sh` — Full system check: core directories, executable permissions, skill validity, memory schema, and unit tests.
- `validate-skills.sh` — Basic check of YAML frontmatter, kebab-case, and that `name` matches the skill directory name.
- `validate-memory.py` — Validate memory entries against the 15 required frontmatter fields, valid enum values (`type`, `scope`, `status`, `confidence`), and ISO date format per `memory-policy.md`.
- `test-validate-memory.py` — Unit tests for `validate-memory.py`.
- `test-init-project.sh` — Integration test for `init-project.sh`.
- `test-init-global.sh` — Integration test for `init-global.sh`.

### 2. Memory search
- `search-memory.sh` (or `search-memory.py`) — Search knowledge in project → global order:
  - Supports smart-case and ripgrep (falls back to the Python search when `rg` is not installed).
  - Supports the `--archive` flag to search the legacy archive.
  - Supports metadata filters: `--type`, `--status`, `--confidence`, `--tag`.
  - Supports the `--summary` flag to print quick summary cards.

### 3. Self-learning & skill distillation
- `skill-distiller.py` — Analyze lessons, check for duplicates (Jaccard similarity), and generate a standardized `SKILL.md` draft in the staging directory (`.agents/skills/.staging/`).
- `promote-skill.py` — Check completeness and syntax, then move a skill draft from staging to the official skills directory (project or global).
- `test-skill-distiller.py` — Automated unit tests for extraction, duplicate detection, and skill promotion.

### 4. Init & install
- `init-global.sh [--force] [target-dir]` — Initialize the global dotagents structure (Global Framework) for the user in `~/.agents/` (or the given target directory); safe by default and never overwrites unless `--force` is passed.
- `init-project.sh [--force] <target-dir>` — Safely initialize the `.agents/` structure and `AGENTS.md` into a target repository (by default it does not overwrite customized files such as `project.md` or `AGENTS.md` unless the `--force` flag is passed).
