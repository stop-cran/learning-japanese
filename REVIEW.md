# Review process

How the kanji and word content is reviewed. The reviewers are Copilot custom agents stored in [.github/agents](.github/agents); the report format and evidence rules are in [.github/copilot-instructions.md](.github/copilot-instructions.md).

## Reviewers

| Agent | Looks at | Typical question |
| --- | --- | --- |
| [kanji-accuracy-reviewer](.github/agents/kanji-accuracy-reviewer.agent.md) | One batch of cards and their words | Are readings, stroke counts, radicals, word types, origins, look-alikes and examples true? |
| [kanji-comprehension-reviewer](.github/agents/kanji-comprehension-reviewer.agent.md) | One batch of cards and their words | Can an N5 learner on a phone follow it? Is jargon explained, are rare items marked, is the quiz title unambiguous? |
| [content-consistency-reviewer](.github/agents/content-consistency-reviewer.agent.md) | The whole repository | Do schema, links, titles, distractors, coverage, strokes and the manifest agree? |

Reviewers are read-only. They report; the maintainer decides what to apply.

## Running a review

1. Run `python tools/validate.py` (on Windows set `PYTHONIOENCODING=utf-8`).
2. Start one accuracy and one comprehension reviewer per batch of about 15 kanji, and one consistency reviewer for everything. Point each at its scope, for example "kanji cards for 右左高安新… plus the words whose `kanji:` contains any of them".
3. Collect findings; treat them as hypotheses and check disputed claims against a dictionary (kanjiapi.dev, Jisho/JMdict, Wiktionary, KanjiVG).
4. Apply fixes, run `validate.py`, then `python tools/build_manifest.py` and commit the manifest with the change.

For large additions, reviewers may handle several explicitly enumerated small batches within one bounded facet. Assign accuracy
and comprehension coverage to every batch, plus a whole-set consistency pass; use at least two model families for each batch.
Do not send the entire repository to every reviewer as an unspecified "check everything" task.

When comparing models, first freeze a shared sample and send the same files and rubric to each model independently. Preserve the
initial reports before sharing findings or applying fixes. Record actual model IDs and unavailable-model failures, without silently
substituting another model under the requested name. For each underlying issue, record severity, evidence, confidence, which reviewers
found it, and disposition (resolved, partial, unresolved, withdrawn, or optional). Count a unique contribution only after adjudication;
different assigned facets are a confound, not evidence that one model is better. Send changed passages and the diff back to the original
reviewers for reconciliation. The comparison describes this sample, not a general ranking of model quality.

