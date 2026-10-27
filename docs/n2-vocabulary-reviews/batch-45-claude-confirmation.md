# Batch 45 confirmation review: one new Low fix needed (成立 needs a 効力 quiz exclusion)

All five of my original findings are resolved, and the correction patch introduces no regressions. One new Low issue remains, which my initial review missed: 成立 has no quiz exclusion for 効力, although both titles contain "validity". Read-only; I used file tools only and did not run Git.

## Snapshot
- **Commit:** 5911eeab48dd93455a75ee54cab7b86113ac1266. The receipt gives parent 7ffb9fef77051410d247dfde7de6c8315ccb8e6f, which matches my original snapshot.
- **Committed content only:** the receipt says "cleanCommittedContent: true". I treated the working tree as that commit.
- **Not reproduced:** I could not reproduce the hash or equivalence checks with file tools. The author ran them.

## Scope
- **Model:** claude-opus-5.5 (Claude family), resuming my own initial batch-45 review session.
- **Read in full this pass:**
  - the correction receipt and the correction patch;
  - words\せっかく.md, 成立.md, 西暦.md, 接する.md, 生存.md and 赤道.md;
  - kanji\角.md;
  - the complete fifteen-family rendering in corrections-comparison-reading.txt.
- **Read in part this pass:**
  - In corrections-existing-reading.txt, the full comparison cards 苦心, 一生懸命, 機会, チャンス, きっかけ, 誕生, 建設, 結論, 終わり, 当たる, 連絡, 時代, 年代, 世紀, 死亡, 緯度 and 熱帯, plus the start of 片付ける.
  - words\効力.md.
  - 1375880 and 1381140 in principal-reading.txt.
  - The Daijisen captures in public-bodies.txt at lines 203 and 247.
- **Searches this pass:**
  - I searched `title:` lines in words\ for overlapping English words.
  - I rechecked the reciprocal-link lines in kanji\清, 掃, 党, 門, 接 and 角.
  - I rechecked the eight old-word link lines.
- **Inherited without rereading:**
  - the fourteen unchanged new cards;
  - the 成長 comparison body, apart from its link line;
  - the twenty TSV mappings.
- **Not mine:** the 140-body and 216-label figures count the author's inspection, not mine.

## Verdicts
Columns: correctness / scoped coverage / comprehensibility.

| Source | Article | Status this pass | Verdict |
|---|---|---|---|
| N2:882 | 青少年 | inherited | CLEAN / CLEAN / CLEAN |
| N2:883 | 整数 | inherited | CLEAN / CLEAN / CLEAN |
| N2:884 | 清掃 | inherited | CLEAN / CLEAN / CLEAN |
| N2:885 | 生存 | **reassessed** | CLEAN / CLEAN / CLEAN |
| N2:886 | 生長 | inherited | CLEAN / CLEAN / CLEAN |
| N2:887 | 政党 | inherited | CLEAN / CLEAN / CLEAN |
| N2:888 | 生年月日 | inherited | CLEAN / CLEAN / CLEAN |
| N2:889 | 性能 | inherited | CLEAN / CLEAN / CLEAN |
| N2:890 | 整備 | inherited | CLEAN / CLEAN / CLEAN |
| N2:891 | 成分 | inherited | CLEAN / CLEAN / CLEAN |
| N2:892 | 性別 | inherited | CLEAN / CLEAN / CLEAN |
| N2:893 | 正方形 | inherited | CLEAN / CLEAN / CLEAN |
| N2:894 | 正門 | inherited | CLEAN / CLEAN / CLEAN |
| N2:895 | 成立 | **reassessed** | **NEEDS FIX (N1)** / CLEAN / CLEAN |
| N2:896 | 西暦 | **reassessed** | CLEAN / CLEAN / CLEAN |
| N2:897 | 背負う | inherited | CLEAN / CLEAN / CLEAN |
| N2:898 | 赤道 | **reassessed** | CLEAN / CLEAN / CLEAN |
| N2:899 | せっかく | **reassessed** | CLEAN / CLEAN / CLEAN |
| N2:900 | 接近 | inherited | CLEAN / CLEAN / CLEAN |
| N2:901 | 接する | **reassessed** | CLEAN / CLEAN / CLEAN |

**Kanji edits:** all CLEAN / CLEAN / CLEAN.
- **角 (updated, reread):**
  - Line 46 now gives the horn-breaking account with qualification.
  - Line 48 cites Daijisen.
  - Line 40 is spelling navigation for 折角 → せっかく and is not counted as a primary pair. Metadata is unchanged.
