## Snapshot
Frozen commit **fc23c8b22dc373e0a087e4ee7f09b550a50d870f**, with parent b2ae1ea479c1b24020216c361ceb4f69b23a13d9, as recorded in `frozen-snapshot.json` with `cleanCommittedContent: true`. I reviewed committed content only. My file tools cannot run Git, so the commit identity, the hashes and the equivalence checks are the author's results. I did not re-run them.

## Scope
**Model:** claude-opus-5.5 (family claude). Read-only. No agents, no delegation and no edits.

**Read in full:**
- **Private files:** `frozen-snapshot.json`, `related.patch`, `review-mappings.jsonl` (20 records), `review-principals.jsonl` (20 complete families with restrictions, flags, POS and senses), `review-components.jsonl` (31 records) and `public-bodies.txt`.
- **Rules:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, `docs\content-format.md:18-103` and `docs\jlpt-levels.md`.
- **TSV:** the header and rows N2:1342–1361 only.
- **Assigned articles:** all 18 new articles, plus 花火 and 羽.
- **Kanji cards:** 肌, 羽, 根 and 放.
- **Older bodies:** 毎朝, 台所 and 場所 for the mixed-reading convention, and 春, 忙しい and 過剰 for my quiz findings.

**Read only partly:**
- `docs\confusable-words.md`: lines 1-30, plus a search for batch words. None appear.
- `kanji\`: a search to confirm which cards exist. There are no cards for 射, 揮, 派, 甚, 嫁 or 鉢, and the articles correctly leave them unlinked.
- About 200 comparison candidates in `words\`: I read only their title, type and quiz_exclusions lines. I did not read those bodies in full.

**Web pages I fetched myself:**
- Kotobank ばつ, which includes the Seisenban Nihon Kokugo Daijiten entry for the mark.
- Kotobank 鉢 (Seisenban, 字通 and encyclopedias).
- Kotobank 鉢多羅.
- ja.wikipedia 応量器.
- Weblio and Kotobank lookups for はったら/はつたら failed (404).

**Not read:** `review-evidence.json`, `review-labels.jsonl`, `public-bodies.json`, family-inspection-01–15, old-body-inspection-01–16, the full `words\示す.md`, `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`.

I did not reproduce the author's 398-family or 132-identity comparison sets. I followed the restriction on forbidden ledgers and on `batch-68.json`.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1342 肌着 | words\肌着.md | CLEAN | CLEAN | CLEAN | Native はだ + ぎ is correctly wago. Exclusions [下着, シャツ] fit. The 肌 card pair is added on both sides. |
| N2:1343 果して | words\果たして.md | CLEAN | CLEAN | CLEAN | 果して is taught at lines 17 and 29. Covers both the "sure enough" and questioning uses. Exclusions fit. |
| N2:1344 鉢 | words\鉢.md | CLEAN | CLEAN | CLEAN | JMdict senses 1–3 are taught. The Sanskrit origin is hedged. 鉢多羅 is written はったら in Wikipedia and はつたら in two encyclopedias, so this is not a defect. |
| N2:1345 ｘ バツ | words\ばつ.md | NEEDS FIX | NEEDS FIX | CLEAN | F2 (type label) and F1 (ｘ not taught). Examples and the バツ spelling are fine. |
| N2:1346 発揮 | words\発揮.md | CLEAN | CLEAN | CLEAN | Exclusions are defensible. The デモ exclusion follows JMdict's "demonstration" gloss. |
| N2:1347 [blank] バック | words\バック.md | CLEAN | CLEAN | CLEAN | Gairaigo. Exclusions for back and support words are defensible. Leaving バッグ unexcluded is acceptable. |
| N2:1348 発射 | words\発射.md | CLEAN | CLEAN | CLEAN | The contrast with 発車 is useful. The [打つ] exclusion is adequate. |
| N2:1349 発想 | words\発想.md | CLEAN | CLEAN | CLEAN | Excluding 表現 is justified by JMdict's "expression" senses. |
| N2:1350 発電 | words\発電.md | CLEAN | CLEAN | CLEAN | No exclusion is established. |
| N2:1351 発売 | words\発売.md | CLEAN | CLEAN | CLEAN | [販売, 売る] fit. |
| N2:1352 派手 | words\派手.md | CLEAN | CLEAN | CLEAN | On-first mixed reading as kango matches 台所 and 毎朝. The derivation is hedged. The source's "gay" gloss is correctly not carried over. |
| N2:1353 話合い | words\話し合い.md | CLEAN | CLEAN | CLEAN | 話合い is taught at line 17. The raw capture was empty; the canonical form returned the target. |
| N2:1354 話し掛ける | words\話しかける.md | CLEAN | CLEAN | CLEAN | 話し掛ける is taught at line 29 with a link to the 掛 card. |
| N2:1355 話中 | words\話し中.md | NEEDS FIX | CLEAN | CLEAN | F4 (missing exclusion). 話中 is taught at line 17. Kun-first mixed reading as wago matches 場所. |
| N2:1356 甚だしい | words\甚だしい.md | NEEDS FIX | CLEAN | CLEAN | F5 (missing exclusion). The examples are acceptable. |
| N2:1357 花火 | words\花火.md | CLEAN | CLEAN | CLEAN | Only `jlpt: 2` was added. The body is unchanged and not newly authored. |
| N2:1358 花嫁 | words\花嫁.md | CLEAN | CLEAN | CLEAN | [嫁, 妻] is defensible. |
| N2:1359 放れる | words\放れる.md | CLEAN | CLEAN | CLEAN | Examples match Daijisen's はなれる heading, not the unrelated たれる heading. It stays separate from 離れる. |
| N2:1360 羽根 | words\羽.md | CLEAN | CLEAN | CLEAN | Lines 25-28 teach 羽根 as a shuttlecock. Lines 47-49 state the badminton and hanetsuki restrictions correctly. Line 35 links 根. |
| N2:1361 [blank] ばね | words\ばね.md | NEEDS FIX | CLEAN | CLEAN | F3 (missing exclusion). Rare spellings and the ぜんまい reading match the JMdict family. |

**Kanji edits**

| Card | Change | Verdict |
|---|---|---|
| 肌 | New pair 肌 ↔ 肌着 はだぎ (line 32 reading row, line 37 common words, footer 1476500). The ID matches the mapping and the article links back. | CLEAN |
| 羽 | Existing 羽 はね pair kept; line 43 adds the 羽根 note. | CLEAN |
| 根 | Line 43 adds the 羽根 はね alias. It claims no new reading and no literal plant-root meaning. Footer 1171680. | CLEAN |
| 放 | Line 33 reading row (はな.れる) and line 40 common words for 放れる. Footer 1516540. The card stays N3 and makes no N2-kanji claim. | CLEAN |

All four card headers are preserved.

**Baseline preservation:** CLEAN.
- 花火 changed only by adding `jlpt: 2`.
- 羽 keeps its title, `jlpt: 3`, reading, tags, `kanji: [羽]`, exclusions `[翼]` and the counter contrast.
- Every primary written kanji is in the metadata. No missing kanji cards were invented.

**Mappings:** all 20 match their source rows; 18 are new and 2 reused. The 羽根 mapping (`teachingSpelling 羽根`, senses 4-5, additional senses 1-2) is accurate. One is NEEDS FIX: the ばつ mapping note overstates the article's ｘ teaching (F1).

## Findings
- **B68-OPUS-01**
  - Severity / facet: Minor; scoped coverage (and the mapping's accuracy).
  - Location: `words\ばつ.md:15-16, 35-37`.
  - Claim / impact: The source spelling ｘ is the only written form in JMdict 2197150, whose sense 1 is "x (mark); cross". The article mentions ｘ only as a letter normally read エックス. It never says that ｘ can stand for this word and be read ばつ. The mapping note says ｘ is "explicitly recognized", which overstates the article.
  - Remedy: Add one sentence: "Dictionaries record ｘ as a written form of this word; when ｘ stands for the cross mark it is read ばつ."
  - Evidence: principals line 20; mappings line 4.
  - Confidence: high that ｘ is not explicitly taught.
- **B68-OPUS-02**
  - Severity / facet: Minor; correctness.
  - Location: `words\ばつ.md:6, 23-25`.
  - Claim / impact: `type: wago` claims a native origin, but the only origin recorded anywhere is Sino-Japanese:
    - Daijisen (frozen capture): 《「罰点」からか》.
    - Seisenban, which I fetched: 「ばってん（罰点）」からできた語か.
    - JMdict sense 1 cross-references 罰点.

    The article calls wago a "practical grouping for this kana mark name", which redefines how the repository uses the type field. In this repository, 場所 is wago because its first reading is native, and ちゃわん is kango even though it is written in kana.
  - Remedy: Change to kango and keep the hedge, or have maintainers document a convention for kana words of uncertain origin.
  - Confidence: medium.
- **B68-OPUS-03**
  - Severity / facet: Minor; correctness (quiz_exclusions).
  - Location: `words\ばね.md:9, 38-39`; `words\春.md:4, 23`.
  - Claim / impact: 春's whole title is "spring", and ばね's JMdict sense 1 is "spring (device)". Each title can reasonably be accepted for the other word, in either quiz direction. Both bodies already point out the English homonym, and 泉 already excludes 春 for this reason.
  - Remedy: Add 春 to ばね's quiz_exclusions.
  - Confidence: medium-high.
- **B68-OPUS-04**
  - Severity / facet: Minor; correctness (quiz_exclusions).
  - Location: `words\話し中.md:2-9, 33`; `words\忙しい.md:4`.
  - Claim / impact: JMdict 1600920 sense 1 is "busy (phone)". 忙しい's title is "busy; occupied". An engaged line is "busy/occupied" in English, so each title is a plausible answer for the other word. The article itself contrasts 忙しい at line 33.
  - Remedy: Add `quiz_exclusions: [忙しい]`.
  - Confidence: medium.
- **B68-OPUS-05**
  - Severity / facet: Minor; correctness (quiz_exclusions).
  - Location: `words\甚だしい.md:4, 9`; `words\過剰.md:4, 18, 30`.
  - Claim / impact: 甚だしい's title is "extreme; excessive" and 過剰's is "excess; too much". 過剰's own body translates 過剰な as "excessive". The two titles overlap in both directions, but neither article excludes the other.
  - Remedy: Add 過剰 to 甚だしい's quiz_exclusions.
  - Confidence: medium.

## Optional
- 肌着.md:24: link [着る](着る.md) as the source of き/ぎ instead of "the clothing word 着 き".
- 甚だしい: add the common pattern 「Xも甚だしい」 (Daijisen's example is 非常識も甚だしい).
- 話し中.md:37: drop "not that a phone is physically moving".
- 羽.md:43-46: an N2 row now also maps to this article, so say "the N3 source row" there. Briefly gloss 羽根つき as a New Year battledore game.
- 話し合い: note that 話し合う is the usual verb.
- ばね ↔ 泉: an optional exclusion. 泉's "source of water" already disambiguates it.

## Limits
- I could not run Git, so I did not verify hashes or the frozen commit.
- The frozen captures all come from one dictionary, Digital Daijisen via Weblio. My only independent dictionary check is the Seisenban entries I fetched from Kotobank. I did not see the author's separate Kotobank capture.
- I compared quiz exclusions mainly by titles; I read only six older bodies in full. Other overlaps may exist beyond the titles I searched.
- I did not read the labels, the inspection chunks, `review-evidence.json` or the snapshot JSON files.
- 花火's absence from the N3 list is inferred from the article having no `jlpt` before this patch. I did not check the source lists directly.
- 鉢's 「鉢が大きい」 is consistent with Seisenban's "head circumference" sense ⑦, but I found no attestation of that exact phrase.
- Judgments on naturalness are not native-speaker certification.
