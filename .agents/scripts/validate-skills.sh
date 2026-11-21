#!/usr/bin/env bash
set -euo pipefail

skills_dir="${1:-.agents/skills}"
if [[ ! -d "$skills_dir" ]]; then
  echo "Error: skills directory not found: $skills_dir" >&2
  exit 1
fi

errors=0
count=0
while IFS= read -r -d '' file; do
  [[ "$(basename "$file")" == "README.md" ]] && continue
  dir="$(basename "$(dirname "$file")")"
  count=$((count + 1))
  first_line="$(head -n 1 "$file")"
  if [[ "$first_line" != "---" ]]; then
    echo "FAIL $file: missing YAML frontmatter opening with ---"
    errors=$((errors + 1)); continue
  fi
  name="$(awk 'NR>1 && $0=="---" {exit} NR>1 && /^name:/ {sub(/^name:[[:space:]]*/, ""); print; exit}' "$file")"
  description="$(awk 'NR>1 && $0=="---" {exit} NR>1 && /^description:/ {sub(/^description:[[:space:]]*/, ""); print; exit}' "$file")"
  if [[ -z "$name" || "$name" != "$dir" ]]; then
    echo "FAIL $file: name='$name' must match directory name '$dir'"
    errors=$((errors + 1))
  fi
  if [[ -z "$description" ]]; then
    echo "FAIL $file: missing description"
    errors=$((errors + 1))
  fi
  if [[ "$name" =~ [^a-z0-9-] || "$name" == -* || "$name" == *- || "$name" == *--* ]]; then
    echo "FAIL $file: name is not valid kebab-case: '$name'"
    errors=$((errors + 1))
  fi
done < <(find "$skills_dir" -mindepth 2 -maxdepth 2 -name SKILL.md -print0 | sort -z)

if (( count == 0 )); then
  echo "Error: no SKILL.md found in $skills_dir" >&2
  exit 1
fi
if (( errors > 0 )); then
  echo "Validation failed: $errors error(s) across $count skill(s)."
  exit 1
fi
echo "OK: checked $count skill(s), basic frontmatter is valid."
