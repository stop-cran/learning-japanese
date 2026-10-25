## Snapshot

The full frozen commit is `3e67155e0a83c666b61719eca7eb3377fd649ce9`, with parent `1544e108e7c7d25df19edbbd93f37a07c9576305` and committed content only. My file tools can't run Git, so the commit, the hashes and the author's equivalence checks are the author's claims; I did not check them myself. I read the working-tree files as the snapshot. The snapshot lists `words/漬ける.md` among the related paths, but the patch has no diff for it, which matches "unchanged".

## Scope

Reviewer: claude-opus-5.5 (family: claude). I made no edits, used no agents and ran no Git.

**Read in full:**
- **Instructions:** `.github\copilot-instructions.md`, `.github\instructions\content-structure.instructions.md` and `docs\content-format.md` lines 18–126.
- **Articles:** all 14 new articles and all 5 reused articles.
- **Kanji cards:** `kanji\造.md` and `kanji\詰.md`.
- **Private files:** `frozen-snapshot.json`, `related.patch`, `review-evidence.json`, `review-mappings.jsonl`, `review-components.jsonl` (29 records), `review-principals.jsonl` (21 families) and `public-bodies.txt`.
- **Mappings:** `docs\n2-vocabulary-sources.tsv`, the header and rows 1102–1121.
- **Comparison articles:** ぺちゃんこ.

