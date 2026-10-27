# Batch 77 confirmation review against the corrected snapshot (claude-opus-5.5)

## Snapshot
- **Revised commit:** a6e1243882b1393de5fabdf9bab9dff65449e4d5. **Parent:** d30143529a24516ba47ea82f15c0c3d66a1a98ad.
- I reviewed committed content only (`cleanCommittedContent: true`).
- My file tools cannot run Git. The snapshot, hash, preservation and coverage-index claims were checked by the author, not by me.

## Scope
**Reviewer:** claude-opus-5.5 (claude family). I made no edits. I used no agents, delegation, shell or public fetches in this pass.

**Process deviations:** I read most files one at a time. Two batches broke the serial-read rule:
- The twenty article reads, sent as one batch earlier in this pass.
- 対策 and 広々 were read separately, but ストップ and ブレーキ were read together.

All reads returned complete content.

**Read completely in this pass:**
- **Correction files:**
  - correction snapshot, correction.patch and reconciliation.
  - The two instruction files and `docs\content-format.md` lines 18–103.
- **Articles and kanji:**
  - All twenty current articles. I reread 包帯, 方針 and 膨大 afterwards to get exact line numbers.
  - All eight kanji bodies.
- **Compact records:**
  - Original and corrected mappings (20 each).
  - Principals (20 families / 28 senses).
  - 34 component records and 268 navigation labels.
- **TSV:** the header (`[1,1]`) and rows `[1522,1541]` only.
- **Five evidence files:**
  - Correction comparison: 13 families / 19 senses, keeping modern 広々 (1602380, ひろびろ) separate from archaic 2588680 (こうこう).
  - Two ALC/EDP captures, treated as one authority.
  - Supplemental comparison: 3 families / 6 senses.
  - Twenty-two Daijisen-via-Weblio captures, also one authority.
- **Six older bodies:** 対策, 広々, 小包, 支配, ストップ and ブレーキ.
- **Optional file:** `correction-completed-inspection.json`.

**Totals this pass:** 30 distinct families / 45 senses, and 6 older bodies.

**Not read this pass:**
- `related.patch`, which was not on this pass's list.
- The two other optional files.
- The raw batch-77 packet, which is forbidden.
- `docs\n2-vocabulary-snapshot.json`.
- The JMdict families for ヘリ (1118730) and お坊さん (1612830).
- Most of the 497 prepared families. The author's 310-family union is not my scope.

**Carried over from my original review:** my `related.patch` preservation assessment, and the 小包, 対策 and 広々 bodies.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1522 | 別荘 | CLEAN | CLEAN | CLEAN | Unchanged; villa sense plus the qualified colloquial "prison" sense |
| N2:1523 | 別々 | CLEAN | CLEAN | CLEAN | Added line "Before a verb, use 別々に" is accurate |
| N2:1524 | ベテラン | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1525 | ヘリコプター | CLEAN | CLEAN | CLEAN | Daijisen supports the short form ヘリ; JMdict 1118730 not read (Limits) |
| N2:1526 | 編集 | CLEAN | CLEAN | CLEAN | Unchanged; links to 編 both ways |
| N2:1527 | 便所 | CLEAN | CLEAN | CLEAN | Deferring stronger トイレ-as-default wording is acceptable |
| N2:1528 | ペンチ | CLEAN | CLEAN | CLEAN | Simpler scissors comparison is accurate |
| N2:1529 | 望遠鏡 | CLEAN | CLEAN | CLEAN | Unchanged; 鏡 stays plain text (no kanji card) |
| N2:1530 | 方角 | CLEAN | CLEAN | CLEAN | Unchanged; ほうがく, senses 1–3 |
| N2:1531 | 箒 | CLEAN | CLEAN | CLEAN | Unchanged; reading ほうき, not historical ははき |
| N2:1532 | 方言 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1533 | 坊さん | CLEAN | CLEAN | CLEAN | Unchanged; 1612830 not read (Limits) |
| N2:1534 | 防止 | CLEAN | CLEAN | CLEAN | "Noun naming the unwanted event" wording adopted; guards unchanged |
| N2:1535 | 方針 | CLEAN | CLEAN | CLEAN | 対策 guard and comparison prose added |
| N2:1536 | 包装 | CLEAN | CLEAN | CLEAN | No 小包 guard; agreed |
| N2:1537 | 法則 | CLEAN | CLEAN | CLEAN | No 支配 guard; agreed |
| N2:1538 | 包帯 | CLEAN | CLEAN | CLEAN | B77-01 resolved |
| N2:1539 | 膨大 | CLEAN | CLEAN | CLEAN | 広々 guard and comparison prose added |
| N2:1540 | 包丁 | CLEAN | CLEAN | CLEAN | B77-02 resolved; raw 庖丁 preserved |
| N2:1541 | 方程式 | CLEAN | CLEAN | CLEAN | Unchanged |

