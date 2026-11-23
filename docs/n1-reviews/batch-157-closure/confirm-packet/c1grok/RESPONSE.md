# Author's statement for the reviewer of `b157-a5c6-reports\grok.md`

This statement answers only the points in YOUR initial report. X1-X11 are your report's Findings 1-11, and O1-O6 are the six
points of your Optional paragraph in order. Two of your Limits raise questions this revision can answer; they are L1 and L2 below.
Your other Limits describe your own method and need no answer. The statement is the author's claim about what changed and why.
Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and
independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet. The ten batch
kanji cards changed, as did the reused kanji cards 助 and 理 and all ten new word articles (諸侯 only on its Dictionary line). The
ledger `docs\n1-sources\batch-157-progress.json` and `tools\audit_n1_batch.py` changed, a JMdict supplement packet for 合併 is new,
and the generated `manifest.json` was regenerated. Every stroke file and every other kanji card and word article is unchanged. See
`CHANGES.md`. Give a disposition for each of X1-X11, O1-O6, L1 and L2, and judge the other reviews' changes described below.

## Findings

### X1: 侮る teaches "underestimate"

Author action: **changed**, with your remedy.

- The title is now “look down on; make light of” (`words\侮る.md:4`, `11`).
- Both example translations use “make light of” (lines 17-18): “Do not make light of your opponent’s strength.” and “He made light
  of the danger and did not prepare.” Line 32, unchanged, already notes that the examples take a person's ability and a danger as
  targets.
- `kanji\侮.md:35` uses the new title. `kanji\侮.md:30` already glossed 侮る as “look down on; make light of” and is unchanged.
- “Underestimate” no longer appears on either card.

### X2: 侍 "samurai" against 武士, and the colloquial sense in Synonyms

Author action: **changed**, with your remedy.

- `words\侍.md:8` is `quiz_exclusions: [武士]` (`evidence\word-quiz.txt:57`).
- Synonyms (line 29) now names 武士 ぶし with its JMdict gloss “samurai; warrior” (entry 1583680) and gives the historical sense of
  侍 さむらい: a warrior, especially a military retainer of a daimyo in the Edo period (entry 1314780 sense 1, cited on the
  Dictionary line 35).
- The colloquial sense moved into Meaning (line 16) and Distinctive meaning (line 33).

### X3: 侮る against 見下ろす

Author action: **changed**, with your remedy. `words\侮る.md:8` is `quiz_exclusions: [見下ろす]` (`evidence\word-quiz.txt:741`).
Line 28 states the shared contempt sense.

### X4: 佐 against 援 and 丞

Author action: **changed**. `kanji\佐.md:14` is `[丞, 助, 援, 支, 副]`. Another review asked for 助 and 支 as well; 副 came from a
later round (JMdict 1500330, “assistant; associate; vice-; sub-; deputy”). Line 40 gives the reasons.

### X5: 俊 and 佳 against 傑, 才 and 秀

Author action: **changed**. `kanji\俊.md:14` is `[秀, 英, 傑, 才, 優, 卓, 豪, 賢, 偉, 哲]` (reasons at line 37), and `kanji\佳.md:14`
is `[美, 良, 善, 宜, 優, 俊, 傑, 秀, 英, 卓, 豪, 偉, 華]` (reasons at line 39). The pairs beyond 傑, 才 and 秀 came from the other reviews and later rounds. The ledger's new `kanjiQuizAudit.directExclusions`
section holds the same rows; `tools\audit_n1_batch.py` now fails if a card's `quiz_exclusions` differs from its ledger row
(`evidence\audit-negative-kanji-exclusion.txt`). `checks\quiz-safety.txt` reports 0 errors and 0 warnings.

### X6: 佳作 against 名作, and the 傑作 quotation

