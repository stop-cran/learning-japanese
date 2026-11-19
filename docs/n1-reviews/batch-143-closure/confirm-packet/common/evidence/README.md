# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1298460, 1310520, 1356870, 1508290, 1508300, 1634480, 1882040, 2583650) cited for the 旨 (うまみ, 旨味), 桜 (桜ん坊), 株 (守株), 染 (愛染), 柄 (え, がら), 暑 (蒸し暑い) and 旦 (旦つく) revisions. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `weblio-dantsuku.txt`: the Digital Daijisen headword だん‐つく【旦つく】, extracted from Weblio; the text the 旦 ダン row (`旦.md:34`) relies on for `a slighting word`.
- `joyo-item6.txt`: item 6 of the Joyo table's 表の見方 (parenthesised forms are the traditional Kangxi-dictionary forms), quoted from the Agency for Cultural Affairs pages; the support for `既.md:38` and `朗.md:43`.
- `word-remarks.json`: the declared old-to-new remark edit in the existing word article 西暦 that `checks\linkplan.txt` allows besides the added kanji links. Unchanged from the freeze.
- `kanji-remarks.json`: the declared old-to-new remark edits in existing kanji cards that `checks\kanji-remarks.txt` allows. It is `[]`, as at the freeze.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `9b8f50a8`; line 1 is the command.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
