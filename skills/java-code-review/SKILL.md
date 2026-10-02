---
name: java-code-review
description: Opinionated Java code review that enforces immutability (every reference final unless a comment justifies otherwise), no if/for/while/switch statements without a justifying comment, SOLID with single responsibility as the top priority, functional style using vavr persistent collections and Option/Either/Try/Validation, fluent APIs, AssertJ, and near-100% test coverage where every test asserts something meaningful. Use this skill whenever the user asks to review, critique, audit, check or tidy Java code - a PR, a diff, a pasted class, uploaded files, a module or a whole repo - and whenever they ask if Java code or Java tests are clean, well-designed, well-tested or ready to merge, even if they never say "code review".
---

# Java code review

This is the author's house style, and they want to be held to it. Review firmly:
code that works but violates these standards still gets findings. Be concrete -
every finding names a location and shows the fix in the codebase's own names.
Never pad with generic advice that isn't tied to a line of code.

## The standards, in priority order

1. **Single responsibility (crucial).** Every class and every method has exactly
   one reason to change. Test: write one sentence saying what the class is
   responsible for. If the sentence needs "and", or names two different kinds of
   stakeholder (e.g. pricing rules *and* persistence), it is a finding. Always
   propose the concrete split: new class names and which members move.
   Details and heuristics: `references/solid.md`.
2. **Immutability.** Domain types are records or final classes with private
   final fields, no setters, no exposed mutable internals, and vavr persistent
   collections instead of `java.util` mutable ones. Change is expressed by
   returning new values (`withX(...)`, `append`, `put`). No mutable static
   state, ever. **Every reference is `final`** - fields, parameters, local
   variables and catch parameters - unless it absolutely has to be reassigned,
   and then an explanatory comment beside it says why.
   Details: `references/immutability.md`.
3. **Tests.** Near-100% coverage (defaults: >= 95% line and >= 90% branch per
   class) and every test asserts something that would fail if the behaviour
   broke. AssertJ fluent assertions throughout. Details: `references/testing.md`.
4. **The rest of SOLID** - open/closed, Liskov, interface segregation,
   dependency inversion. `references/solid.md`.
5. **Functional style with vavr.** No nulls (Option), expected failures as
   values (Either/Try/Validation), pure functions with side effects pushed to
   the edges. **The control-flow statements `if`, `for`, `while`, `do` and
   `switch` are not used** unless absolutely required, and then an explanatory
   comment beside the statement says why: express the logic with
   map/filter/fold, Option, polymorphism or a lookup instead.
   `references/functional-style.md`.
6. **Fluent style.** Expression-oriented pipelines, fluent builders/withers,
   AssertJ chains. Also in `references/functional-style.md`.

Read the reference file for a standard before writing findings about it, the
first time in a conversation. They contain the checklists and the fix patterns.

## Workflow

### 1. Establish scope
- **Pasted code** - review it in chat.
- **Uploaded files or a repo on disk** - run the scanner (step 2) first.
- **A diff/PR** - findings target the changed lines, but judge SRP against the
  whole class, and check that changed behaviour came with changed tests.
  Behaviour changed with no test change is a finding in its own right.

Separate main code from test code (`src/test/`, `*Test.java`, `*IT.java`).

### 2. Pre-scan (when code is on disk)

```bash
python <skill-dir>/scripts/java_review_scan.py <path> [<path> ...] \
    [--jacoco path/to/jacoco.xml] [--line-min 95] [--branch-min 90] [--json]
```

It is heuristic and regex-based. Treat each hit as a lead: open the code,
confirm it, drop false positives, and fold confirmed hits into your own
findings. Never paste raw scanner output as the review. It also misses things
only reading can find (SRP, LSP, naming, abstraction levels), so step 4 is
never optional.

### 3. Coverage
- Look for a JaCoCo report: `target/site/jacoco/jacoco.xml` (Maven) or
  `build/reports/jacoco/test/jacocoTestReport.xml` (Gradle). If found, pass it
  with `--jacoco`; the scanner reports per-class ratios and uncovered lines.
- If there is no report but the project builds here, generate one
  (`mvn -q verify` with the jacoco plugin, or `gradle test jacocoTestReport`).
  Sandboxes often can't reach Maven Central - don't burn many attempts.
- Otherwise build a **coverage map by hand**: list each public method and each
  branch (every `if`, `switch` arm, Option/Either side, `fold` arm, exception
  path) in main code and the test that exercises it. Mark gaps. Say plainly in
  the report that coverage is *estimated*, and give the command that would
  measure it.

### 4. Read and review
For each class: write the one-sentence responsibility (SRP check), then walk
the checklists in the reference files. Review tests as carefully as main code -
a test suite that runs everything but checks nothing is the failure mode this
skill exists to catch.

### 5. Write the report (format below)

## Severity

