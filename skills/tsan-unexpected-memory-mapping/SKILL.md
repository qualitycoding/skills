---
name: tsan-unexpected-memory-mapping
description: Use when ThreadSanitizer fails with 'unexpected memory mapping' at startup; fix by checking vm.mmap_rnd_bits and running under setarch -R.
---

# TSan "unexpected memory mapping" fix

## When this applies
A TSan-instrumented binary (or test run) dies at startup with:

    FATAL: ThreadSanitizer: unexpected memory mapping 0x... -0x...

This is a conflict between TSan's fixed shadow-memory layout and the kernel's mmap ASLR entropy, not a bug in the code under test. Do not debug the code.

## Diagnose (go by the sysctl, not the kernel version)
Baseline: on x86_64, TSan's layout supports `vm.mmap_rnd_bits` up to and including 28 (the upstream Linux kernel default). Values of 29 or more break it.

    uname -r
    cat /proc/sys/vm/mmap_rnd_bits

- x86_64: `mmap_rnd_bits` > 28 is the cause. Known configurations with 32: Ubuntu 22.04 with HWE kernel 6.5 and later, and Ubuntu 24.04 (kernel 6.8). Other distros may differ, so always read the sysctl.
- Other architectures (e.g. aarch64): no baseline recorded here. If the error appears, apply the fix below.
- Toolchain: LLVM/Clang 18 and later re-exec with ASLR disabled automatically, so the error is expected only with Clang earlier than 18 or a GCC whose libsanitizer lacks that fix. Verify the compiler version with `clang --version` or `gcc --version`.

## Fix
If the error occurred and (x86_64 with `mmap_rnd_bits` > 28, or any other architecture), disable ASLR for the process only:

    setarch "$(uname -m)" -R ./your_tsan_binary args...
    # e.g. setarch x86_64 -R ctest --output-on-failure
    # e.g. setarch x86_64 -R bash -c 'mvn test'   # wrap the whole command

Notes:
- `setarch -R` applies to the process and its children, needs no root, and leaves system settings untouched. Prefer it.
- Containers: Docker's default seccomp profile may block the personality syscall. If setarch fails with "Operation not permitted", run with `--security-opt seccomp=unconfined`, or use the sysctl below on the host.
- System-wide alternative (root, affects the whole machine; tell the user before using): `sudo sysctl vm.mmap_rnd_bits=28` (x86_64).
- Only apply this after seeing the error; do not wrap non-TSan runs.

## Report
State that the failure was the known TSan/ASLR conflict, include the observed `mmap_rnd_bits` value and compiler version, and show the setarch command used. Then continue with the actual TSan results.
