## Snapshot
- **Corrected commit:** **b148e3670c00c73701ec5a84c95b2b4b0968ae33**.
- **Parent:** the authored snapshot 65c98d9db417dd02abd5f24f1b48a5d95947a3f1.
- **Basis:** committed content only, as claimed by the author.
- **Not independently verified:** my file tools can't run Git, hash, cleanliness or manifest checks, so those remain the author's checks. I did not inspect `.git`.

## Scope
- **Model:** claude-opus-5.5, Claude family. This was a read-only confirmation of my own initial review. I made no edits and used no agents.
- **Read first:** `batch-58-correction-snapshot.json`.
- **Read completely:**
  - `batch-58-correction.patch`.
  - All four changed articles: 出来上がる, 展開, 手頃 and 鉄砲.
  - `reconciliation-comparison-reading.txt`: all six families and 18 senses (1327660, 1340610, 1375790, 1406110, 1438010, 1440600).
  - `correction-existing-reading.txt`: the complete old bodies of 成長 and 揃う.
- **Read in part:** `corrected-review-evidence.json`, only lines 25407–25520 (start of the correction evidence) and 26122–26260 (`currentQuizDeclarations`). The current declarations match the articles.
- **Mappings:** the TSV header and all 20 rows N2:1142–1161. Associations, selected senses, additional senses and levels are identical to what I read initially.
- **Extra checks this turn:**
  - The 成長 and 揃う front matter is unchanged.
  - A grep of 鉄, 橋 and 照 confirms both reading-row and Common-words links for all five reciprocal pairs (鉄/鉄橋, 橋/鉄橋, 鉄/鉄砲, 照/照らす, 照/照る) at てっきょう, てっぽう, てる and てらす. The word-side links to the kanji cards are also present.
- **Inherited, not reread:**
  - My initial judgments on the 13 unchanged new articles, both reused articles (でこぼこ, 照らす) and all three kanji cards.
  - Those rest on initial complete reads of all 22 assigned bodies, the lossless compact JSONL renderings, public captures, and 10 full plus 8 front-matter comparison bodies. GPT read 117 additional older bodies, so our evidence depth is not equal.
- **Not read:** files outside this turn's seven-file allowlist, and all forbidden paths.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1142 | 出来上がる (new) | Full reread of corrected file | CLEAN | CLEAN | CLEAN |
| N2:1143 | 的確 (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1144 | 的確 (raw spelling 適確; same article) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1145 | 手首 (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1146 | でこぼこ (reused; raw spelling 凸凹) | Inherited initial full read and patch | CLEAN | CLEAN | CLEAN |
| N2:1147 | 手頃 (new) | Full reread of corrected file | CLEAN | CLEAN | CLEAN |
| N2:1148 | でたらめ (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1149 | 手帳 (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1150 | 鉄橋 (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1151 | 手続き (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1152 | 鉄砲 (new) | Full reread of corrected file | CLEAN | CLEAN | CLEAN |
| N2:1153 | テニスコート (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1154 | 手拭い (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1155 | 手前 (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1156 | 出迎え (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1157 | 出迎える (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1158 | 照らす (reused) | Inherited initial full read and patch | CLEAN | CLEAN | CLEAN |
| N2:1159 | 照る (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |
| N2:1160 | 展開 (new) | Full reread of corrected file | CLEAN | CLEAN | CLEAN |
| N2:1161 | 伝記 (new) | Inherited initial full read | CLEAN | CLEAN | CLEAN |

- **Reciprocal kanji: CLEAN.** This inherits my initial check and was re-confirmed by the grep this turn. The patch lists no kanji changes.
- **Baseline preservation: CLEAN.**
  - でこぼこ and 照らす are unchanged since my initial check.
  - The 成長 and 揃う front matter, including exclusions, matches the old bodies.
  - The correction added exactly two guards and removed none.
- **Mappings: CLEAN.** All 20 rows are unchanged and match the principal families. Two articles that previously contradicted their mapping notes now agree: 鉄砲 now qualifies 鉄炮 as rare, and 手頃 cites both selected senses.

## Findings
- **F-01, 手頃 footer under-cited its senses: RESOLVED.** `words\手頃.md:33` now cites "senses 1-2", matching 1327660:1–2 and the mapping. GPT's equivalent optional observation is acknowledged. The teaching itself was already present, so this was an attribution fix only.
- **F-02, 鉄炮 not qualified as rare: RESOLVED.** `words\鉄砲.md:23` now reads "鉄炮 is a rarely used dictionary spelling", matching JMdict's flag on 1438010. The primary spelling, reading and selected sense are unchanged.
- **F-03, 出来上がる/揃う guard: RESOLVED.** `words\出来上がる.md:9` adds 揃う.
  - My original rationale leaned partly on 揃う's existing guards against 仕上がる and できる. Neighbouring guards alone aren't enough, and I withdraw that part.
  - The direct evidence is sufficient: 1340610:1 means "to be completed / finished / ready" and 1406110:1 means "to be complete / make a full set / be satisfied (of conditions)". Both bodies have が-subject completion examples (服が出来上がる, 書類が揃う).
  - The guard prevents ambiguous quiz choices; it does not claim the words are freely interchangeable.
- **F-04, 展開/成長 guard: RESOLVED.** `words\展開.md:9` adds 成長.
  - The direct basis: 1440600:1 includes "development" and 1440600:2 includes "expansion; building up", while 1375790:1 includes "growth; development" and 1375790:2 is "growth of a company or the economy".
  - Both bodies have company examples (事業を展開, 会社が成長).
  - My earlier reliance on 発展's existing guard against 成長 is withdrawn as a sufficient basis on its own.
- **F-05, 展開 mixed pronunciation with meaning: RESOLVED.** `words\展開.md:25` now attributes the meaning to the characters and gives テン + カイ separately as the reading. It adds no historical claim.
- **Qualifications from my initial review stay settled:**
  - 木橋 is read もっきょう, verified on Kotobank (精選版日本国語大辞典).
  - The 手帳 cross-reference IDs 2530640 and 1830990 are verified.
  - The 照る/差す guard is supported, because the 差す article teaches the sunlight use 日が差す.
- **Regression check: no regressions found.** The new exclusion lists have no duplicates, both targets exist, there were no removals, and the new wording is accurate.
- **New findings: none.**

## Optional
These are all nonblocking:
- A dice-origin note for でたらめ.
- A sunny-weather example for 照る.
- A note on で marking the meeting place in 出迎える.
- The sumo thrusting technique for 鉄砲.
- Short body contrasts mentioning 揃う in 出来上がる and 成長 in 展開. These aren't required, since other exclusions also go unmentioned in bodies.
- 手段 and お目に掛かる as possible guards. These remain hypotheses, not established defects.

## Limits
- I could not run Git, hash, cleanliness or manifest checks. I can't tell committed content from the working tree, so I rely on the author's commit and hash assertions.
- I did not reread the 16 unchanged bodies this turn; their verdicts are inherited from my initial review. The two reused articles' baselines were checked through the patch in my initial review.
- I did not read the whole `corrected-review-evidence.json`, only the two excerpts listed above. I also did not read the private files that were outside my initial reads and outside this turn's allowlist.
- My comparison depth (10 full older bodies) is much lower than GPT's (117).
- The public captures all come from one dictionary service.
- I did not run quizzes, measure frequency, audit synonyms exhaustively, or obtain native-speaker certification.
