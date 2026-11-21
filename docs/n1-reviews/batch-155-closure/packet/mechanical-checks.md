# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 6, words checked: 6
WARN  words/卑怯.md: Dictionary: line cites no JMdict entry id
WARN  words/太鼓.md: Dictionary: line cites no JMdict entry id
0 error(s), 2 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 6, words checked: 6
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
卑 (lowly; despicable)  options: courage; bravery | wise; intelligent | sharp; keen
    reading ヒ      (on): wrong options from distractors 3/3 (rest filled from other cards)
汰 (sift; weed out)  options: sew; stitch | polish; grind | paint; coat
    reading タ      (on): wrong options from distractors 3/3 (rest filled from other cards)
沙 (sand; sift)  options: iron | copper | salt
    reading サ      (on): wrong options from distractors 3/3 (rest filled from other cards)
沢 (marsh; luster)  options: frost | rock; boulder | hill; knoll
    reading タク     (on): wrong options from distractors 2/3 (rest filled from other cards)
胡 (foreign; dubious)  options: sweet; pamper | soft; supple | quiet
    reading コ      (on): wrong options from distractors 3/3 (rest filled from other cards)
鼓 (drum; rouse)  options: flute; whistle | koto; zither | brush; writing
    reading コ      (on): wrong options from distractors 1/3 (rest filled from other cards)
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
 砂 茶; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [沢 作] -> さ さく; [沢 再] -> さ さい
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (8 holders tried)
       sampling N1 stack: 200 seeds, 43 of 49 drawable wrong options seen
       sampling All stack: 200 seeds, 43 of 49 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 18 of 18 drawable wrong options seen
   kun: no reading prompts
