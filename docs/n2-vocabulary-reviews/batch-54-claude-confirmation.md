# Batch 54 confirmation review on the corrected snapshot (claude-opus-5.5)

## Snapshot
- **Corrected commit:** `1fcf2decfeb120c621058a587d18178f31c1f3ef`.
- **Parent:** `a01a7787528d7f77f7c415d08747e06d75bb3dde` (the original frozen commit, itself parented on `23d10580d5115175392fe407e21cba9fe94d4fd0`).
- **Committed content only.** My file tools cannot run Git, hash or cleanliness checks, and I did not inspect `.git`. The commit IDs, "clean committed content" and "only four files changed" are the author's claims. My own evidence is that the full correction patch matches the four committed articles.

## Scope
**Model:** claude-opus-5.5 (family claude). This is a resumed confirmation review, not a blind one. Both reviewers received the same adjudications.

**Read in this phase:**
- `batch-54-correction-snapshot.json`, read first.
- The full `batch-54-correction.patch`.
- Complete rereads of `words\散らかる.md`, `words\調味料.md`, `words\直前.md`, `words\長方形.md`, and the unchanged `words\調節.md`.
- All of `correction-comparisons-compact.txt`: 22 families, and I counted 51 senses.
- All 12 old bodies in `correction-existing-reading.txt`: 汚い, ぐしゃぐしゃ, 酢, 食塩, しょうゆ, 以前, 支配, ぱらぱら, 有利, 次, 流れ, 最高.
- `correction-public-reading.txt` (the Daijisen 直前 heading).
- In `corrected-review-evidence.json`, only the start of `correctionEvidence` (lines 26115–26200) and the section from `currentQuizDeclarations` to the end of the file (28031 onward).

**Checks run in this phase:**
- **Quiz exclusions:** I grepped the exclusion lines of all 20 articles. The 16 guarded articles declare 68 pairs at the old commit and 74 now (+2 散らかる, +3 調味料, +1 直前). Nothing was removed, and the result matches `currentQuizDeclarations`.
- **Link targets:** I confirmed the targets exist (汚い, ぐしゃぐしゃ, ぱらぱら, 以前, しょうゆ, 酢, 食塩) and grepped their title, tags and exclusion lines.
- **Seasoning tags:** only 胡椒, 調味料, 酢 and 食塩 carry the tag, and all three ingredient cards among them are now excluded from 調味料.
- **Other lines:** I spot-read 長所:40-52 and grepped 散らかす for its mess/dirt lines.
- **Source rows:** I re-read all 20 TSV rows N2:1062–N2:1081 in full.
- **Kanji reciprocity:** I re-grepped the reading-row and Common-words lines in 線, 貯, 蔵, 角 and 短.
- **Repository snapshots:** I read only the header lines of `n2-vocabulary-snapshot.json` and `n2-source-snapshot.json`; they contain no row-level batch-54 data.

**Inherited from my initial full reads (not reread now):**
- The other 15 new articles.
- The reused 長短 article.
- The five kanji cards, `related.patch`, `principal-reading.txt` and `public-bodies.txt`.
- The guidance documents (`.github\copilot-instructions.md`, `content-structure.instructions.md`, `docs\content-format.md:18-126`).
- The original `review-evidence.json` (read initially, in the wrong order, as I disclosed then).

