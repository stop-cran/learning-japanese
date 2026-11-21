# Blind review, batch 153 (initial reviewer)

Reviewer model: Claude, an Anthropic model. I worked alone and read-only.

## Snapshot

- Commit: cdab83b375e68d14d6d58a4866959611e949c41a (batch 153).
- Packet: C:\Users\romanko\n1-kanji-workspace\review-packets\batch-153-cdab83b3. packet-manifest.json sha256 is a6cf90a441161bb169e8ba911c593fb52ea20fc2506cbaa4f47ee7f29f0ac12c, as given in the mandate. I did not recompute it.
- Unit under review:
  - 15 new kanji cards: 醜 酌 酔 酢 釈 釣 鈴 銃 銭 鎖 鐘 鑑 附 陥 陰.
  - The 15 stroke files.
  - The remark-only edit on 属.
  - 20 one-line word-article diffs.

## Scope

Packet files I opened:

**Read in full**
- INSTRUCTIONS.md
- mechanical-checks.md
- All 15 cards in snapshot\kanji\. Some I viewed again in line ranges: 釈, 鎖, 陰, 附, 鑑, 銭, 鐘.
- All 21 files in diffs\: 1 kanji diff (属) and 20 word diffs.
- evidence\audits\kanji-remarks.json
- evidence\audits\word-remarks.json
- evidence\source-metadata.json
- All 15 evidence\public-source\weblio-*.txt (Digital Daijisen extracts)
- evidence\kanjipedia-outside-readings.json
- evidence\daijisen-heads.txt
- evidence\okurigana-scan.txt
- evidence\kanjivg-components.txt

**Read in part**
- evidence\kanjidic2-records.xml: Select-String and a Python parse of the 15 records.
- evidence\joyo-pages.md: lines 1-800, which cover the front matter and every page the cards cite.
- evidence\jmdict-digest.tsv: targeted lookups.
- evidence\jmdict-families.xml: a Python parse of every JMdict id cited in the 15 cards, plus the 1633480 鎖 entry.
- evidence\audits\reading-options.txt: lines 1-80, plus a grep for HIT lines.
- evidence\audits\reading-exposure.txt: a grep for "attested reading" and the summary lines, plus the 鎖 section.
- titles\kanji-titles.tsv: lookups of individual titles. These cover every exclusion and distractor title quoted on the cards, plus 隠, 酬, 鬼 and 汲, which have no card.
- repo\docs\content-format.md: lines 86-155 (the kanji-card and quiz-authoring rules), plus a heading grep.
- repo\kanji\: the first ~20 lines of 陽, 酒, 鳴, 銅, 跳, 付, 影, 鏡, 解 and 金.
- snapshot\strokes\*.json (all 15): I parsed only the keys, strokeCount, stroke-array length, viewBox and sourceRevision. I did not inspect the path data.

**Not opened**
- evidence\kanjivg-svgs.txt
- evidence\audits\quiz-safety.txt (I relied on the mechanical-checks excerpt)
- evidence\extra-readings.json and provenance.json
- evidence\app-code\
- titles\word-titles.tsv
- Any other repo file

**Public web pages fetched**
- Live Kanjipedia pages for 醜, 酌, 酔, 酢, 釈, 釣, 鎖, 陰, 附, 鑑, 銭 and 鐘.
- For 鈴, 銃 and 陥 I relied on the packet's Kanjipedia JSON and the Daijisen extracts.

## Verdicts

| Facet | Overall | Per-card differences |
| --- | --- | --- |
| 1. Correctness | CLEAN | None |
| 2. Scoped coverage | CLEAN | Optional coverage notes on 釈 (O3) and 鎖 (O4) |
| 3. Consistency and quiz safety | CLEAN | Optional over-breadth notes on the exclusions of 酢, 醜, 陥 and 鑑 (O5) |
| 4. Comprehensibility | CLEAN | Optional ordering note on 鐘 (O1) |

**Diffs (21): CLEAN.**
- Each of the 20 word diffs changes exactly one line. The change wraps the first mention of the new kanji in a link to `../kanji/<kanji>.md`, and the link targets the intended card.
- 附属 and 酌む also delete only the declared sentences, "附 has no card yet." and "There is no 酌 kanji card in the current collection." Both sentences are now false, because this batch adds both cards, and both passages still read naturally after the deletion.
- No diff touches a Dictionary: line. The three lint warnings (日陰, 醜い, 鑑賞) are on lines this batch does not touch, so they are pre-existing and out of scope.
- The 属 diff changes exactly one line and matches the old and new text declared in kanji-remarks.json. It links [附](附.md) with its exact title "affix; append", and the sentence still reads correctly.

