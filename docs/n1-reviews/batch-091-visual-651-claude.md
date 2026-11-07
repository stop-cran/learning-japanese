**Snapshot:** Frozen signed HEAD 99d11124a5eab51850be91b15c0ebd224af7f8ce. The packet's teaching diff from c2a59d5c1cd4ac8040156a6c067bd9d565d59116 is empty. The packet hashes match my earlier reads: `kanji/刃.md` 6d299303…, `words/刃.md` 62a51034…. This is a dependent follow-up that adds visual evidence to my earlier reviews, not a new blind review.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), session 075924f2-f60b-4ae0-bf3f-341db3dfbd74, working alone.
- **Text reads (one call each, in order):**
  1. My initial report `batch-091-initial-claude.md`.
  2. My confirmation report `batch-091-confirmation-claude.md`.
  3. The whole `batch-091-visual-651-packet.txt`, with `forceReadLargeFiles=true`. No truncation marker appeared.
- **Image reads:**
  - All 15 listed PNGs: 12 contact sheets (23 representative frames that the packet maps to 47 captures) and the 3 original Compose font panels.
  - One extra original capture, `n1-091-meaning-question.png`, viewed at full size to see the 刃 glyph more clearly.
- **Process deviation:** I sent the 15 listed image views in a single batched response, not one per response as required. Every image loaded and I inspected each one. The four text and extra-image reads were each in a separate response.
- **Provenance:** The native-run results (route JSON and execution receipt) are coordinator receipts, not tests I ran.

**Verdicts:**
- **`kanji/刃.md`:** correctness CLEAN; scoped coverage CLEAN; rendered comprehensibility NEEDS FIX (Finding 1). Correctness and coverage carry over from my earlier text reviews, and the screenshots match that text.
- **`words/刃.md`:** correctness CLEAN; scoped coverage CLEAN; rendered comprehensibility CLEAN. Correctness and coverage carry over from my earlier reviews; nothing in the screenshots contradicts them.

**What the screenshots show for `kanji/刃.md`:**
- **Complete article:** captures kanji-01, 03, 09, 11, 24 and the bottom frame together show the whole article.
- **Reading table:** it scrolls sideways and says "Scroll sideways to read all columns." Kanji-11 and kanji-24 show the right-hand columns in full. The rows are in source order (ジン, ニン, は, やいば, き.る), and only the は row links to the word article.
- **Earlier labelling preserved:** the mnemonic is still labelled "modern-shape mnemonic, not etymology". The 乃, 凹 and 凸 note and the Common words list (刃物 はもの) are intact.

**What the screenshots show for `words/刃.md`:**
- **Complete article:** blade-02, 07 and 09 show the whole body, down to the dictionary line.
- **Unchanged content:** both examples render with their kana and translations, along with the の and が notes and the 端/縁 contrast. The new 先端 せんたん sentence is visible.
- **Navigation:**
  - The word and kanji articles link to each other, one link pair in two directions.
  - System Back returns to the right screen in both directions (the paired captures are byte-identical).
  - The extra 先端 link opens the 先端 article, and Back returns to the word article.

**What the screenshots show in practice and quiz screens:**
- **N1 selection:** "N1 · 123 cards".
- **Meaning quiz:** the choices are blade; cutting edge / convex; protruding / thereupon; possessive no / concave; sunken. All three curated wrong cards appear and no fallback choice was needed. The feedback screen is correct.
- **Reading quiz:** exactly one kun'yomi question, with choices はと/でこ/は/ぼこ. Answering は gives "Correct! — kun'yomi", and the session ends "1 of 1 answers correct" with Done. No on'yomi question appeared.
- **Drawing:**
  - The tracing screen shows three numbered strokes.
  - Practice feedback says "Practice only: this attempt is not graded" and "Graded by stroke shapes only (handwriting model not available)".
  - Giving up on recall shows "Here is the kanji" with an empty drawing.

