Snapshot: `fb236071b6355b28423581c96a35a8ca1084a193`, compared with `2ef25d33ab16d928ac4f0a845b4d8f78005223da`. Reviewer: GPT; the exact runtime variant is not exposed to me.

Scope:

Read all four changed cards—履, 巡, 彫 and 救—in full and checked every changed hunk against all four facets. Reviewed the supplied meaning options for all fifteen cards and both complete reading audits, covering all 29 prompts: sixteen on and thirteen kun.

**Files opened this round, with depth:**

- In `confirm2-135-gpt`, read in full: `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, and `evidence\README.md`.
- Read `snapshot\kanji\{履,巡,彫,救}.md` in full as prose. All fifteen `snapshot\kanji\{博,厳,及,姿,履,巡,弾,彫,恵,憶,我,揚,救,暇,模}.md` also received complete machine reads for exact comparisons, metadata and prompt checks; the other eleven did not receive another full prose review.
- Read in full: `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`, `checks\link-targets.tsv`, `evidence\jmdict-cited-entries.xml`, `evidence\daijisen-彫る.txt`, and `evidence\joyo\p110.txt`.
- App sources: `evidence\QuizBuilder.kt` read in full; `evidence\KanjiReadings.kt:1–165` and `evidence\Words.kt:210–248` inspected. All three files additionally received complete machine comparisons against their earlier-confirmation counterparts.
- Shape evidence inspected in part: `evidence\kanjivg\05468.svg:35–62`, `05186.svg:35–55`, and `09ad8.svg:35–65`. These files received complete machine reads to select those ranges; no rendering was performed.
- `evidence\reading-exposure-2ef25d33.txt`: complete machine comparison by card block, plus direct inspection of lines 189–214.
- In `confirm-135-gpt`, complete machine reads of `snapshot\kanji\{博,履,巡,弾,恵,憶,揚,救,模}.md`, `checks\quiz-safety.txt`, and `evidence\{QuizBuilder.kt,KanjiReadings.kt,Words.kt}` for comparisons.
- In `batch-135-163b384e`, complete machine reads of `snapshot\kanji\{厳,及,姿,彫,我,暇}.md` as the unchanged predecessor text. Read `repo\kanji\{円,高,見}.md` in full as prose; inspected front matter of `repo\kanji\{川,道,敬,球,教,求}.md`, which received complete machine reads. Read `titles\kanji-titles.tsv` completely as a structured index. Read `rubric\copilot-instructions.md:1–180`.

**Independent verification:**

- The four patch sections reproduce the revised snapshots exactly. The other eleven cards are unchanged. Only the 彫 and 巡 distractor lists change in front matter; metadata readings, titles, tags and exclusions are preserved.
- All 45 displayed meaning-distractor labels match the frozen title index, and each target title is unique. Only 巡 and 彫 have changed meaning-option sets. Their new labels are defensibly wrong in both directions: `river | road, way | see, look` and `yen, circle | high, expensive | see, look`.
- All nine changed-line quoted link titles match their targets after allowing terminal sentence punctuation. All 68 relative-link occurrences in the four changed cards resolve. No changed card lists a distractor among its exclusions.
- Independently enumerated every curated reading combination using the actual provider metadata and the supplied mutation rules. 彫 has one on combination and 75 kun combinations; 巡 has two on combinations and three kun combinations. Every combination supplies three distinct, nonexcluded wrong keys. All five relevant providers—円, 高, 見, 川 and 道—are Starter-tagged.
- For 彫, the on labels are エン, コウ and ケン. The kun choices are one from each disjoint group: `{まるい, まる, まど, まどか, まろやか}`, `{たかい, たか, -だか, たかまる, たかめる}`, and `{みる, みえる, みせる}`. None is える or えり.
- For 巡, the on choices are セン, ドウ/トウ and ケン; the kun choices are かわ, みち and one of みる/みえる/みせる. None is まわる.
- Thus, with the supplied default four-choice builder, 彫 and 巡 cannot admit a fallback answer in any pool containing their three providers, regardless of additional borrowed holders. The builder still traverses fallback candidates, but its capacity guard accepts none.
- The before/after exposure-audit card blocks differ only for 巡 and 彫; the other thirteen card bodies are identical. The older audit reproduces 彫–える with either borrowed 得 or 選. The revised audit includes that attestation and reports no ordinary-reading production or one-holder padded collisions.
- Inspected actual live Daijisen entries for [彫る](https://www.weblio.jp/content/彫る), [草履](https://www.weblio.jp/content/草履), [草](https://www.weblio.jp/content/草), [円](https://www.weblio.jp/content/円), [高](https://www.weblio.jp/content/高) and [見](https://www.weblio.jp/content/見). Inspected the relevant historical-kana and ▽ conventions in its [legend](https://www.weblio.jp/shogakukan.jsp). The new 彫 paragraph accurately distinguishes える/ゑる from the noun's obsolete えり; JMdict entry 2265620 supports the noun spellings, reading qualification and glosses. The 履 rewording agrees with ザウ and ソウ（サウ）.
- Independently fetched the official Joyo PDF into memory, verified SHA-256 `d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42`, and inspected page 110's actual 彫 row. It lists チョウ and ほる, not える or えり. KanjiVG supports the new 冂/口 comparisons; these remain modern-shape comparisons, not historical claims.

Dispositions:

G5 — **RESOLVED** — `彫.md:13` replaces the unavailable Starter providers with 円, 高 and 見. Independent exhaustive curated-combination checks establish that all three wrong slots are always occupied before fallback can add anything, protecting both える and えり across the documented pools and their borrowed-card extensions. The accompanying explanation and sources at lines 41, 52 and 55 are supported. The replacement meaning options introduce no established ambiguity.

Verdicts:

Correctness: **CLEAN** — no new actionable defect established in the four changed cards or changed hunks.

Scoped coverage: **CLEAN** — no metadata reading or existing example coverage was removed; the newly discussed readings are explicitly outside practice.

Consistency and quiz safety: **CLEAN** — G5 is resolved, 巡's replacement preserves its protection, and no new actionable defect was established across the fifteen supplied option sets and 29 reading prompts.

Comprehensibility: **CLEAN** — the new qualifications remain secondary to the central meanings; the shape comparisons and the non-shape rationale for 見 are explicit. No new actionable defect established.

Confirmation: **CONFIRMED** — G5 is resolved and no new actionable finding was established.

Findings: None.

Optional: None.

Limits:

- The supplied audits are Python ports, not execution of Kotlin or the app's random generator. Their scripts were not supplied or inspected. I independently checked the relevant Kotlin logic and exhaustively enumerated the changed curated combinations, but did not run Android/JVM tests, repository suites, or a corpus-wide simulator.
- Pool construction is taken from the packet's documented N1/All and Starter model; its implementation is not independently established by the supplied builders. The 彫/巡 proof applies to default four-choice questions in pools containing their three providers, not arbitrary reduced pools or different option counts.
- The audits' zero-hit summaries are relative to their attestation inventory, not every possible dictionary headword. Their sampled seeds are not exhaustive proofs. Name-only overlaps remain separately disclosed, including three one-holder cases; these are not newly established ordinary on/kun defects.
- For unchanged cards that still use fallback, single-holder checks do not exhaust combinations of borrowed holders. The stronger filled-slot proof removes that limitation specifically for 彫 and 巡.
- `reading-options.txt` still labels 巡–まわる a HIT because that older check ignores already-filled capacity. Direct inspection of the builder and all curated combinations establishes that it cannot enter these questions. The exposure audit models that capacity.
- No phone rendering, stroke animation, publication state or future authoring-process promise was verified. Unchanged word articles and stroke files were not re-reviewed.
- Two initial exact-quotation checks stopped on terminal sentence commas inside quotation marks; the corrected comparison, normalizing only terminal punctuation, passed. One web-fetch output overflowed the display limit; relevant legend passages were retrieved in bounded follow-ups without opening the automatically generated local overflow file.
- Tool calls were serial, with no parallel calls, agents, background jobs, other sessions, recursive listings or corpus scans. No other review or unprovided author material was accessed. The only intentional write is this report.
