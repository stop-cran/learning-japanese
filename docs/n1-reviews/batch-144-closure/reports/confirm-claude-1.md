# Batch 144 confirmation review (Claude)

Snapshot: commit 2be716f0661f17c03da9b4854665fb8e35f1af7a (reviewed snapshot b073abd8f2ab578f29cf2b5e25f36e02fc1aab58). Reviewer: Claude, an Anthropic model; I cannot verify my exact model version from inside the session. I worked alone and read-only, and the only file I wrote is this report.

Scope:
- Read in full: this packet's INSTRUCTIONS.md, CHANGES.md and RESPONSE.md; diffs\fix.patch; my own reports-144\initial-claude.md.
- Revised cards read in full: snapshot\kanji\ 棚, 欄, 棋, 歓, 殻, 汁, 沖, 淡, 渋 and 討 (all 102 lines of 討, so the whole card this time, not only the Notes).
- Evidence read in full: README.md, jmdict-cited-entries.xml, kanji-remarks.json, QuizBuilder.kt, KanjiReadings.kt (lines 1-200: ReadingKey, ReadingCard, KanjiReadingQuiz and the queue) and meta-scan.txt.
- Checks read in full: link-targets.tsv, kanji-remarks.txt, lint.txt and quiz-safety.txt.
- reading-options.txt: the head and every HIT/summary line.
- reading-exposure.txt: the head, the whole 殻 section and the tail with the summary counts.
- Original packet, targeted reads only: evidence\joyo-pages.md (the front-matter lines and the rows for 欄, 殻, 概, 渇, 検 and 沖, including the code points of the 欄 row); evidence\kanjipedia-outside-readings.json (棋, 沖 and their neighbours); evidence\daijisen-heads.txt lines 1-10; evidence\public-source\weblio-淡.txt (the あわ/名のり line); a grep of rubric\copilot-instructions.md and repo\docs\content-format.md for Metadata/JMdict rules.
- Public web:
  - kotobank, Digital Daijisen 表外音訓 (fetched): its 補説 defines ▽ and ×.
  - en.wiktionary 欄 (fetched): U+6B04 and U+F91D, stroke counts and IDS.
  - recatools.com guide on kyūjitai and shinjitai (fetched): it quotes explanatory note 6 of the 2010 Joyo table.
  - Fetching the Joyo PDF itself timed out. The ja.wikipedia 常用漢字一覧 fetch returned only its preamble.
- Not opened: the six unchanged new cards (検 概 殊 泡 泣 渇), the word articles and Words.kt. All are unchanged. I judged their quiz options from quiz-safety.txt, the reading audits and their titles.

Dispositions:
- C1 - RESOLVED - 棚.md:33 now names 陸棚 りくほう (also りくだな), "continental shelf," and 氷棚 ひょうほう, "ice shelf." This matches JMdict 1551120 in evidence\jmdict-cited-entries.xml (readings りくだな and りくほう, gloss "continental shelf"). The revision left the Metadata line without 1551120; that is new Finding 1.
- C2 - RESOLVED - 棚.md:25 now has たな【▽店／棚】, which matches daijisen-heads.txt line 6. Digital Daijisen's own 補説 under 表外音訓 (kotobank) says ▽ is attached when the reading is a 表外音訓 and × when the character is a 表外字. 店 is a Joyo kanji, but its reading たな is not in the table, so "the spelling whose reading is outside the Joyo table" is accurate. The non-standard-form claim is gone.
- C3 - RESOLVED - 歓.md:45 now says 権 has a part at its right that looks like the left part of 歓. This is true of the modern shapes: 権 is 木 plus that element, and 歓 is that element plus 欠. The quoted title of 権, "authority; rights," matches link-targets.tsv.
- C4 - RESOLVED - 淡.md:32 now separates あわ (as in 淡雪 あわゆき) from the name readings あわし and あわじ. weblio-淡.txt line 6 has 〈あわ〉「淡雪」 apart from ［名のり］ あわ・あわし・あわじ, and JMdict 1418470 淡雪 あわゆき is in the evidence. Line 32 now agrees with line 43 of the card.
- C5 - RESOLVED - 討.md:95 reads "In 検討, [検](検.md) supplies ケン and 討 supplies トウ." This is true (検討 けんとう; the Joyo table lists 検討 under トウ, as 討.md:49 says). The bullet stands on its own in the Notes list. kanji-remarks.txt reports the declared edit applied with 0 problems, and the 検 link resolves.
- C6 - DECLINE ACCEPTED - The trade-off the author states is real:
  - KanjiReadingQuiz.question (KanjiReadings.kt:108-112) resolves curated distractors only from the session pool and takes one usable reading from each before any fallback.
  - 休, 本 and 木 are Starter cards, so they are present in every pool, including the Starter practice session (reading-exposure.txt, 殻 section). There they fill all three slots, and 貝 かい is never consulted.
  - Non-Starter look-alikes (殺, 設, 投) would be missing from a Starter session that borrows 殻. That session would then fall back to the open candidates, and the one-holder padded case (a session that also borrows 貝) would become possible.
  - No Starter kanji is a convincing look-alike of 殻.
  - The meaning options "rest | book, origin | tree, wood" are unambiguous against "shell; husk; empty outer covering."
  - This remains a quiz-quality weakness, not a defect.
