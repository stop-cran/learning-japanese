# N5 listening content

This contract implements the bounded [N5 listening pilot](https://github.com/stop-cran/kanji-cards-android/issues/50).
It is not a JLPT exam or a policy for N4-N1. Write original, natural everyday dialogues and short monologues:
greetings, simple orders, shopping, appointments, daily routines, transport and directions.
Airport topics qualify only when the actual language and task are elementary.

## Authoring

- Aim for 20-45 seconds, one situation and a clear main point. Avoid long lists of facts that mainly test working memory.
- Write exactly three independent English multiple-choice questions: one marked main point and two useful details/actions.
  Each has four distinct options, one answer, option rationales, an explanation and evidence referring to complete spoken turns.
  All answers must follow from the audio, not cultural knowledge, a revealing title/picture or another answer's feedback.
- Essential spoken vocabulary, grammar, reductions, speed, length and inference all contribute to an N5-oriented estimate.
  Written kanji lists do not determine listening difficulty. Do not silently reuse grammar-only classification.
- Keep each character's voice consistent. Use a varied set of Japanese stock voices across the collection.
  Start by auditioning approximately 10% slower speech; preserve phrasing, mora lengths and natural pauses.
- Preserve written Japanese and translation. Put approved pronunciation expansions in `spokenText`; do not rewrite the displayed
  transcript merely to persuade TTS to pronounce a date, name or counter correctly.
- Optional pictures are contextual WebP images, not answer disclosures. Do not introduce unreviewed visual evidence.
- Review the full text/question package before rendering. Listen to every final recording against all three questions before
  approving it for scoring. A successful decode, transcript comparison or representative preview is not that approval.

## Schema 1

Each `listening/<id>.json` contains:

| Field | Contract |
| --- | --- |
| `schemaVersion`, `id`, `jlpt` | `1`, a lowercase hyphenated stable ID matching the filename, and integer `5` |
| `title`, `topic`, `levelRationale` | Nonempty context title, topic description and original explanation of the N5-oriented difficulty |
| `kind` | `dialogue` (two speakers) or `monologue` (one speaker) |
| `speakers` | Unique `{id, voice, ratePercent}` records; a `ja-JP-...Neural` stock voice and integer rate from -15 to 0 |
| `turns` | Ordered unique `{id, speaker, text, translation}` records; optional `spokenText` |
| `questions` | Three `{id, mainPoint, prompt, options, answer, evidence, explanation}` records |
| `options` | Four unique `{id, label, rationale}` records; `answer` identifies one option |
| `evidence` | Nonempty unique turn IDs supporting the answer |
| `vocabulary` | Optional `{surface, reading, gloss, word?}` tips; `word`, when present, identifies an existing word article |
| `image` | Optional `{path, sha256}` for `images/<name>.webp`, bound to the existing image manifest |
| `audio` | Optional generated recording metadata described below; absent while authoring |
| `audioReview` | Optional declared listening approval described below; absent until an actual listener approves |

IDs use ASCII lowercase letters, digits and hyphens. Keep one semantic identity across cosmetic corrections and equivalent voice
renders. Changed answer-bearing facts or tested skills require a new passage ID, not inherited mastery.

`audio` contains `path` (`audio/<id>.ogg`), raw-byte `sha256`, `contentSha256`, integer `durationMs`, and `turns` with
`{id, startMs, endMs}` for every turn in order. Timings describe the exact final file, excluding between-turn pauses.
The mono Ogg Opus export targets 32 kbps. The hard media envelope is 15-60 seconds and 512 KiB; 20-45 seconds remains the
authoring target, not permission to pad undersized scripts with silence.

`contentSha256` hashes UTF-8 canonical JSON of the complete document with only `audio` and `audioReview` removed:
recursive lexicographic object-key order, preserved array order, no optional whitespace, unescaped Unicode.
All schema numbers are integers. Thus changes to questions, pictures, pronunciation instructions or text invalidate approval.

`audioReview` contains `status: "approved"`, `audioSha256`, `contentSha256`, `reviewedOn` (ISO date) and a nonempty `note`
describing the listening coverage. This is an author's declaration, not a cryptographic or automated certification.
Both hashes must match the current bundle. Regeneration or a changed learning package needs renewed actual listening approval.
Pending content may be inspected as a draft but must never be enabled for grading.

Publish useful synthetic-audio provenance, not resource endpoints, credentials, PCM caches or private run records.
The shared `book-skills` engine owns synthesis/retry/cache behavior; this repository owns the learning package and publication.
For this pilot, the paid-tier stock-voice output rights were checked against Microsoft's
[Azure Product Terms](https://www.microsoft.com/licensing/terms/productoffering/MicrosoftAzure/MCA), under
"Foundry Tools and Content Safety" / "Text-to-Speech (TTS) Services". They permit paid-tier customers to use prebuilt neural-voice
audio, including commercially, while restricting use of service output to create, train or improve a similar or competing service.
Keep the recordings' synthetic origin disclosed; this collection is language-learning material, not voice-model training data.

## Manifest and budgets

Use optional `listening` (LF-normalized JSON hashes) and `audio` (raw-byte hashes) manifest maps, never legacy `files`.
Include both maps in `contentVersion`. Keep the app's existing 50 MiB retained, 100 MiB inflated and 30 MiB downloaded
archive limits; the pilot budget check retains headroom. Invalid audio, review bindings, paths or timing metadata are errors,
not successful fallbacks. They must not produce learner failures.

## Learning and pacing

Listen first, then show all questions. One complete replay is normal; extra replay, additional slowing or declared guessing
is assistance. Submit all answers before feedback. Give-up, a wrong main point or fewer than two correct answers is Again;
two including the main point, or all three with assistance, is Hard; all three without assistance is Good. No Easy/time grades.

Use one source-scoped passage schedule and one atomic result per attempt. Listening Again waits 24 hours; an initially successful
new passage has a one-day cap. Immediate practice does not advance SRS. Record unscored exposure separately; restarting must not
erase assistance or manufacture a first encounter. After study/discard, new scored entry waits 24 hours after that exposure.
Technical interruptions resume the same attempt. Store the actual content/rendition/option snapshot with historical responses.

The approved pilot policy uses the existing shared new-item allowance plus a listening-only cap:
full days allow at most two new passages and 300 estimated seconds; light days allow at most one and 150 seconds; rest days none.
Estimate a passage as `2 * audioDuration + 90 seconds` for questions/feedback. Charge that captured estimate once on its first
recorded review, including Again, not on playback/study or once per question. Do not introduce a passage that exceeds the remaining
time allowance. A longer passage may therefore have no new introduction on a light day.

Listening's actionable due workload uses the same estimate. Multiply its new-time allowance by
`clamp(2 - dueEstimatedSeconds / 300, 0, 1)`: full allowance up to five due minutes, declining to zero at ten.
Unavailable media and exposure cooldowns remain visibly blocked, preserve due dates, and do not count as actionable workload.
Existing modes retain their count-based estimator without listening review/due rows; listening still consumes the shared
new-item pool and shares the weekday policy. Due reviews are never subject to the new-time cap.

An open new scored listening encounter reserves one shared allowance unit, without introducing an item or creating a review.
Resume or explicitly discard it before starting another listening encounter in that source. Completing an already allowed
encounter remains valid across midnight or settings changes; its final debit uses the submission date. Discard releases the
reservation. Historical submitted responses are immutable even while subsequent unscored replay updates playback/exposure state.
