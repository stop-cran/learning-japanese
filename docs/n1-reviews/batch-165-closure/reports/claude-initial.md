**Snapshot:** 6fb17b33769b5c7ccb2fa1c7ec48667d08356914 (base 1cd30ef3…), as stated in `snapshot.txt`. I ran no git commands, so I could not confirm it independently. No uncommitted changes are known.

**Scope:** One reviewer, Claude Sonnet 5.5 as reported by the runtime. I read these in full, one view at a time:
- `changed.txt` (5 diffs)
- `kanji-1..4` (宮 宰 宵 寛 寡 尉 尚 尺 尼 尽)
- `words-1..4` (神宮 主宰 宵 寛大 寡婦 大尉 尚 尺度 尼 尽くす)
- `primary.xml`, `sources.json`, all rows of `families-1..7`
- `quiz.txt`, `labels.txt`, `rubric.txt`, `snapshot.txt`
- the four cards in `comparison-words.txt`

Correctness and scoped coverage are my assigned facets. Comprehensibility got a lighter pass. Quiz safety was only incidental.

**Verdicts (C = correctness / S = scoped coverage / K = comprehensibility):**
- **Kanji, CLEAN/CLEAN/CLEAN:** 宮, 宰, 宵, 寛, 寡, 尉, 尚, 尺, 尼, 尽.
- **Words, CLEAN/CLEAN/CLEAN:** 神宮, 宵, 寛大, 寡婦, 大尉, 尚, 尺度, 尽くす.
- **主宰:** C UNVERIFIED (F2), S CLEAN, K NEEDS FIX (F1).
- **尼:** C UNVERIFIED (F3), S CLEAN, K CLEAN.
- **Changed kanji 主, 大, 婦, 度, 神:** CLEAN/CLEAN/CLEAN for the diffs only. Reading tables are not shown, so this covers the visible diff, not the whole cards.

**What CLEAN rests on:**
- **Front matter:** strokes, radical, grade, on/kun and quiz keys match `sources.json` for all ten kanji.
- **Reading tables:** every KANJIDIC2 reading has a row or a qualified source-only note (寛 ゆる.やか, 尽 サン, 尉 ジョウ).
- **Whole-word readings:** all ten are allocated correctly.
- **Sense ranges:** the cited senses match `primary.xml` and the quiz `senseNumbers`.
  - 尚 sense 4 (as if; formal/literary) is rightly outside the card.
  - 尼 senses 3–5 are outside the card, and the derogatory use is disclosed.
- **寡婦:** かふ is restricted to 寡婦, やもめ is unrestricted, and the glosses widow / divorced woman not remarried / unmarried woman are reported faithfully.
- **大尉:** だいい is the Imperial Navy reading, and the captain/lieutenant glosses match.
- **尽 rows:** 力尽く reads ちからづく or ちからずく, 納得尽く reads only なっとくずく, and 納得づく reads なっとくづく.
- **Examples:** all 22 example sentences were checked for kana, particles, tense and translation.
- **Changed cards:** the bullets match the new word titles, and every added JMdict ID appears in the families data.

**Findings:** none consequential.
- **F1 – Minor, NEEDS FIX, K.** `words-1`, 主宰, "How the kanji combine": "Reversing who leads whom changes the meaning of the sentence." This is vacuous and unsupported, because 主宰 is not a pair of roles and nothing demonstrates a reversal. Remedy: delete it, or write "Together they name directing a group or heading it; they are not two roles that could be reversed." Evidence: card text and JMdict 1325480. Confidence: high.
- **F2 – Minor, UNVERIFIED naturalness.** `words-1`, 主宰, example 2. "雑誌でその劇団の主宰に話を聞いた" leaves "for a magazine" to the translation, and 雑誌で could be misread as "in a magazine". Remedy: 雑誌の取材でその劇団の主宰に話を聞いた。(ざっしのしゅざいで…). Confidence: low to medium. No native or corpus check.
- **F3 – Minor, UNVERIFIED naturalness.** `words-3`, 尼, example 2. A bare "尼が" as the subject for a present-day nun reads abruptly, and the same card warns about the insulting あま. Remedy: use 尼さん (あまさん) or 尼僧, or restrict 尼 to set phrases such as 尼になる and 尼寺. Confidence: low to medium.

**Optional (nonblocking):**
- 寛大 gives the rule "寛大に before an action" with no example, and doesn't explain the N に寛大だ pattern in example 1. Suggest adding "先生は私たちの失敗を寛大に許してくれた。" (naturalness unverified).
- 尚 contrasts with まだ only as "overlaps". It could note that まだ also means "not yet" (labels: "still; not yet") and that 尚 is usually kana.
- 尺度: "The latter fits an evaluation, not the ruler on your desk" contrasts 基準 with 物差し, not with 尺度. One contrastive example, such as 合格の基準 vs 評価の尺度, would help.
- 尽くす: the "devote oneself to" sense (JMdict sense 2, intransitive) has no に example, such as "彼女は夫に尽くした". The only example is the collocation 力を尽くす.
- 宵: the card has no register note. Standalone 宵 mostly appears in set phrases (宵の口, 夏の宵) and in the poetic 今宵.
- 宮 title "imperial shrine" is narrower than JMdict "shrine" and KANJIDIC2 "Shinto shrine". The body text is fine.
- 尼: the kanji card says "Christian" while the word card and JMdict say "Catholic nun; sister".
- 寡婦: "do not split やもめ into those two on readings" is unclear. Suggest "やもめ is a whole-word reading; don't divide it between 寡 and 婦".
- 宰 Meaning: "not a job title that every group must use" is vague.
- Kanjipedia-only readings are undocumented: 宮 いえ, 宰 つかさど.る, 寡 すく.ない/やもめ, 尚 たっと.ぶ/とうと.ぶ/くわ.える, 尺 ものさし/わず.か, 尼 ジ, 尽 すが.れる. Only 寡 やもめ matters, since the 寡婦 card teaches it.
- Quiz-safety hypotheses for the other reviewer, based on displayed labels:
  - 尽くす is not excluded against 注ぐ ("pour; devote").
  - 尚 is not excluded against じっと ("still; intently; patiently").
  - Kanji 尚 is not excluded against 且 ("moreover; also"), although 更 is excluded.
  - 主宰 vs 監督 ("supervision; director; coach") is a weak overlap.
  - If exclusions are one-way, 物差し and 基準 (both share a gloss with 尺度) and キャプテン, 独身, 神社, 夕方, 夕べ, 晩, 夜 do not exclude the new cards. The packet doesn't say whether exclusions are symmetric.

**Limits:**
- I did not open Kanjipedia, KANJIDIC2 or Digital Daijisen pages. Their claims rest on `sources.json` and JMdict data. The "checked Daijisen character entry" claim for 尽 サン is unverifiable here.
- There was no native, device, whole-deck or corpus verification.
- The five older kanji were reviewed as diffs only.
- Link targets (妻, 優しい, 厳しい, 努力, and kanji 憩, 広, 老, 更) could not be confirmed to exist.
- Line numbers were not shown in the views, so locations are cited by card and section.
- I have no execution records to confirm my own model identity or read ranges.
