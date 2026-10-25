# Batch-71 follow-up reconfirmation (claude-opus-5.5)

Both remaining 一通り issues are now guarded, and I found no actionable defects left in the twenty rows. My first confirmation was not a final acceptance: it left 一通り open on B71-10 and missed GPT-F03.

## Snapshot
- **Revised frozen commit:** dfde68b7992b7151e5fd8ffa1eeaa26135f13a32.
- **Parent:** 73289715182d44fddb23829348ab9bba32ab5f20, the first-correction commit.
- **Content:** committed content only. The snapshot lists `words/一通り.md` as the only changed content or mapping file.
- **Git limitation:** my tools can only read files, not run Git. Checkout, hash, manifest and diff-equivalence checks were run by the author, not by me.

## Scope
Model: claude-opus-5.5. Read-only throughout: no edits, agents, delegation or shell.

**Read in full this turn:**
- **Follow-up files:** the snapshot, followup.patch, the reconciliation, the comparison reading (チェック entry 1077550, 7 senses; 各地 entry 1205100, 1 sense) and the public-bodies note.
- **Articles:** all twenty assigned articles.
- **Kanji cards:** 筆 and 皮.
- **Older and comparison bodies:** チェック and 各地, plus 検査, 確かめる and 改める.
- **Source data:** TSV line 1 and rows 1402–1421 only; mappings (20), principals (20 families, 44 senses) and components (30 records).
- **Rules:** docs\content-format.md lines 60–92.

**Searched or fetched:**
- I searched `words\` titles for "inspection/check/look-over" and "all parts/places" labels, and `quiz_*` lists that mention 一通り. None lists it.
- I fetched the Oxford once-over page myself.

**Carried over from earlier turns:**
- The correction-stage evidence files.
- The Kotobank 日日 and 入る fetches.
- The bodies of 考える, 転がす, 工夫, おおよそ, 出入り, 著す and 絞る.
- The Weblio captures in public-bodies.txt.

**Not read at any stage:**
- The followup review-evidence and completed-inspection JSONs.
- The 18 family chunks and 20 older-body chunks.
- The original supplement.
- Any review ledgers or other reviewers' reports.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1402 | 筆記 | CLEAN | CLEAN | CLEAN | Unchanged; 筆 links reciprocal |
| N2:1403 | ひっくり返す | CLEAN | CLEAN | CLEAN | 転がす guard retained |
| N2:1404 | ひっくり返る | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1405 | 引っ越し | CLEAN | CLEAN | CLEAN | Raw 引越し recognized |
| N2:1406 | 引っ込む | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1407 | 筆者 | CLEAN | CLEAN | CLEAN | 著す guard retained |
| N2:1408 | 必需品 | CLEAN | CLEAN | CLEAN | 需 kept in metadata |
| N2:1409 | 人差し指 | CLEAN | CLEAN | CLEAN | Raw 人差指 search-only |
| N2:1410 | 一通り | CLEAN | CLEAN | CLEAN | チェック and 各地 guards close GPT-F03 and B71-10 |
| N2:1411 | 人通り | CLEAN | CLEAN | CLEAN | 出入り guard retained |
| N2:1412 | ひとまず | CLEAN | CLEAN | CLEAN | Blank source spelling preserved |
| N2:1413 | 瞳 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1414 | 一休み | CLEAN | CLEAN | CLEAN | Only the attested ひと休み listed |
| N2:1415 | 独り言 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1416 | ひとりでに | CLEAN | CLEAN | CLEAN | Blank source spelling preserved |
| N2:1417 | ビニール | CLEAN | CLEAN | CLEAN | Blank spelling; record sense restricted to バイナル |
| N2:1418 | 皮肉 | CLEAN | CLEAN | CLEAN | 皮 links reciprocal |
| N2:1419 | 日にち | CLEAN | CLEAN | CLEAN | Raw "every day, daily" gloss vs 1611370 mismatch kept; Seisenban ③ (earlier fetch) |
| N2:1420 | 捻る | CLEAN | CLEAN | CLEAN | 工夫 and 考える guards retained |
| N2:1421 | 日の入り | CLEAN | CLEAN | CLEAN | 入る (いる) cited |

- **筆 card: CLEAN.**
  - 筆記 ひっき and 筆者 ひっしゃ appear in the ヒツ row, the common words and the contraction note.
  - The footer includes 1487800 and 1487830.
  - The header and the 万年筆, 執筆, 随筆, 鉛筆 and ふで content are preserved.
- **皮 card: CLEAN.**
  - 皮肉 ひにく appears in the ヒ row, the common words and the notes.
  - The footer includes 1483900.
  - The existing content is preserved.
- **Mappings: CLEAN.**
  - All twenty agree with the TSV, including the selected and additional senses.
  - The raw spellings 引っ繰り返す, 引っ繰り返る, 引越し, 人差指 and 日日 remain aliases, not new identities.
  - Additional senses are recognition only, with no separate N2 level assigned.
- **Baseline preservation: CLEAN.**
  - The patch changes only `一通り.md:9`, adding two IDs. Both targets exist and the list has no duplicates or self-reference.
  - No article lists 一通り in `quiz_distractors`.
  - チェック and 各地 are unchanged. The kanji cards, mappings, title, prose and identity are untouched.

## Findings
**GPT-F03 (一通り/チェック): RESOLVED.** I accept it independently.
- The "once-over" label came in with the first correction, so this is a regression from the fix I asked for under B71-09.
- My first-confirmation search matched only the string "once" and missed this overlap.
- **Evidence:**
  - 一通り sense 1 includes "briefly (look over…)".
  - チェック sense 2 includes "looking over", and its title is "check; inspection".
  - I fetched Oxford myself. Use 1 reads "to look at somebody/something quickly to see what they are/it is like". Use 2, quick cleaning, is not relevant to チェック.
- The guard is one direct pair. It does not claim Japanese interchangeability, and it does not inherit the inspection group (検査, 確かめる, 改める guard each other).

**B71-10 (一通り/各地): RESOLVED.**
- The identical unqualified "all parts" segment is now guarded at 一通り.md:9.
- 各地 means spread across places (1205100 sense 1; 各地.md:16, 20), not "the whole set", so a guard is better than a relabel.
- The title search found no other title containing "all parts".

**Weaker edges I checked and did not establish:**
- 検査 is formal testing or inspection; 確かめる is verifying a fact; 改める inspects tickets.
- None of these carries the quick "looking over" sense. The shared generic word "check/inspection" alone does not justify a pair.

**Earlier dispositions stay as before:**
- B71-01 through B71-09: resolved.
- GPT-F01 and GPT-F02: resolved.
- 捻る/絞る: withdrawn.
- The 一人でに, 瞳, page-turning and satire items: remain optional.

**Regressions:** none. **Remaining actionable defects:** none.

## Optional
- 一人でに: JMdict marks it as irregular kanji usage, so "recognized dictionary spelling" could be qualified.
- The 瞳 iris wording, the ひっくり返す page-turning use and the 皮肉 "satire" gloss remain deferred.

## Limits
- I did not fetch Seisenban ひねる or Digital Daijisen 考える myself; those claims rest on the author's excerpts plus JMdict.
- The label checks were pattern searches over titles, not an exhaustive semantic search. The quick-cleaning use of "once-over" was not searched.
- Git and hash verification were done by the author only.
- CLEAN means no actionable defect within the scope I actually read. It is not a runtime-quiz guarantee, native-speaker certification or frequency proof.
