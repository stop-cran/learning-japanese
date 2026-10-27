## Snapshot: 1c55dc75c503046de66d6cf41e73bbe25c96fc62

**Two minor quiz-exclusion gaps need correction.** No actionable defect was established in the twenty source mappings or four narrow kanji edits.

Committed content only, as identified by the frozen receipt; parent: `42283503b9da8e70ae1f17628d1da121c3b93240`. **I have file tools, not Git execution:** I could not independently verify the commit, worktree cleanliness, or hashes. Those assurances remain receipt-backed author assertions.

## Scope

Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family **GPT**. Independent, read-only review; no delegation, agents, edits, or other reviewers’ output.

I read all seventeen new articles completely; all three reuse bodies, with verdicts restricted to their assigned scopes; the actual six-file related patch; all four affected kanji cards in context; and mappings **N2:822–N2:841**. I also read the required repository instructions, `docs\content-format.md:18–126`, permitted provenance records, JLPT guidance, and relevant confusable-word material.

Evidence inspected included the complete principal rendering, all ten selected-family renderings, supplemental 線/本 families, twenty mapping records, twenty-nine component records, 104 existing labels/exclusions, and all thirty-one captured public lexical bodies. I directly read **57 additional comparison word articles** and existing `kanji\滴.md`. This is my actual reading scope, not adoption of the author’s sixty-article inspection claim. Fresh dictionary checks supplemented consequential quiz comparisons.

The prohibited authoring notes, rationale-bearing batch JSON, private author-check files, and reviewer outputs were not read.

## Verdicts

Triples below are **correctness / scoped coverage / comprehensibility**. Article verdicts include quiz metadata. Mapping verdicts separately assess source identity, reading, selected meaning, and recognition coverage.

| Source row | Article and status | Article verdicts | Mapping verdicts |
|---|---|---|---|
| N2:822 | 水蒸気 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:823 | 水素 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:824 | 垂直 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:825 | 推定 — new | **NEEDS FIX** / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:826 | 水滴 — reuse; level addition only | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:827 | 水筒 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:828 | 随筆 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:829 | 水分 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:830 | 水平 — new | **NEEDS FIX** / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:831 | 水平線 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:832 | 水曜 → 水曜日 — unchanged N5 reuse | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:833 | ずうずうしい — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:834 | ずうっと → ずっと — bounded N3 reuse | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:835 | 末っ子 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:836 | スカーフ — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:837 | 図鑑 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:838 | 杉 — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:839 | 好き嫌い — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:840 | 好き好き — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:841 | 透き通る — new | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |

**Reuse and mapping qualifications:** 水滴’s existing droplet teaching covers its selected source sense; the pre-existing inkstone-vessel expansion was not treated as newly authored content. 水曜日 explicitly recognizes 水曜/すいよう at `words\水曜日.md:27`; source entry **1372180:1** and teaching entry **1372190:1** are distinct valid identities, not an ID correction, and N5 remains intact.

ずっと retains N3 and its existing continuity, degree, and distance teaching. The added paragraph at `words\ずっと.md:27` correctly recognizes search-only ずうっと without promoting it to the ordinary spelling. The blank source gloss does not establish compiler intent; the editorial selection of senses 1–3 does not require newly teaching captured sense 4.

水平 appropriately qualifies the raw “water level, horizon” gloss rather than teaching it literally. 水平線’s geometric use is separately attributed to Digital Daijisen, not presented as a nonexistent second JMdict sense. Other important distinctions—including 垂直’s two selected meanings, 図鑑 versus illustrated storybooks, 杉’s spelling qualifications, and 透き通る’s godan/intransitive behavior—are adequately taught.

| Kanji edit | Actual reading-row link / Common words link | Correctness / coverage / comprehensibility |
|---|---|---|
| 蒸 → 水蒸気 | ジョウ, `kanji\蒸.md:30` / `:40` | CLEAN / CLEAN / CLEAN |
| 筒 → 水筒 | トウ, `kanji\筒.md:30` / `:36` | CLEAN / CLEAN / CLEAN |
| 筆 → 随筆 | ヒツ, `kanji\筆.md:30` / `:39` | CLEAN / CLEAN / CLEAN |
| 線 → 水平線 | セン, `kanji\線.md:30` / `:41` | CLEAN / CLEAN / CLEAN |

