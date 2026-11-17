# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 15, words checked: 32
WARN  words/巡る.md: Dictionary: line cites no JMdict entry id
WARN  words/怪我.md: no Dictionary: line
WARN  words/恵まれる.md: Dictionary: line cites no JMdict entry id
WARN  words/普及.md: Dictionary: line cites no JMdict entry id
WARN  words/模倣.md: Dictionary: line cites no JMdict entry id
WARN  words/草履.md: Dictionary: line cites no JMdict entry id
WARN  words/鷹揚.md: Dictionary: line cites no JMdict entry id
0 error(s), 7 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 15, words checked: 32
WARN  words/怪我.md: no Dictionary: line
0 error(s), 1 warning(s)
```

## quiz safety simulation

```text
ptions: inhale; suck in | handle; deal with | grade; school class
    reading キュウ    (on): wrong options from distractors 0/3 (rest filled from other cards)
    reading およ.ぼす  (kun): wrong options from distractors 2/3 (rest filled from other cards)
姿 (figure; appearance; posture)  options: next | resources; capital | entrust; committee
    reading シ      (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading すがた    (kun): wrong options from distractors 2/3 (rest filled from other cards)
履 (footwear; put on shoes; carry out)  options: restore; repeat | roof, shop | reason, logic
    reading リ      (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading は.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
巡 (go around; patrol; tour)  options: order; sequence | river | pure; genuine
    reading ジュン    (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading めぐ.る   (kun): wrong options from distractors 1/3 (rest filled from other cards)
弾 (bullet; play strings; bounce)  options: pull; draw | single; simple | step; level
    reading ダン     (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading ひ.く    (kun): wrong options from distractors 2/3 (rest filled from other cards)
    reading たま     (kun): wrong options from distractors 2/3 (rest filled from other cards)
彫 (carve; engrave; sculpt)  options: circumference; circuit | shadow; silhouette | dig; excavate
    reading チョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading ほ.る    (kun): wrong options from distractors 2/3 (rest filled from other cards)
恵 (blessing; favor; grace)  options: specialize; exclusive | think, feel | drawing; painting
    reading ケイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading エ      (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading めぐ.む   (kun): wrong options from distractors 2/3 (rest filled from other cards)
憶 (remember; recall; guess)  options: hundred million | meaning, intention | roof, shop
    reading オク     (on): wrong options from distractors 1/3 (rest filled from other cards)
我 (self; I; ego)  options: righteousness; duty; meaning | become | picture, brushstroke
    reading ガ      (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading われ     (kun): wrong options from distractors 2/3 (rest filled from other cards)
揚 (hoist; lift; deep-fry)  options: place, site | hot water | sunshine
    reading ヨウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading あ.げる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
救 (rescue; save; relief)  options: seek; request | ball; sphere | teach, instruct
    reading キュウ    (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading すく.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
暇 (free time; leisure; time off)  options: warm; warm up | reflect, project | song, sing
    reading カ      (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading ひま     (kun): wrong options from distractors 3/3 (rest filled from other cards)
模 (imitate; model; pattern)  options: dusk; livelihood | grave; tomb | horizontal
    reading モ      (on): wrong options from distractors 1/3 (rest filled from other cards)
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
stack: curated 求 球 教 -> 2 outcomes; deficit 1/2: the fallback fills the open slots; 41 drawable wrong options (2 curated, 39 fallback)
       All stack: curated 求 球 教 -> 2 outcomes; deficit 1/2: the fallback fills the open slots; 41 drawable wrong options (2 curated, 39 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 15 drawable wrong options (0 curated, 15 fallback)
   kun prompt すく.う (key すくう)
       N1 stack: curated 求 球 教 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 求 球 教 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 8 drawable wrong options (0 curated, 8 fallback)
== 暇 (free time; leisure; time off)   curated option cards: 暖 映 歌   tags: jlpt-n1 grade-8 structure-unclassified
   curated 暖: tags jlpt-n1 grade-6 structure-unclassified; in pools: N1 stack, All stack; on ダン | kun あたた.かい あたた.まる あたた.める
   curated 映: tags jlpt-n4 grade-6 structure-unclassified; in pools: N1 stack, All stack; on エイ | kun うつ.る うつ.す は.える -ば.え
   curated 歌: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on カ | kun うた うた.う
   JMdict single-kanji entries: 1577280: spare time, free time, leisure -> ひま・ヒマ; 2858986: [word usually written using kana alone] (spare) time, free time, leisure -> いとま
   unlisted readings attested for 暇: none
   on prompt カ (key か)
       N1 stack: curated 暖 映 歌 -> 1 outcomes; deficit 1: the fallback fills the open slots; 8 drawable wrong options (2 curated, 6 fallback)
       All stack: curated 暖 映 歌 -> 1 outcomes; deficit 1: the fallback fills the open slots; 8 drawable wrong options (2 curated, 6 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 80 drawable wrong options (0 curated, 80 fallback)
   kun prompt ひま (key ひま)
       N1 stack: curated 暖 映 歌 -> 24 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 9 drawable wrong options (9 curated, 0 fallback)
       All stack: curated 暖 映 歌 -> 24 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 9 drawable wrong options (9 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 11 drawable wrong options (0 curated, 11 fallback)
== 模 (imitate; model; pattern)   curated option cards: 暮 墓 横   tags: jlpt-n1 grade-6 structure-unclassified
   curated 暮: tags jlpt-n3 grade-6 structure-unclassified; in pools: N1 stack, All stack; on ボ | kun く.れる く.らす
   curated 墓: tags jlpt-n1 grade-5 structure-unclassified; in pools: N1 stack, All stack; on - | kun はか
   curated 横: tags jlpt-n3 grade-3 structure-unclassified; in pools: N1 stack, All stack; on オウ | kun よこ
   JMdict single-kanji entries: 1820800: wooden printing block -> かたぎ
   unlisted readings attested for 模: がみ (KANJIDIC2 name reading)  かたぎ (JMdict 1820800)
   on prompt モ (key も)
       N1 stack: curated 暮 横 -> 1 outcomes; deficit 2: the fallback fills the open slots; 4 drawable wrong options (1 curated, 3 fallback)
       All stack: curated 暮 横 -> 1 outcomes; deficit 2: the fallback fills the open slots; 4 drawable wrong options (1 curated, 3 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 3 drawable wrong options (0 curated, 3 fallback)
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 19 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
```

## reading options (tail; full file in evidence\audits)

```text
of the 1651 other kun-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 救 (rescue; save; relief)   curated option cards: 求 球 教
   metadata readings: on キュウ | kun すく.う
   unlisted readings attested for 救: none
   on prompt キュウ (key きゅう)
       excluded keys: 8
       curated 求: きゅう(skipped: excluded) ぐ
       curated 球: きゅう(skipped: excluded)
       curated 教: きょう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 39 keys, 2: 163 keys, 1: 2 keys, 0: 38 keys
       tier 4 candidates (1): きょう
       tier 3 candidates (39): おう きく きつ きゃく きょ きょく きん ぎょう くう ぐう こう ごう しゅう しょう じゅう じょう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 294 other on-reading cards
       simulation: 36 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt すく.う (key すくう)
       excluded keys: 8
       curated 求: もとめる
       curated 球: たま
       curated 教: おしえる おそわる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 2 keys, 3: 89 keys, 2: 721 keys, 1: 3 keys, 0: 33 keys
       tier 4 candidates (2): すう すまう
       tier 3 candidates (89): あう あきなう あじわう あたう あつかう あらう あらそう いう いわう うかがう うしなう うたう うたがう うやまう うらなう うるおう おう おおう おぎなう おこなう おもう おもなう かう かこう かたらう かなう かまう かよう きそう きらう くう こう さからう すえ すがた すぎ すぎる すくない すぐ すぐれる ... (+49 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1651 other kun-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 暇 (free time; leisure; time off)   curated option cards: 暖 映 歌
   metadata readings: on カ | kun ひま いとま
   unlisted readings attested for 暇: none
   on prompt カ (key か)
       excluded keys: 8
       curated 暖: だん
       curated 映: えい
       curated 歌: か(skipped: excluded)
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 6 keys, 2: 215 keys, 0: 29 keys
       tier 3 candidates (6): かい かく かっ かつ かん じか
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 294 other on-reading cards
       simulation: 7 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt ひま (key ひま)
       excluded keys: 8
       curated 暖: あたたかい あたたまる あたためる
       curated 映: うつる うつす はえる ばえ
       curated 歌: うた うたう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 37 keys, 2: 678 keys, 1: 3 keys, 0: 107 keys
       tier 3 candidates (37): あたま あま いま うま かま くま くるま さま しま たま つま なかま なま ひ ひえる ひかる ひがし ひき ひく ひくい ひたい ひだり ひつじ ひと ひとえ ひとり ひな ひのえ ひびく ひやす ひら ひらく ひる ひろい ひろう ま やま
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1651 other kun-reading cards
       simulation: 9 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 模 (imitate; model; pattern)   curated option cards: 暮 墓 横
   metadata readings: on モ ボ | kun -
   unlisted readings attested for 模: がみ (KANJIDIC2 name reading)
   on prompt モ (key も)
       excluded keys: 4
       curated 暮: ぼ(skipped: excluded)
       curated 墓: no usable on reading, slot filled from the fallback
       curated 横: おう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 3 keys, 2: 212 keys, 0: 29 keys
       tier 3 candidates (3): もく もつ もん
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 294 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify

```text
changed word files: 32; expected pairs: 32; added link pairs: 32; total added links: 32; declared remark edits: 0; problems: 0
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8823, 'entries': 8838, 'retainedBytes': 50497082, 'inflatedBytes': 50768660, 'localZipBytes': 31778190, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
manifest.json: 8816 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version c456ab459d7f2c57
```

## unit tests

```text
Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.
Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.
Exported approved packages only. Validate content, rebuild the manifest and check archive budgets before publishing.
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
