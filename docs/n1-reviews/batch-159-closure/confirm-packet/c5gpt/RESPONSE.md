# Author's statement for the reviewer of the confirmation report on `0ba7df63`

This statement answers only the points in YOUR confirmation report on `0ba7df63` (the earlier confirmation report named in `INSTRUCTIONS.md`). You confirmed `0ba7df63` with no findings. O1 and O2 are the two points of your Optional line in order: the readingOptions summary that names only 呉; the CHANGES.md statement about the check outputs, which overlooked `checks\link-targets.tsv`.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and the `evidence\` files; do not rely on this text as evidence.

What changed (`CHANGES.md` lists every line): one line of the ledger. No change was made for another review. Give a disposition for O1 and O2.

## O1: the readingOptions summary names only 呉 (line 953)

Author action: **applied**. Line 953 now reads: “lean reading_options.py with the same --extra list: 0 problems. Two informational notes concern KANJIDIC2 name-only readings that the tool marks as drawable from the fallback: 吉 き on the キツ prompt, offered by 28 cards (among them 気, 期 and 記), and 呉 ぐ on the ゴ prompt, offered by 供, 具, 工 and 求. On both prompts the curated options fill all three wrong slots in every outcome, so the fallback is never consulted, and reading_exposure.py lists both readings among the latent collisions.” The two notes are lines 74 (吉 き) and 147 (呉 ぐ) of `checks\reading-options.txt`. `checks\reading-exposure.txt` lines 82 and 175 show that the curated options fill all three wrong slots of both prompts in every outcome, and lines 88 and 178 say that neither reading can be drawn in a shipped pool.

## O2: the check outputs and `checks\link-targets.tsv`

Author action: **applied in this packet's text** (no repository change). `CHANGES.md` now says that the outputs of the check runner are identical to the `0ba7df63` outputs apart from the header line and the run time, and that `checks\link-targets.tsv` is written by the packet builder for the changed lines of each packet's range, so it differs between packets by design. In this packet it lists no links: its only changed line is in the ledger (“0 link(s) on changed lines”).

Your Limits disposition on Git object and key authenticity is unchanged: `evidence\verify-commit.txt` now also covers `bad899ea`, and it remains the author's transcript.
