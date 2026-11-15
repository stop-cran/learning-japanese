# B124 initial review — N1-B124-GPT-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: The pinned character record supports the title, radical, stroke count and full on/kun metadata. Complete applicable word families support the selected reading and vocabulary; irregular spelling and specialized-use qualifications are preserved. No historical derivation is asserted.

### Scoped coverage
Verdict: CLEAN
Basis: The sole on reading has its own linked example; no source kun reading is omitted. The card supplies the required learner sections, radical-form explanation, useful vocabulary and qualified mnemonic. The one existing-word edit is only the intended component-link wrapper.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: F1 establishes missing direct meaning-choice guards for 多 and 広. The four declared guards are supported, and the current three curated options are distinct; neither fact protects the additional direct pairs. Several other requested semantic comparisons remain consequentially UNVERIFIED, as recorded below, rather than being cleared from current runtime non-exposure.

### Comprehensibility
Verdict: CLEAN
Basis: The explanation distinguishes abundance and leeway, gives kana and English glosses, labels the shape story as a mnemonic, and separates ordinary readings, nanori and irregular spelling. No actionable clarity defect was established.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27; no re-views.
Extension chain: 1, 2, 3, 4; no re-views.
Read evidence/title-index.txt source lines 1-1244 completely: line 1 is "一 one" and line 1244 is "齢 age; years lived".
Snapshot: c8db34902d1a478d2d1de4b761dd3cdbb4585896. Base: 2655539b587c1ab57e64ab74a97cddaf81bb81c6. Scope: one new kanji, its stroke JSON, one existing-word link wrapper, supplied checks and dictionary evidence, all C cards, and the requested D/E cards.
Model: GPT-6.1 Sol, model ID gpt-6.1-sol, as identified by the serving model declaration; no separate execution-model attestation was inspected.
All ten supplied logs were read. They are supplied host/static results, not independently executed tests or linguistic certification.

