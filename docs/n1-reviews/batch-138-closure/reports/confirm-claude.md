# Batch 138 — confirmation review (reviewer 1)

Snapshot: commit acf7297ef66a82f620a6c5551d95a2e3fa356bc7 (revised from the reviewed b6020f9e490298de1756e33c51bf9ce314132f4e). Reviewer model: Claude (Anthropic model family), working alone and read-only. I did not look for or see the other reviewer's report.

Scope:
- This packet, `C:\Users\romanko\n1-kanji-workspace\review-packets\confirm-138-claude`:
  - Read in full:
    - `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`.
    - All 10 revised cards in `snapshot\kanji\`: 契 奏 堅 妨 壊 威 執 垣 塊 奪.
    - `evidence\kanjipedia-契.txt`, `evidence\weblio-押妨.txt`, `evidence\stroke-summaries.txt`, `evidence\QuizBuilder.kt`, `evidence\KanjiReadings.kt`.
    - `evidence\jmdict-cited-entries.xml`. A script parsed all 8 entries and printed their kanji forms, readings, tags and sense glosses: 1204780, 1257110, 1319610, 1416340, 1509290, 1590410, 2080870 and 2714430.
    - `checks\quiz-safety.txt`, `checks\link-targets.tsv`.
  - Read in part:
    - `diffs\changed-lines.txt`, in full (it is short).
    - `diffs\fix.patch`: only the `diff --git` and `@@` headers, checked against `changed-lines.txt` and `CHANGES.md`. Each hunk's content was checked through the revised cards and the old/new text quoted in `CHANGES.md`. I did not read the patch body itself.
    - `checks\reading-exposure.txt`: lines 1–3 and the last 4 lines.
    - `checks\reading-options.txt`: line 1, lines 11–21, lines 155–163, and a grep for HIT/problem.
  - Not opened:
    - `evidence\README.md`, `evidence\Words.kt`, `evidence\meta_scan.py`, `evidence\meta-scan.txt`.
    - `checks\lint.txt`, `checks\unittest.txt`, `checks\validate.txt`, `checks\budget.txt`, `checks\vocabulary.txt`, `checks\manifest.txt`.
- Original packet `batch-138-b6020f9e`, read-only:
  - `evidence\kanjipedia-outside-readings.json`: grep of the 契 record.
  - `titles\kanji-titles.tsv`: lookup of 組 魅 壁 衣 十 女 塀.
  - `evidence\public-source\weblio-{噴,垂,壁,墨,奪}.txt`: the ［音］/［訓］ segment of the Daijisen block.
- My own initial report, from context. I did not reopen the file.
- Public web: the live Kanjipedia 契 page, https://www.kanjipedia.jp/kanji/0001765100. It matches the packet extract: [音] ケイ [外]キツ・ケツ; [訓] ちぎる [外]きざむ・わりふ; [二]キツ「契丹」; [三]ケツ ②久しく会わない「契闊(ケッカツ)」. セツ appears only in the なりたち (formation) note.

Dispositions:
- C1 - RESOLVED - `堅.md:41` now says 硬い and 固い are "two other spellings" and adds "that entry also lists 緊い, marked as irregular kanji usage". JMdict 1257110 lists 硬い, 固い, 堅い and 緊い, and 緊い carries "word containing irregular kanji usage". Line 23 ("JMdict lists 堅い in one entry with the spellings 硬い and 固い") does not claim that the list is complete, so it does not contradict the fix.
- C2 - RESOLVED (the part about セツ: DISPUTE ACCEPTED) - The whole-word claim is gone from `契.md:43`.
  - The new line explains きっ as キツ with gemination. It attributes キツ (契丹, "国の名") and ケツ (契闊, "久しく会わない") to Kanjipedia as outside-table readings, and both are on the live page.
  - It says KANJIDIC2 lists neither reading; KANJIDIC2 gives only on ケイ. It says JMdict 2714430 also reads 契丹 as けいたん; the entry has きったん, けいたん, キタイ and キタン.
  - The author is right that my initial report mis-stated the source of セツ. `kanjipedia-outside-readings.json` lists 契 on readings ケイ, キツ and ケツ, and no セツ. On Kanjipedia, セツ occurs only in the etymology note. Daijisen's せつ【契】 is a headword for a proper name, the legendary Xie, not a reading used in words. Leaving it out is defensible.
- C3 - RESOLVED - `妨.md:25` now names both Daijisen examples, 妨害 and 押妨 (original packet `weblio-妨.txt`: 「妨害／押妨」).
  - The gloss "a historical term for breaking into another's domain to commit violence or impose unjust taxes" matches Daijisen おう‐ぼう【押妨】 (他人の所領などに押し入って乱暴を働いたり、不当な課税をしたりすること, with a 平家 citation) and the 歴史民俗用語辞典 entry.
  - The reading おうぼう is correct; Daijisen also gives おうほう.
- C4 - RESOLVED (the author's wording, not my suggested remedy, is correct) - `壊.md:27` now says "十 … at the top, a box-like 罒 in the middle and the full shape of 衣 … at the bottom".
  - `stroke-summaries.txt` shows that 壊 strokes 11–16 have the same KanjiVG stroke types, in the same order, as 衣 strokes 1–6 (㇑a ㇐ ㇒ ㇙ ㇒ ㇏).
  - Stroke 11 starts at y 50.8, below 罒 (strokes 6–10, y 30.0–49.9). Strokes 4–5, a horizontal and a vertical, form the 十.
  - My suggestion of "a split 衣" was wrong for the modern shape.
- O1 - RESOLVED - `威.md:33` now gives "a long horizontal stroke on top" and "inside it sit a short horizontal stroke and 女". The stroke data agree: stroke 2 is 56.5 wide at y≈28–34, and stroke 3 is 23.7 wide at y≈46–49. The rest of the frame also matches: stroke 1 is the left sweep ㇒, and strokes 7–9 are the hooked ㇂, the slash and the dot.
- O2 - RESOLVED - `威.md:44` now says "威張る mixes an on reading and a kun reading: 威 supplies い, its KANJIDIC2 on reading イ, and 張 supplies ば". This is consistent with Daijisen い‐ば・る〔ヰ‐〕, whose historical kana ヰ is 威's on reading. The contradiction is gone.
- O3 - DECLINE ACCEPTED - The armor sense belongs to the word 縅 おどし, in which 威 is an alternative spelling (JMdict 2581990; Daijisen おどし【▽威／×縅】). It is specialist vocabulary. The おど.し row correctly keeps 威し "threat", and nothing on the card is wrong without it.
- O4 - RESOLVED - `執.md:43` adds 執り行う とりおこなう, "to hold (a ceremony); to perform", which matches JMdict 1319610 (kanji form 執り行う, reading とりおこなう). Entry 1319610 is added to the Metadata line (line 58).
- O5 - DECLINE ACCEPTED - Daijisen's 噴 entry lists only ［音］フン（慣） ［訓］ふく, and KANJIDIC2 lists only フン and ふ.く. ホン and は.く are Kanjipedia-only readings, so leaving them out fits the stated batch rule. The reading audits show them as latent only.
- O6 - DECLINE ACCEPTED - Daijisen's 垂 ［訓］ list is たれる, たらす, しだれる, しずる and なんなんとする, with no しで. JMdict 1767000 gives 垂 only as a minor spelling of しで, whose main spelling is 四手. 垂 is the batch's longest card.
- O7 - DECLINE ACCEPTED - 壁 がけ, 墨 モク and 奪 タツ are in neither KANJIDIC2 nor the Daijisen ［音］/［訓］ lists: 壁 ヘキ/かべ, 墨 ボク/すみ, 奪 ダツ/うばう.
- O8 - RESOLVED - `奏.md:31` adds 功を奏する こうをそうする, "to succeed; to bear fruit", as an example of the third Daijisen sense, achieving a result. This matches JMdict 2080870, whose single sense is exactly that gloss. The sense order on the card (report to a ruler, play, achieve) matches that claim. Entry 2080870 is added to the Metadata line (line 59).
- O9 - DECLINE ACCEPTED - This is tooling, not card content. Keeping the tools unchanged keeps their output comparable with the original packet. The note in `CHANGES.md` states the model difference correctly.

Verdicts:
- Correctness: CLEAN. Every changed hunk was checked against JMdict, Kanjipedia (live), Daijisen extracts and the stroke data. No changed hunk contradicts untouched text on any of the 10 revised cards.
- Scoped coverage: CLEAN. 契 now accounts for キツ and ケツ. The declined readings fall outside the stated rule (KANJIDIC2 plus the Daijisen ［音］/［訓］ lists), and I checked that this is so.
- Consistency and quiz safety: CLEAN.
  - All 21 links on changed lines resolve, and every quoted gloss equals its target title. I independently confirmed 壁 "wall; barrier", 組 "group; assemble", 魅 "charm; bewitch", 衣 "clothing; garment", 十 "ten", 女 "woman, female" and 塀 "boundary wall; fence" in `kanji-titles.tsv`.
  - The new exclusion pairs are real direct pairs, and none of them is also an authored distractor of either card in the pair:
    - 垣–壁: JMdict 1204780 sense 2, "barrier; wall", against 壁's title.
    - 奪–魅: JMdict 1416340 sense 2, "to fascinate; to captivate; to charm".
    - 塊–組: JMdict 1590410 sense 2, "group; crowd".
  - 魅 stays a distractor of 塊, which is a different pair.
  - `QuizBuilder.excluded` is symmetric, so a declaration on one card covers both directions.
- Comprehensibility: CLEAN. The new sentences are short, explain their terms (gemination, okurigana) and keep the central idea first.

Confirmation: CONFIRMED

Findings: none.

Quiz options for all 15 cards (post-fix):
- **Meaning quiz.** `checks\quiz-safety.txt` shows three wrong options for every card. Each is defensibly wrong against the displayed title in both directions, for example 塊 "lump; clod; mass" against "charm; bewitch | castle | place, site", and 奪 "snatch; rob; deprive" against "gather | falcon | miscellaneous". The curated distractors fill all three slots for every batch card. The 11 older cards it lists with 2/3 curated slots (人, 口, 買 and others) predate this batch and are outside its scope.
- **Reading quiz.** `KanjiReadingQuiz.question` adds the curated distractors' readings first and uses the closeness-ranked fallback only for slots still empty. Every reading of the target in either kind, and its voicing, long-vowel and small-っ variants, are excluded from the wrong options. For the batch prompts, the curated readings fill all three slots whenever the distractor cards are in the pool:
  - For 噴 フン, the reading-options simulation sees only the 4 curated keys こう, く, こ and ばい.
  - For 契 ケイ, it sees only the 6 curated keys だい, たい, てん, ぶん, ふん and ぶ.
  - So the two "HIT" labels (噴 ほん, 契 けつ) cannot occur while those distractors are present. This agrees with `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 8 latent collisions.

