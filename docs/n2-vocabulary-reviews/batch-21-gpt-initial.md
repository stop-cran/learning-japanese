## Snapshot: b0dcca6434845e2b41b0161a8f0249502b182e46; committed content only

Parent: `91b33ff51cd3d94c23a6162041cf10597e939f79`.

This is the committed snapshot identified by the frozen receipt. **Overall verdict: NEEDS FIX for three direct quiz-exclusion gaps.** No separate actionable defect was established in the taught definitions, readings, source coverage, or six related changes.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

I read all nineteen new articles completely, the actual six-file related patch and changed passages in context, and all twenty assigned mappings, N2:402–N2:421. 金魚 was assessed only for its 金魚/きんぎょ “goldfish” coverage and newly sourced `jlpt: 2`, not comprehensive recertification of unchanged teaching.

The review used the required repository instructions, allowed provenance files, all twenty complete principal lexical families, component evidence, focused comparison records and existing cards, and independently retrieved public dictionary bodies. Work was sequential and read-only, without delegation. Forbidden authoring material, quiz rationale, and other reviewers’ outputs were not consulted.

## Verdicts: three quiz-correctness fixes; source mappings and teaching otherwise CLEAN within scope

**CLEAN** means no actionable defect established within the assigned scope—not exhaustive correctness or native-speaker certification. The three **NEEDS FIX** results below concern quiz metadata, not the accuracy or completeness of the article’s declared teaching.

