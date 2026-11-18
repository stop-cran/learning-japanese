# Batch 115: textual-review closure

The eight cards are textually review-closed, with the source/runtime limits below.
Publication is **pending** at this closure commit. The subsequent receipt must establish
the actual remote commit, CI and exact served ZIP; no native or phone acceptance is implied.

## Snapshot and scope

Members: **卓 厄 宙 寸 康 漠 票 魔**.
Source rows: 128, 134, 247, 263, 315, 648, 771, 1211.
Published base: `c7a7c8a75eec766d4d66ee172763e119075726ee`.
Blind-review freeze: `f36cd819dcf6ac8b4a3ee8ee29b6e750cd6f09ab`.
Reconciliation: `206f98936307a77937fb38346299af11044af761`.

Exactly eight kanji and eight stroke files are added. Eight existing word articles receive
one link wrapper each. The dependent 標 edit removes its now-false statement that 票 has
no card; no other old-card prose change or new word article is included.
憲・監・督・紀・索・維・賃 remain queued, with their earlier gathered evidence preserved.
The original fifteen-member extraction has 75 complete families; the initial review packet
contains the 41 complete applicable families for these eight active members.

Reconciliation changes six batch cards, adding eleven direct meaning-exclusion pairs and
two sourced clarifications. Titles, full/selected readings, curated distractors, stroke files
and word articles are unchanged after the freeze.

## Review execution and provenance

Initial reviewers independently used the same immutable freeze. Confirmations were serial,
Claude before GPT. Each confirmation received its own initial report, the revised cards and
the exact diff; GPT received neither Claude's confirmation nor the locator adjudication.
Models below are verified from runtime usage records, not report self-labels.

| Run | Actual model | Tool window (UTC) | Calls | Fetches |
|---|---|---|---:|---:|
| Claude initial 004 | claude-opus-5-5 | 2026-11-13 23:54:19 to 2026-11-14 00:05:30 | 46 | 0 |
| GPT initial 001 | gpt-6-astra | 2026-11-14 00:22:56 to 00:35:06 | 48 | 3 |
| Claude CONFIRM-002 | claude-opus-5-5 | 2026-11-14 01:43:49 to 01:46:22 | 29 | 0 |
| GPT CONFIRM-001 | gpt-6-astra | 2026-11-14 01:56:18 to 02:00:02 | 33 | 3 |

Both initial runs read all 30 core segments, then their independently requested extensions:
11 Claude segments / 50 sources and 10 GPT segments / 47 sources. Confirmations read
25 Claude segments / 57 sources and 26 GPT segments / 50 sources.
The complete records establish exact kickoff/bootstrap delivery, serial single-call responses,
one report write, complete readback and exact-enum completion. The accepted report-binding
note is LF creation versus CRLF disk bytes, not another write.

Both initial raw reports failed the frozen structure contract and remain unchanged with that
classification. Explicitly authorized format-only derivatives removed two five-byte Claude
cell annotations and expanded 17 GPT comma-joined citation lists without changing sources,
numbers, order, judgments or evidence. Original reports, derivatives, reversible normalization
proofs and both FAIL/PASS records are retained. GPT's original F5/F6 citation ranges stopped
two lines short; their supporting facts and that separate adjudication remain recorded.

Claude CONFIRM-001 is **VOID**: one fetch had empty same-response public text, and the
run ended without report readback or completion. Its report and observations were quarantined,
not read or used here. The separately authorized fresh CONFIRM-002 retained the same packet
and 25-segment chain, with only run/path substitutions and the prospective announcement
clarification. Frozen-auditor tests used fabricated fixtures only.
Initial Claude 001/002 remain VOID; 003 remains unaccepted. None supplies findings or hints.
The accepted Claude-004 initial slice is distinct from the later void confirmation in its session.

Raw execution payloads remain local because they may contain private system/context data.
This archive contains byte-exact reports, prompts, source chains, packet evidence, explicit
adjudications and bounded audit derivatives identifying their originals by hash.
The audit's redacted report-write marker is not represented as the original argument bytes.
Compressed chains/XML reconstruct their original bytes. Captured CRLF snapshots and LF Git
blobs are distinct representations, not falsely claimed raw-byte-equal.
`provenance.json` hashes the evidence files; the commit binds this README and provenance itself.
Hashes establish consistency, not comprehension.

## Reconciliation and model contributions

| Item | Disposition |
|---|---|
| 卓 / 偉・英・著・冠・凌・越 | Six direct pairs added, with English-choice protection distinguished from free Japanese substitution. |
| 厄 / 労 | Direct labor/trouble guard and sourced 苦労 comparison added. |
| 宙 / 時 | Direct time guard added; the classical temporal qualification and clock-time distinction remain. |
| 寸 / 微 | Direct minute/tiny guard added; the ancient き suffix sentence is clarified. |
| 票 / 署 | Direct sign guard added, explicitly distinguishing a ballot from signing a name. |
| 魔 / 怖 | Direct guard for the separately attested dreadful modifier sense, not a supernatural/fear clique. |
| 悪魔 religious senses | Christian/Buddhist labels explicitly attributed to JMdict. |

