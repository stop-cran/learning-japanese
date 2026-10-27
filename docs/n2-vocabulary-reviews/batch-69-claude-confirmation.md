# Batch 69 correction confirmation review

## Snapshot
- **Revised commit:** 34473aa19eb8c3a6de4410a25b20c5ebfa54fab8.
- **Parent (the snapshot I reviewed originally):** d5066fa715158c8b92eed02438e2c7bb23bf81d5.
- **Committed content only:** the author marks this snapshot as clean committed content. My file tools cannot run Git. The manifest, hash and clean-worktree checks were run by the author, not by me, and I did not confirm independently that the files I read match the commit.

## Scope
- **Model:** claude-opus-5.5 (claude family). Read-only: no edits, shell, agents or delegation.
- **Read completely this turn:**
  - Snapshot and patch: `correction-snapshot.json`, `correction.patch` and `correction-reconciliation.json`.
  - Articles: all 20 current word articles and the four kanji cards 片, 磨, 針 and 省.
  - Source rows: the TSV header plus exactly N2:1362–1381, using an anchored query (21 lines).
  - Mappings and dictionary records: all 20 mappings, 20 principal word families and 35 component records.
  - Correction renderings: all six (38 families, 22 older bodies) and the vigor supplement.
  - Older articles read directly: 活気, ばりばり, 活躍 and 活力.
  - Other: the quiz-exclusion rules in `docs\content-format.md:18-103`, and a bounded search of `docs\confusable-words.md` (it has no rows for these words).
- **Checked by title or exclusion list only:** ぴんぴん, 一生懸命, 夢中, 止める, 諦める, 判断 and 裁判.
- **Omitted:**
  - The optional `corrected-review-evidence.json`, `correction-completed-inspection.json` and `public-bodies.json`.
  - `public-bodies.txt` and `review-labels.jsonl` were read in the original review, not reread.
  - No fresh web fetches this turn.
- **Not read (forbidden):** the ledger, review and manifest files touched by the patch.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1362 | 跳ねる | CLEAN | CLEAN | CLEAN | Added ぴょんぴょん; it is a direct pair ("hop" vs "hopping"). |
| N2:1363 | 破片 | CLEAN | CLEAN | CLEAN | Added 切れ; it is a direct pair (切れ sense 1: "piece; scrap"). |
| N2:1364 | 歯磨き | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1365 | はめる | CLEAN | CLEAN | CLEAN | B69-05 resolved; blank raw spelling preserved. |
| N2:1366 | 早口 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1367 | 流行る | CLEAN | CLEAN | CLEAN | B69-04 resolved. |
| N2:1368 | 払い込む | CLEAN | CLEAN | CLEAN | B69-06 resolved (貯金 and 支払 added). |
| N2:1369 | 払い戻す | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1370 | バランス | CLEAN | CLEAN | CLEAN | Finance wording now matches the dictionary; blank raw spelling preserved. |
| N2:1371 | 針金 | CLEAN | CLEAN | CLEAN | No コード guard ("metal wire" vs "cord"); I accept this. |
| N2:1372 | 張り切る | NEEDS FIX | CLEAN | CLEAN | B69-02 and B69-03 resolved; new B69-07 (活力 missing). |
| N2:1373 | 反映 | CLEAN | CLEAN | CLEAN | B69-01 resolved; the computing sense is scoped and contrasted with 効く. |
| N2:1374 | 半径 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1375 | 判子 | CLEAN | CLEAN | CLEAN | Not excluding 印 is correct: the 印 article is しるし, "mark; sign". |
| N2:1376 | 万歳 | CLEAN | CLEAN | CLEAN | Added 止す; it is a direct pair through the giving-up use. |
| N2:1377 | 判事 | CLEAN | CLEAN | CLEAN | Removing 審判 is not a regression. |
| N2:1378 | 反省 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1379 | 番地 | CLEAN | CLEAN | CLEAN | Kept guards 住居 and 住まい now have positive evidence. |
| N2:1380 | パンツ | CLEAN | CLEAN | CLEAN | Pitch is hedged in the body (lines 43–45); remains a limit. |
| N2:1381 | バンド | CLEAN | CLEAN | CLEAN | Unchanged; blank raw spelling preserved. |

- **Kanji edits:** all CLEAN, and none was touched by the correction patch.

  | Card | Linked reading | Common word | Footer entry |
  |---|---|---|---|
  | 片 | ヘン | 破片 | 1471420 |
  | 磨 | みが.く | 歯磨き | 1601040 |
  | 針 | はり | 針金 | 1366250 |
  | 省 | セイ | 反省 | 1480540 |

  Existing headers and examples are preserved. No missing component cards were invented.
- **Mappings:** CLEAN. The 20 rows map to 20 distinct new identities. Raw fields, spelling restrictions and selected/additional senses are unchanged. The blank spellings for はめる, バランス, パンツ and バンド are preserved.
- **Baseline:** CLEAN. All 20 articles are still new, with the same identities, readings and levels. The patch changes 10 new articles and no older word or kanji cards.

