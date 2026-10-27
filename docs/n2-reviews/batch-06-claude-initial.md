**Snapshot:** da00a42474b6b3bf8cb6acacfc5d9d31c549aca4. I reviewed committed files only. I had file tools but no Git, so I could not check the commit hash or confirm a clean worktree; both rely on the author's confirmation.

**Scope:** Claude Opus 5.5 (`claude-opus-5.5`, Claude family), working sequentially with nothing delegated and no files edited.
- **Kanji cards:** I read all 15 in full: 委 季 孫 宇 宝 寺 封 専 将 尊 導 届 層 岩 岸.
- **Governing docs:** I read the three required documents (.github\copilot-instructions.md, .github\instructions\content-structure.instructions.md and docs\content-format.md:18-109).
- **Evidence:** I read all of `batch-06.json` (metadata, primaryWords, all 41 wordEvidence records and its stated limits) and `n2-source-snapshot.json`:1-75.
- **Related edits:** I checked the component-link passages in context in all 19 word articles: 一層:27, 宇宙:27, 封筒:25, 尊重:24, 寺:23, 孫:24, 尊敬:25, 宝石:25, 季節:23, 将来:24, 宝:24, 専攻:28, 委員:24, 岩:25, 岸:25, 届く:31, 届ける:25, 指導:27, 海岸:24.
- **Distractors:** I checked all 45 against the target meanings, plus the existing kanji they point to and the legacy two-choice card 山 [川, 出].
- **Omitted:**
  - stroke drawing paths (only file presence and `strokeCount` checked);
  - running the validator or manifest;
  - unchanged parts of the word articles;
  - the forbidden ledgers and reports.

**Verdicts:**

| Kanji | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 委 | CLEAN | CLEAN | CLEAN |
| 季 | CLEAN | CLEAN | CLEAN |
| 孫 | CLEAN | CLEAN | CLEAN |
| 宇 | CLEAN | CLEAN | CLEAN |
| 宝 | CLEAN | CLEAN | CLEAN |
| 寺 | CLEAN | CLEAN | CLEAN |
| 封 | CLEAN | CLEAN | CLEAN |
| 専 | CLEAN | CLEAN | CLEAN |
| 将 | CLEAN | CLEAN | CLEAN |
| 尊 | CLEAN | CLEAN | CLEAN |
| 導 | CLEAN | CLEAN | CLEAN |
| 届 | CLEAN | CLEAN | CLEAN |
| 層 | CLEAN | CLEAN | CLEAN |
| 岩 | CLEAN | CLEAN | CLEAN |
| 岸 | CLEAN | CLEAN | CLEAN |

**Findings:** I found no actionable defects. The checks behind this:
- **Metadata:** For all 15 cards, every on and kun reading, primary stroke count, radical with its number, and grade tag matches the batch-06 dictionary records. 封's grade 8 matches the source value "8". The `strokeCount` in each stroke file agrees too: 6 for 宇/寺, 8 for 委/季/宝/届/岩/岸, 9 for 封/専, 10 for 孫/将, 12 for 尊, 14 for 層 and 15 for 導.
- **Dictionary entries:** Every cited dictionary entry ID appears in batch-06.
- **Examples:** Each example uses the reading it is listed under, including written endings.
  - 婚姻届 drops the written け, and 届.md:30,43 explains this.
  - 将に is marked as usually written in kana (将.md:29,45).
- **Readings without examples:** 将.md:36 and 届.md:33 honestly say no example was found for some readings. External checks back this up: the dictionary (via Jisho) has no 将 spelling of ひきいる. A Japanese dictionary (Daijisen on Kotobank) confirms はた 【将／当】 as a non-jōyō adverb meaning "or", with no register label on sense 1.
- **Mnemonics:** All are labelled modern-shape mnemonics, and none of the cards' radicals uses a variant form.
- **Distractors:**
  - All 45 exist and none means the same as its target.
  - Every card has a linked word article.
  - The legacy two-choice card 山 [川, 出] has no overlap with 岩 or 岸.
- **Related edits:** All 19 passages are accurate and consistent with the new cards.

**Optional:** None of these blocks the batch.
- **O-01** 委.md:20,33 – The title says "committee" but only 委員 is shown; add 委員会 いいんかい.
- **O-02** 専.md:33 – Add 専門 せんもん or 専用 as more common words.
- **O-03** 将.md:46 – The phrase "replace 将来" is confusing, since はた has nothing to do with 将来. Optionally mark はた as literary (the modern form is はたまた) and add 将軍.
- **O-04** 寺.md:38 and words\寺.md:23 – The note mentions temple names but gives no example. Add one such as 清水寺 きよみずでら, which also shows the でら sound change.
- **O-05** 層.md – Add the social-class and building-storey senses (年齢層, 高層).
- **O-06** 岩.md:28 – 岩石 or 溶岩 would be a more common on-reading example than 岩塩.
- **O-07** 季.md:20 – The phrase "literal English sum of its parts" is opaque.
- **O-08** 届.md – Optionally show the standalone noun 届け.
- **O-09** – Title overlaps could matter only for cards that fall back to automatic distractors:
  - 封 "seal" with 判, and 封 "close" with 親/閉;
  - 委 "entrust" with 任;
  - 届 "reach" with 到/着/達;
  - 岩 "rock" with 石.

  The curated distractors on these cards avoid all of them.
- **O-10** – Add cross-links from 宝, 岸 and 寺 to the existing 石, 海 and 社 cards.

**Limits:**
- The snapshot and clean worktree could not be verified without Git.
- Stroke paths and the validator were not checked.
- batch-06 is selected evidence, not the whole dictionary, and Jisho may not match the pinned dictionary version.
- I did not verify the history behind the mnemonics (all are labelled as mnemonics).
- Legacy fallback was checked only for directly affected cards.
- This is not a native-speaker naturalness check.
