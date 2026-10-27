## Snapshot
Frozen commit `5769c83f86c2c719c8d38a4f6892cfeee848aab5` (parent `1dd877fe2c139c8091e7c3b3191e4c71d6769b45`). I reviewed committed content only. I had file tools only and could not run Git or compute hashes, so I could not confirm that the files on disk match the commit. The receipt says `cleanCommittedContent: true`, with one stated qualification: 書店 has CRLF line endings.

## Scope
- **Model:** claude-opus-5.5 (Claude family). No delegation and no edits.
- **New articles:** I read all 16 completely.
- **Reused articles:** I checked しょうゆ, 書籍, 書店 and 資料 only for the claimed narrow changes.
- **Diff and kanji:** I read the 8-file related diff and the full kanji cards for 省, 略, 塩, 油 and 籍.
- **Mappings and evidence:** I read TSV rows N2:782–801. I read principal-reading.txt and public-reading.txt completely. I read only parts of the evidence JSON (rows and reviewEvidence sections). I used targeted entry reads of inspection-reading.txt and targeted grep of the MEXT proposal's 助手/助教/准教授 sections.
- **Comparison cards:** I read ご存じ, 器具 and 抜く, and checked the titles and exclusions of about 80 comparison cards.
- **Not read:** extra-comparison-reading.txt, public-bodies.json, both snapshot JSONs, confusable-words.md and jlpt-levels.md. I read no forbidden files and made no web fetches.

## Verdicts
Order in each cell: correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| 消耗, 省略, 初級, 助教授, 食塩, 職人, 初旬, 食器, ショップ, 書道, 白髪, シリーズ, 私立, 汁 | CLEAN / CLEAN / CLEAN |
| 知り合い | NEEDS FIX (B40-F1) / CLEAN / CLEAN |
| 素人 | CLEAN / NEEDS FIX (B40-F2) / CLEAN |

- **Kanji edits:** 省 (ショウ→省略), 略 (リャク→省略), 塩 (エン→食塩) and 油 (ユ→醤油/しょうゆ) are CLEAN on all three facets. Existing readings and source qualifications are kept; the added JMdict IDs are correct.
- **籍/書籍:** The unchanged セキ link to 書籍 is reciprocal and correct. CLEAN.
- **Narrow reuses:** All four are CLEAN.
  - しょうゆ keeps its kana ID, N5 level and empty kanji array; it only gains the 油 (ユ) link.
  - 書籍, 書店 and 資料 only gain `jlpt: 2`. 書籍 keeps its 7 exclusions.
- **Mappings:** All 20 are CLEAN on correctness and comprehensibility; the entry, sense and restriction selections are correct. Scoped coverage is CLEAN except N2:801 (素人), which is NEEDS FIX through B40-F2.

## Findings
**B40-F1 — Minor; correctness (quiz metadata); medium confidence**
- **Where:** `words\知り合い.md:1-9` has no `quiz_exclusions`. `words\ご存じ.md:4` has the title "knowing; being acquainted"; lines 15 and 20 describe "being acquainted" and say the example "illustrates acquaintance".
- **Evidence:** Daijisen defines 知り合い as 「互いに相手を知っていること。また、その相手。」 (public-reading.txt:41). So "being acquainted" is a fair answer for 知り合い, and "acquaintance" is a plausible pick for ご存じ.
- **Impact:** ご存じ (N4) is in the N2 study pool, and both cards are tagged noun. A learner could be marked wrong for a defensible answer.
- **Remedy:** Add `quiz_exclusions: [ご存じ]` to 知り合い.md; exclusions are symmetric, so one side is enough.
- **Why only medium confidence:** I did not inspect how the quiz builder picks wrong answers, and the two cards share no kanji.

**B40-F2 — Minor; scoped coverage; medium confidence**
- **Where:** `words\素人.md:15-17, 33-34, 40-41`; mapping N2:801.
- **Evidence:** The source gloss is "amateur,novice", and JMdict sense 1 includes "novice". Daijisen sense 1 opens with 「その事に経験が浅く、未熟な人。その道で必要な技能や知識をもっていない人」. Its example 「素人とは思えぬみごとな芸」 assumes a 素人 normally lacks skill.
- **Gap:** The article teaches lack of specialist knowledge and non-professional status. It never teaches inexperience or lack of skill, and its contrasts ("need not be new", "an amateur can be skilled") steer learners away from that sense.
- **Impact:** Learners may miss common uses such as 素人考え and 素人とは思えない.
- **Remedy:** Add one Meaning sentence saying 素人 can also describe someone inexperienced or lacking a field's needed skill. Keep the existing 初心者 caveat.

## Optional
These are not defects:
- 食器 / 器具 ("utensil; tool; apparatus"): they share 器, and Daijisen defines 食器 as 容器・器具. Consider an exclusion.
- 職人 / 名人 ("master; expert"): the article teaches 職人's "highly skilled specialist" extension, and both share 人. Consider an exclusion.
- 知り合い: add 知り合いになる as the natural "become acquainted" construction alongside the warning against adding する at lines 29-30.
- 消耗: note that Daijisen calls しょうもう the conventional (慣用) reading of the original しょうこう.
- 白髪 is typed `wago`, but しらが works like a whole-word reading. I recall, without having checked, that 白髪/しらが is in the 常用漢字表付表. This is a consistency point only.

## Limits
- Hashes, equivalence claims and receipts were not independently verified.
- All Daijisen and MEXT material is the author's captures, not my own retrievals.
- I did not read the evidence files listed under Scope as not read, and I did not audit the 34 component records individually.
- I did not inspect the quiz builder's code, so B40-F1's collision likelihood is estimated from the documented rules.
- This is not a native-speaker certification.
