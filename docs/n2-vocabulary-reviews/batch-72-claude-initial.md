## Snapshot
The frozen commit is `ded07a6f4969b3f63f2e62ae73511fade363ead1` (parent `a36e204d10a23de890c76655f8d2ac1b7954fac1`). I reviewed committed content only. My file tools cannot run Git or compute hashes, so I assumed the working tree matches that commit and did not re-run the author's hash or equivalence checks.

## Scope
I am claude-opus-5.5 (claude family), and I worked read-only with no agents.

**Read in full:**
- The frozen snapshot and `.github\copilot-instructions.md`.
- The content-structure instructions, `docs\content-format.md` lines 18-103, and `docs\confusable-words.md` via grep (no hits for this batch).
- All 20 assigned articles.
- `related.patch` and the complete `kanji\皮.md`, `kanji\準.md` and `kanji\膚.md`.
- The mappings (20), principals (20), components (32) and labels (178) files.
- The TSV header (line 1) and lines 1422-1441 only.
- `public-bodies.txt` and `supplement-comparison-reading.txt`.
- These comparison articles: 夜明け, 明け方, 図鑑, 片仮名, 日の入り.
- Titles and exclusions of about 30 more neighboring articles.

**Link and card checks:**
- There are no kanji cards for 響, 標, 評, 典 or 仮. None of them is linked, and all stay in the articles' kanji metadata.
- All 23 linked kanji cards and all 63 linked word targets exist.

**Not read:**
- `review-evidence.json` and `public-bodies.json` (I read their equivalents).
- `family-inspection-01..10` and `old-body-inspection-01..13`.
- `docs\jlpt-levels.md`, `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1422 | 日の出 | NEEDS FIX | CLEAN | CLEAN | F-01: possible missing quiz exclusion with "dawn" words |
| N2:1423 | 響き | CLEAN | CLEAN | CLEAN | Senses 1-3 taught; 響 has no card and is not linked |
| N2:1424 | 響く | CLEAN | CLEAN | CLEAN | Godan intransitive; が/に correct |
| N2:1425 | 皮膚 | CLEAN | CLEAN | CLEAN | Only change is `jlpt: 2`; body and exclusions [肌, 皮] kept |
| N2:1426 | 冷やす | CLEAN | CLEAN | CLEAN | 落ち着く/冷静 exclusions are backed by sense 2 |
| N2:1427 | 百科事典 | CLEAN | CLEAN | CLEAN | Blank source spelling kept; 百科辞典 is the same family; 典 not invented |
| N2:1428 | 美容 | CLEAN | CLEAN | CLEAN | Selected sense 1 is taught at lines 16 and 25-26 |
| N2:1429 | 表紙 | CLEAN | CLEAN | CLEAN | 裏表紙 is supported by the supplement |
| N2:1430 | 標識 | CLEAN | CLEAN | CLEAN | Exclusions are defensible |
| N2:1431 | 標準 | CLEAN | CLEAN | CLEAN | Its 標本 pair is declared on 標本 (F-02) |
| N2:1432 | 標本 | NEEDS FIX | CLEAN | CLEAN | F-02: unneeded 標準 exclusion |
| N2:1433 | 評論 | CLEAN | CLEAN | CLEAN | 評 has no card and is not linked |
| N2:1434 | 平仮名 | CLEAN | CLEAN | CLEAN | Usually-kana taught; no "47 syllables" rule |
| N2:1435 | ビルディング | CLEAN | CLEAN | CLEAN | Blank source spelling kept |
| N2:1436 | 昼寝 | CLEAN | CLEAN | CLEAN | — |
| N2:1437 | 広げる | NEEDS FIX | CLEAN | CLEAN | F-03: unneeded exclusions copied from 広める |
| N2:1438 | 広さ | CLEAN | CLEAN | CLEAN | — |
| N2:1439 | 広場 | CLEAN | CLEAN | CLEAN | — |
| N2:1440 | 広々 | CLEAN | CLEAN | CLEAN | 々 correctly left out of kanji metadata |
| N2:1441 | 広める | CLEAN | CLEAN | CLEAN | Senses 1 and 2 both selected, as instructed |

**Separate assessments:**
- **皮 edit: CLEAN.** It now links 皮膚 at ひふ in two places, footer ID 1483920 was already present, and nothing else changed.
- **準 edit: CLEAN.** It adds 標準 at ひょうじゅん in two places plus footer ID 1488710; the header and examples are preserved.
- **Unchanged 膚: CLEAN.** It already links 皮膚 and lists ID 1483920.
- **皮膚 baseline: CLEAN.** The title, reading and existing exclusions are unchanged.
- **Mappings: CLEAN.** All 20 match the TSV rows.

## Findings
**F-01 — 日の出 may need exclusions for 夜明け and 明け方**
- **Severity / facet:** Low; correctness (quiz exclusions).
- **Location:** `words\日の出.md:1-9` (no `quiz_exclusions` key).
- **Problem:** Its title "sunrise; time of sunrise" sits close to the shared title "dawn; daybreak" of 夜明け and 明け方. In an English-to-Japanese quiz, a learner could reasonably pick 日の出 for "dawn; daybreak".
- **Minimal fix:** Add `quiz_exclusions: [夜明け, 明け方]`.
- **Evidence:** `日の出.md:31-34` and `夜明け.md:29` both say the words are closely related. The existing `日の入り.md:9` excludes 暮れ ("dusk; year-end"). `content-format.md:95` sets the "reasonably accept" test.
- **Confidence:** Medium-low. Dictionaries do separate the senses, so this is partly a judgment call.

**F-02 — 標本 should not exclude 標準**
- **Severity / facet:** Low; correctness (an unneeded exclusion).
- **Location:** `words\標本.md:9`.
- **Problem:** "specimen; sample; example" and "standard; norm; average" share no meaning, and neither article compares the two words. The pair looks based on the shared 標 spelling, which `content-format.md:90` rules out. Both excluding 典型 does not make them pair with each other, because exclusions are not transitive (`content-format.md:87-88`). The cost is losing a useful same-kanji distractor.
- **Minimal fix:** Remove 標準 from the list.
- **Confidence:** Medium.

**F-03 — 広げる excludes three words it does not overlap with**
- **Severity / facet:** Low; correctness (unneeded exclusions).
- **Location:** `words\広げる.md:9`.
- **Problem:** 伝える ("convey; tell"), 伝わる ("be transmitted; be handed down") and 宣伝 ("publicity; advertising; propaganda") match neither 広げる's title nor any of its four dictionary senses (JMdict 1602370: spread/extend, unfold, scatter about, make flourish). The article never compares them, and they mirror 広める's own list at `広める.md:9`.
- **Minimal fix:** Remove those three from 広げる; they can stay on 広める.
- **Confidence:** Medium. Daijisen does list a ひろめる-like spreading sense for 広げる, but that still doesn't make these titles acceptable answers for it.

## Optional
- The 響き and 標準 footers say "senses 1-N" instead of "selected … additional …" like the other articles.
- 広々 could explain that と is optional and add the common predicate form 広々としている.
- 平仮名's 字/文字 exclusions match the existing 仮名 article but are not necessary; 片仮名 has no exclusions.
- 片仮名 and 日の入り could now link to the new 平仮名 and 日の出 articles.

## Limits
- I could not use Git.
- All public evidence comes from one authority (Digital Daijisen via Weblio) plus the JMdict packet, and there was no native-speaker naturalness check.
- I did not read the inspection files listed under Scope.
- I confirmed that words like 目印, 大きさ, 面積 and 普及 have no article only by globbing for those specific names.
- F-01 is a judgment call.
