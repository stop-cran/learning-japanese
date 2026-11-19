# Batch 144 initial blind review (Claude)

## Snapshot

- Commit: b073abd8f2ab578f29cf2b5e25f36e02fc1aab58 (batch 144)
- Packet: C:\Users\romanko\n1-kanji-workspace\review-packets\batch-144-b073abd8 (packet-manifest.json sha256 4f9ef67815b2befda589d5202a86046ee89eb69fdc5e647f1a2fd1b65af62a52)
- Reviewer: Claude, Anthropic model family. I am the first of two blind reviewers. I worked alone and read-only, and the only file I wrote is this report.

## Scope

Unit reviewed:
- the 15 new kanji cards 棋 棚 検 概 欄 歓 殊 殻 汁 沖 泡 泣 淡 渇 渋;
- their 15 stroke files;
- the 18 modified word articles;
- the changed bullet of kanji\討.md;
- all 19 diffs.

Packet files I opened:

| File | Extent |
|---|---|
| INSTRUCTIONS.md | full |
| mechanical-checks.md | full |
| snapshot\kanji\{棋,棚,検,概,欄,歓,殊,殻,汁,沖,泡,泣,淡,渇,渋}.md | full (each) |
| snapshot\kanji\討.md | part (front matter lines 1–17 and Notes lines 85–100) |
| snapshot\strokes\*.json (15 files) | full: parsed strokeCount, ids and point counts |
| snapshot\words\特殊.md | full |
| diffs\ (19 diffs) | full (changed lines plus context) |
| evidence\source-metadata.json | part (entries for the 15 kanji) |
| evidence\kanjidic2-records.xml | part (records for the 15 kanji) |
| evidence\jmdict-families.xml | part (targeted entries, by ent_seq) |
| evidence\jmdict-digest.tsv | part (targeted grep lines) |
| evidence\joyo-pages.md | part (rows for the 15 kanji and the bracketed forms) |
| evidence\kanjipedia-outside-readings.json | part (entries for the 15 kanji) |
| evidence\daijisen-heads.txt | full |
| evidence\public-source\weblio-*.txt for the 15 kanji | full (棚's extract had no usable content, so I used the live page) |
| evidence\audits\quiz-safety.txt | full |
| evidence\audits\reading-options.txt | full |
| evidence\audits\reading-exposure.txt | part (head, the per-card 殊, 殻 and 沖 sections at lines 104–175, the "attested reading … offered by" lines, the tail and its count line) |
| evidence\audits\okurigana-scan.txt | full |
| evidence\audits\kanji-remarks.json | full |
| evidence\audits\word-remarks.json | full |
| titles\kanji-titles.tsv | part (targeted title lookups) |
| titles\word-titles.tsv | part (header and the linked example words) |
| repo\docs\content-format.md | part (lines 86–154: Kanji card, Quiz authoring, Curated reading questions) |
| packet root, evidence\, evidence\public-source\, diffs\ | non-recursive listings only |

Not opened: evidence\app-code\, rubric\ and any other repo\ files.

Public web: I fetched the live Weblio page for 棚. A Jisho query for 陸棚 returned only page chrome, so it gave no evidence.

## Verdicts

| Facet | Overall | Cards that differ |
|---|---|---|
| 1 Correctness | **Minor issues** | 棚 (C1, C2), 歓 (C3), 淡 (C4), 欄 (C7), 討 bullet (C5). The other cards are clean. |
| 2 Scoped coverage | **Clean** | Optional gaps only: 歓 合歓, 渇 渇する, 殻 かい, 泡 あぶく. |
| 3 Consistency and quiz safety | **Minor issues** | 殻 (C6 distractors); 棋 and 沖 (C8 on/kun typing). The other cards are clean. Exclusions are real direct pairs, with a few weak but harmless ones (Optional). |
| 4 Comprehensibility | **Minor issues** | 討 bullet (C5). Small polish items are listed under Optional. |

Per-card summary:

| Card | Status |
|---|---|
| 棋 | Clean except C8. The accounts of 将棋 and 碁 are correct, and Daijisen ご【碁／×棊／▽棋】 matches the card. The title "shogi; go; go stone" is safe because 碁 is excluded. The distractors 模 横 構 are fine. |
| 棚 | C1 and C2. Otherwise correct: たな; 戸棚 / 本棚 / 棚; the Joyo row たな with 棚, 戸棚 and 大陸棚; 大陸棚 and 葡萄棚 described correctly. |
| 検 | Clean, including 検査, 検討, 検察庁, 検非違使 and 検する. The 18 exclusions are real (剖 by 剖検, 偵 by 検 and 偵察, 討 by 検討). 点 and 剖 are weak but harmless. |
| 概 | Clean. 概論, 概して and 概ね are correct. The "bearing" sense versus 穂 "grain-bearing head" is low risk. |
| 欄 | C7. Otherwise correct: らん, てすり marked source-only, the 手摺り/手すり spelling. |
| 歓 | C3. Otherwise correct. |
| 殊 | Clean. 特殊, 殊に, 殊な けな (archaic, JMdict 2229800) and the 特殊 remark edit are all correct. |
| 殻 | C6. Readings and words are correct: から; がら (JMdict 2101970); 抜け殻; 殻に閉じこもる; コク in 船殻 (JMdict 2831954); バイ marked source-only. |
| 汁 | Clean. A small attribution nit is listed under Optional. |
| 沖 | C8. The rest is correct: おき, 沖積層, わく marked source-only, and the Joyo row with 沖する under チュウ. |
| 泡 | Clean. 泡, 発泡 (ぽう), 泡立つ, 水泡に帰す and 淡雪/泡雪 (JMdict 1418470) are correct. |
| 泣 | Clean. |
| 淡 | C4. Otherwise correct: 淡水, 淡水魚, 淡い. |
| 渇 | Clean. 渇く and 消渇 しょうかち are correct. |
| 渋 | Clean. 渋滞, 渋い and 渋る are correct; 渋 しぶ means kakishibu; 渋さ has no JMdict entry; 滞 is plain text. |

Diffs:
- All 18 word diffs are single-line link wraps to the correct `../kanji/X.md`, and each article gains exactly one link.
- The 特殊 diff also deletes exactly the declared sentence, and the passage still reads well.
- The 討 diff matches kanji-remarks.json, and its 検 link is correct. The wording is covered by C5.

Stroke files: all 15 come from KanjiVG revision 70a0b7ae. In each file strokeCount equals the number of strokes and the front-matter strokes value, the ids are sequential, and every stroke has 16 points.

## Findings

### C1: 棚 claims 氷棚 is the only JMdict ほう word, but 陸棚 りくほう exists
- **Severity:** minor
- **Facet:** 1
- **Location:** snapshot\kanji\棚.md:33 (ホウ row)
- **Claim and impact:** The row says "the only JMdict word found with ほう is 氷棚 ひょうほう". This is false. JMdict 1551120 陸棚 has the readings りくだな and りくほう ("continental shelf"), and the digest lists it beside 2831996 氷棚. Learners get a wrong picture of where ホウ appears, and the claim that ホウ gives "no ordinary example" is weakened: 陸棚 りくほう is a technical but real term.
- **Remedy:** Name both words, e.g. "JMdict has ほう only in technical terms: 陸棚 りくほう (beside りくだな) 'continental shelf' and 氷棚 ひょうほう 'ice shelf'".
- **Evidence:** evidence\jmdict-families.xml, entry 1551120; evidence\jmdict-digest.tsv, rows `棚 1551120 陸棚 りくだな りくほう` and `棚 2831996 氷棚 ひょうほう`.
- **Confidence:** high

### C2: 棚 misreads the Daijisen ▽ mark
- **Severity:** minor
- **Facet:** 1
- **Location:** snapshot\kanji\棚.md:25
- **Claim and impact:** The card says Daijisen's たな【▽店／棚】 is written "with 棚 as a non-standard form". In Daijisen the ▽ marks a character used for a reading outside the Joyo table. Here the mark sits on 店, not on 棚. 棚 is the standard Joyo spelling of たな, as the Joyo row cited on the same card shows. The claim is reversed.
- **Remedy:** Say that the headword たな【▽店／棚】 marks 店 (store or shop sense) as the out-of-table spelling and 棚 as standard, or drop the non-standard remark.
- **Evidence:** evidence\daijisen-heads.txt, lines 5–7 (`D たな【 ▽ 店／棚】`, `D たな【棚】`); evidence\joyo-pages.md, row for 棚 (たな: 棚, 戸棚, 大陸棚).
- **Confidence:** high

### C3: 歓 Notes say 権 has a similar-looking left part
- **Severity:** minor
- **Facet:** 1
- **Location:** snapshot\kanji\歓.md, Notes (distractor bullet for 権)
- **Claim and impact:** 権's left part is 木, which looks nothing like 歓's left part. The similarity is between 権's right part (the 隹-type element) and 歓's left part. As written, the component statement is false, and a learner looking at the shapes will be confused.
- **Remedy:** Say instead that 権 "shares the same element, on the right in 権 and on the left in 歓".
- **Evidence:** the glyph shapes of 権 (木 plus that element) and 歓 (that element plus 欠). The card's own mnemonic places 欠 on the right of 歓.
- **Confidence:** high

### C4: 淡 calls あわ a name-only reading in Daijisen
- **Severity:** minor
- **Facet:** 1
- **Location:** snapshot\kanji\淡.md, Meaning/Readings paragraph ("the name-only readings あわ, あわし and あわじ")
- **Claim and impact:** In Daijisen's character entry for 淡, あわ is given as a regular kun reading with the example 淡雪, not only as a name reading. This matches JMdict 1418470 淡雪 あわゆき. Calling あわ name-only misdescribes the source, and it contradicts the card's own mention of 淡雪.
- **Remedy:** Separate the two: あわ in 淡雪 is a regular reading, and あわし and あわじ (as in 淡路) are name readings.
- **Evidence:** evidence\public-source\weblio-淡.txt (Daijisen character entry: 〈あわ〉「淡雪」 apart from the 名のり list); evidence\jmdict-families.xml, entry 1418470.
- **Confidence:** medium-high

### C5: The rewritten 討 bullet keeps a sentence that no longer has a referent
- **Severity:** minor
- **Facet:** 4 (and 1)
- **Location:** snapshot\kanji\討.md:96–97; diffs\ for kanji\討.md
- **Claim and impact:** The new bullet reads "In [検討](…), [検](…) supplies ケン. This does not change the complete word's reading." Before the edit, "This" referred to 検 having no card. With that clause removed, the second sentence says that supplying ケン does not change the word's reading. That is vacuous, and a learner may read it as a hint that something unusual happens. The declared intent, kept in kanji-remarks.json, is preserved literally but no longer makes sense.
- **Remedy:** Delete the second sentence, or reword the bullet as "In 検討 けんとう, 検 supplies ケン and 討 supplies トウ."
- **Evidence:** the 討 diff; evidence\audits\kanji-remarks.json.
- **Confidence:** high

### C6: The 殻 curated distractors 休 本 木 are not plausible wrong answers
- **Severity:** minor
- **Facet:** 3
- **Location:** snapshot\kanji\殻.md, front matter `distractors: [休, 本, 木]` and the Notes bullet that explains them
- **Claim and impact:** The three are Starter N5 kanji ("rest", "book", "tree"). They share neither the shape (殳, 士, 几) nor the meaning field (shell, husk, covering) of 殻. content-format.md asks for "plausible wrong options". On an N1 card, an N4 learner can eliminate them by recognition alone, so the meaning question tests almost nothing. They do not cause any error; the problem is quiz quality. The choice appears to serve reading safety: they keep 貝 (かい) out of reading options, as the audit notes. That goal does not require implausible meaning distractors, because reading options use the quiz lists.
- **Remedy:** Use visually or semantically close kanji that hold no から, がら or かい reading, e.g. 殺, 穀 (if it has a card) or 設 for shape, or 皮-adjacent cards not already excluded. Then rerun reading-options to confirm that かい stays undrawable, or accept and document the latent かい collision.
- **Evidence:** the front matter of 殻; content-format.md:97–117; evidence\audits\reading-options.txt (殻 HIT かい by 貝); evidence\audits\reading-exposure.txt:127–140.
- **Confidence:** medium (this is a judgment of plausibility)

### C7: 欄 misquotes the おばしま gloss and is inconsistent about the bracketed form
- **Severity:** minor
- **Facet:** 1
- **Location:** snapshot\kanji\欄.md, the Readings/Notes text on てすり and おばしま, and the Joyo bracketed-form sentence
- **Claim and impact:**
  1. The card double-quotes JMdict 2844081 おばしま as "archaic handrail; …". "archaic" is a misc tag in that entry, not part of the gloss, so the quoted gloss is not real.
  2. The card does not say that Daijisen's character entry gives ［訓］おばしま, which is the source behind the card's own mention.
  3. The bracketed Joyo form is called "a compatibility form". The other cards in this batch (検, 概, 殻, 渇, 渋) call the same kind of form the "older form" that the table prints in brackets. The codepoint used (U+F91D) is a CJK compatibility ideograph, but the table means the traditional character 欄, so the wording is inconsistent and slightly misleading.
- **Remedy:** Quote the bare gloss and say "(marked archaic)". Optionally add Daijisen ［訓］おばしま. Use the batch's "older form" wording.
- **Evidence:** evidence\jmdict-families.xml, entry 2844081; evidence\public-source\weblio-欄.txt; evidence\joyo-pages.md, row for 欄.
- **Confidence:** medium-high

### C8: 棋 ご and 沖 ちゅう.する are typed "kun" without qualification
- **Severity:** minor
- **Facet:** 1 and 3
- **Location:** snapshot\kanji\棋.md (ご row) and snapshot\kanji\沖.md (ちゅう.する row)
- **Claim and impact:** Both are in the kunyomi lists because KANJIDIC2 puts them there, and the metadata lists rightly follow the source. However, ご for 棋 (from 碁 and 棊) is a Sino-Japanese reading; Kanjipedia gives ゴ as on. 沖する is a 漢語 verb, and the Joyo table puts 沖する under チュウ. A Readings table that labels them "kun" teaches a false category to beginners. Neither reading is quizzed, so there is no quiz risk.
- **Remedy:** Keep the metadata, and mark the table cells, e.g. "kun in KANJIDIC2; really a Sino-Japanese (on) reading", with one sentence of explanation.
- **Evidence:** evidence\kanjidic2-records.xml (棋, 沖); evidence\kanjipedia-outside-readings.json (棋); evidence\joyo-pages.md, row for 沖 (チュウ: 沖積層, 沖する).
- **Confidence:** medium

No other established defects. These leads were checked and found sound:
- (a)–(r) in the brief.
- The reading-collision accounting. The 6 latent collisions (欄 わく, 歓 ぶ, 殊 け, 殻 かい, 沖 とぶ, 沖 むなしい) are correctly counted and none is drawable.
- The 殻 かい HIT in reading-options cannot be drawn, because 休, 本 and 木 are Starter cards present in every pool and fill every slot. The "6 wrong options seen" figure is 3 from 休, 1 from 本 and 2 from 木.
- quiz-safety reports 0 errors. 概, 沖, 淡 and 渇 running 2/3 in reading prompts is explained by their distractors' reading lists (既 has no usable on reading, 汽 has no kun reading, 談 だん is skipped as excluded, 掲 has no usable kun reading).

## Optional

These are polish items, not defects.
- 棚:
  - The Daijisen たな sense list is selective; the page has more senses.
  - The 明 distractor note ("built from 日 and 月 and is not the same part") is confusing, because the card compares 棚's 朋 = 月+月. Say that 明 shares 月 but not the doubled 月.
  - The 店 sentence ("a different word, so it is never an option") is a loose non sequitur.
- 検: the exclusions 点 and 剖 are weak, though defensible through 点検 and 剖検. They are harmless.
- 概:
  - "bearing" (the sense of 気概 or general demeanour) needs a few words for an N5–N4 reader.
  - The overlap with 穂 "grain-bearing head" is low risk because the senses differ visibly.
- 欄:
  - 井, 額, 件 and 条 are weak exclusions. They are harmless because exclusions only remove choices.
  - "form field" against 体, 形 and 状 ("form") is low risk, because the 欄 title clearly reads as a field on a form.
- 歓: mentioning 合歓 (ねむ, as in 合歓木; ごうかん) as a curiosity would explain the meta scan hit.
- 淡 and 渋: "One example of each:" is followed by bullets that hold two or three examples. Adjust the wording.
- 渇 and 渋: the mnemonics barely describe the right-hand part (曷-type / 歩-type shapes). The modern-shape label is present.
- 渇: could mention 渇する / 渇す (かっする, "to be thirsty, to run dry") and the noun 渇 かつ.
- 泡: could note that Daijisen's character entry also gives あぶく.
- 殻: the archaic かい reading (JMdict 2647520) is not discussed. Leaving it out is acceptable.
- 汁: the plain gloss "juice" is attributed to Daijisen's character entry, but that entry glosses in Japanese (しる). The English matches KANJIDIC2, so adjust the attribution.
- Title overlaps I judged non-defensible as wrong answers, so no exclusion is needed:
  - 淡 "plain" against 原 "original; plain"
  - 沖 "rise high" against 高
  - 沖 "open sea" against 剖, 爆, 野 and 開 (whose "open" is a verb or a field)
  - the kakishibu sense shared by 汁 and 渋 (neither title displays it)

## Limits

- I am Claude (Anthropic). I followed the one-call-per-response rule throughout and did not notice any parallel calls, but I cannot fully rule out an early slip.
- Public-web verification was thin. I fetched the live Weblio page for 棚; a Jisho check of 陸棚 returned only page chrome. My other dictionary checks relied on the packet's Weblio/Daijisen extracts and the JMdict and KANJIDIC2 evidence, not on independent live pages for every word. I do not claim independent live verification beyond that.
- I did not open evidence\app-code\. I relied on content-format.md, the audits and mechanical-checks.md for quiz behaviour, including symmetric, non-transitive exclusions, which content-format.md confirms.
- I read only part of 討.md (its front matter and the edited Notes region). The rest of that card is outside scope.
- Assumptions:
  - Undoubled-quoted table glosses need not be exact JMdict strings.
  - Android JVM tests, the Kotlin cross-check and localZipBytes variance are known packet limits, not defects.
  - The three lint warnings (戸棚, 淡水, 特殊) are context only. I found no real defect in them; in 特殊 the entry id sits on the next line.
- Line numbers are given where I recorded them (棚 25/33/51, 討 96–97, reading-exposure 127–140). Otherwise I name the section.
