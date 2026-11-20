# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 15, words checked: 17
WARN  words/校舎.md: Dictionary: line cites no JMdict entry id
WARN  words/翻訳.md: no Dictionary: line
WARN  words/艶.md: Dictionary: line cites no JMdict entry id
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 15, words checked: 17
WARN  words/翻訳.md: no Dictionary: line
0 error(s), 1 warning(s)
```

## quiz safety simulation

```text
翻 (turn over; reverse)  options: open; unfold | talk, speak | stand; set up
    reading ホン     (on): wrong options from distractors 3/3 (rest filled from other cards)
翼 (wing)  options: bird | fish | insect; bug
    reading つばさ    (kun): wrong options from distractors 3/3 (rest filled from other cards)
脈 (pulse; vein)  options: eye | hand | foot, leg
    reading ミャク    (on): wrong options from distractors 3/3 (rest filled from other cards)
腐 (rot; decay; spoil)  options: bake; burn | wash | boil; simmer; stew
    reading くさ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
臨 (face (a situation); attend)  options: reside, dwell | know | use, employ
    reading リン     (on): wrong options from distractors 3/3 (rest filled from other cards)
臭 (foul smell; stink)  options: snow | thread; yarn | bird
    reading くさ.い   (kun): wrong options from distractors 3/3 (rest filled from other cards)
興 (revival; interest; pleasure)  options: sky; empty | water | face; expression
    reading キョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
舌 (tongue)  options: mouth | ear | foot, leg
    reading した     (kun): wrong options from distractors 3/3 (rest filled from other cards)
舎 (house; lodging; hut)  options: rain | tree, wood | mountain
    reading シャ     (on): wrong options from distractors 3/3 (rest filled from other cards)
艶 (gloss; luster; allure)  options: ice; freeze | star; celestial point | fish
    reading つや     (kun): wrong options from distractors 3/3 (rest filled from other cards)
芝 (turf; lawn)  options: dog | stone | mountain
    reading しば     (kun): wrong options from distractors 3/3 (rest filled from other cards)
芽 (bud; sprout)  options: dog | mountain | water
    reading め      (kun): wrong options from distractors 3/3 (rest filled from other cards)
茂 (overgrown; lush)  options: dog | mountain | water
    reading しげ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
荘 (villa; manor; solemn)  options: dog | sun, day | rain
    reading ソウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
