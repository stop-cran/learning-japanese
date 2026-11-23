# Author's statement for the reviewer of `b157-a5c6-reports\claude.md`

This statement answers only the points in YOUR initial report. C1-C10 are your report's Findings 1-10, and O1-O5 are your five
Optional bullets in order. Three of your Limits raise questions this revision can answer; they are L1-L3 below. Your unverified
補佐/援助 nuance is answered in O4. Your other Limits describe your own method and need no answer. The statement is the author's claim about what changed and why. Verify each
claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent
sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet. The ten batch kanji cards
changed, as did the reused kanji cards 助 and 理 and all ten new word articles (諸侯 only on its Dictionary line). The ledger
`docs\n1-sources\batch-157-progress.json` and `tools\audit_n1_batch.py` changed, a JMdict supplement packet for 合併 is new, and
the generated `manifest.json` was regenerated. Every stroke file and every other kanji card and word article is unchanged. See
`CHANGES.md`. Give a disposition for each of C1-C10, O1-O5 and L1-L3, and judge the other reviews' changes described below.

## Findings

### C1: 侍 "samurai" collides with 武士 "samurai; warrior"

Author action: **changed**, with your remedy. `words\侍.md:8` is now `quiz_exclusions: [武士]`.

- `evidence\word-quiz.txt:57` shows the exclusion, and lines 61-63 show the options 侍 can now draw: 剣 and 城 above a 670-word tie
  at score 5.
- `words\侍.md:29` now names 武士 ぶし with its JMdict gloss “samurai; warrior” (entry 1583680) and gives the historical sense of
  侍 さむらい: a warrior, especially a military retainer of a daimyo in the Edo period. That is JMdict entry 1314780 sense 1, which
  the Dictionary line (line 35) cites.
- The kanji card 侍 now excludes 士 and 武 as well (`kanji\侍.md:14`; reasons at line 41).
- 武士 can still appear as a wrong option for 諸侯 (`evidence\word-quiz.txt:2162`). `CHANGES.md` lists this under "Points the
  author judged acceptable": a samurai is not a feudal lord. Please check that judgment.

### C2: 侮る "look down on" overlaps 見下ろす

Author action: **changed**, with your remedy. `words\侮る.md:8` is now `quiz_exclusions: [見下ろす]` (`evidence\word-quiz.txt:741`).
Line 28 states the overlap: like 見下ろす, 侮る can express contempt, and 見下ろす also has a literal sense of looking down from a
higher position.

### C3: 補佐 overlaps 助手, 世話 and 手伝い

Author action: **changed**. `words\補佐.md:8` is now `quiz_exclusions: [援助, 助手, 手伝い, 世話, 手伝う, 助ける, 支える, 応援]`.

- 助手, 世話 and 手伝い are the three you named. 手伝う “to help with a task”, 助ける “help; save”, 支える “support; hold up” and
  応援 “support; cheering” were added in a later round, for the act-of-assisting sense (`evidence\word-quiz.txt:2101` shows all
  eight titles).
- Line 28 now gives the overlapping glosses instead of a nuance claim (see O4).
- The reverse pair 補佐→助手 is gone (`CHANGES.md`, "Word-quiz options"). 補佐's own options come from a 37-word tie at score 7
  (`evidence\word-quiz.txt:2105`), which includes 代理 and 兼任; `CHANGES.md` lists both as judged acceptable.

### C4: missing kanji exclusions (併/兼, 俊/傑 才, 佐/丞 援, 侯/殿)

