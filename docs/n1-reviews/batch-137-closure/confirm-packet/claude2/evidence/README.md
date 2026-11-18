# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1448890, 1623580, 2672330, 2829360) cited for the JMdict ids added to the Metadata lines of 丁 (仕丁), 呂 (当て字) and 唯 (唯々 and 諾々). Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `48332d32`; line 1 is the command. Line 2 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 4-27 list the words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
