Snapshot: `7a525b065ee613535c71d559bfc4ce0aea00beb1`, confirming the revision from `420a6669a2f1dafcc3a237e8b8604ff8cbc4201e`. Reviewer: GPT (OpenAI; exact runtime model identifier unavailable).

Scope:

This was an independent, read-only confirmation. I checked every changed hunk against correctness, scoped coverage, consistency/quiz safety and beginner-phone comprehensibility; reread all five changed cards and the changed word article completely; and examined the post-fix meaning and reading options for all 15 batch cards. Unchanged teaching prose was not subjected to a second complete initial review.

Files opened in this confirmation round are listed below. Brace lists identify each named file, not wildcard sampling.

**Confirmation packet, complete text reads**

- `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`.
- `diffs\fix.patch`, `diffs\changed-lines.txt`.
- `snapshot\kanji\{炊,端,粗,請,駄}.md`; `snapshot\words\透明.md`.
- `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\kanjivg\09759.svg`, `evidence\QuizBuilder.kt`.
- `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt`, `checks\link-targets.tsv`.
- `checks\lint.txt`, `checks\unittest.txt`, `checks\validate.txt`, `checks\budget.txt`, `checks\vocabulary.txt`, `checks\manifest.txt`. These logs were each short enough to read completely; reading them was not rerunning their commands.

**Confirmation packet, partial text reads**

- `evidence\KanjiReadings.kt`: lines 1–165, including reading normalization, selected-stem deduplication, exclusion construction and option selection.
- `evidence\Words.kt`: lines 205–310, including `ReadingOptions.mutations`.

**Original packet, complete machine reads with targeted comparisons/projections**

- `snapshot\kanji\{炊,端,粗,請,駄}.md` and `snapshot\words\透明.md`: compared against the revised files by applying the supplied patch entirely in memory. All six resulting files matched exactly.
- `evidence\audits\{quiz-safety,reading-exposure,reading-options}.txt`: compared with the revised audits.
- `evidence\app-code\{QuizBuilder,KanjiReadings,Words}.kt`: complete byte comparisons with the confirmation copies; all three were identical.
- `evidence\kanjidic2-records.xml`: parsed, with the relevant 端 and 駄 reading records inspected.
- `evidence\jmdict-families.xml`: parsed for the 駄 reading/headword absence check; the supplied families contain 104 entries with 駄, none with においうま.
- `titles\kanji-titles.tsv`, `titles\word-titles.tsv`: parsed for actual changed-line link titles and readings.

**Original packet, other reads**

- `snapshot\kanji\{焦,異,筋,納,脱,膨,致,透,鉢,隔}.md`: front matter only, for the unchanged cards' quiz inputs.
- `repo\words\煮る.md`: complete text.
- `snapshot\words\炊く.md`: lines 40–51.
- `evidence\public-source\weblio-端.txt`, `evidence\public-source\weblio-駄.txt`: complete text.
- My own `reports-136\initial-gpt.md`: Findings and Optional, lines 82–114.

Independent public checks inspected actual live Digital Daijisen entries for 炊く, 煮る, 雑炊, 端, 粗, 駄, 清, 晴 and 静; live Jisho/JMdict entries for the revised vocabulary claims; and public pinned KanjiVG component records for 清, 晴, 静 and 請. Search snippets were not used as verification.

Dispositions:

- **G1 — RESOLVED** — `snapshot\kanji\請.md:54` now correctly distinguishes right-hand 青 in 清/晴/請 from left-hand 青 in 静. The supplied 静 SVG and independently fetched pinned KanjiVG records agree. Live dictionary entries also support the retained セイ readings and 清's シン/ショウ.
- **G2 — RESOLVED** — `snapshot\words\透明.md` deletes exactly the stale no-透-card sentence, retaining the link and the トウ＋メイ explanation at lines 30–31. The in-memory patch comparison verified that nothing else changed. `CHANGES.md:9–11,29` explicitly records the exception to link-wrap-only word edits; no future closure document was assumed to exist.
- **G3 — RESOLVED** — `snapshot\kanji\炊.md:23,50` now preserves the Kansai restriction in both locations, and line 23 links the standard comparison 煮る にる. Supplied JMdict entries 1596830/1322540, independent live dictionary entries and the unchanged 炊く article's lines 45–48 agree. Keeping the broader character title is consistent with the original remedy.
- **OA — DECLINE ACCEPTED** — The suggestion was explicitly nonblocking restructuring polish. The five complete revised cards still lead with their central meaning, explain necessary reading terminology and label their mnemonics honestly. Restricting this confirmation to local corrections avoids unnecessary restructuring; the small additions do not establish a new comprehensibility defect.

Verdicts:

- **Correctness: CLEAN** — all changed cards and the changed article; no per-file exception established.
- **Scoped coverage: CLEAN** — the corrections retain the existing metadata/practice distinction and do not remove necessary material.
- **Consistency and quiz safety: CLEAN** — the changed material and reviewed post-fix options for 炊, 焦, 異, 端, 筋, 粗, 納, 脱, 膨, 致, 請, 透, 鉢, 隔 and 駄; subject to the audit limits below.
- **Comprehensibility: CLEAN** — all five revised cards and 透明; no new actionable regression established.

