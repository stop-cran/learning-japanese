# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 25
WARN  words/煮る.md: Dictionary: line cites no JMdict entry id
WARN  words/矛盾.md: Dictionary: line cites no JMdict entry id
WARN  words/不潔.md: Dictionary: line cites no JMdict entry id
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 25
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
煮 (boil; simmer; stew)  options: fire | water | meat; flesh
    reading に.る    (kun): wrong options from distractors 3/3 (rest filled from other cards)
熟 (ripen; mature; skilled)  options: language, word | tree, wood | rice field
    reading ジュク    (on): wrong options from distractors 3/3 (rest filled from other cards)
牧 (pasture; raise livestock; pastor)  options: song, sing | mountain | rain
    reading ボク     (on): wrong options from distractors 3/3 (rest filled from other cards)
狂 (go mad; frenzied; go awry)  options: dog | spirit, air | wind; style
    reading くる.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
狭 (narrow; cramped; confined)  options: road, way | room, chamber | shop
    reading せま.い   (kun): wrong options from distractors 3/3 (rest filled from other cards)
献 (offer; contribute; dedicate)  options: cat | alone; sole; Germany (abbreviation) | condition; form
    reading ケン     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading コン     (on): wrong options from distractors 3/3 (rest filled from other cards)
玄 (mysterious; profound; dark)  options: rate; lead; frank | livestock; domestic animals | jewel; ball
    reading ゲン     (on): wrong options from distractors 3/3 (rest filled from other cards)
環 (ring; loop; surround)  options: actual; present | reason, logic | koto; zither
    reading カン     (on): wrong options from distractors 2/3 (rest filled from other cards)
甚 (extreme; excessive; very)  options: sweet; pamper | small-animal counter; equal | foundation; basis
    reading はなは.だ  (kun): wrong options from distractors 3/3 (rest filled from other cards)
癖 (habit; quirk; peculiarity)  options: grow tired | pain; hurt | heal; cure
    reading くせ     (kun): wrong options from distractors 2/3 (rest filled from other cards)
益 (benefit; profit; gain)  options: dish; plate | rain | fish
    reading エキ     (on): wrong options from distractors 3/3 (rest filled from other cards)