The machine checks cover app format, not the truth of origins or naturalness of examples. Source records must identify actual dictionary
entries and preserve spelling/reading restrictions. See the [authoring checks](.github/instructions/content-structure.instructions.md#authoring-checks)
and [JLPT policy](docs/jlpt-levels.md). These additions address the observed YAML/parser gap, incomplete word metadata, and the requested
N4 cross-model review (2026-10-08); the older review records below remain historical rather than guarantees for new content.

## Conditionals article (2026-10-20)

**Snapshot:** `ab95097a6aaed3c14a5136f0254202b44c1563f7` plus the new
`articles/japanese-conditionals.md`, SHA-256
`32bf7855fb573c07885c85dcef289b6b7661a341d576f84b0154e6cf427060f3`.

**Scope:** the complete article, reviewed directly by its author, `gpt-6-astra`, before exercise authoring.
The pass checked positive/negative attachment, noun and adjective connectors, relative event time,
premise versus result framing, requests, past habits/discoveries, counterfactuals, translations and readings.
The [source record](docs/grammar-conditionals-sources.json) identifies inspected sections and the
overbroad source restrictions that were not adopted.

**Verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
**Findings:** no actionable defect established in this bounded article pass.
**Optional:** a fuller treatment of conditional set expressions and registers is separate follow-up scope.
**Limits:** direct author review, not independent multi-model review or native-speaker certification.
It does not certify exercises that had not yet been written or every interchangeable formulation.

## Initial conditionals exercises (2026-10-20)

**Snapshot:** the same `ab95097` baseline plus `grammar/conditionals-core.json`, final SHA-256
`ac280a7a8ee2fe6fcc99194874eae287b6f9dfae3dd7b2c95c9839f7235041cd`.
The article review above preceded exercise authoring. The [source record](docs/grammar-conditionals-sources.json)
also pins the before-correction exercise snapshot and the unchanged article bytes.

**Scope:** direct author review by `gpt-6-astra` of all 30 exercises and 187 lexical annotations:
completed Japanese sentences, translations, visible form restrictions, all 307 accepted renderings, wrong-option
rationales, feedback, four introduction groups and canonical vocabulary senses.
**Final verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

| Finding | Disposition |
| --- | --- |
| The two positive 場合 formation tasks omitted fitting である predicate variants | Resolved: accept and explain 雨である／必要である; make nonpast scope visible. |
| The completed museum-visit prompt used an avoidable place-for-visit ellipsis | Resolved: explicitly say 見学した and align the translation and local hint. |
| Broad function exclusions hid ありません, しましょう and せい | Resolved: give these occurrences lexical hints while retaining particle/auxiliary exclusions. |

**Coverage:** 10 named-form tasks, six prospective/completed なら premises, six state-condition polarity tasks,
and eight discoveries, counterfactuals and procedural cases. The groups have soft recommendations, not hard prerequisites.
All 30 new prompts have hash-bound vocabulary review records. Canonical links cover 148 spans and 88 word identities;
39 spans retain local-only glosses. The original four reviewed and 397 pending records are preserved.

**Integration:** content validation and vocabulary coverage checks pass; 148 grammar regression tests pass.
The real Android importer and typed-cache roundtrip ran successfully with one test executed and none skipped.
Manifest `d562b4b694e57b7c` rebuilds deterministically. All 32 prior grammar files and all 401 prior vocabulary records
match the baseline; complete-stage coverage still correctly rejects the original 397 pending prompts.

**Optional:** broader contextual contrasts and further conditional set expressions remain outside this initial set.
**Limits:** no actionable finding remains in this bounded author pass, but this is not independent review,
native-speaker certification, unrestricted five-way discrimination, every dialect/register, owner approval or measured
learning efficacy. No JLPT level is guessed. Structural validation does not replace the linguistic review.

## Independent conditionals review and reconciliation (2026-10-20)

**Snapshots:** original independent review of exercise SHA-256
`ac280a7a8ee2fe6fcc99194874eae287b6f9dfae3dd7b2c95c9839f7235041cd`;
corrected exercise SHA-256
`4fa7391a8411e07369dcc2c20d289bb4ce6bbbcb681b0671029c72bfd8180404`.
The article remains byte-identical to the snapshot above.

**Initial independent scope:** a separate fresh-context reviewer inspected the entire article, all 30 exercises,
307 accepted renderings, 70 options/rationales, 187 vocabulary spans, 252 exclusions, 88 linked word identities
and four introduction groups without reading the author's review conclusions. Its actual model ID was not exposed.
The article was **CLEAN** on all three facets. Exercises were correctness **NEEDS FIX**, scoped coverage **CLEAN**,
and comprehensibility **CLEAN**.

| Independent finding | Severity | Implemented correction |
| --- | --- | --- |
| Fitting polite conditionals were graded wrong without a plain-form restriction | Moderate | Accept appropriate polite forms and spellings; explain register in feedback. |
| Fitting 場合に variants were missing from case-pattern answers | Minor | Include 場合に／ばあいに for the applicable time, fee and membership cases. |
| Lexical 有る／無い spellings were rejected without a kana-only restriction | Minor | Accept fitting existence/possession spellings without generalizing 無 to negative auxiliaries. |

**Correction scope:** nine exercises now accept 403 total renderings, preserving all original 307. The other 21 exercises,
all question text, options, vocabulary hints/exclusions, IDs and introduction groups are unchanged. Only the nine affected
inventory context hashes and correction notes were refreshed. All 401 original exercises and coverage records are preserved.

**Reconciliation round 1:** the original synchronous reviewer could not accept follow-up messages, so a fresh independent
reviewer received the initial findings, frozen snapshots and exact diff. It inspected all 95 additions, nine revised
explanations and 19 options/rationales. 場合に and lexical spelling findings were **resolved**; the polite-form finding was
**partially resolved**, with one minor residual: `cond-positive-member` still rejected **ですと**.
No invalid addition or newly unsuitable option was established. Actual membership-rule usage at
[Nasu Harmony Hall](https://www.nasu-hh.com/tomo.html) supports the residual finding; the
[source record](docs/grammar-conditionals-sources.json) also records inspected formal-negative and narrative examples.

**Reconciliation round 2:** the same replacement reviewer verified that **ですと** is accepted at
`grammar/conditionals-core.json:2160`, with the plain/polite distinction explained at line 2126.
Only this answer/explanation and its inventory context hash/note differ from round 1. All 402 round-one answers remain
accepted, with no option collision. The polite-form finding is now **resolved**; the other two resolved dispositions
are carried forward. No defect caused by the final delta was established.

**Final corrected-scope verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
All three independent findings are **resolved**. The unchanged article's prior independent CLEAN verdicts are carried
forward on identical bytes, not freshly re-reviewed. Neither reviewer's model ID was exposed; no independent model-family
coverage is claimed.

**Integration:** 148 grammar regression tests and content/vocabulary checks pass. The corrected real Android importer
and typed-cache roundtrip ran once with no skips or failures. Manifest `68b70c7a09a97e94` rebuilds deterministically.
Coverage remains 34/431 reviewed, with exactly 397 original prompts pending.

**Optional:** none.
**Limits:** bounded reconciliation, not exhaustive alternative-answer certification or a new full audit of unchanged
exercises/canonical senses. The earlier author-review verdicts describe their identified historical snapshots.
Source evidence, initial findings, both reconciliation rounds and current hashes are in the
[source record](docs/grammar-conditionals-sources.json). No native-speaker certification is claimed.

**Owner status:** on 2026-10-20 the owner approved committing and pushing the pending changes and delivering a release APK.
This is publication approval, not a separate linguistic review or measured learning-use outcome.

## Second conditionals correction and reconciliation (2026-10-21)

**Snapshot:** `98e5decee4bffdc53674d06f861a5b3c95a42763` plus corrected second-batch grammar
SHA-256 `8366cff94044bd958b9cd44a96f96e4a89f78061c36cb0c934db9faddce1d224`
and vocabulary inventory `8cbf13323aa9ec0c81efcbdd2f59ae4f92c788e9e1d31ca614a926da19ab02e4`.
The original article and first batch are unchanged.

**Scope:** bounded read-only `conditionals-batch2-reconciliation-reviewer`, using the original F1 report,
frozen before/after snapshots and exact diff. Reuse of the original reviewer was attempted, but its synchronous
agent could not accept follow-up messages. The fresh replacement's actual model was not reliably exposed.
It inspected all 30 added complete renderings, six revised explanations and 12 displayed options/rationales,
and independently checked preservation and vocabulary context bindings. This was informed reconciliation,
not another blind initial review or full canonical-word audit.

**Verdicts for the corrected scope:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

| Finding | Disposition |
| --- | --- |
| F1, omitted negative conditional contractions | **Resolved**, high confidence: six contextual tasks now accept fitting なきゃ and directly related なけりゃ forms, including kana/copular variants, with colloquial-register feedback. Named conjugation drills are unchanged. |

The reviewer independently inspected the dictionary's ければ → けりゃ → きゃ account, Bunpro's register guidance
and the relevant underlying ば contexts. It distinguished conditional contractions from abbreviated obligation,
and found no invalid new acceptance, misleading explanation, distractor collision or consequential residual omission.
Exact current locations and source qualifications are in the
[reconciliation record](docs/grammar-conditionals-contexts-sources.json).

**Preservation and coverage:** only six answer lists/explanations changed; all 282 original renderings remain in order,
with 30 additions bringing this batch to **312** and the combined set to **715**. The other 24 exercises, all prompts,
options and vocabulary payloads are unchanged. Only six inventory context hashes/notes changed; 455 records are identical.
The scope remains **60 exercises in nine groups**, all with vocabulary support, and the family/model counts below are unchanged.
The full inventory remains **64/461 reviewed**, with the same 397 pending records.

**Integration:** 148 focused regression tests pass; content validation has zero errors. The real Android importer/cache
roundtrip executes one test with no skips, failures or errors. Manifest `7504a72cbe1b389c` reconstructs deterministically.
All 715 accepted completions were individually classified, including the contractions; the 33 preceding grammar files,
431 preceding vocabulary records and all 5,103 preceding manifest payloads are preserved.

**Limits:** unchanged-scope conclusions are carried forward from the original independent review, not freshly certified.
No native-speaker, exhaustive paraphrase, learning-efficacy or physical-phone UI claim is made. The documented coverage
gaps remain; unrelated vocabulary work is not expanded. Changes remain local and uncommitted; no publication or APK
delivery is included.

## Second conditionals independent review (2026-10-20)

**Snapshot:** the second-batch grammar SHA-256
`29b03d71c0cfa828aa8e64bbe7beffebe1d3c599a848a9e6e380527a183636c0`,
vocabulary inventory `2c056320338c7e363c2d6467591fcec6dfbfb7ac443fb1e2f9f58e5598f912af`,
and unchanged article/first batch on `98e5decee4bffdc53674d06f861a5b3c95a42763`.

**Scope:** fresh-context, read-only `conditionals-batch2-independent-reviewer`; actual model not reliably exposed.
The neutral packet withheld author verdicts and earlier findings. The review covered all 30 new exercises,
282 complete accepted renderings, 60 displayed options/rationales, 204 vocabulary spans, 290 exclusions and
88 canonical word identities, plus five groups, 11 facets and four recommendations. The article and first batch
were read for relevant context and combined coverage, not freshly certified in full.

**Verdicts at this snapshot:** correctness **NEEDS FIX**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

| Finding | Evidence and recommended correction |
| --- | --- |
| F1, minor correctness: six negative-condition tasks reject ordinary contractions despite visible plain/basic wording | Accept fitting なきゃ forms and copular variants with colloquial-register feedback, or explicitly require full endings before answering. High confidence in equivalence; medium-high confidence in the wording-scope defect. |

The [first dictionary entry for きゃ](https://kotobank.jp/word/%E3%81%8D%E3%82%84-3239243)
describes ければ through けりゃ to きゃ, including でなきゃ; its separate restrictive-particle entry is not evidence
for this construction. [Bunpro's contraction explanation](https://bunpro.jp/grammar_points/なくちゃ-なきゃ)
supports the form/register relationship but its obligation examples alone do not establish all six substitutions.
The [batch record](docs/grammar-conditionals-contexts-sources.json) pins the original occurrences and later disposition.

**Coverage:** the reviewer confirmed 60 exercises in nine groups, 685 accepted renderings at this snapshot,
the published overlapping family/model counts, and the stated remaining gaps. No invalid accepted completion,
incorrect displayed alternative, vocabulary defect or answer leakage was established.

**Limits:** not native-speaker certification, exhaustive paraphrase coverage or a full article/first-batch re-audit.
The review did not independently audit unrelated corpus-wide pending vocabulary or Android runtime behavior.
Shorter shared hypothesis instructions were optional polish, not a required correction.

## Second conditionals author review and coverage (2026-10-20)

This historical author pass applies to the original second-batch snapshot below, before independent finding F1
and the subsequently authorized corrections. Its original counts and verdicts are retained, not presented as a review
of later exercise bytes.

**Snapshot:** `98e5decee4bffdc53674d06f861a5b3c95a42763` plus the new
`grammar/conditionals-contexts.json`, SHA-256
`29b03d71c0cfa828aa8e64bbe7beffebe1d3c599a848a9e6e380527a183636c0`.
The article and first 30 exercises remain byte-identical to their previously reviewed versions.
The [source and coverage record](docs/grammar-conditionals-contexts-sources.json) pins the vocabulary inventory too.

**Scope:** direct author review by `gpt-6-astra` of all 30 new prompts, 282 accepted renderings,
60 displayed options/rationales, translations, question-side restrictions, feedback, five introduction groups,
204 lexical spans and 290 classified exclusions. All 88 canonical word identities were checked against their
metadata and relevant meaning passages; local-only glosses do not imply an existing canonical card.
The pass read the actual cited source passages and did not adopt their overbroad restrictions.

**Verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

| Finding during authoring | Disposition |
| --- | --- |
| Proposed links for ランプ, 登録 and 通常 had no canonical card | Resolved: retain occurrence-specific local glosses; no fabricated links. |
| A split 声をかけて idiom gave less useful partial hints | Resolved: annotate the meaningful phrase as a single occurrence. |
| Attendance-document and application wording could be clearer | Resolved: use 参加証明書 and consistent 申し込み wording. |

**Coverage:** five groups of six address further forms; preparation, event triggers and ongoing actions;
mechanisms, past voluntary habits and state-based requests; planned/completed procedural cases; and imagined
present identities. The combined set has **60 exercises in nine groups** and accepts 685 renderings.
たら occurs in an accepted completion of 33 exercises, ば in 27, なら in 24, と in 14 and 場合 in 20.
Those overlapping counts include supplied suffixes and are not independent discrimination or mastery measures.
The displayed model counts are respectively 12, 17, 14, 7 and 10, totaling 60.
The new batch contains six named-form tasks, six procedural-viewpoint tasks and 18 contextual polarity tasks
with shared realizations. No valid accepted alternative is displayed as a wrong option.

**Vocabulary:** all 60 conditionals prompts have reviewed support. The additional 204 spans comprise
145 linked occurrences across 88 identities and 59 local-only glosses. Overall coverage is **64/461**;
exactly the original 397 prompts remain pending and the inventory stays at `pilot`.

**Integration:** 148 focused regression tests pass; content validation reports zero errors.
The real Android importer/cache roundtrip executes one test with no skips, failures or errors.
Manifest `3facf661d15c0b5a` matches a deterministic reconstruction.
All 33 previous grammar files and all 431 prior vocabulary records are preserved against the baseline.
The complete-stage gate still rejects exactly the same 397 pending records; no new exercise is pending.

**Optional / remaining scope:** same-scenario comparison of valid alternatives, nonhypothetical 私の場合,
dedicated nominal なのなら production and explicit necessary-versus-sufficient reasoning remain gaps in this
60-exercise set. Related ないかぎり necessity tasks exist elsewhere. Complete register paradigms and the article's
excluded conditional set expressions are not claimed as covered.

**Limits:** this batch has author self-review only, not independent review or native-speaker certification.
The earlier independent verdicts apply only to the unchanged article and first batch; they are not inherited by new
exercises. No full-corpus vocabulary review, new JLPT classification, phone UI check, learning-effectiveness claim,
commit or publication is included in this task.

## Onomatopoeia second-batch images (2026-10-19)

**Snapshot and scope:** text commit `44216dc277a51b7fe8a9eb8603b8069a5eba6a63` plus
100 new scene images and their `image`/`image_scene` fields. This includes all second-batch
words, not just the 97 new files. Runtime manifest: `21e4f01fe7d16471`.
The [image record](docs/onomatopoeia-batch2-images.json) identifies every output by raw-byte
hash and records the actual generation scenes, final captions and per-picture observations.

**Advisory review:** direct `gpt-6-astra` inspection of all 100 images in five contact sheets,
with selected images enlarged to full size. The pass checked the chosen sense, visible text
or answer leakage, scene/caption agreement, anatomy and plausible competing interpretations.
All 100 final image/scene pairs are **ACCEPT** in that bounded advisory record.
This is not the independent two-model linguistic review described in the next section.

| Finding | Disposition |
| --- | --- |
| ぺちゃんこ's crushed can retained a raised round end and a strong crumpling cue | Resolved by regenerating the card's bread-under-a-box example. The final low side view shows intact bread flattened to a thin slice. The first output and its review are retained separately. |
| ぱんぱん's open bag did not match the caption's “zipped” wording | Resolved by changing the caption to “zippered,” without regenerating or altering the image. The original generation prompt remains in provenance. |

**Preservation:** the original 20 image files and pilot prompts/style are unchanged. The 100
cards retain their reviewed teaching text, identities, titles, sourced levels and quiz exclusions.
No new app field, app code, scheduling change or JLPT assignment is introduced. The collection
has 120 images; the remaining 80 first-batch words are not illustrated.

**Limits and owner status:** the previously approved pilot is separate from this new batch.
On 2026-10-19 the owner **accepted the new batch for learning use** and authorized publication:
“Ok, so far looks good. I'll see how it goes during learning.” This is batch-level acceptance,
not a claim of a separate per-image review or completed study-use evaluation.
A scene illustrates one use, not all senses.
Sounds, repeated movement, tastes, feelings and preceding events are not fully demonstrable
in a still image. Existing pairwise exclusions remain in force; this pass is not exhaustive
proof of visually unique quiz choices. This image review does not certify physical-phone
rendering or learning outcomes.

## Onomatopoeia second 100 (2026-10-18)

**Snapshot:** content baseline `2ca54ae0580d7b99fa3bf48dc37fe13ad1adc5cc` plus the second
100-word working-tree addition: 97 new cards, three enriched existing cards, three new guides,
the expanded overview, and accompanying provenance/navigation documentation.
The [second-batch index](articles/japanese-onomatopoeia.md#second-100-word-cards) and
[source record](docs/onomatopoeia-batch2-sources.json) enumerate the exact scope.
Final reviewed runtime manifest: `1ef73b9a7176207a`.

**Scope and reviews:** independent `gpt-6-astra` and `claude-opus-5.5` reviews of the same frozen
100 cards, three guides, overview and scoped documentation. Each review covers correctness,
scoped coverage and comprehensibility in ten enumerated ten-word packets, with whole-set consistency.
Both verified the 111-file initial snapshot (`42bed4cd756115f5`); their blind reports and before-images
were preserved before fixes. The maintainer adjudicated against actual dictionary entries, restrictions
and displayed labels, then returned the real before/after diffs to the same reviewers.
Reconciliation verified the revised files while inheriting unchanged content's earlier assessments;
it was not a claim to reread the entire corpus at each step.

**Verdicts:** both reviewers conclude **CLEAN** for correctness, scoped coverage and comprehensibility
of all 100 selected cards and all four scoped learner guides (the three new guides plus the overview).
All actionable findings and the final residual pair are resolved; no consequential unresolved claim
was established within this scope.

| Finding | Disposition |
| --- | --- |
| Missing ordinary-word, older secondary-sense and within-batch quiz protections | Resolved: 105 further direct pairs beyond the authored draft, bringing this batch to 317 new pairs relative to the baseline. These include 75 distinct numbered-review pairs, 29 accepted optional candidates, and the final ちょこちょこ/たま guard. The source record enumerates every pair; no transitive or family-clique expansion is implied. |
| Selective reading gaps | Resolved in eight cards and one guide, including ambiguous 生（なま）, 跳（と）んだ and 上（のぼ）り. Existing example meanings are preserved. |
| Dictionary spelling status and figurative-source coverage | Resolved: explain the pinned JMdict search-only status of かちかち and ぶうぶう without renaming IDs or inferring frequency. Cite the inspected Digital Daijisen sense for ちくちく's figurative needling remarks, and that dictionary's child-directed pig sense of ぶうぶう. Raw dictionary flags were already preserved in the source record. |
| Scene-based frequency title | Resolved: ちょこちょこ now says “small quick steps; every so often,” with the contextual frequency range still explained. Opus caught the remaining たま endpoint during reconciliation; both reviewers confirmed its final direct guard. |
| Collection counts and navigation description | Resolved: 271 unlevelled articles, 3,209 word articles overall, 200 tagged onomatopoeia cards, and seven guides. |
| Optional wording and broader collision hypotheses | Two clarity edits applied; the remaining stylistic suggestions and unestablished scene/manner equivalences remain optional. Both reviewers accepted these dispositions. Existing baseline-only ambiguity such as びっくり/意外 is not claimed fixed. |

Both models found quiz-label omissions. Astra supplied additional secondary-sense guards, selective
readings and the stale unlevelled count; Opus supplied spelling/source explanations, the frequency-title
refinement, guide-list correction and the final residual guard. Some observations also appeared in
the other report's optional hypotheses, so they are not all unique contributions. This describes the
matched sample, not a general model ranking.

**Preservation:** the three reused cards retain their identities, titles and sourced N3/N3/N4 levels.
The first 100 word files, existing images, grammar, kanji, app code and scheduling remain unchanged.
No new JLPT labels were inferred. Structural validation, all 4,523 manifest payload hashes, package
budgets and the Android real-repository parser check passed for the final runtime snapshot.
The later closure update to this review record does not change imported content or its manifest.

**Limits:** new examples are original, not corpus quotations or native-speaker certification.
Dictionary recognition is not a frequency rank, a level source, or a guarantee that every possible
randomized quiz choice is unambiguous. The archive measurement is a local projection, not a downloaded
GitHub release. No physical-phone rendering, image-quality review or APK delivery belongs to this
text-only batch; the existing image pilot's owner review remains separate.

## Onomatopoeia starter collection (2026-10-15)

**Snapshot:** `7e2b498` plus the phase-1 working-tree addition: 90 new word cards, 10 enriched
existing cards, four learner guides, and the accompanying source and navigation documentation.
The [overview](articles/japanese-onomatopoeia.md#first-100-word-cards) enumerates all 100 selected IDs.

**Scope:** One independent reviewer checked correctness of every card in ten ten-card batches;
another checked comprehension and whole-set consistency for the same 100 plus the guides and
documentation. A separate bounded review covered the four guides. They used the repository's
accuracy, comprehension, and consistency rubrics. Runtime model identifiers were not exposed;
this is not a verified multi-model comparison or evidence of different model-family coverage.

**Verdicts and reconciliation:** No new grammatical, reading, translation, or word-type defect
was established. Review findings and maintainer dispositions:

| Finding | Disposition |
| --- | --- |
| Missing secondary-sense quiz protections | Resolved: 11 new pairwise exclusion edges cover refreshed feelings, smooth progress, chatter, chubbiness, calm manner, rapid succession, frequent changes, and idling. Existing exclusions are preserved; see the [inventory](docs/confusable-words.md#onomatopoeia-starter-comparisons). |
| Unfamiliar kanji in sensory examples without selective reading support | Resolved: 59 reading annotations across 46 example lines in 34 cards; sentences and translations are preserved. |
| Repeated nasal forms listed beneath a “Non-repeated forms” heading | Resolved: the guide now labels that mixed table “Endings and other form patterns.” |
| Peripheral senses and dictionary spelling status | Optional improvements applied: archaic labels on peripheral ふかふか/さくさく senses and a search-only qualification for うとっと. |
| Existing どんどん/急に, どんどん/急速, and そっと/静か quiz ambiguity | Deferred as baseline-only: unchanged meanings, titles, and candidate identities already existed before this phase. They are not claimed to have been fixed. |

Dictionary identities and selected senses were independently compared to the actual hash-pinned
local JMdict snapshot, including original XML checks. The two source records are linked from
[the collection notes](docs/onomatopoeia.md); their upstream release date is not inferred.
All ten retained JLPT declarations were checked against the existing pinned vocabulary-source indexes.
No new JLPT labels were invented. The set is a practical starter selection, not a measured frequency list.

**Limits:** Editorial review is not native-speaker certification or corpus attestation of every
original sentence. No Android runtime or end-to-end randomized quiz was exercised. The checks establish
the documented exclusion edges, not exhaustive semantic uniqueness for every possible existing word.
No images, image review, app filter, or scheduling changes belong to this phase.

## N3 vocabulary expansion (2026-10-09; review in progress)

The draft adds 1,490 word articles and reuses 208, covering all 1,730 rows in the pinned N3 community vocabulary source.
Those rows map to 1,698 articles; the full collection at the pre-merge checkpoint had 3,006 words. Explicit article-level labels were 672 N5, 636 N4
and 1,624 N3, with 74 legacy articles still unlabelled. Existing easier labels, stable metadata and quiz exclusions are preserved.
The N3 vocabulary work itself changed no kanji cards, stroke assets or long-form articles; separately integrated parallel changes are described below.
See the [source snapshot](docs/n3-vocabulary-snapshot.json) and [row index](docs/n3-vocabulary-sources.tsv).

A separate all-row source audit inspected lexical identities and spelling, reading and sense restrictions against the pinned
JMdict snapshot. Six supplied dictionary IDs were corrected, with the original fields retained. Twenty-seven historical
source-intent ambiguities remain explicitly qualified; supported teaching selections are not claims to have recovered the
source compiler's intention.

The initial complete frozen corpus is `draft-r1`, baseline `cdf871bc235bc1822c2d8940c9aa77d9e175118f` plus the draft changes,
with imported-content version `d9b86029e1f5b2b3`. All 48 initial reports are complete: both `gpt-6-astra` and
`claude-opus-5.5` reviewed each of twenty-four disjoint factual packets, covering correctness, scoped coverage and
comprehensibility for every assigned article and source row. Initial reviewers received neither author reports nor
one another's findings. The original reports remain unchanged; separate Claude batch 08 and 09 addenda address omitted
reused-card quiz analysis, and an errata supplement corrects dictionary quotations in Claude batch 19.
**All 48 `revised-r2` reconciliation reports are collected: 46 report remaining fixes and two are scoped-clean.
Parent adjudication is complete for 25 reports; 23 remain. A bounded application of the adjudicated quiz safeguards
is complete, with two citation-blocked pairs held separately. No final CLEAN verdict or model-contribution comparison is claimed.**

Reconciliation used the frozen revised cards, each reviewer's original findings and the actual changes, with separately
attributed parent evidence. Replacement agents were used when the original processes were unavailable. Report authentication
and structural checks do not themselves adjudicate linguistic claims; the original reports, receipts and snapshots remain unchanged.

Recovery checks confirmed all author reports and the exact planned file scope. One author correctly refused to replace
昇る's rising/promotion senses with 登る's climbing sense merely to satisfy a filename-based checker. The corrected check
uses the explicitly taught spelling, preserves the original report, and records the disposition separately.
The same spelling-sensitive mapping check was applied to 明ける/開ける, 二十/二十歳, 張る/貼る and 街/町.
This resolves a provenance-validation defect, not a substitute for linguistic review.

Review-driven corrections include scoped sense additions for 加わる, 馬鹿, 平ら, 平均 and 氏, alongside prose,
classification, link and attachment fixes. These changes and their evidence are recorded separately from the original
author and reviewer reports; implementation does not itself resolve a review finding.

Before the `revised-r2` reconciliation application, the draft passed format, link, selected-sense, source-coverage and manifest checks. Imported-content version
`0121c69c12312ec9` contains 4,238 files; the complete archive projection has 4,277 entries including directories and
8,765,568 uncompressed bytes, within the existing importer budgets. These are historical package metrics, not the current
manifest version. Such checks do not establish naturalness or semantic uniqueness of quiz options.

Before that reconciliation, quiz adjudication added 1,027 direct excluded pairs, recorded in 984 approval records, while preserving baseline exclusions.
The residual application changed 80 word headers; all 3,006 word files were checked to confirm that their bodies and other
metadata were unchanged by that application. Repeat application changed no files. Exact-title duplicates are handled separately by the app. Exclusions are symmetric
direct pairs, not automatic cliques or transitive closure. Of two focused early-batch follow-ups, the batch 07–12 residual
review is complete: 100 comparisons yielded 48 additional parent-selected safeguards, 41 already-protected pairs,
three exact-title duplicates, six rejected proposals and two retained optional deferrals. All 48 selections are applied:
14 have genuine initial citations and 34 have separately registered supplemental evidence.

The batch 01–06 follow-up is also complete. Its 148 comparisons received 46 parent selections, 63 already-protected
dispositions, 18 exact-title dispositions, eight rejections, two retained optional deferrals and 11 nonexplicit group-comparison
dispositions that authorize no new pair. Five selections use genuine initial observations; 41 use separately registered
supplemental evidence, including five whose proposed initial citations were unrelated or contrary to approval. The parent
explicitly resolved the earlier 期間/時期 deferral using the complete lessons and dictionary evidence; 出/元 and
がっかり/失望 remain optional deferrals rather than being silently upgraded to rejections. Across both follow-ups, 94 selected
records produced 89 additional distinct direct pairs; duplicate evidence is retained, not expanded into cliques. All selected
residual safeguards from those two earlier follow-ups are applied, with exact before-images and separate evidence, ledger and application records preserved.
These later checks are not additional blind reviews or evidence of exhaustive synonym coverage.

The first `revised-r2` application (2026-10-10) adds 385 direct pairs from 387 distinct parent selections, changing only
262 word headers. The graph at that application checkpoint had 1,426 direct excluded pairs, including the 14 baseline pairs, declared by 856
word cards. The ledger retains its earlier 984 approvals and appends 385, for 1,369 approval records. All 3,006 word bodies
and their non-exclusion metadata are unchanged by this wave; a repeat application makes no changes.

The unapplied pairs are とうとう/やっと and お酒/アルコール: their cited findings belong to other cards, so those citations
cannot authorize the proposed declaration owners. They remain held, not linguistically rejected or silently reassigned.
The application preserves exact before-images, all 22 parent-selection bindings, duplicate observations, optional-safeguard
status, weaker remedy suggestions and source limitations. It does not approve findings from the 23 reports still awaiting
adjudication, resolve the separate editorial backlog, or imply exhaustive quiz safety.

Publication also integrates 11 parallel commits through `c7cb0ac`, including article-subject cards, reciprocal links,
kanji-reading explanations and curated quiz distractors. The combined collection has 3,022 words and 620 kanji;
[README.md](README.md) gives its combined level counts. 作家 consolidates the two additions for the same lexical identity.
訳 retains both the N3 expansion's separate やく teaching and the parallel わけ grammar explanation, with their sources.
The merged graph preserves all 1,426 application-checkpoint pairs plus 57 independently published pairs, for 1,483 direct pairs.
Those 57 additional pairs are not part of the N3 parent adjudications or their approval ledger.
These parallel changes and merge resolutions are not part of the frozen `revised-r2` review; the outstanding adjudications remain open.

## N5/N4 vocabulary expansion (2026-10-09; reconciled)

The expansion adds 924 word articles and reuses 384, covering all 1,324 rows in the pinned community vocabulary source:
684 N5 rows and 640 additional N4 rows. Those rows map to 1,308 articles, including shared pages for multiple readings.
The repository now contains 1,516 words. Source-covered articles have explicit vocabulary levels: 672 N5 and 636 N4;
208 legacy articles remain without a sourced word-level label. No kanji cards, stroke assets or long-form articles were added.
See the [source snapshot](docs/n5-n4-vocabulary-snapshot.json) and [row index](docs/n5-n4-vocabulary-sources.tsv).

This is named-source coverage, not an official JLPT syllabus or a complete beginner curriculum. In particular, the selected
lists omit several basic standalone particles. Their descendants share a source lineage, so agreement between those mirrors
is not independent corroboration of level membership.

### Source identity and independent coverage

A separate all-row source audit checked lexical identity, spelling/reading restrictions and gloss qualifications against the
recorded JMdict snapshot. Nine supplied dictionary IDs were corrected without rewriting the original CSV fields. コート,
ビル and マッチ distinguish separately recorded homographs; their subsidiary senses do not acquire separate JLPT assignments.
The terse source gloss for マッチ does not settle which "match" sense was intended. Dictionary recognition does not establish
commonness, and uncertain source intent is not silently replaced by a preferred interpretation.

All 32 initial editorial reports are complete and fingerprinted. For each of sixteen disjoint batches, both families received
the same original frozen articles and factual source packet, without the other reviews or the author's review rationale.
Each article was assessed separately for correctness, scoped coverage and comprehensibility.

| Review family | Assignment | Declared coverage |
| --- | --- | --- |
| `gpt-6-astra`, as identified in the initial reports | Sixteen reviewers, one batch each | All 1,308 articles and 1,324 source rows |
| `claude-opus-5.5`, explicitly selected and recorded by the runtime | Eight reviewers, two batches each | The same 1,308 articles and 1,324 source rows |

The snapshots use baseline `fe82cb649b097a4897f8209f1336ce46199e5530` plus the authored changes. Each batch was frozen
independently; they are not represented as one simultaneously captured original checkout. Content hashes normalize CRLF to LF.
Two Claude JSON reports omit a reviewer field; their model attribution is retained separately from the explicit selection and
runtime record rather than added retroactively to the initial reports.

The corrected reconciliation input is imported-content version `e9a9b8f280e5c13c`, with frozen ZIP SHA-256
`4388108bdd26921b5975e225d84abdc9ec815e65379deec29b42a17a4d73f42e`.
There are 85 changed articles in R2 relative to the initial batches, including metadata-only changes. All original reviewers
reconciled the actual diffs and revised passages. Unchanged assessments were carried forward only after hash comparison;
declared reading extent and matching hashes are not machine proof of editorial attention.

An additional review observation prompted a bounded colour-pair check. 青/青い and 白/白い need explicit exclusions;
red, black and yellow pairs already have identical titles and are handled by exact-title deduplication. The R3 follow-up changes
only metadata on 青 and 白, not teaching prose. Both original review families accepted that delta separately, bringing the
number of distinct revised articles to 86. The final imported-content version is `919f5024dcf9724a`; its frozen review ZIP has
SHA-256 `63b562aad2e7129dbfedc384d88c80155e60a9b47d35b30bcca1e555f18220e0`.

**Result:** all 32 R2 reports and four narrow R3 reports are complete, with CLEAN verdicts within their recorded scopes.
Required findings and consequential linguistic uncertainties have explicit dispositions; optional and contextual suggestions
are not silently promoted into defects. Coverage, preserved hashes and those dispositions were checked separately from editorial
judgment. The independent code-review finding was fixed and reconciled by its original reviewer.

### Implemented corrections and calibrated judgments

- Separate character readings, written kana endings and grammatical stems: 足りる/足す, 夫婦, 話す/話 and 出来る.
  Replace the misleading vowel-length contrast for こう and the silent-pause cue before 雑誌's fricative.
- Repair sense and usage explanations: medical 診る versus 視る, the aesthetic contrast in 花より団子, both person and
  area objects of 案内, and 車's compound readings. Teach 午後 as afternoon as well as a p.m. label, and keep the
  numerical 時/時間 contrast distinct from their wider lexical uses.
- Make assigned meanings usable through translated examples and selective readings, including bare もう for an approaching
  event and a complete negative-question exchange for いいえ. Clarify clothing verbs, warm versus cooled drinks,
  phone-device versus phone-call contexts, and ordinary versus honorific or humble uses.
- Remove unsupported frequency, register and historical claims rather than asserting their opposites. Examples include
  毎月's reading-frequency comparison, the school/university cutoff, 電車's blanket commuter-service claim, and component
  origin stories. Meaning aids are labelled as such. Official spelling recommendations are not turned into universal
  ungrammaticality rules, and a contextual English article or number choice is not automatically a mistranslation.
- Preserve word identities, readings, types and tags. Two original title changes are explicitly recorded in the source snapshot:
  一杯 makes "full" co-primary with "one cupful", and 青い qualifies its conventional green uses. New `jlpt` and
  `quiz_exclusions` fields are separate, deliberate metadata additions.

The families produced overlapping and complementary observations. For example, both noticed the 夫婦 reading and the
見る/花 explanations; other useful input concerned 午後, 案内, unsupported frequency claims and spelling-versus-stem wording.
Defects, useful optional refinements and disputed recommendations remain distinct. The different reviewer group sizes and
shared source dependencies prevent interpreting raw finding totals as a general model ranking.

### App integration and limits

The accompanying app change gives explicit word levels precedence over kanji-based inference, while retaining the legacy
fallback only for omitted levels. Native SQLite migration/reopen checks cover preservation of word identities and review history;
they are not an Android-device study session.

The final app run passed 55 tests and a debug build against the immutable R3 directory and ZIP, importing all 1,516 words with
zero problems. It checked 12,928 full-pool selections, 560 among-option cases and 40 triangle cases, plus 2,000 selections after
native database reopen/reimport. All full-pool cases retained four choices without the declared conflicting pairs. The later app
schema-document clarification did not change runtime or test source.

The independent code review found a real format-enforcement gap: escaped or explicitly tagged YAML keys could hide duplicate
declarations and silently remove an exclusion. The paired fix validates raw word keys before map collapse, also protecting `jlpt`;
it rejects delimiter prefixes that could conceal later keys. The original reviewer reran the failing cases, checked 121 paired
key/delimiter cases across Python and Kotlin, and accepted the fix. The content validator's 70 regression tests and full-corpus
check pass. These code changes did not alter the reviewed word articles; validation-tool and documentation changes after the
frozen corpus are recorded separately.

The initial reviews also exposed a cross-word quiz issue. 気 and 気分 have valid, overlapping English glosses, and the
inspected old selection rule ranked them as each other's strongest distractor across the full 1,516-word pool. Changing
accurate meanings to make answer strings different would not solve that problem. The user authorized explicit pair exclusions,
now documented in the [word format](docs/content-format.md#word-article): fourteen pairs, declared on thirteen articles and involving
25 words. The 固い/堅い/硬い triangle has three independently supported edges, not inferred transitive closure.

These constraints do not discover every synonym or guarantee semantic uniqueness for uncurated pairs. Older apps ignore them.
Context-dependent secondary overlaps, including 緑 versus the conventional green uses of 青/青い, remain nonblocking follow-up
notes rather than a claim that the curated set is exhaustive.
The existing small-pool behavior is retained: if every distractor is excluded, only the target can remain; the current collection
has many alternatives, but arbitrary forks or reduced pools need separate consideration.

The editorial reviews are not exhaustive native-speaker, corpus-frequency, pitch-accent or historical-etymology audits.
The 208 unsourced legacy words did not receive a new full linguistic review. An alternative mirror's 叱る versus the pinned
然る item remains an upstream-source uncertainty, not authorization to rewrite the selected row or claim official membership.
Optional sense expansion, additional examples and uniform citation styling are not represented as completed repairs.

## N3 kanji expansion (2026-10-09; reconciled)

The addition contains 362 kanji cards, 313 word articles and 362 generated stroke files, reaching 614 kanji and 592 words.
It covers all 367 characters in the named community N3 set, including five existing cards; this is not an official JLPT syllabus. The
[N3 source snapshot](docs/n3-source-snapshot.json) and [primary-word index](docs/n3-word-sources.tsv) record the exact set,
dictionary versions, selected word senses and transformations. The two reused word articles, 場所 and 部屋, now link their
newly available components.

All new kanji metadata was compared with the pinned KANJIDIC2 records, and all new word spelling/reading pairs were checked
against restriction-aware JMdict records. The 315 primary pairs include the two reused words. Their indexed senses are
non-exhaustive teaching anchors, not an inventory of every sense explained on a page. Modern-shape mnemonics are distinguished
from historical etymology. Dictionary inclusion alone does not establish frequency or the naturalness of an invented example.

### Independent coverage

All sixteen initial reviews used the same immutable snapshot, based on `0fb9bf27b6686443457b8439364298c89e286722`
plus the uncommitted expansion: app content version `e12b36c6323c28a1`, snapshot SHA-256
`c025cc01c0ac7f40bbf0f1dbf6b5bd67b6d535b53d82e9b50da749ea42412a06`.
Initial reports were preserved and fingerprinted before reconciliation, not overwritten with the revised verdicts.

| Scope | Accuracy | Comprehension and scoped coverage |
| --- | --- | --- |
| Shared: 24 kanji + 24 words | Each of `claude-opus-5.5`, `gpt-6-astra`, `grok-4.7` checked all facets independently | Same three reviewers and rubric |
| A: 55 kanji + 52 words | `claude-opus-5.5` | `gpt-6-astra` |
| B: 56 kanji + 47 words | `gpt-6-astra` | `grok-4.7` |
| C: 55 kanji + 49 words | `grok-4.7` | `claude-opus-5.5` |
| D: 58 kanji + 48 words | `claude-opus-5.5` | `gpt-6-astra` |
| E: 57 kanji + 48 words | `gpt-6-astra` | `grok-4.7` |
| F: 57 kanji + 47 words | `grok-4.7` | `claude-opus-5.5` |

The shared words include the two reused articles. These disjoint scopes cover all 677 relevant pages, with at least two model
families per page. A separate `gpt-6-astra` reviewer checked whole-set consistency. The table records actual models used;
no unavailable model was silently replaced.

All sixteen original reviewers then reconciled a separate immutable corrected snapshot: app content version `1e2d7dc8d50fc546`,
snapshot SHA-256 `8a425feb3ad48925eada24447934434b437e93c6160ba847fe2872b8f878f773`.
The shared/A/B/C/D/E/F patches contain 16/15/13/32/12/13/31 changed pages respectively, totaling 132; two provenance files
also changed. Reviewers read the actual diffs and revised changed passages, including changed front matter on tag-only pages.
Unchanged prose was not generally reread. Reported file coverage was checked against the exact assignments; it remains a
declared reading extent, not machine proof of editorial attention.

All original findings have a resolved, withdrawn or optional disposition, with no consequential in-scope issue left open.
Separate scope-label corrigenda preserve two accuracy reviewers' original reports while clarifying that reading every assigned
file is not a curricular-coverage verdict. The final review-record update is outside the app manifest; imported content remains
identical after the documented line-ending normalization to the reconciled snapshot.

### Adjudicated changes

- Correct the interpretation of secondary KANJIDIC2 stroke counts in 込 and 収: they are common miscounts, not equally accepted
  alternatives. Primary metadata counts and stroke assets were already correct and remain unchanged.
- Separate spelling boundaries from the learner's conjugation stem, especially 流れる: the ます-stem is 流れ, not なが.
  Clarify that omitting an understood object does not make 洗う intransitive. Explain 怒る's おこる/いかる readings without
  calling them different written forms, and distinguish 降る/降りる as different words rather than polite/casual readings.
- Add missing kana and explanatory links between meanings: 生命/せいめい, 公苑/こうえん, 制度's 度 contribution,
  等/など and 際's occasion use. Teach 息をする positively, and explain 生徒/学生/児童 as qualified institutional tendencies,
  not absolute age rules. Fix the overbroad 更 nighttime-reading statement and improve the polite listener-family example.
- Replace quiz-author instructions in 34 new kanji pages with learner-facing comparisons. Refine five titles (昨, 晩, 突, 等, 経)
  without claiming their original narrower source-backed glosses were false. All ten affected complete default quiz sets were
  semantically reassessed; no distractor arrays changed.
- Preserve the practical 初めて/始める distinction while acknowledging 始めて as another spelling of the adverb.
  Make the 昔 sense boundary and contextual English translations explicit. The 昨日 translation is more literal; 残念 retains
  "with you" and explains the assumed scene. Contextual English is not inherently an incorrect translation.
- Normalize three plural POS-tag aliases on exactly 59 new word pages, preserving all other tags and baseline metadata.
  Clarify the primary-sense index in both public provenance locations. This does not imply that the earlier tags violated the
  schema or caused a demonstrated app-filter failure.

Adopted polish remains distinct from verified defects. Katakana retention in pronunciation aids is a consistency convention:
the former hiragana transcriptions did not misspell the original Japanese sentences or change their pronunciation.
The D-accuracy reviewer withdrew its contrary defect claim and its mistaken claim that 留学 was the only such conversion.
The F-comprehension reviewer likewise reclassified its reading-aid concern as optional.

### Model contributions in this sample

Only the identical shared sample supports the comparison below. Observations were deduplicated across entire initial reports,
including optional suggestions, source checks and per-page notes, not just their findings lists.

| Model | Useful contribution in the shared sample |
| --- | --- |
| `claude-opus-5.5` | Additional minor findings on the listener's-family example, the broad 更 rule and 降's politeness implication; also the adopted optional 歳/年 clarification. |
| `gpt-6-astra` | Independently identified the 込 common-miscount issue; additionally suggested 程 "refers to a level", adopted as local polish. Its extra age-counter pronunciation list remains optional and deferred. |
| `grok-4.7` | Additional 日程 duration and 性格 component-wording suggestions, both adopted as localized polish. Its 初めて spelling observation overlaps Claude's optional note and is not a unique discovery. |

Claude and Astra independently caught the same 込 source-interpretation issue. Claude and Grok differed on whether the original
初めて spelling wording was a defect or optional qualification; both accept the revised version. Source inspection without a
reported objection is not discovery credit. The broader review also retained a severity disagreement about the original 昔
generalization while agreeing that the added sense qualifier closes the concern.

Useful findings outside the matched sample included Astra's 流れる/洗う explanations, Claude's 息をする and school-term
coverage, and Grok's missing pronunciation aids for 生命 and 公苑. Different files and facets offer different opportunities;
neither these results nor raw finding counts support a numerical ranking. This is one small, task-specific comparison.

### Limits and deferred observations

Whole-set checks cover source membership, metadata, required links, structural stroke data and the deterministic manifest.
All 362 new cards have three curated choices. For the 25 baseline cards needing one default fallback choice, the highest eligible
candidate bands are unchanged: no new N3 card can displace them under the inspected full-pool, four-choice algorithm.
This does not establish safety for arbitrary filtered pools or larger quizzes. For example, 晩's legitimate "evening; night"
title overlaps 夕 and 夜, although they are not paired in the affected authored default sets.

The reviews are not exhaustive native-speaker/corpus validation, pitch-accent or historical-origin audits, visual verification
of every stroke trajectory, or Android device testing. Existing articles outside the declared scopes did not receive a fresh
linguistic audit. Optional examples, mnemonic preferences and exhaustive sense expansion remain deferred.

Word tags remain freeform rather than a complete POS ontology. The additional observation that 備える, 割る, 殺す, 求める and
決める have subtype tags without a generic `verb` tag was checked separately: all five are new N3 pages, but their metadata
did not change during reconciliation, and no documented parent-tag requirement or current app-filter defect was established.
Broader POS-tag coverage is optional future taxonomy work, not an unresolved instance of the corrected plural aliases.

## Review of the first starter set (106 kanji, 159 words)

Done once after the content was drafted: 6 accuracy, 3 comprehension and 1 consistency review.

What it found and what was fixed:

- Wrong or misleading facts: 年上 used for "elderly", 校正 read きょうせい, 話 analysed as containing 舌, 店's phonetic 占 given a テン reading, 銀行 explained with 商行為, 北海道 called "one of the few" 道 prefectures, 九 vs 力 stroke counts, 駅 called a bound noun.
- Reading-table errors: words in the wrong on/kun row, special readings listed as ordinary on readings (今年, 人間, 千葉).
- Comprehension: unexplained jargon (jukujikun, ateji, okurigana, "KANJIDIC"), unmarked rare readings, vague or untrue look-alike notes, duplicate prose.
- Consistency: stale manifest; `distractors` missing on one card.

Status and gaps recorded after that review (historical; see the N4 update below):

- The twelve kanji that words needed (側 海 達 供 旅 京 自 動 物 銀 短 事) now have cards; 118 kanji in total.
- Some word `kanji:` lists omit characters without cards (地, 曜, 心).
- Many words link to a kanji card that does not list the word under Common words (backlinks are not required for every prose link).
- Words that mix on and kun readings (半年, 駅前, 毎月) are typed `kango`; the schema has no on+kun type.
- Radicals were checked against the Kangxi table, not fetched per kanji from KANJIDIC2/Unihan. Word readings were checked from memory and spot lookups, not every entry in JMdict.
- Resolved afterwards: `jlpt` now follows the community lists mirrored by kanjiapi.dev, so cards for kanji such as 安, 新, 古, 多 and 会 are N4 (and 短 N2); all 118 cards in that original cohort carry the `starter` tag.

## Cross-model review (12 new cards plus 12 older ones)

The same accuracy and comprehension prompts were run on gpt-6.1-sol and grok-4.7, in three chunks of 8 cards plus their words, after the earlier Claude-based review and fixes. All three families found real errors the previous round had missed, including in already-reviewed articles (the 東京/京都 "same kanji reversed" claim, the 北 compass-order rule, 下さい filed under くだ.る, 来てください listed as an imperative, 九人 explained via 苦, 三和土 as an example of ゾウ).

- Both models found: 東京/京都, the 北 ordering rule, 犬 listing 犯 as an animal kanji, 食事 "ジ in compounds", the 中 うち example, 円高 reading and type, 銀行 "only" claims, the stale 長短 note.
- Only gpt-6.1-sol found: the 来る request row, 子供/幼児 wording, 水中 contrast, 高 description.
- Only grok-4.7 found: 下 ください, 発達, 九/苦, 三和土, 未/末, 北海道 etymology, 円 shape, 自 kun reading.

Conclusion: no single model is a reliable sole reviewer; each caught roughly half. Run at least two model families per batch and treat findings as hypotheses. Fixes were applied by file group and are not independently re-reviewed.

## N4 expansion (2026-10-08; reconciled)

The addition contains 134 kanji cards, 120 word articles and 134 generated stroke files. Together with the existing cards, this gives
252 kanji and 279 words, including all 166 characters in the named community N4 set. The [source snapshot](docs/n4-source-snapshot.json)
records dictionary versions, hashes, the exact target set and transformations; this is not an official JLPT syllabus.

All 134 new cards' readings, primary stroke counts, classical radical numbers and canonical radical glyphs were compared with the
inspected KANJIDIC2 records. All 120 new word articles' spelling/reading pairs were checked against restriction-aware JMdict lookups.
The new explanations use explicitly labelled modern-shape mnemonics rather than asserting unverified historical origins or phonetic roles.
Dictionary inclusion alone does not establish example naturalness. The independent linguistic reviews covered all new articles;
the original reviewers subsequently reconciled the corrected passages and quiz sets against the actual diffs.

The four incomplete word-kanji arrays for 土地, 安心, 土曜日 and 金曜日 are repaired, with links to their newly added cards.
分 is N5 under the documented source exception. App-format checks now distinguish restricted front matter from full YAML, enforce
complete written-kanji metadata and valid imported-page links, and cover distractors, headings and basic metadata consistency.
These structural checks are not a linguistic-correctness verdict.

### Independent coverage

All eleven initial reports are complete. The reviewers used the same immutable snapshot, based on `8279eaa` plus the uncommitted
expansion: app content version `8e028ca1b338df0b`, snapshot SHA-256
`a3e8eab2d3aa40042e62bcb51a27a338bfca89cda3be2e13f7ab84834b694134`.
Initial reports remain separate, fingerprinted artifacts rather than being overwritten during reconciliation.
Reported file lists match the assigned linguistic scopes.

| Scope | Accuracy | Comprehension and scoped coverage |
| --- | --- | --- |
| Shared: 18 kanji + 18 words | Each of `claude-opus-5.5`, `gpt-6-astra`, `grok-4.7` checked all facets independently | Same three reviewers and rubric |
| A: 39 kanji + 37 words | `claude-opus-5.5` | `gpt-6-astra` |
| B: 39 kanji + 34 words | `gpt-6-astra` | `grok-4.7` |
| C: 38 kanji + 32 words | `grok-4.7` | `claude-opus-5.5` |

The shared words include 17 new articles and the existing 土地 article. Every one of the 134 new kanji and 120 new word articles
therefore received coverage from at least two model families. A separate `gpt-6-astra` pass checked whole-set consistency;
`claude-opus-5.5` reviewed the validator, tests, CI and importer assumptions. These are the actual models used, not substituted aliases.

Reconciliation used a separate immutable snapshot: app content version `7327a218a0a9c842`, snapshot SHA-256
`e0fec24bf7e5b1604dc2cb96c1acdd6f851683a64676809cd8987590848fe19a`. The shared/A/B/C diffs contain 22/41/39/40 changed
files respectively: all 134 new kanji and eight word passages, including existing 土地. Each original linguistic reviewer checked
their assigned changes; reported changed-file lists match the exact diffs. The consistency reviewer confirmed implementation and
coverage, and the tooling reviewer closed the validator changes separately. No actionable in-scope defect remains open.
The final review-record update is outside the app manifest; imported content remains byte-identical to the reconciled snapshot.

### Adjudicated changes

- Correct the default nearby-shop construction to 近くの店, while preserving qualified direct modification such as 駅に近い店.
  Clarify the usual local-government 公立 versus national 国立 distinction.
- Remove misleading "godan despite ending in る" wording from 止まる and the parallel 作る passage. Distinguish the i-sound in
  知る from literally writing いる. Add useful standalone ほう comparison/advice coverage and the polite ご主人 contrast.
- Supply missing kana, explain visible radical forms without changing canonical metadata, clarify modern component comparisons,
  and remove unsupported frequency/register qualifications in 土地. Removing an unverified qualification is not proof that its
  opposite is true.
- Repair ambiguous quiz choices, including 地/土, 屋/店, 問/聞, 題/問 and 言/語. The actual app shows a kanji and offers English
  titles as answers. Its default four-choice quiz fills missing distractors automatically, so merely replacing one synonym while
  retaining two curated choices does not guarantee a safe complete question. Three explicit choices are now present on every
  new card, with every revised set reconciled by the assigned reviewers. The class-level pass also removed ambiguous 研/究 and 洋/海 choices and excluded
  試/験 and 館/堂 as mutual choices; related meanings remain available for comparison in the prose.
  The 25 older two-distractor cards were checked separately: their highest eligible shared-tag band contains only original cards,
  so no new card can win the remaining slot under the inspected inputs. Their lists are left unchanged; optional stabilization
  would not fix a demonstrated expansion regression.
- Repair validator/importer disagreement around Unicode whitespace, header boundaries and free-form articles; strengthen stroke
  identity/geometry checks and their fixtures, and report malformed input explicitly. No current source card was shown to trigger
  the Unicode mismatch; it was reproduced with targeted malformed headers.

These fixes were reconciled against the actual changes, not closed by accepting a majority vote. Adopted optional improvements
remain distinct from corrected defects; other nonblocking suggestions are not presented as completed work.

The tooling reconciliation is complete: the original reviewer confirmed the parser, stroke and error-reporting fixes. That pass
also caught a new platform-dependent test assumption: a 3,000-deep JSON array raised a recursion error on Windows but parsed on Linux,
so the test would fail in CI. The test now injects `RecursionError` deterministically while retaining real deep-YAML inputs.
All 46 tests pass on Windows Python 3.13.14/PyYAML 6.0.2 and Ubuntu Python 3.12.3/PyYAML 6.0.1; the original reviewer independently
confirmed the repair and that removing the error handler still fails the test. Optional dependency pinning remains deferred.

### Model contributions in this sample

The matched sample, rather than the disjoint A/B/C assignments, supports the comparison.

| Model | Additional useful observations in the shared sample |
| --- | --- |
| `claude-opus-5.5` | Standalone ほう coverage and the misleading 止まる verb-ending explanation were not raised by the other shared reviewers. |
| `gpt-6-astra` | Missing ひろい in 広い土地; also explicitly left the "ト occurs in few words" frequency qualification unverified rather than treating it as established. |
| `grok-4.7` | Actionable quiz concerns corroborated concerns raised elsewhere; its two other shared-sample findings were withdrawn as defects after evidence-based discussion. They remain optional presentation suggestions, not unique verified errors. |

Overlap was counted across all report sections. All three noticed 地/土, although Claude initially treated it as a hypothesis.
Claude and Grok raised 屋/店 as an actionable ambiguity; Astra noticed but dismissed it using a full-meaning-prompt interpretation.
Inspection of the actual kanji-to-English UI settled that disagreement. The ご主人 suggestion was shared by Claude and Grok;
the unsupported 地所 register qualification was raised by Claude and separately recorded as unverified by Astra.

Grok's 同じ finding cited the wrong JMdict entry: it supplied the entry for 雷雨. The reviewer corrected the reference to entry
1451750 and withdrew the grammatical-error claim; the original wording already allowed, rather than universally required, な
before の. Its demand for full-sentence 土地 examples was also withdrawn: the authoring rule requires translations, not only complete
sentences. The narrower explanatory-の wording and clearer example layout were adopted as optional improvements.

Outside the matched sample, useful findings included Claude's 近い usage correction, Astra's 問/聞 quiz concern, the 公立 distinction
raised independently by Claude and Astra, and Grok's 知る spelling-versus-sound clarification. Different facets and files prevent
turning those results into a fair numerical ranking. This is a small, task-specific comparison, not a general model benchmark.

### Limits and legacy observations

The reviews are not an exhaustive native-speaker/corpus study, historical reconstruction, pitch-accent audit or Android device test.
Structural checks covered the full 252-kanji/279-word corpus; that does not constitute a fresh linguistic audit of every older article.
The larger-quiz and future-app fallback limits are documented in the [quiz-authoring rule](docs/content-format.md#quiz-authoring).
Quiz judgments concern ordinary learner-facing meanings, not every rare or historical sense. For example, the accuracy-B reviewer
left 曜/明's wider "shine" association as an optional improvement rather than an ordinary-sense defect. Visual resemblance is
editorial judgment, not measured learner-confusion data; several third choices are moderate component/layout contrasts.

The consistency reviewer also reported two pre-existing issues outside this expansion's changes: 六 uses the Nelson indexing radical
亠/8 rather than the selected classical 八/12, and 16 older word articles omit useful component links. All 15 distinct missing-link
targets already existed at `8279eaa`; none became available through the 134-card addition. Those legacy items are left unchanged
rather than silently broadening the N4 task. The alternate radical is not claimed to be invalid in every indexing scheme.
The missing-link articles are 先生, 内側, 出入口, 北海道, 友達, 名前, 国内, 外国, 子供, 旅行, 来年, 自動車, 見物, 買い物, 銀行 and 飲み物.