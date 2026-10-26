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

## Batch 80 authoring observations

- N2:1582-N2:1601 map to twenty articles: eighteen physical additions,
  unchanged cross-batch reuse 混ぜる and unchanged baseline N4 または.
  Source 交ぜる and 又は share those canonical entries and readings.
  Packet new/reused counts are relative to the original baseline:
  nineteen nonbaseline paths include batch 79's 混ぜる, not nineteen
  physical additions in batch 80.
- Actual pre-card inspection covers twenty principal families / 35
  senses, fourteen family chunks with a distinct union of 326 complete
  families / 861 senses, 164 complete older word bodies, all 260
  navigation labels, thirty components and three complete related
  kanji bodies. Larger prepared availability is not actual inspection.
- Five additional complete families / nine senses and four complete
  older bodies were read after drafting. The actual author unions are
  now 331 / 870 and 168 older bodies. Keep the sealed pre-card receipt
  unchanged. Upper/lower eyelid spellings and readings have their own
  complete entry evidence, not just inferred character readings.
- Twenty complete public captures are one Digital Daijisen authority
  via Weblio. Separate the unrelated classical またぐ heading from
  跨ぐ. The captured shortly definition does not establish the separate
  dictionary-form-verb + 間もなく attachment; the pinned full entry does.
- Author self-review replaced an example accidentally using separate
  またがる with an actual またぐ spanning example. It also removed
  wording that could misrepresent 真っ暗い as a nonexistent word.
  Neither correction is an independent reviewer contribution.
- Preserve the distinction between transitive まとめる and
  intransitive まとまる, without imposing a quiz transitivity exemption.
  Color, tanning, pallor, blankness, hopelessness, organization,
  collection and settlement comparisons require actual secondary
  senses, not category cliques or rigid English partitions.
- Kana-primary source mappings still explicitly recognize 纏まる,
  纏める and 間も無く. まぶしい has literal and figurative radiance;
  its spelling list alone does not prove a usual-kana frequency claim.
- Add 街角/角 and 祭る/祭 as two new primary reciprocal N2 pairs.
  Recheck existing 混ぜる/混. Keep both reused cards, kanji 混, and the
  batch 79 packet unchanged; edited 角/祭 retain all prior metadata and
  unrelated teaching.
- Independent initial reviews are authenticated against `6102eb03`,
  using GPT-6.1 Sol and Claude Opus 5.5 sequentially. Both returned all
  33 mandatory complete file reads without edits. GPT additionally
  returned all 36 comparison chunks: actual depth 331 families / 870
  senses and 173 older/reuse bodies. Claude read 25 families / 44
  senses and three older/reuse bodies, including the two assigned
  reuses; snippets and prepared availability are not complete reads.
- GPT uniquely proposed eight adopted direct quiz pairs: hopeless
  真っ暗/終わる, worship 祭る/敬う, both organization verbs/完了 and
  /合同, まとまる/合流, and まもなく/直に through the separately
  recognized じきに reading. An older article's primary title or
  reading does not erase its ordinary secondary senses.
- Claude uniquely motivated bounded またぐ wording, explicit 日焼け
  in the tanning example and optional お金 in the gathered-funds
  example. Do not adopt its no-astride implication categorically:
  the pinned entry explicitly includes straddle, while またがる is
  the separate mounting/sitting lexeme. Retain the source-backed
  title and improve the teaching's specificity instead.
- Post-review author inspection adds 36 complete families / 98
  senses and fifteen full older bodies as a separately recorded
  stage. Six families / eleven senses and five bodies are new to the
  actual union: 337 / 881 and 173 bodies. Three additional live
  Kotobank pages were read, with applicable headings separated from
  empty sections and distinct ワンラ entries; these are not added to
  the twenty frozen captures or represented as byte-hashed captures.
- The author separately added five direct pairs after that inspection:
  both organization verbs/合う and /終了, and まもなく/たちまち.
  The complete entries and actual older bodies, not inherited
  exclusion chains, establish the merging, concluding and short-time
  overlaps. Thirteen additions bring declarations from 151 to 164.
- No shared actionable initial finding was established across either
  report's findings, optional suggestions, limits or row notes.
  Complementary contributions and very different evidence depths
  do not measure bias reduction or rank the models generally.
  Original-session confirmations remain pending; the batch is not closed.

## Batch 79 authoring observations

- N2:1562-N2:1581 map to eighteen articles: seventeen new articles and
  reused 巻く. The source aliases 交ざる/混ざる and 交じる/混じる
  share their respective pinned entry and reading, and are explicitly
  recognized in one canonical article for each pair.
- Actual pre-card inspection covers eighteen principal families / 50
  senses; thirteen selected family chunks / 306 families / 787 senses;
  three supplemental families / twelve senses; nineteen older-body
  chunks / 151 articles and five complete direct older articles.
  Distinct actual unions are 309 families / 799 senses and 156 older
  bodies. All 200 navigation labels, 22 complete components and three
  related kanji bodies were read; larger prepared availability is not
  actual inspection.
- A post-draft dictionary completeness check added four complete
  悪い/礼 matching families / seventeen senses. The final author union is
  313 / 816, while the original pre-card receipt remains unchanged.
  Separate にくい entries are not imported into 悪い/わるい.
- Twenty complete public captures come from one Digital Daijisen
  authority via Weblio. Applicable readings are separated from 枕's
  unrelated character heading, 混じる's こんじる entry and マスク's
  place-name/fragrance homographs. A returned wrapper is not frequency
  evidence or corroboration of every claim.
- Keep 蒔く, 撒く and 巻く as distinct まく identities. Usually-kana
  sowing/scattering, lacquer sprinkling, flyer distribution and losing
  a pursuer require sense-aware teaching, not a one-kanji-one-meaning
  partition. Preserve the reused 巻く title and existing exclusions.
- 本来 includes inherent and proper/rightful expectations, not merely
  past-time "originally." 毎度's familiar customer abbreviation and
  Hokuriku visiting formula are qualified separately. マイナス is not
  restricted to arithmetic, and a negative test is not necessarily bad.
- 曲げる is transitive ichidan; its physical senses are not freely
  written with rare 枉げる. Link the intransitive 曲がる to the existing
  stable 曲る article. まじる remains godan despite じる; dictionary
  混/交 tendencies do not create a strict liquids/solids distinction.
- Add four new primary reciprocal N2 pairs: 枚数/枚, 混ざる/混,
  混じる/混 and 混ぜる/混; recheck existing 巻く/巻. Missing character
  cards do not remove Han from word metadata.
- Independent initial GPT-6.1 Sol and Claude Opus 5.5 reviews are
  authenticated on the same authored commit. GPT supplies three adopted
  direct quiz pairs: 撒く/ぱらぱら and the two mixing verbs/付き合い.
  Claude supplies まごまご/ためらう, explicit expectation wording for
  本来, qualified 混ざる spelling guidance, and the missing プラス link.
  Its optional "interpretation" wording is adopted separately. There is
  no shared actionable initial finding across the complete reports;
  complementarity on this sample is not measured model-bias reduction.
- Initial actual frozen-family depths differ: GPT 313/816 and Claude
  25/79. Complete older bodies, including reused 巻く, are 159 versus
  two; navigation labels and front matter do not count as full bodies.
  Claude disclosed two parallel file-read batches inside its sole
  reviewer process. Reviewer processes themselves never overlapped.
- Post-review adjudication reads 25 complete families / 66 senses and
  twelve complete older bodies. Four newly inspected families / ten
  senses and two newly inspected older bodies bring the author's
  cumulative unions to 317/826 and 158 bodies, without changing earlier
  stage receipts. Separate readings and dance homographs are not
  imported into the assigned words.
- Four direct guards raise the assigned articles' declarations from
  106 to 110. Retain the directly justified scatter, combination and
  negative-aspect comparisons; do not infer other guards transitively.
  本来's revision makes an expectation explicit, not a universal claim
  that the earlier sentence was ungrammatical. 混/交 guidance remains a
  tendency rather than a categorical material/spelling law.
- Both original sessions confirm the accepted correction commit
  `fea8bc2e4234557b3ed0ccca4bb7f5af263c1985`: all twenty rows are CLEAN
  on all three facets, with no remaining actionable finding. Each
  freshly returns all 47 required complete files and the exact TSV
  scope; mandatory fresh dictionary union is 42 families / 123 senses.
  Cumulative reviewer family unions are GPT 317/826 and Claude 42/123;
  existing-body unions including 巻く are 160 and thirteen.
- Claude's confirmation discloses one parallel two-call read pair and
  one out-of-scope `.github` grep returning two agent-file snippets.
  Preserve these deviations, not a strict serial/scope-compliance
  claim; reviewer processes never overlap. File-return authentication
  establishes evidence access, not comprehension or semantic truth.
- Retain native reports unchanged. Claude's F02 shorthand refers to
  association in 1603920 sense 1 and 1603930 sense 2, not a nonexistent
  second sense of 1603920. Do not adopt its preliminary suggestion that
  a distinct thanks sense alone makes a frequency title safe: bare 度
  names an occasion/count; the repeated relationship needs its taught
  度に construction. Different constructions, not POS alone, support
  the final decision.
- Optional idiom/backlink expansion, a more explicitly named dictionary,
  a distinguishable-stones example revision and redundant-but-usable
  count wording are deferred. The 混/交 guidance is expressly a tendency;
  the current example is not established as an actionable defect.
  These twenty rows close without changing accepted teaching or the
  manifest after confirmation.

## Batch 78 authoring observations

- N2:1542-N2:1561 add seventeen articles and reuse 募集, 干す and 濠.
  Source 堀 maps to the same-entry, same-reading stable 濠 article; its
  existing N3 level, filename, primary spelling and title are retained.
  募集 and 干す gain sourced N2 levels. All existing exclusions remain;
  narrow additions and recognition passages are explicitly recorded.
- Before drafting, actually read twenty principal families / 45 senses,
  fourteen selected family chunks / 386 families / 903 senses,
  twenty-two complete older-body chunks / 173 articles, 267 navigation
  labels, 31 component records and six complete related kanji bodies.
  The complete 採掘 supplement adds one family / one sense and one older
  article: actual unions are 387 / 904 and 174 bodies. Larger prepared
  dictionary availability is not completed inspection.
- Twenty initial and two supplemental public captures come from one
  Digital Daijisen authority via Weblio. The initial 坊っちゃん return
  contains only the novel; 坊ちゃん and ぼっちゃん supply the lexical
  heading, yielding twenty-one positive lexical captures, not twenty-two
  independent confirmations. Historical headings and readings are not
  imported into the target senses.
- Create separate ほどく, entry1198900, rather than silently reusing
  解く/とく1198890. The shared spelling does not make all solving,
  dispelling or canceling constructions interchangeable. Recognize the
  separate intransitive ほどける without changing ほどく's transitivity.
- Respect 彫る's explicit ほる-to-彫る restriction and obsolete える;
  rare 雕る/鐫る are not generalized as ほる spellings. Likewise, 放る's
  search-only 投る is not an ordinary-production recommendation.
  北極 explicitly teaches the small っ in ほっきょく.
- Retain practical household 干す teaching while adding drinking-up,
  draining and usually passive work-exclusion recognition. Recruitment,
  contributions and financial subscriptions belong to 募集, but a call
  for applicants does not itself guarantee acceptance.
- 盆's household sense is unmarked in the complete family. Historical
  public examples do not establish modern rarity or obsolescence.
  Preserve that uncertainty without erasing household quiz neighbors;
  the practical tray/Obon focus does not mean the Chinese Lantern Festival.
- Four new primary reciprocal N2 pairs are 防犯/防, 牧畜/畜, 北極/極
  and 掘る/掘. Recheck existing 募集/募 and 干す/干 pairs. Preserve
  kanji metadata and unrelated teaching while adding useful reading-row,
  common-word links and applicable dictionary IDs.
- Quiz safeguards are direct, symmetric and nontransitive hypotheses,
  not category cliques. Consider ordinary secondary fields/aspects in
  方面, boy senses in 坊さん, canal in 濠, mining in 掘る and hidden
  faults in ぼろ. A related animal, building, festival, health measure
  or action is not automatically an equivalent answer.
- Exact-path checks, not unreliable negative glob results, establish
  missing cards. Do not create broken links to absent 坊, 朗, 牧, 保,
  健, 彫 or 盆 components, or absent お盆/トレー comparison articles.
  All primary written Han remain in word metadata.
- Author inspection and structural checks are not independent review,
  native-speaker certification, exhaustive quiz uniqueness or measured
  model-bias reduction. Initial reviews, full confirmations and the
  bounded two-endpoint reconfirmations are authenticated and complete.
- Initial review adds six direct pairs: 放る/止める and /中止,
  朗らか/愉快, 干す/無視, and ぼろ/穴 and /失敗. The applicable
  Daijisen headings explicitly recognize ignoring and failure; do not
  dismiss them merely because the shorter JMdict gloss differs.
  Corrective rereads cover twenty-one complete families / 77 senses and
  twelve unchanged older bodies, all already in the actual author unions.
- For 濠, distinguish source-alias preservation from production guidance:
  show 堀 in an example and identify it as the unmarked Daijisen heading
  spelling. Marked variants and priority tags are not measured frequency.
  Preserve 濠's stable identity and N3 rather than manufacturing a new card.
  For 彫る, explain material で separately from receiving surface に;
  the two existing examples should teach, not obscure, that contrast.
- Optional guard hypotheses need the same actual-label checks as findings.
  Retain ほどく/開く for undo/unpack and 方面/角度 for aspect/angle.
  Do not infer prevention/state, named-festival/category or active
  deprivation/subject's job-loss equivalence from a shared topic.
- Equal source access did not yield equal initial depth. GPT returned
  387 complete families / 904 senses and 174 existing bodies including
  the three assigned reuses; Claude returned 21 / 46 and four including
  those reuses. GPT supplied the six adopted quiz pairs; Claude supplied
  spelling and participant-marking clarifications. Compare all report
  sections before assigning unique credit, without ranking the models.
- A low-confidence Optional observation can become an adopted correction
  after direct evidence inspection. Claude's confirmation raises
  干す/放る: the public 干す entry explicitly gives ほうっておく,
  and the actual 放る title/body teach neglect and leaving someone alone.
  Add that seventh pair directly, not by inheriting the shared 無視 guard.
  The work/role qualification remains; it does not imply every loss,
  throwing or drying use is shared. Reconfirm the bounded change with
  both original sessions rather than treating prior clean verdicts as
  acceptance of an edit they had not seen. Both accepted it at the
  follow-up snapshot; final total: 105 declarations / seven added pairs.
- Full confirmations freshly returned 35 mandatory complete families /
  105 senses and twelve older bodies per reviewer. Cumulative existing-body
  identities are GPT174 and Claude16, including the three assigned reuses;
  unassigned counts are171 and13. The final bounded pass freshly reads
  two articles / two families / six senses, adding no identity, and
  explicitly inherits the other eighteen article and six kanji judgments.
  Exact returned-line authentication is not proof of comprehension.

## Batch 77 authoring observations

- N2:1522-N2:1541 add twenty new articles. All older word articles, including
  their identities, readings, titles, bodies and exclusions, remain unchanged.
  Ten primary reciprocal N2 pairs span eight kanji: 編集/編, 方角/角,
  防止/防, 方針/針, 包装/包 and 装, 法則/則, 包帯/包 and 帯, 包丁/包.
  Existing kanji metadata and teaching are preserved apart from these useful
  navigation additions and supporting dictionary entry IDs.
- Before drafting, actually read twenty principal families / 28 senses,
  eleven selected complete-family chunks / 307 families / 663 senses,
  seventeen complete older-body chunks / 133 articles, 267 navigation labels,
  34 component records and eight complete related kanji bodies.
  A narrow supplement adds three complete families / six senses and complete
  大きな, 別れ and 別れる bodies. The actual union is 310 families / 669 senses
  and 136 older articles, not all 497 prepared families / 1,083 senses.
- Twenty principal and two supplemental complete public lexical wrappers were
  inspected. They are one Digital Daijisen authority via Weblio, not twenty-two
  independent dictionaries. Keep historical びんしょ beside 便所 and ははき
  beside 箒 distinct from the target べんじょ and ほうき readings.
  The confusable inventory was read through line157 plus targeted relevant
  searches, not in its entirety.
- Normalize raw 庖丁 to prioritized common 包丁, keeping the same ほうちょう
  reading and entry1515530. Display 庖丁 explicitly as an alias, preserve every
  raw TSV field, and record the transformation rather than creating a duplicate.
  Primary reciprocal accounting uses written 包 in the chosen headword;
  recognizing an alternate spelling is not another new primary pair.
- 別々 needs explicit 別々に, 別々の and 別々な constructions. ベテラン concerns
  experience in a field, not necessarily military service. Search-only
  ヴェテラン/ヘリコプタ are not promoted to production alternatives.
  編集's editorial-committee use is not the opinion article 社説.
- 方角 includes a method/means sense as well as compass orientation.
  方針 concerns a guiding course, not simply a numerical goal.
  コース actually has a policy sense despite its route/course title.
  方言 includes grammar and vocabulary, not accent alone; 言葉 actually has
  a dialect sense. 坊さん's familiar boy sense is not erased by the monk title.
- Supplemental チェック sense4 explicitly includes investigating to prevent
  unsuitable entry. Therefore 防止 and チェック must not be declared
  categorically disjoint merely because the pinned English family foregrounds
  inspection. Preventing accidents still differs from merely inspecting them.
- 膨大 retains its swelling/expansion noun and intransitive する sense.
  Rare 厖大/尨大 belong to its adjective sense, directly corroborated by the
  supplemental public 厖大 entry. 広々's actual title is spacious/expansive,
  not an imagined extensive label. 法則 is not restricted to natural laws;
  方程式 includes the established figurative formula-for-success use.
- Draft guards are direct, symmetric, nontransitive hypotheses, not claims
  that all tool, dwelling, language, direction or mathematical categories
  are synonyms. 型's formula, 編む's compilation and ordinary secondary
  meanings require individual checks against the actual displayed labels.
  No native-speaker certification or exhaustive quiz-uniqueness claim is made.
- Missing component and comparison cards are not fabricated. Keep all primary
  written Han characters in metadata, including 箒, 荘, 鏡, 坊, 膨 and 丁,
  without creating broken links. Character associations are not etymology.
