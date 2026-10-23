## Snapshot
- **Corrected commit:** `ac74524ac2d47d12c0b2caf8bd430f47f9ab580b`. Its parent is the authored commit `84a79c01fe6b2b669652802823ca0fc09c25fe98`.
- I reviewed committed content only, as recorded in the receipt.
- I only had file, search and web tools, so I could not run Git. The commit identity, the clean tree, the file hashes, the evidence hash (`a55263b2…`) and the diff hash (`fad499b1…`) are the author's claims. I did not check them myself.

## Scope
- **Model:** claude-opus-5.5, Claude family, working alone. This is a bounded confirmation of the changed passages, not another nineteen-card review.
- **Read in full:** 高度, 高等, 合同, 公務, 合理 and 項目, plus the patch (lines 1–30, 850–1003) and the correction receipt.
- **Comparison cards:**
  - Read in full: 松, 訳, 偉い, 立派 and 役.
  - Checked the titles and exclusions of: 務め, 勤め, 義務, 役割, 係, 良い, いい, 優秀, 優れる, 選択, 予定, 高級, 上等, 一流 and コース.
- **Evidence packet:**
  - The correction evidence and the added comparison families (lines 24576–end).
  - The entry families 1155780 偉い, 1283850 高等, 1048830 コース, 1285140 合同 and 1304970 仕事.
- **My own lookups:**
  - Kotobank 松 worked: 日国 まつ [1]⑪ gives the top rank of 松竹梅.
  - Jisho's API (JMdict data) worked for 役. Sense 1 includes duty and service; sense 2 is position of responsibility, post or office.
  - The Kotobank search for 合同 returned nothing usable.
- **Recount:** across the 19 new articles, 16 have exclusions, totalling 107 entries. This matches the author's count.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 高度 | CLEAN | CLEAN | CLEAN |
| 高等 | CLEAN | CLEAN | CLEAN |
| 合同 | CLEAN | CLEAN | CLEAN |
| 公務 | NEEDS FIX (B27-03) | CLEAN | CLEAN |
| 合理 | CLEAN | CLEAN | CLEAN |
| 項目 | CLEAN | CLEAN | CLEAN |
| Packet additions (six families, labels, pair lists) | CLEAN | CLEAN | CLEAN |

## Findings
**My original findings**
- **B27-01 (合同): resolved.**
  - Line 17 now teaches merging into a single body.
  - Line 24 adds the political-party example with kana and English.
  - Lines 46–48 replace the double negative with a plain contrast between a merger and a joint event.
  - JMdict 1285140:1 lists "merger; amalgamation", which supports the change. The new sentence is written by the author, not taken from real usage.
- **B27-02 (公務): resolved.** 務め, 勤め and 義務 are now excluded at line 9, and lines 37–39 add accurate comparisons.

**New finding**
- **B27-03: minor; correctness (quiz); `words\公務.md:9`; medium confidence.**
  - **Claim:** 役, titled "role; duty", is still not excluded from 公務, titled "official public duties".
  - **Learning impact:** a learner who picks "role; duty" for 公務 could be marked wrong, even though the correction now protects the same plain "duty" wording on 務め and 義務.
  - **Evidence:**
    - The existing cards 務め, 義務 and 役割 all exclude 役. The project already treats 役 as confusable with every other "duty" card.
    - 役's JMdict sense 2 is "position of responsibility; post; office", which is close to an official role.
    - The evidence packet has no 役 dictionary entry (1537970), so the correction never considered this pair.
  - **Not a regression:** this gap was already there in the original commit, and I missed it in my first review.
  - **Fix:** add 役 to 公務's quiz exclusions.

**Regression check:** the changed passages introduced no new defects. The bodies of 高度 and 高等 no longer refer to 立派 or 偉い. The 項目 change from "An"/"an" to "A"/"a" (lines 42 and 44) is correct.

**My original optional observations**
- **Withdrawn:** the コース exclusions of 選択 and 予定. Sense 7 of the JMdict entry ("plan; option") supports them.
- **Resolved:** 合理/訳. Sense 3 of 訳 ("(good) sense; reason") supports the new exclusion and the qualified comparison.
- **Partially resolved:** removing 立派 and 偉い from 高度 and 高等 was correct.
- **Optional, and I accept the author's no-change decisions:** 国立's short title, a もみじ example, 国籍/市民, 合理を重んじる and 効力を持ちます, and the unlinked 越す. I found no evidence of an error in any of them.

## Optional
- 高度 against 良い ("good") is still the weakest remaining exclusion. Exclusions that are too broad only shrink the pool of wrong answers.
- 高等 and 偉い still overlap slightly, because 偉い can mean "high-ranking" (JMdict 1155780:2). The displayed labels make this tolerable.
- 役割 ("role; allotted duties") might be considered for 公務, but this has low confidence.
- 合理/理由 needs no exclusion.

## Limits
- I could not run Git or any hashes.
- The author's Daijisen and Weblio checks for 務め, 義務, 合理, 効力 and 合同 are only the author's claims. The only entries I retrieved myself were Kotobank 松 and Jisho's JMdict data for 役.
- I read the evidence packet only in bounded sections.
- I did not run the app's quiz draws or measure how often items are selected.
- Nothing here is certified by a native speaker or by real-usage data, and the community N2 list is not an official JLPT syllabus.
