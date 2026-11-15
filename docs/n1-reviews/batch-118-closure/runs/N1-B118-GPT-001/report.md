# B118 initial review — N1-B118-GPT-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: The supplied KANJIDIC2 record supports the full metadata readings, radical, stroke count and analyze/divide/chop/tear meanings; the complete JMdict families and separately labelled Weblio sources support the taught vocabulary and qualified additional readings. The modern mnemonic does not claim historical derivation.

### Scoped coverage
Verdict: CLEAN
Basis: The sole new card explains its selected reading with linked analysis vocabulary, preserves its complete frozen metadata, explains the source-specific extras and includes the required sections. The sole existing-word change is a component-link wrapper, not a vocabulary expansion.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: F1 establishes missing direct 析/別 and 析/離 guards from the actual displayed separation labels and independently supplied character evidence. Other requested comparisons have explicitly unresolved semantic assessments; the bounded reading model and three current curated options do not establish arbitrary-pool meaning safety.

### Comprehensibility
Verdict: CLEAN
Basis: Analysis is explained through examining parts and relationships; Japanese vocabulary has kana and English glosses. Source-specific readings, the historical board noun, metadata and practice are distinguished, and the mnemonic is explicitly labelled non-etymological.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13; no re-views.
Extension chain: 1, 2, 3, 4; no re-views.
Read evidence/title-index.txt source lines 1-1237 in full. Line 1 is "一 one"; line 1237 is "齢 age; years lived".
Read REVIEW.md before the remaining core sources, all ten check logs, all four complete JMdict families, all three C cards, the external manifest and its one complete supplied extract.
Snapshot: dc2ee12623b36eb059d147ece2f2cfa3f87dfad7. Base: 42478f8000c1ee5c6f157202bef38f56de02d400.
Model: GPT-6.1 Sol, model ID gpt-6.1-sol, as identified by the serving runtime; no separate execution-record verification was performed.