**Stroke files (15): CLEAN.** Every file has:
- sourceRevision 70a0b7ae…, the pinned KanjiVG revision;
- strokeCount equal to the stroke-array length and to the card's `strokes` value;
- viewBox 0 0 109 109.

## Findings

No established defects were found.

What I verified as true, card by card and source by source:
- **Front matter**: grade, strokes, radical, the on and kun lists, and quizOnyomi and quizKunyomi all match source-metadata.json and KANJIDIC2.
- **Readings and Joyo**: every row and every Joyo claim matches joyo-pages.md, including examples, ⇔ pairings and old forms (錢 for 銭; 陰 ⇔ 影; 附 with only フ, 附属 and 寄附).
- **Digital Daijisen**: every claim matches the weblio extracts and daijisen-heads.txt, including:
  - the 呉音 and 漢音 labels (ブ for 附, シュ for 鐘, オン for 陰);
  - the numbered senses cited for exclusions (鐘 sense 3 時計。また、時刻。; 鑑 senses 1-4; 附 senses 1-4 and its [補説]; 陰 senses 1-8);
  - the name readings.
- **Kanjipedia**: every claim matches the live pages or the packet JSON, including:
  - the 外 readings (醜 にくむ, たぐい, しこ; 酢 ソ, すい; 釈 セキ, とく, ゆるす, とかす, おく; 銭 ゼン, すき; 鎖 とざす, さす; 鐘 シュ; 附 ブ, つく, つける; 陰 オン, アン, くらい, ひそか; 鑑 かがみ);
  - the senses quoted (釈 ①-⑧, 鎖 ①-②, 陰 ①-⑤ with 対 陽, 附 ①-③, 鑑 ①-②, 銭 ①-③ including すき（鋤）).
- **JMdict**: every cited entry id, gloss, sense number and marker matches jmdict-families.xml. Examples:
  - 2843271 しこ: derogatory and rare; sense 2 "unworthy; insignificant; humble".
  - 2864475 つつ: archaic.
  - 2859960 鎖す さす: formal or literary.
  - 1508540: 鎖す is a rarely used kanji form of 閉ざす.
  - 1495770 and 1495740: 附ける and 附く are rarely used kanji forms.
  - 1352040: 鐘楼 is read しょうろう and しゅろう.
  - 1324250: 釈然 is read しゃくぜん and せきぜん.
  - 2426060: 附子 is read ぶし and ぶす.
  - 1434040 sense 2: the 釣り change sense.
  - 2017840: 鏡 is a search-only form of 鑑 かがみ.
  - 1602700: 附属 is filed under 付属.

  An automated comparison of every double-quoted gloss found no gloss that is absent from its cited source. The only mismatches were attribution-format artefacts and card titles.
- **Mnemonics**: all 15 are labelled "Modern-shape mnemonic, not etymology" and make no historical claim. Every component, position and stroke statement matches kanjivg-components.txt. Examples:
  - 醜: 甶 contains 田; 儿 is marked original=八; 厶.
  - 勺 is 勹 + 丶.
  - 卆 is 九 over 十.
  - 釈: 釆 is 丿 over 米.
  - 令 is 人, 一 and マ.
  - 充 is 亠 + 允.
  - 戋 is 三 crossed by 戈.
  - 鎖: ⺌ over 貝, which is 目 over 八.
  - 童 is 立 over 里, with 日 inside the 里 group.
  - 付 is 亻 + 寸.
  - 陥: 𠂊 over 旧, which is 丨 + 日.
  - 陰: 今 (人, 一) over 云 (二 over 厶).
- **Reading audits (lead e)**: the accounting is consistent. The 8 latent collisions are 醜 にくむ and たぐい, 釈 しゃ (KANJIDIC2 name reading only) and おく, 鎖 さす, 附 ぶ, and 陰 おん and くらい. reading-exposure.txt marks each as "cannot be drawn" in the N1, All and Starter practice pools, with 0 production, 0 padded-session and 0 one-holder hits.
  - The two HIT labels in reading-options.txt (醜 たぐい by 双 類; 釈 おく by 億 屋 憶) are full-pool labels. They ignore slots already filled by the curated distractors.
  - I found no path by which an attested reading could be drawn as a wrong option in the app.
  - The okurigana-scan extras (え.い and え.う; ちゃん.ころ; さ.す; ふ.す and ふ.する; いん.うつ, いん.に and いん.にこもる) match okurigana-scan.txt.
