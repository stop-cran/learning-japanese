# Mechanical checks (automatic output, not a review verdict)

## Content validation

```text
Command (at 1a9bb910): python tools\validate.py
0 error(s)
exit 0
```

## B159 batch audit

```text
Command (at 1a9bb910): python tools\audit_n1_batch.py --batch 159
{
  "batch": "159",
  "baseCommit": "2787e43b5706a569d83627849aa40ed3582a7d18",
  "draftKanji": 10,
  "newWords": 10,
  "changedReusedArticles": 9,
  "requiredReciprocalPairs": 10,
  "activatedBaselinePairs": 0,
  "readingDispositions": 21,
  "curatedOfferedKeys": 10,
  "sourceOnlyOfferedKeys": 0,
  "dictionaryFamilies": 89,
  "exactBaseRuntimePreservedOutsideRecordedChanges": true,
  "manifestFresh": true,
  "contentVersion": "6d497dcb6f21d7d3",
  "limits": "Mechanical draft audit, not lexical-allocation/naturalness verification, independent review, native/phone acceptance or publication."
}
exit 0
```

## Unit tests (tools suite)

```text
Ran 439 tests in 64.604s
OK
exit 0
```

## Manifest rebuild

```text
Command (at 1a9bb910): python tools\build_manifest.py
manifest.json: 9843 files incl. 504 images, 305 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 6d497dcb6f21d7d3
manifest.json sha256 before AA2963B0413911479F9CBE0372E3341AA9E74DFE7212D82890314EFA5FB3FAB0, after AA2963B0413911479F9CBE0372E3341AA9E74DFE7212D82890314EFA5FB3FAB0; tracked tree after rebuild: clean
exit 0
```

## Content budget

```text
Command (at 1a9bb910): python tools\check_content_budget.py
{'files': 9850, 'entries': 9866, 'retainedBytes': 56880848, 'inflatedBytes': 57316920, 'localZipBytes': 36535545, 'listeningTaskMediaBytes': 5893602}
exit 0
```

## Grammar vocabulary

```text
Command (at 1a9bb910): python tools\grammar_vocabulary.py check
Vocabulary coverage: 3201/3539 reviewed prompts; stage=pilot
exit 0
```

## Whitespace (git diff --check)

```text
Command (at 1a9bb910): git -c core.whitespace=cr-at-eol diff --check 2787e43b 1a9bb910 (whole range from the batch base, including any merged-in main commits)
exit 0
```

## N1 lint (the 4 errors are on reused files and are also reported at base 2787e43b)

```text
Command (at 1a9bb910): python lean\n1_batch_tool.py lint --base 2787e43b
kanji checked: 19, words checked: 66
WARN  kanji/不.md: not in the N1 source index; source comparison skipped
WARN  kanji/不.md: no quizOnyomi
WARN  kanji/不.md: no quizKunyomi
WARN  kanji/不.md: no Metadata: line
WARN  kanji/味.md: not in the N1 source index; source comparison skipped
WARN  kanji/味.md: no quizOnyomi
WARN  kanji/味.md: no quizKunyomi
WARN  kanji/味.md: no Metadata: line
WARN  kanji/太.md: not in the N1 source index; source comparison skipped
WARN  kanji/太.md: no quizOnyomi
WARN  kanji/太.md: no quizKunyomi
WARN  kanji/官.md: not in the N1 source index; source comparison skipped
WARN  kanji/官.md: no quizOnyomi
WARN  kanji/官.md: no quizKunyomi
WARN  kanji/情.md: not in the N1 source index; source comparison skipped
WARN  kanji/情.md: no quizOnyomi
WARN  kanji/情.md: no quizKunyomi
WARN  kanji/服.md: not in the N1 source index; source comparison skipped
WARN  kanji/服.md: no quizOnyomi
WARN  kanji/服.md: no quizKunyomi
WARN  kanji/服.md: no Metadata: line
WARN  kanji/聞.md: not in the N1 source index; source comparison skipped
WARN  kanji/聞.md: no quizOnyomi
WARN  kanji/聞.md: no quizKunyomi
WARN  kanji/聞.md: no Metadata: line
WARN  kanji/贈.md: not in the N1 source index; source comparison skipped
WARN  kanji/贈.md: no quizOnyomi
WARN  kanji/贈.md: no quizKunyomi
WARN  words/不潔.md: Dictionary: line cites no JMdict entry id
WARN  words/不規則.md: Dictionary: line cites no JMdict entry id
WARN  words/不運.md: Dictionary: line cites no JMdict entry id
WARN  words/味.md: no Dictionary: line
WARN  words/和服.md: Dictionary: line cites no JMdict entry id
WARN  words/太る.md: no Dictionary: line
WARN  words/太鼓.md: Dictionary: line cites no JMdict entry id
WARN  words/官庁.md: Dictionary: line cites no JMdict entry id
WARN  words/新聞.md: no Dictionary: line
WARN  words/服.md: no Dictionary: line
WARN  words/洋服.md: no Dictionary: line
WARN  words/聞く.md: no Dictionary: line
WARN  words/調味料.md: Dictionary: line cites no JMdict entry id
ERROR kanji/太.md: metadata reading タ has no Readings row
ERROR kanji/情.md: metadata reading セイ has no Readings row
ERROR kanji/情.md: metadata reading なさ.け has no Readings row
ERROR kanji/聞.md: unknown keys ['phonetic']
4 error(s), 41 warning(s)
exit 1
```

