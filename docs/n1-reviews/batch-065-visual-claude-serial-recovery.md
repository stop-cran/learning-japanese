# Batch 065 serial-recovery confirmation: no content defect; the visual report overstated its process

The two affected 約 images match what my original visual report said about their content, and nothing changes the verdicts. The original run was still not serial: two responses each made two calls. This recovery only re-reads the affected resources one at a time; it does not make that run serial after the fact. Three statements in the original report need correcting, listed under Reconciliation.

## Snapshot
- **Evidence HEAD:** 18c87f8ac27f3bd0eb59f4320130bfdfd34a755f.
- **Teaching files:** unchanged from 45c275e7c041d8486705ab860a31f34e51ac7a70.
- **Native archive source:** ee672744235275d321b4bfb33a6efe0286444594.
- **SHA status:** supplied to me, not checked (no shell available).
- **Uncommitted changes:** none included.

## Scope
- **Reviewer:** Claude Opus 5.5 (claude-opus-5.5), resuming the original session.
- **Read this turn:** exactly five resources, one view call per response, each awaited before the next:
  1. batch-065-visual-claude.md (complete).
  2. batch-065-confirmation-claude.md (complete).
  3. batch-065-visual-task.txt (complete).
  4. n1-065-agreement-approximate-reading.png (returned at about 900×2000 from the 1080×2400 source).
  5. n1-065-agreement-mnemonic.png (same size).
- **Not read:** any other reviewer's report, the adjudication, teaching files, fixture, logs or other images.
- **Not done:** no new blind review, native rerun, or device or process operation.

**Past process defect.** The original visual run (execution 420) made 44 view calls, and two of its responses each contained two calls, which overlapped:
1. My confirmation report and the visual task file.
2. agreement-approximate-reading and agreement-mnemonic.

All other reads in that run were serial. The run therefore remains a non-conformant serial run, with only partial serial process coverage. This turn re-reads the four resources involved in the overlaps one at a time, plus the original report itself.

## Verdicts

| File | Correctness | Scoped coverage | Comprehensibility | Basis |
|---|---|---|---|---|
| kanji/倹.md | CLEAN | CLEAN | CLEAN | Inherited (lexical conclusions plus original serial pixels); not re-observed this turn |
| words/倹約.md | CLEAN | CLEAN | CLEAN | Inherited; not re-observed |
| words/倹しい.md | CLEAN | CLEAN | CLEAN | Inherited; not re-observed |
| kanji/約.md (only the added 倹約 line) | CLEAN | CLEAN | CLEAN | Freshly observed in serial reads 4–5, plus inherited lexical conclusion |

## Freshly observed pixels

**agreement-mnemonic.png**
- Header reads "約 promise; approximately", followed by the full Meaning and origin text: 約束 for agreements and 約一時間 for "about one hour".
- The mnemonic is labelled "Modern-shape mnemonic:" (糸 tying an agreement to the small 勺). It says it recalls only the promise meaning and "is not an etymology explaining every sense".
- **Readings table:**
  - The "Scroll sideways to read all columns." cue is visible.
  - Visible column headers: Reading / Type / Typical words.
  - Two ヤク/on rows: 約束/予約 and 約 "approximately".
  - The right edges of some third-column lines are cut off at the screen edge (for example, the dash after やくそく).
- Visible note: "The source's kun readings remain in the metadata; these examples all use ヤク."
- **Common words:** 約束, then the added "倹約 けんやく — thrift; frugality" shown as a link, then 予約. The 約 line is cut off at the bottom ("before a").

**agreement-approximate-reading.png**
- The screen is scrolled down and the table is shifted sideways. First-column labels are clipped ("ading", "ク"); a shifted table alone is not evidence that the content is inaccessible.
- The same two ヤク rows and the scroll cue are visible.
- **Common words:** all four lines are complete, including the 倹約 link line and the 約 line "about; approximately, before a quantity".
- **Notes:**
  - 約束を守る, with "約 does not mark an exact measurement before a number".
  - 紙/組/終 share 糸; identify 約 by its simple 勺.
  - JMdict entries 1538130, 1538100, 1543750.
- The text above the Readings heading is cut off.
- This image differs visibly from the mnemonic image: different scroll position and horizontal shift.

**Not visible in these two images:** the 約 facts line (9 strokes, 糸 no. 120, N3). That claim rests only on the original serial read of agreement-radical.png, which I did not re-read this turn.

## Findings
- **Content:** no actionable defect.
- **Process (not a content defect):** the original report overstated its process and evidence in three places; see Reconciliation.

## Reconciliation
- **1. "I viewed all 30 listed PNGs one at a time." Unresolved as written, corrected here.**
  - That sentence is false: agreement-approximate-reading and agreement-mnemonic were read in the same response.
  - "Neither affects the content I assessed" played down a real process breach.
  - Bounded remediation: both images have now been re-read serially, and their content matches the original report's claims.
- **2. "約 card (inherited from earlier image reads)." Wrong label, corrected.**
  - These images were freshly viewed during the original visual turn, not inherited from the older text-only confirmation.
  - Corrected provenance:
    - Common-words line and mnemonic: original visual turn, re-confirmed serially now.
    - Facts line: original serial read of agreement-radical only.
- **3. "agreement-on-reading / agreement-approximate-reading" are visually identical. Withdrawn as unsupported this turn.**
  - The original report listed them as one scene.
  - I did not re-read agreement-on-reading, so I cannot compare it with the fresh image.
- **4. Fonts: "presumably a fallback face." Qualified.**
  - The visibly different weight of 儉 in the Textbook row does not identify which typeface was used. The fallback face remains unidentified.
- **5. Visibility of rows and cells. Qualified.**
  - A visible screenshot does not prove that every cell, line or region of the article is visible.
  - Clipped first-column labels, cut-off third-column edges and truncated text above or below the screen are viewport limits, not certified content.
- **6. Lexical conclusions C1–C4. Unchanged:** C1 and C2 resolved; C3 and C4 optional.

## Optional
These carry over unchanged:
- Polish wording: "a kanji spelling 慎ましい" rather than "the kanji spelling".
- C3 and C4.
- The drawing screen shows both "not graded" and "Graded by stroke shapes only", which reads as contradictory. This concerns the app, not the teaching content.

## Limits
- **Original report:** it remains intact and was not rewritten. Its source, dictionary, read-depth and pixel limitations all still apply.
- **Supplied operational results:**
  - Two tests OK in 148.883 s.
  - Content sync: 1077 kanji, 5036 words, 97 N1, 0 problems, contentVersion 6a940651167e0e94, parser epoch 1.
  - Both reading grades persisted; no new meaning grade is claimed; drawing persisted "Draw again".
  - These are supplied, not executed by me.
- **Drawing:** this is not MLKit recognition and not a successful human recall.
- **Device:**
  - Emulator only, API 35, font scale 1.
  - The app must be Android f9b59a2 or later.
- **Historical memory notes:** the 416 denial, 1 GiB OOM and 049 512 MiB failure remain historical. The HOST-only 2 GiB setting never applies to native builds.
- **Not established:**
  - unseen article or table regions;
  - physical phone or general release;
  - the whole set, current main, or publication.

EXIT.
