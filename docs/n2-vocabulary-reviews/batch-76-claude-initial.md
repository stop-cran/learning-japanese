## Snapshot
**c1563f9c47fa9af139ef149893b4c5e4e9be3317**, parent 4047358f535321e7e4373a408258586cd7cd4e43. This review covers committed content only. My file tools cannot run Git, so I did not check this commit, its hashes or the patch pre-images myself. Those checks were run by the author.

## Scope
**Model:** claude-opus-5.5 (Claude family).

**What I read completely:**
- **Guidance:** `frozen-snapshot.json`, the three guidance files, and `content-format.md:18-103`.
- **Source table:** the TSV header (line 1) and rows 1502–1521 only.
- **JSONL files, in bounded ranges:**
  - 20 of 20 mappings.
  - 20 principal families (36 senses).
  - 31 of 31 component records.
  - All 248 labels. I used the labels to find titles, not as full-article reads.
- **Supplement:** all 8 families (18 senses). I kept the readings of 軍 (ぐん/いくさ) and 武士 (ぶし/もののふ) separate.
- **Public dictionary text:** `public-bodies.txt` through the end of the file. All of it comes from one source, Digital Daijisen via Weblio.
- **Articles and kanji:** `related.patch`, all 20 assigned articles, and the 5 kanji pages (芸, 布, 量, 並, 兵).
- **Older articles read in full:** 文学, 仕舞い, 別.
- **Other checks:** title and front-matter searches in `words\`, and a check of which kanji cards exist in `kanji\`.

**Not read:** `review-evidence.json`, `public-bodies.json`, family-inspection 01–08, old-body-inspection 01–15, related-kanji-inspection-01, the other 401 prepared families, `confusable-words.md`, `jlpt-levels.md`, and both snapshot JSONs in `docs\`.

**One process slip:** I read the TSV header and rows at the same time before I noticed the "read serially" rule. Every read after that was one at a time.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1502 | 文芸 | CLEAN | CLEAN | NEEDS FIX | F3 |
| N2:1503 | 文献 | NEEDS FIX | CLEAN | CLEAN | F4: quiz exclusion missing |
| N2:1504 | 噴水 | CLEAN | CLEAN | NEEDS FIX | F1: title |
| N2:1505 | 分数 | CLEAN | CLEAN | CLEAN | |
| N2:1506 | 文体 | CLEAN | CLEAN | CLEAN | |
| N2:1507 | 分布 | CLEAN | CLEAN | CLEAN | The hedge about someone spreading things is backed by Daijisen sense 1; see Optional |
| N2:1508 | 文房具 | CLEAN | CLEAN | CLEAN | |
| N2:1509 | 文脈 | CLEAN | CLEAN | CLEAN | |
| N2:1510 | 分量 | CLEAN | CLEAN | CLEAN | The transitive sense 2 is confirmed and taught as recognition only |
| N2:1511 | 分類 | CLEAN | CLEAN | CLEAN | |
| N2:1512 | 閉会 | NEEDS FIX | CLEAN | CLEAN | F5 |
| N2:1513 | 平気 | CLEAN | CLEAN | CLEAN | Excluding 良い is justified by its sense 4, "all right" |
| N2:1514 | 並行 | CLEAN | CLEAN | CLEAN | I could not confirm the 平行 dictionary ID (2835826) |
| N2:1515 | 平日 | CLEAN | CLEAN | CLEAN | The ひらび sense is correctly left out |
| N2:1516 | 兵隊 | CLEAN | CLEAN | CLEAN | Not excluding 武士 is defensible: "soldier" belongs to the もののふ reading only |
| N2:1517 | 平凡 | CLEAN | CLEAN | CLEAN | |
| N2:1518 | 平野 | CLEAN | CLEAN | CLEAN | |
| N2:1519 | 凹む | CLEAN | CLEAN | CLEAN | The filename is kept; I could not confirm the くぼむ ID (1246840) |
| N2:1520 | 臍 | CLEAN | CLEAN | CLEAN | The filename and the へそ reading are kept |
| N2:1521 | 隔てる | CLEAN | NEEDS FIX | NEEDS FIX | F2 |

**The other four checks (each is CLEAN for correctness, coverage and comprehensibility):**
- **Five kanji pages and their unchanged text — CLEAN.** Each patch adds exactly one word line and its dictionary ID in the footer: 芸 +1505290, 布 +1504160, 量 +1504430, 並 +1508480, 兵 +1506590. The metadata and the visible surrounding text are unchanged. I could not compare against the original files byte for byte.
- **Component links — CLEAN.** Each article links only kanji that have cards. 献, 噴, 房, 脈, 隊, 凡, 凹, 臍 and 隔 have no cards and are left as plain text. Every `kanji:` list includes all of the word's kanji.
- **Reciprocal N2 links — CLEAN.** All five pairs link in both directions: 文芸/芸, 分布/布, 分量/量, 並行/並, 兵隊/兵.
- **Mappings — CLEAN.** All 20 match the TSV rows and the selected senses. The extra 分量 sense 2 is presented as recognition only.

## Findings
**B76-F1** — minor — comprehensibility
- **Where:** `噴水.md:4,12`
- **Problem:** The title "water fountain" usually means a *drinking* fountain in US and Canadian English. The article body itself says 噴水 is not that (lines 16–17 and 36–39), and quizzes show only the title.
- **Fix:** Change the title to something like "fountain (water jet)".
- **Evidence:** Wiktionary lists "water fountain" (US/Canada) as a drinking-water dispenser, citing Lexico. Daijisen defines 噴水 as a device that shoots water up.
- **Confidence:** medium.

**B76-F2** — minor — coverage and comprehensibility
- **Where:** `隔てる.md:18-21`
- **Problem:** Line 18 says only that "an intervening distance can be the を phrase". But in example 1 (川が二つの町を隔てる), を marks the *things being separated*. That role is never explained.
- **Fix:** Teach both patterns: barrier/cause が + separated things を; or the thing, distance or time in between を隔てて.
- **Evidence:** Daijisen: 「疑心暗鬼が二人を隔てた」, 「障子を隔てて話す」, 「五メートル隔ててくいを打つ」.
- **Confidence:** medium-high.

**B76-F3** — minor — comprehensibility
- **Where:** `文芸.md:33-34`
- **Problem:** "Not every occurrence of 文芸 specifically means stage entertainment" implies that some uses do. Neither dictionary source supports that.
- **Fix:** Rephrase as "芸能 often concerns performance; 文芸 does not specifically denote it."
- **Evidence:** Daijisen gives only 文学 and 文学とその他の芸術. JMdict gives "literature" and "the arts".
- **Confidence:** medium.

**B76-F4** — minor — correctness (quiz exclusions)
- **Where:** `文献.md:9`
- **Problem:** 文学 (title "literature") is not excluded. "Literature" is 文献's first JMdict gloss, and the article itself says this English sense applies (lines 43–44). So either word could be a correct answer in both quiz directions.
- **Fix:** Add 文学 to `quiz_exclusions`. The guard works both ways.
- **Evidence:** JMdict 1505330, sense 1: "literature; books (reference); document". `文学.md:4`.
- **Confidence:** medium.

**B76-F5** — minor — correctness (quiz exclusions)
- **Where:** `閉会.md:9`
- **Problem:** 終わる ("end; finish") is excluded, but 仕舞い has the same title, "end; finish". Its article uses it for ending an activity: 今日の練習はこれで仕舞いです. So the same English answer can still appear as a choice.
- **Fix:** Add 仕舞い.
- **Evidence:** `仕舞い.md:4,18`; `終わる.md` has the identical title.
- **Confidence:** medium-low.

## Optional
- **分布:** Replace the hedge about someone spreading things (lines 39–41) with plain guidance. The title "across an area" is narrower than the statistical use the body teaches.
- **分量:** Line 43 says 量が多い; 分量が多い was probably meant.
- **隔てる:** Line 42 mentions the gloss "be shut out", which is not in the source. Consider adding the で pattern: ついたてで部屋を隔てる.
- **並行:** Lines 35–36 contain author-facing wording ("Do not invent an absolute rule"). The 並 kanji card says "proceeding side by side", while the word title says "moving side by side".
- **Kanji cards:** The 布 card could note the ぷ reading in 分布.
- **Other articles:** 文体 could mention です・ます調. 分類 could add an example where に marks the resulting group. 閉会 could consider excluding 閉める and 閉まる.

## Limits
- I could not run Git, so I did not check the snapshot hash, the patch pre-images or the author's hash results myself.
- I could not confirm the JMdict IDs 2835826 and 1246840: the EDRDG lookup needs a password.
- Merriam-Webster (403) and Cambridge (520) failed to load. The F1 English-usage evidence is Wiktionary only.
- All the public dictionary text comes from one source.
- My search for missing quiz exclusions used targeted title searches, not every older article or all 429 prepared families.
- My judgments of whether examples sound natural are not a native-speaker certification.
