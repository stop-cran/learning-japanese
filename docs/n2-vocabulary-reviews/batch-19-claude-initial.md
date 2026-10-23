## Snapshot
**bec5240238e832cc953cbb1f04dbaaf3609a830c** (parent 6ec1829ae5a6f091c951437473b5adbbc867cfd1). The review covers committed content only. I had file tools and no Git execution, so I read the working-tree files and the supplied related patch. I could not confirm that those files match the commit, and I did not recompute the hashes.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked sequentially and made no edits.
- **New articles (all 18 read in full):** 看病, 冠, 漢和, 気圧, 着替え, 機関車, 飢饉, 器具, 期限, 記号, 刻む, 儀式, 基準, 起床, 着せる, 基礎, 気体, 基地.
- **Related changes (all 10, read in context):** the patch plus kanji\圧, 替, 準, 床, 械, 規, 着, 被, words\機械.md (lines 35–43) and words\被せる.md (line 36).
- **Reuse claim:** 機械.md (N3) for the 器械 apparatus sense. I checked only the changed passages and the unchanged identity fields (word, reading, title, level, exclusions). This is not a full recertification of the article.
- **Mappings:** I checked TSV rows N2:362–381, including N2:375 and N2:376, which both map to 基準.md.
- **Evidence used:** the source rows, all 19 principal entry families, the KANJIDIC2 component records, the quiz declarations and rationale, the inspection receipts, and the comparison families needed for specific claims (1119210, 2845313, 1655450, 1737360, 1423170, 1040060, 1240810, 1222700). I also checked titles of all exclusion targets, scanned titles for overlapping English labels, checked docs\confusable-words.md (no hits) and fetched Daijisen entries for 規準, 基準 and 恩に着せる.
- **Not read:** none of the forbidden documents.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 看病 | CLEAN | CLEAN | CLEAN |
| 冠 | CLEAN | CLEAN | CLEAN |
| 漢和 | CLEAN | CLEAN | CLEAN |
| 気圧 | CLEAN | CLEAN | CLEAN |
| 着替え | CLEAN | CLEAN | CLEAN |
| 機関車 | CLEAN | CLEAN | CLEAN |
| 飢饉 | CLEAN | CLEAN | CLEAN |
| 器具 | CLEAN | CLEAN | CLEAN |
| 期限 | CLEAN | CLEAN | CLEAN |
| 記号 | CLEAN | CLEAN | CLEAN |
| 刻む | CLEAN | CLEAN | CLEAN |
| 儀式 | CLEAN | CLEAN | CLEAN |
| 基準 | CLEAN | CLEAN | CLEAN |
| 起床 | CLEAN | CLEAN | CLEAN |
| 着せる | CLEAN | CLEAN | CLEAN |
| 基礎 | CLEAN | CLEAN | CLEAN |
| 気体 | CLEAN | CLEAN | CLEAN |
| 基地 | CLEAN | CLEAN | CLEAN |

**Ten related changes: CLEAN / CLEAN / CLEAN.**
- 圧, 替, 準 and 床 each gain a link to the new word at its actual reading, plus the entry ID.
- The aliases on 械 (器械), 規 (規準) and 被 (被せる read きせる) point to spellings the target articles actually teach.
- The 被 alias sits in Common words, not the readings table. That is correct, because KANJIDIC2 has no き.せる reading for 被.
- 着 links 着せる in its readings table and attributes the two added entries.
- The 機械 and 被せる edits are accurate.

**Reuse claim (機械): CLEAN / CLEAN / CLEAN.** JMdict sense 2 marks 器械 as "often" used for the apparatus meaning, and the article presents this as a tendency. The new sentence 実験に使う器械を点検しました is natural. The N3 level, title and exclusions are unchanged, and 器具's exclusion of 機械 covers that pair in both directions.

**All 20 mappings: CLEAN / CLEAN / CLEAN.**
- Every source spelling, reading and selected sense is explicitly taught.
- Raw glosses that don't fit are qualified: 冠's "first; best" belongs to かん, 記号's "code" is limited to contextual use, and 気体's "vapour" is marked as contextual.
- For N2:376, 規準 is taught in 基準.md with its reading, an example and the dictionary nuance, and 規.md links back to it.

## Findings
None. I found no defects needing a fix within scope. Spot checks that support this:
- **Exclusion targets:** all exist, and their titles back the stated reasons.
- **Unguarded title pairs:** the ones that look similar have clearly different full English titles. Examples: 台 "stand; supporting base" vs 基地; 学期 "school term" vs 期限; 看護婦 vs 看病; イコール vs 記号.
- **Metadata:** every article lists all the kanji in its spelling.
- **Kanji cards:** missing cards were correctly not created.

## Optional
- **O-01** 基地.md:29: "a musical bass identity" is internal jargon. Bass is actually a separate dictionary entry (2845313), not a sense of 1119210. Suggested rewording: "ベース can also be a separate word meaning musical bass."
- **O-02** 期限.md:16–21: both examples show the deadline sense. Adding an example of the "term" sense (sense 1, e.g. 期限付き) would help.
- **O-03** 漢和.md:16–21: neither example shows 漢和 used on its own as the abbreviation.
- **O-04** 冠.md:29: the naming/sponsorship sense has no example (e.g. 冠大会 かんむりたいかい).
- **O-05** 気圧.md:27: the "not pronounced きゃつ" note is odd and could be removed.
- **O-06** kanji\着.md:44–45: these lines use a hyphen, while lines 40–43 use an em dash.
- **O-07** Mentions on non-N2 cards could become links: 刻.md:34,40 (刻む), 限.md:33,39 (期限), 漢.md:36 (漢和).

## Limits
- I couldn't run Git, so I can't confirm that the files and patch I read match the commit.
- I read only 8 of the 127 comparison families; the rest were relied on as summarised in the evidence file.
- I independently confirmed Daijisen only for 規準, 基準 and 恩に着せる. For 冠/冠たる, 漢和, 器械 and the other 着せる senses I relied on the author receipts, JMdict and my own knowledge. Two Kotobank fetches returned unrelated pages and count as limits, not evidence.
- My judgement that the example sentences are natural is not native-speaker or corpus certification. Borderline cases: 国語と漢和の辞典 and 目は覚めましたが、まだ起床していません.
- I didn't run the app's quiz; overlapping labels were checked only by searching titles.
- The fetch tool left three temporary files in %TEMP%, which I couldn't delete without a shell.
