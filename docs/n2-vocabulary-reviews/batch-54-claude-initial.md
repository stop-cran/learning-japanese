# Batch 54 review: N2:1062–N2:1081

I found six minor defects in four articles: 調味料, 直前, 調節 and 散らかる. The other sixteen rows, the four kanji edits, the unchanged 短 card and all twenty mappings are CLEAN within the scope below.

## Snapshot
- Frozen commit: **a01a7787528d7f77f7c415d08747e06d75bb3dde**. Parent is 23d10580d5115175392fe407e21cba9fe94d4fd0, and the file says `cleanCommittedContent: true`.
- I reviewed committed content only.
- My tools can view files but cannot run Git or compute hashes. So I could not confirm the commit, the diff or any hash. The commit ID comes from the author's `batch-54-frozen-snapshot.json`.

## Scope
**Model:** claude-opus-5.5, family claude. I made no edits and used no agents.

**Ordering deviation:** I read `batch-54-review-evidence.json` (all of it) before `frozen-snapshot.json`, although the brief said to read the snapshot first.

**What I read in full:**
- **Private files:** frozen-snapshot.json, review-evidence.json, related.patch, principal-reading.txt, public-bodies.txt.
- **Guidance:** .github\copilot-instructions.md, .github\instructions\content-structure.instructions.md, docs\content-format.md lines 18–126.
- **Articles:** all 19 new articles and words\長短.md.
- **Kanji cards:** 線, 蔵, 貯, 角, 短.

**What I read partly or checked:**
- docs\n2-vocabulary-sources.tsv: only rows N2:1062–1081.
- docs\content-format.md: lines 929–934 (link rules) and a grep.
- docs\confusable-words.md: grep only; no batch words matched.

**Comparison articles:**
- Full bodies: 以前, 酢, 流れ, 支配, 次, 有利, 味噌, 管理, 末, 頭, 山, 最高.
- Titles, tags and exclusions grepped for about 90 more, including 食塩, しょうゆ, 塩, 以後, 以降, 前, ぱらぱら.
- I checked which component kanji cards exist. 整, 節 and 径 have none.

**One web fetch:** jisho.org/word/味噌, a third-party page built from JMdict.

**Not read:**
- Private files: review-mappings, components, labels and principals JSONL; family-inspection-01 to 07; supplement-comparison-reading.txt; public-bodies.json.
- Repository files: docs\n2-vocabulary-snapshot.json, docs\n2-source-snapshot.json, docs\jlpt-levels.md.
- All forbidden ledgers and batch-54.json.

**Other limits:** I did not fetch JMdict or Daijisen independently. The Daijisen text comes from the author's captures.

## Verdicts
**Convention:** quiz-exclusion, link and example-naturalness defects count under Correctness.

| ID | Article | New / reused | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1062 | words\長所.md | new | CLEAN | CLEAN | CLEAN |
| N2:1063 | words\長女.md | new | CLEAN | CLEAN | CLEAN |
| N2:1064 | words\調整.md | new | CLEAN | CLEAN | CLEAN |
| N2:1065 | words\調節.md | new | NEEDS FIX (F05) | CLEAN | CLEAN |
| N2:1066 | words\長短.md | reused; adds N2 level and sources only | CLEAN | CLEAN | CLEAN |
| N2:1067 | words\頂点.md | new | CLEAN | CLEAN | CLEAN |
| N2:1068 | words\長男.md | new | CLEAN | CLEAN | CLEAN |
| N2:1069 | words\長方形.md | new | CLEAN | CLEAN | CLEAN |
| N2:1070 | words\調味料.md | new | NEEDS FIX (F01, F02) | CLEAN | CLEAN |
| N2:1071 | words\チョーク.md | new | CLEAN | CLEAN | CLEAN |
| N2:1072 | words\直後.md | new | CLEAN | CLEAN | CLEAN |
| N2:1073 | words\直線.md | new | CLEAN | CLEAN | CLEAN |
| N2:1074 | words\直前.md | new | NEEDS FIX (F03, F04) | CLEAN | CLEAN |
| N2:1075 | words\直通.md | new | CLEAN | CLEAN | CLEAN |
| N2:1076 | words\直流.md | new | CLEAN | CLEAN | CLEAN |
| N2:1077 | words\貯蔵.md | new | CLEAN | CLEAN | CLEAN |
| N2:1078 | words\直角.md | new | CLEAN | CLEAN | CLEAN |
| N2:1079 | words\直径.md | new | CLEAN | CLEAN | CLEAN |
| N2:1080 | words\散らかす.md | new | CLEAN | CLEAN | CLEAN |
| N2:1081 | words\散らかる.md | new | CLEAN | CLEAN | NEEDS FIX (F06) |

**Kanji edits (all CLEAN):** each card links the new word in its reading row and Common words, and adds the JMdict entry to its sources line.
- **線:** 直線 ちょくせん at セン. Lines 30 and 46; entry 1431310 at line 54.
- **貯:** 貯蔵 ちょぞう at チョ. Lines 28 and 35; entry 1427220 at line 45.
- **蔵:** 貯蔵 ちょぞう at ゾウ. Lines 30 and 41; entry 1427220 at line 49.
- **角:** 直角 ちょっかく at カク. Lines 28 and 36; entry 1430800 at line 49. The small っ is explained from the whole-word reading, not invented as a separate kanji reading.

**Unchanged 短 (CLEAN):** it is not in the patch. Its タン row (line 28) and Common words (line 34) already link 長短 ちょうたん.

