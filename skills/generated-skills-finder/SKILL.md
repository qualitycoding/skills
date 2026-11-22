---
name: generated-skills-finder
description: Find and load lesson-derived skills from the generated-skills directory on the generated-skills branch of qualitycoding/Lessons, using its generated indexes (index/by-trigger.md, index/by-topic.md). Use at the start of qualitycoding-related tasks (before planning), when the user mentions generated skills, the generated-skills branch/directory, or when a task's situation should be checked against lesson-derived skills distilled from past runs.
---

# Generated-skills finder

The `generated-skills` branch of the private repository `qualitycoding/Lessons` holds `generated-skills/skills/`: lesson-derived skills, one per directory as `SKILL.md`, generated from lessons so the same mistakes are not repeated. The branch README says to start with:

- `generated-skills/skills/index/by-trigger.md` — find skills by situation (trigger table)
- `generated-skills/skills/index/by-topic.md` — browse by area (topic sections)

Both indexes are generated; never edit them by hand. Together they exceed 100 KB — do not load them whole into context; shortlist first.

## Skill file format

Generated skills use their own frontmatter (`title`, `topic`, `triggers`, `source_lesson`) — not the `name`/`description` agent-skill format — and body sections `Use when`, `Goal`, `Do`, `Avoid`, `Evidence to collect first`, `Related`. Treat them as instruction runbooks: read them and apply their Do/Avoid items; `source_lesson` points back to the lesson they were distilled from (see the `lessons-index` skill for the lesson store itself).

## Workflow

1. **Describe the task** in a few words covering the domain, the technology and the risky activity (freezing a target, measuring, tracking pitch, …).
2. **Shortlist** with the bundled script (keyword-scores every index entry, prints the ranked matches with trigger text and path):

   ```bash
   GITHUB_TOKEN=... python3 scripts/find_generated_skills.py --task "freezing loudness targets for a blind percussion test"
   ```

3. **Choose** from the shortlist by reading the trigger text: pick skills whose situation matches the current task, not merely whose words overlap. If the shortlist misses, re-run with different task wording or browse `by-topic.md` by area.
4. **Load** the chosen skills and apply them:

   ```bash
   GITHUB_TOKEN=... python3 scripts/find_generated_skills.py --task "..." --fetch --top 3
   GITHUB_TOKEN=... python3 scripts/find_generated_skills.py --fetch --paths skills/domain-audio/pitch-tracker-octave-errors/SKILL.md
   ```

5. **Timing.** Do this at task intake, before planning — not after the work is done. If the store cannot be reached, say so and continue; never invent skill contents.

## Authentication and access

- The repo is private. Use the GitHub token from the environment (`GITHUB_TOKEN`) or git credentials already configured on the machine. Never interpolate a token into a command line as an argument, never hardcode one in files.
- raw.githubusercontent.com and git transport are intermittently blocked from sandboxes; the script uses the GitHub contents API with retries. If it still fails, fetch via the API manually.
- If the indexes or the branch move, probe the repo (`git ls-remote` or the API) instead of assuming paths; if `generated-skills` is merged away, fall back to the lesson store on `main` via the `lessons-index` skill.
