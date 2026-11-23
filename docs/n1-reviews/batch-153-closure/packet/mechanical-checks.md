# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 22
WARN  words/日陰.md: Dictionary: line cites no JMdict entry id
WARN  words/醜い.md: Dictionary: line cites no JMdict entry id
WARN  words/鑑賞.md: Dictionary: line cites no JMdict entry id
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 22
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
酌 (pour sake; ladle)  options: boil; simmer; stew | bake; burn | strangle; wring; squeeze
    reading く.む    (kun): wrong options from distractors 3/3 (rest filled from other cards)
酔 (drunk; intoxicated)  options: sleep; sleepy | grow tired | cry; weep; sob
    reading よ.う    (kun): wrong options from distractors 3/3 (rest filled from other cards)
酢 (vinegar)  options: salt | wheat; barley | oil; grease
    reading す      (kun): wrong options from distractors 3/3 (rest filled from other cards)
醜 (ugly; unsightly)  options: short | red | new
    reading みにく.い  (kun): wrong options from distractors 3/3 (rest filled from other cards)
釈 (interpret; explain)  options: write | hear, ask | study
    reading シャク    (on): wrong options from distractors 3/3 (rest filled from other cards)
釣 (angling; lure)  options: mow; reap | dig; excavate | dive; submerge; lurk
    reading つ.る    (kun): wrong options from distractors 3/3 (rest filled from other cards)
鈴 (small bell)  options: flute; whistle | koto; zither | fan; incite
    reading すず     (kun): wrong options from distractors 2/3 (rest filled from other cards)
銃 (gun; firearm)  options: sword; double-edged blade | arrow; wedge | shield; buckler
    reading ジュウ    (on): wrong options from distractors 2/3 (rest filled from other cards)
銭 (coin; sen (1/100 yen))  options: bowl; flowerpot | needle; pin | tax; fiscal duty
    reading セン     (on): wrong options from distractors 3/3 (rest filled from other cards)
鎖 (chain; shut)  options: rope; cord | needle; pin | sash; zone
    reading くさり    (kun): wrong options from distractors 3/3 (rest filled from other cards)
鐘 (hanging bell; gong)  options: flag; banner; standard | pillar; post | bottle; jar
    reading かね     (kun): wrong options from distractors 3/3 (rest filled from other cards)
鑑 (model; appraise)  options: layer; stratum | summit; receive | tower; pagoda
    reading カン     (on): wrong options from distractors 3/3 (rest filled from other cards)
附 (affix; append)  options: outside | go out, exit | interval, between
    reading フ      (on): wrong options from distractors 3/3 (rest filled from other cards)
陥 (fall into; cave in)  options: rise; ascend | hop; spring up | float
    reading カン     (on): wrong options from distractors 2/3 (rest filled from other cards)
