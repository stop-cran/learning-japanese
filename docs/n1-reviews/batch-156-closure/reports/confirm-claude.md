# Batch 156 confirmation review (Claude)

**Model:** Claude, by Anthropic. I am the same independent reviewer who wrote the initial report (`reports-156-hold\initial-claude.md`).

## Snapshot

- **Revised snapshot under review:** 395f53643988ba24f444a376187c803aa6794654
- **Earlier reviewed snapshot:** c6afa16315d5a88b5045eeb85d429b8f7fd90b1f

## Scope

**Files read in full:**
- **Revised kanji cards (7):** 乙, 亜, 仙, 伎, 伏, 伐, 伴
- **New word article:** `words\甲乙.md`
- **Changed word articles:** `words\仁.md`, `words\亜熱帯.md`
- **Deleted article:** the old `words\乙.md`, read from the original packet

**Every changed hunk:**
- I checked each hunk listed in CHANGES.md against all four facets.
- I compared those hunks with the hunk headers of fix.patch. Each change is a one-line replacement, except two: `words/乙.md` is deleted and `words/甲乙.md` is added.

**Evidence read:**
- **Sources:**
  - `甲乙-daijisen.txt`
  - `jmdict-cited-entries.xml`. I parsed these entries: 1280080, 1182940, 1182945, 1578730, 1583850, 1595120, 1874770, 2124490, 2397580, 1369620, 1466670, 1282860, 1268820, 1778760, 1357390 and 1417780.
  - `wazaogi-scan.txt`
- **App and audit logic:**
  - `distractor-senses.txt`
  - `QuizBuilder.kt`
  - `compound-sound-changes.md`
- **word-quiz.txt:**
  - Lines 60–125.
  - The 仁 tie, by keyword scan only.
  - The reverse 甲乙 entries (2549–2612).
  - The reverse 仁 entries (2691–2740).
- **Checks:**
  - quiz-safety, link-targets, reading-options and reading-exposure (relevant ranges)
  - lint, validate, unittest, linkplan, kanji-remarks and manifest
