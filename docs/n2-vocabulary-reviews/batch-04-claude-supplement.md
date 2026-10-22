## Snapshot
- **Author-verified receipts, not recomputed by me:** commit `dd4d6de4…`, parent `68380b7c…`, clean worktree at freeze, patch hash `1e8d0c6d…`, and hashes for the five files in the snapshot. Content scope is `words/一応.md` only.
- **Read independently:**
  - The patch has one changed line. It appends `くらい, ほど` to the existing list.
  - `一応.md:9` in the working tree matches the patch's `+` line, and the surrounding header lines match the patch context.

## Scope
- **Model:** claude-opus-5.5 (Claude family). Read-only; no agents.
- **Scope:** one file and two pairs, 一応/くらい and 一応/ほど.
- **Files read:**
  - `一応.md`, `くらい.md` and `ほど.md`
  - `content-format.md:80-120` (includes the assigned 88-116)
  - `batch-04.json`: entry 1161170, the N2:72 mapping, and complete supplementary entries 1154340 and 1436510
  - The `quiz_exclusions` checks in `tools/validate.py:443-466`
  - My own `batch-04-claude-confirmation.md:57`, which first suggested this pairing. I did not treat that note as settled.

## Verdicts
| Facet | Verdict |
|---|---|
| Correctness | CLEAN |
| Scoped coverage | CLEAN |
| Comprehensibility | CLEAN |
| Regressions (read, not run) | CLEAN |
| Receipt integrity (commit and hashes) | UNVERIFIED |

**Why the guards are justified:**
- **The titles overlap.** 一応's title includes "roughly" (`一応.md:4`). The くらい title is "approximately; to the extent" (`くらい.md:4`) and the ほど title is "extent; approximately" (`ほど.md:4`).
- **The dictionary supports each overlapping word:**
  - "roughly" is in 1161170 sense 1 (`batch-04.json:~781-789`), which the card teaches.
  - "approximately" is in 1154340 sense 1 (`~8936-8941`).
  - "approximately" is also in 1436510 sense 6 (`~9138-9143`). ほど's card cites sense 6.
- **A learner could reasonably accept either answer.** Without context, "roughly" and "approximately" read as synonyms in English. This meets the criterion at `content-format.md:95-99` in both quiz directions.
- **The guards are consistent.** 約 ("approximately; about") and およそ were already excluded on the same token.
- **The case does not rest on shared subject matter.** The cards share no tags, kanji or word type.
- **The real difference in meaning is kept, not hidden.** 一応 qualifies adequacy rather than quantity (`一応.md:24-25`). The guard is still right, because the title invites the numerical reading. Retitling is not the remedy.

**Coverage:**
- Both pairs are needed, since both titles carry "approximately".
- No other title words overlap.
- Each pair is declared on one card only: くらい's list omits 一応, and ほど has no list.

**Regressions:**
- The list stays inline, has no duplicates and does not include 一応 itself.
- Both IDs exist as word files.
- No `quiz_distractors` entry conflicts with either pair.

## Findings
None established.

## Optional
I withdraw my earlier alternative of retitling "roughly" to "more or less" (`confirmation.md:57`). Re-check these two guards only if the title changes for reasons of meaning.

## Limits
- I could not run Git, a shell, the validator or the tests, and I could not recompute hashes. The receipts are the author's claims.
- I did not read the app code.
- This is not a full-batch review or native-speaker certification.
