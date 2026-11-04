I found **no visual defects** in the eight screenshots. 它 is readable and easy to tell apart from 宅 in all four font-family rows. The mnemonic, the comparison note, the source-only readings and the three word articles are readable where the screenshots show them. Several passages are cut off or outside the screenshots, so this does not certify whole articles or the full readings table.

```text
Snapshot: Current teaching c7ada33b6917a8af9a4ae14809d470b222929bca; reviewed teaching
  3ddad580eadfea6b2a492c69cb6be12c57d334e2. Both come from the coordinator: unchanged
  runtime, no teaching diff. I did not check Git or any hashes myself (no shell).
  I made no edits.

Scope: Claude Opus 5.5, the same session as the initial and confirmation reviews.
  Visual confirmation only. Each item below was viewed once, one tool call at a time:
  - my confirmation report, docs\n1-reviews\batch-037-confirmation-claude.md
  - the eight PNGs in artifacts\batch-037-parent-native-attempt-2:
    font-pairs, kanji-component-mnemonic, kanji-component-comparison,
    kanji-source-only-readings, word-snake, word-dakou, word-faucet, selection
  The text verdicts come from the earlier reviews. The screenshots are new native
  visual evidence, limited to what they show. I did not read other reviews, author
  or parent image opinions, the reconciliation, or the ledgers. No web lookups.

Verdicts:
  kanji/蛇.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
    These text verdicts carry over from the confirmation review. Visually, the
    mnemonic paragraph, the start of the readings table, the タ/ヤ source-difference
    sentence, Common words, Notes and Sources all render readably.
  words/蛇.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
    These carry over from the initial review. The screenshot shows readable text
    from "How the kanji combine" through "Distinctive meaning".
  words/蛇行.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
    These carry over from the confirmation review. The screenshot shows readable
    text from the title and Meaning through the 曲がる/カーブ contrast.
  words/蛇口.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
    These carry over from the initial review. The screenshot shows readable text
    from "How the kanji combine" through the Dictionary line.

Findings: None.

  What the screenshots show:
  - 它 in the font-pairs screen:
    - In all four rows (Gothic, Mincho, Textbook, Brush), 它 is a complete glyph:
      a roof on top and a hooked, curled lower stroke.
    - It is easy to tell apart from 宅 in every row: 宅 has a different lower part
      with an extra crossing stroke.
    - 蛇 and 蚊 are easy to tell apart in every row (它 versus 文 on the right).
    - 它 looks the same in all four rows, while 宅, 蛇 and 蚊 change design from row
      to row. This matches the supplied note that the fallback face is shared.
      A typeface change is not a defect.
  - 它 in running text: it renders as a clear glyph inside the mnemonic sentence
    ("roof-and-curled-lower shape of 它") and inside the Notes sentence about 蚊.
  - Kanji readings table:
    - Unscrolled, the ジャ and ダ rows are fully visible, but じゃこう is cut off at
      the right edge of the Typical words column.
    - Scrolled sideways, the Typical words cells for ダ, イ and ヤ are visible,
      including 委蛇 いい / いだ and "KANJIDIC2 source-only information: no verified
      word example here;". The Reading column is now cut off on the left, so the
      イ and ヤ labels do not appear.
    - The table shows a "Scroll sideways to read all columns." hint, so the edge
      cut-off is expected table behaviour, not a defect.
  - Selection screen: shows "N1 · 69 cards", which matches the supplied sync count.
    Meaning quiz shows 0 due, 10 new. Drawing and Readings are locked. The filter
    chip row runs off the right edge (a chip labelled "St…").

Optional: None. (The 蛇口 article shows "kango" in code formatting. That is
  unchanged reused text and outside this visual scope.)

Limits:
  - Not visible in the screenshots, so not certified:
    - the 蛇.md readings-table lines between the two kanji screens, including the
      paragraph that begins "Kanjipedia lists 委蛇 (イイ)…" and the end of the ヤ
      cell ("not quizzed")
    - the イ/ヤ labels while the table is scrolled sideways
    - the top lines of the comparison screen and the 蛇口 screen, which are hidden
      under the header
    - the Meaning and example sections of the 蛇 and 蛇口 word articles
    - the 蛇行 うろうろ contrast, the dictionary line and the quiz settings (quiz
      exclusions are not visible in the app)
  - Supplied by the coordinator, not observed by me:
    - one ContentSync run with problems 0
    - two terminal case-0 results
    - 16 Paint probes with glyphs
    - the same 它 Paint raster across families, from an unidentified fallback face
    - Android 3+1 passing
  - Device coverage: API 35 emulator only. No physical phone, no general-release
    acceptance and no retest of the meaning, reading or drawing quizzes. Integration,
    CI and the public ZIP are still pending.
  - Carried over:
    - the original review's single parallel-call breach (disclosed then)
    - unverified snapshots
    - validate.py and build_manifest.py were not run
    - both original findings remain RESOLVED, as stated in the confirmation report
  - This is not a new blind initial review, not a native-speaker check and not a
    physical-phone certification.
```