The patch preserves existing metadata and qualifications, including 線’s source-only すじ qualification. Missing component cards remain represented in word metadata without invented files or readings.

## Findings

**GPT42-01 — Minor; correctness: incomplete quiz exclusions for 推定.**

**Location:** `words\推定.md:4,9`; comparison headers at `words\計算.md:2–9` and `words\予定.md:2–9`.

The new answer label **“estimation; inference”** remains eligible against **計算** and **予定**. This is more than a shared thinking/planning topic: 計算 has an ordinary estimation sense, explicitly acknowledged in its existing article at `words\計算.md:17,38–40`; 予定’s dictionary record also includes “estimate.” Consequently, the new label can be a defensible alternative when either existing word is tested, even though their primary titles are “calculation; computation” and “plans; schedule.”

**Minimal remedy:** add `計算` and `予定` to 推定’s direct `quiz_exclusions`. One-sided declarations suffice; do not claim the Japanese words are freely interchangeable.

**Evidence:** complete JMdict-backed [計算 record](https://jisho.org/api/v1/search/words?keyword=%E8%A8%88%E7%AE%97), lexical sense 2, includes “estimation”; complete [予定 record](https://jisho.org/api/v1/search/words?keyword=%E4%BA%88%E5%AE%9A), lexical sense 1, includes “estimate,” without a rare/archaic restriction. Their article identities are 1252140 and 1543240 respectively. Neither side declares these pairs. `docs\content-format.md:80–97` establishes exact-title-only deduplication and symmetric, pairwise exclusions. **Confidence: high.**

**GPT42-02 — Minor; correctness: 水平’s broad “level” label remains ambiguous with 線.**

**Location:** `words\水平.md:4,9`; `words\線.md:2–9`; related but insufficient guards at `words\水平線.md:9`.

水平’s title is **“horizontal; level,”** but its exclusions omit 線. The complete 線/せん family has an unqualified noun/suffix sense **“level.”** Thus 水平’s displayed alternative gloss can be defended when 線 is tested. The existing 水平線→水平 and 水平線→線 exclusions do **not** exclude 水平/線 from each other.

**Minimal remedy:** add a direct 水平/線 exclusion, or qualify the title’s second gloss as **“physically level.”** No new abstract-level teaching belongs in 水平; this is English-label ambiguity, not evidence that 線 means horizontal.

**Evidence:** `batch-42-extra-comparison-reading.txt:17–28`, entry **1391780**, especially sense 6 at line 25; the complete record has no rare/archaic qualification for that sense. Fresh [精選版 日本国語大辞典, 線](https://kotobank.jp/word/%E7%B7%9A-5252), sense ⑤, corroborates the abstract 水準 meaning. The actual headers contain no direct pair declaration. **Confidence: high for the lexical sense and missing pair; medium-high for the resulting label ambiguity.**

Category, component, and topic relationships alone were not used to demand additional exclusions. I considered the existing conservative broad-label guards and did not establish a consequential over-exclusion defect.

## Optional

None.

## Limits

Snapshot authenticity and derivation hashes were not independently Git/hash-checked. The thirty-one supplied public bodies are **author captures**, not my fresh retrievals; packet counts and inspection receipts likewise remain author accounting.

The fresh Jisho records used above are live corroboration, not independently authenticated copies of the pinned JMdict snapshot. Only their relevant lexical records were used—not appended Wikipedia material. Initial irrelevant Weblio extractions were not treated as verification.

No app execution or randomly generated quiz was reproduced. The findings concern pairs permitted by the documented selection rules. Comparison searches and dictionary evidence were substantial but not exhaustive; `docs\confusable-words.md` was consulted partially, not read in full. No additional consequential linguistic claim remains unresolved within the assigned scope. **CLEAN means no actionable defect established here, not exhaustive correctness or native-speaker certification.**
