# B114 confirmation — run N1-B114-CLAUDE-CONFIRM-001

```text
Snapshot: ac38b8e4427afc2c10a957871c5ec99e9cb92bda (revision of reviewed freeze 8c2bdc27e5d556e639a4d0e9239ae5f2009c400f). Reviewer model: the runtime declares Claude Opus 5.5 (claude-opus-5.5); I cannot independently verify the execution model.
Scope: B114 Claude confirmation chain, segments 1-27, each read once in order, no re-views. No web_fetch.
Dispositions: one line per ID in RESPONSE.md (see table below)
Verdicts:
  correctness: CLEAN
  scoped coverage: CLEAN
  consistency and quiz safety: CLEAN
  comprehensibility: CLEAN
Confirmation: CONFIRMED
Findings: none
Optional: see below
Limits: see below
```

## Scope

I read every chain segment in full. What each segment contained:

| Segments | Contents |
| --- | --- |
| 1 | confirm-packet/INSTRUCTIONS.md; start of initial-report/initial-claude.md |
| 2 | rest of initial-claude.md |
| 3 | RESPONSE.md |
| 4 | CHANGES.md; diffs/fix.patch |
| 5 | diffs/changed-lines.txt; diffs/changed-files.txt; revised 娯, 寮, 廊 |
| 6 | revised 栓, 汽, 症, 砲 |
| 7 | revised 碁, 磁, 穀 |
| 8 | revised 穫, 糖, 紺, 雰 |
| 9 | revised 魅; original-packet repo/kanji 房, 庁 |
| 10 | 部, 課, 集, 拾, 利 |
| 11 | 績, 怪, 穂, 盤 |
| 12 | 板, 気; checks budget, link-targets.tsv, lint, manifest, quiz-safety |
| 13–14 | checks/reading-exposure.txt |
| 14–15 | checks/reading-options.txt |
| 15 | checks unittest, validate |
| 16 | checks/vocabulary; evidence/README.md, jmdict-cited-entries.xml, QuizBuilder.kt; start of rubric/copilot-instructions.md |
| 17–18 | rest of rubric/copilot-instructions.md |
| 19 | rubric/content-structure.instructions.md |
| 20 | repo/docs/content-format.md lines 1-139; start of evidence/kanjidic2-records.xml |
| 21–23 | rest of kanjidic2-records.xml |
| 23–26 | evidence/jmdict-families.xml |
| 26–27 | evidence/title-index.txt, lines 1-1221 (line 1 "一 one", line 1221 "齢 age; years lived") |

- All six changed cards (寮, 症, 碁, 穀, 穫, 魅) were read in full and checked against fix.patch.
- The nine unchanged cards were read in full. Their text matches what I reviewed initially, and CHANGES.md says no other line changed.
- web_fetch: none used.

## Dispositions

| ID | Disposition | Reason and evidence |
| --- | --- | --- |
| F1 | RESOLVED | 穀.md:14 now reads `[米, 麦, 稲, 穂, 種, 粒, 実]`. The 穀.md:68-70 note keeps "not a synonym for all grain" and now says the pair is excluded. 穂 (title "grain-bearing head") does not list 穀 among its distractors (積 想 息), and 穀's distractors (殿 投 段) do not overlap 穂. |
| F2 | RESOLVED | 碁.md:14 now reads `[盤]`. The new bullet at 碁.md:59-62 is accurate: JMdict 1270890 碁盤 is "Go board", and JMdict 1482420 盤 sense 1 is "board (in shogi, go, chess, etc.)". "board/disc" matches 盤's title "board; disc". The bullet does not contradict 碁.md:65-67: the exclusion rests on the game's own equipment plus the shared displayed word, not on a shared topic. 盤's distractors (船 番 晩) and 碁's (目 日 田) do not overlap. |
| F3 | RESOLVED | 寮.md:14 now includes 房. 寮.md:62-64 names 房 in the room clause. JMdict 2222290 房 ("chamber; room", "home of a monk") supports the overlap. 房's distractors (戻 防 忙) do not include 寮. |
| O1 | DECLINE ACCEPTED | 板 is now distinguished in the text (碁.md:62) without the equipment link that 盤 has. 行 "go" is the movement verb, which 碁.md:65-66 already separates. Both are label-only overlaps; my initial report called leaving them a defensible choice. |
| O2 | RESOLVED | 寮.md:14 now includes 庁. 寮.md:65-66 names it with the bureau set. 庁's distractors (打 店 床) do not include 寮. |
| O3 | RESOLVED | 穫.md:14 now includes 集 and 拾. 穫.md:58-61 lists them under gathering. Their link titles match: 集 "gather", 拾 "pick up; gather". |
| O4 | DECLINE ACCEPTED | No change, as I recommended. The over-exclusions only shrink fallback pools and are disclosed on the cards. |
| O5 | DECLINE ACCEPTED (deferral) | 気.md is outside the batch, unchanged, and recorded for a later fix. I had already said it was not a B114 defect. |
| O6 | DECLINE ACCEPTED | The Metadata lines record word families that were consulted. That is provenance, not a teaching claim. |
| O7 | RESOLVED | 症.md:50 now reads `重症 じゅうしょう - serious illness`, matching JMdict 1336310 exactly. |

