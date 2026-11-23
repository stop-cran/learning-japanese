# Author's statement for the reviewer of the confirmation report on `5c04be73`

This statement answers only the points in YOUR confirmation report on `5c04be73` (the earlier confirmation report named in `INSTRUCTIONS.md`). You confirmed `5c04be73` with no findings. O1–O3 are the three points of your Optional line in order: 太后 wording; 吟味 attribution; 確認 on 吟味. LIM is the Limits points that call for an answer.

This packet covers five revisions, `4f8ebea7`, `54b00e0c`, `f85ff382`, `0ba7df63` and `bad899ea`; you did not review them. `diffs\fix.patch` shows the combined change from `5c04be73`.

The statement is the author's claim about what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs, the `evidence\` files and independent sources; do not rely on this text as evidence. Line numbers refer to the revised files in this packet.

What changed, in brief (`CHANGES.md` lists every line): the 叔 support article `words\伯叔.md` is replaced by `words\叔母.md`; three lines of `kanji\叔.md`; two lines of `kanji\吟.md`; `kanji\伯.md` is restored to its batch-base text; one line is added to `kanji\母.md` (in `f85ff382`, that line gives the usual reading おば first); one body line each of `words\太后.md` and `words\吟味.md`; the ledger is regenerated for these changes, and its lint statement (line 948) and reading-options statement (line 953) are corrected; `manifest.json` is regenerated. Give a disposition for O1–O3 and LIM, and judge the other reviews' changes described below.

## Optional notes

### O1: 太后 wording (“or one who is also”)

Author action: **changed**. `words\太后.md:15` now reads: “In plain terms, Digital Daijisen describes 太皇太后 as the empress of the emperor two reigns back and 皇太后 as the empress of the previous emperor. In a narrower sense, 皇太后 is such an empress who is also the current emperor's birth mother.” Sources: Digital Daijisen 皇太后「前天皇の皇后。また、前天皇の皇后で、現天皇の生母。」 and 太皇太后「先々代の天皇の皇后。」 (`evidence\daijisen-kotobank.json`).

### O2: 吟味 attributes “savoring its flavor” to both sources

Author action: **changed**. The end of `words\吟味.md:24` now reads: “Both sources mark poetry recitation as the original meaning of 吟味. Digital Daijisen sense 3 is reciting a poem and savoring its flavor, and JMdict sense 4 (archaic) is “reciting and appreciating traditional poetry”.” Sources: Daijisen 吟味 《3が原義》 (`evidence\daijisen-kotobank.json`) and JMdict 1243390 sense 4, [arch], s_inf “orig. meaning” (`evidence\jmdict-cited-entries.xml`).

### O3: 確認 on 吟味 is not a displayed-title overlap

Author action: **none.** As you note, it was added for consistency with the existing exclusion 確かめる, and it only removes a distractor.

## Limits

### LIM: reading safety, and `support_spelling`