All articles in this table are under `words\`.

| Source row | Article / reading | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:402 | 曲線 / きょくせん | CLEAN | CLEAN | CLEAN |
| N2:403 | 規律 / きりつ | CLEAN | CLEAN | CLEAN |
| N2:404 | 斬る / きる | CLEAN | CLEAN | CLEAN |
| N2:405 | 気を付ける / きをつける | CLEAN | CLEAN | CLEAN |
| N2:407 | 区域 / くいき | CLEAN | CLEAN | CLEAN |
| N2:408 | 偶数 / ぐうすう | CLEAN | CLEAN | CLEAN |
| N2:409 | 空想 / くうそう | CLEAN | CLEAN | CLEAN |
| N2:410 | 空中 / くうちゅう | NEEDS FIX | CLEAN | CLEAN |
| N2:411 | クーラー / クーラー | CLEAN | CLEAN | CLEAN |
| N2:412 | 釘 / くぎ | CLEAN | CLEAN | CLEAN |
| N2:413 | 区切る / くぎる | CLEAN | CLEAN | CLEAN |
| N2:414 | 櫛 / くし | CLEAN | CLEAN | CLEAN |
| N2:415 | くしゃみ / くしゃみ | CLEAN | CLEAN | CLEAN |
| N2:416 | 苦情 / くじょう | CLEAN | CLEAN | CLEAN |
| N2:417 | 苦心 / くしん | CLEAN | CLEAN | CLEAN |
| N2:418 | 屑 / くず | CLEAN | CLEAN | CLEAN |
| N2:419 | 崩す / くずす | NEEDS FIX | CLEAN | CLEAN |
| N2:420 | 薬指 / くすりゆび | CLEAN | CLEAN | CLEAN |
| N2:421 | 崩れる / くずれる | NEEDS FIX | CLEAN | CLEAN |

**All twenty source mappings: CLEAN / CLEAN / CLEAN** for spelling, reading, applicable source meaning, and comprehensible explicit use teaching. This mapping assessment is separate from the quiz defects below. N2:406 maps correctly to the reused `words\金魚.md`: 金魚/きんぎょ, “goldfish,” sense 1; its scoped reuse verdict is likewise **CLEAN / CLEAN / CLEAN**.

The sense qualifications are handled appropriately. 規律, クーラー, and 区切る teach selected senses 1–2; 崩す teaches selected senses 1 and 4 plus clearly identified additional sense 2. The other mappings select sense 1, with additional coverage appropriately separated for 屑’s insult sense 2, 薬指’s fourth-toe sense 2, and 崩れる’s senses 2, 3, and 6. The reading-restricted くさめ charm sense is not transferred to くしゃみ. Raw glosses such as “troubles,” “pains,” “stop,” and “vision” are not promoted into unrestricted everyday meanings.

The community list supports the headword-level N2 classification; it does not establish an official modern JLPT syllabus or independently classify every secondary sense as N2.

| Related file | Reviewed change only | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `kanji\線.md` | 曲線 at セン, common-word link, attribution | CLEAN | CLEAN | CLEAN |
| `kanji\律.md` | 規律 at リツ, common-word link, attribution | CLEAN | CLEAN | CLEAN |
| `kanji\区.md` | 区域 and 区切る at ク, links, attribution | CLEAN | CLEAN | CLEAN |
| `kanji\域.md` | Existing 区域 mentions linked; example at イキ | CLEAN | CLEAN | CLEAN |
| `words\金魚.md` | Addition of `jlpt: 2` only | CLEAN | CLEAN | CLEAN |
| `words\カーブ.md` | Link around the existing 曲線 comparison only | CLEAN | CLEAN | CLEAN |

All five required reciprocal N2 word/kanji pairs occur at their applicable readings. Written-kanji metadata is complete, including characters without cards: 斬, 釘, 櫛, 屑, and 崩. Their missing cards do not justify omitting metadata or demanding new stroke files. The mixed-reading treatment of 気を付ける and 区切る follows the documented app convention. No ID replacement or removal of an easier level appears in the supplied related diff.

## Findings: three missing direct exclusions

**GPT21-01 — Medium severity; correctness / quiz ambiguity**

**Location:** `words\崩れる.md:4–9`; counterpart `words\下降.md:4–9,16`.

崩れる does not directly exclude 下降, whose displayed title is **“descent; decline.”** 崩れる has an ordinary financial decline/slump sense, so that answer remains defensible despite not being the sense taught on the new page. Both cards’ exclusions involving 下がる do not protect this pair: exclusions are not transitive.

**Minimal remedy:** Add `下降` to 崩れる’s `quiz_exclusions`, or declare the equivalent pair on 下降. No additional lesson or N2 claim is required.

**Evidence:** Complete JMdict family **1516270, sense 4** records stock-market crashing, slumping, and declining, without a rare/obsolete restriction. Independently retrieved [Digital Daijisen, 崩れる](https://www.weblio.jp/content/崩れる), sense 5, confirms falling market prices through 値が崩れる. [下降](https://www.weblio.jp/content/下降) independently covers downward change in level, not solely physical descent. **Confidence: high.**

**GPT21-02 — Medium severity; correctness / quiz ambiguity**

**Location:** `words\崩す.md:4–9`; counterpart `words\笑い.md:4–9,16–21`.

The smiling-sense exclusions cover 微笑む, 笑う, and 笑顔 but omit 笑い, whose actual title is **“laughter; smile.”** A learner familiar with the ordinary face-expression construction can reasonably accept its “smile” gloss for 崩す. Existing exclusions through the other smiling words do not protect this direct pair.

This is specifically the construction-qualified sense—not a claim that standalone 崩す freely means every kind of smiling or laughing.

**Minimal remedy:** Add `笑い` to 崩す’s `quiz_exclusions`.

**Evidence:** Complete JMdict family **1516260, sense 6** gives “break into a smile,” explicitly qualified **“as 顔を崩す, etc.”** Independently retrieved [Digital Daijisen, 崩す](https://www.weblio.jp/content/崩す) confirms the 相好を崩す / 顔をほころばす construction. The existing 笑い article explicitly teaches the facial-expression sense, including 笑いを浮かべる, rather than audible laughter alone. **Confidence: high.**

**GPT21-03 — Medium severity; correctness / English-label ambiguity**

**Location:** `words\空中.md:4–9,16`; counterpart `words\架空.md:4–9,21`.

空中’s **“midair; in the air”** and 架空’s **“imaginary; overhead”** remain eligible together. 架空’s ordinary physical aerial/overhead sense creates an overlapping English answer, independently of its imaginary sense. The displayed “overhead” gloss is not qualified as a particular wire construction, leaving this distinction unavailable in the context-free quiz.

This is a physical-sense/title overlap, not an exclusion proposed merely because both words contain 空 or concern the sky.

**Minimal remedy:** Add `架空` to 空中’s `quiz_exclusions`, preserving both articles’ useful teaching.

**Evidence:** Complete JMdict families **1245790, sense 1** and **1193130, sense 2** respectively establish the air-space and aerial/overhead senses. The latter applies to the actual spelling 架空 and reading かくう; it does not depend on search-only 仮空 or on transferring the imaginary sense’s reading restriction. Independently retrieved [Digital Daijisen, 架空](https://www.weblio.jp/content/架空), sense 1, confirms the physical construction as spanning through the air. **Confidence: medium-high.**

## Optional: none

## Limits: file-only snapshot assurance and bounded lexical review

I had file tools, **not Git execution**. The full commit, clean committed status, evidence equivalence, and recorded hashes therefore come from the frozen receipt; I could not independently execute hashes or verify file-to-commit equality. No working-tree-only change was intentionally included.

The evidence packet contains selected complete families, not the entire dictionary. I read every principal family but did not independently inspect all 217 comparison families; comparison checking used focused complete records, existing articles, title/exclusion searches, and public dictionary bodies. Embedded author-inspection receipts were treated as assertions, not independent retrieval.

The quiz findings establish possible unguarded pairings under the documented rules, not observed application-generated questions. Unchanged teaching in the six related files, especially 金魚, was not comprehensively recertified; nor does CLEAN imply corpus-wide collocational verification or native-speaker certification.
