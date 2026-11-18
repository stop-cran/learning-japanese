# B126 initial review — N1-B126-GPT-001

## Overall verdict
Verdict: CLEAN

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: The opened KANJIDIC2 record supports the full readings, radical, grade and stroke count. JMdict supports the displayed meanings, reading examples, voiced compounds, physical secondary senses and separately acknowledged からかさ spelling. The supplied Daijisen section independently supports the umbrella/parasol referent and compound reading. The shape explanation explicitly avoids historical claims.

### Scoped coverage
Verdict: CLEAN
Basis: Both metadata readings are explained; only the linked かさ example is selected for practice. The lesson covers the ordinary umbrella/parasol distinction, useful compounds, secondary object senses and the separate whole-word reading without demanding historical completeness or unrelated support articles.

### Consistency/quiz safety
Verdict: CLEAN
Basis: The three curated titles match their actual cards and the full title index, and none is a defensible umbrella answer. The four requested D comparisons establish no additional required direct pair; the broad cover/shelter comparison with 被 is already directly excluded on 傘. The changed word article has exactly the specified reciprocal link wrapper. Reading exposure is supported only within the supplied model's stated bounds.

### Comprehensibility
Verdict: CLEAN
Basis: The card separates metadata from practice, mnemonic from history, lampshade from darkness, and mushroom cap from headgear. Japanese examples have kana and glosses, the indexing radical's visible form is explained, and the linked word article provides an accessible concrete anchor.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23; no re-views.
Extension chain: 1, 2; no re-views.
Read evidence/title-index.txt source lines 1-1246 in full. Line 1 is "一 one"; line 1246 is "齢 age; years lived". All title senses and the supplied ordinary secondary senses of 傘 were compared against this index, including umbrella, parasol/sunshade, shade, cap, cover and their related English stems.
Read REVIEW.md before the other core sources; both rubric files, the specified content-format lines 1-139, the complete supplied JLPT policy, the new card and stroke JSON, the complete changed word article and diff, all ten check logs, all supplied metadata/dictionary/provenance evidence, all three C cards, and the external manifest and complete extract lines 1-894 were opened through the core chain.
Snapshot: 246a1319ef30414d73e4518b52ae99c1d700c57e. Base: ea9e1e364da4f3421a05d2a9706e5dcf44f0d797. This is one independent initial pass, with selection and review phases; no fixes or confirmation round.
Execution-model identity: GPT-6.1 Sol, model ID gpt-6.1-sol, as explicitly supplied by this session's runtime model metadata.

