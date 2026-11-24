Snapshot: 027e5581f5b99523ae5f819d830673c8958560f6, based on 6121ea9e6593497b4a93fb1e9597868bc92a5e6e. Packet only; no git worktree check.

Scope: Comprehensibility and scoped coverage, including natural examples, contrast, and concise phone readings. Correctness is from this same read where packet evidence decides it. Reviewer: Grok 4.7 (grok-4.7); no second model. Read kanji-1..4, words-1..3, reused-word.txt, changed.txt, primary.xml, sources.json, families-1..6 (81 entries), quiz.txt, labels.txt, rubric.txt, snapshot.txt.

Verdicts:
- kanji/姫: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN
- kanji/姻: CLEAN; CLEAN; CLEAN
- kanji/娠: CLEAN; CLEAN; CLEAN
- kanji/婆: CLEAN; CLEAN; NEEDS FIX
- kanji/婿: CLEAN; CLEAN; CLEAN
- kanji/媒: CLEAN; CLEAN; CLEAN
- kanji/媛: CLEAN; CLEAN; CLEAN
- kanji/嫡: NEEDS FIX; NEEDS FIX; NEEDS FIX
- kanji/孔: NEEDS FIX; NEEDS FIX; NEEDS FIX
- kanji/孤: CLEAN; CLEAN; CLEAN
- words/姫: CLEAN; CLEAN; CLEAN
- words/婚姻: CLEAN; CLEAN; NEEDS FIX
- words/妊娠: CLEAN; CLEAN; CLEAN
- words/婿: CLEAN; CLEAN; CLEAN
- words/媒体: CLEAN; CLEAN; CLEAN
- words/才媛: CLEAN; CLEAN; CLEAN
- words/嫡子: NEEDS FIX; NEEDS FIX; NEEDS FIX
- words/孤独: CLEAN; CLEAN; CLEAN
- changed 体, 妊, 婚, 才, 独, 瞳, おばあさん: hunks CLEAN; CLEAN; CLEAN
- changed 子: added line NEEDS FIX; CLEAN; NEEDS FIX
- changed 穴: NEEDS FIX; NEEDS FIX; NEEDS FIX

Findings:
1. Moderate; correctness and comprehensibility; words-3.txt:5,12,16,19; kanji-3.txt:77,82; changed.txt:169. The cards cite JMdict 1422910 senses 1–2 but replace sense 2 "legitimate child" with "child of the principal wife," then prove that narrower equation with unattested 正妻の産んだ嫡子. Impact: the heir-versus-parentage contrast, which this card exists to teach, is memorized as a principal-wife rule. KANJIDIC's character gloss "legitimate wife / direct descent" does not by itself make that the word sense. Remedy: teach sense 2 as "legitimate child"; keep the heir example and the warning not to infer modern legal rights; delete the 正妻 sentence unless the cited Daijisen entry is quoted and labeled as that entry's wording, not as the whole of the JMdict sense. Align the 嫡 reading row, common-word gloss, and the 子.md addition. Evidence: primary.xml and families-3.jsonl 1422910; sources.json 嫡 meanings. Confidence: high on the JMdict mismatch; medium that no teaching correction is justified, because the Daijisen page is not in the packet.

2. Moderate; comprehensibility and scoped coverage; kanji-3.txt:101,103,114,124,128,132; reused-word.txt:61; changed.txt:246. あな is quizzed and called another spelling of 穴, while ク on the next row is flagged outside the standard-use table and あな is not. Impact: learners may write 孔 for ordinary あな. Remedy: on the あな row, add the same outside-table flag Kanjipedia records; say recognize 孔 for a physical あな and write 穴 for the ordinary word. On words/穴.md, replace "another spelling" with that recognition note. Keep the flaw-idiom warning as a usage tendency, not as a JMdict sense ban. Evidence: sources.json 孔 outside list includes あな; JMdict 1254480 lists 孔 with no sense restriction. Confidence: high.

3. Minor; comprehensibility; kanji-2.txt:42. お祖母さん is the spelling contrast but has no reading, so a phone reader can take it as a different word. Remedy: お祖母さん（おばあさん）. Evidence: JMdict 1002330, both spellings, reading おばあさん. Confidence: high.

4. Minor; comprehensibility; words-1.txt:62. 婚約 is the engagement contrast and has no kana, while 結婚しました on the same line does. labels.txt has no words/婚約 entry to supply it. Remedy: add （こんやく）. Evidence: families-2.jsonl 1289710. Confidence: high.

Optional: Flag ばば as outside the standard-use table at kanji-2.txt:33. On kanji-1.txt:34, say the ひめ- in 姫百合 means small/lesser, not princess (JMdict 1602150 sense 3). Label words-1.txt:18–19 as the tale/play use; add a non-royal example only if the cited Daijisen entry attests one. Note 才媛's literary leaning at words-2.txt:85. Drop or specify "or something else" at words-2.txt:51. Mark 嫡子 as advanced on the N5 子 card once the gloss is fixed. Add おうじょ and おうひ beside 王女 and 王妃 at words-1.txt:27.

Limits: No external page, native-speaker, or device check. Daijisen and Kanjipedia prose were not in the packet; reading lists and JMdict families were. Unchanged bodies of the seven older kanji articles were only the diff hunks. Quiz safety and link integrity were not this assignment. Example grammar was checked in-packet only.
