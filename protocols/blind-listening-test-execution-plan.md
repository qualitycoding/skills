# Blind Listening Test Execution Plan

**Repositories:** `oildrumkit`, `sitar`, `chinese-strings`, `oildrumkit-vcvrack`
**Planning basis:** `qualitycoding/skills` planning protocol v3.10 §3.10 and `audio-blind-listening-validation`  
**Purpose:** execute repeatable listening gates whose records let a fresh implementation agent resume without asking for missing context.

## 1. Required outcome

Each repository must finish with either a signed gate response and an explicit downstream resume step, or a blocked/iterating state that names the missing prerequisite, next render/change, and next listening round. A folder of WAVs and a score alone is not completion.

For every scored round, preserve:

- repository, implementation branch, candidate source commit, gate ID, test type, and round number;
- prerequisites and frozen metric results;
- reference provenance, redistribution permission, and checksums;
- candidate render command or reproducible event/session inputs, render commit, and checksums;
- pair-builder commit, seed, window, duration, RMS, fade, and sample-rate settings;
- bundle/evidence location, evidence commit, and `SHA256SUMS`;
- ordered answers, score, exact one-sided binomial p-value, and side-bias observation;
- verbatim qualitative findings, measured follow-up differences, and targeted changes;
- gate response, response timestamp, next implementation step, and updated checkpoint/log commit.

No listening result may relax a frozen test, erase an unresolved earlier gate, rewrite a historical gate response, or establish a fidelity claim outside the comparison actually performed.

## 2. Repository scope and readiness

| Order | Repository | Integration branch | Listening integration | Entry condition |
|---|---|---|---|---|
| 1 | `chinese-strings` | `impl/v0` | Augment existing **G-003a**, then apply the same protocol to G-003b/c/d | `.impl/state.json` is at S-008 `awaiting-G-003a`; its non-blind evidence exists. Add the blind bundle without bypassing G-003a. |
| 2 | `oildrumkit-vcvrack` | new `impl/vcv-listening` from current `main` | Supplementary **S-LISTEN / G-LISTEN** for VST/Rack equivalence | Historical G-101 already says `proceed` and S-010 is complete. Validate the current remediated `main`, not the stale port tip; do not reopen G-101. |
| 3 | `oildrumkit` | new `impl/listening-validation` from current `main` | New realism **S-LISTEN / G-LISTEN** before S-RETRO | Current v3.9 layout does not authorize product execution. Make a listening-only amendment, secure real references, and retain all disclosed metric limitations. |
| 4 | `sitar` | new `impl/listening-validation` from current `main` | New realism **S-LISTEN / G-LISTEN** before S-RETRO | Current v3.9 layout does not authorize product execution. Add a listening-only amendment and a reproducible audio renderer before the gate. |

Repositories may proceed independently once their prerequisites are satisfied. New branches are specified only where no active product implementation branch remains; they hold listening amendments/evidence, not a competing product implementation.

## 3. Amend and freeze before listening

Before rendering a scored round, amend each repository’s own plan artifacts rather than treating this document as an implicit override:

1. Set `audio = true` in the active plan/profile and checkpoint mode flags.
2. Add or update `S-LISTEN` after implementation and applicable `S-REVIEW`/`S-ADVERSARIAL` steps and before `S-RETRO`. For chinese-strings, the family-specific listening work remains inside S-008/S-010/S-011/S-012.
3. Update `plan/PLAN.md`, `plan/GATES.md`, profile, decisions, traceability, and native checkpoint. Record each new comparison or branch with a `D-###`.
4. Freeze the reference set, metric suite, initial seed, onset-window requirement, pass condition, demos, gate questions, responses, three-round limit, evidence route, and downstream branch.
5. Run the repository’s normal unfreeze/red-verify/re-freeze process for any new numeric acceptance test. Never weaken an existing test to obtain a listening pass.
6. Commit and push each successful amendment chunk where authorized and verify the remote commit. Record blocked pushes honestly.

### Pair-tool prerequisite

The four replacement repositories do not currently expose the common `scripts/make_blind_pairs.py` and `scripts/score_blind.py` tools on the inspected implementation refs. Before S-LISTEN, vendor the canonical pair builder/scorer into each repository under `scripts/`, recording the source repository/commit and SHA256 in `plan/DECISIONS.md` and the round manifest. If another agent has already added them, verify the CLI and hashes instead of adding a duplicate implementation.

Required builder CLI:

