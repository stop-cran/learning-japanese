## Snapshot
- **Supplement commit:** `b75d1d1f75d56c67f2b5fc14b2c4d681c7c4da52`. Its parent is `2a93457f…`, which is the corrected commit from my earlier confirmation. The receipt marks it as clean committed content.
- **Content scope:** `words/写る.md` and `words/映る.md`.
- **Receipt hashes:**
  - Diff: `9d6e7afb…4399`.
  - 写る: `1ec473…4e96`. 映る: `39584b…5795a78`.
  - `batch-06.json`: `a5a699…9d85`, the same as before.
  - `manifest.json`: `12adac…f81f`. This changed from `101610…`.
- **Limit:** I only have file tools, so I couldn't run Git or recompute any hash. The two files on disk match the patch.

## Scope
- **Model:** claude-opus-5.5, fresh process. Read-only, no other agents.
- **Content reviewed:** the line-9 `quiz_exclusions` change in each article, giving four pairs: 写る/出る, 写る/現れる, 映る/出る and 映る/現れる.
- **Read:**
  - The snapshot, the patch and my earlier report.
  - Both changed articles in full, plus the 出る and 現れる cards.
  - `content-format.md` lines 62–92 and the `quiz_exclusions` rule in `copilot-instructions.md`.
  - The four complete JMdict entries pinned in `batch-06.json`: 1173710, 1321820, 1338240 (all 21 senses) and 1263510.
- **Not read:** other reports, the ledger, author notes and private inputs. I didn't review unchanged teaching, the official-guide attribution or kanji, and I searched no other files.

## Verdicts
Each cell gives correctness / scoped coverage / comprehensibility.

| Article | Scope | Verdict |
|---|---|---|
| 写る | Line 9 (+出る, +現れる) | CLEAN / CLEAN / CLEAN |
| 映る | Line 9 (+出る, +現れる; earlier exclusions kept) | CLEAN / CLEAN / CLEAN |

## Findings
**Labels compared:**
- 写る: "be photographed; appear in a photograph"
- 映る: "be reflected; appear on screen"
- 出る: "go out or appear"
- 現れる: "appear; become apparent"

**All four pairs are supported.**

1. **写る/出る.** The labels share "appear." 写る means "to be photographed." Its article translates 写りませんでした as "did not come out clearly," and "come out" matches 出る's "to come out" (senses 1 and 5). JMdict lists "to come out (photo)" under 映る, not 写る, so that direct gloss doesn't settle this pair. 出る sense 5 also covers "to show; to be exhibited." Appearing or showing up in a photo is a real overlap in meaning, though the two verbs don't swap freely.
2. **写る/現れる.** "Appear" is the main word of 写る's second label. 現れる sense 1 means "to appear; to become visible." A shape showing up in a photo or X-ray image is a natural overlap.
3. **映る/出る.** "Appear on screen" overlaps directly with 出る sense 5 ("to show; to be exhibited; to be on display"). 画面に地図が出ました ("a map came up on the screen") works alongside the article's own 画面に地図が映りました. JMdict 映る has "to be displayed (on a screen)."
4. **映る/現れる.** On-screen appearance overlaps with 現れる's "to come in sight; to become visible." The reflection sense differs, but the labels clash on "appear."

**Structural checks:**
- All targets exist. There are no self-references or duplicates, and each article has a single unquoted key.
- 映る still excludes 映す, 写る, 写す and 似合う.
- None of the four cards has `quiz_distractors`, so nothing conflicts.
- 現れる/出る and 写る/映る were already excluded from each other, so the four words are now all pairwise excluded.

**Regressions:** none. At N2 the quiz also draws on lower levels, so the pool stays large. This supplement implements the optional note from my earlier report.

## Optional
None.

## Limits
- **Git and hashes:** I couldn't confirm the commit, the parent or any hash.
- **Manifest:** its hash changed, but the patch has no manifest diff, and `manifest.json` wasn't in the allowed evidence. I didn't check whether it lists the two new article hashes.
- **Collocations:** judgments such as 画面に出る and 写真に現れる are my own editorial calls. I didn't check them against example sentences in a public dictionary, and I relied on the pinned JMdict glosses.
- **Native speaker:** CLEAN is editorial acceptance within this scope, not native-speaker certification.
