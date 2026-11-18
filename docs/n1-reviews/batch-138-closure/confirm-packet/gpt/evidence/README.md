# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1204780, 1257110, 1319610, 1416340, 1509290, 1590410, 2080870, 2714430) cited for the 堅 (かたい spellings), 契 (契丹), 執 (執り行う) and 奏 (功を奏する) revisions and for the three new quiz exclusions 垣–壁, 奪–魅 and 塊–組. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `kanjipedia-契.txt`: the Kanjipedia character entry for 契 (cited on `契.md:43`): its reading list as raw HTML and flattened, the meanings section, the formation note and the list of words, with the page URL, retrieval time and the sha256 of the author's cached page, and a count of the occurrences of セツ.
- `weblio-押妨.txt`: the two dictionary entries for 押妨 on its Weblio page (Digital Daijisen and a dictionary of historical terms), flattened, with the page URL, retrieval date and sha256, for the gloss on `妨.md:25`. 押妨 has no JMdict entry.
- `stroke-summaries.txt`: per-stroke type, end points and extents of 威, 壊 and 衣, read from the repository stroke files by a short script, for the 威 and 壊 mnemonics (`威.md:33`, `壊.md:27`).
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `acf7297e`; line 1 is the command. Line 4 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 6-31 list the words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
