# Blind Listening Test Execution Plan

**Repositories:** `saxophone-vst`, `sing-vst`, `guitar-amp-vst`, `sonic-destruction-vst`, `Stream-of-consonance-vst`, `refractor`  
**Planning basis:** `qualitycoding/skills` planning protocol v3.10 §3.10 and `audio-blind-listening-validation`  
**Purpose:** execute repeatable listening gates whose records let a fresh implementation agent resume without asking for missing context.  
**Scope exclusion:** do not rerun or rebuild the existing `trumpet-vst` or `clarinet-vst` bundles.

## 1. Required outcome

Each repository must finish with either a signed gate response and an explicit downstream resume step, or a blocked/iterating state that names the missing prerequisite, the next render/change, and the next listening round. A folder of WAVs and a score alone is not completion.

For every scored round, preserve:

- repository, implementation branch, candidate source commit, gate ID, test type, and round number;
- all prerequisites and frozen metric results;
- reference provenance, redistribution permission or private/local status, and checksums;
- candidate render command or reproducible event/session inputs, render commit, and checksums;
- pair-builder commit, seed, window, duration, RMS, fade, and sample-rate settings;
- bundle/evidence location, evidence commit where public, and `SHA256SUMS`;
- ordered answers, score, exact one-sided binomial p-value, and side-bias observation;
- verbatim qualitative findings, measured follow-up differences, and any targeted change;
- gate response, response timestamp, next implementation step, and updated checkpoint/log commit.

No listening result may relax a frozen test, erase an unresolved earlier gate, or upgrade a product’s fidelity claim by itself.

## 2. Readiness and execution order

Work on the existing implementation branches. Do not create a replacement implementation line merely to hold listening evidence.

| Order | Repository | Existing branch | Listening integration | Current entry condition |
|---|---|---|---|---|
| 1 | `refractor` | `impl/refractor-v0.1` | Extend open **G-003** | Enter after S-013’s existing pre-gate checks; G-003 is already the listening/IP gate. |
| 2 | `sonic-destruction-vst` | `impl-run-20261028T222647Z-geiger-vst3` | Add amended **S-LISTEN / G-LISTEN** after reviews and before package refresh | Original implementation stages are complete and G-001 is already `approximation-only`; resume only at the newly inserted listening step. |
| 3 | `guitar-amp-vst` | `impl-run-20261027T120000Z-guitar-amp-vst` | Extend **G-010**, reached by S-015 | Complete unresolved review/host prerequisites and S-015 first. Final IR selection must be moved before tone approval as specified below. |
| 4 | `saxophone-vst` | `impl/saxophone-v1` | Use existing **G-003**, within S-016 | The checkpoint is awaiting earlier **G-004** at S-014. Resolve G-004 and complete S-015 before creating G-003 evidence. |
| 5 | `sing-vst` | `impl-gen-20261004T095012Z-singing-voice-vst-pitch-lyrics` | Augment existing **G-001** evidence in S-017 | G-004 hosted-GPU training must produce the evaluation renders. G-005’s `use-tiger` answer remains unchanged. Owner-local listening only. |
| 6 | `Stream-of-consonance-vst` | current VST implementation/default branch | Add VST-only **S-LISTEN / G-LISTEN** before S-RETRO | Complete the VST renderer and applicable S-009…S-018/review steps first. Root `plan/` product execution is not authorized. |

Repositories may proceed independently when their prerequisites are satisfied. The order above prioritizes actionable gates and avoids treating blocked repositories as failed listening tests.

## 3. Freeze the amendments before listening

Before rendering a scored round, amend each repository’s own plan artifacts rather than relying on this cross-repository document as an implicit override:

1. Set `audio = true` in the active plan/profile and checkpoint mode flags.
2. Add or update `S-LISTEN` after implementation and applicable `S-REVIEW`/`S-ADVERSARIAL` steps and before `S-RETRO`.
3. Update `plan/PLAN.md`, `plan/GATES.md` (or the repository’s existing gate section), traceability, decisions, and the checkpoint. Use a new `D-###` for each materially new comparison or changed ordering.
4. Freeze the reference set, metric suite, initial seed, onset-window requirement, pass condition, demos, gate questions, response vocabulary, three-round limit, evidence route, and downstream branch.
5. If new numeric acceptance tests are introduced, run the repository’s normal unfreeze/red-verify/re-freeze process. Do not edit a frozen manifest merely to make a failure disappear.
6. Commit and push each successful amendment chunk according to the repository’s access and external-action rules; verify the remote commit. Record any inability to push honestly rather than claiming evidence is available remotely.

