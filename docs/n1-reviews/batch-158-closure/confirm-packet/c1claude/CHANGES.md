# Batch 158 revision: what changed from 60d2cd5a to 6605a8b0

Your report reviewed the frozen draft `60d2cd5a`. The revised snapshot is `6605a8b0`, one signed commit whose parent is `60d2cd5a`. No merge of `main` is in the range. `evidence\verify-commit.txt` shows both signatures and the parent line.

- **Changed:**
  - nine batch cards: 偏 偽 傍 債 勲 匿 升 即 却;
  - six of the ten new word articles: 偏見 傍観 勲章 升 即座 師匠;
  - the ledger `docs/n1-sources/batch-158-progress.json`;
  - the pinned JMdict extract `docs/n1-sources/batch-158-jmdict-selection.json` and `batch-158-jmdict.xml`. They gain the 13 complete entries cited by the new text; nothing was removed.
- **Unchanged:**
  - the card 匠;
  - the word articles 偽造 負債 匿名 返却;
  - the ten existing articles that the frozen draft changed;
  - all stroke files;
  - every kanji card's title, readings metadata (`onyomi`, `kunyomi`, `quizOnyomi`, `quizKunyomi`) and Starter or JLPT tags.
- **Front-matter changes:**
  - 偽's distractors 犬 山 白 → 耳 山 白;
  - `quiz_exclusions` gains 側 on 偏 and 皮 on 匿;
  - the word 偏見 gains 意見 and the word 升 gains 腰掛け;
  - the word 升's title is now “measuring box” (was “measuring box; box seat”).
