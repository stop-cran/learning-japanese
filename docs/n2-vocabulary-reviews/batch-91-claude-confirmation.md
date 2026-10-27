## Snapshot

- **Revised commit reviewed:** `b2c2811a7ee64f9924227376459c0ba00e045fb6`. Its parent is `28ac612d4bd09064cc9c102fa6abd0d84c168434`, the draft I reviewed first. Only committed content was assessed.
- **Author claims I did not check:**
  - Six new cards changed.
  - Six other new cards, all source mappings and raw fields, all older word bodies and the narrow 算 patch are unchanged.
  - Two quiz exclusions were added, taking the total from 84 to 86.
  - No baseline exception was made.
- **Not run by me:** I ran no Git, hash, manifest, `validate.py`, `build_manifest.py` or app checks. File tools cannot execute them, and this turn used no tools at all.

## Scope

**Model and mode:** claude-opus-5.5 (Claude family), resuming the original session. This is a nonblind confirmation with zero tool calls this turn.

**Evidence, all supplied inline by the author:**
- the exact correction diff for six words
- the author's adjudication
- both original reports
- all 12 mappings and all 12 current bodies
- 16 complete older bodies
- the unchanged 算 article and its original patch
- 16 component records
- the principal and corrective JMdict families
- all comparison labels
- the content-format contract
- 12 original Daijisen wrappers, the corrective wrappers and the かなり/だいぶ usage note

None of this is my own retrieval. Author reads (27 families, 50 senses, 16 bodies, 10 wrappers from one authority) are not my reading depth.

**Earlier process:**
- The native record for my session is authoritative: 25 starts, 20 completed, 5 interrupted, at most 5 outstanding. My own count of 19 completed and 24 issued was wrong. The overlap I caused broke the one-outstanding-call rule.
- GPT's session ran 35 starts, 35 completed, at most 1 outstanding.
- Because retrieval depth differed, this is not a controlled model comparison.

**What I checked:** every line of the diff, all 12 current articles, every author disposition (including my Optional and Limits items), and regressions in correctness, coverage and comprehensibility.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1802 | words/分かれる.md | CLEAN | CLEAN | CLEAN | B91-01 resolved: 別 added. Existing pairs with 別れる and 割れる are confirmed. |
| N2:1803 | words/若々しい.md | CLEAN | CLEAN | CLEAN | Unchanged. The immature-sense qualification is correct. |
| N2:1804 | words/湧く.md | CLEAN | CLEAN | CLEAN | The attested 拍手が湧く replaces 歓声が湧く, and the wording about the two separate words is fixed. |
| N2:1805 | words/詫びる.md | CLEAN | CLEAN | CLEAN | B91-05 resolved: the register contrast matches Daijisen's 謝る usage note, presented as a tendency. |
| N2:1806 | words/和服.md | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1807 | words/割合に.md | CLEAN | CLEAN | CLEAN | The retained degree-adverb exclusions are defensible pair by pair. |
| N2:1808 | words/割り算.md | CLEAN | CLEAN | CLEAN | B91-02 resolved: 等分 added. |
| N2:1809 | words/割と.md | CLEAN | CLEAN | CLEAN | Same degree-adverb assessment as 割合に. |
| N2:1810 | words/割引.md | CLEAN | CLEAN | CLEAN | The 低下 and 割る pairs are retained; neither is shown to be excessive. |
| N2:1811 | words/椀.md | CLEAN | CLEAN | CLEAN | B91-04 resolved. お椀 and 杯 are taught, counter recognition is kept, and the unchecked いちわん reading was removed. |
| N2:1812 | words/碗.md | CLEAN | CLEAN | CLEAN | B91-03 resolved. 茶碗 and 杯 (さんばい) are taught, and the わん counter is kept. |
| N2:1813 | words/ワンピース.md | CLEAN | CLEAN | CLEAN | Unchanged. |

**Mappings: CLEAN.** All twelve are unchanged and remain compatible with their families. That includes わりあいに → 割合に, 割算 → 割り算, and 椀 and 碗 as separate entries (1562780 and 1562840).

**Baseline and kanji preservation: CLEAN, based on the supplied content.** No reuse is claimed. The supplied 算 article matches the original narrow patch: metadata and unrelated teaching are preserved.

**Components: CLEAN.** All twelve kanji arrays are complete. Links go only to existing cards (分, 若, 和, 服, 割, 合, 算, 引). No cards were invented for 湧, 詫, 椀 or 碗. The new links (ちゃわん.md and Daijisen 杯 and 謝る) use valid relative or https forms.

**Reciprocity: CLEAN.** 割り算 links to `kanji/算.md`, and 算's Common words section links back to 割り算.

**Quiz changes: CLEAN.** The two added pairs are justified directly by overlapping meanings. Nothing was removed, and no new pair is excessive.

**Final: ACCEPT.**

## Findings

**B91-01 · Minor · coverage (quiz) · words/分かれる.md:9 — RESOLVED**
- **Change:** 別 is now in 分かれる's exclusions.
- **Why the pair is needed:** The overlap is in meaning, not just the shared English word "separate":
  - JMdict 1606600 sense 2 is "to separate".
  - Daijisen's 分かれる senses include べつべつになる ("become separate") and 差異を生じる ("differences arise").
  - JMdict 1509430 sense 2 for 別 is "separate, different".
- **Mechanics:** One declaration covers both directions.
- **Regression:** None.
- **Confidence:** High.

