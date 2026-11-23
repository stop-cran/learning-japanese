# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 17, words checked: 25
WARN  words/井戸.md: Dictionary: line cites no JMdict entry id
WARN  words/但し.md: Dictionary: line cites no JMdict entry id
WARN  words/吐き気.md: Dictionary: line cites no JMdict entry id
WARN  words/風呂敷.md: Dictionary: line cites no JMdict entry id
0 error(s), 4 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 17, words checked: 25
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
丁 (city block; even number; fourth)  options: strike | third rank; third heavenly stem | completion; settling
    reading チョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading テイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
井 (well; well frame)  options: till; plough | mutual | two
    reading い      (kun): wrong options from distractors 3/3 (rest filled from other cards)
仰 (look up; revere)  options: welcome; greet | stamp; mark | relations between people
    reading コウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
但 (however; provided that)  options: daytime, midday | stretch; lengthen | other
    reading ただ.し   (kun): wrong options from distractors 3/3 (rest filled from other cards)
傑 (outstanding; excellence; hero)  options: dance | rest | body, form
    reading ケツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
傷 (wound; injury; damage)  options: hot water | sunshine | hoist; lift; deep-fry
    reading きず     (kun): wrong options from distractors 3/3 (rest filled from other cards)
僕 (I (male); servant)  options: work, occupation | hundred million | admirable; great
    reading ボク     (on): wrong options from distractors 3/3 (rest filled from other cards)
卸 (wholesale; grate)  options: honorific; govern | stamp; mark | noon
    reading おろ.す   (kun): wrong options from distractors 3/3 (rest filled from other cards)
司 (take charge; official; preside)  options: phrase; verse | same, equal | face toward
    reading シ      (on): wrong options from distractors 3/3 (rest filled from other cards)
吐 (spit out; vomit; breathe out)  options: shout; exclaim | inhale; suck in | company, shrine
    reading は.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
呂 (spine; backbone; bass range)  options: mouth | goods, refinement | conduct business; manage
    reading ロ      (on): wrong options from distractors 3/3 (rest filled from other cards)
哀 (sorrow; pity; pathos)  options: clothing; garment | reverse side; lining | bag; sack; pouch
    reading あわ.れ   (kun): wrong options from distractors 3/3 (rest filled from other cards)
哲 (philosophy; wise; sage)  options: fold | near | pray; wish
    reading テツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
唯 (only; solely; merely)  options: gather | advance | miscellaneous
    reading ユイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
善 (good; virtue; handle well)  options: sheep | wear; arrive | difference; gap
    reading ゼン     (on): wrong options from distractors 3/3 (rest filled from other cards)
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
ated 雑: tags jlpt-n3 grade-5 structure-unclassified; in pools: N1 stack, All stack; on ザツ ゾウ | kun まじ.える まじ.る
   JMdict single-kanji entries: 1538900: [word usually written using kana alone] ordinary, common, usual -> ただ・タダ
   unlisted readings attested for 唯: ゆ (KANJIDIC2 name reading)  たんだ (card text)
   on prompt ユイ (key ゆい)
       N1 stack: curated 集 進 雑 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 集 進 雑 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 13 drawable wrong options (0 curated, 13 fallback)
       attested reading ゆ (KANJIDIC2 name reading) is offered by 油 由 輸 遊; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [唯 油] -> ゆ ゆう; [唯 由] -> ゆ ゆう
       Starter practice session that also borrows one holder card (the pool grows by that card): drawable with 2 of 4 holders: 油 輸
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 13 of 13 drawable wrong options seen
   kun: no reading prompts
