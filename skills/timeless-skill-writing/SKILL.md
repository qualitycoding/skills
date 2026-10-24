---
name: timeless-skill-writing
description: Use when writing or editing a skill, instruction file, or runbook, to replace time-relative wording (newer, older, recent, current) with fixed values that stay true as time passes.
---

# Writing skills that do not age

A skill is read months or years after it is written, by a reader who does not know when that was. Any phrase whose meaning depends on "now" silently becomes wrong or ambiguous. Anchor every such claim to a fixed value instead.

## Phrases that age (flag all of these)

- Relative age: newer, older, recent, recently, latest, modern, legacy, up to date, current, currently, nowadays, these days, at the time of writing.
- Relative degree: higher, lower, increased, raised, reduced, elevated, more than before, than it used to be, the old default.
- Open-ended direction: onward, going forward, in future, soon, upcoming, will be fixed, is being worked on, not yet supported.
- Relative versions: "the latest release", "a recent kernel", "newer compilers", "most distros now".
- Relative dates: this year, last month, yesterday, "as of now", "since the update".
- Unanchored comparatives and superlatives: best, fastest, standard, default, common, popular (default of what, and when?).

## Rewrite patterns

1. **Replace the comparison with the baseline value.**
   Bad: "fails when entropy is higher than the old default".
   Good: "fails when `vm.mmap_rnd_bits` is 29 or more (baseline: 28)".
2. **Replace vague age with explicit version bounds.**
   Bad: "newer compilers handle this".
   Good: "Clang 18 and later handle this; earlier versions do not".
3. **Replace "current" and "latest" with a procedure that fetches the truth.**
   Bad: "the latest LTS is 24.04".
   Good: "read the version with `lsb_release -r`; do not assume".
4. **Prefer a runtime check over a version table** when the real cause is a setting, capability, or file, not the version. Version numbers are only a proxy; test the actual condition.
5. **Anchor unavoidable facts with a date or version stamp.**
   Good: "Known configurations with 32: Ubuntu 22.04 HWE kernel 6.5 and later (verified 2026-10)". A dated claim stays true as a historical statement even if the world changes.
6. **State bounds as closed or explicit open ranges**, not trends. "6.5 and later" is fixed; "recent kernels" is not.
7. **Say what is unknown instead of guessing a trend.** "No baseline recorded for aarch64; apply the fix whenever the error appears" beats an unverifiable relative claim.
8. **Replace promises about the future** ("will be fixed", "not yet supported") with the fixed fact ("unsupported as of version X") or delete them.
9. **Give defaults a subject and a value**: "upstream Linux x86_64 default: 28", not "the default".

## Review checklist (run before saving a skill)

1. Search the draft for every phrase in the list above, including variants (new, old, recent, now, still, yet, soon, higher, lower, more, less).
2. For each hit, ask: would this sentence still be true and unambiguous if read ten years from now? If not, rewrite with a rule above.
3. Check that every number has a unit, a subject, and where useful a baseline.
4. Check that every version claim is an explicit bound ("X and later", "before X", "X through Y").
5. Check that every diagnosis step tests the real condition, not just a proxy such as a version number.
6. Check that claims you could not verify are marked as such and paired with a way for the reader to verify.
7. Report to the user which phrases were rewritten and which claims remain unverified.

## Worked example

Before: "Newer kernels raise ASLR entropy, which breaks ThreadSanitizer. If you see the error on a recent system, disable ASLR."

After: "ThreadSanitizer's x86_64 layout supports `vm.mmap_rnd_bits` up to 28 (the upstream Linux default); 29 or more triggers 'unexpected memory mapping'. Read `/proc/sys/vm/mmap_rnd_bits`; if it is above 28, run under `setarch "$(uname -m)" -R`."

The after-version names the setting, gives the threshold, and tells the reader how to check, so it needs no knowledge of when it was written.