## Phase-1 D/E lists
D: D1 余, D2 剰, D3 冗, D4 満, D5 多, D6 広, D7 悠, D8 楽, D9 栄, D10 資, D11 宝, D12 金, D13 充, D14 足, D15 濃
E: E1 厚, E2 富, E3 豊, E4 財
Missing entries: none
Full requests, preserving their phase-1 order and reasons:
D1 余 - 裕: surplus; capacity to spare versus abundance and leeway
D2 剰 - 裕: surplus amount versus abundance and room to spare
D3 冗 - 裕: superfluity; excess versus abundance and spare capacity
D4 満 - 裕: fullness; enough versus plenty and abundance
D5 多 - 裕: many; much versus abundant
D6 広 - 裕: spaciousness versus roominess
D7 悠 - 裕: leisurely ease and possible spaciousness versus having leeway
D8 楽 - 裕: ease; comfort versus having leeway
D9 栄 - 裕: flourishing; prosperity versus material prosperity
D10 資 - 裕: resources; capital versus wealth and riches
D11 宝 - 裕: treasure; valuables versus riches
D12 金 - 裕: money versus material wealth
D13 充 - 裕: filling; sufficiency versus abundance
D14 足 - 裕: sufficiency; enough versus plenty
D15 濃 - 裕: rich versus rich; abundant
E1 厚 - Verify the ordinary abundant secondary sense and the declared direct 裕/厚 guard.
E2 富 - Verify wealth and abundance overlap and the declared direct 裕/富 guard.
E3 豊 - Verify bountiful; abundant; rich overlap and the declared direct 裕/豊 guard.
E4 財 - Verify wealth; riches secondary senses and the declared direct 裕/財 guard.

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 余 | surplus | 裕 | Spare capacity versus surplus: independent 余 meanings include surplus and remainder, evidence/kanjidic2-records.xml:125-143; 裕 has ゆとり, evidence/external-snapshots/01-extract.txt:1-8. | UNVERIFIED whether the ordinary character senses overlap sufficiently to require exclusion. Neither endpoint declares the direct pair, repo/kanji/余.md:1-12; snapshot/kanji/裕.md:13-14. The whole-word surplus gloss for 余裕 alone does not settle constituent equivalence. |
| D2 | 剰 | remainder; surplus amount | 裕 | Surplus and excess are explicit, with useful qualifications distinguishing excess from merely a large amount, repo/kanji/剰.md:21-44. | UNVERIFIED: excess/remainder may overlap leeway but is not automatically abundance. Independent 剰 character evidence is not supplied. No direct pair on either endpoint; 剰/冗 is not a 裕/剰 guard, repo/kanji/剰.md:13-14. |
| D3 | 冗 | superfluous; redundant | 裕 | The article includes unnecessary excess and also technical redundancy that need not be faulty, repo/kanji/冗.md:21-44. | UNVERIFIED: not cleared by the negative primary gloss, because useful redundancy could concern spare capacity; no independent 冗 entry settles the direct pair. Neither endpoint declares it, repo/kanji/冗.md:1-14; snapshot/kanji/裕.md:13-14. |
| D4 | 満 | full; satisfy | 裕 | Independent meanings include full, fullness, enough and satisfy, evidence/kanjidic2-records.xml:450-476; the article also includes satisfaction, repo/kanji/満.md:19-39. | UNVERIFIED: sufficiency/fullness versus abundance/leeway needs a firmer boundary than the occupancy example alone. Neither endpoint declares the pair, repo/kanji/満.md:1-12; snapshot/kanji/裕.md:13-14. |
| D5 | 多 | many, much | 裕 | The actual broad quantity label is a defensible paraphrase of abundant, independently supported for 裕 in evidence/kanjidic2-records.xml:48-55. | Collision-needing-exclusion, F1. Neither endpoint declares 裕/多, repo/kanji/多.md:1-14; snapshot/kanji/裕.md:13-14. Not a current curated option for 裕. |
| D6 | 広 | wide, spacious | 裕 | Roominess overlaps the displayed spacious sense, repo/kanji/広.md:3-21; the independent supplied 裕 sections include ゆとり and the non-Joyo kun ひろい, evidence/external-snapshots/01-extract.txt:1-8; evidence/external-snapshots/01-extract.txt:38-68. | Collision-needing-exclusion, F1. Neither endpoint declares 裕/広, repo/kanji/広.md:1-12; snapshot/kanji/裕.md:13-14. Not a current curated option for 裕. This does not require adding a kun reading to pinned metadata. |
| D7 | 悠 | leisurely; distant | 裕 | The article includes unhurried, composed, easily and spatial/temporal extent, not only distant, repo/kanji/悠.md:21-47. | UNVERIFIED whether leeway makes leisurely/ease an ordinary 裕 answer or whether spatial extent supplies another collision. No direct pair on either endpoint; 悠's guards with 楽 and 広 are not transitive, repo/kanji/悠.md:13-14. Independent 悠 dictionary sections were not supplied. |
| D8 | 楽 | music, enjoyment, ease | 裕 | Ease and comfort are expressly distinguished from enjoyment, repo/kanji/楽.md:19-44. | UNVERIFIED for ease versus 裕's ゆとり; music alone is not the relevant comparison. No direct pair on either endpoint, repo/kanji/楽.md:1-12; snapshot/kanji/裕.md:13-14. The article's cited lexical entries were not supplied. |
| D9 | 栄 | flourish; glory | 裕 | The article explicitly includes prosperity and prosper, alongside glory, shine and appearance senses, repo/kanji/栄.md:19-35. | UNVERIFIED whether prosperity makes 裕's rich label defensible for 栄. Different headwords do not resolve this, and no independent 栄 entry was supplied. Neither endpoint declares the direct pair, repo/kanji/栄.md:1-12; snapshot/kanji/裕.md:13-14. |
| D10 | 資 | resources; capital | 裕 | The article includes funds/capital, information/materials and qualifications, repo/kanji/資.md:19-42. | UNVERIFIED for capital/resources versus riches. Information and qualifications do not eliminate its financial branch, and 資財 is whole-word evidence, not sufficient character allocation. Neither endpoint declares the pair, repo/kanji/資.md:1-12; snapshot/kanji/裕.md:13-14. |
| D11 | 宝 | treasure; valuables | 裕 | Treasure is independently attested with the 宝/財 spellings, evidence/jmdict-families.xml:1659-1691; the comparison article includes valuables and precious objects, repo/kanji/宝.md:3-21. | UNVERIFIED whether rich/riches and treasure/valuables create a defensible ordinary meaning choice. Treasure is not automatically abundance, but the shared 財 spelling prevents dismissing the issue by topic alone. No direct pair on either endpoint, repo/kanji/宝.md:1-12; snapshot/kanji/裕.md:13-14. |
| D12 | 金 | gold, money | 裕 | The article includes metal, gold, cash and money, and 金持ち as rich person, repo/kanji/金.md:19-38. | UNVERIFIED: 金持ち does not by itself establish rich as a constituent meaning, but money/wealth is not dismissed simply as noun versus adjective. Independent 金 lexical evidence is absent. Neither endpoint declares the pair, repo/kanji/金.md:1-12; snapshot/kanji/裕.md:13-14. |
| D13 | 充 | allot; fill | 裕 | Making sufficient and filling are explicit secondary meanings; the article also qualifies rare 充たす spelling, repo/kanji/充.md:21-43. | UNVERIFIED for sufficiency versus abundance. Allocation alone is not the strongest comparison, and no independent 充 evidence was supplied. Neither endpoint declares the direct pair, repo/kanji/充.md:1-14; snapshot/kanji/裕.md:13-14. |
| D14 | 足 | foot, leg | 裕 | The article explicitly includes enough/suffice and adding, besides feet and footwear counting, repo/kanji/足.md:19-38. | UNVERIFIED for enough versus 裕's plenty; foot/leg alone cannot clear the pair. Independent 足 lexical evidence is absent. Neither endpoint declares it, repo/kanji/足.md:1-12; snapshot/kanji/裕.md:13-14. |
| D15 | 濃 | concentrated; dark | 裕 | The article includes taste, density and intensity, repo/kanji/濃.md:19-40. Independent 濃厚 has rich flavor/color plus probability and passionate senses, evidence/jmdict-families.xml:1408-1448. | UNVERIFIED for the reverse-direction rich answer. The compound does not independently allocate rich to 濃, but different displayed titles cannot dismiss that ordinary English rendering. Neither endpoint declares the pair, repo/kanji/濃.md:1-12; snapshot/kanji/裕.md:13-14. |
| E1 | 厚 | thick; cordial | 裕 | JMdict's abundant sense is expressly restricted to 厚い, not its 篤い spelling, evidence/jmdict-families.xml:123-165; the displayed title is repo/kanji/厚.md:3. | Already handled: abundance is a real secondary collision despite the different title. Direct 裕/厚 declared on 裕 only, snapshot/kanji/裕.md:14; repo/kanji/厚.md:1-12. Not in 裕's curated options. |
| E2 | 富 | wealth; abundance | 裕 | Wealth and abundance are both displayed, repo/kanji/富.md:3-22; independent 富 and 富む cover riches/resources and being abundant/wealthy, evidence/jmdict-families.xml:1452-1530. | Already handled: direct semantic collision with abundant/rich. Direct 裕/富 declared on 裕 only, snapshot/kanji/裕.md:14; repo/kanji/富.md:1-12. Not in 裕's curated options. |
| E3 | 豊 | bountiful; abundant | 裕 | The title directly overlaps; independent 豊か includes plentiful/rich/ample, wealthy, relaxed, fullness and excess senses, evidence/jmdict-families.xml:1694-1757; repo/kanji/豊.md:3. | Already handled: direct 裕/豊 declared on 裕 only, snapshot/kanji/裕.md:14; repo/kanji/豊.md:1-12. The additional senses do not undo the direct abundance collision. Not in 裕's curated options. |
| E4 | 財 | wealth; property | 裕 | Independent 財 includes fortune/riches, goods and an abbreviation sense; the character record includes wealth/assets, evidence/jmdict-families.xml:702-736; evidence/kanjidic2-records.xml:755-795; repo/kanji/財.md:3. | Already handled: wealth/riches overlaps 裕's material-richness branch. Direct 裕/財 declared on 裕 only, snapshot/kanji/裕.md:14; repo/kanji/財.md:1-12. Not in 裕's curated options. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 裕 | CLEAN | CLEAN | NEEDS FIX | CLEAN | F1; evidence/kanjidic2-records.xml:1-80; evidence/external-snapshots/01-extract.txt:1-8; evidence/joyo-rows.json:1-15; snapshot/kanji/裕.md:1-49; diffs/existing.diff:1-13. Unsettled additional D comparisons are not cleared. |