## Regression check of the changed hunks

All three changes that did not answer one of my points are acceptable. Each is a conservative, accurately described direct pair; none is also listed as a distractor on either card.

- **寮 + 部, 課** (寮.md:14, 66-67). JMdict 1554230 sense 2 is archaic: "bureau (government department beneath a ministry under the ritsuryō system)". The labels "section; department" and "lesson; organizational division" plausibly overlap "department/division". The sentence describing this is accurate. The pair is a conservative over-exclusion, because the displayed title does not show the bureau sense, but it is harmless. Neither 部 (都 立 問) nor 課 (果 菓 諸) lists 寮 as a distractor.
- **穫 + 利, 績** (穫.md:14, 62-66). JMdict 1330510 sense 2 is "fruits; gain; result; returns". The text frames these as compound-context comparisons for 収穫, consistent with the existing 得/果/実 handling. 利 lists 私 秋 列 as distractors and 績 lists 積 責 緑; neither lists 穫. 利 shares the distractor 秋 with 穫, but that is not a conflict.
- **魅 + 怪** (魅.md:14, 60-61, 63). 怪's own card describes uncanny beings (怪物, 妖怪). The phrase "suspicious/uncanny" matches its title "suspicious; uncanny". "These comparisons" correctly now covers three cards. 怪's distractors (性 経 忙) do not include 魅.

Other checks on the changed hunks:
- **Links.** link-targets.tsv shows 25 links on changed lines, all resolving. Every descriptive phrase I checked matches the real title (盤, 板 "plank" as a partial title, 怪). The other links have no quoted gloss.
- **Front matter.** It is unchanged apart from `quiz_exclusions`. No exclusion overlaps the card's own `distractors`, as content-format.md requires.
- **Readings, meanings, metadata and titles.** All unchanged.

Facets:
- Correctness: every new claim matches JMdict, the counterpart cards or the title index.
- Scoped coverage: unchanged and adequate.
- Comprehensibility: the new bullets are short and plain.

## Quiz options, mechanics and audits

**Meaning options.** checks/quiz-safety.txt has the same SHA-256 as the original packet's copy (59fcd874…). All 15 cards still get three curated wrong options that are not defensible as correct:
- 娯: 誤 妹 妙
- 寮: 察 寧 案
- 廊: 庭 床 府
- 栓: 全 松 村
- 汽: 河 池 海
- 症: 正 政 床
- 砲: 包 砂 硬
- 碁: 目 日 田
- 磁: 硬 研 砂
- 穀: 殿 投 段
- 穫: 程 秋 科
- 糖: 米 数 類
- 紺: 紅 給 結
- 雰: 分 雪 晴
- 魅: 未 妹 末

None of the new exclusion targets is a curated option of its batch card.

