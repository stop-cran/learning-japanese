# N5-oriented counter application set

[Issue #41](https://github.com/stop-cran/kanji-cards-android/issues/41) expansion of the
[20-card pilot](counter-pilot.md). [Draft data: counter-n5.yaml](counter-n5.yaml).

**Live content** now lives in `counters/<id>.json` (one file per counter, validated by
`tools/validate_counters.py` and listed in `manifest.json`); the YAML is the historical
draft and is no longer read by anything except `tools/validate_counter_draft.py`.
The agreed scope is ten counters with twelve forward examples each: **120 forward cards**,
plus **20 authored reverse questions** using those examples' nouns/contexts.
The choose and typed forward modes share cards, not duplicate content.
These are author-written editorial drafts, outside `manifest.json`; the current app cannot load them.
This is the full agreed initial set, not a claim that these are all counters tested at N5.
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
数ヶ月, 十数人, ordinal constructions and additional time/unit counters remain later-level extensions.
Numbers are kanji in the prompts, with Arabic equivalents accepted by the eventual numeric normalizer.
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

## Independent review and reconciliation

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
