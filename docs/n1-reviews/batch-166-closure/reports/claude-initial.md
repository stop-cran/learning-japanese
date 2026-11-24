**Snapshot:** aca8b242dcad188c7927dac74e708cc668de6995 (base 7f13b789…), packet text only. I did not check it against a repository, so I can't say whether uncommitted changes are included.

**Scope:**
- **Reviewer:** one blind reviewer, Claude Sonnet 5.5 (claude-sonnet-5.5). This is not a multi-model review.
- **Facets:** correctness, with attention to reading allocations, restricted senses, grammar and scoped coverage. I also give comprehensibility verdicts.
- **Files read:**
  - Cards: kanji-1..4, words-1..3 (10 new kanji, 8 new words), changed.txt and comparison-words.txt (6 changed kanji, 4 changed words).
  - Evidence: primary.xml (339 lines), families-1..6, sources.json, quiz.txt, labels.txt.
  - Rubric and snapshot: both read.
- **Read limits:** reads were serial, one per turn. Two out-of-range probes confirmed the ends of primary.xml and families-1. No file showed a truncation notice.
- **Changed cards:** the six changed older kanji and four changed older words were reviewed from the diff and comparison text only.

**Verdicts** (Cor / Cov / Cmp = correctness / scoped coverage / comprehensibility)

*New kanji*
- 尾, 尿, 岐, 岳, 崇: CLEAN / CLEAN / CLEAN.
- 屯: CLEAN† / CLEAN / CLEAN. The トン.md link target is UNVERIFIED.
- 峡, 峰: CLEAN / CLEAN / CLEAN. The Daijisen-attributed parts are UNVERIFIED (see Limits).
- 崎: CLEAN / CLEAN (O1) / NEEDS FIX, minor (F3).
- 巧: NEEDS FIX, minor (F2) / CLEAN (O2) / CLEAN.

*New words*
- 尾: CLEAN / CLEAN (O3) / CLEAN.
- 尿: CLEAN / CLEAN / CLEAN (O4).
- 駐屯, 山岳, 海峡: CLEAN† / CLEAN / CLEAN.
- 分岐: CLEAN† / CLEAN (O5) / CLEAN.
- 峰, 崇拝: CLEAN / CLEAN / CLEAN.

*Changed (diff only)*
- 分, 山, 海, 駐, 拝, 利 kanji: CLEAN / CLEAN / CLEAN.
- 利口 and 岬: CLEAN / CLEAN / CLEAN.
- 上手い: NEEDS FIX, minor (F2) / CLEAN / CLEAN.
- しっぽ: CLEAN in content, with the minor navigation issue F4.

† The content matches the packet's JMdict entries. The only gap is that some entries are not cited (F1).

**Reading and sense audit (what was verified)**
- All 28 source reading rows reconcile with the KANJIDIC2 metadata in sources.json.
- The 11 quizzed readings are supported by cards or entries:
  - 尾 お, 尿 ニョウ, 屯 トン, 岐 キ, 岳 ガク, 峡 キョウ, 峰 みね, 崇 スウ.
  - 崎 みさき, which rests on the 崎 spelling in entry 1611700.
  - 巧 コウ, via 利巧 (1549550).
  - 巧 うま.い, via 巧い in 1310460, sense 1 ("esp. 上手い, 巧い").
- The restricted-sense and flag claims match the entries:
  - 巧い is limited to the skill sense and carries no priority tag.
  - 屯する is "usually kana".
  - 巧む is "usually kana".
  - 尿 ゆばり and いばり are obsolete (2872471).
  - 尿 しと sits in an "archaic, children's language" family (2872472).
  - 崎嶇 is a rare term.
  - 岳 だけ is a listed reading.
  - 峰 sense 2 is "back of a blade".
- The 尾 card cites senses 1–3 and leaves out sense 4 (mountain-foot slope).
- All 17 required link pairs plus 尾/しっぽ exist in both directions, with correct readings.

**Findings** (no consequential defect established; all four are minor)

