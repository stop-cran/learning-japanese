**Snapshot:** Supplied frozen snapshot `4dba935415312d39b1c2defdc05b938d37fe21f0`; no uncommitted teaching included according to the task. Git identity, signature and worktree cleanliness were not independently verified because shell/Git operations were prohibited.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual phone comprehensibility of complete `kanji\乏.md`, `words\乏しい.md` and `words\貧乏.md`.

Read all assigned ranges: 64 complete frozen JMdict families (46 lexical, nine initial comparison, nine additional comparison); nine comparison kanji articles; 15 comparison word articles; repository guidance; raw character JSON; all three archived Daijisen sections, including the separate ともしい entry; and the complete pinned SVG. Also inspected scoped `docs\confusable-words.md`, actual title/distractor metadata for the supplied 12 legacy fallback cards, and existing 虎/猿 exclusions. No author rationale, evidence interpretations, reconciliation records or other reviews were consulted.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\乏.md` | CLEAN | CLEAN | CLEAN |
| `words\乏しい.md` | CLEAN | CLEAN | CLEAN |
| `words\貧乏.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no actionable defect established within this bounded scope, not exhaustive certification.

**Findings:** None.

Supporting conclusions:

- **Metadata and reading allocation:** Ordered full readings `[ボウ]` and `[とぼ.しい, とも.しい]`, selected practice readings `[ボウ]`/`[とぼ.しい]`, grade 8, canonical radical 丿/no. 4 and primary four-stroke count match the supplied KANJIDIC2 record. Selected readings normalize to `ぼう` and `とぼしい` and have their own linked model rows. The separate recognition-only ともしい row accurately preserves the alternate reading without mislabeling the linked article’s primary reading or asserting frequency or archaism.
- **Dictionary evidence:** JMdict 1584130 supports both adjective readings and insufficiency/poverty meanings. Archived Daijisen independently distinguishes とぼしい senses 1–2 and explicitly equates ともしい senses 1–2 with them. The teaching does not import ともしい’s additional classical meanings or interpret `▽`. Separate character readings and Daijisen’s split `びん‐ぼう` heading support ビン + ボウ allocation; this is not inferred merely from a kana substring.
- **Drawing and explanation:** The SVG contains four ordered stroke paths, consistent with the chosen model. The alternate three-stroke annotation does not contradict that choice. Modern-shape associations are explicitly mnemonics, not etymology; SVG grouping is not used as historical evidence.
- **Grammar and examples:** 乏しい’s direct noun attachment, negative, past and polite predicate are accurate. 貧乏’s noun/な-adjective attachment, polite predicate and intransitive する use are supported. The original student and household examples are natural, and their kana and English translations fit. The three 乏しい example patterns directly match archived Daijisen examples.
- **Semantic distinctions:** Both insufficiency and financial hardship are covered without falsely separating 乏しい from 貧しい or treating 少ない as incompatible with shortages. 豊富な経験/乏しい経験 supplies a meaningful quantity-and-attachment contrast. 金持ちの家庭 correctly illustrates the financial contrast with different noun attachment.
- **Support and navigation:** The two support articles adequately supply the selected readings; no additional 欠乏 article is necessary. Both selected kanji–word pairs have reciprocal links, totaling four required directed links. 貧 receives a substantive component link. No additional baseline reciprocal pair needs activation; incidental comparisons do not require unrelated backlinks.
- **Quiz exclusions:** Each declared direct pair was assessed independently against displayed labels and ordinary senses: 乏しい with 貧しい, 少ない, 不足, 貧乏, 欠ける, 僅か, 飢饉 and 悪い; and 貧乏 with 貧しい. The guards address defensible poverty, scarcity, meagreness or insufficiency interpretations in both quiz directions. They do not imply unrestricted substitution or a transitive exclusion clique. Actual 金持ち/豊富 contrasts and 少し/少々/ちょっと/粗末 meanings do not establish another necessary exclusion for these new labels. Existing baseline exclusions, including 虎/酔っ払い and 猿/馬鹿, remain present.
- **Default kanji choices:** 久, 反 and 乃 are semantically wrong for 乏 after checking their complete cards, not just titles. 貧, 欠 and 少 retain useful semantic comparisons without becoming wrong answers. The supplied 12 legacy cards each declare two curated distractors; their actual target meanings do not make 乏’s “scarce; lacking” a defensible fallback answer.
- **Presentation and levels:** Concise sections, translated examples and selective kana support textual small-screen comprehension. Neither support word inherits an asserted vocabulary level from the N1 kanji.

**Optional:** None.

**Limits:** All assigned ranges were returned without observed truncation; no resource reads or lookups failed. Dictionary HTML, XML, character metadata and SVG were supplied archived evidence, not fresh retrievals. No external web retrieval was performed, and archive hashes were not independently checked.

This was a textual review, not native-speaker, rendered-glyph, drawing-interaction or physical-phone acceptance. The supplied cmap result reports 丿 and 饉 absent from all three bundled fonts; that alone establishes neither rendering failure nor readability acceptance. Canonical 丿 metadata and the existing 飢饉 guard remain appropriate; fresh native comparison-word fallback evidence is pending.

Compatible Android `f9b59a2+` is required. Native/physical-phone/general-release acceptance remains outstanding, without becoming a blanket veto on bounded owner testing. The default fallback assessment does not certify larger, random or live quiz pools. Baseline preservation was checked only on the inspected surfaces, not through an independently verified Git diff. Tool calls were observed to run singly and serially in this session; no separate execution audit was performed. No files were changed.
