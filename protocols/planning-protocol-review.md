---
# Planning protocol: change and review record

Current version: **core v4.0** (`planning-protocol.md`) with modules v1.0 (`modules/*.md`), recorded 2026-11-12.
Status: **Round 16 completed — core and modules, rigour levels, integration step, gate records, untrusted-content rule, protocol self-measurement and simpler checkpoints, from a ranked review of v3.15.** Previous: Round 15 completed — scheduled content refresh for courseware: content about a changing world is refreshed by a scheduled, append-only, fail-closed task following a checklist kept in the project repository (3.11 item 8, step `S-REFRESH`; skill `learning-exercise-site` section 10).** Previous: Round 14 completed — mutation sharding: an over-budget mutation job is split into a generated per-file or per-module matrix with CPU, memory, parallelism and step limits, bounded three-attempt tool installation, per-shard report gates and a completeness-checking aggregate job (new skill `mutation-sharding`).** Previous: Round 13 completed — project nature and reference material: the protocol states that it builds hobby projects, prefers redistributable reference material, and lets hobby projects link to restrictive reference material instead of republishing it (new Global Rule 15).** Previous: Round 12 completed — source register: every external source checked in the research rounds is listed, with its content and licence, as one knowledge item pushed to the knowledge store (new step `R7`).** Previous: Round 11 completed — learning-exercise pathway: scored practice material (language exercises, quizzes, courses) as a gated, verifiable pathway (new mode flag `courseware`, new skill `learning-exercise-site`).

## Requested changes (v3.15 → core v4.0, modules v1.0)

Requested by the run owner: "Read the planning protocol … and rank all the ways you would improve it", answered with ten ranked proposals with full text; then "Apply all the proposals and push".

**Version class: MAJOR** (Rule 0.8). Rule 16 is a safety rule and Rule 0.8 itself changes what a version means. **Plans needing an addendum: not decided in this change.** Unfinished plans built under v3.x keep running under the version they record; whether any of them should take Rule 16 or the 3.3 gate record by addendum is an open decision for the owner (below). No addendum programme was started.

| Proposal (rank) | Where it lives |
|---|---|
| 1. Planner/implementer boundary: the final check required review reports that only implementation writes; the handoff omitted rules and templates the implementer must use | 1.1 layout (`reviews/` empty, `plan/TEMPLATES.md`, `scripts/check_knowledge_schema.py`); 3.5; 3.6 check; 3.7.1 implementation results header; 5.1 and 5.2 (via `modules/software-ci.md`) |
| 2. Rigour level | Rule 0.6; 0.3.1; 0.3.6; R5; R7 and termination criteria; 3.6; 4.5; 4.6; 4.7; Phase 5 report |
| 3. Integration | New 3.12 `S-INTEGRATE`; Rule 10 `G-INT`; 0.1 permission probe; 0.3.1; 3.5; 3.6; 3.7; 4.2 lens; 5.1 |
| 4. Core plus modules, versions, volatile facts | Rules 0.7 to 0.9; `protocols/modules/` (eight files); 0.2 tiers `T1`–`T4`; change history moved here (below); runner labels, action tags, billing notes, environment classes and the model-tier map moved to five knowledge items in `qualitycoding/knowledge` |
| 5. Pre-mortem convergence | Phase 4 items made headings 4.1–4.6; 4.3 failure path, likelihood, known risks, mitigation cost; 4.4; 4.5; Phase 5 report |
| 6. Untrusted content | New Global Rule 16; 3.5; 4.2 lens; Phase 5 report |
| 7. Gate record | 3.3 template and rules; Rule 10 |
| 8. Simpler checkpoint | 1.2.1–1.2.3 replaced; `.checkpoints/RESUME.md`; snapshots dropped |
| 9. Protocol feedback | 3.7.1 question 6; Appendix C `kind:protocol` and protocol lessons |
| 10. Precision fixes | Rule 2; Rule 4 tie rule; independence of sources (1.3 termination criteria); 1.3 note on 1.3.6; horizontal rule moved after Rule 16; Phase 4 numbering; the "Global Rule 5" citation corrected in the v3.2 → v3.3 table below |

Departures from the proposal text, each because the text as proposed would not have worked:
- **A `figures` module** (`computational` or `publication`) holds 2C. The proposal put 2C in `computational`, but a `publication`-only plan needs it too.
- **Only the listed sections move.** The proposal moved every bullet tagged for one profile; that would have scattered the `[software]` lenses, intake and tests across a module meant for CI. Text outside the listed sections stays in the core with its tags, and R2b (`[math, publication]`) stays in the core.
- **Pointer headings.** Each moved section leaves its heading and a pointer in the core, so references by number (for example "3.10" in two skills) still resolve.
- **3.12 item 7** (deployment needed earlier) was added: a courseware learner trial needs the site deployed, which can depend on the default branch that `S-INTEGRATE` merges into. 3.7 accordingly says the plan "includes" `S-INTEGRATE` rather than that it ends with it.
- **0.1 load order.** Environment-class knowledge items are read before the probe only where the knowledge store is already readable; store access is checked later, in 0.3.7.
- **Checkpoint fields** `rigour` and `diagnostic` (the 0.1 results) were added to the proposed `state.json`.

