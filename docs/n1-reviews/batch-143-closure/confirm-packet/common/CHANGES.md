# Batch 143 revision: what changed from 6b5934e7 to 9b8f50a8

Revised snapshot: `9b8f50a8` (full hash `9b8f50a8b9ddb2123137573ccb26761e05954491`; also in `diffs\fix.patch`'s header and
`packet-manifest.json`). It is reached from the reviewed snapshot `6b5934e71945ed215cf57a8291117762e67b1d9e` by one
commit. Nothing is published.

- Twelve of the 15 new kanji cards changed: 旋 既 旦 旨 暑 朗 条 架 柄 染 株 桜. The other three (施 旗 暦) are unchanged.
  All 17 word articles (including the declared 西暦 remark edit) and all 15 stroke files are unchanged from the reviewed
  snapshot.
- **Front matter changed in two cards, unlike a text-only revision.** `quiz_exclusions` lost 凱 on 旋, and lost 在, 有
  and 存 on 既. No title, tag, metadata reading or `distractors` list changed. The curated distractors still fill all
  three meaning slots of every target prompt, so the exclusions only matter when 旋 or 既 is drawn as a fallback wrong
  option on another card's prompt, or when 在, 存, 有 or 凱 is drawn on a 既 or 旋 prompt. Please re-check the meaning-quiz
  options for both cards (see "Checks").
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. 柄 gained one line (the Common words bullet at line
  48 became lines 48-49); every other changed card keeps its line count.
