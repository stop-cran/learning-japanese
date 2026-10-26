I found two Minor issues. The other 17 rows have no actionable defect within what I read, and I made no edits. The file tools can't run Git, so hashes and patch-to-commit equivalence were not independently checked.

## Snapshot
Frozen commit **77ffbe55d56c925eba2343f9be59b9dcb2daf843** (parent b5684c408f12489418a9bb3c4626b6067e7015b8). I reviewed committed content only, as recorded in the frozen receipt.

## Scope
**Model:** claude-opus-5.5 (claude family). I read serially, with no agents and no edits.

**Read completely:**
- frozen-snapshot.json and related.patch.
- The four JSONL files in the required ranges: mappings 20, principals 19, components 18, labels 188.
- supplement-comparison-reading.txt: 次第, entry 1316680. Its senses 1–3 are suffix uses; senses 4–6 are ordinary nouns.
- public-bodies.txt through the end of the file. For mixed pages I used only the applicable heading:
  - 麓: ふもと, not the kanji heading ろく.
  - 風呂敷: ふろしき, not ふるしき.
  - ブローチ: the brooch heading, not "broach".
  - ふわふわ: not the egg-soup noun.
- The three guidance files, and docs\content-format.md lines 18–103.
- The TSV header and rows 1482–1501.
- All 19 assigned articles.
- Full comparison articles: ごちそう, ソフト, 浮く, 次第.

**Read partially (front matter, opening lines or grep only):** 増減, 激増, 増大, 増加, 増す, 拡大, 拡張, 付ける, 加わる, スタート, 風呂, 仮名, 作法, 振る, 態度, 接する, 行儀, 行動, 動作, 真似, 扱う, 冊子, 番組, 順序, 柔らかい, 軟らかい, うきうき.

**Kanji cards:** I checked existence and levels with glob/grep in kanji\.

**Web fetches:**
- Kotobank 刷子: Daijisen has さっし【刷子】 "はけ。ブラシ。", and Nikkoku has the same.
- Weblio 刷子 returned a Wikipedia mirror, which is only partial support.
- Weblio さっし had no 刷子 heading, so it does not verify anything.

**Not read:** review-evidence.json, public-bodies.json, family-inspection-01 to 13, old-body-inspection-01 to 15. So I did not inspect the 315 prepared families or the 123 older bodies.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1482 | 踏切 | CLEAN | CLEAN | CLEAN | JMdict senses 1–4 plus the Daijisen takeoff use. The 決心/決定 guards are supported by Daijisen sense 3 (ふんぎり). |
| N2:1483 | 麓 | CLEAN | CLEAN | CLEAN | ふもと heading; ロク is noted; 梺 is search-only. |
| N2:1484 | 増やす | CLEAN | NEEDS FIX | CLEAN | F1 |
| N2:1485 | 殖やす→増やす | CLEAN | CLEAN | CLEAN | Shares the 増やす page. The rare-kanji flag and Daijisen's asset/living-thing tendency are correctly kept as a tendency. F1 is tracked on row 1484's mapping. |
| N2:1486 | フライパン | CLEAN | CLEAN | CLEAN | — |
| N2:1487 | ブラウス | CLEAN | CLEAN | CLEAN | Daijisen defines it as an 上着, which supports the guard. |
| N2:1488 | ぶらさげる | CLEAN | CLEAN | CLEAN | Kana headword kept. ぶら下げる is taught and 下 is linked. |
| N2:1489 | ブラシ | CLEAN | CLEAN | CLEAN | 刷子/さっし verified (Kotobank Daijisen). Electrical brush matches Daijisen sense 2. |
| N2:1490 | プラスチック | CLEAN | CLEAN | CLEAN | — |
| N2:1491 | プラットホーム | CLEAN | CLEAN | CLEAN | Stage, computing and business uses match Daijisen senses 1, 5 and 7. |
| N2:1492 | フリー | CLEAN | CLEAN | CLEAN | Suffix use matches Daijisen sense 4. |
| N2:1493 | 振り仮名 | CLEAN | CLEAN | CLEAN | "Usually ふりがな" matches the JMdict usually-kana flag. The contraction note is consistent with 仮名.md, which cites Kotobank. |
| N2:1494 | プリント | CLEAN | CLEAN | CLEAN | Photo and textile uses match Daijisen senses 3–4. |
| N2:1495 | 振舞う | CLEAN | CLEAN | CLEAN | Source 振舞う kept; examples use 振る舞う. The に recipient / を refreshment pattern is correct. |
| N2:1496 | ブローチ | CLEAN | CLEAN | CLEAN | — |
| N2:1497 | プログラム | CLEAN | CLEAN | CLEAN | The 次第 guard rests on noun sense 4 (次第.md:23); the ソフト guard on software. |
| N2:1498 | 風呂敷 | CLEAN | CLEAN | CLEAN | wago type is consistent with 風呂. |
| N2:1499 | ふわふわ | NEEDS FIX | CLEAN | CLEAN | F2 (an existing quiz-guard gap, not caused by this patch). |
| N2:1500 | 噴火 | CLEAN | CLEAN | CLEAN | Intransitive use with が. |
| N2:1501 | 分解 | CLEAN | CLEAN | CLEAN | Both transitive and intransitive uses match Daijisen sense 1. |

