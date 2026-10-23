# Grammar authoring sources

Use this contributor guide to start a search, not as a whitelist that makes every claim on a site authoritative.
The sources below helped with earlier batches; their usefulness depends on the particular construction and claim.
Follow the [grammar exercise contract](content-format.md#grammar-exercises) and
[writing and review rules](../.github/copilot-instructions.md).

## Search order

1. Search the existing `docs/grammar-*-sources.json` records for the construction and its closest alternatives.
   Reuse their inspected URLs and read their scope and caveats before searching afresh.
2. Choose sources by the question: teaching references for whole patterns, dictionaries for exact senses and spellings,
   and contextual explanations for register or speaker intention. The table provides concrete starting pages.
3. Inspect the actual passage, including its publisher, heading, reading, sense or section, and examples.
   A search summary, guessed URL or successful fetch of the wrong entry is not evidence.
   Cross-check consequential restrictions and competing constructions; resolve disagreements by the exact claim, not a vote.
4. Author original scenarios and screen the full linked article inventory. Sources support patterns, not automatically the
   naturalness of a new sentence or completeness of its accepted answer set. Multiple valid completions are welcome:
   investigate their shared meaning and limits rather than force one wording. Follow the
   [answer-set, quiz-option and feedback rules](content-format.md#grammar-exercises), use visible form restrictions only
   for a clear learning goal, and retain editorial review. One correct quiz button does not mean only one acceptable typed answer.

For observed predicate-role, register, typed-spelling, matched-context and response-label pitfalls, see the
[reusable grammar-review lessons](../REVIEW.md#reusable-grammar-review-lessons).

## Reusing lexical annotations

A matching surface is a candidate, not proof of its word boundary or sense in a new sentence. Recheck affected
occurrences after extending a shared lexicon: the [N4 consolidation review](grammar-n4-consolidation-sources.json)
found that adding legitimate affirmative はい also produced false "yes" hints across **は + いない** in
職員はいない. Preserve the real dialogue response and repair the negative clauses by occurrence, not by banning
the spelling globally. Exact offsets, prompt hashes and complete character coverage can all pass for a false boundary.
Likewise, reused glosses must fit the current referent and sense, not just the same written word.

## Assigning exercise study levels

For JLPT metadata, follow the [grammar-level policy](jlpt-levels.md#grammar-baseline) and
[classification source record](grammar-jlpt-sources.json): Bunpro is primary, JLPT Sensei is secondary, and the exact
construction sense matters. A dictionary meaning, vocabulary-card level or optional advanced answer does not establish
an exercise's grammar level. These curriculum estimates are not an official JLPT grammar syllabus.

The 2026-10-22 classification pass established these reusable authoring checks:

- **Match the use, not just the spelling.** Separate past-experience from occasional-occurrence ことがある, the two のに
  constructions, and concentration, recent-completion and approximation ばかり. Ordinary additive も and number-plus-も
  also need distinct anchors; a particle's vocabulary-card level is not its grammar level.
- **Inspect both answer modes.** A substantive contrast in the base fixed choices may require harder grammar than the
  key alone. A required とか or 折 answer is not merely an optional typed alternative; conversely, optional すら or formal
  copulas do not automatically raise a task that can be answered without them. Do not take the hardest string anywhere
  in the record as the level.
- **Separate the elicited skill from its surroundings.** A supplied compound relation need not raise an explicit
  object-marker or noun-linking drill. Glossed interpretation labels are not vocabulary prerequisites. Keep natural
  examples and support unfamiliar words rather than rewriting the language to fit a level.
- **Record the strength of the mapping.** Distinguish an exact entry from an editorial semantic-family extension.
  Document primary/secondary disagreements and overlapping entries within one reference. When the primary lacks the
  relevant sense, cite an applicable secondary entry or leave the level absent; do not borrow a neighboring sense's label.
- **Keep relabeling separate from content revision.** Preserve prompts, translations, answers, vocabulary annotations,
  stable IDs and introduction metadata, then regenerate the manifest. Vocabulary context fingerprints exclude `jlpt`:
  level-only changes must not invalidate lexical reviews or turn pending coverage into reviewed coverage.

## Starting points by purpose

Links in the first column are previously inspected seed pages, not an exhaustive bibliography or a blanket endorsement.
The batch records contain the exact sections and qualifications used.

| Sources and inspected seed pages | Useful starting point for | Existing batch records |
| --- | --- | --- |
| [TUFS: intentions](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/066.html), [Bunpro: 予定](https://bunpro.jp/grammar_points/よていだ), [Japan Foundation: changed abilities and habits](https://www.kyozai.jpf.go.jp/kyozai/material/BTS00086/ja/render.do) | Volitional thought, verb/noun planning frames and changed routines. Inspect actual charts and examples; do not import fixed person/duration bans, a booking requirement, or potential-only attachment for habitual changes. | [Volition, plans and goals](grammar-plans-goals-sources.json) |
| [Tae Kim: embedded questions](https://guidetojapanese.org/learn/grammar/question), [IMABI: indirect questions](https://imabi.org/the-particle-ka-%e3%81%8b-iii-indirect-question/), [Bunpro: reported instructions](https://bunpro.jp/grammar_points/ようにいう) | Inner question versus outer message, bare-か polar questions, and participant roles within a stated clause scope. Inspect intact Japanese and alternative groupings; do not impose a universal だか ban, compulsory どうか, or a rule that every visible が identifies the outer requester. | [Embedded questions, reports and noticing](grammar-reports-questions-sources.json) |
| [Bunpro: とおもう](https://bunpro.jp/grammar_points/とおもう), [Tae Kim: possibility](https://guidetojapanese.org/learn/grammar/certainty), [IMABI: はず](https://imabi.org/planning-obligation/) | Thought time versus content time, nominal attachment, possible negative propositions, and negative expectation versus ruling out. Inspect intact Japanese examples and qualify conflicting shortcuts; do not import permanence/person bans, numerical certainty or a rule that all negative expectations require はずがない. | [Thinking, possibility and expectation](grammar-judgment-expectation-sources.json) |
| [Japan Foundation: そうだ／ようだ／らしい](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/201012.html), [IMABI: appearance-そう](https://imabi.org/seem-%ef%bd%9e%e3%81%9d%e3%81%86%e3%81%a0/), [Bunpro: みたい modifiers](https://bunpro.jp/grammar_points/みたいに-みたいな) | Appearance versus resemblance and inference, documented verbal-negative variation, and nonadjacent modification. Read the complete clause and actual source examples rather than importing a fixed confidence ladder, sight-only rule or next-word attachment shortcut. | [Looks, likeness and informed impressions](grammar-appearance-impressions-sources.json) |
| [Bunpro: causative](https://bunpro.jp/grammar_points/causative) / [causative-passive](https://bunpro.jp/grammar_points/causative-passive), [Tofugu: causatives](https://www.tofugu.com/japanese-grammar/verb-causative-form-saseru/), [Tae Kim: causative-passive forms](https://guidetojapanese.org/learn/grammar/causepass) | Causative-then-passive formation, lexical actor versus causer, contextual permission and common short pairs. Inspect actual Japanese examples; do not import a universal に／を permission switch, obligatory anger or a short-form rule for every verb class. | [Making, letting and being made to act](grammar-causative-perspective-sources.json) |
| [Bunpro: passive](https://bunpro.jp/grammar_points/Verb%5Bpassive%5D), [Tofugu: passive forms and frames](https://www.tofugu.com/japanese-grammar/verb-passive-form-rareru/) | Final ichidan inflection, actor versus target, retained objects and intransitive affected events. Separate illustrated frames from blanket negativity, control or agent-marker rules; a source's neighboring honorific explanation does not establish passive roles. | [Passive voice and affected participants](grammar-passive-participants-sources.json) |
| [Tofugu: ていく／てくる](https://www.tofugu.com/japanese-grammar/teiku-tekuru/), [IMABI: 始める／出す](https://imabi.org/start-to-%EF%BD%9E%E5%A7%8B%E3%82%81%E3%82%8B-%EF%BD%9E%E5%87%BA%E3%81%99-%EF%BD%9E%E3%81%8B%E3%81%91%E3%82%8B/), [Maggie Sensei: ばかり](https://maggiesensei.com/2013/07/02/%E3%81%B0%E3%81%8B%E3%82%8A-bakari/) | Adopted spatial/temporal viewpoints, productive versus lexical compounds, and subjective recency. Inspect past いった and future くる counterexamples, nonvolitional 始める and purposeful 出す, and the explicit week-prior ばかり example rather than importing a tense, intention or stopwatch shortcut. | [Direction, development and event stages](grammar-motion-stages-sources.json) |
| [Tae Kim: favors](https://guidetojapanese.org/learn/grammar/favors), [Wasabi: giving/receiving](https://wasabi-jpn.com/magazine/japanese-grammar/receiving-and-giving/), [Bunpro: indirect requests](https://bunpro.jp/grammar_points/てくれない-てもらえない) | Action performer versus beneficiary, adopted viewpoint, lexical participants and negation inside/outside a request. Do not turn social-circle diagrams into fixed family rules, もらう into coercion, or illustrative politeness scales into universal rankings. The batch records the actual overlapping N1/N4 てやる disagreement rather than dismissing the primary sense as unrelated. | [Benefactive actions and requests](grammar-benefactive-requests-sources.json) |
| [Bunpro: てみる](https://bunpro.jp/grammar_points/てみる) / [てしまう](https://bunpro.jp/grammar_points/てしまう-ちゃう), [Tofugu: ておく](https://www.tofugu.com/japanese-grammar/teoku/), [Tae Kim: trying](https://guidetojapanese.org/learn/grammar/try) | Trial versus maintained practice, preparation/retention, completion/outcome and conversational contractions. Trials can be repeated, completion need not be regretted, and preparing and retaining a state can overlap. Explicit expansion operations avoid pretending that a full form is forbidden in casual conversation. | [Trying, preparing and completing](grammar-try-prepare-complete-sources.json) |
| [Japan Foundation: てある／ている／ておく](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/pdf/NK51_16-17.pdf), [Bunpro: transitivity](https://bunpro.jp/grammar_points/transitive-intransitive-verbs) / [quality changes](https://bunpro.jp/grammar_points/にする-くする), [Maggie Sensei: となる／になる](https://maggiesensei.com/2010/12/10/%E3%81%A8%E3%81%AA%E3%82%8B-vs-%E3%81%AB%E3%81%AA%E3%82%8B%E3%80%80-to-naru-vs-ni-naru/) | Actor/object versus changed thing, purposeful results, が／を／は frames and qualified noun-result alternatives. Neither transitivity nor に／と is an intention/control detector; a prior action and its resulting state can have compatible descriptions. | [Actions, events and results](grammar-transitivity-results-sources.json) |
| [Bunpro: potential](https://bunpro.jp/grammar_points/Verb%5Bpotential%5D), [見える](https://bunpro.jp/grammar_points/見える), [聞こえる](https://bunpro.jp/grammar_points/聞こえる), [がする](https://bunpro.jp/grammar_points/がする) / [Wasabi: potential form](https://wasabi-jpn.com/magazine/japanese-grammar/japanese-potential-form/) | Potential morphology, ability/access and perception. Do not import an absolute attention test, a universal を ban or a claim that potential proves no action occurred. Supplied-predicate interpretation avoids forcing one translation of an underspecified “can see/hear.” | [Ability and perception](grammar-ability-perception-sources.json) |
| [Daijisen: にとって](https://www.weblio.jp/content/にとって) / [こと](https://www.weblio.jp/content/事), [Bunpro: に対して](https://bunpro.jp/grammar_points/に対して), [Wasabi: relational targets](https://wasabi-jpn.com/magazine/japanese-grammar/how-to-express-various-targets/) | Subject matter, directed targets, evaluative standpoints and actual noun-modifying forms; connect these with noun-based complements without asserting obligatory hostility, emotional closeness or achieved benefit. Check actual source sections and qualify categorical shortcuts. | [Compound relations and formal-noun contrasts](grammar-compound-relations-sources.json), [earlier noun relations](grammar-relations-sources.json) |
| [TUFS: focus particles](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/095.html) / [Japonin: だけ versus しか](https://www.japonin.com/articles/dake-vs-shika-japanese) / [Daijisen: さえ](https://www.weblio.jp/content/さえ) | Whole-construction polarity, restriction, unexpected inclusion, retained case roles and sufficient conditions. Read the actual Japanese examples; do not turn teaching metaphors into universal surprise rankings or confuse sufficient with necessary. | [Restriction/inclusion article and exercises](grammar-restriction-sources.json), [listing](grammar-listing-sources.json), [topic/inclusion](grammar-topic-sources.json) |
| [Tofugu: に](https://www.tofugu.com/japanese-grammar/particle-ni/) / [で](https://www.tofugu.com/japanese-grammar/particle-de/) / [noun-modifying の](https://www.tofugu.com/japanese-grammar/particle-no-noun-modifier/), [Bunpro: までに](https://bunpro.jp/grammar_points/までに) | Predicate-dependent noun roles, activity versus existence, modification beyond ownership and temporal limits. Do not turn spatial metaphors into universal particle meanings. | [Basic-particle article review and exercise coverage](grammar-basic-particles-sources.json), [topic/contrast/inclusion](grammar-topic-sources.json) |
| [Japan Foundation: こと](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/grammar/201112.html) / [TUFS: とき](https://www.coelang.tufs.ac.jp/mt/ja/gmod/contents/explanation/093.html) | Teaching explanations, attachment, event order and relative tense. Institutional authorship does not make every teaching shortcut universal. | [Actions](grammar-actions-sources.json), [before/after](grammar-before-after-sources.json), [time](grammar-time-sources.json) |
| [Daijisen: 末](https://kotobank.jp/word/末-136437) / [Nihon Kokugo Daijiten: 代り](https://kotobank.jp/word/代り-468939), via Kotobank | Exact senses, readings, classification and distinctions lost in simplified glosses. Match the dictionary, not just the hosting site. | [Outcomes](grammar-expectations-sources.json), [causes/alternatives](grammar-causes-sources.json) |
| [Bunpro: たほうがいい](https://bunpro.jp/grammar_points/たほうがいい) | Broad construction discovery, structure tables, related patterns and example leads. Cross-check categorical restrictions rather than adopting them wholesale. | [Comparison/advice](grammar-comparisons-sources.json), [conditions](grammar-conditions-sources.json) |
| [Maggie Sensei: ばかり](https://maggiesensei.com/2013/07/02/%E3%81%B0%E3%81%8B%E3%82%8A-bakari/) / [Tofugu: つもり](https://www.tofugu.com/japanese-grammar/tsumori/) | Communicative context, register, speaker intention and contrasting formulations. Separate a scenario's nuance from a universal rule. | [Particle neighbors](grammar-particles-sources.json), [intention/inference](grammar-intent-sources.json) |
| [Tofugu: たら](https://www.tofugu.com/japanese-grammar/conditional-form-tara/) / [ば](https://www.tofugu.com/japanese-grammar/verb-conditional-form-ba/) / [なら](https://www.tofugu.com/japanese-grammar/conditional-form-nara/) / [と](https://www.tofugu.com/japanese-grammar/verb-to/) | Conditional formation, premise framing, invitations, habits and actual discoveries. Cross-check blanket restrictions on time and volition. | [Initial conditionals](grammar-conditionals-sources.json), [contexts and combined coverage](grammar-conditionals-contexts-sources.json) |
| [Daijisen: のに](https://kotobank.jp/word/のに-597141) / [くせに](https://kotobank.jp/word/癖に-483705), [Bunpro: わりに](https://bunpro.jp/grammar_points/わりに) / [purpose のに](https://bunpro.jp/grammar_points/のに) | Distinguish connective/final のに from nominalizing の plus case に; assess overlap and speaker stance. A shared spelling or historical connection is not proof of the same meaning. | [のに contrasts](grammar-noni-sources.json), [earlier degree/minimum practice](grammar-kurai-degree-minimum-sources.json) |
| [Tae Kim: amounts](https://guidetojapanese.org/learn/grammar/amount) / [IMABI: after](https://imabi.org/after-i-%e3%81%82%e3%81%a8-%e3%81%ae%e3%81%a1-%ef%bd%9e%e3%81%a6%e3%81%8b%e3%82%89/) | Syntax, negation, tense and more detailed explanations. Account for differences in grammatical frameworks and scope. | [Degree/extent](grammar-degree-extent-sources.json), [before/after](grammar-before-after-sources.json) |
| [JMdict through Jisho: だけ](https://jisho.org/api/v1/search/words?keyword=だけ) | Lexical identity, readings, sense restrictions and accepted spellings. Recognition is not evidence of frequency or idiomaticity in an invented sentence. | [Particle neighbors](grammar-particles-sources.json), [degree/extent](grammar-degree-extent-sources.json) |

Other sources can be useful when they address the exact question. Do not stop searching merely because a claim appears
on a listed site, or reject a relevant source merely because it is absent here.

## Retrieval pitfalls already encountered

- **PDFs:** a successful download with garbled Japanese extraction is not readable evidence. In the
  [result-state batch](grammar-transitivity-results-sources.json), rendering and actually inspecting both original
  Japan Foundation pages supplied the missing particle/diagram evidence. Record the pages and inspection method;
  do not infer the unread text from a filename or a related summary.
- **Bunpro:** simplified extraction can return a forum comment instead of the grammar explanation. Inspect the actual
  Structure, About and relevant Related sections; community discussion is not interchangeable with the main lesson.
  The [comparison/advice record](grammar-comparisons-sources.json) documents this for たほうがいい.
  Similar-looking slugs can also identify different lessons: [ために](https://bunpro.jp/grammar_points/ために)
  is primarily causal, while [ため-に](https://bunpro.jp/grammar_points/ため-に) is the purpose lesson.
  The [compound-relation review](grammar-compound-relations-sources.json) followed the actual page link and inspected both.
- **Kotobank:** extraction can omit the modern Daijisen entry and expose another dictionary or reading. Check the actual
  entry heading and sense, not merely a matching character. The [outcome record](grammar-expectations-sources.json)
  documents the 末 and 癖に cases.
- **Weblio:** isolate the named dictionary from adjacent expression dictionaries and automatically generated examples.
  The [あげく record](grammar-expectations-sources.json) uses Daijisen's spelling heading; it does not establish equal
  frequency for the accepted spellings.
- **Tae Kim:** inline Japanese can disappear in simplified extraction. Inspect the actual HTML/body text before evaluating
  an incomplete example; see the [degree/extent record](grammar-degree-extent-sources.json).
- **Grammar indexes:** follow pagination before claiming list coverage. An index entry supports its stated curriculum
  placement, not every same-spelled sense or variant; inspect the relevant lesson when scope is unclear. Keep retrieved
  URLs, dates and hashes in provenance rather than copying whole pages; see the [classification record](grammar-jlpt-sources.json).

If the relevant passage remains unavailable, record the limitation instead of reconstructing it from a summary.

## Keep provenance in the batch record

Continue recording the exact URL, retrieval date, publisher, inspected heading/sense/section, supported construction IDs,
and important qualifications or claims not adopted in each batch's source JSON. Do not replace those records with a link
to this guide, duplicate their full bibliographies here, or change an old retrieval date merely because its URL was reused.

These notes are contributor-only: `docs/` is not imported by the app. Learner articles should cite the relevant external
sources directly rather than use relative links into this directory.
