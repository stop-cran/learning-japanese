# Batch 138 — second confirmation review (reviewer 1)

Snapshot: commit 3158b2b97cc9ba61368b722d0c45c37536a909c5 (revised from acf7297ef66a82f620a6c5551d95a2e3fa356bc7, which I confirmed; initially reviewed b6020f9e490298de1756e33c51bf9ce314132f4e). Reviewer model: Claude (Anthropic model family), working alone and read-only. I did not look for or see the other reviewer's report.

Scope:
- This packet (`confirm2-138-claude`):
  - Read in full:
    - `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`.
    - `diffs\fix.patch` (one hunk, `kanji/契.md`) and `diffs\changed-lines.txt`.
    - `evidence\extras-merge-fix.txt`.
    - `snapshot\kanji\契.md` (all 60 lines).
  - Read in part:
    - `evidence\Words.kt`: the `ReadingOptions` voicing map, the constants and `mutations()` (lines 215–270).
    - `checks\reading-exposure.txt`: lines 1–3, 145–156 and 258–262.
    - `checks\reading-options.txt`: line 1, lines 15–18, 128–134, 158–162 and the last 3 lines.
  - Checked by script without reading line by line:
    - Every line except line 1 of `checks\reading-exposure.txt` and `checks\reading-options.txt` was compared with `evidence\reading-exposure-b6020f9e.txt` and `evidence\reading-options-b6020f9e.txt`: 0 differences in each.
    - The SHA-256 of `checks\quiz-safety.txt` was compared with the original packet's `evidence\audits\quiz-safety.txt`: identical, 2A47B4C5…5D65B205.
    - All 15 cards in `snapshot\kanji\` were hashed against the earlier confirmation packet's `snapshot\kanji\`. Only 契.md differs, and a line comparison shows only line 43 changed; both files have 60 lines.
  - Not opened:
    - `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\kanjipedia-契.txt` (I read the earlier packet's copy and the live page in the last round), `evidence\KanjiReadings.kt` (read in full last round), `evidence\QuizBuilder.kt` (read in full last round), `evidence\meta_scan.py`, `evidence\meta-scan.txt`.
    - `checks\lint.txt`, `checks\unittest.txt`, `checks\validate.txt`, `checks\budget.txt`, `checks\vocabulary.txt`, `checks\manifest.txt`, `checks\link-targets.tsv`. The last of these lists no links, according to `CHANGES.md`, and the changed line's only link (Kanjipedia) is unchanged in the patch.
- Earlier confirmation packet `confirm-138-claude`, read-only: `snapshot\kanji\*.md`, hashed and compared as above.
- Original packet `batch-138-b6020f9e`, read-only: `evidence\audits\quiz-safety.txt`, hash only.
- My own earlier reports, from context. I did not reopen the files.
- Public web: none needed this round. The 契闊 reading was verified last round on the live Kanjipedia page (契闊(ケッカツ)).

Dispositions:
- P1 - RESOLVED - `契.md:43` now reads "as in 契闊 けっかつ, not seeing someone for a long time".
  - The patch has one hunk, and that hunk changes only ケッカツ to けっかつ. The new kana is the exact hiragana counterpart of Kanjipedia's ケッカツ (ケ→け, ッ→っ, カ→か, ツ→つ), so the reading is unchanged apart from the script.
  - Every other word reading on the card is in hiragana: けいやく, ちぎる, きったん, もっけい, けいいん, けいき, しょけい, ちぎり, けいごう. The card is now consistent.
  - The line still distinguishes the reading names キツ and ケツ (katakana for on readings) from word readings (hiragana), which is the card's own convention.
  - Nothing else on the card changed.
- A1 - RESOLVED - The corrected audits are as stated, and my earlier verdicts still hold.
  - **Line 1 of both corrected outputs passes every reading in `extras-merge-fix.txt` section 3**, each as a single merged `--extra` per kanji:
    - 垂: しで, なんなん.とする, しず.る, しずれ
    - 執: とら.える
    - 壊: エ, やぶ.る, やぶ.れる, こわ.る
    - 奏: すす.める, もう.す
    - 奪: タツ
  - **Section 3's claim about たつ is true.** `ReadingOptions.mutations` maps 'だ' to "た", so たつ is a voicing variant of 奪's だつ and is excluded anyway.
  - **The new case is as described.**
    - `reading-exposure.txt` lines 146–153: 壊's kun prompt こわ.す lists やぶれる as an attested reading offered by 敗 and 破. It "cannot be drawn in the N1 stack, All stack or Starter practice session pool", and it is "not drawable with any single holder (2 holders tried)".
    - The risk class on line 153 is limited to pools that are "not a pool the app builds from the shipped stacks".
    - `reading-options.txt` line 132 gives the matching note: lower closeness tier, not drawable from the full pool.
  - **Why it cannot be drawn.** 壊's curated distractors fill only 2 of 3 kun slots, because 塔 has no usable kun reading (line 129). The open slot is filled from tier 4, which holds こがす, こす, こぼす, こらす, ころがす and ころす. やぶれる differs in length by 2 and shares neither first nor last kana with こわす, so it scores below tier 4. It is never reached while tier 4 has candidates. Sampling saw 13 of 13 drawable options over 200 seeds, and none was やぶれる.
  - **Summary lines.** Line 261: 0 production hits, 0 padded-session hits, 9 latent collisions. Line 262: 0 one-holder padded hits, 0 more for KANJIDIC2 name-only readings. `reading-options.txt` still reports 2 problems: 噴 ほん (line 17) and 契 けつ (line 160).
  - **Same output at the reviewed snapshot.** Apart from line 1, the outputs are byte-for-byte the same as at b6020f9e, by script comparison. This is consistent with no revision having changed a reading or a `distractors` list.
  - **Correction to my confirmation report.** It quoted 8 latent collisions; the correct figure is 9. It also explained the "(card text)" label on 契 けつ as arising because the card now mentions ケツ. `extras-merge-fix.txt` section 1 says the tools label every `--extra` reading "(card text)" whatever its source. The label therefore says nothing about the card, and my earlier inference from it was wrong. Neither point changes a verdict.

Verdicts:
- Correctness: CLEAN. The changed hunk is a script-only change to a correct reading, and it agrees with the untouched text of 契.md. The other 14 cards are byte-identical to the acf7297e text I confirmed.
- Scoped coverage: CLEAN. No coverage changed.
- Consistency and quiz safety: CLEAN.
  - **Meaning quiz.** No front matter changed, and `quiz-safety.txt` is byte-identical to the audit I checked in full in the last two rounds. Every one of the 15 cards still has three curated wrong options that are defensibly wrong against its displayed title. The symmetric exclusion in `QuizBuilder.excluded` (read in the last round) is unaffected.
  - **Reading quiz, with the corrected audits.** There are no production or padded-session hits.
    - The newly checked readings 垂 なんなんとする, しずる and しずれ, 執 とらえる, 壊 こわる and 奏 すすめる and もうす are offered by no other card.
    - 壊 やぶれる is latent only, as shown above.
    - 噴 ほん and 契 けつ remain latent only while the curated distractors fill all three slots.
- Comprehensibility: CLEAN. Hiragana for a word reading matches the rest of the card and is easier for a beginner to read than katakana, which the card reserves for reading names.

Confirmation: CONFIRMED

Findings: none.

Optional: none.

Limits:
- **What the audits cannot show.**
  - Both tools model the N1 stack, the All stack and the Starter practice session, plus single borrowed holders. They do not model custom or smaller pools.
  - In a pool without 壊's curated cards 均 and 埋, やぶれる could be offered as a wrong option for 壊 こわす (risk class at line 153), as could 噴 ほん and 契 けつ in the matching cases. 壊 already relies on the fallback for one kun slot in every pool, so whether its third option is safe depends on which cards are in the pool.
  - I treat all of these as latent risks under O9, not as defects in this batch.
  - The audits cannot show behavior in older APKs or future content, and the tools do not read `quiz_exclusions`.
- **Not run.** The Android JVM content tests and the Kotlin cross-check of the reading audit were not run for this revision.
- **Taken on trust.**
  - The two audit tools and the gate runner are not in the packet. I verified their arguments (line 1) and their outputs, but not their code. The parsing defect and its fix in `extras-merge-fix.txt` are the author's statement.
  - The claim that batches 135–137 are unaffected is outside this batch and was not checked.
  - I did not open the lint, unittest, validate, budget, vocabulary, manifest or meta-scan outputs, and I take the `CHANGES.md` summaries of them on trust.
- **Not re-checked this round.** I did not open this packet's copy of `kanjipedia-契.txt` or re-fetch the live page. The katakana form ケッカツ was verified on the live page last round, and the change is a pure script conversion.
- Every response in this round contained exactly one tool call.
