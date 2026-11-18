# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1191680, 1251110, 1340820, 1433030, 1694880, 2096040, 2216510, 2230740, 2836096, 2842102) cited for the 嫁 (Kansai "wife"), 嬢 (お嬢様, 嬢ちゃん, 嬢さん), 宣 (宣う, 述べる/宣べる, 宣べ伝える) and 峠 (通る, 経る) revisions. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `extras-correction.txt`: the correction to the reading audits' `--extra` input (宗 たっとぶ and 宣 のる added), with every line of `checks\reading-exposure.txt` and `checks\reading-options.txt` that differs from the original packet's `evidence\audits\` files.
- `weblio-岬-character.txt`: the Digital Daijisen character entry for 岬 on its Weblio page, flattened, with the page URL, retrieval time and the sha256 of the raw HTML. It also holds the word entries みさき and さき that follow it on the page. Re-extracted because the first Daijisen block on that page is a word entry; it supports `岬.md:23` and `:25`.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `3b6f9727`; line 1 is the command. Line 4 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 6-39 list the 34 words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- `word-remarks.json`: the declared old-to-new remark edits in word articles that `checks\linkplan.txt` verifies, in addition to the link wrapping. Only the 宴会 entry differs from the original packet's `evidence\audits\word-remarks.json`: its old and new text now also cover line 32, the reworded closing of the character note.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
