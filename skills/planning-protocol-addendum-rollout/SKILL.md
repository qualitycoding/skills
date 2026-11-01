---
name: planning-protocol-addendum-rollout
description: Upgrade planning documents across a GitHub account or organisation by creating one protocol-gap addendum per code repository plus a central control document for a separate implementation agent. Use when asked to reconcile repositories with a planning protocol, audit plan versions across branches, create and push addendum plans, or repeat a cross-repository planning-protocol rollout without implementing the product plans.
---

# Planning protocol addendum rollout

Create and publish planning amendments only. Do not execute product plans, merge implementation branches, deploy, release, or publish packages.

## Inputs and fixed records

Resolve and record before auditing:

- `owner`: GitHub user or organisation.
- `skills_repo`: repository containing `protocols/planning-protocol.md` and its change/review record.
- `protocol_commit`: exact commit of the protocol used for the rollout.
- `target_version`: version parsed from the protocol title at that commit.
- `version_label`: `target_version` with any leading `v` removed; use it in artifact filenames.
- `exclusions`: protocol/skill source repositories, empty repositories, and any explicit user exclusions, each with a reason.
- `artifact_date`: UTC date used in branch and artifact names.

Use the credential supplied for the task for every write. Never place it in remote URLs, files, logs, commits, status ledgers, or final reports.

## Workflow

### 1. Inventory every repository and branch

1. Query the account endpoint appropriate to its type; if organisation lookup returns not found, test the user endpoint instead of concluding that the owner is absent. Paginate until exhausted.
2. Record name, default branch, fork/archived flags, primary language, size, and visibility. Include owned code forks unless the request excludes them. Exclude empty repositories explicitly; do not silently treat README-only repositories as empty.
3. Enumerate every branch. Planning may exist only on generation, review, remediation, or addendum branches. Do not equate the default branch with the normative planning branch.
4. Clone or fetch the branches needed for inspection. On transient Git transport failures, retry with HTTP/1.1 and bounded backoff. Reconcile remote state before repeating a write.

### 2. Select the normative planning baseline per repository

1. Find `HANDOFF.md`, `PLAN.md`, `plan/`, `docs/PLAN.md`, addenda, amendments, checkpoints, reviews, research, and frozen-test manifests on all candidate branches.
2. Select the branch containing the operative planning contract, considering addenda and remediation branches as well as generation branches. Record the selection rule and exact source commit. Do not choose solely by branch date or name.
3. Determine the baseline from explicit protocol declarations in the plan, handoff, checkpoint, and addenda. Reconcile contradictions and record the evidence. Use `unversioned` for planning without a protocol declaration and `none` when no protocol-based plan exists.
4. Record every planning root. A repository can contain multiple active plans, such as a root computational package and a nested plugin.
5. Read the protocol change record at `protocol_commit` and derive the ordered capabilities missing between baseline and target. Never compare versions as floating-point numbers: a version such as `3.10` is not `3.1`.

### 3. Build a rollout manifest

Create a local manifest with one entry per included repository:

```json
{
  "name": "example",
  "source_branch": "gen-YYYYMMDDTHHMMSSZ-example",
  "source_commit": "<40-char SHA>",
  "plan_roots": ["plan"],
  "baseline": "v3.1",
  "profiles": ["software"],
  "deploys": false
}
```

Add repository-specific platform, mutation-tool, hardware, deployment, and safety constraints. Preserve existing product decisions; do not infer expanded platform support from language alone.

### 4. Create one addendum per code repository

Write `ADDENDUM-PLAN-V<version_label>.md` at each repository root without replacing earlier plans or addenda. Follow [references/artifact-contract.md](references/artifact-contract.md).

Each addendum must:

- name repository, source branch/commit, baseline, target protocol/commit, profiles, deployment flag, and planning roots;
- list only the missing protocol capabilities while requiring a final full consistency check;
- preserve product scope, public interfaces, frozen expected behaviour, and human gates;
- provide sequential, resumable steps with dependencies, literal inputs/outputs, artifact post-conditions, checkpointing, failure rules, and human gates;
- cover every applicable target-protocol addition, including learning stores, reviews, honest verification, ephemeral execution, CI coverage, and mutation strategy when those sections exist in the target;
- pre-decide repository-specific CI coverage and mutation inclusion or a justified opt-out;
- end with independent cold read, pre-mortem, traceability, mechanical verification, retrospective, remote verification, and the protocol's learning-store gate;
- forbid product implementation and external actions.

For repositories with no protocol-based plan, direct the implementation agent to construct the missing planning layout from repository evidence and record defaults as assumptions/decisions. Do not disguise an absent baseline as a small version gap.

### 5. Create the central controller in the skills repository

Create versioned controller and status artifacts under `protocols/`:

- `planning-v<version_label>-addendum-control.md`
- `planning-v<version_label>-addendum-status.json`
- a mechanical verifier appropriate to the target protocol

The controller must link every addendum and specify queue order, exact source branches/commits, implementation branch naming, one-repository-at-a-time execution, resume behavior, source-drift blocking, push-after-step cadence, remote-SHA checks, per-repository completion, central status updates, and final-report requirements.

Use machine-readable statuses `pending`, `pass`, `blocked-source-drift`, `blocked-access`, `blocked-risk`, and `failed-verification`. A pass requires an implementation commit and evidence. A blocked row requires a precise reason and evidence; it never counts as a pass.

Add the controller and skill to the skills repository README tables.

### 6. Validate locally

1. Check repository count and uniqueness against the inventory and exclusions.
2. Verify each addendum names its manifest branch, source commit, baseline, target, and every planning root.
3. Verify each gap produces a step and all steps terminate with review, retrospective, and learning-store closure.
4. Run the bundled structural checker:

   ```sh
   python3 scripts/check_rollout.py \
     --manifest /path/to/rollout-manifest.json \
     --workspace /path/to/workspace \
     --control /path/to/skills/protocols/planning-v<version_label>-addendum-control.md \
     --status /path/to/skills/protocols/planning-v<version_label>-addendum-status.json
   ```

5. Inspect version-control status before staging. Stage only intended artifacts; restore unrelated working-tree changes. Scan all additions for credentials and secret patterns.

### 7. Publish and reconcile

1. Commit each addendum to its audited planning branch unless the user requested another branch. Commit controller artifacts to the skills repository's requested branch.
2. Before each push, verify the remote source branch matches the audited source commit. Never force-push. A mismatch blocks that repository instead of overwriting work absent from the audited source.
3. Push with the supplied credential, then compare remote branch SHA with local HEAD. After timeouts or transport errors, query the remote before retrying: the write may have succeeded.
4. If Git transport remains unreliable, use an authenticated GitHub contents write on the unchanged source branch. Record the resulting remote commit; do not claim it equals the unpushed local commit.
5. Verify remote file content, not only branch existence. Compare every published addendum and controller artifact byte-for-byte with the validated local artifact.

### 8. Stop and report

Report repository/addendum counts, exclusions, controller path, validation results, and publication commit or branch information. State that product execution has not occurred. Stop after publication; the controller is for a separate implementation agent.
