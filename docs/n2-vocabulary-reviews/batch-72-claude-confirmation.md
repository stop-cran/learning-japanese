# Batch-72 confirmation review (claude-opus-5.5)

## Snapshot
- **Revised frozen commit:** `5398d39999695042b16b4af3c4c42fcad307c889`
- **Parent:** `ded07a6f4969b3f63f2e62ae73511fade363ead1`
- **Content reviewed:** committed content only, as declared in `batch-72-correction-snapshot.json`.
- **Git limitation:** my file tools cannot run Git. The commit identity, clean checkout, hashes and rendering-equivalence checks were all run by the author, not re-run by me.

## Scope
**Model:** claude-opus-5.5 (family claude). Read-only: no edits, agents, delegation or shell.

**Complete fresh reads this pass:**
- Correction snapshot, patch and reconciliation.
- All 20 current articles. I reread 広げる, 広める, 響き, 響く, 美容 and 標本 a second time for citations.
- Kanji cards 皮, 準 and 膚.
- All 20 mappings, all 20 principal families (39 senses) and all 32 component records.
- `docs\n2-vocabulary-sources.tsv`: line 1 and lines 1422-1441 only.
- The three evidence files: correction comparison reading (16 families), public inspections, and public bodies.
- The 14 required older bodies: 拡張, 拡充, 揺れる, 美しい, きれい, 夜明け, 明け方, 日の入り, 暮れ, 伝える, 伝わる, 宣伝, 影響, 効果.
- `docs\content-format.md` lines 84-100.

**Not read in either pass:**
- The ten family-inspection chunks and the thirteen old-body-inspection chunks.

**Not read this pass:**
- labels.jsonl and public-bodies.json, both read only in the original pass.
- The optional corrected-review-evidence.json and completed-inspection.json.

**Inherited:**
- JMdict content only through the author's renderings.
- Daijisen through the frozen Weblio capture.
- Seisenban through the author's summaries.

**Fresh web retrievals (none used as evidence):**
- Merriam-Webster "dawn": HTTP 403.
- Weblio 夜明け, よあけ and あけがた: no applicable Daijisen heading was returned.
- Kotobank: returned an unrelated entry.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1422 | 日の出 | CLEAN | CLEAN | CLEAN | I accept the withdrawal of F-01. |
| N2:1423 | 響き | CLEAN | CLEAN | CLEAN | 影響 and 効果 guards accepted; footer now separates selected and additional senses. |
| N2:1424 | 響く | CLEAN | CLEAN | CLEAN | 揺れる guard accepted. |
| N2:1425 | 皮膚 | CLEAN | CLEAN | CLEAN | Only jlpt:2 was added; the body and the [肌, 皮] exclusions are preserved. |
| N2:1426 | 冷やす | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1427 | 百科事典 | CLEAN | CLEAN | CLEAN | Blank raw spelling preserved. |
| N2:1428 | 美容 | CLEAN | CLEAN | CLEAN | Removing 美しい and きれい is accepted. |
| N2:1429 | 表紙 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1430 | 標識 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1431 | 標準 | CLEAN | CLEAN | CLEAN | Footer now matches the mapping (selected 1, additional 2). |
| N2:1432 | 標本 | CLEAN | CLEAN | CLEAN | F-02 resolved. |
| N2:1433 | 評論 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1434 | 平仮名 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1435 | ビルディング | CLEAN | CLEAN | CLEAN | Blank raw spelling preserved. |
| N2:1436 | 昼寝 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1437 | 広げる | NEEDS FIX | CLEAN | CLEAN | The retained 伝える guard is a low-severity excess. |
| N2:1438 | 広さ | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1439 | 広場 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1440 | 広々 | CLEAN | CLEAN | CLEAN | Optional と clarification matches Daijisen's 「―（と）した部屋」. |
| N2:1441 | 広める | CLEAN | CLEAN | CLEAN | 拡張 and 拡充 guards accepted. |