```text
python3 scripts/make_blind_pairs.py --ref ref/ --cand cand/ --out blind/ \
  --seed N --pairs 12 [--window start|middle] [--seconds 1.0] \
  [--rms-db -23.0] [--fade 0.010] [--fs 44100]
```

Required scorer CLI:

```text
python3 scripts/score_blind.py --key blind/key.json.b64 --answers "A,B,..."
```

Use Python 3 with `numpy` and `soundfile`, plus `scipy` when resampling is required. Record the actual environment; do not claim a command was verified until it has run successfully on the pinned setup.

### Frozen common settings

| Setting | Frozen value |
|---|---|
| Primary scored set | 12 matched pairs |
| Primary window | `--window start`; an onset set is mandatory |
| Optional diagnostic set | Separately identified `--window middle` set; never pool it with the onset score |
| Clip length | 1.0 s by default; struck/percussive material may use a shorter interval only if frozen before listening |
| Level | Common RMS at −23 dBFS; retain pre-match level metrics so normalization cannot conceal level defects |
| Fades/output | 10 ms fades, 44.1 kHz PCM-24 WAV unless a repository freezes its working rate before pair construction |
| Numeric gate | At most 8/12 correct on the primary set |
| Qualitative gate | No unresolved finding material to the comparison; a numeric pass cannot override an adverse demo finding |
| Rounds | Maximum three total, including the initial round |
| Iteration seed | New, previously unused seed after every disclosed round |
| p-value | Report exactly; it does not replace the frozen ≤8/12 rule |
| Changes | General mechanisms only, never per-clip/per-note constants tuned to the pair set |

Initial seeds: `20261103` for oildrumkit, `20261104` for sitar, `20261105` for chinese-strings, and `20261106` for oildrumkit-vcvrack. For rounds 2 and 3, add 1000 and 2000 respectively. Record the actual seed in `result.json`. Chinese-strings uses the same base-seed rule independently within each family gate.

## 4. Common bundle and listening procedure

### 4.1 Prepare matched source clips

Create staging outside the public listener bundle:

```text
listening-work/<gate-id>/round-001/
  ref/                 # reference WAVs
  cand/                # candidate WAVs, identical stems
  blind/               # script output; key remains concealed
  events/              # reproducible demo event/phrase files
  demos/               # rendered demo WAVs
  listener-bundle/     # only material visible before answering
```

Every pair must represent the same instrument, note/phrase, preset, event stream, and duration. Match stems exactly. The builder samples matching stems and fails if fewer than 12 are available; do not silence that failure or substitute unmatched material.

Record source URL, licence, original checksum, trim/resample operation, and candidate render provenance before pair construction. Internal baseline renders used for equivalence tests must identify their source commit and renderer settings.

### 4.2 Build and inspect pairs

```bash
python3 scripts/make_blind_pairs.py \
  --ref listening-work/<gate-id>/round-001/ref \
  --cand listening-work/<gate-id>/round-001/cand \
  --out listening-work/<gate-id>/round-001/blind \
  --seed <frozen-seed> \
  --pairs 12 \
  --window start \
  --seconds 1.0 \
  --rms-db -23.0 \
  --fade 0.010 \
  --fs 44100
```

Post-conditions:

- exactly `pair-01-A.wav` through `pair-12-B.wav` exist;
- `key.json.b64` and `sources.json.b64` exist in concealed staging;
- all 24 clips decode and have the frozen format/duration;
- source identity has not been disclosed to the listener;
- settings, source/candidate manifests, script commit, and hashes are recorded.

The pre-answer listener bundle contains pairs, demos, attribution, instructions, and an answer sheet. It excludes the key, source mapping, candidate-identifying filenames, and source directories. After scoring, add the key/mapping to the archival evidence for that disclosed round.

### 4.3 Render demos

Define every demo as a text event/phrase file or reproducible host session plus exported parameters. Render headlessly where supported. Name outputs `demo-NN-topic.wav` and retain the exact input and render command. Demos remain mandatory when the A/B score passes because short matched clips do not expose all transitions, modes, rolls, or host behaviour.

### 4.4 Deliver evidence

1. Use a marker commit containing `[gate-evidence <gate-id>]`.
2. Build the listener ZIP/raw files in CI with a dedicated concurrency group.
3. Publish orphan branch `evidence/<gate-id>` with `SHA256SUMS` and attribution.
4. Put the ZIP URL, per-file raw URLs, evidence commit, and candidate commit in `GATE-<id>.md`.
5. Verify URLs and hashes from a fresh context. Never list an URL that was not produced.

