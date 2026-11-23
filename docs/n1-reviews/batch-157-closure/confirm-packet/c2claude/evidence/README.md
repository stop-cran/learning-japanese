# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1166100, 1171900, 1242590, 1242600, 1258330, 1260670, 1315840, 1323080, 1327190, 1344370, 1344930, 1344940, 1369620, 1374810, 1387000, 1394250, 1419990, 1442730, 1454080, 1454240, 1495370, 1497610, 1498620, 1499960, 1502390, 1522150, 1539980, 1555390, 1567650, 1578010, 1580640, 1582520, 1583390, 1592250, 1593605, 1709000, 2020680, 2216440, 2273940, 2742880, 2773260, 2839304, 2843485, 2860163) cited by the changed text, by `CHANGES.md` and `RESPONSE.md`, and for the new, replaced and rejected distractors. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `distractor-use.tsv`: every curated meaning distractor at the revised snapshot, with its own card's title, JLPT level, starter tag and readings, every card that lists it, and the batch cards that gained it after cd5d75d1; then the batch cards' sets against cd5d75d1, the replaced distractors and the rejected candidates with the author's reasons.
- `prior-distractor-use.tsv`: the same table at cd5d75d1.
- `distractor-senses.txt`: every JMdict entry spelled with the single distractor character, for each distractor in the revision, each distractor replaced since cd5d75d1 and each rejected candidate (sense numbers in JMdict order).
- `word-quiz.txt`: the word meaning-quiz candidates and the reverse pairs for the batch's word articles at the revised snapshot, as the app builds them.
- `prior-word-quiz.txt`: the same output at cd5d75d1.
- `corpus-attested.txt`: word reading-quiz options that are attested readings, across the whole word stack.
- `meta-scan.txt`: a check that every word a batch card names and JMdict spells with kanji has its entry on the card's Metadata line; parts of longer words are listed for information.
- `verify-commit.txt`: the signature of every commit from cd5d75d1 to the revised snapshot.
- `weblio-不倫.txt`: the Digital Daijisen entry for 不倫, retrieved from Weblio (carried over from the first confirmation round).
- `Words.kt`: the app's word-quiz builder (how word `quiz_exclusions` are used).
- `prior-reading-exposure.txt`: `checks\reading-exposure.txt` at cd5d75d1.
- `prior-reading-options.txt`: `checks\reading-options.txt` at cd5d75d1.
- `kanjidic2-卑.xml`: the KANJIDIC2 record for 卑 (not a batch card), copied verbatim from the repository's B155 closure evidence; `kanji\侮.md` cites its meaning “despise”.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
