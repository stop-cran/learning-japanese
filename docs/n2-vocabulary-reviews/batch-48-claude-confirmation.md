## Snapshot

The corrected commit is `06ea875040a5484ccd27594c306884a3aa8958a9`, with parent `614bbb8394118e9e38ebb7b8c6ca2011a62be4bb`. I took both from `batch-48-correction-snapshot.json`. I reviewed committed content only. My file tools cannot run Git, so I could not verify cleanliness, blob hashes or patch-to-commit equivalence; the author ran those checks. I did not inspect `.git`.

## Scope

**Model:** claude-opus-5.5 (Claude family). I used only view, rg, glob and web_fetch, and I made no web fetches in this pass. I did not run the quiz and made no edits, delegation or agent calls.

**Complete reads in this pass:**
- The correction receipt and the whole `batch-48-correction.patch`, which changes only the nine listed articles.
- Full rereads of 属する, 続々, 測量, 備える, そのうえ, そのほか, 祖先, そのころ and 剃る.
- `corrections-comparison-reading.txt`: all 10 families and 43 senses (そして, ばたばた, ある, 持つ, 昔, 調査, 入る/いる, 入る/はいる, 或る, そうして).
- `corrections-existing-reading.txt`: all eight old bodies.
- The `correctionEvidence` section of `corrected-review-evidence.json` (line 24376 to the end). It contains no `quizGuardRationale`.