The full ユウ metadata, empty kun list, seven KANJIDIC2 nanori and explicit practice selections agree with the pinned character record. Digital Daijisen independently supports ユウ and the abundance/leeway explanation; its different nanori list is identified as source-specific. Other Weblio sections are not merged into that dictionary: Wiktionary and the character-dictionary section supply additional readings, while the latter credits KANJIDIC2 for its English meanings and is not independent corroboration of those glosses. The NPO section is not linguistic evidence; the example section explicitly warns of machine-generated examples.

The complete applicable families support 富裕/ふゆう, 裕福/ゆうふく and 余裕/よゆう with the taught meanings. The supplied Joyo row independently associates ユウ with all three. 裕に remains marked irregular, rather than being recommended as ordinary 優に spelling; 裕度 is correctly kept as specialized electrical vocabulary. Fertile is directly present in KANJIDIC2, not independently expanded into an agricultural usage rule.

The C titles each occur once in the full index. 容's contain/form/looks branch is not abundance or room to spare: containing something is not having spare capacity. 補's supplement/supply/make-good/compensate branch and assistant/learner secondary meanings do not describe an abundant state. 複's duplicate/double/compound/multiple branch concerns multiplicity or composition, not a plentiful quantity. These bounded distinctions use the complete supplied character records, not only the comparison-card assertions: evidence/kanjidic2-records.xml:249-321; evidence/kanjidic2-records.xml:488-552; evidence/kanjidic2-records.xml:604-632. All three are defensible wrong options for 裕. No direct 裕/C exclusion is declared on either endpoint, and none is required by these demonstrated meanings.

