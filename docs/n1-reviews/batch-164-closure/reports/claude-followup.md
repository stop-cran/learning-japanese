**Snapshot:** 6ad1fedc1e3a50228ca9ccae45de50e05ac16f7a, on base 6121ea9e. The changes are diffed against 027e5581.

**Scope:** This is a bounded confirmation of my own earlier findings by the same single reviewer, Claude Sonnet 5.5 (`claude-sonnet-5.5`). It is not a new whole-batch review.

I read these in full, one view at a time:
- confirmation-task.txt, treated as data
- changes-1 to changes-4
- revision-1 to revision-5, covering 14 files: kanji 姫, 婆, 媒, 媛, 嫡, 子, 孔 and words 妊娠, 姫, 婚姻, 婿, 媒体, 嫡子, 穴
- dictionary-check.txt, additional-families.xml (7 entries) and line-endings.txt

I did not re-read primary.xml, sources.json, quiz.txt, labels.txt or families-*; I rely on my earlier read of them. Cards that did not change keep my earlier verdicts and were not re-reviewed.

**Reconciliation of my findings**

| ID | Status | Evidence |
|---|---|---|
| F1 婿, groom shown only by 花婿 and "husband" gloss dropped | **Resolved** | words/婿 now says the photo example uses the separate compound 花婿 and cites 1194980 (confirmed in additional-families.xml). It also discloses JMdict's "husband" gloss and points to 夫 as the neutral word. |
| F2 outside-table readings unqualified | **Resolved** | 婆 ばば is marked outside the table. 婆 ばあ is marked as KANJIDIC2-sourced, with バ named as the standard reading. 孔 あな is marked outside the table. 媒 なこうど now names バイ as the standard reading. This matches the Kanjipedia "outside" lists. The quiz still tests ばあ and あな; dictionary-check.txt calls that deliberate, and the cards now disclose it. |
| F3 妊娠: constructed 姉は妊婦だ, no 妊娠する/した, "stage" claim | **Resolved** | The 妊婦 sentence is removed. The card now contrasts 妊娠した "became pregnant" with 妊娠している "is pregnant", and "not a stage" is gone. JMdict 1467350 (vs, vi, "conception") supports this. |
| F4 孔 as "another spelling" without rarity | **Resolved** | 孔 now says to write 穴 and to recognize 孔. 穴 says "outside-table spelling" and "Recognize … in descriptions of a physical opening". This reads as practice advice, not a JMdict restriction, which dictionary-check.txt also states. |
| F6 子.md whole-file diff | **Resolved** | line-endings.txt shows base 65 CRLF, then 0 CRLF (68 LF), then 68 CRLF at head. The diff against base is only the 嫡子 bullet and the Metadata line, which adds up to 68 lines. |

| Optional item from my first report | Status |
|---|---|
| 嫡子 example 1 ambiguous | **Resolved.** The new example ends 家を継いだ, so it clearly shows the "heir" sense. |
| 嫁 "from the other side" | **Resolved.** It now says "the wife of a son". |
| 嫡 title "heir"; 正嫡 lists せいてき first | **Optional, unchanged.** |
| 孤独 vs 寂しい contrast is grammatical only; 孔雀 as a ク example; 婿養子/入り婿 | **Optional, unchanged.** |
| Register notes on 才媛 and bare 婆 | **Unsupported by the packet, remains optional.** |
| Symmetric quiz exclusions | **Author-asserted, outside my facet.** dictionary-check.txt says pairs are tested in both directions; I did not see the quiz code. |

I found no still-actionable defect in the revised text.

**Regression check of changed text**
- **Verified, no regression:** the 姫 ひめ- row matches JMdict's "small; cute; lesser" prefix sense. The 嫡子 and 嫡 titles and the 子 bullet agree with JMdict's "heir; legitimate child". 嫡出子 is confirmed at 1422920 with the reading ちゃくしゅつし. 系図 (1251010) and 正妻 (1377160) are confirmed for the new 嫡子 example. The added readings おうじょ, おうひ and こんやく are correct. The 旋 and 嬢 exclusions and notes match their titles ("rotate; return; mediate"; "young lady; daughter; unmarried woman"). The 媒体 Meaning rewrite is consistent with "medium; media".
- **Optional wording, new and low-impact:**
  - 婿: "gloss it as 'husband,' particularly viewed from the wife's family" attributes a nuance to dictionaries that JMdict does not state. The author's Daijisen paraphrase lists "man marrying into the wife's family" instead, which is a status, not a viewpoint. "Both uses" is now ambiguous because three glosses are present. "Tells you nothing about … where the couple lives" could be softened to "does not by itself state". Simplest fix: say JMdict lists "husband", and optionally mention marrying into the wife's family.
  - 婆: "お祖母さん (also おばあさん)" could read as an alternative spelling. Suggest "(read おばあさん)".
  - 嫡子 example 2: the translation uses *chakushi* with markdown italics, unlike the other cards, and the sentence is a mention of the term, not a use. Suggest plain wording.
- **Incidental, outside my facet:** the new 嬢 exclusion on 媛 is based on label overlap. 姫's label "daughter of noble birth" overlaps 嬢 "daughter" in the same way and has no matching exclusion. I did not check this further.

**Verdicts for the 14 revised cards**
- Correctness: CLEAN for all 14. The one exception is the Daijisen citation in 嫡子 ("especially sense 2"), which I could not check and which stays UNVERIFIED.
- Scoped coverage: CLEAN for all 14.
- Comprehensibility: not assigned.

**Limits**
- I relied on the revision files and diffs; I could not match them to the head commit by hash.
- I assumed changes-1 to changes-4 list every changed file.
- The diffs ignore line endings, so the line endings of files other than 子.md are unverified.
- dictionary-check.txt is the author's paraphrase, not independent evidence. Daijisen and Kanjipedia were not opened, and the sense numbering is unchecked.
- The new 嫡子 examples (嫡子に選ばれ and 「嫡子」と呼んでいる) are not corpus-attested, as the author states, and their naturalness is unverified.
- The quiz and labels data at the new snapshot was not supplied. This matters because the 嫡子 title change alters its displayed label.
- No native or device review was done.
