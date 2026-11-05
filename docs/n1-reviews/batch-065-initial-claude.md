I found one actionable problem: `words/倹しい.md` has no quiz exclusion against 謙虚, even though the two titles overlap on "modest". The other three teaching files are clean within the assigned scope. I made no edits, and this is the complete original review.

```text
Snapshot: Supplied as signed frozen 5da89bd73eff6a195ee0004762e6eced2b77c15c in C:\Users\stop-\n1-kanji-workspace\learning-japanese. I had no shell or git access, so I could not independently confirm HEAD, the signature or whether uncommitted changes exist. I reviewed the working-tree files as they read during this session.

Scope: Model: Claude Opus 5.5 (claude-opus-5.5), one reviewer. All reads were serial, one tool call per response. I read every assigned range completely:
- Teaching files: kanji\倹.md 1-59, words\倹約.md 1-53, words\倹しい.md 1-52, and kanji\約.md 1-51 (only the added Common words line was reviewed).
- Frozen JMdict: batch-065-jmdict.xml 1-244 (all 15 lexical families) and batch-065-comparison-jmdict.xml 1-283 (all 9 comparison families: 経済, 質素, 節約, 貯金, 浪費, 贅沢, 慎ましい, けち, 約やか).
- Frozen KANJIDIC2: batch-065-kanjidic2.xml 1-436 (all 6 raw records: 倹, 検, 険, 人, 値, 約).
- Comparison cards: kanji 険, 験, 値, 人; words 節約, 地味, 経済, けち, 謙虚, 謙遜, 無地, 簡単, 単純, 贅沢, 貯金 (all full assigned ranges).
- Strokes and guidance: strokes\倹.json, the pinned SVG n1-05039-70a0b7ae.svg 1-78, copilot-instructions 1-259, content-structure 1-85, content-format 71-177/260-275/1389-1405, jlpt-levels 1-20/192-234/255-287.
- Targeted searches: titles/tags/distractors of the 11 legacy cards (人, 休, 何, 入, 出, 口, 女, 日, 月, 男, 買); docs\confusable-words.md for the relevant terms (no matching rows); and existing word titles containing frugal, thrift, econom, modest, saving, stingy, plain, simple, humble, conserv or sparing.
- Fresh Kotobank retrieval, all four assigned URLs:
  - 倹: Daijisen and 精選版 entries plus 字通 (常用 10画, older form 儉 15画, 字音 ケン, 字訓 つづまやか).
  - 倹約: Daijisen 名・形動・スル, with 小遣いを倹約する and a ―な生活 citation.
  - 倹しい: Daijisen 【▽倹しい／▽約しい】 つまし・い, glossed as 地味で質素, with 地味 listed among synonyms; 精選版 senses ① thrift and ② 地味/質素で控えめ.
  - 約まやか: the 精選版 つづま‐やか【約やか】 senses; the Daijisen section returned only its heading.

Verdicts:
- kanji\倹.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- words\倹約.md: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.
- words\倹しい.md: correctness NEEDS FIX (quiz-exclusion metadata); scoped coverage CLEAN; comprehensibility CLEAN.
- kanji\約.md, added line 39 only: correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

Findings:
1. Minor; correctness (quiz metadata); words\倹しい.md:4,8 against words\謙虚.md:4,9 and words\地味.md:9,36.
   Claim/impact: The new title "frugal; modest in one's living" and 謙虚's title "modest; humble" share the English word "modest". Neither card excludes the other. A learner could reasonably accept the wrong word in either direction, for example choosing 倹しい for "modest; humble", or "frugal; modest…" for 謙虚. This is the same English-overlap the repository already guards for 地味/謙虚: 地味.md declares 謙虚 and explains that "modest" covers both an attitude and a way of living. This is a direct pair; I am not inferring it through the 地味 exclusion.
   Remedy: Add 謙虚 to 倹しい's quiz_exclusions, or declare the pair on 謙虚. Do not change the title or meaning of either word to avoid the overlap.
   Evidence:
   - Actual displayed titles (above).
   - The 地味 precedent.
   - Kotobank 精選版 倹しい ② 質素で控えめ ("reserved").
   - JMdict 1255980 つましい glosses only thrifty/frugal/economical, so this is a quiz-label problem, not a meaning error.
   Confidence: medium-high.

Other checks that passed (no findings):
- Readings and metadata: ケン, つま.しい and つづまやか match the raw KANJIDIC order. Both practice selections have their own row with a linked word, and つづまやか is properly qualified as source-only. 10 strokes, radical 人 9 (shown as 亻), grade 8 and N1 match the raw record. SVG and JSON agree on 10 strokes. The mnemonic is labelled as non-etymological, and the older form 儉 is supported by 字通.
- 倹約: noun, transitive する verb and な-adjective; を marks the object; な attachment is correct. Examples, kana and translations are accurate. The ケン+ヤク split is correct, and the meaning aid is qualified.
- 倹しい: usually written in kana; 約しい is flagged rare; い-adjective forms are correct. つましい and つつましい are kept separate without inventing a strict split.
- Reciprocal links: all six directed links are present with correct readings (倹↔倹約, 約↔倹約, 倹↔倹しい).
- Quiz choices: 険, 験 and 値 are not defensible meanings of 倹; 検 is not offered. None of the 11 fallback cards' meanings overlaps "frugal; thrifty".
- Exclusions: the eight declared pairs are justified. No other missing guard was established against 節約, 経済, 地味, けち, 貯金, 贅沢, 無地, 簡単, 単純 or 謙遜.
- No word-level JLPT value is inferred for either new word.

Optional:
- kanji\倹.md:49 and words\倹しい.md:43 say つつましい is "often spelled 慎ましい". Frozen JMdict 2009010 marks both senses usually written in kana, which supports 慎ましい as a recognized spelling, not a frequent one. Wording such as "its kanji spelling is 慎ましい" would avoid an unsourced frequency claim.
- 倹しい and 謙遜 ("modesty; self-deprecation") overlap less, because 謙遜 is a noun about an attitude. An exclusion is at the author's discretion.
- 字通 classifies 倹 as 形声 with 僉 as the phonetic, and KanjiVG marks 僉. The card's choice of structure-unclassified with no phonetic claim is allowed; a sourced phonetic note could be added.

Limits:
- Git state and signature were not independently verified.
- Fresh Kotobank results: the Daijisen part of 約まやか returned only a heading (no definition). The 倹約 page was truncated inside the Daijisen synonym list after the definition and examples. Publisher attribution alone was not treated as evidence.
- JMdict and KANJIDIC2 evidence is the supplied frozen XML, not fresh retrieval.
- Larger, random or live quiz pools and the actual app behavior are unverified. Only the documented default four-choice fallback for the 11 named cards was audited.
- No native-speaker, device or physical-phone evidence was supplied. Phone-text readability does not certify rendering or stroke drawing. A native check is still needed for 倹, 儉, 険, 験, 値, 人, 亻, 阝 and any displayed comparison glyphs. Compatible Android f9b59a2 or later is required for curated readings, and physical-phone/general-release acceptance remains outstanding.
- No frequency or corpus measurements were made.
```
