I've finished reading every assigned resource. The review is below.

```text
Snapshot: Frozen signed snapshot 07b359ca4fb55dbcb7623ee96c71c958385d28b8, as supplied. No uncommitted teaching
  was included. I could not check Git independently because I had no shell, so the commit identity and signature
  are taken from the prompt.

Scope: I am Claude Opus 5.5 (claude-opus-5.5). I was a single reviewer working without delegation.
  - New teaching files: kanji\匁.md (1-47) and words\匁.md (1-34). Both were reviewed for correctness, scoped
    coverage and comprehensibility.
  - Dictionary families: all 3 lexical families in batch-051-jmdict.xml (1488550 百匁, 1536280 匁/文目,
    2840989 花一匁). All 18 comparison families in batch-051-comparison-jmdict.xml (1-676).
  - Comparison cards and articles, used as context only: kanji 久, 文, 目, 包; words グラム, 目, 文, 包む, 円.
  - Guidance files: copilot-instructions (1-259), content-structure (1-85), content-format (1-180),
    jlpt-levels (1-160).
  - Raw KANJIDIC2 JSON (1-58) and KanjiVG 05301.svg.
  - Supplied saved pages: Daijisen 匁 and め (one truncation recovered), Kotobank (Nikkoku, Nipponica,
    Sekai Daihyakka) and Kanjipedia.
  - Extra scoped searches: docs\confusable-words.md, plus a title and file inventory of kanji/words to look
    for competing unit or money titles.

Verdicts:
  kanji\匁.md — correctness NEEDS FIX; scoped coverage CLEAN; comprehensibility CLEAN.
  words\匁.md — correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN.

Findings:
  1. Minor; correctness (qualified claims / flags local to one dictionary sense); kanji\匁.md:31, 41.
     Claim and impact: The め row teaches 百匁 ひゃくめ and reports only JMdict's "archaic" flag. It leaves out
       two things:
       - JMdict 1488550 marks the reading ひゃくめ "word containing irregular kana usage" and cross-references
         百目.
       - Nikkoku defines the shortening as 略して「目(め)」. Daijisen 目 [接尾] sense 4 gives 「百目」「一貫目」
         with the meaning 匁.
       As written, a learner may think 百匁 = ひゃくめ is an ordinary spelling–reading pair, and that the shortened
       unit is normally written 匁. Line 41 ("Learn 百匁 as the documented whole expression") reinforces this.
     Remedy: Add the irregular-kana qualification. State that the shortened unit め is usually written 目
       (百目 ひゃくめ). Keep め in the metadata, supported by KANJIDIC2 and Kanjipedia (訓 もんめ・め).
     Evidence: batch-051-jmdict.xml lines 8-18; batch-051-me.html line 1888; batch-051-kotobank-monme.html
       sense ①; batch-051-kanjipedia.html onkunList.
     Confidence: high that the flag and the usual 目 spelling are omitted. Moderate on learning impact, because
       the row already limits め to recognition and the Notes warn against productive substitution.

  Checked with no defect:
  - Metadata matches KANJIDIC2 2026-306: 4 strokes, radical 勹 no. 20, grade 9, no on'yomi, kun もんめ then め.
    quizOnyomi [] and quizKunyomi [もんめ] are correct, and the もんめ row has its own linked word example.
  - The KanjiVG breakdown (勹 plus crossing strokes) agrees with the shape description.
  - The mnemonic is clearly labelled as not etymology.
  - The 3.75 g value matches Nipponica, Sekai Daihyakka and Kanjipedia (Daijisen says 約).
  - Current pearl-trade use is confirmed by Daijisen and Nipponica.
  - The silver-money rate varied by period and market (Nikkoku ②).
  - Word article: "mass sense restricted to the spelling 匁" matches the stagk; the historical-term sense is
    kept separate.
  - Example sentence: 1匁は3.75グラムです and its reading いちもんめはさんてんななごグラムです are correct.
  - Distractor titles are distinct from monme: 久 "a long time", 文 "sentence, writing", 包 "wrap; enclose".
    Their stroke counts (3, 4, 5) and the shared 勹 radical with 包 are stated correctly.
  - No existing kanji title for a mass unit or ryō-type currency competes as a fallback answer. 貨 and 金
    titles stay distinguishable.
  - Word titles "gram" and "yen; circle" are not acceptable answers for 匁, so no exclusion is needed.
    confusable-words.md has no entry for 匁 or グラム.
  - The required 匁 kanji → 匁 word link pair exists in both directions with the reading もんめ.
  - No vocabulary JLPT level is inferred.

Optional:
  - Kanjipedia (Kadokawa Shinjigen) explains 匁 as 文 (もん) plus katakana メ. Nipponica gives a different
    account (a cursive form of 泉). A hedged, sourced mention could help learners and would add to the 文
    comparison. structure-unclassified remains appropriate.
  - kanji\匁.md:24 says 勹's "shape differs from the standalone radical". In KanjiVG, strokes 1-2 form an
    ordinary 勹. The real visual point is that the crossing strokes stick out beyond the outline. Consider
    rewording or dropping the clause.
  - words\匁.md:32 could note that the shortened め is usually written 目.
  - The words article could mention the 文目 spelling (historical sense) and the "weight of one mon" origin.
  - type: wago is a framework-dependent label: もんめ comes from 文目, which mixes the on-reading 文 with
    native め. Recording the rationale is optional; a change isn't required.
  - 花いちもんめ could be added for recognition.

Limits:
  - Dictionary pages were supplied saved copies, not freshly retrieved. I made no web_fetch calls.
  - batch-051-me.html 1792-1888 was truncated at line 1876; I recovered 1877-1888.
  - The confusable-words check was a scoped search only. It does not certify semantic fallback across the whole
    corpus.
  - Textual review only: no native-speaker, device or physical-phone evidence, and no certification of glyph
    rendering. Compatible Android f9b59a2+, physical-phone and general-release acceptance remain outstanding.
  - I made strictly one tool call per response. This is my own observation, not an execution record.
  - I could not independently verify the Git snapshot.
```