### Frozen common settings

| Setting | Frozen value |
|---|---|
| Primary scored set | 12 matched pairs |
| Primary window | `--window start`; at least one onset set is mandatory |
| Optional diagnostic set | A separately identified `--window middle` set; never pool it with the onset score |
| Clip length | 1.0 s unless a repo-specific amendment freezes a shorter percussive/effect interval before listening |
| Level | Common RMS at −23 dBFS; retain pre-match level metrics so normalization cannot conceal a level defect |
| Fades/output | 10 ms fades, mono conversion as implemented by the script, 44.1 kHz PCM-24 WAV unless the repo freezes its working rate |
| Numeric gate | At most 8/12 correct for the primary 12-pair set |
| Qualitative gate | No unresolved finding that contradicts the gate’s purpose; a numeric pass cannot override an adverse demo finding |
| Rounds | Maximum three total, including the initial round |
| Iteration seed | New, previously unused seed after every disclosed round; record it before building the next bundle |
| p-value | Report exactly; it is evidence, not a substitute for the frozen ≤8/12 rule |
| Changes | General mechanism fixes only, never per-clip/per-note constants tuned to the test set |

Suggested initial seeds are `20261001` for saxophone (already planned), `20261102` for sing, `20261103` for guitar, `20261104` for sonic-destruction, `20261105` for Stream, and `20261106` for refractor. For rounds 2 and 3, add 1000 and 2000 respectively to the repository’s initial seed. The actual seed used remains authoritative in `result.json`.

## 4. Common bundle and listening procedure

### 4.1 Prepare matched source clips

Create owner-local staging directories outside the public listener bundle:

```text
listening-work/<gate-id>/round-001/
  ref/                 # reference WAVs
  cand/                # candidate WAVs, identical stems
  blind/               # script output; key remains concealed
  events/              # reproducible demo event files
  demos/               # rendered demo WAVs
  listener-bundle/     # only material the listener may see before answering
```

Every reference/candidate pair must represent the same note, phrase, preset, event stream, and duration. Match stems exactly. The builder samples matching stems and fails if fewer than 12 are available; do not silence that failure or substitute unmatched material.

Record source URL or private source ID, licence/consent, original checksum, trim/resample operation, and candidate render provenance before pair construction. For private voice material, use opaque stems and keep this provenance in the approved private location.

### 4.2 Build and inspect the pairs

From the repository root:

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
- `key.json.b64` and `sources.json.b64` exist in the concealed staging area;
- all 24 clips decode, have the frozen format/duration, and are non-silent unless silence is the intended matched event;
- the candidate/reference mapping has not been disclosed to the listener;
- source and candidate manifests, settings, script commit, and hashes are recorded.

The pre-answer listener bundle contains pairs, demos, attribution safe for disclosure, instructions, and an answer sheet. It does **not** contain the key, source mapping, candidate-identifying filenames, or rendered source directories. After scoring, the key/mapping may be added to the archival evidence for that disclosed round.

### 4.3 Render demos

Define every demo as a text event file or a reproducible host session plus exported event/parameters. Render headlessly where the repository supports it. Name outputs `demo-NN-topic.wav` and retain the exact input and render command.

Demos are mandatory even when the A/B score passes. They expose behaviour that one-second matched excerpts can miss: transitions, noise, underruns, dynamics, modes, expressiveness, and deterministic restart.

### 4.4 Deliver evidence

For public, redistribution-safe material:

1. Use a marker commit containing `[gate-evidence <gate-id>]`.
2. Build the listener ZIP/raw files in CI with a dedicated concurrency group.
3. Publish the orphan branch `evidence/<gate-id>` with `SHA256SUMS` and attribution.
4. Put the ZIP URL, per-file raw URLs, evidence branch commit, and source commit in `GATE-<id>.md`.
5. Verify that the URLs and hashes work from a fresh context. Never list a URL that was not actually produced.

For `sing-vst`, use the private route in §8 instead; do not create public voice-audio URLs.

