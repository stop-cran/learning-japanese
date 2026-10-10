# Learning Japanese

English-language notes on Japanese grammar, vocabulary, and usage.

This repository starts as a collection of standalone articles prompted by specific questions. It is not yet a course or a systematic reference: topics can be connected and organized more formally as the collection grows.

## Articles

| Area | Article | Main question |
| --- | --- | --- |
| Grammar | [Koto, wake, and Japanese noun-based grammar](articles/koto-wake-and-formal-nouns.md) | How do こと and わけ differ, which common formal nouns and noun-based expressions are useful to know, and where do の/ん and ほど fit? |
| Grammar | [Japanese verb extensions: direction and aspect](articles/verb-extensions-direction-and-aspect.md) | How do ～ていく, ～てくる, ～ておく, ～込む, and related constructions express direction, continuation, and completion? |
| Vocabulary | [Strange, suspicious, and rare: ayashii and related words](articles/ayashii-and-related-words.md) | How do 怪しい, 妖しい, 疑わしい, いかがわしい, 変な, and 珍しい differ? |
| Vocabulary | [Japanese occupation and role endings](articles/occupation-and-role-endings.md) | What do 者, 家, 師, 士, 手, 員, and 屋 contribute, and how do they relate to prestige and new word formation? |

## Confusable vocabulary

The [candidate inventory](docs/confusable-words.md) collects overlapping meanings, misleading English glosses,
similar forms, false friends, and other easy-to-conflate cases for future comparison articles. It is a working list with
provisional notation and links to existing material, not yet a complete usage reference or new app metadata.

## Kanji cards and words

Kanji cards, word articles and stroke data feed the [Kanji Cards Android app](https://github.com/stop-cran/kanji-cards-android). The
format is described in [docs/content-format.md](docs/content-format.md); data sources are in [NOTICE.md](NOTICE.md).

- `kanji/` – one card per kanji (620): meaning, radical, readings, common words, and origin notes or explicitly labelled modern-shape mnemonics.
  The deck covers all 79 N5, 166 N4 and 367 N3 kanji in the selected [kanjiapi.dev](https://kanjiapi.dev) community sets.
  It also includes 分 as a documented N5 exception, one original N2 card, and six article-subject additions:
  80 N5, 166 N4, 367 N3, two N2 and five N1. The `starter` tag identifies the original 118-card cohort, not the later expansions.
- `words/` – one article per written word form (1,533): native words, Sino-Japanese compounds and loanwords, including kana-only spellings.
  Articles explain meaning, spelling or formation, synonyms, antonyms and usage distinctions.
  The selected community vocabulary list's 684 N5 and 640 additional N4 rows are covered by 1,308 articles:
  924 new articles and 384 reused ones. Multiple source readings can share an article.
- `strokes/` – generated stroke data. Validate with `python tools/validate.py`.

The revised JLPT does not publish exhaustive kanji or vocabulary syllabi. Level coverage here means the exact named community set,
not a guarantee about every examination question or a complete beginner curriculum.
See the [level-source policy](docs/jlpt-levels.md) and the [N4](docs/n4-source-snapshot.json) and
[N3](docs/n3-source-snapshot.json) kanji source snapshots. The
[N5/N4 vocabulary snapshot](docs/n5-n4-vocabulary-snapshot.json) and
[source-row index](docs/n5-n4-vocabulary-sources.tsv) preserve the pinned list, spelling normalizations, corrected dictionary identities
and sense qualifications.
The [article-subject snapshot](docs/article-subjects-source-snapshot.json) records the six additional kanji,
17 new word cards, and reuse of 訳 for わけ, including dictionary-reading caveats and the 妖 level exception.

Source-covered word articles carry their own `jlpt` metadata: 672 N5, 636 N4, two N3, three N2 and two N1 articles, independently of the kanji they contain.
This article-level label does not assign every subsidiary sense or reading to that level. The remaining 218 articles have no
sourced word-level label. In particular, the pinned list's N1 labels for くらい and だけ are not recommendations to postpone these basic particles.
Vocabulary-aware app versions use explicit levels first and retain kanji-based inference only when the
field is absent; older versions ignore word-level metadata. N4 study includes N5.
Known ambiguous word pairs are marked with [`quiz_exclusions`](docs/content-format.md#word-article);
these require an exclusion-aware app version and do not imply that every possible ambiguity has been identified.

## Approach

- Keep each article independently readable, with a short explanation of the central distinction.
- Write explanations in English; retain Japanese spellings and examples, with English translations.
- Distinguish useful learning shortcuts from strict grammatical or semantic rules.
- Note differences in register, context, and classification where they matter.
- Link to references for further study. Some source material is in Japanese even though the articles are in English.

The notes focus on practical understanding rather than exhaustive coverage. Examples illustrate particular uses; their translations are not intended as universal replacements for the Japanese expressions.

For contributors and reviewers, see the [writing and review guidance](.github/copilot-instructions.md) and [REVIEW.md](REVIEW.md).
