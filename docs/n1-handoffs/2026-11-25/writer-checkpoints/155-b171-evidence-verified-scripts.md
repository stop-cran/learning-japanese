<overview>
This session runs the only sequential authoring stream for the remaining N1 kanji in stop-cran/learning-japanese #60. The coordinator session "N1 kanji" (id 60266d87-4e3d-4c12-86b1-ef1e81f912a4) relayed two user instructions:
- "Ok, great, please go on with the remaining N1 kanji work. Keep iterating batches until its completed."
- "If you see any unverifiable claims in cards, try to drop them and rethink, then repeating the review. For clashed cards, try to generate one card looking at the both and repeat the review."

Each batch of at most 10 kanji goes through these stages:
1. Draft.
2. Blind serial reviews in separate original sessions: Claude (correctness), then GPT (consistency/quiz safety), then Grok (comprehensibility of new words).
3. Fixes, confirmed in the same reviewer sessions.
4. Integration with origin/main and revalidation.
5. Signed content and receipt commits as stop-cran.
6. Verification of both CI/ZIP receipts.
7. A #60 checkpoint and a recount.

Gates are never relaxed and drafts are never counted. There are no competing writers, writer subagents or scheduled workflows. Autopilot is on.
</overview>

<history>
1. **Earlier segments**
   - Published B169, the retained-N2 reverse-link correction, and B170 (content bb6d6682, receipt beca991c), verifying both ZIPs each time.
   - Recount after B170: 728 delivered (722 N1 + 6 N2), 500 missing. Checkpoint: https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7152185324.
   - Chose B171: 戒 戯 扉 扶 抄 把 抑 披 抹 plus 露 (source row 1177, pulled forward for 披露). 拐 moves to B172.
   - Prepared membership and strokes, gathered all evidence, settled the card plan, and studied the format and audit rules.

2. **This segment** (still read-only; no repo changes)
   - Re-read the cleaned Daijisen character entries (b171-dj*.json) and wrote down the exact sense wording below.
   - Re-ran JMdict lookups for all main, related and kun words (output in ..\b171-x.json and ..\b171-x2.json). Full senses and tags are below.
   - Surveyed the existing word-tag vocabulary and the titles/quiz_exclusions of the comparison words.
   - Re-read the full b170_render.py (149 lines; copy it with the B171 changes) and the b170_content.py header/format.
   - Inspected the Common words, Notes and Metadata of the constituent cards 警 握 暴 曲 養 本 制 茶. Line formats and Metadata shapes are below.
</history>

<work_done>
**Worktree:** `C:\Users\romanko\n1-kanji-workspace\b171-wt` (branch n1-b171; HEAD = base beca991c03d66578b2abccce7f29de1c4a2ab983).

**Uncommitted in the worktree:**
- docs/n1-sources/batch-171-membership.json (new)
- strokes/{戒,戯,扉,扶,抄,把,抑,披,抹,露}.json (new, verified)

**Session files dir:** `C:\Users\romanko\.copilot\session-state\22102645-7498-4a81-9366-de9377e0695a\files\`
- Present: b170_content.py, b170_render.py, b169_render.py, n1_gates.py, b170_close/panel/publish/followup.py, b171_strokes.py, b171_lookup.py.
- b171_lookup.py usage: `python b171_lookup.py "w1,w2" out.json`; it verifies the JMdict sha first.
- **NOT YET WRITTEN:** b171_content.py and b171_render.py.

**Status:**
- [x] Evidence, plan, format study, audit-rule study, constituent card inspection
- [ ] Write b171_content.py (NEXT, immediately)
- [ ] Write b171_render.py
- [ ] Run render → validate → build_manifest → audit → gates → signed draft commit
- [ ] Reviews → closure → integration → publication → ZIP verification → checkpoint → recount (target 738 delivered / 490 missing)
- [ ] B172 onward
</work_done>

<technical_details>
### b170_render.py structure (copy to b171_render.py)

Overall flow:
- Imports `words, cards, chars, EXC, EXTRA_MAP` from the content module.
- Asserts the cwd name and BASE, then loads `../bNNN-readings.json`, the membership, and the source index.
- Asserts the member list, then runs the JMdict iterparse into `forms` and `families`.
- Helpers: `original`, `read`, `edit`, `addline`, `cite`, `head`, `sensecount`, `mapping`.
- Main loop per card: builds the word file, the kanji card body, readings table, common words, proj, labels and Metadata line.
- Supp rows: for each other constituent ch not in members, it appends `{**maps[-1-len(EXTRA_MAP.get(c,[]))],'kanji':ch}` and calls `addline(ch,…)`.
- Then the constituent Metadata pass uses `meta_scan.scan` with PICK.
- Then notes, acc and the ledger are written to `batch-NNN-progress.json` and `batch-NNN-jmdict-selection.json`.
- XML: `extract(raw,h,sorted(ids))`.
- Write-out preserves CRLF if the base file had CRLF.

Key code fragments:
- `fmt(t,d)` replaces `@X` with a kanji link and `&word` with a word link, relative to folder d.
- `cite(t,pre)` finds JMdict ids for every multi-char token. It prints `CHECK v ids` for ambiguous tokens; add these to FIX.
- `mapping` asserts:
  - no ke_inf or re_inf;
  - re_restr is compatible;
  - `len(senses)==len(e.findall('sense'))`. B171 must bypass this for PARTIAL 戯曲 (senses [1] of 2).
- Kanji frontmatter: `kanji, title, jlpt: 1, tags [jlpt-n1, grade-N, structure-unclassified], strokes, radical, radicalNumber, onyomi, kunyomi, quizOnyomi, quizKunyomi, distractors, quiz_exclusions`.
- Body:
  - `# c — title`
  - the `**Strokes:** … · **Key (radical):** … · **JLPT:** N1 (community list)` line
  - `## Meaning and origin`, then intro and `**Shape mnemonic, not etymology:** cue`
  - `## Readings` table, `## Common words`, `## Notes`
  - the Metadata line: `[KANJIDIC2](kd), frozen 2026-11-02; [Kanjipedia, c](url); [JMdict](jm), entries …`
