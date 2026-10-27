## Snapshot
- **Corrected commit:** `6f731b2640fa2752c6bbbf9f11e62515727eb9d3`.
- **Parent:** `787b93e13814f9f2052f641645fad70e6962007d` (the authored commit).
- **Diff:** four files (the canonical `batch-30.json`, サイレン, 混合 and 献立), confirmed from the patch's `diff --git` headers.
- **Provenance limits:**
  - I have file, search and web tools only, with no Git or hash execution.
  - The clean-state, identity, diff and evidence hashes are author-executed receipts I could not check.
  - I read the working-tree files and found they match the patch hunks; I could not prove they equal the commit.

## Scope
- **Model:** claude-opus-5.5 (claude family), working alone and read-only.
- **Read in full:**
  - my original report, the correction receipt and the whole correction patch;
  - the current `words\混合.md`, `words\献立.md` and `words\サイレン.md`;
  - the comparison cards 計, プラン, 合図, 信号, plus 祭, お祭り, 祭日, こんばんは and 晩 for the declined hypotheses.
- **Evidence derivative:**
  - JMdict 1056150 (サイレン) and 1258500 (献立, sense 2);
  - all of `additionalComparisonEntryFamilies` (1115900, 1252050, 2817380, 1284930, 1359240);
  - all of `correctionEvidence`.
  - The derivative's appended data matches the patch.
- **Collision checks:** I scanned `words\` titles for plan/preparation/arrangement/schedule/program/menu and signal/sign/cue/alarm/warning labels. I then read 打ち合わせ, 設計 and サイン.
- **Web:**
  - Kotobank 計: Daijisen けい【計】 ② はかりごと。計画 (scheme; plan), with a separate はか heading. This independently confirms the 計 receipt.
  - Kotobank 献立: 精選版 日本国語大辞典 ② 物事を行なう順序や、全体の組み立てなどの計画 (a plan of the order or overall structure for doing something). This independently confirms the nonmeal planning sense.
  - Kotobank 混合: only the 世界大百科事典 article came back; it uses 混合物 for the mixed material.
  - Failed or chrome-only: the Weblio 献立 dictCode page, the Daijisen body on Kotobank 献立, and Kotobank サイレン (404).
- **Not done:** this is not a second full twenty-card review. No other report, ledger or the canonical `batch-30.json` was read.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 混合 | CLEAN | CLEAN | CLEAN |
| 献立 | CLEAN | CLEAN | CLEAN |
| サイレン | CLEAN | CLEAN | CLEAN |
| Appended evidence | CLEAN | CLEAN | CLEAN |

**Mapping N2:584** moves from coverage NEEDS FIX to CLEAN. JMdict 1258500 sense 2 is now explained and illustrated. No TSV, kanji or other-card changes appear in the diff.

**Quiz declarations:** Across the 17 guarded new cards I count 7+2+15+5+8+3+3+2+4+3+4+3+1+6+5+3+1 = 75 declarations. That matches the receipt's 75, up from 71 across 16 cards. The headers recorded in `inspectedComparisonLabels` match the actual cards.

## Findings
**B30-C1** (混合 air example; was Minor, correctness): **Resolved.**
- `words\混合.md:19` now reads 空気はいくつかの気体の混合物です (くうきは…こんごうぶつです).
- Line 21 explains that 混合物 names a mixed substance.
- The を/が explanation (line 16) and the 二種類の粉を混合します mixing example remain.
- My original claim was a naturalness preference, not ungrammaticality. I accept the author's wording that impossibility was not established.

**B30-C2** (献立 sense 2; was Minor, scoped coverage): **Resolved.**
- `words\献立.md:21` explains the nonmeal planning/arrangements use. It gives 会議の献立をする (かいぎのこんだてをする), "make arrangements for a meeting", and ties it to JMdict's program/schedule gloss without making 献立 a general word for "program".
- The sense is independently confirmed by 日本国語大辞典 ②.
- 献立をする is grammatical, because 日本国語大辞典 ① also covers the act of drawing up the plan (その予定を立てること).

**New 献立 guards (計, プラン; `words\献立.md:9`): supported, not excessive.**
- Both cards lead with "plan".
- JMdict 1252050:1 "plan" and 1115900:1 "plan; scheme" back them, as does the Daijisen 計 ② I retrieved.
- Each pair is declared directly, not inferred through 計画.

**New サイレン guards (合図, 信号; `words\サイレン.md:9`) and contrast (line 31): supported.**
- The 合図 card admits a sound as a cue, and the 信号 card treats a signal as carrying information. Both overlap with "signaling sound".
- Each pair is declared directly; neither is inferred from the existing 合図→信号 guard.
- The line-31 claim "a siren's sound can serve as either; neither broader word specifies a siren" is accurate, and both links resolve.

**Optional hypotheses:**
- サイレン/合図: **resolved** (adopted, with 信号 added).
- 祭日 vs 祭/お祭り: **withdrawn.** The お祭り card explicitly says it does not mean a public holiday, and I have no evidence of a collision.
- こんばんは vs 晩: **withdrawn.** It is a greeting versus a time noun, and the older おはよう guard sets no rule.
- 混合 が example and 男女混合; 倒 spelling and placing 逆さま in 逆's さか row: **still optional.**

**Regressions:** none actionable.

## Optional
- **Unguarded title overlaps:** the new 献立 wording ("preparation, arrangements") partly overlaps 打ち合わせ "…; advance arrangements", 設計 "design; planning" and 準備/用意/支度 "preparation…". Their leading labels differ, so this is not an established collision. You could watch it, or narrow line 21 to "planning or arrangements".
- **献立 citation label:** line 37 labels the Daijisen link "Meal-planning use", but it now also supports the nonmeal use; relabel it.
- **献立 comparisons:** the Synonyms section could briefly contrast プラン and 計, which are now guarded.
- **サイン:** its trailing "signal" label (`サイン.md:4`) carries only a low risk against サイレン.

## Limits
- I could not run Git or check any hash.
- **Unretrieved by me:**
  - the exact Daijisen wording of 会議の献立をする (the sense itself is independently confirmed);
  - Daijisen's listing of 混合物;
  - the Daijisen サイレン heading;
  - the earlier コンセント, 採点 and 祭日 receipts, which are outside this correction.
- No app quiz draws, measured frequency, native-speaker certification or official JLPT syllabus are claimed.
- Two raw web fetches were saved by the tool to `%TEMP%`; I have no tool to delete them.