## Findings

**Original findings**
- **B69-01 (反映 title promoting the computing sense): resolved.**
  - The title is now "reflection" (反映.md:4, 12).
  - 効く has been added (:9), and the body (:43-48) keeps "take effect" as a computing use with an explicit contrast to 効く.
  - The 効く guard is justified rather than excessive, because the article still teaches 変更が反映される.
  - A 効果 guard is no longer needed: "effect; effectiveness" is now clearly separate from "reflection".
- **B69-02 (張り切る missing ねっしん / 生き生き): resolved.**
  - ねっしん (dictionary entry 1467910, "enthusiastic; eager") and 生き生き (1609130, "energetically") are both direct pairs.
  - Each extra addition is a direct pair on its own meaning, not an inherited group:

    | Addition | Dictionary evidence | Article title |
    |---|---|---|
    | もりもり | 1012700 senses 2–3, "energetically; welling up" | "heartily; full of vigor" |
    | 盛ん | 1379750 senses 3–4, "energetic; eager" | — |
    | 活気 | 1208270, "energy; vigour" | — |
    | ばりばり | 1010340 sense 4 | "working vigorously" |

  - None of these is an excess.
  - Not adding 活躍 is acceptable (medium confidence): it is about a prominent contribution in a role (活躍.md:15-21), not an eager attitude.
- **B69-03 (unsupported spelling claim): resolved.** 張り切る.md:32 now credits the 張切る spelling to Digital Daijisen's 張（り）切る heading, which matches the captured entry.
- **B69-04 (流行る missing 盛ん): resolved.** Evidence: 1379750 senses 1–2 ("flourishing; popular, widespread") against 1552310 senses 1–3.
- **B69-05 (はめる missing 合う): resolved.** Evidence: 1284430 sense 2 ("to fit") against 1566420 sense 1 ("to fit").
- **B69-06 (払い込む missing 貯金): resolved.** Evidence: 1427170 sense 1 ("deposit (e.g. in a bank)") and 1594480 ("payment") against 1501580 ("to deposit; to pay in").

**Other original items**
- **反映/表す, 表現, 示す and 番地/住居, 住まい ("weakly justified" note): withdrawn.**
  - For 反映: entry 1601160 sense 2, plus Daijisen sense 3 (…現れること／それを現すこと), against 1263490 senses 1–2, 1489510 sense 1 and 1317110 senses 1 and 3.
  - For 番地: 1482360 sense 2 ("address; residence") against 2841455 sense 1 and 1595750 sense 1 ("residence; address").
- **バランス finance wording: resolved.** Lines 43–44 now say "income and expenditure / debits and credits".
- **Borderline pairs from my original limits:**
  - 判子/印: agree no guard. The いん entry 1168050 does not carry over to the しるし article (1168060).
  - 破片/切れ: resolved by the addition.
  - 万歳/応援, 針金/コード and 反映/及ぼす: agree no guard. None of them is an automatic pair.

**Other correction changes**
- 跳ねる/ぴょんぴょん: correct. The ぴょんぴょん body itself uses 跳ねる.
- 万歳/止す: correct. 万歳.md:41-44 teaches the giving-up use; the 止す article (よす, 1310600) is titled "stop doing; give up". It is not the さす entry 2231100, and 諦める.md:9 already excludes 止す.
- 判事/審判 removal: no regression (medium-high confidence). 審判's title and body cover decisions and sports officials, and 判事.md:37-38 draws that contrast.
- Regressions found: none.

**New finding**
- **B69-07 — Low; correctness (quiz metadata); unresolved.**
  - **Location:** 張り切る.md:4, 9; 活力.md:4, 9, 21.
  - **Claim and impact:**
    - 活力's title is "vitality; energy", and its own body glosses 活力にあふれる as "be full of energy". That is exactly 張り切る's title wording.
    - Neither article excludes the other.
    - 活気 ("liveliness; vigor") was added on weaker overlap, so learners can face two defensible answers.
  - **Remedy:** add 活力 to one of the two lists.
  - **Evidence:** dictionary entry 1427870 ("to be full of vigor"). 活力's own dictionary family, 1208480, is not in the permitted renderings, so I judged this from the article.
  - **Confidence:** medium.

## Optional
- 反映.md:23: 水面に夕日が反映する may read more naturally than the current transitive optical example.
- ぴんぴん and 一生懸命 were checked by title only. I did not find a direct pair for either, so I am not proposing them.

## Limits
- Git, the manifest hash and the clean worktree are verified by the author only.
- The public evidence comes from one source (Digital Daijisen via Weblio), and I made no fresh dictionary fetches this turn.
- The optional evidence and inspection JSON files were not read. The 活力 dictionary family was not available.
- パンツ pitch is not verified.
- Ledger and manifest changes in the patch were not reviewed, as instructed.
- These verdicts are not a native-speaker certification.
