## Snapshot
**4fa37301b6863b299555ce1e9bc3e4855e0167d9** (parent 84b5fd4ad97a514701bc1546fdd23ef34c81259d), as recorded in the frozen receipt, which reports clean committed content. This review covers committed content only.

I had file tools only and no Git. I could not check the commit, its parent or file hashes, and I read the working-tree files on the assumption that they match the receipt.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family). I worked alone and sequentially, delegated nothing and edited no files.
- **New articles (19, each read in full):** 釜, 紙屑, 神様, 剃刀, ガム, 貨物, かゆい, 歌謡, 殻, カラー, からかう, 空っぽ, かるた, カロリー, かわいがる, 乾かす, 渇く, 為替, 瓦.
- **Related edits (8):** I read `batch-17-related.patch` and checked the changed passages in context in kanji\乾.md, kanji\替.md, words\乾く.md, kanji\貨.md, words\干す.md, words\色.md, words\いじめる.md and words\枯れる.md.
- **Reuse claim (枯れる):** I checked only the source spelling, reading and plant sense against the article, plus the change that adds `jlpt: 2`. This is not a full recertification of the article.
- **Mappings:** N2:322–N2:341 in docs\n2-vocabulary-sources.tsv.
- **Evidence read in batch-17.json:** the rows, all 20 principal families, the inspection receipts, the quiz declarations and their rationale, and these comparison families: 1277350, 2853151, 2853152 and the first sense of 1193460.
- **Other checks:** title and exclusion greps across words\, link-target globs, kanji card checks, and one public page (Weblio's カラー entry).
- **Not reviewed:**
  - Most of the 141 comparison families, including 1054570 and 1209920.
  - Unchanged teaching in the related files and 枯れる.
  - Every forbidden file listed in the brief.

## Verdicts

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 釜 | CLEAN | CLEAN | CLEAN |
| 紙屑 | CLEAN | CLEAN | CLEAN |
| 神様 | CLEAN | CLEAN | CLEAN |
| 剃刀 | CLEAN | CLEAN | CLEAN |
| ガム | CLEAN | CLEAN | CLEAN |
| 貨物 | CLEAN | CLEAN | CLEAN |
| かゆい | CLEAN | CLEAN | NEEDS FIX (B17-04) |
| 歌謡 | CLEAN | CLEAN | CLEAN |
| 殻 | CLEAN | CLEAN | CLEAN |
| カラー | CLEAN | CLEAN | NEEDS FIX (B17-01) |
| からかう | CLEAN | CLEAN | NEEDS FIX (B17-03) |
| 空っぽ | CLEAN | CLEAN | CLEAN |
| かるた | CLEAN | CLEAN | CLEAN |
| カロリー | CLEAN | CLEAN | CLEAN |
| かわいがる | CLEAN | CLEAN | CLEAN |
| 乾かす | CLEAN | CLEAN | CLEAN |
| 渇く | CLEAN | CLEAN | NEEDS FIX (B17-02, quiz) |
| 為替 | CLEAN | CLEAN | CLEAN |
| 瓦 | CLEAN | CLEAN | CLEAN |

**Related changes:** all eight are CLEAN on all three facets, within the changed passages only.
- **kanji\乾.md:** the three 乾かす links are correct. The thirst qualification is accurate: family 1277350 lists 喉が乾く with no flag and のどが乾く as search-only.
- **kanji\替.md:** 為替 is added at its real reading かわせ, with a correct whole-word-reading warning.
- **kanji\貨.md:** the 貨物 link is added at かもつ.
- **words\乾く.md:** the qualified advice and the 髪が乾く / 髪を乾かす contrast are both accurate and natural.
- **words\干す.md, words\色.md, words\いじめる.md:** the link wording is accurate.
- **words\枯れる.md:** only the level was added. The article had no earlier, easier level to preserve.

**Reuse (枯れる):** CLEAN on all three facets. It teaches 枯れる (かれる) with the plant-withering sense (title "wither (plants)"), and the added N2 level comes from the source.

**Mappings:** all 20 rows map the exact source spelling or kana form, reading and selected senses to an article that teaches them, and none conflicts with the principal family. Kanji metadata is complete. The cards that exist for N2 kanji (貨, 乾, 替, 枯) have reciprocal links at the actual readings. No new kanji files were created.

| Mapping | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| N2:322–327, 329–330, 333–338, 340–341 | CLEAN | CLEAN | CLEAN |
| N2:328 (かゆい) | CLEAN | CLEAN | NEEDS FIX: the note overstates "recognizes the usually-kana flag" (B17-04) |
| N2:331 (カラー) | CLEAN: collar is correctly attributed to entry 2853151 | CLEAN | NEEDS FIX (B17-01) |
| N2:332 (からかう) | CLEAN | CLEAN | NEEDS FIX: the "explicit を" claim is not shown with a person (B17-03) |
| N2:339 (渇く) | CLEAN | CLEAN | CLEAN (the quiz problem is in the article, not the mapping) |

## Findings
- **B17-01. Minor. Comprehensibility. words\カラー.md:22**
  - **Claim:** The article gives シャツのカラー as "a shirt's collar" and tells learners not to read it as the shirt's color.
  - **Impact:** Out of context the phrase is ambiguous, and in shopping or product text it often means color. The repo's own words\色.md:28 says カラー "color" is used especially in product descriptions. Learners may misread color listings as collars.
  - **Remedy:** Say that context decides. Use fashion compounds for collar, such as ボタンダウンカラー or ワイドカラー, and give 襟 (えり) as the everyday word for a collar.
  - **Evidence:** JMdict 2853151 has the single gloss "collar" (spec1). Weblio's Wikipedia-derived entry maps the original sense of collar to 襟 and lists collar compounds (襟カラー, ブルーカラー, エリザベスカラー).
  - **Confidence:** Medium.
- **B17-02. Minor. Comprehensibility (quiz). words\渇く.md:9, 21; words\飢える.md:4, 9, 21; words\憧れる.md:4, 9**
  - **Claim:** 渇く ("be thirsty; crave") has no quiz exclusion against 飢える ("starve; hunger for").
  - **Impact:** 渇く's own example translates 愛に渇いた人 as "a person starved for affection", and 飢える teaches the parallel 愛情に飢えています, "starved of affection". Either title is defensible for the other prompt, so the quiz can mark a correct answer wrong.
  - **Weaker case:** "yearn for" (憧れる) also overlaps "crave". The author already excluded 望む ("hope for; desire") for similar desire labels.
  - **Remedy:** Add 飢える, and optionally 憧れる, to 渇く's `quiz_exclusions`.
  - **Evidence:** In batch-17.json, neither 飢える nor 憧れる appears in the evidence or quiz declarations.
  - **Confidence:** Medium-high for 飢える; low-medium for 憧れる.
- **B17-03. Minor. Comprehensibility. words\からかう.md:16, 18; mapping N2:332**
  - **Claim:** Line 16 says "the person targeted takes を", but the only を example is 私の新しい髪形をからかいました, where the hairstyle takes を.
  - **Impact:** 人をからかう is never shown. Learners may be unsure which noun takes を, or may produce something like 私を髪形をからかう.
  - **Remedy:** Add an example such as 友達をからかう, or say that the person or the trait being mocked takes を.
  - **Confidence:** Medium-high.
- **B17-04. Minor. Comprehensibility. words\かゆい.md:16, 25; mapping N2:328**
  - **Claim:** Line 25 says "Do not add a kanji reading to the kana spelling when speaking." The sentence is unclear and gives no usable instruction. Line 16 says only that the kana form is sufficient. It never says the word is usually written in kana, although the N2:328 note claims the article covers the usually-kana flag.
  - **Remedy:** Replace line 25 with "痒い is read かゆい; the word is usually written in kana."
  - **Evidence:** JMdict 1569570 carries the usually-kana flag.
  - **Confidence:** High for the unclear wording; medium for the overstated note.

## Optional
- 殻: mention 貝殻 (かいがら), "seashell", and the から→がら change in 抜け殻 and 吸い殻.
- からかう: mention the passive からかわれる.
- 剃刀: one kanji-spelling example could help learners recognize the written form.
- 為替: the 案 exclusion is harmless redundancy, since the title no longer contains "draft".

## Limits
- No Git: the commit, its parent and the file hashes were not checked independently.
- Naturalness judgments are my own, not native-speaker certification. The B17-01 usage claim is partly unverified because the Kotobank カラー lookup returned a 404.
- I did not read most comparison families, including 1054570, 1209920 and the rest of 1193460. Collisions outside the titles I grepped are possible.
- Receipts, mapping notes and quiz rationale were treated as author assertions.
- I relied on my own knowledge, without fetching a source, that 為替 is in the Jōyō kanji list's appendix of special readings (付表).
- Unchanged teaching in 枯れる and the related files was not recertified.
