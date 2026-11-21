# Memory store

Memory holds **selected, distilled knowledge**, not a complete log of every working session.

## Categories

- `entries/bugfixes/`: symptom → root cause → fix → verification.
- `entries/decisions/`: decisions and trade-offs with long-term impact.
- `entries/patterns/`: architecture or code patterns proven within a defined scope.
- `entries/workflows/`: repeatable procedures and commands.
- `entries/environment/`: easy-to-forget environment, toolchain, deployment or dependency details.
- `archive/YYYY/`: historical knowledge, excluded from default search results.

## Writing memory

1. Search for a similar topic before creating a file.
2. Use `../template/memory/memory-entry.md`.
3. Keep one reusable lesson per entry; aim for roughly 200–700 words unless the case needs more.
4. State the evidence and the applicable scope; separate confirmed facts from hypotheses.
5. Update `INDEX.md` only for high-value entries or ones you look up often.
6. Track changes with Git and review them like code.

## Searching

Run from the project root:

```bash
.agents/scripts/search-memory.sh "exact error or concept"
.agents/scripts/search-memory.sh --archive "exact error or concept"
```

If the repository has no script, run `"$HOME/.agents/scripts/search-memory.sh" "exact error or concept"`. The script detects the current Git root and searches both project and global memory.
