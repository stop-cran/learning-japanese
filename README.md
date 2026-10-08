# Learning Japanese

English-language notes on Japanese grammar, vocabulary, and usage.

This repository starts as a collection of standalone articles prompted by specific questions. It is not yet a course or a systematic reference: topics can be connected and organized more formally as the collection grows.

## Articles

| Area | Article | Main question |
| --- | --- | --- |
| Grammar | [Koto, wake, and Japanese noun-based grammar](articles/koto-wake-and-formal-nouns.md) | How do こと and わけ differ, and how do の/ん, まま, かぎり, とき, and ころ fit into the family? |
| Grammar | [Japanese verb extensions: direction and aspect](articles/verb-extensions-direction-and-aspect.md) | How do ～ていく, ～てくる, ～ておく, ～込む, and related constructions express direction, continuation, and completion? |
| Vocabulary | [Strange, suspicious, and rare: ayashii and related words](articles/ayashii-and-related-words.md) | How do 怪しい, 妖しい, 疑わしい, いかがわしい, 変な, and 珍しい differ? |
| Vocabulary | [Japanese occupation and role endings](articles/occupation-and-role-endings.md) | What do 者, 家, 師, 士, 手, 員, and 屋 contribute, and how do they relate to prestige and new word formation? |

## Kanji cards and words

Kanji cards, word articles and stroke data feed the [Kanji Cards Android app](https://github.com/stop-cran/kanji-cards-android). The
format is described in [docs/content-format.md](docs/content-format.md); data sources are in [NOTICE.md](NOTICE.md).

- `kanji/` – one card per kanji (20 JLPT N5 samples so far): meaning, origin, key, readings, common words.
- `words/` – one article per word (20 so far, mostly kango): composition of the kanji, synonyms, antonyms, nuance.
- `strokes/` – generated stroke data. Validate with `python tools/validate.py`.

## Approach

- Keep each article independently readable, with a short explanation of the central distinction.
- Write explanations in English; retain Japanese spellings and examples, with English translations.
- Distinguish useful learning shortcuts from strict grammatical or semantic rules.
- Note differences in register, context, and classification where they matter.
- Link to references for further study. Some source material is in Japanese even though the articles are in English.

The notes focus on practical understanding rather than exhaustive coverage. Examples illustrate particular uses; their translations are not intended as universal replacements for the Japanese expressions.

For contributors and reviewers, see the [writing and review guidance](.github/copilot-instructions.md).
