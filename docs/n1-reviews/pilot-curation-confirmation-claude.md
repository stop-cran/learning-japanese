# Bounded confirmation: pilot curation correction bb448a2

Both original findings are resolved, the optional polish is applied correctly, and the correction introduces no regressions. No consequential textual defect remains within scope.

**Snapshot:** revised bb448a25c522e9703d43e87216320c48a9121f1c, checked against the original reviewed b43173e10f158f59df49137394e1ebbfb0821393. This is a follow-up to my own initial review, not a new blind review.

## Scope
**Model:** Claude Opus 5.5 (claude-opus-5.5).

**Changed files and facets:** correctness, scoped coverage and textual phone comprehensibility for:
- `words/凹凸.md`: new exclusions and one new sentence.
- `words/幹.md`: new exclusions.
- `words/鷹揚.md`: one example sentence changed.

**Packets read, in full, one call at a time:**
- `packet-index.json`
- `teaching.diff`, lines 1–47
- `changed-articles.txt`, lines 1–134
- `comparisons-01.txt`, lines 1–171
- `comparisons-02.txt`, lines 1–139
- `dictionary.xml`, lines 1–298

Nothing was truncated or left out. I did not read `content-format.md` again or search any review archives. The exclusion behaviour (pairwise, applying in both directions) is carried forward from my earlier reading of `content-format.md:111`.

## Verdicts (correctness / scoped coverage / comprehensibility)
| File | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| words/凹凸.md | CLEAN | CLEAN | CLEAN |
| words/幹.md | CLEAN | CLEAN | CLEAN |
| words/鷹揚.md | CLEAN | CLEAN | CLEAN |

**Carried forward, not reread:** all 12 kanji cards, `words/矛.md`, and the changed passages of `words/氏.md` and `words/でこぼこ.md` stay CLEAN on all three facets. The diff confirms none of them changed. All 19 offered reading keys and all kanji metadata are untouched.

## Findings and reconciliation

**F1 (凹凸 exclusions): resolved.** Each new pair was checked on its own, without inferring from other exclusions:
- **差** "difference; gap" (JMdict 1291070, sense 1) against 凹凸's "disparity" (1179280, sense 2): this was the established collision, and it is now guarded.
- **違い** and **相違**, both "difference; discrepancy" (1158870 and 1400820, sense 1 each): "discrepancy" is close enough to "disparity" to justify excluding them.
- **ぶつぶつ**: its displayed label includes "small bumps" (1011200, sense 2: pimples; spots), against 凹凸's bumpiness sense (sense 1). The exclusion is defensible and conservative.
- **粗い** "coarse; rough" (1396910, sense 1) against 凹凸's "roughness" gloss (sense 1): defensible.

**F2 (幹 exclusions): resolved.**
- **柱** "pillar; mainstay" (1426480, sense 2) against 幹's "backbone" (1577640, sense 2) is now guarded.
- **地盤** "ground; supporting base" (1421420, senses 2–3: foundation; base) against 幹's base/foundation sense: the exclusion is defensible.

**Optional polish from my initial report: applied.**
- `words/鷹揚.md:18` now reads 小さな失敗には with "about small mistakes", which fits the "without fussing over small things" definition.
- `words/凹凸.md:31` adds that でこぼこ also has an imbalance sense, which matches 1582410 sense 2 (restricted to the でこぼこ reading). I had not called the original example a correctness error, and I am not reclassifying it now.

**Regressions: none found.**
- All eight new exclusion IDs exist; there are no duplicates or self-references.
- The original exclusions are preserved.
- Titles, readings, types and identities are unchanged.
- The same-spelling homographs in the dictionary packet (差 read さし, 2423450; 柱 read ちゅう/じ, 2424140; 柱 read じゅう, 2424150) are not used or transferred.
- The extra exclusions only shrink the pool of wrong answers; they don't make any choice incorrect.

## Optional
`words/凹凸.md:31`: "It also has…" is grammatically about でこぼこ. A reader might take it to mean 凹凸, but the statement is true of both, so this does not need changing.

## Limits
- All evidence is the supplied frozen JMdict families and the packet contents; I did no live retrieval and did not recompute hashes.
- I did not run the app; exclusion behaviour is taken from the documentation.
- There is no native-speaker, phone, publication or measured-learning certification. Native and publication acceptance remain separate and outstanding.
