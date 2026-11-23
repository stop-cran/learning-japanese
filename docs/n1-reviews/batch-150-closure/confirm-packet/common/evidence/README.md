# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1175380, 1204570, 1204580, 1204640, 1204650, 1207730, 1232680, 1232830, 1245370, 1259290, 1260190, 1270760, 1278350, 1295940, 1296050, 1296120, 1296200, 1308190, 1318940, 1336260, 1351510, 1351560, 1365990, 1371120, 1371170, 1409480, 1440660, 1454080, 1456890, 1530020, 1547600, 1547660, 1547670, 1588340, 1595680, 1597030, 1603990, 1662320, 2245190, 2611890) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `7e3c101b`; line 1 is the command.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
