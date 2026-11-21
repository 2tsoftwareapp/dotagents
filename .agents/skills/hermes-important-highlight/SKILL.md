---
name: hermes-important-highlight
description: "Use when a response in Hermes Desktop must highlight one key conclusion or warning with an inline directive. Mark at most one main point; if the directive is unavailable, use bold Markdown."
---

# Highlight key points in Hermes Desktop

## When to use
- A response contains an important conclusion, warning or action the user must notice immediately.
- One point outranks everything else in the answer and deserves to stand out.

## When not to use
- The response is routine status, a lead-in or a list of equally weighted bullets.
- The point is already carried by a heading, a table or a code block.

## Process
1. Pick exactly one point: the conclusion that answers the question, a warning that needs action, a decision or a blocker.
2. Write it as a complete sentence that stands on its own, at most 1000 characters, using the quoted attribute syntax and escaping any inner `"` characters.
3. Place the directive near the related explanation, usually at the start or end of the answer.
4. Keep supporting details in normal text.

```markdown
::important{text="Short, self-contained content, at most 1000 characters."}
```

## Rules
- Use it only for points with real impact. Do not highlight lead-ins, routine status or individual bullets.
- Choose at most one directive per response.
- If the interface does not support the directive, write the point in `**bold**`; do not use both approaches when the directive already renders as a block.

## Rendering behavior
- The directive appears as inline text, with no frame or background. When the assistant finishes the response, the main point only shifts to an accent color with a soft glow; the text does not scale.
- Other text in the same response dims to 18% opacity for 1.8 seconds, then returns to normal. `prefers-reduced-motion` disables the animation.

## Completion criteria
- The response carries at most one directive, the highlighted sentence stands on its own, and the `**bold**` fallback is used only when the directive is unavailable.

Example:

```markdown
::important{text="The current data has not been backed up; create a copy before running the migration."}

You can roll back the migration with `db rollback` if the verification step fails.
```
