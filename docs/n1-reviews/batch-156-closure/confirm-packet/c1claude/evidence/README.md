# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1002570, 1039110, 1075090, 1149820, 1149930, 1182940, 1182945, 1182970, 1184140, 1225090, 1253190, 1264770, 1268820, 1269720, 1280080, 1282860, 1357390, 1366770, 1369070, 1369530, 1369620, 1387170, 1393090, 1417780, 1424550, 1466670, 1472680, 1478430, 1497610, 1525250, 1539620, 1576860, 1577915, 1578730, 1583850, 1595120, 1622940, 1778760, 1874770, 2036160, 2124490, 2232330, 2270390, 2397580, 2414470, 2837087, 2855480) cited by the changed text, `CHANGES.md`, `RESPONSE.md` or `distractor-senses.txt`, or for words the changed text names without an entry number; it also holds the eight entries that one initial review did not check against the pinned JMdict, which `CHANGES.md` (process note "JMdict entries") lists. Every other entry that a batch kanji card or batch word article cites is in the original packet's `evidence\jmdict-families.xml`. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `compound-sound-changes.md`: unchanged copy of `articles/compound-sound-changes.md` (identical at `c6afa163` and `395f5364`), the article that `伐.md:31`, `words\亜熱帯.md:29`, `潜.md:57` and `words\伐採.md:28` link to. Lines 26-49 are "Small っ: gemination in a compound"; lines 51-63 are "Small っ plus /p/".
- `輩.md`: unchanged copy of the published batch-152 card `kanji/輩.md` (identical at `cdd8fd01`, `c6afa163` and `395f5364`). Line 31 links the compound-sound-changes article for ぱい in 先輩 せんぱい.
- `甲乙-daijisen.txt`: text of the Digital Daijisen entries on the Weblio page for 甲乙, with the source URL, retrieval time and raw-HTML sha256 at the top.
- `word-quiz.txt`: the word-quiz option audit at `395f5364` for the ten batch words (丹念 甲乙 亜熱帯 仁 仙人 歌舞伎 降伏 伐採 伯仲 同伴), made by the same tool as the original packet's `evidence\audits\word-quiz.txt`; line 2 is the command.
- `meta-scan.txt`: output of `meta_scan.py` on the ten cards at `395f5364`; line 1 is the command.
- `corpus-attested.txt`: every word article whose reading quiz can offer, as a wrong option, a reading that JMdict gives for the word's written form, at `395f5364`; made by `gen_corpus_attested.py`.
- `gen_corpus_attested.py`: the script that made `corpus-attested.txt`.
- `distractor-senses.txt`: for every new and rejected curated distractor, the JMdict entries spelled with that character alone, with their senses.
- `distractor-use.tsv`: for each of the 17 distinct curated distractors in the six changed sets, its own front matter and every kanji card that lists it; then the batch cards' curated distractors at `2c206d8f` (the same at `395f5364`), and the replaced or rejected candidates; made by `gen_distractor_use.py`.
- `gen_distractor_use.py`: the script that made `distractor-use.tsv`.
- `wazaogi-scan.txt`: scan of the pinned `JMdict_e.gz` for entries read わざおぎ or with a reading starting わざお, and for entries spelled 伎 alone; made by `wazaogi_scan.py`.
- `wazaogi_scan.py`: the script that made `wazaogi-scan.txt`.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
