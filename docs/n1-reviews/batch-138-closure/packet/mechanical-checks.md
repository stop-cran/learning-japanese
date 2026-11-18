# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 24
WARN  words/噴火.md: Dictionary: line cites no JMdict entry id
WARN  words/墨.md: Dictionary: line cites no JMdict entry id
WARN  words/威張る.md: Dictionary: line cites no JMdict entry id
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 24
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
噴 (erupt; spout; gush)  options: mouth | old | buy
    reading フン     (on): wrong options from distractors 3/3 (rest filled from other cards)
垂 (hang down; droop; dangle)  options: mail; postal service | ride; board | heavy; piled up
    reading スイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
垣 (fence; hedge)  options: slope; incline | castle | bury; embed
    reading かき     (kun): wrong options from distractors 3/3 (rest filled from other cards)
執 (take hold; carry out; cling)  options: report; news | happiness; good fortune | heat; fever
    reading シツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
堅 (hard; solid; steady)  options: retainer; subject | oversee; watch over | foundation; basis
    reading かた.い   (kun): wrong options from distractors 1/3 (rest filled from other cards)
塊 (lump; clod; mass)  options: charm; bewitch | castle | place, site
    reading かたまり   (kun): wrong options from distractors 2/3 (rest filled from other cards)
墨 (ink; inkstick)  options: grave; tomb | mold; type | hall
    reading すみ     (kun): wrong options from distractors 2/3 (rest filled from other cards)
壁 (wall; barrier)  options: spicy; painful | foundation; basis | slope; incline
    reading かべ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
壊 (break; destroy; demolish)  options: level; average | bury; embed | tower; pagoda
    reading こわ.す   (kun): wrong options from distractors 2/3 (rest filled from other cards)
    reading こわ.れる  (kun): wrong options from distractors 2/3 (rest filled from other cards)
奏 (play music; report to a ruler)  options: spring season | heaven, sky | reality; fruit
    reading ソウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
契 (pledge; vow; agreement)  options: big, large | heaven, sky | minute, part
    reading ケイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
奨 (encourage; exhort; promote)  options: beauty | interior; depths | strange; extraordinary
    reading ショウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
奪 (snatch; rob; deprive)  options: gather | falcon | miscellaneous
    reading うば.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
妨 (hinder; obstruct; interfere)  options: older sister | begin, start | journey, travel
    reading さまた.げる (kun): wrong options from distractors 3/3 (rest filled from other cards)
威 (intimidate; authority; dignity)  options: become | years of age | decrease, reduce
    reading イ      (on): wrong options from distractors 3/3 (rest filled from other cards)
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
  attested reading とる (card text) is offered by 取 捕 採 撮 録; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [奪 取] -> とり とる どり; [奪 捕] -> つかまえる つかまる とらえる とらわれる とる
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (5 holders tried)
       sampling N1 stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling All stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 14 of 14 drawable wrong options seen
