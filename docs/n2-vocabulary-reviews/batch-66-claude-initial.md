# Batch 66 review: N2:1302–N2:1321

## Snapshot
- **Frozen commit:** `7359a791ab051c71c555a1931bfbaeea7ab07578`. Its parent is `7c56c36ac8ebd74f1e76ae486e05920be683de57` and the file reports `cleanCommittedContent: true`.
- **Committed content only:** the file tools I had cannot run Git. I took the commit, the parent and the clean state from `frozen-snapshot.json` and could not confirm them myself. The author's hash and equivalence checks were not re-run.

## Scope
**Model:** claude-opus-5.5, claude family. Review was read-only, with no agents or edits.

**Read completely:**
- **Instructions:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md:18-103`.
- **Source table:** the TSV header and exactly the 20 assigned rows (1302–1321).
- **Private packet files:** `related.patch`, `review-mappings.jsonl` (20 records), `review-principals.jsonl` (20 complete dictionary families), `review-components.jsonl` (31 records), `review-labels.jsonl` (165 labels), `public-bodies.txt` and `lookup-public-bodies.txt`.
- **Word articles:** all 15 new articles, and the 5 reused ones for their claimed source coverage.
- **Kanji cards:** `kanji\延.md`, `換.md`, `灰.md`, `鈍.md` and the unchanged `伸.md`.
- **Older articles read in full for quiz comparisons:** 全然, さっぱり, 接続, 移す, 送別, スタンド, では, じゃあ.

**Read partially:**
- `review-evidence.json`, lines 1–60 and 3448–3700.
- Two families from the inspection chunks: さっぱり (1005210, chunk 01) and 全然 (1395620, chunk 06).
- Titles and quiz exclusions in `words\` (front matter only, found by search).

**Not read:** the other family-inspection chunks, all thirteen older-article chunks, both supplement files and `lookup-public-bodies.json`. I made no web fetches and did not run the validator. No forbidden files were opened.

**Withdrawn:** I had suspected 残らず wrongly excludes 全然 and さっぱり. Both are justified: 全然 sense 2 means "wholly; entirely; completely" and さっぱり sense 4 means "completely; entirely".

## Verdicts
Each row gives correctness / scoped coverage / comprehensibility.

| Row | Article | Verdicts |
|---|---|---|
| N2:1302 のこぎり | のこぎり | CLEAN / CLEAN / CLEAN |
| N2:1303 残らず | 残らず | CLEAN / CLEAN / CLEAN |
| N2:1304 載せる | 乗せる (claimed 載せる teaching at lines 33–35 only) | CLEAN / CLEAN / CLEAN |
| N2:1305 覗く | 覗く | CLEAN / CLEAN / CLEAN |
| N2:1306 延ばす | 伸ばす (lines 33–35) | CLEAN / CLEAN / CLEAN |
| N2:1307 延びる | 伸びる (lines 38–44; restricted sense 8 taught under the 延びる spelling) | CLEAN / CLEAN / CLEAN |
| N2:1308 上り | 上り | CLEAN / CLEAN / CLEAN |
| N2:1309 上る | 登る (lines 44–45, plus the 昇る/上る natural-rising passage) | CLEAN / CLEAN / CLEAN |
| N2:1310 糊 | 糊 | CLEAN / CLEAN / CLEAN |
| N2:1311 乗換 | 乗り換え | NEEDS FIX (Q1) / CLEAN / CLEAN |
| N2:1312 載る | 載る (a separate dictionary entry from 乗る) | CLEAN / CLEAN / CLEAN |
| N2:1313 鈍い のろい | のろい (the raw にぶい gloss is correctly sent to 鈍い) | CLEAN / CLEAN / CLEAN |
| N2:1314 のろのろ | のろのろ (only `jlpt: 2` added) | CLEAN / CLEAN / CLEAN |
| N2:1315 呑気 | のんき | CLEAN / CLEAN / CLEAN |
| N2:1316 灰色 | 灰色 | CLEAN / CLEAN / CLEAN |
| N2:1317 俳句 | 俳句 | CLEAN / CLEAN / CLEAN |
| N2:1318 売店 | 売店 | CLEAN / CLEAN / CLEAN |
| N2:1319 バイバイ | バイバイ (blank raw spelling and gloss preserved; anchored on sense 1) | NEEDS FIX (Q2) / CLEAN / CLEAN |
| N2:1320 売買 | 売買 | CLEAN / CLEAN / CLEAN |
| N2:1321 這う | 這う | NEEDS FIX (Q3) / CLEAN / CLEAN |

**Kanji edits:**
- **延 — CLEAN on all three.** Both the Readings and Common words entries for 延びる and 延ばす reach `伸びる.md` and `伸ばす.md`. The word side links back to 延 (伸びる:38, 伸ばす:33). The footer has entries 1358870 and 1600290.
- **換 — CLEAN on all three.** 乗り換え のりかえ appears in the -か.える row and in Common words. The word links back (乗り換え:25) and the footer has 1600460.
- **灰 — CLEAN on all three.** 灰色 はいいろ appears in the はい row and in Common words. The word links back (灰色:24) and the footer has 1201970.
- **鈍 — CLEAN on all three.** のろい appears in Common words and Notes. There is no invented のろ reading row, and 鈍 is not added to のろい's `kanji: []`. のろい links back at line 25 and the footer has 2838553.
- **伸 (unchanged):** it links reciprocally to both 伸びる and 伸ばす.

**Baseline preservation — CLEAN.** The kanji headers are unchanged. 乗せる, 伸ばす and 伸びる stay jlpt 3 and 登る stays jlpt 5, with their primary metadata intact. The 乗せる and 登る bodies were not re-reviewed.

**All 20 mappings — CLEAN.**

## Findings
**B66-Q1** — Minor; quiz exclusions; `words\乗り換え.md:4,9,16`. Confidence: moderate.
- **Problem:** 接続 ("connection; joining") and 移す ("move; transfer") are not excluded. A learner could reasonably accept either title for 乗り換え.
- **Evidence:**
  - Dictionary entry 1600460 sense 1 for 乗り換え reads "transfer (trains, buses, etc.); change; connection".
  - The 乗り換え body at line 16 calls it "a transfer or connection".
  - `接続.md:23` teaches the same transport connection, and 接続 already excludes the verb 乗り換える.
- **Fix:** add 接続 and 移す to 乗り換え's exclusions.

**B66-Q2** — Low; quiz exclusions; `words\バイバイ.md:9`. Confidence: moderate-low.
- **Problem:** バイバイ excludes では but not じゃあ. Both have the identical title "well then", so the では exclusion does not keep that answer off バイバイ's quiz.
- **Evidence:** `じゃあ.md:32` teaches じゃあね as a casual sign-off ("See you, then"), the same register as バイバイ. `では.md:15,19` teaches the farewell use.
- **Fix:** add じゃあ to バイバイ's exclusions, or drop では.

**B66-Q3** — Low; quiz exclusions (excess); `words\這う.md:9,31`. Confidence: moderate.
- **Problem:** the 伸びる exclusion is not supported. 伸びる's title is "grow longer; stretch; improve" and 這う's is "crawl; creep"; neither fits the other word in either direction. 這う's own text at line 31 says 伸びる is not a replacement.
- **Note:** 広がる can stay; 這う sense 3 includes "to spread".
- **Fix:** remove 伸びる from 這う's exclusions.

## Optional
- **上り.md:16:** the phrase "or central terminus" is not in either source. Digital Daijisen says 終点から起点への方向 (from the terminus toward the starting point), and dictionary sense 2 says "toward the starting point of its route".
- **Missing examples:** 乗せる could show 載せる for objects (棚に荷物を載せる). 登る could show 階段を上る. 伸びる could show postponement (出発が延びる) and 日が延びる.
- **Titles:** のこぎり could read "saw (tool)" to avoid confusion with the past tense of "see". 乗り換え could add transport context.
- **Weak exclusion:** 覗く's 見物 exclusion has only topic proximity behind it.
- **Possible extra exclusions for editor judgment:** 載る with 刷る or 印刷, 残らず with 全般, バイバイ with 送別, 上り with 昇る, and のんき with ゆっくり or 楽.

## Limits
- I could not run Git, the validator or the hash checks myself.
- All public evidence is Digital Daijisen via Weblio, captured by the author. That is one authority, not fresh independent retrievals. The raw 乗換 capture failed; the separate 乗り換え capture succeeded.
- For most possible missing exclusions I checked titles only, not full older articles. Most inspection and older-article chunks were not read, so not finding a problem there does not prove absence.
- These are editorial judgments, not native-speaker certification.