## Phase-1 D/E lists
D: D1 別, D2 離, D3 断, D4 絶, D5 削, D6 折, D7 研, D8 究, D9 査, D10 調, D11 察, D12 考
E: E1 分, E2 解, E3 割, E4 切, E5 破, E6 剖, E7 板
Missing entries: none
D1 別 - 析: separate; divide into parts
D2 離 - 析: separate; detach
D3 断 - 析: sever; divide
D4 絶 - 析: sever; split apart
D5 削 - 析: chop; cut into smaller pieces
D6 折 - 析: split; break apart
D7 研 - 析: analyze; study closely
D8 究 - 析: analyze; investigate thoroughly
D9 査 - 析: analyze; investigate or inspect
D10 調 - 析: analyze; investigate
D11 察 - 析: analyze; examine and infer
D12 考 - 析: analyze; think over
E1 分 - Assess the declared direct guard for dividing and distinguishing senses.
E2 解 - Assess the declared direct guard for unravelling and analyzing complex things.
E3 割 - Assess the declared direct guard for splitting and dividing senses.
E4 切 - Assess the declared direct guard for cutting and chopping senses.
E5 破 - Assess the declared direct guard for tearing and breaking senses.
E6 剖 - Assess the declared direct guard for dissection and splitting senses.
E7 板 - Assess the declared direct guard for the separately sourced historical thin-board sense.
Eligibility was checked against the supplied exact reference: no D request is a new card, C distractor or existing exclusion target; every E request is an exclusion target and neither new nor a distractor.

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 別 | separate, another | 析 | The separate option overlaps independently attested fine division, not merely analysis as a shared topic: evidence/external-snapshots/01-extract.txt:4-7; repo/kanji/別.md:3. The article also covers difference and people parting, without restricting the displayed separate sense to people: repo/kanji/別.md:20-22; repo/kanji/別.md:41. | Collision-needing-exclusion, F1. No direct pair declared on either endpoint: snapshot/kanji/析.md:14; repo/kanji/別.md:1-12. |
| D2 | 離 | separate; detach | 析 | Separate is a defensible answer to the character's sourced divide/separate sense: evidence/kanjidic2-records.xml:51-54; evidence/external-snapshots/01-extract.txt:7; repo/kanji/離.md:3. Distance, departure and divorce are additional article uses, not a restriction eliminating its separation sense: repo/kanji/離.md:23-27. | Collision-needing-exclusion, F1. No direct 析 pair on either endpoint; 離's 別/分 guards are not transitive: repo/kanji/離.md:15; snapshot/kanji/析.md:14. |
| D3 | 断 | sever; refuse | 析 | Sourced chop/divide/tear makes sever a plausible overlap, while the article explicitly includes cut off, judgment, notice and permission: evidence/kanjidic2-records.xml:51-54; repo/kanji/断.md:20-22; repo/kanji/断.md:43-46. Independent comparison-character evidence establishing the applicable cutoff boundary is absent. | UNVERIFIED whether a further direct guard is required; not adjudicated harmless from refuse or judgment. No pair declared on either endpoint: repo/kanji/断.md:1-12; snapshot/kanji/析.md:14. |
| D4 | 絶 | sever; cease | 析 | Cut-off connection/flow and cessation, plus beyond-comparison usage, require consideration against chop/divide, not dismissal as exclusively abstract: repo/kanji/絶.md:20-22; repo/kanji/絶.md:31-38; evidence/kanjidic2-records.xml:51-54. No independent 絶 character entry was supplied. | UNVERIFIED whether sever creates a required direct collision; no pair on either endpoint: repo/kanji/絶.md:1-12; snapshot/kanji/析.md:14. |
| D5 | 削 | shave; sharpen; pare | 析 | Physical shaving/slicing and the historical thin split board create a plausible boundary question; reduction, deletion and figurative weakening must also be considered: repo/kanji/削.md:22; repo/kanji/削.md:31-32; repo/kanji/削.md:47-49; evidence/external-snapshots/01-extract.txt:12-15. A board noun does not itself establish a constituent shaving verb. | UNVERIFIED whether pare is an ordinary alternative for 析; no independent 削 entry settles the distinction and no direct guard is declared on either endpoint: repo/kanji/削.md:1-14; snapshot/kanji/析.md:14. |
| D6 | 折 | fold | 析 | Fold differs from the opened target glosses, but the comparison also teaches snapping and breaking by bending. That strongest secondary overlap cannot be discarded because fold is the title: repo/kanji/折.md:20-21; repo/kanji/折.md:30-39; evidence/kanjidic2-records.xml:51-54. | UNVERIFIED whether the secondary break sense requires a direct pair; the sources do not independently settle it. No pair on either endpoint: repo/kanji/折.md:1-12; snapshot/kanji/析.md:14. |
| D7 | 研 | polish; study closely | 析 | Study closely can plausibly describe analyzing complex material; sharpening, polishing and training do not erase that title sense: repo/kanji/研.md:3; repo/kanji/研.md:20-21; repo/kanji/研.md:30-37; evidence/external-snapshots/01-extract.txt:7. Independent 研 character evidence was not supplied. | UNVERIFIED whether the broad study label is a sufficiently ordinary alternative to require exclusion; not harmless merely because research is broader. No pair on either endpoint: repo/kanji/研.md:1-12; snapshot/kanji/析.md:14. |
| D8 | 究 | investigate thoroughly | 析 | Pursuing a subject deeply, mastering it and investigation to establish facts are the strongest relevant comparison senses: repo/kanji/究.md:20-21; repo/kanji/究.md:32-38. The independently supplied target means analysis and fine division, but does not establish an exclusive boundary with investigation: evidence/external-snapshots/01-extract.txt:7. | UNVERIFIED whether a direct guard is required; neither shared research compounds nor the broad label alone prove collision or harmlessness. No pair on either endpoint: repo/kanji/究.md:1-12; snapshot/kanji/析.md:14. |
| D9 | 査 | investigate; inspect | 析 | Examination/testing and information gathering can overlap; the article itself rejects an exclusive division: repo/kanji/査.md:20; repo/kanji/査.md:37. The target's analytical unpacking could be called examination, but independent 査 evidence is unavailable: evidence/external-snapshots/01-extract.txt:7. | UNVERIFIED whether the actual investigate/inspect option requires a direct guard; not harmless from a gather-versus-analyze slogan. No pair on either endpoint: repo/kanji/査.md:1-12; snapshot/kanji/析.md:14. |
| D10 | 調 | investigate; tune | 析 | Examine/check/look up is the potentially overlapping side; tone, condition and health are additional senses, not evidence that investigation excludes analysis: repo/kanji/調.md:20-22; repo/kanji/調.md:36-42; evidence/external-snapshots/01-extract.txt:7. No independent 調 article was supplied. | UNVERIFIED whether investigate is a defensible target option requiring a direct guard. No pair on either endpoint: repo/kanji/調.md:1-12; snapshot/kanji/析.md:14. |
| D11 | 察 | observe; infer | 析 | Looking closely and judging from clues may involve analysis, but related activities alone do not establish synonymy; police is another lexical use, not a semantic restriction: repo/kanji/察.md:20-22; repo/kanji/察.md:35-42; evidence/external-snapshots/01-extract.txt:7. Independent 察 evidence is absent. | UNVERIFIED whether the observe/infer label or secondary judge sense creates a required collision. No pair on either endpoint: repo/kanji/察.md:1-12; snapshot/kanji/析.md:14. |
| D12 | 考 | think over | 析 | Considering possibilities and forming judgments is the strongest overlap with analysis. The comparison expressly describes a tendency rather than a logical/emotional rule: repo/kanji/考.md:20-21; repo/kanji/考.md:43-44; evidence/external-snapshots/01-extract.txt:7. No independent 考 sense evidence resolves this boundary. | UNVERIFIED whether a direct guard is required; broad thinking is not automatically synonymous with analysis or proven harmless. No pair on either endpoint: repo/kanji/考.md:1-12; snapshot/kanji/析.md:14. |
| E1 | 分 | minute, part | 析 | The target's independently sourced fine division supports the potential part/division connection; the actual comparison additionally teaches divide, separate, understand and literary parting: evidence/external-snapshots/01-extract.txt:7; repo/kanji/分.md:20-21; repo/kanji/分.md:30-33. The minute sense alone would not settle this pair. | Already handled by the direct declaration on 析, not on 分: snapshot/kanji/析.md:14; repo/kanji/分.md:1-12. Guard is defensible; independent confirmation of every 分 secondary sense was not supplied. |
| E2 | 解 | unravel; solve | 析 | The displayed unravel matches the independently sourced 解きほぐす target sense. The comparison includes untying, solving, understanding and figurative analysis: evidence/external-snapshots/01-extract.txt:7; repo/kanji/解.md:3; repo/kanji/解.md:20-22; repo/kanji/解.md:39-44. Solving and understanding need not be identical for unravel to collide. | Already handled; the direct pair is declared on 析 only: snapshot/kanji/析.md:14; repo/kanji/解.md:1-12. |
| E3 | 割 | split; proportion | 析 | Split overlaps the independent divide gloss and fine-division sense; proportion and object breaking do not remove it: evidence/kanjidic2-records.xml:51-54; evidence/external-snapshots/01-extract.txt:7; repo/kanji/割.md:3; repo/kanji/割.md:20-22; repo/kanji/割.md:38-41. | Already handled; direct pair on 析 only: snapshot/kanji/析.md:14; repo/kanji/割.md:1-12. |
| E4 | 切 | cut | 析 | Chop is a kind of cutting, independently recorded for the target; the actual cut label remains defensible despite the comparison's end/disconnect and important/precious uses: evidence/kanjidic2-records.xml:51-54; repo/kanji/切.md:3; repo/kanji/切.md:20; repo/kanji/切.md:36-39. | Already handled; direct pair on 析 only: snapshot/kanji/析.md:14; repo/kanji/切.md:1-12. |
| E5 | 破 | tear; break | 析 | Tear is an exact independent target gloss. The comparison includes destruction and qualifies the breadth of break; no unrestricted word substitution is inferred: evidence/kanjidic2-records.xml:51-54; repo/kanji/破.md:3; repo/kanji/破.md:20-22; repo/kanji/破.md:36-38. | Already handled; direct pair on 析 only: snapshot/kanji/析.md:14; repo/kanji/破.md:1-12. |
| E6 | 剖 | dissect; split open | 析 | Splitting to examine is a plausible overlap with sourced dividing and analytical unpacking; the comparison also explicitly includes figurative analysis without making 剖 an independent general verb: evidence/kanjidic2-records.xml:51-54; evidence/external-snapshots/01-extract.txt:7; repo/kanji/剖.md:22; repo/kanji/剖.md:29-35; repo/kanji/剖.md:43. | Already handled by the direct pair on 析 only: snapshot/kanji/析.md:14; repo/kanji/剖.md:1-14. The guard is defensible; independent confirmation of 剖's figurative constituent meaning remains unavailable. |
| E7 | 板 | plank; board | 析 | The independent historical entry explicitly defines 析 as a thin split cedar/cypress board, making board defensible in that qualified sense. Glass plates, blackboards, printing blocks and signalling boards are also considered, not substituted for that narrow noun: evidence/external-snapshots/01-extract.txt:12-15; repo/kanji/板.md:3; repo/kanji/板.md:20; repo/kanji/板.md:39-41. | Already handled; direct pair on 析 only: snapshot/kanji/析.md:14; repo/kanji/板.md:1-12. This does not promote the historical noun to a general modern replacement for 板. |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 析 | CLEAN | CLEAN | NEEDS FIX | CLEAN | F1; snapshot/kanji/析.md:1-48; evidence/kanjidic2-records.xml:8-15; evidence/kanjidic2-records.xml:50-54; evidence/jmdict-families.xml:3-94; evidence/joyo-rows.json:6-10; evidence/external-snapshots/01-extract.txt:4-53; diffs/existing.diff:5-13. |

