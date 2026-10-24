# Batch 50 confirmation review (N2:982–N2:1001): all three corrections hold, no new defects

## Snapshot
- Corrected commit: **bfc6d3d3e00525bc21aac101af8d06d7241b88f4**. Parent: 8c71fae49b615f2d6f0de34c6b00d1b20d17dd7e.
- I reviewed committed content only. My file tools cannot run Git, hash or cleanliness checks, and I did not look inside `.git`. Every hash and cleanliness claim below is the author's.

## Scope
- **Model:** claude-opus-5.5 (claude family). Read-only, with no agents and no edits.
- **Read in full this turn:**
  - `correction-snapshot.json` and `correction.patch`.
  - The current `words\体操.md`, `words\ダイヤグラム.md` and `words\竹.md`.
  - `corrective-comparison-reading.txt` (dictionary entries 1068870 スケジュール and 1315960 時間割).
  - `corrective-existing-reading.txt` (the existing スケジュール, 時間割 and 体育 articles).
- **Exact dictionary families reread:**
  - 1409580 体操 and 1409200 体育 (family-inspection-06, lines 34–44).
  - 1422230 竹 (family-inspection-06, lines 127–131).
  - 1076680 ダイヤグラム (family-inspection-01, lines 46–49).
  - 2855660 ダイヤ (family-inspection-11, lines 101–105).
  - 1543240 予定.
  - For spot-checks: 1414920 大分, 1280950 耕す and 1596830 炊く.
- **Other evidence this turn:**
  - Daijisen ダイヤグラム capture: `public-bodies.txt`, lines 129–136.
  - `corrected-review-evidence.json`, partially: lines 340–362, 2440–2470, 2575–2612, 2770–2830 and 27320–27760.
  - The actual TSV rows 982–1001.
