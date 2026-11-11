# Batch 109 — initial blind review (reviewer 1)

Reviewer model: **Claude Opus 5.5** (model ID `claude-opus-5.5`), working alone, read-only, one tool call at a time.

## Snapshot

- Commit `0a20f4bf2415d6b4d20644f518990e8c938259b1`, batch 109.
- Kanji cards: 催 促 摩 擦 括 弧 抵 抗 撮 影 攻 撃 掲 批 択.
- Packet: `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-109-0a20f4bf`.
- Mechanical checks (from `mechanical-checks.md`): tests, validate and the quiz simulation passed. Lint has one warning: `words/撮る.md` has no `Dictionary:` line. That warning predates the batch; the batch only wraps a link in that file.

## Scope

Packet files I opened:

| File | Read |
| --- | --- |
| INSTRUCTIONS.md | full |
| mechanical-checks.md | full |
| evidence\source-metadata.json | full |
| evidence\kanjidic2-records.xml | lines 79–140 viewed; the 15 records parsed and summarized with PowerShell |
| evidence\jmdict-families.xml | parts: lines 2318–2410, 6245–6320, 7435–7470, 7838–7905 and 12137–12170, plus PowerShell dumps of every JMdict entry ID cited in the 15 Metadata lines and the families checked |
| evidence\jmdict-digest.tsv | part: lines 1–37 and greps |
| evidence\public-source\weblio-{催,括,弧,抵,撮,影,攻,撃}.txt | full |
| evidence\public-source\weblio-{批,択}.txt | part: header and Daijisen block |
| evidence\public-source\weblio-{掲,促,摩,擦,抗}.txt | part: first ~700 characters of the extract (Daijisen block and the start of Wiktionary/KANJIDIC) |
| repo\docs\content-format.md | part: lines 1–290 and 96–110, plus a grep for quiz_exclusions and distractors |
| rubric\copilot-instructions.md | part: lines 1–260 of about 300 |
| titles\kanji-titles.tsv | greps only |
| titles\word-titles.tsv | greps only |
| repo\words\たいてい.md | part: lines 1–40 |
| repo\kanji\{形,包,囲,写,選,打,刊,採,景,戦,示,置,反,対,結,束,曲,円,映,磨,掃,勧,励,責,判,功}.md | first 16 lines only (title, distractors, quiz_exclusions) |
| snapshot\kanji\*.md (all 15) | full |
| snapshot\strokes\*.json (all 15) | parsed: kanji, property list and stroke count; first 400 characters of 促.json viewed |
| snapshot\words\催し.md | full |
| diffs\words__*.md.diff (all 18) | full: 催し, 催促, 摩擦, 擦る, 括弧, 撮る, 撮影, 影, 影響, 攻撃, 攻める, 専攻, 反抗, 抵抗, 批判, 批評, 掲示, 選択 |

Public web sources:
- jisho.org API (live JMdict): 擦る (all homographs) and 影 かげ.
- jisho.org API: a batch lookup of 58 example words: 開催, 主催, 催眠, 催涙, 催す, 催し, 催促, 促進, 督促, 促す, 促音, 摩擦, 摩天楼, 摩する, 擦り傷, 擦過傷, 靴擦れ, 擦れる, 括弧, 一括, 総括, 括約筋, 括る, 円弧, 抵抗, 抵触, 抵当, 大抵, 抗議, 対抗, 抗う, 反抗, 抗がん剤, 撮る, 撮影, 特撮, 自撮り, 隠し撮り, 影響, 月影, 面影, 遺影, 攻撃, 攻める, 専攻, 反撃, 衝撃, 目撃, 撃つ, 掲示, 掲載, 掲げる, 批判, 批評, 批准, 選択, 採択 and 択一.
- One jisho.org HTML page returned only navigation chrome and was not used.

## Verdicts

Overall verdicts by facet:

| Facet | Verdict |
| --- | --- |
| 1 Correctness | **Pass with minor defects.** Every front-matter field matches KANJIDIC2 and source-metadata. Every example reading and gloss I checked matches the pinned JMdict and live JMdict (jisho.org). Defects: 摩 (F3) and 擦 (F4). |
| 2 Scoped coverage | **Pass with one minor gap.** Every metadata reading has a row or an explicit qualification. Gap: 擦 (F4). |
| 3 Consistency and quiz safety | **Fail.** 影 (F1) is a major defect; 括 (F2) is minor. Links resolve, tags and grades are right, section order is right, and stroke counts match. |
| 4 Comprehensibility | **Pass with minor defects.** The cards are clear and lead with the central idea. The 摩 contradiction (F3) and the missing kana note on 擦 (F4) affect learners. |

