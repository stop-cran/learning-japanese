# English repository cross-PC preservation handoff

This is a preservation snapshot, not publication, review approval, or permission to
resume held work. No new tests, builds, review admissions, merges, or releases were
run for this handoff. Existing source files were copied without changing their bytes.
Do not treat the Python files under `code/` as newly validated production tooling.

## Remote preservation map

All branches below belong to `stop-cran/learning-japanese`. Worktree files and
ordinary indexes were left intact when creating the four draft snapshots.

| Branch | Preserved commit | Purpose |
| --- | --- | --- |
| `handoff/n1-b134-20261117` | Contains `b140716f5df6d17fb872f477556ef77d2cd59b0e`; the branch also receives this handoff | B134 authored card, corrections, signed review closure and concurrent-main merge; not released |
| `handoff/en-contract-draft-20261117` | `2ee9d1a5e59c13f942cadaafd5d14863c044749a` | Original EN language-contract draft, 13 source/content files including the separate four/nine wording changes |
| `handoff/en-contract-rebased-draft-20261117` | `8cec553b6b1fc13f56c605d06f57682d4c50888d` | The 11-file contract draft based on `625cc322`; no four/nine changes |
| `handoff/verb-completion-draft-20261117` | `478d0667b1cd38338e79e0d80e4d231cd6de9a4d` | Unreviewed 17-line article addition comparing exhaustive action with completion |
| `handoff/reading-review-dumps-20261117` | `0514ae45360eaf001d849505366e602bdbb42d5f` | Five original Momotaro inspection dumps; retained as evidence, not new content acceptance |
| `n1/legacy-audit-checkpoint-20261111` | `8e84c9d0748719ca33cc25c8fd434313030ffad8` | The five outstanding files in the old `content/n1-kanji` worktree are already preserved here |
| `n1/recovery-current-cli-fixture-20261111` | `96f0a089782c92345f85cce96c2537fef697384d` | All 19 changed/untracked current-CLI fixture files are already preserved here |
| `n1/recovery-legacy-cli-fixture-20261111` | `ac2fa6733abd5e8bf062f3fbfea12a1401c56e6d` | The legacy CLI fixture's modified auditor is already preserved here |

The original language-contract pilot (`36b986e8`) remains on
`en-language-contract-pilot`. The pre-existing local branch histories, other than
the superseded B129 candidate described in the issue checkpoint, are already
reachable from remote branches. No historical branch was force-pushed.

The audit covered both English Git groups: the primary checkout's 14 worktrees
and the separate N1/auditor group's 28 worktrees. Fifteen generated Python cache
files in the primary/reading worktrees were left local and untouched, not published.
Normal Git CRLF/LF normalization applies to some draft snapshots; content comparisons
found no substantive differences from their working files. The source copies in
this handoff use `-text` and `inventory.json` to preserve exact bytes instead.

## Current N1 state: B134, not the historical B116 checkpoint

The verified delivered count remains **271/1,228**, with **957 remaining**.
B134 would advance it to 272/1,228 only after its complete publication pipeline.
Pushing a handoff branch does not earn delivery credit.

The B134 member is the purple/violet card. Its lineage is:

| Role | Commit |
| --- | --- |
| Published B133 baseline | `e17cb97c53ca4e3193dae5e11b52ba517fe86e76` |
| Initial B134 authoring | `ba80afffc20a72d31be68b355b6f90aab36a5726` |
| First reconciliation | `355cccb840d22e7313e79f234eb93d1367e00352` |
| Corrected, revision-confirmed snapshot | `cc374051efa75199212a87c9abf08d7391419055` |
| Signed original review closure C | `ae1555736086fa6a7ee29c9707ba4b07e82bf979` |
| Previously integrated main | `830f740bdbe33ac2207acb491cd58e6ab3ab8b8b` |
| Signed two-parent integration M | `b140716f5df6d17fb872f477556ef77d2cd59b0e` |

M's ordered parents are C and `830f740b`. Its content delta from C is exactly the
numbers-and-counters article, `counters/kumiexpressions.json`, and regenerated
`manifest.json`. The manifest SHA-256 is
`ba2ecff171d5ace53d23553a91fdff2f244d3c2ed03a135aa65abc179f0a9b4e`.
The original closure and original/fresh/authorized revision review records remain
in `docs/n1-reviews/batch-134-closure/`; they have not been relabelled.

**Main moved again during preservation**, to
`e60c0298c5737aa29174e043417c678b4ad42e44` (the separate Ki-expressions article).
This handoff did not update main. Fetch and inspect the actual latest main before
planning any eventual integration: the existing 830f740b-pinned publication plan
is no longer sufficient. Do not silently substitute a new incoming commit in a
frozen plan or verifier.

## Existing evidence and unfinished work

Before the preservation pause, both merge-mode and committed-merge ten-check runs
passed, as did the object-preservation verifier. Their existing records are under
`scratch-134/review` on the original machine:

| Evidence | SHA-256 |
| --- | --- |
| `integration-merge-gates-003/summary.json` | `a98414c42db1d604f8986f467405b40b3188a50590a401f12bdeaad95b3218e4` |
| `integration-merge-committed-gates-001/summary.json` | `fafc37792f32690c71b8708ad6be5ba71ce27b6619b0d7da1de2eb18652675c6` |
| `integration-preservation-001/verification.json` | `1d399e894554de6c11ed66f06bdd46b89f2f181c72c108a8bab58612494edf23` |
| `integration-followup-prep-002/actual-plan-001.json` | `0ff4c5ed2818c665f5a37d9c299dd0b778f7cf8e937961335fef7873d74afcf4` |

Earlier failed attempts remain failures. Merge attempt 001 rejected missing sparse
checkout paths. Sparse checkout was backed up and disabled. Attempt 002 rejected
writable helpers; their bytes matched the signed producers and they were made
read-only before the successful attempt. No guard was reduced.

Integration confirmations are **not complete**. No integration closure I, publication
receipt R, publication ZIP/CI/equality acceptance, or B134 delivery checkpoint exists.

The previous same-Claude session exceeded its unchanged 740,000-token forecast
policy once all required complete source units were included. Preparation switched
prospectively to an explicitly labelled replacement Claude-family integration-impact
reviewer, not an original teaching review or same-session continuation. The new
session reached setup-only READY but was never bound or admitted.

GPT's actual prepared dossier forecast was 600,710/710,000:
419,340 retained input + 132,370 complete dossier + 49,000 reserves, with zero
compaction. Its preflight SHA is
`92d665d06bb93aae81732f96df74c753be9d25f2263136de9f0d4caf214d43e9`
and config SHA is
`f3eda596598e4fd5e446ed14941cb38528bb08eb80fc2c26d1b2a3aa98b871e5`.
Prepared does not mean admitted, reviewed, or accepted.

The local integration-followup implementation states are distinct:

- Runtime 005 (`dc2ee289348ca5a3faff97e1e950d04a110a521b85eb788bbbce022dd2c6c28a`)
  passed ten synthetic controls and the actual-M finalizer, but rejected the new
  session's additional canonical `system.message` during bootstrap binding.
- Runtime 006 (`c8a084a33cbbfd9b72c8071efa8efa28d51da35fea26612a4c08b14ea26f3115`)
  adds exact equality with the original accepted Claude system prompt. Controls 007
  failed: a test mutation targeted the wrong event, and nested RAM admissions failed.
- The latest draft corrects that fixture and isolates inner synthetic guards under
  the unchanged outer guard. It is **not revalidated**: attempts 008/009 were refused
  before a child started at 2,134,212,608 and 2,060,845,056 free bytes. There are no
  successful receipts for those launches.

Keep the strict **greater than 2 GiB** start threshold and **1 GiB** abort threshold.
Keep all source-depth, capacity/reserve, session-identity, no-compaction, independent
review, and serial-execution requirements. Do not use runtime 005 or 006 for admission.

## Continuing on the new PC

1. Fetch the handoff branches and existing work-item discussions. Start from the
   desired preserved snapshot, not a stale local `main`; leave main unchanged.
2. Read issues #60 (N1), #61 (language contract) and #65 (reading), including the
   dated preservation comments. The old language-contract drafts and verb addition
   are not reviewed or release-ready merely because they are signed and pushed.
3. Use `inventory.json` to locate the byte-preserved workflow source. `code/` stores
   each unique source by SHA-256; inventory entries map it back to its original
   workspace-relative or coordinator-session-relative filename. This deduplicates
   historical fixture copies and avoids Windows path-length failures. Old absolute
   paths and pinned local inputs are historical; this is not a ready-to-run installer.
4. Arrange secure migration of required private local audit evidence and App session
   state if continuing those exact sessions. Raw event JSONL, system prompts,
   authentication state, and private configuration were deliberately not published.
   The original copies were not deleted. A Git clone alone does not recreate a live
   reviewer, resident App authorization, retained context, or authenticated forwarding.
   Obtain new direct user authorization if the App requires it; never reconstruct
   authorization from a saved quotation.
5. After the pause is lifted and adequate memory is available, repair/revalidate a
   versioned successor against the actual environment and latest main. Preserve
   old failures. Establish actual reviewer identities/capacities before admission.
   If original sessions cannot be restored, make any replacement scope explicit;
   never claim same-session reuse or fabricate acceptance.
6. Only after real accepted integration confirmations: assemble the additive
   integration archive/ledger, run the exact combined-tree gates, sign I, fast-forward
   publish against the rechecked main, inspect actual CI and exact ZIP, record/sign R,
   verify R's CI/ZIP/served equality, and post the real #60 delivery checkpoint.
   Resume subsequent serial N1 batches only after that checkpoint.

Disclosed limitations remain: 58 exclusions at cc374051; the invented
non-etymological mnemonic; historical ツツム and the latent 紫/包 reading pair;
11 versus 12 strokes; 51 Notes warnings; 11 pre-existing fallback cards; missing
font-cmap support for 茈; no native, phone, custom-pool, rendered-font, or whole-set
acceptance. Preserve all original raw verdicts and the earlier authorization hold.

For GitHub writes, use the repository owner's account without changing shared
global authentication. Do not reuse inherited credential environment variables.
Use the configured owner signing identity and stop rather than retrying if signing
waits on an unavailable passphrase.
