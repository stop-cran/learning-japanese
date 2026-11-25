# Batch 170 review reconciliation

Snapshots: initial `0ac3eaad07b20ba50997f128dfb78bba7c99e70a`, follow-up `63ff44d350ec8d6be3b024d6c462119e1ac2ccb2`, final `3a9b777a76a910b84cfbea50e366b0194201eea4`, all on base `4dff7a1c46fa3b06de2f7a97004f9837ec2dc445`. `origin/main` was still at the base when the reviews closed, so no upstream integration merge was needed; see `integration` in the batch ledger.

Reviewers were run serially, blind to one another at the initial stage: claude-sonnet-5.5 (correctness and scoped coverage), gpt-6.2-sol (consistency and quiz safety) and grok-4.7 (comprehensibility). The same original sessions received their own findings, the revised snapshot and the actual diff at each later stage. Reports are archived in `reports/`.

## Initial findings (snapshot 0ac3eaad)

Findings shared across reviewers are merged by underlying defect.

| Finding | Raised by | Disposition |
|---|---|---|
| 遺憾 and 不満 had no direct meaning-quiz exclusion, although both can carry a bare dissatisfaction gloss | GPT (moderate) | **Resolved.** 不満 is declared once, on 遺憾. Pairs are symmetric (content-format lines 119–122). |
| 遺憾 was tagged only as a na-adjective, although JMdict 1159090 records adj-na and n | GPT; Claude optional | **Resolved over three rounds.** The noun tag was added. 遺憾な点 (いかんなてん), "a regrettable aspect", now sits beside the set phrase 遺憾の意. 遺憾な点 was chosen over the reviewer-suggested 遺憾な結果 because Weblio example sentences attest it (Tanaka/Tatoeba, Kenkyusha and Saito examples, author-observed). At the final round, sentence-final です is no longer attributed to the na-adjective use alone (Claude follow-up optional). |
| 懇談 called 会議 "a formal meeting" and 話し合い "a discussion to settle something" | Claude F1, GPT | **Resolved.** 会議 is now "a meeting held for discussion, planning or decisions, large or small" and 話し合い is talking something over together. 懇談 keeps its friendly, relaxed emphasis. |
| The 憾 うら.む row linked 恨み for "matter for regret", but that card teaches only resentment | Claude F2 | **Resolved.** The row keeps JMdict 1289740's "esp. 憾み" note and says the linked card teaches only the resentment sense. |
| 慈善 said 奉仕 is "without seeking reward" | GPT; Claude optional | **Resolved.** 奉仕 is now service or work for others or for a cause; 慈善 is charitable aid or activity. |
| 懲 notes implied that 課, 習 and 学 share a meaning with 懲りる | GPT | **Resolved.** The exclusions are kept and described as protection against a misleading English cue ("lesson"), not shared Japanese meaning. |
| 慨 asserted a dictionary-wide negative for なげく | GPT (unverified) | **Resolved.** The card now says JMdict's なげく entry 1418090 lists only 嘆く and 歎く. The author's full pinned scan, which found no spelling containing 慨 with a reading beginning なげ, stays in the ledger note as author evidence. |
| 遺憾 as the only qualifying route for 憾 was not independently established | GPT (unverified) | **Resolved over two rounds.** The follow-up scan used a narrower tag filter than the batch rule (GPT, partially resolved). The final note names the render's exact predicate, a spelling containing 憾 with ichi1, news1, spec1, gai1, news2 or spec2 on the spelling. The full-predicate scan lists all 11 such spellings and only 遺憾 qualifies; 憾み has priority tags on its reading only. |
| 憂慮 and 懸念 share all three JMdict glosses (1257720) | GPT (limit) | **Withdrawn for this snapshot.** There is no `words/懸念.md` to exclude. This becomes a required pair if a 懸念 card is added. |
| 感慨 and 感じる (1212260 sense 2, "be moved") | GPT (limit) | **Resolved.** 感じる is declared on 感慨, beside the existing 感ずる. |
| Six selected on-readings are shared with listed lookalikes (慈–磁, 慨–概, 憂–優, 憤–噴/墳, 憾–感, 懇–墾/恨/根) | GPT (limit) | **Withdrawn as a card defect.** Kanji reading questions show the written kanji, and all full readings of the target are protected from wrong-answer use (content-format lines 153 and 205). The reading-options gate passes; this is author-side static simulation, not observed app behavior. |
| 慶弔 introduced 弔事 (ちょうじ) without separating the homophone 弔辞 | Grok | **Resolved.** The notes say 弔辞 (ちょうじ), "memorial address; eulogy", is a different word (2116690, 1427690). |
| 愁い had no kana in the 憂 sense note | Grok | **Resolved.** 愁い (うれい) is given. The later mention is a link to the 愁 kanji card, not the word, so the second kana request was withdrawn. |
| 性懲りもなく had no reading in the 懲 note | Grok | **Resolved.** (しょうこりもなく) was added (1882440). |
| Kanji exclusions looked one-directional; 善 and 慮 showed no metadata ID update | Claude, for the consistency reviewer | **Withdrawn by Claude.** Pairs are symmetric, and 1315360 (慈善) and 1540910 (憂慮) were already on those Metadata lines at the base. |
| Optional items adopted | Claude, Grok | 憧れる takes に, 慕う takes を; 監督 translated "coach"; "family" dropped from 慶弔 example 1 and example 2 replaced with a 慶弔見舞金 sentence (2873015); 感慨 is noun only, unlike 感動 and 感激 (1212310, 1212570, 1212360); 遺 tied to 遺憾 through "remain behind"; 羹 and 膾 explained from JMdict 2002120 and 1957170 and the Digital Daijisen proverb entry. |

