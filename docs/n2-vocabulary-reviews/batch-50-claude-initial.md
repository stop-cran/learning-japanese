I found two actionable defects across the 20 mappings: a missing quiz guard on ダイヤグラム (Minor) and a mis-classified sense on 竹 (Nit). Everything else is CLEAN within the scope I actually read.

# Snapshot
Frozen commit `8c71fae49b615f2d6f0de34c6b00d1b20d17dd7e`, parent `89c812eed40575c62f9f24cf97f3f6866473ecd0`. I reviewed committed content only. My file tools can't run Git, so the commit identity, the hashes, the equivalence checks and "だいぶ is byte-for-byte unchanged" all rest on the author's word, not on a check I ran.

# Scope
**Model:** claude-opus-5.5 (Claude family). I made no edits and used no agents or delegation.

**Read completely:**
- **Instructions:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-126`.
- **Assigned articles:** all 16 new articles and the 4 reused ones (だいぶ, 大木, 耕す, 竹).
- **Kanji:** `related.patch` and the cards for 詞, 植, 耕 and 竹.
- **Private files:**
  - The four compact JSONL files (20 mappings, 20 principals, 27 components, 176 labels) and `principal-reading.txt`.
  - All 11 family-inspection files, read with forceReadLargeFiles.
  - `supplemental-comparison-reading.txt`.
  - `public-bodies.txt` lines 1–390, which covers every heading grep found.
- **Mapping evidence:** the `docs\n2-vocabulary-sources.tsv` header and rows 982–1001, and `docs\n2-source-snapshot.json`.
- **Comparison articles:** full bodies of どんどん, 次々, スケジュール and 時間割. For about 90 other comparison cards I used only their titles and quiz exclusions (via grep and glob), plus the JMdict family renderings.

**Read only partly:**
- `review-evidence.json`: lines 1–80 and 27120–27460 (inspection receipts, quiz declarations, access limits).
- `docs\n2-vocabulary-snapshot.json`: lines 1–40.

**Not read:** `public-bodies.json`; the middle sections of `review-evidence.json`; `docs\confusable-words.md`; `docs\jlpt-levels.md`; the full bodies of the other comparison cards, including 表, 予定 and 計画. I fetched nothing from the web. I did not open any ledger, `batch-50.json` or any other private file.

# Verdicts
Cells are Correctness / Scoped coverage / Comprehensibility.

| Row | Article | Status | Correct | Coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:982 | 体操 | new | CLEAN | CLEAN | CLEAN |
| N2:983 | だいぶ | reused, unchanged N4 | CLEAN | CLEAN | CLEAN |
| N2:984 | 大木 | reused | CLEAN | CLEAN | CLEAN |
| N2:985 | 題名 | new | CLEAN | CLEAN | CLEAN |
| N2:986 | 代名詞 | new | CLEAN | CLEAN | CLEAN |
| N2:987 | タイヤ (source タイア) | new | CLEAN | CLEAN | CLEAN |
| N2:988 | ダイヤグラム | new | **NEEDS FIX** (B50-QZ-01) | CLEAN | CLEAN |
| N2:989 | ダイヤモンド | new | CLEAN | CLEAN | CLEAN |
| N2:990 | ダイヤル | new | CLEAN | CLEAN | CLEAN |
| N2:991 | 対立 | new | CLEAN | CLEAN | CLEAN |
| N2:992 | 田植え | new | CLEAN | CLEAN | CLEAN |
| N2:993 | 絶えず | new | CLEAN | CLEAN | CLEAN |
| N2:994 | 楕円 | new | CLEAN | CLEAN | CLEAN |
| N2:995 | 高める | new | CLEAN | CLEAN | CLEAN |
| N2:996 | 耕す | reused | CLEAN | CLEAN | CLEAN |
| N2:997 | 滝 | new | CLEAN | CLEAN | CLEAN |
| N2:998 | 炊く | new | CLEAN | CLEAN | CLEAN |
| N2:999 | 焚く | new | CLEAN | CLEAN | CLEAN |
| N2:1000 | 蓄える | new | CLEAN | CLEAN | CLEAN |
| N2:1001 | 竹 | reused | **NEEDS FIX** (B50-MAP-01; mapping metadata only) | CLEAN | CLEAN |

**Separate assessments:**
- **Kanji edits — CLEAN.**
  - 詞 adds 代名詞 to the シ row (line 28), to Common words (line 34) and to the entry list at line 45 (1412340).
  - 植 adds 田植え to the う.える row with "(植え うえ)" (line 29), to Common words (line 35) and to the entry list at line 46 (1442810).
- **Existing reciprocity — CLEAN, no edits needed.** 耕 already links 耕す (lines 31/35/45) and 竹 already links 竹 (lines 31/35/44).
- **Component metadata — CLEAN.** Every headword kanji appears in `kanji:`, and every existing component card is linked from the word side. Kanji without cards (操, 楕, 滝, 炊, 焚, 蓄) are correctly left unlinked.
- **Reused articles preserved — CLEAN.** The patch doesn't touch だいぶ, which is still N4 with `kanji: []` and still mentions 大分/だいぶん (line 23). 大木, 耕す and 竹 gain only `jlpt: 2` and an appended note. Their IDs, titles and existing guards are unchanged.
- **Mappings — CLEAN except N2:1001.** The JMdict entry numbers, flags (rare タイア, outdated 瀧, rare 橢円, search-only 煮く and だ円) and the additional senses match the family renderings. Senses taught from outside JMdict (the transport chart for ダイヤグラム, incense for 焚く) don't invent JMdict sense numbers.

# Findings
**B50-QZ-01**
- **Severity:** Minor.
- **Facet:** quiz_exclusions.
- **Location:** `words\ダイヤグラム.md:9` (reasoning at lines 39–41).
- **Claim and impact:** The card guards 予定 ("plans; schedule") and 計画 ("plan; planning") because of the schedule overlap, and says "English schedule can describe the transport use". It does not guard スケジュール ("schedule; program of activities") or 時間割 ("timetable; class schedule"). A quiz can therefore show a valid "schedule" or "timetable" meaning as a wrong answer, in either direction.
- **Remedy:** Add スケジュール. Also add 時間割 after judging that pair directly.
- **Evidence:**
  - Daijisen sense 2 for ダイヤグラム (public-bodies.txt:129-136): 「列車など…運行状況を1枚の図に表示したもの。また、その運行予定。ダイヤ。」 (a one-page chart of train operations, and the operating schedule itself).
  - JMdict ダイヤ (2855660) sense 1 is "(railway) schedule, timetable".
  - スケジュール.md:9 already excludes 予定, 計画, 時間割 and ダイヤ.
  - 時間割.md:9 already excludes ダイヤ.
- **Confidence:** High for スケジュール; medium for 時間割.

**B50-MAP-01**
- **Severity:** Nit/Minor.
- **Facet:** mapping, sense selection.
- **Location:** `docs\n2-vocabulary-sources.tsv:1001` and `words\竹.md:52-53`.
- **Claim and impact:** The source gloss is "bamboo,middle (of a three-tier ranking system)". Its second item is exactly JMdict sense 2. Even so, the row selects only sense 1, lists sense 2 as additional, and the card's note says the list selects "plant sense 1". This understates what the source asks for, although the article still teaches the middle-rank sense.
- **Remedy:** Set `sense_indices` to `1,2`, clear `additional_senses`, and update the note.
- **Evidence:**
  - review-mappings.jsonl line 20 (`waller_definition`).
  - The JMdict family rendering of 1422230, where sense 2 is "middle (of a three-tier ranking system)".
  - Row 982 (体操) selects a sense 2 that its own source gloss doesn't contain, so there is no consistent "select only the primary anchor" convention that would explain row 1001.
- **Confidence:** Medium-high.

# Optional
None of these is a defect.
- **絶えず:** Consider guarding 続々 or 次々 ("one after another; in succession"). The card's own "Customers keep coming" example and its "successive" reason for guarding どんどん point that way, but JMdict gives neither word a "continuously" sense.
- **高める:** 持ち上げる ("lift up; flatter") and 増える ("increase in amount") are unguarded. Physical lifting and intransitive increase in quantity make leaving them out defensible.
- **対立:** 喧嘩 ("quarrel; fight") could be guarded. The card says confrontation needn't mean fighting, which makes the omission defensible.
- **蓄える:** Line 19 could link 貯 where it mentions the 貯える spelling.
- **大木:** The inherited ダイ→タイ wording is outside this batch's scope.

# Limits
- **Not verified by me:** Git identity, hashes, equivalence checks and the byte-for-byte state of だいぶ (all rest on the author's word).
- **Dictionary sources:** I made no fresh web fetches. The public bodies are the author's captures, and I made no claims about relative frequency.
- **Partial reads:** the unread middle sections of `review-evidence.json` and the unread `public-bodies.json` may hold records I didn't assess.
- **Comparison cards:** Apart from どんどん, 次々, スケジュール and 時間割, I judged them by title, exclusions and JMdict only. In particular, I didn't check that 表's body teaches ひょう. That guard carries little risk.
- **Missing cards:** I confirmed a card was absent only for the names I globbed.
- **Variant spellings:** I read the "every written Han" rule as covering headword kanji only, so variant-spelling kanji (橢, 瀧, 煮, 貯) are not expected in metadata.
- **Not tested:** I did not run quiz sampling, and this is not a native-speaker check of naturalness.
