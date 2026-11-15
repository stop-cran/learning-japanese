# B123 confirmation — N1-B123-CLAUDE-CONFIRM-002

## Snapshot
Commit: 047970a055903c0337d73823288695938648dd1d
Model: runtime reports Claude Opus 5.5 (claude-opus-5.5); execution-model identity not independently verified

## Scope
Chain: segments 1-61 of n1-b123-claude-confirm-002, each read once in order; no re-views
Fetches: none (no network, web or local reads outside the chain)

## Dispositions
- F1 - RESOLVED - 標 and 紀 are now declared on 範 (snapshot/kanji/範.md:14) and explained at snapshot/kanji/範.md:47. Evidence holds: JMdict 1488710 標準 glosses standard, criterion, norm and model (snapshot/docs/n1-sources/batch-123/reconciliation-001/jmdict-records.xml:1059-1539), the retained Daijisen 標 entry gives 目じるし・目あて with 標準 (external-sources/標-daijisen.txt:24-28), and the Daijisen 紀 entry's first sense is 筋道をきちんと立てたおきて with 紀律・綱紀・風紀 (external-sources/紀-daijisen.txt:5-7).
- F2 - RESOLVED - 鏡 is now declared on 範 (snapshot/kanji/範.md:14) and the note limits it to a model-to-learn-from sense (snapshot/kanji/範.md:48). The retained Daijisen きょう【鏡】 character entry gives sense 3 戒めとなる手本。模範。「鏡鑑」 (external-sources/鏡-retained-extract.txt:6). JMdict 1870020 鏡鑑 means paragon, and 2017840 marks 鏡 search-only for かがみ "model" (snapshot/docs/n1-sources/batch-123/reconciliation-001/jmdict-records.xml:1540-2018). The note does not claim the spellings are equivalent.
- F3 - RESOLVED - 限, 境 and 界 are now declared on 範 (snapshot/kanji/範.md:14) with a bounded note (snapshot/kanji/範.md:49). Daijisen supports a 区切り/delimited-area branch for each: 限 has 範囲を定める and 区切り (external-sources/04-限-tool-result.txt:1-110), 境 has 区切り目 and 一定の区切られた場所 (external-sources/05-境-tool-result.txt:1-77), and 界 has 空間を分けた区切り and 範囲を区切った特定の場所 (external-sources/06-界-tool-result.txt:1-57). These match 範's 区切られた枠 (original-packet/evidence/external-snapshots/01-extract.txt:20).
- O1 - RESOLVED - The metadata line now cites JMdict 1956840 (snapshot/kanji/範.md:55), whose 範 はん record glosses example and model (snapshot/docs/n1-sources/batch-123/reconciliation-001/jmdict-records.xml:1540-2018). The optional standalone 範を示す example was not added; that half of the suggestion was optional.
- O2 - RESOLVED - The note now attributes the 師 model/exemplar sense to KANJIDIC2 (snapshot/kanji/範.md:46), and the supplied complete KANJIDIC2 師 record lists model and exemplar (snapshot/docs/n1-sources/batch-123/reconciliation-001/kanjidic2-records.xml:802-1145). The 儀 wording was also narrowed to a conservative guard that does not claim 儀 itself means model. This is consistent with KANJIDIC2 儀 (ceremony, rule, affair, case, matter) and the whole-word JMdict 地球儀 and 儀範 records.
- O3 - RESOLVED - The Meaning section now states that Digital Daijisen also describes a delimited frame, illustrated by 範囲 and 範疇 (snapshot/kanji/範.md:23). This matches the Daijisen extract (original-packet/evidence/external-snapshots/01-extract.txt:20) and the unchanged 範囲 article's "bounds" gloss (snapshot/words/範囲.md:25).
- O4 - RESOLVED - 倣, 格 and 普 are now declared on 範 (snapshot/kanji/範.md:14) with bounded notes (snapshot/kanji/範.md:47; snapshot/kanji/範.md:50-51).
  - 格: JMdict 1205270 sense 3 gives rule/regulation/law.
  - 倣: JMdict 1599680 gives imitate/follow/emulate.
  - 普: KANJIDIC2 gives universal and wide(ly) (snapshot/docs/n1-sources/batch-123/reconciliation-002/kanjidic2-records.xml:1-79), against Daijisen 範 sense 3 広く行き渡る.
  - The 普 pair is declared directly, not inferred through 広 (snapshot/docs/n1-sources/batch-123/reconciliation-002/pair-disposition.json:1-20).

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: The revision resolves all seven items with source-backed changes. The new exclusions are 34 distinct, existing, single-character IDs that do not overlap the distractors 車, 書 and 達 (snapshot/kanji/範.md:13-14). Changes the author added beyond my requests (様, 形, 広, 道 and 坂) each rest on supplied dictionary records: JMdict 2713240 lists 様 as a spelling of ためし; Daijisen 範 sense 1 gives a 型 pattern; Daijisen 範 sense 3 gives widespread; JMdict 道 and Daijisen のり sense 3 give moral principle; and JMdict 1438050 gives an unrestricted engineering slope sense. The card qualifies each so that no frequency, spelling equivalence or synonymy is implied. Exclusions affect meaning choices only, so 坂 sharing the reading ハン does not matter. Of the nine pairs left unguarded, 本, 像, 囲, 方, 度, 計, 測, 量 and 理, none has a displayed title that would be a defensible answer for 範 on the supplied records, or vice versa. The new note lines check out against KANJIDIC2, JMdict and Daijisen. Metadata, readings, the curated choices, the 範囲 wrapper and the stroke data are unchanged. The committed host checks pass, with the same quiz-safety and reading-exposure outcomes; these are bounded host models, not device acceptance. No new defect is established.

## Findings
None.

## Optional
None.

## Limits
- L1: The fresh Weblio tool captures for 標, 紀, 鏡, 限, 境 and 界 are truncated. The 標 and 鏡 character entries were verified only through the retained earlier extracts. The 鏡 extract is an older coordinator capture, not a re-verified raw response. No pages were fetched in this pass.
- L2: Daijisen かがみ sense 2 (手本・模範) is spelling-restricted to 鑑/鑒, and JMdict 2017840 marks 鏡 search-only. The 鏡 guard therefore rests on the きょう【鏡】 character-entry sense 3, not on 鏡 being an ordinary spelling of the "model" word.
- L3: The nine no-new-guard pairs are accepted as bounded judgements on the supplied records. They are not claims that every contextual ambiguity is impossible, and no Daijisen entries were supplied for 本, 像, 囲, 方, 度, 計, 測, 量 or 理.
- L4: Quiz-safety, reading-exposure, unittest and the other committed checks are bounded Python host models. They do not cover caller-built or multi-borrow pools, Kotlin execution, native/device acceptance, whole-set acceptance or compatibility with the older installed APK 5c000bd.
- L5: Raw HTML responses, raw stroke SVGs, the binary Joyo PDF and any inputs outside the chain were not read. The stroke JSON and manifest bytes were not re-inspected beyond the supplied verification receipts.
- L6: My initial report is preserved unchanged. Its original limits (L1-L8 there) still describe what that pass saw.
