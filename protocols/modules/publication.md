# Planning protocol module: publication (v1.0)

Read when `publication` is active (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

**0.3.5 Publication intake** `[publication]`. Record:
* the **Intended Contribution**, meaning what is claimed to be new;
* the target venue (primary and fallback), article type, and page or word limits;
* the venue's template and author-guidelines URL;
* authors, affiliations, ORCIDs, and the corresponding author;
* the venue's AI-use and image-integrity policies;
* code and data licenses, and the availability-statement wording;
* the archive target (e.g., Zenodo) and whether a preprint is intended;
* whether generative-AI imagery is permitted anywhere (default: only for non-data illustrative graphics, only if the venue allows it, and always disclosed).

### 2D Manuscript Specification `[publication]`
1. **Outline:** Write `manuscript/OUTLINE.md`, mapping each section and paragraph-level claim to evidence IDs (`M-###`, `T-###`, `F-###`, `C-###`). No claim may appear without an evidence ID. Mathematical claims must be worded to match their evidence class (Rule 7). Include a pre-decided priority order for moving material to supplementary files if limits are exceeded.
2. **Generated Values:** Every number quoted in the text or in tables is emitted by code into `manuscript/generated/values.tex` as LaTeX macros (e.g., `\newcommand{\ObservedOrder}{2.01}`). Hand-typed result numbers are prohibited.
3. **Checklist:** Convert the venue's author guidelines into testable items in `manuscript/CHECKLIST.md`, such as:
   * page and word limits;
   * required sections (data availability, AI-use disclosure, competing interests, etc.);
   * reference style;
   * figure formats;
   * abstract length;
   * keywords and classification codes.
4. **Manuscript Tests** (`T-###`):
   * `latexmk -pdf -halt-on-error -interaction=nonstopmode main.tex` succeeds.
   * The log contains no undefined references or citations, and no multiply defined labels.
   * `chktex` reports no warnings above an agreed threshold.
   * Every bibliography entry with a DOI resolves.
   * Every figure `\ref` resolves to an `F-###` output.
   * No hand-typed numerals appear in results sections, outside an allowlist.
   * Every checklist item passes.
   * Notation-lint: symbols in `math/NOTATION.md`, if present, are not redefined.
5. **Reproducibility Package Spec:** Define the archive contents (code, lockfile, data, figure scripts, a README with one-command regeneration), the license files, the metadata (title, authors, ORCIDs, keywords, related identifiers linking paper ↔ code ↔ data), and the availability-statement text.

## Checks this module adds

### Cold read (3.6 step 2)

* `[publication]` every manuscript claim has an evidence ID.

### Pre-mortem lenses (4.2)

* `[publication]` Rigor as perceived by referees; presentation (figure–text mismatch, notation inconsistency, overclaiming beyond the evidence class); venue policy (AI disclosure, image policy, licensing, data availability, citation accuracy); archive completeness.

### Final check (5.1)

None beyond the core.
