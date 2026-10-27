## Snapshot
- **Revised commit:** dd61b410bb42ab827708111fcf9fd0a347f927ce
- **Parent:** 77ffbe55d56c925eba2343f9be59b9dcb2daf843
- I reviewed committed content only. My file tools cannot run Git, so the snapshot, hash, byte-preservation and equivalence claims are the author's checks, not mine.

## Scope
- **Model:** claude-opus-5.5 (family claude). No edits, agents, delegation or shell were used.
- **Snapshot, patch and reconciliation:** I read the correction snapshot first, then the full correction patch and the reconciliation file.
- **Guidance:** I freshly read both guidance files in full and `docs\content-format.md` lines 18–103.
- **Assigned articles:** I freshly reread all 19 completely, including the unchanged ones.
- **Source data, read fresh and complete:**
  - mappings 1–10 and 11–20;
  - principals 1–10 and 11–19 (19 families, 35 senses), plus rereads of lines 4 and 17;
  - components 1–18;
  - labels 1–100 and 101–188.
- **TSV:** the header `[1,1]` and exactly rows `[1482,1501]`.
- **Evidence files, read completely:**
  - the correction comparison file (10 families, 32 senses);
  - the 次第 supplement (1316680, 6 senses, including noun sense 4 "order; program");
  - `public-bodies.txt` (20 captures from one Daijisen/Weblio source).
- **Older bodies, read completely:** ソフト, 包み, 包む, 浮く, 浮かぶ, 接する. I also read 軽い to check for a possible quiz ambiguity.
- **Totals this pass:** 26 complete word bodies.
- **Not read:** the three optional private files (corrected-review-evidence.json, completed-inspection.json, public-bodies.json) and the other prepared families.
- **No new web fetch this pass.** Two items carry over from the initial pass: the Kotobank 刷子 retrieval, and my readings of the ごちそう and 次第 bodies.
- I cannot read the other reviewer's report. Shared or unique attributions below rely on the reconciliation file, not my own comparison.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1482 | 踏切 | CLEAN | CLEAN | CLEAN | Unchanged. All four senses are covered. |
| N2:1483 | 麓 | CLEAN | CLEAN | CLEAN | Unchanged. Uses the ふもと heading, not ろく. |
| N2:1484 | 増やす | CLEAN | CLEAN | CLEAN | F1 fixed at lines 21 and 26. |
| N2:1485 | 増やす | CLEAN | CLEAN | CLEAN | 殖やす is taught separately and described as a spelling tendency (lines 30–35). |
| N2:1486 | フライパン | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1487 | ブラウス | CLEAN | CLEAN | CLEAN | Now says to use 着る (line 17). |
| N2:1488 | ぶらさげる | CLEAN | CLEAN | CLEAN | Kana form kept as the headword; ぶら下げる is the dictionary spelling (line 27). |
| N2:1489 | ブラシ | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1490 | プラスチック | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1491 | プラットホーム | CLEAN | CLEAN | CLEAN | Lines 31–32 clarify the railway ホーム vs the home loanword. フォーム variant still taught. |
| N2:1492 | フリー | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1493 | 振り仮名 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1494 | プリント | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1495 | 振舞う | CLEAN | CLEAN | CLEAN | Source spelling kept. 接する guard added. |
| N2:1496 | ブローチ | CLEAN | CLEAN | CLEAN | Notes the separate broach (cutting-tool) homograph (lines 37–39). |
| N2:1497 | プログラム | CLEAN | CLEAN | CLEAN | Unchanged. 次第 sense 4 supports the existing guard. |
| N2:1498 | 風呂敷 | CLEAN | CLEAN | CLEAN | Teaches the whole reading ふろしき (lines 44–46). Guards are now 布 and 生地. |
| N2:1499 | ふわふわ | CLEAN | CLEAN | CLEAN | Three guards added, as the source_note permits. |
| N2:1500 | 噴火 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1501 | 分解 | CLEAN | CLEAN | CLEAN | Unchanged. |

**Mappings:** all twenty are correct.
- Readings, entries and selected senses are unchanged. 1484 and 1485 both map to entry 1602880, sense 1.
- Blank source spellings and the source spelling 振舞う are kept.
- Only the current TSV source_notes for 1498 and 1499 changed; both match the articles.

