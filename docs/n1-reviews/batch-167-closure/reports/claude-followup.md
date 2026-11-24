**Snapshot:** f0fefbcb342e1cbebdebd67c7681873e46e780e2, reviewed as a confirmation of my a22f26b… report. This is not a fresh whole-deck or device review.

**Scope:** One reviewer, Claude Sonnet 5.5 (claude-sonnet-5.5), covering correctness and scoped coverage. I read followup-diff-1..6, followup-revision-1..6 (16 full revised cards), followup-facts.txt, correction-evidence.txt, correction-families.xml and confirmation-task.txt. I did not re-read the unchanged cards or rubric. For the unchanged cards I rely on my first-round reads, plus the fact that no diff was supplied for them.

**Verdicts (all 16 revised cards)**
- Correctness is CLEAN.
- Scoped coverage is CLEAN.
- Comprehensibility is not assigned.
- Unchanged cards keep their earlier CLEAN verdicts.

**Reconciliation of my earlier findings**
1. **Exclusions possibly one-directional: RESOLVED, on author-reported evidence only.**
   - **Author observation (not source fact):** correction-evidence.txt says the Android `QuizBuilder.kt` and `Words.kt` at commit 4db1297 treat a declaration on either side as sufficient. It says the word fallback checks both directions.
   - **What I checked:** I did not inspect that code. I checked that the new exclusions match the revised frontmatter and that the labels exist. The new exclusions are:
     - 幽 gains 淡
     - 幻 (word) gains 空想
     - 廃止 gains 取り消す
     - 幽閉 gains 缶詰
2. **凡庸 bullet placed after prose: RESOLVED.** In revision-1 it now sits in the Common words list, after 平凡 and 凡例.
3. **Metadata citation 1478740 (判例): RESOLVED.** The 凡 Notes now say 凡例 and 判例 share the reading はんれい. JMdict 1478740 is "judicial precedent".

**Optional items from round 1 that were adopted, each checked against source rows**
- **幽 meaning line:** it now says "usually kana-written かすか", which fits JMdict 1590290.
- **廉:** かど is described as usually in kana, meaning grounds, a charge or suspicion (2085290). The 嫌疑 sentence is also corrected.
- **元帥 and 帥:** both now say 元師 is irregular, as in JMdict 1260890.
- **帆船 ほぶね:** added to both the 帆 kanji and word cards (1583230).
- **庶民:** the 市民 remark is now limited to "these senses".
- **安い:** it now says only 安い carries the priority tags (ichi1, news2, nf47), and that the calm sense is restricted to 安い (`stagk`). Both facts are confirmed in 1153670.
- **幻 second example:** replaced with 写真家は、ついに幻の鳥を撮影した. The reading and translation are correct, and the unverified idiom 幻に終わる is gone.

**Regression inspection:** I found no defects.
- The new 元帥 example sentences are correct.
- The 淡 note ("pale color or vague outline") matches 淡い (1418420).
- The 空想 and 取り消す glosses are consistent with 1245730 and 1326790.
- The 自己 rewording is accurate.
- Reading allocations are unchanged apart from the ほぶね addition.

**Remaining actionable issues:** None.

**Optional ideas, none required**
- **凡庸:** the explicit "before a noun, use 凡庸な" rule was replaced by the example 凡庸な案. That is defensible, because JMdict 1523660 also records の. If you want the rule back, qualify it as "usually 凡庸な (JMdict also records の)".
- **缶詰 sentence:** JMdict 1214560 says "being stuck in a confined space" (usually ～になる) and "confining someone to concentrate on work" (usually ～にする). The card says "stuck in a room", which is narrower. Consider aligning it and showing the ～になる attachment.
- **幻 sense 2:** "fleeting dream" is now explained in prose only, with no example.
- **安い:** "Its separate…" could name the entry as the referent.
- **元帥:** "check the navy and period" could read "check which navy and period". The Distinctive section no longer has contrastive examples.
- **己 おのれ:** "literary" paraphrases JMdict's "poetical term".
- **Carried over from round 1:** a contrastive 自己/自分 pair, 安価 (no card exists), and undocumented Kanjipedia-only readings.

**Limits**
- Android code, Daijisen and Kanjipedia pages were not opened. I relied on the author's reports for them.
- Glyph and shape mnemonics are unverified.
- There was no device or native check.
- followup-facts.txt accounting (`overallN1TaskComplete: false`) is outside my assignment.
