# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1042520, 1179810, 1179830, 1180030, 1257240, 1257320, 1260700, 1337560, 1337650, 1376240, 1376640, 1397300, 1397350, 1400840, 1428700, 1950420, 2856503, 2856504) cited by the revised text. Pinned input
  `n1-implementation-JMdict_e.gz` (sha256 2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `kanjivg\<hex>.svg`: KanjiVG records at the pinned revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc
  (`https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/<hex>.svg`). They show component structure and the `kvg:original` and `kvg:variant` attributes.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz option builder (KanjiReadingQuiz.question, excludedKeys, closeness), taken from the Android checkout at commit 10d98d0.
- `Words.kt`: the app's ReadingOptions (mutations, voicing map, closeness) used by the reading quiz, taken from the same checkout.
- `joyo-p33-utsuwa.png`: crop of the Joyo table page 33 (PDF page index 32) showing the 器 entry with its older form in round brackets. The text extract `joyo\p33.txt` prints that bracketed form as U+FA38 (CJK compatibility ideograph, which Unicode normalisation maps to the standard 器, U+5668), so the text alone does not show the shape; use the images or the PDF.
- `joyo-p33-utsuwa-pair.png`: the two glyphs of that entry enlarged side by side; left = the main entry (centre 大), right = the bracketed older form (centre with a dot, like 犬).
- Pinned KANJIDIC2 input: `n1-planning-kanjidic2.xml.gz` (sha256 af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
