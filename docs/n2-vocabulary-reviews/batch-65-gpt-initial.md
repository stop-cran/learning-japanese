## Snapshot: 76fedcbf56ba9efaf1ccc6e6c9ca60e478ca22db — committed content only

**Three actionable findings:** one register-guidance omission and two quiz-exclusion omissions. The twenty source associations, principal lexical mappings, primary-kanji metadata, and six required reciprocal relationships pass the substantive review.

Parent: `fc77da2dede8066a36e614156994fcd93362dfb7`. This review uses the supplied frozen snapshot’s committed-content representation. File tools cannot execute Git, so I could not independently establish HEAD, worktree cleanliness, parent comparisons, or the supplied hashes.

## Scope

**Reviewer:** GPT-6.1 Sol, model ID `gpt-6.1-sol`, family `gpt`. Independent, read-only review; no agents, delegation, edits, or other reviewer’s report.

I read:

- All nineteen assigned word articles completely; all four complete edited kanji articles; and `related.patch`.
- The required repository instructions and `docs\content-format.md:18–103`; the allowed JLPT and confusable-word policies; both allowed source snapshots; and the TSV header plus exactly `N2:1282–N2:1301`.
- All twenty blind mappings, nineteen complete principal families, 37 component records, and 116 navigation-label/exclusion records, including restrictions, flags, inherited POS, raw fields, and selected/additional senses.
- All 23 bounded family/older-body inspection chunks: the supplied complete family union, reported as **232 families/535 senses**, including nineteen principals/forty senses; and **106 complete reproduced older articles**. The union totals were not independently recomputed.
- The twenty complete reproduced public dictionary bodies and their capture receipts. These are supplied Digital Daijisen captures through Weblio—one authority, not twenty independent dictionaries.
- Ten additional complete repository articles: 能, ぐつぐつ, ことこと, きびきび, さくさく, 考慮, 検討, 評価, 暖まる, and ねっしん.
- Relevant definitions returned by nine fresh Kotobank lookups: 女房, 俄, 濃度, ぐつぐつ, ことこと, 暖まる, 考慮, 焼く, and 睨む. These supplied useful **精選版 日本国語大辞典** evidence and, where actually returned, Digital Daijisen evidence.

The large `review-evidence.json` overview was read only through line 110; its substantive equivalents were inspected through the compact records, complete chunks, and public-body files. I did not equate navigation labels with full-body inspection or read the prohibited rationale-bearing manifest, ledgers, scripts, or reports.

## Verdicts

**CLEAN** means no actionable defect established within this scope. Correctness includes quiz metadata; scoped coverage concerns the teaching needed for the article’s selected practical scope. Finding IDs explain the non-clean cells.

In the mapping column, **S** denotes selected source senses and **A** additional recognition senses; all numbers are one-based.

| Source row and form | Exact article association | Correctness | Scoped coverage | Comprehensibility | Mapping: JMdict; S; A |
|---|---|---|---|---|---|
| N2:1282 女房 | `words\女房.md` | CLEAN | **NEEDS FIX — G65-01** | CLEAN | 1345420; S1; A2 |
| N2:1283 睨む | `words\睨む.md` | **NEEDS FIX — G65-02** | CLEAN | CLEAN | 1569880; S1,4; A2,3,5 |
| N2:1284 煮る | `words\煮る.md` | CLEAN | CLEAN | CLEAN | 1322540; S1; A— |
| N2:1285 俄 | `words\俄.md` | CLEAN | CLEAN | CLEAN | 1599920; S1,2; A4 |
| N2:1286 縫う | `words\縫う.md` | CLEAN | CLEAN | CLEAN | 1517700; S1; A2 |
| N2:1287 濡らす | `words\濡らす.md` | CLEAN | CLEAN | CLEAN | 1467610; S1; A— |
| N2:1288 ねじ | `words\ねじ.md` | CLEAN | CLEAN | CLEAN | 1585010; S1; A2 |
| N2:1289 捩る | `words\捩る.md` | CLEAN | CLEAN | CLEAN | 1611090; S1; A2 |
| N2:1290 ネックレス | `words\ネックレス.md` | CLEAN | CLEAN | CLEAN | 1093000; S1; A— |
| N2:1291 熱する | `words\熱する.md` | **NEEDS FIX — G65-03** | CLEAN | CLEAN | 1467730; S1; A2 |
| N2:1292 寝間着 | `words\寝間着.md` | CLEAN | CLEAN | CLEAN | 1360040; S1; A— |
| N2:1293 寝巻 | **`words\寝間着.md`** | CLEAN | CLEAN | CLEAN | 1360040; S1; A— |
| N2:1294 狙い | `words\狙い.md` | CLEAN | CLEAN | CLEAN | 1396550; S1,2; A— |
| N2:1295 狙う | `words\狙う.md` | CLEAN | CLEAN | CLEAN | 1396590; S1; A2,3 |
| N2:1296 年度 | `words\年度.md` | CLEAN | CLEAN | CLEAN | 1469050; S1,2; A3 |
| N2:1297 農産物 | `words\農産物.md` | CLEAN | CLEAN | CLEAN | 1470710; S1; A— |
| N2:1298 農村 | `words\農村.md` | CLEAN | CLEAN | CLEAN | 1470730; S1,2; A— |
| N2:1299 濃度 | `words\濃度.md` | CLEAN | CLEAN | CLEAN | 1469970; S1; A2 |
| N2:1300 農薬 | `words\農薬.md` | CLEAN | CLEAN | CLEAN | 1470780; S1; A— |
| N2:1301 能率 | `words\能率.md` | CLEAN | CLEAN | CLEAN | 1470330; S1; A2 |

