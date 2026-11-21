#!/usr/bin/env python3
"""Promote Skill: Validate and move a skill draft from staging to production.

Part of the dotagents Self-Learning Skill Loop system.
Supports:
- Check completeness and standards compliance of the `SKILL.md` draft.
- Validate the draft with `validate-skills.sh`, the single source of the skill format contract.
- Move the skill directory from `.agents/skills/.staging/<name>` to `.agents/skills/<name>`
  (or `~/.agents/skills/<name>` when --global is passed).
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def validate_draft_skill(skill_dir: Path) -> list[str]:
    """Validate a skill draft against the shared skill format contract.

    The contract lives in validate-skills.sh so that promotion and the linter
    can never disagree about what a valid skill looks like.
    """
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"SKILL.md not found in directory {skill_dir}"]

    validator = Path(__file__).with_name("validate-skills.sh")
    if not validator.exists():
        return [f"Skill validator not found next to promote-skill.py: {validator}"]

    res = subprocess.run(
        ["bash", str(validator), str(skill_dir.parent), skill_dir.name],
        capture_output=True,
        text=True,
    )
    if res.returncode == 0:
        return []
    output = (res.stdout + res.stderr).strip()
    return [line.strip() for line in output.splitlines() if line.strip()]


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
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        print(
            f"Error: invalid skill name {name!r}: expected kebab-case ('a-z0-9' separated by single dashes)",
            file=sys.stderr,
        )
        return 2

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
    base_resolved = target_base.resolve()
    target_resolved = target_dir.resolve()
    if target_resolved != base_resolved / name:
        print(f"Error: refusing to write outside {base_resolved}: {target_resolved}", file=sys.stderr)
        return 2

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
    validate_script = Path(__file__).with_name("validate-skills.sh")
    if not args.is_global:
        if validate_script.exists():
            res = subprocess.run(["bash", str(validate_script), str(target_base)], capture_output=True, text=True)
            if res.returncode != 0:
                print(f"[WARNING] validate-skills.sh reported issues:\n{res.stdout}\n{res.stderr}")
            else:
                print(f"[VALIDATION COMPLETE] {res.stdout.strip()}")
        else:
            print(f"[WARNING] Skipped catalog validation: {validate_script} not found")

    return 0


if __name__ == "__main__":
    sys.exit(main())
