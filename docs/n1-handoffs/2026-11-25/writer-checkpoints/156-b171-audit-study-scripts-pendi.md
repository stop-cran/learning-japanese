<overview>
This session runs the only sequential authoring stream for the remaining N1 kanji in stop-cran/learning-japanese #60. The coordinator session "N1 kanji" (id 60266d87-4e3d-4c12-86b1-ef1e81f912a4) relayed two user instructions:
- "Ok, great, please go on with the remaining N1 kanji work. Keep iterating batches until its completed."
- "If you see any unverifiable claims in cards, try to drop them and rethink, then repeating the review. For clashed cards, try to generate one card looking at the both and repeat the review."

Each batch covers at most 10 kanji and goes through these stages:
1. Draft.
2. Blind serial reviews in separate original sessions: Claude (correctness), then GPT (consistency and quiz safety), then Grok (comprehensibility of new words).
3. Fixes, confirmed in the same reviewer sessions.
4. Integration with origin/main and revalidation.
5. Signed content and receipt commits as stop-cran.
6. Verification of both CI and ZIP receipts.
7. A #60 checkpoint and a recount.

Gates are never relaxed and drafts are never counted. There are no competing writers, no writer subagents and no scheduled workflows. Autopilot is on.
</overview>

<history>
1. Earlier segments
   - Published B169, the retained-N2 reverse-link correction, and B170 (content bb6d6682, receipt beca991c). Both ZIPs were verified each time.
   - Recount after B170: 728 delivered (722 N1 + 6 N2), 500 missing. Checkpoint: https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7152185324.
   - Chose B171 = 戒 戯 扉 扶 抄 把 抑 披 抹, plus 露 (source row 1177) pulled forward for 披露. 拐 moves to B172.
   - Prepared the membership file and strokes, gathered all evidence (Daijisen, JMdict, Joyo, Kanjipedia), settled the card plan, and studied the format and audit rules.

2. This segment (still read-only; no new repo changes)
   - Read meta_scan.py in full. scan() reads only the first `Metadata:` line's 7-digit ids and checks every Japanese run of 2+ characters containing a kanji against JMdict spellings.
   - Read n1_gates.py, which runs these steps: unittest, validate, budget, grammar, audit, quiz_safety, reading_exposure, reading_options, lint, meta_scan, word_quiz, then a manifest-freshness check.
   - Read b169_render.py's Metadata variants. When a card already has a Metadata line, the variant appends ` Word pairs: {JM}, entries {lst}.` to it. Otherwise it appends `\n\nMetadata: Word pairs: {JM}, entries {lst}.` after the last line.
   - Re-checked the source-index metadata for all 10 members (all match the plan), the word inventory (the missing list is below) and the B170 published card format (慈善.md, 慈.md).
   - Viewed b170_content.py (format) and the full b170_render.py (149 lines).
   - Read words/悪戯.md: it teaches senses 1-2, 4-5, so the manual mapping senseNumbers [1,2,4,5] is correct. It is the only baseline word containing a member kanji.
   - Fetched titles and readings for every distractor and exclusion kanji. All have cards except 戈.
   - Read audit_n1_batch.py lines 119-135 and 701-812, the main audit (details in Technical details).
</history>

<work_done>
**Worktree:** `C:\Users\romanko\n1-kanji-workspace\b171-wt`, branch n1-b171, HEAD = base beca991c03d66578b2abccce7f29de1c4a2ab983.

**Uncommitted in the worktree:**
- `docs/n1-sources/batch-171-membership.json` (new)
- `strokes/{戒,戯,扉,扶,抄,把,抑,披,抹,露}.json` (new, verified)

