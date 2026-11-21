# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 11, words checked: 12
WARN  words/潜る.md: Dictionary: line cites no JMdict entry id
0 error(s), 1 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 11, words checked: 12
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
丹 (red; sincerity)  options: three | company, shrine | journey, travel
    reading タン     (on): wrong options from distractors 3/3 (rest filled from other cards)
乙 (second rank; stylish)  options: box | egg; ovum | pigeon; dove
    reading オツ     (on): wrong options from distractors 2/3 (rest filled from other cards)
亜 (sub-; next in rank; Asia)  options: mother | many, much | matter, affair
    reading ア      (on): wrong options from distractors 3/3 (rest filled from other cards)
仁 (benevolence; humaneness)  options: yen, circle | ten thousand | front, before
    reading ジン     (on): wrong options from distractors 3/3 (rest filled from other cards)
仙 (hermit; immortal)  options: wheat; barley | dish; plate | cylinder; tube
    reading セン     (on): wrong options from distractors 3/3 (rest filled from other cards)
伎 (skill; performer)  options: ume; Japanese apricot | snake; serpent | charcoal; coal
    reading キ      (on): wrong options from distractors 3/3 (rest filled from other cards)
伏 (lie prostrate; lurk; yield)  options: thread; yarn | cupful counter | elephant; image; shape
    reading フク     (on): wrong options from distractors 3/3 (rest filled from other cards)
伐 (fell trees; attack)  options: silk | chicken | tin can; container
    reading バツ     (on): wrong options from distractors 1/3 (rest filled from other cards)
伯 (uncle or aunt; eldest; count (noble))  options: self, oneself | thing, object | every, each
    reading ハク     (on): wrong options from distractors 3/3 (rest filled from other cards)
伴 (accompany; companion)  options: salt | sheep | ink; inkstick
    reading ハン     (on): wrong options from distractors 2/3 (rest filled from other cards)
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
ed)
       attested reading えき (KANJIDIC2 name reading) is offered by 役 易 液 益 駅; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [伯 役] -> えき やく; [伯 易] -> い えき
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (5 holders tried)
       attested reading か (KANJIDIC2 name reading) is offered by 下 仮 何 価 個 加 化 和 (+18 more); it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [伯 下] -> か げ; [伯 仮] -> か
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (26 holders tried)
       attested reading き (KANJIDIC2 name reading) is offered by 企 伎 危 喜 器 基 奇 季 (+20 more); it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [伯 企] -> き; [伯 伎] -> き
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (28 holders tried)
       attested reading は (KANJIDIC2 name reading, --extra list) is offered by 波 派 破; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [伯 波] -> は; [伯 派] -> は
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (3 holders tried)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
   kun: no reading prompts
