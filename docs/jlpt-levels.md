# JLPT study levels and sources

The `jlpt` field is a community study label, not an official assignment of an individual kanji or word to an examination.
The [official JLPT FAQ](https://www.jlpt.jp/e/faq/index.html#anchor28) explains why vocabulary, kanji, and grammar lists
have not been published for the test revised in 2010. Official competence descriptions and sample questions are not exhaustive lists.

## Baseline

For **kanji**, use the community sets exposed by [kanjiapi.dev](https://kanjiapi.dev/):

- [N5](https://kanjiapi.dev/v1/kanji/jlpt-5): 79 characters in the snapshot inspected on 2026-10-08.
- [N4](https://kanjiapi.dev/v1/kanji/jlpt-4): 166 characters in that snapshot, excluding the N5 set.
- [N3](https://kanjiapi.dev/v1/kanji/jlpt-3): 367 characters in the snapshot inspected on 2026-10-09.

Record the retrieved set and date when expanding coverage. Compare characters, not just counts. Existing cards for a level count
toward its coverage; do not create duplicate cards. Complete coverage of a level means all characters in its named source set, not an official guarantee
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

## Vocabulary baseline

Vocabulary levels are separate from kanji levels. For N5, N4 and N3, use Stephen Kraus's
[Yomitan JLPT vocabulary data](https://github.com/stephenmk/yomitan-jlpt-vocab/tree/b062d4e38c4bdd0950ae1d4ec55f04b176182e03/original_data),
pinned to commit `b062d4e38c4bdd0950ae1d4ec55f04b176182e03`. It derives from Jonathan Waller's community lists and adds JMdict entry IDs.
The selected CSVs contain **684 N5 rows and 640 additional N4 rows**: 1,324 source rows for cumulative N4 study.
The [source snapshot](n5-n4-vocabulary-snapshot.json) records the exact downloads and transformations;
the [coverage index](n5-n4-vocabulary-sources.tsv) maps individual source rows to articles and selected dictionary senses.
The same revision's N3 CSV adds **1,730 rows**, for 3,054 source rows across the three levels.
Its separate [snapshot](n3-vocabulary-snapshot.json) and [coverage index](n3-vocabulary-sources.tsv) cover 1,698 articles,
including 208 reused articles. The N5/N4 indexes remain unchanged.

A source row, a dictionary entry, and an article are not the same unit. For example, 明日/あした is listed at N5 and 明日/あす at N4;
one article can teach both readings. Conversely, shared dictionary IDs do not make every spelling or use interchangeable.
Normalize unusual source spellings only with lexical evidence, preserve stable existing article filenames, and retain the original
spelling, reading, level and entry ID in the index. A spelling alias counts as coverage only when the corresponding meaning and
reading are actually taught. Validate spelling-restricted senses against the spelling actually taught, not merely the stable filename:
the 登る article teaches source 昇る/のぼる rising and promotion separately from mountain climbing.
The index's mapping note identifies such teaching spellings; sharing a page does not remove their restrictions.
Do not infer vocabulary membership from a word's kanji, from dictionary inclusion, or from intuition.

Word articles may supply an explicit integer `jlpt: 1..5`. When an article covers several source rows, use the easiest sourced
level (the largest number), while retaining each row's level in the index. This is an **article-level study label**, not a claim
that every reading or sense on the page belongs to that level. Leave `jlpt` absent when no vocabulary source is established;
do not use a blank or `null`, and do not assign the remaining words a speculative level.

Vocabulary-aware app versions give this explicit field precedence, including for kana-only words and words containing kanji
from a harder study set. Older articles without it retain the app's kanji-based fallback; that fallback is not vocabulary provenance.
Word tags are free metadata and need not include a JLPT tag. N4 word study includes N5; N3 word study includes both.

### Corrections and limits

The source's English gloss and JMdict ID both need checking. A matching spelling and reading can still point to the wrong
homograph: the inspected source maps demonstrative これ, noun こと and conditional もし to unrelated interjection/particle entries.
The coverage index preserves those supplied IDs separately from the corrected lexical identities.
Source glosses are identification clues, not teaching prose to copy uncritically; articles qualify overbroad, dated or unnatural
descriptions against the actual usage and dictionary senses.

Some glosses cross homographs: コート lists both a coat and a sports court, while ビル's building and bill senses belong to separate
dictionary entries. The articles distinguish those identities rather than assigning all meanings to one ID.
For マッチ, the source's English "match" does not settle contest versus matchstick; retain the supplied contest/matching ID and
explain the matchstick homograph separately. The index records these additional dictionary senses without inventing extra source
rows or claiming that the ambiguous source proves a particular sense's level.

The N3 index records six supplied-ID corrections and 27 rows whose historical source intent remains uncertain.
Usually a verified Japanese spelling/reading is retained and an inconsistent English gloss is corrected.
For source どうか with the specific "copper coin" gloss, the teaching selection is 銅貨/どうか, JMdict 1454350,
while the original supplied entry 1632200 remains in provenance. This is an explicit editorial selection, not recovered compiler intent.
Blank glosses likewise require documented dictionary-backed teaching anchors, not an assumption that every dictionary sense is N3.
Mixed glosses such as glass/grass, code/cord/chord and rocket/locket require distinct lexical identities to be explained separately.

This is complete coverage of **named community lists**, not a complete curriculum or an official JLPT vocabulary syllabus.
The selected files include expressions, suffixes and counters but omit standalone entries for basic particles such as
は, が, を, に, へ, で, と, も and の. Their absence does not make those particles unimportant.
Other lists descended from Waller are not independent corroboration of an entry's level. Dictionary evidence establishes lexical
identity and applicable senses, not a modern examination assignment or the naturalness of every possible example sentence.
