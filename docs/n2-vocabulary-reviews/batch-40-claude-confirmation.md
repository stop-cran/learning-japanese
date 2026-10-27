## Snapshot
Corrected commit `be09163bbaac80c0e58d21f91c5dddea0eb6fcce` (parent `5769c83f86c2c719c8d38a4f6892cfeee848aab5`). I reviewed committed content only. Model: claude-opus-5.5 (Claude family). I used file tools only and could not run Git or compute hashes, so I could not confirm the clean tree, exact delta or manifest `200bdecf86266b25`; those are author receipts.

## Scope
- **Reread in this pass:**
  - batch-40-correction-snapshot.json and batch-40-correction.patch.
  - 食器.md, 知り合い.md and 素人.md, completely.
  - batch-40-corrections-comparison-reading.txt in full (all 12 families).
  - batch-40-corrections-existing-bodies.txt in full (ご存じ, 器具, 名人, 料理).
  - confirmation-evidence.json lines 13575–13800 (correctionEvidence).
  - content-format.md lines 38–46 and 78–90.
  - TSV rows N2:791, N2:796 and N2:801.
  - A title search for novice/beginner/container/utensil-type labels, and a check for cards named 初心者, 知人, 新人, 新米, 未熟, 容器 or 玄人 (none exist).
- **Carried over from my initial review at 5769c83, not re-inspected at be09163:** the 13 unchanged articles, the four kanji edits, the four narrow reuses, 籍/書籍, and the other 17 mappings. I rely on the author's receipt that these are unchanged.
- **Not read:** corrections-comparisons.json (I read its rendering instead), corrections-comparison-forms.json, the additionalComparisonEntryFamilies section and the rest of confirmation-evidence.json, extra-comparison-reading.txt, public-bodies.json, both snapshot JSONs, confusable-words.md and jlpt-levels.md. No web fetches. No forbidden files: the receipt lists their names and hashes, but I did not open them.

## Verdicts
My initial report grouped 14 articles into one row, so it did not meet this one-row-per-article request. Each article now has its own row. Order: correctness / scoped coverage / comprehensibility.

| # | Article | Basis | Verdict |
|---|---|---|---|
| 1 | 消耗 | Inherited | CLEAN / CLEAN / CLEAN |
| 2 | 省略 | Inherited | CLEAN / CLEAN / CLEAN |
| 3 | 初級 | Inherited | CLEAN / CLEAN / CLEAN |
| 4 | 助教授 | Inherited | CLEAN / CLEAN / CLEAN |
| 5 | 食塩 | Inherited | CLEAN / CLEAN / CLEAN |
| 6 | 職人 | Inherited | CLEAN / CLEAN / CLEAN |
| 7 | 初旬 | Inherited | CLEAN / CLEAN / CLEAN |
| 8 | 食器 | **Reread** | CLEAN / CLEAN / CLEAN |
| 9 | ショップ | Inherited | CLEAN / CLEAN / CLEAN |
| 10 | 書道 | Inherited | CLEAN / CLEAN / CLEAN |
| 11 | 白髪 | Inherited | CLEAN / CLEAN / CLEAN |
| 12 | 知り合い | **Reread** | CLEAN (was NEEDS FIX) / CLEAN / CLEAN |
| 13 | シリーズ | Inherited | CLEAN / CLEAN / CLEAN |
| 14 | 私立 | Inherited | CLEAN / CLEAN / CLEAN |
| 15 | 汁 | Inherited | CLEAN / CLEAN / CLEAN |
| 16 | 素人 | **Reread** | CLEAN / CLEAN (was NEEDS FIX) / CLEAN |

- **Kanji edits:** 省, 略, 塩 and 油 stay CLEAN (inherited).
- **籍/書籍:** stays CLEAN (inherited).
- **Narrow reuses:** しょうゆ, 書籍, 書店 and 資料 stay CLEAN (inherited).
- **Mappings:** all 20 are CLEAN. N2:801's coverage finding is resolved. I reread rows 791, 796 and 801, and they match my initial reading.

## Findings
**B40-F1 (知り合い/ご存じ) — resolved.** `words\知り合い.md:9` now has `quiz_exclusions: [ご存じ]`.
- The support is stronger than my original argument: JMdict 1593570 sense 2 is "(an) acquaintance", and the ご存じ card (lines 4, 15, 20) teaches "being acquainted".
- content-format.md:86 says exclusions apply both ways even when only one card declares them, so one declaration is enough. The target exists, with no duplicate or self ID.

**B40-F2 (素人 novice sense) — resolved.** `words\素人.md:17-18` now says it "can also describe a novice: someone inexperienced or lacking the skills needed in that field."
- This matches JMdict 1397270 sense 1 ("novice") and Daijisen sense 1 (経験が浅く、未熟な人／必要な技能や知識をもっていない人).
- It does not contradict line 35 ("need not be new") or lines 41–42 ("An amateur can be skilled"): "can" and "need not" fit together.
- No new quiz collision: there is no 初心者 or novice card, and 初級's "beginner level" names a level, not a person, with no shared kanji.

**B40-GPT-01 (食器/料理) — accepted.**
- JMdict 1554310 sense 1 includes "dish", and the 料理 card title is "cooking; cuisine; dish". Against 食器's "tableware; dishes", the bare English "dish/dishes" is ambiguous.
- `食器.md:40-43` still teaches the Japanese distinction between utensils and food, so the exclusion is a safeguard, not a synonymy claim.
- My initial review left this pair unflagged. I now agree the exclusion is supported and not excessive.

**Adopted optional 食器/器具 — accepted.**
- JMdict 1218920 sense 1 glosses 器具 as "utensil, implement", and Daijisen defines 食器 as 食事に使う容器・器具.
- 器具's own four exclusions are untouched, and no broader exclusion set across all tool words was added.
- I considered 道具 ("tool; implement") and 入れ物/ケース ("container") as further pairs. These labels are broader and share no kanji with 食器, so they are not consequential and not findings.

**No remaining consequential issues and no regressions.** No exclusions were deleted, titles, identities, readings and levels are unchanged, and nothing was added beyond the three-card delta.

## Optional
- **職人/名人:** not adopting this is reasonable. The 名人 body stresses exceptional mastery, while 職人 is an occupational craftsperson. It stays optional.
- **知り合いになる** and **消耗's しょうこう history:** these stay optional expansions, not defects.
- **白髪:** I withdraw my earlier consistency point. JMdict gives しらが no special-reading flag, unlike 素人's しろうと, so `type: wago` follows the cited dictionary. My recollection about the 常用漢字表付表 is still unverified.
- **N2:801 note:** it could mention "novice" for traceability. This is not needed, because the selected sense 1 already includes it.

## Limits
- I did not run Git, hash checks, validators or real quiz draws, and I did not inspect the QuizBuilder code.
- All Daijisen, MEXT and JMdict material comes from the author's captures; I made no fresh retrievals.
- I did not reread the claimed 126 families/239 senses, 114 labels, 70 existing bodies or 34 components; I read only the files listed under Scope.
- The 13 inherited article rows and the kanji, reuse and mapping verdicts depend on the author's receipt that those files are unchanged.
- This is not a native-speaker certification.
