## Snapshot: `6aa54a72f1f89170d85ef3f0b42af79427018d66`; committed content only

Parent: `42844d9e2a16229696ccf6ec3d1ebde2c65c66a1`.

This review uses the frozen receipt’s identification of the supplied files as clean, committed content. **I have file/web tools, not Git execution**, so I could not independently establish commit membership, worktree cleanliness, or receipt hashes.

## Scope

Actual model: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`.

Reviewed all nineteen new articles completely; all twenty mappings N2:222–N2:241 and their selected senses; the complete eighteen-file related patch and changed passages in context; and 貝’s two-sense reuse and level-only change. Read the required instructions and format documentation, complete principal dictionary families, relevant comparison families, and component evidence. Independently inspected the six cited usage pages rather than treating author inspection receipts as independent evidence.

Existing articles were examined only as needed for changed passages, comparisons, links, and quiz candidates—not comprehensively recertified. No files were edited, and no agents were used.

## Verdicts

**Five new cards need quiz-exclusion corrections. No actionable lesson-body or source-mapping defect was established.** Correctness below includes quiz metadata; scoped coverage and comprehensibility assess the practical teaching supplied, not exhaustive dictionary coverage.

Sense numbers are the supplied one-based JMdict indices.

| New article | Source row | Selected senses | Correctness | Scoped coverage | Comprehensibility |
|---|---|---:|---|---|---|
| 温室 | N2:222 | 1 | CLEAN | CLEAN | CLEAN |
| 温泉 | N2:223 | 1–2 | NEEDS FIX | CLEAN | CLEAN |
| 温帯 | N2:224 | 1 | CLEAN | CLEAN | CLEAN |
| 御中 | N2:225 | 1 | CLEAN | CLEAN | CLEAN |
| 女の人 | N2:226 | 1 | CLEAN | CLEAN | CLEAN |
| 蚊 | N2:227 | 1 | CLEAN | CLEAN | CLEAN |
| カーブ | N2:228 | 1–2 | CLEAN | CLEAN | CLEAN |
| 開会 | N2:230 | 1 | NEEDS FIX | CLEAN | CLEAN |
| 会館 | N2:231 | 1 | CLEAN | CLEAN | CLEAN |
| 改札 | N2:232 | 1–2 | CLEAN | CLEAN | CLEAN |
| 解散 | N2:233 | 1–3 | NEEDS FIX | CLEAN | CLEAN |
| 海水浴 | N2:234 | 1 | CLEAN | CLEAN | CLEAN |
| 回数 | N2:235 | 1 | CLEAN | CLEAN | CLEAN |
| 回数券 | N2:236 | 1 | CLEAN | CLEAN | CLEAN |
| 改正 | N2:237 | 1 | CLEAN | CLEAN | CLEAN |
| 快晴 | N2:238 | 1 | CLEAN | CLEAN | CLEAN |
| 解説 | N2:239 | 1 | NEEDS FIX | CLEAN | CLEAN |
| 改造 | N2:240 | 1–2 | CLEAN | CLEAN | CLEAN |
| 開通 | N2:241 | 1–2 | NEEDS FIX | CLEAN | CLEAN |

**Eighteen related changes:** correctness / scoped coverage / comprehensibility are **CLEAN / CLEAN / CLEAN for each changed surface**:

- Nine kanji cards—温, 泉, 帯, 改, 札, 浴, 券, 快, 造—supply the thirteen reciprocal word pairs at the applicable readings.
- Eight existing word cards—女, 女性, 男の人, 説明, 熱帯, 泉, 会場, 虫—gain appropriate links at their existing comparisons.
- 貝 gains only `jlpt: 2` in the supplied patch. Its stable identity, reading, title, other metadata, and body remain unchanged.

**貝 reuse:** **CLEAN / CLEAN / CLEAN** for the assigned claim. N2:229’s かい and selected senses 1–2 are explicitly taught: molluscan shellfish and a collected seashell, with separate examples. This is not certification of its unchanged secondary-entry discussion or exclusions.

**Twenty mappings:** **CLEAN / CLEAN / CLEAN for the mapping claims.** Every assigned spelling, reading, and selected meaning is explicitly taught in its mapped article. Easier existing levels and stable identities are preserved in the supplied changes. The N2 attribution is to the pinned community list—not an official modern JLPT syllabus, nor an independent N2 assignment to every secondary meaning.

## Findings

The following are localized **quiz-integrity defects**, not claims that the Japanese words are interchangeable. Under `docs\content-format.md:79–99`, semantic overlap is not deduplicated, and exclusions are symmetric but pairwise and non-transitive.

**B12-GPT-01 — Medium; correctness: English-label ambiguity**  
**Location:** `words\温泉.md:4,9`; comparison evidence at `words\春.md:4` and `words\泉.md:4,9`.

温泉’s title is “hot spring; hot-spring spa,” while 春’s displayed title is the unqualified “spring.” In a Japanese-to-English question for 温泉, that bare “spring” is a defensible water-source interpretation even though its underlying card teaches the season. 温泉 excludes 泉, and 泉 excludes 春, but that chain does **not** exclude 温泉/春.

**Minimal remedy:** add a direct 温泉/春 exclusion.  
**Precise evidence:** JMdict 1183450, sense 1, supplies the hot-spring meaning; the existing 泉 title demonstrates the repository’s water-source use of English “spring.” The ambiguity is in the displayed English, not a Japanese synonym claim.  
**Confidence:** high.

**B12-GPT-02 — Medium; correctness: missing direct beginning-label exclusions**  
**Location:** `words\開会.md:4,9`; `words\開通.md:4,9`; comparison evidence at `words\最初.md:4,15–20` and `words\始まり.md:9`.

Both opening cards exclude several start/beginning cards but omit 最初, whose title is “beginning; first.” The opening or commencement of a meeting, and the beginning of route/service operation, can reasonably be identified as a “beginning” in a context-free meaning question. 最初’s exclusion through 始まり does not protect either new card.

**Minimal remedy:** add direct 開会/最初 and 開通/最初 exclusions.  
**Precise evidence:** principal entries 1202560, sense 1, and 1202850, sense 1, establish commencement/opening-for-operation. The actual さいしょ section of [精選版 日本国語大辞典 on Kotobank](https://kotobank.jp/word/%E6%9C%80%E5%88%9D-507748) defines 最初 as the very beginning of something. This concerns the broad English answer label, not substitution of 最初 into a する construction.  
**Confidence:** medium.

**B12-GPT-03 — Medium; correctness: English “dissolve” ambiguity**  
**Location:** `words\解散.md:4,9,16`; comparison evidence at `words\溶ける.md:4,8,15–22`.

解散 teaches dispersal, disbandment, and legislative dissolution, but it can appear beside 溶ける’s “melt; dissolve” label. English “dissolve” ordinarily describes both a substance dissolving and a parliament or gathering breaking up. Consequently, the latter title contains a defensible translation of 解散 even though 溶ける does not teach that organizational meaning. Neither card excludes the other.

**Minimal remedy:** add a direct 解散/溶ける exclusion; retain the Japanese teaching distinction.  
**Precise evidence:** principal entry 1199000, senses 1–3; 溶ける’s physical-change examples; and the independently inspected [Oxford “dissolve” entry](https://www.oxfordlearnersdictionaries.com/definition/english/dissolve), especially sense 1 for solids, sense 3 for ending a parliament, and sense 4’s crowd-dispersal example.  
**Confidence:** high.

**B12-GPT-04 — Medium; correctness: overlapping explanatory-text labels**  
**Location:** `words\解説.md:4,9,16–21`; comparison evidence at `words\注.md:4,15–20`.

解説 excludes 説明 but not 注, titled “annotation; explanatory note.” An explanatory note on a text is itself an explanation/commentary, so 注 can be a defensible Japanese choice for 解説’s broad English label. Conversely, a written 解説 can reasonably be described as an explanatory note. The distinction in textual role does not make these broad labels reliably opposing answers.

**Minimal remedy:** add a direct 解説/注 exclusion without flattening their teaching distinction.  
**Precise evidence:** principal entry 1199080, sense 1; the two articles’ explicit written-explanation uses; and the actual ちゅう entry in [Digital Daijisen on Kotobank](https://kotobank.jp/word/%E6%B3%A8-567071), defining explanatory or supplementary wording attached to a main text. This is meaning overlap, not merely a shared academic topic.  
**Confidence:** medium.

## Optional

None.

## Limits

Snapshot identity and committed-only status remain **receipt-based**, not independently Git-verified. I did not re-download and recompute the pinned CSV, JMdict, or KANJIDIC2 archive hashes, or independently reconstruct the supplied dictionary extraction.

Quiz findings are static assessments against the documented candidate/exclusion contract; the app was not executed. Relevant comparison records and existing cards were inspected, but not every possible repository candidate or all 133 comparison families in full.

Some Jisho responses lacked the requested headword, and Cambridge/Merriam-Webster requests failed; those results were not used as evidence. Successful dictionary and established usage-page inspections support the claims identified above. CLEAN does not imply exhaustive correctness or native-speaker certification.