Author action: **changed**. Every pair you named is now excluded, and the other reviews added more (see "Changes made for the other
reviews", item 1):

- `kanji\併.md:14`: `[合, 兼, 結, 並, 共, 協, 接, 括, 統, 斉]`; the reasons are at line 39.
- `kanji\俊.md:14`: `[秀, 英, 傑, 才, 優, 卓, 豪, 賢, 偉, 哲]`; reasons at line 37.
- `kanji\佐.md:14`: `[丞, 助, 援, 支, 副]`; reasons at line 40.
- `kanji\侯.md:14`: `[殿]`; the reason is at line 37 (殿 can mean “lord” as an honorific as well as a palace).

The ledger's new `kanjiQuizAudit.directExclusions` section holds the same rows. `tools\audit_n1_batch.py` now fails if a card's
`quiz_exclusions` differs from its ledger row (`evidence\audit-negative-kanji-exclusion.txt`). `checks\quiz-safety.txt` reports 0
errors and 0 warnings.

### C5: the untagged 諸侯 needs a row-specific justification

Author action: **not changed** (諸侯 remains the support word), **record added**.

- Ledger line 7 (`selectionReason`) states the rule as applied: a qualifying support word carries news1, ichi1, spec1 or gai1, and
  news2/spec2 do not qualify. It lists 俊英 (1340880), 侯 (1272630), 侯爵 (1272650) and 王侯 (1588830) as news2/spec2 only, and
  names 諸侯 as the batch's sole priority-tag exception.
- Ledger line 14 (`exceptionReason` on the 侯 row) is the row-specific justification. It now also records the comparison you asked
  for: 侯爵 would also need 爵, which has no card; 王侯 means “the king and his feudal lords”; 諸侯 “feudal lords; barons; princes”
  matches the card's feudal-lord sense. Check the glosses in `evidence\jmdict-cited-entries.xml`, and the absence of a 爵 card in
  the original packet's `titles\kanji-titles.tsv`.
- Not switched to 侯爵: it does not qualify either (news2/spec2), and its other kanji has no card.
- On the cards, `kanji\侯.md:33` labels 諸侯 “historical term, not an everyday word”, and line 37 says that JMdict marks it as
  historical and gives it no frequency tag. The 王侯 example line was removed from the kanji card.

Please judge whether this record is enough for the coordinator to accept the exception.

### C6: 倫's title "ethics; moral order" and the quiz-exclusion note

Author action: **changed**.

- The title is now “ethics; moral principles” (`kanji\倫.md:3`, `17`). “Ethics” is KANJIDIC2's first meaning. “Moral principles”
  renders Digital Daijisen's first sense, 人の守るべき筋道 (the original packet's `evidence\public-source\weblio-倫.txt`). Line 23
  says the same in plain words: “the path or principles people should follow”.
- The note at line 38 no longer explains a quiz decision. It contrasts 倫理 with 不倫, gives 五倫 ごりん, says that 伴 and 輩 share
  the companion sense, and names 徳 (“virtue”), 善 (“good; virtue”) and 義 (“righteousness”) as related moral concepts.

### C7: 不倫, the companion sense, and 大佐

Author action: **changed**.

- `kanji\倫.md:34` adds 不倫 ふりん “infidelity; an extramarital affair”. The gloss renders Digital Daijisen's 不倫 entry, which
  defines it as straying from morality and especially as a sexual relationship outside marriage (`evidence\weblio-不倫.txt`). JMdict
  1495370 (news1, nf18) is in Metadata (line 42).
- `kanji\倫.md:23` adds Daijisen's second sense, companions of the same standing, with 絶倫 ぜつりん “matchless; peerless” (entry
  1387000) and KANJIDIC2's “companion”. 比倫 is not added.
- `kanji\佐.md:23` adds Daijisen's officer-rank sense, and line 36 adds 大佐 たいさ “colonel; (navy) captain” (entry 1413740,
  news1, nf17).

### C8: "underestimate" is not a JMdict gloss of 侮る

Author action: **changed**. The title is now “look down on; make light of” (`words\侮る.md:4`, `11`). The example translations at
lines 17-18 now use “make light of”, and `kanji\侮.md:35` uses the new title. Two lines were already present and are unchanged:
`kanji\侮.md:30` glosses 侮る as “look down on; make light of”, and `words\侮る.md:32` notes that the examples take a person's
ability and a danger as the targets.

### C9: 併用's medical-safety framing

Author action: **partly changed**.

- The Distinctive-meaning sentence (`words\併用.md:32`) now gives only the JMdict gloss: combined use, using jointly or using at
  the same time.
- Example 1 (line 17, “Do not use this medicine together with other medicines.”) is kept as one everyday instruction. Example 2
  (line 18) is about methods, and line 15 names methods, tools and medicines as things one can use together.

Please say whether example 1 should still go.

### C10: filler in the Synonyms sections and the 佳 mnemonic

Author action: **changed**.

- 侍: the figurative sense moved out of Synonyms into Meaning (`words\侍.md:16`) and Distinctive meaning (line 33). Synonyms
  (line 29) now contrasts 侍 with 武士.
- 俵: Synonyms (`words\俵.md:28`) now gives the JMdict gloss of 袋 (entry 1411070). The counter sense ひょう is at line 32.
- The 佳 mnemonic is removed; `kanji\佳.md` has no mnemonic now. The 併 mnemonic is removed as well. 佐 keeps its
  labelled modern-shape mnemonic (`kanji\佐.md:25`), which you did not flag.

## Optional notes

### O1: short lines for 不倫 and 大佐

Author action: **changed**. See C7.

### O2: 合併 as an unlinked word on 併

