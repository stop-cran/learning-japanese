**Snapshot:** `7cc896f488ae5315046453777aae6768b9ff18e8`, identified as signed by the packet; no independent signature or Git verification.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), resuming my original batch083 review for **dependent, bounded changed-choice confirmation**, not a fresh blind review. Read exactly `C:\Users\stop-\n1-kanji-workspace\control\batch-083-choice-confirmation-packet.txt` in one whole-file `view` call with `forceReadLargeFiles=true`. The complete returned packet showed no truncation; no recovery reads or other resources were used.

Inspected all eight current article bodies, all 14 complete JMdict families, four complete raw KANJIDIC2 records, the exact diff, supplied audits and production-source excerpts. Earlier full-source conclusions are historical context, not claims of fresh rereading.

**Verdicts:**

| Article and bounded scope | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| `kanji\凌.md` — changed choice | CLEAN | CLEAN | CLEAN |
| `words\凌ぐ.md` — regression-only | CLEAN | CLEAN | CLEAN |
| `words\凌駕.md` — regression-only | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect in this scope.

**083-NATIVE-574-CHOICE: textually resolved; runtime acceptance outstanding.** The correction addresses the demonstrated mechanism, not merely the fixture’s expected label. `QuizViewModel.kt:91–97,155–157` constructs the candidate list after stack filtering. `QuizBuilder.kt:16–26` resolves curated IDs within that list and admits at most three wrong choices for default count four. 准, 冶 and 冴 all have current N1 metadata and distinct titles. Consequently, in the supplied complete N1 and All pools, all three curated choices fill the available slots; subsequent fallback iteration cannot add a substitute. Neither 次’s easier N3 level nor the algorithms or selected pools need changing. The captured 麟 fallback is not established semantically ambiguous.

The actual alternatives remain wrong for 凌’s **“endure; surpass”**:
- **准 — “quasi-; associate rank”:** correspondence, conformity, imitation and approval senses do not make that displayed answer a meaning of 凌.
- **冶 — “smelt; work metals”:** melting, figurative cultivation/training and pottery/casting do not validate that displayed answer for 凌.
- **冴 — “clear; sharp-minded”:** 冴える genuinely includes excelling at/deft execution, and 冴え includes skillfulness. Those overlaps do **not** make clarity or sharp-mindedness an ordinary translation of 凌. This is not a claim of universally disjoint synonym families.

That assessment includes the actual flags: rare 准 spellings versus search-only 順 forms, rare なずらえる pronunciation, kana-preference qualifications, 冱える/陵駕 rare spellings, irregular-okurigana 冴, rare 冴寒, negative-use qualifications and older intense-cold usage. Nanori remain separate from ordinary reading metadata.

The sole article change is `kanji\凌.md:13`. Full and selected 凌 readings, their linked rows, prose, word senses, identities and all 17 direct word guards remain unchanged; no regression is established. Keeping 次 as a linked visual comparison at lines 55–57 is coherent independently of quiz curation.

**Findings:** None remaining within the bounded textual confirmation. No new concern established.

**Optional:** None.

**Limits:** Static source reasoning and supplied availability audits are not executed QuizBuilder/Android acceptance. No independent upstream retrieval, manifest/hash recomputation or pool execution occurred. Corrected HOST/archive/fixture/APK checks, updated 30-Han inventory, 120 individual plus eight whole-word probes across four fonts, PNG inspection and later dependent visual checks remain pending. No device, font, drawing, UI, live-quiz, physical-phone, native-speaker or learning-effectiveness certification is given; custom, partial, larger, reverse-target and broad random-pool safety are outside this conclusion. No edits were made.
