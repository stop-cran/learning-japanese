# Batch 70 confirmation review: N2:1382–1401 on corrected snapshot cced07e

All twenty rows, the three kanji edits, the mappings and the baselines come out CLEAN. My original findings F1–F3 are resolved and I found no regressions. I fetched both Kotobank pages myself, and they confirm the Dutch "pistool" source for ピストル and the ひき‐わけ【引分】 heading.

## Snapshot
- **Revised frozen commit:** `cced07e72cb5bc76192a2118fb47d8785a033d2e`.
- **Parent (authored snapshot):** `c30ca893b7f9271f6b3b95771a7ee361b9236e9f`.
- I reviewed committed content only. My file tools cannot run Git, so the clean checkout, manifest/hash and rendering-equivalence checks are the author's, not mine.

## Scope
- **Model:** claude-opus-5.5 (family claude). I made no edits and used no agents, delegation or shell.
- **Read in full in this stage:**
  - Private files: the correction snapshot, the correction patch and the reconciliation file.
  - All 20 current assigned articles.
  - Kanji cards 島, 比 and 算.
  - The TSV header and physical rows 1382–1401 only.
  - The mappings (20), principals (20 families, 45 senses) and components (28 records).
  - The correction comparison reading (9 families, 28 senses) and the correction public-bodies excerpts.
  - Complete bodies of words\受け持つ.md, 引き出し.md, だます.md and 抜く.md.
  - Both Kotobank pages, fetched myself: ぴすとる-3166237 and 引分-2077017.
  - Front matter for 下ろす, 降ろす, 担当, 承る, 任せる and 預かる.
  - A title-line search limited to words\ to look for overlapping English labels.
- **Carried over from my first review, not reread now:**
  - The guidance docs, docs\content-format.md, docs\confusable-words.md and the original public bodies.
  - The family and old-body chunks. The native receipts say 14 family chunks and 7 body chunks were returned. I only claim the depth my first report preserved. Returned bytes prove access, not comprehension.
- **Not read:** the optional files corrected-review-evidence.json, correction-completed-inspection.json, public-bodies.json and review-labels.jsonl.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1382 | 半島 | CLEAN | CLEAN | CLEAN | Unchanged; "peninsula" is taught; reciprocal link with 島 |
| N2:1383 | ハンドル | CLEAN | CLEAN | CLEAN | Footer (line 48) now says source senses 1-2, additional recognition 3-4, matching the mapping |
| N2:1384 | 日当たり | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1385 | 日帰り | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1386 | 比較的 | CLEAN | CLEAN | CLEAN | Unchanged; reciprocal link with 比 |
| N2:1387 | 日陰 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1388 | ぴかぴか | CLEAN | CLEAN | CLEAN | Stable identity; newly sourced N2 kept; blank source spelling kept |
| N2:1389 | 引き受ける | CLEAN | CLEAN | CLEAN | 受け持つ guard and comparison added; raw 引受る still shown as an alias |
| N2:1390 | 引き返す | CLEAN | CLEAN | CLEAN | Unchanged; 引返す alias |
| N2:1391 | 引き算 | CLEAN | CLEAN | CLEAN | Unchanged; reciprocal link with 算; 引算 alias |
| N2:1392 | 引き出す | CLEAN | CLEAN | CLEAN | N4 kept; 引き出し guard added; the three earlier guards kept |
| N2:1393 | 引き止める | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1394 | 卑怯 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1395 | 引き分け | CLEAN | CLEAN | CLEAN | 引分 cited to 精選版 ひき‐わけ【引分】 sense ② (fetch confirmed); no frequency claim; JMdict not misquoted |
| N2:1396 | 日差し | CLEAN | CLEAN | CLEAN | Unchanged; 陽射 alias |
| N2:1397 | 肘 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1398 | ピストル | CLEAN | CLEAN | CLEAN | Dutch "pistool" confirmed by my fetch of 精選版; unsourced English-route claim removed |
| N2:1399 | ビタミン | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1400 | ぴったり | CLEAN | CLEAN | CLEAN | N3 kept; blank ぴたり spelling and gloss kept; same-family variation does not change identity |
| N2:1401 | 引っ掛かる | CLEAN | CLEAN | CLEAN | Unchanged; existing だます contrast; no guard needed (see O4) |