- Initial GPT review is clean; Claude identifies 包帯 construction coverage
  and an unclear spelling-mapping note. Positive 英辞郎/EDP entries support
  包帯をする and 腕に包帯をする. Lead with these noun constructions and
  包帯を巻く; retain JMdict's transitive verb as recognition, without claiming
  that it is invalid or less common. Missing スル markers do not prove either.
- Reconciliation rereads thirteen complete families / nineteen senses and six
  complete older bodies, all already within the actual 310/669 and 136-body
  unions. Add direct 方針/対策 and 膨大/広々 guards for broad strategy/course
  and extent labels, with the Japanese distinctions preserved. These originate
  in Claude's Limits, not its formal findings. Do not infer 包装/小包 or
  法則/支配 from package-related categories or English "rule" polysemy.
- Adopt three small prose clarifications and clarify the common-entry mapping.
  Defer an optional wasei note and stronger toilet-frequency claims.
  The compact `sense4`/`Sense2` source-note notation is not a mapping defect.
  `teachingSpelling` is present in the committed packet and records the source
  alias to recognize, not the canonical production headword.
- Two corrective frozen public returns are one additional 英辞郎/EDP authority,
  not two dictionaries. A separately inspected 精選版 日本国語大辞典 noun entry
  supplies no frequency evidence; the fresh Kotobank return did not expose
  the Daijisen definition. GPT's broader initial inspection and Claude's useful
  narrower observations show complementarity, not measured bias reduction or
  equal review depth.
- Both original sessions accept corrected teaching snapshot
  `a6e1243882b1393de5fabdf9bab9dff65449e4d5`, with all twenty rows CLEAN
  on correctness, scoped coverage and comprehensibility. Each returns all
  49 required native files completely, the exact header/twenty TSV rows,
  five evidence renderings and six older bodies, with zero edits.
  Fresh family union is 30 / 45 senses; no teaching or manifest edit follows
  acceptance. Cumulative older-body identities are 136 for GPT and six
  for Claude, not equal actual inspection depth.
- Correct the historical author's "unsupported" wasei characterization:
  the frozen JMdict 1121520 record explicitly carries `ls_wasei: y`.
  That supports a classification note from one authority; the note remains
  optional rather than a prerequisite defect. GPT also retracts its original
  overly strong endorsement of the removed bandaging collocation.
  Preserve original reports and supersede these claims explicitly.
- Claude discloses batching the twenty article reads and two older-body reads
  despite the serial-read prompt. The reviewer processes remained strictly
  sequential and exited; no required content is omitted. Keep the deviation
  visible rather than claiming perfect procedural compliance. An applicable
  dynamic ALC link is not replaced with an invented stable URL.

## Batch 76 authoring observations

- N2:1502-N2:1521 add twenty new articles. No older word identity, reading,
  title, body, exclusion or other metadata is changed. Five primary reciprocal
  N2 pairs are 文芸/芸, 分布/布, 分量/量, 並行/並 and 兵隊/兵.
  Each kanji gains one useful word link and its dictionary footer entry;
  complete previous kanji metadata and other body text are preserved.
- Before drafting, actually read twenty complete principal records / 36 senses,
  193 selected complete comparison families / 476 senses, 117 complete older
  articles in fifteen chunks, 242 navigation labels, 31 component records,
  five complete related kanji bodies and twenty public lexical captures.
  All selected chunks were read through their declared EOF, not just prepared.
- A bounded supplement adds six complete older-body reads: がっかり, 失望,
  しんみり, 良い, 軍 and 武士. Eight complete supplemental families / 18
  senses were read; one family was already prepared. The actual family union
  is 201 / 494 and older-body union 123. The larger 429 / 976 prepared union
  remains availability, not a claim that every family was read.
- The public captures are one Digital Daijisen authority via Weblio.
  Keep neighboring 文芸 magazine, 平野 names, historical 平気 calendar method
  and separate 凹む readings apart. Public numbering is not pinned JMdict numbering.
  The confusable inventory was read through line157 plus targeted relevant
  matches, not in its entirety.
- Preserve the raw source's misleading broad glosses. 兵隊's sailor does not
  mean any civilian seafarer; 隔てる's passive-looking shut-out gloss does not
  change its transitive ichidan grammar. No dictionary sense is independently
  assigned N2 merely by appearing beside a sourced row.
- 分量's measuring/weighing sense is qualified additional recognition, not an
  invented ordinary 分量する example. 分布's practical intransitive pattern
  does not establish an absolute ban on all transitive uses. 平日's radical
  sense belongs to ひらび, not source へいじつ; Saturday status is contextual.
- 文献 concerns reference sources rather than simply creative literature.
  Do not invent 献=document. 文房具 uses the 文房 writing-room association,
  not 房's tassel sense. These associations are not historical derivations.
- 並行 and separate 平行 can both concern concurrency. 臍 usually appears
  as へそ; the central-bump/depression sense has a reading restriction.
  Separate くぼむ does not inherit colloquial emotional へこむ meanings.
- Draft exclusions are independently reviewable pairwise hypotheses from actual
  labels and ordinary senses, not a transitive clique or a blanket POS rule.
  文章 style, 前後 context, 分ける sorting, 湿る dejection, 引っ込む recession
  and center/main-point meanings matter beyond primary titles.
  Supplemental しんみり is reflective/sentimental, not automatically dejected;
  武士 is not automatically equivalent to a modern soldier.
- Missing 隊/房/献 and other component cards are not fabricated.
  Component extraction covers BMP Han, not rare supplementary-plane 𦜝.
  Author reads and structural audits are not independent model review,
  native certification, exhaustive quiz uniqueness or measured bias reduction.

### Batch 76 initial-review reconciliation

- Both initial sessions are authenticated against `c1563f9c47fa9af139ef149893b4c5e4e9be3317`,
  with 35 complete required native file returns each and zero edits.
  Both original sessions accept corrected snapshot
  `228808f262a9503b525a4eac2fbe449611f4e58c`: all twenty rows CLEAN on
  correctness, scoped coverage and comprehensibility.
- Adopt six direct guards and remove the two stationery/tool-category guards.
  Clarify the noun-modifying による pattern, 隔てる participant roles, fountain
  title, 文芸 contrast and three small learner-facing prose points.
- Actually read eighteen complete corrective families / 36 senses and ten
  unchanged older bodies. Cumulative actual scope is 208 families / 514 senses
  and 129 older bodies; prepared availability is 431 / 981, not all read.
  Applicable Bunpro attachment guidance supplements the one frozen Japanese
  dictionary authority. Different-reading じまい remains distinct from しまい.
- Claude's comment that "be shut out" is absent from the source is contradicted
  by the preserved raw CSV gloss. It is not presented as a pinned JMdict gloss.
  Complete 平行 and くぼむ families resolve the reported ID-access limitation.
- Both reports identify 閉会/仕舞い. Their other useful observations differ,
  but scope and reading depth differ too; compare every report section and do
  not infer measured bias reduction or a model ranking.
- Both confirmations freshly read all twenty articles, five kanji, complete
  compact records and assigned TSV rows, four complete evidence renderings
  and ten older bodies: 48 authenticated required native file returns each,
  zero edits. The fresh family union is 41 / 84 senses. Cumulative older-body
  identities are 130 for GPT and eleven for Claude, not equal-depth inspection.
- Both accept the direct additions/removals and defer physical-closing guards:
  generic closing of openings/shop is not itself meeting/event completion.
  Other cards' guards do not create transitive obligations. Extra examples
  and wording polish remain nonblocking; no teaching/manifest edit follows acceptance.
- Preserve report-only errata explicitly: GPT misattributes Claude's raw-gloss
  claim to itself; Claude transcribes によるの分類 in its table although the
  actual article says 種類による分類. Do not rewrite native reports or teach
  the extra の. Claude withdraws its moving/proceeding mismatch and discloses
  simultaneous TSV header/row reads; reviewer processes remain sequential.

## Batch 75 authoring observations

- N2:1482-N2:1501 add eighteen new articles and reuse ふわふわ,
  initially adding only `jlpt: 2` to its previously unclassified header.
  That authored snapshot preserves its identity, reading, title, body,
  exclusions and image metadata; the correction below supersedes only exclusions.
  The twenty rows map to nineteen articles because 増やす and 殖やす
  share family 1602880 and one teaching page. Both original sessions accept
  `dd61b410bb42ab827708111fcf9fd0a347f927ce`: all twenty rows CLEAN on
  correctness, scoped coverage and comprehensibility; mappings, components
  and the exact permitted baseline correction assessed separately.
- Actual pre-card inspection covers twenty principal-row records,
  nineteen distinct families / 35 senses, 124 complete older articles,
  eighteen component records and twenty public lexical captures from
  one Digital Daijisen authority via Weblio.
  The older-body union is 123 articles in fifteen complete renderings
  plus a direct complete read of 次第, including its non-title program sense.
- The 315 comparison families / 780 senses are prepared, not all
  author-inspected. None of their thirteen renderings has been read.
  Principal families are included in those totals, not additional.
  The 187 original navigation labels are not 187 body inspections.
- After drafting, read complete supplemental 次第 family 1316680 /
  six senses, including order/program separately from its suffix uses.
  Actual principal/supplement union is twenty families / 41 senses;
  the expanded 316 families / 786 senses remain a preparation total.
- Preserve blank source spellings. Use kana ぶらさげる as the stable
  article and teach ぶら下げる explicitly. Preserve source 振舞う
  while recognizing full-okurigana 振る舞う. Treat 殖やす as a
  same-family rare spelling and asset/living-thing spelling tendency,
  not an exceptionlessly separate verb.
- Public sense numbering is not pinned JMdict numbering. 踏切's
  public athletic takeoff explanation supplements the pinned
  starting-line/scratch gloss; unrelated ブローチ cutting-tool,
  麓 character, and separate 風呂敷 readings are not imported.
- Distinguish freedom, price, freelance work and contextual abbreviations
  in フリー; its no-charge use does not grant every license permission.
  プリント distinguishes printing, a copy and a classroom handout;
  プログラム distinguishes an event plan, booklet and computer program.
  Actual ソフト software and 次第 program senses matter beyond titles.
- 仮名/かな is a contracted unit in 振り仮名. 風呂/ふろ is a
  lexical unit in 風呂敷, whose wago label does not establish the disputed
  historical origin of 風呂. Component associations are not etymological proof.
- No primary source character has an existing N2 kanji card, so this
  batch requires no new reciprocal N2 pair or kanji edit. Link existing
  lower-level components substantively; do not invent missing cards.
- Draft quiz guards are symmetric pairwise hypotheses grounded in actual
  labels and ordinary secondary senses, not transitive category cliques.
  Neither author inspection nor future model agreement establishes
  exhaustive uniqueness, native certification or measured bias reduction.
- Initial GPT and Claude independently identify the same pre-existing
  ふわふわ/ソフト softness gap. Add that direct pair and, after actual
  full-family/body inspection, ふわふわ/浮く and /浮かぶ floating pairs.
  This is an explicit baseline exclusion correction, not a regression
  from the level addition. Preserve the entire reused body and other metadata.
- GPT alone identifies excessive 風呂敷/包み and /包む exclusions.
  Complete applicable families distinguish the cloth, parcel and action;
  remove those two guards, retaining the substantive comparisons.
- Claude's quantity-coverage finding adds a contrastive 従業員を十人に
  増やす example beside 二人増やす: resulting total versus added amount.
  Its tentative 振舞う/接する suggestion is adopted for bare-title
  "treat people" ambiguity, without claiming unrestricted Japanese substitution.
- Adopt five bounded wording suggestions: dictionary spelling ぶら下げる,
  separate ブローチ homograph, unqualified ふろしき pronunciation,
  着る for ブラウス, and railway ホーム versus the home-related loanword.
  The public ふるしき heading says 音変化, not chronological primacy;
  correct the source note without rewriting the original frozen row record.
- Corrective reads cover ten complete families / 32 senses and six
  unchanged older bodies. All ten families were already prepared;
  actual principal/supplement/corrective union is 28 families / 70 senses.
  接する is one additional body identity, bringing the author union to 125.
- Native initial returns authenticate all nineteen articles, twenty
  mappings and assigned TSV rows, complete required evidence and zero edits.
  GPT reads 126 distinct unassigned older bodies / 145 total word bodies;
  Claude reads four / 23. Their actual depths differ despite equal access.
  Compare findings, optional notes, limits and row notes before crediting
  complementarity; the floating follow-through to 浮かぶ is the author's,
  not a new independent reviewer discovery or measured bias reduction.
- Both confirmations freshly reread the nineteen articles, complete
  compact records, assigned TSV rows, three full evidence renderings
  and six required older bodies: 37 authenticated complete required
  native returns each, zero edits. Cumulative unassigned older-body
  identities are 127 for GPT and nine for Claude, not equal-depth inspection.
- GPT withdraws inaccurate pinned-gloss and historical-reading shorthand.
  Claude retains medium confidence on cloth-guard removal and a
  low-risk, nonactionable English bare-verb-label qualification; its
  complete 軽い read does not justify equating weight with floating lightly.
  Preserve these limits rather than presenting agreement as certification.

## Batch 74 authoring observations

- N2:1462-N2:1481 add nineteen new articles and reuse 武士
  unchanged, retaining its sourced N2 level and all baseline metadata
  and body. Both original reviewers accept corrected snapshot
  `c14e72eb3c6ef596210363054f2b7d637b54b67e`: all twenty rows
  CLEAN on correctness, scoped coverage and comprehensibility;
  both kanji edits, mappings and preservation assessed separately.
- Preserve the four blank source spellings, source 附属 and its
  same-family alternative 付属. 不通 is not the homophone 普通.
- Actual pre-card reads cover twenty complete principal families,
  115 complete older articles, all 33 component records, two related
  N2 kanji bodies and twenty public lexical captures. The older-body
  union is 112 articles in fifteen complete renderings plus three
  direct reads: もぐもぐ, ぽつぽつ and 苦情.
- The 415 comparison families / 1,030 senses are prepared evidence,
  not a completed inspection claim. None of their seventeen complete
  renderings has been read by the author. Principal families are
  included in that preparation total. Original navigation labels
  cover 210 candidates, not 210 inspected bodies.
- After drafting, inspect complete supplemental もぐもぐ family
  2009920 / three senses, including mumbling, chewing and wriggling,
  with search-only katakana flags preserved. The actual principal/
  supplemental union is 21 families / 45 senses, not the expanded
  prepared union of 416 / 1,033. Keep the pre-card receipt unchanged.
- All twenty public captures come from one Digital Daijisen
  authority. Separate applicable modern lexical headings from
  historical readings, garment homographs, character entries and
  Buddhist terminology. Public numbering is not JMdict numbering.
- 夫妻 is formal reference to someone else's couple, not a polite
  self-reference. 塞がる is intransitive godan; 塞ぐ combines
  physical transitive uses with intransitive 気がふさぐ.
  ぶつかる is intransitive godan; ぶつける is transitive ichidan
  and can describe accidental impact, not only intentional attacks.
- Keep ordinary kana for ふざける/ぶつける. Rare ateji and
  search-only spellings do not become preferred production forms.
  ご無沙汰 acknowledges one's own silence; it is not necessarily
  an accusation or a general word for neglecting any task.
- 船便's primary ふなびん is kun-first mixed reading, stored
  as wago with the limitation explicit. Alternate せんびん is
  on+on. 吹雪 teaches whole-word ふぶき, not productive 雪=ぶき.
  部首 is an indexing radical, not every glyph component.
- Add primary reciprocal 符/符号 and reused 武/武士 links,
  preserving kanji headers. Missing 塞/無/沙/汰/襖/附/属/蓋/騒
  remain metadata/plain text, never invented cards or broken links.
- Compare each actual title and ordinary secondary sense, including
  complaints, low speech and simmering. Existing exclusions on a
  neighboring word do not protect a new pair. Treat draft declarations
  as hypotheses rather than pre-established reviewer findings.
- Initial independent reviews share two useful direct pairs:
  塞ぐ/覆う and 部品/アクセサリー. GPT additionally identifies
  five useful pairs involving fullness, covering, dejection and
  bubbling. Adopt Claude's optional ぶつぶつ/ささやく and
  /でこぼこ suggestions after full-body and family inspection,
  not by propagating speech/texture exclusions. Nine new direct
  declarations bring the nineteen new cards to 123 declarations.
- Claude leaves 地図の符号 unresolved. Replace that scene with
  モールス符号, explicitly attested in the applicable frozen
  Daijisen heading, rather than asserting the original was wrong.
  Keep 部品's source-backed accessories gloss but explain its
  equipment/component scope, not jewelry in general. Specify that
  misleading "nail on" belongs to the raw list, not JMdict 2742080.
- Corrective reads cover fifteen complete families / 44 senses and
  nine full older bodies. Actual family union becomes 32 / 76;
  prepared union becomes 423 / 1,051, still not all inspected.
  The unrelated ぷくぷく character family and separate きせる
  family are inspected but not evidence for the assigned lexical
  senses. Seven new older identities bring author coverage to 122.
  Keep historical preparation and pre-card receipts unchanged.
- Compare both complete reports, including optional suggestions,
  limits and per-row notes. Complementary observations are useful
  on this shared snapshot, not measured bias reduction or a model
  ranking. Both original sessions accept all consequential
  dispositions and adopted optional guards after fresh complete
  article/evidence reads. Confidence qualifications remain intact.

## Batch 73 authoring observations

- N2:1442-N2:1461 draft nineteen new articles and reuse 増える
  unchanged for source 殖える, preserving its N4 level, identity,
  reading, title, body and metadata. Both original reviewers accept
  the corrected snapshot `125bbe21d9696d59a99ee978efe01de8146ec6e3`;
  all twenty rows are CLEAN on correctness, scoped coverage and
  comprehensibility. Kanji edits and mappings are assessed separately.
- Preserve blank source spellings for ピンク and ファスナー and
  the source headword 瓶詰. Its alternative 瓶詰め is explicit;
  ビン plus voiced native づめ is mixed, not an all-on compound.
- Before drafting, read all nine family and eleven older-body
  renderings completely: 232 families / 512 senses and 86 older
  articles. Supplement with two complete ぷくぷく-request families /
  three senses and sixteen direct older bodies. The pre-card
  completion receipt records 234 families / 515 senses and 102
  distinct older articles. The unrelated Puku Puku character-name
  family is inspected but is not lexical evidence.
