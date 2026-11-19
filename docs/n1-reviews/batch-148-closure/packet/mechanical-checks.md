# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 18, words checked: 29
WARN  words/綱.md: Dictionary: line cites no JMdict entry id
WARN  words/緯度.md: Dictionary: line cites no JMdict entry id
WARN  words/威張る.md: Dictionary: line cites no JMdict entry id
0 error(s), 3 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 18, words checked: 29
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
絞 (strangle; wring; squeeze)  options: paper | end; finish | summer
    reading しぼ.る   (kun): wrong options from distractors 3/3 (rest filled from other cards)
継 (succeed to; continue; patch)  options: paper | rain | fish
    reading ケイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
綱 (thick rope; hawser; main outline)  options: paper | sea, ocean | summer
    reading つな     (kun): wrong options from distractors 3/3 (rest filled from other cards)
緊 (tense; tight; urgent)  options: paper | talk, speak | rain
    reading キン     (on): wrong options from distractors 3/3 (rest filled from other cards)
締 (tighten; fasten; conclude)  options: paper | shop | sea, ocean
    reading し.める   (kun): wrong options from distractors 3/3 (rest filled from other cards)
緩 (loosen; slack; lenient)  options: aid; assistance | drawing; painting | dog
    reading ゆる.い   (kun): wrong options from distractors 1/3 (rest filled from other cards)
緯 (latitude; weft; woof)  options: guard; defense | green | mountain
    reading イ      (on): wrong options from distractors 3/3 (rest filled from other cards)
縁 (edge; connection; fate)  options: green | shrink; contract | fish
    reading ふち     (kun): wrong options from distractors 3/3 (rest filled from other cards)
縄 (rope; cord)  options: paper | practice; refine | horse
    reading なわ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
縛 (bind; tie up; restrain)  options: specialize; exclusive | slender; fine; detailed | station
    reading しば.る   (kun): wrong options from distractors 2/3 (rest filled from other cards)
縦 (vertical; lengthwise; at will)  options: paper | end; finish | dog
    reading たて     (kun): wrong options from distractors 3/3 (rest filled from other cards)
織 (weave; fabric; organization)  options: river | fish | song, sing
    reading シキ     (on): wrong options from distractors 3/3 (rest filled from other cards)
繕 (mend; darn; repair)  options: paper | bird | rain
    reading ゼン     (on): wrong options from distractors 3/3 (rest filled from other cards)
繰 (reel; turn pages; repeat)  options: dog | rain | station
    reading く.る    (kun): wrong options from distractors 2/3 (rest filled from other cards)
罰 (punishment; penalty; divine retribution)  options: four | mountain | song, sing
    reading バツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
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
llback)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 22 of 22 drawable wrong options seen
   kun: no reading prompts
== 繰 (reel; turn pages; repeat)   curated option cards: 犬 雨 駅   tags: jlpt-n1 grade-8 structure-unclassified
   curated 犬: tags jlpt-n4 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ケン | kun いぬ いぬ-
   curated 雨: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ウ | kun あめ あま- -さめ
   curated 駅: tags jlpt-n4 grade-3 phonetic-compound starter; in pools: N1 stack, All stack, Starter practice session; on エキ | kun -
   JMdict single-kanji entries: none
   unlisted readings attested for 繰: くり (KANJIDIC2 name reading, card text)
   on: no reading prompts
   kun prompt く.る (key くる)
       N1 stack: curated 犬 雨 -> 3 outcomes; deficit 1: the fallback fills the open slots; 8 drawable wrong options (4 curated, 4 fallback)
       All stack: curated 犬 雨 -> 3 outcomes; deficit 1: the fallback fills the open slots; 8 drawable wrong options (4 curated, 4 fallback)
       Starter practice session: curated 犬 雨 -> 3 outcomes; deficit 1: the fallback fills the open slots; 5 drawable wrong options (4 curated, 1 fallback)
       attested reading くり (KANJIDIC2 name reading, card text) is offered by 栗; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [繰 栗] -> くり
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (1 holders tried)
       sampling N1 stack: 200 seeds, 8 of 8 drawable wrong options seen
       sampling All stack: 200 seeds, 8 of 8 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
