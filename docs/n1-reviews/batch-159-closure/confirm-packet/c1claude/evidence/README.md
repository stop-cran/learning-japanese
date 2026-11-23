# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1205900, 1211850, 1243390, 1269190, 1274820, 1280390, 1280450, 1312350, 1316390, 1345470, 1410410, 1442420, 1470320, 1474270, 1502850, 1524930, 1524990, 1525120, 1549700, 1555420, 1584370, 1607070, 1607100, 1783060, 1787360, 2012430, 2014540, 2025400, 2177070, 2261490, 2261500) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `joyo\p<N>.txt`: text extracted with pdfplumber from page N of the official Joyo kanji table (2010, MEXT),
  `https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf#page=N` (PDF file sha256 d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42). The extraction is a convenience; verify against the PDF when it matters.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `word-quiz.txt`: the word-quiz audit regenerated at the revised snapshot (option sets, exclusions and reverse pairs for the nine new words). It names the app code `evidence\app-code\Words.kt`; here it is `Words.kt`.
- `distractor-use.tsv`, `distractor-senses.txt`, `corpus-attested.txt` and `meta-scan.txt`: the distractor and metadata audits, regenerated at the revised snapshot.
- `support-selection.json`: the selection statement and every support mapping in the ledger at the revised snapshot.
- `rule-7058679348.md`: the text of issue #60 comment 7058679348, the rule that governs support-word selection.
- `Words.kt`: the app's word-quiz code (how word `quiz_exclusions` and option scoring are used).
- `verify-commit.txt`: `git verify-commit -v` for the reviewed snapshot and the revision commit, with their parent lines, and `git log --show-signature` for the batch range.
- `selection-order.tsv`: the frozen source rows 1-153 (`docs\n1-sources\source-index.json`) with KANJIDIC2 grade, Joyo or name-use class, whether a card exists at the batch base 2787e43b, and membership in this batch.
- `daijisen-kotobank.json`: the Digital Daijisen (デジタル大辞泉, Shogakukan) sections cited by the revision, from kotobank.jp, fetched 2026-11-23: the text between each section heading and its 出典 line, tags stripped, keyed by headword with the canonical kotobank URL.
- `jmdict-scan-c1.txt`: a scan of the pinned JMdict: every entry read ついず or ついで, and every entry with a spelling containing 又, 叔, 叙, 后 or 吏, with priority tags, spelling marks and reading restrictions.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
