---
name: publish-skills-to-repo
description: Use whenever a skill, instruction, protocol or runbook is created or modified, including this one; commit and push it to github.com/qualitycoding/skills so the repo stays the single source of truth.
---

# Publish skills and instructions to qualitycoding/skills

## Standing rule
Every skill, instruction file, protocol or runbook that is created or modified in any session must also be committed and pushed to `github.com/qualitycoding/skills`. The rule covers this skill: any edit to it is pushed too. The repo is the single source of truth, and local or account-level copies are secondary.

## Where each kind of file goes
- Skill: `skills/<skill-name>/SKILL.md`, plus any `references/`, `scripts/`, `evals/` it needs.
- Protocol or longer operating procedure: `protocols/<name>.md`.
- Standing instruction that is not a skill: write it as a skill if it should trigger on a request pattern; otherwise put it in `protocols/`.

## Procedure
1. Make sure the repo is available. If `/home/claude/skills` (or the user's local clone) is absent, clone it once with `git clone --depth 1 https://github.com/qualitycoding/skills`. Before pushing from a shallow clone, run `git fetch origin main`.
2. Write or edit the files at the paths above. Front matter needs `name` (matching the folder) and `description` (says when to use it).
3. Apply `timeless-skill-writing` to the text before committing.
4. Update the README table row for the skill or protocol (add a row for a new one).
5. Commit with a message naming the skill and the change, then push to `main`, unless the user asks for a branch.
6. Tell the user the commit hash and the paths pushed. If the push fails, say so and keep the files in place; do not report success.

## Do not
- Push secrets, credentials or personal data.
- Leave a skill changed in a session but unpushed at the end of the task.
