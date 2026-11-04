Snapshot: aef958a3bccd96044d0af50e2da74b1b8cfe20da, as supplied, with no uncommitted teaching changes. I did not check Git: no shell was allowed, so I cannot confirm that the working tree matches this commit.

Scope:
- **Reviewer:** Claude Opus 5.5 (claude-opus-5.5). Each response made one tool call and waited for its result before the next call.
- **Files and facets:** I reviewed all of `kanji\企.md` (1-67) and `words\企てる.md` (1-61) for correctness, scoped coverage and phone-text comprehensibility. In `words\企業.md`, I reviewed the changed 企 link (line 27) and read lines 1-39 only for context.
- **Dictionary sources:** I read every assigned range of the three JMdict files (2492, 443 and 349 lines) and the KANJIDIC2 file (548 lines, seven records).
- **Comparison articles:** I read the eleven kanji articles (人, 止, 業, 危, 休, 全, 計, 図, 承, 意, 試) and the thirteen word articles (計画, 予定, プラン, 設計, 計, 引き受ける, 案, 提案, 言い出す, 試す, 試し, 会社, 商社).
- **Guidance:** I read `.github\copilot-instructions.md`, `content-structure.instructions.md`, `docs\content-format.md` (1-180) and `docs\jlpt-levels.md` (1-32).
- **Supplied evidence:** I read all eight Kotobank extracts and `04f01.svg`.
- **Extra checks:** I searched `confusable-words.md` and read the title, tag and distractor lines of the twelve legacy cards. I searched all word titles for labels that overlap "plan; attempt", searched the N1 snapshot (no match) and made one live fetch from kanjiapi.dev.

Verdicts:
- **`kanji\企.md`:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- **`words\企てる.md`:** correctness **NEEDS FIX**; scoped coverage **CLEAN**; comprehensibility **NEEDS FIX**.
- **`words\企業.md`, changed passage (line 27):** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
- **`words\企業.md`, unchanged context:** I found no actionable defect, but I did not re-review it.

Findings:
1. **Minor; correctness/comprehensibility; `words\企てる.md`:32, with :52-54**
   - **Claim and impact:** The line "This is one verb, not a compound of separate words for planning and standing" makes an unsourced word-formation claim. It conflicts with the cited dictionaries, which derive くわだてる from くわたつ, "to stand on tiptoe." Lines 52-54 present the tiptoe meaning only as a separate archaic sense, never as the source of the verb. A learner could conclude that standing has nothing to do with the word's history. The rest of the article, including the okurigana split (企 = くわだ, てる = ending), is fine.
   - **Remedy:** Delete the sentence, or replace it with a hedged, sourced note. For example: dictionaries derive the verb from an older word meaning to stand on tiptoe; learn it today as one verb meaning "plan; attempt."
   - **Evidence:**
     - Daijisen, 企てる: 《足をつま立てる意の「くわた（翹）つ」から転じたもの》.
     - 日本国語大辞典: ( 足をつまだてる意の「くわたつ」から転じた語 ). Its usage note (1) hedges a link between くは and foot/heel words (「考えられる」), and note (2) says the tiptoe meaning later passed to ツマダツ.
     - JMdict 1218120, sense 3 (archaic): "to stand on tip-toes".
     - Daijisen, 企 (kanji entry), sense 1: つまだちする (to stand on tiptoe).
   - **Confidence:** High that the derivation is documented. Moderate on how much the sentence will mislead learners.

Other checks found no defect:
- **企 metadata:** Strokes (6), radical 人 (no. 9), grade 8, readings and reading order all match KANJIDIC2. The JLPT level matches the live kanjiapi.dev record (`jlpt: 1`).
- **Selected readings:** The selected readings キ and くわだ.てる each have their own table row linked to a word article (企業 and 企てる). Each word/reading pair is confirmed in JMdict (1218190, 1218120).
- **たくらむ:** The unselected たくら.む row is correctly qualified. JMdict 1218140 marks it godan and "usually written using kana alone", and 日本国語大辞典 qualifies the scheming nuance with 多く ("mostly"). The ichidan and godan forms are correct.
- **Shape explanation:** The mnemonic is labelled as modern-shape, not etymology, and the SVG confirms 人 on top and 止 below. The 全 contrast correctly uses KANJIDIC's classical radical, no. 11 (入).
- **Links:** The links 企↔企てる and 企↔企業 run in both directions.
- **Preserved values:** 企業 keeps `jlpt: 3`, its title and its exclusion of 会社. 商社 still excludes 会社 and 企業. 企てる has no inferred JLPT level.
- **企てる exclusions:** All eleven pairs are defensible as direct pairs, checked in both quiz directions:
  - 計画, 予定, プラン, 設計 and 計 overlap through "plan".
  - 引き受ける overlaps through "undertake" (sense 2).
  - 案, 提案 and 言い出す overlap through JMdict's "to propose"; these are conservative but not harmful.
  - 試す and 試し overlap through "try" ≈ "attempt".
- **Kanji quiz choices:**
  - 企's three curated wrong answers (危 "danger", 休 "rest", 全 "whole; complete") are clearly distinct from "plan; undertake".
  - The twelve legacy cards' titles (person, rest, what, enter, go out, mouth, woman, mountain, sun, moon, man, buy) share no tags with 企 and are not ambiguous with "plan; undertake" if it is used as a fill-in choice.
  - 計, 図, 承, 意 and 試 each have three curated wrong answers, so the default four-choice quiz does not need to fill in 企.
- **Example sentences:** Both 企てる examples, their readings and their translations are natural and accurate.

Optional:
- Words not on the exclusion list whose titles partly overlap might deserve a look: 工夫 ("devising a method"), プログラム ("event plan") and 努める ("make an effort"). I have not shown that any of them is a defensible answer.
- 企.md line 34 says "often written たくらむ", while line 37 calls kana its "usual" spelling, and JMdict says "usually". The wording could be aligned.
- 企.md could briefly mention Daijisen's tiptoe sense (企及) to connect the kanji with the history of 企てる.

Limits:
- The Kotobank extracts were supplied by the coordinator, not retrieved by me. The kanjiapi.dev result is a live fetch, not the pinned snapshot; the N1 snapshot file contained no literal 企 or 4f01, so I could not confirm the frozen entry.
- My exclusion audit covers only the default four-choice quiz and the titles I searched. It does not certify larger, random or live choice pools.
- This is a text review only. I have no native-speaker, device or physical-phone evidence, and font coverage does not show the glyphs are readable.
