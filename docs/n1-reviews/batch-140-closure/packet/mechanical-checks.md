# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 25
WARN  words/往復.md: Dictionary: line cites no JMdict entry id
WARN  words/従姉妹.md: Dictionary: line cites no JMdict entry id
WARN  words/直径.md: Dictionary: line cites no JMdict entry id
WARN  words/通帳.md: Dictionary: line cites no JMdict entry id
0 error(s), 4 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 25
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
嵐 (storm; tempest)  options: rock; boulder | shore; riverbank | crumble; collapse; demolish
    reading あらし    (kun): wrong options from distractors 3/3 (rest filled from other cards)
巣 (nest; hive; den)  options: fruit; fruition | single; simple | flourish; glory
    reading す      (kun): wrong options from distractors 3/3 (rest filled from other cards)
帳 (notebook; account book; register)  options: hat; headgear | width; breadth | sash; zone
    reading チョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
幕 (curtain; act of a play; shogunate)  options: grave; tomb | dusk; livelihood | recruit; solicit
    reading マク     (on): wrong options from distractors 2/3 (rest filled from other cards)
幣 (currency; Shinto offering)  options: middle, inside | within, inner | south
    reading ヘイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
序 (order; preface; beginning)  options: wide, spacious | government agency | deposit; entrust
    reading ジョ     (on): wrong options from distractors 3/3 (rest filled from other cards)
弁 (speech; discern; valve)  options: stand, machine counter | leave, elapse | calculate; reckon
    reading ベン     (on): wrong options from distractors 3/3 (rest filled from other cards)
往 (going; past)  options: reside, dwell | pour, direct attention | wait, await
    reading オウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
径 (diameter; path)  options: role; duty | he | suspicious; uncanny
    reading ケイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
徐 (slowly; gradually)  options: surplus | route; course | on foot
    reading ジョ     (on): wrong options from distractors 3/3 (rest filled from other cards)
従 (follow; obey; subordinate)  options: on foot | law; rhythm | wait, await
    reading したが.う  (kun): wrong options from distractors 2/3 (rest filled from other cards)
徴 (sign; indication; levy)  options: minute; faint | penetrate; be thorough | virtue; benevolence
    reading チョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
志 (will; aspiration; intention)  options: sell | voice | forget
    reading シ      (on): wrong options from distractors 3/3 (rest filled from other cards)
怠 (neglect; be lazy)  options: begin, start | govern; heal | thought; attention
    reading おこた.る  (kun): wrong options from distractors 2/3 (rest filled from other cards)
    reading なま.ける  (kun): wrong options from distractors 2/3 (rest filled from other cards)
恨 (resent; grudge)  options: limit | silver | pleasant; agreeable
    reading うら.む   (kun): wrong options from distractors 3/3 (rest filled from other cards)
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
f 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
   kun: no reading prompts
