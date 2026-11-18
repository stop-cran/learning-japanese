# B112 independent blind initial review

## Snapshot

- Candidate: `d6ad96ebf7d0352d54184ed44a382f70e4497f7b`.
- Base: `0320ba4a199432374096360e984b7dc5754dd6bc`.
- Execution model: GPT-6.1 Sol, model ID `gpt-6.1-sol`, as identified by the serving runtime. An independent provider-side execution trace was not available.
- Packet: `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-112-d6ad96eb`.
- Verified `SHA256SUMS.json` SHA-256: `22dc9721a0dc9bd2d4e1e94a4cf7cc74cc4137ac017a435f78a17787089c2288`. All 6,392 listed packet-file digests matched.

This is one initial review, not a confirmation round. No fixes were implemented.

## Scope

Read `REVIEW.md`, both supplied rubric files, the applicable content-format contracts, packet inventory and source/provenance mappings. Inspected the complete shared changed-content scope:

- All fifteen new kanji articles: 健 妙 射 就 展 微 態 盤 看 至 診 酸 障 離 響.
- All fifteen generated stroke references against their actual pinned KanjiVG SVGs.
- The entire existing-file diff and all 44 affected word articles, including all 45 added word-to-kanji links.
- The complete existing 基, 素 and 鏡 articles, assessing their three narrow changed remarks in context.

Read all 75 complete supplied JMdict families, including spelling and reading restrictions, reading-local annotations, sense restrictions and additional senses. Inspected the fifteen KANJIDIC2 records and metadata, separately distinguishing nanori. Read the applicable official Joyo rows directly from the supplied PDF as well as the extracted rows. Independently read the complete relevant public Digital Daijisen sections for all fifteen new characters.

Read the actual same-snapshot comparison articles, not just their titles: all 122 distinct existing kanji linked from the new lessons, the additional overlap candidates 企 承 敷 関 技 腕 了 完 済 査 軽, and the directly reused comparison word 放す. For comparison articles initially read by section, the omitted readings/common-word sections were subsequently read in full during this same initial review.

Read the supplied host-check outputs. Independent read-only checks established 45 added backlink pairs across 44 word articles, no removed backlinks, resolving local link targets throughout the 62 changed Markdown files, and valid exact-subset reading selections. All 77 changed files agree with the manifest after LF normalization: 75 match raw bytes; 乃至 and 剛健 match after their CRLF is normalized to LF.

For strokes, independently parsed the source SVG paths and compared all generated points with 16 equally spaced arc-length samples per stroke. Character identity, pinned revision, primary count, stroke order/types and finite coordinates agreed. Maximum geometric difference was at most approximately 0.071 source units, consistent with one-decimal rounding. This verifies source-geometry fidelity, not native drawing behavior.

No consequential part of the 77-file changed-content scope remains unread. The full exported repository was verification context, not a recursive audit of every older lesson or every word linked from a comparison article.

## Verdicts

**Overall: NEEDS FIX**, for the meaning-choice exclusions below. No separate actionable linguistic-correctness, scoped-coverage or comprehensibility defect was established.

| Cards | Correctness | Scoped coverage | Consistency / quiz safety, content | Comprehensibility |
| --- | --- | --- | --- | --- |
| 健 射 態 盤 看 至 酸 離 響 | CLEAN | CLEAN | CLEAN | CLEAN |
| 妙 | CLEAN | CLEAN | NEEDS FIX: F1 | CLEAN |
| 就 | CLEAN | CLEAN | NEEDS FIX: F2 | CLEAN |
| 展 | CLEAN | CLEAN | NEEDS FIX: F3 | CLEAN |
| 微 | CLEAN | CLEAN | NEEDS FIX: F4 | CLEAN |
| 診 | CLEAN | CLEAN | NEEDS FIX: F5 | CLEAN |
| 障 | CLEAN | CLEAN | NEEDS FIX: F6 | CLEAN |

The 45 backlink additions, three existing-kanji remark changes and fifteen stroke-reference datasets are **CLEAN within the inspected scope**. Runtime behavior outside the supplied model, actual Kotlin/native execution, phone acceptance and installed-client compatibility are **UNVERIFIED**.

