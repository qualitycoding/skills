# Planning protocol module: audio (v1.0)

Read when the mode flag `audio` is set (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

## Intake

* At intake (0.3.1), record the reference recordings, the licence of each, whether each is redistributable or a private reference (Rule 15), and who will listen.

### 3.10 Audio Listening Validation `[if audio]`
Follow the skill `audio-blind-listening-validation` (qualitycoding/skills). Metrics cannot replace a listener: the plan adds step `S-LISTEN` after the implementation steps and the `S-REVIEW`/`S-ADVERSARIAL` steps (when `software` is active) and before `S-RETRO`.

1. **Reference set.** Recordings chosen under Rule 15: redistributable ones wherever the search allows, and private references only under a `D-###`. Each is recorded with source, author, licence or terms URL, checksum and a `redistributable` flag; private references are linked, not stored in the repository, and are downloaded on demand. If no reference exists, record a `D-###` stating what the candidate is compared with instead (for example a competing tool's output), or that the blind test is replaced by demos only.
2. **Frozen thresholds.** Quantitative metrics for the reference comparison are frozen tests (Phase 2) before any listening. The listening gate never relaxes them.
3. **`S-LISTEN` contents.** The plan states: the blind-pair builder and its seed rule (a new seed after every round the listener has seen results for), at least one pair set cut from the start of each clip, the pass condition (for example the maximum number of correct picks out of 12), the demo list as event files rendered headlessly, the CI marker commit `[gate-evidence <gate-id>]` and orphan evidence branch, and the delivery URLs. When any reference is a private reference, the public evidence branch carries no reference-derived audio (the pairs included): it holds the demos, the link records and the hashes of the private files, and the pairs reach the listener privately (for example as files in the conversation).
4. **Gate.** `plan/GATES.md` defines the listening gate with the questions and responses of the skill (`proceed`, `iterate: <notes>`, `proceed-with-rescope: <text>`, `stop`, plus any named override). An `iterate` response runs the skill's iterate procedure; the gate allows at most 3 rounds, then escalates.
5. **Waiver.** Omitting the phase from an `audio` plan needs a `D-###` giving the reason (no audible output, no reference and no listener).

## Checks this module adds

### Cold read (3.6 step 2)

* `[if audio]` `plan/PLAN.md` includes `S-LISTEN` (3.10) before the closing steps, with the reference set, pass condition, demo list, gate ID and round limit filled in, and `plan/GATES.md` defines its gate, or the omission is recorded as a `D-###`.

### Pre-mortem lenses (4.2)

None beyond the core.

### Final check (5.1)

* `[if audio]` that `S-LISTEN` and its gate exist with a frozen pass condition (3.10), or the omission is recorded as a `D-###`.
