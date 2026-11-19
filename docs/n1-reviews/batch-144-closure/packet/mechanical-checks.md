# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 19
WARN  words/戸棚.md: Dictionary: line cites no JMdict entry id
WARN  words/淡水.md: Dictionary: line cites no JMdict entry id
WARN  words/特殊.md: Dictionary: line cites no JMdict entry id
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 19
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
棋 (shogi; go; go stone)  options: imitate; model; pattern | horizontal | build; stance
    reading キ      (on): wrong options from distractors 3/3 (rest filled from other cards)
棚 (shelf; ledge; trellis)  options: ume; Japanese apricot | bright, clear | build; stance
    reading たな     (kun): wrong options from distractors 3/3 (rest filled from other cards)
検 (inspect; examine; check)  options: horizontal | plant; put in the ground | bridge
    reading ケン     (on): wrong options from distractors 3/3 (rest filled from other cards)
概 (outline; roughly; bearing)  options: already; previously | imitate; model; pattern | ume; Japanese apricot
    reading ガイ     (on): wrong options from distractors 2/3 (rest filled from other cards)
欄 (column; form field; railing)  options: gate; doorway | horizontal | imitate; model; pattern
    reading ラン     (on): wrong options from distractors 3/3 (rest filled from other cards)
歓 (delight; joyful welcome; cheer)  options: authority; rights | next | desire
    reading カン     (on): wrong options from distractors 3/3 (rest filled from other cards)
殊 (especially; special; particular)  options: remain; leftover | death | palace; lord
    reading シュ     (on): wrong options from distractors 3/3 (rest filled from other cards)
殻 (shell; husk; empty outer covering)  options: rest | book, origin | tree, wood
    reading から     (kun): wrong options from distractors 3/3 (rest filled from other cards)
汁 (juice; soup; sap)  options: dirty; defile | pond; reservoir | decide
    reading しる     (kun): wrong options from distractors 3/3 (rest filled from other cards)
沖 (open sea; offshore; rise high)  options: sink; subside | steam; vapor | govern; heal
    reading おき     (kun): wrong options from distractors 2/3 (rest filled from other cards)
泡 (bubble; foam; froth)  options: pond; reservoir | river; watercourse | stay overnight; anchor
    reading あわ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
泣 (cry; weep; sob)  options: stand; set up | pour, direct attention | stay overnight; anchor
    reading な.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
淡 (pale; faint; plain; unsalted)  options: converse; consult | stay overnight; anchor | govern; heal
    reading タン     (on): wrong options from distractors 2/3 (rest filled from other cards)
渇 (thirst; dry up; crave)  options: put up; display; publish | hot water | cross over
    reading かわ.く   (kun): wrong options from distractors 2/3 (rest filled from other cards)
