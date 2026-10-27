## Snapshot
b943db187ef28180325d18358d1251547249d0bf, committed files only. I had file tools but no Git, so I couldn't confirm the commit hash, the clean worktree, the 60-file scope or the diff against 44231580a12fef12ac51b536d4baffe7ec2c3a57.

## Scope
Model: claude-opus-5.5 (claude family).
- **Read in full:** the 15 new kanji cards, `words\浴びせる.md`, `words\液体.md` and `words\湿度.md`.
- **Rules:** the two `.github` instruction files and `docs\content-format.md`:18-109.
- **Evidence:** all of `batch-13.json`, read in sections.
- **Related edits:** the new link passage in each of the 21 word articles. In `kanji\水.md`, the added distractor 木 and the five-elements line that links it.
- **Comparisons:** titles of existing cards, existing word titles and quiz exclusions, and `docs\confusable-words.md`. One jisho lookup (温もり).
- **Not reviewed:** the 15 stroke files, `docs\n2-source-snapshot.json`, the QuizBuilder code, the files you excluded, and the unchanged text of the related pages.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 浅 | CLEAN | NEEDS FIX (F1.1) | CLEAN |
| 浴 | CLEAN | CLEAN | CLEAN |
| 涙 | CLEAN | CLEAN | CLEAN |
| 液 | CLEAN | CLEAN | CLEAN |
| 涼 | CLEAN | CLEAN | CLEAN |
| 混 | CLEAN | NEEDS FIX (F1.5) | CLEAN |
| 清 | CLEAN | CLEAN | CLEAN |
| 減 | CLEAN | NEEDS FIX (F1.2) | CLEAN |
| 温 | CLEAN | NEEDS FIX (F1.6) | CLEAN |
| 測 | CLEAN | NEEDS FIX (F1.3) | CLEAN |
| 湖 | CLEAN | CLEAN | CLEAN |
| 湯 | CLEAN | CLEAN | CLEAN |
| 湾 | CLEAN | NEEDS FIX (F1.4) | CLEAN |
| 湿 | CLEAN | CLEAN | CLEAN |
| 準 | CLEAN | CLEAN | CLEAN |
| 浴びせる | CLEAN | CLEAN | CLEAN |
| 液体 | CLEAN | CLEAN | CLEAN |
| 湿度 | CLEAN | CLEAN | CLEAN |

## Findings
**F1: comparisons with existing cards are not linked.** Severity: Low. Facet: scoped coverage. Confidence: High.

The repository rules say to link words and kanji that have cards, at the main introduction or comparison (`content-structure.instructions.md`:20-21 and :55). Older cards follow this, for example `恋.md`:43 → `[変]`, `層.md`:39 → `[増]` and `戸.md`:42 → `[戻]`. Without links, learners can't jump to the antonym or the look-alike character. I confirmed every target below exists.

| ID | File:line | Unlinked mention | Add link to |
|---|---|---|---|
| F1.1 | `浅.md`:20 | 深い (antonym) | `../words/深い.md` |
| F1.2 | `減.md`:20 | 増 | `増.md` |
| F1.3 | `測.md`:41-42 | 計る; 則, 側 | `../words/計る.md`; `則.md`, `側.md` |
| F1.4 | `湾.md`:43 | 恋, 変 | `恋.md`, `変.md` |
| F1.5 | `混.md`:46 | 込む | `../words/込む.md` |
| F1.6 | `温.md`:46 | 暖かい | `../words/暖かい.md` |

量る and 暖 have no cards, so they stay as plain text.

The other checks found no defects:
- Every reading row matches KANJIDIC2. All 47 word examples use the correct reading and meaning, and the 11 rows with no dictionary example are honestly labelled.
- All 45 distractors are clearly wrong answers.
- No new title creates a synonym clash in the quiz fallback for older cards. The 16 starter cards that still have only two distractors share no tags with the new cards.
- 浴びせる's quiz exclusions cover 注ぐ, あびる, シャワー and 掛ける.
- All 21 related links are correct. 水's new distractor 木 ("tree, wood") is clearly wrong as an answer.

## Optional
- **O1:** Link the characters used in mnemonics: 青 (`清.md`:22), 戻 (`涙.md`:22), 夜 (`液.md`:22), 京 (`涼.md`:22) and 則 (`測.md`:22).
- **O2:** `測.md`:22 plays on English "rule": 則 means a regulation, not a ruler. This undercuts the warning at :42 to keep 則 separate from measuring. Rewording would help.
- **O3:** The ぬく row in `温.md`:35 is accurate and labelled, but its only example is an archaic insult. 温もり ぬくもり "warmth" is common, though usually written in kana (jisho/JMdict). 温まる ぬくまる is also in the batch evidence.
- **O4:** `湖.md`:44 mentions the こ suffix in lake names but gives no example name.
- **O5:** 清 and 湿 each list only one common word.

## Limits
- No Git, so the scope and the "unchanged" status of the related pages were not checked against the diff.
- I didn't check the 15 stroke files, which came from the converter.
- I didn't read `n2-source-snapshot.json`, so the source pins and hashes are unchecked.
- The quiz-fallback analysis relies on the documentation, not the QuizBuilder code.
- I didn't re-fetch the Daijisen (kotobank) citation for 浴びせる.
- The example sentences' naturalness is not certified by a native speaker.
