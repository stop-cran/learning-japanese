Snapshot: commit 5bede460956a421ade851ece295ea87f21201c64 (revised snapshot; reviewed snapshot was 6b5934e7). Reviewer model: Claude, an Anthropic model. The exact version string is not visible to me. I am the reviewer who wrote reports-143\initial-claude.md and I worked alone and read-only.

Scope:
- This packet:
  - Read in full: INSTRUCTIONS.md, RESPONSE.md, CHANGES.md, diffs\fix.patch (lines 1-260, the whole patch), evidence\README.md, evidence\QuizBuilder.kt, evidence\joyo-item6.txt, evidence\weblio-dantsuku.txt, evidence\jmdict-cited-entries.xml (all 8 entries), checks\quiz-safety.txt, checks\link-targets.tsv and checks\reading-options.txt (all 233 lines).
  - Read in part: checks\reading-exposure.txt (lines 1-40: the pool definitions, 施 and 旋) and evidence\KanjiReadings.kt (lines 48-125: the question builder and excludedKeys, plus a grep for exclusion and distractor use).
  - The 12 revised cards in snapshot\kanji\, each read in full: 既 朗 旋 旦 旨 暑 条 架 柄 染 株 桜.
- The original packet (read-only):
  - The うまい entry 1310460, extracted from evidence\jmdict-families.xml with a script.
  - Lines of evidence\public-source\weblio-条.txt matching すじ, 難読, 訓, 条播 and 条彫.
  - A listing of evidence\app-code (no recursion).
- My initial report, read in full.
- Public web: the Digital Daijisen entry み‐ざくら【実桜】 on Weblio, fetched in full. A jisho.org search returned no usable content.
- Not opened: diffs\changed-lines.txt, the other check outputs (lint, unittest, validate, budget, vocabulary, manifest, linkplan, kanji-remarks), evidence\meta-scan.txt and meta_scan.py, evidence\Words.kt, evidence\word-remarks.json, evidence\kanji-remarks.json and evidence\kanjidic2-selected.xml. I did not reopen the unchanged cards 施 旗 暦 or any word article; for those I used quiz-safety.txt and reading-options.txt.

Dispositions:
- C1 - RESOLVED - 既.md:38 and 朗.md:43 now say "adds the traditional (Kangxi dictionary) form in parentheses". This matches 表の見方 item 6 (「丸括弧に入れて添えたものは，いわゆる康熙字典体である」, evidence\joyo-item6.txt). It is now consistent with 暦, 条 and 桜. No compatibility-ideograph wording remains in either card.
- C2 - RESOLVED - 桜.md:37 limits the whole-word caveat to 桜桃 read さくらんぼ and says that in 桜ん坊, 桜 is さくら + ん + 坊 (ぼ). JMdict 1298460 has 桜ん坊 and 桜桃 with the readings さくらんぼ and さくらんぼう. The ぼ statement is correct for the reading さくらんぼ.
- C3 - RESOLVED - "the fruit-cherry tree (ミザクラ, mizakura)" is a correct reading of the Daijisen sense. The 桜 sense reads 「２ 木の名。ミザクラ。」, and Daijisen's own み‐ざくら【実桜】 sense 2 is 「実をとるために栽培される桜。セイヨウミザクラなど。また、オウトウの別名」 (weblio.jp, fetched). Keeping "tree" is therefore better than my proposed "fruit cherry".
- C4 - RESOLVED - The ゼン row (染.md:34) and 染.md:40 now say that 染 is read ゼン in 愛染, an on reading outside the Joyo table, and the "does not establish" sentence is gone. 染.md:42 cites Daijisen and Kanjipedia, which matches weblio-染 「セン（慣） ゼン（漢）」 and kanjipedia-outside-readings. ゼン is still correctly outside the metadata: onyomi is [セン]. The reading audit shows that ぜん is not offered on the セン prompt: it is absent from the tier list, being a mutation of せん.
- C5 - RESOLVED - 旨.md:37 cites the separate うまみ entry. JMdict 1310520 has 旨み, 旨味 {ateji (phonetic) reading} and うま味 {search-only}. "旨 is read うま in both" is correct, and "not a reading to split" is gone. 旨.md:25 says JMdict spells the skillful sense 上手い or 巧い. JMdict 1310460 marks that sense "esp. 上手い, 巧い", so "spells" slightly hardens "esp.", but it is accurate enough for a learner and no longer implies 旨い.
- C6 - RESOLVED - 株.md:25 presents 守株 しゅしゅ as 守 シュ + 株 シュ, the stump-guarding fable, with the JMdict 1882040 glosses. The unchanged echo at 株.md:36 ("The standalone シュ word and 守株 are separate lexical identities") still reads correctly: they are separate JMdict entries, and the sentence no longer contradicts line 25.
- C7 - DECLINE ACCEPTED - In the shipped full pools the pair cannot occur:
  - quiz-safety.txt lists only 11 existing cards whose meaning prompts fall back (人 休 何 入 出 口 女 日 月 男 買), and 準, 範 and 規 are not among them.
  - QuizBuilder fills curated distractors first, so the 準, 範 and 規 prompts never reach the fallback that could draw 旗.
  - 旗 is not a starter card, so a Starter practice session drawn from the 118 starter cards plus the borrowed target cannot draw it either.
  - The 旗 prompt itself is filled by 施, 旋 and 旅.
  The residual risk exists only in a hypothetical pool that holds both 旗 and a 準, 範 or 規 target without that target's curated cards. The reason given for declining is sound, and I keep the point at no more than minor polish.
