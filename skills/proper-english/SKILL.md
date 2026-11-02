---
name: proper-english
description: Use whenever writing or editing prose that other people will read (READMEs, commit messages, docs, comments, reports, replies) to keep it grammatically correct: paired conjunctions (neither/nor, either/or), agreement, parallel structure, modifiers, fewer/less, between/among.
---

# Proper English

Write prose that a careful editor would pass. Apply the rules below to every sentence you produce for a reader, and to text you edit. Rules are sourced; the numbers in brackets point to entries in `references/sources.md`. Where authorities disagree, the rule says so, and you follow the stricter reading unless the user asks otherwise.

## When it applies

- Applies: README and doc text, commit and pull-request messages, code comments, error and log messages written for humans, reports, emails, chat replies.
- Does not apply: quoted text, code identifiers, file names, and deliberate fragments in lists or tables (a bullet such as "No README" is a label, not a sentence). Do not "correct" the user's quotations.

## Rules

### 1. Paired conjunctions (correlatives)

Pairs: both … and, either … or, neither … nor, not only … but also. [1][2]

1. **Always complete the pair.** "Neither" takes "nor"; "either" takes "or"; "both" takes "and". Write "neither X nor Y", not "neither X or Y". Dictionaries record "neither … or" as neither archaic nor wrong, but "nor" is the usual partner, so use "nor". [3][4]
2. **After "no", "not", "never" or "without", use "or", not "nor".** "Not peanut butter or jelly" takes "or". [4] Reserve "nor" for a pair opened by "neither", or for a second clause that follows a negative clause ("She has no README, nor does she have a licence"). [3]
3. **Do not stack a second negative on "neither".** Write "I can neither see it nor hear it", not "I can't neither see it nor hear it". [5]
4. **Parallel structure.** The same part of speech or construction must follow each half of the pair, so place the first word directly before the element it governs. Test: delete the pair words; the two remaining pieces must have the same shape. [1][6]
   - Wrong: "She neither wanted to sing nor to dance." ("neither" precedes a verb, "nor" precedes an infinitive)
   - Right: "She wanted neither to sing nor to dance."
   - Wrong: "The project requires neither significant funding nor takes a long time."
   - Right: "The project requires neither significant funding nor a long time."
5. **Do not put a comma between the pair's parts** when both halves belong to one verb: "Neither you nor I should wear pastels". [5]
6. **A series of three or more items** may use "neither … nor … nor …"; this is accepted. [7]

#### Choosing between "no X or Y" and "neither X nor Y"

Both are grammatical for two negated items. "The repository has no README or licence" is correct English. Use "neither … nor …" when the writer wants the pairing to stand out or the sentence has a negative verb phrase to avoid; otherwise either form passes. Do not "fix" a correct "no X or Y" into a wrong "no X nor Y". [4]

### 2. Subject-verb agreement with "or" and "nor"

- Two singular subjects joined by or, nor, either … or, neither … nor take a **singular** verb: "Neither money nor power was important." [8]
- One singular and one plural subject: the verb agrees with the **nearer** subject. "Neither the television nor the radios work." "Neither the radios nor the television works." [8][9]
- When the order allows, put the plural subject second so the verb reads naturally. [10]
- Words that come between subject and verb do not change the subject's number. [8]

### 3. Modifiers

- A modifier must sit next to the word it modifies, and that word must be in the sentence. [11][12]
- **Dangling:** an opening phrase whose implied subject is not the sentence's subject. Wrong: "Turning the corner, a school building appeared." Fix by naming the doer ("Turning the corner, we saw a school building") or by rewriting the phrase as a clause. [11][13]
- Place limiters (only, just, almost, nearly) directly before the word they limit. [14]

### 4. Word pairs

- **Fewer / less:** "fewer" for things you can count (fewer files, fewer failures); "less" for amounts and masses (less memory, less time). Measures and sums take "less": "less than 5 kilograms". [15][16]
- **Between / among:** "between" for two named items or for relationships among items considered individually; "among" for a member of a group or a mass. The rule "between = two, among = more than two" is a simplification; "between" is correct for three or more items when each relation is treated separately. [15][17]

## Procedure for any text you write

1. Draft the sentence.
2. Find every negative (no, not, never, none, without, neither, nor) and every "or", "and", "either", "both". Check rules 1 and 2.
3. Find every sentence that opens with an "-ing" or "to" phrase or a "When/While/After + adjective" phrase. Check that the next subject is the doer (rule 3).
4. Find every "less", "fewer", "between", "among". Check rule 4.
5. If the text is long, read each sentence once more with the subject and verb underlined.
6. Fix silently. Mention a correction to the user only when it changes meaning or when the user asked for a review.

## Reviewing someone else's text

Report each problem with the quoted fragment, the rule number, and the corrected fragment. Do not flag acceptable variants (for example "no README or licence"). Separate **errors** (breaks a rule above) from **style options** (both forms are correct).

## Extending this skill

Add a rule only with a source you have read, and record it in `references/sources.md` with the URL, the publisher, and the claim it supports. Mark disputed points as disputed, with the sources on each side. Apply `timeless-skill-writing` to additions.
