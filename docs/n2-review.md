# N2 expansion review ledger

Scope: the 365 missing cards in the [selected source set](n2-source-snapshot.json), plus directly related supporting content.
The existing 珍 and 短 cards are not claimed as newly reviewed. Follow the [review contract](../.github/copilot-instructions.md).

## Batch 01 - pilot

Cards: 並 丸 久 乱 乳 乾 了 介 仏 令 仲 伸 伺 低 依.

Status: **reviewed**. Both models confirmed the corrected passages with no actionable remaining defect in scope.

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

These are the author's evidence-based dispositions, not a rewriting of either preserved report's initial verdict.
The changed-passage reviews below confirmed the actual corrections.

| Reports | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT F01 | 仲's 中 distractor can be correct in a secondary sense | Resolved: replace 中 with 住. Kanjipedia's 仲 entry includes the middle of a season; comparing the two quiz titles alone would miss this. |
| GPT F02; Claude F1 | 乾す and 乾る need spelling/reading qualifications | Resolved: retain the recognized variants, compare 干す/干る, and explain the outside-Joyo readings. Daijisen's exact entries and notation guide support these claims; no numerical frequency is inferred. |
| GPT F03; Claude O3 in part | 伺候 needs context | Resolved: attendance/service upon a high-ranking person, supported by the しこう entry in Seisenban Nihon Kokugo Daijiten. Missing JMdict priority is not evidence of obsolescence or rarity. |
| GPT F04; Claude F5 and O2 | 丸薬 and standalone 依怙 under "Common words" lack commonness evidence | Resolved conservatively: remove them from that list but keep their valid reading examples. This does not establish that either word is rare, or that 依怙 appears mainly in a particular compound. |
| Claude F2 | 仏語 needs homograph clarification | Optional clarification adopted: explicitly distinguish ふつご from ぶつご with both JMdict entries. The original note identified ふつご, so the stronger diagnosis that it denied the other reading is withdrawn. |
| Claude F3 | Include 乳房 ちぶさ | Optional coverage adopted, with the exact JMdict pair. The original にゅうぼう reading was valid; exhaustive alternate word readings are not the card's scope. |
| Claude F4, ロン part | 胡乱 うろん supplies a real example | Resolved: add the pair and retain JMdict's "usually written in kana" qualification. This also fixes the word-initial candidate-search blind spot. |
| Claude F4, tentative みだりに part | 乱りに might exemplify `みだ.る` or `みだ` | Optional, not adopted: the word is recognized, but the initial report did not establish allocation to either exact source reading. Retain the qualified dictionary-only rows rather than forcing a match. Claude's follow-up downgrades this to optional; GPT's optional proposal is narrower, `みだ` only. Neither establishes an actionable defect in the retained wording. |
| GPT optional; Claude O1 | 久遠 context and remote-past/future gloss | Optional context adopted: identify Buddhist terminology and cite Seisenban Nihon Kokugo Daijiten. Its くおん entry supports the existing expanded gloss; JMdict's shorter gloss did not disprove it. |
| GPT optional; Claude O4 | 依る qualification conflates spelling and pronunciation | Resolved: "rare kanji spelling", not "rare spelling/reading"; retain the usually-kana qualification. |
| Claude O3, 低まる part | Label 低まる uncommon | Optional, not adopted: the cited absence of priority flags does not support that inference. No frequency label added. |
| Claude O5 | Add フランス語 | Optional, not adopted: an everyday-equivalent expansion is not necessary to distinguish the two readings of 仏語. |
| Claude O6 | Replace 伸べる's futon example with 差し伸べる | Optional, not adopted: the report supplied no contrary attestation or evidence that the original construction was unnatural. No representativeness claim is inferred. |

### Dual-model usefulness

After comparing findings, optional suggestions, limits and per-card notes together, two verified issues were complementary:
GPT alone identified the 仲/中 quiz ambiguity; Claude alone identified the missing 胡乱 example. The latter was missed
both by the authoring heuristic and by GPT's positive source-only assessment. Shared useful observations include the
乾 qualifications, 丸薬/依怙 commonness gap, 伺候 context and 依る spelling distinction. Both also raised the 久遠 passage,
but Claude's gloss-evidence concern and GPT's Buddhist-context suggestion were not identical claims.

Claude also suggested useful optional homograph/alternate-reading explanations, but the valid original readings do not
become errors because another reading exists. Absence of dictionary priorities does not substantiate the report's
frequency claims. These results support using both families for this pilot; they neither rank models generally nor
demonstrate that model bias has been eliminated.

### Changed-passage confirmation

Both reviews used the corrected content at `455bfb27a10d61be997b75261e180cb089a8bbf7` and the actual 168-line
card diff from the initial checkpoint. Each covered all changed passages in 丸, 久, 乱, 乳, 乾, 仏, 仲, 伺 and 依,
with surrounding context and the replacement distractor's actual title. Each reported correctness, scoped coverage and
comprehensibility CLEAN for all nine, with no new actionable finding. The six unchanged pilot cards retain their initial
same-snapshot dual-model coverage; they were not needlessly re-reviewed.

Completed reports: [GPT](n2-reviews/batch-01-gpt-followup.md) and
[Claude](n2-reviews/batch-01-claude-followup.md). Claude resumed the original initial-review context. GPT's first
changed-passage process could not open the external-session diff because of a scoped path-permission failure; that
process was resumed with the artifact directory allowed and successfully inspected every hunk. Its completed report
replaces the incomplete pass for closure. All processes exited sequentially; none were retained running.

The follow-ups' remaining suggestions are **optional**, not required corrections: adding 乱りに for `みだ` only;
duplicating ちぶさ in Common words; rephrasing "established" as "assigned"; adding 仲秋 or 依怙贔屓; and choosing
different contextual wording for 伺候 or 久遠. They were not adopted. The selected 久遠 example's Buddhist context
does not assert that all uses are Buddhist; the 伺 card explicitly teaches humble usage. No unsupported "dated" label
was added. The stronger initial homograph/alternate-reading diagnoses remain calibrated as described above, even though
Claude labels their adopted clarifications resolved.

### Limits

Neither review certifies native-speaker naturalness across the corpus, exhaustively audits stroke geometry, or independently
re-extracts the pinned upstream dictionaries. Dictionary-only reading rows remain explicitly qualified, not ordinary-usage
recommendations. The 22 existing word-link edits and two legacy distractor changes received narrower related-context review,
not a fresh comprehensive review of their teaching text. Reconciliation is not a vote on the initial verdict labels.

The author confirmed clean, unchanged committed content before both review stages. File-only reviewers could read the
HEAD reference and supplied diff, not independently run Git. Source-record changes received current-record inspection,
not a separate upstream re-extraction. Their remaining optional 乱りに allocation is not used as teaching evidence.
