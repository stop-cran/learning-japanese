# Learning Japanese

English-language notes on Japanese grammar, vocabulary, and usage.

This repository starts as a collection of standalone articles prompted by specific questions. It is not yet a course or a systematic reference: topics can be connected and organized more formally as the collection grows.

## Articles

| Area | Article | Main question |
| --- | --- | --- |
| Grammar | [Koto, wake, and Japanese noun-based grammar](articles/koto-wake-and-formal-nouns.md) | How do こと and わけ differ, which common formal nouns and noun-based expressions are useful to know, and where do の/ん and ほど fit? |
| Grammar | [Japanese verb extensions: direction and aspect](articles/verb-extensions-direction-and-aspect.md) | How do ～ていく, ～てくる, ～ておく, ～込む, and related constructions express direction, continuation, and completion? |
| Grammar | [Japanese conditionals: たら, ば, なら, と, and 場合](articles/japanese-conditionals.md) | How do conditions, premises, event order, discoveries, and procedural cases differ, and when can several patterns fit? |
| Grammar | [のに: unexpected outcomes, comparisons, and the other のに](articles/noni-and-concessive-contrasts.md) | How do concessive のに, わりに and くせに overlap, and how is nominalizing の plus に different? |
| Grammar | [Japanese listing and examples: と, や, とか, など, たり, and し](articles/japanese-listing-and-examples.md) | How do named lists, representative examples, added reasons, and alternatives differ, and when is one stated item enough? |
| Vocabulary | [Strange, suspicious, and rare: ayashii and related words](articles/ayashii-and-related-words.md) | How do 怪しい, 妖しい, 疑わしい, いかがわしい, 変な, and 珍しい differ? |
| Vocabulary | [Kaeru: change, replace, exchange, and return](articles/kaeru-change-replace-and-return.md) | How do 変える, 替える, 換える, 代える, 帰る, 返る, 還る, and 孵る differ, and why is 交える not read かえる? |
| Vocabulary | [Japanese occupation and role endings](articles/occupation-and-role-endings.md) | What do 者, 家, 師, 士, 手, 員, and 屋 contribute, and how do they relate to prestige and new word formation? |
| Vocabulary | [Japanese onomatopoeia: 201 words](articles/japanese-onomatopoeia.md) | How do sound words and mimetic words describe everyday scenes, and which constructions go with them? |
| Vocabulary | [Onomatopoeia sound patterns](articles/onomatopoeia-sound-patterns.md) | What can repetition, endings, and voiced consonants suggest without becoming rigid meaning rules? |
| Vocabulary | [Warmth and texture](articles/onomatopoeia-texture-and-warmth.md) | How do ぽかぽか, ほかほか, ふわふわ, ふかふか, ぺたぺた, and べたべた differ? |
| Vocabulary | [Rain, rolling, walking, and similar forms](articles/onomatopoeia-sound-and-movement.md) | How do vivid scene descriptions differ, and why are similar-looking words not necessarily synonyms? |
| Vocabulary | [Eating and drinking](articles/onomatopoeia-eating-and-drinking.md) | How do gulps, chewing, appetite, texture, and flavor differ? |
| Vocabulary | [Body sensations and feelings](articles/onomatopoeia-body-and-feelings.md) | How do mimetics describe pain, excitement, disappointment, and attention without identifying their causes? |
| Vocabulary | [Motion, voices, and everyday sounds](articles/onomatopoeia-motion-and-sound.md) | Which descriptions concern movement, sound, result, or manner, and where do they overlap? |

## Confusable vocabulary

The [candidate inventory](docs/confusable-words.md) collects overlapping meanings, misleading English glosses,
similar forms, false friends, and other easy-to-conflate cases for future comparison articles. It is a working list with
provisional notation and links to existing material, not yet a complete usage reference or new app metadata.

## Kanji cards and words

