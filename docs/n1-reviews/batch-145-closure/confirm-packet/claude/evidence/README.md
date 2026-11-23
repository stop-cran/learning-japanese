# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1147940, 1177090, 1177140, 1262040, 1433700, 1520360, 2861111) cited for the revised cards: 1147940 (roman, the ateji spelling of the 漫 card), 1433700 (tsukemono), 1262040 (gensen), 1520360 (bousai), 2861111 (nasu), 1177140 (enten) and 1177090 (ensho). Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `word-remarks.json`: the declared old-to-new remark edit in the existing word article 湧く that `checks\linkplan.txt` allows besides the added kanji links. New in this revision.
- `kanji-remarks.json`: the declared old-to-new remark edits in the two existing kanji cards the batch modifies (listed in `checks\kanji-remarks.txt`). The 暑 new text is revised; the 渋 edit is unchanged from the freeze.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `e07ab312`; line 1 is the command.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
