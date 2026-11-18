# Batch 137: initial blind review (reviewer 1)

Reviewer model: Claude (Anthropic), working alone and read-only, with no access to the other reviewer's report or the author's rationale.

## Snapshot

- Commit: d3c7394d38992b24d3689bc984fdb4a6cf60bc54 (batch 137).
- New kanji cards: 丁 井 仰 但 傑 傷 僕 卸 司 吐 呂 哀 哲 唯 善.
- Packet: `C:\Users\romanko\n1-kanji-workspace\review-packets\batch-137-d3c7394d`. I took the packet-manifest sha256 bd69f948… from the assignment and did not recompute it.

## Scope

**Unit reviewed:**
- 15 new cards in `snapshot\kanji\`.
- 15 stroke files in `snapshot\strokes\`.
- 23 diffs in `diffs\`: 21 word articles plus the changed lines of `kanji\寧.md` and `kanji\敷.md`.

**Packet files opened:**

| File | How it was read |
| --- | --- |
| `INSTRUCTIONS.md` | In full. |
| `mechanical-checks.md` | In full (as truncated by the packet). |
| `snapshot\kanji\` 丁 井 仰 但 傑 傷 僕 卸 司 吐 呂 哀 哲 唯 善 (`.md`) | In full, all 15. |
| `snapshot\kanji\寧.md` | In part: lines 76–92, the context of the changed bullet. |
| `snapshot\kanji\敷.md` | Not opened separately. I judged it from its diff, which carries the full changed line. |
| `snapshot\strokes\*.json` (15 files) | Parsed in full by a script that checked keys, `strokeCount` and stroke-array length. I did not inspect the stroke paths visually. |
| `diffs\*.diff` (23 files) | In part: every `---`/`+++`/`@@` header and every `-`/`+` line. Unchanged context lines were not printed, but each hunk header shows its location. |
| `evidence\source-metadata.json` | In full. |
| `evidence\kanjidic2-records.xml` | In full, through a script that parsed every `<character>` (grade, strokes, radical, on/kun, nanori, English meanings). |
| `evidence\joyo-pages.md` | In full. |
| `evidence\daijisen-heads.txt` | In full. |
| `evidence\kanjipedia-outside-readings.json` | In part: the first ~2,500 characters, which cover 丁 through part of 唯. |
| `evidence\jmdict-families.xml` | In part: every entry id cited in the 15 cards' Metadata lines, plus other entries looked up by id. |
| `evidence\jmdict-digest.tsv` | In part: rows filtered by kanji (丁 井 仰 但 傑 傷 僕 卸 哲 唯 善) and pattern searches (写経, みこともち, たんだ, よほろ, ぬかす). |
| `evidence\public-source\weblio-<kanji>.txt` (15 files) | In part: the leading Daijisen character entry and nearby text of each. |
| `evidence\audits\quiz-safety.txt` | In full (45 lines). |
| `evidence\audits\reading-exposure.txt` | In part: lines 1–25, every "attested reading" line with its prompt header, and the last two summary lines. |
| `titles\kanji-titles.tsv` | In part: filtered by character. |
| `titles\word-titles.tsv` | In part: filtered by word. |
| `repo\docs\content-format.md` | In part: a heading/keyword grep and lines 71–139 (the Kanji card, Quiz authoring and Curated reading questions sections). |

**Not opened:**
- `evidence\okurigana-scan.txt`
- `evidence\app-code\*`
- `rubric\*`
- `repo\kanji\*` and `repo\words\*` individual files
- `snapshot\words\*.md` (word changes were judged from the diffs)

**Public web:** live Weblio Digital Daijisen page for 卸 (https://www.weblio.jp/content/卸), opened before my context was compacted.

## Verdicts

Overall, across all 15 cards, the 15 stroke files and the 23 diffs:

| Facet | Verdict | Basis |
| --- | --- | --- |
| 1. Correctness | **NEEDS FIX** | Finding C1 only: 16 quoted card titles do not match the cited card's exact title. Every reading, gloss, register label, Joyo-table claim, Daijisen claim, mnemonic component and stroke statement I checked is true. |
| 2. Scoped coverage | **CLEAN** | Every metadata reading has a row or is explicitly qualified as source-only. No important family word is wrongly omitted or misdescribed. Polish suggestions are under Optional. |
| 3. Consistency and quiz safety | **NEEDS FIX** | Finding C1 is also a cross-card consistency defect, because the quoted titles do not match the linked cards. Titles, distractors, exclusions, quiz-reading links, tags, grades, strokes and links are otherwise clean. |
| 4. Comprehensibility | **CLEAN** | Optional polish only. |

Per file, where a file differs from the overall verdicts:

| File | 1 Correctness | 2 Coverage | 3 Consistency/quiz | 4 Comprehensibility |
| --- | --- | --- | --- | --- |
| 丁 仰 但 傑 僕 司 吐 呂 哲 善 (10 cards) | NEEDS FIX (C1) | CLEAN | NEEDS FIX (C1) | CLEAN |
| 井 傷 哀 唯 | CLEAN | CLEAN | CLEAN | CLEAN |
| 卸 | CLEAN* | CLEAN | CLEAN | CLEAN |
| strokes (15 files) | CLEAN | — | CLEAN | — |
| 23 diffs | CLEAN | — | CLEAN | CLEAN |

*卸: the card says Daijisen has a headword おろし written 卸（し）. The packet's `weblio-卸.txt` contains no definition text, and `daijisen-heads.txt` says no headword lists this form. The live Weblio page does show おろし【卸（し）】《「下ろし」と同語源》, so the claim is true, but the packet evidence alone does not support it (see Limits).

## Findings

### C1 — Quoted titles with a comma lose their space, so they are not the exact card titles

- **Severity:** minor.
- **Facet:** 1 (correctness: "every double-quoted … title … must be the exact title of the cited card") and 3 (consistency).
- **Claim and impact:**
  - When a linked card's title contains ", " (comma plus space), these cards quote it with the space removed: "town,neighborhood" instead of "town, neighborhood".
  - Titles separated by "; " are quoted correctly everywhere. A few ", " titles are also quoted correctly, for example 業 "work, occupation" in 僕, 土 "earth, soil" in 吐, and 地 "ground, land" in 敷. So this is a generation inconsistency, not a house style.
  - The quotes are not the exact titles the reader sees on the linked cards, and on a phone "see,look" reads as a typo.
  - Meaning is not affected.
- **All 16 instances (12 cards share the defect pattern in total, but 井 傷 卸 哀 唯 have none):**

  | Card:line | Quoted | Actual title |
  | --- | --- | --- |
  | 丁.md:68 | "town,neighborhood" | 町 "town, neighborhood" |
  | 仰.md:58 | "see,look" | 見 "see, look" |
  | 仰.md:58 | "up,above" | 上 "up, above" |
  | 但.md:27 | "sun,day" | 日 "sun, day" |
  | 但.md:47 | "daytime,midday" | 昼 "daytime, midday" |
  | 傑.md:27 | "tree,wood" | 木 "tree, wood" |
  | 傑.md:46 | "make,produce" | 作 "make, produce" |
  | 傑.md:47 | "body,form" | 体 "body, form" |
  | 僕.md:50 | "serve,attend" | 仕 "serve, attend" |
  | 司.md:55 | "same,equal" | 同 "same, equal" |
  | 司.md:56 | "public,official" | 公 "public, official" |
  | 吐.md:48 | "spirit,air" | 気 "spirit, air" |
  | 吐.md:49 | "company,shrine" | 社 "company, shrine" |
  | 呂.md:52 | "goods,refinement" | 品 "goods, refinement" |
  | 哲.md:55 | "reason,logic" | 理 "reason, logic" |
  | 善.md:58 | "correct,proper" | 正 "correct, proper" |

- **Remedy:** restore the space after the comma in each quote, then re-grep all 15 cards for `"[^" ]+,[^ "]`.
- **Evidence:**
  - `titles\kanji-titles.tsv` rows for 町 見 上 日 昼 木 作 体 仕 同 公 気 社 品 理 正.
  - The same titles appear with spaces as displayed options in `evidence\audits\quiz-safety.txt`, for example "daytime, midday", "body, form", "same, equal", "company, shrine", "goods, refinement".
  - A regex grep over the 17 snapshot cards found exactly these 16 matches and none in 寧 or 敷.
- **Confidence:** high.

No other established defects.

**What I verified as correct, per card (for both reviewers' reconciliation):**

- **丁**
  - Front matter matches KANJIDIC2: grade 3, 2 strokes, radical 1; on チョウ テイ チン トウ チ; kun ひのと.
  - Joyo p.109 rows: チョウ 丁数/落丁/二丁目 and テイ 丁字路/甲乙丙丁.
  - Daijisen senses (チョウ 3, テイ 6), the 難読 丁幾 チンキ, and the ▽よほろ headword.
  - JMdict:
    - 丁 てい/ひのと (1581740): sense 1 is restricted to てい; sense 2 is esp. ひのと.
    - 丁幾: ateji and a rarely used form.
    - 丁々 とうとう (2857308).
    - 丁夜: archaic.
    - 馬丁: dated.
  - Lead (a): the account of チン, トウ, チ and ひのと is accurate. The よほろ statement is true for a standalone entry (see O1).
- **井**
  - Daijisen: 4 セイ senses plus ショウ.
  - JMdict:
    - 井然 is listed after 整然.
    - 井目 is listed after 星目.
    - 井蛙, 鑿井.
  - Joyo p.89: セイ 油井/市井, ショウ 天井, い 井戸.
  - Lead (e) セイ/ショウ: correct.
- **仰**
  - JMdict:
    - 仰っしゃる is a search-only form of 仰る (1238840).
    - 仰る is honorific and usually kana.
    - 仰ぐ senses.
    - 欽仰, 景仰, 渇仰 かつごう, 仰天.
  - Daijisen: コウ is 慣 and ゴウ is 呉; kun あおぐ おおせ おっしゃる.
  - Joyo p.40: ギョウ 仰視/仰天/仰角, コウ 信仰, あおぐ, おおせ.
  - Quizzing コウ (with the linked 信仰) rather than ギョウ is defensible.
- **但**
  - JMdict:
    - 但し (1416190): usually kana.
    - ただ (1538900): 但 is a rarely used form; the conjunction sense is esp. 但.
    - 播但線 タン (5587321).
  - Joyo p.105 has ただし only.
  - Lead (e) タン: correct.
- **傑**
  - JMdict:
    - 傑れる is a search-only form of 優れる.
    - 傑作 sense 2 is jocular and dated.
    - Compound glosses checked: 傑出, 傑物, 英傑, 豪傑, 怪傑, 俊傑, 女傑.
  - Joyo p.46: 傑物, 傑作, 豪傑.
  - Lead (e) すぐ.れる: correct.
- **傷**
  - Daijisen: 3 ショウ senses, and 火傷 in 難読.
  - JMdict:
    - 火傷 やけど is gikun (1577310).
    - 火傷 かしょう (2859761).
    - 傷む/傷める are listed under 痛む/痛める.
    - Compound glosses checked: 軽傷, 重傷, 中傷, 外傷, 損傷, 感傷, 負傷, 傷害, 傷心.
  - Joyo p.81.
  - Lead (c): the card and the 火傷 article both present やけど as a whole-word special reading. That is accurate and consistent.
  - The exclusions 害, 損 "loss; damage" and 痛 "pain; hurt" correctly guard the overlap with "damage".
- **僕**
  - JMdict:
    - ぼく: male "I", colloquial "you", archaic "manservant".
    - やつがれ: archaic, humble.
    - しもべ: usually kana.
    - Compound glosses checked: 下僕, 公僕, 忠僕, 家僕, 従僕, 老僕.
  - Daijisen: the reading ぼく among Meiji students.
  - Joyo p.143: ボク 僕/公僕.
  - The exclusions 私 "I; private" and 我 "self; I; ego" are correct.
- **卸**
  - JMdict:
    - 卸す: 3 senses.
    - 卸/卸し おろし (1589530).
    - 卸下 しゃが (2537870).
    - 卸商, 棚卸し.
  - Joyo p.19: おろす 卸す ⇔ 下ろす・降ろす; おろし 卸/卸商.
  - Lead (e) シャ/おろし: correct.
- **司**
  - KANJIDIC2: grade 4, 5 strokes, radical 30; on シ; kun つかさど.る; nanori つ・つか・つかさ.
  - Weblio Daijisen:
    - ［音］シ, ス（唐）; ［訓］つかさどる, つかさ.
    - 3 senses, with 司書, 上司 and 写経司.
    - 難読 下司・公司.
    - Separate headwords つかさ【▽官/▽司】 and みこともち【▽宰/▽司】.
  - JMdict:
    - 司る: two senses, including "to rule; to govern; to control".
    - 公司: コンス/こうし.
    - つかさ (2251080): "office; official".
    - 下司 げす, 行司 (sumo, "referee"), 宮司 ぐうじ, 司令, 国司 (historical term), 保護司.
    - No 写経司 or みこともち entry in the digest.
  - Joyo p.64: シ 司会/司令/上司.
  - Mnemonic: 𠃌 frame, short horizontal and 口 = 1+1+3 = 5 strokes. True.
  - Lead (e): the card's account of ス and つかさ is accurate.
- **吐**
  - JMdict:
    - 吐く はく (2646460): 4 senses.
    - 吐く つく (1444150): usually kana.
    - ため息をつく, also written 溜息を吐く.
    - 吐血, 吐露, 嘔吐, 反吐, 音吐朗々 (yojijukugo, "in a clear voice"), 吐瀉, 音吐, 呑吐 (formal/literary).
  - Daijisen:
    - One ト sense.
    - ［訓］はく only.
    - 難読 反吐.
    - Separate つく headword.
  - Joyo: ト 吐露/吐血/音吐朗々; はく 吐く/吐き気.
  - 土 is read ト, so the mnemonic's sound remark is true.
  - The distractor comparisons hold: 叫 and 吸 have 口 at the left, and 社 has 土 at the right.
- **呂**
  - JMdict:
    - 風呂 (1500100): not marked ateji.
    - お風呂.
    - 風呂敷.
    - 呂 りょ (2240210): music, abbreviation, "bass range (in Japanese music)". This supports the title.
    - 律呂, 大呂, 南呂, 語呂, 呂律, 背骨 せぼね (no 呂 spelling), 露天風呂 ろてんぶろ.
  - Daijisen:
    - ［音］ロ（呉）, リョ（漢）.
    - 〈リョ〉 雅楽などで陰の調子 (大呂, 南呂, 律呂).
    - 〈ロ〉 当て字 (語呂, 風呂).
    - 難読 呂律.
    - No ［訓］.
  - Joyo p.159: ロ 風呂 only.
  - Lead (b): the card's account of the spelling 風呂 is accurate. Daijisen marks ロ as ateji, JMdict does not mark 風呂, and the Joyo table lists 風呂 under ロ. The accounts of リョ and of せぼね as source-only are also accurate.
  - Mnemonic: 口 + short stroke + 口 = 7 strokes. True. 営 does contain 呂.
- **哀**
  - JMdict:
    - 哀れ: noun, na-adjective and interjection.
    - 哀れむ.
    - 悲しい/哀しい (1483190): main spelling 悲しい.
    - 可哀想/可哀相: ateji, usually kana.
    - 哀れがる: archaic.
    - 哀愁, 哀憐, 哀願, 悲哀, 哀れみ, 哀歓, 哀悼, 哀訴.
  - Daijisen: ［訓］あわれ, あわれむ, かなしい; 3 senses; 難読 可哀相.
  - Joyo p.11: アイ 哀愁/哀願/悲哀; あわれ 哀れ/哀れな話/哀れがる; あわれむ 哀れむ/哀れみ.
  - Mnemonic: 衣 split around 口, 6+3 = 9 strokes. True. 裏 and 袋 do contain 衣.
  - Lead (e) かな.しい: correct.
- **哲**
  - Daijisen: ［音］テツ only and no ［訓］; 3 senses with 明哲, 先哲 and 印哲; also 哲人, 哲理, 賢哲, 十哲, 中哲.
  - JMdict:
    - さとい: 聡い/敏い (2087260).
    - あきらか: 明らか (1532310).
    - Neither entry has a 哲 spelling.
  - Joyo p.114: テツ 哲学/哲人/先哲.
  - Mnemonic: 折 (7) + 口 (3) = 10 strokes. True. 近 and 祈 contain 斤.
  - Lead (e) さとい/あきらか: correct.
- **唯**
  - JMdict:
    - 唯一 ゆいいつ/ゆいつ (1538920).
    - ただ (1538900): 唯 is a rarely used form; sense "only; merely; just; simply" is usually kana.
    - 唯でさえ: usually kana.
    - 唯々諾々: yojijukugo.
    - 唯我独尊: both senses.
    - 唯美主義, 唯識, 唯物論, 唯心論.
    - No たんだ entry with 唯.
  - Daijisen: 〈ユイ〉ただ…だけ and 〈イ〉「はい」という承諾の返事.
  - Joyo p.150: ユイ 唯一/唯物論/唯美主義; イ 唯々諾々.
  - Lead (d): the card's accounts of イ, ただ and たんだ are accurate. On the KANJIDIC2 name reading ゆ, see (h) below.
- **善**
  - JMdict:
    - 善 ぜん: antonym 悪.
    - 良い/好い/善い (1605820): えい is out-dated kana.
    - いい人/善い人 (1835630): いいひと is permitted for 善い人.
    - 良く/善く (1605870): usually kana.
    - 良しとする (2805980): no 善 spelling.
    - 善人, 善処, 親善, 善悪, 慈善, 善行, 最善, 偽善, 善戦, 善後策, 善隣.
  - Daijisen:
    - ［訓］よい, よく, よくする.
    - 3 senses.
    - Separate ぜん headword "⇔悪".
    - え・い headword.
  - Joyo p.96: ゼン 善悪/善処/慈善; よい 善い ⇔ 良い.
  - 良 and 好 do have the kun よ.い and い.い.
  - Mnemonic arithmetic is true: 羊 top (6) + 丷 (2) + 一 (1) + 口 (3) = 12.
  - Lead (e) い.い/よ.く/よし.とする/えい: correct.

**Strokes:** each of the 15 JSON files has `strokeCount` and a stroke array whose length equals the card's `strokes` value (2, 4, 6, 7, 13, 13, 14, 9, 5, 6, 7, 9, 10, 11, 12).

**Diffs (23):**
- **20 word diffs:** each changes exactly one line, and the only change is wrapping the first mention of the new kanji in a `../kanji/<kanji>.md` link to the intended card. The files are お風呂, 丁寧, 井戸, 但し, 信仰, 傑作, 傷, 僕, 包丁, 卸す, 司会, 吐き気, 吐く, 哀れ, 哲学, 唯一, 善, 改善, 風呂 and 風呂敷.
  - In 吐き気, the link wraps 吐 inside 吐き. That renders correctly.
- **火傷:** the diff wraps 傷 and deletes the stale "no kanji card" paragraph together with its blank line. The remaining passage reads correctly.
- **寧:** the two-line bullet becomes "In 丁寧, [丁](丁.md), "city block; even number; fourth," supplies テイ." The title is exact and the sentence is true (Joyo テイ; 丁寧 ていねい).
- **敷:** the line now links [呂](呂.md) with the exact title "spine; backbone; bass range", and the sentence still reads correctly.
- No Dictionary: line is touched.

**Leads (f), (g), (h):**
- **(f) Exclusions.** All are direct pairs, not cliques. Some are only weak overlaps: 井–額, 卸–擦/削 (via "grate"), 丁–偶/四, 司–営/治/御. Each has a stated basis and is harmless, because every new card has three curated distractors (quiz-safety shows 3/3 for all 15).
- **(g) Distractors.** The listed distractors are all defensibly wrong in both directions from the displayed titles: 傑 舞/休/体, 僕 業/億/偉, 吐 叫/吸/社, 哀 衣/裏/袋, 善 羊/着/差, 呂 口/品/営. 吐–吸 ("inhale; suck in") is an antonym pair, not an overlap.
- **(h) Reading exposure.** All 8 "attested reading … offered by" lines are marked "cannot be drawn in the N1 stack, All stack or Starter practice session pool". Neither these nor 唯 ゆ (offered by 油/由/輸/遊; name-only) is a shipped collision.

## Optional

- **O1 (丁, facet 1, nuance).** The card says JMdict has no entry for よほろ. That is true for a standalone headword, but JMdict 仕丁 (2829360) includes the reading つかえのよほろ. Consider "no standalone entry".
- **O2 (傑, facet 1/4).** The Readings row glosses 傑作 as "masterpiece; hilarious absurdity" without JMdict's jocular and dated labels on the second sense. Consider "(jocular, dated)".
- **O3 (卸, facet 1).** 卸下 しゃが is a military term (JMdict field: military). The card could say so.
- **O4 (facet 3).** The weak exclusions 井–額 and 司–営/治/御 could be dropped to keep exclusion lists focused on real near-synonyms. They are not wrong.
- **O5 (哲, facet 2).** The common set phrase 何の変哲もない (なんのへんてつもない, JMdict 1642670) could be a useful "you will meet this" example. It is not required.
- **O6 (facet 2).** Kanjipedia's outside-table readings 吐 ぬ.かす, 哀 かな.しむ, 傷 そこ.なう, 仰 あおの.く/の.く and 但 ダン are not in KANJIDIC2 and are not mentioned. That is acceptable under the scoped-coverage rule. A one-line "other dictionaries also list …" note would be optional.
- **O7 (all cards, facet 4).** The final "For reference, more Daijisen examples …" bullets and the repeated "Being outside the practice set is not proof …" sentence add length for an N5–N4 phone reader. Consider trimming or collapsing them.

## Limits

- **Tool calls.** I issued exactly one tool call per response throughout and no parallel calls, sub-agents or background jobs. Several PowerShell calls read or filtered more than one packet file inside a single command. That is still one tool call.
- **Context compaction.** My context was compacted midway, after reviewing 丁 through 卸. My verification of those eight cards is summarized from my own notes made at the time. The line numbers in C1 were re-derived afterwards by a grep over the snapshot.
- **卸 Daijisen headword.** `evidence\public-source\weblio-卸.txt` has no definition text, and `daijisen-heads.txt` reports no headword for 卸（し）. I verified the card's おろし【卸（し）】 claim only on the live Weblio page.
- **Public checks.** Apart from the live Weblio 卸 page, my public-dictionary verification used the packet's captured Weblio/Daijisen extracts and the JMdict and KANJIDIC2 snapshots. I did not open Jisho, Kotobank or Kanjipedia pages live.
- **Joyo indentation.** `joyo-pages.md` does not preserve the table's 1字下げ indentation, so I could not verify any indentation-dependent ("special or narrow use") claim. As far as I saw, no card makes one.
- **Labels in the exposure audit.** reading-exposure.txt labels some extras "(card text)", for example 吐 ぬかす and 哀 かなしむ, that I did not find in the card text. They come from Kanjipedia or the okurigana scan. This is a labelling issue in the evidence tool, outside scope, and changes no verdict.
- **Files not opened.** `okurigana-scan.txt`, the app code, the rubric, the `snapshot\words\` files (judged from the diffs) and the parts of `kanjipedia-outside-readings.json` after 唯.
- **Section order.** I assumed the cards' section order (Meaning and origin, Readings, Common words, Notes, then Metadata/Usage) is the current house layout. The part of content-format.md I read does not prescribe heading order, and all 15 cards follow the same layout.
- **Known limits.** The Android JVM tests and the Kotlin cross-check were not run at this snapshot. These are known packet limits and are not reported.
