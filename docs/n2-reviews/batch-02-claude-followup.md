## Snapshot
I reviewed the corrected commit 8f857fe0b6df3afa2847f3733cf56e9d714d9140, committed files only; my initial review was at 3ec3eeab4373dc84ade3cd189534d1eae55f4033. I have file-reading and web access but cannot run Git. I could not confirm the commit hash, the clean worktree or where the diff file came from. I checked every hunk in the diff file against the current files and they match.

## Scope
**Reviewer:** claude-opus-5.5 (Claude family). I worked alone, made no edits and read no prohibited files.

**Reviewed:**
- My preserved initial report.
- Every hunk in `n2-batch-02-corrections.diff`.
- The full current text of the nine changed pages: 像, 億, 党, 兵, 刷, 兆候, 児童, 兵士 and 冊子.
- batch-02.json:485–555, covering the 兆候, 児童, 党 and 兵士 source records and the new external 兵士 source.
- batch-02.json:2780–2905, covering the 兵法 ひょうほう and へいほう pair and the 兵士 record.
- The existing articles named in the new exclusions: 少年, 生徒, 図書, 症状 and サイン. I also read 学生.
- Title searches for overlapping meanings.

**Not reviewed again:** the eleven unchanged new pages, the 13 legacy link edits, stroke files, and the rest of batch-02.json.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\像.md | CLEAN | CLEAN | CLEAN |
| kanji\億.md | CLEAN | CLEAN | CLEAN |
| kanji\党.md | CLEAN | CLEAN | CLEAN |
| kanji\兵.md | CLEAN | CLEAN | CLEAN |
| kanji\刷.md | CLEAN | CLEAN | CLEAN |
| words\兆候.md | CLEAN | CLEAN | CLEAN |
| words\児童.md | CLEAN | CLEAN | CLEAN |
| words\兵士.md | CLEAN | CLEAN | CLEAN |
| words\冊子.md | CLEAN | CLEAN | CLEAN |

## Findings
**No actionable findings remain.** None of the changed passages introduces an error, omission or ambiguity that I could establish.

**How each initial finding was handled:**

| ID | Status | Evidence |
|---|---|---|
| F-01 (兵法 reading) | **Resolved** | 兵.md:42 now gives both へいほう and ひょうほう and keeps the warning not to generalize. batch-02.json:2800–2868 has both readings under JMdict 1506680. The card makes no claim about which is more common, which suits the source: only ひょうほう carries reading-priority tags. |
| F-02 (兵士 rank) | **Resolved** | 兵士.md:15–16 now says "ordinarily a rank-and-file member… serving under officers". Lines 35 and 39–40 match this, and "rank" was correctly dropped from the list of things the word doesn't identify. This matches the Nihon Kokugo Daijiten へいし sense ①: 士官の指揮をうける者…兵卒. Lines 43–44 cite that exact entry and sense and keep it separate from ひょうじ, consistent with batch-02.json:547–554. |
| F-03 (児童 exclusions) | **Resolved**, including the secondary 生徒 point | 児童.md:8 adds 少年 and 生徒. Lines 34–36 are accurate: 少年 has a legal "juvenile" sense, and school usage splits 小学校 as 児童 from 中学/高校 as 生徒. Both statements match the 少年 and 生徒 articles. |
| F-04 (冊子 exclusions) | **Resolved** | 冊子.md:8 and 32 add 図書 "books". Every existing title containing "book" (本, 書物, 図書) is now excluded. |
| F-05 (億万長者 kana) | **Resolved** | 億.md:39 adds おくまんちょうじゃ. |
| O-01 (exclude 軍隊 from 兵士) | Still optional | Not adopted. |
| O-02 (兆候) | Partly adopted | The 症状 exclusion and the note at 兆候.md:36 were added; the symptom overlap matches JMdict "symptom" (batch-02.json:2159–2162) and the Nihon Kokugo Daijiten sense ②. The 徴候 spelling is still not mentioned, which remains optional. |
| O-03 (冊子 "names a publication") | Resolved | 冊子.md:27 now says "names a book or booklet". |
| Polish: 像 "an 像" | Resolved | 像.md:20. |
| Polish: 党 "below the table" and "similar-looking 口" | Resolved | 党.md:24 and 45. |
| Polish: 兵士 "brave or argumentative" | Resolved | 兵士.md:40. |

**Additions I had not asked for, now verified:**
- **刷.md:44:** 刷ります/刷って compared with します/して is correct, because 刷る is a godan verb and する is irregular.
- **兆候 excluding サイン (兆候.md:8 and 37):** this is justified. JMdict 1056230 sense 2 gives サイン as "sign; signal; indication" (jisho API), and サイン.md:15 says the same. The remaining "signal" titles, 信号 and 合図, refer to deliberate signals and stay distinct.

## Optional
These are nonblocking.
- **Still open from the initial review:**
  - O-01.
  - The 徴候 spelling note.
  - O-04 expansions: 短冊, 兵器/兵隊 and 刷毛.
  - Polish on unchanged lines: 冊:24 and 43, 停:31 and 42, 傾:46, and 兆候:27 "weather report".
- **兵.md:46:** the card cites the 兵士 dictionary page without saying what it supports. A short label such as "for the 兵士 rank-and-file sense" would help.
- **兵士.md:35:** this is a caution about scope placed under "Synonyms and antonyms". This is a style point only.
- **児童 quiz:** 学生 "student" shares only the kango word type with 児童 and usually means a university student. It is a distinguishable wrong answer, so I don't recommend excluding it.

## Limits
- Without Git I could not confirm the commit, the clean worktree, or that the diff covers every change since 3ec3eeab.
- I did not run the app's quiz scoring, so the exclusion analysis covers eligible candidates, not observed quiz output.
- The jisho API's JMdict version may differ from the pinned snapshot. Kotobank's Daijisen text for 兵士 did not render.
- Naturalness is judged plausible, not certified by a native speaker.
- The unchanged pages and stroke files were not reviewed again.
