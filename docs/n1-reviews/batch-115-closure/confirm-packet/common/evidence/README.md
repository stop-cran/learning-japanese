# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1152510, 1244680, 1343640, 1633990) cited by the revised text (1152510 悪魔, 1633990 魔) or through its new word links and the author's statement (1244680 苦労, 1343640 署名). Pinned input
  `n1-implementation-JMdict_e.gz` (sha256 2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `word-苦労.md`: the word article `words\苦労.md` linked from `厄.md:59`; byte-identical at the revised snapshot, the reviewed snapshot and the base c7a7c8a7.
- `word-署名.md`: the word article `words\署名.md` linked from `票.md:57`; byte-identical at the revised snapshot, the reviewed snapshot and the base c7a7c8a7.
- `lint-rerun-f36cd819.txt`: the batch lint (`lean\n1_batch_tool.py lint`, base c7a7c8a7) rerun at the reviewed snapshot f36cd819; byte-identical to `checks\lint.txt` (revised snapshot).
- `lint-warning-basis.txt`: the wrapped `Dictionary:` lines behind the four lint warnings, with the JMdict entry id on each continuation line.
- Pinned KANJIDIC2 input: `n1-planning-kanjidic2.xml.gz` (sha256 af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed). The 8 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`).