**Never read:**
- The review JSONL files, `family-inspection-01` to `07`, `supplement-comparison-reading.txt`, `public-bodies.json` and `docs\jlpt-levels.md`.
- I did not view the remainder of `corrected-review-evidence.json` beyond the two ranges above.
- No forbidden ledgers, report folders or `batch-54.json` were read.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1062 | words\長所.md (new) | Unchanged; initial judgment kept, lines 40-52 spot-reread | CLEAN | CLEAN | CLEAN |
| N2:1063 | words\長女.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1064 | words\調整.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1065 | words\調節.md (new) | Unchanged; fully reread | CLEAN | CLEAN | CLEAN |
| N2:1066 | words\長短.md (reused; N2/provenance only) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1067 | words\頂点.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1068 | words\長男.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1069 | words\長方形.md (new) | Changed; fully reread | CLEAN | CLEAN | CLEAN |
| N2:1070 | words\調味料.md (new) | Changed; fully reread | CLEAN | CLEAN | CLEAN |
| N2:1071 | words\チョーク.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1072 | words\直後.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1073 | words\直線.md (new) | Unchanged; initial judgment kept, 線 links rechecked | CLEAN | CLEAN | CLEAN |
| N2:1074 | words\直前.md (new) | Changed; fully reread | CLEAN | CLEAN | CLEAN |
| N2:1075 | words\直通.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1076 | words\直流.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1077 | words\貯蔵.md (new) | Unchanged; initial judgment kept, 貯/蔵 links rechecked | CLEAN | CLEAN | CLEAN |
| N2:1078 | words\直角.md (new) | Unchanged; initial judgment kept, 角 links rechecked | CLEAN | CLEAN | CLEAN |
| N2:1079 | words\直径.md (new) | Unchanged; initial judgment kept | CLEAN | CLEAN | CLEAN |
| N2:1080 | words\散らかす.md (new) | Unchanged; initial judgment kept, exclusion and 汚す lines re-grepped | CLEAN | CLEAN | CLEAN |
| N2:1081 | words\散らかる.md (new) | Changed; fully reread | CLEAN | CLEAN | CLEAN |

**Reciprocal kanji links: CLEAN.** I rechecked each one:
- 線: セン row at line 30 and Common words at line 46 link 直線 ちょくせん.
- 貯: チョ row at line 28 and Common words at line 35 link 貯蔵 ちょぞう.
- 蔵: ゾウ row at line 30 and Common words at line 41 link 貯蔵 ちょぞう.
- 角: カク row at line 28 and Common words at line 36 link 直角 ちょっかく.

**Unchanged 短: CLEAN.** The タン row at line 28 and Common words at line 34 still link 長短 ちょうたん.

**Baseline preservation: CLEAN, within the file-level limit.** The correction patch touches only four new word cards. No baseline word, kanji card, TSV row or coverage snapshot changed. Words with no kanji card (整, 節, 径) stay in metadata only, and no cards were invented for them.

**Mappings: CLEAN.** I re-read all 20 TSV rows in this phase. Every row is level 2, batch 54, status `draft`, and points to the correct article and entry. The selected and additional senses match what I verified initially:
- 頂点: sense 2, plus 1, 3 and 4.
- 調味料: plus 1623130:1.
- チョーク: plus 2854421:1-2 and 2854422:1-2.
- 直線: plus 2726190:1-2.
- 直前: sense 1, plus 2.
- 貯蔵: sense 1, plus 2.
- 長短: senses 1 and 2.

## Findings
**My original findings**
- **B54-F01 (調味料 should exclude 酢, 食塩 and しょうゆ): RESOLVED.**
  - Line 9 now adds 酢, 食塩 and しょうゆ, and line 49 cites the sources (1370270:1 vinegar, 1358410:1 table salt, 1595020:1 soy sauce).
  - The reasoning is "a seasoning" as a defensible broad answer, not a shared tag. No other card is seasoning-tagged or seasoning-named, so nothing is left out.
- **B54-F02 (link 醤油 to しょうゆ): RESOLVED.** 調味料:37 now reads `[醤油](しょうゆ.md)`. The target is kana-primary, and its body names 醤油 as the usual spelling.
- **B54-F03 (直前 should exclude 以前): RESOLVED.**
  - Line 9 adds 以前, and lines 36-37 contrast it accurately ("without requiring immediacy").
  - The evidence is 1155150:1 (suffix: before, prior to) and 1155150:2 (the past, previously), plus the old 以前 body.