渋 (astringent; sluggish; reluctant)  options: pond; reservoir | river; watercourse | govern; heal
    reading ジュウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
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
t-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on ジ チ | kun おさ.める おさ.まる なお.る なお.す
   JMdict single-kanji entries: none
   unlisted readings attested for 淡: うすい (card text)
   on prompt タン (key たん)
       N1 stack: curated 談 泊 治 -> 2 outcomes; deficit 1: the fallback fills the open slots; 58 drawable wrong options (3 curated, 55 fallback)
       All stack: curated 談 泊 治 -> 2 outcomes; deficit 1: the fallback fills the open slots; 58 drawable wrong options (3 curated, 55 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 24 drawable wrong options (0 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 51 of 58 drawable wrong options seen
       sampling All stack: 200 seeds, 51 of 58 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
   kun: no reading prompts
== 渇 (thirst; dry up; crave)   curated option cards: 掲 湯 渡   tags: jlpt-n1 grade-8 structure-unclassified
   curated 掲: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ケイ | kun -
   curated 湯: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on トウ | kun ゆ
   curated 渡: tags jlpt-n3 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ト | kun わた.る -わた.る わた.す
   JMdict single-kanji entries: 1955930: thirst -> かつ
   unlisted readings attested for 渇: むさぼる (card text)  かち (card text)  かっす (card text)  かっする (card text)
   on: no reading prompts
   kun prompt かわ.く (key かわく)
       N1 stack: curated 湯 渡 -> 2 outcomes; deficit 1: the fallback fills the open slots; 5 drawable wrong options (3 curated, 2 fallback)
       All stack: curated 湯 渡 -> 2 outcomes; deficit 1: the fallback fills the open slots; 5 drawable wrong options (3 curated, 2 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 9 drawable wrong options (0 curated, 9 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 9 of 9 drawable wrong options seen
== 渋 (astringent; sluggish; reluctant)   curated option cards: 池 河 治   tags: jlpt-n1 grade-8 structure-unclassified
   curated 池: tags jlpt-n2 grade-2 structure-unclassified; in pools: N1 stack, All stack; on チ | kun いけ
   curated 河: tags jlpt-n2 grade-5 structure-unclassified; in pools: N1 stack, All stack; on カ | kun かわ
   curated 治: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on ジ チ | kun おさ.める おさ.まる なお.る なお.す
   JMdict single-kanji entries: 1633440: kakishibu, astringent persimmon juice used as a dye or to treat wood, paper, etc. -> しぶ
   unlisted readings attested for 渋: none
   on prompt ジュウ (key じゅう)
       N1 stack: curated 池 河 治 -> 2 outcomes; deficit 0/1: the fallback fills the open slots; 4 drawable wrong options (3 curated, 1 fallback)
       All stack: curated 池 河 治 -> 2 outcomes; deficit 0/1: the fallback fills the open slots; 4 drawable wrong options (3 curated, 1 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 16 drawable wrong options (0 curated, 16 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 16 of 16 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 6 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
 あたい あたう あたま あたり あたる あだ あつい あてる あと あに あね あばく あびる あぶら あまい あまつ ... (+27 more)
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 1693 other kun-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 泣 (cry; weep; sob)   curated option cards: 立 注 泊
   metadata readings: on キュウ | kun な.く
   unlisted readings attested for 泣: none
   on: no reading prompts
   kun prompt な.く (key なく)
       excluded keys: 5
       curated 立: たつ たつ たち たてる たてる たて たて たて だて だてる
       curated 注: そそぐ さす つぐ
       curated 泊: とまる とめる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 73 keys, 2: 677 keys, 1: 9 keys, 0: 115 keys
       tier 3 candidates (73): あく あばく あるく いく うく うごく えがく おく かく かわく きく きずく こく さく しく しずく すく せく そむく たく だく つく つづく とく とどく な ない なえ なおす なおる なか なかば なかま ながい ながれ なぎ なげる なごむ なさけ なし ... (+33 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1693 other kun-reading cards
       simulation: 11 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 淡 (pale; faint; plain; unsalted)   curated option cards: 談 泊 治
   metadata readings: on タン | kun あわ.い
   unlisted readings attested for 淡: うすい (card text)
   on prompt タン (key たん)
       excluded keys: 3
       curated 談: だん(skipped: excluded)
       curated 泊: はく
       curated 治: じ ち
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 55 keys, 2: 195 keys
       tier 3 candidates (55): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん た たい たく たつ ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ... (+15 more)
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 41 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 渇 (thirst; dry up; crave)   curated option cards: 掲 湯 渡
   metadata readings: on カツ | kun かわ.く
   unlisted readings attested for 渇: むさぼる (card text)  かち (card text)  かっす (card text)  かっする (card text)
   on: no reading prompts
   kun prompt かわ.く (key かわく)
       excluded keys: 6
       curated 掲: no usable kun reading, slot filled from the fallback
       curated 湯: ゆ
       curated 渡: わたる わたる わたす
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 2 keys, 3: 113 keys, 2: 727 keys, 1: 1 keys, 0: 39 keys
       tier 4 candidates (2): かく かたむく
       tier 3 candidates (113): あく あばく あまねく あるく いく いただく うく うごく えがく おく おののく かい かいこ かう かえす かえで かえる かお かおり かかる かかわる かがみ かき かぎる かくれる かける かげ かこむ かさ かさなる かさねる かしこい かしら かす かせ かぜ かた かたい かたどる かたな ... (+73 more)
       unlisted-reading check: none of the 4 unlisted readings is offered by any of the 1693 other kun-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 渋 (astringent; sluggish; reluctant)   curated option cards: 池 河 治
   metadata readings: on ジュウ シュウ | kun しぶ しぶ.い しぶ.る
   unlisted readings attested for 渋: none
   on prompt ジュウ (key じゅう)
       excluded keys: 13
       curated 池: ち
       curated 河: か
       curated 治: じ ち
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 40 keys, 2: 164 keys, 1: 2 keys, 0: 39 keys
       tier 4 candidates (1): じょう
       tier 3 candidates (40): おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しょう じき じつ じゃ じゃく じゅつ じゅん じょ じん すう そう ぞう ちゅう ちょう つう とう どう にゅう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 18; expected pairs: 18; added link pairs: 18; total added links: 18; declared remark edits: 1; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze b073abd8): python -X utf8 kanji_remarks.py REPO 1d262eb60ff8bae674781ce2e7635e002542c36e C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b144\kanji-remarks.json 棋 棚 検 概 欄 歓 殊 殻 汁 沖 泡 泣 淡 渇 渋
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/討.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze b073abd8): python -X utf8 meta_scan.py REPO 棋 棚 検 概 欄 歓 殊 殻 汁 沖 泡 泣 淡 渇 渋
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 24
   棚.md:37: 大陸 1415150 not listed part of 大陸棚
   棚.md:37: 陸棚 1551120 not listed part of 大陸棚
   棚.md:37: 葡萄 1499230 not listed part of 葡萄棚
   検.md:30: 検察 1257910 not listed part of 検察庁
   検.md:41: 調べ 1429050 not listed part of 調べる
   検.md:43: 改め 2035080 not listed part of 改める
   検.md:43: 非違 1688890 not listed part of 検非違使
   欄.md:40: 摺り 1657910 not listed part of 手摺り
   歓.md:34: 合歓 1284640/1284650 not listed part of 合歓木
   殊.md:23: 殊な 2229800 not listed part of 特殊な
   殻.md:23: 閉じこもる 1508570 not listed part of 殻に閉じこもる
   殻.md:37: 抜け 2841555 not listed part of 抜け殻
   汁.md:23: 味噌 1527040 not listed part of 味噌汁
   沖.md:39: 積層 1953120 not listed part of 沖積層
   泡.md:36: 立つ 1597040 not listed part of 泡立つ
   泡.md:36: 水泡に帰す 2852906 not listed part of 水泡に帰する
   泡.md:36: 帰す 1221240/2410530 not listed part of 水泡に帰する
   泡.md:36: 帰する 2082270 not listed part of 水泡に帰する
   泣.md:36: 泣き 1229650 not listed part of 泣き声
   泣.md:36: 泣き 1229650 not listed part of 泣き出す
   泣.md:36: 出す 1338180 not listed part of 泣き出す
   泣.md:36: 泣き 1229650 not listed part of 泣き沈む
   泣.md:36: 沈む 1431670 not listed part of 泣き沈む
   淡.md:43: 水魚 2208290/2637480 not listed part of 淡水魚
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9094, 'entries': 9110, 'retainedBytes': 51640102, 'inflatedBytes': 51999193, 'localZipBytes': 32337756, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze b073abd8: manifest.json: 9087 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version df72cbbbd4bbfc04
manifest.json sha256 before 0F081767DCF543711C68796D0C2DB3280E3CA325C24DCFE1752CDC14FD2AD5FB, after 0F081767DCF543711C68796D0C2DB3280E3CA325C24DCFE1752CDC14FD2AD5FB; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 69.107s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
