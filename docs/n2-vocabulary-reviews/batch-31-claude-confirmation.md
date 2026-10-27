## Snapshot
- **Corrected commit:** `51c96bc0b0f9ce230db86a55971efe258c17d61e`. Its parent is the authored `e0c3e67907cd8aa09f1c610f70c840e6f64aee74`.
- **Committed content only.** I read the working-tree files and checked them against the correction patch.
- **Provenance limits:** I can't run Git or compute hashes. The clean state, commit identity and evidence hash are author-executed receipts; I didn't verify them independently.

## Scope
- **Model:** claude-opus-5.5, claude family. I worked sequentially and alone, with no edits.
- **Twelve changed articles, read in full:** 先程, 削除, 作成, ささやく, さじ, 座敷, 差し支え, 差し引き, 刺身, 刺す, 注す, さすが.
- **Unchanged comparison articles read:** 削る, 書く, 宴会, パーティー, 会, 会合, 集まり, 生け花, はず, ざわざわ, 迷惑, 不自由, 面倒, 箸, 足す, 生, and also 先.
- **Patch:** the article diffs (lines 1442–1640) and the evidence hunk headers.
- **Evidence:**
  - The complete compact rendering of the 25 families and 137 senses.
  - `correctionEvidence`: labels, inspections, origin, `directQuizPairs`, `currentQuizDeclarations` and the full adjudication list.
  - Retained principal families 1593780, 1291990, 1565670, 1297760, 1298120, 1552390 and 2140120.
- **Public check:** the Kotobank 流石 link, fetched and read myself.
- **Rules applied:** the instruction files and `docs\content-format.md:18-126`.
- **Not read:** the forbidden canonical `batch-31.json` and any other report.
- **Not re-reviewed:** unchanged articles, the 作者 reuse, the kanji edit and the mappings. This is not a second full review.

## Verdicts
Facets are correctness / scoped coverage / comprehensibility.

| Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| 先程 | CLEAN | CLEAN | CLEAN |
| 削除 | CLEAN | CLEAN | CLEAN |
| 作成 | CLEAN | CLEAN | CLEAN |
| ささやく | CLEAN | CLEAN | CLEAN |
| さじ | CLEAN | CLEAN | CLEAN |
| 座敷 | CLEAN | CLEAN | CLEAN |
| 差し支え | CLEAN | CLEAN | CLEAN |
| 差し引き | CLEAN | CLEAN | CLEAN |
| 刺身 | CLEAN | CLEAN | CLEAN |
| 刺す | CLEAN | CLEAN | CLEAN |
| 注す | CLEAN | CLEAN | CLEAN |
| さすが | CLEAN | CLEAN | CLEAN |
| Appended evidence | CLEAN | CLEAN | CLEAN |

The appended evidence is author-extracted. It openly discloses the pre-existing 書く citation discrepancy and that the Nikkoku origin entry has no hash.

## Findings

**B31-R-01 (刺す) — Resolved.**
- `刺す.md:16-24` adds:
  - "stab" to the meaning.
  - The pattern "target with を, instrument with で".
  - The example 針で指を刺しました, "I pricked my finger with a needle."
- The insertion would have broken the old "second example" reference; it now correctly says "In the mosquito example".
- The pointed-object-を, destination-に and passive-actor-に distinctions are all kept.

**B31-R-02 (さすが type) — Resolved.**
- `さすが.md:6,8` now has type and tag `wago`.
- The Nikkoku origin (さ + す + がに) supports this. I fetched the Kotobank link myself, and it redirects to the 流石 Nikkoku body.
- Lines 27–29 keep the whole-word irregular-reading explanation and no longer say "jukujikun".

**B31-R-03 ("still") — Resolved.**
- Line 39 now glosses "still; all the same; after all", which matches sense 2 of 1552390 and sense 2 of 2140120.
- Line 45's "English 'still'" now has an antecedent.

**B31-R-04 (削除/削る) — Resolved.**
- 1298120:1 ("striking out") and 1298090:3 ("to delete; to cross out") overlap, and the 削る article teaches deletion.
- Declaring the exclusion on one side applies it in both directions, so 削る.md correctly stays unedited.

**B31-R-05 (注す) — Resolved.**
- Line 24 now uses the attested 杯をさす and gives its reading and translation.

**B31-R-06 (links) — Resolved.** All four required links are in place:
- さじ links 箸.
- 差し引き links 足す.
- 刺身 links 生 at なま, "raw" (1378450:1). It does not conflate せい (2088240).
- 先程 links 先 at さき.

**Optional hypotheses from my original report:**
- **Resolved:** 座敷/宴会, now five guards; 差し支え/迷惑, plus 面倒; ささやく/ざわざわ.
- **Agree with declining:** 挿す/生け花, さすが/はず, 不自由.

**Additional guard checked:** 作成/書く. Its "writing out" overlaps 1343950:1 "to write; to compose", so the guard is supported.

**Regressions:** none. Exclusions are symmetric, pairwise and nontransitive in both directions. The current headers match `currentQuizDeclarations`.

## Optional
- The 座敷↔会合 and 座敷↔集まり guards are broad but defensible: 座敷's sense 2 is itself a gathering. Their only cost is a smaller distractor pool.
- Still optional, as before:
  - A note on 差引's irregular okurigana.
  - Recognition of figurative uses of 刺す.
  - One prose sentence in さすが saying the word is native.
- Pre-existing and outside this scope: the 書く.md citation of 1343910 versus the extracted 1343950, and the 作者/著者 pair.

## Limits
- No Git or hash execution; I relied on the author receipts.
- The Weblio and Daijisen inspections, including 座敷 and 先程, are author receipts. I didn't fetch them myself.
- Bounded scope: unchanged articles, the 作者 reuse, the kanji edit and the mappings were not re-reviewed.
- No app quiz draws were run. There is no measured frequency, native-speaker certification or official JLPT syllabus behind these verdicts.
