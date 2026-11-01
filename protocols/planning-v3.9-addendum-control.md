# Control document — planning protocol v3.9 addendum rollout

**Status:** READY FOR CONTROLLED IMPLEMENTATION  
**Protocol:** v3.9, `protocols/planning-protocol.md` at source commit `ef99285404419153dd5f9aaae14f14bb53604a62`  
**Scope:** 33 code repositories under `github.com/qualitycoding`  
**Excluded:** `skills` (controller/protocol source) and `rainbow-machine` (empty repository; no code or planning baseline)  
**Machine-readable run state:** `protocols/planning-v3.9-addendum-status.json`

## Mission

Upgrade every listed repository's current planning to protocol v3.9 by executing its root `ADDENDUM-PLAN-V3.9.md`. This is a planning amendment programme, not a product implementation programme. Do not execute product steps, merge product branches, deploy, release, publish packages, submit anything, or invoke live external services.

A lower-capability implementing agent must follow this document literally. Read the protocol and the relevant addendum before changing a repository. All decisions and verification evidence belong in committed files, not chat.

## Non-negotiable rules

1. Process repositories in table order, one at a time. Do not run two agents in the same working tree. Sequential execution is the default; independent repositories may run concurrently only in separate clones with separate central-status updates reconciled before push.
2. Use the exact source branch and source commit in the table. A mismatch is `blocked-source-drift`: write the observed SHA in the central status `note`, continue with the next repository, and never overwrite or rebase away newer planning.
3. In each repository create or resume `impl-v39-addendum-20261102`. The first implementation commit must descend from the listed source commit. Do not commit amendment work directly to the source branch.
4. Execute every applicable `S-ADD-*` step in order. Commit and push after every successful step; compare `git rev-parse HEAD` with the remote implementation-branch SHA after every push. Retry transient failures with bounded backoff; visible failure after the last attempt.
5. Update `EXECUTION_LOG.md`, `DEVIATIONS.md`, `.checkpoints/state.json`, lessons and knowledge as required. Never commit credentials, tokens, secrets or personal data. Never swallow a load-bearing failure.
6. Preserve product scope, public interfaces and frozen expected behaviour. Refreeze only artifacts legitimately changed by an amendment, with a traceable decision. A challenge to product behaviour follows `TEST_CHALLENGE.md`; it is not fixed silently.
7. Reviews must be honest. Unavailable fresh-context review is a recorded substitution and risk, not an independent pass. Unrun mutation, code review, platform or hardware checks remain pending/blocked, never green.
8. G-003 controls publication to the separate `qualitycoding/Lessons` and `qualitycoding/knowledge` stores. Wait for sign-off before those pushes; use the protocol's bundle fallback if directed. Do not let store publication delay the repository amendment's completion record.

## Workspace and recovery procedure

1. Clone `qualitycoding/skills`, then every target repository into separate directories. Checkout each listed source branch. Keep the protocol source commit available for reference even if `skills/main` later advances.
2. For each repository, read in this order: this controller → root addendum → `HANDOFF.md` → base `plan/PLAN.md` (or the legacy plan named by the addendum) → v3.9 protocol sections named by the gap table.
3. Run S-ADD-000. If `impl-v39-addendum-20261102` already exists, resume its tip: validate checkpoint artifact hashes, inspect the last execution-log entry, reconcile any in-flight push, and continue at the first non-pass status row. Do not repeat a passed step.
4. On ephemeral infrastructure, keep all repositories and status on durable storage, restage tools each turn, restore executable bits, and move long builds/tests to their planned CI jobs. Never rely on a background process surviving a turn.
5. After S-ADD-090, run the verifier from this skills repository for each listed planning root:

   ```sh
   python3 protocols/v39_addendum_verify.py final --repo /path/to/target --plan-root plan
   ```

   Replace `/path/to/target` and `plan` with the actual values. For `Stream-of-consonance-vst`, run for both `plan` and `vst/plan`. A nonzero exit blocks completion until every reported artifact is fixed.

