I found one minor clarity problem, in `words\楓.md`. I found no defects in `kanji\楓.md`, `kanji\楠.md` or `words\楠.md`.

**Snapshot:** commit `2a9ffe40c77c8fb74cd97c422932ddfe868a3248`. The prompt states that no uncommitted teaching changes are included. I did not check this independently because I had no shell access, and I edited nothing.

**Scope:**
- **Reviewer:** one reviewer, Claude Opus 5.5 (`claude-opus-5.5`). I made one tool call at a time and saw no overlapping calls.
- **Guidance read in full:** `.github\copilot-instructions.md`, `content-structure.instructions.md`, `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` lines 1–96.
- **Teaching files read in full:** `kanji\楓.md`, `kanji\楠.md`, `words\楓.md` and `words\楠.md`.
- **Source packets read in full:**
  - `batch-008-input-metadata.json`: all 8 on/kun readings. The metadata, strokes, radical and level match both cards.
  - `batch-008-jmdict.xml`: 39 families.
  - `batch-008-comparisons-jmdict.xml`: 13 families.
- **Comparison kanji read in full:** 風, 南, 村, 相, 木 and 葉.
- **Comparison words read in full:** 紅葉, 木, 植物, 植木, 植える, 木材, 材木, 材料 and 大木.
- **Live lookups:** both optional Kotobank pages.

**Verdicts:**
- **`kanji\楓.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`kanji\楠.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\楓.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility NEEDS FIX.
- **`words\楠.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

**Findings:**
1. **Severity:** Minor. **Facet:** comprehensibility. **File:** `words\楓.md:28`.
   - **Claim and impact:** The line says "do not use こうよう as the reading of the maple-tree example above." But there is no 紅葉 maple-tree example above it. Both earlier examples use 楓 read かえで. That example (庭に紅葉を植えました, read もみじ) is only in `words\紅葉.md`. A learner may not know which example is meant, or may wrongly think 楓 could be read こうよう.
   - **Remedy:** Say it directly: "When 紅葉 means a maple tree, read it もみじ, not こうよう." Alternatively, add that 紅葉 example with its kana.
   - **Evidence:** `words\楓.md` lines 17–18 are the only examples, and both are 楓/かえで. The もみじ example is in `words\紅葉.md`. The reading split is in JMdict 1578780 (こうよう, autumn colours) and 2857870 (もみじ, sense 1 "maple").
   - **Confidence:** high.

**Optional:**
- **`kanji\楓.md`:** Kotobank's Jitsū entry calls 楓 a phonetic compound, with 風 as the sound component. The card could cite this and add a hedge. Its current mnemonic is correctly labelled as not etymology, and leaving the phonetic field out is allowed.
- **`words\楓.md`:** It could mention the other spelling 槭樹 and the archaic かえるで (JMdict 2059188 is wrong; the entry is 2859188, archaic).
- **`words\楠.md`:** It could add an example that uses くす, or mention the common mixed spelling くすの木.
- **`words\紅葉.md`:** It mentions 楓 only as plain text. Linking it to the new `words\楓.md` would help navigation. This is a reused passage outside this review's scope.
- **Quiz exclusions:** Excluding 材料 on 楠 is cautious but harmless. I did not judge any exclusion to be missing. That includes 大木, 並木 and the other tree-species titles, whose labels are all different.

**Limits:**
- **Confusable pairs:** I searched `docs\confusable-words.md` instead of reading it in full, and found no relevant pairs. I did not read the remaining word titles; I only searched them for 40 tree/wood/plant/leaf titles. I did not list every kanji title the quiz could pull in as a fallback distractor.
- **Live lookups:**
  - The 樟 page confirmed Daijisen くす【樟／楠】 and Seisenban くすのき【樟・楠】/くす as an evergreen tree whose wood is used.
  - The 楓 page confirmed separate ふう and かえで headings, and Daijisen notes that かえで is a different species.
  - I did not fetch the 楠 surname page.
- **Unverified:** I could not confirm any modern word example for the four source-only on readings of 楠.
- **What this review is not:** It is text-only. I did no phone, rendering, native-speaker, frequency or learning-effectiveness checks, and ran no validator or manifest build. The JMdict packets are frozen evidence supplied with the task, not a fresh download.