**Additional changed-hunk checks**

- **炊, line 25:** the expanded 雑炊 gloss matches the complete English gloss in pinned JMdict entry 1299440 and live Jisho data. Independent Daijisen supports the cooked-rice, broth, fish/vegetable description. The additional 煮る citation and link identify the correct entry/article.
- **端, lines 33 and 65:** live Daijisen actually lists はした in its character-level kun list without a corresponding word group there. JMdict entry 2590770 supports 端 はした, “fraction; odd sum.” The pinned KANJIDIC2 record does not list はした. The prose addition does not silently add it to metadata or practice.
- **粗, line 42:** entry 1586730 labels the flaw/fault noun sense as usually written in kana. The revised wording applies that qualification to the taught sense, without incorrectly extending it to the prefix senses. Live dictionary data corroborates the distinction.
- **駄, line 31:** independent Daijisen explicitly prints においうま as a kun reading. It is absent from the pinned KANJIDIC2 reading record and from the supplied complete 駄 families in JMdict. The new source note does not introduce a kun question or contradict the empty pinned kun metadata; see the absence-check limitation below.
- All five changed cards' front matter is unchanged. The exact patch contains only the five stated cards and 透明. Existing distractor/exclusion sets remain disjoint. The changed-line quoted titles agree with the original title indexes; the newly added 煮る article exists and has reading にる and title “boil; simmer; stew.”

**Post-fix quiz examination**

- I checked all 15 meaning option sets, not just the revised cards. Their displayed wrong titles remain defensibly wrong in both directions. No semantic ambiguity or newly unjustified exclusion was established. The meaning builder enforces direct exclusions symmetrically, also between selected distractors, without creating transitive exclusions.
- The reading builder protects all listed on/kun readings and their generated mutations, not merely the selected quiz reading. Thus shared スイ from 吹 and ハチ/ハツ from 八 are rejected where necessary. 納's ナッ and 駄's タ remain supported by their linked examples; the prose edits do not change these selections.
- I read both complete reading audits. The `reading-options.txt` conclusion “2 problem(s)” is not itself a demonstrated learner-facing failure. For 端's はし prompt, 新/山/短 fill all three wrong slots in every enumerated curated outcome; for 致's いたす prompt, 話/買/学 do likewise. Therefore the respective fallback はじめ and おこす cannot be selected in the audited pools. This follows from the actual add/cap logic, not just the absence of a hit in sampled seeds.
- Other prompts genuinely use fallback, including prompts on unchanged cards; I did not generalize curated saturation to the whole batch. The exposure audit reports zero production hits, zero padded-session hits, 17 latent collisions, and zero non-name one-holder padded hits. The extra name-only case and 炊's drawable name-only い do not establish additional correct on/kun answers.
- The additions はした and においうま are included among the extra readings audited. No new reachable collision is established for them.
- Independent file comparison found the reading audits unchanged after their revision-identifying first line. The meaning audit has the same substantive contents, with one blank line removed—not literal byte identity as `CHANGES.md` says. This formatting difference has no quiz or learning impact.

Confirmation: **CONFIRMED** — G1, G2 and G3 are resolved; OA's decline is accepted; no new actionable content defect was established. This confirms the reviewed content revision, not independently verified test execution or release/device acceptance.

Findings:

None.

Optional:

For future confirmation packets, preserve an unambiguous complete unit-test completion result rather than summarizing it as successful when the supplied log does not show success. This is an evidence-quality recommendation, not an established teaching-card defect.

Limits:

- I worked alone and serially, with one tool call per tool-bearing response. No parallel or multiple-tool-call response, agent, background job, other session, recursive listing or corpus filesystem scan was used. No other review or author material outside the permitted packets was sought. The only intentional write is this report.
- `checks\unittest.txt` contains “Ran 436 tests in 57.815s” followed by `System.Management.Automation.RemoteException`; it does **not** contain `OK`. Consequently I cannot verify `CHANGES.md`'s claim that all 436 tests passed. Nor does this fragment establish that content tests failed. No tests were rerun during this read-only review.
- The supplied audits are outputs of a Python model plus finite seeded sampling, not execution of every Kotlin/device outcome. Some candidate listings are abbreviated, and sampled coverage is incomplete for large fallback sets. Source inspection supports the specific curated-slot conclusions, but does not independently certify all pool-construction call sites, every possible session composition, future smaller decks, different clients or unenumerated dictionary readings. Meaning exclusions do not protect reading quizzes.
- Latent collisions are not dismissed as unattested readings: their reachability is what differs. The reported safety is bounded to the studied N1/All pools, Starter cases and the supplied extra-reading inventory; it is not a guarantee for every hypothetical pool.
- For 駄's dictionary-absence statement, I checked the supplied character families, not a newly rebuilt search over the entire compressed pinned JMdict archive. Live Jisho attempts segmented the missing-word queries, so I did not treat those results as proof of absence. The positive Daijisen attestation and pinned KANJIDIC2 omission were independently verified.
- The JVM content tests and Kotlin reading-audit cross-check remain unperformed as acknowledged in the packet. Physical-phone rendering, full dictionary-corpus validation and unchanged stroke files were not re-tested in this confirmation. CLEAN means no actionable defect established within this stated scope, not exhaustive certification.
