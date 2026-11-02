**Snapshot:** 29b2b475771f929976570c27e24b9ac16278cdda committed teaching (base 79051b8), plus the evidence-only `docs\n1-reviews\batch-005-input-metadata.json`. I read the working-tree files. With no shell, I could not run git to confirm HEAD or a clean tree, so I'm assuming they match the snapshot.

**Scope:** Single reviewer, Claude Opus 5.5 (claude-opus-5.5). No other reports or ledgers were read. All three facets were reviewed.

Files read in full, with no truncation:
- Kanji cards: 松, 桃, 梅.
- Word articles: 桃, 白桃, 松竹梅, 松, 梅, 梅雨.
- All three JMdict packets: 8 + 17 + 1 = 26 families.
- The metadata JSON.
- Kanji cards for the distractors and other compound readings: 公, 村, 相, 兆, 毎, 海, 白, 竹, 雨.
- Word comparisons: 竹, 木, 植物, 植える, 果物, 果実, 実, ピンク, 桜, 最高, 上等, 一流, 高級, 位, 級, 段, 段階, レベル.
- `docs\content-format.md`, lines 40–157.

The word articles 最上, 特上 and 最良 don't exist; only their JMdict families were checked.

Live Kotobank pages fetched:
- **桃:** Digital Daijisen もも senses 1–5, Seisenban, and Jitsū.
- **白桃:** Seisenban はくとう and しろもも headings, and Nipponica. The Daijisen body was empty in the extraction.
- **松竹梅:** Seisenban [1]①② and [2] music; Nipponica, Heibonsha and the Daijisen Plus sake brand. The Daijisen body was empty in the extraction.

**Process deviation:** I once sent two reads (実 and ピンク) in a single response, which broke the serial rule. Every other call was serial.

**Verdicts** (correctness / scoped coverage / comprehensibility):
- kanji/松.md: CLEAN / CLEAN / CLEAN
- kanji/桃.md: CLEAN / CLEAN / CLEAN
- kanji/梅.md: CLEAN / CLEAN / CLEAN
- words/桃.md: CLEAN / CLEAN / CLEAN
- words/白桃.md: CLEAN / CLEAN / CLEAN
- words/松竹梅.md: CLEAN / CLEAN / CLEAN
- words/松.md, 梅.md, 梅雨.md (changed links and new support role only): CLEAN / CLEAN / CLEAN

Key checks:
- **Metadata:** Every on/kun entry matches KANJIDIC2 exactly: 松 ショウ/まつ, 桃 トウ/もも, 梅 バイ/うめ. Each is a one-item list, so the quiz selections equal the full lists. Strokes 8/10/10, radical 75 and grades 4/8/4 also match.
- **Reading allocation:**
  - ショウ+チク+バイ in 松竹梅 (JMdict 1349920).
  - ハク+トウ in 白桃 (JMdict 1475340).
  - バイ+ウ in 梅雨 (JMdict 1582960); つゆ is correctly taught as a whole-word (jukujikun) reading.
- **Ranking senses:** 松 sense 2 (highest), 梅 sense 2 (lowest) and 竹 sense 2 (middle) all match JMdict.
- **Other claims:** むめ is marked obsolete kana, as in JMdict. 桃 as an abbreviation of 桃色 is confirmed by Daijisen sense 2 (「桃色」の略). The 白桃 cultivar description (white flesh, pale red tint) and the separate しろもも heading match Seisenban. The two 松竹梅 senses cited match Seisenban [1]①②, and the article correctly leaves out the music and brand entries.
- **Navigation:** All seven support pairs link in both directions: 松–松竹梅, 松–松, 桃–白桃, 桃–桃, 梅–梅雨, 梅–梅, 梅–松竹梅.
- **Kanji distractors:** The wrong-meaning choices are clearly wrong against ordinary secondary senses. 公 is "public, official", 村 "village", 相 "mutual; aspect", 兆 "trillion; omen", 毎 "every, each" and 海 "sea, ocean".
- **Word exclusions:** The lists on 桃 and 白桃 directly pair the hypernyms (木, 植物, 果物, etc.) and ピンク. 白桃→桃 also covers 桃→白桃, because exclusions apply in both directions. 松竹梅 needs no exclusions: no displayed title of a rank or quality word is a reasonable answer for "pine-bamboo-ume grouping; three-tier labels".
- **Reading-question suitability:** The projected keys are しょう/まつ, とう/もも and ばい/うめ, one distinct stem per kind. Each selected reading has its own table row with a linked word. ショウ rests only on 松竹梅 (news2/nf47 priority marks), which is real but less frequent. That is still acceptable for N1 recognition. 相's ショウ duplicates 松's own reading, so I'm assuming the app's own-reading protection filters it out as a wrong answer. Usable wrong readings remain, such as 兆 チョウ and 毎 マイ.

**Findings:** None.

**Optional:**
1. **words/白桃.md, "Distinctive meaning":** Seisenban はくとう ① also means a white-flowered peach (= しろもも). The text implies the flower sense belongs only to しろもも.
2. **Ume vs. plum labels:**
   - words/桃.md calls すもも "Japanese plum", while kanji/梅 also lists that name for ume. Both are JMdict glosses; a short clarification would help.
   - The changed link in 梅雨 says "梅 means plum", which sits loosely with kanji/梅's caution. KANJIDIC also gives "plum", so it isn't an error.
3. **Pre-existing 松 (word) gaps:** It has no exclusions against 最高 "highest; best", 上等 or 高級, although 一流 already excludes 松. It also doesn't link 松竹梅.
4. **桃 phonetic note:** Jitsū treats 桃 as phonetic-semantic with phonetic 兆. A hedged note is possible, but the current mnemonic is allowed.
5. **Unlinked 梅:** The 毎 and 海 cards mention 梅 without linking it, now that the card exists.

**Limits:**
- JMdict evidence came from the coordinator's frozen packets, not my own retrieval. Only Kotobank was fetched live, and its Daijisen bodies for 白桃 and 松竹梅 did not extract.
- I did not check the JLPT N1 "community list" source.
- The behaviour of reading-question wrong answers comes from the docs, not from running the app.
- There is no native-speaker, physical-phone, font or measured-learning evidence.
- One read broke the serial rule, as noted under Scope.
