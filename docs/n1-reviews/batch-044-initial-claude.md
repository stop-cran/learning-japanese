I've finished the review. Both files are accurate, but the word article leaves out that the Boar sign is also commonly called いのしし (いのしし年), so I'm marking its coverage NEEDS FIX. Everything else came out CLEAN.

```text
Snapshot: df413408aa3ef0edd09fbc0dd47756594bd79709 as stated in the task, with no uncommitted teaching. I could not check Git myself (no shell), so I did not confirm the commit, the signature or that the working tree is clean.

Scope: Claude Opus 5.5 (claude-opus-5.5), one reviewer, read-only.
- Files reviewed: kanji/亥.md (lines 1-67) and words/亥.md (lines 1-65), for correctness, scoped coverage and textual phone comprehensibility.
- Sources read in full, one at a time: batch-044-input-metadata.json (all 7 raw character elements).
- Dictionary families: batch-044-jmdict.xml (17 lexical families) and batch-044-comparison-jmdict.xml (19 comparison families), 36 in total.
- Unchanged comparison pages: words 猪, 豚, 年, 時刻 and kanji 猪, 豚, 刻, 交, 亡 (9 in total).
- Guidance: copilot-instructions (1-244), content-structure instructions (1-85), jlpt-levels (1-401), content-format (42-148).
- Supplied artifacts: Daijisen い/がい (1753-1805), Kanjipedia 亥 character (45-145), Kanjipedia い word (45-99), Daijisen 亥年 (1810-1855).
- One bounded search of docs/confusable-words.md for 亥|猪|いのしし|豚|干支|zodiac|boar.

Verdicts:
- kanji/亥.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- words/亥.md: correctness CLEAN; scoped coverage NEEDS FIX; comprehensibility CLEAN.

Findings:
1. Minor; scoped coverage (with a quiz-guard consequence); words/亥.md:8, 17, 34-37, 41-44, 48-49.
   Claim and impact: The article separates the sign from the animal and says the animal nouns are "not unrestricted substitutes" for 亥. That is accurate. But it never says that the sign itself is commonly called いのしし, as in いのしし年 for 亥年. A learner may then think いのしし cannot name the zodiac sign, and will not recognise いのしし年 or 干支はいのしし. For the same reason, an English-to-Japanese quiz asking for "Boar zodiac sign" could reasonably accept 猪 (いのしし). The pair 亥/猪 has no exclusion (亥 has quiz_exclusions: [], and 猪 has only [動物]).
   Remedy: Add a short qualified note that the sign's animal is named いのしし and that 亥年 is also called いのしし年, while keeping the warning against using い for a live animal. Consider a conservative 亥/猪 quiz_exclusions guard. That guard would not claim the two words are synonyms.
   Evidence:
   - Daijisen 亥年 (the very entry the article cites) ends "…その年に生まれた人。いのしし年。"
   - Kanjipedia, word い: "①十二支の一二番目。イノシシ。"
   - Kanjipedia, character 亥: "動物ではイノシシ。"
   - JMdict 2853749: 亥の年 has the readings いのとし and いのししのとし.
   - content-format.md's exclusion rule: a pair needs an exclusion when "a learner could reasonably accept either title" for either word.
   Confidence: high that the いのしし naming is documented and missing from the article. Medium that a quiz exclusion is needed, because I did not check the app's actual candidate pairing.

Optional:
- Daijisen sense 4 (the year or day of the Boar) could be shown with 亥の日 (いのひ, JMdict 2845246) next to 亥年.
- The 亥/豚 pair ("Boar zodiac sign" vs "pig") is a weaker ambiguity. JMdict's "the Pig" is only an English cycle label, so no guard seems needed.
- Line 50 starts with "Likewise", which links awkwardly to the previous sentence; small wording polish.
- Confirmed with no defect:
  - Metadata: readings ガイ, カイ / い in source order; 6 strokes; radical 亠 no. 8; grade 9 = name-use kanji, supported by Daijisen ［人名用漢字］.
  - Quiz selections: quizOnyomi [] and quizKunyomi [い], with a linked support row.
  - Reading layers kept separate: ガイ only through 辛亥 しんがい (JMdict 1883690); カイ qualified as source-only; ゐ given as historical kana (Daijisen い〔ゐ〕).
  - Historical senses: both hour mappings (Daijisen sense 3, JMdict sense 2); the direction (30° west of north / ほぼ北北西); lunar month ten; all marked obsolete.
  - 干支 えと has the 12-sign sense, which JMdict restricts to the reading えと. The いどし reading is supported. Daijisen supports the "person born that year" note.
  - The three distractors 刻, 交, 亡 are described accurately against their cards and are clearly different in meaning. The mnemonic is labelled and does not need to repeat the Shinjigen pictograph account.
  - Both examples are natural, with correct readings and translations. The kanji and word cards link to each other, and the 年 links are correct.
  - The word has no jlpt field, so no level is inferred from the kanji.

Limits:
- I made no web_fetch calls. All Daijisen and Kanjipedia evidence comes from the supplied artifacts; I did not retrieve anything from the original sites, so I did not confirm that the artifacts match the live pages.
- Every assigned file and range was read in full: XML in chunks of 200 lines or fewer, guidance in chunks of 160 or fewer. No reads were truncated or failed.
- The confusable-words check was a single bounded search, not a full read of that file.
- Quiz conclusions come from the documentation in content-format.md, not from the app's code.
- This is a text-only review. There was no native, viewport or physical-phone check, and no glyph-rendering check.
- Overlap: the copilot-instructions guidance was already in my session context before I read the file. I did not read any author progress, audit or reconciliation records, or other reviewers' reports.
```