## Final confirmations (snapshot 3a9b777a)

Claude, GPT and Grok each confirmed that no actionable residue remains and that neither final change regresses its facet. No further revision was made. At this snapshot the batch has 10 source rows, 10 new words, no reused word supports, 12 support and 6 supplementary mappings, 18 reciprocal pairs, 26 reading dispositions, 10 offered reading keys, and 81 kanji and 100 word direct-exclusion entries in the quiz audits.

## Optional items not adopted

- **Claude:** "遺憾の意 is not an apology" (no source in hand for that general claim; the card does not call it an apology); a separate 懲りる sense-2 example and the 懲りない entry (both senses are glossed and 懲りない appears in an example and the grammar note). Claude withdrew 遺憾に思う, 憤慨 versus 恨み, 感慨深げな and teaching the Kanjipedia-only readings.
- **GPT:** a search-only note for 感慨's misspelling 感概 (no card contains 感概); consolidating the overlapping JMdict citation lines on 感, 談 and 産.
- **Grok:** a recognition note for the irregular spelling 如何なく of 遺憾なく.

These are editorial preferences. None is an established defect.

## Unverified claims and limits

- Digital Daijisen (遺憾 definition, 遺 sense 1 後に残る, the 羹に懲りて膾を吹く entry, 不幸), 実用日本語表現辞典 (遺憾 in formal settings), Kanjipedia, standard-use table and Weblio example-sentence checks are author evidence recorded in the batch sources. Reviewers saw only those records.
- The full pinned-JMdict scans (no 慨 spelling with a なげ- reading; 遺憾 as the only 憾 spelling meeting the six-tag predicate) are author-run output. The render asserts the 憾 result at build time; reviewers did not rerun either scan.
- Reading-collision, meaning-quiz and word-option results come from author-side static simulation, not observed app behavior.
- Lint reports three pre-existing metadata-reading errors on 産 (う.まれる, うぶ-, む.す have no Readings row), unchanged at every snapshot. B170 changed only a word bullet and the citation line on 産.
- No added text uses a glyph in Android's RareHan ranges.
- These are packet-based blind facet reviews with bounded confirmations. There is no native-speaker, device, Android or whole-set acceptance.
