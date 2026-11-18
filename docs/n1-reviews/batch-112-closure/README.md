# Batch 112: textual review record

Batch 112 adds fifteen N1 kanji cards, their stroke data, and 45 reciprocal
backlink edits across 44 existing word articles:
健 妙 射 就 展 微 態 盤 看 至 診 酸 障 離 響.
微妙 supplies a mapped word for both 妙 and 微. No word article is added.
Three existing kanji cards, 基, 素 and 鏡, receive narrow updates to stale
remarks now that the linked cards exist.

The signed freeze is
`d6ad96ebf7d0352d54184ed44a382f70e4497f7b`, based on the published B111
record `0320ba4a199432374096360e984b7dc5754dd6bc`. Two independent reviewers
received the same immutable initial packet, whose `SHA256SUMS.json` hash is
`22dc9721a0dc9bd2d4e1e94a4cf7cc74cc4137ac017a435f78a17787089c2288`.
The manifest binds 6,392 files. Initial reports were written to separate
directories; neither reviewer received the other's findings or the author's
prior rationale.

The signed reconciliation commit is
`737cb0201bb3ca76b327504d95b17e64f1a79869`. It changes eight cards
(妙 就 展 微 態 盤 診 障) and regenerates the runtime manifest. The seven
other new cards, all word edits, stroke files and existing-kanji remark edits
are unchanged from the freeze. This revision adds sixteen direct meaning
exclusions and explanatory notes, clarifies one dictionary-spelling statement,
and does not change any title, reading, reading selection or distractor.

## Reconciliation

The following actions are present in `737cb020`. Both reviewers later found
every finding below resolved; neither returned a joint CONFIRMED verdict
(see "Final outcome").

| Observation | Initial report provenance | Action |
|---|---|---|
| 微 versus 分, English "minute" | Claude F1 | Add 分 and explain the English tiny/time-unit distinction; retain the title. This does not protect an older client that ignores exclusions. |
| 就 versus 企 and 承, "undertake" | Claude F2; GPT F2 | Add both direct pairs with explanations. |
| 就 versus 担, 職 and 位 | Claude F2, including weaker/consideration language | Add the responsibility/post/position comparisons; retain the distinction between complete words. Claude later judged 位 mild but defensible. |
| 就 versus 了, 完 and 済, completion | GPT F2 | Add the three pairs and explain the already-taught 成就 sense, without deleting ジュ or the completion explanation. |
| 態 as an additional spelling of other dictionary entries | Claude F3, polish | Name the JMdict entries headed by 体 (てい), 形 (なり) and 様 (ざま). Do not adopt an unsupported frequency claim such as "less common." |
| 障 versus 関, barrier | Claude O1; GPT F6 | Add 関 and explain the barrier overlap. |
| 展 versus 敷, spreading out | Claude O2(a); GPT F3 | Add 敷 and a precise physical spreading comparison. |
| 妙 versus 技 and 腕, skill | Claude O2(b); GPT F1 | Add both pairs, explicitly grounding the skill/cleverness sense in JMdict 1528490. |
| 微 versus 軽, slight degree | GPT F4 | Add 軽 and the sourced 軽微 example; distinguish this from light weight. Add complete JMdict 1615650 to the source citations. |
| 診 versus 査, inspection | GPT F5 | Add 査 to the existing examination comparisons; retain the medical-specific explanation. |
| 盤 versus 乗, English "board" | Author hardening, not a reviewer discovery | Add 乗 and explicitly distinguish the English noun from boarding a vehicle. |
| 態 as grammatical voice | Claude O3, optional enrichment | Decline expansion. The dictionary sense exists, but the bounded lesson does not require an additional voice lesson or unlinked compound. |

These are direct symmetric exclusions, not a transitive group. Six added
pairs arise from observations shared across the reports, including Claude's
Optional section: 妙/技, 妙/腕, 就/企, 就/承, 展/敷 and 障/関. Different
severity or section labels do not make those independent discoveries.
Claude additionally identified the English minute issue, suggested the three
responsibility/position comparisons, and suggested the 態 wording correction.
GPT additionally identified the three completion pairs, 微/軽 and 診/査.
The author's 盤/乗 addition is credited separately. This describes this
bounded sample, not a model benchmark.

The unexcluded generic English fragments "take" (就 compared with 取, 喫 and
連) and "over" (看 compared with unrelated phrasal labels) do not establish
additional interchangeable answers. No exclusions were added merely for
those shared fragments.

## Preserved review runs

