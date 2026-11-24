# B169 follow-up confirmation: correctness facet (reading allocations, restricted senses, grammar, scoped coverage)

**Snapshot:** cfef4688, confirming my findings on dc46cc08. The reviewer is Claude Sonnet 5.5.

**Scope:** I read the 15 revised cards and their diffs, `followup-facts.txt`, `followup-evidence-diff.txt` and `correction-evidence.txt`. For source facts I relied on my first-pass reading of `primary.xml` and the families files, which I did not re-read. I did not open `confirmation-task.txt`. This is not a fresh whole-deck or device review.

## Findings from the first review

| Finding | Status | Basis |
|---|---|---|
| F1: 満悦 omits JMdict's "usu. as ご満悦" | **Resolved** | The Meaning section now carries the JMdict note. The ご満悦 example comes first. The kanji-combination section says the usual form is ご満悦 and 満悦する is also used. Bare 満悦する stays, supported by the author-fetched Daijisen example. Declining "less typical" is fine, since no frequency source is in hand. |
| F2: 郷 metadata ID 1355850 is 場所 | **Withdrawn as a B169 defect** | The author says the ID predates B169 and supports Kanjipedia sense ③ (ところ・場所). That is an author assertion. I cannot check it because the 郷 body is not in the packet. That 1355850 is 場所 remains a source fact. |
| Optional 1: 忍ぶ | **Resolved** | The card now gives JMdict's sense order (hide first, endure second) and the object marking in the enduring sense. It also adds the 隠す contrast, the …に(は)忍びない note (2154730), and "shame" in the translation. |
| Optional 2: 忠実 and 恒例 attachment | **Resolved** | 忠実 now states な before a noun and に for the adverbial use. 恒例 now states の before a noun. |
| Optional 3: kana readings missing | **Resolved** | Added だみん, だき, ぐどん and あんぐ. The readings match what I read in JMdict in the first review. I did not re-compare the new glosses. |
| Optional 4: sense clauses on the 実, 例 and 追 kanji cards | **Optional, declined** | The word cards now link the Daijisen character headings with sense numbers (実 4, 例 3, 追 4). The ledger gives the author-fetched sense text. I accept this as adequate. |
| Optional 5: みじ+め split vs the standard-use table | **Resolved** | Both the みじめ and 惨 cards now state that the split follows KANJIDIC2 and that the table lists whole みじめ with 惨めだ. |
| Optional 6: 懐古 wording | **Resolved** | The card now reads "A related word … which JMdict glosses" and cites 1200550. I did not re-verify that ID. |
| Limit: exclusion symmetry | **Addressed on author evidence only** | The author says exclusions are symmetric and declared once, citing `docs/content-format.md:122`, which is not in the packet. The new pairs are 悼-愁, 忍ぶ-潜る, 忠実-ねっしん and 追悼-嘆く. The word-quiz audit reports 0 problems. |

## Regression check

- **Consistent with source facts, author-side wording or evidence:**
  - 恒: the つね/つねに note matches `quizKunyomi: []` and JMdict 2020520.
  - 惨: the むご.い row and the KANJIDIC2 note are consistent.
  - 愁: the sense-local preference matches 1540740.
  - 愚か: the 疎か entry 2832535 is cited.
  - 恭しい: the attributive example reads correctly.
- **Evidence-only checks:** The 忠実/まめ point rests on the audit evidence. I could not see 隠す (1170650) or the card slugs ねっしん, 潜る and 嘆く, so I did not check them.

## Remaining actionable issue (minor)

**R1. 恭しい, Distinctive meaning.** The card says the word "can also be used ironically for exaggerated formality".
- **Evidence:** The ledger records only "sometimes used ironically" for the 実用日本語表現辞典 entry. "For exaggerated formality" is an unsourced elaboration attributed to that source.
- **Remedy:** Write "and that it is sometimes used ironically", or drop the clause.

## Optional, none blocking

- 忠実 example 2 now has a stray double space before "—".
- 満悦: "in plain narration about a child" is vague.
- 恒例: "though not only" is the author's gloss of Daijisen's "mostly". It could be moved outside the attribution.
- The ledger still says "untagged route" while calling 満悦 a "no qualifying preferred-tier" exception.

## Limits

- No external pages (Weblio, Kanjipedia, the standard-use PDF) were opened. Everything attributed to them is author attestation.
- The raw scan claiming 満悦 is the only priority-tagged 悦 spelling is an author observation.
- The 郷 body, 怠, the unchanged 実, 例 and 追 kanji cards, and link-target existence were not seen.
- No native or device verification was done.

**Conclusion:** All original findings are resolved, withdrawn or optional. R1 is the only remaining actionable item.