== 妨 (hinder; obstruct; interfere)   curated option cards: 姉 始 旅   tags: jlpt-n1 grade-8 structure-unclassified
   curated 姉: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on シ | kun あね はは
   curated 始: tags jlpt-n4 grade-3 structure-unclassified; in pools: N1 stack, All stack; on シ | kun はじ.める -はじ.める はじ.まる
   curated 旅: tags jlpt-n4 grade-3 compound starter; in pools: N1 stack, All stack, Starter practice session; on リョ | kun たび
   JMdict single-kanji entries: none
   unlisted readings attested for 妨: none
   on: no reading prompts
   kun prompt さまた.げる (key さまたげる)
       N1 stack: curated 姉 始 旅 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 姉 始 旅 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated 旅 -> 1 outcomes; deficit 2: the fallback fills the open slots; 12 drawable wrong options (1 curated, 11 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 12 of 12 drawable wrong options seen
== 威 (intimidate; authority; dignity)   curated option cards: 成 歳 減   tags: jlpt-n1 grade-8 structure-unclassified
   curated 成: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on セイ ジョウ | kun な.る な.す -な.す
   curated 歳: tags jlpt-n3 grade-8 structure-unclassified; in pools: N1 stack, All stack; on サイ セイ | kun とし とせ よわい
   curated 減: tags jlpt-n2 grade-5 structure-unclassified; in pools: N1 stack, All stack; on ゲン | kun へ.る へ.らす
   JMdict single-kanji entries: 2581990: leather strap binding the plates of traditional Japanese armor (armour) -> おどし; 2583080: power, authority, might -> い
   unlisted readings attested for 威: いさ (KANJIDIC2 name reading)  たけ (KANJIDIC2 name reading)  たけし (KANJIDIC2 name reading)
   on prompt イ (key い)
       N1 stack: curated 成 歳 減 -> 4 outcomes; deficit 0/1: the fallback fills the open slots; 35 drawable wrong options (4 curated, 31 fallback)
       All stack: curated 成 歳 減 -> 4 outcomes; deficit 0/1: the fallback fills the open slots; 35 drawable wrong options (4 curated, 31 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 14 drawable wrong options (0 curated, 14 fallback)
       sampling N1 stack: 200 seeds, 24 of 35 drawable wrong options seen
       sampling All stack: 200 seeds, 24 of 35 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 14 of 14 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 8 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
tes (31): あい い えい かい がい け けつ けん さい ざい すい せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading きつ (card text) is offered only by card(s) 喫 詰
       HIT (can be drawn): unlisted reading けつ (card text) is offered by card(s) 傑 欠 決 結 血
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading せつ (card text) is offered only by card(s) 切 折 接 殺 節 設 説 雪
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 奨 (encourage; exhort; promote)   curated option cards: 美 奥 奇
   metadata readings: on ショウ ソウ | kun すす.める
   unlisted readings attested for 奨: まさし (KANJIDIC2 name reading)
   on prompt ショウ (key しょう)
       excluded keys: 9
       curated 美: び み
       curated 奥: おう
       curated 奇: き
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 42 keys, 2: 159 keys, 1: 2 keys, 0: 38 keys
       tier 4 candidates (1): しゅう
       tier 3 candidates (42): おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しき しち しつ しゃ しゃく しゅ しゅく しゅつ しゅん しょく しん じゅう すう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう ... (+2 more)
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 奪 (snatch; rob; deprive)   curated option cards: 集 隼 雑
   metadata readings: on ダツ | kun うば.う
   unlisted readings attested for 奪: とる (card text)
   on: no reading prompts
   kun prompt うば.う (key うばう)
       excluded keys: 5
       curated 集: あつまる あつめる つどう
       curated 隼: はやぶさ
       curated 雑: まじえる まじる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 7 keys, 3: 89 keys, 2: 732 keys, 1: 2 keys, 0: 34 keys
       tier 4 candidates (7): うかがう うしなう うたう うたがう うやまう うらなう うるおう
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading とる (card text) is offered only by card(s) 取 捕 採 撮 録
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 妨 (hinder; obstruct; interfere)   curated option cards: 姉 始 旅
   metadata readings: on ボウ | kun さまた.げる
   unlisted readings attested for 妨: none
   on: no reading prompts
   kun prompt さまた.げる (key さまたげる)
       excluded keys: 7
       curated 姉: あね はは
       curated 始: はじめる はじめる はじまる
       curated 旅: たび
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 3 keys, 3: 155 keys, 2: 144 keys, 1: 145 keys, 0: 426 keys
       tier 4 candidates (3): さかえる ささえる さだめる
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1668 other kun-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 威 (intimidate; authority; dignity)   curated option cards: 成 歳 減
   metadata readings: on イ | kun おど.す おど.し おど.かす
   unlisted readings attested for 威: いさ (KANJIDIC2 name reading)  たけ (KANJIDIC2 name reading)  たけし (KANJIDIC2 name reading)
   on prompt イ (key い)
       excluded keys: 18
       curated 成: せい じょう
       curated 歳: さい せい
       curated 減: げん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 33 keys, 2: 187 keys, 0: 29 keys
       tier 3 candidates (33): あい いき いく いち いん えい かい がい けい げい さい ざい すい せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       unlisted-reading check: none of the 3 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 18 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
2 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 17; expected pairs: 17; added link pairs: 17; total added links: 17; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze b6020f9e): python -X utf8 kanji_remarks.py REPO e7eb6886e0b05cb84d9b60d268513b316ad71a82 kanji-remarks.json 噴 垂 垣 執 堅 塊 墨 壁 壊 奏 契 奨 奪 妨 威
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/張.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze b6020f9e): python -X utf8 meta_scan.py REPO 噴 垂 垣 執 堅 塊 墨 壁 壊 奏 契 奨 奪 妨 威
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 22
   噴.md:25: 噴霧 2656950 not listed part of 噴霧器
   噴.md:36: 出す 1338180 not listed part of 噴き出す
   噴.md:38: 吹き 2759690 not listed part of 吹き出す
   噴.md:38: 出す 1338180 not listed part of 吹き出す
   垂.md:32: 枝垂 2609670 not listed part of 枝垂れる
   垂.md:32: 枝垂れ 2609670 not listed part of 枝垂れる
   垂.md:49: 下垂 1185500 not listed part of 胃下垂
   垣.md:36: 紫微 2248140 not listed part of 紫微垣
   垣.md:49: 垣間 2722450 not listed part of 垣間見る
   垣.md:49: 見る 1259290 not listed part of 垣間見る
   堅.md:39: 義理 1225920 not listed part of 義理堅い
   墨.md:44: 水墨 2568680 not listed part of 水墨画
   墨.md:44: 墨画 1521520 not listed part of 水墨画
   墨.md:60: 戦争 1390360 not listed part of 米墨戦争
   壁.md:56: 新聞 1362360 not listed part of 壁新聞
   壊.md:25: 金剛 1242880 not listed part of 金剛不壊
   壊.md:25: 不壊 2597890 not listed part of 金剛不壊
   奨.md:37: 奨め 1210900 not listed part of 奨める
   奨.md:37: 勧め 1210900 not listed part of 勧める
   奪.md:25: 三振 1300990 not listed part of 奪三振
   奪.md:38: 取る 1326980 not listed part of 奪い取る
   妨.md:25: 業務 1239540 not listed part of 業務妨害
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8913, 'entries': 8928, 'retainedBytes': 50871639, 'inflatedBytes': 51143217, 'localZipBytes': 31959139, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze b6020f9e: manifest.json: 8906 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 4019d4e744afd6f4
manifest.json sha256 before 39BF9E1476AF5958F2593077D258BDBAFA37EA2B985E3899C2B2497675B90B34, after 39BF9E1476AF5958F2593077D258BDBAFA37EA2B985E3899C2B2497675B90B34; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 436 tests in 66.909s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
