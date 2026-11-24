**Snapshot:** a22f26b78ce52a4991391092490dd1a118ea80b6, from the supplied packet only. I had no repository checkout and found no uncommitted changes in the packet.

**Scope:** One reviewer, Claude Sonnet 5.5 (claude-sonnet-5.5), covering correctness and scoped coverage.
- **Read in full:** rubric, snapshot, changed.txt, comparison-words.txt, kanji-1..4, words-1..4, sources.json, labels.txt, quiz.txt and primary.xml (10 entries).
- **Families:** I read families-1..7. They hold 104 families, which matches the count in quiz.txt.
- **Not assigned:** I give no comprehensibility verdict, only incidental notes.

**Verdicts**
- **New kanji:** 己 帆 帝 帥 幻 幽 庶 庸 廃 廉. Correctness is CLEAN and scoped coverage is CLEAN.
- **New words:** 自己 帆 帝国 元帥 幻 幽閉 庶民 凡庸 廃止 廉価. Correctness is CLEAN and scoped coverage is CLEAN.
- **Changed kanji, diff lines only:** 価 元 凡 国 止 民 自 閉. Correctness is CLEAN and scoped coverage is CLEAN. See findings 2 and 3 for 凡.
- **Older word 安い (廉い):** Correctness is CLEAN and scoped coverage is CLEAN. JMdict 1153670 gives 廉い for sense 1 with no restriction. The calm sense carries `stagk` 安い.

**What the CLEAN verdicts rest on**
- **Readings, kanji:** Every frontmatter reading in all ten new kanji matches the sources.json KANJIDIC2 metadata and has a table row. 幽's four kun are present with qualifications, and 帝's みかど is flagged as outside the standard table.
- **Readings, words:** Each word's reading allocation is consistent with its kanji cards. Examples are じ+こ, てい+こく, ぼん+よう and れん+か. 帆船 はんせん and 凡例 はんれい match JMdict.
- **Restricted senses:** 帝's second sense is restricted to 御門, as the card says. 帝国 sense 2 is an abbreviation and historical term, and the card says so. 幻 has three senses, as the card says. 己's おのれ, つちのと and な match 1266890, 1578530 and 2174450. 廃る and 廃れる match.
- **Grammar:** I checked these and found no error:
  - suru-verb uses and the を/passive explanations for 幽閉 and 廃止;
  - 凡庸な/だった and 廉価な/で/、with 安いカメラ versus *安いなカメラ*;
  - the の and に終わる attachments for 幻.
- **Furigana and translations:** All checked furigana, translations and Weblio URL encodings are correct.
- **Links:** All 18 required reciprocal pairs are present.

**Findings (no consequential defect established)**
1. **Minor, possibly Moderate; cross-facet quiz safety; UNVERIFIED.**
   - **Claim and impact:** Exclusions are written only on the new cards. labels.txt shows existing cards with near-duplicate labels and no reciprocal exclusion. The worst case is 自 "self, oneself" against 己 "self; oneself".
   - **Other pairs:**
     - 我 and 己
     - 安 and 廉
     - 凡 and 庸
     - 将 and 帥
     - 囚, 微 and 幽
     - 安い and 廉価
     - 中止, 止める and 廃止
     - 自分, 自身 and 自己
   - **Remedy:** Confirm that the app applies exclusions in both directions. If it does not, add the reciprocal `quiz_exclusions` on those existing cards.
   - **Confidence:** Low to moderate. The packet does not show the app's behaviour.
2. **Minor; structure; 凡.md Common words.** The 凡庸 bullet sits directly after the 凡て prose paragraph with no blank line. It reads as part of that paragraph and not as part of the word list. Move it up beside the other word bullets, or add a blank line. Evidence is the diff hunk only. Confidence is medium.
3. **Minor; provenance; 凡.md metadata.** The citation now adds 1478740, which is 判例 (families-5), not 凡例 (1523690). No visible prose depends on it. Confirm the existing text uses 判例, or drop it. Unverifiable without the full file.

**Optional**
- **幽 meaning line:** "幽か can describe a sound barely heard" relies on a usually-kana word whose 幽か form is only a secondary spelling (1590290). Consider showing かすか in kana, with 微か and 幽か as spellings.
- **廉価 and 安価:** Compare with 安価 あんか (1153740). JMdict records a "shallow; superficial; cheap" extended sense for 安価 but none for 廉価.
- **自己:** Add one contrastive 自己/自分 pair. The current examples do not show the claimed distinction.
- **幻 second example:** The sentence repeats itself and the translation is clumsy.
- **幻に終わる:** The idiom is not recorded in the JMdict senses in the packet, and no Daijisen entry for it is recorded either.
- **Kanjipedia-only readings:** Several are undocumented: 帝 タイ, 帥 ソツ and ひき.いる, 幻 まど.わす, 庶 もろもろ, 庸 もち.いる, 廃 や.める, and 廉 いさぎよ.い. Add rows only with a checked word.
- **廉 かど:** Note that かど is usually written in kana (2085290).
- **己 おのれ:** JMdict tags sense 1 as poetical. The card flags only the derogatory "you".
- **元帥:** JMdict lists 元師 as an irregular spelling. The "do not replace with 師" warning could say so.
- **帆船:** It also has the reading ほぶね, where 帆 is ほ.
- **庶民:** The line "Neither word contrasts with an elite" could be limited to their main senses. 市民 sense 3 is "bourgeoisie; middle class".
- **安い:** Say explicitly that 廉い writes only the price sense.

**Limits**
- I did not open Weblio or Kanjipedia. Daijisen and Kanjipedia content is taken from the author's recorded checks in sources.json.
- There was no native, device or app verification.
- I did not check shape mnemonics or glyph statements.
- Changed cards are seen only through diffs. Their existing reading tables, such as 元 ゲン and 国 コク, are not visible.
- Existence of link targets outside the new files is unchecked.
- Findings cite packet files and sections, because repository line numbers are not available.
