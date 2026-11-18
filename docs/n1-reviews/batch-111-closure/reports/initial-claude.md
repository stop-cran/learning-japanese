# Review of batch 111: first blind reviewer

Reviewer model: Claude Opus 5.5 (model ID: claude-opus-5.5).

## Snapshot

- Commit: 3b30803e33438dab7a1071aea34ceb7764189c1f (batch 111).
- New kanji cards: 修 句 房 授 敷 旬 標 独 率 節 義 製 評 養 鏡.
- Also in scope:
  - the 15 files in snapshot\strokes\;
  - the 60 modified word articles in snapshot\words\;
  - 62 one-line diffs: the 60 word articles plus kanji\価.md and kanji\暖.md.

## Scope

Packet root: `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-111-3b30803e`.

**Read in full:**
- INSTRUCTIONS.md
- mechanical-checks.md
- evidence\source-metadata.json
- all 15 snapshot\kanji cards (修 句 房 授 敷 旬 標 独 率 節 義 製 評 養 鏡)
- all 15 snapshot\strokes JSON files. I parsed them with a script that checked stroke count, the kanji field, strokeCount and source. I did not read them by eye.
- all 62 files in diffs\:
  - a script classified every diff by stripping the added link and comparing the − and + lines;
  - I read three by eye: kanji__価.md.diff, kanji__暖.md.diff and words__句読点.md.diff.
- snapshot\words\修理.md

**Read in part:**
- rubric\copilot-instructions.md, lines 1–400.
- repo\docs\content-format.md, lines 71–190.
- evidence\kanjidic2-records.xml: the records of the 15 kanji, found by targeted search.
- evidence\jmdict-families.xml: targeted `<ent_seq>` and headword searches for later senses and flags. The entries checked include 税率, 軽率/軽卒, 節 (ふし and ノット), お節, 節会, 削り節, 制作, 養う, 明鏡 1674690, 眼鏡 1577670 and 2862467, 独楽, 独逸, 独活 and 独鈷.
- evidence\jmdict-digest.tsv: the rows for the example words of all 15 cards.
- evidence\public-source\: the Daijisen (Weblio) character extracts for all 15 kanji.
- snapshot\words\准教授.md, lines 24–36.
- The front matter of these repo\kanji cards: 布, 将, 卒, 律, 栗, 比, 割 and 令. My notes from the earlier part of the session are the source for this list.
- titles\kanji-titles.tsv: targeted lookups and a script lookup of about 120 titles quoted in the Notes.
- titles\word-titles.tsv: a targeted lookup of 29 word titles.
- On every word article I ran a script that checks where its link sits within the section "How the kanji combine".

**Listed (non-recursive only):** the packet top level, snapshot, snapshot\kanji, evidence, evidence\public-source and rubric.

Supplement root: `C:\Users\stop-\n1-kanji-workspace\review-packets\supplement-111`.

- Read in full: README.md and reading-options.txt (read in sections that cover the whole file).
- Read in part:
  - joyo\: the pages the cards cite, which are p34 (義), p39 (鏡), p41 (句), p72 (授), p73 (修), p76 (旬), p91 (製), p93 (節), p101 (率), p120 (独), p132 (標, 評), p134 (敷), p142 (房) and p153 (養);
  - reading-exposure.txt: grep of the summary lines and all lines on attested readings and latent collisions.
- Listed: the supplement top level and joyo\.

**Not opened:** any path outside the packet, the supplement and this report file.

## Verdicts

| Facet | Overall | Cards that differ |
|---|---|---|
| 1. Correctness | MINOR | 敷 (F1); 鏡 (F2). All other cards are CLEAN. |
| 2. Scoped coverage | CLEAN | none |
| 3. Consistency and quiz safety | CLEAN, with one note | 鏡: the "lens" part of the title (F2) affects how the quiz answer reads. |
| 4. Comprehensibility | CLEAN, with one note | 敷: the explanation of the dash (F1) can mislead. |

**Strokes (all 15 files): CLEAN.**
- Every file has a strokes array whose length equals the strokes value in the card's front matter and the file's strokeCount field.
- The kanji field matches the file name.
- The source is KanjiVG (CC BY-SA 3.0).

**Diffs (62): CLEAN.**
- The 59 word diffs other than 句読点 are pure link-wraps: once the new link is stripped, the + line equals the − line.
- Every diff changes exactly one line and adds exactly one link, to the intended batch kanji, at `../kanji/X.md`. Every target card exists.
- In 59 of the 60 word articles the link sits on the first mention of the kanji in "How the kanji combine". The exception is 准教授.md:
  - Line 29 mentions 授 first, inside the existing word link `[教授](教授.md)`, which cannot be nested.
  - The link therefore goes on the next separate mention, at line 31 (`[授](../kanji/授.md) contributes imparting knowledge`).
  - That placement is correct.
- kanji\価.md: "評 in 評価 does not have a kanji card yet" becomes a list item, `[評](評.md), "appraise; reputation," in 評価`.
  - The quoted title matches kanji-titles.tsv exactly.
  - The list's connectives change correctly: "物価 and … 高価" becomes "物価, … 高価 and … 評価".
  - The sentence reads correctly.
