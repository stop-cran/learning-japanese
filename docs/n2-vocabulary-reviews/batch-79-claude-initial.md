## Snapshot
The frozen commit is `193c2cd87a3d78c1b2ea4e3fb680216cbdfaef46`, with parent `54e5f5c919d3fed9cb0e301c92ca404fc162367a`, committed content only. File tools cannot run Git or compute hashes. I read working-tree files and relied on the receipt's `cleanCommittedContent: true`. I did not check that clean state or the author's hash/equivalence checks myself.

## Scope
**Model:** claude-opus-5.5 (claude family).

**Guidance read:** `copilot-instructions.md`, `content-structure.instructions.md` and `content-format.md:18-103`.

**Mappings and source rows:** mappings 1–10 and 11–20, plus TSV `[1,1]` and `[1562,1581]`.

**Packet records, all read in the required bounded ranges:**
- principals: 18 families / 50 senses
- components: 22 records
- labels: 203 records

**Articles and kanji:**
- `related.patch` in full
- all 18 assigned articles and the 枚, 巻 and 混 kanji bodies in full
- a glob of `kanji\` to confirm which component cards exist

**Supplementary dictionary files:**
- `public-bodies.txt`: read in full; Daijisen via Weblio is the only authority.
- `supplement-comparison-reading.txt`: どうも, 御礼 and ごしごし, 12 senses.
- `extra-comparison-reading.txt`: 悪い, 憎い, 礼 and 難い, 17 senses.
- In total I read 25 dictionary families / 79 senses. That is not the author's 313/816 or the 399 prepared families.

**Comparison words:**
- I read 度 in full, ためらう lines 1–12, and front matter only for プラス, おどおど, 交流, 一応, 割合 and 種.
- I compared titles and exclusions for other words from the labels file, not their full bodies.

**Web:**
- Kotobank's Nikkoku entry for 交ざる confirms the 交, 混 and 雑 spellings but gives no usage guidance.
- The 文化審議会 PDF came back as binary, so I could not use it.

**Not read:** all `family-inspection-*` files, `old-body-inspection-*` files, `public-bodies.json` and `related-kanji-inspection-01`. I read only lines 1–60 of `review-evidence.json`, which does not count as a full read.

**Process deviations:**
- The TSV header and rows were read in one parallel batch.
- The two supplementary comparison files were also read in one parallel batch.
- Some greps covered several files in one call.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1562 | 盆地 | CLEAN | CLEAN | CLEAN | Matches Daijisen |
| N2:1563 | 本部 | CLEAN | CLEAN | CLEAN | Includes temporary/operational HQ (捜査本部) |
| N2:1564 | 本来 | NEEDS FIX | CLEAN | CLEAN | F1 |
| N2:1565 | まあまあ | CLEAN | CLEAN | CLEAN | Adjectival and urging uses supported |
| N2:1566 | 枚数 | CLEAN | CLEAN | CLEAN | |
| N2:1567 | 毎度 | CLEAN | CLEAN | CLEAN | Thanks guards are justified |
| N2:1568 | マイナス | CLEAN | NEEDS FIX | CLEAN | F3 |
| N2:1569 | 巻く | CLEAN | CLEAN | CLEAN | Reuse preserved; additions sourced |
| N2:1570 | 蒔く | CLEAN | CLEAN | CLEAN | Separate identity 2611890 |
| N2:1571 | 撒く | CLEAN | CLEAN | CLEAN | Separate identity 1303400 |
| N2:1572 | 枕 | CLEAN | CLEAN | CLEAN | ちん heading not imported |
| N2:1573 | 曲げる | CLEAN | CLEAN | CLEAN | 枉げる senses handled |
| N2:1574 | まごまご | NEEDS FIX | CLEAN | CLEAN | F4 |
| N2:1575 | 摩擦 | CLEAN | CLEAN | CLEAN | |
| N2:1576 | 混ざる | CLEAN | NEEDS FIX | CLEAN | F2 (shared) |
| N2:1577 | 混ざる (交ざる) | CLEAN | NEEDS FIX | CLEAN | F2 |
| N2:1578 | 混じる | CLEAN | CLEAN | CLEAN | Godan and こんじる separation correct |
| N2:1579 | 混じる (交じる) | CLEAN | CLEAN | CLEAN | 交じって shown; tendency qualified |
| N2:1580 | マスク | CLEAN | CLEAN | CLEAN | Place-name and musk headings not imported |
| N2:1581 | 混ぜる | CLEAN | CLEAN | CLEAN | |

**Kanji and baseline preservation: CLEAN.**
- 枚: adds the 枚数 links and appends entry 1524630; nothing else changes.
- 混: adds links only; metadata is unchanged.
- 巻: unchanged.
- 巻く: identity, reading, title, type, tags, original teaching and the original four exclusions are all kept. It gains `jlpt: 2`, a bounded recognition note for 煙に巻かれる, and the additional exclusions 覆う, 着る, 転がる and 転がす.

**Component links: CLEAN.**
- Every written Han character is in the metadata.
- Every existing card is linked: 地, 本, 部, 来, 枚, 数, 毎, 度, 曲, 混 and 交.
- Missing cards are left as plain text: 盆, 蒔, 撒, 枕, 摩 and 擦. No missing card was fabricated.

**Reciprocal N2 links: CLEAN.** 枚数/枚, 混ざる/混, 混じる/混 and 混ぜる/混 link both ways. The existing 巻く/巻 pair still holds.

**Mappings: CLEAN (20/20).**
- Raw TSV values are unchanged.
- 交ざる maps to 1603920 (まざる) and 交じる to 1603930 (まじる); both aliases are named in the articles.
- 巻く, 蒔く and 撒く stay distinct from each other and from 幕.

## Findings
**B79-F1**
- **Severity:** Minor.
- **Facet:** Correctness (example naturalness and translation fidelity).
- **Location:** `words\本来.md:17`.
- **Claim/impact:** 本来なら、今日は休みです。 has no counterfactual or contrast, yet it is translated "would be". It reads abruptly and does not match the English.
- **Minimal remedy:** use 本来なら、今日は休みのはずです。 or 本来なら今日は休みなのですが…
- **Evidence:** Daijisen [用法] gives 「本来なら直接伺ってお願いすべきところですが」 (`public-bodies.txt:29`). The article's own lines 22 and 36 (本来ならできるはずだ) use the expectation pattern.
- **Confidence:** Medium.

**B79-F2**
- **Severity:** Minor.
- **Facet:** Scoped coverage.
- **Location:** `words\混ざる.md:19,21,27`.
- **Claim/impact:** The article only lists 交ざる as a spelling. Line 27 says character associations do not settle the choice, but gives no dictionary tendency. Its people-joining example is written 混ざって, though Daijisen links that use to 交 (members stay distinguishable). Row 1577 (交ざる) therefore gets no usage guidance. The sibling `混じる.md:29` does give the tendency.
- **Minimal remedy:** Add the qualified 交/混 tendency sentence. Optionally show 子供たちに交ざって遊びました.
- **Evidence:** `public-bodies.txt:257/265` (→混じる［補説］), `:293/311` (補説: 交 for distinguishable constituents) and `:287` (子供たちに―・って遊ぶ).
- **Confidence:** Medium-high.

**B79-F3**
- **Severity:** Minor.
- **Facet:** Scoped coverage (linking).
- **Location:** `words\マイナス.md:27`.
- **Claim/impact:** プラス is compared substantively but not linked, although `words\プラス.md` exists ("plus; positive factor").
- **Minimal remedy:** Write `[プラス](プラス.md)`.
- **Evidence:** `content-structure.instructions.md:20,55`.
- **Confidence:** High.

**B79-F4**
- **Severity:** Low.
- **Facet:** Correctness (quiz_exclusions).
- **Location:** `words\まごまご.md:9`, with the teaching wording at lines 19 and 30.
- **Claim/impact:** The article teaches "dithering" and "confused, ineffective hesitation". A learner could then accept ためらう ("hesitate; waver") for まごまご. ためらう is not excluded, although 迷う ("be undecided") is.
- **Minimal remedy:** Add ためらう on one side, or drop the "hesitation" wording.
- **Evidence:** JMdict 1012110 glosses only "confused; flustered; at a loss". The ためらう label is `[迷う, ぐずぐず, おどおど]`.
- **Confidence:** Medium-low.

## Optional
- **巻く:** distinguish the idiom 煙(けむ)に巻く ("mystify") from 煙に巻かれる (けむりに, enveloped in smoke). Daijisen lists both.
- **撒く:36:** "reading of the situation" could be misread as a kana reading; consider "interpretation".
- **Low-value conservative exclusions:**
  - 蒔く/散る (intransitive "fall like blossoms")
  - 合同 and 組み合わせ on the three 混 verbs
  - マイナス with 欠陥 and 弱点
- **Weak omissions, possibly not worth a guard:** 毎度/度 (titles differ by "thanks…" and "degree"), 本来/自然, まあまあ/普通.
- **枚数:33:** 枚数は何枚ですか is redundant; a plainer alternative is 何枚ありますか.

## Limits
- Only one public authority (Daijisen) was available. The 異字同訓 guidance could not be checked because the PDF fetch failed.
- Example naturalness is my judgment, not a native-speaker certification.
- I did not read the inspection files of family records and older bodies. Exclusion judgments rest on full current titles and exclusions, plus the full bodies of 度, 巻く and the assigned articles. Ordinary secondary senses in other older bodies were not fully inspected.
- Dictionary coverage was 25 families / 79 senses, not all 399.
- Hash and equivalence checks and the clean committed state were not independently verified.
- Two parallel read batches broke the serial-read instruction.
