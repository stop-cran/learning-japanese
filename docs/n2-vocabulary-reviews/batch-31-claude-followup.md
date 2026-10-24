## Snapshot
- **New commit:** `fd0bfd6ca17d51c7500eb72b5602f6af65dafb42`. Its parent is the corrected `51c96bc0b0f9ce230db86a55971efe258c17d61e`.
- The receipt lists no learner-content changes. Its only changed file is `docs/n2-vocabulary-batch-sources/batch-31.json`.
- **Provenance limits:** I can't run Git or compute hashes. The following are author-executed receipts that I haven't verified:
  - commit identity and clean state;
  - the diff, file, evidence and input hashes;
  - byte preservation of the rest of the file;
  - the derivative's equivalence to the canonical source packet.

## Scope
- **Model:** claude-opus-5.5, claude family. I worked alone, read-only and without delegation.
- **Read:**
  - My own prior confirmation report.
  - The follow-up receipt and the complete patch, which has two hunks: the provenance sentence and the appended `confirmationFollowThrough` block.
  - The complete compact rendering, all 162 lines.
  - All `entry` and `index` keys in the raw 25-family extraction.
  - In `batch-31-followup-evidence.json`: section boundaries, the family locations, the corrected provenance (line 21757), the whole appended block (22223–22258) and the full family 生/なま 1378450 (7971–8260).
- **Counting method:** I counted with grep and by reading the files myself, not with a script.
- **Not read:** the canonical source packet (forbidden), ledgers, author notes and other reports.
- **Not re-reviewed:** the twelve articles.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Corrected evidence count (provenance plus `confirmationFollowThrough`) | CLEAN | CLEAN | CLEAN |

## Findings
**GPT31-04 (the count) — resolved.** My own counts match every figure in the corrected provenance:

| Count | Value | How I verified it |
|---|---|---|
| ENTRY headers in the rendering | 25 | grep |
| Indexed sense lines in the rendering | 62 | grep, and by reading each entry |
| Families in the raw extraction | 25 | grep for `entry` keys |
| Sense indices in the raw extraction | 62 | Each family numbered 1..n with no gaps, same per-entry counts as the rendering |
| Previously captured families / senses | 12 / 35 | 1378440, 1378450, 1404700, 1587180, 2036160, 2088240, 2416400, 2416410, 2416420, 1005430, 1476430, 2461070, all in `comparisonEntryFamilies` |
| New families / senses | 13 / 27 | 1100760, 1176320, 1198160, 1198170, 1198530, 1298090, 1298100, 1343950, 1476410, 1492680, 1532800, 1533550, 1609050, all in `additionalComparisonEntryFamilies` |
| Physical lines in the rendering | 162 | 137 non-blank plus 25 blank lines |

- **Where 137 came from:** it equals the 137 non-blank lines (25 × 3 entry header/spelling/reading lines, plus 62 sense lines). It counted lines, not senses.
- **Forms:** the 25 families map to the sixteen stated forms.
- **Remaining "137":** the only place it still appears is `previousFalseProvenanceStatement`, which is explicitly labelled as the former false statement.
- **Spot check:** family 1378450 in the evidence ends at sense 12 ("tipsiness"), matching the extraction.

**My own prior confirmation — corrected (superseded).**
- My Scope repeated the author's "25 families and 137 senses" without counting. That figure was wrong; I withdraw it and replace it with 62.
- I also gave the appended evidence correctness CLEAN, which missed this count error. It is now resolved.
- My lexical conclusions are unaffected, because I had read the complete rendering.
- B31-R-01 to R-06 remain resolved; no articles changed.

**Regressions:** none. The change is evidence-only and internally consistent. No dictionary records, guards, articles or mappings are touched in the patch.

## Optional
- The correct-count block could also record the 137 non-blank-line count, so readers can see where the old figure came from. This is nonblocking.

## Limits
- I didn't verify the hashes in `inputSha256`, the receipt hashes, or byte preservation outside the two hunks.
- I compared all 62 records' IDs and positions between the extraction and the evidence file. I compared field contents only for family 1378450.
- My counts came from grep and reading, not executed parsing. Whether the rendering ends with a final newline doesn't change the 162-line count.
- The lexical scope of my prior review is unchanged.
- No app was run. Nothing here rests on measured frequency, native-speaker certification or an official JLPT syllabus.