**Mapping-content assessment: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN for all twenty mappings.** The source forms/readings and applicable meanings are taught, and the selected/additional senses agree with the complete principal families. This is a substantive assessment of the blind derivative, not independent verification of its equivalence to the prohibited original.

Both sleepwear rows legitimately reach the shared article: **寝間着・寝巻・寝巻き, all ねまき**, are explicitly taught as alternate spellings with the same sleepwear meaning. No unsupported garment distinction or frequency hierarchy is imposed. Primary metadata correctly describes 寝間着 rather than importing 巻 from its variants.

The raw kanji fields for **ねじ and ネックレス remain empty**, appropriately corresponding to kana-primary articles with `kanji: []`.

**濃度’s raw “brightness” gloss is not a teaching requirement.** JMdict 1469970 and the supplied Daijisen entry support chemical concentration and mathematical cardinality. Independently retrieved 日本国語大辞典 additionally records **color depth/light absorption**, not an unrestricted synonym for a light’s brightness. The article’s specific rejection of “the brightness of a light” is defensible. This does not establish what the vocabulary compiler intended by the raw gloss.

Additional court-lady, figurative, slang, product-year, mathematical, and physics senses are reasonably separated as recognition teaching. Their inclusion does **not** establish separate N2 classifications. No easier existing article identity or level needs replacement.

**Kanji edits and reciprocal relationships:**

| Edited card | Correctness | Scoped coverage | Comprehensibility | Required relationships checked |
|---|---|---|---|---|
| `kanji\農.md` | CLEAN | CLEAN | CLEAN | 農産物 **のうさんぶつ / 1470710**; 農村 **のうそん / 1470730**; 農薬 **のうやく / 1470780** |
| `kanji\巻.md` | CLEAN | CLEAN | CLEAN | 寝巻 and 寝巻き **ねまき / 1360040**, both reaching `words\寝間着.md` |
| `kanji\村.md` | CLEAN | CLEAN | CLEAN | 農村 **のうそん / 1470730** |
| `kanji\濃.md` | CLEAN | CLEAN | CLEAN | 濃度 **のうど / 1469970** |

For all six relationships, I checked substantive word-side explanation, the relevant kanji reading-row example, Common words navigation, destination, whole-word reading, and matching footer ID. 寝間着’s alternate-spelling explanation links 巻.

**Baseline preservation: CLEAN within the supplied patch.** The four kanji headers and existing readings are preserved; the patch does not replace their metadata. Independent Git-level baseline verification remains unavailable.

Every primary written Han character is retained in word metadata. Existing primary component cards receive substantive links. The absent cards—房, 睨, 煮, 俄, 縫, 濡, 捩, 狙, 率—are not grounds for inventing cards or dropping characters.

**Quiz adjudication:** I treated exclusions as symmetric, nontransitive pairs applying in both quiz directions and among other choices. The findings below identify direct omissions, not inherited neighboring cliques.

Several superficially broad existing guards have real support: **針** has an ordinary “needlework/sewing” sense; **薬** includes efficacious chemicals such as pesticides; **性能** includes efficiency. **濃度／集中** warrants protection because their nonidentical full English titles overlap in “concentration,” despite the important Japanese distinction.

Conversely, shared cooking, ornament, farming, or thinking categories alone did not justify adding guards. For example, ぐつぐつ／ことこと describe sensory manner rather than automatically becoming synonyms of 煮る; ネックレス is not interchangeable with 指輪 merely because both are ornaments. I did not extend 睨む’s new 考慮 relationship automatically to 検討 or 評価. One redundant exact-title guard is noted under Optional.

## Findings

**G65-01 — Minor; scoped coverage/register — `words\女房.md:16–25,35–46`**

The article distinguishes one’s own wife from respectful reference to another person’s wife, but leaves the **register of the own-wife use** unexplained. Its uncomplicated productive examples and “妻 is another word” comparison can leave an English-speaking learner treating 女房 as an unmarked substitute for 妻.

