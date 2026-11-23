# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (2216510, 2230740) for 嬢さん じょうさん, whose quoted glosses changed on `嬢.md:47`, and 嬢さん とうさん, quoted on the same line. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `f1b2bdb8`; line 1 is the command. Apart from line 1 it is identical to the earlier confirmation packet's `evidence\meta-scan.txt`.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
