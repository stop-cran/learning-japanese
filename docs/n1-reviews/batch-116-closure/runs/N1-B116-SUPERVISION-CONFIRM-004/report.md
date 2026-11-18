# B116 confirmation — N1-B116-SUPERVISION-CONFIRM-004

## Snapshot
Commit: 34687354b531a32fea9c10b745e80ac963ac1d4b
Model: runtime reports Claude Opus 5.5 (claude-opus-5.5); execution-model identity is not independently verifiable in this pass

## Scope
Chain: segments 1-9 of n1-b116-supervision-confirm-004, each read once in order, no re-views; scoped card 督 read in full at the revised snapshot (confirm-packet/snapshot/kanji/督.md:1-197); 憲 and 監 read in full as context only; full 員 and 更 cards and their supplied Daijisen, JMdict and KANJIDIC2 evidence read in full
Fetches: none (no web, shell, search or other local reads; only chain segments)

## Dispositions
- O1 - RESOLVED - 督's JMdict entry list now ends with 1365990, 1559440 and 1547190 (confirm-packet/snapshot/kanji/督.md:177-180), matching the 連行 and 養成 words its Notes teach (confirm-packet/snapshot/kanji/督.md:100-102; confirm-packet/snapshot/kanji/督.md:114-117). The supplied complete entries confirm both IDs: 連行 1559440 and 養成 1547190 (confirm-packet/evidence/jmdict-cited-entries.xml:71-107). The patch hunk changes only that metadata line for this point (confirm-packet/diffs/fix.patch:142-148).

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN

## Confirmation
Verdict: CONFIRMED
Basis: O1 is resolved. The only other changed 督 lines (14 and 95-97) add a direct 員 guard and one qualifying sentence. That sentence is accurate: the pinned KANJIDIC2 record lists "the one in charge" for 員 beside employee, member and number (confirm-packet/evidence/kanjidic2-meanings.json:87-96). Daijisen 員 sense 2 is people who make up an organization or work in a job (confirm-packet/evidence/character-definition-員.txt:12), and the card attributes the gloss to KANJIDIC2 only, explicitly denying that every member or employee supervises (confirm-packet/snapshot/kanji/督.md:95-97). This is a conservative direct pair parallel to the existing 係 person-in-charge guard, and quiz exclusions are symmetric, so one declaration suffices (confirm-packet/evidence/QuizBuilder.kt:27). My previous limit L4 on 更 is now settled: the complete Daijisen 更 entry gives replacing, one of the five night-time divisions, growing late and reviving (confirm-packet/evidence/character-definition-更.txt:11-14). "Night watch" is therefore a time division, not a watching or supervising sense; 更's displayed title is "renew; grow late", and no 督/更 pair is needed. The exclusion list has no duplicates and no overlap with distractors 目, 眠 and 且. The 督 link on changed lines resolves. Meaning options (eye; sleep; sleepy; moreover; also), the トク reading audit, validate, lint, quiz-safety and 431 unit tests are unchanged and passing. The 憲 and 監 changes leave the 監/督 and 憲/督 pairs intact, and I established no new defect.

## Findings
None.

## Optional
None.

## Limits
- L1: Execution-model identity is reported by the runtime only and is not independently verified.
- L2: No checks/reading-options.txt was supplied, and the reading-exposure log is unchanged. The meaning and reading audits model bounded N1, All and Starter pools only. They do not establish caller-built or multi-borrow pools, Kotlin execution, native or phone acceptance, or compatibility with the older installed APK that ignores quiz_exclusions.
- L3: The coordinator's KANJIDIC2-token scan of all 1232 cards was not re-run. Overlaps revealed only by Japanese dictionary senses, without shared English tokens, remain bounded by the evidence of this and earlier rounds rather than exhaustively proven absent.
- L4: The 憲 changes (僚, 権, 任, 係, 士 and 数 guards) and 監 changes (士 and 員 guards) were read only as context and not adjudicated.
- L5: Raw KanjiVG SVGs and the binary Joyo PDF were not read; strokes and word wrappers are unchanged per the changed-files list. The supplied Daijisen extracts are bounded coordinator retrievals, not fresh reviewer fetches.
