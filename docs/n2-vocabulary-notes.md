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

- **Batch 36 reconciliation:** A curated comparison inventory
  is not an exhaustive title audit. Claude's wider title search
  found デモ outside the initial capture; actual protest-rally
  uses support 集会/デモ, not a blanket institution/crowd clique.
  Conversely, generic “stop” language alone does not justify
  締め切る/止す. Add and remove edges on precise meanings.
- **Batch 36 reconciliation:** Name the morphology behind a
  related example: 洒落た店 uses the verb 洒落る's た-form,
  not the noun 洒落 plus た. The actual public verb sense 2
  supports the refined shop; JMdict1568670:2 concerns joking.
  Keep these public and pinned-dictionary indices separate.
- **Batch 36 authoring:** Keep public-dictionary headings
  separate even inside one captured lexical container:
  氏名/うじな, 蛇口/へびくち and 集会's historical Buddhist
  readings do not license pooling their definitions.
  Public sense order also differs from JMdict for 締め切り.
  Record the exact teaching identity and one-based JMdict index.
- **Batch 36 authoring:** Interpret coarse source glosses
  in their actual construction. 締め切る's “shut up” concerns
  closing an opening, not silencing a person; しゃぶる's
  raw “chew” must be qualified against the suck/lick entry.
  Attested 打線が湿る supports a figurative slump example,
  not an inference that every reflective mood is depressed.
- **Batch 35 confirmation:** Do not narrow a recorded behavioral
  sense to outward appearance when adjudicating coarse quiz
  labels. 地味's reserved/modest behavior can leave 謙虚 a
  defensible English answer even though plain living does not
  itself imply humility. Add the precaution and teach the
  distinction. Preserve the first reviewers' disagreement;
  a later correction is not retroactive initial agreement.
  しびれる's emotional sense is index 3, not electric-shock
  index 2; check exact indices before accepting an added pair.
- **Batch 35 reconciliation:** An adverb label does not prohibit
  an attested しみじみとした + noun construction. Teach the
  positive pattern without inventing unrestricted standalone
  する usage, an omitted と, or frequency from an example count.
  Read actual source bodies: footer-only pages and generated
  search attributions are not corroboration.
- **Batch 35 quiz review:** Shared English words are hypotheses,
  not automatic guards. Distinguish unshowy living from humility,
  geographical plain from plain appearance, and authoring from
  written representation. Conversely, read complete comparison
  articles before removing a precaution: 棒 explicitly teaches
  a drawn-line/dash use, not only a physical rod.
- **Batch 35 model comparison:** 実例/ケース appears as a GPT
  finding and a Claude optional observation, so it is shared.
  Across all sections the first thirteen accepted pairs divide into
  five shared, four GPT-only and four Claude-only observations.
  Final confirmations accept two more Claude-origin pairs,
  giving fifteen cumulative additions: five shared, four
  GPT-origin and six Claude-origin. Both models accept the final
  correction; that does not change initial-discovery attribution.
  Keep the non-animal example and explicit scope improvements
  separate from claims that the original selected senses were wrong.
- **Batch 35 authoring:** A raw English gloss can span multiple
  current senses: 実力 explicitly includes arms/force as well as
  ability, so both are selected, not mislabeled as additional.
  Conversely, しぼむ has one broad principal sense despite public
  subdivisions for flowers, balloons and hopes. Preserve the
  pinned dictionary's actual indices.
- **Batch 35 evidence:** Distinguish captured comparison bodies
  from inspected ones; reading every family and label does not
  mean every captured article was read. Likewise, the historical
  reciprocal-pair audit counts new articles only: existing reuse
  backlinks remain useful but must not inflate that count.
- **Batch 35 authoring:** Conventional 私鉄/JR usage is not
  mechanically derivable from present ownership alone. Separate
  different public headwords (実物/みもの, 紙幣/しべい,
  地味/ちみ) and historical spellings from the selected identity.
