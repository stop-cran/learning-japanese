# Batch 141 second confirmation review — Claude

## Snapshot

Commit 094a1649552f7773f0a636a104cc797a765bec6e. My first confirmation covered 65b47299, and the initially reviewed snapshot was a92d134a. Reviewer model: Claude (Anthropic model family), the same reviewer who wrote `reports-141\initial-claude.md` and `reports-141\confirm-claude.md`.

## Scope

Packet `confirm2-141-claude`:

| File | How read |
| --- | --- |
| `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md` | full |
| `diffs\fix.patch`, `diffs\changed-lines.txt`, `diffs\changed-files.txt` | full |
| `evidence\README.md`, `evidence\kanjidic2-斗.xml`, `evidence\jmdict-cited-entries.xml` (entries 1257720 and 1601650) | full |
| `snapshot\kanji\抽.md`, `snapshot\kanji\懸.md` | full, with line numbers |
| `checks\quiz-safety.txt`, `link-targets.tsv`, `validate.txt`, `unittest.txt`, `linkplan.txt`, `kanji-remarks.txt`, `lint.txt` | full |
| `checks\reading-exposure.txt` | last 22 lines read; the whole file compared line by line with the earlier copy |
| `checks\reading-options.txt` | lines 1-6 and 172-230 (懸, 扇, 抽, 拡) read; the whole file compared line by line with the earlier copy |
| `checks\vocabulary.txt`, `manifest.txt`, `budget.txt` | not compared (the comparison command stopped on `validate.txt`) and not read beyond what is listed above |

Comparisons:

- **Hashes.** I compared SHA-256 hashes of every file in this packet's `snapshot\kanji\` and `snapshot\words\` with the earlier confirmation packet's copies. Only 抽.md and 懸.md differ. The other 13 batch cards, 張.md, 悔しい.md and 悔やむ.md are byte-identical.
- **Checks, excluding line 1 (the command).** `quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt` and `lint.txt` are identical to the earlier confirmation packet's copies.
- **Not opened:** `evidence\QuizBuilder.kt` this round (its hash comparison did not run, see Limits), `evidence\meta-scan.txt`, `evidence\meta_scan.py` and `packet-manifest.json`.

Other allowed reads:

