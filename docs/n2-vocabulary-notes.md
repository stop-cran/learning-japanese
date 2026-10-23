# N2 vocabulary authoring notes

## Scope and plan

Cover all **1,812 rows** of `original_data/n2.csv` in the pinned
[Kraus distribution](https://github.com/stephenmk/yomitan-jlpt-vocab/tree/b062d4e38c4bdd0950ae1d4ec55f04b176182e03/original_data).
This is a named community list, not an official JLPT syllabus. The baseline is
`f1a93f249b78ae87c8233da1fbb48e92f02d4b44`: 3,273 word articles after the completed
[N2 kanji expansion](n2-review.md).

Use **20 consecutive source rows per batch**: 90 full batches and a final 12-row batch.
Split a batch if its lexical or review complexity requires it; do not increase concurrent work.
The [index](n2-vocabulary-sources.tsv), [snapshot](n2-vocabulary-snapshot.json), and
[review ledger](n2-vocabulary-review.md) distinguish pending, drafted, and review-closed work.
Source IDs use physical CSV lines, including the header: the first row is `N2:2`.

Initial navigation found 75 exact-filename candidates and 76 additional same-entry spelling
candidates. These **151 candidate rows are not verified coverage**. The other 1,661 rows
have neither candidate; none of these counts establishes the eventual number of new articles.
There are 1,808 distinct source forms and 1,794 supplied entry IDs, all present in the pinned JMdict.

## Batch sequence

1. Inspect the original rows, complete applicable dictionary entries, existing cards and comparisons.
   Establish the spelling, reading, intended sense, restrictions, and any uncertain source intent.
2. Author original teaching text or make a narrowly necessary addition to a reusable article.
   Record the exact mapping and dictionary senses; unresolved rows remain explicitly unresolved.
3. Add useful word-to-kanji and kanji-to-word links, check answer-label ambiguity, validate content,
   regenerate the manifest, and commit the authored snapshot as `stop-cran`.
4. Run independent GPT and Claude reviews **sequentially**, on the same frozen snapshot and scope,
   without sharing the other report or the author's adjudication. Each reviewer process must exit
   before the next starts; no nested agents or background reviewer pool.
5. Reconcile against evidence, fix supported defects, and obtain bounded changed-passage confirmation
   where needed. Archive reports, record model contributions and limitations, and commit closure.

The user authorized batch authoring and commits. The completed kanji branch was pushed separately;
this vocabulary branch starts from that completed work. A drafted or structurally valid row is not
review-closed merely because a commit exists.

## Authoring contract

The canonical [format](content-format.md#word-article), [source policy](jlpt-levels.md#vocabulary-baseline),
and [repository review guidance](../.github/copilot-instructions.md) remain authoritative.
These notes add project-specific decisions, not a replacement format or a linguistic validator.

- Preserve stable word IDs, primary readings, existing teaching, and easier sourced article levels.
  A source alias counts only if the article actually teaches the applicable spelling, reading and use.
- Preserve original source fields separately from selected teaching identities. A shared JMdict ID
  is not proof that every spelling accepts every reading or sense. Read `re_restr`, `re_nokanji`,
  `stagk`, `stagr`, spelling/readings flags, inherited parts of speech, and sense-local qualifications.
- Inspect complete relevant entry families, not the kanji project's abbreviated candidate cache.
  Sense indices are one-based within the **2026-10-21** JMdict snapshot. Additional senses do not
  acquire an N2 label merely because an article teaches them.
- Keep all written Han characters in `kanji`, including those without cards. Link every existing
  written component substantively. For a newly covered word containing an N2 kanji card, add or
  update a useful reciprocal example on that card, with the word article's actual reading.
  Other useful backlinks can update existing plain-text examples; do not invent constituent readings
  to accommodate an irregular whole-word reading.
- Inspect actual meanings behind candidate English labels, including ordinary secondary senses.
  Curate direct `quiz_exclusions` where two displayed answers are defensible; the relation is
  symmetric but not transitive. Identical titles already deduplicate. Shared topics alone do not
  justify an exclusion, and distinct wording alone does not establish semantic uniqueness.
- Examples need English translations and selective kana. Distinguish lexical recognition from
  frequency and naturalness; do not turn dictionary order, missing priority, or an unusual source
  spelling into a frequency claim.

## Review and evidence

The requester checks each report's Snapshot / Scope / Verdicts / Findings / Optional / Limits
contract and adjudicates recommendations. The repository validator enforces structure and links;
neither it nor a CLEAN model verdict certifies exhaustive linguistic correctness.
Review correctness, scoped coverage, and comprehensibility for every new article and changed passage.
An unchanged reused article is checked for the specific claimed source coverage, not silently
reported as a new whole-article review.

Record useful unique contributions, shared observations, unsupported findings, optional suggestions,
and evidence unavailable to a reviewer. Compare equivalent observations across the entire reports,
not only their Findings headings. This measures usefulness on the reviewed sample, not a model ranking.

Before each content commit run `python -X utf8 -B tools/validate.py`,
`python -X utf8 -B tools/build_manifest.py`, and the whitespace check; commit the manifest.
For final closure check every source row, preserved baseline identities/levels, exact spelling and
sense mappings, reciprocal N2 links, review coverage, deterministic manifest and commit authorship.

## Current limits and feedback

The initial inventory is navigation only; unworked rows have no selected teaching mapping.
Dictionary evidence establishes lexical identity, not an official modern level or every example's
idiomaticity. Pause consequential unresolved claims rather than manufacturing coverage.
These notes will accumulate grounded corrections from the actual batches.

Report concrete content or guidance gaps through
[repository issues](https://github.com/stop-cran/learning-japanese/issues), identifying the passage,
evidence and learning impact; issue creation requires authorization.

## Recorded lessons

- **Batch 18 reconciliation:** A replacement family with
  several selected senses needs demonstrations of the role
  change and place exchange promised by alias backlinks,
  not only representation. Match a particle explanation
  to an actual construction: Daijisen attests 運転を代わる,
  not a universal rule for every intransitive verb.
- **Batch 18 reconciliation:** An apparently empty simplified
  dictionary fetch can omit a real entry. Inspect the actual
  lexical section when available; a footer, search page or
  challenge is not verification. Keep the receipt's scope
  narrower than the full original examples.
- **Batch 18 reconciliation:** Check feeling, prediction,
  appearance and sign labels against ordinary secondary
  senses and fallback choices. 気味's noun きみ is distinct
  from suffix ぎみ and market-reading きあじ. Preserve the
  initial evidence and append corrections rather than
  silently rewriting the reviewed snapshot's rationale.

- **Batch 18 authoring:** Distinguish dictionary frameworks
  from invented conjugation. Seisenban analyzes 感ずる as
  サ変 and 感じる as its ichidan development; JMdict's
  ずる/じる classification is not a godan paradigm.
- **Batch 18 authoring:** Inspect actual regional and technical
  explanations rather than literalizing compact glosses.
  Modern 関東/関西 need not have historical extents; a dry
  cell still has electrolyte, and a toast does not require
  emptying the glass at once. Match each qualification to
  the source passage that actually supports it.

- **Batch 17 reconciliation:** A tool-only lesson does not
  sense-restrict its quiz prompt: 剃刀's ordinary figurative
  mental-sharpness use still matters against 鋭い's actual
  answer label. Protect direct overlap without expanding
  every article into all dictionary senses.
- **Batch 17 reconciliation:** Merely explaining two
  homographs does not make an unmarked example unambiguous.
  シャツのカラー needs context; do not command one reading
  of its meaning when both color and collar are documented.
- **Batch 17 reconciliation:** Match particle explanations
  to demonstrated argument roles, and replace opaque
  kana-versus-kanji speaking advice with the actual spelling
  and reading. These localized clarity fixes are distinct
  from optional expansion.

- **Batch 17 authoring:** Preserve distinct homograph identities
  when a source gloss bundles them. カラー's color and collar
  uses share Japanese spelling but belong to separate entries;
  additional teaching is not an independently inferred N2 level.
- **Batch 17 authoring:** A useful conventional spelling contrast
  is not always an absolute prohibition. The complete phrase
  family for thirst recognizes 喉が乾く alongside 喉が渇く;
  qualify the older drying-card advice rather than denying it.
- **Batch 17 authoring:** Keep unit claims tied to the actual
  inspected source. Food energy, a calorie definition, and the
  decimal kilo prefix establish different facts; none alone
  verifies every nutritional-label convention or diet claim.

- **Batch 15 reconciliation:** Keep source-storage qualifications
  in the evidence packet, but express their learner consequence
  plainly. 貸家 needs や versus いえ explained for the two whole
  readings; 片仮名 and カタカナ need a shared pronunciation,
  not a discussion of a kana-only dictionary record.
- **Batch 15 reconciliation:** Recheck ordinary secondary senses
  against actual answer labels: settled plans, completed work and
  figurative embodiment can collide even when primary titles differ.
  A rental-property label can also overlap broader house/building
  labels. Add the direct pairs, not a transitive or whole-topic guard.
- **Batch 15 reconciliation:** A useful spelling-recognition example
  need not claim frequency. 偏る can be demonstrated alongside
  片寄る without inferring a corpus tendency from headword order
  or dictionary priority tags.
- **Batch 15 authoring:** Preserve grammatical viewpoint when a
  supplied English gloss is misleading. 片付く is intransitive
  despite the raw "to put in order" wording; a separate historical
  transitive entry does not change modern かたづく. Conversely,
  課税's POS label alone does not license a universal particle
  rule: the actual Japanese entry attests 輸入品に課税する.
- **Batch 15 authoring:** Distinguish whole-entry variants from
  sense-restricted spellings. 個所/箇所 support the noun, while
  additional カ所/ヶ所/か所 forms are counter variants. A shared
  entry does not establish a rigid physical/mental spelling split
  between 片寄る and 偏る.
- **Batch 15 authoring:** Related English technical labels can
  obscure distinct quantities. 加速度 concerns velocity change,
  including direction; it is not current speed. The everyday
  加速/減速 speeding-up/slowing-down contrast is not a universal
  restriction on physical acceleration.

- **Batch 14 reconciliation:** Test tentative quiz leads against
  complete applicable senses, not shared components or related
  English words alone. 可 has an actual approval/vote sense,
  supporting a 可決 guard even though the existing title
  foregrounds permission and a passing grade. A certainty
  adjective alone does not establish a polite acknowledgment.
- **Batch 14 authoring:** An English university label can cross
  levels of reference. 学部 names a faculty/division, including
  the undergraduate division contrasted with graduate school;
  it is not by itself an individual undergraduate or a teaching
  staff member. Inspect the actual definition, not the raw
  "undergraduate" gloss alone.
- **Batch 14 authoring:** An acknowledgment formula's tense and
  speech act differ from a literal past-event report. In
  かしこまりました, polite past form accepts a request rather
  than asserting the work is already finished. English
  "certainly" does not license truth-asserting uses.
- **Batch 14 authoring:** The available word types lack a mixed
  category. Native-first 掛け算 uses `wago` and `mixed-reading`,
  with native かけ plus voiced on-reading ざん explicitly
  explained; the existing on-first `kango` convention is not a
  reason to call both parts on readings.

- **Batch 13 reconciliation:** Distinguish a useful homograph
  clarification from proof that a scoped reading statement denied
  every other word. 帰す/かえす remains the send-home verb while
  separate 帰す/きす supplies a contrast, not another primary
  reading or an independently sourced N2 assignment.
- **Batch 13 reconciliation:** A selected sense can be explicitly
  recognized yet still benefit from a concrete example. Use the
  attested 裾が返る construction for an original garment-hem
  sentence; distinguish construction attestation from attestation
  of the exact new sentence.
- **Batch 13 reconciliation:** Technical source fields such as
  JMdict's stagk are not automatically typos. Check the actual
  data model before taking a reviewer's spelling suggestion.
- **Batch 13 authoring:** A source's spelling, reading and supplied
  entry can agree while its gloss belongs to another reading. The
  反る/かえる row retains that identity, explicitly teaches 返る/反る,
  and distinguishes separate 反る/そる. Record the mismatch and
  additional recognition senses without claiming to recover the
  historical compiler's intent or silently changing the reading.
- **Batch 13 authoring:** Respect spelling-restricted senses even
  inside a shared entry. 関わる/係わる does not acquire 拘る's
  restricted "stick to" sense. A source's bundled gloss is not
  permission to transfer it, just as an alternate reading does not
  acquire 架空/かくう's restricted imaginary sense.

- **Batch 12 reconciliation:** A link can resolve structurally yet
  target the wrong lexical identity. A warning that よう is not
  さま does not make the よう word article a useful さま lesson.
  Prefer the existing kanji card that actually teaches the suffix
  when no dedicated word article exists.
- **Batch 12 reconciliation:** Check English polysemy independently
  of Japanese synonymy: water-source/season "spring" and physical/
  institutional "dissolve" can make context-free answer labels
  ambiguous. Direct guards do not redefine the Japanese words or
  propagate through an intermediate excluded card.
- **Batch 12 reconciliation:** Compare reviewer observations across
  their whole recorded output. An examined lead later dismissed as
  nonactionable is not a unique discovery by the reviewer who
  promoted it to a finding.
- **Batch 12 authoring:** A dictionary aggregation page's headline
  reading need not identify the relevant entry inside it. The 御中
  page headline gives オナカ, but its actual おんちゅう sections
  define the organizational address suffix. Record the inspected
  reading and section instead of transferring the headline's identity.
- **Batch 12 authoring:** Broad source glosses such as "good weather"
  and "and Company" require the actual lexical function. Teach 快晴's
  low-cloud condition and 御中's organizational addressee use without
  turning a loose English label into an unrestricted Japanese rule.
- **Batch 12 authoring:** A reused card with a previously absent
  `jlpt` field can gain source-backed N2 without altering its teaching.
  Call that a level-only update, not an unchanged reuse, and retain
  the baseline identity, reading, title and exclusions.

- **Batch 11 reconciliation:** A dictionary's recall gloss and a
  teaching source's idea-versus-memory contrast answer different
  questions. Retain the supported recognition sense while giving a
  practical 思い出す pattern for ordinary name/past-event recollection.
  Do not invent an unattested 思い付く errand example or a universal
  spontaneous-versus-deliberate rule to satisfy a literal suggestion.
  An AI search synopsis contradicting the inspected dictionary is not
  evidence that the dictionary sense does not exist.
- **Batch 11 reconciliation:** English "morning" can itself be a
  shortened greeting. A greeting/time-period answer-label guard can
  therefore be justified without claiming Japanese 朝 or 午前 is a
  greeting. Check the actual English entry and Japanese target cards,
  not shared tags or an unmeasured candidate-frequency inference.

- **Batch 11 authoring:** A bundled source gloss can cross lexical
  categories or separate families, not merely spellings. Distinguish
  adjective おめでたい from happy-event/pregnancy noun おめでた,
  and aunt 叔母さん from unrelated-woman 小母さん. Preserve the raw
  source wording while recording the actual selected lexical identity;
  do not transfer every bundled gloss to the mapped article.

- **Batch 10 reconciliation:** Spelling-specific examples are not
  exhaustive meaning compartments. Contrast taxes under 納める and
  achievement under 収める while acknowledging 収める's shared
  dispute-settlement use with 治める. Check unrestricted senses and
  their cross-references before presenting a spelling contrast.
- **Batch 10 reconciliation:** A subtype can accept a broad displayed
  label: a school excursion or date can be an outing, and a domestic
  worker can be a helper. Inspect both actual titles and complete
  senses before guarding a pair; shared topic alone is insufficient.
  Conversely, a startle reaction is not the same viewpoint as
  transitively startling someone merely because both concern surprise.

- **Batch 10 authoring:** A source row's gloss can bundle senses that
  the complete dictionary restricts to different spellings. Preserve
  納める's original achievement/payment gloss as provenance, but teach
  achievement under 収める and payment/delivery under 納める. A shared
  entry ID is not permission to copy every gloss into both cards.
- **Batch 10 authoring:** Do not normalize a surprising source reading
  to a familiar homograph. 御手洗 at みたらし is the shrine purification
  place; おてあらい is a separate restroom entry. Inspect the actual
  row and definition, and avoid invented constituent readings.

- **Batch 09 reconciliation:** English "I am sorry" can collide between
  sympathy and apology answers without making the Japanese expressions
  interchangeable. Guard the actual labels and preserve the speech-act
  distinction. Shared tags alone do not establish candidate frequency.
- **Batch 09 reconciliation:** A warning using "historical" can wrongly
  suggest an archaic register when it merely contrasts past-time and
  interactional translations. State the construction-dependent contrast
  directly and check the dictionary's actual register tags.

- **Batch 09 authoring:** Exact-word searches must account for CRLF:
  an end-of-line pattern without optional carriage return missed most
  existing comparison cards. An empty or partial search is not evidence
  of absence until the query is checked against a known existing card.
- **Batch 09 authoring:** A rendered table-of-contents heading such as
  "etymology" is not the etymology text. If the actual entry is unavailable,
  omit an unnecessary borrowing-history claim rather than infer it from
  the katakana spelling or an empty JMdict loan-source list.

- **Batch 08 authoring:** Copy comparison entry IDs from the extracted
  records, not from memory or similar-looking numbers. A correct
  comparison in prose does not verify its numeric citation. Check
  the cited family's actual headword and applicable reading/sense.
- **Batch 08 reconciliation:** Check provenance statements about omitted
  senses against the complete family too. 延長's selected teaching was
  correct while its omitted-sense note named unrelated meanings.
  Correct the mapping and packet together, refresh the index hash,
  and include the actual provenance diff in bounded confirmation,
  not only the app-facing card diff.

- **Planning:** `揚げる` and `挙げる` have separate modern JMdict entries from the giving
  article `あげる`; matching kana is not adequate reuse evidence. The original source gloss
  remains in provenance even when its broad English wording needs correction.
- **Planning:** Source `明き` can map to stable `空き` only after explicit alias teaching is
  present. Source kana `あかんぼう` can reuse `赤ん坊` without changing its N4 label.
- **Pilot review:** A displayed English label can collide through a taught secondary sense
  (`挙げる`/`収める`) or an English noun/verb ambiguity (`味わう`/`味`).
  Check actual labels as well as Japanese lexical substitution, and add direct pairs:
  exclusion through a third article does not protect them.
- **Pilot review:** Inspect useful alternate-spelling and comparison links, not only the written
  headword's metadata: 相 in 相変わらず and 示す in 例を示す were missed in the first draft.
- **Pilot reconciliation:** Check habitual-adverb candidates directly. Complete entries for
  `いつも` and `普段`, not their existing mutual exclusions, supported the additional pairs.
  Priority-tag counts were not used to invent a frequency distinction between spelling variants.
- **Pilot reconciliation:** A mnemonic warning should not accidentally sound like a qualified
  literal definition. The 飽くまで revision states the learner warning directly and names the
  Japanese expressions being contrasted, rather than using an English gloss as the subject.
- **Batch 02 authoring:** Preserve an established easier vocabulary label, not an incidental
  kanji-based app fallback. The reused 暴れる, 脂, 余る and 編む previously had no vocabulary
  level; their verified N2 rows now establish explicit N2 labels without changing their identities
  or teaching. Existing あちこち retains N3 and explicitly teaches source あちらこちら.
- **Batch 02 authoring:** An alternate spelling can link to an article under another stable
  spelling when that article explicitly teaches it: 温まる/温める link to 暖まる/暖める.
  Keep the written-headword kanji metadata separate from these additional spelling links.
- **Batch 02 reconciliation:** When an alternate-spelling article says to use context, give a
  supported contextual contrast rather than leaving that instruction abstract. Official
  異字同訓 entry 007 explicitly includes 暖まる/温まる and 暖める/温める; it supports
  room/air versus food/drink tendencies, but not the body/hand preference proposed in review.
  Replace uncertain teaching examples without treating an unverified preference as a strict error.
- **Batch 02 reconciliation:** Check direct pairs even when another related pair is already
  guarded: 名/名前 does not protect either from 宛名. A conversational translation such as
  あたりまえでしょう, "of course," can also reveal an answer-label overlap with もちろん.
- **Batch 03 authoring:** Source 在る can reuse the unchanged N5 ある article: it already
  teaches existence and explicitly displays 在る through a linked character followed by る.
  Coverage checks normalize Markdown link labels before testing that displayed alias;
  no duplicate article or invented general "live/reside" definition is needed.
- **Batch 03 authoring:** The official 異字同訓 report's entries 014-016 were inspected in
  the actual PDF. They ground the 荒い/粗い and 著す/表す/現す comparisons and corroborate
  recognizing 在る while usually writing ある. Keep reading-restricted senses separate:
  あれこれ does not inherit the approximate-duration use restricted to かれこれ.
- **Batch 03 reconciliation:** Avoid unexplained references to "the source" inside app-facing
  articles; state the learner's spelling or meaning guidance directly. English noun/verb
  ambiguity such as "author" can require a direct quiz guard even when the Japanese
  grammatical roles are different. Compare optional/tentative report notes too: 粗い/かさかさ
  and the 徐々に link were shared observations, not unique findings of the model assigning
  the higher severity.
- **Batch 04 authoring:** A source row can supply a real word but an incompatible
  character-like gloss. Preserve both original fields; do not reuse a homophone
  or teach every character meaning as a word sense. For 佚/いつ, the actual
  Seisenban noun entry and Koji Seigo expression establish a recognition-focused
  article without manufacturing modern collocations or inferring frequency.
  A web-search summary was not sufficient: actual fetched entries were inspected.
- **Batch 04 authoring:** Existing date cards can already cover a source on-reading
  while retaining easier native primary readings. Reuse 一昨日 and 一昨年 unchanged
  after checking their bodies. Qualify normal temporal-boundary inclusion rather
  than claiming every event-based use of 以後 or 以降 has an absolute inclusive boundary.
- **Batch 04 reconciliation:** Explain native-first mixed kun+on readings and use
  the established `wago`/mixed-reading grouping, as on 場所; recognizing the whole
  reading is not the same as explaining its components. Keep a collective gloss
  such as "food, clothing and shelter" together instead of separating its parts
  with the semicolons used for alternative senses.
- **Batch 04 reconciliation:** Compare equivalent observations across all report
  sections: 同一/同様 and 優秀 were shared observations even though Claude put
  them under Optional. Check newly proposed ordinary secondary senses, not just
  title text or a mutual exclusion neighbor. 一緒 has a same-time sense; 常に's
  frequency meaning alone does not make it a fixed-value synonym of 一定.
- **Batch 04 confirmation:** Approximation particles can share a defensible
  context-free English answer with a qualifying adverb even when their Japanese
  syntax differs. Check actual labels and entries, not just shared candidate
  tags: fallback choices still justify the cautious 一応/くらい and 一応/ほど
  guards. Do not remove valid glosses merely to disguise label ambiguity.
- **Batch 05 authoring:** Preserve source variants without promoting search-only
  forms to preferred production spellings. Source ウエートレス is explicitly
  taught under ウェイトレス. Same-entry 煎る/炒る can share an article
  when both spellings and the actual cooking use are taught; homophonous いる
  is not reusable. Actual dictionary entries support a qualified cooking
  comparison, not a sharp oil-free division inferred from a search summary.
- **Batch 05 authoring:** A kanji's written reading boundary is not necessarily
  the verb's conjugation stem. 飢 writes う, but the ichidan stem retained
  before ます is うえ-. Keep spelling explanation separate from inflection.
- **Batch 05 reconciliation:** A semantic distinction can need both explanation
  and a quiz guard: observer unawareness in いつのまにか differs from secret
  action in こっそり, while their context-free English labels still overlap.
  Name the contrast rather than leaving an unexplained situation in the text.
- **Batch 05 reconciliation:** Industry terminology sources can support a
  qualified usage convention when a general dictionary only establishes shared
  meaning. Actual manufacturer and printing-dictionary pages support consumer
  インク versus printing-industry インキ labels; they do not establish a
  composition boundary, universal substitution ban or measured frequency.
- **Batch 06 authoring:** A historical Chinese-derived name can justify a
  kana headword's grouping without inventing modern per-character readings.
  For うどん, distinguish lexical name history from a comprehensive claim
  about the dish's ancestry. Keep `kanji: []` for the actual kana headword,
  while recognizing rare 饂飩 and outdated うんどん explicitly.
- **Batch 06 authoring:** Official spelling guidance can expressly allow
  overlap rather than partitioning homophones by medium. 異字同訓 entry 025
  contrasts image recording with reproduction/display and allows 映る for
  playback and simultaneous live displays. Keep that viewpoint distinction
  instead of imposing an absolute photograph-versus-video boundary.
- **Batch 06 reconciliation:** A binary PDF response is not readable evidence.
  Give both confirming reviewers the same provenance-labelled extraction of
  the actual page and footnote; distinguish their independent interpretation
  from independent retrieval. Do not rewrite supported spelling guidance
  merely to conceal a tool-access limitation.
- **Batch 06 reconciliation:** Check appearance, facial-expression and humble
  acceptance senses against actual answer labels. Nearby exclusions through
  現れる, いただく or 会議 do not protect another pair. A recognized
  visual-harmonizing sense can justify a quiz guard without becoming the
  lesson's production focus or an unsupported modern-frequency claim.
- **Batch 07 authoring:** Keep source sales labels separate from the selected
  practical comparison. Actual 売上 and 売れ行き entries support takings
  versus how goods sell, not an absolute numerical-versus-trend partition.
  A search-only source spelling can be recognized explicitly without
  becoming the preferred written learning form.
- **Batch 07 authoring:** A written expression can combine on readings with
  a native linking particle: 絵/エ + の + 具/グ. Preserve the actual
  construction rather than inventing a のぐ constituent reading or
  calling every kana-containing form an all-kun compound.
- **Batch 07 reconciliation:** A dictionary's secondary adverbial sense
  can create an English-answer collision even when the existing article's
  title foregrounds an adjective: 大変 also means "very." Inspect the
  actual uses, not just title strings or a chain of existing exclusions.
  Apply the same direct-pair check to broad dictionary, entrance and
  exhausted-supply labels without asserting unrestricted Japanese
  substitution.
