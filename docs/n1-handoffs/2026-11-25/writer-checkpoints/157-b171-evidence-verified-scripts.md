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
   - Prepared the membership file and strokes, gathered evidence, settled the card plan, and studied the format and audit rules.

2. This segment (still read-only; no new repo changes)
   - **Audit rules**
     - Read lexical_pair (audit lines 45-57). The 悪戯 row passes: the gikun re_inf on いたずら is not "search-only", and k_ele 悪戯 matches.
     - support_mapping_rows (lines 132-150) forbids duplicate (kanji, article) pairs. supplementary kanji must not be members and must have baseline kanji cards.
   - **Precedent for reused-article mapping rows** (newArticle False), from B159-169: they carry fields spelling, senseNumber/senseNumbers, priorityTags, readingPriorityTags and priorityTagAttribution or note. Example B169 惨→みじめ.
   - **Corpus tag counts:** safety 11, literature 15, home 40, household 41, family 65, documents 10, thinking 12, behavior 39, communication 118, drinks 9, food 137, information 12, media 23, society 54, crime 5, performance 9, arts 14, attention 19, knowledge 10, understanding 6, culture 14.
   - **word_quiz_audit.py** (docs/n1-reviews/batch-156-closure/packet/evidence/audits/): usage `python word_quiz_audit.py REPO_ROOT WORD...`.
     - Score = 2 per shared tag + 1 same type + 1 shared kanji.
     - Problems are flagged for reachable distractors and ATTESTED readings.
     - Run it after rendering to tune exclusions.
   - **File names corrected:** lookup outputs are b171-jm.json through b171-jm7.json, not b171-x*.json. jm3 is a dict of lists; the others are lists of {id,k,r,s}. Daijisen fetches are b171-dj.json through b171-dj4.json (dicts keyed by word or kanji, raw HTML text).
   - **Re-verified Daijisen bodies and JMdict entries** (see Technical details). 戯画 1224990 is not in the lookup files; don't cite it unless re-looked up.
   - **Re-viewed templates in full:** b170_render.py and b170_content.py (header, cards, 慈善/慕う/感慨 word tuples, all chars tuples, EXC).
</history>

<work_done>
**Worktree:** `C:\Users\romanko\n1-kanji-workspace\b171-wt`, branch n1-b171, HEAD = base beca991c03d66578b2abccce7f29de1c4a2ab983.

**Uncommitted in the worktree:**
- `docs/n1-sources/batch-171-membership.json` (new)
- `strokes/{戒,戯,扉,扶,抄,把,抑,披,抹,露}.json` (new, verified)

