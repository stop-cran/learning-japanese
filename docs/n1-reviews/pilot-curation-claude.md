# N1 pilot curation diff review: snapshot b43173e

I found two minor quiz-exclusion gaps, both affecting coverage. I found no correctness errors in the changed passages, the reading allocations, the quiz metadata or the four new support articles.

**Snapshot:** b43173e10f158f59df49137394e1ebbfb0821393, committed teaching only, diff base b43143f. I edited nothing and ran no commands.

## Scope
**Model:** Claude Opus 5.5 (claude-opus-5.5).

**Facets reviewed:** correctness, scoped coverage and phone comprehensibility for:
- The changed passages and quiz metadata in all 12 kanji cards.
- The four new support articles in full: `words/幹.md`, `words/凹凸.md`, `words/矛.md`, `words/鷹揚.md`.
- The changed passages in the reused `words/氏.md` and `words/でこぼこ.md`.

**Packets read in full, one call at a time:**
- `packet-index.json`
- `teaching-01.txt` (204 lines), `teaching-02.txt` (244), `teaching-03.txt` (282), `teaching-04.txt` (131)
- `dictionary-01.txt` to `dictionary-05.txt` (467, 482, 408, 419 and 74 lines)
- `comparisons-01.txt` to `comparisons-03.txt` (264, 244 and 89 lines)
- `metadata-and-offered-keys.json` (470 lines)
- `teaching.diff`, lines 1–240 and 241–478

Nothing was truncated or left out.

**Extra read-only checks:**
- A search of `title:` lines in `words/` for labels that could clash with the new articles' quiz labels.
- Titles and `quiz_exclusions` of 22 comparison candidates.
- A check that 20 linked articles exist.
- A check that the 13 linked articles link back to their kanji cards.
- `docs\content-format.md` lines 80–116.

**Accidental exposure:** one search returned snippets of older review reports from `docs\n1-reviews`, `n2-reviews` and `n2-vocabulary-reviews`. I did not use them. The fact that exclusions apply in both directions comes only from `content-format.md:111` ("must not appear together as quiz choices").

## Verdicts (correctness / scoped coverage / comprehensibility)
All 12 kanji cards are judged on changed passages and metadata only, not a fresh review of unchanged text.

| File | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| kanji/幹 | CLEAN | CLEAN | CLEAN |
| kanji/氏 | CLEAN | CLEAN | CLEAN |
| kanji/扱 | CLEAN | CLEAN | CLEAN |
| kanji/乃 | CLEAN | CLEAN | CLEAN |
| kanji/凹 | CLEAN | CLEAN | CLEAN |
| kanji/凸 | CLEAN | CLEAN | CLEAN |
| kanji/矛 | CLEAN | CLEAN | CLEAN |
| kanji/鷹 | CLEAN | CLEAN | CLEAN |
| kanji/彗 | CLEAN | CLEAN | CLEAN |
| kanji/漱 | CLEAN | CLEAN | CLEAN |
| kanji/栞 | CLEAN | CLEAN | CLEAN |
| kanji/莉 | CLEAN | CLEAN | CLEAN |
| words/幹.md | CLEAN | NEEDS FIX (F2) | CLEAN |
| words/凹凸.md | CLEAN | NEEDS FIX (F1) | CLEAN |
| words/矛.md | CLEAN | CLEAN | CLEAN |
| words/鷹揚.md | CLEAN | CLEAN | CLEAN |
| words/氏.md (changed passage only) | CLEAN | CLEAN | CLEAN |
| words/でこぼこ.md (changed passage only) | CLEAN | CLEAN | CLEAN |

## Findings

**F1 — Minor; scoped coverage; `words/凹凸.md:4,8`**
- **Claim:** the displayed title "unevenness; disparity" is guarded only against texture words: でこぼこ, ごつごつ and ざらざら.
- **What's missing:** the corpus label 差 "difference; gap" is a near-synonym of "disparity".
  - Weaker candidates, each needing a separate pairwise check:
    - 違い and 相違, both "difference; discrepancy".
    - ぶつぶつ "…small bumps". It already excludes でこぼこ.
    - 粗い "coarse; rough". It already excludes でこぼこ, ざらざら and ごつごつ.
