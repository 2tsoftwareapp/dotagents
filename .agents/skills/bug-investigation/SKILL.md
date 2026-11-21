---
name: bug-investigation
description: "Investigate failures from evidence, reproduce them, form hypotheses, confirm the root cause and add a regression test. Use when there is a bug, runtime error, bad data, unstable behavior or failing test."
---
# Bug investigation and resolution

## When to use
- There are error symptoms, a failing test, a crash, wrong state or a bug that is hard to reproduce.

## When not to use
- The request is to add new behavior that does not exist yet → `requirements-discovery`.
- An incident is affecting production and impact reduction needs coordinating now → `incident-response` first.

## Process
1. Search memory for the exact error message, symptoms, subsystem and synonyms.
2. Collect evidence: reproduction steps, input, environment/version, logs with sensitive data redacted, and expected/actual behavior.
3. Determine the reproduction level: always happens, conditional, or not reproduced yet.
4. Propose hypotheses a test can distinguish; prefer small experiments that eliminate hypotheses.
5. Trace through the data/state flow to find the root cause; do not stop at symptoms when the cause can be identified.
6. Use `bug-investigation.md` when the investigation is complex or the conclusions need to be recorded.
7. Fix the confirmed cause and add a regression test that reproduces the earlier failure.
8. Run the targeted test, related tests and check for side-effect failures.
9. Call `memory-curation` if the fix is reusable or the bug is likely to recur.

## Rules
- Do not conclude a root cause just because one change made the symptom disappear.
- Separate observed facts, hypotheses and conclusions.
- If you cannot reproduce it, state the conditions you tried and the evidence you are missing.
- Do not accidentally hide errors with broad catches, arbitrarily increased timeouts or fallbacks that corrupt data.
- When using the `bug-investigation.md` template, you must write the investigation results to a `.md` file; the chat message only summarizes the root cause, the fix and the report file path.

## Completion criteria
- A root cause supported by evidence, or an explicit note that it remains unidentified.
- A verified fix with appropriate protective tests; remaining limitations are stated.

## Related templates
`.agents/template/software/bug-investigation.md`