## Meaning quiz safety

```text
Command (at 1a9bb910): python quiz_safety.py 厘 又 叔 叙 吉 后 吏 吟 呈 呉
厘 (one-hundredth; rin (1/1000 yen))  options: left | blue, green | electricity
    reading リン     (on): wrong options from distractors 3/3 (rest filled from other cards)
又 (again; also; or)  options: north | country | man, male
    reading また-    (kun): wrong options from distractors 3/3 (rest filled from other cards)
叔 (uncle or aunt (younger than a parent))  options: east | school | thing, object
    reading シュク    (on): wrong options from distractors 3/3 (rest filled from other cards)
叙 (narrate; describe; confer (rank or honor))  options: within, inner | eat, food | eight
    reading ジョ     (on): wrong options from distractors 3/3 (rest filled from other cards)
吉 (good luck; auspicious)  options: down, below | matter, affair | thousand
    reading キツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
后 (empress; queen (consort))  options: one | come | hundred
    reading コウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
吏 (official; civil servant)  options: now | six | red
    reading リ      (on): wrong options from distractors 3/3 (rest filled from other cards)
吟 (recite poetry; chant)  options: two | self, oneself | company, shrine
    reading ギン     (on): wrong options from distractors 3/3 (rest filled from other cards)
呈 (present; offer; reveal)  options: short | go | seven
    reading テイ     (on): wrong options from distractors 3/3 (rest filled from other cards)
呉 (Wu (ancient Chinese state); China)  options: spirit, air | yen, circle | foot, leg
    reading ゴ      (on): wrong options from distractors 3/3 (rest filled from other cards)
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
4 outcomes; deficit 0/1: the fallback fills the open slots; 61 drawable wrong options (4 curated, 57 fallback)
       Starter practice session: curated 二 自 社 -> 4 outcomes; deficit 0/1: the fallback fills the open slots; 27 drawable wrong options (4 curated, 23 fallback)
       sampling N1 stack: 200 seeds, 29 of 61 drawable wrong options seen
       sampling All stack: 200 seeds, 29 of 61 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 23 of 27 drawable wrong options seen
   kun: no reading prompts
== 呈 (present; offer; reveal)   curated option cards: 短 行 七   tags: jlpt-n1 grade-8 structure-unclassified
   curated 短: tags jlpt-n2 grade-3 phonetic-compound starter; in pools: N1 stack, All stack, Starter practice session; on タン | kun みじか.い
   curated 行: tags jlpt-n5 grade-2 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on コウ ギョウ アン | kun い.く ゆ.く おこな.う
   curated 七: tags jlpt-n5 grade-1 number starter; in pools: N1 stack, All stack, Starter practice session; on シチ | kun なな なな.つ なの
   JMdict single-kanji entries: none
   unlisted readings attested for 呈: しめす (--extra list)
   on prompt テイ (key てい)
       N1 stack: curated 短 行 七 -> 3 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 5 drawable wrong options (5 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       sampling N1 stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling All stack: 200 seeds, 5 of 5 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
   kun: no reading prompts
== 呉 (Wu (ancient Chinese state); China)   curated option cards: 気 円 足   tags: jlpt-n1 grade-8 structure-unclassified
   curated 気: tags jlpt-n5 grade-1 compound starter; in pools: N1 stack, All stack, Starter practice session; on キ ケ | kun いき き
   curated 円: tags jlpt-n5 grade-1 shinjitai currency starter; in pools: N1 stack, All stack, Starter practice session; on エン | kun まる.い まる まど まど.か まろ.やか
   curated 足: tags jlpt-n4 grade-1 pictograph starter; in pools: N1 stack, All stack, Starter practice session; on ソク | kun あし た.りる た.る た.す
   JMdict single-kanji entries: 2811510: go, soy beans soaked and mashed to a creamy paste (ingredient of tofu and soy milk) -> ご; 2836255: Wu (region in China, south of the lower Yangtze) -> ご
   unlisted readings attested for 呉: ぐ (KANJIDIC2 name reading)
   on prompt ゴ (key ご)
       N1 stack: curated 気 円 足 -> 2 outcomes; the curated options fill all three wrong slots in every outcome, the fallback is never consulted; 4 drawable wrong options (4 curated, 0 fallback)
       All stack: identical to N1 stack
       Starter practice session: identical to N1 stack
       attested reading ぐ (KANJIDIC2 name reading) is offered by 供 具 工 求; it cannot be drawn in the N1 stack, All stack or Starter practice session pool
       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): [呉 供] -> きょう く くう ぐ; [呉 具] -> ぐ
       Starter practice session that also borrows one holder card (the pool grows by that card): not drawable with any single holder (4 holders tried)
       sampling N1 stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling All stack: 200 seeds, 4 of 4 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 4 of 4 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 10 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 0 more for KANJIDIC2 name-only readings
exit 0
```