- Word frontmatter: `word, reading, title, type, kanji [..], tags [kind, tags], quiz_exclusions`.
- Word body sections:
  - `# w (y) — gloss`
  - `## Meaning` (intro plus two bullet examples)
  - `## How the kanji combine`
  - `## Synonyms and antonyms`
  - `## Distinctive meaning`
  - the `Dictionary: [JMdict](jm), entry eid, sense(s) sensestr{EXTRA}; [Digital Daijisen, w](weblio).` line
- The final assert checks that each output file is either new or matches the original (base) content.
- In b170 the changes assert requires every change to be under kanji/. **B171 must also allow words/悪戯.md.**

### B171 render changes (decided)

- `r.name=='b171-wt'`; BASE beca991c…; `../b171-readings.json` (dict with on, kun, outside, url; use `km[c]['url']`); batch-171-membership.json; tmp `../b171-scan`; batch '171'.
- Member assert: `[k for k in absent if int(source[k]['grade'])<=8][:9]+['露']`, plus `'露' in absent and int(source['露']['grade'])==8`.
- Remove the kanqual assert.
- Add 1151580 to `primary`.
- **FIX:** `{'悪戯':'1151580','露':'1560070','把':'1607320','抑える':'2836285','助ける':'1344410','戯れる':'1224970','戒め':'1609250'}`. Extend it as CHECK prints appear.
- **EXTRA**

| Word | Appended text |
|---|---|
| 扶養 | `'; 扶養家族, entry 1690990'` |
| 抄本 | `'; 戸籍抄本, entry 1651120; 戸籍謄本, entry 1651110; 謄本, entry 1450020'` |
| 披露 | `'; 披露宴, entry 1483500; 疲労, entry 1483780'` |
| 扉 | `'; 門扉, entry 1536270'` |

- **EXTRA_MAP:** `{'露':[('披露','ひろう','1483490','ロウ')]}`. The 暴 supp row uses index -1-len(EXTRA_MAP) (the main mapping comes first, then the extras), which is correct.
- **PARTIAL `{'戯曲':[1]}`:** skip the sense-count assert and add the note "JMdict sense 2 'Chinese opera' not taught."
- **Word-exclusion existence:** allow `k in words`.
- Add asserts that every @X is an existing kanji or a member, and every &w is an existing word or a new word.
- **Manual 戯→悪戯 row:**
  ```
  dict(kanji='戯',article='words/悪戯.md',newArticle=False,primaryReading='いたずら',entryIds=['1151580'],senseNumbers=[1,2,4,5],priorityTags=['ichi1'],readingPriorityTags=['ichi1'],note='Existing N3 identity/reading/title/type preserved. Whole-word jukujikun; no allocation of いたずら to 戯. New kanji common-word row reciprocates the required activated baseline pair.')
  ```
  - Verify the tags from families: the k_ele 悪戯 has ke_pri ichi1, and the reading いたずら has re_pri ichi1 plus re_inf gikun.
  - Sense 3 is humble pastime and was excluded. Sense 5 (euphemistic lewd) is in the plan list [1,2,4,5]; reconsider whether to list [1,2,4] only. It must match the senses the existing article teaches, so check words/悪戯.md.
- **戯 Common words:** add `- [悪戯](../words/悪戯.md) いたずら — mischief; prank; a whole-word reading, usually written いたずら; do not assign parts of いたずら to 戯`.
- **Edit words/悪戯.md** (CRLF): `and 戯 suggests play.` → `and [戯](../kanji/戯.md) suggests play.`

