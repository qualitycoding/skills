---
name: learning-exercise-site
description: Use when planning or building interactive learning exercises delivered as a website - language practice (reading, listening, writing, speaking), quizzes or courses - that must be scored, retryable, saved between visits and hosted on GitHub Pages. Defines the S-LEARN pathway of the planning protocol - intake decisions, dated and sourced content with register labels (slang, colloquial, idiom), item and scoring design, browser speech with fallbacks, persistence, a data validator, browser tests with a fake speech API, hosting preflight, and a learner-trial gate.
---

# Interactive learning-exercise sites

A learning site fails in ways a normal web app does not: an answer key that marks a correct answer wrong, a text
that is out of date or attributes invented words to a real person, a slang word presented as neutral, an exercise
that takes forty minutes instead of ten, or a speaking task that only works in one browser. This skill makes those
risks explicit and checkable. It was derived from `qualitycoding/swedish-exercises` (Swedish current affairs: 6
themes × reading, listening, writing and speaking; static GitHub Pages app), which serves as the reference
implementation for every rule below.

## When it applies

Use it whenever the deliverable is practice material a learner works through and is scored on. In the planning
protocol it is the `courseware` mode flag and section 3.11 (step `S-LEARN`, gate `G-LEARN`). It normally accompanies
the `software` profile. Omitting the learner trial needs a recorded `D-###` reason.

## 1. Intake decisions (record each as an assumption or decision)

| Decision | Default used in the reference implementation |
|---|---|
| Target language, learner's language, level (CEFR) | Swedish, English glosses avoided in favour of Swedish explanations, B1–B2 |
| Skills covered | reading, listening, writing, speaking – one exercise per skill per theme |
| Session length and score scale | about 10 minutes; 10 items × 1 point, half points allowed |
| Retry and persistence | unlimited retries with reshuffled options; best, last, attempts and history in `localStorage`; export/import JSON for moving devices; no accounts |
| Register labelling | every glossed term carries `slang`, `vardagligt` (colloquial), `idiom` or no label |
| Content currency | "news situation on <date>" shown on every theme; sources linked |
| Hosting | GitHub Pages from `main` / root; no build step |

## 2. Hosting and repository preflight (do this in the first message)

Agent sandboxes often cannot create repositories or change Pages settings, and cannot load `*.github.io`.
- Probe repository creation and the Pages API before building. If refused (for example `POST user/repos` or
  `POST repos/<o>/<r>/pages` answered 403 by a session proxy), ask the human in the first message to create the
  empty repository and to set **Settings → Pages → Deploy from a branch → main → / (root)**. Build meanwhile.