- Complete 町/清掃 reads occur after that receipt but before
  drafting; an additive receipt is persisted during drafting.
  Current author union is 104 older bodies, not a rewritten
  historical count. Twenty principals / 29 senses are included
  in the family totals. Read 127 original navigation labels,
  31 complete component records and all eight edited N2 kanji bodies.
  Labels, hashes and available files do not prove comprehension.
- Twenty inspected public captures come from one Digital Daijisen
  authority via Weblio. 含める uses the ふくめる heading, not the
  separate くくめる historical quotations. Explain the whole
  かんで含めるように construction; both 含む/含める are transitive.
- Distinguish color ピンク from additional erotic recognition,
  toy 風船 from its explicitly dated gas/hot-air sense, and public
  seasonal 更ける from an invented JMdict sense. ファスナー is
  not every English fastener; 便箋 is not every stationery item.
- 普及 has both transitive and intransitive する patterns.
  膨らます is an established transitive godan headword, not a
  misspelling to replace with 膨らませる. 膨らむ is intransitive;
  膨れる comparison tendencies are not absolute subject bans.
- 複数 is more than one, not necessarily many; 副詞 is not
  limited to modifying verbs. 不規則 does not automatically mean
  unethical rule-breaking, and 不潔 is not a neutral erotic label.
- Add nine primary reciprocal pairs across 瓶/詰/則/普/副/詞/複/含,
  preserving every kanji header. Missing 箋/殖/及/拭/膨/潔 remain
  metadata/plain text, not fabricated cards or successful body reads.
- Both reviewers independently catch the false "long vowel" in
  びんづめ and the missing 普及/流行る pair. Remove the false
  pronunciation instruction and add fifteen direct guard declarations:
  GPT-only eleven, Claude-only two, one shared, and one adopted
  Claude-only optional 拭く/乾燥 observation. The latter has explicit
  "to dry" in 1357240 and actual drying in complete 1209920.
- Compare expansion, intensification, unsystematicity and sympathy
  pairs against actual full titles and ordinary senses, not a
  synonym clique or a POS exemption. かわいそう's unfortunate
  title and full teaching matter even though the pinned glosses
  emphasize pity; the words are not unrestricted Japanese synonyms.
- Corrective inspection covers 21 full families / 49 senses,
  including four additional families / eight senses, and twelve
  complete older bodies. Current author union is 238 families /
  523 senses and 108 older identities. The separate すさむ reading
  in the extracted 進む family is not evidence for すすむ.
- Both initial native prompts, models, complete final messages,
  37 required full returns per reviewer, bounded TSV rows, required
  content-format range and zero edits are authenticated.
  GPT additionally returns all twenty comparison chunks and
  106 complete older bodies; Claude returns no such chunks and
  eight direct complete older bodies. Common access is not equal
  depth or comprehension. Useful complementary findings in this
  sample do not measure bias reduction or rank models.
- Other optional recognition/register expansion stays deferred.
  普及 already teaches 普及させる. No new mandatory claim follows
  from an unverified usage tendency. Initial reports remain unchanged.
- Both original-session confirmations run sequentially and read-only.
  Exact prompts/models/final messages, 51 fresh complete required
  native returns each, bounded TSV rows and the content-format range
  are authenticated. Each freshly returns all twenty assigned bodies,
  eight kanji, twelve older bodies and 21 corrective families.
  Actual cumulative complete older-body unions are GPT 109 / Claude 16,
  not author totals or evidence of equal comprehension.
- Both accept all original dispositions and the adopted drying guard;
  no new actionable defect is established. Confidence in marginal
  label guards remains qualified, not a guarantee of unrestricted
  Japanese synonymy. No teaching or manifest edit follows acceptance.
  Closure leaves 1,460 closed / 352 pending, no draft or unresolved rows.

## Batch 72 authoring observations

- Both original reviewers accept the final teaching snapshot
  `754578b2ffff7294b32a51fd11f3550421d4f140`, sequentially and
  read-only. All twenty rows are CLEAN on three facets; three kanji
  cards, mappings and baseline preservation are assessed separately.
  All 34 required fresh complete native returns per reconfirmation
  are authenticated. Six full reports and the bounded Claude addendum
  remain unchanged; GPT has three turns and Claude four.
  Actual cumulative complete older-body unions are GPT 122 / Claude 16,
  not author totals or evidence of equal comprehension.
  No teaching edit follows acceptance. Closure is 1,440 closed /
  372 pending, with no draft or unresolved rows.
- N2:1422-N2:1441 add nineteen articles and narrowly reuse 皮膚:
  only its sourced N2 field changes. Source blanks for ひゃっかじてん
  and ビルディング remain intact. 百科事典 is the recorded canonical
  encyclopedia spelling; 百科辞典 is the same word's alternative.
- Keep 平仮名 as the source-based identity, paralleling 片仮名, while
  explicitly teaching usual ひらがな. The raw "47 syllables" gloss
  is not a modern inventory rule. A script's spelling is separate
  from the origin of words written in it.
- Read ten complete-family and thirteen complete older-body chunks
  through EOF before drafting: 281 families / 640 senses and
  103 older bodies. 夜明け was also read completely before drafting.
  During drafting, inspect seven additional full families / thirteen
  senses and complete 字/文字 bodies. The union is 288 families /
  653 senses and 106 distinct older articles, not 106 navigation labels.
  Principals are included: twenty complete families / 39 senses.
- The completion receipt is persisted during drafting, not a
  contemporaneous pre-authoring gate. The original immutable
  preparation plan remains `prepared_for_inspection`. All 176 original
  navigation labels, 32 component records and three related kanji
  bodies were read; hashes authenticate bytes, not comprehension.
- All twenty public captures have inspected applicable lexical
  headings from Digital Daijisen via Weblio, one authority.
  日の出's satellite/music headings and separate 響き/どよめき and
  響く/どよめく readings are not substituted for the assigned words.
  The figurative English "come home" for 響く is not physical homecoming.
- Whole constructions matter: 頭を冷やす concerns composure;
  肝を冷やす concerns fright, not unrestricted bare fear synonymy.
  Cooling verbs overlap; a hot-versus-cold starting-temperature rule
  would overstate the distinction. Source 昼寝 is not home-only,
  表紙 is not front-only or paper-only, and ビルディング is not
  every English use of "building."
- 標準/基準 genuinely overlap. 標本 includes classic-example and
  statistical senses, not just preserved animals. 評論 is critical
  assessment, not inherently insult or an unfavorable verdict.
  Inspect ordinary secondary senses and actual displayed labels
  rather than creating synonym cliques from English keywords.
- 広げる/広める are not divided by an absolute physical/abstract
  boundary. 開く's older article also teaches ひらく; its primary
  あく title does not exhaust the comparison. 広さ measures extent
  rather than naming a region. 広々 needs its actual とした/する
  constructions, and 々 is not a separate metadata kanji.
- Primary reciprocal pairs are 皮/皮膚, 膚/皮膚 and 準/標準.
  Edit only 皮 and 準; 膚 already has useful links. Keep all primary
  written characters in metadata; absent 典 remains plain text,
  not a fabricated card or a successfully inspected body.
- Both blind initial reviews are now authenticated and archived,
  with 29 complete required native returns each and zero edits.
  GPT returned all ten family/thirteen older-body chunks; Claude
  returned none of them but five direct complete older bodies.
  Equal access is not equal depth or a controlled model comparison.
- Actual secondary senses matter in both directions: 響き's applicable
  influence/effect heading and 響く's vibration justify direct guards;
  both expansion verbs need their own 拡張/拡充 pairs.
  Conversely, beautiful/clean does not label beauty care, and a
  classic specimen/example is not automatically a standard or average.
- Do not copy an evening analogy to morning: 暮れ explicitly includes
  sunset/sundown; the inspected dawn families do not establish the
  same solar-event meaning. A failed English dictionary request is
  not evidence. Both final reviewers accept declining the dawn guards.
- At the first correction, 広げる's actual Daijisen dissemination
  sense and 伝える's complete propagation sense supported retaining
  that independently judged pair for confirmation, not inheriting a
  whole communication clique. The final actual-label judgment below
  reverses that retention without denying the Japanese overlap.
  Remove its 伝わる/宣伝 pairs; no generic POS exemption is used.
- Read sixteen corrective families / 31 senses completely; only four
  families / eight senses are new. Four further older identities
  yield author unions of 292 families / 661 senses and 110 older
  bodies. Two positive Seisenban inspections add one authority;
  short inspection notes are not full-page archives.
- Seven guards added and five removed, plus two precise footers and
  optional と guidance, change eight assigned cards only. Both
  original-session confirmations were then pending; historical initial
  findings are not rewritten into CLEAN acceptance. Other optional
  older-card link and 平仮名 guard work stays deferred.
- Comparing every report section shows complementary useful
  observations, not measured bias reduction or native certification.
- First confirmations are not acceptance. GPT discovers the older
  響く/伝わる omission; add that direct sound-transmission safeguard.
  Claude retains the 広げる/伝える objection on narrower displayed
  labels. Remove that pair while acknowledging genuine Japanese
  propagation overlap; "spread out" is not bare "spread." This reverses
  author retention and GPT acceptance, not either dictionary.
- Do not use a literary first citation as frequency evidence. Fresh
  Seisenban headings recognize both dissemination senses; Claude's
  bounded addendum withdraws rarity and no-overlap arguments but
  retains the lower-confidence actual-label objection. 広める/伝える
  stays independently supported. Both original reviewers now accept
  this precise distinction in their final reconfirmations.
- Authentication catches a fresh-read overclaim: Claude's first
  confirmation returned only fifteen principal families / 27 senses.
  Its separate original-session addendum returns all twenty / 39 and
  corrects the record; historical reports stay unchanged. Count
  45 of 46 complete required files in that confirmation, not 46;
  the missing rendering is supplied only by the bounded addendum.
- Four follow-up families / fifteen senses and two complete older
  bodies add no new identities: author union remains 292 / 661 / 110.
  Three positive Seisenban inspections add no third authority; another
  Cambridge HTTP 520 adds no evidence. Only two exclusion lines
  change, one added and one removed; 95 declarations remain.

## Batch 71 authoring observations

- Both original reviewers accepted the final corrections at
  `dfde68b7992b7151e5fd8ffa1eeaa26135f13a32`, sequentially
  and read-only. All twenty final rows are CLEAN on three separate
  facets; two kanji cards, mappings and baseline preservation are
  assessed separately with independent Git limitations. All six
  reports, exact prompts/models, 28/37/32 required complete returns
  per stage, bounded TSV reads and zero edits are authenticated.
  Actual cumulative complete older-body unions are GPT 180 /
  Claude 15, not author counts or overlapping reported totals.
  No teaching edit follows acceptance. Closure is 1,420 closed /
  392 pending, with no draft or unresolved rows.
- First confirmations at `73289715` did not close the batch.
  GPT found a new once-over/チェック label collision introduced
  by the first correction; Claude found the older unqualified
  all-parts/各地 collision missed in its blind review. Both are
  direct displayed-label issues, not unrestricted Japanese synonym
  claims. Add both safeguards only on 一通り, preserving its title,
  prose and all prior guards. No inspection or location clique is
  inherited. Both final reconfirmations accept the two remedies.
- Two complete follow-up families / eight senses and two full older
  bodies raise author totals to 479 families / 1,150 senses and
  174 older identities. Oxford's actual once-over heading supports
  the quick-looking-over label; its separate cleaning use is not
  evidence for チェック. This English authority is not a third
  Japanese dictionary authority. First confirmations and their
  non-CLEAN verdicts remain archived unchanged.
- Authenticated blind initial reviews used GPT-6.1 Sol and Claude
  Opus 5.5 sequentially on `88aea28d`. Both found the missing
  捻る/工夫 guard. GPT also found 捻る/考える and the inaccurate
  "native reading" description of 日にち; its optional 日日
  qualification prompted positive verification of a daily ひにち
  construction in a second authority.
- Claude uniquely found four other direct safeguards (転がす,
  おおよそ, 出入り, 著す), two unsupported spelling assertions,
  the missing いる component reading and an ambiguous "general pass"
  title. Adopted translation polish removes unsupported "main".
  Eight new articles are corrected; six direct guards are added on
  five of them. 一通り now uses "once-over" in its title. Existing
  guards remain; no older identity, title or exclusion is changed.
- Corrective inspection adds four full families / 27 senses and
  five full older identities: cumulative author scope is 477
  families / 1,142 senses and 172 older bodies. The complete new
  rendering contains eight families / 39 senses, including the
  distinct こうふ homograph of 工夫. Four positive corrective
  lexical inspections cover two dictionary authorities; two other
  Kotobank returns provide no usable lexical evidence. Stored
  corrective text is short inspection excerpts, not full captures.
  Original preparation, inspection and initial-review receipts
  remain unchanged.
- Native returns establish unequal initial depth: GPT returned all
  eighteen family and twenty older-body chunks plus the supplement;
  Claude returned none of those chunks but seven direct older bodies.
  Equivalent observations in findings, options and limits were
  compared before assigning contributions. Complementary catches
  were useful here, not measured bias reduction or model ranking.
  The first correction required a further pass, documented above.
- The optional 捻る/絞る edge is not established by their actual
  labels and complete families: whole idioms sharing "rack one's
  brains" do not automatically equate the bare verbs, and 捻る's
  animal-neck wringing sense does not establish cloth/liquid wringing.
  This is a claim-specific limit, not a proof of global quiz safety.
  Other optional spelling/recognition expansions stay deferred.
- Twenty new articles cover N2:1402-N2:1421. The raw source
  fields remain intact, including blank spellings for ひとまず,
  ひとりでに and ビニール. Canonical articles explicitly recognize
  引っ繰り返す, 引っ繰り返る, 引越し and 人差指 without
  copying a spelling restriction from one family to another.
- Raw 日日 at ひにち belongs to the date/day-count family 1611370.
  Its source gloss, "every day,daily,day after day," instead matches
  separate daily family 1602120 at ひび/にちにち. Preserve the
  mismatch as evidence and identify that distinction as pinned
  JMdict data, not a universal lexical ban. 精選版 日本国語大辞典
  separately records daily ひにち, especially 毎日ひにち /
  ひにち毎日. Recognize that construction without a frequency claim
  or unrestricted daily substitution. The compiler's intention is
  not inferred.
- Source 捻る's "puzzle over" gloss is taught through the actually
  attested whole construction 頭をひねる, not a fabricated unrestricted
  cognitive sense in JMdict. The separate ねじる identity and its
  shared spelling do not license every ひねる idiom or injury phrase.
  ビニール's vinyl-record sense is restricted to バイナル, and the
  public vinyl heading does not prove an exact borrowing route.
- Original completed author inspection covers 473 full families / 1,115
  senses, 167 distinct complete older bodies, 30 component records
  and two related kanji bodies. All eighteen family and twenty
  older-body chunks were read through EOF. The original 467-family /
  1,102-sense and 155-body preparation plan stays immutable.
  Two direct older-body reads preceded drafting; ten further bodies
  and six full families / thirteen senses were read during drafting.
  The completed receipt was persisted during drafting, not before it.
- All 22 public captures have inspected applicable lexical headings,
  from one dictionary authority. Mixed 瞳 character/satellite,
  独り言 book-title and 捻る reading headings are excluded where
  irrelevant. The 259-label union is navigation metadata, not
  259 fully read bodies; 92 original candidates remain unselected.
- Ordinary secondary meanings matter beyond older primary titles:
  通り has traffic, まず and しばらく have for-now uses, たいてい
  has an ordinary/negative use, and 暮れ includes sunset.
  These are direct-pair quiz hypotheses, not transitive cliques,
  global uniqueness proof or independent reviewer conclusions.
- 筆 gains reciprocal reading/common-word links for 筆記 and 筆者;
  皮 gains 皮肉. Both kanji headers are preserved, absent component
  cards stay unlinked, and primary metadata retains every written
  character. Authored draft coverage was 1,400 closed / 20 draft /
  392 pending; all twenty rows are now review-closed.

## Batch 70 authoring observations

- Both original reviewers accepted the corrections at
  `cced07e72cb5bc76192a2118fb47d8785a033d2e`, sequentially and
  read-only. All twenty final rows have three separate CLEAN
  facets; three kanji edits, mappings and baselines are separately
  accepted. Exact native prompts, models, four complete reports,
  assigned returns and bounded TSV access are authenticated.
  Actual cumulative complete older-body unions are GPT 146 /
  Claude 66, not author counts or overlapping report totals.
  No teaching edits follow acceptance; closure is 1,400 closed /
  412 pending, with no draft or unresolved rows.
- Authenticated blind initial reviews used GPT-6.1 Sol and Claude
  Opus 5.5 sequentially on the same committed draft. Both found the
  missing 引き出す/引き出し cash-withdrawal safeguard. Claude uniquely
  found 引き受ける/受け持つ and suggested aligning ハンドル's footer
  with selected senses 1-2 versus additional recognition 3-4.
  GPT uniquely identified the unsupported English borrowing route
  for ピストル and positively verified 引分 in a second authority.
- The correction adds both direct safeguards, cites the explicit
  Dutch pistool attribution, and sources 引分 without claiming
  present-day frequency. Claude's source-gap observation prompts
  a citation, but absence from its two inspected spelling lists
  does not disprove the separately verified heading. Complete
  1329640 adds one family/one sense: author totals are now
  388 families / 946 senses. Full 受け持つ and 引き出し add two
  older identities, bringing that union to 144; だます was a reread.
  Original prepared/completed receipts remain immutable.
- Native complete-return authentication found broader initial
  access than Claude's final scope statement recalls: fourteen
  whole family chunks (333 families) and seven older-body chunks
  (60 identities), not just targeted family searches/four chunks.
  Preserve the raw report and disclose the discrepancy; returned
  bytes prove access, not remembered comprehension. GPT returned
  all sixteen family/seventeen older-body chunks and the supplement.
  Equal access is not equal coverage or measured bias reduction.
- The optional 引っ掛かる/だます guard is not established by the
  actual titles and complete families: falling for a trick and
  actively deceiving someone describe opposite participants.
  This is a claim-specific judgment, not a blanket voice exemption.
  Keep the explicit contrast; no inherited exclusion clique.
  Other optional grammar/process/variant/link polish stays deferred.
  Both original-session confirmations accept these dispositions.