- **Searches and spot-checks:**
  - `quiz_exclusions` in `words\` for regressions and duplicate guards.
  - Front matter (word, reading, title, level, kanji, exclusions) of all 20 articles.
  - Source aliases: タイア, 大分/だいぶん, and the appended N2 notes on 大木 and 耕す.
  - Reciprocal rows in the 詞, 植, 耕 and 竹 kanji cards.
- **Carried over from my first review:** complete reads of the 14 unchanged new articles, the 3 unchanged reused articles (だいぶ, 大木, 耕す) and the 4 kanji cards. The author's hashes for these files are the same in both snapshots, so I did not reread their bodies in full.
- **Not inspected:**
  - `manifest.json` (outside the permitted scope).
  - The changed `docs\n2-vocabulary-snapshot.json`, apart from a grep of its hash fields.
  - The middle of `corrected-review-evidence.json`.
  - No new web fetches.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:982 | words\体操.md (new) | Full reread at bfc6d3d plus patch | CLEAN | CLEAN | CLEAN |
| N2:983 | words\題名.md (new) | Carried over; unchanged per author's hash; front matter rechecked | CLEAN | CLEAN | CLEAN |
| N2:984 | words\代名詞.md (new) | Carried over; front matter and 詞 row rechecked | CLEAN | CLEAN | CLEAN |
| N2:985 | words\だいぶ.md (reused, N4) | Carried over; front matter and 大分/だいぶん rechecked | CLEAN | CLEAN | CLEAN |
| N2:986 | words\大木.md (reused) | Carried over; front matter and N2 note rechecked | CLEAN | CLEAN | CLEAN |
| N2:987 | words\タイヤ.md (new) | Carried over; タイア alias rechecked | CLEAN | CLEAN | CLEAN |
| N2:988 | words\ダイヤグラム.md (new) | Full reread plus patch | CLEAN | CLEAN | CLEAN |
| N2:989 | words\ダイヤモンド.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:990 | words\ダイヤル.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:991 | words\対立.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:992 | words\田植え.md (new) | Carried over; 植 rows rechecked | CLEAN | CLEAN | CLEAN |
| N2:993 | words\絶えず.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:994 | words\楕円.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:995 | words\高める.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:996 | words\耕す.md (reused) | Carried over; front matter, N2 note and 耕 rows rechecked | CLEAN | CLEAN | CLEAN |
| N2:997 | words\滝.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:998 | words\炊く.md (new) | Carried over; entry 1596830 rechecked | CLEAN | CLEAN | CLEAN |
| N2:999 | words\焚く.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:1000 | words\蓄える.md (new) | Carried over | CLEAN | CLEAN | CLEAN |
| N2:1001 | words\竹.md (reused) | Full reread plus patch and TSV row | CLEAN | CLEAN | CLEAN |

**Separate checks:**
- **Kanji edits:** CLEAN. The 詞 card gives 代名詞 under シ (row 28, Common words line 34). The 植 card gives 田植え under う.える with the 植え うえ form (row 29, line 35). Neither card changed in the correction.
- **Existing reciprocity:** CLEAN. The 耕 card links 耕す (lines 31 and 35) and the 竹 card links 竹 (lines 31 and 35), with no manufactured edits.
- **Reuse preservation:** CLEAN.
  - だいぶ is still N4 with `kanji: []`.
  - 竹 keeps its ID, reading たけ, title "bamboo", the four existing exclusions and the N2 level. Only lines 59–61 of the note changed.
  - 大木 and 耕す are unchanged.
- **Mappings:** CLEAN.
  - All twenty raw source fields are intact.
  - Nineteen selections are unchanged.
  - N2:1001 now selects senses 1422230:1,2 with no additional senses, matching the gloss "bamboo,middle (of a three-tier ranking system)".
- **Guard count:** 3+4+4+8+4+1+5+1+8+10+4+8+12 = 72 exclusions across 13 new cards, up from 71. This matches the author's figure.

## Findings
- **B50-QZ-01** (Minor, quiz exclusions; ダイヤグラム missing スケジュール/時間割 guards): **RESOLVED.**
  - `ダイヤグラム.md:9` now lists both words.
  - Lines 25–29 add "or the operating schedule itself". Lines 48–51 compare スケジュール and 時間割 while saying not every school schedule is a railway diagram.
  - Evidence: Daijisen 「また、その運行予定。」 (`public-bodies.txt:129–136`); 1068870 "schedule"; 1315960 "timetable…, schedule".
  - `スケジュール.md` does not declare ダイヤグラム, so the new guards add no duplicate declaration. The pairing is not inferred through ダイヤ.
  - No regression. Confidence: high.
- **B50-MAP-01** (Nit/Minor, mapping; N2:1001 selected only bamboo): **RESOLVED.**
  - TSV line 1001 now selects senses `1,2` with no additional senses, and its source note is rewritten.
  - The `竹.md:59–61` note matches the new selection. The original body teaching was untouched, as it should be.
  - Confidence: high.
- **GPT's flag on 体操/体育** (I had marked 体操 CLEAN): I **agree** with removing this guard.
  - 1409580 sense 3 ("PE class") is marked obsolete. 1409200 means physical education or the PE class.
  - The existing 体育 article says 体操 "is not an unrestricted synonym" for the school subject.
  - "Gymnastics; physical exercises" and "physical education" are not interchangeable answers in either direction.
  - The prose at `体操.md:36–41` and `47–50` still teaches the contrast and the obsolete sense without implying a guard. No other card guards this pair.
  - No regression. Confidence: medium-high, since this is an ordinary-answer judgment rather than proof that no context ever overlaps.
- **Regression sweep:** the three changed articles and the TSV show no front-matter, prose or link regressions.
- **New defects:** none.

## Optional
- My earlier optional guard ideas stay optional and are reasonably declined:
  - 絶えず with 続々/次々.
  - 高める with 持ち上げる/増える.
  - 対立 with 喧嘩.
- The optional 貯 link on 蓄える and the inherited 大木 wording also stay optional.
- **Evidence-file housekeeping:** `corrected-review-evidence.json` still holds the frozen originals at the top level:
  - `quizDeclarations` (lines 27325–27422): 体操 still has 体育, and ダイヤグラム has six items.
  - `sourceMappingDecisions` for N2:1001 (around lines 2786–2795): still sense [1] with additional sense `1422230:2`.

  The corrected values sit under `correctionEvidence`. Labeling the old sections "frozen/authored" would help anyone reading the file. This is not a repository defect.

## Limits
- Git, hash, cleanliness, equivalence and "unchanged file" claims are the author's. My carried-over verdicts rely on them.
- I did not check `manifest.json` contents. I only saw that its hash changed (fcda54bd… → db610d7c…), which fits regeneration.
- `docs\n2-vocabulary-snapshot.json` changed hash but is not in the listed content changes. I only grepped it: line 34 holds a `coverageIndexSha256` for the TSV, which would plausibly change with row 1001. I did not verify its value.
- Public dictionary bodies are the author's captures. I made no fresh retrievals.
- I did not read the evidence JSON files in full.
- Comparison articles other than スケジュール, 時間割, 体育 and the ones named in my first review were judged from titles and exclusions only.
- No live quiz run and no native-speaker certification.