Author action: **changed**. `words\佳作.md:8` is `[傑作, 名作, 作品, 制作]`. Line 28 no longer quotes 傑作's title; it says that 傑作
and 名作 can both describe outstanding works, that 佳作 can also name an honorable mention, and glosses 作品 and 制作.

### X7: 補佐 against 助手, and 併 against 兼

Author action: **partly changed**: both exclusions are made; no separate role contrast is added.

- `words\補佐.md:8` is `[援助, 助手, 手伝い, 世話, 手伝う, 助ける, 支える, 応援]`. Line 28 gives the glosses: 援助 and 補佐 both
  mean aid or assistance; 助手 names an assistant; “[手伝い] can mean help or a helper; [世話] can mean care or assistance”; and
  these English glosses overlap, though each Japanese word has distinct uses. Line 32, unchanged, already says 補佐 can name the
  act or the person.
- The earlier claims that 援助 is “broader” and that 補佐 “often describes helping a person carry out a role” were removed
  rather than rewritten, because the author could not tie them to a source (another review said they are not in JMdict). Please say whether the exclusion is enough without a contrast line.
- `kanji\併.md:14` includes 兼; line 39 says 兼 can describe combining roles.

### X8: 合併 is missing from 併

Author action: **changed**, with your remedy. `kanji\併.md:35` adds an unlinked line 合併 がっぺい “merger; consolidation” (JMdict
1578970). The batch's pinned JMdict families lacked this entry, so a supplement packet adds it to the batch record
(`snapshot\docs\n1-sources\batch-157-jmdict-supplement-selection.json` and `batch-157-jmdict-supplement.xml`).

### X9: 俗's unrefined sense and the 風俗 gloss

Author action: **changed**, with your remedy.

- `kanji\俗.md:23` now covers customs, ordinary or worldly things, colloquial use, and what is considered lowbrow or vulgar, and
  says 風俗 can mean manners, customs or public morals and, in another sense, the sex-service industry.
- Line 34 glosses 風俗 the same way (entry 1499960). Line 38 keeps the note's first sentence, that 俗語 is not necessarily
  offensive; its second sentence, on whether a term is rude, playful or neutral, was removed as unsourced.
- 低俗, 俗悪 and 卑俗 are not added: 低俗 (1434570) is news2 only and the other two have no frequency tag, so none qualifies under
  the batch's common-word rule (news1, ichi1, spec1 or gai1).

### X10: 俊足's combination section and the gifted-person sense

Author action: **changed** (combination and label), **no example**.

- Line 15 keeps “俊足 means swiftness of foot or a fast runner.”; its second sentence, on the gifted-person sense, is removed, and
  that sense is now explained at line 32.
- Line 24 now says how the parts combine: 俊 conveys talent or excellence, 足 means foot, and together they form a word for
  swiftness on foot and a fast runner.
- Line 32 labels the gifted-person sense as restricted to the spelling 俊足 and says the article focuses on JMdict's first sense. It
  also cites Digital Daijisen's 俊足 and 駿足 entries on Kotobank (`evidence\kotobank-俊足.txt`, `kotobank-駿足.txt`): Daijisen
  gives the gifted-person sense first, its second 俊足 sense points to 駿足 sense 2, and “swift horse” is 駿足 sense 1.
- No gifted-person example sentence was added. Please say whether the label is enough.

### X11: authoring jargon in Readings rows

Author action: **changed**.

- No batch card's Readings row says “Not selected for questions.” or “source-only” any more. Quiz selection comes from each card's
  front matter, so the rows do not say “not used in questions” either.
- `kanji\侮.md:31`: あなず.る now reads “older form of あなどる (Digital Daijisen via Weblio)”; line 40 says the same in Notes.
- `kanji\侍.md:30`: 内侍 gives JMdict's glosses “maid of honor; lady-in-waiting” (entry 1582520; JMdict also lists the spelling
  “maid of honour”), then “a historical court title”. Line 41 repeats that in Notes. `evidence\kotobank-内侍.txt` holds the Digital Daijisen, Seisenban Nihon Kokugo Daijiten
  and Nipponica extracts.
