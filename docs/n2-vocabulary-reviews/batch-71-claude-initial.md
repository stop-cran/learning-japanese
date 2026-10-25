## Snapshot
**88aea28d8f5e1d4d17088835c03b9c93d19eb6cd** (parent 0e8e0b43c74d97a7367c5438012d09d495f34b18). I reviewed committed content only. My file tools can't run Git, so I couldn't independently check that the working tree matches the commit or diff it against the parent. The hash and equivalence checks were run by the author, not by me.

## Scope
**Model:** claude-opus-5.5 (claude family). Read-only review; no delegation and no edits.

**What I read in full:**
- **Snapshot and instructions:** frozen-snapshot.json, .github\copilot-instructions.md, .github\instructions\content-structure.instructions.md, and docs\content-format.md lines 18-103.
- **Assigned content:** all twenty assigned articles, related.patch, and the complete kanji\筆.md and kanji\皮.md.
- **Source rows:** TSV line 1 and lines 1402-1421 only.
- **Private files:** mappings.jsonl, principals.jsonl (all twenty families), components.jsonl, labels.jsonl and public-bodies.txt.
- **Older bodies:** 転がす, 工夫, おおよそ, 絞る, 著す, 出入り and 人込み.

**Searches:**
- Grepped title lines in words\ for overlapping meanings.
- Checked words\ and kanji\ for which files exist. There are no cards for 繰, 需, 瞳, 独 or 捻, and none for 日の出, 日没, とりあえず, プラスチック, 嫌味 or 勝手.
- Grepped docs\confusable-words.md; it has no matches.

**External checks:**
- The jisho.org API (current JMdict) loaded for 日の入り and 一休み.
- Kotobank loaded but didn't show definition text, so it verifies nothing.

**Not read:** review-evidence.json, public-bodies.json, family-inspection-01 to 18, old-body-inspection-01 to 20, supplement-comparison-reading.txt, docs\n2-vocabulary-snapshot.json, docs\n2-source-snapshot.json and docs\jlpt-levels.md. I didn't open any forbidden files.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1402 | 筆記 | CLEAN | CLEAN | CLEAN | Transitive する and senses 1-3 match. The broad exclusions (文字/字/文章) are low-harm. |
| N2:1403 | ひっくり返す | NEEDS FIX | CLEAN | CLEAN | Raw 引っ繰り返す (rare) is recognized. Missing exclusion 転がす (B71-01). |
| N2:1404 | ひっくり返る | CLEAN | CLEAN | CLEAN | Intransitive, senses 1-2 correct. |
| N2:1405 | 引っ越し | CLEAN | CLEAN | CLEAN | Raw 引越し is recognized; intransitive する. |
| N2:1406 | 引っ込む | CLEAN | CLEAN | CLEAN | Senses 1-3 handled appropriately. |
| N2:1407 | 筆者 | NEEDS FIX | CLEAN | CLEAN | Self-reference use covered. Missing exclusion 著す (B71-05). |
| N2:1408 | 必需品 | CLEAN | CLEAN | CLEAN | 需 is kept in metadata with no link, correctly, since there is no card. |
| N2:1409 | 人差し指 | CLEAN | CLEAN | CLEAN | Raw 人差指 (search-only form) recognized; second-toe sense covered. |
| N2:1410 | 一通り | NEEDS FIX | CLEAN | NEEDS FIX | Missing exclusion おおよそ (B71-03); unclear title wording (B71-09). |
| N2:1411 | 人通り | NEEDS FIX | CLEAN | CLEAN | Missing exclusion 出入り (B71-04). |
| N2:1412 | ひとまず | CLEAN | CLEAN | CLEAN | Blank source spelling preserved; 一先ず noted; sense 2 included. |
| N2:1413 | 瞳 | CLEAN | CLEAN | CLEAN | 瞳 kept in metadata with no link; 眸 (rare) and 睛 (search-only) are accurate. |
| N2:1414 | 一休み | NEEDS FIX | CLEAN | CLEAN | Unsupported spelling 一やすみ (B71-06). |
| N2:1415 | 独り言 | CLEAN | CLEAN | CLEAN | 独 left plain text (no card); rare-spelling labels accurate. |
| N2:1416 | ひとりでに | CLEAN | CLEAN | CLEAN | Blank source spelling preserved. |
| N2:1417 | ビニール | CLEAN | CLEAN | CLEAN | Blank source spelling preserved; vinyl-record sense correctly kept to バイナル only; no "plastic" titles conflict. |
| N2:1418 | 皮肉 | CLEAN | CLEAN | CLEAN | Senses 1-4 match JMdict and Daijisen. |
| N2:1419 | 日にち | CLEAN | CLEAN | CLEAN | The source gloss belongs to ひび/にちにち; the article handles this correctly. |
| N2:1420 | 捻る | NEEDS FIX | CLEAN | CLEAN | Missing exclusion 工夫 (B71-02). |
| N2:1421 | 日の入り | NEEDS FIX | CLEAN | NEEDS FIX | Unsupported spellings (B71-07); reading of 入る not given (B71-08). |

- **筆 edit:** CLEAN. 筆記 ひっき and 筆者 ひっしゃ are added to the ヒツ row and Common words. Footer IDs 1487800 and 1487830 match the articles. The header and existing examples are preserved, and the links work in both directions.
- **皮 edit:** CLEAN. 皮肉 ひにく is added with footer ID 1483900. The caution about etymology is appropriate, existing content is preserved, and the links work in both directions.
- **Baseline preservation:** CLEAN, based on related.patch and the snapshot (Git not executed). All twenty articles are new. No identity, title, level, asset or exclusion changes.
- **Mappings (20):** correctness, scoped coverage and comprehensibility are all CLEAN. Entries, selected/additional senses and restrictions match the principals, and footer IDs match.

