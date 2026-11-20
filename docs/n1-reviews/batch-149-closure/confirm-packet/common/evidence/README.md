# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1177680, 1177690, 1177700, 1177720, 1197720, 1213470, 1303190, 1364370, 1402100, 1432200, 1432710, 1450070, 1451580, 1497770, 1497780, 1497800, 1497810, 1497820, 1497870, 1505630, 1528440, 1528470, 1533740, 1555640, 1559210, 1600990, 1616390, 2249290, 2519020, 2573230, 2682080, 2708210, 2832743, 2833260) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `word-remarks.json`: the declared old-to-new remark edits in the two word articles the revision changes (`words\艶.md` and `words\芝居.md`). `checks\linkplan.txt` verifies the word articles against it.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `06b2db87`; line 1 is the command.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