- `kanji\俵.md:40` no longer says “The selected quiz reading is たわら …”. It now says that JMdict lists ヒョウ in 土俵 and, for the
  standalone word 俵, tags たわら as common and also lists ひょう, the only reading for the counter sense.

## Optional notes

### O1: vague mnemonics on 佳 and 併

Author action: **changed**. Both mnemonics are removed. 佐's labelled modern-shape mnemonic (`kanji\佐.md:25`) is kept.

### O2: 倫's Notes explain a quiz decision

Author action: **changed**. `kanji\倫.md:38` no longer explains a quiz decision. It contrasts 倫理 with 不倫, gives 五倫 ごりん, says
that 伴 and 輩 share the companion sense, and names 徳 (“virtue”), 善 (“good; virtue”) and 義 (“righteousness”) as related moral
concepts.

### O3: 倫理:24 and 補佐:24 do not say what each kanji contributes

Author action: **not changed**. Both lines link the two kanji cards, which give each character's meaning. Please say whether the
lines still need the meanings.

### O4: 補佐 examples show only 補佐する

Author action: **not changed**. Line 15 states the assistant or adviser sense, and line 32 says 補佐 can name the person. Both
examples keep the verb use.

### O5: em dashes in Common words differ from older hyphens in 補 and 諸

Author action: **not changed**. Both separators occur in the repository's Common words sections: 1,065 kanji cards use only em
dashes, 511 only hyphens, and 12 (補 and 諸 among them) mix both. `docs\content-format.md` fixes neither. The batch lines keep the
em dash used by the new cards.

### O6: 土俵 as a valid ヒョウ alternative

Author action: **already met**. `kanji\俵.md:29` uses 土俵 (JMdict 1445550) in the ヒョウ row and line 35 lists it under Common
words; no article was added. The row's second clause changed for another reason: it now says that JMdict also lists 俵 ひょう, the
only reading for the counter sense (entry 1583390).

## Limits answered

### L1: the 諸侯 tag check is not acceptance of an exception

Author action: **evidence added**. The ledger `snapshot\docs\n1-sources\batch-157-progress.json` is in this packet.

- Line 7 (`selectionReason`) states the rule as applied (news1, ichi1, spec1 or gai1; news2/spec2 do not qualify), lists 俊英, 侯,
  侯爵 and 王侯 as news2/spec2 only, and names 諸侯 as the batch's sole exception.
- Line 14 (`exceptionReason` on the 侯 row) records the same check you made, including 侯補 as a search-only form for 候補. It adds
  that 侯爵 would also need 爵, which has no card, and that 王侯 (1588830) means “the king and his feudal lords”, while 諸侯
  (1344250) “feudal lords; barons; princes” matches the card's sense.
- `kanji\侯.md:33` and `37` label 諸侯 as a historical term with no frequency tag.

### L2: the pre-existing lint errors in 理 and 語

Author action: **changed** for 理, **not changed** for 語. `kanji\理.md:31` adds the ことわり row (JMdict 2412900), labelled “kun,
source-only here” like 助's new す.ける and すけ rows (`kanji\助.md:32-33`); line 26 introduces it and line 46 adds a Metadata line.
`checks\lint.txt` now shows only the `phonetic` error in `kanji/語.md`, which is outside the batch and unchanged. `CHANGES.md`
("Labels") asks whether the batch should use the same label.

## Changes made for the other reviews

