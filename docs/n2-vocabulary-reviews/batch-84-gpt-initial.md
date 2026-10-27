## Snapshot: 04e39de5d1d0055ec6702a224270bffa57e188e6; committed content only

Parent: `bf0edffe59470653020849eb7cbb23614bba9495`. This review uses the supplied frozen snapshot. File tools cannot execute Git; commit membership, cleanliness, hashes, and equivalence checks were not independently executed.

## Scope: gpt-6.1-sol; family gpt

Completed the required reads: repository instructions; `docs\content-format.md:18–103`; the TSV header and **only physical rows 1662–1681**; all twenty complete assigned articles; complete `税`, `接`, and `材` kanji bodies; and `related.patch`. Read all **20 mappings, 20 complete principal families, 30 component records, and 291 comparison labels** through the specified lossless bounded JSONL ranges, including restrictions, flags, inherited POS, raw fields, and selected senses.

Additional complete reads comprised `family-inspection-01.txt` through `family-inspection-13.txt`, `supplemental-comparison-reading.txt`, and `final-precard-comparison-reading.txt`. I inspected **54 distinct complete older bodies**: 40 in `old-body-inspection-01.txt` through `05.txt`; ten in the supplemental/final old-body captures; and direct bodies for `つまらない`, `偶然`, `たまたま`, and `寝る`. I have not independently calculated a deduplicated count of the additional comparison families.

Read all **307 lines of `public-bodies.txt`**, covering twenty applicable Digital Daijisen captures through Weblio—**one dictionary authority**, not twenty. Unrelated works and other readings were not treated as corroboration. Two supplementary public retrievals for `つまらない` yielded no usable lexical evidence and were not counted as verification. No prohibited ledgers or rationale-bearing source file was read. **78 sequential read-only tool calls; no agents, edits, or concurrent work.**

## Verdicts: three articles need direct quiz-exclusion fixes

**Correctness includes quiz-answer ambiguity. Scoped coverage concerns the assigned lexical teaching, not exhaustive dictionary expansion.** CLEAN means no actionable defect established within the actual inspection.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1662 | めちゃくちゃ | NEEDS FIX | CLEAN | CLEAN | R84-01: missing direct guard with つまらない. State, attachment, and additional intensifier use are distinguished. |
| N2:1663 | めっきり | CLEAN | CLEAN | CLEAN | Noticeable-change tendency is not presented as an absolute rule; broader recorded degree use is qualified. |
| N2:1664 | めでたい | NEEDS FIX | CLEAN | CLEAN | R84-03: ironic personal use overlaps 馬鹿’s displayed “foolish.” |
| N2:1665 | メニュー | CLEAN | CLEAN | CLEAN | Food, planned program, and computing recognition are distinguished; French origin is supported. |
| N2:1666 | めまい | CLEAN | CLEAN | CLEAN | めまいがする and symptom meaning are clear; separate げんうん identity is not merged. |
| N2:1667 | 目安 | CLEAN | CLEAN | CLEAN | Practical criterion and rough-estimate uses are covered with useful attachment. |
| N2:1668 | 免税 | CLEAN | CLEAN | CLEAN | Fiscal exemption, suru usage, and eligibility qualification are sound; reciprocal 税 link is present. |
| N2:1669 | 面積 | CLEAN | CLEAN | CLEAN | Measured area, square units, and contrast with region/volume are clear. |
| N2:1670 | 面接 | CLEAN | CLEAN | CLEAN | Applicant/conductor roles and particles are distinguished; employment is a tendency, not a categorical restriction. |
| N2:1671 | 面倒くさい | NEEDS FIX | CLEAN | CLEAN | R84-02: missing つまらない guard for “tiresome.” Source 面倒臭い and primary めんどうくさい are explicit. |
| N2:1672 | 儲かる | CLEAN | CLEAN | CLEAN | Godan/intransitive teaching and profit-versus-revenue distinction are sound; public saving use is separately attributed. |
| N2:1673 | 儲ける | CLEAN | CLEAN | CLEAN | Ichidan/transitive money and child senses are taught; luck recognition and 設ける are distinguished. |
| N2:1674 | 申し訳ない | CLEAN | CLEAN | CLEAN | Apology, apologetic gratitude, and polite forms are explained without an absolute grammatical prohibition. |
| N2:1675 | モーター | CLEAN | CLEAN | CLEAN | Electric-motor tendency is qualified; motor, engine, and containing machinery are distinguished. |
| N2:1676 | 木材 | CLEAN | CLEAN | CLEAN | Material scope includes manufacturing/pulp; applicable reading もくざい is distinguished from きざい. |
| N2:1677 | 目次 | CLEAN | CLEAN | CLEAN | Contents list is distinguished from actual contents, index, and individual items. |
| N2:1678 | 潜る | CLEAN | CLEAN | CLEAN | もぐる/1609715 is preserved; diving, getting underneath, and hiding are taught separately from くぐる and obsolete むぐる. |
| N2:1679 | もしかしたら | CLEAN | CLEAN | CLEAN | Tentative possibility is taught without fixed probability bands or automatic coincidence interpretation. |
| N2:1680 | もしかすると | CLEAN | CLEAN | CLEAN | Separate identity is preserved; identical answer title deduplicates without requiring a mutual guard. |
| N2:1681 | もたれる | CLEAN | CLEAN | CLEAN | Physical support and stomach senses have appropriate particles; dependent-use recognition is separately sourced. |

