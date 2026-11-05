All 30 lexical families in lines 1–487 are now confirmed complete. The original conclusions still hold: every facet of the four teaching files remains CLEAN, with no findings. Turn 4 of 4: one tool call only.

**Snapshot:** Frozen teaching snapshot `2567f5e7b3888f2df3ed560f618341266b471902`. You reported an empty runtime teaching/manifest diff against HEAD `928a12f3796714edd74116fe5ac49b06f31d839c`; I can't check Git myself.

**Scope:** Claude Opus 5.5, same session as the original review. This is a dependent confirmation, not a new blind review. One call this turn: `batch-061-jmdict.xml`, lines 421–487. I'm carrying forward lines 1–420 from turns 1–3, so the four turns cover the whole file.

**Entries in this slice:**
- **2859896 アクション俳優/アクションはいゆう (completed from turn 3):** action movie actor; action star.
- **Four entries labelled "organization name":**
  - 5136341 映画俳優組合 (Screen Actors Guild);
  - 5294608 国際俳句交流協会 (Haiku International Association);
  - 5589220 俳優組合 (British Actors' Equity Association);
  - 5589221 俳優労働組合 (Actors Equity Association).

  None is taught, and none needs a support article.

**All 30 families confirmed:**

| Slice | Entries | Count |
| --- | --- | --- |
| Turn 1 | 1471890, 1471900, 1471910, 1471920, 1471930, 1471940, 1471950, 1471960, 1471970 | 9 |
| Turn 2 | 1471980, 1471990, 1472000, 1582950, 1600580, 1673920, 1813780 | 7 |
| Turn 3 | 1930590, 2098180, 2576280, 2639520, 2833326, 2845970, 2847588, 2853535, 2855783, 2859896 | 10 |
| Turn 4 | 5136341, 5294608, 5589220, 5589221 | 4 |

Spellings, readings and labels across the file:
- **Spelling and reading variants:** 誹諧 is a rarely used form of 俳諧. 俳徊 and 徘回 are search-only forms of 徘徊. 俳風 and 誹風 share one reading, with no restriction tying a reading to either spelling. 俳名 has two readings, はいめい and はいみょう.
- **Usage labels:** historical term, abbreviation, poetical term and organization name all appear.

None of these conflicts with the teaching.

**Verdicts:** The original four-file, three-facet conclusions remain supportable.

| File | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\俳.md` | CLEAN | CLEAN | CLEAN |
| `words\俳句.md` | CLEAN | CLEAN | CLEAN |
| `words\俳優.md` | CLEAN | CLEAN | CLEAN |
| `kanji\優.md` | CLEAN | CLEAN | CLEAN |

For `words\俳句.md`, `words\俳優.md` and `kanji\優.md`, the verdicts cover the changed link and the text closely tied to it.

**Findings:** None.

**Optional:** None new. The original four optional suggestions stay nonblocking and are not adopted.

**Limits:**
- **Earlier process violations still stand:**
  - 061-P1: one original response sent three view calls with two overlapping starts, reading lexical lines 150–300, 300–450 and 450–487.
  - 061-P2: fourteen calls each returned 151 lines, over the 150-line limit.

  This confirmation doesn't make the initial review strictly compliant.
- **This sequence re-read only the lexical XML.** The comparison XML, kanji dictionary XML, stroke data, guidance and articles were not re-read; I rely on the original reads.
- **Lookup limits unchanged:**
  - No Daijisen definition text was returned.
  - The haiku encyclopedia page was truncated.
  - The actor page gave only encyclopedia material, not a modern dictionary entry. Modern 俳優 identity rests on frozen JMdict entry 1471970.
- **Nothing new retrieved or tested:** no new retrieval, and no native-speaker, phone, rendering, drawing or runtime acceptance.
