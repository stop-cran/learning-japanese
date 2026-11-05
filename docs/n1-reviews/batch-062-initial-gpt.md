**Snapshot:** `38ab6072d2041325142c54cf54be5d126928eb31`, as supplied. No uncommitted teaching included; review remained read-only. Git identity, signature and worktree correspondence could not be independently verified with the permitted tools.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and phone-**text** comprehensibility:
- Complete `kanji\俸.md`, `words\俸給.md` and `kanji\給.md`; only 給’s added 俸給 Common words line and tightly coupled behavior receive a verdict.
- Complete supplied XML: all **42 JMdict families**—16 lexical, 22 comparison and four further quiz families—and all **six KANJIDIC2 records** (給・年・付・俸・奉・棒), including restrictions, alternative forms and sense-local qualifications.
- Complete comparison cards: `kanji\棒.md`, `借.md`, `付.md`, `人.md`; `words\給料.md`, `給与.md`, `月給.md`, `収入.md`, `支給.md`, `支払.md`, `払う.md`, `支払う.md`, `代金.md`, `料金.md`, `小遣い.md`, `領収.md`, `サラリーマン.md`. Also inspected complete `words\納める.md` because 給与’s exclusions raised that directly relevant comparison.
- Actual titles, tags and distractors for all eleven assigned two-distractor legacy cards, retrieved with `rg`. The targeted `docs\confusable-words.md` search returned no matching rows.
- Every assigned guidance range in `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md`, `docs\content-format.md` and `docs\jlpt-levels.md`; complete pinned 90-line SVG; all three requested public dictionary pages freshly retrieved.

**Verdicts:**

| Teaching file / reviewed passage | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| `kanji\俸.md` — complete | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\俸給.md` — complete | **CLEAN** | **CLEAN** | **CLEAN** |
| `kanji\給.md` — added Common words line and coupled behavior only | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification. Unchanged 給 teaching was read as context, not independently cleared in full.

**Findings:** None.

Supporting checks:
- 俸 preserves the raw sole on-reading `[ホウ]`, empty kun list and corresponding practice subsets. Its selected reading has its own table row and linked, verified 俸給 example. Ten strokes, canonical 人 radical 9 and grade 8 match the supplied KANJIDIC2 record. The SVG contains ten numbered stroke paths and identifies left-hand 亻 as a variant of 人. The card explains that visible form without changing indexing metadata; its mnemonic is explicitly not etymology.
- 俸給／ほうきゅう and ホウ＋キュウ are supported. Both complete example sentences, kana, translations and grammatical explanations are sound. The combination explanation adequately connects salary with giving/paying and the resulting employment pay.
- The official-pay association is qualified correctly. Freshly retrieved **Seisenban Nihon Kokugo Daijiten, ほう‐きゅう【俸給】**, explicitly extends the word to company employees’ wages. Neither card invents government-only usage or universal legal distinctions among payroll terms.
- 年俸 is correctly ねんぽう, not ねんぼう. Fresh **Digital Daijisen, ねん‐ぽう【年俸】**, defines an annual basis or a year’s pay, supporting the distinction from payment schedule. JMdict supports the irregular 年棒 flag, 減俸／げんぽう and historical 俸禄／ほうろく. Historical, outdated and search-only forms were not promoted into modern metadata or ordinary spelling recommendations.
- Both mapped reciprocal pairs are present in both directions: 俸↔俸給 and 給↔俸給, **four directed links**. The relevant comparison links resolve to the inspected cards. No separate annual-pay article is required; the targeted file search found only 俸給 among word filenames containing 俸.
- The displayed wrong labels for 棒・借・付 are semantically distinct from salary/stipend. 給 genuinely overlaps pay, but has three authored distractors and is not one of the eleven legacy fallback cases. Adding 俸’s label introduces no established ambiguity for those eleven inspected targets.
- All nine exclusions on 俸給 are direct guards, not transitive synonym claims. The inspected labels and families establish no additional missing meaningful guard. 料金・小遣い・領収・サラリーマン—and 納める’s specifically qualified title—do not require exclusion merely because they concern money or employment.
- No vocabulary JLPT level is inferred from 俸’s kanji level.

**Optional:** None.

**Limits:** Supplied frozen XML and SVG were inspected directly, but their upstream hashes and snapshot provenance were not independently authenticated. All assigned file ranges returned without reported truncation.

The three fresh Kotobank extractions exposed relevant definitions for 俸 and 年俸 and the cited Seisenban definition for 俸給. On the 俸給 page, Digital Daijisen, Jitsū and Britannica sections returned attribution only; these were **not** treated as definitions. Historical gaiji in the character-page extraction were not fully readable, and its additional character readings were not substituted for frozen KANJIDIC2 metadata.

No measured frequency study, exhaustive historical reconstruction, whole-pool quiz certification or runtime verification was performed. Textual clarity and SVG count/shape inspection do not certify native drawing, glyph rendering or physical-phone readability. Compatible Android `f9b59a2` or later remains required for reading curation; physical-phone/general-release acceptance is outstanding, distinct from bounded owner testing.
