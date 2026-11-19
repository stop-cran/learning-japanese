# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 15, words checked: 17
WARN  words/一旦.md: Dictionary: line cites no JMdict entry id
WARN  words/凱旋.md: Dictionary: line cites no JMdict entry id
WARN  words/蒸し暑い.md: Dictionary: line cites no JMdict entry id
WARN  words/西暦.md: Dictionary: line cites no JMdict entry id
0 error(s), 4 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 15, words checked: 17
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
施 (carry out; give; alms)  options: rotate; return; mediate | flag; banner; standard | journey, travel
    reading シ      (on): wrong options from distractors 2/3 (rest filled from other cards)
旋 (rotate; return; mediate)  options: carry out; give; alms | flag; banner; standard | journey, travel
    reading セン     (on): wrong options from distractors 2/3 (rest filled from other cards)
旗 (flag; banner; standard)  options: carry out; give; alms | rotate; return; mediate | journey, travel
    reading はた     (kun): wrong options from distractors 1/3 (rest filled from other cards)
既 (already; previously)  options: good; favorable | sun, day | bright, clear
    reading すで.に   (kun): wrong options from distractors 3/3 (rest filled from other cards)
旦 (dawn; daybreak; morning)  options: moreover; also | eye | former; old
    reading タン     (on): wrong options from distractors 2/3 (rest filled from other cards)
旨 (purport; gist; delicious)  options: sun, day | early | person in a role
    reading シ      (on): wrong options from distractors 3/3 (rest filled from other cards)
暑 (hot weather; summer heat; hot season)  options: sun, day | early | person in a role
    reading あつ.い   (kun): wrong options from distractors 3/3 (rest filled from other cards)
暦 (calendar; almanac; year reckoning)  options: tree, wood | grove; woodland | sun, day
    reading レキ     (on): wrong options from distractors 3/3 (rest filled from other cards)
朗 (cheerful; clear; resonant)  options: moon, month | have, exist | morning
    reading ほが.らか  (kun): wrong options from distractors 3/3 (rest filled from other cards)
条 (clause; condition; item; line)  options: not yet | end; tip | bundle
    reading ジョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
架 (rack; bridge; overhead; imaginary)  options: tree, wood | end; tip | not yet
    reading カ      (on): wrong options from distractors 3/3 (rest filled from other cards)
柄 (handle; pattern; nature)  options: tree, wood | book, origin | rest
    reading がら     (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading え      (kun): wrong options from distractors 3/3 (rest filled from other cards)
染 (dye; stain; infect; permeate)  options: tree, wood | water | nine
    reading セン     (on): wrong options from distractors 3/3 (rest filled from other cards)
株 (share; stump; rooted plant)  options: not yet | book, origin | rest
    reading かぶ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
桜 (cherry tree; blossom)  options: woman, female | desk; writing table | apricot
    reading さくら    (kun): wrong options from distractors 3/3 (rest filled from other cards)
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
ted plant)   curated option cards: 未 本 休   tags: jlpt-n1 grade-6 structure-unclassified
   curated 未: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on ミ ビ | kun いま.だ ま.だ ひつじ
   curated 本: tags jlpt-n5 grade-1 indicative starter; in pools: N1 stack, All stack, Starter practice session; on ホン | kun もと
   curated 休: tags jlpt-n5 grade-1 compound starter; in pools: N1 stack, All stack, Starter practice session; on キュウ | kun やす.む やす.まる やす.める
   JMdict single-kanji entries: 1208920: stock, share -> かぶ; 1279450: stake, post, pile -> くい; 2645430: stump -> しゅ; 2645440: stump -> くいぜ・くいせ; 2737710: [archaic] stump -> かぶた
   unlisted readings attested for 株: くい (card text, JMdict 1279450)  くいぜ (card text, JMdict 2645440)  くいせ (JMdict 2645440)  かぶた (JMdict 2737710)
   on: no reading prompts
   kun prompt かぶ (key かぶ)
       N1 stack: curated 未 本 休 -> 9 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       All stack: curated 未 本 休 -> 9 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       Starter practice session: curated 本 休 -> 3 outcomes; deficit 1: the fallback fills the open slots; 12 drawable wrong options (4 curated, 8 fallback)
       sampling N1 stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling All stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 12 of 12 drawable wrong options seen
