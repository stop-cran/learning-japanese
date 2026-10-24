# Batch 35 correction confirmation (claude-opus-5.5)

## Snapshot
- **Corrected commit:** `5d8e436a121ad5007143f771f76c3fcdff0a981e`.
- **Parent:** `978aed9979689800a07e505bf370846e4c3cc12c`. The receipt sets `cleanCommittedContent: true`.
- **Scope:** committed content only.
- **Not independently verified:** I have file tools only, so I could not run Git or compute hashes. The commit identity, the patch and evidence hashes, the new TSV hash, and the claimed equivalence of the derivative files all rest on the author's receipt.

## Scope
**Model:** claude-opus-5.5 (claude family), resuming my original blind-review session.

**Read in full:**
- Patch lines 2536 to the end: the snapshot JSON hunk, the TSV row 701 hunk, and all eleven article hunks.
- All eleven changed articles in their current form.
- `words\棒.md`.
- `batch-35-corrections-comparison-reading.txt` (26 families).
- `batch-35-corrections-existing-comparison-cards.txt` (all 19 cards).
- Evidence lines 30870–30888 and 32851–33405. These cover the provenance, the 18 new labels, the inspected-article list, the receipts, the public observations, the 13 added pairs and the 90 current declarations.
- The original records for 1519750 (棒), 1421490 (地味) and the 1594520 (絞る) sense layout.
- `words\地味.md`, reread to reassess Q3.
- TSV rows 685, 698 and 701.

**Fetched and inspected the actual pages:**
- WURK's しみじみ article: the noun-modification section and the section cautioning about しみじみする.
- Kotobank 尻尾: the Seisen しっぽ entry, sense ④.

**Not read:**
- Patch lines 121–2535, which are the appended part of `batch-35.json`. I used the allowed derivative files instead.
- The full JSON form of the 26 families (evidence lines 30888–32850). The compact rendering covers the same families, but their equivalence is the author's claim.

**Carried forward without rereading:** six untouched new cards (執筆, 実物, 失恋, 指定, 私鉄, 縛る), the five related edits, and 17 of the 20 mappings.

**Exposure note:** the assigned evidence file includes the author's adjudication list and a "modelContributionComparison" section. These cite the other family's finding IDs. I did not read the other family's reports, and my judgments below are independent of those IDs.

## Verdicts
**The eleven changed articles** (correctness / scoped coverage / comprehensibility):

| Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| しっぽ | CLEAN | CLEAN | CLEAN |
| 実用 | CLEAN | CLEAN | CLEAN |
| 実力 | CLEAN | CLEAN | CLEAN |
| 実例 | CLEAN | CLEAN | CLEAN |
| 地盤 | CLEAN | CLEAN | CLEAN |
| しびれる | CLEAN | CLEAN | CLEAN |
| 紙幣 | CLEAN | CLEAN | CLEAN |
| 絞る | CLEAN | CLEAN | CLEAN |
| しみじみ | CLEAN | CLEAN | CLEAN |
| しぼむ | CLEAN | CLEAN | CLEAN |
| 縞 | CLEAN | CLEAN | CLEAN |

**The seven unchanged new cards:**
- 執筆, 実物, 失恋, 指定, 私鉄 and 縛る: CLEAN on all three facets, carried forward.
- 地味: correctness stays **NEEDS FIX (Q3)** after reassessment; coverage and comprehensibility stay CLEAN.

**Related edits:** the three kanji edits (筆, 恋, 鉄) and the two reuse claims (湿度, 児童) are carried forward as CLEAN. The patch touches no kanji or reused article.

**Mappings:** all 20 are now CLEAN.
- Earlier exceptions resolved:
  - N2:685 (しっぽ): C2.
  - N2:698 (絞る): C3, via the article.
  - N2:701 (しみじみ): the TSV note is clarified.
- No change to source identities, sense indices or levels: the TSV note is the only row text that changed.

**Totals:** I confirmed 90 directional declarations across the eighteen new cards (77 + 13), with no removals.