**Session files dir:** `C:\Users\romanko\.copilot\session-state\22102645-7498-4a81-9366-de9377e0695a\files\`
- Present: b170_content.py, b170_render.py, b169_render.py, n1_gates.py, b170_close/panel/publish/followup.py.
- In the workspace root: b171_strokes.py and b171_lookup.py (`python b171_lookup.py "w1,w2" out.json`, which verifies the JMdict sha).
- **Not yet written:** b171_content.py and b171_render.py.

**Checklist:**
- [x] Evidence, plan, format study, audit-rule study, Daijisen and JMdict re-verification
- [ ] Write b171_content.py (next, immediately)
- [ ] Write b171_render.py
- [ ] Run render → validate → build_manifest → word_quiz_audit → audit → gates → signed draft commit
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
- `words={w:(gloss, kind, 'tags-after-kind e.g. "noun, society"', [exclusions], 'sensestr e.g. "1" or "1–2"', intro, exampleA, exampleB, formText, synText, distinctText)}`
  - sensecount uses the last number of sensestr after '–'.
  - The rendered tags are `[kind, tags]`.
- `chars={c:(intro, cue, notes, {reading:(shownText, 'eid eid')})}`
- `EXC={}`

**Text style**

- `@X` renders a kanji link; `&w` renders a word link (only for existing words or new batch words).
- Intro: Daijisen definition quoted as 日本語 (かな), “English,” then "JMdict glosses it “…”."
- Example bullets use the form `日本語。 (かな。) — English.`
- formText cites the [Digital Daijisen, X]({W("X")}) character entry for the other constituent.
- Use curly quotes “ ” and ’.
- Notes must @-mention every distractor and exclusion with its meaning, and cite `[standard-use table, PDF p. N]({JOYO}#page=N)` with its readings and examples.
- Source-only readings must contain "source-only" in the shown text.

### b170_render.py → b171_render.py changes

The template is 149 lines; changes reference its structure.

- Import from b171_content. Set `r.name=='b171-wt'`, BASE beca991c03d66578b2abccce7f29de1c4a2ab983, `../b171-readings.json` (dict with on, kun, outside, url; use `km[c]['url']`), batch-171-membership.json, tmp `../b171-scan`, and batch '171' throughout (ledger file names, xml, selection).
- Member assert: `[k for k in absent if int(source[k]['grade'])<=8][:9]+['露']`, plus `'露' in absent and int(source['露']['grade'])==8`.
- Remove the kanqual collection and assert.
- `primary` must include 1151580.
- **FIX** `{'悪戯':'1151580','露':'1560070','把':'1607320','抑える':'2836285','助ける':'1344410','戯れる':'1224970','戒め':'1609250'}`. Extend it as CHECK prints appear.
- **EXTRA**

| Word | Appended text |
|---|---|
| 扶養 | `'; 扶養家族, entry 1690990'` |
| 抄本 | `'; 戸籍抄本, entry 1651120; 戸籍謄本, entry 1651110; 謄本, entry 1450020'` |
| 披露 | `'; 披露宴, entry 1483500; 疲労, entry 1483780'` |
| 扉 | `'; 門扉, entry 1536270'` |

- **EXTRA_MAP** `{'露':[('披露','ひろう','1483490','ロウ')]}`. The supp row uses `maps[-1-len(EXTRA_MAP.get(c,[]))]`.
  - 披露's components are 披 and 露, both members, so 露 gets no supp row. 暴露's components are 暴 (non-member → supp + edit) and 露.
- **PARTIAL** `{'戯曲':[1]}`. mapping() must skip the `len(senses)==len(sense elems)` assert for it, and the ledger note should say "JMdict sense 2 'Chinese opera' not taught." 扉 teaches senses 1–2 (both).
- Word exclusions may name new batch words: allow `Path(...).exists() or k in words`. Add asserts that every @X is an existing kanji or a member and every &w is an existing word or a new word.
- **Manual 戯→悪戯 row**, appended to maps (do not run mapping() on it):

```
dict(kanji='戯',article='words/悪戯.md',newArticle=False,primaryReading='いたずら',entryIds=['1151580'],senseNumbers=[1,2,4,5],priorityTags=['ichi1'],readingPriorityTags=['ichi1'],spelling='悪戯',note='Existing N3 identity/reading/title/type preserved. Whole-word jukujikun (JMdict re_inf gikun; all senses usually kana); no allocation of いたずら to 戯. New kanji common-word row reciprocates the required activated baseline pair.')
```

  - Add the CW line `- [悪戯](../words/悪戯.md) いたずら — mischief; prank; a whole-word reading, usually written いたずら; do not assign parts of いたずら to 戯` to 戯's Common words, but not to its readings table.
  - Edit words/悪戯.md (CRLF preserved): `and 戯 suggests play.` → `and [戯](../kanji/戯.md) suggests play.`
  - The changes assert must allow words/悪戯.md as well as kanji/.
- **Constituent edits** (current lines are LF)
  - 警: table cell `警戒 けいかい — vigilance` → `[警戒](../words/警戒.md) けいかい — vigilance`, and the CW line `- 警戒 けいかい — being on guard` gets the same link.
  - 握: `- 把握 はあく - grasp; understanding` → linked.
  - 暴: the table row `| バク | on | 暴露 ばくろ - disclosure; revelation |` and the CW line `- 暴露 ばくろ - disclosure; revelation` both get linked.
  - Use edit() for these three; the supp loop must skip addline for 警, 握 and 暴.
  - 曲, 本, 制, 茶 and 養 use addline.
- **Metadata handling**

| Card(s) | Current Metadata state | Action |
|---|---|---|
| 曲, 本, 制, 茶, 警 | None (警 ends with a `Dictionary:` line listing 1252330, 1252360, 1252310) | Append `\n\nMetadata: Word pairs: {JM}, entries {lst}.` |
| 握 | Multi-line Metadata; first line starts `Metadata: [KANJIDIC2](...)` | Append ` Word pairs: …` to the first line (meta_scan reads only the first line). |
| 暴 | One-line Metadata already ending `Word pairs: [JMdict](…), entries 1519330, 1519340, 1519590, 1549100, 1601280.` | Extend via the entries regex; relax the `'Word pairs' not in t` assert. |
| 養 | Long one-line Metadata without a regex match | Append ` Word pairs: {JM}, entries {lst}.` |

- Expected meta_scan gaps (ambiguous ones need PICK):

| Card | Gap ids |
|---|---|
| 曲 | 1239730, 1239740 |
| 本 | 1582710 1523060 1523180 1328390 1755110 1464780 1166600 2005520 1301640 2005490 2005500 1561550 2005510 1583120 1335130 |
| 制 | 1374880 1223010 1409550 |
| 茶 | 1422720 1002430 1280770 1422770 |

- **acc:** frozenPendingRecords=1228, publishedPendingRecordsWithCards=728, publishedN1Additions=722, n2Placements=6, undelivered=500, localUnreviewedDrafts=10, notStarted=490, overallN1TaskComplete=False.
- **selectionReason:** "First nine absent Jōyō rows on the beca991c receipt plus 露 (source row 1177), pulled forward for 披露 so that 露's ロウ reading has a qualifying route; 拐 moves to B172. Supports qualify through JMdict ichi1, news1, spec1 or gai1, with news2 and spec2 also qualifying under issue #60 comment 7112026459."
- **dictionaryChecks:** Daijisen word bodies for the 10 words plus 悪戯; character entries 戒 戯 扶 抄 把 抑 披 抹 露 and 警 曲 養 本 握 制 暴 茶; Joyo pages 23, 34, 130, 133, 79, 124, 153, 130, 145, 160 (暴 on p. 143).

### Audit facts (audit_n1_batch.py)

- activated_baseline_pairs = frozen pairs ∪ (member, baseline word file containing the member). For B171 this gives 戯/悪戯.md, which must be in the mappings.
- For every mapping:
  - `meta.reading == primaryReading`;
  - newArticle matches;
  - entryIds are in the packet;
  - lexical_pair holds (rejects only search-only re_inf when the flag is set);
  - the word text contains `(../kanji/c.md)`;
  - the kanji card contains `(../{article})`.
- readingDispositions must be in source order (on then kun), and each reading must appear exactly once in the table as `| reading |`. sourceOnly rows must contain "source-only". Selected rows must link the article.
- quizOnyomi/quizKunyomi must equal the projection; offered keys must match.
- quizAudit: exactly 3 distinct distractors; labels must equal the distractor card titles.
- Exclusion ledgers must equal the frontmatter. reused_changes must match the recorded edits exactly, with no frontmatter change. Packet XML ids must equal selection entryIds in order.

### Member metadata

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
| 助 | help; rescue | 援 | aid; assistance | 支 | support |
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
| 曲 | bend; musical piece | 本 | book, origin | 茶 | tea |
| 暴 | violence; outburst (ボウ, バク) | | | | |

戈 has no card.

### Verified JMdict entries (pinned)

**Main supports**

| Entry | Word | Tags | Glosses |
|---|---|---|---|
| 1252310 | 警戒 けいかい | ichi1/news1 | "vigilance; caution; alertness; precaution; being on guard" (1 sense) |
| 1225010 | 戯曲 ぎきょく | ichi1/news1 | 1 "drama; play"; 2 "Chinese opera" |
| 1483380 | 扉 とびら | ichi1/news1; 闔 rare | 1 "door; gate; opening"; 2 "title page" |
| 1496990 | 扶養 ふよう | ichi1/news1 | "support (e.g. of one's dependents); maintenance" |
| 1349540 | 抄本 しょうほん | news2/spec2; 鈔本 rare | "excerpt; abridgment; abridgement; book of selections" |
| 1470910 | 把握 はあく | news1 | "grasp (of the situation, meaning, etc.); understanding; control; hold; grip" |
| 1547290 | 抑制 よくせい | ichi1/news1 | "control; restraint; suppression; constraint; curtailment; inhibition; check; curb" |
| 1483490 | 披露 ひろう | news1 | "announcement; presentation; demonstration; displaying; showing; introducing; unveiling; revealing; performing" |
| 1525220 | 抹茶 まっちゃ | news2/spec2; まっ茶 and 末茶 search-only | "matcha; powdered green tea" |
| 1601280 | 暴露 ばくろ | ichi1/news1; 曝露 untagged | "disclosure; exposure; revelation" |
| 1151580 | 悪戯 | ichi1; いたずら ichi1 + gikun | 5 senses, all uk: 1 mischief; prank; trick; practical joke / 2 mischievous; naughty / 3 pastime; hobby (humble) / 4 playing with (e.g. a lighter); fooling around with…; tampering with / 5 lewd behaviour… (euphemistic) |

**Readings and related words**

| Entry | Word | Tags | Glosses |
|---|---|---|---|
| 1200650 | 戒める いましめる | ichi1/news2 | 1 to warn against; to caution against / 2 to admonish; to scold; to rebuke / 3 to prohibit…; 4-6 archaic |
| 1609250 | 戒め いましめ | ichi1/news2 | 1 caution; admonition; warning; lesson / 2 prohibition… / 3 punishment |
| 1224970 | 戯れる | ichi1 on たわむれる; ざれる untagged | 1 to be playful; to gambol; …to joke / 2 to flirt with / 3 archaic |
| 1224960 | 戯れ たわむれ | ichi1/news2 | "play; sport; fun; caprice; joke; jest; flirtation" |
| 2859078 | 戯れる じゃれる | untagged, uk | "to play around (of a cat, dog, etc.); to frisk; to gambol; to frolic" |
| 1577840 | 戯作 げさく/ぎさく | untagged | 1 cheap literature; writing for amusement / 2 light literature popular in the late Edo period |
| 1756640 | 戯れ言 ざれごと/たわむれごと | untagged; 戯言 search-only | "joke; jest; gag" |
| 1536270 | 門扉 もんぴ | news1 | "door(s) of a gate" |
| 1202900 | 開扉 かいひ | untagged | "opening a door" |
| 1344410 | 助ける たすける | — | 扶ける rarely used form; 1 save/rescue, 2 help/assist, 3 support (financially)… |
| 1165640 | 一把 いちわ | untagged | "bundle; bunch" |
| 1607320 | 把 わ | ichi1/news2 (ば, ぱ untagged) | "counter for bundles" |
| 2836285 | 抑える おさえる | ichi1/news1 | 1 to keep within limits…; to restrain (e.g. emotions)… / 2 to hold back… |
| 1613650 | 抑え おさえ | news1 | — |
| 1560070 | 露 つゆ | ichi1 | 1 dew / 2 tears / 3 (not) a bit |
| 1537230 | 夜露 よつゆ/やろ | — | "evening dew; night dew" |
| 1690990 | 扶養家族 | — | "one's dependents" |
| 1651120 | 戸籍抄本 | — | "official copy of part of family register" |
| 1651110 | 戸籍謄本 | spec1 | "official copy of the family register" |
| 1450020 | 謄本 | — | 1 "certified copy; transcript" |
| 1483500 | 披露宴 | ichi1 | "reception (e.g. wedding); banquet; celebration; party" |
| 1483780 | 疲労 ひろう | ichi1/news1 | "fatigue; weariness; exhaustion; tiredness" |
| 1252320 | 警戒心 | — | "wariness" |
| 1542190 | 遊戯 ゆうぎ | news2/spec2 | — |
| 1547270 | 抑圧 | ichi1/news1 | — |
| 1525200 | 抹消 | ichi1/news2 | "erasure; striking off; crossing out; cancellation; deletion" |
| 1525190 | 抹殺 | news2/spec2 | — |
| 1166790 | 一抹 | news2/spec2 | "a touch (of sadness…)" |
| 1560130 | 露出 | news2/spec2 | — |
| 1349560 | 抄録 | news2/spec2 | — |
| 1349550 | 抄訳 | — | "abridged translation" |
| 1496980 | 扶助 | ichi1/news1 | "aid; help; assistance; support" |
| 1200700 | 戒律 | news2/spec2 | — |
| 1470920 | 把持 はじ | untagged | "grasp; hold; grip" |

1224990 (戯画) was not in the lookup files; re-look it up if needed.

### Verified Digital Daijisen texts (verbatim tables removed from this public copy)

Three verbatim tables stood here and were removed from the handoff copy because they reproduced whole Digital Daijisen entries: the word bodies (警戒 戯曲 扉 扶養 抄本 把握 抑制 披露 抹茶 暴露 悪戯 門扉 戒める 戯れる 抑える), the ten member character entries (戒 戯 扉 扶 抄 把 抑 披 抹 露) and the constituent character senses used for the formText sentences (警 曲 養 本 握 制 暴 茶). Re-fetch them when authoring: `python n1_batch_tool.py webcheck <kanji...> --out <dir>` for character entries (see `code/lean/n1cmds.py`) and `python code/lean/webtest.py <word>` for a word. Quote only a short clause, as the shipped cards do. Checkpoint 156 lists the short key clauses the plan relies on.

**Member character entries** and **Constituent character senses (for formText)**: tables removed, see the note above.

### Joyo rows

| Kanji | Page | Readings and examples |
|---|---|---|
| 戒 | 23 | カイ 戒心 戒律 警戒 / いましめる 戒める 戒め |
| 戯 | 34 | ギ 戯曲 遊戯 児戯 / たわむれる 戯れる 戯れ |
| 扉 | 130 | ヒ 開扉 門扉 / とびら 扉 |
| 扶 | 133 | フ 扶助 扶養 扶育 |
| 抄 | 79 | ショウ 抄録 抄本 抄訳 |
| 把 | 124 | ハ 把握 把持 一把（ワ）三把（バ）十把（パ) |
| 抑 | 153 | ヨク 抑圧 抑制 抑揚 / おさえる 抑える 抑え |
| 披 | 130 | ヒ 披見 披露 直披 |
| 抹 | 145 | マツ 抹殺 抹消 一抹 |
| 露 | 160 | ロ 露出 露店 雨露 / ロウ 披露 / つゆ 露 夜露 |
| 暴 | 143 | バク 暴露 |

