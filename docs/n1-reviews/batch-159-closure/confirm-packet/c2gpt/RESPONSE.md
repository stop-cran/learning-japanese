# Author's statement for the reviewer of the confirmation report on `5c04be73`

This statement answers only the points in YOUR confirmation report on `5c04be73` (the earlier confirmation report named in `INSTRUCTIONS.md`). F2 and F4 are the two findings you marked PARTIALLY RESOLVED. OPT is your Optional line (ledger line 946). L2 and L3 are the two Limits you marked PARTIALLY RESOLVED. You marked F1, F3 and F5 RESOLVED and accepted the declines for O1 and L1; the text behind them is unchanged in this revision.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (`CHANGES.md` lists every line): one front-matter line and one Notes line of `kanji\吟.md`, one body line each of `words\太后.md` and `words\吟味.md`, five ledger lines, and the regenerated `manifest.json`. Give a disposition for F2, F4, OPT, L2 and L3, and judge the other reviews' changes described at the end.

## F2: 吟 / 験 overlap

Author action: **changed**, as you asked.
- `kanji\吟.md:14` adds 験 to `quiz_exclusions`: [詩, 歌, 謡, 句, 検, 審, 査, 調, 究, 研, 験].
- Line 42 names it with its title: “…究 (“investigate thoroughly”), 研 (“polish; study closely”) and 験 (“test; verify”) overlap with the sense of examining something closely, as in 吟味.”
- 診 偵 試 察 鑑 覧 stay unexcluded, as you accepted.
- The exclusion check is symmetric (`evidence\QuizBuilder.kt` line 26). The meaning options of 吟 are still 二 自 社 (`checks\quiz-safety.txt` line 16).

## F4: 叔's justification and point 2

Author action: **wording changed**; 伯叔 is **kept**, now as a disclosed author's exception, not as a case of the untagged route.

- **What changed.** Ledger line 78 (`exceptionReason`) no longer says that no candidate qualifies. It now says:
  - the row is an author's exception to point 2's preference, reported to the owner for a decision;
  - under the letter of point 2, the tagged spellings 叔父 (1607070) and 叔母 (1607100), both ichi1/news1, are candidates, because their readings しゅくふ and しゅくぼ use シュク and carry no flagged mark.

  Line 29 (`selectionReason`) no longer counts 叔 among the untagged-route rows: two rows (后 吏) take that route, and the 叔 row is an author's exception to the tagged-spelling preference, reported to the owner. Line 952 (`status`) says the same. The full text of line 78 is quoted in `CHANGES.md`.
- **Why the exception is kept for now.**
  - The tags in those entries also sit on the whole-word readings おじ and おば (`evidence\jmdict-cited-entries.xml`), which the Joyo table gives for 叔父 and 叔母 (`evidence\joyo\p75.txt`, lines 44–46, and the appendix on `p162.txt`).
  - An article headed 叔父 or 叔母 would teach おじ or おば as its primary reading.
  - B156 applied the same interpretation to 伯父 and 伯母 when it kept 伯仲 for 伯. `evidence\b156-selection.json` quotes the published B156 selection statement: “伯仲 is kept because 伯父 and 伯母 are tagged only for their whole-word readings おじ and おば … All three review families accepted these row decisions.”
- **The owner's decision.** No owner decision exists yet, so the ledger does not claim one. The author will ask the owner on issue #60 whether this interpretation stands for 叔 and for B156's 伯. If the owner prefers the letter of point 2, the fallback named in line 78 is an article headed 叔父 whose reading is しゅくふ, which would be a later revision.

Please judge whether the row is now described accurately. Also judge whether a disclosed author's exception with a pending owner question, applying the same interpretation the published B156 row used, is acceptable for confirmation. If you hold that the batch cannot be confirmed until the owner decides, or until the 叔父 (しゅくふ) fallback is used, say so.

## OPT: ledger line 946 overstated reading-option completeness

Author action: **changed**, and the earlier statements are corrected.
- **Ledger.** Line 947 (formerly 946) now says the following. The curated distractors fill all three wrong options of each meaning question. For the reading questions, nine cards are filled by their curated options in every outcome. For 吟's ギン prompt, 二 (ニ, ジ) and 自 (ジ, シ) both show ジ in one of four outcomes, and the fallback fills the open slot: 61 drawable wrong options in the N1 and All stacks (4 curated, 57 fallback) and 27 in the Starter practice session, with no exposure hit.
- **App code.** `evidence\KanjiReadings.kt` (new in this packet, from the pinned Android commit; see L2) shows the mechanism:
  - line 110: each curated card gives one random reading;
  - line 100: a repeated key is dropped;
  - line 111: the closeness fallback fills the slot.
- **Correction.** `CHANGES.md` (“Correction to the earlier statements”) also withdraws the earlier RESPONSE's line that 吟's curated distractors “fill all three slots in every shipped pool”. That line is true for the meaning question and false for the reading question.

## L2: manifest freshness and the kanji-reading builder

Author action: **evidence added** for the builder; manifest unchanged in kind.
- **The builder.** `evidence\KanjiReadings.kt` is the app's `KanjiReadingQuiz` at kanji-cards-android commit `91e1d4b578859f7bfb582f7b9c6acf48c6ca6a75`. `evidence\app-code-SOURCES.json` gives each file's Git blob id with its raw and web URL, so you can fetch and compare it. `checks\reading-exposure.txt` and `checks\reading-options.txt` are Python ports of `question` (lines 91–116).
- **The manifest.** It is still evidenced by `checks\manifest.txt` (rebuild identical) and `checks\audit.txt` (fresh, `c459784ce290b1ef`). The packet's `snapshot\` holds only the batch cards and the changed files, so the manifest cannot be rebuilt from the packet; this remains a transcript.

## L3: Git object and key authenticity

Author action: **evidence extended**. `evidence\verify-commit.txt` now covers `1a9bb910`, `5c04be73` and `4f8ebea7` (each `git verify-commit -v` with its parent line) and `git log --show-signature` for `2787e43b..4f8ebea7`. As you note, this is the author's transcript; the packet cannot authenticate the signing key independently.

## Changes made for the other reviews

The other two reviews confirmed `5c04be73` with optional notes. Please judge each change as a reviewer of the revised text.

1. **太后** (`words\太后.md:15`).
   - Both reviews said that “…the empress of the previous emperor, or one who is also the current emperor's birth mother” could be read as two different people.
   - The sentence now reads: “In plain terms, Digital Daijisen describes 太皇太后 as the empress of the emperor two reigns back and 皇太后 as the empress of the previous emperor; in a narrower sense, 皇太后 is such an empress who is also the current emperor's birth mother.”
   - Sources: Digital Daijisen 皇太后「前天皇の皇后。また、前天皇の皇后で、現天皇の生母。」 and 太皇太后「先々代の天皇の皇后。」 (`evidence\daijisen-kotobank.json`).
2. **吟味** (`words\吟味.md:24`).
   - One review noted that “savoring its flavor” was attributed to both sources, while only Daijisen says 味わう.
   - The last sentence now reads: “Both sources mark poetry recitation as the original meaning of 吟味: Digital Daijisen sense 3 is reciting a poem and savoring its flavor, and JMdict sense 4 (archaic) is “reciting and appreciating traditional poetry”.”
   - Sources: Daijisen 吟味 《3が原義》 and JMdict 1243390 sense 4, [arch], s_inf “orig. meaning”.
3. **Notes with no change:**
   - the exclusion of 確認 from 吟味 stays, for consistency with 確かめる;
   - the 吟 exclusions stay. One review called them harmless over-exclusion, since the curated meaning distractors never use them.