### 4.5 Listener instructions

Ask the listener to:

1. Use their own headphones in a quiet environment and keep playback volume unchanged across a pair.
2. Play pairs in numeric order, A then B, once each, without inspecting filenames outside the listener bundle or using analysis tools.
3. Record exactly one `A` or `B` per pair as the side believed to be the reference. For equivalence tests, phrase this as “which side is the independent/baseline implementation?” without revealing which renderer is which.
4. Answer the demo and weak-spot questions in their own words, identifying demo numbers and timestamps where possible.
5. Submit answers before seeing the key, source identity, correctness, score, or prior-round answers.

Do not reject an answer pattern merely because it is biased. Count same-side answers and note side bias; near-total side bias is itself consistent with inability to distinguish the sources.

### 4.6 Score only after answers are locked

Save the ordered answer string and timestamp, then run:

```bash
python3 scripts/score_blind.py \
  --key listening-work/<gate-id>/round-001/blind/key.json.b64 \
  --answers "<12 ordered A/B answers>"
```

Save complete stdout as `score.txt`. Independently check that the score uses:

```text
p = sum(C(n,k) for k = correct..n) / 2**n
```

Record `correct`, `total`, `p_value`, all per-pair results, and the side-bias count in `result.json`.

## 5. Gate decision and iteration rules

### Proceed

`proceed` is valid only when:

- all prerequisites and frozen metrics pass or have an already recorded, applicable disposition;
- the primary score is ≤8/12;
- demo/weak-spot answers have no unresolved finding material to the test purpose;
- evidence and gate files satisfy the post-conditions;
- the response file names the exact next step and checkpoint commit.

### Iterate / calibrate

For `iterate: <notes>` or refractor’s existing `calibrate`:

1. Preserve the listener’s wording verbatim.
2. Analyze the reported region or mechanism. For onset complaints, inspect the first 50–200 ms for envelope, pitch, noise, transient, and high-frequency differences; for effect/equivalence complaints, inspect the corresponding routing/state/timing behaviour.
3. Record measured differences and make one targeted general-mechanism change per difference.
4. Re-run all affected frozen metrics and applicable reviews. Never relax them because of the listening result.
5. Re-render reference/candidate clips and demos from the new candidate commit.
6. Build a new bundle with the next unused seed and repeat the same gate questions.
7. Stop after round 3. The only permitted responses then are `proceed-with-rescope: <text>` or `stop`, unless the score and qualitative findings genuinely justify `proceed` without concealing residual differences.

### Rescope or stop

`proceed-with-rescope` must name the removed/narrowed claim or feature, affected files/tests/docs, and whether another listening round is required. It cannot convert implementation equivalence into hardware authenticity. `stop` leaves the checkpoint halted at the same gate with the reason and evidence pointer intact.

## 6. Required record layout and machine-readable schema

Use this layout on the implementation branch for non-sensitive records; put public audio on the evidence branch and private audio only in the approved private store:

```text
listening/<gate-id>/round-001/
  result.json
  answers.txt
  score.txt
  findings.md
  metrics.md
  provenance.md          # private provenance may be replaced by safe IDs + private pointer
  render-manifest.json
  SHA256SUMS
  iteration.md           # rounds 2–3: previous findings, measurements, changes, commits
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
  "test_type": "realism | singer-similarity | implementation-equivalence | rendering-regression",
  "status": "awaiting-listener | scored | iterating | proceeded | rescoped | stopped | blocked",
  "prerequisites": [{"id": "", "status": "", "evidence": ""}],
  "frozen_metrics": [{"id": "", "threshold": "", "observed": "", "status": "", "evidence": ""}],
  "reference": {
    "kind": "",
    "source_ids": [],
    "licence_or_consent": "",
    "redistribution": "public-evidence-allowed | private-local-only",
    "checksums": ""
  },
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
  "evidence": {
    "mode": "public-branch | private-local",
    "branch": "",
    "commit": "",
    "bundle": "",
    "sha256sums": "",
    "private_location_id": ""
  },
  "answers": {"ordered": "", "submitted_at": "", "same_side_count": 0},
  "score": {"correct": 0, "total": 12, "one_sided_p": 0.0, "pass_condition": "correct <= 8 && no unresolved qualitative finding"},
  "qualitative_findings": [{"demo_or_pair": "", "verbatim": "", "disposition": ""}],
  "iterations": [{"finding": "", "measured_difference": "", "change": "", "commit": ""}],
  "response": {"value": "", "recorded_at": "", "file": ""},
  "resume": {"next_step": "", "checkpoint_file": "", "checkpoint_commit": "", "execution_log_commit": ""}
}
```

