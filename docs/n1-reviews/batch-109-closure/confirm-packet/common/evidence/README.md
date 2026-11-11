# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1250600, 1253590, 1253620, 1279170, 1298910, 1298950, 1383160, 1414580, 1523790, 1590145, 1592730, 1595910, 1951490, 1982610) cited by the revised text. Pinned input
  `n1-implementation-JMdict_e.gz` (sha256 2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `kanjivg\<hex>.svg`: KanjiVG records at the pinned revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc
  (`https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/<hex>.svg`). They show component structure and the `kvg:original` and `kvg:variant` attributes.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- Pinned KANJIDIC2 input: `n1-planning-kanjidic2.xml.gz` (sha256 af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
