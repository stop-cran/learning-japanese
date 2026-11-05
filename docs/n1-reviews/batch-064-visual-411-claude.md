# Batch 064 recovery confirmation (Claude Opus 5.5, execution 411)

**Snapshot:** evidence HEAD 976b825f0d32d1074c63c6f7b71388daa9da81a9; teaching unchanged at ff6eb7893344b806bf517ebd41bf19089bed5021. Both hashes were supplied to me; I have not checked them with Git.

**Scope:** a bounded recovery check in my original Claude session, using only the `view` tool, one call at a time. It rechecks two claims in my 408 report against the two current articles and six screenshots. It is not a new blind review, a dictionary review, a native rerun, or retroactive acceptance of 408, 409 or 410. I did not read the other reviewer's report or any adjudication.

## Reads

**This run, in order (all successful):**
1. The shared task file `control\batch-064-visual-task.txt`, read in full for the first time by me. Its text matches the 408 task text I worked from. I could not compute the byte count or hash, so the parent's 7294 bytes / 57b9eaef…12cf is supplied, not checked.
2. My 408 visual report, in full.
3. `kanji\偵.md`, in full (60 lines).
4. `words\探偵.md`, in full (55 lines).
5. Six PNGs, one per call, all returned at 900x2000: kanji-compound-boundary, kanji-no-kun, kanji-detective-story, detective-fiction-example, detective-components and detective-role-summary.

**Inherited, not re-read:** the 28 images from 408 (the six above plus the 22 others listed in 408), the 408 text reads, the fixture ranges, the terminal log and the route receipt.

**Earlier failed task-file reads:**
- 408: permission denied; I worked from the task text in the prompt.
- 409 and 410: permission denied; I stopped each time.

Those records stay as they are, and strict 408 process and coverage remain FALSE.

## Reconciliation of the two 408 claims

### Claim 1: "the kun cell is a dash … visible after sideways scrolling" — WITHDRAWN

- **Source:** `偵.md` lines 34–36 have one table row only: `テイ | on | [探偵] たんてい — detective; investigator`. There is no kun row and no kun cell. Lines 38–39 state in prose that no kun reading is supplied.
- **Fresh pixels:**
  - kanji-compound-boundary, unscrolled: shows "Reading / Type / Typical words" and a single row, テイ | on | 探偵 たんてい / detective; / investigator. No dash is visible between たんてい and "detective".
  - kanji-no-kun and kanji-detective-story, scrolled sideways: the left labels are clipped ("ading", "イ"), and "探偵 たんてい —" appears in the Typical-words cell.
- **Conclusion:** the dash that appeared after scrolling is the em dash in the Typical-words gloss. It is not a kun cell.
- **Corrected statement:**
  - The table has one テイ/on row with the linked 探偵 example.
  - The "no kun" information is given in the following sentence, which is fully visible in all three of these 偵 frames.
  - Across the unscrolled and scrolled frames, every cell of that one row was seen.

This was an error in my report wording, not a content defect.

### Claim 2: "every in-scope paragraph" and "full footer" visible — RESOLVED for 偵 and 探偵 (with qualifications); INHERITED and QUALIFIED for 探 and 刑事

**偵.md**
- **Fresh pixels:**
  - Meaning and origin, the mnemonic paragraph, the Readings intro and row, the no-kun sentence, Common words, all three Notes bullets with the 刑事/停/低/値 links, and the complete footer.
  - The footer reads "…entries 1418380, 1418390, 1435100 and 1249660. Character meaning and reading: Jitsu, 偵." (detective-story).
- **Not in the six fresh frames:** the facts line (11 strokes, 人 as 亻, no. 9, N1) is supported only by retained 408 pixels.

**探偵.md**
- **Fresh pixels:**
  - The header title.
  - Meaning, with 私立探偵, both examples with kana and translations, the に/を explanation, and the 探偵する note.
  - How the kanji combine, with the 探/偵 links and タン + テイ.
  - Synonyms and antonyms, with the 刑事/調査/調べる/探る links and the "not a rule … excludes police" qualifier.
  - Distinctive meaning, with the spy and success qualifiers.
- **Footer:**
  - Cut off in detective-components.
  - Complete in detective-role-summary, including "Selected Edition … Nipponica, 探偵."
- **Not in the fresh frames:**
  - The Markdown H1 line and the front matter. The app shows the title in its header.

**探.md and 刑事.md**
- Neither was part of this run's reading set.
- Visibility of the changed lines (探 line 40, 刑事 line 28) and their footers rests only on retained 408 pixels.
- 408's "every in-scope paragraph" wording is narrowed to those changed lines plus whatever context those 408 frames showed. Unchanged context is not freshly reviewed.

## Verdicts

| File | Correctness | Scoped coverage | Comprehensibility | Evidence |
|---|---|---|---|---|
| 偵.md | CLEAN | CLEAN | CLEAN | Fresh source and pixels; facts line from retained 408 pixels; lexical conclusions inherited |
| 探偵.md | CLEAN | CLEAN | CLEAN | Fresh source and pixels; lexical conclusions inherited |
| 探.md (line 40 only) | CLEAN | CLEAN | CLEAN | Inherited (408); not freshly re-examined |
| 刑事.md (line 28 only) | CLEAN | CLEAN (064-N1 resolved) | CLEAN | Inherited (408); not freshly re-examined |

## Findings

No content defects. The only correction is to my own 408 report: the kun-cell claim is withdrawn, and the visibility claim is qualified as set out above.

## Optional

The 408 optional items still stand:
- Note that 低 also reads テイ.
- Gloss 読むのが好き, or add a 探偵する example.
- Polish 探's reading table and consider linking 探る.
- Outside content scope: the drawing screen shows "not graded" next to "Graded by stroke shapes only".

## Limits

- **Image transport:** every image came back at 900x2000, and the source is reportedly 1080x2400.
- **Clipping:**
  - The Reading-column labels are clipped in the two frames scrolled sideways.
  - The Typical-words dash is clipped in the unscrolled frame.
  - The 探偵 footer is cut off in one frame.
- **Source versus pixels:** source text does not prove that content outside a frame was visible.
- **Inherited and unchanged:**
  - My original lexical, source, lookup, citation and process limits.
  - The 404 Android and 406 native results, which were supplied to me, not run by me.
  - The Paint-probe and drawing limits recorded in 408.
- **Not certified:** dictionaries, the actual fallback face, physical phones, general release, the whole set, latest main and publication.
