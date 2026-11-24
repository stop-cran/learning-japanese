**All three items left open in the previous confirmation are resolved within the supplied evidence.** I found no actionable regression or new optional suggestion.

**Snapshot and scope:** `9ffbf4529ac7585ca28fd623dbd64883f4699e04`, compared with `cfef4688ebb87df5d3532cac45d372ccf502da34` (initial blind candidate `dc46cc08608fa8714a68a36af77fb9ebd1b8fa37`). I read all five complete revised cards, the card and ledger diffs, and the final facts, trace, and reconciliation files. I cross-checked the relevant local JMdict entries and 恒 source record.

| Previous finding | Disposition | Confirmation |
|---|---|---|
| 恒 reading row made 常に sound exclusive | **Resolved** | `kanji/恒.md:33` now calls 常に the ordinary spelling, attributes outside-standard-use `つね.に` to Kanjipedia, and explicitly keeps it out of practice. The ledger matches the card. |
| 満悦 eligibility record contradicted itself | **Resolved** | Both 悦 mappings drop `exceptionReason`. JMdict `1526740` records `news2`, `spec2`, and `nf37` on both spelling and reading. The ledger correctly separates qualifying `priorityTags` from raw `readingPriorityTags` and follows the supplied owner decision that `news2` and `spec2` qualify. |
| 忠実 might offer valid まめ as a wrong reading | **Resolved for the supplied simulation** | JMdict `2827450` confirms まめ is valid. I checked the author-run trace and the code excerpt: neither the four generated look-alikes nor the four reachable corpus readings is まめ. The trace is from `cfef4688`; the author reports identical output for the nine new words at `9ffbf4529`. |
| Four direct exclusions; ご満悦 usage; 愁い spelling preferences; dictionary citations | **Resolved, unchanged** | No final diff reopens 忍ぶ–潜る, 忠実–ねっしん, 悼–愁, or 追悼–嘆く. 満悦 still leads with ご満悦 and retains 満悦する. The 愁い preferences and citation fixes are untouched. |
| 忍ぶ contrast with 隠す | **Optional, already addressed** | Neither passage changed in this round. |

**Regression check:** 忠実’s card change is spacing only. 恒例 now separates the Daijisen usage tendency from the JMdict gloss and the original workplace example. 恭しい’s irony note matches the author-recorded quotation and remains qualified. The diffs leave membership, reciprocal links, readings, offered keys, and distractors unchanged. The prior counts carry forward: **10 source rows, 9 new words, 1 N2 reuse, 16 reciprocal pairs, 25 reading rows, 10 offered keys, 30 fixed distractor slots, and 55 kanji / 49 new-word exclusion declarations**.

**Limits:** The owner comment, external dictionary checks, exhaustive priority scans, and mechanical gate results are supplied author evidence; I did not independently fetch or rerun them. No fresh whole-deck, manifest, native-speaker, or device review was performed.
