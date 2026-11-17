# Batch 135: initial blind review (reviewer 1)

## Snapshot

- Commit under review: `163b384e6cb8f75c06fe395f7b144cdd8b105673` (batch 135).
- New kanji cards: 博 厳 及 姿 履 巡 弾 彫 恵 憶 我 揚 救 暇 模.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-135-163b384e` (the manifest sha256 given in the brief is 9254e071…b796; I did not recompute it).
- Reviewer: a Claude model (Anthropic), working alone and read-only. I did not open the other reviewer's report or the author's rationale.
- Emphasis: facet 1 (correctness) and facet 2 (scoped coverage) are examined deepest. All four facets are covered for all 15 cards, the 15 stroke files and the 32 word-article diffs.

## Scope

Unit reviewed:
- the 15 files in `snapshot\kanji\`;
- the 15 files in `snapshot\strokes\`;
- the 32 modified word articles, through their 32 diffs in `diffs\`.

`repo\` and `titles\` were used only as context.

Packet files I opened:

| File | Extent |
| --- | --- |
| `INSTRUCTIONS.md` | full |
| `mechanical-checks.md` | full |
| `snapshot\kanji\*.md` (all 15) | full. I re-read the bodies and front matter while checking. |
| `diffs\*.diff` (all 32) | full |
| `snapshot\strokes\*.json` (all 15) | full. Parsed: kanji, strokeCount, number of strokes, source, revision, viewBox. Raw JSON printed for 及.json. |
| `evidence\source-metadata.json` | full |
| `evidence\joyo-pages.md` | part. Lines 1-900, which is essentially all pages: pp. 2, 3, 18, 21, 22, 35, 36, 44, 49, 65, 76, 106, 110, 126, 148, 152, 155, 162, 163. I also searched it for 臆/憶. |
| `evidence\public-source\weblio-*.txt` (all 15) | Full text of each Daijisen extract minus header lines. In one print batch the extracts were cut at about 1,300 characters each. I re-checked 履 by a targeted search. |
| `evidence\kanjidic2-records.xml` | part. Parsed records for 扱 丞 凜 墓 博 厳 巡 救, plus confirmation that 段 and 暮 are absent. |
| `evidence\jmdict-families.xml` | part. Structured queries of about 250 headwords covering every example word, compound and gloss quoted in the 15 cards, and reading searches for はじきゆみ, いつくし, ただす and たんじ. |
| `evidence\jmdict-digest.tsv` | part (header and first rows only) |
| `evidence\audits\quiz-safety.txt` | full |
| `evidence\audits\reading-options.txt` | part (header; the 博, 厳, 及, 姿 and 模 sections) |
| `evidence\audits\reading-exposure.txt` | part (header; every "attested reading … offered by" line; the 履 section; the final count line) |
| `titles\kanji-titles.tsv` | part (filtered lookups of quoted titles, "no card here" claims and English-title overlaps) |
| `titles\word-titles.tsv` | part (filtered lookups of words containing the batch kanji) |
| `repo\docs\content-format.md` | part (heading search; lines 71-139: kanji card fields, quiz authoring, curated reading questions) |
| `snapshot\words\恵まれる.md` and `snapshot\words\草履.md` | part (targeted line searches) |

I also made non-recursive listings of these folders:
- `snapshot\kanji`, `snapshot\strokes`, `snapshot\words`;
- `diffs`, `evidence`, `evidence\public-source`, `evidence\audits`;
- `titles`, the `repo` top level, `rubric`.

I did not open `evidence\app-code\*`, `rubric\*`, `provenance.json`, `packet-manifest.json` or `repo\docs\confusable-words.md`.

Public web sources:
- kanjiapi.dev, which serves KANJIDIC2 data: 甫 (7 strokes) and 段 (on ダン, タン).
- Weblio, おくそく: the 実用日本語表現辞典 and Digital Daijisen headwords 憶測／臆測.
- A jisho.org kanji search for 甫. It returned only the radical picker and was not usable.

## Verdicts

| Facet | Overall | Cards that differ |
| --- | --- | --- |
| 1. Correctness | NEEDS FIX (minor) | 博: false component statement in the mnemonic (C1). 憶: misleading account of 臆測 against the Joyo table the card itself cites (C2). The other 13 cards are CLEAN. |
| 2. Scoped coverage | CLEAN, one minor gap | 憶: the Joyo-standard spelling 臆測/臆説 is not acknowledged (part of C2). The other 14 cards are CLEAN. |
| 3. Consistency and quiz safety | CLEAN | No card differs. Some quiz_exclusions are weak but harmless; see Optional. |
| 4. Comprehensibility | CLEAN, with polish suggestions | No card fails. 弾, 博, 我 and 揚 have dense Daijisen sense paragraphs (see Optional). |

**Diffs (32 word articles): CLEAN.**
- Each diff changes exactly one line, in "How the kanji combine". It link-wraps the first mention of the new kanji to `../kanji/X.md`.
- Every target is the intended card, and no other text changed.
- The CRLF line endings of 模倣 and 鷹揚 are preserved, and the passages still read correctly.
- This matches the mechanical link plan (32/32 pairs, 0 problems).

**Strokes (15 files): CLEAN.**
- In every file, `kanji` equals the file name and strokeCount equals the number of strokes equals the card's `strokes:` value.
- Source: KanjiVG revision 70a0b7ae…, viewBox 0 0 109 109.
- 及.json's three stroke types (㇒, ㇋, ㇏) match the card's verbal description of the three strokes.

**What was checked and found correct** (summary of the CLEAN results):

Front matter:
- Every card's grade, strokes, radical and number, on/kun lists, quizOnyomi and quizKunyomi match `source-metadata.json`.
- Spot checks against KANJIDIC2 also agree: 博 ひろ nanori, 厳 radical 27, 巡 radical 47, 救 grade 5.

Joyo table claims:
- Every reading row, example word, bracketed form, ⇔ contrast and variant-form mention quoted from `joyo-pages.md` matches. This includes:
  - 博: 博士(はかせ) and the バク row with 博労 and 博徒;
  - 履: 草履(ぞうり);
  - 巡: お巡（まわ）りさん;
  - 弾: 弾く⇔引く and 弾⇔玉,球, plus the (彈) variant;
  - 恵: (惠);
  - 揚: ⇔ 上げる/挙げる and 上がる/挙がる.

Daijisen claims:
- All 15 match the extracts. This covers the sense counts and sense contents, compounds, 難読 lists (博, 我, 模) and the separate counter entries (弾 だん, 巡 じゅん).
- Kun lists: 履 はく ふむ くつ; 厳 いつくし; 憶 おもう; 博 ひろい.
- The 呉音 mark on 救 ク.

JMdict glosses:
- Every double-quoted English gloss attributed to JMdict, about 150 across the 15 cards, matches the cited entry, as do the sense positions. Examples: たま "bullet" as sense 5; 彫る "to tattoo" as sense 2; 揚げる "deep-fry" first.
- The spelling notes also match:
  - irregular okurigana: 及 for および;
  - rarely used forms: 順礼/一順, 回る→巡る, 憶う/憶える, 履→靴, 摸倣;
  - ateji: 怪我, 埃及;
  - honorific: 恵贈/恵与/恵投;
  - usually written in kana: お巡りさん, はじく, 酸模.

Readings in words:
- Every per-character segmentation statement was checked against the JMdict readings. Examples: 鷹揚 オウ+ヨウ, 賭博 ト+バク, 規模 キ+ボ, 下履き ば.

Titles and component claims:
- Every quoted card title matches `kanji-titles.tsv` exactly.
- Every "no card here" claim is true: 弓 戈 慧 彡 臆 甫 又 攴 摸 敢.
- Stroke arithmetic and component positions are true for all cards except 博 (C1). Examples: 履 = 尸 3 + 復 12; 救 = 求 7 + 攵 4 = 11 (the same as 教); 暖 has 13 strokes; 模 = 木 + 莫 (艹 日 大).

Comparisons in the Notes:
- All true, including 扱 having キュウ in KANJIDIC2, 段 having ダン and タン, 墓 being read ボ, and 丞 すく.う and 凜 きびし.い in KANJIDIC2.

Rare and source-only rows:
- 厳 いつくし, 弾 タン, ただ.す and はじ.きゆみ, 暇 いとま, and 救 ク (Daijisen only) are each qualified honestly. The JMdict extract has no はじきゆみ or いつくし word; ただす occurs only in ただすつかさ (弾正台), and たん only in rare or obsolete forms (弾棋 たんぎ; 弾指 たんじ/たんし).

Quiz checks:
- Titles are unique.
- No unexcluded English title outside the batch is a defensible answer for any new card. I searched the titles for synonyms of every sense; the close ones are already excluded: 医, 広, 容, 恩, 助, 丞, 援, 貯, 覚, 届, 至, 到, 達, 自, 靴, 着, 演, 倣, 範, 型, 形, 刻, 時, 悠.
- Distractor titles are wrong in both directions.
- Every quizOnyomi/quizKunyomi reading has a linked word article in its own Readings row, as `content-format.md` requires.
- The quiz-safety audit has 0 errors. The reading audits show 0 production hits and 0 padded hits, and 0 seeds produced fewer than three wrong options.

Section order and headings (`## Meaning and origin`, `## Readings`, `## Common words`, `## Notes`) and the modern-shape mnemonic disclaimers are present on all 15 cards. No card makes a historical claim.

