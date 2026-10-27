## Snapshot: 2eccc7af442aeb9cbcb7c064650a2e6b63b11e1e — committed content only

Parent: `1aaf5435e579a352cfdc3069e0656be0d5f4fc2c`. Snapshot identity and committed-content status are taken from the frozen receipt; independent Git verification was unavailable.

## Scope

**Reviewer:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`; one independent reviewer, no delegation or edits.

Read all nineteen new articles completely, the actual eight-file related patch and its changed passages in context, and the unchanged `叔母さん／おばさん → 伯母さん` reuse claim. Assessed all twenty mappings, N2:202–N2:221, against the supplied principal families, relevant comparison/component evidence and independently retrieved dictionary entries. Read the required instructions and content-format section. No forbidden authoring material, review ledgers or other reviewer output was consulted.

**Outcome:** Five articles need quiz-exclusion fixes. No actionable defect was established in their teaching prose, the twenty lexical mappings, the eight related changes or the narrowly scoped reuse claim.

## Verdicts

Correctness includes quiz-answer fairness. Scoped coverage concerns the declared practical lesson and assigned source coverage, not exhaustive dictionary coverage.

| New article, under `words\` | Source row | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `驚かす.md` | N2:202 | CLEAN | CLEAN | CLEAN |
| `お願いします.md` | N2:203 | CLEAN | CLEAN | CLEAN |
| `各々.md` | N2:204 | CLEAN | CLEAN | CLEAN |
| `おはよう.md` | N2:206 | CLEAN | CLEAN | CLEAN |
| `お参り.md` | N2:207 | CLEAN | CLEAN | CLEAN |
| `お待たせしました.md` | N2:208 | NEEDS FIX | CLEAN | CLEAN |
| `お待ちどおさま.md` | N2:209 | CLEAN | CLEAN | CLEAN |
| `おめでたい.md` | N2:210 | CLEAN | CLEAN | CLEAN |
| `思いがけない.md` | N2:211 | CLEAN | CLEAN | CLEAN |
| `思い込む.md` | N2:212 | NEEDS FIX | CLEAN | CLEAN |
| `思いっきり.md` | N2:213 | NEEDS FIX | CLEAN | CLEAN |
| `思い付く.md` | N2:214 | CLEAN | CLEAN | CLEAN |
| `重たい.md` | N2:215 | NEEDS FIX | CLEAN | CLEAN |
| `おやすみ.md` | N2:216 | CLEAN | CLEAN | CLEAN |
| `おやつ.md` | N2:217 | CLEAN | CLEAN | CLEAN |
| `親指.md` | N2:218 | CLEAN | CLEAN | CLEAN |
| `オルガン.md` | N2:219 | CLEAN | CLEAN | CLEAN |
| `卸す.md` | N2:220 | CLEAN | CLEAN | CLEAN |
| `恩恵.md` | N2:221 | NEEDS FIX | CLEAN | CLEAN |

**Related changes — changed passages only:**

| Passage | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\各.md:29,34,38` — reciprocal examples and spelling link | CLEAN | CLEAN | CLEAN |
| `words\おどかす.md:28` — 驚かす link | CLEAN | CLEAN | CLEAN |
| `words\お菓子.md:26` — おやつ comparison link | CLEAN | CLEAN | CLEAN |
| `words\ください.md:32–33` — お願いします comparison link | CLEAN | CLEAN | CLEAN |
| `words\どうぞ.md:28` — お願いします comparison link | CLEAN | CLEAN | CLEAN |
| `words\休日.md:27` — お休み alias link and reading | CLEAN | CLEAN | CLEAN |
| `words\宜しく.md:37–40` — request-formula link in context | CLEAN | CLEAN | CLEAN |
| `words\菓子.md:29` — おやつ comparison link | CLEAN | CLEAN | CLEAN |

**Unchanged reuse, N2:205:** **CLEAN / CLEAN / CLEAN**, limited to the claimed coverage. `words\伯母さん.md:15,28` explicitly teaches `叔母さん`, its shared reading おばさん and the younger-aunt relationship. N5 and the stable article identity remain intact. The supplied family 2261500 supports this aunt sense; the unrelated-woman use belongs to separate family 2261510. This is not whole-article recertification.

**All twenty mapping claims:** **CLEAN / CLEAN / CLEAN** within their lexical-mapping scope, independently of the quiz defects below. In particular:

- N2:203, 208 and 209 explicitly teach the source kana formulas at their written article IDs, with matching readings and applicable meanings.
- N2:211 explicitly recognizes `思い掛けない／おもいがけない`; N2:213 explicitly recognizes `思いっ切り／おもいっきり`. Both correctly qualify the rare **spellings**, without calling the pronunciations rare.
- N2:210 correctly separates adjective おめでたい from noun おめでた rather than teaching “pregnancy” as an unrestricted adjective meaning. N2:211 does not promote “casual” into clothing/register senses.
- N2:213 retains the blank source gloss and uses dictionary-backed adverb teaching. N2:220 correctly treats 卸す as a verb and acknowledges cooking overlap with 下ろす／降ろす rather than inventing exclusive spelling compartments.

The new primary-word kanji arrays account for every written kanji. The required N2 reciprocal example is present at `各／おのおの`; alias-only characters are not incorrectly added to primary-spelling metadata.