華 (flower; splendor; showiness)  options: dog | moon, month | water
    reading カ      (on): wrong options from distractors 3/3 (rest filled from other cards)
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
ls: N1 stack, All stack, Starter practice session; on ウ | kun あめ あま- -さめ
   JMdict single-kanji entries: 2249280: manor, villa -> しょう・そう; 2249290: counter for games of mahjong -> チャン
   unlisted readings attested for 荘: そ (KANJIDIC2 name reading)  しもやしき (card text)  かざる (card text)
   on prompt ソウ (key そう)
       N1 stack: curated 犬 日 雨 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       attested reading そ (KANJIDIC2 name reading) is offered by 想 礎 祖 粗 素 組; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [荘 想] -> そ; [荘 礎] -> そ
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (6 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 4 of 4 drawable wrong options seen
   kun: no reading prompts
== 華 (flower; splendor; showiness)   curated option cards: 犬 月 水   tags: jlpt-n1 grade-8 structure-unclassified
   curated 犬: tags jlpt-n4 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ケン | kun いぬ いぬ-
   curated 月: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ゲツ ガツ | kun つき
   curated 水: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on スイ | kun みず みず-
   JMdict single-kanji entries: 1194500: flower, blossom, bloom -> はな; 2842901: flashiness, showiness, brilliance -> か
   unlisted readings attested for 華: わ (KANJIDIC2 name reading)  げ (card text)  しろい (card text)
   on prompt カ (key か)
       N1 stack: curated 犬 月 水 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       attested reading わ (KANJIDIC2 name reading) is offered by 和 話; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [華 和] -> お わ; [華 話] -> わ
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (2 holders tried)
       attested reading げ (card text) is offered by 下 夏 外 解; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [華 下] -> げ; [華 夏] -> が げ
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (4 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 4 of 4 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 16 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
ngs: on ガ | kun め
   unlisted readings attested for 芽: めぐむ (card text)  じ (KANJIDIC2 name reading)  めぐ (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt め (key め)
       excluded keys: 2
       curated 犬: いぬ いぬ
       curated 山: やま
       curated 水: みず みず
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 12 keys, 2: 437 keys, 1: 6 keys, 0: 430 keys
       tier 3 candidates (12): あめ うめ かめ ぎめ こめ ぞめ つめ どめ めし めす ゆめ よめ
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading めぐむ (card text) is offered only by card(s) 恵
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading じ (KANJIDIC2 name reading) is offered only by card(s) 路
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 茂 (overgrown; lush)   curated option cards: 犬 山 水
   metadata readings: on モ | kun しげ.る
   unlisted readings attested for 茂: ぼう (card text)  すぐれる (card text)  うむさ (KANJIDIC2 name reading)  き (KANJIDIC2 name reading)  し (KANJIDIC2 name reading)  つとむ (KANJIDIC2 name reading)  む (KANJIDIC2 name reading)  もて (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt しげ.る (key しげる)
       excluded keys: 5
       curated 犬: いぬ いぬ
       curated 山: やま
       curated 水: みず みず
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 11 keys, 3: 306 keys, 2: 561 keys, 1: 9 keys, 0: 32 keys
       tier 4 candidates (11): しいる しずまる しずめる したたる しばる しぼる しみる しめる しらげる しらべる しる
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading すぐれる (card text) is offered only by card(s) 優 勝
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading き (KANJIDIC2 name reading) is offered only by card(s) 木 来 気 生 黄
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading む (KANJIDIC2 name reading) is offered only by card(s) 六
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 荘 (villa; manor; solemn)   curated option cards: 犬 日 雨
   metadata readings: on ソウ ショウ チャン | kun ほうき おごそ.か
   unlisted readings attested for 荘: しもやしき (card text)  かざる (card text)  そ (KANJIDIC2 name reading)
   on prompt ソウ (key そう)
       excluded keys: 20
       curated 犬: けん
       curated 日: にち じつ
       curated 雨: う
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 37 keys, 2: 212 keys
       tier 3 candidates (37): う おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しゅう じゅう すう そ そく そつ そん ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       info (can be drawn): そ is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 想 礎 祖 粗 素 組
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 華 (flower; splendor; showiness)   curated option cards: 犬 月 水
   metadata readings: on カ ケ | kun はな
   unlisted readings attested for 華: げ (card text)  しろい (card text)  わ (KANJIDIC2 name reading)
   on prompt カ (key か)
       excluded keys: 5
       curated 犬: けん
       curated 月: げつ がつ
       curated 水: すい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 6 keys, 2: 222 keys, 0: 31 keys
       tier 3 candidates (6): かい かく かっ かつ かん じか
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading げ (card text) is offered only by card(s) 下 夏 外 解
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading わ (KANJIDIC2 name reading) is offered only by card(s) 和 話
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 17; expected pairs: 17; added link pairs: 17; total added links: 17; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze 070b6f69): python -X utf8 kanji_remarks.py REPO 090faab2ce29168e9d9bbcee0021e5ecf1d7b798 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b149\r2\kanji-remarks.json 翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
new cards: 15/15; modified existing cards: 0; declared remark edits applied: 0; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze 070b6f69): python -X utf8 meta_scan.py REPO 翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
脈.md:41: 水脈 1657110/2255000 not listed
臨.md:40: 来臨 1548330 not listed
臭.md:54: 特に 1454670 not listed
興.md:46: 起こる 1223680 not listed
興.md:46: 起こす 1223660 not listed
舌.md:47: 舌禍 1387020 not listed
舌.md:47: 筆舌 1731950 not listed
舌.md:47: 舌戦 1387050 not listed
舌.md:47: 饒舌 1574520 not listed
舎.md:48: 舎弟 1321740 not listed
舎.md:50: 寄宿舎 1219740 not listed
舎.md:50: 舎監 1321710 not listed
芝.md:41: 霊芝 1916430 not listed
荘.md:44: 別宅 1509990 not listed
華.md:44: 華盛頓 1149020 not listed
-- whole-run gaps: 15; part-of-run matches not listed: 14
   脈.md:43: 望み 1519620 not listed part of 先の望み・見込み
   脈.md:43: 見込 1604480 not listed part of 先の望み・見込み
   脈.md:43: 見込み 1604480 not listed part of 先の望み・見込み
   脈.md:43: 込み 2078750 not listed part of 先の望み・見込み
   腐.md:33: 真面 1378040/2854581 not listed part of 真面目腐る
   腐.md:33: 真面目 1364350/1364360 not listed part of 真面目腐る
   腐.md:33: 面目 1533590 not listed part of 真面目腐る
   臭.md:33: 面倒 1533550 not listed part of 面倒臭い
   舎.md:50: 寄宿 1219730 not listed part of 寄宿舎
   艶.md:51: 美しい 1486360 not listed part of あでやかで美しい
   荘.md:45: 旅館 1553130 not listed part of やど・旅館
   華.md:45: 輝き 1224010 not listed part of 輝き・光・栄え
   華.md:45: 栄え 1600610/2842896/2871083 not listed part of 輝き・光・栄え
   華.md:45: 美しい 1486360 not listed part of はなやか・美しい
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9244, 'entries': 9260, 'retainedBytes': 52276965, 'inflatedBytes': 52636056, 'localZipBytes': 32642160, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze 070b6f69: manifest.json: 9237 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version d54a695542868df4
manifest.json sha256 before 12D5E31D222C2790BD48F7942E0A31134BCB2FE5D96A3AA645E563E3B18B90E3, after 12D5E31D222C2790BD48F7942E0A31134BCB2FE5D96A3AA645E563E3B18B90E3; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 93.178s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
