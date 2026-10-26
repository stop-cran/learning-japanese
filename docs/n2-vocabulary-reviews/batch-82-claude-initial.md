# Batch-82 N2 vocabulary review: rows N2:1622–1641

## Snapshot
The frozen commit is `c2e4e07abeda5bd28c12d0b3f9b0102212d2ae88`, with parent `bc3244fc7256c83e9c44499a65e6b85d586ae0aa`. I reviewed committed content only. File tools cannot run Git, so the hashes and equivalence checks were run by the author and were not re-run by me. I assumed the files I read match the commit.

## Scope
- **Model and method:** claude-opus-5.5 (claude family). The review was read-only, with no edits and no agents.
- **One rule break:** I read `content-structure.instructions.md` and `docs\content-format.md:18-103` as one parallel pair. Every other call was single and serial.
- **Read in full:**
  - `frozen-snapshot.json` and `related.patch`.
  - `.github\copilot-instructions.md` and the two instruction/format files above. I re-read `content-format.md:18-103` later.
  - All 20 assigned articles. I re-read 蒸し暑い, 醜い, 実る, むく, ミリ, 未満, 無数, 無限 and 向かう to pin line numbers.
  - `kanji\蒸.md` and `docs\confusable-words.md:260-264`.
  - The TSV header `[1,1]` and rows `[1622,1641]` only.
  - All 20/20 mappings, 20/20 principal families, 33/33 components and 290/290 labels, using the bounded line ranges you specified.
  - `public-bodies.txt`, complete in one forced read.
  - Two comparison articles: `words\以内.md` and `words\皮.md`.
