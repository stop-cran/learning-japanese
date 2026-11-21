# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1154700, 1174680, 1312940, 1357210, 1372800, 1403830, 1431810, 1432410, 1512080, 1518280, 1518320, 1535010, 1542540, 1555830, 1555850, 1598830, 1603990, 1623650, 2083420, 2163190, 2866687) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiMeaningMetadata.kt`: how the app reads a kanji card's `quiz_exclusions`. Unchanged copy of the original packet's `evidence\app-code\KanjiMeaningMetadata.kt`.
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `e5c945d6`; line 1 is the command.
- `daijisen-aku.txt`: the Digital Daijisen headword block あ・く【飽く／×厭く／×倦く】 on the Weblio page for 飽く, including its senses and its [補説], which `飽.md:34` quotes. The header gives the URL, the retrieval time and the hash of the raw page. The spaces inside the extracted text are Weblio's link boundaries, and the final word 大阪弁 is the start of the next block on the page.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