- Seventeen new articles and three reused identities cover
  N2:1382-N2:1401. Previously unlevelled ぴかぴか gains
  sourced N2; 引き出す keeps N4 and ぴったり keeps N3.
  Existing titles, primary readings, identity, assets and
  scene eligibility are preserved. Direct quiz additions to
  the latter two are explicitly enumerated in the packet.
- The source's ぴたり and teaching ぴったり share one family.
  Neither the blank source spelling nor blank gloss is filled
  with invented provenance. 引受る, 引返す, 引算, 引出す,
  引分け and 陽射 remain visible aliases, not new identities.
  Search-only forms are not promoted to preferred spellings.
- Completed author inspection comprises 387 complete
  families / 945 senses: 385 / 937 in sixteen full-family
  chunks and two additional families / eight senses. All
  seventeen older-body chunks were actually read through
  EOF, covering 139 identities; direct 合う, しっかり and
  降ろす reads bring the distinct full-body union to 142.
  Metadata-only navigation is not full-body inspection.
- All twenty principal records / 45 senses, 213 original
  navigation labels, 28 complete component records and three
  complete related kanji bodies were inspected. Three
  additional metadata records make the packet's label union
  216. Of 75 originally unselected navigation candidates,
  only 降ろす was subsequently selected; 74 remain unselected.
  The other direct supplements were outside that initial set.
- All 23 public captures were inspected: 21 applicable
  lexical headings from one authority, Digital Daijisen via
  Weblio. Raw 陽射 yields no lexical body and raw 引受る
  returns HTTP 404; neither failure verifies an alias.
  Canonical 日差し/陽射し and 引き受ける are separate
  positive captures. The collector now records a 404 as an
  explicit failed request without treating other HTTP errors
  as successful evidence.
- 日陰's sunlight sense belongs only to 日影/日かげ.
  日当たり's additional per-day sense is restricted to
  日当たり/日当り. Full-family membership does not remove
  spelling restrictions. 日差し metadata retains 日/差,
  not the characters of its alternative 陽射 form.
- 引き返す teaches modern intransitive turning back, not
  unrestricted modern transitive repetition or sending back.
  Public older literary senses genuinely include repetition,
  reversal and return: qualify them rather than calling the
  source gloss fictitious or asserting compiler intent.
- 引き算 follows 掛け算's native-first mixed-reading
  convention: ひき + サン, voiced ざん. Its `wago`
  field does not say both readings are native. The three
  reciprocal N2 pairs are 島/半島, 比/比較的 and 算/引き算.
  Missing 較/的/陰/卑/怯/肘 cards are not invented.
- ぴかぴか's finished-food use is children's language,
  distinct from ordinary shine or a polished clean plate.
  ぴたり/ぴったり additionally illustrates abrupt complete
  stopping. 引き出す adds bounded talent/information eliciting;
  public sense numbering differs from pinned JMdict.
- 引っ掛かる's splash recognition keeps the liquid as
  grammatical subject. ピストル and ビタミン are lexical
  teaching, not operational weapon or medical advice.
  Guard choices are direct author hypotheses for review,
  not cliques, universal substitutions or global uniqueness.

## Batch 69 authoring observations

- First confirmation found a further 張り切る/活力 energy
  competitor (Claude) and a mistaken 万歳 giving-up sense
  citation in the contributor disposition (GPT). Add the direct
  guard after full 1208480/older-body inspection and correct :4
  to :3 in the current disposition, retaining frozen history.
  Totals become 268 families / 716 senses / 106 older identities.
  GPT's accidental unassigned TSV read is disclosed and recorded
  alongside its successful corrected exact query, not erased or
  presented as exact-only access. Both original reviewers accepted
  the bounded followup at b0a8b14; all six native reports are
  authenticated. The final fresh assigned body is 張り切る,
  with nineteen words/four kanji explicitly inherited after
  author byte checks. Actual native older-body unions are GPT
  110 / Claude 29; these are not the author's comparison totals.
  Claude's final context had compacted its preceding report;
  native event history preserves its earlier complete judgments.
  Reviewer sense identification and author verification of the
  actual published disposition remain separately scoped.
- Initial GPT and Claude reviews ran independently and sequentially
  on the same committed draft, with authenticated actual model and
  complete-return evidence. Their access was common, but actual read
  depth differed; do not claim matched coverage or bias reduction.
  生き生き occurs in GPT findings and Claude's tentative note,
  while 切れ occurs in Claude's limits: contribution accounting
  includes all report sections.
- Reconciliation adds fourteen direct safeguards and removes the
  excessive judicial-person/sporting-official 判事/審判 edge.
  Complete family/body evidence supports actual fit, thriving,
  vigor, deposit/payment, giving-up and broken-piece competitors.
  Additional 張り切る vigor guards are author-derived, not
  invented reviewer findings or inherited exclusion cliques.
- Shorten 反映's title to "reflection"; keep computing application
  explicitly scoped and contrast 効く rather than presenting a
  general efficacy meaning. 張切る is attributed to Daijisen's
  actual heading, and unsupported はり切る attribution is dropped.
  Retain positively supported representation/address guards, not
  because excessive guards are harmless. Stable 印しるし does
  not acquire separate 印いん's seal sense.
- Six complete corrective chunks plus the two-family vigor
  supplement establish 267 families / 715 senses cumulatively.
  Full older-body reads establish 105 distinct identities;
  活躍 was a reread, not a new identity. Original prepared and
  completed receipts stay separate. The additional 活力 read
  raises final totals as above; both reviewers accepted the repairs.
- Twenty rows map to twenty new identities. Blank raw spellings
  for はめる, バランス, パンツ and バンド remain provenance.
  The kana-primary articles do not acquire alternative-spelling
  Han metadata. Existing cards and easier levels are unchanged.
- 歯磨き's source sense is toothpaste; brushing is additional
  recognition with its own construction. 歯磨き粉 is not
  necessarily dry powder. はめる teaches everyday fitting and
  wearing separately from its vulgar colloquial sexual use;
  the source's "make love" is not a neutral register guide.
- 跳ねる does not inherit hit/reject/behead senses from separate
  撥ねる/刎ねる identities. 早口 recognizes はやくち and
  はやぐち without mandatory rendaku. 流行る is godan,
  despite its final る, and its special whole-word reading is
  not an ordinary component-reading decomposition.
- 判子 preserves the source identity while teaching usual kana
  はんこ/ハンコ. The inspected public entry connects it with
  はんこう（版行）; its `kango` label follows that lineage,
  not an invented all-on reading or a literal judgment-child
  compound. Both reviewers accepted this scoped classification.
  万歳 does not add an unsupported ザイ reading to 歳.
- 払い込む is not restricted to personal savings or bank
  transfers. 払い戻す is not unrestricted debt repayment.
  バランス includes equilibrium and account balance without
  making every arithmetic 差し引き interchangeable.
- 張り切る's pinned family does not justify a blanket
  transitivity label. 反映 has both transitive and intransitive
  evidence; its representation/update constructions differ from
  反省's self-review and remorse. Shared English "reflection"
  is not a single Japanese sense.
- 判事 is a judicial rank/title, not every court worker.
  番地 is not universally sequential street numbering.
  パンツ recognizes both underwear and trousers without a
  rigid pronunciation rule. Bare source バンド does not prove
  which band sense the compiler intended.
- All primary written characters remain in metadata; missing
  component cards are not invented. Four reciprocal N2 pairs
  use matching reading-table and common-word links, preserving
  kanji headers and existing examples. Validation caught
  nonexistent guard ID 当てはめる: use actual stable
  あてはめる, whose complete older body was inspected.
- Completed author reads cover 249 complete families / 675
  senses, including twenty principals / 45 senses; 111 labels,
  91 complete older bodies, 35 complete component records and
  four related kanji bodies. Eleven family and twelve older-body
  chunks were read through EOF, covering 89 older identities.
  Supplemental full reads of 所 and 早い bring the union
  to 91, leaving 20 candidates unselected. Original preparation,
  completed inspection and supplemental receipts remain separate.
- All 25 public captures have applicable selected headings
  from one authority, Digital Daijisen via Weblio. Exclude
  unrelated Valence, Hanko, 班固, まんざい, はんす,
  bund, 礬土 and 晩材. Public everyday はめる evidence
  does not establish the sexual register; pinned JMdict does.
  Captured headings do not establish frequency, compiler intent
  or independent examination levels for all recognition senses.
- Quiz declarations are direct symmetric, nontransitive
  hypotheses based on actual older bodies and complete families,
  not inherited cliques or a proof of global uniqueness.
  Independent sequential GPT and Claude reviews are pending;
  inherited batch61 quiz debt is not silently expanded here.

## Batch 68 authoring observations

- Twenty source rows map to eighteen new articles and two reused
  identities. 花火 gains only sourced N2. 羽 keeps its N3 level,
  title, primary spelling/reading/characters and exclusions while
  explicitly adding 羽根 はね shuttlecock teaching. 放れる gets
  a distinct release-focused article; existing 離れる is untouched.
  Record `teachingSpelling: 羽根` for the spelling-restricted
  hanetsuki sense rather than falsely claiming it under primary 羽.
- Recognize raw 果して, 話合い, 話し掛ける and 話中 under
  their canonical spellings. The blank spellings for バック and
  ばね and the blank gloss for fullwidth ｘ remain provenance.
  The latter maps to the cross-mark name ばつ, not the Latin
  letter name エックス.
- 鉢's noun heading traces the vessel word to Sanskrit through
  鉢多羅. Its Sino-Japanese reading does not establish an
  ultimately Chinese origin or a metal-only vessel meaning.
  ばつ's proposed derivation from 罰点 is tentative in both
  inspected dictionary authorities. Review rejected the arbitrary
  kana-to-`wago` grouping. The correction explicitly makes `kango`
  provisional, following that possible connection, with an
  `etymology-uncertain` tag. This is not positive proof of settled
  historical type. Both original reviewers accept the qualified
  teaching, not a proven historical classification.
- 派手 is on-first mixed ハ plus て voiced で, following the
  existing 毎朝/台所 `kango` convention. 話し中 is native-first
  mixed はなし plus チュウ. Both carry `mixed-reading`;
  neither is described as a uniform all-on/all-kun formation.
- Preserve every primary written character even without a
  component card. The validator caught a nonexistent 派 link;
  leave that character plain rather than inventing a card.
  肌/肌着 gets both reciprocal table and common-word links.
  羽 retains its primary links; explicit 根/羽根 alias links
  do not invent a plant-root meaning or a component reading.
- Selected source 発想 teaching includes music expression as
  well as conceptualization. バック's ten-sense family does
  not assign a single transitivity to reverse movement and
  refunding. 発電's telegram sense is a contrast, not email.
  発売 establishes availability, not necessarily a discount.
- Actual existing comparisons matter: ボール includes bowl,
  バッグ recognizes irregular バック, ねじ includes a clock
  spring, シャツ can be outerwear, and 下着 is not restricted
  to the lower body. Do not erase these facets to simplify
  new titles or quiz decisions.
- Completed author reads comprise 398 complete families /
  914 senses, including twenty principal families / 46 senses;
  132 distinct complete older comparison articles, 228 labels, 31 complete
  component records and four complete related kanji bodies.
  All fifteen family and sixteen older-body chunks were read
  through EOF, accounting for 131 older identities. 示す was
  then read directly in full for a declared guard, bringing the
  union to 132 and leaving 96 candidates unselected. The initial
  completed receipt and original prepared plan are unchanged.
  Complete 毎朝 and 台所 were additionally read for the mixed
  classification convention, outside that comparison-body union.
- All 26 frozen public records and captured lexical text were
  inspected. Twenty-four nonempty extractions include one
  wrong-target raw ｘ response: only 23 requests are
  target-positive, while 話合い and 話中 are empty.
  Digital Daijisen via Weblio is one authority, not 26.
  A separately fetched Kotobank/Seisenban entry corroborates
  the tentative wording about ばつ; no saved response hash
  or inclusion in the frozen 26-request capture is claimed.
- These are author reads and direct symmetric, nontransitive
  quiz hypotheses. Both blind initial reviews are authenticated;
  both first confirmations resolve the original findings, and
  both bounded followup reconfirmations are accepted.
  Preparation, inspection and review receipts remain distinct;
  inherited batch61 quiz debt is not silently expanded here.
- Corrections add nineteen direct safeguards and remove the
  unsupported 発射/打つ edge. Modern 撃つ/射つ supplies the
  shooting identity; full 打つ teaches hitting/striking and other
  separate senses. Do not transfer meanings from a homophone.
  Add explicit departure/source を guidance for 放れる without
  changing its attested example or intransitive classification.
- Compare actual secondary facets as well as titles: 背 includes
  back/rear despite its height title; 案 includes an idea; 話 and
  話す include discussion; あまり independently recognizes
  affirmative excessive degree. Spring and busy guards protect
  context-free English answers without claiming Japanese synonymy.
- Corrective reads comprise 37 complete families / 108 senses,
  adding eleven / 30 to the original union: 409 / 944. Twenty-one
  full older comparison bodies add nine identities; separate full
  着る adds one, bringing the author union from 132 to 142.
  All six bounded corrective chunks were read through EOF.
  Original prepared and completed receipts remain unchanged.
- Authenticated initial GPT returns include all 31 family/body
  chunks and 23 additional direct older word bodies; Claude
  returns no such chunks and six complete older word bodies,
  three for classification conventions. Equal availability is not
  equal depth. Shared observations concern ｘ, the arbitrary
  type grouping and 甚だしい/過剰. GPT supplied other verified
  guard groups, the shooting-identity correction and departure を;
  Claude supplied 春 and 忙しい guards and useful optional
  wording/link improvements. This supports complementary catches,
  not measured model-bias reduction or a general model ranking.
- First confirmation kept the batch open: Claude identified a
  stale current `wago` source note and two further intensifier
  safeguards after GPT's CLEAN table. Update the current note and
  index checksum without rewriting frozen mappings or reports.
  Separate current contributor metadata from historical snapshots.
- Followup inspection adds specific 甚だしい safeguards for
  非常に, 極, ド and 超過, and バック/逆. Complete families and
  bodies establish the degree, excess and reversed-direction
  English-answer facets; these are not unrestricted Japanese
  synonyms, a shared-tag clique or transitive inference.
  Attribute fullwidth ｘ specifically to JMdict.
- Twelve complete followup families / 27 senses add seven / eleven
  to reach 416 / 955. Five full older bodies add four identities
  (ド was already read), reaching 146. Both compact renderings
  were read through EOF. The prior older-body chunks contain
  7 + 8 + 6 articles, not Claude's prose count of 7 + 7 + 7;
  exact native outputs govern accounting. Both original reviewers
  independently accept the five new safeguards and precise
  source attribution at `bb580c4`.
- Final reconfirmations freshly read three changed assigned
  articles, the current twenty mappings, complete principals and
  components, full patch, both followup chunks and exact TSV
  header/twenty rows. The other seventeen words and four kanji
  inherit the preceding complete-body judgments; author Git
  checks establish that those bodies are unchanged. Do not
  describe this as twenty-four fresh final article reads.
- All six native reports are authenticated. Required complete
  returns are initially 63 for GPT / 30 for Claude, then 35
  each and finally ten each. Native complete older-body unions
  across all turns are 152 / 30, including direct convention
  checks and without summing overlaps. These reviewer totals
  differ in scope from the author's 146 comparison identities.
- Both accept the direct 極 safeguard, but explain its basis
  differently: GPT emphasizes degree overlap; Claude emphasizes
  the displayed "very; extremely" title and qualifies JMdict's
  narrower "quite; very" gloss. Preserve that distinction rather
  than manufacturing unanimity about semantic equivalence.
  CLEAN accepts qualified provisional ばつ teaching, not a
  verified historical origin. No teaching changes follow final
  acceptance; optional expansion and unestablished guards remain
  deferred. The combined corrections add 24 direct safeguards
  and remove one unsupported edge across thirteen new articles.
- Final GPT prose overstates the 根/羽根 link location. It is
  a substantive Notes alias at `kanji/根.md:43`, with footer
  1171680 and a word-side 根 link, not a Readings/Common words
  pair. The preceding full-body report identified it correctly.
  Preserve both reports and verify the actual alias separately
  from the three primary table/common-word pairs; do not invent
  a new character reading or change accepted teaching.

## Batch 67 authoring observations

- Twenty source rows map to fifteen new and three reused identities.
  Both 量る and 測る reuse the existing N3 計る article, which
  already teaches those spellings. 始めに and 初めに share new
  はじめに. Preserve the raw blank spelling for ばからしい.
- Kana-primary はがす, ばからしい, はしご, はじめに and
  はじめまして explicitly recognize alternate Han spellings
  without adding those characters to their primary metadata.
  Source-primary 秤 and 斜 retain their actual characters;
  吐き気 retains 吐 despite its missing component card.
- Distinguish surface detachment in はがす from exposing the
  inside by removing an outer covering in むく, without an
  absolute split where uses overlap. The public raw 剥す lookup
  failed; canonical 剥がす succeeded. A failed surface lookup
  does not invalidate the pinned spelling or count as verification.
- Read the actual modern headword: 生える's historical おえる,
  挟む's さしはさむ, 梯子's ていし and 斜's しゃ are not the
  assigned readings. The rare はす example follows an attested
  construction, not an invented rare collocation.
- Keep 秤 as a weighing tool, 歯車's mechanical and figurative
  senses separate, はしご's venue succession distinct from a
  ladder, and 外れる's physical, off-target and exclusion facets
  explicit. A button that 外れる is undone, not necessarily torn off.
- はじめに recognizes both source spellings while qualifying the
  official-writing distinction; dictionary identity is not an
  unrestricted all-context interchangeability rule. The three
  public はじめに-form requests returned no selected lexical
  body and are not positive evidence.
- Actual author reads: 268 complete families / 703 senses,
  including eighteen principal families / 35 senses; 101
  complete older bodies, 177 labels, 27 component records and
  four complete related kanji bodies. All eleven family and
  thirteen older-body chunks were read through EOF. Seventy-six
  older candidates remain unselected; preparation and actual
  inspection receipts remain distinct.
- Twenty-six public requests produced twenty-two positive
  captures from one authority, Digital Daijisen via Weblio.
  Mixed readings, historical senses and unrelated headings
  are not silently imported. These are author inspections,
  not independent reviewer retrievals or frequency evidence.