## Reading quiz options (tail; full output in evidence\audits)

```text
ゃく
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 39 keys, 2: 215 keys
       tier 3 candidates (39): う おう きゅう きょう ぎゅう ぎょう くう ぐう こ こく こつ こん しゅう しょう じゅう じょう すう そう ぞう ちゅう ちょう つう とう どう にゅう にょう のう ひょう びょう ふう ほう ぼう みょう もう ゆう よう りゅう りょう ろう
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 吏 (official; civil servant)   curated option cards: 今 六 赤
   metadata readings: on リ | kun -
   unlisted readings attested for 吏: つかさ (--extra list)  さと (KANJIDIC2 name reading)  し (KANJIDIC2 name reading)
   on prompt リ (key り)
       excluded keys: 1
       curated 今: こん きん
       curated 六: ろく りく
       curated 赤: せき しゃく
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 5 keys, 2: 224 keys, 1: 3 keys, 0: 29 keys
       tier 3 candidates (5): りき りく りつ りょ りん
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading し (KANJIDIC2 name reading) is offered only by card(s) 仕 伺 使 刺 史 司 四 士 姉 始 姿 子 市 師 志 思 指 支 施 旨 枝 次 止 歯 死 氏 示 私 糸 紙 脂 自 至 視 詞 試 詩 誌 資
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 吟 (recite poetry; chant)   curated option cards: 二 自 社
   metadata readings: on ギン | kun -
   unlisted readings attested for 吟: うたう (--extra list)  うめく (--extra list)
   on prompt ギン (key ぎん)
       excluded keys: 2
       curated 二: に じ
       curated 自: じ し
       curated 社: しゃ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 57 keys, 2: 199 keys
       tier 3 candidates (57): あん いん うん えん おん かん がん ぎ ぎゃく ぎゅう ぎょ ぎょう ぎょく くん ぐん けん げん こん さん ざん しゅん しん じゅん じん すん せん ぜん そん たん だん ちん てん でん どん なん にん ねん はん ばん ひん ... (+17 more)
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 19 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 呈 (present; offer; reveal)   curated option cards: 短 行 七
   metadata readings: on テイ | kun -
   unlisted readings attested for 呈: しめす (--extra list)
   on prompt テイ (key てい)
       excluded keys: 2
       curated 短: たん
       curated 行: こう ぎょう あん
       curated 七: しち
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 32 keys, 2: 223 keys
       tier 3 candidates (32): あい い えい かい がい けい げい さい ざい すい ずい せい ぜい たい だい つい てき てつ てん ない ねい はい ばい へい べい まい めい ゆい らい りい るい れい
       unlisted-reading check: none of the 1 unlisted readings is offered by any of the 304 other on-reading cards
       simulation: 5 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 呉 (Wu (ancient Chinese state); China)   curated option cards: 気 円 足
   metadata readings: on ゴ | kun く.れる くれ
   unlisted readings attested for 呉: ぐ (KANJIDIC2 name reading)
   on prompt ゴ (key ご)
       excluded keys: 6
       curated 気: き け
       curated 円: えん
       curated 足: そく
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 2 keys, 2: 227 keys, 0: 32 keys
       tier 3 candidates (2): ごく ごん
       tier 2 candidates (227): あ あい あく あつ あん い いき いく いち いん う うん えい えき えつ えん お おう おく おつ おん か かい かく かつ かん が がい がく がん き きく きつ きょ きん ぎ ぎょ ぎん く くう ... (+187 more)
       info (can be drawn): ぐ is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) 供 具 工 求
       simulation: 4 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
0 problem(s)
exit 0
```
