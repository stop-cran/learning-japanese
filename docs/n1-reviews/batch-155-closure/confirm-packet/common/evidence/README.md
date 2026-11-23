# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1177680, 1183240, 1186230, 1252570, 1267540, 1267560, 1267600, 1267900, 1268000, 1268020, 1270650, 1273050, 1291480, 1291490, 1291500, 1341780, 1341810, 1350020, 1408280, 1415850, 1415870, 1426180, 1436950, 1448570, 1478190, 1482660, 1482670, 1482680, 1482700, 1482710, 1482720, 1482740, 1482820, 1572080, 1573150, 1593800, 1635870, 1672130, 1950140, 2230390, 2257170, 2270830, 2457840, 2714830, 2827211) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiMeaningMetadata.kt`: how the app reads a kanji card's `quiz_exclusions`. Unchanged copy of the original packet's `evidence\app-code\KanjiMeaningMetadata.kt`.
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`). Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `meta-scan.txt`: output of `meta_scan.py` on the six cards at `25609582`; line 1 is the command.
- `exclusion-proofs.md`: the line-23 meaning paragraph and the `## Notes` section of each of the six cards exactly as they were at `97c49eb2`, moved off the cards by the fix, with a closing section on the two exclusions the fix removes (卑/底 and 沙/漠). It will be filed with the batch's closure documents.
- `batch-149-closure-README.md`: unchanged copy of the published `docs/n1-reviews/batch-149-closure/README.md` (identical at `97c49eb2` and `25609582`). Line 111 records the batch-149 G4 fix that the Notes layout in this revision follows.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 6 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
