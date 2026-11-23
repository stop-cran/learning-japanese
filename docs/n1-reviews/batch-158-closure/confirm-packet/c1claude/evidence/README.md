# Evidence added for the confirmation round

- `jmdict-cited-entries.xml`: complete JMdict entries (1010130, 1156530, 1156680, 1163460, 1163470, 1170650, 1170790, 1182460, 1182490, 1214900, 1224340, 1224350, 1224390, 1224580, 1226610, 1226620, 1232060, 1232670, 1247200, 1247240, 1258330, 1260000, 1260770, 1286390, 1291410, 1292070, 1292080, 1292110, 1308900, 1321470, 1322880, 1323940, 1328680, 1331530, 1331540, 1344810, 1346260, 1346290, 1351910, 1363520, 1403830, 1404090, 1404100, 1404110, 1404180, 1404210, 1404240, 1411260, 1411360, 1454460, 1454470, 1473980, 1484150, 1498080, 1510320, 1510330, 1510370, 1510380, 1512130, 1512180, 1517130, 1518800, 1518810, 1518840, 1518940, 1519260, 1531680, 1533700, 1556870, 1562560, 1577800, 1581960, 1584140, 1590240, 1590420, 1590440, 1592060, 1595084, 1611480, 1643130, 1654590, 1706800, 1710750, 2248100, 2411570, 2867582) cited by the revised text. Pinned input
  `JMdict_e.gz` (sha256 42bd8fbc917bc039a1d4f4da0e75a1f5e03ba342b51b51ddc89a95f713ca6cec). Today's online JMdict may differ slightly.
- `QuizBuilder.kt`: the app's answer-option builder (how `distractors` and `quiz_exclusions` are used).
- `word-quiz.txt`: the word-quiz audit regenerated at the revised snapshot (option sets, exclusions and reverse pairs for the ten new words). It names the app code `evidence\app-code\Words.kt`; here it is `Words.kt`.
- `distractor-use.tsv`, `distractor-senses.txt`, `corpus-attested.txt` and `meta-scan.txt`: the distractor and metadata audits, regenerated at the revised snapshot.
- `support-selection.json`: the selection statement and every support mapping in the ledger at the revised snapshot.
- `rule-7058679348.md`: the text of issue #60 comment 7058679348, the rule that governs support-word selection.
- `Words.kt`: the app's word-quiz code (how word `quiz_exclusions` and option scoring are used).
- `verify-commit.txt`: `git verify-commit -v` and `git log --show-signature` for the reviewed and revised snapshots, and their parents.
- `selection-order.tsv`: the frozen source rows 1-140 (`docs\n1-sources\source-index.json`) with KANJIDIC2 grade, Joyo or name-use class, whether a card exists at the batch base ad1694c1, and membership in this batch.
- Pinned KANJIDIC2 input: `kanjidic2-selected.xml` (sha256 481865c3e06efce142039741f2eb30a85e2b6d305e05b1c9c8ec9126044ddd9c). The 10 KANJIDIC2 records are in the original packet
  (`evidence\kanjidic2-records.xml`), together with the retrieved Digital Daijisen text (`evidence\public-source\`).
