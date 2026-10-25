## Snapshot
**65c98d9db417dd02abd5f24f1b48a5d95947a3f1** (parent 86c16b88ae91b6064c55d1d379d904b3121aa44c). I reviewed committed content only. My file tools can't run Git, so this commit identity, the clean-tree status and all hash/equivalence checks come from the author's `frozen-snapshot.json`; I did not verify them myself.

## Scope
- **Reviewer:** claude-opus-5.5, Claude family. I worked alone and made no edits.
- **Instructions read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-103`.
- **Assigned files, read completely:**
  - All 17 new articles.
  - The two reused articles, でこぼこ and 照らす.
  - The edited cards `kanji\鉄.md`, `kanji\橋.md` and `kanji\照.md`.
  - `related.patch`.
- **Mappings:** the TSV header and rows N2:1142–1161, retrieved by grep.
- **Private files read:**
  - Fully: `frozen-snapshot.json`, `review-mappings.jsonl`, `review-principals.jsonl` (19 families), `review-components.jsonl`, `review-labels.jsonl`, `public-bodies.txt` and `supplement-public-bodies.txt` (解凍).
  - Grep only: `family-inspection-01` through `-11` and `support-comparison-reading.txt`. I searched them only to confirm the 手帳 cross-reference IDs, which are 2530640 (身体障害者手帳) and 1830990 (警察手帳).
- **Comparison articles:**
  - Full: 成長, 揃う, 差す, 手段, 日光, 晴れ, 荷物, 豚肉, コート, 迎え.
  - Front matter only: 仕方, 申請, 自分, 圧縮, 前進, ぎらぎら, きらきら, 見送り.
  - I also searched all titles under words\ for overlapping English glosses.
  - `docs\confusable-words.md`: a grep found no entries for these words.
- **Existence checks (glob):** `kanji\` (的, 帳, 展, 頃, 拭, 砲, 凸 and 凹 have no cards) and `words\`.
- **Web lookups:** 木橋 on Kotobank (精選版日本国語大辞典 gives もっきょう and きばし) and on Weblio (the Wikipedia article gives もくきょう).
- **Not read:** `review-evidence.json`, `principal-reading.txt`, `public-bodies.json`, `supplement-public-bodies.json`, `docs\jlpt-levels.md`, `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`. Forbidden ledgers and the batch source file were not accessed.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| Row | Article | New or reused | Cells |
|---|---|---|---|
| N2:1142 | 出来上がる | new | **NEEDS FIX** (F-03) / CLEAN / CLEAN |
| N2:1143 | 的確 | new | CLEAN / CLEAN / CLEAN |
| N2:1144 | 的確, raw spelling 適確 | same article | CLEAN / CLEAN / CLEAN |
| N2:1145 | 手首 | new | CLEAN / CLEAN / CLEAN |
| N2:1146 | でこぼこ, raw spelling 凸凹 | reused | CLEAN / CLEAN / CLEAN |
| N2:1147 | 手頃 | new | **NEEDS FIX** (F-01) / CLEAN / CLEAN |
| N2:1148 | でたらめ | new | CLEAN / CLEAN / CLEAN |
| N2:1149 | 手帳 | new | CLEAN / CLEAN / CLEAN |
| N2:1150 | 鉄橋 | new | CLEAN / CLEAN / CLEAN |
| N2:1151 | 手続き | new | CLEAN / CLEAN / CLEAN |
| N2:1152 | 鉄砲 | new | **NEEDS FIX** (F-02) / CLEAN / CLEAN |
| N2:1153 | テニスコート | new | CLEAN / CLEAN / CLEAN |
| N2:1154 | 手拭い | new | CLEAN / CLEAN / CLEAN |
| N2:1155 | 手前 | new | CLEAN / CLEAN / CLEAN |
| N2:1156 | 出迎え | new | CLEAN / CLEAN / CLEAN |
| N2:1157 | 出迎える | new | CLEAN / CLEAN / CLEAN |
| N2:1158 | 照らす | reused | CLEAN / CLEAN / CLEAN |
| N2:1159 | 照る | new | CLEAN / CLEAN / CLEAN |
| N2:1160 | 展開 | new | **NEEDS FIX** (F-04) / CLEAN / **NEEDS FIX** (F-05) |
| N2:1161 | 伝記 | new | CLEAN / CLEAN / CLEAN |

**Kanji edits:**
- **鉄: CLEAN.** The テツ reading row (line 30) and Common words (lines 36–37) link 鉄橋 and 鉄砲, and the entry list adds 1437820 and 1438010.
- **橋: CLEAN.** The キョウ row (line 28) and Common words (line 34) link 鉄橋.
- **照: CLEAN.** The て.る row (line 31) and Common words (line 38) link 照る, and the existing 照らす links remain.
- **Word side of the five pairs:** every article links its components substantively, with whole-word readings てっきょう, てっぽう, てる and てらす.

**Baseline metadata: CLEAN.**
- **でこぼこ:** gains only `jlpt: 2` plus an explicit 凸凹 recognition sentence. Its primary spelling, reading, title, type, empty kanji list and tags are unchanged. It had no exclusions to preserve.
- **照らす:** gains `jlpt: 2` and a link to 照る. All eight exclusions are preserved.
- **Kanji cards:** front matter is unchanged.

**Mappings: CLEAN as mappings.**
- **Sense selections:** all 20 match the principal families, including restrictions such as でこぼこ sense 2, which is restricted to the reading でこぼこ.
- **Article notes:** two articles contradict their mapping notes. 鉄砲 leaves 鉄炮 unqualified (F-02), and 手頃 cites fewer senses than the mapping selects (F-01).

## Findings
**F-01. Minor. Facet: source attribution.** `words\手頃.md:33` (taught at lines 4 and 16).
- **Claim:** The footer cites only "entry 1327660, sense 1", but the title and second example teach sense 2 ("suitable; reasonable; moderate"). The mapping selects senses 1 and 2.
- **Remedy:** Change the footer to "senses 1-2".
- **Evidence:** In `review-principals.jsonl`, 1327660 sense 2 is glossed "suitable / reasonable / moderate". The TSV row for N2:1147 has `sense_indices` 1,2.
- **Confidence:** high.

**F-02. Minor. Facet: variant qualification.** `words\鉄砲.md:23`.
- **Claim:** The sentence "鉄炮 is another dictionary spelling" doesn't say the form is rare. The mapping note claims "Rare 鉄炮 remains qualified", while 手首 does qualify its rare 手頸.
- **Remedy:** Say "鉄炮 is a rarely used dictionary spelling."
- **Evidence:** JMdict 1438010 marks 鉄炮 as "rarely used kanji form".
- **Confidence:** high.

**F-03. Minor. Facet: quiz_exclusions.** `words\出来上がる.md:9` (compare `words\揃う.md:9`).
- **Claim:** 出来上がる ("be finished; be ready") does not exclude 揃う ("be complete; be all present; match"). 揃う already guards 仕上がる ("be finished; be completed"), できる ("…be ready"), 完成 and 完了, which are the exact overlaps 出来上がる combines. 出来上がる's first JMdict gloss is "to be completed".
- **Remedy:** Add 揃う to 出来上がる's exclusions, or add 出来上がる to 揃う's; one side is enough because exclusions are symmetric.
- **Evidence:** `review-labels.jsonl` line 139 (揃う) and principal 1340610 sense 1.
- **Confidence:** medium-high.

**F-04. Minor. Facet: quiz_exclusions.** `words\展開.md:9`.
- **Claim:** 展開 ("unfolding; development; expansion") excludes 発展 ("development; expansion"), 発達 ("development; growth") and 過程, but not 成長 ("growth; development"). That title reorders the same two words as 発達's, and 発展 itself guards 成長. A quiz could offer two choices that both fit "development".
- **Remedy:** Add 成長.
- **Evidence:** Label lines 131 (成長) and 165 (発展 → 成長), and `words\成長.md:4`.
- **Confidence:** high.

**F-05. Minor. Facet: linguistic layers.** `words\展開.md:25`.
- **Claim:** "The on readings テン + カイ support the idea of opening out" treats the pronunciation as if it carried meaning; only the characters do.
- **Remedy:** Say the characters' meanings support the idea, and give テン + カイ as the reading separately.
- **Evidence:** The line text itself; checks item 3 asks for pronunciation and associations to be kept separate.
- **Confidence:** medium-high.

## Optional
- **でたらめ (line 23):** Daijisen records the commonly cited dice origin 《さいころを振って、出たその目のままにする意》. A qualified origin note could say 出 and 目 match that origin, while 鱈 is purely phonetic.
- **照る:** The title includes "be sunny" but there is no example. 降っても照っても (Daijisen sense 2) would show it.
- **出迎える (line 19):** The second example uses で, while line 16 mentions only に; a one-line note on で would help.
- **手続き (line 9) and 出迎え/出迎える:** Possible parity guards are 手段 (because 法 guards 方法, 手段 and 仕方) and お目に掛かる (because 会う is already guarded). Neither is established as a defect.
- **鉄砲:** Daijisen also describes the sumo thrusting technique, not only the practice pole.

## Limits
- I could not run Git, so the hash checks remain the author's claims.
- These files were not read: `review-evidence.json`, `principal-reading.txt`, the two `*-public-bodies.json` files and `docs\jlpt-levels.md`. The family-inspection files were only grepped. Supplementary families beyond the 19 principal families were not independently inspected.
- Quiz-collision checks covered the author's labels file plus a title search for selected English keywords. They are not exhaustive across every word.
- The Daijisen captures all come from one service (Weblio) and are the author's own captures; 木橋 was my only fresh lookup.
- Naturalness of the examples is judged, not certified by a native speaker.
