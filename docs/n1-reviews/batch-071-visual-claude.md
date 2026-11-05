**Native visual confirmation: 允 / 允可, batch 071**

None of the 22 screenshots changes my original verdicts; all six remain CLEAN, with no findings.

**Snapshot:** Teaching files are at `1dc352148065c47d6d3a33206c62f3b877e678f6` and unchanged. The evidence is at HEAD `43016306901a1111e309e7081e90db258cbc5f2d`, with native envelope `f6ff96a109f3e7b6a67f41e6b9ee214962c9a39f`. The model is Claude Opus 5.5 (`claude-opus-5.5`).

**Scope:**
- **Text reads:** the task file, my original report, `kanji\允.md` and `words\允可.md` in full, the native test fixture in five ranges (`[1,120]` through `[481,-1]`), `instrumentation.txt` and `n1-071-article-route.json`.
- **Screenshots (22):** font pairs; kanji views 01, 03, 09, 11, 20 and 24; word views 02, 03 and 07; the link from 允可 to 允; System Back in both directions; the on'yomi question, feedback and Done screens; the meaning question and feedback; drawing trace, feedback and recall.
- **Execution:** this run used one tool call per response, with no deviations. My initial review read the two halves of `copilot-instructions.md` in parallel; that run was not fully serial.

**Verdicts** (correctness, scoped coverage, comprehensibility):
- 允: CLEAN, CLEAN, CLEAN.
- 允可: CLEAN, CLEAN, CLEAN.

**Evidence layers:**
- **Inherited:** the lexical conclusions from my original review are unchanged.
- **New, from the pixels:**
  - **Glyphs:** every face shows 允 with 厶 above 儿, including large Gothic and Mincho renders.
  - **Readings quiz:** options イン, ハン, ケン and リン; "Correct! — on'yomi"; the feedback line lists イン、じょう、まことに、ゆるす. No kun'yomi question appeared, and Done showed "1 of 1 answers correct."
  - **Meaning quiz:** the wrong options (camphor tree, chestnut, hawk; falcon) don't overlap with "permit; sincerity".
  - **Drawing:** the stroke order is fold, dot, ノ, 乚. Tracing feedback says "Practice only: this attempt is not graded" and "Well drawn!"; recall feedback says "Here is the kanji".
  - **Navigation:** the 允可 link and System Back both work in each direction. The N1 stack shows 103 cards.
- **Supplied, not run by me:** 2 tests passed; 0 import problems; a persisted reading grade 3 and drawing grade 1.

**Findings:** none.

**Optional:**
- My original suggestions stand:
  - Explain the うた + の + じょう reading in 雅楽允.
  - Say "Osaka-prefecture publication" instead of "governmental text".
  - Cite 允文允武 for the "truly" sense.
  - Drop the unprompted "emperor" mention.
  - 従う not being excluded is acceptable.
- New polish: "character-dictio/nary" wraps mid-word without a hyphen.

**Limits:**
- **Display:**
  - The readings table's third column is clipped unless scrolled sideways. The hint is present, and the right-offset views show the full text.
  - The top heading of 允可 never appears in a screenshot.
  - In the Textbook row, 儿 and 厶 render in a heavier, probably fallback, face. Which face was used is not identified.
- **Drawing:** grading used stroke shapes only ("handwriting model not available"), not ML Kit recognition.
- **Grades:** no new meaning grade is persisted.
- **Device:** emulator API 35 only, screenshots resized to 900×2000, no physical phone. Android f9b59a2 or later is required.
- **Not a general-release check:** this does not cover the whole set, latest main or publication.
- **Not re-checked:** N1 membership. The 許/允 title overlap in larger quiz pools remains a risk.
- **Not done by me:** fresh source retrieval and running the native tests.
