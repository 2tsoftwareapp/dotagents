#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

target="${1:-}"
if [[ -n "$target" ]]; then
  if [[ -d "$target/.agents" ]]; then
    AGENTS_DIR="$(cd "$target/.agents" && pwd)"
  elif [[ -d "$target" ]]; then
    AGENTS_DIR="$(cd "$target" && pwd)"
  else
    echo "Error: target directory does not exist: $target" >&2
    exit 1
  fi
else
  if [[ -d "$SCRIPT_DIR/../rules" && -d "$SCRIPT_DIR/../skills" ]]; then
    AGENTS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
  elif [[ -d "$ROOT_DIR/.agents" ]]; then
    AGENTS_DIR="$(cd "$ROOT_DIR/.agents" && pwd)"
  else
    AGENTS_DIR="$ROOT_DIR"
  fi
fi

echo "=== dotagents framework health check ==="
echo "Framework directory: $AGENTS_DIR"
echo

failures=0

# 1. Check the core directory structure
echo "[1/4] Checking core directories:"
required_dirs=("rules" "skills" "scripts" "template" "memory")
for d in "${required_dirs[@]}"; do
  if [[ -d "$AGENTS_DIR/$d" ]]; then
    echo "  ✓ $d"
  else
    echo "  ✗ Missing directory $d"
  fi
done

# 2. Check script executable permissions
echo
echo "[2/4] Checking script executable permissions:"
for s in "$AGENTS_DIR/scripts"/*.sh "$AGENTS_DIR/scripts"/*.py; do
  [[ ! -f "$s" ]] && continue
  fname="$(basename "$s")"
  if [[ -x "$s" ]]; then
    echo "  ✓ $fname (executable)"
  else
    echo "  ✗ $fname (missing chmod +x)"
    failures=$((failures + 1))
  fi
done

# 3. Run validate-skills.sh
echo
echo "[3/4] Checking skill validity:"
if "$AGENTS_DIR/scripts/validate-skills.sh" "$AGENTS_DIR/skills"; then
  echo "  ✓ All skills pass YAML frontmatter validation"
else
  echo "  ✗ Skill format error"
  failures=$((failures + 1))
fi

# 4. Run validate-memory.py
echo
echo "[4/4] Checking memory schema validity:"
if python3 "$AGENTS_DIR/scripts/validate-memory.py" "$AGENTS_DIR/memory/entries"; then
  echo "  ✓ All memory entries have the 15 frontmatter fields and valid enums"
else
  echo "  ✗ Memory entry format error"
  failures=$((failures + 1))
fi

# 5. Run unit tests
echo
if python3 "$AGENTS_DIR/scripts/test-validate-memory.py" && \
   python3 "$AGENTS_DIR/scripts/test-search-memory.py" && \
   python3 "$AGENTS_DIR/scripts/test-skill-distiller.py" >/dev/null; then
  echo "  ✓ Unit tests passing (validate-memory, search-memory, test-skill-distiller)"
else
  echo "  ✗ Unit tests failed"
  failures=$((failures + 1))
fi

echo
if (( failures == 0 )); then
  echo "===> RESULT: ALL CHECKS PASSED! (0 errors) <==="
  exit 0
else
  echo "===> RESULT: Found $failures error(s) to fix! <==="
  exit 1
fi
