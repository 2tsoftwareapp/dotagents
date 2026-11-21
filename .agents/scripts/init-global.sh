#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  init-global.sh [--force] [target-dir]

Initialize the global dotagents structure (Global Framework) for the user.
Installs into: ~/.agents by default (or the given target directory).

Safe by default: does NOT overwrite existing files unless the --force (-f) flag is passed.

Examples:
  ./init-global.sh
  ./init-global.sh --force
  ./init-global.sh /path/to/custom-global-agents
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
  target_arg="${HOME:-~}/.agents"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

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

# 1. Global AGENTS.md (taken from .agents/AGENTS.md - the standard dotagents workflow)
if [[ -f "$ROOT_DIR/.agents/AGENTS.md" ]]; then
  copy_file_safe "$ROOT_DIR/.agents/AGENTS.md" "$TARGET/AGENTS.md" "AGENTS.md"
fi

# 2. All files under .agents/ (skip AGENTS.md, project.md, and cache)
cd "$ROOT_DIR/.agents"
find . -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '.DS_Store' | while IFS= read -r rel_file; do
  rel_file="${rel_file#./}"
  [[ "$rel_file" == "AGENTS.md" ]] && continue
  [[ "$rel_file" == "rules/project.md" ]] && continue
  copy_file_safe "$ROOT_DIR/.agents/$rel_file" "$TARGET/$rel_file" "$rel_file"
done

# Ensure scripts are executable
chmod +x "$TARGET/scripts/"*.sh "$TARGET/scripts/"*.py 2>/dev/null || true

echo "==> Global dotagents initialized successfully at: $TARGET"
echo "Next steps:"
echo "  1. Configure your agent to read: $TARGET/AGENTS.md as Global Instructions."
echo "  2. Run: $TARGET/scripts/doctor.sh to check integrity."