- Quiz guards are direct symmetric, nontransitive hypotheses,
  not an inherited synonym clique. Independent initial reviews
  and original-session confirmations are complete. No global ambiguity,
  native certification or measured model-bias claim is made.
- Review corrections add nine direct safeguards, including the
  secondary rounds sense of 回る and humorous absurd-blunder
  sense of 傑作. Neither a narrow title nor a noun/verb distinction
  automatically removes competition from an actually taught facet.
  Conversely, shared "brush" wording does not make polishing or
  brushing teeth equivalent to sweeping away debris.
- Correct 吐き気's explanation to native 吐き plus on-reading け.
  Retain the app's existing native-first mixed-word `wago` grouping,
  checked in complete 場所, and add `mixed-reading`; do not
  relabel all mixed words as all-on compounds.
- Delete the unsupported exact-form 挾まる claim instead of
  turning incomplete evidence into a claim of nonexistence.
  Keep source-row provenance in contributor records, not the
  learner's explanation. A complete POS record marking both
  transitive and intransitive does not justify calling はしごする
  exclusively transitive.
- Corrective actual reads add eleven complete families / 35
  senses, nine / 31 of them new to the original union of 268 / 703:
  the union is 277 / 734. Eight full older comparison bodies
  contain seven additional identities. Complete 場所 and 磨く
  and unchanged kanji 気 were also directly read. Prepared
  plans and actual-read receipts remain separate.
- Compare observations anywhere in each report before calling
  them unique. Both models noticed タイプ, 種類 (tentative in
  Claude) and the old-character issue (optional in GPT).
  GPT contributed other quiz pairs; Claude contributed the
  mixed-reading correction, direct 挟む pair, learner prose and
  optional POS qualification. Actual comparison-read depth
  differed substantially; this is not measured bias reduction.
- Both original sessions accepted corrected `0aed71b4` without
  further teaching changes. Complete current rereads and both
  corrective chunks are authenticated for both models.
  The author older-word union is 109; actual reviewer older-word
  unions are 115 (GPT) and 13 (Claude), deduplicated across
  direct and reproduced bodies. Initial Claude read four older
  word articles plus kanji 計, not five word articles; use native
  returns rather than narrative counters.
- Confirmation caught a contributor-evidence citation slip:
  種類 is 1328890, whereas 1342050 is 巡る. The actual supplied
  family/body and both reviewers' classification judgments
  already used the correct record. Fix the contributor
  disposition without churning accepted learner content.
- Keep optional polish separate from defects. The remaining
  はしご source-reading phrase and 斜 repetition are nonblocking.
  Claude's later タイプ/一種 observation concerns an older
  pair outside this batch; retain it as a later quiz-audit
  candidate alongside, not a silent extension of, deferred
  batch61 debt.

## Batch 66 authoring observations

- Twenty source rows map to fifteen new articles and five reused
  identities. Preserve 乗せる, 伸ばす, 伸びる and 登る at their
  existing easier levels. のろのろ gains only the sourced N2
  field; its body, image and exclusions are unchanged.
- Shared dictionary identity is not enough for alias coverage.
  載せる must actually be taught under 乗せる, 延ばす under
  伸ばす, 延びる under 伸びる, and 上る under 登る. In particular,
  延びる's selected extension sense is restricted to that spelling,
  not primary 伸びる. The packet's explicit `teachingSpelling`
  records the taught alias used to check that restriction.
- Source 乗換 maps to the article explicitly teaching 乗り換え,
  乗換 and 乗換え at のりかえ. The source 鈍い のろい is distinct
  from existing にぶい; its raw knife-dull gloss is not imported.
  のこぎり, のろい and のんき stay kana-primary with empty
  character arrays. Recognizing an alias does not change that
  metadata or justify inventing a のろ character-reading row.
- 覗く has deliberate looking and intransitive partial appearance.
  載る's separate family covers publication and physical placement,
  not all of 乗る's riding senses. Preserve constructions and
  spelling restrictions rather than forcing one English gloss
  across every subject or grammatical role.
- 上り's train direction is relative to the designated route
  origin, not invariably Tokyo or uphill. Traditional 俳句 counts
  morae, not English syllables; its conventions have exceptions.
  糊's clothing starch is not every dietary starch. 這う includes
  snakes and trailing plants without a mandatory stealth meaning.
- 呑気 and 暢気 are ateji. The captured Daijisen origin note,
  not literal modern "swallow + spirit," grounds the type choice.
  The same carefree attitude can be favorable or irresponsible
  in context. Direct quiz guards remain review hypotheses;
  neither shared English labels nor different parts of speech
  settle every pair.
- Actual author reads: 257 complete families / 739 senses,
  including twenty principals / 72 senses; 111 complete older
  bodies, 165 labels, 31 component records and five complete
  related kanji bodies. Twelve original family and thirteen
  older-body chunks were read completely. Three supplemental
  bodies were read directly and 完全's one complete family
  separately; the prepared plans are not relabeled as receipts.
  Fifty-four original body candidates remain unselected.
- Twenty-three public requests produced twenty-two positive
  captures from one authority, Digital Daijisen via Weblio.
  The failed raw 乗換 lookup remains recorded; the canonical
  乗り換え lookup succeeded separately. Captures and author reads
  are not independent reviewer retrieval or frequency evidence.
  Independent initial reviews and original-session correction
  confirmations are complete. No linguistic certification,
  global quiz-uniqueness or model-bias improvement is claimed.
- GPT identified direct missing guards for 残らず/いちいち,
  残らず/皆さん, 売店/スタンド and バイバイ/それでは.
  Claude identified 乗り換え/接続 and /移す, the conversational
  バイバイ/じゃあ safeguard, and the unsupported 這う/伸びる
  guard. Accept the bounded changes, but keep contextual
  utterances and noun/verb constructions distinct.
- Claude's optional observations also prompted removing the
  覗く/見物 topic-only guard, narrowing 上り to the attested route
  starting point, and guarding バイバイ's parting use against
  送別. Printed production is not automatically publication
  appearance; broad overall scope is not omission-free
  distribution; comfort and slow leisure are not automatically
  a carefree temperament. Assess these individual facets rather
  than accepting every suggested extra pair.
- The じゃあ safeguard is contextual: its complete family
  records "well then," not an independent dictionary goodbye
  sense. The existing complete body teaches じゃあね at closing.
  A fresh Weblio fetch did not expose the standard Daijisen
  lexical body; unrelated dialect material is not confirmation.
  Keep the conservative guard without claiming that じゃあ
  and バイバイ are unrestricted translations.
- In confirmation Claude identified the separate existing
  じゃ card, whose complete body also teaches farewell.
  Add it to the same conservative closing-context safeguard;
  do not infer the pair merely from its shared title, an
  inherited さて edge, or dictionary-family membership alone.
  This was a missed initial candidate, not a regression or
  another blind model-comparison discovery. Both original
  sessions accept the final guard while retaining medium-low
  confidence that it is necessary. Distinguish じゃ's connector
  introducing farewell from the taught じゃあね closing.
- The cumulative author union is 268 complete families /
  766 senses / 122 older article identities, not reviewer
  coverage. Count actual full returned bodies and deduplicate
  direct reads and reproductions across turns. In particular,
  Claude's three complete extra first-confirmation returns
  remain complete evidence even though its report calls them
  partial. Both final twenty-row verdicts explicitly inherit
  unchanged judgments; neither confirmation adds fresh public
  retrieval. Preserve all six historical reports and the real
  nonblocking qualifications rather than rewriting earlier
  NEEDS FIX cells after resolution.

## Batch 65 authoring observations

- Twenty source rows need nineteen new articles, not twenty
  duplicate teaching identities. 寝間着, 寝巻 and 寝巻き share
  ねまき and the same nightclothes meaning. Explicitly teach the
  alias and separately verify 巻's two backlink locations;
  do not add 巻 to primary 寝間着 metadata.
- Preserve raw empty spelling fields and the 濃度 "brightness"
  gloss without importing unsupported luminance teaching.
  Source-selected senses and additional recognition senses
  remain separate from independent N2 sense assignments.
- Modern 女房 especially concerns one's wife. The inspected
  evidence does not justify an unqualified rough/old-fashioned/
  colloquial label. 睨む has modern examination, estimation,
  suspicious watching and consideration uses beyond an angry
  stare; select the actual にらむ heading, not historical ねむ.
- 煮る is liquid cooking, not every English "cook." Assess the
  direct boiling/cooking overlaps without inheriting the whole
  煮える guard list or erasing 炊く's regional qualifications.
  縫う has ぬって and potential ぬえる; its route-through-gaps
  sense is additional teaching, not literal sewing of a crowd.
- にわか has sudden and improvised attachment patterns.
  A bandwagon-fan use does not establish every recent fan's
  sincerity. Suddenness, immediacy, brief duration and grouped
  occurrence require individual meaning checks, not a copied
  clique of exclusions.
- 濡らす teaches the transitive make-wet construction and an
  explicit contrast to getting wet. ねじ's clock mechanism is
  not necessarily a fastening screw. For 捩る, use the correct
  ねじる reading; do not invent an injury collocation merely
  because the full family has a sprain sense.
- 熱する can be transitive or intransitive and can concern
  excitement. Do not require an object or boiling temperature.
  狙い is a noun, 狙う an object-taking verb; overlap with purpose,
  intention, hope and goal pursuit needs direct judgment rather
  than either blanket equivalence or a part-of-speech exemption.
- 年度's institutional year need not be a calendar year.
  Japan's government fiscal calendar is not every company's
  rule, and a school term need not be a full school year.
  農村's agricultural focus is not an administrative definition
  or a claim that every resident farms.
- 農産物 includes livestock products as well as plant produce.
  農薬 includes growth regulators, not only insecticides.
  Actual secondary senses matter: 針 includes sewing/needlework,
  薬 includes efficacious chemicals/pesticides, and 性能
  explicitly includes efficiency. Do not infer corresponding
  guards for every nearby tool, medicine, ability or effect.
- Actual completed reads: 232 distinct complete families /
  535 senses, including nineteen principals / forty senses;
  106 full older articles, 116 labels, 37 component records,
  four complete related kanji bodies and twenty matching public
  bodies. Eight main family chunks, ten main body chunks and
  five supplemental chunks were actually read through EOF.
  One supplemental family overlaps, 興奮. Ten original body
  candidates remain unselected. Prepared plans remain unchanged;
  a separate receipt records actual inspection.
- Public bodies represent one authority, Digital Daijisen via
  Weblio, not twenty independent dictionaries or reviewer reads.
  Original draft declarations remain historical. Blind initial
  reviews and both original-session confirmations are complete.
  No measured
  model-bias improvement or global ambiguity guarantee is claimed.
- Shared review finding: qualify modern 女房's register.
  The added Nikkoku sense supports a context-dependent somewhat
  disparaging tone, not an invariably insulting, obsolete or
  technically self-deprecating word. The original own-wife
  tendency was already taught; do not count it as a new omission.
- GPT uniquely found direct 考慮 and two heating guards.
  Claude uniquely found 嫁, raised a conservative wetting-pair
  guard and attachment question, and identified a possible kana
  frequency implication plus six missing substantive links.
  Compare all report sections: optical-density expansion is
  shared optional material, not a unique discovery.
- Do not overstate corrections. A direct 濡らす/ぬれる guard
  does not erase make-wet/get-wet or prove unrestricted
  interchangeability. Failed English-dictionary fetches supply
  no evidence. な/の are recorded; a historical の example does
  not establish modern frequency or prove an invented な
  collocation wrong. Use the recorded にわか雨 compound
  instead. Dictionary order and priority tags do not rank
  hiragana ねじ against katakana ネジ in ordinary usage.
- Corrective reads contain twelve complete families / 31 senses
  and five full older bodies. Four recaptured families include
  an already-inspected にわか雨: the deduplicated author total is
  **235 families / 540 senses / 109 older bodies**, not 236/541.
  Keep the original completed-inspection receipt unchanged.
  The two additionally inspected relevant Nikkoku definitions
  come from actual authenticated reviewer returns, not new
  author fetches or two independent dictionaries.
- Actual initial reading depth differs: both models returned all
  nineteen new articles, four full related kanji bodies and
  exact twenty source associations. GPT also returned all
  23 bounded evidence chunks; Claude did not read those chunks
  and directly returned only two full older articles. Title/
  exclusion scans are not full-body inspection. Equal access
  was not equal evidence depth; both contributed useful,
  complementary observations, not a measured bias reduction.
- Both original sessions accept the corrected teaching and all
  twenty mappings. The wetting guard remains conservative:
  Claude lowers confidence to medium and accepts borderline/
  optional classification. GPT independently retrieves American
  Heritage's explicitly transitive/intransitive "moisten"; the
  successful native return was checked, not merely its report.
  Three other GPT English fetches fail and add no evidence.
  Do not convert this resolution into a universal guard rule.
- Verify complete-body unions, not just path lists or counters.
  Initial GPT direct full reads have ten distinct bodies beyond
  the 106 reproduced ones: 116 total, not 106 plus eleven.
  After confirmation the actual older-body unions are GPT 120 /
  Claude 5. Both return the same twelve complete corrective
  families and five complete older bodies; inherited and fresh
  reads remain separate. Claude checks link destinations'
  existence/metadata, while GPT reads their six full bodies.
- 焼く's full dictionary family explicitly teaches heating,
  while its existing article foregrounds baking/grilling and
  burning/firing. Do not credit an old article with every
  secondary dictionary sense. Both reviewers accept the
  direct guard; expanding that older body remains optional.
- Batch closure changes only audit files and row statuses.
  There are no teaching or manifest edits after the final
  confirmed snapshot; optional preferences remain recorded.

## Batch 64 authoring observations

- Blind reviews found different useful gaps: GPT established four
  missing direct guards in two findings; Claude identified a
  title/body mismatch and source limitations worth narrowing.
  No initial actionable finding is shared. Both families are useful
  on this sample, not a controlled model-bias experiment.
- Match the quiz label to the actual secondary sense. "Really"
  competes with まさに and 実際; 本当's complete body also teaches
  本当に and conversational "Really?" The 本当 guard is less direct
  and conservative, not a claim that its noun identity is merged
  with the separate 本当に family. "Be cooked through" also fits
  焼ける's cooking-result sense despite different cooking methods.
- Narrow 憎らしい's title to "hateful; annoyingly good," matching
  its existing admiring example. Do not invent an affectionate
  collocation merely to make an English dictionary gloss concrete.
  Remove 匂う's unverified literary-register assertion and use kana
  におう for the figurative suspicion statement; retain the supported
  brightness/hint senses and literal-odor spelling preferences.
- Do not accept removal of both なかなか guards from the older
  article's narrow opening alone. Complete 1599420:4 has excellent/
  wonderful/very good, without rare/obsolete marks; an actually
  returned Kotobank Nikkoku 中中 body also records favorable
  evaluation. Retain conservative direct guards without claiming
  unrestricted substitution or measured modern frequency.
- Authenticated initial returns show unequal evidence depth:
  GPT read all 250 family records and 130 complete older baseline
  bodies; Claude returned one complete 20-family chunk, the twenty
  principals, a targeted アメリカ record and eight complete older
  baseline bodies. Both body unions include the three reused
  assigned articles; comparison-only counts are 127 and five.
  Both returned all 23 assigned/related bodies. GPT exposed one
  additional TSV row, N2:1282, without using it as review evidence.
  Equal access is not equal actual reading depth.
- Corrective evidence adds five complete families / 13 senses and
  three full older bodies, yielding 255 families / 569 senses and
  104 author-inspected older bodies. Two successful matching
  Kotobank bodies are the same Nikkoku authority; their empty
  Daijisen headings do not count as additional inspected entries.
  Both original sessions subsequently accepted the actual corrections.
- Authenticate actual complete returns, not just requested paths.
  Each confirmation returned all four changed bodies, unchanged 憎い,
  twelve complete families / 31 senses, five full older bodies,
  the patch, snapshot and public receipt. Both also returned the exact
  header/twenty TSV rows without a neighbor. Cumulative distinct
  complete older bodies are GPT 131 / Claude 13, including three reused
  assigned articles; comparison-only counts are 128 / 10.
- Claude withdrew the なかなか removal finding as actionable after
  reading the full secondary sense and independently fetching the
  matching Nikkoku body. Keep its residual conservative-guard
  preference rather than forcing identical confidence. Both models
  actually fetched 中中; GPT also fetched 匂う and 憎らしい.
  These are one Nikkoku authority, and historical examples do not
  establish contemporary frequency.
- Preserve optional alignment separately from defects: 憎's ironic
  "darling" wording is dictionary-backed, and an affectionate example
  must not be invented to make it concrete. The unchanged source
  note's literary-brightness annotation is not verified register
  evidence for the corrected article. Distinct full titles alone
  are not a general quiz-safety rule for 上手い/上手 or other pairs.
- Preserve the existing unlevelled 憎む, にこにこ and 鈍い articles;
  only add `jlpt: 2`. Exact checks found no matching form/reading
  in the four lower-level source TSVs. The fifth vocabulary TSV
  is N2 itself, not a fifth lower-level source. Keep にぶい distinct
  from the later のろい row and preserve にこにこ's empty raw gloss.
- Separate unexplained motivation in なんとなく from overcoming
  obstacles in 何とか, and extreme degree in なんとも from its
  negative anything/at-all construction. Negative 何とも言えない
  can genuinely express an inability to judge or say.
- A matching modern public dictionary entry explicitly includes
  liquid boiling for 煮える. Food is a useful default example, not
  an exclusive semantic boundary. Explain the intransitive
  food-or-liquid が construction rather than teaching object を.
- 匂う and 臭う have spelling tendencies, not an absolute pleasant/
  unpleasant partition. Inspect the modern heading separately
  from historical lower-bigrade material. The whole family also
  includes brightness and hints; additional recognition teaching
  does not acquire an independently established N2 label.
- 憎い and 憎らしい both allow ironic positive evaluation.
  Do not impose a fixed intensity hierarchy or infer quiz guards
  from the neighboring hatred clique. Full positive secondary
  senses of comparison words matter as well.
- 南米's 米 refers to America, not rice or the southern USA.
  Verify the actual アメリカ family, 1149830, before attributing
  historical 亜米利加; do not guess a plausible entry number.
