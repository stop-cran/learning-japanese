# B119 initial review — N1-B119-CLAUDE-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Metadata (strokes, radical, on readings, empty kun, JLPT, grade tag) of 妥 and 循 match the supplied KANJIDIC2 records, source-metadata.json and Joyo rows; meanings and source-only reading notes match KANJIDIC2 and the two Weblio extracts; stroke JSON counts and KanjiVG revision match; both link wrappers target the correct cards. No established factual defect.

### Scoped coverage
Verdict: CLEAN
Basis: Each card teaches its single Joyo on reading with a linked, dictionary-backed word (妥当 JMdict 1408540; 循環 JMdict 1341340), explains the empty kun metadata and qualifies source-only readings; the required body sections are present. Further compounds (妥協, 妥結, 悪循環) are optional, not required (O3).

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: Several direct pairs whose displayed titles share head words or stems with the new cards' titles or sourced secondary senses (settle/settled, follow/follow a model, peace, appropriate, gentle) are declared on neither endpoint (F1-F5). Curated distractors and the declared exclusions are otherwise sound.

### Comprehensibility
Verdict: CLEAN
Basis: Meaning paragraphs, labelled modern-shape mnemonics, reading tables and comparison notes are clear and qualified; the comparison notes I checked against the actual exclusion-target cards are supported by those cards.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4, 5, 6, 7, 8, 9 (each read once, in order; no re-views)
Title index evidence/title-index.txt: read source lines 1-1239 in full (core segments 11-13); line 1 is "一 one" and line 1239 is "齢 age; years lived".
All six curated distractor cards (女 母 子 休 人 本) were read in core segments 13-14; both Weblio extracts and the external-snapshot manifest were read in core segments 14-15.
The instruction file was read once at kickoff and not re-read; the report is read back once after writing.

