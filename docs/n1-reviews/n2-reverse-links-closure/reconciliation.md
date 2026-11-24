# Retained N2 reverse-link correction: review reconciliation

Snapshots: initial `3cbc312e31506bb099b599c7025030f44e820c0e` and follow-up `ce260bb71ad56c40be503479fe0670a392402bb2`, both on base `6e1e0342c91d9d6ba88fee577abd9e638dd645d3` (the published B169 receipt). The ledger is [`n2-reverse-links-correction.json`](../../n1-sources/n2-reverse-links-correction.json).

## Scope

This correction edits five retained N2 kanji cards: 保, 案, 派, 結 and 第. It is not an N1 batch and adds no card. A cumulative recount at B167 and B168 found that 805 of the 810 frozen kanji/word candidate pairs were active. Every one of those words already linked its kanji, but nine kanji-to-word links were missing, all on these five cards:

- 保 → 保健 ほけん, 保証 ほしょう
- 案 → 案外 あんがい, 答案 とうあん
- 派 → 立派 りっぱ
- 結 → 結局 けっきょく, 結構 けっこう, 結論 けつろん
- 第 → 落第 らくだい

The correction adds each link to the card's primary on-reading row and to Common words, using the word card's title. It cites the JMdict entry ID in Metadata and adds or adjusts four short notes.

The following are unchanged:
- front matter, including the JLPT 2 study placement, quiz readings, distractors and exclusions;
- every word card;
- every stroke file.

## Reviewers

Reviewers were run serially. At the initial stage each was blind to the other reviewers' findings:

- claude-sonnet-5.5: correctness and scoped coverage.
- gpt-6.2-sol: consistency and quiz safety.
- grok-4.7: comprehensibility.

At follow-up, each original session received only its own findings and their dispositions, together with the revised snapshot, the actual diff and the revised checks. Reports are archived in `reports/`.

## Initial findings (snapshot 3cbc312e)

| Finding | Raised by | Disposition |
|---|---|---|
| Minor (comprehensibility), `kanji/第.md:41`: "第 follows 落 rather than a number" implied that ordinal 第 follows a number. The next note says it precedes one. | GPT | **Resolved.** GPT's replacement wording was adopted verbatim: "In 落第 (らくだい), 第 is part of a fixed word. It does not introduce an ordinal number as it does in 第三 (だいさん, "third"). Learn 落第 as a whole." JMdict 1623520 (第三 / 第３, だいさん, "third") is now cited. It also covers the pre-existing standalone 第三 at 第.md:22, which the metadata scan had reported as an uncited whole word at base, so the scan's whole-run gaps fell from 1 to 0. GPT confirmed this as resolved. |
| Optional: shorten the 結 ケツ cell, which repeated the note's けっ/けつ rule. | Grok; GPT suggested scoping the clause with "In these examples" | **Resolved.** The row's trailing clause was removed. That clause was "ケツ changes before the following consonant" at base and the more specific "ケツ becomes けっ before a k sound but stays けつ in けつろん" in the draft. The 結.md:49 note now gives the outcome for each listed word: けっこん, けっか, けっきょく and けっこう take small っ, and けつろん keeps つ. Grok confirmed this as resolved. GPT withdrew its suggestion as superseded. |
| Optional: extend the 案 note to the new words, matching the 保 note. | Claude, Grok | **Resolved.** The note now reads: "The source-listed つくえ does not make ordinary 案内, 提案, 案外 or 答案 native-reading words. Practice selects アン." |
| Limit: 策 was not checked. | Claude | **Resolved for link coverage.** The whole-set recount checks every active frozen pair, including 策's, in both directions. At base it flags exactly these nine pairs and none for 策; at the revised snapshot it flags none. This is mechanical link evidence, not a linguistic review of 策. |

## Optional items not adopted

- **Claude, 案外 "beyond expectation, not 'plan outside'":** not adopted. `words/案外.md` already offers "the result lies outside the expectation" as a learning association and says it is not etymology. A "not plan outside" caution on the kanji card would add a word-formation claim that no packet source supports. The disposition sent to Claude put this as "案外 can itself be read as 'outside what one had in mind'". That was the author's paraphrase of the word card's hedged association, not a sourced parse, and no card asserts it. Claude withdrew the item because its own wording would have asserted an unsourced word-formation reading.
- **Claude, 立's ツ becoming っ in the 派 note:** not adopted. The note already says that ハ becomes ぱ after small っ, and `words/立派.md` teaches りっぱ "including its small っ". Withdrawn.
- **Claude, a rank or grade sense and 及第 in the 第 note:** `words/及第.md` does not exist, and the revised note contrasts 落第 with ordinal 第三 instead. The rank sense remains on `words/落第.md`. Withdrawn.
- **Claude, a "quite" gloss for 結構:** the row and Common words use the word card's title gloss, "fine; sufficient". The adverb sense remains on `words/結構.md`. Withdrawn.
- **Grok, a "not literal" note for 結構:** not adopted, for the reason Grok gave: `words/結構.md` already says not to derive "fine; sufficient" from the characters.
- **Claude follow-up optional, naming "before k" in the 結 note:** not adopted. In pinned JMdict, small っ also appears before s, sh and t: 結成 けっせい (1254900), 結晶 けっしょう (1254870), 結束 けっそく (1254930) and 結託 けったく (1254940). A "before k" condition would therefore be incomplete. The note states only the outcome for each listed word, which Claude confirmed contains no false claim.

## Follow-up confirmations (snapshot ce260bb7)

Claude, GPT and Grok each confirmed CLEAN verdicts for all five cards on their assigned facets, with no new defect. Grok left correctness UNVERIFIED because it was not assigned that facet. GPT counted:

- 9 distinct pairs;
- 18 new kanji-to-word link placements;
- nine pair IDs plus the separate 第三 citation;
- unchanged front matter, quiz fields, distractors and word files;
- zero card additions.

## Unverified claims and limits

- **Author-run checks.** Reviewers saw these as packet records and did not rerun them:
  - gates: validate, budget, quiz safety, reading exposure and options, lint, metadata scan and word quiz;
  - the correction-specific mechanical check;
  - the local-archive recounts.
- **Quiz safety.** The gate reports the same six errors at base and at both snapshots. They come from N1-only checks applied to retained N2 cards: 派, 結 and 第 are not tagged N1, and the fixed distractors 客, 笑 and 箱 are not mentioned in Notes. These are pre-existing and do not amount to a quiz-safety pass.
- **Batch audit.** `tools/audit_n1_batch.py --batch 169` passes at base but rejects this snapshot by design, because it accepts only runtime changes recorded in a batch ledger. The correction-specific check replaces it here.
- **Earlier evidence.** The JMdict evidence for the earlier nine IDs was in the initial packet. KANJIDIC2 and the unchanged IDs were not re-reviewed.
- **Acceptance.** These are packet-based blind facet reviews with bounded confirmations. There is no native-speaker, device, Android or whole-set acceptance.
