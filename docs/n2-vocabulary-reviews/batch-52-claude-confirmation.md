## Snapshot
- **Corrected commit:** `960be0a8245a50449de9d40f98a6706c933e966e`
- **Parent:** `3d66845af7cc97508b6a8d4348f0792e2cbdb9c6`, the authored snapshot. Its own parent is `ba5b4d4cb75a542fe74572dfb1efff1fe0788693`.
- I reviewed committed content only. File tools can't run Git, hash or cleanliness checks, and I didn't inspect `.git`. The commit IDs, hashes and the claim that nothing else changed are all the author's checks.

## Scope
- **Model:** claude-opus-5.5, Claude family. Read-only; no edits, agents or delegation.

**Read again in full this pass**
- `correction-snapshot.json`
- The whole `correction.patch`
- `correction-comparisons-compact.txt`: all 27 families / 71 senses
- `correction-existing-reading.txt`: 16 old word bodies plus the 魚 kanji card
- `corrected-review-evidence.json` lines 25420–25860. This is the whole `correctionEvidence` section, including current, added and removed declarations, the adjudications and the limits.
- All eleven changed articles
- The 20 TSV rows N2:1022–1041
- `docs\content-format.md` lines 84–98, the quiz-exclusion rules

**Targeted checks this pass**
- In `words\`: titles and exclusions for 開く, 開ける, 一つ, 級, 位, 小説, 映画, 物語, 話, 判断, 決定, 欠点, 欠陥, 弱点, 苦手 and the 付く/集まる/始まる verb pairs.
- A search of every `words\` card for exclusions naming any changed title.
- In the six kanji cards: reciprocal links and metadata fields.

**Inherited from my initial full reads (not reread)**
- The nine unchanged articles: 短期, 炭鉱, 断水, 団地, 誓う, 地下水, 近寄る, 千切る, 地質.
- The full bodies of the six kanji cards. This pass only spot-checked them by search.
- The private mappings, principals, components and labels files, `principal-reading.txt` and `public-bodies.txt`.

**Not read in either pass:** the nine `family-inspection-0N.txt` renderings, `public-bodies.json` and `review-evidence.json` outside the correction section. I made no fresh web fetches.

## Verdicts

| Source ID | Article | Read basis | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1022 | words\足る.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1023 | words\段階.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1024 | words\短期.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1025 | words\炭鉱.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1026 | words\短所.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1027 | words\たんす.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1028 | words\淡水.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1029 | words\断水.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1030 | words\単数.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1031 | words\団地.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1032 | words\断定.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1033 | words\短編.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1034 | words\誓う.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1035 | words\地下水.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1036 | words\近々.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1037 | words\近付ける.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1038 | words\近寄る.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1039 | words\力強い.md (new) | Fresh full reread, corrected | CLEAN | CLEAN | CLEAN |
| N2:1040 | words\千切る.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |
| N2:1041 | words\地質.md (new) | Inherited initial full read; unchanged | CLEAN | CLEAN | CLEAN |

**Kanji edits and reciprocity: CLEAN.** I'm inheriting my initial full reads of the six cards. This pass's search confirmed each of the eight pairs at its whole-word reading in both the reading table and Common words:

| Kanji | Word | Reading | Lines |
|---|---|---|---|
| 階 | 段階 | だんかい | 30, 36 |
| 短 | 短所 | たんしょ | 28, 35 |
| 短 | 短期 | たんき | 28, 36 |
| 短 | 短編 | たんぺん | 28, 37 |
| 炭 | 炭鉱 | たんこう | 28, 34 |
| 鉱 | 炭鉱 | たんこう | 30, 37 |
| 団 | 団地 | だんち | 30, 40 |
| 編 | 短編 | たんぺん | 30, 39 |

The jlpt, strokes, radical, onyomi, kunyomi and distractors fields are all present. The patch doesn't touch `kanji\`.

**Baseline preservation: CLEAN.** The patch changes only new articles, and the evidence records `baselineQuizExclusionChanges: {}`. No baseline card declares an exclusion naming any of the 11 changed words.

**Mappings: CLEAN.** I searched the TSV rows again and they're identical to the initial review, with the same entries and selected/additional senses. The evidence records `mappingChanges: {}`.

## Findings

**Dispositions of my original findings**
- **B52-01** (Minor, correctness; the 淡水 reading explanation): **Resolved.** 淡水.md:25 now reads "using 魚's on reading ギョ" and keeps たんすいぎょ. The kanji card for 魚 and the word 金魚 (きんぎょ) confirm ギョ is the ordinary on reading. No voicing claim remains.
- **B52-02** (Minor, excess guard 力強い/がんがん): **Resolved.**
  - 力強い.md:9 has 11 guards and no longer includes がんがん.
  - JMdict 1040570:3 ("vigorously; flat out") still exists, but the がんがん title "loud banging; a pounding headache" isn't a reasonable answer for "powerful; reassuring", or the reverse.
  - I keep the 頼もしい, 確か, 確実 and しっかり judgments; no defect was established for them.
- **B52-03** (Minor, links to existing words): **Resolved.**
  - 足る.md:40 now has `[不足](不足.md)する`.
  - 近々.md:41 now has `[遠く](遠く.md)`.
  - たんす.md:45 now has `[押入れ](押し入れ.md)`. JMdict 1589110 lists 押入れ and 押し入れ as one entry, and the 押し入れ article says "押入れ is another normal spelling."
- **Initial optional 10分:** adopted at 短編.md:21 with じゅっぷん kept. It's a clear duration and not a regression.

**My initial qualification that the four 近付ける exclusions were justified: revised. I accept the removal, with medium confidence.**
- content-format.md:95 requires an exclusion when either title is a reasonable answer for the other word.
- The 開く/開ける precedent (開く.md:3, 開ける.md:9) shows that a transitive/intransitive pair can need a guard. In that pair, though, both titles use the same English verb, "open".
- Here the titles separate the meanings in their wording. "Bring close; let approach" (bring something closer, or allow someone near) differs from:
  - 近寄る "approach; draw near"
  - 寄る "draw near; stop by"
  - 接近 "approach; drawing close"
  - 迫る "approach; press for"
- 迫る's transitive sense 1475720:2 means press, urge or compel, not bring close.
- 近寄る's body teaches the 近付ける contrast directly, so seeing both in one quiz tests a taught distinction.
- No remaining declaration covers these pairs: 近付ける has no exclusions, and no card names it.
- This is an editorial judgment, not a defect in either direction.

**Added guards: no excess established**
- **段階/クラス:** supported by the old クラス body ("category or rank") and sense 1419950:2. It matches the existing 級 card's exclusions `[位, クラス]`.
- **短所/粗:** supported by 1586730:2 ("flaw, esp. of a person") and matches the 弱点 card, which also excludes 粗.
- **単数/一:** 1417670:1 means "single; one", and 一つ doesn't protect the 一 pair, since exclusions aren't transitive.
- **断定/審判:** 1360410:1 covers judgment, decision and verdict, and the 審判 card already excludes 判断.
- **短編/詩:** this is the most borderline. The title "short story; short film" doesn't mention poems, but the article's Meaning section and 1597300:1 include short poems, and the guard only removes one distractor. Acceptable.

**Regression checks: none found**
- Every guard line in the 11 changed articles matches `currentQuizDeclarations` exactly. 近付ける's front matter is still valid without the exclusions line.
- The totals of 14 guarded cards and 72 guards add up from the evidence lists. I didn't search the three unchanged guarded cards (短期, 誓う, 近寄る) again.
- The three new links point to existing files.

**New defects:** none.

## Optional
These are not blocking:
- A brief 足るを知る idiom note. It is backed by Daijisen sense 2; noun+に足る is not, so I'd leave that out.
- A 神に誓う example on 誓う.
- An alternative 地下水 sentence using から.

I withdraw my earlier optional suggestions about splitting 千切る (the article already rejects a productive 千=ちぎ), 短所/下手, 段階/程度 and 団地/住宅/アパート. I agree with the author's reasons for not changing those.

## Limits
- I can't run Git, hashes or cleanliness checks, so "no other files changed" is the author's assertion.
- I didn't read the nine family-inspection renderings or `public-bodies.json`. Dictionary support relies on the compact 27-family file and the author's Daijisen captures. I made no fresh public retrievals.
- The nine unchanged articles and the full bodies of the six kanji cards are inherited from my initial reads, not reread.
- Some guard calls are judgments, not certainties: 段階/クラス, 短編/詩, 近付ける without guards, and 確か/確実/しっかり.
- There was no live quiz run and no native-speaker certification.
