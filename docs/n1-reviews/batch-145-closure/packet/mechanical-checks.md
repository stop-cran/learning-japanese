# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 17, words checked: 22
WARN  words/不潔.md: Dictionary: line cites no JMdict entry id
WARN  words/湧く.md: Dictionary: line cites no JMdict entry id
WARN  words/潜る.md: Dictionary: line cites no JMdict entry id
WARN  words/澄む.md: Dictionary: line cites no JMdict entry id
WARN  words/蒸し暑い.md: Dictionary: line cites no JMdict entry id
0 error(s), 5 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 17, words checked: 22
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
湧 (well up; surge; arise)  options: harbor | concentrated; dark | fishing; fishery
    reading わ.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
源 (source; headwaters; origin)  options: desert; vague | damp, moist | harbor
    reading ゲン     (on): wrong options from distractors 3/3 (rest filled from other cards)
滅 (perish; destroy; die out)  options: sea, ocean | water | fire
    reading メツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
滑 (slide; slippery; smooth)  options: lake | concentrated; dark | tears
    reading すべ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
滞 (stagnate; stay; be delayed)  options: fishing; fishery | cool, refreshing | lake
    reading タイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
漫 (aimless; rambling; comic)  options: sea, ocean | water | sun, day
    reading マン     (on): wrong options from distractors 3/3 (rest filled from other cards)
漬 (soak; pickle; steep)  options: blame; hold responsible | fishing; fishery | cross over
    reading つ.ける   (kun): wrong options from distractors 3/3 (rest filled from other cards)
潔 (clean; pure; upright)  options: fishing; fishery | melt; dissolve | cross over
    reading ケツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
潜 (dive; submerge; lurk)  options: fishing; fishery | melt; dissolve | cross over
    reading もぐ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
澄 (clear; become transparent; serene)  options: sea, ocean | water | river
    reading す.む    (kun): wrong options from distractors 3/3 (rest filled from other cards)
濁 (muddy; cloudy; impure; voiced)  options: touch; contact | cross over | hot water
    reading にご.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
瀬 (shallows; rapids; position)  options: hot water | damp, moist | drip; drop
    reading せ      (kun): wrong options from distractors 3/3 (rest filled from other cards)
災 (calamity; disaster; misfortune)  options: go around; patrol; tour | cook rice; boil | ashes
    reading サイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
炎 (flame; blaze; inflammation)  options: pale; faint; plain; unsalted | converse; consult | cook rice; boil
    reading ほのお    (kun): wrong options from distractors 1/3 (rest filled from other cards)
為 (do; act; for the sake of)  options: black | fish | fire
    reading な.す    (kun): wrong options from distractors 3/3 (rest filled from other cards)
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
 cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [炎 抜] -> ぬかす ぬかる ぬき ぬく ぬける; [炎 温] -> あたたか あたたかい あたたまる あたためる ぬく
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (2 holders tried)
       attested reading もえる (card text) is offered by 燃; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [炎 燃] -> もえる もす もやす
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (1 holders tried)
       sampling N1 stack: 200 seeds, 25 of 25 drawable wrong options seen
       sampling All stack: 200 seeds, 25 of 25 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