- **The five unchanged cards (reciprocal lines rechecked):**
  - 清: セイ row at line 30 with 清掃; Common words at line 42.
  - 掃: ソウ row at line 30; Common words at line 39.
  - 党: Meaning at line 20; トウ row at line 30; Common words at line 39.
  - 門: モン row at line 30; Common words at line 37.
  - 接: セツ row at line 30 with 接近 and 接する; Common words at lines 41-42; the small-っ note at line 50.

**Old-word edits:** all CLEAN / CLEAN / CLEAN.
- The link lines are all present at 青年:31, 小数:28, 誕生日:28, 性:28, 四角:27, 四角い:35, 門:29 and 成長:42.
- The 成長 comparison judgment is inherited.

**Mappings N2:882-N2:901:** CLEAN / CLEAN / CLEAN, inherited. The patch changes no mapping.

## Findings
**My original findings:**
- **F1 (Medium) — resolved.**
  - せっかく.md:9 now excludes 苦心 ("painstaking effort; taking pains"), 一生懸命 ("with utmost effort"), 機会 ("opportunity") and チャンス ("chance; opportunity").
  - The extra きっかけ exclusion is justified: its title is "trigger; opening; opportunity" and 1591290:1 includes "opportunity".
- **F2 (Low) — resolved.**
  - せっかく.md:30-35 and 角.md:46 now match the Daijisen capture at public-bodies.txt:203 (朱雲…鹿の角を折る…「漢書」朱雲伝の故事から), and both are properly qualified.
- **F3 (Low) — resolved by the author's alternative remedy; I withdraw my "add 世紀" remedy.**
  - My finding was about inconsistency: 時代 and 年代 were excluded but 世紀 was not.
  - Removing the 時代 and 年代 exclusions settles that.
  - The full title "Common Era year numbering; Western calendar" is not a plausible answer for "era; period" (時代), "era; period of years" (年代) or "century; era" (世紀). 1381140 is a dating system, while 1316300, 1468950 and 1373990 are periods or centuries.
  - 西暦.md:39-40 teaches this distinction explicitly, so those period words can now usefully appear as distractors.
  - This is my own reassessment, not forced agreement.
- **F4 (Low) — resolved.** 赤道.md:33-35 links 緯度 and 熱帯.
- **F5 (Low) — resolved.** 生存.md:36 links 死亡.
- **Optional 二つの面を接する example — resolved.**
  - 接する.md:26-28 now uses ひざを接する, which matches Daijisen sense 6 at public-bodies.txt:247 (近くに寄せる。近づける。「ひざを―・する」).
  - The card says "bringing close", which is accurate.

**Other checks on the changes:**
- **成立:** 誕生 (1419080:2 "formation"), 建設 ("establishment"), 結論 ("conclusion") and 終わり ("end; conclusion") are justified exclusions. My initial review missed the "conclusion" overlap.
- **接する:** 当たる (1448810:2 "to touch") and 連絡 ("contact") are justified. The new title "treat people" introduces no clash, because 扱う is already excluded.

**N1 (new; Low; correctness, quiz exclusions; confidence medium-high)**
- **Where:** 成立.md:4 and 9; 効力.md:4 and 9.
- **Problem:**
  - 成立's title "formation; conclusion; validity" and 効力's title "efficacy; validity; potency" share the exact English word "validity".
  - Neither card excludes the other, although both are jlpt 2.
  - 成立 already excludes 有効 ("valid; effective") for the same reason.
  - The meanings differ (1375880:3 is an argument being valid; 効力 is the legal force of an agreement), but the English labels are ambiguous.
- **Status:** not a regression from this patch. It is pre-existing, and the author's label packet did not list 効力.
- **Remedy:** add 効力 to 成立's quiz_exclusions.

**Regressions from this patch:** none found.

## Optional
- Align 接.md:30 and 42, which still gloss 接する as "deal with", with the new title "treat people". "Deal with" is still an accurate gloss, and no rule requires these glosses to match the word title.
- 西暦 vs 日付 ("calendar date") and 接する vs 境界/国境 ("border") share only one English word, across different word classes. No guard is needed.
- These items from my first report are still optional:
  - the stranded 正方形 一辺 note;
  - 成立させる;
  - the せいそん reading;
  - more 背負う collocations.

## Limits
- I did not run Git, and the receipt's hash and equivalence checks were run by the author. I can't confirm with file tools that the working tree is the committed state, or that 効力.md was already in my original snapshot.
- I did not fetch any web pages. All Daijisen evidence comes from the author's captures.
- I did not reread the fourteen unchanged cards, the 成長 comparison body or the TSV mappings. Their verdicts are inherited.
- My overlap search matched English words on `title:` lines only, so overlaps in other wording may be missed.
- I assumed how the quiz uses exclusions from the repository docs.
- CLEAN is not a native-speaker certification.