**Baseline kanji metadata (CLEAN):** the patch touches only body rows and the sources line; front matter is untouched. I could not check hashes. 整, 節 and 径 stay in word metadata without invented cards. The 節 link in 調節 points to the word article for ふし, which is correct.

**長短 (CLEAN):** only `jlpt: 2` and the JMdict 1430070 senses 1–2 and Daijisen source lines were added. The title, body and exclusions are unchanged.

**Mappings (CLEAN):**
- All 20 rows point to the right article and pinned entry, with the right selected and additional senses. For example, 頂点 selects sense 2 and adds 1, 3 and 4; チョーク adds entries 2854421 and 2854422; 直前 adds sense 2.
- Uses found only in Daijisen are credited to Daijisen, with no made-up JMdict sense numbers (直後 spatial, 直流 headings). The raw 長所 "(1)(2)" gloss correctly maps to one sense.

## Findings
**B54-F01**
- **Severity / facet:** Minor; quiz_exclusions.
- **Where:** words\調味料.md:9 (list at 34–37).
- **Problem:** The card excludes four seasonings (塩, 砂糖, 味噌, 胡椒) but not three others: 酢 "vinegar", 食塩 "table salt" and しょうゆ "soy sauce". 食塩 shares all four of 調味料's tags and 酢 shares three, so they are the app's most likely automatic distractors. They are exactly the same relationship as the excluded 塩 "salt".
- **Fix:** add 酢, 食塩 and しょうゆ to quiz_exclusions.
- **Evidence:** 酢.md:8 tags include `seasoning`, and 酢.md:15 calls vinegar "the sour seasoning". 食塩.md tags are [kango, noun, food, seasoning]. Daijisen's 調味料 entry lists 砂糖・味噌・醤油・塩・酢.
- **Confidence:** medium-high.

**B54-F02**
- **Severity / facet:** Trivial; linking.
- **Where:** words\調味料.md:37.
- **Problem:** "醤油 (しょうゆ)" is plain text, but words\しょうゆ.md ("soy sauce") exists. Text should stay plain only when the word has no card.
- **Fix:** link it to しょうゆ.md.
- **Evidence:** content-format.md:933.
- **Confidence:** high.

**B54-F03**
- **Severity / facet:** Minor; quiz_exclusions.
- **Where:** words\直前.md:9.
- **Problem:** 以前 "before; previously" is not excluded. Both cards are tagged kango and time, so 以前 is a likely distractor, and its body teaches "before; prior to" after a time word. The batch is also inconsistent: 直後 excludes 以後, and 直前 excludes 前.
- **Fix:** add 以前.
- **Evidence:** 以前.md:4, 8 and 16; 直後.md:9.
- **Confidence:** medium.

**B54-F04**
- **Severity / facet:** Minor; example naturalness.
- **Where:** words\直前.md:41–43.
- **Problem:** 目の直前を虫が飛びました is stiff, possibly unidiomatic. Daijisen glosses spatial 直前 as 「すぐ前。目の前」, so the usual phrasing is 目の前 or 目のすぐ前.
- **Fix:** use the attested pattern instead, e.g. 車の直前を横切りました (くるまのちょくぜんをよこぎりました), "crossed right in front of the car".
- **Evidence:** public-bodies.txt, 直前 sense 2: 「車の―を横断する」.
- **Confidence:** medium; this is not a native-speaker judgment.

**B54-F05**
- **Severity / facet:** Minor; quiz_exclusions.
- **Where:** words\調節.md:9 and 47–48.
- **Problem:** The title "regulation; adjustment; control" and 支配's "rule; domination; control" share "control", and "rule" is close to "regulation". The article itself admits English uses "control" for both. 管理 "management; control" is already excluded, which is inconsistent. Both cards are tagged kango.
- **Fix:** add 支配.
- **Confidence:** medium.

**B54-F06**
- **Severity / facet:** Trivial; comprehensibility.
- **Where:** words\散らかる.md:49.
- **Problem:** "Sparse raindrops or separate rice grains do not by themselves imply that disorder." This hints at ぱらぱら ("scattered pattering; loose separate grains") without naming it, so learners get an unexplained aside.
- **Fix:** name and link [ぱらぱら](ぱらぱら.md), or delete the line.
- **Confidence:** medium-high.

## Optional
- **頂点:** excluding 山, 頭 and 末 is broad. It is justified in the text (lines 42–45) and only removes distractors.
- **長所:**
  - Excluding 味噌 is harmless but unneeded, because its title is "miso paste". JMdict's key-point sense (#3) is real but usually written ミソ.
  - 有利 "advantageous" could be excluded (low confidence).
- **Possible further exclusions:** 直後 with 次; 直流 with 流れ.
- **長方形:30:** "both long vowels" could note that けい is usually also pronounced long.
- **Baseline text:** 長短 and 短 mention 長所 as plain text. It could now be linked, but those cards' teaching is meant to stay unchanged.
- **直角:** could mention 直角な; it already teaches 直角に.

## Limits
- I could not run Git or compute hashes, so I accepted the author's commit and baseline-equality claims without checking them.
- I did not independently fetch JMdict or Daijisen. Daijisen text is the author's capture from one dictionary service.
- I did not read the JSONL files, the seven family-inspection files, supplement-comparison-reading.txt, public-bodies.json, the two docs snapshot JSONs or jlpt-levels.md. Exclusion choices outside the articles I read in full or grepped may be missing.
- How natural the examples are has not been confirmed by a native speaker.
