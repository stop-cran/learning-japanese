# Confirmation report (correctness and scoped coverage)

**Snapshot:** 63ff44d350ec8d6be3b024d6c462119e1ac2ccb2, confirming my findings on the initial candidate 0ac3eaad07b20ba50997f128dfb78bba7c99e70a.

**Outcome:** both original findings are resolved. I found no regressions and no remaining actionable issues in my facet.

## What I read
- **Read this turn:** `followup-diff-1..3`, `followup-evidence-1..3`, `followup-dispositions`, `followup-revision-1..4`.
- **Not read:** `confirmation-task.txt`. The follow-up scope is the one the user gave me.
- **Not re-read this turn:** `rubric`, `quiz`, `primary.xml` and `families-*`. Where I cite JMdict facts not in the follow-up evidence, they come from my earlier full read. These are 憾む 2833583, 懲りる 1428190, 憂い 1540740 and 慕う 1514910.
- **Assumption:** the diffs are the complete set of changes. Cards not in the diffs are taken as unchanged. I did not re-review them.

## Reconciliation of original findings

| ID | Status | Basis |
|---|---|---|
| F1 懇談 "会議 is a formal meeting" | **Resolved** | The text now says 会議 is "a meeting held for discussion, planning or decisions, large or small". That matches the raw JMdict 1198360 and the 会議 card as I read it earlier. 話し合い is now "talking something over together", which matches the card title. The friendly/relaxed contrast with 懇談 is kept. |
| F2 憾 うら.む row links 恨み, which teaches only resentment | **Resolved** | The row now says the sense is "especially 憾み" and "the linked card teaches only the resentment sense". Raw 1289740 sense 2 has `s_inf` "esp. 憾み", glossed "matter for regret; regret". |

Optional items from my first report:

| Item | Status | Basis |
|---|---|---|
| 慕う: 憧れる (に) vs 慕う (を) | **Adopted, resolved** | Verified in the revised text. 憧れる takes に and 慕う takes を, as I read in the 憧れる and 慕う cards earlier. |
| 監督 "director" ambiguity | **Adopted, resolved** | Both occurrences now read "coach". |
| 遺憾 noun and adj-na, 遺憾な点 | **Adopted, resolved** | The tags now include noun. Raw 1159090 has both adj-na and n. 遺憾な点 rests on author-observed Weblio example sentences (evidence-2). |
| 奉仕 "without seeking reward" overstated | **Adopted, resolved** | It now reads "service or work for others or for a cause", which is consistent with raw 1515950 and the 奉仕 card. |
| 慶弔 translation adds "family" | **Adopted, resolved** | Example 1 no longer says "family". |
| 遺憾の意 is not an apology | **Optional, not adopted** | The card never claims an apology, so this is not a defect. |
| 遺憾に思う | **Withdrawn** | Not needed for the card's question. |
| 憤慨 vs 恨み | **Withdrawn** | No defect shown. |
| 感慨深げな vs 感慨深い表情 | **Withdrawn** | 感慨深い is a real entry (2272660), and the example is ordinary. |
| 懲りる sense-2 example, 懲りない as a separate entry | **Optional, not adopted** | Both senses are glossed and cited, and 懲りない appears in the example and grammar note. |
| Kanjipedia-only readings not taught | **Withdrawn** | This is the documented batch policy, and the progress notes record the reasons. |
| One-directional kanji exclusions | **Withdrawn** | Source fact (evidence-1, `content-format.md` lines 119–122): a declaration on either card excludes the pair in both directions. |
| No 善/慮 metadata ID update | **Withdrawn** | Evidence-1 shows 1315360 and 1540910 already present on both the base and revised Metadata lines. |

## Regression check
I checked every changed passage in correctness terms and found none. The raw entries are source facts from evidence-2 and evidence-3.
- **慨 なげく:** the narrowed claim "entry lists only 嘆く and 歎く" matches raw 1418090.
- **憂 愁い (うれい):** accurate against 1540740.
- **懲:**
  - 性懲りもなく (しょうこりもなく) matches raw 1882440.
  - The new note on 課, 習 and 学 and the misleading English cue is accurate.
- **遺:** "remain behind" is consistent with the 遺憾 card.
- **感慨:**
  - "Noun only, whereas 感動 and 感激 can also be する verbs" matches raw 1212310, 1212570 and 1212360.
  - Both 感じる and 感ずる are now excluded.
- **慶弔:**
  - The 慶弔見舞金 sentence is natural, and its translation fits raw 2873015.
  - The 弔事 vs 弔辞 note matches raw 2116690 and 1427690.
- **懲りる:**
  - The に and で grammar note is supported by the Meaning quotation.
  - The 羹 and 膾 explanation is consistent with raw 2002120 and 1957170, plus the author-observed Daijisen text.
- **遺憾:** 不満 exists as a card and is added to the exclusions. The な and の grammar is consistent with the raw adj-na and n tags.

## Verdicts on revised cards
| Card | Correctness | Scoped coverage |
|---|---|---|
| 慨, 憂, 憾, 懲, 遺 | CLEAN | CLEAN |
| 感慨, 慈善, 慕う, 慶弔, 懇談, 懲りる, 遺憾 | CLEAN | CLEAN |

Cards the diffs do not show were not re-reviewed. They keep my earlier CLEAN verdicts only on the assumption they are unchanged.

## Remaining actionable issues
None.

## Optional ideas (not consequential)
- **遺憾 grammar sentence:** です ends both noun and na-adjective sentences, so it does not distinguish them. Mapping な to the adj-na use and の to the noun use is the author's analysis, not a JMdict attestation. Softening it to "JMdict classifies it as both; 遺憾な点 shows adjectival use and 遺憾の意 is a set phrase" would be more precise.
- **Optional items still open:** 遺憾の意 is not an apology, and a 懲りる sense-2 example.

## Limits
- The Daijisen, 実用日本語表現辞典, standard-use table and Weblio example-sentence results are author-observed or author-attested. I did not verify them externally.
- The author's full-JMdict scans (no 慨 spelling with a なげ- reading, and 遺憾 as the only 憾 spelling with a priority tag) are author-run output. I could verify only the entry 1418090 spellings from the raw entry.
- Diff-3 adds only 1957170, 2002120 and 2873015 to the selection JSON. 慶弔.md now also cites 2116690 and 1427690. I cannot tell from the hunks whether those two were already in the list. This is a metadata question for the consistency reviewer, not a correctness issue.
- This is not a fresh whole-deck review, and there is no native or device verification.
