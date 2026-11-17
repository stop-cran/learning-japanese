# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (2265620) cited for the revised 彫 card (彫り, also written 彫: ほり and the out-dated kana えり). Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `kanjivg\<hex>.svg`: KanjiVG records at the pinned revision 70a0b7ae0c18ceb5cb358274b029cce0234a43bc
  (`https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/<hex>.svg`). They show component structure and the `kvg:original` and `kvg:variant` attributes.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings.
- `daijisen-彫る.txt`: Digital Daijisen extract (Weblio) for 彫る, cited on the revised 彫 card: the headword え・る〔ゑる〕【▽彫る】 (line 7) and the headword ほ・る【彫る】 (line 9).
- `kanjipedia-outside-readings.json`: for all 15 batch kanji, the Kanjipedia on and kun readings and the ones marked [外]; with 彫=え.る, these are the `--extra` readings of `checks\reading-exposure.txt` and `checks\reading-options.txt`.
- `reading-exposure-2ef25d33.txt`: for comparison only, the same reading-exposure audit (same tool, same `--extra` readings) run on the earlier revision `2ef25d33`. Only the 巡 and 彫 blocks, the commit named on line 1 and line 400 differ from `checks\reading-exposure.txt`.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
