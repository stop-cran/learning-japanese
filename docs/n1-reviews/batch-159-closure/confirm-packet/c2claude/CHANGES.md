# Batch 159 revision: what changed from 5c04be73 to 4f8ebea7

The revised snapshot is `4f8ebea7`, one commit whose parent is `5c04be73`. The range has no merges. Every commit from the reviewed freeze `1a9bb910` through `4f8ebea7` is signed with key D4C9A275A218AF747B787AFA9D94B9D311BD26A7 (`evidence\verify-commit.txt`).

This revision answers the confirmation reports on `5c04be73`:
- two reviewers confirmed with no findings, each with optional notes;
- a third reviewer found two points only partly resolved (NEEDS FIX) and added one optional note.

`RESPONSE.md` answers your own report only.

- **Changed:**
  - the batch card `kanji/吟.md`: one front-matter line (14) and one Notes line (42);
  - the word articles `words/太后.md` (line 15) and `words/吟味.md` (line 24), one body line each;
  - the ledger `docs/n1-sources/batch-159-progress.json`: the selection statement (line 29), the 叔 exception reason (line 78), the 吟 kanji-exclusion row (lines 426–427, generated from the front matter), the quiz-safety check note (line 947) and the status (line 952).
- **Unchanged:**
  - the other nine batch cards, and the 吟 card's title, readings, distractors and tags;
  - the other seven new word articles, and every existing card or article changed earlier in the batch (太 官 不 伯 味 情 服 贈, また, または);
  - `tools/`, the pinned JMdict selection and extract (still 87 complete families), every stroke file and every other file.