- **Reading safety.** The packet now includes the app's kanji reading-question builder, `evidence\KanjiReadings.kt`, from the pinned Android commit listed in `evidence\app-code-SOURCES.json`. Writing the corrections, the author found that the ledger's earlier statement on reading questions was too broad. It is now corrected (ledger line 950; `CHANGES.md`, “Correction to the earlier statements”).
- **`support_spelling`.** No change. As you note, the repository audit checks the spelling, the reading and the reading's restrictions (`lexical_pair` in `tools\audit_n1_batch.py`, lines 45–57; the file is unchanged since `5c04be73` and is in the earlier confirmation packet's `snapshot\tools\`) but does not itself reject ateji or gikun marks. For 又, `evidence\jmdict-scan-c3.txt` lists the spelling marks: 又 (entry 1524930) and 又は (entry 1524990) carry none, while the other spellings 亦 and 復 of entry 1524930 are marked as rarely used kanji forms. For 叔母, the spelling carries no `ke_inf` mark and しゅくぼ no `re_inf` mark (`evidence\jmdict-cited-entries.xml`, entry 1607100).
- **伯叔 examples.** Your limit that the rare 伯叔 examples were not corpus-checked no longer applies: the 伯叔 article is deleted (change 2 below).

## Changes made for the other reviews

Please judge each change as a reviewer of the revised text, not only as an answer to your own notes.

1. **吟 / 験** (`kanji\吟.md:14` and 42).
   - Another review asked to exclude 験 (“test; verify”), because Digital Daijisen's first sense of 験, 証拠によって確かめる, overlaps 吟's taught sense 内容を探り確かめる.
   - Line 14 adds 験 to `quiz_exclusions`, and line 42 names it with its title.
   - The curated meaning distractors 二 自 社 are unchanged (`checks\quiz-safety.txt` line 16). The exclusion acts only in fallback or custom pools (`evidence\QuizBuilder.kt` lines 26–34).
2. **叔 support: 伯叔 is replaced by 叔母 (しゅくぼ)**, which reverses the row you confirmed.
   - Another review held that, under the letter of point 2 of the issue #60 rule (`evidence\rule-7058679348.md`), a tagged spelling qualifies when its reading uses a KANJIDIC2 reading of the kanji and carries no excluded mark; the reading itself need not be tagged. The tagged spellings 叔父 and 叔母 (ichi1/news1) are therefore candidates through their unflagged, restricted readings しゅくふ and しゅくぼ, and the earlier statement that no candidate qualifies was wrong. `4f8ebea7` kept 伯叔 as an author's exception awaiting the owner; that review then asked for the qualifying fallback or explicit owner acceptance before publication. `54b00e0c` follows the letter of point 2.
   - 叔母 (entry 1607100) is used. 叔父 (entry 1607070) qualifies in the same way but is not used: 精選版 日本国語大辞典 gives the variant reading しゅくぶ for 叔父 (「( 「しゅくぶ」とも )」) and none for 叔母 (`evidence\daijisen-kotobank.json`, field `nikkoku`). The word reading quiz always shows two generated look-alikes (`evidence\Words.kt` lines 256–268), and しゅくぶ is one of the five look-alikes of しゅくふ, so it would be shown as a wrong option in 4 of 10 pairs (`evidence\reading-lookalikes-c3.txt`). None of しゅくぼ's five look-alikes is recorded.
   - `words\叔母.md` is new. It cites Digital Daijisen 「父母の妹。おば。」 and JMdict sense 1 “aunt”, gives two original examples, and its “Distinctive meaning” section (line 32) says that 叔母 is also read おば (the Joyo special reading, and the reading JMdict tags) and that not every printed 叔母 is pronounced しゅくぼ.
   - `kanji\叔.md` lines 29, 34 and 38; `words\伯叔.md` deleted; `kanji\伯.md` back to its batch-base text; `kanji\母.md:38` adds the 叔母 line. Word quiz: 伯母さん, 親戚 and 親類 are excluded; 0 problems (`evidence\word-quiz.txt` lines 70–97).
   - Your Correctness verdict on `5c04be73` accepted the earlier reasoning (“叔父/叔母 tags belong to おじ/おば, not to シュク”). Please judge the new row on its own terms.
3. **Reading-option statements** (ledger line 950, and a correction in `CHANGES.md`).
   - The earlier ledger and one earlier RESPONSE said that the curated distractors fill all three wrong options of every reading question, or of every shipped pool for 吟. That holds for meaning questions.
   - For 吟's ギン prompt, it does not: 二 and 自 both show ジ in one of four outcomes, and the fallback fills the open slot (`checks\reading-exposure.txt` lines 138–150; `evidence\KanjiReadings.kt` lines 100 and 110–111).
   - The audit finds no exposure hit, and the card is unchanged.
4. **Ledger lint statement** (ledger line 948, in `0ba7df63`).
   - Another review of `f85ff382` found that the sentence “Of the 37 warnings, 35 are on reused cards and words.” no longer matched `checks\lint.txt`, which has reported 42 warnings since `kanji/母.md` entered the lint scope at `54b00e0c`.
   - The sentence now reads: “Of the 42 warnings, 40 are on reused cards and words. They report a missing N1 source-index entry, quiz reading list or Metadata line, or a missing Dictionary line or one that cites no JMdict entry id; B159 changes none of these fields, because it only adds or links one Common words line on each of those cards and does not change those word articles.”
   - `CHANGES.md` lists the warnings by kind, and `evidence\reused-lint-diff.txt` shows what B159 changes in the 20 warned files.
5. **Ledger reading-options statement** (ledger line 953, in `bad899ea`).
   - A confirmation report on `0ba7df63` noted that the statement named only the 呉 ぐ informational note, while `checks\reading-options.txt` also has one for 吉 き (line 74).
   - The statement now names both and says that the curated options fill all three wrong slots of both prompts, so the fallback is never consulted (`CHANGES.md`, “The new reading-options statement”).
