#!/usr/bin/env python3
"""Promote Skill: Validate and move a skill draft from staging to production.

Part of the dotagents Self-Learning Skill Loop system.
Supports:
- Check completeness and standards compliance of the `SKILL.md` draft.
- Run the linter against the `.agents/AGENTS.md` standard.
- Move the skill directory from `.agents/skills/.staging/<name>` to `.agents/skills/<name>`
  (or `~/.agents/skills/<name>` when --global is passed).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def parse_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        return {}
    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return {}
    fm_raw = parts[1]
    fields: dict[str, str] = {}
    for line in fm_raw.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            raw_val = m.group(2).strip().strip("\"'")
            fields[key] = raw_val
    return fields


def validate_draft_skill(skill_dir: Path) -> list[str]:
    """Validate the content and structure of a skill draft."""
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"SKILL.md not found in directory {skill_dir}"]

    content = skill_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)

    name = fm.get("name", "")
    desc = fm.get("description", "")
    dir_name = skill_dir.name

    if not name:
        errors.append("Missing 'name' field in YAML frontmatter")
    elif name != dir_name:
        errors.append(f"Skill name '{name}' does not match directory name '{dir_name}'")

    if not desc:
        errors.append("Missing 'description' field in YAML frontmatter")

    if re.search(r"[^a-z0-9-]", name) or name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append(f"Name '{name}' is not valid kebab-case")

    required_sections = [
        "## When to use",
        "## When not to use",
        "## Process",
        "## Rules",
        "## Completion criteria"
    ]
    for sec in required_sections:
        if sec not in content:
            errors.append(f"Missing required section: '{sec}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote a draft skill into the official skills directory")
    parser.add_argument("name", help="Name of the skill to promote (e.g. my-new-skill)")
    parser.add_argument("--staging-dir", default=".agents/skills/.staging", help="Staging directory (default: .agents/skills/.staging)")
    parser.add_argument("--skills-dir", default=".agents/skills", help="Target skills directory (default: .agents/skills)")
    parser.add_argument("--global", dest="is_global", action="store_true", help="Promote into ~/.agents/skills/ instead of the current project")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite if the skill already exists at the destination")
    parser.add_argument("--dry-run", action="store_true", help="Only validate without moving any files")

    args = parser.parse_args()

    name = args.name.strip()
    staging_dir = Path(args.staging_dir)
    source_dir = staging_dir / name

    if not source_dir.exists():
        print(f"Error: draft skill not found at: {source_dir.resolve()}", file=sys.stderr)
        return 1

    # 1. Validate the draft skill
    errors = validate_draft_skill(source_dir)
    if errors:
        print(f"[FAILED] Draft skill '{name}' does not meet the standards:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 2

    # 2. Resolve the target directory
    if args.is_global:
        target_base = Path.home() / ".agents" / "skills"
    else:
        target_base = Path(args.skills_dir)

    target_dir = target_base / name

    if target_dir.exists() and not args.overwrite:
        print(f"Error: skill '{name}' already exists at the destination: {target_dir.resolve()}", file=sys.stderr)
        print("Use the --overwrite flag to replace the old version.", file=sys.stderr)
        return 3

    if args.dry_run:
        print(f"[DRY-RUN OK] Draft skill '{name}' is valid.")
        print(f"  Source: {source_dir.resolve()}")
        print(f"  Planned destination: {target_dir.resolve()}")
        return 0

    # 3. Perform the promotion
    target_base.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(source_dir, target_dir)
    shutil.rmtree(source_dir)

    print(f"[PROMOTED] Moved skill '{name}' to: {target_dir.resolve()}")

    # 4. Re-validate with validate-skills.sh when inside the repo scope
    validate_script = Path(".agents/scripts/validate-skills.sh")
    if not args.is_global and validate_script.exists():
        res = subprocess.run([str(validate_script), str(target_base)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[WARNING] validate-skills.sh reported issues:\n{res.stdout}\n{res.stderr}")
        else:
            print(f"[VALIDATION COMPLETE] {res.stdout.strip()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
