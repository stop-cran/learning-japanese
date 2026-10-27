## Snapshot
Frozen commit: **1e39beb7f4a0f18f01f4851698fb346ea443f6c6** (parent f3c0ec4d7cda9b6f1948d7989b15221cb90d12b1). I reviewed committed content only. File tools can't run Git, so I read working-tree files and relied on the author's `cleanCommittedContent` claim. I did not rerun the author's hash or equivalence checks.

## Scope
**Model:** claude-opus-5.5 (claude family). Read-only; one tool call at a time; no agents or edits.

**Read completely:**
- frozen-snapshot.json; the three instruction docs (content-format.md lines 18–103)
- All 20 assigned articles, `kanji\順.md` and related.patch
- Mappings 1–20, principals 1–20 (34 senses), components 1–28 and labels 1–316
- supplemental-comparisons.json, extra-comparisons.json and public-bodies.txt (through EOF)
- The TSV header (line 1) and rows 1602–1621 only
- `words\伸ばす.md`

**Read partially:**
- Grep lines from 復習, 人込み, 見出し, 満員, 回り道, 道順, 見つかる, 見つける and 見直す
- Titles of 18 comparison articles
- `kanji\付.md` lines 1–12
- Globs of `kanji\` and `words\` for existence checks

**Web:** kotobank 見直す (Daijisen and Nikkoku) was usable. Weblio 持ち直す gave no definition and kotobank 持ち直す returned 404, so neither counts as verification.

**Not read:** review-evidence.json, family-inspection-01 to 13, old-body-inspection-01 to 23, related-kanji-inspection-01, public-bodies.json, and the supplemental/extra comparison-reading .txt files.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1602 | マラソン | CLEAN | CLEAN | CLEAN | 42.195 km and extended uses supported |
| N2:1603 | まれ | CLEAN | CLEAN | CLEAN | Recognizes 稀 and links 希; no 稀 card exists |
| N2:1604 | 回り道 | NEEDS FIX | CLEAN | CLEAN | F3: no guard against 道順 |
| N2:1605 | 満員 | NEEDS FIX | CLEAN | CLEAN | F2: no guard against 人込み |
| N2:1606 | マンション | CLEAN | CLEAN | CLEAN | 11 guards are defensible |
| N2:1607 | 満点 | CLEAN | CLEAN | CLEAN | Extra sense (栄養満点) supported |
| N2:1608 | 見送る | CLEAN | CLEAN | CLEAN | Senses 1–6 split correctly; 伸ばす guard justified because 伸ばす's body teaches 延ばす "postpone" |
| N2:1609 | 見下ろす | CLEAN | CLEAN | CLEAN | Contempt sense supported by Daijisen |
| N2:1610 | 見かけ | CLEAN | CLEAN | CLEAN | Recognizes 見掛け; "apparent" sense rests on JMdict only (disclosed) |
| N2:1611 | 三日月 | CLEAN | CLEAN | CLEAN | Novel title (unrelated heading) correctly excluded |
| N2:1612 | 岬 | CLEAN | CLEAN | CLEAN | No 岬 or 崎 card exists; kanji metadata kept |
| N2:1613 | みじめ | CLEAN | CLEAN | CLEAN | Raw "(arch)" flag rightly not adopted |
| N2:1614 | ミシン | CLEAN | CLEAN | CLEAN | Daijisen gives the "sewing machine" origin |
| N2:1615 | 店屋 | CLEAN | CLEAN | CLEAN | Separate てんや heading kept apart |
| N2:1616 | 見出し | CLEAN | CLEAN | CLEAN | 説明 guard is borderline but grounded in "caption" |
| N2:1617 | 道順 | NEEDS FIX | CLEAN | CLEAN | F3 (same pair); reciprocal link to 順 present |
| N2:1618 | 見つかる | CLEAN | CLEAN | CLEAN | Additions only; 見付かる correctly called a rare spelling |
| N2:1619 | 見つける | CLEAN | CLEAN | CLEAN | Additions only; sense 2 uses Daijisen's attested phrase |
| N2:1620 | みっともない | CLEAN | CLEAN | CLEAN | Comparison with 見苦しい is reasonable |
| N2:1621 | 見直す | NEEDS FIX | CLEAN | CLEAN | F1 (invented example), F4 (no 復習 guard) |

**Separate assessments:**
- **Kanji 順 and baseline preservation — CLEAN.** The 順 card's metadata and teaching are unchanged; only the 道順 rows and entry 1611770 were added. 見つかる and 見つける keep their word, reading, title, N4 level and all old teaching.
- **Components — CLEAN.** No missing links to existing cards: 稀, 崎, 惨 and 岬 have no cards, and no links were invented. 付 (N3) is unlinked in the reuse spelling notes; see Optional.
- **Reciprocal links — CLEAN.** 道順 and 順 link to each other.
- **Mappings — CLEAN.** All 20 rows match their TSV entry IDs and selected senses. The raw spellings 稀, 見掛け, 見付かる and 見付ける are each explicitly recognized in their articles.

## Findings
**F1 — Minor; correctness**
- **Where:** `words\見直す.md:25` (also :27, and guards on line 9)
- **Problem:** The intransitive "recover" use is illustrated with 景気が見直す, which the author made up. It is presented as normal usage with no dated or literary label.
- **Evidence:** Daijisen sense 3's only example is from Tōson's 夜明け前 (稲穂もよほど見直した). Nikkoku's intransitive sense gives examples from 1527 and 1900. Neither shows 景気が見直す.
- **Impact:** Learners may produce dated phrasing.
- **Fix:** Mark the use as dated or literary, and either use the attested example or describe the sense without a made-up phrase. Point to 回復, which the article already links.
- **Confidence:** Medium.

**F2 — Low; quiz guard (correctness)**
- **Where:** `words\満員.md:9`; `words\人込み.md:9`
- **Problem:** No guard between 満員 ("full of people; at capacity") and 人込み ("crowd of people").
- **Evidence:** 満員 already guards 混雑 and 込む, yet 人込み has the closest overlapping title.
- **Fix:** Add the 満員/人込み pair.
- **Confidence:** Medium-low.

**F3 — Low; quiz guard (correctness)**
- **Where:** `words\回り道.md:9`; `words\道順.md:9`
- **Problem:** No guard between "detour; roundabout route" and "route; directions".
- **Evidence:** 道順.md:27 itself justifies guarding コース because it overlaps on "route", and both articles guard コース. The same reasoning applies to this pair.
- **Fix:** Add the 回り道/道順 pair.
- **Confidence:** Medium-low.

**F4 — Minor; quiz guard (correctness)**
- **Where:** `words\見直す.md:9`; `words\復習.md` (it has no quiz_exclusions)
- **Problem:** No guard between "look again; review; think better of" and "study review".
- **Evidence:** 見直す.md:35 contrasts the two directly, and 批評 ("critique; review") is already guarded.
- **Fix:** Add the 見直す/復習 pair.
- **Confidence:** Medium-high.

## Optional
- In 見直す, the 進歩 and 伸びる guards depend only on the dated "recover" sense, and line 39 says skill improvement isn't 見直す. Consider dropping them once F1 is fixed.
- 見直す's title "think better of" can be read in English as "decide against". "Think better of (someone)" would be clearer.
- Link 付 in the 見付かる and 見付ける spelling notes.
- Note in 見つける that sense 2 is uncommon in modern speech.
- Add Daijisen's usage note contrasting みっともない and 見苦しい.
- The 満点/結構 and マンション/部屋 guards are weak but harmless.

## Limits
- I didn't read the old-body or family-inspection files. Guards involving words whose articles I didn't read were judged from labels only, which are not full-body evidence.
- I couldn't confirm that modern Japanese uses 持ち直す rather than 見直す for an economy recovering.
- Hashes, Git state and native-speaker naturalness were not independently verified.
