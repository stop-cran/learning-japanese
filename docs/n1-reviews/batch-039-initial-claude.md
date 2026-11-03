I completed the read-only review. All three cards are textually clean apart from one minor finding on the 鴻 kanji card: it leaves out the sound-component explanation that its own cited source gives.

**Snapshot:** 9b21ba549417d25c54183a37e4f5cc35a2689638, committed content only, as the task assigned. I could not check Git independently (no shell), so I relied on the working-tree files.

**Scope:**
- **Reviewer:** one reviewer, Claude Opus 5.5 (`claude-opus-5.5`). All tool calls were made one at a time.
- **Files and facets:** `kanji\鴻.md`, `words\鴻.md` and `words\鴻鵠.md`, each checked for correctness, scoped coverage and textual comprehensibility.
- **Guidance and level docs:** `.github\copilot-instructions.md` to EOF (lines 1–228), the full content-structure instructions, `docs\content-format.md` lines 42–148 and `docs\jlpt-levels.md` to EOF.
- **Metadata:** `batch-039-input-metadata.json` in full, including all eight KANJIDIC2 elements.
- **Dictionary packets:** all 47 frozen JMdict families: 17 + 20 + 10 across the three packets, every line read in ranges of 200 lines or fewer.
- **Comparison cards:** kanji 紅, 鳴, 島, 鳥, 鶴, 鷹 and 鳳, plus words 鳥, 鶴, 鷹, 鳳凰, 動物, 生き物, 生物, 小鳥, ぴよぴよ, ちゅんちゅん, 鷹揚, 偉大, 湖 and 図鑑.
- **Searches:** one bounded search of `confusable-words.md` (no matches) and two title-overlap searches across `kanji\` and `words\`.
- **Supplied dictionary pages:** all eleven saved Weblio/Kanjipedia pages, at the assigned line ranges.

**Verdicts:**
- **`kanji\鴻.md`:**
  - Correctness: CLEAN.
  - Scoped coverage: NEEDS FIX (minor).
  - Comprehensibility: CLEAN.
- **`words\鴻.md`:**
  - Correctness: CLEAN.
  - Scoped coverage: CLEAN.
  - Comprehensibility: CLEAN.
- **`words\鴻鵠.md`:**
  - Correctness: CLEAN.
  - Scoped coverage: CLEAN.
  - Comprehensibility: CLEAN.

**Checked and supported:**
- **Metadata:** readings in source order (コウ, ゴウ / おおとり, ひしくい, おおがり), 17 strokes and radical 196 match KANJIDIC2. Both quiz lists are curated, non-empty and each has its own linked reading row.
- **ゴウ:** no word allocating ゴウ appears in the 47 families. Daijisen and Kanjipedia list only コウ as the on-reading, so the "source-only" qualification is supported.
- **おおとり:** 鴻 is a spelling in JMdict 2267700, and Daijisen's kanji entry lists おおとり as a kun-reading.
- **おおがり:** Daijisen's 大雁／鴻 entry gives two senses: another name for ヒシクイ, and another name for ガチョウ. The card matches.
- **ひしくい:** JMdict 2157630 marks the word "usually written using kana", and ヒシクイ is a kana-only spelling. The article says this.
- **鴻鵠:** こうこく matches JMdict 2843944's two senses and Kanjipedia's "大人物や英雄のたとえ". Kanjipedia also supports "くぐい = old name for the swan".
- **Proverb description:** matches Kanjipedia's 燕雀安んぞ… entry.
- **Distractors:** 紅, 鳴 and 島 are visually related, and none of their titles means a large bird.
- **Links and exclusions:** links between the kanji card and both word articles work in both directions. The exclusions are sensible pairs. The kanji title is unique.
- **大トリ note:** JMdict ties the spelling 大トリ to the kana おおトリ, but Daijisen writes it as おおとり, so the card's wording is acceptable.

**Findings:**
- **Minor; scoped coverage (also affects comprehensibility); `kanji\鴻.md`:22–24.**
  - **Claim and impact:** the card tags 鴻 as `structure-unclassified` and offers only a memory aid ("Notice 江 beside 鳥"), adding that this is "not a historical or phonetic rule". But Kanjipedia's 鴻 page, which the card itself cites, explains the character as a 形声 compound: 鳥 plus the sound component 江 (カウ→コウ). A learner may read the disclaimer as denying any sound link, and misses a sourced aid for the selected reading コウ (江 is also read コウ).
  - **Remedy:**
    - Add a hedged line, for example "Kadokawa Shinjigen, via Kanjipedia, explains 鴻 as 鳥 + sound component 江 (コウ)", or reword the disclaimer.
    - Changing the tag or `phonetic` metadata is an editorial decision.
  - **Evidence:** `batch-039-kanjipedia-kou.html` lines 89–96: "形声。鳥と、音符江(カウ)→(コウ)とから成る。", sourced to 角川新字源 改訂新版.
  - **Confidence:** high that the source says this; medium that it belongs in the teaching text, since it rests on a single reputable source.

**Optional:**
- **偉大 quiz guard:** `words\鴻鵠.md` excludes 鷹揚 ("magnanimous; composed") but not 偉大 ("great; outstanding"), which its own Synonyms section compares directly. An English-to-Japanese prompt "great; outstanding" could plausibly tempt someone who knows 鴻鵠 as "great person". The ambiguity is weaker than a true synonym pair; 大 ("large; great") is a lesser case.
- **Full proverb:** `words\鴻鵠.md` could quote the whole proverb with its reading, 燕雀安んぞ鴻鵠の志を知らんや (えんじゃくいずくんぞこうこくのこころざしをしらんや).
- **"Phoenix" translations:** it could also note that some English translations render 鴻鵠 as "phoenix" (JMdict 2834550, 2042230), which supports the article's existing caution.

**Limits:**
- **Dictionary access:** the dictionary pages were the supplied saved copies only; I did not fetch anything independently. The JMdict packets are supplied frozen evidence, not a fresh upstream lookup. I did not open `n1-source-snapshot.json`, so I did not check that 鴻 belongs to the N1 set myself.
- **Glyphs and phone:** I did not check font coverage for 鵠 or the inherited 凰. This was a text review, not a native-app or physical-phone test.
- **Pending checks:** Android, current-main, CI and public-ZIP checks remain pending, and phone/general-release acceptance is outstanding.
- **Confusable-words check:** the `confusable-words.md` check was a single keyword search, not a full inventory.
- **Overlapping reads:** the guidance file was already in my context before I read it as assigned. The `batch-039-kou.html` range repeats the ひしくい and おおがり entries from their separate files.