For chinese-strings, retain its existing large-audio evidence-branch convention and add round directories rather than replacing the original G-003a files.

### 4.5 Listener instructions

Ask the listener to:

1. Use their own headphones in a quiet environment and keep playback volume unchanged across a pair.
2. Play pairs in numeric order, A then B, once each, without analysis tools or concealed metadata.
3. Record exactly one `A` or `B` per pair as the side believed to be the reference. For the Rack equivalence test, ask which side is the VST without revealing the mapping.
4. Answer demo and weak-spot questions in their own words, identifying demo numbers and timestamps where possible.
5. Submit answers before seeing the key, source identity, correctness, score, or prior-round answers.

Count same-side answers and note side bias. Near-total side bias is consistent with inability to distinguish sources and must not be discarded.

### 4.6 Score after answers are locked

Save the ordered answer string and submission timestamp, then run:

```bash
python3 scripts/score_blind.py \
  --key listening-work/<gate-id>/round-001/blind/key.json.b64 \
  --answers "<12 ordered A/B answers>"
```

Save complete stdout as `score.txt`. Verify that the reported one-sided value is:

```text
p = sum(C(n,k) for k = correct..n) / 2**n
```

Record `correct`, `total`, `p_value`, per-pair correctness, and side-bias count in `result.json`.

## 5. Decisions and iterations

### Proceed

`proceed` requires all prerequisites and applicable frozen metrics to pass or carry an existing explicit disposition; primary score ≤8/12; no unresolved material demo finding; complete evidence; and a response file naming the exact next step and checkpoint commit.

### Iterate

For `iterate` or a repository-specific change response:

1. Preserve the listener’s wording verbatim.
2. Analyze the reported region/mechanism. For onset complaints, inspect the first 50–200 ms; for rolls/transitions/host issues, inspect the corresponding scheduling, state, or rendering path.
3. Record measured differences and make one targeted general-mechanism change per difference.
4. Re-run affected frozen metrics and reviews. Do not relax thresholds.
5. Re-render all affected pairs/demos from the new candidate commit.
6. Use the next unused seed and repeat the same gate questions.
7. After round 3, permit only a genuine `proceed`, `proceed-with-rescope: <text>`, or `stop`; do not keep iterating.

### Rescope or stop

A rescope must name the narrowed claim/feature, affected docs/tests, and whether another round is required. `stop` leaves the checkpoint halted at the same gate with the evidence pointer and reason intact.

## 6. Required result layout and schema

```text
listening/<gate-id>/round-001/
  result.json
  answers.txt
  score.txt
  findings.md
  metrics.md
  provenance.md
  render-manifest.json
  SHA256SUMS
  iteration.md           # rounds 2–3
GATE-<gate-id>.md
GATE-<gate-id>.RESPONSE.md
```

`result.json` must contain at least:

```json
{
  "schema_version": 1,
  "repository": "",
  "branch": "",
  "candidate_commit": "",
  "gate_id": "",
  "round": 1,
  "test_type": "realism | implementation-equivalence",
  "status": "awaiting-listener | scored | iterating | proceeded | rescoped | stopped | blocked",
  "prerequisites": [{"id": "", "status": "", "evidence": ""}],
  "frozen_metrics": [{"id": "", "threshold": "", "observed": "", "status": "", "evidence": ""}],
  "reference": {"kind": "", "source_urls_or_ids": [], "licence": "", "checksums": ""},
  "candidate_renders": {"manifest": "", "checksums": ""},
  "pair_builder": {
    "script": "scripts/make_blind_pairs.py",
    "commit": "",
    "seed": 0,
    "pairs": 12,
    "window": "start",
    "seconds": 1.0,
    "rms_db": -23.0,
    "fade_seconds": 0.01,
    "sample_rate": 44100
  },
  "evidence": {"branch": "", "commit": "", "bundle": "", "sha256sums": ""},
  "answers": {"ordered": "", "submitted_at": "", "same_side_count": 0},
  "score": {"correct": 0, "total": 12, "one_sided_p": 0.0, "pass_condition": "correct <= 8 && no unresolved qualitative finding"},
  "qualitative_findings": [{"demo_or_pair": "", "verbatim": "", "disposition": ""}],
  "iterations": [{"finding": "", "measured_difference": "", "change": "", "commit": ""}],
  "response": {"value": "", "recorded_at": "", "file": ""},
  "resume": {"next_step": "", "checkpoint_file": "", "checkpoint_commit": "", "execution_log_commit": ""}
}
```