Measured effect of the split (words read, counted from the files): v3.15 17,385; core 14,710. A `software` plan reads 16,357 (−5.9 %); `software` + `audio` 16,853 (−3.1 %); `software` + `courseware` 17,248 (−0.8 %); `math` + `computational` + `publication` 18,074 (+4.0 %, because `computational` implies `software`). The proposal estimated about a fifth less for a software plan; the new rules added about 1,500 words and absorbed most of the saving. Section 3.8 still restates much of the two mutation skills; trimming it to what the plan must record is the remaining saving.

Checks run: every edit was applied by script with an assertion that its target occurred exactly once. A reference checker resolves every section, rule, phase and appendix reference in the core and modules (0 unresolved; the same checker finds the two broken references in v3.15, "Phase 4.4" and "4.6"). The five knowledge items pass the knowledge store's schema script. **None of the new text has been followed in a planning run.** The savings expected from rigour levels (proposal 2) and the pre-mortem change (proposal 5) are reasoned from loop bounds; the 3.7.1 question 6 table is how later runs will show whether they hold.

Found while moving facts: the v3.15 statement that the Claude cloud sandbox is `stable` conflicts with two existing knowledge items recording `/home/claude` work directories vanishing between turns. The moved item records the conflict; the 0.1 probe decides per run.

## Requested changes (v3.14 → v3.15)

Requested by the run owner after asking how often the `qualitycoding/swedish-exercises` pages regenerate (answer: never by themselves — a static site changes only when something is pushed, so the news-based content had been frozen at its launch date): set up an automatic refresh, and add it to the planning protocol so future similar projects refresh automatically.

| Request / observed gap | Where it lives |
|---|---|
| Courseware about current events had no plan for staying current | Intake 0.3.1 records the refresh cadence or `refresh: none` with a reason; 3.11 item 8 adds `S-REFRESH` |
| A refresh must not break learners' saved scores | 3.11 item 8: append-only units with new dated ids; existing ids never change |
| An unattended run must not publish broken or unverified content | 3.11 item 8: baseline check, validator and browser tests before push, content fixed rather than tests, three-attempt stop, CI + deployment + live-site check reported |
| The live site cannot be loaded from the agent sandbox | Live-site check workflow on `deployment_status`, read through the Actions API |
| Nothing checked that a courseware plan carried the refresh | 5.1 final check; Phase 4 lens |

Reference implementation: `REFRESH.md` and `.github/workflows/live-check.yml` in `qualitycoding/swedish-exercises`, and a weekly cloud scheduled task (Saturdays 10:32 Europe/London, push notifications). Its first run had not happened when this round was recorded.

## Requested changes (v3.13 → v3.14)

Requested by the run owner: when mutation testing must be split into shards to complete inside budget, record the procedure in enough detail to follow reliably; consider rewriting the mutation workflow into a per-file matrix with memory and CPU caps; treat Mull installation taking tens of minutes instead of under one minute as an indication of flaky network and retry with three bounded install attempts and a step limit.

| Request | Where it lives |
|---|---|
| Split an over-budget mutation suite into shards | New skill `mutation-sharding` (`skills/mutation-sharding/SKILL.md`), sections 1–2; 3.8 `S-MUTATE` requires a generated per-file or per-module matrix when the priced job exceeds budget |
| Per-file matrix with memory and CPU caps | Skill sections 2–3 and `references/per-file-matrix.yml`; 3.8 `S-MUTATE` records shard grouping and caps; 3.9 item 7 places the shard matrix on pinned Linux runner labels with matching inventory |
| Flaky network indicated by a tens-of-minutes Mull install | Skill section 4: exactly three attempts, each bounded, with sleep only between attempts and a hard stop after the third failure |
| Step limit | Skill sections 3–4 and the matrix template: job timeout plus explicit shell `timeout` for install and mutation-run steps |
| Shard results cannot be silently incomplete | Skill sections 5–6: per-shard report gates, always-uploaded artifacts, and an aggregate job that checks expected report count before scoring |
| Planning protocol references the new skill | Title/version bump; 3.8 `S-MUTATE`; 3.9 item 7 |

Skill files: `skills/mutation-sharding/SKILL.md`, `references/per-file-matrix.yml`.

## Requested changes (v3.12 → v3.13)

Requested by the run owner: make it clear from the outset that the protocol is used to create a hobby project, and that reference material need not be republished in the repository, although a reference to its origin must then be provided; material can be downloaded into the sandbox on demand; redistributable references are to be preferred over more restrictive ones; for freely redistributable material the existing protocol is acceptable.

Interpretation recorded: "from the outset" is read as a statement at the top of the protocol plus an intake field (`project.nature`, default `hobby`). "Reference material" is read as material the work is compared against or learns from, not material copied into the deliverable (that still needs a licence compatible with the target repository). "Strive for redistributable" is read as an ordered search with a recorded justification (`D-###`) before any restrictive source is used. The private route is for personal download and use only; it never circumvents a paywall, login terms or an automated-access ban, and it still requires a named author and original source page.

| Request | Where it lives |
|---|---|
| Hobby project stated from the outset | Opening statement; intake 0.3.1 `Project nature`; Rule 15 |
| No need to republish references; give their origin | Rule 15 *Private reference* (a) to (e): link record with URL, author, licence or terms URL, date, sha256; never committed or published |
| Download into the sandbox on demand | Rule 15 (d): download outside the working tree, check the sha256; the human downloads where the sandbox cannot reach the site |
| Prefer redistributable | Rule 15 *Redistributable first*: ordered search, searches logged, `D-###` for any shortfall; R7 route per source; Phase 5 report counts |
| Redistributable material stays as before | Rule 15; 3.10 item 1 |
| Safety | Fail-closed `redistributable` flag with a test that can fail (Rule 14); 3.10 evidence branch omits reference-derived audio when any reference is private; 5.1 final check |

