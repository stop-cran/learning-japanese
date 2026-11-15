# B117 initial review — N1-B117-CLAUDE-001

## Overall verdict
Verdict: NEEDS FIX

## Facet verdicts
### Correctness
Verdict: CLEAN
Basis: Every checked metadata field, reading, stroke count, radical, nanori disposition, dictionary gloss and restriction on the four new cards matches the opened KANJIDIC2, JMdict, KanjiVG-derived stroke JSON, cached Joyo rows and Daijisen extracts; no incorrect Japanese claim was established. Bounded limits are in L1-L6.

### Scoped coverage
Verdict: CLEAN
Basis: Each card teaches its selected on reading with a linked word, preserves full source readings and nanori separately, and explains the compound-level meanings it uses; the omission of 紀's rules/discipline sense is recorded as optional (O1), not as a blocking gap.

### Consistency/quiz safety
Verdict: NEEDS FIX
Basis: Several direct pairs whose displayed titles overlap ordinary secondary senses of a new card are undeclared on either endpoint: 索/維 and 維/緒 (rope; cord), 紀/歴 (history), 索/捜 and 索/探 (search), and 賃/代, 賃/俸, 賃/給 (fee; wages; pay). See F1-F4. Other uncertain pairs are UNVERIFIED in the D/E table and L7.

### Comprehensibility
Verdict: CLEAN
Basis: Card prose is clear, mnemonics are labelled as modern-shape aids, whole-word versus character meanings are explicitly distinguished, and the four added links are placed at the substantive kanji explanations; one framing tension is optional (O2).

## Segments read
Core chain: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20 (each viewed once, in order; no re-views)
Extension chain: 1, 2, 3, 4, 5, 6, 7, 8, 9 (each viewed once, in order; no re-views)
Title index evidence/title-index.txt: I read source lines 1-1236 in full across core segments 15-17; line 1 is "一 one" and line 1236 is "齢 age; years lived".
The instruction file was read once at kickoff. No packet file was opened directly; all evidence came from the two chains. The report was written once and read back once.

