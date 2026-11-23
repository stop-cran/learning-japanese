# Batch 140 confirmation report: Claude (Anthropic)

## Snapshot

- Revised snapshot: commit 1b24a5f97a396d7121689f3928c7aa500e0054ef.
- Previously reviewed snapshot: 28831314c9b8203cf7dd66c4eec16f23ef0fef22.
- Reviewer: Claude (Anthropic model family), working alone and read-only. I did not open the other reviewer's report or any author material outside the packet.

## Scope

Files opened in the confirmation packet `confirm-140-claude\`:

| File | How read |
| --- | --- |
| INSTRUCTIONS.md | in full |
| CHANGES.md | in full |
| RESPONSE.md | in full |
| diffs\fix.patch | in full (all hunks) |
| checks\quiz-safety.txt | in full |
| checks\reading-exposure.txt | in part: lines 1-120 (嵐 to 往, including 幣 and 弁) and the summary at about line 252 |
| checks\reading-options.txt | in part: grep for HIT, problem, the headers and fallback; the problem count line |
| checks\link-targets.tsv | in full |
| evidence\jmdict-cited-entries.xml | in part: grep for entries 1512850, 1524750, 2175880 and 2859605 |
| evidence\雨.json | in part: stroke start and end points |
| snapshot\kanji\弁.md | in full |
| snapshot\kanji\帳.md | in full |
| snapshot\kanji\幕.md | in full |
| snapshot\kanji\従.md | in part: lines 17-61 (the whole body, front matter not reread) |
| snapshot\kanji\幣.md | in part: lines 17-50; lines 1-16 and 51-end seen through fix.patch and link-targets.tsv |
| snapshot\kanji\径.md | in part: lines 17-end |
| snapshot\kanji\徐.md | in part: lines 17-end |
| snapshot\kanji\徴.md | in part: lines 1-50; line 56 seen through fix.patch and link-targets.tsv |
| Folder listings | root, evidence\, checks\ and snapshot\kanji\ (non-recursive) |

Files opened in the original packet `batch-140-28831314\` (read-only):

| File | How read |
| --- | --- |
| evidence\jmdict-digest.tsv | grep only: 幣 read にき, にぎ or ぜに (no match) |
| evidence\kanjipedia-outside-readings.json | grep only: 幣 |
| evidence\public-source\weblio-径.txt | grep only: 小径, 径庭, 捷径, 山径 |

My own report `reports-140\initial-claude.md` was used as the reference for my earlier IDs.

Public web sources checked:

- jisho.org API for 和幣 (no JMdict entry) and for 幣帛 (へいはく, "offering of cloth (rope, paper, etc.)", Shinto).
- The weblio Digital Daijisen headword にきて: 榊の枝に掛けて神前にささげる麻や楮で織った布, written 和幣, 幣帛 or 幣.

## Dispositions

**C1, 幣 distractors overlapping in meaning: RESOLVED.**
- The distractors are now [中, 南, 雨], with the titles "middle, inside", "south" and "rain". These are distinct from each other and from "currency; Shinto offering".
- The new Notes claim about 雨 is a true shape description. Stroke 4 in 雨.json is the central vertical, running from under the top bar (y 23.5) through 冂 (y 87.3).
- All three distractors are Starter cards, so the ヘイ reading quiz fills all three slots from them in every pool. reading-exposure shows 0 production hits and 0 padded hits for 幣.
- The author chose differently from my suggested remedy, and the reason holds. The fallback in the Starter pool could otherwise surface まい, as the superseded run showed with a PAD-HIT.

**C2, 徴 and 署 both titled with "sign": RESOLVED.**
- 署 is added to 徴's quiz_exclusions (line 14), and the Notes bullet (line 56) names it with its exact title "sign; government office". link-targets.tsv confirms the title matches.
- quiz-safety shows the curated 微, 徹 and 徳 filling every slot.

**C3, 帳 and 幕 share a curtain sense without excluding each other: RESOLVED.**
- 幕 is added to 帳's quiz_exclusions (line 14).
- Both Notes bullets (帳 line 50, 幕 line 60) state the shared sense with the exact other title. link-targets shows both titles match.
- An exclusion listed on either card applies in both directions, so this one entry covers both quizzes.

**O1, 径 path example: RESOLVED.**
- Line 28 uses 小径 しょうけい "path; lane", marked formal or literary. This matches JMdict 2859605, whose sense 2 is "small diameter".
- 小径 is one of Daijisen's sense-2 examples. 径庭 has moved to the reference bullet with the true gloss "great difference" and its alternative spelling 逕庭.

**O2, 幣 readings ぜに and にきて: RESOLVED.**
- ぜに comes from Kanjipedia 0006218900, which lists the kun readings ぜに, ぬさ and みてぐら. JMdict writes ぜに as 銭 (entry 2175880), and that entry is added to the Metadata line.
- にきて matches the live Daijisen headword, including the spellings 和幣 and 幣帛.
- The claim "in neither KANJIDIC2 nor JMdict" is supported: the digest grep found no match and jisho has no 和幣 entry.

**O3, 幕 マク fallback filling two slots: DECLINE ACCEPTED.**
- The fallback does fill two slots. The audits show no hit and no latent collision for 幕, so this is not a defect.

**O4, 弁 title and the word 弁当: RESOLVED.**
- The title and heading are now "speech; discern; valve; bento". The title is unique, quiz-safety shows no warning, and 飯 stays excluded.

**O5, 怠 distractor 治: DECLINE ACCEPTED.**
- The reason holds: the dated sense belongs to the word 怠る, not to the title shown as a quiz option.

## Verdicts

These hold for all 15 cards; no card differs.

| Facet | Verdict |
| --- | --- |
| 1. Correctness | CLEAN |
| 2. Scoped coverage | CLEAN |
| 3. Consistency and quiz safety | CLEAN (was NEEDS FIX, minor; C1-C3 are fixed) |
| 4. Comprehensibility | CLEAN |

## Confirmation

CONFIRMED.

Hunk checks:

- **弁 lines 3, 17, 25, 55 and 58.**
  - The 辨, 辯 and 瓣 grouping matches the Daijisen [補説].
  - 弁護士 matches JMdict 1512850 "lawyer; attorney", and the entry is added to the Metadata line.
  - The reference bullet keeps all eleven senses.
- **従 lines 25 and 56.** The restructure keeps every sense, example, kun reading and ひろい. It does not contradict the Readings table, the Joyo paragraph or the 従弟 note.
- **幣 lines 13, 31, 53 and 57.** Checked as described under C1 and O2.
- **帳 lines 14 and 50; 幕 lines 60 and 62.**
  - The exclusions and the text agree.
  - The quotation marks on paraphrases are removed. "act of a play" is part of the title, and "end; close" is a JMdict sense of entry 1524750.
- **径 lines 28 and 60.** Checked as described under O1.
- **徐 lines 36 and 48.**
  - The おもむ.ろに okurigana statement is correct: KANJIDIC2's dot marks ろに.
  - 遅 and 悠 are cited with their exact titles.
- **徴 lines 14 and 56.** Checked as described under C2.

Post-fix quiz options for all 15 cards:

- **Meaning quiz:** quiz-safety.txt has 0 errors and 0 warnings. Every card is served by its own curated distractors, and each is defensibly wrong.
- **Reading quiz:** reading-options.txt has one problem: the known HIT label for 幣 まい. まい is a non-quizzed reading, and reading-exposure shows it cannot be drawn.
- **reading-exposure:** 0 production hits and 0 padded hits. The 4 latent collisions (幣 まい, 弁 とく, 従 ひろい, 志 じん) are unchanged and are covered in each card's text.
- **Fallback slots:** the fallback fills slots for 幕 マク (two), 従 したが.う (律 has no kun reading) and 怠 おこた.る and なま.ける (念 has no kun reading). In each case no audit hit was found.

## Findings

None. There are no new established defects.

## Optional

- **O-A (弁 line 25).** The paragraph says Daijisen gives "eleven senses … in a few main groups", but the groups it describes cover only senses 1-8. Senses 9-11 (the cap of 武弁, the business sense of 合弁, and the braiding of 弁髪) appear only in the reference bullet. The pointer "listed at the end of the Notes" mitigates this. Wording such as "most of them fall into three groups" would be exact. This is polish, not a defect.

## Limits

- I made exactly one tool call per response and no parallel calls.
- **Tests and audits:**
  - The Android JVM tests and the Kotlin cross-check were not run at this snapshot.
  - The quiz and reading audits are Python models of the app. They sample the pools over a fixed set of seeds, do not model curated slots that are already filled in reading-options, and do not judge whether a distractor makes sense.
  - I did not open QuizBuilder.kt. The two-way exclusion behaviour is taken from CHANGES.md and from my first-round reading of the app code.
- **Partial reads:**
  - 幣's Notes (line 53 onward), 徴 line 56 and 従's front matter were checked through fix.patch and link-targets.tsv, not by rereading the whole file.
  - reading-exposure.txt lines 120-251 were not read individually; I relied on its summary.
- **Unverified items:**
  - For JMdict 1524750 sense 4 "end; close", I saw only the start of the entry and relied on CHANGES.md for the full sense.
  - jisho.org may mirror a different JMdict version than the 2026-11-17 snapshot.
  - I did not recompute the packet hash, and I did not reread unchanged lines beyond the regions listed in Scope.
- **Assumption:** no word article or stroke file changed, as CHANGES.md and fix.patch state.
