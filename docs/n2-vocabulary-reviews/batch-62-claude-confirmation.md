# Batch 62 corrected confirmation review (claude-opus-5.5)

All twenty rows are now CLEAN. Both of my original findings (B62-01, B62-02) are fixed. The author's added quiz exclusions introduce no regressions, and I found no new defects.

## Snapshot
- **Corrected commit:** 8b26a20ba93ffeeaaf10e4f1b9eb55cbf49dd26d. Parent: 329ee65a6b15e20d59cf3426b50dc51aafecd408. The original blind snapshot was 329ee65a… on parent df77fa11….
- I reviewed committed content only. My file tools can't run Git, hash or cleanliness checks, so the commit identity and `cleanCommittedContent: true` are as the author reports them. I did not look inside `.git`.

## Scope
**Model:** claude-opus-5.5 (claude family). Read-only, with no agents or delegation.

**Read fresh in this session:**
- Private files:
  - `correction-snapshot.json` (read first).
  - The complete `correction.patch`: 7 files, 13 exclusion additions and one reading fix.
  - Both `correction-families` chunks in full: 19 families, 77 senses.
  - Both `correction-old-bodies` chunks in full: 選ぶ, 選択, 抜く, コレクション, 受ける, 収穫, 直す, 伸ばす, ずるずる, だらだら, 綿.