Do not replace native checkpoints with this schema. Add a pointer to `result.json`, set the repository’s native step/gate/status fields, and preserve existing run IDs, artifact hashes, and history.

## 7. `oildrumkit` — struck-steel realism

### Entry and plan integration

1. Create `impl/listening-validation` from current `main`; record the base commit. The old `modal-rewrite` implementation is already represented in `main`, so do not resurrect it.
2. Amend the current planning layout with listening-only authorization, `audio = true`, S-LISTEN after applicable reviews, and G-LISTEN before S-RETRO.
3. Preserve the retrospective’s disclosed limitations: no prior listening/real-recording comparison, only 2/4 original numeric targets passing, no DAW/Windows validation, and open engineering items. The listening amendment does not convert those items into passes.
4. Run current reproducibility/build/metric checks and record actual outcomes before pair construction.

### Comparison and assets

- **Type:** realism against redistribution-compatible recordings of real struck steel oil drums/barrels or closely matched struck sheet steel. Legacy-versus-current renders are useful demos but are not realism references.
- **Reference:** at least 12 matched hits across the kit’s representative families, with source URL, licence, and checksums. If real references cannot be secured, block the scored realism test and record a demos-only `D-###`; do not use the legacy synth as “real.”
- **Candidate:** current modal-engine renders using matched instrument, velocity, hammer, damping, pitch, strike, room, and seed settings. Record raw levels before RMS matching.
- **Primary set:** 12 onset pairs, initial seed `20261103`, ≤8/12 plus no unresolved realism finding.
- **Demos:** existing deterministic sections A–D (single hits, velocity ladder, groove, snare roll), plus hat choke, all hammer types, strike/damping/room controls, cymbal/ride sustain, and known cowbell behaviour.

### Gate questions

Ask which side is the real recording and whether each demo has convincing metallic ring, attack, decay, velocity response, roll variation, cymbal shimmer versus hiss, snare rattle, hat choke, stereo/room character, and cowbell partial structure. Require instrument and timestamp for every adverse finding.

### Responses and resume

- `proceed`: close G-LISTEN and resume **S-RETRO**, then the existing S-KNOW/G-003 closing sequence.
- `iterate: <notes>`: remain at G-LISTEN; adjust general voicing/physics in `Tools/voicing.json` or the relevant engine mechanism, regenerate/recalibrate, rerun metrics/reviews, and use a new seed.
- `proceed-with-rescope: <text>`: narrow the realism/instrument claim and update README/research limitations before S-RETRO.
- `stop`: halt at G-LISTEN with S-RETRO pending.

## 8. `sitar` — instrument realism

### Entry and renderer prerequisite

1. Create `impl/listening-validation` from current `main`; record the base commit.
2. Amend the planning layout with listening-only authorization, `audio = true`, S-LISTEN after implementation/reviews, and G-LISTEN before S-RETRO.
3. Run the existing 19-test suite and record the actual summary; green tests establish DSP properties, not realism.
4. Add a deterministic JUCE-free offline renderer if none exists. It must accept a text phrase/event file, sample rate, seed, raga/tuning, and parameter state, and write PCM WAV without host interaction. Freeze its CLI and event schema before listening.

### Comparison and assets

- **Type:** realism against redistribution-compatible sitar performances.
- **Reference:** at least 12 matched notes/phrases covering low/high register, meend, jawari buzz, chikari/jhala, and sustained sympathetic resonance; record source, licence, and checksums.
- **Candidate:** renderer output using matched pitch, phrase, pluck/mizrab hardness, jawari, tarab/raga, meend, and dynamics settings.
- **Primary set:** 12 onset pairs, initial seed `20261104`, ≤8/12 plus no unresolved realism finding. A separate sustained/middle set is diagnostic only unless separately frozen and scored.
- **Demos:** scale/short melody, fast passage, slow sustain, soft/loud plucks, low/high register, meend and legato transitions, jawari settings, sympathetic/tarab response, chikari drone and jhala, pluck positions, and each supported raga.

### Gate questions

Ask which side is the recorded sitar and whether demos show convincing pluck attack, jawari buzz, pitch/meend behaviour, sympathetic bloom, chikari/jhala rhythm, decay, stereo character, and dynamics. Identify any synthetic, overly clean, unstable, or wrongly pitched passage by demo/time.

### Responses and resume

