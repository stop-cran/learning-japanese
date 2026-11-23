Snapshot: commit 8d16c5825b55edb369dd53be72decb401b805a0b (8d16c582); reviewer model: Claude (Anthropic), running as GitHub Copilot sub-agent.

Scope: Read in full: this packet's INSTRUCTIONS.md, CHANGES.md, RESPONSE.md, diffs\fix.patch, snapshot\kanji\牧.md, evidence\README.md, checks\link-targets.tsv, checks\quiz-safety.txt (all 45 lines, all 15 cards). Read partially: checks\reading-exposure.txt (first 40 lines, through the start of 牧), checks\reading-options.txt (only the lines matching 牧, "problem" and "summary"), evidence\QuizBuilder.kt (only the lines matching exclusion, distractor and shuffle logic: 9-38). From the original packet batch-146-38833c7f: repo\docs\content-format.md lines 107-131 (kanji quiz authoring and `quiz_exclusions`), titles\kanji-titles.tsv (searched only for the compared kanji and for overlapping glosses such as priest, govern, official, field, raise and administer), evidence\public-source\weblio-牧.txt (Daijisen character entry). I did not open diffs\changed-lines.txt, the other checks files, the earlier confirmation packet or my earlier reports in this round; the 14 unchanged cards were not reread. No web fetches were needed: the Daijisen text was already in the packet.

Dispositions: RESPONSE.md has no earlier IDs, so there are none to give. On the author's question about the rule: I agree with it. content-format.md:124 and :129 ask authors to check the displayed labels against the target's "ordinary meanings". Here the card itself teaches the Daijisen senses 2 and 3 (牧.md:26-27). An exclusion only removes wrong options and can never create a second correct answer, so excluding the labels that give the taught senses is the safer reading of the rule. My earlier acceptance ("govern" is not in the title) was the narrower reading, and the restored list is more consistent with the card body. Pair by pair (target title "pasture; raise livestock; pastor"):
- 畜 "livestock; domestic animals": defensible. It overlaps "raise livestock" directly.
- 養 "nourish; raise; adopt": defensible. "raise" overlaps "raise livestock".
- 育 "grow up; raise": defensible, for the same reason.
- 農 "agriculture; farming": defensible. Stock farming (牧場 "stock farm; ranch") is farming, so a learner could accept it.
- 野 "open field": defensible. A pasture is an open field, and Daijisen まき is a place for grazing.
- 僧 "Buddhist monk; priest": defensible. "pastor" and "priest" are both clergy. But see Finding 1 on 坊.
- 師 "teacher; specialist": weakest of the twelve, but defensible as a conservative choice. It is the second element of 牧師, and a pastor is a spiritual teacher. Over-exclusion costs nothing here, because 牧 always gets its 3 curated options.
- 治 "govern; heal": defensible. Daijisen sense 2 is 「人々を治め導く」 (weblio-牧.txt:6), taught at 牧.md:26.
- 御 "honorific; govern": defensible. Its "govern" matches sense 2.
- 官 "government official": defensible. It matches sense 3, 「役人。地方長官」 (州牧), taught at 牧.md:27.
- 司 "take charge; official; preside": defensible. Its "official" matches sense 3.
- 導 "guide; conduct": defensible. Daijisen sense 2 literally contains 導く. The card text says only "Govern", though (see Optional).
Removals: 牛 "cattle, cow", 馬 "horse", 羊 "sheep" and 草 "grass; weeds" are correctly dropped. They are things in the scene, not meanings of 牧, and no learner would accept them for "pasture; raise livestock; pastor", or 牧's title for them. 草 is the closest, since English "pasture" can mean grazing grass, but 草 does not mean pasture and 牧 does not mean grass. The removal of 坊 is inconsistent with keeping 僧 (Finding 1).

