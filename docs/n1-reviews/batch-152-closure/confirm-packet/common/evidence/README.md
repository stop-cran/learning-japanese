# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1177680, 1180470, 1272940, 1367140, 1372620, 1383040, 1416550, 1419400, 1429620, 1450270, 1475720, 1583260, 1600270, 1600620, 1753470) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `kanjidic2-records-b81299f3.xml`: KANJIDIC2 records from the same pinned input, extracted for the revised snapshot. Besides the 15 batch kanji it includes the cards the revision newly excludes or compares (for example 華, 艶, 弾, 執, 脱), which the original packet's `evidence\kanjidic2-records.xml` lacks in part.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `b81299f3`; line 1 is the command.
- `o6-daijisen-names.txt`: `reading_exposure.py` at `b81299f3` on 載 迫 郷 輩 較 趣, with each card's `--extra` list from `checks\reading-exposure.txt` plus the Digital Daijisen name readings that the initial Claude review listed (its Optional item 6); lines 1-2 give the command and the added readings.
- `compound-sound-changes.md`: the repository article `articles/compound-sound-changes.md` that `載.md:42`, `輩.md:31` and `遣.md:38` link, copied unchanged from `b81299f3` (git blob `6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`, the same at `cdd8fd01`).
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
