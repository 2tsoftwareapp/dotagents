# Native ai-memory lifecycle adapter for Hermes

This provider supplies the lifecycle absent from the installed native pre/post-tool hooks. It invokes the existing `ai-memory hook` CLI, which owns sanitization, durable spooling, authentication and delivery. It adds no MCP server, HTTP credential handling, database, recall tool or mirror of built-in Hermes memory.

The configured backend name is `ai-memory-native`. Install its `__init__.py` and `plugin.yaml` into `$HERMES_HOME/plugins/ai-memory-native/`, then use `hermes plugins enable ai-memory-native` and `hermes config set memory.provider ai-memory-native`. The current Hermes plugin installer accepts Git sources, not a local directory; do not pass an absolute source directory to `plugins install`.

Only primary sessions with an explicit absolute `cwd` and a nearest `.ai-memory.toml` containing nonempty `workspace` and `project` are admitted. Unknown scope, cron and delegated children do not produce provider lifecycle writes. Existing pre/post tool hooks retain their own native capture policy. No global project is hardcoded. New repositories must opt in with a marker; existing MCP calls must still name both workspace and project.

A single worker serializes start, prompt and end events. Every job captures its session ID and cwd before enqueueing, so a later session switch cannot reattribute queued observations. Finalization waits for the native durable-spool command. Errors log only a safe failure class/exit code. Assistant content is omitted, matching the current capture policy. Existing memory records and historical queue entries are never rewritten or discarded.

Use the existing ai-memory MCP tools for retrieval and curated task finalization. Automatic prompt recall is intentionally not added by this adapter. Native tool capture is still limited by the Hermes runtime's propagation of session IDs; the separate nested-dispatch regression fix addresses that path.

Run unit tests using the installed native launcher:

```sh
/home/vietis/.hermes/hermes-agent/.hermes/bin/hermes --run-module unittest discover -s .agents/tools/hermes-ai-memory-native/tests -v
```

For a live check, run a harmless one-shot Hermes task from a marked project, finalize it, then inspect its actual ai-memory session, pre/post observations, prompt, `ended_at`, and scoped retrieval. The unit tests alone do not prove backend ingestion.

Rollback: set `memory.provider` to its previous value using `hermes config set`, disable this plugin, and retain its files and all ai-memory data. Configuration backup for the initial rollout is under `~/.agents/outputs/hermes-engineering/backups/2026-11-13-m01-m1/`.