Kanjipedia lists 戯's ゲ and ざ.れる, and 扶's たす.ける, as outside standard use.

### Word frontmatter plan

Existing tags to use: safety, literature, home, family, documents, thinking, behavior, communication, drinks, information, media.

| Word | Title | Kind | Tags | Senses | Exclusions |
|---|---|---|---|---|---|
| 警戒 | vigilance; being on guard | kango | noun, suru-verb, safety | 1 | 用心 注意 警告 警備 予防 油断 気を付ける 慎重 |
| 戯曲 | play (drama); script | kango | noun, literature | 1 | 演劇 劇 芝居 ドラマ 小説 物語 文学 作品 原稿 劇場 舞台 悲劇 作家 |
| 扉 | door; title page | wago | noun, home | 1–2 | ドア 戸 門 玄関 入口 出入口 ページ 題名 表紙 戸棚 窓 |
| 扶養 | supporting dependents | kango | noun, suru-verb, family | 1 | 世話 援助 支える 育てる 面倒 助ける 育児 生活 |
| 抄本 | excerpt; abridged copy | kango | noun, documents | 1 | 写す 複写 コピー 要旨 あらすじ 記録 原稿 要点 |
| 把握 | grasp; understanding | kango | noun, suru-verb, thinking | 1 | 理解 分かる 掴む 握る 心得る 捕える 押さえる 握手 |
| 抑制 | restraint; control | kango | noun, suru-verb, behavior | 1 | 制限 我慢 こらえる 防止 調節 管理 支配 ブレーキ 限度 押さえる |
| 披露 | presenting; showing; announcement | kango | noun, suru-verb, communication | 1 | 発表 公表 紹介 見せる 示す 演技 演奏 発揮 宣伝 現す 表す 暴露 |
| 抹茶 | matcha; powdered green tea | kango | noun, drinks | 1 | 茶 お茶 紅茶 粉 緑 喫茶店 |
| 暴露 | disclosure; exposure | kango | noun, suru-verb, information | 1 | 発表 公表 現す 表す 発見 秘密 隠す 披露 |

