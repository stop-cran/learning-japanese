# Batch 138 — initial blind review (reviewer 1)

## Snapshot

- Commit under review: `b6020f9e490298de1756e33c51bf9ce314132f4e`. This is batch 138: new kanji cards 噴 垂 垣 執 堅 塊 墨 壁 壊 奏 契 奨 奪 妨 威, one changed line in the existing 張 card, and 17 word articles with link-wraps.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-138-b6020f9e`. The manifest sha256 given to me is `25d66ae4756bcc10cb638b1cf77828a1513e461cccca49bb797d21ee4a2aa415`. I did not recompute it.
- Reviewer model: Claude (Anthropic model family), working alone and read-only. I did not look for or see the other reviewer's report or the author's rationale.

## Scope

Packet files I opened ("full" means the whole file was read; "part" means line ranges, a grep, or a scripted extraction):

- `INSTRUCTIONS.md`: full
- `mechanical-checks.md`: full (as shipped, with the truncated sections)
- `evidence\source-metadata.json`: full
- `evidence\kanjidic2-records.xml`: full. I parsed it with a script and printed grade, strokes, classical radical, on, kun, nanori and English meanings for every record: all 15 kanji plus the comparison and exclusion kanji present.
- `evidence\joyo-pages.md`: full
- `evidence\daijisen-heads.txt`: full
- `evidence\kanjipedia-outside-readings.json`: full
- `evidence\okurigana-scan.txt`: full
- `evidence\jmdict-digest.tsv`: part (greps per kanji; one grep for 奨/奪/妨/威 returned truncated output)
- `evidence\jmdict-families.xml`: part. I grepped individual entries, including:
  - 1257110 かたい
  - 1133090 and 1521510 (墨)
  - 墨刑, 墨家, 米墨戦争, 縄墨
  - 障壁, 岸壁
  - 金剛不壊
  - 奏する / 奏す
  - 奨学金, 奨める
  - 業務妨害
  - 1156320 威張る
  - 威す, 威かす, 威し, 2581990 おどし
  - 1767000 しで
- `evidence\public-source\weblio-*.txt`: all 15 read in full. The 垣 extract was empty, so I fetched the live page (see below).
- `evidence\audits\reading-exposure.txt`: part (lines 1–74 plus a grep of the key lines and totals)
- `evidence\audits\reading-options.txt`: part (lines 1–30 and 149–222, plus a grep for HIT)
- `evidence\audits\quiz-safety.txt`: **not opened**. I relied on the truncated tail in `mechanical-checks.md`.
- `evidence\audits\kanji_remarks.py`, `evidence\app-code\*`, `rubric\*`: **not opened**
- `snapshot\kanji\*.md`, all 15 new cards: full
- `snapshot\kanji\張.md`: part (grep of the changed bullet and its surroundings)
- `snapshot\strokes\*.json`, all 15: part. I checked stroke counts for all 15 and the full stroke sequence of 壊 and 威.
- `snapshot\words\墨.md`: part (lines 1–47). The other 16 snapshot word articles were checked only via their diffs.
- `diffs\*`, all 18: part (the changed lines and their context, printed by script)
- `titles\kanji-titles.tsv`: part. A script checked for duplicate titles, looked up the titles of the distractors, exclusions and comparison kanji, and confirmed that 緊 and 拡 have no card.
- `titles\word-titles.tsv`: **not opened**
- `repo\docs\content-format.md`: part (headings grep; lines 71–138, the quiz and readings rules)
- `repo\kanji\団.md`: part (lines 1–14)

Public sources consulted:
- weblio Digital Daijisen pages: 垣 (live) and 威張る (live). The latter shows い‐ば・る〔ヰ‐〕【威張る】 and the separate えば・る【▽威張る】 「いばる」の音変化.
- Wiktionary entries for 奨 and 妨, for the 表外 (outside-table) on readings ソウ and ホウ.
- A kotobank attempt for 威張る redirected to an unrelated page (一応). I did not use it.

## Verdicts

Overall:

| Facet | Verdict |
|---|---|
| 1 Correctness | **Minor defects** (C1–C4). No consequential reading, sense or quiz-answer error found. |
| 2 Scoped coverage | **Pass with one minor gap** (C2, 契). Every metadata reading has a row or an explicit source-only/rare qualification. |
| 3 Consistency and quiz safety | **Pass** |
| 4 Comprehensibility | **Pass**, with optional polish only |

Per card, where it differs from "pass on all four facets":

- **堅**: facet 1 minor (C1)
- **契**: facet 1 minor and facet 2 minor (C2)
- **妨**: facet 1 minor (C3)
- **壊**: facet 1 minor (C4, a mnemonic component statement)
- **威**: facets 1 and 4 have optional wording items only (O1, O2)

All other cards pass all four facets: 噴 垂 垣 執 塊 墨 壁 奏 奨 奪. The 18 diffs also pass.

### What I verified as correct

**Front matter (all 15 cards)**
- Grade, strokes, radical, on and kun lists match `source-metadata.json` and `kanjidic2-records.xml`.
  - Stroke counts: 噴15 垂8 垣9 執11 堅12 塊13 墨14 壁16 壊16 奏9 契9 奨13 奪14 妨7 威9. These also match the stroke JSON files.
  - Grade tags: 垂 and 奏 are grade-6; the others are grade-8.
- quizOnyomi / quizKunyomi values are spelled exactly as in the full lists. Each one has its own Readings row with a linked word example:
  - 噴 フン, 垂 スイ, 執 シツ, 奏 ソウ, 契 ケイ, 奨 ショウ, 威 イ
  - 垣 かき, 奪 うば.う, 妨 さまた.げる, 壁 かべ, 墨 すみ, 壊 こわ.す / こわ.れる
- No quizzed selection is rare, name-only or dictionary-unsupported.

**Readings and senses**
- Each card's Daijisen claims match the weblio extracts: sense counts, 音 labels (呉/漢/慣), listed kun, and examples.
- The Joyo-table claims match `joyo-pages.md`. This includes:
  - the 噴く / 吹く note
  - the 執る note
  - 奨 listing only ショウ
  - 壊 listing カイ (with エ treated as described)
- Specific points checked:
  - 墨: the JMdict historical tags on 墨刑, 墨家 and 米墨戦争 are correct, and 墨西哥 is marked ateji / rarely used / usually kana.
  - 壊: 金剛不壊 is tagged yojijukugo; Daijisen does not list やぶる.
  - 奏: the title's second sense, "report to a ruler," is supported by Daijisen sense 1 (天子に申し上げる), JMdict 奏する / 奏す ("to report to the Emperor") and the KANJIDIC2 meaning "speak to a ruler." かな.でる is described accurately.
  - 奨: 奨める is a rarely used form, and ソウ is outside the table.
  - 奪: ダツ is 慣 in Daijisen; だつ is also a word element, as in 奪三振.
  - 妨: ボウ is 慣; ホウ is outside the table.
  - 威張る (JMdict 1156320) is not ateji and has the variant えばる. 威す and 威かす are rarely used forms; 威し is an alternative form. weblio confirms いばる (ヰ) and えばる.
- 塊: the claim that 団 also has the kun reading かたまり is true (`repo\kanji\団.md`: `kunyomi: [かたまり, まる.い]`).

**Diffs**
- All 17 word diffs change exactly one line. Each wraps the first mention, in the "How the kanji combine" section, as `[X](../kanji/X.md)`, and each link targets the intended new card. Nothing else changes.
  - In the 墨 word article, an earlier bare 墨 in the Meaning section stays unlinked. This follows the existing convention of linking within the composition section, and I do not count it as a defect.
- The 張 card's bullet:
  - It now links 威 and quotes "intimidate; authority; dignity", the exact title of 威.md.
  - It keeps the statement that 緊 and 拡 have no cards, which is true per `kanji-titles.tsv`.
  - The passage still reads grammatically.

**Quiz safety**
- Titles are unique corpus-wide.
- Every distractor title is plausible as a guess but defensibly wrong in both directions. Distractor sets are listed under lead (j).
- Exclusion lists are direct synonym or confusable pairs (see lead (i)).
- Section order and headings follow `content-format.md`.

## Findings

Established defects, all of minor severity: no quiz answer is wrong and no reading is misattributed in a way that would mislead a learner.

**C1 — 堅: incomplete "other two spellings" claim.**
- The card says 硬い and 固い are "the other two spellings in JMdict's かたい entry."
- JMdict entry 1257110 (かたい) also lists 緊い (tagged irregular kanji form). JMdict therefore has three other kanji spellings, not two.
- Fix: say "the other common spellings" or "besides the irregular 緊い."

**C2 — 契: the outside-table on readings are misattributed and omitted.**
- The card says 契丹 きったん's "reading belongs to the whole word" (a whole-word reading, like jukujikun).
- That is inaccurate. きっ is the on reading キツ of 契, with the usual gemination before た. Kanjipedia records キツ as one of 契's readings outside the official table (`kanjipedia-outside-readings.json`: キツ, ケツ, セツ).
- The card also does not mention ケツ or セツ at all. Daijisen even has a separate headword せつ【契】 (the legendary figure Xie).
- None of these is quizzed, and reading-exposure shows no production collision. This is an accuracy and scoped-coverage point.
- Fix: replace the whole-word statement with one sentence: "契丹 uses an outside-table reading キツ; Kanjipedia also lists ケツ and セツ, none used in everyday words."

**C3 — 妨: the Daijisen example claim is understated.**
- The card says Daijisen's example is 妨害, in the singular.
- The Daijisen character entry (weblio extract) gives two examples, 妨害 and 押妨.
- Fix: "Its examples are 妨害 and the rare 押妨", or "examples include 妨害."

**C4 — 壊: the mnemonic understates the bottom-right shape.**
- The card's mnemonic describes the lower right as "like the lower part of 衣."
- The stroke data for strokes 11–16 show a complete 衣-like shape under 罒: a short top vertical and horizontal, then the four remaining strokes. The count confirms it: 土 3 + 十-top 2 + 罒 5 + 衣-shape 6 = 16.
- So the shape is effectively the whole of 衣 split around 罒, not just its lower part. This is a component statement in the modern-shape mnemonic, so facet 1 requires it to be true.
- Fix: "罒 sits inside a split 衣" or "the bottom looks like the lower half of 衣, whose top sits above 罒."

## Optional

Polish, not defects.

- **O1 — 威, frame wording.** The card calls the frame's top "a short horizontal stroke." In the stroke data, stroke 2, the top horizontal, is long; the short horizontal is the inner one above 女. Suggest "a long top stroke".
- **O2 — 威, "native verb" wording.** The card calls 威張る "a native verb whose reading is learned as a whole" but also presents 威 as supplying イ in it. Daijisen writes い‐ば・る〔ヰ‐〕, i.e. い = イ (ヰ) plus はる. Calling it a mixed on + kun compound would be clearer and not contradictory.
- **O3 — 威, armor-lacing おどし.** Both JMdict 2581990 and Daijisen (おどし【▽威／×縅】) give the armor-lacing sense. A half-sentence would round out the おど.し row.
- **O4 — 執, と.る examples.** Only 執る is shown for と.る. The common 執り行う or 指揮を執る would make the Joyo-table note concrete.
- **O5 — 噴, ホン and は.く.** Mentioning these source-only readings (Kanjipedia, KANJIDIC2 context) in one clause would explain why the reading-options audit flags ほん.
- **O6 — 垂, しで.** Kanjipedia lists the outside-table reading しで (JMdict 1767000 紙垂 / 垂, Shinto paper streamers). It could join the existing source-only qualification of しだれ / なんなんとす.
- **O7 — Minor source-only readings.** 壁 がけ, 墨 モク and 奪 タツ could each get a one-clause mention, like the other qualified rare readings.
- **O8 — 奏, 功を奏する.** This very common N1 idiom would illustrate ソウ and the "report / present" sense well.
- **O9 — Audit labels.** `reading-options.txt` labels 噴 ほん and 契 けつ "HIT (can be drawn)", while `reading-exposure.txt`, which models the actual N1/All/Starter pools, shows them not drawable. Harmonising the two audits' wording would prevent false alarms.

### Leads (a)–(k)

**(a) 執**
- The card's account of シュウ (執着/執念, with 執着 also read しゅうちゃく / しゅうじゃく) and of と.る with the Joyo-table note on 執る is accurate.
- KANJIDIC2 し is a nanori, a name-only reading, so not selecting it is correct.
- reading-exposure shows し as drawable in a Starter practice session. Marking し wrong there is defensible: it is a name reading and not a reading of the character in ordinary words. Not a defect; see O4.

**(b) 垂**
- た.れる, た.らす, た.れ and -た.れ are explained through 垂れる / 垂らす and words with 垂れ.
- なんなんと.す and しだれ are correctly qualified as dictionary-only or rare.
- Not quizzing the kun readings is a defensible editorial choice. Not a defect; see O6.

**(c) Listed but not quizzed**
- 塊 カイ/ケ, 壊 カイ/エ, 堅 ケン, 壁 ヘキ, 墨 ボク, 奪 ダツ and 妨 ボウ each have accurate rows or text. The non-quizzed status is clear from the quiz lists and the prose.
- 塊 つちくれ and 壊 やぶ.る are explicitly qualified as source-only.
- Not a defect.

**(d) 奏**
- The second title sense is supported (see Verdicts), and the かな.でる account is accurate.
- Not a defect; see O8.

**(e) 契**
- ちぎ.る (契る) is accurate.
- The outside-table readings are covered by C2.
- The distractors 大, 天 and 分 have clearly distinct titles and are defensibly wrong. 大 is the bottom component, which makes it a fair visual lure.

**(f) 噴**
- フン, ふ.く and the Joyo note distinguishing 噴く from 吹く are accurate.
- On ホン and は.く, see O5.
- The distractors 口, 古 and 買 have distinct titles and are fine.

**(g) 威 and 張**
- イ, おど.す, おど.し and おど.かす are accurate. JMdict marks 威す and 威かす as rarely used, and the card reflects that.
- The 張 bullet is correct.
- On wording, see O1–O3.

**(h) Rare readings**
- 垣 エン, 堅 -がた.い and 奨 ソウ / すす.める are handled accurately.
- 墨 モク, 壁 がけ, 奪 タツ and 妨 ホウ are either qualified or harmlessly unmentioned (O7).
- Not a defect.

**(i) Exclusions**
- 垣: 塀 囲 境 界 関 限
- 執: 取 握 持 捕 履 司
- 堅: 硬 固 剛 勁 強 厳
- 奏: 演 弾 楽 遊 申 報 告
- 威: 権 力 勢 厳 圧 恐 怖 慢
- 垂: 掛 滴 下 低
- 噴: 吹 吐 爆 発

Each pair rests on an overlapping displayed title or ordinary sense of the target, e.g. 履 "perform; put on" against 執 "carry out". Some are wide but direct, not transitive cliques. Excluding a pair cannot make a quiz wrong; at worst it slightly shrinks the pool. Not a defect.

**(j) Distractors**
- 垂: 郵 乗 重
- 墨: 墓 型 堂
- 壁: 辛 基 坂
- 奨: 美 奥 奇
- 妨: 姉 始 旅
- 塊: 魅 城 場

These are mostly shape lures (shared 土/女/大 parts or a similar top). Their displayed titles do not overlap the targets' meanings in either direction, so each is a plausible but defensibly wrong answer. Not a defect.

**(k) Audits**
- The 8 "attested reading … offered by …" latent collisions are not drawable in production pools: ほど 塊, がけ 壁, きつ/せつ 契, とる 奪, はく 噴, and the rest.
- The two HIT labels are an audit-model mismatch (O9), not a content defect.

## Limits

- **Execution-rule breach:** in one response early in the review, I issued two tool calls together (a view of `daijisen-heads.txt` and a web fetch of the weblio 垣 page). Every other response used exactly one call.
- I treated the pinned JMdict (2026-11-17) and KANJIDIC2 (2026-11-02) extracts in the packet as authoritative where they differ from the live dictionaries. For Daijisen I relied on the packet's weblio extracts and two live weblio pages.
- Not opened:
  - `quiz-safety.txt` in full (I relied on the truncated tail in `mechanical-checks.md`)
  - `word-titles.tsv`, `app-code\`, `rubric\`, `kanji_remarks.py`
  - 16 of the 17 snapshot word articles beyond their diffs
- Quiz-safety conclusions rest on the card front matter, `kanji-titles.tsv` and `reading-exposure.txt`.
- One digest grep (奨/奪/妨/威) returned truncated output; I compensated with entry-level greps in `jmdict-families.xml`.
- For C4 I assumed that the stroke JSON order is the standard order, and that "lower part of 衣" means the strokes below 罒 only.
- My quotations of card wording in C1–C3 and O1–O2 come from my reading of the cards earlier in the session; they may differ in punctuation from the source text.
- I did not recompute the packet manifest hash.