- Original packet `batch-141-a92d134a`: `evidence\public-source\weblio-抽.txt`, lines 1-8 (Daijisen 抽 entry).
- Earlier confirmation packet `confirm-141-claude`: `snapshot\` and `checks\`, used only for the hash and line comparisons.
- My own reports: used from context, not re-opened.
- Public web: none needed this round. The 斗 claim is now backed by the pinned KANJIDIC2 record. In round 2 I had checked en.wiktionary and ja.wiktionary 抽斗 and the jisho.org page for 斗.

## Dispositions

- **F1 — RESOLVED.**
  - The sentence that split 抽斗 into 抽 ひき + 斗 だし is gone (`fix.patch`).
  - `抽.md:36` now says 抽斗 ひきだし "is a reading of the whole word, not a kanji-by-kanji reading, and KANJIDIC2 gives 斗 no reading だし". This matches the pinned `kanjidic2-斗.xml`, which gives ja_on ト and トウ, no ja_kun, and nanori ます.
  - Daijisen does list 抽斗 (ひきだし) under ［難読］ (`weblio-抽.txt` line 6).
  - The treatment now matches `扇.md:58` on 団扇.
  - No sentence on lines 34-36 gives 斗 a reading or splits 抽斗 by kanji.
  - The new ひき- example 抽出し is analysed correctly: 抽 ひき + 出 だ + okurigana し, and 抽出 is ちゅうしゅつ.
  - The JMdict labels in the `抽.md:34` cell match entry 1601650 exactly:
    - 引き出し is the head form.
    - 抽出し is a search-only kanji form.
    - 抽き出し and 抽斗 are rarely used kanji forms.
    - Sense 1, "drawer", has no `stagk` restriction, so it applies to these spellings.
  - The cell explicitly says that 抽出し is not a recommended word example and that the word article 引き出し uses the usual spelling. ひき- is not quizzed (`quizKunyomi: []`).
- **F2 — RESOLVED.**
  - The last clause of `懸.md:46` now says JMdict "lists けねん first and also けんねん, which it marks as irregular kana usage; in けんねん, 懸 supplies ケン". This matches entry 1257720: `<re_inf>word containing irregular kana usage</re_inf>` on けんねん, and the priority tags ichi1, news1 and nf02 only on けねん.
  - Nothing else on the line changed (`fix.patch`, `changed-lines.txt`).
  - The wording parallels `扇.md:42`.

## Verdicts

| Facet | Verdict |
| --- | --- |
| Correctness | CLEAN. 抽 and 懸 are now clean; the other 13 cards and 張 are unchanged since my earlier confirmation. |
| Scoped coverage | CLEAN. The ひき- row still has an example, and 抽斗 and 抽き出し are both still explained. |
| Consistency and quiz safety | CLEAN. There is no front-matter change, the quiz audits are identical, and the changed lines contain no links (`link-targets.tsv`: 0 links). |
| Comprehensibility | CLEAN. See Optional for two wording nits on 抽. |

## Confirmation

CONFIRMED.

## Findings

None.

Regression check of every changed hunk against the untouched text:

- **抽, line 34.** It agrees with line 25 (抽選/抽籤, ぬきんでる), line 36 (no verb reading ひ.く) and line 48 (引 writes the usual spelling of ひきだし).
- **抽, line 36.** The order is now 抽出し, then 抽き出し, then 抽斗. Each spelling is described accurately and the paragraph does not contradict itself.
- **懸, line 46.** It agrees with line 42 (ケ row, 懸念 けねん) and with line 33 (Daijisen ケ, a customary reading).

## Quiz options

**Meaning quiz** (`checks\quiz-safety.txt`):

- The file is identical to the copy I judged in my earlier confirmation round.
- All 15 cards keep the same three curated wrong titles.
- None of these titles overlaps the target title in either direction.
- The audit reports 0 errors and 0 warnings.
- The mechanics are as I reviewed them in `QuizBuilder.kt`: symmetric exclusions, unique titles, curated distractors first and then a fallback ranked by shared tags. I did not re-open or re-hash the file this round.

**Reading quiz** (`checks\reading-options.txt` and `reading-exposure.txt`):

- Both files are identical to the earlier copies apart from line 1.
- `reading-options.txt` reports 0 problems.
- `reading-exposure.txt` reports 0 production hits, 0 padded-session hits and 0 one-holder padded hits. Its 5 latent collisions are unchanged and cannot be drawn from any of the pools: 悔 け (twice), 慎 みつ, 懐 かね, 扇 おう.
- The four prompts that fill one wrong slot from the fallback are unchanged: 慮 (虎), 慰 (封), 憧 (慢), 懐 (慢).
- Every prompt has three wrong options in every seed.
- For 抽, the audit still covers ひく, ぬく, ぬきんでる and ちゅうだい. None of them is offered by another on-reading card.

What the audits cannot show:

- Whether card prose is true. For example, they could not have caught the old 斗 だし claim, and they cannot confirm the new one; I checked it against the KANJIDIC2 record myself.
- Whether a fallback reading is confusing for a beginner, as opposed to merely wrong.
- Whether the meaning-level exclusions are justified.
- Any reading that was not supplied as `--extra`.

## Optional

- **`抽.md:34`, "this index form".** The phrase introduces new jargon right after "search-only kanji form". Repeating "this search-only form" would be plainer for a beginner.
- **`抽.md:36`, "Daijisen lists the rarely used spelling 抽斗".** This could be read as attributing "rarely used" to Daijisen. That label is JMdict's (line 34); Daijisen only lists the word under 難読. Something like "Daijisen lists 抽斗 ひきだし, a spelling JMdict marks as rarely used, as a hard-to-read word" would remove the ambiguity.

Neither point is a factual defect.

## Limits

- **Tool calls.** I made one tool call per response with no parallel calls. Some PowerShell calls read or compared several packet files in one command.
- **Comparisons that did not complete.** The comparison stopped with an error at `validate.txt`, a one-line file. Its content and that of `unittest.txt`, `linkplan.txt` and `kanji-remarks.txt` were then read directly: 0 errors; 436 tests OK; 21/21 links, 2 remark edits, 0 problems; 0 problems. `vocabulary.txt`, `manifest.txt`, `budget.txt` and the hash of `QuizBuilder.kt` were not checked this round.
- **Author claims taken from CHANGES.md and not verified:**
  - The 191-byte and 77-byte budget deltas.
  - The meta-scan line-number change.
  - That the wording follows other cards (双, 圧, 訓). Those cards are outside my allowed reads.
- **Not run by the author:** the Android JVM content tests and the Kotlin reading-audit cross-check.
- **Scope of this round.** The 13 unchanged cards were not re-read; they are byte-identical to the text I judged before.
