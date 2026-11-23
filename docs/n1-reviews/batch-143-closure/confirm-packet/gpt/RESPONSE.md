# Author's statement for the reviewer of `reports-143\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 to G4 are your report's own Findings labels; your
Optional section has two bullets, which are called O-A (reduce dictionary and audit inventory in learner-facing prose)
and O-B (the 朗 良 shape wording) below. The statement is the author's claim about what changed and why. Verify each
claim against the revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as
evidence. Card line numbers refer to the revised cards in this packet; other line numbers refer to the named file in
the original packet unless stated. Twelve of the 15 new cards changed (旋 既 旦 旨 暑 朗 条 架 柄 染 株 桜), the other three
(施 旗 暦) did not; front matter changed in 既 and 旋 only (`quiz_exclusions`, see `CHANGES.md`). Give a disposition for
each of G1 to G4, O-A and O-B.

## Findings

### G1 (minor): 柄 Common words pairs え with "pattern"

Author action: **changed** as you proposed. `柄.md:48-49` now has two bullets, `柄 え — handle; grip` and `柄 がら — pattern;
design`, both linking the same word article. Support: `evidence\jmdict-cited-entries.xml` (1508290 え; 1508300 がら).

### G2 (minor): 旦つく presented simply as "husband"

Author action: **changed**. `旦.md:34` now reads `旦つく だんつく — husband (a slighting word)`; the word is kept as an example.
Support: `evidence\weblio-dantsuku.txt` (Daijisen: 「旦那」を軽んじていう語). Verify that the label is adequate.

### G3 (minor): 暑 "蒸 supplies むし"

Author action: **changed** as you proposed. `暑.md:36` now says that in 蒸し暑い 蒸 writes む and し is okurigana, so 蒸し is むし.
Support: `evidence\jmdict-cited-entries.xml` (1356870 蒸し暑い).

### G4 (minor): association-based exclusions 既–在, 既–存, 既–有 and 旋–凱; 旋's false comparison

Author action: **changed** as you proposed, for all four pairs.

- `既.md:14` no longer lists 在, 存 or 有, and `既.md:48` no longer has the existence sentence; the 既 exclusions are now the
  time/former group (前 予 先 昨 旧 元 故) and the completion group (完 全 終 済 卒).
- `旋.md:14` no longer lists 凱, and `旋.md:54` no longer puts 凱 among the kanji that overlap returning (帰, 戻 and 返
  remain). 凱 is still explained on `旋.md:41` and `旋.md:51` as the other kanji of 凱旋.
- The three quiz and reading audits were rerun and are unchanged apart from their command lines (see `CHANGES.md`).
  Because front matter changed, please re-check the meaning-quiz options for 既 and 旋 yourself, as the audits may not
  cover the effect of removed exclusions.

## Optional

- **O-A (compress the 条 and 架 prose): not applied.** The Joyo, Daijisen and JMdict facts in 条 and 架 are the
  card's support for the readings it lists, and the batch's other cards of the same collection carry similar paragraphs.
  The author did not want to remove reading support in a revision round. The 条 stroke wording
  (`条.md:58`, `an added horizontal stroke`) and the 架 example (`架.md:25`, 書架 しょか, bookshelf) were changed for other
  reasons.
- **O-B (朗 `良` at the left): not applied.** The mnemonic is labelled a modern-shape memory aid with no etymological
  claim (`朗.md:31`). `朗.md:51` now names 月, 有 and 朝 as the distractors, so 良 is not read as one.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; review them like any other changed hunk.

- **既 and 朗 Joyo wording** (`既.md:38`, `朗.md:43`): `compatibility ideograph` replaced by the traditional (Kangxi
  dictionary) form (`evidence\joyo-item6.txt`); **桜** (`桜.md:25`, `桜.md:37`: ミザクラ is the fruit-cherry tree; 桜ん坊
  is さくら + ん + 坊); **染** (`染.md:34,40,42`: 愛染 reads ゼン, outside the Joyo table); **旨** (`旨.md:25,37`: 旨味 is a
  separate JMdict entry; the skillful sense is marked as especially written 上手い or 巧い); **株** (`株.md:25`: 守株 is 守 シュ + 株 シュ); **旦**
  (`旦.md:25,41,52`: 一旦 is いっ + タン and contains no あした; だんな in hiragana); **条** (`条.md:58,61`: 条 is read すじ in 条彫り and 条播き; the whole-word caveat is kept for 発条 ばね only); **架** (`架.md:25`).

## Process notes

- `9b8f50a8` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `6b5934e7`.
- The checks in `checks\` were run on the committed revision. Front matter changed in 旋 and 既, and the three quiz and
  reading audits are unchanged apart from their command lines (see `CHANGES.md`).
