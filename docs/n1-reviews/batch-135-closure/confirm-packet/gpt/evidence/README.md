# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1182750, 1182790, 1589020) cited for the 憶 revision (憶説/臆説, 臆病/憶病 and 憶測/臆測). Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `kanjivg\<hex>.svg`: KanjiVG records at the pinned revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc
  (`https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/<hex>.svg`). They show component structure and the `kvg:original` and `kvg:variant` attributes.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings.
- `kanjipedia-救.txt`, `kanjipedia-巡.txt`: the reading lists of the Kanjipedia character entries cited on the revised 救 and 巡 cards; [外] marks readings outside the official table.
- `kanjipedia-outside-readings.json`: for all 15 batch kanji, the Kanjipedia on and kun readings and the ones marked [外]; these are the `--extra` readings of `checks\reading-exposure.txt` and `checks\reading-options.txt`.
- `reading-exposure-163b384e.txt`: for comparison only, the reading-exposure audit run on the reviewed snapshot `163b384e` with the same `--extra` readings as `checks\reading-exposure.txt`. Only the 巡 and 救 blocks and the summary line differ from the revised-snapshot audit.
- `daijisen-草.txt`, `daijisen-草履.txt`: Digital Daijisen extracts (Weblio) for 草 (historical kana サウ of ソウ) and 草履 (headword ぞう‐り〔ザウ‐〕), cited on the revised 履 card.
- `kanjidic2-甫.xml`: the KANJIDIC2 record for 甫 (7 strokes) from the pinned input below, for the revised 博 mnemonic.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
