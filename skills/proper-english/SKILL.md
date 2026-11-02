---
name: proper-english
description: Use whenever writing or editing prose that people will read (READMEs, commit messages, documentation, comments, reports, replies) so that it is grammatically correct British English: spelling, punctuation, paired conjunctions (neither/nor), agreement, parallel structure, modifiers, fewer/less.
---

# Proper English (British)

Write prose that a careful British copy-editor would pass. Apply the rules below to every sentence written for a reader and to any text you edit. The bracketed numbers point to entries in `references/sources.md`, which gives the authority, what it supports, and whether its text was read. Where a rule rests on no retrieved British authority, it is marked **[unverified]**; follow it, and verify it against the works listed under "Consult" in the sources file before extending it.

## Variety and scope

- **Variety:** British English throughout: spelling, punctuation, vocabulary and date style. American forms are errors in this skill, except inside quotations, code identifiers, file names, product names and API fields, which stay as written.
- **Applies to:** README and documentation text, commit and pull-request messages, code comments, human-facing error and log messages, reports, emails and chat replies.
- **Does not apply to:** quoted text, code, and deliberate fragments in lists or tables (a bullet "No README" is a label, not a sentence). Do not "correct" the user's quotations.

## 1. British spelling and punctuation

### Spelling

| Use | Not | Source |
|---|---|---|
| -ise, -isation (organise, recognise, organisation) | -ize, -ization | [7][9] |
| -yse (analyse, paralyse, catalyse) | -yze | [7][9][10] |
| -our (colour, behaviour, favour) | -or | **[unverified]** |
| -re (centre, metre, fibre) | -er | **[unverified]** |
| defence, offence (-ce nouns) | defense, offense | [12] |
| licence (noun), license (verb); practice (noun), practise (verb) | licence or practice as the verb | **[unverified]** |
| grey, cheque (payment), catalogue | gray, check (payment), catalog | **[unverified]** |
| programme (a plan or schedule); "program" for a computer program | program (plan), programme (software) | **[unverified]** |

