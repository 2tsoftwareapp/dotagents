#!/usr/bin/env python3
"""Unit tests for skill-distiller.py and promote-skill.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import importlib.util
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


distiller_mod = _load_module("skill_distiller", "skill-distiller.py")


def test_kebab_case() -> None:
    assert distiller_mod.to_kebab_case("My New Feature") == "my-new-feature"
    assert distiller_mod.to_kebab_case("Docker_PG_Migrate-2026!") == "docker-pg-migrate-2026"
    assert distiller_mod.to_kebab_case("---bad---name---") == "bad-name"


def test_render_skill_md() -> None:
    content = distiller_mod.render_skill_md(
        name="test-skill",
        description="Test skill description",
        triggers=["When running unit tests"],
        anti_triggers=["When deploying to production"],
        procedure=["Run pytest", "Check the exit code"],
        rules=["Never skip asserts"],
        gotchas=["Watch out for timeouts"],
        code_snippets=["pytest -v"]
    )
    assert content.startswith("---\nname: test-skill\n")
    assert 'description: "Test skill description"' in content
    assert "## When to use" in content
    assert "- When running unit tests" in content
    assert "## When not to use" in content
    assert "## Process" in content
    assert "1. Run pytest" in content
    assert "## Rules" in content
    assert "## Common pitfalls & troubleshooting" in content
    assert "## Code snippets / sample commands" in content
    assert "```bash\npytest -v\n```" in content
    assert "## Completion criteria" in content


def test_similarity_and_deduplication() -> None:
    with tempfile.TemporaryDirectory() as td:
        skills_dir = Path(td)
        existing_skill_dir = skills_dir / "sqlite-wal-optimization"
        existing_skill_dir.mkdir(parents=True)
        (existing_skill_dir / "SKILL.md").write_text("""---