**Minimal remedy:** Add a short, qualified warning that this wife-use can sound familiar/blunt or depreciative depending on speaker and setting, with 妻 the safer neutral starting choice. Do not turn that into “always insulting,” “always obsolete,” or an absolute prohibition.

**Exact evidence:** The complete article contains no such warning. [精選版 日本国語大辞典, 女房, にょうぼう sense ③](https://kotobank.jp/word/女房-110666) explicitly describes a modern depreciative nuance and frequent reference to one’s own wife. The supplied Daijisen capture independently supports the own-wife tendency, though it does not itself supply that register warning.

**Confidence:** High that the guidance is missing and the contextual risk is documented; the precise social effect is context-dependent. The existing examples are not being declared ungrammatical.

**G65-02 — Moderate; correctness/quiz exclusions — `words\睨む.md:9,46–50`; comparison `words\考慮.md:4,15–17`**

**睨む／考慮 is an unguarded direct semantic pair.** 睨む explicitly teaches “taking something into consideration” and “take the future into account.” 考慮’s full title is **“consideration; taking into account,”** and its body teaches that same operation.

Consequently, 考慮’s English label can be defensible for 睨む’s ordinary additional sense, and 睨む can be defensible for the “taking into account” part of an English-to-Japanese prompt. Protecting 睨む／考える does not protect this separate pair.

**Minimal remedy:** Add `考慮` to 睨む’s `quiz_exclusions`, or declare the equivalent pair on 考慮. One declaration is sufficient; do not automatically import 考慮’s neighboring exclusions.

**Exact evidence:** Article passages above; complete JMdict **1569880, sense 5**; supplied Daijisen **にらむ, sense 5**, “前もって考慮に入れる”; and freshly retrieved [日本国語大辞典, にらむ sense ④](https://kotobank.jp/word/睨む-593488), which likewise explicitly says “前もって考慮に入れる.”

**Confidence:** High.

**G65-03 — Moderate; correctness/quiz exclusions — `words\熱する.md:4,9,16–18`; comparisons `words\焼く.md:4,15–34` and `words\暖まる.md:4,9,16–20`**

The exclusion list misses **two independently supported heating pairs**:

- **熱する／焼く:** 焼く’s older title “bake; grill” does not exhaust its ordinary meanings. Complete JMdict **1350600, sense 3** explicitly gives **“to heat; to heat up,”** matching 熱する’s displayed “heat up” label.
- **熱する／暖まる:** 熱する explicitly includes intransitive becoming hot; 暖まる teaches becoming warm, including a room or soup warming up. The broad English **“heat up”** is defensible for that change. Neither article establishes a rigid temperature boundary that makes the labels reliably exclusive.

The absence matters in reverse-direction questions and when these cards occur together among other choices. Existing guards involving 暖める or あぶる do not transitively protect either pair.

**Minimal remedy:** Add `焼く` and `暖まる` to 熱する’s exclusion list. Preserve the useful distinctions and current meanings rather than narrowing titles artificially.

**Exact evidence:** Complete 焼く family in `batch-65-family-inspection-03.txt:60–69`, particularly sense 3 at line 65; complete older bodies cited above; supplied Daijisen **熱する senses 1–2**; and fresh [日本国語大辞典, 暖まる sense ①](https://kotobank.jp/word/暖まる-425212), “熱を帯びる。あたたかくなる.” The fresh [焼く entry](https://kotobank.jp/word/焼く-9411) also corroborates heating uses; the precise English “heat up” evidence is the complete JMdict family.

**Confidence:** High for 焼く; medium-high for 暖まる’s broad English-label overlap.

## Optional

- `words\女房.md:9`: The 妻 exclusion is redundant because both complete titles are exactly **“wife”**, already handled by title deduplication. Removing it is cleanup, not a blocking correctness fix.
- 濃度 could optionally add a brief recognition note about **color/optical density**, supported by 日本国語大辞典 sense ②. That expansion is not required for the selected chemical-concentration teaching and should not be called “brightness” without qualification.

## Limits

Git provenance, supplied hashes, clean-worktree assertions, and blind-derivative equivalence were **not independently executed or verified**. Baseline and committed-content conclusions rely on the supplied frozen evidence and patch.

I inspected the specified complete evidence, not every repository article or every navigation candidate. Full-body reads were not inferred from labels. Quiz conclusions use the documented exclusion behavior; I did not inspect or run the external application implementation.

The three direct Weblio fetches returned encyclopedia material rather than the intended Daijisen definitions and were **not used as dictionary verification**. Fresh Kotobank conclusions use actual returned, reading-specific definitions; missing extracted Daijisen sections were not treated as inspected.

Example naturalness was assessed editorially with construction-level lexical evidence, not native-speaker or corpus certification. No compiler-intent claim, independent sense-by-sense N2 classification, or frequency ranking is established here.
