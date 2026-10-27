## Snapshot: `bfc6d3d3e00525bc21aac101af8d06d7241b88f4`; parent `8c71fae49b615f2d6f0de34c6b00d1b20d17dd7e`

**My original finding is resolved. The other two corrections are independently supported, and no actionable regression was established.**

The correction descriptor was read first and declares clean committed content. File tools cannot execute Git, hashes, or cleanliness checks; commit attribution and committed-only correspondence therefore remain supplied assertions. I did not inspect `.git`.

## Scope:

**Model:** GPT-6.1 Sol, `gpt-6.1-sol`; family `gpt`. Read-only confirmation in the original session; no edits, agents, or delegation.

**Complete current rereads:** `words\体操.md`, `words\ダイヤグラム.md`, `words\竹.md`, the complete correction patch including its changed TSV row, both complete corrective dictionary families—1068870 and 1315960—and all three bodies in `corrective-existing-reading.txt`. I also read the actual current スケジュール, 時間割, and 体育 files completely, plus unchanged だいぶ and タイヤ.

**Source/evidence checks:** all twenty current TSV mappings, the complete original compact mappings, the corrected derivative’s twenty current rows and correction section, complete relevant principal records 1409580/1076680/1422230, complete 体育 1409200, and the original captured Daijisen ダイヤグラム entry. Current selections were judged from the corrected rows and actual TSV, not the derivative’s retained historical authored-mapping records. Both repository instruction files, the requested format range, and the current vocabulary snapshot were reread.

**Preservation checks:** current exclusions across all sixteen new cards; targeted identity, metadata, alias, and word-side-link checks; reading-row/Common words spot-checks on all four related kanji cards.

**Inherited scope:** my initial complete reads of all twenty assigned word articles, all four related kanji cards, 113 additional older word bodies, complete principal/comparison renderings, component/label evidence, and 22 frozen public captures. Unchanged judgments are explicitly inherited—not represented as new complete rereads. スケジュール and 時間割 add two distinct older bodies, making my cumulative additional-old-body scope **115**, beyond the four assigned reuses—not the author’s 124.

No forbidden ledger, report, rationale-bearing batch file, script, or another reviewer’s output was read. The corrected evidence JSON was read selectively, not completely; unchanged evidence coverage is inherited.

## Verdicts:

All articles below are `words\<article>.md`. **Inherited** means the initial complete-body review, supplemented only by the current checks stated. **CLEAN** means no actionable defect established within that scope.

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:982 | 体操 — new | Corrected full reread | CLEAN | CLEAN | CLEAN |
| N2:983 | だいぶ — reused, N4 | Unchanged full reread | CLEAN | CLEAN | CLEAN |
| N2:984 | 大木 — reused | Inherited; metadata check | CLEAN | CLEAN | CLEAN |
| N2:985 | 題名 — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:986 | 代名詞 — new | Inherited; link/guard checks | CLEAN | CLEAN | CLEAN |
| N2:987 | タイヤ — new | Unchanged full reread | CLEAN | CLEAN | CLEAN |
| N2:988 | ダイヤグラム — new | Corrected full reread | CLEAN | CLEAN | CLEAN |
| N2:989 | ダイヤモンド — new | Inherited; alias/guard checks | CLEAN | CLEAN | CLEAN |
| N2:990 | ダイヤル — new | Inherited; alias/guard checks | CLEAN | CLEAN | CLEAN |
| N2:991 | 対立 — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:992 | 田植え — new | Inherited; link/guard checks | CLEAN | CLEAN | CLEAN |
| N2:993 | 絶えず — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:994 | 楕円 — new | Inherited; guard-field check | CLEAN | CLEAN | CLEAN |
| N2:995 | 高める — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:996 | 耕す — reused | Inherited; metadata/link/guard checks | CLEAN | CLEAN | CLEAN |
| N2:997 | 滝 — new | Inherited; guard-field check | CLEAN | CLEAN | CLEAN |
| N2:998 | 炊く — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:999 | 焚く — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:1000 | 蓄える — new | Inherited; guard check | CLEAN | CLEAN | CLEAN |
| N2:1001 | 竹 — reused | Corrected full reread; remapping check | CLEAN | CLEAN | CLEAN |

**Mappings — CLEAN:** visual comparison of the original compact mappings, corrected rows, actual TSV, and patch supports preservation of all twenty raw source records and nineteen selected/additional mappings. N2:1001 now correctly selects **1422230:1,2**, with no additional senses. ダイヤグラム remains selected JMdict sense 1; its transport-schedule teaching is separately public-backed, without an invented JMdict sense number.

