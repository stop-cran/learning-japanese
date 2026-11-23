Snapshot: commit d276f63b4d2adf4985f8bf929bdad1103987556b (d276f63b); reviewer model: Claude (Anthropic), running as a GitHub Copilot sub-agent.

Scope:
- Read in full from this packet: INSTRUCTIONS.md, CHANGES.md, RESPONSE.md, diffs\fix.patch, diffs\changed-lines.txt, snapshot\kanji\牧.md (all 58 lines), evidence\README.md, evidence\QuizBuilder.kt, evidence\meta-scan.txt, checks\quiz-safety.txt (all 15 cards), checks\link-targets.tsv, checks\lint.txt, checks\validate.txt, checks\unittest.txt, checks\kanji-remarks.txt and checks\budget.txt.
- Glanced at: checks\reading-exposure.txt and checks\reading-options.txt. I read only the command lines, the 牧 sections' header and unlisted-reading lines, and the summary lines (exposure :277-278, options :241).
- Also read: my own report reports-146\confirm4-claude.md, and the original packet's evidence\public-source\weblio-牧.txt (Daijisen extract).
- Web: one live fetch of https://www.weblio.jp/content/牧 (Digital Daijisen character entry).
- Not reopened in this round: the 14 unchanged cards, content-format.md, kanji-titles.tsv and the confirm4 packet. For the rule I relied on my confirm4 reading of content-format.md:107-131. For the displayed titles I relied on link-targets.tsv.

Dispositions:
- Finding 1 (僧 excluded while 坊 was not) - RESOLVED.
  - The author took my alternative remedy: 僧 is now treated the same as 坊.
  - 牧.md:14 now lists 11 entries, `[畜, 養, 育, 農, 野, 治, 御, 官, 司, 導, 師]`. It includes neither 僧 nor 坊.
  - 牧.md:54 states the same reason for both: "Buddhist clergy, not meanings of 牧".
  - The patch matches: it removes only 僧 from line 14.
  - On the merits the remedy is sound. Each label carries "Buddhist", and 牧師 is a Christian (Protestant) pastor. So neither "Buddhist monk; priest" nor "Buddhist priest; boy" can be a second correct answer for "pasture; raise livestock; pastor". The reverse also holds: 牧's title cannot be a second correct answer when 僧 or 坊 is the target.
  - In confirm4 I preferred restoring 坊. Treating the two alike is equally consistent, and it is the better-grounded reading of the "ordinary meanings" rule.
- Optional "l.54 five kanji in the previous bullet" - RESOLVED. 牧.md:54 now reads "These six, with 畜 養 育 農 野 above". 6 + 5 = 11, which equals the length of line 14.
- Optional "l.53 Words for the first sense" - RESOLVED. 牧.md:53 now opens "Kanji related to the first sense".
- Optional "l.26 and guide" - RESOLVED.
  - 牧.md:26 now reads "Govern and guide people".
  - This matches Daijisen sense 2, 「人々を治め導く」. I checked it in weblio-牧.txt and on the live Weblio page today.
  - It now grounds the 導 "guide; conduct" exclusion in the card text.
- Optional "掌 府 公" - DECLINE ACCEPTED. No change was made, as I had recommended. None of the three is a plausible second answer for 牧's displayed title.

