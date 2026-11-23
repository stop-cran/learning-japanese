Snapshot: `f1b2bdb84f7e932dfe59cb68829fc004415d0a74`, confirming the revision from `3b6f972767928e01261440466899f32df398d7f1`. Reviewer: GPT (OpenAI; the exact runtime model identifier is not exposed to me).

Scope:

Independent, blind, read-only second confirmation. I read the changed card in full, checked the sole changed hunk against all four facets, and examined the complete meaning and reading audit outputs for all 15 batch cards.

Files opened in `confirm2-139-gpt`:

- **Full:** `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`.
- **Full linguistic reread:** `snapshot\kanji\嬢.md`.
- **Complete byte comparisons and front-matter equality checks, not fresh full linguistic rereviews:** `snapshot\kanji\{嫁,嬢,宗,宜,宣,宴,寂,密,審,尋,屈,属,岬,峠,崩}.md`.
- **Full:** `evidence\README.md`, `evidence\jmdict-cited-entries.xml`, `evidence\QuizBuilder.kt`.
- **Full:** `checks\{quiz-safety.txt,reading-exposure.txt,reading-options.txt,link-targets.tsv,lint.txt,unittest.txt,validate.txt,linkplan.txt,kanji-remarks.txt,budget.txt}`.

Files reopened in the earlier confirmation packet, `confirm-139-gpt`:

- `snapshot\kanji\{嫁,嬢,宣,峠}.md`: complete byte comparisons; 嬢's old/new line comparison verified the precise replacement.
- `checks\{quiz-safety.txt,reading-exposure.txt,reading-options.txt}`: complete comparisons with this round's outputs.
- `evidence\QuizBuilder.kt`: complete byte comparison with the current copy.
- `evidence\KanjiReadings.kt`: lines 1–155, covering reading normalization, protected keys, curated/fallback construction, shared-stem deduplication and queue eligibility.
- `evidence\Words.kt`: lines 211–246, including the complete sound-change mutation function.
- `evidence\jmdict-cited-entries.xml`: parsed for complete comparison of entries 2216510 and 2230740; the other entries were not freshly reviewed.

Files reopened in the original packet, `batch-139-a47efe9a`:

- `snapshot\kanji\{宗,宜,宴,寂,密,審,尋,屈,属,岬,崩}.md`: complete byte comparisons as the unchanged baseline for those eleven cards.

Fresh independent public verification inspected the actual [Jisho 嬢さん entry response](https://jisho.org/api/v1/search/words?keyword=嬢さん), including both readings, complete senses and register labels. No other reviewer's report was opened.

Dispositions:

- **G2 — RESOLVED** — `snapshot\kanji\嬢.md:47` now retains the complete second gloss, `young lady (esp. of respectable upbringing)`, matching pinned entry 2230740 and the independently inspected live entry. “Esp.” remains a tendency, not an absolute restriction. The separate とうさん reading, its Kansai/honorific qualification and its `daughter (of a good family)` gloss remain unchanged and match entry 2216510.

Verdicts:

- Correctness: **CLEAN** — G2 is fixed; no new actionable defect established.
- Scoped coverage: **CLEAN** — the restored qualification loses no reading, example or sense coverage.
- Consistency and quiz safety: **CLEAN** — all 15 cards' front matter and all actual audit results are unchanged.
- Comprehensibility: **CLEAN** — the parenthetical restores useful nuance without contradicting the surrounding explanation.

No card differs from these verdicts within this confirmation's scope.

Regression verification:

- The only difference among the 15 supplied card texts is the declared replacement on 嬢 line 47. Its line count remains 53; all fourteen other cards are byte-identical to their applicable reviewed baselines.
- The complete changed line equals the previous line with only ` (esp. of respectable upbringing)` inserted. The other related forms, the separate とうさん statement, and Metadata line 51 are unchanged.
- All 15 front-matter blocks are unchanged, including titles, metadata readings, practice selections, distractors and exclusions. No link is added or changed by the hunk; the changed-line link audit correctly lists zero links.
- The two supplied JMdict entries are unchanged from the earlier confirmation evidence. The restored wording matches the two glosses of 2230740 joined by a semicolon; it does not borrow a gloss from the different reading's entry.
- The meaning builder is byte-identical to the earlier copy. Its symmetric, pairwise exclusions and curated-first ordering remain unchanged.

Batch-wide quiz checks:

- I examined the meaning options for **嫁, 嬢, 宗, 宜, 宣, 宴, 寂, 密, 審, 尋, 屈, 属, 岬, 峠 and 崩**. The complete meaning simulation is byte-identical to the previous confirmation's output. Each still receives three curated wrong options. The prior bidirectional assessment carries forward; this prose-only insertion establishes no new alternative correct answer.
- I examined all scheduled reading prompts in both complete reading audit files: on readings **嬢 ジョウ, 宗 シュウ, 宣 セン, 宴 エン, 密 ミツ, 審 シン, 屈 クツ, 属 ゾク**; kun readings **嫁 よめ, 宜 よろしく, 寂 さびしい, 尋 たずねる, 岬 みさき, 峠 とうげ, 崩 くずれる**.
- Both reading outputs differ from the earlier copies only on command line 1. Their candidate tiers, curated choices, reachability results and summaries are otherwise identical. The source still protects all metadata readings and their generated sound-change variants, not just selected readings.
- The exposure summary remains **0 production non-name collisions, 0 Starter padded-session collisions, 0 one-holder padded collisions and 11 latent collisions**. Those latent cases do not become production defects because a prose qualification was restored.
- The persistent 岬/さき HIT in `reading-options.txt` is still not reachable in the reported shipped pools: 山/田/中 already fill all three wrong-reading slots before fallback is considered. The actual source ordering supports that distinction.
- 宗/し remains drawable but name-only, not an additional correct on reading for the シュウ prompt. 崩 still selects both verbs in metadata while scheduling the first shared くず stem; this revision does not change that previously dispositioned behavior.

The supplied validation and link-plan outputs report no errors, the test log reports 436 passing tests, and the two existing Dictionary lint warnings remain unchanged. These are supplied check results, not tests I independently reran.

Confirmation: **CONFIRMED** — G2 is resolved, and no new actionable defect was established.

Findings:

None.

Optional:

None new. Previously accepted nonblocking deferrals remain unchanged.

Limits:

- The exact GPT runtime model/version was not exposed; I have not invented one.
- This confirms the packet's revision, not an independently fetched Git tree, commit signature or regenerated manifest. Unchanged content retains its earlier linguistic review; byte equality is not claimed as a fresh full review.
- I did not run the Python audits, Android JVM content tests or Kotlin cross-check, and did not render the phone UI or stroke animations. Source inspection and supplied Python outputs do not constitute execution of the Kotlin app.
- Seed sampling alone cannot establish every random outcome. Some long fallback lists abbreviate candidates; I checked the displayed tiers, source mechanics and reported reachability, not every omitted kana individually.
- Extra readings are bounded source evidence, not an exhaustive historical/dialect/name lexicon. The modeled full stacks, Starter pool and one-holder cases do not certify every multi-holder borrowing combination, arbitrary reduced pool or future content set. No broader guarantee is inferred from their zero-hit summaries.
- All tool calls were serial, one per tool-bearing response. No parallel calls, sub-agents, other sessions, background jobs, recursive listings or corpus scans were used. The only intentional file write is this report.
