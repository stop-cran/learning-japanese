# B169 final confirmation: correctness facet

**Snapshot:** 9ffbf452, confirming my findings from cfef4688. The first review was on dc46cc08. The reviewer is Claude Sonnet 5.5.

**Checked:** I read `final-reconciliation.txt`, `final-diff-1.txt`, `final-revision-1..2.txt` (all five changed cards), `final-evidence-diff.txt`, `final-facts.txt` and `final-mame-trace.txt`. I also re-read `primary.xml` to check source facts.

**Not read:** `confirmation-task.txt`, the full ledger, the manifest diff and the families files. This is not a fresh whole-deck or device review.

## Status of my earlier findings

| Finding | Status | Basis |
|---|---|---|
| R1 (actionable): 恭しい irony clause was an unsourced elaboration | **Resolved** | The card now says "sometimes used ironically, with a nuance of affected, more-than-necessary politeness." The author quotes the entry as 「わざとらしさ」のニュアンスを込めた皮肉… and 「必要以上に丁重っぽく」. The rendering is faithful to that quote. The quote itself is author-recorded, not packet evidence. |
| Optional: 忠実 stray double space | **Resolved** | The diff shows a single space. |
| Optional: 満悦 "plain narration about a child" | **Resolved** | The sentence is removed. The Distinctive meaning section now opens on the dictionary note. |
| Optional: 恒例 "though not only" inside the Daijisen attribution | **Resolved** | The card keeps Daijisen's "mostly" and adds a separate sentence. Source fact: JMdict 1278800 glosses are "established practice" and "custom", and it takes の (`primary.xml`). The second example is correctly described as a workplace custom. |
| Optional: ledger said "untagged route" for 悦 | **Resolved** | See the 悦 check below. |
| Earlier declined items (kanji-card clauses on 実, 例 and 追) | **Optional, unchanged** | I accepted these last round. |

## Source facts I checked against `primary.xml`

- 満悦 1526740 has `news2`, `nf37` and `spec2` on both the spelling and the reading. It carries the note "usu. as ご満悦" and is intransitive with suru. This matches `final-facts.txt` item 2 and the card text.
- 恭しい 1236790 has no priority tags on any spelling. It remains the only genuine untagged exception.
- 忠実 1012210 has a single sense. The card's まめ statement is unaffected.

## Regression check

- **恒 つねに row:** The new text says Kanjipedia lists つね.に outside standard use. That is a new author-attested claim and I cannot check it. It is consistent with `quizKunyomi: []` and with the Notes, which say the reading is not offered in practice.
- **満悦 and 恒例 cards:** The edits are grammatical and still match JMdict.
- **悦 ledger records:** Both `exceptionReason` fields are removed. The JSON diff shows valid closure, and `readingPriorityTags` keeps `nf37` as the raw list. `selectionReason` and `selectionNotes` now agree that only 恭 is an exception. I could not see the whole ledger, so a stale reference elsewhere is not excluded; the author reports the batch audit shows no errors.
- **忠実/まめ trace:** The tool output lists the generated look-alikes じゅうじつ, ちゅじつ, ちゅうしつ and ちゅうじず, and the corpus tier 口実, 実物, 現実 and 確実. None of them is まめ, and the tool reports 0 problems. This is an author-side port of the app code, which I saw only as an excerpt.
- **Owner decision:** The author quotes issue #60 comment 7112026459, "news2 and spec2 count as qualifying tags," as the basis for treating 満悦 as qualifying. The comment itself was not opened, so that quotation is author-supplied. The author withdrew the earlier "B158/B159" rationale.

## Remaining actionable issues

None.

## Optional

- 恭しい: the card says everyday conversation "seldom calls for it," while the ledger says "seldom deliberately used." The source Japanese for that clause is not in the packet. The two could be worded the same way.

## Limits

I did not open the Weblio, Kanjipedia or GitHub pages. The following are author attestations, not verified:
- the Japanese quotes
- the Kanjipedia reading
- the owner comment
- the raw scan claiming 満悦 is the only priority-tagged 悦 spelling
- the quiz simulation
