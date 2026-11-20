# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 18, words checked: 31
WARN  words/比較的.md: Dictionary: line cites no JMdict entry id
WARN  words/踏切.md: Dictionary: line cites no JMdict entry id
WARN  words/逸れる.md: Dictionary: line cites no JMdict entry id
WARN  words/平仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/振り仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/響き.md: Dictionary: line cites no JMdict entry id
WARN  words/響く.md: Dictionary: line cites no JMdict entry id
0 error(s), 7 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 18, words checked: 31
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
趣 (elegance; gist)  options: dislike; suspicion | pride; boast | shame
    reading シュ     (on): wrong options from distractors 2/3 (rest filled from other cards)
跳 (hop; spring up)  options: slide; slippery; smooth | sink; subside | shake; sway; waver
    reading は.ねる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
踏 (tread; trample)  options: grip; grasp | dig; excavate | pick up; gather
    reading ふ.む    (kun): wrong options from distractors 3/3 (rest filled from other cards)
躍 (leap; jump up)  options: turn; roll | topple; collapse | sink; subside
    reading ヤク     (on): wrong options from distractors 3/3 (rest filled from other cards)
較 (compare; contrast)  options: choose | evidence; proof | extract
    reading カク     (on): wrong options from distractors 3/3 (rest filled from other cards)
載 (load; publish)  options: descend | fall down | float
    reading の.る    (kun): wrong options from distractors 3/3 (rest filled from other cards)
輝 (shine; sparkle)  options: cloud over; cloudy weather | dirty; defile | wither; dry up
    reading かがや.く  (kun): wrong options from distractors 3/3 (rest filled from other cards)
輩 (fellows; companions)  options: enemy; opponent; rival | retainer; subject | teacher; specialist
    reading ハイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
迫 (press; approach)  options: go out, exit | enter, put in | rest
    reading せま.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
逸 (deviate; stray)  options: meet | accompany, offer | road, way
    reading そ.れる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
遂 (accomplish; at last)  options: already; previously | renew; grow late | without fail
    reading つい.に   (kun): wrong options from distractors 3/3 (rest filled from other cards)
遣 (dispatch; usage)  options: welcome; greet | call out | request; rely
    reading -づか.い  (kun): wrong options from distractors 3/3 (rest filled from other cards)
避 (avoid; evade)  options: seek; request | follow; obey; subordinate | pick up; gather
    reading さ.ける   (kun): wrong options from distractors 3/3 (rest filled from other cards)
郡 (county; district)  options: bay, gulf | hill; knoll | shore; riverbank
    reading グン     (on): wrong options from distractors 3/3 (rest filled from other cards)