- **Batch 34 reconciliation:** Temporal extent or habitual
  frequency is not the same lexical answer as continuation or
  performing an action again. Remove those five 始終 edges,
  but independently retain its all-times overlap with いつでも.
  Actual English labels can also blur item-taking 持参 and
  person-taking 連れる; a guard does not erase that Japanese
  distinction. Check missing comparisons outside the first capture.
- **Batch 34 review:** Distinguish a correct alternate spelling
  from an example that introduces it before explaining it.
  Illustrating 静まる's subsiding use with 静 keeps the learner
  oriented without making 静/鎮 preferences absolute.
  Clarify current noun 始終 without an unevidenced frequency
  ranking, and connect シュウ to voiced ジュウ explicitly.
  Shared voicing observations and three shared tentative
  overguard observations are not model-unique discoveries.
- **Batch 34 authoring:** Distinguish duplicate source readings
  from duplicate article identities: 湿気 しっけ and しっき
  share one complete dictionary family and one new article,
  but retain two independently mapped source rows.
  Compare the raw gloss before classifying secondary teaching:
  下町's source explicitly names Shitamachi as well as lower
  parts of town; しつこい's rich-taste use is additional to
  the source's persistence gloss.
- **Batch 34 authoring:** A useful character mnemonic cannot
  overrule an actual adverbial sense: 始終 includes frequent
  habitual occurrence, not only an uninterrupted finite event.
  Likewise, 四捨五入's raw "rounding up" must not become
  ceiling, and 静/鎮 spelling preferences are not strict
  reading/sense restrictions.
- **Batch 33 reconciliation:** Check actual manner versus timing,
  not a loose shared English gloss: はきはき's clear/brisk
  speaking does not make it 至急's urgent/as-soon-as-possible
  answer. Remove that unsupported edge, while adding directly
  supported personal-origin 出 and completion しまう edges.
  A correct semantic finding does not establish a reviewer's
  speculative account of how the mistake was introduced.
- **Batch 33 model comparison:** 出/しまう appeared as GPT
  findings and Claude optional observations. Comparing only the
  Findings sections would falsely credit unique discoveries.
  Preserve complete native final reports, including substantive
  opening paragraphs, and state actual source-inspection limits;
  shared CLEAN judgments do not fill a source-access gap.
- **Batch 33 authoring:** An already taught same-entry variant can
  need only sourced level metadata: しいん maps to existing しーん,
  adding N2 without changing its ID, primary reading, title, image
  or exclusions. Call this metadata-enriched reuse, not unchanged
  reuse. Likewise, use the linked 故郷 article's actual こきょう
  reading rather than silently attaching a different valid reading.
- **Batch 33 authoring:** Inclusive calendar counting and elapsed
  days are different quantities. Daijisen's fourth day counting
  today supports standard しあさって at day +3, not day +4.
  The separately evidenced regional +4 use stays explicitly regional.
- **Batch 32 review:** Both independent models found the missing
  すっと comparison; GPT additionally caught its ordinary refreshed-
  feeling sense against さわやか. A movement-focused title does not
  erase an explicitly taught secondary meaning. Complete comparison
  families still matter after a large initial candidate selection.
- **Batch 32 reconciliation:** A useful practical farewell contrast
  does not license an unsupported register rule. Preserve the
  teacher/pupil example and specify leaving-work-first with
  お先に失礼します; do not infer universal adult usage or final
  separation from failed public lookups or general learner lore.
- **Batch 32 authoring:** Check the complete lexical family behind
  a comparison card's introductory focus. 布団 also has a Zen
  meditation-cushion sense, 写真 includes photography, and 写す
  includes photographing. Useful teaching contrasts must not become
  false absolute sense boundaries.
- **Batch 32 authoring:** A source gloss can differ from the current
  dictionary family: 錆's raw "rust (colour)" remains in the source
  index, while current 錆 teaches rust and 錆色 is separately indexed.
  Do not invent a principal sense to make the old gloss appear exact.
- **Batch 32 authoring:** Distinguish the audit's new-article
  reciprocal-pair count from links supporting unchanged reused
  articles. Four new pairs bring that count to 145; three existing
  再 examples support reuse but do not increment it.
