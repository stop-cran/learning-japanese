## Snapshot
**b1a28f8a42d8b45be7452d65242454bbe63c8ee3**, parent 36f7c0c4bdb997b4d2939cb191ee6cfe43a58cdb, which is the snapshot of my initial review. I reviewed committed content only, as supplied verbatim in the prompt. I made no tool calls, so I could not check Git state, commit identity, either sha256 value (`coverageIndexSha256` in `docs\n2-vocabulary-snapshot.json`, or the public-capture hash) or the diff's fidelity. The author ran those checks; I did not.

**Final: ACCEPT.**

## Scope
**Model:** claude-opus-5.5 (Claude family). This continues my original batch-85 review session. It is a post-fix confirmation, and it is not blind: I have now seen GPT's report and the author's adjudication. It is not a fresh independent review.

**Tools this turn:** none. Every judgment below rests on prompt-supplied text, plus my memory of earlier reads where stated.

**Evidence supplied in this prompt:**
- The correction diff, the author's adjudication and both original reports.
- All twenty mappings, earlier closed row N2:530 and the index semantics.
- All twenty current word bodies.
- Full bodies of `kanji\紅.md`, `kanji\燃.md` and `kanji\缶.md`.
- All 34 component records.
- Principal families plus corrective families 1002770, 1003450, 1006380, 1073570, 1221130, 1247470, 1293990, 1309950, 1328890, 1342540, 1379730, 1488820, 1599420 and 2646830.
- Twelve older bodies: きつい, 訓練, 指導, おしゃれ, スマート, 初め, 最初, ずっと, なかなか, 機能, 種類, 標本.
- All 411 lines of the public capture.

**What I actually read with tools earlier (initial review):**
- 21 principal families and 2 older bodies (注ぐ, 初め).
- `public-bodies.txt` lines 1–408 only. My initial report listed this under "Complete reads", which was wrong: the file has 411 lines. Lines 409–411 add Daijisen's historical third 役者 sense, 役人. That sense is outside JMdict 1538010 and does not conflict with the article ("does not make every person with an assigned duty an actor"), so no verdict changes.
- The author's cumulative volumes (340 families / 721 senses / 153 older bodies) are the author's work, not mine.

**Execution interruptions (initial review):** these were scheduling failures, not review content.
- First, three views were issued together, so that attempt produced no review.
- Later, a reread of 盛る and a mapping grep were issued together. Neither completed.

**Incidental context:** the TSV diff context showed adjacent pending rows N2:1702–1703. I did not use them.

**Dictionary authority:** the public capture is a single dictionary, Daijisen via Weblio, and its sense numbering differs from pinned JMdict.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1682 | words\モダン.md | CLEAN | CLEAN | CLEAN | B85-F3 resolved: guards for おしゃれ and スマート added |
| N2:1683 | words\餅.md | CLEAN | CLEAN | CLEAN | Unchanged; 餅 has no kanji card and is correctly unlinked |
| N2:1684 | words\もったいない.md | CLEAN | CLEAN | CLEAN | Unchanged; senses 1–2 taught, sense 3 distinguished |
| N2:1685 | words\モデル.md | CLEAN | CLEAN | CLEAN | B85-F1 resolved: を/に roles now correct |
| N2:1686 | words\元々.md | CLEAN | CLEAN | CLEAN | B85-F4 resolved: 初め and 最初 guarded; translation improved |
| N2:1687 | words\物置.md | CLEAN | CLEAN | CLEAN | Existential translation fixed |
| N2:1688 | words\物語る.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1689 | words\物差し.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1690 | words\物凄い.md | CLEAN | CLEAN | CLEAN | B85-F2 resolved: neutral wording; きつい added and ずっと removed |
| N2:1691 | words\モノレール.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1692 | words\紅葉.md (もみじ) | CLEAN | CLEAN | CLEAN | Unchanged; N2:530 now supports the earlier-row sentence |
| N2:1693 | words\揉む.md | CLEAN | CLEAN | CLEAN | F85-01 and F85-02 are GPT's IDs; F85-02 resolved here: 訓練 and 指導 guarded |
| N2:1694 | words\燃やす.md | CLEAN | CLEAN | CLEAN | Unchanged; もす correctly assigned to 燃す |
| N2:1695 | words\催し.md | CLEAN | CLEAN | CLEAN | Unchanged; 機能 guard justified by the article's own "function" gloss |
| N2:1696 | words\盛る.md | CLEAN | CLEAN | CLEAN | B85-F5: sense 3 now direct; slang labelled additional |
| N2:1697 | words\問答.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1698 | words\やかましい.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1699 | words\夜間.md | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1700 | words\薬缶.md | CLEAN | CLEAN | CLEAN | Body unchanged; additional sense 1605370:2 now in TSV and mapping |
| N2:1701 | words\役者.md | CLEAN | CLEAN | CLEAN | Unchanged; capture lines 409–411 are outside scope |

**Kanji and baseline preservation: CLEAN.** The supplied 紅, 燃 and 缶 bodies match my initial understanding.
- **紅.md:** unchanged. Line 40 links 紅葉 as こうよう, and its metadata cites 1578780.
- **燃.md:** links 燃やす and lists 1582900. It correctly assigns もす to 燃す.
- **缶.md:** links 薬缶 in its カン row and Common words, and lists 1605370.
- No kanji file changed after the initial review.

