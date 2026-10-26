## Snapshot
- **Revised commit:** 228808f262a9503b525a4eac2fbe449611f4e58c
- **Parent:** c1563f9c47fa9af139ef149893b4c5e4e9be3317
- I assessed committed content only. File tools can't run Git, so the snapshot, hash and preservation claims were checked by the author, not by me.

## Scope
**Model:** claude-opus-5.5 (Claude family). I made no edits and used no agents, delegation or shell.

**Fresh complete reads in this pass:**
- **Snapshot and correction files:** the correction snapshot, `batch-76-correction.patch` and the reconciliation JSON.
- **Guidance:** `.github\copilot-instructions.md`, `content-structure.instructions.md` and `docs\content-format.md` lines 18–103.
- **Assigned content:** all 20 assigned articles and the five kanji bodies (芸 布 量 並 兵).
- **JSONL files, in bounded ranges:** all 20 mappings, 20 principal families (36 senses), 31 component records and 248 labels. The labels are navigation only, not full-body reads.
- **TSV:** row [1,1] plus physical rows [1502,1521].
- **Comparison readings:** the correction file (10 families, 21 senses) and the qualification file (8 families, 15 senses), totalling 18 families, 36 senses and 17 forms. The supplement adds 8 families and 18 senses.
- **Public bodies:** `public-bodies.txt` through EOF.
- **Older bodies, read completely:** 道具, 器具, 文学, 終える, 仕舞い, しまう, 一度に, 損害, 閉める, 閉まる.
- **Distinct family coverage this pass:** 41 families and 84 senses.