Per-card verdicts (P = pass, P− = pass with optional or minor notes, F = fail):

| Card | Correctness | Coverage | Quiz safety and consistency | Comprehensibility |
| --- | --- | --- | --- | --- |
| 催 | P | P | P− (O6) | P |
| 促 | P | P | P− (O5) | P |
| 摩 | P− (F3) | P | P | P− (F3) |
| 擦 | P− (F4) | P− (F4) | P | P− (F4) |
| 括 | P | P | P− (F2) | P |
| 弧 | P− (O3) | P | P | P |
| 抵 | P− (O2) | P | P− (O10) | P |
| 抗 | P− (O4) | P | P | P |
| 撮 | P− (F5) | P | P | P |
| 影 | P | P | **F (F1)** | P |
| 攻 | P | P | P | P− (O7) |
| 撃 | P | P | P | P− (O7) |
| 掲 | P− (F5) | P | P | P |
| 批 | P | P | P | P |
| 択 | P | P | P | P |

The 18 word-article diffs pass. Each diff changes exactly one line, and the only change is wrapping an existing kanji character in a link of the form `[X](../kanji/X.md)`. Every target is one of the 15 cards in this batch. The surrounding sentences, readings and line breaks are unchanged and still read correctly. Unlinked characters with no card (響, 評) were correctly left plain.

## Findings

Established defects follow. Severity scale:
- **Major** means a learner can be marked wrong for a defensible answer, or is taught something false.
- **Minor** means misleading or inconsistent content with limited impact.

### F1 — Major — Facet 3 (quiz safety) — `snapshot\kanji\影.md:13` (`distractors: [景, 形, 京]`)

**Claim and impact:** The curated distractor 形 is displayed as "shape; form". That is a defensibly correct meaning of 影, not a wrong one:
- JMdict sense 1 of 影 かげ is "shadow; silhouette; **figure; shape**". This appears in the pinned entry 1590145 and in the live jisho.org entry.
- Digital Daijisen 影 sense 3 is 「物の姿や形」, for example 人影 and 機影.
- The card's own title, "silhouette", is a kind of shape.

A learner who chooses "shape; form" for 影 has given a dictionary-supported answer and is marked wrong. The card's Notes (line 45) also point out that 形 shares 彡, so the pair is confusable in both shape and meaning. In the reverse direction, 形.md's distractors are [開, 研, 新] and contain no 影.

**Remedy:**
- Replace 形 with a clearly wrong option, for example another エイ sound-alike or a look-alike whose title is not shape, shadow, image or light. Confirm that the replacement card exists.
- Consider declaring `quiz_exclusions: [映, 形]` so that tag or random fallbacks cannot pair the two either. 形 already shares 彡, so tag-based fallback could easily choose it.
- Keep the 形 comparison in Notes.

**Evidence:** jmdict-families.xml entry 1590145; jisho.org API `影 かげ`; weblio-影.txt (Daijisen ３ 物の姿や形).

**Confidence:** High.

### F2 — Minor — Facet 3 (quiz safety) — `snapshot\kanji\括.md:3, 15` (title "tie together; enclose"; `quiz_exclusions: [結, 束]`)

**Claim and impact:** Two existing cards display the same English word "enclose": 包 "wrap; enclose" (kanji-titles.tsv line 205) and 囲 "surround; enclose" (line 271). Neither side declares an exclusion:
- 包.md has no quiz_exclusions and distractors [回, 勉, 同].
- 囲.md has no quiz_exclusions and distractors [国, 困, 図].

The curated four choices are safe. However, content-format.md lines 96–106 says the app fills or replaces choices from tag, random, level and custom pools, and only quiz_exclusions blocks such a pair. In those modes, 括 could appear next to "wrap; enclose" or "surround; enclose", which gives two literally matching answers.

