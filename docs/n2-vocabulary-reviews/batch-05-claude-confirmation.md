## Snapshot
- **Corrected commit:** `52b52704688827a30f8937a5930433b2f7cef8f0`, parent `7cc99e2535f9e4ac917278a5b4f2e49db954e4fa`. The receipt reports clean committed content.
- **Git limit:** I only had file tools, so I could not run Git or recompute the frozen hashes (the content hashes, `actualDiffSha256` and `promptSha256`). The files on disk match the patch text exactly.

## Scope
- **Reviewer:** claude-opus-5.5, working alone without delegation.
- **Changed contexts:**
  - `いつのまにか.md:9,43-46`
  - `ウーマン.md:20`
  - `インキ.md:39-44,48-49`
- **Direct pair:** いつのまにか ↔ こっそり.
- **Also checked:** こっそり.md and インク.md (for contradictions only), the format rules, the receipts and JMdict 1004520 in batch-05.json, and both cited pages, which I fetched myself.
- **Not covered:** unchanged teaching, other cards and kanji, all prohibited reports and notes, and the app's quiz scoring.

## Verdicts
| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| いつのまにか | CLEAN | CLEAN | CLEAN |
| ウーマン | CLEAN | CLEAN | CLEAN |
| インキ | CLEAN | CLEAN | CLEAN |

## Findings
- **R1 (quiz overlap with こっそり): resolved.** The new exclusion is valid under the format rules: one top-level key, an existing target, and not a self-reference. Exclusions apply both ways, so one side is enough.
- **R2 (dangling "departure" sentence): resolved.** The unexplained sentence is gone. The new linked contrast (observer didn't notice vs. someone acting secretly) matches JMdict 1188850 and 1004520.
- **R3 ("Uman" romanization): resolved.** The English line now keeps ウーマン, so it no longer drops the long vowel. Line 29 still teaches ウー・マ・ン.
- **R4 (no インキ/インク usage guidance): resolved.** Both cited pages confirm the qualified convention: インク for stationery and home printers, インキ in the printing industry. They also say the two names refer to the same material.
  - TOKA says either word is acceptable: 「どちらを使っても誤りではありません」.
  - The industry association's name, 印刷インキ工業会, attests the card's example 印刷インキ.
  - This is industry usage evidence, not frequency data. The card makes no frequency, prohibition, composition or dating claim.
- **Regressions:** none found.

## Optional
- **インキ:** the ori-marusin page notes printing inks tend to be thicker. A brief "though printing inks are typically thicker" would avoid over-reading "not a difference in substance".
- **インク.md:** a matching usage note pointing back to インキ is still optional.

## Limits
- **Git:** as noted under Snapshot, I could not run Git or recompute hashes.
- **Quiz behaviour:** I did not run the app's candidate scoring.
- **Sources:** both usage sources are industry pages, not corpora.
- **Naturalness:** judgements are a reviewer's view, not native-speaker certification.