### Constituent card edits (exact current lines; all LF)

| Card | Edits |
|---|---|
| 警 | Table row `| ケイ | on | 警官 けいかん — police officer; 警戒 けいかい — vigilance |`: replace `警戒 けいかい — vigilance` with `[警戒](../words/警戒.md) けいかい — vigilance`. CW `- 警戒 けいかい — being on guard` → `- [警戒](../words/警戒.md) けいかい — being on guard`. |
| 握 | CW `- 把握 はあく - grasp; understanding` → `- [把握](../words/把握.md) はあく - grasp; understanding` (hyphen style). |
| 暴 | Table `| バク | on | 暴露 ばくろ - disclosure; revelation |` → link 暴露. CW `- 暴露 ばくろ - disclosure; revelation` → link. |
| 曲 | CW lines use —; addline 戯曲. |
| 本 | CW lines use —; addline 抄本. |
| 制 | CW lines use —; addline 抑制. |
| 茶 | CW lines use —; addline 抹茶 (after `- 茶道 さどう — the Way of Tea`). |
| 養 | CW lines use —; addline 扶養. |

**Metadata states**

| Card | Current Metadata | Planned action |
|---|---|---|
| 警 | No Metadata line; ends `Dictionary: [JMdict](…), entries 1252330, 1252360, 1252310.` | 警戒 1252310 is already there. Add a new `\n\nMetadata: Word pairs: {JM}, entries {lst}.` line only if the scan finds gaps. b170 asserted `len(ml)==1`, so B171 must handle zero Metadata lines by appending a new line. |
| 握 | Multi-line wrapped Metadata; first line `Metadata: [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project),`; ids 1152720, 1152730, 1152660, 1152750 and 1470910 sit on continuation lines. | Append ` Word pairs: {JM}, entries {lst}.` to the first line (meta_scan reads only the first line), or append a new Metadata line at the end. |
| 暴 | One-line Metadata ending `Word pairs: [JMdict](…), entries 1519330, 1519340, 1519590, 1549100, 1601280.` | Extend via the entries regex if there are gaps. |
| 養 | One long Metadata line with "entries 1228100 … 1213140 (the last three from …)"; it does not match `entries (\d{7}(?:, \d{7})*)\.`. | Append ` Word pairs: {JM}, entries {lst}.` to it. |
| 曲, 本, 制, 茶 | No Metadata line. | Append a new line. |

- The b170 assert `'Word pairs' not in t` would fail for 暴. Relax it to: if 'Word pairs' is present, use the regex-extension path.

Expected gaps from the earlier scan:

| Card | Gap ids |
|---|---|
| 曲 | 1239730, 1239740 |
| 本 | 1582710 1523060 1523180 1328390 1755110 1464780 1166600 2005520 1301640 2005490 2005500 1561550 2005510 1583120 1335130 |
| 制 | 1374880 1223010 1409550 |
| 茶 | 1422720 1002430 1280770 1422770 |
| 警 | 1252330 1252360 1252310 |

Ambiguous gaps need PICK entries.

### JMdict facts (verified this segment)

**Main supports**

