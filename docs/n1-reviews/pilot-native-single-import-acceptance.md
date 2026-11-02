# N1 pilot native retry: bounded owner-testing acceptance

Content archive snapshot: `79360e975ccf54cb484994ddc2632b2c7dabc6b1`;
teaching snapshot: `bb448a25c522e9703d43e87216320c48a9121f1c`;
Android production: `f9b59a2bc5a203c6b4de26be50021a4c720dc22c`.
The original [fixture and failures](pilot-native-acceptance.md) are preserved,
not relabelled as passing. No production app code, algorithms, heap limits,
archive guards or teaching content changed in this retry.

## What passed

The [named retry fixture](pilot-native/N1PilotSingleImportRetryTest.kt)
passes the **complete exact Git archive** through production `ContentSync`
**once per route execution**, with no separate `ContentParser` preflight.
It uses a synthetic source/HEAD HTTP adapter, not public GitHub sync.
The [artifact index](pilot-native/execution-008-artifact-index.json) pins
the old fixture, every retry version, archive and retained receipts.

Assertions use the actual `SyncResult.Updated` and accepted Room metadata:
**997 kanji, 4,951 words, 17 N1-labelled kanji, zero problems**;
contentVersion **`92c2025be954cf03`**, reading parser epoch **1**, and no
Grammar, Listening or curriculum problem. The full source metadata stays
available: 漱 has four kun entries, an explicitly empty on quiz list and
the single approved kun question うがい.

One combined native case exercises real MainActivity routes:

- Select Kanji → N1 and display the 17-card exact-level collection.
- Answer 莉's meaning, follow the 茉莉花 article link, and use system Back
  to recover the same answer/ViewModel and then the Kanji page.
- Enter Readings, answer the actual curated 漱 / kun'yomi / うがい question,
  advance, and verify the source-scoped reading/grade log in Room.
- Enter Drawing, inject all 24 generated 鷹 reference strokes as touch input,
  check ungraded tracing feedback/reference, advance to recall, select
  “I don't remember”, advance and verify a drawing log, then system Back.

The emulator's Wi-Fi and mobile data were disabled before execution.
`ConnectivityManager.activeNetwork` was null both before MainActivity and
after the routes. These are actual offline cached-content checks, not just
an HTTP mock called “offline”. The drawing screenshot explicitly reports
shape-only grading because the handwriting model is unavailable offline;
this is not ML Kit recognition, human-handwriting or model-download evidence.

The [second attempt](pilot-native/execution-008-single-import-native-attempt-2.txt)
and [final fourth attempt](pilot-native/execution-008-single-import-native-attempt-4.txt)
each have terminal **per-case status 0**, respectively 34.634 and 32.574 seconds.
This is one combined case per execution, not seven independently isolated
test cases. The final execution's
[actual Room/route receipt](pilot-native/n1-retry-native-route.json),
semantics tree and all nine screenshots were exported successfully, with
terminal exporter status 0. The coordinator visually inspected all nine:
selection, meaning, support article, article Back, curated reading question
and feedback, drawing trace, tracing feedback and recall feedback.
No unreadable glyph, missing control or clipped answer was established in
those frames; this is bounded inspection at one emulator size/font scale.

## Environment and fixture corrections

Both owned emulator launches used explicit `emulator-5580`, after checks
found no connected device or occupied port:
`N3_Acceptance_20261029`, read-only, no snapshots/window/audio, host GPU,
Vulkan disabled, 2,048 MB guest memory and two cores. Both booted and responded;
both were stopped with explicit-serial `adb emu kill`. No owner device or saved
AVD configuration was modified.

API 35 fingerprint:
`google/sdk_gphone64_x86_64/emu64xa:15/AE3A.240806.036/12592187:user/release-keys`;
hardware `ranchu`, heapgrowthlimit **192m**, 1080 × 2400, 420 dpi, font scale 1.0.
JDK 17 and the existing SDK were used. Gradle had one worker and the quoted
in-process Kotlin compiler argument. Builds, native runs and exports were
serial; no reviewer was launched.

All failed attempts remain preserved:

- Attempt 1 imported successfully but asserted visibility of an offscreen N1
  summary. The fixture now scrolls to the summary.
- Attempt 2 passed. Its exporter was accidentally a local class, so discovery
  failed. The read-only emulator was stopped before the artifacts could be
  recovered; do not claim its screenshots were retained.
- Attempt 3 imported and passed meaning/article/reading routes, then reached
  Drawing's temporarily disabled Home Start action. The fixture now awaits
  the enabled action, not merely the already-present label. This is a harness
  readiness correction, not an app behavior change.
- Attempt 4 passed with the standalone exporter. Initial host decoding used
  the Windows default encoding for the UTF-8 JSON and failed after writing
  the eleven decoded files. Explicit UTF-8 verification then succeeded before
  shutdown. No bytes or original test outcomes were replaced to hide failures.

Fresh non-skipped Android checks also passed against **this sibling content
worktree**, with copied XML receipts: `RealContentTest` **3/3** and
`RareHanTest` **1/1**, zero failures/errors/skips. Both app/core
`../../learning-japanese` paths resolve here. Temporary test sources and
the complete ZIP asset were removed; the dedicated Android worktree is clean.

## Acceptance boundary

The unchanged production fonts inherit the earlier **40 targets × four
families / 160 probes and seven visually inspected screenshots**, not a
fresh full-font run in this execution. The four pilot fallback characters
remain covered there; new route screenshots additionally render 莉 and 漱.
No physical phone, native speaker, other OS/font scale, human drawing or
learning-effectiveness acceptance is claimed.

The delivered curated-reading prerequisite and the closed two-family
[curation review](pilot-curation-reconciliation.json) resolve the original
reading-prompt blocker: **19 offered keys, zero offered source-only keys,
all 47 full entries/order preserved**. Together with this native receipt
and the [updated estimate](../n1-sources/pilot-accepted-recalibration.json),
the twelve-card pilot is locally accepted for **bounded owner testing**.
The normal signed integration/publication/CI/immutable-ZIP gates still
determine delivery, recorded separately from local acceptance.

**Compatible Android `f9b59a2` or later is required**: older APKs ignore
curation, and old 8,000-entry clients cannot import this collection. The
normally owner-signed prerequisite APK is retained externally under
`control\artifacts\enso-nihongo-f9b59a2-curated-readings.apk`.
No phone was connected; transfer, phone installation, physical-phone and
general-release acceptance remain **explicitly outstanding**. Under the
approved issue checklist, that honest status is not a new veto on bounded
owner-testing publication.
