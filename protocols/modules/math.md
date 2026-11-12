# Planning protocol module: math (v1.0)

Read when `math` is active (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

**0.3.3 Mathematical intake** `[math]`. Record:
* the **Research Question** and **Hypothesis** (or "exploratory, no hypothesis");
* the known target statements, if any (which sets `math.exploration`);
* which statements require `formally-checked` status (default: none);
* the exploration budget, if `math.exploration` is set (default: stated as a count of plan steps and compute hours).

### 2A Mathematical Specification `[math]`

**2A.0 Exploration** `[math, if math.exploration]`. Runs before 2A.1 when the statements to be proved are not yet known.
1. **Conjecture generation.** Search for analogous known results and check small cases by hand or with the CAS. `[computational]` Run bounded numerical experiments in `research/spikes/`. Record each candidate statement in `math/EXPLORATION.md` as `X-###`, with its supporting evidence and an evidence class of `heuristic` or `numerically-supported`.
2. **Strategy selection.** For each promising `X-###`, list the candidate proof strategies (e.g., induction, a variational argument, a spectral estimate, reduction to a known theorem). For each strategy, record:
   * its required lemmas;
   * the known obstacles;
   * an estimated difficulty.

   Choose a primary strategy and a fallback, and write the switching rule (e.g., "if lemma L fails or is not proved within N steps, switch to the fallback").
3. **Budget and exit.** Exploration is bounded by the intake budget. At exit, one of three outcomes applies:
   * each surviving `X-###` is promoted to `M-###` with a target evidence class;
   * it is retained as a conjecture, to be stated only per Rule 7;
   * it is converted into an implementer exploration step, followed by gate `G-001`, with Rule 8 result-pivot rules.

   If no candidate survives, log a High risk and carry it to Phase 4.

**2A.1 Notation** `[math, publication]`. Write `math/NOTATION.md`, defining every symbol, convention (sign, normalization, index placement, units), and function space. All later artifacts must use it.

**2A.2 Statements.** In `math/STATEMENTS.md`, list every mathematical statement the deliverables will make as `M-###`, recording:
* the precise statement with all hypotheses;
* its current evidence class;
* its dependencies (other `M-###`, `C-###`, `X-###`);
* its target evidence class.

Include a dependency graph and check it for cycles.

**2A.3 Proof Obligations.** For each `M-###` whose target is `proved` or `formally-checked`, write a proof or detailed proof sketch in `math/proofs/M-###.md` (or `.tex`). If a statement cannot be proved during planning, the plan must include an implementer step to attempt it, using the strategy and fallback from 2A.0 (or chosen here), with a result-pivot rule (3.2) for failure.

**2A.4 Adversarial Proof Review (T2, fresh context, one reviewer per proof).** The reviewer:
* checks every step and every hypothesis;
* tries to construct counterexamples;
* tests edge cases (degenerate dimensions, boundary parameter values, empty or trivial cases);
* symbolically or numerically spot-checks any identity used.

Record the verdict in `math/reviews/M-###-rN.md` as `accept`, `accept-with-fixes`, or `reject`. Repeat with a **new** reviewer after every fix, up to 3 rounds. A statement still rejected is downgraded to `numerically-supported` or `heuristic`, and its wording changes accordingly.

**2A.5 Formal Checking** `[math, if formal checking required]`. Specify the formalization target, library versions, and the exact command whose success constitutes `formally-checked` (e.g., `lake build` with zero `sorry`, confirmed by `grep -r "sorry" math/formal` returning nothing).

## Checks this module adds

### Cold read (3.6 step 2)

None beyond the core.

### Pre-mortem lenses (4.2)

* `[math]` Mathematical correctness (unchecked hypotheses, edge cases, sign and normalization conventions); every `M-###` below its target evidence class; `[if math.exploration]` conjectures promoted on weak evidence.

### Final check (5.1)

* `[math]` that every `M-###` has an evidence class consistent with its planned wording.