- `diffs\fix.patch` is the exact patch from `6b5934e7` to `9b8f50a8`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`, with the target's
  real `title:`.
- No card's Metadata line changed. `evidence\meta-scan.txt` is the author's scan of the 15 cards at `9b8f50a8`; the
  three lines under "not listed" (染め, 抜き and 雌雄) are parts of compounds, as at the freeze.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 既 | 14, 38, 48 | Line 14: `quiz_exclusions` loses 在, 存 and 有. Line 38: the Joyo sentence `It prints 既 in parentheses as a compatibility ideograph, not as a historical form.` now reads `It adds the traditional (Kangxi dictionary) form in parentheses.` Line 48: the exclusion explanation now lists only the time/former group and the completion group (完 全 終 済 卒); the sentence about existence (在 存 有) is gone. Support: `evidence\joyo-item6.txt` (表の見方 item 6: the parenthesised forms are the traditional Kangxi-dictionary forms; the packet's `joyo-pages.md` shows U+FA42 in parentheses after 既, which is how the PDF text layer encodes that form). |
| 朗 | 43, 51 | Line 43: the same Joyo sentence is replaced by `The Joyo table adds the traditional (Kangxi dictionary) form in parentheses.` (the packet's `joyo-pages.md` shows U+F929 there). Line 51 (Notes): `These three cards supply the distractors` now reads `The cards 月, 有 and 朝 supply the distractors`, so 良 is not read as a distractor. |
| 旋 | 14, 54 | Line 14: `quiz_exclusions` loses 凱. Line 54 (Notes): 凱 is removed from the group that `overlap returning` (帰, 戻, 返 remain); 凱 is still explained on lines 41 and 51 as the other kanji of 凱旋. |
| 旦 | 25, 34, 41, 52 | Line 25 and line 52: the garbled `does not support a new reading in 一旦` and `do not treat it as support for splitting the reading into 一旦` now say that no ordinary JMdict word was found that uses あした and that 一旦 is read いっ + タン (it contains no あした). Line 34: 旦つく だんつく is `husband (a slighting word)`; support: `evidence\weblio-dantsuku.txt` (Daijisen: 「旦那」を軽んじていう語). Line 41: `ダンナ` becomes `だんな`. |
| 旨 | 25, 37 | Line 25: the skillful sense of うま.い is no longer presented as a sense of 旨い; it now says JMdict marks that sense as especially written 上手い or 巧い (the entry's `esp.` marking). Line 37: the claim that the うまい entry lists 旨味 as ateji is replaced by `A separate JMdict entry for うまみ lists 旨み and 旨味, and tags 旨味 as ateji (kanji chosen for sound or sense); 旨 is read うま in both.` and the `not a reading to split` wording is gone. Support: `evidence\jmdict-cited-entries.xml` (1310520 旨み / 旨味 {ateji} / うま味, and the original packet's `jmdict-families.xml` for the うまい entry 1310460 and its `esp.` spelling restrictions). |
| 暑 | 36 | In 蒸し暑い, `蒸 supplies むし` now reads `蒸 writes む and し is okurigana, so 蒸し is むし`. Support: `evidence\jmdict-cited-entries.xml` (1356870 蒸し暑い). |
| 条 | 58, 61 | Line 58: `resemble the 木 base with a changed upper stroke` now reads `with an added horizontal stroke`. Line 61: the sentence that called 条彫り すじぼり, 条播き すじまき and 発条 ばね all whole-word readings is replaced. It now says that in 条彫り and 条播き 条 is read すじ, the kun reading in the table above, which is not selected for questions here, and that the whole-word (gikun/jukujikun) caveat applies to 発条 ばね only. Support: the original packet's `public-source\weblio-条.txt` (「［訓］すじ」; 「［難読］条彫(すじぼ)り・条播(すじま)き・発条(ばね)」) and `jmdict-families.xml` for 発条. The jargon paragraph and the すじ row are unchanged. |
| 架 | 25 | `as in 架 か` is now `as in 書架 しょか, bookshelf`, a word in the Daijisen extract (the original packet's `public-source\weblio-架.txt`). |
| 柄 | 48-49 | The single Common words bullet `柄 え — handle; pattern` is split into `柄 え — handle; grip` and `柄 がら — pattern; design`, both linking the same word article. Support: `evidence\jmdict-cited-entries.xml` (1508290 え; 1508300 がら). |
| 染 | 34, 40, 42 | Lines 34 and 40: 愛染 あいぜん is no longer called a whole-word reading; the ゼン row and the paragraph now say 染 is read ゼン in it, an on reading outside the Joyo table. Line 42: `ゼン is recorded by Digital Daijisen and Kanjipedia but is not in the KANJIDIC2 metadata list.` Support: the original packet's `public-source\weblio-染.txt` (「［音］セン（慣） ゼン（漢）」) and `kanjipedia-outside-readings.json` (染: ゼン), and `evidence\jmdict-cited-entries.xml` (2583650 愛染). |
| 株 | 25 | `守株 しゅしゅ is a word-level reading ... do not split that whole-word reading among the characters` now reads `守株 しゅしゅ is 守 シュ + 株 シュ, an idiom from the fable of guarding a tree stump, meaning "lack of innovation; stupidity."` Support: `evidence\jmdict-cited-entries.xml` (1882040 守株 しゅしゅ). |
| 桜 | 25, 37 | Line 25: `the mizaru cherry` now reads `the fruit-cherry tree (ミザクラ, mizakura)`; the original packet's `public-source\weblio-桜.txt` has 「２ 木の名。ミザクラ。「桜桃(おうとう)」」. Line 37: the whole-word caveat is limited to 桜桃 read さくらんぼ; in 桜ん坊, `桜 is plainly さくら, followed by ん and 坊 read ぼ`. Support: `evidence\jmdict-cited-entries.xml` (1298460 桜桃 / 桜ん坊 / さくらんぼ). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter (15 kanji cards, 17 word articles): 0 errors, 4 warnings, all on word articles whose
  Dictionary line cites no JMdict entry id. The same four warnings were reported at the reviewed snapshot.
- `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes. `manifest.txt`: `manifest.json`
  regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt`: 17 changed word files, 17 expected and 17 added link pairs, 1 declared remark edit (西暦), 0 problems.
- `kanji-remarks.txt`: no existing kanji card changed; 15 of 15 new cards present, 0 problems.
- The Android app's JVM tests that read the real content were not run for this revision either (no JDK on the authoring
  machine), so there is no `jvm.txt`.

### Quiz and reading audits

`quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt` were rerun at `9b8f50a8` with the same `--extra`
input as at the freeze. Although front matter changed in 既 and 旋, the rerun is line-for-line identical to the freeze
output apart from the command line in `reading-exposure.txt` and `reading-options.txt` (the author's comparison of the
two runs, not a substitute for your own reading of the files):

- `quiz-safety.txt`: 0 errors, 0 warnings.
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 0 one-holder padded hits, and 10 latent collisions
  (7 distinct target/reading pairs, as at the freeze).
- `reading-options.txt`: 0 problems.

Whether the audits themselves cover the effect of the removed exclusions is for you to judge; the author's expectation is
that the curated distractors fill all meaning slots on the 既 and 旋 prompts and that 在, 存, 有 and 凱 are not similar in
meaning to "already; previously" or to "go around; return", but that is a claim to test against `QuizBuilder.kt` and the
card titles, not a result of the audits.

## Process notes

- `9b8f50a8` is the only fix commit; `diffs\fix.patch` is the whole change from the reviewed snapshot `6b5934e7`.
- The checks in `checks\` were run on the committed revision.
