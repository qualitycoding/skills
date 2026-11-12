---
name: create-plan
description: Use when the user directs 'create a plan' (for example 'create a plan for X'); read and follow the planning protocol in github.com/qualitycoding/skills (protocols/planning-protocol.md) end to end, then stop once the plan is pushed.
---

# Create a plan

## Trigger
The user directs Claude to "create a plan", with or without a subject ("create a plan for the sitar release"). The phrase is an instruction to run the planning protocol, not a request for an informal outline in the reply. Do not use this skill for casual uses of the word, such as "what is your plan?" or "plan mode".

## What to do
Follow the planning protocol in `protocols/planning-protocol.md` of `github.com/qualitycoding/skills`, from Phase 0 to Phase 5, exactly as that file instructs. The protocol is the authority; this skill only gets it loaded and obeyed.

1. **Load the protocol from the repository, not from memory.**
   - If a clone exists (for example `/home/claude/skills`), run `git fetch origin main` and read the file at `origin/main`. If no clone exists, attach and clone `qualitycoding/skills` (shallow clone, one clone only).
   - Read the whole of `protocols/planning-protocol.md` (the core), not only the headings. Then, once intake has fixed the profiles and mode flags and 0.1 has fixed the environment class, read in full every module under `protocols/modules/` whose condition the core's Rule 0.7 table says is met. Record each file read and its version (the first line of each) in `plan/PROFILE.md` and in the plan's provenance.
   - Never rely on a remembered copy of the protocol, and never paste the protocol into this skill: a copy drifts from the source.
2. **Read the skills the protocol and its modules name** (for example `learning-exercise-site`, `audio-blind-listening-validation`, `mutation-testing-in-ci`, `mutation-sharding`) when the profile or mode flags chosen at intake call for them. They are in the same repository under `skills/`.
3. **Run intake as the protocol defines it.** Take the subject, profile and mode flags from the user's request. Where the protocol requires a question to be asked, ask it; do not guess values the protocol says must be confirmed.
4. **Carry out every phase the protocol requires for the chosen profile**: research, specification and freeze, plan construction, pre-mortem, and the push. Do not skip, merge or reorder phases to save time.
5. **Stop when the plan is pushed.** The protocol forbids executing plan steps. Do not start implementation, even if the plan looks quick to carry out.
6. **Report to the user**: the repository and generation branch pushed to, the commit hash, the core and module versions followed, the rigour level, the open human gates, and where the lessons and knowledge items were or will be pushed.

## Writing rules
- Write prose in British English (see the `proper-english` skill).
- Apply `timeless-skill-writing` to any wording that will outlive the session.

## If the protocol cannot be followed
If the repository is unreachable or a phase cannot be completed, say so plainly and stop at that point. Do not substitute an informal plan and describe it as the protocol's output.

## Keeping this skill current
Any edit to this skill is pushed to `qualitycoding/skills` (see `publish-skills-to-repo`).
