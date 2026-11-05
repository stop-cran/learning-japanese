# Batch 064 native visual confirmation (Claude Opus 5.5, execution 408)

I found no actionable defects. Across the four production font rows, the screenshots, the article routes and the two quizzes, nothing contradicts my earlier text verdicts. The only finding from the earlier reviews, 064-N1 (the missing 探偵 link in `刑事.md`), stays resolved.

**Snapshot:** evidence HEAD e2c49895daee2bbf0019388c0333e3d0e245fd4a; teaching unchanged from ff6eb7893344b806bf517ebd41bf19089bed5021; native archive source bf6204e5b4e4c64f340dcd8db65b2924b869cc45. These hashes were supplied to me; I did not check them with Git.

**Scope:** dependent native visual confirmation by the original session, not a new blind initial review, dictionary audit or native rerun.
- **Process deviation:** `control\batch-064-visual-task.txt` could not be read (permission denied), so I worked from the task text in the prompt.
- **Text reads, one call each, in order:**
  1. my original report and my textual confirmation, both in full;
  2. 偵.md, 探偵.md, 探.md and 刑事.md, each in full (only 探.md line 40 and 刑事.md line 28 are changed scope);
  3. `N1Batch064NativeTest.kt` lines 54–143, 150–285, 286–453 and 499–550 (lines 144–149 and anything past 550 were not read);
  4. the complete `instrumentation.txt` and `n1-064-article-route.json`.
- **Images:** all 28 PNGs in the order listed, one per call. Every one came back at 900x2000 (source reportedly 1080x2400).

## Verdicts

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 偵.md | CLEAN | CLEAN | CLEAN |
| 探偵.md | CLEAN | CLEAN | CLEAN |
| 探.md (line 40 only) | CLEAN | CLEAN | CLEAN |
| 刑事.md (line 28 only) | CLEAN | CLEAN (064-N1 resolved) | CLEAN |

## What the screenshots show

**Fonts (font-pairs)**
- 偵 貞 停 低 値 人 亻 探 手 扌 探偵 刑事 render in all four rows (Gothic, Mincho, Textbook, Brush).
- No blank or replacement boxes; the radical forms 亻 and 扌 are visible in every row.
- In the Textbook row, 探偵 wraps across two lines, with both characters visible.
- Some styles may look alike, and the actual fallback face is not identified.

**偵 card**
- The header facts read: 11 strokes, radical 人 (as 亻, no. 9), N1.
- The mnemonic is labelled "Modern-shape mnemonic" and says it is not etymology.
- The reading table shows テイ (on) with the 探偵 link, and the kun cell is a dash. That dash was visible only once the table was scrolled sideways, so the earlier gap was clipping.
- The no-kun / タン+テイ note, the Common words (探偵, 探偵小説, 偵察, with kana) and the Notes are visible, including the 刑事, 停, 低 and 値 links.
- The source footer is visible.

**探偵 article**
- The header reads "detective; secret investigation".
- Both example sentences appear with kana and translations, and so do the explanations of the に and を particles and of 探偵する.
- The 探 and 偵 links, with タン + テイ, are visible.
- The 刑事 comparison keeps its qualifier: "a practical distinction, not a rule that every occurrence of 探偵 excludes police."
- The spy and success qualifiers and the full dictionary footer are visible.

**探 card**
- The header facts read: 手 (as 扌, no. 64), N3.
- Changed line 40, "探偵 たんてい — detective; investigator (探 is タン here)", is fully visible and linked. タン breaks across two lines but stays readable.

**刑事 article**
- Changed line 28 shows 探偵 as an underlined link.
- The "not 'criminal' as … the person who committed an offense" boundary and the footer are visible.

**Navigation routes**
- The four links between 偵/探 and 探偵 work in both directions.
- 探偵 → 刑事 → 探偵 works, and system Back returns to 刑事.

**Meaning quiz**
- The live options were monkey, spy; covert investigation, raised ridge; land measure, and imitate; emulate. These are fallback distractors, not the authored 停, 低 and 値 meanings, but only one option fits 偵.
- The feedback screen shows "Correct!" with the 偵 card.

**Reading quiz**
- "Pick the on'yomi" offered スイ, ケイ, テイ and ナイ, with no kun option.
- The feedback reads "Correct! — on'yomi" and "spy; covert investigation: テイ".

**Drawing**
- The trace template shows 11 numbered strokes, with "Ungraded tracing practice" and "Downloading the handwriting model (first use only)…". That status message does not show the download succeeded.
- After the trace: "Practice only: this attempt is not graded", "Well drawn!" and "Graded by stroke shapes only (handwriting model not available)".
- The recall screen shows "Here is the kanji" next to an empty "Your drawing" box.

## Findings

None.

## Optional

These are carried over from my earlier reviews and none blocks:
- Note that 低 also reads テイ.
- Gloss 読むのが好き, or add a 探偵する example.
- Polish 探.md's reading table, and consider linking 探る.
- Outside the content scope: the drawing screen shows "this attempt is not graded" alongside "Graded by stroke shapes only", which reads slightly inconsistently. This is not a finding.

## Limits

**Inherited text conclusions:** they keep my original source, lookup, read-depth and citation limits. I did no fresh dictionary or quiz-pool certification; source, reading, spelling and quiz-exclusion judgements are inherited.

**New pixel observations**
- Images arrived at 900x2000.
- Some table columns were seen only when scrolled sideways, and some footers were cut off in individual frames. Every in-scope paragraph was still seen in at least one frame.
- The actual fallback face is not identified.
- The Paint glyph probe uses `Typeface.DEFAULT` for the Gothic row. Its 40 single-glyph and 8 whole-word probes show non-blank, distinct output only, not the face used or readability on every phone.

**Supplied operational results (not run by me)**
- 2 tests, both status 0, 160.379 s, OK.
- Archive counts: 1076 kanji, 5034 words, 96 N1 cards, 0 problems, contentVersion ae05977ba66f42f5, parser epoch 1.
- Emulator: API 35, font scale 1, offline. This is an emulator, not a phone.
- No new meaning grade was saved: the test pressed Back before Next.
- The single On "Good" log, zero Kun logs and the drawing "Draw again" log are asserted by the test, not observed by me.
- The drawing test used 11 injected reference strokes. It is not ML Kit, a successful human recall, or a negative or reverse-order test.
- The 406 post-run permission denial is kept as a separate record.
- Port 5581 / PID 9520 was recorded, which does not show that all ports are free.
- The 404 Android run was not rerun.
- The historical 049 host OOM is unchanged.

**Still open**
- Android f9b59a2 or later is required.
- Physical-phone, general-release, whole-set, current-main and publication acceptance are outstanding.