Claude F1/F2 and O1 overlap GPT F1/F2: optional labels do not make shared observations
GPT-only discoveries. GPT additionally supplied 宙/時, 寸/微, 票/署, 魔/怖 and the religious
attribution point, and exposed the unverified 寸 suffix claim. These are contributions to this
bounded sample, not model rankings. Direct pairs were decided from the actual labels and
source senses, not transitivity or a vote.

Claude's optional 厄/害・損, 寸/軽・粒 and 康/幸・福 guards were declined with confirmation
acceptance. Reciprocal declarations are unnecessary under the supplied symmetric meaning
builder. Broader 票/魔 reading-distractor changes remain optional/deferred; unread GPT limit
candidates were not promoted into defects. Claude CONFIRM-002's two optional suggestions
were not applied. Its weak-motivation qualification for 票/署 remains unchanged.

Both initial verdicts were **NEEDS FIX**, with GPT correctness **UNVERIFIED**.
Both accepted confirmations are **CONFIRMED**, with four CLEAN facets and no remaining
actionable finding in their assigned scope. Original judgments are not overwritten.

## Claude's eight locator errors

CONFIRM-002 is accepted **unchanged**, with no coordinator-normalized derivative.
Each fact was found in the already supplied source and none was contradicted.
The separate mapping is **N1's own adjudication evidence**, not corrected reviewer citations:

| Source | Original locator | Correct locator |
|---|---:|---:|
| title-index.txt: 軽 | 1121 | 1077 |
| title-index.txt: 害 | 419 | 354 |
| title-index.txt: 損 | 507 | 525 |
| title-index.txt: 幸 | 453 | 409 |
| title-index.txt: 福 | 775 | 837 |
| title-index.txt: 時 | 617 | 562 |
| repo/docs/content-format.md: symmetric exclusions | 89-91 | 102-107 |
| evidence/kanjidic2-records.xml: 宙 interval of time | 202 | 210 |

All supporting text, hashes, the historical hold and acceptance conditions are retained under
`adjudications/`. No new fetch was made to repair these locators.

## Source and execution limits

All seven Claude and ten GPT confirmation limits are copied verbatim into their separate
acceptance records and remain part of this closure.

- Claude's Daijisen 寸/き and 宙 statements remain **unverified by Claude CONFIRM-002**.
  GPT later made its own three properly announced fetches and actually received the relevant
  寸, 宇宙 and 康 text. This resolves GPT's own earlier 寸 uncertainty and supports its fresh
  classical 宙 check, without attributing those reads to Claude or erasing Claude's limit.
- No current Kotlin/JVM, Gradle, emulator, native or phone execution occurred in either
  confirmation. Host Python tests are separate evidence. The installed `5c000bd` APK predates
  `quiz_exclusions`; publication does not upgrade it or establish device compatibility.
- Only the meaning builder source was supplied. Reading builder/parser/stack propagation,
  arbitrary custom/caller-built pools and multi-borrow Starter pools remain unverified.
  The reading model reports zero N1/All and restricted Starter hits, with four latent collisions.
  A hundred seeds and zero reported problems are not exhaustive app-safety evidence.
- Source-only readings are covered by the separate exposure model, not every inventory in
  the reading-options output. Nanori and historical readings are not silently promoted into
  ordinary quiz metadata. The larger 75-family author collection was not independently
  reconstructed by GPT's 41-plus-four-entry confirmation.
- Confirmation does not freshly inspect raw SVG geometry, visual Joyo glyphs, all original
  word articles or all comparison-card bodies. Title-only and missing-card limits persist,
  including the explicit absent-card lists and broader candidate uncertainties in the reports.
- The reproduced lint result is **zero errors and four unchanged pre-existing warnings**
  for 寸法, 標本, 標準 and 標識. Their IDs are on wrapped continuation lines.
  The frozen zero-warning result **cannot be reproduced**; that log remains unchanged and
  is not relied upon. The four warnings are accepted on the stated non-strict basis.
- B113's historical UNVERIFIED verdict, missing compliant Claude confirmation and quarantines
  are unchanged. No later B113/B114 fix or observation from a void review is included.

## Validation and accounting

The signed runtime candidate passed 431 host tests, content validation, the qualified lint gate,
eight required word-link pairs, meaning checks, reading-option/exposure checks and archive budgets.
Manifest regeneration produced the exact committed LF bytes; the initial raw-byte comparison
against the CRLF checkout failed solely on line endings. The separate reproduction record states
that distinction, and the checkout was returned to CRLF without changing committed content.

Runtime version: **8a1b246322fb62d9**, **8,680 entries**.
Local archive: 8,687 files / 8,702 entries / 46,000,236 inflated bytes.
Vocabulary coverage remains 2,122/2,431; no additional pilot coverage is claimed.
The refreshed remote remained `c7a7c8a7`, already an ancestor; no integration merge was needed.

After local closure, source accounting is **239 done / 0 in progress / 989 not started**,
including six earlier N2 placements. Published accounting remains **231 delivered / 997
undelivered** until the separate remote/CI/ZIP receipt succeeds.
The tree contains 1,229 kanji and 5,083 words. Overall issue #60 is not complete.
