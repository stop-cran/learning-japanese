## Batch 067 visual confirmation, execution 436: complete report

**Snapshot:** Evidence HEAD is `a6c57b57f7c90f5a9c78e5bdf953bd2df768d5ed`. Teaching is supplied as unchanged from `5cb2ea4bc804ac218b17d5c583d4fba95e60971c`. The native Git envelope source is `a45ce3014661487bf16977260daa5ca23e001663`. I could only use view, so I did not verify any of these commits myself. I found no uncommitted teaching edits.

**Scope:** Claude Opus 5.5, in the same session as my original initial review. This is a dependent visual confirmation, not a blind review, dictionary audit or native rerun.

- **Text read:**
  - The task file.
  - My original report `batch-067-initial-claude.md` (complete).
  - Fresh complete reads of `kanji\僧.md`, `words\僧侶.md` and `words\坊さん.md`.
  - `N1Batch067NativeTest.kt` in ranges 1–140, 141–280, 281–420 and 421–518.
  - `instrumentation.txt` and `n1-067-article-route.json`, both complete.
- **Images:** all 23 PNGs, each viewed on its own. They displayed at about 900×2000, apparently scaled down from the 1080×2400 source. I did not see raw pixels.
- **Deviation:** I viewed `instrumentation.txt` and the route JSON in one response with two calls. That broke the one-call rule. Every other read was serial.
- **Images that look the same:** I can't compute hashes, but these pairs look identical apart from, at most, the clock. Each pair counts as one scene, not two independent ones:
  - `bousan-boy-boundary` and `bousan-changed-comparison`
  - `clergy-catholic-boundary` and `clergy-person-temple-boundary`
  - `clergy-kanji-backlink` and `kanji-compound-reading-boundary`
  - `bousan-meaning` and `bousan-directions-example`

**Verdicts:**
- **`kanji\僧.md`:** correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**.
- **`words\僧侶.md`:** correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**.
- **`words\坊さん.md`** (line 30 only; the rest is context): correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**.

Each verdict rests on three separate kinds of evidence:

- **Inherited lexical conclusions** come from my original review and keep all of its limits. They are unchanged.
- **New pixel evidence** comes from the images below.
- **Operational assertions** were supplied to me, not run by me.

**What the images actually show:**

- **僧 card**
  - Shown across `kanji-radical`, `kanji-components`, `kanji-compound-reading-boundary`/`clergy-kanji-backlink` and `kanji-collective-sense`.
  - Facts line: Strokes 13 · Key (radical) 人 (as 亻, no. 9) · JLPT N1.
  - Meaning text says Buddhist clergy, "not simply anyone who believes in Buddhism", and links 僧侶.
  - Components sentence shows 亻, a link to 人, and 曽. "Modern-shape mnemonic:" is labelled and says it is not a historical or phonetic explanation.
  - Readings table:
    - The unshifted view shows the first column (ソウ) and the Type column (on).
    - The "Typical words" cell is cut off at the right edge ("Buddhist pries…") in the unshifted view. The sideways-shifted view shows the whole cell: "Buddhist priest; monk".
    - The sideways-scroll hint is visible.
  - Also fully visible:
    - The ソウ / no-kun sentence, and 小僧 こぞう glossed as boy, young monk or apprentice.
    - Common words: the 僧侶 link and 高僧 こうそう.
    - The sangha (collective) note and the scope note on the gloss "priest".
    - The look-alike bullet: 増 with 土; 値 and 倍 with different right-hand parts. It is cut off in one screen but fully visible in `kanji-collective-sense`.
    - The footer (KANJIDIC2, JMdict entries, World Encyclopedia).
- **僧侶 article**
  - `clergy-meaning`:
    - The clerical role, as opposed to every believer.
    - One person or a group.
    - Both examples, with readings and translations.
  - `clergy-catholic-boundary` (all lines visible):
    - 僧 linked and 侶 リョ unlinked.
    - The 坊さん link with a sentence that separates register, not occupation.
    - The 神父 (Catholic priest) contrast.
    - The 寺 person-versus-temple boundary.
    - The full footer.
  - The last footer line is cut off only in `bousan-clergy-backlink`.
- **坊さん article**
  - Line 30 shows the 僧侶 link with そうりょ and the "more formal" sentence.
  - The boy sense, both examples with translations, and the footer are fully visible in `bousan-boy-boundary`.
