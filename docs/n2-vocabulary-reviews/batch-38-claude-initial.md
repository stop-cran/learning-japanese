I found no correctness errors in the teaching content. There are five low-severity fixes: one missing quiz exclusion, three missing word links and one inaccurate mapping note. I reviewed using file tools only, with no Git, so I couldn't confirm the files match the commit or run any hashes. All files were read-only.

# Snapshot
`4ec7f6f7dabbe669a42d686fbd9ada6da362326a`, parent `368da250ef323ddef1609a7e0789a59c093fb6a7`. The receipt says the content is clean and committed; I reviewed what's on disk on that basis.

# Scope
- **Model:** claude-opus-5.5 (claude family).
- **New articles:** all nineteen read completely.
- **Reused 定規:** read in full, but only the narrow level/reuse change was assessed; this is not a whole-article review.
- **Kanji:** the full seven-file patch, plus all six edited kanji cards in full.
- **Mappings:** TSV rows N2:742–761.
- **Evidence JSON (bounded reads):** source rows, all twenty principal entries, the relevant component records, the 21 public lookup receipts, the grammar check, failed lookups and quiz declarations.
- **Comparison files:** only targeted records were read (通う, 詰める, 吸収, おめでたい, ガス).
- **Existing cards:** titles and exclusions for about 120 comparison cards, plus a keyword scan of all word titles for English-label collisions.
- **Fetched pages:** Bunpro てしょうがない and Weblio 巡査.
- **Forbidden files:** none read.

# Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 出勤 | CLEAN | CLEAN | CLEAN |
| 述語 | CLEAN | CLEAN | CLEAN |
| 出張 | CLEAN | CLEAN | CLEAN |
| 寿命 | CLEAN | CLEAN | CLEAN |
| 主役 | CLEAN | CLEAN | CLEAN |
| 受話器 | CLEAN | CLEAN | CLEAN |
| 循環 | CLEAN | CLEAN | CLEAN |
| 巡査 | CLEAN | CLEAN | CLEAN |
| 順々 | NEEDS FIX (B38-QZ-01) | CLEAN | CLEAN |
| 順序 | CLEAN | CLEAN | CLEAN |
| 純情 | CLEAN | CLEAN | CLEAN |
| 純粋 | CLEAN | CLEAN | CLEAN |
| 消化 | CLEAN | CLEAN | CLEAN |
| 小学生 | CLEAN | NEEDS FIX (B38-LNK-01) | CLEAN |
| しょうがない | CLEAN | CLEAN | CLEAN |
| 将棋 | CLEAN | NEEDS FIX (B38-LNK-03) | CLEAN |
| 蒸気 | CLEAN | CLEAN | CLEAN |
| 上級 | CLEAN | NEEDS FIX (B38-LNK-02) | CLEAN |
| 商業 | CLEAN | CLEAN | CLEAN |

- **Six kanji edits:** CLEAN on all three facets.
  - All eight word pairs are added at the correct on readings, the dictionary entry numbers are present, and existing readings and source-only notes are kept.
  - These are the only N2 kanji in the batch's words; all the others are N3 or easier.
- **定規 (narrow check):** CLEAN on all three facets.
  - Only `jlpt: 2` was added; the title, reading, body and identity are unchanged.
  - The card had no earlier level, and docs\jlpt-levels.md has no 定規 record.
- **Twenty mappings:** nineteen are CLEAN on all facets. N2:750 has a correctness defect (B38-MAP-01).

# Findings
- **B38-QZ-01** (Low, correctness, confidence medium)
  - **Where:** `words\順々.md:4,9` against `words\どんどん.md:4`.
  - **Issue:** both titles contain "one after another", but neither card excludes the other. Exclusions don't carry over: 順々 excludes 次々, and 次々 already excludes どんどん for this same shared gloss, but that doesn't cover 順々 and どんどん.
  - **Impact:** a quiz could show two defensible answers.
  - **Fix:** add どんどん to 順々's exclusions.
- **B38-LNK-01** (Low, coverage, confidence high)
  - **Where:** `words\小学生.md:16,25`.
  - **Issue:** 小学校 is introduced and paired with 小学生 as plain text, but `words\小学校.md` exists. The repo rule is to link an existing card where it is substantively introduced.
  - **Fix:** link `[小学校](小学校.md)` at line 16.
- **B38-LNK-02** (Low, coverage, confidence medium-high)
  - **Where:** `words\上級.md:33`.
  - **Issue:** the contrast with 先輩 is unlinked, though `words\先輩.md` exists ("senior colleague or student").
  - **Fix:** add the link.
- **B38-LNK-03** (Low, coverage, confidence medium)
  - **Where:** `words\将棋.md:20`.
  - **Issue:** the article discusses the meaning of 指す ("does not mean merely pointing") without linking the existing `words\指す.md`.
  - **Fix:** add the link.
- **B38-MAP-01** (Low, mapping correctness, confidence high)
  - **Where:** `docs\n2-vocabulary-sources.tsv:750`.
  - **Issue:** the note says sense 1 covers "successively", but the pinned dictionary entry (1342230) glosses only "in order" and "in turn" (evidence JSON lines 1130–1133). "Successively" comes from the Daijisen receipt (evidence line 30592).
  - **Fix:** reword the note and attribute the "one after another" rendering to the receipt.

# Optional
- **しょうがない:**
  - Link 仕方 in the 仕方がない mention (line 31).
  - Consider excluding だめ: its secondary "hopeless" sense overlaps this title, and this word's sense 3 includes "no good". Confidence is low.
- **将棋:** mention or link the existing 碁 card ("go board game") next to 囲碁, and link 打つ.
- **受話器 line 24:** link the word card 話.
- **Kanji card 蒸:** it spells "vapour" while the 蒸気 article title uses "vapor".

# Limits
- **No Git:** I couldn't confirm the files on disk match the commit, or check any hashes or the evidence-file equivalence.
- **Partial evidence reads:** I didn't fully read the comparison families in the evidence JSON or the four compact comparison files.
- **Public sources:**
  - Bunpro confirmed the しょうがない attachment rule (verb て-form, い-adjective くて, な-adjective で).
  - On the Weblio 巡査 page I only reached the Wikipedia content, which confirms "lowest rank"; I didn't reach the Daijisen section behind the "broader use" claim. The pinned dictionary's plain "police officer" gloss is consistent with that claim.
  - These claims rely on the author's paraphrased receipts or general knowledge: the figurative use of 主役, 将棋を指す, the 純情 statement that it doesn't mean self-sacrificing devotion, and non-water vapor for 蒸気.
- **Collision scan:** the title scan for English-label collisions used keywords and wasn't exhaustive.
- **Not run:** the validator and the app's quiz draws.
- **Not checked for 定規:** easier levels in other community lists.
- **No native-speaker certification.**