**Separate assessments:**
- **Reused header (ふわふわ):** CLEAN. The patch has one hunk that adds only `jlpt: 2`. Word, reading, title, type, kanji, tags, quiz exclusions, image and body are unchanged in the current file.
- **Component links:** CLEAN. Every existing card is linked: 切, 増, 下, 名, 舞, 風, 火, 分, 解. Missing cards are not invented: 踏, 麓, 殖, 振, 仮, 呂, 敷, 噴.
- **N2 reciprocal edits:** none required. The existing cards are levels 3–5.
- **Mappings:** all 20 match the TSV, JMdict entries and selected senses. Exception: the 1484 note promises "by-versus-to" quantities (F1).

## Findings
**F1 — 増やす "to a total" construction missing**
- Severity: Minor.
- Facet: Scoped coverage.
- Location: words\増やす.md lines 19–24.
- Claim and impact: The page teaches only the "by" amount (二人増やす). The 1484 mapping's source note promises "by-versus-to quantities", and learners don't get the common "to" pattern.
- Minimal remedy: add one example of the "to" form, e.g. 従業員を十人に増やします ("increase the staff to ten").
- Evidence: mappings line 3; the article never uses に to mark the resulting total.
- Confidence: high.

**F2 — ふわふわ has no guard against ソフト**
- Severity: Minor (existing gap, now exposed at N2).
- Facet: Correctness (quiz exclusions).
- Location: words\ふわふわ.md line 9.
- Claim and impact: ソフト ("soft", N4, no exclusions) can be a correct answer for ふわふわ: JMdict sense 2 is "soft" and the source gloss is "light, soft". The page already guards 柔らかい ("soft; flexible"), and 軟らかい guards both words. Adding jlpt 2 brings ふわふわ into N2 study.
- Minimal remedy: add ソフト to ふわふわ's quiz_exclusions (one-sided entry is enough).
- Evidence: principals line 4; mappings line 18; ソフト.md line 4; 軟らかい.md line 8.
- Confidence: medium.

## Optional
- **ぶらさげる.md:27** — "also writes ぶら下げる" understates it. It is the only JMdict spelling (ichi1, no usually-kana flag) and the Daijisen heading. A contrast with ぶら下がる could also be added.
- **振舞う.md:19–20** — "manner … with に" describes adverb forms such as 丁寧に. Could add 〜らしく and 〜ように振る舞う (Daijisen: 紳士らしく).
- **ブローチ.md:37** — "technical dictionary": Daijisen itself has the broach heading.
- **風呂敷.md:47–48** — Daijisen describes ふるしき as a sound change of ふろしき, not an older reading.
- **ブラウス.md:17** — 履く also covers trousers and skirts, not just shoes.
- **プラットホーム.md:32–33** — the "house" sentence is unclear.
- **Possible additions:**
  - 踏切: the spellings 踏切り and 踏み切り.
  - 振り仮名: katakana フリガナ, as used on forms.
  - ブラシ: 歯ブラシ.
  - 風呂敷: 大風呂敷を広げる.
- **Low-confidence guards I did not flag:** 振舞う/接する ("treat people") and ふわふわ/浮く ("float").

## Limits
- Git could not be run, so I did not check hashes or whether the patch matches the commit.
- I didn't verify the quiz pool mechanics (whether N4 words appear in N2 distractor pools); app code was outside the permitted search scope.
- All dictionary support comes from one authority (Daijisen via Weblio), plus Kotobank for 刷子. The failed Weblio fetches verify nothing.
- Naturalness judgments are my own, not a native speaker's: 壁にかばんをぶらさげました and 午後はフリーです are plausible but unconfirmed.
- I did not inspect the prepared comparison families or the older bodies. Comparison judgments rest only on the current articles listed under Scope; front-matter reads are not full-body reads.