- Daily necessities can be durable. A 日課 can be personal,
  customary or assigned, not only a school lesson. Actual
  lexical overlap, not category membership alone, must decide
  guards against goods, tools, work and habit labels.
- 日時 includes appointed date/time and elapsed days/hours.
  Attribute 日程's selected-date teaching specifically to the
  matching Digital Daijisen entry. Inspect カレンダー and both
  ダイヤ families instead of inheriting a scheduling guard clique.
- Turbidity, contamination and danger are not equivalent:
  pollution can be invisible and harmless cloudiness is possible.
  入社 is becoming a company's employee, not daily office arrival.
  Escaping, releasing and failing to catch also require direct
  constructions rather than automatic participant-role exemptions.
- Completed evidence is separate from unchanged preparation plans:
  **250 complete families / 556 senses**, including twenty principals
  / 37 senses; **101 complete older bodies**, **158 actual labels**,
  **23 component records**, three complete related kanji bodies and
  twenty matching public captures. The original 149 candidate labels
  do not mean 149 inspected bodies: 92 were read, 57 remain unselected;
  nine further complete bodies came from supplemental candidates.
- Twenty captures mean one authority, Digital Daijisen through
  Weblio, not twenty independent dictionaries. Initial quiz
  declarations were author hypotheses; final dispositions are
  independently reviewed bounded judgments, not proven equivalences.
  Structural checks do not prove linguistic correctness or global
  quiz uniqueness; inherited batch61 quiz debt remains deferred.

## Batch 63 authoring observations

- Both blind reviews identified なせる業's false potential analysis.
  A successful direct Kotobank 為せる lookup explicitly confirms
  the older perfect/resultative construction in two named dictionaries.
  A modern potential listed on a verb page does not analyze every
  homographic expression.
- GPT uniquely found two direct explanatory guards with なぜなら;
  Claude uniquely found 生意気's mixed-reading misdescription and
  馴れる's inaccurate description of the preserved older body.
  Both read all 337 family records, but complete older-body returns
  differ: GPT 153, Claude three. This supports complementary value
  on this sample, not a model ranking or measured bias reduction.
- Do not remove guards merely because an older article foregrounds
  another sense. Complete 打つ1408810:11 and 作る1597890:14 have
  doing/carrying-out and committing senses without obsolete/rare
  marks. Both original reviewers accepted retaining the guards with
  為す; Claude withdrew the removal finding as actionable and retained
  weaker confidence for 作る. Acceptance is not equal confidence.
- Both confirmations accepted the actual five-body correction.
  They returned six complete older comparison bodies; GPT's split
  chunk required exact per-line and full interval verification.
  Cumulative actual older-body depth is GPT 154 / Claude six.
  Do not convert supplying a file, a requested range or a claimed
  read into successful complete returned evidence.
- A neighboring だって exclusion is not proof of either new causal
  pair, even when a reviewer describes an inconsistency. Keep the
  direct complete-family/body reasoning for each なぜなら guard.
  Weak optional guards remain qualified, not mandatory equivalences.
- Keep raw source evidence separate from adopted teaching. The empty
  なだらか gloss does not invalidate the word. Source 何分 is なにぶん,
  not the separate minutes question なんぷん; retain the raw erroneous
  minutes gloss in the audit packet rather than teaching it.
- Shared dictionary membership is not proof of existing coverage.
  N4 慣れる teaches accustomed use, not the specifically selected
  tame-animal sense. Add bounded 馴れる without rewriting that identity
  or pretending that tameness and biological domestication are identical.
- Preserve kana source identities なぐる and なにしろ while explicitly
  teaching 殴る and 何しろ. Primary metadata follows the primary spelling,
  not every written variant mentioned in the body.
- Read matching public headings, not everything returned by an endpoint.
  Modern 殴る, なす and fruit-bearing なる must be separated from unrelated
  classical headings. Twenty positive Weblio captures here represent one
  authority, Digital Daijisen, not twenty independent dictionaries.
- Original and supplemental captures share one three-sense family:
  the inspected union is 337 complete families / 815 senses, not 338 / 818.
  The 151 complete older bodies are disjoint across the two captures.
  The final 224 labels include 90 recovered from those complete bodies.
- Use an actual reputation construction, 名投手で鳴らした, instead of
  inventing 評判で鳴らす from an English gloss. Assess ordinary complaint
  senses against 訴える and 文句 as well as literal sound labels.
- Guard declarations are author hypotheses, not review verdicts.
  Gentle slope, gradual change, smooth surface and gentle tone need
  individual comparisons; a neighboring exclusion does not prove an edge.
  Earlier batch61 inherited quiz debt remains outside this batch.

## Batch 62 authoring observations

- Blind initial reviews caught different gaps: GPT identified
  additional selection, gathering, catching, healing and duration
  quiz pairs; Claude identified drawn-out-action pairs and the
  linked material reading 綿 (めん). Claude's optional selection
  observation overlaps GPT's finding and is not credited as a
  wholly GPT-unique discovery.
- Inspect complete comparison families as well as older openings.
  抜く includes selection/extraction and capture; 収穫 includes
  fishing catch/haul. コレクション includes collecting as an
  activity, not only an assembled collection. Direct quiz guards
  do not teach unrestricted substitution among these words.
- Usually written as 治す is a preference, not a hard spelling
  restriction on 直す's medical sense. Keep the practical spelling
  contrast without dropping the direct guard. Align ナイロン's
  cotton-material link with めん, without claiming わた cannot name
  a cotton plant or padding.
- Authenticated native returns show unequal initial source depth:
  GPT read 92 distinct complete older bodies, Claude five.
  Both read all 24 distinct assigned word/kanji bodies. Different
  useful catches support retaining both families here, not a
  model ranking or a measured reduction in bias.
- Both original sessions accepted the committed corrections with
  no actionable defect remaining. Preserve their real confidence
  difference: Claude considers some catching/yield guards and
  捕る/抜く conservative or weak, while GPT supports them from
  secondary senses. Acceptance is not equal confidence, and an
  unmarked dictionary sense alone does not prove unrestricted use.
- Confirmation receipts verify seven complete changed bodies,
  nineteen complete families/77 senses and eleven complete older
  bodies per reviewer. Cumulative actual older-body unions are
  GPT 94 and Claude 12; unchanged judgments inherit actual initial
  reads. A truncated or selectively inspected derivative is not
  counted as a complete read.
- Check actual returned source IDs, not just requested TSV paths.
  GPT's first confirmation search returned four following rows
  outside assignment; an exact reread followed. Record this
  disclosed exception rather than claiming perfect row-scope
  compliance or crediting the extras as review coverage.
- Preserve source 捕える as a stable identity while explicitly
  teaching 捕らえる/捉える and the reading とらえた for 捕えた.
  A joint spelling heading establishes recognition, not exclusive
  physical/mental spelling compartments or measured frequency.
- Keep raw source glosses and selected teaching separate:
  治す2856318 teaches medical cure/heal, not the repair/correction
  senses of 直す1599390. Reuse 永い through the actual temporal
  teaching in N5 長い, not spatial sense1 or a new duplicate card.
- Two spellings need not make two articles: 中身/中味 share
  なかみ1599430; 中味 is ateji. Preserve all primary written
  components in metadata, including 身 despite its missing card.
- A dictionary's search-only spelling flag is not a complete
  usage rule. Sense-local notes and the public heading explicitly
  recognize 採り入れる for adoption and 穫り入れる for harvest.
- Catching is not confined to living targets: 捕る's complete
  sense includes baseballs. 採る also covers collecting insects.
  Training is not sport-only, and prolonged duration is not
  obligatorily negative or deliberately caused.
- The twenty positive public lookups are all Digital Daijisen
  via Weblio, not twenty independent authorities. Preserve the
  actual completed reads separately from unchanged preparation
  plans; byte-bounded supplemental renderings avoid confusing
  character limits with tool-output byte limits.
- Quiz declarations remain author hypotheses until independent
  review. Reassess full secondary meanings and both answer
  directions; neighboring training, learning, duration and
  interior exclusions do not establish transitive cliques.

## Batch 61 authoring observations

- Same-spelling navigation can find a different lexical identity:
  the pinned N3 解ける1198910 row does not establish melting
  溶ける1546070 at N3. Record exact form/reading/family adjudication
  without rewriting the original broad navigation capture.
- Reusing a kana identity does not require changing its kanji array.
  床屋 is already taught under とこや; preserve that N4 identity and
  add the substantive 床 link and backlinks to its actual path.
  Reuse 跳ぶ only because the unchanged 飛ぶ body actually teaches it.
- Preserve lexical overlap rather than imposing tidy compartments:
  特色 can emphasize an outstanding point; 特長 normally highlights
  merit; 特徴 is not restricted to good features.
  Public どなる includes loud calling as well as loud scolding.
- Separate dictionary scope from compiler intent. The exact public
  とまる heading includes fixed-in-place recognition and historical
  remaining senses beyond pinned1310620. That does not make its
  raw fixed/abide/stay source gloss wholly erroneous.
- Record completed body reads separately from captures. Correcting
  an overescaped title-navigation regex yielded further candidates,
  not retroactive proof that the original navigation was complete.
- Full comparison records can overturn title-only guard removals:
  利益 has advantage, 味噌 has a good-point use, and 入る/良い/いい
  have readiness senses. Check the exact kana identity too.
  Preparing something and the preparations being ready are not
  automatically the same meaning; neighboring guards are nontransitive.
- A joint spelling heading supports recognition, not per-sense
  frequency. Clarify possible 留まる/perching spelling without
  claiming that 止まる is common in that use. Teach the attested
  fixed-in-place example separately from とどまる.
- Authenticate returned bodies, not scope lists: initial native
  complete older-body returns establish GPT 116 and Claude four,
  despite many more search/header accesses. This limits comparisons
  of model contributions and does not measure bias reduction.
- Record genuine inherited findings without silently expanding a
  batch into baseline repairs. 飛ぶ/飛行 and 止まる/止む remain
  uncorrected pre-existing quiz debt, not batch regressions.
- Recheck the actual label field before citing a usually-kana flag.
  Claude's resumed review caught an author-evidence error: entry
  2850084 has empty `misc`, spelling-info and reading-info fields.
  The kanji heading's mark and an unlisted jōyō reading do not
  themselves measure spelling frequency. Retire the unsupported
  "usually" claim instead of defending it with a different proxy.
- Confirmation findings are not blind-initial discoveries. The same
  sessions can validate a small retirement of an unsupported claim
  without rerunning twenty unchanged judgments. Preserve the
  historical assertion and reports, append its explicit supersession,
  and verify the actual returned revised body, patch and source.

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

- **Batch 60 reconciliation:** Reading restrictions apply to
  comparisons too: physical よける cannot be attributed to the
  existing さける card merely because both use 避ける.
  Actual complaint, assigned-role, financial-loss and special
  adjective senses establish seven direct guards; neighboring
  exclusions do not establish the optional 義務 pair. Modern
  kerosene teaching can retain its scope while qualifying the
  oil contrast: the public とうゆ heading itself includes a
  broader lighting-oil sense. Link existing comparison articles
  at their substantive use, including a fuel/appliance contrast.
  Both models contributed useful findings, with authenticated
  complete older-body counts of GPT 102 and Claude four;
  partial reads are not complete reads, and unequal depth does
  not measure model bias or establish a model ranking.
  Both original sessions accepted the bounded corrections.
  Corrective rereads give cumulative distinct older-body counts
  of GPT 103 and Claude fourteen, including Claude's additional
  訴える read; do not simply add twelve to each initial count.
  Claude withdrew the optional 義務 guard after full evidence.
  Further physical/transitive よける polish remains nonblocking.
  Preserve the public lighting-oil definition without inventing
  a historical date or frequency claim that its source lacks.

- **Batch 60 authoring:** A shared written 退く does not
  merge どく, のく, しりぞく and ひく; respect the
  のく-only restriction on resigning/retiring. Keep actual
  additional senses visible: 溶かす can concern financial
  loss, 溶く can mean beating eggs, and 尖る extends
  beyond a physical point. Mixing flour is not necessarily
  chemical dissolution; clear/transparent does not mean
  hygienically clean. 石油 and オイル have explicit
  kerosene senses, so comparison cannot stop at their lead
  petroleum/oil labels. Preserve unlevelled どきどき's
  teaching while adding its exactly sourced N2 label only
  after checking lower-level indexes. A failed greeting
  endpoint remains failed; captured counts and complete
  physical-line reads must not be conflated with rendered
  logical-record counts or independent verification.

- **Batch 59 reconciliation:** Actual complete families and titles,
  not neighboring guards alone, establish the direct pairs. 採点
  also names the assigned score; 転がる has a static scattered
  sense beyond rolling; 揃う has a uniform-state sense. Broad
  signal, speed and manner labels can need guards without making
  their Japanese constructions interchangeable. Conversely,
  copper's membership in the metal category does not by itself
  justify an exclusion. Attribute 動作's raw "manners" gloss to
  word lists instead of pointing to an invisible learner-facing
  antecedent. Both models found useful shared and complementary
  observations; GPT actually read 112 complete older bodies and
  Claude 11. These unequal depths do not establish a model
  ranking or measured bias reduction. Both original sessions
  accepted all bounded corrections. Complete corrective rereads
  give cumulative distinct older-body counts of GPT 113 and
  Claude 16, not the initial counts plus twelve each. Fresh
  Kotobank 採点 retrievals support the result-noun sense;
  failed or irrelevant public returns do not count as verification.
  No further consequential defect was established. A pre-existing
  アンテナ wording observation remains explicitly outside scope.

- **Batch 59 authoring:** Preserve a source error without teaching
  it: 統計's supplied entry means statistics, not the raw
  scattering/dispersion gloss. Keep same-reading 点々 and 転々
  as distinct identities, and do not generalize scattered or
  intermittent appearances into unrestricted gradual improvement.
  Distinguish current in amperes, power in watts and energy over
  time. A reading sound change in 天皇 or 電波 does not create
  a new unrestricted constituent reading. Deduplicate comparison
  evidence: 210 original families/478 senses plus 33 support/86
  overlap at one family/three senses; one additional AC family/two
  senses yields 243 distinct families/563 senses, not their naive
  sum. These are author observations, not independent findings.

- **Batch 58 closure:** Both original reviewers accepted the same
  bounded corrections and exact twenty all-three-CLEAN mappings.
  Preserve native reports while separately clarifying arithmetic
  slips: 22 assigned bodies minus four changed leaves 18 unchanged,
  not 16. Corrective rereads of 成長/揃う do not increase either
  reviewer's distinct older-body count. The global reciprocal audit
  counts new articles only; validate a reused article's required
  reading-row and Common words pair separately instead of
  inflating that audit's expected count.

- **Batch 58 reconciliation:** Assess direct completeness and
  development guards from actual complete families and older
  bodies, not parity with a neighboring exclusion list alone.
  Both reviews identified 展開/成長, the rare 鉄炮 qualification,
  and 手頃's incomplete sense citation; their different severity
  labels do not make those unique discoveries. Claude additionally
  supplied 出来上がる/揃う and a useful separation of character
  meanings from pronunciation. Actual complete older-body reads
  differed substantially: GPT 117, Claude 10. Complementary
  observations helped this sample, but do not measure model bias
  or establish a general ranking.

- **Batch 58 authoring:** Resolve actual public cross-references,
  such as 展開's computing sense pointing to 解凍, before claiming
  corroboration. Mixed headings can contain unrelated readings
  (鉄橋/鉄灸, 伝記/しるしぶみ, 手前/てめえ); preserve the
  selected family and register. A loose source gloss may have a
  dictionary-related basis without being valid as a general
  translation: 出来上がる's "by definition" must not become an
  unrestricted adverb. Native-first mixed 手帳 follows the actual
  荷物/豚肉 classification precedent; state the kun/on split
  rather than calling both readings on. Preserve stable kana-only
  でこぼこ when adding 凸凹 recognition. Captured comparison
  chunks are not inspected merely because files exist; record
  actual completed reads separately from preparation status.
  These are author observations, not independent findings.

- **Batch 57 closure:** Both original sessions accepted the same
  committed corrections after complete bounded rereads. Authenticate
  actual successful returned content, not just requested file paths,
  and verify the exact twenty final all-three-CLEAN associations.
  Count repeated reads separately from distinct older bodies:
  Claude's ten reading occurrences covered nine distinct articles.
  Keep optional contextual contrasts and weak English-polysemy
  hypotheses separate from consequential unresolved defects.
  Complementary observations were useful on this sample, while
  unequal comparison depth prevents model rankings or measured
  bias-reduction claims.

- **Batch 57 reconciliation:** An existing Common words link does
  not prove that a required reading-row example is present; check
  both surfaces explicitly at the actual whole-word reading.
  Dictionary spelling restrictions apply to the listed family, not
  every Japanese source, and missing spellings must not be invented.
  Distinguish noun + をする from a direct する construction in the
  explanation even when both examples are correct. Use actual
  ordinary secondary meanings, not neighboring exclusions or
  English polysemy, to adjudicate lowering, stopping and matching
  guards. A useful clarity improvement need not mean that the
  original qualified construction was false. Count overlapping
  evidence by deduplicated families, senses and actual complete
  bodies; retain unequal reviewer read depths and pending
  confirmation rather than claiming review closure.

- **Batch 57 authoring:** A failed raw-alias endpoint is not
  dictionary verification; preserve its failure and separately
  inspect the canonical entry. A thin cross-reference such as
  定休日 needs its referenced 定休 body for the relevant claim.
  Keep unrelated readings/headings apart, including 強気's
  つよき and 停止's restricted ちょうじ sense. Loose predicative
  source glosses do not change 出来上がり's noun status.
  Direct public usage can supplement a source-specific POS label
  without licensing unrestricted substitution. Preserve stable
  easier-level identities when adding explicit source variants.
  These are authoring observations, not independent review findings.

- **Batch 56 closure:** Both original sessions confirmed the same
  corrected snapshot after full bounded rereads; authenticate all
  four native reports, required complete reads and twenty exact
  all-three-CLEAN associations before closing. Claude withdrew two
  neighbor/same-root-based hypotheses after reading complete actual
  comparisons. Shared findings include the variant-component gap
  even though one report called it optional. Other Claude proposals
  supplied useful direct guards and precision, not evidence for a
  model ranking. Keep one-service public captures distinct from
  pinned JMdict, and do not generalize a noun/predicate shorthand
  into an exemption for a word with actual する uses.

