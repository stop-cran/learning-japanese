# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 18, words checked: 25
WARN  words/隣.md: no Dictionary: line
WARN  words/眼鏡.md: no Dictionary: line
WARN  words/鏡.md: no Dictionary: line
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 18, words checked: 25
WARN  words/隣.md: no Dictionary: line
WARN  words/眼鏡.md: no Dictionary: line
WARN  words/鏡.md: no Dictionary: line
0 error(s), 3 warning(s)
```

## quiz safety simulation

```text
随 (follow; at will)  options: reverse; opposite | separate; detach | guide; conduct
    reading ズイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
隠 (hide; conceal)  options: search | indicate | capture
    reading かく.す   (kun): wrong options from distractors 3/3 (rest filled from other cards)
隣 (next door; adjoining)  options: far | interior; depths | reverse side; lining
    reading となり    (kun): wrong options from distractors 3/3 (rest filled from other cards)
雄 (male; hero)  options: weak; frail | dull; blunt | soft; supple
    reading ユウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
雷 (thunder; lightning)  options: frost | rainbow | cloud
    reading かみなり   (kun): wrong options from distractors 3/3 (rest filled from other cards)
霧 (fog; mist)  options: ice; freeze | storm; tempest | star; celestial point
    reading きり     (kun): wrong options from distractors 3/3 (rest filled from other cards)
項 (item; clause)  options: forehead; frame; sum | summit; receive | deposit; entrust
    reading コウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
顕 (evident; reveal)  options: pale; faint; plain; unsalted | withdraw; retreat | perish; destroy; die out
    reading ケン     (on): wrong options from distractors 3/3 (rest filled from other cards)
飼 (keep (animals); rear)  options: capture | discard; abandon | wash
    reading か.う    (kun): wrong options from distractors 3/3 (rest filled from other cards)
飽 (tire of; satiate)  options: get lost; be unsure | shame | celebrate; congratulate
    reading あ.きる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
飾 (decorate; adorn)  options: dirty; defile | shave; sharpen; pare | break; destroy; demolish
    reading かざ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
驚 (be surprised; astonish)  options: sadness | anger | rejoice
    reading おどろ.く  (kun): wrong options from distractors 3/3 (rest filled from other cards)
鬼 (demon; ogre)  options: Buddha; Buddhism | monkey | bear (animal)
    reading おに     (kun): wrong options from distractors 3/3 (rest filled from other cards)
鮮 (fresh; vivid)  options: rot; decay; spoil | pale; faint; plain; unsalted | muddy; cloudy; impure; voiced
    reading セン     (on): wrong options from distractors 1/3 (rest filled from other cards)
