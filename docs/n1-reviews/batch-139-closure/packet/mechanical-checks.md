# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 15, words checked: 20
WARN  words/宣伝.md: Dictionary: line cites no JMdict entry id
WARN  words/宴会.md: Dictionary: line cites no JMdict entry id
0 error(s), 2 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 15, words checked: 20
0 error(s), 0 warning(s)
```

## quiz safety simulation

```text
嫁 (bride; daughter-in-law; marry into)  options: liking; favorable | hinder; obstruct; interfere | surname; family name
    reading よめ     (kun): wrong options from distractors 2/3 (rest filled from other cards)
嬢 (young lady; daughter; unmarried woman)  options: recreation; amusement | strange; exquisite | begin, start
    reading ジョウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
宗 (religion; sect)  options: indicate | eaves; space | government official
    reading シュウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
宜 (suitable; proper; good)  options: moreover; also | group; assemble | investigate; inspect
    reading よろ.しく  (kun): wrong options from distractors 2/3 (rest filled from other cards)
宣 (proclaim; announce; declare)  options: fence; hedge | space; midair | room, chamber
    reading セン     (on): wrong options from distractors 2/3 (rest filled from other cards)
宴 (banquet; feast; party)  options: room, chamber | necessity; essentials | lodging
    reading エン     (on): wrong options from distractors 3/3 (rest filled from other cards)
寂 (lonely; quiet; desolate)  options: supervise; urge | lodging | room, chamber
    reading さび.しい  (kun): wrong options from distractors 2/3 (rest filled from other cards)
密 (secret; dense; close)  options: without fail | treasure; valuables | island
    reading ミツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
審 (examine; judge; trial)  options: turn in a series | space; midair | lodging
    reading シン     (on): wrong options from distractors 3/3 (rest filled from other cards)
尋 (inquire; search for; fathom)  options: Buddhist temple | revere; esteem | shoot; shine into
    reading たず.ねる  (kun): wrong options from distractors 3/3 (rest filled from other cards)
屈 (bend; yield; submit)  options: go out, exit | reach; deliver; notify | be present; dwell
    reading クツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
属 (belong; affiliated; genus)  options: layer; stratum | roof, shop | footwear; put on shoes; carry out
    reading ゾク     (on): wrong options from distractors 3/3 (rest filled from other cards)
岬 (cape; headland; promontory)  options: mountain | rice field | middle, inside
    reading みさき    (kun): wrong options from distractors 3/3 (rest filled from other cards)
峠 (mountain pass; peak; climax)  options: shore; riverbank | island | up, above
    reading とうげ    (kun): wrong options from distractors 3/3 (rest filled from other cards)
崩 (crumble; collapse; demolish)  options: rock; boulder | island | bright, clear
    reading くず.れる  (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading くず.す   (kun): wrong options from distractors 3/3 (rest filled from other cards)
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
JIDIC2 name reading, card text, JMdict 1297220) is offered by 先; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [岬 先] -> さき まず
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (1 holders tried)
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
== 峠 (mountain pass; peak; climax)   curated option cards: 岸 島 上   tags: jlpt-n1 grade-8 structure-unclassified
   curated 岸: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ガン | kun きし
   curated 島: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on トウ | kun しま
   curated 上: tags jlpt-n5 grade-1 indicative starter; in pools: N1 stack, All stack, Starter practice session; on ジョウ ショウ | kun うえ うわ- かみ あ.げる あ.がる のぼ.る
   JMdict single-kanji entries: 1454420: (mountain) pass, highest point on a mountain road, ridge -> とうげ
   unlisted readings attested for 峠: none
   on: no reading prompts
   kun prompt とうげ (key とうげ)
       N1 stack: curated 岸 島 上 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 8 drawable wrong options (8 curated, 0 fallback)
       All stack: curated 岸 島 上 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 8 drawable wrong options (8 curated, 0 fallback)
       Starter practice session: curated 上 -> 6 outcomes; deficit 2: the fallback fills the open slots; 10 drawable wrong options (6 curated, 4 fallback)
       sampling N1 stack: 200 seeds, 8 of 8 drawable wrong options seen
       sampling All stack: 200 seeds, 8 of 8 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 10 of 10 drawable wrong options seen