Kanji cards, word articles and stroke data feed the [Ensō Nihongo Android app](https://github.com/stop-cran/kanji-cards-android). The
format is described in [docs/content-format.md](docs/content-format.md); data sources are in [NOTICE.md](NOTICE.md).

- `kanji/` – one card per kanji (985): meaning, radical, readings, common words, and origin notes or explicitly labelled modern-shape mnemonics.
  The deck covers all 79 N5, 166 N4, 367 N3 and 367 N2 kanji in the selected [kanjiapi.dev](https://kanjiapi.dev) community sets.
  It also includes 分 as a documented N5 exception and five N1 article-subject additions:
  80 N5, 166 N4, 367 N3, 367 N2 and five N1. The [N2 expansion](docs/n2-review.md) added 365 cards
  to the two existing N2 cards in twenty-four 15-card batches and a final five-card batch.
  All 25 batches have independent GPT/Claude review and reconciled reports, including changed-passage confirmations.
  These community level sets are not official JLPT kanji lists.
  The `starter` tag identifies the original 118-card cohort, not the later expansions.
- `words/` – one article per written word form (3,273): native words, Sino-Japanese compounds and loanwords, including kana-only spellings.
  Articles explain meaning, spelling or formation, synonyms, antonyms and usage distinctions.
  The selected community vocabulary list's 684 N5 and 640 additional N4 rows are covered by 1,308 articles:
  924 new articles and 384 reused ones. Multiple source readings can share an article.
  Its 1,730 additional N3 rows are covered by 1,698 articles: 1,490 new and 208 reused from the preceding collection.
  The level indexes overlap where an existing article teaches an additional reading or meaning.
  The [N2 vocabulary expansion](docs/n2-vocabulary-review.md) is in progress against 1,812 further
  source rows, with separate pending/draft/closed coverage and sequential independent GPT/Claude reviews.
- `strokes/` – generated stroke data. Validate with `python tools/validate.py`.
- `grammar/` – versioned, contrast-focused exercises for the app's Grammar section: the original 8-exercise pilot, an
  18-exercise foundations batch on nominalization and negative meanings, 12 exercises on ability, occurrence, decisions and
  outcomes, 9 on intended meaning, inference and normative judgment, 9 on ところ action stages, 6 on まま state contrasts,
  6 on before/after event order, 27 on time windows, periods and occasions, 24 on purposes, causes and alternatives,
  12 on evidence, cases and conditions, 12 on models, governing conditions and linked steps,
  12 on comparison, addition and advice, 15 on expectations and eventual outcomes,
  12 on characteristic patterns, recollections and reasons, 15 on particle neighbors,
  12 on degree, comparison and desired extent, 12 on plans and believed completion,
  12 on よう comparisons, examples and desired outcomes,
  12 on きり limits, estimates, last events and recurring follow-ups,
  12 on よう changes in ability or habit and positive/negative practices,
  12 on つもり self-assessment versus intended changes,
  12 on negative plans and present/past intention denial,
  12 on retained versus changed noun/adjective states,
  12 on ほか exclusions and no other option versus no need,
  12 on past はず expectations, event time and actual outcomes,
  12 on possible versus desired extent with かぎり／だけ,
  12 on くらい degree/minimum versus のに counterexpectations,
  12 mixed-context questions on changed routines, maintained practices and current inferences,
  12 on recent completion, retained states and inferences about past actions,
  12 on current intentions, no need and no available alternative,
  12 on earlier intentions, completion beliefs and current inferences,
  12 on norms, predictions and goal-relative practical necessity,
  60 on たら／ば／なら／と／場合 conditionals in two batches, 26 on のに and related contrasts,
  and 36 on listing, examples and addition (523 in total).
  Time practice includes うち, あいだ, とき, ころ, たび and shared とき／おり／さい occasion answers;
  shared alternatives are not independently contrasted targets.
  Purpose/cause practice adds ため, おかげ, せい, かわり and ついで, including compensating trade-offs.
  Condition practice covers かぎり evidence limits and positive/negative conditions, plus ばあい procedural cases.
  Relational practice covers とおり／どおり, もと, and additive versus preliminary-step うえ.
  Comparison/advice practice adds ほう and additive ほか, including recommendations to do or not do something.
  Expectation/outcome practice adds わり and くせに, plus six shared すえ／あげく answers contrasted with additive うえ.
  The shared outcome items show three model options per noun, not independent discrimination between the two nouns.
  The もの batch practices general patterns and past recollections, plus casual もの／もん reasons versus わけだ conclusions.
  Particle practice groups six shared approximate quantities with ほど／くらい／ぐらい／ばかり, adds three constrained だけ
  limits, and contrasts three activity-concentration with three recent-completion ばかり items.
  The six shared quantity items are not independently discriminated particle targets.
  Degree/extent practice adds three each for a stated ほど degree, a below-standard comparison, correlated change with
  VばVるほど, and a desired amount with Vたいだけ. It uses controlled adjective forms and explicitly named whole patterns.
  Plan practice adds three each for affirmative and negative つもり intentions, past intentions and past beliefs in
  completed actions. It preserves the difference between 送るつもりでした and 送ったつもりでした, including a fulfilled
  plan and a confirmed belief; not every past plan failed or every completion belief was mistaken.
  よう practice contrasts three adverbial comparisons with three direct noun modifiers, then three enabled-ability
  goals with three prevented-ability goals. Noun modifiers include two category examples and one figurative resemblance;
  they are not three independently tested examples of each meaning.
  Change/effort practice adds three newly possible actions and three new habits before supplied ようになりました,
  then three positive and three negative maintained practices before supplied ようにしています.
  These verb-form tasks do not independently test selecting なる versus する in unrestricted contexts.
  Self-assessment practice adds six matched つもり pairs, using two nouns, two な-adjectives and two い-adjectives.
  It distinguishes a current self-view from an intention to become something or change a quality, with つもりです supplied.
  Intention-denial practice groups three shared negative plans/denials against three affirmative future intentions,
  then contrasts three denied past intentions with three affirmed ones. It includes accidental actions, blocked intentions
  and a fulfilled plan; an outcome does not by itself establish whether it was intended.
  Noun/adjective state practice adds six matched まま／なる pairs, using two nouns and two adjectives of each class.
  It distinguishes persistence from a transition across the stated interval, including desirable retained states, deliberate
  changes and a past clean state that no longer holds; it does not claim that every detail stays unchanged.
  Exclusion practice contrasts three outside-group ほか answers with three shared within-group なか／うち answers,
  then three shared no-alternative ほか／しか answers with three no-need ことはない answers.
  It preserves the relevant group or goal, accepts fitting particle variants and distinguishes no need from prohibition.
  Past-expectation practice separates earlier forward expectations from current inferences about completed events,
  then affirmative from negative recalled expectations. It includes fulfilled and contradicted outcomes, preserving the
  explicit recollection contexts that avoid treating every はずだった as an automatically failed forecast.
  Possible-extent practice adds six shared potential＋かぎり／だけ answers against six たいだけ desired amounts.
  It separates the available and desired bounds using access, space, transport, supplies, service quotas and speaking time;
  three かぎり and three だけ model labels are not independently discriminated targets.
  The latest particle batch adds three shared くらい／ぐらい／ほど degree illustrations and three くらい／ぐらい basic
  minimums, each with three reciprocal のに counterexpectations. It includes noun-predicate な attachment, optional は
  for the selected minimums, speaker-relative ease and tone, and a favorable outcome despite an obstacle.
  The first mixed set blanks the whole ending and uses one common five-pattern pool throughout: ようになる／ようにする／
  ことにする／はずだ／ようだ. Four questions per function now include contextual なる-versus-する selection, with shared
  ことにしている and habitual ようにする practice alternatives, plus ようだ inferences. The English meaning remains visible, but no item-specific
  form instruction selects the function or conjugation for the learner.
  The next mixed set contrasts shared たところ／たばかり completion, retained たまま results and current はずだ／ようだ
  judgments about past actions. Matching few-second window contexts prevent elapsed time alone from selecting the account;
  deliberate states, lights remaining off and a coat drying in an unchanged position preserve the underlying distinctions.
  Mixed intention/necessity practice adds voluntary unnecessary plans, shared ことはない／必要 no-need answers and all
  fitting basic ほか／しか no-alternative endings. Requirements do not determine intentions, and alternatives are evaluated
  relative to the stated goal rather than every imaginable action.
  Mixed past-stance practice blanks the whole predicate and separates earlier intentions, earlier completion beliefs
  and current はずだ／ようだ inferences about past actions. Fulfilled/unfulfilled plans and supported/contradicted beliefs
  prevent outcome-based guessing; first-person inferences prevent pronouns from supplying the answer.
  Basic だった／であった and だ／である alternatives remain within one shared visible task.
  The final mixed set distinguishes normative べき／もの, predictive はず／よう and goal-relative ほか／しか.
  The same return/wait/contact/redo verbs recur across the three accounts, with complete predicate blanks that retain
  both 連絡するべき and 連絡すべき. Norms can be followed or violated, a prediction can align with a rule,
  and an optional goal can still have a necessary means. Shared equivalents remain one answer class per exercise.
  The first conditionals set adds four introduction groups: 10 named-form tasks, six prospective/completed なら premises,
  six positive/negative state conditions, and eight discoveries, counterfactuals and procedural cases.
  It accepts fitting alternatives within the visible task, rather than claiming unique five-way conditional selection.
  The second set adds five six-exercise groups: further verb/negative-predicate forms; preparation, event triggers and
  ongoing actions; mechanisms, past habits and state-based requests; planned/completed procedural cases; and imagined
  present identities. The original 30 remain unchanged. Across the 60 exercises, たら is accepted in 33, ば in 27,
  なら in 24, と in 14 and 場合 in 20; these overlapping counts measure supported forms, not independent discrimination.
  Nonhypothetical 私の場合, dedicated nominal なのなら practice and explicit necessary-versus-sufficient reasoning
  remain gaps in this dedicated comparison set. Conditional set expressions remain outside its basic scope.
  The のに follow-up adds eight relationship/attachment tasks, six explicit meaning-label questions, six overlapping
  のに／わりに／くせに contrasts and six はず／つもり compositions, in four introduction groups.
  It distinguishes concession from required time and tool use without judging by the spelling or tense alone.
  The six overlap tasks accept fitting alternatives together; they are not independent discrimination of every connector.
  The listing set has six groups of six: noun lists and single examples; たり formation; し/て attachment;
  examples versus variation and denial; inclusion, alternatives and suggestions; and added facts/reasons versus のに.
  It contains 24 completion tasks and 12 explicitly defined meaning-label tasks. Eight questions accept substantive
  alternatives together, with optional choose-any buttons; named-form drills state their restrictions before answering.
  All 60 conditional, 26 のに and 36 listing prompts include vocabulary hints; total author-reviewed coverage is **126/523**,
  with the original 397 still pending. The のに source record keeps author and independent review snapshots separate;
  the unsettled causal-past expectation card was retired in favor of a current timetable-based preparation example.
  See the [content format](docs/content-format.md#grammar-exercises), [foundations sources](docs/grammar-foundations-sources.json),
  [actions sources](docs/grammar-actions-sources.json), [intent sources](docs/grammar-intent-sources.json),
  [action-stage sources](docs/grammar-stages-sources.json), [state sources](docs/grammar-states-sources.json),
  [before/after sources](docs/grammar-before-after-sources.json),
  [time-expression sources](docs/grammar-time-sources.json), [cause/alternative sources](docs/grammar-causes-sources.json),
  [condition sources](docs/grammar-conditions-sources.json), [relation sources](docs/grammar-relations-sources.json),
  [comparison/advice sources](docs/grammar-comparisons-sources.json),
  [expectation/outcome sources](docs/grammar-expectations-sources.json),
  [pattern/recollection/reason sources](docs/grammar-mono-sources.json),
  [particle-neighbor sources](docs/grammar-particles-sources.json),
  [degree/extent sources](docs/grammar-degree-extent-sources.json),
  [plan/belief sources](docs/grammar-plans-sources.json),
  [よう sources](docs/grammar-you-sources.json),
  [change/effort sources](docs/grammar-you-change-effort-sources.json),
  [self-assessment sources](docs/grammar-self-assessment-sources.json),
  [intention-denial sources](docs/grammar-intention-denial-sources.json),
  [noun/adjective state sources](docs/grammar-state-change-sources.json),
  [exclusion/no-alternative sources](docs/grammar-hoka-exclusion-sources.json),
  [past-expectation sources](docs/grammar-past-expectation-sources.json),
  [possible-extent sources](docs/grammar-possible-extent-sources.json),
  [くらい degree/minimum sources](docs/grammar-kurai-degree-minimum-sources.json),
  [mixed-routine sources](docs/grammar-mixed-routines-sources.json),
  [mixed completion/state sources](docs/grammar-mixed-completion-state-sources.json),
  [mixed intention/necessity sources](docs/grammar-mixed-intention-necessity-sources.json),
  [mixed past-stance sources](docs/grammar-mixed-past-stance-sources.json) and
  [mixed norms/expectations sources](docs/grammar-mixed-norms-expectations-sources.json),
  plus the [initial conditionals sources and review](docs/grammar-conditionals-sources.json) and
  [second conditionals batch and combined coverage](docs/grammar-conditionals-contexts-sources.json), plus the
  [のに source and coverage record](docs/grammar-noni-sources.json) and
  [listing source and coverage record](docs/grammar-listing-sources.json).
  Every named formal-noun/particle family in the formal-nouns article now appears in practice, but this is not complete construction
  coverage. The five mixed sets complete the bounded formal-noun expansion planned in
  [Android #46](https://github.com/stop-cran/kanji-cards-android/issues/46); the app's remaining engineering, documentation
  and local-evidence acceptance is separate. Stated pools do not claim every construction or register, or unrestricted cloze.

The revised JLPT does not publish exhaustive kanji or vocabulary syllabi. Level coverage here means the exact named community set,
not a guarantee about every examination question or a complete beginner curriculum.
See the [level-source policy](docs/jlpt-levels.md) and the [N4](docs/n4-source-snapshot.json) and
[N3](docs/n3-source-snapshot.json) kanji source snapshots. The
[N5/N4 vocabulary snapshot](docs/n5-n4-vocabulary-snapshot.json) and
[source-row index](docs/n5-n4-vocabulary-sources.tsv) preserve the pinned list, spelling normalizations, corrected dictionary identities
and sense qualifications.
The separate [N3 vocabulary snapshot](docs/n3-vocabulary-snapshot.json) and
[source-row index](docs/n3-vocabulary-sources.tsv) extend that same pinned list and dictionary snapshot.
The [article-subject snapshot](docs/article-subjects-source-snapshot.json) records the six additional kanji,
17 new word cards, and reuse of 訳 for わけ, including dictionary-reading caveats and the 妖 level exception.
作家 is shared with the N3 vocabulary expansion, so merging these additions adds 16 distinct word cards to that collection.

Source-covered word articles carry their own `jlpt` metadata: 672 N5, 636 N4, 1,625 N3, three N2 and two N1 articles, independently of the kanji they contain.
This article-level label does not assign every subsidiary sense or reading to that level. The remaining 272 articles have no
sourced word-level label. In particular, the pinned list's N1 labels for くらい and だけ are not recommendations to postpone these basic particles.
Vocabulary-aware app versions use explicit levels first and retain kanji-based inference only when the
field is absent; older versions ignore word-level metadata. N4 study includes N5; N3 study includes both.
Known ambiguous word pairs are marked with [`quiz_exclusions`](docs/content-format.md#word-article);
these require an exclusion-aware app version and do not imply that every possible ambiguity has been identified.

## Onomatopoeia collection

The [201-word index](articles/japanese-onomatopoeia.md) preserves the first 100 and adds a
[second 100](articles/japanese-onomatopoeia.md#second-100-word-cards), grouped by everyday situation.
The second batch adds 97 cards and enriches three existing ones, plus three comparison guides.
Later additions are listed separately, beginning with [ぶかぶか / ブカブカ](words/ぶかぶか.md), for oversized clothing or shoes.
Cards carry the `onomatopoeia` tag, a broad category such as
`giongo`, `giseigo`, or `gitaigo`, and a form tag where applicable. Categories can overlap by sense;
these tags are not new word types or JLPT levels. Existing word IDs and sourced level labels are retained.

The app has an Onomatopoeia stack with the normal word quizzes. Eligible named scenes (`scenes/` and `images/`)
support both picture-to-word and word-to-picture quizzes; article-only scenes remain visible in the article.
The Onomatopoeia stack includes
tagged words independently of JLPT level; unlevelled words also remain in All rather than a numbered JLPT stack.
All 201 tagged words have scene catalogs, with 396 illustrations in total. The original 120 image files
are preserved; the latest addition is an oversized-coat scene for ぶかぶか.
See the [collection and source notes](docs/onomatopoeia.md).

### Generated images

The pictures in `images/` are AI-generated with Azure OpenAI from original scenes in
`tools/image_prompts.json` and `tools/onomatopoeia_scene_plan.json`, then compressed to 512 px WebP. Each illustrates one selected use, not
every sense or a guarantee of unique quiz choices. The original 20-image pilot has owner approval.
The new 100 received an assistant visual review and were **accepted by the owner for learning use
on 2026-10-19**; feedback from actual study remains to come.
The [named-scene provenance and per-picture observations](docs/onomatopoeia-scene-images.json) record
the actual model, output hashes, corrections and limitations. The images are text-free by design,
but generated art may still contain small inaccuracies. Earlier batch acceptance does not imply owner
approval of later additions. The original implementation is tracked in
[app issue #45](https://github.com/stop-cran/kanji-cards-android/issues/45).

## Approach

- Keep each article independently readable, with a short explanation of the central distinction.
- Write explanations in English; retain Japanese spellings and examples, with English translations.
- Distinguish useful learning shortcuts from strict grammatical or semantic rules.
- Note differences in register, context, and classification where they matter.
- Link to references for further study. Some source material is in Japanese even though the articles are in English.

The notes focus on practical understanding rather than exhaustive coverage. Examples illustrate particular uses; their translations are not intended as universal replacements for the Japanese expressions.

For contributors and reviewers, see the [writing and review guidance](.github/copilot-instructions.md) and [REVIEW.md](REVIEW.md).
