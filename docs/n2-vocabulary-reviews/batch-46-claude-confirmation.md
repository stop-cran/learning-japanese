## Correction review: N2 batch 46 (N2:902–921)

All five of my original findings are resolved, and none of the seven changed cards introduced a regression. All twenty rows, the three kanji edits, the seven link-only edits, the せっせと level change and all twenty mappings are CLEAN.

### Snapshot
- **Correction commit:** `069fddd9213233078034643051e18ba9749cf354`
- **Parent:** `97436ec4589201838df1b398046729a2c43d57fe`, my original snapshot, as the receipt requires.
- **Content:** the receipt says committed content only (`cleanCommittedContent: true`). It lists seven changed files, all of them new cards.
- **Not reproducible by me:** my tools can only read files, not run Git. I read the working tree and assumed it matches the commit. The Git, hash and equivalence results (including `contentDiffSha256` and the per-file hashes) are the author's claims.

### Scope
- **Reviewer:** claude-opus-5.5 (Claude family), read-only. No edits, commands, agents or delegation.
- **Session:** this is the same session as my initial review. Earlier context was summarized, and my original findings come from that summary and the report I already issued.
- **Read completely in this pass:**
  - `batch-46-correction-snapshot.json` and `batch-46-correction.patch` (seven files, nine hunks).
  - The seven changed cards: せめて, 攻める, 先端, ゼミ, 専制, 全集 and 前後.
  - `batch-46-corrections-comparison-reading.txt`: all 17 corrective families, listed under Corrective families below.
  - `batch-46-corrections-existing-reading.txt`: all six old card bodies (くらい, トップ, 授業, 支配, シリーズ, 戦う).
- **Read in part:** the `correctionEvidence` section of `batch-46-corrected-review-evidence.json` (lines 43355–43700), which holds the adjudications, current declarations and inspection counts. I did not reread the rest of that ~43k-line file.
- **Spot-checked by grep:**
  - Reading-row, Common-words and note lines in `kanji\接.md`, `戸.md` and `専.md`.
  - The seven link-only lines.
  - Frontmatter of せっせと and of the exclusion targets (くらい, 授業, トップ, シリーズ, 支配, 戦う, 勉強).
  - TSV rows N2:902–921 (20 rows), with N2:908 and N2:912 read in full.
- **Carried over from my initial review, not reread:**
  - The bodies of the twelve unchanged new cards: 接続, 瀬戸物, ぜひとも, 迫る, セメント, 栓, 洗剤, 全身, 扇子, 先々月, 先々週 and 先祖. That earlier read was a complete read.
  - The full body of せっせと.
  - The principal, mapping, component and label JSONL files.
  - The public bodies.
  - Exception: during the summarized part of this session I reread ぜひとも, 攻める and 接続 in full, before the correction.
- **Not read:** the other reviewer's report, the forbidden documents and the batch packet, `n2-vocabulary-snapshot.json`, `n2-source-snapshot.json` and `jlpt-levels.md`.
- **Counts I did not verify:** the author's totals of 436 families, 1,080 senses, 118 existing bodies and 272 labels describe the author's inspection, not mine.

### Verdicts
Cells are correctness / scoped coverage / comprehensibility.

| ID | Article | Status | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:902 | せっせと | reused, level only; carried over (frontmatter rechecked) | CLEAN | CLEAN | CLEAN |
| N2:903 | 接続 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:904 | 瀬戸物 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:905 | ぜひとも | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:906 | 迫る | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:907 | ゼミ | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |
| N2:908 | せめて | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |
| N2:909 | 攻める | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |
| N2:910 | セメント | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:911 | 栓 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:912 | 前後 | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |
| N2:913 | 洗剤 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:914 | 全集 | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |
| N2:915 | 全身 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:916 | 扇子 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:917 | 専制 | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |
| N2:918 | 先々月 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:919 | 先々週 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:920 | 先祖 | new, unchanged; carried over | CLEAN | CLEAN | CLEAN |
| N2:921 | 先端 | new, **changed; reassessed** | CLEAN | CLEAN | CLEAN |

**Kanji edits (unchanged): CLEAN / CLEAN / CLEAN.** The reciprocal links are still at the right readings:
- 接/接続 at セツ: `接.md` lines 30 (reading row), 43 (Common words) and 52 (note: せつ without っ).
- 戸/瀬戸物 at と inside the place name 瀬戸 (Seto): `戸.md` lines 31, 38 and 46.
- 専/専制 at セン: `専.md` lines 28, 34 and 40.

**Seven link-only old-word edits (unchanged): CLEAN / CLEAN / CLEAN.** Each link is present and its target exists:
- 繋ぐ:29 → 接続
- コンクリート:28 → セメント
- 少なくとも:36 → せめて
- せっけん:25 → 洗剤
- 責める:35 → 攻める
- 先週:25 → 先々週
- 再来月:26 → 先々月

**Reused せっせと level: CLEAN / CLEAN / CLEAN.** Line 5 is still `jlpt: 2`, it is still a level-only change, and its existing exclusions are unchanged.

