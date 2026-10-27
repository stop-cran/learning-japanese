## Snapshot
I reviewed frozen commit **b0dcca6434845e2b41b0161a8f0249502b182e46** (parent 91b33ff51cd3d94c23a6162041cf10597e939f79), committed content only. I had file and web tools but could not run Git, so I could not confirm the commit, the diff or any hashes myself. Hash equivalence of the evidence file is the author's claim; I did not verify it.

## Scope
- **Model:** claude-opus-5.5 (Claude family).
- **New articles:** I read all 19 in full.
- **Related edits:** I read the six-file patch and looked at the changed passages in 区.md, 域.md, 律.md, 線.md, カーブ.md and 金魚.md. I only checked those passages, not the rest of each file.
- **金魚 reuse:** I checked only the goldfish identity and the new `jlpt: 2`. I did not re-review its existing teaching.
- **Mappings:** I checked TSV rows N2:402–421. They match the pinned public n2.csv, which I fetched.
- **Dictionary evidence:** I checked the JMdict entries for all 20 words against the evidence file. I also checked titles, links and quiz exclusions against existing files in `words\` and `kanji\`.
- **Not read:** `componentEvidence`, the author's inspection receipts, and any forbidden files.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 曲線 | CLEAN | CLEAN | CLEAN |
| 規律 | CLEAN | CLEAN | CLEAN |
| 斬る | CLEAN | CLEAN | CLEAN |
| 気を付ける | CLEAN | CLEAN | CLEAN |
| 区域 | CLEAN | CLEAN | CLEAN |
| 偶数 | CLEAN | CLEAN | CLEAN |
| 空想 | CLEAN | CLEAN | CLEAN |
| 空中 | CLEAN | CLEAN | CLEAN |
| クーラー | CLEAN | CLEAN | CLEAN |
| 釘 | CLEAN | CLEAN | CLEAN |
| 区切る | CLEAN | CLEAN | CLEAN |
| 櫛 | CLEAN | CLEAN | CLEAN |
| くしゃみ | CLEAN | CLEAN | CLEAN |
| 苦情 | CLEAN | CLEAN | CLEAN |
| 苦心 | CLEAN | CLEAN | CLEAN |
| 屑 | CLEAN | CLEAN | CLEAN |
| 崩す | CLEAN | CLEAN | **NEEDS FIX** (B21-R01) |
| 薬指 | CLEAN | CLEAN | CLEAN |
| 崩れる | CLEAN | CLEAN | CLEAN |

- **Six related edits: all CLEAN.**
  - 曲線 is added to 線 at セン, 規律 to 律 at リツ, and 区域 and 区切る to 区 at ク, each with the right JMdict ID.
  - 域 now links 区域 and lists it at イキ.
  - カーブ only gains a link to 曲線.
  - 金魚 only gains `jlpt: 2`.
- **金魚 reuse: CLEAN.**
  - 金魚 (entry 1242750) is not where it would appear in the alphabetically sorted き sections of the pinned n5, n4 and n3 lists.
  - So N2 is its easiest listed level and `jlpt: 2` is correct.
- **All 20 mappings: CLEAN for correctness, coverage and clarity.**
  - The selected dictionary senses and the extra senses taught match the evidence. These include 崩す 1, 4 (+2), 崩れる 1 (+2, 3, 6), 屑 1 (+2), 薬指 1 (+2), 規律 1–2, クーラー 1–2 and 区切る 1–2.
  - くしゃみ correctly leaves out sense 2, which belongs only to the reading くさめ.
  - Raw source glosses that could mislead are explained with qualifications rather than taught as unlimited meanings: 斬る "behead/murder", 区切る "stop", 苦心 "pain" and 区域 "domain".
- **Kanji metadata:** complete. The only N2 kanji in this batch are 線, 律, 区 and 域, and all now have reciprocal examples at the correct readings. 斬, 釘, 櫛, 屑 and 崩 are listed in the word metadata but have no kanji cards, and the articles say so.

## Findings
**B21-R01**
- **Severity:** Minor. **Facet:** comprehensibility. **Location:** words\崩す.md:37.
- **Problem:** The sentence "Likewise, the intransitive counterpart does not automatically license every same-object use of 崩す." is hard to follow. "Likewise" doesn't connect to the previous sentence, and "license every same-object use" is linguistics jargon. A learner may not understand the point, though nothing in it is wrong.
- **Remedy:** Reuse the clearer wording from 崩れる.md:31 ("…not a guarantee that every use has an equally usual counterpart"), add a concrete example, or delete the sentence.
- **Evidence:** the line itself, compared with 崩れる.md:31. **Confidence:** high.

## Optional
- **崩す and 故障:** consider excluding 故障 ("breakdown; malfunction") from 崩す quizzes. English "break down" can mean a machine failing, and 壊れる is already excluded for a similar reason.
- **気を付ける and かまう:** consider excluding かまう ("mind; be concerned"). "Mind…" in English can mean "be careful", although "be concerned" lowers the risk.
- **Other low-risk exclusions:** 警告 ("warning; caution") and そろそろ ("slowly and carefully") for 気を付ける.
- **斬る:** could mention the figurative media use 世相を斬る ("criticise society"). JMdict 1304400 doesn't include it.
- **薬指:** 指輪 ("finger ring") could be a good intentional wrong answer (`quiz_distractors`).

## Limits
- I could not run Git or verify any hashes.
- I didn't read `componentEvidence` or the author receipts. I checked kanji only against the repository's kanji files and JLPT levels.
- The Weblio and Kotobank pages for Daijisen didn't load usable content. These Daijisen claims are therefore supported only by JMdict and general knowledge:
  - 句切る being "especially recognisable in language contexts"
  - the 崩す uses the article attributes to Daijisen
  - クーラー as a portable cooler box (JMdict sense 2 does support this)
  - 苦情 as "difficult circumstances"
- I checked n5, n4 and n3 only at the alphabetical spot where 金魚 would appear, not by searching each whole file for its ID.
- I judged quiz risk from article titles, not by running the app.
- None of this is native-speaker certification.