**Session files dir:** `C:\Users\romanko\.copilot\session-state\22102645-7498-4a81-9366-de9377e0695a\files\`
- Present: b170_content.py, b170_render.py, b169_render.py, n1_gates.py, b170_close/panel/publish/followup.py, b171_strokes.py, b171_lookup.py.
- b171_lookup.py usage: `python b171_lookup.py "w1,w2" out.json`. It verifies the JMdict sha first.
- **Not yet written:** b171_content.py and b171_render.py.

**Checklist:**
- [x] Evidence, plan, format study, audit-rule study, constituent card inspection, distractor title fetch
- [ ] Write b171_content.py (next, immediately)
- [ ] Write b171_render.py
- [ ] Run render → validate → build_manifest → audit → gates → signed draft commit
- [ ] Reviews → closure → integration → publication → ZIP verification → checkpoint → recount (target 738 delivered / 490 missing)
- [ ] B172 onward
</work_done>

<technical_details>
### b170_content.py format (copy for B171)

**Header**

```
from urllib.parse import quote
JOYO='https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf'
def W(s):return 'https://www.weblio.jp/content/'+quote(s)
```

**Structures**

- `cards=[(c, word, reading, eid, selectedReading, title, 'distractors3', 'exclusions'),...]`
- `EXTRA_MAP={kanji:[(word,reading,eid,selReading)]}`
- `words={w:(gloss, kind, 'tags', [exclusions], 'sensestr', intro, exampleA, exampleB, formText, synText, distinctText)}`
- `chars={c:(intro, cue, notes, {reading:(shownText, 'eid eid')})}`
- `EXC={}`

**Text style**

- `@X` renders a kanji link; `&w` renders a word link.
- Daijisen quotes use the form 日本語 (かな), “English.”
- Example bullets use the form `日本語。 (かな。) — English.`
- Use curly quotes “ ” and ’.
- Notes must @-mention every distractor and exclusion with its meaning, and cite `[standard-use table, PDF p. N]({JOYO}#page=N)` with its readings and examples.
- Source-only readings must contain "source-only" in the shown text.

### b170_render.py (149 lines) → b171_render.py changes

- Change the import to b171_content.
- Set `r.name=='b171-wt'`, BASE beca991c03d66578b2abccce7f29de1c4a2ab983, `../b171-readings.json` (dict with on, kun, outside, url; use `km[c]['url']`), batch-171-membership.json, tmp `../b171-scan`, and batch '171' throughout (ledger file names, xml, selection).
- Member assert: `[k for k in absent if int(source[k]['grade'])<=8][:9]+['露']`, plus `'露' in absent and int(source['露']['grade'])==8`.
- Remove the kanqual collection and assert.
- `primary` must include 1151580 so that 悪戯's family is loaded.
- **FIX** `{'悪戯':'1151580','露':'1560070','把':'1607320','抑える':'2836285','助ける':'1344410','戯れる':'1224970','戒め':'1609250'}`. Extend it as `CHECK` prints appear.
- **EXTRA** (replace the B170 dict)

| Word | Appended text |
|---|---|
| 扶養 | `'; 扶養家族, entry 1690990'` |
| 抄本 | `'; 戸籍抄本, entry 1651120; 戸籍謄本, entry 1651110; 謄本, entry 1450020'` |
| 披露 | `'; 披露宴, entry 1483500; 疲労, entry 1483780'` |
| 扉 | `'; 門扉, entry 1536270'` |

- **EXTRA_MAP** `{'露':[('披露','ひろう','1483490','ロウ')]}`. The 暴 supp row uses `maps[-1-len(EXTRA_MAP.get(c,[]))]`.
- **PARTIAL** `{'戯曲':[1]}`. mapping() must skip the `len(senses)==len(sense elems)` assert for it, and the ledger/notes should say "JMdict sense 2 'Chinese opera' not taught."
- Word exclusions may name new batch words: allow `Path(...).exists() or k in words`. Add asserts that every @X is an existing kanji or a member and every &w is an existing word or a new word.
- **Manual 戯→悪戯 row**, appended to maps:

```
dict(kanji='戯',article='words/悪戯.md',newArticle=False,primaryReading='いたずら',entryIds=['1151580'],senseNumbers=[1,2,4,5],priorityTags=['ichi1'],readingPriorityTags=['ichi1'],note='Existing N3 identity/reading/title/type preserved. Whole-word jukujikun; no allocation of いたずら to 戯. New kanji common-word row reciprocates the required activated baseline pair.')
```

  - Verify the tags from families: k_ele 悪戯 has ke_pri ichi1; reading いたずら has re_pri ichi1 and re_inf gikun.
  - Do not run mapping() on it, because the re_inf assert would fail.
  - Add `- [悪戯](../words/悪戯.md) いたずら — mischief; prank; a whole-word reading, usually written いたずら; do not assign parts of いたずら to 戯` to 戯's Common words. Do not add it to the readings table.
- **Edit words/悪戯.md** (CRLF preserved by the writer): `and 戯 suggests play.` → `and [戯](../kanji/戯.md) suggests play.`
- The changes assert must allow words/悪戯.md as well as kanji/.
- **Constituent edits** (current lines are LF)
  - 警: the readings table cell `警戒 けいかい — vigilance` becomes `[警戒](../words/警戒.md) けいかい — vigilance`, and the CW line `- 警戒 けいかい — being on guard` gets the same link.
  - 握: `- 把握 はあく - grasp; understanding` → `- [把握](../words/把握.md) はあく - grasp; understanding`.
  - 暴: the table row `| バク | on | 暴露 ばくろ - disclosure; revelation |` and the CW line `- 暴露 ばくろ - disclosure; revelation` both link 暴露.
  - These cards already contain the word, so use edit() instead of addline (the supp loop must skip addline for 警, 握 and 暴).
  - 曲, 本, 制, 茶 and 養 use addline. 茶 gets 抹茶 after `- 茶道 さどう — the Way of Tea`; addline appends after the last CW line, which is acceptable.
- **Metadata handling** (must handle all of these)

| Card(s) | Current Metadata state | Action |
|---|---|---|
| 曲, 本, 制, 茶 | No Metadata line | Append `\n\nMetadata: Word pairs: {JM}, entries {lst}.` |
| 警 | No Metadata line; ends with a `Dictionary:` line listing 1252330, 1252360, 1252310 | Same append. |
| 握 | Multi-line wrapped Metadata; first line `Metadata: [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project),` | Append ` Word pairs: …` to the first line. meta_scan reads only the first line, so its ids must be on it. |
| 暴 | One-line Metadata already ending `Word pairs: [JMdict](…), entries 1519330, 1519340, 1519590, 1549100, 1601280.` | Extend via the entries regex. Relax B170's `'Word pairs' not in t` assert. |
| 養 | Long one-line Metadata, "entries … (the last three from …)", no regex match | Append ` Word pairs: {JM}, entries {lst}.` |

- Expected gaps from the earlier scan:

| Card | Gap ids |
|---|---|
| 曲 | 1239730, 1239740 |
| 本 | 1582710 1523060 1523180 1328390 1755110 1464780 1166600 2005520 1301640 2005490 2005500 1561550 2005510 1583120 1335130 |
| 制 | 1374880 1223010 1409550 |
| 茶 | 1422720 1002430 1280770 1422770 |

  Ambiguous gaps need PICK entries.
- **acc:** frozenPendingRecords=1228, publishedPendingRecordsWithCards=728, publishedN1Additions=722, n2Placements=6, undelivered=500, localUnreviewedDrafts=10, notStarted=490, overallN1TaskComplete=False.
- **selectionReason:** "First nine absent Jōyō rows on the beca991c receipt plus 露 (source row 1177), pulled forward for 披露 so that 露's ロウ reading has a qualifying route; 拐 moves to B172. Supports qualify through JMdict ichi1, news1, spec1 or gai1, with news2 and spec2 also qualifying under issue #60 comment 7112026459."
- **dictionaryChecks:** list the Daijisen word bodies, the character entries and the Joyo pages (23, 34, 130, 133, 79, 124, 153, 130, 145, 160; 暴 is on p. 143).

### Audit facts (audit_n1_batch.py)

- `activated_baseline_pairs` = frozen candidate pairs ∪ (member, words/X.md) for baseline word files whose name contains a member. For B171 this gives 戯/悪戯.md. All of them must be in the mapping pairs.
- For every mapping:
  - `meta.reading == primaryReading`;
  - newArticle matches;
  - entryIds are in the packet;
  - some `lexical_pair` holds;
  - the word text contains `(../kanji/c.md)`;
  - the kanji card contains `(../{article})`.
- readingDispositions must be in source order (on then kun), and each reading must appear exactly once in the table as `| reading |`. A sourceOnly row must contain "source-only". A selected row must link the article in its row.
- quizOnyomi/quizKunyomi must equal the projection and the selected decisions; offered keys must match.
- quizAudit: the title and distractors must match, with exactly 3 distinct distractors, and the labels must equal the distractor card titles.
- Word and kanji exclusion ledgers must equal the frontmatter.
- reused_changes must match the recorded before/after edits exactly, with no frontmatter change.
- The dictionary packet XML ids must equal the selection entryIds in order.

### Member metadata (verified this segment)

| Kanji | Onyomi | Kunyomi | Strokes | Radical (no.) |
|---|---|---|---|---|
| 戒 | カイ | いまし.める | 7 | 戈 62 |
| 戯 | ギ, ゲ | たわむ.れる, ざ.れる, じゃ.れる | 15 | 戈 62 |
| 扉 | ヒ | とびら | 12 | 戶 63 |
| 扶 | フ | たす.ける | 7 | 手 64 |
| 抄 | ショウ | — | 7 | 手 64 |
| 把 | ハ, ワ | — | 7 | 手 64 |
| 抑 | ヨク | おさ.える | 7 | 手 64 |
| 披 | ヒ | — | 8 | 手 64 |
| 抹 | マツ | — | 8 | 手 64 |
| 露 | ロ, ロウ | つゆ | 21 | 雨 173 |

All are grade 8.

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

### Distractor and exclusion card titles (for the notes text)

| Kanji | Title | Kanji | Title | Kanji | Title |
|---|---|---|---|---|---|
| 械 | machine; fetter (カイ) | 成 | become | 戦 | battle |
| 警 | warn; be on guard | 慎 | careful; prudent; discreet | 禁 | prohibit; ban |
| 律 | law; rhythm | 注 | pour, direct attention | 守 | guard; obey |
| 懲 | punish; learn a lesson | 訓 | instruction; kun reading | 備 | prepare; equip |
| 衛 | guard; defense | 護 | safeguard; protect | 虚 | empty; void; false (キョ) |
| 劇 | drama; play | 遊 | play | 娯 | recreation; amusement |
| 興 | revival; interest; pleasure | 楽 | music, enjoyment, ease | 演 | perform; stage |
| 笑 | laugh | 奏 | play music; report to a ruler | 弾 | bullet; play strings; bounce |
| 幕 | curtain; act of a play; shogunate | 芸 | art; performance; craft | 非 | non-; wrong (ヒ) |
| 悲 | sadness (ヒ) | 俳 | haiku; actor (ハイ) | 戸 | door; counter for households |
| 門 | gate; doorway | 窓 | window | 関 | involve; barrier |
| 開 | open; unfold | 閉 | shut | 隣 | next door; adjoining |
| 夫 | husband (フ) | 技 | skill; technique | 失 | lose; loss |
| 助 | help; rescue (たす.ける) | 援 | aid; assistance | 支 | support |
| 養 | nourish; raise; adopt | 補 | supplement; make good | 佐 | aide; assistant |
| 救 | rescue; save; relief | 丞 | assist; aid | 賛 | approve; praise |
| 少 | few, a little (ショウ) | 妙 | strange; exquisite | 秒 | second as a time unit |
| 抜 | extract | 略 | abbreviate; omit | 写 | copy, photograph |
| 録 | record; register | 要 | necessity; essentials | 訳 | translate; explanation |
| 選 | choose | 粋 | stylish; essence; pure | 抽 | pull out; extract; abstract |
| 択 | select; opt for | 色 | color | 拝 | worship; bow in respect (ハイ) |
| 抗 | defy; oppose | 握 | grip; grasp | 持 | hold, have |
| 取 | take | 束 | bundle (たば) | 捕 | capture |
| 執 | take hold; carry out; cling | 抱 | embrace | 括 | tie together; enclose |
| 柄 | handle; pattern; nature | 仰 | look up; revere (ギョウ, コウ) | 迎 | welcome; greet (ゲイ) |
| 柳 | willow (リュウ) | 圧 | pressure; oppress | 押 | push (お.さえる) |
| 制 | system; regulate | 止 | stop, halt | 縛 | bind; tie up; restrain |
| 防 | defend; ward off | 節 | joint; season; restraint | 被 | cover; incur (ヒ) |
| 波 | wave; billow (ハ) | 彼 | he (ヒ) | 示 | indicate |
| 発 | depart, emit | 表 | surface; chart | 展 | unfold; expand |
| 現 | actual; present | 告 | announce; inform | 顕 | evident; reveal |
| 呈 | present; offer; reveal | 宣 | proclaim; announce; declare | 掲 | put up; display; publish |
| 爆 | burst open; explode | 剖 | dissect; split open | 未 | not yet (ミ) |
| 味 | taste, flavor (ミ) | 株 | share; stump; rooted plant | 消 | extinguish; erase |
| 削 | shave; sharpen; pare | 除 | remove; exclude | 擦 | scrape; scrub |
| 塗 | paint; coat | 粉 | flour; powder | 殺 | kill |
| 末 | end; tip (マツ) | 摩 | rub; chafe | 磨 | polish; grind |
| 路 | path; route (ロ) | 霧 | fog; mist | 雪 | snow |
| 裸 | naked; bare | 浴 | bathe, be exposed to | 滴 | drip; drop |
| 皮 | skin; hide (ヒ) | 雨 | rain | 夜 | night |
| 曲 | bend; musical piece | 本 | book, origin | 茶 | tea (チャ, サ) |
| 暴 | violence; outburst (ボウ, バク) | | | | |

戈 has no card.

### JMdict, Daijisen and Joyo facts (verified earlier)

**Main supports**

| Word | Entry | Tags | Notes |
|---|---|---|---|
| 警戒 | 1252310 | ichi1/news1 | — |
| 戯曲 | 1225010 | ichi1/news1 | 2 senses; teach sense 1 only |
| 扉 | 1483380 | ichi1/news1 | senses 1–2; 闔 is rare |
| 扶養 | 1496990 | ichi1/news1 | — |
| 抄本 | 1349540 | news2/spec2 | — |
| 把握 | 1470910 | news1 | — |
| 抑制 | 1547290 | ichi1/news1 | — |
| 披露 | 1483490 | news1 | — |
| 抹茶 | 1525220 | news2/spec2 | — |
| 暴露 | 1601280 | ichi1/news1 | 曝露 also listed |
| 悪戯 | 1151580 | ichi1 | 5 senses, all uk |

**Other entries**

| Word | Entry | Word | Entry | Word | Entry |
|---|---|---|---|---|---|
| 戒める | 1200650 | 戒め | 1609250 | 戯れる | 1224970 (たわむれる ichi1, ざれる untagged) |
| 戯れ | 1224960 | じゃれる | 2859078 | 戯作 | 1577840 (げさく/ぎさく) |
| 戯れ言 | 1756640 | 門扉 | 1536270 (news1) | 開扉 | 1202900 |
| 助ける | 1344410 (扶ける is a rare form) | 一把 | 1165640 (いちわ) | 把 | 1607320 |
| 抑える | 2836285 | 抑え | 1613650 | 露 (つゆ) | 1560070 |
| 夜露 | 1537230 | 扶養家族 | 1690990 | 戸籍抄本 | 1651120 |
| 戸籍謄本 | 1651110 | 謄本 | 1450020 | 披露宴 | 1483500 |
| 疲労 | 1483780 | 警戒心 | 1252320 | 遊戯 | 1542190 |
| 戯画 | 1224990 | 抑圧 | 1547270 | 抑止 | 1547280 |
| 抑揚 | 1547300 | 抹消 | 1525200 | 抹殺 | 1525190 |
| 一抹 | 1166790 | 露出 | 1560130 | 茶道 | 1422770 |
| 茶の湯 | 1422610 | 煎茶 | 1391530 | 掌握 | 1349660 |
| 把持 | 1470920 | 抄録 | 1349560 | 抄訳 | 1349550 |
| 扶助 | 1496980 | 戒律 | 1200700 | 厳戒 | 1262560 |
| 披瀝 | 1483480 | | | | |

**Avoid:** 戯言 and 朝露.

**Daijisen character and word texts:** recorded in the earlier summary. Key items:
- 戯 sense 2 芝居。演劇。「戯曲」.
- 抄 sense 3 抜き書き「抄本」.
- 把 sense 1 しっかりと手中に握る「把握」.
- 抑 上からおさえつけてとめる「抑制」.
- 披 sense 2 手の内をすっかり開いて見せる「披露」.
- 抹 sense 3 すりつぶして粉にする「抹茶」.
- 露 ロ sense 3 むきだしにあらわす「暴露」; 〈ロウ〉あらわし見せる「披露」.
- 扶 sense 1 わきから支えて助ける「扶養」.
- 戒 sense 1 よくない事態に備えて気を引き締める「警戒」.
- 扉 entry 両側に開く戸; word senses: 1 開き戸の戸, 2 書名・著者名などを記したページ.
- Word bodies:
  - 警戒: 危険や災害に備えて….
  - 戯曲: 演劇の脚本・台本…ドラマ.
  - 扶養: 助け養うこと….
  - 抄本: sense 1 原本のある一部分を書き抜いたもの; sense 3 戸籍抄本など→謄本.
  - 把握: sense 1 しっかりとつかむこと; sense 2 しっかりと理解すること.
  - 抑制: おさえとどめること….
  - 披露: 《披き露す意》; sense 2 広く人に知らせること.
  - 暴露: sense 1 むき出しにすること…あばいて明るみに出すこと.
  - 抹茶: 茶の新芽…臼でひいて粉末にしたもの。主として茶の湯に用い.

**Joyo rows**

| Kanji | Page | Readings and examples |
|---|---|---|
| 戒 | 23 | カイ 戒心 戒律 警戒 / いましめる 戒める 戒め |
| 戯 | 34 | ギ 戯曲 遊戯 児戯 / たわむれる 戯れる 戯れ |
| 扉 | 130 | ヒ 開扉 門扉 / とびら |
| 扶 | 133 | フ 扶助 扶養 扶育 |
| 抄 | 79 | ショウ 抄録 抄本 抄訳 |
| 把 | 124 | ハ 把握 把持 一把（ワ）三把（バ）十把（パ）; note that ハ becomes ワ/バ/パ by the preceding sound |
| 抑 | 153 | ヨク 抑圧 抑制 抑揚 / おさえる 抑える 抑え ⇔ 押さえる |
| 披 | 130 | ヒ 披見 披露 直披 |
| 抹 | 145 | マツ 抹殺 抹消 一抹 |
| 露 | 160 | ロ 露出 露店 雨露 / ロウ 披露 / つゆ 露 夜露 |
| 暴 | 143 | バク 暴露 |

**Kanjipedia:** ゲ and ざ.れる of 戯, and たす.ける of 扶, are outside standard use.

### Word frontmatter plan

| Word | Title | Kind | Tags | Senses | Exclusions |
|---|---|---|---|---|---|
| 警戒 | vigilance; being on guard | kango | noun, suru-verb, safety? | 1 | 用心 注意 警告 警備 予防 油断 気を付ける 慎重 |
| 戯曲 | play (drama); script | kango | noun, arts | 1 | 演劇 劇 芝居 ドラマ 小説 物語 文学 作品 原稿 劇場 舞台 悲劇 作家 |
| 扉 | door; title page | wago | noun, home | 1–2 | ドア 戸 門 玄関 入口 出入口 ページ 題名 表紙 戸棚 窓 |
| 扶養 | supporting dependents | kango | noun, suru-verb, family | 1 | 世話 援助 支える 育てる 面倒 助ける 育児 生活 |
| 抄本 | excerpt; abridged copy | kango | noun, writing | 1 | 写す 複写 コピー 要旨 あらすじ 記録 原稿 要点 |
| 把握 | grasp; understanding | kango | noun, suru-verb, thinking? | 1 | 理解 分かる 掴む 握る 心得る 捕える 押さえる 握手 |
| 抑制 | restraint; control | kango | noun, suru-verb, behavior | 1 | 制限 我慢 こらえる 防止 調節 管理 支配 ブレーキ 限度 押さえる |
| 披露 | presenting; showing; announcement | kango | noun, suru-verb, communication | 1 | 発表 公表 紹介 見せる 示す 演技 演奏 発揮 宣伝 現す 表す 暴露 |
| 抹茶 | matcha; powdered green tea | kango | noun, food | 1 | 茶 お茶 紅茶 粉 緑 喫茶店 |
| 暴露 | disclosure; exposure | kango | noun, suru-verb, media/communication | 1 | 発表 公表 現す 表す 発見 秘密 隠す 披露 |

Tags marked ? are unconfirmed. Choose tags that already exist in the corpus, for example attention, society, perception, learning, media, communication, food.

### Word existence

**Missing (plain text only; never &-link):** 和菓子 暴力 真相 脚本 台本 茶道 監視 抜粋 要約 原本 一部 粉末 週刊誌 上演 上昇 社員 規制 結婚式 展示会 新製品 アイス 京都 書き写す 市役所 戸籍 一通 母 年老いた 老いる 三人 部下 近づく 知らない 大雨 お店 遊戯 煎茶 抑える 抑圧 戒める.

**Existing (linkable):** most common words, including 用心 注意 警告 警備 予防 油断 気を付ける 慎重 演劇 劇 芝居 ドラマ 小説 物語 文学 作品 原稿 劇場 舞台 悲劇 作家 ドア 戸 門 玄関 入口 出入口 ページ 題名 表紙 戸棚 窓 世話 援助 支える 育てる 面倒 助ける 育児 生活 写す 複写 コピー 要旨 あらすじ 記録 要点 理解 分かる 掴む 握る 心得る 捕える 押さえる 握手 制限 我慢 こらえる 防止 調節 管理 支配 ブレーキ 限度 発表 公表 紹介 見せる 示す 演技 演奏 発揮 宣伝 現す 表す 茶 お茶 紅茶 粉 緑 喫茶店 発見 秘密 隠す 悪戯 遊ぶ 冗談 家族 結婚 製品 不正 政治家 状況 感情 物価 政府 対策 部長 友人 会社 雑誌 菓子.

### Examples (kana reading and English required)

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

### Unselected readings (other dict)

| Kanji | Reading | Shown | Entry ids |
|---|---|---|---|
| 戒 | いまし.める | 戒める/戒め | 1200650 1609250 |
| 戯 | ゲ | 戯作 げさく; JMdict also ぎさく; Kanjipedia outside standard use | 1577840 |
| 戯 | たわむ.れる | 戯れる/戯れ | 1224970 1224960 |
| 戯 | ざ.れる | ざれる reading of 戯れる, untagged; 戯れ言 ざれごと; outside standard use | 1224970 1756640 |
| 戯 | じゃ.れる | じゃれる, usually kana | 2859078 |
| 扉 | ヒ | 門扉 もんぴ / 開扉 かいひ | 1536270 1202900 |
| 扶 | たす.ける | 扶ける, a rarely used form of &助ける; outside standard use | 1344410 |
| 把 | ワ | 一把 いちわ; Joyo note on ワ/バ/パ | 1165640 |
| 抑 | おさ.える | 抑える/抑え | 2836285 1613650 |
| 露 | つゆ | 露/夜露 | 1560070 1537230 |

### Shape cues

| Kanji | Cue |
|---|---|
| 戒 | @械 contains 戒 (also カイ); @戦 shares 戈 |
| 戯 | left as in @虚, right as in @戦 |
| 扉 | @戸 over @非 (ヒ) |
| 扶 | 扌 + @夫 (フ) |
| 抄 | 扌 + @少 (ショウ) |
| 把 | 扌 + bottom of @色 |
| 抑 | right as in @仰/@迎; compare @柳 |
| 披 | 扌 + @皮 (ヒ; 皮 has a card); @被 and @波 share 皮; @彼 |
| 抹 | 扌 + @末 (マツ) vs @未; @味, @株 |
| 露 | @雨 over @路 (ロ) |

**Kanji with no card (never @-link):** 頁 摘 控 鎮 謄 巴 肥 戈 廾 卬 虍 曝 闔 鈔 碾 扌.

### Selection notes

- 抄本 and 抹茶 qualify via news2/spec2 under #60 comment 7112026459.
- 露 ロウ is supported by 披露 (in batch); 露 ロ by 暴露 (暴 has a card). 暴露 is NOT a Joyo example for 露 (露出 露店 雨露 are), but it is the Joyo バク example on 暴 p. 143.
- 扉's support is the word 扉 itself, whose reading とびら is listed in the Joyo table.

### Procedures and quirks

- **Gates:** from b171-wt run
  `python <files>\n1_gates.py 171 beca991c03d66578b2abccce7f29de1c4a2ab983 "戒 戯 扉 扶 抄 把 抑 披 抹 露" "警 握 暴 曲 養 本 制 茶" "警戒 戯曲 扉 扶養 抄本 把握 抑制 披露 抹茶 暴露"`
  It takes about 8 min; set `ONLY=` to restrict steps.
- **Validation commands:** `python tools/validate.py`, `python tools/build_manifest.py`, `python tools/audit_n1_batch.py --batch 171`.
- **meta_scan:** needs `$env:N1_LEAN=(Resolve-Path ..\lean).Path`.
- **Publication:** workflow 378446878; docs/n1-reviews/batch-112-publication/verify-zip.py; tools/n1_record_publication.py.
- **Signing and auth:** `git -c user.signingkey=D4C9A275A218AF747B787AFA9D94B9D311BD26A7`; `$env:GH_TOKEN=(gh auth token --user stop-cran)`; add the Co-authored-by trailer.
- **Shell quirks:**
  - Set `$env:PYTHONIOENCODING='utf-8'`.
  - Redirect output to `..\b171-tmp.txt` and read it with `Get-Content -Encoding utf8`.
  - The grep tool fails in worktrees, so use Python.
  - cd does not persist between calls.
  - Pipe here-strings to `python -`.
- **Content constraints:**
  - No JLPT on new words.
  - Avoid glyphs in U+2E80–2FDF and U+3400–4DBF.
  - Never fabricate support for blocked grade-9 rows: 崚 彪 晟 燿 舜 赳 侑 嵯 怜 滉 瑚.
- **Next batch, B172:** 拐 拒 拓 拘 拙 拠 拳 拷 挑 据.
</technical_details>

<important_files>
- **C:\Users\romanko\n1-kanji-workspace\b171-wt**
  - The worktree.
  - The render will create 10 kanji cards, 10 word cards, batch-171-progress.json, and the jmdict selection and xml.
  - It will edit words/悪戯.md and kanji/{警,握,暴,曲,養,本,制,茶}.md.
- **files\b170_render.py** (149 lines): full render template, viewed this segment; copy it with the B171 changes above.
  - Lines 1–30: setup and iterparse.
  - Lines 31–60: helpers and mapping.
  - Lines 61–105: the main loop.
  - Lines 106–127: constituent Metadata.
  - Lines 128–149: notes, ledger and write-out.
- **files\b170_content.py**: content format template.
  - Lines 1–17: header and cards.
  - Lines 17–90: words.
  - Lines 91–143: chars and EXC.
- **files\n1_gates.py**: the gate runner.
- **tools\audit_n1_batch.py**:
  - Lines 124–129: activated_baseline_pairs.
  - Lines 700–812: the main audit.
- **docs\n1-reviews\batch-137-closure\confirm-packet\gpt\evidence\meta_scan.py**: scans only the first Metadata line.
- **words\悪戯.md**: an N3 jukujikun word teaching senses 1-2, 4-5. Must get a `[戯](../kanji/戯.md)` link; its CRLF line endings must be preserved.
- **Workspace evidence** (`C:\Users\romanko\n1-kanji-workspace\`): b171-dj*.json, b171-x.json, b171-x2.json, b171-readings.json, b171-joyo.txt, jmdict\JMdict_e.gz.
</important_files>

<next_steps>
1. **Write `files\b171_content.py`.** Include the header, cards, `EXTRA_MAP={'露':[('披露','ひろう','1483490','ロウ')]}`, ten word tuples with full prose (Daijisen quotes with kana and English, two examples each, form/synonym/distinctive texts), ten chars tuples (intro, cue, notes listing every distractor and exclusion with meaning plus the Joyo citation, and the other dict), `EXC={}` and a `PARTIAL={'戯曲':[1]}` constant.
2. **Write `files\b171_render.py`** with every B171 change: PARTIAL, the manual 悪戯 row plus the 戯 CW line and 悪戯.md edit, the link edits for 警/握/暴 instead of addline, flexible Metadata handling (none, multi-line 握, existing Word pairs on 暴, non-matching 養), changes allowing words/悪戯.md, and new-word exclusion existence.
3. **Run the render from b171-wt.** Resolve CHECK prints via FIX and ambiguous gaps via PICK. Then run validate, build_manifest, the audit and the full gates until clean.
4. **Make the signed draft commit** "N1 B171 draft: 戒 戯 扉 扶 抄 把 抑 披 抹 露".
5. **Review and integrate:** serial blind reviews (Claude correctness → GPT consistency/quiz → Grok comprehensibility); fixes and confirmations; closure; integration with origin/main; revalidation.
6. **Publish:** signed content and receipt commits, verify both ZIPs, post the #60 checkpoint, recount (target 738 delivered / 490 missing).
7. **Continue** with B172 (拐 拒 拓 拘 拙 拠 拳 拷 挑 据) and onward.
8. **Clean up** temporaries: ..\b171-tmp.txt, ..\b171-x*.json, ..\b170-scan, ..\b171-scan, C:\Users\romanko\b170-glcheck.txt.
</next_steps>