# Batch-57 correction review: all five original findings are resolved, and I found no regressions

## Snapshot

- **Corrected commit:** `e2315ebd92a28ebbea5ccfd9a69218bbf5ea1cce`.
- **Parent:** `2a1d30f2abe197b94ac8a92730fd8e69086ae30a` (the authored snapshot).
- **Basis:** both values come from `correction-snapshot.json`, which I read first. I reviewed committed content only. File tools cannot run Git, hash, cleanliness, metadata or manifest checks, and I did not look in `.git` instead. The author-reported coverage hash change (d49ab8c… → d4a25ca…) is not verified.

## Scope

**Model:** claude-opus-5.5 (Claude family). Read-only. No agents, no edits, and no web fetches this turn.

**Read completely this turn:**
- **Private files:**
  - `correction-snapshot.json`
  - `correction.patch`
  - `reconciliation-comparison-reading.txt`: 14 families, 89 senses (下げる 5, 壊れる 3, 差し引き 2, 手洗い 3, 出入り 6, 上がる 26, 揃う 3, 断る 3, 釣り合う 2, 低下 1, 停止 4, 適当 2, 落ちる 27, 出かける 2).
  - `correction-existing-reading.txt`: 8 older bodies (落ちる, 下げる, 上がる, 壊れる, 揃う, 適当, 差し引き, 断る).
  - `correction-public-reading.txt`: the captured dictionary headings for 手洗い, でいり, ではいり and 出掛ける.