- **Original packet:**
  - `jmdict-families.xml`: entry 1149930 (亜流)
  - `snapshot\kanji\潜.md`: Notes
  - Related word articles: 丹念, 伐採, 伯仲, 同伴, 降伏, 歌舞伎
  - Rubric: lines 100–125
  - `evidence\app-code\`: the exclusion logic

**Web:** one search for 甲乙 in contracts (snippet only) and one jisho.org fetch for 甲乙 (rendered no results).

## Dispositions

- **C1 — RESOLVED.**
  - `words/乙.md` is deleted and nothing links to it any more. `link-targets.tsv` shows all 16 links resolve, and the quoted titles I compared match.
  - 甲乙 こうおつ has one JMdict reading (entry 1280080).
  - Its reading quiz (word-quiz.txt:90–92) offers only invented look-alikes: ごうおつ, こおつ, こうおうつ and こうおず. None is an attested reading of 甲乙, so the 音 おと collision is gone.
  - The 乙 card still teaches both readings adequately for a beginner:
    - おと: kunyomi おと- (line 10), 乙子 おとご (33), 乙女 おとめ (42), and the 弟/妹 note (53).
    - おつ: line 31 names the word 乙 おつ with JMdict 1182940.
  - The app-level fix (ReadingOptions) is deferred, and that is acceptable for this batch.
- **O1 — RESOLVED.** `仁.md:22` now reads "This book discusses benevolence in Confucianism.", which is natural English.
- **O2 — RESOLVED.** `仁.md:38` matches JMdict 1369620:
  - Senses 1, 2 and 4 are restricted to the reading じん.
  - "Kernel" is unrestricted.
  - The nucleolus sense is marked as biology.
- **O3 — DECLINE ACCEPTED.**
  - `reading-options.txt:131` still prints the は HIT line.
  - 伯's curated cards (自, 物, 毎) fill all three slots, so は cannot be drawn in the N1 stack, the All stack or a Starter session. `reading-exposure.txt` confirms this, and its holder-borrow test also says は is not drawable.
  - The line is a tooling over-report, not a content defect. Recording it as a tooling follow-up is appropriate.
- **L1 — RESOLVED.**
  - `wazaogi-scan.txt` reports 0 entries read わざおぎ and 0 readings starting with わざお.
  - The only entry spelled 伎 is 1225090 (わざ, ぎ).
  - The scanned file's sha256, 42bd8fbc…ca6cec, equals `jmdictSha256` in the original packet's provenance.json.
- **L2 — RESOLVED.** I parsed each cited entry from `jmdict-cited-entries.xml` and compared it with the article text. Every quoted gloss matches:
  - 入念 1466670 (丹念.md:32)
  - 降参 1282860, both senses (降伏.md:32)
  - 互角 1268820 (伯仲.md:32)
  - 歌舞 1778760 (歌舞伎.md:29)
  - 植林 1357390 (伐採.md:34)
  - 単独 1417780, sense 1 (同伴.md:34)
  - 甲 1578730 and 乙 1182940

## Changes made for the other reviews (judged as revised text)

### `words\甲乙.md` (new)

**Meanings:**
- They match JMdict 1280080:
  - Sense 1: "first and second; A and B".
  - Sense 2: "superiority and (or) inferiority; distinction (in quality)…".
- They also match Digital Daijisen (`甲乙-daijisen.txt`):
  - １ 第一と第二
  - ２ 二つのものの間の優劣, with the example 「―をつけがたい」
  - The etymology 《十干の甲と乙から》

**Readings:**
- こうおつ is correct.
- The かるめる paragraph matches Daijisen: 邦楽で、高い調子の「かる」と低い調子の「める」, written 上下／甲乙. Its Dictionary line cites that page.

**Related words and supporting glosses:**
- 甲乙つけがたい (2124490) "difficult to say which of the two is better": correct.
- 甲乙丙丁 (1874770) "A, B, C and D": correct.
- 丙 "third rank; class C": correct.
- The 甲 sense "the A party (e.g. in a contract); the first party": correct.

**Examples:** natural Japanese, and the kana いっつう is correct.

**Quiz:**
- The distractor 丙 is a good wrong answer from the same category, and it is not excluded.
- The eight exclusions are defensible against sense 2 or against the "first" overlap: 優劣, 区別, 差, 比較, 相違, 対照, いちばん, 伯仲.
- None of the remaining tie words is a correct answer: 他, 共通, 凌駕, 同格, 後者, 標準, 水準, 逆.
- None of the reverse targets makes 甲乙 a correct answer. These include 前者, 後者, 比較的, 凹凸, 対, 左右 and 同格.

**Verdict:** clean.

### 仁 exclusions (人物, 個人, 芯, 中心)

None of the four overlaps the displayed title "benevolence; compassion". Each rests on a sense the article teaches (`仁.md:38`):
- **人物:** the JMdict "human" sense. This is the strongest of the four.
- **個人:** weaker, but acceptable.
- **芯:** the "core" sense, close to "kernel". Acceptable.
- **中心** ("center; core; focus"): the weakest, discussed under Optional.

The exclusions are direct pairs, as the rubric (lines 110–112) requires.

I scanned the remaining ~1409 tied words by keyword, not line by line: 人命, 人種, 女性, 男性, 美人, 職人, 世話, 中央, 都心, 心臓, 儒教 and others. None found is a defensible correct answer.

I read all 51 reverse targets (word-quiz.txt:2691–2740), including 礼 "thanks; bow", 恩恵 "benefit; blessing", 功績 and 責任. In none of them is "benevolence; compassion" a correct meaning.

Over-exclusion only removes options, so it is harmless.

### Six new kanji distractor sets (乙 亜 仙 伎 伏 伐 伴, line 13 of each card except 亜)

**Labels and errors:** the displayed titles match `quiz-safety.txt`, which reports 0 errors.

**Correct-answer risk:** no distractor is a defensible correct meaning for its card, and none is in the target's exclusions. Two needed a closer look:
- **伏 / 座:** sitting is not lying prostrate. 伏 separately excludes 寝, 拝 and 礼.
- **伴 / 迎:** JMdict has no "escort" sense for 迎. 伴 excludes 供, whose とも entry 1233560 is also spelled 伴.

**Category:** every set stays inside the target's semantic area, so none can be rejected by category alone.

**Reading collisions:** none.
- The curated readings are:
  - 王 おう/のう; 硬 こう; 粗 そ
  - 下 か/げ; 供 きょう/く/くう/ぐ; 生 せい/しょう
  - 食 しょく/じき; 自 じ/し; 起 き
  - 座 ざ; 伸 しん; 保 ほ
  - 耕 こう; 育 いく; 迎 げい
  - 離 り; 他 た
- None of these equals an attested extra reading of its target.
- For 乙, `reading-options.txt` also confirms that the unlisted reading めり is offered by no card.
- `reading-exposure.txt` reports:
  - 0 production hits
  - 0 padded-session hits
  - 0 one-holder padded hits

**Starter sessions:** 乙, 伏, 伐 and 伴 still use the fallback options there. This is unchanged from before.

### Wording changes

- **亜:31:** "(inferior) imitator; poor imitation" matches JMdict 1149930. The gloss "epigone" was dropped, which is fine.
- **仙:32:** the ateji gloss is accurate.
- **仙:49, 伎:50, 伏:55, 伐:56, 伴:53, 乙:58:** these distractor sentences agree with the new sets and titles.
- **亜熱帯:29:** "any of the three characters" is correct.
- **乙:38:** the common-words line no longer lists 乙 as a separate article, and it is consistent with 甲乙.

### Declined layout change

I accept the decline: the change would affect every N1 card, so it is out of scope for this batch.

### Links to compound-sound-changes

- **ねっ in 亜熱帯 and ばっ in 伐採:** the gemination section explains both correctly.
- **ぷく in 潜伏:** see Optional.

### Gates

| Check | Result |
|---|---|
| lint | 0 errors; 1 pre-existing warning on 潜る |
| validate | 0 errors |
| unittest | 439 tests OK |
| linkplan | 0 problems |
| kanji-remarks | 0 problems (remark-only edit to 潜) |
| manifest | unchanged; tree clean |

## Verdicts

- **Correctness:** CLEAN
- **Scoped coverage:** CLEAN
- **Consistency and quiz safety:** CLEAN
- **Comprehensibility:** CLEAN

## Confirmation

CONFIRMED

## Findings

None. I found no new established defect in the revised hunks.

## Optional

1. **Add a ん + /p/ example to the compound-sound-changes article.**
   - The article names the h-row → p-row change, but it illustrates the change only after small っ, in the section "Small っ plus /p/".
   - It never shows /p/ after ん. That is the case in 潜伏 せんぷく (the 潜 Notes link) and in the already published 輩 (先輩).
   - The link therefore names the change but only partly explains it.
   - Suggested remedy: add one ん example, for instance 先輩 せんぱい or 散歩 さんぽ. This is not a regression in this batch.
2. **Revisit the 中心 exclusion on 仁.**
   - It is the weakest of the four: "center; core; focus" against the sense "kernel".
   - 中央 "center; middle" remains in the tie. This is an inconsistency only, because neither word is a correct answer for 仁.
3. **The 甲乙 exclusions 対照 and 差 are loose.** They do no harm and need not change.

## Limits

**Not independently verified:**
- That 甲乙 has no other JMdict reading or entry: I relied on word-quiz.txt and the audit's report of 0 attested problems, because the jisho.org fetch rendered no results.
- That 甲乙 names the two parties together in contract boilerplate: I saw only a search snippet. The article's claim is plausible but not verified against a source.

**Read only partly:**
- The 仁 tie of ~1409 words: keyword scan only, not every line.
- `corpus-attested.txt` and `distractor-use.tsv`: not opened in detail.
- `WordQuizViewModel.kt`: not opened. My view of the word quiz comes from `Words.kt`, `QuizBuilder.kt` and the audit.

**What the audits cannot show:**
- A reading equal to an attested reading that no source lists.
- Whether a distractor is semantically correct. That needs a human reading of the titles, which I did for the changed sets.
- Behaviour after an app-side change to ReadingOptions, which is deferred.

**Not done:**
- I did not run the JVM tests.
- I did not scan the corpus for dangling links, because corpus scans are forbidden. I relied on `link-targets.tsv` and `linkplan.txt`.
- The manifest is outside my content review.

**Process:**
- I made exactly one tool call per response and no parallel calls.
- A few single PowerShell calls combined several read-only commands, for example reading several small check files at once or parsing several JMdict entries.
- I created no helper scripts or temporary files.
- I wrote only this report.