- C8 - RESOLVED - 旦.md:25 and 旦.md:52 now say that no ordinary JMdict word uses あした and that 一旦 is いっ + タン and contains no あした. 旦.md:41 writes だんな. The new line-34 gloss "husband (a slighting word)" matches JMdict 1634480 ("husband") and Daijisen 「「旦那」を軽んじていう語」 (evidence\weblio-dantsuku.txt).
- C9 - RESOLVED - 柄.md:48-49 now has two bullets, "え — handle; grip" and "がら — pattern; design". These match JMdict 1508290 (handle; grip) and 1508300 (pattern; design) and agree with lines 23 and 42. Both links resolve to words/柄.md (link-targets.tsv).
- O1 - DECLINE ACCEPTED - The すじ row follows JMdict's sense order and is clearly marked as not selected for questions. This was optional.
- O2 - RESOLVED (partly applied; the rest DECLINE ACCEPTED) - 条.md:58 says "an added horizontal stroke", which is correct for 未 and 末. Leaving the jargon paragraph untrimmed is an acceptable editorial choice. That paragraph does, however, contain a factual error; see Finding 1.
- O3 - RESOLVED - 架.md:25 uses 書架 しょか, bookshelf. This is in the Daijisen 架 extract and is also a Joyo example cited at 架.md:42.
- O4 - RESOLVED - 朗.md:51 names 月, 有 and 朝 as the distractors, which matches the front matter `distractors: [月, 有, 朝]`.
- O5 - DECLINE ACCEPTED - The word-article titles are outside this batch's scope.
- O6 - DECLINE ACCEPTED - No change was needed. This was my own judgement.
- O7 - DECLINE ACCEPTED - 雌雄異株 is the sourced Daijisen example, and 菌株 was only a suggestion.
- O8 - DECLINE ACCEPTED - Name readings need no account on the card. The reading audit shows あき and お cannot be drawn from the full pool.

Exclusion removals (not an ID; checked as requested):
- **旋 no longer excludes 凱.** 凱 "victory song; triumph" against 旋 "rotate; return; mediate": in either direction, neither title is a defensible answer to the other's prompt. The link is only the compound 凱旋.
- **既 no longer excludes 在, 存 and 有.** 在 "exist; be located", 存 "exist; be aware" and 有 "have, exist" against 既 "already; previously": no shared sense, and no defensible double answer in either direction.
- **How the change works in QuizBuilder.kt.** Exclusions are symmetric, and they also stop two mutually excluded cards from appearing together as wrong options. Removing these pairs can therefore only add options; it cannot remove a correct one. The new possibilities are:
  - 既 or 旋 drawn on a 在, 存, 有 or 凱 prompt;
  - the reverse;
  - 既 with 有, 在 or 存 side by side as two wrong options;
  - 旋 with 凱 side by side as two wrong options.
  All of these are harmless.
- **What the pools actually draw.** The 既 and 旋 prompts are filled 3/3 by curated cards (good; favorable | sun, day | bright, clear and carry out; give; alms | flag; banner; standard | journey, travel). None of 在, 存, 有 or 凱 is among the 11 fallback cards. So in the full pools the removal changes no drawn option.
- **Reading prompts are not affected.** The reading quiz (KanjiReadingQuiz) does not use quiz_exclusions; it excludes only the target's own on and kun keys and their mutations.

