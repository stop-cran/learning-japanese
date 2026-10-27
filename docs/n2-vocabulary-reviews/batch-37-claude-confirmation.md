# Batch 37 corrections: confirmation review (Claude)

All five of my original findings are resolved. B37-05 is partly resolved and I withdrew the rest of it. I found no new defects or regressions, and all five corrected articles are now CLEAN on every facet.

## Snapshot
- **Corrected commit:** `916247bf6bbf7ffca6ba1cddc2ff2608f6b610b0`.
- **Parent:** `fa390bf5776402ca8a27fac55cb75990d1f37b1d`, which matches the snapshot I originally reviewed.
- I reviewed committed content only. With file tools only and no Git, I could not confirm the commit or recompute any hashes; those come from the author's receipt.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked alone and edited nothing.
- **Read in full:**
  - the correction snapshot and correction patch;
  - the five corrected articles (住居, 集金, 終点, 周辺, 終了);
  - the `correctionEvidence` section of the confirmation evidence and the 21-family correction rendering;
  - the existing cards 切る, 切れる, 端, 宿 and コレクション;
  - mapping row N2:722;
  - my own initial report.
- **Checked by title and exclusion lines:** 仕舞い, 終わる, 閉める, 閉まる, 郊外 and 結論.
- **Carried forward, not re-reviewed:** the other fifteen articles, the five kanji edits and the twenty mappings, which the snapshot lists as unchanged.
- **Web:** goo, Weblio and Kotobank lookups for 住居 failed or returned only encyclopedia text.
- **Not read:** the other reviewer's report, ledgers, notes, the unblinded batch file and private author checks.

## Verdicts
Each cell reads correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| 住居 | CLEAN / CLEAN / CLEAN |
| 集金 | CLEAN / CLEAN / CLEAN |
| 終点 | CLEAN / CLEAN / CLEAN |
| 周辺 | CLEAN / CLEAN / CLEAN |
| 終了 | CLEAN / CLEAN / CLEAN |

- **Other fifteen articles:** CLEAN on all facets, carried forward.
- **Five kanji edits:** CLEAN, carried forward.
- **Mappings:** all twenty are CLEAN. N2:722's coverage changes from NEEDS FIX to CLEAN because the article now presents "address" as dictionary recognition only. The other nineteen are carried forward.

## Findings
**New findings:** none. The ten added exclusions are 住居–宿, 集金–コレクション, four for 終点, one for 周辺 and three for 終了.

**B37-01 (住居 "address"): resolved**
- The title is now "dwelling; residence" (住居.md:4).
- The example that put "address" on 住所 is gone. The new example is この町に住居を定めました (line 20).
- Line 25 keeps JMdict's "address" only as dictionary recognition and says 住居 does not freely replace 住所. It does not use the gap in the Japanese dictionary to dispute JMdict.
- Without "address" in the title, 宛名 no longer needs an exclusion.
- The new 宿 exclusion is justified: JMdict 1337190 sense 2 includes "house, home, dwelling", and the card title "lodging; inn" is close to "dwelling".

**B37-02 (終点 "end" labels): resolved, including my lower-confidence extras**
- 終点.md:9 now excludes 仕舞い, 終わる, 終了 and 端.
- Line 33 keeps the distinctions: 終了 is the end of an activity, 終点 is an endpoint, and 端 is an edge or end more broadly.
- JMdict 1581610 sense 1 for 端 includes "end (e.g. of street)". I treated the other readings of 端 as separate entries.

**B37-03 (周辺 vs 郊外): resolved**
- 周辺.md:9 adds 郊外, and line 33 explains the difference.
- Supported by JMdict 1282490 sense 1 and the 郊外 card title "suburbs; outskirts".

**B37-04 (集金 vs コレクション): resolved**
- 集金.md:9 adds コレクション, and line 35 keeps the payment-versus-hobby distinction.
- Supported by JMdict 1051540 sense 1.

**B37-05 (終了 exclusions): 結論 part resolved; 切る/切れる removal withdrawn**
- 結論, 閉める and 閉まる are added (終了.md:9). Line 37 still separates a reasoned conclusion and physical shutting from 終了.
- I withdraw my proposal to remove 切る and 切れる. The existing cards teach senses that overlap with "ending; termination":
  - 切る teaches 電話を切る, hanging up (JMdict 1384830 sense 4: "terminate (e.g. a conversation), hang up").
  - 切れる teaches 期限が切れる, expiring (JMdict 1384860 sense 6: "expire").
- So keeping both is a supported precaution, not clear over-exclusion.

**Regression check:** none found.
- The links to 宿, コレクション, 終了, 端 and 郊外 all point to existing files.
- The new sentences are natural and accurate.

## Optional
- The N2:722 mapping note still says "residential address retained". Wording such as "address recognized only as a dictionary sense" would match the article better. Not blocking.
- My earlier remarks on 集合 (generous exclusions), 受験 vs 試験 and 熟語 vs 諺 stay optional; none is a defect.

## Limits
- I could not run Git or check any hashes.
- I could not retrieve the Digital Daijisen entry for 住居 to confirm 住居を定める; every lookup failed or returned encyclopedia text. The pattern is natural and plausible, but its attestation rests on the author's receipt.
- Dictionary records come from the author-supplied rendering and receipts, not my own retrieval.
- I counted the ten added exclusion pairs myself. I did not re-count the totals of 16 guarded cards and 91 declarations.
- The carried-forward scope was not re-reviewed.
- Naturalness of the sentences is my judgement, not a native-speaker certification.
