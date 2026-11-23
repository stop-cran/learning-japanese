# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 18, words checked: 27
WARN  words/瞳.md: Dictionary: line cites no JMdict entry id
WARN  words/透明.md: Dictionary: line cites no JMdict entry id
0 error(s), 2 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 18, words checked: 27
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
瞬 (blink; instant)  options: parent; close | test; verify | topic; question
    reading シュン    (on): wrong options from distractors 3/3 (rest filled from other cards)
瞳 (pupil of the eye; eyes)  options: true, genuine | wear; arrive | mutual; aspect
    reading ひとみ    (kun): wrong options from distractors 3/3 (rest filled from other cards)
矢 (arrow; wedge)  options: noon | cattle, cow | heaven, sky
    reading や      (kun): wrong options from distractors 3/3 (rest filled from other cards)
砕 (smash; crush; break into pieces)  options: investigate thoroughly | ten | sand
    reading くだ.く   (kun): wrong options from distractors 3/3 (rest filled from other cards)
礎 (cornerstone; foundation)  options: polish; study closely | music, enjoyment, ease | picture, brushstroke
    reading ソ      (on): wrong options from distractors 3/3 (rest filled from other cards)
秀 (excel; outstanding)  options: tree, wood | I; private | second as a time unit
    reading シュウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
秘 (secret; conceal)  options: tree, wood | second as a time unit | tax; fiscal duty
    reading ヒ      (on): wrong options from distractors 3/3 (rest filled from other cards)
稚 (immature; childish; young)  options: tree, wood | I; private | tax; fiscal duty
    reading チ      (on): wrong options from distractors 3/3 (rest filled from other cards)
稼 (earn; work hard)  options: tree, wood | I; private | second as a time unit
    reading かせ.ぐ   (kun): wrong options from distractors 2/3 (rest filled from other cards)
稿 (manuscript; draft)  options: tree, wood | I; private | tax; fiscal duty
    reading コウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
穏 (calm; gentle; peaceful)  options: tree, wood | rice field | flower
    reading おだ.やか  (kun): wrong options from distractors 3/3 (rest filled from other cards)
穴 (hole; pit; cavity)  options: investigate thoroughly | thrust; sudden | determine; settle
    reading あな     (kun): wrong options from distractors 3/3 (rest filled from other cards)
笛 (flute; whistle)  options: laugh | answer | brush; writing
    reading ふえ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
粋 (stylish; essence; pure)  options: rice grain | flour; powder | sugar
    reading スイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