## Phase-1 D/E lists
D: D1 歴, D2 期, D3 代, D4 規, D5 律, D6 則, D7 典, D8 法, D9 捜, D10 探, D11 査, D12 求, D13 調, D14 究, D15 散, D16 糸, D17 結, D18 括, D19 隅, D20 基, D21 給, D22 俸, D23 価, D24 値, D25 費, D26 払, D27 貨, D28 雇, D29 貸, D30 賞, D31 償, D32 税, D33 金
E: E1 史, E2 記, E3 誌, E4 録, E5 緒, E6 借, E7 料
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 歴 | history; passage of time | 紀 | KANJIDIC2 lists "history" for 紀 (evidence/source-metadata.json:22); Daijisen 紀 sense 3 is a history book (evidence/external-snapshots/01-extract.txt:9) | Collision needing exclusion (F2); not declared on 紀 (snapshot/kanji/紀.md:14) or 歴 (repo/kanji/歴.md:1-12, no field); 紀 already excludes 史 for the same "history" label |
| D2 | 期 | period; term | 紀 | 紀's JMdict single-character sense is "period" restricted to the geology field (evidence/jmdict-families.xml:534-538 range of entry 2205760); Daijisen 紀 sense 6 is a geological division (evidence/external-snapshots/01-extract.txt:12) | UNVERIFIED: the period sense is field-restricted (geology), so ordinary ambiguity is plausible but not established; undeclared on both sides (repo/kanji/期.md:1-12) |
| D3 | 代 | replace, era | 紀, 賃 | 代's own card states a "charge or fee" sense (repo/kanji/代.md:20); Daijisen 紀 sense 4 is 年代/era (evidence/external-snapshots/01-extract.txt:10) | 賃/代: collision needing exclusion (F4); undeclared (snapshot/kanji/賃.md:14; repo/kanji/代.md:1-12). 紀/代: UNVERIFIED, era is a Daijisen secondary sense of 紀 not in KANJIDIC2 (evidence/source-metadata.json:19-24) |
| D4 | 規 | standard; rule | 紀 | Daijisen 紀 sense 1 is established rules/discipline as in 紀律, 綱紀, 風紀 (evidence/external-snapshots/01-extract.txt:7); 規 is "rule" (repo/kanji/規.md:3) | UNVERIFIED: rules is Daijisen's first 紀 sense but absent from KANJIDIC2 English glosses (evidence/source-metadata.json:19-24) and 紀律 is a rare JMdict form; undeclared on either side; see O1 |
| D5 | 律 | law; rhythm | 紀 | Same 紀 rules/discipline sense (evidence/external-snapshots/01-extract.txt:7); 律 teaches 規律 discipline (repo/kanji/律.md:30) | UNVERIFIED for the same reason as D4; undeclared on either side |
| D6 | 則 | rule; follow a model | 紀 | Same 紀 rules sense (evidence/external-snapshots/01-extract.txt:7); 則 is a rule or standard (repo/kanji/則.md:20) | UNVERIFIED for the same reason as D4; undeclared on either side |
| D7 | 典 | reference texts; rules; ceremony | 紀 | Rules and recorded texts could overlap 紀 senses 1-3 (evidence/external-snapshots/01-extract.txt:7-9) | UNVERIFIED for the rules part as D4; the reference-text part is harmless: 典 means dictionaries, classics and models (repo/kanji/典.md:21-24), not a chronicle or account |
| D8 | 法 | law; method | 紀 | Rules/law overlap with 紀 sense 1 (evidence/external-snapshots/01-extract.txt:7) | Harmless at this evidence level: 法 is law or legislation and method (repo/kanji/法.md:19-21), while 紀 sense 1 is discipline or conduct rules, not law or method; undeclared |
| D9 | 捜 | search; look for | 索 | KANJIDIC2 gives 索 "searching" (evidence/source-metadata.json:47); Daijisen 索 sense 2 is searching, as in 検索 and 捜索 (evidence/external-snapshots/02-extract.txt:7) | Collision needing exclusion (F3); undeclared on 索 (snapshot/kanji/索.md:14) or 捜 (repo/kanji/捜.md:1-12) |
| D10 | 探 | search | 索 | Same 索 searching sense (evidence/external-snapshots/02-extract.txt:7); 探 is search (repo/kanji/探.md:3) | Collision needing exclusion (F3); undeclared on either side |
| D11 | 査 | investigate; inspect | 索 | KANJIDIC2 "inquiring" for 索 (evidence/source-metadata.json:48) | UNVERIFIED: Daijisen frames sense 2 as seeking via leads, not inspection (evidence/external-snapshots/02-extract.txt:7); the overlap between inquiring and investigating is not settled; undeclared |
| D12 | 求 | seek; request | 索 | Daijisen gives 索 the kun gloss もとめる and sense 2 探し求める (evidence/external-snapshots/02-extract.txt:5-7) | UNVERIFIED: seek overlaps the Daijisen sense, but もとめる is not a KANJIDIC2 or card reading and request does not apply; undeclared; reported with F3 |
| D13 | 調 | investigate; tune | 索 | 索 "inquiring" (evidence/source-metadata.json:48) | UNVERIFIED for the same reason as D11; undeclared |
| D14 | 究 | investigate thoroughly | 索 | 索 "inquiring" (evidence/source-metadata.json:48) | UNVERIFIED for the same reason as D11; 究 is research or deep study (repo/kanji/究.md:20-21); undeclared |
| D15 | 散 | scatter | 索 | Daijisen 索 sense 3: scattered and gone, as in 索然 and 索漠 (evidence/external-snapshots/02-extract.txt:8) | Harmless: that sense appears only in those literary compounds, and the card does not teach it; 散 is the ordinary verb sense of falling or scattering (repo/kanji/散.md:20-21) |
| D16 | 糸 | thread; yarn | 索, 維 | Daijisen 維 sense 2 is つな and 糸すじ, a thread strand (evidence/external-snapshots/03-extract.txt:20) | 索: harmless; 索 is a thick rope (evidence/external-snapshots/02-extract.txt:6), not thread. 維: UNVERIFIED; fiber and a thread strand are close, but "thread; yarn" (repo/kanji/糸.md:3) is not an established 維 gloss in KANJIDIC2 |
| D17 | 結 | tie; join; conclude | 維 | KANJIDIC2 "tie" for 維 (evidence/source-metadata.json:70); Daijisen つなぐ and つなぎとめる (evidence/external-snapshots/03-extract.txt:18-21) | UNVERIFIED, plausible collision: the 括 card excludes 結 for the same tying overlap (repo/kanji/括.md:14); undeclared on 維 (snapshot/kanji/維.md:14) or 結 (repo/kanji/結.md:1-14) |
| D18 | 括 | tie together; enclose | 維 | 維 "tie" (evidence/source-metadata.json:70) | UNVERIFIED, weaker than D17: 括 means bundling or enclosing (repo/kanji/括.md:20); undeclared on either side (repo/kanji/括.md:14) |
| D19 | 隅 | corner; nook | 維 | Daijisen 維 sense 4 すみ, as in 四維 (evidence/external-snapshots/03-extract.txt:22) | Harmless: that sense is limited to a specialized compound and is not in KANJIDIC2 (evidence/source-metadata.json:69-71) or the card |
| D20 | 基 | foundation; basis | 維 | Daijisen 維 sense 1: a great rope, the nation's foundation (evidence/external-snapshots/03-extract.txt:19) | Harmless: a figurative literary sense not in KANJIDIC2 or the card; 基 is a physical or abstract foundation (repo/kanji/基.md:22) |
| D21 | 給 | pay; bestow | 賃 | JMdict 賃 "wages", "payment" (evidence/jmdict-families.xml:572-573); 給 supplies pay in 給料 (repo/kanji/給.md:20-21) | Collision needing exclusion (F4); undeclared on 賃 (snapshot/kanji/賃.md:14) or 給 (repo/kanji/給.md:1-12) |
| D22 | 俸 | salary; stipend | 賃 | 賃 wages (evidence/source-metadata.json:96); Daijisen 賃: money received as payment for work (evidence/external-snapshots/04-extract.txt:11) | Collision needing exclusion (F4); undeclared on both sides (repo/kanji/俸.md:1-14) |
| D23 | 価 | worth; price | 賃 | Daijisen 賃 = 代価, the price paid for use (evidence/external-snapshots/04-extract.txt:7) | UNVERIFIED: a fee and a price can overlap, as 価's own exclusion of 費 for cost suggests (repo/kanji/価.md:14), but the opened evidence does not settle it; undeclared |
| D24 | 値 | value; price | 賃 | Same 代価 sense (evidence/external-snapshots/04-extract.txt:7) | UNVERIFIED for the same reason as D23; undeclared (repo/kanji/値.md:1-12) |
| D25 | 費 | expense; spend | 賃 | 賃 charge; 費 includes 学費 school expenses (repo/kanji/費.md:20-21) | UNVERIFIED: the expense and fee overlap is plausible but unsettled; undeclared on both sides |
| D26 | 払 | pay | 賃 | English "pay" as a noun means wages; 賃 includes wages and payment (evidence/jmdict-families.xml:572-573) | UNVERIFIED: 払 teaches only the verb (repo/kanji/払.md:20-21), but the displayed one-word label is ambiguous between verb and noun; undeclared |
| D27 | 貨 | goods; freight; currency | 賃 | JMdict 賃 "freight" (evidence/jmdict-families.xml:571) | Harmless: 賃's freight is a freight charge (運賃 freight rates), while 貨 means cargo, goods or currency (repo/kanji/貨.md:20) |
| D28 | 雇 | employ; hire | 賃 | KANJIDIC2 "hire" for 賃 (evidence/source-metadata.json:94) | Harmless: JMdict qualifies it as "hire (charge)" (evidence/jmdict-families.xml:566); 雇 is the act of employing (repo/kanji/雇.md:20) |
| D29 | 貸 | lend | 賃 | 貸す also means renting out (repo/kanji/貸.md:20), and 賃's displayed title includes "rent" | UNVERIFIED: when 貸 is the target, "fee; rent" could be read as the verb "rent (out)"; 賃 excludes 借 for "rent" (snapshot/kanji/賃.md:47), but 貸's displayed title lacks "rent"; undeclared |
| D30 | 賞 | prize; reward | 賃 | Daijisen 賃 報酬, remuneration (evidence/external-snapshots/04-extract.txt:7) | Harmless: 賞 is a prize, award or bonus for merit (repo/kanji/賞.md:20), not payment for labor or use |
| D31 | 償 | recompense; make amends | 賃 | 報酬 could be glossed "recompense" (evidence/external-snapshots/04-extract.txt:7) | Harmless: the paired "make amends" and the card fix the sense as compensation for loss (repo/kanji/償.md:3; repo/kanji/償.md:22-25) |
| D32 | 税 | tax; fiscal duty | 賃 | Charge or levy | Harmless: the 税 card states that a fee or charge is not necessarily a tax (repo/kanji/税.md:37) |
| D33 | 金 | gold, money | 賃 | Daijisen 賃: money paid (evidence/external-snapshots/04-extract.txt:7) | Harmless: 金 is metal, gold or money in general (repo/kanji/金.md:20); 賃 names a specific fee or rent payment, not money as such |
| E1 | 史 | history; chronicle | 紀 | Shared "chronicle" and "history" (evidence/source-metadata.json:19-22) | Already handled: declared on 紀 (snapshot/kanji/紀.md:14); justified |
| E2 | 記 | record in writing | 紀 | Daijisen 紀 senses 2-3: recording and recorded documents (evidence/external-snapshots/01-extract.txt:8-9) | Already handled: declared on 紀 (snapshot/kanji/紀.md:14); justified |
| E3 | 誌 | written record; journal | 紀 | Same record sense (evidence/external-snapshots/01-extract.txt:8-9) | Already handled: declared on 紀 (snapshot/kanji/紀.md:14); justified |
| E4 | 録 | record; register | 紀 | Same record sense (evidence/external-snapshots/01-extract.txt:8-9) | Already handled: declared on 紀 (snapshot/kanji/紀.md:14); justified |
| E5 | 緒 | cord; beginning | 索, 維 | Cord overlaps 索 rope and cord (evidence/source-metadata.json:45-46) and 維 rope (evidence/source-metadata.json:71) | 索/緒 already handled (snapshot/kanji/索.md:14). 維/緒 is a collision needing exclusion (F1); undeclared on 維 (snapshot/kanji/維.md:14) or 緒 (repo/kanji/緒.md:1-12) |
| E6 | 借 | borrow, rent | 賃 | Shared "rent" (repo/kanji/借.md:3) | Already handled: declared on 賃 (snapshot/kanji/賃.md:14); justified |
| E7 | 料 | materials, fee | 賃 | Shared "fee" (repo/kanji/料.md:3) | Already handled: declared on 賃 (snapshot/kanji/賃.md:14); justified |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 紀 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2 and JMdict 2205760; Daijisen extract 01; stroke JSON 9 strokes; F2; O1; D1-D8 and E1-E4 |
| 索 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2; JMdict 1298310 and 2833466; Daijisen extract 02; stroke JSON 10 strokes; F1; F3; D9-D16; E5 |
| 維 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2; JMdict 1391890 and 1628530; Daijisen extract 03; stroke JSON 14 strokes; F1; O2; D16-D20; E5 |
| 賃 | CLEAN | CLEAN | NEEDS FIX | CLEAN | KANJIDIC2; JMdict 2844192 and 1431990; Daijisen extract 04; stroke JSON 13 strokes; F4; D3; D21-D33; E6-E7 |

