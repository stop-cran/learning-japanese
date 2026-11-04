**Snapshot:** `e18a46afb0ded56ddff74924d4b1c6ea339550d8`, identified by the task as the frozen signed snapshot, with no uncommitted teaching included. I could not independently verify Git HEAD, signature, or worktree status using the permitted tools. Review was read-only; no files changed.

**Scope:** One reviewer, **GPT-6.1 Sol** (`gpt-6.1-sol`), reviewing correctness, scoped coverage, and textual phone comprehensibility throughout `kanji\鳳.md` and `words\鳳凰.md`.

Read scope completed:
- Entire `.github\copilot-instructions.md` and `.github\instructions\content-structure.instructions.md`; `docs\content-format.md:42–148`; entire `docs\jlpt-levels.md`.
- Entire input metadata, including all seven raw KANJIDIC2 elements: 鴻・鳥・風・鳳・鵬・凡・凰.
- Complete lexical packet, lines 1–636, **34 families**, and complete comparison packet, lines 1–253, **11 families**: **45 distinct complete JMdict families**, including spellings, readings, restrictions, senses, and flags. The overlapping seven-family core packet was not read or counted separately.
- Entire comparison cards: `kanji\鳥.md`, `kanji\風.md`, `kanji\鶴.md`, `kanji\鷹.md`; `words\鳥.md`, `words\鶴.md`, `words\鷹.md`, `words\絵.md`, `words\模様.md`, `words\布.md`.
- Scoped search of `docs\confusable-words.md` for the reviewed bird terms, example vocabulary, and phoenix labels; no matches returned.
- All six supplied raw dictionary ranges: 鳳 1740–1830; 鳳凰 1833–1885; フェニックス 1740–1815; おおとり 1740–1810; Kanjipedia 鳳 50–140; Kanjipedia 鳳凰 45–85. Relevant Japanese entry headings and bodies were inspected.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鳳.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\鳳凰.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification or native-device acceptance.

**Findings:** None.

The principal checks supporting these verdicts were:

- **Metadata and curation:** 鳳 preserves the frozen source’s ordered `ホウ・フウ`, empty kun list, 14 strokes, and classical radical 196. Explicit `[ホウ]` selects supported practice; explicit `quizKunyomi: []` disables kun questions rather than invoking omitted-field behavior. ホウ has its own linked 鳳凰 row. フウ remains explicitly source-only, without an invented allocation or an assertion that it is invalid.
- **Reading-layer distinctions:** JMdict 1518400 supports 鳳凰／ほうおう; 1518370 separately documents rare 鳳／ほう, and 2564400 documents 凰／おう. Family 2267700 and Daijisen’s spelling-specific mythical-bird subentry support 鳳／おおとり. Its placement under KANJIDIC2 nanori therefore does not make the lexical reading merely a personal name. The performer homograph is correctly separated using family 2732830 and Daijisen’s 大取（り） entry.
- **Meaning and translation boundaries:** Daijisen and Kanjipedia support the traditional male/female pairing. Both cards qualify that explanation rather than requiring two birds or sex identification in every use. JMdict 1518400’s Egyptian-phoenix association warning and Daijisen’s フェニックス sense support the distinction from the rebirth tradition. Motif usage is supported by Daijisen’s crest sense and JMdict 2685310, not merely inferred from English “phoenix.”
- **Examples and navigation:** Both Japanese examples are natural, with fitting particles, polite past/existential predicates, complete readings, and accurate translations. They describe representations, not living-animal sightings. Both directions of the 鳳↔鳳凰 link resolve to the reviewed files with the correct whole-word reading. Word metadata includes 凰 despite its absent kanji card, and no vocabulary level is inferred from 鳳’s kanji level.
- **Shape and quiz semantics:** The visible 鳥 component and surrounding-frame mnemonic are accurately described and explicitly distinguished from etymology. The three curated kanji distractors’ actual labels—“wind; style,” “crane (bird),” and “hawk; falcon”—are semantically distinct from the target. The direct 鳳凰／鳥 exclusion guards the broad “bird” label; it does not imply transitive exclusions with 鶴 or 鷹. No additional ambiguous pair was established among the inspected comparisons.

**Optional:** None required. Broader mythology, historical derivation, additional compounds, and personal-name instruction are outside the necessary scope.

**Limits:** No requested read failed or was truncated. All XML reads used explicit ranges of at most 200 lines. Tool calls were serial, without parallel execution. Repeated content included the prescribed instruction-file acquisition and the same Daijisen おおとり entry appearing in two supplied HTML resources; this was not additional independent corroboration.

Dictionary evidence was **supplied frozen evidence**, not independently retrieved upstream. No web fetches, hash recomputation, Git verification, validator execution, or repository-wide title/exclusion audit were performed. Kanjipedia lists ホウ・ブウ and supplies a phonetic derivation; those observations do not invalidate the preserved KANJIDIC2 フウ or the card’s expressly nonhistorical mnemonic.

Comprehensibility verdicts concern text only. The reported absence of 凰 from three bundled cmaps was not independently checked and does not itself establish glyph failure. Supported-native four-production-family rendering, lookalikes, article/reciprocal navigation, system Back, offline behavior, visual acceptance, and physical-phone testing remain pending. Unchanged pilot/all40/160 acceptance does not establish fresh batch-038 acceptance. Fresh non-skipped Android, current-main, CI, and public-ZIP checks likewise remain unverified here; batch-037 XML is not substitute evidence. Compatible Android `f9b59a2+` and outstanding phone/general-release acceptance remain explicit qualifications, not a blanket owner-testing veto.
