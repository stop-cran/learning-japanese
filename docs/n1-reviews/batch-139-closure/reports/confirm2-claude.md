# Confirmation report, round 2: batch 139

**Snapshot:** commit f1b2bdb84f7e932dfe59cb68829fc004415d0a74. My earlier confirmation covered 3b6f972767928e01261440466899f32df398d7f1, and the initially reviewed snapshot was a47efe9af926316eaa86656033bf6e109f2be697. Reviewer model: Claude (Anthropic).

**Scope:**

Packet `confirm2-139-claude`:
- Read in full: `INSTRUCTIONS.md`, `RESPONSE.md`, `CHANGES.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, `diffs\changed-files.txt`, `evidence\README.md`, `evidence\jmdict-cited-entries.xml` (entries 2216510 and 2230740) and `snapshot\kanji\嬢.md` (53 lines).
- Read in full in `checks\`: `link-targets.tsv`, `budget.txt`, `unittest.txt`, `linkplan.txt`, `validate.txt`, `vocabulary.txt`, `lint.txt`, `manifest.txt` and `kanji-remarks.txt`.
- Compared, not read in full:
  - All 15 `snapshot\kanji\*.md`: hash-compared with the earlier confirmation packet's copies.
  - `checks\quiz-safety.txt`: line-compared with the earlier packet's copy. Its option content was read in full in the earlier round.
  - `checks\reading-exposure.txt` and `checks\reading-options.txt`: line-compared with the earlier copies; I read their summary lines and line 196 of `reading-options.txt`.
  - `evidence\meta-scan.txt`: line-compared.
  - `evidence\QuizBuilder.kt`: hash-compared.
- Listed only: `evidence\meta_scan.py` and `packet-manifest.json`.

Earlier confirmation packet `confirm-139-claude` (read-only): its `snapshot\kanji\*.md`, `checks\*` and `evidence\meta-scan.txt` and `QuizBuilder.kt`, for the comparisons above. I did not reopen `KanjiReadings.kt` or `Words.kt` this round. I relied on my earlier reading of the reading-quiz mechanics and on the fact that no front matter changed.

Original packet `batch-139-a47efe9a`: not reopened this round.

My own reports `initial-claude.md` and `confirm-claude.md`, as context.

**Dispositions:**
- **P1 – RESOLVED.** `嬢.md:47` now quotes 嬢さん じょうさん as "(another's) daughter; young lady (esp. of respectable upbringing)."
  - This is exactly the two glosses of JMdict 2230740, sense 1 and sense 2, joined by a semicolon.
  - `fix.patch` shows that the only change is the inserted text " (esp. of respectable upbringing)". The rest of line 47 and the rest of the card are unchanged; `changed-lines.txt` lists only 嬢:47.
  - The Metadata line 51 already lists 2230740.
- **W1 – RESOLVED.** The "Corrections to the earlier CHANGES.md" section of `CHANGES.md` now states that 1531190 (嬢) and 1896840 (峠) did not move: each stayed at the end of the old list, and the new entries were appended after it. This matches the earlier `fix.patch`.
- **W2 – RESOLVED.** The same section now states that in 宴会 the colon became a full stop and "The on readings are" was added. It also notes that the row's quoted old and new text were exact. Both statements match the earlier `fix.patch` and `words\宴会.md`.

**Regression check of the changed hunk (嬢.md:47):**
- Correctness: the added parenthesis is verbatim JMdict. The other quoted glosses on the line are unchanged and were verified in the earlier round. Nothing on the line now contradicts the untouched text: line 23 still describes お嬢さん, and line 49 covers the exclusions.
- Scoped coverage: unchanged.
- Consistency: there are no links on the line, which `link-targets.tsv` confirms with 0 links. No front matter changed, and the 14 other cards are byte-identical to 3b6f9727.
- Comprehensibility: the bullet is a little longer, but the parenthesis is plain English and still fine on a phone.

**Checks and quiz options:**
- `quiz-safety.txt` is identical line for line to the copy I reviewed at 3b6f9727. The meaning options for all 15 cards are therefore unchanged, and I already judged them defensibly wrong in both directions. It reports 0 errors and 0 warnings.
- `QuizBuilder.kt` is unchanged.
- `reading-exposure.txt` and `reading-options.txt` differ from the earlier copies only at line 1, the command. Their summary lines are unchanged:
  - 0 production hits, 0 padded-session hits and 11 latent collisions, all in exposure.
  - 0 one-holder padded hits.
  - 1 options problem: the 岬 さき HIT label at line 196, offered by 先. The exposure audit models the real pools and finds it not drawable.
- `meta-scan.txt` differs only at line 1.
- These outputs are unchanged: lint (0 errors; the same 2 warnings on 宣伝 and 宴会), validate (0 errors), vocabulary (3201 of 3336), linkplan (0 problems) and kanji-remarks (0 problems; line 1, the command, differs).
- `unittest.txt`: 436 tests, OK.
- `manifest.txt`: the rebuild is idempotent and the tree is clean.
- `budget.txt`: retained and inflated bytes grow by 33 each, which equals the length of the inserted ASCII text " (esp. of respectable upbringing)". `localZipBytes` grows by 14. This matches `CHANGES.md`.

**Verdicts:**
- Correctness: CLEAN (all 15 cards)
- Scoped coverage: CLEAN
- Consistency and quiz safety: CLEAN
- Comprehensibility: CLEAN

**Confirmation:** CONFIRMED

**Findings:** none.

**Optional:** none.

**Limits:**
- The audits simulate option draws and string collisions only. They cannot judge whether a displayed title is semantically defensible as a wrong answer, or whether a card's prose is true. I judged the titles by reading `quiz-safety.txt` in the earlier round; that file is identical now.
- The Android JVM content tests and the Kotlin reading-audit cross-check were not run at this revision (known packet limit).
- The packet holds no stroke files or word articles. The claim that none changed rests on `diffs\changed-files.txt` and `fix.patch`, which list only `kanji/嬢.md` and `manifest.json`.
- I did not re-verify JMdict 2230740 against the live online JMdict. I relied on the pinned entry in the packet, whose README notes that today's JMdict may differ slightly.
- My first line comparison of the single-line check files was invalid, because PowerShell indexed characters instead of lines. I re-checked those files by full-text equality. `budget.txt` was confirmed to differ as described above, and the other four single-line files are identical.
- Execution limits: every response made exactly one tool call; no parallel calls were issued.