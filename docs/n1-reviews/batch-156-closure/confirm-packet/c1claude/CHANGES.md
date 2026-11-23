# Batch 156 revision: what changed from c6afa163 to 395f5364

Revised snapshot: `395f5364` (full hash `395f53643988ba24f444a376187c803aa6794654`; also in `packet-manifest.json`). It is three
commits after the reviewed snapshot `c6afa16315d5a88b5045eeb85d429b8f7fd90b1f`: `7eaf5c24` (the review fixes), `2c206d8f` (the
distractor sets of four more cards, and new choices for two distractors that `7eaf5c24` had put on 仙 and 伎) and `395f5364` (the
new 甲乙 article's Dictionary line cites KANJIDIC2's records for both 甲 and 乙, since the article states 甲's on reading コウ).
`diffs\fix.patch` is the whole change from `c6afa163` to `395f5364`. Nothing is published.

- **Changed:** seven kanji cards (乙 亜 仙 伎 伏 伐 伴) and three word articles. The word article 乙 is deleted, the word article 甲乙
  is new, and 亜熱帯 and 仁 changed. **Unchanged:** the kanji cards 丹, 仁 and 伯; every existing kanji card, including the declared
  remark edit on 潜; every stroke file; and every other word article: 丹念, 仙人, 歌舞伎, 降伏, 伐採, 伯仲, 同伴, and the link edit on
  伯母さん.
- **Front-matter changes:**
  - `distractors` (line 13) on six cards:
    - 乙 `[箱, 卵, 鳩]` → `[王, 硬, 粗]`
    - 仙 `[麦, 皿, 筒]` → `[下, 供, 生]`
    - 伎 `[梅, 蛇, 炭]` → `[供, 食, 自]`
    - 伏 `[糸, 杯, 象]` → `[起, 座, 伸]`
    - 伐 `[絹, 鶏, 缶]` → `[保, 耕, 育]`
    - 伴 `[塩, 羊, 墨]` → `[迎, 離, 他]`
  - The word 仁 (line 8): `quiz_exclusions` gained 人物, 個人, 芯 and 中心. It is now `[善, 親切, 優しい, 道徳, 人類, 人間, 人物, 個人,
    芯, 中心]`.
  - The new word 甲乙 (lines 1-10): reading こうおつ; title "first and second; A and B; relative merit"; tags `[kango, noun,
    labels, comparison]`; `quiz_distractors: [丙]`; `quiz_exclusions: [優劣, 区別, 差, 比較, 相違, 対照, いちばん, 伯仲]`.
  - Nothing else in front matter changed. No kanji card's title, tags, readings, `quizOnyomi`, `quizKunyomi` or `quiz_exclusions`
    changed, and no front matter outside the batch changed.
- **The word article 乙 is replaced by 甲乙.**
  - **Why:** the reading quiz for the word 乙 (おつ) could offer 音 おと as a wrong option, and おと is an attested reading of the
    written form 乙.
  - **The new article's readings:** JMdict's only entry spelled 甲乙 (1280080) has one reading, こうおつ.
  - **乙 is still taught:** the kanji card links 甲乙 at lines 23, 31 and 38, and still names the word 乙 おつ and its JMdict entry
    (lines 23 and 31). It also still teaches おと (lines 10, 33, 42 and 53).
  - **No dangling references:** no file in `words\`, `kanji\`, `articles\` or `docs\` links `words/乙.md`.
  - **No learner impact:** `words/乙.md` was new in this batch and was never published, so no learner data refers to it.
- **Distractor sentences:** each card whose set changed has one distractor sentence. It now names the three cards with their
  titles and says that none has the card's meaning; it no longer groups the old distractors as "concrete things".
- **Wording:**
  - 亜:31: 亜流 is glossed without "epigone".
  - 仙:32: "ateji" is glossed.
  - 亜熱帯:29: "any of the three characters".
  - 仁:22: "discusses".
  - 仁:38: the "nucleolus" sense, and which senses can also be read にん.
- **Generated file:** `manifest.json` was regenerated. It is a generated index and outside the review.
- **Line numbers:**
  - Every hunk replaces one line with one line, so line numbers are the same before and after.
  - `words/乙.md` (43 lines) was deleted, and `words/甲乙.md` (43 lines) was added.
  - Line numbers below refer to the revised snapshot in this packet.

## Changed lines

| File | Changed lines | Change |
| --- | --- | --- |
| kanji 乙 | 13, 23, 31, 38, 58 | 13: distractors `[王, 硬, 粗]`. 23: the last sentence now reads "As a word, 乙 おつ first means “(the) second (party, rank, etc.); B (grade); the latter” (JMdict), and [甲乙](../words/甲乙.md) こうおつ pairs it with 甲: “first and second; A and B”." 31: the オツ row links 甲乙 as the word that establishes the reading, and adds "乙 alone is also a word read おつ — second rank; class B; stylish (JMdict entry 1182940)". 38: the Common words line is 甲乙 (was the word 乙). 58: "The meaning-quiz distractors are 王 (“king”), 硬 (“hard; stiff”), and 粗 (“coarse; rough; crude”); none means a second rank or stylish." |
| kanji 亜 | 31 | 亜流 ありゅう is "(inferior) imitator; poor imitation" ("epigone" removed). |
| kanji 仙 | 13, 32, 49 | 13: distractors `[下, 供, 生]`. 32: "ateji (kanji chosen for their sound, not their meaning)". 49: "The meaning-quiz distractors are 下 (“down, below”), 供 (“accompany, offer”), and 生 (“life, birth”); none means a hermit or an immortal." |
| kanji 伎 | 13, 50 | 13: distractors `[供, 食, 自]`. 50: "…are 供 (“accompany, offer”), 食 (“eat, food”), and 自 (“self, oneself”); none means skill or a performer." |
| kanji 伏 | 13, 55 | 13: distractors `[起, 座, 伸]`. 55: "…are 起 (“wake; rise”), 座 (“sit; seating”), and 伸 (“stretch; lengthen”); none means lying prostrate, lurking or yielding." |
| kanji 伐 | 13, 56 | 13: distractors `[保, 耕, 育]`. 56: "…are 保 (“protect; preserve”), 耕 (“till; plough”), and 育 (“grow up; raise”); none means felling trees or attacking." |
| kanji 伴 | 13, 53 | 13: distractors `[迎, 離, 他]`. 53: "…are 迎 (“welcome; greet”), 離 (“separate; detach”), and 他 (“other”); none means accompanying or a companion." |
| words 乙 | deleted | The whole article (43 lines, title "second rank; class B; stylish", 22 `quiz_exclusions`) is gone. |
| words 甲乙 | new, 1-43 | New article. Meaning (16), two original examples (18-23) and a note on them (25); How the kanji combine (29); Synonyms and antonyms (33, 35); Distinctive meaning (39, 41), including the かるめる note; Dictionary line (43). |
| words 亜熱帯 | 29 | "…not the historical origin of any of the three characters" (was "either character"). |
| words 仁 | 8, 22, 38 | 8: `quiz_exclusions` add 人物, 個人, 芯, 中心. 22: "This book discusses benevolence in Confucianism." 38: "JMdict also gives the senses "human", "kernel" and, in biology, "nucleolus"; only the kernel sense, the seed inside a fruit, can also be read にん." |

## Distractor choices

| Card (title) | Reviewed snapshot | Revised | Revised distractors' card titles | Starter cards |
| --- | --- | --- | --- | --- |
| 乙 (second rank; stylish) | 箱 卵 鳩 | 王 硬 粗 | king · hard; stiff · coarse; rough; crude | none |
| 仙 (hermit; immortal) | 麦 皿 筒 | 下 供 生 | down, below · accompany, offer · life, birth | all three |
| 伎 (skill; performer) | 梅 蛇 炭 | 供 食 自 | accompany, offer · eat, food · self, oneself | all three |
| 伏 (lie prostrate; lurk; yield) | 糸 杯 象 | 起 座 伸 | wake; rise · sit; seating · stretch; lengthen | none |
| 伐 (fell trees; attack) | 絹 鶏 缶 | 保 耕 育 | protect; preserve · till; plough · grow up; raise | none |
| 伴 (accompany; companion) | 塩 羊 墨 | 迎 離 他 | welcome; greet · separate; detach · other | none |

- **Principle:** the old sets were concrete objects (food, animals, containers, materials) set against abstract targets, so a
  learner could reject them by category. Each new set stays in the target's area:
  - rank and quality for 乙;
  - posture and movement for 伏;
  - looking after land and people for 伐;
  - meeting, parting and others for 伴.
- **仙 and 伎:** these take common Starter cards, so the curated options also apply in Starter practice sessions. 供 has the same 亻
  key as both targets.
- **Evidence:** every revised distractor was checked against the target's `quiz_exclusions`, and against every JMdict entry spelled
  with the distractor character alone. `evidence\distractor-senses.txt` lists those entries. `evidence\distractor-use.tsv` lists each
  distractor's own front matter and every card that uses it.
- **Titles:** distractor titles are quoted from the distractor cards' own `title:`, the text the app shows.

### Candidates replaced or rejected during the fix

None of these is in the revision. `evidence\distractor-use.tsv` (last section) and `evidence\distractor-senses.txt` hold the JMdict
entries.

| Candidate | For | Where | Reason |
| --- | --- | --- | --- |
| 父 “father” | 仙 | in `7eaf5c24` | JMdict 1497610 ちち sense 3 "God; Father" is close to the reason 仙 excludes 神 (an immortal pictured as a godlike being). |
| 達 “reach, plural suffix” | 伎 | in `7eaf5c24` | the 達 card teaches the sense "attain skill" (上達), which is the reason 伎 excludes 熟. |
| 行 “go” | 伎 | in `7eaf5c24` | No sense clash was found: JMdict 2270390 こう sense 2 "act; action" is a deed. It was replaced by 供 so that the set holds a 亻 card. |
| 末 “end; tip” | 乙 | draft only, never committed on this branch | JMdict 1525250 すえ "youngest child" matches the 児 exclusion (乙子 おとご). |
| 初 “first time; initial” | 乙 | considered, never committed | JMdict 2036160 うぶ "inexperienced; green; naive" is close to the 稚 and 幼 exclusions. |
| 敵 “enemy; opponent; rival” | 伴 | draft only, never committed on this branch | JMdict 1577915 かたき sense 3, archaic "spouse", is close to 伴's KANJIDIC2 meaning "consort" and to 伴侶 (1478430) "companion; partner; spouse". |

### Points the author judged acceptable (please check them)

- **伏/座:** 座 (“sit; seating”) is a different posture from lying face down. The word 土下座 どげざ, a kneeling bow with the head
  to the floor, is written with 座, but the 座 card's title is about sitting.
- **伏/起 and 伏/伸:** rising and stretching out are the opposite of lying low.
- **伴/迎:** the 伴 card excludes 送 because 送る can mean "to escort; to accompany". JMdict's 迎える (1253190) has no escorting or
  accompanying sense.
- **伴/他:** ほか "other; besides; in addition to" adds something; it does not accompany it.
- **乙/王 and 乙/粗:** a king is first, not second, and "coarse; rough; crude" is low quality, not the second rank or stylishness.
- **仙/生:** "life, birth" is not immortality. JMdict 2036160 (うぶ "inexperienced; naive") is spelled 初, 初心, 産 or 生, but 仙
  excludes no youth sense.
- **The 甲乙 word quiz:** the meaning tier (score 7, 8 words tied, 2 slots) includes 後者 "the latter" and 同格 "same rank;
  apposition". Neither is "first and second" or "relative merit", and 伯仲 "being evenly matched" is excluded.

### What the new sets change in the reading quiz (`checks\reading-exposure.txt`)

The kanji reading quiz takes its wrong options from the curated distractor cards' readings, then from a fallback. A curated card
that is not in the session's pool is skipped; the meaning quiz works the same way (`evidence\QuizBuilder.kt` line 34).

| Card | Reviewed snapshot (N1 / All stack; Starter practice session) | Revised |
| --- | --- | --- |
| 乙 | curated 箱 卵, deficit 1 (鳩 has no usable on reading), 39 drawable wrong options; Starter: fallback only, 8 drawable | curated 王 硬 粗, curated only, 4 drawable; Starter: fallback only, 8 drawable |
| 仙 | curated only, 3 drawable; Starter: fallback only, 23 drawable | curated only in all three pools, 8 drawable |
| 伎 | curated only, 4 drawable; Starter: fallback only, 5 drawable | curated only in all three pools, 8 drawable |
| 伏 | curated only, 4 drawable; Starter: fallback only, 16 drawable | curated only, 3 drawable; Starter: fallback only, 16 drawable |
| 伐 | curated 缶, deficit 2 (絹 and 鶏 have no usable on reading), 39 drawable; Starter: fallback only, 9 drawable | curated only, 3 drawable; Starter: fallback only, 9 drawable |
| 伴 | curated 塩 羊, deficit 1 (墨 has no usable on reading), 57 drawable; Starter: fallback only, 24 drawable | curated only, 3 drawable; Starter: fallback only, 24 drawable |

The totals are unchanged: 0 production hits, 0 padded-session hits, 10 latent collisions, 0 one-holder hits, and 0 more for
KANJIDIC2 name-only readings.

## Checks run on the revised snapshot (outputs in `checks\`)

- **`lint.txt`:** 0 errors, 1 warning (`words/潜る.md`: the Dictionary line cites no JMdict entry id); identical to the freeze.
- **`unittest.txt`:** 439 tests, OK.
- **`validate.txt`:** 0 errors.
- **`manifest.txt`:** rebuilding `manifest.json` leaves it unchanged and the tree clean.
- **`budget.txt` and `vocabulary.txt`:** informational. Retained bytes are 56,572,091 (352 more than at the freeze); vocabulary
  coverage is 3201/3539, as at the freeze.
- **`linkplan.txt`:** 10 new word articles (甲乙 instead of 乙), 11 changed word files, 1 expected and 1 added link pair, 0 problems.
  Apart from the 甲乙 line, identical to the freeze.
- **`kanji-remarks.txt`:** 10 new cards, 1 modified existing card (the remark edit on 潜), 0 problems. Apart from the command line,
  identical to the freeze.
- **`quiz-safety.txt`:** 0 errors, 0 warnings.
  - Every batch card's meaning options are its three curated titles.
  - The reading prompts 乙 オツ, 伐 バツ and 伴 ハン now take 3/3 wrong options from the distractors (2/3, 1/3 and 2/3 at the
    freeze).
  - The list of 11 existing cards that fall back is unchanged.
- **`reading-exposure.txt`:** see the table above.
- **`reading-options.txt`:**
  - 1 problem, as at the freeze: 伯's unlisted は "can be drawn" from 波, 派 or 破, a conservative over-report. 伯's curated
    cards 自, 物 and 毎 fill all three wrong slots, so the fallback is never reached, and `reading-exposure.txt` shows no hit for 伯.
  - The changed curated lines are 乙 (王 おう のう, 硬 こう, 粗 そ), 仙 (下 か げ, 供, 生), 伎 (供, 食, 自), 伏 (起 き, 座 ざ, 伸 しん),
    伐 (保 ほ, 耕 こう, 育 いく) and 伴 (迎 げい, 離 り, 他 た).
- **`evidence\word-quiz.txt`** (the word-quiz audit at `395f5364`; same tool as the original packet's `evidence\audits\word-quiz.txt`):
  - It reports 0 ATTESTED or too-few-candidate problems; the freeze had 1, the word 乙's 音 おと.
  - 甲乙's reading quiz offers two of the generated look-alikes ごうおつ, こおつ, こうおうつ and こうおず. Its corpus slot draws from a
    closeness tier of 9 words (九つ, 今月, 公立, 口実, 国立, 混雑, 穀物, 鉱物, 骨折); none is a reading of 甲乙.
  - 仁's meaning tier is now 1,409 tied words (1,413 at the freeze).
- **`evidence\corpus-attested.txt`** (every word in the All word stack, at `395f5364`; produced by
  `evidence\gen_corpus_attested.py` with the same audit's functions):
  - 112 words can still be offered, in their reading quiz, a wrong option that JMdict gives as a reading of the word's written form:
    93 only through generated look-alikes and 19 through other words' readings. At the freeze there were 113; the only row removed
    is the word 乙's 音 おと.
  - None of the 112 is a batch-156 word. They are existing words, and the remedy the initial reviews named (in the app's
    `ReadingOptions.build`) is outside this content revision.
- **`evidence\meta-scan.txt`:** apart from the command line, identical to the freeze. It shows 6 whole-run gaps (乙種, 亜麻, 仁術,
  仙骨, 酒仙, 伯母さん) and 4 part-of-run matches, all on unchanged lines.
- **JVM tests:** the Android JVM tests that read the real content were not run, as at the freeze (no JDK on this machine).

## Process notes

- **Sense scan:** after `7eaf5c24`, every JMdict entry spelled with a new distractor alone was read against the target card's
  exclusion reasons. That scan found the 父, 末, 初 and 敵 problems in the table above; each was replaced before `2c206d8f`.
- **The かるめる note:** the 甲乙 note says only what the sources show.
  - `evidence\甲乙-daijisen.txt` gives the Digital Daijisen entries かる‐める【上下／甲乙】 and こう‐おつ【甲乙】.
  - JMdict's only entry spelled 甲乙 (1280080) is read こうおつ.
  - The Daijisen extract ends partway into the next section of the Weblio page (難読語辞典), which is not cited.
- **Absence claims:** the 伎 card's "JMdict has no entry read わざおぎ" (unchanged line 34) was checked against the pinned JMdict.
  `evidence\wazaogi-scan.txt` (produced by `evidence\wazaogi_scan.py`) shows that no entry has that reading and none has a
  reading that starts with わざお.
- **JMdict entries:** `evidence\jmdict-cited-entries.xml` holds every JMdict entry cited by the changed text and the distractor
  notes, and the entries for words the changed text names without an entry number (仁's six `quiz_exclusions` for the human and
  kernel senses, the synonyms in the 甲乙 article and 1039110, the only entry read カルメル, which is "honeycomb toffee" and not the
  music term かるめる). It also holds the eight entries one initial review did not check against the pinned JMdict: 1466670, 1578730,
  1282860, 1268820, 1778760, 1357390, 1417780 and 1002570. The first seven were already in the original packet's
  `evidence\jmdict-families.xml`. 1002570 (お疲れ様) was not; it was cited only by the deleted word article 乙, and no revised file
  cites it.
- **The compound-sound-changes article:** `evidence\compound-sound-changes.md` is the article that `伐.md:31` and
  `words\亜熱帯.md:29` link to, and so do `潜.md:57` and `words\伐採.md:28`, which are unchanged since the freeze and are in the
  original packet's `snapshot\`. The article is unchanged since the freeze.
  - ねっ (ネツ) in 亜熱帯 and ばっ (バツ) in 伐採 are the small-っ change in "Small っ: gemination in a compound" (lines 26-49).
  - For ぷく (フク) in 潜伏 せんぷく, the "Small っ plus /p/" section (lines 51-63) names the h-row to p-row change
    (handakuon-ka, lines 56-57), but its example 失敗 has the /p/ after small っ; in 潜伏 it follows ん. The published 輩 card
    (batch 152; `evidence\輩.md:31`) links the article in the same way for ぱい in 先輩 せんぱい. Please judge whether the 潜
    link is adequate.
- **Checks:** the checks in `checks\` and the evidence audits were run on the committed revision `395f5364`.
