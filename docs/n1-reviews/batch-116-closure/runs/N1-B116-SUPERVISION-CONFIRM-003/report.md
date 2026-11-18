# B116 confirmation — N1-B116-SUPERVISION-CONFIRM-003

## Snapshot
Commit: 2b81b65b52ef8daa2c8690bd240371656545d1ef
Model: runtime reports Claude Opus 5.5 (claude-opus-5.5); execution-model identity is not independently verifiable in this pass

## Scope
Chain: segments 1-11 of n1-b116-supervision-confirm-003, each read once in order, no re-views; scoped card 督 read in full at the revised snapshot (confirm-packet/snapshot/kanji/督.md:1-193); 監 and 憲 read as context only; full 連, 養, 習 and 帰 cards and their supplied Daijisen, JMdict and KANJIDIC2 evidence read in full
Fetches: none (no web, shell, search or other local reads; only chain segments)

## Dispositions
- O1 - RESOLVED - The single urging bullet is now three bullets: encouragement with 勧, 励, 激 and 勉 (confirm-packet/snapshot/kanji/督.md:122-126); pressing/hurrying with 促, 催, 急, 追, 進 and 責 (confirm-packet/snapshot/kanji/督.md:127-137); and persuasion with 説 (confirm-packet/snapshot/kanji/督.md:138-140). Compared with the old text, the diff only adds lead phrases and moves 勧/励 and 促/催 into their respective groups (confirm-packet/diffs/fix.patch:113-141). Every per-character qualification is retained with unchanged substance, and no exclusion changed for this point.

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: O1 is resolved and my held L4 claim is now settled on the supplied complete entries. The new direct 督/連 guard is supported: KANJIDIC2 gives 連 "take along" and "lead" (confirm-packet/evidence/kanjidic2-meanings.json:33-45), Daijisen 連 sense 3 is 引きつれる with 連行 (confirm-packet/evidence/character-definition-連.txt:13), and JMdict 連行 is "taking (a suspect to the police); dragging (someone) away" (confirm-packet/evidence/jmdict-cited-entries.xml:236-255); this is the same loose leading comparison already guarded for 引. The new direct 督/養 guard is supported by Daijisen 養 sense 3, 精神的な糧を与えてりっぱに育てる with 養成 (confirm-packet/evidence/character-definition-養.txt:13), and JMdict 養成 "training; education; development; cultivation" (confirm-packet/evidence/jmdict-cited-entries.xml:217-235), matching the existing 育 coaching guard. The no-guard decision for 習 is accepted: Daijisen gives only one's own repeated learning and custom (confirm-packet/evidence/character-definition-習.txt:11-12), KANJIDIC2 only "learn", and the 習 card frames 習う as the learner's side of instruction, so neither "learn; practise" nor "supervise; urge" is a defensible answer for the other. The scan decision for 帰 is accepted: its KANJIDIC2 "lead to; result in" is an outcome sense, confirmed by Daijisen's returning and settling branches (confirm-packet/evidence/character-definition-帰.txt:11-12), not leading people, and its displayed title is "return home". The changed 督 lines (14, 100-102, 114-117, 122-141, 189-191) are accurate and qualified. All 19 changed-line links resolve with 0 mismatches. The exclusion list adds 連 and 養 without duplicates or overlap with distractors 目, 眠 and 且. QuizBuilder excludes symmetrically, so the 督 meaning options are unchanged (eye; sleep; sleepy; moreover; also), as is the トク reading audit. Validate, lint, quiz-safety and 431 unit tests pass, and no new established defect remains.

## Findings
None.

## Optional
### O1: Add the newly cited 連行 and 養成 entries to the JMdict metadata list
- Facet: Consistency and quiz safety
- Severity: optional
- Confidence: medium
- Citations: confirm-packet/snapshot/kanji/督.md:100-102; confirm-packet/snapshot/kanji/督.md:114-117; confirm-packet/snapshot/kanji/督.md:173-176; confirm-packet/evidence/README.md:3
- Evidence: The revised Notes now teach 養成 ようせい and 連行 れんこう, and the evidence README describes JMdict 1547190 and 1559440 as cited on changed 督 lines. The card's "Complete word families" JMdict list still ends at 1365990 and omits both entries, although the Daijisen links for 連 and 養 were added.
- Suggestion: Append 1547190 and 1559440 to the JMdict entry list so the source record matches the words the Notes now cite. No teaching or exclusion change is implied.

## Limits
- L1: Execution-model identity is reported by the runtime only and is not independently verified.
- L2: No checks/reading-options.txt was supplied, and the reading-exposure log is unchanged from earlier rounds. The meaning and reading audits model bounded N1, All and Starter pools only. They do not establish caller-built or multi-borrow pools, Kotlin execution, native or phone acceptance, or compatibility with the older installed APK that ignores quiz_exclusions.
- L3: The coordinator's KANJIDIC2-token scan of all 1232 cards was not re-run here; only its two surfaced candidates (連 and 帰) and the named 養 and 習 comparisons were verified against complete entries. Overlaps that only Japanese dictionary senses reveal, without shared English tokens, remain bounded by earlier rounds' evidence rather than exhaustively proven absent.
- L4: The supplied KANJIDIC2 record for 更 lists "night watch". No Digital Daijisen entry for 更 was supplied, and the response does not address it for 督. Read with its companion glosses ("grow late", "sit up late") it appears to be a night-time division rather than a supervising sense, and 督's meanings contain no "watch" token. I judge it not consequential for 督, but it is not verified against a full entry.
- L5: Changes to 監 (new 法, 儀, 王 and 社 guards) and the unchanged 憲 card were read only as context and not adjudicated; the 監/督 and 憲/督 pairs remain declared on those cards.
- L6: Raw KanjiVG SVGs and the binary Joyo PDF were not read; strokes and word wrappers are unchanged per the changed-files list. The supplied Daijisen extracts are bounded coordinator retrievals, not fresh reviewer fetches.
