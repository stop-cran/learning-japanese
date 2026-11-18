Snapshot: `48332d3258953779dda24c0df6fb1c649e6defbb`, compared with `d3c7394d38992b24d3689bc984fdb4a6cf60bc54`. Reviewer: OpenAI GPT, operating as GitHub Copilot; the exact deployed model/version is not exposed to me.

Scope:

Independently checked the revision, all four response IDs, every changed hunk against all four facets, and post-fix meaning/reading options for all 15 batch cards. Read all 12 changed cards completely. The unchanged cards 井, 傷 and 哀 remain covered by the initial linguistic review and this round's quiz, metadata and title checks.

**Confirmation-packet files read in full:**

- `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`
- `diffs\fix.patch`, through overlapping ranges; `diffs\changed-lines.txt`
- `snapshot\kanji\{丁,仰,但,傑,僕,卸,司,吐,呂,哲,唯,善}.md`
- `evidence\README.md`
- `evidence\jmdict-cited-entries.xml`, through successive ranges, including all eight entries
- `evidence\weblio-卸-daijisen.txt`
- `evidence\meta_scan.py`, read but not executed
- `evidence\meta-scan.txt`
- `evidence\QuizBuilder.kt`
- `checks\link-targets.tsv`
- `checks\quiz-safety.txt`
- `checks\reading-exposure.txt`, through successive ranges
- `checks\reading-options.txt`, through successive ranges

**Confirmation-packet files read in part:**

- `evidence\KanjiReadings.kt`: lines 1–130, including reading normalization, excluded keys, curated choices and fallback selection.
- `evidence\Words.kt`: lines 211–253, including the complete sound-change mutation function.

**Original-packet files opened for bounded comparisons/context:**

- `snapshot\kanji\{丁,井,仰,但,傑,傷,僕,卸,司,吐,呂,哀,哲,唯,善}.md`: complete-file programmatic comparisons or targeted metadata, reading-row and quotation checks; not a fresh full prose reread of the old cards.
- `titles\kanji-titles.tsv`, `titles\word-titles.tsv`: complete structured indexes for target identity, title and link checks; unrelated entries were not individually linguistically reviewed.
- `evidence\audits\{quiz-safety.txt,reading-exposure.txt,reading-options.txt}`: complete programmatic comparisons with the revised outputs.
- `evidence\app-code\{QuizBuilder.kt,KanjiReadings.kt,Words.kt}`: complete byte comparisons with the supplied confirmation copies.
- `evidence\kanjidic2-records.xml`: selected Japanese readings for 丁.
- `evidence\jmdict-families.xml`: selected record/reading queries concerning よほろ and 仕丁.

Also reread the Findings, Optional and Limits portions of my own `reports-137\initial-gpt.md`, starting at line 95. No other report was opened.

**Independent checks and regression coverage:**

