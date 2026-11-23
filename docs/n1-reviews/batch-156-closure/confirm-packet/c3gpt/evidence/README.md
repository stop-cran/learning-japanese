# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1182940, 1182945, 1197500, 1280080, 1280090, 1280150, 1371750, 1387170, 1474240, 1474260, 1474280, 1601290, 1607070, 1607100, 1844500, 1862630, 1907280, 2164680, 2648950, 2837087, 2855480) cited by `RESPONSE.md`, `CHANGES.md`, `selection-evidence.md` or the new 乙種 article: the new word and the words its article and the 乙 card cite, and the candidate words for the 乙, 仙 and 伯 rows. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `merge-scope.txt`: git output for the merge `eafee44b`: its parents, the batch line up to the merge, every path the batch's own commits add, change or delete (merges of main excluded), the merge's diff restricted to those paths (empty), and the paths the merge brought in from main.
- `selection-evidence.md`: verbatim quotations of the word-selection rule (issue #60), JMdict's definitions of its priority tags, the Joyo table rows and the dictionary entries used for the 乙, 仙 and 伯 rows, each with its source.
- `candidates.md`: every pinned-JMdict entry with a tagged kanji form containing 乙, 仙 or 伯, with its tags, readings, the other kanji's cards and existing articles, generated at `ba44b280` by `cands.py` (which needs the author's JMdict path module, not included; it is here to be read).
- `word-quiz.txt`: the word-quiz option audit rerun at `ba44b280` for the ten batch words; line 2 is the command.
- `meta-scan-after.txt`: the Metadata-id scan (every whole run of Japanese script with a kanji named on a batch card, against the card's Metadata line) at `ba44b280`.
- `budget-at-merge.txt`: the author's size-budget run at the merge `eafee44b` (`retainedBytes` is the retained size).
- `link-scan.txt`: `git grep` of the whole revision `ba44b280` for links to the deleted articles `words/乙.md` and `words/甲乙.md` (plain and percent-encoded) and for every mention of 甲乙.
- `weblio-<word>.txt`: Digital Daijisen entries on Weblio (乙, 乙種, 乙種合格, 甲種, 丙種, 種), tags stripped, each headed by its URL, retrieval time and the raw page's sha256. Weblio pages change between fetches; check the live page.
- `kanjipedia-乙.txt`: the readings and meanings sections of Kanjipedia's 乙 page, with its URL and retrieval date. The other nine characters' Kanjipedia records are in the original packet's `evidence\kanjipedia-senses.txt`.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