Added beyond the request: a `never used` list (unknown licence, no named author or original source, terms that bar personal use), because a licence label on a re-hosting page that names no creator grants nothing; a `commercial` setting that turns the private route off; and a hash-mismatch stop so that a changed source is never silently accepted.

Checks run: the new text was applied first to the oildrumkit listening-phase plan (decision D-020, tests T-L08b, T-L08d and T-L16, 21 frozen tests green on a reference implementation and 19 red on stubs). Rule 15 itself has not yet been followed in a complete planning run.

## Requested changes (v3.11 → v3.12)

Requested by the run owner: at the end of the research round, all external sources checked should be listed with their content, licensing and so on as a knowledge item and, ultimately, posted to the knowledge store.

Interpretation recorded: "the research round" is read as the end of the research loop (the last round), with each round logging its sources as it goes so nothing is lost if a round is interrupted. "Listed as a knowledge item" is read as one item per run, a table with one row per source, rather than one item per source; per-source facts that the run relies on remain ordinary knowledge items under Rule 12. A source counts as checked whether or not it was used.

| Request | Where it lives |
|---|---|
| List every external source checked | `Sources checked` section in each round log (1.3); R7 step 1 collects from round logs, `research/SOURCES.md`, `claims.json`, `NOVELTY.md`, 1.3.6 locators and spike downloads |
| With their content | R7 step 2: content in the agent's own words, outcome, and the claims supported or contradicted |
| With licensing, etc. | R7 step 2: licence as SPDX identifier or named terms, where it was read, permitted use, compatibility with the target repository's licence for reused material, access notes. `none stated` is recorded as all rights reserved, never as permissive |
| As a knowledge item | Rule 12 bullet; Appendix B register template; new `kind:source-register` tag (Appendix C); passes the existing schema check unchanged |
| Ultimately posted to the knowledge store | `knowledge/` already travels to the store at `G-003`; 3.7.2 now names the register in the gate record and in its done-when |
| Nothing checked that it happened | R7 review (live spot-check of licences) and completeness check; termination criteria; 3.7.1 retrospective question 5; 5.1 final check; Phase 5 report line |

Added beyond the request: R0 step 5 lets a later run use the register as a map of sources already evaluated while counting it as zero sources towards corroboration, so a register cannot launder a claim into `corroborated`; sources checked after R7 are appended by the agent that checked them; unknown licence on reused material is a High risk.

Checks run: the Appendix B register example was extracted from the protocol and passed the Appendix C schema script (exit status 0). The R7 procedure itself has not yet been run in a planning run.

## Requested changes (v3.10 → v3.11)

Requested by the run owner after building `qualitycoding/swedish-exercises` (Swedish current-affairs exercises: 6 themes × reading, listening, writing, speaking; scored out of 10, retryable, scores saved between visits, GitHub Pages): encapsulate everything done in that run as a new pathway in the planning protocol, backed by a skill.

Observed in that run: repository creation and the Pages settings API were refused by the session proxy, so both had to be requested from the owner mid-run; the published `*.github.io` site could not be loaded from the sandbox, so deployment was verified through the Actions runs list; a first theme draft omitted the slang labels the request required; a listening script attributed invented words and plans to a real athlete until a sentence-by-sentence source check removed them; a keyword stem of one letter would have accepted any spoken answer; DOM `append` calls given arrays silently dropped content; a lockfile generated next to a symlinked `node_modules` recorded a local link and failed CI.

| Request / observed failure | Where it lives |
|---|---|
| No pathway for scored learning material | New mode flag `courseware` (Rule 0), intake decisions in 0.3.1, new section 3.11 with step `S-LEARN` and gate `G-LEARN` (3.3) |
| Repository creation and Pages settings discovered as blocked mid-run | 0.1 permission probe names repository creation and settings such as Pages; 3.11 item 1 hosting preflight and verification channel |
| Out-of-date, uncited or invented content; slang not labelled | 3.11 items 2–3; skill sections 3–4; Phase 4 lens |
| Answer keys that mark correct answers wrong; one-letter keyword stems; session length | 3.11 item 4 (frozen item and scoring rules, data validator); skill sections 5 and 8 (`scripts/validate.mjs`) |
| Browser and speech paths untested; checks that cannot fail | 3.11 item 5: fake speech API, correct → full marks and wrong → low ceiling, fallback path (Rule 14) |
| Nothing checked that a learning plan carried the pathway | 3.6 cold-read check and 5.1 final consistency check |

Skill files: `skills/learning-exercise-site/SKILL.md`, `scripts/scoring.js`, `scripts/validate.mjs`, `references/theme-schema.md`, `evals/evals.md`. The validator and scoring functions were run in the reference repository (24 exercises valid; 38 unit and browser tests passing locally and in CI); the learner-trial gate is defined but was not yet run with a learner.

## Requested changes (v3.9 → v3.10)

Requested by the run owner after the trumpet-vst implementation run: the phase in which blind listening comparisons and demo listening were performed must be an explicit part of any plan that generates audio or audio tooling, reproducible through a skill and linked from the planning protocol.

Observed in that run: objective realism metrics passed while a listener could still pick out the real recording in most blind pairs, by the start of each clip; the metrics-only view missed a synthetic-sounding pedal tone that listening to the demos found; a leaked answer key (the listener was told which pairs were right) forced a new seed; delivering the evidence for phone listening needed a CI-built orphan branch and a zip URL.

