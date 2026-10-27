## Snapshot: c28c421695f83aac0494994c604792fa8c0f277d — committed content only

Parent: `45d3bbbc5c1a98a48fd3d00c4284d94692b96930`.

**Result:** Fixes are needed for quiz exclusions and three component links. No actionable source-association, selected-sense mapping, grammatical, or example-translation defect was established. Two quiz findings concern inherited behavior in reused articles, not regressions introduced by this batch.

The frozen snapshot was read first. Available file tools cannot execute Git; commit membership, worktree cleanliness, hashes, and unchanged-file assertions therefore remain supplied evidence rather than independently executed checks.

## Scope

Reviewer: **GPT-6.1 Sol**, model ID **`gpt-6.1-sol`**, family **gpt**. Read-only; no agents, delegation, edits, or implementation.

Complete reads covered all sixteen new articles, all four reused bodies, `related.patch`, the three edited kanji cards, and comparison cards `kanji\屋.md`, `kanji\調.md`, and `kanji\止.md`. I also directly read **116 complete older comparison word bodies**, including every declared exclusion target in the assigned articles and the additional bodies supporting the findings below. These are reviewer reads, not the author’s reported 189 inspections.

Required instructions and allowed documentation were read, including `docs\content-format.md:18–103`; both source snapshot documents; and the TSV header and **only N2:1202–N2:1221**.

The permitted blind evidence reads included:
- All twenty mappings, twenty complete principal families, 33 component records, and 212 label records.
- All eleven complete original family renderings and the complete support, extra, and quiz-support renderings. Their supplied union is 358 families/965 senses; those counts were not independently scripted.
- Both complete public-body renderings: twenty capture records, nineteen positive and one failed.
- `review-evidence.json` ranges **1–100, 3005–3210, 3290–3584, 3646–3942, and 39782–EOF**, plus structural-heading searches—not the entire large packet.

