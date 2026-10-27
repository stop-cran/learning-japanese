## Snapshot
This review covers the corrected commit `093d288e79ecdae3aa14ff6d1f00853c5bef6683`, compared with the original snapshot `78ce7d7b97b863a034746ed2fcd43084233756db`. `.git\refs\heads\jlpt-n2-kanji` contains the corrected hash. It covers committed files only. I could only read files and did not run Git, so I could not confirm the clean worktree or the eleven-file scope myself. Those are the author's checks.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **Diff read in full:** `n2-batch-18-fix.patch`, which changes five pages. It matches the pages exactly.
- **Pages read in full:** `words\群れ.md`, `words\耕す.md`, `words\脂.md`, `kanji\脂.md`, `kanji\耕.md`.
- **Also read:**
  - My original report.
  - `words\学校.md`, `起す.md`, `打つ.md` and `石油.md`.
  - The quiz-exclusion rules in `content-format.md:66-67`.
- **Pinned source records read in `batch-18.json`:** 群れ 1247510, 起す 1223660, 打つ 1408810, 石油 1382830 and 次 1316380. The packet has 78 records.
- **Outside the suggested file list:** I read only the front matter of `作る.md`, `返す.md` and `開く.md`, to check whether the 耕す fix is complete.

## Verdicts
| Page | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| words\群れ | CLEAN | CLEAN | CLEAN |
| words\耕す | CLEAN | NEEDS FIX | CLEAN |
| words\脂 | CLEAN | CLEAN | CLEAN |
| kanji\脂 | CLEAN | CLEAN | CLEAN |
| kanji\耕 | CLEAN | CLEAN | CLEAN |

## Findings
**Dispositions of the original review:**
- **Original findings:** there were none.
- **Gap in my own first review:** I marked the quiz coverage of 群れ and 耕す CLEAN but missed three overlaps.
  - 群れ sense 1 includes "school", which matches 学校's plain title "school".
  - 起す sense 5 is "to plough; to plow; to till".
  - 打つ sense 9 is "to till (soil)".
  - None of these senses is restricted to another spelling or reading. The new exclusions fix all three.
- **Exclusion rules:** every new target exists, none repeats or names itself, and none clashes with a curated distractor (学校's are [学生, 大学]).
- **O-3 (kerosene label): resolved.** Both 脂 pages now call the kerosene sense colloquial (`words\脂.md:39`, `kanji\脂.md:44`). This matches 1382830 sense 2 and `石油.md`.
- **O-1 (羽音) and O-2 (群雲): optional and declined.** I accept that; the cards make no frequency claims.
- **Limit on 翌日 and 次: withdrawn.** 次 (1316380) means only "next; following; subsequent" or "stage; station", with no day sense, so there is no direct ambiguity with 翌日.

**R-1: Minor, coverage.**
- **Where:** `words\耕す.md:8`, plus the source citations at `words\耕す.md:50` and `kanji\耕.md:45`.
- **Problem:** the new exclusions [起す, 打つ] leave out 作る (title "make; prepare"). Its JMdict entry 1597890, cited by `作る.md:38`, has sense (4) "to till" with no restriction. That is the same problem the fix addressed for 起す and 打つ.
- **Impact:** "till; plough" is a valid meaning of 作る. If 作る and 耕す appear in the same word quiz, either direction can show two correct choices.
- **Fix:** confirm the sense in the pinned dictionary, then add 作る to the exclusions and add 1597890 to both citations and, if your conventions require it, the source packet.
- **Evidence:** EDRDG WWWJDIC (version 25 Jun 2025) lists 作る/造る/創る つくる, verb, sense (4) "to till". jisho.org's JMdict data agrees.
- **Status and confidence:** this is not a regression; the fix is incomplete. I am highly confident about the public dictionary data and moderately confident the pinned version matches.

**Regressions:** none.

## Optional
- `words\群れ.md` could mention "school (of fish)" in its meaning text so that the 学校 exclusion has a visible reason.

## Limits
- This was a bounded check of the changed passages only. I did not run Git or the validator, review stroke drawings, test the quiz in the app, or check the examples as a native speaker would.
- **Source checks:**
  - 作る's record is not in the pinned packet.
  - The EDRDG JMdict database is password-protected, so I used public mirrors (WWWJDIC and jisho) instead.
  - I counted the 78 records but did not count the 75 entry families.
- **Search coverage:** I did not search the whole dictionary for other words meaning "till" or "school". I checked existing word titles and tested 返す (no till sense). The 開く page in the app is the あく reading ("open"), so I did not check it.
