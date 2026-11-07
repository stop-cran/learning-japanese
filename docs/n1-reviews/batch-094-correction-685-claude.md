# Batch 094 correction 685: 縮める exclusion added to 削る — textual fix CLEAN, runtime checks not yet run

The text change resolves my 683 finding: `words\削る.md:9` now ends its quiz exclusions with 縮める. No regression appears in the supplied text. The corrected native ContentSync import and production quiz-builder checks have not been run, so runtime acceptance stays open.

## Snapshot
- **Signed HEAD:** b85d7a4d40225ad829891c1c7fe3b31f8cd31afe; contentVersion 74b7e886a1afbd46.
- **Correction base:** da2905cd. The previous contentVersion was eeae47753a460f72.
- **Review type:** dependent confirmation in my original session, not a fresh blind review.

## Scope
- **Model and session:** claude-opus-5.5, session edf22897-9f87-4a3b-b20f-4c2fd839013a.
- **Reads:** exactly three, one view call per response, each read in full with no ranges:
  1. My 683 report.
  2. My serial-repair report.
  3. `control\batch-094-correction-common-685.txt`.
- **Not re-read:** the 121 dictionary families, any images, and anything else.

## Verdicts (this narrow correction only)

| Facet | Verdict |
|---|---|
| Correctness | CLEAN |
| Scoped coverage | CLEAN |
| Comprehensibility | CLEAN |

**Correctness**
- **The change:** line 9 changes from `[切る, 減らす, 省く, 消す, 除く, 外す]` to the same list with `縮める` appended at the end. The existing exclusions and their order are preserved.
- **Nothing else changed:** the diff touches only that line plus the manifest hash and contentVersion. 削る's title, identity, reading けずる, level (jlpt 2), body and links are unchanged. 縮める.md is unchanged.
- **Sources support the pair directly:**
  - 削る sense 2 is "to cut down (budget, expenses, staff, time, etc.); to curtail; to reduce".
  - 縮める sense 1 is "to shorten; to reduce; to condense; to shrink".
  - The displayed titles overlap too: "cut down" against "shorten; reduce". The 縮める article's example of shortening meeting time (会議の時間を縮めました) matches 削る's "cutting … time".
- **Not a transitive guard:** the pair rests on the two words' own meanings, not on the fact that both already exclude 減らす and 省く.

**Scoped coverage**
- The quiz contract (`docs/content-format.md:155-177`) says one declaration excludes a pair in both directions and in both quiz types. Declaring it on 削る alone is therefore enough.
- No further guards are needed: 縮む and 圧縮 stay unwarranted, as I judged in 683.

**Comprehensibility**
- The quiz-exclusion field is not displayed to learners, and the article text is unchanged.

## Findings
- None.

## Reconciliation

**Textual**
- **削る/縮める (683 finding):** resolved at the source and declaration level.
- **削除/省く, 削る/除く, 削る/外す:** still resolved.
- **My original "exclusions cover the real overlaps" claim:** stays withdrawn, as recorded in 683.
- **除く/取り出す:** remains an out-of-scope hypothesis, not a finding.
- **Execution 683:** the overlapping panel 1 and 2 reads remain rejected. The serial repair does not relabel that execution.

**Runtime**
- **Not yet run:** the corrected native ContentSync import and the production builder guard records. The audit itself shows these checks as `"pending"` and `runtimeAccepted: false`.
- **Inherited evidence:** the earlier visual captures and the 682 native receipts are inherited. They are not evidence about the corrected archive.

## Optional
These earlier polish items stay optional and unchanged:
- 削.md:51: change "words" to "characters".
- 削.md:50: add the idiom 興をそぐ.
- Reduce jargon in 削る.md:25 and :44, and in 削除.md:38.
- Rephrase 削除.md:41.
- 削除.md:22: describe された as the "passive past of する".
- The 削る link wraps across lines as "削 / る".
- Align the 削る gloss in 削.md ("shave; sharpen; cut down") with its title ("shave; pare; cut down").

## Limits
- **Audit is not test execution:** the 684 audit is mechanical and I did not run it.
- **Audit base commits:** the audit lists `baseCommit` 48765e20 and `correctionBase` da2905cd; I did not check how these relate.
- **Not verified:** no hashes, Git history, signatures or upstream JMdict entries.
- **Not claimed:** no fresh 121-family review; no native, physical-phone, handwriting or ML Kit, latest-app-main, general-release, whole-set or publication claim.
- **Recommendation:** only bounded textual closure, pending the corrected native import and builder checks.
