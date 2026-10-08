# JLPT study levels and sources

The `jlpt` field is a community study label, not an official assignment of an individual kanji to an examination.
The [official JLPT FAQ](https://www.jlpt.jp/e/faq/index.html#anchor28) explains why vocabulary, kanji, and grammar lists
have not been published for the test revised in 2010. Official competence descriptions and sample questions are not exhaustive lists.

## Baseline

Use the community sets exposed by [kanjiapi.dev](https://kanjiapi.dev/):

- [N5](https://kanjiapi.dev/v1/kanji/jlpt-5): 79 characters in the snapshot inspected on 2026-10-08.
- [N4](https://kanjiapi.dev/v1/kanji/jlpt-4): 166 characters in that snapshot, excluding the N5 set.

Record the retrieved set and date when expanding coverage. Compare characters, not just counts. Existing cards for a level count
toward its coverage; do not create duplicate cards. "All N4" means all characters in this named source set, not an official guarantee
about every character that could appear in the exam. Earlier-level knowledge is still needed for higher-level study.

An API `null`, a missing entry, or a network failure does not authorize an inferred level. Check another identified learning source
and document any exception below. If evidence still conflicts, leave the decision unresolved rather than silently choosing a number.
Historical KANJIDIC levels are not modern N-numbers: [old Level 4 corresponds to N5, and old Level 3 to N4](https://www.jlpt.jp/e/faq/index.html#anchor13).

## Documented exceptions

| Kanji | Repository label | Evidence and reason |
| --- | --- | --- |
| 分 | N5 | kanjiapi.dev returned `jlpt: null` on 2026-10-08. [Kanshudo](https://www.kanshudo.com/kanji/%E5%88%86) explicitly labels 分 N5; [JLPT Sensei's N5 list](https://jlptsensei.com/jlpt-n5-kanji-list/) includes it. These are community sources, not an official ruling. |

With this exception, the repository's N5 study set has 80 characters. Keep the card's `jlpt`, its `jlpt-nX` tag, and its facts line
in agreement. Reassess an exception if its cited evidence changes; do not overwrite it merely because the baseline still has no value.