## Phase-1 D/E lists
D: D1 包, D2 帽, D3 暗, D4 影
E: E1 被
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 包 | wrap; enclose | 傘 | Requested cover/wrapping versus umbrella or lampshade. 包's article includes wrapping, enclosing, parcels, packaging, bandages and encirclement, not merely its title: repo/kanji/包.md:19-47. Independent character evidence includes the broader cover and conceal glosses: evidence/kanjidic2-records.xml:148-230. | Harmless for this direct meaning-choice pair. The broader cover gloss is acknowledged, but the displayed wrap/enclose operations are not translations of the independently attested umbrella, lampshade or mushroom-cap objects; conversely umbrella/parasol does not answer wrapping/enclosing. This is not a claim that 包 is confined to parcels or cannot describe covering. The physical object senses are explicit in evidence/jmdict-families.xml:16-28. Neither endpoint declares 傘/包: snapshot/kanji/傘.md:13-14; repo/kanji/包.md:1-12. Not a current curated option. |
| D2 | 帽 | hat; headgear | 傘 | Requested cap/headgear versus mushroom cap and conical-hat-shaped objects. The complete comparison includes the source-only おお.う reading as well as hat/cap, rather than silently discarding that reading: repo/kanji/帽.md:19-42. | Harmless. JMdict's 傘 secondary sense is something shaped like an umbrella or conical hat, with lampshade and mushroom-cap examples, not an assertion that 傘 ordinarily means worn headgear: evidence/jmdict-families.xml:21-28. Daijisen positively distinguishes the handled umbrella held overhead from 笠: evidence/external-snapshots/01-extract.txt:4-9. A source-only reading おお.う does not by itself establish an ordinary umbrella/parasol meaning for 帽. Neither endpoint declares 傘/帽: snapshot/kanji/傘.md:13-14; repo/kanji/帽.md:1-12. Not a current curated option. |
| D3 | 暗 | dark | 傘 | Requested shade/darkness versus lampshade. The comparison also includes memorization and gloomy, while the independent character record includes shade, disappear, informal and becoming dark or blinded: repo/kanji/暗.md:19-44; evidence/kanjidic2-records.xml:381-470. | Harmless. The independently supplied 傘 gloss explicitly specifies shade of a lamp, an umbrella-shaped object, whereas dark and the lighting-state shade do not name that object: evidence/jmdict-families.xml:21-28. Memorization, disappearance and the other supplied 暗 senses do not make umbrella/parasol a defensible reverse answer. This distinguishes the meanings of English shade, not merely the titles. Neither endpoint declares 傘/暗: snapshot/kanji/傘.md:13-14; repo/kanji/暗.md:1-12. Not a current curated option. |
| D4 | 影 | shadow; silhouette | 傘 | Requested shadow/shade versus parasol or lampshade. The full article additionally discusses reflected image, trace, light, remembered face/portrait, influence and photography: repo/kanji/影.md:21-47. | Harmless within the opened senses. A parasol produces shade, but is not a shadow or silhouette; JMdict identifies the 傘 extension as the shaped object, specifically a lamp's shade or mushroom cap: evidence/jmdict-families.xml:21-28. The article's further light/image/trace/effect senses do not identify an umbrella or parasol either. No independently asserted exhaustive restriction of 影 to darkness or abstraction is needed. Neither endpoint declares 傘/影; 影's exclusions involving third cards do not handle or determine this pair: snapshot/kanji/傘.md:13-14; repo/kanji/影.md:13-14. Not a current curated option. |
| E1 | 被 | cover; incur | 傘 | Requested assessment of the existing direct cover/shelter guard. Independent KANJIDIC2 evidence supplies cover, veil and shelter alongside incur, wear, put on, exposure and receiving: evidence/kanjidic2-records.xml:795-851. The complete card covers receiving kindness as well as harm and distinguishes native verbs and spelling/register flags: repo/kanji/被.md:19-47. | Already handled. The displayed cover alternative is broad enough to be defensible for a protective umbrella or physical lampshade, so retaining this conservative direct guard is justified by evidence/jmdict-families.xml:16-28 and evidence/external-snapshots/01-extract.txt:4-6. Incurring/receiving and wearing senses do not erase that overlap. The direct pair is declared on 傘 only, not 被: snapshot/kanji/傘.md:14; repo/kanji/被.md:1-12. It is therefore symmetric under repo/docs/content-format.md:103-108, not dependent on a third card. 被 is not a current curated option. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 傘 | CLEAN | CLEAN | CLEAN | CLEAN | Metadata and meaning: snapshot/kanji/傘.md:1-51; evidence/kanjidic2-records.xml:1-62; evidence/source-metadata.json:1-25. Reading/word support: evidence/jmdict-families.xml:1-44, 203-225, 241-259, 282-297, 387-406; evidence/joyo-rows.json:1-15; independently supplied Daijisen evidence/external-snapshots/01-extract.txt:4-16. The exact on-reading サン is supported by 傘下 and 落下傘; かさ is supported by the linked single-character word. 日傘 and 雨傘 support voiced がさ without inventing separate metadata. The separate からかさ entry is positively acknowledged, not dismissed as rare. D1-D4 and E1 above assess semantic pairs independently of current curated exposure. The stroke JSON has schema 1, the correct character, pinned revision, 12 consecutively identified strokes and stated viewBox; evidence/shape-evidence.json:1-106 and snapshot/strokes/傘.json:1 support textual consistency only. |

