# Author's statement for the reviewer of `reports-141\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 and C2 are your report's own Findings labels, and O1
to O5 are your Optional labels. The statement is the author's claim about what changed and why. Verify each claim
against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in
this packet unless the original packet is named. Four of the 15 new cards changed (懐 懸 扇 抽), the other eleven did
not; the existing card 張 and the word articles 悔しい and 悔やむ also changed; no front matter or stroke file changed
(see `CHANGES.md`). Give a disposition for each of C1, C2 and O1 to O5.

## Findings

### C1 (moderate): two word articles still say there is no 悔 card

Author action: **changed** as you proposed (deletion).

- `words\悔しい.md:25` now reads `[悔](../kanji/悔.md) supplies the regret/frustration association in the native
  adjective くやしい. The dictionary also records 口惜しい as a rare kanji spelling.` The sentence `There is no 悔 card in
  the current collection.` is removed.
- `words\悔やむ.md:28` now reads `[悔](../kanji/悔.md) carries a regret association, here in the native verb くやむ; む is
  the ending. 悔む is another dictionary spelling of the same word.` The sentence `No 悔 kanji card is currently
  available.` is removed.
- Both removals are declared in `evidence\word-remarks.json` (it was `[]`), so the link-plan check now verifies them:
  `checks\linkplan.txt` reports 2 declared remark edits and 0 problems.
- Scope: besides your search of the 21 changed articles, the author scanned every published word article and kanji card
  for a sentence saying that one of this batch's 15 kanji has no card or is not available. These two lines were the
  only hits. That scan is the author's claim; it is not in the packet.

### C2 (minor): 抽's ひき- row illustrated with a word where 抽 writes only ひ

Author action: **changed** as your first remedy proposed.

- `抽.md:34`, the ひき- row: the example is now `抽斗 ひきだし - drawer`, and the row says JMdict `marks 抽斗 and 抽き出し
  as rarely used kanji forms` (the order of the two forms is swapped); the rest of the row is unchanged.
- `抽.md:36`: the sentence `In 抽き出し, 抽 writes ひ, …` is replaced by: `In 抽斗, 抽 writes ひき and 斗 writes だし;
  Daijisen lists 抽斗 ひきだし as a hard-to-read word. JMdict also lists 抽出し, where 抽 writes ひき, 出 writes だ and し
  is okurigana, the kana ending that follows the kanji, as a search-only spelling. In the rarely used spelling 抽き出し,
  抽 writes only ひ and き is okurigana; KANJIDIC2 lists ひき- for 抽 but no verb reading ひ.く.` Your report gave
  `出し = だし` for 抽出し; the card splits it further into 出 だ and okurigana し.
- Support: `evidence\jmdict-cited-entries.xml`, entry 1601650; the original packet's `evidence\kanjidic2-records.xml`
  (抽: チュウ, ひき-) and `evidence\public-source\weblio-抽.txt` line 6. No new word is named, and 1601650 was already on
  the Metadata line.

## Optional

- **O1 (張, first Notes bullet): changed.** `張.md:59` now ends `[威](威.md), "intimidate; authority; dignity," is the
  other kanji in 威張る, and [拡](拡.md), "expand; enlarge; widen," is the other kanji in 拡張. 緊 in 緊張 does not have a
  kanji card yet.` The quoted gloss is 拡's title (`checks\link-targets.tsv`). The declared remark edit in
  `evidence\kanji-remarks.json` is updated to this text, and `checks\kanji-remarks.txt` reports 0 problems.
- **O2 (悔過 けか for ケ): not applied.** `悔.md:27` presents ケ as a Daijisen reading that is not in KANJIDIC2, with
  懺悔, and says it is voiced to げ in both readings of 懺悔. 悔過 けか (JMdict 2865883) is a Buddhist term with no word
  article; adding it would lengthen that paragraph for a reading the card does not practise, and the card makes no
  claim that ケ only occurs voiced.
- **O3 (懸, "the common words"): changed.** `懸.md:56` now reads `The other kanji in the common word are …`.
- **O4 (慎's つつましやか and 要慎): not applied,** as your report allowed. つつましやか (JMdict 2201680, an adjectival
  noun) is a relative of 慎ましい, which the card's つつ.ましい row (`慎.md:35`) already covers, and 要慎 is a search-only
  kanji form in JMdict's 用心 entry (1546310), so neither adds a reading or a sense a learner needs here.
- **O5 (懸念 けんねん): changed.** `懸.md:46` now ends `In 懸念, 懸 supplies ケ and 念 supplies ネン; JMdict lists けねん
  first and also the reading けんねん, where 懸 supplies ケン.` Support: `evidence\jmdict-cited-entries.xml`, entry
  1257720.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **懐's reference bullet** (`懐.md:66-69`): the single "For reference" bullet with the extra Daijisen examples is split
  into four bullets, one each for the first, second and fourth カイ senses and one for the ふところ example 懐刀. The
  examples and glosses are unchanged and in the same order. The sense names repeat those at lines 27-30. Support: the
  original packet's `evidence\public-source\weblio-懐.txt` line 6.
- **扇's reference bullet** (`扇.md:57-58`): split before `Under おうぎ`, so the セン examples and the おうぎ examples are
  separate bullets. No word changed.
- Both splits only make the longest reference lines easier to scan on a phone.

## Process notes

- `65b47299` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `a92d134a`.
- The checks in `checks\` were run on the committed revision. No front matter changed, so the quiz and reading audits
  are identical to the freeze apart from their command lines.
