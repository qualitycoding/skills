# Planning protocol module: computational (v1.0)

Read when `computational` is active (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

**0.3.4 Computational intake** `[computational]`. Record:
* the required floating-point precision;
* the reproducibility requirements (bitwise identical, or within tolerance);
* the target hardware and thread counts;
* the maximum compute budget per run and in total.

### 2B items moved from the core

2. **Provenance Contract** `[computational]`: Every result file must embed or sidecar the following metadata:
   * the git commit hash;
   * an environment lockfile hash;
   * random seeds;
   * all input parameters;
   * a UTC timestamp;
   * the hardware and thread count.

   Tests enforce this contract.

   **Numerical V&V categories** `[computational]`:
   * **Code verification:** the method of manufactured solutions, or known analytic or closed-form cases.
   * **Convergence:** observed order of accuracy across at least 3 (preferably 4 or more) refinement levels, asserting the observed order is within a stated band of the theoretical order.
   * **Invariants:** conservation laws, symmetries, positivity, and identities from `M-###` statements.
   * **Precision cross-check:** key quantities recomputed at elevated precision (e.g., mpmath) must agree within the stated tolerance.
   * **Reproducibility:** identical results across repeated runs, and results within tolerance across the specified thread counts.
   * **Symbolic cross-check:** CAS verification of any closed-form expression implemented in code.

## Checks this module adds

### Cold read (3.6 step 2)

None beyond the core.

### Pre-mortem lenses (4.2)

* `[computational]` Numerical validity (discretization, conditioning, precision, under-resolved regimes); reproducibility (environment drift, nondeterminism); compute budget.

### Final check (5.1)

None beyond the core.
