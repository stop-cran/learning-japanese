All three corrections are clean, both of my original findings are resolved, and no consequential in-scope textual claim remains unresolved. This is a bounded confirmation of the changed passages only, not a second complete review.

**Snapshot:** Corrected teaching snapshot 0a5f2e23862c44df3a79c342fbcd5e5c1d376d29, compared against the original 9fee5174f695d5cbc1a45752e633c9622b011e38. No uncommitted teaching was involved. I did not inspect the regenerated manifest.

**Scope:** I am Claude Opus 5.5 (model ID: claude-opus-5.5). I made four tool calls, strictly one at a time:
- `docs\n1-reviews\batch-002-confirmation.diff`, in full (3 hunks).
- `kanji\稲.md`, in full.
- `words\水稲.md`, in full.
- `words\桑.md`, in full.

I did not reread the dictionary packets, because the JMdict entries 1371310, 1167820, 1247060 and 1534520 were already in my original read. I relied on my original reading of the `words\稲.md` and `words\木.md` headers. Both files exist and their titles are "rice plant" and "tree; wood".

**Verdicts** (correctness / scoped coverage / comprehensibility)

| File | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\稲.md` | CLEAN | CLEAN | CLEAN |
| `words\水稲.md` | CLEAN | CLEAN | CLEAN |
| `words\桑.md` | CLEAN | CLEAN | CLEAN |

**Checks behind the verdicts**
- **稲 mnemonic (line 24):** It now reads "above 旧 (a vertical stroke to the left of 日)". That fixes the missing stroke: 禾 (5) + 爫 (4) + 丨 (1) + 日 (4) = 14, matching KANJIDIC2. Your KanjiVG breakdown (旧 = 丨 on the left + 日 on the right; stroke 10 is the vertical, 11–14 are 日) agrees. The "not etymology" label is still there, and no historical claim was added. No other line changed.
- **水稲 exclusion (line 8):** `quiz_exclusions: [稲]` is a single, correctly formed key. The target exists, is not the article itself, and is not in a `quiz_distractors` list (水稲 has none). It applies in both directions. It fits the article's own wording that 稲 is "the broader plant word" (line 27), and it does not claim the two words are synonyms.
- **桑 exclusion (line 8):** `quiz_exclusions: [木]` is formed the same way and fits the article's "木 き is the broader word for a tree" (line 25). It is a direct pair only, not a rule to exclude every tree.
- **Regressions:** none found. Titles, readings, quiz selections, links and body text are otherwise unchanged.

**Findings:** None.

**Reconciliation of my original observations**
1. **Finding 1** (the 稲 mnemonic left out the vertical stroke of 旧): **resolved** at 0a5f2e2.
2. **Finding 2** (no exclusion between 水稲 and 稲): **resolved**. This also clears the coverage NEEDS FIX I gave the reused `words\稲.md` for this pair.
3. **Optional 桑/木 exclusion:** **resolved** by being adopted. It stays optional-origin in my original report.
4. **Other optional items** (桑園 listed among common words, the おかぼ reading of 陸稲, the "dismissive" wording in 芋): still **optional**, and they do not block closure.
5. **Process note:** my original report disclosed one parallel read. Every read in this confirmation was serial.

**Optional:** None new.

**Limits**
- The KanjiVG evidence was supplied and inspected by you; I did not retrieve it myself.
- The dictionary evidence is the frozen extracts from the original read.
- How the app handles these exclusions is taken from the format documentation; I did not run it.
- My original limit on how reading keys from different kanji interact in the app still stands. It is out of scope here.
- This is a textual review only: no native-speaker, physical-phone or measured-learning certification.