## Findings
- **B71-01; Minor; Correctness (quiz)**
  - **File:** words\ひっくり返す.md:9.
  - **Claim/impact:** 転がす is not excluded, so a quiz can show two defensible answers in either direction.
  - **Remedy:** add 転がす.
  - **Evidence:** JMdict 1601870 sense 2 is "to knock over; to tip over". 転がす's title is "roll something along; tip over". The two articles give the same translation, "I accidentally knocked the glass over" (ひっくり返す.md:21; 転がす.md:19).
  - **Confidence:** High.
- **B71-02; Minor; Correctness (quiz)**
  - **File:** words\捻る.md:4,9.
  - **Claim/impact:** the title contains "devise", but 工夫 ("ingenuity; devising a method") is not excluded.
  - **Remedy:** add 工夫.
  - **Evidence:** Daijisen ひねる sense 6 is "わざと変わった趣向や考案をする". 捻る.md:22 says the word covers "making something ingenious".
  - **Confidence:** High.
- **B71-03; Low; Correctness (quiz)**
  - **File:** words\一通り.md:9.
  - **Claim/impact:** おおよそ ("approximately; outline") is not excluded, though its meaning overlaps as much as the already-excluded およそ.
  - **Remedy:** add おおよそ.
  - **Evidence:** JMdict 1164910 sense 1 is "generally; in the main; briefly; roughly". Daijisen sense 3 gives あらまし. おおよそ.md:16-17 says "generally; on the whole" and "outline or gist".
  - **Confidence:** Medium.
- **B71-04; Low; Correctness (quiz)**
  - **File:** words\人通り.md:9.
  - **Claim/impact:** 出入り ("coming and going") is not excluded.
  - **Remedy:** add 出入り.
  - **Evidence:** Daijisen defines 人通り as "人が行き来すること". 出入り.md:18-19 has 人の出入りが多い, translated "Many people come and go".
  - **Confidence:** Medium.
- **B71-05; Low; Correctness (quiz)**
  - **File:** words\筆者.md:9.
  - **Claim/impact:** 著す ("author; publish a work") is not excluded, and both titles include "author".
  - **Remedy:** add 著す.
  - **Evidence:** 筆者.md:4 and 著す.md:4. 著す.md:9 already excludes 著者 "author" for the same noun/verb overlap.
  - **Confidence:** Medium.
- **B71-06; Minor; Correctness**
  - **File:** words\一休み.md:30.
  - **Claim/impact:** the article lists 一やすみ as a recognized spelling, but no source supports it.
  - **Remedy:** keep only ひと休み.
  - **Evidence:** the frozen JMdict 1161830 lists only 一休み and ひと休み, and the current jisho API shows the same. The Daijisen heading is 【一休み】.
  - **Confidence:** High.
- **B71-07; Minor; Correctness**
  - **File:** words\日の入り.md:29.
  - **Claim/impact:** "日入 and 日の入 are additional dictionary spellings" is not supported by the dictionaries the article cites.
  - **Remedy:** delete the sentence, or cite a dictionary that lists these spellings.
  - **Evidence:** the frozen JMdict 1463800 lists only 日の入り, as does the current jisho API. The Daijisen heading is 【日の入り】.
  - **Confidence:** Medium-high.
- **B71-08; Low; Comprehensibility**
  - **File:** words\日の入り.md:27.
  - **Claim/impact:** "from 入る, to enter" gives no reading. Learners will default to はいる, but the いり here comes from いる.
  - **Remedy:** add "(いる)".
  - **Evidence:** KANJIDIC 入 lists い.る and はい.る; the article's reading is ひのいり.
  - **Confidence:** Medium-high.
- **B71-09; Low; Comprehensibility**
  - **File:** words\一通り.md:4,12.
  - **Claim/impact:** in the quiz, the title "general pass" reads like an admission pass.
  - **Remedy:** use a phrase like "once-over; roughly" or "briefly; in general".
  - **Evidence:** the source gloss is "ordinary, usual, in general, briefly", and JMdict sense 1 is "generally… briefly… roughly".
  - **Confidence:** Medium.

## Optional
- 一通り.md:21: "All the main dishes are ready" adds "main". "Everything is set out" would be closer.
- ひとりでに: JMdict flags 一人でに as "irregular kanji usage", which the article could mention. The sentence beginning "not obtained by treating every use of 一人…" is awkward.
- 瞳: the article could mention the iris/colour use in Daijisen sense 1 (青い瞳).
- ひっくり返す: the article could mention the page-flipping use in Daijisen sense 2.
- 皮肉: the article could add "satire" from JMdict sense 1.
- 捻る ↔ 絞る: worth considering an exclusion. Both have a "rack one's brains" idiom (頭をひねる and 知恵を絞る), and 捻る has a wringing sense (JMdict sense 3). I have low confidence in this one.

## Limits
- Git was not executed, so I couldn't confirm the working tree matches the snapshot or diff it against the parent.
- All the Daijisen captures come from one source (Weblio), not twenty-two independent dictionaries.
- B71-07 can't rule out headings in other dictionaries (for example Nihon Kokugo Daijiten), because Kotobank showed no definition text.
- Exclusion judgments rely on full titles plus the seven older bodies I read. I didn't open the author's family-inspection or old-body files, so for any older article I didn't open, a missing exclusion conflict isn't confirmed as absent.
- The mapping notes come from the compact blind JSONL; I didn't check them against the original batch file, which was forbidden.
- This review doesn't certify naturalness as a native speaker would.