- **Wording:** every other changed line answers a review finding or adds a source-backed note on a reading that is not in the card's metadata.
- **Generated file:** `manifest.json` is regenerated (contentVersion `db1b983a19c5e487`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `kanji/偏.md` | 14 | quiz_exclusions [片, 傾, 傍] → [片, 傾, 傍, 側] |
| | 23 | gives readings and glosses for the Daijisen examples: 偏狭 へんきょう “narrow-mindedness” and 人偏 にんべん “the ‘person’ radical” |
| | 40 | the overlap note now also names 側 (“side”): KANJIDIC2 lists “side” among the meanings of 偏, and the meanings of 傍 also include “side” |
| | 42 | new note: Digital Daijisen gives the kun reading ひとえに, which Kanjipedia marks as outside the Joyo table (外); JMdict spells it 偏に, “wholly; solely; earnestly,” usually written in kana (entry 1510320); not in the card's metadata and not quizzed |
| | 46 | Metadata adds JMdict entries 1510370 (偏狭), 1643130 (人偏), 1510320 (偏に) |
| `kanji/偽.md` | 13 | distractors [犬, 山, 白] → [耳, 山, 白] |
| | 32 | にせ row: 偽物's gloss “spurious article; counterfeit” → “forgery; counterfeit; imitation” (JMdict 1577800) |
| | 44 | defines “source-only” before using it: a source lists the reading but no checked word example uses it |
| | 48 | distractor sentence names 耳 (“ear”) instead of 犬 (“dog”) |
| `kanji/傍.md` | 23 | gives readings and glosses for 傍系 ぼうけい “a collateral or subsidiary line” and 傍流 ぼうりゅう “an offshoot or something outside the mainstream” |
| | 46 | new note: Daijisen gives the on reading ホウ and lists 傍輩 ほうばい among its hard-to-read words; JMdict lists 傍輩 as a spelling of ほうばい, “comrade; friend; associate; colleague” (entry 1517130); Kanjipedia marks ホウ and そ.う as outside the Joyo table; neither is in the metadata or quizzed |
| | 52 | Metadata adds JMdict entries 1518840 (傍系), 1710750 (傍流), 1517130 (傍輩) |
| `kanji/債.md` | 23 | gives readings: 負債 ふさい, 債務 さいむ, 債権 さいけん “a claim”, 債券 さいけん “a bond”; adds “債権 and 債券 sound the same but are different words.” |
| | 29 | サイ row gains 債券 さいけん — bond; debenture (JMdict entry 1292070) |
| | 40 | the pairing note now cites JMdict's antonym marks on 債務 and 債権: “the debt owed by one side and the claim held by the other” (was “the claim held by the lender”) |
| | 42 | new note: Kanjipedia gives the kun readings か.り and か.し, both marked 外; not in the metadata, not quizzed |
| | 48 | Metadata adds JMdict entry 1292070 |
| `kanji/勲.md` | 23 | 元勲 gains its reading and gloss, げんくん “elder statesman”; the rank sense now reads “a rank or order of merit, as in 勲一等 くんいっとう, ‘order of the 1st class’” (was “a rank of merit, as in 叙勲”) |
| | 42 | new note: Daijisen gives the kun reading いさおし, which Kanjipedia, like いさお, marks 外; not in the metadata, not quizzed |
| | 46 | Metadata adds JMdict entries 1260770 (元勲), 1247200 (勲一等) |
| `kanji/匿.md` | 14 | quiz_exclusions [隠, 秘, 密, 潜, 伏] → [隠, 秘, 密, 潜, 伏, 皮] |
| | 40 | the overlap note adds 皮 (“skin; hide”), which shares only the English word “hide,” there meaning an animal skin |
| | 42 | new note: JMdict lists 匿す as a rarely used spelling of 隠す かくす (entry 1170650); Kanjipedia gives ジョク and かく.れる, marked 外; none is in the metadata or quizzed |
| | 46 | Metadata adds JMdict entry 1170650 |
| `kanji/升.md` | 23 | the 昇 interchange is limited to two senses: “Digital Daijisen also gives two more senses, rising and, from grain ripening, a peaceful, well-governed age; it notes that in these two senses 升 is used interchangeably with 昇.” (was: “the sense ‘rise,’ in which 升 is used interchangeably with 昇”) |
| | 30 | ます row: 升's gloss “measuring box; box seat” → “measuring box; also box seating at a theatre” |
| | 34 | support-word bullet: “measuring box; box seat” → “measuring box” (the word card's new title) |
| | 40 | the sentence about JMdict priority tags (news1, ichi1, spec1, gai1, news2, spec2) is deleted. The 枡/桝 kokuji sentence stays, and a note is added: Kanjipedia gives the kun reading のぼ.る, marked 外; not in the metadata, not quizzed |
| `kanji/即.md` | 23 | the Daijisen sense “being in close contact with something, as in 即位” → “attaching closely to something, read つく,” with 即位 そくい, accession to the throne, listed under it; the sense “that is; namely” is now given with its reading すなわち instead of the example 色即是空 |
| | 45 | new note: Kanjipedia gives the on reading ショク, marked 外; not in the metadata, not quizzed |
| `kanji/却.md` | 23 | the fourth sense's example is now 忘却 ぼうきゃく, “forgetting completely; oblivion” (JMdict); 冷却 is no longer cited |
| | 43 | defines “source-only” as on 偽.md:44 |
| | 49 | Metadata adds JMdict entry 1519260 (忘却) |
| `words/偏見.md` | 8 | quiz_exclusions [差別, 片寄る] → [差別, 片寄る, 意見] |
| | 28 | adds: [意見](意見.md) (いけん) is an opinion or view in general (JMdict entry 1156530); 偏見 is a view that leans to one side |
| | 34 | Dictionary line: compare entries 1291410, 1590420 and 1156530 |
| `words/傍観.md` | 17 | example translation: “You should not just stand by …” → “You must not just stand by …” (〜てはいけません) |
| `words/勲章.md` | 15 | adds: “Here ‘order’ means an order of merit, an honour awarded for service, not a command.” |
| `words/升.md` | 4, 11 | title and heading: “measuring box; box seat” → “measuring box” |
| | 8 | quiz_exclusions gains 腰掛け (“seat; bench”) |
| | 15 | drops the grid-square sense. JMdict's sense 2 is now explained (“a box, as in box seating at a theatre and similar places”), and 升席 ますせき, a tatami “box seat” for four people at sumo, kabuki and similar shows (JMdict entry 1706800), is added |
| | 18 | example translation: “a wooden measuring box” → “a wooden masu (measuring box)” |
| | 34 | Dictionary line: senses 1–3 → senses 1–2; compare entries 2248100 and 1706800 |
| `words/即座.md` | 24 | 座 “a seat or sitting” → “a seat or to sit” |
| `words/師匠.md` | 15 | “a stable master” → “a stable master, the head of a sumo stable” |
| | 18 | example translation glosses Rakugo: “Rakugo (traditional Japanese comic storytelling) performers …” |
| `docs/n1-sources/batch-158-progress.json` | 29 | `selectionReason`: 升 now takes the rule's untagged route, with the row-specific justification in its support mapping |
| | 132 | 升 `exceptionReason`: the row-specific justification (quoted in full in your RESPONSE.md) |
| | 261–262, 336–337 | word exclusion rows: 偏見 gains 意見; 升 gains 腰掛け |
| | 375–376, 434–435 | kanji exclusion rows: 偏 gains 側; 匿 gains 皮 |
| | 931, 936 | 偽's quiz-audit row: 犬 “dog” → 耳 “ear” |
| | 1053 | `batchAudit`: 73 → 86 complete JMdict families |
| | 1062 | `status`: “Candidate under independent review: first-round fixes applied; not published.” |
| `docs/n1-sources/batch-158-jmdict-selection.json`, `batch-158-jmdict.xml` | 13 ids added | 1510370 1643130 1510320 1518840 1710750 1517130 1292070 1260770 1247200 1170650 1519260 1156530 1706800, complete entries from the pinned snapshot |

## Distractor choices

| Card (title) | Reviewed snapshot | Revised | Revised distractors' card titles | Starter cards |
|---|---|---|---|---|
| 偽 (fake; false) | 犬 山 白 | 耳 山 白 | ear; mountain; white | all three |

- **Why it changed:** JMdict 1258330 いぬ sense 4 is “counterfeit; inferior; useless; wasteful” (`evidence\distractor-senses.txt`), so the sentence “none means fake or false” was not true of 犬.
- **耳:** JMdict 1317170 みみ has five senses: ear; hearing; ear (for music, etc.); edge, crust, heel, selvedge; and ear (of a pot, jug, etc.), handle. None is near “fake.” Its readings ジ and みみ do not collide with 偽's ギ, カ, いつわ.る, にせ or いつわ.り.
- **Shared distractor:** 耳 now serves three batch cards: 偏, 偽 and 升 (`evidence\distractor-use.tsv`, line 6). Each card's quiz draws its own set.
- **Reading quiz:** curated 耳 山 白 fill all three wrong slots in every outcome in the N1 stack, the All stack and Starter practice sessions; the fallback is never consulted (`checks\reading-exposure.txt`). No other card's distractors changed.

### Points the author judged acceptable (please check them)

- **債, line 23:** “collecting what one has lent, as in 債権” paraphrases Digital Daijisen's sense 2 of 債, 「貸しを取り立てること」 (the original packet's `evidence\public-source\weblio-債.txt`). JMdict 1292080 glosses 債権 “credit; claim”.
- **升 seating words:** 席 “seat”, 座席 “seat; seating” and 客席 “audience seating; audience” are not excluded from the word 升.
  - None of them is among the 669 candidates at or above 升's last-slot score of 5 (`evidence\word-quiz.txt`, lines 1697–2365; the score summary is line 1696). None of them carries 升's `wago` tag (席 and 客席 are `kango`; 座席 is tagged noun, transport, places).
  - No reverse pair shows 升 in their quizzes.
  - 腰掛け, which was in the tie (the original packet's `evidence\audits\word-quiz.txt`, line 2216), is now excluded.
- **Reading-options problems:** `checks\reading-options.txt` still reports two problems (lines 43 and 130), the same as in the reviewed snapshot.
  - The full-pool fallback for 傍's on prompt ボウ could offer そう, and Kanjipedia gives そ.う as a kun reading outside the Joyo table.
  - The full-pool fallback for 即's on prompt ソク could offer しょく, and Kanjipedia gives ショク outside the Joyo table.
  - In every shipped pool the curated distractors fill all three slots, so the fallback is never consulted. `checks\reading-exposure.txt` reports 0 production hits and 0 padded-session hits.
  - The two readings are now named on the cards as not quizzed (傍.md:46, 即.md:45).
- **“外” notes:** the new reading notes cite the Kanjipedia “outside the Joyo table” marks (the original packet's `evidence\public-source\kanjipedia.json`) and Daijisen for ひとえに, ホウ/傍輩 and いさおし (`weblio-偏.txt`, `weblio-傍.txt`, `weblio-勲.txt`).

### Word-quiz options

- **偏見** (`evidence\word-quiz.txt`, lines 8–18): 意見 “opinion” is gone from the option set. Now 4 words tie at score 6: 拝見, 見学, 見当 and 見物 (was 5, including 意見).
  - The reading-quiz reverse pair 偏見→意見 (line 3608) remains. It is a reading look-alike; exclusions apply to meaning quizzes.
- **升** (lines 1690–1700): the title is now “measuring box” and 腰掛け is excluded. 俵 scores 7, and 668 words tie at score 5 (was 669).
- **Reverse pairs:** 1128 meaning-quiz pairs (line 2478) and 61 reading-quiz pairs (line 3607), the same counts as at the reviewed snapshot.
- **Reading quiz:** 0 ATTESTED or too-few-candidate problems (line 3670).

## Checks run on the revised snapshot (outputs in `checks\`)

- **quiz-safety:** 0 errors and 0 warnings for the ten cards. The only change from the reviewed snapshot is 偽's options (dog → ear).
- **reading-exposure:** 0 production hits, 0 padded-session hits and 4 latent collisions, as at the reviewed snapshot. **reading-options:** 2 problems, the two described above; exit 1.
- **lint** (`lean\n1_batch_tool.py lint --base ad1694c1`): 4 errors and 59 warnings, the same output as at the reviewed snapshot.
  - The errors are on existing cards outside the batch: 師 いくさ; 観 み.る and しめ.す; 負 ま.かす. Each is a metadata reading without a Readings row.
- **audit** (`tools\audit_n1_batch.py --batch 158`): exit 0.
  - Counts: 10 kanji, 10 new words, 10 changed reused articles, 30 reading dispositions, 86 complete JMdict families (was 73).
  - The manifest is fresh (`db1b983a19c5e487`).
- **budget:** retained 56,811,507 bytes, inflated 57,247,579 and local ZIP 36,498,222. The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **manifest:** rebuilding gives an identical file.
- **diffcheck:** clean from the batch base `ad1694c1`.
- **validate:** 0 errors.
- **unittest:** 439 tests OK.
- **vocabulary:** 3201/3539.
- **link-targets.tsv:** every link on a changed line, resolved by the packet builder.
- **Also in `evidence\`:**
  - `word-quiz.txt`, `distractor-use.tsv`, `distractor-senses.txt`, `corpus-attested.txt` and `meta-scan.txt`, regenerated at the revised snapshot;
  - `support-selection.json`: the selection policy statement and support mappings at the revised snapshot;
  - `rule-7058679348.md`: the text of the issue #60 rule comment that governs support-word selection;
  - `verify-commit.txt`;
  - `selection-order.tsv`: the frozen source rows 1–140 (`docs\n1-sources\source-index.json`) with KANJIDIC2 grade, Joyo or name-use class, whether a card exists at the base `ad1694c1`, and B158 membership. The first ten Joyo rows with no card at the base are this batch;
  - `QuizBuilder.kt` and `Words.kt`: the app's kanji-quiz and word-quiz code. `word-quiz.txt` names the latter `evidence\app-code\Words.kt`; in this packet it is `evidence\Words.kt`.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Process notes

- **One commit:** the revision was built as one commit and amended in place several times before this packet. Each version was signed. Only `6605a8b0` is reviewed here.
- **Last two amends:**
  - The last content amend removed “literary” from 升.md:23. Daijisen does not label those two senses literary.
  - The final amend changed only the commit message, so that the message no longer says “literary”; the tree is identical.