- **Batch 31 confirmation:** Compute provenance volumes from the
  actual parsed families and rendering, not an unmeasured number
  carried in working notes. GPT caught a false 137-sense claim:
  twenty-five complete families contain 62 senses. Claude repeated
  the incoming count. Preserve both reports and correct the
  evidence with a machine-counted receipt; model agreement alone
  cannot establish a numerical inspection claim.

- **Batch 31 reconciliation:** Pierce/prick teaching needs both
  argument patterns: pointed thing を plus destination に, and
  pierced target を plus instrument で. A natural needle/finger
  example can demonstrate the second without a violent example.
  Keep the insect-passive actor に distinct from a destination.
- **Batch 31 reconciliation:** Recheck actual trailing labels and
  ordinary secondary senses directly. Text-deletion 削る and
  document-writing 書く need their own pairs, not inference through
  消す or 作る. 座敷's positively supported party sense requires
  separate checks against actual party/gathering labels. A shared
  English murmur can warrant a quiz guard without making quiet
  whispering and collective commotion interchangeable Japanese.
- **Batch 31 reconciliation:** For kana-primary さすが, native
  origin supports `wago` while 流石 retains its whole-word irregular
  reading explanation. This is not a universal ban on a type for
  kana spellings. Prefer the positively attested 杯をさす to a
  distracting invented contrast; replacement does not prove the
  former 酒をさす impossible.

- **Batch 31 authoring:** A word's origin and a character-reading
  category are different descriptive layers. Daijisen explicitly
  traces さじ to the Sino-Japanese reading of 茶匙; KANJIDIC's
  kun-labelled さじ does not independently disprove that origin.
  Record the actual source rather than classifying from the
  appearance of a single-character spelling.
- **Batch 31 authoring:** Similar readings do not pool meanings.
  裂く's family reserves allocation for 割く, while 注す/点す
  preferences remain sense-local. Distinguish a dedicated 挿す
  heading from the surrounding broad 差す/指す material; a cutting
  planted to root is not necessarily a graft onto another plant.
  Retain the failed standalone さすがに extraction explicitly.

- **Batch 30 confirmation:** Different leading glosses are not
  protection when the same displayed title also contains an
  applicable ordinary meaning. Follow through on trailing
  planning/arrangements and signal labels with complete families.
  Guard 献立's supported broader use without equating designing,
  discussion and physical preparation; keep サイン's signal sense
  distinct from its signature and separate mathematical identities.

- **Batch 30 reconciliation:** A broader selected sense needs enough
  context to recognize it. Both reviewers noticed 献立's nonmeal
  planning use, although one classified the missing example as
  optional. Its attested meeting construction makes the sense
  concrete. Check direct plan-label pairs independently of existing
  計画 guards; also distinguish the noun 計/けい from the separate
  はか family and the character heading.
- **Batch 30 reconciliation:** Replacing a questioned example with
  a positively supported construction does not prove the former
  sentence impossible. 混合物 provides a clear substance construction
  without deleting JMdict's mixture gloss. Likewise, a tentative
  signal-label hypothesis needs actual sound-use and comparison
  evidence: サイレン's emitted sound supports direct guards with
  合図 and 信号, not an inference through their existing guard.

- **Batch 30 authoring:** As with コレクション, a legacy gloss can
  have positive support under a separate homograph. コンセント's
  Daijisen *consent* heading and informed-consent expression are not
  senses of current JMdict1052330's electrical outlet entry. The
  electrical borrowing's `concent(ric plug)` source does not establish
  an ordinary Japanese adjective meaning "concentric." Keep raw
  source text, current identity and external recognition distinct.
- **Batch 30 authoring:** A source's English "make retroactive" does
  not determine Japanese transitivity. 遡る remains intransitive;
  route を and a construction with transitive 適用する need their
  own explanations. Similarly, 裁縫をする marks an activity noun,
  not proof of an object-taking 裁縫 verb. 採点's separately supported
  assigned-score recognition receives no fabricated JMdict index.

