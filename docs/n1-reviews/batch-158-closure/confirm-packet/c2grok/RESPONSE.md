# Author's statement for the reviewer of `b158-confirm-reports\grok.md`

Your confirmation report on ccc046bb was CONFIRMED with no findings. This revision changes two exclusions you judged acceptable, and applies one of your optional notes. This statement answers only the points in YOUR report.

- **Labels:** X9 is your disposition of the 匿/皮 exclusion (originally your review's X9). E2 is your item on 腰掛け under "Other reviews". P1, P2, P3 and P4 are the four points of your Optional note, in order.
- **Why the two exclusions changed:** another confirmation reviewer reported both exclusions as minor defects.
- **What this text is:** the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence.
- **Line numbers** refer to the revised files in this packet.
- **What changed:** `kanji\匿.md` (one front-matter line), `words\升.md` (one front-matter line and one body line), `words\勲章.md` (one spelling), the ledger (two exclusion rows) and the regenerated `manifest.json`. See `CHANGES.md`.

Give a disposition for each of X9, E2, P1, P2, P3 and P4, and say whether the revision introduces any new defect.

## Reversed decisions

### X9: 匿 no longer excludes 皮

Author action: **exclusion removed; the body contrast stays**.

- **What changed:**
  - `kanji\匿.md:14` is now `quiz_exclusions: [隠, 秘, 密, 潜, 伏]`.
  - The ledger's kanji-exclusion row for 匿 (lines 427–434) no longer lists 皮.
  - Line 40 still says 皮 (“skin; hide”) shares only the English word “hide,” there meaning an animal skin.
- **Why:** your original review asked for the exclusion because “hide” appears in both displayed titles. The repository's rule and precedent treat a shared English homograph as insufficient.
  - `docs/content-format.md` lines 124 and 129: author a pair from the displayed labels and ordinary meanings, and check the titles against the target's ordinary meanings, not merely for duplicate strings.
  - Line 115 keeps useful comparisons in the body even when they are unsuitable as wrong answers.
  - Batch 139: 峠 “mountain pass; peak; climax” excluded 通 “pass through; commute” and 経 “pass through; sutra”. As here, the titles shared an English word with a different meaning. A reviewer returned NEEDS FIX, and fix `3b6f9727` removed both exclusions. `kanji/峠.md:49` explains the difference in the body and keeps them as ordinary wrong options.
  - Batch 130 notes: “shared topics, materials and English homographs alone do not compel guards.”
  - The excerpts are in `evidence\exclusion-precedents.md`.
- **Why a learner is not misled:** “hide” in 皮's title is the noun (an animal skin), listed after “skin”. 匿's title is the verb sense, paired with “shelter”. Neither title is a correct meaning answer for the other kanji.
- **Effect on quizzes:**
  - `checks\quiz-safety.txt` is unchanged apart from its header.
  - 匿's curated 父 魚 年 and 皮's curated 波 彼 坂 fill all three wrong options of each card's meaning and reading questions, so neither card's question can draw the other.
  - A third card's question can now show both as wrong options, which adds no second correct answer.

### E2: the word 升 no longer excludes 腰掛け

Author action: **exclusion removed; the sourced contrast stays**.

- **What changed:**
  - `words\升.md:8` drops 腰掛け.
  - The ledger's word-exclusion row for 升 (lines 327–337) drops it too.
  - Line 28 keeps the contrast with JMdict 1288370, now split into two sentences for readability (another reviewer's optional note; see `CHANGES.md`).
- **Why:** you judged the pair “not a title overlap with ‘measuring box’” and precautionary. The rule at `docs/content-format.md` line 124 asks for evidence about the displayed labels, which these two titles do not share. The contrast belongs in the body, as line 115 says.
- **Effect on quizzes** (`evidence\word-quiz.txt`, block from line 1690):
  - 腰掛け is now one of 669 words tied at the last-slot score 5 (line 2215). 俵 is still the one candidate above it.
  - The reverse section still has no row for 腰掛け, so questions on 腰掛け cannot draw 升.
  - Your report's point about 席, 座席 and 客席 is unaffected: they remain outside the reachable set.

## Optional note

### P1: 勲章 “honour” and 勲.md “honor”

Author action: **changed**. `words\勲章.md:15` now reads “an honor awarded for service”, matching `kanji\勲.md` lines 23 and 40. Across `kanji\` and `words\`, 186 lines contain a word starting “honor” and 8 a word starting “honour”, so the author chose “honor”.

### P2: 傍系 compresses JMdict 1518840

Author action: **not changed**. You noted that the wording is not false and matches Daijisen's sense of departing from the main line.

### P3: the 意見 and 腰掛け exclusions are precautionary rather than title-identical

Author action: **腰掛け removed (E2); 意見 kept**.

- **意見 on 偏見** (`words\偏見.md`) is unchanged. The titles “opinion” and “prejudice; bias” both name a view held about something. Line 28 explains the difference: 意見 is an opinion or view in general (JMdict entry 1156530), and 偏見 is a view that leans to one side.
- **Why 意見 differs from 腰掛け:** the two displayed labels name the same kind of thing, a view. “Seat; bench” and “measuring box” do not, and a shared English word alone is not a reason.
- If you think 意見 should also go, say so with your reason.

### P4: 耳 山 白 can be rejected by category

Author action: **not changed**. You noted this is not a meaning collision, and the batch's other starter distractor sets behave the same way.
