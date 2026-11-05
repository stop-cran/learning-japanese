I found no defects in the four teaching files and no fixes are needed. One process lapse to flag first: early on I sent two `view` calls in a single response, which broke your one-call-per-response rule. Every other call ran on its own.

**Snapshot:** ea1dac1a6fd2c452db9cf602442e1f287ff95c67, as you supplied it. No uncommitted changes were included. I couldn't confirm the commit or the cleanness of the working tree myself, because only file viewing, search and web fetch were available.

**Scope:** Reviewer: Claude Opus 5.5 (claude-opus-5.5), working alone and without seeing any author or reviewer records.
- **Read in full:** `kanji\亭.md`, `words\料亭.md`, `kanji\料.md` and `kanji\停.md`.
- **Frozen sources:** the full lexical and comparison JMdict files (all 51 families) and all six KANJIDIC2 records (京, 高, 主, 亭, 停, 料).
- **Comparison articles:** the kanji cards 京, 高, 主, 享, 庭, 館 and 口, and the word articles レストラン, 食堂, 料理, 旅館, 宿, ホテル, 主人, 夫 and 御主人.
- **Guidance:** `copilot-instructions.md`, `content-structure.instructions.md`, `content-format.md` lines 1–180, `jlpt-levels.md` lines 1–32, and the pinned SVG.
- **Searches:** confusable-word rows, word titles, kanji titles, the eleven legacy two-distractor cards, and the N1 snapshot.
- **Fresh Kotobank retrievals:** the 亭 page and the 料亭 page.

**Verdicts:**
- **`kanji\亭.md` (new):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`words\料亭.md` (new):** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- **`kanji\料.md`, added Common words line only:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN. The unchanged metadata and context are kept as they were.
- **`kanji\停.md`, added link only:** correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN. The link sits inside the labelled modern-shape memory aid and makes no new claim about pronunciation.

**Findings:** None.

What I checked:
- **亭 metadata:** The readings テイ then チン, the empty kun list, 9 strokes, radical 亠 (no. 8) and grade 8 all match the raw KANJIDIC2 record in order.
  - The SVG has 9 strokes, grouped as 亠, 口, 冖 and 丁. That matches the memory aid, which is clearly labelled as not etymology.
  - Practice uses テイ only, and that reading has its own table row linking to 料亭.
- **Reading restrictions:** In JMdict 2589430, the pavilion noun allows both てい and ちん. The suffix senses (restaurant names, writers' and performers' pen names) are limited to てい. The card says exactly this.
  - Daijisen and the Nihon Kokugo Daijiten both have separate ちん noun entries for a garden or viewpoint pavilion. This supports keeping チン for recognition only.
- **亭 senses:** Daijisen's character entry (sense 3: a building that draws guests for food or entertainment) supports the "restaurant building" part of the title.
- **料亭:** JMdict 1554300 gives りょうてい as a noun meaning a traditional Japanese restaurant, especially a luxurious one. The Nihon Kokugo Daijiten defines it as a high-class restaurant serving mainly Japanese food.
  - The article's "especially upscale" and "chiefly Japanese cuisine" match these sources. Its hedges about menu, price, facilities, private rooms, reservations and entertainment do not contradict them.
  - 涼亭 (JMdict 2567560) is marked archaic and means a garden pavilion. The article handles it correctly.
  - The examples and their kana, the particle で, and the translations are all correct. Splitting the word as リョウ + テイ, both on readings, is correct.
- **Links:** All four directed links exist with correct relative paths: 亭↔料亭 and 料↔料亭.
- **Quiz exclusions:** 料亭 excludes レストラン and 食堂 on one side only, which the format spec says is enough for both directions. Both pairs are justified in both quiz directions:
  - JMdict glosses レストラン as "restaurant (esp. Western-style)", which a learner could accept for 料亭.
  - 食堂 has a second sense, restaurant or eatery, so it could also be accepted.
  - Other similar titles are distinct enough not to need exclusions: 旅館 (inn), 宿 (lodging), ホテル (hotel), 料理 (cooking or dish), 酒場 (bar or pub).
  - No row in `confusable-words.md` covers these words.
- **Kanji quiz:** 亭's wrong choices are look-alike shapes, and their titles (halt, capital, enjoy) can't be defended as answers for 亭.
  - None of the eleven legacy two-distractor cards (人, 休, 何, 入, 出, 口, 女, 日, 月, 男, 買) shares a tag with 亭.
  - None of their titles would make "pavilion; restaurant building" a defensible answer.

**Optional:**
- `kanji\亭.md:23`: briefly mention 亭's lodging sense, for example 旅亭 りょてい (inn; Daijisen sense 1, JMdict 1916170). This would explain why the card says "not overnight accommodation."
- `kanji\亭.md:41`: add 亭主 ていしゅ (host, master or husband; JMdict 1434160) as an unlinked common word. It doesn't need its own article.
- `words\料亭.md:20`: the romanized word "ryotei" first appears without introduction. Adding "(ryotei)" to the opening line would help.
- KanjiVG marks 丁 as the sound component. The card neither claims nor denies this, which is acceptable without a cited source.

**Limits:**
- The Daijisen body for 料亭 did not come through; only its heading and source line did. The 字通 section on the 亭 page also had no body text.
- The Heibonsha encyclopedia excerpts (Chinese relay stations, and 待合 houses relabelled as 料亭 under business-licensing rules) were treated as historical and regulatory context, not as definitions.
- The Kotobank pages were fetched fresh today. Everything else was the frozen XML supplied with the batch.
- The N1 snapshot JSON does not list 亭 in a searchable form. So N1 level rests on KANJIDIC2's jlpt=1 and the batch assignment, not on the kanjiapi list itself.
- I did not test validation, the manifest or the actual quiz algorithm, and the fallback audit doesn't cover larger or random quiz pools.
- This review covers the text only. No native-speaker, device, glyph-rendering or stroke-drawing evidence was supplied or checked. Phone and general-release acceptance are still outstanding.
