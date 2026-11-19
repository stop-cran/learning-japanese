# Author's statement for the reviewer of `reports-144\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C8 are your report's own Findings labels. Your
Optional section is a bulleted list without IDs; its items are labelled O-A to O-L below in the order they appear
(O-A 棚, O-B 検, O-C 概, O-D 欄, O-E 歓, O-F 淡 and 渋 "One example of each", O-G 渇 and 渋 mnemonics, O-H 渇 渇する,
O-I 泡 あぶく, O-J 殻 かい, O-K 汁 attribution, O-L title overlaps judged non-defensible). The statement is the author's
claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch` and
independent sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet;
other line numbers refer to the named file in the original packet unless stated. Nine of the 15 new cards changed
(棋 棚 欄 歓 殻 汁 沖 淡 渋) and the existing card 討; the other six new cards (検 概 殊 泡 泣 渇) did not. No front matter
changed in any card (see `CHANGES.md`). Give a disposition for each of C1 to C8 and O-A to O-L.

## Findings

### C1: 棚 claims 氷棚 is the only JMdict ほう word, but 陸棚 りくほう exists

Author action: **changed** as you proposed. `棚.md:33` now says JMdict has ほう only in technical words, 陸棚 りくほう
(also りくだな), "continental shelf," and 氷棚 ひょうほう, "ice shelf." Support: `evidence\jmdict-cited-entries.xml`
(1551120).

### C2: 棚 misreads the Daijisen ▽ mark

Author action: **changed** as you proposed. `棚.md:25` now writes the headword as たな【▽店／棚】 and says the ▽ marks 店,
not 棚. The non-standard-form claim is gone. Verify that my wording of the ▽ (`the spelling whose reading is outside the
Joyo table`) is accurate.

### C3: 歓 Notes say 権 has a similar-looking left part

Author action: **changed** as you proposed. `歓.md:45` now says 権 has a part at its right that looks like the left part
of 歓.

### C4: 淡 calls あわ a name-only reading

Author action: **changed** as you proposed. `淡.md:32` now says Daijisen lists あわ as in 淡雪 あわゆき, and the name
readings あわし and あわじ. Support: original `public-source\weblio-淡.txt`; `evidence\jmdict-cited-entries.xml` (1418470).

### C5: the rewritten 討 bullet keeps a sentence that no longer has a referent

Author action: **changed** as you proposed (your second remedy). `討.md:95` now reads `In 検討, [検](検.md) supplies ケン
and 討 supplies トウ.` The declared remark edit in `evidence\kanji-remarks.json` was updated to the new text. Verify
that the new bullet is true and still reads correctly in its Notes list.

### C6: the 殻 curated distractors 休 本 木 are not plausible wrong answers

Author action: **declined**, with reasons. `殻.md` front matter is unchanged.

- The three are Starter cards. Because they are in every pool and fill all three slots of every 殻 reading prompt, the
  attested かい that 貝 offers cannot be drawn (`reading-exposure.txt`: 0 production, 0 padded, 0 one-holder hits; the
  older `reading-options.txt` HIT 殻 かい is not drawable). Replacing them with look-alike kanji that hold no から, がら
  or かい reading would reopen that exposure and need a new reading audit; the same curated-Starter approach was
  accepted for earlier batches.
- The meaning prompt is a different question: the curated distractors are also the meaning options, and the author's
  view is that 休, 本 and 木 are defensibly wrong ("rest", "book", "tree" against "shell; husk; empty outer covering"),
  just easy. Your finding states that they cause no error. The other reviewer reached the same view (safe but easy).
- To verify: whether you still regard this as a defect rather than optional polish, and whether any better-looking
  replacement would keep かい undrawable in `QuizBuilder.kt` and the Starter pool.

### C7: 欄 misquotes the おばしま gloss and is inconsistent about the bracketed form

Author action: **partly changed**.

- Point 1 changed: `欄.md:42` now quotes `"handrail; railing; banister; balustrade,"` and says JMdict marks the entry
  archaic. Support: `evidence\jmdict-cited-entries.xml` (2844081).
- Point 2 not applied: the card does not add the Daijisen ［訓］おばしま mention. The card already names the JMdict entry
  and says this card does not add it; the author did not add a second source for a reading that is not taught.
- Point 3 declined: `欄.md:44` keeps `a compatibility form of the same kanji`. The packet's `joyo-pages.md` prints the
  bracketed form after 欄 with a different code point (U+F91D, a compatibility ideograph) that is drawn like 欄, so it is
  not a different, older character the way 檢, 槪 and 殼 are, which is why the other cards say `older form`. Verify that
  the wording is accurate rather than inconsistent.

### C8: 棋 ご and 沖 ちゅう.する are typed "kun" without qualification

Author action: **changed**, in the table cell only. The `kun` type and the metadata lists are unchanged because they
follow KANJIDIC2. `棋.md:32` now says KANJIDIC2 files ご under kun but Kanjipedia lists ゴ as an on reading (original
`kanjipedia-outside-readings.json`: 棋 on キ and ゴ). `沖.md:34` says KANJIDIC2 files ちゅう.する under kun but the Joyo
table files 沖する under チュウ (original `joyo-pages.md`).

## Optional

- **O-A (棚: Daijisen sense list, the 明 note, the 店 sentence): not applied.** The Daijisen sense list is a selection
  by design; the 明 and 店 sentences are accurate. 棚.md:51 is unchanged.
- **O-B (検 exclusions 点 and 剖): no change.** Both are supported by 点検 and 剖検 and are harmless as exclusions.
- **O-C (概 "bearing" explanation): not applied.** The card already explains the 気概 sense; you judged the overlap with
  穂 low risk.
- **O-D (欄 weak exclusions 井 額 件 条; "form field"): no change.** Exclusions only remove options.
- **O-E (歓 合歓 mention): not applied.** 合歓 is outside the card's example set; the meta scan lists 合歓木 as a part of
  a run.
- **O-F ("One example of each:" in 淡 and 渋): not applied.** Cosmetic; the lists are labelled by sense.
- **O-G (渇 and 渋 mnemonic detail): no change.** The mnemonics carry the modern-shape label.
- **O-H (渇 渇する): not applied.** Not a quizzed reading; 渇す and 渇する are fed to the audits as extra readings.
- **O-I (泡 あぶく): not applied.** Not selected for questions.
- **O-J (殻 かい discussion): not applied.** You said leaving it out is acceptable.
- **O-K (汁 attribution of "juice"): not applied.**
- **O-L (title overlaps 淡/原, 沖/高, 沖/剖 爆 野 開, 汁/渋): no change.** Your judgement matched the author's.

## Process notes

- `2be716f0` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `b073abd8`.
- The checks in `checks\` were run on the committed revision. No front matter changed, and the three quiz and reading
  audits are unchanged apart from their command lines (see `CHANGES.md`).
