# Author's statement for the reviewer of `b158-confirm-reports2\claude.md`

Your confirmation report on ccc046bb was CONFIRMED. In it, you accepted the author's decision to keep 腰掛け in the word 升's exclusions. This revision removes that exclusion, removes one exclusion from the kanji card 匿, and applies your optional note. This statement answers only the points in YOUR report and the decisions that reverse them.

- **Labels:** F1 is your disposition of the 腰掛け exclusion, O1 is your Optional note, and N1 is the new 匿 change.
- **Why the exclusions changed:** another confirmation reviewer reported both exclusions as minor defects, and a third reviewer called them precautionary.
- **What this text is:** the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence.
- **Line numbers** refer to the revised files in this packet.
- **What changed:** `kanji\匿.md` (one front-matter line), `words\升.md` (one front-matter line and one body line), `words\勲章.md` (one spelling), the ledger (two exclusion rows) and the regenerated `manifest.json`. See `CHANGES.md`.

Give a disposition for each of F1, O1 and N1, and say whether the revision introduces any new defect.

## Reversed decision

### F1: the word 升 no longer excludes 腰掛け

Author action: **exclusion removed; the sourced contrast stays on the article**.

- **What changed:**
  - `words\升.md:8` is now `quiz_exclusions: [箱, 容器, 入れ物, ケース, 計る, 測定, 計, 容積]`.
  - The ledger's word-exclusion row for 升 (`docs\n1-sources\batch-158-progress.json`, lines 327–337) no longer lists 腰掛け.
  - Line 28 keeps the contrast with JMdict 1288370, and line 34 still lists 1288370, so the pinned selection and extract are unchanged.
- **Why the author reversed it:**
  - `docs/content-format.md` line 124 asks for pairs authored from evidence about the displayed labels, and line 129 asks the author to check the titles against the target's ordinary meanings. “Measuring box” and “seat; bench” share no displayed meaning.
  - Line 115 keeps useful comparisons in the body even when they are unsuitable as wrong answers.
  - Your own report called the exclusion “a harmless guard” and the remedy “keep-with-reason or remove”. The other reviewer showed that the guard has no displayed-label basis.
  - In Batch 139 the repository removed exclusions like this one. 峠 excluded 通 and 経 on a shared “pass”; a reviewer returned NEEDS FIX, and fix `3b6f9727` removed both. `kanji/峠.md:49` keeps the contrast in the body.
  - The excerpts are in `evidence\exclusion-precedents.md`.
- **Effect on quizzes** (`evidence\word-quiz.txt`, block from line 1690):
  - 腰掛け is now one of 669 words tied at the last-slot score 5 (line 2215). 俵 is still the one candidate above it.
  - If drawn, “seat; bench” is a wrong answer for 升 “measuring box”: the title shows only sense 1, and the article says sense 2 is a whole box of seating, not a single seat or bench.
  - The reverse section has no row for 腰掛け, so questions on 腰掛け still cannot draw 升.

## Optional note

### O1: split 升.md:28

Author action: **applied, with different wording**. Line 28 now ends with two sentences: “[腰掛け](腰掛け.md) (こしかけ) is a seat or bench (JMdict entry 1288370). In its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench.”

- The split comes at the former semicolon.
- The author kept “a whole box of seating” rather than your suggested “a box of seats”. Line 15 calls a 升席 a tatami “box seat” for four people, so the whole box is what 升 names, not one seat in it.
- “Not a single seat or bench” keeps both words of 腰掛け's title.

## New change

### N1: the kanji card 匿 no longer excludes 皮

Your report did not review this exclusion. The author includes it because it reverses a choice another reviewer had made.

- **What changed:**
  - `kanji\匿.md:14` is now `quiz_exclusions: [隠, 秘, 密, 潜, 伏]`.
  - The ledger's kanji-exclusion row for 匿 (lines 427–434) no longer lists 皮.
  - Line 40 still explains the difference: 皮 “skin; hide” shares only the English word “hide,” there meaning an animal skin.
- **Why:** the titles “hide; shelter” and “skin; hide” share an English homograph only. The Batch 130 notes say English homographs alone do not compel guards, and the 峠 precedent above is the same case.
- **Effect on quizzes:**
  - `checks\quiz-safety.txt` is unchanged apart from its header.
  - 匿's curated distractors (父 魚 年) and 皮's (波 彼 坂) fill all three wrong options of each card's meaning and reading questions, so neither card's question can draw the other.
  - A third card's question can now show both as wrong options, which adds no second correct answer.

## Also changed

`words\勲章.md:15` now spells “honor” instead of “honour”, matching `kanji\勲.md` (a third reviewer's optional note).
