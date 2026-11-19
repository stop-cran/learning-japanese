# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1418470, 1551120, 2844081) cited for the revised cards: 1551120 (rikuhou, continental shelf; the hou row of the tana card), 2844081 (obashima; the ran card) and 1418470 (awayuki; the awai card). Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `word-remarks.json`: the declared old-to-new remark edit in the existing word article for the word tokushu that `checks\linkplan.txt` allows besides the added kanji links. Unchanged from the freeze.
- `kanji-remarks.json`: the declared old-to-new remark edit in the one existing kanji card the batch modifies (listed in `checks\kanji-remarks.txt`) that `checks\kanji-remarks.txt` allows. The new text is the revised bullet; the old text is unchanged from the freeze.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `8db07f74`; line 1 is the command.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