- First push includes a `LICENSE` (the owner's standard licence), `.nojekyll`, a `README.md`, CI and a lockfile.
- Verify the deployment without loading the site: the Actions runs list shows a `pages build and deployment` run
  for the pushed commit; its conclusion is the evidence. A `startup_failure` straight after Pages is first enabled
  is retried (rerun the run or push a commit) before it is reported.

## 3. Content: current, sourced, original, honest

1. Research each theme with web search on the day; keep the sources (title + URL) in the theme file and show them
   with the date. Two independent sources for every number used in a question.
2. Write original texts. Never copy sentences from sources; quotations of real people stay under 15 words and
   only when the exact wording matters. Prefer paraphrase.
3. **Never invent statements, feelings or plans of real people.** A listening script that dramatises news may only
   contain facts from the sources. Check every sentence about a named person against a source before freezing.
4. Colloquial material goes in clearly fictional frames: the reference texts end with a coffee-room dialogue
   marked *påhittat exempel* (invented example); listening intros say the script was written for the exercise.
5. Political topics: describe procedures, results and positions neutrally; no verdicts; each side's position in
   its own words (paraphrased).
6. Length targets for about 10 minutes at B1–B2: reading 200–450 words + 10 questions; listening script
   120–320 words + 10 questions. The validator enforces them.

## 4. Register labels

Mark glossed words inline as `[[word|explanation|label]]` with label `slang`, `vardagligt`, `idiom` or empty.
Render a dotted underline, a coloured tag naming the register and a tap/hover explanation; list all terms in a
glossary per text; show a legend on the index and on every exercise. Each reading text must contain at least one
`slang` term (validator rule). Writing checklists say where a register fits (slang is fine in a text message,
not in a debate article or an email to a manager).

## 5. Items and scoring (10 items per exercise)

| Skill | Items | Scoring rule |
|---|---|---|
| Reading | multiple choice (≥3 options, shuffled per attempt), true/false, vocabulary-in-context | 1 / 0 |
| Listening | 8 multiple choice or true/false + 2 dictation sentences | dictation by word-level similarity: ≥ 0.9 → 1, ≥ 0.7 → ½ |
| Writing | 4 inflection gaps, 3 word-order builds (tap chips), 3 translations | gap: exact → 1, only å/ä/ö wrong or one typo in a word of 6+ letters → ½; order: exact sequence → 1; translation: keyword groups (stems) all → 1, ≥ half → ½ |
| Speaking | 6 read-aloud + 4 short answers | read-aloud: similarity ≥ 0.85 → 1, ≥ 0.6 → ½; answers: keyword groups; best of 3 attempts; self-assessment 0 / ½ / 1 without recognition |

Rules learned the hard way:
- Keyword stems shorter than 2 letters match almost everything (a stem `s` accepted any answer). Validator rule.
- Every model answer must score full marks against its own keywords; every canonical word-order sentence must
  rebuild from its chips; avoid commas inside word-order sentences (they end up glued to chips).
- No digits in spoken targets (dictation, read-aloud): recognisers and learners write numbers inconsistently.
- Free writing has no reliable automatic score: offer it unscored with a checklist, a model text, a word counter
  and an auto-saved draft.

## 6. Speech in the browser

- Synthesis: `speechSynthesis` with a voice whose `lang` is the target (exact, then prefix). Voices load
  asynchronously (`voiceschanged`). Speak sentence by sentence; long single utterances get cut off in some
  browsers. Offer speed (0.7 / 0.9 / 1.05), play-by-part, stop, and a transcript revealed after listening. Show
  which voice was found and what to do if none was.
- Recognition: `SpeechRecognition || webkitSpeechRecognition`, `lang` set to the target, `maxAlternatives = 3`,
  score the best alternative. Supported in Chromium browsers and Safari; Firefox only behind a flag. Chrome sends
  audio to a server – say so on the about page. Always provide the self-assessment fallback and a manual switch to it.
- Strip markup before speaking.

## 7. App structure (static, no build)

- `index.html`, `assets/app.js` (router, storage, renderers), `assets/scoring.js` (pure functions, unit-tested
  under `node --test`), `assets/style.css`, `data/manifest.json` (theme order), `data/themes/<id>.json`.
- Hash routes: `#/`, `#/ovning/<theme>/<kind>`, `#/om`. Previous/next links follow manifest order × skill order;
  "Continue" on the index jumps to the first exercise below full marks.
- Storage: one versioned key; wrap every `localStorage` call in try/catch and tell the learner when saving failed.
- DOM pitfall: `append`/`replaceChildren` do not flatten arrays and turn `null` into the text "null". Use a helper
  that flattens and filters; an index with missing cards was caused by passing arrays.
- Test hooks: set `data-ready` on `<html>` after data loads and `data-route` after each render, so tests wait for
  the right page instead of racing hash changes.

## 8. Verification

1. **Data validator** (`scripts/validate.mjs`, uses `scripts/scoring.js`): structure, exactly 10 items per
   exercise, answer indices in range, no duplicate options, markup well-formed with known labels, slang present in
   each reading text, length bounds, keyword stems ≥ 2 letters, model answers hit their keywords, word-order
   canonical sentence rebuilds, no digits in spoken targets, https sources.
2. **Browser tests** with Playwright and a fake Web Speech API injected by `addInitScript` (synthesis records what
   was spoken; recognition returns `window.__say`). For every exercise: correct answers score 10, deliberately wrong
   answers score ≤ 2 (a check that can fail), retry clears the score, stored best/last/attempts are right. Also:
   scores persist across reloads, next/previous walk the whole sequence, the half-point rule, markup is not read
   aloud, the self-assessment fallback scores 10 when recognition is absent.
3. **Visual check**: screenshot the index, a reading page with an opened slang tooltip, and a writing page in a
   phone viewport (Playwright `devices["Pixel 7"]`) and look at them.
4. **CI**: pinned action SHAs, `npm ci` from a lockfile, validator then tests. Generate the lockfile in a clean
   directory: a lockfile made next to a symlinked `node_modules` records a local `link` and CI fails.

## 9. Learner trial gate (`G-LEARN`)

After CI is green and Pages is deployed, the human (ideally a learner at the target level) completes one exercise
of each skill on their own phone. Evidence bundle: site URL, CI run, deployment run, list of themes with dates and
sources, browser support notes. Questions:
1. Did each exercise take roughly the intended time?
2. Was any answer marked wrong that you think is right (or the reverse)? Which item?
3. Did listening and speaking work on your device and browser? Which ones?
4. Were slang and colloquial words clearly labelled and correctly explained?
5. Is any content out of date, unclear or one-sided?

Responses: `proceed`, `iterate: <notes>` (fix the items, re-run the validator and tests, redeploy, ask again;
at most 3 rounds), `proceed-with-rescope: <text>`, `stop`. Each wrongly scored item becomes a validator or test
case before it is fixed.

## Files

- `scripts/scoring.js` – scoring and markup functions from the reference implementation.
- `scripts/validate.mjs` – the data validator; expects `assets/scoring.js` and `data/manifest.json` relative to
  the project root (adjust the import path when copying).
- `references/theme-schema.md` – the theme JSON format with an example.
- `evals/evals.md` – prompts with expected behaviour.