**Searched only:**
- `review-labels.jsonl`, for specific titles.
- The title and guard lines of `words\` articles (生産, 苦心, 役, 役割, 務め, 勤め, 勤める, 関係, 関連, 繋ぐ, 結ぶ, 製造, 作製, 製作, 通信, 主役 and others).
- `kanji\` for the batch words.
- `docs\confusable-words.md`, which has CW020, CW021 and CW084.

**Not read:**
- `family-inspection-01` to `08`, `supplement-comparison-reading.txt` and `public-bodies.json`.
- `docs\n2-vocabulary-snapshot.json`, `docs\n2-source-snapshot.json` and `docs\jlpt-levels.md`.
- Full bodies of the 伝, 務, 努, 着, 突, 込 and 点 kanji cards.
- No web pages fetched.

`principal-reading.txt` does not exist at the exact path I was given.

## Verdicts

Columns are correctness / scoped coverage / comprehensibility. Missing quiz-exclusion pairs are counted under coverage, and a pair-level finding is marked on both of its articles.

| Row | Article (raw source spelling) | Corr. | Cov. | Compr. |
|---|---|---|---|---|
| N2:1102 | 作る, reused (造る) | CLEAN | NEEDS FIX (B56-Q1) | CLEAN |
| N2:1103 | 付ける, reused (着ける) | CLEAN | CLEAN | CLEAN |
| N2:1104 | 付ける, reused (点ける) | CLEAN | CLEAN | CLEAN |
| N2:1105 | 漬ける, reused (浸ける) | CLEAN | CLEAN | CLEAN |
| N2:1106 | 伝わる, new | CLEAN | CLEAN | CLEAN |
| N2:1107 | 突っ込む, new | CLEAN | CLEAN | CLEAN |
| N2:1108 | 務める, new | CLEAN | NEEDS FIX (B56-Q4) | CLEAN |
| N2:1109 | 努める, new | CLEAN | NEEDS FIX (B56-Q3) | CLEAN |
| N2:1110 | 綱, new | CLEAN | CLEAN | CLEAN |
| N2:1111 | 繋がり, new | CLEAN | NEEDS FIX (B56-Q2) | CLEAN |
| N2:1112 | 繋がる, new | CLEAN | NEEDS FIX (B56-Q2, pair) | CLEAN |
| N2:1113 | 繋げる, new | CLEAN | NEEDS FIX (B56-Q2, pair) | CLEAN |
| N2:1114 | 粒, reused (level only) | CLEAN | CLEAN | CLEAN |
| N2:1115 | 潰す, new | CLEAN | CLEAN | CLEAN |
| N2:1116 | 潰れる, new | CLEAN | NEEDS FIX (B56-Q5) | CLEAN |
| N2:1117 | つまずく, new | CLEAN | CLEAN | CLEAN |
| N2:1118 | 詰まる, new | CLEAN | CLEAN | CLEAN |
| N2:1119 | 積む, reused (level only) | CLEAN | CLEAN | CLEAN |
| N2:1120 | 爪, new | CLEAN | CLEAN | CLEAN |
| N2:1121 | 艶, new | CLEAN | CLEAN | CLEAN |

**Kanji edits**
- **造 edit: CLEAN.** The つく.る row (line 31) and the Common words entry (line 39) link to `words\作る.md` and explain that 造る is a spelling taught in the 作る article.
- **詰 edit: CLEAN.** The つ.まる row (line 33) and the Common words entry (line 41) now link [詰まる].

**Baseline metadata preservation: CLEAN**
- 作る keeps N5, "make; prepare" and `[作]`; 付ける keeps N5, "attach; add" and `[付]`.
- 漬ける is unchanged at N4.
- 粒 and 積む only gained `jlpt: 2`, and the 粒 guards are kept.
- The 造 and 詰 frontmatter is unchanged.

**Mappings: CLEAN**
- All 20 rows in the TSV and mappings file match the associations you specified.
- 務める: the raw ID 1240825 is spelled only 勤める, so the switch to 2872052 is an identity correction, and the article says so.
- 努める: the copied employment gloss is not taught.
- 点ける: it stays a separate entry (1610400) that cross-references 1495770 sense 13, and the primary spelling 付ける is kept.
- 浸ける: only sense 1 (soaking) is shared. JMdict restricts sense 2 (pickling) to 漬ける, and the article teaches that.
- 着ける: the article accepts it only for wearing (sense 3) and bringing alongside (sense 7), and teaches attaching (sense 1) under 付ける. That matches the dictionary text's split of (着ける) senses.
- つまずく: the article lists no kanji, which is correct for a word usually written in kana.

**Examples checked against the dictionary text**
- 丈が詰まった is supported by "洗濯したら、丈が詰まった".
- 酔って潰れる is supported by sense 7 (and JMdict sense 9).
- 才能を潰す is supported by JMdict sense 6.
- 電話をつなげる is supported by JMdict sense 3.

## Findings

All five findings are Low severity and concern missing quiz-exclusion pairs. The rule in `docs\content-format.md` (lines 95–99) is to exclude a pair when a learner could reasonably accept either title for either word.

- **B56-Q1 · Low · `words\作る.md:9`.** 作る ("make; prepare") and 生産 ("production; manufacture") are not excluded from each other; 生産 has no exclusions at all.
  - Evidence: this batch added 製造 ("manufacturing") to 作る. 作製 and 製作 (both "manufacture; production") exclude both 作る and 生産. こしらえる, 制作, 創作 and 造船 also exclude both.
  - Fix: add 生産 to 作る's exclusions.
  - Confidence: medium-high.
- **B56-Q2 · Low · `words\繋がり.md:9`.** 繋がり ("connection; relationship") doesn't exclude its own verbs: 繋がる ("be connected; lead to"), 繋げる ("connect; link together") and 繋ぐ ("connect; tie").
  - Evidence: 繋がる already excludes 関係, whose title is "relationship; connection" (`関係.md:5`), the same glosses as 繋がり, plus 接続. 勤め/勤める is an existing same-root noun/verb exclusion.
  - Fix: add 繋がる, 繋げる and 繋ぐ to 繋がり's exclusions.
  - Confidence: medium-high.
- **B56-Q3 · Low · `words\努める.md:9`.** 努める ("strive; make an effort") and 苦心 ("painstaking effort; taking pains") are not excluded from each other.
  - Evidence: both already exclude 努力 and 一生懸命.
  - Fix: add 苦心 to 努める's exclusions.
  - Confidence: medium.
- **B56-Q4 · Low · `words\務める.md:9`.** 務める ("serve as; play a role") and 役割 ("role; allotted duties") are not excluded from each other. 役 ("role; duty") and the same-root 務め ("duty; responsibility") are also unguarded.
  - Evidence: this batch's own 努める/努力 exclusion and the 勤め/勤める precedent treat similar verb/noun pairs as confusable. 役, 役割, 務め and 主役 already exclude one another.
  - Fix: add 役割, and consider adding 役 and 務め.
  - Confidence: medium.
- **B56-Q5 · Low · `words\潰れる.md:9`.** 潰れる ("be crushed; go out of business") and ぺちゃんこ ("squashed flat") are not excluded from each other.
  - Evidence: ぺちゃんこ has no exclusions, its own example uses つぶした, and it isn't in the author's 289-label comparison set.
  - Fix: add ぺちゃんこ to 潰れる's exclusions, and consider adding it to 潰す.
  - Confidence: medium.

I judged these existing exclusions defensible rather than excessive: 突っ込む/質問, 付ける/掛ける (consistent with CW020), 潰す and 潰れる with 無駄, and 綱 with 線 and 筋.

## Optional

- `艶.md:24` says "personal appeal". Wording such as "charm or depth (e.g. of a performance)" would stay closer to sense 3 ("芸に艶が出る") and further from sense 4, sexiness, which isn't selected.
- Weaker exclusion candidates: 伝わる/通信 and 詰まる/渋滞.
- `kanji\突.md` and `kanji\込.md` could mention 突っ込む. 努める could link the existing 勉 and 力 cards for its rare spellings.

## Limits

- I didn't run Git or hash checks, and author-run checks aren't independent verification.
- I didn't read the eight family-inspection files, the supplement rendering or the two docs snapshot JSON files. My sense-level claims rely on `review-principals.jsonl` plus one public dictionary text (author captures, not fresh retrievals), and I fetched no web pages.
- I judged exclusions from titles plus targeted reads of comparison articles, not a full read of every `words\` body, so other missing pairs may exist.
- This is not a native-speaker certification, and frequency was not measured.
