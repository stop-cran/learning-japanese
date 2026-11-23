# Author's statement for the reviewer of `b157-a5c6-reports\gpt.md`

This statement answers only the points in YOUR initial report. G1-G9 are your report's Findings 1-9. Your report had no optional
notes. Two of your Limits raise questions this revision can answer; they are L1 and L2 below. Your other Limits describe your own
method and need no answer. The statement is the author's claim about what changed and why. Verify each claim against the revised
text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this
text as evidence. Line numbers refer to the revised files in this packet. The ten batch kanji cards changed, as did the reused kanji
cards 助 and 理 and all ten new word articles (諸侯 only on its Dictionary line). The ledger
`docs\n1-sources\batch-157-progress.json` and `tools\audit_n1_batch.py` changed, a JMdict supplement packet for 合併 is new, and
the generated `manifest.json` was regenerated. Every stroke file and every other kanji card and word article is unchanged. See
`CHANGES.md`. Give a disposition for each of G1-G9, L1 and L2, and judge the other reviews' changes described below.

## Findings

### G1: ordinary meaning overlaps on the new kanji are unprotected

Author action: **changed**. Every pair you named is now a direct exclusion on the new card:

- 佐 `[丞, 助, 援, 支, 副]` (`kanji\佐.md:14`; reasons at line 40);
- 佳 `[美, 良, 善, 宜, 優, 俊, 傑, 秀, 英, 卓, 豪, 偉, 華]` (`kanji\佳.md:14`; reasons at line 39);
- 併 `[合, 兼, 結, 並, 共, 協, 接, 括, 統, 斉]` (`kanji\併.md:14`; reasons at line 39);
- 侍 `[士, 武, 臣, 仕, 僕, 兵]` (`kanji\侍.md:14`; reasons at line 41);
- 侯 `[殿]` (`kanji\侯.md:14`; line 37: 殿 can mean “lord” as an honorific as well as a palace);
- 俊 `[秀, 英, 傑, 才, 優, 卓, 豪, 賢, 偉, 哲]` (`kanji\俊.md:14`; reasons at line 37);
- 俵 `[袋]` (`kanji\俵.md:14`; line 42 gives JMdict's “straw bag; sack; bale” against 袋's title).

The pairs beyond your G1 and G2 lists came from later rounds: 佐 副; 佳 善, 宜, 卓, 豪, 偉, 華; 併 共, 協, 接, 括, 統, 斉; 侍 僕, 兵;
俊 豪, 偉, 哲; 倫 徳, 義, 善 (your G2 named 伴 and 輩). (美 and 優 on 佳, 合 on 併, 士 on 侍, and 秀 and 英 on 俊 were already in the reviewed snapshot.) Each card's Notes
line gives the overlapping sense. The ledger's new `kanjiQuizAudit.directExclusions` section holds the same rows, and
`tools\audit_n1_batch.py` now fails if a card's `quiz_exclusions` differs from its ledger row
(`evidence\audit-negative-kanji-exclusion.txt`). `checks\quiz-safety.txt` reports 0 errors and 0 warnings.

### G2: secondary senses also need guards

Author action: **changed**.

- 併/並: excluded; `kanji\併.md:23` now gives Digital Daijisen's side-by-side sense, used interchangeably with 並, with 併記 and 併存.
- 侍/仕: excluded; `kanji\侍.md:23` names KANJIDIC2's serving sense, and line 41 adds Daijisen's ジ sense of serving beside a person
  of high rank.
- 侮/卑: `kanji\侮.md:14` is `[卑]`; line 40 notes that KANJIDIC2 lists “despise” for 卑.
- 俗/凡 and 俗/卑: `kanji\俗.md:14` is `[凡, 卑]`; line 38 ties 凡 to the “mundane” sense and 卑 to the lowbrow sense.
- 倫/伴 and 倫/輩: `kanji\倫.md:14` is `[伴, 輩, 徳, 義, 善]`. The no-exclusion explanation is gone; line 38 says 伴 and 輩 share the
  companion sense, and line 23 adds that sense with 絶倫 (see "Changes made for the other reviews", item 3).

### G3: 侍 "samurai" against 武士 "samurai; warrior"

Author action: **changed**, with your remedy. `words\侍.md:8` is `quiz_exclusions: [武士]` (`evidence\word-quiz.txt:57`).
Synonyms (line 29) now names 武士 ぶし with its JMdict gloss (entry 1583680) and gives the historical sense of 侍 さむらい.

### G4: 侮る against 見下ろす

Author action: **changed**, with your remedy. `words\侮る.md:8` is `quiz_exclusions: [見下ろす]`. Line 28 no longer treats
見下ろす as spatial only: like 見下ろす, 侮る can express contempt, and 見下ろす also has a literal sense.

### G5: 補佐 against 助手, 手伝い and 世話

