# Batch 53 confirmation review: corrected snapshot (claude-opus-5.5)

The correction resolves all four of my original findings without regressions, and I agree with the added チップ/末 guard. All twenty rows are now CLEAN on every facet. One correction to my own initial report: my 着々/徐々に citation (1345600) was wrong because that entry is archaic. The finding still holds on the right evidence, 1595480:1.

## Snapshot
- **Corrected commit:** 2be7616abc9dcef1ec5d2ab8219736e0ebca4d80. Parent: d67609747e671278f9a6a4e973ea0a0832a8cad8 (the authored snapshot). `cleanCommittedContent: true`.
- I reviewed committed content only. My file tools can't run Git, hash or cleanliness checks, and I didn't inspect .git, so those checks rest on the author.

## Scope
**Model:** claude-opus-5.5 (Claude family). Read-only; no edits, agents or delegation. This is a resumed confirmation of my initial report, not a blind review.

**Read in this pass:**
- **Snapshot and patch:** correction-snapshot.json and correction.patch (complete). The patch has exactly four word hunks and no kanji, TSV or reuse hunks.
- **Changed articles:** チップ, 地帯, 着々 and 中性, reread completely.
- **Corrective families:** correction-comparisons-compact.txt, all 11 families. I counted 29 senses myself: 1120070, 1525230/40/50/60, 1581610, 1595480, 2590770, 2746070, 2764560 and 2867582.
- **Old bodies:** correction-existing-reading.txt, all five (端, 末, ベルト, 徐々に, 酸性).
- **Public evidence:** correction-public-reading.txt (complete). I also read **public-bodies.txt completely (172 lines)**, which I had left unread initially.
- **Corrected evidence file:** batch-53-corrected-review-evidence.json lines 25700–25990 and 26640–26982. These cover the historical quizDeclarations and correctionEvidence (current declarations, counts, dispositions and the 茶色い body).
- **Mappings:** docs\n2-vocabulary-sources.tsv, the **twenty assigned rows only** (lines 1042–1061). My initial pass checked mappings only against the blind JSONL.
- **Targeted greps (current state):**
  - Front matter (jlpt, kanji, quiz_exclusions, quiz_distractors) and Dictionary lines of all 20 articles.
  - Titles and exclusions of 端, 末, ベルト, 徐々に and 酸性.
  - The reciprocal rows in 帯, 象 and 超.
  - Provenance precedent in words\.
  - Additional title-overlap searches.
- **Pinned glosses re-confirmed by grep:**
  - 1077740:3 "tip (of a ballpoint pen)" (family-inspection-02.txt:6).
  - 1345600, both senses marked archaic (family-inspection-05.txt:10–11).
  - 1422720:1 "brown, light brown, tawny" (family-inspection-06.txt:95).

**Inherited, not freshly reread:**
- **Article bodies:** the fourteen unchanged new articles, ちゃわん and 超過 come from my two complete initial reads. Current front matter, Dictionary lines and the 超過 provenance line were re-grepped and match.
- **Kanji cards:** the complete front matter of 帯, 象 and 超 comes from my initial full reads. Only their reciprocal rows and entry lists were re-grepped now.
- **Family evidence:** principal and supplemental families come from the initial complete reads.

**Not read:**
- public-bodies.json (I read the .txt instead).
- The rest of the corrected and original review-evidence files.
- docs\n2-vocabulary-snapshot.json, docs\n2-source-snapshot.json, docs\confusable-words.md and docs\jlpt-levels.md.
- Every forbidden file, including the two initial-review report files whose hashes appear in the snapshot.

The prompt calls 地帯/ベルト and 着々/徐々に "the other reviewer's" findings. In my initial report they were my own B53-C-02 and B53-C-03, and the author's dispositions map them that way. チップ/末 was the other reviewer's addition.