For reading choices, 容 has ヨウ and い.れる, 補 has ホ and おぎな.う, and 複 has フク and no kun reading; none duplicates 裕's selected ユウ or its recorded nanori. This agrees with the opened character records and checks/reading-exposure.txt:6-21. The source-only/name-reading ゆ risk is separately limited below.

The sole wrapper changes bare 裕 to [裕](../kanji/裕.md) at the substantive component introduction in snapshot/words/余裕.md:24. Its target matches the new character card and its reciprocal 余裕 link; diffs/existing.diff:1-13 shows no other textual change. The complete changed article preserves its reading, level, title, examples and two senses.

The stroke JSON identifies 裕, schema 1, twelve sequential strokes, a 109-square view box and the pinned KanjiVG revision, consistent with the card and evidence/shape-evidence.json:1-51. The extracted group attributes support left 衤 as a form of 衣 and right 谷. This is a textual consistency review, not fresh geometry, stroke-animation or historical-phonetic acceptance.

The index was screened against abundant/abundance/plentiful, rich/wealth/prosperity, fertile/productive, and roominess/leeway/ease. Its exact abundant and wealth families include the guarded 富/豊/財; thick/cordial required opening 厚's secondary evidence. The D selection covers additional quantity, surplus, spatial, prosperity, resources, sufficiency and rich/intensity leads. Shared room/chamber labels such as 室 and 房, and agricultural topics such as 産 and 耕, do not alone establish the abstract abundance or fertility meaning; their full articles were not opened.

