## Snapshot
The frozen commit is **2a1d30f2abe197b94ac8a92730fd8e69086ae30a** (parent 10eb0db442aca4eca75f52f4e15c81ebcd977b01). The review covers committed content only. My file tools cannot run Git, so I read working-tree files and could not confirm independently that they match this commit. `cleanCommittedContent: true` in frozen-snapshot.json is the author's claim.

## Scope
**Model:** claude-opus-5.5 (claude family). The review was read-only, with no agents and no edits.

**Read in full:**
- **Instructions:** `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md:18-126`.
- **Articles:** all 17 new articles, the three reused articles (出会い, 出入口, 出かける) and the three kanji cards (低, 券, 停).
- **Private files:**
  - frozen-snapshot.json and related.patch
  - review-mappings, review-principals, review-components and review-labels (234 labels)
  - principal-reading, family-inspection-01 to 06 and support-comparison-reading
  - public-bodies.txt, supplement-public-bodies.txt and support-public-bodies.txt
- **Repository evidence:** `docs\n2-vocabulary-sources.tsv` (header and rows 1122–1141).

**Partly read:**
- `review-evidence.json`: lines 1–120 and 2973–~3300 only.
- `docs\n2-vocabulary-snapshot.json`: lines 1–40 only.
- Comparison articles: titles and quiz_exclusions for about 150 words. I read full bodies only for 揃う and 下降.

**Not read:**
- The entryFamilies and componentEvidence sections of `review-evidence.json`.
- The three `*.json` capture files (I read their `.txt` equivalents instead).
- `confusable-words.md`, `jlpt-levels.md` and `n2-source-snapshot.json`.

**Web fetches:**
- The Weblio page for 出はいり worked. It shows で‐はいり【出入り／出×這入り】.
- The Kotobank page for 出掛ける redirected to an unrelated entry (嫡庶), and the Weblio page for 出掛ける returned only boilerplate. Neither counts as evidence.

## Verdicts
| ID | Article (raw) | Status | Entry:senses | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|---|---|
| N2:1122 | 強気 | new | 1236230:1-2 | CLEAN | CLEAN | CLEAN |
| N2:1123 | 釣り合う | new | 1434050:1-2 | CLEAN | CLEAN | CLEAN |
| N2:1124 | 吊る | new | 1434020:1 | CLEAN | CLEAN | CLEAN |
| N2:1125 | 吊るす (raw 吊す) | new | 1433980:1 | CLEAN | CLEAN | CLEAN |
| N2:1126 | 出会い (raw 出合い) | reused | 1338400:1-2 | CLEAN | CLEAN | CLEAN |
| N2:1127 | 手洗い | new | 1328020:1-3 | NEEDS FIX (F2) | CLEAN | NEEDS FIX (F2) |
| N2:1128 | 定員 | new | 1435400:1-2 | CLEAN | CLEAN | CLEAN |
| N2:1129 | 定価 | new | 1435410:1 | CLEAN | CLEAN | CLEAN |
| N2:1130 | 低下 | new | 1434250:1 | CLEAN | CLEAN | NEEDS FIX (F4) |
| N2:1131 | 定期券 | new | 1435510:1 | CLEAN | CLEAN | CLEAN |
| N2:1132 | 定休日 | new | 1435540:1 | CLEAN | CLEAN | CLEAN |
| N2:1133 | 停止 | new | 1434920:1-3 | CLEAN | CLEAN | CLEAN |
| N2:1134 | 停車 | new | 1434960:1 | CLEAN | CLEAN | CLEAN |
| N2:1135 | 停電 | new | 1435020:1 | CLEAN | CLEAN | CLEAN |
| N2:1136 | 出入り | new | 1339910:1-4 | NEEDS FIX (F1) | CLEAN | NEEDS FIX (F1) |
| N2:1137 | 出入口 | reused | 1598540:1 | CLEAN | CLEAN | CLEAN |
| N2:1138 | 手入れ | new | 1328250:1 (+2 additional) | CLEAN | CLEAN | CLEAN |
| N2:1139 | テーマ | new | 1078830:1 | CLEAN | CLEAN | CLEAN |
| N2:1140 | 出かける (raw 出掛ける) | reused | 1598550:1-2 | CLEAN | NEEDS FIX (F3) | NEEDS FIX (F3) |
| N2:1141 | 出来上がり | new | 1340600:1-2 | CLEAN | CLEAN | CLEAN |

**Kanji edits**
- **低: CLEAN.** The テイ reading row and Common words both link 低下, and 低下 links back to 低.
- **券: NEEDS FIX (F5).** Common words and the entry metadata now include 定期券, but the ケン reading row lists only 券.
- **停: NEEDS FIX (F5).** The テイ reading row links 停止 but not 停車 or 停電. Common words links all three, and the metadata adds 1434960.
- **Word side:** every N2 word links its existing component kanji in its own text. The missing cards (釣, 吊, 価, 逢, 遭, 這) stay plain text, which is correct.

**Baseline metadata: CLEAN.** The front matter of all three kanji cards is unchanged. The reused articles keep their identity, reading, title, kanji and level: 出会い stays N3 and keeps its 出会う guard; 出かける stays N5. 出入口 only gains `jlpt: 2`.

