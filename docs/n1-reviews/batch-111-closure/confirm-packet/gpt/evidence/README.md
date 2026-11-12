# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1183910, 1215960, 1222840, 1225740, 1225810, 1225840, 1225900, 1225920, 1238550, 1238570, 1238590, 1260660, 1278260, 1291990, 1298070, 1303670, 1306030, 1316270, 1344160, 1356600, 1376910, 1386140, 1386150, 1386160, 1386230, 1386290, 1386350, 1419860, 1429240, 1454260, 1456020, 1483440, 1489990, 1490010, 1490070, 1490080, 1497020, 1497030, 1497040, 1497050, 1497060, 1500150, 1519300, 1519650, 1561830, 1577670, 1596460, 1605460, 1610060, 1613780, 1646450, 1646640, 1646710, 1674690, 1722060, 1722070, 1821400, 1870020, 2845184, 2862467) cited by the revised text. Pinned input
  `n1-implementation-JMdict_e.gz` (sha256 2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz option builder (KanjiReadingQuiz.question, excludedKeys, closeness), taken from the Android checkout at commit 10d98d0.
- `Words.kt`: the app's ReadingOptions (mutations, voicing map, closeness) used by the reading quiz, taken from the same checkout.
- `kanjidic2-judge.xml`: the pinned KANJIDIC2 record for 判 (on ハン and バン; kun わか.る), supplied because the original packet's `evidence\kanjidic2-records.xml` holds only the 15 batch kanji; 評判 is cited by the revised text of 評.md line 35.
- Pinned KANJIDIC2 input: `n1-planning-kanjidic2.xml.gz` (sha256 af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