The three C options were checked against their full cards, the full index and independent character records, not just against the audit log. 金 displays "gold, money", also teaches metal, and has full readings キン・コン・ゴン / かね・かな-・-がね (repo/kanji/金.md:1-44; evidence/kanjidic2-records.xml:862-951). 全 displays "whole; complete"; its wider whole/entire/all/complete/fulfill senses and ゼン / まった.く・すべ.て do not answer 傘 (repo/kanji/全.md:1-45; evidence/kanjidic2-records.xml:63-147). 合 displays "fit together"; its fit/suit/join and measurement glosses, on-readings ゴウ・ガッ・カッ and full あう/あい/あわす/あわせる family do not answer 傘 (repo/kanji/合.md:1-47; evidence/kanjidic2-records.xml:231-315). Their title strings agree with evidence/title-index.txt:1-1246. None of their listed readings equals 傘's サン, かさ or independently attested whole-word からかさ. Neither endpoint declares a 傘 direct exclusion for any C option; none is required by these meanings. The visual-comparison rationale is a mnemonic distinction, not a new geometric or historical certification.

The one changed article was read completely. diffs/existing.diff:1-13 changes only the substantive-introduction occurrence 傘 into the relative link ../kanji/傘.md; snapshot/words/傘.md:1-33 confirms the target, preserved reading かさ, N5 word metadata, prose, examples and sections. The kanji's reverse word link is present at snapshot/kanji/傘.md:23-38. No vocabulary level is inferred from the new N1 kanji label, and no second wrapper or unrelated textual edit appears in the supplied diff.

All ten logs were read as supplied static evidence. checks/lint.txt:1-2, checks/quiz-safety.txt:1-16, checks/linkplan.txt:1, checks/unittest.txt:1-22 and checks/validate.txt:1 report the scoped structural outcomes. checks/manifest.txt:1 and checks/manifest-rebuild.txt:1 agree on version 54646f3d85c21fd3 and file count. checks/budget.txt:1 is a local archive measurement, not a served-ZIP or Android-limit certification. checks/vocabulary.txt:1 explicitly retains pilot coverage 2122/2431. checks/reading-exposure.txt:1-22 explicitly includes からかさ and reports no modeled production, padded-session or latent hit; it is not independent linguistic proof or Kotlin execution.

## Findings
None.

## Optional points
None.

## Limits
- L1: CLEAN means no actionable defect or consequential unresolved teaching claim was established in this bounded pass, not exhaustive linguistic correctness or complete N1 delivery. Source-row membership and source hashes were supplied in the packet evidence; the underlying full community-list dataset and compressed dictionaries were not independently reopened or hashed.
- L2: Raw stroke SVGs, binary Joyo PDF, raw HTTP response, fonts, all packet assets outside the chains, changed checkout and all prior reports/rationales remained unread. Stroke review is textual consistency against supplied source metadata, not fresh geometry, rendering, animation or PDF-glyph inspection.
- L3: Reading audits cover only the supplied N1/All pools and the specified single-borrow Starter model. Custom/caller-built pools, multiple borrowed cards, Kotlin/JVM execution, emulator/native/phone acceptance and compatibility with installed APK 5c000bd are unverified. No such work was attempted; that APK predates quiz_exclusions.
- L4: Index-only thematic leads 保・守・防 (protection), 冠 (crown), 屋・宇・軒 (roof/eaves), 灯 (lamp), 塗 (coat), and 竹・紙・笹 (materials or superficially related forms) were not requested or read as full cards. Shared function, material, shape or subject matter alone did not establish meaning-choice ambiguity. They receive no full-card semantic adjudication here. JMdict's 笠 cross-reference was read, but no 笠 article was read. No additional candidate was added after the selection boundary.
- L5: The supplied complete external extract was read, but source sections were not merged into one dictionary entry. The Daijisen entry supplies the material independent lexical corroboration; Wikipedia, historical slang, fiction catalogues and mechanically generated example sections do not establish ordinary modern meanings, historical completeness or model-sentence naturalness. No fresh external retrieval was performed.
- L6: Comparison-card secondary senses were considered in full as supplied; 影's additional dictionary claims have no separate raw 影 dictionary entry in these chains and are not independently certified here. The harmless direct-pair disposition does not depend on proving an exhaustive negative about 影: the independently established 傘 object sense differs from the displayed shadow/silhouette choice, and no supplied secondary sense establishes umbrella/parasol.
- L7: Static host results do not prove exact served archive acceptance, runtime manifest import, physical-device behavior or publication. No missing D/E entry was reported, and no report from another reviewer, session history, author rationale or confirmation evidence was accessed.
