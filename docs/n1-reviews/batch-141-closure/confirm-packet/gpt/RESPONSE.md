# Author's statement for the reviewer of `reports-141\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 is your report's own Findings label. Your report's
Optional section has three unlabelled bullets; here they are Optional 1 to 3 in the order they appear. The statement
is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`,
`diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line numbers refer to the revised
cards in this packet; other line numbers refer to the named file in this packet unless the original packet is named.
Four of the 15 new cards changed (懐 懸 扇 抽), the other eleven did not; the existing card 張 and the word articles
悔しい and 悔やむ also changed; no front matter or stroke file changed (see `CHANGES.md`). Give a disposition for G1 and
for Optional 1 to 3.

## Findings

### G1 (minor): 悔しい and 悔やむ still deny that the linked 悔 card exists

Author action: **changed** as you proposed.

- `words\悔しい.md:25` now reads `[悔](../kanji/悔.md) supplies the regret/frustration association in the native
  adjective くやしい. The dictionary also records 口惜しい as a rare kanji spelling.` The sentence `There is no 悔 card in
  the current collection.` is removed.
- `words\悔やむ.md:28` now reads `[悔](../kanji/悔.md) carries a regret association, here in the native verb くやむ; む is
  the ending. 悔む is another dictionary spelling of the same word.` The sentence `No 悔 kanji card is currently
  available.` is removed.
- Both removals are declared in `evidence\word-remarks.json` (it was `[]`), and the two diffs were regenerated:
  `checks\linkplan.txt` reports 21 added link pairs, 2 declared remark edits and 0 problems.
- Scope: the author scanned every published word article and kanji card for a sentence saying that one of this
  batch's 15 kanji has no card or is not available. These two lines were the only hits. That scan is the author's
  claim; it is not in the packet.

## Optional

- **Optional 1 (shorten or restructure the reference inventories): changed for 懐 and 扇, not for the others.**
  - `懐.md:66-69`: the single "For reference" bullet you named is split into four bullets, one each for the first,
    second and fourth カイ senses and one for the ふところ example 懐刀. The examples and glosses are unchanged and in
    the same order; the sense names repeat those at lines 27-30. Support: the original packet's
    `evidence\public-source\weblio-懐.txt` line 6 (the Daijisen character entry's numbered sense lists).
  - `扇.md:57-58`: the bullet is split before `Under おうぎ`, so the セン examples and the おうぎ examples are separate
    bullets. No word changed.
  - Not changed: `悟.md:25` is the sense paragraph, a two-sense account with its examples, not a reference list; `惑.md:51`
    (one sense's examples) and `慮.md:53` (three examples) are already single labelled reference bullets of moderate
    length. Removing examples was not done, because each one is a Daijisen example that the reference lines exist to
    record.
- **Optional 2 (compress the practice-selection explanations and mnemonic disclaimers): not applied.** Both are
  collection-wide conventions, not wording specific to this batch. In the original packet's `repo\kanji\` (1,367
  cards), the label `**Modern-shape mnemonic, not etymology:**` opens the mnemonic on 732 cards, a `Practice selects`
  sentence appears on 214 and the sentence `Being outside the practice set is not proof that a reading is invalid`
  appears on 116. Compressing them in one batch would make these cards inconsistent with the rest.
- **Optional 3 (no expansion required for name readings or unquizzed extras): agreed; no change.**

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **抽's ひき- example** (`抽.md:34`, `:36`): the ひき- row's example is now 抽斗 ひきだし, where 抽 writes ひき and 斗
  writes だし, instead of 抽き出し, where 抽 writes only ひ. Line 36 explains 抽斗, the search-only 抽出し (抽 ひき, 出 だ,
  okurigana し) and the rarely used 抽き出し, and says KANJIDIC2 lists ひき- for 抽 but no verb reading ひ.く. Support:
  `evidence\jmdict-cited-entries.xml`, entry 1601650; the original packet's `evidence\kanjidic2-records.xml` and
  `evidence\public-source\weblio-抽.txt` line 6.
- **張's remark** (`張.md:59`): the first Notes bullet now also names [拡](拡.md), "expand; enlarge; widen," as the other
  kanji in 拡張, and the closing sentence names only 緊 as having no card. The declared remark edit in
  `evidence\kanji-remarks.json` is updated; `checks\kanji-remarks.txt` reports 0 problems.
- **懸** (`懸.md:46`, `:56`): line 46 adds that JMdict also reads 懸念 けんねん, where 懸 supplies ケン (entry 1257720 in
  `evidence\jmdict-cited-entries.xml`); line 56 says `the common word` instead of `the common words`, because the
  section lists only 一生懸命.

## Process notes

- `65b47299` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `a92d134a`.
- The checks in `checks\` were run on the committed revision. No front matter changed, so the quiz and reading audits
  are identical to the freeze apart from their command lines.