The other two reviews asked for the changes below, and four later review rounds (r2-r5, GPT-family only, see `CHANGES.md` "Process
notes") added to them. Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **More kanji exclusions:**
   - 併 adds 結, 並, 共, 協, 接, 括, 統 and 斉 (`kanji\併.md:23` adds the side-by-side sense shared with 並);
   - 侍 `[士, 武, 臣, 仕, 僕, 兵]` (line 41; line 23 names KANJIDIC2's serving sense);
   - 侯 `[殿]` (line 37);
   - 侮 `[卑]` (line 40: KANJIDIC2 lists “despise” for 卑);
   - 俗 `[凡, 卑]` (line 38);
   - 俵 `[袋]` (line 42);
   - 倫 `[伴, 輩, 徳, 義, 善]` (line 38).

   Please check that each excluded pair rests on a real sense overlap and that none is excessive.
2. **More word exclusions:** 俵 `[袋, バッグ, 鞄]`, 併用 `[使用, 利用, 使う, 用いる, 用, 用途]`, 俗語 `[言葉, 単語, 語]`, 俊足
   `[速い]`, 倫理 `[道徳, 善, 仁]`. `CHANGES.md` ("Word-quiz options") gives the reverse pairs these removed and the ties that
   changed.
3. **倫:** the title is “ethics; moral principles” (`kanji\倫.md:3`, `17`; KANJIDIC2's “ethics” and Digital Daijisen's first sense
   人の守るべき筋道). Line 23 adds Daijisen's companion sense with 絶倫; line 34 adds 不倫 ふりん “infidelity; an extramarital
   affair” (`evidence\weblio-不倫.txt`).
4. **佐's officer-rank sense:** `kanji\佐.md:23` and line 36, 大佐 たいさ “colonel; (navy) captain” (JMdict 1413740).
5. **Word articles:**
   - 併用's Distinctive meaning (line 32) now gives only the JMdict gloss; example 1 about medicine is kept;
   - 俵 (line 28) and 倫理 (line 28) give JMdict glosses instead of unsourced comparisons;
   - the 補佐, 倫理 and 諸侯 Dictionary lines cite “sense 1” (line 34).
6. **Removed common-word lines:** 王侯 on 侯 and 俊英 on 俊. Both carry only news2/spec2.
7. **Distractors:** all ten sets changed after the author's own quiz-safety check. No reviewer asked for this; `CHANGES.md`
   ("Distractor choices") gives the reasons and the pairs the author judged acceptable. Please check that no new distractor is a
   defensible answer for its card.

8. **Wording tied to a source, or removed when it could not be:**
   - 佳: line 37 adds that JMdict records 佳い (よい) as a rarely used spelling (entry 1605820) that the card does not teach as a usual
     kun reading;
   - 佐: line 40 adds that JMdict records 佐ける (たすける) as a rare spelling of 助ける (entry 1344410);
   - 併: line 39 opens with JMdict's note that 併せる is a rarely used kanji form of 合わせる, though the sense “to do at the same time;
     to take (e.g. into consideration) together; to do in addition to” is written esp. 併せる when in kanji (entry 1284480), and ends
     with 併せて sense 2, “in addition; besides; at the same time” (entry 1506010);
   - 俊: line 23 now quotes 俊足's first JMdict sense, “swiftness of foot; fast runner” (was “a word whose common sense is ‘fast
     runner’”);
   - 侯: line 23 now calls 諸侯 a historical compound;
   - 俵: `words\俵.md:32` now says the counter is read ひょう and that, for the noun, JMdict tags たわら as common and also lists ひょう
     (the kanji card's lines are in X11 and O6);
   - 助: the Notes line 45 now reads “The table marks source-only readings explicitly.” (was “The table selects readings; the metadata
     retains the additional source forms.”);
   - removed as unsourced: the second sentence of the 俗語 note (X9), the second sentence of `words\俊足.md:15` (X10), and the
     補佐/援助 breadth and role claims (X7).

Every other changed line is a distractor sentence or Metadata line that follows from the changes above, a Dictionary line or
併's Words line that adds JMdict entry ids to cite or compare (`kanji\併.md:34`, `words\佳作.md:34`, `words\侍.md:35`,
`words\俵.md:34`, `words\倫理.md:34`), a ledger or tooling line, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
