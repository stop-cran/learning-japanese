# Batch 159 revision: what changed from 1a9bb910 to 5c04be73

Your report reviewed the frozen draft `1a9bb910`. The revised snapshot is `5c04be73`, one signed commit whose parent is `1a9bb910`. No merge of `main` is in the range. `evidence\verify-commit.txt` shows both signatures and the parent line. The tables below cover the whole range: 26 files.

- **Changed:**
  - five batch cards: 厘 又 叔 吟 呈;
  - the frozen one-line additions to two existing cards, 太 and 官;
  - the frozen draft's one-line addition to the existing card 聞 (a link to 又聞き) is removed, so `kanji/聞.md` is again identical to the batch base `2787e43b`;
  - all nine remaining new word articles. Each gains a Digital Daijisen link on line 34, and 伯叔 厘 吟味 呉服 太后 官吏 also change text;
  - the new word article 又聞き is deleted;
  - two existing kana-headed articles that the frozen draft did not touch, また and または: line 24 of each now links the 又 card;
  - the repository audit `tools/audit_n1_batch.py` and its tests `tools/test_audit_n1_batch.py`;
  - the ledger `docs/n1-sources/batch-159-progress.json`;
  - the pinned JMdict extract `docs/n1-sources/batch-159-jmdict-selection.json` and `batch-159-jmdict.xml`. Two entries are removed: 1442420 (伝聞), cited only by the deleted 又聞き, and 2025400 (又ね, read またね), cited only by the old 又 exception reason. Nothing was added; 87 complete JMdict families remain (was 89).
- **Unchanged:**
  - the cards 叙 吉 后 吏 呉;
  - the frozen one-line additions to the existing cards 不 伯 味 情 服 贈;
  - all stroke files;
  - every kanji card's title, `onyomi`, `kunyomi`, `quizOnyomi`, distractors and tags. The only readings-metadata change is 又's `quizKunyomi`.
- **Front-matter changes:**
  - 又: `quizKunyomi` [また-] → [また];
  - 吟: `quiz_exclusions` gains 検 審 査 調 究 研;
  - the word 吟味: `quiz_exclusions` gains 試験 and 確認.
