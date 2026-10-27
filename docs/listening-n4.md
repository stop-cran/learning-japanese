# N4 listening: authoring profile and rollout

Implements the reviewed design in [A / #48](https://github.com/stop-cran/learning-japanese/issues/48).
**This is the adopted design, not a declaration that the app, recordings or complete pool are ready.**
The [source ledger](listening-n4-sources.json) separates official evidence from project choices.
The [app extension contract](https://github.com/stop-cran/kanji-cards-android/blob/main/docs/LISTENING-N4.md)
owns runtime behavior and implementation status.

Use this profile with the [Japanese task contract](listening-tasks.md), its
[practical authoring sequence](listening-tasks.md#practical-authoring-sequence), and the
[scoped instructions](../.github/instructions/listening-authoring.instructions.md).
The [36 legacy passages](listening-n5.md) and existing schema-1 Japanese tasks remain N5;
their identities, grades, approval bindings and exposure histories are not reset.

## Target ability, not a speed label

The official N4 descriptor concerns following everyday conversations **spoken slowly**.
N5 emphasizes necessary information from short, slowly spoken conversations; near-natural
speed appears in the N3 descriptor. N4 does not mean normal-speed native conversation,
everyday slang at any density, or an arbitrary increase in TTS playback speed.

The four objectives remain task-based comprehension, key-point comprehension, verbal
expression and quick response. Understanding a conversation's overall meaning is useful,
but N4 has no separate general-outline or integrated-comprehension listening section.
Its approximately 35-minute section is not a per-dialogue duration requirement.

JLPT does not publish an exhaustive current vocabulary/grammar syllabus. The JLPT Can-do
survey reports learners' self-assessments, not mandatory test outcomes. Irodori Elementary
1/2 is useful communication-oriented reference material, not a one-to-one JLPT specification.
Write original content; source questions, pictures and recordings are not reusable templates
to copy, translate or lightly reskin.

## Coverage and independence

The first bounded pool has **56 scored tasks and four independent worked examples**:

| Family | Scored pool | Scored in one diagnostic | Worked examples |
| --- | --- | --- | --- |
| Task-based | 16 | 8 | 1 |
| Key-point | 14 | 7 | 1 |
| Verbal expression | 10 | 5 | 1 |
| Quick response | 16 | 8 | 1 |
| Total | 56 | 28 | 4 |

The 8/7/5/8 selection follows an observation from the 2018 official workbook, not a
guaranteed current or future item count. Doubling it is a project pool-size decision,
not proof of N4 adequacy, learning effectiveness or readiness to pass.

Maintain an authoring ledger of scored/story identities, operation, context/topic family,
roles/register, source/sense qualifications, answer evidence, heard/seen information and
relationships to existing material. Each core operation needs at least three independent
contexts across two topic families in the final pool:

| Operation | What the learner must resolve |
| --- | --- |
| Plans and changes | Proposed versus agreed arrangements, constraints, deadlines and action order |
| Reasons and conditions | The actual reason or applicable condition, not a rejected suggestion |
| Event stages | Intended/completed/outstanding actions, preparation, continuation and result states |
| Participants and favors | Who requests, performs, receives or reports an action |
| Descriptions and comparisons | Identify a person/object/place using relevant combined details |
| Interaction and repair | Requests, offers, permission, invitations/refusals, apologies/thanks and clarification |
| Practical details | Relevant times, dates, durations, quantities, prices or directions in communication |

Use home, school, work, shopping/services, transport, appointments/health and leisure.
Count an operation only when answering requires it. Incidental grammar does not fill a
coverage cell. A changed noun, voice, option order or picture does not create a new story
or prove transfer; compare against existing N5 material as well as new peers.

Existing N5 focused tasks already contain multi-turn constraints and some N4-associated
forms, with main passages around 39-54 seconds. Do not automatically reclassify them
from one construction, or count an accelerated version as new N4 content. A genuine
change of tested skill requires a reviewed scored identity; reused stories retain their
shared exposure identity. Cosmetic or equivalent-rendition changes keep both identities.

## Script and task design

- Start with the communicative decision, not a grammar quota. Make the answer depend on
  connected meaning: reference across turns, a meaningful condition, participant role,
  event stage or the actual purpose of an utterance.
- Keep one clear situation and a focused objective. Link clauses naturally, but do not
  simultaneously add obscure vocabulary, many speakers, dense nesting and several
  unrelated facts. Background words can be supported by context; unexplained specialist
  language must not be the hidden answer-critical test.
- A main-dialogue pilot around 30-60 seconds is a starting heuristic, not a hard minimum
  or level classifier. Short monologues and short responses remain short. Do not force
  every dialogue into the same turn count, pad silence, or add irrelevant speech to
  reach a section duration.
- Use polite and familiar exchanges where the relationship warrants them. Naturalness
  includes purposeful omitted subjects, backchannels, explanatory forms and selected
  ordinary reductions. Explain relevant spoken forms in feedback, including their
  expanded form where helpful; do not make everything casual or introduce dense slang,
  dialect, overlapping voices or background noise as default N4 difficulty.
- Keep a pre-announced spoken focus for task-based/key-point tasks. The former asks for
  the appropriate action; the latter for the specified information. Their common stage
  shape is not permission to erase the distinction or invent another reading window.
- Review every option as an actual utterance/interpretation in that context. A natural
  refusal, contraction or polite alternative is not wrong because it differs from the
  model. Wrong options may reflect a rejected proposal, another participant or an
  earlier event stage, but their explanations must not invent facts.
- Identify actual participants in role-sensitive feedback. Distinguish a receiving-side
  role from a benefit that occurred, permission from obligation, and an earlier plan
  from a completed event. Recheck translations, evidence and every dependent branch
  after shortening or revising a turn.
- Keep titles, labels and question-side help from revealing answers. Expression scenes
  must identify the speaking participant without making the audio irrelevant; include
  plausible other-role alternatives. Quick response has no picture. Preserve the
  approved animated/editorial still style, exact visual invariants and local crisp marks.

Keep these authoring annotations in the ledger and supported fields such as
`levelRationale`; do not add unversioned grading/presentation fields to strict runtime JSON.

## Speech calibration and learning support

Audition the actual voices, roles and complete task, including every spoken option number.
Candidate stock-voice settings around -10%, -5% and 0% are comparisons, not fixed N4 bands.
A percentage is relative to a particular voice/model; it is not an absolute speech rate.
The inspected official specifications provide no WPM target. Japanese orthographic word
counts also require a stated segmentation convention before they can support comparisons.

After the initial N4 auditions, the owner selected **-5% for longer, information-dense
speech and 0% for short speech**, rather than a fixed rate per voice. Apply this by
coherent passage or utterance, not a mechanical character-count cutoff. Keep a dialogue
at one pace, including its short backchannels, and keep all spoken alternatives within
an item at the same pace so speed does not hint at the answer. The
[pilot assignments](listening-n4-pilots/speech-selection.json) record the exact choices
and the shared-narrator exception for illustrated tasks. This is the cohort's delivery
choice, not an official N4 standard or a change to existing N5 recordings.

Preserve mora lengths, pitch/intonational phrasing and natural turn pauses while keeping
delivery accessible. Check difficult dates, counters, names, reductions and speaker
separability by actual listening. Retain displayed Japanese; use approved `spokenText`
expansions only for the intended pronunciation. Decode success, ASR, a voice name or a
successful generation command is not perceptual approval.

Following Irodori's listening approach, begin with the situation and required meaning,
then use vocabulary, transcript and replay for deeper understanding. Understanding every
word is not the prerequisite for succeeding at a focused communicative task. Such support
is useful study, not evidence of an untouched diagnostic first encounter.

N4 guided practice keeps policy 1: the existing normal whole replay, explicit assistance,
Good/Hard/Again rules, 24-hour exposure cooldown and shared introduction/time limits.
Do not silently harden grading or shorten cooldowns because an item is N4.

## Versioned implementation handoff

New N4 Japanese packages use `schemaVersion: 2`, `policyVersion: 1`, `jlpt: 4`.
They retain the four existing task shapes and separate task/media manifest maps.
Schema-1/policy-1 Japanese tasks and legacy English-question packages remain N5-only.
Schema 2 is a compatibility envelope, not new guided grading. Old clients must detect it
as unsupported before decoding its media; B implements matching validation and parser refresh.

B adds source-saved **N5** (default) and **N4 + N5** practice scopes. Compute allowances,
reservations and actionable due backlog source-wide, then filter level/format candidates
**before bounded fresh selection**. Filtering an already truncated queue can let hidden
items consume all visible fresh slots. Admission must revalidate the selected scope.
Home/reminders use the level scope; format filtering belongs to the browser. Explain
out-of-scope backlog that still affects the shared allowance. Never split budgets or
history; captured activities remain resumable even if a new scope hides their level.

C adds exact-level `n4-section-v1`, independently selected from the cumulative practice
scope. It captures the profile and all policy/media/source data; existing N5 profiles
and historical captures retain their behavior. The initial N4 projected form envelope is
**31-39 minutes**, including the existing preview/answer/example windows and every audio
stage occurrence. This is a reviewed project tolerance around approximately 35 minutes.
Measure shortest/longest permitted forms, not an average or a convenient seed; shared
recordings count at every playback occurrence but occupy storage only once.

Default N4 scored material must be unseen. Worked examples may recur after the unchanged
24-hour exposure cooldown, with example familiarity separately disclosed; N5's existing
example eligibility is unchanged. Thus the pool can supply two nonoverlapping scored
forms before scored exposure, not two immediately available or perpetually fresh forms.
Study/pilot exposure consumes that capacity. Familiar-scored opt-in, shortage, interruption,
nonvisual study and raw-result limitations remain explicit; there is no official scaled score.
The shared [pool checker](listening-tasks.md#static-full-pool-feasibility) now supports
`--profile n4-section-v1`. Its explicit `--unpublished-candidate` path checks complete
private media and every permitted form without creating approval or claiming scoring/
publication readiness. Normal runtime/app checks remain exact-approval gated.

## Media budgets and publication gates

B implements finite app limits of **48 MiB downloaded ZIP / 64 MiB retained** and content
publishing guards of **42 MiB compressed / 56 MiB retained / 20 MiB combined task media**.
Inflation stays at 80 MiB publishing / 100 MiB app. The
[N2 archive packaging adjustment](../README.md#app-archive-packaging) excludes contributor-only folders
and raises the publishing entry guard to 7,980; the app's 8,000-entry hard limit is unchanged.
Per-file audio/image limits, codec/path checks and hash/approval bindings are unchanged.

The last baseline public archive was 28,426,795 bytes, with 4,841,326 bytes of task media.
A preliminary 9-13 MiB new-media estimate is not measured output or spending authorization.
The upper estimate leaves about 1.89 MiB below the 42-MiB publishing guard for additional
package/document overhead. Check the complete candidate tree and exact immutable public
archive; retain headroom and stop for reviewed adjustment rather than reducing quality
or raising caps automatically.

An enlarged archive may exceed older apps' **30-MiB download cap**. Skipping schema 2 does
not make such an archive downloadable. Old clients retain their last-known-good offline
collection and report an update failure; continuing sync requires the new release APK.
Deliver the upgrade before a runtime publication exceeds that cap. A copied APK is not
an installed app. Excluding authoring documentation alone does not fund this whole pool.

Follow this sequence, which is not a learner prerequisite graph:

| Item | Deliverable |
| --- | --- |
| [A #48](https://github.com/stop-cran/learning-japanese/issues/48) | This profile, source ledger and reviewed runtime handoff |
| [B #75](https://github.com/stop-cran/kanji-cards-android/issues/75) | Package support, scopes, finite budgets and release |
| [C #76](https://github.com/stop-cran/kanji-cards-android/issues/76) | Diagnostic profile and explicit candidate-only feasibility checks |
| [D #49](https://github.com/stop-cran/learning-japanese/issues/49) | Eight scored pilots, two per family |
| [E #50](https://github.com/stop-cran/learning-japanese/issues/50) | 26 focused scored tasks plus two examples |
| [F #51](https://github.com/stop-cran/learning-japanese/issues/51) | 22 spoken-choice scored tasks plus two examples |
| [G #77](https://github.com/stop-cran/kanji-cards-android/issues/77) | Prepublication integrated/phone acceptance and actual runtime delivery |

D-F own complete per-package linguistic review, original-reviewer reconciliation, actual
full-order listener/picture acceptance and guided-native evidence. They publish reviewed
authoring/source/tooling changes and retain frozen private media candidates; they do not
need G's later checks to finish their own work, and do not push N4 runtime media early.
F's explicit candidate-feasibility report cannot grant publication/scoring readiness.

G checks the unpublished complete candidate through explicitly unscored author/test paths.
After integrated real-media/physical-phone gates pass, or a **fresh, bounded N4 owner-testing
exception is granted**, G binds runtime authorization, verifies normal import and publishes
actual runtime packages/assets/manifest. Any exception must precede the affected push.
Authoring-only pushes never count as completed runtime delivery.

Fresh bounded spending authorization is required for frozen N4 pilots, then for the
remaining pool after pilot reconciliation. Preserve per-attempt accounting and exact
media bindings; image-only revisions reuse verified unchanged audio. The N5 allocation,
owner acceptance and testing-publication exception do not apply to N4. Missing approval
stops the dependent work without invented receipts or an assertion of completion.

### Owner-testing pilots, 2026-10-26

The owner separately authorized publishing the eight completed D pilots in the app.
The [publication ledger](listening-n4-pilots/publication.json) binds their exact runtime
packages, audio and pictures; the original private candidates remain unchanged.
Their approval notes grant ordinary app testing without claiming complete-order
listener/picture, guided-native or physical-phone acceptance.

The N4-capable release `5044d58` has been copied for installation; the previously
delivered `be7286c` predates schema-2 support. After upgrading, use **Settings > Save & sync**
and select **Listening > N4 + N5**. The scope defaults to N5 and persists per source.
This is eight scored tasks, two per family, with no N4 worked examples. Guided practice
and study are available; the full N4 diagnostic remains unavailable until its existing
pool/example/timing requirements are met. The remaining 48 scored stories and four
examples are not published or authorized for generation by this bounded trial.
