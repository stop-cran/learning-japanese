## Snapshot
`d5066fa715158c8b92eed02438e2c7bb23bf81d5` (parent `1d6bdc3c2bdb3b4231853bd98cabf5ca32076586`). I reviewed committed content only. My file tools can't run Git, so I relied on what `frozen-snapshot.json` states and did not check commit identity or the author's hashes myself.

## Scope
**Model:** claude-opus-5.5 (claude family). The review was read-only, with no edits or delegation.

**Read in full:**
- The instruction files and `docs\content-format.md` lines 18–103.
- All 20 new articles.
- `related.patch` and `kanji\片.md`, `kanji\磨.md`, `kanji\針.md`, `kanji\省.md`.
- These private batch-69 files: mappings (20 records), principals (20 complete families), components (35), labels (111) and `public-bodies.txt`.
- The TSV header and exactly rows N2:1362–1381, found with an anchored search so no neighbouring rows were read.

**Older articles read in full:** ねっしん, 効く, 効果, ぽちゃん, 応援, 印, 盛ん, 支払, 切れ, 所, 早い, 合う, 貯金, 番地, 生き生き. Other older articles were checked only by their title and exclusion lines.

**Read partly:** `review-evidence.json`, lines 1–80 only.

**Not read:**
- `family-inspection-01` to `-11`, `old-body-inspection-01` to `-12`, `public-bodies.json`.
- `docs\n2-vocabulary-snapshot.json`, `docs\n2-source-snapshot.json`, `docs\confusable-words.md`, `docs\jlpt-levels.md`.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1362 | 跳ねる | CLEAN | CLEAN | CLEAN | Intransitive ichidan verb; the splash and show-ending senses are bounded; exclusions are reasonable |
| N2:1363 | 破片 | CLEAN | CLEAN | CLEAN | The 片 reciprocal link is correct |
| N2:1364 | 歯磨き | CLEAN | CLEAN | CLEAN | Source sense 2 plus extra sense 1 |
| N2:1365 | はめる | NEEDS FIX | CLEAN | CLEAN | Missing 合う exclusion (B69-05); good register warning on the vulgar sense |
| N2:1366 | 早口 | CLEAN | CLEAN | CLEAN | Excluding 早い/速い is a bit broad but harmless |
| N2:1367 | 流行る | NEEDS FIX | CLEAN | CLEAN | Missing 盛ん exclusion (B69-04) |
| N2:1368 | 払い込む | NEEDS FIX | CLEAN | CLEAN | Missing 貯金 exclusion (B69-06) |
| N2:1369 | 払い戻す | CLEAN | CLEAN | CLEAN | Narrows the source's broad "repay" gloss correctly |
| N2:1370 | バランス | CLEAN | CLEAN | CLEAN | Blank source spelling preserved |
| N2:1371 | 針金 | CLEAN | CLEAN | CLEAN | Reading はりがね is correct |
| N2:1372 | 張り切る | NEEDS FIX | CLEAN | CLEAN | B69-02 and B69-03 |
| N2:1373 | 反映 | NEEDS FIX | CLEAN | NEEDS FIX | B69-01 |
| N2:1374 | 半径 | CLEAN | CLEAN | CLEAN | Keeps 径 even though there is no card for it |
| N2:1375 | 判子 | CLEAN | CLEAN | CLEAN | Ateji and usually-kana notes are present |
| N2:1376 | 万歳 | CLEAN | CLEAN | CLEAN | Leaves out まんざい and the old reading ばんぜい |
| N2:1377 | 判事 | CLEAN | CLEAN | CLEAN | Limited to the judge title and rank |
| N2:1378 | 反省 | CLEAN | CLEAN | CLEAN | Reciprocal links to 省 and 反映 are correct |
| N2:1379 | 番地 | CLEAN | CLEAN | CLEAN | Senses 1–2 plus extra senses 3–4 |
| N2:1380 | パンツ | CLEAN | CLEAN | CLEAN | Blank source spelling preserved |
| N2:1381 | バンド | CLEAN | CLEAN | CLEAN | Blank source spelling preserved; the music sense is the anchor |

**Kanji edits:** 片/破片 はへん, 磨/歯磨き はみがき, 針/針金 はりがね and 省/反省 はんせい are all CLEAN. The readings are the real whole-word readings, the footer dictionary IDs match, and existing headers and examples are preserved.