## Findings

Established defects:

### C1: 博 mnemonic misstates the right-hand component (minor; facet 1)

- **File:** `snapshot\kanji\博.md` line 27.
- **Claim:** "At the right is a shape like 甫 with an extra dot at its top right … standing over 寸".
- **Problem:** 甫 already has the dot at its top right as its own seventh stroke. It is 7 strokes in KANJIDIC2 (checked on kanjiapi.dev) and has the same dot in 補 and 捕. The right side of 博 is 甫 + 寸 with no additional dot: 十 2 + 甫 7 + 寸 3 = 12, which matches `strokes: 12` and 博.json. An "extra" dot would give 13 strokes.
- **Impact:** A learner who checks the shape against 甫 will look for a dot that is not there, or write 博 with a superfluous stroke. The card has thus made a false component statement.
- **Remedy:** "At the right is 甫 (which has no card here), dot included, standing over 寸". Optionally add "the same right-hand part as 薄 under 艹", which the Notes already say.
- **Evidence:** the 博.json strokeCount of 12; 甫's 7 strokes (KANJIDIC2 via kanjiapi.dev, `stroke_count: 7`); stroke arithmetic.
- **Confidence:** high.

### C2: 憶 presents 臆測 as a rare spelling, though the cited Joyo table treats 臆 as the primary form (minor; facets 1 and 2)

