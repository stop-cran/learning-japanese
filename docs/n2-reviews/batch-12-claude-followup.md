## Snapshot
Correction checkpoint `55afc4add77d21ec8c8aae013bac072d39e9e881`, committed files only. The initial snapshot was `dfe4fb06ebb16b9a224e63b56f23a787b8502880`. I could not run Git or any command, so the following rest on the author's word:
- the commit identity, clean worktree and 14-file scope;
- zero validation errors and the 180/550 counts;
- preservation of the 52 records and the byte-identical manifest.

## Scope
- **Model:** claude-opus-5.5 (claude family). I worked alone and sequentially, with no edits and no sub-agents.
- **Diff:** I read the whole of `n2-batch-12-correction.diff`: 481 lines, 13 hunks, 8 files. That is four hunks in `batch-12.json` plus 汗, 沈, 況, 泉, 汚す ×2, 沈める ×2 and 泊める.
- **Revised pages read completely:** kanji 汗, 沈, 況 and 泉; words 汚す, 沈める and 泊める.
- **Source record:**
  - The added records 汗する (2463120) and 静める/鎮める (1594280), plus their primaryWords additions.
  - The working-tree primaryWords list (lines 400–520), which contains both new entry IDs.
  - The complete 沈める record (1431680).
- **Quiz checks:**
  - Titles and exclusions of the neighbouring words 下げる, 下ろす, 降ろす, 下がる, 汚れる, 汚い, 汚染, 土, 沈む, 泊まる, 宿泊 and 止める.
  - A title search across `words\` for lower, stain, soil, dirty, sink, lodge, overnight, put up, calm and quiet.
  - `docs\content-format.md:38-50,78-109`, `docs\confusable-words.md`, and context at `words\汗.md:12-36` and `words\汚れる.md:30`.
- **Own report:** `docs\n2-reviews\batch-12-claude-initial.md`.
- **Fetched:** AH "soil", AH "stain" and Oxford Learner's "put up".
- **Not read:**
  - The 6 files of the 14-file commit that are not in the diff.
  - The other family's report and all forbidden ledgers.
  - The 11 pages not revised, which keep their initial same-snapshot verdicts.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\汗 | CLEAN | CLEAN | CLEAN |
| kanji\沈 | CLEAN | CLEAN | CLEAN |
| kanji\況 | CLEAN | CLEAN | CLEAN |
| kanji\泉 | CLEAN | CLEAN | CLEAN |
| words\汚す | CLEAN | CLEAN | CLEAN |
| words\沈める | CLEAN | CLEAN | CLEAN |
| words\泊める | CLEAN | CLEAN | CLEAN |

## Findings
No defects remain. Status of earlier and new claims:

**Resolved**
- **B12-01 (`kanji\汗.md:40`):** The card keeps 汗をかく and now attests 汗する あせする, "perspire".
  - This matches pinned record 2463120: a suru verb, intransitive, "to perspire; to sweat", with no spelling or reading flags.
  - The card makes no frequency claim. That is better calibrated than my original remedy, because the record has nothing to support a ranking.
- **B12-02 (`words\汚す.md:28-29`):** 汚し is now called the masu-stem (汚します), and the negative is given as 汚さない rather than 汚しない. This is correct for a godan verb.
- **B12-03 (`words\沈める.md:48-50`):** The homophone is now named: 静める/鎮める しずめる, "quiet; calm", a transitive ichidan verb.
  - The citation of 1594280 senses 1-2 is accurate; those senses carry no spelling note.
  - The page claims no exclusive spelling rule. The "esp. 鎮める" notes on senses 3-5 are not overstated.
- **Initial Optional #3, #4 and #5 (沈:45, 泉:41, 況:44):** The reading-list wording, the season-versus-water-source wording and the emphatic-comparison wording are now accurate and clear.

**Calibrated (my initial view superseded)**
- **Initial Optional #6 (汚す/汚れる):** I had called this exclusion optional; it is warranted.
  - AH has intransitive "soil": "To become dirty, stained, or tarnished". AH also has intransitive "stain": "To produce or receive discolorations".
  - The repo itself renders 汚す as "get … dirty" (`words\汚す.md:16` and `words\汚れる.md:30`). So each title is a reasonable answer for the other word, which meets the rule at `content-format.md:95`.
  - My precedent argument was weak. 止める marks "something", while 壊す/壊れる and 沸く/沸かす are older unexcluded pairs, not a standard. I am not demanding that those be cleaned up.
- **泊める title:** I originally judged this low-risk. Oxford, however, attests intransitive "put up (at…)", meaning "to stay somewhere for the night", so the old second gloss "put up overnight" could be read as 泊まる's "stay overnight".
  - The new "put someone up overnight" fixes this. It agrees with Oxford's "put somebody up": "to let somebody stay at your home".
  - No pair with 泊まる is needed. The host-versus-guest choice is the intended contrast, as with 止まる/止める.

**Evaluated and accepted (new)**
- **沈める exclusions of 下げる, 下ろす and 降ろす:** Entry 1431680 sense 2 is "to lower (e.g. one's body into a chair)", and the article teaches it at lines 45-46.
  - The three neighbour titles are "lower; hang", "lower; take down" and "lower; unload; drop off". 下ろす also teaches 手を下ろす, "lower your hand".
  - A learner could therefore accept "lower" for 沈める, so the exclusions are justified.
  - Keeping 沈む is correct. The neighbours' own exclusions are unchanged.
  - 下がる ("go down; become lower", intransitive) does not need a pair.

**Carried forward unchanged:** Initial Optional #1, #2, #7 and #8 concern pages outside this correction. They were not re-reviewed and remain nonblocking.

## Optional
1. **Citation of 1594280 on 沈 (`kanji\沈.md:48`, `batch-12.json` primaryWords for 沈):** The card lists 1594280 as a word-pair entry, but that entry's spellings (静める, 鎮める) contain no 沈, and the card never mentions them.
   - This is harmless.
   - If the validator allows, either add a one-line Notes item naming the homophone or cite the entry only in the 沈める article.
2. **`words\汗.md:32` (unchanged, outside the narrow scope):** "Do not translate English 'I sweat' by adding する directly to 汗" now sits next to the card's attestation of 汗する.
   - It reads as everyday translation advice, so it is not a defect.
   - Possible wording: "Use 汗をかく for everyday 'I sweat'."
3. **`words\沈める.md:49-50`:** "a general verb for quieting a room" hints that there might be a narrow quieting use. Simpler wording would be "沈める itself does not mean quiet or calm."

## Limits
- **No Git or command execution:** see Snapshot for what rests on the author's word. I could not check the 6 commit files outside the diff.
- **Source manifest:** I only searched `docs\n2-source-snapshot.json` for batch references. I could not compute or compare any hash for `batch-12.json`.
- **Source records:** I confirmed records 2463120 and 1594280 against the diff and the working-tree primaryWords. Public evidence for both comes from Jisho searches in the initial session; EDRDG JMdictDB was password-protected.
- **Not re-reviewed:** the stroke files and the 11 pages that were not revised.
- **General limits:** batch-12 is a selected extraction, not the complete dictionary. These verdicts are not native-speaker certification.
