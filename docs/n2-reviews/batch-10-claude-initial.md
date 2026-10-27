## Snapshot
Frozen commit `013263037da18cd9f5f25e199685493011f94df5`, committed files only. I can't run Git, so the commit, the clean worktree and the 57-file scope are taken from the author's statement and were not verified.

## Scope
Reviewer: claude-opus-5.5 (Claude family). I worked sequentially, read-only, with no delegation.

- **Read in full:** 15 kanji cards (普 暴 曇 替 札 机 材 村 板 林 枚 枝 枯 柔 柱) and 4 word articles (暴れる, 枚, 枯れる, 柱).
- **Related edits, narrow scope:** the component-link passage in each of the 17 listed word articles, and `kanji\木.md` distractors (人, 水, 米) against "tree, wood".
- **Comparison pages:** titles of all distractor cards, plus selected words, tags and exclusions.
- **Guidance and evidence:**
  - The three assigned guidance files.
  - `docs\n2-batch-sources\batch-10.json`, read in full.
  - `docs\n2-source-snapshot.json`: all 15 kanji are in planned batch 10, line 23.
  - Jisho API and Kotobank fetches.
- **Omitted:** the forbidden ledgers and reports; unchanged teaching text in the 17 related articles; stroke drawing paths (only `strokeCount` was checked); the validator and manifest tooling.

## Verdicts
| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| kanji\普.md | CLEAN | CLEAN | CLEAN |
| kanji\暴.md | CLEAN | CLEAN | CLEAN |
| kanji\曇.md | CLEAN | CLEAN | CLEAN |
| kanji\替.md | CLEAN | CLEAN | CLEAN |
| kanji\札.md | CLEAN | CLEAN | CLEAN |
| kanji\机.md | CLEAN | CLEAN | CLEAN |
| kanji\材.md | CLEAN | CLEAN | CLEAN |
| kanji\村.md | CLEAN | CLEAN | CLEAN |
| kanji\板.md | NEEDS FIX | CLEAN | CLEAN |
| kanji\林.md | CLEAN | CLEAN | CLEAN |
| kanji\枚.md | CLEAN | CLEAN | CLEAN |
| kanji\枝.md | CLEAN | CLEAN | CLEAN |
| kanji\枯.md | CLEAN | CLEAN | CLEAN |
| kanji\柔.md | CLEAN | CLEAN | CLEAN |
| kanji\柱.md | CLEAN | CLEAN | CLEAN |
| words\暴れる.md | CLEAN | CLEAN | CLEAN |
| words\枚.md | CLEAN | CLEAN | CLEAN |
| words\枯れる.md | CLEAN | CLEAN | CLEAN |
| words\柱.md | CLEAN | CLEAN | CLEAN |

**Checked and found correct:**
- All 15 cards match the source record for strokes, radical and number, grade tag, onyomi and kunyomi. Every stroke file's `strokeCount` matches its card.
- All 40 reading rows are backed by retained JMdict pairs. The あまねし source-only qualification is honest; Jisho returns no あまねし entry.
- All 45 distractors exist, are semantically wrong options and are three per card. 米 activates no ambiguity on 木.
- All 17 related link passages are accurate in context.

## Findings
**B10-板-01 — Minor — Correctness (homograph)**
- **Location:** `kanji\板.md:28` and `kanji\板.md:39-40`.
- **Claim:** The only ハン example is 板木 はんぎ, and line 40 tells learners to "learn … ハン in 板木". But the same spelling 板木 is also a separate word read ばんぎ, a wooden board struck as a signal. Japanese dictionaries head 板木 with the reading バンギ.
- **Impact:** The example chosen to isolate ハン actually carries a competing バン reading. A learner may misread 板木 or overgeneralize.
- **Minimal remedy:** Add a homograph note, for example: "The same spelling also names 板木 ばんぎ, a wooden board struck as a signal; read 板木 from context." Reword line 40 so it doesn't imply 板木 is always ハン. Keep the ハン row; no deletion is needed.
- **Evidence:**
  - Pinned `batch-10.json:2008-2056` retains only entry 1626140 (版木/板木 はんぎ). Its priority flags are on the reading, and 版木 is listed first.
  - Jisho API for 板木 returns a separate JMdict entry 板木 ばんぎ, "wooden board struck with a mallet as a signal".
  - Kotobank 板木: heading "板木（読み）バンギ"; 精選版日本国語大辞典 "ばん‐ぎ【板木・盤木・番木】"; 世界大百科事典 gives both 板木 (はんぎ) and 板木 (ばんぎ).
- **Confidence:** Medium-high. The ばんぎ entry wasn't confirmed inside the pinned JMdict download.

## Optional
These are nonblocking.
- 枝: mention 枝葉 えだは for literal foliage. Jisho lists えだは and しよう, with sense 2 "esp. しよう".
- Possible extra examples: 人材 for 材, 千円札 for 札, 電柱 for 柱. For 替, link 両替 or 取り替える.
- Low-risk word-quiz overlaps you may want to exclude:
  - 激しい ("violent") with 暴れる.
  - 台, 骨, 棒 or 基 ("support", "pole", "foundation") with 柱.

## Limits
- I couldn't run Git, so the snapshot and clean state are unverified.
- Stroke drawing paths weren't reviewed. The validator and manifest checks weren't run.
- The full reading list for 枝葉 isn't retained in the pinned evidence; the えだは reading comes from the live Jisho lookup.
- Two Kotobank lookups failed (an unrelated page and an empty search). They are not evidence either way.
- Natural-sounding examples aren't certified by a native speaker, and priority flags weren't treated as frequency evidence.
