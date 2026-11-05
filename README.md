# Skills

AI skills: folders of instructions, reference material and scripts that teach an AI assistant to do a particular
kind of task well and consistently. Each skill follows the Agent Skills format used by Claude: a `SKILL.md` file
with YAML front matter (a `name` and a `description` that says when to use it), plus any supporting files it
needs.

## Skills

| Skill | What it does |
|---|---|
| [java-code-review](skills/java-code-review) | Opinionated Java code review: immutability with every reference `final`, no `if`/`for`/`while`/`switch` without a justifying comment, SOLID with single responsibility first, functional style with vavr, AssertJ, and near-100% coverage where every test asserts something. Includes a scanner for the mechanical checks. |
| [tsan-unexpected-memory-mapping](skills/tsan-unexpected-memory-mapping) | Fixes ThreadSanitizer's "unexpected memory mapping" startup failure: checks `vm.mmap_rnd_bits` (above 28 on x86_64 breaks TSan) and reruns under `setarch -R`. |
| [timeless-skill-writing](skills/timeless-skill-writing) | Rewrites time-relative wording (newer, recent, current, higher) in skills and runbooks into fixed baselines, explicit version bounds and runtime checks. |
| [mutation-testing-in-ci](skills/mutation-testing-in-ci) | How to run mutation testing in CI: price the job first, three tiers (incremental pull-request runs on changed files, scheduled full run, on-demand dispatch) behind one always-running required check, a score gate computed from the report with post-conditions, runtime control, and working the survivors. Includes a score gate script, an incremental-scope script and a workflow template. |
| [publish-skills-to-repo](skills/publish-skills-to-repo) | Standing rule: every skill, instruction or protocol created or modified, including this one, is committed and pushed to this repo. |
| [proper-english](skills/proper-english) | Grammatically correct British English for anything a person will read: -ise/-yse spelling, single quotation marks, complete correlative pairs (neither … nor, either … or), "or" after "no/not", parallel structure, agreement, dangling participles, fewer/less. Sources are British (Oxford and Cambridge dictionaries and grammars, university style guides), each marked read, excerpt or consult; unverified rules are flagged. Evals include acceptable variants that must be left alone. |
| [audio-blind-listening-validation](skills/audio-blind-listening-validation) | Human listening validation for anything that generates audio or audio tooling: seeded blind A/B pairs against reference recordings (onset-preserving cuts, loudness-matched, base64 key), headless-rendered demos, CI evidence bundle on an orphan branch for phone listening, a gate with fixed questions and responses, scoring against chance, and iterating on what the listener heard. Includes a pair builder and a scorer. |
| [learning-exercise-site](skills/learning-exercise-site) | Scored, retryable learning exercises on GitHub Pages (reading, listening, writing, speaking): dated and sourced content with slang/colloquial/idiom labels, 10-item scoring with partial credit, browser speech with a self-assessment fallback, `localStorage` scores with export/import, a data validator and Playwright tests with a fake speech API, hosting preflight, and a learner-trial gate. The `courseware` pathway of the planning protocol. |
| [planning-protocol-addendum-rollout](skills/planning-protocol-addendum-rollout) | Repeatable cross-repository planning upgrades: inventory all branches, audit each repository's protocol baseline, create per-repository addendum plans and a central implementation controller, publish safely, and verify remote artifacts. Includes an artifact contract and structural checker. |

## Protocols

Longer operating procedures that an AI agent follows end to end, rather than skills it reaches for on demand.

| Protocol | What it does |
|---|---|
| [planning-protocol](protocols/planning-protocol.md) | Hardened planning: research, test-first specification and freeze, a zero-question plan, recursive pre-mortem, and a push to a generation branch for a separate implementing agent. Profiles select the parts that apply (`software`, `math`, `computational`, `publication`); the `audio` flag adds a blind-listening and demo-listening phase; the `courseware` flag adds the learning-exercise pathway (sourced content, frozen scoring, browser tests, learner trial). It learns across tasks: corrections become classified lessons that are ultimately pushed to the `Lessons` repo, findings become knowledge items pushed to the knowledge repo, and both are loaded at the start of later research. At the end of the research rounds, every external source checked is listed with its content and licence as a source-register knowledge item, pushed with the rest. Change history and review record: [planning-protocol-review](protocols/planning-protocol-review.md). |
| [planning-v3.9-addendum-control](protocols/planning-v3.9-addendum-control.md) | Cross-repository controller for upgrading the 33 qualitycoding code repositories it lists to planning protocol v3.9. Includes exact source branches/commits, execution and recovery rules, a resumable JSON status ledger (`protocols/planning-v3.9-addendum-status.json`), and a mechanical verifier (`protocols/v39_addendum_verify.py`). |
| [blind-listening-test-execution-plan](protocols/blind-listening-test-execution-plan.md) | Execution plan for running repeatable blind listening gates in `oildrumkit`, `sitar`, `chinese-strings` and `oildrumkit-vcvrack`, so that a fresh agent can resume from the committed records. Based on the `audio-blind-listening-validation` skill. |
| [oildrumkit-vcvrack-plan](protocols/oildrumkit-vcvrack-plan.md) | Execution plan (protocol v3.3) for fixing known defects in and hardening the Oil Drum Kit VCV Rack 2 module in `oildrumkit-vcvrack`. |

## Layout

```
protocols/          operating procedures followed end to end
skills/
  <skill-name>/
    SKILL.md        instructions and front matter (required)
    references/     detail loaded only when needed
    scripts/        tools the skill runs
    evals/          example prompts with expected outcomes
```

## Using a skill

- **Claude apps (claude.ai, desktop, mobile):** zip the skill's folder and upload it as a skill in Settings.
  For example: `cd skills && zip -r java-code-review.zip java-code-review`.
- **Claude Code:** copy the skill's folder into `~/.claude/skills/` to use it everywhere, or into a project's
  `.claude/skills/` to share it with that project.

Once installed, the skill is used automatically when a request matches its description, e.g. "review this
Java class".

## The Java review scanner

`java-code-review` includes a heuristic pre-scan the skill runs before reading the code. It can also be run
directly:

```
python skills/java-code-review/scripts/java_review_scan.py path/to/repo [--jacoco target/site/jacoco/jacoco.xml] [--json]
```

It reports leads to confirm by reading the code (assertion-less tests, non-final references, unjustified
control-flow statements, mutable collections and more), plus per-class coverage from a JaCoCo report.

## Licence

[Apache License 2.0](LICENSE)
