# Batch 106: rendered confirmation, execution 829 (bounded recovery, original session)

**Summary:** I found no defects in the three teaching units or in the answer choices actually offered. All nine verdicts are CLEAN. The 勅/訓 hypothesis stays open but does not block. Every view call in this run was a single serial call, including each font panel.

## Snapshot
- **Model and session:** claude-opus-5.5, continuing original session 4304295f-1fe0-4f7a-a8c4-2db9b547857d.
- **Commits:**
  - Frozen signed evidence HEAD: 99522a889cdbd8d04f4a185d2fcfd69d5c7302bb.
  - Common evidence snapshot: 12ae2584f0d92703706833a629f5406ed87ad9c1.
  - Teaching snapshot: 5fe224b5c611e8ca0c7c5a1fcbd5ea4a025e606a. The teaching is stated to be unchanged since then.
- **SHA verification:** I could not check any SHA, commit or hash. Only `view` was available, so these values are as supplied.
- **Relation to execution 828:** this is a new, standalone, compliant confirmation. Execution 828 and its report stay rejected and unchanged. I do not accept them retroactively.

## Scope
**Read fresh in this execution (one serial call each, in this order):**
1. `docs\n1-reviews\batch-106-initial-claude.md` (my original report), in full.
2. `docs\n1-reviews\batch-106-rendered-828\claude-report.md` (the rejected report), in full, as context only.
3. Initial packet `control\batch-106-rendered-827-n1-reviews-batch-106-initial-packet.txt`, lines 1815–1895. This range contains the complete XML entries 1430550 勅令, **1430560 勅諚/勅定**, 1597670 勅使 and 1604470 詔/勅/御言宣.
   - **Discrepancy:** the intervening entry in this range is 1430560, not 1432920 as the instruction stated.
   - Read through the closing tag of 1604470. Spellings, readings and restrictions are listed in the 1604470 bullet below.
4. Host KANJIDIC2 (`…host-823-sampled-kanjidic2.xml`), full read. It reaches `</kanjidic2>` with no truncation.
5. Native KANJIDIC2 (`…native-only-kanjidic2.xml`), full read: 扱/芋/獣/剰/矛. No truncation.
6. Host JMdict (`…host-823-sampled-jmdict.xml`), full read. It reaches `</JMdict>`. It includes 1956150 訓, 1236890 教え/訓え, 1430550, 1532160, 1531950/1531970, 1517150, 1517480, 1438050 and 1223021.
7. Native JMdict (`…native-only-jmdict.xml`), full read. It reaches `</JMdict>`.
8. `n1-106-font-panel-1.png`.
9. `n1-106-font-panel-2.png`.
10. `n1-106-font-panel-3.png`.

The tool showed each image as a 900×2000 rendition.

**Inherited from execution 828 (serial reads there; not reread here):**
- The common packet (6123 lines), source-access.json and image-manifest.json.
- The 23 non-font PNGs:
  - quiz screens: meaning-question/feedback, curated-on-question/feedback, curated-sole-on-done;
  - drawing screens: drawing-trace/feedback/recall-feedback;
  - article viewports 00, 02, 05, 06, 11, 12, 14 and 17;
  - word-0-01 and word-0-08;
  - pair-0-components, reused-令-new-line, selection, all-selection and preinstrumentation.

**Duplicate and unviewed screenshots:**
- Duplicates by hash:
  - article-03 = 02;
  - article-07 and 09 = 05;
  - article-08 and 10 = 06;
  - article-16 = 14;
  - article-18 and 19 = 17;
  - word-0-02/03/04 = 01;
  - word-0-09/11/12/13 = 08;
  - word-0-06 = pair-0-components.
- I did not view these indices: article-01/04/13/15 and word-0-00/05/07/10. I make no claim about them.

**Not done:** no fresh full initial review, no Git or upstream retrieval, no shell.

## Fresh source facts used
- **1604470:**
  - Kanji forms: 詔 (spec1), 勅 (ichi1/news2/nf36), 御言宣.
  - みことのり has no restriction. ちょく is restricted to 勅, and しょう to 詔.
  - Single sense: imperial decree / imperial edict.
- **1430550 勅令 / ちょくれい:** unrestricted noun, "(imperial) edict".
- **KANJIDIC2 勅:**
  - Radical 19, 9 strokes, frequency 2157.
  - On reading チョク; kun readings いまし.める and みことのり.
  - English meaning: "imperial order".
- **Native-only characters (KANJIDIC2 and JMdict):** 扱 (handle/entertain/thresh/strip), 芋 (taro/yam/tuber), 獣 (animal/beast), 剰 (surplus/besides) and 矛 (halberd/arms/festival float).
  - Their full JMdict families have no sense of an order, a decree or a sovereign.
  - 扱く/しごく "work someone hard" and 扱う (archaic) "mediate" are not senses of an order or decree.
