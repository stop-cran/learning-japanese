## Snapshot: `68380b7c43f3dc42c56f88e5639b525357dd4e85` — committed content only

The supplied correction snapshot identifies this commit as the clean committed correction to `a14eb7276298c2231ac00aa70cea55948bb3e7fc`. The twelve inspected file contexts match the supplied patch. Commit identity, cleanliness and file-to-commit correspondence remain **author-attested**, not independently Git-verified.

## Scope

**GPT-6.1 Sol** (`gpt-6.1-sol`, GPT family), performing a bounded follow-up to my own `batch-04-gpt-initial.md`, not a new independent full-batch review.

Inspected the actual twelve-file patch and changed passages in context: **15 added direct exclusion pairs**, 幾分’s classification/explanation, 衣食住’s collective title, and **five comparison-link occurrences**. Checked relevant original/comparison dictionary families, component records, actual target-card passages and the unguarded 常に candidate.

Read-only; no edits, delegation or agents. No other reviewer’s report or prohibited notes/private inputs were read. Unchanged comparison cards received only targeted checks—not comprehensive review. Kanji pages, reuse articles and the remaining original batch articles were not newly reviewed.

## Verdicts

Paths are under `words\`. Each verdict applies only to the indicated changed context.

| File | Changed context / added direct partners | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| 幾分.md | Native-first mixed grouping; kun+on explanation; 気持ち | CLEAN | CLEAN | CLEAN |
| 育児.md | 教育 comparison link | CLEAN | CLEAN | CLEAN |
| 以後.md | 来 guard; 以前 comparison link | CLEAN | CLEAN | CLEAN |
| 以降.md | Separate 来 guard; 以前 comparison link | CLEAN | CLEAN | CLEAN |
| イコール.md | 同一・同様・平等 guards | CLEAN | CLEAN | CLEAN |
| 衣食住.md | Collective title; 生活 comparison link | CLEAN | CLEAN | CLEAN |
| いちいち.md | あらゆる guard | CLEAN | CLEAN | CLEAN |
| 一応.md | およそ・約・ほぼ guards | CLEAN | CLEAN | CLEAN |
| 一流.md | 上等・優秀 guards | CLEAN | CLEAN | CLEAN |
| 佚.md | ゆっくり guard | CLEAN | CLEAN | CLEAN |
| 一斉.md | 一緒 guard | CLEAN | CLEAN | CLEAN |
| 一定.md | 安定 guard; 変化 comparison link | CLEAN | CLEAN | CLEAN |

## Findings

**All eight of my original findings are resolved. No actionable regression was established.**

- **GPT04-01 — resolved:** `words\幾分.md:6–9,30–33` now uses the repository’s native-first `wago` grouping and explicitly identifies native いく + on ブン as mixed kun+on/yutoyomi. The component records support those readings; the qualification avoids claiming a wholly native reading and matches the established 場所 treatment.
- **GPT04-02 — resolved:** `words\幾分.md:9` directly excludes 気持ち. Its ordinary “slightly/a little” sense—not merely its emotional meaning—supports the guard.
- **GPT04-03 — resolved:** `words\以後.md:9` and `words\以降.md:9` each directly exclude 来. Both are necessary because protection through 以来 is not transitive; 来’s suffix “since” sense supplies the relevant overlap.
- **GPT04-04 — resolved:** `words\イコール.md:9` directly excludes both 同一 and 同様, whose relevant dictionary senses include “equal.”
- **GPT04-05 — resolved:** `words\いちいち.md:9` directly excludes あらゆる, addressing “every single/each and every” versus “every.”
- **GPT04-06 — resolved:** `words\一応.md:9` directly excludes およそ, protecting the displayed “roughly” label.
- **GPT04-07 — resolved:** `words\一流.md:9` directly excludes 上等 and 優秀, covering the overlapping first-class/excellent quality evaluations.
- **GPT04-08 — resolved:** `words\佚.md:9` directly excludes ゆっくり. The leisure/relaxation overlap supports this without overriding 佚’s retained recognition/register warning.

The **five additional pairs** are also justified by actual meanings and labels: イコール／平等 through equality/equal; 一応／約 and 一応／ほぼ through “roughly/approximately”; 一斉／一緒 through 一緒’s explicit “at the same time” sense; and 一定／安定 through settled constancy/steadiness. Supporting comparison entries in `batch-04.json` are respectively **1507670/1, 1538100/1, 1551940/2, 1163400/4 and 1154120/1**, assessed against the changed cards’ relevant senses and displayed titles. These guards address answer-label ambiguity, **not unrestricted Japanese substitution**. None relies solely on shared topics, neighbors or part-of-speech labels; none merely duplicates an exactly equal title.

The revised `words\衣食住.md:4` correctly presents **food, clothing and shelter as one collective meaning**, matching entry 1158780/1 and the heading/body. All five new links point to existing, correctly read targets and preserve useful distinctions: 教育 overlaps only aspects of upbringing (`育児.md:33–34`); 以前 supplies the opposite temporal direction in both temporal cards (`以後.md:37`, `以降.md:37`); 生活 is broader (`衣食住.md:34`); and 変化 contrasts with an unchanging value (`一定.md:36–38`).

**Leaving 常に unguarded is acceptable in this scope.** Its actual title and teaching (`words\常に.md:4,15–22`; entry 1355970/1) concern always/constantly occurring or continuing, whereas 一定’s relevant sense concerns a fixed or uniform value/extent. Constantly changing is not remaining constant. The evidence does not establish the same answer-label ambiguity here; this was not an unresolved finding in my initial report.

## Optional

None.

## Limits

I **cannot independently execute Git or recompute the frozen hashes**. The supplied dictionary/component extracts and snapshot attestations are author-supplied evidence, not independently reconstructed snapshots. No fresh public retrieval or runtime quiz execution was performed. The source record’s irrelevant Kotobank 一応 extraction and failed HTTP-504 search were not used as verification.

No consequential linguistic claim remains unresolved within this bounded scope. **CLEAN means scoped editorial acceptance, not exhaustive lexicography or native-speaker certification.**
