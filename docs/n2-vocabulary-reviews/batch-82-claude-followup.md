## Snapshot

- **Revised commit:** 76a5a8505c135eb33e550fef10f805c2cd7d57a7
- **Parent:** 6244a236f9ba26870928c7721f16903b367cbdae
- **Committed content only.** File tools cannot run Git. Clean state, file and patch hashes, and preservation are the author's assertions, not checks I made. I make no claim of independent byte verification.

## Scope

**Model:** claude-opus-5.5 (claude family). I made no edits.

**Fresh complete reads:**
- **Follow-up files:** the snapshot (read first), the two-line patch and the reconciliation. The reconciliation's first view returned only a size error; a forced read then returned it in full.
- **Instructions:** both instruction files and content-format.md:76-103.
- **Word bodies:** all eight (無地, 向かう, 原, 野, 顔, 蒸す, 蒸気, 水蒸気).
- **Families:** followup-families.jsonl, all 8 families / 19 senses.
- **Grep:** title and exclusion lines for 地味 and 対する.

**Live American Heritage fetches:** plain, face and steam all returned full entries. None is hashed.

**Inherited from my confirmation at 6244a23:**
- The other 18 rows, mappings, components and 蒸.md reciprocity.
- CW091, the 20 TSV rows and the public bodies.

**Scheduling deviation:** I issued 無地, 向かう, 原 and 野 as four parallel views in one turn. Every other call was serial. The reconciliation's record of my previous turn (up to three calls outstanding) matches the two triple reads I disclosed then.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1622 | 見慣れる | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1623 | 醜い | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1624 | 実る | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1625 | 身分 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1626 | 見本 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1627 | 見舞う | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1628 | 未満 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1629 | 名字 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1630 | ミリ | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1631 | 診る | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1632 | 民間 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1633 | 民謡 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1634 | 向かう | CLEAN | CLEAN | CLEAN | B82-06 resolved; baseline preserved |
| N2:1635 | むく | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1636 | 無限 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1637 | 無地 | CLEAN | CLEAN | CLEAN | B82-05 resolved |
| N2:1638 | 蒸し暑い | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1639 | 矛盾 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1640 | 蒸す | NEEDS FIX | CLEAN | CLEAN | B82-07: steam pair; fix on other cards |
| N2:1641 | 無数 | CLEAN | CLEAN | CLEAN | Inherited |

**Mappings, components and reciprocal pairs (蒸し暑い/蒸, 蒸す/蒸):** CLEAN. These are inherited; the patch touches none of them.

**Baseline preservation:** CLEAN.
- 向かう keeps N4, its title, reading, `[向]` and its body including line 25; only line 9 changed.
- 蒸す is unchanged.

**Declaration count:** 133, which matches my own recount.

## Findings

**B82-05: resolved.** I accept both new pairs, 無地/原 and 無地/野.
- 無地.md:4 "plain; patternless" and 原.md:4 / 野.md:4 "open field; plain" share bare "plain".
- American Heritage gives adjective 6 "Not dyed, twilled, or patterned" and noun 1a, level land.
- JMdict 1530650 sense 1, 1261140 sense 1 and 1537250 sense 1 keep the Japanese identities separate.
- The guard rests on ambiguity in the English label, not on a group of related topics. 原 and 野 have identical titles, so the app already deduplicates them.
- No regression: the list is valid and both targets exist.

**B82-06: resolved.** I accept the 向かう/顔 pair.
- Both titles contain bare "face". American Heritage gives transitive 1 and intransitive 1–2 (orientation) and noun 1a.
- JMdict 1604800 sense 1 is "to face"; 1217730 sense 1 is a noun. Nothing claims 顔 is a verb.
- No regression.

**B82-01, 03, 04, the object-role fix and the adopted polish:** remain resolved. **B82-02:** remains withdrawn. **GPT-01 to GPT-03:** remain as confirmed and are kept distinct from the Claude edges. No regressions.

**B82-07 (new; replaces my earlier steam limit): Minor; Correctness (quiz guard); medium confidence.**
- **Location:** 蒸す.md:4, 9 and 16-21; 蒸気.md:4, 9 and 29; 水蒸気.md:4 and 9.
- **Claim:** "steam; vapor" and "water vapor; steam" contain bare "steam".
  - American Heritage transitive 1 is "To expose to steam, as in cooking". That is 1356900 sense 1, which the 蒸す card teaches with 野菜を蒸します.
  - So a learner could reasonably accept either noun title for 蒸す, in both quiz directions.
- **Why the author's distinction does not hold:** the claimed difference ("qualified 'steam food'") is not material.
  - 実る "bear fruit" against 実 "fruit; substance" has the same structure: a qualified verb phrase on one card and a bare token on the other.
  - むく against 肌 "skin; surface texture" is the same, and so is 蒸し暑い against 近い "near; close". All three were accepted.
  - The reasoning "neither noun title means steam food" covers only one direction.
- **Coupling to this batch:** the issue predates the batch, as B82-06 did. The batch made 蒸す jlpt 2, the level 蒸気 and 水蒸気 already carry, and the three share 蒸, which content-format.md:80-81 says influences choice selection.
- **Remedy:** add 蒸す to the exclusions of 蒸気.md and 水蒸気.md. Either side's declaration covers both directions, so 蒸す stays byte-identical.

**Closure:** blocked only by B82-07. No other actionable defect or consequential unresolved claim remains in scope.

## Optional

- **Same issue outside the assigned rows:** 地味 "plain; unshowy" against 原 and 野, and 対する "face; be directed toward" against 顔, are unguarded. They cannot appear in 無地 or 向かう questions.
- **Earlier optional items still open:** 名字's "なじ" note, 無限/有限, 未満/以内, a predicate example for 見慣れる, the 無数 example, and the 民謡 wording.

## Limits

- **English evidence:** one dictionary authority, fetched live with no hashes.
- **Learner judgment:** whether a learner would "reasonably accept" a title is a judgment, not an empirical result.
- **App behaviour:** I did not verify the app's choice pools or how a card without a level, such as 顔, is selected.
- **Inherited rows:** the 18 unchanged rows were not reread.
- **No guarantees:** this does not establish exhaustive correctness, native-speaker certification, frequency, or how quizzes behave at runtime.
