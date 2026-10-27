## Snapshot: 3ec3eeab4373dc84ade3cd189534d1eae55f4033; committed files only

Baseline supplied: `1023fa9`. **Git execution was unavailable**: this report relies on the requester’s identification of the clean checkout. I did not independently verify the commit, cleanliness, or baseline diff.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Single-reviewer, sequential, read-only review. All 20 new pages listed below were read completely and assessed independently for correctness, scoped coverage and comprehensibility.

Reviewed the three required instruction/format passages, the source snapshot, all 15 metadata records and all 64 selected word-evidence records. Checked actual distractor titles, relevant legacy two-choice fallback, word-title overlaps, symmetric/direct exclusions, homophones and supporting links.

The 13 link-only passages reviewed under `words\` were: `個人.md:25`, `倍.md:23`, `停留所.md:24`, `傾向.md:24`, `億.md:21`, `党.md:24`, `再び.md:25`, `再来年.md:24`, `再来月.md:22`, `再来週.md:24`, `凍る.md:24`, `印刷.md:24`, and `想像.md:24`. Their corresponding character links resolve to the intended new cards; no actionable link defect was established.

**Not reviewed:** unrelated legacy teaching, nanori, old four-level JLPT assignments, exhaustive stroke drawing paths, other reviewers’ reports, adjudication or authoring inputs. No assigned new page or related link passage was omitted.

## Verdicts:

“Correctness” includes quiz-answer uniqueness. **CLEAN** means no actionable defect established within this scope, not exhaustive truth or native-speaker certification.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\個.md` | CLEAN | CLEAN | CLEAN |
| `kanji\倍.md` | CLEAN | CLEAN | CLEAN |
| `kanji\停.md` | CLEAN | CLEAN | CLEAN |
| `kanji\傾.md` | CLEAN | CLEAN | CLEAN |
| `kanji\像.md` | CLEAN | CLEAN | CLEAN |
| `kanji\億.md` | CLEAN | CLEAN | CLEAN |
| `kanji\兆.md` | CLEAN | CLEAN | CLEAN |
| `kanji\児.md` | CLEAN | CLEAN | CLEAN |
| `kanji\党.md` | CLEAN | CLEAN | CLEAN |
| `kanji\兵.md` | CLEAN | CLEAN | CLEAN |
| `kanji\冊.md` | CLEAN | CLEAN | CLEAN |
| `kanji\再.md` | CLEAN | CLEAN | CLEAN |
| `kanji\凍.md` | CLEAN | CLEAN | CLEAN |
| `kanji\刊.md` | CLEAN | CLEAN | CLEAN |
| `kanji\刷.md` | CLEAN | CLEAN | CLEAN |
| `words\兆候.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\児童.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\兵士.md` | CLEAN | NEEDS FIX | CLEAN |
| `words\冊子.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\刊行.md` | CLEAN | CLEAN | CLEAN |

All 15 kanji reading lists, primary stroke counts, canonical radicals/numbers and grade tags match the supplied metadata. Reading examples respect the inspected spelling/reading/sense evidence. Source-only rows appropriately disclose their limitations. Each kanji has a useful linked vocabulary article and three existing, plausible, semantically wrong curated choices.

## Findings:

### G01 — Moderate; correctness: incomplete exclusions for 兆候

**Location:** `words\兆候.md:4–8,15`.

The exclusions omit **症状** and **サイン**, allowing defensible alternative meaning answers. For 兆候, the existing title “symptoms” matches a documented sense. For サイン, the new title “sign; indication” matches its documented indication sense. This can penalize correct vocabulary knowledge.

**Minimal remedy:** add `症状` and `サイン` to 兆候’s direct `quiz_exclusions`; preserve the accurate glosses.

