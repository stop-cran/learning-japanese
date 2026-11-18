# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 16, words checked: 28
WARN  words/扇風機.md: Dictionary: line cites no JMdict entry id
WARN  words/威張る.md: Dictionary: line cites no JMdict entry id
0 error(s), 2 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 16, words checked: 28
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
悔 (regret; repent; mourn; frustration)  options: ume; Japanese apricot | every, each | accustomed
    reading く.やむ   (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading くや.しい  (kun): wrong options from distractors 3/3 (rest filled from other cards)
悟 (realize; enlightenment; perceive)  options: mouth | busy | arrogance; slackness
    reading ゴ      (on): wrong options from distractors 3/3 (rest filled from other cards)
惑 (bewilder; perplex; delude)  options: region; range | feeling; sensation | forget
    reading ワク     (on): wrong options from distractors 3/3 (rest filled from other cards)
惜 (pity; precious; begrudge)  options: hate; detest | nature; gender | accustomed
    reading お.しい   (kun): wrong options from distractors 3/3 (rest filled from other cards)
愉 (cheerful; joyful; delight)  options: busy | suspicious; uncanny | accustomed
    reading ユ      (on): wrong options from distractors 3/3 (rest filled from other cards)
慎 (careful; prudent; discreet)  options: accustomed | busy | nature; gender
    reading シン     (on): wrong options from distractors 3/3 (rest filled from other cards)
慮 (consider; concern; forethought)  options: tiger | drama; play | skin; bodily surface
    reading リョ     (on): wrong options from distractors 2/3 (rest filled from other cards)
慰 (console; comfort; solace)  options: forget | anger | seal; close
    reading なぐさ.める (kun): wrong options from distractors 2/3 (rest filled from other cards)
憧 (long for; yearn; admire)  options: hate; detest | suspicious; uncanny | arrogance; slackness
    reading あこが.れる (kun): wrong options from distractors 2/3 (rest filled from other cards)
憩 (rest; take a break; relax)  options: talk, speak | lively | nose; snout
    reading ケイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
懐 (bosom; nostalgic; become attached)  options: arrogance; slackness | hate; detest | busy
    reading なつ.かしい (kun): wrong options from distractors 2/3 (rest filled from other cards)
懸 (hang; suspend; stake)  options: lineage; system | favor; debt of gratitude | forget
    reading ケン     (on): wrong options from distractors 3/3 (rest filled from other cards)
扇 (fan; incite)  options: room; tassel; bunch | shoulder | employ; hire
    reading セン     (on): wrong options from distractors 3/3 (rest filled from other cards)
抽 (pull out; extract; abstract)  options: oil; grease | push | reach; deliver; notify
    reading チュウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
拡 (expand; enlarge; widen)  options: pay | worship; bow in respect | bottom; base
    reading カク     (on): wrong options from distractors 3/3 (rest filled from other cards)
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
d, 23 fallback)
       attested reading おう (KANJIDIC2 name reading) is offered by 凹 区 圧 央 奥 往 応 押 (+5 more); it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [扇 凹] -> おう; [扇 区] -> おう く こう
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (13 holders tried)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 23 of 23 drawable wrong options seen
   kun: no reading prompts
== 抽 (pull out; extract; abstract)   curated option cards: 油 押 届   tags: jlpt-n1 grade-8 structure-unclassified
   curated 油: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ユ ユウ | kun あぶら
   curated 押: tags jlpt-n3 grade-8 structure-unclassified; in pools: N1 stack, All stack; on オウ | kun お.す お.し- お.っ- お.さえる おさ.える
   curated 届: tags jlpt-n2 grade-6 structure-unclassified; in pools: N1 stack, All stack; on カイ | kun とど.ける -とど.け とど.く
   JMdict single-kanji entries: none
   unlisted readings attested for 抽: ひく (card text)  ぬく (card text)  ぬきんでる (card text)  ちゅうだい (card text)
   on prompt チュウ (key ちゅう)
       N1 stack: curated 油 押 届 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: curated 油 押 届 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 13 drawable wrong options (0 curated, 13 fallback)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 13 of 13 drawable wrong options seen
   kun: no reading prompts
