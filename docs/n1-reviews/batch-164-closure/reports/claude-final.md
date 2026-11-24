**Snapshot:** 755ded1c5c12302f7d4d9fdf10a62a47ec5bb839, after 6ad1fedc.

**Scope:** This is a bounded confirmation of my own facet (correctness and scoped coverage) by one reviewer, Claude Sonnet 5.5. I read final-cards.txt in full and final-diff.txt in full, one view at a time. The cards are words/嫡子, kanji/嫡, words/婿 and kanji/姫. It is not a whole-batch review, and I did not re-read other files. For JMdict 1422910, 1422920, 1531160, 1194980 and 1580880 I rely on my earlier reads. Comprehensibility was not assigned, so it is UNVERIFIED.

**Verdicts**

| Card | Correctness | Scoped coverage |
|---|---|---|
| words/嫡子 | CLEAN | CLEAN |
| kanji/嫡 | CLEAN | CLEAN |
| words/婿 | CLEAN | CLEAN |
| kanji/姫 | CLEAN | CLEAN |

**Confirmations**
- **嫡子 example 2:** 彼は王の嫡子として生まれたが、王位は継がなかった is an ordinary sentence, not a metalinguistic mention. Readings and grammar are correct: おうの, ちゃくし, うまれた, おうい, つがなかった. The translation "legitimate child" and the denied succession support the parentage sense. The italic *chakushi* from my earlier nit is gone.
- **嫡子 sources are distinguished:**
  - JMdict gives sense 2, "legitimate child".
  - Daijisen is credited with the child of the principal wife and the cross-reference to 嫡出子, which is glossed as a child born to married parents.
  - The two Daijisen definitions are kept apart, and the Dictionary line matches.
  - Both JMdict senses have an example.
- **嗣子 line:** It correctly places 嗣子 in the succession sense only.
- **婿:**
  - The JMdict "husband" gloss is disclosed.
  - The Daijisen "man marrying into his wife's family" is attributed to Daijisen.
  - The unsupported "viewed from the wife's family" claim and the ambiguous "both uses" are gone.
  - The 花婿 disclosure and entry 1194980 stay in place.
- **嫡 notes:** The line "not who a child's mother was" is gone. That line contradicted sense 2. The replacement, "Neither contrast makes every 嫡子 an heir", is true.
- **姫:**
  - Adding 嬢 as an exclusion is harmless and the daughter-sense overlap justifies it.
  - The Notes and the 媛 exclusion remain coherent.
  - The 姫 and 嬢 daughter-sense overlap I raised before is closed.
- **Hunks:** The final-diff hunks are small, and the final cards match them.

**Actionable defects:** None remain. No regressions were found in the changed text.

**Optional suggestions (not defects)**
1. **嫡子 example 2.** The Japanese alone still allows a reading of "heir who never succeeded". The parentage sense is fixed by the translation and the Meaning text, not by the sentence. A sentence contrasting 嫡子 with a non-wife's child, such as 庶子, would force it. I could not check naturalness.
2. **嫡子 Meaning.** "Daijisen illustrates this distinction" suggests Daijisen is illustrating JMdict. "Daijisen's sense 2 defines it as … and refers to 嫡出子" would be more exact.
3. **婿 Distinctive meaning, unchanged.** "tells you nothing about his surname or where the couple lives" now sits next to the Daijisen "marrying into the wife's family" note. It is true for the son-in-law relationship, but "does not by itself state" would be softer.
4. **姫 Notes.** "嬢 … without implying noble birth" is accurate for お嬢さん. Honorifics such as 令嬢 can suggest good family. This is my own knowledge, not packet-verified; "ordinarily" would soften it.
5. **Carried over, unchanged.** The 嫡 title lists "heir" although KANJIDIC does not give it. Register notes on 才媛 and bare 婆 remain optional and unsupported by the packet.

**Limits**
- Daijisen sense numbering and the 嫡出子 definition rest on the author's paraphrase. I did not fetch them.
- The hashes are labelled SHA-256, not git blob IDs. I cannot recompute them or tie them to 755ded1c.
- I cannot confirm line endings. The diff hunks are localized, which suggests no EOL churn, but the diff options are not stated.
- Link targets, including 嬢, 夫, 嫁 and 嗣子, are unverified.
- Symmetry of the 姫/嬢 exclusion in the quiz generator is unverified.
- No native, corpus or device verification was done.