- **Mappings: CLEAN.**
  - The corrected and original mapping files differ only in the identity note for N2:1540.
  - TSV row 1540 matches the corrected note. Raw 庖丁, ほうちょう, the gloss, entry 1515530, the article, level, sense 1 and `draft` status are all preserved.
- **Component links: CLEAN.**
  - Existing cards are linked.
  - 荘, 鏡, 坊, 膨, 丁 and 箒 stay plain text, with no invented cards.
- **Ten reciprocal N2 pairs: CLEAN.** All ten are present in both directions:
  - 編集 ↔ 編, 方角 ↔ 角, 防止 ↔ 防, 方針 ↔ 針
  - 包装 ↔ 包, 包装 ↔ 装, 法則 ↔ 則
  - 包帯 ↔ 包, 包帯 ↔ 帯, 包丁 ↔ 包
- **Baseline preservation: CLEAN within scope.**
  - The correction patch touches no kanji or older word file.
  - The current kanji bodies match my original reads, including the added dictionary IDs (包, 帯, 装 and 角).

## Findings
- **B77-01 — RESOLVED.** `words\包帯.md:15-21,37-40`
  - The 腕を包帯する example and the unqualified production claim are gone.
  - The article now teaches 包帯をする and 包帯を巻く, says に marks the body part and を marks the bandage, and frames 包帯する as JMdict's transitive-verb listing to recognize.
  - The ALC capture supports this: 包帯をする "apply… wear a bandage", 腕に包帯をする "have a bandage around one's arm", and (人)の腕に包帯する.
  - Daijisen defines 包帯 as cloth that is 巻く'd around a wound.
  - Confidence: high.
- **B77-02 — RESOLVED.** `docs\n2-vocabulary-sources.tsv:1540` now reads "share entry 1515530 and reading ほうちょう". Confidence: high.
- **方針 / 対策 — RESOLVED: guard justified.** `words\方針.md:9,35-37`
  - The glosses overlap: 方針 "plan (of action)" against 対策 "measure… strategy".
  - The added prose ("対策 foregrounds the issue") matches the 対策 body.
- **膨大 / 広々 — RESOLVED: guard justified.** `words\膨大.md:9,34-36`
  - JMdict glosses both 1602380 sense 1 and 1603660 sense 1 as "extensive". That shared gloss supports the guard more strongly than the reconciliation's title-based reasoning.
  - The archaic こうこう entry is kept separate.
- **包装 / 小包 and 法則 / 支配 — my concerns WITHDRAWN.**
  - 小包 is the packaged item. 包装 is the act of wrapping or the outer wrapper.
  - None of 支配's four senses matches 法則; the overlap is only the English word "rule".
- **防止 / ストップ and 防止 / ブレーキ — WITHDRAWN; guards kept.**
  - ブレーキ sense 2 means a check on a development or behavior, which supports the 防止/ブレーキ guard.
  - The 防止/ストップ guard is weaker but defensible: stopping something from happening overlaps with prevention. Nothing shows the guard is excessive.
- **teachingSpelling — my original "private-only" claim WITHDRAWN.** I cannot inspect the forbidden packet to confirm the field is committed. The described meaning (a source alias to recognize) is consistent with the mapping and the article.
- **Kanji-summary erratum — ACCEPTED.** My "links only" description of 編, 防, 針 and 則 was imprecise; reading-row examples were also present. The actual patches control.
- **Three optional prose changes:** all adopted correctly.
- **Deferred items:** the wasei note, トイレ-default wording and sense-number spacing are acceptable to defer. Correction to the reconciliation: the frozen JMdict 1121520 record carries `ls_wasei: y`, so a wasei note is supported by one authority. It is still optional.
- **Regressions:** none found.
- **Remaining actionable defects:** none.

## Optional
- A wasei note on ペンチ could cite JMdict's `ls_wasei` flag.
- The 包帯 usage link points to a dynamic ALC search page. A stable entry page would be more durable.

## Limits
- No exhaustive correctness, native-speaker certification, frequency claims or runtime quiz guarantees.
- The ALC evidence is one EDP authority and shows attestation, not frequency. Whether 腕を包帯する is natural remains unverified, but it is no longer taught.
- I did not read the JMdict families for ヘリ (1118730) or お坊さん (1612830).
- The 精選版 entry was not a frozen capture, and I did not read it in this pass.
- I did not reread `related.patch` or the snapshot JSON. Hash and coverage-index checks are author-executed.
