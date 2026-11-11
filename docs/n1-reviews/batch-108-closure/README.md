# Batch 108 (勧): three-family textual review closure

This directory closes the independent textual review of batch 108 and preserves
its evidence. The batch adds one N1 kanji card, 勧, and one new support word,
勧告. Three reviewers from three different model families read the frozen draft
(`9955ac12`), one found a minor unsupported claim, the claim was deleted in
`6547715c`, and all three confirmed the corrected text.

The teaching content reviewed here is byte-identical (same Git blobs) at the
integrated head `60d7892a`, which contains `6547715c` plus a merge of
`origin/main` `21a22764`. The integrated tree was then checked mechanically (see
below). No native, rendered, phone, CI or archive credit is claimed by this
record; publication is recorded separately.

## Teaching scope

| File | Change |
|---|---|
| `kanji/勧.md` | new N1 card |
| `strokes/勧.json` | generated stroke data |
| `words/勧告.md` | new word (かんこく), unlevelled kango |
| `words/勧める.md` | links to 勧; `quiz_exclusions: [推薦, 提案]` |
| `kanji/告.md` | one new Common-words bullet linking 勧告 |

At the reviewed snapshot the payload went from 8,474 to 8,477 manifest entries
(kanji 1,130 to 1,131, strokes 1,130 to 1,131, words 5,080 to 5,081) and
`contentVersion` from `edcfcbb8a57f26d2` to `da08658f4feb79ea`.

## Reviews

All times are UTC on 2026-11-10. The runs were serial and did not overlap; each
exited with code 0. The actual model is taken from each session's usage record,
not from the requested model. Claude and GPT gave all-facet initial reviews. The
Grok initial review had comprehensibility (including scoped coverage of
`words/勧告.md`) as its primary facet.

| Run | Actual model | Snapshot | Window | API requests | Confirmation primary facet |
|---|---|---|---|---|---|
| `initial-claude` | claude-opus-5.5 | `9955ac12` | 20:07:04-20:09:46 | 28 | correctness |
| `initial-gpt` | gpt-6.1-sol | `9955ac12` | 20:10:18-20:13:26 | 22 | consistency and quiz safety |
| `initial-grok` | grok-4.7 | `9955ac12` | 21:20:46-21:33:20 | 30 | comprehensibility |
| `confirm-gpt` | gpt-6.1-sol | `6547715c` | 21:57:26-22:04:13 | 32 | |
| `confirm-claude` | claude-opus-5.5 | `6547715c` | 22:05:15-22:07:04 | 38 | |
| `confirm-grok` | grok-4.7 | `6547715c` | 22:07:43-22:10:47 | 40 | |

Every reviewer was bound to the same snapshot, rubric and source extracts and
authenticated the snapshot by separate serial reads. The initial Claude run
continued an earlier session whose first attempt was denied the HEAD/reference
reads; that denial and its unaccepted report remain in
`../batch-108-textual-862/` and carry no review credit here.

`reports/` holds the six verbatim reports, `prompts/` the exact prompts and
`scope-audits/` the read-scope and model-identity audits. An audit's
`reviewAccepted: false` is by design: it records read scope and model identity
only, not acceptance. `confirm-packet/` holds the four-part common packet shown
to the confirmation round (gzip, byte-exact) and its provenance.
`records/third-family-completion-870.json` and
`records/revised-textual-closure-873.json` are the earlier coordinator records,
kept unchanged; their `published`, `batchAccepted` and remaining-work fields
describe the state at their own time and are superseded by this record and the
batch ledger.

## Reconciliation

| Item | Disposition |
|---|---|
| Grok, Minor, `words/勧告.md:15`: the clause teaching a recipient marked with に was asserted without an example or attestation in the supplied extracts. Grok did not claim it was wrong. | Resolved by deleting the clause in `6547715c`, the only teaching change; the generated manifest was regenerated. All three families then returned CLEAN with no findings. |
| Claude and GPT initial CLEAN verdicts had accepted the same clause. | GPT withdrew its evidentiary endorsement and Claude conceded it had accepted the clause without attestation. Neither asserts the construction is false. |
| Grok's report said 警告.md line 15 was not returned. | Factually mistaken: the blank original line 15 is present in part 07 and part 08 resumes at line 16. The verbatim report is unchanged and the correction is in `records/third-family-completion-870.json`. |
| Grok made five redundant tail rereads after complete views. | Protocol deviation recorded in `scope-audits/initial-grok.json`; no exactly-one-read claim is made for Grok. |
| Claude optional notes: punctuation of the new `kanji/告.md` bullet; 相談's title beside 勧告 in English-to-Japanese quizzes; 募 as a tag fallback for 勧. | Optional and tentative, restated unchanged in the confirmation. Not adopted. |

The confirmation round satisfied the repository rule that a new word card needs
three reviewers from three model families, covering correctness, consistency and
quiz safety, and comprehensibility, with scoped coverage reported separately.
Claude held correctness, GPT consistency and quiz safety (counts, navigation,
source records, manifest), and Grok comprehensibility. The original blind
reports were not relabeled.

## Byte identity

`provenance.json` records, for the five teaching files, the Git blob at `6547715c`
and at `60d7892a`; all five are identical. The packets printed Windows-form
(CRLF) raw SHA-256 values while Git stores LF. The CRLF reconstruction of each
blob at `60d7892a` equals the confirmation-packet label for the four articles
it printed, and equals the initial-packet label for 勧, 告, 勧める and
`strokes/勧.json`. The initial-packet label for `words/勧告.md` differs, as
expected, because it predates the deleted clause. The same CRLF/LF portability
is described for historical inventories in
`../../n1-sources/batch-108-byte-form-erratum.json`.

The SHA-256 of the confirmation packet's own `provenance.json`
(`12dfd1dd...20fa0`) equals the `commonPacketSha256` of the earlier closure
record; each of its four parts matches the gzip-compressed copies here.

## Integrated-tree checks (mechanical, not reviewer credit)

At `60d7892a`: lint 0 errors and 3 warnings; 431 unit tests pass; validation 0
errors; budget 8,503 entries, 44,944,819 retained bytes, 45,216,129 inflated,
30,466,248 local ZIP bytes; vocabulary 2122/2431; manifest rebuild shows no
diff. The Android JVM `RealContentTest` (3 tests) and `RareHanTest` (1 test) ran
with no skips. The merged-in main content (みっちり, four articles, images, policy
text) is unrelated to 勧告 and 勧める and changed no reviewed teaching, so the
merge needed mechanical re-validation only.

## Limits

- The reviews predate the merge of `origin/main` `21a22764`; the combined tree
  is covered mechanically only.
- Reviewers assessed supplied hashes, counts and extracts; they did not
  recompute them or perform fresh dictionary lookups. Claude marked the
  140-N1-card histogram unverified because no baseline histogram was supplied.
- No native emulator, rendered, physical-phone, older-client, handwriting or
  global quiz-safety credit. The repository's batch cycle does not require a
  native run per batch; one native smoke is planned for a milestone or the final
  acceptance.
- The multi-megabyte session event archives of the reviewers remain local and
  are not committed.
