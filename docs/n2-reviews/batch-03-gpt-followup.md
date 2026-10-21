## Snapshot

`35e794f234701002bb2d09b54ce20ce2ad8506c0` — committed files only, as identified by the requester. Compared with initial review snapshot `408be09e0156fc6ed3c0ed1b1b0ac67f592eb1a9` using the supplied Git-generated diff.

**Git execution was unavailable:** I could not independently verify either checkout identity or worktree cleanliness.

## Scope

**Reviewer:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`; sole reviewer, read-only, without delegation or edits.

Read my preserved initial report, the required instructions, **all 83 diff lines and seven hunks**, and the complete current versions of the five changed pages. Inspected relevant current source records, external counter-pronunciation evidence, and all five referenced exclusion cards’ actual titles and relevant meanings.

Not re-reviewed: the thirteen unchanged new pages, unrelated legacy teaching, or stroke drawing paths. No other reviewer’s reports, author adjudication, or prohibited authoring inputs were accessed.

## Verdicts

These verdicts apply to the changed passages and their surrounding context.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\刺.md` | CLEAN | CLEAN | CLEAN |
| `kanji\勢.md` | CLEAN | CLEAN | CLEAN |
| `kanji\匹.md` | CLEAN | CLEAN | CLEAN |
| `words\副作用.md` | CLEAN | CLEAN | CLEAN |
| `words\匹敵.md` | CLEAN | CLEAN | CLEAN |

## Findings

**No actionable finding remains in the changed-passage scope. Both initial findings are resolved.**

**R01 — RESOLVED.** Original severity: Moderate; facet: correctness.
**Location:** `words\匹敵.md:8,30`.

The missing direct exclusions could permit competing defensible equality labels. The remedy is implemented: `同様` and `同一` are now directly excluded alongside the original three entries, without relying on transitivity. Their existing titles remain “same; similar” and “identical; one and the same.” The added comparison accurately distinguishes matching ability from identity.

**Evidence:** current source packet `docs\n2-batch-sources\batch-03.json:3165–3207`, JMdict **1487250**, supports 匹敵／ひってき as matching or equaling. The inspected exact [同様／どうよう](https://jisho.org/api/v1/search/words?keyword=%E5%90%8C%E6%A7%98) and [同一／どういつ](https://jisho.org/api/v1/search/words?keyword=%E5%90%8C%E4%B8%80) records both include “equal” in their relevant first senses. Direct exclusions satisfy `docs\content-format.md:85–98`. **Confidence: High.**

**R02 — RESOLVED.** Original severity: Minor; facet: scoped coverage.
**Location:** `kanji\匹.md:31,40,45`.

The formerly isolated counter reading now has the usable example **二匹 にひき**. The note demonstrates **一匹 いっぴき**, **二匹 にひき**, and **三匹 さんびき**, making the pronunciation warning actionable without requiring an exhaustive chart.

**Evidence:** current source packet `docs\n2-batch-sources\batch-03.json:3208–3275`, JMdict **1583370**, supports the small-animal counter sense; `:563–580` records the external pronunciation evidence. The linked [Tofugu pronunciation table](https://www.tofugu.com/japanese/japanese-counter-hiki/#pronunciation-of-japanese-counter-) explicitly confirms all three forms. **Confidence: High.**

The remaining changed passages introduce no established regression:

- **`kanji\刺.md:33,47`:** removing “sense 3” preserves the correctly qualified noun example 刺し／さし, “stabbing; piercing.” Source packet `:1094–1163`, JMdict **1306410**, explicitly supports that sense; the surrounding note still acknowledges other senses.
- **`kanji\勢.md:47`:** restricting the noun explanation to the force/momentum sense is accurate. Source packet `:2807–2899`, JMdict **1375040**, identifies those senses as nouns and separately records an adverbial sense. No additional sense inventory is needed here.
- **`words\副作用.md:33`:** the remaining statement correctly separates side effects from failure to achieve an intended effect. Source packet `:1658–1696`, JMdict **1500400**, supports 副作用／ふくさよう as “side effect; adverse reaction”; the inspected [Kotobank entry](https://kotobank.jp/word/%E5%89%AF%E4%BD%9C%E7%94%A8-123978) explains intended versus secondary effects. Removing the figurative-use sentence neither disproves that use nor makes the remaining medical explanation misleading.

## Optional

**Initial optional suggestions: none; reconciliation unchanged.** No new nonblocking expansion is requested.

## Limits

- **Initial snapshot/diff limit — partially resolved:** the actual teaching-content diff is now available and was inspected completely. Independent commit and cleanliness verification remains **unresolved** without Git.
- **Initial provenance limits — unresolved:** upstream downloads/hashes were not regenerated; public corroboration is live evidence rather than a frozen-source reproduction.
- **Initial methodological limits — unchanged:** no exhaustive stroke-path audit, corpus-frequency measurement, or native-speaker certification was performed.
- No consequential linguistic claim remains unverified within this changed-passage scope. **CLEAN** means no actionable defect established there, not exhaustive truth.
