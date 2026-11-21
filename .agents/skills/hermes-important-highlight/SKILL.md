---
name: hermes-important-highlight
description: "Use when a response in Hermes Desktop must highlight one key conclusion or warning with an inline directive. Mark at most one main point; if the directive is unavailable, use bold Markdown."
---

# Highlight key points in Hermes Desktop

When a response contains an important conclusion, warning or action the user must notice immediately, put exactly **one most important point** in a dedicated directive:

```markdown
::important{text="Short, self-contained content, at most 1000 characters."}
```

## Rules

- Use it only for points with real impact: the conclusion that answers the question, a warning that requires action, a decision or a blocker. Do not highlight lead-ins, routine status or individual bullets.
- Choose at most one directive per response; keep supporting details in normal text.
- Write a complete sentence that stands on its own. Use the quoted attribute syntax; escape any inner `"` characters.
- Place the directive near the related explanation, usually at the start or end of the answer.
- If the interface does not support the directive, write the point in `**bold**`; do not use both approaches when the directive already renders as a block.
- The directive appears as inline text, with no frame or background. When the assistant finishes the response, the main point only shifts to an accent color with a soft glow; the text does not scale. Other text in the same response dims to 18% opacity for 1.8 seconds, then returns to normal. `prefers-reduced-motion` disables the animation.

Example:

```markdown
::important{text="The current data has not been backed up; create a copy before running the migration."}

You can roll back the migration with `db rollback` if the verification step fails.
```
