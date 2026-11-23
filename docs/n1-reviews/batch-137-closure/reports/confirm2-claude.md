# Batch 137 second confirmation report (Claude)

Snapshot: commit 48332d3258953779dda24c0df6fb1c649e6defbb (revision of 2bc8e9b1, which revised d3c7394d). Reviewer model: Claude (Anthropic), the reviewer who wrote `reports-137\initial-claude.md` and `reports-137\confirm-claude.md`.

Scope:
- Packet `confirm2-137-claude`:
  - Read in full: `INSTRUCTIONS.md`, `RESPONSE.md`, `CHANGES.md`, `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\meta-scan.txt`, `checks\link-targets.tsv`, `checks\manifest.txt`, `diffs\changed-files.txt` and `diffs\changed-lines.txt`.
  - All 3 changed cards (丁, 呂, 唯) read in full, including front matter.
  - All 15 cards in `snapshot\kanji\` compared line by line with the earlier confirmation packet's `snapshot\kanji\`. Only 丁:71, 呂:55 and 唯:54 differ.
  - `diffs\fix.patch` read for its file and hunk headers and its changed lines: 3 hunks, each one Metadata line.
  - `checks\quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`, `lint.txt`, `unittest.txt`, `validate.txt` and `vocabulary.txt` compared line by line with the earlier packet's checks. I also read the summary lines of the two reading audits.
  - `evidence\QuizBuilder.kt`, `KanjiReadings.kt` and `Words.kt` were hash-compared with the earlier packet's copies; all three are identical. I read QuizBuilder in full and KanjiReadings in part in the earlier round.
  - Not opened: `evidence\meta_scan.py`, `packet-manifest.json`, `checks\budget.txt`.
- Earlier confirmation packet `confirm-137-claude`, read-only: `snapshot\kanji\*.md` (old text), `checks\*` and `evidence\*.kt`, for comparison only.
- Original packet `batch-137-d3c7394d`, read-only: `evidence\jmdict-digest.tsv`, filtered to the ids next to the new ones (2622400, 2829360, 2857308, 2240210, 1271230, 1538910, 1538900, 1587010, 2672330), to check the entries and their order.
- My earlier reports, as recalled; they were not reopened.
- Web: none needed this round. The new claims are id-provenance claims, and I checked them against the pinned JMdict extracts.

Dispositions:
- P1 - RESOLVED - `丁.md:71` now lists 2829360. The id is right for the word the card uses: `jmdict-cited-entries.xml` and `jmdict-digest.tsv` both give 2829360 = 仕丁, with readings しちょう, じちょう, してい and つかえのよほろ, which is the entry 丁:40 describes.
  - **Placement:** it sits after 2622400 (丁幾 チンキ) and before 2857308 (丁々 とうとう). 丁幾 is named earlier in line 40, and 丁々 is first named at line 51, so this is first-mention order.
  - **Nothing else on the line changed:** my line diff and `fix.patch` show only the inserted ", 2829360". All other ids and links are byte-identical.

The two extra hunks, which do not answer a point of mine, also check out:
- `呂.md:55` adds 1448890 = 当て字 あてじ. That is the term 呂:27 uses: "only 当て字 (ateji), kanji used for their sound", and JMdict sense 1 is "kanji used as a phonetic symbol…; ateji". It is placed after 2240210 (呂 りょ, line 25) and before 1271230 (語呂, named after 当て字 in line 27), which is first-mention order.
- `唯.md:54` adds 2672330 = 唯々 いい and 1623580 = 諾々 だくだく. That matches 唯:39 ("唯々 is いい and 諾々 is だくだく"); both entries have xref 唯々諾々 and the gloss "obedient; submissive; tame; slavish". They are placed after 1538910 (唯でさえ, first named at line 34) and before 1538900 (ただ, line 39 after them), which is first-mention order. I did not count the separate 1587010 (唯々諾々, already listed) twice.

Verdicts:
- Correctness: CLEAN. All four added ids are the JMdict entries for the words as the cards use them, per the pinned entries supplied, and no teaching text changed.
- Scoped coverage: CLEAN. Unchanged from my confirmation round; nothing was removed.
- Consistency and quiz safety: CLEAN.
  - No front matter changed in any card.
  - `quiz-safety.txt` is identical to the reviewed one: all 15 cards are 3/3 curated, with 0 errors.
  - `reading-exposure.txt` and `reading-options.txt` differ from the earlier ones only in line 1, the command label. They show 0 production hits, 0 padded hits, 8 latent collisions and 1 KANJIDIC2 name-only reading, and 0 problems.
  - The app sources are unchanged, so the meaning and reading options for all 15 cards are as I judged them before.
  - `link-targets.tsv`: no card or word links on the changed lines. The external links are byte-identical.
- Comprehensibility: CLEAN. Only provenance lines changed, so the learner-facing text is untouched.

Confirmation: CONFIRMED

Findings: none.

Optional: none.

Limits:
- I issued exactly one tool call per response this round.
- Id identities were checked against the pinned JMdict extracts in the packets (`jmdict-cited-entries.xml`, `jmdict-digest.tsv`), not against live JMdict. EDRDG's JMdictDB search needs a password, and Jisho and WWWJDIC do not show entry ids.
- I did not run or read `meta_scan.py`. Its "none missing" result covers only multi-character kanji runs that match a JMdict spelling exactly; kana-only words, single-kanji words and words inside longer words are outside it. I did not do an independent full audit of every Metadata id list. The author applies a rule from its own brief, which is not in any packet, to list "every JMdict entry id for every word named on the card"; I did not audit compliance with it beyond the changed lines.
- The "only in つかえのよほろ" claim at 丁:40 still rests on the author's search of the pinned JMdict (unchanged since my confirmation round).
- The audits cannot show random draws, other stacks or pools, or older app builds. The Android JVM content tests and the Kotlin reading-audit cross-check were not run.
- The 12 unchanged cards, the stroke files, 寧, 敷 and the 21 word articles were not reread this round. The 12 cards were byte-compared as unchanged. For the others I relied on `CHANGES.md` and `diffs\changed-files.txt`, which list only 丁, 呂, 唯 and `manifest.json`.
