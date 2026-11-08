# Batch 106 rendered confirmation (execution 828): 勅, 勅令 and the new 令 line

No defect is established. All nine verdicts stay CLEAN, and the real quiz choices are judged wrong for the target and target-safe (none means "imperial order"). One process breach: I viewed the three font panels in a single batch, not one call at a time. All other reads were serial.

## Snapshot
- **Evidence snapshot:** 12ae2584f0d92703706833a629f5406ed87ad9c1.
- **Frozen execution HEAD:** bef71a87216e8a220b5e0699547237d6d66fdb4a.
- **Teaching text:** unchanged from 5fe224b5c611e8ca0c7c5a1fcbd5ea4a025e606a.
- I could not run Git or compute hashes. So I did not verify any SHA, the evidence-only preparation commit, or the source-access hashes; all are taken as recorded.

## Scope
- **Model:** claude-opus-5.5. This continues my original session 4304295f-1fe0-4f7a-a8c4-2db9b547857d; it is not a fresh initial review.
- **Fresh full text reads:**
  - my original report `batch-106-initial-claude.md`;
  - the common packet, in one call with no truncation notice;
  - `source-access.json`;
  - host-823 `sampled-jmdict.xml` (885 lines);
  - native-826 `native-only-jmdict.xml` (701 lines);
  - `image-manifest.json`.
- **Families read in full this session:**
  - 訓 1956150, 教え/訓え 1236890, 勅令 1430550;
  - 命令 1532160, 命じる 1531950, 命ずる 1531970;
  - 法 1517150, のり 1438050, 法律 1517480, 規則 1223021;
  - all host-sampled word-choice families;
  - all native families for 剰, 扱, 獣, 矛 and 芋.
- **Inherited, not re-read:**
  - The 4833-line initial packet. Its contents, including みことのり 1604470 and 1597670, come from my original read.
  - Both KANJIDIC2 sample files. English character meanings come from the packet's host-823 projections.

**PNGs.** The 42 originals have 26 distinct hashes. I viewed one original for each hash:
- font-panel-1, 2 and 3;
- meaning-question and meaning-feedback;
- curated-on-question, curated-on-feedback and curated-sole-on-done;
- drawing-trace, drawing-feedback and drawing-recall-feedback;
- article-00, 02, 05, 06, 11, 12, 14 and 17;
- word-0-01 and word-0-08;
- pair-0-components and reused-令-new-line;
- selection and all-selection;
- preinstrumentation (the home screen; no teaching content).

The other 16 files are byte-identical duplicates by recorded hash, so I covered them by hash but did not open them:
- article-03 matches 02;
- article-07 and 09 match 05;
- article-08 and 10 match 06;
- article-16 matches 14;
- article-18 and 19 match 17;
- word-0-02, 03 and 04 match word-0-01;
- word-0-09, 11, 12 and 13 match word-0-08;
- word-0-06 matches pair-0-components.

The manifest has no article-01/04/13/15 or word-0-00/05/07/10. Renditions were 900x2000.

## Verdicts

| Unit | Correctness | Scoped coverage | Text comprehensibility |
|---|---|---|---|
| kanji/勅.md | CLEAN | CLEAN | CLEAN |
| words/勅令.md | CLEAN | CLEAN | CLEAN |
| 令.md line 37 (勅令 line) | CLEAN | CLEAN | CLEAN |

**Real quiz choices, meaning and rendering: no defect found within the recorded contexts.**
- **Default N1:** the live sequence is 畔 "paddy boundary; waterside" / 剰 "remainder; surplus amount" / 俸 "salary; stipend" / 勅. It rendered exactly that way and all three are wrong for the target.
  - 剰's full families (surplus, remainder, besides) and 俸 "salary" have no command or edict sense. 俸 shares only an official/government topic.
- **All and custom:** the curated 束/効/勤 are safe.
- **Native random-pool choices:**
  - 扱: the full family includes handle/treat/deal in/operate, and 扱く "work someone hard"; none is an order.
  - 獣, 矛 and 芋: no relevant sense.
  - Other offered characters (刑, 准, 冒, 凝): judged safe from their labels and raw meanings.
- **Word choices, both directions:** 政府, 官庁, 公務, 法-free choices and the rest were judged safe from their full families.
  - 不正 "illegality" and 専制 "autocracy" are related by topic only.

This is not a guarantee for every possible future pool.

**Rendering:**
- On-reading choices チョウ/サク/チョク/キク display correctly, with チョク shown as correct.
- Drawing shows 9 numbered reference strokes, 束 left and 力 right. Tracing is ungraded; "handwriting model not available"; recall shows a reveal.
- The 令 line renders as a link, and the article viewport sequence is coherent.
- The reading table's first viewport cuts off the third column. The sideways-scrolled capture (article-06/11) shows the full disposition text.

## Findings
No defects are established.

**Unresolved hypothesis (non-blocking): 訓 as a fallback choice.**
- **Evidence for:** 1956150 sense 2 is "precept, lesson, one's teachings" and 1236890 訓え is "teaching, instruction". The displayed label is "instruction; kun reading".
- **Evidence against:** neither family has a sovereign's or command sense. "Imperial" in the target label separates the two. 訓 never appeared in any real N1/All/custom/random sample; it appears only in the 32 deliberately constructed test pairs.
- **Status:** weakened but not closed, since every possible future pool can't be checked. No guard is proposed. Confidence that it is a real problem: low.

**Reconciliation of my original items:**
1. **ちょく vs チョク wording** (勅.md:35): partly resolved. The screens show katakana チョク while the answer is stored as ちょく; "practiced as ちょく" is accurate but slightly unclear. Optional.
2. **令/命 overlap sentence** (勅.md:46): unchanged. As rendered, "overlap in their order/command meanings" still reads ambiguously. Optional.
3. **Mention standalone 勅, old form 敕, 勅命/詔勅:** unchanged. Optional.
4. **令.md footer lacks 1430550:** confirmed in the rendered screen (footer lists 1517500, 1532160, 1556190). Optional.
5. **訓 hypothesis:** unresolved and non-blocking, as above.

## Optional
- The four items above.
- The quiz feedback line "imperial order: チョク、いましめる、みことのり" shows the unverified いましめる without the article's qualification. This is an app-wide display behaviour, not a defect in this batch.

## Limits
- **Machine-only evidence:** emulator (SDK 35, offline) and scaled renditions only. Nothing certifies original pixels, a physical phone, a native speaker's judgement or the fallback font face.
- **Fonts:** the panels label Gothic, Mincho, Textbook and Brush. No row is separately labelled as the default system font, though the quiz screens show 勅 in default faces.
- **Handwriting:** drawing mechanics are not handwriting recognition or mastery.
- **Not done:**
  - no independent upstream dictionary retrieval;
  - no Git or hash verification;
  - no check of every future quiz pool;
  - no measure of learning effectiveness.
- **Inherited material:** 1604470 and the KANJIDIC records were not re-read this session.
- **Process:** the one parallel batch (the three font panels) breached the serial-read rule.
- **Not claimed:** no edits, no publication, and no claim of phone, general-release or whole-project acceptance.
