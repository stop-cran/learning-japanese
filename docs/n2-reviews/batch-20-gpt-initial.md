## Snapshot: adaf3b4c7349e9d7ecb1360b91e9cd85d1ae20ac; committed files only

The frozen snapshot records `clean: true`, 57 scope files, and baseline `799bf28ae8fbc48c1af8e80b797bcb2ebfd57a2f`. **File tools were available, but Git execution was not**: I relied on that record for commit identity, cleanliness and change scope rather than independently verifying them.

## Scope: gpt-6.1-sol; family gpt

Read all 16 new teaching pages completely. Reviewed all 59 reading rows—54 lexical examples and five qualified source-only/index rows—against the supplied metadata and restriction-aware dictionary evidence. Checked all 45 new-kanji distractor assignments, useful word links, relevant vocabulary answer labels and direct exclusions, and the existing two-distractor kanji fallback surface.

Inspected the linked component passages in context in these 21 existing `words\` articles: `冷蔵庫.md`, `薄い.md`, `虫.md`, `虫歯.md`, `血.md`, `衣服.md`, `手袋.md`, `袋.md`, `被る.md`, `被害.md`, `服装.md`, `装置.md`, `裏.md`, `裏切る.md`, `候補.md`, `複雑.md`, `角.md`, `触る.md`, `触れる.md`, `訓.md`, `訓練.md`.

**Omissions:** No assigned teaching page or related component passage was omitted. Unchanged word content was not comprehensively reviewed. Exhaustive drawing-path review of the 15 generated stroke files was not performed. No prohibited authoring material, review ledger or other reviewer’s output was read. No files were edited and no agents were used.

## Verdicts:

**The 15 kanji cards have no established actionable defect. The supporting word article needs an additional quiz safeguard; its teaching explanation is sound.**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\蒸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\蔵.md` | CLEAN | CLEAN | CLEAN |
| `kanji\薄.md` | CLEAN | CLEAN | CLEAN |
| `kanji\虫.md` | CLEAN | CLEAN | CLEAN |
| `kanji\血.md` | CLEAN | CLEAN | CLEAN |
| `kanji\衣.md` | CLEAN | CLEAN | CLEAN |
| `kanji\袋.md` | CLEAN | CLEAN | CLEAN |
| `kanji\被.md` | CLEAN | CLEAN | CLEAN |
| `kanji\装.md` | CLEAN | CLEAN | CLEAN |
| `kanji\裏.md` | CLEAN | CLEAN | CLEAN |
| `kanji\補.md` | CLEAN | CLEAN | CLEAN |
| `kanji\複.md` | CLEAN | CLEAN | CLEAN |
| `kanji\角.md` | CLEAN | CLEAN | CLEAN |
| `kanji\触.md` | CLEAN | CLEAN | CLEAN |
| `kanji\訓.md` | CLEAN | CLEAN | CLEAN |
| `words\蒸す.md` | NEEDS FIX | CLEAN | CLEAN |

CLEAN denotes no established actionable defect within this scope, not exhaustive truth or native-speaker certification.

## Findings:

### GPT-20-01 — Minor; correctness: English answer-label ambiguity remains unguarded

**Location:** `words\蒸す.md:4,8,15-18`. Comparison labels and exclusions: `words\べたべた.md:4,8`, `words\密.md:4,9`, `words\近い.md:4`, `words\親しい.md:4,9`, `words\閉じる.md:4,9`, `words\閉まる.md:4`.

**Claim and impact:** The weather sense of 蒸す overlaps with established weather meanings of English **sticky** and **close**. Existing answer labels include “sticky; clingy,” “dense; close,” “near; close,” “close; familiar,” “close; shut” and “close; be shut.” None has a direct exclusion with 蒸す. Consequently, an unqualified English weather reading can make an intended wrong answer defensible. The closing labels also present a written-English homograph across adjective and verb pronunciations.

This is an **English-label collision**, not a claim that the Japanese words for proximity, relationships or closing mean humid weather. Companion glosses help indicate their intended senses, but the displayed labels retain the unqualified alternatives.

**Minimal remedy:** Add direct exclusions from 蒸す to `べたべた`, `密`, `近い`, `親しい`, `閉じる` and `閉まる`, retaining its current exclusions. This avoids changing unrelated articles. Alternatively, disambiguate the affected English labels explicitly. Existing exclusions between those older words do not protect their pairs with 蒸す.

**Exact evidence:**
- JMdict entry **1356900**, sense 2, in `docs\n2-batch-sources\batch-20.json:1381-1451`, licenses 蒸す むす as “to be hot and humid” / “to be sultry,” with intransitive godan classification.
- Successfully fetched [American Heritage, *sticky*](https://www.ahdictionary.com/word/search.html?q=sticky), adjective sense **3**: “Warm and humid; muggy.”
- Successfully fetched [American Heritage, *close*](https://www.ahdictionary.com/word/search.html?q=close), adjective sense **14**: “Warm and humid or stuffy.”
- `docs\content-format.md:79-99` establishes displayed-title comparison, symmetric but nontransitive exclusions, and the reasonable-acceptance criterion.

**Confidence:** High in the dictionary overlap and missing direct exclusions; medium in the practical ambiguity of the complete multi-gloss labels. Actual candidate occurrence was not executed.

No other actionable defect was established. All 15 cards match the supplied reading inventories, primary stroke counts, canonical radicals and grade tags. The source-only/index qualifications are appropriately bounded; spelling rarity, obsolete pronunciation and kana-only restrictions are distinguished correctly. All 45 curated kanji options are semantically wrong for their targets, every new kanji has a useful linked word article, and no new direct-synonym hazard was established for an older two-choice fallback. The 21 related component passages remain consistent with their linked cards.

## Optional:

None.

## Limits:

Commit state and the exact baseline diff were not independently verified without Git. Pinned dictionary records were inspected, but their original downloads, hashes and full-dictionary negative scans were not independently reproduced; the cards’ bounded source-only wording does not claim dictionary-wide absence.

The app was not executed, so the finding establishes answer-label ambiguity and missing safeguards, not observed selection frequency. Generated stroke geometry, unrestricted corpus frequency, comprehensive unchanged-page correctness and native-speaker naturalness certification remain outside this review.
