## Snapshot
The frozen commit is `9de757c1fdaff0d2012091652d43247998307d29`, with parent `e2edfb235baf79faefae1a7df0785d6f394cf2d4`. I reviewed committed content only. My file tools can't run Git, so the commit identity, clean state and author hash/equivalence checks come from `frozen-snapshot.json`. I did not verify them independently.

## Scope
- **Model:** claude-opus-5.5, Claude family. Read-only; no agents or edits.
- **Read in full:**
  - The three guidance documents, with `content-format.md` limited to lines 18–126.
  - All 20 new articles, `related.patch`, and the 畳, 線 and 袋 kanji cards.
  - The mappings, principals, components (30) and labels (178) JSONL files.
  - `principal-reading.txt` and `public-bodies.txt`.
  - Assigned rows 1002–1021 of `n2-vocabulary-sources.tsv`.
  - The old articles 例え, 立つ and 一瞬.
- **Read in part:**
  - `review-evidence.json`: about lines 1–120, 420–620 and 2620–2800.
  - `family-inspection-08.txt`: only entries 1597040, 1597120, 1597130, 1597190 and 1597200, plus a cut-off list of entry headings. I did not read the ten family files completely.
  - `n2-vocabulary-snapshot.json` (lines 1–40; no per-row data) and `n2-source-snapshot.json` (lines 1–30).
  - `confusable-words.md`: searched only; no relevant pairs.
- **Not read:** `public-bodies.json`, `jlpt-levels.md`, and no forbidden ledgers or files.
- I checked that every linked word and kanji card exists.
- **Web:** one new fetch of the weblio 足袋 page. It was cut off but confirms 足袋（たび）.

## Verdicts
Cells are correctness / scoped coverage / comprehensibility. All articles are new.

| ID | Article | Correct | Coverage | Comprehensible |
|---|---|---|---|---|
| N2:1002 | words\助かる.md | CLEAN | CLEAN | CLEAN |
| N2:1003 | words\但し.md | CLEAN | CLEAN | CLEAN |
| N2:1004 | words\畳む.md | CLEAN | CLEAN | CLEAN |
| N2:1005 | words\立ち止まる.md | CLEAN | CLEAN | CLEAN |
| N2:1006 | words\たちまち.md | NEEDS FIX (B51-F2) | CLEAN | CLEAN |
| N2:1007 | words\建つ.md | CLEAN | CLEAN | CLEAN |
| N2:1008 | words\発つ.md | CLEAN | CLEAN | CLEAN |
| N2:1009 | words\脱線.md | CLEAN | CLEAN | CLEAN |
| N2:1010 | words\妥当.md | CLEAN | CLEAN | CLEAN |
| N2:1011 | words\例える.md | NEEDS FIX (B51-F1) | CLEAN | CLEAN |
| N2:1012 | words\頼もしい.md | CLEAN | CLEAN | CLEAN |
| N2:1013 | words\足袋.md | CLEAN | CLEAN | CLEAN |
| N2:1014 | words\ダブル.md | CLEAN | CLEAN | CLEAN |
| N2:1015 | words\だます.md | CLEAN | CLEAN | CLEAN |
| N2:1016 | words\溜まる.md | CLEAN | CLEAN | CLEAN |
| N2:1017 | words\ダム.md | CLEAN | CLEAN | CLEAN |
| N2:1018 | words\ため息.md (source 溜息) | CLEAN | CLEAN | CLEAN |
| N2:1019 | words\ためらう.md | CLEAN | CLEAN | CLEAN |
| N2:1020 | words\溜める.md | CLEAN | CLEAN | CLEAN |
| N2:1021 | words\だらしない.md | CLEAN | CLEAN | CLEAN |

**Kanji edits**
- **畳: CLEAN.** The たた.む row (line 30) and Common words (line 39) now link 畳む. The metadata already listed 1356780.
- **線: CLEAN.** 脱線 だっせん is added to the セン row (line 30) and Common words (line 45). 1416560 is added to the metadata (line 53).
- **袋: teaching content CLEAN; source note NEEDS FIX (low, B51-F3).** The new row is a qualified whole-word たび reading (line 33), with Common words (line 41) and a Note (line 48). It does not invent 袋び or 足た. The 麦 card already uses a similar "whole-word reading" row.