Verdicts:
- Correctness: CLEAN. Every gloss quoted at 牧.md:53-54 equals the target's displayed title (link-targets.tsv: 16 links, 0 mismatches). The Daijisen-based statements match weblio-牧.txt.
- Scoped coverage: CLEAN.
- Consistency and quiz safety: NEEDS FIX (牧, Finding 1). Mechanically the list is clean. 12 distinct entries, no self entry and no overlap with distractors [歌, 山, 雨]. All links resolve. QuizBuilder.kt:26-30 applies exclusions symmetrically, against both the target and the options already chosen. quiz-safety.txt shows 牧's options as song, sing | mountain | rain, filled 3/3 from distractors. The other 14 cards' options are unchanged and give no new concern.
- Comprehensibility: CLEAN (polish under Optional).

Confirmation: NEEDS FIX. There are no IDs to disposition, but Finding 1 is a minor actionable consistency defect.

Findings:
1. Severity: minor. Facet: consistency and quiz safety. Location: 牧.md:14 and 牧.md:54.
   - Claim and impact: 僧 "Buddhist monk; priest" stays excluded on the stated ground that the title's "pastor" overlaps it (牧.md:54). 坊 "Buddhist priest; boy" (kanji-titles.tsv:313) carries the same "priest" overlap and is no longer excluded. Neither 僧 nor 坊 is a meaning of 牧. The only basis for either is that its displayed label is near "pastor", and on that basis the two labels cannot be told apart. The exposure is fallback-only. 牧 normally fills 3/3 slots from 歌 山 雨, so it arises in a custom pool lacking those, or when 坊 is the target and 牧 is offered as a fallback option. A learner could then treat "pastor" and "Buddhist priest" as rival correct answers, which is the case content-format.md:111-113 warns about.
   - Remedy: restore 坊 to `quiz_exclusions` (13 entries) and name it in 牧.md:54 beside 僧. Alternatively, drop 僧 as well, with the same stated reason, so the two are treated alike. Restoring 坊 is preferred because an exclusion costs nothing here.
   - Evidence: 牧.md:14 and 牧.md:54; diffs\fix.patch, where 坊 is removed and 僧 kept; titles\kanji-titles.tsv:114 and :313.
   - Confidence: high that the treatment is inconsistent; medium that the 坊/牧 pair would actually confuse a learner.

Optional:
- 牧.md:54 says "with the five kanji in the previous bullet", but that bullet now links nine kanji, four of them explicitly not excluded. "with the first five kanji of the previous bullet (畜 養 育 農 野)" would be clearer on a phone.
- 牧.md:53 opens "Words for the first sense", but the items are kanji, not words. "Kanji related to the first sense" would be more accurate.
- 牧.md:26 glosses sense 2 only as "Govern". Daijisen has 「治め導く」, "govern and guide people". Adding "and guide" would ground the 導 exclusion in the card text itself.
- The title scan found three unexcluded labels near the official and govern senses: 掌 "palm (of the hand); administer", 府 "urban prefecture; administration" and 公 "public, official". None is a plausible second answer for 牧's displayed title, so this is not a defect, only a note that the "taught senses" rule could be applied further.

Limits:
- I did not rerun quiz-safety.txt, reading-options.txt or reading-exposure.txt. I read them as outputs, and reading-exposure.txt only up to the start of 牧's section. So I did not verify the claimed "0 production or padded hits, 10 latent collisions". The 牧 section of reading-options.txt was not read in full; I relied on its "0 problem(s)" summary.
- I did not check whether any other card lists 牧 in its `distractors` together with one of the 12 excluded kanji. In that case QuizBuilder would drop one of them silently and fall back. This needs a corpus scan, which the mandate forbids.
- The audits cannot show learner perception: whether a given label pair actually reads as two correct answers is an editorial judgment. They also cannot show behavior on older APKs that ignore `quiz_exclusions`. The Android JVM tests on the real content were not run.
- I read only the Weblio rendering of the Daijisen entry, in the packet copy, not the live site.
- Every response in this round contained exactly one tool call. Some single PowerShell calls chained several read-only commands.
