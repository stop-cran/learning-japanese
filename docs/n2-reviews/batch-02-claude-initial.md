## Snapshot
I reviewed frozen commit 3ec3eeab4373dc84ade3cd189534d1eae55f4033, committed files only. I had file-reading tools but no Git, so I could not confirm the hash, that the worktree is clean, or the diff against baseline 1023fa9. I relied on the author's statement that the worktree is clean.

## Scope
**Reviewer:** model claude-opus-5.5, Claude family. I worked alone, made no edits, and did not read any prohibited files.

**Read completely:**
- Kanji cards: 個, 倍, 停, 傾, 像, 億, 兆, 児, 党, 兵, 冊, 再, 凍, 刊, 刷.
- Word articles: 兆候, 児童, 兵士, 冊子, 刊行.
- docs\n2-batch-sources\batch-02.json, in full: the KANJIDIC2 metadata and all JMdict records.

**Narrow scope:** I checked only the first-mention card link in "How the kanji combine" in these 13 articles: 個人, 倍, 停留所, 傾向, 億, 党, 再び, 再来年, 再来月, 再来週, 凍る, 印刷 and 想像. All 13 links are correct. 印 is correctly left unlinked because there is no 印 card.

**Supporting pages:** I checked the front matter (titles, distractors, tags and exclusions) of the distractor cards, the overlap candidates and the legacy cards that have only two distractors.

**Not reviewed:** stroke files and the teaching text of the legacy articles.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 個 | CLEAN | CLEAN | CLEAN |
| 倍 | CLEAN | CLEAN | CLEAN |
| 停 | CLEAN | CLEAN | CLEAN |
| 傾 | CLEAN | CLEAN | CLEAN |
| 像 | CLEAN | CLEAN | CLEAN |
| 億 | CLEAN | CLEAN | NEEDS FIX |
| 兆 | CLEAN | CLEAN | CLEAN |
| 児 | CLEAN | CLEAN | CLEAN |
| 党 | CLEAN | CLEAN | CLEAN |
| 兵 | NEEDS FIX | CLEAN | CLEAN |
| 冊 | CLEAN | CLEAN | CLEAN |
| 再 | CLEAN | CLEAN | CLEAN |
| 凍 | CLEAN | CLEAN | CLEAN |
| 刊 | CLEAN | CLEAN | CLEAN |
| 刷 | CLEAN | CLEAN | CLEAN |
| 兆候 | CLEAN | CLEAN | CLEAN |
| 児童 | CLEAN | NEEDS FIX | CLEAN |
| 兵士 | NEEDS FIX | CLEAN | CLEAN |
| 冊子 | CLEAN | NEEDS FIX | CLEAN |
| 刊行 | CLEAN | CLEAN | CLEAN |

**Checked and consistent with the source:**
- Every reading, stroke count, radical and grade matches KANJIDIC2.
- Every reading-table example matches its JMdict record, including spelling, reading and sense restrictions.
- The source-only reading rows (児 ゲイ, 党 なかま/むら, 冊 ふみ, 凍 こご.る) are honestly qualified. JMdict has こごる only under 凝る.
- The Kotobank 兆候 and 児童 pages and the Kanjipedia 掃く page (②「刷く」とも書く) support what the cards cite them for.
- All 45 kanji distractors are existing cards with titles that are clearly different in meaning. All legacy cards with overlapping titles (止, 子, 士, 本, 画, 冷) have three curated distractors. The legacy cards with only two distractors share no tags with the new cards.

## Findings
**F-01 · Minor · Correctness · kanji\兵.md:42**
- **Problem:** The note says the ヒョウ reading occurs in 兵法 ひょうほう and tells learners to "learn the compound's reading". This treats ひょうほう as the reading of 兵法. The cited entry, JMdict 1506680, lists へいほう first and ひょうほう second. The batch record (batch-02.json:2794–2830) selected only ひょうほう. Kotobank (世界大百科事典) gives 兵法 (へいほう) and says 〈ひょうほう〉と呼ばれることも多い.
- **Impact:** Learners may think the standard reading へいほう is wrong.
- **Fix:** Say that 兵法 is read へいほう or ひょうほう, or drop the 兵法 example and keep 兵糧.
- **Evidence:** jisho.org API (JMdict); kotobank.jp/word/兵法-129027.
- **Confidence:** High.

