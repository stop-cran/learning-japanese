# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1198600, 1216120, 1216130, 1324260, 1333820, 1486430, 1633480) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `3f8b951d`; line 1 is the command.
- `daijisen-joo.txt`: the two Digital Daijisen じょう entries on the Weblio page for 錠, including the headword じょう〔ヂヤウ｜ジヤウ〕【錠／▽鎖／×鏁】, its sense 1 and its [補説], which `鎖.md:43` cites. The header gives the URL and fetch time.
- `daijisen-heads.txt`: the Digital Daijisen headword list for the 15 kanji, regenerated with the fixed parser; it replaces the original packet's `evidence\daijisen-heads.txt` as the source of the audit `--extra` lists.
- `daijisen-heads-diff.txt`: the old and the fixed headword pattern, a unified diff of the original packet's headword list against the regenerated one, and the resulting change in the audit `--extra` lists (鎖 gains じょう).
- `retro-check-yoh.txt`: `reading_exposure.py` at `3f8b951d` on 益 with `--extra 益=よう`, the one reading not already on a card that the fixed parser recovers from the headword lists of batches 144 to 152; lines 1-3 give the context and the command.
- `joo-holders.txt`: at `3f8b951d`, the cards that offer じょう as an on or a kun quiz reading, by the audit's own card model, and 鎖's reading prompts; it shows why `checks\reading-exposure.txt` lists じょう as attested for 鎖 without a collision line.
- `compound-sound-changes.md`: the repository article `articles/compound-sound-changes.md` that `酢.md:40` links, copied unchanged from `3f8b951d` (git blob `6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`, the same at `cdab83b3`).
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
