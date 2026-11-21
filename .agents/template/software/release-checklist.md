# Release checklist: <release/change>

- **Version/build:**
- **Target environment:**
- **Release owner:**
- **Planned time:** YYYY-MM-DD HH:mm TZ

## Before release

- [ ] Acceptance criteria and critical tests pass.
- [ ] Build/artifact/config reviewed.
- [ ] Migrations and data compatibility checked.
- [ ] Feature flags, permissions, secrets, and access policies checked.
- [ ] Changelog/runbook/support notes updated.
- [ ] Backup or recovery plan confirmed where needed.

## Deployment

- [ ] Deploy steps:
- [ ] Ordering/migration constraints:
- [ ] Smoke test:
- [ ] Health indicators/logs/metrics to watch:

## Rollback

- **Trigger conditions:**
- **Rollback steps:**
- **Data/schema notes:**
- **Decision owner:**

## After release

- [ ] Core user flows checked.
- [ ] Error rate/latency/business signals checked.
- [ ] Known issues and their owners recorded.
- [ ] Memory updated if the release surfaced reusable operational knowledge.
