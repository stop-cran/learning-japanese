# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 30
WARN  words/一斉.md: Dictionary: line cites no JMdict entry id
WARN  words/体操.md: Dictionary: line cites no JMdict entry id
WARN  words/振り仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/振舞う.md: Dictionary: line cites no JMdict entry id
WARN  words/斜.md: Dictionary: line cites no JMdict entry id
WARN  words/平仮名.md: Dictionary: line cites no JMdict entry id
0 error(s), 6 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 30
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
挙 (raise; cite; hold (an event))  options: roll; book volume | search | sweep; brush
    reading あ.げる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
振 (wave; swing; allocate)  options: lips | worship; bow in respect | dig; excavate
    reading ふ.る    (kun): wrong options from distractors 3/3 (rest filled from other cards)
挿 (insert; plant a cutting)  options: discard; abandon | worship; bow in respect | grip; grasp
    reading さ.す    (kun): wrong options from distractors 3/3 (rest filled from other cards)
掌 (palm (of the hand); administer)  options: hall | political party; faction | shoot; strike
    reading ショウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
推 (infer; recommend; push forward)  options: only; solely; merely | fiber | miscellaneous
    reading スイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
描 (draw; depict; sketch)  options: push | grip; grasp | dig; excavate
    reading えが.く   (kun): wrong options from distractors 3/3 (rest filled from other cards)
提 (submit; propose; carry in hand)  options: hoist; lift; deep-fry | search | invite
    reading テイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
揮 (wield; command; display)  options: carry; luck | shoulder; take on | pick up; gather
    reading キ      (on): wrong options from distractors 3/3 (rest filled from other cards)
揺 (shake; sway; waver)  options: enter, put in | see, look | rest
    reading ゆ.れる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
操 (operate; manipulate; fidelity)  options: goods, refinement | tree, wood | worship; bow in respect
    reading ソウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
故 (reason; former; the late; mishap)  options: attack; go on the offensive | rescue; save; relief | teach, instruct
    reading コ      (on): wrong options from distractors 3/3 (rest filled from other cards)
敵 (enemy; opponent; rival)  options: respect; honor | rescue; save; relief | scatter
    reading テキ     (on): wrong options from distractors 3/3 (rest filled from other cards)
斉 (uniform; all together; simultaneous)  options: sentence, writing | oppose; face | intersect; mingle
    reading セイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
斎 (purification; abstinence; study room)  options: sea, ocean | every, each | buy
    reading サイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