Do not replace each repository’s native checkpoint with this schema. Add a pointer to the round’s `result.json`, set the native active step/gate/status fields, and preserve its existing run ID, history, artifact hashes, and branch convention.

## 7. `saxophone-vst` — realism calibration at existing G-003

### Entry and plan integration

1. Check out `impl/saxophone-v1` and restore `.checkpoints/impl-state.json`.
2. Do not start G-003 while the checkpoint says S-014 is `awaiting-gate` at **G-004**. Complete and record G-004 first.
3. Complete S-015: TinySOL/reference preparation, source/licence/checksum records, render tooling, and required metrics.
4. Amend S-016 only to make the blind protocol explicit; retain existing **G-003**, its demos, and its downstream S-017. Do not create a parallel gate.

### Comparison and assets

- **Type:** realism against licensed TinySOL reference recordings, not implementation equivalence.
- **Reference:** 12 or more matched saxophone notes/phrases covering the planned registers and playing conditions; record TinySOL source, licence, and checksums.
- **Candidate:** same notes/phrases rendered from the current instrument at the recorded commit.
- **Primary set:** onset, 12 pairs, initial seed `20261001`, ≤8/12 plus acceptable qualitative realism.
- **Demos:** reproducible event files for chromatic scale, short melody, fast passage, slow sustain, soft-to-loud dynamics, legato, vibrato, lowest/highest registers, Overblow, and Harmonic mode.

### Gate questions

In addition to ordered reference choices, ask: whether the demos sound like a saxophone; whether attacks/breath/noise/pitch settling reveal synthesis; whether legato and vibrato are convincing; and whether Overblow and Harmonic behaviour are acceptable. Require demo numbers/timestamps for adverse findings.

### Responses and resume

- `proceed`: mark G-003 and S-016 complete; checkpoint active step **S-017**; resume S-017.
- `iterate: <notes>`: remain in S-016/G-003, analyze and change the general mechanism, rerun metrics/reviews, and present the next seed/round.
- `proceed-with-rescope: <text>`: record the narrowed instrument/mode claim and affected tests/docs before entering S-017; do not silently ship a failed mode.
- `stop`: remain halted at G-003 with S-017 pending.

## 8. `sing-vst` — private target-singer comparison within G-001

### Entry and privacy boundary

1. Check out `impl-gen-20261004T095012Z-singing-voice-vst-pitch-lyrics` and restore its native checkpoint.
2. G-004 hosted-GPU training remains the active blocker. Complete the approved training/evaluation and produce converted and target renders before listening.
3. Preserve G-005’s answered `use-tiger` decision. Augment S-017/G-001; do not create a competing singer-similarity gate or retrain merely because a blind bundle was requested.
4. Voice recordings, converted/target renders, voice packages, credentials, singer-identifying metadata, and personal data remain owner-local with the required consent and private visibility. Public commits contain only safe scores, answers, comments, opaque IDs, checksums/provenance-safe metadata, response, and checkpoint state.

### Comparison and assets

- **Type:** target-singer similarity plus existing lyric-intelligibility/local-plugin evaluation; not a claim of consent or identity verification.
- **Reference:** owner-approved target-singer phrases, matched to converted lyrics/phoneme content and approximate pitch/rhythm.
- **Candidate:** current S-017 converted renders from the same input phrases.
- **Primary set:** 12 onset pairs where onset cutting is meaningful; if sustained phonemes are required, use a separately scored middle-window set. Do not combine window scores.
- **Demos:** reproducible lyric/pitch event inputs covering intelligibility, sustained vowels, consonants/onsets, pitch transitions, low/high notes, soft/loud phrases, and known weak lyrics.

### Private evidence procedure

Build the bundle locally and give the listener a local path or approved private transfer route. `evidence.mode` is `private-local`; public gate files say that audio is private and name only the private location ID and metadata commit. There are no public ZIP/raw URLs. The scorer runs locally; only non-sensitive result records are committed.

