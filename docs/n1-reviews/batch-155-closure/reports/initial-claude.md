# Batch 155 blind review: initial report (Claude)

## Snapshot

- Commit `97c49eb27abbd2961ed93de7c67ece0fa53b5c8a` (batch 155). New kanji cards: 卑 汰 沙 沢 胡 鼓.
- Packet `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-155-97c49eb2` (manifest sha256 669b1560…e9d1aa, as given in the assignment).
- Reviewer: Claude, an Anthropic model, acting as the first of the two blind reviewers. The review was read-only and done alone.

## Scope

Unit under review:
- the 6 new cards in `snapshot\kanji\`;
- the 6 stroke files in `snapshot\strokes\`;
- the 6 modified word articles in `snapshot\words\`, with their 6 diffs in `diffs\`.

`repo\` was used only as read-only context.

Packet files opened:

| File | Read |
|---|---|
| INSTRUCTIONS.md | full |
| mechanical-checks.md | full |
| snapshot\kanji\卑.md, 汰.md, 沙.md, 沢.md, 胡.md, 鼓.md | full |
| snapshot\strokes\卑.json, 汰.json, 沙.json, 沢.json, 胡.json, 鼓.json | 汰.json raw in full; all 6 parsed in full (kanji, revision, strokeCount, ids, types, point counts) |
| snapshot\words\卑怯.md, 太鼓.md, 胡椒.md, 贅沢.md, 無沙汰.md, 御無沙汰.md | full |
| diffs\ (all 6 .diff files) | full |
| evidence\kanjipedia-senses.txt | full |
| evidence\daijisen-heads.txt | full |
| evidence\kanjipedia-outside-readings.json | full |
| evidence\public-source\weblio-*.txt (all 6) | full |
| evidence\source-metadata.json | full |
| evidence\okurigana-scan.txt | full |
| evidence\joyo-pages.md | full |
| evidence\kanjivg-components.txt | full |
| evidence\audits\word-remarks.json | full |
| evidence\jmdict-families.xml | part: script extracts of every entry id the cards cite, plus related entries |
| evidence\jmdict-digest.tsv | part: header and the 卑 rows |
| evidence\kanjidic2-records.xml | part: parsed records for the 6 kanji and for every exclusion and distractor kanji |
| evidence\audits\reading-options.txt | part: lines 1-60, plus the tail kept in mechanical-checks.md |
| evidence\audits\reading-exposure.txt | part: grep of the key lines, plus the tail |
| titles\kanji-titles.tsv | part: filtered rows |
| titles\word-titles.tsv | part: header and filtered rows |
| repo\docs\content-format.md | part: grep, then lines 110-175 |
| repo\kanji\湿.md | part: first 14 lines |
| repo\kanji\低.md, 近.md, 軽.md, 疑.md, 何.md, 乱.md, 長.md, 洗.md, 選.md, 抜.md, 打.md, 砂.md | part: title and kunyomi front-matter lines |

Not opened: evidence\kanjivg-svgs.txt, evidence\audits\quiz-safety.txt, evidence\app-code\.

Public web check: jisho.org's kanji page for 胡. It gives 9 strokes, radical 肉 (⺼), parts 十 口 月, the meanings "barbarian, foreign", kun なんぞ and on ウ (the rest of the page was truncated). This matches KANJIDIC2 and the card.

## Verdicts

| Facet | Overall | Per card |
|---|---|---|
| 1. Correctness | CLEAN | Same for all 6 cards and all 6 diffs. |
| 2. Scoped coverage | CLEAN | Same for all 6 cards. |
| 3. Consistency and quiz safety | CLEAN | Same for all 6 cards. 胡's distractor set is weak but valid (O1). |
| 4. Comprehensibility | CLEAN | Same for all 6 cards. |

### 1. Correctness

**Front matter.** Every card's front matter matches source-metadata.json and KANJIDIC2: grade, strokes, radical, on and kun lists, the name readings, and quizOnyomi and quizKunyomi.

**Joyo claims.** Every claim about the Joyo table matches joyo-pages.md:
- 卑, p.130: ヒ with 卑近, 卑屈 and 卑下; いやしい, いやしむ and いやしめる.
- 汰, p.102: タ with 沙汰.
- 沙, p.58: サ with 沙汰.
- 沢, p.104: タク with 光沢 and 潤沢; さわ with 沢; the old form 澤.
- 鼓, p.50: コ with 鼓動, 鼓舞 and 太鼓; つづみ with 鼓 and 小鼓.
- 胡: the card correctly says it is not in the table, and it has no Joyo PDF Usage link.

**Kanjipedia and Digital Daijisen quotes.** I checked every quote against the evidence files and found them all accurate:
- the senses of all 6 kanji;
- the outside-the-table (外) lists;
- Daijisen's 5 senses for 卑, which have no ちかい sense but add へりくだる and 土地が低い;
- 沙: ▽ for a reading outside the table, and 梵語の音訳字;
- 沢: 物が豊かにあること with 沢山 and 贅沢, and 人に施す恵み;
- 胡: ［人名用漢字］, 外国産の with 胡椒 and 胡麻, いいかげんな with 胡散 and 胡乱, and 胡蝶;
- 鼓: three senses, and the note that 皷 is a variant (異体字).

**JMdict glosses and ids.** Every quoted gloss and entry id is real and attached to the right entry, including:
- 卑怯 1482710 (2 senses);
- 卑劣 1482820;
- 卑しい 1482660 ("shabby; poor-looking" as sense 3);
- 卑しむ 1482670;
- 淘汰 1448570;
- 淘げる 2827211 (rare, usually written in kana);
- 沙門 1291490 (しゃもん and さもん);
- 砂 1291500 (すな is restricted to 砂 and 沙; いさご is unrestricted);
- 沢 1415850;
- 沢 たく 2843433 (archaic);
- 贅沢 1573150;
- 潤い, 潤す and 艶, none of which lists 沢;
- 胡椒 1267600 and 胡麻 1267560 (usually written in kana);
- 胡散 2457840;
- 胡乱 1267590;
- 胡散臭い 1267540;
- 何ぞ 2270830 (written 何ぞ or 奚, not 胡; its sense 2 is "what");
- みだり 2714830 (archaic; lists 乱り);
- 胡蝶 (poetical term);
- 胡 こ 2230390 (historical term);
- 鼓 1267900;
- 小鼓 2257170;
- 長生き 1610940;
- 低い 1434180;
- 近い 1242130;
- 軽んじる 1252570;
- 抜く 1478190.

**Readings and examples.** Every quiz reading has a word link that is supported by the dictionaries:
- 卑 ヒ: 卑怯;
- 汰 タ and 沙 サ: 無沙汰 and 御無沙汰;
- 沢 タク: 贅沢;
- 胡 コ: 胡椒;
- 鼓 コ: 太鼓.

No kun reading is quizzed on any card. The source-only and non-KANJIDIC2 rows are accurately qualified and sourced:
- 汰: タイ, おご.る, にご.る and よな.げる;
- 沙: いさご, シャ and すな;
- 沢: うるお.い, うるお.す and つや;
- 胡: なんぞ.

Note on 沙's いさご row: content-format.md lines 135-147 do not forbid extra rows. 沙 line 44 explains why みぎわ gets no row.

**Mnemonics.** All six are labelled as modern-shape mnemonics, not etymology, and make no historical claim. Every component, position and stroke statement matches kanjivg-components.txt at revision 70a0b7ae:
- 卑: 丿(1), 田(2-6), 丿(7), 十(8-9).
- 汰, 沙 and 沢: 氵 on the left, marked original=水.
- 汰: 太 contains 大 at the top (4-6) and 丶 at the bottom (7).
- 沙: 少 = 小(4-6) + 丿(7).
- 沢: 尺 = 尸 with a split 八 (6 and 7).
- 胡: 古 on the left = 十(1-2) + 口(3-5); 月 on the right, marked original=肉.
- 鼓: 壴 on the left with 士(1-3); 豆 is split into three parts, with stroke 3 shared. 支 on the right = 十(10-11) + 又(12-13).

**Stroke files.** All six use KanjiVG revision 70a0b7ae. The strokeCount equals the number of strokes and the KANJIDIC2 count (9, 7, 7, 7, 9, 13). Ids run sequentially, and the stroke types equal the KanjiVG types.

**"The X card lists …" claims.** All verified against repo front matter:
- 湿: うるお.う and うるお.す;
- 低: ひく.い;
- 近: ちか.い;
- 軽: かろ.んじる;
- 疑: うたが.う;
- 何: なに;
- 乱: みだ.る;
- 長: なが.い;
- 洗: あら.う;
- 選: えら.ぶ;
- 抜: ぬ.く;
- 打: う.つ;
- 砂: すな.

**Diffs.** Each of the 6 diffs changes exactly one line in "How the kanji combine". No Dictionary: line is added, removed or changed.

All 8 links are relative paths `../kanji/<k>.md` to the intended new card:
- 卑 on 卑怯;
- 鼓 on 太鼓;
- 胡 on 胡椒;
- 沢 on 贅沢;
- 沙 and 汰 on 無沙汰;
- 沙 and 汰 on 御無沙汰.

The remark edit on 無沙汰 matches word-remarks.json: "None of these written characters has a card yet" became "無 does not have a card yet". kanji-titles.tsv has no row for 無, and 沙 and 汰 now have cards, so the new sentence is true.

御無沙汰 line 26 ("contains all four characters even when some do not yet have individual cards") is still true, because 無 still has no card and 御 does. Every edited passage reads naturally.

### 2. Scoped coverage

Every metadata reading has a row or is explicitly qualified. Important family words are present, or appear as unlinked rows where no article exists:
- 卑劣, 卑しい and 卑しむ;
- 淘汰;
- 沙門 and 砂;
- 光沢 and 潤沢;
- 胡散, 胡散臭い, 胡麻 and 胡蝶;
- 鼓動, 鼓舞 and 小鼓.

The notes on outside-the-table and Kanjipedia-only readings are fairly scoped:
- 卑: ひくい;
- 沙: みぎわ;
- 胡: えびす, でたらめ, みだり, ながいき and いずくんぞ;
- 汰: Daijisen's on-only entry.

### 3. Consistency and quiz safety

**Exclusions.** I judged each exclusion pair against the displayed titles. Every pair rests on a stated direct sense or gloss overlap, and the sets are not transitive cliques:
- 卑/底 rests only on "base". It is a weak but harmless over-exclusion (O2).
- 沙/汰 is declared once, on 沙, which is enough because exclusions are symmetric.

Non-excluded pairs I judged safe:
- 卑/尊 and 卑/貴 are opposites, not confusables.
- 汰/清 is likewise an opposite.
- 沙/粉, 沙/土 and 沙/泥 differ from "sand; sift".
- 沢/湖 and 沢/泉 differ from "marsh; luster".
- 胡/奇, 胡/妖, 胡/虚 and 胡/惑: none of their titles says "foreign" or "dubious".
- 鼓/鳴, 響, 奏, 器, 振, 起 and 勇: none of their titles is "drum" or "rouse". 勇 "courage; bravery" sits next to "rouse", but it describes a quality, not the act of stirring up.

**Close pairs inside the batch.** These are distinguishable or excluded:
- 汰/沙 is excluded.
- 沢/沙: "marsh; luster" and "sand; sift" differ.
- 卑/胡: "lowly; despicable" and "foreign; dubious" differ.
- 汰/沢: KANJIDIC2's "luxury" is not displayed in 汰's title.

**Distractors.** They are defensibly wrong in both directions, and none of their readings gives the answer away:
- 卑: 勇 ゆう, 賢 けん, 鋭 えい.
- 汰: 縫 ほう, 磨 ま, 塗 と.
- 沙: 鉄 てつ, 銅 どう, 塩 えん.
- 沢: 岩 がん, 丘 きゅう.
- 胡: 甘 かん, 柔 じゅう, 静 せい.
- 鼓: 筆 ひつ.

**Reading audits.** The accounting holds. The only latent collision is 沢 さ, a KANJIDIC2 name reading offered by 作 再 左 差 査 沙 砂 茶. It cannot be drawn in the production pools. The extra readings come from the okurigana scan:
- 卑: ひ.わい (卑わい 1482840);
- 汰: ゆ.る (汰る 1584980, an out-dated kanji usage);
- 鼓: こ.す and こ.する (鼓す 2450760, 鼓する 2450770).

These are real and were passed in correctly.

**Format.** Section order and headings follow content-format.md.

### 4. Comprehensibility

Each card puts the central idea first and explains its jargon (外, ▽, 人名用漢字, ateji, usually-kana). Readings are given in kana, and the mnemonics are concrete. The Notes on exclusions are dense, but they are reference material placed after the teaching core.

## Findings

No established defects.

## Optional

- **O1 (polish, facet 3; 胡.md line 13).** The distractors 甘 "sweet; pamper", 柔 and 静 (softness and quietness) are defensibly wrong, but they are so far from "foreign; dubious" that the set teaches little. A distractor nearer in register, still clearly different, would make a better quiz. Examples: 古 (also a shape component of 胡) or 貴 "precious; esteem".
- **O2 (polish, facet 3; 卑.md lines 14 and 53).** The 卑/底 exclusion rests only on the English word "base" shared by KANJIDIC2/JMdict and 底's title. "Bottom; base" is unlikely to be picked as an answer for "lowly; despicable". Keeping it is harmless; dropping it would also be defensible.
- **O3 (polish, facet 3; 卑.md line 14).** 醜 "ugly; unsightly" is a borderline disparaging neighbour of "lowly; despicable". I judge it distinguishable, so no exclusion is needed; this is noted only for awareness.
- **O4 (polish, facet 4; words\御無沙汰.md line 26, not changed in this batch).** "Even when some do not yet have individual cards" is still true, but only 無 now lacks a card. Wording that mirrors the new 無沙汰 sentence would be more precise. This is optional, because the line is outside the diff.

## Limits

- Public-web verification was limited to one live jisho.org kanji page (胡). Every other dictionary check used the packet's pinned extracts of JMdict, KANJIDIC2, Kanjipedia, Digital Daijisen and the Joyo PDF. Those extracts state their retrieval, and I assumed they faithfully represent the live sources.
- I did not open evidence\audits\quiz-safety.txt, evidence\kanjivg-svgs.txt or evidence\app-code\. For quiz safety I relied on the summary in mechanical-checks.md and the reading-audit extracts. For the mnemonics I relied on kanjivg-components.txt, which states that it was generated from those SVGs.
- jmdict-families.xml, kanjidic2-records.xml and the title TSVs were read through targeted extraction, not in full.
- Android JVM tests and the Kotlin cross-check were not run at this snapshot. This is a known limit of the packet and is not reported.
- Assumption: content-format.md does not prohibit a sourced non-KANJIDIC2 kun row such as 沙's いさご when the row is labelled as not quizzed.
- Every assistant response contained exactly one tool call.