== 伴 (accompany; companion)   curated option cards: 塩 羊 墨   tags: jlpt-n1 grade-8 structure-unclassified
   curated 塩: tags jlpt-n2 grade-4 structure-unclassified; in pools: N1 stack, All stack; on エン | kun しお
   curated 羊: tags jlpt-n1 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ヨウ | kun -
   curated 墨: tags jlpt-n1 grade-8 structure-unclassified; in pools: N1 stack, All stack; on - | kun すみ
   JMdict single-kanji entries: 1233560: companion, follower, attendant -> とも
   unlisted readings attested for 伴: とも (KANJIDIC2 name reading, --extra list, JMdict 1233560)
   on prompt ハン (key はん)
       N1 stack: curated 塩 羊 -> 1 outcomes; deficit 1: the fallback fills the open slots; 57 drawable wrong options (2 curated, 55 fallback)
       All stack: curated 塩 羊 -> 1 outcomes; deficit 1: the fallback fills the open slots; 57 drawable wrong options (2 curated, 55 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 24 drawable wrong options (0 curated, 24 fallback)
       sampling N1 stack: 200 seeds, 51 of 57 drawable wrong options seen
       sampling All stack: 200 seeds, 51 of 57 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 24 of 24 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 10 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
st kana): 3: 48 keys, 2: 209 keys
       tier 3 candidates (48): あく いく おく かく がく きく きゃく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく じゅく そく ぞく たく ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふ ふう ふつ ふらん ふん ほく ぼく まく みゃく もく ... (+8 more)
       unlisted-reading check: none of the 4 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 伐 (fell trees; attack)   curated option cards: 絹 鶏 缶
   metadata readings: on バツ ハツ カ ボチ | kun き.る そむ.く う.つ
   unlisted readings attested for 伐: ほこる (--extra list)
   on prompt バツ (key ばつ)
       excluded keys: 18
       curated 絹: no usable on reading, slot filled from the fallback
       curated 鶏: no usable on reading, slot filled from the fallback
       curated 缶: かん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 38 keys, 2: 217 keys
       tier 3 candidates (38): あつ いつ えつ おつ かつ きつ くつ けつ げつ こつ さつ ざつ しつ しゅつ じつ じゅつ せつ ぜつ そつ たつ だつ つ てつ とつ ねつ ば ばい ばく ばん ひつ ふつ ぶつ べつ まつ みつ めつ りつ れつ
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 37 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 伯 (uncle or aunt; eldest; count (noble))   curated option cards: 自 物 毎
   metadata readings: on ハク | kun -
   unlisted readings attested for 伯: は (--extra list)  はたがしら (--extra list)  かしら (--extra list)  おさ (--extra list)  かみ (--extra list)  いき (KANJIDIC2 name reading)  えき (KANJIDIC2 name reading)  か (KANJIDIC2 name reading)  き (KANJIDIC2 name reading)  ひろ (KANJIDIC2 name reading)
   on prompt ハク (key はく)
       excluded keys: 4
       curated 自: じ し
       curated 物: ぶつ もつ
       curated 毎: まい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 48 keys, 2: 208 keys
       tier 3 candidates (48): あく いく おく かく がく きく きゃく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく じゅく そく ぞく たく ちく ちゃく ちょく とく どく にく は はい はち はっ はつ はん ひゃく ふく ほく ぼく まく みゃく もく ... (+8 more)
       HIT (can be drawn): unlisted reading は (--extra list) is offered by card(s) 波 派 破
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading いき (KANJIDIC2 name reading) is offered only by card(s) 域
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading えき (KANJIDIC2 name reading) is offered only by card(s) 役 易 液 益 駅
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading か (KANJIDIC2 name reading) is offered only by card(s) 下 仮 何 価 個 加 化 和 夏 家 暇 果 架 歌 河 火 科 突 花 荷 菓 華 課 貨 過 靴
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading き (KANJIDIC2 name reading) is offered only by card(s) 企 伎 危 喜 器 基 奇 季 寄 希 帰 幾 揮 期 机 棋 機 気 汽 祈 紀 肌 虫 規 記 貴 起 飢
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 伴 (accompany; companion)   curated option cards: 塩 羊 墨
   metadata readings: on ハン バン | kun ともな.う
   unlisted readings attested for 伴: とも (--extra list)
   on prompt ハン (key はん)
       excluded keys: 7
       curated 塩: えん
       curated 羊: よう
       curated 墨: no usable on reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 56 keys, 2: 200 keys
       tier 3 candidates (56): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん は はい はく はち はっ はつ ひん ... (+16 more)
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 41 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
1 problem(s)
```

## link plan verify (word articles)

```text
NEW ARTICLE: words/丹念.md declares 丹念; unlinked batch kanji: none
NEW ARTICLE: words/乙.md declares 乙; unlinked batch kanji: none
NEW ARTICLE: words/亜熱帯.md declares 亜熱帯; unlinked batch kanji: none
NEW ARTICLE: words/仁.md declares 仁; unlinked batch kanji: none
NEW ARTICLE: words/仙人.md declares 仙人; unlinked batch kanji: none
NEW ARTICLE: words/伐採.md declares 伐採; unlinked batch kanji: none
NEW ARTICLE: words/伯仲.md declares 伯仲; unlinked batch kanji: none
NEW ARTICLE: words/同伴.md declares 同伴; unlinked batch kanji: none
NEW ARTICLE: words/歌舞伎.md declares 歌舞伎; unlinked batch kanji: none
NEW ARTICLE: words/降伏.md declares 降伏; unlinked batch kanji: none
changed word files: 11; expected pairs: 1; added link pairs: 1; total added links: 1; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at c2 c6afa163): python -X utf8 kanji_remarks.py REPO 0638544c C:\Users\romanko\.copilot\session-state\60266d87-4e3d-4c12-86b1-ef1e81f912a4\files\b156\links\kanji-remarks.json 丹 乙 亜 仁 仙 伎 伏 伐 伯 伴
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/潜.md
new cards: 10/10; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at c2 c6afa163): python -X utf8 meta_scan.py REPO 丹 乙 亜 仁 仙 伎 伏 伐 伯 伴
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
乙.md:42: 乙種 1862630 not listed
亜.md:40: 亜麻 1149860 not listed
仁.md:41: 仁術 1369740 not listed
仙.md:40: 仙骨 1387150 not listed
仙.md:40: 酒仙 1329130 not listed
伯.md:33: 伯母さん 2261500 not listed
-- whole-run gaps: 6; part-of-run matches not listed: 4
   亜.md:23: 熱帯 1467930 not listed part of 亜熱帯
   伎.md:23: 歌舞 1778760 not listed part of 歌舞伎
   伏.md:32: 伏せ 2860802 not listed part of 伏せる
   伯.md:33: 母さん 1609470 not listed part of 伯母さん
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9750, 'entries': 9766, 'retainedBytes': 56571739, 'inflatedBytes': 57002981, 'localZipBytes': 36337450, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at c2 c6afa163: manifest.json: 9743 files incl. 501 images, 303 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version e550208aa4999076
manifest.json sha256 before 042DB25369803872AE0600208094DEE990F2A4CF8ECD4236807AB0D4852F4E25, after 042DB25369803872AE0600208094DEE990F2A4CF8ECD4236807AB0D4852F4E25; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 439 tests in 63.001s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
