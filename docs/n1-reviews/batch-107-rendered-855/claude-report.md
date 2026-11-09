# Batch 107 native/rendered follow-up review: 勘 at snapshot 1d341ac

I read every required file and viewed all 38 native screenshots; none were skipped or denied. I found no defect introduced by this batch. The 定 and 違 reading gaps and the 支払う/支払 pair stay unresolved; they predate the batch and don't block it.

**Snapshot:** I did three serial reads of the git metadata. `.git` points to the `auditor-compatibility-isolated` worktree, whose HEAD is `refs/heads/n1/resume-after-106-476f429`, and that ref contains `1d341ac022bb652ac38a6c39a589bce5cc51261f`. This only shows the ref points to that commit; the signature check is the coordinator's, not mine.

**Model:** Claude Opus 5.5 (`claude-opus-5.5`).

**Scope:** independent continuation of my batch-107 review. I didn't read any other reviewer's report or any ledger.

## What I read

All reads were serial, one per response, and none was denied or visibly truncated.

**Text files**
- My own `followup-850\confirmation-claude.md`.
- In `batch-107-native-853`:
  - `common-task.txt`
  - `common-rendered-packet.txt`
  - `comparison-cards-01.txt`, `-02.txt` and `-03.txt` (48 comparison cards)
  - `sampled-kanjidic2.xml` (database version 2026-306)
  - `sampled-jmdict.xml`
- Full text files were read with `forceReadLargeFiles` and no range.

**Images**
- All 38 PNGs, one view call each:

  | Group | Screenshots |
  |---|---|
  | All-pool quiz | 5 |
  | Article viewports | 6 |
  | Curated reading quiz | 3 |
  | Drawing | 3 |
  | Font panels | 8 |
  | N1 quiz | 3 |
  | Word-page components | 3 |
  | New 定 and 違 lines | 2 |
  | Word pages | 5 |

- **None omitted.**
- The other 27 screenshots were never opened. The manifest maps them as duplicates of the representatives above (for example, article-03 and -04 map to article-02), so their equivalence is the manifest's claim, not something I checked.
- The images came through at roughly 900×2000 instead of the original 1080×2400. Fine stroke detail and exact stroke-number positions are therefore checked only approximately.

**Previous rounds:** I re-read my 0b6be1de report this round but not my original `initial-claude.md`; what I say about the earlier rounds comes from those two reports.

## Verdicts

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji/勘 | CLEAN | CLEAN | CLEAN |
| words/勘 | CLEAN | CLEAN | CLEAN |
| words/勘定 | CLEAN | CLEAN | CLEAN |
| words/勘違い | CLEAN | CLEAN | CLEAN |
| kanji/定: new 勘定 line | CLEAN | CLEAN | CLEAN |
| kanji/定: whole reading table | — | **NEEDS FIX**, but not caused by this batch and not blocking | — |
| kanji/違: new 勘違い line | CLEAN | CLEAN | CLEAN |
| kanji/違: whole reading table | — | **NEEDS FIX**, but not caused by this batch and not blocking | — |

## Rendered evidence

**Quiz options**
- In the N1 pool, the meaning options were 刑 "criminal punishment", 剤 "medicinal preparation; chemical agent" and 剛 "sturdy; unyielding strength".
- In the All pool, they were 勤 "employment; diligence", 助 "help; rescue" and 期 "period; term".
- None of these labels overlaps "intuition; hunch".
- The All-pool reading options were カン, ジョ, ゴ and ゴン. The curated reading options were カン, ケン, ハン and ジュン. All are distinct.

**Single on'yomi:** because 勘 has only the reading カン, the curated reading session ends after one question ("1 of 1 answers correct").

**Distractors**
- I found no meaning overlap among the 46 distractors or the sampled options, using KANJIDIC2 and JMdict 1210590 (勘: "perception, intuition, sixth sense").
- 期 has a secondary JMdict sense, "opportunity/chance" (1220540), which isn't close to "intuition".
- **勘/識 remains an unguarded hypothesis only (low confidence).**
  - 識 is labelled "knowledge; awareness", which is close to 勘's "perception" but not the same meaning.
  - 識 is not among 勘's exclusions, and it appeared in none of the 64 sampled quizzes.
  - This doesn't justify adding an exclusion.

**Articles**
- The kanji/勘 viewports render the header, the "modern-shape mnemonic" with its "not a verified historical account" qualification, the reading table, Common words, the 勤/助/期 look-alike notes and the 勘える "recognition only" note with its sources.
- The "Typical words" column is clipped at the right edge, but a "Scroll sideways" hint is shown, and article-07 shows the full cell after scrolling. Not a defect.
- The three word pages render their examples with readings, the "how the kanji combine" explanation, the synonym/antonym contrasts and the dictionary citations.

**Drawing**
- The trace shows 11 strokes in the usual order: 甚 in nine strokes (horizontal, two verticals, two inner horizontals, long horizontal, ノ, inner ㇄, outer ㇗), then 力 in two.
- The screens say grading is by stroke shape only because the handwriting model wasn't available ("downloading…" during the trace). The injected trace is not evidence of handwriting recognition.

**Fonts**
- All glyphs render in all four families (Gothic, Mincho, Textbook, Brush), with no missing-glyph boxes.
- The look-alikes 勘, 勤, 助 and 期 can be told apart at this resolution.
- 宀, 辵, 辶 and 韋 visibly fall back to a heavier face in Textbook, and seemingly in Mincho and Brush too. The style doesn't match, but they stay legible. Not blocking.
- The line breaks inside 勘違い happen only on the test panel, not in the app's article layout.

**Stack state:** Drawing shows "1 new" in the N1 stack but is locked in the All stack. That matches the "each stack keeps its own review schedule" text and isn't a content issue.

## Prior findings

| Item | Status |
|---|---|
| 勘/感覚 | **Resolved** by the guard |
| 勘定/支払う, 給与, 払う, 代金 and 料金 guards | **Intact**; these are conservative quiz safeguards, not claims that the words are synonyms |
| Earlier optional suggestions (甚 shape label, 期's 其 look-alike, 定/違 reading-row additions, 勘弁/割り勘, splitting bullets) | **Optional** |
| 定: no row for さだ.か (rendered table shows テイ, ジョウ, さだ.める and さだ.まる) | **Unresolved**; predates this batch, not blocking |
| 違: no rows for ちが.える, -ちが.える, たが.う or たが.える | **Unresolved**; predates this batch, not blocking |
| 支払う/支払 | **Unresolved**; predates this batch, not blocking |

On 違:
- The table says it "selects useful readings", but the app still offers たが.う as a quiz answer without explaining it.
- The authoring rule asks for a row for every kun reading. The validator only enforces that for N5/N4 cards and for explicitly curated readings.

## Findings

No new actionable defect from this batch. The 定/違 rows above are the only remaining remedy, outside this batch. Severity: minor. Facet: coverage. Confidence: high.

Optional, outside this batch: on kanji/定, 予定 is glossed "plan; schedule" in the table but "plan; arrangement" under Common words.

## Limits

- This was an emulator (sdk_gphone64, Android 15), not a physical phone.
- The screenshots were downscaled, so stroke detail was checked only approximately.
- The 64 quiz samples and test results were supplied by the packet; I didn't run them.
- The dictionary excerpts were supplied, not fetched fresh.
- I don't claim native-speaker, physical-phone, merged-tree, publication or global semantic acceptance.