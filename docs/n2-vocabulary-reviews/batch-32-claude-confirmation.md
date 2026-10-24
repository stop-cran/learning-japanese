## Snapshot
- **Corrected commit:** **7c8589f091e37b73a1945e696624e32c1168d8e6**. **Parent:** **f6d1ef9efca4ffa026bcdb0fe4eb4e768ade64c8**.
- I reviewed committed content only: six articles plus the `batch-32.json` provenance hunk.
- I had file tools only and couldn't run Git or compute hashes. The commit identity, file hashes, diff completeness and evidence equivalence all rest on the author's receipt. I assumed the working-tree files match the commit.

## Scope
- **Model:** claude-opus-5.5 (Claude family). I worked alone, read-only, with no delegation.
- **Read in full:**
  - the correction receipt and my initial report
  - the whole correction patch (seven file sections: six articles plus the provenance hunk)
  - the 7-line comparison rendering, all three senses
  - `words\すっと.md` and the six changed articles
- **Evidence derivative:**
  - read in full: the original quizDeclarations, sourceAccessLimits, the additional 1006140 family and correctionEvidence
  - complete families 1005190, 1057960, 1299280 and 1399520
  - the Daijisen receipts for さようなら and サラリーマン
- **Targeted checks:**
  - English titles in `words\` that share a key word, and every `quiz_exclusions` entry naming すっと or 雑音
  - お先に.md and the チェーン example line in 錆びる.md
  - the TSV header
  - `docs\confusable-words.md` (no rows for these words)
  - only the six `manifest.json` entries for the changed files: the receipt hashes the manifest, and repository rules require it to be regenerated
  - the public Weblio page for サラリーマン
- **Carried forward without re-reading:** the eleven other new articles, three reuse claims, four kanji edits and twenty mappings.
- **Not read:** the other family's reports, the review ledger, authoring notes, REVIEW.md and the committed `batch-32.json`. The patch and evidence contain author adjudications that name other-family finding IDs (GPT F01, F02 and an optional item). I saw only those author summaries.

## Verdicts

| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| さっさと | CLEAN | CLEAN | CLEAN |
| さわやか | CLEAN | CLEAN | CLEAN |
| さようなら | CLEAN | CLEAN | CLEAN |
| サラリーマン | CLEAN | CLEAN | CLEAN |
| 雑音 | CLEAN | CLEAN | CLEAN |
| 錆 | CLEAN | CLEAN | CLEAN |

- **Other eleven new articles:** the initial all-CLEAN verdicts stand. These are 撮影, 早速, 錆びる, 座布団, 冷ます, 妨げる, 冷める, 騒がしい, 三角, 算数 and 酸性.
- **Reuse claims (N2:633 to N2:635):** CLEAN, carried forward.
- **Kanji edits (布, 団, 角, 算):** CLEAN, carried forward.
- **Twenty mappings:** CLEAN, carried forward. My initial summary grouped the additional senses wrongly:
  - N2:640 selects 1303930 senses 1 and 2, and its additional_senses field is empty.
  - I also left out N2:624, which does carry additional sense 1005190:2.
  - The correct additional-sense rows are N2:623 (1299280:3), N2:624 (1005190:2) and N2:631 (1556750:3).
  - No mapping verdict changes.

## Findings

**B32-QZ-01 (missing さっさと/すっと exclusion): resolved.** Confidence: high.
- さっさと.md:9 now lists すっと.
- The pinned evidence supports the overlap:
  - さっさと 1005190 sense 1 includes "quickly" and "without hesitation".
  - すっと 1006140 sense 1 reads "straight, quickly, directly, all of a sudden".
  - すっと.md:15 says "often without hesitation".
- One declaration is enough because exclusions are symmetric. すっと.md correctly gets no edit.
- The pinned family removes my earlier caveat about the public JMdict version Jisho uses.

**New さわやか/すっと exclusion: supported, not excessive.** Confidence: medium-high.
- さわやか 1399520 sense 1 means "fresh, refreshing".
- すっと 1006140 sense 3 is "to feel refreshed" (used with する), and すっと.md:32 teaches すっとする.
- The English labels "smoothly" and "fluent" are also close.

**Declaration counts:** I confirmed 13 cards and 61 directional declarations. The original 59 differ only by the two すっと additions.

**B32-RG-01 (さようなら register): resolved within its bounded scope. The broader proposal is reclassified Optional.**
- さようなら.md:34 now contrasts the teacher example with お先に失礼します for leaving work before colleagues. This matches お先に.md's title and example, and it covers the colleague case I flagged.
- The article states no universal rule about adult use, frequency or final partings. My broader proposal had no public support I could inspect, so it shouldn't be imposed.
- No established defect or consequential unresolved claim remains.

**Original optional items that were adopted:**
- **雑音 title:**
  - "noise; static" matches 1299280 sense 1 ("noise (usu. unpleasant)") and sense 2 ("interference (e.g. radio), static, noise").
  - Lines 16, 18 and 34 still teach interference and the sense-3 gossip/criticism use.
  - No other title contains "static", and じゃま no longer shares "interference". 音, 物音 and 騒音 stay excluded, and the heading matches the title.
- **錆, チェーン:** this matches 錆びる.md:18. It is polish only, not proof that 鎖 is wrong.
- **サラリーマン:**
  - Line 23's wasei-eigo claim is now sourced. Line 33 credits it to 1057960 sense 1, whose loan source "salaryman" carries `ls_wasei=y`.
  - Line 34's "Definition" label is accurate.

**Regressions:** none found. All six manifest entries match the receipt's post-correction hashes, so a stale manifest isn't dropping any card.

## Optional
- **さようなら:** a casual-farewell contrast, such as じゃあね or またね, framed as a tendency and added only with an inspected public teaching source.
- **サラリーマン:** line 31 could acknowledge broader dictionary definitions. The Wikipedia text on Weblio quotes Daijisen as 給料で生活する人。月給取り。勤め人. The line is already hedged, so this isn't a defect.
- **Unchanged earlier items:**
  - さわやか: 弁舌さわやか
  - 妨げる: the noun 妨げ and ～の妨げになる
  - 三角: the さんかっけい reading of 三角形
  - 錆: 身から出た錆
  - 錆びる: 腕が錆びる, labelled as outside the source sense
  - さっさと: さっさとしなさい, without a command-register rule

  None of these causes new learning harm.

## Limits
- **Author's receipt:**
  - Commit identity, hashes and evidence equivalence aren't independently verified.
  - The patch omits `manifest.json`. I judged it current only by comparing hash strings.
- **Unchanged scope:** I carried it forward without re-reading it.
- **Public dictionary pages:** my Weblio fetches for さようなら and サラリーマン showed only text taken from Wikipedia. I didn't see the Daijisen bodies the author receipts claim.
- **さっさと:** still has no positive public lexical source beyond JMdict.
- **さようなら register:** unverified in public sources, but the article now asserts no such rule.
- **No quiz runs and no native-speaker review:** I ran no app quiz draws and have no native-speaker certification.
- **Consequential unresolved claims:** none.