Actual models come from execution usage records, not reviewers' configured
labels. Times below are UTC.

| Run | Actual model | Snapshot | Window (UTC) | API requests | Tool calls | Maximum in flight |
|---|---|---|---|---:|---:|---:|
| `initial-claude` | claude-opus-5.5 | `d6ad96eb` | 11-12 19:08:25-19:13:45 | 52 | 53 | 2 |
| `initial-gpt` | gpt-6.1-sol | `d6ad96eb` | 11-12 19:18:36-19:36:14 | 126 | 126 | 1 |
| `confirm-claude` | claude-opus-5.5 | `737cb020` | 11-13 06:20:00-06:22:00 | 13 | 13 | 1 |
| `confirm-claude-coverage` | claude-opus-5.5 | `737cb020` | 11-13 06:26:09-06:27:00 | 11 | 11 | 1 |
| `confirm-gpt` | gpt-6.1-sol | `737cb020` | 11-13 06:28:14-06:33:45 | 49 | 49 | 1 |

Both initial reports returned NEEDS FIX for meaning-quiz exclusions. Claude
also recorded the 態 wording polish and optional points above. GPT reported
six moderate findings, covering eleven omitted direct pairs. Neither report
established a failure of ordinary full-pool four-choice questions: the batch
already has three curated distractors per card. The omissions matter to
exclusion-aware fallback and filtered pools. Their actual Kotlin/custom-pool
exposure was not executed.

Initial scope limits remain visible. Claude did not read all 44 reused word
articles in full, the detailed reading-exposure lines or the Daijisen pages.
It disclosed briefly creating and deleting a temporary file. Its first two
rubric reads overlapped; the run is not described as strictly serial tool
execution. GPT inspected the full changed content, all 75 supplied JMdict
families, actual comparison articles and relevant Daijisen entries. Its
read-only SVG comparison supports source-geometry fidelity, not native
drawing behaviour.

The first Claude confirmation ran on 2026-11-13 at
06:20:00.858-06:22:00.184. It resolved the textual points, accepted the
optional decline, found no new defect, and returned UNVERIFIED because L1
remained partially resolved. That report was **not accepted as a complete
confirmation**: the actual commands returned Notes and patch hunks rather
than eight complete revised cards, and ran a prohibited scan of all 1,191
original kanji. The automatic audit missed this `os.listdir`-based scan; a
separate manual audit observation records the exact command and coverage
gap. Original reports and audits were not rewritten.

The coordinator stopped the cycle before GPT, explicitly returned the shared
content-reviewer allocation, and obtained a fresh reservation for two bounded
passes. The corrective Claude pass ran at
06:26:09.948-06:27:00.789. Its execution record establishes exactly eight
complete file-view reads, one at a time, with no shell, search, enumeration,
corpus scan or web work. It wrote a separate supplemental report, changed no
disposition, and established no new actionable defect. It relied on the
earlier patch and source inspection rather than claiming fresh reads of every
supporting source. The earlier process violation remains disclosed; the later
full-card read does not retroactively erase it.

Both Claude reports remain UNVERIFIED for L1. Complete reading does not
establish caller pool construction, installed-client compatibility, Kotlin/JVM
execution, reading-quiz behaviour or phone acceptance.

The GPT confirmation ran at 06:28:14.735-06:33:45 under the same
reservation, after the corrective Claude pass had ended. Its execution record
shows 41 file views, one at a time: the packet instructions, response, full
patch and gate outputs, all eight revised cards in full, its own initial
report, and exactly the sixteen permitted original comparison cards
(技 腕 企 承 担 職 位 了 完 済 敷 分 軽 乗 査 関). It made six permitted
public dictionary fetches (Daijisen entries for 担, 職 and 位) and wrote one
report. It used no shell, search, enumeration, corpus scan or outside local
path. The fetch tool automatically spooled one oversized web response to a
temporary file; the reviewer disclosed this and did not open or modify it.

GPT checked all fifteen post-fix default meaning-option sets and the reverse
direction for all sixteen counterparts: no curated distractor is removed and
no triple gains an internal exclusion. By static reading of the supplied
`QuizBuilder.kt`, each added pair is rejected with either member as target and
among chosen wrong options, for any caller-supplied pool. It resolved F1-F6,
reported no findings or optional items, and returned UNVERIFIED solely
because L1 remains partially resolved.

## Final outcome

