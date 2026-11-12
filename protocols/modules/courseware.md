# Planning protocol module: courseware (v1.0)

Read when the mode flag `courseware` is set (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

## Intake

* At intake (0.3.1), record the 3.11 intake decisions: target language and level, skills covered, session length, score scale and partial-credit rules, retry and persistence, register labelling, the content date and sources policy, the hosting target, and who will do the learner trial.
* If the content describes a changing world (news, prices, rules, results), also record the refresh cadence and what one refresh run adds; content that cannot go stale records `refresh: none` with the reason.

### 3.11 Learning-Exercise Pathway `[if courseware]`
Follow the skill `learning-exercise-site` (qualitycoding/skills). Correct-looking pages can still mark right answers wrong, carry out-of-date or invented content, or hide slang as neutral language; the plan makes each of these checkable.

1. **Hosting preflight.** At 0.1, probe every hosting action the plan needs (repository creation, Pages settings, reaching the published site). Anything the agent cannot do becomes a human action requested in the intake batch, with the exact setting; publication is verified through a reachable channel (for GitHub Pages, the `pages build and deployment` run for the pushed commit).
2. **Content.** Each theme or unit records its sources (title and URL) and the date its content describes, shown to the learner. Texts are original; quotations of real people are short and sourced; statements, feelings or plans are never invented for real people; invented material (dialogues, scripts) is labelled as written for the exercise. Every fact used in a question traces to a source (`C-###`).
3. **Register.** Every glossed term carries a register label (for example `slang`, colloquial, `idiom`); the plan states the label set, how labels render, and which tasks call for which register.
4. **Items and scoring frozen.** The plan freezes, as Phase 2 tests: the number of items and points per exercise, the item types, every partial-credit rule, the length bounds that make the intended session time, and a data validator that rejects an exercise whose own model answers or canonical sentences do not score full marks.
5. **Browser verification.** Browser tests answer every exercise correctly (full marks) and deliberately wrongly (a stated low ceiling), check persistence across reloads, retry, navigation through the whole sequence, and every speech path through a fake speech API, including the fallback when recognition is absent (Rule 14).
6. **`S-LEARN` contents.** After the implementation steps and `S-REVIEW`/`S-ADVERSARIAL`, before `S-RETRO`: CI green on the pushed commit, the deployment verified, phone-viewport screenshots inspected, then halt at `G-LEARN` with the evidence bundle and questions of the skill (time taken, wrongly scored items, speech on the learner's device, register labels, outdated or one-sided content). Responses: `proceed`, `iterate: <notes>` (at most 3 rounds; every wrongly scored item becomes a validator or test case before it is fixed), `proceed-with-rescope: <text>`, `stop`.
7. **Waiver.** Omitting the learner trial from a `courseware` plan needs a `D-###` giving the reason.
8. **Scheduled content refresh.** Unless intake recorded `refresh: none`, the plan includes `S-REFRESH` after `G-LEARN`: write the per-run checklist (`REFRESH.md`) into the project repository; add a live-site check run by the hosting platform (for GitHub Pages, a workflow on `deployment_status` that fetches every data file from the live site); create a cloud scheduled task at the recorded cadence whose prompt probes push access, follows `REFRESH.md` and reports; and tell the owner the first run time and the approval setting the task received. Each run is append-only (new unit with a new dated id first in the manifest; existing units and the ids that key saved scores are never changed), rotates topics, keeps two independent sources per fact, fails closed (publishes only when the validator and browser tests pass, fixes content rather than tests, stops after three attempts) and reports CI, deployment and live-check results for its commit. Creating the schedule is an external action: the `G-LEARN` evidence bundle names the task (cadence, prompt, notification and approval setting), and it is created only after a `proceed` response and a verified first deployment.

## Checks this module adds

### Cold read (3.6 step 2)

* `[if courseware]` `plan/PLAN.md` includes `S-LEARN` (3.11) before the closing steps, with the item and scoring rules, the validator rules, the browser-test list (including a wrong-answers-score-low check), the hosting preflight and the gate ID filled in, and `plan/GATES.md` defines `G-LEARN`, or the omission is recorded as a `D-###`.

### Pre-mortem lenses (4.2)

* `[if courseware]` Content currency and integrity (dated, sourced, nothing invented for real people); scoring fairness (a correct answer marked wrong, partial credit too generous); session length; register labelling; speech coverage per learner device and browser; persistence loss when the learner changes device; content going stale without a scheduled refresh, and a refresh run that breaks saved scores or publishes unverified content.

### Final check (5.1)

* `[if courseware]` that `S-LEARN` and `G-LEARN` exist (3.11) with the frozen item and scoring rules, the data validator, the wrong-answers check and the hosting preflight, or the omission is recorded as a `D-###`;
* `[if courseware]` that `S-REFRESH` exists with its cadence, `REFRESH.md`, live-site check and scheduled-task creation (3.11 item 8), or intake recorded `refresh: none` with a reason.