== 怠 (neglect; be lazy)   curated option cards: 始 治 念   tags: jlpt-n1 grade-8 structure-unclassified
   curated 始: tags jlpt-n4 grade-3 structure-unclassified; in pools: N1 stack, All stack; on シ | kun はじ.める -はじ.める はじ.まる
   curated 治: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on ジ チ | kun おさ.める おさ.まる なお.る なお.す
   curated 念: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on ネン | kun -
   JMdict single-kanji entries: none
   unlisted readings attested for 怠: だるい (card text)  たるい (card text)
   on: no reading prompts
   kun prompt おこた.る (key おこたる)
       N1 stack: curated 始 治 -> 8 outcomes; deficit 1: the fallback fills the open slots; 26 drawable wrong options (6 curated, 20 fallback)
       All stack: curated 始 治 -> 8 outcomes; deficit 1: the fallback fills the open slots; 26 drawable wrong options (6 curated, 20 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 26 drawable wrong options (0 curated, 26 fallback)
       sampling N1 stack: 200 seeds, 26 of 26 drawable wrong options seen
       sampling All stack: 200 seeds, 26 of 26 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 26 of 26 drawable wrong options seen
   kun prompt なま.ける (key なまける)
       N1 stack: curated 始 治 -> 8 outcomes; deficit 1: the fallback fills the open slots; 13 drawable wrong options (6 curated, 7 fallback)
       All stack: curated 始 治 -> 8 outcomes; deficit 1: the fallback fills the open slots; 13 drawable wrong options (6 curated, 7 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 24 drawable wrong options (0 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 13 of 13 drawable wrong options seen
       sampling All stack: 200 seeds, 13 of 13 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
== 恨 (resent; grudge)   curated option cards: 限 銀 快   tags: jlpt-n1 grade-8 structure-unclassified
   curated 限: tags jlpt-n3 grade-5 structure-unclassified; in pools: N1 stack, All stack; on ゲン | kun かぎ.る かぎ.り -かぎ.り
   curated 銀: tags jlpt-n4 grade-3 phonetic-compound starter; in pools: N1 stack, All stack, Starter practice session; on ギン | kun しろがね
   curated 快: tags jlpt-n2 grade-5 structure-unclassified; in pools: N1 stack, All stack; on カイ | kun こころよ.い
   JMdict single-kanji entries: none
   unlisted readings attested for 恨: none
   on: no reading prompts
   kun prompt うら.む (key うらむ)
       N1 stack: curated 限 銀 快 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 限 銀 快 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated 銀 -> 1 outcomes; deficit 2: the fallback fills the open slots; 15 drawable wrong options (1 curated, 14 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 15 of 15 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 4 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
nd same first and last kana): 4: 1 keys, 3: 38 keys, 2: 168 keys, 1: 1 keys, 0: 38 keys
       tier 4 candidates (1): ちゅう
       tier 3 candidates (38): おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しゅう しょう じゅう すう そう ぞう ちく ちゃ ちゃく ちょく ちん つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 4 unlisted readings is offered by any of the 298 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 志 (will; aspiration; intention)   curated option cards: 売 声 忘
   metadata readings: on シ | kun シリング こころざ.す こころざし
   unlisted readings attested for 志: しるす (card text)  さかん (card text)  しっぽく (card text)  じん (KANJIDIC2 name reading)  べ (KANJIDIC2 name reading)  べし (KANJIDIC2 name reading)  ゆき (KANJIDIC2 name reading)
   on prompt シ (key し)
       excluded keys: 22
       curated 売: ばい
       curated 声: せい しょう
       curated 忘: ぼう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 7 keys, 2: 215 keys, 1: 6 keys, 0: 23 keys
       tier 3 candidates (7): しき しち しつ しゃ しゅ しょ しん
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading じん (KANJIDIC2 name reading) is offered only by card(s) 人 沈 神 臣
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 怠 (neglect; be lazy)   curated option cards: 始 治 念
   metadata readings: on タイ | kun おこた.る なま.ける
   unlisted readings attested for 怠: だるい (card text)  たるい (card text)
   on: no reading prompts
   kun prompt おこた.る (key おこたる)
       excluded keys: 12
       curated 始: はじめる はじめる はじまる
       curated 治: おさめる おさまる なおる なおす
       curated 念: no usable kun reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 21 keys, 3: 289 keys, 2: 294 keys, 1: 21 keys, 0: 265 keys
       tier 4 candidates (21): おいる おえる おきる おくまる おくる おくれる おこる おさえる おさめる おしえる おじる おそれる おちる おとずれる おとる おどる おびる おぼえる おりる おれる おわる
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1678 other kun-reading cards
       simulation: 25 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt なま.ける (key なまける)
       excluded keys: 12
       curated 始: はじめる はじめる はじまる
       curated 治: おさめる おさまる なおる なおす
       curated 念: no usable kun reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 8 keys, 3: 293 keys, 2: 304 keys, 1: 24 keys, 0: 262 keys
       tier 4 candidates (8): なおる ながらえる ながれる なげる なぞらえる なまる ならべる なれる
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1678 other kun-reading cards
       simulation: 13 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 恨 (resent; grudge)   curated option cards: 限 銀 快
   metadata readings: on コン | kun うら.む うら.めしい
   unlisted readings attested for 恨: none
   on: no reading prompts
   kun prompt うら.む (key うらむ)
       excluded keys: 7
       curated 限: かぎる かぎり かぎり
       curated 銀: しろがね
       curated 快: こころよい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 93 keys, 2: 749 keys, 1: 2 keys, 0: 35 keys
       tier 4 candidates (1): うむ
       tier 3 candidates (93): あからむ あかるむ あむ あやしむ あやぶむ あゆむ いさむ いそしむ いたむ いとなむ いなむ うい うえ うえる うお うかがう うがい うく うける うごく うし うしなう うしろ うじ うすい うた うたう うたがう うたた うち うつ うつす うつつ うつる うてな うで うね うばう うま うまい ... (+53 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1678 other kun-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 23; expected pairs: 23; added link pairs: 23; total added links: 23; declared remark edits: 2; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze 28831314): python -X utf8 kanji_remarks.py REPO f37cd97f43e8e2b2792cbe3d89e728c76e453646 kanji-remarks.json 嵐 巣 帳 幕 幣 序 弁 往 径 徐 従 徴 志 怠 恨
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/慢.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze 28831314): python -X utf8 meta_scan.py REPO 嵐 巣 帳 幕 幣 序 弁 往 径 徐 従 徴 志 怠 恨
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 24
   巣.md:43: 食う 1592100 not listed part of 巣食う
   巣.md:43: 喰う 1592100 not listed part of 巣喰う
   巣.md:45: 立つ 1597040 not listed part of 巣立つ
   巣.md:56: 帰巣 2107200 not listed part of 帰巣性
   帳.md:25: 大福 1623450/2624430 not listed part of 大福帳
   幕.md:50: 切れ 1384840/2518850 not listed part of 幕切れ
   幣.md:42: 担ぎ 1865980 not listed part of 御幣担ぎ
   弁.md:32: 東北 1448160 not listed part of 東北弁
   弁.md:34: 安全 1153930 not listed part of 安全弁
   弁.md:50: 弁え 2516660 not listed part of 弁える
   弁.md:51: 分け 1502990 not listed part of 分ける
   弁.md:55: 辨え 2516660 not listed part of 辨える
   径.md:29: 直情 1431050 not listed part of 直情径行
   径.md:29: 径行 1831150 not listed part of 直情径行
   径.md:41: 書房 1344160 not listed part of 径書房
   径.md:42: 差し 2423450/2711180 not listed part of 差し渡し
   径.md:42: 渡し 1855000 not listed part of 差し渡し
   従.md:23: 従兄 1335280 not listed part of 従兄弟
   従.md:23: 兄弟 1249960/2870775 not listed part of 従兄弟
   従.md:23: 従姉 1335300 not listed part of 従姉妹
   従.md:23: 姉妹 1579490 not listed part of 従姉妹
   従.md:34: 三位 1579360 not listed part of 従三位
   従.md:65: 従業 1335240 not listed part of 従業員
   志.md:29: 三国 1300410/5744975 not listed part of 三国志
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8973, 'entries': 8988, 'retainedBytes': 51127854, 'inflatedBytes': 51399432, 'localZipBytes': 32082422, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze 28831314: manifest.json: 8966 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 602bba1215b4c1de
manifest.json sha256 before 690B5A2DAE28005BFE4FD27D95BC79EB9B7AD3E8B4043B409A73C01F2E540552, after 690B5A2DAE28005BFE4FD27D95BC79EB9B7AD3E8B4043B409A73C01F2E540552; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 436 tests in 97.159s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
