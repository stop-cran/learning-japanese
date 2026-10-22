## Snapshot
`e80e0c452d4cd55c9bee9a3ab125b40fc85be953`: clean committed files only. The baseline is `eb9376ba6afa36d7e3803c788427797f15fa1750`. I can't run Git, so I couldn't confirm that the working-tree files match this commit, nor the 54-file diff. I reviewed the files as they are on disk and assumed they are that snapshot.

## Scope
Model: claude-opus-5.5 (family: claude). Single sequential reviewer; no files edited.

- **Read in full:** the 15 kanji cards (築 簡 籍 粉 粒 糸 紅 純 細 紹 絡 綿 総 緑 線) and the three new words (書籍, 粒, 総額).
- **Read for context:** the instruction files and `docs\content-format.md:18-109`.
- **Related edits:** I checked the link passages in all 15 word articles and the 小 distractor change, with surrounding context.
- **Evidence:** `batch-17.json` (metadata, reading rows, the relevant word evidence records, and gloss lines for the book synonyms), the titles, distractors and exclusions of comparison pages, and `docs\confusable-words.md`.
- **Not reviewed:** stroke JSON drawing paths, unchanged teaching text in the related articles, and all forbidden files.

## Verdicts
| Page | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| 築 簡 籍 粉 粒 紅 純 細 紹 絡 綿 総 緑 線 (each) | CLEAN | CLEAN | CLEAN |
| 糸 | NEEDS FIX | CLEAN | CLEAN |
| 書籍 / 粒 / 総額 (words) | CLEAN | CLEAN | CLEAN |

## Findings
**F1** (Minor; correctness)
- **Location:** `kanji\糸.md:41`
- **Claim and impact:** The note reads "毛糸 preserves いと after 毛's ケ reading". The repo writes on readings in katakana and kun readings in hiragana, so "ケ" tells learners that け is an on reading. It is actually 毛's kun reading; the on reading is モウ.
- **Remedy:** Change it to "after 毛's kun reading け".
- **Evidence:** `kanji\毛.md` lists `onyomi: [モウ]` and `kunyomi: [け]`, and its reading table labels け as kun. The 毛糸 record reads けいと.
- **Confidence:** high.

Other checks found no problems:
- **Metadata:** all strokes, radicals, grades and readings match the KANJIDIC records.
- **Source-only readings:** the three qualifications (簡 えら.ぶ, 総 す.べて, 線 すじ) are honest. The 筋 entry lists only 筋 and 条 as spellings.
- **Distractors:** all 45 are semantically wrong options. Older cards with similar meanings (建, 全, 単, 赤, 青, 米, 清, 真) each have three curated distractors, and no remaining two-option card has a meaning close to a new kanji.
- **Word quizzes:** the exclusions on 書籍, 粒 and 総額 cover every direct synonym I found.
- **木綿 claim:** the claim that もめん and the cotton-material sense are kept separate from the きわた tree-name sense is confirmed by the public JMdict entry 1534870 (fetched through the Jisho API).

## Optional
- **O1:** 築 "build; construct" is almost the same label as 建 "build, construct". They are not in each other's quizzes, but the app's duplicate check only catches identical strings. A label like "build up; establish" would separate them.
- **O2:** The 紅 べに row could add "rouge", its most common modern standalone sense. The Notes already mention it.
- **O3:** The 粉 こ row could show 小麦粉 as its typical example instead of standalone 粉 こ.
- **O4:** In the 綿 わた row, "(usually written in kana)" could sit beside "cotton plant", since that flag applies only to the plant sense.

## Limits
- No Git verification of the commit or the 54-file diff.
- Stroke paths not reviewed; they came from the pinned converter.
- Book-synonym records 本…発行 were read at gloss level only.
- The Jisho mirror's JMdict version may differ from the pinned source.
- Naturalness of the example sentences is not native-certified.
