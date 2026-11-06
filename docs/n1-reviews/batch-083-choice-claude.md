**Snapshot:** Signed 7cc896f488ae5315046453777aae6768b9ff18e8 (previous eb7e1b3781c707ef270b8a242c343e6cf388e2b9), as stated in the packet. I did not check Git, upstream sources or uncommitted state myself.

**Scope:**
- **Reviewer:** Claude Opus 5.5 (`claude-opus-5.5`), resuming my original batch-083 review. This is a dependent confirmation, not a blind review.
- **Read:** One resource, `control\batch-083-choice-confirmation-packet.txt`, with one `view` call (`forceReadLargeFiles=true`, no range). It returned in full through `content-format.md` line 125 with no truncation marker, so I made no recovery reads. The tool reports no byte or line totals. No access was denied.
- **Inspected:**
  - the one-line diff;
  - all eight article bodies: 凌, 准, 冶, 冴 and 次 kanji cards, and the 凌ぐ, 凌駕 and 冴える word articles;
  - all 14 JMdict families;
  - four complete KANJIDIC2 records;
  - the selection, source-evidence, correction-audit and font-audit JSON;
  - `QuizBuilder.kt` (lines 1–30) and `QuizViewModel.kt` (lines 65–160).
- **Changed choice:** `kanji\凌.md` only. The two word articles were checked for regression only.

**Verdicts:**
- `kanji\凌.md` (changed choice): correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- `words\凌ぐ.md` (regression only): correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- `words\凌駕.md` (regression only): correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.

**Findings:** None. These checks found no defect:

- **The fix addresses the failure mechanism.**
  - `QuizViewModel.start` builds `quizCards` only from cards in the selected stack (lines 91, 97).
  - `QuizBuilder.options` keeps only curated IDs found in that list (line 24), then fills empty slots by tag score with random order (lines 25–26).
  - 次 is `jlpt: 3` (`次.md:4`), so it is absent from the N1 stack. That left one random slot.
  - 冴 is `jlpt: 1` and tagged `jlpt-n1` (`冴.md:4–5`), so it is in the N1 stack, and it is also in All.
  - With 准, 冶 and 冴 all present and four distinct titles, `tryAdd` fills all three wrong-answer slots from the curated list, leaving no random slot when the default count is four.
  - This matches the audit's figures: N1 has 115 cards, All has 1,095, and both show zero fallback slots.
  - 次's level, the app algorithms and the selected stacks are unchanged.
- **冴's displayed title is still a wrong answer for 凌.**
  - I am not claiming the two characters' meanings never overlap. 冴える sense 4 is "to master; to excel at; to cleanly execute"; 冴え sense 2 is "skillfulness"; KANJIDIC2 lists "skilful" for 冴.
  - 凌ぐ sense 3 includes "to excel." So an undisplayed "excel" overlap exists.
  - The displayed label is only "clear; sharp-minded." That matches 冴える senses 1–2 (clarity, alertness). None of 凌's sources gives clarity or alertness: 凌ぐ senses 1–3, 凌駕's surpassing sense, and the 凌 KANJIDIC2 meanings (endure, keep rain out, stave off, tide over, defy, slight, surpass).
  - A learner could not reasonably pick "clear; sharp-minded" for 凌. No exclusion is needed.
- **准 and 冶 are still safe.**
  - 准's other senses are its rarely used spellings (准える, 准じる, 准ずる: liken, imitate, conform, correspond) and ratification (批准).
  - 冶's other senses are melting, metallurgy, and 陶冶 (training/cultivation; pottery and metal casting).
  - None of these makes their displayed titles a meaning of 凌.
- **No regression.**
  - In `凌.md`, only line 13 changed (SHA256 0577… → 187e…).
  - Unchanged: title, readings and their order, selected quiz readings, all prose, and the Notes comparison with 次 (a body comparison need not be a quiz option).
  - The 凌ぐ and 凌駕 word articles are byte-identical (aac06d…, df0994…), so the 17 direct word exclusions are unchanged.
  - 冴 shares the visible 冫 marks, and no shape relationship is claimed beyond that.

**083-NATIVE-574-CHOICE:** Textually resolved for the default four-choice question in the complete N1 and All stacks. Runtime acceptance is outstanding and separate: the corrected HOST checks, archive, fixture and APKs, both named native cases, and the updated inventory (30 Han characters, 120 individual and 8 whole-word probes, four fonts, Paint/Compose PNG). Dependent visual confirmations are also still pending.

**Optional / new concerns (not findings for this change):**
- **Same mechanism elsewhere (legacy, not a regression, extent unverified):** `冴.md:13` lists 次 (N3) as a distractor, so a 冴 question in the N1 stack will also lose a curated option and get a fallback. I could not check the levels of 汗 and 河 from this packet.
- **Extra-practice padding:** `QuizViewModel.pad` (lines 115–128) adds only the borrowed cards to the list of possible quiz choices. If 凌 is borrowed into another stack's extra session, its N1 distractors may be unavailable there. This existed before the change and is outside the certified default N1/All scope.

**Limits:**
- Static text and source evidence only, all supplied in the packet. I checked no Git or upstream sources myself and ran no live QuizBuilder, Android, native, font, PNG or physical-phone tests.
- I make no native-speaker or learning-effectiveness claim.
- Nothing here certifies custom, partial, larger, padded or random stacks, or reverse questions for unrelated targets.
- The production code was read only in the supplied line ranges.
