## Snapshot: a01a7787528d7f77f7c415d08747e06d75bb3dde; committed content only

**Result: NEEDS FIX for 散らかる’s quiz exclusions.** Two direct “messy/untidy” overlaps remain unguarded. No other actionable defect was established within the reviewed scope.

Frozen parent: `23d10580d5115175392fe407e21cba9fe94d4fd0`. The snapshot identifies the commit above and asserts clean committed content. **File tools cannot execute Git:** I could not independently authenticate the supplied files against that commit or verify its parent/tree. This report assesses the supplied frozen content, not uncommitted implementation work.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family gpt

Read-only review; no edits, agents, delegation, or Git execution.

**Assigned and related content:** Read all nineteen new articles completely, reused `words\長短.md` completely, all five requested kanji cards completely, and the complete `related.patch`. Read the two required instruction files, `docs\content-format.md:18–126`, both source snapshots, `docs\confusable-words.md`, and `docs\jlpt-levels.md`.

**Mappings and blind evidence:** Read the twenty assigned TSV mappings only; complete compact mappings, principals, components and labels; `principal-reading.txt`; all seven `family-inspection` renderings; the supplemental comparison rendering; and both complete public-body renderings. These cover the supplied **265-family/633-sense union, including the twenty principals/26 senses**—not twenty additional families. The seven original renderings contain 238 families/563 senses; the supplemental rendering supplies thirty records, three duplicates. Counts and author hash/equivalence checks were not independently executed. Only lines 1–120 of `review-evidence.json` were read; the complete compact equivalents and family renderings supplied the substantive evidence.

**Actual old-body inspection:** Read every article in the 109-record label inventory, including assigned 長短, plus 汚い, ぐしゃぐしゃ and 損得: **111 distinct comparison articles beyond the twenty assigned articles**. This is my actual read scope, not adoption of the author’s reported 100 reads. Complete comparison bodies included the adjustment, summit/tip, family, shape, timing, connection, electricity, storage and disorder groups, together with their inventory contrasts.

