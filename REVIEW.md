# Review process

How the kanji and word content is reviewed. The reviewers are Copilot custom agents stored in [.github/agents](.github/agents); the report format and evidence rules are in [.github/copilot-instructions.md](.github/copilot-instructions.md).

## Reviewers

| Agent | Looks at | Typical question |
| --- | --- | --- |
| [kanji-accuracy-reviewer](.github/agents/kanji-accuracy-reviewer.agent.md) | One batch of cards and their words | Are readings, stroke counts, radicals, word types, origins, look-alikes and examples true? |
| [kanji-comprehension-reviewer](.github/agents/kanji-comprehension-reviewer.agent.md) | One batch of cards and their words | Can an N5 learner on a phone follow it? Is jargon explained, are rare items marked, is the quiz title unambiguous? |
| [content-consistency-reviewer](.github/agents/content-consistency-reviewer.agent.md) | The whole repository | Do schema, links, titles, distractors, coverage, strokes and the manifest agree? |

Reviewers are read-only. They report; the maintainer decides what to apply.

## Running a review

1. Run `python tools/validate.py` (on Windows set `PYTHONIOENCODING=utf-8`).
2. Start one accuracy and one comprehension reviewer per batch of about 15 kanji, and one consistency reviewer for everything. Point each at its scope, for example "kanji cards for 右左高安新… plus the words whose `kanji:` contains any of them".
3. Collect findings; treat them as hypotheses and check disputed claims against a dictionary (kanjiapi.dev, Jisho/JMdict, Wiktionary, KanjiVG).
4. Apply fixes, run `validate.py`, then `python tools/build_manifest.py` and commit the manifest with the change.

## Review of the N5 set (106 kanji, 159 words)

Done once after the content was drafted: 6 accuracy, 3 comprehension and 1 consistency review.

What it found and what was fixed:

- Wrong or misleading facts: 年上 used for "elderly", 校正 read きょうせい, 話 analysed as containing 舌, 店's phonetic 占 given a テン reading, 銀行 explained with 商行為, 北海道 called "one of the few" 道 prefectures, 九 vs 力 stroke counts, 駅 called a bound noun.
- Reading-table errors: words in the wrong on/kun row, special readings listed as ordinary on readings (今年, 人間, 千葉).
- Comprehension: unexplained jargon (jukujikun, ateji, okurigana, "KANJIDIC"), unmarked rare readings, vague or untrue look-alike notes, duplicate prose.
- Consistency: stale manifest; `distractors` missing on one card.

Known gaps, deliberately left for later:

- Twelve kanji used in words have no card yet: 側 海 達 供 旅 京 自 動 物 銀 短 事. 物 and 事 are the strongest candidates for a next batch.
- Some word `kanji:` lists omit characters without cards (地, 曜, 心).
- Many words link to a kanji card that does not list the word under Common words (backlinks are not required for every prose link).
- Words that mix on and kun readings (半年, 駅前, 毎月) are typed `kango`; the schema has no on+kun type.
- Radicals were checked against the Kangxi table, not fetched per kanji from KANJIDIC2/Unihan. Word readings were checked from memory and spot lookups, not every entry in JMdict.
- `jlpt: 5` follows an unofficial list. kanjiapi's old JLPT data puts several of these kanji (安, 新, 古, 多, 少, 黒, 赤, 青, 駅, 道, 店, 会, 社, 花, 魚, 犬) at N4.
