# B117 confirmation — N1-B117-CLAUDE-CONFIRM-001

## Snapshot
Commit: 8c40423d66d176580a4b3f89d11c3ba077cbb829
Model: runtime-reported Claude Opus 5.5 (claude-opus-5.5); identity not independently verified

## Scope
Chain: segments 1-70 of n1-b117-claude-confirm-001, each viewed once in order; no re-views
Fetches: none

## Dispositions
- F1 - RESOLVED - 維 now declares 索 and 緒 directly (snapshot/kanji/維.md:14), with a Notes explanation of the rope/tie overlap (snapshot/kanji/維.md:47). The overlap is supported by KANJIDIC2 維 "rope" (original-packet/evidence/source-metadata.json:69-71) and Daijisen 維 sense 2 つな/糸すじ (original-packet/evidence/external-snapshots/03-extract.txt:20).
- F2 - RESOLVED - 紀 now declares 歴 (snapshot/kanji/紀.md:14), explained at snapshot/kanji/紀.md:46. 歴's title "history; passage of time" (snapshot/docs/n1-sources/batch-117/reconciliation-001/comparison-cards/歴.md:3) overlaps KANJIDIC2 紀 "history" and Daijisen 紀 sense 3.
- F3 - RESOLVED - 索 now declares 捜 and 探, plus 求/問/聞/伺/調/査/究/散 (snapshot/kanji/索.md:14), with notes at snapshot/kanji/索.md:46-47. This matches KANJIDIC2 "searching/inquiring" and Daijisen 索 sense 2 (original-packet/evidence/external-snapshots/02-extract.txt:7).
- F4 - RESOLVED - 賃 now declares 代, 俸 and 給, plus 費/価/値/払/報/賞/雇/償 (snapshot/kanji/賃.md:14), with notes at snapshot/kanji/賃.md:48-49. KANJIDIC2 代 itself lists charge/rate/fee, and 給 lists salary/wage (kanjidic2-comparison-records.xml).
- O1 - RESOLVED - 紀 Meaning now teaches Daijisen's rules/code-of-conduct sense with 綱紀/風紀 and distinguishes it from rare 紀律 (snapshot/kanji/紀.md:23). This matches Daijisen sense 1 (original-packet/evidence/external-snapshots/01-extract.txt:7). Rule-titled guards 規/律/則/典/法/制/憲 were added.
- O2 - RESOLVED - 維 Meaning now cites Daijisen's つなぎとめる hold-fast sense with 維持 as the example, while keeping maintenance as a whole-word meaning (snapshot/kanji/維.md:23). This is consistent with the unchanged 維持 wrapper line (snapshot/words/維持.md:25) and Daijisen sense 3 (original-packet/evidence/external-snapshots/03-extract.txt:21).

## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: NEEDS FIX
Comprehensibility: CLEAN

## Confirmation
Verdict: NEEDS FIX
Basis: F1-F4 and O1-O2 are resolved, with sourced guards, accurate new Daijisen paraphrases, a corrected 維 reading-choice set and fresh passing gates. However, the revision's own guard criteria leave three same-label direct pairs undeclared on either endpoint (紀/著, 紀/歳, 索/偵), so the consistency facet needs one minor fix (new F1).

## Findings
### F1: Revised guard sets omit three same-label direct pairs
- Facet: Consistency and quiz safety
- Severity: minor
- Confidence: medium
- Citations: snapshot/kanji/紀.md:14; snapshot/kanji/索.md:14; snapshot/docs/n1-sources/batch-117/reconciliation-001/comparison-cards/書.md:3; snapshot/docs/n1-sources/batch-117/reconciliation-001/comparison-cards/著.md:3; snapshot/docs/n1-sources/batch-117/reconciliation-001/comparison-cards/著.md:20; original-packet/evidence/title-index.txt:660; original-packet/evidence/title-index.txt:95; reconciliation/pair-dispositions.json:28-31; reconciliation/pair-dispositions.json:107-111; reconciliation/pair-dispositions.json:154-163; original-packet/evidence/external-snapshots/01-extract.txt:5; original-packet/evidence/external-snapshots/01-extract.txt:10
- Evidence: 紀 now excludes 書, displayed as "write", because 紀 includes recording and recorded documents (Daijisen also gives 紀 the kun
    gloss しるす). It does not exclude 著, whose displayed title "write; remarkable" has the same head word and whose card teaches
    著す write/publish. 紀 also excludes 齢 "age; years lived" for the Daijisen 年代/とし sense, but not 歳 "years of age".
    索 excludes 査 and 究 as conservative investigation guards, but not 偵 "spy; covert investigation". The 著 comparison card was
    supplied, but pair-dispositions gives no disposition for 紀/著. 歳 and 偵 appear in no disposition. None of these pairs is declared
    on either endpoint: the 著 card has no quiz_exclusions, and only the four scoped cards changed. A learner applying the same reasoning
    the revision uses could accept these titles. Neither pair appears in current curated options, but fallback and other pools can expose them.
- Required change: Add 著 and 歳 to 紀's quiz_exclusions and 偵 to 索's, or record source-backed declines for each pair in the
    pair dispositions and card Notes. Then rerun validation and rebuild the manifest.

## Optional
None.

## Limits
- L1: The model identity above is runtime-reported and was not verified by any tool in this pass.
- L2: Only chain-supplied evidence was read. The 歳, 偵, 筆 and 文 comparison cards beyond the title index were not supplied, so F1 relies on displayed
  titles from the index and the revision's own guard bases. Raw HTML, SVGs, the Joyo PDF and Kotlin/native/device behavior were not examined.
- L3: 紀/筆 ("brush; writing") and 紀/文 ("sentence, writing") remain UNVERIFIED. The noun "writing" may overlap 紀's account/record senses
  less directly than "write", and the supplied evidence does not settle them.
- L4: My initial review accepted the original reading-exposure summary of zero production hits. That log's own 維 line said 由's ゆい was drawable in the
  N1/All stacks, and the pre-revision reproduction with 維=ゆい confirms a hit (coordinator/pre-revision-reading-extra-reproduction.log:72).
  The revision fixes this for the modeled N1/All pools (fresh-gates/reading-exposure-supplemental.log:75). A single-borrow Starter case can
  still draw ユイ from 由, as the 維 card discloses (snapshot/kanji/維.md:46). Arbitrary or multi-borrow pools are not covered.
- L5: Fresh gates (lint, quiz-safety, linkplan, reading-exposure-supplemental, validate, manifest, unittest, budget, vocabulary, manifest-rebuild)
  are host/static evidence, not linguistic proof. Compatibility with the installed 5c000bd APK, which predates quiz_exclusions, is not claimed.
- L6: The four existing word-article wrappers and their prose are unchanged from the reviewed freeze. The 紀 Notes still refer to JMdict's
  geological suffix entry after that sentence was removed from Meaning, but the Meaning paragraph still mentions the geological-period use,
  so this is not a defect.
