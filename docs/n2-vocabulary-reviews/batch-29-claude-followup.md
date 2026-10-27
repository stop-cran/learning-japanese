## Snapshot
The follow-through commit is **a2ce2462ad5b3f10cc9e10710eccbf9ff1a06c80**, and its parent is corrected commit 790d3d1cd94e28f1a06c2aa55ec7d5eea8c8693b. I reviewed committed content as the supplied patch and the working-tree files show it.

I can't run Git or compute hashes, so the clean state, commit identity and all hashes in the receipt are the author's results, not mine.

## Scope
- **Model:** claude-opus-5.5 (Claude family), working alone, read-only.
- **Receipt, patch and evidence:** I read the receipt, the full follow-up patch, and the full `confirmationFollowThrough` section of the evidence file. That section matches the patch, and `quizGuardRationale` is not in it.
- **Articles:** I read `ごめん.md`, `恐縮.md` and `申し訳.md` in full.
- **Dictionary records:** I read the complete JMdict records 1270670, 1236740 and 1363050.
- **Rules and reports:** I checked the exclusion rules in `docs\content-format.md` (lines 67 and 85–87) and reread my own initial and confirmation reports.
- **Counts and links:** I recounted the exclusions on all 20 new cards: 82 declarations across 18 cards, with none on 御無沙汰 or コンクリート. 恐縮 is excluded from ごめん only once, and the link target `恐縮.md` exists.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `words\ごめん.md` | CLEAN | CLEAN | CLEAN |
| Appended evidence | CLEAN | CLEAN | CLEAN |

## Findings
- **B29-CL-06 (the missing ごめん/恐縮 quiz guard): resolved.**
  - `ごめん.md:9` now excludes 恐縮 directly. Under `docs\content-format.md`, that one declaration protects both quiz directions and choices offered alongside each other.
  - `ごめん.md:40` matches JMdict 1236740 senses 1 and 2: gratitude or feeling obliged, and feeling sorry for troubling someone, often before a request as ～ですが. It says 恐縮 is not the same as bare familiar ごめん and does not express the refusal ～はごめんだ, so it claims no interchangeability.
  - The reading きょうしゅく is correct, and `ごめん.md:48` cites comparison entry 1236740 accurately.
- **CL-01 to CL-05: no regression.** Only `ごめん.md` changed. Its earlier guards against the two waiting apologies (お待ちどおさま, お待たせしました) and あいにく, the greeting example ごめん、お邪魔するよ and the source line are all intact. No identities, titles, readings, levels, mappings or kanji metadata changed.
- **申し訳 (left optional by the author): I accept this.** 申し訳.md teaches that the bare noun "apology; excuse" (JMdict 1363050:1) is not a complete apology. The interjection "my apologies" in 1270670:1 is not the noun "apology."
- **New actionable defects:** none.

## Optional
- **申し訳 guard:** excluding 申し訳 from ごめん would match ごめん's own generous guard against 謝る ("apologize"), but it isn't required.
- **Carried over, unchanged:**
  - Cross-guarding 転がす/返る and 転がる/裏返す.
  - 届ける/言付ける.
  - Polishing the wording at `転がす.md:33`.
  - Teaching recognition of the 此間 spelling.
  - Technical 琴/箏 instrument taxonomy.

## Limits
- **No Git or hashes:** all commit, clean-state and hash claims come from the author's receipt.
- **Manifest:** the working-tree `manifest.json` (line 2293) records the same hash for `ごめん.md` as the receipt, c7a362f2…. The patch contains no manifest diff, so I couldn't verify the regenerated whole-manifest hash (05583d95…).
- **Not tested:** I didn't run the app or test quiz draws, and made no corpus, frequency or native-speaker check. There is no official JLPT syllabus to check against.
- **Bounded scope:** this is a follow-through on the changed card, not a second full review of all twenty cards.
