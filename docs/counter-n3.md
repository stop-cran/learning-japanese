# N3 Numbers & counters: coverage and calibration contract

Status: **contract and pilot accepted for B/C/D authoring** (2026-10-29).
The initial matrix review and additional Marugoto B1 comparison found seven
actionable issues, now [independently reconciled](counter-n3-review.json).
Separate complete-pilot review found localized handout defects, now corrected
and independently accepted. The complete candidate `4f06ad3693ee5c04` passed
the actual importer and focused production-grading probes. Native app/release
acceptance remains separate; new-owner rows are still required unfinished work.

Work: [parent #52](https://github.com/stop-cran/learning-japanese/issues/52),
[contract/pilot #54](https://github.com/stop-cran/learning-japanese/issues/54),
[numerical forms #53](https://github.com/stop-cran/learning-japanese/issues/53),
[counter families #56](https://github.com/stop-cran/learning-japanese/issues/56),
[time/measures/interpretation #57](https://github.com/stop-cran/learning-japanese/issues/57),
[release acceptance #55](https://github.com/stop-cran/learning-japanese/issues/55)
and [Android #109](https://github.com/stop-cran/kanji-cards-android/issues/109).

## What this claim means

This is a practical intermediate extension of the unchanged N5/N4 foundation,
not an official exhaustive JLPT counter list, a complete mathematics curriculum,
or a list of everything bearing a number in Japanese. N3 allocation in a
counter file is an editorial study placement unless an exact lexical
spelling/reading/sense has separate source membership. CEFR A2/B1 or B1 course
inclusion does not establish a JLPT equivalence. Grammar keeps its own
Bunpro-first, complete-task classification; new material in this project can
legitimately remain N4, N5 or unclassified.

The denominator is the union of:

1. Existing numerical operations, not just filenames or suffix inventories.
2. Numerical senses in the pinned community N3 vocabulary index, with its
   documented identity corrections retained.
3. Practical gaps identified in inspected intermediate resources and exact
   usage references, followed by an independent additional-reference check.

The source and coverage ledger is [counter-n3-sources.json](counter-n3-sources.json).
Its `rows` are the finite coverage denominator; `lexicalCandidates` account for
the broader lexical screening, including false positives. A candidate is not
automatically a new exercise. `new-owner` means **required work, not coverage**.
Inherited existing coverage counts only for the operation actually inspected.
Reference-only and deferred items do not count as practised.
The operation-specific baseline map covers all 54 unchanged counter files,
including age/floor practice and actual reverse records; an expression is
not counted as contextual selection evidence.

The initial screening used English numerical/unit glosses and Japanese
headwords, then a second pass for labels, arithmetic, changes, prices and
measurements. It is not proof that regex matching finds every numerical sense.
Raw source rows and the earlier sense mapping remain in the pinned TSV rather
than being silently rewritten here. The independent reference cross-check must
identify omissions, not merely confirm these headings.

## Immutable starting point and reuse

Content: `b697a3d65a4edf893b04eea33d2356cd600e87c9`.
App: `7b87b24a39d8e46c4cf42db8436dcd68df3a823e`.
The generated [baseline inventory](counter-n3-baseline.json) pins exact bytes,
all record IDs and canonical object hashes, including unrelated Grammar
exercises so a later preservation comparison can detect accidental changes.
The inventory itself is not a linguistic review.

The 54 counter files contain 148 forward cards, 32 reverse records and 272
expressions: 452 authored records, 420 forward/expression identities. The
projected reading pool is 419 identities because one source expression is
already kana. None is level 3. Preserve their bytes, levels, IDs and accepted
forms; do not relabel or duplicate them to inflate the extension.

Actual existing coverage includes compound counts, million-yen prices and
internal zero, decimal lengths/weights, whole percentages, negative
temperatures, calendar dates, 24-hour times, hours/minutes and years/months,
platform/room labels and generic ordinals. For example:

| Existing evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| `prices-expression-11`, `-14`, `-15` | Million yen, compound grouping, internal zero | Productive 億/兆 grouping |
| `weight-expression-6`, `length-expression-5` | Decimal readings, including zero alternatives | Fractions or reading every equivalent written answer |
| `percent-expression-1` through `-4` | Whole percent notation and reading | Discount amount versus price left to pay |
| `durations-expression-1` through `-6` | Compound duration and half-units | Seconds, or a fixed day conversion for calendar months |
| `labels-expression-1` through `-7`; `ordinals-expression-1` through `-8` | Labels and requested ordinal forms | New document counters or the meaning of every rank suffix |
| Existing `ken` questions | Contextual alternatives for houses/shops | Dedicated 戸/棟 selection and readings |
| All 28 `quantity-scope` tasks | Inclusive/strict bounds, benchmark/indefinite amount, per-period frequency, negative scope, resource/price/activity frames | Fraction/discount/ratio interpretation |
| All 16 `quantity-zutsu` tasks | Per-unit versus total; grouped/repeated amounts; implications | A new numerical-comprehension engine, or more copies of the same scenarios |
| Five `particle-neighbors` quantity tasks | Approximation versus exclusive limits | Productive 数十/十数 or exact uncertainty intervals |
| Six `means-and-scope-rank` tasks | Comparison domain, non-first rank anchor, preference versus location | Reading ～位, ～級 or chapter labels |
| Existing `n5-comparisons-change` superlative/set tasks | Named comparison sets and maxima | A new need to reteach 一番 |

Paired interpretation questions share a context key. Changing a number or noun
does not create another independent context. Support vocabulary such as 合計
and 残り is not itself proof of a tested total/remainder operation.

## Required strands and ownership

The machine-readable rows give exact source sections, sense restrictions,
planned context keys, sound classes, modes and completion requirements.

| Owner | New required work | Reused foundations |
| --- | --- | --- |
| B / #53 | 億/兆 and mixed large-number notation with place-value language support; fractions/mixed numbers; 割 and discount forms; ratios/倍; 数・十数・数十, non-interrogative 何百 and bounded approximation forms | Decimal numbers, prices through 百万, whole percentages |
| C / #56 | 頭/羽; copies 部 and correspondence 通; 箱/袋/皿/組/束; 粒/錠/件/品; housing 戸/棟 and 部屋; lesson/chapter/section/episode/volume labels and counts; 位/級/段; 人前/人分, tofu 丁, group membership 人組, merchandise/scores 点, 種類, slices/bunches, numerical ways 通り, digits/text units including 以内 character limits, flight labels and 株 counts | Basic object counters, 軒/名/回/度/泊, ordinary labels and 目 |
| D / #57 | 秒 and minute-second durations; capacity, metric tons, everyday speed; housing area, rice 合 and cooking measures; age/price bands, decades and centuries; interval-before-repeat ～ぶり; genuine missing fraction/discount/ratio/uncertain-amount and 以内 interpretation in existing quantity owners | Existing mixed durations, decimal measures, quantity-scope and quantity-zutsu operations |
| E / #55 | Whole matrix, distinct contexts, preservation, actual importer/native paths, immutable archive, compatible publication | Individual batch checks are necessary, not combined delivery evidence |

These are functional owners, not commands to create one file per row. V1 and v2
remain separate. Estimated new records are approximately B 45-65, C 140-200
and D 30-50, with the pilot included once. These planning bands are neither
quotas nor caps. Reassess after the reviewed rows and actual contexts, rather
than padding or discarding a practical gap to meet a total.

The reference-only boundary is finite: fractional 厘/毛, historical volume
勺/升/斗/石 and mass 匁/貫, detailed 尺貫法 conversion tables, formal 壱/弐/参,
and 京/垓 or higher magnitudes. This is a curricular boundary, not a measured
claim that every traditional use is uncommon. Housing area (including 畳/坪),
rice 合 and recipe spoon measures now have required bounded rows; ordinary
shopping discounts and package/content distinctions remain required.
Specialized finance/science courses and medical dosing instruction remain
outside the project. Practical additions surfaced by review are included,
not dismissed to fit an estimate. No owner approval of a significant new
exclusion is asserted; if independent reconciliation identifies one in the
remaining boundary, obtain actual owner agreement before bulk work. Posting
under the owner's GitHub account is not that agreement.

## Runtime and answer contract

Keep the existing schema, parser epoch, database and SRS identities.
V1 trains contextual suffix selection/typing and noun-only reverse selection;
v2 trains whole expressions and the reading of the displayed canonical form.
Neither writing an expression nor recognizing its kana is automatically a
comprehension test. Interpretive choices live in existing Grammar owners.

The visible cue must identify the counted entity, unit, register and notation
where needed. Alternatives that remain natural in that context are accepted,
not used as wrong options. A stated writing convention can narrow formatting;
an invisible author's preference cannot. Do not equate packaging with pieces,
copies with sheets, a housing unit with a building, or a label with a quantity.
Reverse distractors must be wrong for the actual displayed noun, without the
forward sentence; do not use another animal as an allegedly incompatible 頭
distractor merely because it is small.

V2 limits remain 16 written alternatives, eight kana readings and 80 characters
per answer. NFKC/whitespace and kana normalization are not arithmetic or numeral
conversion. Readings pronounce only the displayed expression. Glosses appear
inline and must not reveal a tested fraction, discount result or unit decision.

The app's `counterReading` index is source-wide and keyed by displayed counter,
not by scope or file ID. Use distinct category metadata for expressions such
as fractions (分数), rather than introducing a new 分/ぶん file that overwrites
the existing minute 分/ふん label. Check every new displayed label/reading pair.
Do not introduce a broad engine change without a reproduced blocker.

New Grammar tasks use existing `quantity-scope`/`quantity-zutsu` ownership, with
additive groups/facets only where the operation genuinely differs. Preserve old
exercise objects, members, gates and edges. New groups belong to the existing
`focus-and-quantity` chapter. No new hard gate is required for this extension.
Use the vocabulary review tool and exact full-task context hashes; retain all
unrelated existing review records and their statuses.

## Pilot envelope and difficulty rubric

The authored pilot has 24 identities: 21 new records and three unchanged
controls. [Its record ledger](counter-n3-pilot.json) contains actual IDs, sources,
context keys, initial author scores and independent rubric comparisons.
[Complete-task text review](counter-n3-pilot-review.json), corrected-text
reconciliation and actual importer checks are accepted:

| New sample | Count | Learner-visible purpose |
| --- | --- | --- |
| 頭 forward and reverse | 4 | Contextual animal selection, 1/6/8 sound classes, fair noun-only reverse |
| 部 forward | 3 | Complete document copies versus loose sheets/bound volumes; no automatic contraction |
| Magnitude expressions | 2 | 億 grouping and a zero-containing amount, not merely a longer numeral |
| Fraction | 1 | Denominator-first writing/reading |
| Uncertain amount | 1 | 数十 versus 十数 as a requested form |
| Proportion/discount form | 1 | 割引 as reduction, not the retained proportion |
| Packaging expression | 1 | Box count versus stated contents |
| Lesson label/count expressions | 2 | Identifier versus count is the actual requested decision |
| Seconds/compound duration | 2 | Minute/second components and actual duration |
| Paired discount interpretation | 2 | Reduction amount versus payable amount in the same context |
| Paired fraction interpretation | 2 | Used amount versus remainder, resolving a fraction against a stated whole |

Controls: `prices-expression-15`, `durations-expression-2`, and
`quantity-zutsu-stickers-total`. The first draft proposed only the discount
pair, but the existing curriculum validator requires two distinct contexts per
facet. The fraction-reference pair supplies a genuinely different construction;
reducing the unchanged controls keeps the envelope at 24. No validator was
relaxed, and paired questions do not acquire artificial independent keys.
The four new numerical interpretations are unclassified rather than borrowing
N3 from the project or a level from incidental grammar.

Score each complete task on the following small rubric; these are editorial
comparisons, **not measurements of learner proficiency**:

| Facet | Foundation / 0 | Ordinary intermediate / 1 | Upper edge / 2 |
| --- | --- | --- | --- |
| Lexical load | Familiar words or answer-safe readings/glosses | A few supported practical nouns | Multiple unfamiliar terms; simplify/support before acceptance |
| Decision load | One supplied unit/form | Select the relevant unit or distinguish two meanings | Integrate a short context and an explicit contrast |
| Calculation | None | One transparent operation with small numbers | Multi-step or large mental arithmetic: redesign unless indispensable |
| Answer ambiguity | Explicit operation; all fitting alternatives handled | Context needed but resolves the decision | A plausible rejected answer: fix, not a difficulty feature |
| Feedback | Names the requested quantity/form | Explains why a tempting alternative changes the unit/sense | Missing/inconsistent branch: fix, not an upper-level feature |

Ordinary N3 extension tasks should add a meaningful decision without increasing
every facet simultaneously. Bigger numbers, rarer counters and unsupported
kanji do not independently establish difficulty. Upper-edge examples still
need manageable arithmetic and honest support. Foundation controls demonstrate
the comparison's baseline; they are not new N3 records.

## Acceptance and evidence

Two independent passes are distinct: (1) matrix/reuse/exclusion review plus
an additional independently compiled intermediate source not used above,
and (2) complete pilot text, every answer/choice/feedback branch, lexical
support and calibration. Initial reviewers receive the snapshot and rubric,
not the author's prior review verdicts or one another's findings.

Record report paths/hashes, actual reviewer models and reconciliation states.
An unresolved consequential claim cannot be marked clean. Nothing here claims
native-speaker endorsement, an empirical learner trial, audio perception
acceptance, or a physical-phone check.

Before A can unblock B-D, run the focused content/Grammar checks and the app's
production real-content importer against the stable pilot, forcing
`cleanTestDebugUnitTest testDebugUnitTest --tests '*ContentTest*'`. Before E,
also compare every baseline record/file, check all matrix evidence IDs, counts
and context keys, inspect native genuine-level-3 flows with the easier corpus
still present, and verify exact published ZIP manifest entries/hashes and
compatible app publication. A successful synthetic fixture is not actual
N3-content acceptance. Full release/CI checks remain in #55.
