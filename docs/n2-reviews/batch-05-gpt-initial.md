## Snapshot: d9f323abaec692983e6ca2d31f419edb644974f5

**Committed files only**, relying on the supplied clean-worktree confirmation. I have file tools but **no Git execution**, so I could not independently verify HEAD, cleanliness, or the diff from baseline `bc9ca10052766e7d240a769e1e29bd068282755a`.

## Scope:

**GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`**, working independently and sequentially, without delegation or edits.

Read all 18 assigned teaching pages completely. Reviewed `kanji\中.md` only for the affected quiz answers and fallback. Inspected the component-link passages in context in these 16 existing articles: `words\中央.md`, `words\典型.md`, `words\固い.md`, `words\国境.md`, `words\地域.md`, `words\坂.md`, `words\型.md`, `words\城.md`, `words\塔.md`, `words\塗る.md`, `words\塩.md`, `words\境.md`, `words\奥.md`, `words\奥さん.md`, `words\平均.md`, and `words\環境.md`.

Read the three requested instruction/format documents, the source snapshot, all 15 metadata records, and all 52 selected JMdict records. Checked relevant existing titles, comparisons, supporting links, and direct exclusions. No assigned teaching page or related link passage was omitted.

**Excluded:** unrelated legacy prose, exhaustive stroke-path inspection, `docs\n2-authoring-notes.md`, `docs\n2-review.md`, `REVIEW.md`, `docs\n2-reviews\`, session authoring inputs, and other reviewers’ output.

## Verdicts:

**One minor scoped-coverage issue; no incorrect reading or metadata value established.**

| Page | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\固.md` | CLEAN | CLEAN | CLEAN |
| `kanji\圧.md` | CLEAN | CLEAN | CLEAN |
| `kanji\坂.md` | CLEAN | CLEAN | CLEAN |
| `kanji\均.md` | CLEAN | CLEAN | CLEAN |
| `kanji\型.md` | CLEAN | CLEAN | CLEAN |
| `kanji\埋.md` | CLEAN | CLEAN | CLEAN |
| `kanji\城.md` | CLEAN | **NEEDS FIX** | CLEAN |
| `kanji\域.md` | CLEAN | CLEAN | CLEAN |
| `kanji\塔.md` | CLEAN | CLEAN | CLEAN |
| `kanji\塗.md` | CLEAN | CLEAN | CLEAN |
| `kanji\塩.md` | CLEAN | CLEAN | CLEAN |
| `kanji\境.md` | CLEAN | CLEAN | CLEAN |
| `kanji\央.md` | CLEAN | CLEAN | CLEAN |
| `kanji\奥.md` | CLEAN | CLEAN | CLEAN |
| `kanji\姓.md` | CLEAN | CLEAN | CLEAN |
| `words\圧力.md` | CLEAN | CLEAN | CLEAN |
| `words\埋める.md` | CLEAN | CLEAN | CLEAN |
| `words\姓.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no actionable defect established within this scope—not exhaustive truth or native-speaker certification.

## Findings:

**F01 — Minor · Scoped coverage · `kanji\城.md:20,29,39` — 傾城 needs a historical-register qualification.**

The card correctly supplies **傾城 けいせい — “beauty; courtesan”** as a セイ example, but neither its introduction, reading row nor explanatory note identifies its historical usage. A learner could interpret the unqualified gloss as a current general-purpose expression.

**Minimal remedy:** retain the reading and example; append a concise qualification such as “historical/literary term,” particularly for the courtesan sense. This concerns the example word’s register—not the validity of セイ or merely an uncommon spelling.

**Exact evidence:** `docs\n2-batch-sources\batch-05.json:2526-2575`, JMdict entry **1249540**, establishes the spelling, reading and two gloss groups but supplies no register flag. Independently fetched [Kotobank, 傾城](https://kotobank.jp/word/傾城-164172): *精選版 日本国語大辞典*, heading **けい‐せい【傾城・契情】**, confirms the beauty and courtesan meanings; *日本大百科全書*, heading **傾城（花魁、娼妓）／けいせい**, explicitly states **「明治以後はほとんど使われなくなった」**—it largely fell out of use after the Meiji period. **Confidence: high.**

No other actionable defect was established:

- Every supplied kanji reading, primary stroke count, canonical radical/number and grade tag matches its source record. Reading examples respect the inspected spelling/sense restrictions; 圧 and 奥 honestly qualify their source-only readings.
- All **45 distractor assignments** reference existing cards and supply semantically wrong displayed answers. Every new kanji has three choices and a useful linked word article. 中’s added 申 (“humbly say”) is wrong for 中; its three curated options avoid the default fourth-choice fallback that could otherwise introduce overlapping 央.
- All three new word articles have complete written-kanji metadata, verified lexical identities, appropriate examples/translations and useful contrasts, without inferred vocabulary JLPT levels. Direct exclusions cover 埋める/詰める, 埋める/記入, 姓/名 and 姓/名前; no transitive exclusion assumption was needed. The 16 related component-link passages are consistent with their targets.

## Optional:

None.

## Limits:

Repository provenance and the precise baseline diff remain independently unverified because Git execution was unavailable; judgments apply to the supplied on-disk contents.

The evidence file is a selected extraction, not the complete dictionary. I did not treat omitted spellings or missing priority flags as evidence of absence or rarity. Source-only readings remain lookup inventory, not independently established everyday vocabulary examples.

The 15 generated stroke files’ converter provenance was supplied; I did **not** inspect or certify their drawing paths. No consequential linguistic claim remains unresolved within the reviewed scope.
