# Confirmation report: correctness facet (f5a9c5e8, against my findings from aca8b242)

## Snapshot and scope
- **Snapshot:** f5a9c5e8c8ae139398910cec196754efe7c033ab, compared with my own blind review of aca8b242.
- **Read in full:**
  - followup-diff-1 to 5
  - followup-revision-1 to 5
  - followup-facts.txt
  - correction-evidence.txt
  - correction-families.xml
  - confirmation-task.txt
- **Cards covered:** 尾, 屯, 峡, 峰, 崇, 崎, 巧, 駐, しっぽ, 上手い, 分岐, 山岳, 崇拝, 海峡, 駐屯.
- **Not re-read:** untouched cards (尿, 岐, 岳, 利, 峰/岬/利口 word cards, and so on). I rely on my baseline reading for those.
- **Not a fresh review.** No external pages, native-speaker check or device test.

## Verdicts
- **Cor (correctness): CLEAN** for the revised text.
- **Cov (scoped coverage): CLEAN.**
- **Cmp (comprehensibility): CLEAN.**

## Reconciliation of my findings

| ID | Finding | Status | Evidence |
|---|---|---|---|
| F1 | Five JMdict ids not cited | Resolved | All five are now cited: 1457320 (屯), 1503370 (分岐), 1302790 (山岳), 1426960 (駐屯), 1622730 (海峡). Each id's gloss in correction-families.xml agrees with the card wording. |
| F2 | 巧い needed a "usually kana" qualifier | Resolved | 巧 Notes and the 上手い card both now say it. The XML gives "usually written using kana alone" on all three senses of 1310460. |
| F3 | Garbled 崎 キ row | Resolved | It now reads "the word is rare, and キ is outside the standard-use table". |
| F4 | しっぽ had an unlinked 尾, and the exclusion was one-way | Resolved, with a limit | The link is added. しっぽ's own exclusions are unchanged, but 尾 excludes しっぽ in followup-facts. correction-evidence states "stored exclusions apply symmetrically". That is the author's assertion, and I cannot check the quiz builder. |

## Optional items (O1–O7)
- **O1, adopted:** 崎 Common words now lists さき and 岬. The distractor 岸 became 岩. The みさき row is reworded.
- **O7, adopted:** quiz-safety exclusions were added: 屯→拾, 崇→尚/貴, 巧→芸, 崇拝→憧れる, 上手い→上手. followup-facts lists all of them, and correction-evidence gives labels for each target card.
- **O2–O6, not adopted and still open:**
  - 巧み unquizzed; 利 lists 利巧 rather than 利口.
  - 尾 vs しっぽ register.
  - 小便 register.
  - 分岐 vs 分かれる formality.
  - Kanjipedia-only readings, e.g. 屯 チュン/なや.む, 岐 わか.れる/ちまた, 峰 フ, 崇 シュウ.
  - None is a defect.

## Regressions checked
None found.

- **屯する:** the revised たむろ row matches both senses of JMdict 2151610. That is people gathering or hanging out, and troops assembling or being quartered.
- **駐屯:** the "(of troops)" wording matches the JMdict gloss "stationing (troops)". The "intransitive verb" tag is intact; correction-evidence says so and the XML shows it.
- **峡 はざま:** the row is now source-only and cites Kanjipedia, which matches sources.json. The Daijisen claim is gone.
- **崎 / 岬:** the さき and みさき rows agree with entries 1297220 and 1611700. 崎 is the priority spelling of さき, and a non-priority alternate spelling of みさき.
- **崇拝 / 憧れる:** "without implying worship" is consistent with the 憧れる glosses (yearn, admire).
- **Exclusions:** 峰 Notes mention 岳 although 峰's own exclusions omit it. The facts file shows 岳 excludes 峰, and exclusions are symmetric on the author's word, so this is consistent.

## Source facts vs author observations
- **Source facts (packet XML and facts file):**
  - JMdict glosses and tags.
  - The exclusion tables.
  - The 1426940 tag retention.
- **Author-supplied, unverified by me:**
  - The Daijisen ね【峰／嶺】 reading for 峰. correction-evidence itself says it was "checked by the author, not the reviewers".
  - The Daijisen みさき【岬／崎】 gloss.
  - Quiz symmetry.
  - Existence of link targets. The card labels suggest the 拾, 尚, 貴, 芸, 上手 and 憧れる cards exist, but トン.md and 湾.md remain unverified.

## Remaining actionable issues
**None.**

## Optional ideas (non-blocking)
1. **尾 counter wording:** 尾 says "fish, shrimp and similar animals". JMdict 2247790 says "fish, shrimp, etc." Mirroring that would be safer.
2. **駐屯地 wording:** the card says "garrison or camp". The JMdict gloss for 1426960 is "garrison; military base". "Camp" comes from the archaic 屯 entry.
3. **上手 link:** the 上手い Synonyms section leaves 上手 (じょうず) unlinked, though it is now a quiz exclusion with a card.
