I found no actionable defects. All four teaching files are CLEAN on all three facets. This was a read-only review: I edited, committed and filed nothing.

**Snapshot:** commit `69f0b3bd995c6071c1845a4e550c117d4233ae7d`. I did not inspect the working tree for uncommitted changes. The task says no uncommitted teaching is included.

**Scope:**
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`), as named by the runtime. No subagents or other reviewers were used.
- **Process:** I made one tool call at a time. I read no other reports and no author progress, audit, reconciliation or rationale files.
- **Rules and format docs:** `.github\copilot-instructions.md` and `content-structure.instructions.md` in full; `docs\content-format.md` lines 42–148; `docs\jlpt-levels.md` lines 1–105.
- **Teaching files, all three facets, read in full:** `kanji\梓.md`, `kanji\橘.md`, `words\梓.md`, `words\橘.md`.
- **Source metadata:** `batch-011-input-metadata.json` in full, including the raw KANJIDIC2 entries for both kanji.
- **Dictionary packets, every line returned:**
  - `batch-011-jmdict.xml`, lines 1–584 (30 entries)
  - `comparisons-jmdict.xml`, lines 1–812 (26 entries)
  - `supplement-jmdict.xml`, lines 1–362 (12 entries)
  - `notes-jmdict.xml`, lines 1–151 (3 entries)
- **Comparison kanji, read in full:** 木, 辛, 新, 村, 橋, 商, 相, 矛.
- **Comparison words, read in full:** 木, 植物, 植える, 植木, 果物, 果実, 実, 柚, 花, 香り, 印刷, 出版.
- **`confusable-words.md`:** searched only, not read in full. A search for 梓, 橘, 植木, 柚, 植物, 果実, 果物, 印刷, 出版, 香り, azusa, tachibana, citrus and plant found no matches.
- **Kotobank:** fetched all four assigned URLs.

**Verdicts:**
- `kanji\梓.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN
- `kanji\橘.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN
- `words\梓.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN
- `words\橘.md`: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN

**Findings:** None.

What I checked, and what supports each point:
- **Metadata:**
  - KANJIDIC2 gives シ and あずさ for 梓, and キツ and たちばな for 橘. Both cards keep these in the same order, and the stroke counts, radical 75 and N1 level also match.
  - Each selected quiz reading (あずさ, たちばな) has its own reading row and links to the matching word article.
  - The disabled on'yomi questions (`[]`) are explained with real words: 梓 し and 上梓 じょうし for シ; 柑橘類 and 柑橘 for キツ. The name reading きっ is out of scope.
- **梓, tree species:** Seisenban (the compact Nihon Kokugo Daijiten on Kotobank) says the accepted identification is now ヨグソミネバリ (Japanese cherry birch). It records キササゲ (catalpa) and アカメガシワ (Japanese mallotus) as earlier views. The cards present this as "usually … in Japanese descriptions", which fits.
- **梓, Chinese reference and printing:**
  - Seisenban's し entry gives 梓 as the Chinese name of a catalpa-type tree. Its usage note says 上梓 comes from Chinese use of 梓 wood for printing blocks.
  - Heibonsha's encyclopedia says the Chinese 梓 is not the Japanese アズサ. This supports the article's "different naming histories".
- **梓, printing-block sense and abbreviations:**
  - JMdict's printing-block sense has no reading restriction, Seisenban lists it under あずさ, and Daijisen lists 梓 (し) as a printing block.
  - The bow and spirit-medium abbreviations are attested in both sources.
  - JMdict's "usually written in kana" flag applies only to the birch sense, and the article qualifies it that way.
- **橘:**
  - Seisenban supports the old name for mandarins eaten fresh, the wild plant (evergreen, white flowers, bitter and sour fruit), the flower sense (= 花橘) and the family crest. Its two fragrance-related senses are an incense wood (香木) and a blended incense (薫物).
  - 枸橘 (からたち) and 酢橘 (すだち) appear in JMdict as whole-word spellings.
- **Example sentences:** All four are natural Japanese, and the translations fit.
- **Quiz exclusions:** Each is a direct pair based on the actual titles. Neither card adds a printing or fragrance cluster.
- **Look-alike kanji:** The other kanji offered as wrong answers have plainly different meanings.

**Optional:**
1. `kanji\梓.md:33,39` and `words\梓.md:34` gloss 梓弓 only as a spirit bow, matching JMdict. Seisenban's あずさ② cites a Man'yōshū line where the bow seems to be held for hunting. That suggests 梓弓 also has a plain "azusa-wood bow" sense. I didn't fetch the 梓弓 entry itself, so this is unconfirmed.
2. In `words\橘.md:36`, "perfume" could read "incense". The source senses are an incense wood (香木) and a blended incense (薫物).
3. `kanji\橘.md:45` could say what 商 shares with 橘's right side: the lower box-like enclosure.
4. `kanji\梓.md:43` ("not source-only…") and `kanji\橘.md:41` use contributor wording that could be simpler for learners.
5. 字通 classifies 梓 as phonetic, with 辛 as the sound element; 説文 instead treats it as an abbreviated 宰. The mnemonic is labelled and the `structure-unclassified` tag is conservative, so this could be noted as debated.
6. Seisenban also lists 橘 as another name for からたちばな (*Ardisia crispa*), which is not a citrus. A note could mention this; it is not required.

**Limits:**
- **Line numbers:** The file viewer returned no line numbers, so I counted the cited lines by hand. They may be off by one or two.
- **Kotobank coverage:**
  - The 上梓 page's Daijisen section had a heading but no body. Only its Seisenban body was checked.
  - The 柑橘類 page returned only the Heibonsha encyclopedia entry, which I read in full across two fetches. It had no Daijisen section.
  - I didn't fetch 梓弓, which was not among the assigned URLs.
- **Packets and provenance:** The JMdict packets are frozen supplied evidence, not my own upstream retrieval. I didn't open `n1-source-snapshot.json`.
- **App behaviour:** I didn't simulate the app's automatic fallback choices.
- **Not covered:** This review is textual only. No phone or native-speaker testing was done, and nothing here measures frequency or teaching effectiveness.
- **Tool use:** Calls were strictly serial with no overlap.