- `proceed`: close G-LISTEN and resume **S-RETRO**, then S-KNOW/G-003.
- `iterate: <notes>`: change the general KS/jawari/tarab/meend/renderer mechanism implicated by the finding, rerun all affected tests, and present a new seed/round.
- `proceed-with-rescope: <text>`: narrow the realism/technique claim explicitly before S-RETRO.
- `stop`: halt at G-LISTEN with S-RETRO pending.

## 9. `chinese-strings` — staged family realism at G-003a–d

### Current entry and gate preservation

1. Use `impl/v0` and `.impl/state.json`; it is currently S-008 `awaiting-G-003a`. Do not start S-009.
2. Retain existing family gates and existing public G-003a renders. Add blind reference/candidate pairs and the common result record to G-003a; do not create a parallel gate or overwrite its original evidence.
3. Amend G-003a–d before the next scored round with `audio` semantics, ≤8/12 condition, three-round maximum, evidence marker, and common schema. Preserve DD-only tuning restrictions.
4. Existing `proceed-with-changes` remains the DD-tuning iteration response. Add `iterate` for findings requiring a general algorithm change and `proceed-with-rescope` for a narrowed claim. Algorithm changes require the normal plan/test amendment path, not undocumented DD edits.

### References and common assets

- **Type:** realism against redistribution-compatible recordings of each named Chinese instrument.
- **Reference:** matched performances for the instruments and techniques covered by the active family gate; source URL, licence, and checksums per file. Do not substitute a different instrument and call it equivalent.
- **Candidate:** `cs_render` output from the active implementation commit using the existing JSON phrases and recorded settings.
- **Primary set per active gate:** 12 onset pairs, base seed `20261105`, ≤8/12 plus acceptable per-instrument demos. Ensure the pair manifest identifies instrument/technique coverage so a family-wide score cannot hide a badly failing instrument.
- **Missing references:** block the affected scored realism comparison or record an explicit demos-only/rescope decision. Never silently score against placeholder voices.

### Family-specific demos and resume

| Gate | Candidate/demo coverage | Proceed resumes |
|---|---|---|
| **G-003a / S-008** | Eight bowed instruments: open strings, scale, legato, vibrato; include bow noise/cleanliness, yehu radiation, banhu level/colour, sihu string change and notes 54–56 | **S-009** |
| **G-003b / S-010** | Seven plucked lutes: open strings, chromatic run, tremolo/lunzhi, bend, harmonic, muted technique where supported | **S-011** |
| **G-003c / S-011** | Guzheng glissando/press-bend/yaozhi, guqin harmonics/slides, konghou bends and body coupling | **S-012** |
| **G-003d / S-012** | Yangqin single strikes across range, rolls/lunyin, damping, course detuning | **S-013** |

For every gate ask which side is the real instrument, whether each instrument is recognisable, and which DD row or general mechanism explains any retuning need. Preserve the existing weak-spot questions and report known issues even when the score passes.

### Responses

- `proceed`: mark only the active family gate/step complete and resume the exact step in the table.
- `proceed-with-changes: <instrument>: <DD field>=<value>; ...`: edit only the named DD rows under DR-10, re-render, rerun the suite, and re-open the same gate with a new seed; maximum three total rounds.
- `iterate: <notes>`: for non-DD findings, amend/freeze the required general mechanism work, implement and review it, then re-open the same gate with a new seed.
- `proceed-with-rescope: <text>`: record the narrowed instrument/technique claim and update the plan/docs before taking the proceed branch.
- `stop`: write the existing stop artifact and leave the next step pending.

Later family gates remain pending until their implementation step is reached; completing G-003a does not authorize jumping directly to G-003b/c/d evidence.

## 10. `oildrumkit-vcvrack` — VST/Rack implementation equivalence

### Entry and historical-gate boundary

1. Create `impl/vcv-listening` from current `main`, which includes the remediation state. Record the base and engine-submodule commits.
2. Historical G-101 contains a human `proceed` and S-010 completed. Do not reopen it, rewrite its response, or claim the new blind test happened before publication.
3. Add supplementary S-LISTEN/G-LISTEN after the applicable remediation/review checks. This is a post-G-101 validation amendment; no new release, tag, or VCV Library submission is authorized.
4. Re-run `tests/run_all.sh` and record `ALL FROZEN TESTS PASSED`, T-040/T-041 observations, SDK kind/hash, and current candidate commit before listening.

### Comparison and assets