**Mappings — CLEAN:** All twenty source associations preserve the inspected identities and selected-sense scope. Additional recognition is not presented as an independent N2 assignment to every recognized sense. The 面倒臭い mapping preserves the source spelling and distinguishes めんどうくさい from shorter めんどくさい. The malformed 潜る raw gloss is preserved as evidence, not converted into teaching “drive”; shared spelling does not merge entries 1609715 and 1609710.

**Components — CLEAN:** Primary written-Han metadata and substantive links to existing component cards are appropriate. Kana-primary alternate spellings do not require importing their characters into primary metadata. No missing cards should be invented for 免, 儲, or 潜.

**Reciprocity — CLEAN:** The three primary pairs are present in both directions: **免税 ↔ 税**, **面接 ↔ 接**, and **木材 ↔ 材**.

**Kanji preservation — CLEAN against the supplied patch:** Metadata and unrelated teaching remain intact in all three complete bodies. The patch adds or links the relevant vocabulary and receipts without replacing existing instruction. **Repository-wide absence of baseline-word edits remains independently UNVERIFIED** because Git could not be executed; the frozen snapshot reports twenty additions and no baseline-word edits.

## Findings: three missing direct guards

1. **R84-01 — Moderate; Correctness, quiz ambiguity.**

   **Location:** `words\めちゃくちゃ.md:4–9`; comparison `words\つまらない.md:4,15–19,31–33`.

   **Claim/impact:** めちゃくちゃ’s displayed title includes **“absurd,”** but neither card declares their direct exclusion. The complete inspected family for **つまらない, entry 1008190, sense 3**, includes “absurd; foolish; silly; stupid.” Its ordinary dismissive use is not confined to boredom: the “absurd” answer component can reasonably describe つまらない in that use. The different primary title **“boring”** does not deduplicate the labels, allowing an ambiguous English-to-Japanese question.

   **Minimal remedy:** Add `つまらない` to めちゃくちゃ’s `quiz_exclusions`; no level, title, or older-body change is required. Symmetry supplies the reverse guard.

   **Evidence/confidence:** Complete family in `batch-84-family-inspection-01.txt`, actual older body, and both inspected metadata records. **High.**

2. **R84-02 — Moderate; Correctness, quiz ambiguity.**

   **Location:** `words\面倒くさい.md:4–9,16–22,35–37`; comparison `words\つまらない.md:4,15–19`.

   **Claim/impact:** The displayed **“bothersome; tiresome”** overlaps つまらない’s ordinary boring/tedious use, but the pair is unguarded. This is not an assertion that the Japanese adjectives are freely interchangeable: the English component **“tiresome”** can reasonably describe the boring repetition illustrated in the older body. The existing direct guard with 退屈 does not protect this separate pair.

   **Minimal remedy:** Add `つまらない` to 面倒くさい’s `quiz_exclusions`. Do not expand this into a clique of evaluation adjectives.

   **Evidence/confidence:** Principal **1533560, sense 1**; complete **1008190, sense 1**, including “tedious”; actual older-body repetition example; and the assigned article’s own tiresome/boredom distinction. **Medium-high.**

3. **R84-03 — Moderate; Correctness, quiz ambiguity.**

   **Location:** `words\めでたい.md:4–9,22–25`; comparison `words\馬鹿.md:4,15–17`.

   **Claim/impact:** The taught ironic, too-trusting personal use can reasonably receive the answer **“foolish,”** already displayed on 馬鹿, yet neither card excludes the other. The article’s example—believing an implausible story—supports that overlap directly. This concerns the critical personal use, not celebration, general association, or inherited exclusions from おめでたい.

   **Minimal remedy:** Add `馬鹿` to めでたい’s `quiz_exclusions`, preserving 馬鹿’s existing easier level and teaching.

   **Evidence/confidence:** Complete **1608630, sense 2**, with its cross-reference to **おめでたい/1647360, sense 2**; that complete family’s foolish/naive use; the actual おめでたい and 馬鹿 bodies; and めでたい’s own example. **Medium-high.**

## Optional: none

## Limits: provenance and comparison breadth

Git/hash/equivalence assertions remain supplied provenance, not independently executed reviewer checks. Kanji preservation conclusions are relative to the complete inspected bodies and supplied patch, not an independently generated parent-to-commit diff.

The exclusion review is not an exhaustive certification of every possible pair behind the 291 labels. `old-body-inspection-06.txt` through `24.txt` were not read; prepared availability and author read totals were not counted as my inspection. All consequential pairs reported above have complete relevant family evidence and actual older-body inspection. No actionable excessive guard was established strongly enough to report.

The public captures constitute one dictionary authority, and the two unsuccessful supplementary retrievals add no corroboration. CLEAN judgments are scoped review outcomes, not exhaustive correctness or native-speaker certification.