## Phase-1 D/E lists
D: D1 了, D2 定, D3 済, D4 寧, D5 優, D6 快, D7 満, D8 決, D9 結, D10 柔, D11 凪, D12 応, D13 好, D14 治, D15 収, D16 落, D17 則, D18 倣, D19 準, D20 復, D21 転, D22 輪, D23 番, D24 次, D25 続, D26 通, D27 流
E: E1 当, E2 正, E3 良, E4 和, E5 静, E6 順, E7 追, E8 守, E9 後, E10 周
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 了 | completion; settling | 妥 | Title "settling" vs 妥 title "settled"; 了 body says a matter is understood and settled (repo/kanji/了.md:20) | Collision needing exclusion; declared on neither endpoint (了 has no quiz_exclusions, repo/kanji/了.md:1-12; 妥 list snapshot/kanji/妥.md:14); F1 |
| D2 | 定 | determine; settle | 妥 | Title "settle" vs "settled"; 定まる become settled (repo/kanji/定.md:33-39) | Collision needing exclusion; declared on neither endpoint; F1 |
| D3 | 済 | settle; finish | 妥 | Title "settle" vs "settled"; body: settled, finished, taken care of (repo/kanji/済.md:20) | Collision needing exclusion; declared on neither endpoint; F1 |
| D4 | 寧 | polite; peaceful | 妥 | 妥 KANJIDIC2 peace/gentle and Daijisen おだやかに落ち着く vs 寧 "peaceful" and "calm, settled peace" (repo/kanji/寧.md:23) | Collision needing exclusion; 寧 excludes 安 平 静 凪 和 but not 妥 (repo/kanji/寧.md:14), 妥 excludes the same peace cards but not 寧; F3 |
| D5 | 優 | gentle; superior | 妥 | 妥 KANJIDIC2 "gentle", taught in the 妥 card notes, vs 優 title "gentle" (kindness sense, repo/kanji/優.md:20-22) | Collision needing exclusion (medium confidence); declared on neither endpoint; F5 |
| D6 | 快 | pleasant; agreeable | 妥 | 妥 "satisfactory" vs "agreeable" | Harmless: 快 concerns a pleasant feeling (repo/kanji/快.md:20), not acceptability or fit; no sourced 妥 feeling sense |
| D7 | 満 | full; satisfy | 妥 | 妥 "satisfactory" vs "satisfy" (shared stem) | Harmless (medium): 満 is fullness and contentment as in 満足 (repo/kanji/満.md:20-22); 妥 satisfactory means acceptably fitting as in 妥当; no source gives 妥 fullness or contentment |
| D8 | 決 | decide | 妥 | 決まる become settled and settling something (repo/kanji/決.md:20-21) vs 妥 "settled" | Collision needing exclusion (medium confidence): the card itself glosses its sense as settling; declared on neither endpoint; F1 |
| D9 | 結 | tie; join; conclude | 妥 | 妥結 settlement; 結 brings to a conclusion (repo/kanji/結.md:22) | Harmless (medium): 結 body speaks of tying and concluding, not of being settled, appropriate or calm; the settlement meaning belongs to the compound 妥結 |
| D10 | 柔 | soft; supple | 妥 | 妥 gentle vs 柔 gentleness in 柔和 (repo/kanji/柔.md:20) | Harmless (low confidence): displayed "soft; supple" denotes physical softness and flexibility; gentleness appears only through 柔和; no exclusion declared on either endpoint |
| D11 | 凪 | calm seas; lull | 妥 | 妥 calmly settling vs calm | Harmless: 凪 is restricted to wind and sea and explicitly not every English use of calm (repo/kanji/凪.md:23-26); 妥's settling concerns matters (Daijisen 事がおさまる) |
| D12 | 応 | respond; comply | 妥, 循 | 応 Daijisen sense suitable or well matched (相応 suitable; appropriate), repo/kanji/応.md:25; 応 compliance vs 循 follow a rule | 妥: collision needing exclusion; 応 itself excludes 適 for that suitable sense (repo/kanji/応.md:14, repo/kanji/応.md:60) but neither endpoint declares 応/妥; F4. 循: UNVERIFIED (comply vs follow a rule), O2 |
| D13 | 好 | liking; favorable | 妥 | 妥 satisfactory vs favorable | Harmless: 好 concerns liking and preference (repo/kanji/好.md:20); favorable here is a feeling toward something, not acceptability |
| D14 | 治 | govern; heal | 妥 | 治める govern; settle (repo/kanji/治.md:38) vs 妥 事がおさまる | Harmless as displayed (low confidence): settle appears only as a secondary word gloss, displayed title is govern or heal; O1 |
| D15 | 収 | collect; store | 妥 | 収まる fit within; settle (repo/kanji/収.md:38) | Harmless as displayed (low confidence): settle is a secondary gloss of fitting into place; O1 |
| D16 | 落 | fall down | 妥 | 落ち着く in Daijisen gloss of 妥 | Harmless: 落 card teaches only falling and dropping (repo/kanji/落.md:20); 落ち着く is a Daijisen paraphrase, not a 落 sense taught here |
| D17 | 則 | rule; follow a model | 循 | Title "follow a model" and 則る follow a rule (repo/kanji/則.md:3, repo/kanji/則.md:20) vs 循 title "follow" and Daijisen 決まったルールにしたがう | Collision needing exclusion (high); 則 has no quiz_exclusions and 循 does not list 則 (snapshot/kanji/循.md:14); F2 |
| D18 | 倣 | imitate; emulate | 循 | 倣 is following an existing model; 倣う follow an example or precedent (repo/kanji/倣.md:23-24) | Collision needing exclusion (medium-high); declared on neither endpoint; F2 |
| D19 | 準 | standard, conform | 循 | Conformity to a model; 準じる conform to (repo/kanji/準.md:20) vs 循 follow a set rule | Collision needing exclusion (medium); declared on neither endpoint; F2 |
| D20 | 復 | restore; repeat | 循 | Repeat vs cycle | Harmless (medium): 復 is returning to an earlier state or doing again (repo/kanji/復.md:20); the 循環 article itself says mere repetition is not a cycle (snapshot/words/循環.md:33) |
| D21 | 転 | turn; roll | 循 | Turning vs going around; 循環 gloss rotation | Harmless (low confidence): 転 is turning, rolling or changing position (repo/kanji/転.md:20), not a circuit; but 循 excludes 回 for revolving, so O2 suggests review |
| D22 | 輪 | wheel; ring | 循 | Ring or loop vs cycle | Harmless (medium): 輪 names objects such as wheel, ring, circle or loop (repo/kanji/輪.md:20); 循 is a following or circulating process; loop is a whole-word gloss of 循環, not of 循 |
| D23 | 番 | turn in a series | 循 | 循 KANJIDIC2 sequential vs a turn within a series (repo/kanji/番.md:20) | UNVERIFIED: the 循 card treats sequence as exclusion-worthy for 順, while 番 is a position or turn number, not following; supplied evidence does not settle it; O2 |
| D24 | 次 | next | 循 | Sequence; next is following | Harmless (medium): 次 locates the next item in a sequence (repo/kanji/次.md:20); 循 follow means follow a rule or course, not being next |
| D25 | 続 | continue | 循 | Following on, forming a series (repo/kanji/続.md:20) | Harmless (medium): 続 is continuation in time; 循 follow concerns rules or a circuit; continue is not a defensible meaning answer for 循 in the opened sources |
| D26 | 通 | pass through; commute | 循 | Circulation sense of 通う excluded at word level by 循環 | Harmless: 通 card teaches passage, connection and repeated trips (repo/kanji/通.md:20), not a cycle; the 循環/通う word exclusion is word-level only |
| D27 | 流 | flow | 循 | Circulation vs flow | Harmless: 流 is flowing or a current (repo/kanji/流.md:20); no cycle or following sense |
| E1 | 当 | hit; be on target | 妥 | 妥 note cites 当 for appropriateness | Already handled: 当 body says right or appropriate (repo/kanji/当.md:20); declared on 妥 (snapshot/kanji/妥.md:14) |
| E2 | 正 | correct, proper | 妥 | 妥 note cites 正 for proper or right | Already handled: 正 body supports proper and right (repo/kanji/正.md:20); declared on 妥 |
| E3 | 良 | good; favorable | 妥 | 妥 note cites 良 for a satisfactory condition | Already handled: 良好 favorable; satisfactory condition (repo/kanji/良.md:20-21); declared on 妥 |
| E4 | 和 | harmony; Japanese style | 妥 | 妥 note cites 和 for peace | Already handled: 和 signals harmony or peace (repo/kanji/和.md:20); declared on 妥 |
| E5 | 静 | quiet | 妥 | 妥 note cites 静 for becoming quiet | Already handled: 静まる quiet down supports the claim (repo/kanji/静.md:20); declared on 妥 |
| E6 | 順 | order; sequence | 循 | 循 note cites sequence and obedience | Already handled: sequence title and recorded obedient sense (repo/kanji/順.md:44); declared on 循 (snapshot/kanji/循.md:14) |
| E7 | 追 | chase; pursue | 循 | 循 note cites following | Already handled: following after something (repo/kanji/追.md:20); declared on 循 |
| E8 | 守 | guard; obey | 循 | 循 note cites following a rule | Already handled: keeping a rule; 守る follow a rule (repo/kanji/守.md:20); declared on 循 |
| E9 | 後 | behind, after | 循 | 循 note cites position behind or time after | Already handled (conservative): 後 behind, after, later (repo/kanji/後.md:20); declared on 循 |
| E10 | 周 | circumference; circuit | 循 | 循 note cites circuit | Already handled: going around (repo/kanji/周.md:20); declared on 循 |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 妥 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 record, source-metadata, Joyo row, Weblio extract 01, strokes JSON, diff wrapper; F1, F3, F4, F5; O1, O3 |
| 循 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 record, source-metadata, Joyo row, Weblio extract 02, strokes JSON, diff wrapper; F2; O2, O3 |