name: sqlite-wal-optimization
description: "Optimize concurrent writes and prevent database locking with SQLite WAL mode"
---
# SQLite WAL Optimization
## When to use
- When SQLite database locked appears
""", encoding="utf-8")

        # High-similarity case
        similar = distiller_mod.find_similar_skills(
            name="sqlite-wal-lock-fix",
            description="Optimize and prevent locking with SQLite WAL mode",
            skills_dir=skills_dir
        )
        assert len(similar) >= 1
        name, sim, _ = similar[0]
        assert name == "sqlite-wal-optimization"
        assert sim > 0.4


def test_end_to_end_distill_and_promote() -> None:
    with tempfile.TemporaryDirectory() as td:
        base_dir = Path(td)
        staging_dir = base_dir / "staging"
        skills_dir = base_dir / "skills"
        skills_dir.mkdir(parents=True)

        payload_path = base_dir / "lesson.json"
        payload_data = {
            "name": "auto-cache-busting",
            "description": "Automatically bust the static asset cache when building frontend assets",
            "triggers": ["When new frontend assets are deployed"],
            "anti_triggers": ["When only the backend API changes"],
            "procedure": ["Generate content hash", "Update manifest.json"],
            "rules": ["SHA-256 is mandatory"],
            "gotchas": ["Avoid hardcoding timestamps"],
            "code_snippets": ["npm run build -- --hash"]
        }
        payload_path.write_text(json.dumps(payload_data, ensure_ascii=False), encoding="utf-8")

        # 1. Run the distiller
        cmd_distill = [
            sys.executable,
            str(SCRIPTS_DIR / "skill-distiller.py"),
            "--payload", str(payload_path),
            "--skills-dir", str(skills_dir),
            "--staging-dir", str(staging_dir)
        ]
        res_distill = subprocess.run(cmd_distill, capture_output=True, text=True)
        assert res_distill.returncode == 0, f"Distill failed: {res_distill.stderr}"

        draft_file = staging_dir / "auto-cache-busting" / "SKILL.md"
        assert draft_file.exists()

        # 2. Run promote in dry-run mode
        cmd_dry_run = [
            sys.executable,
            str(SCRIPTS_DIR / "promote-skill.py"),
            "auto-cache-busting",
            "--staging-dir", str(staging_dir),
            "--skills-dir", str(skills_dir),
            "--dry-run"
        ]
        res_dry_run = subprocess.run(cmd_dry_run, capture_output=True, text=True)
        assert res_dry_run.returncode == 0, f"Dry run failed: {res_dry_run.stderr}"

        # 3. Run the actual promotion
        cmd_promote = [
            sys.executable,
            str(SCRIPTS_DIR / "promote-skill.py"),
            "auto-cache-busting",
            "--staging-dir", str(staging_dir),
            "--skills-dir", str(skills_dir)
        ]
        res_promote = subprocess.run(cmd_promote, capture_output=True, text=True)
        assert res_promote.returncode == 0, f"Promote failed: {res_promote.stderr}"

        promoted_file = skills_dir / "auto-cache-busting" / "SKILL.md"
        assert promoted_file.exists()
        assert not draft_file.exists()


def test_promote_rejects_path_traversal() -> None:
    with tempfile.TemporaryDirectory() as td:
        base_dir = Path(td)
        staging_dir = base_dir / "staging"
        skills_dir = base_dir / "skills"
        staging_dir.mkdir()
        outside = base_dir / "escape"
        outside.mkdir()
        (outside / "SKILL.md").write_text(
            '---\nname: escape\ndescription: "demo"\n---\n# Demo\n', encoding="utf-8"
        )

        res = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "promote-skill.py"),
                "../escape",
                "--staging-dir", str(staging_dir),
                "--skills-dir", str(skills_dir),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 2, f"Traversal name was accepted: {res.stdout}"
        assert not skills_dir.exists(), "Promotion created an out-of-scope destination"


def test_promote_rejects_missing_sections() -> None:
    with tempfile.TemporaryDirectory() as td:
        base_dir = Path(td)
        staging_dir = base_dir / "staging"
        skills_dir = base_dir / "skills"
        draft_dir = staging_dir / "incomplete-skill"
        draft_dir.mkdir(parents=True)
        (draft_dir / "SKILL.md").write_text(
            '---\nname: incomplete-skill\ndescription: "demo"\n---\n# Demo\n\n## Rules\n- Only one section\n',
            encoding="utf-8",
        )

        res = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "promote-skill.py"),
                "incomplete-skill",
                "--staging-dir", str(staging_dir),
                "--skills-dir", str(skills_dir),
                "--dry-run",
            ],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 2, f"Incomplete draft was accepted: {res.stdout}"
        assert "missing required section" in (res.stdout + res.stderr)


def test_distiller_rejects_empty_slug() -> None:
    with tempfile.TemporaryDirectory() as td:
        staging_dir = Path(td) / "staging"
        res = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "skill-distiller.py"),
                "--name", "\u4fee\u590d\u6570\u636e\u5e93",
                "--description", "demo",
                "--staging-dir", str(staging_dir),
            ],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 1, res.stdout + res.stderr
        assert not (staging_dir / "SKILL.md").exists(), "Empty slug wrote a draft into the staging root"


def main() -> int:
    print("Running test_kebab_case...")
    test_kebab_case()
    print("Running test_render_skill_md...")
    test_render_skill_md()
    print("Running test_similarity_and_deduplication...")
    test_similarity_and_deduplication()
    print("Running test_end_to_end_distill_and_promote...")
    test_end_to_end_distill_and_promote()
    print("Running test_promote_rejects_path_traversal...")
    test_promote_rejects_path_traversal()
    print("Running test_promote_rejects_missing_sections...")
    test_promote_rejects_missing_sections()
    print("Running test_distiller_rejects_empty_slug...")
    test_distiller_rejects_empty_slug()
    print("ALL TESTS PASSED! (7/7 test suites)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
