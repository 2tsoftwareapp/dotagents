#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  init-project.sh [--force] <target-project-dir>

Initialize the .agents/ structure and AGENTS.md for a new repository from the dotagents framework.
Safe by default: does NOT overwrite existing files (such as .agents/rules/project.md, AGENTS.md, ...)
unless the --force flag is passed.

Examples:
  ./init-project.sh ~/tx/GitHub/my-new-app
  ./init-project.sh --force ~/tx/GitHub/my-new-app
USAGE
}

force=false
target_arg=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force|-f)
      force=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$target_arg" ]]; then
        target_arg="$1"
      else
        echo "Error: too many positional arguments: $1" >&2
        usage >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$target_arg" ]]; then
  usage >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Ensure target directory exists first so cd/pwd resolves absolute path cleanly
mkdir -p "$target_arg"
TARGET="$(cd "$target_arg" && pwd)"


copy_file_safe() {
  local src="$1"
  local dest="$2"
  local rel="$3"

  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" && "$force" != true ]]; then
    echo "  - Kept (already exists): $rel"
  else
    cp "$src" "$dest"
    echo "  + Copied: $rel"
  fi
}

# 1. Root AGENTS.md
copy_file_safe "$ROOT_DIR/AGENTS.md" "$TARGET/AGENTS.md" "AGENTS.md"

# 2. .agents/AGENTS.md
if [[ -f "$ROOT_DIR/.agents/AGENTS.md" ]]; then
  copy_file_safe "$ROOT_DIR/.agents/AGENTS.md" "$TARGET/.agents/AGENTS.md" ".agents/AGENTS.md"
fi

# 3. All files under .agents/ (skip __pycache__, *.pyc, .DS_Store, temp artifacts)
cd "$ROOT_DIR"
find .agents -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '.DS_Store' | while IFS= read -r rel_file; do
  [[ "$rel_file" == ".agents/AGENTS.md" ]] && continue
  copy_file_safe "$ROOT_DIR/$rel_file" "$TARGET/$rel_file" "$rel_file"
done

# Ensure scripts are executable
chmod +x "$TARGET/.agents/scripts/"*.sh "$TARGET/.agents/scripts/"*.py 2>/dev/null || true

echo "==> Initialized successfully!"
echo "Next steps:"
echo "  1. Open: $TARGET/.agents/rules/project.md and fill in the stack and the test/run commands for the project."
echo "  2. Run: $TARGET/.agents/scripts/doctor.sh to check integrity."