**Separate assessments:**
- **皮 edit:** CLEAN. The ヒ row, Common words and footer ID 1483920 link 皮膚 ひふ.
- **準 edit:** CLEAN. The ジュン row, Common words and footer ID 1488710 link 標準 ひょうじゅん.
- **Unchanged 膚:** CLEAN. It already links 皮膚 with ID 1483920. All three reciprocal pairs hold at the actual readings, and existing kanji headers and examples are preserved.
- **Mappings:** CLEAN. All 20 are unchanged, and the footers now agree with them.
- **Raw TSV fields:** unchanged.
- **Kanji metadata:** every primary kanji is still listed, including those without a component card, and 々 is absent from 広々.
- **Baseline preservation:** CLEAN.
- **Regressions:** none found.

## Findings
**Dispositions of the original findings:**
- **GPT-F72-01 — RESOLVED.**
  - 広げる/拡張: strong. The 拡張 card's own example is "The city widened the road", and 広げる has 道を広げる.
  - 広げる/拡充 and 広める/拡張: supported by JMdict 1602370:1 (expand, enlarge) and 1278460:2 (extend, enlarge).
  - 広める/拡充: the weakest of the four, medium-low confidence. 拡充 itself already excludes 広がる.
  - Each edge has its own support, so this is not a copied clique.
- **GPT-F72-02 — RESOLVED.**
  - 響き/影響: frozen Daijisen ひびき sense 5 is glossed literally as 「影響」 and has a modern example, 「物価上昇の―」.
  - 響き/効果: accepted at medium-low confidence, through the "effect" reading of that same sense.
  - No N2 sense was added; the mapping is unchanged.
- **GPT-F72-03 — RESOLVED.** JMdict 1238610:2 (shake, vibrate) overlaps 揺れる "shake; sway", and the 響く body teaches vibration.
- **GPT-F72-04 — RESOLVED.** Under the title test in `content-format.md:94`, "beauty care; beautification" and "beautiful" are not mutually acceptable answers. 化粧 remains.
- **Claude-F-01 — WITHDRAWN (I accept).**
  - The 暮れ precedent rests on JMdict 1514950:1, which explicitly lists sunset and sundown. 夜明け and 明け方 have no equivalent sunrise gloss.
  - 夜明け.md:25 explicitly separates 日の出 from the broader brightening of the sky.
- **Claude-F-02 — RESOLVED.** "standard; norm; average" and "specimen; sample; example" are not mutually acceptable titles. The two separate 典型 guards do not make 標準 and 標本 a pair, because guards are not transitive.
- **Claude-F-03 — PARTIALLY RESOLVED.** Removing 伝わる and 宣伝 is verified. I **reject** keeping the 伝える guard; see the remaining finding.
- **Optional footer items and the 広々 clarification:** RESOLVED.
- **平仮名 字/文字 re-audit and 片仮名/日の入り links:** OPTIONAL, deferred, with no defect shown.

**Remaining finding — Claude-F-03 (residual):**
- **Severity:** low.
- **Facet:** Correctness (quiz_exclusions).
- **Location:** `words\広げる.md:9`.
- **Claim:** a learner could not reasonably accept either title, "spread out; widen; unfold" or "convey; tell", as the answer for the other word, so the guard fails the test in `content-format.md:94`.
- **Evidence:**
  - Daijisen ひろげる sense 6 is just 「広い範囲にゆきわたらせる。ひろめる。」, supported only by a literary 〈漱石・草枕〉 citation; senses 1-5 have modern examples.
  - JMdict 1602370 has no sense meaning convey or propagate.
  - The 伝える body teaches only conveying a message to a recipient.
  - `広める.md:41-42` itself says 伝える "need not make it widely known".
- **Remedy:** remove 伝える from 広げる's exclusions and keep the 広める/伝える guard.
- **Confidence:** medium.

## Optional
- 響き could mention the repercussion sense that now motivates its 影響/効果 guards. This is nonblocking, and the mapping should stay unchanged.
- The deferred 平仮名, 片仮名 and 日の入り items remain optional.

## Limits
- I could not run Git, so commit cleanliness and hashes are author-asserted.
- JMdict was not fetched independently. Daijisen evidence is the frozen capture from a single authority. The Seisenban evidence is author summaries, not raw pages.
- None of my fresh web retrievals produced usable evidence, and the failed Cambridge request is not evidence either.
- I did not recount the 31 senses in the comparison reading.
- I did not exhaustively search `words\` for every possible omitted guard.
- None of this guarantees exhaustive correctness, native-speaker certification, frequency or runtime-quiz behavior.
