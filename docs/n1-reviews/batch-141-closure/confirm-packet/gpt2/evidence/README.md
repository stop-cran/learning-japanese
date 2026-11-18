# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1257720, 1601650) cited for the 抽 (抽出し, 抽き出し, 抽斗) and 懸 (懸念 けんねん) revisions. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `kanjidic2-斗.xml`: the complete record for 斗 from the pinned KANJIDIC2 input named below, cited for the 抽斗 sentence on `抽.md:36`. Its readings: ja_on ト and トウ, no ja_kun reading, nanori ます.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `094a1649`; line 1 is the command. Apart from line 1 it differs from the earlier confirmation packet's `evidence\meta-scan.txt` only in the line number of the 抽出し part-of-run line (34, was 36).
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
