## Snapshot: e02823f4e2628344b9ba4fd896fde675e6bce08d; committed files only

The frozen snapshot records a clean worktree and 59 scoped files, against baseline `95dcb10075d23a934e6ea2c801e27c71ff2de777`. **I had file tools, not Git execution:** the commit identity, clean state and exact diff scope are recorded snapshot assertions, not independently verified Git results.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed sequentially, independently and read-only, without agents or edits. Read all 17 pages below completely; compared all 15 metadata sets and 41 reading rows with the pinned evidence; checked all 45 new-kanji distractor assignments, useful word links, relevant word-answer labels and direct exclusions, and older two-choice kanji fallback.

Inspected the linked passages in context—not the entirety of unchanged teaching content—in these 22 articles under `words\`: `指輪.md`, `柔らかい.md`, `賞.md`, `賢い.md`, `贈り物.md`, `贈る.md`, `跡.md`, `踊り.md`, `踊る.md`, `軍.md`, `軍隊.md`, `軒.md`, `軽い.md`, `輪.md`, `輸入.md`, `輸出.md`, `辛い.md`, `農家.md`, `農業.md`, `農民.md`, `辺.md`, `辺り.md`.

Read the required instructions and format reference, the permitted source records, relevant confusable-word passages, comparison pages and relevant pinned app code. **Omitted:** exhaustive review of the 15 generated stroke drawings; comprehensive review of unchanged articles; `docs\n2-authoring-notes.md`, `docs\n2-review.md`, `REVIEW.md`, `docs\n2-reviews\`, session authoring inputs, author-check receipts and other reviewers’ outputs.

## Verdicts:

CLEAN means no established actionable defect within the assigned scope—not exhaustive truth or native-speaker certification.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\賞.md` | CLEAN | CLEAN | CLEAN |
| `kanji\賢.md` | CLEAN | CLEAN | CLEAN |
| `kanji\贈.md` | CLEAN | CLEAN | CLEAN |
| `kanji\超.md` | CLEAN | CLEAN | CLEAN |
| `kanji\跡.md` | CLEAN | CLEAN | CLEAN |
| `kanji\踊.md` | CLEAN | CLEAN | CLEAN |
| `kanji\軍.md` | CLEAN | CLEAN | CLEAN |
| `kanji\軒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\軟.md` | CLEAN | CLEAN | CLEAN |
| `kanji\軽.md` | CLEAN | CLEAN | CLEAN |
| `kanji\輪.md` | CLEAN | CLEAN | CLEAN |
| `kanji\輸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\辛.md` | CLEAN | CLEAN | CLEAN |
| `kanji\農.md` | CLEAN | CLEAN | CLEAN |
| `kanji\辺.md` | CLEAN | CLEAN | CLEAN |
| `words\超過.md` | CLEAN | CLEAN | CLEAN |
| `words\軟らかい.md` | CLEAN | CLEAN | CLEAN |

## Findings:

**None established.**

All kanji readings, primary stroke counts, canonical radicals/numbers and grade tags match the pinned records. All 41 reading rows have supporting lexical realizations, including the unusual readings and bound forms. The articles appropriately distinguish spelling rarity, kana preference and reading identity; they do not turn missing priority flags into frequency claims.

All 45 authored distractor assignments reference existing, semantically wrong answer labels, and every new kanji has a useful linked word article. The supporting words’ direct exclusions cover the established overlaps found in the scoped comparison, including secondary senses and the unqualified English **light** labels. No actionable defect was established in the 22 related link passages.

## Optional:

**O1 — Nonblocking quiz hardening; correctness/quiz coverage.** `kanji\出.md:11` could gain a third curated wrong option to protect reduced-content pools against the new `超` answer label (`kanji\超.md:3`).

The lexical overlap is real: JMdict entry **1338240**, sense 10, gives 出る “to exceed; to go over” (`docs\n2-batch-sources\batch-22.json:7535–7545`); entry **1593070**, sense 2, gives 超える “to exceed; to surpass” (`:4948–4959`). This is not merely a shared category.

However, it **does not establish a default four-choice defect with the full frozen content pool**. The [pinned QuizBuilder](https://github.com/stop-cran/kanji-cards-android/blob/8c130a25bdb4e444a80a2f78ef0d11b04bddc12f/app/src/main/java/io/github/stopcran/kanji/core/quiz/QuizBuilder.kt) fills 出’s single remaining slot by descending shared-tag count. 日 is an available distinct-title candidate sharing three tags with 出 (`kanji\日.md:3–5`; `kanji\出.md:3–5`), while 超 shares none (`kanji\超.md:3–5`). Thus 超 cannot take that slot in this full-pool configuration. **Confidence:** high in the overlap and the pinned-algorithm conclusion; no current fix is required on that basis.

## Limits:

The Git state, baseline diff, download hashes, converter execution and exact 59-file scope were not independently reproduced. The pinned stroke provenance was accepted; exhaustive drawing-path review was not assigned.

Quiz conclusions concern the documented default four-choice behavior and inspected pinned code, not an executed Android session, another app revision, larger quizzes or partial imports. Public lookups that failed or returned no relevant definition supplied no evidence. Dictionary selection was not treated as dictionary exhaustiveness, and attestation or priority flags were not treated as frequency measurements. No consequential linguistic claim remains unresolved within the reviewed scope.