**F-02 · Minor · Correctness · words\兵士.md:35, 39–40**
- **Problem:** The article says "There is no requirement that a 兵士 be an officer" and that the word "does not by itself identify the person's rank". The Nihon Kokugo Daijiten (Kotobank 兵士-624031) defines へいし ① as 軍隊で、士官の指揮をうける者…兵卒: a rank-and-file soldier under officers. The article has the nuance backwards.
- **Fix:** State the core sense as a rank-and-file soldier under officers' command (兵卒). Keep the point that the word does not specify nationality or whether the person is in combat.
- **Confidence:** Medium-high. Loose modern usage was not checked against a corpus.

**F-03 · Minor · Scoped coverage (quiz) · words\児童.md:8 and words\少年.md:4, 7–8**
- **Problem:** 少年 "boy; juvenile" and 児童 "children; juvenile" share the type kango, the tags kango and people, and the exact gloss "juvenile". Neither excludes the other.
- **Impact:** The 児童 word quiz can show two choices that both say "juvenile".
- **Fix:** Add 少年 to 児童's quiz_exclusions.
- **Secondary, a judgment call:** 生徒 "pupil; student" (kango, education) overlaps with the article's own school sense at lines 15–16 (Nihon Kokugo Daijiten: 特に小学校に学んでいる子ども). Consider excluding it too.
- **Confidence:** High for 少年; medium for 生徒.

**F-04 · Minor · Scoped coverage (quiz) · words\冊子.md:8, 32–34, 39–40 and words\図書.md:4, 7–8**
- **Problem:** 冊子 excludes 本 and 書物 because of its broader "book" sense. 図書 "books" shares the books tag and the kango type, but it is not excluded.
- **Impact:** "books" can appear as a defensible wrong answer in the 冊子 quiz.
- **Fix:** Add 図書 to 冊子's quiz_exclusions.
- **Confidence:** Medium-high. The inconsistency is certain; whether 図書 is actually selected depends on the candidate scoring.

**F-05 · Low · Comprehensibility · kanji\億.md:39**
- **Problem:** 億万長者 is the only word in the batch's kanji cards given without kana, and 長者 is not basic vocabulary.
- **Fix:** Add おくまんちょうじゃ.
- **Confidence:** High.

## Optional
These are nonblocking.
- **O-01:** In the 兵士 quiz, 軍隊 "armed forces; troops" shares the military tag, and the 兵 card is itself titled "soldier; troops". Consider excluding 軍隊.
- **O-02:** 兆候 could mention the 徴候 spelling (Nihon Kokugo Daijiten headword 兆候・徴候). Line 15 says 兆候 can mean "symptom", while 症状 is titled "symptoms"; an exclusion may be worth considering.
- **O-03:** 冊子:27 says the word "names a publication", while the 出版 and 刊行 titles start with "publication". Consider a different wording.
- **O-04 (expansions):**
  - 冊: 短冊 たんざく would be a more useful サク example than 冊封.
  - 兵: add 兵器 and 兵隊 to the common words.
  - 刷: mention 刷毛 はけ.
- **Wording polish:**
  - 像:20 "an 像".
  - 党:45 says the readings are "below the table", but they are in table rows 31–32. 党:24 "similar-looking 口".
  - 冊:24 "not a separate word within 冊"; 冊:43 "さくし".
  - 停:31 "alternative stopping spelling". 停:42 uses the rare spelling 停まる in a model sentence.
  - 傾:46 "same conjugation" is vague.
  - 兆候:27 "not a literal weather report".
  - 兵士:41 "brave or argumentative".

## Limits
- Without Git, I could not confirm the snapshot, a clean worktree, or that the 13 legacy articles are otherwise unchanged from 1023fa9.
- Stroke files were made by the pinned KanjiVG converter and were not audited.
- I did not run the app's quiz candidate scoring. F-03, F-04 and O-01 describe eligible candidates, not observed quiz output.
- The jisho.org web pages failed to load, so I used its API, which may use a different JMdict version from the pinned snapshot. Kotobank's Daijisen text for 兵士 did not render, so I relied on the Nihon Kokugo Daijiten entry.
- Naturalness of the examples is judged plausible, not certified by a native speaker.