**External access:** Independently retrieved useful lexical text for [汚い, Digital Daijisen via Weblio](https://www.weblio.jp/content/汚い) and [ぐしゃぐしゃ, Jisho](https://jisho.org/search/ぐしゃぐしゃ). Other attempts returned missing lexical text, a DNS failure, or mixed/truncated material and were not counted as verification. The twenty supplied public captures remain author captures from one dictionary service, not twenty independent dictionaries.

No prohibited ledgers, rationale-bearing batch source, private authoring materials, or other reviewer reports were read.

## Verdicts: twenty source rows and related surfaces

**CLEAN** means no actionable defect established within this scope. Correctness includes quiz behavior; scoped coverage includes required direct exclusion coverage. The 散らかる lesson itself is linguistically sound—the failing cells concern its incomplete quiz protection.

| Source ID | Exact article association | Source-anchor sense(s) | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1062 | `words\長所.md` — new | 1430030:1 | CLEAN | CLEAN | CLEAN |
| N2:1063 | `words\長女.md` — new | 1430040:1 | CLEAN | CLEAN | CLEAN |
| N2:1064 | `words\調整.md` — new | 1429200:1 | CLEAN | CLEAN | CLEAN |
| N2:1065 | `words\調節.md` — new | 1429240:1 | CLEAN | CLEAN | CLEAN |
| N2:1066 | `words\長短.md` — reused; N2/provenance only | 1430070:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1067 | `words\頂点.md` — new | 1430240:2 | CLEAN | CLEAN | CLEAN |
| N2:1068 | `words\長男.md` — new | 1430080:1 | CLEAN | CLEAN | CLEAN |
| N2:1069 | `words\長方形.md` — new | 1430130:1 | CLEAN | CLEAN | CLEAN |
| N2:1070 | `words\調味料.md` — new | 1429290:1 | CLEAN | CLEAN | CLEAN |
| N2:1071 | `words\チョーク.md` — new | 1078240:1 | CLEAN | CLEAN | CLEAN |
| N2:1072 | `words\直後.md` — new | 1430930:1 | CLEAN | CLEAN | CLEAN |
| N2:1073 | `words\直線.md` — new | 1431310:1 | CLEAN | CLEAN | CLEAN |
| N2:1074 | `words\直前.md` — new | 1431330:1 | CLEAN | CLEAN | CLEAN |
| N2:1075 | `words\直通.md` — new | 1431440:1 | CLEAN | CLEAN | CLEAN |
| N2:1076 | `words\直流.md` — new | 1431600:1 | CLEAN | CLEAN | CLEAN |
| N2:1077 | `words\貯蔵.md` — new | 1427220:1 | CLEAN | CLEAN | CLEAN |
| N2:1078 | `words\直角.md` — new | 1430800:1 | CLEAN | CLEAN | CLEAN |
| N2:1079 | `words\直径.md` — new | 1597720:1 | CLEAN | CLEAN | CLEAN |
| N2:1080 | `words\散らかす.md` — new | 1303420:1 | CLEAN | CLEAN | CLEAN |
| N2:1081 | `words\散らかる.md` — new | 1303430:1 | **NEEDS FIX** | **NEEDS FIX** | CLEAN |

**Mappings — CLEAN within the supplied evidence.** All twenty source IDs, raw spellings/readings, dictionary sequences and gloss fields agree with their inspected mapping records and applicable teaching. Actual restrictions, flags, inherited POS and homographs were considered, not just English gloss matches. In particular:

- 長所’s numbered raw gloss remains one combined pinned sense. 長短 covers both length and pros/cons without reproducing `+-` as teaching prose.
- 頂点’s source anchor is sense 2; senses 1, 3 and 4 are additional teaching. 直前’s spatial use and 貯蔵’s hoarding use have separately identified pinned senses.
- チョーク separates principal chalk from entries 2854421’s chock/doorstop and 2854422’s choke uses.
- 直後’s spatial extension is public-backed, without an invented pinned principal sense 2. Other additional identities/uses are not independently assigned N2.
- The supplied patch preserves 長短’s identity, title, original teaching and exclusions. Its previously absent level receives sourced `jlpt: 2`; no easier level is overwritten.

**Kanji and component assessment:**

| Surface | Judgment | Evidence |
|---|---|---|
| 線/直線 addition | CLEAN | `kanji\線.md:30,46`: セン row and Common words both link **直線 ちょくせん**; substantive reciprocal word-side link present. |
| 貯/貯蔵 addition | CLEAN | `kanji\貯.md:28,35`: チョ row and Common words both link **貯蔵 ちょぞう**; reciprocal link present. |
| 蔵/貯蔵 addition | CLEAN | `kanji\蔵.md:30,41`: ゾウ row and Common words both link **貯蔵 ちょぞう**; reciprocal link present. |
| 角/直角 addition | CLEAN | `kanji\角.md:28,36`: カク row and Common words both link **直角 ちょっかく**, including the contraction; reciprocal link present. |
| Unchanged 短/長短 | CLEAN | `kanji\短.md:28,34`: existing タン row and Common words retain **長短 ちょうたん**. |
| Baseline kanji metadata | CLEAN in supplied patch comparison | Four edited cards change examples/provenance, not baseline front matter. No 短 change appears. Independent parent-tree verification remains unavailable. |
| New-word components | CLEAN | Every distinct written Han character is retained in metadata; existing components have substantive word-side links. Missing 整, 節 and 径 remain metadata components without fabricated kanji cards. `words\節.md` is correctly treated as a word article, not a kanji card. |

Quiz judgments used complete titles and ordinary secondary senses. Existing one-sided protection was credited—for example, 損得 already excludes 長短. I did not infer a clique from a comparison cluster, propagate guards transitively, or establish a pair from homophony/category membership alone. No additional actionable excess was established.

## Findings: N2-54-GPT-01

**Medium severity · quiz correctness / scoped exclusion coverage · `words\散らかる.md:4,9,16–24`**

**Claim and impact:** 散らかる lacks direct exclusions against **汚い** and **ぐしゃぐしゃ**, despite ordinary untidiness meanings that make the contextless quiz labels defensibly overlap.

| Endpoint | Complete displayed title | Exact supporting evidence |
|---|---|---|
| 散らかる | `be untidy; lie scattered around` | `words\散らかる.md:16–24` teaches an untidy place and resulting messy state. Its line 9 excludes only 混乱, 荒れる and 混雑. |
| 汚い | `dirty; messy` | `words\汚い.md:4,15,28` explicitly includes untidiness and compares 散らかっている. Its complete header has no exclusion. Independently retrieved Daijisen sense 2 describes disorder/untidiness, distinct from physical dirt. |
| ぐしゃぐしゃ | `crumpled; messy; soggy` | `words\ぐしゃぐしゃ.md:4,17,28` includes disorder and state/change constructions. Independently retrieved Jisho display meaning 3 is “messy; untidy; disorganized.” Line 8 does not exclude 散らかる. |

For Japanese→English, the “messy” alternatives can describe 散らかる’s ordinary untidy-state use. For English→Japanese, 散らかる is likewise a plausible choice for the overlapping untidiness component. The full titles’ additional dirt, crumpling or wetness meanings do not eliminate that overlap.

The titles are not identical, so exact-title deduplication does not protect them. ぐしゃぐしゃ’s existing exclusion against 汚い also does **not** protect either direct pair with 散らかる. Under `docs\content-format.md:79–99`, these gaps can affect both quiz directions and co-occurring distractor choices.

**Minimal remedy:** Add `汚い` and `ぐしゃぐしゃ` to `words\散らかる.md:9`, preserving the existing exclusions. One declaration per pair suffices; no old-body rewrite or title distortion is needed. Do not automatically extend this finding to 散らかす by transitivity: its causative/action title requires its own judgment.

**Confidence:** High for 汚い; high for the ordinary untidiness overlap with ぐしゃぐしゃ. This is a static content finding, not an observed runtime question.

## Optional: none

No expansion is required merely to exhaust dictionary senses. The scoped recognition notes, distinctions and examples are adequate apart from the exclusion gap above.

## Limits: snapshot authentication and bounded lexical review

The commit/tree relationship, working-tree cleanliness, captured-response hashes, rendering equivalence and supplied union counts were **not independently executed checks**. The patch supports the narrow preservation judgments, but cannot substitute for a Git comparison.

The review covers the assigned articles, complete supplied lexical families and the explicitly described comparison reads—not every repository article or the complete dictionaries. Public captures support particular definitions/examples, not measured frequency, unrestricted interchangeability, or native-speaker certification. Live Jisho evidence is current JMdict-derived evidence, not authentication of the pinned snapshot.

No consequential linguistic or mapping question remains unresolved within that bounded scope. The established outstanding issue is **N2-54-GPT-01**.