- **Batch 29 confirmation:** An earlier CLEAN review can still miss a
  direct ordinary-secondary-meaning pair. ごめん/恐縮 is supported by
  the pinned feeling-sorry sense and the actual courteous-request
  teaching, not by transitivity through older apology guards. Keep
  the familiar apology distinct from formal request-softening and
  gratitude; do not turn a shared apology situation into a clique
  including the bare noun 申し訳.

- **Batch 29 reconciliation:** A character variant is not an older
  form merely because a dictionary lists it. Both reviewers caught
  the unsupported 筝 chronology; remove that qualification without
  replacing it with an equally unverified historical ordering.
  A Chinese simplified/traditional relation does not by itself
  establish Japanese spelling chronology.
- **Batch 29 reconciliation:** Inspect direct broad-label candidates
  beyond the initial evidence list: musical instrument, entrust,
  recently/lately, waiting apologies and turn over each exposed
  independently supported pairs. Preserve differences in Japanese
  constructions. Replace an unverified mixed-register visiting
  example with a positively attested short formula rather than
  claiming the old sentence has been proved impossible.

- **Batch 29 authoring:** A legacy gloss can have positive support in
  a different dictionary without becoming a sense in the pinned
  principal family. コレクション's separate Daijisen *correction*
  heading is recognized explicitly; JMdict1051540 remains collection
  and fashion. Record the external heading, URL and response hash
  without inventing a JMdict ID or rewriting the raw source.
- **Batch 29 authoring:** Separate construction and register from a
  respectful origin. 御覧's noun, short looking direction and
  て-form invitation need their actual constructions; bare ごめん
  does not become formally respectful from 御 alone. A tipped cup
  also distinguishes contents spilling with こぼれる from exceeding
  capacity with あふれる, despite overlapping English glosses.

- **Batch 28 confirmation:** Describe the exact frozen source field,
  not nearby baseline prose or remembered glosses. Both reviewers
  caught an audience-related gloss incorrectly attributed to N2:552;
  its raw field is only `to cross,to pass,to tide over`. Preserve the
  previous note in correction history rather than silently rewriting
  the evidence trail.
- **Batch 28 reconciliation:** Source-spelling coverage must select the
  sense actually taught with that spelling, even if JMdict has no
  explicit restriction. 超す's quantity example supports selected
  sense 4; 越す crossing, hardship, time and moving are additional
  teaching, not silently transferred source uses. Preserve the raw
  gloss mismatch and original mapping alongside the correction.
