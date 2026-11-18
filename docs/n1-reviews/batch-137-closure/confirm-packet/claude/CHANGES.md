# Batch 137 revision: what changed from d3c7394d to 2bc8e9b1

Revised snapshot: `2bc8e9b13ea85b39c533735f63643af44d1ce690`, a child of the reviewed snapshot
`d3c7394d38992b24d3689bc984fdb4a6cf60bc54`. Nothing is published.

- Eleven of the 15 kanji cards changed: 丁, 仰, 但, 傑, 僕, 卸, 司, 吐, 呂, 哲 and 善. The other four (井, 傷, 哀, 唯) are
  unchanged. So are all 15 stroke files, the whole front matter of every card (titles, tags, metadata readings,
  `distractors` and `quiz_exclusions`), the two older kanji cards the batch edits (寧, 敷) and all 21 word articles the
  batch edits. Each of those 23 files still differs from the published text exactly as in the reviewed snapshot.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot). No line was added or
  removed, so they are also the line numbers of the reviewed snapshot.
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Every quoted title on a changed line was checked by script against the linked card's real `title:` (see
  `checks\link-targets.tsv`). In two rows there, 傑 lines 33 and 42, the gloss after the link to the word article 傑作 is
  not in quotation marks, so the last column says `n/a`. That gloss now ends with the label `(jocular, dated)`, which the
  word article's unchanged title, `masterpiece; hilarious absurdity`, does not have; the difference is intended.
- Cause of the 16 title defects: the author's working table of card titles, used when drafting the Notes, had lost the
  space after every comma inside a title. The table was rebuilt from the cards' front matter, and the 16 quotations now
  copy the exact titles. A script then compared every quoted title of a linked card or word article in all 15 cards (143
  quotations) with the target's `title:` and found no other mismatch.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 丁 | 40, 68 | Line 40: the よほろ sentence now ends `KANJIDIC2 does not list よほろ, and JMdict has no standalone entry for it; it appears only in つかえのよほろ, one reading of 仕丁 しちょう, which JMdict marks archaic and glosses "men pressed into forced labor (ritsuryō system)."` (it ended `KANJIDIC2 does not list よほろ, and JMdict has no entry for it.`). Support: `evidence\jmdict-cited-entries.xml`, entry 2829360 (仕丁; readings しちょう, じちょう, してい and つかえのよほろ; sense 1, tagged `archaic`, is "men pressed into forced labor (ritsuryō system)"; sense 2 is restricted to the other three readings). In the pinned JMdict, 2829360 is the only entry with a reading containing よほろ (author's search). Line 68: 町 is quoted as `"town, neighborhood,"` (it read `"town,neighborhood,"`). |
| 仰 | 58, 59 | Line 58: 見 and 上 are quoted as `"see, look,"` and `"up, above,"` (they read `"see,look,"` and `"up,above,"`). Line 59: the 仰山 example now ends `which JMdict marks as Kansai dialect in this sense and as usually written in kana.` (it ended `which JMdict marks as usually written in kana.`). Support: `evidence\jmdict-cited-entries.xml`, entry 1238920 (sense 1, "a lot; plenty; abundant; great many", carries `<dial>Kansai-ben</dial>` and `word usually written using kana alone`; sense 2, "exaggerated; grandiose", has no dialect tag). |
| 但 | 27, 47 | 日 and 昼 are quoted as `"sun, day,"` and `"daytime, midday,"` (they read `"sun,day,"` and `"daytime,midday,"`). |
| 傑 | 27, 33, 42, 46, 47 | Lines 27, 46 and 47: 木, 作 and 体 are quoted as `"tree, wood."`, `"make, produce,"` and `"body, form,"` (the comma had no space after it). Lines 33 (the ケツ row of the Readings table) and 42 (Common words): 傑作 is glossed `masterpiece; hilarious absurdity (jocular, dated)` (it read `masterpiece; hilarious absurdity`). Support: `evidence\jmdict-cited-entries.xml`, entry 1253840 (sense 2, "(unintentionally) hilarious; absurd (e.g. blunder); outrageous; wild", carries `jocular, humorous term` and `dated term`; sense 1, "masterpiece", carries neither). The word article `words\傑作.md` is unchanged; it already says that JMdict marks the second use jocular and dated. |
| 僕 | 50 | 仕 is quoted as `"serve, attend,"` (it read `"serve,attend,"`). |
| 卸 | 25, 33 | Line 25: the Daijisen おろし entry is now described as one that `defines as the act of a wholesaler selling goods to retail shops` (it read `defines as a wholesale dealer selling goods to retail shops`). Support: `evidence\weblio-卸-daijisen.txt` (the Daijisen block おろし【卸（し）】: 問屋が商品を小売店に売り渡すこと). Line 33: the シャ row glosses 卸下 しゃが as `cargo unloading (military term)` (it read `cargo unloading`). Support: `evidence\jmdict-cited-entries.xml`, entry 2537870 (`<field>military</field>`, "cargo unloading"). The row still says there is no word article and the word is not selected for questions. |
| 司 | 55, 56 | 同 and 公 are quoted as `"same, equal,"` and `"public, official,"` (they read `"same,equal,"` and `"public,official,"`). The exclusion list in line 56 is unchanged. |
| 吐 | 48, 49 | 気 and 社 are quoted as `"spirit, air,"` and `"company, shrine,"` (they read `"spirit,air,"` and `"company,shrine,"`). |
| 呂 | 52 | 品 is quoted as `"goods, refinement,"` (it read `"goods,refinement,"`). |
| 哲 | 55 | 理 is quoted as `"reason, logic,"` (it read `"reason,logic,"`). |
| 善 | 58 | 正 is quoted as `"correct, proper,"` (it read `"correct,proper,"`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 17 kanji cards (the 15 new cards, 寧 and 敷) and 25 word articles: 0 errors, 4
  warnings, all on word articles whose Dictionary line cites no JMdict entry id (井戸, 但し, 吐き気, 風呂敷). The output is
  identical to the reviewed snapshot's (the original packet's `mechanical-checks.md` lines 5-11); this revision touched
  no word article.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage pilot).
  `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine; the original packet's `mechanical-checks.md` line 211), so there is no
  `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether the
  gloss quoted after the link equals that title.
- `quiz-safety.txt`, `reading-options.txt` and `reading-exposure.txt`: no front matter changed, so the quiz options are
  unchanged. `quiz-safety.txt` is identical to the original packet's `evidence\audits\quiz-safety.txt`, and the other two
  differ from the same files there only in line 1 (the command line, which names the revision). In that line the
  interpreter is shown as `python -X utf8 utf8`; the doubled `utf8` is a typo in the author's label, present in the
  original packet as well, and the scripts ran normally.
  - `reading-exposure.txt` line 264: 0 production hits, 0 padded-session hits, 8 latent collisions; line 265: 0
    one-holder padded hits, 1 more for KANJIDIC2 name-only readings.
  - `reading-options.txt` line 231: 0 problems.
