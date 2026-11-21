---
name: release-deployment
description: "Prepare releases and deploy safely: check changes, migrations, configuration, rollout, smoke tests, monitoring and rollback. Use before releasing or deploying to shared/production environments."
---
# Release preparation and deployment

## When to use
- Preparing a tag/release/deploy, a schema or runtime configuration change, a feature-flag rollout, or when a rollback plan is needed.

## When not to use
- Only local code changes that have not reached the release step.
- An incident is in progress and impact must be reduced now → `incident-response`.

## Process
1. Determine the environment, release scope, commit/build artifact and who has approval authority.
2. Read the diff, test results, security findings, feature flags and compatibility requirements.
3. Check environment variables/config, secret references, dependencies, health checks and observability.
4. For migrations, confirm rollout order, old/new code compatibility, backfill, locks/downtime and how to roll back or forward-fix.
5. Build the rollout steps, smoke tests, monitoring signals, stop thresholds and rollback plan.
6. Use `release-checklist.md` for releases with significant impact.
7. Perform an actual deploy only when the environment, permissions and authorization are clear; otherwise stop at preparation and report back.
8. After deploy, check health, logs/metrics, critical business flows and abnormal error increases.
9. Record the release outcome, deviations and reusable memory.

## Rules
- Do not deploy to production, delete data or run destructive migrations without explicit approval.
- Do not treat a code rollback as sufficient if schema/data changed incompatibly.
- You must have a way to detect a bad release and stopping conditions; do not just write “monitor logs”.

## Completion criteria
- The release has before/after checks, a response plan, and the deployment status is reported accurately.

## Related templates
`.agents/template/software/release-checklist.md`
