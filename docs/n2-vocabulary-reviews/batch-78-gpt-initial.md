## Snapshot: da41f6ef4025d64580008f97051637a74522025b; committed content only

**Four articles need quiz-exclusion fixes: 放る, 朗らか, 干す and ぼろ.** No actionable teaching-prose, source-mapping, component-link or baseline-preservation defect was established within the inspected scope.

Frozen parent: `3f88cca3e759ec8dd348f408f86a2c34d6952b8e`. I read `frozen-snapshot.json` first. File tools cannot execute Git, so the commit association, clean-worktree assertion, hashes and rendering-equivalence checks remain supplied author receipts—not independently executed reviewer checks.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`); family `gpt`

This was a serial, read-only review: no agents, delegation, concurrent work or edits.

Complete reads included:

- All twenty assigned current word articles; all six related current kanji bodies; the complete seven-file `related.patch`; and all six supplied baseline kanji bodies.
- All twenty mappings, twenty complete principal families containing 45 senses, 31 complete component records and 268 complete comparison-label records, using the prescribed bounded JSONL ranges.
- The TSV header and exactly physical lines 1542–1561; both permitted repository snapshot JSON files; the two required instruction files; `docs\content-format.md:18–103`; and `docs\confusable-words.md`.
- All fourteen complete family-inspection chunks and the complete supplementary 採掘 family. Under the supplied receipt’s deduplication, these represent **387 distinct families / 904 senses**, including the principals—not all 546 prepared families / 1,276 senses.
- All 22 older-body renderings: **173 complete articles**, plus the complete current 採掘 article. 止める, 中止, 愉快, 無視, 穴 and 失敗 were additionally checked completely in their current repository files.
- Both complete public-body text captures and their JSON receipts: twenty initial and two supplemental captures.

The public material is **one authority, Digital Daijisen via Weblio**. The initial 坊っちゃん capture concerns the novel and was not used as lexical corroboration. The supplemental 坊ちゃん and ぼっちゃん headings provide applicable lexical evidence, producing 21 positive lexical captures across the 22 captures.

I used the complete compact derivatives rather than reading `review-evidence.json` itself. I did not read the prohibited rationale, ledgers, scripts or other reviewers’ reports. No live external retrieval was performed.

## Verdicts:

Here, **Correctness includes quiz metadata**; Scoped coverage assesses practical source-sense and recognition teaching. Thus the four quiz findings do not reject those articles’ prose or selected teaching coverage. Sense references below are the mapping’s selected **one-based JMdict senses**, not public-dictionary numbering.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1542 | 防犯 | CLEAN | CLEAN | CLEAN | 1520570:1–2. Crime prevention and security-device prefix; no blanket suru claim. |
| N2:1543 | 方面 | CLEAN | CLEAN | CLEAN | 1517100:1–2. Direction/area and abstract field; destination distinction is clear. |
| N2:1544 | 坊や | CLEAN | CLEAN | CLEAN | 1519060:1–2. Familiar boy/son and greenhorn recognition; formation explained. |
| N2:1545 | 放る | NEEDS FIX | CLEAN | CLEAN | 1516530:1–2. Transitivity and conjugation sound; missing direct guards: B78-GPT-01. |
| N2:1546 | ボーナス | CLEAN | CLEAN | CLEAN | 1123520:1. Employment payment and other extras; no entitlement or schedule invented. |
| N2:1547 | 朗らか | NEEDS FIX | CLEAN | CLEAN | 1560710:1–2. な/に attachment and clear-sky limitation sound; B78-GPT-02. |
| N2:1548 | 牧場 | CLEAN | CLEAN | CLEAN | 1584250:1–2. Both ぼくじょう and まきば; place/activity/animal distinctions preserved. |
| N2:1549 | 牧畜 | CLEAN | CLEAN | CLEAN | 1521820:1. Livestock farming, not cattle alone or generic pet care. |
| N2:1550 | 保健 | CLEAN | CLEAN | CLEAN | 1513410:1–2. Preservation/hygiene and school subject; health state and insurance distinguished. |
| N2:1551 | 募集 | CLEAN | CLEAN | CLEAN | 1514830:1–3. Recruitment retained; solicitation/subscription recognition added appropriately. |
| N2:1552 | 干す | NEEDS FIX | CLEAN | CLEAN | 1603510:1–4. Household teaching preserved; additional uses distinguished; B78-GPT-03. |
| N2:1553 | ポスター | CLEAN | CLEAN | CLEAN | 1125110:1. Displayed item and practical constructions; ポスタ recognized. |
| N2:1554 | 北極 | CLEAN | CLEAN | CLEAN | 1520890:1–2. Pole versus Arctic region and small っ explained. |
| N2:1555 | 坊っちゃん | CLEAN | CLEAN | CLEAN | 1603720:1–2. Another’s son/young master versus sheltered young man; lexical heading verified. |
| N2:1556 | ほどく | CLEAN | CLEAN | CLEAN | 1198900:1. Separate from とく1198890; transitive forms and ほどける contrast sound. |
| N2:1557 | 濠 | CLEAN | CLEAN | CLEAN | 1522060:1–2. Source 堀 explicitly recognized; stable article and earlier N3 retained. |
| N2:1558 | 掘る | CLEAN | CLEAN | CLEAN | 1246690:1–3. Digging, extraction and delving; vulgar sense 4 need not be expanded. |
| N2:1559 | 彫る | CLEAN | CLEAN | CLEAN | 1427950:1–2. Object/surface marking and tattoo recognition; reading restrictions respected. |
| N2:1560 | ぼろ | NEEDS FIX | CLEAN | CLEAN | 1572500:1–4. Rag, concealed flaw and shabby condition distinguished; B78-GPT-04. |
| N2:1561 | 盆 | CLEAN | CLEAN | CLEAN | 1523700:1–4. Tray/Obon focus; household and gambling-den recognition kept separate. |

**Mappings—all twenty CLEAN.** Each assigned source identity, reading and applicable meaning is explicitly represented. In particular:

- Raw **堀／ほり／1522060** legitimately maps to existing **濠**, whose article recognizes 堀. No duplicate card or N3-to-N2 replacement is required.
- **ほどく1198900** remains separate from **解く／とく1198890** despite shared possible spelling.
- Raw English glosses remain source evidence, not grammatical instructions: 放る’s “let go” does not establish unrestricted substitution with 放す, and 盆’s “Lantern Festival” does not require teaching the Chinese festival.
- Recognition coverage does not independently certify every recognized sense as N2.

**Six related kanji—all three facets CLEAN within scope.**

| Kanji | Precise change and preservation judgment |
|---|---|
| 防 | Adds 防犯 to reading/common-word teaching and its source reference. Metadata and unrelated teaching preserved. |
| 畜 | Adds 牧畜 to reading/common-word teaching and its source reference. Metadata and unrelated teaching preserved. |
| 極 | Adds 北極, its contracted pronunciation guidance, common-word link and source reference. Metadata and unrelated teaching preserved. |
| 掘 | Existing 掘る mentions become links across the relevant sections. No unrelated semantic or metadata change established. |
| 募 | Unchanged against the supplied baseline; existing 募集 reciprocity retained. |
| 干 | Unchanged against the supplied baseline; existing 干す reciprocity retained. |

**Three reused-word baselines—preservation CLEAN.** 募集 and 干す preserve their stable identities, titles and earlier recruitment/household teaching while gaining explicit N2 levels and recognition/exclusion additions. 濠 preserves its filename, primary spelling, identity, title, earlier teaching and N3 level while adding the canal comparison and direct 運河 exclusion.

**Components and reciprocal links—CLEAN.** All 21 distinct primary written Han are represented in metadata. The thirteen existing primary component cards—北, 場, 募, 極, 方, 放, 掘, 干, 防, 畜, 犯, 集, 面—have substantive word-side links. The eight absent cards—坊, 朗, 牧, 保, 健, 濠, 彫, 盆—were not invented. Actual whole-word readings, contractions and spelling restrictions are respected.

All four new reciprocal pairs are present: **防犯/防, 牧畜/畜, 北極/極, 掘る/掘**. Existing **募集/募** and **干す/干** were rechecked.

**Existing exclusions:** no actionable removal was established. Ordinary secondary senses matter: 開く includes transitive ひらく “undo/unpack,” and 採掘 was checked through both its complete family and actual article. Homophony alone does not require a 掘る/彫る guard. Existing neighboring exclusions were not treated as transitive protection.

## Findings:

Private artifact citations below use the supplied exact `batch-78-` prefix.

**B78-GPT-01 — Medium; Correctness—quiz exclusions**

**Location:** `words\放る.md:9`; supporting teaching at `:16–21`.

The guard list omits **止める** and **中止**, although both have direct ordinary overlap with abandoning/discontinuing work. The actual titles are “stop something; discontinue” and “cancellation; discontinuation.” Neither comparison article supplies an incoming guard.

**Impact:** 放る can face a defensible discontinuation answer; conversely, 止める’s やめる use can admit “abandon.” This is activity-cessation overlap, not merely shared topic or an inferred noun/verb exemption.

**Minimal remedy:** add `止める` and `中止` to 放る’s exclusions. One declaration per pair is sufficient.

**Exact evidence:** `words\止める.md:4,15–20` explicitly teaches discontinuing an activity and abandoning a plan; `words\中止.md:4,15–20` includes stopping work already underway. Applicable Daijisen ほうる says `途中でやめる` and `あきらめて放棄する` in `batch-78-public-bodies.txt:79–81`. Complete JMdict families 1310680 and 1424410 corroborate these ordinary senses. The existing 止す guard does not protect either pair. **Confidence: high.**

**B78-GPT-02 — Medium; Correctness—quiz exclusions**

**Location:** `words\朗らか.md:9`; supporting teaching at `:16–21`.

The direct **朗らか/愉快** pair is unguarded. This is not inferred through 明るい, 陽気 or 楽しい: 愉快 itself has an ordinary cheerful-character sense.

**Impact:** In particular, a 愉快-to-English question can plausibly admit 朗らか’s full answer label, “cheerful; bright and clear,” through its cheerful alternative. The additional weather meaning does not eliminate that collision.

**Minimal remedy:** add `愉快` to 朗らか’s exclusions.

**Exact evidence:** `words\愉快.md:4,9,16–21` supplies its actual title, existing guards and explicit cheerful-character teaching. Complete JMdict 1538560:1 includes “cheerful”; 1560710:1 supplies 朗らか’s cheerful/merry sense. Applicable Daijisen confirms the disposition sense at `batch-78-public-bodies.txt:135`. **Confidence: high.**

**B78-GPT-03 — Medium; Correctness—quiz exclusions**

**Location:** `words\干す.md:9`; recognition discussion at `:43–48`.

The direct **干す/無視** pair is unguarded. Beyond household drying, applicable modern dictionary evidence explicitly includes deliberate ignoring—not merely the indirect proposition that depriving someone of work might involve disregard.

**Impact:** A 干す-to-English question can plausibly admit 無視’s “ignoring; disregarding” label through that ordinary secondary use. The household title may remain unchanged.

**Minimal remedy:** add `無視` to 干す’s exclusions; no separate N2 claim for the ignoring sense is needed.

**Exact evidence:** applicable Daijisen ほす states `故意に仕事や役割を与えないでほうっておく。また、無視する` at `batch-78-public-bodies.txt:209`. `words\無視.md:4,15–20` confirms the actual label and ordinary transitive ignoring sense; its complete header contains no incoming guard. This public sense numbering is not being equated with pinned JMdict index 4. **Confidence: high.**

**B78-GPT-04 — Medium; Correctness—quiz exclusions**

**Location:** `words\ぼろ.md:9`; concealed-fault teaching at `:16–22,32`.

Two direct pairs remain unguarded: **ぼろ/穴** and **ぼろ/失敗**.

**Impact:** 穴’s ordinary figurative flaw/weakness sense can admit the “hidden flaw” answer alternative. Conversely, the applicable ぼろ dictionary heading explicitly includes 失敗, allowing 失敗’s “failure; mistake” label to compete for ぼろ. Physical-hole and unsuccessful-attempt primary examples do not erase these overlaps.

**Minimal remedy:** add `穴` and `失敗` to ぼろ’s exclusions. This does not justify automatically importing an entire flaw/error exclusion clique.

**Exact evidence:** `words\穴.md:4,30,35–37` teaches the figurative flaw in a plan; complete JMdict 1254480:6 includes flaw/fault/defect/weak point. `words\失敗.md:4,15–19` gives its actual title and mistake/blunder meaning. Applicable Daijisen ぼろ states `隠していた都合の悪い点。また、失敗` at `batch-78-public-bodies.txt:390`. Neither comparison header declares the pair. **Confidence: high.**

## Optional:

None required. Missing component cards, exhaustive slang expansion and separate N2 assignments for every recognition sense are not defects in this batch.

## Limits:

This is a content review against the supplied freeze, **not an independent Git provenance or hash-equivalence attestation**. Repository reads cannot independently prove that the working files equal the recorded commit; the supplied receipt and patch provide that association.

I did not inspect the remaining prepared families outside the stated 387-family union or perform an exhaustive all-pairs ambiguity enumeration. Complete label availability was not counted as full-body inspection. The findings concern established direct pairs; they do not assert that every possible exclusion is closed.

Public corroboration comes from one dictionary authority, and an applicable heading does not verify every usage claim. No independent corpus-frequency study, audio assessment or native-speaker certification was performed. **CLEAN means no actionable defect established within the actual scope, not exhaustive correctness.**