- **Exclusions (lead a)**: each listed pair is anchored in a real sense that the card cites from KANJIDIC2, JMdict, Kanjipedia or Daijisen. The cards justify pairs individually; they are not transitive cliques.
  - Non-excluded pairs I judged safe as quiz answers in both directions: 酔/酒 ("drunk; intoxicated" against "alcohol; sake"), 銭/銅, 鈴/鳴, 陰/陽 (陽 "sunshine" is the opposite, not a synonym), and 釣/銭. For 釣/銭, the change sense of 釣り is a word-level sense; "angling; lure" and "coin" stay distinct.
- **In-batch pairs (lead b)**: all are distinguishable from the displayed titles. The 鈴/鐘 exclusion is justified: KANJIDIC2 gives 鐘 "bell", so "small bell" and "hanging bell; gong" would both be defensible for either kanji.
- **Distractors (lead c)**: all are plausible but defensibly wrong in both directions. Examples:
  - 絞 "strangle; wring; squeeze" is not pouring or ladling.
  - 税 is a levy, not a coin.
  - 縄 and 帯 are not chains.
  - 外 is not appending.
  - 陽 is the opposite of shade.
  - 跳 "hop; spring up" is not falling in.

  The easy sets for 醜 (短 赤 新), 釈 (書 聞 学) and 附 (外 出 間) are easy, but none is a defensible answer. That is acceptable. No distractor's curated reading gives away an answer.

## Optional

- **O1 (polish, facet 4; 鐘.md, Readings table).** The on-reading row シュ comes after the kun row かね, which splits the two on rows (ショウ, シュ). Moving シュ directly under ショウ would read more naturally. Confidence: high that this is cosmetic.
- **O2 (polish, facet 1; 醜.md, Notes).** The note says Joyo lists みにくい with 醜い. That is true, but the table also prints 醜さ. Adding it would make the note complete. Confidence: medium.
- **O3 (coverage, facet 2; 釈.md, Common words).** Only 解釈 is given.
  - 釈放 しゃくほう "release; liberation" is a Joyo example and very common, and the 放 exclusion depends on its sense.
  - 会釈 えしゃく "nod; bow" is common and is not mentioned.

  Adding one or both as plain (unlinked) examples would help learners. Confidence: medium. Scoped coverage does not strictly require them.
- **O4 (coverage, facet 2; 鎖.md, Notes).** JMdict 1633480 gives 鎖 read じょう, "lock, padlock". Daijisen's じょう headword 【錠／▽鎖】 supports it, and reading-exposure.txt lists it as an attested, unlisted reading with no drawable collision. The card cites the 錠前 sense but not this reading. A one-line note would close the gap. Confidence: medium.
- **O5 (quiz safety, facet 3; exclusion breadth).** These pairs are defensible but weakly anchored. They only shrink the distractor pool, so they are low impact:
  - 酢/賞: via Kanjipedia's むくいる, the cup-returning sense.
  - 醜/同, 醜/似, 醜/等 and 醜/匹: via Kanjipedia's outside-the-table sense ③.
  - 陥/滑: via KANJIDIC2 "slide into".
  - 鑑's 25-card list, for example 鑑/本, 鑑/冊 and 鑑/巻 via Daijisen's book sense.

  Removing any of them is a matter of judgement, not a correction.
- **O6 (note; 鎖 audit).** The audit did not add 1633480 じょう as an extra reading. It is harmless at this snapshot: quizOnyomi is [], and the curated distractors 縄 針 帯 fill all slots. Adding じょう would keep the audit honest if quizOnyomi ever changes.

## Limits

- The Android JVM content tests and the Kotlin cross-check of the reading audit were not run at this snapshot. This is known and is not reported.
- Pinned dictionary data (JMdict and KANJIDIC2 2026-11-02, the Daijisen extracts) may differ from the live sites. I checked live Kanjipedia pages for 12 of the 15 kanji; for 鈴, 銃 and 陥 I relied on the packet JSON and the Daijisen extracts.
- I did not open quiz-safety.txt in full. I relied on the mechanical-checks summary and on reading-options.txt and reading-exposure.txt.
- I did not open evidence\kanjivg-svgs.txt. I checked the mnemonics against kanjivg-components.txt only.
- I did not open the app code. I took the quiz semantics from content-format.md and the audit texts.
- Repo kanji cards other than the ten listed in Scope were checked only through titles\kanji-titles.tsv.
- localZipBytes drift is not a defect (per the mandate).
- Tool calls: I am not aware of issuing more than one tool call in any response.
- Assumption: "exact title" means the title string in titles\kanji-titles.tsv at this snapshot.
