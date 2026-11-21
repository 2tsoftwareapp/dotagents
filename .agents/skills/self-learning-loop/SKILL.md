---
name: self-learning-loop
description: "Automatically analyze and distill technical lessons after any turn/task with repeated failures, corrections or a new solution; generate and refine skills to accumulate knowledge for later sessions."
---
# Self-learning and skill distillation loop

## When to use
- When an error or command experiment fails $\ge 2$ times before you find a working fix.
- When the user responds with a correction or provides new business guidance/conventions.
- After completing a complex technical problem, resolving a hard root cause, or a process that does not exist in the skill library yet.
- When the user explicitly asks: "distill this into a skill", "/learn", or "save this process for next time".

## When not to use
- Routine interactions, simple documentation lookups or explanatory questions that produce no reusable knowledge.
- Problems that are one-off and temporary with no chance of recurrence.
- The solution has not been verified in practice (do not distill unverified hypotheses).

## Process
1. **Signal capture:**
   - Identify: (a) the initial symptoms/error, (b) the root cause, (c) the exact action/syntax that produced the successful result, (d) applicability conditions.
2. **Duplicate check & draft creation:**
   - Run the script that checks for duplicates and creates a draft in the staging directory:
     ```bash
     python3 .agents/scripts/skill-distiller.py \
       --name "<skill-name-kebab-case>" \
       --description "<Short description of purpose and trigger>" \
       --trigger "<Activation condition 1>" \
       --anti-trigger "<Case where it should not be used>" \
       --step "<Step 1>" \
       --step "<Step 2>" \
       --rule "<Safety rule>" \
       --gotcha "<Common pitfall>" \
       --code "<Command or sample code>"
     ```
   - If the script detects high overlap with an existing skill: open the old skill and add the gotcha/edge case instead of creating a duplicate.
3. **Draft quality verification:**
   - Run a dry-run check with the promote script:
     ```bash
     python3 .agents/scripts/promote-skill.py <skill-name-kebab-case> --dry-run
     ```
4. **Approval & promotion to the official library:**
   - Present a summary of the new skill to the user (or move it into the official library if already authorized):
     ```bash
     python3 .agents/scripts/promote-skill.py <skill-name-kebab-case>
     ```
   - Run the catalog integrity check:
     ```bash
     .agents/scripts/validate-skills.sh .agents/skills
     ```

## Rules
- **Quality over quantity:** Do not create junk skills for basic tasks already covered in the standard documentation.
- **Verification is mandatory:** Distill a solution only when you have real run evidence (tests pass, exit code 0).
- **Follow the naming standard:** The skill name must be kebab-case and match the directory containing the `SKILL.md` file.
- **Safe staging mechanism:** Every newly generated skill must go through `.agents/skills/.staging/` before promotion.

## Completion criteria
- The skill draft is created successfully and passes the `validate-draft-skill` and `validate-skills.sh` checks.
- Report clearly the path of the skill file that was created or updated.

## Related templates/references
- `.agents/template/skill/SKILL.md`
- `.agents/scripts/skill-distiller.py`
- `.agents/scripts/promote-skill.py`
- `.agents/scripts/validate-skills.sh`