== 桜 (cherry tree; blossom)   curated option cards: 女 机 杏   tags: jlpt-n1 grade-5 structure-unclassified
   curated 女: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ジョ ニョ ニョウ | kun おんな め
   curated 机: tags jlpt-n2 grade-6 structure-unclassified; in pools: N1 stack, All stack; on キ | kun つくえ
   curated 杏: tags jlpt-n1 grade-9 structure-unclassified; in pools: N1 stack, All stack; on - | kun あんず
   JMdict single-kanji entries: 1593710: cherry tree, cherry blossom, sakura -> さくら・サクラ
   unlisted readings attested for 桜: さ (KANJIDIC2 name reading)  ろう (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt さくら (key さくら)
       N1 stack: curated 女 机 杏 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 女 机 杏 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated 女 -> 2 outcomes; deficit 2: the fallback fills the open slots; 10 drawable wrong options (2 curated, 8 fallback)
       attested reading さ (KANJIDIC2 name reading) is offered by 小 早 然; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [桜 小] -> お こ さ ちいさい; [桜 早] -> さ はや はやい はやまる はやめる
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (3 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 10 of 10 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 10 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
ower closeness tier): unlisted reading つく (card text) is offered only by card(s) 付 就 点 着 突
       info (can be drawn): ら is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 等
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt え (key え)
       excluded keys: 9
       curated 木: き こ
       curated 本: もと
       curated 休: やすむ やすまる やすめる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 13 keys, 2: 421 keys, 1: 10 keys, 0: 404 keys
       tier 3 candidates (13): いえ うえ えだ えむ えり える かえ こえ ごえ すえ なえ ばえ まえ
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading いきおい (card text) is offered only by card(s) 勢
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading つく (card text) is offered only by card(s) 付 就 点 着 突
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading ら (KANJIDIC2 name reading) is offered only by card(s) 等
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 染 (dye; stain; infect; permeate)   curated option cards: 木 水 九
   metadata readings: on セン | kun そ.める そ.まる し.みる し.み
   unlisted readings attested for 染: しめる (card text)  そめ (KANJIDIC2 name reading)
   on prompt セン (key せん)
       excluded keys: 12
       curated 木: ぼく もく
       curated 水: すい
       curated 九: きゅう く
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 54 keys, 2: 196 keys
       tier 3 candidates (54): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せい せき せつ そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ... (+14 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 株 (share; stump; rooted plant)   curated option cards: 未 本 休
   metadata readings: on シュ | kun かぶ
   unlisted readings attested for 株: くい (card text)  くいぜ (card text)
   on: no reading prompts
   kun prompt かぶ (key かぶ)
       excluded keys: 5
       curated 未: いまだ まだ ひつじ
       curated 本: もと
       curated 休: やすむ やすまる やすめる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 70 keys, 2: 678 keys, 1: 10 keys, 0: 114 keys
       tier 3 candidates (70): あそぶ うかぶ うぶ えらぶ か かい かいこ かう かえす かえで かえる かお かかる かがみ かき かぎる かく かける かげ かこむ かさ かしら かす かず かせ かぜ かた かたい かたな かたる かつ かつぐ かつら かど かなう かなめ かね かねる かぶる かべ ... (+30 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1692 other kun-reading cards
       simulation: 7 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 桜 (cherry tree; blossom)   curated option cards: 女 机 杏
   metadata readings: on オウ ヨウ | kun さくら
   unlisted readings attested for 桜: さ (KANJIDIC2 name reading)  ろう (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt さくら (key さくら)
       excluded keys: 6
       curated 女: おんな め
       curated 机: つくえ
       curated 杏: あんず
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 59 keys, 2: 788 keys, 1: 1 keys, 0: 39 keys
       tier 4 candidates (1): さら
       tier 3 candidates (59): あぶら あら いくら いたずら うすら うら かしら かつら がら くじら くら さいわい さえる さか さかい さかえる さかさま さかずき さかな さが さがす さき さく さぐる さけ さけぶ さげる ささ ささえる さす さだめる さとる さびしい さま さます さむい さむらい さめ さめる さる ... (+19 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading さ (KANJIDIC2 name reading) is offered only by card(s) 小 早 然
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 17; expected pairs: 17; added link pairs: 17; total added links: 17; declared remark edits: 1; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze 6b5934e7): python -X utf8 kanji_remarks.py REPO ef2b1b9fc9c5d40def44c4c9734f62004958a4a2 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b143\kanji-remarks.json 施 旋 旗 既 旦 旨 暑 暦 朗 条 架 柄 染 株 桜
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
new cards: 15/15; modified existing cards: 0; declared remark edits applied: 0; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze 6b5934e7): python -X utf8 meta_scan.py REPO 施 旋 旗 既 旦 旨 暑 暦 朗 条 架 柄 染 株 桜
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 7
   架.md:34: 掛け 1207600/2148680 not listed part of 掛ける
   架.md:39: 懸け 1207600/2148680 not listed part of 懸ける
   架.md:39: 賭け 1590040 not listed part of 賭ける
   染.md:35: 染め 1854060 not listed part of 染める
   染.md:42: 染め 1854060 not listed part of 染め物
   染.md:42: 抜き 2009330 not listed part of 染み抜き
   株.md:25: 雌雄 1312940 not listed part of 雌雄異株
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9064, 'entries': 9080, 'retainedBytes': 51521371, 'inflatedBytes': 51880462, 'localZipBytes': 32279118, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze 6b5934e7: manifest.json: 9057 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version a8b2f0aa83b2c12d
manifest.json sha256 before B8D714874863C99A8AA1900FCA2927DF0510F02F1D52242BC2EACF8D3367740E, after B8D714874863C99A8AA1900FCA2927DF0510F02F1D52242BC2EACF8D3367740E; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 53.318s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