## Findings
### F1: Missing direct guards for quantity and spaciousness answers
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/裕.md:3-14; snapshot/kanji/裕.md:21-25; repo/kanji/多.md:1-14; repo/kanji/広.md:1-21; evidence/kanjidic2-records.xml:48-55; evidence/external-snapshots/01-extract.txt:1-8; evidence/external-snapshots/01-extract.txt:38-68; repo/docs/content-format.md:94-114
- Evidence: 裕 displays abundant and teaches roominess. Its independent character evidence gives abundant and ゆとり; the separately labeled Wiktionary section also lists non-Joyo ひろい. 多 displays the broad quantity answer many, much, which is defensible for abundance; 広 displays spacious, which is defensible for the documented roominess branch. These are semantic overlaps, not just shared topics. Neither endpoint declares 裕/多 or 裕/広. 裕 currently curates 容/補/複, so the demonstrated gap is a missing direct semantic safeguard, not a claim that either candidate appears in its current default options. The contract also covers fallbacks and reverse-direction choices, and existing exclusions involving third cards cannot supply either guard.
- Required change: Add direct 裕/多 and 裕/広 meaning-quiz exclusions on either endpoint, retaining three semantically distinct curated distractors. Do not alter the complete pinned reading metadata to implement a meaning-choice guard.

## Optional points
None.

## Limits
- L1: Raw stroke SVGs, the binary Joyo PDF, raw HTTP response and every other packet asset outside the supplied chains were unread. The full compressed dictionaries, original source-list bytes, manifest entries and exact served GitHub ZIP were not opened or independently hashed. Source hashes and snapshot identity are supplied provenance, not fresh byte verification.
- L2: D1-D4 and D7-D15 remain consequentially UNVERIFIED semantic dispositions, not harmless findings. The supplied target dictionary establishes abundance/leeway and richness but does not settle every surplus, sufficiency, ease, prosperity, capital or rich-intensity boundary. Most requested comparison articles lack independent applicable character/word entries in this packet. No new source retrieval or additional D/E request is authorized.
- L3: Identified but unread follow-up leads are 快, 安, 平, 寧, 静, 休, 息 and 凪, prompted by ease/calm comparisons in repo/kanji/悠.md:43-47. Their relationship to 裕 is unadjudicated: 悠's comparisons are not transitive exclusions, and composure in the whole word 余裕 does not automatically establish a calm/rest constituent sense of 裕. 室, 房, 宇 and 宙 were screened as room/space headword leads but not opened; a room or spatial domain is not itself roominess. 産 and 耕 were screened as fertility-related topics but not opened; production and cultivation do not alone prove fertile as a character meaning. No missing requested entry was reported.
- L4: The neutral index supplies titles, not independent dictionaries or full ordinary-sense coverage for all 1,244 cards. No exhaustive corpus-wide negative is claimed. No report, earlier adjudication, author rationale, changed checkout or session history was consulted.
- L5: checks/reading-exposure.txt:11-27 reports no exposed nanori in its bounded N1/All and single-borrow Starter models, but records latent ゆ risk and exposure when Starter additionally borrows 輸. This is not arbitrary/custom-pool, multiple-borrow, Kotlin execution, native/phone acceptance or compatibility with installed APK 5c000bd. JVM/emulator/device work was not performed. Meaning exclusions do not protect reading choices.
- L6: Supplied validation, unit, manifest, budget and vocabulary logs are not linguistic proof or fresh execution evidence. Local archive measurements are not exact served-ZIP acceptance, and the vocabulary pilot percentage is not whole-curriculum completion.
- L7: CLEAN facet verdicts are bounded absence of an established defect, not exhaustive historical, lexical-frequency, native-naturalness or whole-set certification. Model identity is the serving declaration only, without an independently inspected execution record.