Notes:
- The University of Oxford's own style guide prescribes -ise and -yse. Oxford University Press uses -ize with -yse ("Oxford spelling") in its publications. This skill follows the University guide and mainstream UK practice, so use -ise. If the user asks for Oxford spelling, switch to -ize and keep -yse. [7][9]
- A few words keep -ize whatever the house style (capsize, seize, prize meaning "to value"). Words such as advertise, comprise, revise and supervise take -ise because the ending is not the -ize suffix. Do not alter these. [10] (-ise words: consult *New Hart's Rules*.)
- Spelling inside a quotation, identifier or proper name is left alone (a function called `initialize`, an American company name).

### Punctuation

- Use **single quotation marks** for quotations, speech and titles of short works; use double quotation marks for a quotation inside a quotation. [7][8]
- Put a full stop or comma **outside** the closing quotation mark unless the punctuation belongs to the quoted sentence. [11] (secondary source; check against *New Hart's Rules*.)
- Write dates as day, month, year ("2 November 2026"), without ordinal suffixes in running text. **[unverified]**
- Use a serial (Oxford) comma only where it prevents ambiguity or where the document already uses one; keep the document's existing practice. **[unverified]**

## 2. Paired conjunctions (neither … nor, either … or, both … and, not only … but also)

1. **Complete the pair.** "Neither" is answered by "nor", "either" by "or", "both" by "and". Write "neither X nor Y", never "neither X or Y". [1][2]
2. **After "no", "not", "never" or "without", use "or"; do not use "nor".** "The repository has no README or licence" is correct. "No README nor licence" is wrong. **[unverified]**
3. **Reserve "nor" for a pair opened by "neither", or for a second clause that follows a negative clause** ("It has no README, nor does it have a licence"). [2]
4. **Choosing the form.** For two negated items, "no X or Y" and "neither X nor Y" are both grammatical. Use "neither … nor" when the sentence needs the emphasis or the pairing; otherwise keep whichever form is already written. Do not rewrite a correct "no X or Y" into a wrong "no X nor Y".
5. **Parallel structure.** Place "neither" (and each first member of a pair) directly before the element it governs, and make the element after "nor" the same kind of thing. Test: delete the pair words; the two remaining pieces must have the same shape. [2]
   - Wrong: "She neither wanted to sing nor to dance."
   - Right: "She wanted neither to sing nor to dance."
   - Wrong: "The project requires neither significant funding nor takes a long time."
   - Right: "The project requires neither significant funding nor a long time."
6. **Prefer coordination below clause level.** Do not open a main clause with "Neither" and then continue with "nor" and an inverted clause ("Neither did he oversleep nor was his bus late" is ungrammatical). Coordinate the verb phrases instead: "He neither overslept nor missed his bus", "We are neither trying to keep out immigrants nor favouring the well-to-do". [2]
7. **Three or more items** may use "neither … nor … nor …". [2]
8. **Do not stack a second negative on "neither".** Write "I can neither build nor test it", not "I can't neither build nor test it". **[unverified]**

## 3. Agreement with "or" and "nor"

- Two singular subjects joined by "neither … nor" or "either … or": write the verb in the **singular** in formal prose. A plural verb is recorded as more informal. [1]
- One singular and one plural subject: some writers follow the proximity rule (the verb agrees with the nearer subject). To satisfy both conventions, **put the plural subject second and use a plural verb**: "Neither the tests nor the linters pass." [3]
- After "neither" or "either" used alone as a subject, the verb is singular: "Neither candidate was selected." "Neither of …" takes a plural noun or pronoun and is followed by a singular verb in formal prose. [1]
- Phrases between subject and verb do not change the subject's number. **[unverified]**

## 4. Modifiers

- A modifier must sit next to the word it modifies, and that word must be in the sentence. [6]
- **Dangling participle:** an opening "-ing" phrase whose implied subject is not the subject of the main clause. Wrong: "Walking home, my phone rang." Right: "While I was walking home, my phone rang." Fix by naming the doer or turning the phrase into a clause. [6]
- Place limiters (only, just, almost, nearly) directly before the word they limit. **[unverified]**

## 5. Fewer and less

- Use "fewer" with countable nouns (fewer errors, fewer people); use "less" with uncountable nouns (less sugar, less time). [4]
- "Less than" is acceptable and ordinary before a number, a period of time or a sum of money, which are treated as one amount: "less than ten times", "less than three weeks", "less than five pounds". "Fewer than" is the more formal form for separate countable items. [4]
- Usage guides record that real usage is more complicated than the simple rule, so apply the rule to the writer's own sentences and do not "correct" established idioms ("one less thing", "no less than"). [5]

## 6. Between and among

Use "between" for two items, and for relations among three or more items considered pair by pair ("a treaty between three states"); use "among" for something within a group or mass ("among the contributors"). **[unverified]** against a British authority; consult the OED entries for *between* and *among* before changing existing text. Do not change an existing correct use.

## Procedure for any text you write

1. Draft the sentence in British English.
2. Check spelling against the table in section 1 (-ise, -our, -re, -ce/-se, grey, programme/program).
3. Check quotation marks and the position of closing punctuation.
4. Find every negative (no, not, never, none, without, neither, nor) and every "or", "and", "either", "both". Check section 2 and section 3.
5. Find every sentence that opens with an "-ing" or "to" phrase. Check that the next subject is the doer (section 4).
6. Find every "less", "fewer", "between", "among". Check sections 5 and 6.
7. Fix silently. Tell the user about a correction only when it changes meaning or when the user asked for a review.

## Reviewing someone else's text

Report each problem with the quoted fragment, the section and rule number, and the corrected fragment. Separate **errors** (breaks a rule above) from **style options** (both forms are correct). Do not flag acceptable variants (for example "no README or licence").

## Extending this skill

Add a rule only when its source has been read and recorded in `references/sources.md` with publisher, edition or URL, and the claim it supports. Prefer British academic and publisher sources: the *Oxford English Dictionary*, Oxford and Cambridge University Press reference works, *Fowler's Dictionary of Modern English Usage*, *The Cambridge Grammar of the English Language*, and university and learned-society style guides. Do not cite American style manuals or dictionaries as authority for British usage. Mark any rule without such a source **[unverified]**. Apply `timeless-skill-writing` to additions.