Pair-by-pair defensibility of 牧's 11 `quiz_exclusions`. The target title is "pasture; raise livestock; pastor". The taught senses are Daijisen 1-3 at 牧.md:25-27.
- 畜 "livestock; domestic animals": defensible. It overlaps "raise livestock" directly.
- 養 "nourish; raise; adopt": defensible. "raise" overlaps "raise livestock".
- 育 "grow up; raise": defensible. "raise" overlaps in the same way.
- 農 "agriculture; farming": defensible. Stock farming is farming (牧場 "stock farm", 牧畜 "livestock farming").
- 野 "open field": defensible. A pasture is an open grazing field (まき, 「放し飼いにする場所」).
- 治 "govern; heal": defensible. "govern" is Daijisen sense 2, taught at :26.
- 御 "honorific; govern": defensible. "govern" is sense 2.
- 官 "government official": defensible. It matches sense 3, 「役人。地方長官」 (州牧, taught at :27).
- 司 "take charge; official; preside": defensible. "official" matches sense 3.
- 導 "guide; conduct": defensible. 導く is in Daijisen sense 2, and the card now says "guide" at :26.
- 師 "teacher; specialist": defensible but the weakest, unchanged from my confirm4 judgment.
  - "teacher" is not itself a meaning of 牧.
  - The exclusion rests on 師 being the other element of the taught word 牧師 (牧.md:40) and on "pastor" as a spiritual teacher.
  - It only removes a wrong option, so it cannot create a second correct answer. 牧 always fills 3/3 options from 歌 山 雨.

Removed entries: 牛, 馬, 羊, 草, 僧 and 坊 are correctly not excluded. None is a meaning of 牧. No label among "cattle, cow", "horse", "sheep", "grass; weeds", "Buddhist monk; priest" and "Buddhist priest; boy" is a plausible correct answer for 牧's title, or the reverse.

Verdicts:
- Correctness: CLEAN.
  - Line 26 matches Daijisen sense 2.
  - Every gloss quoted at :53-54 equals the target's displayed title: link-targets.tsv has 17 links, 0 unresolved or mismatched.
  - "Buddhist clergy" is accurate for 僧 and 坊.
  - The statement "not excluded" matches line 14.
- Scoped coverage: CLEAN. The change only narrows Notes text and front matter, and nothing previously covered was lost.
- Consistency and quiz safety: CLEAN.
  - The exclusion list is 11 distinct entries, with no self entry and no overlap with distractors [歌, 山, 雨].
  - The Notes text at :53-54 names exactly the 11 excluded kanji and the 6 non-excluded ones, in agreement with :14.
  - QuizBuilder.kt applies exclusions symmetrically, both against the target and against options already chosen. Titles are deduplicated.
  - quiz-safety.txt shows 牧's options as song, sing | mountain | rain, 3/3 from curated distractors. The other 14 cards' options are as before and give no new concern.
  - Reading checks show no problems: reading-options.txt has 0 problems, and reading-exposure.txt has 0 production and 0 padded hits, with 10 latent collisions. This revision does not touch readings.
- Comprehensibility: CLEAN. "Kanji related to the first sense" and "with 畜 養 育 農 野 above" are clearer on a phone than the previous wording.

Confirmation: CONFIRMED. Every item is RESOLVED or DECLINE ACCEPTED, and I established no new actionable defect.

Findings: none.

Optional:
- 牧.md:54 now says 師 "teacher; specialist" overlaps the title's "pastor", but says 僧 and 坊 are "not meanings of 牧". A careful reader may find "teacher" no closer to "pastor" than "priest" is.
  - This is not a defect: the exclusion is harmless, and 師 is justified as the co-element of the taught 牧師.
  - A short clause would make the asymmetry explicit, for example: "師 is the second kanji of 牧師".

Limits:
- I did not rerun any check. quiz-safety.txt, reading-exposure.txt and reading-options.txt were read as outputs, the latter two only in part. The claimed "10 latent collisions" was not recounted.
- I did not check whether another card lists 牧 in its `distractors` together with one of its excluded kanji. That needs a corpus scan, which the mandate forbids. The removals of 僧 and 坊 can only make such conflicts rarer.
- The audits cannot show learner perception, or the behavior of older APKs that ignore `quiz_exclusions`. The Android JVM tests on real content were not run.
- Displayed titles of 僧 and 坊 come from link-targets.tsv. I did not reopen kanji-titles.tsv in this round.
- Every assistant response in this round contained exactly one tool call; no parallel calls were made. Some single PowerShell calls chained several read-only reads.