The batch otherwise excludes every title-overlap pair:
- 抗 excludes 反 and 対 ("oppose").
- 掲 excludes 刊 ("publish"), 示 and 置.
- 択 excludes 選 and 採.

So 括 is inconsistent with the rest of the batch.

**Remedy:** Add 包 and 囲 to 括's `quiz_exclusions`. Alternatively, retitle 括 without "enclose", for example "tie together; bundle; bracket". The direct pairs 括/包 and 括/囲 each have literal title evidence; this is not a transitive clique.

**Evidence:** kanji-titles.tsv lines 205, 271 and 478; the front matter of 包.md, 囲.md and 括.md; content-format.md lines 96–106.

**Confidence:** Medium-high. The risk is limited to fallback and custom pools.

### F3 — Minor — Facets 1 and 4 — `snapshot\kanji\摩.md:32–36`

**Claim and impact:** Line 36 says the selection "is a teaching selection, not a claim that those readings are invalid, obsolete or rare." The rows directly above it contradict that:
- Line 34 says 摩る (する) "is only a rarely used kanji form" (the rK flag in JMdict).
- Line 33 says さする is "usually written in kana".

The Wiktionary text in weblio-摩.txt also says the jōyō table has **no** kun readings for 摩: ま-する, さ-する and す-る are all 表外. A beginner is told two incompatible things in the same section.

A related point: ま.する is labelled "kun" (line 32). That follows KANJIDIC2 and Wiktionary, but 摩する まする is the on reading マ + する (JMdict 1982610, a vs-s verb). The card could say so in a few words.

**Remedy:** Replace the line-36 boilerplate with something like: "None of these is a jōyō-table reading: 摩る is a rare spelling of する and さする is usually kana, so only マ is practised. まする is マ + する."

**Evidence:** jmdict-families.xml (摩る rK; さする uk); jisho.org (摩する まする; 摩る さする, usually kana); weblio-摩.txt (Wiktionary: 常用漢字表内の訓読みはありません).

**Confidence:** High.

### F4 — Minor — Facets 1, 2 and 4 — `snapshot\kanji\擦.md:35, 38` (quizKunyomi こす.る)

**Claim and impact:** The card selects こす.る as the practised kun reading and links 擦る こする with no qualification. However:
- JMdict 1298910 (pinned, and live jisho.org) marks 擦る こする as "**usually written using kana alone**".
- weblio-擦.txt (Wiktionary) lists こす-る and こす-れる as **outside** the jōyō table. The jōyō kun readings are す-る and す-れる, which the card keeps but does not select.

Other cards in the same batch flag kana-usual words (摩 line 33, 括 line 32), so the omission is inconsistent. An N5–N4 learner will assume 擦る is the normal spelling of こする, and that こす.る is the main kun reading of 擦.

Keeping こす.る for practice is acceptable, because it is the reading that has a linked article. The missing qualification is the defect.

**Remedy:** In row 35 or line 38, add: "こする is usually written in kana; the jōyō kun readings are す.る and す.れる (擦る する "rub; strike a match")."

**Evidence:** jmdict-families.xml 1298910; jisho.org API `擦る`; weblio-擦.txt.

**Confidence:** High.

### F5 — Minor — Facet 1 (component statements) — `snapshot\kanji\撮.md:25` and `snapshot\kanji\掲.md:25`

**Claim and impact:** The mnemonics say 最 is "made of 日 above 取" and 曷 is "made of [日](日.md) … above 匂". In both characters the top element is conventionally 曰 ("say", radical 73; KANJIDIC2 gives 最 radical 73), not 日 "sun".

The 掲 mnemonic then builds on the wrong component ("holding a sign up toward the sun") and links to the 日 card. The labels "modern shape" and "not etymology" make the harm small. Even so, the brief requires component statements to be true, and the two shapes look alike in print.

**Remedy:** Change the statements to "曰 (a flat 日-like box)". Alternatively, keep the sun image but say "a 日-like box".

**Evidence:** KANJIDIC2 and standard radical tables (曰, no. 73).

**Confidence:** Medium. Some learner dictionaries and radical-search UIs lump 曰 under 日, so a reviewer may treat this as polish.

## Optional

These are polish items, not defects.

