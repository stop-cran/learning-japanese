# Author's statement for the reviewer of `b158-60d2-reports\claude.md`

This statement answers only the points in YOUR initial report. C1-C3 are your report's Findings 1-3, and O1-O5 are your five
Optional bullets in order. One of your Limits raises a question this revision can answer; it is L1 below. Your other Limits
describe your own method and need no answer. The statement is the author's claim about what changed and why. Verify each claim
against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources;
do not rely on this text as evidence. Line numbers refer to the revised files in this packet. Nine batch kanji cards changed (all
but 匠), as did six of the ten new word articles (偏見 傍観 勲章 升 即座 師匠). The ledger `docs\n1-sources\batch-158-progress.json`,
the batch's pinned JMdict extract `batch-158-jmdict.xml` and its entry list `batch-158-jmdict-selection.json` changed (13 entries
added for the newly cited ids), and the generated `manifest.json` was regenerated. Every stroke file and every other
kanji card and word article is unchanged. See `CHANGES.md`. Give a disposition for each of C1-C3, O1-O5 and L1, and judge the other
reviews' changes described below.

## Findings

### C1: the support word 升 ます carries only news2/spec2

Author action: **not changed** (升 ます remains the support word), **record changed**.

- The rule that governs support words is in `evidence\rule-7058679348.md`, point 2 ("Choice of word"). It prefers a spelling with
  one of news1, ichi1, spec1 or gai1, and says: "where none exists, an untagged word may be used with a justification reviewed for
  that row." It also says: "The tags guide the choice; they are not evidence of frequency." The frozen ledger treated 升 as an
  exception to a rule that news2/spec2 do not qualify, without a row-specific justification. That was the defect you found.
- Ledger line 29 (`selectionReason`) now says that no candidate written with 升 carries a qualifying tag, "so the rule's untagged
  route applies", and that the row-specific justification is in the 升 support mapping and must receive independent review.
- Ledger line 132 (`exceptionReason` on the 升 row) is that justification. Check each claim in it:
  - 升 ます (1346290) is the only 升 entry with any priority marker (news2/spec2, treated as untagged);
  - its spelling and reading carry no irregular, rare, outdated, ateji or gikun mark;
  - ます is a KANJIDIC2 reading of 升, and the word is the single kanji, so no other card is needed;
  - its sense 1, "measuring box", matches the first KANJIDIC2 meaning of 升 and the card's main meaning, and it backs the quizzed
    kun reading ます (`kanji\升.md:12`);
  - the alternatives are all untagged: 升 しょう (2248100) is the volume unit; 一升 (1163460) and 一升瓶 (1163470) use the
    unselected ショウ reading; 升目 (1654590) is a derived word.
- The same record precedes this batch for 仙人 and 伯仲 (B156) and 諸侯 (B157). `evidence\support-selection.json` holds the
  selection statement and every support mapping at the revised snapshot. The entries are in `evidence\jmdict-cited-entries.xml`.
- The owner has not yet ruled on whether news2/spec2 should count as qualifying; the author will ask again when the batch is
  published.

Please judge whether this justification satisfies the rule's untagged route for this row.

### C2: priority-tag jargon in the 升 Notes

Author action: **changed**. The sentence naming news1, ichi1, spec1, gai1, news2 and spec2 is deleted from `kanji\升.md:40`; the tag
audit stays in the ledger (C1). The line keeps JMdict's spellings 枡 and 桝 and Daijisen's note that both are kokuji.

- Your suggested plain-words substitute, that 升 "is a less common word" and that ます "is often written in kana", is not added. The
  rule says the tags are not evidence of frequency, and the author has no other frequency source for it. JMdict 1346290 has no
  "usually written using kana" mark; only sense 3 (square on a grid) carries the note "esp. マス", and the word article no longer
  teaches that sense (see "Changes made for the other reviews", item 2).

### C3: readings given by the cited sources but not shown on 傍, 偏, 匿 and 即

Author action: **changed**. Each card now has one Notes line that names the reading, its source and its Kanjipedia 外 mark, and
says that it is not in the card's metadata and is not quizzed:

- 偏: `kanji\偏.md:42`, ひとえに (Daijisen kun; Kanjipedia 外), spelled 偏に in JMdict, "wholly; solely; earnestly", usually
  written in kana (entry 1510320).
- 傍: `kanji\傍.md:46`, ホウ (Daijisen on) with 傍輩 ほうばい from Daijisen's hard-to-read list (JMdict 1517130, "comrade;
  friend; associate; colleague"), and the kun reading そ.う; Kanjipedia marks both 外.
- 匿: `kanji\匿.md:42`, 匿す as a rarely used spelling of 隠す かくす (entry 1170650), and ジョク and かく.れる (Kanjipedia 外).
- 即: `kanji\即.md:45`, ショク (Kanjipedia 外).

The same kind of line was added for consistency on 債 (`kanji\債.md:42`, か.り and か.し), 勲 (`kanji\勲.md:42`, いさおし, with
いさお already noted) and 升 (`kanji\升.md:40`, のぼ.る; see O4). The Kanjipedia data is in the original packet's
`evidence\public-source\kanjipedia.json`, and the Daijisen text in `weblio-<kanji>.txt`. On 偽 and 却 the label "source-only"
is now defined where it is used (`kanji\偽.md:44`, `kanji\却.md:43`).