陰 (shade; yin)  options: sunshine | light; radiance | flame; blaze; inflammation
    reading かげ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
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
-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun は.ねる
   curated 浮: tags jlpt-n3 grade-8 structure-unclassified; in pools: N1 stack, All stack; on フ | kun う.く う.かれる う.かぶ う.かべる
   JMdict single-kanji entries: none
   unlisted readings attested for 陥: none
   on prompt カン (key かん)
       N1 stack: curated 昇 浮 -> 1 outcomes; deficit 1: the fallback fills the open slots; 58 drawable wrong options (2 curated, 56 fallback)
       All stack: curated 昇 浮 -> 1 outcomes; deficit 1: the fallback fills the open slots; 58 drawable wrong options (2 curated, 56 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 24 drawable wrong options (0 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 48 of 58 drawable wrong options seen
       sampling All stack: 200 seeds, 48 of 58 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
   kun: no reading prompts
== 陰 (shade; yin)   curated option cards: 陽 光 炎   tags: jlpt-n1 grade-8 structure-unclassified
   curated 陽: tags jlpt-n3 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ヨウ | kun ひ
   curated 光: tags jlpt-n3 grade-2 structure-unclassified; in pools: N1 stack, All stack; on コウ | kun ひか.る ひかり
   curated 炎: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun ほのお
   JMdict single-kanji entries: 1170230: (the) negative (e.g. pole) -> いん; 1590150: shade, shadow -> かげ; 2656090: [archaic] female private parts, female genitals -> ほと
   unlisted readings attested for 陰: おん (--extra list)  あん (--extra list)  くらい (--extra list)  ひそか (--extra list)  ほと (--extra list, JMdict 2656090)  いんうつ (--extra list)  いんに (--extra list)  いんにこもる (--extra list)
   on: no reading prompts
   kun prompt かげ (key かげ)
       N1 stack: curated 陽 光 炎 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 陽 光 炎 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 7 drawable wrong options (0 curated, 7 fallback)
       attested reading おん (--extra list) is offered by 御; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [陰 御] -> お おん み
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (1 holders tried)
       attested reading くらい (--extra list) is offered by 位 夢 暗; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [陰 位] -> くらい ぐらい; [陰 夢] -> くらい ゆめ ゆめみる
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (3 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 7 of 7 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 8 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
かぶ かぶる かべ ... (+27 more)
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 1737 other kun-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 鑑 (model; appraise)   curated option cards: 層 頂 塔
   metadata readings: on カン | kun かんが.みる かがみ
   unlisted readings attested for 鑑: あき (KANJIDIC2 name reading)  あきら (KANJIDIC2 name reading)
   on prompt カン (key かん)
       excluded keys: 8
       curated 層: そう
       curated 頂: ちょう
       curated 塔: とう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 56 keys, 2: 197 keys
       tier 3 candidates (56): あん いん うん えん おん か かい かく かっ かつ きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ... (+16 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 302 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 附 (affix; append)   curated option cards: 外 出 間
   metadata readings: on フ | kun つ.ける つ.く
   unlisted readings attested for 附: ぶ (--extra list)  ふす (--extra list)  ふする (--extra list)  ずき (KANJIDIC2 name reading)  づけ (KANJIDIC2 name reading)
   on prompt フ (key ふ)
       excluded keys: 8
       curated 外: がい げ
       curated 出: しゅつ すい
       curated 間: かん けん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 4 keys, 2: 222 keys, 0: 31 keys
       tier 3 candidates (4): ふう ふく ふつ ふん
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading ぶ (--extra list) is offered only by card(s) 不 分 夫 武 歩 舞 豊 部
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 陥 (fall into; cave in)   curated option cards: 昇 跳 浮
   metadata readings: on カン | kun おちい.る おとしい.れる
   unlisted readings attested for 陥: none
   on prompt カン (key かん)
       excluded keys: 13
       curated 昇: しょう
       curated 跳: no usable on reading, slot filled from the fallback
       curated 浮: ふ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 56 keys, 2: 197 keys
       tier 3 candidates (56): あん いん うん えん おん か かい かく かっ かつ きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ... (+16 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 302 other on-reading cards
       simulation: 37 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 陰 (shade; yin)   curated option cards: 陽 光 炎
   metadata readings: on イン | kun かげ かげ.る
   unlisted readings attested for 陰: おん (--extra list)  あん (--extra list)  くらい (--extra list)  ひそか (--extra list)  ほと (--extra list)  いんうつ (--extra list)  いんに (--extra list)  いんにこもる (--extra list)
   on: no reading prompts
   kun prompt かげ (key かげ)
       excluded keys: 7
       curated 陽: ひ
       curated 光: ひかる ひかり
       curated 炎: ほのお
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 57 keys, 2: 738 keys, 1: 9 keys, 0: 123 keys
       tier 3 candidates (57): か かい かいこ かう かえす かえで かえる かお かかる かがみ かき かぎる かく かこむ かさ かしら かす かず かせ かせぐ かぜ かた かたい かたな かたる かつ かつぐ かつら かど かなう かなめ かね かねる かぶ かぶる かべ かま かまう かみ かめ ... (+17 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading おん (--extra list) is offered only by card(s) 御
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading くらい (--extra list) is offered only by card(s) 位 夢 暗
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
2 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 20; expected pairs: 20; added link pairs: 20; total added links: 20; declared remark edits: 2; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze1 cdab83b3): python -X utf8 kanji_remarks.py REPO 67b9567098ae1a2fe357f53fac530188788ba1ba C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b153\links\kanji-remarks.json 酌 酔 酢 醜 釈 釣 鈴 銃 銭 鎖 鐘 鑑 附 陥 陰
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/属.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
EPO 酌 酔 酢 醜 釈 釣 鈴 銃 銭 鎖 鐘 鑑 附 陥 陰
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
銃.md:23: 鉄砲 1438010 not listed
銭.md:23: 分の一 2269760 not listed
鎖.md:23: つなぎ合わせる 1008140 not listed
鎖.md:23: 錠前 1357130 not listed
鐘.md:46: 時計 1316140 not listed
鑑.md:23: 手本 1328390 not listed
鑑.md:23: 模範 1533690 not listed
鑑.md:23: 見わける 1260020 not listed
附.md:23: 補説 2179450 not listed
附.md:54: 手渡す 1328210 not listed
附.md:55: 届ける 1457210 not listed
附.md:56: 任せる 1467150 not listed
陥.md:23: 欠ける 1253920 not listed
陥.md:51: おとし穴 1548640 not listed
陰.md:53: 暗い 1154330 not listed
陰.md:53: 曇る 1457560 not listed
陰.md:54: 時間 1315920 not listed
-- whole-run gaps: 17; part-of-run matches not listed: 64
   酌.md:40: 交わす 1590750 not listed part of 酌み交わす
   酌.md:50: 察す 2409970 not listed part of 察する
   酔.md:23: 払い 1611280 not listed part of 酔っ払い
   酔.md:43: 二日 1462900 not listed part of 二日酔い
   酢.md:48: 報い 1642330 not listed part of 報いる
   釣.md:23: 合う 1284430 not listed part of 釣り合う
   釣.md:45: 合い 1284320 not listed part of 釣り合い
   鈴.md:23: 鳴らす 1532880 not listed part of 振って鳴らす器具
   鈴.md:23: 器具 1218920 not listed part of 振って鳴らす器具
   銃.md:23: 武器 1498460 not listed part of 武器の一つ
   銃.md:23: 一つ 1160820 not listed part of 武器の一つ
   銃.md:23: 弾丸 1419440 not listed part of 弾丸を発射する小型の武器
   銃.md:23: 発射 1477490 not listed part of 弾丸を発射する小型の武器
   銃.md:23: 射す 1322170 not listed part of 弾丸を発射する小型の武器
   銃.md:23: 小型 1620810 not listed part of 弾丸を発射する小型の武器
   銃.md:23: 武器 1498460 not listed part of 弾丸を発射する小型の武器
   銭.md:23: 一円 1161130 not listed part of 一円の一
   銭.md:23: 分の 2145670 not listed part of 分の一
   銭.md:34: 農具 1643240 not listed part of 農具の一種
   銭.md:34: 一種 1163170 not listed part of 農具の一種
   銭.md:42: 入れ 1465600 not listed part of 銭入れ
   鎖.md:23: 合わせ 1284470 not listed part of つなぎ合わせる
   鎖.md:23: 合わせる 1284480 not listed part of つなぎ合わせる
   鐘.md:23: 打楽器 1408860 not listed part of 打楽器の一
   鐘.md:23: 楽器 1207340 not listed part of 打楽器の一
   鑑.md:23: 見わけ 1611860 not listed part of 見わける
   鑑.md:23: 見る 1259290 not listed part of 照らしあわせて見る
   鑑.md:23: 資料 1312820 not listed part of 資料を並べて手本とする書物
   鑑.md:23: 並べて 2569660 not listed part of 資料を並べて手本とする書物
   鑑.md:23: 手本 1328390 not listed part of 資料を並べて手本とする書物
   鑑.md:23: 書物 1344150 not listed part of 資料を並べて手本とする書物
   鑑.md:49: 反省 1480540 not listed part of 反省の資となる前例や手本
   鑑.md:49: 前例 1394190 not listed part of 反省の資となる前例や手本
   鑑.md:49: 手本 1328390 not listed part of 反省の資となる前例や手本
   鑑.md:51: 見分 1617840 not listed part of よしあしを見分ける
   鑑.md:51: 見分け 1611860 not listed part of よしあしを見分ける
   鑑.md:51: 見分ける 1260020 not listed part of よしあしを見分ける
   鑑.md:51: 分け 1502990 not listed part of よしあしを見分ける
   鑑.md:51: 分ける 1503000 not listed part of よしあしを見分ける
   鑑.md:54: 点検 1441540 not listed part of よく点検する
   鑑.md:54: 検する 2504560 not listed part of よく点検する
   鑑.md:60: 身分 1365810 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 資格 1312690 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 見分 1617840 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 見分け 1611860 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 見分ける 1260020 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 分け 1502990 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 分ける 1503000 not listed part of 身分・資格などを見分ける証拠
   鑑.md:60: 証拠 1351600 not listed part of 身分・資格などを見分ける証拠
   附.md:23: 通用 1433570 not listed part of と通用する
   附.md:32: 附け 1495750 not listed part of 附ける
   附.md:32: 付け 1495750/1495760 not listed part of 付ける
   附.md:51: 付き 1583630 not listed part of 付き従う
   附.md:51: 従う 1335210 not listed part of 付き従う
   附.md:55: 届け 1598810 not listed part of 届ける
   附.md:56: 任せ 2741830 not listed part of 任せる
   陥.md:23: 攻め 1279120 not listed part of 攻めおとされる
   陥.md:23: 欠け 1253910 not listed part of 欠ける
   陥.md:23: 不足 1493700 not listed part of 不足する
   陥.md:23: 足す 1404700 not listed part of 不足する
   陥.md:48: 地面 1421510 not listed part of 地面がへこむ
   陰.md:54: 移り 1854920 not listed part of 移りゆく日かげ
   陰.md:54: 移りゆく 1158180 not listed part of 移りゆく日かげ
   陰.md:55: 北側 1584180 not listed part of 山の北側
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9678, 'entries': 9694, 'retainedBytes': 56315617, 'inflatedBytes': 56745181, 'localZipBytes': 36211935, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze1 cdab83b3: manifest.json: 9671 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version a736997f1ae15901
manifest.json sha256 before C07E9C581641C7598A6FF402F26FE5A3C221A5B2385D039AD31537CE7FE63F3C, after C07E9C581641C7598A6FF402F26FE5A3C221A5B2385D039AD31537CE7FE63F3C; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 71.755s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