Confirm the tag/kind convention against a published B170 card (e.g. words/慈善.md uses `tags: [kango, noun, society]`). The 扉 wago kind follows 慕う's usage.

### Word existence

**Missing (plain text only; never &-link):** 和菓子 暴力 真相 脚本 台本 茶道 監視 抜粋 要約 原本 一部 粉末 週刊誌 上演 上昇 社員 規制 結婚式 展示会 新製品 アイス 京都 書き写す 市役所 戸籍 一通 母 年老いた 老いる 三人 部下 近づく 知らない 大雨 お店 遊戯 煎茶 抑える 抑圧 戒める.

**Existing (linkable):** the exclusion words above, plus 悪戯 遊ぶ 冗談 家族 結婚 製品 不正 政治家 状況 感情 物価 政府 対策 部長 友人 会社 雑誌 菓子, among others.

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
| 戯 | ゲ | 戯作 げさく (JMdict also ぎさく); Kanjipedia outside standard use | 1577840 |
| 戯 | たわむ.れる | 戯れる/戯れ | 1224970 1224960 |
| 戯 | ざ.れる | ざれる, the untagged reading of 戯れる; 戯れ言 ざれごと; outside standard use | 1224970 1756640 |
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
| 披 | 扌 + @皮 (ヒ); @被 and @波 share 皮; @彼 |
| 抹 | 扌 + @末 (マツ) vs @未; @味, @株 |
| 露 | @雨 over @路 (ロ) |

