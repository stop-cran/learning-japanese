# Mechanical checks (automatic output, not a review verdict)

## lint (JMdict ids checked)

```text
kanji checked: 15, words checked: 34
WARN  words/炊く.md: Dictionary: line cites no JMdict entry id
WARN  words/脱ぐ.md: no Dictionary: line
WARN  words/脱線.md: Dictionary: line cites no JMdict entry id
WARN  words/膨らます.md: Dictionary: line cites no JMdict entry id
WARN  words/膨らむ.md: Dictionary: line cites no JMdict entry id
WARN  words/透明.md: Dictionary: line cites no JMdict entry id
WARN  words/鉢.md: no Dictionary: line
WARN  words/間隔.md: Dictionary: line cites no JMdict entry id
0 error(s), 8 warning(s)
```

## lint (--no-jmdict)

```text
kanji checked: 15, words checked: 34
WARN  words/脱ぐ.md: no Dictionary: line
WARN  words/鉢.md: no Dictionary: line
0 error(s), 2 warning(s)
```

## quiz safety simulation

```text
bear (animal)
    reading ショウ    (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading こ.げる   (kun): wrong options from distractors 3/3 (rest filled from other cards)
    reading こ.がす   (kun): wrong options from distractors 3/3 (rest filled from other cards)
異 (different; unusual; strange)  options: stomach | together; shared | surround; enclose
    reading イ      (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading こと.なる  (kun): wrong options from distractors 2/3 (rest filled from other cards)
端 (edge; end; tip)  options: new | mountain | short
    reading タン     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading はし     (kun): wrong options from distractors 3/3 (rest filled from other cards)
筋 (muscle; sinew; line; plot)  options: employment; diligence | cylinder; tube | box
    reading キン     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading すじ     (kun): wrong options from distractors 3/3 (rest filled from other cards)
粗 (coarse; rough; crude)  options: ancestor | group; assemble | flour; powder
    reading ソ      (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading あら.い   (kun): wrong options from distractors 2/3 (rest filled from other cards)
納 (pay; deliver; put away; accept)  options: paper | brain; mind | south
    reading ナッ     (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading おさ.める  (kun): wrong options from distractors 3/3 (rest filled from other cards)
脱 (undress; remove; escape)  options: drink | read | hear, ask
    reading ダツ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading ぬ.ぐ    (kun): wrong options from distractors 3/3 (rest filled from other cards)
膨 (swell; expand; inflate)  options: shadow; silhouette | arm; skill | hat; headgear
    reading ボウ     (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading ふく.らむ  (kun): wrong options from distractors 3/3 (rest filled from other cards)
致 (do humbly; bring about; send)  options: talk, speak | buy | study
    reading チ      (on): wrong options from distractors 3/3 (rest filled from other cards)
    reading いた.す   (kun): wrong options from distractors 3/3 (rest filled from other cards)
請 (request; beg; undertake)  options: pure, clean | clear skies | quiet
    reading セイ     (on): wrong options from distractors 0/3 (rest filled from other cards)
    reading こ.う    (kun): wrong options from distractors 3/3 (rest filled from other cards)
透 (transparent; see through; permeate)  options: escape; flee | get lost; be unsure | tower; pagoda
    reading トウ     (on): wrong options from distractors 1/3 (rest filled from other cards)
    reading す.く    (kun): wrong options from distractors 2/3 (rest filled from other cards)
鉢 (bowl; flowerpot)  options: eight | iron | lead (metal)
    reading ハチ     (on): wrong options from distractors 2/3 (rest filled from other cards)
隔 (separate; partition; every other)  options: rank; character | leather; reform | sunshine
    reading カク     (on): wrong options from distractors 2/3 (rest filled from other cards)
    reading へだ.てる  (kun): wrong options from distractors 2/3 (rest filled from other cards)
駄 (packhorse; horse load; worthless)  options: thick; plump | station | strike
    reading タ      (on): wrong options from distractors 3/3 (rest filled from other cards)
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
ng N1 stack: 200 seeds, 13 of 13 drawable wrong options seen
       sampling All stack: 200 seeds, 13 of 13 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 5 of 5 drawable wrong options seen
   kun: no reading prompts
== 隔 (separate; partition; every other)   curated option cards: 格 革 陽   tags: jlpt-n1 grade-8 structure-unclassified
   curated 格: tags jlpt-n3 grade-5 structure-unclassified; in pools: N1 stack, All stack; on カク コウ キャク ゴウ | kun -
   curated 革: tags jlpt-n2 grade-6 structure-unclassified; in pools: N1 stack, All stack; on カク | kun かわ
   curated 陽: tags jlpt-n3 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ヨウ | kun ひ
   JMdict single-kanji entries: 2076880: every other, second, alternate -> かく
   unlisted readings attested for 隔: none
   on prompt カク (key かく)
       N1 stack: curated 格 革 陽 -> 4 outcomes; deficit 1/2: the fallback fills the open slots; 46 drawable wrong options (4 curated, 42 fallback)
       All stack: curated 格 革 陽 -> 4 outcomes; deficit 1/2: the fallback fills the open slots; 46 drawable wrong options (4 curated, 42 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 16 drawable wrong options (0 curated, 16 fallback)
       sampling N1 stack: 200 seeds, 41 of 46 drawable wrong options seen
       sampling All stack: 200 seeds, 41 of 46 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 16 of 16 drawable wrong options seen
   kun prompt へだ.てる (key へだてる)
       N1 stack: curated 革 陽 -> 1 outcomes; deficit 1: the fallback fills the open slots; 288 drawable wrong options (2 curated, 286 fallback)
       All stack: curated 革 陽 -> 1 outcomes; deficit 1: the fallback fills the open slots; 288 drawable wrong options (2 curated, 286 fallback)
       Starter practice session: curated none -> 1 outcomes; deficit 3: the fallback fills the open slots; 21 drawable wrong options (0 curated, 21 fallback)
       sampling N1 stack: 200 seeds, 135 of 288 drawable wrong options seen
       sampling All stack: 200 seeds, 135 of 288 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 21 of 21 drawable wrong options seen
== 駄 (packhorse; horse load; worthless)   curated option cards: 太 駅 打   tags: jlpt-n1 grade-8 structure-unclassified
   curated 太: tags jlpt-n3 grade-2 structure-unclassified; in pools: N1 stack, All stack; on タイ タ | kun ふと.い ふと.る
   curated 駅: tags jlpt-n4 grade-3 phonetic-compound starter; in pools: N1 stack, All stack, Starter practice session; on エキ | kun -
   curated 打: tags jlpt-n3 grade-3 structure-unclassified; in pools: N1 stack, All stack; on ダ ダース | kun う.つ う.ち- ぶ.つ
   JMdict single-kanji entries: 2648880: poor, low-grade, trivial -> だ
   unlisted readings attested for 駄: のせる (card text)  においうま (card text)
   on prompt タ (key た)
       N1 stack: curated 太 駅 打 -> 4 outcomes; deficit 0/1/2: the fallback fills the open slots; 6 drawable wrong options (3 curated, 3 fallback)
       All stack: curated 太 駅 打 -> 4 outcomes; deficit 0/1/2: the fallback fills the open slots; 6 drawable wrong options (3 curated, 3 fallback)
       Starter practice session: curated 駅 -> 1 outcomes; deficit 2: the fallback fills the open slots; 4 drawable wrong options (1 curated, 3 fallback)
       sampling N1 stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling All stack: 200 seeds, 6 of 6 drawable wrong options seen
       sampling Starter practice session: 200 seeds, 4 of 4 drawable wrong options seen
   kun: no reading prompts
0 production hit(s) (N1 / All stack pools); 0 padded-session hit(s) (Starter practice session only); 17 latent collision(s) (attested reading offered by another card, not drawable in any of these pools)
0 one-holder padded hit(s) (a Starter practice session that also borrows one holder card can offer an attested reading that is not a KANJIDIC2 name-only reading); 1 more for KANJIDIC2 name-only readings
```

