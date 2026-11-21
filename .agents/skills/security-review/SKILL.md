---
name: security-review
description: "Assess security risk for changes involving authentication, authorization, sensitive data, uploads, files, external integrations, secrets or handling of untrusted input."
---
# Security review

## When to use
- Changes to authn/authz, session/token, tenant isolation, data access permissions, upload/download, webhooks, secrets, logging or dependencies with an attack surface.
- Before release when the risk level requires a dedicated security check.

## When not to use
- Purely content changes with no related data/trust flows; applying the general security rules is still mandatory.

## Process
1. Read `.agents/rules/security.md`, the requirements and the related code.
2. Identify the assets to protect, attackers/actors, trust boundaries, sensitive data and the privileges that must be enforced.
3. Check server-side authentication and authorization, per-resource permission checks, tenant boundaries and fail-closed behavior.
4. Check input validation/normalization, injection, file/path handling, SSRF or deserialization where relevant to the actual flow.
5. Check secret management, logs/telemetry, error responses, CORS/CSRF/cookie/token policy and dependencies across the relevant surface.
6. For schema/permission changes, check legacy data, default permissions, backfill and rollback capability.
7. Record findings with location, condition, impact and mitigation. If documentation is needed, use the security review template.
8. Test access-denial cases and invalid input; do not only test the happy path.

## Rules
- Do not put real secrets into prompts, logs, documents or fixtures.
- Do not treat hiding a button in the UI as an authorization mechanism.
- Do not run penetration tests on systems where you are not authorized.
- Do not claim a system is absolutely secure; state only the scope you checked and the remaining risk.

## Completion criteria
- No unaddressed serious finding remains, or one accepted by an authorized person; the review scope and limits are clear.

## Related templates
`.agents/template/software/security-review.md`