- **Kanji edits:** all CLEAN.
  - 島: トウ row and 半島 はんとう link; footer has ID 1479770.
  - 比: ヒ row and 比較的 ひかくてき link; footer has ID 1483600.
  - 算: サン row and 引き算 ひきざん link; footer has ID 1601610.
  - Existing headers and examples are preserved, and no missing cards were invented.
- **Mappings:** CLEAN. All 20 are unchanged and match the TSV and principals, with selected and additional-recognition senses kept separate.
- **Baseline preservation:** CLEAN. No primary title, reading, identity, type, kanji, asset or scene changed.

## Findings
- **F1** (Medium; 引き受ける missing a 受け持つ guard): **RESOLVED.**
  - 引き受ける.md:9 now excludes 受け持つ, and lines 37-38 add the comparison.
  - The overlap is real: 受け持つ's title "take charge of" matches sense 1 of JMdict 1601520, "to take charge of".
  - Declaring the guard once covers both directions, and 受け持つ's own guards are untouched.
- **F2** (Low; 引分 unsupported): **RESOLVED** as a sourcing gap.
  - I **withdraw** any suggestion that 引分 is an invalid spelling; its absence from JMdict and Daijisen did not prove that.
  - Evidence: 引き分け.md:30-32 and :51, and my own Kotobank fetch.
- **F3 / GPT's B70-02** (Low; 引き出す missing a 引き出し guard): **RESOLVED.**
  - Evidence: 引き出す.md:9 and :41-42. The cash-withdrawal sense (sense 2) of JMdict 1601650 applies to the 引き出し spelling, so the guard is needed.
  - The earlier guards 下ろす, 降ろす and 出す are kept. 抜く already excludes 引き出す (shared "pull out").
- **GPT's B70-01** (ピストル): **RESOLVED.** Evidence: ピストル.md:26 and :46. My fetch shows 精選版 gives "〘名詞〙([オランダ語] pistool)".
- **O2** (ハンドル footer): **RESOLVED.**
- **O4** (引っ掛かる / だます): **WITHDRAWN** as an actionable item. I agree no guard is needed, for a concrete reason rather than a blanket voice or part-of-speech exemption:
  - The titles name opposite participants. "fall for a trick" is the person deceived, using the intransitive sense 4 of JMdict 1169350. "deceive; trick; coax" is the deceiver acting on a を-object.
  - 引っ掛かる.md:49-51 already states this contrast.
  - A small optional uncertainty remains because the bare label "trick" appears in both titles.
- **O1, O3, O5:** still optional and deferred.
- **Regressions:** none. Both new guards rest on direct overlaps between titles and ordinary senses, not on topic proximity.
- **Remaining actionable defects:** none.

## Optional
- **O1:** remove the process meta-line at 引き出す.md:48 ("retains its sourced N4 level when covering the N2 source row") and the similar line in ぴったり.
- **O3:** rephrase 引っかかる's description as "another recorded spelling".
- **O4 residual:** consider a 引っ掛かる/はめる note.
- **O5:** add backlinks in 掛け算 and 比較.
- **GPT's optional 日当たり の/が wording:** optional.

## Limits
- I did not reread the earlier family and old-body chunks or the optional evidence files in this stage.
- Exclusion judgments are my own reasoning; I ran no quiz draws.
- The Kotobank ピストル page's header shows the English spelling "pistol" as an alternative notation. The article attributes the Dutch origin only to 精選版, which my fetch confirms. I did not check other dictionaries' etymologies.
- This review does not certify exhaustive correctness, native-speaker naturalness or frequency, and author-executed hash checks were not reproduced.