| Word | Entry | Tags | Senses |
|---|---|---|---|
| 警戒 | 1252310 | ichi1/news1 | 1: vigilance; caution; alertness; precaution; being on guard |
| 戯曲 | 1225010 | ichi1/news1 | 1 drama; play; 2 Chinese opera |
| 扉 | 1483380 | ichi1/news1; 闔 is a rarely used form | 1 door; gate; opening; 2 title page |
| 扶養 | 1496990 | ichi1/news1 | support (e.g. of one's dependents); maintenance |
| 抄本 | 1349540 | news2/spec2; 鈔本 is a rarely used form | excerpt; abridgment; book of selections |
| 把握 | 1470910 | news1 | grasp (of the situation, meaning, etc.); understanding; control; hold; grip |
| 抑制 | 1547290 | ichi1/news1 | control; restraint; suppression; constraint; curtailment; inhibition; check; curb |
| 披露 | 1483490 | news1 | announcement; presentation; demonstration; displaying; showing; introducing; unveiling; revealing; performing |
| 抹茶 | 1525220 | news2/spec2; まっ茶 and 末茶 are search-only | matcha; powdered green tea |
| 暴露 | 1601280 | ichi1/news1; 曝露 also listed | disclosure; exposure; revelation |
| 悪戯 | 1151580 | ichi1 | 5 senses, all uk. 1 mischief/prank; 2 mischievous (adj-na); 3 hum. pastime; 4 playing with/tampering; 5 euph. lewd behaviour. The reading いたずら is ichi1 + gikun; イタズラ is also listed. |

**Kun and other words**

| Word | Entry | Tags | Gloss / notes |
|---|---|---|---|
| 戒める | 1200650 | ichi1/news2 | warn against; admonish; prohibit |
| 戒め | 1609250 | ichi1/news2 | caution; admonition; lesson |
| 戯れる | 1224970 | ichi1 | readings たわむれる ichi1 and ざれる untagged; to be playful/frolic/joke; flirt |
| 戯れ | 1224960 | ichi1/news2 | — |
| 戯れる (じゃれる) | 2859078 | untagged | uk; play around (of a cat, dog) |
| 戯作 | 1577840 | untagged | readings げさく and ぎさく |
| 戯れ言 | 1756640 | untagged | ざれごと |
| 助ける | 1344410 | ichi1/news1 | 扶ける is a rarely used kanji form |
| 把 | 1607320 | ichi1/news2 | reading わ (also ば, ぱ); counter for bundles |
| 一把 | 1165640 | untagged | いちわ; bundle |
| 束 | 1404450 | — | also lists 把 as たば |
| 抑える | 2836285 | ichi1/news1 | keep within limits; restrain; hold back; xref 押さえる sense 6 |
| 抑え | 1613650 | news1 | also written 押さえ |
| 押さえる | 1589080 | — | existing card: title "hold down; secure; grasp" |
| 露 (つゆ) | 1560070 | ichi1 | dew; tears; (not) at all |
| 夜露 | 1537230 | untagged | よつゆ, やろ |
| 露 (ろ) | 1147330 | — | abbreviation: Russia |
| 露 (あらわ) | 1560080 | — | — |
| 門扉 | 1536270 | news1 | — |
| 開扉 | 1202900 | untagged | — |
| 鉄扉 | 1854520 | — | — |
| 回転扉 | 1976370 | — | — |
| 扶助 | 1496980 | ichi1/news1 | — |
| 扶養家族 | 1690990 | untagged | one's dependents |
| 扶養控除 | 1691000 | — | — |
| 扶持 | 1496970 | — | historical |
| 戸籍抄本 | 1651120 | untagged | — |
| 戸籍謄本 | 1651110 | spec1 | — |
| 謄本 | 1450020 | news2/spec2 | — |
| 抄録 | 1349560 | news2/spec2 | — |
| 抄訳 | 1349550 | untagged | — |
| 原本 | 1262360 | news1 | — |
| 写本 | 1322160 | news2 | — |
| 抜粋 | 1601310 | ichi1/news2 | — |
| 掌握 | 1349660 | news1 | — |
| 把持 | 1470920 | untagged | — |
| 十把一絡げ | 1745110 | — | — |
| 抑圧 | 1547270 | ichi1/news1 | — |
| 抑止 | 1547280 | ichi1/news1 | — |
| 抑揚 | 1547300 | ichi1/news2 | — |
| 披露宴 | 1483500 | ichi1 | — |
| 疲労 | 1483780 | ichi1/news1 | same reading ひろう as 披露 |
| 披瀝 | 1483480 | news2/spec2 | — |
| 煎茶 | 1391530 | news2 | xref 抹茶 |
| 薄茶 | 1690520 | — | — |
| 濃茶 | 2142940 | — | — |
| 点てる | 2410820 | — | — |
| 茶の湯 | 1422610 | news2/spec2 | — |
| 茶道 | 1422770 | ichi1/news1 | — |
| 一抹 | 1166790 | news2/spec2 | — |
| 抹消 | 1525200 | ichi1/news2 | — |
| 抹殺 | 1525190 | news2/spec2 | — |
| 露出 | 1560130 | news2/spec2 | — |
| 暴露本 | 2641090 | — | — |
| 警戒心 | 1252320 | untagged | — |
| 厳戒 | 1262560 | news2/spec2 | — |
| 戒律 | 1200700 | news2/spec2 | — |
| 遊戯 | 1542190 | news2/spec2 | — |
| 児戯 | 1315020 | — | — |
| 戯画 | 1224990 | news2/spec2 | — |

**Avoid:** 戯言 (ambiguous; it is search-only under 1756640) and 朝露.

### Daijisen character senses (verbatim table removed from this public copy)

This section held the verbatim Digital Daijisen character entries (the ten members 戒 戯 扶 抄 把 抑 披 抹 露 扉 and the constituents 警 養 制 曲 本 茶 握 暴) as checked on Weblio. It was removed from the handoff copy because it reproduced whole dictionary entries. Re-fetch an entry when authoring with `python n1_batch_tool.py webcheck <kanji...> --out <dir>` (see `code/lean/n1cmds.py`) and quote only a short clause, as the shipped cards do. Checkpoint 156 lists the short key clauses the plan relies on.

### Daijisen word texts (verbatim table removed from this public copy)

This section held the verbatim Digital Daijisen word bodies for 戯曲 扉 扶養 把握 抑制 披露 暴露 抹茶 門扉 警戒 抄本 戒める 抑える じゃれる たわむれる, removed from the handoff copy because it reproduced whole dictionary entries. Re-fetch a word with `python code/lean/webtest.py <word>` (prints the Weblio Digital Daijisen block) and quote only a short clause, as the shipped cards do.

### Member metadata

| Kanji | Onyomi | Kunyomi | Strokes | Radical | Notes |
|---|---|---|---|---|---|
| 戒 | カイ | いまし.める | 7 | 戈 | — |
| 戯 | ギ, ゲ | たわむ.れる, ざ.れる, じゃ.れる | 15 | 戈 | Kanjipedia lists ゲ and ざ.れる outside standard use |
| 扉 | ヒ | とびら | 12 | 戶 | — |
| 扶 | フ | たす.ける | 7 | 手 | たす.ける is outside standard use |
| 抄 | ショウ | none | 7 | 手 | — |
| 把 | ハ, ワ | none | 7 | 手 | — |
| 抑 | ヨク | おさ.える | 7 | 手 | — |
| 披 | ヒ | none | 8 | 手 | — |
| 抹 | マツ | none | 8 | 手 | — |
| 露 | ロ, ロウ | つゆ | 21 | 雨 | — |

All are grade 8. Kanjipedia URLs are in b171-readings.json.

### Card plan

| Kanji | Word | Reading | Entry | Selected | Title | Distractors | Exclusions |
|---|---|---|---|---|---|---|---|
| 戒 | 警戒 | けいかい | 1252310 | カイ | guard against; admonish | 械成戦 | 警慎禁律注守懲訓備衛護 |
| 戯 | 戯曲 | ぎきょく | 1225010 | ギ | play; jest; drama | 虚戦成 | 遊劇娯興楽演笑奏弾幕芸 |
| 扉 | 扉 | とびら | 1483380 | とびら | door; title page | 非悲俳 | 戸門窓関開閉隣 |
| 扶 | 扶養 | ふよう | 1496990 | フ | help; support | 夫技失 | 助援支養補佐救護丞賛 |
| 抄 | 抄本 | しょうほん | 1349540 | ショウ | excerpt; extract | 少妙秒 | 抜略写録要訳選粋抽択 |
| 把 | 把握 | はあく | 1470910 | ハ | grasp; bundle | 色拝抗 | 握持取束捕執抱括柄 |
| 抑 | 抑制 | よくせい | 1547290 | ヨク | restrain; hold down | 仰迎柳 | 圧押制止縛禁防節 |
| 披 | 披露 | ひろう | 1483490 | ヒ | open; reveal | 被波彼 | 示発表展開現告顕露呈宣掲爆剖 |
| 抹 | 抹茶 | まっちゃ | 1525220 | マツ | rub out; powder | 未味株 | 消削除擦塗粉殺末摩磨 |
| 露 | 暴露 | ばくろ | 1601280 | ロ | dew; expose | 路霧雪 | 顕裸呈浴披滴 |

Every distractor and exclusion must be @-mentioned in the chars notes with its meaning.

### Word frontmatter

| Word | Title | Kind | Tags | Senses | Exclusions |
|---|---|---|---|---|---|
| 警戒 | vigilance; being on guard | kango | 'noun, suru-verb, safety' | '1' | 用心 注意 警告 警備 予防 油断 気を付ける 慎重 |
| 戯曲 | play (drama); script | kango | 'noun, arts' | '1' (PARTIAL) | 演劇 劇 芝居 ドラマ 小説 物語 文学 作品 原稿 劇場 舞台 悲劇 作家 |
| 扉 | door; title page | wago | 'noun, home' | '1–2' | ドア 戸 門 玄関 入口 出入口 ページ 題名 表紙 戸棚 窓 |
| 扶養 | supporting dependents | kango | 'noun, suru-verb, family' | '1' | 世話 援助 支える 育てる 面倒 助ける 育児 生活 |
| 抄本 | excerpt; abridged copy | kango | 'noun, writing' | '1' | 写す 複写 コピー 要旨 あらすじ 記録 原稿 要点 |
| 把握 | grasp; understanding | kango | 'noun, suru-verb, thinking' | '1' | 理解 分かる 掴む 握る 心得る 捕える 押さえる 握手 |
| 抑制 | restraint; control | kango | 'noun, suru-verb, behavior' | '1' | 制限 我慢 こらえる 防止 調節 管理 支配 ブレーキ 限度 押さえる |
| 披露 | presenting; showing; announcement | kango | 'noun, suru-verb, communication' | '1' | 発表 公表 紹介 見せる 示す 演技 演奏 発揮 宣伝 現す 表す 暴露 |
| 抹茶 | matcha; powdered green tea | kango | 'noun, drinks' | '1' | 茶 お茶 紅茶 粉 緑 喫茶店 |
| 暴露 | disclosure; exposure | kango | 'noun, suru-verb, information' | '1' | 発表 公表 現す 表す 発見 秘密 隠す 披露 |

Existing tag vocabulary includes safety? (not seen in the top 150), family, writing, communication, behavior, arts, home, thinking? (not seen), drinks? (food is common). Confirm or choose existing tags: e.g. "food" instead of "drinks", "attention" or "society" instead of "safety", "information" → "media"/"communication", "thinking" → "perception"/"learning". Tags seen include: food, communication, family, writing, behavior, arts, home, media, attention, books, literature, art, rules, society, government, culture, daily-life, household, emotion, feelings, perception.

Existing comparison-word titles:

| Word | Title | Existing quiz_exclusions |
|---|---|---|
| 押さえる | hold down; secure; grasp | 押す 掴む 握る 捕まえる 持つ 止める 理解 分かる 予約 我慢 |
| 助ける | help; save | — |
| 警告 | warning; caution | — |
| 警備 | guarding; security | — |
| 用心 | caution; precaution | — |
| 注意 | attention, caution | — |
| 油断 | carelessness; letting one's guard down | — |
| 演劇 | theatre; drama | — |
| 芝居 / 劇 | play; drama | — |
| 冗談 | joke; jest | — |
| ドア | door | — |
| 戸 | door; especially a traditional door | — |
| 門 | gate | — |
| 表紙 | book cover; binding | — |
| 世話 | care; assistance | — |
| 援助 | aid; assistance; support | — |
| 写す | copy; photograph | — |
| 要旨 | gist; main points; abstract | — |
| 理解 | understanding | — |
| 握る / 掴む | grasp; grip / grasp; seize | — |
| 制限 | restriction; limit | — |
| 我慢 | endurance; self-restraint | — |
| 発表 | announcement; presentation | — |
| 紹介 | introduction; referral | — |
| 公表 | official public announcement | — |
| 秘密 | secret; secrecy | — |
| 隠す | hide; conceal | — |
| お茶 / 茶 / 紅茶 | tea / tea / black tea | — |

### Example sentences (each needs a kana reading and an English translation)

| Word | Example A | Example B |
|---|---|---|
| 警戒 | 大雨の予報が出ているので、川の近くの住民は警戒している。 | その猫は知らない人を警戒して、なかなか近づかない。 |
| 戯曲 | この作家は、小説だけでなく戯曲も書いている。 | 学生たちは、有名な戯曲を自分たちで上演した。 |
| 扉 | 会議室の扉を静かに閉めた。 | 本の扉に、作者のサインがあった。 |
| 扶養 | 彼は働きながら、年老いた母を扶養している。 | 彼には扶養家族が三人いる。 |
| 抄本 | 市役所で戸籍抄本を一通取ってきた。 | これは長い物語の一部だけを書き写した抄本だ。 |
| 把握 | まず、現場の状況を正確に把握する必要がある。 | 新しい部長は、部下一人一人の仕事をよく把握している。 |
| 抑制 | 政府は物価の上昇を抑制するための対策を発表した。 | 彼女は感情を抑制して、冷静に話し続けた。 |
| 披露 | 結婚式で、友人たちが歌を披露した。 | 新しい製品は、来月の展示会で披露される予定だ。 |
| 抹茶 | 京都のお店で、抹茶と和菓子を楽しんだ。 | 最近は、抹茶味のアイスやケーキも人気がある。 |
| 暴露 | 元社員が、会社の不正を週刊誌に暴露した。 | その本には、有名な政治家の秘密が暴露されている。 |

### Unselected readings (`other` dict)

| Kanji | Reading | Shown words | Entry ids | Note |
|---|---|---|---|---|
| 戒 | いまし.める | 戒める (いましめる) / 戒め (いましめ) | '1200650 1609250' | — |
| 戯 | ゲ | 戯作 (げさく; JMdict also gives ぎさく) | '1577840' | outside standard use |
| 戯 | たわむ.れる | 戯れる / 戯れ | '1224970 1224960' | — |
| 戯 | ざ.れる | ざれる reading of 戯れる (untagged); 戯れ言 ざれごと | '1224970 1756640' | outside standard use |
| 戯 | じゃ.れる | じゃれる | '2859078' | usually kana |
| 扉 | ヒ | 門扉 (もんぴ) / 開扉 (かいひ) | '1536270 1202900' | — |
| 扶 | たす.ける | 扶ける | '1344410' | rarely used form of 助ける; outside standard use; possibly a source-only-ish qualification |
| 把 | ワ | 一把 (いちわ) | '1165640' | Joyo note: 「把（ハ）」は，前に来る音によって「ワ」，「バ」，「パ」になる。 Daijisen わ counter. |
| 抑 | おさ.える | 抑える / 抑え | '2836285 1613650' | — |
| 露 | つゆ | 露 (つゆ) / 夜露 (よつゆ) | '1560070 1537230' | — |

### Joyo rows (PDF pages)

| Kanji | Page | Readings and examples |
|---|---|---|
| 戒 | 23 | カイ 戒心 戒律 警戒 / いましめる 戒める 戒め |
| 戯 | 34 | ギ 戯曲 遊戯 児戯 / たわむれる 戯れる 戯れ |
| 扉 | 130 | ヒ 開扉 門扉 / とびら |
| 扶 | 133 | フ 扶助 扶養 扶育 |
| 抄 | 79 | ショウ 抄録 抄本 抄訳 |
| 把 | 124 | ハ 把握 把持 一把（ワ）三把（バ）十把（パ） |
| 抑 | 153 | ヨク 抑圧 抑制 抑揚 / おさえる 抑える 抑え ⇔ 押さえる |
| 披 | 130 | ヒ 披見 披露 直披 |
| 抹 | 145 | マツ 抹殺 抹消 一抹 |
| 露 | 160 | ロ 露出 露店 雨露 / ロウ 披露 / つゆ 露 夜露 |
| 暴 | 143 | — |

### Shape cues

| Kanji | Cue |
|---|---|
| 戒 | @械 contains 戒; @戦 shares 戈 |
| 戯 | left as in @虚, plus the right of @戦 |
| 扉 | @戸 over @非 |
| 扶 | 扌 + @夫 |
| 抄 | 扌 + @少 |
| 把 | 扌 + the bottom of @色 |
| 抑 | right as in @仰/@迎; compare @柳 |
| 披 | 扌 + @皮 (check that 皮 has a card before @-linking); @被 and @波 share 皮 |
| 抹 | 扌 + @末 (vs @未); compare @味 and @株 |
| 露 | @雨 over @路 |

### Kanji with no card (never @-link)
頁 摘 控 鎮 謄 巴 肥 戈 廾 卬 虍 曝 闔 鈔 碾 扌.

### Word cards
- **Exist (linkable with &):**
  - 用心 注意 警備 警告 油断 警察 予防 気を付ける 慎重
  - 演劇 芝居 劇 小説 悪戯 遊ぶ 冗談 作品 劇場 舞台 ドラマ 物語 文学 作家 悲劇
  - ドア 戸 門 表紙 窓 戸棚 玄関 入口 出入口 ページ 題名
  - 世話 援助 育てる 支える 面倒 助ける 家族 生活 育児
  - 写す コピー 要旨 複写 原稿 記録 要点 あらすじ
  - 理解 分かる 握る 掴む 握手 心得る 捕える 押さえる
  - 制限 我慢 防止 調節 管理 支配 ブレーキ 限度 こらえる
  - 発表 紹介 見せる 公表 示す 演奏 演技 発揮 宣伝 現す 表す 疲れ 結婚
  - お茶 茶 紅茶 粉 緑 喫茶店
  - 秘密 隠す 発見 写真 心配 守る 防ぐ 備える 厳しい 開く 閉める 抜く
  - 内容 全部 状況 状態 意味 感情 気持ち 物価 宴会 製品 歌 味 不正 隠れる 政治家 明らか 冷静 正確 現場 政府 対策 部長 友人
- **Missing (plain text only):** 遊戯 茶道 戸籍 脚本 台本 煎茶 抑える 抑圧 監視 戒める 抜粋 要約 原本 一部 粉末 アイス 週刊誌 秘める 和菓子 展示会 上演 部下 上昇 結婚式 社員 暴力 実態 真相 茶の湯.

### Selection notes
Cover the support's tags and standard-use example status with PDF page, which constituent has a card, and which readings are shown but not offered.
- 抄本 and 抹茶 qualify via news2/spec2 under #60 comment 7112026459.
- 露: ロウ is via 披露 (in-batch); ロ is via 暴露 (暴 has a card). 暴露 is NOT a Joyo example (露出 露店 雨露 are).
- 扉 とびら: 扉 is the word itself (Joyo lists とびら).

### acc and ledger
- acc: frozenPendingRecords=1228, publishedPendingRecordsWithCards=728, publishedN1Additions=722, n2Placements=6, undelivered=500, localUnreviewedDrafts=10, notStarted=490, overallN1TaskComplete=False.
- selectionReason: "First nine absent Jōyō rows on the beca991c receipt plus 露 (source row 1177), pulled forward for 披露 so that 露's ロウ reading has a qualifying route; 拐 moves to B172. Supports qualify through JMdict ichi1, news1, spec1 or gai1, with news2 and spec2 also qualifying under issue #60 comment 7112026459."
- dictionaryChecks: list the Daijisen word bodies, the character entries and the Joyo pages above.

### Audit facts
- activated_baseline_pairs = frozen pairs ∪ baseline word files containing a member kanji. Only 悪戯 was found earlier.
- Each reading appears in the table exactly once. A selected row needs its article linked. sourceOnly rows need "source-only" in the line.
- Quiz fields must equal the projection; labels must equal the distractor titles; exactly 3 distinct distractors.
- Word quiz_exclusions must equal the wex ledger.
- reused_changes require the exact recorded edits, with no frontmatter change.

### Procedures and quirks

**Gates:** from b171-wt run
`python <files>\n1_gates.py 171 beca991c03d66578b2abccce7f29de1c4a2ab983 "戒 戯 扉 扶 抄 把 抑 披 抹 露" "警 握 暴 曲 養 本 制 茶" "警戒 戯曲 扉 扶養 抄本 把握 抑制 披露 抹茶 暴露"` (about 8 min; `ONLY=` restricts steps).

**Other commands**
- Validation: `python tools/validate.py`, `python tools/build_manifest.py`, `python tools/audit_n1_batch.py --batch 171`.
- meta_scan: `$env:N1_LEAN=(Resolve-Path ..\lean).Path`.

**Publication:** workflow 378446878; docs/n1-reviews/batch-112-publication/verify-zip.py; tools/n1_record_publication.py.

**Signing and auth:** `git -c user.signingkey=D4C9A275A218AF747B787AFA9D94B9D311BD26A7`; `$env:GH_TOKEN=(gh auth token --user stop-cran)`; Co-authored-by trailer.

**Shell quirks**
- Set `$env:PYTHONIOENCODING='utf-8'`.
- Redirect output to `..\b171-tmp.txt`, then read it with `Get-Content -Encoding utf8`. If it is over 20KB, split the print.
- The grep tool fails in worktrees, so use Python. cd does not persist. Pipe here-strings to `python -`.
- Scanning yaml over all words takes about 60s.

**Content constraints**
- No JLPT on new words. Avoid glyphs in U+2E80–2FDF and U+3400–4DBF.
- Blocked grade-9 rows; never fabricate support for them: 崚 彪 晟 燿 舜 赳 侑 嵯 怜 滉 瑚.
- Next batch, B172: 拐 拒 拓 拘 拙 拠 拳 拷 挑 据.
</technical_details>

<important_files>
- **C:\Users\romanko\n1-kanji-workspace\b171-wt**
  - The worktree.
  - The render will create 10 kanji cards, 10 word cards, batch-171-progress.json, and the jmdict selection and xml.
  - It will edit words/悪戯.md and kanji/{警,握,暴,曲,養,本,制,茶}.md.
- **files\b170_render.py** (149 lines): full render template; copy it with the B171 changes above.
- **files\b170_content.py** (34KB): content format template.
  - Lines 1–17: header and cards.
  - Lines 17–90: words.
  - Lines 91–143: chars and EXC.
- **files\b169_render.py** lines 106–121: Metadata variants.
- **files\b171_lookup.py**: JMdict lookup helper.
- **tools\audit_n1_batch.py**:
  - Lines 45–58: lexical_pair.
  - Lines 124–129: activated_baseline_pairs.
  - Lines 700–812: the main audit.
- **docs\n1-reviews\batch-137-closure\confirm-packet\gpt\evidence\meta_scan.py**: gap scanner; reads only the first Metadata line.
- **Workspace evidence** (`C:\Users\romanko\n1-kanji-workspace\`): b171-dj.json, dj2, dj3, dj4 (Daijisen), b171-gl.txt, b171-x.json, b171-x2.json (JMdict lookups), b171-readings.json, b171-joyo.txt, jmdict\JMdict_e.gz.
</important_files>

<next_steps>
1. **Write `files\b171_content.py`** with all 10 cards, EXTRA_MAP, 10 word tuples (full prose with kana and English, using the Daijisen quotes above), 10 chars tuples (intro, cue, notes and other dict), and `EXC={}`. Choose word tags from the existing vocabulary.
2. **Write `files\b171_render.py`** with all the B171 changes: PARTIAL, the 悪戯 manual row and edit, link-replacing edits for 警/握/暴, flexible Metadata handling (zero lines, multi-line 握, existing Word pairs on 暴, non-matching 養), and allowing words/悪戯.md in changes.
3. **Run and commit.** Run the render from b171-wt and fix CHECK prints and asserts. Then run validate, build_manifest, the audit and the gates until clean. Make the signed draft commit "N1 B171 draft: 戒 戯 扉 扶 抄 把 抑 披 抹 露".
4. **Review and integrate:** serial blind reviews (Claude → GPT → Grok); fixes and confirmations; closure; integration with origin/main; revalidation.
5. **Publish:** signed content and receipt commits, verify both ZIPs, post the #60 checkpoint, and recount (target 738/490).
6. **Continue** with B172 onward.
7. **Clean up** temporaries: ..\b171-tmp.txt, ..\b171-x*.json, ..\b170-scan, ..\b171-scan, and C:\Users\romanko\b170-glcheck.txt.
</next_steps>