- **Wording:** every other changed line answers a review finding.
- **Generated file:** `manifest.json` is regenerated (contentVersion `92143d996fc2aff4`; was `6d497dcb6f21d7d3`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot. `diffs\changed-lines.txt` has the old and new text of every changed line.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `kanji/厘.md` | 42 | 分 ぶ “is the fractional unit ten times larger” (was “the next larger fractional unit”), and adds “while 厘 is one-hundredth, including 0.3 mm as one-hundredth of a sun” |
| `kanji/又.md` | 12 | `quizKunyomi` [また-] → [また] |
| | 23 | links [又](../words/また.md) and [又は](../words/または.md). The senses of また are quoted one by one (“again,” “also,” “on the other hand,” “and; in addition” and “or; otherwise”) instead of the run-on “and, or or”. Adds “so the linked articles are headed in kana and show 又 and 又は as other spellings”. 又聞き and 又貸し are now unlinked examples of the prefix |
| | 30 | また row: 又は is listed first, and both 又は and 又 are linked; “Not selected for questions here.” is removed, because また is now the quizzed kun reading |
| | 31 | また- row: 又聞き is unlinked, and the row adds “Not selected for questions here.” |
| | 36–38 | Common words: linked 又は and 又 come first; 又聞き is unlinked |
| | 48 | the distractor sentence quotes the meanings: none means “again,” “also” or “or.” |
| `kanji/叔.md` | 39 | adds: “The Joyo table gives 伯叔 as its only example word for シュク; its readings おじ for 叔父 and おば for 叔母 are whole-word special readings, not readings of 叔 alone.” |
| `kanji/吟.md` | 14 | `quiz_exclusions` [詩, 歌, 謡, 句] → [詩, 歌, 謡, 句, 検, 審, 査, 調, 究, 研] |
| | 42 | the overlap note adds the six cards with their titles, which “overlap with the sense of examining something closely, as in 吟味” |
| `kanji/呈.md` | 40 | 呈する's JMdict glosses are quoted in full: “to present; to offer,” “to show; to display; to exhibit” and “to assume (e.g. a shape)” (entry 2012430; was “to show; to assume (a shape)”) |
| `kanji/太.md` | 38 | the 太后 line adds “(here 太 is added to an honored person's title; it does not mean “thick”)” |
| `kanji/官.md` | 37 | the 官吏 line adds “(dated)” |
| `kanji/聞.md` | (old 39) | the frozen draft's line “- [又聞き](../words/又聞き.md) またぎき — hearsay; learning by hearsay” is removed |
| `words/また.md` | 24 | “又 is a recognized spelling” → “[又](../kanji/又.md) is a recognized spelling” |
| `words/または.md` | 24 | “又は is another spelling” → “又は, written with [又](../kanji/又.md), is another spelling” |
| `words/又聞き.md` | deleted | the whole article (its old text is in `diffs\fix.patch` and `diffs\changed-lines.txt`) |
| `words/伯叔.md` | 15 | rewritten: Digital Daijisen's two senses are numbered, “(1) older and younger brothers; (2) the older and younger brothers of one's father or mother, that is, 伯父 and 叔父, one's uncles”; JMdict's gloss follows; adds “Both examples below use sense 2.” |
| | 24 | rewritten: 伯 “stands for the older” and 叔 “for the younger”, applied to both Daijisen senses (兄と弟, and a parent's older and younger brothers, 伯父 and 叔父), with JMdict's note on 伯父 and 叔父 (entry 1607070). The frozen line started from “an uncle or aunt” |
| | 32 | adds “Neither sense covers aunts (伯母 and 叔母).” |
| `words/厘.md` | 28 | 分 “is the next larger unit” → “is ten times larger … so one 分 equals ten 厘” |
| `words/吟味.md` | 8 | `quiz_exclusions` gains 試験 and 確認 |
| | 24 | rewritten: 吟 “can mean reciting poetry, but here it has its sense of examining contents closely: Digital Daijisen lists 吟味 under that sense of 吟.” Reciting a poem and savoring its flavor is named as the original meaning, JMdict sense 4 (archaic) and Daijisen sense 3 |
| `words/呉服.md` | 18 | translation: “I chose an obi, the long sash tied around the waist over a kimono, at the department store's kimono-fabric counter.” (was “… an obi in the department store's kimono section”) |
| `words/太后.md` | 15 | adds a plain-terms sentence from Daijisen: 皇太后 is the empress of the previous emperor, or one who is also the current emperor's birth mother, and 太皇太后 is the empress of the emperor two reigns back |
| `words/官吏.md` | 18 | example 2: 汚職をした官吏が処分されました。 → 歴史の本で、汚職をした官吏の話を読みました。 — “I read about a corrupt government official in a history book.” |
| `words/` 不吉 伯叔 厘 叙情 吟味 呉服 太后 官吏 贈呈 | 34 | the Dictionary line adds the Digital Daijisen entry, linked on kotobank.jp, e.g. `[Digital Daijisen, 吟味](https://kotobank.jp/word/%E5%90%9F%E5%91%B3-54502)` |
| `tools/audit_n1_batch.py` | 60–67 | new `support_spelling()`. Without a `spelling` field a mapping uses the headword, as before. With one, it is accepted only when the article is kana-headed (word equals reading, no `kanji:` list) and the spelling contains the kanji and appears in the article text |
| | 715–722 | the support check uses that spelling for the JMdict lexical match and reads the article text once |
| `tools/test_audit_n1_batch.py` | 4, 129–153 | five tests: the headword default; a kana-headed article that teaches the spelling; and rejection of a kanji-headed article, of a spelling absent from the article, and of a spelling without the mapped kanji |
| `docs/n1-sources/batch-159-progress.json` | 29 | `selectionReason`: 又 is supported by the existing kana-headed articles または (spelling 又は, ichi1/news1) and また (spelling 又) under point 2 of the rule; three rows (叔 后 吏) keep the untagged route |
| | 45–67 | 又's support mappings: または (entry 1524990, tags ichi1/news1, spelling 又は) and また (entry 1524930, spelling 又, with a note that only the reading また carries ichi1/news1, so this mapping is recorded as untagged). They replace 又聞き and its `exceptionReason` |
| | 78 | 叔 `exceptionReason`: the tags are on the spellings 叔父 and 叔母, whose tagged readings are the whole-word readings おじ and おば; しゅくふ and しゅくぼ carry no priority tag; an article headed 叔父 or 叔母 would teach おじ or おば; 伯叔 is the Joyo table's only example for シュク |
| | 175–179 | required reciprocal pairs: 又 ↔ または and 又 ↔ また (was 又 ↔ 又聞き) |
| | 233, 253 | the recorded additions to 官 (“(dated)”) and 太 (the bridge clause) |
| | (old 231–235) | the recorded addition to 聞 is removed |
| | 255–263 | the changes to または and また are recorded as reused-article changes |
| | (old 251–258) | 又聞き's word-exclusion row is removed |
| | 321–323, 420–426 | exclusion rows: 吟味 gains 試験 and 確認; 吟 gains 検 審 査 調 究 研 |
| | 483–489, 495–500, 507 | reading dispositions: また selected (article または); また- not selected (又聞き and 又貸し kept for reference); また.の- reason updated |
| | 707 | quiz projection: 又 `quizKunyomi` また |
| | 942–944, 946 | `batchAudit`, `unitTests`, `n1Lint` and `quizSafety` texts updated to the checks below |
| | 951 | `status`: the 叔, 后 and 吏 untagged-support exceptions and the kana-headed 又 support remain subject to review |
| `docs/n1-sources/batch-159-jmdict-selection.json`, `batch-159-jmdict.xml` | 2 ids removed | 1442420 and 2025400 |

## Distractor choices

None changed. 又's reading quiz now prompts また instead of また-. Its curated distractors 北 国 男 (readings きた, くに, おとこ, お) fill all three wrong slots in every outcome in the N1 stack, the All stack and Starter practice sessions; the fallback is never consulted (`checks\reading-exposure.txt`, lines 24–43).

### Points the author judged acceptable (please check them)

- **又's support words:**
  - 又 is now supported by two existing articles, `words/または.md` (jlpt 4, “or; either alternative”) and `words/また.md` (jlpt 5, “again; in addition”). Point 2 of the rule (`evidence\rule-7058679348.md`) puts an existing article, “including a kana-headed one”, first.
  - または's JMdict entry 1524990 carries ichi1/news1 on both the spelling 又は and the reading または. For また (entry 1524930), only the reading また carries ichi1/news1; the spelling 又 has no tag, so the ledger records that mapping as untagged, with a note. The Joyo table's examples for 又 are 又 and 又は (`evidence\joyo\p145.txt`).
  - Their headwords are kana, so their `kanji:` lists cannot name 又: `tools/validate.py` rejects a `kanji:` entry that does not occur in the headword. lint therefore reports two new warnings on `kanji/又.md` (its また examples do not list 又). The audit and quiz-safety checks accept the support through the ledger spellings 又は and 又.
- **吟's exclusion scope:** the six added cards have titles that name examining or investigating: 検 “inspect; examine; check”, 審 “examine; judge; trial”, 査 “investigate; inspect”, 調 “investigate; tune”, 究 “investigate thoroughly” and 研 “polish; study closely”.
  - Not excluded: 診 “diagnose; examine medically”, 偵 “spy; covert investigation”, 試 “test; try”, 験 “test; verify”, 察 “observe; infer”, 鑑 “model; appraise” and 覧 “look over; peruse”. Each names a narrower activity (medical, covert, trial, observation, appraisal, reading) than 吟's “examining contents closely”.
  - 吟's curated distractors 二 自 社 fill all three slots in every shipped pool (`checks\quiz-safety.txt` line 16, `checks\reading-options.txt` line 108), so these exclusions matter only in fallback or custom pools.
- **吟味 is still drawable** in these meaning quizzes (`evidence\word-quiz.txt`):

  | Line | Word quizzed | Score |
  |---|---|---|
  | 943 | 審判 “judgment; referee; umpire” | 5, tie of 8 |
  | 944 | 対照 “contrast; comparison against” | 9, tie of 30 |
  | 967 | 批評 “critique; review” | 5, tie of 394 |
  | 974 | 探偵 “detective; secret investigation” | 7, tie of 304 |
  | 985 | 断定 “definite judgment; assertion” | 9, above the last slot |
  | 994 | 比較 “comparison” | 5, tie of 395 |
  | 1001 | 測定 “measurement; measuring” | 9, tie of 27 |
  | 1020 | 研究 “research” | 5, tie of 381 |
  | 1049 | 観察 “observation” | 5, tie of 371 |
  | 1050 | 観測 “observation; prediction” | 7, tie of 262 |
  | 1054 | 評価 “assessment; appraisal” | 5, tie of 22 |
  | 1066 | 重視 “attaching importance to” | 5, tie of 4 |

  The author judged that none of these words would be glossed “close examination; careful selection”, so 吟味 is not a second defensible answer in any of them.
- **Digital Daijisen links in earlier batches:** the B156–B158 word articles do not link their Daijisen entries either (B157's 俊足 is the only one that does). That backfill (29 articles) is outside this batch's diff; it will be offered to the owner as a separate follow-up.

### Word-quiz options

- **吟味** (`evidence\word-quiz.txt`, lines 216–252): the option set is unchanged: last-slot score 9, with 推定 above it (score 11) and 29 words tied at 9. Neither 試験 nor 確認 was in it.
  - The two reverse pairs 吟味 → 確認 and 吟味 → 試験 (the original packet's `evidence\audits\word-quiz.txt`, lines 1189 and 1223) are gone.
- **又聞き** no longer appears anywhere in the file.
- **Reverse pairs:** 1019 meaning-quiz pairs (line 322; was 1173) and 93 reading-quiz pairs (line 1342; was 96).
  - The 154 meaning pairs removed are the 152 in which 又聞き was drawable, plus 吟味 → 確認 and 吟味 → 試験.
  - The 3 reading pairs removed are 又聞き's (shown for 周り, 紫 and 聞こえる).
- **Reading quiz:** 0 ATTESTED or too-few-candidate problems (line 1437).

## Checks run on the revised snapshot (outputs in `checks\`)

- **quiz-safety:** 0 errors and 0 warnings for the ten cards, as at the reviewed snapshot. 又's options (north | country | man, male) are unchanged (line 4).
- **reading-exposure:** 0 production hits, 0 padded-session hits and 10 latent collisions, as at the reviewed snapshot (line 186). For 又, the two latent classes are [又 安] (やす, a KANJIDIC2 name reading) and [又 再] (ふたたび, the `--extra` list); neither reading can be drawn in the N1 stack, All stack or Starter practice session pool (lines 35–40).
- **reading-options:** 0 problems, as at the reviewed snapshot (line 151).
- **lint** (`lean\n1_batch_tool.py lint --base 2787e43b`): 3 errors and 37 warnings (was 4 and 41); exit 1.
  - The errors are on existing cards outside the batch: 太 タ; 情 セイ and なさ.け. Each is a metadata reading without a Readings row, present at the base.
  - Removed with the 聞 addition: 聞's error (unknown front-matter key `phonetic`), four warnings on 聞 and the two “no Dictionary line” warnings on 新聞 and 聞く. Added: the two 又 warnings described above. 41 − 6 + 2 = 37.
- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0.
  - Counts: 10 kanji, 9 new words (was 10), 10 changed reused articles (was 9; 聞 out, また and または in), 11 required reciprocal pairs (was 10), 21 reading dispositions, 10 curated offered keys and 87 complete JMdict families (was 89).
  - The manifest is fresh (`92143d996fc2aff4`).
- **budget:** retained 56,880,820 bytes (was 56,880,848), inflated 57,316,892 and local ZIP 36,535,306. The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **manifest:** rebuilding gives an identical file.
- **diffcheck:** clean from the batch base `2787e43b`.
- **validate:** 0 errors.
- **unittest:** 444 tests OK (was 439; the five new tests above).
- **vocabulary:** 3201/3539.
- **link-targets.tsv:** every link on a changed line, resolved by the packet builder.
- **Also in `evidence\`:**
  - `word-quiz.txt`, `distractor-use.tsv`, `distractor-senses.txt`, `corpus-attested.txt` and `meta-scan.txt`, regenerated at the revised snapshot;
  - `support-selection.json`: the selection policy statement and support mappings at the revised snapshot;
  - `rule-7058679348.md`: the text of the issue #60 rule comment that governs support-word selection;
  - `verify-commit.txt`;
  - `selection-order.tsv`: the frozen source rows 1–153 (`docs\n1-sources\source-index.json`) with KANJIDIC2 grade, Joyo or name-use class, whether a card exists at the base `2787e43b`, and B159 membership;
  - `joyo\p<page>.txt`: the text of each cited page of the official Joyo kanji table PDF, with its sha256;
  - `jmdict-cited-entries.xml`: complete pinned JMdict entries for the ids cited in this file and in your RESPONSE.md;
  - `jmdict-scan-c1.txt`: every pinned JMdict entry with a reading ついず or ついで, and every entry with a spelling containing 又, 叔, 叙, 后 or 吏, with its priority tags and marks;
  - `daijisen-kotobank.json`: the 17 Digital Daijisen sections cited by the revision, from kotobank.jp (fetched 2026-11-23): the nine words, 又 吏 太 吟 叙 呈, 皇太后 and 太皇太后;
  - `QuizBuilder.kt` and `Words.kt`: the app's kanji-quiz and word-quiz code. `word-quiz.txt` names the latter `evidence\app-code\Words.kt`; in this packet it is `evidence\Words.kt`.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Process notes

- **Amends before review:** the fix commit was amended in place several times before this review, and each version was signed. Only `5c04be73` is in this range. The last two amends added 確認 to 吟味's exclusions, for consistency with the existing 確かめる exclusion, and then 研 to 吟's, for consistency with 究.
- **Temporary commit:** the check runner needs a clean tree, so one run used a temporary unsigned commit `5f082d75`. It is not in the history, and every output in `checks\` was produced at `5c04be73`.
- **Local check tool:** the lean `quiz_safety.py` (not in the repository) now reads the support-mapping `spelling` field from the ledgers, so it accepts a kana-headed article the same way as the repository audit.