**Components: CLEAN.**
- All 21 distinct Han characters in the primary written forms appear in the word metadata.
- The 16 that have cards are linked.
- 餅, 凄, 揉, 催 and 盛 have no cards and are not linked.
- The kana headwords (もったいない, やかましい, モダン, モデル, モノレール) correctly have `kanji: []`.
- No もみじ component readings are invented.

**Reciprocity: CLEAN.** 燃↔燃やす and 缶↔薬缶 link both ways, and 紅↔紅葉 is preserved.

**Mappings: CLEAN.**
- The twenty mappings agree with the TSV. N2:1700 now has `additionalSenses` 1605370:2, consistent with the index definition ("separately distinguished entry:sense pairs").
- N2:530 keeps 1578780/こうよう, with its raw maple gloss qualified and 2857870:1,2 as additional senses.
- N2:1692 independently supplies 2857870/もみじ, with no merge.

## Findings
No new actionable defect was found in the changed passages. Status of earlier items:

**My initial findings**
- **B85-F1 (モデル.md:28–29): RESOLVED.** The text now says: "Use **Xをモデルにする** … を marks the person or thing used as the model, and に marks the role モデル." This is accurate. I accept recalibrating the severity to minor because the defect was localized. Confidence: high.
- **B85-F2 (物凄い.md:29–30): RESOLVED.** The text now says 物 "writes the もの part … Learn the expression as a whole rather than assuming a fixed meaning for もの-." I also correct my own initial claim: the classical sense 3 (何となく恐ろしい) does not establish my suggested "somehow/vaguely" derivation either. The neutral wording is correct. Confidence: medium-high.
- **B85-F3 (モダン.md:9): RESOLVED.** おしゃれ (1002770:1 "stylish") and スマート (1073570:1 "stylish") directly overlap with モダン's title "modern; stylish". Neither older body declares the pair. Confidence: high.
- **B85-F4 (元々.md:9, :21): RESOLVED.** 初め (1342540:1 "outset") and 最初 (1293990:1 "beginning, outset") overlap with 元々's "from the outset". The 最初 body teaches 最初から and 最初は. I agree with adding 最初, a check I had left open. Confidence: high.
- **B85-F5 (盛る.md:24–31): RESOLVED, and my original severity was overstated.** The pre-fix article already taught sense 3 with 一服盛る, a reading and an English meaning. The defect was framing ("The dictionary also records…"), not missing coverage. I accept the author's "optional clarity" classification and the retained "exaggerate" in the title, since the body now labels it additional slang. The revised text matches Daijisen もる sense 3 (調合…与える…毒を飲ませる) and sense 6.

**GPT's findings**
- **F85-01 (物凄い.md:9): VERIFIED RESOLVED.** 1003450:3 ("intense") and :5 ("extreme"), plus the きつい body's teaching about intensity, overlap with 1502630:1. Confidence: high.
- **F85-02 (揉む.md:9): VERIFIED RESOLVED.** 1567610:4 ("train, coach") and Daijisen もむ sense 6 (相手になって教えてやる) overlap with 訓練 ("training; drill") and 指導 ("…coaching"). The 揉む body itself names training among its further uses. Confidence: high.

**Items from my Limits and Optional sections**
- **薬缶 metadata (TSV line 1701 / N2:1700): RESOLVED.** Confidence: high.
- **紅葉 earlier-row sentence: RESOLVED** by the supplied N2:530 row. This rests on prompt-supplied text, not my own TSV read.
- **Translations (物置.md:21, 元々.md:21): APPLIED.** Both are accurate.

**Over-guard dispositions**
- **物凄い→ずっと removal: AGREE.** 1006380:2 is comparative degree ("much more"), and the ずっと body teaches ずっと軽い, not plain "tremendous".
- **Withdrawals I accept:**
  - なかなか, via 1599420:1 "very/considerably/highly".
  - 揉む→問答: Daijisen もむ sense 5 激しく議論 and 問答 sense 1 また、議論すること are direct, not via a chain.
  - 催し→機能: the 催し body itself glosses the event as a "function".
  - モデル→種類 and →標本: overlap through 標本 sense 2 "example, type" and モデル's display-sample, exemplar and 型式 senses.
- These are conservative choices and do not block acceptance.

## Optional
- **モデル.md:** a full sentence for the construction would help, e.g. 作者は祖父をモデルにして主人公を書きました.
- **モダン.md:** one sentence in Synonyms contrasting おしゃれ and スマート would explain the new guards.
- **盛る.md:4:** the title could favour selected senses (e.g. "dish up; heap up; dose") over the additional slang. The author's retention is acceptable.

## Limits
- **Supplied evidence:** all current bodies, families and older bodies came as prompt text. Their match to commit b1a28f8 is author-asserted, and no Git, hash or file verification was possible.
- **Not blind:** this confirmation was made after seeing GPT's report and the author's adjudication, which may have influenced it.
- **Single dictionary:** the public evidence is one dictionary, and its numbering differs from pinned JMdict.
- **Quiz guards:** completeness is not certified. My title searches in the initial review did not cover "rice cake", "cake" or "train", and I have not run the quiz builder.
- **Historical source questions** remain unresolved. Neither affects the current teaching, which handles both explicitly:
  - Why the compiler paired こうよう with "maple" in N2:530 is unknown; the article says so.
  - The historical meaning of もの- in 物凄い is unestablished; the article now avoids claiming it.
- **Scope of CLEAN:** CLEAN means no actionable defect found within this scope. It is not exhaustive correctness or native-speaker certification.
