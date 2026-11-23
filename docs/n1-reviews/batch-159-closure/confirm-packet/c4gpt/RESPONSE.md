# Author's statement for the reviewer of the confirmation report on `f85ff382`

This statement answers only the points in YOUR confirmation report on `f85ff382` (the earlier confirmation report named in `INSTRUCTIONS.md`). F1 is your finding 1; L3 is your Limits disposition on Git object and key authenticity.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and the `evidence\` files; do not rely on this text as evidence.

What changed (`CHANGES.md` lists every line): one line of the ledger. No change was made for another review. Give a disposition for F1 and L3.

## F1: the ledger's lint warning count (line 948)

Author action: **applied**. Line 948 now says: “Of the 42 warnings, 40 are on reused cards and words. They report a missing N1 source-index entry, quiz reading list or Metadata line, or a missing Dictionary line or one that cites no JMdict entry id; B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.” The counts are those of `checks\lint.txt`; `CHANGES.md` lists the warnings by kind, and `evidence\reused-lint-diff.txt` shows that B159 does not change the warned fields.

## L3: Git object and key authenticity

Author action: **none**. `evidence\verify-commit.txt` now also covers `0ba7df63`. It remains the author's transcript: a local packet cannot authenticate the Git objects, the signing key or the signer independently.