- **F1 — minor; source records; confidence high.**
  - Taught compounds whose JMdict entries are in the packet are cited by no card:
    - kanji/屯.md Notes, the ton unit トン: 1457320 (families-3).
    - words/分岐.md, 分岐点: 1503370 (families-4).
    - words/山岳.md, 山岳地帯: 1302790 (families-2).
    - words/駐屯.md, 駐屯地: 1426960 (families-3).
    - words/海峡.md, 地峡: 1622730 (families-5).
  - The content is accurate; only the citations are missing.
  - Remedy: add those ids to the relevant Dictionary or Metadata lines.
- **F2 — minor; qualified claim; confidence medium.**
  - Where: kanji/巧.md, last Notes sentence; also the sentence added to words/上手い.md.
  - Problem: "Choose the spelling 巧い for skill here" reads as advice. JMdict marks all senses of うまい "usually written using kana alone", and 巧い has no priority tag.
  - Remedy: "巧い is a recognized spelling of うまい (skill sense only). JMdict marks the word usually kana, and 巧い has no priority tag."
- **F3 — minor; comprehensibility; confidence high.**
  - Where: kanji/崎.md, キ row.
  - Problem: "a rare word and an outside-table on reading" is garbled. Kanjipedia lists キ as outside the table.
  - Remedy: "a rare word; this on reading is outside the standard-use table."
- **F4 — minor; navigation and consistency; confidence medium.**
  - Where: words/しっぽ.md, Synonyms.
  - Problem: "尾 (お)" is still unlinked now that words/尾.md exists. The しっぽ↔尾 exclusion is declared only on 尾.
  - Remedy: link [尾](尾.md); consider adding 尾 to しっぽ's exclusions, or confirm the engine treats exclusions symmetrically.

**Optional**
- **O1.**
  - Add one Notes sentence to 崎.
  - The standalone JMdict headword 崎 is read さき (1297220, news1 nf10, and Kanjipedia's only kun).
  - The quizzed みさき rests on the non-priority 崎 spelling in 岬.
  - Both facts are true, and the card already discloses the outside-table status.
- **O2.**
  - The priority-tagged 巧み (1278290) is taught but not quizzed. The quizzed コウ and うま.い rest on non-priority alternates, which is disclosed.
  - Consider a future 巧み or 技巧 card.
  - In kanji 利's Common words, consider listing the headword 利口 (also 利巧) rather than 利巧.
- **O3.** 尾 vs しっぽ: add a register or frequency note. The packet has no evidence for this, so I did not assert it.
- **O4.** 尿: note that 小便 is colloquial. JMdict glosses it "piss; pee".
- **O5.** 分岐: add a one-line formality contrast with 分かれる. JMdict 分かれる sense 1 is also "branch; fork; diverge".
- **O6.**
  - Kanjipedia-only readings are not mentioned: 屯 チュン / なや.む; 岐 わか.れる / ちまた; 峰 フ; 崇 シュウ plus four kun.
  - JMdict 峡 かい (2568690, archaic) is also unmentioned.
  - These are not required.
- **O7 — quiz-safety pointers, outside my facet; unverified.**
  - 崎 uses the distractor 岸, but the baseline 岬 (same meaning) excludes 岸.
  - 屯 excludes 集 but not 拾 ("pick up; gather").
  - 岳 excludes 峰, but 峰 does not exclude 岳.
  - 尿 excludes 小便 one-way.
  - 巧/功/攻 share コウ, and 峡/狭/挟 share キョウ.
  - Confirm how the engine applies exclusions and builds reading options.

**Limits**
- I opened no external pages (Kanjipedia, Daijisen/Weblio, kotobank, JMdict site). Kanjipedia evidence is the reading lists in sources.json only.
- These Daijisen-attributed claims are UNVERIFIED:
  - 峡 はざま attribution.
  - 峰 ね.
  - 山岳 "high, rugged".
  - 海峡 "connects two bodies of water".
  - 岬 lake-shore.
- The following were not evidenced in the packet and are not verified:
  - JLPT N1 "community list" tags.
  - Shape mnemonics and component descriptions, which I judged from general knowledge.
  - Link-target existence for トン.md, 駐車.md and 湾.md, since labels.txt is partial.
  - Quiz-engine semantics.
- Example naturalness is my own judgment. There is no native, device or whole-deck verification.
- The packet's line numbers are unavailable, so findings cite files and sections.
