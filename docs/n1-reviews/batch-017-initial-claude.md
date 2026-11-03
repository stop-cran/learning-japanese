I found no actionable defects in the three files. One process failure: one response issued six parallel `view` calls, which broke the one-call-per-response rule (see Limits).

Snapshot: b751248ea6f9f3d2cd2084e7e744d9de4d7ff30d. No uncommitted teaching included. No files were written.

Scope:
- **Model:** Claude Opus 5.5 (claude-opus-5.5), one reviewer.
- **Guidance read:**
  - `.github\copilot-instructions.md`, lines 1–160 and 161–218.
  - `.github\instructions\content-structure.instructions.md`, complete.
  - `docs\content-format.md`, lines 42–148.
  - `docs\jlpt-levels.md`, lines 1–110.
- **Teaching files read in full:** `kanji\蛍.md`, `words\蛍.md` and reused `words\蛍光灯.md`.
- **Metadata:** all of `batch-017-input-metadata.json`, including the raw KANJIDIC2 element.
- **JMdict packets, all four read completely in ranges of 200 lines or fewer:**
  - `batch-017-jmdict.xml`: 1–200, 201–400, 401–600, 601–750.
  - `batch-017-comparisons-jmdict.xml`: 1–200, 201–400, 401–506.
  - `batch-017-notes-jmdict.xml`: 1–200, 201–385.
  - `batch-017-supplement-jmdict.xml`: 1–116.
- **Comparison kanji, complete:** 虫, 光, 灯, 火, 学, 栄, 営.
- **Comparison words, complete:** 虫, 蚊, 火, 光, 灯.
- **Partial inventory:**
  - `docs\confusable-words.md`: two searches, no pairs involving 蛍, 虫, 蚊, 火 or "insect".
  - Title searches across `words\` and `kanji\`.
- **Web source:** I fetched the given Kotobank URL myself.
- **Facets:** correctness, scoped coverage and textual phone comprehensibility.

Verdicts:
- **`kanji\蛍.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\蛍.md`:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\蛍光灯.md` (reused):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
  - The only change is the link `[蛍](../kanji/蛍.md)` on line 26. The relative path is valid and sits at the component introduction.
  - Title, level, exclusions, senses and the ケイ+コウ+トウ allocation match JMdict 1592540 (sense 2 is flagged dated). Other text is unchanged.

Findings: none.

What I checked:
- **Metadata:** KANJIDIC2 gives strokes 11, radical 142, grade 8, JLPT 1, and readings ケイ / ほたる in that order. The card's metadata matches.
  - Both readings are selected for the quiz, and each has its own reading row with a link to an existing word article.
- **ほたる:** JMdict 1252000 has only ほたる / ホタル (kana-only). The card is right that ケイ is not the reading of the standalone noun.
- **Two different spelling flags:** the "usually written in kana" note applies to the sense. The flag on 螢 marks an out-dated character form. The word article (line 26) keeps these apart.
- **ケイ:** supported by 蛍光 けいこう (1592530) and 蛍光灯 けいこうとう. This comes from the whole-word entries, not from splitting the kana.
- **Other words listed:**
  - 蛍石 ほたるいし / けいせき (1794750) is correct.
  - 蛍狩り (1252030) is "firefly watching", with "firefly catching" flagged as dated. Both articles describe this correctly.
- **Insect scope:** Seisenban ① says ホタル科に属する甲虫の総称 ("general term for beetles of the firefly family"). That supports "insects of the firefly family" in `words\蛍.md:15`. JMdict's "(Luciola cruciata)" is only a scientific-name parenthetical in the gloss; it does not narrow the word to one species.
- **Historical senses:** Seisenban ② gives a small leftover fire (埋火などの小さく消え残った火). Sense ③ is an Edo-period Gion sex worker or that tea house. [2] is Genji chapter 25.
  - `words\蛍.md:38` reports these accurately and marks them as not neutral modern substitutes.
- **Mnemonic:** the modern shape is ⺍ (3 strokes) + 冖 (2) + 虫 (6) = 11, which matches the explicitly labelled mnemonic. The 学 / 栄 / 営 contrasts match those cards.
- **Kanji quiz choices:** the distractors 学 "study", 栄 "flourish; glory" and 営 "conduct business; manage" are not defensible answers for "firefly".
- **Word exclusions:**
  - 蛍/虫 is justified: in the English-to-Japanese direction, "insect; bug" could reasonably be accepted for 蛍.
  - 蛍/火 rests only on the documented historical ember sense (see Optional).
  - No guard is needed against 蚊 "mosquito", 光 "light" or 灯 "lamplight; light".
  - No other word has an overlapping title; 輝く "shine; sparkle; glow" does not overlap.
- **Links:** kanji ↔ both words, and 灯's existing link to 蛍光灯, are all present.

Optional:
- **蛍/火 guard:** it is conservative. In modern use a learner would not accept "fire; flame" for 蛍. Keeping it is harmless, but if the curation rule is applied strictly, the historical ember sense alone is a weak reason.
- **"Seisenban":** `words\蛍.md:38` could expand this once to 精選版 日本国語大辞典 for readers.
- **Glow wording:** Seisenban says 発光する種はわずかである ("few species luminesce"). The articles' wording ("some species do not glow conspicuously", `kanji\蛍.md:22`, `words\蛍.md:15`) is weaker than that but still consistent; no change is required.
- **Kanji quiz fallback:** 蛍 shares the `structure-unclassified` tag with 虫 "insect; bug". The default quiz uses the three curated distractors, but larger quizzes that fill choices by tags could show it. Kanji cards have no exclusion mechanism, and the body already says 虫 is not an unambiguous wrong answer.

Limits:
- **Daijisen not read:** the simplified extraction showed only the heading, and the raw HTML I reached (at offsets 40000, 90000 and 200000) was CSS/JS; the body appears to load dynamically. The source lines attribute reading allocation and the older form 螢 partly to Daijisen; I could not check that attribution.
  - The teaching claims themselves are supported by JMdict and Seisenban.
  - I did not read 字通 or the 動植物名 body text.
- **Packets are frozen:** they are not a fresh upstream retrieval. I did not read `n1-source-snapshot.json`.
- **Line numbers:** the tool output did not include line numbers, so the cited lines are my manual count.
- **Partial inventory:** `confusable-words.md` was searched, not read in full.
- **Tool overlap:** one response issued six parallel `view` calls (kanji 光, 灯, 火, 学, 栄, 営), against the one-call rule. Every other response used one call.
- **Native/phone:** this is a text review only. I cannot certify device or native rendering, the old form 螢 against the bundled fonts, the four production families or physical-phone acceptance; that acceptance remains outstanding.
