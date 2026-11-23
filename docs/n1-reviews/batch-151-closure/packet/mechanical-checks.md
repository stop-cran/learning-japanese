# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 25, words checked: 65
WARN  kanji/長.md: not in the N1 source index; source comparison skipped
WARN  kanji/長.md: no quizOnyomi
WARN  kanji/長.md: no quizKunyomi
WARN  kanji/長.md: no Metadata: line
WARN  words/民謡.md: Dictionary: line cites no JMdict entry id
WARN  words/看護婦.md: no Dictionary: line
WARN  words/誓う.md: Dictionary: line cites no JMdict entry id
WARN  words/平仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/延長.md: Dictionary: line cites no JMdict entry id
WARN  words/振り仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/校長.md: no Dictionary: line
WARN  words/特長.md: Dictionary: line cites no JMdict entry id
WARN  words/生長.md: Dictionary: line cites no JMdict entry id
WARN  words/縫う.md: Dictionary: line cites no JMdict entry id
WARN  words/長女.md: Dictionary: line cites no JMdict entry id
WARN  words/長所.md: Dictionary: line cites no JMdict entry id
WARN  words/長方形.md: Dictionary: line cites no JMdict entry id
WARN  words/長男.md: Dictionary: line cites no JMdict entry id
WARN  words/長短.md: Dictionary: line cites no JMdict entry id
0 error(s), 19 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 25, words checked: 65
WARN  kanji/長.md: not in the N1 source index; source comparison skipped
WARN  kanji/長.md: no quizOnyomi
WARN  kanji/長.md: no quizKunyomi
WARN  kanji/長.md: no Metadata: line
WARN  words/看護婦.md: no Dictionary: line
WARN  words/校長.md: no Dictionary: line
0 error(s), 6 warning(s)
```

## quiz safety simulation

```text
訴 (sue; appeal to)  options: welcome; greet | escape; flee | battle
    reading うった.える (kun): wrong options from distractors 3/3 (rest filled from other cards)
証 (evidence; proof)  options: crime; guilt | criminal punishment | loss; damage
    reading ショウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
詩 (poem; poetry)  options: drama; play | koto; zither | drawing; painting
    reading シ      (on): wrong options from distractors 2/3 (rest filled from other cards)
詳 (detailed; well-informed)  options: weak; frail | dark | coarse; rough; crude
    reading くわ.しい  (kun): wrong options from distractors 3/3 (rest filled from other cards)
誇 (pride; boast)  options: shame | anger | doubt; suspect
    reading ほこ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
誓 (vow; swear)  options: sever; refuse | break; destroy; demolish | steal
    reading ちか.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
誘 (invite; tempt)  options: attack; go on the offensive | dance | grip; grasp
    reading さそ.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
謙 (humble; modest)  options: strong | dirty; defile | anger
    reading ケン     (on): wrong options from distractors 3/3 (rest filled from other cards)
謡 (ballad; Noh chanting)  options: dance | flute; whistle | tea
    reading ヨウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
譲 (hand over; yield)  options: eat, food | go | come
    reading ゆず.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
護 (safeguard; protect)  options: steal | break; destroy; demolish | battle
    reading ゴ      (on): wrong options from distractors 2/3 (rest filled from other cards)
豆 (bean; pea)  options: tuber; yam | egg; ovum | salt
    reading まめ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
豪 (powerful; excelling)  options: weak; frail | quiet | dark
    reading ゴウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
貢 (tribute; contribute)  options: loss; damage | punishment; penalty; divine retribution | snatch; rob; deprive
    reading コウ     (on): wrong options from distractors 2/3 (rest filled from other cards)
