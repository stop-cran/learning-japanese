# Bounded curation confirmation

**Result: CLEAN.** The revised passages and direct exclusions are defensible; no consequential in-scope textual defect or correction regression remains established.

## Snapshot and scope

- **Revised snapshot:** `bb448a25c522e9703d43e87216320c48a9121f1c`
- **Originally reviewed snapshot:** `b43173e10f158f59df49137394e1ebbfb0821393`
- **Model:** GPT-6.1 Sol (`gpt-6.1-sol`)

This continues my original review, which reported **no findings**. It confirms the actual changes to `words\幹.md`, `words\凹凸.md`, and `words\鷹揚.md`, assessing correctness, scoped coverage, and textual phone comprehensibility. Snapshot attribution follows the supplied frozen context; Git state and hashes were not independently verified.

All six bounded files were read completely, serially, in the requested order:

| File | Range read |
|---|---|
| `packet-index.json` | Entire document |
| `teaching.diff` | 1–47 |
| `changed-articles.txt` | 1–134 |
| `comparisons-01.txt` | 1–171 |
| `comparisons-02.txt` | 1–139 |
| `dictionary.xml` | 1–298 |

Nothing was omitted or truncated. No other files, archives, reports, or public pages were retrieved during this confirmation. No commands, edits, delegation, parallel calls, tasks, issues, or publication occurred.

## Verdicts

| Changed file | Correctness | Scoped coverage | Textual phone comprehensibility |
|---|---|---|---|
| `words\幹.md` | CLEAN | CLEAN | CLEAN |
| `words\凹凸.md` | CLEAN | CLEAN | CLEAN |
| `words\鷹揚.md` | CLEAN | CLEAN | CLEAN |

**Carry-forward, not fresh rereview:** My original three-facet CLEAN assessments remain unchanged for all twelve kanji, `words\矛.md`, and reused `words\氏.md` and `words\でこぼこ.md`, within their originally assigned scopes.

## Findings and reconciliation

F1/F2 below are identifiers supplied for reconciliation, **not retrospective findings attributed to my original report**. My earlier comparison evidence did not include these seven newly supplied comparison articles.

| Item | Confirmation and evidence | Status |
|---|---|---|
| **F1: 凹凸 ↔ 差** | `words\凹凸.md:8` now directly excludes 差. Its actual “difference; gap” label and quantitative-gap examples overlap abstract disparity: JMdict **1291070 sense 1** versus **1179280 sense 2** from the original evidence. | **Resolved in revised text; high confidence** |
| 凹凸 ↔ 違い | The added direct exclusion is independently defensible: actual “difference; discrepancy,” including a price difference, overlaps disparity. **1158870 sense 1** versus **1179280 sense 2**. No reliance on its exclusion of 差. | **Hypothesis assessed; exclusion justified** |
| 凹凸 ↔ 相違 | Actual “difference; discrepancy” and the formal-comparison body support overlap with abstract disparity. **1400820 sense 1** versus **1179280 sense 2**. Register differences do not make a safe context-free wrong answer. | **Hypothesis assessed; exclusion justified** |
| 凹凸 ↔ ぶつぶつ | Its displayed label expressly includes “small bumps,” and the body teaches that separate physical use. **1011200 sense 2** supports the bumps/spots interpretation against **1179280 sense 1**, physical unevenness. This is not a claim that grumbling means unevenness. | **Hypothesis assessed; conservative direct exclusion justified** |
| 凹凸 ↔ 粗い | Actual “coarse; rough,” rough finishing, and **1396910 sense 1** support physical-roughness ambiguity against **1179280 sense 1**. The different grammatical categories do not eliminate meaning-label ambiguity. | **Hypothesis assessed; exclusion justified** |
| **F2: 幹 ↔ 柱** | `words\幹.md:8` now directly excludes 柱. Its actual “pillar; mainstay” label and figurative supporting-person use overlap 幹’s backbone sense: **1426480 sense 2** versus **1577640 sense 2**. | **Resolved in revised text; high confidence** |
| 幹 ↔ 地盤 | The direct exclusion is independently supported by the actual “ground; supporting base” label and explicit figurative foundation/base teaching. **1421420 senses 2–3** overlap the foundation use in **1577640 sense 2**. No inference from shared exclusions is needed. | **Optional hypothesis assessed; exclusion justified** |

These judgments concern quiz ambiguity, **not unrestricted Japanese synonymy**. Separate same-spelling families—差 read さし (**2423450**) and 柱 read ちゅう／じ／じゅう (**2424140**, **2424150**)—supply no meanings to the comparison identities above.

### Passage polish and regressions

- **`words\鷹揚.md:18`: optional polish accepted.** The revised `小さな失敗には` and “about small mistakes” agree, and the kana matches. This does not establish that the earlier `にも` sentence was erroneous.
- **`words\凹凸.md:30–32`: clarification accepted.** “It” clearly refers to the explicitly identified でこぼこ reading. The added imbalance/mismatch statement agrees with **1582410 sense 2**, restricted to でこぼこ, without extending it to とつおう.
- Existing exclusions are retained. The diff changes no identities, primary readings, levels, links, kanji metadata, full reading lists/order, or selected subsets. No regression was established.

**Actual-reading-key suitability:** The original assessment of all **19 offered keys** carries forward unchanged, including 漱 → うがい as explicitly qualified rare-spelling recognition. This diff neither changes those questions nor weakens their teaching anchors; they were not freshly re-executed.

## Optional

None remaining.

## Limits

The ten complete dictionary families and comparison articles were supplied frozen evidence, not independent upstream retrieval. Relevant target-family evidence and public-source qualifications were carried forward from my own original review. No new live dictionary access or independent hash/commit verification occurred.

This is textual confirmation only: no native execution/import, physical-phone or rendering, publication acceptance, native-speaker, or measured-learning certification. Compatible-client and full native/publication gates remain separate and outstanding. **CLEAN means no actionable defect established within this bounded scope.**
