#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Running integration test for init-project.sh..."
# Ensure the temp directory works reliably in every environment
if [[ -z "${TMPDIR:-}" ]]; then
  if mkdir -p "$HOME/.cache/tmp" 2>/dev/null; then
    export TMPDIR="$HOME/.cache/tmp"
  fi
fi

TEMP_TARGET="$(mktemp -d)"
SANDBOX="$(mktemp -d)"
trap 'rm -rf "$TEMP_TARGET" "$SANDBOX"' EXIT

# Scenario 1: Pre-existing custom project.md and custom AGENTS.md
mkdir -p "$TEMP_TARGET/.agents/rules"
echo "# CUSTOM PROJECT RULES DO NOT OVERWRITE" > "$TEMP_TARGET/.agents/rules/project.md"
echo "# CUSTOM ROOT AGENTS" > "$TEMP_TARGET/AGENTS.md"

# Run init-project.sh
"$SCRIPT_DIR/init-project.sh" "$TEMP_TARGET"

# Assert pre-existing files preserved
if ! grep -q "CUSTOM PROJECT RULES DO NOT OVERWRITE" "$TEMP_TARGET/.agents/rules/project.md"; then
  echo "FAIL: .agents/rules/project.md was overwritten!" >&2
  exit 1
fi
if ! grep -q "CUSTOM ROOT AGENTS" "$TEMP_TARGET/AGENTS.md"; then
  echo "FAIL: root AGENTS.md was overwritten!" >&2
  exit 1
fi

# Assert .agents/AGENTS.md copied
if [[ ! -f "$TEMP_TARGET/.agents/AGENTS.md" ]]; then
  echo "FAIL: missing .agents/AGENTS.md!" >&2
  exit 1
fi

# Assert NO generated cache artifacts copied into target
if find "$TEMP_TARGET" -name '*.pyc' -o -name '__pycache__' | grep -q .; then
  echo "FAIL: init-project copied junk artifacts/pycache into the target!" >&2
  exit 1
fi
(
  cd "$TEMP_TARGET"
  git init -q
  "$TEMP_TARGET/.agents/scripts/doctor.sh"
)

# Scenario 2: Test relative destination directory handling inside an isolated temp sandbox
(
  cd "$SANDBOX"
  "$SCRIPT_DIR/init-project.sh" "my_relative_app"
  if [[ ! -f "my_relative_app/AGENTS.md" || ! -f "my_relative_app/.agents/AGENTS.md" ]]; then
    echo "FAIL: init-project failed with a relative destination path!" >&2
    exit 1
  fi
)

# Scenario 3: Test --force overwrite
"$SCRIPT_DIR/init-project.sh" --force "$TEMP_TARGET"
if grep -q "CUSTOM PROJECT RULES DO NOT OVERWRITE" "$TEMP_TARGET/.agents/rules/project.md"; then
  echo "FAIL: --force did not overwrite .agents/rules/project.md!" >&2
  exit 1
fi

echo "test_init_project: ok"
