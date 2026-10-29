# Independent initial review — N3 corrective finalization

## Snapshot

- Reviewed on **2026-10-29**. Reviewer: independent Copilot review; **actual model unknown**.
- Content baseline: `f4242f21d7722b06e4f697c4a2cb72f2ec5ab06d`.
- Frozen candidate: **`33988dec4053bdf7`**, including all 12 files listed in `review-candidate.json`, including the untracked `docs\counter-n3-finalization.json`.
- Every frozen file's raw SHA-256 matched that inventory and the working file at inspection. The six changed runtime article/counter/Grammar/curriculum entries also matched their LF-normalized manifest hashes. These are different hash conventions, not a discrepancy.
- App baseline: `3f8f8e87dffb1df75751c20880ef17f22f1ff37d`, plus only the new hotel-booking regression in `app\src\test\java\io\github\stopcran\kanji\core\RealContentTest.kt`.
- Reviewed app test raw SHA-256: `4f019673d77a6899e435afc8d071794564e78f6148cf3019456184eb72ef2188`; LF-normalized SHA-256: `90d717e325fe5b4029d22faf4946b3f8e4fb6445fc8b181b98cf10d504a829c9`.
- This is the **initial report**, to be retained unchanged for later reconciliation. It is not a release or native-acceptance receipt.

## Scope

Reviewed the complete changed booking and room records; both new Grammar tasks, including every prompt, instruction, accepted answer, option and rationale, explanation and lexical hint; their group/chapter placement; all added learner-guide passages; and current finalization, source, vocabulary and curriculum metadata. Checked preservation through complete-object comparisons, not identity counts alone.

Read the relevant production grading and navigation code, including `GrammarHome.kt`, `GrammarBrowser.kt`, `strings.xml`, `GrammarPracticeScreen.kt`, `GrammarScope.kt`, `Counters.kt`, `CounterExpressions.kt` and the counter answer transition. Inspected the actual public sources below independently. No other review report was used as evidence for these conclusions. The candidate's author rubric was visible in the required metadata; the estimates below are independently reasoned, not a comparison-based endorsement.

Excluded the specified cache files and app issue JSON files. No repository files were modified, builds/tests/native checks run, GitHub changes made, or subagents launched.

## Verdicts

**CLEAN** means no actionable defect established in this bounded text/static review, not exhaustive linguistic correctness or demonstrated learning effectiveness.

| Reviewed component | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `articles\numbers-and-counters.md`, changed discovery, room-reading, interval and reference passages | CLEAN | CLEAN | CLEAN |
| `articles\quantity-ranges-and-frequency.md`, new section 13, practice-scope guidance and references | CLEAN | CLEAN | CLEAN |
| Booking alias correction and complete affected card | CLEAN | CLEAN | CLEAN |
| Three-room expression and finite reading scope | CLEAN | CLEAN | CLEAN |
| Both new interval interpretation exercises and four lexical spans | CLEAN | CLEAN | CLEAN |
| Added group/chapter membership and current contributor metadata | CLEAN | CLEAN | CLEAN |
| New `RealContentTest` regression, static inspection only | CLEAN | CLEAN | CLEAN |

## Findings

**No high-confidence actionable defect found. No corrective patch is requested.**

The room disposition below distinguishes a supported finite teaching scope from unverified additional pronunciations; it is not a finding that every unlisted pronunciation is invalid.

## Room U1 disposition

**Recommendation: resolve U1 for the revised finite exercise, not for an exhaustive pronunciation claim.** The current model and accepted pair are fair on the inspected evidence. No consequential ordinary-answer false negative was established.

Locations: `counters\roomcounts.json:47–60`; `articles\numbers-and-counters.md:571–578`; `docs\counter-n3-finalization.json:23–46`.

Reasoning:

1. The JapanesePod101 **actual teacher transcript** discusses allocating separate karaoke rooms, then explicitly teaches `三部屋（さんへや）` and considers `みへや` as an alternative. This is positive evidence about ordinary room counting in a closely matching allocation situation, not merely an isolated word-list omission. The teachers' preference is teaching commentary, not a measured frequency result.
2. The actual にほんごべや table independently supplies `さんへや`; the actual Benricho room row supplies `みへや・さんへや`. Both also support the guide's neighboring counts. I did not generate readings by combining numeral and voicing variants.
3. The exercise explicitly asks for a count **using 部屋**, not a hotel identifier or a free choice among room counters. Its written answers `三部屋` and `3部屋` implement that operation. Sanabo's ordinary room-counting entry also makes clear why hotel `室` is a possible unit elsewhere without making it a missing answer to this specifically cued 部屋 task.
4. The revised explanation teaches both accepted full readings and warns against mechanical voicing. It does not assert that `さんべや` is linguistically impossible. The displayed canonical reading is now positively supported.
5. I independently checked the exact Yahoo `三部屋`/`さんべや` lead. Its results point to Mazii examples under room-partition verbs. The followed Mazii URL returned generic application HTML rather than an inspected dictionary passage. This is **unverified evidence**, not proof of an ordinary pronunciation and not proof of an error in Mazii. The bounded `三部屋`/`みべや` search produced no relevant exact result; that absence is not linguistic evidence.

The decision is therefore based on the positive, contextually applicable teacher discussion plus the corroborating full-form references, **not** on treating a table as exhaustive or search failure as a prohibition. The unresolved status of those voiced alternatives does not by itself establish a consequential rejected ordinary answer. Their general validity, distribution and applicability to this prompt remain **UNVERIFIED**. If an inspectable, reliable source subsequently establishes an ordinary alternative here, the minimal response is to add that complete reading to `readingAnswers` and explain it; do not manufacture a cross-product of voiced forms.

Confidence: **high** in the model and accepted pair; **moderate** in the finite-scope adjudication, which is not an exhaustive dialect/frequency judgment. This recommendation does not independently accept all historical C5 content or any native/release gate.

## Complete-task observations

### Booking and regression

`counters\casesken.json:58–96`: the scenario counts one reservation for three travelers. The complete written set remains `件`, `一件`, `つ`, `一つ`, `個`, `一個`, `組`, `一組`; the retained kana set is `いっけん`, `けん`, `ひとつ`, `こ`, `いっこ`, `くみ`, `ひとくみ`. Canonical Read remains `いっけん`. The three distractors `軒`, `頭`, `冊` do not supply a fitting count in this scenario.

IMABI's actual 組み discussion distinguishes numerical class labels from native one/two set counts. Removing contextual `いちくみ`, while keeping `ひとくみ`, is justified. The complete `kumiexpressions.json` object is unchanged, including the legitimate Class 1 `いちくみ`.

`RealContentTest.kt:30–41` directly exercises the production grader: removed alias Wrong, retained group reading Yellow, and the specified written forms Good. It would fail against the previous alias list. Production `Counters.kt:139–152` and `CounterQuizViewModel.kt:177–199` retain the existing Yellow/Hard behavior; the patch does not change SRS semantics. This is static review, not a claim that the test was executed.

### Return visit

`grammar\quantity-scope.json:3149–3204`: the full supplied sentence is natural. `三年ぶりに` describes recurrence after the elapsed interval; the proposed three-year stay is not established. The visible instructions explicitly define **1** and **2**, so the complete authored typed set **["1"]** is fair: a Japanese paraphrase or written-out numeral is not the requested operation. The correct button and both rationale branches agree with that mapping. Answer-side feedback supplies the full translation and distinguishes interval, visit duration and calendar date without claiming an exact anniversary.

The lexical spans are correctly bounded and sensed: `この`/この, “this”; `町`/まち, “town”; `訪れました`/おとずれました, headword 訪れる, “visited.” They do not translate the assessed `三年ぶり` phrase or reveal the answer label.

### Recurring rain