盛 (thrive; heap up; serve food)  options: mountain | sea, ocean | shop
    reading も.る    (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading さか.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
盾 (shield; buckler)  options: eye | direct; repair | true, genuine
    reading ジュン    (on): wrong options from distractors 3/3 (rest filled from other cards)
眺 (gaze; view; look out over)  options: mutual; aspect | prefecture | ministry; omit
    reading なが.める  (kun): wrong options from distractors 3/3 (rest filled from other cards)
睡 (sleep; doze)  options: true, genuine | wear; arrive | direct; repair
    reading スイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
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
 curated 目 直 真 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 6 drawable wrong options (6 curated, 0 fallback)
       All stack: curated 目 直 真 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 6 drawable wrong options (6 curated, 0 fallback)
       Starter practice session: curated 目 -> 2 outcomes; deficit 2: the fallback fills the open slots; 31 drawable wrong options (2 curated, 29 fallback)
       sampling N1 stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling All stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 31 of 31 drawable wrong options seen
   kun: no reading prompts
== 眺 (gaze; view; look out over)   curated option cards: 相 県 省   tags: jlpt-n1 grade-8 structure-unclassified
   curated 相: tags jlpt-n3 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ソウ ショウ | kun あい-
   curated 県: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ケン | kun か.ける
   curated 省: tags jlpt-n2 grade-4 structure-unclassified; in pools: N1 stack, All stack; on セイ ショウ | kun かえり.みる はぶ.く
   JMdict single-kanji entries: none
   unlisted readings attested for 眺: none
   on: no reading prompts
   kun prompt なが.める (key ながめる)
       N1 stack: curated 相 県 省 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 相 県 省 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 24 drawable wrong options (0 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
== 睡 (sleep; doze)   curated option cards: 真 着 直   tags: jlpt-n1 grade-8 structure-unclassified
   curated 真: tags jlpt-n4 grade-3 structure-unclassified; in pools: N1 stack, All stack; on シン | kun ま ま- まこと
   curated 着: tags jlpt-n4 grade-3 structure-unclassified; in pools: N1 stack, All stack; on チャク ジャク | kun き.る き.せる つ.く つ.ける
   curated 直: tags jlpt-n3 grade-2 structure-unclassified; in pools: N1 stack, All stack; on チョク ジキ ジカ | kun ただ.ちに なお.す -なお.す なお.る なお.き す.ぐ
   JMdict single-kanji entries: none
   unlisted readings attested for 睡: ねぶる (card text)  ねむり (card text)  ねぶたい (card text)  ねぶり (card text)
   on prompt スイ (key すい)
       N1 stack: curated 真 着 直 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 6 drawable wrong options (6 curated, 0 fallback)
       All stack: curated 真 着 直 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 6 drawable wrong options (6 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 12 drawable wrong options (0 curated, 12 fallback)
       sampling N1 stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling All stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 12 of 12 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 10 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
g options
   kun: no reading prompts
== 盛 (thrive; heap up; serve food)   curated option cards: 山 海 店
   metadata readings: on セイ ジョウ | kun も.る さか.る さか.ん
   unlisted readings attested for 盛: もり (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt も.る (key もる)
       excluded keys: 15
       curated 山: やま
       curated 海: うみ
       curated 店: みせ たな
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 4 keys, 3: 190 keys, 2: 561 keys, 1: 46 keys, 0: 77 keys
       tier 4 candidates (4): もえる もぐる もてる もどる
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading もり (KANJIDIC2 name reading) is offered only by card(s) 守 森
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt さか.る (key さかる)
       excluded keys: 15
       curated 山: やま
       curated 海: うみ
       curated 店: みせ たな
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 11 keys, 3: 302 keys, 2: 545 keys, 1: 8 keys, 0: 32 keys
       tier 4 candidates (11): さえる さかえる さぐる さげる ささえる ささる さだめる さとる さめる さる さわる
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading もり (KANJIDIC2 name reading) is offered only by card(s) 守 森
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 盾 (shield; buckler)   curated option cards: 目 直 真
   metadata readings: on ジュン | kun たて
   unlisted readings attested for 盾: none
   on prompt ジュン (key じゅん)
       excluded keys: 5
       curated 目: もく ぼく
       curated 直: ちょく じき じか
       curated 真: しん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 60 keys, 2: 150 keys, 1: 1 keys, 0: 40 keys
       tier 4 candidates (1): じん
       tier 3 candidates (60): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しん じき じつ じゃ じゃく じゅ じゅう じゅく じゅつ じょ じょう すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん ... (+20 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 眺 (gaze; view; look out over)   curated option cards: 相 県 省
   metadata readings: on チョウ | kun なが.める
   unlisted readings attested for 眺: none
   on: no reading prompts
   kun prompt なが.める (key ながめる)
       excluded keys: 5
       curated 相: あい
       curated 県: かける
       curated 省: かえりみる はぶく
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 10 keys, 3: 301 keys, 2: 314 keys, 1: 28 keys, 0: 273 keys
       tier 4 candidates (10): なおる ながらえる ながれる なぐさめる なげる なぞらえる なまける なまる ならべる なれる
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1704 other kun-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 睡 (sleep; doze)   curated option cards: 真 着 直
   metadata readings: on スイ | kun ねむ.る ねむ.い
   unlisted readings attested for 睡: ねぶる (card text)  ねむり (card text)  ねぶたい (card text)  ねぶり (card text)
   on prompt スイ (key すい)
       excluded keys: 4
       curated 真: しん
       curated 着: ちゃく じゃく
       curated 直: ちょく じき じか
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 32 keys, 2: 220 keys
       tier 3 candidates (32): あい い えい かい がい けい げい さい ざい す すう すん せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       unlisted-reading check: none of the 4 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 23; expected pairs: 23; added link pairs: 23; total added links: 23; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at frozen 38833c7f): python -X utf8 kanji_remarks.py REPO ffbf576ee0531e56f8f36e0a7287b53f443b0d29 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b146\kanji-remarks.json 煮 熟 牧 狂 狭 献 玄 環 甚 癖 益 盛 盾 眺 睡
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/潔.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at frozen 38833c7f): python -X utf8 meta_scan.py REPO 煮 熟 牧 狂 狭 献 玄 環 甚 癖 益 盛 盾 眺 睡
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 5
   煮.md:39: 凝り 1593460/2251170 not listed part of 煮凝り
   熟.md:39: 熟れ 1860760/2429210 not listed part of 熟れる
   狭.md:48: 苦しい 1244320 not listed part of 狭苦しい
   盛.md:43: 上がる 1352290 not listed part of 盛り上がる
   盾.md:36: 突く 1456890/1456895 not listed part of 盾突く
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9154, 'entries': 9170, 'retainedBytes': 51900630, 'inflatedBytes': 52259721, 'localZipBytes': 32461936, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at frozen 38833c7f: manifest.json: 9147 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 64b3062644ac03f2
manifest.json sha256 before A650FC2777832842803A95FB1E148EF40619019A00AC67CB69E7B691A349E9C0, after A650FC2777832842803A95FB1E148EF40619019A00AC67CB69E7B691A349E9C0; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 56.272s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
