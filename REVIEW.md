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

## Actions, events and results: independent review and reconciliation (2026-10-23 UTC)

**Snapshot and scope:** `a45b9ccd5c996147179cbc977556591e8b69921c` plus
[issue #19](https://github.com/stop-cran/learning-japanese/issues/19). One fresh independent reviewer
inspected the whole new article, 28 exercises, all answers/options, 34 lexical spans, 84 exclusions,
source mappings, exact reuse and three reciprocal-link changes. The actual runtime model was unavailable.
The [ledger](docs/grammar-transitivity-results-sources.json) preserves both snapshots and original findings.

**Findings and reconciliation:** TR-01 (moderate) omitted fitting topical は answers; TR-02/03 (minor)
omitted polite contractions and noun-result となりました alternatives. TR-04 (minor) copied not-yet
feedback into already-done or cause-unknown scenes; TR-05 (minor) omitted a heading number in a fragment.
All were confirmed and repaired without narrowing contextual questions. The same reviewer independently
checked all 44 added realizations, ten changed contexts and the article/link repairs: all five **resolved**,
original severities retained, no introduced defect established. Final correctness, scoped coverage and
comprehensibility are **CLEAN** within the combined original/reconciliation scope.

**Coverage and reflection:** four groups, nine facets, six soft recommendations and no prerequisites;
18 formation and ten contextual-selection tasks share ten context-key strings. All 1202 prior exercise
objects and lexical records are preserved; lexical coverage is 921/1230, with 309 pending. Regroup the
observed contraction/register and stage-feedback examples under existing checks, rather than adding a new
review layer. Add useful source navigation and the demonstrated PDF-rendering retrieval lesson.
The final 110 accepted strings, unchanged 62 base/two additional options, focused regressions and fresh
Android importer pass. These are not physical-device or unrestricted-conversation certifications.

## Ability and perception: independent content review (2026-10-23 UTC)

**Snapshot and scope:** `3ebaf6d580a1930edeca46d5f0ad3b6d9bc727d6` plus the installment for
[issue #18](https://github.com/stop-cran/learning-japanese/issues/18). One fresh independent reviewer
inspected the whole 170-line article, all 34 new exercises, 71 accepted renderings, 68 base options,
79 lexical spans, 164 exclusions, source/coverage mappings and the three reciprocal-link changes.
Its actual runtime model identity was unavailable, recorded as `null` rather than inferred.
The [ledger](docs/grammar-ability-perception-sources.json) preserves the initial snapshot and report hash.

**Verdicts:** correctness, scoped coverage and comprehensibility **CLEAN**. No actionable findings or
consequential unresolved claims were established; no reconciliation or manufactured finding was needed.
The review inspected actual primary lessons, supplementary passages and exact dictionary senses.
It checked standard potential formation and polarity, reverse conversions, skill/access interpretation,
perception/access overlap, sensory frames and non-agent noun roles rather than relying on planning approval.

**Coverage and preservation:** five groups, 11 facets and seven soft recommendations, with no prerequisites.
The 22 formation and 12 interpretation tasks share 24 context-key strings; paired scenes are not counted as
independent conversations. All 1168 preceding exercise objects and vocabulary records are preserved.
Exact reuse identifies three ability tasks plus two experience controls, three ability changes plus three
habit controls, and six potential-goal tasks, each in its original owning group. Corpus coverage reaches
1202 exercises in 55 sets, including 274 N4; lexical coverage is 893/1202 with 309 still pending.

**Reflection (navigation add, existing rules retained):** the existing complete-task, sense-specific source,
bounded-operation and nonleaking-hint rules handled this installment without a demonstrated new process gap.
The source guide adds the inspected potential/perception starting points and their concrete qualifications.
In particular, a source's introductory shortcut must not override its own accomplished-event or particle
examples. No extra mandatory review rule is invented from a clean result.
The content/vocabulary checks, 151 focused regressions and fresh non-skipped Android importer pass.
Unchanged article sections, physical-device UI and unrestricted conversational mastery are not certified.

## N4 consolidation: independent review and reconciliation (2026-10-23 UTC)

**Snapshot and scope:** `d6b0b69809eed30898c46ff59bfefcb6331c86f8` plus the additions for
[issue #17](https://github.com/stop-cran/learning-japanese/issues/17). One fresh independent reviewer
inspected all 88 prompt annotations, initially 969 lexical spans and 1434 exclusions, plus all 13 new
groups, 27 facets, 73 memberships and eight soft recommendations. Its actual model ID was unavailable.
The [ledger](docs/grammar-n4-consolidation-sources.json) preserves separate initial and revised snapshots,
original verdicts, the finding and its reconciliation.

**Finding and resolution:** the review found one **minor** segmentation defect, F1: two hints treated
the はい substring of 職員はいない as affirmative "yes", crossing the boundary between topic は and
negative existential いない. We confirmed the actual clause boundary and removed only those two lexical
spans, replacing them with function exclusions. The genuine affirmative はい in the braille dialogue
remains unchanged. The original reviewer verified the repair and preservation, marked F1 **resolved** at
its original severity, and found no changed-passage regression. Final correctness, scoped coverage and
comprehensibility are **CLEAN** within the combined original-review/reconciliation scope.

**Preservation and integration:** the resulting 967 spans and 1436 exclusions cover the 88 prompts.
All 1168 existing question/answer/level objects, original groups and 1080 unaffected vocabulary records
remain unchanged. All 240 N4 tasks now have a group and reviewed lexical support; global vocabulary
coverage is **859/1168**, with 309 pending and the inventory still `pilot`. The 59 new context-key strings
include paired scenarios, not 73 independent conversations. Content/vocabulary checks, 151 focused
regressions and the freshly rerun, non-skipped real Android importer pass. These checks are not
linguistic proof. No app, SRS, new exercise, article-content or phone UI change is claimed.

**Reflection (add):** matching a known spelling is not enough to identify a word at a particular
occurrence. A useful lexicon addition can introduce a false match in another already-scanned prompt.
Recheck affected boundaries and senses; valid offsets and complete coverage do not detect this error.
The [authoring source guide](docs/grammar-authoring-sources.md#reusing-lexical-annotations) records the
concrete check without globally banning the legitimate word. Unchanged articles and inherited answer
alternatives were preserved, not newly certified by this consolidation.

## Desire comparison: independent review and reconciliation (2026-10-22 UTC)

**Snapshot and scope:** `0a7e9eb414ca018352888fed31774d6aa1335039` plus installment 9 under
[issue #14](https://github.com/stop-cran/learning-japanese/issues/14): the complete 238-line original article,
all 34 complete exercises and lexical records, the source ledger, and the exact reciprocal-link changes with
surrounding context in the wants and giving/receiving articles. One fresh independent reviewer covered all
three facets; its actual runtime model ID was unavailable. Only reusable lessons, not historical reports or
author research/generators, accompanied the initial assignment. The [source ledger](docs/grammar-desire-sources.json)
preserves the unmodified initial report, reconciliation, severities and both snapshots.

**Initial findings and resolution:** the article, lexical annotations and reciprocal edits were CLEAN.
The reviewer found a **minor** accepted-answer omission: six fitting 手つだって... realizations were missing
across three help tasks (IND-DESIRE-001). It also found **moderate** question-side leakage: two selection
instructions prescribed the missing ほしい and five role questions named the requested participant in English
(IND-DESIRE-002). Both findings were confirmed, not accepted merely by reviewer authority.

The repair adds the documented same-sense spellings without new semantic buttons, presents the two noun-choice
candidates symmetrically, and uses explicit Japanese 私/あなた references with common role-neutral English
instructions in all eight paired role tasks. Necessary disambiguation was not simply removed. Thirteen objects
and their records changed; the other 21 remain identical. IDs, targets, levels and groups are unchanged.
The same reviewer independently reconciled **both findings as resolved**, retaining their original severities.
It reread all 13 complete revised objects/records, checked the actual diff and all 34 bindings, and proved the
other 21 identical. All facets are now **CLEAN** within that composite scope, with no regression, optional
suggestion or consequential unresolved claim. This is not a fresh reread of every unchanged final-file line.

**Preservation and integration:** all 1134 previous complete exercise objects and inventory records remain
unchanged. Only the two declared reciprocal article links update existing runtime assets. The 34 new tasks
comprise 16 formation, 12 interpretation and six contextual-selection items: **30 N4 and four N5-only**
quotation/question role tasks. They have 98 accepted renderings, 68 base options, 105 lexical spans and
197 exclusions. Six groups have 17 facets, five soft recommendations and no hard prerequisites.
Current practice has **1168 exercises in 54 sets**, with **771/1168** reviewed vocabulary records and the
original 397 pending at `pilot`. Content/vocabulary, preservation, deterministic manifest
`abd5f846019eacf4` and the freshly executed real Android importer pass. Integration is not linguistic proof.

**Reflection:** these findings reinforce the existing spelling-recognition and actual-operation lessons below.
Checking only model-kanji plus all-kana answers misses mixed-script dictionary spellings. Correct Japanese
and correct keys do not ensure a useful assessment if English instructions supply the requested role.
The repair preserves support while requiring interpretation. Sixteen context-key strings include paired
forms/roles, not 34 independent conversations or unrestricted mastery. Observation and benefactive forms stay
optional; the 38-set/635-object construction screen is not a fresh audit of those older objects.
No native certification, exhaustive official syllabus, app/SRS change or phone UI check is claimed.

## N5 explanations, quotations and endings: independent review (2026-10-22 UTC)

**Snapshot and scope:** `1422bdf8e755dee9fe85ee0276a7db33b7258bf7` plus installment 8 under
[issue #12](https://github.com/stop-cran/learning-japanese/issues/12): the complete 279-line article,
all 52 complete exercises, their lexical payloads and 52 full inventory records, all groups and the
1674-line source ledger. One fresh independent reviewer covered all three facets; its actual runtime
model ID was unavailable. Only the assigned reusable lessons were supplied, not historical reports
or author research/generators. The [source ledger](docs/grammar-n5-endings-sources.json) preserves the
original report and hashes. Its reviewer-local date is 2026-10-23; integration dates are UTC.

**Result:** article, exercise set, lexical support and provenance are **CLEAN in correctness,
scoped coverage and comprehensibility**. No actionable finding, optional suggestion or consequential
unresolved claim remains. The reviewer independently read all eight primary and seven supporting
lessons, supplementary teaching pages and the seven exact response-label entries. It additionally
checked an explanatory-predicate conjugation chart through an actual source link. No repair or
artificial reconciliation round was required; runtime and all 52 lexical records remain as reviewed.

**Preservation and integration:** all 1082 previous complete exercise objects and inventory records,
all prior runtime assets and unrelated caches are unchanged. The 52 new tasks comprise 38 formation
and 14 bounded interpretation items, with 86 accepted renderings, 110 base options, 12 additional
fitting options, 132 lexical spans and 225 exclusions. Eight groups have 20 facets, seven soft
recommendations and no hard prerequisites. Current practice has **1134 exercises in 53 sets**,
including **583 N5**, with **737/1134** reviewed vocabulary records and the original 397 pending at
`pilot`. Content/vocabulary checks, deterministic manifest `b10336f60f893b3f` and the freshly
executed real Android importer pass. Integration is separate from linguistic review.

**Reflection:** the clean result reinforces existing visible-boundary and entailment guidance.
Short-copula restrictions cover the inner past predicate as well as the final ending; interpretation
separates grammatical presentation from factual truth. Requested formation avoids manufacturing a
unique natural ending from an English gloss or imagined intonation. Recognition-only なあ／お・ご
pages do not import every larger construction in their examples into N5 choices. These are
applications of existing guidance, not a new failure or checklist quota. The 36 key strings account
for paired forms and frames, not 52 independent conversations or unrestricted discourse mastery.
The 35-set/477-object inventory screen is not a fresh full linguistic audit of older material.
No audio/prosody assessment, native certification, app/SRS change or phone UI check is claimed.

## N5 giving, receiving and viewpoint: independent review (2026-10-22)

**Snapshot and scope:** `cbdfd15ef7520624ea8cf748f601842157250a79` plus installment 7 under
[issue #11](https://github.com/stop-cran/learning-japanese/issues/11): the complete 237-line article,
all 36 complete new exercises and vocabulary records, every answer/option/rationale, all groups
and the source ledger. One fresh independent reviewer covered correctness, scoped coverage and
comprehensibility; its actual runtime model ID was unavailable. It read only the assigned reusable
lessons, not historical reports or author research/generators. No model comparison is claimed.
The [source ledger](docs/grammar-n5-giving-sources.json) retains the frozen hashes, complete initial
report and separate integration evidence.

**Result:** the article and complete exercise/lexical set are **CLEAN in all three facets**.
There are no actionable findings, optional suggestions or consequential unresolved claims.
The reviewer independently inspected the three basic-transfer lessons, three inflection lessons,
supplementary Japanese teaching examples and exact dictionary senses/readings. It checked every
literal completion, both fitting human-source markers, matched giver/receiver interpretations and
the explicitly requested third-person viewpoints. No repair or artificial reconciliation round
was needed: the reviewed runtime and all 36 lexical records remain unchanged.

**Preservation and integration:** all 1046 previous complete objects, their vocabulary records,
all prior runtime files and unrelated caches are preserved. The new set has 20 formation, eight
interpretation and eight contextual-selection tasks, with 66 accepted renderings, 80 base options,
two additional correct options, 108 lexical spans and 188 exclusions. Four groups contain 11 facets,
three soft recommendations and no hard prerequisites. Current practice has **1082 exercises in
52 sets**, including **531 N5**, with **685/1082** reviewed vocabulary records and the same 397 pending
at `pilot`. Content/vocabulary checks, deterministic manifest `1a4cf7e602926e50` and the freshly
executed real Android importer pass. Integration is separate from linguistic review.

**Reflection:** retain the matched-event approach: the actual giver/receiver, grammatical frame and
adopted viewpoint are distinct. The clean result reinforces the existing matched-example and
literal-role checks, rather than establishing a new defect or a fixed family/person prohibition.
This distinction is useful for the later benefactive/desire follow-up. Eleven context-key strings
are not proof of 36 independent conversations or demonstrated mastery. The 35-set/525-object
inventory screen was not a new full linguistic audit of older material; six supporting word-card
reads were distinct from the reviewer's fresh dictionary retrievals. No native certification,
app/SRS change or phone UI check is claimed.

## N5 comparisons, change and degree: independent review and reconciliation (2026-10-22)

**Snapshot and scope:** `68359e278a075a9ef5562d126cf2c2ad037fdf5a` plus installment 6 under
[issue #15](https://github.com/stop-cran/learning-japanese/issues/15): the complete 250-line article,
all 42 complete new exercises and vocabulary records, metadata, six primary anchors, exact secondary
support and a new group owning five unchanged N5 quantity/limit tasks. The
[source ledger](docs/grammar-n5-comparisons-sources.json) preserves original/revised hashes,
complete reports, adjudication and integration evidence. One fresh independent reviewer covered
all three facets; its actual runtime model ID was unavailable. It read only the assigned reusable
lessons, not historical reports or author research/generators. No model comparison is claimed.

| Initial observation | Reconciled disposition |
| --- | --- |
| IND-COMP-001, Minor: two weather tasks omitted recognized same-sense さぶい forms | Resolved: accept さぶくなりました and さぶいです in their respective tasks, explain the recorded pronunciation, and preserve the さむい models. |
| O03, optional: one source sentence called required とても support-only | Resolved: clarify its required degree/excess role; the complete-task level mapping was already correct. |
| O01/O02, optional: ordinary-form feedback order and more precise 操作 English wording | Remain optional and unapplied, not withdrawn or declared false. The reviewed Japanese forms and keys are sound. |

**Same-reviewer reconciliation:** the original reviewer read the complete 59-line actual diff,
251-line packet, both entire changed objects/records and the revised snapshot. The initial review
carries forward for the unchanged article, other 40 new objects and bounded five-task reuse.
Article, new exercises and reused group are **CLEAN in correctness, scoped coverage and
comprehensibility within that composite scope**. No new actionable finding or consequential
unresolved claim remains. The initial exercise-correctness NEEDS FIX verdict stays bound to its
original snapshot; this is not a second full linguistic audit.

**Preservation and integration:** all 1004 earlier complete objects and inventory records are
unchanged, including all 15 old objects in the reused file. Reconciliation changes only two new
answer lists and their explanatory notes, plus their two inventory context hashes. The new set has
127 accepted renderings, 84 base options, two additional correct options, 93 lexical spans and
199 exclusions. Eight groups contain 16 facets, six soft recommendations and no hard prerequisites.
The reused group has five members and two facets; its five old lexical records remain pending.
Current practice has **1046 exercises in 51 sets**, including **495 N5**, with **649/1046** reviewed
vocabulary records and the same 397 pending at `pilot`. Content/vocabulary checks, deterministic
manifest `0f4968e36448e7be` and the freshly executed real Android importer pass. All other runtime
assets and unrelated caches are preserved. Integration is separate from linguistic review.
Final staged-diff inspection also removed one stray CR before the inserted group's comma.
The same reviewer checked the complete 12-line diff and exact one-byte removal: all other bytes
and parsed content are unchanged, so the composite verdicts carry forward. Both earlier reports
remain untouched; this follow-up is formatting verification, not another linguistic audit.

**Reflection:** regroup the existing supplied-word recognition lesson to make its adjective
application explicit, including words inside meaning-focused tasks. A default reading is not an
exclusive-pronunciation instruction, and recognition does not establish equal frequency. The
secondary-source wording repair reinforces the existing complete-required-choice level policy;
neither finding warrants a duplicate checklist rule. The 26 formation, eight interpretation and
eight contextual-selection tasks are scaffolded practice, not unrestricted discourse mastery;
26 example-key strings are not proof of independent scenarios. No native certification, app/SRS
change or phone UI check is claimed.

## N5 reasons and contrasts: independent review and reconciliation (2026-10-22)

**Snapshot and scope:** `7a16f02d752812c9ae3b9a508af2847173115c8d` plus installment 5 under
[issue #9](https://github.com/stop-cran/learning-japanese/issues/9): the complete 284-line article,
all 34 complete new exercises and vocabulary records, metadata, five primary anchors and bounded
supporting material. The [source ledger](docs/grammar-n5-reasons-sources.json) preserves original and
revised hashes, complete reports, adjudication and integration evidence. One independent reviewer
covered all three facets; its actual runtime model ID was unavailable. It read only the specified
reusable lessons, not historical reports or author conclusions. No model comparison is claimed.

| Initial observation | Reconciled disposition |
| --- | --- |
| N5RC-F01, Minor: a nonpast-only copula restriction left two past-noun tasks rejecting fitting expanded plain-past forms | Resolved: explicitly request the ordinary short affirmative past noun predicate in those two instructions; rebind only their context hashes. The unchanged article's practice description is now accurate. |

**Same-reviewer reconciliation:** the original reviewer read the complete 20-line diff, 253-line
packet, both complete changed objects/records and the unchanged article practice-description passage.
The initial full review carries forward for the other 32 objects and unchanged material. Article and
exercises are **CLEAN in correctness, scoped coverage and comprehensibility within that composite
scope**. No new actionable finding, optional finding or consequential unresolved claim remains.
The initial article-correctness and exercise-correctness/comprehensibility NEEDS FIX verdicts remain
attached to their original snapshot; this is not a second full linguistic audit.

**Preservation and integration:** all 970 earlier exercise objects and inventory records are unchanged.
Only two question-side instruction fields and their context hashes change during reconciliation.
All 110 accepted renderings, 74 base options, six additional correct options and 101 lexical spans
remain unchanged. Six groups contain 17 facets, five soft recommendations and no hard prerequisites.
Current practice has **1004 exercises in 50 sets**, including **453 N5**, with **607/1004** reviewed
vocabulary records and the same 397 pending at `pilot`. Content/vocabulary checks, deterministic
manifest `67e6c78ccc87d886` and the freshly executed real Android importer pass; all older runtime
assets and unrelated caches remain intact. Integration is separate from linguistic review.

**Reflection:** regroup the existing register/visible-scope lesson with the observed tense-branch
example: a restriction expressly limited to nonpast forms does not bound a past task. Existing
template-branch checks already apply; no speculative or duplicate rule is needed. The 22 formation,
four contextual-selection and eight interpretation tasks are scaffolded practice, not unrestricted
discourse mastery; 24 key strings account for paired examples, not proven independent scenarios.
Sentence-level conjunctions, open replies and explanatory んですが remain supporting reading.
The CAPTCHA-blocked そして lesson was not inspected or bypassed; its bounded unscored use has
separate index/card/dictionary support. No native certification or app/SRS change is claimed.

## N5 wants, plans and invitations: independent review and reconciliation (2026-10-22)

**Snapshot and scope:** `dd621c44ff34343844ac33282c859402a9239559` plus installment 4 under
[issue #10](https://github.com/stop-cran/learning-japanese/issues/10): the complete 249-line article,
all 38 complete new exercises and selected vocabulary records, metadata, seven primary anchors,
secondary-supported requests and bounded reuse of six existing intention drills.
The [source ledger](docs/grammar-n5-wants-sources.json) preserves initial/revised hashes, complete
reports, adjudication and integration evidence. One independent reviewer covered all three facets;
its actual runtime model ID was unavailable. It read only the specified reusable-lesson range, not
historical review reports or author verdicts. No model comparison is claimed.

| Initial observation | Reconciled disposition |
| --- | --- |
| IND-WANTS-001, Minor: four typed-answer lists omitted verified ゆく／往く realizations of the supplied going verb | Resolved: add 14 same-sense renderings and rebind the four context hashes; model buttons and teaching defaults stay unchanged. |

**Same-reviewer reconciliation:** the original reviewer read the complete 56-line answer diff,
453-line packet, all four changed complete objects/records and separate 360-line formatting diff.
The initial review carries forward for the unchanged article, 34 unchanged new objects and bounded
reused material. Article and exercises are **CLEAN in correctness, scoped coverage and comprehensibility
within that composite scope**. No new actionable defect, optional suggestion or consequential unresolved
claim remains. The original exercise-correctness NEEDS FIX verdict stays bound to its initial snapshot.

**Preservation and integration:** all 932 earlier exercise objects and inventory records are unchanged.
Only accepted-answer lists change in four new objects, from 108 to **122** total renderings; only their
inventory context hashes change. There are still 98 base options, ten additional correct options and
74 lexical spans. Eight new groups have 19 facets, six soft recommendations and no hard prerequisites.
The six reused intention tasks gain one two-facet group; their older vocabulary records remain pending.
The old file's compact formatting is retained, and its parsed JSON equals the initial reviewed version.
Current practice has **970 exercises in 49 sets**, including **419 N5**, with **573/970** vocabulary-reviewed
prompts and the same 397 pending records at `pilot`. Content/vocabulary checks, deterministic manifest
`7c0052a2314b4aa9` and the freshly executed real Android importer pass; unrelated caches and other
runtime assets remain intact. These integration checks are separate from linguistic review.

**Reflection:** regroup the existing recognition lesson to check a supplied verb's same-sense readings
and spellings across parallel grammar frames, without promoting uncommon variants to default buttons.
A default parenthetical reading is not a hidden pronunciation-only task. No duplicate checklist rule or
exhaustive rare-spelling quota is added. The 26 formation, eight contextual-selection and four scaffolded
interpretation tasks are not unrestricted conversational mastery; 16 context keys account for paired
scenarios. はどうですか and the N4 desire bridge remain supporting reading, not additional scored facets.
No second full audit, native certification or app/SRS change is claimed.

## N5 noun descriptions: independent review and reconciliation (2026-10-22)

**Snapshot and scope:** `f3695d9601ce3a77e92e380c1a5b3930ef918f18` plus installment 3 under
[issue #8](https://github.com/stop-cran/learning-japanese/issues/8): the complete 230-line article,
all 32 complete exercises and selected vocabulary records, metadata, 13 primary anchors and pertinent
reuse of six existing attachment drills. The [source ledger](docs/grammar-n5-descriptions-sources.json)
preserves initial/revised hashes, complete reports, adjudication and integration evidence.
One independent reviewer covered all three facets; its actual runtime model ID was unavailable.
It read only the specified reusable-lesson range, not historical review reports or author verdicts.
No model comparison is claimed.

| Initial observation | Reconciled disposition |
| --- | --- |
| IND-DESC-001, Minor: a supplied independent-clause control had 焼いました and reading やい | Resolved: 焼きました / やき, with rebound vocabulary/context hashes. The correct plain-past modifier 焼いた / やい is unchanged. |
| IND-DESC-002, Minor: four wrong-scope rationales affirmatively defined the wrong reading | Resolved: explain the actual head noun, inner object and whole nominalized activity in each sentence. |

**Same-reviewer reconciliation:** the original reviewer read the actual 67-line diff, the complete
536-line packet and all five changed complete objects/records. The initial review carries forward for
the unchanged article and 27 unchanged exercises. Article and exercises are **CLEAN in correctness,
scoped coverage and comprehensibility within that composite scope**. No new actionable defect,
optional suggestion or consequential unresolved claim remains. The original exercise correctness and
comprehensibility NEEDS FIX verdicts remain attached to their original snapshot.

**Preservation and integration:** all earlier 900 exercise objects and inventory records are unchanged.
New exercise IDs, targets, levels, relationships, keys, accepted answers, option IDs/labels and groups
survive reconciliation. Six groups have 14 facets, five soft recommendations and no hard prerequisites.
There are 64 accepted renderings, 76 base options and 71 lexical spans. Current practice has **932 exercises
in 48 sets**, including **381 N5**, with **535/932** vocabulary-reviewed prompts and the same 397 pending
records at `pilot`. Content/vocabulary checks, deterministic manifest `6a16fcd05f857be8` and the freshly
executed real Android importer pass; unrelated caches and other runtime assets remain intact.
These integration checks are separate from the reviewer's linguistic conclusions.

**Reflection:** add one observed supplied-inflection check: a correct plain-past sound change is not a
reusable polite stem, and matching lexical offsets cannot establish grammatical correctness. Regroup the
existing contextual-distractor lesson to cover interpretation labels rather than add a duplicate rule.
The 24 formation, four interpretation and four recognition tasks remain scaffolded; the outer activity が
is supplied, not independently selected. Broader omission, relative-tense and が／の production remain
outside the assessed scope. No second full audit, native certification, mastery or app/SRS change is claimed.

## N5 pointing/questions: independent review and reconciliation (2026-10-22)

**Snapshot and scope:** `c80d4533e613b8010b4d6e8b09f16eceeeea756c` plus installment 2 under
[issue #13](https://github.com/stop-cran/learning-japanese/issues/13): the complete article and all 54 exercises.
The [source and coverage ledger](docs/grammar-n5-pointing-sources.json) preserves the initial/revised hashes,
all 19 assigned primary anchors, secondary-supported どうやって, complete reports, actual diff/packet hashes
and integration evidence. One independent reviewer covered all three facets; its actual runtime model ID
was unavailable. It incidentally saw unrelated historical review summaries while locating reusable lessons,
but no earlier pointing/questions review or author verdict. Perfect historical blinding and model comparison
are not claimed.

| Initial observation | Reconciled disposition |
| --- | --- |
| N5PQ-F01, Minor: statement explanations described a requested question | Resolved: local statement feedback and explicitly conditional instructions in all four ending tasks. |
| N5PQ-F02, Minor: four lists omitted spellings of already accepted optional wording | Resolved: 何方／如何 added without new semantic buttons or frequency claims. |
| N5PQ-F03, Minor: four broadly worded person-phrase tasks omitted respectful variants | Resolved: どなたかに／どなたにも／どなたかと／どなたとも and their 何方 spellings accepted; register explained. |
| N5PQ-O01/O02, optional: templated English and generic case/interpretation feedback | Adopted and resolved: remove doubled articles, identify the unknown book, and localize the relevant explanations. |

**Same-reviewer reconciliation:** the original reviewer assessed the revised article passages, the exact
498-line diff and all 38 complete changed objects; the initial review explicitly carries forward for
16 unchanged objects and unchanged teaching/metadata. The article and exercises are **CLEAN in correctness,
scoped coverage and comprehensibility within that composite scope**, with no new actionable defect or
consequential unresolved claim. Initial exercise coverage/comprehensibility NEEDS FIX verdicts remain tied
to the original snapshot; no incorrect Japanese model was established.

**Preservation and integration:** all prompts, exercise identities, targets, levels, option IDs/labels,
old accepted answers, vocabulary payloads and group metadata are preserved. Acceptance rises from 194
to 206 renderings; there are still 162 base options, ten additional options and 81 lexical spans.
The ten groups have 27 facets, four soft recommendations and no hard prerequisites.
All 846 earlier exercise objects and inventory records remain unchanged. Current practice has **900
exercises in 47 sets**, including **349 N5**, with **503/900** vocabulary-reviewed prompts and the same
397 pending records at `pilot`. Content/vocabulary checks, deterministic manifest `bc2c96ccdb8fc270`,
and a freshly executed real Android importer pass: one test, zero skips, failures or errors.
Other runtime assets and unrelated caches remain intact. These are parent integration checks, not reviewer claims.

**Reflection:** regroup three existing checks rather than add duplicate rules: shared-feedback branches,
spellings of optional accepted wording, and respectful bases after case/polarity formation.
The review improved feedback and typed-answer fairness, not the required grammar syllabus.
The 30 context, 20 formation and four interpretation tasks remain scaffolded. Broader discourse pointing,
embedded questions and affirmative question-word patterns are not independently assessed; どんな remains
an optional N4 bridge. No native certification, mastery, second full audit, app/schema/SRS change, APK or phone check is claimed.

## N5 foundations: independent review and reconciliation (2026-10-22)

**Snapshot and scope:** `c7ad52870843aece0b605e69af833c053a93d5cd` plus installment 1 under
[issue #16](https://github.com/stop-cran/learning-japanese/issues/16): four complete entry articles,
two existing-article supplements and all 125 new exercises. The
[source and coverage ledger](docs/grammar-n5-foundations-sources.json) pins the initial/revised content hashes,
all 71 assigned primary anchors, full initial and reconciliation reports, exact diff/packet hashes,
classification decisions and integration evidence. One independent reviewer covered correctness, scoped coverage
and comprehensibility; its actual runtime model ID was unavailable. No model comparison is claimed.

| Initial observation | Reconciled disposition |
| --- | --- |
| N5FI-F01, Minor: the verb article defined a ます-stem without the general godan formation operation | Resolved: added the u-row to i-row rule, useful examples, and the ichidan/irregular contrast. |
| N5FI-F02, Minor: 30 interpretation instructions omitted response-label readings | Resolved: every alternative now has question-side kana, preserving answer-independent ordering. |
| N5FI-F03, Minor: five typed-answer classes omitted recognized 迄／奇麗 spellings | Resolved: eight renderings added; existing answers, models and options retained. |
| N5FI-O01/O02, optional: practice-description and lexical-gloss precision | Adopted: describe scaffolded formation/recognition accurately; split the water/medicine meanings of 飲みます. |

**Same-reviewer reconciliation:** the original reviewer read both revised article passages, the entire exact diff
and all 37 complete changed exercise objects. The initial review is explicitly carried forward for the other
88 objects and unchanged teaching/metadata. Correctness, scoped coverage and comprehensibility are now
**CLEAN within this composite scope**, with no new actionable defect or consequential unresolved claim.
Initial NEEDS FIX verdicts remain attached to their original snapshot.

**Preservation and integration:** all 125 prompts, identities, choices, targets, levels and group metadata survive
the fixes. The final exercises have 328 accepted renderings, 331 base options and 246 lexical spans. All 721
previous exercise objects and vocabulary records are preserved. Six old advice exercises remain in their
own file and acquire one local group, recommended from the new rules practice. There are 16 new groups
with 51 facets, six soft recommendations and no hard prerequisites.
Current totals are **846 exercises in 46 sets**, including **295 N5**, and **449/846** vocabulary-reviewed
prompts; all 397 old pending records remain pending and the stage remains `pilot`.
Content and vocabulary checks, deterministic manifest `aea8964021b7fadb`, and a freshly executed real Android
importer pass; the importer XML contains one test with zero skips, failures or errors. Other runtime assets
and unrelated caches are preserved. These parent integration checks are separate from linguistic review.

**Reflection and instruction maintenance:** add question-side response-label readings as an explicit check;
regroup the existing productive-operation lesson to cover article prerequisites as well as drill instructions.
Retain the existing spelling-recognition, transfer-accounting and contextual-gloss guidance rather than duplicate
it. The independent pass was useful for learner interaction and a missing prerequisite, not evidence that
the displayed Japanese was generally incorrect.

**Limits:** the 87 formation, 34 interpretation and four contextual predicate-selection tasks remain scaffolded
by English meanings and visible restrictions. Negative experience, broader ている inflection and contraction
production are explained rather than independently produced in this installment. The ledger distinguishes
those boundaries from newly practised and reused material. No complete official syllabus, mastery, native
certification, second-model opinion, app/schema/SRS change, APK or phone check is claimed.

## Compound relations: independent review and reconciliation (2026-10-22)

**Snapshots:** `75f7f55ce7a7de27f9be4477eb39aeac526d8a56` plus the local article and exercises.
Initial exercise SHA-256: `3ebfa4c1690aec56addeec6e9481b59d8cf36b66da9053704535a694d13245dc`;
reconciled: `cd21fed8f78a77b4e7de8456b170ab39c0888a0ff6064a3d4f75ac1fd9b60ac1`
(normalized LF). The 305-line article is unchanged. The
[source record](docs/grammar-compound-relations-sources.json) preserves the author snapshot, full original reports,
initial adjudication, exact diff/packet hashes and updated vocabulary/coverage evidence.

**Initial independent scope:** one blinded reviewer assessed the whole article and all 48 complete exercises,
110 accepted renderings, 126 base options, four additional options, 132 lexical spans, 219 exclusions and all
34 canonical vocabulary cards. **Initial verdicts:** article CLEAN in all three facets; exercise correctness and
comprehensibility CLEAN, scoped coverage NEEDS FIX. Both reviewers' actual model IDs were unavailable.

| Observation | Disposition |
| --- | --- |
| CR-F01, Minor: all 22 interpretation instructions listed the keyed answer first | Resolved: definition lists now have fixed answer-independent ordering; short layered-choice lists are counterbalanced across their paired contexts. Definitions, readings and answer units are preserved. |
| CR-O01, optional: repeated scenarios had inconsistent context keys | Adopted and resolved: six keys are aligned across travel/teacher/plan discussions, history-book reading and family-benefit tasks. |
| CR-O02, optional: eight drills printed the exact fragment to copy | Adopted and resolved: six now assemble a noun-plus-relation phrase; two transform a polite verb to plain nonpast plus こと. Visible constraints and every old completed sentence are preserved. |

**Reconciliation:** the original synchronous reviewer had no follow-up-capable agent ID. A fresh informed reviewer
read the original report and exact diff, then assessed 34 complete current objects: all 22 interpretation tasks,
all eight strengthened formation tasks and every context-key-changed task. This covers 95 accepted renderings,
92 base options, two additional options, 92 lexical spans and 179 exclusions. The remaining 14 unchanged objects
carry forward their initial review. The article's original CLEAN verdicts are carried forward with teaching/exercise
consistency checks, not presented as a second full source audit.
All three exercise facets are now **CLEAN within this bounded composite scope**, with no new actionable content
finding or consequential unresolved linguistic claim. A nonblocking packet locator ended one line before the closing
brace; complete object payloads were intact. Corrected ranges are in the report, and future packet generators were
corrected without modifying the frozen evidence.

**Preservation and integration:** 22 exercise payloads changed and 26 are unchanged; IDs, targets, answer classes,
relationships, group/facet structure and recommendation edges are preserved. The eight enlarged blanks retain all
18 former completed renderings and accept 41 current renderings. Other prompts, answers and vocabulary payloads
are unchanged. The final set has 133 accepted renderings, 128 base options, four additional options, 124 lexical
spans and the same 34 canonical identities. All 673 preceding inventory records, 39 published grammar files,
existing runtime payloads and unrelated caches are preserved. Corpus/vocabulary totals remain 721 exercises in
40 files and 324/721 reviewed, still `pilot` with 397 pending. Content/vocabulary checks, 150 focused tests and
a freshly executed real Android importer pass; deterministic manifest `36be4fcdbd03e843`.
These parent integration checks are separate from the reconciler's packet-only verification.

**Usefulness and limits:** the independent pass caught a systematic assessment cue missed by the author, not an
incorrect Japanese rule. Correct-label positions of 10/6/6, 32 context keys and stronger answer operations are
descriptive checks, not measured mastery or independent discourse breadth. Formation remains scaffolded.
No native-speaker certification, model comparison, APK, phone check or automatic issue closure is claimed.

## Compound relations and formal-noun contrasts: earlier author pass (2026-10-22)

**Snapshot:** published `75f7f55ce7a7de27f9be4477eb39aeac526d8a56` plus the new
`articles/about-targets-and-perspectives.md` and `grammar/compound-relations.json`.
Article SHA-256: `525895f8acad5fdd6282790b0fd6feedf86b92dab2931cb5490ffa6fd1524168`;
exercise SHA-256: `3ebfa4c1690aec56addeec6e9481b59d8cf36b66da9053704535a694d13245dc`
(normalized LF). The [source record](docs/grammar-compound-relations-sources.json) pins the inventory,
manifest, inspected sources, canonical identities and article-to-exercise coverage. This is part 4 under issue #5.

**Scope:** direct author review by `gpt-6-astra` of the complete article and all 48 exercises:
110 accepted renderings, 126 base options, four additional correct options, 132 lexical spans,
219 exclusions and all 34 complete linked vocabulary cards.
**Author verdicts, separately for article and exercises:** correctness **CLEAN**; scoped coverage **CLEAN**;
comprehensibility **CLEAN**. No actionable defect or consequential unresolved claim was established in this
bounded pass. **No independent review or reconciliation had been performed at that author snapshot.**

The eight groups have 21 answer classes and 24 facet assignments: 22 formation, 22 interpretation and four
bounded contextual tasks, with six soft recommendations, no hard prerequisites and no inferred JLPT labels.
Core relations, actual noun modifiers, shared subject-matter frames, intended benefit, noun-based attachment
and nominalized/comparative layers are distinguished. Closely paired scenes share keys across facets;
48 tasks are not 48 independently sampled discourse situations.

**Authoring decisions:** accept fitting について／に関して／のことを frames in the shared talking tasks;
keep named-family constraints visible elsewhere. Do not equate に対して with hostility, にとって with every
English "for," or intended benefit with an actual result. Nのこと may concern someone's status, but it does
not explicitly build the same predicate as Nであること. Nominalization does not establish completed experience.
The ordinary 答え spelling correctly links to the existing 答 noun card, not the verb 答える.
Two `____場合` prompts contain only protected grammar and deliberately have no lexical hints.

**Source handling:** inspect actual main/dictionary sections when simplified extraction returns related text,
irrelevant links or nearby entries. Do not adopt the inconsistent 付いて rare-kanji header for について,
universal hostility or thinking-verb restrictions, or the 場合 page's randomness/uncontrollability shortcut.
Dictionary recognition supports accepted spellings, not equal frequency or blanket interchangeability.

**Integration:** all 673 preceding inventory records and 39 published grammar files are unchanged.
The corpus is 721 exercises in 40 files; vocabulary coverage is 324/721, still `pilot` with the same 397 pending.
Content/vocabulary checks, 150 focused tests and a freshly executed real Android importer pass;
manifest `be50a3bc873a2e87` is deterministic. Existing runtime payloads, 396 images, 201 scene catalogs and
unrelated caches are preserved; Android source is unchanged.

**Limits:** supporting i-adjective cases, added は/も, nonhuman evaluators and broader comparative attachment
are not independent new exercise facets. These are author judgments, not native-speaker certification or
measured transfer/mastery. Article 3 was published first; at that stage this new batch remained local and uncommitted.
No APK, phone check or issue closure is claimed.

## Restriction and unexpected inclusion: independent review and reconciliation (2026-10-22)

**Snapshots:** `de0df855080b0bbc0bd9c0565184f21e4c1c9366` plus the local article and exercises.
Initial exercise SHA-256: `173a2a9c64876a37034ceb7b8ffef468b873ef186635e2396ba50c8a98a25d21`;
reconciled: `09c15bbf7faabbf0007f86bcc0c4e7c2b769c19195a2673383b63fbd726a10ce`.
The article remains byte-identical. The [source record](docs/grammar-restriction-sources.json) preserves the
historical author pass, full original reports, adjudication, exact diff/snapshot hashes and updated coverage.

**Initial independent scope:** one fresh reviewer read the whole article and all 48 complete exercises,
126 accepted renderings, 122 base options, eight additional options, 93 vocabulary spans, 220 exclusions
and all 31 canonical vocabulary identities. Author judgments and earlier reviews were withheld.
**Initial verdicts:** article **CLEAN** in all three facets; exercises correctness/comprehensibility **NEEDS FIX**,
scoped coverage **CLEAN**. Neither reviewer's actual model ID was exposed.

| Observation | Disposition |
| --- | --- |
| RII-F01, Minor: a rationale turned ability to come into actual participation | Resolved: the teacher-only alternative now contradicts the friends' ability to come, not an invented attendance event. No answer-key change. |
| RII-O01, optional: limited transfer beyond named/cued patterns | Adopted and resolved: two bounded refrigerator/wallet contexts require choosing the particle or polarity from the whole construction. |
| RII-O02, optional: feedback retained a paired scenario's details | Adopted and resolved: affected explanations refer to their own reading/drinking, ability/error, absence/diet, endpoint, quantity or invitation context. |
| RII-O03, optional: sufficiency versus necessity was explained but not directly offered as a contrast | Adopted and resolved: both conditional tasks offer an exclusive-route distractor and no longer pre-answer sufficiency in the English scene. |

**Reconciliation:** a fresh informed reconciler reviewed all 18 changed and two new complete objects, their
35 vocabulary spans and 82 exclusions, and the group metadata against the original report and exact diff.
The original synchronous reviewer could not receive a follow-up; this is not same-reviewer reconciliation.
All three exercise facets are now **CLEAN within this bounded composite scope**, carrying forward the
original review of 30 unchanged objects. The article's original CLEAN verdicts are carried forward, not
presented as a repeated full audit. No new actionable regression or consequential unresolved claim was found.

**Preservation and integration:** the set now has 50 exercises, 129 accepted renderings, 128 base options,
eight additional options, 97 lexical spans and 33 canonical identities. All original prompts, vocabulary payloads,
targets, answers and accepted renderings are unchanged; only affected context bindings are refreshed.
All 623 preceding exercise/inventory records and unrelated caches remain intact. The corpus is 673 exercises in
39 files, vocabulary coverage 276/673, still `pilot` with the same 397 pending. Content/vocabulary checks,
150 focused tests and a freshly executed real Android importer pass; manifest `2fe260ff984d31a4` is deterministic.
These parent integration checks are separate from the reconciler's packet-only checks and disclosed limits.

**Usefulness and limits:** the concrete gain was a small consistency defect missed when a scene changed to ability,
not a newly discovered particle rule. The optional improvements make feedback local and align options with the
distinctions explained. Four contextual tasks remain guided practice, not evidence of measured transfer or mastery.
An exclusive-route inference is not established by the conditional sentence; this does not prove that its condition
can never also be necessary in a particular situation. No native-speaker certification, app/schema change,
APK, phone check, commit, push or automatic issue closure is claimed.

## Restriction and unexpected inclusion: earlier article and exercise author pass (2026-10-22)

**Snapshot:** `de0df855080b0bbc0bd9c0565184f21e4c1c9366` plus the new
`articles/only-and-unexpected-inclusion.md` and `grammar/restriction-and-inclusion.json`.
The [source record](docs/grammar-restriction-sources.json) pins their hashes, vocabulary binding, manifest and coverage matrix.
This is part 3 under issue #7; parts 1 and 2 were published separately.

**Scope:** direct author review by `gpt-6-astra` of the complete article and all 48 exercise objects:
whole completed sentences, 126 accepted renderings, 122 base options, eight additional options,
all 93 lexical spans and their exclusions, and all 31 linked canonical identities.
**Author verdicts, separately for article and exercises:** correctness **CLEAN**; scoped coverage **CLEAN**;
comprehensibility **CLEAN**. These are bounded author judgments, not independent confirmation.

The eight groups cover restriction, polarity, retained case roles, unexpected inclusion, negative addition/minimum
counts, emphatic versus endpoint まで, context-dependent も/でも, and focus scope with a sufficient-condition boundary.
There are 16 formation, 30 interpretation and two contextual tasks, with 24 group/facet assignments, six soft
recommendations and no hard prerequisites or inferred JLPT labels.

**Authoring decisions:** compare subject-focused だけ negatives with しか negatives rather than assigning every
object-negative sentence one scope. Keep fitting case-particle orders and recognized 丈/迄 spellings.
Use explicit ability/generic-error contexts for broad shared inclusion, not an assumption that every past-arrival
でも is scalar. Clarify that ability is not an actual arrival, ordinary も need not be surprising, and conditional
さえ supplies sufficiency rather than logical uniqueness. Use books/newspapers rather than assume books/manga are
disjoint categories; invitation glosses do not assert factual nondrinking/nonreading.

**Integration:** all 623 prior exercises and complete inventory records are preserved. Vocabulary coverage is
274/671, still `pilot`, with the same 397 pending. Content/vocabulary checks, 150 focused tests and a freshly executed
real Android importer pass; only the article and exercise set are new runtime payloads.

**Limits / remaining work:** no independent review or reconciliation has been performed for this draft.
Matched contexts and shared alternatives are not separately mastered distinctions. Broader register, dialect,
paraphrase and conditional coverage remain outside scope. No app/schema change, APK, physical-phone check, new
commit or push is claimed; unrelated Python caches remain untouched and issue #7 is not automatically closed.

## Basic nouns and particles: independent exercise review and reconciliation (2026-10-22)

**Snapshots:** baseline `f6c45c5f9c4f35a8d6d94a6863862bd7edfcf178` plus local basic-particle content.
Initial exercise SHA-256: `03c910a78a3c457f3a5b90942727dc73b2f26827932efa59cac73a4e6d4936ad`;
corrected: `04cde4d224761003203502896656acbd03934ec2f1dc2b671a865b93718e0a15`.
The [source record](docs/grammar-basic-particles-sources.json) preserves full reports, exact snapshot/diff hashes,
parent adjudication, source passages and historical author verdicts. The independently reviewed article is unchanged.

**Initial independent scope:** one fresh reviewer read all 64 exercises, every accepted form, 188 base options,
four initial extra options, 159 lexical spans, 258 exclusions, all 52 canonical cards and the article as coverage context.
Author rationale/verdicts and earlier article-review reports were withheld.
**Initial verdicts:** correctness **NEEDS FIX**; scoped coverage **CLEAN**; comprehensibility **NEEDS FIX**.

| Finding | Initial severity/status | Correction |
| --- | --- | --- |
| BPI-F01: the language-use request rejected 日本語を話します | Moderate | Accept を beside で with a substantive extra correct button; explain object versus medium. Keep the fixed 手紙を sentence distinct and rename the unpublished local class coherently to `language-use`. |
| BPI-F02: meaningful typed spellings were omitted | Minor | Accept 迄, 迄に and 3時 in their applicable tasks; retain ordinary model buttons rather than adding spelling-only choices. |
| BPI-F03: the polite negative did not exclude ではございません | Minor | State ordinary ありません/ないです formation explicitly and acknowledge that the more-polite alternative is grammatical but outside this drill. |
| BPI-L01: allowed contractions could include rough ない variants | UNVERIFIED task boundary | Require standard ない in the plain drill and say that the permitted contraction is では to じゃ. Do not conflate neutral/rough with plain/polite. |

Optional self-contained feedback, the formal わたくし reading with a register note, and explicit single-particle noun
linking were adopted (O02/O04/O05). Extra route/departure/relative-time practice and broader transfer variation
remain optional future work (O01/O03), not newly invented acceptance requirements.

**Reconciliation:** F01-F03 and L01 **resolved**; adopted O02/O04/O05 **resolved**; O01/O03 remain **optional**.
Correctness, scoped coverage and comprehensibility are **CLEAN within the bounded reconciliation scope**,
with the initial review's unchanged-content coverage explicitly carried forward. No new actionable regression
or consequential unresolved linguistic concern was identified.
The original review session rejected follow-up messages because it ran in sync mode. A fresh reconciliation reviewer
was therefore supplied the original report, before/after snapshots and exact diff. This is not same-reviewer
reconciliation or a second fresh linguistic audit of all unchanged exercises. Neither actual model ID was exposed.

**Preservation and integration:** 17 exercise objects changed and 47 remained identical; all 64 Japanese prompts,
vocabulary payloads and canonical cards remain unchanged. Only context hashes changed in the corresponding
17 inventory records; all 606 other complete records are preserved. There are now 98 accepted renderings and five
meaningful extra choices across three eligible questions. Content/vocabulary checks, 150 focused tests and a freshly
executed real Android importer pass; manifest `f89227c7dda18b9f` rebuilds deterministically.
The corpus remains 623 exercises in 38 files, with vocabulary coverage 226/623, `pilot`, and the same 397 pending.
The actual external `topic-architecture` recommendation and source-global group uniqueness are parent integration
evidence, separate from the reviewer's initially bounded packet access.
The reconciler verified the supplied target but left source-global uniqueness (BPI-L02) and full-inventory
preservation (REC-L02) **UNVERIFIED** outside its packet. The parent checks above resolve those integration limits;
the source record preserves both the reviewer's limits and the separate parent evidence.

**Limits:** no native-speaker certification, exhaustive paraphrase/dialect claim, Android source change, APK or phone
check. Signed publication is authorized after review; this entry does not assert a push before it happens.
Unrelated Python cache files remain outside the publication batch, and issue #4 is not automatically closed.

## Basic nouns and particles: earlier independent article review and exercise author pass (2026-10-21)

**Snapshot:** `f6c45c5f9c4f35a8d6d94a6863862bd7edfcf178` plus the local basic-particle article.
The independent packet pins article SHA-256
`1818b4b3804d63c19b6175d40235cda836b5861e2431fa6dc6cfdb7dea1dde1f`
and packet manifest SHA-256 `6ae696a8710f63f79d30830f9994de8dc2958da0aabee4828a5854dcf09480d9`.
The [source record](docs/grammar-basic-particles-sources.json) preserves the original report, inspected evidence,
author adjudication and separate later exercise/integration hashes.

**Independent scope:** one fresh reviewer read all 424 article lines against the three-facet rubric and issue #4.
The packet supplied the article, linked references and source navigation, withholding author verdicts/rationale.
The actual model identifier was not exposed, so no model is attributed or comparison claimed.
**Article verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.
**Findings / optional:** none. No consequential unresolved claim was identified. The article was left byte-identical;
no correction or reconciliation round was necessary or claimed.

**Exercise author scope:** 64 new exercises in `grammar/basic-particles.json`, with 11 introduction groups,
32 group-facet assignments, seven soft recommendations and no hard prerequisites or invented JLPT labels.
Direct author review by `gpt-6-astra` covers whole completed sentences, visible task restrictions, accepted forms,
every option/rationale and occurrence-specific vocabulary. The coverage matrix distinguishes graded facets from
article-only signposts. **Exercise author verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**;
comprehensibility **CLEAN**.

The exercises separate formation, contextual selection, interpretation and pronunciation. Broad destination tasks
accept に／へ／まで, with the goal/direction/extent difference explained rather than silently rejecting a fitting form.
Noun negatives retain appropriate contracted and uncontracted alternatives. Clock-time/duration expressions and
tested particle sounds are protected targets, not lexical hints that supply the answer. Kana はさみ links to the
existing 鋏 card rather than inventing a missing canonical identity.

**Integration:** the source record contains the current content/vocabulary, focused-test, deterministic-manifest
and real-importer results. The 559 existing exercises and all 559 prior vocabulary records are preserved;
64 reviewed records bring coverage to 226/623, still `pilot` with the same 397 pending.

**Limits:** the article's independent verdict does not extend to the subsequently authored exercises.
No independent exercise review, native-speaker certification, exhaustive alternative inventory, physical-phone
check, app/schema change, commit or push is claimed. Issue #4 remains open.

## Basic nouns and particles: earlier article-only author pass (2026-10-21)

**Snapshot:** `f6c45c5f9c4f35a8d6d94a6863862bd7edfcf178` plus
`articles/japanese-nouns-and-basic-particles.md`, SHA-256
`1818b4b3804d63c19b6175d40235cda836b5861e2431fa6dc6cfdb7dea1dde1f`.
The [source and coverage record](docs/grammar-basic-particles-sources.json) identifies actual inspected
passages, retrieval limits, linked-card checks and the article's bounded coverage.

**Scope:** direct author review by `gpt-6-astra` of the complete 424-line article, its examples/readings/
translations and the relevant meanings/patterns of all ten linked canonical words. This pass implements
the article portion of [issue #4](https://github.com/stop-cran/learning-japanese/issues/4), not its exercise set.
**Verdicts:** correctness **CLEAN**; scoped coverage **CLEAN**; comprehensibility **CLEAN**.

| Authoring concern | Disposition |
| --- | --- |
| Calling the subject a doer and every を phrase an affected object creates false generalizations | Qualified: include state/existence subjects, preference-pattern navigation and route/departure を. |
| A verb-only に/で shortcut misses event ある | Addressed: contrast locating a library with a class taking place at school. |
| English at/with/to can hide different roles or fitting alternatives | Addressed: paired library and letter-writing contexts, vehicle-plus-predicate contrasts, and explicit に/へ overlap. |
| Saying nouns do not decline could be mistaken for denying noun-predicate endings | Addressed: distinguish the stable noun from the changing だ/です, negative and past material. |
| An exact-looking source URL or extraction may lead to the wrong lesson | Recorded: failed URLs are not evidence; Bunpro's emphatic まで page is not used as the temporal-limit explanation. |

**Integration:** content validation and the real Android importer pass; manifest `d1a8b4e2c9963e3e`
rebuilds deterministically with exactly one new runtime payload, the article. All previously published
payloads, the 559 existing exercises and their complete vocabulary inventory remain unchanged.
Vocabulary coverage stays 162/559, `pilot`, with 397 pending.

**Optional / remaining work at this snapshot:** the covering exercises, their coverage matrix, vocabulary support
and introduction groups had not yet been authored; the later pass is recorded above. Fuller word-order, copula,
passive/causative, relative-clause and omission treatment
is beyond this introductory article.
**Limits:** author self-review only, not independent review, native-speaker certification, exhaustive alternatives,
new JLPT classification or a physical-phone check. The preceding article's independent verdicts do not transfer
to this new one. This article draft remains local; the topic-particle batch was published separately at `f6c45c5`.

## は／が／も independent review and reconciliation (2026-10-21)

**Snapshots:** `7a92dde23107173af8aabef51971dbc66b754a93` plus the local topic-particle additions.
The [source and review record](docs/grammar-topic-sources.json) preserves the initial article/exercise hashes
`7c96233a…` / `3e561579…` and their historical author and independent verdicts.
The reconciled article is SHA-256 `b6d1a5e9fc7ddf353c3ce6539301d3237710288c7abbb2a70a4b262f70ee90a1`;
the exercise file is `57ae76fcf563c20ab0c5c9217657c2cc9b1e5a5c21c5b2425d3dcb538a5fbf93`.
Vocabulary inventory: `96dec70f6fde272a87022d3b300b0b4a02089ecf42ce3fed539d1ff48b05a4f0`.

**Initial independent scope:** `gpt-6-astra` and `claude-opus-5.5` each reviewed the complete article,
all 36 exercises, 54 accepted renderings, 114 base options, three additional correct options, six groups,
110 lexical spans, 180 exclusions and relevant senses/readings in 48 canonical cards. Both received the same
frozen packet without author verdicts or the other review. Actual model IDs were confirmed from parent runtime
metadata, separately from the reviewers' own inability to see their runtime identifiers.

**Reconciliation scope:** both original reviewers received the revised snapshot, their original findings,
the other initial report, parent adjudication and exact diff. Each read the complete 351-line revised article,
all 11 changed exercises, dependent metadata and adjacent content. The 25 unchanged exercises and canonical
senses carry forward on matching content; this is informed reconciliation, not another blind full-corpus audit.
Neither reviewer saw the other's reconciliation report.

**Final verdicts from both reviewers:** article correctness **CLEAN**, scoped coverage **CLEAN**,
comprehensibility **CLEAN**; exercises correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**.
No new actionable regression or consequential unresolved claim was established.

| Underlying observation | Contribution | Reconciled disposition |
| --- | --- | --- |
| Factual non-drinking was described as refusal | Astra | **Resolved:** feedback states only that the speaker does not drink coffee. |
| Generic が feedback hid a buyer/eater/worker role change | Both; Opus additionally identified Tuesday | **Resolved:** predicate-specific explanations and wrong-option rationales. Different original severity labels do not make the shared object cases separate discoveries. |
| The opening 私は／私が学生です pair lacked a direct matched-context explanation | Opus | **Resolved:** ordinary self-introduction versus identifying who is the student; concrete brother/book feedback. Both は and が remain accepted. |
| 対比 was used for a narrower response class than general grammatical contrast | Opus | **Resolved:** 相違（そうい） and matching definitions, buttons, answers and metadata; the article distinguishes stated outcomes from implied contrast. |
| Pronunciation/readings and the window example could be more accessible | Astra / Opus | **Resolved:** を pronounced o, 今 and 何も readings, and a room-tour context. |

**Adjudication retained:** Opus accepted the downgrade of its first finding from moderate to minor and explicitly
withdrew the proposed broad rule about が before です/property adjectives: the unfetched Kuno recollection did
not support imposing that restriction. The narrower contextual repair is sufficient. Opus still rates the old
対比 terminology concern minor, while the parent and Astra consider it optional because the task defined the
response class before answering. That historical severity disagreement is preserved, not forced into consensus;
all agree that the revised label resolves it and that the original answer key was not invalid.

**Preservation and integration:** all prompts, lexical annotations and particle answers remain unchanged.
Only two unpublished meaning-label answers change from 対比／たいひ to 相違／そうい; counts remain unchanged.
Only the 11 changed exercises' inventory context hashes differ; all 548 other full records are identical.
The parent checked the full inventory; reviewers explicitly limit their independent inventory checks to the
36 records supplied in the packet. All 523 preceding exercises and 48 linked word cards are unchanged.
Content/vocabulary checks and 150 focused tests pass; the real Android importer ran with one test and no skips
or failures. Manifest `fd29624693a27ec9` is deterministic. Coverage remains 162/559, `pilot`, with 397 pending.

**Optional:** a source explicitly naming neutral-description が would strengthen the existing bounded dictionary
and contextual evidence; neither reviewer considers it a remaining defect. Stronger object-topic wording is
stylistic, not required.
**Limits:** no native-speaker certification, exhaustive paraphrase inventory, new JLPT classification, app change,
phone UI check or measured learning outcome. This pass does not commit, push or deliver an APK.

## Reusable grammar-review lessons

The [は／が／も review record](docs/grammar-topic-sources.json) grounds these lessons in specific findings:

- **Check what the predicate entails, not just a plausible scenario.** A factual negative such as 飲みません does not
  inherently express refusal or deliberate rejection. Feedback must not add intention that the question never supplied
  (ASTRA-TOPIC-001).
  The clean [explanations/endings review](docs/grammar-n5-endings-sources.json) applies the same discipline to
  presentation versus truth: a quoted report or an assertion need not be correct, and a conjectural ending does not
  assign a fixed numerical confidence. Judge the stated task and context, not an imagined voice or guarantee.
- **Read the literal completion of every distractor.** Shared "different framing" feedback can hide a changed grammatical
  role: 魚が食べません makes the fish the eater, not the food. Explain the role change in that exact predicate pattern;
  do not replace the template with an equally broad ban on all object/time が constructions (ASTRA-TOPIC-O01 / WGM-OPUS-F2).
  For interpretation labels, reject the actual wrong reading rather than affirmatively defining it: the noun-description
  review found four wrong-scope rationales that sounded like validation of the selected analysis
  ([record](docs/grammar-n5-descriptions-sources.json), IND-DESC-002; regroup).
  The clean [giving/receiving review](docs/grammar-n5-giving-sources.json) illustrates the same check:
  keep actual giver/receiver, grammatical frame and adopted viewpoint separate. A different grammatical viewpoint
  can fall outside a requested framing without reversing roles or establishing a fixed family/person prohibition.
- **Close the opening question with a matched example.** An explanation of identification with a motion verb can be
  correct yet leave a promised occupation-predicate comparison implicit. Show the actual opening pair in contrasting
  contexts, without converting a contextual tendency into an absolute restriction (WGM-OPUS-F1).
- **Separate response-label definitions from grammatical terminology.** A task can be correctly graded under its visible
  operational definition while using a familiar technical term too narrowly. Here 相違, with its reading and definition,
  names different stated outcomes without redefining every contrastive use of は. Calibrate the original concern as
  terminology polish rather than an invalid answer key (WGM-OPUS-F3).

The [basic-particle exercise review](docs/grammar-basic-particles-sources.json) adds three observed checks:

- **A requested language is not necessarily only a means phrase.** 日本語を話します fits a broad language-use request
  beside 日本語で話します. Read the complete predicate and visible task; do not transfer that を alternative to
  英語で手紙を書きます, where 手紙を already supplies the object (BPI-F01).
- **Separate the register axes before excluding an answer.** Plain/polite does not decide neutral/rough, and a request
  for a polite form does not by itself exclude heightened-polite self-presentation. Bound an ordinary-ending drill
  before answering rather than treating a marked but valid form as ungrammatical (BPI-F03 / BPI-L01).
  Recheck that choice after combining a base with the taught particles: the unrestricted person-phrase tasks also
  allow respectful どなたかに／どなたにも／どなたかと／どなたとも, not only bare どなた in a question
  ([pointing/questions review](docs/grammar-n5-pointing-sources.json), N5PQ-F03; regroup).
  Apply a short/expanded copula restriction to the requested tense: an expressly nonpast-only exclusion
  did not rule out the plain past であった in two reason drills
  ([record](docs/grammar-n5-reasons-sources.json), N5RC-F01; regroup).
  Conversational contractions can retain polite endings: the result-state review accepted 開いてます and
  開けときます without creating new targets. Its noun-result となりました alternatives likewise retain ordinary
  polite grammar despite a more formal presentation ([record](docs/grammar-transitivity-results-sources.json), TR-02/03).
- **Normalization is not recognition of every spelling.** NFKC folds ３時 to 3時 but does not convert it to 三時 or
  迄 to まで. Grammar tasks should accept appropriate recognized spellings without promoting them to separate
  semantic choice buttons or claiming equal frequency (BPI-F02).
  Include accepted optional wording in that check, not just the model: どなた／何方 and どう／如何 were the
  omitted pairs in the pointing/questions review (N5PQ-F02; regroup).
  Check a supplied word across parallel grammar frames too: the wants/plans review found missing same-sense
  ゆく／往く realizations in four desire, intention and purpose tasks. A default reading in parentheses is
  not an explicit pronunciation-only restriction; verify lexical sense and preserve the teaching defaults
  ([record](docs/grammar-n5-wants-sources.json), IND-WANTS-001; regroup).
  This also applies to adjectives inside meaning-focused tasks: the comparison review found omitted
  さぶい realizations of 寒い in the current-state and transition answer lists
  ([record](docs/grammar-n5-comparisons-sources.json), IND-COMP-001; regroup).
  Check mixed-script spellings too, not just the model kanji and an all-kana rendering:
  the desire review found six missing 手つだって... realizations across three help tasks
  ([record](docs/grammar-desire-sources.json), IND-DESIRE-001; regroup).

These are checks for observed failure modes, not a requirement to invent a finding in every review. The batch record
preserves original severities, adjudication and reconciliation separately; agreement is not a substitute for evidence.

The [restriction/inclusion review](docs/grammar-restriction-sources.json) adds three concrete lessons:

- **Propagate a scenario change through every feedback path.** Changing a factual arrival to ability requires checking
  distractor rationales and shared explanations, not just the prompt and correct-answer explanation (RII-F01/O02).
  Check every branch of a shared formation template too: a correct statement answer must not receive an explanation
  of “the requested question.” Tie person-question distractors to the printed case role, and interpretation feedback
  to its own example rather than a paired scenario (N5PQ-F01/O02; regroup).
  Recheck every stage branch too: four result-state distractors incorrectly said an action was explicitly not yet
  performed in already-done or cause-unknown scenes (TR-04). A shared auxiliary label does not share a scenario's facts.
- **An explanation is not an assessed distinction.** Conditional feedback already separated sufficiency from necessity,
  but the options only contrasted a condition with an occurred surprise. Offering the exclusive-route alternative
  makes that inference part of the actual recognition task (RII-O03).
- **Count transfer opportunities separately from templates.** Two new bounded existence/cash situations add useful
  practice without claiming that 50 items measure 50 independent decisions or demonstrated mastery (RII-O01).

The [compound-relation review](docs/grammar-compound-relations-sources.json) adds three observed checks:

- **Audit instruction ordering as well as answer buttons.** A shuffled quiz still leaks its answer when every
  learner-facing definition list places the correct label first. Check the whole comparable task family, including
  unchanged instructions, and keep ordering independent of the answer (CR-F01).
- **Distinguish a new exercise from a new scenario.** Different target families or answer spans can reuse the same
  underlying conversation or event. Align genuinely paired context keys without equating their grammar or counting
  keys as independent discourse breadth (CR-O01).
- **Name the operation in a scaffolded drill.** A named pattern can support a useful attachment or form conversion;
  printing its exact missing fragment mostly supports copying. Preserve fair visible restrictions while requiring
  a small operation, and do not describe the result as unrestricted mastery (CR-O02).
  The [N5 foundations review](docs/grammar-n5-foundations-sources.json) extends this to prerequisite explanations:
  defining a ます-stem from an already-inflected example does not teach the productive godan u-row to i-row
  operation needed to form it from a dictionary verb (N5FI-F01; regroup).
  The [desire review](docs/grammar-desire-sources.json) found two selection instructions prescribing the exact
  missing ほしい and five role questions naming the requested participant in English (IND-DESIRE-002; regroup).
  Present candidates symmetrically and leave the tested role to be interpreted. If omission genuinely needs
  disambiguation, make the reference explicit in Japanese or ask a different role; do not simply delete necessary context.

The [N5 foundations review](docs/grammar-n5-foundations-sources.json) adds one response-support check:

- **Make interpretation labels enterable before answering.** Supply kana readings as well as meanings for every
  unfamiliar Japanese response label in the question-side instructions, retaining answer-independent ordering.
  Kana strings hidden in `acceptedAnswers` do not help a learner enter the label using an ordinary IME
  (N5FI-F02; add). This supports the response interface without revealing which interpretation is correct.

The same review's 迄／奇麗 omissions reinforce the existing spelling-recognition lesson (N5FI-F03); no duplicate
rule is added. Its practice-description and local-gloss refinements apply the existing transfer-accounting and
context-specific-vocabulary guidance rather than introducing new process.

The [noun-description review](docs/grammar-n5-descriptions-sources.json) adds one supplied-morphology check:

- **Check the supplied inflection, not only the blank.** A sound-changed plain-past base such as 焼い in 焼いた
  cannot be reused before ました: the polite form is 焼きました. Review the whole supplied predicate and its
  displayed-form reading when adapting a paired example. Exact span/hash checks can faithfully match a malformed
  verb; they do not establish its grammatical correctness (IND-DESC-001; add).

## のに article and initial exercises (2026-10-21)

**Snapshot:** `0045656b1e7a6dc55c73ae03f909c840e0eaed84` plus the local additions:
`articles/noni-and-concessive-contrasts.md`, SHA-256
`d3b44a090d9cd7ea622ef405d977aede3e2d0d11a51d29a50cc490f7f886426b`;
`grammar/noni-contrasts.json`, SHA-256
`30ae8194d44bc3eceef59d18453c6b1865248559bf3187261dadc2e71ea26fcd`.
The vocabulary inventory is pinned at
`7524052e91bcdf1378a42d35fa42ec7fe4cbdeb4156749ee766b72d00779e8a2`.

**Scope:** direct author review by `gpt-6-astra` of the complete article, all 26 exercises, 56 accepted renderings,
58 displayed options/rationales, four introduction groups, 182 lexical spans and 218 exclusions. The pass inspected
metadata and relevant meaning passages for all 73 linked canonical word identities.
The [source record](docs/grammar-noni-sources.json) identifies actual inspected source sections and qualifications.
**Verdicts:** article and exercises each correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**.

| Authoring finding | Disposition |
| --- | --- |
| A whole-sentence meaning label could fit both a concession and a stated duration | Resolved: ask about the role of the single quoted のに, not every fact the sentence states. |
| Meaning-label typing requires readings for unfamiliar labels | Resolved: show all three Japanese labels, kana readings and English meanings before answering. |
| Two proposed canonical word targets did not exist | Resolved: retain local glosses for すぐ and 何も rather than fabricate links. |
| An initial lexical span included the topic particle in 今回は | Resolved: separate 今回 from function-particle は. |

**Coverage:** eight standard-ending relationship/attachment tasks, six meaning-label questions, six shared
のに／わりに／くせに contrasts and six compositions around supplied はず／つもり. Thus 20 are connector-completion
tasks and six are interpretation tasks, not 26 independent production tests. Six shared-answer questions do not
independently discriminate every accepted connector. All new prompts have vocabulary support; the total is 90/487,
with the original 397 pending and the inventory still `pilot`.

**Integration:** zero content errors, 148 grammar regression tests, and one actual Android importer/cache-roundtrip
test executed with zero skipped/failures/errors. Manifest `95f98270e9418a5a` has 5,106 payloads and rebuilds deterministically.
All 34 preceding grammar files and all 461 preceding complete vocabulary records are preserved; the complete-stage gate
still rejects precisely the same 397 pending records. The two existing articles have navigation-only crosslinks:
removing the exact added bytes reproduces their baseline files, including their original line endings.
Earlier review hashes/verdicts remain historical rather than being reassigned to the newly linked article.

**Optional:** independent practice for ても and sentence-final のに, fuller register/context coverage, and the deferred
multi-correct option interaction in [Android #47](https://github.com/stop-cran/kanji-cards-android/issues/47).
Concrete representation and ambiguity notes were [added to that issue](https://github.com/stop-cran/kanji-cards-android/issues/47#issuecomment-6311563327);
this pass makes no app/schema change.
**Limits:** direct author review, not independent review, native-speaker certification, exhaustive paraphrase coverage,
new JLPT labeling, physical-phone verification or measured learning efficacy.

## Independent のに review and replacement reconciliation (2026-10-21)

**Snapshots:** the initial independent review covered exercise SHA-256
`30ae8194d44bc3eceef59d18453c6b1865248559bf3187261dadc2e71ea26fcd`.
The replacement snapshot is
`884317df71b85d136fefbaad8f160e25e75c1e9ddbd6b147dc8e9508a7003c1b`,
with vocabulary inventory
`27fe299a5b9a5e6ac2736b2bf9e4922a94ba382577c40f33769653e6b53e4a8d`.
The article remains byte-identical to the snapshot above. The
[source record](docs/grammar-noni-sources.json) preserves the distinct review stages.

**Initial independent review:** one fresh-context reviewer inspected the full article, all 26 exercises,
56 accepted renderings, 58 options/rationales, 182 lexical spans, 218 exclusions, 73 canonical identities and four groups.
The article was **CLEAN** on all three facets. Exercise correctness was **UNVERIFIED** solely for NONI-U01;
scoped coverage and comprehensibility were **CLEAN**, with no confirmed linguistic defects.
The actual reviewer model ID was not exposed.

| Item | Disposition |
| --- | --- |
| NONI-U01: the claimed outcome-open interpretation of causal past はずだったので in `noni-rain-preparation` could not be independently settled | Resolved in active content by retiring that unpublished card and replacing it with `noni-train-arrival-preparation`. The old interpretation remains unverified, not declared correct or incorrect. |

The replacement uses a current timetable-based expectation:
**時刻表では、電車はあと五分で来るはずなので、切符を用意して待っています。**
It retains the causal-preparation role but has a new exercise ID and example key. The visible task requests
なのに or なので; the expected arrival explains the preparation rather than contradicting it.

**Bounded reconciliation:** the original synchronous reviewer could not receive follow-up messages, so a fresh replacement
reviewer inspected the entire new card, both completed alternatives, all eight lexical spans/eight exclusions,
five canonical cards, dependent metadata, exact diffs and preservation. Its actual model ID was not exposed.
**Verdicts:** correctness **CLEAN**, scoped coverage **CLEAN**, comprehensibility **CLEAN**; no residual findings.
The article and 25 unchanged exercises retain their original independent coverage. This is a reconciled verdict for the
current batch, not a second full linguistic review or retrospective validation of the retired interpretation.

**Preservation and integration:** all 25 other のに exercises, all 486 other complete inventory records and all 34 preceding
grammar files remain unchanged. Counts remain 26 exercises, 56 accepted renderings and four groups.
Current vocabulary support is 182 lexical spans, 93 linked occurrences across 71 canonical identities, 89 local-only spans
and 217 exclusions; total coverage remains 90/487, `pilot`, with the same 397 pending records.
Content validation reports zero errors; 148 focused tests pass. One real Android import/cache-roundtrip test ran with
zero skipped/failures/errors. Manifest `6c6aea54806f0a43` rebuilds deterministically; only the のに grammar payload changed
relative to the initial のに manifest.

**Optional:** none from the reconciliation.
**Limits:** bounded linguistic review, not native-speaker certification, exhaustive paraphrase coverage or a physical-phone
check. The runtime integration evidence is separate from the reviewer's linguistic verdict.

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