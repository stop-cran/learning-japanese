# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1238920, 1253840, 1448890, 1623580, 1642670, 2537870, 2672330, 2829360) cited for the 仰 (仰山), 丁 (仕丁 つかえのよほろ), 卸 (卸下) and 傑 (傑作) revisions, 何の変哲もない for the 哲 response, and 当て字, 唯々 and 諾々 for the 呂 and 唯 Metadata entries. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `weblio-卸-daijisen.txt`: the only Digital Daijisen block on the Weblio page for 卸 (headword おろし【卸（し）】), verbatim HTML and flattened text, with the page URL, retrieval time and the sha256 of the author's cached raw HTML, and why the original packet's `weblio-卸.txt` and `daijisen-heads.txt` do not show it.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `48332d32`; line 1 is the command. Line 2 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 4-27 list the words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
