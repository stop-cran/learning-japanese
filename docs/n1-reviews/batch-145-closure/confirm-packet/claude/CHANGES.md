# Batch 145 revision: what changed from 845aefbb to e07ab312

Revised snapshot: `e07ab312` (full hash `e07ab3127d6ea3d9daa507b519fc993bd968f08c`; also in `packet-manifest.json`). It is
reached from the reviewed snapshot `845aefbb37e40aeb737f32de8066959968cc2cf6` by one commit, `e07ab312`;
`diffs\fix.patch` is its patch. Nothing is published.

- Eight new kanji cards changed (漫 漬 潜 濁 瀬 災 炎 為), one existing kanji card (暑; its declared remark edit was
  reworded) and one existing word article (湧く; its declared remark edit is new). The other seven new cards
  (湧 源 滅 滑 滞 潔 澄), the 渋 card, all other word articles and all 15 stroke files are unchanged from the reviewed
  snapshot.
- **No front matter changed.** No title, tag, metadata reading, `distractors` or `quiz_exclusions` list changed in any
  card, so the meaning and reading options are unchanged.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line.
- `diffs\fix.patch` is the exact patch from `845aefbb` to `e07ab312`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`.
- No Metadata line changed.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 漫 | 30, 44, 46 | Line 30: 浪漫 is now given as ロマン, a JMdict ateji (phonetic) spelling whose reading ろうまん is only a rarely used kana form (JMdict 1147940). Line 44: the code `spec1` is gone (マンガ is now "in katakana") and the clause about a "small ん" is removed. Line 46: すず is corrected to すずろ. |
| 漬 | 23, 39, 41 | Line 23: the schema words `stagk=漬ける` are replaced by a plain restriction sentence (JMdict limits the pickling sense to the spelling 漬ける; 浸ける covers the soaking sense only). Line 39: the tag note `(tagged spec1)` after 浸かる is removed. Line 41: the entry headword is 漬物 (JMdict 1433700), with 漬け物 as another spelling and 漬けもの as "search-only kanji form". |
| 潜 | 30 | 原潜 げんせん is JMdict "nuclear submarine," tagged "abbreviation" (JMdict 1262040): the tag is no longer inside the quoted gloss. |
| 濁 | 46 | The table does not list ジョク; KANJIDIC2 lists it, and Kanjipedia marks it as outside the table. |
| 瀬 | 27 | The mnemonic now says the whole right-hand part is the kanji 頼 (the shape "that also stands at the right of 頼" is gone). The modern-shape, not-etymology label is unchanged. |
| 災 | 25 | The 防災 gloss is "protection against disaster" (JMdict 1520360, singular). The Daijisen わざわい paraphrases are no longer in double quotes. |
| 炎 | 57 | `and` added between the 熱 and 暑 items; the note about the 暑 card now says 炎 mainly names fire. |
| 暑 | 49 | The declared remark edit is reworded: 炎, "flame," mainly names fire, but in 炎天 (JMdict 1177140) and 炎暑 (JMdict 1177090) it also means blazing heat, so the 炎 card keeps 暑 out of its meaning choices. `evidence\kanji-remarks.json` is the updated declaration. |
| 為 | 23, 25, 42, 44 | Line 23: "first sense" becomes "it" (JMdict 2861111 has one sense). Line 25: the Daijisen ため paraphrases are unquoted and "for the same doing" is gone. Line 42: the sentence about the repo's reading checker is replaced by `な.る and な.す share the stem な, so this card claims only what the linked word supports`. Line 44: added `The table lists no kun reading for 為; な.す and the other kun readings are outside the table.` |
| 湧く (word) | 31-32 | The stale sentence that neither character had a kanji card now says 湧 has a kanji card, that the rare alternate 涌 does not, and that this word's written-kanji metadata lists only 湧. `evidence\word-remarks.json` is the declaration. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (17 kanji cards: the 15 new cards and the modified 暑 and 渋; 22 word articles touched by the
  batch): 0 errors, 5 warnings, all Dictionary lines that cite no JMdict entry id (four on modified articles, 不潔, 湧く,
  潜る and 澄む, and 蒸し暑い, which the linter reaches because the modified 暑 card declares it). The same five were
  reported at the reviewed snapshot. With `--no-jmdict` there are 0 warnings.
- `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes. `manifest.txt`: `manifest.json`
  regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt`: 20 changed word files, 20 expected and 20 added link pairs, 1 declared remark edit (湧く), 0 problems.
- `kanji-remarks.txt`: 15 of 15 new cards present; two modified existing cards (暑 and 渋), their declared remark edits
  applied, 0 problems.
- The Android app's JVM tests that read the real content were not run for this revision either, and the Kotlin
  cross-check of the reading audit was not run, as at the freeze.

### Quiz and reading audits

`quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt` were rerun at `e07ab312`. The `--extra` input differs
from the freeze in one respect: the 漫 kun list taken from the Daijisen character entry now reads すずろ, not the
truncated すず that both first-round reports found (Claude C1, GPT G2), so the audit's attested-reading list for 漫 no longer contains すず.
Apart from that and the command line, the three files are identical to the freeze output (the author's comparison, not a
substitute for your own reading of the files):

- `quiz-safety.txt`: 0 errors, 0 warnings.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 0 one-holder padded hits, and 10 latent collisions, as at
  the freeze.
- `reading-options.txt`: the freeze result, including its labelled HITs, which the exposure audit shows cannot be drawn
  because the curated distractors fill every slot.

## Process notes

- `e07ab312` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `845aefbb`.
- The checks in `checks\` were run on the committed revision.
