# B125 initial review — N1-B125-CLAUDE-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: 侵 metadata (title, strokes 9, radical 人 no. 9, grade 8, シン, おか.す) matches KANJIDIC2 and the 9-stroke KanjiVG JSON; word glosses, the 侵す harm/afflict sense, 進入 contrast and Joyo おかす row match the supplied JMdict, KANJIDIC2 and Joyo evidence; no established factual defect.

### Scoped coverage
Verdict: CLEAN
Basis: Both metadata readings appear in the reading table, the selected シン has a linked example, the unselected おか.す is explained, key compounds (侵入, 侵害, 侵す) are given, and the one required 侵入 link wrapper is present with no other change.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: The direct 侵–討 pair is declared on neither endpoint although 討's displayed title "attack; discuss" shares the head word "attack" that the 侵 card itself treats as ambiguity-bearing when excluding 攻 and 撃; both cards are jlpt-n1 so tag-preferring fallback can pair them (F1).

### Comprehensibility
Verdict: CLEAN
Basis: Card explains senses, the intransitive 侵入 vs 侵す, the unselected kun reading, labelled mnemonic, and the 侵入/進入 homophone in plain English with kana; no learner-blocking gap found.

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 (each read once, in order; no re-views)
Extension chain: 1, 2, 3, 4 (each read once, in order; no re-views)
Title index: I read evidence/title-index.txt source lines 1-1245 in full across core segments 17-19; line 1 is "一 one" and line 1245 is "齢 age; years lived".
Also read: REVIEW.md, packet.json, both rubric files, repo/docs/content-format.md lines 1-139, repo/docs/jlpt-levels.md, snapshot 侵 card and stroke JSON, diffs/existing.diff, snapshot/words/侵入.md, all ten checks, all listed evidence files, the three C distractor cards (寝, 進, 掃), the external-snapshot manifest and its one SUPPLIED Weblio extract.

## Phase-1 D/E lists
D: D1 討, D2 略, D3 占, D4 越, D5 損, D6 破, D7 違, D8 荒
E: E1 犯, E2 冒, E3 害, E4 攻, E5 撃, E6 入
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 討 | attack; discuss | 侵 | Shared head word "attack"; 討つ attack/defeat/conquer and 討伐 military subjugation (repo/kanji/討.md:21-33) vs 侵 raid/invasion and the card's own attack-based 攻/撃 exclusions (snapshot/kanji/侵.md:45) | Collision needing exclusion: pair declared on neither endpoint (repo/kanji/討.md:14; snapshot/kanji/侵.md:14); see F1 |
| D2 | 略 | abbreviate; omit | 侵 | 略 also has おか.す and a "taking or plundering" range (repo/kanji/略.md:10; repo/kanji/略.md:20), relatable to 侵 raid/invade | Harmless as a 侵 option (displayed title and ordinary senses are abbreviation); reverse 略-target risk is low and secondary; pair undeclared; see O2 |
| D3 | 占 | divine fortunes; occupy | 侵 | "occupy"/占領 taking possession could seem near invading territory (repo/kanji/占.md:20) | Harmless: 占 senses are fortune-telling and occupying/accounting for a share, not entering or encroaching (repo/kanji/占.md:20); pair undeclared and not needed |
| D4 | 越 | cross over; exceed | 侵 | Crossing a boundary vs trespassing/violating a border (repo/kanji/越.md:20-21) | Harmless: 越 gives neutral passing over a mountain or boundary and exceeding; no unauthorized or encroaching sense in its card (repo/kanji/越.md:20-22); pair undeclared and not needed |
| D5 | 損 | loss; damage | 侵 | 損なう/損ねる harm vs 侵す third sense harm/afflict (repo/kanji/損.md:20; snapshot/kanji/侵.md:34) | Low-risk: 侵's harm sense is a third, 冒す-xref'd sense not in its displayed title; pair undeclared; optional guard, see O1 |
| D6 | 破 | tear; break | 侵 | Break (rules/defenses) vs violate/infringe | Harmless: 破 card teaches tearing, breaking, destruction only (repo/kanji/破.md:20-22); no violating or invading sense displayed or taught; pair undeclared and not needed |
| D7 | 違 | differ | 侵 | Possible violate sense via 違反 vs 侵 violate | Harmless: card teaches difference/being wrong only (repo/kanji/違.md:20-21); "differ" does not plausibly answer invade/encroach; pair undeclared and not needed |
| D8 | 荒 | rough; wild; laid waste | 侵 | 荒らす lay waste and 荒らし robbery/vandalism suffix uses vs raid (repo/kanji/荒.md:20) | Harmless: 荒 concerns roughness/devastation, not entering another's domain (repo/kanji/荒.md:20); pair undeclared and not needed |
| E1 | 犯 | commit an offense | 侵 | Shared おか.す; 犯す violate a rule (repo/kanji/犯.md:20-21) and JMdict 1481550 violate | Already handled: declared on 侵 (snapshot/kanji/侵.md:14); 侵 Notes claim is supported |
| E2 | 冒 | brave danger; venture | 侵 | Shared おか.す and harm/affliction sense (repo/kanji/冒.md:46-49) | Already handled: declared on 侵 (snapshot/kanji/侵.md:14); 冒 card independently states the overlap |
| E3 | 害 | harm | 侵 | 侵す harm/afflict sense vs title "harm" (repo/kanji/害.md:20) | Already handled: declared on 侵 (snapshot/kanji/侵.md:14) |
| E4 | 攻 | attack; go on the offensive | 侵 | Attack/aggression vs invasion and 侵攻 (repo/kanji/攻.md:23) | Already handled: declared on 侵 (snapshot/kanji/侵.md:14); its logic also covers 討, see F1 |
| E5 | 撃 | shoot; strike | 侵 | Attack sense; 侵撃 invading and attacking (repo/kanji/撃.md:23) | Already handled: declared on 侵 (snapshot/kanji/侵.md:14) |
| E6 | 入 | enter, put in | 侵 | Entering vs intrusion; 侵入 component (repo/kanji/入.md:22) | Already handled: declared on 侵 (snapshot/kanji/侵.md:14); 侵入 article keeps the enter/intrude distinction |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 侵 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 and source-metadata records, JMdict 1359800/1359810/1359850/1366180/1481550/1519820, Joyo row, stroke JSON, Weblio Daijisen extract, 侵入 diff; F1, O1, O2 |