**Spot-checks in this pass:**
- The 続, 属 and 剃 records in `review-components.jsonl`.
- Daijisen passages in `public-bodies.txt`: lines 18–35 (しょくする), 133 (祖先 sense 3) and 285 (なまって).
- Rows 942–961 of `n2-vocabulary-sources.tsv`.
- The `quiz_exclusions` line on all 19 new cards. My own count is 95 declarations on 18 cards (蕎麦 has none), plus 2 on 備える.
- Glob checks confirming that all eight guard-target files exist.
- A title grep across `words\` for possible collisions with the new guards, plus the titles of 準備, 用意, 支度, 設備 and 兼ねる.

**Inherited without rereading:** my initial complete reads of the 11 unchanged new cards, the six kanji cards, the six link-only articles and the mapping files, and the related patch.

**Not read:** `selected-families-01`–`08`, `additional-comparison-reading`, `alias-public-bodies`, the two snapshot JSONs, `confusable-words.md`, `jlpt-levels.md`, all forbidden ledgers, `batch-48.json`, and other reviewers' output, including the report paths listed in the receipt.

## Verdicts

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:942 | 総理大臣 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:943 | 送料 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:944 | 属する (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:945 | 続々 (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:946 | 速達 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:947 | 測定 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:948 | 測量 (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:949 | 速力 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:950 | 素質 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:951 | 祖先 (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:952 | そそっかしい (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:953 | 率直 (new; 卒直 normalized) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:954 | 備える (reused N3) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:955 | そのうえ (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:956 | そのころ (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:957 | そのため (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:958 | そのほか (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:959 | 蕎麦 (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |
| N2:960 | 剃る (new) | complete reread (corrected) | CLEAN | CLEAN | CLEAN |
| N2:961 | それなのに (new) | inherited initial complete read | CLEAN | CLEAN | CLEAN |

- **Six kanji cards (総, 臣, 測, 量, 麦, 卒):** CLEAN, inherited and unchanged according to the patch.
  - 総 and 臣 link to 総理大臣 at ソウ and ジン.
  - 測 links to 測定 and 測量 at ソク, and 量 links to 測量 at リョウ.
  - 麦 links to 蕎麦 only as a whole-word そば reading; it does not assign ば to 麦.
  - 卒 has 卒直 alias navigation only.
- **Six link-only articles (首相, ぞくぞく, 側, 先祖, 子孫, うどん):** CLEAN, inherited and unchanged.
- **Preservation of reused 備える:** CLEAN, with one recorded exception. The patch adds only line 9, `quiz_exclusions: [持つ, ある]`. The body, N3 level, ID, reading, title, type, kanji, tags and citation are unchanged.
  - The exception is justified because the newly taught possession sense (1244960:3) overlaps 持つ sense 2 (1315720:2) and ある senses 2 and 4 (1296400:2,4).
  - The mapping note for 954 lists ID, reading, title, N3 and original teaching. Quiz exclusions are not among them, so the note is not contradicted.
- **Mappings N2:942–961:** CLEAN and unchanged, which I re-checked by grep. Raw fields are preserved:
  - blank glosses for 956 and 961;
  - 卒直 normalized to 率直;
  - 具える mapped to 備える at level 3 with senses 1–3;
  - 蕎麦 sense 2 plus 1238460:1,3;
  - search-only その他 spellings.

## Findings

**Dispositions of my initial findings:**

- **B48-01 (続々 voicing claim): resolved.** 続々.md:29 now reads "Here the on reading ゾク is repeated: ぞく + ぞく." The 続 record in `review-components.jsonl` lists ゾク as an on reading. I accept that this record is the precise anchor, not my earlier principal-reading citation.
- **B48-02 (祖先 scope): resolved.** 祖先.md:24-25 adds 人類の祖先 with kana and a translation, and line 31 now says "ancestral line." This matches Daijisen sense 3 「一族のもと。『人類の―』」 (`public-bodies.txt`:133). I withdraw my suggested 先祖 register contrast because the evidence does not support it.
- **B48-03 (そのころ example): resolved.** そのころ.md:20 now has an explicit antecedent. I accept the reclassification as clarity polish because the original was not shown to be ungrammatical.
- **B48-04 (属する / しょくする wording): resolved.** 属する.md:44-46 now describes overlapping belonging plus other uses. This matches Daijisen しょくする sense 1 「所属する。ぞくする。」 and senses 2–3 (`public-bodies.txt`:18-35). I withdraw my "mostly 嘱する / rare literary" remedy; neither the ▽ marker nor the captured text establishes frequency or register.
- **B48-05 (剃る する reading): resolved.** 剃る.md:31 matches 「[補説] なまって『する』ともいう。」 (`public-bodies.txt`:285). Both godan readings stay distinct from irregular する ("do"). I withdraw my regional and colloquial labels.
- **B48-06 (測量/調査 guard): resolved** at 測量.md:9. The other reviewer made the same observation, so it is not a unique contribution.

**Guards I did not raise initially (from the other reviewer).** I tested each against the complete families and old bodies, and I accept all of them. My initial CLEAN quiz verdicts for 属する, 続々, そのうえ, そのほか and 備える missed these collisions.
- **属する/入る:** 入る sense 1465590:3 is "come under; belong," and its old body discusses joining a group.
- **続々/ばたばた:** ばたばた sense 1098660:3 is "falling one after another," and its old body teaches 看板がばたばたと倒れた.
- **そのうえ and そのほか / そして and そうして:** the senses and old bodies of both conjunctions include addition. The overlap between そのほか and そうして is the weakest of the four, but excluding it is harmless.
- **備える/持つ and 備える/ある:** these follow from the newly taught possession sense.

**そのころ/昔:** this was my optional suggestion and was adopted as a precaution only. It does not equate future-reference そのころ with 昔.

**Guard checks:**
- All exclusion pairs are pairwise, with no transitive assumptions, and every original exclusion is retained.
- The guards rest on actual senses, not homophony.
- 或る and 入る/いる are separate identities and are not the basis of any guard.
- I found no excessive guard.
- The title grep surfaced 相続 ("inheritance; succession") and 過去 ("the past"). Neither is a genuine answer ambiguity, so neither needs a guard.

**New actionable defects:** none.

## Optional

- 属する.md:44 could name Digital Daijisen instead of saying "The dictionary." The usage link below it already supplies the source.
- My earlier optional notes remain nonblocking: exhaustive kanji-card footer lists, other spellings for そのため, the breadth of 素質's exclusions, and the 蕎 kun reading.

## Limits

- I did not fetch any dictionary pages myself. Daijisen evidence is limited to the author's captures; five extractions are missing, そのころ/その頃 have no positive lexical extraction, and 其の頃 returned HTTP 404.
- Rows 956, 957 and 961 therefore rest on JMdict and the captured headings.
- I did not run the quiz, and this review is not a native-speaker certification.
- Hashes, Git cleanliness and commit equivalence were checked by the author, not by me.
- I did not reread the inherited files in this pass, and I never read the selected-families files or the additional comparison union. That initial scope gap explains the missed guards.
- Overlaps between 備える's unchanged preparation sense and 準備, 用意 or 支度 are baseline content outside this batch's scope, so I did not assess them.