## Per-repository completion and central reporting

After S-ADD-100 verifies the remote implementation commit:

1. Update that repository's object in `planning-v3.9-addendum-status.json`: `status: pass`, exact `implementation_commit`, and `evidence` pointing to `ADDENDUM-V3.9-STATUS.md` and the verifier output.
2. Commit the central status change on branch `impl-v39-addendum-control-20261102` in `skills`, push it, and verify the remote SHA. Use one central commit per completed repository so the programme is resumable.
3. For a repository that cannot complete, set `status` to `blocked-source-drift`, `blocked-access`, `blocked-risk`, or `failed-verification`; record the precise evidence and continue with independent repositories. Never mark it pass.
4. When every row is `pass` or has an evidence-backed blocked state, write `protocols/planning-v3.9-addendum-final-report.md` listing passes, residual blocked rows, commits, open G-003 learning-store requests, and any Medium/Low risks. Commit, push and verify. Stop; do not begin product implementation.

## Repository queue

| # | Repository | Baseline | Source branch | Required source commit | Planning root(s) | Addendum |
|---:|---|---|---|---|---|---|
| 1 | `guitar-amp-vst` | v3.8 | `gen-20261027T120000Z-guitar-amp-vst` | `55a295296bead2b32652d23e987852a9ab869988` | `plan` | [addendum](https://github.com/qualitycoding/guitar-amp-vst/blob/gen-20261027T120000Z-guitar-amp-vst/ADDENDUM-PLAN-V3.9.md) |
| 2 | `audio-to-midi` | v3.6 | `addendum-20261101T033000Z-protocol-v3.6` | `549d0687f9466926a9cb3af2f6f327bdae03564e` | `plan` | [addendum](https://github.com/qualitycoding/audio-to-midi/blob/addendum-20261101T033000Z-protocol-v3.6/ADDENDUM-PLAN-V3.9.md) |
| 3 | `kimi-code-github-app` | v3.6 | `gen-20261028T232935Z-kimi-github-app-connector` | `61b6379cb6b3f9449e36da30ba64a61e5b34850a` | `plan` | [addendum](https://github.com/qualitycoding/kimi-code-github-app/blob/gen-20261028T232935Z-kimi-github-app-connector/ADDENDUM-PLAN-V3.9.md) |
| 4 | `microtonal-guitar` | v3.6 | `main` | `5a8b6e4e7ff3ac3cde052c66f4d013b146872186` | `plan` | [addendum](https://github.com/qualitycoding/microtonal-guitar/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 5 | `sing-vst` | v3.6 | `gen-20261004T095012Z-singing-voice-vst-pitch-lyrics` | `657cb1764f767cbedac0079bb8ce95786440eea8` | `plan` | [addendum](https://github.com/qualitycoding/sing-vst/blob/gen-20261004T095012Z-singing-voice-vst-pitch-lyrics/ADDENDUM-PLAN-V3.9.md) |
| 6 | `sonic-destruction-vst` | v3.4 | `gen-20261028T222647Z-geiger-vst3` | `8716e093903364fbe8f7cac67e6653f9cee91e53` | `plan` | [addendum](https://github.com/qualitycoding/sonic-destruction-vst/blob/gen-20261028T222647Z-geiger-vst3/ADDENDUM-PLAN-V3.9.md) |
| 7 | `trumpet-vst` | v3.2 | `gen-20261007T145241Z-trumpet-vst-plan` | `4f67cc4ea3df1a7e23650d7206d1400a0fb1db51` | `plan` | [addendum](https://github.com/qualitycoding/trumpet-vst/blob/gen-20261007T145241Z-trumpet-vst-plan/ADDENDUM-PLAN-V3.9.md) |
| 8 | `ariel-ignition` | v3.1 | `gen-20260930T084855Z-ariel-electronic-ignition` | `452ecea39985b9657c8edbf630fb475da3cc97e2` | `plan` | [addendum](https://github.com/qualitycoding/ariel-ignition/blob/gen-20260930T084855Z-ariel-electronic-ignition/ADDENDUM-PLAN-V3.9.md) |
| 9 | `audio-to-rocksmith` | v3.1 | `review/plan-v2-20260923T200925Z` | `065504cf5d8a37a60119c92cb45a5531b0dfb387` | `plan` | [addendum](https://github.com/qualitycoding/audio-to-rocksmith/blob/review%2Fplan-v2-20260923T200925Z/ADDENDUM-PLAN-V3.9.md) |
| 10 | `chinese-strings` | v3.1 | `gen-20261003T134254Z-chinese-strings-vst` | `35cc365580a77c6e27797bc278c8eeee6e0d58e6` | `plan` | [addendum](https://github.com/qualitycoding/chinese-strings/blob/gen-20261003T134254Z-chinese-strings-vst/ADDENDUM-PLAN-V3.9.md) |
| 11 | `clarinet-vst` | v3.1 | `gen-20261002T075147Z-clarinet-vst-plan` | `74fade60cbbb0eec9b34ca4b4d15133b30d823f0` | `plan` | [addendum](https://github.com/qualitycoding/clarinet-vst/blob/gen-20261002T075147Z-clarinet-vst-plan/ADDENDUM-PLAN-V3.9.md) |
| 12 | `oildrumkit-vcvrack` | v3.1 | `plan/v3.3-defect-remediation` | `96a00b653686cce5e0234e8dac07aca940536118` | `plan` | [addendum](https://github.com/qualitycoding/oildrumkit-vcvrack/blob/plan%2Fv3.3-defect-remediation/ADDENDUM-PLAN-V3.9.md) |
| 13 | `Rawksmyth` | v3.1 | `gen-20260923T152727Z-rocksmith-clone` | `9d43955e82cccb0cece7162b193dfddd0ab32284` | `plan` | [addendum](https://github.com/qualitycoding/Rawksmyth/blob/gen-20260923T152727Z-rocksmith-clone/ADDENDUM-PLAN-V3.9.md) |
| 14 | `refractor` | v3.1 | `gen-20260928T151837Z-refractor-rainbow-machine-vst` | `17f474850deb6bea728465098d34a14afb310295` | `plan` | [addendum](https://github.com/qualitycoding/refractor/blob/gen-20260928T151837Z-refractor-rainbow-machine-vst/ADDENDUM-PLAN-V3.9.md) |
| 15 | `Renault-diagnosticiser` | v3.1 | `gen-20260924T110646Z-renault-scenic-obd-reader` | `23f6a510d8686d61d45bf987335e03e30801f4e2` | `plan` | [addendum](https://github.com/qualitycoding/Renault-diagnosticiser/blob/gen-20260924T110646Z-renault-scenic-obd-reader/ADDENDUM-PLAN-V3.9.md) |
| 16 | `saxophone-vst` | v3.1 | `gen-20261001T211329Z-saxophone-vst-plan` | `cc53ac03b66dde0ef2a3078eb5fdda7dbbb1166d` | `plan` | [addendum](https://github.com/qualitycoding/saxophone-vst/blob/gen-20261001T211329Z-saxophone-vst-plan/ADDENDUM-PLAN-V3.9.md) |
| 17 | `tracer-diagnosticiser` | v3.1 | `gen-20260926T164526Z-tracer9gt-obd-reader` | `069cfff57e2e686e0b09739cab18b36d153aacba` | `plan` | [addendum](https://github.com/qualitycoding/tracer-diagnosticiser/blob/gen-20260926T164526Z-tracer9gt-obd-reader/ADDENDUM-PLAN-V3.9.md) |
| 18 | `oildrumkit` | unversioned | `main` | `35fbfead61a11a8c7f5609a95831a29f2cb2bf78` | `plan` | [addendum](https://github.com/qualitycoding/oildrumkit/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 19 | `stem-splitter` | unversioned | `main` | `b9173b7d80c0323b28bf69cfe09e8b6eb478bef9` | `plan` | [addendum](https://github.com/qualitycoding/stem-splitter/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 20 | `Stream-of-consonance` | unversioned | `main` | `9c8e5e10f467d695c31914034f4b6c4e265a6179` | `plan` | [addendum](https://github.com/qualitycoding/Stream-of-consonance/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 21 | `Stream-of-consonance-vst` | unversioned | `main` | `d4075852db02391ed0be2a25fd30132728279b99` | `plan and vst/plan` | [addendum](https://github.com/qualitycoding/Stream-of-consonance-vst/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 22 | `atmospheric-javascript` | none | `main` | `0d4e8d73863c93b24f0ca4b37e7cc113db3e00d7` | `plan` | [addendum](https://github.com/qualitycoding/atmospheric-javascript/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 23 | `AutoHedge` | none | `main` | `72a325b5ad7e41ccbe019b69f5ef9c5d13e50f26` | `plan` | [addendum](https://github.com/qualitycoding/AutoHedge/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 24 | `docplan-executor` | none | `main` | `6e2ea701d2b78f31c80aa59c86fc76f5c1f39c77` | `plan` | [addendum](https://github.com/qualitycoding/docplan-executor/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 25 | `functional-utils` | none | `master` | `e85c1348917499d4c75e83e0f3accf7bfb55d949` | `plan` | [addendum](https://github.com/qualitycoding/functional-utils/blob/master/ADDENDUM-PLAN-V3.9.md) |
| 26 | `invasion` | none | `main` | `4bea40b041643b5cfc9935abfb2d97183f6f8146` | `plan` | [addendum](https://github.com/qualitycoding/invasion/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 27 | `midi-generator` | none | `main` | `1940bc4b4cfe3cb5d77afffb072a418b3f64c86d` | `plan` | [addendum](https://github.com/qualitycoding/midi-generator/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 28 | `munch` | none | `main` | `e55f1b7814b7e6d759af9f8fcdaede28972e16b5` | `plan` | [addendum](https://github.com/qualitycoding/munch/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 29 | `nv-i18n` | none | `master` | `415547a5502789a0bcca21885b2be6017736432e` | `plan` | [addendum](https://github.com/qualitycoding/nv-i18n/blob/master/ADDENDUM-PLAN-V3.9.md) |
| 30 | `Playlists` | none | `main` | `7f12ea432d83af00d182ad494bd5fc41d7ca8d28` | `plan` | [addendum](https://github.com/qualitycoding/Playlists/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 31 | `reflection-utils` | none | `master` | `436e31aa75305e43985f844f77b08a6c48c5bd2e` | `plan` | [addendum](https://github.com/qualitycoding/reflection-utils/blob/master/ADDENDUM-PLAN-V3.9.md) |
| 32 | `side-splitter` | none | `main` | `c1e8525b2b84478abf288a5cce7ee4d5123949a6` | `plan` | [addendum](https://github.com/qualitycoding/side-splitter/blob/main/ADDENDUM-PLAN-V3.9.md) |
| 33 | `sitar` | none | `main` | `1d91a89ae26722718fc8362023fc3684493d5c17` | `plan` | [addendum](https://github.com/qualitycoding/sitar/blob/main/ADDENDUM-PLAN-V3.9.md) |

## Final programme definition of done

- All 33 repositories have an evidence-backed terminal status; every `pass` has a remote implementation commit descending from the exact audited source.
- Every passing repository has a completed addendum status log, v3.9 gap ledger, updated handoff/plan/traceability, split learning stores, honest reviews, an intake-derived CI matrix, and a v3.9 mutation design or explicit opt-out.
- Every planning root passes `v39_addendum_verify.py final`; no secret scan finding remains.
- Central status and final report are pushed and remote-verified. No product implementation, merge, deployment or release has occurred.