## Findings
### F1: 妥 lacks direct exclusions with settle-titled cards
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/妥.md:3; snapshot/kanji/妥.md:14; repo/kanji/了.md:3; repo/kanji/了.md:20; repo/kanji/定.md:3; repo/kanji/定.md:33-39; repo/kanji/済.md:3; repo/kanji/済.md:20; repo/kanji/決.md:20-21; evidence/external-snapshots/01-extract.txt:8
- Evidence: 妥 displays "appropriate; settled", and Daijisen glosses 妥 as おだやかに落ち着く and 事がおさまる. 了 displays "completion; settling", 定 "determine; settle", 済 "settle; finish"; 決's body glosses its sense as settling and 決まる becoming settled. For prompts 了, 定 and 済 the option "appropriate; settled" shares the settle head word, and for prompt 妥 "settle; finish" or "determine; settle" is defensible from the shared English word. None of these pairs is declared on either endpoint (妥's list omits them; 了, 定, 済, 決 carry no quiz_exclusions). They are not current curated options, but tag/random fallback and custom pools can draw them.
- Required change: Add direct exclusions 妥–了, 妥–定 and 妥–済 (on 妥 or the other endpoint), and decide 妥–決 explicitly (exclusion recommended); optionally note the settle-sense distinctions in the 妥 card body.

