**Snapshot:** dc46cc08608fa8714a68a36af77fb9ebd1b8fa37, based on 894d3052. This is the packet only; no uncommitted changes were seen.

**Scope:** I reviewed correctness and scoped coverage as a single blind reviewer, Claude Sonnet 5.5 (`claude-sonnet-5.5`, runtime-reported and not independently verified). I read these files in full:
- rubric.txt, snapshot.txt, changed.txt.
- kanji-1 to 4 and words-1 to 3.
- comparison-words.txt.
- sources.json, quiz.txt, labels.txt.
- primary.xml, in two ranged views through line 244.
- families-1 to 8, with families-1 read in two ranges.

I did not assess comprehensibility. The viewer showed no line numbers, so findings cite article sections instead.

**Verdicts**

| Article | Correctness | Scoped coverage |
|---|---|---|
| New kanji 忍 忠 恒 恭 悦 悼 惨 惰 愁 愚 | CLEAN | CLEAN |
| Words 忍ぶ, 忠実, 恒例, 恭しい, 追悼, 怠惰, 郷愁, 愚か | CLEAN | CLEAN |
| Word 満悦 | CLEAN | **NEEDS FIX (minor)** |
| Changed みじめ, 例, 実, 満, 追, 怠 | CLEAN | CLEAN |
| Changed 郷 | UNVERIFIED (one metadata ID, F2) | CLEAN |

- **Kanji readings:** For all ten new kanji, the on, kun and quiz readings match their reading tables or qualified source-only rows. These are 恒 つねに and 惨 いた.む.
- **Outside-table readings:** Kanjipedia readings outside the standard-use table (忍 ジン/むご.い, 忠 まごころ, 恭 つつし.む, 惰 タ/おこた.る, 惨 いた.ましい) are correctly left out of the metadata.
- **JMdict citations:** Every cited sense and restriction checks out against the packet. Examples are 忠実 versus まめ 2827450, 偲ぶ as a separate entry, 疎か 2832535, 恭々しい as search-only, and 惰性 sense 1 "force of habit".
- **Spellings and links:** 悦ぶ and 愁える are rarely used forms, and 愁い is an unmarked second spelling. The 覚える "to feel" sense restricts to that spelling. All 16 required reciprocal pairs are present in both directions with the correct readings.
- **Comparison articles:** I used the eight older articles only for the claims that bear on the new cards. Their JMdict sense citations match, and I found no conflicts. This is not a full review of them.

**Findings**

**F1. Minor, scoped coverage and qualified claim: 満悦 (words-2, Meaning, How the kanji combine, Distinctive meaning, first example)**
- **Claim and impact:** JMdict 1526740 sense 1 carries the note "usu. as ご満悦". The card omits it, says "満悦する is the verb form", and uses bare 満悦していた in example 1. The packet shows only that the bare form is attested (Daijisen's 〜に満悦する, as quoted in the card). Learners may over-generalise the bare verb.
- **Remedy:** Add to Distinctive meaning: "JMdict notes 満悦 is usually met as ご満悦. Bare 満悦する, as in Daijisen's 手厚いもてなしに満悦する and example 1, is attested but less typical; ご満悦だ/ご満悦の様子 is the usual frame." Keep both examples.
- **Evidence:** primary.xml and families-6 entry 1526740.
- **Confidence:** high that the flag is omitted; medium on "less typical".

**F2. Minor, verification: 郷 changed Metadata line**
- **Claim and impact:** The new "Word pairs" list includes 1355850, which is 場所 and contains no 郷. The ID was already in the old metadata line, so this is probably a leftover. The card body outside the diff was not provided.
- **Remedy:** Drop 1355850 from "Word pairs" unless the body uses 場所 as a contrast.
- **Evidence:** families-3.
- **Confidence:** low to medium.

**Optional**
1. 忍ぶ: JMdict orders hide (sense 1, intransitive) before endure (sense 2, transitive); the card reverses this. Add a clause saying so, and note that 忍びない is usually …に(は)忍びない (JMdict 2154730).
2. 忠実, 恒例: state the attachments. 忠実な + noun and 忠実に + verb; 恒例の + noun (JMdict marks 恒例 as taking の).
3. Joyo-table sentences: add readings from JMdict. 惰眠 (だみん), 惰気 (だき), 愚鈍 (ぐどん), 暗愚 (あんぐ).
4. Kanji cards 実, 追 and 例 only list the new word. Add a clause for the shifted sense: sincerity, looking back, custom.
5. 惨 and みじめ: the standard-use table lists the whole みじめ; the みじ+め split follows KANJIDIC2. Add one qualifier.
6. 郷愁: "JMdict also lists 懐古" overstates the link. It is a separate entry with no cross-reference; reword it.

**Limits**
- **Pages not in the packet:** The Joyo PDF pages, Kanjipedia pages and Daijisen/実用日本語表現辞典 text are not included. Their claims rest on sources.json's authorDictionaryChecks. Quoted Daijisen examples and the ごうれい note are unverified. JMdict corroborates 満悦至極, 追悼の辞, 哀悼の意, 人目を忍ぶ and 見るに忍びない.
- **Quiz exclusions:** The packet cannot show whether exclusions work symmetrically. The new cards exclude older ones, but the older cards do not exclude the new ones. Examples are 怠 ("neglect; be lazy") vs 惰, こらえる/たえる/凌ぐ ("endure") vs 忍ぶ, and 弔/悔/喪/忌 ("mourn") vs 悼. This is a consistency and quiz-safety question for another reviewer; if exclusions are one-way, add the reciprocal exclusions.
- **Items I could not check:** link targets such as 行事, 毎年 and まじめ (labels.txt is only a subset); 怠's quizOnyomi; 馬鹿's ばかにならない entry 1471660; and the visual-component claims in the kanji shape mnemonics, which I judged from my own knowledge.
- **Not done:** No external, native or device verification, and no whole-deck acceptance.
