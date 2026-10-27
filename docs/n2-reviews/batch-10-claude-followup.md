## Snapshot
Revised frozen commit `a61167fec3c034abee9580d7edac20e2c077fe17`, committed files only. I can only read files, not run Git, so the commit, the clean checkpoint and the eleven-file correction scope are taken from your statement.

## Scope
Reviewer: claude-opus-5.5 (Claude family). I worked sequentially and read-only, with no delegation.

- **Read:**
  - My own initial report, `docs\n2-reviews\batch-10-claude-initial.md`.
  - The complete 358-line, 11-hunk diff, `n2-batch-10-correction.diff`.
  - The four revised pages in full: `kanji\板.md`, `kanji\枝.md`, `kanji\柱.md`, `words\柱.md`.
  - `words\棒.md`, as the comparison and exclusion target.
  - The quiz-exclusion rules (`docs\content-format.md:80-90`) and the source-record rule (`content-structure.instructions.md:16-17`).
  - The changed records in `docs\n2-batch-sources\batch-10.json`: 2012-2036 (板木 ばんぎ), 2038-2075 (板木 はんぎ), 2703-2860 (both 枝葉 records with the full family) and 3424 onward (棒). The file has 51 selected records and 14 `entrySpellings` blocks, which is 13 families because 1579520 appears twice.
- **Not read:** the other family's report, other review archives, ledgers, authoring notes, session inputs, and unchanged pages beyond their comparison labels.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\板.md | CLEAN | CLEAN | CLEAN |
| kanji\枝.md | CLEAN | CLEAN | CLEAN |
| kanji\柱.md | CLEAN | CLEAN | CLEAN |
| words\柱.md | CLEAN | CLEAN | CLEAN |

## Findings
**B10-板-01 (Minor, correctness): resolved.**
- `kanji\板.md:40` now names 板木 ばんぎ as a separate signal-board word that is distinct from the printing woodblock. This matches packet record 2868686, "wooden board struck with a mallet as a signal", and the earlier Jisho and Kotobank lookups.
- Line 41 now ties ハン to "the printing word 板木 はんぎ" and says the reading depends on the word and sense. That is a sense-qualified example, not a claim that 板木 is always read はんぎ.
- The ハン row at line 28 is kept, and footer line 44 adds 2868686.
- Confidence: high.

**Changes made for observations outside my findings: no regressions.**
- **`kanji\枝.md:39`:** えだは for branches and leaves, with the figurative sense "especially しよう", matches packet lines 2703-2860. Neither sense in 1579520 restricts which reading may be used, and sense 2 carries only "esp. しよう". The phrase "not exclusive reading compartments" correctly states a preference, not an exclusive rule. No frequency is asserted. Line 20 and the しよう row stay valid because sense 1 isn't tied to one reading.
- **`words\柱.md:8` and `words\柱.md:37-38`:**
  - The direct exclusion with 棒 is justified in both quiz directions. 柱 is shown as "pillar; mainstay" and 棒 as "stick; rod; pole", and English "pole" overlaps an upright post.
  - Japanese→English: with 柱 as the prompt, "stick; rod; pole" would be a semi-correct wrong choice. With 棒 as the prompt, "pillar; mainstay" would be the same.
  - English→Japanese: the same overlap applies in both directions.
  - One declaration covers both directions. The exclusion is pairwise only, so no transitive link to 支える, 援助 or 賛成 is implied or needed.
  - The comparison sentence matches 1519750 sense 1 and `words\棒.md`. The link target exists, and the footer cites "1519750, sense 1".
- **`kanji\柱.md:42`:** the only change is the footer, which adds 1519750. It is accurate as a source pointer. See Optional.

No actionable defect remains.

## Optional
- `kanji\柱.md:42` cites 1519750 (棒), but the kanji card never mentions 棒. It reflects the packet's per-card evidence list, which includes entries cited by the linked word article. You could note that or drop it. It doesn't affect learners.
- The other overlaps from my first report (台, 骨, 基 with 柱) are still not excluded. Nothing here makes them worse.

## Limits
- **Git:** I couldn't run Git to verify the commit.
- **Entry ID 2868686:** not confirmed against a public JMdict copy. EDRDG's JMdictDB asks for a password, which I didn't try to work around, and WWWJDIC returned no result rows. The headword, reading and sense come from earlier lookups.
- **板木 ばんぎ record:** the packet keeps it without its full spelling and reading lists. The 世界大百科事典 entry on Kotobank says the signal board may also be called はんぎ. The card claims no exclusive reading, so this isn't actionable.
- **Linguistic certification:** none. No native-speaker check and no frequency claims; validator and manifest weren't run.