- **Generated file:** `manifest.json` is regenerated (contentVersion `c459784ce290b1ef`; was `92143d996fc2aff4`) and left out of `diffs\`.
- **Line numbers** below are in the revised snapshot. `diffs\changed-lines.txt` has the old and new text of every changed line.

## Changed lines

| File | Changed lines | Change |
|---|---|---|
| `kanji/吟.md` | 14 | `quiz_exclusions` [詩, 歌, 謡, 句, 検, 審, 査, 調, 究, 研] → [詩, 歌, 謡, 句, 検, 審, 査, 調, 究, 研, 験] |
| | 42 | the list of examining neighbours adds 験 (“test; verify”): “…究 (“investigate thoroughly”), 研 (“polish; study closely”) and 験 (“test; verify”) overlap with the sense of examining something closely, as in 吟味.” |
| `words/太后.md` | 15 | the last sentence now reads: “In plain terms, Digital Daijisen describes 太皇太后 as the empress of the emperor two reigns back and 皇太后 as the empress of the previous emperor; in a narrower sense, 皇太后 is such an empress who is also the current emperor's birth mother.” It was “…describes 皇太后 as the empress of the previous emperor, or one who is also the current emperor's birth mother, and 太皇太后 as…”, which could be read as naming two people. Digital Daijisen: 皇太后「前天皇の皇后。また、前天皇の皇后で、現天皇の生母。」; 太皇太后「先々代の天皇の皇后。」 (`evidence\daijisen-kotobank.json`). |
| `words/吟味.md` | 24 | the last sentence now reads: “Both sources mark poetry recitation as the original meaning of 吟味: Digital Daijisen sense 3 is reciting a poem and savoring its flavor, and JMdict sense 4 (archaic) is “reciting and appreciating traditional poetry”.” It was “Reciting a poem and savoring its flavor is the original meaning of 吟味 in both JMdict (sense 4, archaic) and Digital Daijisen (sense 3).” Only Daijisen says 味わう (「詩歌を吟じてその趣を味わうこと」, marked 《3が原義》); JMdict 1243390 sense 4 is marked archaic with the note “orig. meaning”. |
| `docs/n1-sources/batch-159-progress.json` | 29 | `selectionReason`: two rows (后 吏) take the untagged route. The 叔 row is now described as an author's exception to point 2's preference for a tagged spelling, reported to the owner: the tagged spellings 叔父 and 叔母 have the シュク readings しゅくふ and しゅくぼ, but those readings carry no tag, and the tags belong to the whole-word readings おじ and おば; B156 applied the same interpretation to 伯 (伯仲). |
| | 78 | 叔 `exceptionReason`, rewritten (see “The 叔 exception” below). It no longer says “No candidate qualifies through a reading of 叔”. |
| | 426–427 | the 吟 kanji-exclusion row adds 験 (generated from the front matter) |
| | 947 | `mechanicalChecks.quizSafety`: corrected (see “Correction to the earlier statements” below) |
| | 952 | `status`: “The 后 and 吏 untagged-support exceptions, the 叔 exception to the tagged-spelling preference (reported to the owner), and the kana-headed 又 support remain subject to review.” |

## The 叔 exception

Ledger line 78 now reads, in full:

> This row is an author's exception to the preference in point 2 of the issue #60 rule, reported to the owner for a decision. Under the letter of point 2, the tagged spellings 叔父 (entry 1607070) and 叔母 (entry 1607100), both ichi1/news1, are candidates: their readings しゅくふ and しゅくぼ, restricted to those spellings, use the KANJIDIC2 reading シュク and carry no irregular, rare, outdated, ateji, or gikun mark. They are not used because the tags in those entries belong to the whole-word readings おじ and おば, which the Joyo table lists in its notes for 叔 as special readings of 叔父 and 叔母; しゅくふ and しゅくぼ carry no priority tag; and an article headed 叔父 or 叔母 would teach おじ or おば as its primary reading, not シュク. B156 applied the same interpretation to 伯父 and 伯母 when it kept 伯仲 for 伯, and all three review families accepted that row. Every other candidate written with 叔, including 叔世 and the おじ/おば compounds such as 大叔父 and 叔父さん, is untagged. 伯叔 (entry 1474270) is untagged and is the Joyo table's only example for シュク; its other kanji 伯 has a card; its spelling and reading carry no irregular, rare, outdated, ateji, or gikun mark; and it backs the quizzed on reading シュク. JMdict glosses it “brothers; one's father's brothers”. If the owner prefers the letter of point 2, the fallback is an article headed 叔父 whose reading is しゅくふ. Keep this exception for independent review.

Sources:
- `evidence\jmdict-cited-entries.xml`, entries 1607070 and 1607100: 叔父 and 叔母 carry ichi1/news1 on the spelling; おじ and おば carry tags; しゅくふ and しゅくぼ are restricted (`re_restr`) to 叔父 and 叔母 and carry none.
- `evidence\joyo\p75.txt` (the 叔 row) and `evidence\joyo\p162.txt` (the appendix of whole-word readings).
- `evidence\b156-selection.json`: the published B156 ledger's selection statement, which says “伯仲 is kept because 伯父 and 伯母 are tagged only for their whole-word readings おじ and おば, 伯爵 needs 爵, which has no card, and 画伯 is the alternative. All three review families accepted these row decisions.”
- `evidence\rule-7058679348.md`: point 2 of the rule.

The batch content is unchanged: `words/伯叔.md` stays the 叔 support article, and `kanji/叔.md:39` still says that おじ and おば are whole-word special readings, not readings of 叔 alone. The owner will be asked on issue #60 whether this interpretation (here and in B156) stands, with the 叔父 (しゅくふ) article as the fallback.

## Correction to the earlier statements

The earlier revision's CHANGES.md (under “Points the author judged acceptable”) and one RESPONSE said that 吟's curated distractors 二 自 社 “fill all three slots in every shipped pool”, citing `checks\quiz-safety.txt` line 16 and `checks\reading-options.txt` line 108. The old ledger line 946 said that each card's curated distractors fill all three wrong options of its meaning and reading questions. Both statements were wrong for 吟's reading question.

- **Meaning question.** The statements hold. 二 “two”, 自 “self, oneself” and 社 “company, shrine” have distinct titles, and none is excluded, so they fill all three wrong options (`checks\quiz-safety.txt` line 16; `evidence\QuizBuilder.kt` lines 26–34). The 吟 `quiz_exclusions`, including the new 験, therefore matter only in fallback or custom pools.
- **Reading question (ギン).** The statements are wrong. 二 offers ニ or ジ, 自 offers ジ or シ, and 社 offers シャ. Each curated card gives one random reading, and a repeated reading is dropped (`evidence\KanjiReadings.kt` lines 100 and 110). In one of the four outcomes, 二 and 自 both show ジ, and the closeness fallback fills the open slot (line 111). `checks\reading-exposure.txt` lines 138–150 report “deficit 0/1: the fallback fills the open slots”: 61 drawable wrong options in the N1 and All stacks (4 curated, 57 fallback) and 27 in Starter practice sessions (4 curated, 23 fallback). `checks\reading-options.txt` lines 108–119 list the 57 tier-3 fallback keys and see 19 wrong options over 100 seeds. The totals at the end of `checks\reading-exposure.txt` report 0 production and 0 padded-session hits. `checks\quiz-safety.txt` line 17 (“wrong options from distractors 3/3”) counts the three curated cards; it does not model the shared ジ.
- **The other nine cards.** Their curated options fill all three wrong slots of every reading prompt in every outcome; the fallback is never consulted (`checks\reading-exposure.txt`).
- **Ledger line 947** now says this: the meaning questions are filled by the curated distractors; for 吟's ギン prompt, the fallback fills the open slot in one of four outcomes, with no exposure hit.

The card's distractors are unchanged: the fallback options are readings of other cards, the audit finds no hit, and existing cards also rely on fallback options (`checks\quiz-safety.txt` lines 22–33 list 11 existing cards whose curated distractors fill only two of three slots).

## Quiz options

- **Kanji quiz.** `checks\quiz-safety.txt`, `checks\reading-exposure.txt` and `checks\reading-options.txt` are identical to the earlier revision's apart from the header line. 吟's meaning options are still 二 自 社. The exclusion check is symmetric (`evidence\QuizBuilder.kt` line 26). Adding 験 therefore removes 験 as a fallback meaning option for 吟, keeps 吟 out of 験's fallback meaning options, and stops 吟 and 験 from appearing together as wrong options for a third card (line 30). 験's own curated distractors are unaffected. Reading questions do not use `quiz_exclusions`: they exclude only the target's own readings (`evidence\KanjiReadings.kt` lines 80–88 and 100).
- **Word quiz.** `evidence\word-quiz.txt` is identical apart from its header line; no word front matter changed.

## Checks run on the revised snapshot (outputs in `checks\`)

Every check gives the same result as at `5c04be73`, except the numbers named here.

- **audit** (`tools\audit_n1_batch.py --batch 159`): exit 0; 87 complete JMdict families; the manifest is fresh (`c459784ce290b1ef`, was `92143d996fc2aff4`).
- **budget:** retained 56,880,977 bytes, inflated 57,317,049 and local ZIP 36,535,366 (+157 retained bytes from `5c04be73`). The CI limits are 62 MiB, 80 MiB and 42 MiB.
- **quiz-safety:** 0 errors, 0 warnings. **reading-exposure:** 0 production hits, 0 padded-session hits, 0 one-holder padded hits and the same 10 latent collisions. **reading-options:** 0 problems.
- **lint:** exit 1 with the same 3 errors and 37 warnings as at `5c04be73`. The errors are on the reused cards 太 and 情, present at the batch base `2787e43b`.
- **Other checks:**
  - manifest rebuild identical;
  - diffcheck clean from the batch base `2787e43b`;
  - validate 0 errors;
  - unittest 444 tests OK;
  - vocabulary 3201/3539.
- **Not run:** the Kotlin (JVM) tests. Quiz behaviour comes from the Python ports named in each output.

## Evidence added in this round

- `evidence\b156-selection.json`: an excerpt of the published B156 ledger (`docs/n1-sources/batch-156-progress.json` at `4f8ebea7`): its status, its selection statement and its 伯 support row.
- `evidence\KanjiReadings.kt`: the app's kanji reading-question builder (`KanjiReadingQuiz`), from kanji-cards-android commit `91e1d4b578859f7bfb582f7b9c6acf48c6ca6a75` (Git blob `492a43c315816fbdf2079ee8c0bb05c731136b5c`).
- `evidence\app-code-SOURCES.json`: the pinned Android commit with the Git blob id, raw URL and web URL of each app file. `KanjiReadings.kt`, `QuizBuilder.kt` (blob `47ce071b…`) and `Words.kt` (blob `9c8b2c82…`) in this packet match the listed blobs (`git hash-object --no-filters` on the raw bytes; the files keep their CRLF line ends).
- `evidence\jmdict-scan-c2.txt`: the same pinned-JMdict scan as `jmdict-scan-c1.txt` in the earlier revision packet (the JMdict pin did not change).
