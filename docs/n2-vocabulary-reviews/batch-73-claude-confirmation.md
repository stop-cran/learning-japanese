# Batch 73 correction confirmation (claude-opus-5.5)

All four of my original findings are resolved. No regressions or remaining actionable defects were found. All twenty source rows are CLEAN on every facet.

## Snapshot

- **Revised commit:** `125bbe21d9696d59a99ee978efe01de8146ec6e3`
- **Parent:** `4abf8105090403e90d2a950b90a733cd538d1424`
- I reviewed committed content only. My file tools cannot run Git, so the snapshot identity, manifest, hash and preservation checks were run by the author, not by me.

## Scope

**Model:** claude-opus-5.5, claude family. I made no edits and used no agents, delegation or shell.

**Read completely in this round:**
- The correction snapshot, `correction.patch` and the reconciliation JSON.
- `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md` lines 18-103.
- All 20 current articles.
- All 8 kanji bodies: 瓶, 詰, 則, 普, 副, 詞, 複, 含.
- The TSV header (line 1) and rows 1442-1461 only.
- The mappings, principals (20 families, 29 senses), components and labels JSONL files.
- `correction-comparison-reading.txt` (21 families).
- `public-bodies.txt`. I picked out the assigned ふくめる heading and kept it separate from the くくめる heading.
- 12 older bodies: 進む, 強化, 加わる, 広がる, 広げる, 広める, 拡大, 展開, 流行る, でたらめ, かわいそう, 乾燥.

**Not read:**
- `docs\confusable-words.md` was only searched; it had no matches for these words.
- `docs\jlpt-levels.md`.
- The three optional private JSON files: corrected-review-evidence, correction-completed-inspection and public-bodies.json.
- I did no new web fetches. The pages I fetched in the first round (jisho for 流行る and 出鱈目, kotobank for 含める) are carried over, not re-fetched.

The author's totals (238 families, 108 older bodies) are not my actual scope.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1442 | ピンク | CLEAN | CLEAN | CLEAN | Blank source spelling kept; sense 2 is extra recognition only |
| N2:1443 | 便箋 | CLEAN | CLEAN | CLEAN | 箋 stays in metadata, not linked |
| N2:1444 | 瓶詰 | CLEAN | CLEAN | CLEAN | B73-01 fixed at :48-50; source spelling 瓶詰 kept |
| N2:1445 | ファスナー | CLEAN | CLEAN | CLEAN | Blank source spelling kept |
| N2:1446 | 風船 | CLEAN | CLEAN | CLEAN | Dated sense 2 is extra recognition only |
| N2:1447 | 不運 | CLEAN | CLEAN | CLEAN | B73-04 fixed |
| N2:1448 | 増える | CLEAN | CLEAN | CLEAN | Unchanged existing N4 article; teaches 殖える |
| N2:1449 | 深まる | CLEAN | CLEAN | CLEAN | N273-02 additions supported |
| N2:1450 | 不規則 | CLEAN | CLEAN | CLEAN | B73-03 fixed |
| N2:1451 | 普及 | CLEAN | CLEAN | CLEAN | B73-02 / N273-04 fixed |
| N2:1452 | 付近 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1453 | 拭く | CLEAN | CLEAN | CLEAN | Optional 乾燥 exclusion adopted |
| N2:1454 | 副詞 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1455 | 複写 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1456 | 複数 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1457 | 含める | CLEAN | CLEAN | CLEAN | Senses 1-2 taught, 3-5 extra; くくめる heading not used as evidence |
| N2:1458 | 膨らます | CLEAN | CLEAN | CLEAN | N273-03 additions supported |
| N2:1459 | 膨らむ | CLEAN | CLEAN | CLEAN | N273-03 additions supported |
| N2:1460 | 不潔 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1461 | 更ける | CLEAN | CLEAN | CLEAN | Seasonal use is public-dictionary recognition, not an invented sense |

**Eight kanji edits: CLEAN.** All nine reciprocal pairs appear in the reading tables and common-word lists with the correct whole-word readings, and each footer cites the right dictionary entry:
- 瓶/瓶詰 and 詰/瓶詰 (びんづめ, 1491130)
- 則/不規則 (1491840)
- 普/普及 (1497110)
- 副/副詞 and 詞/副詞 (1500440)
- 複/複写 (1501390) and 複/複数 (1501400)
- 含/含める (ふく.める, 1216890)

