# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1446650, 1734790, 1734800, 2751570) cited for the 提 (提灯行列, 提灯持ち, 唐音) and 描 (すがき) revisions. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `weblio-chouchin.txt`: the Digital Daijisen headword ちょう‐ちん【▽提▽灯】 (labelled 唐音), extracted from Weblio; the text the 提 チョウ row (`提.md:40`) relies on.
- `weblio-saigu.txt`: the Digital Daijisen headword いつき‐の‐みや【▽斎宮】, extracted from Weblio; the text the 斎宮 sentence (`斎.md:32`) relies on.
- `stroke-types.txt`: KanjiVG stroke types of the repository files `strokes\揺.json` and `strokes\缶.json`; the support for the 缶-shape wording in `揺.md:31,60`.
- `word-remarks.json`: the declared old-to-new remark edits in existing word articles that `checks\linkplan.txt` allows besides the added kanji links. It is `[]`, as at the freeze.
- `kanji-remarks.json`: the declared old-to-new remark edit in the existing card `kanji\仮.md` that `checks\kanji-remarks.txt` allows. Unchanged from the freeze.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `3a0399bd`; line 1 is the command. It states that no word the script checks lacks its JMdict entry in the Metadata line.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