斜 (diagonal; slanting; oblique)  options: surplus | remove; exclude | route; course
    reading なな.め   (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading はす     (kun): wrong options from distractors 3/3 (rest filled from other cards)
existing cards that fall back to tag-similar options: 11
    人 (person) curated slots used 2/3
    休 (rest) curated slots used 2/3
    何 (what) curated slots used 2/3
    入 (enter, put in) curated slots used 2/3
    出 (go out, exit) curated slots used 2/3
    口 (mouth) curated slots used 2/3
    女 (woman, female) curated slots used 2/3
    日 (sun, day) curated slots used 2/3
    月 (moon, month) curated slots used 2/3
    男 (man, male) curated slots used 2/3
    買 (buy) curated slots used 2/3
0 error(s), 0 warning(s)
```

## reading exposure (tail; full file in evidence\audits)

```text
(the pool grows by that card): not drawable with any single holder (1 holders tried)
       attested reading い (card text) is offered by 以 位 依 偉 医 囲 委 威 (+8 more); it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [斎 以] -> い; [斎 位] -> い
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (16 holders tried)
       attested reading ゆ (card text) is offered by 愉 油 由 輸 遊; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [斎 愉] -> ゆ; [斎 油] -> ゆ ゆう
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (5 holders tried)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 3 of 3 drawable wrong options seen
   kun: no reading prompts
== 斜 (diagonal; slanting; oblique)   curated option cards: 余 除 途   tags: jlpt-n1 grade-8 structure-unclassified
   curated 余: tags jlpt-n3 grade-5 structure-unclassified; in pools: N1 stack, All stack; on ヨ | kun あま.る あま.り あま.す あんま.り
   curated 除: tags jlpt-n3 grade-6 structure-unclassified; in pools: N1 stack, All stack; on ジョ ジ | kun のぞ.く -よ.け
   curated 途: tags jlpt-n3 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ト | kun みち
   JMdict single-kanji entries: 1322400: slanting, tilted, sloping -> ななめ・なのめ; 2085880: diagonal -> はす・しゃ
   unlisted readings attested for 斜: なのめ (card text, JMdict 1322400)  なのめならず (card text)
   on: no reading prompts
   kun prompt なな.め (key ななめ)
       N1 stack: curated 余 除 途 -> 8 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       All stack: curated 余 除 途 -> 8 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 7 drawable wrong options (0 curated, 7 fallback)
       sampling N1 stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling All stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 7 of 7 drawable wrong options seen
   kun prompt はす (key はす)
       N1 stack: curated 余 除 途 -> 8 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       All stack: curated 余 除 途 -> 8 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 3 drawable wrong options (0 curated, 3 fallback)
       sampling N1 stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling All stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 3 of 3 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 12 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 斉 (uniform; all together; simultaneous)   curated option cards: 文 対 交
   metadata readings: on セイ サイ | kun そろ.う ひと.しい ひと.しく あたる はやい
   unlisted readings attested for 斉: ととのえる (card text)  ものいみ (card text)  ととのう (card text)  ただ (KANJIDIC2 name reading)  なり (KANJIDIC2 name reading)  ひと (KANJIDIC2 name reading)  ひとし (KANJIDIC2 name reading)
   on prompt セイ (key せい)
       excluded keys: 31
       curated 文: ぶん もん
       curated 対: たい つい
       curated 交: こう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 29 keys, 2: 217 keys
       tier 3 candidates (29): あい い えい かい がい けい げい すい せき せつ せん たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       unlisted-reading check: none of the 7 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 斎 (purification; abstinence; study room)   curated option cards: 海 毎 買
   metadata readings: on サイ | kun とき つつし.む ものいみ い.む いわ.う いつ.く
   unlisted readings attested for 斎: い (card text)  いつき (card text)  いみ (card text)  いもい (card text)  いわい (card text)  ゆ (card text)  さえ (KANJIDIC2 name reading)  ひとし (KANJIDIC2 name reading)  いつ (KANJIDIC2 name reading)  きよ (KANJIDIC2 name reading)  ただ (KANJIDIC2 name reading)  よし (KANJIDIC2 name reading)
   on prompt サイ (key さい)
       excluded keys: 21
       curated 海: かい
       curated 毎: まい
       curated 買: ばい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 33 keys, 2: 213 keys
       tier 3 candidates (33): あい い えい かい がい けい げい さ さく さっ さつ さん すい せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       HIT (can be drawn): unlisted reading い (card text) is offered by card(s) 以 位 依 偉 医 囲 委 威 意 易 異 移 維 胃 衣 違
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading ゆ (card text) is offered only by card(s) 愉 油 由 輸 遊
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading いつ (KANJIDIC2 name reading) is offered only by card(s) 一
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 斜 (diagonal; slanting; oblique)   curated option cards: 余 除 途
   metadata readings: on シャ | kun なな.め はす
   unlisted readings attested for 斜: なのめ (card text)  なのめならず (card text)
   on: no reading prompts
   kun prompt なな.め (key ななめ)
       excluded keys: 7
       curated 余: あまる あまり あます あんまり
       curated 除: のぞく よけ
       curated 途: みち
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 49 keys, 2: 807 keys, 1: 5 keys, 0: 35 keys
       tier 3 candidates (49): あめ うめ かなめ かめ ききめ ぎめ こめ つめ づとめ どめ ない なえ なおす なおる なか なかば なかま ながい ながれる なぎ なく なげる なごむ なさけ なし なす なずむ なつ など なな なに なま なまける なまめく なまる なみ なみだ なやむ ならう ならす ... (+9 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1687 other kun-reading cards
       simulation: 7 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt はす (key はす)
       excluded keys: 7
       curated 余: あまる あまり あます あんまり
       curated 除: のぞく よけ
       curated 途: みち
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 5 keys, 3: 118 keys, 2: 617 keys, 1: 14 keys, 0: 109 keys
       tier 4 candidates (5): はずす はたす はなす はやす はらす
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1687 other kun-reading cards
       simulation: 7 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 24; expected pairs: 24; added link pairs: 24; total added links: 24; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze ed966c3e): python -X utf8 kanji_remarks.py REPO ed966c3e4ad280a7463da6e6861e73077c413b0e kanji-remarks.json 挙 振 挿 掌 推 描 提 揮 揺 操 故 敵 斉 斎 斜
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/仮.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze ed966c3e): python -X utf8 meta_scan.py REPO 挙 振 挿 掌 推 描 提 揮 揺 操 故 敵 斉 斎 斜
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 57
   挙.md:49: 上げ 1352300 not listed part of 上げる
   挙.md:49: 揚げ 1352300/1545490 not listed part of 揚げる
   挙.md:63: 育て 1160550 not listed part of 育てる
   振.md:23: 振舞 1952740 not listed part of 振舞う
   振.md:23: 舞う 1499100 not listed part of 振舞う
   振.md:25: 舞う 1499100 not listed part of 振る舞う
   振.md:58: 揺す 2410160 not listed part of 揺する
   挿.md:52: 一輪 1167350 not listed part of 一輪挿し
   掌.md:33: 仙人 1387170 not listed part of 仙人掌
   掌.md:45: 指す 1309670 not listed part of 掌を指す
   掌.md:45: 返す 1512130 not listed part of 掌を返す
   掌.md:45: 返す 1512130 not listed part of 手のひらを返す
   推.md:43: 推し 2742350 not listed part of 推し量る
   推.md:43: 量る 1600650 not listed part of 推し量る
   推.md:43: 推し 2742350 not listed part of 推し進める
   推.md:43: 進める 1365990 not listed part of 推し進める
   推.md:43: 押し 1180130 not listed part of 押し進める
   推.md:43: 進める 1365990 not listed part of 押し進める
   提.md:42: 提げ 2423430 not listed part of 提げる
   提.md:44: 提げ 2423430 not listed part of 手提げ
   提.md:46: 下げ 2423430 not listed part of 下げる
   提.md:58: 屈す 2409930 not listed part of 屈する
   揮.md:25: 揮発 1220160 not listed part of 揮発油
   揮.md:34: 振る 1361330/2038080 not listed part of 振るう
   揺.md:25: 揺蕩 2513040 not listed part of 揺蕩う
   揺.md:40: 揺す 2410160 not listed part of 揺する
   揺.md:42: 揺す 2410160 not listed part of 揺すぶる
   揺.md:43: 揺り 1605770 not listed part of 揺り動かす
   揺.md:43: 動かす 1451170 not listed part of 揺り動かす
   揺.md:45: 揺す 2410160 not listed part of 揺す振る
   揺.md:47: 揺り 1605770 not listed part of 揺り返し
   揺.md:47: 返し 2202100 not listed part of 揺り返し
   揺.md:47: 揺り 1605770 not listed part of 揺り籠
   揺.md:47: 揺るぎ 2513050 not listed part of 揺るぎない
   揺.md:47: 貧乏 1490900 not listed part of 貧乏揺すり
   揺.md:47: 揺す 2410160 not listed part of 貧乏揺すり
   揺.md:47: 揺すり 2828307 not listed part of 貧乏揺すり
   揺.md:47: 貧乏 1490900 not listed part of 貧乏ゆすり
   揺.md:47: 揺るぎ 2513050 not listed part of 揺るぎ無い
   揺.md:47: 無い 1529520 not listed part of 揺るぎ無い
   揺.md:47: 無い 1529520 not listed part of 揺ぎ無い
   揺.md:56: 入れ 1465600 not listed part of 入れる
   揺.md:56: 見え 1578350 not listed part of 見える
   揺.md:56: 休め 1221830 not listed part of 休める
   操.md:44: 操り 1400000 not listed part of 操り人形
   故.md:65: 遅れ 1422020 not listed part of 遅れる
   故.md:65: 更け 2260190 not listed part of 更ける
   敵.md:25: 敵手 1735090 not listed part of 好敵手
   敵.md:25: 商売 1347200 not listed part of 商売敵
   敵.md:25: 商売 1347200 not listed part of 商売がたき
   敵.md:25: 討つ 1478010 not listed part of 親のかたきを討つ
   敵.md:38: 討つ 1478010 not listed part of 仇を討つ
   敵.md:38: 討つ 1478010 not listed part of 敵を討つ
   斉.md:25: 整え 1376130 not listed part of 整える
   斉.md:39: 均し 1642720 not listed part of 均しく
   斜.md:39: 向かい 1604750 not listed part of 斜向かい
   斜.md:39: 向かい 1604750 not listed part of はす向かい
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9034, 'entries': 9050, 'retainedBytes': 51424120, 'inflatedBytes': 51783211, 'localZipBytes': 32227628, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze ed966c3e: manifest.json: 9027 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version ec9fd0449faf4bc1
manifest.json sha256 before E12EC15E03D65791D48CCB46622A95893A82F23EACEBD75B9FB976DDB51DD388, after 7B226812D8A4570C88268CF7510913EE9A002BCA0E714559515E5B9CB94C8DF5; tracked tree after rebuild: M docs/n1-authoring-notes.md
 M "kanji/\344\273\256.md"
 M manifest.json
 M "words/\344\270\200\346\226\211.md"
 M "words/\344\272\213\346\225\205.md"
 M "words/\344\275\223\346\223\215.md"
 M "words/\345\214\271\346\225\265.md"
 M "words/\346\214\231\343\201\222\343\202\213.md"
 M "words/\346\214\257\343\202\212\344\273\256\345\220\215.md"
 M "words/\346\214\257\343\202\213.md"
 M "words/\346\214\257\350\210\236\343\201\206.md"
 M "words/\346\214\277\343\201\231.md"
 M "words/\346\216\250\345\256\232.md"
 M "words/\346\216\250\350\226\246.md"
 M "words/\346\217\217\343\201\217.md"
 M "words/\346\217\220\345\207\272.md"
 M "words/\346\217\220\346\241\210.md"
 M "words/\346\217\272\343\202\214\343\202\213.md"
 M "words/\346\223\215\344\275\234.md"
 M "words/\346\225\205\351\203\267.md"
 M "words/\346\225\205\351\232\234.md"
 M "words/\346\225\265.md"
 M "words/\346\226\234.md"
 M "words/\346\226\234\343\202\201.md"
 M "words/\346\233\270\346\226\216.md"
 M "words/\347\231\272\346\217\256.md"
 M "words/\350\273\212\346\216\214.md"
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 57.596s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
