# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1512850, 1524750, 2175880, 2859605) cited for the 弁 (弁護士), 径 (小径), 幣 (銭 ぜに) and 幕 (sense 4 "end; close") revisions. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `KanjiReadings.kt`: the app's reading-quiz builder (`KanjiReadingQuiz`): curated `distractors` first, one usable reading each, then the closeness-tiered fallback. Unchanged copy of the original packet's `evidence\app-code\KanjiReadings.kt`.
- `Words.kt`: `ReadingOptions.mutations`, the sound-change variants added to a target's excluded readings. Unchanged copy of the original packet's `evidence\app-code\Words.kt`.
- `雨.json`: the repository's stroke data for 雨 (`strokes\雨.json`, identical at both snapshots; KanjiVG revision 70a0b7ae, stated in the file). Coordinates are in a 109 by 109 box. Stroke 4 runs from (52.2, 23.5), just under the top bar (stroke 1), down to (53.5, 87.3), through the middle of the frame drawn by strokes 2 and 3; it supports `幣.md:53`.
- `superseded-775debde.txt`: the 幣 block and summary lines of `reading-exposure.txt` for `775debde`, an earlier local version of this fix with the 幣 distractors `[常, 帯, 希]`, never reviewed or published. Its header says how that version differs from `1b24a5f9`. It shows the Starter-session `PAD-HIT` (まい) that the final distractors avoid.
- `meta-scan.txt`: output of `meta_scan.py` on the 15 cards at `1b24a5f9`; line 1 is the command. Line 4 says that no word the script checks lacks its JMdict entry in the Metadata line. Lines 6-29 list the 24 words found only inside a longer word, which the script reports but does not count.
- `meta_scan.py`: the author's script that produced `meta-scan.txt`; its docstring states what it checks. It needs the author's JMdict index module (n1lib), which is not included, so it is here to be read, not run.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 15 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