== 崩 (crumble; collapse; demolish)   curated option cards: 岩 島 明   tags: jlpt-n1 grade-8 structure-unclassified
   curated 岩: tags jlpt-n2 grade-2 structure-unclassified; in pools: N1 stack, All stack; on ガン | kun いわ
   curated 島: tags jlpt-n2 grade-3 structure-unclassified; in pools: N1 stack, All stack; on トウ | kun しま
   curated 明: tags jlpt-n4 grade-2 structure-unclassified; in pools: N1 stack, All stack; on メイ ミョウ ミン | kun あ.かり あか.るい あか.るむ あか.らむ あき.らか あ.ける -あ.け あ.く あ.くる あ.かす
   JMdict single-kanji entries: none
   unlisted readings attested for 崩: ほうじる (card text)  ほうずる (card text)
   on: no reading prompts
   kun prompt くず.れる (key くずれる)
       N1 stack: curated 岩 島 明 -> 10 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 12 drawable wrong options (12 curated, 0 fallback)
       All stack: curated 岩 島 明 -> 10 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 12 drawable wrong options (12 curated, 0 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 23 drawable wrong options (0 curated, 23 fallback)
       sampling N1 stack: 200 seeds, 12 of 12 drawable wrong options seen
       sampling All stack: 200 seeds, 12 of 12 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 23 of 23 drawable wrong options seen
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 11 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
 and same first and last kana): 3: 36 keys, 2: 213 keys
       tier 3 candidates (36): あつ いつ えつ かつ きつ く くう くん けつ げつ こつ さつ ざつ しつ しゅつ じつ じゅつ せつ ぜつ そつ たつ だつ つ てつ とつ ねつ はつ ばつ ひつ ふつ ぶつ べつ まつ みつ りつ れつ
       unlisted-reading check: none of the 9 unlisted readings is offered by any of the 297 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 属 (belong; affiliated; genus)   curated option cards: 層 屋 履
   metadata readings: on ゾク ショク | kun さかん つく やから
   unlisted readings attested for 属: しょくす (card text)  しょくする (card text)  ぞくす (card text)  ぞくする (card text)  さっか (KANJIDIC2 name reading)  つき (KANJIDIC2 name reading)
   on prompt ゾク (key ぞく)
       excluded keys: 18
       curated 層: そう
       curated 屋: おく
       curated 履: り
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 39 keys, 2: 207 keys
       tier 3 candidates (39): あく いく おく かく がく きく きゃく きょく ぎゃく ぎょく く こく さく しゃく しゅく じゃく ぞう ぞん たく ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふく ほく ぼく もく やく よく らく りく りゃく りょく ろく
       unlisted-reading check: none of the 6 unlisted readings is offered by any of the 297 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 岬 (cape; headland; promontory)   curated option cards: 山 田 中
   metadata readings: on コウ | kun みさき
   unlisted readings attested for 岬: さき (card text)
   on: no reading prompts
   kun prompt みさき (key みさき)
       excluded keys: 6
       curated 山: やま
       curated 田: た
       curated 中: なか うち あたる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 1 keys, 3: 54 keys, 2: 785 keys, 1: 2 keys, 0: 35 keys
       tier 4 candidates (1): みき
       tier 3 candidates (54): あき いき いたずき いただき おき おもむき かき がき くしき くすのき さかずき さき ざき しき すすき せき たき つき つばき とき なおき なき ぬき のき ひき ひらき まき みがく みぎ みじかい みず みずうみ みずから みずもり みせ みたまや みだれる みち みちびく みちる ... (+14 more)
       HIT (can be drawn): unlisted reading さき (card text) is offered by card(s) 先
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 峠 (mountain pass; peak; climax)   curated option cards: 岸 島 上
   metadata readings: on - | kun とうげ
   unlisted readings attested for 峠: none
   on: no reading prompts
   kun prompt とうげ (key とうげ)
       excluded keys: 4
       curated 岸: きし
       curated 島: しま
       curated 上: うえ うわ かみ あげる あがる のぼる
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 33 keys, 2: 804 keys, 1: 1 keys, 0: 36 keys
       tier 3 candidates (33): かげ とう とうとい とお とおい とおる とき とく とぐ とける とこ ところ とし とじる とつぐ ととのう とどける との とぶ とぼしい とぼす とまる とむ とめる とも ともしび ともに とよ とら とらえる とり とる なげ
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1674 other kun-reading cards
       simulation: 8 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 崩 (crumble; collapse; demolish)   curated option cards: 岩 島 明
   metadata readings: on ホウ | kun くず.れる -くず.れ くず.す
   unlisted readings attested for 崩: ほうじる (card text)  ほうずる (card text)
   on: no reading prompts
   kun prompt くず.れる (key くずれる)
       excluded keys: 13
       curated 岩: いわ
       curated 島: しま
       curated 明: あかり あかるい あかるむ あからむ あきらか あける あけ あく あくる あかす
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 11 keys, 3: 288 keys, 2: 300 keys, 1: 29 keys, 0: 259 keys
       tier 4 candidates (11): くだる くちびる くばる くみする くもる くらべる くるしめる くれる くわえる くわだてる くんずる
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 1674 other kun-reading cards
       simulation: 12 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
