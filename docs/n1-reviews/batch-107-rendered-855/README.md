# Batch 107: independent native/rendered follow-up

The original Claude and GPT reviewers independently continued their reviews on
signed evidence snapshot `1d341ac022bb652ac38a6c39a589bce5cc51261f`. Both
accepted the changed articles and examples in the bounded review and found no
new blocking issue in the captured rendering or finite option samples.

The native run used content snapshot `996898d775c61af7188c6da5b4644b838f999236`,
whose runtime payload was unchanged from the final reviewed correction
`0b6be1de66c9681b208ee2d27f0253baed4052cc`. The shared packet, source records,
native data and screenshots are in the sibling `batch-107-native-853` directory.
The reviewers did not independently verify the commit signature or execute the
native tests.

## Reports and provenance

- [Claude report](claude-report.md) and [clarification](claude-addendum.md).
- [GPT report](gpt-report.md) and [clarification](gpt-addendum.md). The original
  report explicitly listed 42 rather than all 46 sampled distractors; the
  clarification assesses the four omitted from that enumeration.
- `claude-provenance.json` and `gpt-provenance.json` describe the original
  sessions, report hashes, serial text reads, permissions and event hashes.
  Their `imageModules` identify the two bounded image-read modules per reviewer.
  The modules losslessly retain the original audit data; the original path-bearing
  event archives remain local.

Claude's continuation shut down before GPT's began. Each made one read-only
`view` call per response, read the same complete text and source modules, and
viewed all 38 distinct original PNG representatives. The 27 other captured
screenshots were not independently viewed by the reviewers: a separate
mechanical check compared each original screenshot byte-for-byte with its
manifest representative. Permission requests were approved individually for
the exact metadata reads, without remembered path or directory grants.

The image-read records contain runtime-reported content-addressed PNG asset IDs
and sizes. The delivered asset bytes and dimensions were not independently
rehashed or measured. Both reviewers reported downscaled views, so their
judgments of fine stroke detail are approximate. Apparent differences in glyph
styling do not identify the actual resolved fallback face.

## Reconciliation and remaining limits

- Both reviewers accepted the retained direct 勘定/料金 safeguard, while
  preserving their earlier disagreement about whether it was necessary. It is
  a conservative context-free bill/charge safeguard, not a claim of unrestricted
  synonymy or a transitive exclusion.
- 勘/識 remains an unguarded hypothesis, not an established defect. The 64
  recorded production-option samples contain 46 distinct distractors and cannot
  establish global semantic safety.
- The pre-existing 定 `さだ.か` explanation gap and 違 `ちが.える`,
  `-ちが.える`, `たが.う` and `たが.える` gaps remain unresolved. The app
  can offer the distinct `たが.う` stem. The newly changed examples are accepted;
  neither whole reading table is represented as globally clean.
- The pre-existing 支払う/支払 ambiguity remains unresolved. The original
  reviewers disagreed on whether it needs a direct safeguard; this batch did not
  change or fix it.
- The screenshots came from an emulator, not a physical phone. The injected
  reference strokes were ungraded practice; a separate recall action
  intentionally recorded grade 1. The unavailable handwriting model means
  the run is not handwriting-recognition or mastery evidence.

This follow-up does not establish native-speaker approval, physical-device
acceptance, merged-tree validation, publication, general-release readiness or
global semantic safety.
