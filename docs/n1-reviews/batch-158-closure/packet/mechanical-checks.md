# Mechanical checks (automatic output, not a review verdict)

## Content validation

```text
Command (at 60d2cd5a): python tools\validate.py
0 error(s)
exit 0
```

## B158 batch audit

```text
Command (at 60d2cd5a): python tools\audit_n1_batch.py --batch 158
{
  "batch": "158",
  "baseCommit": "ad1694c1fe537a090c712065e77c480deb9edf4d",
  "draftKanji": 10,
  "newWords": 10,
  "changedReusedArticles": 10,
  "requiredReciprocalPairs": 10,
  "activatedBaselinePairs": 0,
  "readingDispositions": 30,
  "curatedOfferedKeys": 10,
  "sourceOnlyOfferedKeys": 0,
  "dictionaryFamilies": 73,
  "exactBaseRuntimePreservedOutsideRecordedChanges": true,
  "manifestFresh": true,
  "contentVersion": "f8022e4fa1e23aaa",
  "limits": "Mechanical draft audit, not lexical-allocation/naturalness verification, independent review, native/phone acceptance or publication."
}
exit 0
```

## Unit tests (tools suite)

```text
Ran 439 tests in 70.223s
OK
exit 0
```

## Manifest rebuild

```text
Command (at 60d2cd5a): python tools\build_manifest.py
manifest.json: 9813 files incl. 504 images, 305 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version f8022e4fa1e23aaa
manifest.json sha256 before 72B7BA0986B836ABBC6DB1BC485BFFE27BB6ADA209536A2F1C3BD46A83F75B85, after 72B7BA0986B836ABBC6DB1BC485BFFE27BB6ADA209536A2F1C3BD46A83F75B85; tracked tree after rebuild: clean
exit 0
```

## Content budget

```text
Command (at 60d2cd5a): python tools\check_content_budget.py
{'files': 9820, 'entries': 9836, 'retainedBytes': 56808374, 'inflatedBytes': 57244446, 'localZipBytes': 36496778, 'listeningTaskMediaBytes': 5893602}
exit 0
```

## Grammar vocabulary

```text
Command (at 60d2cd5a): python tools\grammar_vocabulary.py check
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
exit 0
```

## Whitespace (git diff --check)

```text
Command (at 60d2cd5a): git -c core.whitespace=cr-at-eol diff --check ad1694c1 60d2cd5a (whole range from the batch base, including any merged-in main commits)
exit 0
```

## N1 lint (the 4 errors are on reused files and are also reported at base ad1694c1)