1 problem(s)
```

## link plan verify (word articles)

```text
changed word files: 20; expected pairs: 20; added link pairs: 20; total added links: 20; declared remark edits: 4; problems: 0
```

## kanji card edits (new cards and remark-only edits; evidence\audits\kanji_remarks.py)

```text
Command (at freeze a47efe9a): python -X utf8 kanji_remarks.py REPO d65a9931d4231bf56f76c2c2a975b8bdd75eb3cd kanji-remarks.json 嫁 嬢 宗 宜 宣 宴 寂 密 審 尋 屈 属 岬 峠 崩
Checks that kanji/ differs from the base only by the batch's new cards and by the declared old-to-new remark replacements in existing cards (n1_linkplan.py verify covers words/ only).
new cards: 15/15; modified existing cards: 0; declared remark edits applied: 0; problems: 0
```

## card Metadata entry ids (meta scan)

```text
Command (at freeze a47efe9a): python -X utf8 meta_scan.py REPO 嫁 嬢 宗 宜 宣 宴 寂 密 審 尋 屈 属 岬 峠 崩
Lists words named on each card whose JMdict entry id is missing from the card's Metadata line.
whole runs: none missing
-- whole-run gaps: 0; part-of-run matches not listed: 33
   嫁.md:36: 遅れ 1422020 not listed part of 嫁き遅れ
   嫁.md:36: 行き 1578790 not listed part of 行き遅れ
   嫁.md:36: 遅れ 1422020 not listed part of 行き遅れ
   嫁.md:41: 嫁す 2410610 not listed part of 嫁する
   嫁.md:41: 嫁ぎ 2846288 not listed part of 嫁ぎ先
   嬢.md:23: お嬢 2216480 not listed part of お嬢さん
   嬢.md:23: 嬢さん 2216510/2230740 not listed part of お嬢さん
   嬢.md:25: 受付 1588060 not listed part of 受付嬢
   嬢.md:46: 御嬢 2216480 not listed part of 御嬢さん
   嬢.md:46: 嬢さん 2216510/2230740 not listed part of 御嬢さん
   宜.md:49: 敷く 1497020 not listed part of 宜敷く
   宴.md:25: 張る 1427900/2250310 not listed part of 宴を張る
   宴.md:36: 花見 1194660 not listed part of 花見の宴
   宴.md:49: 披露 1483490 not listed part of 披露宴
   寂.md:54: 荒び 2842308 not listed part of 荒びれる
   審.md:56: 審美 1360430 not listed part of 審美的
   審.md:56: 美的 1486570 not listed part of 審美的
   尋.md:23: 尋ね 2835838 not listed part of 尋ねる
   尋.md:23: 訊ね 2835838 not listed part of 訊ねる
   尋.md:46: 尋ね 2835838 not listed part of 尋ね人
   屈.md:23: 屈す 2409930 not listed part of 屈する
   属.md:23: 属す 2410040/2410050 not listed part of 属する
   属.md:34: 嘱す 2410050 not listed part of 嘱する
   属.md:35: 雅楽 1197870 not listed part of 雅楽属
   峠.md:25: 向け 1277090 not listed part of 手向け
   峠.md:25: 祖神 2832403 not listed part of 道祖神
   峠.md:25: 病気 1490230/2839802 not listed part of 病気は今夜が峠だ
   峠.md:25: 今夜 1289520 not listed part of 病気は今夜が峠だ
   峠.md:35: 越え 2858626 not listed part of 峠越え
   峠.md:46: 越す 1175300 not listed part of 峠を越す
   峠.md:46: 越え 2858626 not listed part of 峠を越える
   峠.md:46: 越える 1593070 not listed part of 峠を越える
   崩.md:25: 瓦解 1209590 not listed part of 土崩瓦解
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8943, 'entries': 8958, 'retainedBytes': 50998003, 'inflatedBytes': 51269581, 'localZipBytes': 32020125, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze a47efe9a: manifest.json: 8936 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 2bb33333fe020021
manifest.json sha256 before 986B3E34CFE98A818A7E8329406C5D755CC1C9A0B534A85EC3C1953350973A89, after 986B3E34CFE98A818A7E8329406C5D755CC1C9A0B534A85EC3C1953350973A89; tracked tree after rebuild: clean
```

## unit tests

```text
----------------------------------------------------------------------
Ran 436 tests in 65.237s
OK
```

## Android JVM tests

```text
NOT RUN: the Android JVM content tests (RealContentTest, RareHanTest, KanjiReadingsTest) and the Kotlin reading-exposure cross-check need a JDK, which the continuation machine does not have. No Kotlin, native, device or phone result is claimed.
```