## Findings
### F1: 維 lacks direct exclusions against 索 (rope) and 緒 (cord)
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: evidence/source-metadata.json:69-71; evidence/source-metadata.json:45-46; evidence/external-snapshots/03-extract.txt:19-20; evidence/external-snapshots/02-extract.txt:6; snapshot/kanji/維.md:14; snapshot/kanji/維.md:23; snapshot/kanji/索.md:3; snapshot/kanji/索.md:14; snapshot/kanji/索.md:45; repo/kanji/緒.md:3
- Evidence: KANJIDIC2 gives 維 "fiber", "tie" and "rope", and the 維 card repeats this in its own Meaning
    section. Daijisen gives 維 the senses 大綱 and つな／糸すじ. 索's displayed title is "rope", and Daijisen glosses 索 as
    太い縄／つな. When 維 is the target, the option "rope" (索) is therefore defensible; "cord; beginning" (緒) is
    defensible for the same reason, and 索 already excludes 緒 because cord overlaps rope. Neither endpoint declares
    索/維 (維 has quiz_exclusions [], 索 has only 緒), and 緒 has no quiz_exclusions field. Exclusions are not transitive,
    so 索/緒 does not cover 維/緒. The current curated 維 options do not expose either pair, but All, level, custom and
    fallback pools can.