## Findings

All findings below concern **direct, missing quiz exclusions**, not incorrect definitions or unrestricted Japanese interchangeability. Exact-title deduplication does not cover these pairs. An exclusion through a third card does not protect them, in either quiz direction or when both appear among other choices.

**B11-GPT-01 — Minor; correctness, quiz — `words\お待たせしました.md:4,9`**

The wait-acknowledgment card excludes ありがとう but not **どうも**, whose displayed title is “thanks; very much” (`words\どうも.md:4,15`). Generic “thanks” remains a defensible English answer for the explicitly taught “thank you for waiting” use, producing an ambiguous meaning question.

**Minimal remedy:** Add a direct `どうも` exclusion on お待たせしました.

**Evidence:** Supplied JMdict family 2149640, sense 1 (`batch-11.json:1585–1630`), explicitly includes “thank you for waiting.” Independently inspected [Jisho どうも](https://jisho.org/search/どうも), including its full API record, gives “thank you; thanks” in sense 1. **Confidence: high.**

**B11-GPT-02 — Minor; correctness, quiz — `words\思い込む.md:4,9`**

**決める** remains eligible against “be convinced; assume.” Its ordinary secondary meaning includes **“take for granted; assume,”** so it is a defensible Japanese answer to that English prompt. Its decision sense also overlaps 思い込む’s separately recorded “make up one’s mind” use. Neither card declares this direct pair.

**Minimal remedy:** Add `決める` to 思い込む’s exclusions.

**Evidence:** Complete principal family 1309230, senses 1–2 (`batch-11.json:798–895`); independently inspected [Jisho 決める](https://jisho.org/search/決める), reading きめる, senses 1 and 5. The actual competing title is “decide; settle” at `words\決める.md:5`. **Confidence: high.**

**B11-GPT-03 — Minor; correctness, quiz — `words\思いっきり.md:9,33`; `words\思い込む.md:9`**

The resolution-related guards omit **覚悟**, titled “mental preparedness; resolve” (`words\覚悟.md:4`). 思いっきり has an explicitly acknowledged noun sense “resolution; determination; resignation”; 思い込む also has a “make up one’s mind; be determined” sense. Consequently, the context-free English label **“resolve”** can admit these alternatives. Existing guards involving 決心 do not transitively exclude 覚悟.

**Minimal remedy:** Add direct `覚悟` exclusions for both 思いっきり and 思い込む.

**Evidence:** Complete families 1309310, sense 2 (`batch-11.json:896–978`), and 1309230, sense 2; independently inspected [Jisho 覚悟](https://jisho.org/search/覚悟), reading かくご, senses 2–3: “resolution; determination” and “resignation.” **Confidence: high.**

**B11-GPT-04 — Minor; correctness, quiz — `words\重たい.md:4,9,16`**

**大変**, displayed as “difficult, serious,” remains an eligible choice although 重たい’s ordinary figurative meaning includes **“serious.”** The existing exclusions for 重大 and 深刻 address this overlap only for those particular pairs; they do not protect 大変. This can make “serious” a second defensible answer despite the different titles.

**Minimal remedy:** Add a direct `大変` exclusion on 重たい.

**Evidence:** Complete principal family 1335780, sense 2 (`batch-11.json:979–1043`), includes “serious”; complete comparison family 1415000, sense 3 (`batch-11.json:8892–9031`), gives 大変 “serious; grave.” Its actual title and explanation are at `words\大変.md:4,15`. **Confidence: high.**

**B11-GPT-05 — Minor; correctness, quiz — `words\恩恵.md:4,9`**

**おかげ** remains eligible against “benefit; blessing.” Its displayed title, “help; thanks to,” does not expose its ordinary noun sense **“grace; blessing.”** In an English-to-Japanese question for 恩恵, おかげ can therefore be a defensible answer. This is lexical overlap, not merely a shared gratitude topic.

**Minimal remedy:** Add a direct `おかげ` exclusion on 恩恵.

**Evidence:** Complete principal family 1183140, sense 1 (`batch-11.json:697–747`), includes “grace; blessing; benefit.” Independently inspected [Jisho’s full おかげ record](https://jisho.org/api/v1/search/words?keyword=%E3%81%8A%E3%81%8B%E3%81%92) identifies お陰／お蔭, reading おかげ, with sense 1 “grace (of God); benevolence (of Buddha); blessing,” marked usually kana-written. `words\おかげ.md` declares no reciprocal exclusion. **Confidence: high.**

## Optional

None.

## Limits

I had **file tools, not Git execution**. I could not independently verify the checkout, commit ancestry, clean-worktree assertion or normalized hashes against Git objects. “Committed content only” therefore follows the frozen receipt’s identification, not an independently executed Git comparison.

The supplied JMdict/KANJIDIC2 records and provenance were not independently re-extracted or hash-verified. Author inspection receipts were treated as assertions, not independent retrieval. I separately inspected the three cited Kotobank entries, the actual Weblio 卸す definitions and the Jisho records used above; failed or heading-only extractions were not used as evidence.

This was an editorial review, not exhaustive dictionary, corpus-frequency or native-speaker certification. Existing comparison cards were consulted as evidence without recertifying their unchanged teaching. The pinned vocabulary list supplies community study labels, not an official modern JLPT syllabus.
