# Batch 137 confirmation report (Claude)

Snapshot: commit 2bc8e9b13ea85b39c533735f63643af44d1ce690 (revision of the reviewed d3c7394d). Reviewer model: Claude (Anthropic), the reviewer who wrote `reports-137\initial-claude.md`.

Scope:
- Confirmation packet `confirm-137-claude`:
  - Read in full: `INSTRUCTIONS.md`, `RESPONSE.md`, `CHANGES.md`, `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\weblio-卸-daijisen.txt`, `evidence\QuizBuilder.kt`, `checks\link-targets.tsv`, `checks\quiz-safety.txt`, `checks\lint.txt`, `checks\unittest.txt`, `checks\validate.txt`, `checks\budget.txt`, `checks\vocabulary.txt`, `checks\manifest.txt`, `diffs\changed-files.txt` and `diffs\changed-lines.txt`.
  - Read in part: `diffs\fix.patch` (file and hunk headers; I made the line-by-line comparison myself, see below); `checks\reading-exposure.txt` (lines 1, 2, 104, 173 and 206, the last four lines, and a full line-by-line comparison with the original packet's audit); `checks\reading-options.txt` (the last lines, and a full line-by-line comparison with the original); `evidence\KanjiReadings.kt` (the key lines of the option builder: `excludedKeys`, `question`, curated-then-closeness fallback).
  - Not opened: `evidence\Words.kt`, `packet-manifest.json`.
- Revised cards: all 11 changed cards (丁 仰 但 傑 僕 卸 司 吐 呂 哲 善) were read in full. 丁, 仰, 傑 and 卸 were read with front matter; for 但, 僕, 司, 吐, 呂, 哲 and 善 I read the body, and checked their front matter through the line diff, which showed no front-matter change. I compared all 15 revised cards line by line with the original packet's `snapshot\kanji\` myself. The 4 unchanged cards (井 傷 哀 唯) were byte-checked as unchanged by that comparison and were not reread.
- Original packet `batch-137-d3c7394d`, read-only:
  - `snapshot\kanji\*.md` (15 cards) for the line comparison.
  - `titles\kanji-titles.tsv` and `titles\word-titles.tsv`, to check every quoted title in all 15 revised cards.
  - `evidence\audits\quiz-safety.txt`, `reading-exposure.txt` and `reading-options.txt`, for comparison only.
  - `repo\docs\content-format.md` and `rubric\*.md`, searched for one pattern only.
- My own `initial-claude.md`, as recalled; it was not reopened.
- Web:
  - jisho.org API search for よほろ.
  - WWWJDIC (EDRDG) entries for よほろ and 膕.
  - The EDRDG jmwsgi search, which needs a password, so nothing was retrieved.

Dispositions:
- C1 - RESOLVED - All 16 quotations now carry the space and equal the linked card's `title:`.
  - My line diff shows each of the 16 lines changed only inside the quotation. Exception: 傑 lines 33/42 and 丁 40, 仰 59 and 卸 25/33 also changed, for O1/O2/O3 and the extra hunks below.
  - The comma-without-space pattern now has 0 hits in the 15 cards.
  - My own scan matched every `[X](X.md) … "…"` and `[W](../words/W.md) … "…"` in all 15 revised cards against the titles TSVs: 145 quotations, 0 real mismatches. The 2 hits were 僕:23, a prose gloss "I; me" before "in masculine speech", not a title quotation, and 呂:23 お風呂 "bath", which equals the title (column-order artefact of my script).
  - `link-targets.tsv` agrees: 57 links, 0 mismatched.
- O1 - RESOLVED - `丁.md:40` now says JMdict has no standalone よほろ entry and that the word appears only as つかえのよほろ, a reading of 仕丁. This matches `jmdict-cited-entries.xml` 2829360:
  - The readings are しちょう, じちょう, してい and つかえのよほろ.
  - Sense 1 is tagged `archaic`, applies to all readings, and its gloss is exactly "men pressed into forced labor (ritsuryō system)".
  - Sense 2 is restricted by stagr to the other three readings.
  - WWWJDIC shows no よほろ headword: a partial match only, with an offer to propose a new entry.
  - Jisho's API returns 膕 for よほろ, but WWWJDIC's 膕 entry has only ひかがみ, so that was a fuzzy match, not a reading.
  - "Only" rests on the author's search of the pinned file (see Limits). See also Optional P1.
- O2 - RESOLVED - `傑.md:33` and `:42` read "masterpiece; hilarious absurdity (jocular, dated)". 1253840 sense 2 carries `jocular, humorous term` and `dated term`, and sense 1 carries neither.
  - The label sits directly after the second gloss, so it reads as qualifying that sense only.
  - Line 23 already said the same in prose.
  - The intended difference from the word title is noted in `CHANGES.md`. It is not a quotation of the title (no quotes; `link-targets.tsv` n/a).
- O3 - RESOLVED - `卸.md:33` "cargo unloading (military term)" matches 2537870 `<field>military</field>`. 2537870 is listed in the card's Metadata line.
- O4 - DECLINE ACCEPTED - In round 1 I called 井–額 and 司–営/治/御 weak but not wrong. Each has a stated basis on the card:
  - 井.md:56 for "frame".
  - 司.md:56 quotes JMdict 司る "to rule; to govern; to control", and the titles of 営 and 治 and 御 contain "manage" and "govern".
  - `QuizBuilder.kt` only uses exclusions to remove options. With 3 curated distractors each (quiz-safety 3/3), removing them gains nothing.
- O5 - DECLINE ACCEPTED - It was optional. 何の変哲もない (1642670) is idiomatic but has no word article. The card already illustrates テツ adequately (lines 39, 45, 49).
- O6 - DECLINE ACCEPTED - The stated batch rule is reasonable and the facts hold:
  - The rule is to cover every KANJIDIC2 reading and every Daijisen ［音］/［訓］ reading, and Kanjipedia-only readings selectively.
  - None of 吐 ぬ.かす, 哀 かな.しむ, 傷 そこ.なう, 仰 あおの.く/の.く and 但 ダン is a KANJIDIC2 reading of its kanji (round-1 parse of `kanjidic2-records.xml`).
  - All five are passed as `--extra` (exposure line 1; line 2 states their provenance).
  - The only collisions are latent and not drawable in the N1, All or Starter pools: line 104 そこなう via 損 and 残, line 173 ぬかす via 抜, line 206 かなしむ via 悲. The 0 production and 0 padded hits are on the last lines.
- O7 - DECLINE ACCEPTED - The boilerplate is collection-wide layout. Changing it in one batch would make the cards inconsistent with the 42/10 published cards the author cites. This is editorial, not a defect.
- LW - RESOLVED - `evidence\weblio-卸-daijisen.txt` gives the URL, retrieval time, raw-HTML sha256 and the verbatim single `Sgkdj` block おろし【卸（し）】 with 《「下ろし」と同語源》問屋が商品を小売店に売り渡すこと。
  - This agrees with my round-1 live check of the Weblio page.
  - It supports `卸.md:25`: no character entry for 卸, and the only Daijisen entry is おろし written 卸/卸し, sharing its origin with 下ろし.
  - The new wording "the act of a wholesaler selling goods to retail shops" renders 問屋が…売り渡すこと more faithfully than the old "a wholesale dealer selling".
  - The explanation for the empty extract and the missing daijisen-heads entry (the parentheses are stripped, so 卸し ≠ 卸) is plausible and consistent with the files.
- LE - DECLINE ACCEPTED - The "(card text)" label is the tool's and does not affect any card. Line 2 of `checks\reading-exposure.txt` states the real provenance of the extras. Keeping the tool unchanged keeps the outputs comparable: I confirmed that the revised and original exposure and options audits differ only in line 1.

Verdicts:
- Correctness: CLEAN.
  - The new text is verified: 丁:40 against 2829360 and WWWJDIC, 仰:59 against 1238920 sense 1 `<dial>Kansai-ben</dial>` and kana tag, 傑:33/42 against 1253840, 卸:25 against the Daijisen block, and 卸:33 against 2537870.
  - All 16 title quotations are exact.
- Scoped coverage: CLEAN. No reading row or example was removed, and no front matter changed.
- Consistency and quiz safety: CLEAN.
  - The links resolve and the quoted titles equal their targets (145 checked).
  - Front matter is unchanged, so distractors, exclusions and quiz readings are as reviewed. No exclusion is also a distractor.
  - `quiz-safety.txt` is identical to the reviewed audit: all 15 cards are 3/3 curated, with 0 errors.
  - Reading options: 0 problems, 0 production or padded hits.
- Comprehensibility: CLEAN.
  - The added clauses are short.
  - 丁:40 grows by one clause in an already long paragraph; this is acceptable for a source-only reading.
  - 仰:59's "Kansai dialect in this sense" is clear.

Confirmation: CONFIRMED

Findings: none.

Optional:
- P1 (丁.md:76, Metadata line): the new 丁:40 text cites JMdict 仕丁 (2829360), but 2829360 is not in the card's list of JMdict entries. The other cited entries added or relied on in this revision are listed in their cards: 1238920 in 仰, 1253840 in 傑, 2537870 in 卸. Adding 2829360 would keep the provenance line complete. I found no format rule that makes this mandatory (a search of `content-format.md` and the rubric found none), so this is polish, not a defect.

Limits:
- I issued exactly one tool call per response throughout this round.
- "Only in つかえのよほろ" is the author's search of the pinned JMdict. Public checks:
  - WWWJDIC (version June 2025) shows no よほろ headword, and its 膕 entry has only ひかがみ.
  - The EDRDG JMdictDB search needs a password, so I could not run a full reading search of current JMdict.
  - The claim that no other entry has a reading containing よほろ is therefore unverified beyond these checks.
- The audits cannot show:
  - the actual random draws;
  - fallback behaviour for future or other users' custom stacks and pools other than N1, All and Starter;
  - behaviour of app builds older than the current QuizBuilder and KanjiReadings, for example ones that ignore `quiz_exclusions`;
  - collisions with readings attested only in sources not passed as `--extra`.
- The 11 existing cards that fall back to tag-similar meaning options (人, 休, 日, 口 …) may now draw batch cards such as 僕 for 人, 呂 for 口 or 但 for 日. I judged these titles distinct, but which cards are drawn depends on randomness and the whole corpus.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run (known packet limit).
- I did not reread the 4 unchanged cards or the 23 unchanged diffs. My byte-level line comparison confirmed the cards are unchanged, and `CHANGES.md` says no word article, stroke file, 寧 or 敷 changed, which I did not independently diff.
- `evidence\Words.kt` was not opened. I relied on the reading-options audit for mutation exclusions.