**Kanji with no card (never @-link):** 頁 摘 控 鎮 謄 巴 肥 戈 廾 卬 虍 曝 闔 鈔 碾 扌.

### Selection notes

- 抄本 and 抹茶 qualify via news2/spec2 under #60 comment 7112026459.
- 露 ロウ is supported by 披露 (in batch). 露 ロ is supported by 暴露 (暴 has a card); 暴露 is not a Joyo example for 露, but it is in Daijisen's 露 ロ sense 3 and is the Joyo バク example on 暴 p. 143.
- 扉's support is the word 扉 itself; the reading とびら is in the Joyo table.

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
- **files\b170_render.py** (149 lines): render template; copy it with the B171 changes above.
  - Lines 1–30: setup and iterparse.
  - Lines 31–60: helpers (fmt, edit, addline, cite, mapping).
  - Lines 61–105: the main loop.
  - Lines 106–127: constituent Metadata.
  - Lines 128–149: notes, ledger and write-out.
- **files\b170_content.py**: content format template.
  - Lines 1–17: header, cards and EXTRA_MAP.
  - Lines 17–90: word tuples.
  - Lines 91–143: chars and EXC.
- **files\n1_gates.py**: the gate runner.
- **tools\audit_n1_batch.py**:
  - Lines 45–57: lexical_pair.
  - Lines 124–150: activated pairs and mapping rows.
  - Lines 700–812: the main audit.