== 胡 (foreign; dubious)   curated option cards: 甘 柔 静   tags: jlpt-n1 grade-9 structure-unclassified
   curated 甘: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on カン | kun あま.い あま.える あま.やかす うま.い
   curated 柔: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ジュウ ニュウ | kun やわ.らか やわ.らかい やわ やわ.ら
   curated 静: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on セイ ジョウ | kun しず- しず.か しず.まる しず.める
   JMdict single-kanji entries: 2230390: [historical term] barbarian tribes surrounding ancient China -> こ
   unlisted readings attested for 胡: えびす (KANJIDIC2 name reading, --extra list)  くる (KANJIDIC2 name reading)  でたらめ (--extra list)  みだり (--extra list)  ながいき (--extra list)  いずくんぞ (--extra list)
   on prompt コ (key こ)
       N1 stack: curated 甘 柔 静 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 甘 柔 静 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 76 drawable wrong options (0 curated, 76 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 69 of 76 drawable wrong options seen
   kun: no reading prompts
== 鼓 (drum; rouse)   curated option cards: 笛 琴 筆   tags: jlpt-n1 grade-8 structure-unclassified
   curated 笛: tags jlpt-n1 grade-3 structure-unclassified; in pools: N1 stack, All stack; on - | kun ふえ
   curated 琴: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun こと
   curated 筆: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ヒツ | kun ふで
   JMdict single-kanji entries: 1267900: tsuzumi, hourglass-shaped Japanese hand drum -> つづみ
   unlisted readings attested for 鼓: こす (--extra list)  こする (--extra list)
   on prompt コ (key こ)
       N1 stack: curated 筆 -> 1 outcomes; deficit 2: the fallback fills the open slots; 4 drawable wrong options (1 curated, 3 fallback)
       All stack: curated 筆 -> 1 outcomes; deficit 2: the fallback fills the open slots; 4 drawable wrong options (1 curated, 3 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 78 drawable wrong options (0 curated, 78 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 70 of 78 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 1 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
ゆる (--extra list)
   on prompt タ (key た)
       excluded keys: 13
       curated 縫: ほう
       curated 磨: ま
       curated 塗: と
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 3 keys, 2: 222 keys, 0: 31 keys
       tier 3 candidates (3): たく たつ たん
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 303 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 沙 (sand; sift)   curated option cards: 鉄 銅 塩
   metadata readings: on サ シャ | kun すな よなげる
   unlisted readings attested for 沙: みぎわ (--extra list)  いさご (--extra list)
   on prompt サ (key さ)
       excluded keys: 8
       curated 鉄: てつ
       curated 銅: どう
       curated 塩: えん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 5 keys, 2: 218 keys, 0: 31 keys
       tier 3 candidates (5): さい さく さっ さつ さん
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 303 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 沢 (marsh; luster)   curated option cards: 霜 岩 丘
   metadata readings: on タク | kun さわ うるお.い うるお.す つや
   unlisted readings attested for 沢: うるおう (--extra list)  おも (KANJIDIC2 name reading)  さ (KANJIDIC2 name reading)  さわん (KANJIDIC2 name reading)  わさ (KANJIDIC2 name reading)
   on prompt タク (key たく)
       excluded keys: 12
       curated 霜: no usable on reading, slot filled from the fallback
       curated 岩: がん
       curated 丘: きゅう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 47 keys, 2: 207 keys
       tier 3 candidates (47): あく いく おく かく がく きく きゃく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく じゅく そく ぞく た たい たつ たん ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふく ほく ぼく まく みゃく もく やく ... (+7 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading さ (KANJIDIC2 name reading) is offered only by card(s) 作 再 左 差 査 沙 砂 茶
       simulation: 35 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 胡 (foreign; dubious)   curated option cards: 甘 柔 静
   metadata readings: on ウ コ ゴ | kun なんぞ
   unlisted readings attested for 胡: えびす (--extra list)  でたらめ (--extra list)  みだり (--extra list)  ながいき (--extra list)  いずくんぞ (--extra list)  くる (KANJIDIC2 name reading)
   on prompt コ (key こ)
       excluded keys: 8
       curated 甘: かん
       curated 柔: じゅう にゅう
       curated 静: せい じょう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 3 keys, 2: 220 keys, 0: 31 keys
       tier 3 candidates (3): こく こつ こん
       unlisted-reading check: none of the 6 unlisted readings is offered by any of the 303 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 鼓 (drum; rouse)   curated option cards: 笛 琴 筆
   metadata readings: on コ | kun つづみ
   unlisted readings attested for 鼓: こす (--extra list)  こする (--extra list)
   on prompt コ (key こ)
       excluded keys: 4
       curated 笛: no usable on reading, slot filled from the fallback
       curated 琴: no usable on reading, slot filled from the fallback
       curated 筆: ひつ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 3 keys, 2: 223 keys, 0: 31 keys
       tier 3 candidates (3): こく こつ こん
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 303 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 6; expected pairs: 8; added link pairs: 8; total added links: 8; declared remark edits: 1; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at worktree-over 6cbc14fe): python -X utf8 kanji_remarks.py REPO 6cbc14fe C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b155\links\kanji-remarks.json 卑 汰 沙 沢 胡 鼓
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
new cards: 6/6; modified existing cards: 0; declared remark edits applied: 0; problems: 0
```

## card Metadata entry ids (meta scan)

```text
isted
-- whole-run gaps: 4; part-of-run matches not listed: 75
   卑.md:23: 地位 1420780 not listed part of 地位や身分が低い
   卑.md:23: 身分 1365810 not listed part of 地位や身分が低い
   卑.md:23: 自分 1318610 not listed part of 自分のことをいうときの謙称
   卑.md:23: 分の 2145670 not listed part of 自分のことをいうときの謙称
   卑.md:23: 謙称 1260200 not listed part of 自分のことをいうときの謙称
   卑.md:23: 身近 1365650 not listed part of 身近な
   卑.md:23: 土地 1445470 not listed part of 土地が低い
   卑.md:47: 身分 1365810 not listed part of 身分や地位が低い
   卑.md:47: 地位 1420780 not listed part of 身分や地位が低い
   卑.md:48: 品性 1490630 not listed part of 品性が劣る
   卑.md:48: 劣る 1558400 not listed part of 品性が劣る
   卑.md:48: 価値 1189600 not listed part of 価値が劣る
   卑.md:48: 劣る 1558400 not listed part of 価値が劣る
   卑.md:51: 自分 1318610 not listed part of 自分のことをへりくだっていう語
   卑.md:51: 分の 2145670 not listed part of 自分のことをへりくだっていう語
   汰.md:23: 不要 1602900 not listed part of 不要のものを流し去る
   汰.md:23: 流し 1552100 not listed part of 不要のものを流し去る
   汰.md:23: 去る 1231650 not listed part of 不要のものを流し去る
   汰.md:23: 良い 1605820 not listed part of 良いものと悪いものをより分ける
   汰.md:23: 悪い 1151260/1403390/2772730 not listed part of 良いものと悪いものをより分ける
   汰.md:23: より分ける 1581090 not listed part of 良いものと悪いものをより分ける
   汰.md:23: 分け 1502990 not listed part of 良いものと悪いものをより分ける
   汰.md:23: 分ける 1503000 not listed part of 良いものと悪いものをより分ける
   汰.md:55: 行い 1589050 not listed part of 行いや志が清潔でない
   汰.md:55: 清潔 1378200 not listed part of 行いや志が清潔でない
   沙.md:23: 水辺 1649910 not listed part of 水辺の砂地
   沙.md:23: 砂地 1291580 not listed part of 水辺の砂地
   沙.md:23: 水中 1371840 not listed part of 水中で洗ってよりわける
   沙.md:23: 適否 1437480 not listed part of 水で洗って適否をより分ける
   沙.md:23: より分ける 1581090 not listed part of 水で洗って適否をより分ける
   沙.md:23: 分け 1502990 not listed part of 水で洗って適否をより分ける
   沙.md:23: 分ける 1503000 not listed part of 水で洗って適否をより分ける
   沙.md:32: 梵語 1568160 not listed part of 梵語の音訳字
   沙.md:32: 音訳 1184090 not listed part of 梵語の音訳字
   沙.md:53: 非常 1484920 not listed part of 非常に細かい石の粒
   沙.md:53: 非常に 1484930 not listed part of 非常に細かい石の粒
   沙.md:53: 常に 1355970 not listed part of 非常に細かい石の粒
   沙.md:53: 細か 1295520 not listed part of 非常に細かい石の粒
   沙.md:53: 細かい 1295530 not listed part of 非常に細かい石の粒
   沙.md:53: 細か 1295520 not listed part of 石のごく細かいもの
   沙.md:53: 細かい 1295530 not listed part of 石のごく細かいもの
   沙.md:56: 水中 1371840 not listed part of 水中で洗って
   沢.md:23: 草木 1581300 not listed part of 草木の生えている湿地帯
   沢.md:23: 湿地 1320470/1389560 not listed part of 草木の生えている湿地帯
   沢.md:23: 湿地帯 2840245 not listed part of 草木の生えている湿地帯
   沢.md:23: 地帯 1421360 not listed part of 草木の生えている湿地帯
   沢.md:23: 豊か 1518130 not listed part of 物が豊かにあること
   沢.md:53: 施す 1310370 not listed part of 人に施す恵み
   沢.md:53: 恵み 1250470 not listed part of 人に施す恵み
   胡.md:23: 中国 1424270 not listed part of 中国の北方・西方に住む異民族
   胡.md:23: 北方 1521310 not listed part of 中国の北方・西方に住む異民族
   胡.md:23: 西方 1580920 not listed part of 中国の北方・西方に住む異民族
   胡.md:23: 住む 1334040 not listed part of 中国の北方・西方に住む異民族
   胡.md:23: 民族 1604740 not listed part of 中国の北方・西方に住む異民族
   胡.md:23: 中国 1424270 not listed part of 中国で
   胡.md:23: 北方 1521310 not listed part of 北方または西方の異民族
   胡.md:23: 西方 1580920 not listed part of 北方または西方の異民族
   胡.md:23: 民族 1604740 not listed part of 北方または西方の異民族
   胡.md:23: 外国産 2069450 not listed part of 外国産の
   胡.md:23: 国産 1286590 not listed part of 外国産の
   胡.md:31: 臭い 1333150/1599760 not listed part of 胡散臭い
   胡.md:42: 人名 1369340 not listed part of 人名用漢字
   胡.md:42: 漢字 1213170 not listed part of 人名用漢字
   胡.md:50: 民族 1604740 not listed part of 異民族
   胡.md:56: 長生 1797520 not listed part of 長生き
   胡.md:56: 生き 1378500 not listed part of 長生き
   胡.md:57: 昆虫 1289980 not listed part of は昆虫の名
   鼓.md:23: 打楽器 1408860 not listed part of 打楽器の一種
   鼓.md:23: 楽器 1207340 not listed part of 打楽器の一種
   鼓.md:23: 一種 1163170 not listed part of 打楽器の一種
   鼓.md:23: 打楽器 1408860 not listed part of 打楽器の一
   鼓.md:23: 楽器 1207340 not listed part of 打楽器の一
   鼓.md:23: 打つ 1408810/1408815 not listed part of つづみを打つ
   鼓.md:41: 異体 1157920 not listed part of は異体字
   鼓.md:41: 異体字 1157930 not listed part of は異体字
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9720, 'entries': 9736, 'retainedBytes': 56501181, 'inflatedBytes': 56930745, 'localZipBytes': 36296656, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at worktree-over 6cbc14fe: manifest.json: 9713 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version b487d4e935c3d111
manifest.json sha256 before 43573805439040C53B6C4E968DDFE612E6F3B271A086E55D5B6175E75D599E7F, after DBC622214882205621643F04AC458F929757831F67A823081E0A0EA8182F890D; tracked tree after rebuild: M manifest.json
 M "words/\345\215\221\346\200\257.md"
 M "words/\345\244\252\351\274\223.md"
 M "words/\345\276\241\347\204\241\346\262\231\346\261\260.md"
 M "words/\347\204\241\346\262\231\346\261\260.md"
 M "words/\350\203\241\346\244\222.md"
 M "words/\350\264\205\346\262\242.md"
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 65.195s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