貴 (precious; esteem)  options: dirty; defile | coarse; rough; crude | lightweight; slight
    reading キ      (on): wrong options from distractors 3/3 (rest filled from other cards)
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
 損 罰 奪   tags: jlpt-n1 grade-8 structure-unclassified
   curated 損: tags jlpt-n2 grade-5 structure-unclassified; in pools: N1 stack, All stack; on ソン | kun そこ.なう そこな.う -そこ.なう そこ.ねる -そこ.ねる
   curated 罰: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on バツ | kun -
   curated 奪: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun うば.う
   JMdict single-kanji entries: 2254120: [obsolete term] tribute -> こう
   unlisted readings attested for 貢: none
   on prompt コウ (key こう)
       N1 stack: curated 損 罰 -> 1 outcomes; deficit 1: the fallback fills the open slots; 41 drawable wrong options (2 curated, 39 fallback)
       All stack: curated 損 罰 -> 1 outcomes; deficit 1: the fallback fills the open slots; 41 drawable wrong options (2 curated, 39 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 18 drawable wrong options (0 curated, 18 fallback)
       sampling N1 stack: 200 seeds, 35 of 41 drawable wrong options seen
       sampling All stack: 200 seeds, 35 of 41 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 18 of 18 drawable wrong options seen
   kun: no reading prompts
== 貴 (precious; esteem)   curated option cards: 汚 粗 軽   tags: jlpt-n1 grade-6 structure-unclassified
   curated 汚: tags jlpt-n2 grade-8 structure-unclassified; in pools: N1 stack, All stack; on オ | kun けが.す けが.れる けが.らわしい よご.す よご.れる きたな.い
   curated 粗: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on ソ | kun あら.い
   curated 軽: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ケイ キョウ キン | kun かる.い かろ.やか かろ.んじる
   JMdict single-kanji entries: 2244100: [archaic] value, preciousness, nobility -> とうと・たっと; 2260030: [honorific or respectful (sonkeigo) language] your -> き; 2580450: [honorific or respectful (sonkeigo) language, archaic] lord, god, goddess -> むち
   unlisted readings attested for 貴: きよ (KANJIDIC2 name reading)  ぎ (KANJIDIC2 name reading)  たか (KANJIDIC2 name reading)  たかし (KANJIDIC2 name reading)  よし (KANJIDIC2 name reading)  たかい (--extra list)  あて (--extra list)  むち (--extra list, JMdict 2580450)  あてやか (--extra list)  とうと (JMdict 2244100)  たっと (JMdict 2244100)
   on prompt キ (key き)
       N1 stack: curated 汚 粗 軽 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 汚 粗 軽 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 5 drawable wrong options (0 curated, 5 fallback)
       attested reading ぎ (KANJIDIC2 name reading) is offered by 儀 技 疑 義 議; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [貴 儀] -> ぎ; [貴 技] -> ぎ
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (5 holders tried)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 3 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
ny of the 302 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 豆 (bean; pea)   curated option cards: 芋 卵 塩
   metadata readings: on トウ ズ | kun まめ まめ-
   unlisted readings attested for 豆: たかつき (--extra list)  ど (KANJIDIC2 name reading)  ま (KANJIDIC2 name reading)
   on: no reading prompts
   kun prompt まめ (key まめ)
       excluded keys: 4
       curated 芋: いも
       curated 卵: たまご
       curated 塩: しお
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 54 keys, 2: 731 keys, 1: 3 keys, 0: 127 keys
       tier 3 candidates (54): あめ うめ かなめ かめ ききめ ぎめ こめ つめ づとめ どめ ななめ はじめ ま まいる まう まえ まかす まがる まく まける まこと まご まさ まさに まさる まして まじる ます まず また まだ まち まつ まつる まと まど まな まなぶ まねく まもる ... (+14 more)
       info (can be drawn): ま is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 目 真 間 馬
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 豪 (powerful; excelling)   curated option cards: 弱 静 暗
   metadata readings: on ゴウ | kun えら.い
   unlisted readings attested for 豪: つよい (--extra list)  えら (--extra list)  ご (KANJIDIC2 name reading)  すぐる (KANJIDIC2 name reading)  たけ (KANJIDIC2 name reading)  たけし (KANJIDIC2 name reading)  ひで (KANJIDIC2 name reading)  まさる (KANJIDIC2 name reading)
   on prompt ゴウ (key ごう)
       excluded keys: 3
       curated 弱: じゃく
       curated 静: せい じょう
       curated 暗: あん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 38 keys, 2: 216 keys
       tier 3 candidates (38): う おう きゅう きょう ぎゅう ぎょう くう ぐう ご ごく ごん しゅう しょう じゅう じょう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       info (can be drawn): ご is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 互 五 午 娯 後 御 悟 期 碁 語 誤 護 降
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 貢 (tribute; contribute)   curated option cards: 損 罰 奪
   metadata readings: on コウ ク | kun みつ.ぐ
   unlisted readings attested for 貢: none
   on prompt コウ (key こう)
       excluded keys: 7
       curated 損: そん
       curated 罰: ばつ
       curated 奪: no usable on reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 39 keys, 2: 212 keys
       tier 3 candidates (39): う おう きゅう きょう ぎゅう ぎょう くう ぐう こ こく こつ こん しゅう しょう じゅう じょう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 302 other on-reading cards
       simulation: 31 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 貴 (precious; esteem)   curated option cards: 汚 粗 軽
   metadata readings: on キ | kun たっと.い とうと.い たっと.ぶ とうと.ぶ
   unlisted readings attested for 貴: たかい (--extra list)  あて (--extra list)  むち (--extra list)  あてやか (--extra list)  きよ (KANJIDIC2 name reading)  ぎ (KANJIDIC2 name reading)  たか (KANJIDIC2 name reading)  たかし (KANJIDIC2 name reading)  よし (KANJIDIC2 name reading)
   on prompt キ (key き)
       excluded keys: 25
       curated 汚: お
       curated 粗: そ
       curated 軽: けい きょう きん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 13 keys, 2: 213 keys, 1: 3 keys, 0: 28 keys
       tier 3 candidates (13): いき えき きく きつ きょ きん げき しき じき せき てき りき れき
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading ぎ (KANJIDIC2 name reading) is offered only by card(s) 儀 技 疑 義 議
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 19; expected pairs: 19; added link pairs: 19; total added links: 19; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze b624890f): python -X utf8 kanji_remarks.py REPO b9f0e3403cf692850df678db3a3fd7544c3e0323 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b151\links\kanji-remarks.json 訴 証 詩 詳 誇 誓 誘 謙 謡 譲 護 豆 豪 貢 貴
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/仮.md
OK remark-only edit: kanji/憩.md
OK remark-only edit: kanji/推.md
OK remark-only edit: kanji/熟.md
OK remark-only edit: kanji/献.md
OK remark-only edit: kanji/級.md
OK remark-only edit: kanji/縫.md
OK remark-only edit: kanji/義.md
OK remark-only edit: kanji/長.md
OK remark-only edit: kanji/養.md
new cards: 15/15; modified existing cards: 10; declared remark edits applied: 10; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze b624890f): python -X utf8 meta_scan.py REPO 訴 証 詩 詳 誇 誓 誘 謙 謡 譲 護 豆 豪 貢 貴
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 61
   訴.md:23: 求め 1229340 not listed part of さばきを求めて申し出る
   訴.md:23: 申し 2607720 not listed part of さばきを求めて申し出る
   訴.md:23: 申し出 1362920 not listed part of さばきを求めて申し出る
   訴.md:23: 出る 1338240 not listed part of さばきを求めて申し出る
   訴.md:23: 同情 1452720 not listed part of 同情を求める
   訴.md:23: 求め 1229340 not listed part of 同情を求める
   訴.md:44: 不満 1494970 not listed part of 不満・苦痛などを告げ知らせる
   訴.md:44: 苦痛 1244560 not listed part of 不満・苦痛などを告げ知らせる
   訴.md:44: 知らせ 1420400 not listed part of 不満・苦痛などを告げ知らせる
   訴.md:44: 知らせる 1420410 not listed part of 不満・苦痛などを告げ知らせる
   訴.md:47: 求め 1229340 not listed part of 求める
   訴.md:47: 求め 1229340 not listed part of さばきを求めて
   訴.md:50: 申し 2607720 not listed part of 申し出る
   訴.md:50: 申し出 1362920 not listed part of 申し出る
   訴.md:50: 出る 1338240 not listed part of 申し出る
   訴.md:50: 裁き 1295920 not listed part of 裁きを求めるため上に申し出る
   訴.md:50: 求め 1229340 not listed part of 裁きを求めるため上に申し出る
   訴.md:50: 申し 2607720 not listed part of 裁きを求めるため上に申し出る
   訴.md:50: 申し出 1362920 not listed part of 裁きを求めるため上に申し出る
   訴.md:50: 出る 1338240 not listed part of 裁きを求めるため上に申し出る
   誇.md:23: 大げさ 1588890 not listed part of 大げさに言う
   誇.md:23: 言う 1587040 not listed part of 大げさに言う
   誇.md:46: 勝ち 1609560/2016470 not listed part of 勝ち誇る
   譲.md:40: 譲り 2766700 not listed part of 親譲り
   護.md:23: 看護 1213810 not listed part of 看護婦
   護.md:23: 看護 1213810 not listed part of 看護師
   豆.md:23: マメ科 2065850 not listed part of マメ科の植物の総称
   豆.md:23: 植物 1357300 not listed part of マメ科の植物の総称
   豆.md:23: 物の 2272520 not listed part of マメ科の植物の総称
   豆.md:23: 総称 1401620 not listed part of マメ科の植物の総称
   豆.md:23: 一つ 1160820 not listed part of 五穀の一つ
   豆.md:23: 電球 1443170 not listed part of 豆電球
   豆.md:44: 食物 1358620/1640430 not listed part of 食物を盛る脚のついた器
   豆.md:44: 盛る 1379730/1379740 not listed part of 食物を盛る脚のついた器
   豪.md:23: 力強い 1554940 not listed part of すぐれて力強い
   豪.md:23: 強い 1236070/2087680 not listed part of すぐれて力強い
   豪.md:23: 勢い 1375040 not listed part of 勢いが盛ん
   豪.md:23: 盛ん 1379750 not listed part of 勢いが盛ん
   豪.md:23: 能力 1470370/2721460 not listed part of 能力・財力などがぬきん出た人
   豪.md:23: 財力 1297030 not listed part of 能力・財力などがぬきん出た人
   豪.md:23: 並み 1599620 not listed part of 並み外れている
   豪.md:23: 並み外れ 1508420 not listed part of 並み外れている
   豪.md:23: 外れ 1203300 not listed part of 並み外れている
   豪.md:23: 大い 2427860 not listed part of 大いに
   豪.md:56: 勢い 1375040 not listed part of 勢いがさかんである
   貢.md:23: 朝廷 1428490 not listed part of 朝廷に地方の産物を献上する
   貢.md:23: 地方 1421450/2796690 not listed part of 朝廷に地方の産物を献上する
   貢.md:23: 産物 1303870 not listed part of 朝廷に地方の産物を献上する
   貢.md:23: 献上 1258440 not listed part of 朝廷に地方の産物を献上する
   貢.md:23: 上す 1352410 not listed part of 朝廷に地方の産物を献上する
   貢.md:41: 貢ぎ 1282390 not listed part of 貢ぎ物
   貢.md:50: 人材 1367760 not listed part of 人材を推薦する
   貴.md:23: 身分 1365810 not listed part of 身分や価値が高い
   貴.md:23: 価値 1189600 not listed part of 身分や価値が高い
   貴.md:23: 高い 1283190 not listed part of 身分や価値が高い
   貴.md:23: 大切 1414340/1643470 not listed part of 大切にする
   貴.md:23: 大切に 2018350 not listed part of 大切にする
   貴.md:23: 切に 1953140 not listed part of 大切にする
   貴.md:23: 相手 1401000 not listed part of 相手への敬意を表す語
   貴.md:23: 敬意 1250720 not listed part of 相手への敬意を表す語
   貴.md:23: 表す 1263490/2410100 not listed part of 相手への敬意を表す語
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9616, 'entries': 9632, 'retainedBytes': 56066721, 'inflatedBytes': 56426017, 'localZipBytes': 36082622, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze b624890f: manifest.json: 9609 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 6de07340290705e6
manifest.json sha256 before C0830896478271517515969615DA0D9C0B9DEE90D92D1BE0A1BC6FF0F832667F, after C0830896478271517515969615DA0D9C0B9DEE90D92D1BE0A1BC6FF0F832667F; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 136.773s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