== 善 (good; virtue; handle well)   curated option cards: 羊 着 差   tags: jlpt-n1 grade-6 structure-unclassified
   curated 羊: tags jlpt-n1 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ヨウ | kun -
   curated 着: tags jlpt-n4 grade-3 structure-unclassified; in pools: N1 stack, All stack; on チャク ジャク | kun き.る き.せる つ.く つ.ける
   curated 差: tags jlpt-n3 grade-4 structure-unclassified; in pools: N1 stack, All stack; on サ | kun さ.す さ.し
   JMdict single-kanji entries: 1394250: good, goodness, right -> ぜん
   unlisted readings attested for 善: たる (KANJIDIC2 name reading)  よし (KANJIDIC2 name reading)  えい (card text)  よくする (card text)  えし (card text)
   on prompt ゼン (key ぜん)
       N1 stack: curated 羊 着 差 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 羊 着 差 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 21 drawable wrong options (0 curated, 21 fallback)
       attested reading えい (card text) is offered by 営 影 映 栄 永 泳 英 衛 (+1 more); it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [善 営] -> えい; [善 影] -> えい
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (9 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 21 of 21 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 8 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 1 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
eck: none of the 2 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 哀 (sorrow; pity; pathos)   curated option cards: 衣 裏 袋
   metadata readings: on アイ | kun あわ.れ あわ.れむ かな.しい
   unlisted readings attested for 哀: かなしむ (card text)  あはれ (card text)
   on: no reading prompts
   kun prompt あわ.れ (key あわれ)
       excluded keys: 7
       curated 衣: ころも きぬ ぎ
       curated 裏: うら
       curated 袋: ふくろ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 82 keys, 2: 740 keys, 1: 4 keys, 0: 32 keys
       tier 3 candidates (82): あいだ あいて あう あえる あお あか あかい あかがね あかし あかり あがる あき あきなう あく あげる あさ あさい あさる あざ あし あじ あずける あずさ あせ あぜ あそぶ あたい あたう あたえる あたたか あたま あたり あたる あだ あつい あつかう あつまる あてる あと あに ... (+42 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading かなしむ (card text) is offered only by card(s) 悲
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 哲 (philosophy; wise; sage)   curated option cards: 折 近 祈
   metadata readings: on テツ | kun さとい あきらか
   unlisted readings attested for 哲: あき (KANJIDIC2 name reading)  あきら (KANJIDIC2 name reading)  さと (KANJIDIC2 name reading)  さとし (KANJIDIC2 name reading)  さとる (KANJIDIC2 name reading)  てっ (KANJIDIC2 name reading)  てつん (KANJIDIC2 name reading)  のり (KANJIDIC2 name reading)  よし (KANJIDIC2 name reading)
   on prompt テツ (key てつ)
       excluded keys: 12
       curated 折: せつ しゃく
       curated 近: きん こん
       curated 祈: き
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 35 keys, 2: 213 keys
       tier 3 candidates (35): あつ いつ えつ かつ きつ くつ けつ げつ こつ さつ ざつ しつ しゅつ じつ じゅつ せつ ぜつ そつ たつ だつ つ てい てき てん とつ ねつ はつ ばつ ひつ ふつ ぶつ べつ まつ りつ れつ
       unlisted-reading check: none of the 9 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 唯 (only; solely; merely)   curated option cards: 集 進 雑
   metadata readings: on ユイ イ | kun ただ
   unlisted readings attested for 唯: たんだ (card text)  ゆ (KANJIDIC2 name reading)
   on prompt ユイ (key ゆい)
       excluded keys: 5
       curated 集: しゅう
       curated 進: しん
       curated 雑: ざつ ぞう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 30 keys, 2: 215 keys
       tier 3 candidates (30): あい えい かい がい けい げい さい ざい すい せい ぜい たい だい つい てい でい ない ねい はい ばい へい べい まい めい ゆ ゆう らい りい るい れい
       info (can be drawn): ゆ is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 油 由 輸 遊
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 善 (good; virtue; handle well)   curated option cards: 羊 着 差
   metadata readings: on ゼン | kun よ.い い.い よ.く よし.とする
   unlisted readings attested for 善: えい (card text)  よくする (card text)  えし (card text)  たる (KANJIDIC2 name reading)  よし (KANJIDIC2 name reading)
   on prompt ゼン (key ぜん)
       excluded keys: 17
       curated 羊: よう
       curated 着: ちゃく じゃく
       curated 差: さ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 53 keys, 2: 193 keys
       tier 3 candidates (53): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん ぜい ぜつ そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ぶん ... (+13 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading えい (card text) is offered only by card(s) 営 影 映 栄 永 泳 英 衛 鋭
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify

```text
changed word files: 21; expected pairs: 21; added link pairs: 21; total added links: 21; declared remark edits: 1; problems: 0
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8883, 'entries': 8898, 'retainedBytes': 50747305, 'inflatedBytes': 51018883, 'localZipBytes': 31898788, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze d3c7394d: manifest.json: 8876 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version f0580ba26b9adae2
manifest.json sha256 before 514CABC5FF26191ACB47A0FA7830A4D82F11E35CD3B358C966DD4901E3303A3D, after 514CABC5FF26191ACB47A0FA7830A4D82F11E35CD3B358C966DD4901E3303A3D; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 436 tests in 64.286s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
