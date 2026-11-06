# Batch 079 — final visual confirmation report

**Model:** Claude Opus 5.5 (claude-opus-5.5).

## Snapshot
- Evidence HEAD: dcfcbb43b30b63beef3f689d3ebae4e412c9120c
- Reviewed teaching: 0f7f20e93b1e20cbc9943011e9ac69b20f75086e
- Native envelope: 3fdc0bf952e299060b5a07ac372bb6d926595a4c
- Teaching and manifest are unchanged since my textual confirmation, according to supplied evidence. I did not verify this in Git myself.

## Scope
**What I read in this pass:**
- 30 one-resource host turns, each with exactly one view call:
  - Resource 1: the full source packet, read with forceReadLargeFiles and not truncated.
  - Resources 2–30: the 29 PNGs, in the order listed.
- No read failed or was truncated, and no image was read twice.

**What I reviewed:**
- The four assignments: new kanji 冠, new word 王冠, reused word 冠 (including its navigation link), and only line 39 of kanji 王.

**Where my notes come from:**
- My earlier overlapping parallel run is set aside for breaking the one-call rule. Nothing here relies on it.
- My notes on resources 1–17 survive as a context summary written at the time I read them. They are not in my live context.
- Resources 18–30 are in my live context.
- Inherited, not reread: the lexical conclusions, the 177 dictionary families, the five raw character records, and my supplemental resolutions.

## Verdicts
CLEAN means no actionable defect was found within this scope. It is not exhaustive certification.

| Assignment | Correctness | Scoped coverage | Visual comprehensibility (bounded) |
|---|---|---|---|
| New kanji 冠 | CLEAN | CLEAN | CLEAN |
| New word 王冠 | CLEAN | CLEAN | CLEAN |
| Reused word 冠 | CLEAN | CLEAN | CLEAN |
| 王:39 | CLEAN | CLEAN | CLEAN |

**What I saw in the pixels:**
- **Readings table:** the full linked examples for カン (王冠 おうかん – royal crown; crown-type bottle cap) and かんむり (冠 かんむり – crown; ceremonial cap) are each complete in at least one scroll position: kanji-12, kanji-15, kanji-17 and system-back-to-kanji.
  - Other frames cut the table off at the edge. That is layout from the sideways scroll; no screen shows every column at once.
- **Notes:** the shape comparisons with 冗, 完, 元, 守 and 寸 are labelled as not claiming a shared origin.
- **Restrictions:** "peerless" and 冠たる are restricted to the かん reading in both 冠 articles and kept away from 王冠.
- **王冠 article:**
  - Royal and awarded crown are separated from the crown-type metal closure.
  - The examples use かぶっている and 外しました.
  - The distinctions from 帽子, 蓋 and 栓 are explained.
- **Quizzes:**
  - Meaning: the choices are crown; peerless, exempt; be spared, superfluous; redundant and frugal; thrifty. None of the wrong choices is a second correct answer.
  - Readings: on'yomi choices ケン/カン/ハン/ジョウ and kun'yomi choices かねる/しおり/かんむり/かつら, each marked correct, then "2 of 2" Done.
- **Selection screen:** "N1 · 111 cards", Meaning 1 due, Drawing 1 new, Readings 2 due. These match the seeded fixture state.
- **Fonts:** all 35 scoped Han characters and the whole words appear in Gothic, Mincho, Textbook and Brush, with no blanks, replacement boxes or misleading look-alikes. 冖 and 宀 are visibly distinct.

## Findings
None. My original Finding 1 (the "named for its crown shape" claim at 王冠.md:16,27) stays resolved by the supplied Daijisen sense 3. The pixels show the same text.

## Optional
These earlier suggestions are kept as optional, not defects:
- Add JMdict 1181450 to the 王 Metadata line. The pixels confirm it lists only 1629200, 1181700 and 1181480.
- 開ける or 取る may be more typical than 外す (low confidence).
- Consider the title "crown cap" instead of "bottle cap".
- Add a compound such as 冠婚葬祭 to the kanji card.
- Add a かん/カン bridge note.
- Add a 冠大会 example.

## Limits
**Rendering:**
- Partly resolved, for the API 35 emulator only.
- The fallback typeface cannot be identified from pixels or hashes.
- The 148 native raster records are fixture assertions, not 148 separate images I inspected.
- Some readings break across lines; this is layout only.

**Navigation, Back, persistence, offline behaviour and the ContentSync result** (1091 kanji, 5047 words, 111 N1, version a01eb85b17601ac0, 0 problems): these rest on supplied fixture and terminal assertions. Still images do not prove them.

**Drawing:**
- The strokes were nine injected reference strokes, compared by shape only. The screen showed the handwriting model was not available.
- Grade 1 being saved on Next is an assertion, not something the pixels show.
- None of this is human handwriting, a successful recall, or ML Kit recognition.

**Not covered:**
- Physical phone, native-speaker judgement, frequency, and safety of the large distractor pool.
- I did no upstream or Git verification myself.
- The pilot evidence and all-40-font evidence are inherited.
- Still outstanding: current-main integration, publication, CI, the immutable ZIP and general release.