黙 (be silent; silence)  options: shout; exclaim | run | dance; hop
    reading だま.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
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
ated 仏 猿 熊 -> 1 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 3 drawable wrong options (3 curated, 0 fallback)
       All stack: curated 仏 猿 熊 -> 1 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 3 drawable wrong options (3 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 11 drawable wrong options (0 curated, 11 fallback)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 11 of 11 drawable wrong options seen
== 鮮 (fresh; vivid)   curated option cards: 腐 淡 濁   tags: jlpt-n1 grade-8 structure-unclassified
   curated 腐: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun くさ.る
   curated 淡: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on タン | kun -
   curated 濁: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun にご.る
   JMdict single-kanji entries: 2862566: [abbreviation, obsolete term] Korea -> せん
   unlisted readings attested for 鮮: あたらしい (--extra list)  すくない (--extra list)
   on prompt セン (key せん)
       N1 stack: curated 淡 -> 1 outcomes; deficit 2: the fallback fills the open slots; 54 drawable wrong options (1 curated, 53 fallback)
       All stack: curated 淡 -> 1 outcomes; deficit 2: the fallback fills the open slots; 54 drawable wrong options (1 curated, 53 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 23 drawable wrong options (0 curated, 23 fallback)
       sampling N1 stack: 200 seeds, 50 of 54 drawable wrong options seen
       sampling All stack: 200 seeds, 50 of 54 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 23 of 23 drawable wrong options seen
   kun: no reading prompts
== 黙 (be silent; silence)   curated option cards: 叫 走 踊   tags: jlpt-n1 grade-8 structure-unclassified
   curated 叫: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on キョウ | kun さけ.ぶ
   curated 走: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on ソウ | kun はし.る
   curated 踊: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ヨウ | kun おど.る
   JMdict single-kanji entries: 2849868: [word usually written using kana alone, poetical term] silence, stillness, quietness -> しじま
   unlisted readings attested for 黙: だんまり (--extra list)  もだ (--extra list)  もくする (--extra list)  もくとう (--extra list)  しじま (JMdict 2849868)
   on: no reading prompts
   kun prompt だま.る (key だまる)
       N1 stack: curated 叫 走 踊 -> 1 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 3 drawable wrong options (3 curated, 0 fallback)
       All stack: curated 叫 走 踊 -> 1 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 3 drawable wrong options (3 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 22 drawable wrong options (0 curated, 22 fallback)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 22 of 22 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 8 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 3 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
 tier): unlisted reading しか (KANJIDIC2 name reading) is offered only by card(s) 然 鹿
       simulation: 9 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 驚 (be surprised; astonish)   curated option cards: 悲 怒 喜
   metadata readings: on キョウ | kun おどろ.く おどろ.かす
   unlisted readings attested for 驚: none
   on: no reading prompts
   kun prompt おどろ.く (key おどろく)
       excluded keys: 17
       curated 悲: かなしい かなしむ
       curated 怒: いかる おこる
       curated 喜: よろこぶ よろこばす
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 2 keys, 3: 79 keys, 2: 589 keys, 1: 22 keys, 0: 295 keys
       tier 4 candidates (2): おののく おもえらく
       tier 3 candidates (79): あばく あまねく あるく いただく いだく うごく えがく おいる おえる おおい おおう おおきい おおやけ おかす おがむ おきる おぎなう おくまる おくる おくれる おこたる おこなう おこる おさえる おさない おさめる おしい おしえる おしむ おじる おそれる おだやか おちる おっと おとうと おとこ おとずれる おとる おどる おなじ ... (+39 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1745 other kun-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 鬼 (demon; ogre)   curated option cards: 仏 猿 熊
   metadata readings: on キ | kun おに おに-
   unlisted readings attested for 鬼: none
   on: no reading prompts
   kun prompt おに (key おに)
       excluded keys: 3
       curated 仏: ほとけ
       curated 猿: さる
       curated 熊: くま
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 56 keys, 2: 744 keys, 1: 14 keys, 0: 120 keys
       tier 3 candidates (56): あに お おいる おう おえる おお おおい おおう おか おかす おがむ おき おきる おく おくる おこる おさ おしい おしむ おじる おす おそい おそる おちる おっと おと おとこ おとる おどる おなじ おびる おも おもい おもう おもて おもり おや およぐ おりる おる ... (+16 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1745 other kun-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 鮮 (fresh; vivid)   curated option cards: 腐 淡 濁
   metadata readings: on セン | kun あざ.やか
   unlisted readings attested for 鮮: あたらしい (--extra list)  すくない (--extra list)
   on prompt セン (key せん)
       excluded keys: 5
       curated 腐: no usable on reading, slot filled from the fallback
       curated 淡: たん
       curated 濁: no usable on reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 54 keys, 2: 200 keys
       tier 3 candidates (54): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せい せき せつ そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ... (+14 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 303 other on-reading cards
       simulation: 44 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 黙 (be silent; silence)   curated option cards: 叫 走 踊
   metadata readings: on モク ボク | kun だま.る もだ.す
   unlisted readings attested for 黙: だんまり (--extra list)  もだ (--extra list)  もくする (--extra list)  もくとう (--extra list)
   on: no reading prompts
   kun prompt だま.る (key だまる)
       excluded keys: 13
       curated 叫: さけぶ
       curated 走: はしる
       curated 踊: おどる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 309 keys, 2: 601 keys, 1: 11 keys, 0: 32 keys
       tier 4 candidates (1): だてる
       tier 3 candidates (309): あえる あきる あける あげる あさる あずける あたえる あたる あつまる あてる あばれる あびる あまえる あまる あやまる あやめる ある あれる あわせる いかる いきる いする いためる いたる いのる いる いれる うえる うかれる うける うすめる うせる うつる うまれる うめる うる える おいる おきる おくまる ... (+269 more)
       unlisted-reading check: none of the 4 unlisted readings is offered by any of the 1745 other kun-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 19; expected pairs: 19; added link pairs: 19; total added links: 19; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze1 f8f3db8c): python -X utf8 kanji_remarks.py REPO 45de81cd C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b154\links\kanji-remarks.json 随 隠 隣 雄 雷 霧 項 顕 飼 飽 飾 驚 鬼 鮮 黙
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/塊.md
OK remark-only edit: kanji/微.md
OK remark-only edit: kanji/鏡.md
new cards: 15/15; modified existing cards: 3; declared remark edits applied: 3; problems: 0
```

## card Metadata entry ids (meta scan)

```text
isted part of 言いなりになる
   随.md:23: 成り 2611370 not listed part of 成り行きにまかせる
   随.md:23: 成り行き 1599700 not listed part of 成り行きにまかせる
   随.md:23: 行き 1578790 not listed part of 成り行きにまかせる
   隠.md:23: 住む 1334040 not listed part of かくれ住む
   隠.md:23: 隠れ 1613470 not listed part of 隠れる
   隠.md:53: 世間 1373970 not listed part of 世間からかくれる
   隠.md:53: 秘密 1484150 not listed part of 秘密にする
   隣.md:41: 合う 1284430 not listed part of 隣り合う
   雄.md:23: 動植物 1451410 not listed part of 動植物のおす
   雄.md:23: 植物 1357300 not listed part of 動植物のおす
   雄.md:23: 物の 2272520 not listed part of 動植物のおす
   雄.md:23: 人物 1369070 not listed part of すぐれた人物
   雄.md:23: 強い 1236070/2087680 not listed part of 勇ましく強い
   雄.md:23: 規模 1223090 not listed part of 規模が大きい
   雄.md:23: 大き 2427850 not listed part of 規模が大きい
   雄.md:23: 大きい 1588880 not listed part of 規模が大きい
   雄.md:55: 特に 1454670 not listed part of 特にすぐれていること
   雷.md:23: 形容 1250420 not listed part of かみなりのようなものの形容
   雷.md:23: 爆発 1475910 not listed part of 爆発するしかけの兵器
   雷.md:23: 発する 1477130 not listed part of 爆発するしかけの兵器
   雷.md:23: 兵器 1506320 not listed part of 爆発するしかけの兵器
   霧.md:23: 集まり 1609050 not listed part of きりのように集まり
   霧.md:23: 消える 1350040 not listed part of または消えるさま
   霧.md:23: 散らばる 1303480 not listed part of きりのように散らばる水滴
   霧.md:23: 水滴 1371880 not listed part of きりのように散らばる水滴
   霧.md:23: 噴霧 2656950 not listed part of 噴霧器
   項.md:23: 小分け 1640320 not listed part of 小分けした一つ一つのことがら
   項.md:23: 分け 1502990 not listed part of 小分けした一つ一つのことがら
   項.md:23: 一つ 1160820 not listed part of 小分けした一つ一つのことがら
   項.md:23: 一つ一つ 1160830 not listed part of 小分けした一つ一つのことがら
   項.md:47: 小分け 1640320 not listed part of 小分けした一つ一つ
   項.md:47: 分け 1502990 not listed part of 小分けした一つ一つ
   項.md:47: 一つ 1160820 not listed part of 小分けした一つ一つ
   項.md:47: 一つ一つ 1160830 not listed part of 小分けした一つ一つ
   顕.md:23: 隠れ 1613470 not listed part of 隠れたものを明らかにする
   顕.md:23: 明らかにする 1532320 not listed part of 隠れたものを明らかにする
   顕.md:23: 顕微 1260650 not listed part of 顕微鏡
   顕.md:33: 現れ 1610550 not listed part of 現れる
   顕.md:33: 顕れ 1610550 not listed part of 顕れる
   顕.md:51: 高い 1283190 not listed part of 名高い
   顕.md:51: 地位 1420780 not listed part of 地位が高い
   顕.md:51: 高い 1283190 not listed part of 地位が高い
   顕.md:51: 地位 1420780 not listed part of 地位・身分が高い
   顕.md:51: 身分 1365810 not listed part of 地位・身分が高い
   顕.md:51: 高い 1283190 not listed part of 地位・身分が高い
   飼.md:23: 動物 1451470 not listed part of 動物を育てる
   飼.md:23: 育て 1160550 not listed part of 動物を育てる
   飼.md:23: 与え 1544720 not listed part of えさを与えて養う
   飼.md:41: 学習 1206820 not listed part of 学習漢字
   飼.md:41: 漢字 1213170 not listed part of 学習漢字
   飼.md:47: 育て 1160550 not listed part of 育てる
   飽.md:23: 腹いっぱい 1611290 not listed part of 腹いっぱい食べる
   飽.md:23: 食べる 1358280 not listed part of 腹いっぱい食べる
   飽.md:23: 飽き 1609020 not listed part of 飽きる
   飽.md:49: 疲れ 1483730/2845234 not listed part of 疲れる
   飽.md:51: 十分 1335070/1335080 not listed part of 十分に満たされる
   驚.md:49: 恐れ 1236660 not listed part of 恐れる
   驚.md:49: 怖れ 1236660 not listed part of 怖れる
   鬼.md:23: 死者 1310870 not listed part of 死者のたましい
   鬼.md:23: 死者 1310870 not listed part of 死者の霊魂
   鬼.md:23: 霊魂 1557790 not listed part of 死者の霊魂
   鬼.md:23: この世 2002260 not listed part of この世のものとも思われない恐るべき存在
   鬼.md:23: 恐る 1496960 not listed part of この世のものとも思われない恐るべき存在
   鬼.md:23: 恐るべき 1609420 not listed part of この世のものとも思われない恐るべき存在
   鬼.md:23: 存在 1406150 not listed part of この世のものとも思われない恐るべき存在
   鬼.md:23: 化け 2527190 not listed part of 化け物
   鬼.md:23: 鬼ご 2869370 not listed part of 鬼ごっこ
   鬼.md:33: 百合 1488160/2862412 not listed part of 鬼百合
   鮮.md:23: 生き 1378500 not listed part of 生きがいい
   鮮.md:23: 生きがい 1378550 not listed part of 生きがいい
   鮮.md:23: 取り 2451270/2762480 not listed part of 取りたてで生きがよい
   鮮.md:23: 取りたて 1707460 not listed part of 取りたてで生きがよい
   鮮.md:23: 生き 1378500 not listed part of 取りたてで生きがよい
   鮮.md:23: 生きがよい 1021150 not listed part of 取りたてで生きがよい
   鮮.md:23: 生生 1829690 not listed part of 生生しい
   鮮.md:48: 冴え 1297040 not listed part of 冴える
   黙.md:23: 言葉 1264540 not listed part of 声・言葉を出さない
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9708, 'entries': 9724, 'retainedBytes': 56445366, 'inflatedBytes': 56874930, 'localZipBytes': 36271374, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze1 f8f3db8c: manifest.json: 9701 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 6f0cc4e50b038fd3
manifest.json sha256 before FAD8A4317CC6CE455521C669B26554C0659809B0F66BAF3477AE93D4BDCECADC, after FAD8A4317CC6CE455521C669B26554C0659809B0F66BAF3477AE93D4BDCECADC; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 74.188s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