- Required change: Declare the direct pairs 索/維 and 維/緒 (for example, add 索 and 緒 to 維's quiz_exclusions),
    explain the rope/cord overlap in 維's Notes, then rerun validation and the manifest build.

### F2: 紀 excludes 史 for "history" but not 歴
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: evidence/source-metadata.json:19-24; evidence/external-snapshots/01-extract.txt:9; snapshot/kanji/紀.md:14; snapshot/kanji/紀.md:45; repo/kanji/歴.md:3; repo/kanji/歴.md:1-12
- Evidence: KANJIDIC2 lists "history" and "annals" among 紀's meanings, and Daijisen 紀 sense 3 is a recorded
    history book. 紀 already excludes 史 ("history; chronicle") because its English label overlaps, but 歴's displayed
    title "history; passage of time" has the same "history" head word and is undeclared on both endpoints. When 紀 is
    the target, "history; passage of time" is a defensible answer.
- Required change: Declare the 紀/歴 direct pair (add 歴 to 紀's quiz_exclusions), mention 歴 in the existing 紀
    exclusion note, then rerun validation and the manifest build.

### F3: 索's searching sense collides with 捜 and 探
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: medium
- Citations: evidence/source-metadata.json:44-48; evidence/external-snapshots/02-extract.txt:7; snapshot/kanji/索.md:23; snapshot/kanji/索.md:14; snapshot/words/索引.md:23; repo/kanji/捜.md:3; repo/kanji/探.md:3
- Evidence: KANJIDIC2 gives 索 the meanings "searching" and "inquiring", and Daijisen lists searching as an ordinary
    sense (検索・捜索・探索・模索). The 索 card cites this sense in its Meaning section, and the newly linked 索引 article
    says 索 "contributes searching or inquiring". 捜 ("search; look for") and 探 ("search") display that sense directly,
    yet no 索/捜 or 索/探 exclusion is declared on any endpoint. A learner who uses the card and the linked article could
    defensibly choose "search" for 索. Confidence is medium because "rope" is the displayed title and the searching sense is
    secondary; related investigate/seek pairs (査, 調, 究, 求) remain UNVERIFIED (L7).
- Required change: Declare the 索/捜 and 索/探 direct pairs, or record source-backed reasons why the searching sense
    is not an ordinary standalone meaning of 索, then rerun validation and the manifest build.

### F4: 賃 lacks exclusions against 代 (fee), 俸 (salary) and 給 (pay)
- Facet: Consistency/quiz safety
- Severity: medium
- Confidence: high
- Citations: evidence/jmdict-families.xml:566-573; evidence/source-metadata.json:92-97; evidence/external-snapshots/04-extract.txt:7; evidence/external-snapshots/04-extract.txt:11; snapshot/kanji/賃.md:14; snapshot/kanji/賃.md:23; repo/kanji/代.md:20; repo/kanji/俸.md:22; repo/kanji/給.md:20
- Evidence: JMdict and KANJIDIC2 give 賃 "fee", "charge", "wages" and "payment", and Daijisen also covers money received
    as payment for work. The 代 card itself teaches "a charge or fee" as a meaning, so "fee; rent" is defensible when 代
    is the target. 俸 ("salary; stipend") and 給 ("pay; bestow", the pay in 給料) display 賃's wages sense, so either is
    defensible when 賃 is the target. 賃 declares only 借 and 料, and 代, 俸 and 給 have no exclusions for 賃. Curated
    賃 options (任, 住, 仕) hide these pairs now, but fallback and other pools do not.
- Required change: Declare the 賃/代, 賃/俸 and 賃/給 direct pairs, extend 賃's exclusion note accordingly, then
    rerun validation and the manifest build.

## Optional points
### O1: 紀's rules/discipline sense is untaught
- Facet: Scoped coverage
- Severity: optional
- Confidence: medium
- Citations: evidence/external-snapshots/01-extract.txt:7; evidence/joyo-rows.json:11; snapshot/kanji/紀.md:23; snapshot/kanji/紀.md:41; snapshot/kanji/紀.md:47
- Evidence: Daijisen's first 紀 sense is established rules or discipline (紀律, 綱紀, 風紀), and the cached Joyo row
    gives 風紀 as an example. The card presents 紀 only as chronicle or account, and mentions 紀律 only as a rare
    spelling of 規律. KANJIDIC2's English glosses do not include this sense, so the omission is not a demonstrated defect.
- Suggestion: Add a short qualified note on 風紀/綱紀 and the discipline sense, then decide on source evidence
    whether 紀 should exclude 規, 律, 則 or 典 (left UNVERIFIED in the D/E table).

### O2: Align 維's link target with the 維持 article's character framing
- Facet: Comprehensibility
- Severity: optional
- Confidence: medium
- Citations: snapshot/words/維持.md:25; snapshot/kanji/維.md:23; snapshot/kanji/維.md:44; evidence/external-snapshots/03-extract.txt:21
- Evidence: The newly linked 維持 sentence says 維 "contributes holding together or sustaining". The 維 card says the
    maintenance sense belongs to the whole word unless established for the character. Daijisen sense 3,
    つなぎとめる「維持」, supports holding fast, so the two statements are compatible but read as contradictory.
- Suggestion: Add one clause to the 維 card noting Daijisen's "keep tied/hold fast" sense in 維持, while keeping
    "maintenance" as a whole-word meaning.

## Limits
- L1: Execution model: the runtime reports Claude Opus 5.5 (claude-opus-5.5); this identity was not independently verified
    by any tool in this pass.
- L2: Not read (outside chain-only access): raw KanjiVG SVGs, raw Weblio HTML responses, the binary Joyo PDF,
    repo/docs/content-format.md beyond line 139, the complete word corpus, the pinned source inputs listed in
    provenance.json, and every other packet asset not in the chains. Stroke JSON was checked only for stroke count,
    revision and schema against the cards and evidence; no visual geometry claim is made.
- L3: Joyo PDF pages (48/77/29/127) are consistent with cached printed pages (32/61/13/111) plus a constant offset of
    16; this rests on the cached text extraction, not a fresh PDF-glyph check.
- L4: JLPT N1 membership is supported only by packet sourceRows (packet.json) and the card labels; the n1 source
    snapshot itself was not opened. KANJIDIC2's historical jlpt value 2 for 賃 is an old pre-2010 level, not a modern
    N-level, and was not used either way.
- L5: The automated checks (lint, quiz-safety, linkplan, reading-exposure, unittest, validate, manifest, budget,
    vocabulary) are host/static evidence, not linguistic proof. Reading audits model limited pools only, not custom
    pools, multiple-borrow Starter behavior, Kotlin execution, native/phone acceptance, or the installed 5c000bd APK,
    which predates quiz_exclusions. JVM/emulator work was not performed.
- L6: The four link wrappers (diffs/existing.diff:9-10, :22-23, :35-36, :48-49) target ../kanji/紀.md, 賃.md, 索.md and
    維.md correctly and change nothing else; confirmed against the complete changed articles. Only the 紀/索/維/賃 C
    distractors and the D/E cards listed above were read; distractor titles and readings showed no collision or reading
    overlap (snapshot/kanji/*.md frontmatter; checks/reading-exposure.txt).
- L7: UNVERIFIED pairs, which the opened evidence cannot settle: 紀/期, 紀/代, 紀/規, 紀/律, 紀/則, 紀/典 (rules part);
    索/査, 索/求, 索/調, 索/究; 維/糸, 維/結, 維/括; 賃/価, 賃/値, 賃/費, 賃/払, 賃/貸. They do not change the facet
    verdict, which already rests on F1-F4.
- L8: Identified but not requested (to stay within plausible-ambiguity selection): 齢, 年, 世, 伝, 述, 編 (紀);
    線, 束, 漠 (索); 綿, 線, 続, 持, 保 (維); 額, 労, 資 (賃). I judged their overlap weaker than the requested set; they
    remain unread and unadjudicated.
- L9: Daijisen extracts are the only external sources, and Daijisen's per-character readings (for example 維 ユイ,
    索 もとめる) were used only as sense evidence, not as metadata corrections; KANJIDIC2 remains the metadata source.
