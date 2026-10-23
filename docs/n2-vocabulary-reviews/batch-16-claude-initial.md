## Snapshot
I reviewed frozen commit `a3f5bd39d72e1dfc5361a8d2c213ef0f7cb79cc5` (parent `f0c4257b1097bb0cde57718096f0a1ecbb0e0d14`), committed content only. I could read files but not run Git. So I read the working-tree files and relied on the receipt's statement that content is clean and committed; I did not recompute its normalized SHA-256 hashes.

## Scope
- **Model:** claude-opus-5.5 (family: claude). I worked sequentially, delegated nothing and edited nothing.
- **New articles:** I read all 20 new articles in full.
- **Related edits:** I read all 12 related files through the provided patch, with the changed passages in context. I did not review unchanged teaching in those files.
- **Mappings:** I checked rows N2:302–321 in the sources file against the principal JMdict families in `batch-16.json` (lines 12–1797). There are no reused principal articles.
- **Other evidence used:** quiz declarations, guard rationale and source-access limits (lines 15150–15300). I spot-read comparison entries 1577090 (かめい), 1422990 (きせる) and 1922120 (かねない), and used glob to confirm that link targets and kanji cards exist.
- **Fetched:** the Kotobank 仮定 page cited by the article (Daijisen and Nihon Kokugo Daijiten).
- **Not read:**
  - most of the comparison families (about lines 2583–15056) and of componentEvidence (to about line 2558);
  - any forbidden document.

## Verdicts
| Word | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 学科 | CLEAN | CLEAN | CLEAN |
| 学会 | CLEAN | CLEAN | CLEAN |
| 楽器 | CLEAN | CLEAN | CLEAN |
| 学級 | CLEAN | NEEDS FIX (F4) | CLEAN |
| 担ぐ | CLEAN | CLEAN | CLEAN |
| 括弧 | CLEAN | CLEAN | CLEAN |
| 活字 | CLEAN | CLEAN | CLEAN |
| 活躍 | CLEAN | CLEAN | CLEAN |
| 活力 | CLEAN | CLEAN | CLEAN |
| 仮定 | NEEDS FIX (F1) | CLEAN | CLEAN |
| 過程 | CLEAN | CLEAN | CLEAN |
| 課程 | CLEAN | CLEAN | CLEAN |
| 仮名 | CLEAN | CLEAN | CLEAN |
| 仮名遣い | CLEAN | CLEAN | CLEAN |
| 鐘 | CLEAN | CLEAN | CLEAN |
| 加熱 | CLEAN | CLEAN | CLEAN |
| 兼ねる | CLEAN | NEEDS FIX (F3) | CLEAN |
| カバー | CLEAN | CLEAN | CLEAN |
| 過半数 | CLEAN | CLEAN | CLEAN |
| 被せる | CLEAN | NEEDS FIX (F2) | CLEAN |

**Related changes (12 files): CLEAN on all three facets.**
- 担.md links 担ぐ at its actual reading.
- 課.md adds 課程 to Common words with JMdict entry 1195850.
- 被.md adds 被せる (かぶせる) to its readings table and Common words.
- 被る.md adds an accurate contrast between かぶる (on oneself) and かぶせる (on someone else).
- 学部, クラス, ベル, 片仮名, 送り仮名, 漢字, ピアノ and バイオリン gain link-only changes on mentions that already existed.
- Every new N2 primary word containing an N2 kanji now has a reciprocal example: 担/担ぐ, 課/課程, 被/被せる.

**Mappings (N2:302–321): CLEAN on all three facets.**
- All 20 rows match their article's spelling and reading exactly, and the selected senses are taught.
- 仮名 (N2:314): the raw gloss "alias, pseudonym" conflicts with the reading かな. It is handled correctly: 仮名.md:33 teaches kana and assigns the alias meaning to the separate word かめい (JMdict 1577090, which I verified).
- 学級 (N2:305): the raw gloss "grade" is correctly qualified against 学年 (学級.md:33).

**Metadata:**
- All kanji arrays are complete.
- Every link target I checked exists.
- Missing kanji cards (器, 級, 括, 弧, 躍, 仮, 遣, 鐘, 兼) are correctly left unlinked.

## Findings
**F1. Minor. Correctness. 仮定.md:21**
- **Claim and impact:** "Use a plain clause before と; a noun predicate retains だ" reads as a fixed rule. Learners may reject natural forms that drop だ, and they don't learn the common pattern XをYと仮定する.
- **Remedy:** Change to "a noun predicate often keeps だ (一万円だと仮定する)". Optionally add an XをYと仮定する example.
- **Evidence:** The Nihon Kokugo Daijiten entry on the article's own cited Kotobank page has the example 「政党の真面目は此の如きものと仮定しますも」: a noun before と仮定 with no だ. Pattern XをYと仮定する (e.g., 半径をrと仮定する) is ordinary modern usage; this is reviewer knowledge.
- **Confidence:** medium-high.

**F2. Minor. Coverage (quiz). 被せる.md:9 and :34**
- **Claim and impact:** The article teaches the "pour over" sense (line 34; JMdict 1484320 sense 3, "pour liquid on") and excludes 注ぐ "pour; devote". It does not exclude 浴びせる "pour over; shower someone with", and 浴びせる.md:8 does not exclude 被せる either. That label could be accepted for 被せる.
- **Remedy:** Add 浴びせる to 被せる's `quiz_exclusions`. One side is enough because the app applies exclusions symmetrically.
- **Evidence:** The author's own guard rationale says "被せる protects covering, pouring-over and blame labels".
- **Confidence:** medium.

**F3. Minor. Coverage (quiz). 兼ねる.md:1–9**
- **Claim and impact:** There is no `quiz_exclusions` field and no quizDeclarations entry for 兼ねる. The title "cannot readily do" overlaps 難しい "difficult; hard to do" (難しい.md:4). The article itself (line 15) says ～かねる means to "find it difficult to do", so a learner could reasonably accept 難しい's title for 兼ねる.
- **Remedy:** Add `quiz_exclusions: [難しい]`. Optionally also add どうしても ("simply cannot"), which is a weaker overlap.
- **Confidence:** medium.

**F4. Minor. Coverage (quiz). 学級.md:9**
- **Claim and impact:** 学級 excludes 教室 "classroom, class" but not 授業 "class, lesson" (授業.md:5). JMdict 1206680 glosses 学級 as "(school) class", so a learner could accept "class, lesson" for 学級. The article contrasts the two words (line 29), but the quiz doesn't protect that contrast.
- **Remedy:** Add 授業 to the list.
- **Evidence:** The author already pairs 授業 with 課程 in that word's quiz declarations.
- **Confidence:** medium-high.

## Optional
- Possible further exclusions, all low risk:
  - カバー vs 皮 ("outer covering")
  - 仮定 vs もし or もしも ("supposing")
  - 被せる vs 着る or 乗せる ("put on")
  - 仮名遣い vs 送り仮名
  - 学会 vs 組合 ("association")
- 括弧: the article mentions that it can take する but gives no する example.
- 担ぐ: the "fool someone" sense would benefit from a full example sentence.

## Limits
- I could not run Git, and I did not recompute the receipt's hashes.
- I fetched only the Kotobank 仮定 page. The other usage citations (学級, 被せる, 兼ねる and so on) and the author's inspection receipts were not checked independently; I treated them as the author's claims.
- I did not read most of the comparison families or the KANJIDIC2 component evidence. I checked the kanji arrays directly against the written forms instead.
- Whether the examples sound natural is my judgment as a reviewer, not native-speaker certification.
- I did not run the app's quiz or any validator; I took exclusion behavior from the docs.