- The seven changed article bodies in full: 捕える, 取り出す, 採る, 捕る, 治す, 長引く, ナイロン.
- The TSV header and all twenty assigned rows, N2:1222–1241.
- Bounded checks inside `words\`:
  - A search for `quiz_distractors` lines naming any of the changed pairs. There were none.
  - Front matter of ぐずぐず, 直る, 長期 and 長引く, to look for omitted guards.

**Inherited from my initial review (not reread):**
- The twelve unchanged assigned bodies, including the reused 泊める and 長い.
- The five kanji cards 採, 線, 永, 仲 and 泊, and `related.patch`.
- The five reciprocal pairs, the compact derivatives and the public Weblio/Daijisen captures.

The correction patch touches none of these.

**Not read:**
- `corrected-review-evidence.json` (not required, and I didn't read it).
- Any forbidden ledgers, reports, author scripts, or the rationale-bearing `batch-62.json`.
- No live dictionary pages fetched.

## Verdicts
| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1222 | words\泊める.md | Inherited full read (reused; only jlpt:2 added) | CLEAN | CLEAN | CLEAN |
| N2:1223 | words\ともかく.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1224 | words\捕える.md | Full corrected reread, patch, families | CLEAN | CLEAN | CLEAN |
| N2:1225 | words\取り入れる.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1226 | words\取り消す.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1227 | words\取り出す.md | Full corrected reread, patch, families | CLEAN | CLEAN | CLEAN |
| N2:1228 | words\採る.md | Full corrected reread, patch, families | CLEAN | CLEAN | CLEAN |
| N2:1229 | words\捕る.md | Full corrected reread, patch, families | CLEAN | CLEAN | CLEAN |
| N2:1230 | words\トレーニング.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1231 | words\丼.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1232 | words\内科.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1233 | words\内線.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1234 | words\ナイロン.md | Full corrected reread, patch, 綿 families/body | CLEAN | CLEAN | CLEAN |
| N2:1235 | words\治す.md | Full corrected reread, patch, families | CLEAN | CLEAN | CLEAN |
| N2:1236 | words\長い.md | Inherited full read (reused N5; 永 link only) | CLEAN | CLEAN | CLEAN |
| N2:1237 | words\仲直り.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1238 | words\長引く.md | Full corrected reread, patch, families | CLEAN | CLEAN | CLEAN |
| N2:1239 | words\中身.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1240 | words\中身.md | Inherited full read; shared 中味 teaching | CLEAN | CLEAN | CLEAN |
| N2:1241 | words\中指.md | Inherited full read; unchanged | CLEAN | CLEAN | CLEAN |

**Reciprocal pairs: CLEAN (inherited; the patch doesn't touch them).**

| Kanji | Word and reading | Entry ID |
|---|---|---|
| 泊 | 泊める (とめる) | 1474860 |
| 採 | 採る (とる) | 1599160 |
| 線 | 内線 (ないせん) | 1458650 |
| 永 | 永い (ながい) via 長い.md | 1429750 |
| 仲 | 仲直り (なかなおり) | 1426000 |

Each pair has its reading-row example, Common words entry, a substantive word-side link and a footer ID that matches.

**Kanji and baseline preservation: CLEAN.**
- The kanji headers are preserved.
- 泊める gained only `jlpt: 2`. 長い is still N5, with only its existing 永 mention linked.
- No cards were created for the missing 捉, 兎, 穫, 身 or 丼.
- Primary metadata wasn't expanded for variant spellings.
- No baseline quiz exclusions were removed.

**Mappings: CLEAN.** All twenty TSV rows match my initial judgments. Additional senses:

| Article | Additional senses |
|---|---|
| 捕える | 1598960:3 |
| 取り出す | 1326770:2 |
| 採る | 1599160:3–6 |
| 中指 | 1581690:2 |

N2:1236 maps to 長い (level 5, 1429750:2). N2:1239 and N2:1240 both map to 中身 (1599430:1–3).

## Findings
**My original findings**
- **B62-01 (長引く quiz guards): RESOLVED.** `長引く.md:9` now excludes ずるずる and だらだら.
  - Evidence: the full bodies teach 話し合いがずるずる続いた and 会議がだらだら続いた, and the families give 1006440:3 and 1007510:3.
- **B62-02 (cotton reading): RESOLVED.** `ナイロン.md:28` now reads [綿](綿.md) (めん).
  - Evidence: this matches 1533330 and the linked 綿 article. 1533340 (わた, the cotton plant or padding) is still valid and isn't contradicted.

**My optional observations**
- 取り出す vs 選ぶ/採る is now implemented through G01, and I agree with it.
- The extra 永い example in 長い.md is still optional.
- I agree that 中身/物質 and 内科/薬/医学 aren't pairs, and that 採る/入れる can stay.

**Author adjudications**
- **G01 (取り出す / 選ぶ, 選択, 採る): agree.** The title "pick out" competes with "choose", "selection" and "pick". Evidence: 1326770:1 and the Daijisen sense 「多くの中から選び出す」.
- **G02 (採る / 抜く, コレクション): agree.**
  - 1478190:5 (pick out, choose, select, extract) and 1599160:3 (extract a sample) support 抜く.
  - "collect" against "collection; collecting" is a direct title overlap; 1051540:1 is a transitive する noun.
- **G03 (捕える / 受ける; 捕える and 捕る / 収穫): acceptable.**
  - Catching a ball (1329590:2) and a fishing catch or haul (1330510:3) are ordinary secondary senses.
  - Neither older body teaches them, so the titles overlap only weakly. These guards are conservative but harmless.
- **G04 (治す / 直す): agree.** 1599390:4 lists cure/heal with "usu. written as 治す", so the reading and meaning genuinely compete. 治す still teaches only the medical meaning.
- **G05 (長引く / 伸ばす): agree.** "lengthen" against "be prolonged" is real title ambiguity (1600290:2,8). It doesn't erase the transitivity difference.
- **Author-A01 (捕る / 抜く): acceptable, but weakly motivated.**
  - 1478190:11 (seize, capture) has no usage marks, but it is mainly the literary sense of taking a stronghold (城を抜く).
  - 抜く's title "pull out" and its body don't compete with "catch; capture" from 抜く's side.
  - The guard only reduces the pool of wrong answers, so it's harmless and not a regression. I don't count it as a defect.

**Regression check: none found.**
- All thirteen additions are valid inline list entries, with no duplicates or self-references.
- Every target is an actual article in `words\`.
- No `quiz_distractors` line conflicts with them.
- No title, reading, level, kanji or teaching text changed, apart from the cotton reading at line 28.

**New actionable defects:** none.

## Optional
- Add one temporal 永い example to `長い.md`.
- G03's 受ける guard and A01's 抜く guard could be revisited if the wrong-answer pool becomes thin. I'm not asking for either to be removed.
- ぐずぐず ("dawdling; grumbling; unsettled") and 長期 ("long term; long period") don't establish a pair with 長引く, so no guard is needed.

## Limits
- **Unverifiable here:**
  - Git identity, hashes, cleanliness, manifests and lower-level index checks are author-executed; I couldn't run them.
  - I didn't read `corrected-review-evidence.json`.
- **Inherited, not reread:**
  - The twelve unchanged bodies and the five kanji bodies.
  - The pair, footer and mapping checks.
- **Source depth:**
  - All public dictionary support comes from one authority (Digital Daijisen via Weblio), and I did no fresh live lookups.
  - In my initial session I read only a few older bodies in full; I now have the eleven shared corrective bodies, so model-depth comparisons aren't meaningful.
- **Not done:** no live quiz draws, native-speaker certification, measured frequency or exhaustive synonym audit.
