#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Running integration test for init-global.sh..."

# Ensure the temp directory works reliably in every environment
if [[ -z "${TMPDIR:-}" ]]; then
  if mkdir -p "$HOME/.cache/tmp" 2>/dev/null; then
    export TMPDIR="$HOME/.cache/tmp"
  fi
fi

TEMP_TARGET="$(mktemp -d)"
SANDBOX="$(mktemp -d)"
trap 'rm -rf "$TEMP_TARGET" "$SANDBOX"' EXIT

# Scenario 1: custom AGENTS.md and rules/language.md already exist
mkdir -p "$TEMP_TARGET/rules"
echo "# CUSTOM GLOBAL AGENTS" > "$TEMP_TARGET/AGENTS.md"
echo "# CUSTOM LANGUAGE RULES" > "$TEMP_TARGET/rules/language.md"

# Run init-global.sh into the target directory
"$SCRIPT_DIR/init-global.sh" "$TEMP_TARGET"

# Safety check: existing files are not overwritten without --force
if ! grep -q "CUSTOM GLOBAL AGENTS" "$TEMP_TARGET/AGENTS.md"; then
  echo "FAIL: AGENTS.md was overwritten without --force!" >&2
  exit 1
fi
if ! grep -q "CUSTOM LANGUAGE RULES" "$TEMP_TARGET/rules/language.md"; then
  echo "FAIL: rules/language.md was overwritten without --force!" >&2
  exit 1
fi

# Scenario 2: check the flat structure (no nested .agents/.agents)
if [[ -d "$TEMP_TARGET/.agents" ]]; then
  echo "FAIL: init-global created a .agents/ subdirectory inside the global target!" >&2
  exit 1
fi

# Check that the core directories sit directly under TARGET
for dir in rules skills scripts template memory; do
  if [[ ! -d "$TEMP_TARGET/$dir" ]]; then
    echo "FAIL: missing directory $dir in the global target!" >&2
    exit 1
  fi
done

# Scenario 3: rules/project.md must not be copied into global
if [[ -f "$TEMP_TARGET/rules/project.md" ]]; then
  echo "FAIL: rules/project.md (per-project only) was copied into the global target!" >&2
  exit 1
fi

# Scenario 4: no junk artifacts/pycache copied
if find "$TEMP_TARGET" -name '*.pyc' -o -name '__pycache__' | grep -q .; then
  echo "FAIL: init-global copied junk artifacts/pycache into the target!" >&2
  exit 1
fi

# Scenario 5: run doctor.sh on the freshly initialized global directory
"$TEMP_TARGET/scripts/doctor.sh"

# Scenario 6: test a relative path inside the sandbox
(
  cd "$SANDBOX"
  "$SCRIPT_DIR/init-global.sh" "my_relative_global"
  if [[ ! -f "my_relative_global/AGENTS.md" || ! -d "my_relative_global/rules" ]]; then
    echo "FAIL: init-global failed with a relative destination path!" >&2
    exit 1
  fi
)

# Scenario 7: --force overwrites existing files
"$SCRIPT_DIR/init-global.sh" --force "$TEMP_TARGET"
if grep -q "CUSTOM GLOBAL AGENTS" "$TEMP_TARGET/AGENTS.md"; then
  echo "FAIL: --force did not overwrite AGENTS.md!" >&2
  exit 1
fi

echo "test_init_global: ok"
