# Evals for proper-english

Each case gives an input and the expected outcome. A passing run applies the rule and leaves acceptable text alone.

| # | Input | Expected |
|---|---|---|
| 1 | "The repo has neither a README or a licence." | "neither a README nor a licence" (rule 1.1) |
| 2 | "The repo has no README nor licence." | "no README or licence" (rule 1.2) |
| 3 | "The repo has no README or licence." | Unchanged. Grammatical; optional style variant "neither a README nor a licence" (choosing section) |
| 4 | "I can't neither build nor test it." | "I can neither build nor test it." (rule 1.3) |
| 5 | "She neither wanted to sing nor to dance." | "She wanted neither to sing nor to dance." (rule 1.4) |
| 6 | "Neither the tests nor the linter pass." | "Neither the tests nor the linter passes." (rule 2, nearer subject singular) |
| 7 | "Neither the linter nor the tests passes." | "Neither the linter nor the tests pass." (rule 2) |
| 8 | "Running the build, the file was missing." | Rewritten with a doer: "When I ran the build, the file was missing." (rule 3) |
| 9 | "The change touches less files." | "fewer files" (rule 4) |
| 10 | "Fewer than 5 kilograms" | "Less than 5 kilograms" (rule 4, measures) |
| 11 | "Split the work among the two of us." | "between the two of us" (rule 4) |
| 12 | A bullet "- No README" in a checklist | Unchanged. A label, not a sentence (scope) |