**Baseline kanji metadata: CLEAN.** The patch changes only body text. Front matter and the existing rows and words are unchanged.

**Kanji in word metadata: CLEAN.** Every written kanji appears in each article's `kanji` list. All 13 existing cards are linked. 但, 脱, 妥 and 溜 have no cards, so they stay in metadata without links.

**Mappings: CLEAN / CLEAN / CLEAN.**
- The TSV rows match the mappings JSONL: IDs, level 2 for source and article, entry numbers and sense indices.
- No article invents a pinned sense number.
- Raw source glosses are kept as-is in the TSV but are not taught as valid: "dumb" for ダム, "to erect" for 建つ, "a slut" for だらしない. Spelling 溜息 → ため息 is normalized and 溜息 is still taught.

## Findings
**B51-F1 · Minor · Quiz exclusions (check 5)**
- **Where:** `words\例える.md:9`; the article itself presents 例え as the related noun at lines 36–38.
- **Problem:** 例え is not excluded. Its title, "example; analogy; metaphor", is a figurative comparison, so a learner could reasonably accept it for "liken; compare figuratively", or the reverse.
- **Inconsistency:** The batch excludes the weaker noun 比較 ("comparison"). Existing articles exclude other noun/verb pairs with the same meaning: 手伝い/手伝う (labels:97), 救助/救う (:107), 生存/生きる (:128) and 信頼/信じる (:52).
- **Fix:** Add 例え to the `quiz_exclusions` of 例える. One side is enough.
- **Evidence:** JMdict 1597120 sense 2 is "simile; metaphor…". JMdict 1597130 is "to compare (something) to; to liken… use a metaphor" (family-inspection-08:56–65).
- **Confidence:** Medium.

**B51-F2 · Minor · Quiz exclusions**
- **Where:** `words\たちまち.md:4,9`.
- **Problem:** The title "in an instant; suddenly" contains 一瞬's title "an instant" (labels:37). 一瞬's own article calls it a "noun and adverb" and teaches 一瞬で "in an instant" (`一瞬.md:16,19,21`). So a learner could reasonably accept either word in either quiz direction.
- **Inconsistency:** The mapping note says a noun is not the same as an adverb. But たちまち already excludes 急, which is not an adverb either ("sudden; urgent; steep", labels:92).
- **Fix:** Add 一瞬 to the exclusions of たちまち.
- **Confidence:** Medium.

**B51-F3 · Low/Trivial · Kanji source note**
- **Where:** `kanji\袋.md:50`.
- **Problem:** The JMdict word list on the 袋 card's last line (`Metadata: … Word pairs:`) leaves out 1404920 (足袋). The same batch's 線 edit added 1416560 to its line (`related.patch:49`). Note line 48 cites 1404920 inline, so the source is stated, just not in that list.
- **Fix:** Append 1404920 to the list.
- **Confidence:** High on the fact; low impact.

## Optional
- **建つ/立つ:** 立つ sense 2 is "to stand (of a… building)" (`family-inspection-08:33`), which overlaps 建っている. An exclusion would match the one 発つ has for 立つ. I did not treat this as a defect because 立つ's title is about posture.
- **たちまち/瞬間** ("instant; moment"): a weaker version of B51-F2.
- **頼もしい/頼る** ("rely on; turn to for help"): same-kanji relationship; an exclusion is optional.
- **助かる:** excluding 手伝う and 手伝い is cautious. Not excluding おかげ ("help; thanks to") is also defensible. Neither choice is established as a defect.

## Limits
- I could not run Git, the validator or any tests, so this is not confirmed to pass a build.
- Judgments of naturalness are not native-speaker certification.
- I did not fully read the ten family renderings, `public-bodies.json` or `review-evidence.json`. A claim that no other sense exists depends on the principal readings and targeted extracts. Records I didn't read don't prove anything is absent.
- Apart from 例え, 立つ and 一瞬, I judged old-article exclusion pairs from their titles and exclusions (labels) only, not their full text. The author's 108 full reads were not repeated.
- The Daijisen evidence is the author's captures. My only new check was a partial 足袋 fetch.
- A search of `content-format.md` displayed some lines outside 18–126. I did not rely on them.
