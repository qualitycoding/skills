# Skills

AI skills: folders of instructions, reference material and scripts that teach an AI assistant to do a particular
kind of task well and consistently. Each skill follows the Agent Skills format used by Claude: a `SKILL.md` file
with YAML front matter (a `name` and a `description` that says when to use it), plus any supporting files it
needs.

## Skills

| Skill | What it does |
|---|---|
| [java-code-review](skills/java-code-review) | Opinionated Java code review: immutability with every reference `final`, no `if`/`for`/`while`/`switch` without a justifying comment, SOLID with single responsibility first, functional style with vavr, AssertJ, and near-100% coverage where every test asserts something. Includes a scanner for the mechanical checks. |

## Protocols

Longer operating procedures that an AI agent follows end to end, rather than skills it reaches for on demand.

| Protocol | What it does |
|---|---|
| [planning-protocol](protocols/planning-protocol.md) | Hardened planning: research, test-first specification and freeze, a zero-question plan, recursive pre-mortem, and a push to a generation branch for a separate implementing agent. Profiles select the parts that apply (`software`, `math`, `computational`, `publication`). It learns across tasks: corrections become classified lessons, findings become knowledge items, and both are loaded at the start of later research. Change history and review record: [planning-protocol-review](protocols/planning-protocol-review.md). |

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