## Findings
### F1: Missing direct 侵–討 quiz exclusion
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: snapshot/kanji/侵.md:14; snapshot/kanji/侵.md:45; repo/kanji/討.md:3; repo/kanji/討.md:14; repo/kanji/討.md:21-33; repo/kanji/攻.md:3; evidence/title-index.txt:75
- Evidence: 侵 excludes 攻 "attack; go on the offensive" and 撃 because "an invasion can involve attack", but 討's displayed title "attack; discuss" carries the same head word, and its card glosses 討つ attack, defeat, conquer and 討伐 subjugation by military force. JMdict 侵 family includes raid, aggression and war of conquest. Neither 侵's nor 討's quiz_exclusions declares the direct pair; both are jlpt-n1, so fallback can show "attack; discuss" for 侵 or "invade; encroach" for 討, where invasion is arguably defensible for 討's military-attack sense. Exclusions are not transitive, so 攻/撃 do not cover it.
- Required change: Declare the direct pair (add 討 to 侵's quiz_exclusions or 侵 to 討's), with a short note on the shared attack/aggression sense, then validate and rebuild the manifest.

## Optional points
### O1: Consider guarding 侵–損 for the harm sense
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: snapshot/kanji/侵.md:34; snapshot/kanji/侵.md:44; repo/kanji/損.md:3; repo/kanji/損.md:20
- Evidence: The card excludes 害 for 侵す's harm/afflict sense; 損 "loss; damage" and 損なう harm partially overlap that sense. It is a third, 冒す-cross-referenced sense absent from 侵's title, so ambiguity is weak.
- Suggestion: Optionally declare 侵–損 or note why "damage" is not a defensible answer for 侵.

### O2: Note 略's おか.す/plunder range relative to 侵
- Facet: Consistency/quiz safety
- Severity: optional
- Confidence: low
- Citations: repo/kanji/略.md:10; repo/kanji/略.md:20; snapshot/kanji/侵.md:10
- Evidence: 略 shares the おか.す kun reading and its card mentions taking or plundering; 侵略 joins the two. With 略 as target, "invade; encroach" is a weak, secondary-sense candidate answer.
- Suggestion: Optionally declare 侵–略 if the plunder sense is considered ordinary enough; otherwise no change.

## Limits
- L1: Raw stroke SVGs, raw Weblio response HTML, the binary Joyo PDF, repo/docs/content-format.md beyond line 139, and every packet asset not in the chains were unread.
- L2: Identified but unread candidates: 戦 "battle" (excluded by 攻 and 討 but not by 侵), 暴 "violence; outburst", 軍 "army; troops", 領 "territory; jurisdiction", 突 "thrust; sudden", 汚 "dirty; defile". I judged their overlap weaker than the requested D items, but did not read their cards; 戦 is the most plausible further pair under the card's attack logic.
- L3: Automated checks (lint, validate, quiz-safety, reading-exposure, manifest, budget) are host/static evidence; reading exposure models bounded pools only, not custom or multi-borrow Starter pools, Kotlin, native/phone acceptance, or compatibility with installed APK 5c000bd, which predates quiz_exclusions.
- L4: Stroke JSON was checked only for count and source/revision agreement with the card and shape evidence; no visual geometry claim is made.
- L5: Execution model: the runtime reports Claude Opus 5.5; this identity is not independently verifiable from within the pass.
- L6: KANJIDIC2 meanings for D/E characters other than those in the core evidence (e.g. 略, 討) were not supplied; their dispositions rely on the cards' own text and the supplied JMdict families.
