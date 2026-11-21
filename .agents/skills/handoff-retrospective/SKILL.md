---
name: handoff-retrospective
description: "Hand off unfinished tasks between sessions/agents/people and summarize improvements after a feature, release or incident. Use when work must continue safely or actionable lessons need to be captured."
---
# Handoff and retrospective

## When to use
- A task is unfinished, the session/agent changes, or the investigation must continue or be handed to someone else.
- After a large feature, complex change, release or incident when a summary yields concrete improvements.

## When not to use
- The task is small and finished, with no loose ends or lessons worth keeping; a short summary is enough.

## Handoff process
1. Record the goal, scope, current status and changes already made.
2. List important files/paths, commands already run and their actual results.
3. State what is unfinished, blockers, assumptions, risks and next steps that can be acted on immediately.
4. List uncommitted changes or user-edited files that the next person must preserve.
5. Note related memory/ADR if any; do not copy memory wholesale into the handoff.
6. Use `.agents/template/software/handoff.md` when the next person must continue asynchronously.

## Retrospective process
1. Base it on facts: goals, results, deviations, waiting time, bugs, tests and rollout.
2. Record what worked, what did not, and the systemic causes; avoid assigning personal blame.
3. Turn lessons into concrete action items with an owner, priority and completion condition.
4. Create a retrospective when it adds value; move durable knowledge into memory instead of keeping a long-term diary.

## Rules
- Do not write "done" if any step remains unverified.
- Do not assume the next agent/session can access the current conversation; hand off enough context.
- Do not put secrets in the handoff.
- When using the handoff or retrospective template, write the document to a `.md` file; chat only summarizes what was done, what comes next and the handoff file path.

## Completion criteria
- The recipient knows exactly the status, next steps and risks; the retrospective has clear follow-up actions.

## Related templates
- `.agents/template/software/handoff.md`
- `.agents/template/software/retrospective.md`