== 拡 (expand; enlarge; widen)   curated option cards: 払 拝 底   tags: jlpt-n1 grade-6 structure-unclassified
   curated 払: tags jlpt-n3 grade-8 structure-unclassified; in pools: N1 stack, All stack; on フツ ヒツ ホツ | kun はら.う -はら.い -ばら.い
   curated 拝: tags jlpt-n2 grade-6 structure-unclassified; in pools: N1 stack, All stack; on ハイ | kun おが.む おろが.む
   curated 底: tags jlpt-n2 grade-4 structure-unclassified; in pools: N1 stack, All stack; on テイ | kun そこ
   JMdict single-kanji entries: none
   unlisted readings attested for 拡: none
   on prompt カク (key かく)
       N1 stack: curated 払 拝 底 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: curated 払 拝 底 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 16 drawable wrong options (0 curated, 16 fallback)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 16 of 16 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 5 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
 くわしい けがらわしい けわしい こいしい こころよい こまかい さいわい さびしい さむらい さわがしい したしい すくない すずしい すまない するどい ただしい たっとい たのしい たのもしい ちいさい ... (+28 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading かね (KANJIDIC2 name reading) is offered only by card(s) 金
       simulation: 9 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 懸 (hang; suspend; stake)   curated option cards: 系 恩 忘
   metadata readings: on ケン ケ | kun か.ける か.かる
   unlisted readings attested for 懸: へだたる (card text)  かかり (card text)  がけ (card text)
   on prompt ケン (key けん)
       excluded keys: 11
       curated 系: けい
       curated 恩: おん
       curated 忘: ぼう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 53 keys, 2: 197 keys
       tier 3 candidates (53): あん いん うん えん おん かん がん きん ぎん くん ぐん けい けつ こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ぶん ... (+13 more)
       unlisted-reading check: none of the 3 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 扇 (fan; incite)   curated option cards: 房 肩 雇
   metadata readings: on セン | kun おうぎ
   unlisted readings attested for 扇: あおぐ (card text)  おだてる (card text)  あおる (card text)  おう (KANJIDIC2 name reading)  おおぎ (KANJIDIC2 name reading)
   on prompt セン (key せん)
       excluded keys: 5
       curated 房: ぼう
       curated 肩: けん
       curated 雇: こ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 54 keys, 2: 196 keys
       tier 3 candidates (54): あん いん うん えん おん かん がん きん ぎん くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せい せき せつ そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん びん ふらん ふん ... (+14 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading おう (KANJIDIC2 name reading) is offered only by card(s) 凹 区 圧 央 奥 往 応 押 横 欧 王 鷹 黄
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 抽 (pull out; extract; abstract)   curated option cards: 油 押 届
   metadata readings: on チュウ | kun ひき-
   unlisted readings attested for 抽: ひく (card text)  ぬく (card text)  ぬきんでる (card text)  ちゅうだい (card text)
   on prompt チュウ (key ちゅう)
       excluded keys: 7
       curated 油: ゆ ゆう
       curated 押: おう
       curated 届: かい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 39 keys, 2: 169 keys, 1: 2 keys, 0: 39 keys
       tier 4 candidates (1): ちょう
       tier 3 candidates (39): おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しゅう しょう じょう すう そう ぞう ちく ちゃ ちゃく ちょ ちょく ちん つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 4 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 拡 (expand; enlarge; widen)   curated option cards: 払 拝 底
   metadata readings: on カク コウ | kun ひろ.がる ひろ.げる ひろ.める
   unlisted readings attested for 拡: none
   on prompt カク (key かく)
       excluded keys: 19
       curated 払: ふつ ひつ ほつ
       curated 拝: はい
       curated 底: てい
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 44 keys, 2: 203 keys
       tier 3 candidates (44): あく いく おく か かい かっ かつ かん きく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく そく ぞく たく ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふく ほく ぼく まく もく やく よく らく りく ... (+4 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 299 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 21; expected pairs: 21; added link pairs: 21; total added links: 21; declared remark edits: 0; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze a92d134a): python -X utf8 kanji_remarks.py REPO 466b7b283661febf8f93fa2d9675ea0a14767cde kanji-remarks.json 悔 悟 惑 惜 愉 慎 慮 慰 憧 憩 懐 懸 扇 抽 拡
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
OK remark-only edit: kanji/張.md
new cards: 15/15; modified existing cards: 1; declared remark edits applied: 1; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze a92d134a): python -X utf8 meta_scan.py REPO 悔 悟 惑 惜 愉 慎 慮 慰 憧 憩 懐 懸 扇 抽 拡
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 30
   悔.md:42: 悔やみ 1592370 not listed part of お悔やみ
   悔.md:51: 惜しい 1382280 not listed part of 口惜しい
   惜.md:27: 身命 1705900 not listed part of 不惜身命
   惜.md:39: 負け 1497960 not listed part of 負け惜しみ
   惜.md:49: 名残 1531530 not listed part of 名残惜しい
   惜.md:53: 懐かし 2133230 not listed part of 懐かしい
   愉.md:50: 慰め 1156880 not listed part of 慰める
   憧.md:51: 懐かし 2133230 not listed part of 懐かしむ
   懐.md:23: 懐かし 2133230 not listed part of 懐かしい
   懐.md:44: 懐かし 2133230 not listed part of 懐かしむ
   懐.md:64: 憧れ 1453800 not listed part of 憧れる
   懸.md:23: 一生 1576200 not listed part of 一生懸命
   懸.md:43: 懸け 1207600/2148680 not listed part of 命懸け
   懸.md:46: 一生 1576200 not listed part of 一生けんめい
   懸.md:46: 一生 1576200 not listed part of 一生けん命
   懸.md:46: 一所 1576120 not listed part of 一所懸命
   懸.md:46: 懸け 1207600/2148680 not listed part of 懸ける
   懸.md:46: 掛け 1207600/2148680 not listed part of 掛ける
   懸.md:48: 賭け 1590040 not listed part of 賭ける
   扇.md:27: 扇状 1953210 not listed part of 扇状地
   扇.md:57: 換気 1212780 not listed part of 換気扇
   抽.md:25: 抜き 2009330 not listed part of 抜きん出る
   抽.md:25: 出る 1338240 not listed part of 抜きん出る
   抽.md:34: 出し 1339160 not listed part of 抽き出し
   抽.md:34: 引き 2026830/2148430 not listed part of 引き出し
   抽.md:34: 出し 1339160 not listed part of 引き出し
   抽.md:36: 出し 1339160 not listed part of 抽出し
   拡.md:25: 拡声 2780220 not listed part of 拡声器
   拡.md:37: 広め 1483510/2858954 not listed part of 広める
   拡.md:37: 弘め 1483510 not listed part of 弘める
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 9003, 'entries': 9018, 'retainedBytes': 51265076, 'inflatedBytes': 51536654, 'localZipBytes': 32146266, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze a92d134a: manifest.json: 8996 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 742c010848bf0948
manifest.json sha256 before 760B92D959C8206FD959EE1ED121874B1280B2D77B8E66D9D8BC9A464D87F455, after 760B92D959C8206FD959EE1ED121874B1280B2D77B8E66D9D8BC9A464D87F455; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 436 tests in 72.450s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
