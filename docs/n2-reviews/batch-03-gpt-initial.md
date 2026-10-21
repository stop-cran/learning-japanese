## Snapshot: 408be09e0156fc6ed3c0ed1b1b0ac67f592eb1a9; committed files only

The files were treated as the supplied frozen snapshot. **Git execution was unavailable**, so I could not independently verify the commit, worktree cleanliness, or diff against baseline `2cf65f405c9a4ef162c11240a62ad6af30a40de6`.

## Scope

**Reviewer:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Independent, sequential, read-only review; no delegation or edits.

Read all 18 pages below completely, assessing correctness, scoped coverage, and comprehensibility separately. Read the three required instruction/format passages; compared all 15 kanji metadata records and reading examples with the supplied snapshot and restriction-aware evidence packet. Inspected the 42 distinct distractor cards’ actual titles, legacy two-choice fallback metadata, relevant supporting cards, and vocabulary title overlaps/direct exclusions.

Reviewed the new-character links at their substantive introduction in **“How the kanji combine”** in these 20 existing articles:

`words\券.md`, `words\刺激.md`, `words\規則.md`, `words\劇.md`, `words\劇場.md`, `words\悲劇.md`, `words\効く.md`, `words\効果.md`, `words\有効.md`, `words\勇気.md`, `words\勢い.md`, `words\大勢.md`, `words\包み.md`, `words\包む.md`, `words\小包.md`, `words\区別.md`, `words\地区.md`, `words\卒業.md`, `words\協力.md`, `words\占める.md`.

**Not reviewed:** the remaining teaching content of those 20 legacy articles, unrelated legacy defects, excluded review reports or authoring/adjudication material, nanori, old four-level JLPT assignments, or stroke drawing paths.

## Verdicts

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\券.md` | CLEAN | CLEAN | CLEAN |
| `kanji\刺.md` | CLEAN | CLEAN | CLEAN |
| `kanji\則.md` | CLEAN | CLEAN | CLEAN |
| `kanji\副.md` | CLEAN | CLEAN | CLEAN |
| `kanji\劇.md` | CLEAN | CLEAN | CLEAN |
| `kanji\効.md` | CLEAN | CLEAN | CLEAN |
| `kanji\勇.md` | CLEAN | CLEAN | CLEAN |
| `kanji\募.md` | CLEAN | CLEAN | CLEAN |
| `kanji\勢.md` | CLEAN | CLEAN | CLEAN |
| `kanji\包.md` | CLEAN | CLEAN | CLEAN |
| `kanji\匹.md` | CLEAN | NEEDS FIX | CLEAN |
| `kanji\区.md` | CLEAN | CLEAN | CLEAN |
| `kanji\卒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\協.md` | CLEAN | CLEAN | CLEAN |
| `kanji\占.md` | CLEAN | CLEAN | CLEAN |
| `words\副作用.md` | CLEAN | CLEAN | CLEAN |
| `words\募集.md` | CLEAN | CLEAN | CLEAN |
| `words\匹敵.md` | NEEDS FIX | CLEAN | CLEAN |

All 15 kanji metadata sets match the supplied records for readings, primary stroke counts, canonical radicals/numbers, and grade tags. Every new kanji has a useful linked word article and three existing, plausible, semantically wrong curated choices. No additional batch-caused ambiguity was established in the inspected legacy two-choice fallback cases. The 20 scoped link passages point to the corresponding new cards correctly.

## Findings

### R01 — Moderate; correctness: word-quiz answer ambiguity

**Location:** `words\匹敵.md:4,8`; supporting metadata in `words\同様.md:4,9` and `words\同一.md:4,9`.

The new title **“be a match for; equal”** can compete with the existing cards 同様, **“same; similar,”** and 同一, **“identical; one and the same.”** Neither pair has a direct exclusion. When either existing word is the question, the new option’s **“equal”** is itself a documented translation, creating two defensible English answers.

The existing exclusion of 匹敵/同じ does not protect these pairs through 同じ’s relationships with the other cards.

**Minimal remedy:** add `同様` and `同一` directly to 匹敵’s `quiz_exclusions`. No teaching-text rewrite is necessary.

**Exact evidence:**
- `docs\n2-batch-sources\batch-03.json:3160–3201`, JMdict entry **1487250**, supports 匹敵／ひってき as “to be a match for,” “to equal,” and “to be equivalent to.”
- The inspected [Jisho/JMdict record for 同様／どうよう](https://jisho.org/api/v1/search/words?keyword=%E5%90%8C%E6%A7%98), sense 1, includes “same,” “similar,” and **“equal,”** without spelling/reading restrictions.
- The inspected [Jisho/JMdict record for 同一／どういつ](https://jisho.org/api/v1/search/words?keyword=%E5%90%8C%E4%B8%80), sense 1, includes “identical,” “same,” “one and the same,” and **“equal,”** without spelling/reading restrictions.
- `docs\content-format.md:87–88,95–96` specifies pairwise, non-transitive exclusions for defensible overlapping answer labels.

**Confidence:** High.

### R02 — Minor; scoped coverage: no usable animal-count example

**Location:** `kanji\匹.md:31,36,40`.

The card teaches the bound counter reading **ひき**, but its only example is the isolated counter itself. It then warns that number combinations change pronunciation without showing any correctly formed count. Consequently, the card’s primary “small-animal counter” meaning lacks a usable example; the linked 匹敵 article explicitly teaches the other word family.

**Minimal remedy:** use **二匹 にひき — two small animals** in the reading row, and make the existing warning concrete with **一匹 いっぴき** and **三匹 さんびき**. An exhaustive counter chart is unnecessary.

**Exact evidence:**
- `docs\n2-batch-sources\batch-03.json:3203–3270`, JMdict entry **1583370**, identifies the relevant ひき sense as a **counter for small animals**.
- `.github\instructions\content-structure.instructions.md:43–44` calls for an example compound when explaining a bound reading.
- Tofugu’s [“Pronunciation of Japanese Counter 匹”](https://www.tofugu.com/japanese/japanese-counter-hiki/#pronunciation-of-japanese-counter-) explicitly gives 一匹／いっぴき, 二匹／にひき, and 三匹／さんびき.

**Confidence:** High. This is a localized missing example, not an incorrect reading or a demand for exhaustive counter instruction.

## Optional

None.

## Limits

- Snapshot identity, cleanliness, and the claimed unchanged legacy text could not be independently diff-verified without Git.
- The supplied source records were inspected, but upstream downloads and hashes were not independently regenerated. Additional public dictionary lookups are live evidence, not frozen downloads.
- Stroke files were described as generated by the existing pinned KanjiVG converter. **No exhaustive drawing-path audit was performed**, as assigned.
- Naturalness judgments are editorial assessments, not native-speaker certification or corpus-frequency measurements. No consequential linguistic claim remains unresolved within the reviewed scope.
- **CLEAN** means no established actionable defect in this scope, not exhaustive truth.
