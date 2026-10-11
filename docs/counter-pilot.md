# Counters: 20-card pilot

Draft for [app issue #41](https://github.com/stop-cran/kanji-cards-android/issues/41).
The author-written examples and provisional grading data are in [counter-pilot.yaml](counter-pilot.yaml).
They are not in `manifest.json`, are not consumed by the app, and do not change the existing content schema.
Do not bulk-generate or publish until the remaining editorial questions below are resolved.

## Numerals and prompts

The pilot prefers kanji numerals: 三匹, 一人, 五、六本.
This is a learning/display preference, not a claim that Arabic numerals are unnatural in Japanese.
Kanji numerals are also not the same as native Japanese number *readings*: 三匹 uses さん,
while 三つ uses みっつ.
Later cards can use Arabic numerals where appropriate; typed answers accept either spelling.

`text` has exactly one `{}` marking the counter-only blank.
`phrase` is the corresponding complete counting expression, including its numeral or question word.
`reading` gives that phrase's pronunciation, not the whole sentence.
Most examples are sentences; two are bare-noun prompts. Noun and quantity can be separated in a sentence,
but the numeral and counter normally remain together. `floated-quantity` does not mean splitting 三 from 匹.

The 20 forward examples cover 本 (5), 匹 (4), 枚 (4), 人 (3), 個 (4).
There are five additional reverse-question fixtures, derived from the same noun relations, not five new forward cards.
Levels are provisional community study labels. The ずつ card is an N4 stretch, not forced into N5.
数ヶ月, 十数人, larger-number comparisons and further counter categories belong to the next, level-reviewed batch.

## Grading proposal

- `good`: preferred written answers and genuinely equally natural written alternatives.
- `hard`: usable but less-targeted answers, each with a replacement phrase, its reading and a learner-facing reason.
  Show yellow and grade Hard, above Again; do not re-ask solely because an acceptable alternative was used.
- `kana`: explicitly authored phrase readings, graded Hard for this written-answer task.
- An incorrect count, unsuitable counter, malformed phrase or giving up is Again.

Normalize NFKC and whitespace, and equate Arabic/kanji *numeric expressions* without erasing number identity.
三本 and 3本 match, but 二本 must not match 三本.
Do not remove or reinterpret 何, 数, ranges or suffixes by a blanket digit-stripping rule.
No invented morphology: all accepted phrase forms/readings are authored.

Accepting つ is contextual, not a global rule. A normal alternative such as 三つ for apples stays green.
The question alternative to 何本 is いくつ, never 何つ.
When an alternative changes the construction, replace the entire `phrase` in the revealed sentence;
do not insert いくつ after 何.
Similarly 十 with the native reading とお is not 十つ.

Register is contextual too: 着 is a normal clothing counter and is green for shirts.
A suitable formal answer is not inherently wrong. Yellow means this exercise targets a different everyday usage,
not that the accepted answer is ungrammatical.
Do not use a yellow answer as a false distractor.

Reverse questions show the counter and four nouns. Exactly one offered noun must accept that counter.
A noun need not have only one possible counter in all Japanese: eggs can accept both 個 and つ.
All compatibility tiers count when excluding wrong noun options; do not pretend general/formal alternatives are incompatible.
The pilot's relation lists are scoped drafts, not exhaustive dictionaries.

## Sources inspected

These links are references for checking facts, not permission to copy their explanations, examples or dictionary tables.
All sentences here are independently authored; no dictionary dataset has been imported.

| YAML source ID | Reference | What was checked |
| --- | --- | --- |
| `hon` | [Tofugu: 本](https://www.tofugu.com/japanese/japanese-counter-hon/) | Long objects, umbrellas, bottles, standing trees and numeral readings |
| `hiki` | [Tofugu: 匹](https://www.tofugu.com/japanese/japanese-counter-hiki/) | Living fish, small animals, professional dog contexts, numeral readings |
| `mai` | [Tofugu: 枚](https://www.tofugu.com/japanese/japanese-counter-mai/) | Flat objects and numeral readings |
| `ko` | [Tofugu: 個](https://www.tofugu.com/japanese/japanese-counter-ko/) | General object counting, overlap with more specific counters and numeral readings |
| `tsu` | [Tofugu: つ](https://www.tofugu.com/japanese/japanese-counter-tsu/) | General counts, ticket orders, readings and いくつ |
| `readings` | [Wiktionary: Japanese counters](https://en.wiktionary.org/wiki/Appendix:Japanese_counters) | Cross-check of common counters and 人 readings |

[小学館『数え方の辞典』 on JapanKnowledge](https://japanknowledge.com/contents/kazoekata/)
is a dedicated dictionary: its public description reports about 4,600 counted nouns and 600 counters/counting expressions.
It explains that form and context affect counter choice. Its paid entries have **not** been checked here.
JMdict is a potential additional reference, not a verified source for every pilot claim; confirm entry evidence
and licensing before importing any data. Tofugu's usefulness tiers are guidance, not an official JLPT syllabus.

## Remaining editorial checks

- Confirm per-sentence general-counter alternatives, rather than extending a broad dictionary definition automatically.
- Confirm 頭 for household cats and 名 for the exact person contexts.
- Check the 五、六本 range reading, clothing alternatives, and naturalness of the quantity comparison.
- Check vocabulary and grammar levels against the project's community lists; ordinary vocabulary can still need a gloss.
- Expand compatibility lists before deriving unrestricted reverse distractors.
- Specify forward distractor lists and shared Python/Kotlin parser/grading fixtures before app implementation.

The earlier agent-only review was not dictionary verification. In particular, it was too categorical about 尾 requiring
large fish, automatically rejecting つ for some objects, and treating 着 as merely formal.
Those rules are not adopted here. Fish have a living-aquarium context; unverified restrictions are not presented as facts.