### Gate questions and resume

Ask which side is the target singer, whether lyrics are intelligible, whether voice identity/timbre is convincing, which words or phonemes fail, and whether local plugin playback reveals artefacts. Retain all existing G-001 metric thresholds and retrain/budget rules.

- `proceed`: mark the listening augmentation of G-001 satisfied and resume the existing S-017 post-G-001 step, not an earlier training decision.
- `iterate: <notes>`: follow the existing retrain/budget path, record the audible mechanism and new training/render commit, then use a new seed; maximum three listening rounds.
- `proceed-with-rescope: <text>`: narrow the stated singer/lyric/use-case claim explicitly and keep privacy constraints unchanged.
- `stop`: leave S-017/G-001 halted with the private evidence pointer and next required owner action.

## 9. `guitar-amp-vst` — realism and tone at G-010

### Entry and required ordering amendment

S-015 depends on S-014, S-REVIEW, S-ADVERSARIAL, and S-MUTATE; finish any unresolved findings and execute T-030…T-034 on Live 12 before G-010. The recent tree still lacks the complete S-015 Live record/render evidence, so the gate is not immediately ready.

The existing sequence places final factory IRs in S-016 after G-010 while S-015 would audition placeholders. Amend the plan before listening: move final original/CC0 IR selection, provenance, and a candidate render refresh into S-015’s pre-gate work; leave packaging/installers in S-016. G-010 therefore judges the actual tonal content intended for release. Record this ordering change as a decision and update traceability/checkpoint artifacts.

### Comparison and assets

- **Type:** realism/tone against matched real-amp/reference recordings, plus existing Live checklist and CPU evidence.
- **Reference:** redistribution-compatible recordings for representative voicings/presets, with source, licence, and checksums. Dry DI alone is not a realism reference. If suitable references cannot be secured, block the realism amendment or record an explicit demos-only/rescope decision; do not mislabel the test.
- **Candidate:** Live DI-loop bounces using the same DI performance, comparable amp/cab settings, final IRs, and recorded preset/state.
- **Primary set:** 12 matched onset pairs, ≤8/12, initial seed `20261103`. Retain unmatched level and noise measurements alongside RMS-matched clips.
- **Demos:** factory-preset clips plus reproducible DI/event inputs for clean edge-of-breakup, blues-rock attack, high-gain rhythm, fast palm mutes, sustained lead, soft/loud dynamics, all voicing transitions, gate open/close, sag, low end, cab/IR changes, and Eco/High modes.

### Gate questions

Preserve G-010’s goal question (“70s blues rock through high-gain black metal and beyond”) and add ordered pair answers plus weak spots: attack/transient shape, high-gain noise and gate chatter, sag/feel, low-end control, cab/IR character, voicing transitions, and any synthetic/fizz/caveat by preset and timestamp.

### Responses and resume

- `proceed`: complete S-015/G-010 and resume **S-016** packaging/provenance/installers. Since final IR selection moved earlier, S-016 verifies rather than silently replaces the approved tonal assets.
- `iterate: <notes>`: add this listening response alongside G-010’s existing rescope vocabulary; rework the named general DSP/IR/gate mechanism, rerun affected Live/frozen tests and S-015 renders, then present a new seed/round.
- `proceed-with-rescope: <text>`: implement the stated voicing/feature rescope, rerun S-015 for affected material, and re-present G-010 as the existing plan requires.
- `stop`: halt at G-010 with S-016 pending.

The stricter three-round listening limit and G-010’s existing additional-round language must be reconciled in the amendment to at most three total listening rounds.

## 10. `sonic-destruction-vst` — implementation equivalence only

### Entry and new gate

Do not reopen or rewrite G-001. Its `approximation-only` response and the absence of hardware captures remain authoritative; T-019…T-021 were not performed.

Add a planned **S-LISTEN** after S-REVIEW/S-ADVERSARIAL and before a refreshed S-PACKAGE, with new gate **G-LISTEN**. Because earlier stages already completed, resume at this new step, then refresh any package that predates the tested candidate. Public release remains subject to its existing release gate.

### Comparison and assets

