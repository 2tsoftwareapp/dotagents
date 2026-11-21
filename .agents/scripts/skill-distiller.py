#!/usr/bin/env python3
"""Skill Distiller: Automatically extract, deduplicate, and generate skill drafts.

Part of the dotagents Self-Learning Skill Loop system.
Supports:
- Input from a JSON file, CLI arguments, or reflection text.
- Duplicate detection (lexical similarity & token overlap) against the existing skills.
- Generate a standardized `SKILL.md` draft at `.agents/skills/.staging/<skill-name>/SKILL.md`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


def to_kebab_case(s: str) -> str:
    """Convert a string to valid kebab-case."""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s_-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def parse_frontmatter(content: str) -> dict[str, str]:
    """Extract simple YAML frontmatter."""
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


def tokenize(text: str) -> set[str]:
    """Split semantic words for similarity scoring (Unicode-aware)."""
    words = re.findall(r"[\w-]{2,}", text.lower())
    # Drop basic stop words
    stop_words = {
        "and", "the", "for", "with", "from", "when", "that", "this", "skill"
    }
    return {w for w in words if w not in stop_words}


def compute_similarity(tokens1: set[str], tokens2: set[str]) -> float:
    """Compute Jaccard similarity between two word sets."""
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)


def find_similar_skills(
    name: str,
    description: str,
    skills_dir: Path
) -> list[tuple[str, float, str]]:
    """Find existing skills with similar content or purpose."""
    results: list[tuple[str, float, str]] = []
    if not skills_dir.exists():
        return results

    query_tokens = tokenize(f"{name} {description}")

    for skill_path in skills_dir.glob("*/SKILL.md"):
        if ".staging" in skill_path.parts:
            continue
        existing_name = skill_path.parent.name
        try:
            content = skill_path.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = parse_frontmatter(content)
        existing_desc = fm.get("description", "")
        existing_tokens = tokenize(f"{existing_name} {existing_desc}")

        sim = compute_similarity(query_tokens, existing_tokens)
        if sim > 0.35:  # Threshold for noteworthy similarity
            results.append((existing_name, sim, existing_desc))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def render_skill_md(
    name: str,
    description: str,
    triggers: list[str],
    anti_triggers: list[str],
    procedure: list[str],
    rules: list[str],
    gotchas: list[str],
    code_snippets: list[str]
) -> str:
    """Render SKILL.md content following the standard template."""
    lines = [
        "---",
        f"name: {name}",
        f"description: \"{description}\"",
        "---",
        f"# {name}",
        "",
        "## When to use",
    ]
    if triggers:
        for t in triggers:
            lines.append(f"- {t}")
    else:
        lines.append("- Apply when the situation matches the described context.")

    lines.extend(["", "## When not to use"])
    if anti_triggers:
        for at in anti_triggers:
            lines.append(f"- {at}")
    else:
        lines.append("- Do not apply when the problem falls outside the described scope.")

    lines.extend(["", "## Process"])
    if procedure:
        for idx, step in enumerate(procedure, 1):
            lines.append(f"{idx}. {step}")
    else:
        lines.append("1. Read and identify the preconditions.")
        lines.append("2. Execute the verification steps in order.")
        lines.append("3. Check the actual result.")

    lines.extend(["", "## Rules"])
    if rules:
        for r in rules:
            lines.append(f"- {r}")
    else:
        lines.append("- Verify the actual result before concluding.")
        lines.append("- Keep changes to a minimum (minimal diff).")

    if gotchas:
        lines.extend(["", "## Common pitfalls & troubleshooting"])
        for g in gotchas:
            lines.append(f"- {g}")

    if code_snippets:
        lines.extend(["", "## Code snippets / sample commands"])
        for snippet in code_snippets:
            lines.append("```bash")
            lines.append(snippet.strip())
            lines.append("```")

    lines.extend(["", "## Completion criteria", "- The verification step succeeds and no unexpected errors occur.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill Distiller - Automatically extract and generate skill drafts")
    parser.add_argument("--name", help="Skill name (kebab-case)")
    parser.add_argument("--description", help="Description of the skill purpose and triggers")
    parser.add_argument("--payload", help="Path to a JSON file with the distilled lesson data")
    parser.add_argument("--skills-dir", default=".agents/skills", help="Main skills directory (default: .agents/skills)")
    parser.add_argument("--staging-dir", default=".agents/skills/.staging", help="Staging directory for draft skills")
    parser.add_argument("--trigger", action="append", default=[], help="Add a trigger condition")
    parser.add_argument("--anti-trigger", action="append", default=[], help="Add a non-applicable condition")
    parser.add_argument("--step", action="append", default=[], help="Add a procedure step")
    parser.add_argument("--rule", action="append", default=[], help="Add a mandatory rule")
    parser.add_argument("--gotcha", action="append", default=[], help="Add a pitfall / note")
    parser.add_argument("--code", action="append", default=[], help="Add a code snippet / sample command")
    parser.add_argument("--force", action="store_true", help="Ignore duplicate warnings and create a new draft")

    args = parser.parse_args()

    # Load data from the JSON payload when provided
    data: dict[str, Any] = {}
    if args.payload:
        p_path = Path(args.payload)
        if not p_path.exists():
            print(f"Error: payload file does not exist: {args.payload}", file=sys.stderr)
            return 1
        with open(p_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    raw_name = args.name or data.get("name")
    if not raw_name:
        print("Error: missing skill name (--name or in --payload)", file=sys.stderr)
        return 1

    name = to_kebab_case(raw_name)
    if not name:
        print("Error: skill name must contain at least one ASCII letter or digit (kebab-case slug)", file=sys.stderr)
        return 1
    description = (args.description or data.get("description") or "").strip()
    if not description:
        print("Error: missing skill description (--description or in --payload)", file=sys.stderr)
        return 1

    triggers = args.trigger or data.get("triggers", [])
    anti_triggers = args.anti_trigger or data.get("anti_triggers", [])
    procedure = args.step or data.get("procedure", [])
    rules = args.rule or data.get("rules", [])
    gotchas = args.gotcha or data.get("gotchas", [])
    code_snippets = args.code or data.get("code_snippets", [])

    skills_dir = Path(args.skills_dir)
    staging_dir = Path(args.staging_dir)

    # 1. Check for duplicates
    similar = find_similar_skills(name, description, skills_dir)
    if similar:
        top_name, top_sim, top_desc = similar[0]
        if top_sim >= 0.65 and not args.force:
            print(f"[DUPLICATE WARNING] Skill '{name}' is highly similar ({top_sim:.1%}) to existing skill '{top_name}'.")
            print(f"  Existing description: {top_desc}")
            print("  Recommendation: update the existing skill instead of creating a new one, or pass --force to continue.")
            return 2
        else:
            print(f"[NOTICE] Found {len(similar)} skill(s) with shared terms:")
            for s_name, s_sim, _ in similar[:3]:
                print(f"  - {s_name} (similarity: {s_sim:.1%})")

    # 2. Render the SKILL.md content
    content = render_skill_md(
        name=name,
        description=description,
        triggers=triggers,
        anti_triggers=anti_triggers,
        procedure=procedure,
        rules=rules,
        gotchas=gotchas,
        code_snippets=code_snippets
    )

    # 3. Write into the staging directory
    draft_skill_dir = staging_dir / name
    draft_skill_dir.mkdir(parents=True, exist_ok=True)
    draft_file = draft_skill_dir / "SKILL.md"

    draft_file.write_text(content, encoding="utf-8")
    print(f"[SUCCESS] Draft skill created at: {draft_file.resolve()}")
    print("Next: use 'scripts/promote-skill.py' to validate and move it into the official catalog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