### F2: 循 lacks direct exclusions with follow-a-rule/model cards
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: snapshot/kanji/循.md:3; snapshot/kanji/循.md:14; repo/kanji/則.md:3; repo/kanji/則.md:20; repo/kanji/倣.md:23-24; repo/kanji/準.md:3; repo/kanji/準.md:20; evidence/external-snapshots/02-extract.txt:7
- Evidence: 循 displays "follow; cycle", and Daijisen's first sense is 決まったルールにしたがう (follow a set rule); KANJIDIC2 glosses follow. 則 displays "rule; follow a model" and 則る means follow a rule or precedent; 倣 is following an existing model (倣う follow an example or precedent); 準 displays "standard, conform" and 準じる conform to. The 循 card already excludes 守 for following a rule and 追 for following, so these closer pairs are inconsistent omissions. None is declared on either endpoint. Confidence is high for 則, medium-high for 倣, medium for 準.
- Required change: Add direct exclusions 循–則 and 循–倣, and 循–準 unless an explicit evidence-based reason for keeping it is recorded; mention the follow-a-rule overlap in the 循 notes.

### F3: 妥–寧 peace overlap is undeclared
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/妥.md:43; snapshot/kanji/妥.md:14; repo/kanji/寧.md:3; repo/kanji/寧.md:14; repo/kanji/寧.md:23; evidence/kanjidic2-records.xml:57-58
- Evidence: The 妥 card teaches KANJIDIC2 peace and gentleness and excludes 安, 和 and 平 for peace. 寧 displays "polite; peaceful" and describes calm, settled peace; 寧 excludes 安, 平, 静, 凪 and 和 but not 妥. By the 妥 card's own criterion (peaceful titles excluded), the direct 妥–寧 pair needs the same handling, and 寧's "calm, settled" wording overlaps 妥's settled title.
- Required change: Add the direct exclusion 妥–寧 on either endpoint and add 寧 to the 妥 peace comparison note.

### F4: 妥–応 appropriateness overlap is undeclared
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/妥.md:3; snapshot/kanji/妥.md:42; repo/kanji/応.md:14; repo/kanji/応.md:25; repo/kanji/応.md:60
- Evidence: 応's own card records Daijisen's suitable or well-matched sense (相応 suitable; appropriate) and excludes 適 "suitable" for it. 妥's displayed title is "appropriate", and 妥 likewise excludes 適 for appropriateness. For prompt 応, the option "appropriate; settled" is defensible through that recorded sense; the direct 妥–応 pair is declared on neither endpoint.
- Required change: Add the direct exclusion 妥–応 on either endpoint, or record why the secondary 相応 sense does not make "appropriate" defensible for 応.

