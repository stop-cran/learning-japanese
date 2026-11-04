**Snapshot:** `baa525f2d6c2331530bab235ce97a5eaf38b33af`, identified by the task as the frozen signed snapshot with no uncommitted teaching changes. Git identity, signature and worktree cleanliness could not be independently verified with the permitted tools. Review was read-only; nothing was changed.

**Scope:** One reviewer, GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual phone comprehensibility of the entire `kanji\鵬.md` and `words\鵬.md`.

Read completely:
- `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\jlpt-levels.md`; also `docs\content-format.md:42–148`.
- `batch-040-input-metadata.json`, including all eight complete raw KANJIDIC2 elements: 巨・月・鴻・鳥・朋・鳳・鵬・翼.
- All **29 complete JMdict families** across the three frozen packets: primary `1–159` (9 families), comparison `1–200` and `201–382` (16), support comparison `1–95` (4). Reviewed spellings, reading restrictions, senses, priorities and flags, including kana-only readings, rare spellings/terms, search-only spelling and sense-local restrictions.
- All six comparison kanji articles: 鳳・鴻・月・鳴・島・鳥.
- All ten comparison word articles: 鳳凰・鴻鵠・鳥・動物・生き物・生物・翼・月・鴻・鶴.
- All seven specified Japanese dictionary HTML sections, including their actual Daijisen/Kanjipedia headings and bodies, and the complete `docs\n1-source-snapshot.json`.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鵬.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\鵬.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review, not exhaustive certification.

**Findings:** None.

The following checks support those verdicts:

- **Readings and metadata:** 鵬’s complete sourced lists and order are preserved: `onyomi: [ホウ]`, `kunyomi: [おおとり]`. `quizOnyomi: [ホウ]` selects an exact supported reading; explicit `quizKunyomi: []` disables that question kind rather than invoking omitted-field/full-list behavior. The selected row links to the existing ほう word article, and the reciprocal component link is present. Nineteen strokes, classical radical 196/鳥 and grade 9 agree with the supplied character record.
- **Lexical identity:** JMdict 2267690 supports 鵬/ほう・ぼう as the peng transformed from a fish. Family 2267700 documents おおとり and distinguishes peng and fenghuang senses through “esp.” qualifications—not absolute spelling restrictions. The teaching appropriately avoids unrestricted substitution. Supplied Daijisen and Kanjipedia entries independently establish おおとり as a lexical bird reading, not merely a personal name. The word article correctly omits an independently unsupported vocabulary `jlpt`.
- **Meaning and example:** The fish-to-bird account, imaginary-creature qualification and distinction from 鳳凰 fit the inspected evidence. `鵬は想像上の鳥です。` has correct particles, reading and translation; it describes the creature without manufacturing a sighting or rare collocation. The 大トリ performer distinction matches the separate dictionary family and Daijisen entry.
- **Quiz integration:** The three curated kanji labels—“moon, month,” “animal call; ring,” and “island”—are genuinely wrong answers for 鵬. All seven declared word exclusions reference inspected existing articles and directly protect their pairs. Protection was not inferred transitively. 鳳凰’s actual label identifies a different mythical bird, so no additional 鵬/鳳凰 exclusion was established as necessary.
- **Presentation:** The modern-shape mnemonic is explicitly separated from etymology. Readings, long-vowel guidance, register qualifications and English translations make the two short articles understandable textually. The “Common words” heading is expressly qualified against an everyday-frequency interpretation. No missing prerequisite or necessary compound lesson was established within the one-kanji/support-word scope.

**Optional:** A source-attributed phonetic explanation could replace the conservative structural nonclassification: supplied `batch-040-kanjipedia-hou.html:97–101` identifies 鵬 as 形声, comprising 鳥 and phonetic 朋（ホウ）. This would be nonblocking enrichment; the current mnemonic does not assert an incorrect historical origin or deny a phonetic component. No 朋 card should be assumed.

**Limits:**
- Every mandatory file/range returned completely; no mandatory read was truncated or failed. All calls were serial, one per response, with no self-observed overlapping tool execution. No external execution records were inspected.
- The XML packets and seven HTML excerpts are **supplied frozen evidence**, not fresh upstream retrieval. Independent Kanjipedia fetching returned only copyright text; independent Weblio fetching returned Wikipedia-derived material, not the requested Daijisen sections. Neither lookup independently verified those dictionary bodies.
- The bounded `confusable-words.md` search returned no matches for the reviewed bird/category terms, 翼 or 月. This was not a complete repository-wide synonym inventory.
- An additional search for the snapshot-named `n1-kanji-source-20261102.json` failed at the attempted path; a bounded documentation glob found no such file. Exact frozen community-list membership and provenance hashes were therefore not independently reverified.
- Native glyph rendering, viewport behavior and physical-phone usability were not tested. Supplied cmap assurances are not native acceptance; inherited 凰 disposition is not fresh batch-040 acceptance. Prior pilot/all40/160 acceptance covers only unchanged production scope. Fresh batch-040 Android/native/current-main/CI/public-ZIP checks remain pending; batch-039 XML evidence was not reused. Compatible Android `f9b59a2` or later is required, and phone/general-release acceptance remains outstanding—not a blanket owner-testing veto.
- No other reviewers’ reports, author rationale, progress/audit/reconciliation records or canonical checkout were inspected.