**Kanji edits and reciprocity — CLEAN across all three facets:** inherited complete-card judgments stand. Current checks confirm 詞/代名詞 at **シ**, 植/田植え under **う.える**, explicitly 植え＝うえ, and both Common words links. Existing 耕/耕す at **たがや.す** and 竹/竹 at **たけ** remain complete without manufactured edits. Word-side links remain present.

**Reuse preservation — CLEAN for observed content scope; exact byte preservation UNVERIFIED:** だいぶ visibly retains its stable identity, N4 level, `kanji: []`, and recognition of 大分/だいぶん. 大木 and 耕す retain the inspected identities and metadata. 竹 retains its original teaching, title, reading, N2 metadata, and four exclusions; only its appended coverage assertion changes in the supplied patch. None is treated as a wholly new card.

## Findings:

**B50-GPT-01 — RESOLVED — originally Low severity, quiz over-exclusion.**

`words\体操.md:9` now removes **体育 only**. The modern comparison and obsolete-sense qualification remain at lines 37–50.

The complete 1409580 record marks PE-class sense 3 obsolete; complete 1409200 and `words\体育.md:15–22,35` teach education/the subject rather than an exercise routine or gymnastics discipline. This supports the narrow ordinary-answer distinction underlying my original finding. It does **not** prove zero imaginable historical or contextual overlap. The requested minimal remedy is implemented without changing the lexical teaching. **Confidence: high in resolution; no further remedy.**

**B50-QZ-01 — independently confirmed corrected — quiz coverage and supporting explanation.**

`words\ダイヤグラム.md:9,25–29,48–51` adds direct exclusions for **スケジュール** and **時間割**, explicitly teaches the operating schedule itself, and links both comparisons.

The decisive original evidence is `public-bodies.txt:128–136`: the exact Daijisen ダイヤグラム heading and reading precede sense 2, which includes the chart and “また、その運行予定.” Complete 1068870 supports schedule/program/calendar; complete 1315960 supports timetable, especially a school timetable, and schedule. Their actual titles are `schedule; program of activities` and `timetable; class schedule`. Thus the guards have direct meaning evidence, not merely a transitive connection through ダイヤ. The explanation preserves the school/transport distinction and does not fabricate JMdict sense 2. **Confidence: high; no further remedy.**

This correction addresses a gap in my initial CLEAN assessment of ダイヤグラム’s exclusions; it was not a finding I originally reported.

**B50-MAP-01 — independently confirmed corrected — source-scope metadata.**

`docs\n2-vocabulary-sources.tsv:1001` now selects **1,2**, clears additional senses, and corrects the source note. `words\竹.md:59–61` agrees.

The unchanged raw gloss explicitly names both bamboo and the middle of a three-tier ranking system. Complete 1422230 contains those two unrestricted noun senses. The correction therefore fixes an inaccurate source-scope assertion—not absent rank teaching. The original teaching and four exclusions remain intact in the supplied diff. **Confidence: high; no further remedy.**

My initial all-CLEAN mapping conclusion overlooked this mismatch and is revised accordingly.

**Regression assessment:** every hunk of the content/mapping correction patch is accounted for. The diagram additions retain the original examples, identity, and qualifications; the bamboo change stays within its appended note and mapping fields; the exercise change stays within one exclusion list. Manual counting of current new-card lists gives **72 declarations across thirteen cards**, consistent with two additions minus one removal from 71. No baseline guard change appears in the supplied patch, and no actionable new defect was established.

## Optional:

None. No additional mandatory guard expansion is established by the reviewed evidence; the unadopted candidate distinctions need not be erased merely because contextual overlap is imaginable.

## Limits:

Git identity, cleanliness, hashes, derivative equivalence, patch completeness, and exact unchanged-file preservation remain **UNVERIFIED independently**. No `.git` substitute was used. Supplied aggregate totals such as 242 families/665 senses were not independently recounted or treated as proof of additional body reads.

No fresh public retrieval was performed during this confirmation. Frozen endpoint captures remain author captures; the initial review’s partial/irrelevant retrieval limitations remain inherited. Unchanged bodies were not comprehensively reread, and label-only candidates were not silently promoted to full-body inspections.

The inherited 大木 ダイ→タイ explanation was not independently established; it remains outside the narrow sourced-reuse confirmation, not newly certified etymology. No other consequential unresolved linguistic claim was identified in the corrected passages. This is not exhaustive dictionary coverage, a live-quiz check, or native-speaker certification.