Kanji headers and examples are unchanged. The missing characters 箋, 殖, 及, 拭, 膨 and 潔 stay as plain metadata with no invented cards.

**Mappings: CLEAN.** All 20 TSV rows match the mapping JSONL, including the selected and additional senses, the blank ピンク and ファスナー spellings, and 殖える→増える at N4.

**Baseline preservation: CLEAN.** 増える is not among the changed files, and my reread found it intact: N4, ふえる, the same title, [増], the 殖える note, no exclusions and dictionary entry 1602440.

## Findings

**My original findings:**
- **B73-01 (same as N273-01) — RESOLVED.** 瓶詰.md:48-50 now reads "Learn the voiced ending: びんづめ, not びんつめ." The false long-vowel claim is gone. High confidence.
- **B73-02 (part of N273-04) — RESOLVED.** 普及.md:9 adds 流行る. Dictionary sense 1552310:2 ("be prevalent; spread widely") and the 流行る body's disease use support it. Medium-high confidence.
- **B73-03 — RESOLVED.** 不規則.md:9 adds でたらめ. Both words share the gloss "unsystematic" (1491840:1 and 1339630:2), and the でたらめ body teaches でたらめに並べる. Medium-high confidence.
- **B73-04 — RESOLVED.** 不運.md:9 adds かわいそう. The overlap is in the かわいそう title itself ("pitiable; unfortunate") and its body example かわいそうな人, "an unfortunate person", not copied from 気の毒's exclusions. Low-medium confidence that the pair is needed, but it is valid.

**N273 dispositions (not my original findings):**
- **N273-02 — ACCEPTED** (深まる.md:9):
  - 強化: its body explicitly teaches "intensification", and 1236200:1 includes "intensifying". Medium-high confidence.
  - 加わる: its body teaches 暑さが加わる, "the heat intensifies" (1189980:3). Medium confidence.
  - 進む: its title and body don't teach this meaning, but its ordinary secondary sense 1365980:4 is literally "intensify; heighten; deepen". Medium confidence.
  - The unrelated すさむ entry (1984310) was not used.
- **N273-03 — ACCEPTED** (膨らむ.md:9, 膨らます.md:9), six direct pairs:
  - 広がる: the Daijisen definition of 膨らむ sense 2 itself uses 広がって. Medium-high confidence.
  - 広げる: 1602370:1 includes "expand; enlarge". Medium confidence.
  - 広める: 1278460:2 includes "broaden; enlarge", and its body teaches 知識を広める. This is the weakest pair but is a defensible "expand"/"enlarge" overlap, not an established excess. Low-medium confidence.
  - None of these are inferred through 拡大.
- **N273-04, the 拡大 and 展開 parts — ACCEPTED:**
  - 拡大: 1205200:3 "spread", and its body teaches 被害が拡大する ("damage spreads"). Medium confidence.
  - 展開: 1440600:2 "spreading out", and its body covers deployment over an area. Medium-low confidence.

**Other items:**
- **Optional 拭く/乾燥 — ADOPTED, acceptable.** The labels overlap directly ("dry by wiping" vs "drying"), and the 乾燥 body teaches transitive 木材を乾燥します. The pair does not claim that all drying is wiping.
- **Other optional items — DEFERRED.** Still nonblocking.
- **Regressions:** none. The fix adds exclusions only and removes nothing. Every added target is an existing article, and no list has duplicates.
- **Remaining actionable defects:** none.

## Optional

These remain nonblocking and were deferred:
- 瓶詰 as a product noun.
- A register note for 複写.
- 普及に努める.
- 複数形.
- 含める set-phrase frequency (unverified).

## Limits

- No Git: all identity and hash checks were run by the author.
- All public definitions come from one authority (Digital Daijisen via Weblio). I did no new fetches this round.
- I did not read the three optional private JSON files, and I only searched `confusable-words.md`.
- How strongly the exclusion pairs are needed (especially 膨らむ/広める and 普及/展開) is a judgment call with low-to-medium confidence.
- This review does not guarantee exhaustive correctness, native-speaker naturalness, frequency claims or runtime quiz behaviour.
