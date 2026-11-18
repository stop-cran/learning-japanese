# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1257720, 1601650) cited for the 抽 (抽斗, 抽出し, 抽き出し) and 懸 (懸念 けんねん) revisions. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `word-remarks.json`: the declared old-to-new remark edits in existing word articles that `checks\linkplan.txt` allows besides the added kanji links. It was `[]` at the freeze; it now declares the two deleted sentences in `words\悔しい.md` and `words\悔やむ.md`.
- `kanji-remarks.json`: the declared old-to-new remark edit in the existing card `kanji\張.md` that `checks\kanji-remarks.txt` allows. The `new` text now also names 拡 in 拡張.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `65b47299`; line 1 is the command. Line 4 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 6-35 list the 30 words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