Author action: **changed**. `kanji\併.md:35` adds 合併 がっぺい “merger; consolidation” (JMdict 1578970, ichi1/news1/nf03). The
batch's pinned JMdict families did not contain this entry, so a supplement packet adds it to the batch record:
`docs\n1-sources\batch-157-jmdict-supplement-selection.json` and `batch-157-jmdict-supplement.xml` in `snapshot\`.

### O3: the 補佐 Dictionary line should cite the sense number

Author action: **changed**. `words\補佐.md:34` now cites “sense 1”. The other single-sense entries got the same treatment:
`words\倫理.md:34` (1555390) and `words\諸侯.md:34` (1344250).

### O4: the 補佐/援助 nuance claims are not in JMdict

Author action: **changed**. The claims that 補佐 “often describes helping a person carry out a role” and that 援助 is “broader”
are removed. `words\補佐.md:28` now gives the glosses plus one sentence noting the overlap: 援助 and 補佐 both mean aid or
assistance; 助手 names an assistant; “[手伝い] can mean help or a helper; [世話] can mean care or assistance”; and these English
glosses overlap, though each Japanese word has distinct uses.

### O5: the baseline lint errors in 理 and 語

Author action: **changed** for 理, **not changed** for 語.

- 理: `kanji\理.md:31` adds the ことわり row (JMdict 2412900), labelled “kun, source-only here”. Line 26 introduces it, and line 46 adds
  a Metadata line.
- `checks\lint.txt` now shows 1 error, the unknown `phonetic` key in `kanji/語.md`. That file is outside the batch and unchanged.

## Limits answered

### L1: the "historical title" label for 内侍 was unverified

Author action: **changed** and **evidence added**.

- `kanji\侍.md:30` now gives JMdict's glosses “maid of honor; lady-in-waiting” (entry 1582520; JMdict also lists the spelling
  “maid of honour” and an obsolete reading ないじ), then “a historical court title” outside the JMdict citation.
- `evidence\kotobank-内侍.txt` holds three Kotobank extracts:
  - Digital Daijisen: the women officials of the palace office 内侍司;
  - Seisenban Nihon Kokugo Daijiten: places them under the ritsuryō system (令制で…);
  - Nipponica: describes the later period (平安後期以降…).
- Ledger line 83 records the same reason for keeping シ.

### L2: the selection policy is not in the packet rubric

Author action: **evidence added**. Ledger line 7 (`selectionReason`) in `snapshot\` states the rule the batch applied, and line 14
records the 諸侯 exception (see C5). Please judge C5 against that text.

### L3: the exclusion findings assume full-pool random and tag-fallback distractors

Author action: **evidence added**.

- Kanji meaning quiz: the app tries the card's curated distractors first (`evidence\QuizBuilder.kt:34`), stops adding at three
  wrong options (line 29), and only then reaches the rest of the pool, sorted by shared tags (lines 35-36). For every batch card,
  `checks\quiz-safety.txt` lists the three curated meaning options, and the “curated …: in pools” lines of
  `checks\reading-exposure.txt` show each curated card in the N1, All and Starter pools. The tag fallback is therefore not reached
  for the batch cards' own meaning questions. (The same file's prompt lines show the curated cards also fill every wrong slot of
  the batch cards' reading questions.)
- The batch kanji can still be fallback options on other cards' questions, and an exclusion declared on either card removes the
  pair both ways (`QuizBuilder.kt:26`). The exclusions therefore matter in both directions.
- Word quiz: `WordQuizBuilder.select` (`evidence\Words.kt:176`) adds curated distractors first (line 192) and then draws from the
  full word pool, sorted by a score from shared tags, word type and shared kanji (lines 193 and 197-199). `evidence\word-quiz.txt`
  ports this code and lists the options each batch word can draw.

## Changes made for the other reviews

The other two reviews asked for the changes below, and four later review rounds (r2-r5, GPT-family only, see `CHANGES.md` "Process
notes") added to them. Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **More kanji exclusions:**
   - 佳 `[美, 良, 善, 宜, 優, 俊, 傑, 秀, 英, 卓, 豪, 偉, 華]` (`kanji\佳.md:14`; reasons at line 39);
   - 侍 adds 武, 臣, 仕, 僕 and 兵 (line 41);
   - 侮 `[卑]` (line 40: KANJIDIC2 lists “despise” for 卑);
   - 俗 `[凡, 卑]` (line 38; the 俗語 note on that line keeps its first sentence, and its second sentence, on whether a term is rude,
     playful or neutral, was removed as unsourced);
   - 俵 `[袋]` (line 42);
   - 倫 `[伴, 輩, 徳, 義, 善]` (line 38);
   - 佐 adds 助, 支 and 副; 併 adds 結, 並, 共, 協, 接, 括, 統 and 斉; 俊 adds 優, 卓, 豪, 賢, 偉 and 哲.

   Please check that each excluded pair rests on a real sense overlap and that none is excessive.
2. **More word exclusions:**
   - 佳作 `[傑作, 名作, 作品, 制作]`;
   - 俵 `[袋, バッグ, 鞄]`;
   - 併用 `[使用, 利用, 使う, 用いる, 用, 用途]`;
   - 俗語 `[言葉, 単語, 語]`;
   - 俊足 `[速い]`;
   - 倫理 `[道徳, 善, 仁]`.

   `CHANGES.md` ("Word-quiz options") gives the six reverse pairs that these removed and the ties that changed.
3. **Secondary senses:**
   - 併's side-by-side sense shared with 並 (`kanji\併.md:23`);
   - 俗's lowbrow/vulgar sense and 風俗's sex-service sense (`kanji\俗.md:23`, `34`);
   - the companion sense of 倫 (C7).
4. **俊足:**
   - line 24 now explains how 俊 and 足 combine;
   - line 32 explains the gifted-person sense restricted to the spelling 俊足, citing Digital Daijisen's 俊足 and 駿足 entries on
     Kotobank (`evidence\kotobank-俊足.txt`, `kotobank-駿足.txt`).
5. **Labels:**
   - the batch cards' Readings rows no longer say “Not selected for questions.” or “source-only”;
   - 侮's あなず.る row now reads “older form of あなどる (Digital Daijisen via Weblio)” (`kanji\侮.md:31`, `40`);
   - 助 and 理 use the existing “kun, source-only here” label (`kanji\助.md:32-33`, `kanji\理.md:31`). `CHANGES.md` ("Labels") asks
     whether the batch should use it too.
6. **Removed common-word lines:** 王侯 on 侯 and 俊英 on 俊. Both carry only news2/spec2.
7. **Glosses instead of unsourced comparisons:**
   - 佳作's 制作 (`words\佳作.md:28`);
   - 倫理's 道徳, 善 and 仁 (`words\倫理.md:28`);
   - 俵's 袋 (C10).
8. **Distractors:** all ten sets changed after the author's own quiz-safety check. No reviewer asked for this; `CHANGES.md`
   ("Distractor choices") gives the reasons and the pairs the author judged acceptable. Please check that no new distractor is a
   defensible answer for its card.

9. **Wording tied to a source, or removed when it could not be:**
   - 佳: line 37 adds that JMdict records 佳い (よい) as a rarely used spelling (entry 1605820) that the card does not teach as a usual
     kun reading;
   - 佐: line 40 adds that JMdict records 佐ける (たすける) as a rare spelling of 助ける (entry 1344410);
   - 併: line 39 opens with JMdict's note that 併せる is a rarely used kanji form of 合わせる, though the sense “to do at the same time;
     to take (e.g. into consideration) together; to do in addition to” is written esp. 併せる when in kanji (entry 1284480), and ends
     with 併せて sense 2, “in addition; besides; at the same time” (entry 1506010);
   - 俊: line 23 now quotes 俊足's first JMdict sense, “swiftness of foot; fast runner” (was “a word whose common sense is ‘fast
     runner’”);
   - 侯: line 23 now calls 諸侯 a historical compound;
   - 俵: the ヒョウ row (line 29), line 40 and `words\俵.md:32` now say that ひょう is the only JMdict reading for the counter sense and
     that, for the noun 俵, JMdict tags たわら as common and also lists ひょう (entry 1583390). Line 40 replaces “The selected quiz
     reading is たわら …”;
   - 侍: `words\侍.md:29` gives the readings ぶし and さむらい (C1);
   - 助: the Notes line 45 now reads “The table marks source-only readings explicitly.” (was “The table selects readings; the metadata
     retains the additional source forms.”);
   - removed as unsourced: the second sentence of the 俗語 note (item 1), and the second sentence of `words\俊足.md:15`, “JMdict also
     records a sense meaning a gifted person for this spelling.” The sense stays at line 32, now tied to Daijisen (item 4).

Every other changed line is a distractor sentence or Metadata line that follows from the changes above, a Dictionary line or
併's Words line that adds JMdict entry ids to cite or compare (`kanji\併.md:34`, `words\佳作.md:34`, `words\侍.md:35`,
`words\俵.md:34`, `words\倫理.md:34`), a ledger or tooling line, or the regenerated `manifest.json`. `CHANGES.md` lists every changed line by file.
