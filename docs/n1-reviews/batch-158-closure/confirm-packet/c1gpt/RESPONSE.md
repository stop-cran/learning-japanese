# Author's statement for the reviewer of `b158-60d2-reports\gpt.md`

This statement answers only the points in YOUR initial report. G1-G6 are your report's Findings 1-6, and O1-O2 are the two points
of your Optional paragraph in order. Two of your Limits raise questions this revision can answer; they are L1 and L2 below. Your
other Limits describe your own method or files this revision does not change, and need no answer. The statement is the author's
claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\`
outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised
files in this packet. Nine batch kanji cards changed (all but 匠), as did six of the ten new word articles (偏見 傍観 勲章 升 即座
師匠). The ledger `docs\n1-sources\batch-158-progress.json`, the batch's pinned JMdict extract `batch-158-jmdict.xml` and its entry
list `batch-158-jmdict-selection.json` changed (13 entries added for the newly cited ids), and the generated `manifest.json` was
regenerated. Every stroke file, every reused kanji card and every other word article is unchanged. See `CHANGES.md`. Give a
disposition for each of G1-G6, O1-O2, L1 and L2, and judge the other reviews' changes described below.

## Findings

### G1: 偏見 and 意見

Author action: **changed**. `words\偏見.md:8` now excludes 意見. Line 28 adds the distinction: 意見 (いけん) is an opinion or view in
general (JMdict entry 1156530); 偏見 is a view that leans to one side. The Dictionary line (line 34) cites 1156530 among the compared
entries. `evidence\word-quiz.txt`, lines 8-18, shows the new option set: three exclusions, and four words tie at score 6 (拝見, 見学,
見当, 見物). The reading-quiz reverse pair 偏見→意見 (line 3608) remains; it is a reading look-alike (へんけん/いけん), and
exclusions apply to meaning quizzes.

### G2: the seating sense of 升

Author action: **changed**. The sense is kept and the learner-facing labels and guards are changed:

- The word's title, which is the label the quiz shows, is now "measuring box" (`words\升.md:4`, `11`), so no quiz option labels 升
  as a seat.
- Line 15 explains JMdict's sense 2 as "a box, as in box seating at a theatre and similar places", with 升席 ますせき, a tatami "box
  seat" for four people at sumo, kabuki and similar shows (entry 1706800). The kanji card's ます row reads "measuring box; also box
  seating at a theatre" (`kanji\升.md:30`). The grid-square sense (JMdict sense 3, "esp. マス") is no longer taught.
- 腰掛け "seat; bench", which you found reachable, is now excluded (line 8), and line 28 says why: 腰掛け is a seat or bench (JMdict
  entry 1288370), while 升 in its second sense is a whole box of seating. `evidence\word-quiz.txt`, lines 1690-2365: 俵 scores 7,
  and 668 words tie at 5; 腰掛け is no longer among them.
- 席 "seat", 座席 "seat; seating" and 客席 "audience seating; audience" are not excluded. None of them is among the 669 candidates
  (lines 1697-2365), and no reverse pair (lines 3221-3327) shows 升 in their quizzes. An exclusion that names a word the quiz
  cannot draw would protect nothing. If you think any of them can still be offered, please cite the line.

### G3: 偏 and 側

Author action: **changed**. `kanji\偏.md:14` now excludes 側. Line 40 gives the reason: KANJIDIC2 lists "side" among the meanings of
偏, which overlaps with 側 ("side") and with 傍, whose KANJIDIC2 meanings also include "side".

### G4: 偽's distractor 犬

Author action: **changed**. 犬 is replaced by 耳 "ear" (`kanji\偽.md:13`, `48`), so the set is 耳, 山, 白 and the sentence "none
means fake or false" holds for each. `evidence\distractor-senses.txt` shows every JMdict sense of 耳, 山 and 白, and
`evidence\distractor-use.tsv` (line 6) shows 耳 is already used by curated sets in this batch (偏 and 升). `checks\quiz-safety.txt`,
`checks\reading-exposure.txt` (偽 section) and `checks\reading-options.txt` show no new collision.

### G5: the support word 升 ます carries only news2/spec2

Author action: **not changed** (升 ます remains the support word), **record changed**.

- The rule that governs support words is in `evidence\rule-7058679348.md`, point 2 ("Choice of word"). It prefers a spelling with
  one of news1, ichi1, spec1 or gai1, and says: "where none exists, an untagged word may be used with a justification reviewed for
  that row." You were right that the frozen ledger did not use this route: it recorded 升 as an exception with no row-specific
  justification.
- Ledger line 29 (`selectionReason`) now says that no candidate written with 升 carries a qualifying tag, "so the rule's untagged
  route applies", and that the row-specific justification is in the 升 support mapping and must receive independent review.
- Ledger line 132 (`exceptionReason`) is that justification. It says that:
  - 升 ます (1346290) is the only 升 entry with any priority marker (news2/spec2, treated as untagged);
  - its spelling and reading carry no irregular, rare, outdated, ateji or gikun mark;
  - ます is a KANJIDIC2 reading of 升, and the word is the single kanji, so no other card is needed;
  - its sense 1, "measuring box", matches the first KANJIDIC2 meaning of 升 and the card's main meaning, and it backs the quizzed
    kun reading ます;
  - the alternatives are all untagged: 升 しょう (2248100) is the volume unit; 一升 (1163460) and 一升瓶 (1163470) use the
    unselected ショウ reading; 升目 (1654590) is a derived word.
- The same record precedes this batch for 仙人 and 伯仲 (B156) and 諸侯 (B157). `evidence\support-selection.json` holds the
  selection statement and every support mapping at the revised snapshot, and the entries are in
  `evidence\jmdict-cited-entries.xml`.
- The owner has not yet ruled on whether news2/spec2 should count as qualifying; the author will ask again when the batch is
  published.

Please judge whether this justification satisfies the rule's untagged route for this row.

### G6: 債権 as the claim "held by the lender"

Author action: **changed**. `kanji\債.md:40` now says that JMdict marks 債務 ("debt; liabilities; obligation") and 債権 ("credit;
claim") as antonyms: "the debt owed by one side and the claim held by the other". It no longer names a lender.

Line 23 still describes Digital Daijisen's second sense of 債 as "collecting what one has lent, as in 債権 さいけん, a claim". That is
a paraphrase of the kanji sense 「貸しを取り立てること」 (original packet, `evidence\public-source\weblio-債.txt`), with 債権 as its
example, not a definition of 債権. Line 23 also adds that 債権 ("a claim") and 債券 ("a bond") sound the same but are different
words, and the サイ row (line 29) adds 債券 (entry 1292070).

## Optional notes

### O1: "order" in 勲章

Author action: **changed**. `words\勲章.md:15`: "Here “order” means an order of merit, an honour awarded for service, not a command."

### O2: "stable master" in 師匠

Author action: **changed**. `words\師匠.md:15`: "In sumo, it also means a stable master, the head of a sumo stable."

## Limits answered

### L1: the manifest, the app code and the commit signatures

Author action: **evidence added**.

- `evidence\verify-commit.txt` holds `git verify-commit -v` and `git log --show-signature` for the reviewed snapshot 60d2cd5a and the
  two revision commits 6605a8b0 and ccc046bb, and their parents.
- `evidence\QuizBuilder.kt` and `evidence\Words.kt` are the app's kanji-quiz and word-quiz code, which `word-quiz.txt`,
  `reading-options.txt` and `reading-exposure.txt` model.
- `manifest.json` is generated and is left out of `diffs\` by design. `checks\manifest.txt` shows that rebuilding it at ccc046bb
  leaves its sha256 unchanged, and `checks\audit.txt` reports `"manifestFresh": true` and content version `d5b0861e10d1bf24`.

### L2: the first-ten-remaining selection order

Author action: **evidence added**. `evidence\selection-order.tsv` lists the frozen source rows 1-140 from
`docs\n1-sources\source-index.json` with each kanji's KANJIDIC2 grade, its class (Joyo for grades 1-8, name-use for grade 9),
whether `kanji\<kanji>.md` exists at the batch base ad1694c1, and whether it is in this batch. The first ten Joyo rows with no card
at the base are rows 63, 67, 68, 72, 120, 123, 125, 126, 131 and 132 (偏 偽 傍 債 勲 匠 匿 升 即 却), which is this batch.

## Changes made for the other reviews

The other two reviews asked for the changes below. Please judge each change as a reviewer of the revised text, not only as an
answer to your own notes.

1. **Policy jargon removed.** The sentence naming JMdict's priority tags is deleted from `kanji\升.md:40`; the tag audit stays in
   the ledger (G5).
2. **Readings the sources give but the cards did not show.** One Notes line each names the reading, its source and its Kanjipedia
   外 mark, and says it is not in the card's metadata and is not quizzed: 偏 ひとえに, spelled 偏に (entry 1510320)
   (`kanji\偏.md:42`); 傍 ホウ with 傍輩 ほうばい (entry 1517130) and そ.う (`kanji\傍.md:46`); 匿す as a rarely used spelling of 隠す
   (entry 1170650), and ジョク and かく.れる (`kanji\匿.md:42`); 即 ショク (`kanji\即.md:45`); 債 か.り and か.し
   (`kanji\債.md:42`); 勲 いさおし (`kanji\勲.md:42`); 升 のぼ.る (`kanji\升.md:40`). On 偽 and 却 the label "source-only" is now
   defined where it is used (`kanji\偽.md:44`, `kanji\却.md:43`).
3. **升's 昇 interchange** (`kanji\升.md:23`): "Digital Daijisen also gives two more senses, rising and, from grain ripening, a
   peaceful, well-governed age; it notes that in these two senses 升 is used interchangeably with 昇." This follows Daijisen's
   補説 「2・3は「昇」と通用する」.
4. **即's opening** (`kanji\即.md:23`): the sense "attaching closely to something, read つく", with 即位 そくい, accession to the
   throne, listed under it; 色即是空 is replaced by the reading すなわち for "that is; namely".
5. **勲's opening** (`kanji\勲.md:23`): 元勲 げんくん "elder statesman" (entry 1260770), and 勲一等 くんいっとう "order of the 1st
   class" (entry 1247200) for the rank sense instead of 叙勲.
6. **却's opening** (`kanji\却.md:23`): the "doing something completely" sense is illustrated by 忘却 ぼうきゃく, "forgetting
   completely; oblivion" (entry 1519260); 冷却 is no longer cited.
7. **匿 excludes 皮** "skin; hide" (`kanji\匿.md:14`; reason at line 40: it shares only the English word "hide").
8. **Wording:**
   - "a wooden masu (measuring box)" in the 升 sake example (`words\升.md:18`);
   - Rakugo glossed in the 師匠 example (`words\師匠.md:18`);
   - kana readings at first mention for 偏狭, 人偏, 傍系, 傍流 and 元勲;
   - 即座: 座 is "a seat or to sit" (`words\即座.md:24`);
   - 傍観: "You must not just stand by …" (`words\傍観.md:17`);
   - 偽物's gloss is now JMdict's "forgery; counterfeit; imitation" (`kanji\偽.md:32`).
9. **Evidence.** `evidence\jmdict-cited-entries.xml` includes the complete pinned entries for every id the revised text cites and
   for the compared words.

Every other changed line is a Metadata line or Dictionary line that adds the JMdict entry ids cited above, a ledger line that
records the same changes, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