Author action: **changed**. `words\補佐.md:8` is
`quiz_exclusions: [援助, 助手, 手伝い, 世話, 手伝う, 助ける, 支える, 応援]`. Line 28 now gives the overlapping glosses in place of the
unsourced claims that 援助 is “broader” and that 補佐 “often describes helping a person carry out a role”. Line 32, unchanged, already says 補佐 can name either the act or the person. `evidence\word-quiz.txt:2101` shows all
eight; line 2105 shows that 補佐's options now come from a 37-word tie at score 7. `CHANGES.md` ("Points the author judged
acceptable") names 代理 and 兼任 in that tie; please check that judgment.

### G6: 佳作 against 名作

Author action: **changed**, with your remedy. `words\佳作.md:8` is `[傑作, 名作, 作品, 制作]`. Line 28 says 傑作 and 名作 can both
describe outstanding works, glosses 作品 and 制作, and no longer quotes 傑作's title.

### G7: 俵 against 袋

Author action: **changed**, with your remedy. `words\俵.md:8` is `[袋, バッグ, 鞄]`; line 28 gives JMdict's gloss of 袋 (entry
1411070). The kanji pair is G1.

### G8: 佐's military-rank sense

Author action: **changed**. `kanji\佐.md:23` adds Digital Daijisen's officer-rank sense, and line 36 adds 大佐 たいさ
“colonel; (navy) captain” (JMdict 1413740). One example covers the branch; 少佐 and 中佐 are not added.

### G9: 俗's vulgar sense and 風俗

Author action: **changed** (explanation), **no example word**.

- `kanji\俗.md:23` now lists customs, ordinary or worldly things, colloquial use, and what is considered lowbrow or vulgar.
- Line 34 glosses 風俗 as “manners; customs; public morals; also the sex-service industry in a separate sense” (entry 1499960).
- Line 38 keeps the note's first sentence, that 俗語 is not necessarily offensive. Its second sentence, on whether a term is rude,
  playful or neutral, was removed as unsourced.
- No vulgar-sense example word was added, because none qualifies under the batch's common-word rule (news1, ichi1, spec1 or gai1):
  低俗 (1434570) is news2 only, and 俗悪 (1405140), 卑俗 (1482810) and 俗っぽい (1405110) have no frequency tag. The same rule
  removed 王侯 and 俊英 (item 6 below). Please say whether the sentence is enough without an example.

## Limits answered

### L1: the row-specific justification for the untagged 諸侯

Author action: **evidence added**. The ledger `snapshot\docs\n1-sources\batch-157-progress.json` is in this packet.

- Line 7 (`selectionReason`) states the rule: a qualifying support word carries news1, ichi1, spec1 or gai1; news2/spec2 do not
  qualify. It lists 俊英, 侯, 侯爵 and 王侯 as news2/spec2 only, and names 諸侯 as the batch's sole exception.
- Line 14 (`exceptionReason` on the 侯 row) is the row-specific justification. It repeats your finding that no 侯 candidate
  qualifies and that 侯補 is search-only for 候補. It adds that 侯爵 would also need 爵, which has no card, and that 王侯 (1588830)
  means “the king and his feudal lords”, while 諸侯 (1344250) “feudal lords; barons; princes” matches the card's sense.
- `kanji\侯.md:33` and `37` label 諸侯 as a historical term with no frequency tag.

The coordinator's acceptance of the exception is not in this packet; this record is what it will rest on. Please judge whether the
record is sufficient.

### L2: no runtime manifest or signature evidence

Author action: **evidence added**.

- `checks\manifest.txt`: `tools\build_manifest.py` at the fix commit leaves `manifest.json` byte-identical (same sha256 before and
  after; tracked tree clean). `checks\audit.txt` reports `manifestFresh: true` and contentVersion `00777806885a6934`.
- `checks\budget.txt`: the content budget the CI enforces.
- `evidence\verify-commit.txt`: the signature status and key of every first-parent commit from the reviewed snapshot to the fix
  commit, and of the merge's second parent `2bc61140` (all `G` with key 9D94B9D311BD26A7), then `git verify-commit` of the fix
  commit and of `2bc61140`. The signer's user ID is redacted.
  `CHANGES.md` ("Process notes") discloses that five early commits were re-signed from another key, with identical trees.
- `evidence\word-quiz.txt` and `evidence\Words.kt`: the word-quiz options, computed by a Python port of the app's word-quiz code,
  which is included for comparison. The Kotlin tests were not run.

## Changes made for the other reviews

