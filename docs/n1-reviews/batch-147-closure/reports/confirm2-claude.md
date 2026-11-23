# Batch 147: second confirmation review (Claude)

Snapshot: commit 886671da825c2da9ccbbf34506cf0b7747d7804c (revised), compared with 99487bb5 (my previous confirmation snapshot). Reviewer model: Claude, an Anthropic model. The exact version string is not available to me.

Scope:
- Read in full: this packet's `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch` (both hunks), `diffs\changed-lines.txt`, `diffs\changed-files.txt`, `evidence\README.md`, `evidence\QuizBuilder.kt` and `evidence\meta-scan.txt`.
- Read in full: the checks `quiz-safety.txt`, `link-targets.tsv`, `lint.txt`, `validate.txt`, `unittest.txt`, `linkplan.txt`, `kanji-remarks.txt`, `budget.txt`, `vocabulary.txt` and `manifest.txt`.
- `checks\reading-options.txt`: read the 穏 section, the 粋 and 糧 sections and the summary line. I diffed the whole file, and `reading-exposure.txt`, against the earlier confirmation packet's copies. Only the command header line differs, so the results are identical.
- Read in full, every line: the two changed cards 穏 and 稚 in `snapshot\kanji\`.
- Compared by file hash: the other 13 cards against the earlier confirmation packet's `snapshot\kanji\`. All 13 are byte-identical. I diffed 穏 and 稚 line by line against the earlier text: only lines 25 and 40 differ, and both match `fix.patch`.
- Grepped `穴.md` and `矢.md` in this packet to check the O-穴 decline reason.
- My own earlier confirmation report: read in full.
- From the original packet, read-only:
  - `evidence\public-source\weblio-穏.txt`: grepped line 6, the Daijisen character entry.
  - `evidence\jmdict-families.xml`: extracted entry 2863360.
  - `rubric\copilot-instructions.md`: grepped for the requirements on metadata and kana readings.
- Public web: the Jisho API JSON (JMdict-sourced) for 静穏.

Dispositions:
- O4 - RESOLVED:
  - `穏.md:25` now reads "Its examples include 穏健 おんけん, 穏和 おんわ, 安穏, 静穏, 不穏 ふおん and 平穏 へいおん."
  - This matches Daijisen (`weblio-穏.txt:6`): 「穏健・穏和／安穏(あんおん・あんのん)・静穏・不穏・平穏」. It has the same six words in the same order.
  - "include" is accurate. 静穏 is a real word, せいおん, "tranquility; calmness; serenity" (JMdict via Jisho).
- O-稚 - RESOLVED:
  - `稚.md:40` now reads "in the JMdict spelling 稚けない".
  - JMdict 2863360 has the kanji forms 稚い, 幼い, 稚けない and 幼けない, plus 幼ない and 稚ない as search-only forms. The revised wording no longer implies that only one other spelling exists, and it stays true.
- O-矢 - DECLINE ACCEPTED - this was polish only. The image at `矢.md:27` works as written, as I noted in my earlier report.
- O-穴 - DECLINE ACCEPTED:
  - The reason holds. The "well-kept secret" sense belongs to the one-kanji word 穴 itself, and `穴.md:23` quotes it.
  - By contrast, the removed 矢 → 恋 exclusion rested on a sense of the compound 矢印, not of the word 矢. The two cases are therefore not the same, and the exclusion on 穴 is a real direct pair.
  - It is also harmless: 穴 fills 3/3 slots from curated distractors.
- O-粋 - DECLINE ACCEPTED:
  - メエトル comes from the existing 米 card's quiz readings, which are outside this batch's diff.
  - The option is wrong for 粋, so it is safe. The `reading-options.txt` result for 粋 is unchanged.

Verdicts:
- Correctness - CLEAN:
  - Both changed hunks are true. I checked them against Daijisen (`weblio-穏.txt:6`), JMdict 2863360 and JMdict 静穏.
  - The rest of 穏 and 稚 does not contradict the revised lines. `稚.md:35`, "with 幼い as another written form", is still consistent with line 40.
- Scoped coverage - CLEAN: no reading row, word or explanation changed except the two lines.
- Consistency and quiz safety - CLEAN:
  - There are no links on the changed lines (`link-targets.tsv`: 0).
  - The front matter is unchanged on both cards.
  - 静, newly named on `穏.md:25`, is already in 穏's `quiz_exclusions`.
  - `quiz-safety.txt` is identical to the earlier round, and every batch card's three meaning options are clearly wrong curated titles under `QuizBuilder.options`.
  - The reading checks are identical apart from their headers. The 穏 prompt おだ.やか sees only き, こ, た and はな over 100 seeds, so the latent やすらか of 安 is never drawn.
- Comprehensibility - CLEAN: both edits are small and read naturally on a phone.

Confirmation: CONFIRMED. All five items are RESOLVED or DECLINE ACCEPTED, and I established no new actionable defect.

Findings: none.

Optional:
- `穏.md:25`: 静穏, newly added, has no kana reading anywhere on the card. 安穏 is at least read at `:39`. Adding せいおん, and perhaps あんのん on line 25, would help a beginner.
- `meta-scan.txt` reports that 静穏's JMdict entry 1381850 is not on the Metadata line. The card makes no JMdict claim about 静穏: it is cited as a Daijisen example, and Daijisen is on the Metadata line. The rubric does not require every named word's JMdict id, so this is not a defect. Add 1381850 only if a gloss or reading from JMdict is ever added.

Limits:
- I issued exactly one tool call per response, and no parallel calls, sub-agents or background jobs.
- `evidence\jmdict-cited-entries.xml` is described as "(none)" and is not in the packet. For 静穏 I used the Jisho API, which is JMdict-derived but not the pinned snapshot. I did not check that 1381850 is the entry id of 静穏.
- I did not re-run any audit. The quiz and reading conclusions rest on the supplied outputs, on `QuizBuilder.kt` and on my earlier reading of `KanjiReadings.kt`, which this packet does not supply again.
- What the audits cannot show:
  - Options that are pedagogically odd but safe, such as メエトル.
  - Pools beyond the N1, All and Starter-practice pools that the audit models.
  - The Android JVM content tests, which were not run.
- The 13 unchanged cards were checked for identity only (by hash), not re-reviewed.
