---
name: incident-response
description: "Coordinate handling of an incident affecting a service or its users: establish scope, reduce impact, post status updates, recover and run a postmortem."
---
# Incident response

## When to use
- Production/service is failing, degraded, losing data, erroring on transactions, or user impact is ongoing.

## When not to use
- The bug is unreleased and does not affect a running system → `bug-investigation`.

## Process
1. Establish the impact, start time, affected systems/segments and how reliable the available data is.
2. Prioritize safe, reversible impact-reduction measures: rollback, feature disable, traffic shift or an appropriate mitigation.
3. Assign roles/points of contact if available; keep a timeline of events and decisions and post clear status updates.
4. Collect redacted logs/metrics/traces; separate confirmation from hypothesis.
5. Do not make destructive changes or bulk-edit data without a backup, a plan and the proper authority.
6. Verify the service has recovered using the relevant indicators and business flows, not just the fact that the homepage loads.
7. Once stable, use `incident-postmortem.md` to record impact, timeline, cause, contributing factors and action items with an owner/completion condition.
8. Pass durable lessons to `memory-curation` when they help with similar incidents.

## Rules
- Restoring service and protecting important data outranks finding someone to blame.
- Do not write secrets, tokens or unnecessary user data into reports.
- Do not assert a final cause before the evidence is strong enough.
- Action items must be checkable; avoid vague goals such as "be more careful".

## Completion criteria
- The impact is stopped/recovered or the remaining impact is disclosed; the postmortem and follow-up actions have an owner where appropriate.

## Related templates
`.agents/template/software/incident-postmortem.md`
