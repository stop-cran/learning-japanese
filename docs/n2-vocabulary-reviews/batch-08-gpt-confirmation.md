## Snapshot: `5cabdf7ea6ee50bf59bc1a743c76f7797dfcbd6f` — author-supplied identity

The receipt identifies this correction as directly following `c3e705025de8ed252789968a9a37ab0535ddf3a3`. Current file contents agree with the supplied changed passages. Commit identity, parentage, cleanliness and hash checks remain **author provenance**, not independently executed Git verification.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed the supplied nine-file correction: six changed cards—延長, 応ずる, 応接, 応対, 往復 and 追い越す—plus `docs\n2-vocabulary-batch-sources\batch-08.json`, `docs\n2-vocabulary-sources.tsv` and `docs\n2-vocabulary-snapshot.json`. This covers **six direct pairs, one particle-explanation edit and synchronized provenance**, not another full-batch review.

Read all six changed cards and all five actual comparison cards—続き, 受ける, 扱う, 便り and 越える—in full, including their displayed titles and taught uses. Inspected the three added complete comparison families, retained 受ける and 越える families, unchanged 延長 family, relevant principal senses, and correction receipts. The supplied patch leaves original family, row and component records intact apart from the assigned source-note correction.

Independently retrieved the four public entries: [続き](https://kotobank.jp/word/続き-571885), [受ける](https://kotobank.jp/word/受ける-439397), [扱う](https://kotobank.jp/word/扱う-425433) and [往復](https://kotobank.jp/word/往復-449276). Relevant definitions rendered in **Daijisen** for 続き and 往復, and **Seisenban** for 受ける and 扱う; the latter two pages’ Daijisen headings did not expose definitions.

Applied the three required guidance documents. No edits, Git commands, delegation, prohibited review files or other reviewer output.

## Verdicts: All assigned corrections CLEAN

| Changed article/correction | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 延長: direct 続き guard | CLEAN | CLEAN | CLEAN |
| 応ずる: direct 受ける guard | CLEAN | CLEAN | CLEAN |
| 応接: direct 扱う guard | CLEAN | CLEAN | CLEAN |
| 応対: direct 扱う guard and particle clarification | CLEAN | CLEAN | CLEAN |
| 往復: direct 便り guard | CLEAN | CLEAN | CLEAN |
| 追い越す: direct 越える guard | CLEAN | CLEAN | CLEAN |
| N2:148 source note, added evidence and refreshed index-hash reference | CLEAN | CLEAN | CLEAN |

Each new guard names an existing exact word ID, preserves previous exclusions, and introduces no duplicate, self-reference or distractor conflict in the inspected cards. Each pair has applicable meaning/answer-label overlap; none rests solely on a shared component or topic. One-sided declarations suffice under the documented symmetric, **non-transitive** contract.

The packet and TSV now correctly identify omitted 延長 senses **4–6** as mathematics, philosophy and the Enchō era. Selected senses **1, 2, 3 and 7 remain unchanged**. The snapshot’s refreshed `coverageIndexSha256` is:

`5bb2b4b73f90472358a99415231909d27c791b1fa9146fda202422f5b37810b2`

This matches the receipt’s asserted normalized TSV hash; I did not recompute it.

## Findings: Original findings resolved; no actionable regression

All four original **Minor · Correctness** findings are **resolved**, with high confidence.

| Original ID | Reconciliation and precise evidence |
|---|---|
| **GPT-B08-01** | **Resolved** at `words\延長.md:9`: direct 続き exclusion. 延長’s acknowledged continuation sense overlaps 続き’s “continuation; rest of a story or task” label. JMdict 1176510:3 and 1894690:1 support this; independently retrieved Daijisen 続き:1 explicitly uses 延長. |
| **GPT-B08-02** | **Resolved** at `words\応ずる.md:9`: direct 受ける exclusion removes reliance on an exclusion chain. Ordinary accepting-a-challenge in JMdict 1329590:5 supports the “accept” overlap despite 受ける’s narrower displayed “receive; undergo” title. This does **not** generalize the Go-specific response sense 13. Seisenban [1][一]③–④ separately corroborates acceptance/response uses. |
| **GPT-B08-03** | **Resolved on both cards**, at `words\応接.md:9` and `words\応対.md:9`: each directly excludes 扱う. JMdict 1153440:1 covers dealing with people, handling and entertaining; principal entries 1179930:1 and 1179980:1 support the overlap. Seisenban 扱う② explicitly associates the use with 応対. |
| **GPT-B08-04** | **Resolved** at `words\往復.md:9`: direct 便り exclusion. 往復’s correspondence sense overlaps 便り’s displayed “news; correspondence” label. JMdict 1179760:3 and 1512410:1 support this; independently retrieved Daijisen 往復:2 confirms exchanging letters. An exchange and an individual communication need not be freely substitutable Japanese expressions. |

The additional corrections also withstand independent assessment:

- **追い越す–越える**, `words\追い越す.md:9`: justified by the actual “overtake; surpass” and “cross over; go beyond” labels and their surpassing uses, not merely shared 越. JMdict 1432280:2 and 1593070:2 support the overlap. “Especially 超える” is a **spelling preference**, not a restriction excluding 越える.
- **Particle clarification**, `words\応対.md:26–27`: “In the second example, を” accurately identifies the example. を marks 電話の応対 as the activity being practised by 練習する; it does not establish transitive 応対する.
- **Provenance correction**, `docs\n2-vocabulary-batch-sources\batch-08.json:127–134` and `docs\n2-vocabulary-sources.tsv:148`: accurately matches the unchanged principal family’s senses. The synchronized snapshot reference is at `docs\n2-vocabulary-snapshot.json:34`.

No further required remedy was established.

## Optional: None

No nonblocking expansion or precision polish is necessary in this bounded correction.

## Limits: Provenance and runtime verification remain unexecuted

No consequential linguistic claim remains unresolved within the assigned changes. The author’s source-hash rechecks and re-extraction equality assertions were not independently reproduced; inspecting the supplied complete families is not verification against the original dictionary downloads.

The app and validation tools were not executed. Quiz conclusions are static assessments under the documented exclusion-aware behavior; older apps ignore these guards. **CLEAN** is limited to these corrections and necessary comparison contexts, not exhaustive correctness or native-speaker certification.