- kanji\暖.md: "the 房 in 暖房, which does not have a kanji card here" becomes `[房](房.md), "room; tassel; bunch," in 暖房`.
  - The title is exact, and the sentence reads correctly.
- words\句読点.md: the first 句 becomes `[句](../kanji/句.md)`, and the sentence "There is no 句 card currently." is dropped.
  - Nothing else changes, and the passage reads correctly.

The 13 lint warnings about "Dictionary:" lines in modified word articles are context only. No diff touches those lines, and I found no defect to report about them.

## Findings

### F1. 敷: 敷地 is filed under the suffix reading -し.き, and the card defines the dash wrongly
- **Severity:** Low.
- **Facets:** 1 (correctness), with an effect on 4 (comprehensibility).
- **Location:** snapshot\kanji\敷.md, line 35 (Readings row `-し.き`) and line 37 (the sentence "The dash in -し.き marks a bound form, one that appears inside compounds").
- **Claim:**
  - The -し.き row lists 敷地 しきち next to 座敷 and 風呂敷.
  - The paragraph says the leading dash marks "a bound form, one that appears inside compounds".
- **Problem:**
  - In KANJIDIC2 and in the repo's content-format convention, a leading "-" marks a suffix: a form that follows another element. A trailing "-" marks a prefix.
  - 座敷 and 風呂敷 fit the suffix reading, because しき follows another element. 敷地 does not: 敷 comes first.
  - The しき in 敷地 is the 連用形 (stem form) of 敷く, which belongs to the し.く reading.
  - The Joyo table supports this. Page 134 files 屋敷 and 敷石 under the しく row and has no separate しき row, and line 39 of the card says so.
  - So the card's own rule ("bound form … inside compounds") was stretched to fit 敷地. A learner would take from it that the dash means "inside a compound", which is wrong for every other card that uses a leading dash.
- **Remedy:** Either option fixes it.
  - Move 敷地 to the し.く row, noting it as the stem form しき of 敷く. The -し.き row keeps 座敷 and 風呂敷.
  - Or keep the row and rewrite the dash sentence: "the leading dash marks a suffix form, used after another element, as in 座敷 and 風呂敷". Then add that 敷地 uses the same しき at the start of a word.
- **Evidence:**
  - evidence\kanjidic2-records.xml (敷: the readings し.く and -し.き);
  - repo\docs\content-format.md (the convention for leading and trailing dashes in kunyomi);
  - supplement-111\joyo\p134.txt (the しく row with 敷く, 敷石 and 屋敷);
  - the Daijisen extract for 敷, which groups しき and じき "after another element" separately from word-initial しき.
- **Confidence:** High that the definition of the dash is inaccurate; medium–high that filing 敷地 under -し.き is the wrong row.

### F2. 鏡: "lens" in the title is not a meaning of 鏡
- **Severity:** Low.
- **Facets:** 1 (correctness) and 3 (quiz answer).
- **Location:** snapshot\kanji\鏡.md, line 3 (`title: mirror; lens`) and line 17 (H1).
- **Claim:** The title presents "lens" as a meaning of 鏡, parallel to "mirror".
- **Problem:**
  - KANJIDIC2 gives 鏡 the meanings "mirror, speculum, barrel-head, round rice-cake offering"; "lens" is not among them.
  - The Daijisen's second sense, quoted correctly in the card's body at line 25, is an instrument that uses lenses (眼鏡, 顕微鏡, 望遠鏡). That is "optical instrument; -scope", not "lens"; a lens itself is レンズ.
  - The only JMdict support I found is 鏡面 "mirror surface; lens surface", which is weak.
  - The body (line 23) explains the idea correctly: "the last part of many names for instruments built on lenses". The short title is what a quiz-taker sees, though, and it teaches a meaning the sources do not give.
  - It is not a quiz-safety failure: no other title or distractor collides with it.
- **Remedy:** Retitle to something like "mirror; -scope (optical instrument)" or "mirror; optical instrument", and keep the body as it is.
- **Evidence:**
  - evidence\kanjidic2-records.xml (鏡);
  - the Daijisen extract for 鏡 (senses 1–3);
  - jmdict-families.xml (鏡面, 眼鏡 1577670 and 2862467);
  - kanji-titles.tsv (`鏡	mirror; lens`).
- **Confidence:** Medium. The title is a defensible shorthand; the defect is the wording, not a wrong concept. The owner may reasonably downgrade it to Optional.

No other established defects. Specifically:

- Front matter matches source-metadata.json and KANJIDIC2 on all 15 cards: grade, strokes, radical, on and kun lists, quizOnyomi and quizKunyomi.
- Every Joyo claim matches the extracts, including the bracketed 節（節）, お節 under セチ, 眼鏡（めがね） in the remarks of 鏡, and 桟敷 さじき in brackets for 敷.
- Every example word's reading and first-sense gloss matches JMdict. The later-sense glosses quoted from JMdict (for example 税率 "tax rate", which is sense 2, and 節 ふし "notable point") are real.
- Every double-quoted kanji title I checked in the Notes matches kanji-titles.tsv exactly, about 120 of them.
- Mnemonics are labelled as modern-shape mnemonics, and the component claims are true: 制 + 衣; 羊 over 我; ⺮ + 即; 金 + 竟 with 竟 = 音 over 儿; and 玄 at the top of 率 with 十 at the bottom.
- Lead outcomes:
  - (a) Covered by F2 and Optional 2. The treatment of キョウ and ケイ is accurate: JMdict 1674690 lists めいけい as the third reading of 明鏡, and the card says ケイ is not in the Joyo table and is absent from the Daijisen.
  - (b) Not a defect; see Optional 3.
  - (c) F1.
  - (d) Not a defect. シュツ for 率 and リョウ for 養 are correctly marked source-only:
    - 卒 also carries シュツ;
    - 出塁率 does not show シュツ from 率;
    - 療養 is りょう + よう, so it does not show リョウ for 養.
  - (e) Not a defect.
    - Joyo p93 has rows only for セツ, セチ and ふし.
    - The card qualifies -ぶし (rendaku, as in 削り節 "flaked bonito") and のっと (JMdict 節 ノット: ateji, uk).
    - It does not present ノット as a Joyo reading.
  - (f) Not a defect. reading-exposure.txt reports 0 hits in production and 0 in padded sessions. The six latent collisions are 房 お and わ, 節 よ under two prompts, 養 や and 鏡 あき. They are attested non-quiz readings, and none of them can be drawn in the N1, All or Starter pools.
  - (g) Not a defect. JMdict has 独逸 ドイツ (ateji, rarely used, uk), and the abbreviation 独 = Germany is standard (独語, 日独). The title parallels the existing 欧 "Europe (abbreviation)", and no distractor or excluded card shares "Germany".

## Optional

1. **房, line 25 (attribution).** The card says the Daijisen illustrates the Awa sense "as in 安房 あわ". The Daijisen gives "安房国" and illustrates the sense with 房州 and 房総. Better: "the old province of Awa (安房), as in 房総 ぼうそう". Tiny; the gloss quoted for 安房 is fine.
2. **鏡, lines 25 and 34 (readings).**
   - The Daijisen's second キョウ sense lists 眼鏡 in its Sino-Japanese reading がんきょう, which JMdict has as a separate entry, 2862467. The card cites that sense right after saying (line 39) that 眼鏡 めがね gives 鏡 no reading. A short "(here read がんきょう)" would remove the apparent contradiction.
   - Optionally, mention that 眼鏡 めがね is often written in kana (JMdict: uk).
   - Note that めいきょう is the usual reading of 明鏡. Only めいけい appears in the ケイ row, though the paragraph at line 37 does explain it.
3. **義 (reading quiz).**
   - All three curated distractors, 議 疑 技, share the reading ギ. The ギ reading question therefore excludes all of them and falls back to tiered random options. reading-options.txt shows 143 distinct wrong options over 400 seeds and 0 problems.
   - That is safe. If the owner wants curated near-misses in the reading quiz, one distractor could be swapped for a visually confusable non-ギ kanji that has a card. Not required.
4. **節約 word-article title (context, not scope).** "economizing; conserving" is a paraphrase. JMdict's first glosses are "saving; economising; economizing; …". The diff only link-wraps that article, so this is not a batch defect.

## Limits

- **Contract breach, now disclosed:**
  - One of my responses, at about 11:26:21 UTC, contained two parallel `view` calls on rubric\copilot-instructions.md, which together covered lines 1–400.
  - The coordinator flagged it. Every response since has made exactly one call.
  - No other response contained more than one call.
- One earlier call failed because I gave a wrong path for a supplement file, a path under the packet instead of the sibling supplement folder. It returned nothing and opened nothing outside the allowed set.
- The Android JVM content tests were not run at this snapshot. That is a known limit of the packet; mechanical-checks.md says so.
- **Public-dictionary checks:**
  - I used the pinned public-source extracts in the packet (Weblio Daijisen character entries), together with the pinned JMdict/KANJIDIC2 data and the Joyo extracts.
  - I made no live web requests. Today's online dictionaries could differ slightly from the pinned snapshot.
  - Reading and sense claims that cite JMdict were checked against the families XML, not the live JMdict site.
- I read rubric\copilot-instructions.md and content-format.md only in part: the parts covering card structure, readings, dash conventions, quiz exclusions and distractors.
- Line numbers in Findings and Optional come from line-numbered searches of the snapshot files. In Scope, partial-read ranges and the list of repo cards for the first eight kanji are as recorded in my working notes.
- **Assumptions:**
  - The leading "-" in a KANJIDIC2 kun reading means a suffix, as in KANJIDIC2's own convention and the repo's content-format.
  - A kanji link nested inside an existing word link is not expected, so linking 授 at its second mention in 准教授.md is correct.