## Findings
**My original findings:**
- **C1 (しみじみ "do not add する" warning): Resolved, narrowed.**
  - しみじみ.md:37 now teaches しみじみとした気持ち with its reading and gloss, and keeps a hedged caution about adding する.
  - The WURK page explicitly gives 「しみじみとした気持ち」 and calls verb use "あまり一般的でなく" (not very common).
  - I withdraw my earlier "very common" wording: a Weblio count of 30 example sentences does not measure frequency.
  - TSV row 701 is consistent with the article.
- **C2 (しっぽ lacks a non-animal tail-end example): Resolved.**
  - しっぽ.md:23 now has 列のしっぽ, cited at line 42.
  - Seisen sense ④ (順位の末のほう) gives 「列の尻っぽ」 (嘉村礒多, 1928). This is separate from the しりお headings on the same page.
- **C3 (絞る extortion sense neither taught nor excluded): Resolved.**
  - 絞る.md:52 now names extortion/exploitation as outside the introduction.
  - 1594520:4 is "to extort; to exploit", and senses 11–13 are the bow, sumo and go uses.
- **Q1 (紙幣/金銭), Q2 (地盤/基, 基本), Q4 (しびれる/凍える) and Q5 (しみじみ/感激, 感動): Resolved.** Each pair is now at line 9 of its card, and the actual titles support each guard.
- **Q3 (地味/謙虚): Unresolved, maintained.**
  - Severity: Minor. Facet: correctness (quiz guard). Location: 地味.md:9 and :23.
  - The author's rationale, "unshowy appearance/living", leaves out 地味.md:23's own "modest, reserved, or unobtrusive manner of living **or behaving**" and its gloss "live modestly".
  - The source entry 1421490:2 reads "reserved (behaviour, attitude, etc.); modest; quiet; unobtrusive".
  - 謙虚's title is "modest; humble". Its own card concedes that English can call a modest dwelling "humble", which is exactly the unshowy-life reading that 地味 teaches.
  - The correction accepted 実用/用いる and 紙幣/金銭 on overlap at this coarse level of English labels. The same standard applies here.
  - Remedy: add 謙虚 to 地味's `quiz_exclusions`.
  - Confidence: moderate-high.

**My original optional items:**
- **Resolved:** 実力/勢い (実力.md:25 already qualifies "coercive force"), 実例/ケース and 場合, and the wording polish (しぼむ.md:23, 紙幣.md:33, しびれる.md:33–35).
- **Withdrawn:**
  - 縞/棒: 縞.md:37 now explains the link. 棒.md:34 already teaches the line/dash sense, and 1519750:2 is "line; dash".
  - 実例/事件: 1313830 has no example or instance sense, and "actual example" in 実例's title rules out the incident reading.
  - 執筆/文字: "written character" leads 文字's title, and 1505390 has no authoring sense.
  - 地味/原・野: "open field" rules out the landscape reading.
  - 縛る/不自由: 1492680 lists states (discomfort, lack, impairment), not an act of binding.

**New regressions from the correction:** none. The new examples, readings, glosses and citations are accurate, and the 13 new guards are supported by the actual titles and senses without being excessive.

## Optional
- **しびれる/感激:** this would parallel the existing しびれる/感動 guard, since 感激's card glosses 会えて感激 as "thrilled". The two share no tags, so they would rarely be drawn together. Nonblocking.
- **しみじみ.md:37:** could say plainly that standalone しみじみする is uncommon, and that a subdued or gloomy mood is expressed with しんみり(と)する (per WURK).
- **TSV N2:698 note:** could mention the extortion sense alongside bow/sumo/go. The indices already leave out sense 4.
- **Still optional:** an electric-shock example for しびれる, and the idioms しっぽを出す and しっぽをつかむ.

## Limits
- Commit identity, hashes and derivative equivalence are author-verified only.
- The eight cards not changed in this commit (the seven new ones plus 棒) were not checked for any later edits. I relied on the patch's file list.
- The verdicts carried forward rely on my initial review, not a fresh inspection.
- No quiz draws were executed, and this is not native-speaker certification.
- **Consequential unresolved claim:** Q3 (地味/謙虚).