One fresh [Jisho/JMdict query for いい](https://jisho.org/api/v1/search/words?keyword=%E3%81%84%E3%81%84) was read, including its complete 良い and いい lexical entries. Its unrelated homophones and JLPT metadata were not used. No prohibited rationale, ledger, reviewer report, or private authoring material was accessed.

Private evidence filenames below refer to the permitted `batch-61-` files at the supplied exact prefix.

## Verdicts

**C** = correctness, including quiz-answer validity; **S** = scoped coverage, including required component navigation; **L** = comprehensibility. A quiz finding does not mean the article’s linguistic explanation is wrong. CLEAN means no actionable defect established within this scope, not exhaustive certification.

The mapping column gives **JMdict entry:selected one-based senses**. **Each of the twenty mappings is separately CLEAN/CLEAN/CLEAN for C/S/L.** Additional recognized senses were assessed without assigning each an independent N2 label.

| Source row | Exact article association | Mapping | C | S | L |
|---|---|---|---|---|---|
| N2:1202 特色 | `words\特色.md` | 1455080:1 | CLEAN | CLEAN | CLEAN |
| N2:1203 特長 | `words\特長.md` | 1455200:1 | NEEDS FIX — F03 | CLEAN | CLEAN |
| N2:1204 特定 | `words\特定.md` | 1455210:1 | CLEAN | CLEAN | CLEAN |
| N2:1205 特売 | `words\特売.md` | 1455250:1 | CLEAN | CLEAN | CLEAN |
| N2:1206 溶け込む | `words\溶け込む.md` | 1546090:1,2 | CLEAN | CLEAN | CLEAN |
| N2:1207 溶ける | `words\溶ける.md` — reuse; level addition only | 1546070:1,2 | CLEAN | CLEAN | CLEAN |
| N2:1208 退ける | `words\退ける.md` — **どける** | 2850084:1 | CLEAN | CLEAN | CLEAN |
| N2:1209 床の間 | `words\床の間.md` | 1349400:1 | CLEAN | CLEAN | CLEAN |
| N2:1210 床屋 | `words\とこや.md` — N4 kana-identity reuse | 1349410:1 | CLEAN | NEEDS FIX — F04 | CLEAN |
| N2:1211 所々 | `words\所々.md` | 1598730:1 | CLEAN | CLEAN | CLEAN |
| N2:1212 都心 | `words\都心.md` | 1445000:1 | CLEAN | CLEAN | CLEAN |
| N2:1213 戸棚 | `words\戸棚.md` | 1267050:1 | CLEAN | CLEAN | CLEAN |
| N2:1214 とっくに | `words\とっくに.md` | 1320570:1 | CLEAN | CLEAN | CLEAN |
| N2:1215 どっと | `words\どっと.md` | 1009210:1,2,3 | CLEAN | CLEAN | CLEAN |
| N2:1216 整う | `words\整う.md` | 1598800:1,2 | NEEDS FIX — F02 | NEEDS FIX — F04 | CLEAN |
| N2:1217 留まる・とどまる | `words\留まる.md` | 2657130:1,2 | NEEDS FIX — F01 | NEEDS FIX — F04 | CLEAN |
| N2:1218 どなる | `words\どなる.md` | 1445740:1 | CLEAN | CLEAN | CLEAN |
| N2:1219 飛び込む | `words\飛び込む.md` | 1598890:1,2 | CLEAN | CLEAN | CLEAN |
| N2:1220 跳ぶ | `words\飛ぶ.md` — unchanged N5 reuse | 1429700:2 | NEEDS FIX — F05 | CLEAN | CLEAN |
| N2:1221 留まる・とまる | `words\止まる.md` — N5 reuse | 1310620:1,2,3 | NEEDS FIX — F06 | CLEAN | CLEAN |

**Mapping adjudication:** The melting family **溶ける1546070** is distinct from the lower-level untie/solve family **解ける1198910**; the complete records support that distinction. The supplied lower-level checks were not rerun. For N2:1221, the article explicitly teaches 留まる/**とまる**, perching, and cautious fixed-in-place recognition. Public とまる is broader than pinned1310620; neither its raw “abide/stay” wording nor the pinned three-sense structure establishes the compiler’s intended individual gloss alignment.

**Kanji edits:**

| Edited card | C | S | L | Reciprocal-pair assessment |
|---|---|---|---|---|
| `kanji\溶.md` | CLEAN | CLEAN | CLEAN | 溶け込む **とけこむ**,1546090; 溶ける **とける**,1546070 |
| `kanji\床.md` | CLEAN | CLEAN | CLEAN | 床の間 **とこのま**,1349400; 床屋 **とこや**,1349410, via `words\とこや.md` |
| `kanji\戸.md` | CLEAN | CLEAN | CLEAN | 戸棚 **とだな**,1267050 |

All five pairs have substantive word-side component links, appropriate kanji reading-row examples, Common words links, and matching footer entry IDs. The supplied patch preserves all three kanji headers. Primary-spelling metadata is correct; missing 棚/整/跳 cards are not defects requiring invented cards.

**Baseline preservation:** CLEAN on the supplied patch and current-body comparison. 溶ける receives only `jlpt: 2`; とこや retains its kana identity, N4 level, title, and prior 床屋 teaching; 止まる retains its N5 identity and prior teaching while adding 留まる/perching recognition. 飛ぶ retains N5 and explicitly teaches 跳ぶ and hopping; its unchanged-byte status is supported only by the frozen receipt, not an independently executed comparison. F05–F06 do not allege preservation regressions.

No actionable excessive exclusion was established. In particular, judgments accounted for ordinary secondary senses—利益’s “advantage,” 味噌’s “good point,” and 避ける’s taught よける variant—rather than rejecting guards from narrow titles or homophony alone.

## Findings

**F01 — Moderate; correctness / quiz exclusions — `words\留まる.md:4,9,42–45`.**

Direct guards are missing for **いる**, **ストップ**, and **立ち止まる**. The “stay” branch of 留まる’s complete title is an ordinary meaning of いる. Separately, the article recognizes the stopping sense of **とどまる**; the captured public entry’s modern first sense explicitly includes stopping ongoing progress and 立ちどまる. Consequently, the complete labels `stop; halt` and `stop in one's tracks; pause` can also be defensible answers for that recognized sense.

**Minimal remedy:** Add those three exact IDs to 留まる’s exclusions; do not inherit an entire stopping clique. Existing guards through 居る or 止まる are nontransitive and do not cover these pairs.

**Exact evidence:** Complete `words\いる.md:4,15–35`; JMdict1577980 sense2, “to stay,” unrestricted readingいる, in `family-inspection-08.txt:97–103`. Complete `words\ストップ.md:4,9,16–23` and `words\立ち止まる.md:4,9,16–23`; corresponding complete families1071100 and1551350 in `support-comparison-reading.txt:34–37,624–627`. The exact とどまる heading is in `public-bodies.json:179–186`, not the separate とまる heading or historical cancellation senses. **Confidence: high.**

**F02 — Moderate; correctness / quiz exclusions — `words\整う.md:4,9`.**

The title’s `be ready` branch is an ordinary secondary meaning of **入る**, **良い**, and **いい**, but none is directly guarded. This is not an inference from the topics “entering” or “goodness”: the complete lexical records explicitly contain readiness senses. A question involving one of those words can therefore offer 整う’s title as a defensible competing answer.

**Minimal remedy:** Add exact IDs `入る`, `良い`, and `いい` to 整う’s exclusions without changing the articles’ titles, levels, or teaching scope. 良い/いい’s existing mutual guard does not protect either against 整う.

**Exact evidence:** Complete older bodies `words\入る.md:1–36`, `words\良い.md:1–46`, and `words\いい.md:1–35`. Complete JMdict1465590, readingはいる, sense12 “to be ready (of tea, coffee, etc.),” in `family-inspection-07.txt:60–75`; complete1605820 sense2 “ready; prepared,” with the explicit “also いい (all senses)” note, in `family-inspection-09.txt:111–118`. The fresh Jisho response also supplies the complete kana-only いい entry, whose second sense is “sufficient; enough; ready; prepared,” without a rare or obsolete restriction. **Confidence: high.**

**F03 — Moderate; correctness / quiz exclusions — `words\特長.md:4,9,16–21`.**

The pair **特長/機能** is unguarded. 機能’s complete title is `function; feature`; its “feature” branch can reasonably answer 特長 when a useful capability is being presented as a product’s favorable feature. 特長’s article itself defines the word as a “strong point, merit, or favorable feature.” 機能’s lack of an inherent positive evaluation does not prevent a useful 機能 from being a 特長.

**Minimal remedy:** Add exact ID `機能` to 特長’s exclusions. This recommendation is based on the pair’s own meanings, not on 特色’s existing guard or a transitive synonym clique.

**Exact evidence:** Complete `words\機能.md:4,15–23,40–45`, including its useful-camera-feature example; complete JMdict1221130, “function; facility; faculty; feature,” in `support-comparison-reading.txt:176–179`. Complete principal1455200 sense1 and the captured public 特長 definition support favorable/superior points. **Confidence: medium-high**, because the collision depends on the ordinary breadth of English “feature,” not exact synonymy in every context.

**F04 — Minor; scoped coverage / component navigation — three locations.**

Existing written components are substantively explained without links to their existing kanji cards:

| Location | Missing substantive link | Evidence |
|---|---|---|
| `words\とこや.md:23` | 屋 in the explanation of や and shop/occupation names | Complete `kanji\屋.md:10,20,29` |
| `words\整う.md:47–48` | 調 in the recognized 調う spelling | Complete `kanji\調.md:10`, including ととの.う |
| `words\留まる.md:31` | 止 in the recognized 止まる/**とどまる** spelling | Complete `kanji\止.md` header includes とど.まる |

**Minimal remedy:** Link the explained characters to those existing kanji cards at these passages. Keep the primary-spelling metadata unchanged: kana とこや remains `kanji: []`, 整う remains `[整]`, and 留まる remains `[留]`. Do not invent missing cards or additional mandatory reciprocal pairs.

The 屋 omission is inherited in the sentence touched by this patch, not newly introduced linguistic misinformation. The later word link to 止まる does not itself link the explained component to `kanji\止.md`. **Confidence: high.**

**F05 — Minor; correctness / inherited quiz omission — `words\飛ぶ.md:4,8–9,15–19`; `words\飛行.md:4,8–9,15–28`.**

The reused 飛ぶ card and older 飛行 card have no direct exclusion. Their complete titles, `fly; soar` and `flight; flying`, describe the same ordinary airborne activity; both complete bodies actually use an airplane flying as an example. 飛行 is also an intransitive する word, so a blanket noun/verb exemption would not resolve the answer ambiguity.

**Minimal remedy:** Add `飛ぶ` to **飛行’s** exclusions, leaving the required unchanged 飛ぶ article and its N5 identity untouched.

**Exact evidence:** The complete bodies cited above; complete JMdict1429700’s flying sense and complete1485450 sense1, “flight; flying; aviation,” with noun/する/intransitive POS, in `support-comparison-reading.txt:599–602`. The N2 跳ぶ/hopping mapping itself is correct. **Confidence: medium-high. This is inherited, not a batch regression.**

**F06 — Minor; correctness / inherited quiz omission — `words\止まる.md:4,8–15`; `words\止む.md:4,8–15`.**

Neither card excludes the other. 止む’s complete title `cease; let up` can answer 止まる’s ordinary cessation sense; conversely, 止まる’s `to stop, come to a halt` contains a valid “stop” answer for 止む. The complete older body explicitly teaches cessation of continuing phenomena, including sound—not merely a weather category association.

**Minimal remedy:** Add `止まる` to **止む’s** exclusions, preserving the reused N5 article’s identity and prior teaching.

**Exact evidence:** Complete `words\止む.md:15–32`; complete principal1310620 sense2 includes “to cease”; complete1310640 sense1 includes “to cease; to stop; to be over” in `support-comparison-reading.txt:337–340`. Guards through other stopping words do not transitively protect this pair. **Confidence: high. This is inherited, not introduced by the perching addition.**

## Optional

None. Exhaustive sense expansion, additional kanji-card creation, and stronger spelling distinctions are not required.

## Limits

- **Snapshot mechanics remain UNVERIFIED independently:** file tools cannot execute Git or recompute the supplied hashes/equivalence checks. Preservation judgments distinguish the visible patch/body evidence from those mechanical assertions.
- The nineteen positive frozen public captures are **one dictionary service**, not nineteen independent dictionaries or fresh reviewer retrievals. Mixed headings and historical material were separated from the applicable readings. The fresh Jisho lookup is another JMdict rendering, not an independent underlying dictionary.
- **とっくに’s frozen public endpoint failed to return a lexical body.** Its CLEAN teaching verdict rests on complete JMdict1320570, not a purported successful public retrieval.
- Compiler intent and exact raw-gloss-to-sense provenance were not independently recovered. Selected senses were treated as scoped mappings, not separate JLPT certifications for every recognized use.
- No live quiz was generated. Findings establish unguarded, defensible answer collisions under the documented pairwise behavior, not an observed question frequency. This was not an exhaustive whole-lexicon exclusion audit, corpus-frequency study, or native-speaker certification.