**Targeted checks:**
- I reread 並行 in full again.
- I grepped the front matter of 凹む, 閉会, 噴水, 文献 and 文芸.
- I grepped `words\` for titles containing fountain, spring, jet or spout, and for any reverse exclusions of the eleven changed words.

**Inherited from my original session:** `frozen-snapshot.json`, `related.patch`, the 別 body, and earlier web fetches. Those fetches were Wiktionary/Lexico, plus failed retrievals (Merriam-Webster 403, Cambridge 520), which count as limits, not evidence.

**Not read:** `corrected-review-evidence.json`, `correction-completed-inspection.json` and `public-bodies.json`. I made no fresh public fetch in this pass.

**Disclosure:** the TSV header and row views were issued together in one batch, not strictly one at a time. The content read is unaffected.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1502 | 文芸 | CLEAN | CLEAN | CLEAN | Contrast with performance is now direct; excludes 文学, 芸術 and 芸能. |
| N2:1503 | 文献 | CLEAN | CLEAN | CLEAN | 文学 guard added; no automatic clique with 文芸. |
| N2:1504 | 噴水 | CLEAN | CLEAN | CLEAN | Title is now "fountain; water jet"; 泉 guard and explanation kept; no title collision. |
| N2:1505 | 分数 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1506 | 文体 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1507 | 分布 | CLEAN | CLEAN | CLEAN | Dictionary wording supported by Daijisen 「また、あちこちに置くこと」. |
| N2:1508 | 文房具 | CLEAN | CLEAN | CLEAN | Category-only guards removed; comparisons kept. |
| N2:1509 | 文脈 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1510 | 分量 | CLEAN | CLEAN | CLEAN | Now reads 分量が多い; additional sense 1504430:2 stays recognition only. |
| N2:1511 | 分類 | CLEAN | CLEAN | CLEAN | によって分類する vs によるの分類 is now explicit. |
| N2:1512 | 閉会 | CLEAN | CLEAN | CLEAN | 終える, 仕舞い and しまう guards added. |
| N2:1513 | 平気 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1514 | 並行 | CLEAN | CLEAN | CLEAN | 一度に guard added; 平行 concurrency (2835826 sense 2) confirmed. |
| N2:1515 | 平日 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1516 | 兵隊 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1517 | 平凡 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1518 | 平野 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1519 | 凹む | CLEAN | CLEAN | CLEAN | 損害 guard added; 窪む 1246840 is physical only. |
| N2:1520 | 臍 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1521 | 隔てる | CLEAN | CLEAN | CLEAN | Explains が barrier + を separated things vs を隔てて. |

**Separate assessments:**
- **Mappings — CLEAN:**
  - All 20 match the TSV rows unchanged: level 2, same entries and senses.
  - 凹む (1179200) and 臍 (1571170) keep their stable filenames.
  - 分量 keeps 1504430:2.
  - 隔てる keeps the raw gloss "to be shut out".
- **Component links — CLEAN:** existing cards are linked; 献 噴 房 脈 隊 凡 凹 臍 隔 remain metadata only, with no invented links.
- **Reciprocal N2 pairs — CLEAN:** all five are intact (文芸/芸, 分布/布, 分量/量, 並行/並, 兵隊/兵) with their footer IDs.
- **Baseline preservation — CLEAN within patch scope:** the patch touches only the eleven new word articles; no kanji or older words changed.

## Findings
**My original findings:**

| ID | Disposition | Basis |
|---|---|---|
| B76-F1 (噴水 title) | Resolved | `words\噴水.md:4,12`; Daijisen sense 2 (装置…噴泉); 泉 guard at line 9 with explanation at line 29; no title collision. |
| B76-F2 (隔てる を) | Resolved | `words\隔てる.md:18-21`; matches Daijisen senses 1, 2 and 4. |
| B76-F3 (文芸 wording) | Resolved | `words\文芸.md:32-34`. |
| B76-F4 (文献/文学) | Resolved | `words\文献.md:9`; JMdict 1505330 sense 1 "literature" against 文学's title "literature". |
| B76-F5 (閉会/仕舞い), shared with GPT-F03 | Resolved | 仕舞い = JMdict 1594530 sense 1 (end, close, finish); kept separate from the じまい suffix (2582570). |
| Optional claim that "be shut out" was absent from the source | Withdrawn | My error: the raw source gloss is exactly "to be shut out". |

**GPT findings:**
- **GPT-F01 — Resolved (agree).**
  - 道具 ("tool; implement") and 器具 ("utensil; tool; apparatus") are generic categories that contain stationery; they are not equivalent answers to it.
  - Neither body teaches a stationery sense, and no older article declares 文房具 in reverse.
- **GPT-F02 — Resolved.**
  - Supported by Daijisen 「五十音順に―する」.
  - I relied on the author's Bunpro read and did not fetch it myself.
- **GPT-F03 — Resolved.**
  - 終える sense 1 ("bring to an end") matches Daijisen 閉会 「また、終えること」.
  - しまう's title includes "finish", and its body teaches standalone transitive finishing and closing a business, not only the auxiliary.
- **GPT-F04 — Resolved.**
  - English "all at once" also has a simultaneity reading that overlaps "concurrency".
  - 一斉 and 同時 are already excluded.
- **GPT-F05 — Resolved.**
  - 凹む teaches suffering a loss (Daijisen sense 3 損をする).
  - 損害 has a financial-loss example, and 損 is already excluded.

**Optional items and regressions:**
- **Optional items adopted:** 分布, 分量 and 並行 prose.
- **Deferrals accepted:** the 布 note, extra examples, and 閉会 guards against 閉める/閉まる.
- **Withdrawn:** my earlier moving vs proceeding mismatch.
- **Regressions:** none.
- **Remaining actionable defects:** none.

## Optional
- **並行 line 34:** "the two spellings" could say "the separate 平行 entry". Line 36 already makes the identity clear.
- **分布 line 39:** "Dictionary definitions" rests on one authority, and "examples" is plural although only one is locational.
- **閉会 vs 閉める/閉まる:** a guard could be reconsidered. The repository's 終了 and 締め切る pages exclude both, but judged pair by pair these bodies don't teach event closing.

## Limits
- I couldn't execute Git or hashes.
- All the Japanese public evidence comes from one authority (Daijisen via Weblio).
- The 248 labels are navigation, not full-body reads.
- There's no native-speaker, frequency or runtime quiz-behaviour guarantee.
