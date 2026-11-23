# Author's statement for the reviewer of `b158-confirm-reports\gpt.md`

This statement answers only the points in YOUR confirmation report on ccc046bb.

- **Labels:** F1 and F2 are your Findings 1 and 2, O1 is your Optional note, and L1 is your Limit L1, which you marked PARTIALLY RESOLVED.
- **Your report file:** you could not write your report to the requested file. The author saved your final message, unchanged, as that report.
- **What this text is:** the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence.
- **Line numbers** refer to the revised files in this packet.
- **What changed:** `kanji\匿.md` (one front-matter line), `words\升.md` (one front-matter line and one body line), `words\勲章.md` (one spelling), the ledger (two exclusion rows) and the regenerated `manifest.json`. See `CHANGES.md`.

Give a disposition for each of F1, F2, O1 and L1.

## Findings

### F1: 匿 excluded 皮 on an English homograph

Author action: **changed as you proposed**.

- **Front matter:** `kanji\匿.md:14` is now `quiz_exclusions: [隠, 秘, 密, 潜, 伏]`.
- **Ledger:** the kanji-exclusion row for 匿 (`docs\n1-sources\batch-158-progress.json`, lines 427–434) no longer lists 皮.
- **Card body:** the distinction stays at line 40: 皮 (“skin; hide”) shares only the English word “hide,” there meaning an animal skin.
- **Reasons:**
  - `docs/content-format.md` lines 124 and 129 ask for pairs authored from the displayed labels and ordinary meanings.
  - Line 115 keeps useful comparisons in the body even when they are unsuitable as wrong answers.
  - The repository has removed a pair like this before. In Batch 139, 峠 “mountain pass; peak; climax” excluded 通 and 経, which share only “pass”. GPT returned NEEDS FIX, and fix `3b6f9727` removed both exclusions. `kanji/峠.md:49` keeps them as ordinary wrong options.
  - The Batch 130 notes state that English homographs alone do not compel guards.
  - The excerpts are in `evidence\exclusion-precedents.md`.
- **Effect on quizzes:** `checks\quiz-safety.txt` is unchanged apart from its header line.
  - 匿's curated distractors (父 魚 年) fill all three wrong options of its meaning and reading questions. So do 皮's (波 彼 坂).
  - Neither card's question can draw the other.
  - A third card's question can now show both as wrong options, which adds no second correct answer.

### F2: the word 升 excluded 腰掛け without a direct overlap with “measuring box”

Author action: **changed as you proposed**.

- **Front matter:** `words\升.md:8` is now `quiz_exclusions: [箱, 容器, 入れ物, ケース, 計る, 測定, 計, 容積]`.
- **Ledger:** the word-exclusion row for 升 (lines 327–337) no longer lists 腰掛け.
- **Card body:** the sourced distinction stays at `words\升.md:28`. It is now two sentences: 腰掛け is a seat or bench (JMdict entry 1288370). In its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench. Line 34 still lists 1288370, and the pinned extract keeps the entry.
- **Effect on quizzes** (`evidence\word-quiz.txt`, block from line 1690):
  - 腰掛け “seat; bench” is now one of 669 words tied at the last-slot score 5 (line 2215).
  - 俵 is still the one candidate above it.
  - The reverse section has no row for 腰掛け, so questions on 腰掛け still cannot draw 升.
- **Other reviewers:** one other reviewer had accepted the exclusion as a harmless guard, and another called it precautionary. The author followed your finding because the rule in `docs/content-format.md` line 124 asks for an overlap in the displayed labels, which “measuring box” and “seat; bench” do not have.

## Optional note

### O1: replace “not in this card's metadata”

Author action: **not changed**.

- **Published use:** the phrase is the established wording of the published N1 cards. `evidence\metadata-phrase.txt` lists it in 12 published kanji cards outside this batch (救 椋 泡 淡 渇 滅 滑 漫 潔 炎 甚 環), none changed by this batch.
- **Defined in the card:** the B158 cards that use “source-only” define it in their Notes (偽.md:44, 却.md:43), as your report notes.
- **Consistency:** changing the phrase in this batch alone would make the cards inconsistent. The author leaves any change to a separate, repository-wide pass.

## Limits answered

### L1: the manifest, signed Git objects and kanji-reading builder were not reproduced

Author action: **packet limit, stated as such**. This packet cannot carry the repository's object database or the Android app's kanji reading builder. The author offers the following, and will record this limit in the closure README.

- **Signatures:** `evidence\verify-commit.txt` is a fresh transcript of `git verify-commit -v` and `git log --show-signature` for 60d2cd5a, 6605a8b0, ccc046bb and 348c4f70. It ends with `git rev-list --parents 60d2cd5a^..348c4f70`. The commits form one linear chain: 348c4f70 → ccc046bb → 6605a8b0 → 60d2cd5a → ad1694c1.
- **Manifest:** `checks\manifest.txt` records the manifest's SHA-256 before and after a rebuild at 348c4f70; they are identical and the tracked tree stays clean.
- **Reading quizzes:** `checks\reading-exposure.txt` and `checks\reading-options.txt` model the reading questions with the Python ports named in each output.