```text
Command (at 60d2cd5a): python lean\n1_batch_tool.py lint --base ad1694c1
kanji checked: 19, words checked: 91
WARN  kanji/名.md: not in the N1 source index; source comparison skipped
WARN  kanji/名.md: no quizOnyomi
WARN  kanji/名.md: no quizKunyomi
WARN  kanji/名.md: no Metadata: line
WARN  kanji/師.md: not in the N1 source index; source comparison skipped
WARN  kanji/師.md: no quizOnyomi
WARN  kanji/師.md: no quizKunyomi
WARN  kanji/座.md: not in the N1 source index; source comparison skipped
WARN  kanji/座.md: no quizOnyomi
WARN  kanji/座.md: no quizKunyomi
WARN  kanji/章.md: not in the N1 source index; source comparison skipped
WARN  kanji/章.md: no quizOnyomi
WARN  kanji/章.md: no quizKunyomi
WARN  kanji/見.md: not in the N1 source index; source comparison skipped
WARN  kanji/見.md: no quizOnyomi
WARN  kanji/見.md: no quizKunyomi
WARN  kanji/見.md: no Metadata: line
WARN  kanji/観.md: not in the N1 source index; source comparison skipped
WARN  kanji/観.md: no quizOnyomi
WARN  kanji/観.md: no quizKunyomi
WARN  kanji/負.md: not in the N1 source index; source comparison skipped
WARN  kanji/負.md: no quizOnyomi
WARN  kanji/負.md: no quizKunyomi
WARN  kanji/負.md: no Metadata: line
WARN  kanji/返.md: not in the N1 source index; source comparison skipped
WARN  kanji/返.md: no quizOnyomi
WARN  kanji/返.md: no quizKunyomi
WARN  kanji/返.md: no Metadata: line
WARN  kanji/造.md: not in the N1 source index; source comparison skipped
WARN  kanji/造.md: no quizOnyomi
WARN  kanji/造.md: no quizKunyomi
WARN  words/ひっくり返す.md: Dictionary: line cites no JMdict entry id
WARN  words/ひっくり返る.md: Dictionary: line cites no JMdict entry id
WARN  words/代名詞.md: Dictionary: line cites no JMdict entry id
WARN  words/名作.md: Dictionary: line cites no JMdict entry id
WARN  words/名刺.md: Dictionary: line cites no JMdict entry id
WARN  words/名前.md: no Dictionary: line
WARN  words/名字.md: Dictionary: line cites no JMdict entry id
WARN  words/名所.md: Dictionary: line cites no JMdict entry id
WARN  words/名物.md: Dictionary: line cites no JMdict entry id
WARN  words/名詞.md: Dictionary: line cites no JMdict entry id
WARN  words/平仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/引き返す.md: Dictionary: line cites no JMdict entry id
WARN  words/振り仮名.md: Dictionary: line cites no JMdict entry id
WARN  words/文章.md: no Dictionary: line
WARN  words/有名.md: no Dictionary: line
WARN  words/構造.md: Dictionary: line cites no JMdict entry id
WARN  words/背負う.md: Dictionary: line cites no JMdict entry id
WARN  words/見せる.md: no Dictionary: line
WARN  words/見慣れる.md: Dictionary: line cites no JMdict entry id
WARN  words/見本.md: Dictionary: line cites no JMdict entry id
WARN  words/見物.md: no Dictionary: line
WARN  words/見舞う.md: Dictionary: line cites no JMdict entry id
WARN  words/観念.md: Dictionary: line cites no JMdict entry id
WARN  words/観測.md: Dictionary: line cites no JMdict entry id
WARN  words/講師.md: Dictionary: line cites no JMdict entry id
WARN  words/返事.md: no Dictionary: line
WARN  words/造船.md: Dictionary: line cites no JMdict entry id
WARN  words/題名.md: Dictionary: line cites no JMdict entry id
ERROR kanji/師.md: metadata reading いくさ has no Readings row
ERROR kanji/観.md: metadata reading み.る has no Readings row
ERROR kanji/観.md: metadata reading しめ.す has no Readings row
ERROR kanji/負.md: metadata reading ま.かす has no Readings row
4 error(s), 59 warning(s)
exit 1
```

## Meaning quiz safety

```text
Command (at 60d2cd5a): python quiz_safety.py 偏 偽 傍 債 勲 匠 匿 升 即 却
偏 (lean to one side; biased)  options: fish | rain | ear
    reading ヘン     (on): wrong options from distractors 3/3 (rest filled from other cards)
偽 (fake; false)  options: dog | mountain | white
    reading ギ      (on): wrong options from distractors 3/3 (rest filled from other cards)
傍 (beside; nearby)  options: red | noon | gold, money
    reading ボウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
債 (debt; bond)  options: flower | moon, month | water
    reading サイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
勲 (meritorious service; order of merit)  options: east | mouth | black
    reading クン     (on): wrong options from distractors 3/3 (rest filled from other cards)
匠 (artisan; master craftsman)  options: rain | dog | south
    reading ショウ    (on): wrong options from distractors 3/3 (rest filled from other cards)
匿 (hide; shelter)  options: father | fish | year
    reading トク     (on): wrong options from distractors 3/3 (rest filled from other cards)
升 (measuring box; shō (volume unit))  options: dog | river | ear
    reading ます     (kun): wrong options from distractors 3/3 (rest filled from other cards)
即 (immediate; at once)  options: mother | white | heaven, sky
    reading ソク     (on): wrong options from distractors 3/3 (rest filled from other cards)
却 (step back; reject)  options: woman, female | rice field | flower
    reading キャク    (on): wrong options from distractors 3/3 (rest filled from other cards)
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
exit 0
```

## Reading quiz exposure (tail; full output in evidence\audits)