## Verdicts

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1042 | 知人 (new) | Inherited full reads; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1043 | 地帯 (new) | Complete reread; patch; 1120070 family; ベルト body | CLEAN | CLEAN | CLEAN |
| N2:1044 | 縮む (new) | Inherited; lines 40–50 reread; public body read | CLEAN | CLEAN | CLEAN |
| N2:1045 | 縮める (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1046 | 縮れる (new) | Inherited; hair/wrinkle lines re-grepped; public body read | CLEAN | CLEAN | CLEAN |
| N2:1047 | チップ (new) | Complete reread; patch; 1581610/1525250 families; 端 and 末 bodies | CLEAN | CLEAN | CLEAN |
| N2:1048 | 地点 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1049 | 地名 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1050 | 茶色い (new) | Inherited; lines 10–30 reread; complete public heading | CLEAN | CLEAN | CLEAN |
| N2:1051 | 着々 (new) | Complete reread; patch; 1595480 family; 徐々に body | CLEAN | CLEAN | CLEAN |
| N2:1052 | ちゃわん (reused N5; source 茶碗) | Inherited full read; jlpt 5 and `kanji: []` re-grepped; TSV row | CLEAN | CLEAN | CLEAN |
| N2:1053 | 中間 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1054 | 中旬 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1055 | 抽象 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1056 | 中世 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1057 | 中性 (new) | Complete reread; patch; 酸性 body; public body read | CLEAN | CLEAN | CLEAN |
| N2:1058 | 中途 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |
| N2:1059 | 中年 (new) | Inherited; lines 14–30 reread; public body read | CLEAN | CLEAN | CLEAN |
| N2:1060 | 超過 (reused; N2/provenance edit only) | Inherited full read; jlpt 2, line 42 and guards re-grepped; TSV row | CLEAN | CLEAN | CLEAN |
| N2:1061 | 彫刻 (new) | Inherited; front matter and TSV rechecked; public body read | CLEAN | CLEAN | CLEAN |

**Kanji edits and reciprocity:**
- **帯 edit: CLEAN.** 地帯 ちたい is in the タイ row (line 28) and Common words (line 39), with 1421360 at line 46.
- **象 edit: CLEAN.** 抽象 ちゅうしょう is in the ショウ row (line 30) and Common words (line 39), with 1426190 at line 46.
- **超 (unchanged): CLEAN.** 超過 ちょうか is already at line 28 (チョウ row) and line 34 (Common words), with 1429410 at line 43.
- All three use actual whole-word readings; no individual character readings were invented. The correction touches no kanji files.

**Baseline preservation: CLEAN.**
- Only four word files change.
- ちゃわん keeps jlpt 5 and `kanji: []`.
- 超過 keeps its jlpt 2 edit, provenance line and eleven baseline guards.
- 端, 末, ベルト, 徐々に and 酸性 are unchanged; their titles and guards match correctiveExistingLabels.
- The baseline kanji front matter is inherited from my initial full read.

**Mappings: CLEAN.**
- Every TSV selected/additional column matches the article's Dictionary line. For example:
  - 1047: 1077740:1, plus 1077740:2,3 and 2850287:1,2,4.
  - 1053: 1423680:1,3, plus :2.
  - 1055: 1426190:1, plus 1426200:1.
  - 1057: 1424710:1,3, plus :2.
  - 1058: 1425030:1, plus 2059610:1 and 1425050:1.
  - 1045: 1337570:1, plus :2,3.
- The reuse level columns (5 for ちゃわん, 2 for 超過) match front matter.
- No invented pinned sense numbers.

**Guard counts:** 81 guards on 15 cards, matching currentQuizDeclarations, versus 77 initially. That is exactly four additions and no removals. There are no duplicate or self IDs, every target exists, and no quiz_distractors exist to conflict.

## Findings
**Dispositions of my original findings:**

- **B53-C-01 (チップ/端): RESOLVED.**
  - The fix is at チップ.md:9.
  - Overlap: 1077740:3 is "tip (of a ballpoint pen)" and 1581610:1 is "end, tip, point, edge, margin". 端.md teaches "edge, end, or tip" and its title is "edge; end; tip".
  - The existing 先 and 先端 guards don't cover 端, because guards are not transitive. Confidence: high.
- **チップ/末 (other reviewer's addition): AGREE.** I missed this pair initially.
  - 末.md's Meaning paragraph says "meaning an end or tip", and 1525250:1 is "end, tip, top" with no misc flag.
  - The archaic 1525230 (うら) and the 1525260 (まつ, "the end (of)"/powder) entries are separate identities and are rightly not relied on.
  - Not excessive: a learner taught that 末 means "tip" could reasonably accept "tip; chip". Confidence: medium-high.
- **B53-C-02 (地帯/ベルト): RESOLVED.**
  - The fix is at 地帯.md:9.
  - The complete pinned 1120070:3 ("belt, zone, area") supersedes my unpinned initial Jisho retrieval.
  - The guard rests on that ordinary secondary sense and on 地帯's own title containing "belt". ベルト's old body (senses 1–2 only) doesn't establish it, and the rationale doesn't claim it does. Confidence: high.
- **B53-C-03 (着々/徐々に): RESOLVED, with my rationale corrected.**
  - I concede my initial citation was invalid: both senses of 1345600 are archaic (family-inspection-05.txt:10–11), and bare 徐々 is not the 徐々に identity.
  - The correct basis is 1595480:1, "gradually, steadily, slowly, little by little, step by step, by degrees", with no archaic flag.
  - The guard is a direct title comparison ("steadily; step by step" vs "gradually; by degrees"), not derived from だんだん. The two words are not interchangeable in all contexts: 着々 is orderly progress, 徐々に is gradual change. Confidence: high.
- **B53-C-04 (中性/酸性): RESOLVED.**
  - 中性.md:36 now reads `[酸性](酸性.md) (さんせい)`.
  - The target exists (title "acidity; acidic", reading さんせい), and all other wording is unchanged.

**My initial qualifications:**
- **茶色い public-backed claim: RESOLVED (was UNVERIFIED).**
  - The complete heading is `［形］茶色である。「―・い紙」`, equating the adjective with 茶色. Pinned 1422720:1 glosses 茶色 as "brown, light brown, tawny".
  - That supports 茶色い.md:18–19 ("the public dictionary gives the broader brown-color description").
  - The support is definitional (via 茶色) rather than a separate color description. That nuance is not a defect.
- **Mappings checked only against the blind derivative: RESOLVED** by reading the TSV rows directly.
- **public-bodies not read: RESOLVED.** The complete .txt matches the article claims checked. Examples:
  - 着々 「次々と順序よくはかどる」.
  - 縮む sense 4 ちぢれる (hair).
  - 縮れる sense 1 しわ (wrinkling).
  - 中性 senses 1–5.
  - 中年 「ふつう40歳代から50歳代」, which agrees with 中年.md:24's no-fixed-age statement.
  - チップ 心付け/祝儀 and wood chip.
  - 中旬 11th–20th.
  - 抽象 (スル).
- **超過 provenance-style concern: WITHDRAWN.** There is a precedent at 大木.md:31 ("The N2 label follows the pinned community vocabulary list.").

**Regression check:** No new defects. The four edits are confined to three guard lists and one link.
- The title searches I ran over existing words\ cards found no new required pair. ちびちび, 作品, 切れ and 屑 overlap only through English homonymy or category membership.
- 工業, 洗剤, 機械 and 準備 have cards but appear only in examples or compounds, not as named comparisons, so the B53-C-04 linking rationale doesn't extend to them.

## Optional
- **抽象:** a brief register note that 抽象する is formal/academic. I couldn't verify its frequency against 抽象化する.
- **中性:** a sense-2 example, such as Daijisen's 中性的な魅力.
- **着々:** a one-line contrast with 徐々に in the body. The guard doesn't need it.

I agree with the author that none of these is a defect. I withdraw my earlier 集合地点, straight-hair, 古代/近世, provenance-style and 茶色い-tag suggestions as unnecessary.

## Limits
- **Unchanged files:** that the unchanged files are identical rests on the correction patch, the author's Git/hash checks and my re-greps. Bodies of the sixteen unchanged word cards and the complete front matter of the three kanji cards are inherited from my initial full reads, not reread.
- **Public evidence:** it comes from a single service (Weblio Daijisen), as author captures, not fresh retrievals. I made no fresh retrieval in this pass.
- **Evidence and docs not read:** most of the corrected and original review-evidence JSON, public-bodies.json, the two docs snapshots, confusable-words.md and jlpt-levels.md. The level policy for reuses is assessed only through the TSV and the 大木 precedent.
- **Comparison coverage:** the search for comparison pairs relies on title searches, not on reading every words\ body.
- **Certification:** no runtime quiz draws. Example naturalness is a non-native judgment, not native-speaker certification.