糧 (provisions; food supply)  options: coarse; rough; crude | heavy; piled up | open field
    reading リョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
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
 options (0 curated, 4 fallback)
       attested reading う (KANJIDIC2 name reading) is offered by 卯; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [笛 卯] -> う
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (1 holders tried)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 4 of 4 drawable wrong options seen
== 粋 (stylish; essence; pure)   curated option cards: 米 粉 糖   tags: jlpt-n1 grade-8 structure-unclassified
   curated 米: tags jlpt-n3 grade-2 structure-unclassified; in pools: N1 stack, All stack; on ベイ マイ メエトル | kun こめ よね
   curated 粉: tags jlpt-n2 grade-5 structure-unclassified; in pools: N1 stack, All stack; on フン | kun デシメートル こ こな
   curated 糖: tags jlpt-n1 grade-6 structure-unclassified; in pools: N1 stack, All stack; on トウ | kun -
   JMdict single-kanji entries: 1372410: chic, smart, stylish -> いき; 2848938: essence, the best, cream -> すい
   unlisted readings attested for 粋: none
   on prompt スイ (key すい)
       N1 stack: curated 米 粉 糖 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 米 粉 糖 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 12 drawable wrong options (0 curated, 12 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 12 of 12 drawable wrong options seen
   kun: no reading prompts
== 糧 (provisions; food supply)   curated option cards: 粗 重 野   tags: jlpt-n1 grade-8 structure-unclassified
   curated 粗: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ソ | kun あら.い
   curated 重: tags jlpt-n4 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ジュウ チョウ | kun え おも.い おも.り おも.なう かさ.ねる かさ.なる おも
   curated 野: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on ヤ ショ | kun の の-
   JMdict single-kanji entries: 2017850: food, provisions -> かて・りょう・かりて
   unlisted readings attested for 糧: かりて (card text, JMdict 2017850)
   on prompt リョウ (key りょう)
       N1 stack: curated 粗 重 野 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 粗 重 野 -> 4 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 17 drawable wrong options (0 curated, 17 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 17 of 17 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 7 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
ずから おののく おびる おぼえる ... (+27 more)
       HIT (can be drawn): unlisted reading やすらか (card text) is offered by card(s) 安
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 穴 (hole; pit; cavity)   curated option cards: 究 突 定
   metadata readings: on ケツ | kun あな
   unlisted readings attested for 穴: めど (card text)  けつまんこ (card text)  けな (KANJIDIC2 name reading)  しし (KANJIDIC2 name reading)  な (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt あな (key あな)
       excluded keys: 4
       curated 究: きわめる
       curated 突: つく
       curated 定: さだめる さだまる さだか
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 75 keys, 2: 692 keys, 1: 17 keys, 0: 110 keys
       tier 4 candidates (1): あざな
       tier 3 candidates (75): あい あいだ あいて あう あえる あお あか あかい あかし あかり あがる あき あく あげる あさ あさい あさる あし あじ あずさ あせ あぜ あそぶ あたい あたう あたま あたり あたる あだ あつい あてる あと あに あね あばく あびる あぶら あまい あまつ あまる ... (+35 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading しし (KANJIDIC2 name reading) is offered only by card(s) 肉
       info (can be drawn): な is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 名 字 菜
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 笛 (flute; whistle)   curated option cards: 笑 答 筆
   metadata readings: on テキ | kun ふえ
   unlisted readings attested for 笛: じゃく (card text)  ちゃく (card text)  う (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt ふえ (key ふえ)
       excluded keys: 6
       curated 笑: わらう えむ
       curated 答: こたえる こたえ
       curated 筆: ふで
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 39 keys, 2: 731 keys, 1: 3 keys, 0: 124 keys
       tier 3 candidates (39): いえ いりえ うえ え かえ こえ こずえ こたえ ごえ すえ たまえ つくえ なえ はえ ばえ ひとえ ひのえ ふえる ふかい ふく ふくむ ふくろ ふける ふさ ふし ふせぐ ふた ふたつ ふだ ふで ふとい ふね ふみ ふゆ ふる ふるい ふるう ふれる まえ
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading う (KANJIDIC2 name reading) is offered only by card(s) 卯
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 粋 (stylish; essence; pure)   curated option cards: 米 粉 糖
   metadata readings: on スイ | kun いき
   unlisted readings attested for 粋: none
   on prompt スイ (key すい)
       excluded keys: 4
       curated 米: べい まい めえとる
       curated 粉: ふん
       curated 糖: とう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 32 keys, 2: 219 keys
       tier 3 candidates (32): あい い えい かい がい けい げい さい ざい す すう すん せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 糧 (provisions; food supply)   curated option cards: 粗 重 野
   metadata readings: on リョウ ロウ | kun かて
   unlisted readings attested for 糧: かりて (card text)
   on prompt リョウ (key りょう)
       excluded keys: 6
       curated 粗: そ
       curated 重: じゅう ちょう
       curated 野: や しょ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 38 keys, 2: 171 keys, 1: 2 keys, 0: 39 keys
       tier 4 candidates (1): りゅう
       tier 3 candidates (38): おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しゅう しょう じゅう じょう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りく りつ りゃく りょく りん
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 18; expected pairs: 18; added link pairs: 18; total added links: 18; declared remark edits: 3; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze 6a2323e7): python -X utf8 kanji_remarks.py REPO d97126fe54f7c060df157b933736c71e4f2caed9 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b147\kanji-remarks.json 瞬 瞳 矢 砕 礎 秀 秘 稚 稼 稿 穏 穴 笛 粋 糧
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/基.md
OK remark-only edit: kanji/密.md
OK remark-only edit: kanji/透.md
new cards: 15/15; modified existing cards: 3; declared remark edits applied: 3; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze 6a2323e7): python -X utf8 meta_scan.py REPO 瞬 瞳 矢 砕 礎 秀 秘 稚 稼 稿 穏 穴 笛 粋 糧
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 0
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9184, 'entries': 9200, 'retainedBytes': 52024923, 'inflatedBytes': 52384014, 'localZipBytes': 32522013, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze 6a2323e7: manifest.json: 9177 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version ce8db072c8838b3a
manifest.json sha256 before 700531E40B9AF53E281791BA218E31489B2A7DBAB7C78C2C592B32670558A76D, after 700531E40B9AF53E281791BA218E31489B2A7DBAB7C78C2C592B32670558A76D; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 62.119s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