**Baseline preservation:** CLEAN. No reused articles, and no easier level is changed.

**Mappings:** CLEAN, 20/20. The TSV rows, the mappings and each article's footer senses agree.

## Findings
- **B69-01 (Medium; Correctness/Comprehensibility)** — `words\反映.md` lines 4, 9, 12 and 44–47.
  - **Problem:** the title "reflection; taking effect" presents the extra computing-only sense 3 (JMdict 1601160, "application (of an update, changes); taking effect") as a general meaning. In ordinary English, "taking effect" is what 効く means.
  - **Impact:** the quiz becomes ambiguous against 効く "take effect; be effective" (`効く.md:4`), and arguably 効果 "effect; effectiveness" (`効果.md:4`). Neither is excluded.
  - **Fix:** retitle to something like "reflection; incorporation (of changes)". If "taking effect" stays, add 効く (and consider 効果) to the exclusions.
  - **Confidence:** high.
- **B69-02 (Low; Correctness, quiz exclusions)** — `words\張り切る.md` lines 4, 9 and 16.
  - **Problem:** "be eager", plus the body's "enthusiasm, or eagerness", overlaps ねっしん "enthusiastic; devoted" (`ねっしん.md:4`). JMdict's glosses for 張り切る include "to be enthusiastic; to be eager". The article already excludes 熱中 "enthusiasm" for this same overlap.
  - **Fix:** add ねっしん. Consider 生き生き "lively; energetically" too.
  - **Confidence:** medium-high for ねっしん; low-medium for 生き生き.
- **B69-03 (Low; Correctness)** — `words\張り切る.md:32`.
  - **Problem:** the line "The dictionary also lists 張切る and はり切る" is not supported. The frozen JMdict 1427870 record lists only 張り切る. The Digital Daijisen heading 張（り）切る supports 張切る only; nothing in the evidence supports はり切る.
  - **Fix:** attribute 張切る to Daijisen and drop はり切る.
  - **Confidence:** high.
- **B69-04 (Low; Correctness, quiz exclusions)** — `words\流行る.md` lines 4, 9 and 26.
  - **Problem:** "flourish" and the body's "thriving or popular shop" overlap 盛ん "thriving; active" (`盛ん.md:4,16`). The repository already treats these as confusable: 栄える "flourish" excludes 盛ん (`栄える.md:8`).
  - **Fix:** add 盛ん.
  - **Confidence:** medium-high.
- **B69-05 (Low; Correctness, quiz exclusions)** — `words\はめる.md` lines 4 and 9.
  - **Problem:** "fit into" overlaps 合う "fit; match" (`合う.md:5`), because English "fit" can be either transitive or intransitive. The existing あてはめる "fit into" already excludes 合う (`あてはめる.md:9`).
  - **Fix:** add 合う.
  - **Confidence:** medium.
- **B69-06 (Low; Correctness, quiz exclusions)** — `words\払い込む.md` lines 4 and 9.
  - **Problem:** "deposit money" overlaps 貯金, whose body says "make a deposit" (`貯金.md:14`). The article excludes 預ける but not 貯金.
  - **Fix:** add 貯金. Consider 支払 "payment".
  - **Confidence:** medium-low.

## Optional
- `反映.md:20`: the optical example could follow Daijisen's intransitive pattern, 夕日が水面に反映する. The current transitive sentence is acceptable.
- The exclusions 反映–表す/表現/示す and 番地–住居/住まい are only weakly justified, but they do no harm.
- `バランス`: the financial sense could follow Daijisen more closely: "balance of income/expenditure or debits/credits".

## Limits
- **No Git:** I couldn't run Git, and I didn't check the author's hash or equivalence results myself.
- **Unread inspection files:** I didn't read the family- or old-body-inspection files. So my claims about the related dictionary entries (撥ねる, 刎ねる, 逸る, 印 read いん, 歯磨き粉) rest only on the articles and the source notes.
- **Single dictionary source:** the public evidence is one dictionary, Digital Daijisen via Weblio. My own fetches from jisho, WWWJDIC and Weblio didn't show the entry text, so they confirm nothing.
- **Borderline exclusions left out on purpose:** 判子/印 (印 read いん means "seal"), 破片/切れ, 万歳/応援, 針金/コード and 反映/及ぼす.
- **Not verified:** the パンツ pitch-accent wording. This review is not a native-speaker certification.
