# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 15, words checked: 18
WARN  words/公衆.md: Dictionary: line cites no JMdict entry id
WARN  words/葬式.md: Dictionary: line cites no JMdict entry id
WARN  words/蓄える.md: Dictionary: line cites no JMdict entry id
WARN  words/街角.md: Dictionary: line cites no JMdict entry id
0 error(s), 4 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 15, words checked: 18
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
葬 (bury; funeral)  options: earth, soil | flower | Buddhist temple
    reading ソウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
蒔 (sow seeds)  options: blossom; bloom | wither; dry up | dig; excavate
    reading ま.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
蓄 (store up; amass)  options: use, employ | sell | borrow, rent
    reading たくわ.える (kun): wrong options from distractors 3/3 (rest filled from other cards)
薦 (recommend; mat)  options: talk, speak | write | teach, instruct
    reading セン     (on): wrong options from distractors 3/3 (rest filled from other cards)
虚 (empty; void; false)  options: full; satisfy | true, genuine | heavy; piled up
    reading キョ     (on): wrong options from distractors 3/3 (rest filled from other cards)
融 (melt; circulate)  options: water | snow | ice; freeze
    reading ユウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
衆 (the masses; multitude)  options: king | guest; customer | father
    reading シュウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
街 (street; town)  options: bridge | garden; yard | pond; reservoir
    reading まち     (kun): wrong options from distractors 3/3 (rest filled from other cards)
衝 (collide; thrust)  options: run | stop, halt | revolve; times
    reading ショウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
裁 (judge; cut out cloth)  options: thread; yarn | needle; pin | law; method
    reading サイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
裂 (tear apart; split)  options: sew; stitch | knit; compile | tatami; fold
    reading さ.く    (kun): wrong options from distractors 3/3 (rest filled from other cards)
裸 (naked; bare)  options: shoes | sash; zone | umbrella; parasol
    reading はだか    (kun): wrong options from distractors 3/3 (rest filled from other cards)
覆 (cover; overturn)  options: open; unfold | pick up; gather | throw
    reading おお.う   (kun): wrong options from distractors 3/3 (rest filled from other cards)
視 (look at; regard as)  options: hear, ask | say; words | sound
    reading シ      (on): wrong options from distractors 3/3 (rest filled from other cards)
覧 (look over; peruse)  options: write | song, sing | drawing; painting
    reading ラン     (on): wrong options from distractors 3/3 (rest filled from other cards)
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
d, 14 fallback)
       sampling N1 stack: 200 seeds, 9 of 9 drawable wrong options seen
       sampling All stack: 200 seeds, 9 of 9 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 14 of 14 drawable wrong options seen
== 視 (look at; regard as)   curated option cards: 聞 言 音   tags: jlpt-n1 grade-6 structure-unclassified
   curated 聞: tags jlpt-n5 grade-2 phonetic-compound starter; in pools: N1 stack, All stack, Starter practice session; on ブン モン | kun き.く き.こえる
   curated 言: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on ゲン ゴン | kun い.う こと
   curated 音: tags jlpt-n4 grade-1 structure-unclassified; in pools: N1 stack, All stack; on オン イン -ノン | kun おと ね
   JMdict single-kanji entries: 2257780: viewing as ..., seeing as ..., treating as ... -> し
   unlisted readings attested for 視: とも (KANJIDIC2 name reading)  み (KANJIDIC2 name reading)  しする (card text)
   on prompt シ (key し)
       N1 stack: curated 聞 言 音 -> 12 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       All stack: curated 聞 言 音 -> 12 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 7 drawable wrong options (7 curated, 0 fallback)
       Starter practice session: curated 聞 -> 2 outcomes; deficit 2: the fallback fills the open slots; 7 drawable wrong options (2 curated, 5 fallback)
       attested reading み (KANJIDIC2 name reading) is offered by 味 未 美 魅; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [視 味] -> み; [視 未] -> び み
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (4 holders tried)
       sampling N1 stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling All stack: 200 seeds, 7 of 7 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 7 of 7 drawable wrong options seen
   kun: no reading prompts