| Item | Claude | GPT |
|---|---|---|
| Initial verdict | NEEDS FIX (2 + polish) | NEEDS FIX (6) |
| Confirmation of fix `737cb020` | All resolved; O3 decline accepted | F1-F6 RESOLVED |
| New findings | None | None |
| Confirmation verdict | UNVERIFIED (L1 only) | UNVERIFIED (L1 only) |

No joint CONFIRMED verdict is claimed. There is no outstanding content
finding. The residual L1 is an evidence limit: importer/field propagation,
actual pool construction, executed Kotlin draws, custom or multi-borrow
reading pools, native rendering, phone acceptance and older-client
compatibility were not executed. No further review round was run; those
limits require native/phone work, not more textual review.

## Evidence preservation

The initial packet uses a flat checksum manifest plus `packet.json`, unlike
earlier batches. The closure helper retains its exact checksum manifest and
copies bound supporting files byte-for-byte, compressing large XML evidence.
Snapshot and corpus files are represented by recorded hashes and the pinned
Git revision rather than duplicated wholesale in the closure. The packet's
6,278 `repo/` files were rechecked against freeze `d6ad96eb`: 704 match the
Git blob exactly and 5,574 differ only by CRLF line endings, so all are
recoverable from Git. The 3.5 MB public Joyo PDF is likewise kept as a
hash only.

`scope-audits/` holds the automatic audit for each run plus two manual
observation records: `confirm-claude-observations.json` (the rejected first
confirmation's scan and coverage gap) and `confirm-gpt-observations.json`
(acceptance of the GPT confirmation's scope).

Received prompts, including coordinator/user framing where present, are
preserved separately from authored prompt files. Reports retain their exact
bytes. The first Claude initial audit originally hashed newline-normalized
text; the corrected raw-byte audit is the one used for this record, and the
original audit remains preserved outside it. An audit records activity and
coverage; it does not itself accept a linguistic review. Variable-based shell
reads and scans require manual interpretation rather than treating automatic
"none" or empty scan lists as authoritative.

The two confirmation packets bind 41 files each. Their manifests are:

- Claude: `c6b725c6ae290a963f2dc9f650e4996b4d8103c1f23bdebe28a87f1da5cda29a`
- GPT: `5853deae7b1ce2778fbfd64f02bd2fe3bfc76c87d92fd5222e6ce45b101c90a2`

They contain the revised cards, exact fix patch, neutral change list,
reviewer-specific author response, six complete cited JMdict entries,
relevant Joyo extracts and the supplied meaning-quiz builder. An author
response is a claim for independent checking, not evidence. Neither
confirmation packet exposes the other reviewer's report.

## Existing host gates and accounting

The signed fix passed the existing host gates: 431 Python tests, content
validation with zero errors, scoped lint with zero errors and eight existing
word-article warnings, meaning-quiz audit with zero errors/warnings, vocabulary
check 2122/2431, and unchanged manifest after regeneration. Closure gates
rerun on the closure commit are recorded in `batch-112-progress.json`;
publication evidence is recorded separately.

The runtime manifest version is `b81044aafa8b5a07`. Its `files` dictionary has
7,747 entries; all nine runtime sections together contain 8,601 entries.
Those are different counts, not contradictory measurements. The committed
manifest SHA-256 is
`ab01e94fa5ffa384ff05bcb8184f67004c998e97fc2c9907d503198d14cefda2`.
There are 1,191 kanji and 5,082 word articles.

The fix's local working-tree ZIP budget is 8,608 files / 8,623 entries,
45,408,039 retained bytes, 45,679,349 inflated bytes and 30,685,740 compressed
bytes; listening-task media contributes 5,893,602 bytes. A local CRLF budget
is not an exact GitHub ZIP receipt. Published LF bytes and exact remote
archive hashes must be checked separately.

Before publication, source accounting remains 180 published N1 additions,
six pre-existing N2 placements and 1,042 unpublished frozen pending rows.
Publishing these fifteen would yield 195 N1 additions, 201 present frozen
pending rows including the six N2 placements, and 1,027 still absent. A
present draft is not counted as a published delivery.

The bounded reading-exposure model reports zero full-pool hits, zero
single-borrowed-target Starter hits and eleven latent entries. It is not
proof about arbitrary custom/caller-built pools or multiple borrowed targets.
No new reading or selection changed in the fix, and meaning exclusions do
not affect reading questions.

No JVM, Gradle, emulator, browser, native rendering or phone acceptance is
claimed. The older `5c000bd` APK predates kanji meaning exclusions; these
content changes do not make that installed client enforce them. Native and
phone acceptance remain separate from this bounded textual review.