- **訓:**
  - KANJIDIC2 meanings: instruction, Japanese character reading, explanation, read.
  - JMdict 1956150 sense 2: precept/lesson/one's teachings (cross-reference 処世訓).
  - JMdict 1236890: 訓え is a rarely used form of おしえ (teaching/precept/doctrine).
  - None of these is an imperial or sovereign order.
- **Curated wrong choices:** 束 (bundle; its secondary senses govern/manage/control are not "order"), 効 (merit/efficacy) and 勤 (diligence/serve). None means "imperial order".

## Verdicts
| Unit | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| kanji\勅.md | CLEAN | CLEAN | CLEAN |
| words\勅令.md | CLEAN | CLEAN | CLEAN |
| 令.md changed line 37 | CLEAN | CLEAN | CLEAN |

**Answer choices actually offered (meaning and rendering): no defect found within the recorded contexts.**
- **Contexts covered:**
  - the default N1 meaning question, with choices 畔 "paddy boundary; waterside", 剰 "remainder; surplus amount", 俸 "salary; stipend" and 勅 "imperial order";
  - All/custom with the curated wrong choices 効/束/勤;
  - the recorded random N1 subset 冒/冶/倣/僚/蛍/蛇/剤;
  - the native random offers 扱/芋/刑/准/冒/獣/凝/矛;
  - both directions of the 勅令 word quiz.
- **Why the choices are safe:** no offered wrong choice has an ordinary secondary sense that also means "imperial order".
  - 刑, 劾 and 僚 share only a legal or official topic with the target.
  - 命/令/命令 are broader than the target and are handled as comparisons.
- **Readings:** チョク is the only selected reading. いましめる and みことのり appear in the feedback as reference text only.
- **Rendering:** the font panels and the other screenshots show the content. This is emulator evidence only; it is not a universal future-pool, phone or font-face certification.

## Findings
**Proved defects:** none.

**Reconciling my original findings:**
1. 勅.md:35 "practiced as ちょく" vs the チョク display: **partially resolved / optional.** The screens show the key ちょく displayed as チョク. The wording could still mention the katakana.
2. 勅.md:46 "overlap… with 勅": **optional, unchanged.**
3. Standalone 勅, the old form 敕, and 勅命/詔勅: **optional, unchanged.**
   - 1604470 supports ちょく as a reading restricted to 勅.
   - 1430560 also supplies 勅諚/勅定.
4. The 令.md:44 footer lacks 1430550: **optional, unchanged.** The rendered footer is confirmed to still read 1517500 / 1532160 / 1556190.
5. 勅/訓 hypothesis ("instruction/precept" could be confused with "imperial order"): **unresolved, nonblocking, weakened.**
   - Severity: low. Facet: distractor safety. File: kanji\勅.md (fallback pool).
   - Evidence: 訓 sense 2 means a moral precept or teaching and has no command or sovereign sense. The target label's word "imperial" separates the two. 訓 appeared only in the 32 explicit unguarded hypothesis fixtures, never in real offers.
   - Remedy: none is required, and I propose no guard.
   - Confidence: medium.

## Optional
- The feedback line shows the raw, unselected kun readings, including いましめる. This is app-wide display behaviour, not a defect in this batch. A modern written example of いまし.める remains unverified.
- Items 1–4 above.

## Limits
- **Verification:**
  - no Git, SHA or upstream verification;
  - the dictionary text comes only from the supplied projections;
  - the entry-ID discrepancy (1432920 stated, 1430560 actual) is recorded under Scope.
- **Rendering:**
  - **Font panels:**
    - Panels 1 and 2 together show the 17 scoped Han characters plus 訓 (18 in total) in the Gothic, Mincho, Textbook and Brush rows.
    - Panel 3 repeats 勅/束/効/勤/力/令/命/訓 and the whole word 勅令.
    - No row is separately labelled as the default system font. The only default-UI Han is 訓 in the header and caption.
  - The images were 900×2000 tool renditions of 1080×2400 emulator originals. That gives no original-pixel, physical-phone, fallback-face or native-speaker certification.
  - The reading table scrolls sideways, so I make no claim about columns I did not see.
- **Drawing:** the trace is ungraded, nine reference strokes were injected, the handwriting model was unavailable, and the recall screen reveals the answer. These show only that the mechanics work, not handwriting recognition or mastery.
- **Not claimed:**
  - an exhaustive future pool;
  - measured learning effectiveness;
  - phone, general-release or whole-project acceptance;
  - acceptance of execution 828.