- **O1 — Mnemonic tags.** Many of these characters are commonly analysed as phonetic compounds, for example 批 (比 ヒ), 抗 (亢), 抵 (氐) and 攻 (工 コウ). The cards correctly make no historical claim and use the tag `structure-unclassified`. That is consistent with the repository's cautious policy, so no change is needed.
- **O2 — 抵 title and link.**
  - "collide" (line 3) is only weakly supported. Daijisen's 突き当たる and JMdict 抵触's "running afoul / conflict" sense are the closest. Consider "resist; push against".
  - Line 23 mentions 大抵 たいてい and says it is usually kana, but does not link the existing kana article `../words/たいてい.md`. That article would be a useful N4 bridge.
- **O3 — 弧 line 23.** "an older sense of 'bow' (ゆみ)": Daijisen lists 木の弓 as sense 1 with no age label. "First dictionary sense" would be safer than "older". Separately, the Notes' look-alike framing with 弱 is slightly loose, because 弱's halves are not exactly 弓.
- **O4 — 抗 line 23.** JMdict lists 抗がん剤 as the first form, and jisho.org finds it as written. 癌 is not a jōyō kanji. The card's 抗癌剤 is valid, but 抗がん剤 is the more usual modern spelling.
- **O5 — 促 distractor 速 "fast".** It sits close to 促す's "hasten / quicken" senses. It is defensibly wrong because the card explains urging versus speed (line 43). Low risk.
- **O6 — 催 distractor 集 "gather".** 催し is glossed "social gathering" and Daijisen explains 開催 as 人を集めて会を開く. "gather" is still not a meaning of 催 itself, so it is defensibly wrong. Similarly, 催's secondary sense うながす (催促) sits near 促 "urge; prompt", but only in fallback mode. Low risk. Consider a more neutral distractor.
- **O7 — 攻.md and 撃.md, first Notes bullet on each.** "Both characters concern hitting at a target" fits 撃 but loosely describes 攻, which is attacking or going on the offensive, not hitting. Consider "both concern attacking".
- **O8 — 催 もよう.す.** This is correctly marked "Source-only" (line 31). Optionally add that the standard verb is もよおす and that もようす is a non-standard variant.
- **O9 — Out of scope (pre-existing word articles).** 括弧 is marked uk in JMdict (かっこ), and `words/撮る.md` has no Dictionary line. These are not batch changes.
- **O10 — 抵 fallback pairs.** "resist" (抵) could show alongside 反 "oppose; reverse" or 対 "oppose; face" in fallback pools. The overlap is real but weaker than the 抵/抗 pair the card already excludes. Optional.

## Limits

- I followed the serial rule: one tool call per response. Earlier in the session, before the coordinator's correction, some view calls were batched in parallel. Nothing was redone.
- I did not search for or read other reviewers' reports or the author's rationale. I opened no path outside the packet except the report path.
- Partial reads:
  - rubric\copilot-instructions.md: the last ~40 lines.
  - content-format.md: beyond line 290, except lines 96–110 and greps.
  - Several Weblio extracts: only their Daijisen and Wiktionary heads.
  - jmdict-digest.tsv: mostly by grep.
  - repo\kanji cards: front matter only.
- Assumptions:
  - The English kanji-card section order was inferred from content-format.md's mapping. All 15 cards use: H1, facts line, Meaning and origin, Readings, Common words, Notes, Metadata.
  - For F2, I assumed quiz_exclusions on related existing cards are declared within their first 16 lines, as they are on 勧, 励 and 功.
- Public verification:
  - Live jisho.org (current JMdict) matched the pinned evidence for every word in the 58-word batch: readings and glosses as cited.
  - Pinned data may still differ from current online data for entries I did not look up live. For example, the live API's form list for 摩る omits the rK label that the pinned entry shows.
  - Daijisen claims were checked only against the packet's Weblio extracts, not re-fetched.
  - Example sentences: the cards in this batch contain no full example sentences apart from the word lines. The word-article sentences outside the diff hunks are out of scope.
- Strokes: I checked strokeCount and the stroke-array length against the card and KANJIDIC2 for all 15 files (all match: source KanjiVG, revision 70a0b7a…, viewBox 0 0 109 109). I did not visually inspect stroke geometry or order.
- I could not verify whether the app actually uses fallback distractors when all three curated distractors are present. F2's impact assumes the fallback and custom-pool behaviour that content-format.md describes.