`grammar\quantity-scope.json:3205–3242`: `二か月ぶりの雨です` naturally describes rain returning after the gap. It is neither two months of continuous rain nor a forecast of the new rain's duration. The instructions deliberately reverse the numeric mapping: the complete typed set **["2"]** and both option rationales are consistent. `ぶりの` correctly modifies 雨; `雨`/あめ, “rain,” is a safe, correctly bounded lexical hint.

### Group and coverage

`grammar\quantity-scope.json:3732–3755` adds one coherent supplied-message interpretation facet with two contexts and no new gate/recommendation. A return visit with adverbial `ぶりに` and recurring weather with noun-modifying `ぶりの` differ in event type and attachment, not just noun or numeral. They support the stated narrow two-context claim, not independent proof of broad transfer or mastery.

The required interval interpretation has **not** been silently discarded or replaced by cued expression production. Two supplemental interpretations now perform it. The original two counter-form drills remain separate, and the 22 older numerical interpretations remain unclassified.

## Independent rubric estimates

Order: **[lexicalLoad, decisionLoad, calculation, answerAmbiguity, feedback]**, using `docs\counter-n3.md:241–255`. These are editorial estimates; feedback measures completeness, not difficulty.

| Exercise | Estimate | Independent rationale |
| --- | --- | --- |
| `quantity-scope-return-after-gap` | **[0, 1, 0, 0, 2]** | The potentially less familiar 訪れる is safely glossed/read; one supplied report requires distinguishing interval from stay duration; no calculation; explicit numeric response contract; feedback explains both timelines and the inference limit. |
| `quantity-scope-rain-after-gap` | **[0, 1, 0, 0, 2]** | Familiar/supported rain vocabulary; one interval-versus-continuous-duration decision; no calculation; explicit reversed numeric mapping is unambiguous; feedback explains the noun modification and both interpretations. |

Neither task requires the integrated multi-fact reasoning of decision-load 2. A two-option interpretation is useful bounded practice, not evidence of unaided production.

## Classification and learner navigation

- The inspected Bunpro page's **actual HTML title** is `ぶりに (JLPT N2) | Bunpro`; its body treats the temporal lapse sense and noun-modifying `ぶりの`. Nonbiri and Edew actually teach that same sense at **N3**. The classification is an exact-sense N2 mapping under `docs\jlpt-levels.md:123–189`, especially the primary-source disagreement rule at 179–183, not absence of N3 evidence or a vocabulary-derived level.
- The conditional earlier N2 fallback is not transformed into unconditional owner approval. Current metadata accurately describes applying the existing policy under the current finalization instruction. The new N2 companion retains the original interval operation without reclassifying the old unclassified set.
- The new guide section correctly explains attachment, recurrence versus duration, nonintentional weather, and the possibility of a subjectively long short interval. The stay comparison, selective readings and translations are sufficient for this scope.
- `GrammarHome.kt:115–144` separates **New grammar** from browsing and states the started-review exception. `GrammarBrowser.kt:114–158,215–221` connects the root Article sets choice and browse controls to the corresponding preferences. `strings.xml:62–84,92–104,223–225,264` contains **Filters and next topic**, **Article sets**, and the explicit scope-exception wording.
- The exact set title is **Quantity, ranges, frequency and scope**. `curriculum\grammar.json:88–125` maps all the relevant groups, including the new one, to **Focus, inclusion and quantity**.
- `GrammarPracticeScreen.kt:41–83` actually presents out-of-scope counts and explicit session-only inclusion consent. `GrammarScope.kt:7–23,42–47` distinguishes exact browse levels from cumulative new scope and retains started reviews. Thus All/Unclassified discovery, separate New grammar intake, All/N2 discovery for the supplement, and reviews outside new scope are accurately described. Browsing does not narrow a topic's full targeted membership.

## Preservation and metadata checks

Read-only comparisons produced:

