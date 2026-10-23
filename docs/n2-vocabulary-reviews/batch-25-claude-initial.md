## Snapshot
The frozen commit is **c6d44ce4b6dd2e8fceb2fa8ffae7c632ed87e801** (parent 3a3517322ec749d892e8fe5f97f4cac2a54431ae). The receipt marks the content as clean and committed, with no reuse claims. I reviewed committed content only. I had file tools but no Git execution, so I could not check the commit, the diff provenance or the recorded file hashes myself.

## Scope
- **Model:** claude-opus-5.5 (Claude family), in a fresh process.
- **Instructions read:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-119`.
- **Articles:** all 20 read in full.
- **Related edits:** the four-file patch for 県, 庁, 恋 and 芸, plus each changed passage in context.
- **Mappings:** TSV rows N2:482–N2:501 only.
- **Evidence read:** the rows, all 20 principal entry families, the 136 existing-card labels and exclusions, the author-inspection receipts, the quiz declarations and the stated source limits.
- **Evidence searched only:** the 307 comparison families were consulted by targeted search, not read in full.
- **Other cards checked:** 拝む, 一流, 天然, 故郷, 生物, 生き物, 寂しい, 押さえる, ゲーム, 県 and others. I also grepped every word title for meaning collisions.
- **Outside sources fetched:** the Daijisen entry for 請う on Weblio, and the Jisho API (JMdict-based) for 生物 and いきもの.
- **Not read:** every forbidden file, including `batch-25.json` and all review or notes documents.

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| 原産 | NEEDS FIX (F6) | CLEAN | CLEAN |
| 原始 | NEEDS FIX (F3) | CLEAN | CLEAN |
| 研修 | CLEAN | CLEAN | CLEAN |
| 厳重 | CLEAN | CLEAN | CLEAN |
| 謙遜 | CLEAN | CLEAN | CLEAN |
| 県庁 | CLEAN | CLEAN | CLEAN |
| 限度 | CLEAN | CLEAN | CLEAN |
| 現に | CLEAN | CLEAN | CLEAN |
| 顕微鏡 | NEEDS FIX (F5) | CLEAN | CLEAN |
| 原理 | CLEAN | CLEAN | CLEAN |
| 原料 | CLEAN | CLEAN | CLEAN |
| 碁 | CLEAN | CLEAN | CLEAN |
| 恋しい | CLEAN | CLEAN | CLEAN |
| 請う | NEEDS FIX (F1); naturalness of example 2 UNVERIFIED (F2) | CLEAN | NEEDS FIX (F2) |
| 工員 | CLEAN | CLEAN | CLEAN |
| 強引 | CLEAN | CLEAN | CLEAN |
| 公害 | CLEAN | CLEAN | CLEAN |
| 高級 | NEEDS FIX (F4) | CLEAN | CLEAN |
| 公共 | CLEAN | CLEAN | CLEAN |
| 工芸 | CLEAN | CLEAN | CLEAN |

**Kanji edits:** all four are CLEAN on all three facets.
- 県 and 庁 each add 県庁 (けんちょう) and add entry 1258880 to the footer.
- 恋 links 恋しい in the meaning text, the こい.しい readings row and Common words. Entry 1558760 was already in its footer.
- 芸 adds 工芸 (こうげい) and adds entry 1278090 to the footer.
- Missing kanji cards (修, 厳, 謙, 遜, 顕, 微, 鏡, 碁, 請, 級) stay as metadata only. Every existing component card is linked.

**Mappings:** all 20 are CLEAN on all three facets.
- Every spelling, reading and entry ID matches its article.
- The selected senses are correct: sense 1 for every row except 原始, which selects senses 1 and 2.
- The two extra senses are labelled honestly in the articles: 請う 1592920:2 (pray/wish) and 高級 1283400:2 (high rank).

## Findings
**F1. Moderate · correctness (quiz) · `words\請う.md:9`. Confidence: high.**
- **Problem:** the existing 拝む card is titled "worship; beg" (`words\拝む.md:4`), so it shares the exact word "beg" with 請う ("beg; request; invite"). Both are native verbs tagged wago and verb. Neither card excludes the other: 拝む excludes 祈る, 願う, 頼む, 拝見 and 見る.
- **Impact:** a quiz can show two defensible answers. 請う already excludes 祈る and 願う for the same reason.
- **Fix:** add 拝む to 請う's `quiz_exclusions`.

**F2. Moderate · comprehensibility (naturalness UNVERIFIED) · `words\請う.md:17,20`. Confidence: high for the mismatch, medium for naturalness.**
- **Problem:** line 17 says "What is requested can take を; the person asked can take に." In 専門家を講師に請いました, を marks the person invited and に marks their role. A learner who applies line 17 would parse it as "asked the lecturer for a specialist."
- **Naturalness:** Daijisen lists only (1) asking someone for something, with 食物/救援/許しを請う, and (2) praying to gods. It gives no "invite" use. The Weblio example sentences consistently use "person に + thing を請う", which matches line 17 but not the example. The construction Xを講師に請う looks invented, and lines 44–46 of the article themselves warn against invented 請う collocations.
- **Fix:** replace example 2 with an attested one, such as 王様に助命を請うた or 許しを請う. If the invite example stays, explain its frame and cite a source.

**F3. Minor · correctness (quiz) · `words\原始.md:9` and `words\原産.md:9`. Confidence: medium.**
- **Problem:** 原始 ("origin; primeval") and 原産 ("native origin") share the kanji 原, the type and the noun tag, and both titles contain "origin". Neither excludes the other. 天然 ("natural origin; nature") also contains "origin" and is not excluded by 原始.
- **Impact:** the author already excluded 元 and 出 from both new cards because their titles contain "origin", so this pair breaks that same pattern.
- **Fix:** add 原産 and 天然 to 原始's exclusions. Because exclusions are symmetric, one side is enough.

**F4. Minor · correctness (quiz) · `words\高級.md:9`. Confidence: medium-high.**
- **Problem:** 一流 ("first-rate; leading", tagged quality) is a near-synonym of "high-grade" and is not excluded; for example, 一流ホテル and 高級ホテル are near-equivalent.
- **Impact:** both cards already exclude 上等 and 優秀, so leaving 一流 out is an unexplained gap.
- **Fix:** add 一流.

**F5. Minor · correctness (kana) · `words\顕微鏡.md:20`. Confidence: medium-high.**
- **Problem:** the example writes 生物 but gives the kana as いきもの. The repo's `words\生物.md` card teaches せいぶつ, and `words\生き物.md` uses the spelling 生き物 for いきもの. The JMdict-based Jisho API lists 生物 only as せいぶつ or なまもの.
- **Impact:** learners may learn the wrong reading. In a microscope context the expected reading is せいぶつ.
- **Fix:** change the kana to せいぶつ, or change the spelling to 生き物.

**F6. Minor · correctness (identity) · `words\原産.md:36`. Confidence: medium.**
- **Problem:** the text `[故郷](故郷.md) (ふるさと)` links to a card whose taught reading is こきょう. In JMdict, こきょう is entry 2853884 and ふるさと is entry 1603050, a separate entry marked as usually written in kana.
- **Impact:** the link's reading contradicts the card it points to.
- **Fix:** label the link (こきょう), or keep ふるさと and remove the link.

## Optional
- **原始:** add an example that clearly shows the "origin/beginning" sense, and possibly mention 原始的.
- **原料 vs 材料:** note the general tendency, not a rule, that 原料 loses its original form while 材料 keeps it.
- **恋しい:** add a comparison with 寂しい.
- **公共:** link 個人 as a contrast.
- **厳重:** the "secure" in its title overlaps with 押さえる ("hold down; secure; grasp"), but the two are unlikely to be quizzed together.

## Limits
- I could not execute Git or check hashes. Receipts and mapping notes were assessed as author assertions, not independent proof.
- I did not consult the Nihon Kokugo Daijiten, so an archaic or formal "invite" use of 請う is possible. The naturalness of F2's example remains unverified.
- The Jisho JMdict version may differ from the pinned snapshot.
- I did not read all 307 comparison families. I did not run the quiz's automatic distractor selection, so how often these pairs actually appear together is unknown.
- I did not verify whether 工員 sounds dated.
- No example sentence has been checked by a native speaker.
