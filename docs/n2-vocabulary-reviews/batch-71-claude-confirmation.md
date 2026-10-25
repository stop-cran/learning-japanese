# Batch-71 correction confirmation review (claude-opus-5.5)

Every original finding is resolved, but one blocking defect remains (B71-10, low severity). 一通り's title still shares the unqualified label "all parts" with 各地 ("various places; all parts"), with no guard between them. That overlap was already in the earlier title and I missed it in my blind review, so it is not caused by the correction.

## Snapshot
- **Revised frozen commit:** 73289715182d44fddb23829348ab9bba32ab5f20.
- **Parent:** 88aea28d8f5e1d4d17088835c03b9c93d19eb6cd.
- **Committed content only:** I read working-tree files, which the author reports as a clean checkout of that commit.
- **Git limitation:** my file-only tools cannot run Git. Clean-checkout, manifest/hash and rendering-equivalence checks were run by the author, not by me.

## Scope
**Model:** claude-opus-5.5. Read-only; no edits, agents, delegation or shell.

**Read fresh and in full at this stage:**
- the correction snapshot, correction.patch and reconciliation.json;
- all twenty current articles, and kanji\筆.md and kanji\皮.md;
- the TSV header (line 1) and physical rows 1402–1421 only;
- mappings.jsonl (20 rows), principals.jsonl (20 families, 44 senses) and components.jsonl (30 records);
- correction-comparison-reading.txt (8 families, 39 senses) and correction-public-bodies.txt;
- the full bodies of 考える, 転がす, 工夫, おおよそ, 出入り, 著す and 絞る;
- three extra comparison bodies: 各地, 一度 and 一旦;
- docs\content-format.md lines 76–92.

**Searched, not read in full:**
- a search of word titles in words\ for segment overlaps;
- labels.jsonl (searched only);
- content-format.md:63 and the instructions file (located by search).

**Fetched independently:** the Kotobank pages for 日日 and 入る. Both applicable Seisenban headings came back.

**Carried over from my blind review:** related.patch, public-bodies.txt (22 Digital Daijisen inspections via Weblio), and the 人込み body.

**Not read:** the 18 family and 20 older-body chunks, the original supplement, corrected-review-evidence.json, correction-completed-inspection.json and public-bodies.json. My depth is therefore not matched to the GPT reviewer's.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1402 | 筆記 | CLEAN | CLEAN | CLEAN | Unchanged; 筆 links reciprocal. |
| N2:1403 | ひっくり返す | CLEAN | CLEAN | CLEAN | 転がす guard added (B71-01). |
| N2:1404 | ひっくり返る | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1405 | 引っ越し | CLEAN | CLEAN | CLEAN | Unchanged; "relocation" labels (移転, 移動) are guarded. |
| N2:1406 | 引っ込む | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1407 | 筆者 | CLEAN | CLEAN | CLEAN | 著す guard added (B71-05). |
| N2:1408 | 必需品 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1409 | 人差し指 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1410 | 一通り | NEEDS FIX | CLEAN | CLEAN | B71-03 and B71-09 resolved; new B71-10 ("all parts" vs 各地). |
| N2:1411 | 人通り | CLEAN | CLEAN | CLEAN | 出入り guard added (B71-04). |
| N2:1412 | ひとまず | CLEAN | CLEAN | CLEAN | Blank source spelling preserved. |
| N2:1413 | 瞳 | CLEAN | CLEAN | CLEAN | Iris/colour wording remains optional. |
| N2:1414 | 一休み | CLEAN | CLEAN | CLEAN | Only the attested ひと休み remains (B71-06). |
| N2:1415 | 独り言 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1416 | ひとりでに | CLEAN | CLEAN | CLEAN | Blank spelling preserved; 一人でに wording remains optional. |
| N2:1417 | ビニール | CLEAN | CLEAN | CLEAN | Blank spelling preserved. |
| N2:1418 | 皮肉 | CLEAN | CLEAN | CLEAN | 皮 links reciprocal. |
| N2:1419 | 日にち | CLEAN | CLEAN | CLEAN | Kun+on wording, pinned-JMdict distinction and Seisenban sense ③ all verified. |
| N2:1420 | 捻る | CLEAN | CLEAN | CLEAN | 工夫 and 考える guards both justified. |
| N2:1421 | 日の入り | CLEAN | CLEAN | CLEAN | 入る (いる) explained and its Seisenban heading verified. |

**筆 edit: CLEAN.**
- 筆記 ひっき and 筆者 ひっしゃ appear in the reading table, the common-word list and the contraction note.
- The footer includes entries 1487800 and 1487830.
- Existing content is preserved: 万年筆, 執筆, 随筆, 鉛筆, ふで and the header.

**皮 edit: CLEAN.**
- 皮肉 ひにく appears in the ヒ reading-table row, the common words and the notes.
- The footer includes entry 1483900.
- 皮膚, 毛皮 and the 革 note are preserved.

**Mappings: CLEAN.**
- All twenty associations, raw fields and selected/additional senses match the TSV.
- The blank source spellings for ひとまず, ひとりでに and ビニール are preserved.
- The raw spellings 引っ繰り返す, 引っ繰り返る, 引越し, 人差指 and 日日 are recognized as aliases, not new identities.