- **Fonts** (`font-pairs`):
  - All four rows (Gothic, Mincho, Textbook, Brush) render 僧, 増, 値, 倍, 人, 亻, 曽, 侶, 僧侶 and 坊さん.
  - No row has blank glyphs or replacement boxes.
  - 亻 versus 土 (僧 vs 増), the right-hand parts of 値 and 倍, and 人 versus 亻 are distinguishable in every row.
  - Gothic and Mincho look very similar. That is not a defect.
  - ん wraps to a new line in three rows, which is harmless.
- **Quizzes**
  - Reading question: "Pick the on'yomi", with options ソウ, ショウ, ホウ and ボウ. There is no kun prompt.
  - Reading feedback: "Correct! — on'yomi", ✓ ソウ, then the line "Buddhist monk; priest: ソウ".
  - Meaning question options are "vertebra; chinquapin", "mosquito", "Buddhist monk; priest" and "Japanese cedar". These differ from the authored look-alike cards 増, 値 and 倍. Only one option is correct, so this displayed set is unambiguous. I am not certifying the whole distractor pool.
  - Meaning feedback: "Correct!", with Next and "I guessed" buttons.
- **Drawing**
  - Trace screen: 13 numbered strokes, "Ungraded tracing practice", and "Downloading the handwriting model…". A downloading label does not show that a download succeeded.
  - Feedback screen: "Practice only: this attempt is not graded", "Well drawn!", and "Graded by stroke shapes only (handwriting model not available)".
  - Recall feedback: "Here is the kanji", with a blank drawing and 13 reference strokes.
- **Selection screen:** N1 · 99 cards. Meaning 1 due; Drawing 1 new; Readings 1 due.

**Operational assertions (supplied, not run by me):**
- 2 tests passed, 0 skipped, 138.141 s.
- One archive sync: 1079 kanji, 5037 words, 99 N1 cards, 0 problems, contentVersion `68c767f176e68882`, parser epoch 1.
- Readings: on [ソウ] and kun [] in both lists; the only reading key is そう.
- Navigation: both backlink directions for 僧 ↔ 僧侶, and both comparison directions for 僧侶 ↔ 坊さん, returning with SystemBack.
- Grades:
  - **Meaning:** Back was pressed before Next, so no new meaning grade can be claimed.
  - **Reading:** one persisted Good grade for on, and no kun log.
  - **Drawing:**
    - The trace step was ungraded.
    - The feedback used stroke geometry because the handwriting model was unavailable.
    - The recall miss wrote a persisted Again grade.
    - None of this is ML Kit recognition, a real person recalling the kanji, or a test of wrong shapes or reverse stroke order.
- Device: emulator (`sdk_gphone64_x86_64`), API 35, offline, font scale 1.

**Findings:** None.

**Optional:**
- From the original review: mention the voicing in 小僧 こぞう, and add a register note for the shared example frame.
- An app-level UI point, not a teaching issue: "Practice only: this attempt is not graded" sits next to "Graded by stroke shapes only" on `drawing-feedback`. The two messages read as slightly contradictory.

**Limits:**
- **Inherited from the original review:**
  - The 僧 Kotobank page was truncated.
  - The 僧侶 Kotobank page covered only two dictionaries.
  - "More formal" was an inference held with moderate confidence.
  - I did not inspect the N1 freeze snapshot or run the validator.
- **Visual:**
  - I saw scaled-down images only.
  - I did not identify which font each row actually uses.
  - The Paint/raster probes show only that glyphs are nonblank and differ. They do not identify the font or prove readability on every phone.
  - Some cells and footer lines are cut off in individual screens; each one is fully visible in another screen, as listed above.
  - The 僧 card and 僧侶 article were not each captured in one continuous scroll. Their full text was pieced together from overlapping screens.
- **Not established:**
  - Physical-phone testing; this run used only the emulator.
  - General-release readiness and latest-main validation.
  - Whole-set review and publication acceptance.
  - Owner progress or learning efficacy.
- **Requirements and history:**
  - Requires compatible Android `f9b59a2` or later.
  - I did not fetch anything from upstream and ran nothing natively myself.
  - The accepted 433 baseline and the earlier host-only out-of-memory history are inherited and were not rerun.