== 為 (do; act; for the sake of)   curated option cards: 黒 魚 火   tags: jlpt-n1 grade-8 structure-unclassified
   curated 黒: tags jlpt-n4 grade-2 compound starter; in pools: N1 stack, All stack, Starter practice session; on コク | kun くろ くろ.ずむ くろ.い
   curated 魚: tags jlpt-n4 grade-2 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ギョ | kun うお さかな -ざかな
   curated 火: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on カ | kun ひ -び ほ-
   JMdict single-kanji entries: 1157080: [word usually written using kana alone] good, advantage, benefit -> ため; 2219050: [word usually written using kana alone] to do -> す; 2870964: second string of a koto (counting from the player's near side) -> い
   unlisted readings attested for 為: びい (KANJIDIC2 name reading)  す (card text, JMdict 2219050)  た (card text)  されつつある (card text)  される (card text)
   on: no reading prompts
   kun prompt な.す (key なす)
       N1 stack: curated 黒 魚 火 -> 27 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 9 drawable wrong options (9 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       attested reading す (card text, JMdict 2219050) is offered by 州 巣; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [為 州] -> す; [為 巣] -> す
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (2 holders tried)
       attested reading た (card text) is offered by 手 田; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [為 手] -> た て; [為 田] -> た
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (2 holders tried)
       sampling N1 stack: 200 seeds, 9 of 9 drawable wrong options seen
       sampling All stack: 200 seeds, 9 of 9 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 9 of 9 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 10 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
offered by any of the 1697 other kun-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 瀬 (shallows; rapids; position)   curated option cards: 湯 湿 滴
   metadata readings: on ライ | kun せ
   unlisted readings attested for 瀬: せと (card text)  いわた (KANJIDIC2 name reading)  がせ (KANJIDIC2 name reading)  しげ (KANJIDIC2 name reading)  せい (KANJIDIC2 name reading)  せっ (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt せ (key せ)
       excluded keys: 2
       curated 湯: ゆ
       curated 湿: しめる しめす うるおう うるおす
       curated 滴: しずく したたる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 7 keys, 2: 434 keys, 1: 2 keys, 0: 418 keys
       tier 3 candidates (7): あせ かせ せき せく せる とせ みせ
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading せい (KANJIDIC2 name reading) is offered only by card(s) 背
       simulation: 7 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 災 (calamity; disaster; misfortune)   curated option cards: 巡 炊 灰
   metadata readings: on サイ | kun わざわ.い
   unlisted readings attested for 災: none
   on prompt サイ (key さい)
       excluded keys: 4
       curated 巡: じゅん
       curated 炊: すい
       curated 灰: かい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 33 keys, 2: 214 keys
       tier 3 candidates (33): あい い えい かい がい けい げい さ さく さっ さつ さん すい せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 300 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 炎 (flame; blaze; inflammation)   curated option cards: 淡 談 炊
   metadata readings: on エン | kun ほのお
   unlisted readings attested for 炎: もえる (card text)  ほむら (card text)  ぬく (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt ほのお (key ほのお)
       excluded keys: 7
       curated 淡: no usable kun reading, slot filled from the fallback
       curated 談: no usable kun reading, slot filled from the fallback
       curated 炊: たく
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 24 keys, 2: 839 keys, 1: 1 keys, 0: 40 keys
       tier 3 candidates (24): あお うお おお かお しお とお ほうる ほか ほがらか ほこ ほし ほす ほそい ほたる ほっする ほとけ ほとり ほど ほどく ほね ほぼ ほめる ほる ほろびる
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading もえる (card text) is offered only by card(s) 燃
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading ぬく (KANJIDIC2 name reading) is offered only by card(s) 抜 温
       simulation: 25 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 為 (do; act; for the sake of)   curated option cards: 黒 魚 火
   metadata readings: on イ | kun ため な.る な.す す.る たり つく.る なり
   unlisted readings attested for 為: す (card text)  た (card text)  されつつある (card text)  される (card text)  びい (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt な.す (key なす)
       excluded keys: 15
       curated 黒: くろ くろずむ くろい
       curated 魚: うお さかな ざかな
       curated 火: ひ び ほ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 3 keys, 3: 109 keys, 2: 641 keys, 1: 10 keys, 0: 115 keys
       tier 4 candidates (3): なおす ながす ならす
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading す (card text) is offered only by card(s) 州 巣
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading た (card text) is offered only by card(s) 手 田
       simulation: 9 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
2 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 20; expected pairs: 20; added link pairs: 20; total added links: 20; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at frozen 845aefbb): python -X utf8 kanji_remarks.py REPO 305763eab81430f26c51446ed0532cc03910ffbb C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b145\kanji-remarks.json 湧 源 滅 滑 滞 漫 漬 潔 潜 澄 濁 瀬 災 炎 為
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/暑.md
OK remark-only edit: kanji/渋.md
new cards: 15/15; modified existing cards: 2; declared remark edits applied: 2; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at frozen 845aefbb): python -X utf8 meta_scan.py REPO 湧 源 滅 滑 滞 漫 漬 潔 潜 澄 濁 瀬 災 炎 為
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 29
   滅.md:48: 入る 1465580/1465590 not listed part of 滅入る
   漫.md:41: 漫り 2714830 not listed part of 漫りに
   漫.md:46: 妄り 2714830 not listed part of 妄りに
   漫.md:46: 濫り 2714830 not listed part of 濫りに
   漫.md:46: 猥り 2714830 not listed part of 猥りに
   漫.md:46: 乱り 2714830 not listed part of 乱りに
   漬.md:23: 漬け 2083400 not listed part of 漬ける
   漬.md:23: 付け 1495750/1495760 not listed part of 付ける
   漬.md:36: 漬け 2083400 not listed part of 塩漬け
   漬.md:39: 漬け 2083400 not listed part of 漬けます
   漬.md:39: 漬け 2083400 not listed part of 漬けて
   漬.md:39: 漬け 2083400 not listed part of 茶漬け
   漬.md:39: 漬け 2083400 not listed part of 粕漬け
   漬.md:39: 漬け 2083400 not listed part of 糟漬け
   漬.md:39: 漬け 2083400 not listed part of かす漬け
   漬.md:41: 漬け 2083400 not listed part of 漬け物
   漬.md:41: 漬け 2083400 not listed part of 漬けもの
   潔.md:44: 良い 1605820 not listed part of いさぎ良い
   潔.md:44: 良い 1605820 not listed part of 潔良い
   潜.md:47: 地下 1420840/2872078 not listed part of 地下に潜る
   潜.md:47: 潜り 1391260/2097230 not listed part of 潜り込む
   潜.md:47: 込む 1593410 not listed part of 潜り込む
   潜.md:47: 込む 1593410 not listed part of もぐり込む
   潜.md:47: 潜り 1391260/2097230 not listed part of 潜りこむ
   澄.md:36: 聞き 2701450 not listed part of 聞き澄ます
   澄.md:38: 研ぎ 1897300 not listed part of 研ぎ澄ます
   澄.md:40: 澄まし 2678820 not listed part of 澄まし顔
   瀬.md:36: 立つ 1597040 not listed part of 立つ瀬
   為.md:25: 為政 1803550 not listed part of 為政者
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9124, 'entries': 9140, 'retainedBytes': 51778664, 'inflatedBytes': 52137755, 'localZipBytes': 32403162, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at frozen 845aefbb: manifest.json: 9117 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 0119fa9f674ffd74
manifest.json sha256 before 223FD5FC623BB60B9DED4028DF65C5B04C3CF2CCD7016ADE56CF12DB183701B6, after 223FD5FC623BB60B9DED4028DF65C5B04C3CF2CCD7016ADE56CF12DB183701B6; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 55.988s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
