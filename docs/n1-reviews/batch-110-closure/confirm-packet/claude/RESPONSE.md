# Author's statement for the reviewer of `reports-110\initial-claude.md`

This statement answers only the points in YOUR initial report. IDs F1-F5 and O1-O6 are your report's own labels. L1 and L2
are questions the author adds, based on the first two bullets under your Limits (the Joyo table; the truncated quiz
simulation). L3 is a question the author adds about a topic your report does not cover (the reading prompts). The
statement is the author's claim about what changed and why. Verify each claim against the revised card text in
`snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Line numbers refer to
the revised cards in this packet (and to `snapshot\words\応援.md`). All 15 cards are in `snapshot\kanji\`, and all 15
changed, because every long paragraph was split (see `CHANGES.md`). Give a disposition for each of F1-F5, O1-O6 and L1-L3.

## Findings

### F1 (major): 器 mnemonic describes a component the modern character does not have

Author action: **changed.**

- `器.md:29`: the mnemonic is rebuilt. The centre is now "[大](大.md), "big, large," with no dot"; the image is "four
  mouths crowded around one big serving bowl"; the disclaimer says "口 or 大". `器.md` no longer links the 犬 card.
- `器.md:27` (new paragraph): "The official Joyo table also prints an older form of 器 in round brackets, with a dot in
  its centre like 犬; this card teaches the standard form, whose centre is plain 大." Evidence: `evidence\joyo\p33.txt` (text
  extract of Joyo page 33; it prints the bracketed older form as the compatibility ideograph U+FA38, which Unicode
  normalisation maps to the standard 器, U+5668, so the two can look alike in some fonts) and two images,
  `evidence\joyo-p33-utsuwa.png` (crop of the 器 entry) and `evidence\joyo-p33-utsuwa-pair.png` (both glyphs side by side,
  enlarged); `evidence\README.md` describes them.
- Stroke data is unchanged (15 strokes; original packet `snapshot\strokes\器.json`). The KanjiVG record is
  `evidence\kanjivg\05668.svg`: two 口 on top; 大 with two 口 below.

To verify: that the Joyo table does print an older, dotted form of 器 in brackets, that the new mnemonic describes the
standard glyph correctly, and that paragraph 27 would not confuse a beginner.

### F2 (minor): 価 readings paragraph wrongly says 価 supplies both か syllables of かかく

Author action: **changed.**

- `価.md:37`: "In 価格, 価 is read か and 格 supplies カク." The clause "so 価 is か in both syllables of かかく" is gone. The
  wording differs from your suggestion ("supplies the first か") but states the same split.

To verify: that the split is stated correctly and that nothing else in `価.md:37-41` misaligns a character and a reading.

### F3 (minor): 激 mnemonic misplaces 放

Author action: **changed.**

- `激.md:27`: "find 氵, "water," at the left, [白](白.md), "white," above [方](方.md), "direction, method," in the middle,
  and 攵 standing at the far right; 方 and 攵 together make [放](放.md), "release." ... it makes no claim that 白, 方 or 放
  contributes meaning or sound." This follows your suggested geometry.
- KanjiVG record `evidence\kanjivg\06fc0.svg` (stroke coordinates): 氵 at x 10-26; the right part 敫 has, in its left
  column (x 25-62), 白 at y 14-53 above 方 at y 54-94, and 攵 at x 57-94 on the right; the record marks 放 as part 1 (方)
  and part 2 (攵).

To verify: that the geometry in the new sentence matches the standard glyph and the KanjiVG record.

### F4 (minor): 応 paragraph denies that ヨウ is a reading of 応

Author action: **changed.**

- `応.md:40`: the last sentence now reads "In 応用, 応 is read オウ and 用 supplies ヨウ." The clause "which is why ヨウ
  appears in the word without being a reading of 応" is gone. Your suggested closing clause ("even though ヨウ is also
  listed as a rare on reading of 応") was not added, because the card already says it in two places: the ヨウ row
  (`応.md:34`: "no common word reads 応 as ヨウ; the ヨウ of 応用 おうよう belongs to 用; not selected for questions here")
  and `応.md:44` ("KANJIDIC2 and the Daijisen character entry list ヨウ, the 漢 reading, alongside オウ ...").

To verify: that no remaining sentence of `応.md` contradicts the ヨウ row, and that the shorter sentence is accurate.

### F5 (minor): 嫌 / 怪 is not excluded

Author action: **changed.**

- `嫌.md:14`: `quiz_exclusions: [憎, 疑, 怪]`.
- `嫌.md:58`: the Notes bullet says why: 憎 shares the KANJIDIC2 glosses "hate" and "detest" with 嫌; 疑, "doubt; suspect,"
  and 怪, "suspicious; uncanny," overlap the Daijisen sense of suspecting and the title word "suspicion"; all three are kept
  out of the quiz options.
- 怪 is listed on 嫌's side only. `excluded(a, b)` in `evidence\QuizBuilder.kt` is true if either card lists the other, so
  with 怪 as the prompt the title of 嫌 is also kept out. `怪.md` is unchanged (original packet `repo\kanji\怪.md`).
- The options now shown for 嫌 are on the 嫌 line of `checks\quiz-safety.txt`.

To verify: that 怪 cannot appear among the options for 嫌 in either direction, and that the three exclusions are justified.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `素.md:39`, `素.md:63` | New paragraph on 素敵 すてき, "lovely; wonderful; charming," and 素晴らしい すばらしい, "wonderful; splendid; magnificent," left unlinked as you suggested (no word article). It says that JMdict marks both spellings as ateji, so they help you recognise 素 but do not show its meaning. JMdict entries 1397350 and 1397300 are added to the Metadata line and are in `evidence\jmdict-cited-entries.xml`. |
| O2 | **changed** | `嫌.md:23` | "in some older compounds suspecting it" is now "in a few compounds suspecting it". "Formal" was not used: JMdict 嫌疑 (1257320) is glossed "suspicion (of having committed a crime, wrongdoing)" and carries no register tag (see the evidence file). |
| O3 | **changed** | `縮.md:56`, `騒.md:56` | Now "In this word 縮 is read ちり, which is not one of the readings above." and the same for 騒 and さい. The card states the fact without the label "irregular reading". |
| O4 | **declined** | `words\仮名遣い.md:24` (original packet `snapshot\words\仮名遣い.md`; unchanged in this revision) | The new link `[仮](../kanji/仮.md)` sits on the 仮 of "the contracted 仮名 unit". It is harmless (your own assessment) and goes to the right card. The batch's link plan puts the word-to-kanji link for each declared kanji on an occurrence in the article's "How the kanji combine" section, preferring a stand-alone occurrence to one inside a longer word. 仮名遣い has no stand-alone 仮 anywhere: every 仮 in the text of the article is followed by 名, so the only candidates in that section are 仮名 (line 24, the one linked), 仮名遣 and 仮名使い (line 26). Leaving 仮 unlinked would drop the word-to-kanji link for a declared kanji, and the other candidates are no better placed. |
| O5 | **changed** | `応.md:38` | The まさに row now says that JMdict gives 正に, 将に and 当に as spellings of まさに, which it marks as usually written in kana alone. Entries 1376640 (正に), 2856503 (将に) and 2856504 (当に) are in `evidence\jmdict-cited-entries.xml`, so the 将に and 当に claim can be checked against the pinned JMdict instead of live Jisho. |
| O6 (整) | **declined** | `整.md:23` | "[整備] せいび is maintenance or putting in place" paraphrases the two JMdict senses of 整備 (1376240): "maintenance; servicing" and "putting in place; development; improvement; preparation; provision; equipping; outfitting." The article's own title, "maintenance; putting in order," is a different, equally accurate gloss. `words\整備.md` is unchanged. |
| O6 (嫌い) | **declined** | `嫌.md:36` | The table glosses 嫌い as "disliked; dislike," following the title of the linked article `words\嫌い.md` ("disliked, dislike"). JMdict 嫌い (1257240) sense 1 is "disliking; hating; detesting." The difference is one of wording, not of meaning. The article is unchanged. |

## Limits

### L1: Joyo table claims (UNVERIFIED in your report; author's question)

Your first Limits bullet could not read the Joyo PDF. This packet carries text extracts of the Joyo pages for all 15
kanji: `evidence\joyo\p<N>.txt`. Each file's header gives the page, the source URL and the expected kanji; the PDF's SHA-256
is in `evidence\README.md`. Please check the claims you left UNVERIFIED: each card's Joyo example words, the "⇔" contrasts
(張/貼, 応える/答える, 基 もと ⇔ 下/元/本, 価/値, 暖か/温か, 整/調) and the remarks-column items (応 反応/順応, 素 素人, 仮 仮名).
This revision changes no Joyo claim except the new 器 paragraph (`器.md:27`, see F1). Give a disposition for L1 itself:
`RESOLVED` (nothing remains open), or a statement of what remains.

### L2: options for 張, 器 and 素 (not visible in your report; author's question)

Your second Limits bullet says that the simulation in the original packet was truncated, so the options for 張, 器 and 素
could not be seen. `checks\quiz-safety.txt` now lists the options of all 15 cards after this revision. Please read it, check
that every option shown for 張, 器 and 素 (and for the other twelve cards) is defensibly wrong in both directions, and give a
disposition for L2 itself: `RESOLVED`, or a statement of what remains.

### L3: reading prompts (not covered by your report; author's question)

The reading quiz is separate from the meaning quiz: `quiz_exclusions` do not apply to it. `evidence\KanjiReadings.kt` and
`evidence\Words.kt` are the app's sources for the reading options (`KanjiReadingQuiz`, `excludedKeys`, `closeness`,
`ReadingOptions.mutations`); `evidence\README.md` says where they come from. `checks\reading-options.txt` is the author's audit of every reading
prompt of the 15 cards. It lists the excluded readings, the curated and fallback candidates for each wrong option and any
reading that is attested for a card but not listed in its metadata (it prints these as "unlisted readings attested", for
example 張 わり, 素 もとより, 応 いらえる, 縮 ちり, 騒 さい). Its result is "0 problem(s)". Caveats: the audit pool is every
card in `kanji\` (the app draws from the cards the learner has studied), fallback options are random within closeness tiers,
and the audit's random generator is not the app's, so it reports candidate sets rather than exact draws. Please say whether
any wrong option for a reading prompt of these cards could be a valid reading of the card, say what the audit cannot show,
and give a disposition for L3 itself: `RESOLVED`, or a statement of what remains.

### Other limits in your report

Version differences, example sentences, out-of-scope items and the heading-order assumption: no action is claimed and no
disposition is needed. (For the version point: the entries for 将に and 当に are now in `evidence\jmdict-cited-entries.xml`.)