- C7 - PARTIALLY RESOLVED - Point by point:
  - Point 1 is resolved. 欄.md:42 quotes the four bare glosses and says JMdict marks the entry archaic, matching 2844081 (misc archaic; glosses handrail, railing, banister, balustrade).
  - Point 2 (the Daijisen ［訓］おばしま mention): DECLINE ACCEPTED. It was optional, and the card already names the JMdict entry and says it is not added.
  - Point 3: DECLINE REJECTED, because the stated reason is factually wrong.
    - The bracketed form is not "drawn like 欄." Wiktionary gives the IDS ⿰木闌 for the traditional (TK) form and ⿰木䦨 for the Japanese form. The bracketed form has 柬 inside 門 and 21 strokes; the Japanese form has 東 and 20 strokes.
    - U+F91D is a compatibility ideograph only because Unicode unifies the two shapes under U+6B04, so the old shape has no unified code point of its own.
    - The table's explanatory note says its round-bracketed forms are the so-called Kangxi dictionary forms (いわゆる康熙字典体). I have this through a secondary source that quotes note 6; the PDF fetch timed out. Those forms have exactly the status of 殼, 槪, 檢, 渴 and 澁, which the batch's other cards call the "older form."
    - So 欄.md:44, "a compatibility form of the same kanji," uses an encoding term that the table does not mean. It is inconsistent with the five sibling cards and is jargon to a beginner.
    - Remedy: "It prints the older form of 欄 in brackets, which this card does not teach separately."
- C8 - RESOLVED - 棋.md:32 and 沖.md:34 now qualify the kun typing:
  - kanjipedia-outside-readings.json has 棋 on: キ, ゴ.
  - joyo-pages.md has 沖 チュウ: 沖積層, 沖天, 沖する.
  - The metadata stays with KANJIDIC2, and 棋.md:36 ("The kun reading ご is retained from KANJIDIC2") still reads consistently.
- O-A - DECLINE ACCEPTED - Optional polish. The sense list is a stated selection, and the 明 and 店 sentences are not false.
- O-B - DECLINE ACCEPTED - 点検 and 剖検 are real direct pairs, and exclusions only remove options.
- O-C - DECLINE ACCEPTED - Low-risk wording polish.
- O-D - DECLINE ACCEPTED - Weak exclusions are harmless. "form field" is unambiguous among the options shown (gate; doorway | horizontal | imitate; model; pattern).
- O-E - DECLINE ACCEPTED - 合歓木 is already named at 歓.md:34 as a whole hard-to-read word. A note on 合歓 alone is optional.
- O-F - DECLINE ACCEPTED - Cosmetic. 淡.md:25 and 渋.md:25 still say "One example of each:" and then give two or three examples under some bullets.
- O-G - DECLINE ACCEPTED - Both mnemonics carry the modern-shape and not-etymology label.
- O-H - DECLINE ACCEPTED - 渇す and 渇する are not quizzed and are fed to the audits as extras (reading-options.txt command line).
- O-I - DECLINE ACCEPTED - あぶく is not selected, and it is fed to the audits as an extra.
- O-J - DECLINE ACCEPTED - I had said that leaving it out is acceptable. かい is tracked as a latent collision and is not drawable.
- O-K - DECLINE ACCEPTED - A minor attribution nit. 汁.md:23 is unchanged.
- O-L - DECLINE ACCEPTED - The author's judgement agrees with mine; no exclusion is needed.