**Component links:** unchanged and correct.
- Existing cards 増, 舞, 風 and the others are linked.
- Missing cards (振, 呂, 敷 and others) stay as plain text or metadata.

**New N2 pairs:** none required, and no kanji card was edited.

**Baseline preservation (ふわふわ):** according to the patch, the only line changed is line 9 (exclusions).
- Title, reading, type, kanji, tags, image, image_scene and body are unchanged.
- The three new exclusions deliberately override the original "only add jlpt" scope, and the 1499 source_note now allows this.
- Byte identity is the author's claim.

## Findings
- **F1 – resolved.** `増やす.md:21,26` now shows 十人に as the resulting total, beside 二人 as the amount added. The example is natural.
- **F2 / GPT-01 (shared) – resolved.** `ふわふわ.md:9` now excludes ソフト.
  - Evidence: 1075500 sense 1 glosses exactly "soft" (adjectival noun), and 1113060 sense 2 glosses "soft; fluffy; spongy" (also adjectival).
  - The "gentle/mild" wording comes only from the ソフト article body (`ソフト.md:15`), as the author says.
  - This omission predates the jlpt addition.
- **Tentative guard ふわふわ/浮く – adopted, and I agree.**
  - 1497420 sense 1 is "to float"; 浮く's title is plain "float" (`浮く.md:4`).
  - ふわふわ's title "floating lightly" matches 1113060 sense 1, so a learner could defensibly pick 浮く.
- **Follow-through guard ふわふわ/浮かぶ – I agree, as an independent judgement.**
  - 1497430 sense 1 is "to float, to be suspended", and the 浮かぶ title is "float; come to mind".
  - It is justified directly by these senses, not inherited through 浮く.
  - This was the author's addition, not my finding.
- **Tentative guard 振舞う/接する – adopted, and I agree.**
  - 接する's title includes "treat people" (`接する.md:4`), and 1385350 sense 2 includes "act towards; deal with".
  - That overlaps 振舞う sense 1 "act" and the English "treat" in its title. For example, 親切に接する and 丁寧に振る舞う are close.
  - This does not claim the two verbs are freely interchangeable.
- **GPT-02 (removing the 風呂敷 guards with 包み and 包む) – I agree with the removal.**
  - 1515340 (包み) has only "bundle; package; parcel" and a counter sense; it has no cloth or wrapper sense.
  - 1584060 (包む) has only verb senses. The different-reading entries ぐるみ (1985490) and くるむ (2831360) are not these articles.
  - Daijisen calls the bundle 風呂敷包み, not 風呂敷.
  - The distinction is still taught in the body (`風呂敷.md:37–40`), and the 布 and 生地 guards remain.
  - Confidence: medium. A residual concern is under Limits.
- **Five wording options – resolved (these were optional).** ぶら下げる, the broach homograph, ふろしき without claiming historical primacy, 着る, and ホーム.
- **Deferred expansions – remain optional.** No prerequisite gap: 振舞う already shows a manner adverb with に at line 24.
- **Regressions:** none found.
- **Remaining actionable defects:** none.

## Optional
These are the deferred items from my original review, all nonblocking:
- the 踏切り and 踏み切り spellings;
- らしく and ように manner patterns for 振舞う;
- フリガナ;
- 歯ブラシ;
- 大風呂敷;
- a ぶら下がる contrast;
- the プログラムする verb use.

## Limits
- **Unverified totals:** I did not recount the "80 declarations on 18 new cards" figure. Hash and preservation claims are the author's checks.
- **Residual GPT-02 risk:** 包む's bare-verb title "wrap; bundle" could be read as the English noun "a wrap". I judge this low risk because the repository consistently uses bare-verb titles, so it is not actionable.
- **軽い:** considered and not flagged. "Light in weight" is a different meaning from ふわふわ's sense 1 "lightly (floating)".
- **Coverage:** I did not read the other prepared families.
- **Public evidence:** comes from a single dictionary (Daijisen) and was not re-fetched in this pass.
- **No guarantees:** this is not exhaustive correctness, native-speaker certification, frequency evidence, or a guarantee of runtime quiz behaviour.
