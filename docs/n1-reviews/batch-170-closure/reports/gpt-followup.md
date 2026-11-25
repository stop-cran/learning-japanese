**The original card fixes are resolved. One evidence issue remains:** the supplied scan does not establish that 遺憾 is the only qualifying support for 憾 under the batch’s stated priority rule. I found no regression in the revised cards.

**Snapshot and scope:** GPT-6.2 Sol, confirming `63ff44d350ec8d6be3b024d6c462119e1ac2ccb2` against the blind candidate `0ac3eaad07b20ba50997f128dfb78bba7c99e70a`. I read all four revision files, all three diff files, all three evidence files, and the proposed dispositions. The diff covers five kanji, seven words, and two source records. It adds two direct exclusions and three citation IDs without changing the original 10 kanji source rows, 10 distinct mapped words, 18 reciprocal pairs, or 10 selected reading keys.

| Original finding | Disposition | Confirmation |
|---|---|---|
| 遺憾–不満 meaning quiz | **Resolved** | `words/遺憾.md:8` and the progress record both add `不満` directly. The documented pair rule is symmetric; no second declaration is needed. |
| 遺憾 noun and な-adjective coverage | **Resolved** | The noun tag and the contrast between 遺憾な点 and 遺憾の意 are present. JMdict 1159090 records both categories; the usage examples in the packet are author-observed. |
| 懇談 vs. 会議 and 話し合い | **Resolved** | The revised contrast no longer requires formality or a resolution, and preserves 懇談’s friendly, relaxed emphasis. |
| 慈善 vs. 奉仕 | **Resolved** | The revised contrast distinguishes charitable aid from service or work for others without imposing an unpaid-motive requirement. |
| 懲 vs. 課・習・学 | **Resolved** | The note now explains that the exclusions guard against misleading English cues, not shared Japanese meanings. |
| 慨 dictionary-wide negative | **Resolved** | The card and reading disposition now limit the claim to the spellings in entry 1418090. The supplied entry confirms 嘆く and 歎く; the broader scan is an author observation. |
| 遺憾 as the only qualifying 憾 route | **Partially resolved** | The scan supports uniqueness under its narrower filter, not under the stated batch policy. See below. |
| 憂慮–懸念 meaning quiz | **Withdrawn** for this snapshot | JMdict confirms the overlap, but the author’s inventory reports no `words/懸念.md`. There is no supplied card to exclude. |
| 感慨–感じる meaning quiz | **Resolved** | `words/感慨.md:8` and the progress record add `感じる` directly. JMdict 1212260 sense 2 supports the overlap. |
| Shared readings among kanji lookalikes | **Withdrawn** as a card defect | The documented prompt shows the written kanji and protects all its valid readings from wrong-answer use. The passing reading-options gate is author-reported, not a runtime check I performed. |

**Remaining actionable issue:** `docs/n1-sources/batch-170-progress.json`, `selectionNotes.憾` and `.遺`: the scan in `followup-evidence-1.txt` filters for `news1/ichi1/spec1/gai1`, while `selectionNotes.慶` explicitly says `news2` and `spec2` also qualify. Rerun the pinned scan with the full batch predicate and record its result, or narrow the uniqueness claim to the filter actually used. This does not undermine 遺憾 itself as valid support.

**Optional:** A 感概 search-only note remains optional; the revised card does not teach that spelling. Consolidating the overlapping citations in 感・談・産 also remains optional.

**Regression check and limits:** The supplied JMdict excerpts support the new 慶弔 terms and the cited proverb vocabulary; the three new citation IDs match the selection diff. No mapped link, selected reading, or prior exclusion was removed in the supplied diff. I reviewed the local excerpts, not the external pages, and did not rerun the author’s scans or gates or verify the manifest, native usage, a device, or the whole deck.
