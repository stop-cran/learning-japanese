# JLPT study levels and sources

The `jlpt` field is a community study label, not an official assignment of an individual kanji, word or grammar item to an examination.
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
| 妖 | N1 | kanjiapi.dev returned `jlpt: null` on 2026-10-10. [Kanshudo's 妖 details](https://www.kanshudo.com/kanji/%E5%A6%96) explicitly display **JLPT: N1**. This is the kanji's level label, not an inference from its usefulness rating or school grade. |

With the 分 exception, the repository's N5 study set has 80 characters. Keep the card's `jlpt`, its `jlpt-nX` tag, and its facts line
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

### Selected article-subject additions

The [2026-10-10 source record](article-subjects-source-snapshot.json) also inspects `n1.csv`, `n2.csv`, and `n3.csv`
at the same pinned revision for selected article subjects, without claiming complete coverage of those levels.
It records the exact source rows, dictionary identities, and spelling normalizations:

- **N2:** 怪しい, 作者, 武士.
- **N3:** 作家, ころ (source spelling 頃).
- **N1:** くらい (source reading ぐらい), だけ (source spelling 丈).
- **Reused N4 card:** 訳, also teaching the spelling わけ; no duplicate kana card.

The N3 位/くらい row names the noun entry for rank, even though its gloss also includes "about".
The particle card instead uses the unambiguous N1 ぐらい row for JMdict 1154340; it does not silently borrow
the rank noun's level. Similarly, N1 間々/まま means "occasionally", not the unchanged-state noun まま.
These list labels do not imply that useful basic grammar such as だけ should be postponed until N1.

No vocabulary level was established for 妖しい, 奇しい, 疑わしい, いかがわしい, unchanged-state まま,
かぎり, ばかり, 研究者, 研究員, or 政治家 in the inspected sources. Their cards omit `jlpt`.
Do not copy 怪しい's level to its separately recorded or rare alternative spellings merely because they share a reading.

### App interpretation

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

## Grammar baseline

Use [Bunpro's grammar library](https://bunpro.jp/grammar_points) as the primary level reference, with
[JLPT Sensei's grammar lists](https://jlptsensei.com/jlpt-n5-grammar-list/) for secondary comparisons. These are study curricula, not official
examination specifications. The [grammar classification record](grammar-jlpt-sources.json) preserves the inspected index
URLs, retrieval dates, source hashes, selected entries, secondary comparisons and the decision for the original 721 exercises.
The [N5 foundations ledger](grammar-n5-foundations-sources.json) records the subsequent 125 exercises and their complete-task mappings.
The [pointing/questions ledger](grammar-n5-pointing-sources.json) adds 54 N5 tasks. Its six person/reason/method
questions include the secondary-supported どうやって contrast; optional accepted wording is not a separate level prerequisite.
The [noun-description ledger](grammar-n5-descriptions-sources.json) adds 32 N5 tasks. It distinguishes new past/ている
modifiers from reused nonpast attachment, explicitly scoped の formation from harder の／こと selection, and
bounded subject が／の recognition from unrestricted substitution. The N4 word-card level of 運転 does not raise
an exercise practising these N5 grammatical roles.
The [wants/plans ledger](grammar-n5-wants-sources.json) adds 38 N5 tasks. All four choice/request items
need the secondary N5 noun + をください pattern in their visible contrast; はどうですか is supporting
article material only. Optional N4 てほしい／がほしい and advanced intention/completion-belief reading
are not required choices, and the six reused N5 intention objects retain their original levels.
The [reasons/contrasts ledger](grammar-n5-reasons-sources.json) adds 34 N5 tasks across five assigned primary
anchors, with subject が as an additional supporting entry. Attached nominal だ／です + が follows the
explicit N5 connective lesson, not the separate N4 standalone だが／ですが entry. The preface tasks do not
require N4 んだけど／んですが; sentence-level conjunctions remain article support. Existing N4 のに／ので
comparisons keep their complete-task classifications and unchanged objects.
The [comparisons/change ledger](grammar-n5-comparisons-sources.json) adds 42 N5 tasks. The exact combined
より／ほう and set-plus-一番 patterns follow their N5 entries, not separate standalone N4 entries.
Ordinary past controls and the substantive degree/excess choices are included in the mapping; the latter also
uses the exact secondary N5 とても entry. 結構 supplies shared optional degree wording, while たくさん remains
lexical/context support. Five already-N5 quantity/limit objects are grouped without relabeling the neighboring
N3 tasks or the existing N4 ほう／ほか and N3 なる／まま contrasts.

**Classify grammar, not vocabulary or kanji.** Use the construction and substantive contrast needed for the complete
visible task. Keep natural examples; unfamiliar words should be supported by readings, glosses and translations rather
than by inflating the grammar level or simplifying away useful language. Vocabulary-help coverage is a separate concern:
the classification pass does not fill the existing annotation gaps.

Assign one integer `jlpt` per exercise, not one blanket level per article or set. An explicit contrast can be harder than
its correct answer alone: a はず/べき task requires the N3 contrast even when はず is the answer. Conversely, supplied
background grammar, glossed interpretation labels, malformed distractors and advanced **optional** accepted answers do
not automatically raise the level. A construction required by the base fixed choices is not merely an optional typed
alternative. Simple noun-linking or object-marker drills can remain N5 inside an advanced lesson.

When applicable entries disagree, retain Bunpro's placement and document the secondary placement, rather than averaging
them or silently choosing the harder number. Examples include unchanged-state まま (Bunpro N3; JLPT Sensei N4),
ことになっている (N2; N3), 上に and 際に (N2; N3), purpose ように (N4; N3), and とき (N4; N5).
Match the actual sense: past-experience たことがある is not occasional nonpast ことがある, and concessive のに is not
the resource/purpose construction with the same spelling.

If the exact primary sense is not established, use a documented exact secondary entry where available; otherwise leave
the exercise unclassified. This pass uses JLPT Sensei's N3 **maximum-extent だけ** and N2 **approximate-quantity ばかり**
instead of borrowing Bunpro's levels for exclusive だけ, だけは or concentration ばかり. Optional versions elsewhere
do not raise those exercises. Bunpro itself has overlapping N4/N3 だけでなく entries: the inspected N4 lesson explicitly
supports the simple noun-plus-も tasks here, so they use N4.

Some decisions are explicitly **semantic-family mappings**, not separate source labels for every ending: extended つもり
self-view/completion-belief predicates use the N2 つもりで family, while ordinary past inflection of a future intention
remains N5; established ことにしている practice uses the N3 ことにする family. These editorial estimates can be revised
without changing exercise identities or resetting progress. Prior linguistic-review verdicts do not certify this new
metadata pass; the source record identifies it as author classification, not independent review.

### Current classified practice

The original 2026-10-22 pass classified 721 exercises in 40 sets. With 125 N5 foundations, 54 pointing/questions,
32 noun-description, 38 wants/plans, 34 reasons/contrasts and 42 comparisons/change additions,
current practice has **1046 exercises in 51 sets**:
**495 N5, 210 N4, 235 N3, 102 N2 and four N1**.
The original 19 pilot labels are unchanged. No exercise remains unclassified in this snapshot, but omission remains the
correct representation for future unresolved cases. These counts are coverage of our existing exercises, not coverage
of every grammar item in any level's curriculum.

| Linked article | N5 | N4 | N3 | N2 | N1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Verb foundations](../articles/japanese-verb-foundations.md) | 41 | 0 | 0 | 0 | 0 |
| [Adjective foundations](../articles/japanese-adjective-foundations.md) | 22 | 0 | 0 | 0 | 0 |
| [Actions, states and time](../articles/japanese-actions-states-and-time.md) | 24 | 0 | 0 | 0 | 0 |
| [Requests, permission and rules](../articles/japanese-requests-permission-and-rules.md) | 22 | 0 | 0 | 0 | 0 |
| [Pointing and asking questions](../articles/pointing-and-asking-questions.md) | 54 | 0 | 0 | 0 | 0 |
| [Noun descriptions and activities](../articles/noun-descriptions-and-activities.md) | 32 | 0 | 0 | 0 | 0 |
| [Wants, plans, invitations and offers](../articles/wants-plans-and-invitations.md) | 38 | 0 | 0 | 0 | 0 |
| [Reasons, contrasts and prefaces](../articles/reasons-and-contrasts.md) | 34 | 0 | 0 | 0 | 0 |
| [Comparisons, changes and degree](../articles/comparisons-change-and-degree.md) | 42 | 0 | 0 | 0 | 0 |
| [Nouns and basic particles](../articles/japanese-nouns-and-basic-particles.md) | 73 | 3 | 0 | 0 | 0 |
| [Topic, contrast and inclusion](../articles/wa-ga-mo-topic-and-inclusion.md) | 36 | 0 | 0 | 0 | 0 |
| [Listing and examples](../articles/japanese-listing-and-examples.md) | 23 | 17 | 0 | 0 | 0 |
| [Restriction and unexpected inclusion](../articles/only-and-unexpected-inclusion.md) | 15 | 25 | 10 | 0 | 0 |
| [Compound relations](../articles/about-targets-and-perspectives.md) | 8 | 2 | 38 | 0 | 0 |
| [Conditionals](../articles/japanese-conditionals.md) | 2 | 58 | 0 | 0 | 0 |
| [のに contrasts](../articles/noni-and-concessive-contrasts.md) | 0 | 17 | 9 | 0 | 0 |
| [こと, わけ and noun-based grammar](../articles/koto-wake-and-formal-nouns.md) | 29 | 88 | 178 | 102 | 4 |

The four N1 tasks have formal 折(おり)に in their actual fixed-choice contrast; optional 折 answers elsewhere do not make
those tasks N1. Bunpro's 折には entry explicitly includes 折に without は.

Article browsing derives matching levels from linked exercises; no article front matter or blanket article label is
needed. The table does not grade every passage in a mixed-level article. Articles without linked exercises, such as
the verb-extensions overview, receive no exercise-derived level from this pass. The app's new-material scope remains
cumulative, while article/exercise browsing uses exact matching levels; classification does not change SRS identities.
