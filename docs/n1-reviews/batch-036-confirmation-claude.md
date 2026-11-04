Both corrections are resolved, and I found no regressions in the changed text. Both changed files are now CLEAN on all three facets. I made no edits.

**Snapshot:** c444a7fd31befdd9af1e1935cad6c54d04ee4021, as stated in the task. I couldn't check HEAD or the signature without a shell, so I read the working-tree files at that path. The supplied diff touches only `kanji/獣.md` and `words/獣.md`. I didn't open `words/獣医.md`, `manifest.json` or the stroke files, so "unchanged" for them rests on the task statement.

**Scope:** Claude Opus 5.5, continuing my own initial review of 47edd129. This is a correction confirmation that depends on that review, not a new blind initial review. I read, one call at a time:
- my initial report;
- the full correction diff;
- the current `kanji/獣.md` and `words/獣.md` in full;
- the full `words/生き物.md`;
- the full correction packet `batch-036-review-comparisons-jmdict.xml`, lines 1–29;
- the supplied Daijisen notation guide, lines 700–707.

I re-checked the けだもの (lines 1740–1783) and けもの (lines 1743–1787) Daijisen headings from my initial reading and didn't reopen them. I didn't repeat the original guidance, the 167 original families or the comparison inventory, and I didn't read the other reviewer's report or the author's records.

**Verdicts:**
- `kanji/獣.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words/獣.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- `words/獣医.md`: unchanged and not re-read. My initial CLEAN/CLEAN/CLEAN verdict carries over without re-reading it.

**Findings:**
1. **Resolved — けだもの spelling qualification** (initial finding 1, minor; coverage/comprehensibility).
   - **Change:** `kanji/獣.md` Notes (lines 62–64) and `words/獣.md` Meaning (lines 31–33) now say that writing 獣 for けだもの uses a reading outside the standard Jōyō reading table. They add that Daijisen's ▽ mark is about spelling, not a rare or obsolete pronunciation.
   - **Evidence:**
     - The supplied guide, section 5「表記」, part [2] item 1, says ▽ marks「常用漢字音訓表にない読み」(a reading not in the Jōyō reading table).
     - The original headings are け‐だ‐もの【▽獣】 and け‐もの【獣】, so only けだもの carries the mark.
     - The guide gives ▽ no rarity or register meaning. JMdict 1335590 gives けだもの the `ichi1` common-word tag, which fits the "not rare" wording.
     - The `#5` link in the citation matches the guide's `name="5"` anchor.
   - **Wording check:**
     - The new text keeps three things separate: whether the 獣 spelling is standard, whether the pronunciation is valid, and the existing warning about insulting use.
     - It makes no claim about which reading is the default or how frequent either is.
     - My initial remedy wording ("read けもの by default") would have been less precise, so leaving it out is better.
     - The readings table and the reading-question selection are unchanged.
   - **Confidence:** High.
2. **Resolved — 獣/生き物 quiz exclusion** (initial finding 2, minor; quiz labels).
   - **Change:** 生き物 is added once, at the end of `words/獣.md`'s `quiz_exclusions`. The other 15 entries keep their order.
   - **Evidence:**
     - JMdict 1378590 sense 1 includes the gloss "animal" alongside "living thing" and "living creature". 生き物's displayed title is "living thing; creature".
     - JMdict 1335590 sense 1 glosses 獣 as "beast; brute; animal".
     - The packet's only extra spelling, 生きもの, is search-only, and the reading has no restrictions. Nothing there affects the pair.
   - **Boundaries:**
     - This is one direct pair. It doesn't treat animal species as synonyms or exclude every living-thing category.
     - It doesn't touch 生き物's own file: its N3 level, title and 生物 exclusion are as I read them initially.
     - It doesn't rely on protection passing through 生物, since exclusions only work pair by pair.
   - **Confidence:** Medium-high, since whether "creature" fits as an answer still depends on how a learner reads it.

**Optional** (all still optional; none was needed for these two corrections):
- the "vet ≠ veteran" sentence in `獣医.md`;
- "my dog's" → "the dog's" in `獣医.md`;
- "wild animal" instead of "beast" in the `獣.md` example;
- recognition notes for the old form 獸, the archaic reading しし and the name けものへん for 犭;
- new: writing "Jōyō" with the macron for consistency.

**Limits:**
- The notation guide is evidence supplied by the coordinator; I didn't fetch it myself in this session. The only lookup I ever did myself was the Wiktionary check in my initial review.
- Every judgement on unchanged content depends on my initial scope.
- No native, phone, glyph-rendering, Android, CI, combined-main or publication checks were done; those remain pending.
- Every tool call in this session ran on its own. The initial review's single parallel-call breach is still recorded in that report.
- This report shows only my own assessment. It says nothing about whether the other reviewer agreed the defects needed fixing or covered the comparisons equally.
