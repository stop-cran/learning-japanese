# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1149860, 1329130, 1369740, 1387150, 1862630, 2261500) added to the Metadata lines of 乙, 亜, 仁, 仙 and 伯 by this revision: 乙種, 亜麻, 仁術, 仙骨, 酒仙 and 伯母さん. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `merge-scope.txt`: git output showing the merge `e37ad00b` (its parents, every path the batch adds or changes since its base `0638544c`, the merge's diff restricted to those paths, which is empty, and the full list of the 102 paths the merge brought in from main).
- `meta-scan-before.txt`: the Metadata-id scan at the merge `e37ad00b` (batch text identical to `3c5ef845`): six whole-run gaps and four part-of-run matches.
- `meta-scan-after.txt`: the same scan at `a7cc61e2`: no whole-run gap; the same four part-of-run matches.
- `meta_scan.py`: the scan script, identical to the copy published in the repository's B137 closure (`docs/n1-reviews/batch-137-closure/confirm-packet/gpt/evidence/meta_scan.py`). It needs the author's JMdict path module (n1lib), which is not included, so it is here to be read, not run.
- `word-quiz.txt`: the word-quiz option audit rerun at `a7cc61e2` for the ten batch words; line 2 is the command. Byte-identical to your earlier confirmation packet's `evidence\word-quiz.txt`.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
