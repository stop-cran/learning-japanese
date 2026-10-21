# N2 expansion review ledger

Scope: the 365 missing cards in the [selected source set](n2-source-snapshot.json), plus directly related supporting content.
The existing 珍 and 短 cards are not claimed as newly reviewed. Follow the [review contract](../.github/copilot-instructions.md).

## Batch 01 - pilot

Cards: 並 丸 久 乱 乳 乾 了 介 仏 令 仲 伸 伺 低 依.

Status: initial independent reviews completed; corrections prepared, changed-passage review pending.

Evidence: [batch-01.json](n2-batch-sources/batch-01.json).
Related edits: third quiz distractors on 下 and 長; component links in 22 existing word articles.

Both initial reviewers inspected `a73354e75917d4758b386c870a4284cd70dfacee`, with no uncommitted content changes.
The author confirmed the clean worktree; the read-only reviewers could not independently run Git. Both reviewed all 15
new cards for correctness, scoped coverage and comprehensibility, using identical instructions and source access.
They ran sequentially in isolated processes, exited before the next started, and did not see one another's reports
or the author's adjudication. Actual models: **gpt-6.1-sol** and **claude-opus-5.5**.

Initial reports, preserved before corrections: [GPT](n2-reviews/batch-01-gpt-initial.md) and
[Claude](n2-reviews/batch-01-claude-initial.md). These describe the initial snapshot, not the corrected cards.

### Initial-finding reconciliation

The dispositions below describe the prepared changes; changed-passage confirmation remains pending.

| Reports | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT F01 | 仲's 中 distractor can be correct in a secondary sense | Resolved in the prepared revision: replace 中 with 住. Kanjipedia's 仲 entry includes the middle of a season; comparing the two quiz titles alone would miss this. |
| GPT F02; Claude F1 | 乾す and 乾る need spelling/reading qualifications | Resolved in the prepared revision: retain the recognized variants, compare 干す/干る, and explain the outside-Joyo readings. Daijisen's exact entries and notation guide support these claims; no numerical frequency is inferred. |
| GPT F03; Claude O3 in part | 伺候 needs context | Resolved in the prepared revision: attendance/service upon a high-ranking person, supported by the しこう entry in Seisenban Nihon Kokugo Daijiten. Missing JMdict priority is not evidence of obsolescence or rarity. |
| GPT F04; Claude F5 and O2 | 丸薬 and standalone 依怙 under "Common words" lack commonness evidence | Resolved conservatively: remove them from that list but keep their valid reading examples. This does not establish that either word is rare, or that 依怙 appears mainly in a particular compound. |
| Claude F2 | 仏語 needs homograph clarification | Optional clarification adopted: explicitly distinguish ふつご from ぶつご with both JMdict entries. The original note identified ふつご, so the stronger diagnosis that it denied the other reading is withdrawn. |
| Claude F3 | Include 乳房 ちぶさ | Optional coverage adopted, with the exact JMdict pair. The original にゅうぼう reading was valid; exhaustive alternate word readings are not the card's scope. |
| Claude F4, ロン part | 胡乱 うろん supplies a real example | Resolved in the prepared revision: add the pair and retain JMdict's "usually written in kana" qualification. This also fixes the word-initial candidate-search blind spot. |
| Claude F4, tentative みだりに part | 乱りに might exemplify `みだ.る` or `みだ` | Not adopted: the word is recognized, but the report does not establish allocation to either exact source reading. Retain the qualified dictionary-only rows rather than forcing a match. This hypothesis remains unverified, not a demonstrated coverage defect. |
| GPT optional; Claude O1 | 久遠 context and remote-past/future gloss | Optional context adopted: identify Buddhist terminology and cite Seisenban Nihon Kokugo Daijiten. Its くおん entry supports the existing expanded gloss; JMdict's shorter gloss did not disprove it. |
| GPT optional; Claude O4 | 依る qualification conflates spelling and pronunciation | Resolved in the prepared revision: "rare kanji spelling", not "rare spelling/reading"; retain the usually-kana qualification. |
| Claude O3, 低まる part | Label 低まる uncommon | Withdrawn as unsupported by the cited absence of priority flags. No frequency label added. |
| Claude O5 | Add フランス語 | Optional, not adopted: an everyday-equivalent expansion is not necessary to distinguish the two readings of 仏語. |
| Claude O6 | Replace 伸べる's futon example with 差し伸べる | Optional, not adopted: the report supplied no contrary attestation or evidence that the original construction was unnatural. No representativeness claim is inferred. |

### Dual-model usefulness

After comparing findings, optional suggestions, limits and per-card notes together, two verified issues were complementary:
GPT alone identified the 仲/中 quiz ambiguity; Claude alone identified the missing 胡乱 example. The latter was missed
both by the authoring heuristic and by GPT's positive source-only assessment. Shared useful observations include the
乾 qualifications, 丸薬/依怙 commonness gap, 伺候 context, 久遠 context and 依る spelling distinction.

Claude also suggested useful optional homograph/alternate-reading explanations, but the valid original readings do not
become errors because another reading exists. Absence of dictionary priorities does not substantiate the report's
frequency claims. These results support using both families for this pilot; they neither rank models generally nor
demonstrate that model bias has been eliminated.

### Limits and remaining review

Neither review certifies native-speaker naturalness across the corpus, exhaustively audits stroke geometry, or independently
re-extracts the pinned upstream dictionaries. Dictionary-only reading rows remain explicitly qualified, not ordinary-usage
recommendations. The 22 existing word-link edits and two legacy distractor changes received narrower related-context review,
not a fresh comprehensive review of their teaching text. Reconciliation is not a vote on the initial verdict labels.

Same-model changed-passage reviews must inspect the corrected snapshot and actual diff before closure. Fresh short-lived
processes will receive each model's own original report; this is not claimed as reuse of the original conversation context.
