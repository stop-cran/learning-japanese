# Numbers & counters: N4-oriented extension

This is an editorial everyday-language allocation, not an official JLPT inventory
or a claim that a finite set establishes N4 mastery. The [official level description](https://www.jlpt.jp/e/about/levelsummary.html)
concerns basic Japanese in familiar reading/listening situations; the [FAQ](https://www.jlpt.jp/e/faq/#anchor28)
does not provide a current exhaustive vocabulary/grammar list. Written and reading
recall support learning but do not themselves establish listening comprehension.

The original [N5 foundation](counter-n5.md) remains unchanged: 22 files, 124 suffix
cards, 20 reverse questions and 123 whole expressions (267 authored records).
Baseline content commit: `675ed8315ed218d18016781576416bddafdca070`.
The companion learner article remains [Numbers, counters, time and dates](../articles/numbers-and-counters.md).

## Runtime and ownership

- App [#73](https://github.com/stop-cran/kanji-cards-android/issues/73), commit
  `f20a8cae22a8d61a0e95b2279a0ce6f70fb7c5fc`, adds source-persisted N5 / N4 + N5 / All levels.
  Intersect level and group once; retain foreign reverse references without enqueueing them.
  Filters retain the same IDs, review evidence and shared allowance.
- New files have `level: 4`; do not relabel complete N5 families just to add compounds.
  Follow the existing [v2 transport and grading contract](counter-n5.md#version-2-transport-and-future-authoring).
  V1 and v2 stay in separate files. No schema, media, engine or Room migration is required.
- Numbers & counters owns quantities, units, complete expressions and their readings.
  Existing [quantity Grammar](../grammar/quantity-scope.json) owns frequency, scope,
  boundaries and related sentence interpretation; do not recreate those lessons here.
- The focused ずつ follow-up is a useful bridge but follows the repository's Bunpro-aligned
  **N3** grammar placement, not a new N4 classification exception. It has its own work item.
- New Listening media, paid generation, broad animal/industrial-counter expansion and
  exhaustive number-by-counter drilling are outside this bounded series. No new audio
  acceptance or official coverage percentage is claimed.

## Foundation matrix: content #39

The new foundation has **100 whole expressions in 20 v2 files**, each available for
Write and Read. Those are 100 authored identities, not 200 independent examples.
The nine traditional families are compound-form/reading extension, not 27 new
independent counter-selection contexts. A cue naming a unit or construction is a
constrained form drill; it must not be credited as spontaneous counter choice.

| Files | Records | Coverage |
| --- | ---: | --- |
| `honcompound`, `hikicompound`, `maicompound`, `nincompound`, `kocompound`, `satsucompound`, `daicompound`, `haicompound`, `kaicompound` | 27 | Eleven, a twenties/four-person compound and thirty; contracted versus unchanged sounds; 人/名 and 回/度 alternatives |
| `prices` | 16 | Irregular hundreds/thousands, 万 grouping, a million yen, internal zero and mixed amounts, 何円 |
| `length` | 6 | Metres/kilometres, decimal length, 何メートル |
| `weight` | 6 | Grams/kilograms, irregular hundreds, half a kilogram and decimal zero |
| `percent` | 4 | Whole percentage rates and their interrogative, not discount arithmetic |
| `temperature` | 4 | Positive, negative, fractional 度/分 and an interrogative; temperature 分 is ぶ |
| `calendaryears` | 4 | Four full calendar years, including the よねん ending |
| `compounddates` | 6 | Month/day and year/month/day composition, inherited exact date variants and a real leap-day date |
| `timetable` | 6 | 24-hour values, midnight, composite minutes and distinction from durations |
| `durations` | 6 | Hours/minutes, half hours, years/months and half months; no false fixed-day conversion |
| `labels` | 7 | 番, 番線, 番乗り場, 号, 号室 and 何番; identifying numbers versus quantities |
| `ordinals` | 8 | 番目, 回目/度目, 人目, native つ目 and 何番目 |

The time group contains 22 new expressions; Everyday contains 78. The baseline
already supplies most simple counter and time interrogatives: do not duplicate
each one merely to pad an N4 total. Native つ does not extend to 十一つ.

After this item the aggregate is 42 files and 367 authored records:
124 suffix + 20 reverse + 223 whole expressions. Read projects 346 eligible
identities from v1 and v2; already-kana prompts remain excluded. N5-only membership
and its 246 Read identities are unchanged.

## Evidence and answer policy

Inspect exact entries, not search summaries or generic sound rules. These sources
support usage and readings, not official JLPT classification:

| Source | Inspected evidence and its limits |
| --- | --- |
| [IMABI numbers](https://imabi.org/sino-japanese-numbers-2/) | Eleven-to-100 composition; irregular 三百/六百/八百/三千/八千; 千/一千 and number grouping. Use the modern ordinary readings, not every historical or proper-name reading. |
| [IMABI counter tables](https://imabi.org/counters-with-sino-japanese-numbers-i/) | Exact suffix sounds for 円/冊/枚/匹/台/杯/本/個/人, including fourteen-person よにん and tens contractions. This is an inspected secondary reference, not direct inspection of its cited NHK dictionary. |
| [Irodori Elementary 1 wordlist](https://www.irodori.jpf.go.jp/assets/data/wordlist_Y.pdf) | PDF p.10: マイナス and temperature; p.45: 38度5分 with 分 read ぶ. The latter is a tenth of a degree, not a minute. |
| [Irodori Elementary 2 wordlist](https://www.irodori.jpf.go.jp/assets/data/wordlist_Z.pdf) | PDF p.23: numbered platforms/boarding points; around p.29: 回目 and 14時–15時; p.46: percentages; p.64: 円札 including 一万円札. |
| [Marugoto Elementary 1 A2 index](https://marugoto.jpf.go.jp/assets/docs/download/elementary1_c/MarugotoElementary1CompetencesVocabularyIndex_EN.pdf) | Yen, metres/kilometres, number labels and everyday counts. A2 course inclusion is a practical relevance criterion, not a JLPT equivalence proof. |
| [Marugoto Elementary 2 A2 index](https://marugoto.jpf.go.jp/assets/docs/download/elementary2_c/MarugotoElementary2CompetencesVocabularyIndex_EN.pdf) | Grams, degrees, percentages and occurrence ordinals. |
| [Tofugu 時間](https://www.tofugu.com/japanese/japanese-counter-ji-jikan/#hours) and [分](https://www.tofugu.com/japanese/japanese-counter-fun/#unit-for-minutes-of-time) | Half-hour composition and optional duration 間 after minutes. |
| Published N5 expressions and their cited sources | Compose calendar/time readings from their exact owning senses. Never use a duration's 一日 reading for a calendar date. |

Writing is binary in v2. Accept fitting alternative expressions as well as
ordinary spellings, or visibly constrain the requested operation. Do not silently
reject an equally suitable sentence because the author preferred another form.
For multi-component month durations, unrestricted numeral and six unit-spelling
combinations exceed the 16-answer bound: the affected prompts explicitly request
Arabic digits without connecting と or final 間. They are spelling drills, not a
claim that other natural duration expressions are ungrammatical.
The two-and-a-half-hour prompt also excludes connecting と, while accepting
half-hour, decimal-hour and hours/minutes forms, including final 分間.
Mixed Arabic/kanji place-value spellings are accepted for prices. Negative Celsius
answers distinguish hyphen-minus from mathematical minus: NFKC does not merge those
signs, although it does merge ℃ with °C. Do not waste two answer slots on the latter.

Readings pronounce **only the displayed canonical expression**. 二時間三十分 can
be a written answer for two and a half hours, but its reading does not answer a
displayed 二時間半. The same rule applies to formal people, occurrences, symbols,
abbreviations, negatives and alternate calendar spellings. Neither automatic
number arithmetic nor permissive numeral normalization should be added to grade
these expressions.

## Review and publication

The independently reviewed work items are content [#39](https://github.com/stop-cran/learning-japanese/issues/39)
(foundation), [#40](https://github.com/stop-cran/learning-japanese/issues/40)
(practical families), and [#41](https://github.com/stop-cran/learning-japanese/issues/41)
(quantity-grammar bridge), following app #73.

Before publication, review every cue, canonical spelling, accepted written form,
canonical reading, accepted reading and explanation for correctness, scoped
coverage and comprehensibility. Classify repeated number cases and reading
projections honestly. Run counter tests, the full validator, manifest regeneration,
archive budgets and the real Android importer after staging new files; force the
importer's test task to rerun when only content changed. Keep the original N5 file
hashes unchanged and exercise the new level/group intersections.

### Foundation review reconciliation

One independent language reviewer examined all six learner-visible fields of all
100 expressions, the article extension and both changed coverage documents at
candidate manifest `64ba1073b5274444`. Scoped coverage and comprehensibility were
CLEAN; correctness needed three minor written-answer fairness fixes: duration
spellings, mixed-place price notation and negative Celsius notation. All three
were resolved and independently reconciled against the actual three-file diff.
Final verdicts were CLEAN in all three facets; canonical spellings/readings were
unchanged and no previously accepted answer was removed. This is a bounded review,
not an exhaustive enumeration of every possible Japanese expression.

Native acceptance retains the real N5 corpus and makes its isolated review states
future-due when selecting new N4 material. It does not relabel N4 files as N5 or
remove reference data to manufacture a pass. App test companion
`1dd903dc533139561b74f043c46441858e56b432` covers N5 and N4 Write/Read, article Back
and production session continuation, with explicit light/dark palettes. The final
publication and exact validation evidence are recorded on content #39.
