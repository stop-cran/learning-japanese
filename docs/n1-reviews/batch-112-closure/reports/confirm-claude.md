Snapshot: 737cb0201bb3ca76b327504d95b17e64f1a79869 (child of reviewed d6ad96eb). Reviewer model: configured claude-opus-5.5; actual execution-model identity unverified.

Scope:
- Confirmation packet confirm-112-737cb020-claude: read INSTRUCTIONS.md, RESPONSE.md, CHANGES.md and evidence\README.md in full.
- diffs\fix.patch: read all 8 files' hunks in full.
- Revised cards (妙 就 展 微 態 盤 診 障): Notes sections read in full; each hunk read in context, together with the front matter and the body lines that the hunks refer to.
- evidence\QuizBuilder.kt (40 lines) and checks\quiz-safety.txt (51 lines): read in full.
- evidence\jmdict-cited-entries.xml: parsed all 6 entries (k_ele with ke_inf, r_ele, every sense with pos/misc).
- Original packet: used its repo\kanji\ (1,191 cards, unchanged except the 8) for one read-only Python scan. The scan covered all 16 new pairs: counterpart titles, distractors and exclusions, both directions; every card whose distractors pair two mutually excluded cards; batch cards used as anyone's distractor; and unexcluded English-word overlaps between batch titles and all titles.
- Not opened:
  - diffs\changed-lines.txt, changed-files.txt and checks\link-targets.tsv (I resolved targets via the scan instead);
  - evidence\joyo\ (no reading changed);
  - the other check outputs, beyond CHANGES.md's summary;
  - the seven unchanged cards (identical to the initial review);
  - the Weblio/Daijisen pages (not fetched).
- No temporary files were written by me. The harness auto-saved one oversized command output (the first combined read of the packet docs) to its own temp folder.

Dispositions:
- F1 - RESOLVED.
  - 微.md:14 now excludes 分. excluded(a, b) at QuizBuilder.kt:26 is symmetric, and tryAdd (line 30) skips it against the target and against already-chosen options. So 分 can no longer be a wrong option for 微, nor 微 for 分.
  - 分 is unchanged (distractors 今/半/木, no exclusions) and does not list 微.
  - The new note (微.md:68-71) is accurate and clear.
  - Keeping the title is acceptable: KANJIDIC2 "minuteness" supports it, and the exclusion was my first remedy.
  - The older-APK caveat is correctly disclosed.
- F2 - RESOLVED.
  - 就.md:14 now excludes 企 and 承, the shared "undertake".
  - It also excludes 担 (take on) and 職 (employment/post; 就職 is the card's own word).
  - 位 is a mild but defensible addition, given the card's position sense at 就.md:23-25. It is not over-broad in effect, because 就 keeps its curated 京/秋/州 (quiz-safety.txt:8) and a large fallback pool.
  - None of the counterparts lists 就 as a distractor or exclusion.
- F3 - RESOLVED. 態.md:62-63 now says "additional spelling in the entries headed by 体 (てい), 形 (なり) and 様 (ざま)". In jmdict-cited-entries.xml, 1409160, 2138450 and 1410750 each list 態 as the second keb with no ke_inf, so the wording is exact. Line 64 still follows correctly.
- O1 - RESOLVED. 障.md:14 adds 関. The bullet at 障.md:61-63 quotes part of 関's title, "involve; barrier", accurately. 関 is unchanged and does not list 障.
- O2(a) - RESOLVED. 展.md:14 adds 敷. The bullet at 展.md:66-67 glosses 敷 as "spread/lay out", which matches its title. 敷's exclusions (布, 普, 散, 床) and distractors (放, 敬, 敗) do not involve 展.
- O2(b) - RESOLVED. 妙.md:14 adds 技 and 腕. The bullet at 妙.md:67-69 matches JMdict 1528490 sense 3, "cleverness; adroitness; knack; skill", and the glosses match the titles of 技 and 腕.
- O3 - DECLINE ACCEPTED. It was optional enrichment. No 受動態 or 能動態 article exists to link, and its absence leaves no claim on the card wrong.
- L1 - PARTIALLY RESOLVED.
  - Verified from source: for meaning quizzes, QuizBuilder.kt establishes that exclusions are symmetric and apply to both the curated and the fallback candidates. It also enforces pairwise exclusion among the chosen options and deduplicates titles. Distractors missing from the pool are skipped (lines 34-36).
  - Still unverified: how the app builds `all` for each pool (level, custom or Starter); that the installed or shipping build contains this code (2edbf36 or later); actual Kotlin or JVM execution; phone acceptance; the reading-quiz sources; and multi-borrow Starter.

Verdicts:
- Correctness: CLEAN. Every changed claim is consistent with JMdict 1375720, 1409160, 1410750, 1528490, 1615650 and 2138450 and with the linked card titles.
- Scoped coverage: CLEAN. All 8 changed cards and all 16 new pairs were reviewed, and the 7 unchanged cards are unaffected.
- Consistency and quiz safety: CLEAN.
  - No new excluded card is also a distractor on either side, and no card lists both members of an excluded pair as distractors.
  - No batch card is anyone's curated distractor.
  - All 15 cards still show 3 curated wrong options in quiz-safety.txt (lines 1-37), unchanged from the initial packet.
  - All glosses on the new links match their targets' titles.
- Comprehensibility: CLEAN. The new bullets are short, state each comparison's direction, and explicitly avoid implying interchangeability.

Confirmation: UNVERIFIED.
- F1-F3, O1, O2(a) and O2(b) are RESOLVED, O3 is DECLINE ACCEPTED, and no new actionable defect was established.
- Strictly, the only thing preventing CONFIRMED is L1, which remains partially resolved. Its residue is runtime and pool-construction behaviour that is outside this content review (JVM and emulator work remains on hold).

Findings: none.

Optional:
- 就 "take a position; undertake" still shares "take" with 取 "take", 喫 "consume; take in" and 連 "link; take along", none of which is excluded.
  - The shared word is weak: no option title is fully correct for the other card, so this is not a defect.
  - The 看 "watch over" and "… over" overlaps are trivial.
- The 了/完/済 exclusions on 就 rest on its 成就 completion side (taught at 就.md:29-31 and in the ジュ row). They are harmless and defensible. I did not independently confirm them against a character dictionary (Daijisen not fetched).

Limits:
- The quiz-safety output reflects the full pool only; level, custom and Starter pool contents are not shown.
- QuizBuilder.kt is a supplied excerpt (Android 10d98d0). I did not verify it against a live checkout or build.
- quiz_exclusions are not enforced by the older 5c000bd APK.
- Reading-quiz behaviour is unchanged and unverified. reading-exposure.txt has the same limits as before, and no reading-options.txt or app reading-quiz sources were supplied.
- No JVM, Gradle or emulator was run.
- Public Daijisen pages were not consulted.
