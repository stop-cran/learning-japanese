Snapshot: `acf7297ef66a82f620a6c5551d95a2e3fa356bc7`, confirming changes from `b6020f9e490298de1756e33c51bf9ce314132f4e`. Reviewer: OpenAI GPT-family model; the exact serving model/version identifier is not exposed to me.

Scope:

Independent, blind, read-only confirmation. Every changed card was read completely, every patch hunk was checked against all four facets, and meaning/reading quiz evidence was examined for all fifteen batch cards.

**Confirmation packet files opened**

Paths below are relative to `C:\Users\romanko\n1-kanji-workspace\review-packets\confirm-138-gpt`.

- **Full text:** `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`.
- **Full text, `snapshot\kanji\`:** `垣.md`, `執.md`, `堅.md`, `塊.md`, `壊.md`, `奏.md`, `契.md`, `奪.md`, `妨.md`, `威.md`.
- **Full text:** `diffs\fix.patch`, `diffs\changed-files.txt`, `diffs\changed-lines.txt`. All ten revised files were also independently reconstructed from the patch and original files in memory; every reconstruction matched.
- **Full text, `checks\`:** `quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`, `link-targets.tsv`, `lint.txt`, `unittest.txt`, `validate.txt`, `budget.txt`, `vocabulary.txt`, `manifest.txt`. Large audits were inspected in bounded ranges.
- **Full text, `evidence\`:** `README.md`, `jmdict-cited-entries.xml`, `QuizBuilder.kt`, `kanjipedia-契.txt`, `weblio-押妨.txt`, `stroke-summaries.txt`, `meta-scan.txt`, `meta_scan.py`.
- **Selective substantive inspection plus full byte comparison:** `evidence\KanjiReadings.kt`, lines 1–125, and `evidence\Words.kt`, lines 163–end, including `ReadingOptions.mutations`. Both files were compared in full with their original-packet copies. `QuizBuilder.kt` was also compared in full.

**Original packet context reopened**

Paths below are relative to `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-138-b6020f9e`.

- **Read programmatically in full; selected content inspected:** `snapshot\kanji\噴.md`, `垂.md`, `垣.md`, `執.md`, `堅.md`, `塊.md`, `墨.md`, `壁.md`, `壊.md`, `奏.md`, `契.md`, `奨.md`, `奪.md`, `妨.md`, `威.md`. Used for exact patch reconstruction, metadata comparisons, batch-layout counts and checking the author's correction to my initial coverage notes; not a fresh full editorial rereview of every unchanged passage.
- **Metadata inspected:** `repo\kanji\魅.md`, `repo\kanji\組.md`, for reverse-direction exclusion checks.
- **Full JSON parsed, relevant geometry inspected:** `snapshot\strokes\威.json`, `snapshot\strokes\壊.json`.
- **Full TSV parsed, relevant titles inspected:** `titles\kanji-titles.tsv`.
- **Full XML parsed, eight entries compared:** `evidence\jmdict-families.xml`. Every new cited-entry extract exactly matched its original structured entry.
- **Full text comparison with revised audits:** `evidence\audits\quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`.
- **Full byte comparisons:** `evidence\app-code\QuizBuilder.kt`, `KanjiReadings.kt`, `Words.kt`.
- **Full captured text:** `evidence\public-source\weblio-妨.txt`.

Independent public checks inspected actual Jisho entries for 執り行う, 功を奏する and 緊い/かたい; Kanjipedia's 契 entry; Digital Daijisen's 押妨 and 威張る entries on Weblio; and the public KanjiVG 壊 SVG. No search snippet was used as verification.

Dispositions:

- **G1 — RESOLVED** — `垣.md:14,48` adds the direct 垣–壁 exclusion and accurate explanatory prose. The supplied builder applies it symmetrically. In-memory reproductions of `{垣, 壁, 噴, 契}` exclude the competing card in both target directions.
- **G2 — RESOLVED** — `奪.md:14,48` adds only 魅 to that card's exclusion list and accurately retains the attention-capturing sense. `{奪, 魅, 噴, 契}` excludes the competing card in both directions. 魅 remains an appropriate authored distractor for 塊.
- **OP — DECLINE ACCEPTED** — This was nonblocking presentation polish, not a factual defect. The claimed batch-local layout pattern is verifiable: nine cards contain the specified closing inventory wording, and all fifteen retain the practice-set disclaimer. Accepting the limited revision scope does not depend on the unverified published-corpus counts.
- **OR — RESOLVED, for case retention** — All eight latent cases remain explicitly recorded in the complete revised exposure audit, with unchanged substantive results. This satisfies retaining the cases as reference/regression material; it does not independently establish the author's claims about future execution schedules or closure notes.

Verdicts:

- **Correctness: CLEAN** — all ten revised cards and every changed hunk; no new factual defect established.
- **Scoped coverage: CLEAN** — additions are supported, existing reading coverage is preserved, and no new consequential omission established.
- **Consistency and quiz safety: CLEAN** — G1/G2 are fixed, the additional 塊–組 edge is justified, and no new collision established in the inspected meaning questions or audited reading pools.
- **Comprehensibility: CLEAN** — changes are intelligible for the stated audience; phonetic terminology is explained, and mnemonics remain explicitly modern-shape aids.

No card differs from these facet verdicts within this confirmation's scope.

**Changed-hunk regression checks**

- **垣, 塊 and 奪:** The three new exclusions are direct semantic pairs, not transitive expansions. Their quoted 壁, 組 and 魅 titles exactly match the unchanged title index. All twenty-one local kanji-link rows in the changed-line audit independently matched the title index and existing packet files. No exclusion overlaps the card's authored distractors. The added 塊–組 protection also worked in both directions in the restricted pool `{塊, 組, 噴, 契}`.
- **執:43,58:** 執り行う とりおこなう and “to hold (a ceremony); to perform” agree with pinned entry **1319610** and the [actual public entry](https://jisho.org/api/v1/search/words?keyword=%E5%9F%B7%E3%82%8A%E8%A1%8C%E3%81%86). The added citation is correct, and the example genuinely illustrates と.
- **堅:41:** Pinned entry **1257110** has four spellings, with 緊い specifically marked irregular kanji usage. The revision no longer calls 硬い and 固い the only other spellings. The [public dictionary response](https://jisho.org/api/v1/search/words?keyword=%E7%B7%8A%E3%81%84) also contains the relevant かたい entry; I did not confuse it with the separate きつい result.
- **壊:27; 威:33:** The 壊 description includes the complete lower 衣 shape, including its upper two strokes. Original stroke coordinates and the [public KanjiVG decomposition](https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/058ca.svg) corroborate it. 威's top horizontal is approximately 56.5 units wide versus 23.7 for the inner horizontal, supporting the revised relative-length wording. Neither revision claims historical etymology.
- **奏:31,59:** 功を奏する こうをそうする, “to succeed; to bear fruit,” agrees with pinned entry **2080870** and the [actual public entry](https://jisho.org/api/v1/search/words?keyword=%E5%8A%9F%E3%82%92%E5%A5%8F%E3%81%99%E3%82%8B). It illustrates the already-explained result sense without changing the selected reading.
- **契:43:** The [actual Kanjipedia entry](https://www.kanjipedia.jp/kanji/0001765100) lists outside-table キツ and ケツ, associates キツ with 契丹, prints キッタン, and gives 契闊 ケッカツ. The gemination explanation is supported. Pinned entry **2714430** confirms both きったん and けいたん. The paragraph does not misidentify the formation note's セツ as an ordinary reading listed there.
- **妨:25:** The original Daijisen character capture indeed lists both 妨害 and 押妨. The [actual 押妨 entries](https://www.weblio.jp/content/%E6%8A%BC%E5%A6%A8) support おうぼう, the landholding/violence/unjust-tax explanation and its historical qualification. This is not presented as a new common practice word.
- **威:44:** The on/kun account is consistent with イ plus voiced はる, while retaining the distinction for えばる. The [actual Daijisen entry](https://www.weblio.jp/content/%E5%A8%81%E5%BC%B5%E3%82%8B) separates い‐ばる and identifies えばる as its sound variant. No unsupported historical derivation is introduced.

**All fifteen cards: post-fix quiz check**

The meaning columns below identify the source cards; the actual English titles in `quiz-safety.txt` were assessed. All forty-five authored alternatives remain plausible but defensibly wrong, including ordinary secondary senses and reverse-direction consideration.

| Card | Meaning wrong-option cards | Reading prompt checked |
|---|---|---|
| 噴 | 口・古・買 | フン |
| 垂 | 郵・乗・重 | スイ |
| 垣 | 坂・城・埋 | かき |
| 執 | 報・幸・熱 | シツ |
| 堅 | 臣・監・基 | かたい |
| 塊 | 魅・城・場 | かたまり |
| 墨 | 墓・型・堂 | すみ |
| 壁 | 辛・基・坂 | かべ |
| 壊 | 均・埋・塔 | こわす; shared-stem handling of こわれる |
| 奏 | 春・天・実 | ソウ |
| 契 | 大・天・分 | ケイ |
| 奨 | 美・奥・奇 | ショウ |
| 奪 | 集・隼・雑 | うばう |
| 妨 | 姉・始・旅 | さまたげる |
| 威 | 成・歳・減 | イ |

Independent metadata comparison confirmed that only the three stated exclusion lists changed: no title, tag, metadata reading, practice selection or distractor list changed. All three supplied app sources are byte-identical to their original-packet copies.

The meaning-audit results are unchanged, apart from one removed blank line; therefore the author's literal “line for line” wording is slightly inaccurate but has no content or quiz consequence. Both reading audits differ only in their command headers.

The exposure audit still reports **0 production hits, 0 Starter padded-session hits, 0 one-holder padded hits and 8 latent collisions**. Those eight normalized-key cases remain 噴 ほん/はく, 塊 ほど, 壁 がけ, 契 きつ/けつ/せつ and 奪 とる. The narrower reading-options audit's two HIT labels, 噴 ほん and 契 けつ, do not account for already-filled curated slots. Checking the actual builder's tier order confirms that these labels do not establish drawable collisions in the audited shipped pools. 執's name-only し is not an ordinary on/kun alternative. 壊's two selected forms share a stem, explaining the single normally scheduled prompt.

Confirmation: **CONFIRMED** — G1 and G2 are resolved, the optional-point dispositions are acceptable as qualified above, and no new actionable defect was established.

Findings:

None.

Optional:

None new. The accepted OP decline does not turn the original presentation preference into a release requirement.

Limits:

- I correct my initial report's coverage prose: the old cards did **not** discuss 噴 ホン/はく, 壁 がけ, 墨 モク, 奪 タツ or 契 キツ/ケツ. Those were audit extras, not card text. I verified their absence in the original cards; the revised 契 paragraph now explicitly discusses キツ/ケツ. The audit's generic “card text” labels must not be used to infer that an extra actually appears in a card. This corrects my reporting, not a new card defect.
- The exposure/options tools themselves are not supplied here. I inspected their complete outputs and the relevant app mechanics, but did not independently rerun their whole-pool enumeration or execute Kotlin. Seeded simulations are not exhaustive: some reachable candidates were not observed in the sampled seeds, and some printed candidate lists are abbreviated.
- Audit safety is bounded to the stated frozen inputs, extra-reading list, shipped-stack and padded-session pools, and four-choice behavior. It does not certify every dictionary reading, hypothetical pool, future quiz size or changed client.
- The link audit covers local kanji targets and quoted titles, not semantic truth or all external URLs. The metadata scan excludes kana-only words, single-kanji words and substring-only matches; its helper dependency is absent, so I read rather than ran it. New lexical claims and citations were checked directly.
- Future per-batch/pre-publication execution, closure-note retention and the OP counts for published cards outside this batch were not independently verified. They were not used as proof of current card correctness.
- Test logs report 436 passing tests and other successful checks; I did not rerun them, inspect an external checkout/manifest, certify Git ancestry, run Android/JVM tests or test a phone. Those known packet limits are not new findings.
- Stroke geometry was checked against original packet data and independently corroborated for 壊 with live KanjiVG; no animation/device-rendering certification is claimed.
- All tool calls were serial, with no parallel-call violation, sub-agent, background job, other session, recursive listing or corpus scan. One initial combined read exceeded the output limit; I did not open its tool-managed spill path and recovered the relevant contents through bounded reads. No other reviewer's report was accessed. The only intended persistent change is this report.
