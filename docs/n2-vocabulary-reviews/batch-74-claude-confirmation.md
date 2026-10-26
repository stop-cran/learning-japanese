## Snapshot

- **Revised commit:** c14e72eb3c6ef596210363054f2b7d637b54b67e
- **Parent:** 66364c849c41507a674454aadb1b6cb018595541
- **Content:** committed content only (cleanCommittedContent true).
- **Git limitation:** file tools cannot run Git. The snapshot identity, manifest and hashes, and the preservation checks are the author's results; I did not run them.

## Scope

- **Model:** claude-opus-5.5 (Claude family). No edits, agents, delegation or shell.
- **Fresh complete reads:**
  - Correction snapshot, patch and reconciliation.
  - Both instruction files, and docs\content-format.md lines 18–103.
  - All 20 assigned articles. The six changed ones were reread again before citing.
  - kanji\符.md and kanji\武.md.
  - Mappings (20), principals (20 families/42 senses), components (33) and labels (211).
  - TSV line 1 and lines 1462–1481 only.
  - All four evidence files: 15 families/44 senses, the もぐもぐ supplement, and 20 Daijisen captures.
  - All nine required older bodies.
- **Partial reads:** front matter only for がっかり, 包む, 被る and 暗い.
- **Not read:** the three optional private files, the 423 prepared families and the original 17 comparison renderings. No web fetch was made in this pass.
- **Cumulative coverage:** 22 distinct comparison bodies plus the 20 assigned ones, across both passes.

## Verdicts

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1462 | 符号 | CLEAN | CLEAN | CLEAN | モールス符号 is attested in the frozen Daijisen capture (sense 2) |
| N2:1463 | 夫妻 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1464 | 塞がる | CLEAN | CLEAN | CLEAN | Adds 一杯; kana wording fixed |
| N2:1465 | 塞ぐ | CLEAN | CLEAN | CLEAN | B74-01 resolved |
| N2:1466 | ふざける | CLEAN | CLEAN | CLEAN | Blank source spelling preserved |
| N2:1467 | 無沙汰 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1468 | 武士 | CLEAN | CLEAN | CLEAN | Baseline preserved |
| N2:1469 | 部首 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1470 | 襖 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1471 | 附属 | CLEAN | CLEAN | CLEAN | Shares a family with 付属 |
| N2:1472 | 蓋 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1473 | 不通 | CLEAN | CLEAN | CLEAN | No exclusion against 普通 (homophone only) |
| N2:1474 | ぶつかる | CLEAN | CLEAN | CLEAN | Blank spelling preserved |
| N2:1475 | ぶつける | CLEAN | CLEAN | CLEAN | "nail on" note is accurate |
| N2:1476 | 物騒 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1477 | ぶつぶつ | CLEAN | CLEAN | CLEAN | Four guards added |
| N2:1478 | 船便 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1479 | 部品 | CLEAN | CLEAN | CLEAN | B74-02 resolved |
| N2:1480 | 吹雪 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1481 | 父母 | CLEAN | CLEAN | CLEAN | Unchanged |

- **Kanji 符:** CLEAN. 符号 appears in the meaning text (line 20), the フ reading row (line 30) and the common-word list (line 35). The footer (line 43) lists 1497710.
- **Kanji 武:** CLEAN. 武士 ぶし appears in the ブ reading row (line 28) and the common-word list (line 38). The footer (line 47) lists 1583680.
- **Mappings:** CLEAN. All 20 match the TSV and the principals, and selected and additional senses stay separate.
- **Baseline (武士):** CLEAN. Level, identity, reading, title, body, kanji [武, 士] and the empty exclusions are unchanged.

## Findings

- **B74-01 (塞ぐ/覆う): resolved.** 塞ぐ.md line 9 now excludes 覆う. Lines 16–19 teach "cover", which matches 1602590 sense 1 and 1588840 sense 1. High confidence.
- **B74-02 / G04 (部品/アクセサリー): resolved.** Line 9 adds the exclusion and line 16 explains the gloss. The "accessories" gloss is supported by 1499480 sense 1, and the アクセサリー card covers equipment uses (1015220 sense 2). Keeping the gloss is acceptable.
- **G01 (塞がる/一杯): resolved.**
  - 塞がる.md line 19 translates its example as "My hands are full".
  - The Daijisen ふさがる sense 4 reads 「いっぱいであきがない」.
  - 一杯's title is "full", matching 1165670 sense 3.
- **G02 (塞ぐ/被せる, しょんぼり): accepted.**
  - 被せる rests on 1484320 sense 1 ("to cover") and the lid example in its body. The separate きせる entry (1422990) was not relied on.
  - しょんぼり ("downcast") pairs with 塞ぐ "feel down" through 1005740 sense 1 and 1602590 sense 5.
  - I considered カバー and がっかり and did not establish a pair for either.
- **G03 (ぶつぶつ/ぶくぶく, ぷくぷく): accepted, medium confidence.**
  - ぶつぶつ.md line 27 teaches simmering, and Daijisen senses 3 and 4 explicitly mention bubbles (泡).
  - ぶくぶく matches through 1011140 sense 2, and ぷくぷく through 2699730 sense 1.
  - Each pair stands on its own evidence, not by transitivity through ぐつぐつ.
- **符号 limit: resolved.** Line 18 now uses モールス符号. The 記号［用法］ note was still not retrieved.
- **Optional guards: agreed.**
  - ささやく: Daijisen ぶつぶつ sense 1 「小声でものを言う」 overlaps 1565670 sense 1 ("to whisper, to murmur"). Medium confidence.
  - でこぼこ: "small bumps" overlaps "bumpiness" (1582410 sense 1). Low-to-medium confidence.
- **"Nail on": resolved.** ぶつける.md line 32 is accurate: the raw N2:1475 gloss includes "to nail on", but 2742080 does not.
- **塞がる kana wording: resolved.** Line 16 now matches the "usually kana" flag on 1602570.
- **Regressions:** none. Every new exclusion target exists, nothing was removed, and the kanji cards and 武士 are unchanged.

## Optional

- The semicolon in the 武 reading row (line 28) still runs two linked words together.
- 吹雪's snow compounds and 父母's register remain deferred; neither is a defect.

## Limits

- I verified no Git operations, hashes or runtime quiz behaviour.
- All public evidence comes from one dictionary authority (Digital Daijisen via Weblio), read from frozen captures.
- Example naturalness is not certified by a native speaker, and no frequency claims are established.
- Exclusion omissions were checked only within the bodies and titles I actually read.
