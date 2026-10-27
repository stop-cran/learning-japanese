## Snapshot:

**Revised commit:** `6244a236f9ba26870928c7721f16903b367cbdae`

**Parent/authored commit:** `c2e4e07abeda5bd28c12d0b3f9b0102212d2ae88`

Committed content only, as identified by the supplied frozen snapshot. File-only tools cannot execute Git: I did not independently verify HEAD, worktree cleanliness, hashes, or byte-preservation assertions. Those checks remain author-executed.

## Scope:

**Model:** GPT-6.1 Sol (`gpt-6.1-sol`, family `gpt`), continuing the original review session. **Read-only:** no edits, shell, agents, or delegation. All tool calls were serial, with no scheduling deviation.

Fresh complete reads covered both patches and the reconciliation; both instruction files; the required content-format and CW091 ranges; all twenty current assigned articles; complete `kanji\蒸.md`; twenty historical mappings; twenty principal families/32 senses; 33 component records; all 290 comparison labels; the TSV header and exactly physical lines 1622–1641; the correction rendering’s 44 complete families/102 senses; complete frozen Japanese public bodies; and all nineteen specified older articles. All five requested American Heritage entries were freshly fetched successfully, and their complete applicable lexical bodies inspected.

Inherited evidence includes the original review’s **374 complete families/949 senses and 167 existing word bodies, including both reuses**. These overlapping historical reads are not fresh confirmation reads or prepared-availability counts. I did not reopen prohibited ledgers, rationale packets, reviewer reports, or private directories. The optional correction receipts were unnecessary and were not read.

## Verdicts:

**The original three GPT findings are resolved. No remaining actionable defect or consequential unresolved linguistic claim was established within this scope.**

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1622 | 見慣れる | CLEAN | CLEAN | CLEAN | Visual familiarity, ichidan forms, and qualified spelling recognition remain sound. |
| N2:1623 | 醜い | CLEAN | CLEAN | CLEAN | Rare 見憎い correctly identified; useful 美しい link added. |
| N2:1624 | 実る | CLEAN | CLEAN | CLEAN | Three fruit-label guards added; godan forms and successful-fruition distinction retained. |
| N2:1625 | 身分 | CLEAN | CLEAN | CLEAN | Status, identity/origin, and circumstances remain differentiated. |
| N2:1626 | 見本 | CLEAN | CLEAN | CLEAN | Sample/model coverage and native-first mixed-reading explanation retained. |
| N2:1627 | 見舞う | CLEAN | CLEAN | CLEAN | Sympathetic inquiry and harmful-event constructions remain distinguished. |
| N2:1628 | 未満 | CLEAN | CLEAN | CLEAN | Boundary exclusion remains exact; source-gloss prose improved without broadening meaning. |
| N2:1629 | 名字 | CLEAN | CLEAN | CLEAN | 苗字 recognition, name-order guidance, and 名前/氏 distinctions retained. |
| N2:1630 | ミリ | CLEAN | CLEAN | CLEAN | Metric prefix and length abbreviation separated; bounded French-source fact retained. |
| N2:1631 | 診る | CLEAN | CLEAN | CLEAN | Direct 確かめる guard added; medical scope and pulse example remain clear. |
| N2:1632 | 民間 | CLEAN | CLEAN | CLEAN | Non-governmental and folk uses remain appropriately qualified. |
| N2:1633 | 民謡 | CLEAN | CLEAN | CLEAN | Traditional transmission is not incorrectly made an absolute authorship rule. |
| N2:1634 | 向かう | CLEAN | CLEAN | CLEAN | N4 identity retained; new alias paragraph links the distinct むこう noun. |
| N2:1635 | むく | CLEAN | CLEAN | CLEAN | Three skin-label guards added; both spellings/senses retained; を roles clarified. |
| N2:1636 | 無限 | CLEAN | CLEAN | CLEAN | Modifier attachment and infinity/eternity uses retained without a categorical 無数 divide. |
| N2:1637 | 無地 | CLEAN | CLEAN | CLEAN | Patternlessness, の attachment, and color/design distinctions remain clear. |
| N2:1638 | 蒸し暑い | CLEAN | CLEAN | CLEAN | Six disputed guards are supported by bare English weather alternatives, not Japanese synonymy. |
| N2:1639 | 矛盾 | CLEAN | CLEAN | CLEAN | Intransitive construction, rare spelling, and attributed origin account remain bounded. |
| N2:1640 | 蒸す | CLEAN | CLEAN | CLEAN | Both constructions and existing exclusions preserved; original addition remains sourced `jlpt: 2` only. |
| N2:1641 | 無数 | CLEAN | CLEAN | CLEAN | Countless abundance remains distinct from a mathematical assertion without a finite-only rule. |

**Mappings — CLEAN.** All twenty source associations, raw fields, selected one-based senses, and additional recognition agree across the inspected records and current teaching. 向う/むかう remains entry **1604800**, not 向こう/むこう **1277140**. 剥く maps to usually-kana むく **1474370**, recognizes 剝く, and is not confused with 向く or すく. Additional senses are not presented as independently sourced N2 assignments.

**Components and reciprocal links — CLEAN.** All primary written Han are included in metadata; kana-primary むく appropriately has `kanji: []`. Useful existing component links are present without inventing absent character cards. The new **蒸し暑い↔蒸** pair and existing **蒸す↔蒸** pair are present, including `kanji\蒸.md:32,38–39`.

