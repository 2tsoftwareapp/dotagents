---
schema_version: 1
id: "MEM-YYYYMMDD-short-topic"
title: "One short, clear, easy-to-search sentence"
type: bugfix # bugfix | decision | pattern | workflow | environment
scope: project # project | global
status: needs-review # active | needs-review | superseded | archived
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
verified_on: "YYYY-MM-DD" # use "unknown" if not verified
confidence: medium # high | medium | low
tags: [subsystem, symptom, technology]
applies_to:
  repo: "repository name or any"
  stack: "framework/runtime"
  versions: "known version range or unknown"
sources:
  - "path/to/file.ts"
  - "URL or ID of the PR/issue/commit/doc"
related: []
supersedes: null
---

# Summary

State the reusable lesson in 1–3 sentences. What does a future engineer/agent need to know before doing this work?

## When to apply

- Symptoms, trigger conditions, affected subsystem, and related environment/version.
- Conditions where this guidance does **not** apply.

## Context and evidence

- **Observed:** what was seen, with file paths/errors/metrics where relevant.
- **Confirmed:** facts supported by reproduction, tests, source, or runtime evidence.
- **Hypothesis:** state what is unconfirmed, or omit if not useful.

## Root cause / decision

Explain the mechanism behind the problem or the important decision. Do not just restate the task description.

## Resolution / recommended procedure

1. Step or change to make.
2. Step or change to make.
3. Important note on compatibility, limitations, or rollback.

## Verification

- **Command/script:** `exact command or repeatable check`
- **Expected:** the successful result.
- **Result:** pass/fail/not run, with date and relevant version.

## Alternatives and pitfalls

- Options tried/considered and why they were rejected, if this helps avoid repeating wasted effort.
- Known limitations or cases where the solution is unsafe/unsuitable.

## Change history

- YYYY-MM-DD — Created or significantly updated; state what was re-verified.
