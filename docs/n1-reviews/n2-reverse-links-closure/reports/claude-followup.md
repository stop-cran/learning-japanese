**Snapshot:** ce260bb71ad56c40be503479fe0670a392402bb2, the revision of the draft I reviewed at 3cbc312e.

**Scope:** I reviewed correctness and scoped coverage only, as a single reviewer, Claude Sonnet 5.5 (claude-sonnet-5.5). I read revision.diff, revised-cards.txt, jmdict-revision.xml and revised-checks.txt in full, one view each. 保 and 派 are not in revision.diff. I compared their revised text with the draft by eye and found it identical.

**Verdicts**

| Card | Correctness | Scoped coverage |
|---|---|---|
| 保 | CLEAN | CLEAN |
| 案 | CLEAN | CLEAN |
| 派 | CLEAN | CLEAN |
| 結 | CLEAN | CLEAN |
| 第 | CLEAN | CLEAN |

Comprehensibility was not assigned.

**Findings and reconciliation:** I raised no findings originally and the revision introduces no defect.

Changed passages:
1. **第.md:41 (落第 note): no regression.** The note is accurate. 落第 is not an ordinal-numeral construction, and 第三 is correctly read だいさん, "third", per JMdict 1623520. It stays consistent with the card's "ordinal-number prefix" framing and with the word card's "rank or order".
2. **第.md Metadata: correct.** 1623520 (第三/第３, だいさん, "third") supports both the new note and the pre-existing 第三 mention at line 22. The whole-run gap dropped from 1 to 0 in meta_scan, consistent with that.
3. **結.md:30 (row clause removed): no wrong claim remains.** The row lists exactly the five words that the note at line 49 treats. Every claim is true: けっこん, けっか, けっきょく and けっこう take the small っ, and けつろん keeps つ.
4. **案.md:44: resolved.** 案内, 提案, 案外 and 答案 are all on-reading compounds (アン+ナイ, テイ+アン, アン+ガイ, トウ+アン), so the note is accurate.

Original optional items:
- **Optional 1 (案 note parity):** resolved, as change 4.
- **Optional 2 (案外 caution):** withdrawn. The author's rationale is accepted, because my wording would have asserted a word-formation reading that is not sourced in the packet. The word card already hedges it.
- **Optional 3 (立's ツ to っ):** withdrawn. The 派 note is accurate as written.
- **Optional 4 (rank sense and 及第):** withdrawn. 及第 has no word card, and the reworded note is adequate. The rank sense stays on words/落第.md.
- **Optional 5 (結構 "quite"):** withdrawn. The row gloss matches the word-card title.
- **Limit on 策:** resolved for link coverage.
  - At base, the recount flags exactly nine reverse-missing pairs: 保健, 保証, 案外, 答案, 立派, 結局, 結構, 結論 and 落第. None involve 策.
  - At the revised snapshot it flags none.
  - Scope of this evidence: the recount covers frozen candidate pairs only, and I did not rerun it.

**Optional (nonblocking, not a defect)**
- The author's description says the sound-change rule is now "stated once" in the note at 結.md:49. In fact the note gives per-word outcomes (small っ, and けつろん keeps つ) but no longer names the condition, "before a k sound". The card text makes no false claim. If you want the condition kept, add "before k" to that note.

**Limits**
- jmdict-revision.xml contains only entry 1623520. I did not re-verify the unchanged IDs, KANJIDIC2, or the other word cards.
- The gates in revised-checks.txt are author-run. I accepted them as reported and did not check them against base. The quiz_safety list is the same six errors as the draft, and the author says they exist at base too.
- I did no external, native or device verification, and I did not review comprehensibility or quiz safety.