- **B54-F04 (replace the insect example in 直前): RESOLVED.**
  - Lines 44-45 now read 車の直前を横断しました, which directly inflects the captured Daijisen sense-2 example 「車の―を横断する」.
  - I withdraw my earlier 横切る suggestion; it was not the attested wording.
  - I never established that the old sentence was ungrammatical. My concern was naturalness, and this is not a native-speaker certification.
- **B54-F05 (調節 should exclude 支配): WITHDRAWN.**
  - 1310270 senses 1-4 cover rule/domination, direction/management, governing influence and grammatical government. None of them means adjusting to a suitable level (1429240).
  - My original case rested on English "control", rule≈regulation, shared tags and the 管理 guard. `content-format.md` explicitly rejects tags and surface similarity as grounds.
  - 管理 overlaps 調節 in actual Japanese collocations (温度管理 / 温度調節). 支配 has no comparable construction (\*温度を支配する).
  - The qualified distinction at 調節:47-48 stands, and N2:1065 correctness is now CLEAN.
- **B54-F06 (name ぱらぱら in 散らかる): RESOLVED.**
  - 散らかる:51-52 now names and links ぱらぱら, and line 56 cites 1102580:1,3-4.
  - The only overlap is English "scattered", so a guard is not required.
- **長方形 "both long vowels" (my optional note): RESOLVED.** Line 30 now reads "Read チョウ + ホウ + ケイ." No regression.

**Consequential qualifications**
- **長所/味噌 (my initial "unneeded" note): REVISED.**
  - 味噌 has an ordinary secondary sense "key point; good part" (usually spelled ミソ), so in the English-to-Japanese direction it can plausibly answer "merit".
  - Keeping the guard follows the project's rule on secondary senses. I withdraw the "unneeded" rationale.
  - 長所:46-47 already explains the distinction.
- **GPT N2-54-GPT-01 (散らかる/汚い and /ぐしゃぐしゃ): AGREE.**
  - Sources 1178940:2 (messy, untidy) and 2097580:3 (messy, untidy, disorganized), and both old bodies, support ordinary untidiness.
  - The new guards and the line 41-42 comparison are accurate.
  - Not extending this to 散らかす is defensible; the parts of speech differ (verb versus adjective/mimetic).
- **Remaining hypotheses: NOT ESTABLISHED, agree with the author.**
  - 長所/有利: 1605720 is a favorable-position na-adjective (\*長所な条件 is impossible).
  - 直後/次: 1316380 is about sequence (次の電車 versus 食事の直後), and じ (1579580) has no article.
  - 直流/流れ: 1552130:1 is a fluid or gas current, not electrical.
  - 頂点/最高 (1293850): 最高 is about evaluation and degree, not the summit/vertex meaning of 頂点.

**Regression check:** I found no regressions in the four changed articles:
- All new links resolve.
- Each new pair is declared once, so nothing is duplicated.
- Attributions match the families I read.
- No baseline text was touched.

**New defects:** none.

## Optional
- 散らかる:41-42: the "also" right after the 汚れる sentence is slightly ambiguous. A part-of-speech cue such as 部屋が汚い versus 部屋が散らかっている would help.
- 散らかす/汚い and /ぐしゃぐしゃ guards: low priority.
- 長所:46: mention that the key-point sense is usually written ミソ.
- Carried over unchanged from my initial review: 頂点's 11-entry exclusion list is broad, 直角な usage, and linking 長所 from 長短/短.

## Limits
- I ran no Git, hash or cleanliness checks; the snapshot identity and "unchanged elsewhere" are author-executed claims.
- The 直前 example is backed only by the author's original Daijisen capture. I made no fresh dictionary retrievals in this phase; my only fetch overall was jisho 味噌, in the initial phase.
- There are no native-speaker certifications and no runtime quiz draws.
- The judgments for the 15 unchanged articles, 長短 and the five kanji cards are inherited from my initial reads, not fresh full rereads.
- The unread files listed under Scope remain unread. The author's corrective-read totals are their counts, not mine.
- In the initial phase I read `review-evidence.json` before `frozen-snapshot.json`, contrary to the required order.