== 罰 (punishment; penalty; divine retribution)   curated option cards: 四 山 歌   tags: jlpt-n1 grade-8 structure-unclassified
   curated 四: tags jlpt-n5 grade-1 number starter; in pools: N1 stack, All stack, Starter practice session; on シ | kun よ よ.つ よっ.つ よん
   curated 山: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on サン セン | kun やま
   curated 歌: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on カ | kun うた うた.う
   JMdict single-kanji entries: 1478050: (divine) punishment, curse, retribution -> ばち; 1478060: punishment, penalty -> ばつ
   unlisted readings attested for 罰: ばちがあたる (card text)
   on prompt バツ (key ばつ)
       N1 stack: curated 四 山 歌 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 四 山 歌 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated 四 山 -> 2 outcomes; deficit 1: the fallback fills the open slots; 12 drawable wrong options (3 curated, 9 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 12 of 12 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 9 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
もて すべて た たい たいら たえる たおす たか たかい たから たがい たがう たき たく たぐい たけ たしか たたむ ただし ただす たち たつ たてる たな たに たね たのむ たば たび たべる たま たまう たまご たみ ためす ためる たもつ たより ... (+6 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading はなつ (card text) is offered only by card(s) 放 発
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading ゆるす (card text) is offered only by card(s) 許
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading よし (card text) is offered only by card(s) 由
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 織 (weave; fabric; organization)   curated option cards: 川 魚 歌
   metadata readings: on ショク シキ | kun お.る お.り おり -おり -お.り
   unlisted readings attested for 織: こおり (KANJIDIC2 name reading)  こり (KANJIDIC2 name reading)  のり (KANJIDIC2 name reading)
   on prompt シキ (key しき)
       excluded keys: 11
       curated 川: せん
       curated 魚: ぎょ
       curated 歌: か
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 21 keys, 2: 229 keys
       tier 3 candidates (21): いき えき き げき し しち しつ しゃ しゃく しゅ しゅう しゅく しゅつ しゅん しょ しょう しん せき てき りき れき
       unlisted-reading check: none of the 3 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 繕 (mend; darn; repair)   curated option cards: 紙 鳥 雨
   metadata readings: on ゼン | kun つくろ.う
   unlisted readings attested for 繕: つくろい (card text)  づくろい (card text)
   on prompt ゼン (key ぜん)
       excluded keys: 7
       curated 紙: し
       curated 鳥: ちょう
       curated 雨: う
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 53 keys, 2: 199 keys
       tier 3 candidates (53): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん ぜい ぜつ そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ぶん ... (+13 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 繰 (reel; turn pages; repeat)   curated option cards: 犬 雨 駅
   metadata readings: on ソウ | kun く.る
   unlisted readings attested for 繰: くり (card text)
   on: no reading prompts
   kun prompt く.る (key くる)
       excluded keys: 4
       curated 犬: いぬ いぬ
       curated 雨: あめ あま さめ
       curated 駅: no usable kun reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 4 keys, 3: 207 keys, 2: 558 keys, 1: 44 keys, 0: 79 keys
       tier 4 candidates (4): くだる くばる くもる くれる
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading くり (card text) is offered only by card(s) 栗
       simulation: 8 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 罰 (punishment; penalty; divine retribution)   curated option cards: 四 山 歌
   metadata readings: on バツ バチ ハツ | kun ばっ.する
   unlisted readings attested for 罰: ばちがあたる (card text)
   on prompt バツ (key ばつ)
       excluded keys: 12
       curated 四: し
       curated 山: さん せん
       curated 歌: か
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 37 keys, 2: 214 keys
       tier 3 candidates (37): あつ いつ えつ かつ きつ くつ けつ げつ こつ さつ ざつ しつ しゅつ じつ じゅつ せつ ぜつ そつ たつ だつ つ てつ とつ ねつ ば ばい ばく ばん ひつ ふつ ぶつ べつ まつ みつ めつ りつ れつ
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 301 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 17; expected pairs: 17; added link pairs: 17; total added links: 17; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze 8408b3a5): python -X utf8 kanji_remarks.py REPO a0f8d72a8206c24a6fcb81e3a9efec4c94c89bd1 C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b148\kanji-remarks.json 絞 継 綱 緊 締 緩 緯 縁 縄 縛 縦 織 繕 繰 罰
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/修.md
OK remark-only edit: kanji/張.md
OK remark-only edit: kanji/慢.md
new cards: 15/15; modified existing cards: 3; declared remark edits applied: 3; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze 8408b3a5): python -X utf8 meta_scan.py REPO 絞 継 綱 緊 締 緩 緯 縁 縄 縛 縦 織 繕 繰 罰
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 32
   絞.md:38: 上げ 1352300 not listed part of 絞り上げる
   絞.md:38: 上げる 1352320 not listed part of 絞り上げる
   絞.md:38: 上げ 1352300 not listed part of 搾り上げる
   絞.md:38: 上げる 1352320 not listed part of 搾り上げる
   絞.md:40: 締め 1853450 not listed part of 締める
   綱.md:29: 哺乳 1565230 not listed part of 哺乳綱
   綱.md:42: 引き 2026830/2148430 not listed part of 綱引き
   緊.md:42: 締め 1853450 not listed part of 締める
   締.md:23: 締め 1853450 not listed part of 締める
   締.md:23: 締め 1853450 not listed part of 締め切り
   締.md:23: 切り 1383800 not listed part of 締め切り
   締.md:23: 締め 1853450 not listed part of 締め切る
   締.md:23: 切る 1384830 not listed part of 締め切る
   締.md:37: 引き 2026830/2148430 not listed part of 引き締め
   締.md:37: 締め 1853450 not listed part of 引き締め
   締.md:38: 締め 1853450 not listed part of 元締め
   緩.md:37: 緩め 1621550 not listed part of 緩める
   緩.md:55: 下剤 1185000 not listed part of 緩下剤
   縁.md:32: 眼鏡 1577670/2862467 not listed part of 眼鏡のふち
   縁.md:32: 川べ 1636650 not listed part of 川べり
   縁.md:43: 取る 1326980 not listed part of 縁取る
   縁.md:49: 取り 2451270/2762480 not listed part of 縁取り
   縄.md:42: 跳び 2248520 not listed part of 縄跳び
   縄.md:42: 自縛 1318540 not listed part of 自縄自縛
   縛.md:25: 自縛 1318540 not listed part of 自縄自縛
   縛.md:36: 縛め 2655690 not listed part of 縛める
   織.md:28: 時代 1316300 not listed part of 織豊時代
   繰.md:23: 返す 1512130 not listed part of 繰り返す
   繰.md:36: 出す 1338180 not listed part of 繰り出す
   罰.md:44: 当たり 1448780 not listed part of 罰当たり
   罰.md:44: 当たり 1448780 not listed part of バチ当たり
   罰.md:44: 当り 1448780 not listed part of 罰当り
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9214, 'entries': 9230, 'retainedBytes': 52173345, 'inflatedBytes': 52532436, 'localZipBytes': 32591081, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze 8408b3a5: manifest.json: 9207 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 3f5f0498ce47f5a9
manifest.json sha256 before 53814D60AD9149CF4C5A10EBE80FE61255BCF5D636205D76A751F1F7A47EDB51, after 53814D60AD9149CF4C5A10EBE80FE61255BCF5D636205D76A751F1F7A47EDB51; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 56.342s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