| Request / observed failure | Where it lives |
|---|---|
| No listening phase in plans for audio work | New mode flag `audio` (Rule 0), new 3.10 step `S-LISTEN` before the closing steps, intake line in 0.3.1, listening gate in 3.3 |
| Procedure for the blind test, demos, evidence delivery, gate questions, scoring and iteration was only in one project's records | New skill `audio-blind-listening-validation` (`SKILL.md`, `scripts/make_blind_pairs.py`, `scripts/score_blind.py`, `evals/evals.md`) |
| Nothing checked that an audio plan carried the phase | 3.6 cold-read check and 5.1 final consistency check |

Scripts were run against synthetic tones (same seed gives an identical key; a key-matching answer sheet scores all pairs correct); the end-to-end flow with a real instrument was observed in the trumpet-vst run, not re-run from the skill.

## Requested changes (v3.8 → v3.9)

Requested by the run owner after the guitar-amp-vst implementation run: record the recommended approach for running mutation testing in CI as a skill and reference it from plan creation.

Observed in that run: a mutation job that took 66 to 150 minutes on every push, including pushes that changed only documentation or workflow files; a job that stayed green for several runs without executing a mutant (a runner error swallowed by `|| true`, then a tolerance option that made the tool's threshold flag inert, so a 37.7 % score passed); and a score of 74.1 % against a 75 % floor, one test from failing every run.

| Request / observed failure | Where it lives |
|---|---|
| No guidance on when a mutation job should run; it ran on every push regardless of what changed | New skill `mutation-testing-in-ci` (three tiers: incremental PR/push runs on changed files, scheduled full run, on-demand dispatch; aggregator job as the only required status; no `paths:` filter on a workflow whose status is required); 3.8 `S-MUTATE` pre-decides the trigger strategy |
| Cost was never estimated before the job was wired in | 3.8 `S-MUTATE`: measured baseline test time, mutant count, estimated job time against a stated runtime budget; skill section 1 |
| A mutation gate that could not fail (swallowed runner error; tolerance option disabling the threshold) | 3.8 `S-MUTATE`: score computed from the report file, post-conditions (report exists, minimum mutant count), shown once to fail (Rule 14); skill section 3 with `scripts/mull_score.py` |
| Floor set at the achieved score; omitted slow tests silently lowered the score | 3.8 `S-MUTATE`: floor below the first real score; each omitted test a `D-###` |
| Mutation job treated like a per-platform matrix entry | 3.9 item 7: single pinned Linux runner, own trigger strategy |
| Nothing checked that the plan carried the strategy | 3.6 cold-read check and 5.1 final consistency check |

Skill files: `skills/mutation-testing-in-ci/SKILL.md`, `scripts/mull_score.py`, `scripts/mull_include_paths.py`, `references/example-mutation-workflow.yml` (the working workflow from guitar-amp-vst; not-applicable and incremental paths observed, full-run and schedule unobserved).

## Requested changes (v3.7 → v3.8)

Requested by the run owner: extend the protocol so plans consider CI platforms beyond a Windows/Linux/macOS matrix — the extras identified for GitHub Actions (ARM64 runners, libc-variant containers, oldest-toolchain jobs, QEMU-VM guests such as the BSDs and Solaris/illumos, emulated CPU architectures) — and investigate adding Android and iOS.

| Request / observed mismatch | Where it lives |
|---|---|
| Plans defaulted to a `windows/linux/macos` matrix; ARM64 runners, musl/libc-variant container jobs, and oldest-supported-toolchain jobs were never considered | New 3.9 CI Platform Matrix `[software]`, items 1–3 (versioned runner labels instead of `-latest`; labels and action pins existence-checked per 1.3.6, examples date-stamped "verified 2026-11") |
| BSDs, Solaris/illumos, and exotic CPU architectures had no planned route into CI | 3.9 item 4 (pinned `vmactions/*-vm` QEMU guests on Ubuntu runners; build-only QEMU user-mode for riscv64/s390x/ppc64le; anything else needs a self-hosted runner recorded at intake) |
| No guidance for mobile projects: Android | 3.9 item 5 (JVM unit tests vs instrumented tests; pinned `reactivecircus/android-emulator-runner` on a KVM-enabled Linux runner; matrix over the intake's supported API levels) |
| No guidance for mobile projects: iOS | 3.9 item 6 (macOS runners only; pinned Xcode; explicit `simctl boot` + `bootstatus -b`; `CODE_SIGNING_ALLOWED=NO` for simulator tests; signing/TestFlight in a `G-002`-gated release workflow; macOS-minute cost split recorded as a `D-###`) |
| Nothing verified that intake's supported platforms were actually exercised in CI | Coverage mapping (3.9 item 1) wired into the 3.6 cold-read mechanical check, the Phase 4 `[software]` lens list, and the 5.1 final consistency check |

## Requested changes (v3.6 → v3.7)

Requested by the run owner: lessons learned under the protocol must ultimately live in the existing `qualitycoding/Lessons` repository, not in the same default store as factual knowledge items.

| Request / observed mismatch | Where it lives |
|---|---|
| The protocol's default store sent lessons and knowledge items to one repository, while the Lessons repo is the canonical lesson store | Title/version bump; Global Rule 13 renamed **Lesson & Knowledge Stores** with default lesson store `Lessons` and default knowledge store `knowledge`; 0.3.1 intake default, 0.3.6 readiness check, 0.3.7 access check, checkpoint schema (`lesson_store`, `knowledge_store`), R0 wording, HANDOFF restatement |
| Gate `G-003`/`S-KNOW` treated lessons and knowledge as one push target | Rule 10 `G-003`; 3.7.2 splits the closing push into lesson-store and knowledge-store pushes, with separate index regeneration, retry limits, and bundle fallbacks |
| Appendix C described a single combined store layout | Appendix C now documents the split `Lessons` and `knowledge` repo layouts, generated indexes, schema scripts, and store-specific matching |

## Requested changes (v3.5 → v3.6)

Hardening from the sonic-destruction-vst implementation run in a heavily recycled
Kimi-cloud sandbox (~16+ container recycles in one session), requested by the run
owner. Scope rule from the request: the recycling protections apply **only** on
environments that actually recycle (observed: Kimi on cloud; Kimi on localhost
unknown → treat as ephemeral; Claude on cloud/remote observed stable → N/A), while
pushing to the remote after every successful chunk is **active on all platforms**.

| Request / observed failure | Where it lives |
|---|---|
| Sandbox containers recycled mid-run: `/tmp`/`/var/tmp` wiped, staged toolchains lost, background processes reaped at call boundaries/deadline kills; builds exceeding a container lifetime could never finish (ASan build never completed) | 0.1 execution-environment class probe (`stable` vs `ephemeral`, with observed class table); new 1.5 Ephemeral-Environment Protections `[ephemeral]` (durable-surface rule, turn-start restaging with exec-bit restoration, checkpointed resumable builds, ordering invariants learned from real failures, right-sizing steps to container lifetimes, CI for long work); 3.4 resiliency hook |
| Exec bits stripped on every copy from the fuse mount; restored binaries refused to run until re-chmodded | 1.5 item 2 |
| Dependency source-dir overrides passed as env vars were silently ignored by CMake; configure re-touched generated headers and invalidated precompiled objects | 1.5 item 4 |
| A long verification dimension (ASan+UBSan fuzz) could not complete locally and risked being silently treated as green | 1.5 items 5–6 (environment-blocked + CI-named, never reported as a pass) |
| Remote could drift from local when pushes were batched; a PAT died mid-run and work queued unpushed | Global Rule 6 push cadence `[All]`: commit-and-push after every successful chunk on **all** platforms, with `ls-remote` verification, backoff retries, and mismatch reporting |

Supporting change: Rule 0.3 gains the `[ephemeral]` environment tag; 3.5 HANDOFF
restates Rule 6 (with push cadence) alongside Rules 11–13.

## Requested changes (v3.4 → v3.5)

Hardening from the first implementation run of a v3.4 plan (guitar-amp-vst): review found "green" CI that had not verified anything.

| Request / observed failure | Where it lives |
|---|---|
| A CI job stayed green because `|| true` swallowed a tool's bad-flag error, and a later upload step found no report | Rule 14 (no swallowed failures; artifact post-conditions); 3.1 Done-when post-conditions; 3.6 and 5.1 idiom checks; severity rubric: silently-green verification is Critical |
| A bench step was informational, so a 15% CPU budget failing by >2x on one platform never gated | Rule 14 (budgets gate; per-environment targets; relaxing a target is a human-gate decision) |
| A regression check ("within X% of baseline") had no stored baseline to compare against | Rule 14 (baselines bootstrap, else absolute thresholds) |
| A literal CLI flag from the plan did not exist in the pinned tool version; the option lived in a config file in that version; the pinned tool version itself turned out to exist only as a beta | 1.3.6 Command & Pin Verification (pins must exist; commands spike-run or doc-verified against the pinned version; config files are part of the pin) |
| Implementation substitutions (beta pin, extra packages, timeout, .gitattributes) were never logged | Rule 14 (substitutions are deviations, logged when made); 3.7.1 question 1a verifies DEVIATIONS.md/EXECUTION_LOG.md completeness by diffing against ENVIRONMENT.md |

## Requested changes (v3.3 → v3.4)

| Request | Where it lives |
|---|---|
| After pre-mortem, a step that reviews assumptions and premises; false ones recorded as lessons and potentially knowledge, triggering normal plan iteration to apply the change | Phase 4.7 (Assumption & Premise Audit); artifact `premortem/ASSUMPTION_AUDIT.md`; amendment machinery via 2E.4; wired into 3.6 and 5.1 checks |
| Traditional code review step: bad code, anti-patterns, untested code, security issues/vulnerabilities, outdated or superseded dependencies | 3.8 `S-REVIEW`; artifact `reviews/CODE_REVIEW.md` |
| Adversarial review step that tries to break the app by challenging assumptions | 3.8 `S-ADVERSARIAL`; artifact `reviews/ADVERSARIAL_REVIEW.md` |
| Option to run a mutation test | 3.8 `S-MUTATE` (optional, pre-decided tool/scope/score target; opt-out recorded as `D-###`); artifact `reviews/MUTATION.md` |

## Requested changes (v3.2 → v3.3)

| Request | Where it lives |
|---|---|
| Periodically save planning agent state and progress to the project repo as a checkpoint to prevent data loss on reset | Phase 1.2.1 (corrected in v4.0: this row cited Global Rule 5, which is Tier Fallback) |
| Include full execution context (objective, call stack, step pointer, scratchpad, in-flight action) and active variable states in checkpoint so a fresh agent with no context can resume planning | Phase 1.2.2 |
| When planning agent resumes, check the repo for the most recent checkpoint to pick up exactly where it left off | Phase 1.2.3 |

## Requested changes (v3.1 → v3.2)

| Request | Where it lives |
|---|---|
| Record every correction to execution as a lesson, with the information that prevents a repeat, classified so related lessons can be read as a group | Global Rule 11; Appendix A (template); Appendix C (tags, matching rule) |
| As the last step of implementation, request a target for pushing the lessons | Gate `G-003` (Rule 10); closing step `S-KNOW` (3.7.2) |
| In research, read the lessons related to the problem and its implementation (e.g. audio lessons for a VST, Java lessons for a Java implementation) | R0 in 1.3; intake Subject tags (0.3.1); matching rule (Appendix C) |
| Before pushing lessons, a retrospective that identifies errors and overlooked steps and adds them as lessons | Closing step `S-RETRO` (3.7.1) |
| Record research and derived knowledge in a classified knowledge base, adding new facts about the Subject whenever they are found | Global Rule 12; R2/R6 coupling in 1.3; Appendix B (template) |

Supporting design: lessons and knowledge persist across tasks in a **knowledge store** (Rule 13; intake 0.3.1, access check 0.3.7, layout in Appendix C). During a run they accumulate on the working branch as one file per entry and are pushed at the end. They never contain secrets.

## Speed review: gaps that would slow implementation

Each round read the whole protocol and asked where an implementation would stall, need rework, or wait.

### Round 1
| Gap | Why it slows implementation | Resolution |
|---|---|---|
| Access was checked only as "push permission" | Missing workflow, pull-request, or packages permission surfaces mid-implementation and blocks work | 0.1 checks every permission the plan needs |
| Network checked in general, not per host | An unreachable registry or CI log store forces late workarounds | 0.1 checks each host the work depends on and decides an alternative channel |
| No implementation start step, branch, or log | Problems surface after delivery work has started; the retrospective has no record to read | Opening step `S-000` (3.7.0): branch, setup, access re-checked, `EXECUTION_LOG.md` |
| Gates idle the implementer; `G-003` could hold up completion | Waiting for a human stops all progress | Independent steps continue at gates (3.3); implementation completes after `S-RETRO` |
| A challenged frozen test forced a re-run from Phase 0 | A local problem triggered a full re-plan | Scoped amendment of the item and its dependants (2E.4) |
| No fallback for the store | An unreadable or moved store blocks research or the final push | Unreadable store is a risk, not a blocker (0.3.7); retry and bundle fallback (3.7.2) |

### Round 2
| Gap | Why it slows implementation | Resolution |
|---|---|---|
| No concurrency rule | Independent steps run one at a time | `Exclusive resources` field and concurrency rule (3.1) |
| Unbounded retrospective | Could re-investigate or re-run work | One pass over a collected digest; re-runs nothing (3.7.1) |
| Repeated mistakes create duplicate lesson files | Slower to write now and to read later | `occurrences` on the run's lesson (Rule 11, Appendix A) |
| Schema check was prose | Every run writes its own checker | Literal script in Appendix C, tested against the templates and against broken entries |
| No reading order for prior lessons | Large stores slow R0; later phases re-read lessons | Severity-then-recency order; prevention rules compiled into a checklist (R0) |
| Facts written twice by hand (claims and knowledge items) | Double bookkeeping in research | Knowledge items generated from `claims.json` (R2) |

### Round 3
| Gap | Why it slows implementation | Resolution |
|---|---|---|
| Checkpoint schema lacked the knowledge-store fields that 0.3.7 and R0 record | Agents invent field names; resume and audits break | Fields added to the `state.json` schema (1.2) |

### Round 4
No valuable gaps. Considered and declined, because none would speed implementation enough to justify the extra process:
- a pruning or archiving policy for the store (retirement and superseding already exist, and R0 reads in priority order);
- metrics on how effective lessons are;
- confidentiality rules beyond the existing no-secrets, no-personal-data rule;
- support for several stores (personal and team);
- automatic tag suggestion.

### Round 5: Agent Interruption & State Recovery Gaps
| Gap | Why it causes failure / data loss | Resolution |
|---|---|---|
| Checkpointing only on sub-phase boundaries | When an agent is stopped by external circumstances (timeouts, process reset, preemptions) during long research or step decomposition, all intermediate progress is lost | 1.2.1 Periodic cadence (every 3 actions / 3 min) and pre-action flush |
| Checkpoint schema lacked active variables and execution context | A fresh agent starting after a reset had no access to active constraints, open questions, draft step specifications, call stack, or scratchpad | 1.2.2 Full `execution_context` and `active_variables` schema |
| Undefined resumption discovery and reconciliation | Protocol lacked explicit procedure for locating the latest checkpoint, verifying disk artifact integrity, and resuming interrupted operations idempotently | 1.2.3 Zero-Context Resumption Protocol |

## Open decisions for the owner
- Whether any unfinished plan built under v3.x should take Global Rule 16 (untrusted content) or the 3.3 gate record by addendum (Rule 0.8). Default if undecided: no addendum; v4.0 applies to plans created from now on.
- The default lesson store proposed at intake is a repository named `Lessons` under the target repository's owner; the default knowledge store remains a repository named `knowledge` under the same owner. Each run asks at intake, so different locations can be given at any time.

## Corrections

| Date | Correction | Reason |
|---|---|---|
| 2026-10-27 | 0.3.1 default knowledge-store proposal renamed `agent-knowledge` → `knowledge` | The default did not match the actual store (`qualitycoding/knowledge`); a planner adopted it silently and the human had to correct it mid-run. Recorded in the run as a lesson: never adopt the protocol default without probing and confirming with the human. |
| 2026-11-01 | Protocol default split: lessons → `Lessons`, knowledge items → `knowledge` | The Lessons repo already exists as the canonical lesson store; keeping the protocol default combined risked lessons landing in the wrong repository at `S-KNOW`. |

## Change summaries v3 to v3.15 (moved from the protocol header in v4.0)

These were the summaries at the top of `planning-protocol.md` until v3.15, kept here unchanged. The detailed record of each change is in the sections above.

> **Changes from v3.14 (v3.15):**
> * Scheduled content refresh for courseware (3.11 item 8, intake 0.3.1, 5.1 final check; skill `learning-exercise-site` section 10): a `courseware` plan whose content describes a changing world records a refresh cadence at intake and plans a scheduled task that adds new units append-only (new dated ids, old units and saved scores untouched), follows a per-run checklist kept in the project repository, publishes only when the validator and browser tests pass, and confirms CI, the deployment and a live-site check for its commit before reporting. A static site never regenerates by itself; without this step the content silently goes stale.
>
> **Changes from v3.13 (v3.14):**
> * Mutation sharding (3.8 `S-MUTATE` and 3.9 mutation-job placement, new skill `mutation-sharding`): when the priced mutation job exceeds its runtime, memory or install budget, the plan designs a generated per-file or per-module shard matrix with explicit CPU, memory, parallelism and step limits, bounded three-attempt tool installation, per-shard report gates and one completeness-checking aggregate job as the only required status.
>
> **Changes from v3.12 (v3.13):**
> * Project nature and reference material (new Global Rule 15; intake 0.3.1; R7 permitted-use values; 3.10 reference set and evidence delivery; Phase 5 report and 5.1 final check; skill `audio-blind-listening-validation`): the protocol states from the outset that it builds hobby projects, and intake records `project.nature`. Reference material (anything the work is compared against or learns from that does not become part of the deliverable) must be **redistributable wherever the search allows**, and the research records what was searched. Where it cannot be, a hobby project may use restrictive material as a **private reference**: the licence is read from the source and allows personal download and use, the origin (URL, author, licence, date, sha256, terms URL) is recorded, the material is never committed, pushed or attached to any public artefact, and it is downloaded into the sandbox on demand (or by the human at a gate if the sandbox cannot reach it). Publication of anything derived from a reference fails closed.
>
> **Changes from v3.11 (v3.12):**
> * Source register (new research step `R7`, Rule 12, Appendix B): at the end of the research rounds, every external source checked, whether it was used, corroborating, rejected or unreachable, is listed with what it contains, its licence and terms of use, what the run may do with it, and where it was used. The list is one knowledge item tagged `kind:source-register`. It travels with the run's other knowledge items and is pushed to the knowledge store at gate `G-003`. Round logs carry a `Sources checked` section so nothing is lost if a round is interrupted. A later run loads the register in R0 to avoid re-checking sources, but it never counts as a source for any claim. The layout (1.1), the closing retrospective (3.7.1), the closing push (3.7.2), the final check (5.1) and the Phase 5 report verify it.
>
> **Changes from v3.10 (v3.11):**
> * Learning-exercise pathway (new mode flag `courseware`, new section 3.11 step `S-LEARN` and gate `G-LEARN`, new skill `learning-exercise-site`): a plan whose deliverable is practice material a learner is scored on (language exercises, quizzes, courses) fixes the learning design at intake, sources and dates its content, labels register (slang, colloquial, idiom), freezes item and scoring rules with a data validator and browser tests that use a fake speech API, carries a hosting preflight for settings an agent cannot change, and ends with a learner trial on the learner's own device. Intake (0.1, 0.3.1), gates (3.3), the 3.6 cold read, the Phase 4 lenses and the 5.1 final check verify it.
>
> **Changes from v3.9 (v3.10):**
> * Audio listening validation (new mode flag `audio`, new section 3.10 step `S-LISTEN`, new skill `audio-blind-listening-validation`): a plan that generates audio or audio tooling carries an explicit listening phase — a blind A/B test against reference recordings and a set of demos rendered from event files, delivered as a CI evidence bundle for phone listening, judged at a human gate with fixed questions and a pass condition frozen beforehand, and iterated on what the listener heard, with a round limit. Intake (0.3.1), human gates (3.3), the 3.6 cold-read check and the 5.1 final consistency check verify it.
>
> **Changes from v3.8 (v3.9):**
> * Mutation testing in CI (3.8 `S-MUTATE`, new skill `mutation-testing-in-ci`): the plan prices the mutation job before choosing when it runs (measured baseline test time, mutant count, estimated job time against a runtime budget) and pre-decides a three-tier trigger strategy — incremental runs on pull requests and default-branch pushes scoped to the changed mutable files, a scheduled full run, and an on-demand dispatch — with one always-running aggregator job as the only required status, so the job is neither run needlessly on every push nor silently skipped. The score gate is computed from the tool's report, not its exit status, with post-conditions (report exists, minimum mutant count); scheduled failures have a named owner.
> * The 3.6 cold-read check, the 3.9 CI matrix and the 5.1 final consistency check verify the mutation strategy when `S-MUTATE` is included.
>
> **Changes from v3.7 (v3.8):**
> * CI platform matrix (3.9 `[software]`): the CI runner matrix becomes a plan artifact derived from the supported platforms recorded at intake (0.3.2) — versioned runner labels instead of `-latest`, ARM64 jobs, a libc-variant container job, and an oldest-supported-toolchain job by default; QEMU-VM guests (BSDs, Solaris/illumos) and emulated CPU architectures on demand; Android jobs (KVM-accelerated emulator on Linux runners, matrix over API levels) and iOS jobs (macOS runners only, pinned Xcode, explicitly booted simulator, unsigned simulator tests, release signing behind `G-002`) when intake includes mobile platforms. Every intake-declared platform maps to a CI job or a recorded `D-###` waiver; the cold read (3.6), the pre-mortem lenses (Phase 4), and the final check (5.1) verify the mapping.
>
> **Changes from v3.6 (v3.7):**
> * Lesson store: lessons recorded under Rule 11 are ultimately pushed to the `Lessons` repository (default: a repository named `Lessons`, owned by the same account as the target repository). The knowledge store remains the destination for Rule 12 knowledge items; gate `G-003`/`S-KNOW` pushes the two stores separately.
> * Intake, access-check, checkpoint, R0, and closing-step language now distinguishes the lesson store from the knowledge store; Appendix C gives the layout and schema check for both repositories.
>
> **Changes from v3.5 (v3.6):**
> * Ephemeral-environment protections (0.1 environment-class probe; 1.5 `[ephemeral]`): on sandboxed platforms whose containers are recycled (temp dirs wiped, staged toolchains lost, background processes reaped at call boundaries or deadline kills), the plan and execution assume any container may die at any turn boundary — durable-mount discipline, turn-start restaging with exec-bit restoration, checkpointed resumable builds, ordering invariants, right-sizing steps to container lifetimes, CI for long work, and evidence honesty for locally blocked dimensions. Applies only when the environment probe classifies the platform as recycling (Kimi cloud: observed ephemeral; Kimi localhost: unknown → treat as ephemeral; Claude cloud/remote: observed stable → N/A).
> * Push cadence (Global Rule 6), active on **all** platforms: after every successful chunk — a step turning green, an amendment round, a review or gate record — commit and push immediately, verify with `ls-remote`, retry transient failures with backoff, and report mismatches.
>
> **Changes from v3.4 (v3.5):**
> * Honest verification (Rule 14): a check that cannot fail is not a check — no swallowed failures (`|| true`, `continue-on-error`), artifact post-conditions in every Done-when, budgets gate instead of inform, regression baselines are bootstrapped, and performance targets are per-runner-class with pre-decided miss rules.
> * Command & pin verification (1.3.6): literal commands and flags in the plan are spike-run or doc-verified against the *pinned* tool version, and every pinned version is checked to exist, before the plan freezes.
> * Deviation completeness: every substitution (version pin, added package, timeout, config file) is logged in `DEVIATIONS.md` the moment it is made; the retrospective verifies the log against the diff (3.7.1).
>
> **Changes from v3.3 (v3.4):**
> * Assumption & Premise Audit (Phase 4.7): after pre-mortem convergence, a fresh-context adversarial audit of every `A-###` assumption and the premises behind decisions and load-bearing claims. Falsified items are recorded as lessons (Rule 11) and knowledge items (Rule 12), and trigger the amendment machinery (2E.4) so the plan is iterated to apply the correction.
> * Code review steps (3.8): every `software` plan includes a traditional code review step (`S-REVIEW`) and an adversarial review step (`S-ADVERSARIAL`) before packaging/release; mutation testing (`S-MUTATE`) is an optional step with a pre-decided score target.
>
> **Changes from v3.2 (v3.3):**
> * Periodic Checkpointing (1.2.1): the planning agent periodically saves its state, active variables, and execution context to `.checkpoints/state.json`, surviving process termination or resets without data loss.
> * Full Context & Variable Serialization (1.2.2): checkpoint schema captures the active objective, hierarchical call stack, step pointer, working scratchpad, open questions, candidate decisions, uncommitted drafts, and runtime variable store.
> * Zero-Context Resumption Protocol (1.2.3): on startup, checks the repo for the most recent checkpoint, verifies artifact hashes, rehydrates variables and context, and picks up exactly where it left off.
>
> **Changes from v3.1 (v3.2):**
> * Lessons (Rule 11): every correction to execution is recorded as a classified lesson.
> * Knowledge base (Rule 12): research findings, and facts discovered later, are recorded as classified knowledge items.
> * Knowledge store (Rule 13): lessons and knowledge persist across tasks; research starts by loading the relevant ones (R0).
> * Closing steps (3.7): every plan ends with a retrospective, then a request (gate `G-003`) for where to push the run's lessons and knowledge.
>
> **Changes from v3:**
> * Adds profiles (Rule 0), so only the sections relevant to the task apply.
> * Restores every v2 software provision under the `software` profile: the security, data-corruption, unrecoverable-state, and feature-failure severities; the deployment pre-mortem; and the scale/performance, security, and operational lenses.
> * Adds a software intake block and software test categories (security, performance, operational).
> * Adds an Exploration sub-phase (2A.0) for mathematical work whose statements are not yet known.
> * Makes every consistency check profile-conditional.
>
> With only the `software` profile active, this protocol contains all of v2. With `math` + `computational` + `publication` active, it contains all of v3.