| Severity | Meaning | Typical examples |
|---|---|---|
| **Blocker** | Must fix before merge | Test with no assertion, or `assertThat(x);` with nothing chained; class with two or more clearly unrelated responsibilities; mutable static state; internal mutable collection returned to callers; public behaviour with no test; changed code below coverage threshold |
| **Major** | Should fix before merge | A reference (field, parameter, local, catch parameter) that is not `final` and has no comment justifying it; an `if`/`for`/`while`/`do`/`switch` with no comment justifying it; a justification comment that does not hold up (it restates what the code does, or the alternative is straightforward); non-final field or setter in a domain type; `java.util` mutable collections in domain code; returning or passing `null`; field injection; `new`-ing collaborators inside business logic; LSP breaks (`UnsupportedOperationException` overrides); tests whose only assertion is `isNotNull()`; god method mixing abstraction levels |
| **Minor** | Fix soon | JUnit/Hamcrest assertions instead of AssertJ; `Collectors.toList()`; logic (`if`/loops) inside tests; `Instant.now()` instead of an injected `Clock`; long method |
| **Nit** | Optional polish | Naming, chain formatting, mixing `Optional` and vavr `Option` |

Verdict:
- any Blocker or Major -> **Request changes**
- only Minor/Nit -> **Approve with suggestions**
- nothing -> **Approve**

## Judgement calls

Don't flag, or downgrade to Nit, when the code is doing the right thing for a
real constraint - but say why in one line if you mention it:

- **Framework-bound types** (JPA entities, Jackson DTOs needing no-arg
  constructors/setters, Spring `@ConfigurationProperties`). Acceptable *only*
  at the boundary. If they leak into domain logic, that is the finding: map to
  an immutable domain record at the edge.
- **`java.util` at third-party API boundaries**, converted immediately
  (`List.ofAll(javaList)`, `seq.asJava()`).
- **Sealed interfaces + records** are good algebraic-data-type modelling, not an
  OCP violation, when the set of variants is genuinely closed. Prefer putting
  the behaviour on the types (a method on the sealed interface). An exhaustive
  pattern-matching `switch` over them is still a control-flow statement: when
  it is genuinely the clearest option (e.g. the operation belongs outside the
  types), it needs its justifying comment like any other.
- **Justification comments** sit on the same line as, or the line directly
  above, the `if`/`for`/`switch` or non-final declaration. They must say *why*
  the construct is needed, not restate what it does: "// loop: called per audio
  sample; a stream allocates on every call (measured, see PerfTest)" is a
  justification; "// loop over the samples" is not. Judge whether the reason
  holds - an unconvincing justification is still a finding.
- **Contained local mutation** in a measured hot path, with a comment or
  benchmark justifying it. Without the justification it's a Minor.
- **Builders** are fine if `build()` returns an immutable object and the builder
  never escapes.
- **Coverage exclusions** for generated code, `main` bootstrap and pure
  framework wiring are fine *if configured in JaCoCo*, not silently left red.
  Unreachable defensive branches should usually be deleted (make the types rule
  the case out) rather than excluded.

**Codebase-wide gaps**: if the project doesn't use vavr (or AssertJ) at all,
raise it once as a single Major "adopt vavr / AssertJ" finding with a migration
sketch, not as fifty per-line findings. Then review the rest against the
standards as if adopted.

**Group repeats.** Seven non-final fields become one finding listing seven
locations with one fix example - not seven findings.

## Report format

Use this structure. Omit empty sections except Verdict and Tests & coverage.

```markdown
# Java review: <scope>

**Verdict:** Request changes | Approve with suggestions | Approve
**Coverage:** <line %> line / <branch %> branch (measured | estimated)

## Summary
2-4 sentences: overall shape, the most important problem, what's done well.

## Blockers
### B1. <short title> - `path/File.java:42` [SRP]
What's wrong and why it matters (1-3 sentences).
```java
// suggested fix, in the codebase's own names
```

## Major
### M1. ...

## Minor & nits
- `File.java:88` [Functional] ... - one line each, snippet only if non-obvious.

## Tests & coverage
- Coverage table or estimated coverage map for classes below threshold.
- Tests lacking assertions or with weak assertions.
- Behaviours with no test (list them as test names you'd write, e.g.
  `rejectsOrderWhenBasketIsEmpty`).

## What's good
1-3 bullets - brief and specific.
```

Tag each finding with its standard: `[SRP]`, `[Immutability]`, `[OCP]`,
`[LSP]`, `[ISP]`, `[DIP]`, `[Functional]`, `[Fluent]`, `[Tests]`, `[Coverage]`.

For SRP findings the fix is a design sketch, not a snippet: list the new types,
their one-sentence responsibilities and which members move where.

If the user asks you to *apply* the fixes rather than review, make the changes,
then re-run the scanner and re-check the report's Blockers and Majors against
the new code before handing it back.
