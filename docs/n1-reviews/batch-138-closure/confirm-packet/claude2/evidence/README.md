# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (2714430) for 契丹, named on the changed line `契.md:43` (契闊, the word whose reading changed, has no JMdict entry). Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `extras-merge-fix.txt`: the author's account of the defect in the reading audits of the earlier packets (some extra readings for 垂, 執, 壊, 奏 and 奪 were left out), the fix, the readings that were left out and what the corrected audits show.
- `reading-exposure-b6020f9e.txt`: the corrected reading-exposure audit run on the reviewed snapshot `b6020f9e`; line 1 is the command. Apart from line 1 it is the same as `checks\reading-exposure.txt`.
- `reading-options-b6020f9e.txt`: the corrected reading-options audit run on the reviewed snapshot `b6020f9e`; line 1 is the command. Apart from line 1 it is the same as `checks\reading-options.txt`.
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `kanjipedia-契.txt`: the Kanjipedia character entry for 契 (cited on `契.md:43`), the same file as in the earlier confirmation packet. It shows 契闊(ケッカツ) in the reading list.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `3158b2b9`; line 1 is the command. Line 4 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 6-31 list the words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
