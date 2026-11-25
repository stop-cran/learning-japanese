**Snapshot:** 3a9b777a76a910b84cfbea50e366b0194201eea4, a child of 63ff44d3.

**Files read:** `final-diff.txt` and `final-evidence.txt`. I did not re-review unchanged cards.

## Follow-up items
| Item | Status | Basis |
|---|---|---|
| 遺憾 grammar: です did not distinguish the noun from the na-adjective | **Resolved** | です is no longer tied to the na-adjective alone. The revised text gives な before a noun (遺憾な点), の in the set phrase 遺憾の意 (first example) and sentence-final です (second example). It still says JMdict classifies 遺憾 as both na-adjective and noun, which matches raw 1159090 (adj-na and n). The text now makes no claim beyond the attested forms. |
| Optional: 遺憾の意 is not an apology | **Optional, unchanged** | The card claims no apology, so this is not a defect. |
| Optional: 懲りる sense-2 example | **Optional, unchanged** | Both senses are cited, and the negative 懲りない appears in the example. |

My original findings F1 and F2 stay resolved. Nothing in these two diffs touches them.

## Regression check
- **`words/遺憾.md`:** I found no regression.
  - The reworded sentence is accurate against raw 1159090, whose adj-na and n tags support な before a noun and の in the set phrase.
  - Entry 2851165 (遺憾の意) is a separate set-phrase entry.
  - 遺憾な点 is attested only by author-observed Weblio examples. That support is unchanged from my last report.
- **`batch-170-progress.json`, 憾 note:**
  - The wording now matches the predicate in `final-evidence.txt`: spelling contains 憾 and carries ichi1, news1, spec1, gai1, news2 or spec2 on the spelling.
  - In the author's scan, 遺憾 is the only spelling that qualifies, out of 11 spellings containing 憾.
  - Every other spelling shows no spelling priority tag.
  - 憾み (1289740) and 憾む (2833583) are consistent with my earlier read of their JMdict entries. They are shown, not offered.
  - The 憾 note keeps 憾む as shown-not-offered, and this is consistent with the 憾.md card.
  - 憾み carries reading-level tags (ichi1, news1, nf16), but not on the spelling. The note correctly says "on the spelling", which keeps the claim accurate.

## Remaining actionable issues
None in my facet.

## Optional
None new.

## Limits
- I did not re-read the scan's script or the render assertion. I took the scan as author-run output. I could check only that its listed predicate matches the new note wording.
- I did not independently scan the full JMdict. Entries 1159090 and 1289740 match raw entries I read earlier.
- The Weblio example attestation for 遺憾な点 remains author-observed.
- I did not read the regenerated manifest hash.
- This is not a fresh whole-deck review, and there is no native or device verification.
