## Snapshot: eabe2e942e8e6fa67cc4dd4093c3e6ea14edaf3c; committed content only

The frozen receipt identifies this commit, parent `f8eaca3bef6d3c90b5002e0d3b50b206acc73d5d`, and clean committed content. **I have file tools, not Git execution**; commit identity, cleanliness, and file hashes are receipt-backed rather than independently recomputed.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Reviewed all 19 new articles below completely, sequentially, without delegation or edits; assessed all 20 assigned mappings, N2:42–N2:61, against the supplied dictionary families, restrictions, component records, and spelling extracts.

Read the actual related patch and inspected changed passages in context in `kanji\荒.md`, `改.md`, `著.md`, `争.md`, `有.md`, `難.md`, `易.md`, `外.md`, `言.md`, `付.md`, `意.md`, `生.md`, and `words\戦う.md`. For unchanged `words\ある.md`, reviewed only the 在る/ある source-coverage claim and supporting spelling, reading, meaning, and level passages. Existing comparison cards were inspected for relevant meanings, titles, and exclusions.

Unchanged teaching on related pages was **not comprehensively reviewed**. Prohibited authoring notes, review reports, private inputs, author-check receipts, and other reviewers’ outputs were not consulted.

## Verdicts

**Three minor quiz-metadata findings, covering four missing direct exclusion pairs.** No actionable defect was established in the new articles’ Japanese explanations, scoped source coverage, or comprehensibility.

| New article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `words\荒い.md` | CLEAN | CLEAN | CLEAN |
| `words\粗い.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\あらすじ.md` | CLEAN | CLEAN | CLEAN |
| `words\争う.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\改めて.md` | CLEAN | CLEAN | CLEAN |
| `words\改める.md` | CLEAN | CLEAN | CLEAN |
| `words\著す.md` | CLEAN | CLEAN | CLEAN |
| `words\有難い.md` | CLEAN | CLEAN | CLEAN |
| `words\あれこれ.md` | CLEAN | CLEAN | CLEAN |
| `words\あわただしい.md` | CLEAN | CLEAN | CLEAN |
| `words\あわてる.md` | CLEAN | CLEAN | CLEAN |
| `words\安易.md` | CLEAN | CLEAN | CLEAN |
| `words\案外.md` | CLEAN | CLEAN | CLEAN |
| `words\アンテナ.md` | CLEAN | CLEAN | CLEAN |
| `words\言い出す.md` | CLEAN | CLEAN | CLEAN |
| `words\言い付ける.md` | CLEAN | CLEAN | CLEAN |
| `words\意義.md` | CLEAN | CLEAN | CLEAN |
| `words\生き生き.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\いきなり.md` | CLEAN | CLEAN | CLEAN |

**Related edits:** correctness **CLEAN** / scoped coverage **CLEAN** / comprehensibility **CLEAN**, for the changed passages only. Added word links and examples teach the linked readings; the N2 荒・改・著 cards provide useful reciprocal examples. Written-word kanji metadata and substantive links to existing constituent cards were satisfactory.

**ある reuse claim:** correctness **CLEAN** / scoped coverage **CLEAN** / comprehensibility **CLEAN**. `words\ある.md:24` renders full spellings **有る / 在る**, despite linking only their character portions. Its reading metadata and existence/location teaching (`:3,15–17`) establish the requested 在る/ある use, while `:5` preserves N5. No duplicate alias card is needed.

CLEAN means no actionable defect established within this scope—not exhaustive correctness or native-speaker certification.

## Findings

**B03-GPT-01 — Minor; correctness, quiz answer uniqueness**  
**Location:** `words\粗い.md:4,9`; comparison evidence at `words\かさかさ.md:4,8,15–17`.

The title **“coarse; rough”** remains eligible beside かさかさ, whose title is **“dry and rough; rustling.”** In a question about かさかさ, the unqualified “rough” alternative is defensible for its ordinary rough-texture meaning. Neither card directly excludes the other. Protection through ざらざら does not exclude this pair transitively.

**Minimal remedy:** add `かさかさ` to 粗い’s `quiz_exclusions`, without presenting the Japanese words as unrestricted substitutes.

**Evidence:** frozen JMdict entry **1396910, sense 1**, gives 粗い “coarse; rough”; the independently retrieved [Jisho JMdict-backed かさかさ entry](https://jisho.org/api/v1/search/words?keyword=かさかさ), sense 1, gives “dry and rough; desiccated,” matching the inspected existing card. This is an English-answer-label collision, not a claim that 粗い entails dryness. **Confidence: high.**

**B03-GPT-02 — Minor; correctness, quiz answer uniqueness**  
**Location:** `words\争う.md:4,9`; comparison evidence at `words\議論.md:4,9,16–18,38–39`.

争う’s **“compete; dispute”** label can be a defensible answer for 議論’s ordinary dispute/argument use, but there is no direct exclusion. Both cards’ relationships with 論争 do not protect the 争う/議論 pair. The distinction between neutral discussion and quarreling does not remove 議論’s documented dispute meaning.

**Minimal remedy:** add `議論` to 争う’s `quiz_exclusions`.

**Evidence:** frozen JMdict **1400620, sense 2**, includes “quarrel; argue; dispute.” The independently retrieved [Jisho 議論/ぎろん entry](https://jisho.org/api/v1/search/words?keyword=議論) lists “argument; discussion; dispute; controversy,” with noun/する-verb classification. The inspected cards have unequal titles and no direct guard. **Confidence: high.**

**B03-GPT-03 — Minor; correctness, quiz answer uniqueness**  
**Location:** `words\生き生き.md:4,9`; comparison evidence at `words\もりもり.md:4,8,17,28` and `words\ばりばり.md:4,8,17–20`.

生き生き’s **“lively; vividly; energetically”** label remains eligible as a supposedly wrong answer for **もりもり** and **ばりばり**, both of which have ordinary energetic-activity meanings. Their inspected cards explicitly teach energetic work. Neither pair has a direct exclusion; guards involving 元気, 活気, or ぴんぴん do not extend transitively.

**Minimal remedy:** add both `もりもり` and `ばりばり` to 生き生き’s `quiz_exclusions`.

**Evidence:** frozen JMdict **1609130, sense 1**, includes “actively; energetically.” Independently retrieved Jisho entries give [もりもり, sense 2](https://jisho.org/api/v1/search/words?keyword=もりもり), “energetically; vigorously; (working) hard; enthusiastically,” and [ばりばり, sense 4](https://jisho.org/api/v1/search/words?keyword=ばりばり), “(working) hard; energetically; vigorously; furiously.” These are actual overlapping activity senses, not merely a shared topic. **Confidence: high.**

## Optional

At `words\いきなり.md:33`, link the existing `徐々に` article from the contextual contrast. The current reading and gloss already make the explanation understandable; this is nonblocking navigation polish.

## Limits

No Git commands, hash recomputation, or app execution were available. Quiz findings establish ambiguity from the inspected labels, ordinary meanings, direct declarations, and supplied app behavior; they do not claim a particular generated question was observed.

Official-PDF claims were assessed against the supplied short extracts and author inspection receipt, **not independent reviewer inspection of the PDF bytes**. Live Jisho API evidence was independently retrieved but derives from JMdict, not a separate lexicographic authority; an initial Jisho HTML lookup returned no usable entry text.

One TSV range read incidentally returned the N2:62 mapping; it was not assessed or used. Searches and conclusions otherwise remained within assigned files, `words\`, `kanji\`, and explicitly allowed evidence. No consequential lexical claim remains unresolved within the reviewed practical scope.