- **Batch 56 reconciliation:** A same-root noun/verb precedent is not
  a rule that every related noun and predicate need an exclusion.
  Inspect actual senses: a connection or assigned role is not
  automatically connecting or performing the role. Conversely,
  生産's actual manufacture use, 苦心's taking pains, physical
  squashing and a congested state support direct guards even when
  labels or word classes differ. Neighboring edges prove neither
  inclusion nor exclusion. Check optional hypotheses as well as
  formal findings; both models noticed the rare-spelling link gap,
  so its different severity labels do not make it unique to GPT.
  A full blind source derivative is not a substitute for reading
  old bodies, and reviewers must retain unequal actual scopes.

- **Batch 56 authoring:** Distinguish a wrong supplied identity from a
  genuine separate-entry alias. The 務める row points to 勤める-only
  1240825; teach inspected 2872052 while preserving the raw source.
  By contrast, 点ける 1610400 explicitly crossreferences 付ける's
  lighting sense and can be recorded as a validated source alias.
  努める's copied employment gloss does not override its effort meaning.
  Test transitivity per sense for 突っ込む, and do not generalize
  浸ける soaking to 漬ける-only pickling. Existing coverage can require
  no article edit: 漬ける already teaches the complete selected source
  association. Level-only reuses are not whole-article reauthorings.
  The source's "glaze" for 艶 must not become a claim about glazing
  material. These are author findings; shared and complementary
  model contributions are recorded separately in the review ledger.

- **Batch 55 closure:** A first confirmation can expose a small
  regression; retain its NEEDS FIX verdict and obtain another bounded
  confirmation rather than treating it as clean. Authenticate all six
  native reports and the exact twenty all-three-CLEAN final associations.
  Both original sessions accepted the functioning-versus-acceptance
  clarification and four more guards, while qualifying the declined
  work-noun/passing-through hypotheses. Keep inherited judgments,
  fresh reads, author checks and optional baseline work separate.
  Complementary findings are useful sample evidence, not a model ranking.

- **Batch 55 confirmation:** Adding a synonym comparison can introduce
  a comprehension gap even when its dictionary sense is correct.
  Explain operating/having an effect versus an excuse being accepted,
  and place a non-substitution warning after the comparisons it qualifies.
  A reviewer's invented starred sentence is not independent evidence of
  universal ungrammaticality. Recheck optional guard hypotheses against
  complete actual meanings: spatial reaching, efficacy and unqualified
  interpret labels support four more pairs; operation nouns and explicit
  passing-through activity do not by themselves establish validity or a
  physical passageway. Additional evidence counts must be deduplicated.

- **Batch 55 reconciliation:** Bare English labels can remain
  ambiguous across Japanese lexical distinctions: interpretation,
  work, spread out, passage and currency need direct pair checks.
  Existing guards are not transitive. Inspect whole older bodies
  and ordinary secondary senses before adding or rejecting a pair;
  explicit untidy-state wording is not automatically an active
  scattering answer, and a valuable occasion is not necessarily
  an incidental opportunity.

- **Batch 55 reconciliation:** Explain same-spelling つく/つつく
  with the actual readings and light/repeated-poke tendency,
  without claiming that つく excludes a light poke. Attribute
  1456895:1-2 separately as recognition, not another N2 source row.
  Gloss サ変 in plain English and connect the classification
  warning to practical 通じ- forms. Attested に and で constructions
  do not establish unrestricted particle substitution.

- **Batch 55 review limits:** Compare all report sections, including
  tentative optional hypotheses, before crediting unique discoveries.
  GPT read 96 complete older comparison bodies; Claude read four,
  not the author's 120. Claude's disclosed broad `.github` search
  also surfaced two unassigned agent files; do not describe that
  as perfect scope compliance. The unchanged 月日/日月 explanation
  remains a separately recorded baseline limitation.

- **Batch 55 authoring:** A blank raw gloss does not authorize
  reconstruction of compiler intent. Explicit 通ずる/通じる
  crossreferences support bounded recognition in the existing
  primary-reading article; keep source and teaching identities
  separate and validate each. JMdict's alternative-ずる label does
  not by itself settle the public サ変 conjugation description.
  Preserve the easier N3 article level.

- **Batch 55 authoring:** Count twenty source principal families
  separately from the extra reused teaching family; both belong
  inside, not on top of, the inspected union. Complete supplementary
  金銭, 銅貨, デート and 先 evidence adds six distinct families
  and four old bodies. Verify manually entered cross-entry citations:
  点く overlaps the lighting sense of 1495740付く:9.
  Mixed public headings do not supply every homograph's meaning.

- **Batch 55 authoring:** Retain source aliases visibly without
  duplicating articles. Hygienic ちり紙 is not arbitrary decorative
  tissue; 通貨 need not be cash; 通勤 is not every kind of work;
  付き合う need not be romantic. A directional 突き当たり may
  allow a turn. Godan 散る has 散って and 次ぐ has 次いで.
  Incidental ついで attachment differs from sequential 次いで;
  attribute the latter's separate lexical identity.

- **Batch 54 closure:** Authenticate all four complete native reports
  and exact twenty-row all-three-CLEAN associations before closing.
  Both original sessions accepted the corrections; Claude withdrew
  the English-control guard and revised the primary-title-only
  argument against secondary-sense protection. Preserve those
  revisions rather than treating initial findings as authority.
  Do not turn an unverified starred counterexample, a category-tag
  search or a part-of-speech difference into a universal lexical
  rule. Close the sourced example improvement without claiming
  that its predecessor was proved ungrammatical. Author counts,
  actual reviewer reads and inherited judgments stay distinct.

- **Batch 54 reconciliation:** Ordinary 汚い/ぐしゃぐしゃ
  untidiness needs direct protection with 散らかる; indirect guards
  are insufficient. Look beyond exact filenames: 醤油 has a
  kana-primary しょうゆ article. Inspect individual condiment
  meanings and before/prior-to uses, rather than deriving exclusions
  from shared tags, category cliques or the matching after-side pair.
  An unnamed mimetic contrast is clearer when named and linked.
  Prefer the actual attested spatial 直前 construction over an
  unverified alternative; this does not prove the old example wrong.
  Shared English control alone does not establish that 支配 can
  replace 調節 in level adjustment. Preserve ordinary secondary-sense
  protection even when an older title foregrounds a different sense.

- **Batch 54 authoring:** A raw numbered gloss does not determine
  pinned sense divisions: 長所's strong point/advantage is one sense.
  Conversely, チョーク's chock is supported by a separate complete
  homograph family, not by inventing a second chalk sense or treating
  the mixed raw gloss as wholly unsupported. Public chalk/choke
  headings do not independently verify chock. Deduplicate supplemental
  families by identity before reporting inspected evidence counts.

- **Batch 54 authoring:** Keep practical tendencies distinct from
  universal rules: 調整/調節 overlap, eldest daughter/son need not
  be the first child overall, through service need not be nonstop,
  and DC magnitude need not be constant. A vertex survives rotation;
  everyday elongated-rectangle language must not silently prohibit
  the inclusive mathematical square case. Public spatial 直後
  recognition needs its own attribution rather than a fabricated
  pinned sense. Actual storage and ordinary tip/disorder secondary
  meanings require direct checks, not topic cliques or indirect guards.

- **Batch 53 closure:** Both original sessions accepted the exact
  corrected snapshot, four direct guard additions and existing 酸性
  link; validate all twenty final source-ID/article associations and
  all three verdict facets. Resolve an initial UNVERIFIED public-backed
  qualification by reading the actual complete heading, not by silently
  inheriting CLEAN. Both models revised bounded initial judgments;
  Claude explicitly corrected its archaic-entry rationale. For an
  identical two-model confirmation prompt, use absolute attribution
  or neutral "one reviewer" wording throughout, rather than a relative
  "the other reviewer" that points differently for each reader.

- **Batch 53 reconciliation:** A modern expression and a bare
  dictionary form are not interchangeable evidence: archaic 徐々
  1345600 does not establish modern 徐々に, whose own complete
  1595480 family independently supports the direct overlap.
  Physical tip 端/はし and 末/すえ, and geographical ベルト,
  require actual secondary-meaning inspection, not English-label
  matching or indirect guards. Link an existing substantive
  comparison such as 酸性. Compare all report sections and record
  unequal evidence depth before attributing value to model diversity.
  The shared audit counts reciprocal pairs for new word articles
  only: retain 240 tracked pairs and check reused 超/超過 separately,
  rather than reporting 241 under the wrong counting definition.

- **Batch 53 authoring:** A raw loanword row can span separate
  dictionary identities: チップ's tip and chip meanings require
  1077740 and 2850287, not fabricated senses of one entry.
  Blank raw glosses and misleading English "sterility" stay preserved
  separately from supported teaching. Exact calendar 中旬 is the
  11th-20th, not arithmetic thirds. Do not turn a useful 縮む/
  縮れる contrast into absolute nonoverlap when the inspected public
  entry also records curled hair. Deduplicate supplementary full-family
  and old-body rereads before reporting inspection totals.

- **Batch 52 closure:** Both original sessions accepted the same committed
  correction with twenty exact all-CLEAN three-facet associations. Keep
  revised initial judgments visible: GPT accepted the sound/headache guard
  removal, and Claude accepted the qualified causative-label distinction
  after comparing the same-English-verb 開く/開ける precedent. A borderline
  editorial judgment is not automatically a consequential unresolved
  defect. Preserve optional expansions without changing confirmed teaching.
  Counts distinguish sixteen old word bodies from the additional 魚 kanji
  card and deduplicate against earlier actual reads.

- **Batch 52 reconciliation:** Secondary senses can require direct guards
  despite unlike titles: クラス has rank/category use, 粗 has personal
  flaws, and 審判 includes judgment beyond sports officials. 一つ does
  not transitively protect 一, and short-poem teaching needs its own 詩
  comparison. Inspect excesses too: causative bring-close/let-approach
  labels distinguish 近付ける from approaching labels here, while
  がんがん's actual sound/headache title does not answer powerful/
  reassuring merely because a secondary use describes vigorous work.
  ギョ is 魚's ordinary on reading, not a voicing change. Link substantive
  comparisons using actual filenames, including 押入れ to 押し入れ.
  Record model-unique contributions across all sections and actual read
  depth; equal evidence access is not equal inspection or bias reduction.

- **Batch 52 authoring:** Allocate source senses by the actual raw
  gloss, not first dictionary sense: 単数's singular-number anchor
  and 力強い's reassurance anchor are both sense 2. Conversely,
  近々's raw nearness/before-long gloss supports both senses, while
  its spatial sense excludes alternate きんきん. A 炭坑-only shaft
  sense must remain spelling-restricted rather than becoming an
  unrestricted 炭鉱 definition. Distinguish geological 地質 ちしつ
  from the separate fabric-quality じしつ identity in mixed public
  headings. Missing 淡/誓 cards do not justify dropping written
  characters from metadata. Explicitly record failed exact-family
  extraction such as 近日中; removing a request is not verification.
  These are authoring observations, not independent reviewer findings.

- **Batch 51 closure:** Both original sessions accepted the second
  correction on the same committed teaching snapshot; both final tables'
  exact source-ID/article associations and three CLEAN facets were
  checked, not just row counts. Preserve the first confirmation's
  NEEDS FIX rows as history alongside final resolutions. Further
  optional rapid-progress/momentum candidates did not establish a
  mandatory guard or justify editing correct teaching merely to
  accommodate an ever-growing neighbor inventory. Native reports
  remain unmodified; author counts come from deduplicated actual
  inspections, not a reviewer's retrospective scope shorthand.

- **Batch 51 confirmation follow-up:** Confirmation is not a formality:
  Claude caught two original omissions after accepting the first fixes.
  一度に's unqualified "all at once" label can collide even though its
  full teaching distinguishes grouping from suddenness. おどおど's
  actual hesitant-behavior title/body and complete dictionary sense
  support a direct ためらう guard. On the same candidate sweep, the
  author adopted optional さっさと for prompt/immediate action, rather
  than dismissing it because it lacks a sudden-surprise sense.
  Distinguish this exact-label/practical-use judgment from automatic
  cliques: qualified simultaneous 一斉 and efficacy/legal-force 効力
  remain unadopted. Refresh stale current source-note assertions while
  preserving frozen historical evidence. First all-CLEAN confirmation
  from one model does not close another model's new NEEDS FIX findings.

- **Batch 51 reconciliation:** Actual secondary senses exposed missing
  direct guards despite distinct titles: すっと includes suddenness,
  重なる includes accumulation, and ぐずぐず includes hesitation.
  The precise untidy/slovenly senses, not wet "sloppy" alone, support
  だらしない comparisons. Inspect noun/adverb constructions rather than
  dismissing 一瞬 by part of speech; its existing article explicitly
  teaches rapid-result 一瞬で. The author's follow-up also found
  reasonable/valid 立つ sense 13 for 妥当, separate from the optional
  and unadopted building-standing comparison. Model-diverse reviews
  supplied complementary required pairs, but GPT read 116 old bodies
  and Claude only three: equal access is not equal actual depth or a
  controlled measurement of model bias.

- **Batch 51 authoring:** Preserve erroneous raw glosses in the source
  index without teaching them: ダム is a dam, not "dumb"; 建つ is
  intransitive despite the source's "to erect." Normalize 溜息 to
  ため息 while explicitly recognizing the source spelling. 足袋 is
  learned as the complete word たび; do not invent individual
  足=た or 袋=び readings to manufacture reciprocity. Failed or
  irrelevant Kanjipedia retrievals do not verify that classification.
  A separate 貯 spelling for financial saving does not establish
  an absolute money/nonmoney spelling boundary for 溜まる/溜める.

- **Batch 50 reconciliation:** A source gloss that explicitly includes
  bamboo and the middle rank calls for both 竹 senses in the selected
  mapping, not a plant-only anchor with additional rank teaching.
  Distinguish a modern school subject from exercises: obsolete 体操/PE
  evidence does not justify suppressing the modern 体育 contrast.
  Conversely, Digital Daijisen's ダイヤグラム entry includes the
  operating schedule itself, not only its drawn representation; judge
  スケジュール and 時間割 directly rather than relying on their
  existing indirect links through ダイヤ. Independent reviewers found
  complementary issues, with unequal actual comparison-body reading depth.
  Claude's confirmation then misassigned four source-ID/article labels despite
  correct substantive reads. Preserve that report and its same-session corrected
  addendum; check each final verdict's exact source-ID/article association against
  the pinned mapping, not merely twenty source IDs and CLEAN cells.

- **Batch 50 authoring:** Preserve recognized rare aliases without promoting
  them to preferred spellings: source タイア maps to タイヤ. Keep additional
  public-dictionary uses separate from pinned sense numbering:
  ダイヤグラム has one JMdict sense, even though Digital Daijisen separately
  describes transport operating charts. A successful mixed-heading capture
  is not evidence for every homograph it contains.
- **Batch 50 authoring:** Inspect actual additional teaching as well as a
  primary header: 表 has primary おもて but explicitly distinguishes
  ひょう/chart in its body. Record that separate identity rather than
  claiming it is the primary reading. Likewise, assess continuous
  どんどん and all-times いつでも without indiscriminately excluding
  every frequency word. Regional 炊く and archaic 滝 senses retain their
  qualifications; noun evidence for 田植え is not a suru-classification.

- **Batch 49 reconciliation:** Inspect direct new-new transitivity pairs
  as well as old comparison labels. 揃う/揃える share matching/completeness
  answers despite their different argument structures. Broad labels
  can also hide concrete overlaps: 作る includes preparation, 量 includes
  physical volume, and グランド has a grand/large modifier identity
  separate from the sports ground. Conversely, comparative ずっと is
  not automatically absolute "very"; its actual Daijisen heading and
  old article justify removing that overly broad 大層 guard.
  Do not infer copying or transitive reasoning merely from similar lists.
  Replace the awkward それた道 illustration with an actually attested
  construction rather than inventing another contrast. Equal reviewer
  access did not yield equal actual reading depth in this batch.

- **Batch 49 authoring:** A family can include a source spelling without
  allowing the source reading for it: search-only 田ぼ does not remove
  the restriction of たんぼ to 田んぼ/田圃. Preserve that conflict
  explicitly while teaching the normalized form. Kanjipedia groups
  熟字訓 and 当て字 under one bracket marker; it supports whole-word
  learning for 算盤, not a historical classification or productive
  算=そろ rule. Distinguish JMdict's -zuru grouping from Japanese
  サ変 labels for 存ずる. Neither taxonomy licenses 存ずります.
  Existing 大小 receives a sourced N2 level and coverage citation,
  not a rewritten identity or silent claim to teach specialized senses.

- **Batch 48 reconciliation:** Check ordinary secondary senses even when
  an older title highlights another use: 入る includes belonging in a
  category, ばたばた includes successive falling, and そして/そうして
  include addition rather than only sequence. Newly taught possession
  in reused 備える requires direct 持つ/ある safeguards; record this exact
  baseline-exclusion addition rather than silently weakening preservation.
  続 already has on ゾク, so 続々 needs no invented voicing explanation.
  祖先 is not limited to an individual family. Dictionary しょくする has
  an overlapping belonging sense, not disjoint uses; 剃る's なまって note
  supports pronunciation qualification, not a guessed region or frequency.
  GPT's broader comparison reads and Claude's localized explanatory catches
  were complementary on this batch, not a controlled model-bias experiment.

- **Batch 48 authoring:** Check flags on each spelling, not just
  membership in a family: 其の他/其の外/其他 are search-only;
  其の頃 is not in the selected pinned family and is not taught.
  Normalize rare 卒直 to 率直 while explicitly preserving recognition
  of the source form; its 卒 link is alias navigation, not a primary
  reciprocal pair. Keep 続々 separate from shivering ぞくぞく and
  蕎麦 separate from spatial 側. The whole-word reading そば does not
  assign ば to 麦. Preserve N3 備える while adding rare 具える
  recognition and possession, not a since-birth-only restriction.
  剃る's alternate する remains godan, not irregular "do."
  A simplified rate-only extraction did not verify 率's ソツ
  meaning; the separately captured actual Daijisen character entry
  does. Distinguish the 26 original public attempts from that
  supplemental character inspection.