- **File:** `snapshot\kanji\憶.md` line 25 (and the usage evidence on line 51, which cites PDF p. 18).
- **Claim:** "JMdict also lists 臆説 and 臆念 as spellings of 憶説 and 憶念, and 臆測 as a rarely used spelling of 憶測; 臆 does not have a kanji card here."
- **What is true:** The JMdict attribution is accurate. Entry 1589020 is 憶測 with 臆測 tagged "rarely used kanji form", and entry 1182750 is 憶説;臆説 with no tag.
- **What is missing:** The card cites the official Joyo table p. 18 as its usage evidence, and that page (`joyo-pages.md` lines 120-122) gives:
  - 臆 its own row, オク 臆説，臆測，臆病;
  - the note 「臆説」，「臆測」は，「憶説」，「憶測」とも書く.

  The table therefore treats 臆測/臆説 as the standard spellings and 憶測/憶説 as the alternatives. The Digital Daijisen headword is おく‐そく【憶測／臆測】, which gives the two equal weight (live Weblio).
- **Impact:** A learner is told, with no counterweight, that 臆測 is rare, when it is the Joyo-table form under its own Joyo kanji. That is a misleading usage claim on a point the card's own cited source addresses. It is also a small coverage gap, since 臆 and its オク words are the main confusable of 憶 and the Joyo table pairs them explicitly.
- **Remedy:** Keep the JMdict sentence and add one sentence along these lines: "The official Joyo table, under the separate Joyo kanji 臆 (no card here), lists 臆説 and 臆測 and notes that they may also be written 憶説 and 憶測; both spellings are in ordinary use." Optionally add 臆病 おくびょう, "cowardly; timid", as the everyday 臆 word, which JMdict does not allow as 憶病 except as a rare form.
- **Evidence:** `joyo-pages.md` lines 118-122; `jmdict-families.xml` entries 1589020, 1182750 and 1182790; Weblio おくそく (Daijisen headword 憶測／臆測).
- **Confidence:** high on the facts. The severity (minor) is my judgement.

No other established defects were found.

How the leads resolved, none of them a defect:

(a) 履 / 草履:
- The card says ぞう belongs to 草 and り is 履's リ. This is supported by the Daijisen headword ぞう‐り (historical kana ザウ‐リ) and by JMdict, which does not tag 草履 as jukujikun, unlike 博士 はかせ.
- The account of the Joyo table (bracketed under 履, listed in the appendix) is accurate.
- `content-format.md` warns that the linked word is navigation evidence only, and the card's segmentation claim is independently supported. Not a defect; see Optional for polish.

(b) 博:
- ハク is exemplified by 博物館, which divides cleanly.
- The card correctly refuses to segment 博士 はかせ, which JMdict tags as gikun/jukujikun and the Joyo table brackets.
- The バク row (博徒, 賭博) is correct and matches the table (博労, 博徒).