Optional:
- 契.md:43 writes 契闊 ケッカツ in katakana, as Kanjipedia prints it. Every other word reading on the card is in hiragana (けいやく, ちぎる, きったん), so けっかつ would be more consistent. This is a matter of style only.

Limits:
- **What the audits cannot show.** `reading-exposure.txt` models the N1 and All stack pools and the Starter practice session only. In a custom or other filtered pool that lacks a target's curated distractor cards (for 契: 大, 天 and 分), the fallback fills the empty slots. If my reading of the code is right, けつ would then be a closeness-3 candidate for 契 ケイ. It is the on reading ケツ, which the card now names as an outside-table reading, so the app could mark a real reading wrong.
  - ほん for 噴 フン is a closeness-4 candidate in the same way.
  - Neither tool models such pools. I treat this as a latent risk already covered by O9, not an established defect.
  - The meaning-quiz audit likewise does not model fallback composition in custom pools.
- The Android JVM content tests and the Kotlin cross-check of the reading audit were not run at this snapshot (`CHANGES.md`).
- I did not open `evidence\Words.kt`, so I did not verify the exact mutation set (`ReadingOptions.mutations`). I also did not open the lint, unittest, validate, budget, vocabulary or manifest outputs, and I take their summaries in `CHANGES.md` on trust.
- I did not read the body of `fix.patch`. I relied on the hunk headers, `changed-lines.txt`, the old/new text quoted in `CHANGES.md`, and full reads of the revised cards, so a change outside those headers would not be caught. The headers match the stated changed lines exactly.
- I did not check whether JMdict 2080870 carries a frequency (priority) tag, which would support the card's word "common" for 功を奏する. This is editorial wording, and the phrase is in frequent written use.
- I accepted the stroke-summary file's arithmetic (computed from KanjiVG) without recomputing it from the raw stroke JSON. Its figures agree with what I saw in the first round.
- Every response in this round contained exactly one tool call.