- **Learning impact:** in a 差 quiz, "unevenness; disparity" could appear as a wrong answer that is defensibly correct.
- **Evidence:** JMdict 1179280 sense 2 (imbalance; inequality; unevenness; disparity) and sense 1 ("roughness", "bumpiness").
- **Remedy:** add 差 to 凹凸's `quiz_exclusions`. One declaration covers both directions. Decide the weaker candidates pair by pair, not by inference from other exclusions.
- **Confidence:** medium for 差; low to medium for the others.

**F2 — Minor; scoped coverage; `words/幹.md:4,8`**
- **Claim:** "tree trunk; backbone" excludes the 基 family but not 柱 "pillar; mainstay". In English, "backbone" and "mainstay" are close synonyms (compare 一家の柱, the mainstay of a family).
- **Learning impact:** in a 柱 quiz, "tree trunk; backbone" could look like a correct answer.
- **Evidence:** JMdict 1577640 sense 2 (backbone; base; foundation).
- **Remedy:** add 柱 to 幹's exclusions. Optionally check 地盤 "ground; supporting base" pair by pair.
- **Confidence:** medium.

## How suitable the offered reading keys are
Each offered key has a defensible anchor: its own Readings row and a link to an existing article. Each kanji's reading in that word is supported by the dictionary entry.

| Kanji | Offered keys | Anchor |
| --- | --- | --- |
| 幹 | かん, みき | 新幹線 (しんかんせん), 幹 (みき) |
| 氏 | し, うじ | 氏 (し). The うじ word is explicitly taught as a separate identity in `words/氏.md:29-36`. |
| 扱 | あつかう | 扱う (あつかう) |
| 乃 | ない | 乃至 (ないし); the article notes it is usually written in kana. |
| 凹 | おう, へこむ, ぼこ | 凹凸/凹レンズ, 凹む (へこむ), 凸凹 (でこぼこ) |
| 凸 | とつ, でこ | 凸レンズ, 凸凹 (でこぼこ) |
| 矛 | む, ほこ | 矛盾 (むじゅん), 矛 (ほこ) |
| 鷹 | おう, たか | 鷹揚 (おうよう), 鷹 (たか) |
| 彗 | すい | 彗星 (すいせい) |
| 漱 | うがい | うがい; the card says 漱 is a rare spelling of it. |
| 栞 | しおり | 栞 (しおり) |
| 莉 | り | 茉莉花 (まつりか) |

The weakest selections are still acceptable:
- 漱 → うがい uses a rare spelling (JMdict 1577660 marks it "rarely used").
- 凹 → ぼこ only occurs bound inside でこぼこ.

Leaving readings out (くぼむ, ヨウ, ソウ and the source-only readings) is defensible. All full readings stay protected from wrong-answer use, and the full source metadata and order are unchanged.

## Optional, nonblocking
- `words/鷹揚.md:18`: the example 小さな失敗にも ("even about small mistakes") reads oddly, because tolerance of small things is the expected case. 小さな失敗には鷹揚です would fit the definition better. This is low confidence and needs native-speaker judgment.
- `words/凹凸.md:30` could mention that でこぼこ also shares the imbalance sense (JMdict 1582410 sense 2).

## Limits
- I did no live retrieval. The Kotobank and Kanjipedia evidence comes only from the coordinator's supplied observations.
- I did not recompute any hashes.
- The checks that linked articles exist and link back, and the collision search, ran against the working tree, not the committed snapshot bytes.
- I did not run the app. Symmetric exclusions are taken from the documentation, not observed.
- There is no native-speaker, phone, rendering or measured-learning certification. "CLEAN" means no actionable defect was found within this scope.
