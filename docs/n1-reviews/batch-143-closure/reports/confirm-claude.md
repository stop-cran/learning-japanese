# Confirmation review: batch 143 (reviewer 1, confirmation round)

Snapshot: commit 9b8f50a8b9ddb2123137573ccb26761e05954491 (reviewed snapshot 6b5934e7). Reviewer model: Claude (Anthropic model family). I cannot verify my exact version from inside the session. I worked alone and read-only.

Scope:
- Confirmation packet, read in full: INSTRUCTIONS.md, RESPONSE.md and CHANGES.md.
- `diffs\fix.patch`: all 251 lines, read in ranges. I also read `diffs\changed-lines.txt`.
- Revised cards: I read all 12 changed cards in full in `snapshot\kanji\` (旋 既 旦 旨 暑 朗 条 架 柄 染 株 桜).
- `checks\quiz-safety.txt` and `checks\link-targets.tsv`: full.
- `checks\reading-options.txt`: lines 1-60, 62-75 and 190-233 in full, plus every prompt, unlisted-reading, note and simulation line for the other cards.
- `checks\reading-exposure.txt`: the command line, the pool definitions and the 桜 section, plus the summary lines.
- Evidence, read in full: `evidence\README.md`, `QuizBuilder.kt`, `joyo-item6.txt`, `weblio-dantsuku.txt` and `jmdict-cited-entries.xml`.
- Evidence, read in part: `KanjiReadings.kt` and `Words.kt` (a grep for how exclusions and distractors are used, and `Words.kt` lines 220-242, the `mutations` function).
- Original packet: `evidence\public-source\weblio-架.txt`, and JMdict entry 1310460 extracted from `evidence\jmdict-families.xml`.
- My own initial report: full.
- Public web: Weblio/Digital Daijisen headword 実桜 (み‐ざくら).
- Not opened: lint, unittest, validate, budget, vocabulary, manifest, linkplan and kanji-remarks outputs; meta-scan and meta_scan.py; word-remarks.json and kanji-remarks.json; the three unchanged cards 施 旗 暦 (all unchanged, per the instructions).

Dispositions:
- C1 - RESOLVED - 既.md:38 and 朗.md:43 now say the table adds the traditional (Kangxi dictionary) form in parentheses. This matches 表の見方 item 6 (`joyo-item6.txt`: 丸括弧に入れて添えたものは，いわゆる康熙字典体である). No "compatibility ideograph" wording remains on either card.
- C2 - RESOLVED - 桜.md:37 limits the whole-word caveat to 桜桃 read さくらんぼ and says that in 桜ん坊, 桜 is さくら + ん + 坊 (ぼ). JMdict 1298460 has 桜ん坊 and 桜桃 with the readings さくらんぼ and さくらんぼう. 坊 = ぼ is right for the さくらんぼ form the card cites.
- C3 - RESOLVED - 桜.md:25 now says "fruit-cherry tree (ミザクラ, mizakura)". Daijisen's character entry has 「木の名。ミザクラ」. Daijisen's own headword み‐ざくら【実桜】, sense 2 (Weblio, fetched), reads 「実をとるために栽培される桜…オウトウの別名」, so "tree" is the correct reading of ミザクラ.
- C4 - RESOLVED - 染.md:34 and :40 say 染 is read ゼン in 愛染, an on reading outside the Joyo table, and the "does not establish an independent reading" sentence is gone. Line 42 credits Daijisen and Kanjipedia, which is consistent with weblio-染 (ゼン（漢）) and with JMdict 2583650.
- C5 - RESOLVED - 旨.md:37 cites the separate うまみ entry; JMdict 1310520 has 旨み, 旨味 {ateji (phonetic) reading} and うま味, and "not a reading to split" is gone. 旨.md:25 matches 1310460, whose skillful sense is marked `esp. 上手い, 巧い` (I checked the entry text).
- C6 - RESOLVED - 株.md:25 gives 守株 as 守 シュ + 株 シュ, the stump-guarding fable, with the JMdict 1882040 glosses. The echo at line 36 still reads correctly: they are two separate words.
- C7 - DECLINE ACCEPTED - In the audited pools the pair cannot occur. All three meaning slots on the 旗 prompt are curated (施 旋 旅). The 11 existing cards that fall back to tag-similar options (人 休 何 入 出 口 女 日 月 男 買) do not include 準, 範 or 規, so `QuizBuilder.options` never reaches the fallback on those prompts. The cost of a title change against a medium-confidence, minor concern is a reasonable ground for declining. The residual case is a padded or smaller session; see Limits.
- C8 - RESOLVED - 旦.md:25 and :52 now say plainly that no ordinary JMdict word was found that uses あした and that 一旦 is いっ + タン. 旦.md:41 writes だんな.
- C9 - RESOLVED - 柄.md:48-49 has `柄 え — handle; grip` and `柄 がら — pattern; design`. These match JMdict 1508290 (handle; grip) and 1508300 (pattern; design) and the card's own え/がら distinction.
- O1 - DECLINE ACCEPTED - The すじ row follows JMdict 筋's sense order and is already marked as not quizzed and without an article. This was optional polish.
- O2 - DECLINE ACCEPTED (partly applied) - 条.md:58 now says "an added horizontal stroke", which is correct for 未 and 末. The jargon paragraph was kept, but the rewrite of line 61 made it clearer (see the new-hunk check below).
- O3 - RESOLVED - 架.md:25 uses 書架 しょか. weblio-架.txt lists 書架 under sense 1 (物を載せるため…台。また、棚).
- O4 - RESOLVED - 朗.md:51 names 月, 有 and 朝 as the distractors, which matches the front matter.
- O5 - DECLINE ACCEPTED - The titles belong to word articles outside this batch's scope. 柄's line no longer copies "handle; pattern".
- O6 - DECLINE ACCEPTED - My own judgement was that no change was needed.
- O7 - DECLINE ACCEPTED - 雌雄異株 is the Daijisen example. 菌株 was only an optional extra.
- O8 - DECLINE ACCEPTED - Name-only readings need no account on the card. The audit shows あき and お cannot be drawn in any pool.

New hunks that answer none of my points:
- 旦.md:34: "a slighting word" matches Daijisen だん‐つく (「旦那」を軽んじていう語) and JMdict 1634480 (husband).
- 暑.md:36: "蒸 writes む and し is okurigana" is correct (蒸す むす; JMdict 1356870 蒸し暑い むしあつい).
- 条.md:61: 条彫り すじぼり and 条播き すじまき as 条 = すじ is consistent with Daijisen's kun reading すじ. Keeping the gikun/jukujikun caveat only for 発条 ばね is correct.
- Exclusions removed from 既 (在 存 有) and 旋 (凱):
  - In `QuizBuilder.options`, exclusions matter only in three cases: when a card is drawn as a fallback wrong option, through the mutual check among chosen options, or when they block a curated distractor.
  - The 既 and 旋 prompts are filled 3/3 by curated distractors (quiz-safety.txt). In the full pools, 在, 存, 有 and 凱 are not among the cards that fall back, so the removal changes no shipped meaning option.
  - In any smaller pool, a resulting pair would be one of: 既 "already; previously" against 在 "exist; be located", 存 "exist; be aware" or 有 "have, exist"; or 旋 "rotate; return; mediate" against 凱 "victory song; triumph". None of these pairs makes two answers defensible from the titles.
  - `KanjiReadings.kt` uses no `quiz_exclusions`, so the reading audits are rightly unchanged.

Verdicts:
- Correctness: CLEAN for all 12 changed cards. Every changed claim I checked is supported by the cited JMdict entries, the Daijisen extracts or the Joyo front matter.
- Scoped coverage: CLEAN. No reading or example was dropped. 柄 now lists both of its quizzed readings in Common words.
- Consistency and quiz safety: CLEAN.
  - All 34 links on changed lines resolve (link-targets.tsv).
  - The Notes sentences on 既 and 旋 match their reduced `quiz_exclusions`.
  - The post-fix meaning options for all 15 cards are three distinct, non-defensible wrong titles. On the 桜 prompt, "apricot" is a different tree, not a second answer.
  - The reading prompts show 0 problems. Unlisted readings are never drawable in the shipped pools. On the 染 セン prompt, ぜん is absent from the candidate list because it is a voicing mutation of せん, so the newly stressed ゼン cannot be offered as a wrong option.
- Comprehensibility: CLEAN. The 旦, 柄, 桜 and 株 rewrites are plainer than before.

Confirmation: CONFIRMED

Findings: none

Optional:
1. 条.md:61, "the kun reading in the table above": the preceding paragraph is about the official Joyo table, which does not list すじ. Writing "the kun reading in the Readings table above" would remove the ambiguity.
2. 株.md:36: since 守株 now appears only in the prose at line 25, the sentence "The standalone シュ word and 守株 are separate lexical identities" could go, or 守株 could be added to the シュ row.
3. 旨.md:37: JMdict's tag is "ateji (phonetic) reading". The card's gloss "kanji chosen for sound or sense" is a fair general definition, but the card could quote the tag instead.

Limits:
- Tool calls: I made exactly one tool call per response and issued no parallel calls. Early on, one command's output was too large for the tool, and the harness saved it to a temporary file automatically. I did not open that file; I re-read `fix.patch` in line ranges with the view tool.
- The audits do not show meaning-quiz options on prompts where an existing card draws 旗, 既 or 旋 as a fallback in smaller or padded sessions. Examples are a Starter "Practice more" session that borrows started cards from other stacks, or a test-sized pool. Whether the meaning quiz uses such padded pools is not shown in the packet. C7 is unverified for those sessions. For 既 and 旋 I reasoned from the titles alone that no defensible pair arises.
- I did not re-open the unchanged cards 施, 旗 and 暦 or the word articles. I took the lint, unittest, validate and manifest outputs on trust without reading them, and I did not run the app's JVM tests (none were supplied).
- I did not confirm two claims myself, which is my own limit: the negative claim "no ordinary JMdict word uses あした" for 旦 (I accepted it from my initial-round scan of the 旦 family entries), and that Kanjipedia records ゼン for 染 (I accepted it from the original packet's kanjipedia-outside-readings.json, which I read in round 1). The 守株 fable attribution rests on general knowledge and on JMdict 2834654, which I cited in round 1.