### F5: 妥–優 gentle overlap is undeclared
- Facet: Consistency/quiz safety
- Severity: low
- Confidence: medium
- Citations: snapshot/kanji/妥.md:43; evidence/source-metadata.json:19-24; repo/kanji/優.md:3; repo/kanji/優.md:20-22
- Evidence: The 妥 card explicitly teaches that KANJIDIC2 includes gentleness for 妥 and excludes 温 for mildness. 優 displays "gentle; superior". For prompt 妥, a learner who read the card's gentleness note can defend "gentle; superior"; no exclusion is declared on either endpoint. The kindness sense of 優 differs from 妥's calm sense, which is why confidence is only medium.
- Required change: Add the direct exclusion 妥–優, or remove or qualify the gentleness association in the 妥 notes and record why 優 is harmless.

## Optional points
### O1: Secondary settle glosses of 治 and 収
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: repo/kanji/治.md:38; repo/kanji/収.md:38; evidence/external-snapshots/01-extract.txt:8
- Evidence: 治める is glossed "govern; settle" and 収まる "fit within; settle"; Daijisen's 妥 gloss 事がおさまる uses the same おさまる idea. Displayed titles (govern; heal / collect; store) do not share the head word, so I treat them as harmless with low confidence.
- Suggestion: Consider recording the おさまる overlap and deciding these pairs explicitly when F1 is addressed.

### O2: Borderline 循 pairs with 応, 番 and 転
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/循.md:42-43; repo/kanji/応.md:3; repo/kanji/番.md:3; repo/kanji/番.md:20; repo/kanji/転.md:20
- Evidence: 循 excludes 順 for sequence and 回 for revolving. 番 "turn in a series" marks a position in a sequence, 転 "turn; roll" is turning, and 応 "respond; comply" overlaps following a demand. The supplied evidence does not settle whether these displayed labels are defensible answers for 循.
- Suggestion: Record an explicit disposition for 循–番, 循–転 and 循–応; exclude any judged defensible.

### O3: Optional recognition compounds
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/joyo-rows.json:10; evidence/joyo-rows.json:19; evidence/external-snapshots/01-extract.txt:8; evidence/external-snapshots/02-extract.txt:55
- Evidence: The Joyo rows list 妥協 and 妥結 for 妥 and 因循 for 循; the Weblio examples show 妥協 and 悪循環 in frequent use. The cards teach only 妥当 and 循環, which satisfies the scoped contract.
- Suggestion: Optionally add 妥協 (compromise) and 悪循環 (vicious circle) as plain-text recognition words.

## Limits
- L1: Execution-model identity is unverified; the runtime reports Claude Opus 5.5, but I cannot independently verify it.
- L2: Raw stroke SVGs, raw Weblio HTML responses, the binary Joyo PDF and all other packet assets outside the two chains were not read; stroke JSON was checked only for count, revision and consistency with card and evidence text, with no visual geometry claim.
- L3: Exclusion targets not requested in E (適, 安, 平, 温, 回) were judged only from their index titles; their card text was not read.
- L4: Identified but unread candidates (not selected as less plausible): 理 reason (reasonable), 協 cooperate (妥協), 軟 soft, 康 well-being, 承 accept, 肯 consent, 経 pass through, 律 law; rhythm, 再 again; repeat, 連 link, 期 period, 季 seasons, 第 ordinal prefix, 道 road, way. Characters such as 従, 遵, 随, 巡, 環, 穏, 宜 and 可 have no card in the title index.
- L5: dictionary-index.json and jmdict-families.xml include 徳 and 道徳 entries whose purpose is not explained in the packet; I did not use them in any conclusion.
- L6: Check logs are host/static evidence. The reading-exposure audit models limited pools only, not custom or multi-borrow Starter behavior, Kotlin execution, native or phone acceptance, or compatibility with installed APK 5c000bd, which predates quiz_exclusions. JVM/emulator work remains on hold.
- L7: Dispositions rely on the supplied cards, KANJIDIC2, JMdict families and two Weblio extracts only; no fresh dictionary lookup was possible, so harmless dispositions marked low confidence remain judgments rather than proofs.
