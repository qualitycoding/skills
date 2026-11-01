# Addendum and controller artifact contract

Use this contract with the target protocol at the rollout's pinned commit. The target protocol governs when a requirement differs from this template.

## Repository addendum

Start with this metadata:

```markdown
# Addendum plan — planning protocol <target_version>

**Status: READY FOR ADDENDUM IMPLEMENTATION**
**Repository:** `<owner>/<repo>`
**Planning source branch:** `<branch>`
**Audited source commit:** `<40-char SHA>`
**Planning baseline:** `<baseline>`
**Target protocol:** `<target_version>`, `<skills_repo>` commit `<protocol_commit>`
**Active profiles:** `<profiles>`; `software.deploys = <true|false>`
**Planning root(s):** `<plan roots>`
```

### Required sections

1. **Purpose and scope.** Amend planning only. Preserve product scope, interfaces, frozen expected behaviour, human decisions, and earlier plan history.
2. **Audited version gap.** Map each missing target capability to an amendment step. Treat capabilities outside the gap as present but verify them at closure; repair false baseline claims rather than hiding them.
3. **Global execution contract.** Require an implementation branch from the audited source, immediate push/remote verification after each step, execution/deviation/lesson records, secret exclusion, idempotent resume, and no external actions.
4. **Steps.** Use the target protocol's step template. Include opening source/access verification and a gap ledger before capability steps.
5. **Closure.** Require traceability, cold read, pre-mortem, honest freeze handling, mechanical verification, retrospective, learning-store gate, and verified remote implementation commit.

### Capability-step checklist

Derive the applicable subset from the protocol's ordered change record rather than copying version numbers from an earlier rollout.

- Learning: prior-knowledge load, lessons, knowledge, retrospective, closing gate.
- Checkpoints: full execution context, artifact hashes, atomic snapshots, zero-context resume.
- Review: assumption/premise audit, traditional review, adversarial review, mutation inclusion or opt-out.
- Honest verification: no swallowed failures, artifact post-conditions, gating budgets, bootstrapped baselines, command/pin evidence, deviation completeness.
- Environment: stable/ephemeral probe, durable state, restaging, resumable builds, immediate push verification.
- Store separation: distinct lesson and knowledge repositories in intake, checkpoint, handoff, and closing push.
- CI matrix: map every declared OS/architecture/runtime bound to a versioned job or explicit waiver; disable fail-fast; check label/action/pin existence.
- Mutation CI: price the job, choose incremental/scheduled/dispatch triggers, require one aggregator, calculate the score from a parseable report, enforce mutant-count post-conditions, prove the gate can fail, and pre-decide survivor handling.

For multiple planning roots, apply the gap ledger and final verifier to each root. Keep shared execution records at repository root and nested plan artifacts beside their respective plans.

## Central controller

Include these sections:

1. Mission, target protocol commit, inclusion count, exclusions, and status-ledger path.
2. Non-negotiable planning-only, credential, frozen-test, honest-evidence, and external-action rules.
3. Workspace setup, reading order, branch creation, resume, and ephemeral-environment procedure.
4. Exact verifier invocation for every planning-root shape.
5. Per-repository terminal-status and central-report procedure.
6. A queue table with sequence, repository, baseline, source branch, source commit, planning roots, and addendum link.
7. Final programme definition of done.

The controller guides implementation of the addenda; it does not authorise merging those implementation branches or executing product plans.

## Status ledger

Use one object per repository:

```json
{
  "sequence": 1,
  "repository": "example",
  "source_branch": "gen-example",
  "source_commit": "<40-char SHA>",
  "implementation_branch": "impl-addendum-<artifact_date>",
  "plan_roots": ["plan"],
  "status": "pending",
  "implementation_commit": null,
  "evidence": null,
  "note": null
}
```

Update one repository at a time. Commit and remote-verify each central status transition so another agent can resume without conversation history.