- **Batch 28 reconciliation:** A narrower baseline title does not erase
  an ordinary secondary meaning. 掛ける's seating use needs direct
  protection against 腰掛ける. Conversely, a heat description
  (じりじり's scorching sun), an occupation (コック), and an activity
  (料理) are not automatically synonymous with related actions.
- **Batch 28 reconciliation:** A promised additional building sense
  needs an actual construction, not only "build" in a prose inventory.
  家をこしらえる supplies the missing teaching without expanding
  the selected dictionary scope.

- **Batch 28 authoring:** A legacy vocabulary row can mix readings or
  current lexical identities. 擦る's こする rubbing entry is not
  silently given the match-striking sense of する; コック's Dutch
  cook and English valve entries remain separate, with actual
  reading-specific examples and additional-sense mappings. Preserve
  the raw fields instead of reconstructing compiler intent.
- **Batch 28 authoring:** Record a failed lexical lookup as a failure,
  not a successful page inspection. こちらこそ has positive complete
  JMdict evidence but no lexical body from the attempted public
  lookup. The other nineteen containers do not make it a twentieth
  positive verification.
- **Batch 28 authoring:** Register-sensitive formulas need their actual
  social function. ごくろうさま normally points downward despite
  polite endings; ごちそうさま thanks for a meal rather than naming
  a feast. Traditional 五十音 is not an exact modern kana count.

- **Batch 27 closure:** Distinguish compact rendering lines from lexical
  records when reporting inspection counts: ENTRY headings and array
  lines are not additional senses. Preserve the authentic reviewer
  disagreement and clarify the counting unit rather than rewriting
  historical evidence to make reports appear to agree.
- **Batch 27 confirmation:** Follow a missed duty-label pair through
  other actual duty/responsibility answers, not through an exclusion
  clique. 公務/役・役割・係・責任 each has positive task/duty evidence;
  係's person sense alone would be insufficient. A confirmation can
  expose a first-review miss without implying the correction caused it.
- **Batch 27 reconciliation:** Check broad duty and reason labels against
  positive secondary senses, not a synonym clique. 公務 needs direct
  務め/勤め/義務 guards; 合理/訳 is supported by 訳's good-sense/reason
  sense, not merely its causal-reason use. 高等/松 needs its own guard
  despite an indirect path through 一流.
- **Batch 27 reconciliation:** Keep publisher and register boundaries
  explicit. Daijisen's historical 松 rank uses do not establish the
  modern 松竹梅 tier; the actual 日国 sense does. A historical 合理なり
  example does not license modern 合理な, and noun recognition does
  not settle an unverified modern collocation preference.
- **Batch 27 reconciliation:** Teach a selected merger sense plainly,
  with a contrastive example, rather than a source-facing double negative.
  This improves 合同's coverage without claiming the original joint
  examples were wrong or the new whole sentence was corpus-attested.
- **Batch 27 authoring:** A publisher's lexical container may contain
  several reading headings. 紅葉/こうよう supplies autumn coloring;
  the source's maple gloss is positively supported under separate
  紅葉/もみじ entry 2857870, not by moving that sense to 1578780.
  Preserve raw spelling, reading, entry and gloss, teach the separate
  reading explicitly, and leave the historical compiler's intent unknown.
- **Batch 27 authoring:** A loanword's broad English gloss is not an
  exhaustive sense assignment. コース selects route/study senses and
  separately indexes additional meal and offered-plan uses. Recognize
  individual course versus a complete meal; 皿's positive serving/course
  sense matters when assessing answer-label ambiguity.
- **Batch 27 authoring:** Word-family derivatives and aliases need actual
  construction coverage. 合理's noun does not license 合理な; 合理的
  supplies the adjective. Reusing 越える for source 超える requires
  its already taught spelling, reading and exceeding use, plus a useful
  超 component link, without changing its stable identity or easier N3.

- **Batch 26 reconciliation:** An absent English gloss is not proof of an
  absent ordinary sense. 公衆/一般 is supported by the existing 一般
  article and positive Daijisen public-noun sense even though JMdict's
  glosses differ. 功績/働き similarly requires inspecting the ordinary
  achievement sense, not only the work/functioning title. Resolve
  disagreement with positive evidence rather than counting model votes.
- **Batch 26 reconciliation:** Track the actual dictionary section, not
  just its last redirect link. The follow-up 働き extraction initially
  carried SGKDJ into a later NHGKT machine-generated section. Resetting
  publisher at named section anchors and checking all seventeen actual
  bodies preserved the fifteen original receipts and excluded the false
  extra container.
- **Batch 26 reconciliation:** An optional observation can close a real
  label ambiguity or source limit. 交差/越える・越す need guards for
  the actual English crossing labels, not merely consistency with 渡る.
  高層気流 supplies positive compound evidence for the atmospheric
  example without proving the removed construction wrong or certifying
  the whole authored sentence as corpus-attested.
- **Batch 26 authoring:** A successful page fetch is not a dictionary-entry
  check. Simplified Weblio output for 高層/公式/校庭 and 交替 yielded
  unrelated material or footers. Inspect the complete lexical container
  associated with the actual publisher; do not promote the failed
  extraction to a positive receipt. Keep complete copyrighted evidence
  private and publish concise original observations and source links.
- **Batch 26 authoring:** Preserve source-gloss qualifications and dictionary
  sense numbering separately. 高層's upper maps explicitly to pinned
  JMdict sense 2 while building sense 1 is additional; Daijisen reverses
  their order. 校庭's campus concerns outdoor school grounds, not all
  campus buildings. A broad gloss needs positive qualified coverage,
  not silent replacement.

- **Batch 25 reconciliation:** An unexplained change of particle roles is
  real even when the dictionary recognizes the verb's meaning. 請う's
  request frame did not explain the invited-person/role frame of its
  second example. Replace the unverified collocation with the inspected
  許しを請う expression; retain JMdict's positive invite sense without
  treating its absence from Daijisen as disproof. The authored receipt
  over-attributed inviting to Daijisen and is explicitly superseded by
  the correction evidence rather than silently rewritten.
- **Batch 25 reconciliation:** Check a linked card's full body before
  calling its alternate reading wrong. 故郷 explicitly recognizes
  ふるさと while teaching こきょう as primary; aligning the incoming
  label improves navigation, not lexical correctness. For 顕微鏡's
  science example, use the positively sourced 生物/せいぶつ reading
  rather than infer an unlimited prohibition from missing dictionary forms.
- **Batch 25 reconciliation:** Review observations under Optional as well
  as Findings. 厳重/押さえる's exposed "secure" labels warrant a direct
  safeguard despite different Japanese constructions; no unmeasured
  assumption that the app rarely draws the pair can replace that check.
- **Batch 25 authoring:** Broad source glosses need construction-level
  qualifications, not deletion: 原産's habitat concerns native origin,
  恋しい's dear/beloved retains longing, 原理's theory concerns an
  explanatory foundation, and 公共's society/community concerns public
  affairs. A shared sense does not make every English rendering unrestricted.
- **Batch 25 authoring:** Verify exceptional conjugation against an actual
  table rather than a recognized headword or an unsourced adjacent
  correction. 請う uses こうて/こうた, with こわない and こいます;
  contradictory Japanese Wiktionary material is not affirmative evidence.
- **Batch 25 authoring:** Separate source sense selection from useful extra
  teaching when the English list is broad. 高級 selects quality here;
  high rank remains explicitly additional and retains its separate
  noun/の-modifier classification. 請う's praying/wishing is likewise
  additional, not another independently established N2 assignment.

- **Batch 24 reconciliation:** General English answer labels can overlap a
  qualified sense even when the Japanese words are not unrestricted substitutes.
  The actual amusing, tone, text and visit labels justify direct guards for
  傑作/愉快, 気配/調子, 原稿/テキスト and 見学/訪問・訪ねる.
  Existing guards through 面白い or 文章 do not protect a third pair.
- **Batch 24 reconciliation:** An unlocated example is not disproved by a
  failed search. Replace an uncertain specialist collocation with an actually
  inspected dictionary compound when that preserves the lesson.
  気配 now uses Daijisen's 買い気配 and notes the financial きはい
  cross-reference without incorrectly excluding けはい from that sense.

- **Batch 24 authoring:** Readings and source IDs can
  agree while an English gloss belongs to another
  reading: 削る's percentage-taking is はつる,
  not selected けずる. Preserve the raw gloss and
  record the exact separate entry instead of
  manufacturing a commission sense.
- **Batch 24 authoring:** Qualify raw English at the
  construction level. 桁's column is structural
  or numerical, not every pillar or spreadsheet
  column; 険しい's sharp eyes describe a stern
  look, not visual acuity. 気配's market tone is
  positively taught, but raw worry remains
  unestablished.
- **Batch 24 authoring:** Do not infer constituent
  irregularity solely from a public heading mark:
  KANJIDIC2 explicitly gives 駄 the on reading タ,
  supporting 下駄 ゲ + タ. Conversely, 気配's
  ateji and older けわい require an actual
  spelling/history source, not an invented
  distribute-spirit compound explanation.
- **Batch 24 authoring:** Recheck exact supporting
  entry IDs against the extraction before freezing.
  Source-local sense numbering can reverse:
  下水 is infrastructure then wastewater in
  JMdict, but wastewater then infrastructure in
  the inspected Daijisen body.

- **Batch 23 reconciliation:** Baseline exclusions
  may need a narrowly documented extension when a
  reused article's answer-label neighborhood is
  genuinely ambiguous. The form quartet needs all
  six direct pairs, including comparison-to-comparison
  pairs; exclusions are not transitive. Preserve
  original lists and record exact additions rather
  than claiming unchanged baseline exclusions.
- **Batch 23 reconciliation:** Inspect ordinary
  secondary meanings beyond a card's selected
  teaching: 筋 includes lineage. Compare all report
  sections before crediting model diversity. The
  shared 形式/形 finding is one catch; optional
  honorific and cultivated-accomplishment guards
  also count as observations.
- **Batch 23 reconciliation:** Resolve uncertainty
  without inventing a rule. Replace disputed 何郡
  with どの郡 rather than infer a categorical reading
  rule from analogy. Use Daijisen's actual
  青系統の色 example and remove an unverified
  芸能 collocation while retaining its supported
  cultivated-ability meaning. Update source IDs
  when adding linked kanji examples.

- **Batch 23 authoring:** Shared spelling does not
  authorize changing a baseline card's reading.
  包む つつむ remains its existing N4 identity;
  source くるむ gets a separate usual-kana article
  and a dictionary-backed 包 backlink. Likewise,
  毛糸 is native け + いと, not evidence that 毛
  has an on reading ケイ.
- **Batch 23 authoring:** Preserve raw mismatches,
  but teach qualified identities: 郡 is county,
  not nation; 形式's mathematical use is a form,
  not every expression; 系統's raw geology gloss
  is not established by the inspected definitions.
  芸能's accomplishments are cultivated abilities,
  not completed results. 蛍光灯's person label
  must remain explicitly dated.
- **Batch 23 authoring:** Identify missing exact
  headwords and the actual supplementary source.
  二次形式 and きれいだ were absent from the pinned
  exact-form extraction. The separately inspected
  二次形式 introduction was hosted Wikipedia,
  not JMdict or Daijisen. The partial 形容詞
  introduction was 実用日本語表現辞典.

- **Batch 22 reconciliation:** Search actual English
  labels beyond the initially selected Japanese
  comparison neighborhood. 工夫/知恵 share practical
  ingenuity; くっつく/べたべた share sticking/clinging;
  組み立てる/セット share the broad setting-up answer.
  These direct quiz guards do not assert unrestricted
  Japanese substitution. Replace 悔しい's ambiguous
  English "mortified" with frustrated/disappointed;
  do not turn that clarity fix into an unsupported
  claim that JMdict's "mortifying" gloss is obsolete.

- **Batch 22 authoring:** A source can give a reading
  and entry ID that agree while its English gloss
  belongs to another homograph. Preserve 工夫's raw
  "labourer,worker", but explicitly map the agreeing
  くふう/1278220 to devising and practical ideas.
  Worker belongs to dated/sensitive こうふ/1278230,
  not a new meaning or N2 assignment for くふう.
- **Batch 22 authoring:** Preserve genuine spelling
  overlap rather than manufacturing tidy compartments.
  汲む and 酌む both support pouring/drinking and
  considering feelings; the sake-serving spelling note
  favors 酌む without creating an absolute partition.
  悔やむ must positively teach the selected mourning
  sense, not only the additional regret use.
- **Batch 22 authoring:** Dictionary numbering is
  source-local. Daijisen reverses JMdict's 悔やむ
  order and combines taste/color under one くどい
  definition. Identify the actual hosted dictionary:
  the partial 句読点 body was 新語時事用語辞典,
  not Daijisen.

- **Batch 21 reconciliation:** A comparison sweep can
  cover 笑う/笑顔 yet miss the separately titled 笑い,
  or cover 下がる yet miss 下降. Check direct pairs,
  including derived nouns and ordinary secondary
  meanings. 架空's physical overhead sense matters
  when 空中 is added even though its earlier main
  teaching concerned imaginary things. Preserve the
  actual spelling/reading restrictions.

- **Batch 21 authoring:** Treat raw English glosses
  as claims to resolve, not instructions to flatten
  Japanese meanings. 苦心's "pain" is painstaking
  effort, 斬る's "murder" requires blade context,
  and 区切る's "stop" needs a section or stopping
  point. Preserve both banknote-changing and
  demolition uses selected by the 崩す row.
- **Batch 21 authoring:** A complete family can contain
  a sense that belongs to another reading: the
  くさめ charm expression is not a くしゃみ meaning.
  Dictionary order and a historical quotation do not
  independently establish modern rarity or obsolescence.
- **Batch 21 review setup:** The batch-20 report
  disclosed an accidental grep hit in the forbidden
  author rationale. For batch 21, give both reviewers
  an equivalent, hash-recorded evidence derivative
  with only `quizGuardRationale` removed, and forbid
  the full packet. This reduces accidental exposure;
  the canonical source packet retains the rationale.

- **Batch 20 reconciliation:** A selected embarrassment
  sense needs positive teaching, not only a contrast:
  恐縮 can describe being humbled by praise or ashamed
  of an error. Keep this self-effacing use distinct from
  an unrestricted replacement for 恥ずかしい.
- **Batch 20 reconciliation:** Direct quiz guards cannot
  be inherited through other gratitude, apology or pay
  words. Check 恩/申し訳 against 恐縮 and 納める
  against 給与 themselves. English "function" also
  needs attention across 行事/機能 despite their
  different Japanese meanings. A shared word inside
  a compound title does not by itself prove ambiguity:
  客間's room and 応接's receiving activity remain
  distinct in the inspected entries.
- **Batch 20 reconciliation:** A general cue
  clarification can be grounded in JMdict without
  promoting a community theater gloss to compulsory
  specialist teaching. Trim キャンパス's unsupported
  "university life" expansion while retaining the
  dictionary-supported extended university use.

- **Batch 20 authoring:** Keep a source-selected sense
  even when another use is more familiar. 給与's raw
  allowance/grant/supply row selects provision; salary
  is explicitly additional teaching. 行列's raw row
  requires both a queue and a mathematical matrix.
- **Batch 20 authoring:** Attribute the actual dictionary
  body, not the hosting page or a simplified extraction.
  The 給与, キャンパス and 行列 Daijisen bodies were
  inspected separately; an English "gang" article is
  not evidence for neutral Japanese ギャング usage.
  A successful encyclopedia fetch is not automatically
  a lexical dictionary check.
- **Batch 20 authoring:** Rest words can differ in
  perspective without a fixed duration rule. 休憩
  frames a break in activity; 休養 emphasizes restoring
  energy. 客間 foregrounds receiving visitors, without
  an absolute ban on overnight use.

- **Batch 19 reconciliation:** A reused baseline article
  can expose a direct quiz ambiguity: 機械's instrument/
  apparatus use overlaps 道具 even though the primary
  title foregrounds machinery. Preserve original guards
  and record an exact, evidenced addition rather than
  pretending a corrected baseline list is unchanged.
  Keep the audit exception as narrow as the actual pair.
- **Batch 19 reconciliation:** A plain separate-word
  explanation is clearer than internal "identity" jargon:
  ベース's musical bass belongs to its own dictionary
  family, not a new sense of the operating-base entry.

- **Batch 19 authoring:** A raw gloss can bundle meanings
  restricted to different readings: 冠's first/best sense
  belongs to かん, not primary かんむり. Record the
  supplementary reading explicitly rather than transferring
  its meaning to the source reading.
- **Batch 19 authoring:** Shared entries need not create
  duplicate cards or erase spelling preferences. Reuse
  existing N3 機械 for explicitly taught 器械, and teach
  基準/規準 together with their qualified dictionary
  emphases. Separate 被せる/かぶせる and 着せる/きせる
  identities despite the latter's recognized 被せる spelling.
- **Batch 19 authoring:** Count distinct mapped articles
  and reciprocal pairs, not source rows. The two 基準/規準
  rows share one article and one primary 準 backlink.
  An existing baseline article first reused in this batch
  still increases the cumulative reused-article count.

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
