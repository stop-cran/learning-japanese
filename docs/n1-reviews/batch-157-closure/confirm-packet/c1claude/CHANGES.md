# Batch 157 revision: what changed from a5c6a0ff to cd5d75d1

Your report reviewed the frozen draft `a5c6a0ff`. The revised snapshot is `cd5d75d1`, 19 first-parent batch commits later. One more first-parent commit, `684d754c`, is a merge of `main` that touched no batch path: it removed 5,998 old review files under `docs/n1-reviews/`, added the index `docs/n1-reviews/README.md`, and linked it from `README.md` and `docs/n1-authoring-notes.md`. Its paths are left out of `diffs\` and listed in `evidence\merge-scope.txt`. Every commit in the range is signed: `evidence\verify-commit.txt` lists each first-parent commit and the merge's second parent `2bc61140`.

- **Changed:**
  - the ten batch cards 佐 佳 併 侍 侮 侯 俊 俗 俵 倫;
  - the reused kanji cards 助 (two Readings rows and one Notes line) and 理 (one Readings row, the Readings intro line and a Metadata line); their front matter is unchanged;
  - the ten new word articles 佳作 併用 侍 侮る 俊足 俗語 俵 倫理 補佐 諸侯 (諸侯 only on its Dictionary line);
  - the ledger `docs/n1-sources/batch-157-progress.json`;
  - a new JMdict supplement packet for entry 1578970 (合併): `batch-157-jmdict-supplement-selection.json` and `batch-157-jmdict-supplement.xml`;
  - `tools/audit_n1_batch.py`.
- **Unchanged:** `words/速い.md`, all stroke files, and the front matter of 助 and 理. 速い and 助 had a `quiz_exclusions` entry added during the fix and removed again later (see Process notes), so their net diff is empty or limited to the lines listed below.
- **Front-matter changes:** every batch card has new `distractors` and a longer `quiz_exclusions` list. 倫's title is now “ethics; moral principles” (was “ethics; moral order”). In the words, `quiz_exclusions` grew on every changed article except 諸侯, and 侮る's title is now “look down on; make light of” (was “look down on; underestimate”).
- **Distractor sentences:** each batch card's Notes now ends with one sentence that names its three distractors with their card titles.
- **Wording:** all other changed lines answer review findings or remove wording that the author could not tie to a source.
- **Generated file:** `manifest.json` is regenerated (contentVersion `00777806885a6934`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `kanji/佐.md` | 13–14 | distractors 左 差 査 → 母 友 子; quiz_exclusions [] → [丞, 助, 援, 支, 副] |
| | 23 | adds the Digital Daijisen officer-rank sense, with 大佐 たいさ “colonel; (navy) captain” |
| | 36 | new example: 大佐 たいさ (JMdict entry 1413740) |
| | 40 | replaces the old distractor note. It now says that 左, 差 and 査 share サ but differ in meaning, contrasts 佐 with 助 (Daijisen: supporting and helping from the side, as in 補佐; 助 is the character of 助ける), and glosses 丞, 援, 支 and 副 (entry 1500330). It also records 佐ける as a rare spelling of 助ける (entry 1344410) |
| | 42–44 | distractor sentence; Metadata now lists JMdict entries 1603460, 1344410, 1413740, 1500330 |
| `kanji/佳.md` | 13–14 | distractors 価 加 果 → 新 古 短; quiz_exclusions [美, 優] → [美, 良, 善, 宜, 優, 俊, 傑, 秀, 英, 卓, 豪, 偉, 華] |
| | deleted after 24 | the mnemonic line and the blank line after it are removed |
| | 37 | 佳作's two senses; KANJIDIC2 lists カ for this card; JMdict also records 佳い (よい) as a rarely used spelling, not taught here as a usual kun reading |
| | 39 | why each excluded kanji overlaps (美; 良 善 宜 with Daijisen's よい gloss; 優; 俊 傑 秀 英 卓 豪; 偉い entry 1155780; 華 entry 1194500) |
| | 41, 43 | distractor sentence; Metadata now lists JMdict entries 1189760, 1605820, 1155780, 1194500 |
| `kanji/併.md` | 13–14 | distractors 平 兵 閉 → 分 動 休; quiz_exclusions [合] → [合, 兼, 結, 並, 共, 協, 接, 括, 統, 斉] |
| | 23 | meaning line merged with the second sense shared with 並 (併記 へいき, 併存 へいぞん; JMdict also lists the spellings 並記 and 並存); the mnemonic is removed |
| | 30 | あわ.せる row: “Not selected for questions.” removed |
| | 34–35 | 併用 line gains “(JMdict entry 1506200)”; new line 合併 がっぺい “merger; consolidation” (entry 1578970, from the new supplement packet) |
| | 39 | JMdict marks 併せる as a rarely used kanji form of 合わせる but prefers it in kanji for the sense “to do at the same time; to take (e.g. into consideration) together; to do in addition to” (entry 1284480); why each excluded kanji overlaps; ends with KANJIDIC2 “collective” and 併せて sense 2 “in addition; besides; at the same time” (entry 1506010, esp. 併せて), which is close to 斉. Replaces the line that called 併用 “the more useful support word” |
| | 41, 43 | distractor sentence; Metadata now lists JMdict entries 1284480, 1506200, 1578970, 1506070, 1663430, 1506010 |
| `kanji/侍.md` | 13–14 | distractors 字 寺 次 → 父 母 子; quiz_exclusions [士] → [士, 武, 臣, 仕, 僕, 兵] |
| | 29–30, 32 | ジ and はべ.る rows: “Not selected for questions.” and “Source-only.” removed; シ row: 内侍 now gives JMdict's glosses “maid of honor; lady-in-waiting” (was “lady-in-waiting”; JMdict also lists the spelling “maid of honour”), then “a historical court title” outside the JMdict citation; “source-only.” is removed |
| | 41 | Notes: 侍る is usually written in kana and 内侍 is a historical court title; contrasts with 士, 武, 兵 (つわもの, entry 2822790), 臣, 仕 and 僕; Daijisen explains the ジ sense as serving beside a person of high rank |
| | 43–45 | distractor sentence (it also says the three are family members); Metadata adds entry 2822790 and the Kotobank 内侍 link |
| `kanji/侮.md` | 13–14 | distractors 舞 武 部 → 聞 話 会; quiz_exclusions [] → [卑] |
| | 29, 31 | ブ row: “Not selected for questions.” removed; あなず.る row now reads “あなずる — older form of あなどる (Digital Daijisen via Weblio).” |
| | 35 | 侮る example gloss: “look down on; make light of” (“underestimate” removed) |
| | 40 | Notes: あなずる as an older form of あなどる; 卑 is related, and KANJIDIC2 also lists “despise” among its meanings |
| | 42–44 | distractor sentence; Metadata adds the Daijisen 侮る Weblio link |
| `kanji/侯.md` | 13–14 | distractors 交 光 向 → 国 京 社; quiz_exclusions [] → [殿] |
| | 23 | “The historical compound [諸侯] …” |
| | 33 | 諸侯 example now “feudal lords; historical term, not an everyday word” (was “feudal lords; barons; princes”); the 王侯 line is removed |
| | 37 | 候補/侯補 note, plus: JMdict marks 諸侯 as historical and gives it no frequency tag; 殿 can mean “lord” as an honorific as well as a palace, while 侯 refers specifically to a rank |
| | 39–41 | distractor sentence; Metadata no longer lists entry 1588830 (王侯) |
| `kanji/俊.md` | 13–14 | distractors 春 瞬 旬 → 安 少 多; quiz_exclusions [秀, 英] → [秀, 英, 傑, 才, 優, 卓, 豪, 賢, 偉, 哲] |
| | 23 | the first JMdict sense of 俊足 is “swiftness of foot; fast runner” |
| | deleted after 33 | the 俊英 example line is removed |
| | 37 | 俊足 as a whole-word example (not a claim that 俊 alone means “fast”) and its JMdict “gifted person” sense; why each excluded kanji overlaps (偉, entry 1155780; Digital Daijisen explains 俊 as outstanding talent and intellect, which overlaps with 賢 and 哲) |
| | 39–41 | distractor sentence; Metadata lists JMdict entries 1340940 and 1155780 (1340880, 俊英, dropped) |
| `kanji/俗.md` | 13–14 | distractors 属 続 族 → 天 新 名; quiz_exclusions [] → [凡, 卑] |
| | 23 | adds the lowbrow/vulgar sense, and says that 風俗 refers in another sense to the sex-service industry |
| | 34 | 風俗 example: “manners; customs; public morals; also the sex-service industry in a separate sense (JMdict entry 1499960)” |
| | 38–40 | Notes: the 俗語 note keeps its first sentence; its second, “Whether a particular term is rude, playful or neutral depends on that term and its context.”, is removed as unsourced; 凡 and 卑 are added; distractor sentence |
| `kanji/俵.md` | 13–14 | distractors 表 票 評 → 田 土 木; quiz_exclusions [] → [袋] |
| | 29 | ヒョウ row: “Not selected for questions.” removed; “俵 ひょう is also listed for the counter sense” is now “JMdict also lists 俵 ひょう, the only reading for the counter sense” |
| | 40–44 | replaces “The selected quiz reading is たわら …”: JMdict lists ヒョウ in 土俵; for the standalone word 俵 it tags たわら as common and also lists ひょう, the only reading for the counter sense; JMdict glosses 俵 as “straw bag; sack; bale,” which overlaps with 袋's title; distractor sentence |
| `kanji/倫.md` | 3, 17 | title “ethics; moral principles” |
| | 13–14 | distractors 林 輪 臨 → 力 事 名; quiz_exclusions [] → [伴, 輩, 徳, 義, 善] |
| | 23 | 倫 as the path or principles people should follow; the Daijisen second sense “companions of the same standing” (絶倫 ぜつりん); KANJIDIC2 “companion” |
| | 34 | new example: 不倫 ふりん “infidelity; an extramarital affair”, an English rendering of Digital Daijisen's 不倫 entry (JMdict 1495370, in Metadata, glosses it “adultery; impropriety; (an) affair; immorality”) |
| | 38 | replaces “The meaning quiz excludes no character here …”: 倫理 and 不倫 as common compounds with distinct senses; 五倫 ごりん; 伴 and 輩 share the companion sense, while 徳, 善 and 義 are related moral concepts |
| | 40–42 | distractor sentence; Metadata lists JMdict entries 1555390, 1495370, 1387000, 1593605, plus the Daijisen 不倫 link |
| `kanji/助.md` | 32–33 | new Readings rows す.ける and すけ, both labelled “kun, source-only here” |
| | 45 | “The table marks source-only readings explicitly.” (was “The table selects readings; the metadata retains the additional source forms.”) |
| `kanji/理.md` | 26 | “This table includes ことわり as a source-only kun reading alongside the common on reading リ.” |
| | 31 | new Readings row ことわり, labelled “kun, source-only here” (entry 2412900) |
| | 45–46 | new Metadata line (this fixes the earlier lint error and warning on 理) |
| `words/佳作.md` | 8 | quiz_exclusions [傑作] → [傑作, 名作, 作品, 制作] |
| | 28, 34 | Synonyms: 傑作 and 名作 can both describe outstanding works; 佳作 also names an honorable mention; 作品 is any work; JMdict glosses 制作 first as “work (film, book)”; the sources line adds “compare entries 1297910 and 1374810” |
| `words/併用.md` | 8 | quiz_exclusions [] → [使用, 利用, 使う, 用いる, 用, 用途] |
| | 32 | “JMdict glosses 併用 as combined use, using jointly or using at the same time.” (replaces a sentence about medicine safety) |
| `words/侍.md` | 8 | quiz_exclusions [] → [武士] |
| | 16 | new line on the colloquial figurative sense |
| | 29, 33, 35 | 武士 ぶし with its gloss (entry 1583680), and the historical sense of 侍 さむらい, “a warrior, especially a military retainer of a daimyo in the Edo period” (entry 1314780 sense 1, cited at line 35); the figurative sense describes a person, not a warrior from a historical period; “compare entry 1583680” |
| `words/侮る.md` | 4, 11 | title “look down on; make light of” |
| | 8 | quiz_exclusions [] → [見下ろす] |
| | 17–18 | example translations: “Do not make light of your opponent’s strength.” / “He made light of the danger and did not prepare.” |
| | 28 | Synonyms: like 見下ろす, 侮る can express contempt; 見下ろす also has a literal sense of looking down from a higher position |
| `words/俊足.md` | 8 | quiz_exclusions [] → [速い] |
| | 15, 24 | “俊足 means swiftness of foot or a fast runner.” (line 15's second sentence, “JMdict also records a sense meaning a gifted person for this spelling.”, is removed; the sense is at line 32); 俊 conveys talent or excellence and 足 means foot, and together they form a word for swiftness on foot and a fast runner |
| | 32, 34 | the gifted-person sense, citing the Daijisen 俊足 and 駿足 entries (駿足's two senses are paraphrased, not quoted); sources: Kotobank 俊足 (530016) and 駿足 (530017) |
| `words/俗語.md` | 8 | quiz_exclusions [] → [言葉, 単語, 語] |
| `words/俵.md` | 8 | quiz_exclusions [] → [袋, バッグ, 鞄] |
| | 28, 32, 34 | 袋 gloss (entry 1411070); line 32 replaces “the selected word reading in this article is たわら”: the counter is read ひょう, and for the noun JMdict tags たわら as common and also lists ひょう; “compare entry 1411070” |
| `words/倫理.md` | 8 | quiz_exclusions [道徳] → [道徳, 善, 仁] |
| | 28, 34 | 道徳 “morals; morality”, 善 and the JMdict gloss of 仁; the Dictionary line cites sense 1 (the entry has one sense) and “compare entries 1454240, 1394250 and 1369620” |
| `words/補佐.md` | 8 | quiz_exclusions [援助] → [援助, 助手, 手伝い, 世話, 手伝う, 助ける, 支える, 応援] |
| | 28 | 援助 and 補佐 both mean aid or assistance; 助手 names an assistant; 手伝い and 世話 are glossed; these English glosses overlap, though each Japanese word has distinct uses |
| | 34 | the Dictionary line cites sense 1 (the entry has one sense) |
| `words/諸侯.md` | 34 | the Dictionary line cites sense 1 (the entry has one sense) |
| `docs/n1-sources/batch-157-progress.json` | 7, 14, 39–44, 48–70, 74–75, 80–83, 85–86, 88, 109–118, 126–134, 136 | selection reason (諸侯 exception); the 侯 row's `exceptionReason` (line 14) now also compares 侯爵, 王侯 and 諸侯; changed reused passages (助, 理), word and new kanji exclusion rows (`kanjiQuizAudit`), the supplement packet, reading dispositions, quiz audit, mechanical checks (line 127 now names manifest `00777806885a6934`), status |
| `docs/n1-sources/batch-157-jmdict-supplement-selection.json`, `…-supplement.xml` | all (new files) | JMdict entry 1578970 (合併) from the pinned snapshot |
| `tools/audit_n1_batch.py` | 628–632, 681–687, 768–770 | reads an optional `kanjiQuizAudit.directExclusions` ledger section; counts a reused kanji card's exclusion row among the reused-article decisions; fails with “Kanji exclusion ledger mismatch” when a card's `quiz_exclusions` differs from its ledger row (negative test in `evidence\audit-negative-kanji-exclusion.txt`) |

## Distractor choices

| Card (title) | Reviewed snapshot | Revised | Revised distractors' card titles | Starter cards |
|---|---|---|---|---|
| 佐 (aide; assistant) | 左 差 査 | 母 友 子 | mother; friend; child | all three |
| 佳 (beautiful; excellent) | 価 加 果 | 新 古 短 | new; old; short | all three |
| 併 (combine; join together) | 平 兵 閉 | 分 動 休 | minute, part; move; rest | all three |
| 侍 (samurai; retainer) | 字 寺 次 | 父 母 子 | father; mother; child | all three |
| 侮 (despise; scorn) | 舞 武 部 | 聞 話 会 | hear, ask; talk, speak; meet | all three |
| 侯 (marquis; feudal lord) | 交 光 向 | 国 京 社 | country; capital; company, shrine | all three |
| 俊 (talented; outstanding) | 春 瞬 旬 | 安 少 多 | cheap, peaceful; few, a little; many, much | all three |
| 俗 (customs; mundane) | 属 続 族 | 天 新 名 | heaven, sky; new; name | all three |
| 俵 (straw bag; bale) | 表 票 評 | 田 土 木 | rice field; earth, soil; tree, wood | all three |
| 倫 (ethics; moral principles) | 林 輪 臨 | 力 事 名 | power; matter, affair; name | all three |

- **Why they changed:** no reviewer asked for this. The author's own quiz-safety check (`evidence\freeze-quiz-safety.txt`, summary at line 34) failed the frozen draft with 29 errors and 1 warning:
  - nine cards' Notes did not name their distractors (lines 35–63);
  - the excluded pairs 春/旬 (俊) and 属/族 (俗) sat inside option sets;
  - 俊's option titles shared the word “season” (line 64).
  The same-sound sets also could not serve the reading question, because a card that shares the answer reading cannot be a wrong option there. The app therefore filled those slots from other cards (`evidence\freeze-reading-exposure.txt`; for 俗, 3 curated and 43 fallback options at line 124). Line 127 shows a production hit: しょく, which JMdict 1405100 records as an obsolete kana reading of 俗, could be offered by the curated distractor 続 (line 119) and by the fallback cards 植, 職, 色, 触 and 食.
- **Principle:** each new set holds three everyday Starter cards whose meanings are far from the batch card and whose readings do not collide with it. With these sets, all three wrong options of both the meaning question and the reading question come from the curated set in the N1 stack, the All stack and Starter practice sessions; the fallback is never consulted (`checks\reading-exposure.txt`, lines 13–162; `checks\quiz-safety.txt`).
- **Please judge:** all 30 distractors are Starter-level cards. Are any sets too easy to reject by category alone? Examples: family members for 佐 and 侍, sizes and amounts for 俊 (安 少 多), nature for 俵 (田 土 木), and everyday verbs for 侮 (聞 話 会).
- **Evidence:** `evidence\distractor-senses.txt` lists every JMdict entry spelled with each single distractor character, including the rejected candidates below. `evidence\distractor-use.tsv` gives each distractor's own front matter, its Starter tag and every card that already uses it.
- **Titles:** taken from the distractor cards' own front matter; they match the `quizAudit` labels in the ledger.

### Candidates rejected during the fix (never committed)

The reasons below were restated from `evidence\distractor-senses.txt` after the fact; the original notes were not saved.

| Candidate | For | Reason |
|---|---|---|
| 長 | 佐 | JMdict 1429740 ちょう sense 1 “head; chief; leader; elder” and 2251080 つかさ senses 1–2 “office; official” and “chief; head” sit next to 佐's officer-rank (大佐) and aide senses |
| 社 | 俗 | JMdict 2015400 しゃ sense 1 “company; firm; office; association; society” is close to the worldly sense of 俗 |
| 国 | 俗 | dropped together with 社; 1592250 senses 1, 2 and 4 (“country; state”, “region”, “home”) are not a strict clash |

### Points the author judged acceptable (please check them)

- 子 for 佐 and 侍: JMdict 2216440 し includes “viscount” (sense 2) and “founder of a school of thought (esp. Confucius); master” (sense 3). The card title is “child”.
- 友 for 佐: 1539980 “friend; companion; comrade”. A companion is not an aide.
- 父 for 侍: 1497610 sense 2 “father (e.g. of a discipline); pioneer (e.g. of field of research); founder” and sense 3 “God; Father”.
- 分 for 併: 1502860 ぶん “part; portion; share”. Dividing is the opposite of combining.
- 国, 京 and 社 for 侯: 1592250 sense 5 “province (of Japan)” [historical]; 1233320 “imperial capital”; 2015400 sense 3 “regional Chinese god of the earth”. They share a historical or political setting with a feudal lord, but none names a lord or a rank. 国 and 社 are the same cards rejected for 俗 above.
- 天 for 俗: 1438210 senses 1, 2, 3 and 5 (“sky”, “heaven”, “God”, “deva”). The sacred is the opposite of the mundane.
- 名 for 俗 and 倫: 1531330 sense 3 “fame; renown; reputation”.
- 田 for 俵: 1442730 “rice field”. Rice farming is the setting of a straw rice bale, but a field is not a bag.
- 事 for 倫: 1313580 sense 10 “you should …; I advise that you …; it's important to …”, which is near “what one should do”.
- 多 for 俊: KANJIDIC2 lists the kun reading まさ.る for 多 (まさる means to excel), though not among its meanings; the card title is “many, much”.
- Word quizzes (`evidence\word-quiz.txt`; options are drawn from the listed tie):
  - 諸侯 (line 2154) can draw 武士 “samurai; warrior” and 丞相 “grand chancellor (ancient China)”.
  - 補佐 (line 2105) can draw 代理 “representation; proxy” (JMdict 1412400 also has “deputy”) and 兼任.
  - 俗語 (line 1382) always draws three of 主語, 敬語, 熟語, 用語, 略語, 言語, including possibly 用語 “term; terminology; wording” and 熟語 “kanji compound; idiom”.
  - 倫理 (line 2082) can draw 原理 “underlying principle”.
  - 佳作 (line 14) always shows 作家 and 作者, plus one of twelve art words such as 絵画 “painting; pictorial art” or 芸術 “art; the arts”.
  - 併用 (line 40) can draw 実用 “practical use; utility”, 応用 “practical application” or 活用 “practical use; conjugation”.

### What the new sets change in the reading quiz (`checks\reading-exposure.txt`)

The reading question takes its wrong options from the card's curated distractors first and fills open slots from other cards; the meaning quiz works the same way (`evidence\QuizBuilder.kt` line 34). Frozen-draft lines are in `evidence\freeze-reading-exposure.txt`.

| Card | Frozen draft (N1 / All; Starter) | Revised (all three pools) |
|---|---|---|
| 佐 | 1 curated + 5 fallback; Starter 1 + 80 fallback (lines 12–14) | 5 curated, no fallback (line 13) |
| 佳 | 0 curated + 6 fallback; Starter 80 fallback; けい (KANJIDIC2 name reading) drawable in Starter (line 30); えい latent, but drawable if a Starter session borrows one holder card (lines 31, 33) | 3 curated (line 28); けい and えい latent only (lines 31, 34) |
| 併 | 2 curated + 30 fallback; Starter 12 fallback (46–48) | 5 curated (49) |
| 侍 | 6 curated; Starter 17 fallback (62–64); かみ latent (65) | 5 curated (65); かみ latent (68) |
| 侮 | 5 curated; Starter 4 fallback (80–82) | 7 curated (83) |
| 侯 | 39 fallback; Starter 18 fallback (94–96) | 5 curated (97) |
| 俊 | 63 fallback; Starter 31 fallback (109–111) | 3 curated (112) |
| 俗 | 3 curated + 43 fallback; Starter 14 fallback (124–126); **HIT** しょく via 続 and others (127) | 4 curated (127); しょく latent (130) |
| 俵 | 3 curated + 2 fallback; Starter 10 fallback (141–143) | 4 curated (146) |
| 倫 | 60 fallback; Starter 26 fallback (155–157) | 7 curated (160) |

Totals: frozen draft 1 production hit, 0 padded-session hits, 2 latent collisions and 1 one-holder padded hit (lines 163–164); revised 0, 0, 4 and 0 (lines 168–169). Your original packet's `mechanical-checks.md` (copied as `evidence\freeze-mechanical-checks.md`) had no reading-exposure section, so the しょく hit was not visible to you.

### Word-quiz options

- **Reverse pairs:** 813 (target, drawable listed word) pairs at line 2170 of `evidence\word-quiz.txt`, down from 819 at line 2164 of `evidence\freeze-word-quiz.txt`. The new word exclusions removed six pairs and added none:
  - 併用→用途 (freeze line 2260);
  - 俗語→単語 (2617) and 俗語→語 (2668);
  - 倫理→仁 (2792) and 倫理→善 (2802);
  - 補佐→助手 (2864).
- **Ties that changed:**
  - 佳作: last-slot score 8 with 作家, 作者 and 制作 (freeze line 14) → score 7, with 2 above and 12 tied (line 14).
  - 併用: 11 tied → 9 tied at score 6 (line 40).
  - 侮る: 611 → 610 tied at score 5 (line 745). 俵: 671 → 670 at score 5 (line 1400).
  - 倫理: in the frozen draft, 仁 at score 7 was offered in every quiz (freeze line 2075); now 11 tie at score 6 (line 2082).
- **Reading quiz:** 121 reverse pairs (line 2984). No ATTESTED problems (line 3107). Corpus tiers still include 傑作 and 制作 for 佳作 (line 32), 単語 for 俗語 (line 1392) and 使用 and 利用 for 併用 (line 53). These are reading options; the exclusions apply to meaning quizzes.

## Checks run on the revised snapshot (outputs in `checks\`)

- **quiz-safety:** 0 errors and 0 warnings for the ten cards. The frozen draft had 29 errors and 1 warning (`evidence\freeze-quiz-safety.txt`).
- **reading-exposure:** see the table above. **reading-options:** 0 problems. The frozen draft's output is `evidence\freeze-reading-options.txt`.
- **lint** (`lean\n1_batch_tool.py lint --base e2c25363`): 1 error and 44 warnings. The error is the pre-existing unknown `phonetic` key in `kanji/語.md`, outside the batch.
  - The frozen draft had 2 errors and 41 warnings. The 理 ことわり error and 理's missing-Metadata warning are fixed.
  - Four warnings are new only because 助 is now a changed file: three on `kanji/助.md` (not in the N1 source index; no quizOnyomi; no quizKunyomi) and one on `words/助かる.md` (Dictionary line cites no entry id).
- **audit** (`tools\audit_n1_batch.py --batch 157`): exit 0; 10 kanji, 10 new words, 8 changed reused articles, 17 reading dispositions, 27 dictionary families, manifest fresh (`00777806885a6934`).
- **budget:** retained 56,739,536 bytes, inflated 57,175,608 and local ZIP 36,459,991. The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **manifest:** rebuilding gives an identical file. **diffcheck:** clean from the batch base `e2c25363`. **validate:** 0 errors. **unittest:** 439 tests OK. **vocabulary:** 3201/3539.
- **link-targets.tsv:** every link on a changed line, resolved by the packet builder.
- **Also in `evidence\`:**
  - `meta-scan.txt`: no whole-run JMdict gaps; two part-of-run matches (佐.md:40 助け, 併.md:39 合わせ);
  - `corpus-attested.txt`: corpus-wide ATTESTED options in the word reading quiz;
  - `audit-negative-kanji-exclusion.txt`: the audit fails when a card's exclusions differ from the ledger, and passes again after the file is restored;
  - public-source snapshots: Weblio 不倫 and 侮る, Kotobank 俊足 and 駿足, and Kotobank 内侍 (Digital Daijisen, Seisenban Nihon Kokugo Daijiten and Nipponica extracts);
  - `verify-commit.txt`.
  - `Words.kt`: the app's word-quiz code at kanji-cards-android commit 91e1d4b5 (the current `main`). `word-quiz.txt` names it `evidence\app-code\Words.kt`; in this packet it is `evidence\Words.kt`. Since commit 4db1297c, used by earlier batches, the file has only gained `canInferWordMeaning`; `WordQuizBuilder.select` (line 176) and `ReadingOptions.build` (line 256) are unchanged.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Process notes

- **Other review rounds:** after your report, the author ran four more review rounds (r2–r5) on intermediate snapshots. Each round ran three parallel GPT-family reviews, one per facet (correctness, coverage, quiz behaviour). Their findings account for changes that no first-round report asked for; RESPONSE.md lists them under “Changes made for the other reviews”.
- **Re-signing:** five early fix commits were first signed with key AD3E63ADB89CAE86. They were re-signed with key 9D94B9D311BD26A7, which signed `a5c6a0ff` and every other commit in the range. Their trees are identical: 77ff93d9→2798cfbc, 77f56733→c8937669, 4bf9db0c→967b8603, f811f8eb→e2ef32e5, 970bb0dc→f1a69909.
- **Mirror exclusions:** the first fixes also declared 佐/助 on 助 and 俊足/速い on 速い. Both were removed because `docs/content-format.md` (lines 117–120 and 191–192) says a declaration on either card excludes the pair both ways.
- **Labels:** the batch cards no longer carry “Not selected for questions.” or “source-only” in Readings rows; quiz selection comes from front matter, and the ledger's reading dispositions give the reasons. The reused cards 助 and 理, however, use the “kun, source-only here” kind label; 98 other existing cards use “kun, source-only here” or “on, source-only here”. The ledger no longer marks 侍 シ or 侮 あなず.る as source-only. Please say whether the batch should use the same label.
- **併用 example 1:** “Do not use this medicine together with other medicines.” (line 17) is unchanged. Only the Distinctive-meaning sentence at line 32 was replaced.
