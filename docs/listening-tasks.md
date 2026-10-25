# Japanese listening task packages: schema 1 contract

The [N4 profile and rollout](listening-n4.md) defines a reviewed schema-2/N4 extension
with the same task shapes and guided policy. Its linked software/media work is still pending;
this document remains the existing N5 contract, not permission to publish N4 packages early.

Companion to [app contract 1](https://github.com/stop-cran/kanji-cards-android/blob/main/docs/LISTENING-TASKS.md)
for app #66 and content #38. **Independently reviewed contract, adopted under delegated autonomous decision-making.**
B adds compatible validation, manifest/budget tooling and the app's shared data/media foundation.
General-release publication waits for C/D's renderers and E's exact-output approval and device gates.
The explicitly authorized [owner-testing publication](#owner-authorized-testing-publication)
allows the selected content to reach the owner's installed app before device acceptance is complete.
The [existing English-question schema](listening-n5.md) and its 36 approved passages are unchanged.
These reviewed conservative defaults are adopted under delegated autonomous implementation
authority, not recorded as separate personal confirmation. Paid-media authorization
and actual listener/device approval remain separate requirements, not inferred consent.

## Publication envelope

Keep manifest `schemaVersion: 1`. New optional maps contain path-to-SHA-256 strings:

| Map | Flat paths | Hash |
| --- | --- | --- |
| `listeningTasks` | `listening-tasks/<id>.json` | LF-normalized UTF-8 JSON bytes |
| `listeningTaskAudio` | `task-audio/<name>.ogg` | Raw bytes |
| `listeningTaskImages` | `task-images/<name>.webp` | Raw bytes |

Include the new maps in `contentVersion`. Never put them in `files`, `listening`, `audio` or
`images`; an older client must ignore both new documents and short recordings. Keep these map
shapes stable; future unsupported task documents must not force decoding their unreferenced media.
Only a new app's wanted-file list expands. Old archive size/inflation/entry checks still apply.

## Package shape

All IDs are lowercase ASCII kebab-case; filenames exactly match IDs. All numbers are integers,
text is nonempty plain text, arrays retain authored order, and references are closed within a package
except optional existing word articles. Scored IDs are unique across legacy and new catalogs.
Omit optional fields instead of writing null; numeric strings are not integer fields.
Unknown schema/policy versions or task types are unsupported. Unknown fields in a supported version
are errors; new grading/presentation requirements need an explicit version, not silently ignored metadata.
The four [structural examples](listening-task-examples/) are original **unapproved documentation
fixtures**, not runtime content, approved pilots or spend authorization.
The four [E pilot sources](listening-task-pilots/coverage.json) are separate original learning
packages. Their final recordings, along with the full pool and
[eight selected illustrations](listening-task-pool/illustrations.json), are published under the
[owner-testing authorization](listening-task-pool/publication.json). Contributor drafts remain
outside runtime namespaces. Coverage distinguishes authorized runtime use from outstanding
general-release device/full-section acceptance; structural documentation fixtures never supply the pool.

| Field | Contract |
| --- | --- |
| `schemaVersion`, `policyVersion`, `jlpt` | Integers `1`, `1`, `5` |
| `id`, `exposureId` | Scored/example identity and explicit shared-story identity |
| `taskType` | `task-based`, `key-point`, `verbal-expression`, `quick-response` |
| `kind` | `dialogue` or `monologue`; two or one speaking character roles, excluding the narrator |
| `usage` | `scored` or `example`; examples never enter SRS or scored denominators |
| `blueprint` | Optional `n5-section-v1`; marks scored pool members or the corresponding worked examples |
| `title`, `topic`, `levelRationale` | Neutral English context and justified N5-oriented difficulty |
| `speakers` | Unique `{id, role, voice, ratePercent}`; role `narrator`/`character`, Japanese stock voice and -15..0 rate as in legacy authoring |
| `turns` | Unique `{id, speaker, text, translation, spokenText?}`; Japanese source, English translation, optional approved pronunciation expansion |
| `stages` | Ordered `{id, role, turns, optionId?}`; turn-ID list in exact recorded order; `optionId` only for a spoken choice |
| `choiceMode` | `text`, `visual` or `audio`; rules below |
| `options` | Ordered `{id, number, label, translation, rationale}`; fixed consecutive numbers 1..N, Japanese label and English feedback |
| `answer`, `evidence`, `explanation` | One option ID, nonempty supporting story-turn IDs, English explanation of that actual task |
| `visual` | Optional `{role, description}`; role `context`/`required`, neutral English description of all relevant scene evidence, not the answer |
| `vocabulary` | Optional existing-schema vocabulary tips, maximum 30, with valid optional word references |
| `media` | Absent while authoring; complete generated output object below |
| `approval` | Exact-output publication authorization; normally full listening/device review, or an explicit documented owner-testing exception |

Bound packages to 4 speakers (exactly one narrator), 32 turns, 8 stages, text fields of at most
2,000 characters (turns/labels at most 500), and one composite picture. Every turn and character
speaker is used; every stage references existing turns. Repeated focus may reuse the same turn.
Evidence includes a `passage`, `situation` or `utterance` turn, not instructions/choices alone.
Only task-based/key-point allow `text` or `visual`, with four choices. Visual choices use one
required numbered map/grid and number-only buttons; labels are feedback/described-study text.
Expression requires a scene with the target role indicated and three audio choices. Quick response
requires three audio choices and **no picture**. No task option shuffling in version 1.

| Type | Required stage roles, in order |
| --- | --- |
| Task-based / key-point | `instruction`, `focus`, `passage`, `focus-repeat` |
| Verbal expression | `instruction`, `situation`, `choice`, `choice`, `choice` |
| Quick response | `instruction`, `utterance`, `choice`, `choice`, `choice` |

Focus-repeat uses exactly the initial focus's turn list. An audio-choice stage has exactly one
turn, linked to the corresponding option, in number order. Its displayed source text is
`<number>。<label>`; `spokenText` may expand the numeral/pronunciation without changing the meaning
or audible number. Exact listening approval checks the **heard** number too, not only JSON equality.
Required first choice plays are evidence, not replay help.

Japanese instruction/focus/utterance and spoken-choice texts stay hidden during normal scoring,
except the generic instruction text. Text choices and required pictures are visible; feedback
includes the captured Japanese, translations, all rationales and evidence. Deliberate guided text
help is assistance, not an accidental accessible-name disclosure.
Before exposure, discovery/preflight shows only neutral titles and task types; topic, level
rationale, IDs and feedback metadata are not additional learner hints.

## Generated output and approval

`media` contains:

```json
{
  "contentSha256": "<semantic-package hash>",
  "audio": {
    "<stage-id>": {
      "path": "task-audio/<name>.ogg",
      "sha256": "<raw audio hash>",
      "durationMs": 1200,
      "turns": [{"id": "<turn-id>", "startMs": 0, "endMs": 1100}]
    }
  },
  "image": {"path": "task-images/<name>.webp", "sha256": "<raw image hash>"}
}
```

The image member is present iff `visual` is present. Audio keys exactly match all stage IDs.
The same unchanged focus/instruction recording may be referenced more than once; duration counts
at every playback occurrence, bytes only once. Timings cover every stage turn in order, with
nonoverlapping positive intervals inside the exact recording. No arbitrary gap/padding to meet
a minimum duration. Target mono Ogg Opus at 32 kbps; allow **250-90,000 ms per clip**, at most
**150,000 ms across all stage occurrences per package**, and at most **512 KiB per audio file**.
Validate Ogg/Opus framing, sequence/CRC, declared versus measured duration within 100 ms, hashes
and actual platform playback. Do not weaken the legacy 15-60-second envelope.

WebP remains at most 150 KiB, decoded sides 1-2048 pixels, displayed downsampled to at most 512
pixels. An optional contextual visual may be omitted in the authored package; a declared but missing
asset is not permission for a fallback. A required picture's absence cannot become a wrong answer.

Canonical JSON follows the existing integer-only listening convention: recursive sorted object keys,
preserved arrays, unescaped Unicode, no optional whitespace, UTF-8. `contentSha256` hashes the whole
package excluding only `media` and `approval`. `mediaSha256` hashes the complete `media` object,
including paths, all hashes, timings, durations and the content binding. This avoids self-reference
while binding every output, not just the first clip.

`approval` is `{status:"approved", contentSha256, mediaSha256, reviewedOn, note}` with an ISO date
and an explicit account of the authorization and actual listening/visual coverage. It is an author
declaration, not cryptographic certification or proof of device testing. Both hashes must match.
Any changed learning text, option, order,
picture, pronunciation, timing or audio invalidates approval. Cached byte-identical synthesis can
be reused after renewed package review; updating metadata alone does not constitute approval.
No media is a valid pending draft. Partial/mismatched declared media is an error, not an approved
subset. Complete media without approval remains an explicitly unapproved draft.

### Owner-authorized testing publication

On 2026-10-25 the owner explicitly requested publishing the 32 selected packages for personal
testing, rather than blocking normal-app access on unperformed physical-phone/full-section
acceptance. This supersedes those **publication prerequisites for this bounded trial only**;
it does not claim the checks passed, change the schema, weaken media integrity or grant paid generation.
The [publication ledger](listening-task-pool/publication.json) identifies the exact authorized outputs.

Use the existing `approval.status: "approved"` as runtime permission for those exact packages,
with `approval.note` explicitly identifying **owner-authorized testing** and outstanding checks.
Schema 1 does not have a separate trial flag: the current app will make these items available for
ordinary guided practice and eligible diagnostic sessions, including normal exposure/SRS policies.
The public repository is not access-controlled to the owner; this scope describes the authorization,
not a claim that other users cannot download it. This is not general-release or proficiency certification.

Verify the frozen source packages, every stage/asset, selected picture, both canonical hashes,
identities, final manifest and complete-archive budgets before publishing. Retain private runs and
record a sanitized exact-output publication ledger. Do **not** invoke `approve-task` with fictional
`--phone-reviewed`, `--native-reviewed` or `--listened-all-stages` flags to satisfy the default exporter.
A specifically authorized publication may materialize the verified packages/assets directly under
this policy, without creating false review receipts. The default renderer approval/export commands
remain strict for ordinary publication; future trials require their own explicit scope.

Compatibility remains a design requirement, not a reason to withhold this authorized trial.
Keep new short media out of legacy maps and isolate unsupported versions/items with visible notices.
The current importer isolates unknown task versions/types; malformed supported content can still
preserve the previous new-task catalog. Further per-item corruption isolation is separate app work,
not permission to silently accept bad assets or block this valid batch.

## Identity, originals and review

Keep scored identity for cosmetic/equivalent changes. A genuinely different tested skill gets a
new scored ID, but shares `exposureId` if it reuses the story. Legacy stories default to their
existing passage ID. Keep a ledger of both IDs, context, objective, evidence and any reuse;
renaming is not independent transfer or a reset of familiarity. Never silently rebind an existing ID.

The [official source record](listening-task-sources.json) supports format decisions, not borrowed
content. Write original situations and pictures. Review whole task/role/register/translation,
every distractor and feedback branch, N5 spoken demands, graphic reference frame and all disclosures.
See the [shared review instructions](../.github/copilot-instructions.md).
Render and inspect the real phone-sized picture in both themes. Alternative descriptions must not
name the key or silently replace a visual listening task with easier textual evidence.

Contract 1 offers described **unscored study** when a learner chooses nonvisual presentation for
required graphics; it does not claim a scored equivalent. Audio-choice accessibility labels expose
only numbers until authorized help/feedback. Test actual C/D presentation and all required stages,
not just a file player or representative voice preview.

E first authors/reviews/listens to one original scored pilot per type. The separately authorized
full pool has 28 scored tasks (8/7/6/7 by type) including those pilots, plus four separate worked
examples. All 32 stories are independent. Examples have `usage:"example"` and cannot supply
scored content or leak the answer-bearing story of another selected item.
Each group shares equivalent generic Japanese instructions; its example instruction supplies that
group's assessment introduction. The actual stage order and every spoken option need exact-output
approval. Decode success, ASR, a text review or a filename is never listening approval.

Keep approved synthesis provenance, not credentials, endpoints, private logs or PCM caches.
Paid previews/pilots require explicit bounded authorization; after accepted pilots, the remaining
pool requires **fresh** explicit authorization. This document does not grant either.

## Practical authoring sequence

Use the [scoped contributor instructions](../.github/instructions/listening-authoring.instructions.md).
The first 32-package pool and its illustration revision established the following working sequence.
These are authoring lessons, not additional runtime fields or an official difficulty calibration.

1. **Design the task before the media.** Record the independent event/story, tested operation,
   roles/register, answer evidence and the division between heard and visual information.
   Keep discovery titles neutral. Compare against existing stories as well as IDs; the first
   pool replaced an invitation-refusal draft that was too close to a legacy episode.
2. **Write and review the complete exchange.** Read every possible response in the speaker's
   role, including translations and all feedback. Distinguish request, offer, permission,
   ownership and event stage. Plausible other-role alternatives made the door, card, floor
   and checkout illustrations genuinely necessary; removing redundant role narration alone
   was not enough. Do not turn a fitting refusal into an incorrect answer.
3. **Calibrate natural length from actual pilots.** Measure the intended voices/rates, then
   shorten or expand the meaningful dialogue, not silence. Reread the entire revised task:
   shortening previously left a denial replying to a deleted question. Check modality in
   translations and avoid feedback deductions unsupported by the conversation. After recording,
   calculate the shortest and longest permitted forms, counting repeated stage occurrences
   but deduplicating stored bytes.
4. **Agree on representative artwork before a whole image batch.** Default to the soft,
   natural animated/editorial still style used by the onomatopoeia cards, with
   `tools/image_prompts.json`'s shared `style`. Show a people scene and, when applicable,
   a numbered grid. The first schematic pictures were legible but did not meet the owner's
   visual preference. Style review and answer-evidence review are separate checks.
5. **Generate to explicit visual invariants.** The
   [selected illustration catalog](listening-task-pool/illustrations.json) preserves prompts,
   generation settings, final hashes and marker coordinates. Specify role positions,
   object count, size/color mapping, action state and crucial props. Check the *output*:
   both hands must hold the box; the door must be closed; the camera must face its subjects;
   a finder must be distinguishable from an owner; a mop must connect to the cleaner's hands.
   Do not rewrite accepted audio/options to excuse a contradictory picture.
6. **Add only necessary controlled marks.** Generate text-free scenes, then place a single
   high-contrast, outlined role arrow using the actual person's position. Add grid numbers
   in fixed order with equal treatment of all choices; never an arrow to the correct cup.
   Keep marks clear of faces, hands and diagnostic props. Ordinary natural scenes should
   not become diagrams, but natural shading must not obscure the task's distinguishing features.
7. **Review the final learner-visible form.** Inspect marked 512px output and 256px previews,
   then native light/dark rendering and required accessibility behavior. Keep text, alt
   descriptions, labels and feedback from leaking answers before the permitted stage.
   Listen to complete audio order, every audible option number and difficult counters,
   not just a representative voice. Browser playback and native instrumentation are useful
   evidence, not substitutes for a listener or physical-phone acceptance.
8. **Publish only the selected, correctly bound version.** Preserve earlier comparisons,
   source art and frozen runs. Record owner text/audio/artwork acceptance accurately.
   Keep any missing exact-output/device gates explicit rather than repeatedly asking for
   acceptance already given or silently transferring approval. If the owner explicitly authorizes
   a testing publication, follow the bounded exception above instead of withholding all app access.

### Image generation and adoption

Reuse the existing image generator's generation/conversion helpers; its word-card `--apply`
workflow and article-bound scene receipts are **not** a task-image exporter. New task art
belongs in the task authoring catalog until guarded runtime export selects it. Keep raw
service responses, account bindings and billing records private.

Before sending a batch, inspect the actual deployment's quota and applicable token prices.
Pace consecutive requests; the illustration run encountered a 429 between successive
requests until start-to-start spacing was added. Honor `Retry-After` as well as the deployment's
request interval. Reserve for every actual HTTP attempt, distinguish provider-reported token
cost estimates from conservative retained reservations, and reconcile any attempt-ceiling
amendment without erasing prior charges or increasing the owner's monetary allocation.
Do not estimate one model's token consumption using another model's image-price calculator.
An uncertain response is not permission for an automatic second potentially billed request.

For an **image-only revision**, keep the original plan, packages and media immutable.
Create a new plan with the unchanged draft documents and the selected WebP files.
Reuse only request-matching verified stage/preview receipts and byte-identical encoded
audio: text, `spokenText`, voice/rate, renderer identity, stage order and every timing
binding must still match. Verify the rebuilt packages with the normal renderer/validator;
the new image path/hash changes the complete `mediaSha256`, not the learning-content hash.
Do not copy spending authorization, preview/package/device declarations or old release
approval into the new run. Record the precise scope of any owner acceptance against
the selected bytes, then satisfy the applicable release gates or explicit owner-testing authorization.
No synthesis is necessary
when all required audio is already verified.

The selected WebPs and their former SVG schematics remain in `docs/` for authoring and
comparison, outside the runtime image map. Include **both** in complete-archive budget checks;
ignored documentation still occupies download/inflation space. Guarded general-release export or
the explicitly authorized testing publication adds the selected bytes to `task-images/` and
authorized packages to `listening-tasks/`.

## Private task-stage rendering

`tools/render_listening_tasks.py` adapts the shared `book-skills` synthesis engine;
it does not alter that engine or the legacy `listening.py` passage bounds. Normal
Content validation uses PyYAML/Pillow; renderer tests additionally use `requests`
with a fully mocked transport (also installed by content CI).
Rendering uses the shared engine's environment (`requests`, `azure-identity` and
`imageio-ffmpeg`); `--engine` points to its `reference` directory. No keys are saved.

Use a **new private run directory outside this repository**, not a folder that
could be committed. Supply reviewed draft JSONs without `media`/`approval`, the
exact WebP for every declared picture, explicit `task-id:turn-id` preview choices,
and the intended existing resource/subscription. Planning performs no synthesis
or Azure login. It freezes all learning text, voices/rates, pictures, preview
selection and renderer/validator versions. The previews must cover every voice/rate;
the author must also select the counters, numbering and role/pronunciation cases
that need auditioning.

For example, in PowerShell, with `$engine`, `$run`, `$resource` and `$subscription`
set to the intended paths/resource:

```powershell
python -B tools\render_listening_tasks.py --engine $engine --run $run plan `
  --content-root . --inputs <reviewed-task-json-paths> `
  --image "<task-id>=<reviewed-picture.webp>" `
  --preview-turn "<task-id>:<turn-id>" `
  --resource $resource --subscription $subscription
```

Repeat `--image` and `--preview-turn` as needed. The resulting `plan.json` and
all run records are private authoring artifacts, not content publication.
If a source, image, plan or renderer changes, stop and prepare a newly reviewed
run; a previous consent/approval receipt cannot silently transfer.

Only **after explicit owner spending authorization**, record that exact scope,
note and ceilings. `complete` covers the selected plan's previews and complete
packages, not any other tasks; `preview` prohibits complete rendering. The
applicable stock-neural USD price must be checked for the actual resource before
recording it; an example price or a previous run is not a quote or consent.

```powershell
python -B tools\render_listening_tasks.py --engine $engine --run $run authorize `
  --owner-authorized --scope complete --max-request-units <authorized-ceiling> `
  --max-usd <authorized-ceiling> --usd-per-million <verified-price> --note "<actual authorization>"
python -B tools\render_listening_tasks.py --engine $engine --run $run render `
  --allow-paid --phase preview --resource $resource --subscription $subscription
```

Accounting reserves allowance durably **before every HTTP attempt**, including
failed attempts, retries and split retries. It conservatively counts every SSML
code point twice, even otherwise exempt markup. This accommodates
[kanji's double counting and billable SSML](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech#billable-characters).
Both the cumulative request-unit ceiling and the quoted-price monetary ceiling
apply across preview/full phases and restarts. Failed requests are not refunded.
HTTP redirects are disabled and rejected, so they cannot silently replay an
authenticated POST outside this accounting or change its endpoint.
Do not reset `spend.json` or rewrite an authorization to regain allowance.
One writer holds `operation.lock`; after a crash, check that its recorded PID has
stopped before removing that one lock file. A missing/corrupt ledger is an error,
not permission to start again at zero.

Listen to `preview-review.html` and inspect the exact source/roles before using
`approve-preview --listened --reviewed-on YYYY-MM-DD --note "<actual listening>"`.
Only then may `render --allow-paid --phase complete` run within the same authorized
scope and ceiling. The renderer reuses verified turn PCM and identical stage
recordings, including the repeated focus. It retains exact stage-turn timing,
validates actual Opus decoding and counts every occurrence toward the 150-second
package cap. Ordinary fixed leading/trailing/inter-turn gaps are not adjusted to
make an undersized or oversized script fit.
Private cache receipts are keyed by the synthesis request; public audio filenames
address the encoded bytes together with their exact duration/turn bindings.
Freshly encoded reviewed revisions can coexist with old recordings, without
overwriting assets referenced by another package.

An owner may explicitly authorize **complete private generation before audition**.
Record that decision with `authorize --scope complete --defer-preview-approval`
and an accurate authorization note; the normal default still requires preview approval.
All selected previews must first be rendered and byte-verified, but this opt-in
does not create a listening declaration. It permits generation at the owner's
accepted risk of later rerenders, including a separately authorized full pool.
`approve-task` and `export` still require actual preview listening approval and
the complete package's listening/device declarations. Never manufacture those
receipts to satisfy a generation request.

`complete-review.html` plays each full required sequence and exposes all text,
translations and feedback for **unscored author review**. It is not the Android
C/D host, physical-phone acceptance, or automatic listening approval. Required
native/device checks must still exercise the exact packages in an explicitly
unscored author/test path without manufacturing a production approval.
The app's [`LISTENING-TASKS.md`](https://github.com/stop-cran/kanji-cards-android/blob/main/docs/LISTENING-TASKS.md#private-native-author-preview)
documents its isolated, release-signed native author-preview instrumentation.

After actual full-order listening, required-picture inspection, native playback
and physical-phone acceptance, `approve-task` requires `--task-id`, `--note`,
`--reviewed-on`, `--listened-all-stages`, `--native-reviewed`, `--phone-reviewed`
and, for a picture, `--visual-reviewed`. These are explicit human declarations,
not certification by the tool. They bind the whole current output and cannot
approve a missing stage, changed choice, changed picture or incomplete capture.

`verify --phase preview|complete` rechecks the private outputs without spending or
adding approval. `export --task-id <id>` publishes only selected packages with
matching exact-output and device receipts. It never copies PCM, credentials,
private plans or unapproved recordings. Existing different documents require
explicit `--replace`, and exposure identities may never be rebound. Export does
not rebuild manifests or commit: run normal validation, manifest generation and
complete-archive budget checks before publication, and retain sanitized provenance
in the coverage ledger. This tool does not waive E's pilot-to-full-pool gate.

## Static full-pool feasibility

After validation, approved-package export and manifest generation, run:

```powershell
python -B tools\check_listening_pool.py --root .
```

This read-only E gate emits JSON and exits **1** for missing/invalid content,
shortages, reused declared story identities or out-of-envelope timing. It exits
**0** only when its static checks pass. An empty catalog or the four pilots alone
must fail; do not add this as an unconditional CI gate while E is still in draft.
The report is bound to the current manifest content version. Stale manifests,
broken actual media, invalid approvals and unreferenced new media are errors,
not candidates silently dropped from a successful pool.

Only approved `n5-section-v1` members supply the minimum 8/7/6/7 scored tasks and
one independent worked example per type. Drafts, nonmembers and examples cannot
fill scored slots. Scored/example exposure IDs must be distinct across the pool
and from legacy stories. Unique IDs alone do not establish semantic independence:
the original-context/relationship ledger still needs editorial review.

For each type the checker sums its shortest and longest possible scored selections
(7/6/5/6), then adds the shortest/longest available example. Scored items omit the
generic instruction; each example includes its instruction once as the group
introduction. Repeated focus occurrences count twice even when their audio file
is shared. It includes the 5-second preview except for quick response, 15-second
focused or 10-second spoken-choice scored answers, and 10-second example answer
plus 10-second feedback windows. **Every** permissible form must lie within the
inclusive 26-34-minute envelope, not just an average or one convenient seed.

The default above remains N5-compatible. For N4, pass `--profile n4-section-v1`: only
schema-2/level-4 members contribute to the 16/14/10/16 minimum scored pool, the 8/7/5/8
selection and four independent examples. All forms must fit 31-39 minutes; fixed windows
total 550 seconds. N4 members cannot reuse another level's declared story identity.

For N4 F's **private, unpublished** complete candidate tree, use:

```powershell
python -B tools\check_listening_pool.py --root <candidate-tree> --profile n4-section-v1 --unpublished-candidate
```

Keep existing source packages/identities and a current generated manifest in that tree.
This explicit read-only mode validates actual media files and the same shape/hash/identity/
timing rules without requiring or creating approval. Missing media cannot fill the pool;
a malformed approval declaration is still an error, not silently ignored.
The report uses `candidateScoredIds`/`candidateExampleIds` and explicitly sets
`publicationReady` and `scoringReady` to false, even when `checksPassed` is true.
Normal checker/app entry still requires exact-output approval. Passing candidate feasibility
is not listener acceptance, spending authorization or permission to publish runtime content.

The report lists instruction wording variants for checking equivalence; different
wording is not automatically judged equivalent or wrong. Extra candidates in a
fork are included in the extrema rather than ignored. This does not expand E's
authorized 28+4 batch or grant spending permission. Actual full-order listening,
native/physical-phone acceptance, semantic/instruction review and the separate
complete-archive budget check remain required. F additionally checks current
learner exposure/cooldown/accessibility and the exact captured selection.

## Full-tree budget and rollout

The following records the historical contract-1 adjustment. [N4 B](listening-n4.md#media-budgets-and-publication-gates)
supersedes its capacities: app download/retained caps 48/64 MiB; publishing compressed/retained/
combined-task-media guards 42/56/20 MiB. Inflation, entry and per-file limits are unchanged.
An older 30-MiB app cannot fetch an oversized new archive and keeps its last accepted offline
content; deliver the upgraded APK before that publication. Capacity does not authorize spending.

The pulled `73bde0f` tree's local ZIP is 22,665,639 bytes, already close to the current 24-MiB
conservative publishing guard. Adopted contract 1 raises only that conservative guard to 28 MiB
in B, **not** the app's 30-MiB download / 50-MiB retained / 100-MiB inflated / 8,000-entry limits.
Retain the 40-MiB / 80-MiB / 7,000-entry publication guards. All new unique audio/images together
must fit 6 MiB; test the complete archive, including ignored documentation and existing media.
Update budget accounting for curriculum and the new folders in B. If real approved output cannot
fit, stop for a reviewed adjustment; do not lower quality or raise hard limits automatically.

`python -B tools/validate.py` includes task validation, while `python -B tools/build_manifest.py`
adds the three separate maps only when populated. `tools/test_listening_tasks.py` pins the same four
structural content hashes as the Android tests, exercises strict media/approval/reference rules and
checks namespace/budget compatibility. `validate_listening_tasks.check_listening_tasks` can also compare an
explicit prior task/exposure binding ledger; never rename or rebind scored identities to reset history.

Use [app contract 1](https://github.com/stop-cran/kanji-cards-android/blob/main/docs/LISTENING-TASKS.md)
for exact 26-34-minute form calculations, eligibility, guided grades, shared exposure, accounting,
interruption outcomes and B-F verification ownership. E checks the shortest/longest permitted
24-item forms against that blueprint without waiting for F. The full-form renderer follows later.
Old/new reader compatibility remains required design. General release requires B/C/D support,
actual exact-output approval and E's device gates; the scoped owner-testing exception above permits
earlier testing with truthful pending checks. A small pilot is not a full assessment pool.