**B91-02 · Minor · coverage (quiz) · words/割り算.md:9 — RESOLVED**
- **Change:** 等分 is now in 割り算's exclusions.
- **Why the pair is needed:** 等分's whole family and body teach division into equal parts. Its label, "division into equal parts", is a defensible alternative answer to "division (mathematics)", and the reverse also holds. I accept the author's basis: this is a direct overlap, not one inferred through the existing 等分/割る pair.
- **Confidence:** Medium-high.

**B91-03 · Minor · correctness/coverage · words/碗.md:19–28, 56–58 — RESOLVED; naturalness allegation WITHDRAWN**
- **Change:** The examples now use 茶碗にご飯をよそいました and ご飯を三杯食べました, as I proposed. 杯 and さんばい are taught.
- **Support:**
  - JMdict 2019640 sense 2 is "counter for cupfuls, bowlfuls".
  - Daijisen's はい counter heading gives 「御飯を三ばい食べる」 and the rule that it is read ばい after ん.
- **Withdrawn:** My stronger claim that the original standalone 碗 sentences were unnatural was never established. The missing JMdict priority tags do not prove rarity or formality. That claim is now moot rather than unresolved.
- **Status labels:** The author calls this "partially resolved". The difference is only a label; no actionable defect remains.
- **Confidence:** High that the defect is fixed.

**B91-04 · Minor · coverage · words/椀.md:19–26, 54–56 — RESOLVED**
- **Change:** The article now uses お椀 and みそ汁を三杯, and teaches 杯.
- **Counter recognition:** It keeps the わん counter through the attested Daijisen example 一―の吸い物.
- **Reading removed:** The previously unverified reading いちわん was removed rather than asserted.
- **Confidence:** High.

**B91-05 · Minor · correctness/coverage · words/詫びる.md:34–37, 46–48 and the closing citation — RESOLVED**
- **Evidence now available:** The supplied Daijisen 謝る usage note says:
  - The two verbs are interchangeable (相通じて) in some uses.
  - 謝る is mostly everyday speech (日常の口語として多く).
  - わびる is more formal (改まった言い方) and is used for serious faults or in writing (文章語).
  - お詫び in お詫び申し上げます cannot be replaced by お謝り.
- **Change:** The article now states this as a tendency. The misleading line implying no difference in formality is gone, while the points about exact words and forgiveness are kept.
- **Provenance:** This is verification by the author's evidence, not by my retrieval. My three original attempts remain failures.
- **Confidence:** High.

**My earlier Limits items:**
- **Degree adverbs on 割と/割合に (だいぶ and the others): accepted as defensible.**
  - だいぶ uses the 大分 entry (1414920); I did not import 大部's "fairly" gloss.
  - Daijisen describes the adverbs だいぶ and 割に both with 思ったよりも ("more than expected"). Daijisen's 割合 adverb describes a degree exceeding comparable cases.
  - The other pairs have their own direct glosses meaning "fairly / quite / rather" (1590560; 1401240 sense 5; 1599420 sense 1; 1372800 sense 1).
  - I did not rely on a chain through かなり. Excluding these costs only distractors, and no learning harm is shown.
- **椀/碗 with カップ and 湯飲み: retained, no defect.**
  - For 碗 the overlap is well supported: KANJIDIC gives "tea cup", and 茶碗 means "teacup".
  - 椀/カップ is the weakest of these pairs, but Daijisen's combined わん heading does not tie the meaning to one material.
- **割引/低下: retained.** Daijisen sense 3 of 割引 ("rate somewhat lower") gives a direct overlap.
- **Uncertain pair statuses: closed.** The current front matter shows 分かれる excludes 別れる and 割れる, 椀 and 碗 exclude each other, and both exclude ちゃわん.
- **My withdrawn hypotheses stay withdrawn:** 割引/割る (割る "to discount") and 割り算/割れる (割れる "to be divisible").

**New actionable findings:** none.

## Optional

- **椀.md:24–25 and 碗.md:25–27:** Daijisen actually prints 一―の吸い物, where the dash stands for the headword わん. The articles render it as 一椀. In the 碗 article, consider noting that 一碗 is equally valid (JMdict 1562840 sense 2 supports 碗 as a counter).
- **碗.md:17–20:** "It also counts bowls" comes right before an example using 杯. A short lead-in such as "everyday sentences use 茶碗 and 杯" would prevent a momentary misreading.
- **一椀:** Add a reading only if a source verifies it.
- **詫びる:** Optionally add Daijisen's nuance that わびる strongly expresses one's feelings in words or manner (非礼をわびる).
- **分かれる/枝:** Keeping 枝 deferred is reasonable. Alternatively, a verb-marked title such as "branch off; split; separate" would remove the ambiguity.
- **Still deferred and nonblocking:** 値引き and 割増し for 割引, 割に, ツーピース, and 膳 (unverified).

## Limits

- **Nothing executed:** No Git, hash, manifest, validator or app runs. Committed status, the six-files-changed scope, the 84→86 count and the unchanged-file claims are author assertions.
- **Evidence origin:** All new evidence was supplied by the author, and the dictionary wrappers come from one authority (Digital Daijisen). Failed author requests (お椀, 一椀, 一碗) and my failed 謝る fetches verify nothing.
- **Quiz calibration:** The retained degree-adverb and vessel pairs are judgments from dictionary descriptions. There is no learner data or live quiz run.
- **Not verified in the supplied evidence (unchanged, low-consequence lines):** お椀 as "the familiar prefixed form" and 会場が沸く.
- **Naturalness of the original bare 碗/椀 sentences:** neither established nor refuted. It no longer matters because those sentences were replaced.
- **Older bodies not supplied** (for example 沸く, 別れる, 比較的) were not reread.
- **Status of this review:** CLEAN is scoped. This is not native-speaker, frequency, corpus or runtime certification, and the unequal process means no model ranking can be drawn.