- **docs\n1-reviews\batch-156-closure\packet\evidence\audits\word_quiz_audit.py**: word quiz distractor audit; run it after rendering.
- **docs\n1-reviews\batch-137-closure\confirm-packet\gpt\evidence\meta_scan.py**: scans only the first Metadata line.
- **words\悪戯.md**: an N3 jukujikun word teaching senses 1-2, 4-5. Needs a `[戯](../kanji/戯.md)` link; preserve its CRLF line endings.
- **Workspace evidence** (`C:\Users\romanko\n1-kanji-workspace\`): b171-dj.json through b171-dj4.json (Daijisen), b171-jm.json through b171-jm7.json (JMdict lookups), b171-readings.json, b171-joyo.txt, jmdict\JMdict_e.gz, b171_lookup.py.
</important_files>

<next_steps>
1. **Write `files\b171_content.py`.** Include the header, cards, EXTRA_MAP, `PARTIAL={'戯曲':[1]}`, ten word tuples with full prose (Daijisen quotes with kana and English, two examples each, form/synonym/distinctive texts using only the verified texts above), ten chars tuples (intro, cue, notes naming every distractor and exclusion with its meaning plus the Joyo citation, and the other dict) and `EXC={}`.
2. **Write `files\b171_render.py`** with every listed change: PARTIAL, the manual 悪戯 row plus the 戯 CW line and 悪戯.md edit, link edits for 警/握/暴 instead of addline, flexible Metadata handling, a changes assert that allows words/悪戯.md, and existence asserts for new-word exclusions and links.
3. **Run the render from b171-wt.** Resolve CHECK prints via FIX and ambiguous gaps via PICK. Then run validate, build_manifest, word_quiz_audit over the ten words (tune exclusions to 0 problems), the audit and the full gates until clean.
4. **Make the signed draft commit** "N1 B171 draft: 戒 戯 扉 扶 抄 把 抑 披 抹 露".
5. **Review and integrate:** serial blind reviews (Claude correctness → GPT consistency/quiz → Grok comprehensibility); fixes and confirmations; closure; integration with origin/main; revalidation.
6. **Publish:** signed content and receipt commits, verify both ZIPs, post the #60 checkpoint, recount (target 738 delivered / 490 missing).
7. **Continue** with B172 (拐 拒 拓 拘 拙 拠 拳 拷 挑 据) and onward.
8. **Clean up** temporaries: ..\b171-tmp.txt, ..\b170-scan, ..\b171-scan, C:\Users\romanko\b170-glcheck.txt.
</next_steps>