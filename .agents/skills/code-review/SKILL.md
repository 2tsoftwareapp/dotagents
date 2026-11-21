---
name: code-review
description: "Review code changes based on the diff and surrounding context, prioritizing bugs, regressions, security, data and maintainability. Use before merge or when asked to assess code quality."
---
# Code review

## When to use
- Before merge/release, after a significant change, or when asked for an independent review.

## When not to use
- The requirement is still being implemented; use `implementation` and review the diff afterwards.

## Process
1. Read the requirements/acceptance criteria and related memory; define the diff scope.
2. Read the diff together with surrounding code, callers/callees, tests, schema and related contracts.
3. Look for logic errors, state handling, race conditions, validation, access control, data leaks, backward compatibility and regressions.
4. Check whether new tests actually catch the defect or guarantee the required behavior.
5. Rank findings by impact; each finding needs a specific location, trigger condition, impact and remediation direction.
6. Record findings in `code-review.md` if the review is large or history must be kept. If you find no issues, state the scope you examined and its limits.

## Rules
- Only report what the diff/code/tests support; do not create findings from unverified speculation.
- Prioritize actionable findings; do not focus on formatting preferences when a formatter already exists.
- Distinguish definite bugs from questions that need verification.
- Do not claim a complete review if you only looked at part of the file or could not run tests.
- A review report based on the template must be written to a Markdown file (`.md`); chat only summarizes the conclusion, findings count, main blockers and the file path.
- Review tone follows *Clear but not cold* and *Helpful but not overly-prescriptive*: state the cause with evidence, suggest remediation and analyze trade-offs instead of imposing or issuing orders.

## Completion criteria
- Findings are clearly classified; blockers/high severity issues are addressed or deliberately accepted before merge.

## Related templates
`.agents/template/software/code-review.md`
