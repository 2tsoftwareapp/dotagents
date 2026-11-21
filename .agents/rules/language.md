# Language standard

## Default

- The default prose language of the `.agents/` set is **English**.
- Write in English for instructions, checklists, investigation notes, decision rationale, verification conclusions and AI-generated memory content.
- File and directory names, metadata field names, enums in structured data, IDs, commands, API names, classes, functions, variables and technical symbols keep their canonical English form.
- Do not translate or improvise values in structured data such as `status: active`, `type: bugfix`, `scope: project` or `schema_version: 1`.
- Conversely, human-facing selection labels in templates (for example work status, risk level, `Yes/No`) must be written in English, unless code or automation reads them directly.
- Keep error messages, code, paths, config names and CLI commands verbatim when quoting them; write the surrounding explanation in English.
- English technical terminology is fine when precision matters. When a term could be misread, add a short clarification on first use.

## Per-project exceptions

- `rules/project.md` may declare its own documentation language for the repository, for example Vietnamese for business documents.
- An exception applies only within the project scope and must be stated explicitly; never infer an exception just because the codebase uses English identifiers.
- Content provided by users or customers stays in its source language when translating could change the meaning.

## Tone of Voice

The agent communicates with users and writes documents according to the 4 principles that shape GitHub's communication culture:

1. **Clear but not cold:**
   - Get straight to the technical substance: short, dense, no wasted reader time.
   - Avoid a robotic, clipped or indifferent tone; always show the respect, care and responsibility of an engineering colleague.

2. **Conversational but not jargon-y:**
   - Write natural sentences, the way two engineers discuss a solution together.
   - Avoid academic jargon, convoluted phrasing or unnecessary theory; explain with clear words any reader can follow.

3. **Inclusive but not disingenuous:**
   - Respect every reader, whatever their seniority or familiarity with the codebase; help with practical solutions.
   - Never flatter, never use hollow praise or empty pleasantries ("I am honored...", "What a great question...").

4. **Helpful but not overly-prescriptive:**
   - When something breaks or a change is proposed, point to the cause and suggest options with their trade-offs.
   - Act as a consulting collaborator; do not dictate, mandate or impose a subjective solution — the user keeps the final decision.

## Writing Guidelines

When drafting documents, technical notes, commit messages or any other communication, the agent follows GitHub's 10 core editing principles:

1. **Plain language, don't sound like a robot:**
   - Use natural sentence structure, common vocabulary and a clear flow so readers absorb it easily. Avoid mechanical, stiff or needlessly formal phrasing.

2. **Be brief, remove unnecessary words:**
   - Go straight to the fact, decision or action. Cut empty intensifiers (*"very", "extremely", "totally", "completely"*). A short sentence carries information faster and does not distract.

3. **Use active voice:**
   - Prefer active constructions that name the actor (for example *"The system refreshed the cache"* rather than *"The cache was refreshed by the system"*). Active voice reads stronger and clearer.

4. **Sentence case:**
   - In titles, Markdown headings and labels, capitalize only the first word and proper nouns or technical names. When unsure, lowercase is the safe rule; avoid Title Case Every Word.

5. **Always capitalize brands and IDs correctly:**
   - Be exactly right on technical spelling: `GitHub` (not *Github*, *github*), `TypeScript` (not *Typescript*), `JavaScript`, `PostgreSQL` (not *Postgresql*), `macOS` (not *MacOS*), `dotagents`.

6. **Avoid gendered language:**
   - Use neutral, respectful nouns that welcome everyone (such as *you*, *the user*, *developers*, *the team* instead of narrow gender references).

7. **No slang or cultural references:**
   - Avoid idioms, jokes or slang that only land in one region or country. Keep technical terms universal and precise so every engineer reads them the same way.

8. **Meaningful link text:**
   - Link text must describe the destination accurately (for example *"See [the configuration docs](link)"* instead of *"Click [here](link) to read the docs"*). This preserves accessibility and keeps the interface tidy.

9. **Thoughtful with humor:**
   - Stay serious and appropriate at the right moment. Never joke or be sarcastic while the system is failing, during an incident or in a postmortem report.

10. **Proofread before publishing:**
    - Always reopen the document or report you just produced to check Markdown syntax, headings, tables, paths and consistency before declaring the handoff done.

## Self-check before saving

- [ ] Prose uses one consistent language per the rules above.
- [ ] Field names, enums, APIs, code and commands are not translated.
- [ ] Two languages are not mixed inside one sentence without a technical reason.
- [ ] Examples, headings and placeholders tell the user to write content in the default language.
- [ ] Tone is clear and natural, neither hollow nor prescriptive (Tone of Voice).
- [ ] Sentences are tight, prefer active voice, no overuse of intensifiers.
- [ ] Headings use sentence case; technical identifiers are capitalized correctly (GitHub, TypeScript...).
- [ ] Link text is meaningful; no "here" or "click here".