Verdicts:
- Correctness - NEEDS FIX (minor) - 条 (Finding 1, in unchanged text). The other 11 revised cards are CLEAN, and every changed hunk is correct.
- Scoped coverage - CLEAN - No changed hunk drops a reading or a needed word. The 柄 Common words section now covers both quizzed kun readings.
- Consistency and quiz safety - CLEAN - All 34 links on changed lines resolve, and the quoted glosses agree with their sources.
  - Meaning options: on all 15 prompts in quiz-safety.txt I found no pair with two defensible answers.
  - Exclusions: the remaining exclusions on 既 and 旋 are direct overlaps, and none is also a curated distractor.
  - Reading options: reading-options.txt reports 0 problems and every prompt fills three wrong options. No metadata reading or mutation is offered: for example ぜん is absent on the 染 セン prompt, and だん on the 旦 タン prompt. The only drawable unlisted reading is the KANJIDIC2 name-only ら (offered by 等) on the 柄 がら prompt; it was accepted at the initial round and is not an on or kun reading.
- Comprehensibility - CLEAN - The revised sentences in 旦, 旨, 暑, 柄, 株 and 桜 are plain and unambiguous for an N5-N4 reader.

Confirmation: NEEDS FIX - Every RESPONSE.md item is RESOLVED or DECLINE ACCEPTED. However, I established one new minor correctness defect, Finding 1. It is in text the revision did not touch.

Findings:
1. **Minor; correctness and consistency; 条.md:61.** I missed this in the initial round and found it on the full re-read of 条 required by this round.
   - **Claim:** After 条彫り すじぼり, 条播き すじまき and 発条 ばね, the card says "these spellings do not establish readings to split among the kanji. They are whole-word readings, not alternate character readings".
   - **Why it is wrong:** That holds only for 発条 ばね (gikun/jukujikun). In 条彫り and 条播き, 条 is the kun reading すじ followed by 彫り ぼり and 播き まき. Daijisen gives 条 「［訓］すじ」 and lists both words under 難読 because the すじ reading is unexpected, not because it is unsplittable.
   - **Impact:** The card's own すじ row (line 45) and line 47 say that すじ is used for 条 in some spellings, and line 61 then tells the learner that the two clearest such spellings do not show it. This is the same pattern as C2 and C6.
   - **Remedy:** Say that in 条彫り and 条播き, 条 is read すじ, and keep the whole-word caveat for 発条 ばね only.
   - **Evidence:** Original packet evidence\public-source\weblio-条.txt: 「［音］ジョウ…［訓］すじ」 and 「［難読］条彫(すじぼ)り・条播(すじま)き・発条(ばね)」. Daijisen headword すじ【筋／▽条】 sense 5 is 線.
   - **Confidence:** high.

Optional:
- 旨.md:25: "JMdict spells its skillful sense 上手い or 巧い" could say "usually spells", matching JMdict's "esp.".
- 株.md:36: now that line 25 explains 守株, the sentence "The standalone シュ word and 守株 are separate lexical identities" adds little and could be cut.
- 桜.md:37: could mention that JMdict also has the reading さくらんぼう (坊 read ぼう).

Limits:
- **Tool calls:** I made exactly one tool call per response and no parallel calls. I used no sub-agents and no background jobs.
- **Starter and padded sessions:** C7's undrawability rests on quiz-safety.txt's list of fallback cards and on the pool definitions in reading-exposure.txt. I did not see the app's session-assembly code for meaning quizzes. A Starter session that borrows several started cards at once was not modelled, and the audits cannot show it.
- **What the audits cannot show:**
  - Whether a fallback option is semantically defensible; I judged that from the titles.
  - Whether the exclusion removals matter in non-shipped or future pools.
  - The real app behaviour, since no JVM tests were run for this revision.
  - That quiz-safety.txt is unchanged by the front-matter edit: this is consistent with my analysis, but I did not compare it with the freeze output myself.
- **旦 あした claim:** "no ordinary JMdict word uses あした" for 旦 rests on my initial-round search of the packet's JMdict family entries. My one web attempt (jisho.org) returned no usable content.
- **Daijisen:** apart from 実桜, Daijisen claims rest on the frozen Weblio extracts.
- **Unchanged cards and word articles:** I did not re-read 施, 旗 or 暦, or the word articles. For those I relied on the quiz audits and my initial review.
