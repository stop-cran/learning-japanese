# Batch 67 N2 vocabulary review (rows N2:1322–N2:1341)

I found no blocking defects. Five rows need small fixes: 吐き気 states the wrong reading type for 気, 挟まる claims an unsourced spelling, パターン is missing a quiz exclusion, and 斜 and はじめに contain notes written for authors rather than learners. The four kanji edits, the twenty mappings and the preserved existing content all check out.

## Snapshot
The frozen commit is `82e2764231c6146414d806551d1db63670d9191a` (parent `6c9d2f5c650e9aa298e539724be17821d0045554`), committed content only. My file tools cannot run Git, so I took the commit and hashes from `frozen-snapshot.json` without checking them myself.

## Scope
**Model:** claude-opus-5.5 (Claude family). No agents, no delegation, no edits.

**Instructions and patch read:**
- `.github\copilot-instructions.md`
- `.github\instructions\content-structure.instructions.md`
- `docs\content-format.md`, lines 18–103
- `related.patch`

**Articles read in full:**
- All 15 new articles.
- The 3 reused articles (計る, はきはき, 挟む).
- The 4 edited kanji cards (量, 測, 掃, 挟).
- For comparison: kanji\計.md, 払う, タイプ, 始め and 初め.

**Private files read:**
- `review-mappings.jsonl` (20 records)
- `review-principals.jsonl` (18 families)
- `review-components.jsonl` (27 records)
- `public-bodies.txt`

**TSV:** the header and rows N2:1322–N2:1341. N2:1340 needed a second search.

**Read only partly:**
- Searches of 気, 生, 外, 歯, 車, 初 and 始.
- Titles and exclusions for about 63 comparison articles.

**External pages I fetched:**
- Kotobank 挟まる: returned the Daijisen and Nikkoku dictionary entries.
- Jisho 挾まる: returned only the 挟む entry, which lists 挾む as an out-of-date kanji spelling.
- Weblio 挾まる: license text only.
- One Kotobank link redirected to an unrelated word.

**Not read:**
- Private files: `review-evidence.json`, `review-labels.jsonl`, `public-bodies.json`, all 11 family-inspection files and all 13 old-body-inspection files.
- Docs: `n2-vocabulary-snapshot.json`, `n2-source-snapshot.json`, `confusable-words.md`, `jlpt-levels.md`.

## Verdicts
| Row | Source → article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|---|
| N2:1322 | 生える → 生える | CLEAN | CLEAN | CLEAN |
| N2:1323 | 剥す → はがす | CLEAN | CLEAN | CLEAN |
| N2:1324 | (blank spelling) ばからしい → ばからしい | CLEAN | CLEAN | CLEAN |
| N2:1325 | 秤 → 秤 | CLEAN | CLEAN | CLEAN |
| N2:1326 | 量る → 計る | CLEAN | CLEAN | CLEAN |
| N2:1327 | 測る → 計る | CLEAN | CLEAN | CLEAN |
| N2:1328 | 吐き気 → 吐き気 | NEEDS FIX (F01) | CLEAN | NEEDS FIX (F01) |
| N2:1329 | はきはき → はきはき | CLEAN | CLEAN | CLEAN |
| N2:1330 | 掃く → 掃く | CLEAN | CLEAN | CLEAN |
| N2:1331 | 歯車 → 歯車 | CLEAN | CLEAN | CLEAN |
| N2:1332 | バケツ → バケツ | CLEAN | CLEAN | CLEAN |
| N2:1333 | 挟まる → 挟まる | NEEDS FIX (F02, F04) | CLEAN | CLEAN |
| N2:1334 | 挟む → 挟む | NEEDS FIX (F04, shared quiz pair) | CLEAN | CLEAN |
| N2:1335 | 梯子 → はしご | CLEAN | CLEAN | CLEAN |
| N2:1336 | 始めに → はじめに | CLEAN | CLEAN | NEEDS FIX (F05) |
| N2:1337 | 初めに → はじめに | CLEAN | CLEAN | NEEDS FIX (F05) |
| N2:1338 | はじめまして → はじめまして | CLEAN | CLEAN | CLEAN |
| N2:1339 | 斜 (はす) → 斜 | CLEAN | CLEAN | NEEDS FIX (F05) |
| N2:1340 | 外れる → 外れる | CLEAN | CLEAN | CLEAN |
| N2:1341 | パターン → パターン | NEEDS FIX (F03) | CLEAN | CLEAN |

For N2:1336 and N2:1337 (はじめに), correctness rests on the JMdict family and the repo's 2014 spelling guidance cited in 始め.md. No Daijisen text was captured for はじめに.