- All provided baseline snapshots match the stated content HEAD after LF normalization.
- **50/50** old `quantity-scope` exercise objects and **9/9** old local introduction-group objects retained exactly, including nested answers, vocabulary, memberships, facets and links. Only two exercises and one group are appended. No other Grammar file has a tracked diff against the supplied HEAD.
- Candidate local classification totals: **26 N4, 2 N5, 22 unclassified, 2 N2**. All 22 unclassified objects, not just their IDs/levels, are unchanged.
- **2,429/2,429** previous vocabulary inventory records retained exactly; two added records produce 2,431. New prompt, context and vocabulary hashes independently recompute correctly. The four lexical spans plus exclusions form exact, nonoverlapping full-prompt partitions; grammatical targets remain protected.
- All previous chapter objects and ordered memberships are unchanged after removing the single appended new group. All previous curriculum-ledger top-level values are preserved.
- Source-wide structure: **286 → 287** authored groups; **23** hard leaf edges, **247** recommendations and **9** derived chapter edges remain exactly the same. All old group objects/ownerships survive. **292** unowned compatibility exercises remain unchanged, with zero authored unmapped groups. Both leaf and collapsed chapter graphs are acyclic; no edge is incident to the new group.
- The original contract's **54 counter files** also match commit `b697a3d65a4edf893b04eea33d2356cd600e87c9` after LF normalization. In the two corrective files, the other cards/expressions and all nonidentified fields remain unchanged; room sources are additive.
- The current source row still distinguishes draft evidence from accepted evidence. Finalization metadata explicitly leaves independent/native/publication acceptance pending and physical/learning trials unperformed. The project-accounting increment of two identities is consistent: 255 → 257 new project identities and 259 → 261 scoped identities, not an N3 Grammar classification count.

These are structural/static checks, not an importer run, test-suite pass or native acceptance.

## Actual sources inspected

1. [JapanesePod101 teacher transcript](https://www.japanesepod101.com/lesson/lower-intermediate-lesson-s3-14-box-karaoke-for-one-part-3-do-you-mind), room-allocation dialogue and subsequent counter discussion.
2. [にほんごべや counter table](https://learning-japanese.com/number-count/), actual 部屋 section, including neighboring counts.
3. [Benricho pronunciation table](https://www.benricho.org/kazu/kids/hatsuon.html), actual 部屋 row and its general representative-example qualification; unrelated table rows are not endorsed.
4. [Sanabo 部屋](https://www.sanabo.com/kazoekata/ct_ha/he/heya/), counted units and contextual distinctions; not evidence for the three-room pronunciation.
5. [IMABI Counters V](https://imabi.org/counters-v/), actual “The Counter ～組み” section, table and accompanying class/set restrictions.
6. [Bunpro ぶりに](https://bunpro.jp/grammar_points/%E3%81%B6%E3%82%8A%E3%81%AB), actual temporal-sense explanation and raw page title.
7. [Nonbiri ぶりだ／ぶりに／ぶりの](https://mainichi-nonbiri.com/grammar/n3-burida/), N3 identification, attachment and subjective interval explanation.
8. [Edew ぶり①（期間）](https://www.edewakaru.com/archives/13969183.html), actual N3 heading and gap/recurrence explanation, including rain and noun-modifying examples.

Yahoo/Mazii were checked only as unresolved leads, not counted as inspected dictionary evidence.

## Optional

None. No speculative alias additions, new production code, expanded source hunt or additional exercise quota is recommended.

## Limits

- General validity/frequency of `さんべや` and `みべや` remains unverified; the finite-scope adjudication above does not declare either impossible.
- Historical signed-release/public-sync and earlier packet-acceptance statements were not replayed or independently certified here. They are explicitly separated from the present candidate's pending acceptance.
- No production importer, Gradle build/test, emulator/AppNav/lifecycle check, physical-device check, audio/native-speaker approval, owner learning trial, or immutable publication was performed or asserted.
- This initial report covers the frozen candidate only. Any subsequent revision requires reconciliation against this unchanged report.
