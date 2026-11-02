# Evals for proper-english

Each case gives an input and the expected outcome. A passing run applies the rule and leaves acceptable text alone.

| # | Input | Expected |
|---|---|---|
| 1 | "The repo has neither a README or a licence." | "neither a README nor a licence" (2.1) |
| 2 | "The repo has no README nor licence." | "no README or licence" (2.2) |
| 3 | "The repo has no README or licence." | Unchanged. Grammatical; optional emphasis form "neither a README nor a licence" (2.4) |
| 4 | "I can't neither build nor test it." | "I can neither build nor test it." (2.8) |
| 5 | "She neither wanted to sing nor to dance." | "She wanted neither to sing nor to dance." (2.5) |
| 6 | "Neither did he oversleep nor was his bus late." | "He neither overslept nor missed his bus." (2.6) |
| 7 | "Neither the tests nor the linter pass." | "Neither the tests nor the linter passes." in formal prose (3) |
| 8 | "Neither the linter nor the tests passes." | "Neither the linter nor the tests pass." (3, plural second) |
| 9 | "Walking home, my phone rang." | "While I was walking home, my phone rang." (4) |
| 10 | "The change touches less files." | "fewer files" (5) |
| 11 | "It took less than three weeks." | Unchanged. Time period treated as one amount (5) |
| 12 | "Please organize the data and analyze it." | "organise" and "analyse" (1, spelling) |
| 13 | "The colour of the defense is grey." | "defence" (1); "colour" and "grey" unchanged |
| 14 | "He said \"ship it\" on Friday." | "He said ‘ship it’ on Friday." (1, single quotation marks) |
| 15 | A function named `initialize()` in a code block | Unchanged. Identifier (scope) |
| 16 | A quotation from an American source: "The color is gray." | Unchanged. Quoted text keeps its spelling (scope) |
| 17 | A bullet "- No README" in a checklist | Unchanged. A label, not a sentence (scope) |
