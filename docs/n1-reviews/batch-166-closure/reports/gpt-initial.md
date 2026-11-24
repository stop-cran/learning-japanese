**Needs fixes:** The packet is missing direct meaning-quiz exclusions, and the English label for 駐屯 can teach the wrong verb pattern. All 17 required mapped navigation pairs are present in both directions.

**Snapshot:** `aca8b242dcad188c7927dac74e708cc668de6995`, as identified by the packet; content version `6b5c0cb6871a6d99`. No uncommitted material was identified in the packet; commit and worktree state were not independently verified.

**Scope:** One blind reviewer, GPT-6.2 Sol (`gpt-6.2-sol`). Read all seven card bundles and all four comparison cards in full: **10 new kanji, 8 new words, 3 spelling reuses, and 1 additional comparison word**. Reviewed the six older kanji only at the changed hunks. Checked the rubric, quiz and label extracts, 11 primary XML entries, 10 source records, and all 90 families in `families-1.jsonl` through `families-6.jsonl`.

**Verdicts** — correctness / scoped coverage / comprehensibility. Grouped cards share the same verdicts; older kanji verdicts apply only to their excerpts.

| Cards | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Kanji 尾・尿・岐・岳・崎 | CLEAN | CLEAN | CLEAN |
| Kanji 屯 | NEEDS FIX | CLEAN | CLEAN |
| Kanji 峡 | CLEAN | NEEDS FIX | CLEAN |
| Kanji 峰 | UNVERIFIED | NEEDS FIX | CLEAN |
| Kanji 崇・巧 | NEEDS FIX | CLEAN | CLEAN |
| Words 尾・尿・分岐・山岳・海峡・峰・利口・しっぽ | CLEAN | CLEAN | CLEAN |
| Word 駐屯 | NEEDS FIX | CLEAN | NEEDS FIX |
| Words 崇拝・上手い | NEEDS FIX | CLEAN | CLEAN |
| Word 岬 | UNVERIFIED | CLEAN | CLEAN |
| Older kanji 分・利・山・拝・海 | CLEAN | CLEAN | CLEAN |
| Older kanji 駐 | NEEDS FIX | CLEAN | CLEAN |

**Findings**

1. **Moderate · meaning quiz · `words\上手い.md:4,30–32`.** 上手 and 上手い both answer “skillful; good at.” The card itself confirms the overlap, and neither label record excludes the other. The exclusions from 器用 do not protect this pair. Add `quiz_exclusions: [上手]` to 上手い; keep the distinction between the *na*- and *i*-adjectives and the existing taste-spelling guidance. **High confidence.**
2. **Moderate · meaning quiz · `kanji\崇.md:14`, `kanji\巧.md:14`, `words\崇拝.md:8`.** Add direct exclusions for **崇–尚** and **崇–貴**: both comparison labels include “esteem,” and the supplied 崇 record gives the reverence/esteem sense, including とうとぶ. Add **巧–芸** for the craft/skill overlap (`1278290` sense 2 and `2842968`), and **崇拝–憧れる** for admiration of a person (`1372870` and the displayed “yearn for; admire”). These are missing guards, not observed production collisions. **High confidence** for the esteem pairs; **medium** for the craft and admiration pairs.
3. **Moderate · meaning and consistency · `words\駐屯.md:4,11,15–18`, `kanji\屯.md:31,36`, `kanji\駐.md:37`.** “Garrisoning troops” makes *troops* sound like the object, but the article’s troops are the subject of 駐屯する. Replace the gloss throughout, including the quiz label, with **“being stationed (of troops)”**; retain the examples. Also reconcile record `1426940` in `families-3.jsonl:9`: `primary.xml` marks it intransitive, but the normalized record drops that tag. **High confidence.**
4. **Minor · source coverage · `kanji\峡.md:33`, `kanji\峰.md:33`.** The packet supports はざま and ね as recorded readings, but neither card links the Daijisen entry it invokes, and the packet does not contain the cited sense or literary examples. Cite the exact headings and retain the relevant excerpts in the evidence record. If those cannot be supplied, remove the extra Daijisen attribution for 峡 and describe 峰’s ね as a recorded, non-quiz reading without the unverified usage claim. **High confidence in the evidence gap, not a finding that either reading is wrong.**

**Navigation and counts:** Verified both relative links and the word reading for all **17/17 packet-defined pairs**, grouped by word: 尾←尾, 尿←尿, 駐屯←駐・屯, 分岐←分・岐, 山岳←山・岳, 海峡←海・峡, 峰←峰, 崇拝←崇・拝, 岬←崎, 上手い←巧, 利口←利・巧. Also verified the separate **尾↔しっぽ** comparison without assigning ぽ to 尾. The 10 source rows account for **28 metadata readings** (12 on, 16 kun); all are addressed in the cards. The **11 offered keys** (7 on, 4 kun) match the supplied projection, including `うま.い` → `うまい`. The packet lists **26 kanji** and **23 word** direct exclusion pairs; those counts do not establish completeness. The three reused writings retain their existing headwords and levels and do not inherit spelling-priority tags from the primary writings.

**Optional:** Label the spelling-priority field as excluding `nf*` ranks, or retain those ranks separately so readers can distinguish the filtered field from raw dictionary tags.

**Limits:** No external page, native-speaker, or device verification. The local evidence confirms 岬／崎 as みさき, but not the inherited lake-shore claim in `words\岬.md:15,30`; verify it against the cited みさき heading. The 30 named kanji meaning distractors were inspectable, but the packet does not establish runtime eligibility, fallback behavior, or whether an unoffered valid reading can appear as a wrong answer. The reported collision totals, baseline preservation beyond the supplied hunks, unchanged reverse links outside the 17-pair list, and manifest integration were not independently verified.