The raw source inventories and curated practice choices are appropriately separated. In particular, the text preserves the entry-local obsolescence of 神妙 しんびょう, the separate obsolete 微妙 みみょう family, rare/kana-preferred spellings such as 態と, whole-word readings such as 微笑む and 算盤, and reading-specific 響 families. The selected readings have applicable linked examples. These distinctions should not be removed to address the quiz findings.

## Findings

All six findings are **moderate severity; consistency / meaning-quiz safety**. They concern evidenced ordinary meanings and actual displayed labels, not identical-title checking or mere topical similarity.

The shared impact is conditional: all fifteen new cards have three acceptable curated distractors, so these findings do **not** establish failure of their ordinary full-pool four-choice questions. However, the authoring contract expressly covers fallback when curated cards are absent, including filtered/custom pools. None of the direct pairs below is declared at either endpoint. Exclusions through a third character do not protect these pairs. The data gaps are established; their actual Kotlin/custom-pool exposure was not executed.

### F1. 妙 leaves ordinary skill answers eligible

**Location:** `kanji\妙.md:14,23-25,63-66`; counterpart labels and explanations at `kanji\技.md:3,20` and `kanji\腕.md:3,20,31`.

The displayed alternatives **"skill; technique"** (技) and **"arm; skill"** (腕) contain a defensible ordinary meaning of 妙. The supplied complete JMdict family 1528490, sense 3, explicitly gives "cleverness; adroitness; knack; skill" without an obsolete or rare qualifier for that sense. This is not an inference from the English word "exquisite" alone.

**Remedy:** Declare the direct 妙/技 and 妙/腕 exclusions at an appropriate endpoint; retain the useful skill explanation.

