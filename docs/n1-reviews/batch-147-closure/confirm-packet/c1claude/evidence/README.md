# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (none) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `kanji-remarks.json`: the declared old-to-new remark edits in the three existing kanji cards the batch modifies (the first three kanji in `checks\kanji-remarks.txt`). Unchanged from the freeze.
- `word-remarks.json`: the declared remark edits in the three word articles that carry one (the other 15 word diffs are link-wraps). Unchanged from the freeze.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `99487bb5`; line 1 is the command.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
