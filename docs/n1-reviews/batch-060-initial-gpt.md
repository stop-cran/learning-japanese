**Snapshot:** Supplied frozen commit `ea1dac1a6fd2c452db9cf602442e1f287ff95c67`; no uncommitted teaching included in the requested scope. Git identity, signature and worktree cleanliness could not be independently verified with the permitted tools. Review was read-only.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and phone-text comprehensibility:
- Complete `kanji\亭.md` and `words\料亭.md`; complete `kanji\料.md` and `kanji\停.md` for context, with verdicts limited to their specified changes and tightly coupled behavior.
- All **51 complete JMdict families**: 16 lexical families in `batch-060-jmdict.xml:1–275` and 35 comparison families in `batch-060-comparison-jmdict.xml:1–919`, including alternative spellings/readings, restrictions and sense-local labels.
- All **six complete KANJIDIC2 records** in `batch-060-kanjidic2.xml:1–460`: 京, 高, 主, 亭, 停 and 料.
- Complete assigned comparison articles: kanji 京, 高, 主, 享, 庭, 館 and 口; words レストラン, 食堂, 料理, 旅館, 宿, ホテル, 主人, 夫 and 御主人.
- Every assigned guidance range, the complete pinned SVG, relevant `confusable-words.md` search results, and actual title/distractor metadata for all eleven specified legacy fallback cards.
- Fresh retrieval of both assigned Kotobank pages. No author records, other reviews or adjudications were consulted.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\亭.md` — complete | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\料亭.md` — complete | **CLEAN** | **CLEAN** | **CLEAN** |
| `kanji\料.md` — added Common words entry and coupled behavior | **CLEAN** | **CLEAN** | **CLEAN** |
| `kanji\停.md` — added mnemonic link and coupled behavior | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification of the unchanged comparison/context articles.

**Findings:** None.

Supporting assessment:

- **Readings and character metadata:** 亭 preserves the complete ordered `[テイ, チン]` and empty kun list. Practice selects only テイ, with its own reading row and linked 料亭 example. チン receives an explicit pavilion-noun recognition example rather than being dismissed as name-only or assigned to restaurant-name suffixes. JMdict 2589430 permits both readings for the pavilion noun but restricts both suffix senses to てい; the explanation respects that distinction.
- **Count, shape and history:** Nine strokes, classical radical number 8/亠 and grade 8 agree with the raw KANJIDIC2 record. The pinned SVG contains nine ordered stroke paths and supports the described 亠/口/冖/丁-shaped mnemonic. Both new and reused mnemonics are explicitly modern-shape memory aids, not etymological or phonetic claims. The 停 link does not change that qualification.
- **Word identity and usage:** JMdict 1554300 supports 料亭・りょうてい as a noun meaning a traditional Japanese restaurant, especially a luxurious one. リョウ＋テイ agrees with the constituent metadata. Both example sentences, kana, translations and activity-location で are sound. The explanation distinguishes the restaurant noun from cuisine/dishes, pavilions and overnight lodging without inventing universal menu, price, room, reservation or entertainment requirements.
- **Public dictionary evidence:** On the fresh 亭 page, Shogakukan’s *Digital Daijisen* separately exposes the てい character entry and ちん pavilion entry. *Seisenban Nihon Kokugo Daijiten* separately exposes てい and ちん word entries, including historical lodging/residence senses. These do not contradict the article’s explicitly whole-word restaurant/lodging distinction. On the fresh 料亭 page, *Seisenban* identifies りょうてい as a noun for an upscale establishment chiefly serving Japanese cuisine. Historical encyclopedia excerpts and region-dependent legal/business categories were not treated as universal modern lexical requirements.
- **Spelling restrictions:** JMdict 2567560 separately marks 涼亭・りょうてい as archaic and defines the garden pavilion. The article correctly avoids presenting it as an alternative spelling of the restaurant noun.
- **Reciprocal navigation:** Both required pairs work in both directions: 亭→料亭→亭 and 料→料亭→料, four directed links with the correct word reading. The supplied reused changes introduce no metadata alteration.
- **Word quiz exclusions:** `quiz_exclusions: [レストラン, 食堂]` directly covers both required pairs. Under the documented exclusion-aware contract, each pair is excluded in both Japanese-to-English and English-to-Japanese questions, despite declaration on only one article. レストラン’s displayed “restaurant” label overlaps the restaurant category; 食堂’s ordinary eatery sense warrants considering more than its displayed cafeteria label. Neither exclusion was inferred transitively. 料理, 旅館, 宿 and ホテル remain meaningfully different from this restaurant noun.
- **Kanji choices and fallback:** 停, 京 and 享 are plausible visual distractors with semantically distinct displayed answers. 高, 庭 and 館 do not establish an additional ambiguity: height, garden space and a hall/large building are not interchangeable with “pavilion; restaurant building.” For the eleven assigned legacy cards—人, 休, 何, 入, 出, 口, 女, 日, 月, 男 and 買—the new 亭 answer supplies no established competing correct meaning. In particular, a pavilion used for resting is a place, not the action “rest.”
- **Text comprehensibility:** The short sections, selective kana, translated examples and explicit qualifications are understandable without relying on other articles. The 主/主人/夫/御主人 material provides comparison context but establishes no need to add 亭主 or other dictionary compounds. No vocabulary JLPT level is inferred for 料亭.

**Optional:** None.

**Limits:** All assigned local ranges were returned without unresolved truncation. The fresh Kotobank extractions exposed relevant definitions, but the 亭 page’s *普及版 字通* section and the 料亭 page’s *Digital Daijisen* section contained headings without definition text; those sections supplied no verification. Frozen XML was supplied evidence, not an independently authenticated upstream download. No measured-frequency claim, exhaustive historical account or corpus attestation of the original examples is certified.

The fallback audit is limited to the specified default four-choice exposure; it does not certify larger, random or live pools. Exclusion behavior was assessed against the supplied format contract, not executed in Android. Reading curation requires the stipulated compatible Android `f9b59a2+`; installed-client compatibility was not verified. Textual comprehensibility and SVG inspection do not establish native approval, glyph rendering, drawing quality or physical-phone/general-release acceptance. Those remain outstanding, not an independently established veto on bounded owner testing.
