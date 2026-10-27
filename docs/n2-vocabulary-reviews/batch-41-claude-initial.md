## Snapshot
The frozen commit is `f36e1e751aee9d9853bf113bc8d7f11f4734bf8f` (parent `2187c2e50aba8e69e0b21c04559888d89ed30489`). I reviewed committed content only, as recorded in the frozen receipt. I had file tools only, with no Git or hash execution. I could not independently confirm that the working tree matches the commit, or check the packet hashes and equivalence claims.

## Scope
- **Model and process:** claude-opus-5.5 (Claude family). I made no edits and did not delegate. This batch has no reused articles.
- **Articles:** I read all twenty new articles in full.
- **Kanji edits:** I read the whole five-file related patch. For 森 and 林, I grepped the 森林 lines and metadata lines in context. I did not re-read the other kanji files beyond the patch context.
- **Mappings:** I read the TSV header and lines 802–821.
- **Instructions:** I read `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-126`.
- **Evidence read:**
  - principal-reading, in full
  - review-evidence JSON, only in bounded sections: principal records, existingComparisonLabels and quiz declarations
  - selected-families-07, lines 1–30 (the 命 entry 1531940)
  - public-bodies.txt, lines 1–420 (the Daijisen captures for every principal word)
  - many words\ title and quiz_exclusions greps
  - comparison articles: 芸術, 応用, 適用, あてはめる, 申し込む, 学問 and others
- **Fresh fetches:**
  - Weblio 信ずる, which shows the サ変 table taken from Wikipedia
  - en.wiktionary 信ずる
  - ja.wikipedia サ行変格活用
  - Kotobank, which failed or returned nothing relevant
- **Incidental exposure:** one bounded grep over `batch-41-*.txt` also returned lines from three files not on the allowed list:
  - batch-41-comparison-reading.txt
  - batch-41-existing-comparison-cards.txt
  - batch-41-selected-existing-*.txt

  The lines contained JMdict data and existing-article text only. I did not open these files and did not rely on them.
- **Not read:**
  - selected-families 01–06 and 08–10
  - the supplement and final comparison readings
  - public-bodies.json
  - most of componentEvidence
  - n2-vocabulary-snapshot.json and n2-source-snapshot.json
  - confusable-words.md and jlpt-levels.md
- **Forbidden files:** none opened.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 芯 | CLEAN | CLEAN | CLEAN |
| 新幹線 | CLEAN | CLEAN | CLEAN |
| 真空 | CLEAN | CLEAN | CLEAN |
| 信ずる | CLEAN | CLEAN | CLEAN |
| 心身 | CLEAN | CLEAN | CLEAN |
| 申請 | NEEDS FIX (B41-Q-01) | CLEAN | CLEAN |
| 人造 | CLEAN | CLEAN | CLEAN |
| 寝台 | CLEAN | CLEAN | CLEAN |
| 診断 | CLEAN | CLEAN | CLEAN |
| 侵入 | CLEAN | CLEAN | CLEAN |
| 人文科学 | NEEDS FIX (B41-Q-02) | CLEAN | CLEAN |
| 人命 | CLEAN | CLEAN | CLEAN |
| 深夜 | CLEAN | CLEAN | CLEAN |
| 森林 | CLEAN | CLEAN | CLEAN |
| 親類 | CLEAN | CLEAN | CLEAN |
| 針路 | CLEAN | CLEAN | CLEAN |
| 神話 | CLEAN | CLEAN | CLEAN |
| 酢 | CLEAN | CLEAN | CLEAN |
| 水産 | CLEAN | CLEAN | CLEAN |
| 炊事 | CLEAN | CLEAN | CLEAN |

- **Five kanji edits:** CLEAN on all three facets.
  - Each new link sits in the correct on-reading row and in Common words: 線 セン (新幹線), 造 ゾウ (人造), 森 シン (森林), 林 リン (森林) and 針 シン (針路).
  - 線, 造 and 針 add the matching entry IDs (1361590, 1368580, 1366280); 森 and 林 already list 1362530.
  - The existing qualifications are kept: the 線 すじ note, the 造 づくり notes and the 針 notes.
  - The only other N2-level batch characters lack kanji cards: 芯, 幹, 請, 診, 侵, 炊 and 酢. The batch's other written kanji are N3 or easier. No missing component received an invented card or reading.
