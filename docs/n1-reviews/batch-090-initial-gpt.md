## Snapshot

`e044e953133548dd37fdf1dba449de2f4ee7575f`, identified as the signed snapshot by the supplied packet. Signature, Git state and correspondence to repository files were not independently verified.

Reviewer: **GPT-6.1 Sol (`gpt-6.1-sol`)**, independently reviewing the supplied evidence.

## Scope

Read exactly one resource: `C:\Users\stop-\n1-kanji-workspace\control\batch-090-initial-packet.txt`, using one whole-file `view` call with `forceReadLargeFiles=true`, without `view_range`. The packet identifies itself as **248,434 bytes / 6,161 lines**; the returned text showed no truncation notice. No recovery reads or other resource access occurred.

Reviewed both complete new articles, the four exact changed reused passages, and supplied complete reused articles as context—not rewrite assignments. Inspected all **207 supplied complete dictionary families: 194 lexical and 13 comparison**, their reading/spelling/sense restrictions and flags, all eight complete raw character records, stroke data, public dictionary extractions and provenance, and supplied format/quiz policies. This was packet-based evidence inspection, not independent upstream retrieval.

## Verdicts

**CLEAN** means no established actionable defect within this bounded review, not exhaustive correctness. Text comprehensibility assesses wording suitable for phone reading, not rendered phone behavior.

| Article or changed passage | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| NEW `kanji\刀.md:1–48` | CLEAN | CLEAN | CLEAN |
| NEW `words\日本刀.md:1–38` | CLEAN | CLEAN | CLEAN |
| `words\刀.md:24` — linked component introduction | CLEAN | CLEAN | CLEAN |
| `words\剃刀.md:25` — linked component introduction | CLEAN | CLEAN | CLEAN |
| `kanji\日.md:48` — 日本刀 navigation entry | CLEAN | CLEAN | CLEAN |
| `kanji\本.md:37` — 日本刀 navigation entry | CLEAN | CLEAN | CLEAN |

**Lexical and construction checks.** 日本刀’s noun definition—Japanese sword made in the traditional Japanese manner—is supported by the supplied Daijisen and Seisenban definitions. The museum and photograph sentences, kana, English translations, and explanations of を and の are correct and neutral. 日本 functions as the lexical country name modifying 刀, not a literal “sun + book” derivation. Both にほんとう and にっぽんとう are documented; the article neither ranks their frequency nor invents a general pronunciation-change rule.

The broader category versus a narrowly historical katana subtype is appropriately qualified. JMdict’s “usually single-edged and curved” supports the nonabsolute shape description. The prose does not turn dictionary evidence into technical sword history or a manufacture/handling lesson.

**Reading and character checks.** Raw metadata preserves, in order, on **トウ** and kun **かたな, そり**. Only トウ and かたな are selected; each has its own reading-table row and linked example with defensible actual character allocation: 日本刀 supplies トウ for 刀, and standalone 刀 supplies かたな. Source-only そり remains available for lookup without being labelled nonexistent or archaic. 剃刀’s whole-word かみそり is correctly not divided to manufacture independent readings.

The complete 刀 family restricts scalpel, graver/chisel and knife-money senses to **とう**; none is transferred to かたな. Selective teaching of sword/katana does not require adding those other senses. Grade 2, radical 刀/18 and two strokes match the raw record. The supplied SVG and generated JSON both contain the two corresponding strokes; their coordinates support the inward-starting sweep description. The mnemonic is explicitly modern-shape-based, not historical origin. The 力 crossing contrast is appropriate. Omitted phonetic metadata does not assert that a phonetic component is absent.

**Levels and quiz choices.** N1 is explicitly a community classification, not an official syllabus. 日本刀 receives no invented vocabulary-level metadata. Reused 刀 N3 and 剃刀 N2 identities, readings and exclusions remain unchanged.

All three authored wrong-kanji choices—乃, 凹 and 凸—have supplied N1 cards and distinct displayed labels. Their ordinary and supplied secondary meanings do not furnish a sword/blade answer: connecting/particle uses, hollowness, convexity, forehead and bump are not competing translations. Under the supplied documented default four-choice behavior, these three eligible curated choices fill the wrong-answer positions without fallback. Legacy clients’ disregard of reading curation remains relevant: they can expose source-only そり. This review does not certify their behavior as safe reading instruction.

The direct **日本刀/刀** exclusion addresses genuine semantic overlap. It is not a claim of universal synonymy or a transitive exclusion clique. ナイフ, 包丁 and 剃刀 were checked against their actual families, including 包丁’s archaic cooking sense and 剃刀’s kana preference and figurative senses; none establishes a necessary additional exclusion with 日本刀. Existing 包丁/ナイフ and 剃刀/鋭い exclusions are preserved. 力 and 切 already have three curated wrong cards; no expansion is needed here.

**Reciprocal navigation.** All five required mapped pairs have both directions:

| Pair | Kanji → word | Word → kanji |
|---|---|---|
| 刀 ↔ 刀 | `kanji\刀.md:31,38` | `words\刀.md:24` |
| 刀 ↔ 日本刀 | `kanji\刀.md:30,39` | `words\日本刀.md:24` |
| 刀 ↔ 剃刀 | `kanji\刀.md:34,40` | `words\剃刀.md:25` |
| 日 ↔ 日本刀 | `kanji\日.md:48` | `words\日本刀.md:24` |
| 本 ↔ 日本刀 | `kanji\本.md:37` | `words\日本刀.md:24` |

The exact word IDs and primary readings are consistent. Written-kanji metadata includes `[日, 本, 刀]`, `[刀]` and `[剃, 刀]` respectively. 剃 correctly remains in metadata despite lacking a current card. No incidental-backlink quota was imposed.

## Findings

**Proved defects: none established.**

**Consequential unresolved hypotheses: none within the reviewed textual scope.**

## Optional

None necessary.

## Limits

No independent Git, signature, hash, archive or upstream verification was performed. Public dictionary evidence consists of coordinator-extracted text and supplied provenance; extraction removes formatting, links and images. Encyclopedic history and metallurgy were not independently validated.

No native-font, drawing/rendering, interactive UI or physical-phone evidence was obtained, and no learning effectiveness was measured. Stroke conclusions are textual comparisons of supplied SVG/JSON data, not visual acceptance.

Actual N1/All production choices, wider custom/random pools, larger quizzes and installed-client compatibility remain later gates. Documented fallback and exclusion behavior is not a certification of every runtime choice set. No files were edited.