- **Type:** implementation equivalence of current C++ against the independent Python/golden model. This is not realism and not evidence of WMD/Geiger pedal authenticity.
- **Reference:** independent Python/golden-model renders from recorded source commit and event/parameter inputs.
- **Candidate:** C++ renders from identical impulse/noise/ramp/sine and musical/event inputs, seeds, sample rate, state, and parameters.
- **Primary set:** 12 onset/event pairs, ≤8/12, initial seed `20261104`, in addition to—not instead of—existing exact/golden metrics.
- **Demos:** event-driven ZOH/sample-rate reduction, bit depth/mask/routing, preamp/tone/DC protection, procedural tables, noise seeded behaviour, bypass/state transitions, parameter extremes, and self-oscillation/harsh operating regions where applicable.

Any audible difference is an implementation finding even if the numeric score passes. Record pre-normalization level/timing differences because RMS matching can mask them.

### Responses and resume

- `proceed`: close G-LISTEN with test type `implementation-equivalence`; resume **S-PACKAGE** refresh, then the normal release/close sequence. Keep `approximation-only` in all product claims.
- `iterate: <notes>`: fix C++/model divergence, rerun golden/frozen tests and applicable reviews, render a new candidate, and use a new seed/round.
- `proceed-with-rescope: <text>`: narrow only an implementation behaviour/support claim; never upgrade hardware fidelity.
- `stop`: halt at G-LISTEN with package/release held.

Hardware authenticity still requires the original capture and fidelity path; no listening response in this runbook substitutes for it.

## 11. `Stream-of-consonance-vst` — VST/Python-oracle equivalence

### Scope and entry

Keep the two planning roots separate:

- Root `plan/` and `docs/LISTENING_PROTOCOL.md` describe a separate, not-yet-run 20+-listener pleasantness/perceptual study across timbres, tunings, and targets, with 1–7 ratings and mixed-effects regression. This A/B plan neither executes nor replaces that study.
- Root product execution is not authorized. Work only under `vst/plan/` when its VST implementation is authorized to continue.

The VST checkpoint has S-009 onward unfinished and the source tree does not yet contain the complete synth voice/plugin audio path. Complete S-009…S-018 and applicable host, performance, review, and frozen-test prerequisites before S-LISTEN; at minimum S-011 must produce real C++ audio, but an early renderer alone is not final gate readiness.

### Plan integration and comparison

Insert VST **S-LISTEN / G-LISTEN** after implementation/reviews and before VST **S-RETRO**. Do not add a consonance-model revalidation claim, which the VST plan excludes.

- **Type:** implementation equivalence against the Python `consonance/render.py` oracle.
- **Reference:** Python renders from identical fixture streams/events, PCG64 seeds, pitch sets, timbre, tuning, and render settings.
- **Candidate:** C++ VST offline/host renders from those same serialized inputs. Record any documented cross-library threshold deviation rather than hiding it through clip selection.
- **Primary set:** 12 onset pairs, ≤8/12, initial seed `20261105`, alongside existing fixtures and deterministic tests.
- **Demos:** short melody, fast passage, sustained notes, dynamics/register extremes, pitch modes, consonance range, note transitions, MPE behaviour, transport/deterministic restart, and underrun/soak scenarios.

### Questions and resume

Ask which side is the Python oracle and whether any demo differs in pitch stream, timbre, onset/transition, level, noise, continuity, or restart behaviour. Pleasantness ratings are not part of this gate.

- `proceed`: close VST G-LISTEN and resume **S-RETRO**, followed by the existing S-KNOW/G-003 closing sequence.
- `iterate: <notes>`: correct the general C++ rendering/stream/state mechanism, rerun fixtures and host/performance tests, and re-present with a new seed.
- `proceed-with-rescope: <text>`: explicitly narrow VST behaviour/platform claims and update docs/tests before S-RETRO.
- `stop`: halt at VST G-LISTEN with S-RETRO pending.

The root perceptual protocol remains an independent pending item regardless of this gate’s result.

## 12. `refractor` — rendering regression plus character/IP at G-003

### Entry and comparison

Enter existing **G-003** only after S-013’s pre-gate verification. Retain its character/IP questions, response vocabulary, and calibration semantics. Add the blind comparison as regression evidence, not as a realism test against a dry input.

