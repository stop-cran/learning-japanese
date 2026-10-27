## Snapshot
The follow-up commit is `84ba65fcfaaa5784daca1841f35aabe26e917a8a`, with parent `5c9570bb46ccbee8376d7cbfa48eca1ca916b6a2`. I took both from `batch-66-followup-snapshot.json`, which I read first. It lists one changed content file, `words/バイバイ.md`. This review covers committed content only: file tools can't run Git, hash or cleanliness checks, and I did not inspect `.git`.

## Scope
**Model:** claude-opus-5.5 (family claude). Read-only, with no edits, agents or delegation.

**Read completely this turn:**
- `followup-snapshot.json` and the full `followup.patch`. The patch is a one-line change at `バイバイ.md:9`.
- `followup-evidence.txt` through EOF: complete family 1005900 and the complete unchanged `words\じゃ.md`.
- The current `words\バイバイ.md`, which matches the patch.
- The TSV header (line 1) and exactly rows N2:1302–1321, matched by source ID.

**Read in part:**
- `followup-review-evidence.json`, lines 34940–35010 (the author's disposition), found by grep.
- `words\` searches only: farewell titles, and any card that excludes バイバイ.

**Not reread this turn:** `correction-snapshot.json`, which I read in the prior turn; its parent matches.

**Inherited:**
- The six other first-correction bodies, and the 16 comparison bodies and 18 families/54 senses, from my first confirmation.
- All unchanged cards, the four edited kanji, 伸, the related patch, the derivatives and the Daijisen captures, from my initial review.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1302 | words\のこぎり.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1303 | words\残らず.md | inherited first confirmation | CLEAN | CLEAN | CLEAN |
| N2:1304 | words\乗せる.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1305 | words\覗く.md | inherited first confirmation | CLEAN | CLEAN | CLEAN |
| N2:1306 | words\伸ばす.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1307 | words\伸びる.md | inherited initial + first confirmation | CLEAN | CLEAN | CLEAN |
| N2:1308 | words\上り.md | inherited first confirmation | CLEAN | CLEAN | CLEAN |
| N2:1309 | words\登る.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1310 | words\糊.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1311 | words\乗り換え.md | inherited first confirmation | CLEAN | CLEAN | CLEAN |
| N2:1312 | words\載る.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1313 | words\のろい.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1314 | words\のろのろ.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1315 | words\のんき.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1316 | words\灰色.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1317 | words\俳句.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1318 | words\売店.md | inherited first confirmation | CLEAN | CLEAN | CLEAN |
| N2:1319 | words\バイバイ.md | fresh full reread (follow-up) | CLEAN | CLEAN | CLEAN |
| N2:1320 | words\売買.md | inherited initial | CLEAN | CLEAN | CLEAN |
| N2:1321 | words\這う.md | inherited first confirmation | CLEAN | CLEAN | CLEAN |

- **Mappings: CLEAN.** I reread all 20 TSV rows this turn. Associations and selected/additional senses are unchanged. 1358870:8 stays restricted to the taught spelling 延びる.
- **Baseline preservation: CLEAN, judged from the patch.** Only `バイバイ.md:9` changes. N3 乗せる/伸ばす/伸びる and N5 登る are preserved, and のろのろ only has `jlpt2`. Hashes were checked by the author, not by me.
- **Edited kanji 延, 換, 灰, 鈍: CLEAN (inherited initial).** 鈍 keeps its Common words/Notes alias link and has no invented のろ reading row.
- **Unchanged 伸: CLEAN (inherited).**
- **Primary/alias reciprocal links: CLEAN (inherited).** 換/乗り換え and 灰/灰色; 延/伸ばす and 延/伸びる in the shared 伸 articles; 鈍/のろい.

## Findings
**B66-Q4 (バイバイ/じゃ): resolved.** `バイバイ.md:9` now lists `じゃ`. I agree with the change on lexical grounds:
- `じゃ.md:15` explicitly teaches じゃ for moving to a "farewell". Its second example, じゃ、私は帰ります, is a leave-taking.
- So a learner shown "bye-bye; goodbye" could plausibly pick じゃ in a closing context.
- Family 1005900 has one connector sense only ("then; well; so; well then"), with no goodbye sense. The guard therefore rests on the taught farewell use, not on the shared title, family membership, the さて edge or transitivity.
- The guard is conservative, not a blanket rule for all connectors or a claim that じゃ is a standalone goodbye.
- **Confidence:** medium that it belongs alongside the existing じゃあ guard; medium-low that it is strictly necessary.
- This was a candidate I missed initially, not a regression.

**Regression check: none found.**
- `words\じゃ.md` exists, and the list has no duplicates.
- じゃ.md declares no exclusions, so nothing conflicts in reverse, and no other card excludes バイバイ.
- Every farewell-titled card (さようなら, 別れ, 送別) is already excluded.
- There are no prose, title, reading, level or kanji changes.

**My other prior items:** no change. B66-Q1, Q2 and Q3 and the optional decisions on 上り, 覗く and 送別 stay resolved. My withdrawn 全然/さっぱり concern stays withdrawn. No new actionable defects.

## Optional
- **Necessity confidence differs between the two guards.** The じゃあ body teaches the standalone closing じゃあね; the じゃ body teaches only the connector introducing a farewell. Keeping both guards is defensible caution, not a requirement.
- **Unchanged nonblocking notes:** 乗り換え/移す is a guard of moderate strength. 売店/売り場 and 残らず/一人一人 or それぞれ are not established pairs. Title polish for のこぎり and 乗り換え remains optional.

## Limits
- I ran no Git, hash, manifest or validator checks; baseline preservation relies on the patch and author receipts.
- Unchanged cards and kanji were not reread this turn; their verdicts are inherited.
- There is no public confirmation of the farewell use of じゃ or じゃあ. The evidence is the project bodies plus one pinned JMdict family, and the earlier public captures come from a single source (Daijisen via Weblio).
- There were no live quiz draws, native-speaker certification, frequency study or exhaustive ambiguity audit.
- The batch-61 issues (飛ぶ/飛行, 止まる/止む) remain deferred.
