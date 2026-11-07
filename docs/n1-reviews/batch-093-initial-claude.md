Snapshot: 27663944c7217a19e7de2f363e1b31a5f13452b6. I relied only on the packet. I did not check Git or upstream sources myself.

Scope: The model used was Claude Opus 5.5 (`claude-opus-5.5`). I reviewed `kanji/刑.md` lines 1–49 and `words/刑事.md` lines 1–35 in full, plus the added line 37 in `kanji/事.md`. The other 12 articles were used only for comparison. I also checked the two JMdict extracts, the eight KANJIDIC2 character records, the metadata JSON, the KanjiVG SVG, `strokes/刑.json`, the receipts, the two Kotobank text extracts and the guidance excerpts.

**Verdicts**
- **`kanji/刑.md`:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- **`words/刑事.md`:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.
- **`kanji/事.md` line 37:** correctness CLEAN; scoped coverage CLEAN; text comprehensibility CLEAN.

**Findings:** None proved.

What I checked and found supported:
- **Meaning:**
  - Line 22 of `刑.md` separates a legal sentence from a grammatical sentence. This matches JMdict 1249610 and the Daijisen entry.
  - Lines 21 and 33 of `刑事.md`, and line 47 of `刑.md`, say that 刑事 is either a detective or "criminal" as in criminal matters. They correctly say it never means an offender.
  - 刑事事件, 刑事裁判 and the 民事 contrast all match JMdict entries 1249680, 1249670 and 1528730 and Daijisen's ⇔民事.
- **Readings:**
  - The metadata reads `onyomi: [ケイ]`, `kunyomi: []`, `quizOnyomi: [ケイ]` and `quizKunyomi: []`, exactly matching the frozen KANJIDIC2 record.
  - The ケイ row in the reading table links to 刑事, and splitting it as ケイ+ジ is correct.
  - ギョウ is credited to Daijisen and shown in 刑部省 ぎょうぶしょう (JMdict 2256510). It is not added to the metadata.
  - でか is described as a slang reading of the whole word (JMdict 1008360), not a kun reading of 刑.
  - Primary reading けいじ, N3 level and title are preserved.
- **Character facts:**
  - Grade 8, 6 strokes, radical 刀 no. 18, and the visible 刂 all match KANJIDIC2 and the six stroke paths in KanjiVG.
  - The mnemonic is labelled as invented. It does not deny KanjiVG's `phon="井"` or 字通's 形声 classification.
- **Quiz exclusions on 刑事:**
  - Excluding 警官, 警察 and 巡査 is supported. Daijisen and Nipponica describe 刑事 as a common name for police officers who are usually ranked 巡査 or 巡査部長.
  - おまわりさん is in a different register but still an overlapping police-officer label, so excluding it is a reasonable cautious choice.
  - The existing exclusion from 探偵 to 刑事 is justified because both titles contain "detective".
  - These are separate pairs; they don't form a group where everything excludes everything.
- **Wrong-answer kanji 乃, 凹, 凸:** None of their titles or secondary meanings overlap with punishment. Leaving 形 and 型 out is sensible because 刑 has model/form senses.
- **Links:** Both links between 刑 and 刑事 work, as do both links between 事 and 刑事. The 事→刑事 link is the new half of the existing 事/刑事 pair. The paths, the reading けいじ and `kanji: [刑, 事]` are all correct.

**Hypotheses (not proven):**
- Line 45 of `刑.md` calls the model/form senses "older". Daijisen only marks them as used interchangeably with 型/形. The hedge is adequate (low confidence).
- On wider quiz pools, 文's title "sentence, writing" could look like a possible answer for 刑. Default quizzes use the three curated wrong answers, so this belongs to later app testing.

**Optional**
- `刑事.md` line 18: "is questioning a witness" fits 話を聞いています more closely than "is talking to a witness".
- Mention that でか is often written デカ in katakana, and maybe add a short でか pointer in `刑事.md`.
- 乃, 凹 and 凸 are unambiguous but not very believable wrong answers.

**Limits**
- **What I read:** One full-file read returned all 5,392 lines. A second read of lines 5300–5392 only confirmed the end; nothing was missing.
- **Counting:** I counted the 23 comparison entries but did not tally the 157 lexical entries one by one, though I read all of them.
- **Source limits:** Some characters are missing from the 字通 text, so I can't verify historical claims from it. The 2026 Kotobank pages and the date match aren't independently checked.
- **Not checked:**
  - How the fonts, stroke drawings, app screens or phone render.
  - The production N1/All and custom/random quiz pools, including any other words titled "criminal".
  - Whether the cards actually help learners.
- I made no edits.
