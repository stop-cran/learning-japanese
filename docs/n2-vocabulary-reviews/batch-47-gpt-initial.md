## Snapshot: `7f42dbaf6ee9651095fe53f7b0efaf32b346c068` — committed content only

Parent: `65f15e38eccebb81b697be187c8702bf85265fa5`.

The frozen receipt was read first. Its commit, clean-worktree statement, hashes and equivalence checks are **author-executed assertions**: the available file tools cannot execute Git, so I could not independently verify them. No uncommitted changes were intentionally included.

## Scope

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`. Independent, read-only review; no agents, delegation or edits.

Completely read all nineteen new articles, reused `words\そっと.md`, the five assigned kanji cards, the four link-only old cards, and `batch-47-related.patch`. Also completely read **90 additional existing comparison articles**, including every existing target of the newly authored exclusions and consequential additional candidates such as 激増, 丸, ざわざわ, 架空 and 空想. These are my reads—not an adoption of the author’s claimed 110 old-body inspections.

Read the required repository instructions and `docs\content-format.md:18–126`; the vocabulary/source snapshots; only the twenty assigned TSV mappings; and `docs\jlpt-levels.md`. For `docs\confusable-words.md`, read lines 1–100 and searched the assigned terms, not the entire document.

Evidence reads included the complete mapping, principal, component and label JSONL renderings; all twelve selected-family files; the eighteen-family supplemental rendering; and both public-body renderings. These cover the receipt-described **194-family/435-sense union, including the twenty principals/27 senses**. I did not independently recompute that deduplicated count or the equivalence hashes. The large review-evidence JSON was inspected selectively, not read in full; the separate principal-reading TXT was unnecessary because its complete JSONL counterpart was read.

Fresh lexical entries were inspected for 騒騒しい, 丸, 全般, 激増, ざわざわ, 架空 and 空想. Prohibited notes, the rationale-bearing batch JSON, author-check receipts and other reviewers’ outputs were not read.

## Verdicts

**Five localized quiz-exclusion gaps need fixes; one word-origin classification remains unverified.** No other actionable definition, construction, example, source-mapping or comprehensibility defect was established.

Quiz-guard omissions are charged to **scoped coverage** below; they do not make the otherwise accurate definitions incorrect. Source selections are one-based. **CLEAN** means no actionable defect established within this review’s scope, not exhaustive correctness or native-speaker certification.

| Mapping | Article / status | Correctness | Scoped coverage | Comprehensibility | Mapping / selected senses |
|---|---|---|---|---|---|
| N2:922 | センチ — new | CLEAN | CLEAN | CLEAN | CLEAN — 1075060:1,2 |
| N2:923 | 宣伝 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1389730:1 |
| N2:924 | 先頭 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1596210:1 |
| N2:925 | 全般 — new | CLEAN | NEEDS FIX — F2 | CLEAN | CLEAN — 1396020:1,2 |
| N2:926 | 扇風機 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1390760:1 |
| N2:927 | 線路 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1391880:1 |
| N2:928 | 相違 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1400820:1 |
| N2:929 | そういえば — new | CLEAN | CLEAN | CLEAN | CLEAN — 1982210:1 |
| N2:930 | 雑巾 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1299370:1 |
| N2:931 | 増減 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1403200:1 |
| N2:932 | 倉庫 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1399120:1 |
| N2:933 | 相互 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1596370:1 |
| N2:934 | 創作 — new | CLEAN | NEEDS FIX — F5 | CLEAN | CLEAN — 1398420:1,2 |
| N2:935 | 葬式 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1402160:1 |
| N2:936 | 造船 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1403720:1 |
| N2:937 | 騒々しい — new | UNVERIFIED — F6 | NEEDS FIX — F4 | CLEAN | CLEAN — 1596440:1,2 |
| N2:938 | 増大 — new | CLEAN | NEEDS FIX — F1 | CLEAN | CLEAN — 1403310:1 |
| N2:939 | そうっと → そっと — reused | CLEAN | CLEAN | CLEAN | CLEAN — 1006810:1,2,3 |
| N2:940 | 送別 — new | CLEAN | CLEAN | CLEAN | CLEAN — 1402850:1 |
| N2:941 | 草履 — new | CLEAN | NEEDS FIX — F3 | CLEAN | CLEAN — 1402060:1 |

**Mapping qualifications:** The selections account for 26 senses; センチ’s separately qualified sentimental sense 3 brings the complete principal-family total to 27. It is not independently assigned N2. Blank source fields remain blank, especially both kanji and gloss for N2:939; dictionary-supported reuse does not establish an unstated compiler intention. Search-only, rare, irregular and outdated forms are appropriately distinguished. Kana-primary そういえば correctly retains `kanji: []` while recognizing そう言えば.

**Five kanji edits — correctness / scoped coverage / comprehensibility CLEAN for each:** 般↔全般, 線↔線路, 減↔増減, 庫↔倉庫 and 造↔造船. Both the reading row and Common words provide useful reciprocal links at the actual readings: ハン appearing as パン, セン, ゲン, コ and ゾウ respectively. Written-kanji metadata is complete; unavailable component cards are not invented.

**Four link-only edits — all three facets CLEAN for each:** 広告→宣伝, 頭→先頭, 扇子→扇風機 and 下駄→草履. The links fit their existing passages without redesigning baseline teaching. F3 concerns the new card’s quiz guard, not the correctness of 下駄’s added link.

**Reused preservation — CLEAN:** The supplied patch preserves そっと’s stable ID, primary reading, title `gently; quietly`, N3, original teaching and baseline exclusion declarations. The alias paragraph, gentle-handling example and source link are additive. The three selected uses remain covered; this is not a wholly new N2 article.

**Source-sensitive constructions — CLEAN:** 相互’s の/に attachment, 増減’s two valencies, and 増大’s direct transitive versus causative constructions are distinguished. 造船 correctly reports the pinned intransitive label separately from the captured dictionary’s direct-object example rather than forcing them into one unrestricted POS claim.

## Findings

**F1 — Minor; scoped coverage; missing 増大/激増 quiz exclusion.**

**Location:** `words\増大.md:4,9,46–48`; comparison `words\激増.md:4,9,16–17`.

Neither card excludes the other. For 激増, the alternative label `enlargement; increase` contains a defensible ordinary answer: a sharp increase remains an increase. The complete articles explicitly distinguish rate without making the underlying increase meanings disjoint. Shared exclusions with 増加 and 増える do not protect this pair or separate them when both are other choices. **Minimal remedy:** add 激増 to 増大’s exclusions; no reciprocal edit is required. **Evidence:** complete cards; JMdict 1403310:1 and 1253690:1; fresh [精選版日本国語大辞典, 激増](https://kotobank.jp/word/激増-489714). **Confidence: high.**

**F2 — Minor; scoped coverage; missing 全般/丸 quiz exclusion.**

**Location:** `words\全般.md:4,9,16–18`; comparison `words\丸.md:4,15–20,32`.

The complete labels are `the whole; overall scope` and `circle; whole`. 丸’s ordinary whole/full-amount use is genuinely taught, including 丸一年; this is not an inference from circular shape or a rare alternate reading. Without attachment context, “whole” remains a defensible answer for 全般. Different noun/suffix/prefix behavior does not resolve the displayed-label ambiguity. **Minimal remedy:** add 丸 to 全般’s exclusions while retaining the useful grammatical distinctions. **Evidence:** complete cards; JMdict 1396020:1–2; the current まる heading and prefix use in [精選版日本国語大辞典, 丸](https://kotobank.jp/word/丸-137471), not the separate historical まろ heading. **Confidence: medium-high.**

**F3 — Minor; scoped coverage; missing 草履/下駄 quiz exclusion.**

**Location:** `words\草履.md:4,9,36–38`; comparison `words\下駄.md:4,9,16`.

草履’s label includes the broad alternative `traditional Japanese sandals`, which also accurately describes 下駄 in its complete existing article. Thus it can be a defensible answer when 下駄 is tested, despite the correctly explained distinction between zori and geta. Both cards excluding サンダル and 靴 does not exclude them from each other. **Minimal remedy:** add 下駄 to 草履’s exclusions; do not merge the words or alter the old article’s teaching. **Evidence:** complete titles and bodies; principal 1402060 and the inspected 下駄 family 1185780. **Confidence: high.**

**F4 — Minor; scoped coverage; missing 騒々しい/ざわざわ quiz exclusion.**

**Location:** `words\騒々しい.md:4,9,15–24`; comparison `words\ざわざわ.md:4,8,17–28`.

The existing card’s complete title is `crowd murmuring; rustling`, but its ordinary meanings also include commotion and an unsettled feeling. Consequently 騒々しい’s displayed `noisy; boisterous; unsettled` supplies plausible answers for those uses. This is supported lexical overlap, not merely a shared sound tag. The existing 騒がしい/ざわざわ guard does not extend transitively to 騒々しい. **Minimal remedy:** add ざわざわ to 騒々しい’s exclusions. **Evidence:** complete cards; JMdict 1596440:1–2; fresh [精選版日本国語大辞典, ざわざわ](https://kotobank.jp/word/ざわざわ-512678), senses 1–2 covering noisy commotion and restlessness. **Confidence: high.**

**F5 — Minor; scoped coverage; missing 創作/架空 quiz exclusion.**

**Location:** `words\創作.md:4,9,23–26`; comparison `words\架空.md:4,9,16–21,29–35`.

創作 expressly includes fabrication/made-up material. 架空’s ordinary かくう meaning includes fictitious, imaginary or fabricated content—not only overhead structures. That makes `imaginary; overhead` a plausible alternative for 創作’s made-up-story use. The overhead sense does not erase the first meaning, and their separate guards with 小説 do not protect this pair. **Minimal remedy:** add 架空 to 創作’s exclusions, without implying unrestricted grammatical interchangeability or adding the reading がくう to this sense. **Evidence:** complete cards; JMdict 1398420:2; fresh [精選版日本国語大辞典, 架空](https://kotobank.jp/word/架空-460081), current かくう heading, sense 2. **Confidence: medium-high.**

**F6 — Minor unresolved claim; correctness of word-origin metadata; 騒々しい’s native classification is UNVERIFIED.**

**Location:** `words\騒々しい.md:6,8,32–33`; classification convention at `docs\content-format.md:63`.

The sources establish an i-adjective, but that grammatical fact does not establish `type: wago` or the definite “native-adjective classification.” The fresh [精選版日本国語大辞典 entry](https://kotobank.jp/word/騒騒しい-552771) discusses competing derivations, including adjectival formation from 忩々, and questions 騒騒 as potentially ateji. **Minimal remedy:** establish and document a defensible word-origin classification, distinguishing it from conjugation; qualify disputed formation and align the metadata, tag and prose with the repository’s convention. This finding does **not** establish that an unqualified switch to `kango` is correct. **Confidence: medium; unresolved classification, not a demonstrated reading or meaning error.**

No actionably excessive exclusion was established. In particular, conservative guards must be assessed against the displayed English alternatives; a guard is not itself a claim that the Japanese words are freely interchangeable.

## Optional

None. Exhaustive dictionary expansion, additional examples and unrelated baseline redesign are not required.

## Limits

Snapshot identity and committed cleanliness rely on the supplied receipt, not independent Git or hash execution. Source-count and rendering-equivalence assertions were not independently recomputed.

The supplied public bodies are **author captures**. I inspected their actual lexical headings and identity qualifications, including mixed センチ headings, the separate 創作 magazine title, unrelated 率土, and 草履’s historical/current readings. The そういえば extraction failed and provides no positive public corroboration; its CLEAN mapping rests on the complete pinned JMdict record.

Fresh failed fetches and encyclopedic extractions were not treated as lexical verification. In particular, the captured Daijisen direct-object example for 造船 was inspected but not independently re-established by a fresh lexical retrieval.

Quiz findings establish missing static guards under the documented selection contract, not observed runtime questions. I did not execute the app or inspect every existing article or possible exclusion pair. F6 remains consequentially unverified; the other CLEAN judgments are bounded editorial conclusions, not native-speaker certification.