- **Batch 47 reconciliation:** An adjective ending does not establish
  native lexical origin. For 騒々しい, distinguish the collection's
  on-first mixed study classification from disputed historical formation;
  the inspected dictionary discusses competing origins and possible ateji.
  Do not replace an unsupported native-origin claim with an equally
  unqualified on-reading etymology. Actual ordinary senses and displayed
  labels support six additional direct safeguards, including 丸's
  whole-amount sense, ざわざわ's noisy-commotion sense and 表's front
  label. Neither footwear topic overlap nor an older indirect guard
  suffices by itself. Both reviewers found useful gaps, but GPT's complete
  comparison-family scope and Claude's targeted-label scope differ;
  complementary findings are not proof that model bias was eliminated.
- **Batch 47 authoring:** Reuse an established kana-primary
  article only after explicitly teaching the source alias:
  そうっと is an emphatic form of existing N3 そっと,
  not a reason to replace its stable ID, reading or level.
  Preserve the blank raw gloss separately. A shared
  dictionary family also does not make センチ's
  sentimental use independently N2 when the source
  selects measurement/prefix senses. Record conflicting
  source granularity precisely: JMdict labels 造船する
  intransitive, while inspected Daijisen gives a direct
  object. Neither observation warrants a universal ban.
  全般 needs its noun-suffix and 全般的 attachment
  patterns; 相互 is not automatically a な-adjective.
  Typical railway 線路 and traditional 草履 examples
  do not establish railway-only or grass-only rules.
  Mixed historical/homophone headings and failed
  そういえば extraction remain explicit limitations.

- **Batch 46 review/reconciliation:** Separate the kanji's
  reading/okurigana boundary from the inflectional stem:
  攻 is read せ, but 攻める's ichidan stem is せめ.
  A particle's ordinary secondary sense can need a
  direct guard even when its card focuses on approximation:
  くらい also supports minimum requests overlapping
  せめて. Broader class, rule and series labels warrant
  direct precautions against the actual seminar,
  autocracy and collected-edition labels; this does
  not make the Japanese words unrestricted substitutes.
  Existing 頂上 protection does not propagate to
  先端/トップ. Remove a warning's unsupported source
  gloss rather than leaving learners to infer a use
  that the selected records do not establish.
  GPT and Claude supplied complementary observations
  at different comparison depths; confirmations assess
  shared hypotheses, not a second blind experiment.

- **Batch 46 authoring:** A mixed dictionary extraction
  can contain both the minimum-wish adverb せめて and
  the attack-method noun 攻め手. Preserve the raw gloss
  mismatch and supplied identity separately; a successful
  page fetch does not choose the correct heading.
  ぜひとも can make a polite invitation rather than
  require coercion. 前後 needs both attachment patterns
  and its order/co-occurrence senses, with close succession
  distinguished from exact simultaneity. 洗剤 can include
  soap, and 全集 can collect a genre rather than one
  person's every work. A kana-primary alias does not add
  unwritten characters to metadata; 瀬戸物's place name
  does not authorize a literal door-based etymology.

- **Batch 45 review/reconciliation:** Assess the complete
  qualified English label, not an isolated substring:
  Common Era year numbering does not mean any era or
  century, so remove the unsupported period-word guards
  rather than expanding them transitively. Conversely,
  effort/opportunity and formation/conclusion labels
  need their own direct overlapping-label precautions.
  Qualifying 接する's interpersonal title avoids implying
  generic matter-settling; its physical contact still
  needs the actual 当たる comparison. Prefer the
  dictionary's attested ひざを接する for the transitive
  use. A warning against invented etymology should not
  suppress the source's actual historical account:
  Daijisen connects older 折角 to breaking a horn.
  Link existing contrast cards as well as synonyms.
  Both model families found effort/opportunity gaps;
  their competing era-guard remedies required source
  adjudication, not majority vote.
  Claude's confirmation then found the missed direct
  成立/効力 validity-label pair; the existing 有効
  guard did not cover it. Record this as a follow-up
  discovery, not retrospective initial-review credit.

- **Batch 45 authoring:** A useful plant-growth focus does
  not make 生長 historically plant-only or prohibit 成長
  for plants. Source legal-age ranges for 青少年 need their
  defining context, not a universal cutoff. 背負う's conceit
  sense is restricted to しょう/しょってる; select ordinary
  せおう senses separately and recognize that extra sense
  explicitly. 接する is a special-class する verb with
  adjacency, interpersonal, news, encounter, tangency and
  transitive contact uses, not a free noun 接 plus regular
  する. A usually-kana 折角/せっかく lesson can link both
  components without including unwritten characters in its
  metadata or counting alias navigation as a primary
  reciprocal pair. Resolve exact existing filenames before
  adding links or guards; dictionary spellings alone do
  not prove a target article exists.

- **Batch 44 review/reconciliation:** An apology card's
  thanks sense needs direct safeguards against each
  gratitude label; protecting ありがとう is not transitive.
  Likewise, 澄む's selected serenity sense matters beside
  its physical-clarity title, and rescheduling overlaps
  変える's actual meeting-time example. Bare English
  nature/print labels can justify conservative precautions
  without equating natural origin with inherent properties
  or printed matter with the printing action. Avoid a
  negated "X while Y" contrast that appears to affirm the
  very people/things partition being rejected. Both models
  found the gratitude gap; their other useful observations
  were complementary, but actual source-reading depths
  differed despite equal access.
- **Batch 44 authoring:** A dictionary spelling can
  need navigation without changing character metadata:
  清む belongs to 澄む/すむ, but pinned KANJIDIC2 does
  not list す.む for 清. Recognize the alias in the word
  and kanji notes rather than inventing a source reading.
  Keep 相撲's whole-word reading separate from component
  readings, and 刷る's regular conjugation separate from
  general-purpose する. Ordinary secondary uses matter:
  寸法 includes an arrangement, スライド includes shifts,
  and 製作 includes films. The source's work/slide/nature
  glosses do not establish unrestricted English
  equivalence. A redirect for ずらり was insufficient
  for the array description; inspect ずらっと itself.
- **Batch 43 review/reconciliation:** A comparison belongs
  at its substantive introduction, including 甘い/苦い in
  酸っぱい and ゴール in スタート; complete the directly
  dependent backlinks without rewriting old lessons.
  Bare cooling, starting and gap labels also need direct
  safeguards. Keep 涼む/冷める and 隙間/差 distinctions:
  an English-label precaution does not make the Japanese
  words freely interchangeable. Inspect ordinary secondary
  senses, such as 頭's beginning and 立ち上がる's computer
  start-up. Compare optional notes too: both reviewers
  noticed 冷める, despite different severities. Equal source
  access did not produce equal reading depth, so their
  complementary findings are not a model benchmark.
- **Batch 43 authoring:** A source's rare spelling can be
  recognized on an easier existing article: 棄てる belongs
  to the unrestricted 捨てる family, not a new conjugation
  or a reason to overwrite N4. Preserve its blank source
  gloss and identify the discard sense as an editorial
  anchor. Likewise, an audio-led スピーカー title and an
  appearance-led スマート explanation must not erase their
  recorded human-speaker and clever/adroit uses. Public
  extraction can also mix unrelated material, such as disk
  diagnostics under スマート; verify the intended heading.
- **Batch 42 review/reconciliation:** Recognition of a
  kana alias must not leave its extra vowel unexplained:
  ずうっと writes lengthening, not the short pronunciation
  of ずっと. Keep the search-only dictionary flag distinct
  from that orthographic teaching. Bare estimation/level
  labels also require ordinary secondary-sense checks;
  推定/計算, 推定/予定 and 水平/線 are direct safeguards,
  not transitive consequences of existing exclusions.
  These are documented-label precautions, not reproduced
  quiz failures or unrestricted Japanese synonym claims.
- **Batch 42 authoring:** A valid shortened form and its
  expanded reusable article can have different dictionary
  identities. Preserve source 水曜/すいよう (1372180),
  validate the unchanged 水曜日/すいようび article against
  1372190, and explicitly select the source alias sense.
  This is neither a source-ID correction nor a reason to
  create a redundant card or change its N5 level. Count
  twenty source principals separately from the twenty-one
  source-plus-teaching families in this packet.
- **Batch 42 source interpretation:** A blank raw gloss
  stays blank; a dictionary-backed editorial anchor does
  not recover the compiler's intent. A search-only alias
  such as ずうっと needs explicit recognition teaching.
  Preserve 水平's raw water-level/horizon gloss while
  teaching its actual horizontal sense; attribute the
  instrument use and 水平線's geometric use to the public
  dictionary, not invented extra JMdict sense indices.

- **Batch 41 review/reconciliation:** Name excluded subtypes
  precisely: excluding pistil/stamen does not exclude the
  plant-pith use of 芯 already taught. Keep source-note
  descriptions of actual example sentences distinct from
  uses merely listed in Meaning. For English "arts" and
  "application," evaluate actual quiz labels and qualifiers;
  conservative direct safeguards do not assert Japanese
  synonymy, transitive protection or a reproduced quiz
  failure. Preserve original authored notes and append exact
  correction counterparts rather than rewriting history.
  GPT accepted the 申請 precautions without independently
  establishing necessity; preserve that distinction instead
  of calling acceptance a reproduced defect or unanimous
  synonymy finding.
- **Batch 41 evidence access:** A wildcard grep can expose
  unassigned derivatives even without opening their files.
  Claude disclosed this; the complete native result contained
  data-only lines, not another report or author quiz rationale.
  Record the deviation rather than claiming strict allowlist
  compliance. Give searches exact evidence paths instead of
  a private-directory wildcard; distinguish three derivative
  groups from the five actual files returned here.
- **Batch 41 authoring:** Raw glosses need scoped lexical
  interpretation, not literal expansion. 寝台's "couch"
  does not make every living-room sofa a sleeping platform;
  人造's "imitation" does not imply fraud; 炊事's
  "culinary arts" does not require an artistic discipline.
  Preserve those raw fields and qualify the teaching with
  inspected entries rather than silently rewriting the list.

- **Batch 41 source handling:** Separate dictionary
  frameworks and broader public senses. 信ずる's JMdict
  `-zuru` classification and Daijisen サ変 label do not
  license a regular godan paradigm. Public figurative uses
  of 真空, 針路 and 神話 are not fabricated JMdict indices.
  人文科学's narrower humanities anchor must not erase its
  documented broader human/cultural-studies usage.

- **Batch 40 confirmation:** Distinguish complementary
  blind initial discoveries from agreement after sharing
  the fixes. Both original models accepted all three
  corrected cards, but that agreement is not a new
  independent discovery. Record the three complete rereads
  separately from thirteen inherited verdicts; preserve
  different source-reading depths and withdrawn optional
  hypotheses without turning them into verified facts.

- **Batch 40 review:** Check complete acquaintance senses,
  not only grammatical labels. ご存じ's second JMdict
  sense explicitly includes an acquaintance, supporting
  its direct guard against 知り合い. Also preserve both
  sides of 素人: an amateur may be skilled, but the word
  can describe a novice lacking experience or field skills.
  A valid caution against equating amateurs with beginners
  must not erase the affirmative inexperienced-person use.

- **Batch 40 review scope:** Preserve an original report
  even when its verdict table groups articles or its
  evidence reading is narrower than requested. Record the
  actual scope and request individual verdicts in bounded
  confirmation; do not retroactively claim complete source
  inspection or silently rewrite the archived report.

- **Batch 40 authoring:** Reused kana cards still need
  cross-references for the kanji spelling they teach.
  Preserve しょうゆ's kana ID, N5 level and empty kanji
  array while linking 油 in its existing 醤油 explanation
  and adding the reciprocal example at ユ. The current
  new-article-only coverage audit does not check reused
  pairs; explicitly verify this pair and existing
  籍 / 書籍 separately.

- **Batch 40 source handling:** Separate a reform proposal
  from evidence of its implementation. The inspected MEXT
  proposal explains the 助教授 / 准教授 reform and distinct
  助教 / 助手 roles; Daijisen supplies the April 2007 date.
  Do not turn historical Japanese ranks into a universal
  one-to-one mapping to current US academic titles.

- **Batch 39 confirmation:** Review scope prose can itself
  be inconsistent. Claude listed 原因 as both re-read and
  carried-over-only; the successful native view returned
  its complete body in confirmation. Preserve the report,
  verify the actual event and append a narrow scope
  clarification instead of silently repairing the archive.

- **Batch 39 review:** A caution against invented etymology
  must not itself invent a negative historical claim.
  焦点's cited dictionary explicitly explains its name
  through black paper scorching at focused sunlight.
  Attribute that explanation rather than calling it
  merely a mnemonic or denying its derivational basis.
  Keep the compound's naming separate from the historical
  origins of its individual characters.

- **Batch 39 authoring:** A raw English gloss is not a
  technical guarantee: 消毒's "sterilization" gloss needs
  the bounded public definition distinguishing making
  pathogens harmless from eliminating every organism.
  Preserve the source gloss and qualify the teaching.
  Likewise 小数's "fraction" does not erase the difference
  between decimal and numerator-over-denominator notation.

- **Batch 39 source handling:** 生ずる illustrates a real
  classification difference between JMdict and Daijisen.
  Name the frameworks, teach the actual particles and
  inflected forms, and do not invent a regular godan
  paradigm to reconcile their labels. Keep alternate
  public headings such as 上下's other readings separate
  from the narrowly reused article's mapping.

- **Batch 39 inspection accounting:** Preserve a
  capture-stage plan's original pending status and append
  the later completed-inspection receipt. The 412-family
  capture is not a claim to have read all of it. Count the
  239 selected families, then the two inspected supplements;
  principals already included in that union are not extra.
  A failed actual-body extraction remains a failed lookup.

- **Batch 38 confirmation:** Match each overlap to its actual
  sense index: だめ's no-good sense overlaps しょうがない:3,
  while its hopeless sense overlaps しょうがない:4. A sound
  guard does not make a compressed citation precise.
  Preserve reviewed evidence and append the clarification.
  Archive the complete native final message, including any
  introductory paragraph before the Snapshot heading;
  slicing from that heading can silently drop part of a
  review. Authenticate against the actual final event.

- **Batch 38 review:** Keep dictionary-gloss attribution
  separate from a licensed teaching paraphrase. 順々's
  pinned English glosses are "in order" and "in turn";
  the independently inspected Japanese order-following
  explanation additionally supports a succession rendering.
  A precise mapping note should distinguish those sources.
  Direct quiz pairs also need their own evidence: 順々/どんどん
  is not protected through 次々, and 消化's broad "working
  through" label overlaps 詰める's ordinary details-resolution
  use. Compare optional observations as well as findings:
  both initial reviewers noticed the missing 打つ link,
  despite placing it in different report sections.

- **Batch 38 authoring:** A blank source gloss does not
  establish which dictionary sense the compiler intended.
  For しょうがない, preserve the empty raw fields and state
  an explicit dictionary-backed editorial anchor, with
  additional senses recorded separately. Likewise, the
  raw 純情 devotion gloss is not an independent teaching
  sense when the inspected entries establish innocence
  and pure-heartedness instead.
- **Batch 38 authoring:** Character and spelling variants
  do not supply missing grammatical attachment rules.
  The actual てしょうがない page supports verb て,
  い-adjective くて and な-adjective で; a CAPTCHA wrapper
  and a 404 supply no evidence for a different construction.
  Keep the unverified productive ようがない contrast out
  of this card rather than inventing an explanation.
- **Batch 38 authoring:** A full-body capture is not an
  inspection receipt. Of 89 bodies in twelve selected
  bundles, only 53 were read completely. Reused 定規 and
  seven additional nuisance/commute/processing/gas cards
  bring the actual inspected total to 61. Complete 通う
  also supplies circulation, beyond its commuting title;
  警察 includes an officer and 清潔/きれい moral purity.
  Preserve these ordinary meanings in quiz assessment.
- **Batch 37 confirmation:** Both original reviewers accepted
  the evidence for retaining 終了/切る・切れる; Claude withdrew
  its removal proposal. Preserve that as a withdrawal, not
  a useful correction or a newly shared initial discovery.
  Later agreement does not change who first found a defect.
- **Batch 37 reconciliation:** An example containing both a
  dwelling and its address does not demonstrate that the
  dwelling noun itself means a written address. Qualify
  住居's JMdict address gloss as dictionary recognition and
  use the attested 住居を定める pattern instead of inventing a
  direct address-field substitution. Keep the raw source
  gloss separate from that narrower teaching decision.
- **Batch 37 reconciliation:** Do not remove a quiz safeguard
  from primary titles alone. The actual 切る article teaches
  hanging up, supported by complete sense 4; 切れる teaches
  expiry, supported by sense 6. These support keeping the
  終了 precautions. Conversely, the complete 端1581610:1
  explicitly includes the end of a street, strengthening a
  tentative endpoint-label concern. A lower-confidence
  observation can become useful without becoming a second
  model's unique discovery.
- **Batch 37 authoring:** Deduplicate evidence by entry ID and
  check repeated records before counting. The 325-family
  capture includes twenty principal families, leaving 305
  nonprincipal families; it is not 345 distinct families.
  The selected full-body inventory also includes デモ outside
  the original 194 labels. With おやすみ and 学会, this gives
  197 actual labels and 120 inspected bodies, not 194 full
  inspections. Record those different scopes explicitly.
- **Batch 37 authoring:** Keep raw source glosses separate
  from licensed teaching. 重量's community “heavyweight boxer”
  is not a bare-noun sense in the pinned family; heavyweight
  class entries do not establish a boxer-person meaning.
  Conversely, the absence of 重点's colon sense from the
  inspected public entry does not invalidate its explicit
  JMdict sense. Neither disagreement establishes frequency.
- **Batch 37 authoring:** Inspect ordinary secondary senses
  when assessing quiz answers: 字 includes handwriting,
  おやすみ includes a day off, 学会 includes an academic
  conference, and 閉じる can end a meeting. A limited primary
  title is not proof that these meanings are absent.
  Keep grammar examples bounded: a 主語 need not be an agent,
  a は-topic need not be the subject, and omitted subjects
  depend on context and the grammatical framework.
- **Batch 36 confirmation:** Partial source inspection cannot
  establish that a family is absent. Both confirmations found
  洒落る1568670 already in the original packet; the repeated
  capture was checked equal, leaving two genuinely new
  demonstration families, not three. Preserve the useful
  morphology finding separately from the withdrawn absence
  premise and do not inflate model-contribution counts.
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
