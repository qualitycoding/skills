# Planning protocol module: figures (v1.0)

Read when `computational` or `publication` is active (core Rule 0.7). Written for core v4.x of `protocols/planning-protocol.md`; a plan records this module's version in `plan/PROFILE.md` (Rule 0.8). Section numbers are the core's: the core keeps each heading below with a pointer to this file, so references by number resolve in either place.

### 2C Figure Specification `[computational, publication]`
1. For each figure that is a deliverable, write an entry `F-###` in `figures/SPEC.md` with:
   * the claim or statement it supports;
   * the source data file(s) and the step that produces them;
   * the generating script path;
   * the output path;
   * the format (vector PDF or EPS for plots; raster only for inherently raster content, at ≥ the required DPI);
   * the size (`[publication]` in the venue's column widths);
   * fonts and font size (`[publication]` matching the manuscript);
   * a colormap that is perceptually uniform and colorblind-safe (e.g., viridis or cividis);
   * axis labels using `math/NOTATION.md` symbols, where that file exists;
   * `[publication]` caption text requirements.
2. **Figure Tests** (`T-###`):
   * The figure regenerates from its script and committed data with a single command.
   * The data file hash matches the provenance record. Do not hash the image pixels.
   * The output exists in the specified format.
   * `pdffonts` reports all fonts embedded.
   * Every plotted quantity traces to a result file.
   * `[publication]` The figure is referenced in the manuscript.
3. **Generative Imagery Rule:** Generative-AI images may never depict data, results, or experimental or computational output. `[publication]` If intake permitted illustrative generative imagery, each such figure must be flagged `illustrative-generated` in the spec, must comply with the venue policy recorded in `A-###`, and must be disclosed in the manuscript. Otherwise, all illustrations are produced programmatically (e.g., TikZ, Matplotlib, Asymptote).

## Checks this module adds

### Cold read (3.6 step 2)

* `[computational, publication]` every `F-###` has a producing step.

### Pre-mortem lenses (4.2)

None beyond the core.

### Final check (5.1)

* `[computational, publication]` that every `F-###` has a producing step and a test.
