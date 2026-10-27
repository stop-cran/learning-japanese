## Snapshot: `8f03c81ff667930c81be8b0990ff6425b3b8c1d9`

**Review target: committed content only**, as identified by the frozen receipt. Parent: `4b9eb80c502524daf4521bb2fa340681d026fab7`.

The receipt’s commit, cleanliness, hashes and rendering-equivalence checks are author-executed assertions. I have file tools but **no Git execution**, so I cannot independently authenticate those assertions.

## Scope

**Reviewer:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Independent, read-only review; no delegation, agents or edits.

I completely read the eighteen new articles, both reused articles, the actual four-file related patch, and both edited kanji articles. I assessed all twenty assigned TSV mappings, applying the required instruction files and `docs\content-format.md:18–126`.

Evidence inspected included the complete supplied principal/comparison renderings—reported as 249 families and 581 senses, including twenty principal families/forty senses and the two separate ダイヤ families—plus twenty mapping records, eighteen component records, 160 captured labels/exclusions and all twenty-five supplied public-body captures. I also read targeted actual comparison articles and checked reverse exclusions in `words\`. This was not an exhaustive reading of the existing corpus or an assertion that I reproduced the author’s particular comparison-body inspection set.

The prohibited authoring rationale, authoring notes and reviewers’ outputs were not consulted. Public extensions were kept separate from pinned sense indices and from unrelated extracted material.

## Verdicts

**Three articles need scoped fixes:** 涼む, スタート and 酸っぱい. No actionable definition, conjugation, translation or source-identity defect was established. All twenty mappings and both narrow kanji edits are CLEAN.

Each verdict triple below is **correctness / scoped coverage / comprehensibility**. Missing quiz safeguards and required comparison links are recorded under scoped coverage; the linguistic explanations themselves remain CLEAN.

| Source row | Article | Status | Article verdicts | Mapping verdicts |
|---|---|---|---|---|
| N2:842 | 隙間 | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:843 | スクール | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:844 | 少なくとも | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:845 | 図形 | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:846 | スケジュール | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:847 | 鈴 | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:848 | 涼む | New | CLEAN / NEEDS FIX / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:849 | スタート | New | CLEAN / NEEDS FIX / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:850 | スチュワーデス | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:851 | すっきり | Reuse | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:852 | 酸っぱい | New | CLEAN / NEEDS FIX / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:853 | ステージ | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:854 | 捨てる | Reuse | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:855 | ストッキング | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:856 | ストップ | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:857 | 素直 | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:858 | 頭脳 | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:859 | スピーカー | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:860 | 図表 | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |
| N2:861 | スマート | New | CLEAN / CLEAN / CLEAN | CLEAN / CLEAN / CLEAN |

Mapping verdicts cover the source spelling/reading, applicable selected meanings, article identity and level preservation—not presumed compiler intent. In particular:

- **N2:851:** the existing refreshed, neat/uncluttered, resolved and clear teaching adequately supports selected senses 1–4 in practical scope. The patch adds only `jlpt: 2`; the identity, title, body, tags and five exclusions are preserved. Captured senses 5–6 are not treated as newly authored or independently assigned N2.
- **N2:854:** 捨てる/すてる remains the N4 primary identity. The added paragraph correctly recognizes rare spelling 棄てる without inventing another pronunciation, conjugation or sense. The blank source gloss remains blank; discarding sense 1 is a supported editorial anchor, not recovered compiler intent.

| Related kanji edit | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 涼 / 涼む at `すず.む` | CLEAN | CLEAN | CLEAN |
| 脳 / 頭脳 at `ノウ` | CLEAN | CLEAN | CLEAN |

`kanji\涼.md:32,43` supplies both required 涼む links; `kanji\脳.md:30,39` supplies both 頭脳 links. The word articles link back to the correct kanji. The patch preserves metadata and the qualifications on source-only readings.

## Findings

**F01 — Moderate; scoped coverage: missing direct 涼む / 冷める quiz exclusion.**

**Location:** `words\涼む.md:4,9,16–21`; comparison `words\冷める.md:4,9,16`.

The existing title **“cool down; lose enthusiasm”** supplies a defensible English answer for 涼む’s literal cooling-off use. This does not make the Japanese verbs freely interchangeable: the article correctly distinguishes enjoying cool conditions from something losing heat. Nevertheless, the unqualified English “cool down” can create a second acceptable meaning-quiz choice. Both cards exclude 冷える, but that two-edge relationship does not exclude them from each other.

**Minimal remedy:** add `冷める` to 涼む’s `quiz_exclusions` once; no reciprocal duplicate declaration is needed.

**Evidence:** frozen JMdict entry 1554380, sense 1, explicitly includes “to cool oneself” and “to cool off”; the actual 冷める title and body teach cooling down. `docs\content-format.md:98–111` establishes symmetric, nontransitive exclusions. The fresh Kotobank 冷める entry also corroborates its thermal-cooling meaning.

**Confidence: high.**

**F02 — Moderate; scoped coverage: スタート’s exclusions miss two ordinary secondary-meaning overlaps.**

**Location:** `words\スタート.md:4,9`; comparisons `words\立ち上がる.md:4,9,16–21` and `words\頭.md:2–9`.

The title **“start; starting point”** can reasonably answer 立ち上がる in its computing use and 頭 in its beginning/start use. The existing 立ち上がる article actually teaches computer start-up, including a translated example. 頭’s article concentrates on anatomy, but that teaching focus does not remove its ordinary secondary meaning from a context-free written-word quiz. Neither comparison has a reverse exclusion protecting the pair.

**Minimal remedy:** add `立ち上がる` and `頭` to スタート’s exclusions. Do not rewrite their meanings or claim unrestricted Japanese substitution.

**Evidence:** complete frozen records in `batch-43-selected-families-10.txt`: JMdict 1551370, sense 5, “to start up; to boot up,” explicitly marked computing; and 1582310, sense 6, “beginning; start,” applicable to あたま without a rare/archaic or sense-specific reading restriction. These are semantic overlaps, not merely shared topics or spelling.

**Confidence: high.**

**F03 — Minor; scoped coverage: substantive comparisons omit links to existing cards.**

**Location:** `words\酸っぱい.md:33–39`; `words\スタート.md:36–37`.

酸っぱい substantively compares 甘い and 苦い, while スタート introduces ゴール as its race contrast, but all three references are plain text despite existing cards. The explanations are understandable; the defect is missing required navigation to the comparison lessons.

**Minimal remedy:** link those introductions as `[甘い](甘い.md)`, `[苦い](苦い.md)` and `[ゴール](ゴール.md)`, preserving the wording.

**Evidence:** I read the actual cards: `words\甘い.md:15–20`, `words\苦い.md:15–17` and `words\ゴール.md:15–20` teach the cited senses. `.github\instructions\content-structure.instructions.md:20–21` requires linking existing cards at substantive introductions or comparisons.

**Confidence: high.**

## Optional

None.

## Limits

**Independent commit/file-hash verification remains UNVERIFIED.** Snapshot attribution and equivalence of the permitted renderings rely on the frozen receipt; file access cannot independently prove Git membership or byte-for-byte equality with that commit.

The supplied public bodies are author captures, not my fresh retrievals. Supplemental web access was incomplete: the Weblio requests did not provide usable lexical bodies, and the Kotobank 立ち上がる lookup failed. Those results were not treated as evidence of absence; F02 rests on the inspected frozen families and actual comparison articles.

The selected dictionary evidence is not the entire dictionary, and the comparison audit is not every possible corpus-wide quiz combination. CLEAN means no actionable defect established within the assigned scope—not exhaustive correctness, official modern JLPT syllabus certification or native-speaker certification.