```text
る (KANJIDIC2 name reading, --extra list) is offered by 上 昇 登; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [升 上] -> あがる あげる うえ うわ かみ のぼる; [升 昇] -> のぼる
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (3 holders tried)
       sampling N1 stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling All stack: 200 seeds, 3 of 3 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 3 of 3 drawable wrong options seen
== 即 (immediate; at once)   curated option cards: 母 白 天   tags: jlpt-n1 grade-8 structure-unclassified
   curated 母: tags jlpt-n5 grade-2 indicative starter; in pools: N1 stack, All stack, Starter practice session; on ボ | kun はは も
   curated 白: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ハク ビャク | kun しろ しら- しろ.い
   curated 天: tags jlpt-n5 grade-1 indicative starter; in pools: N1 stack, All stack, Starter practice session; on テン | kun あまつ あめ あま-
   JMdict single-kanji entries: 2264220: instantly, immediately, at once -> そく
   unlisted readings attested for 即: しょく (--extra list)
   on prompt ソク (key そく)
       N1 stack: curated 母 白 天 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       attested reading しょく (--extra list) is offered by 植 続 職 色 触 食; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [即 植] -> しょく; [即 続] -> きょう こう しょく
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (6 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 4 of 4 drawable wrong options seen
   kun: no reading prompts
== 却 (step back; reject)   curated option cards: 女 田 花   tags: jlpt-n1 grade-8 structure-unclassified
   curated 女: tags jlpt-n5 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ジョ ニョ ニョウ | kun おんな め
   curated 田: tags jlpt-n4 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on デン | kun た
   curated 花: tags jlpt-n4 grade-1 phonetic-compound starter; in pools: N1 stack, All stack, Starter practice session; on カ ケ | kun はな
   JMdict single-kanji entries: none
   unlisted readings attested for 却: none
   on prompt キャク (key きゃく)
       N1 stack: curated 女 田 花 -> 6 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 6 drawable wrong options (6 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       sampling N1 stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling All stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 6 of 6 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 4 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
exit 0
```

## Reading quiz options (tail; full output in evidence\audits)

```text
 (44): おう きゅう きょう ぎゅう ぎょう くう ぐう こう ごう しき しち しつ しゃ しゃく しゅ しゅく しゅつ しゅん しょく しん じゅう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう ... (+4 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 匿 (hide; shelter)   curated option cards: 父 魚 年
   metadata readings: on トク | kun かくま.う
   unlisted readings attested for 匿: じょく (--extra list)  かくれる (--extra list)  かくす (--extra list)
   on prompt トク (key とく)
       excluded keys: 8
       curated 父: ふ
       curated 魚: ぎょ
       curated 年: ねん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 46 keys, 2: 209 keys
       tier 3 candidates (46): あく いく おく かく がく きく きゃく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく じゅく そく ぞく たく ちく ちゃく ちょく と とう とつ とん にく はく ばく ひゃく ふく ほく ぼく まく みゃく もく やく よく ... (+6 more)
       unlisted-reading check: none of the 3 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 升 (measuring box; shō (volume unit))   curated option cards: 犬 川 耳
   metadata readings: on ショウ | kun ます
   unlisted readings attested for 升: のぼる (--extra list)
   on: no reading prompts
   kun prompt ます (key ます)
       excluded keys: 5
       curated 犬: いぬ いぬ
       curated 川: かわ
       curated 耳: みみ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 2 keys, 3: 119 keys, 2: 679 keys, 1: 8 keys, 0: 127 keys
       tier 4 candidates (2): まかす まわす
       tier 3 candidates (119): あかす あます あらす あわす いかす いたす いやす うす うつす おかす おこす おす おとす おぼす おろす かえす かくす かす からす きざす くす くずす くらす けがす けす こがす こす こぼす こらす ころす こわす さがす さす さます しめす しるす す すかす すごす すます ... (+79 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading のぼる (--extra list) is offered only by card(s) 上 昇 登
       simulation: 3 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 即 (immediate; at once)   curated option cards: 母 白 天
   metadata readings: on ソク | kun つ.く つ.ける すなわ.ち
   unlisted readings attested for 即: しょく (--extra list)
   on prompt ソク (key そく)
       excluded keys: 14
       curated 母: ぼ
       curated 白: はく びゃく
       curated 天: てん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 46 keys, 2: 209 keys
       tier 3 candidates (46): あく いく おく かく がく きく きゃく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく じゅく そ そう そつ そん たく ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふく ほく ぼく まく みゃく もく やく よく ... (+6 more)
       HIT (can be drawn): unlisted reading しょく (--extra list) is offered by card(s) 植 続 職 色 触 食
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 却 (step back; reject)   curated option cards: 女 田 花
   metadata readings: on キャク | kun かえ.って しりぞ.く しりぞ.ける
   unlisted readings attested for 却: none
   on prompt キャク (key きゃく)
       excluded keys: 18
       curated 女: じょ にょ にょう
       curated 田: でん
       curated 花: か け
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 4: 2 keys, 3: 44 keys, 2: 168 keys, 1: 2 keys, 0: 40 keys
       tier 4 candidates (2): きく きょく
       tier 3 candidates (44): あく いく おく かく がく きつ きゅう きょ きょう きん ぎょく こく さく しゃく しゅく しょく じゃく じゅく そく ぞく たく ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふく ほく ぼく まく みゃく もく やく よく らく りく ... (+4 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
2 problem(s)
exit 1
```
