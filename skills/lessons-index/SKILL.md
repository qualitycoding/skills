---
name: lessons-index
description: Find and load relevant lessons from the generated index in the qualitycoding/Lessons repository (lessons/INDEX.md) and apply them to the current task. Use at the start of any task (before planning) in qualitycoding-related work, when the user mentions lessons, the Lessons repo, generated index, or when tags for a task need to be matched against stored lessons learned by past runs.
---

# Lessons index lookup

The private repository `qualitycoding/Lessons` stores lessons learned by past runs, one file per lesson under `lessons/<facet>-<value>/`. `lessons/INDEX.md` is a generated index (by `scripts/build_index.py`; never edit it by hand) mapping each tag to a list of entries:

```
## domain:audio

- [L-<timestamp>-<slug>](lessons/domain-audio/L-<timestamp>-<slug>.md) One-line title (High)
```

A companion private repository `qualitycoding/knowledge` holds facts (`knowledge/INDEX.md`, same format) for the same workflow.

## Matching rule (from the repo README)

Load a lesson when any of its `domain:` or `tech:` tags equals one of the task's tags, or it carries `applies:all`. Skip superseded and retired lessons. Read by severity, then most recent first.

## Workflow

1. **Tag the task.** Pick `domain:` and `tech:` tags for the current task from the controlled vocabulary in [references/taxonomy.md](references/taxonomy.md). The taxonomy may lag the repo; if unsure of valid tags, fetch `TAXONOMY.md` from the repo root.
2. **Look up.** Run the bundled script (it fetches the index, merges the requested sections with `applies:all`, dedupes, ranks by severity then newest first, and prints id/title/path):

   ```bash
   GITHUB_TOKEN=... python3 scripts/lessons_lookup.py --tags domain:audio tech:python
   ```

3. **Load.** Fetch the full lesson files with `--fetch` (use `--top N` to bound context). The script skips lessons whose frontmatter `status` is `superseded` or `retired`. Read each lesson's sections (Trigger, What went wrong, Correction, Prevention rule, Detection check) and apply its prevention rule during the task.
4. **Timing.** Do this at task intake, before planning — not after the work is done. If the store cannot be reached, say so and continue; never invent lesson contents.

## Authentication and access

- The repo is private. Use the GitHub token from the environment (`GITHUB_TOKEN`) or git credentials already configured on the machine. Never interpolate a token into a command line as an argument, never hardcode one in files (there is a standing lesson on this).
- raw.githubusercontent.com and git transport are intermittently blocked from sandboxes; the script uses the GitHub contents API with retries. If it still fails, fetch via the API manually.

## Adding new lessons

After a task, if the user wants a new lesson recorded: one file per lesson named `L-<UTC-timestamp>-<slug>.md` in the folder of its first `tech:` or `domain:` tag (`general` if none), frontmatter fields `id`, `title`, `status: active`, `severity`, `tags` (controlled vocabulary — add new tags to `TAXONOMY.md` in the same commit), then regenerate the index by running `scripts/build_index.py` and commit both together. Never put credentials, tokens or personal data in an entry.