**Kanji edits — CLEAN.**
- 量 and 測: the はか.る reading rows and Common words now link to `words\計る.md`, and the footers include 1600650.
- 掃: the は.く row links 掃く (footer includes 1399760).
- 挟: the はさ.まる row links 挟まる (footer includes 1236840), and the existing 挟む link is kept.
- Front-matter headers are unchanged.
- The word articles link back to their kanji: 計る→量/測 (with an explanatory sentence), 掃く→掃 and 挟まる→挟.

**Existing content preserved — CLEAN.** 計る keeps jlpt 3, its identity and its title; only the kanji links were added. はきはき and 挟む only gained jlpt 2, plus the 挟まる link in 挟む. No unchanged passage is presented as new.

**Mappings — CLEAN.** All 20 mappings match the TSV and resolve to 18 articles. The additional senses match the source records.

## Findings
**B67-F01 — Minor; reading type; `words\吐き気.md:28-30`**
- **Claim:** 気 is "read け here", and "This is a native reading pattern, not an all-on compound."
- **Why it's wrong:** け is an on reading of 気, specifically the older Go-on reading. The 気 component record (KANJIDIC2) lists ケ as an on reading, and the repo's own `kanji\気.md` (lines 29 and 33) calls ケ a Go-on reading. So 吐き気 is a mixed word: native 吐き plus on-reading け.
- **Fix:** Say that 吐き is native and け is the Go-on reading of 気, as in 寒気 (さむけ). Also reconsider the `type: wago` setting.
- **Confidence:** High.

**B67-F02 — Low; spelling; `words\挟まる.md:29`**
- **Claim:** "挾まる is another recognized spelling."
- **Why it's a problem:** No source supports it.
  - JMdict entry 1236840, which the article cites, lists only 挟まる.
  - Kotobank's Daijisen heading is 【挟まる】 and Nikkoku's is 【挟】.
  - 挾 is the older form of 挟; Jisho marks 挾む as out-of-date.
- **Fix:** Delete the sentence, or label 挾 as an older character form and cite a source.
- **Confidence:** Medium.

**B67-F03 — Minor; quiz exclusions; `words\パターン.md:9`**
- **Problem:** タイプ is not excluded, although the titles "pattern; type; …" and "type or style" overlap in both quiz directions. Daijisen's first sense of パターン is 型・類型 ("type"). Neither article excludes the other.
- **Fix:** Add タイプ. 種類 ("kind; variety") is also arguable, because the article's own example translates パターン as "types."
- **Confidence:** High for タイプ, medium for 種類.

**B67-F04 — Low; quiz exclusions; `words\挟まる.md:9`**
- **Problem:** 挟む and 挟まる do not exclude each other.
  - 挟む ("hold between; pinch") has a sense meaning to catch a finger in a door. In English that is usually "got caught", which overlaps 挟まる's title.
  - `docs\content-format.md` uses the similar pair 開く/開ける as its example of a pair needing an exclusion.
  - This batch already excludes 外れる/外す.
- **Fix:** Add 挟む to 挟まる's exclusions. Exclusions are symmetric, so one side is enough.
- **Confidence:** Medium.

**B67-F05 — Low; learner readability; `words\斜.md:42-43`, `words\はじめに.md:31, 46-47`**
- **Problem:** Notes aimed at authors appear in learner text ("The source row has no English gloss…", "Do not silently replace…", "without creating duplicate identities", "the blank gloss on one row…"). Learners never see the source rows.
  - JMdict entry 2085880 lists both はす and しゃ as readings of 斜 with the same sense ("diagonal"). So telling learners not to "replace" はす with しゃ is confusing.
- **Fix:** Rewrite these lines for learners, or delete them.
- **Note:** Similar wording appears in about 100 other word articles, so this looks like a repo-wide habit.
- **Confidence:** Medium.

## Optional
- `words\はしご.md:23` calls はしごする transitive, but JMdict marks it both transitive and intransitive. "Often takes を for the places visited" would be more accurate.
- `words\はがす.md:27`: the phrase "the source list's 剥す" could be reworded for learners.
- `kanji\計.md:33,40`: 計る is not linked yet (this predates the batch). Linking it would match the new 量 and 測 links.
- Optional links: 生える in 生.md:34, 外れる in 外.md:32, and 当たる in 外れる.
- 吐き気 could add the collocation 吐き気を催す and the figurative "disgust" use.
- はきはき could add Daijisen sense 2 (clear thinking).
- 掃く and 磨く may overlap on "brush" (low confidence).

## Limits
- All the dictionary text the author captured comes from one source, Digital Daijisen via Weblio. No dictionary text was captured for はじめに.
- I didn't read the files listed under Scope as not read. I read the full articles of only five comparison words; for the rest I saw only titles and exclusions. Exclusions may still be missing elsewhere.
- I couldn't fully settle the 挾まる question in F02: Weblio returned no content.
- I didn't recheck whether 容器 and コップ exist as articles.
- Naturalness of the examples is not certified by a native speaker.
