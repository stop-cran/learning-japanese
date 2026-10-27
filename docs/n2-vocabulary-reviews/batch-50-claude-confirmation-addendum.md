# Corrected batch 50 confirmation report (N2:982–N2:1001): four article labels fixed, verdicts unchanged

My previous confirmation report put the wrong articles on N2:983–N2:986. The actual TSV rows confirm the corrected assignments below. All twenty verdicts stay CLEAN/CLEAN/CLEAN, and no content defect remains. I'm issuing this as a complete new report; the earlier one stays as it was.

## Snapshot
- Corrected commit: **bfc6d3d3e00525bc21aac101af8d06d7241b88f4**. Parent: **8c71fae49b615f2d6f0de34c6b00d1b20d17dd7e**. The content is the same as in my previous confirmation report.
- I reviewed committed content only. My file tools cannot run Git, hash, equivalence, manifest or cleanliness checks, and I did not look inside `.git`. Every claim of that kind below comes from the author.

## Scope
- **Model:** claude-opus-5.5 (claude family). Read-only, with no agents, delegation or edits.
- **Checked this turn:**
  - `docs\n2-vocabulary-sources.tsv`, rows N2:982–N2:1001. Line 1 is the header, so row N2:n is file line n. I checked the article for every row, plus the new-versus-reused notes and the selected and additional senses.
  - `batch-50-correction-snapshot.json`, read in full. It lists 16 new and 4 reused articles, and its changed-file list has only `体操`, `ダイヤグラム`, `竹` and the TSV.
  - `batch-50-corrected-review-evidence.json`, lines 28–100 only. These are the mapping records for N2:983–N2:986, and they agree with the TSV.
- **Carried over from earlier turns (not reread this turn):**
  - Initial review at 8c71fae: complete reads of all 16 new and 4 reused articles, the related patch, the 詞/植/耕/竹 kanji cards, the mapping and component files, all 11 family-inspection files, the supplemental reading and the public dictionary headings.
  - Previous confirmation turn:
    - Complete rereads of `体操.md`, `ダイヤグラム.md` and `竹.md`, plus the correction patch.
    - The two new dictionary entries for スケジュール and 時間割, and the existing スケジュール, 時間割 and 体育 articles.
    - The exact dictionary families for these words.
    - Front-matter checks on all twenty articles, and spot-checks of the source aliases and the kanji cards' reading rows.
- **Not read this turn:** article bodies or front matter, kanji cards, `manifest.json`, `n2-vocabulary-snapshot.json` and the rest of the evidence JSON. No web fetches.

## Verdicts
How the "Read basis" column is abbreviated:
- **Initial** means I read the article completely at 8c71fae in the first review.
- **Unchanged** means the author's file hash is identical in both snapshots; I have not verified this myself.
- **FM** means I checked its front matter at bfc6d3d in the previous confirmation turn.
- **TSV** means I checked the actual row this turn.

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:982 | words\体操.md (new) | Full reread at bfc6d3d plus patch (previous turn); TSV | CLEAN | CLEAN | CLEAN |
| N2:983 | words\だいぶ.md (reused, N4) | Initial; Unchanged; FM, line 23 (大分/だいぶん) and entry 1414920 (previous turn); TSV; evidence lines 32–47 | CLEAN | CLEAN | CLEAN |
| N2:984 | words\大木.md (reused) | Initial; Unchanged; FM and N2 note at line 31 (previous turn); TSV; evidence lines 49–64 | CLEAN | CLEAN | CLEAN |
| N2:985 | words\題名.md (new) | Initial; Unchanged; FM (previous turn); TSV; evidence lines 66–81 | CLEAN | CLEAN | CLEAN |
| N2:986 | words\代名詞.md (new) | Initial; Unchanged; FM and 詞 kanji rows 28/34 (previous turn); TSV; evidence lines 83–95 | CLEAN | CLEAN | CLEAN |
| N2:987 | words\タイヤ.md (new) | Initial; Unchanged; FM and タイア alias at lines 28/44; TSV | CLEAN | CLEAN | CLEAN |
| N2:988 | words\ダイヤグラム.md (new) | Full reread at bfc6d3d plus patch (previous turn); TSV | CLEAN | CLEAN | CLEAN |
| N2:989 | words\ダイヤモンド.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:990 | words\ダイヤル.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:991 | words\対立.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:992 | words\田植え.md (new) | Initial; Unchanged; FM and 植 kanji rows 29/35; TSV | CLEAN | CLEAN | CLEAN |
| N2:993 | words\絶えず.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:994 | words\楕円.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:995 | words\高める.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:996 | words\耕す.md (reused) | Initial; Unchanged; FM, N2 note at line 53, 耕 kanji rows 31/35/41 and entry 1280950; TSV | CLEAN | CLEAN | CLEAN |
| N2:997 | words\滝.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:998 | words\炊く.md (new) | Initial; Unchanged; FM and entry 1596830; TSV | CLEAN | CLEAN | CLEAN |
| N2:999 | words\焚く.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:1000 | words\蓄える.md (new) | Initial; Unchanged; FM; TSV | CLEAN | CLEAN | CLEAN |
| N2:1001 | words\竹.md (reused) | Full reread at bfc6d3d plus patch (previous turn); TSV (senses `1,2`, no additional senses) | CLEAN | CLEAN | CLEAN |