(c) 及:
- All three distractors give no usable キュウ option: 吸 and 級 are キュウ and excluded, and 扱 has no on-reading on its card. The fallback still yields 36 distinct wrong options over 100 seeds and never fewer than three.
- The account of およ.び / および is accurate: JMdict marks 及 alone as irregular okurigana, and the Joyo table marks 及び as a conjunction.

(d) 模:
- Only four wrong options are reachable for モ (おう from 横, plus もく, もつ, もん), but never fewer than three per quiz.
- ぼ is correctly excluded as 模's own reading.
- The ボ / 規模 row matches the Joyo table. The claim that 暮 and 墓 are read ボ is true per KANJIDIC2, even though the repo's 墓 card shows no on-reading.

(e) Rare rows: all are honestly qualified and match KANJIDIC2, JMdict and the Daijisen (see the verdict summary).

(f) 我/怪我, 恵/恵まれる, 憶:
- 怪我 is correctly explained as ateji.
- 恵まれる correctly supplies the めぐ stem; its word article traces it to the passive of 恵む.
- 憶 having no kun row is correct. The 臆 point is C2.

(g) quiz_exclusions: some are weak but harmless (see Optional).

(h) Reading-exposure:
- All 19 latent collisions are KANJIDIC2 name readings or the JMdict 靴 entry 履 = くつ. None can be drawn in any shipped pool.
- No action needed.

## Optional

Polish, not defects:

- **O1: 履** (line 36). The account would be clearer with one clause saying that ぞう is a voiced, sound-changed form of 草's old reading サウ (Daijisen ザウ). It could also soften "which is why the Joyo table puts 草履 … in its appendix" to "the Joyo table accordingly lists 草履 in its appendix". The 草履 word article (line 31) tells learners to "learn the complete reading ぞうり", which is consistent but could cross-reference the card's segmentation.
- **O2: 模** (line 36). "Both are learned here as whole words" (相模, 酸模) reads oddly, since neither has an article. Suggest "Both are read as whole words; 模 has no separate reading in them."
- **O3: weak quiz_exclusions.** These are harmless but not strong direct pairs:
  - 揚–起 ("wake; rise") and 揚–賛: the 揚 title has no "praise".
  - 模–漠: the 模 title has no "vague".
  - 巡–査.
  - 暇–去 (only via お暇).

  They only reduce fallback pools; keep or drop at the author's discretion. By contrast, 救–貯 ("save" / "save up") and 救–保 are justified by the English wording of the titles.
- **O4: comprehensibility.** The Daijisen sense paragraphs of 弾 (line 25: five senses, 14 quoted glosses), 博, 我 and 揚 are long for an N5-N4 reader on a phone. Consider trimming each to the two or three most useful compounds per sense. The central idea is correctly placed first on every card.
- **O5: reading-quiz options.** The curated distractors of 及 (吸 扱 級) contribute no option to the キュウ reading question. If the author wants one curated non-キュウ option, a different-reading look-alike could replace one of them. This is a pure quality preference: the quiz is safe as it stands.

## Limits

- **Tool-call discipline.** In this part of the session every response contained exactly one tool call. Earlier context was summarized; the summary records no parallel calls, but I cannot re-inspect those turns directly.
- **Packet limits.** The Android JVM content tests and the Kotlin reading-audit cross-check were not run at this snapshot (known packet limit; not reported). I did not run any tests myself.
- **Dictionary checks.**
  - Readings and glosses were verified mainly against the packet's pinned JMdict extract (`jmdict-families.xml`, 2026-11-17 snapshot) and the Daijisen extracts.
  - Live public checks were spot checks only: kanjiapi.dev for 甫 and 段, and Weblio for おくそく. Live dictionaries may differ from the pinned snapshots.
  - "No JMdict word found" statements (いつくし, はじきゆみ) were confirmed only within the packet's JMdict family extract, not the full JMdict.
- **Daijisen extracts.** One print batch truncated each extract at about 1,300 characters. The sense, compound and 難読 claims had already been checked against the complete text in the other batch and in targeted searches.
- **Not opened.** `evidence\app-code\`, `rubric\` and `provenance.json` were not opened. Reading-quiz behaviour was judged from the audit files and `content-format.md`.
- **Lint warnings.** The 7 context warnings in mechanical-checks.md were not investigated beyond confirming that no diff touches a Dictionary: line. I found no real defect there.
- **Assumptions.** I assume the "official Joyo table" text extracts in `joyo-pages.md` faithfully represent the PDF. I also assume a mnemonic component statement counts as a correctness claim under facet 1, as INSTRUCTIONS.md states.