郷 (hometown; village)  options: castle | tower; pagoda | palace; lord
    reading キョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
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
ots; 24 drawable wrong options (0 curated, 24 fallback)
       attested reading かわす (--extra list) is offered by 交; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [避 交] -> かう かわす こもごも まざる まじえる まじる まじわる まぜる
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (1 holders tried)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
== 郡 (county; district)   curated option cards: 湾 丘 岸   tags: jlpt-n1 grade-4 structure-unclassified
   curated 湾: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ワン | kun いりえ
   curated 丘: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on キュウ | kun おか
   curated 岸: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ガン | kun きし
   JMdict single-kanji entries: 1249230: district, county -> ぐん・こおり
   unlisted readings attested for 郡: none
   on prompt グン (key ぐん)
       N1 stack: curated 湾 丘 岸 -> 1 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 3 drawable wrong options (3 curated, 0 fallback)
       All stack: curated 湾 丘 岸 -> 1 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 3 drawable wrong options (3 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 24 drawable wrong options (0 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
   kun: no reading prompts
== 郷 (hometown; village)   curated option cards: 城 塔 殿   tags: jlpt-n1 grade-6 structure-unclassified
   curated 城: tags jlpt-n2 grade-4 structure-unclassified; in pools: N1 stack, All stack; on ジョウ セイ | kun しろ
   curated 塔: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on トウ | kun -
   curated 殿: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on デン テン | kun との -どの
   JMdict single-kanji entries: 1550760: village, hamlet -> さと; 2145770: hometown -> きょう; 2259810: countryside, country -> ごう
   unlisted readings attested for 郷: くに (KANJIDIC2 name reading)
   on prompt キョウ (key きょう)
       N1 stack: curated 城 塔 殿 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 城 塔 殿 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 14 drawable wrong options (0 curated, 14 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 14 of 14 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 20 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 2 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
s
       tier 4 candidates (1): つぶさに
       tier 3 candidates (65): あに いずくに おおいに かたみに くに ごとに さらに しに すでに ただちに たに ついやす つか つかう つかえる つかさ つかまる つかれる つかわす つがい つき つく つくえ つくる つぐ つぐなう つける つげる つたわる つち つつ つつむ つづく つづまる つとめる つどう つな つね つの つのる ... (+25 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading つい (--extra list) is offered only by card(s) 終
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 遣 (dispatch; usage)   curated option cards: 迎 呼 頼
   metadata readings: on ケン | kun つか.う -つか.い -づか.い つか.わす や.る
   unlisted readings attested for 遣: よこす (--extra list)  しむ (--extra list)
   on: no reading prompts
   kun prompt -づか.い (key づかい)
       excluded keys: 19
       curated 迎: むかえる
       curated 呼: よぶ
       curated 頼: たのむ たのもしい たよる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 2 keys, 3: 125 keys, 2: 772 keys, 1: 5 keys, 0: 38 keys
       tier 4 candidates (2): づたい づらい
       tier 3 candidates (125): あい あおい あかい あかるい あさい あたい あつい あぶない あまい あやしい あらい いきおい いたい いとしい いぬい うい うがい うすい えらい おおい おおきい おさない おしい おそい おもい かい かこい かしこい かたい かなしい かるい きたない きびしい きよい きらい くさい くやしい くらい くるしい くれない ... (+85 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1734 other kun-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 避 (avoid; evade)   curated option cards: 求 従 拾
   metadata readings: on ヒ | kun さ.ける よ.ける
   unlisted readings attested for 避: かわす (--extra list)
   on: no reading prompts
   kun prompt さ.ける (key さける)
       excluded keys: 9
       curated 求: もとめる
       curated 従: したがう
       curated 拾: ひろう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 11 keys, 3: 312 keys, 2: 570 keys, 1: 10 keys, 0: 31 keys
       tier 4 candidates (11): さえる さかえる さかる さぐる ささえる ささる さだめる さとる さめる さる さわる
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading かわす (--extra list) is offered only by card(s) 交
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 郡 (county; district)   curated option cards: 湾 丘 岸
   metadata readings: on グン | kun こおり
   unlisted readings attested for 郡: none
   on prompt グン (key ぐん)
       excluded keys: 6
       curated 湾: わん
       curated 丘: きゅう
       curated 岸: がん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 53 keys, 2: 200 keys
       tier 3 candidates (53): あん いん うん えん おん かん がん きん ぎん ぐ ぐう けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ぶん ... (+13 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 302 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 郷 (hometown; village)   curated option cards: 城 塔 殿
   metadata readings: on キョウ ゴウ | kun さと
   unlisted readings attested for 郷: くに (KANJIDIC2 name reading)
   on prompt キョウ (key きょう)
       excluded keys: 9
       curated 城: じょう せい
       curated 塔: とう
       curated 殿: でん てん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 36 keys, 2: 172 keys, 1: 2 keys, 0: 39 keys
       tier 4 candidates (1): きゅう
       tier 3 candidates (36): おう きく きつ きゃく きょく きん ぎゅう くう ぐう しゅう しょう じゅう じょう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 302 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 20; expected pairs: 20; added link pairs: 20; total added links: 20; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at B152 freeze1 cdd8fd01): python -X utf8 kanji_remarks.py REPO d59c45576d5438036e317dfbbc3c353ea4fc74a6 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b152\links\kanji-remarks.json 趣 跳 踏 躍 較 載 輝 輩 迫 逸 遂 遣 避 郡 郷
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/仮.md
OK remark-only edit: kanji/故.md
OK remark-only edit: kanji/響.md
new cards: 15/15; modified existing cards: 3; declared remark edits applied: 4; problems: 0
```

## card Metadata entry ids (meta scan)

```text
 迫 逸 遂 遣 避 郡 郷
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 73
   趣.md:23: 向かう 1604800 not listed part of 心の向かうところ
   跳.md:23: 地面 1421510 not listed part of はね上がって地面から離れる
   跳.md:23: 離れ 2013190/2855165 not listed part of はね上がって地面から離れる
   跳.md:23: 離れる 1550840 not listed part of はね上がって地面から離れる
   跳.md:23: 跳ね 1429610 not listed part of 跳ねる
   跳.md:34: 跳び 2248520 not listed part of 縄跳び
   踏.md:23: 行う 1589060 not listed part of ふみ行う
   踏.md:23: 切り 1383800 not listed part of 踏み切り
   踏.md:42: 高踏 1809580 not listed part of 高踏的
   躍.md:23: はね上がる 1601010 not listed part of 高くはね上がる
   躍.md:23: 上がる 1352290 not listed part of 高くはね上がる
   躍.md:23: 勢い 1375040 not listed part of 勢いよく動き回る
   躍.md:23: 勢いよく 1375070 not listed part of 勢いよく動き回る
   躍.md:23: 動き 1451180 not listed part of 勢いよく動き回る
   躍.md:23: 動き回る 1451200 not listed part of 勢いよく動き回る
   躍.md:23: 回る 1342050/1604300/1605260/2255060 not listed part of 勢いよく動き回る
   躍.md:40: 躍り 1546880/1643460 not listed part of 躍り上がる
   躍.md:40: 上がる 1352290 not listed part of 躍り上がる
   躍.md:41: 走る 1402540 not listed part of はやく走る
   較.md:23: 合わせ 1284470 not listed part of つき合わせて見比べる
   較.md:23: 合わせて 1506010 not listed part of つき合わせて見比べる
   較.md:23: 見比べる 1604440 not listed part of つき合わせて見比べる
   較.md:23: 比べ 1003950 not listed part of つき合わせて見比べる
   較.md:33: 較べ 1003950 not listed part of 較べる
   較.md:33: 比べ 1003950 not listed part of 比べる
   較.md:49: 競べ 1003950 not listed part of 競べる
   載.md:23: 積む 1382970 not listed part of 車や船に積む
   載.md:23: 印刷 1168190 not listed part of 印刷物にのせる
   載.md:23: 印刷物 1168300 not listed part of 印刷物にのせる
   載.md:23: 刷物 1298640 not listed part of 印刷物にのせる
   載.md:42: 千載 2868500 not listed part of 千載一遇
   載.md:42: 一遇 1162020 not listed part of 千載一遇
   迫.md:49: 詰め 1226500/2861276 not listed part of 追い詰める
   迫.md:49: 詰める 1226510 not listed part of 追い詰める
   逸.md:36: 逸す 2410170 not listed part of 逸する
   逸.md:56: 気楽 1222010 not listed part of 気楽に楽しむ
   逸.md:56: 楽しむ 1207270 not listed part of 気楽に楽しむ
   遂.md:53: し遂げる 1594460 not listed part of 成し遂げる
   遣.md:23: 使用 1306200 not listed part of 使用する
   遣.md:23: 使役 1306180 not listed part of 使役の助字
   遣.md:23: 助字 2804840 not listed part of 使役の助字
   遣.md:23: 仮名 1577090/1590540 not listed part of 仮名遣い
   遣.md:23: 言葉 1264540 not listed part of 言葉遣い
   遣.md:33: 人形 1367120/2856519 not listed part of 人形遣い
   遣.md:33: 人形 1367120/2856519 not listed part of 人形使い
   避.md:23: 避け 2099800 not listed part of 避ける
   避.md:35: 除け 2099800 not listed part of 除ける
   避.md:43: 不可 1491370 not listed part of 不可避
   郡.md:23: 行政 1282010 not listed part of 行政区画の一つ
   郡.md:23: 行政区 1282040 not listed part of 行政区画の一つ
   郡.md:23: 行政区画 1282050 not listed part of 行政区画の一つ
   郡.md:23: 区画 1592110 not listed part of 行政区画の一つ
   郡.md:23: 一つ 1160820 not listed part of 行政区画の一つ
   郡.md:23: 日本 1582710 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 都道 2844021 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 都道府県 1445030 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 道府県 2151380 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 府県 1496900 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 行政 1282010 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 行政区 1282040 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 行政区画 1282050 not listed part of 日本では都道府県の下にある行政区画
   郡.md:23: 区画 1592110 not listed part of 日本では都道府県の下にある行政区画
   郷.md:23: 生まれ 1609350 not listed part of 生まれたところ
   郷.md:23: 行政 1282010 not listed part of 昔の行政区画の一つ
   郷.md:23: 行政区 1282040 not listed part of 昔の行政区画の一つ
   郷.md:23: 行政区画 1282050 not listed part of 昔の行政区画の一つ
   郷.md:23: 区画 1592110 not listed part of 昔の行政区画の一つ
   郷.md:23: 一つ 1160820 not listed part of 昔の行政区画の一つ
   郷.md:50: 行政 1282010 not listed part of 行政区画の一つ
   郷.md:50: 行政区 1282040 not listed part of 行政区画の一つ
   郷.md:50: 行政区画 1282050 not listed part of 行政区画の一つ
   郷.md:50: 区画 1592110 not listed part of 行政区画の一つ
   郷.md:50: 一つ 1160820 not listed part of 行政区画の一つ
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9646, 'entries': 9662, 'retainedBytes': 56187484, 'inflatedBytes': 56546780, 'localZipBytes': 36139254, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at B152 freeze1 cdd8fd01: manifest.json: 9639 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 3f2b0c6b779cf85d
manifest.json sha256 before 901E808596BE0001C870E43014C89AC5975277744D19E53D1FC6B54468A0BF7A, after 901E808596BE0001C870E43014C89AC5975277744D19E53D1FC6B54468A0BF7A; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 76.708s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