**All twenty mappings: CLEAN / CLEAN / CLEAN.**
- The TSV still has 20 rows, and the raw source fields are preserved.
- **N2:908 せめて:** the selected entry is still adverb 1006570, sense 1. The mismatched raw gloss "offense, method of attack" is still credited to the separate noun 攻め手 1675160. The notes do not claim to recover the compiler's intent.
- **N2:912 前後:** 1392910 senses 1–8 are still selected, and the raw "throughout" gloss is preserved.
- **ぜひとも:** still `kanji: []`. Its written forms 是非とも and 是非共 are only recognized in the text, with no kanji metadata or reciprocal pairs added.

### Findings
Severity and confidence below are kept as I originally graded them.

**My original findings**
- **F1 (minor, medium): resolved.** `先端.md:9` now excludes トップ.
  - 1388110:2 is "forefront; leading edge"; 1085030:2 is "top position".
  - トップ's actual title is "top; leading position", and 先端 line 45 says "identifies a leading position".
- **F2 (minor, medium): resolved.** `ゼミ.md:9` now has `quiz_exclusions: [授業]`.
  - 授業's title is "class, lesson" and 1330290 covers "lesson; class".
  - Lines 34–36 still keep the two apart ("A ゼミ can be a 授業, but…"), so the guard does not equate them.
- **F3 (minor, medium-low): resolved.** `専制.md:9` now excludes 支配.
  - 支配's title is "rule; domination; control" (1310270:1).
  - Lines 15 and 47 still limit 専制 to arbitrary, concentrated rule.
- **F4 (minor, medium-low): resolved.** `全集.md:9` now excludes シリーズ.
  - 1395340:1 includes "complete series", and シリーズ's title is "series" (1062910:1).
  - The text does not claim that every series is a complete collected edition.
- **F5 (minor, medium): resolved.** `前後.md:57` now reads "前後 does not always mean a reversed order; the attached phrase and the presence of する matter."
  - It no longer implies that some uses mean "throughout".
  - It follows logically from the 前後して co-occurrence paragraph above it. Inversion is backed by sense 7 and co-occurrence by sense 8.
  - Selected senses and raw fields are unchanged.

**My original optional items**
- **攻める/戦う: adopted and supported.** "Attack; take on" and "fight; compete" overlap under 1279130:1–2 and 1596960:1–2. The card's transitive を usage is unaffected, and 戦う is not mentioned elsewhere in the body.
- **前後.md:40 "always ぜんご": withdrawn.** The separate archaic entry 2629970 (まえしりえ, "front and rear") makes "always ぜんご" too strong. The current line, which only says the approximation use is not read まえあと, is accurate.
- **専制 "uncommon する" qualifier: withdrawn.** JMdict marks 1389810 as a suru noun, and I have no frequency evidence.

**Changes I did not originally raise, assessed as regression checks**
- **せめて + くらい (`せめて.md:9`): supported, no regression.**
  - The particle entry 1154340 sense 2 glosses "at least", which matches the minimum-request pattern. A learner shown くらい could reasonably accept "at least; even just".
  - The adjective entry 1154330 (暗い) and the rank noun 1155400 (位) remain separate.
  - 前後's own くらい exclusion is unrelated and implies no chain of exclusions.
- **攻める stem wording (`攻める.md:30–31`): correct, no regression.** 攻 is read せ, the okurigana is める, and the ichidan stem is せめ. "Conjugation changes the final る" is still true, and the forms on line 26 (攻めます, 攻めて, 攻めない) are unchanged.
- **Frontmatter:** the new `quiz_exclusions` lines are well formed, and every target card exists.

**New consequential regressions:** none.

### Optional
None of these block the batch.
- **前後 mapping note:** row N2:912 could add an identity note that "throughout" has no 1392910 sense.
- **せめて:** the card could mention the せめて〜くらいは collocation. JMdict's "at most" gloss for 1006570 is still not addressed.
- **ゼミ:** line 29, "inventing an English spelling", is still vague. A 勉強 ("study") guard is possible but weakly supported.
- **ぜひとも:** "weather-prediction adverb" (line 45) is still cryptic.
- **Kanji backlinks to non-N2 cards:** `前.md:28` could link 前後, `子.md:32` 扇子, and `祖.md` (lines 22, 33, 39) 先祖.
- **Other:** 扇子 has no usage citation. 先月 on `再来月.md:26` is still unlinked, as it was before this batch.

### Limits
- **No Git:** that the snapshot is committed, the hashes, and that "no other teaching changed" all rest on the receipt and patch. I could not diff.
- **Unchanged cards:** the twelve unchanged new cards (bodies) and the せっせと body were not reread; their verdicts come from my initial complete read.
- **Comparison families:** in the initial review I read only targeted families, not all 436 families / 1,080 senses. Missing guards elsewhere are still possible.
- **Public dictionary bodies:** these are the author's captures and nothing was fetched fresh. The せっせと and 先々週 captures are empty and 扇子's is a stub.
- **Evidence file:** I read only the `correctionEvidence` section of the corrected evidence file.
- **Judgment and nature of this pass:** whether a guard is plausible is a judgment call. CLEAN is not a native-speaker certification. This pass confirms shared correction hypotheses and is not a second blind review.