- **Twenty mappings (N2:802–821):** CLEAN on all three facets. Every row points to the correct article at level 2, with the same entry ID as its source and sense 1 (芯 uses senses 1–2), and status draft.
  - The articles explicitly qualify the broad raw glosses: 人文科学 "social sciences", 炊事 "culinary arts", 真空 "hollow, empty", 寝台 "couch" and 針路 "compass bearing".
  - I checked restrictions, kanaOnly and readings in principal-reading. 寝台's alternate reading ねだい is acknowledged rather than taught.

## Findings
**B41-Q-01: Low; correctness (quiz)**
- **Location:** `words\申請.md:4`, `words\申請.md:9` and `words\申請.md:40-41`.
- **Claim:** the title "application; formal request" leads with bare "application", but 申請 does not exclude 応用 "practical application" or 適用 "application of a rule or method". The article itself warns at lines 40–41 that 申請 "is not the 'application' of a rule or method, as in 適用".
- **Precedent:** the corpus already excludes the apply/application English homographs across senses.
  - `応用.md:9` excludes 適用, あてはめる, 塗る and 申し込む.
  - `あてはめる.md:9` excludes 塗る, 申し込む and 適用.
- **Impact:** in English→Japanese questions, a learner may reasonably accept 応用 for "application", or 申請 for 応用.
- **Remedy:** add 応用 and 適用 to 申請's quiz_exclusions. あてはめる and 塗る are optional.
- **Evidence:** content-format.md:38–99 (quiz exclusion rule); the titles listed above.
- **Confidence:** medium. The qualifiers partly disambiguate, so this is a consistency fix.

**B41-Q-02: Low; correctness (quiz), with wording**
- **Location:** `words\人文科学.md:1-8` (no quiz_exclusions) and `words\人文科学.md:20`.
- **Claim:** line 20 says that English "may also call these academic fields 'the arts'". That echoes the title of 芸術 (`芸術.md:4`, "art; the arts"), and JMdict 1369140 also glosses "arts". Line 17 ("not simply a name for artistic practice") only partly offsets this.
- **Impact:** a learner taught that 人文科学 can mean "the arts" can reasonably accept 芸術's title, and the reverse.
- **Remedy:** add 芸術 to quiz_exclusions, or qualify line 20, for example: "'arts' as in a Faculty of Arts, not 芸術 (artistic practice)". Doing both is best.
- **Evidence:** principal-reading lines 88–92 and the titles above.
- **Confidence:** medium.

## Optional
- **芯:**
  - The 命 exclusion is conservative but defensible: 命 sense 3 means "most important thing, core". 身 is a weak "main part" basis.
  - Line 46's "botanical senses" sits awkwardly beside "plant pith" at line 16; naming pistil/stamen would be clearer.
  - The TSV:802 note says the examples are "pencil lead and plant pith", but the actual examples are pencil lead and a candle wick.
  - Daijisen's undercooked-core use (芯のある御飯) could be added.
- **信ずる:** could show ずる-specific forms (信ずれば, 信ずべき) and a register note. The register claim is unverified.
- **寝台:** could note that ベッド is everyday and 寝台 typical in 寝台車 and institutional contexts. This is unverified.
- **親類:** could add Daijisen's 用法 note comparing 親戚 and 親族, and the figurative "same kind" sense.
- **針路:** 科目 "school subject; course" is not excluded. The qualifiers disambiguate, consistent with the existing 方向/科目 precedent.

## Limits
- With no Git, I could not verify the commit contents or packet hashes. I relied on the receipt.
- The public captures are author captures; my only independent retrievals were the 信ずる lookups.
- Most selected-family files, the comparison readings, componentEvidence and the source snapshots were not read. Omission there does not prove absence.
- I checked exclusion candidates by title grep, not by reading every corpus article.
- The register points for 信ずる and 寝台 are unverified.
- Mapping notes, counts and receipts are author assertions; I treated them as such.
- This review is not a native-speaker certification.