**Fonts (three original Compose panels):**
- All 21 scoped kanji render in all four font settings (Gothic, Mincho, Textbook, Brush).
- 丶 (U+4E36) renders as a down-right dot.
- 刃 and 刀 are distinct in every face, as are 乃, 凹 and 凸. 先 and 端, and 刃物, are clear.
- The faces do not draw 刃 the same way, which matters for Finding 1.

**Findings:**

1. **Minor; rendered comprehensibility.**
   - **Location:** `kanji/刃.md` line 24 (mnemonic) as rendered in the default Gothic text. The large glyph is clearest in the original `n1-091-meaning-question.png`; the same shape appears in contact-05 and contact-11 and in the Gothic row of `n1-091-font-panel-3.png`.
   - **Claim and impact:**
     - In the default Gothic face, 刃's extra mark is a short stroke falling down-left, separate from the long sweeping stroke. It looks like a small ノ, not a 丶.
     - The Mincho, Textbook and Brush rows and the KanjiVG stroke reference used for drawing practice show the mark crossing the sweeping stroke from upper-left to lower-right.
     - The mnemonic tells learners to notice a mark "shaped like 丶". On the default rendering that description does not match what they see, and they then trace a different form in drawing practice.
     - This is not a requirement that all fonts look alike. The problem is that the text points to a shape the default rendering does not show.
   - **Minimal remedy:** Qualify the line 24 description, for example "an extra short mark (some fonts draw it as a small separate stroke; the stroke-order diagram shows it crossing the sweep)". Separately, the app team could check which face the default Gothic setting falls back to. That is outside these two articles.
   - **Evidence:** the full-size quiz glyph versus the drawing reference in contact-06 and contact-07, and the four rows of font panel 3.
   - **Confidence:** high for the visible shape difference. Medium for the learning impact. I did not identify the font face.

**Reconciliation with my earlier reports:**
- **Initial Finding 1 (先端 exclusion and figurative "cutting edge" note):** stays **resolved**; the screenshots show the new sentence and link working.
- **刃傷 gloss:** stays **resolved**.
- **刃/ナイフ hypothesis:** stays **unresolved but not actionable**.
- **"No visual evidence" limit:** **partially resolved** by these emulator captures (no phone).
- **"Fallback behaviour not certified" limit:** **resolved only for the tested N1 setup**, where I saw zero fallback choices. "All" (pool 1,114, zero fallback) comes from the receipt only. Other custom pools and old app versions stay open.
- **Optional notes:** all kept unchanged (the "のはは" kana parsing, the 歯 "tooth" homophone, the 刄 variant, more ジン words). On this screen width, the kana line happens to wrap between のは and はするどい, which helps parsing here.

**Optional:**
- The reading-quiz feedback lists every raw reading of 刃, showing き.る as "きる" without the dot. This is reference feedback, not offered answers, but a learner could take it as an everyday reading. The article already labels き.る as source-only.

**Limits:**
- **Images:** the contact sheets are scaled down (frames 700×1556 from 1080×2400). Only the three font panels and one capture were viewed at original size, and I did not view the other originals.
- **Fonts:** the font face was not identified. The 84 per-character and 4 whole-word rendering checks are recycled hashes from the receipt, not images I viewed.
- **Device:** API 35 emulator only; no physical phone and no native-speaker review.
- **Drawing:** the tracing used injected strokes, not human handwriting, and the offline handwriting model did not run.
- **Builds and content:** the receipt says the run used the test-only Android build 1c1b7bf4, which retains production f9b59a2, not the latest app main. I did not independently verify the content sync figures (one archive download, 1,114 kanji, 5,070 words, zero problems, content version cb3c857f3614485d, reading-parser epoch 1), the two passing native test cases, or the coordinator's LF normalization of manifest hashes.
- **Not certified here:** current main, combined checks, CI, the public ZIP, publication, phone acceptance, general release and the whole N1 set.
- **Learning effectiveness:** not measured.
