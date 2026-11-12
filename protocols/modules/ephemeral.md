# Planning protocol module: ephemeral (v1.0)

Read when the 0.1 diagnostic classifies the environment as `ephemeral` (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

### 1.5 Ephemeral-Environment Protections `[ephemeral]`
Applies iff the Phase 0.1 diagnostic classified the execution environment as `ephemeral` (container/sandbox subject to reaping: temp dirs wiped between turns, toolchain staging lost, background processes killed at call boundaries or deadline kills). On such platforms, design and execute as if any container may die at any turn boundary — because it may. The executing agent must:

1. **Durable surface only.** Treat only the persistent mount recorded in the 0.1 diagnostic as durable. Assume `/tmp`, `/var/tmp`, environment variables, installed packages, and running processes may vanish at any turn boundary or deadline kill. Anything needed by a later turn is copied to the mount within the same action that produces it.
2. **Turn-start restaging.** Begin every turn by re-staging toolchain/runtime pieces from the mount into fast local disk (compilers, build systems, downloaded/extracted dependencies), and restore executable bits after every copy — network/fuse mounts commonly strip exec bits, so `chmod -R +x` after each restore (or run scripts via an interpreter where the mount forbids exec entirely). Verify staged binaries actually run before depending on them.
3. **Checkpointed long builds.** Any build or run that can exceed one container lifetime executes as a resumable loop: build in fast local storage, periodically sync the whole tree back to the mount, keep a persistent compiler cache on the mount (e.g. ccache), and make the loop safe to relaunch after any recycle. Never rely on a background process outliving its tool call — if work must continue past a call deadline, use a foreground wrapper that waits and checkpoints; a detached process spawned inside a call is reaped with the call.
4. **Ordering invariants.** Learned from real failures: pass dependency source overrides as `-D` configure arguments, not environment variables (CMake ignores the env vars); when configure re-touches generated headers, do header back-dating/precompiling only after the final configure; export `compile_commands.json` at configure time; cache downloaded tool archives on the mount and resume partial downloads.
5. **Right-size the work.** Design steps so no single operation depends on surviving: target container lifetimes of minutes, not hours. Anything longer (heavy instrumented builds, multi-hour benchmarks/fuzz runs) is executed in CI by design and recorded locally as environment-blocked with the CI equivalent identified — never reported as green.
6. **Evidence honesty.** A verification dimension that cannot complete locally because of recycling is documented as blocked (environment limitation), with the identical job named in CI; it is a failure of integrity to present it as a pass.

## Checks this module adds

### Cold read (3.6 step 2)

None beyond the core.

### Pre-mortem lenses (4.2)

None beyond the core.

### Final check (5.1)

None beyond the core.
