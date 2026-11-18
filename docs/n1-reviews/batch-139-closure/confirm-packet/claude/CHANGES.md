# Batch 139 revision: what changed from a47efe9a to 3b6f9727

Revised snapshot: `3b6f972767928e01261440466899f32df398d7f1`. It is reached from the reviewed snapshot
`a47efe9af926316eaa86656033bf6e109f2be697` by one commit. Nothing is published.

- Four of the 15 kanji cards changed: 嫁, 嬢, 宣 and 峠. The other eleven (宗, 宜, 宴, 寂, 密, 審, 尋, 屈, 属, 岬, 崩)
  are unchanged. One of the 20 word articles the batch edits changed, 宴会, in one line, as one reviewer suggested. The 15 stroke files
  and the other 19 word articles are unchanged; each of those 34 files still differs from the published text exactly as
  in the reviewed snapshot.
- Front matter: only `quiz_exclusions` of 峠 changed, from `[頂, 山, 旬, 通, 経]` to `[頂, 山, 旬]`. Titles, tags,
  metadata readings and every `distractors` list are unchanged. Neither 通 nor 経 has a `quiz_exclusions` list, so
  after this change the pairs 峠–通 and 峠–経 are excluded by neither side (the app excludes a pair when either card
  lists the other, `evidence\QuizBuilder.kt` line 26). `checks\quiz-safety.txt` is identical, line for line, to the
  original packet's `evidence\audits\quiz-safety.txt`; 峠's three curated distractors (岸, 島, 上) still fill all three
  wrong slots of its meaning question.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` and `snapshot\words\宴会.md` in this packet (the revised
  snapshot). 嬢 and 峠 each gained one
  line (a new Notes bullet at 嬢 line 47 and 峠 line 49), so their Metadata lines are now line 51 (line 50 in the
  reviewed snapshot). Every other line number is unchanged.
- `diffs\fix.patch` is the exact patch from `a47efe9a` to `3b6f9727`. `diffs\changed-lines.txt` lists the changed lines
  per file.
- Every link on a changed line and the title quoted after it are listed in `checks\link-targets.tsv`, with the target's
  real `title:`.
- The Metadata lines. The author's writing rule for these cards is that the Metadata line lists the JMdict entry of
  every word the card names. Each word newly named by this revision has its entry added (嬢 line 51, 宣 line 57, 峠 line
  51). `evidence\meta-scan.txt`, made by `evidence\meta_scan.py`, finds no word without its entry. The script checks
  every run of Japanese script that has at least two characters, contains a kanji and exactly matches a JMdict kanji
  spelling. It does not check words written only in kana, single-kanji words, or words that appear only inside a longer
  word; it lists these separately, 34 of them, one more than at the reviewed snapshot. Three are new: お嬢 inside お嬢様
  (嬢 line 47), and 伝え and 伝える inside 宣べ伝える (宣 line 31). Two are gone: 嬢さん inside お嬢さん (嬢 line 23)
  and inside 御嬢さん (嬢 line 46), because 嬢さん's two entries are now listed.
- One audit input was corrected; see "Reading audits" below and `evidence\extras-correction.txt`.
- New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file. All other
  evidence stays in the original packet.

| File | Changed lines | Change |
| --- | --- | --- |
| 嫁 | 23 | `its third sense is "wife."` now reads `its third sense, which JMdict marks as Kansai dialect, is "wife."` Support: `evidence\jmdict-cited-entries.xml`, entry 1191680 (嫁 よめ; sense 3 "wife" with `<dial>&ksb;</dial>`, Kansai-ben). |
| 嬢 | 47, 51 | Line 47 is a new Notes bullet: `Related forms in JMdict: お嬢様 おじょうさま, "(another's) daughter," marked polite language, and "young lady (of pampered upbringing)"; 嬢ちゃん じょうちゃん, "young girl; young lady"; and 嬢さん じょうさん, "(another's) daughter; young lady." 嬢さん read とうさん is a Kansai-dialect honorific, "daughter (of a good family)."` Line 51 (Metadata; line 50 before): entries 1694880, 2836096, 2230740 and 2216510 are added, and 1531190 moves before them. Support: `evidence\jmdict-cited-entries.xml`, entries 1694880 (お嬢様; polite language on sense 1 only), 2836096 (嬢ちゃん), 2230740 (嬢さん じょうさん) and 2216510 (嬢さん とうさん; honorific language, `<dial>&ksb;</dial>`). |
| 宣 | 31, 40, 57 | Line 31: `Of the kun readings in the character entry, only のたまう is a KANJIDIC2 reading.` now reads `The character entry gives the kun readings のべる, のる and のたまう; only のたまう is a KANJIDIC2 reading. JMdict has 宣べる only as a rarely used spelling of 述べる のべる, "to state; to express; to say"; its one word that writes のべ with 宣 as the main spelling is 宣べ伝える のべつたえる, "to proclaim (e.g. gospel)." JMdict has no entry writing のる with 宣.` Line 40, the のたま.う row: the parenthesis `(honorific; usually written in kana)` now ends `usually written in kana; JMdict notes it was originally respectful and is nowadays often used sarcastically)`. Line 57 (Metadata): entries 1340820 and 2096040 are added after 1430430. Support: the original packet's `evidence\public-source\weblio-宣.txt` line 6 (`［訓］のべる のる のたまう`); `evidence\jmdict-cited-entries.xml`, entries 2842102 (宣う; note `originally respectful language; nowadays oft. used sarcastically`), 1340820 (述べる; 宣べる tagged `rarely used kanji form`) and 2096040 (宣べ伝える). The claim that no JMdict entry writes のる with 宣 rests on the original packet's `evidence\jmdict-families.xml`, which holds every JMdict entry that writes any kanji of the batch (the original packet's `evidence\provenance.json`, the note at line 365). |
| 峠 | 14, 48, 49, 51 | Line 14: `quiz_exclusions: [頂, 山, 旬]` (通 and 経 removed). Line 48 no longer names 通 and 経 or the sense "pass": it now reads `[頂](頂.md), "summit; receive," [山](山.md), "mountain," and [旬](旬.md), "ten days; peak season," overlap the senses "peak" and "mountain" that 峠 and its word carry. … Do not treat "peak" as exclusive to any one character.` Line 49 is a new Notes bullet: `A mountain pass is 峠. Passing through a place is a different idea, expressed by verbs such as 通る とおる, to go by or through a place, and 経る へる, for time to pass or to go through a place. English "pass" covers both ideas, so [通](通.md), "pass through; commute," and [経](経.md), "pass through; sutra," remain ordinary wrong options for 峠.` Line 51 (Metadata; line 50 before): entries 1433030 and 1251110 are added, and 1896840 moves before them. Support: `evidence\jmdict-cited-entries.xml`, entries 1433030 (通る) and 1251110 (経る); `checks\link-targets.tsv` for the titles of 通 and 経. |
| 宴会 (word article) | 32 | `gathering. The first character specifies the kind of gathering:` now reads `gathering. The first character specifies the kind of gathering. The on readings are`; line 33, `エン + カイ.`, is unchanged. The batch had already edited this paragraph (it links 宴 and drops the sentence saying 宴 had no card); this revision changes only the colon. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on the 15 kanji cards and 20 word articles: 0 errors, 2 warnings, both on word articles
  whose Dictionary line cites no JMdict entry id (宣伝, 宴会). The same two warnings were reported at the reviewed
    snapshot (the original packet's `mechanical-checks.md` lines 7-9); this revision changed one line of 宴会's character
    note and no Dictionary line.
- `unittest.txt`: 436 tests, OK. `validate.txt`: 0 errors. `budget.txt`: the content budget script's size summary; it
  raised no budget error. `vocabulary.txt`: vocabulary coverage check passes (3201 of 3336 reviewed prompts, stage
  pilot). `manifest.txt`: `manifest.json` regenerated, rebuild idempotent, tracked tree clean.
- `linkplan.txt` and `kanji-remarks.txt`: the word-article link plan (20 changed word files, 20 added links, 4 declared
  remark edits, 0 problems) and the check that existing kanji cards are unchanged (0 modified, 0 problems). The declared
  remark edit for 宴会 now also covers the reworded line 32;   The remark declarations are in `evidence\word-remarks.json` (the original packet's
    `evidence\audits\word-remarks.json` had the old 宴会 entry); the other three are unchanged.
- The Android app's JVM tests that read the real content and the Kotlin reading-audit cross-check were not run for this
  revision either (no JDK on the authoring machine), so there is no `jvm.txt`.
- `link-targets.tsv`: every link on a changed line, with the existence of its target, the target's `title:` and whether
  the gloss quoted after the link equals that title.
- `quiz-safety.txt` matches the original packet's `evidence\audits\quiz-safety.txt` line for line.

### Reading audits

`reading-exposure.txt` and `reading-options.txt` were rerun with a corrected input. The original packet says their
`--extra` readings include every kun reading in the Digital Daijisen character entries, but two were missing at the
freeze: 宗 たっとぶ and 宣 のる. Both are now included. `evidence\extras-correction.txt` lists every line that differs
from the original packet's `evidence\audits\` files; apart from line 1 (the command), the only differences are the two
readings appearing in the 宗 and 宣 "unlisted readings attested" lines and the 宣 unlisted-reading count going from 10 to
11. No count of hits or collisions changed.

- `reading-exposure.txt` line 267: 0 production hits, 0 padded-session hits, 11 latent collisions; line 268: 0
  one-holder padded hits, 0 more for KANJIDIC2 name-only readings.
- `reading-options.txt` line 227: 1 problem, the HIT label at line 196 (岬 さき, offered by 先). This tool does not model
  curated slots that are already filled; `reading-exposure.txt`, which models the actual pools, finds さき not drawable.