## Optional notes

### O1: 返却's "How the kanji combine"

Author action: **not changed**. The line (`words\返却.md`, unchanged) ties the combination to Daijisen's sense of 却 that lists
返却. The author found no source that says 却 adds a sense of finishing or sending off in 返却, which your suggestion required.

### O2: "a wooden masu" for the sake example

Author action: **changed**. `words\升.md:18` now reads "into a wooden masu (measuring box)".

### O3: 隠す and 隠れる as exclusions for 匿名

Author action: **not changed**. As you say, they differ in meaning (匿名 is anonymity). Neither appears anywhere in
`evidence\word-quiz.txt`: not among 匿名's meaning-quiz options (a 33-word tie at score 7) and not in any reverse pair.

### O4: the のぼ.る reading of 升

Author action: **changed**. `kanji\升.md:40` adds that Kanjipedia gives the kun reading のぼ.る, marked 外, not in the card's
metadata and not quizzed. The opening (line 23) now limits the 昇 interchange to the two senses Daijisen names (item 6 below).

### O5: your list of checks with no defect found

No answer needed.

## Limits answered

### L1: JMdict ids that were not in the packet

Author action: **evidence added**. `evidence\jmdict-cited-entries.xml` now includes the complete pinned entries for all nine ids you
could not check: 1291410 (差別), 1321470 (実名), 1484150 (秘密), 1351910 (賞), 1533700 (模倣), 1214900 (観察), 1260000 (見物),
1512130 (返す) and 1590240 (貸し出し).

## Changes made for the other reviews

The other two reviews asked for the changes below. Please judge each change as a reviewer of the revised text, not only as an
answer to your own notes.

1. **偏見 excludes 意見.** `words\偏見.md:8`; line 28 glosses 意見 "an opinion or view in general" (entry 1156530) and says 偏見 is a
   view that leans to one side. `evidence\word-quiz.txt:8-18` shows the new option set.
2. **The word 升.** The title is now "measuring box" (`words\升.md:4`, `11`), and 腰掛け "seat; bench" is excluded (line 8). Line 15
   drops the grid-square sense (JMdict sense 3, marked "esp. マス") and explains sense 2 as "a box, as in box seating at a theatre
   and similar places", with 升席 ますせき, a tatami "box seat" for four people at sumo, kabuki and similar shows (entry 1706800).
   The Dictionary line cites senses 1-2. On the kanji card the ます row reads "measuring box; also box seating at a theatre"
   (`kanji\升.md:30`). `CHANGES.md` explains why 席, 座席 and 客席 are not excluded.
3. **偏 excludes 側** (`kanji\偏.md:14`; reason at line 40).
4. **偽's distractor 犬 is replaced by 耳** (`kanji\偽.md:13`, `48`). JMdict 1258330 sense 4 of 犬 is "counterfeit; inferior;
   useless; wasteful" (`evidence\distractor-senses.txt`).
5. **債.** Line 40 now cites JMdict's antonym marks on 債務 and 債権: "the debt owed by one side and the claim held by the other"
   (was "held by the lender"). Line 23 gives the readings ふさい, さいむ and さいけん and says that 債権 ("a claim") and 債券 ("a
   bond") sound the same but are different words; the サイ row (line 29) adds 債券 (entry 1292070).
6. **升's 昇 interchange** (`kanji\升.md:23`): "Digital Daijisen also gives two more senses, rising and, from grain ripening, a
   peaceful, well-governed age; it notes that in these two senses 升 is used interchangeably with 昇." This follows Daijisen's
   補説 「2・3は「昇」と通用する」.
7. **即's opening** (`kanji\即.md:23`): the sense "attaching closely to something, read つく", with 即位 そくい, accession to the
   throne, listed under it; 色即是空 is replaced by the reading すなわち for "that is; namely".
8. **勲's opening** (`kanji\勲.md:23`): 元勲 げんくん "elder statesman" (entry 1260770), and 勲一等 くんいっとう "order of the 1st
   class" (entry 1247200) for the rank sense instead of 叙勲.
9. **却's opening** (`kanji\却.md:23`): the "doing something completely" sense is illustrated by 忘却 ぼうきゃく, "forgetting
   completely; oblivion" (entry 1519260); 冷却 is no longer cited.
10. **匿 excludes 皮** "skin; hide" (`kanji\匿.md:14`; reason at line 40).
11. **Optional wording:**
    - 勲章 explains "order" as an order of merit, not a command (`words\勲章.md:15`);
    - 師匠 explains a stable master as the head of a sumo stable (`words\師匠.md:15`) and glosses Rakugo (line 18);
    - kana readings at first mention for 偏狭, 人偏, 傍系, 傍流 and 元勲;
    - 即座: 座 is "a seat or to sit" (`words\即座.md:24`);
    - 傍観: "You must not just stand by …" (`words\傍観.md:17`);
    - 偽物's gloss is now JMdict's "forgery; counterfeit; imitation" (`kanji\偽.md:32`).

Every other changed line is a Metadata line or Dictionary line that adds the JMdict entry ids cited above, a ledger line that
records the same changes, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
