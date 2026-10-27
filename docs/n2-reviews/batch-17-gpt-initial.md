## Snapshot: e80e0c452d4cd55c9bee9a3ab125b40fc85be953 — committed files only

The frozen manifest identifies this commit, reports `clean: true`, and records a 54-file scope. Baseline: `eb9376ba6afa36d7e3803c788427797f15fa1750`. **One actionable quiz-exclusion defect was established.** No files were edited.

## Scope: gpt-6.1-sol; family gpt

Single independent reviewer, working sequentially without delegation. Read all 18 pages below completely. Checked every kanji’s readings, primary stroke count, canonical radical and grade against the pinned record; all 41 reading rows, including the three explicitly qualified source-only rows; all 45 new-kanji distractor assignments; useful word links; supporting-word quiz exclusions; and newly activated risks in older two-choice fallbacks.

Inspected the linked passages in these existing word articles, without comprehensively reviewing their unchanged teaching content: `単純`, `地平線`, `建築`, `木綿`, `簡単`, `粉`, `糸`, `紅茶`, `細い`, `細かい`, `紹介`, `綿`, `緑`, `連絡`, and `線`. Also inspected the distractor change in `kanji\小.md` in context. No defect was established in these narrow related edits or the 45 curated kanji distractors.

Read the required instructions and format reference, the two allowed source records, and relevant comparison pages. Did **not** read the prohibited authoring notes, review ledgers, review directories, authoring inputs, author-check receipts, or other reviewers’ outputs. Generated stroke drawings and other ancillary changes were not comprehensively reviewed.

## Verdicts: 18 assigned pages

**CLEAN** means no established actionable defect within the assigned scope, not exhaustive truth or native-speaker certification.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\築.md` | CLEAN | CLEAN | CLEAN |
| `kanji\簡.md` | CLEAN | CLEAN | CLEAN |
| `kanji\籍.md` | CLEAN | CLEAN | CLEAN |
| `kanji\粉.md` | CLEAN | CLEAN | CLEAN |
| `kanji\粒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\糸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\紅.md` | CLEAN | CLEAN | CLEAN |
| `kanji\純.md` | CLEAN | CLEAN | CLEAN |
| `kanji\細.md` | CLEAN | CLEAN | CLEAN |
| `kanji\紹.md` | CLEAN | CLEAN | CLEAN |
| `kanji\絡.md` | CLEAN | CLEAN | CLEAN |
| `kanji\綿.md` | CLEAN | CLEAN | CLEAN |
| `kanji\総.md` | CLEAN | CLEAN | CLEAN |
| `kanji\緑.md` | CLEAN | CLEAN | CLEAN |
| `kanji\線.md` | CLEAN | CLEAN | CLEAN |
| `words\書籍.md` | CLEAN | CLEAN | CLEAN |
| `words\粒.md` | **NEEDS FIX** | CLEAN | CLEAN |
| `words\総額.md` | CLEAN | CLEAN | CLEAN |

## Findings: GPT-17-01

**Medium severity — correctness, quiz-answer ambiguity — `words\粒.md:4,8`.**

The new answer label **“grain; bead; drop”** remains eligible opposite both `玉` and `球`. Those written words have an applicable **たま** reading meaning a bead or droplet, so the new label can be a defensible answer rather than a genuinely wrong choice. `球` having **きゅう** as its primary card reading does not eliminate its other taught lexical reading. Its existing exclusion with `玉` does not protect either word from `粒`: exclusions are not transitive.

**Minimal remedy:** add both direct exclusions to `words\粒.md`, preserving its accurate definition:

```yaml
quiz_exclusions: [穀物, 米, 水滴, 玉, 球]
```

**Exact evidence:**
- `docs\n2-batch-sources\batch-17.json:2723–2818`, JMdict **1552890**, supports 粒／つぶ, sense 1, **“grain; bead; drop.”**
- `words\玉.md:3–8,33–35,44` identifies 玉／たま and JMdict **1240530**, with no exclusion for 粒.
- `words\球.md:3–9,16,25,35` explicitly teaches both きゅう and たま; its sole exclusion is 玉.
- Independently fetched [Jisho’s JMdict-backed 玉 entry](https://jisho.org/api/v1/search/words?keyword=%E7%8E%89) lists **玉／たま** and **球／たま**. Its second dictionary sense is **“bead (of sweat, dew, etc.); drop; droplet”**, with no spelling or reading restriction on that sense.
- No reverse declaration excluding 粒 was found on either existing card.

**Confidence: high.** This is an answer-label/exclusion defect, not a claim that every construction using these words permits substitution.

## Optional: none

## Limits: provenance and validation boundaries

Only file and web tools were available—**no Git execution**. The commit identity, cleanliness and 54-file scope therefore come from the frozen manifest and supplied scope; I could not independently verify the worktree against that commit, inspect the baseline diff, or reproduce the recorded hashes.

The 15 stroke files were supplied as outputs of the pinned repository converter; exhaustive drawing-path and stroke-order review was not assigned and was not performed.

The qualified source-only rows—簡／えら.ぶ, 総／す.べて, and 線／すじ—were assessed as lookup-only disclosures, not verified everyday lexical examples or claims of dictionary absence. Dictionary attestation was not treated as frequency or corpus proof of naturalness.

The direct JMdictDB lookup for entry 1240530 returned an access gate, not an entry; the finding instead uses the successfully fetched matching Jisho entry. Live public evidence is not itself the pinned dictionary download. No other consequential teaching claim remained unresolved within the reviewed scope.
