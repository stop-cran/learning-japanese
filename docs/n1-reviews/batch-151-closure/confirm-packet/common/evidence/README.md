# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1155780, 1211120, 1213870, 1223520, 1223530, 1223580, 1229120, 1260190, 1260210, 1260240, 1266440, 1268260, 1271510, 1271590, 1282400, 1282410, 1285490, 1285520, 1285560, 1285580, 1285680, 1327100, 1327120, 1348560, 1357030, 1357040, 1357050, 1365210, 1371170, 1381210, 1381260, 1412880, 1414680, 1431900, 1450030, 1450070, 1450970, 1468630, 1470070, 1496780, 1505380, 1513530, 1538130, 1541900, 1542040, 1568160, 1598620, 1598640, 1603220, 1604560, 1629710, 1640960, 1872960, 1907230, 1928100, 2008000, 2080860, 2794210, 2832734, 2845049) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `kanjivg\<hex>.svg`: KanjiVG records at the pinned revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc
  (`https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/<hex>.svg`). They show component structure and the `kvg:original` and `kvg:variant` attributes.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `15441514`; line 1 is the command.
- `distractor-trials.txt`: eleven trial distractor sets for 譲 at `15441514`. Each trial swaps only the `distractors:` line, runs `quiz_safety.py` and `reading_exposure.py` (same `--extra` list as `checks\reading-exposure.txt`) and restores the file; the header explains the expected "not mentioned in Notes" errors.
- `compound-sound-changes.md`: the repository article `articles/compound-sound-changes.md` that `貢.md:32` links, copied unchanged from `15441514` (git blob `6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`, the same at `b624890f`).
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