**Builder mechanics.** In evidence/QuizBuilder.kt:
- `excluded` (line 26) is symmetric: a pair declared on either card excludes both directions.
- `tryAdd` (lines 28-32) rejects a candidate that is excluded against the target or against an option already chosen. It is applied to curated and fallback candidates alike (lines 34-36).

So declaring each new pair only on the batch card's side is sufficient, and exclusions are not transitive.

**Reading prompts.**
- checks/reading-options.txt: every curated or fallback wrong reading that shares the target's key is skipped, and every prompt keeps at least three wrong options over 100 seeds ("0 problem(s)").
- checks/reading-exposure.txt is byte-identical to the original's reading-exposure-final.txt: 0 production hits, 0 padded hits, 1 latent collision (碁 き).

**What these audits cannot show.**
- The new pairs only take effect when fallback is consulted. In the modelled N1/All pools, the curated options fill all three slots, so the audits never exercise the new pairs. Custom or caller-built pools, multi-borrow Starter, and pools missing curated cards are not modelled.
- QuizBuilder.kt is a supplied static copy. Nothing here establishes that it matches the deployed build, and no Kotlin, JVM, emulator or phone execution occurred.
- Installed APK 5c000bd predates quiz_exclusions and ignores every pair, old and new.
- The two reading audits use different scopes for "unlisted" readings:
  - reading-options.txt counts only KANJIDIC2 name readings (砲 づつ, 穀 たけ).
  - reading-exposure.txt also includes card-text Daijisen readings (娯 たのしむ, 寮 つかさ, 碁 き, 糖 あめ, 穀 たなつもの).
  - So reading-options' "none" for 碁 does not cover the latent き case; only reading-exposure shows it.

## Optional

- 穀.md:69, "Like the rice plant, its displayed grain wording is close enough…": 稲's displayed title "rice plant" has no *grain* wording, and 稲 is excluded for overlapping crop meaning, not for its label. The comparison could mislead slightly. A clearer wording would be "Its displayed grain wording is close enough that the pair is excluded from choices, as 稲 is for the crop meaning." This is polish, not a defect.
- The 寮 (部, 課) and 穫 (利, 績) additions protect senses the displayed titles do not show. They are acceptable, but continuing to add compound-context labels steadily shrinks fallback pools. Future batches may want to reserve this for senses that are displayed or ordinary.

## Limits

- **L1, L2.** Stroke files, the raw SVGs, the Joyo PDF and other original-packet assets were not in this chain, and I did not re-read them. The author says they are unchanged; I have only that claim and the hashes of the checks. There is still no visual glyph or geometry verification.
- **L3.** Reading audits are host Python models of limited pools. I have no Kotlin or native evidence, no custom or multi-borrow Starter model, and no 5c000bd compatibility evidence. The bounds above apply.
- **L4.** The Daijisen-only statements remain UNVERIFIED. No web_fetch was used, and none of them changed: 娯 たのしむ; 寮 temple-monk accommodation; 碁 キ; 糖 あめ; 砲 baseball sense; 穀 beans and たなつもの; 紺 purplish cast; 雰 氛; 魅 monster sense (which the new 怪 rationale relies on); 栓をする.
- **L5.** No new candidate cards were added. 銃, 霧, 獲, 棋 and 陶 still have no card in the 1221-line index. 空, 風, 愛, 恋, 耕, 産, 爆, 黒, 緑, 盆 and 皿 remain unread as cards.
- **L6.** The checks are static evidence:
  - lint 0/0; validate 0 errors; unittest 431 OK; vocabulary 2122/2431.
  - manifest regenerated at version c78ebbacf53520b6 (8664 files).
  - budget within limits.
  - quiz-safety and reading-exposure byte-identical to the original packet.
  - reading-options and link-targets: 0 problems.
  - The manifest.json content itself was not supplied, and I did not verify it.
- **Initial-report correction.** My initial report cited front-matter `quiz_exclusions` at line 15 of the cards. The patch hunks (`@@ -11,7 +11,7 @@`) show it is line 14. The citations were off by one; the substance is unaffected.
- **No independent hash check.** I hashed nothing; I relied on the coordinator's pre-verification of the chain inputs.