**Kanji, CW091, and baseline preservation — CLEAN on the inspected textual evidence.** The related patch preserves 蒸’s metadata and unrelated teaching while adding the 蒸し暑い example, common-word link, and source entry. CW091’s change is only the 診る link at `docs\confusable-words.md:260`. The supplied diffs, fresh current bodies, and inherited baseline reads show 向かう retaining N4, stable identity and all original teaching; its correction changes only the new alias paragraph. 蒸す remains unchanged from the authored snapshot and differs from the original parent only by its sourced level. This is textual review, not independently executed byte-equivalence verification.

## Findings:

- **GPT-01 — Resolved.** Former **Minor / Correctness—quiz** defect at `words\実る.md:9`. The three direct guards to 実, 果物, and 果実 are present. Their complete actual titles contain **fruit**; the freshly inspected [American Heritage fruit entry](https://www.ahdictionary.com/word/search.html?q=fruit) explicitly records the produce-fruit verb. Complete JMdict families **1320850, 1320810, 1193060, 1192940** preserve the distinct Japanese verb and noun identities. The minimal remedy is implemented; no fruit-category clique is implied. **Confidence: high.**

- **GPT-02 — Resolved.** Former **Minor / Correctness—quiz** defect at `words\診る.md:9`. The direct 確かめる guard is present. Its actual title, **check; make sure**, can answer 診る’s explicitly taught pulse/condition-checking use. Complete families **1365450** and **1205780**, the older article, and [American Heritage check](https://www.ahdictionary.com/word/search.html?q=check), transitive **1a–b**, support that English overlap. No edge is inferred transitively through 確認 or チェック. **Confidence: high.**

- **GPT-03 / Claude B82-01 — Resolved.** Former **Minor / Correctness—quiz** defect at `words\むく.md:9`. All three direct guards—皮, 皮膚, 肌—are present; 皮 is the shared observation. Complete families **1474370, 1483800, 1483920, 1476450**, their actual articles, and [American Heritage skin](https://www.ahdictionary.com/word/search.html?q=skin), transitive **1 and 3**, establish the removal/peeling ambiguity. Japanese anatomical nouns remain nouns; POS alone does not eliminate the English-label ambiguity. **Confidence: high.**

- **Claude B82-02 — Withdrawal warranted; removal recommendation not sustained.** Retain the six guards at `words\蒸し暑い.md:9`. Fresh actual titles supply bare **close** on 密, 近い, 親しい, 閉じる, 閉まる, and **sticky** on べたべた. Independently retrieved [close, adjective 14](https://www.ahdictionary.com/word/search.html?q=close), and [sticky, adjective 3](https://www.ahdictionary.com/word/search.html?q=sticky), expressly support humid-weather meanings. Conversely, **close something**, **close up; close applications**, **stick to; keep close to**, and **approach; drawing close** are qualified whole phrases, not bare weather alternatives. This supports neither Japanese weather synonymy nor a closing/proximity clique. **Confidence: high.**

- **Claude B82-03 — Resolved.** Learner-facing cleanup is present in 蒸し暑い, むく, and ミリ. Quiz/source-authoring and irrelevant city commentary are removed while the weather-English explanation/citations, 剥く/剝く recognition, usually-kana flags, both むく senses, and bounded French-source statement remain. No regression established.

- **Claude B82-04 — Resolved.** `words\醜い.md:29–30,37` correctly recognizes rare 見憎い as the same みにくい adjective and links the existing 美しい article. Complete entries **1333810** and **1486360** support the treatment; no unsupported derivation or rare-spelling collocation is introduced.

- **Claude optional むく object-role observation — Resolved as a minor comprehensibility defect.** `words\むく.md:28–30` now separates the peeled thing/removed covering from the teeth exposed or eyes opened wide. The two complete senses and actual constructions support this localized correction.

- **Adopted optional polish — Confirmed without regression.** 実る/無限/無数 lose trivial reading comparisons; 未満/無数 use learner-facing gloss explanations; `words\向かう.md:25` links 向こう only in the new paragraph. Conjugations, strict numerical exclusion, ordinary countless/infinite overlap, and baseline teaching remain intact.

The correction adds **seven direct declarations**, taking the assigned cards’ exclusion declarations from **123 to 130**. No additional excessive pair was established for 身分 or 無地; “broad but harmless” is not a justification for either retaining or removing a guard.

**Remaining actionable findings: none.**

## Optional:

A predicate 見慣れる example or a further 未満/以内 comparison could provide additional practice, but neither is required for scoped correctness. No high-confidence defect requires replacing the 無数 example. These remain nonblocking expansions, not unresolved findings.

## Limits:

The frozen Japanese material provides **nineteen applicable Digital Daijisen bodies through Weblio—one Japanese dictionary authority**. Its failed 向う capture supplies no corroboration; the complete pinned family supports that spelling. Mixed metric/city, medical/general-みる, and むく/すく headings were kept separate.

All five live American Heritage fetches succeeded. They independently support the consequential English-label claims, but are live retrievals rather than frozen hash-authenticated responses.

CLEAN means no actionable defect established within the actual reviewed scope. It does not certify exhaustive correctness, native-speaker naturalness, frequency, historical reconstruction, or runtime quiz behavior. No consequential linguistic uncertainty remains identified here; Git provenance and preservation execution retain the limitation stated above.