## Findings
### F1: Separation labels lack direct exclusions
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: evidence/external-snapshots/01-extract.txt:4-7; evidence/kanjidic2-records.xml:51-54; repo/kanji/別.md:3; repo/kanji/別.md:1-12; repo/kanji/離.md:3; repo/kanji/離.md:15; snapshot/kanji/析.md:13-14; repo/docs/content-format.md:100-120
- Evidence: The independent character entry defines 析 through fine division and disentangling complex material, and KANJIDIC2 independently includes divide. The actual displayed labels "separate, another" and "separate; detach" each include a defensible separation answer to that division sense. This is an overlap with the displayed choices, not a deduction from compound membership or shared subject matter. Neither endpoint declares 析/別 or 析/離. 析/分 and 離/分, and 離/別, do not transitively exclude these missing pairs. Neither comparison is among 析's three current curated distractors; that limits immediate default exposure but does not satisfy the direct-pair contract for fallback/custom meaning choices.
- Required change: Declare the direct 析/別 and 析/離 meaning-exclusion pairs on either endpoint, preserving the existing exclusions and the useful semantic distinctions. Do not claim that the characters' words become interchangeable.

## Optional points
None.

## Limits
- L1: CLEAN findings are bounded to the opened packet sources, not exhaustive linguistic or historical certification. Only the core and extension chains were read; no checkout, earlier report, rationale, session history or other packet was consulted. No content fixes or confirmation pass were performed.
- L2: D3-D12 remain consequential UNVERIFIED direct semantic assessments for the reasons in their table rows. Comparison cards establish their actual displayed labels and authored claims, but are not independent proof of all their character senses. Their linked dictionary entries were not supplied in the permitted chain. No harmlessness conclusion is substituted from first senses, different titles, compound status, exclusive-domain assumptions, part of speech or current curated exposure. The consistency facet is NEEDS FIX because F1 is established, not because these unresolved candidates are assumed to require guards.
- L3: Later-identified unread candidates include 盤 ("board; disc") against the supplied historical board sense, 片 ("one-sided; sheet") against the thin-board description and the whole-word alias 片木, and 刈 ("mow; reap") against chop. Their full cards were not requested in phase 1 and cannot be added now. Their title-index labels are screening evidence only; no collision or harmlessness is established. The alias 片木 does not automatically allocate the board meaning to 片. Other broad reasoning/examination labels such as 判 ("judge; seal"), 診 ("diagnose; examine medically"), 討 ("attack; discuss") and 試 ("test; try") were not opened; shared investigative activity alone does not establish a required pair.
- L4: C checks covered the actual titles new, book/origin and rest and their full articles: repo/kanji/新.md:3-10; repo/kanji/新.md:20-31; repo/kanji/本.md:3-10; repo/kanji/本.md:20-28; repo/kanji/休.md:3-10; repo/kanji/休.md:20-30. The entire index contains those exact titles on their respective cards, with no second identical title observed. New/fresh, book/origin/root/main/true/counter and rest/absence/break do not furnish an identified answer to the independently attested analyze/divide/chop/tear or historical board noun. The board noun is not the book label. All displayed C options are therefore harmless in this bounded target comparison; no direct pair is declared on either endpoint. Their シン, ホン and キュウ and listed kun forms do not overlap セキ or the supplied シャク/さく/へぎ extras. C-card historical origins and their unrelated pre-existing teaching were not independently certified.
- L5: For every D/E row, the semantic assessment precedes the exclusion disposition. All requested D/E cards are outside 析's current three curated options, and their opened curated lists likewise do not include 析. A missing direct pair identifies absent protection, not proof that a particular shipped session currently samples that choice. All E pairs are declared on 析; none is declared reciprocally in the opened E card. Reciprocation is not required.
- L6: The single wrapper was reviewed against the complete changed 分析 article: diffs/existing.diff:5-13 and snapshot/words/分析.md:1-34 show only 析 becoming [析](../kanji/析.md) in the component explanation. The target is the actual new kanji card, and the new card links back to this ぶんせき example. Metadata, readings, teaching prose and the existing word level are unchanged. JMdict supports analysis, parsing and chemistry separation/precipitation in their respective complete families, not an unrestricted transfer of senses among spellings. The irregular 解折 spelling remains distinct from ordinary 解析, and the search-only 析 spelling in entry 2139510 does not establish き or たく as practice readings.
- L7: Stroke JSON was reviewed only as text against the card, eight-stroke KANJIDIC2 record, canonical count and left 木/right 斤 group evidence: snapshot/strokes/析.json:1; evidence/kanjidic2-records.xml:8-15; evidence/shape-evidence.json:3-28. Eight sequential stroke records and the matching source revision support textual consistency. Raw SVGs, binary Joyo PDF, raw external HTML responses, original compressed dictionaries, full source-set assets and every other packet asset outside the chains remain unread. No fresh stroke-geometry, PDF-glyph, phonetic-history or visual-device claim is made.
- L8: The reading-exposure log models N1/All shipped pools and bounded Starter borrowing, recording no production hit but two latent reading collisions for source-specific シャク and さく: checks/reading-exposure.txt:1-30. This is supplied host-model evidence, not Kotlin execution, arbitrary caller/custom pools, multi-borrow Starter safety or physical-phone/native acceptance. Installed APK 5c000bd predates quiz_exclusions; compatibility is not claimed. JVM/Gradle/emulator/ADB work remains on hold and was not performed.
- L9: The ten static/host logs report clean scoped lint, structural validation, link accounting and 431 tests, matching manifest-build summaries, local budget data and pilot vocabulary coverage. They are not linguistic proof, a fresh manifest-byte comparison, an exact served GitHub ZIP check or publication approval. In particular checks/budget.txt:1 supplies local counts only; packaging/native acceptance is not inferred from it.
- L10: The N1 placement is treated as the packet's bounded community-study placement with source row 528 and pinned source provenance, not an official exam assignment or a fresh full-set membership audit: packet.json:21-23; evidence/source-metadata.json:24; evidence/provenance.json:5-8; repo/docs/jlpt-levels.md:18-22. All actual opened target metadata readings are preserved. Additional シャク, さく and historical へぎ are supported by their separate named source sections, not silently merged into the frozen KANJIDIC2 list. Machine-generated Weblio example lines 55-78 were read but are not used as independent naturalness certification.