- **Globs:** one in `kanji\` (which character cards exist) and one in `words\` (which comparison articles exist).
- **Not read:**
  - `review-evidence.json`: it is 1.2 MB, and I did not search inside it.
  - `family-inspection-01..15`, `old-body-inspection-01..20`, `related-kanji-inspection-01` and `public-bodies.json`.
  - `docs\n2-vocabulary-snapshot.json` and `docs\n2-source-snapshot.json`.
  - The families I inspected were the 20 principals only. Beyond the assigned articles, the only full older bodies I read were 皮 and 以内. Other comparisons rest on the label titles.
- **Web:** no fetches.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1622 | 見慣れる | CLEAN | CLEAN | CLEAN | Daijisen sense 1 agrees. Its archaic sense 2 is rightly left out. |
| N2:1623 | 醜い | CLEAN | CLEAN | NEEDS FIX | B82-04: 美しい is not linked, and the 見憎い sentence doesn't follow. |
| N2:1624 | 実る | CLEAN | CLEAN | CLEAN | Both senses match Daijisen. The conjugation wording is odd (Optional). |
| N2:1625 | 身分 | CLEAN | CLEAN | CLEAN | The 14 guards are broad but harmless. |
| N2:1626 | 見本 | CLEAN | CLEAN | CLEAN | Typed wago for the mixed み+ホン reading (yutō). The format rule only covers the on-first case, so this is acceptable. |
| N2:1627 | 見舞う | CLEAN | CLEAN | CLEAN | Visit plus the strike/hit sense (Daijisen 1–2). The large guard list is grounded in the titles. |
| N2:1628 | 未満 | CLEAN | CLEAN | CLEAN | The title "(excluding the limit)" keeps it apart from 以内 "within". |
| N2:1629 | 名字 | CLEAN | CLEAN | CLEAN | Recognizes 苗字. Guards 姓, 名 and 名前 are good. |
| N2:1630 | ミリ | CLEAN | CLEAN | NEEDS FIX | Prefix plus the ミリメートル abbreviation, confirmed by Daijisen. B82-03: the city sentence. |
| N2:1631 | 診る | CLEAN | CLEAN | CLEAN | Matches Daijisen みる sense 7 (「診る」とも書く). CW091 is consistent. |
| N2:1632 | 民間 | CLEAN | CLEAN | CLEAN | Both Daijisen senses are covered. |
| N2:1633 | 民謡 | CLEAN | CLEAN | CLEAN | Consistent with Daijisen. |
| N2:1634 | 向かう (source 向う) | CLEAN | CLEAN | CLEAN | N4, word, reading, title and the old body are kept. The 向う/むこう note at line 25 is accurate. |
| N2:1635 | むく (source 剥く) | NEEDS FIX | CLEAN | NEEDS FIX | B82-01: the 皮 guard is missing. B82-03: meta prose. The すく heading is correctly kept out. |
| N2:1636 | 無限 | CLEAN | CLEAN | CLEAN | Both JMdict senses and both の and な patterns are covered. |
| N2:1637 | 無地 | CLEAN | CLEAN | CLEAN | Guards are weak but harmless. |
| N2:1638 | 蒸し暑い | NEEDS FIX | CLEAN | NEEDS FIX | B82-02: excess guards. B82-03: meta sentence. |
| N2:1639 | 矛盾 | CLEAN | CLEAN | CLEAN | The 韓非子 story matches Daijisen. |
| N2:1640 | 蒸す | CLEAN | CLEAN | CLEAN | Only `jlpt: 2` was added. Body, title, reading and exclusions are unchanged. |
| N2:1641 | 無数 | CLEAN | CLEAN | CLEAN | Wording polish is under Optional. |

**Separate assessments**
- **kanji/蒸 edit and baseline preservation: CLEAN.** The metadata and other teaching are unchanged. The edit adds 蒸し暑い to the む.す row and to Common words, and appends 1356870.
- **Reciprocal links: CLEAN.** 蒸し暑い↔蒸 is new and correct. 蒸す↔蒸 is intact.
- **Components: CLEAN.** Characters with existing cards are linked. Characters without cards (身, 醜, 診, 暑, 無, 矛, 盾, 謡, 剥/剝) are plain text, and no cards are invented. The metadata kanji lists are complete, and むく `[]` is correct.
- **Mappings: CLEAN.** All 20 are correct, including 向う→1604800 (not むこう) and 剥く→1474370 むく (not 向く).
- **CW091: CLEAN.** It only adds the 診る link.

## Findings
- **B82-01**
  - Severity, facet and location: Minor; quiz guard; `words\むく.md:9`.
  - Problem: むく's title "peel; bare teeth" and 皮's title "skin; peel; outer covering" share "peel". "Skin" and "peel" are also むく's own JMdict verb glosses, so a learner could reasonably accept either title for either word.
  - Fix: add 皮 to むく's `quiz_exclusions`.
  - Evidence:
    - `皮.md:4` (title) and `皮.md:14` (teaches 皮をむく).
    - `むく.md:4` (title).
    - Principal 1474370: "to peel; to skin".
  - Confidence: medium.
- **B82-02**
  - Severity, facet and location: Minor; quiz guard; `words\蒸し暑い.md:9`.
  - Problem: the guards 密, 近い, 親しい, 閉じる and 閉まる (and arguably べたべた) rest only on English "close/sticky" weather wording. "Muggy; sultry" shares no meaning with them. The format doc requires guards to come from meanings that actually overlap. The set is also inconsistent: 閉める, 締め切る, くっつく and 接近 are not guarded. A similar baseline guard pattern on 蒸す is out of scope.
  - Fix: remove those five guards.
  - Evidence: `content-format.md` (curate guards from actual overlapping meanings); the label titles; Daijisen 「風がなくて湿気が多く…暑い」.
  - Confidence: medium.
- **B82-03**
  - Severity, facet and location: Minor; comprehensibility. `蒸し暑い.md:44-46`, `むく.md:33`, `むく.md:47-48`, `ミリ.md:36-37`.
  - Problem: learner-facing prose contains notes about authoring and evidence sources, for example "Their quiz safeguards concern ambiguous English labels" (蒸し暑い), "does not pretend the source has no kanji spelling" and "presence of 剥 in another dictionary heading" (むく), and "an unrelated place named ミリ" (ミリ).
  - Fix: delete these sentences or rewrite them as learner notes.
  - Evidence: the quoted lines.
  - Confidence: high.
- **B82-04**
  - Severity, facet and location: Minor; links and comprehensibility. `醜い.md:37` and `醜い.md:29-30`.
  - Problem: 美しい is plain text although `words\美しい.md` exists. Also, the 見憎い sentence about "a sequence of on-readings" doesn't follow from anything.
  - Fix: link it as `[美しい](美しい.md)`. Rephrase to "rare spelling 見憎い (み+にくい)".
  - Evidence: the `words\` glob.
  - Confidence: high for the link, medium for the wording.

## Optional
- 実る:22,30: "despite ending in る / like 見る" is odd, since みのる cannot be ichidan.
- 無数:30 ("ゲン") and 無限:29-30: drop the trivial reading comparisons.
- 未満:42-43 and 無数:41: rephrase "source gloss".
- 無数:21: the example might read more naturally as 「この種の問題の例は無数にある」 (low confidence).
- むく:28: in 歯をむく, を marks what is exposed, not what is removed.
- 向かう:25: could link [向こう](向こう.md).
- 未満: could mention 以内.
- 見慣れる: could add an example used as a predicate.

## Limits
- I did not run Git.
- One read pair broke the serial rule.
- Old-body and family inspection files and `review-evidence.json` were not read. Guard judgments beyond 皮 and 以内 rest on label titles.
- Public corroboration comes from one dictionary, Daijisen via Weblio. The 向う capture was empty.
- The American Heritage and Cambridge observations were not relied on.
- I did not check whether a 有限 article exists.
- Judgments on example naturalness are not native-speaker certification.