**Separate conclusions:**
- **Kanji edits and links between kanji and word cards: CLEAN.** This comes from the previous turn and was not rechecked this turn.
  - `詞` links `代名詞` under the シ reading (row 28) and in Common words (line 34).
  - `植` links `田植え` under う.える, showing the 植え うえ form (row 29), and in Common words (line 35).
  - `耕` already linked `耕す` (lines 31/35) and `竹` already linked `竹` (lines 31/35), so no edits were needed there.
  - The author's hashes for all four kanji cards are unchanged.
- **Reuse preservation: CLEAN.**
  - This turn's TSV check confirms the four reused rows: だいぶ at level 4 (line 983), 大木 (984), 耕す (996) and 竹 (1001). Their notes say to preserve the original identity and body.
  - The body-level judgments come from earlier turns: だいぶ is still N4 with `kanji: []`, and 竹 keeps its identity, title and four exclusions.
- **Mappings: CLEAN.**
  - This turn's TSV check shows the raw source fields and selections consistent with my earlier reads. For example, N2:986 selects sense `1` with additional sense `1412340:2`, and N2:1001 selects `1,2` with no additional senses.
  - Nineteen selections are unchanged from the authored snapshot (author's claim, consistent with my earlier comparison).

## Findings
- **B50-CONF-BK-01** (report bookkeeping only, no content impact). Location: rows N2:983–N2:986 of the previous confirmation report's Verdicts table.
  - **Error:** those four rows named the wrong articles. They showed 題名, 代名詞, だいぶ and 大木; the correct articles are だいぶ (reused, N4), 大木 (reused), 題名 (new) and 代名詞 (new). The new/reused labels and the article-specific "Read basis" notes moved with the wrong rows. For example, the 詞 kanji check sat on N2:984 and the 大分/だいぶん check on N2:985.
  - **Evidence:** TSV lines 983–986 and corrected evidence lines 32–95. Totals were unaffected: 16 new and 4 reused.
  - **Impact:** none on the content. All four rows were and remain CLEAN on every facet, and checking the actual rows **changes no substantive judgment**.
  - **Fix:** the corrected table above. **Confidence:** high.
- **Earlier dispositions, carried forward without new content review:**
  - **B50-QZ-01** (ダイヤグラム missing スケジュール/時間割 guards): resolved.
  - **B50-MAP-01** (N2:1001 selected only the bamboo sense): resolved. TSV line 1001 still shows senses `1,2` with no additional senses.
  - **GPT's 体操/体育 guard removal:** I agree with it.
  - **Regressions:** none found in the previous turn across the three changed articles and the TSV.
  - **New content defects:** none.
  - There has been no new content change since then.

## Optional
- These remain optional and are reasonably not adopted:
  - Extra quiz guards: 絶えず with 続々/次々, 高める with 持ち上げる/増える, and 対立 with 喧嘩.
  - Linking 蓄える to the 貯 kanji card.
  - Rewording the inherited 大木 explanation.
- I withdraw my earlier evidence-file housekeeping suggestion. The frozen quiz and mapping records kept alongside `correctionEvidence` are historical records, as clarified.

## Limits
- **Author-run checks:** Git, hash, equivalence, manifest and cleanliness checks were run by the author. The verdicts for the 17 rows I did not reread rest on the author's claim that those files are unchanged.
- **This turn's reads:** I reread no article bodies, front matter or kanji cards. Front-matter and kanji-row evidence comes from the previous turn.
- **Evidence JSON:** this turn I cross-checked it only for N2:983–N2:986; earlier turns read it only in part.
- **Hash consistency:** in the previous turn, `docs\n2-vocabulary-snapshot.json:34` recorded the TSV hash as `e2bbe88a…`. That matches the author's TSV hash in `correction-snapshot.json`. Both values come from the author; I computed neither and did not reread that file this turn.
- **Not inspected:** the contents of `manifest.json`.
- **Public dictionary text:** these are the author's captures; I made no fresh retrievals.
- **Comparison words:** articles other than those I named were judged on titles and exclusions only.
- **Not tested:** no live quiz run and no native-speaker check.