**Mappings: CLEAN in IDs, spellings, readings and senses, with one exception.** The N2:1136 source_note starts from a wrong assumption (F1).
- The raw 吊す correctly maps to the canonical 吊るす entry (1433980).
- 吊る (1434020) is correctly kept separate from 釣る (1434120).
- 強気 is correctly read つよき, not ごうぎ.
- 停止 correctly selects senses 1–3; sense 4 belongs to the reading ちょうじ.
- 手洗いする is supported by Daijisen, which marks the word ［名］(スル).
- 停車 is taught with the vehicle as subject, and the transitive use is credited to Daijisen.
- 定期券 is explained as short for 定期乗車券; 定休日 is supplemented by 定休.
- 手入れ's police-raid sense 2 is labelled as additional, not as an N2 sense.
- テーマ cites German Thema, and テマ is not promoted.
- 出来上がり is treated as a noun.

## Findings
**B57-F1**
- **Severity:** Moderate.
- **Facet:** correctness and comprehensibility.
- **Location:** `words\出入り.md:35` and `docs\n2-vocabulary-sources.tsv:1136` (source_note).
- **Claim:** line 35 says "The dictionary also has ではいり, but its spelling 出入 does not license reading that shorter spelling でいり". The pinned entry has no 出入 spelling at all, so the sentence invents one and misstates the restriction.
- **Remedy:** rewrite as "ではいり is a less common reading of 出入り (also 出這入り); the dictionary restricts でいり to the spelling 出入り." Correct the TSV source_note the same way.
- **Evidence:**
  - family-inspection-03.txt:93-94 lists the spellings 出入り, 出這入り and 出はいり. The reading でいり is restricted to 出入り; ではいり is unrestricted.
  - public-bodies.txt:251-252 and the fresh Weblio fetch show で‐はいり【出入り／出×這入り】.
- **Confidence:** high.

**B57-F2**
- **Severity:** Minor.
- **Facet:** correctness and comprehensibility.
- **Location:** `words\手洗い.md:18,25`.
- **Claim:** line 25 says "The first and third examples use 手洗いする". The first example (line 18) is 手洗いをしましょう, which is the noun plus をする.
- **Remedy:** "The first example uses 手洗いをする and the third 手洗いする."
- **Evidence:** public-bodies.txt:110 and 116 (［名］(スル), 「セーターを―する」).
- **Confidence:** high.

**B57-F3**
- **Severity:** Minor.
- **Facet:** scoped coverage and comprehensibility.
- **Location:** `words\出かける.md:41-44`.
- **Claim:** the article teaches sense 2 ("be about to leave") with 今、出かけるところです. In that sentence the "about to" meaning comes from ところです, which works with any verb. Nothing shows 出かける itself carrying sense 2, and learners may credit the meaning to the wrong part.
- **Remedy:** say that ところです is a general pattern, and add a context where the verb carries the sense, such as 出かけたところに客が来た ("a visitor came just as I was going out").
- **Evidence:**
  - JMdict 1598550 sense 2: "to be about to leave; to be just going out".
  - public-bodies.txt:302: 「出て行こうとする…「―・けたところに客が来る」」.
- **Confidence:** medium.

**B57-F4**
- **Severity:** Minor.
- **Facet:** quiz_exclusions.
- **Location:** `words\低下.md:4,9`.
- **Claim:** two likely quiz confusions are not excluded:
  - 下げる ("lower; hang") directly overlaps the "lowering" in 低下's title. The article already excludes the transitive 減らす, so it treats transitive counterparts as confusable.
  - 落ちる's ordinary sense "decline/deteriorate" overlaps 低下's title, and the existing 下降 card already excludes 落ちる on the same grounds.
- **Remedy:** add 下げる, and probably 落ちる, to the exclusions.
- **Evidence:**
  - 下げる.md:4 has no exclusions.
  - JMdict 下げる sense 2 "to lower, reduce"; 落ちる sense 3 "decline, deteriorate".
  - 下降.md:9.
- **Confidence:** medium for 下げる; low-medium for 落ちる.

**B57-F5**
- **Severity:** Minor.
- **Facet:** kanji reciprocity.
- **Location:** `kanji\停.md:30` and `kanji\券.md:30`.
- **Claim:** the requested reading-row examples are missing for three of the five pairs: 停車 and 停電 are not in 停's テイ row, and 定期券 is not in 券's ケン row. Common words and the word-side links are present.
- **Remedy:** add the linked words to those reading-row cells. 77 kanji cards already put several linked words in one reading-row cell.
- **Confidence:** medium. The facts are certain; whether this is a defect depends on your reciprocity requirement, since content-format.md does not require it.

## Optional
- **出入口:** JMdict ranks 出入り口 (ichi1/news1/nf18) above 出入口. The article could say which form is more common.
- **Article additions:** 停車 could contrast with 駐車, and 吊る could mention 首を吊る (sense 2).
- **Low-confidence guards:** 釣り合う and 差し引き both have "balance" in their titles. 低下 and 断る both have "decline"; 下降 already excludes 断る, so excluding it here would be consistent.
- **停止 exclusions:** 停電, 断水 and しまう are broad but defensible, since JMdict 停止 sense 2 covers interruption of supply.
- **Gaps that predate this batch:** 出入口 has no exclusions against 入口, 出口 or 玄関. 出かける has none against 発つ or 外出.

## Limits
- **Single dictionary service:** all positive public captures are Daijisen through Weblio, and they are the author's captures, not fresh retrievals.
- **Failed endpoint:** the raw 吊す page returned nothing and is not evidence.
- **Not reproduced:** the author's hash and equivalence checks.
- **Unread sections:** the unread parts of review-evidence.json may hold relevant records. I checked components through review-components.jsonl and the kanji cards instead.
- **Comparison judgments:** these rest mostly on titles plus JMdict senses, not full comparison bodies.
- **No native-speaker check:** sentence naturalness has not been certified by a native speaker.
- **Interpretive findings:** F3, F4 and F5 involve judgment calls.