Verdicts:
- Correctness: CLEAN within scope. Every changed claim I checked (棚 25 and 33, 歓 45, 淡 32, 欄 42, 棋 32, 沖 34, 討 95) is true. The 欄.md:44 wording is listed under consistency, not as a false statement.
- Scoped coverage: CLEAN. The splits in 殻, 汁 and 渋 move text without loss. I compared them against fix.patch: the paragraphs are identical apart from the breaks.
- Consistency and quiz safety: NEEDS FIX. 欄 (C7 point 3, "compatibility form" against the batch's "older form"); 棚 (Finding 1, Metadata line missing 1551120). Quiz options: no defect.
- Comprehensibility: CLEAN. The paragraph splits in 殻, 汁 and 渋 improve phone reading. The 欄 "compatibility form" jargon is covered by C7.

Confirmation: NEEDS FIX - C7 is only partially resolved (point 3's decline rests on a false premise), and the revision introduced one small provenance inconsistency (Finding 1). Both are minor one-line fixes.

Findings:
1. Minor. Facet: consistency (provenance).
   - Location: snapshot\kanji\棚.md:53, the Metadata line, against 棚.md:33.
   - Claim and impact: The revised ホウ row now names 陸棚 りくほう as JMdict evidence. The Metadata line lists 2831996 (氷棚) but not 1551120 (陸棚). The author's own meta-scan.txt flags exactly this: "棚.md:33: 陸棚 1551120 not listed", the only whole-run gap in the batch. The card's word-identity sources are therefore incomplete for a word it now cites as reading evidence. There is no quiz impact.
   - Remedy: add 1551120 to the entries list on 棚.md:53.
   - Evidence: evidence\meta-scan.txt line 4; evidence\jmdict-cited-entries.xml (1551120); 棚.md:53.
   - Confidence: high.

Quiz options, checked for all 15 cards and 討:
- Meaning options:
  - QuizBuilder.options tries the curated distractors first. It skips any card in an exclusion pair, in either direction, with the target or with an option already chosen, and it allows no duplicate titles. The tag-ranked fallback runs only for slots that are still open.
  - quiz-safety.txt shows three curated options for every batch card. None of them is excluded from its target.
  - For every card, the titles of the three wrong options cannot also be correct: none overlaps the card's own title as a meaning that would make it right.
  - The weakest options are on 殻 (C6, accepted) and on 欄 and 淡, where the overlaps 原, 高 and 開 were judged earlier and do not appear here.
  - No front matter changed (fix.patch touches no line from 1 to 15 of any card), so the options are the same as those I reviewed in round 1.
- Reading options:
  - KanjiReadingQuiz.excludedKeys removes every metadata reading of the target and its sound-change variants.
  - The audit's --extra lists also cover the attested readings outside the metadata: ご/ゴ, ホウ, おばしま, あわ, わく, と.ぶ, むな.しい and かい.
  - Summary: 0 production hits, 0 padded hits, 0 one-holder hits and 6 latent collisions (欄 わく, 歓 ぶ, 殊 け, 殻 かい, 沖 とぶ, 沖 むなしい). The single labelled HIT is 殻 かい from 貝 (reading-options.txt:116). It is not drawable, because 休, 本 and 木 fill every slot in all three pools.
  - 概, 沖, 淡 and 渇 use 2 of 3 curated reading slots, for the reasons I gave in round 1. Their fallback options were audited as safe.
- What the audits cannot show:
  - whether a wrong meaning title is semantically defensible (only a human can judge that);
  - pools other than the N1 stack, the All stack, the Starter session and one-holder padding, such as a Starter session that borrows two or more holder cards;
  - readings that are attested but absent from the --extra inputs;
  - runtime behaviour of the real app (the Kotlin cross-check and the Android JVM content tests were not run).

Optional:
- 淡.md:25 and 渋.md:25: change "One example of each:" to "Examples:". This is O-F, cosmetic.
- 欄.md:44: when fixing C7, the card could add that the older form differs in the part inside 門. This is optional.

Limits:
- I made exactly one tool call per response throughout and noticed no parallel calls.
- I could not open the official Joyo PDF (the fetch timed out). The meaning of its round brackets (いわゆる康熙字典体) comes from a secondary source that quotes note 6. The shape difference of 欄 comes from Wiktionary's IDS and stroke data, not from the PDF image. I did not inspect the U+F91D glyph image itself.
- The Daijisen ▽ convention is verified from Daijisen's own 補説, through kotobank. I did not re-fetch the live weblio pages for 棚 or 淡; I used the packet's extracts.
- I did not re-read the six unchanged new cards or the word articles in this round. I relied on round 1, on fix.patch (which shows no change to them) and on the audits.
- The claim that the rerun audits are line-for-line identical to the freeze is the author's. I read the rerun outputs themselves, not a diff against the freeze.
- I am Claude by Anthropic; I cannot confirm the exact model version.