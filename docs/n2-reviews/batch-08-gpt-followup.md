## Snapshot: be11959de0714d98c0f7a7d95bdbc8e687d86fc6; clean committed files only

**The original finding is resolved. No actionable defects or regressions were established in the corrected passages.**

Git execution is unavailable. Snapshot identity, clean-worktree status and diff provenance remain author-authenticated, not independently Git-verified.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`); family `gpt`

Sequential, read-only confirmation. Read the supplied `n2-batch-08-corrections.diff` completely and all six changed pages completely: `kanji\庫.md`, `kanji\延.md`, `kanji\恋.md`, `kanji\悩.md`, `kanji\戸.md`, and `kanji\承.md`.

Revisited the governing instructions, format reference, my initial report, relevant complete JMdict records, supplied Joyo extraction receipt, and exact public Wiktionary Japanese verb entry. Rechecked 戸’s three distractor labels.

**Not re-reviewed:** the unchanged nine kanji—弱, 律, 復, 快, 患, 憎, 技, 担, 拝—`words\憎む.md`, the 22 legacy word passages, and stroke files. Their initial coverage and limitations carry forward. No other reviewer’s report or prohibited authoring material was read.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\庫.md` | CLEAN | CLEAN | CLEAN |
| `kanji\延.md` | CLEAN | CLEAN | CLEAN |
| `kanji\恋.md` | CLEAN | CLEAN | CLEAN |
| `kanji\悩.md` | CLEAN | CLEAN | CLEAN |
| `kanji\戸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\承.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect within this bounded review.

## Findings:

**B08-GPT-01 — RESOLVED; originally Minor / scoped coverage — `kanji\恋.md:29,41,47`.** The table and note now explicitly identify 恋う／こう as literary, preventing its presentation as a neutral everyday verb. The original minimal remedy is implemented. The added “miss” sense and special forms 恋うて／こうて and 恋うた／こうた match the fetched [Japanese verb entry](https://en.wiktionary.org/wiki/恋う). JMdict entry **1558750**, retained at `docs\n2-batch-sources\batch-08.json:2157–2183`, independently supports the reading, “love” sense and special-class godan classification; its unlabelled sense is not misrepresented as supplying the literary label. **Confidence: high that the finding is resolved; usage evidence remains secondary.**

**No new findings.** The remaining corrections are supported without overstating their evidence:

- `kanji\庫.md:30,41,47` and `kanji\承.md:33,44,46,50`: recognition guidance preserves the dictionary readings while distinguishing Joyo-table status from rarity. The supplied complete table-row excerpts support the stated inclusions and omissions. JMdict entries **1592380** and **1329590** preserve the cited spelling lists; neither their order nor absent priority flags is used as a frequency ranking.
- `kanji\延.md:43` and `kanji\承.md:46`: “especially” accurately preserves JMdict’s **esp.** qualification rather than turning it into an exclusive restriction. Evidence: entry **1600290**, sense **7**; entry **1329590**, senses **7** and **10**.
- `kanji\悩.md:45`: the direct explanation correctly retains final み in kana, consistent with **悩み／なやみ**, entry **1469850**. `kanji\戸.md:3,14` clarifies the counter meaning without changing its scope or making “stone,” “return; revert,” or “shop” defensible answers.

My initial report contained no optional observations or unresolved consequential linguistic claims requiring further reconciliation.

## Optional:

None.

## Limits:

The Joyo claims were checked against the **author-generated bounded extraction receipt** and matching packet records. I did not independently download, hash or extract the binary government PDF; the supplied SHA256 is provenance information, not a hash I reproduced.

Raw JMdict downloads, transformations and full spelling-list extraction were not independently reproduced. The public Wiktionary entry was fetched and inspected directly; no publisher-dictionary search claim was used as evidence.

This was changed-passage confirmation, not a fresh full-batch review, exhaustive frequency study, native-speaker certification, manifest audit or stroke-path audit. No consequential linguistic uncertainty remains unresolved within the corrected passages on the supplied evidence.
