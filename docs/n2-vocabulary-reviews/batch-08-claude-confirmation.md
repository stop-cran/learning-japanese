## Snapshot
**5cabdf7ea6ee50bf59bc1a743c76f7797dfcbd6f**, parent c3e705025de8ed252789968a9a37ab0535ddf3a3. I didn't run Git, so the commit identity, clean tree and every SHA-256 value are the author's claims, not something I verified.

What I did check by reading files:
- The working files contain every change in the supplied patch.
- The six cards' hashes in `manifest.json` match the snapshot receipt. The supplied patch doesn't include `manifest.json`.
- The new `coverageIndexSha256` value in `docs\n2-vocabulary-snapshot.json` is the same as the receipt's TSV hash. I couldn't recompute it.

## Scope
- **Model:** claude-opus-5.5 (claude family), working alone.
- **Changed cards, read in full:** 延長, 応ずる, 応接, 応対, 往復, 追い越す.
- **Provenance:**
  - N2:148 in `n2-vocabulary-sources.tsv`
  - `batch-08.json:134` and the new evidence block in that file
  - the snapshot-index line in `docs\n2-vocabulary-snapshot.json`
- **Comparison cards, read in full:** 続き, 受ける, 扱う, 便り, 越える.
- **Dictionary records checked (JMdict, the open Japanese–English dictionary):**
  - 1176510 (延長), all senses
  - 1179760 (往復), 1179930 (応接), 1179980 (応対)
  - 1329590 (受ける): sense 5, and sense 13, which is restricted to the game of Go
  - 1593070 (越える): senses 1–2
  - the three newly added families: 扱う, 便り, 続き
- **Author receipts:** I fetched all four Kotobank pages myself, and each matches the author's claim.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 延長 | CLEAN | CLEAN | CLEAN |
| 応ずる | CLEAN | CLEAN | CLEAN |
| 応接 | CLEAN | CLEAN | CLEAN |
| 応対, including the reworded sentence | CLEAN | CLEAN | CLEAN |
| 往復 | CLEAN | CLEAN | CLEAN |
| 追い越す | CLEAN | CLEAN | CLEAN |
| N2:148 source note | CLEAN | CLEAN | CLEAN |

Each new quiz exclusion has real overlapping dictionary meanings behind it:

| Card | Excludes | Shared meaning |
|---|---|---|
| 延長 | 続き | Both have "continuation" (延長 sense 3). Daijisen also defines 続き as 「あるものの延長」. |
| 応ずる | 受ける | The title's "accept" matches 受ける sense 5, "accept (a challenge)". That is the ordinary sense, not the Go-only sense 13. |
| 応接 | 扱う | Both have "deal with". 扱う sense 1 is "deal with (a person); entertain". |
| 応対 | 扱う | Both have "dealing with / handling". Nikkoku's 扱う definition ② cites 応対. |
| 往復 | 便り | Both have "correspondence" (往復 sense 3). Daijisen 往復 definition 2 is 「手紙などのやり取り」. |
| 追い越す | 越える | 越える has "surpass" and "go past". 超える is only a spelling preference, not a restriction. |

Other checks:
- **Exclusion lists:** every target exists, with no repeats or self-references, and none of these cards has `quiz_distractors` that could conflict.
- **応対 rewording:** the first example has no を, so "In the second example" is unambiguous and accurate.

## Findings
- **F1 (N2:148 source note): resolved.** JMdict 1176510 senses 4, 5 and 6 are mathematics, philosophy and the Enchō era, exactly as the new note says. The selected senses 1, 2, 3 and 7 are unchanged, and the old wording appears nowhere in the three provenance files. Writing "Encho" without the macron is acceptable.
- **F2 (追い越す / 越える): resolved** by the new exclusion.
- **O1 (応対 wording): resolved**, adopted as I suggested.
- **O2 (往復 / 帰り): optional, unchanged.** Still no action needed. The new 便り exclusion is a separate, justified pair.

No regressions or new actionable defects.

## Optional
None needed. If you want, a one-line contrast in the body text could explain the 延長/続き or 往復/便り exclusions, but the cards don't need it.

## Limits
- **Not run:** Git, `validate.py`, `build_manifest.py` and the app. I checked reference integrity by reading the files.
- **Not reviewed:** I only reviewed the assigned changes, not the whole batch or the rest of the content.
- **Not certified:** CLEAN means no defect found in this scope; it is not native-speaker certification.