**Baseline preservation: CLEAN.** The patch touches only eight assigned articles. No older articles or kanji cards changed, and no identity, level or asset changed.

## Findings

**Original findings (B71-01 to B71-05: added guards)**

| ID | Disposition | Basis for the new guard |
|---|---|---|
| B71-01 ひっくり返す/転がす | RESOLVED (ひっくり返す.md:9) | Tipping-over senses on both sides (1601870 sense 2, 1440980 sense 2) and the 転がす glass example; not all rolling. |
| B71-02 捻る/工夫 | RESOLVED (捻る.md:9) | Shared "devise" label; 1469530 senses 5–6. |
| B71-03 一通り/おおよそ | RESOLVED (一通り.md:9) | 1164910 sense 1 ("generally/roughly") against 1415050 senses 2 and 4 (general use, outline); not numerical approximation. |
| B71-04 人通り/出入り | RESOLVED (人通り.md:9) | 1339910 sense 1 (going in and out) and the example 人の出入りが多い; not accounting. |
| B71-05 筆者/著す | RESOLVED (筆者.md:9) | Shared unqualified "author" label; the article claims no person/action interchangeability. |

**Original findings (B71-06 to B71-09: text changes)**
- **B71-06: RESOLVED.** 一休み.md:30 keeps only ひと休み, which entry 1161830 lists. No universal nonexistence claim is made.
- **B71-07: RESOLVED.** The 日入/日の入 spelling sentence is gone.
- **B71-08: RESOLVED.** 日の入り.md:27 now gives 入る (いる), and lines 48–49 cite Seisenban.
  - I fetched that heading myself: い・る ①(ロ) reads 「特に、日、月が沈む」.
  - Seisenban's はいる ①(ロ) also allows setting, so the article's restraint (not claiming はいる can't describe it) is correct.
- **B71-09: RESOLVED.** The title and H1 are now "once-over; all parts; ordinary" (lines 4 and 12).
  - No other title contains "once-over".
  - 一度 ("once") and 一旦 ("once; temporarily") share only a partial string, a different English word. Lines 48–49 explicitly warn against treating 一通り as a synonym of 一度, so no pair is established.
  - All prior guards are preserved.

**Other dispositions**
- **"main" in the dishes translation: RESOLVED** (line 21).
- **GPT-F01 (捻る/考える): justified, not excessive.**
  - 考える has an ordinary devising use (1281020 sense 6), and its body includes "working out an idea".
  - The 頭をひねる example in 捻る is itself translated with 考えました.
- **GPT-F02 and the 日日 precision fix: RESOLVED.**
  - ひ kun + にち on is correct.
  - `type: wago` is consistent with content-format.md:63, which assigns `kango` only to on-first mixed words.
  - I independently confirmed Seisenban ひにち ③: 「ひび。ひごと。にちにち。多く、「ひにち毎日」「毎日ひにち」の形で用いる」.
- **捻る/絞る optional pair: WITHDRAWN.** The displayed titles share no label. 捻る sense 3 concerns an animal's neck, and the rack-one's-brains idioms appear only in the bodies. The existing 捩る/絞る guard does not carry over because guards are nontransitive.
- **Regressions:** none found.

**New remaining defect**

| Field | Detail |
|---|---|
| ID | B71-10 |
| Severity | Low |
| Facet | Correctness (quiz label/guard) |
| Location | words\一通り.md:4, 9, 12; words\各地.md:4, 16 |
| Claim | The unqualified label "all parts" appears in both titles. 各地 is not excluded. Exact-title deduplication doesn't apply (content-format.md:78–83). With 各地 as the prompt, 一通り would be a partly label-correct distractor, the same kind of English-label ambiguity accepted for B71-05. |
| Origin | Present since 88aea28 ("general pass; all parts; ordinary"), so not a correction regression. I missed it blind, and 各地 is absent from the author's labels. |
| Remedy | Preferred: qualify the title (e.g. "full set"), because the meanings don't truly overlap (content-format.md:88). Alternative: add 各地 to quiz_exclusions. |
| Evidence | 1164910 sense 2 includes the gloss "all parts". 各地.md:16 reads "all parts of a stated or understood area". |
| Confidence | Medium |

## Optional
These stay deferred; no consequential defect was shown in what each card selects to teach:
- 一人でに: JMdict marks it as irregular kanji usage, which the article's wording could reflect.
- 瞳: iris/colour wording.
- ひっくり返す: the page-turning use.
- 皮肉: "satire".

## Limits
- I did not fetch Seisenban ひねる [1]3 or Digital Daijisen 考える sense 3 myself. Those rely on the author's excerpts plus pinned JMdict (1469530 senses 5–6; 1281020 sense 6), which is enough to support the guards.
- The Kotobank 入る return was truncated, but only after the applicable いる and はいる headings.
- The title-collision check was a pattern search over title segments, not an exhaustive semantic search.
- I did not read the author's chunk sets or the optional evidence files.
- There is no Git verification, native-speaker certification, frequency claim or runtime-quiz guarantee.
