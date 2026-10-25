# N5-oriented counter application set

[Issue #41](https://github.com/stop-cran/kanji-cards-android/issues/41) expansion of the
[20-card pilot](counter-pilot.md). [Draft data: counter-n5.yaml](counter-n5.yaml).

**Live content** now lives in `counters/<id>.json` (one file per counter, validated by
`tools/validate_counters.py` and listed in `manifest.json`); the YAML is the historical
draft and is no longer read by anything except `tools/validate_counter_draft.py`.
The original scope was ten counters with twelve forward examples each: **120 forward cards**,
plus **20 authored reverse questions** using those examples' nouns/contexts; all original identities remain.
The choose and typed forward modes share cards, not duplicate content.
The live JSON is published and app-loadable; only the historical YAML drafts stay outside the manifest.
The Numbers & counters expansion adds four forward gap prompts and 123 complete expressions below.
This is beginner-oriented coverage, not a claim that these are all counters tested at N5.
There is no official exhaustive JLPT counter/grammar syllabus.

## Coverage

| Counter | Coverage |
| --- | --- |
| 本 | Pens/pencils, umbrellas, films, bottles, trees, stemmed flowers, bananas/carrots and spoons |
| 匹 | Living aquarium fish/shrimp, cats, small dogs, frogs, mice, ants, insects and small turtles |
| 枚 | Paper, shirts, tickets, stamps, printed photographs, plates, postcards, handkerchiefs and towels |
| 人 | Students, family, friends, teachers, children, customers, passengers and swimmers |
| 個 | Fruit, eggs, individual small cakes, balls, sweets, stones, erasers and potatoes |
| 冊 | Books, notebooks, dictionaries, magazines, picture books, comics, textbooks, memo pads and photo albums |
| 台 | Cars, bicycles, buses, televisions, computers, refrigerators, cameras, pianos, beds and phones |
| 杯 | Cups/glasses of drinks and bowls of rice/soup, contrasting contents with containers |
| 回 | Repeated reading/viewing, calls, meals, bathing, writing, singing, button presses and frequency |
| つ | Objects, rooms, questions, seasons, homework tasks, menu orders and いくつ |

Most prompts are sentences. Nine bare-noun prompts provide a small amount of brief practice.
Every counter has a question prompt; approximate counts, a range, negatives, comparison,
irregular readings and frequency are mixed in where natural.
The two 本 examples for films and the 冊 photo-album/枚 photograph contrast cover less-obvious applications.
台 for beds/pianos and つ for abstract items extend beyond a single noun-to-counter stereotype.

The pilot's N4 `nin-each-1` (ずつ) is deliberately not part of this beginner set.
数ヶ月, 十数人 and further ordinal constructions remain later-level extensions.
Basic age, floors, time, dates and durations now have dedicated whole-expression practice.
Numbers are kanji in the original prompts, with Arabic equivalents accepted by the legacy numeric normalizer.
`noun` is a display/context label, not an assertion that every word is in an official N5 list.
Less-basic object names are written in kana when useful. The YAML `vocabulary` map supplies
selective reading/gloss support for both sentence prompts and reverse noun labels.

## Schema and answer policy

Each counter group supplies a stable ID, written counter, base reading, title and source IDs.
Each card supplies stable `id`, `kind`, Japanese `text` with one `{}`, English `en`,
counted `noun`, counted `phrase`, phrase `reading`, explicit `good`/`kana` forms and three `distractors`.
The file-wide `level: 5` is provisional beginner targeting, not a per-word JLPT guarantee.

`good` is green/Good; `kana` is yellow/Hard for the written-answer exercise.
`hard_variants` maps card IDs to yellow accepted written/kana alternatives with a reason,
replacement phrase and pronunciation. Yellow usable variants are not re-asked just for being yellow.
Wrong answers or giving up are Again. Distractors must not be any listed acceptable counter.

Variants are contextual: つ for fruit and coffee orders can be green.
着 for shirts, 名 for customers and 度 for these repeated-action prompts are green.
Formal register alone is not a defect. Some cards deliberately target the specific everyday counter
and grade an authored generic/formal variant yellow, with a contextual explanation.
Yellow can be a target-counter learning score even when a general answer is natural;
the explanation must not imply that such Japanese is defective.
Do not automatically demote every general counter or automatically allow つ for every object.

Accepted forms can change the entire counting phrase: いくつ replaces 何本/何個;
何個 replaces いくつ. 十 with とお is valid in the apple-count context, not 十つ.
Revealed sentences must replace `phrase`, not insert such alternatives into `{}`.
Canonical `phrase` appears in the sentence completed with the group's counter.
Accept both numeric spellings without losing number identity or inventing morphology.
The base counter reading need not equal its surface reading (本/ぼん/ぽん; 一人/ひとり).

Reverse questions display the counter (without the revealing title) and the referenced cards'
`noun` values, **not their sentences with numerals**. Exactly one noun/context must be compatible.
For 回, display the event (本を読むこと), not just 本.
Accepted alternatives at every tier matter when excluding false distractors.
These authored fixtures are bounded; do not derive arbitrary options from an incomplete compatibility list.

Show full translations only after checking an answer: "cups" or "sheets" would reveal the blank.
Randomize options in both directions; source-order answers in reverse fixtures are not a display order.

## Source use and editorial limitations

The YAML maps references to the corresponding counter groups. The Tofugu guides for
本, 匹, 枚, 人, 個, 冊, 台, 回 and つ were inspected for usage categories and readings.
Wiktionary's 杯 entry is a reading/use cross-check, not a source of copied example sentences.
References support counter categories, not the exact naturalness or every alternative of each invented sentence.
No dictionary tables, example corpus or third-party article text is imported.
The dedicated 小学館『数え方の辞典』 remains a possible further check, not a paid source already consulted.

The following still require native/editor evidence before the dataset is used for automatic grading:

- Alternative counters beyond those authored here, including generic counts and fish/animal registers.
- Whether each yellow answer is merely less targeted or equally idiomatic in the particular sentence.
- The 五、六本 reading and range normalization.
- Vocabulary/grammar progression and presentation of unfamiliar nouns.
- Exact handling of full-phrase alternatives and all readings in the Android parser/grader.

Retained pilot card IDs preserve identity. The old pilot stays available as a historical design fixture;
the ずつ card stays there at its provisional N4 level.
Run `python tools/validate_counter_draft.py` for reproducible count, ID, phrase, tier and option checks.
It checks reverse compatibility against the authored variants, not every possible Japanese usage.
The live validator does not yet support this draft schema. Structural checks of the draft are separate
from language review and do not establish native idiomaticity.

## Historical #41 independent review and reconciliation

Two independent subagents covered all 120 forward cards and 20 reverse fixtures:
one for Japanese correctness and grading; one for scoped coverage, comprehension and quiz pedagogy.
Both reviewed the same uncommitted expansion over `7ede429` without seeing the other's findings.
Coverage of the ten agreed counters and object variety was judged sufficient.

- **Resolved:** added selective vocabulary readings/glosses; corrected nine noun prompts;
  accepted 通 for postcard correspondence, 個 for televisions and つ for beds.
- **Resolved conservatively:** removed 皿 as a green answer for the empty-plate washing card.
  [The dedicated plate entry](https://www.sanabo.com/kazoekata/ct_sa/sa/sara/)
  lists 枚/個/客, whereas Tofugu's general counter list allows 皿 for empty plates.
  This disagreement is not treated as proof that 一皿 is universally wrong.
- **Resolved:** removed the unsupported "three sheets" interpretation of 紙を三つください
  from approved variants; clarified yellow target-counter scoring versus naturalness.
- **Partially resolved:** strengthened contextual distractors for albums/photos, repeated readings,
  repeated viewings and button presses. Some introductions intentionally keep easier options.
  The ambiguous "two films" prompt does not use 回 as a false distractor.
- **Unresolved before automatic grading:** completeness of general alternatives and contextual tiers;
  absence from authored variants is not linguistic proof of incorrectness.

Sources used to reconcile postcards and tableware were inspected as references only;
their dictionary explanations were not copied. Further native/editor review remains useful.

## Numbers & counters expansion (#71)

[App work item and independent plan review](https://github.com/stop-cran/kanji-cards-android/issues/71).
The section owns expression/unit selection and reading. Grammar retains sentence constructions,
including time-point に and frequency. The companion is
[Numbers, counters, time and dates](../articles/numbers-and-counters.md).

The live totals are **124 suffix prompts, 20 reverse questions, 123 complete expressions**.
Reading practice also uses the suffix prompts' canonical phrases, except already-kana いくつ:
**246 reading items**. These are modes over shared identities, not 513 unrelated content items.
All/Everyday/Time filters do not create new stacks or multiply the shared daily allowance.

| V2 file | Expressions | Coverage |
| --- | --- | --- |
| `age` | 9 | 1/4/8/10/20/21/28/30 and 何歳; 歳/才 |
| `floor` | 8 | 1/2/3/4/6/8/10 and 何階, using Japanese floor labels |
| `clock` | 16 | All 12 hours, 半, 9:15, 12:45 and 何時 |
| `minutes` | 15 | 1–11, 15/20/30 and 何分 |
| `months` | 13 | All 12 calendar months and 何月 |
| `dates` | 20 | 1–10, 11/14/17/19/20/24/29/30/31 and 何日 |
| `hours` | 8 | 1/2/3/4/8/10 hours, 1.5 hours and 何時間 |
| `days` | 14 | 1–10/14/20/24 days and 何日, with duration context |
| `weeks` | 6 | 1/2/3/4/8 weeks and 何週間 |
| `monthspan` | 7 | 1/2/3/6/8/10 months and 何か月; spelling variants |
| `years` | 6 | 1/2/3/4/10 years and 何年 |
| `native` | 1 | Primary 十 / とお, not 十つ |

The four added v1 prompts supply 八本, 十本, 十杯 and 八回 without rewriting old cards.
The 123 expressions split into 18 Everyday and 105 Time & dates items. Group membership is authored.

### Version-2 transport and future authoring

Create **new files** under `counters/`, in `manifest.files`, rather than changing the schema of a
published v1 family. Older apps skip v2 files and retain the original practice. New modes require
a compatible APK; content sync alone cannot install these UI/parser capabilities.

Required root fields: integer `schemaVersion: 2`, filename-matching `id`, `counter`, kana `reading`,
nonblank `title`, integer `level` 1–5, `group` (`everyday` or `time`), existing
`article: articles/<slug>.md`, and `expressions`. Optional `sources` is an array of HTTPS URLs.
Do not mix nonempty legacy `cards`/`reverse` arrays into v2; unknown v2 fields are rejected.

Each of 1–256 expressions has exactly `id`, `cue`, `written`, `writtenAnswers`, `reading`,
`readingAnswers`, `explanation`. IDs follow `[a-z]+-[a-z]+-[0-9]+` and are globally unique across
forward, reverse and expression records. Keep IDs stable when improving text.
The cue must disambiguate the quantity and sense without showing its answer.
Canonical `written` and `reading` must appear in their accepted lists.
Text fields are nonblank and at most 1,000 characters; written alternatives are 1–16 nonblank strings,
readings 1–8 kana strings, each at most 80 characters, with no normalized duplicates.

- Writing requires the **entire** expression. Explicitly list kanji/Arabic and intended unit/spelling
  alternatives, including mixed numerical spellings for compound times. Never accept a bare suffix.
- Reading alternatives pronounce **only the displayed canonical expression**. Do not derive them from
  the legacy `kana` list, which may also describe alternate counters. Do not include かん unless the
  displayed expression includes 間; do not accept よじさんじゅっぷん as a reading of 四時半.
- New modes use NFKC and whitespace removal, plus katakana-to-hiragana folding for reading only.
  They do **not** use the legacy numeral arithmetic: malformed 十十 must not match 二十.
  Small っ/ゃ/ゅ/ょ and long vowels remain significant. Correct readings earn Good, not legacy Hard.
- Already-kana canonical forms do not enter reading drills. Explain おいくつ in prose instead of
  inventing a kanji spelling or a copy-the-answer question.
- V1 may add `article`, `group` (defaults Everyday), and per-card `readingAnswers`.
  The optional list uses the same kana/canonical/duplicate rules; omission keeps only `reading`.
  Never change old IDs or suffix-mode tiers merely to add the reading mode.
- Check references directly and author original cues/explanations. Search summaries are not evidence:
  they can invent lesson URLs or misclassify legitimate readings. Keep a source beside each family,
  explain spelling/pronunciation alternatives, and request independent language/coverage review.
- Run `python -B -m unittest discover -s tools -p test_counters.py`, `python -B tools/validate.py`,
  `python -B tools/build_manifest.py` and the content-budget check. Stage new files before the app's
  full tracked-archive test; force that test to rerun when only the sibling content repo changed.
  Structural acceptance does not prove natural Japanese.

### #71 independent language review and reconciliation

One independent read-only reviewer checked all 123 expressions, four added suffix prompts,
124 canonical-reading sets and the entire article, preserving the original 120/20 records.
The review covered correctness, required coverage and cue comprehension, with direct reference checks.
It was an automated editorial review, not physical-device acceptance or a native-speaker certificate.

Resolved findings: added documented カ月/ヵ月/ケ月 spellings; accepted the documented alternate
date, seven-o'clock and July readings; accepted 分間 for minute durations; explicitly constrained
month-span prompts to か月 without 間 and week prompts to 週間. Alternate written expressions
still do not leak their pronunciations into the canonical reading drill.

A bounded follow-up could not verify the exact uncontracted age/week readings はちさい,
にじゅうはちさい and はちしゅうかん. The general counter pattern offers indirect support,
but this new beginner set conservatively teaches the directly supported contracted defaults instead.
This is an authoring-scope decision, not proof that every unlisted pronunciation is impossible.
二十歳's regular readings and 八か月's はちかげつ alternative have direct reference support.