- **The six changed articles:** 手洗い, 出入り, 低下, 停止, 釣り合う and 出かける.
- **All three kanji cards:** 低, 券 and 停.
- **TSV:** the header and rows N2:1122–1141.
- **Style check:** a search of `kanji\` reading rows for the separator between linked words (55 cards use the same `; [` pattern).

**Inherited from my initial review, not reread this turn:**
- The 14 unchanged articles.
- `frozen-snapshot.json`, `related.patch`, the compact evidence files, the family-inspection files and the original public captures.

**Not read:**
- `corrected-review-evidence.json`. I checked the current guards and the added pairs against the patch's inline correction diff and the actual article front matter instead.
- `docs\confusable-words.md`, `docs\jlpt-levels.md` and `docs\n2-source-snapshot.json`.
- `docs\n2-vocabulary-snapshot.json`, apart from its patch hunk.

**Older comparison bodies read in full:** 揃う and 下降 in the initial review, plus the 8 bodies listed above this turn. Every other quiz-exclusion judgment rests on titles, existing guards and complete dictionary families, not complete old bodies.

## Verdicts

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1122 | 強気 (new) | Unchanged; initial judgment inherited | CLEAN | CLEAN | CLEAN |
| N2:1123 | 釣り合う (new) | Changed; fully reread with families 1434050, 1406110, 1437450 and the 揃う/適当 bodies | CLEAN | CLEAN | CLEAN |
| N2:1124 | 吊る (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1125 | 吊るす (new; raw 吊す) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1126 | 出会い (reused; raw 出合い) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1127 | 手洗い (new) | Changed; fully reread with 1328020 and the public capture | CLEAN | CLEAN | CLEAN |
| N2:1128 | 定員 (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1129 | 定価 (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1130 | 低下 (new) | Changed; fully reread with 1434250, 1548550, 1184170, 1419570, their bodies and 低 | CLEAN | CLEAN | CLEAN |
| N2:1131 | 定期券 (new) | Article inherited; 券 reread | CLEAN | CLEAN | CLEAN |
| N2:1132 | 定休日 (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1133 | 停止 (new) | Changed; fully reread with 1434920, 1352290, 1199900, 1548550, their bodies and 停 | CLEAN | CLEAN | CLEAN |
| N2:1134 | 停車 (new) | Article inherited; 停 reread | CLEAN | CLEAN | CLEAN |
| N2:1135 | 停電 (new) | Article inherited; 停 reread | CLEAN | CLEAN | CLEAN |
| N2:1136 | 出入り (new) | Changed; fully reread with 1339910, the でいり/ではいり captures and the TSV note | CLEAN | CLEAN | CLEAN |
| N2:1137 | 出入口 (reused) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1138 | 手入れ (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1139 | テーマ (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |
| N2:1140 | 出かける (reused; raw 出掛ける) | Changed; fully reread with 1598550 and the 出掛ける capture | CLEAN | CLEAN | CLEAN |
| N2:1141 | 出来上がり (new) | Unchanged; inherited | CLEAN | CLEAN | CLEAN |

- **Kanji reciprocity: CLEAN.** All five pairs now have a reading-row link, a Common words link and a substantive link from the word article at the actual reading:
  - 低/低下 (ていか) at `低.md` reading and Common words rows.
  - 券/定期券 (ていきけん) at `券.md:30` and Common words.
  - 停/停止 (ていし), 停/停車 (ていしゃ) and 停/停電 (ていでん) at `停.md:30` and Common words.
  - The `; [` separator matches house style.
- **Baseline preservation: CLEAN.** Kanji metadata is unchanged. The primary identity, reading, title, level and kanji of 出会い, 出入口 and 出かける (でかける, N5, [出]) are unchanged. No baseline exclusions were removed.
- **Mappings: CLEAN.** The raw fields, IDs, article associations, levels, and selected and additional senses are unchanged. The only changed note, N2:1136, matches 1339910 exactly.

## Findings

**Original findings**

- **B57-F1 (出入り spelling claim): RESOLVED.**
  - Fixed at `出入り.md:35` and in the N2:1136 note.
  - The fix matches 1339910: spellings 出入り, rare 出這入り and search-only 出はいり; でいり restricted to 出入り; ではいり unrestricted.
  - It also matches the captured で‐はいり【出入り／出×這入り】 heading.
  - It makes no frequency claim and no language-wide prohibition. High confidence.
- **B57-F2 (手洗い construction attribution): RESOLVED.**
  - `手洗い.md:25` now correctly says the first example uses 手洗いをする and the third uses 手洗いする.
  - The dictionary supports する (［名］(スル); 「セーターを―する」). High confidence.
- **B57-F3 (出かける, "about to leave" attribution): RESOLVED.**
  - I agree the original ところです construction was never wrong.
  - My concern was that the example credited a general construction to the verb itself. `出かける.md:46-50` now separates the two:
    - ところ is described as a general stage expression.
    - The verb's own "about to leave" use is shown by the Daijisen sense-2 example 「―・けたところに客が来る」, given in the past tense.
  - The translation and the "In that context" limit are supported. I retain no consequential disagreement; one nuance is under Optional. Medium-high confidence.
- **B57-F4 (低下 guards): RESOLVED.**
  - 落ちる is justified by its ordinary sense 3, decline or deterioration of quality, speed or sales, despite the old card's physical title.
  - 下げる is justified by sense 2, lower or reduce, and its old-body volume example テレビの音を下げて.
  - I did not rely on the existing 減らす or 下降 guards. High confidence.
- **B57-F5 (kanji reciprocity): RESOLVED** at `券.md:30` and `停.md:30`. High confidence.

**Guard additions I did not originally raise**

- **停止 + 壊れる: supported.** 壊れる's title is "break; stop working", matching its sense 2.
- **停止 + 上がる: defensible.** Sense 14 means cut out or die, and the old body teaches 雨が上がる, "the rain stops".
- **停止 + 落ちる: defensible.** Sense 23 is a server going down.

  None of these three is an excess. Medium confidence.
- **釣り合う + 揃う: supported.** 揃う's title includes "match", and its sense 2 is match or be even.
- **釣り合う + 適当: supported.** 適当's sense 1 "suitable" matches 釣り合う's sense 2 "to suit", consistent with the existing 適する guard. No transitive propagation through 合う or マッチ was used. Medium-high confidence.

**My original optional items**

- **釣り合う/差し引き and 低下/断る:** downgraded to low-confidence optional ideas.
  - The complete families confirm different meanings: subtraction, net balance or fluctuation for 差し引き; refusal, notice or permission for 断る.
  - The 差し引き body explicitly rejects physical balance.
  - Only English title words ("balance", "decline") overlap.
- **Spelling-frequency ranking:** withdrawn as a frequency claim, since priority tags are not measured usage.
- **駐車, 吊る sense 2, and the 出入口/出かける baseline guards:** still optional.

**New defects or regressions:** none. Front matter is intact. There are no duplicate exclusions, every new guard target exists, there were no removals, and the TSV note and article agree.

## Optional

- **出かける:** contrast the sense-2 context with the common 今出かけたところです, "has just gone out", so learners do not over-apply "not a completed outing".
- **出入り:35:** could say that ではいり means the same thing as でいり.
- **Low-confidence ideas:** guarding 釣り合う/差し引き (possible overlap in income-and-expenditure contexts) and 低下/断る (shared English word "decline").

## Limits

- Commit identity comes from the author's snapshot file. Hashes, manifests and cleanliness were not checked.
- The public captures are author-captured and come from a single dictionary service. No fresh retrieval was made this turn.
- For unchanged rows, conclusions about missing guards rest on titles plus complete families. Only 10 older comparison bodies were read in full.
- I did not read `corrected-review-evidence.json` or several other permitted docs.
- How strong the 上がる/落ちる guards are, and how to read 出かけたところに, are interpretive judgments.
- No quiz draws were run, no native speaker checked the content, and no frequency data was measured.
- The two reviewers worked at different depths, so the results do not support ranking the models or drawing bias conclusions.