## reading options (tail; full file in evidence\audits)

```text
urated 迷: まよう
       curated 塔: no usable kun reading, slot filled from the fallback
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 63 keys, 2: 655 keys, 1: 8 keys, 0: 106 keys
       tier 3 candidates (63): あく あばく あるく いく うく うごく えがく おく かく かわく きく きずく こく さく しく しずく す すう すえ すがた すぎ すぎる すくう すこし すさぶ すじ すすき すすぐ すすむ すずむ すてる すな すべ すべて すみ すむ すもも する すわる せく ... (+23 more)
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading とおる (card text) is offered only by card(s) 通
       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading とおす (card text) is offered only by card(s) 通
       simulation: 51 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 鉢 (bowl; flowerpot)   curated option cards: 八 鉄 鉛
   metadata readings: on ハチ ハツ | kun -
   unlisted readings attested for 鉢: none
   on prompt ハチ (key はち)
       excluded keys: 8
       curated 八: はち(skipped: excluded) はつ(skipped: excluded)
       curated 鉄: てつ
       curated 鉛: えん
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 11 keys, 2: 237 keys
       tier 3 candidates (11): いち きち しち ち にち は はい はく はっ はん りち
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 13 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
== 隔 (separate; partition; every other)   curated option cards: 格 革 陽
   metadata readings: on カク | kun へだ.てる へだ.たる
   unlisted readings attested for 隔: none
   on prompt カク (key かく)
       excluded keys: 15
       curated 格: かく(skipped: excluded) こう きゃく ごう
       curated 革: かく(skipped: excluded)
       curated 陽: よう
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 42 keys, 2: 203 keys
       tier 3 candidates (42): あく いく おく か かい かっ かつ かん きく きょく ぎゃく ぎょく く こく さく しゃく しゅく しょく じゃく そく ぞく たく ちく ちゃく ちょく とく どく にく はく ばく ひゃく ふく ほく ぼく もく やく よく らく りく りゃく ... (+2 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 36 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun prompt へだ.てる (key へだてる)
       excluded keys: 15
       curated 格: no usable kun reading, slot filled from the fallback
       curated 革: かわ
       curated 陽: ひ
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 286 keys, 2: 301 keys, 1: 18 keys, 0: 266 keys
       tier 3 candidates (286): あからめる あける あげる あさる あずける あたえる あたたまる あたる あつまる あてる あばれる あびる あまえる あまる あやまる あやめる あらためる あらわれる あれる あわせる いかる いきる いする いためる いたる いでる いのる いましめる いれる うえる うかれる うける うすめる うせる うつる うまれる うめる うれる おいる おきる ... (+246 more)
       unlisted-reading check: none of the 0 unlisted readings is offered by any of the 1659 other kun-reading cards
       simulation: 83 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
== 駄 (packhorse; horse load; worthless)   curated option cards: 太 駅 打
   metadata readings: on ダ タ | kun -
   unlisted readings attested for 駄: のせる (card text)  においうま (card text)
   on prompt タ (key た)
       excluded keys: 2
       curated 太: たい た(skipped: excluded)
       curated 駅: えき
       curated 打: だ(skipped: excluded) だーす
       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): 3: 4 keys, 2: 216 keys, 0: 29 keys
       tier 3 candidates (4): たい たく たつ たん
       unlisted-reading check: none of the 2 unlisted readings is offered by any of the 296 other on-reading cards
       simulation: 6 wrong options seen over 100 seeds; 0 seeds with fewer than three wrong options
   kun: no reading prompts
2 problem(s)
```

## link plan verify

```text
changed word files: 34; expected pairs: 34; added link pairs: 34; total added links: 34; declared remark edits: 0; problems: 0
```

## validate

```text
0 error(s)
```

## content budget

```text
{'files': 8853, 'entries': 8868, 'retainedBytes': 50635475, 'inflatedBytes': 50907053, 'localZipBytes': 31843256, 'listeningTaskMediaBytes': 5893602}
```

## grammar vocabulary

```text
Vocabulary coverage: 3201/3336 reviewed prompts; stage=pilot
```

## manifest rebuild

```text
build_manifest.py at freeze 420a6669: manifest.json: 8846 files incl. 401 images, 203 scene catalogs, 36 listening passages, 1 curriculum catalogs, 40 listening tasks, version 867f67a7f9ec4ba1
manifest.json sha256 before 4D53BB8D1FDE4FC9A4576CEE3D9551ABE02CEB46C5002DF9FD1883B85AA5855C, after 4D53BB8D1FDE4FC9A4576CEE3D9551ABE02CEB46C5002DF9FD1883B85AA5855C; tracked tree after rebuild: clean
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
