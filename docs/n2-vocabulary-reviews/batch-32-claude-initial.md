## Snapshot
Frozen commit **f6d1ef9efca4ffa026bcdb0fe4eb4e768ade64c8** (parent dd03c892652a0deb17b1261dd10e0fb33d5328b8). I reviewed committed content only, but I had file tools and no Git or hashing. I couldn't confirm that the working-tree files match the commit, so I assumed they do.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked alone and changed no files.
- **Read in full:**
  - all 17 new articles
  - the 3 reused articles (再来月, 再来週, 再来年)
  - the four-file related patch and the edited 布, 団, 角 and 算 kanji cards
  - mapping rows N2:622 to N2:641
  - the rules files listed in the request
- **Evidence:** the relevant records in the evidence packet (rows, entry families, comparison labels, quiz declarations, failed lookups and access limits) and the full comparison-reading file (123 families). I also read existing words and kanji to check links and quiz titles.
- **Not read:** batch-32.json, the forbidden review and notes docs, author-check receipts and other reviewers' output. My searches stayed inside the assigned files, `words\`, `kanji\` and the allowed evidence.

## Verdicts

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 撮影 | CLEAN | CLEAN | CLEAN |
| 雑音 | CLEAN | CLEAN | CLEAN |
| さっさと | NEEDS FIX (B32-QZ-01) | CLEAN | CLEAN |
| 早速 | CLEAN | CLEAN | CLEAN |
| 錆 | CLEAN | CLEAN | CLEAN |
| 錆びる | CLEAN | CLEAN | CLEAN |
| 座布団 | CLEAN | CLEAN | CLEAN |
| 冷ます | CLEAN | CLEAN | CLEAN |
| 妨げる | CLEAN | CLEAN | CLEAN |
| 冷める | CLEAN | CLEAN | CLEAN |
| さようなら | CLEAN | CLEAN | NEEDS FIX (B32-RG-01) |
| サラリーマン | CLEAN | CLEAN | CLEAN |
| 騒がしい | CLEAN | CLEAN | CLEAN |
| さわやか | CLEAN | CLEAN | CLEAN |
| 三角 | CLEAN | CLEAN | CLEAN |
| 算数 | CLEAN | CLEAN | CLEAN |
| 酸性 | CLEAN | CLEAN | CLEAN |

**Reuse claims (N2:633 to N2:635): all CLEAN on correctness, coverage and comprehensibility.**
- 再来月 (N4), 再来週 (N4) and 再来年 (N5) already teach the exact spelling, reading and calendar meaning at easier levels.
- The patch doesn't touch any of them.

**Kanji edits: all four CLEAN.**
- New examples: 布.md:42 and 団.md:42 add 座布団 (ざぶとん), 角.md:36 and :42 link 三角, and 算.md:40 adds 算数.
- Every reading row is still there.
- 座, 雑, 冷, 性 and 数 are N3 or easier, so they don't need reciprocal examples.
- 撮, 影, 錆, 妨, 騒, 酸 and 爽 have no kanji cards. They correctly stay as metadata, and no kanji files were invented for them.

**Mappings (N2:622 to N2:641): all 20 CLEAN on spelling, reading and selected senses.** Three need a note:
- **N2:626 (錆):** the raw gloss "rust (colour)" is kept as a source label. The article doesn't present it as a sense of this entry and points to the separate entry 錆色.
- **N2:624 (さっさと):** only JMdict supports it, because the public lookups failed. The mapping says so itself.
- **N2:623, N2:631 and N2:640:** these list extra senses. Each is taught as a secondary meaning, not given N2 status of its own.

## Findings

**B32-QZ-01: a missing quiz exclusion lets two correct answers appear**
- **Severity:** Minor
- **Facet:** correctness (quiz)
- **Where:** words\さっさと.md:4 and :9, and words\すっと.md:4 and :15
- **Problem:** さっさと is titled "quickly; without hesitation" and すっと "swiftly; smoothly". Neither file excludes the other. "Quickly" and "swiftly" are near-synonyms in English, and すっと.md:15 even says "often without hesitation". A quiz could therefore offer two answers that both look right.
- **Inconsistency:** さっさと already excludes weaker matches such as すたすた, 急速 and どんどん.
- **Evidence:** JMdict 1006140 sense 1 for すっと (via Jisho) reads "straight, quickly, directly, all of a sudden".
- **Fix:** add すっと to さっさと's `quiz_exclusions`. One side is enough because exclusions are symmetric.
- **Confidence:** medium-high. すっと's entry isn't in the evidence packet, and Jisho may use a different JMdict version.

**B32-RG-01: the article never says when さようなら is the right goodbye**
- **Severity:** Minor
- **Facet:** comprehensibility (register)
- **Where:** words\さようなら.md:18 and :34
- **Problem:** the article says "Choose a farewell for the relationship and situation" but gives no usable guidance. Learners may then say さようなら to colleagues or friends every day.
- **Fix:** add one sentence stating the tendency, not a rule. さようなら is typical of school partings, formal partings, and partings expected to be long or final. Adults leaving work or friends usually say お先に失礼します, お疲れ様です, じゃあね or またね.
- **Confidence:** medium. This is widely taught. JMdict gives no register flag, and I couldn't find public support (see Limits). It could fairly be moved to Optional instead.

## Optional
These are nonblocking polish suggestions:
- 雑音 "noise; interference" and じゃま "hindrance; interference" share "interference" in their titles. The first glosses tell them apart. Retitling 雑音 to "noise; static" would remove the overlap.
- 錆.md:16 uses 自転車の鎖. 自転車のチェーン is more natural, and 錆びる.md already uses チェーン.
- さわやか could add 弁舌さわやか for its "clear speech" sense.
- 妨げる could add the noun 妨げ and the pattern ～の妨げになる.
- 三角 could note that 三角形 is also read さんかっけい.
- 錆 could add 身から出た錆. 錆びる could add the figurative 腕が錆びる, labelled as outside the source sense.
- さっさと could mention commands such as さっさとしなさい.

## Limits
- I couldn't run Git or hashes, so the snapshot match and evidence equivalence come from the author's receipt.
- すっと and 賑やか are outside the comparison packet. I checked them only through the existing articles and Jisho.
- I found no public source confirming さようなら's register.
  - The Weblio page cited in the article as "Digital Daijisen" showed only Wikipedia-derived text in my fetch. That text supports the さようならば etymology, not register.
  - Tofugu returned 404, and Kotobank searches came back irrelevant.
- I had no public lexical source for さっさと beyond JMdict.
- I didn't consult the N5 to N3 source indexes. I only confirmed that no さよなら or other easier article exists.
- There was no native-speaker review, and no quiz draws were run.
- CLEAN means no actionable defect was found within this scope.
