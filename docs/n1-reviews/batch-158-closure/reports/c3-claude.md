Snapshot: commit 348c4f70465633c63706133babacda198eedaa27; reviewer model: Claude (Anthropic; I identify as claude-opus-5.5, not verifiable from inside the session).

Scope: Read INSTRUCTIONS.md, CHANGES.md, RESPONSE.md, diffs\fix.patch and changed-lines.txt in full. Read kanji\匿.md, words\升.md and words\勲章.md in full. Read evidence\exclusion-precedents.md in full. Read the glosses of JMdict entries 1288370, 1346290 and 1706800 in evidence\jmdict-cited-entries.xml. Read the 升 block head of evidence\word-quiz.txt and the 匿 line of checks\quiz-safety.txt. Read the title, distractors and exclusions of kanji\皮.md and the title of words\皮.md, and the front matter of words\腰掛け.md (title "seat; bench", type wago, tags wago/noun/furniture/posture, own quiz_exclusions [いす, ベンチ, 席, 座席]), in the original packet. In a second pass I read the ledger rows in snapshot\docs\n1-sources\batch-158-progress.json (via grep with context) and the exclusion and option-selection code of evidence\QuizBuilder.kt (lines 15-40, in full) and evidence\Words.kt (lines 162-212).

Dispositions:
- F1 - RESOLVED - 腰掛け is gone from the 升 quiz_exclusions (升.md:8) and from the ledger row (patch hunk at progress.json 333). The exclusion has no displayed-label basis. Titles "measuring box" and "seat; bench" share no meaning, and content-format.md lines 124/129 require evidence from displayed labels. JMdict 1346290 sense 2 is "box (seating at a theatre, etc.)" and 1288370 is "seat; bench", so the title of 升 shows only sense 1. Showing "seat; bench" as a wrong option is correct. The body at 升.md:28 keeps the contrast, as content-format.md line 115 allows. Word-quiz: 腰掛け is only one of 669 ties for the last slot, and 俵 is above it.
- O1 - RESOLVED - 升.md:28 is now two sentences. "[腰掛け] (こしかけ) is a seat or bench (JMdict entry 1288370). In its second sense, 升 is a whole box of seating, such as a 升席, not a single seat or bench." This is true against entries 1346290 sense 2 and 1706800 ("tatami box seat for four people"). It is short and readable on a phone. The wording differs from my suggestion, and the author's reason (a 升席 is one box for four people) is sound.
- N1 - RESOLVED (change accepted) - 皮 is removed from 匿's quiz_exclusions (匿.md:14) and from the ledger row. Titles "hide; shelter" and "skin; hide" share only an English homograph. Batch 130 notes say homographs alone do not compel guards, and the 峠 precedent (fix 3b6f9727) removed the same kind of exclusion. 匿 (distractors 父 魚 年) and 皮 (波 彼 坂, kanji\皮.md) have three curated distractors each. Neither card's question can therefore draw the other, and quiz-safety shows 匿 with father | fish | year. A third card's question that shows both as wrong options gains no second correct answer. 匿.md:40 still explains the contrast and makes no claim about the quiz. "Hide" meaning animal skin is not a sense of 匿.

New defects introduced by the revision: none established.

Verdicts:
- Correctness: CLEAN (匿.md:40, 升.md:28 against JMdict 1288370, 1346290, 1706800; 勲章 "honor" is spelling only).
- Scoped coverage: CLEAN (the contrasts stay in both bodies; line 34 of 升 still cites 1288370).
- Consistency and quiz safety: CLEAN (front matter matches the ledger hunks at progress.json 333 and 430; no exclusion also appears as a distractor; no question gains a second correct answer). I checked 匿 and 升 only; the other eight cards are unchanged from ccc046bb, and I did not re-audit their options.
- Comprehensibility: CLEAN (the split sentence reads easily; "a whole box of seating" is understandable with the 升席 example).

Confirmation: CONFIRMED

Findings: none

Optional: none

Second-pass verification (changes nothing above, strengthens it):
- Ledger: the word-exclusion row for 升 (lines 327-337) is exactly [箱, 容器, 入れ物, ケース, 計る, 測定, 計, 容積] and the kanji-exclusion row for 匿 (lines 427-435) is exactly [隠, 秘, 密, 潜, 伏]; both match the front matter. The ledger's quizzed-reading rows for 匿 (トク) and 升 (ます) and the distractor rows (匿 父/魚/年) match the cards.
- 勲章.md in full: title "decoration; order; medal", "honor" spelling now matches kanji\勲.md; the rest is consistent with its exclusions and its single JMdict citation.
- 腰掛け.md: title "seat; bench"; its own quiz_exclusions do not list 升, so no exclusion remains in either direction.
- QuizBuilder.kt (kanji): excluded(a, b) is symmetric (b in a's list or a in b's list). tryAdd rejects a candidate excluded against the target or against any already chosen option, and the card's own distractors are added first (three fill all wrong slots). So 匿 and 皮 cannot meet in either card's question (curated 父 魚 年 / 波 彼 坂), and in a third card's question the removal means both can appear together as wrong options; both are wrong for that card. Confirmed.
- Words.kt (word): same symmetric excluded(); curated distractors are capped at count-2 so one scored slot remains. score = 2 x shared tags + 1 for the same type + 1 for a shared kanji. For 升 vs 腰掛け: shared tags wago and noun = 4, same type wago = 1, no shared kanji, so 5, which matches the 5 reported in word-quiz.txt (俵 = 7 above it, 669 words tied at 5). 腰掛け can now be offered as a wrong option for 升 (probability about 1 in 669 per slot, not deterministic); it is a wrong answer for "measuring box". In the reverse direction 升 scores 5 for 腰掛け while furniture/posture words score higher, as the author said; even if drawn, 升 "measuring box" is wrong for "seat; bench". Confirmed.
No disposition or verdict changes.

Limits: Reviewed from the packet only. I could not run the Kotlin app or the audits, and I did not open the reading-options check or the reading code, so the reading prompts are not assessed by me. Random draws among the tied candidates are not shown deterministically; I checked the scoring arithmetic for 升/腰掛け only, not the whole word pool. I did not independently check the "186 vs 8" honor/honour counts or the 3b6f9727 history beyond the quoted excerpts. Execution limits: in the first pass I issued two tool calls in parallel once (word-quiz.txt lines 1688-1712 with changed-lines.txt); in the second pass I did so again (two edit calls in one response). In the second pass I also created and then deleted a stray placeholder file (claude.md.new) in the report folder by mistake; the folder now holds only claude.md.
