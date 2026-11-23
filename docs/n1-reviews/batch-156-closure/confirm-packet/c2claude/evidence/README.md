# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1182940, 1280080, 1280090, 1291070, 1410080, 1423430, 1424550, 1578730, 1595120, 1874770, 2124490) cited by the changed text of 甲乙, `CHANGES.md` or `RESPONSE.md`: the entries for 甲乙 and the longer words containing it, for 甲 and 乙, and for the words 中心, 中央, 芯, 差 and 対照 named in `RESPONSE.md` P2 and P3. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `甲乙-daijisen.txt`: text of the Digital Daijisen entries on the Weblio page for 甲乙, with the source URL, retrieval time and raw-HTML sha256 at the top. The same file as in the earlier confirmation packet.
- `kouotsu-scan.txt`: scan of the pinned `JMdict_e.gz` for entries whose written form is or contains 甲乙, entries read こうおつ, and entries read かるめる; made by `kouotsu_scan.py`. Line 3 gives the sha256 of the scanned file.
- `kouotsu_scan.py`: the script that made `kouotsu-scan.txt`. It needs the author's JMdict path module (n1lib), which is not included, so it is here to be read, not run.
- `word-quiz.txt`: the word-quiz option audit at `3c5ef845` for the ten batch words; line 2 is the command. Byte-identical to the earlier confirmation packet's `evidence\word-quiz.txt`.
- `compound-sound-changes.md`: unchanged copy of `articles/compound-sound-changes.md` (identical at `c6afa163`, `395f5364` and `3c5ef845`), for `RESPONSE.md` P1.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
