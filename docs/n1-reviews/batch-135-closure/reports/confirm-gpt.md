Snapshot: `2ef25d33ab16d928ac4f0a845b4d8f78005223da`, compared with `163b384e6cb8f75c06fe395f7b144cdd8b105673`. Reviewer: GPT; the exact runtime variant is not independently exposed to me.

Scope:

Read all nine revised cards in full and checked every changed hunk against correctness, coverage, quiz safety and beginner-phone comprehensibility. Checked the supplied meaning options for all 15 cards and all 29 reading prompts: 16 on and 13 kun. The six unchanged cards were included in those quiz checks.

**Confirmation-packet files opened:**

- In full: `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, and `evidence\README.md`.
- In full: `snapshot\kanji\{博,履,巡,弾,恵,憶,揚,救,模}.md`.
- In full: `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`, and `checks\link-targets.tsv`.
- In full: `evidence\QuizBuilder.kt`; in part: `evidence\KanjiReadings.kt:1–155` and `evidence\Words.kt:210–245`.
- In full: `evidence\kanjipedia-outside-readings.json`, `evidence\kanjipedia-救.txt`, `evidence\kanjipedia-巡.txt`, `evidence\daijisen-草.txt`, `evidence\daijisen-草履.txt`, `evidence\jmdict-cited-entries.xml`, and `evidence\kanjidic2-甫.xml`.
- In full: `evidence\joyo\{p18,p98,p155,p163}.txt` and `evidence\kanjivg\{0535a,0752b}.svg`; SVG structure/path data inspected, not rendered.
- `evidence\reading-exposure-163b384e.txt`: complete machine comparison with the revised exposure audit; differing blocks and summary inspected. Apart from introductory descriptions, only 巡, 救 and the summary differ.

**Original-packet files opened this round:**

- `snapshot\kanji\{博,厳,及,姿,履,巡,弾,彫,恵,憶,我,揚,救,暇,模}.md`: complete machine reads for metadata/table comparisons and old-to-new hunk verification. 彫 was additionally read in full as prose; the other unchanged cards' prose was not re-reviewed in full this round.
- In full as prose: `repo\kanji\{敬,道,達}.md`.
- `repo\kanji\{川,球,教,買,会,食}.md`: complete machine reads, with front matter inspected.
- `repo\kanji\{言,行,周,影,掘,細,蛍,賞}.md`: lines 1–14; `repo\kanji\得.md`: complete machine read, with front matter and lines 1–20 inspected.
- `titles\kanji-titles.tsv`: complete structured read for exact-title checks, not a prose review of the corpus.

**Independent public checks:**

- Inspected the actual reading inventories on all 15 live Kanjipedia character pages, using the URLs in `kanjipedia-outside-readings.json`. Their outside-Joyo markings agree with the supplied inventory.
- Inspected actual Weblio/Daijisen entries for 草履, 草, 相模, 酸模, 臆病, 弾, 彫 and 彫る. The last entry establishes the new finding below.
- Independently fetched the official Joyo PDF into memory, verified SHA-256 `d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42`, and checked the relevant passages on PDF pages 18, 98, 155 and 163.

**Verification results:**

- Applying the supplied patch in memory reproduces all nine revised cards. Across all 15 cards, the only front-matter changes are the two intended distractor lists; every reading table is unchanged.
- 弾 retains all sixteen example spellings and seventeen quoted gloss strings from its old introductory catalog, allowing the disclosed terminal-punctuation changes.
- All 45 meaning-distractor labels match the frozen title index. All eleven changed-line quoted link labels match their target titles; all 175 relative-link occurrences across the nine revised cards resolve. No batch card lists a kanji as both distractor and exclusion.
- Reviewed all fifteen meaning-option sets, including the new 巡 options `river | road, way | reach, plural suffix` and 救 options `respect; honor | ball; sphere | teach, instruct`. No new meaning-answer ambiguity was established.
- Independently checked G1/G2 against the reading builder. For 救, fixed Starter readings セン, ドウ and タツ outrank グ/ク; かう, あう and くう outrank たすける. These provide enough higher-tier distinct choices whenever fallback is needed. 巡's three Starter-tagged providers fill all three wrong slots directly.

Dispositions:

- **G1 — RESOLVED** — 敬 replaces 求 at `救.md:13`; the explanatory additions at lines 48–49 match Kanjipedia and the context card. Curated outcomes and fallback-tier bounds exclude グ, ク and たすける in the packet-defined shipped/Starter pools, including added borrowed holders.
- **G2 — RESOLVED** — `巡.md:13` now uses 川, 道 and 達, all Starter-tagged. Every curated outcome fills three safe slots: kun labels are かわ, みち and -たち; the fallback cannot introduce まわる. The replacement meaning options and shape comparisons are defensible.
- **G3 — RESOLVED** — `博.md:27` correctly places the dot inside the seven-stroke 甫 component. Naming the compressed component 甫 is acceptable in this explicitly modern-shape mnemonic despite KanjiVG's variant flag; no historical identity or phonetic claim is made.
- **G4 — RESOLVED** — `弾.md:25–33` now gives five short sense bullets; the remaining catalog is explicitly secondary at line 67. Examples, readings and glosses are preserved, and the rare-reading table remains intact.
- **GR — DECLINE ACCEPTED** — I accept not introducing a new Kotlin harness or duplicate quiz engine for this content-only correction. The before/after audits document the two regression cases, but are not an executable automated regression guard. This acceptance does not verify the author's toolchain claims or future workflow promises.
- **OA — DECLINE ACCEPTED** — The remaining six compression suggestions were expressly nonblocking. Deferring those unchanged paragraphs in a confirmation round is reasonable; 弾's actionable case has been addressed.
- **OB — RESOLVED** — `巡.md:39`, `恵.md:40` and `揚.md:40` now distinguish the grouped stem from the displayed めぐる, めぐむ and あげる forms, agreeing with `ReadingKey.display`.
- **OC — RESOLVED, for the specified inventory expansion** — Both audit commands include the verified Kanjipedia outside readings for all fifteen characters. This extends the old attestation inventory as requested, but does not cover every reading attested in dictionary word entries; G5 demonstrates that remaining limitation.

Verdicts:

Correctness: **CLEAN** — no new actionable factual defect established in the revised hunks. The added 憶/臆 spelling comparison agrees with the official table and cited JMdict entries; 履's historical kana agree with Daijisen.

Scoped coverage: **CLEAN** — no reading-table coverage was lost, and no new material omission was established.

Consistency and quiz safety: **NEEDS FIX** — 彫, G5. G1/G2 are resolved; no other new actionable quiz defect was established.

Comprehensibility: **CLEAN** — G4 and OB are resolved; no new actionable comprehension defect established in the nine revised cards.

Confirmation: **NEEDS FIX** — all eight response items have accepted dispositions, but the all-batch quiz check established the additional issue G5.

Findings:

**G5 — major; consistency and quiz safety; `kanji\彫.md:10–13` — える can be offered as a wrong kun-reading in a permitted padded Starter session.**

This card is unchanged in the revision; its current text is the original packet's `snapshot\kanji\彫.md`. This is a newly established finding, not a regression attributed to the nine-card patch.

**Claim and impact:** Daijisen explicitly records **え・る〔ゑる〕【▽彫る／×雕る／×鐫る】**, with carving/engraving senses. Thus える is a legitimate outside-Joyo reading of 彫る, even though neither the pinned metadata nor Kanjipedia's character-reading inventory lists it. A Starter practice session borrowing both 彫 and 得 can display える as wrong alongside the selected correct answer ほる.

**Evidence and reachability:**

1. The actual [Daijisen 彫る entry](https://www.weblio.jp/content/%E5%BD%AB%E3%82%8B) supplies the reading and carving sense, with literary usage examples. This is not a name reading or an inference from a search result.
2. 彫 protects only its metadata readings `ほ.る` and `-ぼ.り`, plus the on-reading and their generated variants. The resulting ten protected keys do **not** contain える.
3. `repo\kanji\得.md:9–11` has `kunyomi: [え.る, う.る]`, no narrower quiz-kun override, and no Starter tag. Against ほる, both readings score 3; `maxByOrNull` keeps the first, **え.る**, displaying **える**.
4. The supplied exposure audit's 彫/ほる block shows that the plain Starter session has **no curated providers** and **17 drawable wrong keys**. The full-pool options audit lists only three distinct tier-4 keys: ほそる, ほたる and ほめる. If Starter contained all three, they would fill all wrong slots and only three keys could be drawn—not seventeen. Therefore at least one tier-3 slot is reachable.
5. Adding 得 adds a tier-3 provider, not a new tier-4 key. A permitted shuffle placing 得 first among tier-3 providers admits える into that remaining slot. This follows `evidence\KanjiReadings.kt:98–112`. The packet explicitly treats “Starter plus the borrowed target and one extra holder” as a permitted session model.

The full N1/All pools remain protected by their higher-tier choices for this particular reading. The defect is the padded Starter path, not an arbitrary two-card hypothetical pool.

**Why the supplied zero-hit result misses it:** `kanjipedia-outside-readings.json` has no outside reading for 彫. The exposure audit adds the standalone-noun reading えり, but not the verb reading える. Its zero padded-session count therefore does not test this attestation.

**Remedy:** Include `--extra 彫=え.る` in the exposure check, retaining the existing extras. Prevent that valid reading from being drawn—for example through separately sourced wrong-answer protection, or safe curated providers available in every applicable pool, as done for 巡. Preserve the pinned-metadata policy and recheck both reading and meaning options after the chosen correction.

**Confidence:** high against the packet's documented pool model and supplied builder. Reachability is analytical, not a captured app session.

Optional:

None additional.

Limits:

- Neither supplied audit executes Kotlin or the app's random generator. I inspected the builder and mutation helper and performed bounded independent logic checks; I did not rerun a whole-corpus simulator, app/JVM tests or repository test suites.
- The G5 tier-capacity proof uses the supplied audit's Starter outcome count and full-pool tier inventory, checked against the actual builder and specific provider metadata. I did not independently rebuild the complete 118-card Starter inventory. The app's stack/pool construction is taken as documented in the packet; this is not a claim about arbitrary custom pools.
- Sampled seeds are sanity checks, not exhaustive proofs. The older `reading-options.txt` warning about 巡–まわる is a capacity-blind false positive here: its three curated slots are already full.
- The zero-hit summary is relative to the attestation inventory and its treatment of readings. It is not proof against all public-dictionary readings, as G5 shows. Name-only overlaps are treated separately; for example, the audit explicitly permits some 恵 name-reading strings among wrong options. Those were not newly classified as ordinary on/kun defects.
- The audits test single extra borrowed holders, not every combination of borrowed cards. The explicit G1/G2 bounds remain safe when additional cards are added to the documented Starter base.
- No phone rendering, stroke animation or runtime UI validation was performed. Unchanged word articles and stroke files were not re-reviewed this round. Future authoring-note changes, the author's JDK availability and `RESPONSE.md`'s exact model-ID attribution were not independently verified.
- One patch output and one public-entry output overflowed the tool's display limit; needed passages were retrieved in bounded follow-ups without opening the automatically generated overflow files. An initially literal gloss comparison failed on the disclosed punctuation changes; the corrected terminal-punctuation-normalized comparison passed.
- All tool calls were serial, one per tool-bearing response. No parallel calls, subagents, background jobs, other sessions, recursive listings or corpus scans were used. No other review or unprovided author material was accessed. The only intentional write is this report.