**Exact evidence:** `words\症状.md:4,15` gives “symptoms”; `words\サイン.md:4,9,16` gives its different displayed title, current exclusions and sign/indication meaning. Neither declares a reverse exclusion. `docs\n2-batch-sources\batch-02.json:2168–2205`, JMdict **1597620**, explicitly includes “symptom” for 兆候・ちょうこう. The inspected [Jisho JMdict result for サイン](https://jisho.org/api/v1/search/words?keyword=%E3%82%B5%E3%82%A4%E3%83%B3), second sense of the autograph/sign entry—not the separate sine entry—gives “sign, signal, indication.”

**Confidence:** high.

### G02 — Moderate; correctness: 児童 and 少年 remain competing “juvenile” answers

**Location:** `words\児童.md:4–8,41`.

児童’s title is “children; juvenile”; existing 少年’s title is “boy; juvenile.” Their complete title strings differ, so exact-title deduplication does not protect this pair. The shared juvenile meaning makes them unsuitable context-free opposing answers, despite their useful everyday and contextual distinctions.

**Minimal remedy:** add `少年` to 児童’s direct exclusions. No title change or universal age definition is needed.

**Exact evidence:** `words\少年.md:4,9,16–18` supplies its title, exclusions and broader legal juvenile/child sense; no reverse exclusion exists. `docs\n2-batch-sources\batch-02.json:2246–2282`, JMdict **1315060**, gives “children, juvenile” for 児童・じどう. The problem is meaning overlap, not the unrelated homophone 自動.

**Confidence:** high.

### G03 — Moderate; correctness: 冊子/図書 needs its own exclusion

**Location:** `words\冊子.md:8,15–16,32–40`.

冊子 explicitly includes the broader book sense, but its exclusions cover only 本 and 書物. Existing 図書 displays “books,” a defensible answer for that sense of 冊子. Both pages’ exclusions involving 本 do **not** exclude 冊子/図書: exclusions are not transitive.

**Minimal remedy:** add `図書` directly to 冊子’s exclusions.

**Exact evidence:** `words\図書.md:4,9,16–24` gives “books,” excludes only 本, and explicitly allows a singular book. `docs\n2-batch-sources\batch-02.json:3038–3074`, JMdict **1298530**, includes “book” for 冊子・さっし. The inspected [Seisenban 冊子 entry](https://kotobank.jp/word/%E5%86%8A%E5%AD%90-511053), **さっし**, sense 1, likewise includes books generally.

**Confidence:** high.

### G04 — Minor; scoped coverage: explain the ordinary rank-and-file sense of 兵士

**Location:** `words\兵士.md:15–16,35,39–40`.

The broad military-service definition and statement that rank is unspecified omit the ordinary distinction between **rank-and-file soldiers and officers**. “There is no requirement … be an officer” does not teach that distinction. Learners may consequently treat 兵士 as an unrestricted equivalent of any military member.

**Minimal remedy:** explain that 兵士 normally refers to rank-and-file soldiers serving under officers, while not specifying an exact rank. Qualify this as ordinary usage rather than imposing an absolute restriction on every context.

**Exact evidence:** the inspected [Seisenban 兵士 entry](https://kotobank.jp/word/%E5%85%B5%E5%A3%AB-624031), specifically **へいし**, sense 1—not the separate historical **ひょうじ** entry—defines soldiers under officers’ command and supplies 兵卒 as an equivalent.

**Confidence:** medium-high. The finding concerns a missing useful distinction, not a claim that the existing examples are wrong or that every broader use is impossible.

## Optional:

**Nonblocking polish:** at `kanji\刷.md:44`, add **刷ります（すります）／刷って（すって）** to make the distinction from general-purpose **します／して** immediately usable. The existing reading and lexical distinction are correct.

## Limits:

No live app execution was available; quiz findings follow the documented title/exclusion behavior and the inspected pinned `QuizBuilder`. Arbitrary reduced card pools were not exhaustively evaluated.

Stroke files were treated as generated by the existing pinned KanjiVG converter; **no exhaustive drawing-path audit** was performed. Naturalness was assessed editorially, not through a comprehensive corpus study or native-speaker certification.

Public dictionary pages are current lookups rather than frozen artifacts. The 兵士 distinction rests on the identified Seisenban sense; additional Weblio/Kanjipedia attempts supplied no usable corroboration and were not treated as evidence. No consequential unresolved linguistic claim otherwise remains identified in the assigned scope.