- Verified all 16 patch hunks against both snapshots, covering all 24 changed lines. The changed-line inventory agrees. Front matter is unchanged in every revised card.
- Independently compared all 143 quoted linked titles across the 15 cards with the original title indexes: no mismatch. All 207 internal card-link occurrences resolve by those indexes. This verifies the author's result rather than merely accepting `link-targets.tsv`.
- Verified the four added citation IDs against their actual records: 丁 **2829360** = 仕丁; 呂 **1448890** = 当て字; 唯 **2672330** = 唯々 いい and **1623580** = 諾々 だくだく.
- Inspected fresh live Jisho API entries for 仰山, 仕丁, 卸下, 傑作, 当て字, 唯々 and 諾々, including readings, senses, restrictions and register. Additional よほろ searches were not treated as proof merely because a result was returned.
- Retrieved the actual live Digital Daijisen blocks for [卸](https://www.weblio.jp/content/%E5%8D%B8) and [よほろ](https://www.weblio.jp/content/%E3%82%88%E3%81%BB%E3%82%8D). 卸 has one Daijisen block, defining wholesale selling as `問屋が商品を小売店に売り渡すこと`.
- The new 仕丁 explanation accurately associates つかえのよほろ with the archaic forced-labor sense, not the palanquin-bearer sense restricted to the other three readings. The supplied complete-family evidence contains only that entry among readings containing よほろ. The card does not promote よほろ into metadata or practice.
- The new 傑作 labels qualify the jocular, dated second sense; the opening paragraph already distinguishes it from ordinary “masterpiece.” 卸下's military qualification matches its record and remains outside practice. The added citation IDs introduce no new reading or spelling claim beyond the cited entries.

Dispositions:

- **G1 — RESOLVED** — `仰.md:59` now explicitly restricts the quoted quantity sense of 仰山 to Kansai dialect and retains the usually-kana qualification. No other passage on the fully read card presents that example as unmarked standard vocabulary. Verified against JMdict **1238920** and the fresh [Jisho API entry](https://jisho.org/api/v1/search/words?keyword=%E4%BB%B0%E5%B1%B1).
- **G2 — RESOLVED** — All 16 reported title quotations now contain the correct internal comma spaces. Independent checking also found all 143 linked-title quotations accurate across the batch; no title metadata or quiz setting changed.
- **OP — DECLINE ACCEPTED** — This was a nonblocking presentation suggestion, not an established defect. Retaining the reference material does not invalidate this bounded correction. I confirmed the stated batch counts of 15 practice-policy sentences and 11 closing “more Daijisen examples” bullets; acceptance does not depend on the unverified published-corpus counts.
- **OW — RESOLVED** — `卸.md:25` now clearly defines the activity, “the act of a wholesaler selling goods to retail shops.” That preserves the actor and action in the actual Daijisen definition and removes the ambiguity identified in my optional suggestion.

Verdicts:

- **Correctness: CLEAN** — all changed hunks; no card differs.
- **Scoped coverage: CLEAN** — all 15 batch cards retain their metadata/practice coverage; the regional and register qualifications are accurate.
- **Consistency and quiz safety: CLEAN** — all 15 cards; quotations and links check out, and no new unsafe meaning or reading option was established.
- **Comprehensibility: CLEAN** — all 12 revised cards read coherently in full; the added qualifications clarify rather than contradict the surrounding explanations. OP remains nonblocking.

Post-fix quiz coverage is shown below. The meaning-choice IDs identify the complete English labels checked in `quiz-safety.txt`, not a judgment based on character identity alone. Asked readings use the displayed form, without metadata dots.

| Card | Meaning distractors checked | Asked reading(s) |
|---|---|---|
| 丁 | 打・丙・了 | チョウ・テイ |
| 井 | 耕・互・二 | い |
| 仰 | 迎・印・仲 | コウ |
| 但 | 昼・伸・他 | ただし |
| 傑 | 舞・休・体 | ケツ |
| 傷 | 湯・陽・揚 | きず |
| 僕 | 業・億・偉 | ボク |
| 卸 | 御・印・午 | おろす |
| 司 | 句・同・向 | シ |
| 吐 | 叫・吸・社 | はく |
| 呂 | 口・品・営 | ロ |
| 哀 | 衣・裏・袋 | あわれ |
| 哲 | 折・近・祈 | テツ |
| 唯 | 集・進・雑 | ユイ |
| 善 | 羊・着・差 | ゼン |

All 45 target/distractor pairings remain defensibly wrong in both directions from the displayed labels and ordinary senses. The 60 authored exclusions are unchanged; none is also an authored distractor. Every one of the 16 selected reading prompts retains its own linked word example.

The meaning builder applies exclusions symmetrically and also checks exclusions between chosen wrong options. Distinct titles alone would not prove semantic safety. The reading builder instead excludes every metadata on/kun reading and its generated variants, then selects from the curated candidates before fallback; meaning exclusions do not protect reading questions.

The revised meaning audit is identical to the original apart from empty lines. Both reading audits are identical after their command-label line, and all three supplied app-source copies are byte-identical to their original counterparts. The full reading exposure audit reports zero production hits and zero ordinary padded-session hits. Its eight latent collisions remain conditional risks, not eight demonstrated errors in the shipped pools. The additional one-holder padded 唯ゆ case remains name-only, not an ordinary on/kun answer.

Confirmation: **CONFIRMED** — G1, G2 and OW are RESOLVED; OP is DECLINE ACCEPTED. No new actionable defect established.

Findings: None.

Optional: None new.

Limits:

- The exact deployed GPT model identifier remains unavailable; no version number or independently verified model-family separation is claimed.
- All tool calls were serial, exactly one per assistant response, with results received before proceeding. No parallel calls, agents, other sessions, background jobs, recursive listings or corpus scans were used. Local reads stayed within the permitted packets and my initial report.
- The first bounded patch read was output-truncated near its end; an overlapping subsequent range recovered the missing material. I did not open an overflow file or treat the truncated return as a complete read.
- I did not verify OP's counts of 42 and 10 published cards outside this batch: doing so would require the prohibited corpus scan. Those counts are unnecessary to accept an explicitly optional layout suggestion's deferral.
- Reading-audit results are conditional on the supplied dictionaries, extra-reading set, metadata and pool definitions. They do not prove that every possible reading is known, or that future, smaller or differently padded pools are safe. Finite seeds are not exhaustive: the 呂 Starter sample saw 71 of 80 drawable wrong readings in 200 seeds. Reachability analysis and source inspection matter beyond sampled outcomes.
- I inspected the supplied app logic and audit outputs but did not independently rebuild whole-corpus pools or exercise the native quiz in a running app. Mechanical audits cannot themselves establish dictionary sense, register, English-label ambiguity or beginner comprehension.
- `meta_scan.py` checks exact Japanese-script runs of at least two characters containing kanji. It omits kana-only and single-kanji words, reports embedded substrings separately, and does not establish that a listed ID supplies the intended reading or sense. Its “0” is not proof of exhaustive citation completeness. The missing helper module was not sought outside the packet; I verified the four added IDs directly instead.
- Unchanged word articles and stroke files were not rereviewed in full this round. Their initial review stands; the supplied revision patch changes neither. No device-layout or native-speaker certification is claimed.