The other two reviews asked for the changes below, and four later review rounds (r2-r5, GPT-family only, see `CHANGES.md` "Process
notes") added to them. Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **More word exclusions:** 併用 `[使用, 利用, 使う, 用いる, 用, 用途]`, 俗語 `[言葉, 単語, 語]`, 俊足 `[速い]`, 倫理
   `[道徳, 善, 仁]`. `CHANGES.md` ("Word-quiz options") gives the reverse pairs these removed and the ties that changed.
2. **侮る's title:** “underestimate” is gone. The title is “look down on; make light of” (`words\侮る.md:4`, `11`), the example
   translations (lines 17-18) use “make light of”, and `kanji\侮.md:35` uses the new title. `kanji\侮.md:30` already glossed 侮る
   as “look down on; make light of” and is unchanged.
3. **倫:** the title is “ethics; moral principles” (`kanji\倫.md:3`, `17`; KANJIDIC2's “ethics” and Digital Daijisen's first sense
   人の守るべき筋道). Line 23 adds Daijisen's companion sense with 絶倫; line 34 adds 不倫 ふりん “infidelity; an extramarital
   affair” (Daijisen, `evidence\weblio-不倫.txt`); line 38 contrasts 倫理 with 不倫 and gives 五倫.
4. **合併:** `kanji\併.md:35` adds 合併 がっぺい “merger; consolidation” (1578970). A JMdict supplement packet adds this entry to the
   batch record (`snapshot\docs\n1-sources\batch-157-jmdict-supplement-selection.json` and `batch-157-jmdict-supplement.xml`).
5. **Word articles:**
   - 侍's figurative sense moved into Meaning (`words\侍.md:16`, `33`);
   - 俊足 now explains how 俊 and 足 combine (line 24) and the gifted-person sense restricted to the spelling 俊足 (line 32, citing
     Digital Daijisen on Kotobank, `evidence\kotobank-俊足.txt`, `kotobank-駿足.txt`);
   - 併用's Distinctive meaning (line 32) now gives only the JMdict gloss; example 1 about medicine is kept;
   - 倫理 (line 28) and 佳作 (line 28) give JMdict glosses instead of unsourced comparisons;
   - the 補佐, 倫理 and 諸侯 Dictionary lines cite “sense 1” (line 34).
6. **Removed common-word lines:** 王侯 on 侯 and 俊英 on 俊. Both carry only news2/spec2.
7. **Labels and readings:**
   - the batch cards' Readings rows no longer say “Not selected for questions.” or “source-only”;
   - 侮's あなず.る row reads “older form of あなどる (Digital Daijisen via Weblio)” (`kanji\侮.md:31`, `40`);
   - 侍's シ row gives JMdict's 内侍 glosses “maid of honor; lady-in-waiting” (JMdict also lists the spelling “maid of honour”), then “a historical court title”
     (`kanji\侍.md:30`; `evidence\kotobank-内侍.txt`);
   - mnemonics removed from 佳 and 併.
8. **助 and 理:** the baseline 理 lint error you mentioned is fixed. `kanji\理.md:31` adds the ことわり row (JMdict 2412900),
   labelled “kun, source-only here”, as 助's new す.ける and すけ rows are (`kanji\助.md:32-33`). Line 26
   now introduces the row, and line 46 adds a Metadata line citing 2412900. `CHANGES.md` ("Labels") asks whether
   the batch should use the same label. The 語 `phonetic` error is outside the batch and unchanged.
9. **Distractors:** all ten sets changed after the author's own quiz-safety check. No reviewer asked for this; `CHANGES.md`
   ("Distractor choices") gives the reasons and the pairs the author judged acceptable. Please check that no new distractor is a
   defensible answer for its card.

10. **Wording tied to a source, or removed when it could not be:**
    - 佳: line 37 adds that JMdict records 佳い (よい) as a rarely used spelling (entry 1605820) that the card does not teach as a
      usual kun reading;
    - 佐: line 40 adds that JMdict records 佐ける (たすける) as a rare spelling of 助ける (entry 1344410);
    - 併: line 39 opens with JMdict's note that 併せる is a rarely used kanji form of 合わせる, though the sense “to do at the same
      time; to take (e.g. into consideration) together; to do in addition to” is written esp. 併せる when in kanji (entry 1284480),
      and ends with 併せて sense 2, “in addition; besides; at the same time” (entry 1506010);
    - 俊: line 23 now quotes 俊足's first JMdict sense, “swiftness of foot; fast runner” (was “a word whose common sense is ‘fast
      runner’”);
    - 侯: line 23 now calls 諸侯 a historical compound;
    - 俵: the ヒョウ row (line 29), line 40 and `words\俵.md:32` now say that ひょう is the only JMdict reading for the counter sense
      and that, for the noun 俵, JMdict tags たわら as common and also lists ひょう (entry 1583390). Line 40 replaces “The selected
      quiz reading is たわら …”;
    - 助: the Notes line 45 now reads “The table marks source-only readings explicitly.” (was “The table selects readings; the
      metadata retains the additional source forms.”);
    - removed as unsourced: the second sentence of the 俗語 note (G9), and the second sentence of `words\俊足.md:15`, “JMdict also
      records a sense meaning a gifted person for this spelling.” The sense stays at line 32, now tied to Daijisen (item 5).

Every other changed line is a distractor sentence or Metadata line that follows from the changes above, a Dictionary line or
併's Words line that adds JMdict entry ids to cite or compare (`kanji\併.md:34`, `words\佳作.md:34`, `words\侍.md:35`,
`words\俵.md:34`, `words\倫理.md:34`), a ledger or tooling line, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