- **Type:** rendering regression/equivalence between an immutable last-known-good baseline and the current candidate.
- **Reference:** baseline renders from a recorded accepted source/render commit using identical event files and settings. If no accepted baseline exists, create one from the designated last-known-good source commit before listening; never substitute dry input and call it pedal fidelity.
- **Candidate:** current S-013 renders at the recorded commit.
- **Primary set:** 12 onset/event pairs, ≤8/12, initial seed `20261106`, plus existing deterministic/numeric checks.
- **Demos:** existing chorus, slapback, harmony, Magic modes, self-oscillation, and bass demos, rendered from reproducible event/parameter files. Include bypass/transitions and parameter smoothing if covered by S-013.

The gate continues to state that no reference pedal captures exist. A passing score means no detectable baseline regression; it does not establish authenticity to the original pedal.

### Questions and responses

Preserve the IP sign-off and pedal-character questions. Add baseline-side answers and ask whether any demo shows a rendering regression in pitch, timing, modulation, feedback, noise, level, transitions, or stereo behaviour.

- `proceed`: close G-003 and resume **S-014**.
- `calibrate`: treat as the skill’s iteration response; record listener wording and measured baseline differences, make targeted general fixes, rerun S-013 checks, and reopen G-003 with a new seed. Maximum three total rounds.
- `proceed-with-rescope: <text>`: record the narrowed feature/character claim and required S-014 changes; do not claim pedal authenticity.
- `stop`: remain halted at G-003 with S-014 pending.

## 13. Checkpoint and execution-log update procedure

After every bundle, score, response, or iteration:

1. Commit the non-sensitive round record and gate update on the implementation branch.
2. Update the native checkpoint with active step `S-LISTEN` or the repository’s existing host step, gate ID, round, status, evidence/result path, candidate commit, and next step.
3. Add an execution-log row containing UTC time, step/gate, attempt/round, outcome, commit, evidence pointer, score/p-value when scored, and exact next action.
4. For `proceed`, mark only the listening gate/step complete and set the downstream step named in the relevant runbook. Do not mark intervening prerequisites complete retroactively.
5. For `iterate`/`calibrate`, keep the gate open, record the next seed and required mechanism change, and do not set the downstream step active.
6. For blocked prerequisites, set `status = blocked` with the missing gate/step/render/reference; do not manufacture a listening score.
7. Push and verify each successful chunk where authorized. Confirm evidence branch and implementation branch commits independently.
8. Test zero-context resumption from a fresh clone: read only the checkpoint, gate response, `result.json`, and linked plan/log artifacts; identify the exact next command/step without the prior chat.

## 14. Final cold-check before declaring the plan complete

For each of the six repositories, verify mechanically:

- [ ] Correct repository and existing implementation branch; trumpet/clarinet untouched.
- [ ] Earlier gates and incomplete implementation steps remain blocking where applicable.
- [ ] `audio = true`, S-LISTEN position, gate definition, and downstream dependency are in the repository’s own plan artifacts.
- [ ] Test purpose is correctly labelled realism, singer similarity, implementation equivalence, or rendering regression.
- [ ] Reference source/licence/consent/checksums and candidate provenance are complete.
- [ ] Frozen quantitative tests remain intact and have recorded results.
- [ ] Twelve matched onset pairs, frozen ≤8/12 condition, initial seed, new-seed rule, and three-round limit are explicit.
- [ ] Listener bundle conceals key/source identity until answers are locked.
- [ ] Reproducible event-driven demos and weak-spot questions are present.
- [ ] Public evidence marker/orphan branch/`SHA256SUMS`/URLs are real, or sing’s private-local route is explicit.
- [ ] Ordered answers, exact score/p-value, side-bias note, and verbatim findings are recorded.
- [ ] Qualitative findings can block an otherwise passing numeric score.
- [ ] Iterations name measured differences, general changes, new commits, and new seeds.
- [ ] Gate response uses the repository’s allowed vocabulary and maps to the correct next step.
- [ ] Sonic-destruction remains `approximation-only`; refractor makes no pedal-authenticity claim; Stream’s perceptual study remains separate.
- [ ] Native checkpoint and execution log point to the same round, evidence, response, and resume commit.
- [ ] No secrets, private voice audio, credentials, or personal data entered public evidence.

Completion means every repository is either properly advanced through its listening gate or left at a fully evidenced, resumable blocked/iterating state—not that all six are forced to return `proceed`.
