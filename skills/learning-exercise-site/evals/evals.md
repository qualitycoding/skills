# Evals for learning-exercise-site

1. **Prompt:** "Make me ten-minute German reading and listening exercises about this week's news, scored out of 10, on GitHub Pages."
   **Expected:** asks in the first message for any repository/Pages setting the session cannot change; researches the week's news with dated sources; writes original texts with `[[…|…|label]]` register labels; each exercise has 10 items; validator and Playwright tests (fake speech API) pass, including the wrong-answers-score-low check; shows the date and sources on each theme.

2. **Prompt:** "Add a speaking exercise where I answer questions out loud."
   **Expected:** uses `SpeechRecognition || webkitSpeechRecognition` with the target `lang`, keyword-group scoring with stems ≥ 2 letters, best of three attempts, a self-assessment fallback and a manual switch to it; spoken targets contain no digits; a test covers the fallback.

3. **Prompt:** "Write a listening script where the Prime Minister explains why she resigned."
   **Expected:** does not invent the person's words; uses only sourced statements (short quotes or paraphrase) or reframes as a neutral news report; labels the script as written for the exercise.

4. **Prompt:** "Mark the slang so I know not to use it at work."
   **Expected:** distinguishes `slang` from colloquial (`vardagligt`) and `idiom`; tags render on every occurrence and in the glossary; writing checklists say which register fits the task.

5. **Prompt:** "Scores disappear when I switch from my phone to my laptop."
   **Expected:** explains that `localStorage` is per browser; offers the export/import JSON on the about page rather than adding accounts.

6. **Prompt:** "The news in the exercises is a week old. Keep it fresh automatically."
   **Expected:** writes `REFRESH.md` in the project repository (append-only units with dated ids, topic rotation, fail-closed publishing), adds a live-site check workflow if there is none, creates a weekly cloud scheduled task whose prompt probes push access and follows `REFRESH.md`, and tells the owner the first run time and the task's approval setting.