== 覧 (look over; peruse)   curated option cards: 書 歌 絵   tags: jlpt-n1 grade-6 structure-unclassified
   curated 書: tags jlpt-n5 grade-2 compound starter; in pools: N1 stack, All stack, Starter practice session; on ショ | kun か.く -が.き
   curated 歌: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on カ | kun うた うた.う
   curated 絵: tags jlpt-n3 grade-2 structure-unclassified; in pools: N1 stack, All stack; on カイ エ | kun -
   JMdict single-kanji entries: none
   unlisted readings attested for 覧: none
   on prompt ラン (key らん)
       N1 stack: curated 書 歌 絵 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 書 歌 絵 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated 書 -> 1 outcomes; deficit 2: the fallback fills the open slots; 25 drawable wrong options (1 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 25 of 25 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 4 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 1 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
d 編: あむ あみ
       curated 畳: たたむ たたみ かさなる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 68 keys, 2: 707 keys, 1: 11 keys, 0: 118 keys
       tier 3 candidates (68): あく あばく あるく いく うく うごく えがく おく かく かわく きく きずく くだく こく さ さえる さか さかい さかさ さかな さかる さが さがす さき さくら さぐる さけ さけぶ ささ さす さだか さち さま さます さむい さめ さめる さら さる さわぐ ... (+28 more)
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 1722 other kun-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 裸 (naked; bare)   curated option cards: 靴 帯 傘
   metadata readings: on ラ | kun はだか
   unlisted readings attested for 裸: none
   on: no reading prompts
   kun prompt はだか (key はだか)
       excluded keys: 6
       curated 靴: くつ
       curated 帯: おびる おび
       curated 傘: かさ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 76 keys, 2: 806 keys, 1: 2 keys, 0: 40 keys
       tier 4 candidates (1): はか
       tier 3 candidates (76): あか あきらか あたたか いかでか おか おだやか かろやか こまか さか さだか しか しずか すずやか たか たしか つか なか なごやか にわか はい はいる はえ はえる はかる はく はぐくむ はげしい はげむ はこ はこぶ はさむ はし はしばみ はしゃぐ はしら はしる はじめ はじめる はじる はす ... (+36 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1722 other kun-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 覆 (cover; overturn)   curated option cards: 開 拾 投
   metadata readings: on フク | kun おお.う くつがえ.す くつがえ.る
   unlisted readings attested for 覆: ふ (card text)  ふう (card text)  おいかぶさる (card text)
   on: no reading prompts
   kun prompt おお.う (key おおう)
       excluded keys: 18
       curated 開: ひらく ひらき びらき ひらける あく あける
       curated 拾: ひろう
       curated 投: なげる なげ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 5 keys, 3: 112 keys, 2: 764 keys, 1: 2 keys, 0: 40 keys
       tier 4 candidates (5): おう おぎなう おこなう おもう おもなう
       unlisted-reading check: none of the 3 unlisted readings is offered by any of the 1722 other kun-reading cards
       simulation: 9 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 視 (look at; regard as)   curated option cards: 聞 言 音
   metadata readings: on シ | kun み.る
   unlisted readings attested for 視: しする (card text)  とも (KANJIDIC2 name reading)  み (KANJIDIC2 name reading)
   on prompt シ (key し)
       excluded keys: 2
       curated 聞: ぶん もん
       curated 言: げん ごん
       curated 音: おん いん のん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 7 keys, 2: 217 keys, 1: 6 keys, 0: 25 keys
       tier 3 candidates (7): しき しち しつ しゃ しゅ しょ しん
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading み (KANJIDIC2 name reading) is offered only by card(s) 味 未 美 魅
       simulation: 7 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 覧 (look over; peruse)   curated option cards: 書 歌 絵
   metadata readings: on ラン | kun み.る
   unlisted readings attested for 覧: none
   on prompt ラン (key らん)
       excluded keys: 2
       curated 書: しょ
       curated 歌: か
       curated 絵: かい え
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 54 keys, 2: 200 keys
       tier 3 candidates (54): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ぶん ... (+14 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 302 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 18; expected pairs: 18; added link pairs: 18; total added links: 18; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze1 2dd9d46b): python -X utf8 kanji_remarks.py REPO c6dbb52e3d64b0af6213aa6ee17eb37db10b6c93 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b150\r2\kanji-remarks.json 葬 蒔 蓄 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
new cards: 15/15; modified existing cards: 0; declared remark edits applied: 0; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze1 2dd9d46b): python -X utf8 meta_scan.py REPO 葬 蒔 蓄 薦 虚 融 衆 街 衝 裁 裂 裸 覆 視 覧
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
蓄.md:40: 蓄え 1854350 not listed
薦.md:23: 敷物 1633930 not listed
裸.md:41: 難読 1461050 not listed
視.md:23: じっと見る 1005880 not listed
-- whole-run gaps: 4; part-of-run matches not listed: 37
   葬.md:23: 死者 1310870 not listed part of 死者をほうむる
   葬.md:23: その儀 1890110 not listed part of その儀式
   葬.md:23: 儀式 1224700 not listed part of その儀式
   蒔.md:23: 植物 1357300 not listed part of 植物を移しうえる
   蒔.md:51: 散らし 1303440 not listed part of 散らし落とす
   蒔.md:51: 落とす 1589260 not listed part of 散らし落とす
   蓄.md:23: 多く 1861770 not listed part of 多くのものを一所に集めておく
   蓄.md:23: 一所 1576120 not listed part of 多くのものを一所に集めておく
   蓄.md:23: 集め 2082280 not listed part of 多くのものを一所に集めておく
   蓄.md:23: 蓄え 1854350 not listed part of 蓄える
   蓄.md:41: 貯え 1854350 not listed part of 貯える
   蓄.md:48: 一所 1576120 not listed part of 一所に集めて
   蓄.md:48: 集め 2082280 not listed part of 一所に集めて
   薦.md:23: 選び 2785990 not listed part of 人を選びだす
   薦.md:23: 選びだす 1392150 not listed part of 人を選びだす
   薦.md:32: 薦め 1210900 not listed part of 薦める
   薦.md:32: 勧め 1210900 not listed part of 勧める
   薦.md:49: 敷物 1633930 not listed part of こも・敷物
   虚.md:23: 邪心 1634860 not listed part of 邪心をもたない
   虚.md:42: 虚無 1232810 not listed part of 虚無僧
   虚.md:48: 中身 1448900/1599430 not listed part of 中身がない
   融.md:23: 通じ 1854760 not listed part of とおる・通じる・流通する
   融.md:23: 通じる 1432880 not listed part of とおる・通じる・流通する
   融.md:23: 流通 1552440 not listed part of とおる・通じる・流通する
   融.md:23: 通す 1432900 not listed part of とおる・通じる・流通する
   衆.md:23: 多く 1861770 not listed part of 多くの人・たみ
   衆.md:48: 多い 1407460 not listed part of 数が多い
   裂.md:34: 古代 1265760 not listed part of 古代裂れ
   裂.md:34: 古代 1265760 not listed part of 古代裂
   裂.md:34: 古代 1265760 not listed part of 古代切
   覧.md:23: 広く 1951480 not listed part of 広くながめる
   覧.md:23: 展覧 1619690 not listed part of 展覧会
   覧.md:51: 全体 1395660 not listed part of 全体を視野に収めて眺める
   覧.md:51: 視野 1312140 not listed part of 全体を視野に収めて眺める
   覧.md:51: 収め 2060670 not listed part of 全体を視野に収めて眺める
   覧.md:51: 眺め 1610960 not listed part of 全体を視野に収めて眺める
   覧.md:51: 眺める 1428830 not listed part of 全体を視野に収めて眺める
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9586, 'entries': 9602, 'retainedBytes': 55947412, 'inflatedBytes': 56306708, 'localZipBytes': 36026148, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze1 2dd9d46b: manifest.json: 9579 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 5bd132e6d48cc437
manifest.json sha256 before DF405D06816D85A93BD43ABEEA69C74503CEED1B25998E3CFC825AD46CC5A184, after DF405D06816D85A93BD43ABEEA69C74503CEED1B25998E3CFC825AD46CC5A184; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 117.539s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