- **Type:** implementation equivalence of the Rack module against the oildrumkit VST/engine reference, not a new realism test against physical drums.
- **Reference:** VST or canonical oildrumkit engine renders at the recorded source/submodule commit, using the same trigger schedule and settings.
- **Candidate:** Rack `KitCore`/module renders using identical trigger times, voltages/velocities, hammer, tuning, damping, strike, room, limiter, sample rate, and seed. Account explicitly for the fixed 128-frame latency before windowing.
- **Primary set:** 12 matched instrument/event onset pairs, initial seed `20261106`, ≤8/12 plus no unresolved equivalence finding, in addition to T-010/T-012 and the full frozen suite.
- **Demos:** existing `demo_48k.wav` pattern plus event-driven single hits at 3/6/10 V, dense roll/groove, closed-hat choke, all controls and CV, mono fold, reset/retrigger, and 44.1/48/96/192 kHz comparisons.

### Questions and responses

Ask which side is the VST and whether any instrument differs in attack, ring/decay, velocity/timbre, choke, control/CV response, stereo/mono behaviour, latency, crackles, or reset behaviour. Preserve the existing Windows/Rack checklist as host evidence; it is not replaced by the blind score.

- `proceed`: close supplementary G-LISTEN and resume the amended **S-RETRO**/close sequence. Do not rerun S-010 or create another tag merely because the gate passed.
- `iterate: <notes>`: correct wrapper scheduling/block/latency/parameter behaviour or another general divergence, rerun the frozen suite/reviews, and use a new seed. Keep the engine submodule unchanged unless a separately planned engine change is authorized.
- `proceed-with-rescope: <text>`: record the narrowed support/equivalence claim; any behaviour-changing rescope follows the existing re-planning rule.
- `stop`: halt at G-LISTEN with the close sequence pending and no external release action.

A passing result supports VST/Rack equivalence only. Physical-drum realism remains the separate oildrumkit G-LISTEN question.

## 11. Checkpoint and execution-log updates

After every bundle, score, response, or iteration:

1. Commit non-sensitive round records and gate updates on the integration branch.
2. Update the native checkpoint with active step/gate, round, status, evidence/result path, candidate commit, and next step.
3. Add an execution-log row with UTC time, step/gate, round, outcome, commit, evidence pointer, score/p-value when scored, and exact next action.
4. On `proceed`, complete only the listening gate/step and activate the downstream step named above. Never mark prerequisites complete retroactively.
5. On iteration, keep the gate open, record the next seed and required change, and leave the downstream step pending.
6. On missing references/renderer/prerequisites, use `status = blocked`; do not manufacture a score.
7. Push and verify each successful chunk where authorized; verify evidence and implementation branch commits independently.
8. From a fresh clone, confirm that the checkpoint, gate response, `result.json`, and linked plan/log identify the exact next action without prior chat.

## 12. Final cold-check

For each of the four repositories, verify:

- [ ] Correct repository/branch; no old-scope repository remains in the active plan.
- [ ] Earlier gates and incomplete implementation steps still block where applicable.
- [ ] `audio = true`, S-LISTEN position, gate definition, and downstream dependency exist in the repository’s own amended plan.
- [ ] Comparison is correctly labelled realism or implementation equivalence.
- [ ] Pair scripts are vendored/verified with source commit and hashes.
- [ ] Reference source/licence/checksums and candidate provenance are complete.
- [ ] Frozen quantitative tests remain intact and actual results are recorded.
- [ ] Twelve matched onset pairs, ≤8/12 condition, seed rule, and three-round limit are explicit.
- [ ] Listener bundle conceals key/source identity until answers are locked.
- [ ] Reproducible demos and weak-spot questions are present.
- [ ] Evidence marker, orphan branch, `SHA256SUMS`, and URLs are real and verified.
- [ ] Ordered answers, exact score/p-value, side-bias note, and verbatim findings are recorded.
- [ ] Qualitative findings can block an otherwise passing numeric score.
- [ ] Iterations name measured differences, general changes, new commits, and new seeds.
- [ ] Gate response uses allowed vocabulary and maps to the correct next step.
- [ ] Chinese-strings remains within G-003a–d ordering; VCV’s historical G-101 response is unchanged; VCV equivalence is not called physical-drum realism.
- [ ] Native checkpoint and execution log point to the same round, evidence, response, and resume commit.
- [ ] No credentials or personal data entered the evidence.

Completion means every repository is either advanced through its listening gate or left at a fully evidenced, resumable blocked/iterating state—not that all four are forced to return `proceed`.