**Sources:** `evidence\jmdict-families.xml`, entry 1528490, sense 3; [Daijisen, 妙](https://www.weblio.jp/content/妙), character sense 2, "きわめて巧みである", and noun sense 1, including 演技の妙; [技](https://www.weblio.jp/content/技), ぎ/わざ entries; [腕](https://www.weblio.jp/content/腕), うで sense 2 and ワン sense 2. Complete relevant sections inspected. **Confidence: high.**

### F2. 就 omits both exact undertaking-label overlaps and completion overlaps

**Location:** `kanji\就.md:3,14,23-31,69-73`; counterparts `kanji\企.md:3,22-24`, `kanji\承.md:3,20,32`, `kanji\了.md:3,20`, `kanji\完.md:3,20-21`, `kanji\済.md:3,20-23`.

企 displays **"plan; undertake"** and 承 **"accept; undertake"**, sharing the literal undertaking answer already displayed by 就. Its explicitly taught ordinary completion sense also makes **"completion; settling"** (了), **"complete"** (完) and **"settle; finish"** (済) defensible alternatives. Excluding 成 and 始 does not exclude any of these five cards.

**Remedy:** Add these evidenced direct pairs: 就/企, 就/承, 就/了, 就/完 and 就/済. Do not remove the valid completion sense merely because ジュ is not selected for reading questions.

**Sources:** [Daijisen, 就](https://www.weblio.jp/content/就), シュウ "その事に取りかかる" and ジュ "出来あがる。しとげる"; complete same-snapshot counterpart articles cited above; [了](https://www.weblio.jp/content/了), sense 1; [完](https://www.weblio.jp/content/完), sense 2; [済](https://www.weblio.jp/content/済), サイ sense 2. These completion senses are not historical-only annotations. **Confidence: high.**

### F3. 展 and 敷 can both accept the displayed spreading answer

**Location:** `kanji\展.md:14,23-25,61-65`; `kanji\敷.md:3,14,23-25`.

敷 displays **"spread; lay out"**. 展 ordinarily includes spreading/laying things out flat, not only abstract development. This is the same relevant physical sense explained in both articles. Neither exclusion list protects 展/敷.

**Remedy:** Add the direct 展/敷 exclusion without treating the existing extension-related exclusions as a transitive group.

**Sources:** [Daijisen, 展](https://www.weblio.jp/content/展), sense 1, "平らに広げ並べる"; [敷](https://www.weblio.jp/content/敷), フ, "平らに広げて全体に及ぼす。しき延べる". Complete sections and actual 敷 article inspected. **Confidence: high.**

### F4. 微 leaves the ordinary "slight" answer from 軽 eligible

**Location:** `kanji\微.md:14,23,40,62-64`; `kanji\軽.md:3,20`.

軽 displays **"lightweight; slight"**. The slight-degree sense is independently supported for both characters; 微 itself correctly teaches "very small, slight" and 微か as "faint; slight". The ambiguity concerns slightness, not a claim that 微 means light in weight.

**Remedy:** Add the direct 微/軽 exclusion.

**Sources:** [Daijisen, 微](https://www.weblio.jp/content/微), ビ sense 2, "ほんの少し。わずか", including 軽微; [軽](https://www.weblio.jp/content/軽), ケイ sense 3, "程度が小さい", also including 軽微. Complete sections inspected. **Confidence: high.**

### F5. 診 omits an existing general inspection answer

**Location:** `kanji\診.md:14,23-27,58-61`; `kanji\査.md:3,20,28,38`.

査 displays **"investigate; inspect"**, an applicable broader description of examining a medical condition. The 診 article already excludes 察, 調 and 試 for examination/investigation overlap, correctly noting that broader labels can be defensible without making every compound medical. The same issue remains for 査; neither endpoint declares the pair.

**Remedy:** Add the direct 診/査 exclusion. Preserve the medical-specific explanation; this is not a request to equate diagnosis with every investigation.

**Sources:** [Daijisen, 診](https://www.weblio.jp/content/診), "病状をよく調べて判断する"; [査](https://www.weblio.jp/content/査), "しらべる"; actual 査 article's examination/inspection explanation. Complete sections inspected. **Confidence: high for the lexical overlap and missing pair; actual fallback exposure unverified.**

### F6. 障 leaves the ordinary barrier answer from 関 eligible

**Location:** `kanji\障.md:14,23,28-30,60-62`; `kanji\関.md:3,20-22`.

関 displays **"involve; barrier"**. A barrier/partition is an ordinary independently sourced sense of 障, explicitly taught through 障子 and its barrier explanation. The unrelated "involve" branch of the composite label does not remove its valid barrier answer.

**Remedy:** Add the direct 障/関 exclusion.

**Sources:** [Daijisen, 障](https://www.weblio.jp/content/障), sense 2, "隔てさえぎるもの"; [関](https://www.weblio.jp/content/関), せき sense 2, "物事をさえぎりとどめるもの。へだて。しきり". Complete relevant sections and actual 関 article inspected. **Confidence: high.**

The eleven cited pairs are concrete counterexamples, not a claim to have discovered every possible semantic overlap in the entire repository. Their correction need not create a clique or introduce unrelated vocabulary.

## Optional

None. No unrelated expansion or exhaustive historical treatment is requested.

## Limits

- The supplied Python reading audit has explicitly bounded modeled pools: full N1/All, Starter with one borrowed target, and its reported single-holder probes. Zero modeled main/padded-session hits is **not** a universal safety result.
- Custom/caller-built pools, multiple borrowed Starter cards, actual Kotlin draws, native execution, phone acceptance and older installed-client compatibility remain **UNVERIFIED**. No JVM, Gradle, emulator or phone work was performed.
- The reported eleven latent reading entries include eight nanori-only entries outside lexical teaching scope and three other dictionary/character readings. Neither their existence nor the zero modeled hits proves a runtime failure or universal immunity. The legacy helper's stronger pool-coverage prose is not adopted.
- The previously delivered `5c000bd` APK predates kanji `quiz_exclusions`. This review does not certify that installed APK, or claim that content exclusions protect it.
- Supplied validation, unit-test, manifest-rebuild and budget outputs were read as host evidence, not rerun or treated as linguistic proof. Other runtime assets and importer source were not supplied for independent execution. The manifest comparison above explicitly accounts for the two CRLF-normalized files; it is not an installed-client hash test.
- Dictionary lookup verifies the applicable inspected entry/sense, not universal frequency or every conceivable usage. CLEAN means no established actionable defect in the inspected content, not exhaustive linguistic correctness or release acceptance.
- Local review access was confined to the packet and this report destination. No other review report, author rationale, live checkout or session history was inspected. No subagents, other work sessions or background processes were started. The packet and repository exports were not changed; this report is the only intentional persistent write.

End of the single initial review. No implementation or confirmation round was performed, and the shared reviewer slot is not released by this report.
