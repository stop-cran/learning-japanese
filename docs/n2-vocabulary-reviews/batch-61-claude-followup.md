I agree with the correction: the false "usually written in kana" claim is gone from 退ける.md, and nothing else changed. N2:1208 is CLEAN, and I found no new defects.

## Snapshot
**Follow-up commit:** 46233abe6b58dcaad2df25e26b8a6ed297dd0b2b
**Parent:** b76948a5da23c6267098c80359cf81e836e28a8a

followup-snapshot.json lists `words/退ける.md` as the only changed file and reports `cleanCommittedContent: true`. I reviewed committed content only. My file tools can't run Git, hash, manifest or cleanliness checks, so the snapshot's hashes and claims were checked by the author, not by me. I didn't inspect .git.

## Scope
**Model:** claude-opus-5.5 (claude family). Read-only: no edits, agents or delegation.

**Read in full this turn:**
- followup-snapshot.json (read first)
- followup.patch, a single one-line change at 退ける.md:17
- followup-family.json (dictionary entry 2850084)
- words\退ける.md

**Partial reads:**
- The author's evidence packet (followup-review-evidence.json): the follow-up record at lines 44375–44440 and 44985–45060, plus the two mapping notes found at lines 134 and 3380.
- kanji\退.md.
- A search of words\ and kanji\ for どける/どけ.
- A search of the three instruction files for kana and frequency rules.

**Inherited, not reread:** the other nineteen word judgments, all twenty mappings, the TSV rows, the three kanji cards (溶, 床, 戸) and the five kanji–word link pairs, all from my earlier reads.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1208 退ける (どける) | words\退ける.md | Full read this turn, plus the full patch and the full 2850084 entry | CLEAN | CLEAN | CLEAN |

**Inherited and unchanged:**
- **Other nineteen rows:** CLEAN on all three facets.
  - N2:1220 (跳ぶ → 飛ぶ) is CLEAN only for this batch's additions.
  - N2:1221 (留まる → 止まる) is also CLEAN only for this batch's additions.
- **Mappings:** CLEAN. N2:1208 is still 退ける/どける, entry 2850084, sense 1.
- **Kanji cards 溶/床/戸 and the five link pairs:** CLEAN.
- **Baseline preservation:** CLEAN.

**Uncorrected inherited debt, outside batch scope:** the quiz pairs 飛ぶ/飛行 and 止まる/止む still have no exclusion on either side.

## Findings
**My earlier finding R1: resolved.**
- followup-family.json shows sense 1 with `misc: []`, empty spelling and reading `info`, and `kanaOnly: false`. There is no "usually kana" label, so the earlier author claim was false.
- The follow-up record in the evidence packet (lines 44382–45060) states this correctly. Its copy of the entry matches followup-family.json field for field.
- Earlier records are left as historical and marked as superseded, which is appropriate.

**The changed sentence (退ける.md:17)** now reads: "It is a transitive ichidan verb; its kana spelling is どける."
- It is accurate: the entry lists it as an ichidan, transitive verb with the reading どける.
- It makes no claim about how often each spelling is used. This follows .github\copilot-instructions.md:40, which says a dictionary spelling list supports recognition, not frequency.

**Correcting my own earlier review:** I said "usually written" had indirect support from the Daijisen ▽ mark and from どける not being an official (jōyō) reading. Both only show official spelling standards; neither measures usage. I withdraw my "commonly written in kana" suggestion. The author's neutral wording is the better fix.

**Regressions:** none.
- The patch changes one line. Metadata, quiz exclusions, examples, kanji explanation, distinctive-meaning section and footer are unchanged.
- No other どける spelling-frequency claim exists in words\ or kanji\.

**New defects:** none.

## Optional
- **退ける.md:** could say the examples use kana because 退ける in kanji can also be read しりぞける or のける, as line 43 already notes. This is a reason for the writing choice, not a frequency claim.
- **Evidence packet:** the internal mapping notes at lines 134 and 3380 still say "usual kana どける taught". They aren't shown to learners, and the follow-up record supersedes them. They could be reworded the next time the batch source is edited, but I'm not allowed to read batch-61.json, so I can't confirm whether it contains the same wording.
- **Unchanged earlier items:** the weak 都心/中 and 整う/入る exclusions stay nonblocking, as do the 所々 reading/kana note, the rare-spelling labels and the どなる sound-word prefix.

## Limits
- The snapshot, hash, manifest and cleanliness checks were run by the author; I didn't run them.
- No spelling frequency was measured. I make no claim either way about how often どける is written in kana.
- I read the evidence packet only in the ranges listed under Scope.
- Inherited judgments rest on earlier reads; I didn't reread the TSV rows, the other nineteen articles or the kanji cards this turn.
- The 飛ぶ/飛行 and 止まる/止む quiz gaps remain unfixed, so I am not certifying the whole corpus as quiz-clean.
- Earlier evidence limits still apply:
  - The official guide to kanji for same-sounding words (異字同訓) was never parsed.
  - The public captures all came from one dictionary service (Daijisen).
  - The public lookup for とっくに failed.
- The 退 kanji card wasn't edited in this batch and isn't one of the assigned link pairs. Its missing ど.ける reading and missing 退ける link were not assessed.
- I ran no live quiz draws, did no exhaustive synonym check, and this is not a native-speaker review.
