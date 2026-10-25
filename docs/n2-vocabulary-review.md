# N2 vocabulary expansion and review ledger

## Status

**Batches 01-58 review-closed.** The target is all 1,812 source rows,
not 1,812 necessarily distinct new articles. The [source index](n2-vocabulary-sources.tsv)
preserves every row; empty teaching columns mean the mapping has not yet been established.
The first 1,160 rows are review-closed; none are draft,
652 remain pending, and none are unresolved.

Baseline: `f1a93f249b78ae87c8233da1fbb48e92f02d4b44` on the local
`jlpt-n2-vocabulary` branch. The completed kanji work is separately pushed as
[`jlpt-n2-kanji`](https://github.com/stop-cran/learning-japanese/tree/jlpt-n2-kanji).

See the [plan and authoring notes](n2-vocabulary-notes.md) and
[pinned source snapshot](n2-vocabulary-snapshot.json).

## Coverage states

- `pending`: original row inventoried; no reviewed teaching mapping claimed.
- `draft`: article and selected evidence exist, but independent review/reconciliation is incomplete.
- `closed`: independent GPT and Claude reviews and evidence-based reconciliation are recorded.
- `unresolved`: a consequential mapping or teaching question remains open; never counted as closed.

Rows may share an article but retain their own status, source identity, selected senses and notes.
`article_level` is the actual article's easiest sourced level, not a replacement for source N2.
Planning batch numbers are scheduling aids, not claims that a batch has been authored.

## Batch 58: N2:1142-N2:1161

**Status:** closed after authenticated independent reviews, bounded
corrections and original-session confirmations.

Seventeen new articles: 出来上がる, 的確, 手首, 手頃,
でたらめ, 手帳, 鉄橋, 手続き, 鉄砲, テニスコート,
手拭い, 手前, 出迎え, 出迎える, 照る, 展開 and 伝記.
The 的確 article explicitly teaches source alias 適確; both rows
retain their own identities and mappings. Two narrow reuses add
sourced N2: kana-primary でこぼこ recognizes 凸凹, and 照らす
links its existing 照る comparison. Their primary IDs, readings,
titles, kanji arrays, tags and original exclusions remain unchanged.

The [batch packet](n2-vocabulary-batch-sources/batch-58.json)
preserves all twenty raw rows and 19 distinct complete principal
families/40 senses. Actual author reading covers all 217 originally
captured complete comparison families/531 senses and all 106
captured older bodies. Three complete support families/six senses
cover 武器 and the native-first precedents 荷物/豚肉.
Together with the two reused candidates, these add five distinct
full bodies, giving 111 inspected older articles. The 207 original
navigation labels do not by themselves count as body inspection.
Another 36 labels from inspected front matter give 243 distinct
labels overall.
The principal records are included in the 220-family/537-sense
union, not added to it.

All 30 complete component records and the complete 鉄/橋/照
kanji bodies were read. Twenty source endpoints and a separately
captured 解凍 target yielded 21 positive lexical captures from one
dictionary service, not 21 independent dictionaries. The actual
解凍 computing definition resolves 展開's cross-reference.
Mixed public headings and unequal evidence depth remain explicit.

Do not promote raw "by definition" into an unrestricted
出来上がる adverb, raw "we" into a neutral 手前 pronoun,
or "opposite of compression" into every 展開 context.
手帳's certificate/ID uses, 鉄砲's specialized senses and
照る's Noh-mask use are bounded recognition, not separately
assigned N2. The native-first mixed classification follows
actual repository precedent and states 手て plus 帳チョウ.

Five reciprocal N2 pairs are checked at reading-row and Common
words surfaces: 鉄/鉄橋, 橋/鉄橋, 鉄/鉄砲,
照/照らす and 照/照る. Existing written components are linked
substantively; missing cards are not fabricated. Baseline kanji
metadata remains unchanged.

Closed totals: 1,150 mapped articles = 1,069 new and 81 reused
baseline identities; 4,342 total word articles.

### Batch 58 - initial reviews and reconciliation

Sequential, initially blind reviews of `65c98d9` used GPT-6.1 Sol
(`gpt-6.1-sol`) and Claude Opus 5.5 (`claude-opus-5.5`).
Both complete native final reports, exact prompts, models, snapshot
hashes, allowed reads and zero edits were authenticated.
Both actually read all 22 assigned word/kanji bodies; GPT additionally
read 117 complete older word bodies and Claude 10. These are actual
successful returned reads, not counts inferred from requested paths.
Their complete reports are archived as
[GPT initial](n2-vocabulary-reviews/batch-58-gpt-initial.md) and
[Claude initial](n2-vocabulary-reviews/batch-58-claude-initial.md).

Both identified the direct 展開/成長 guard, missing rarity
qualification for 鉄炮 and incomplete 手頃 sense citation, although
GPT classified the citation as optional. Claude additionally supplied
出来上がる/揃う and the pronunciation/character-meaning clarity
improvement in 展開. Six complete corrective families/18 senses
and the full 成長/揃う articles ground the two direct guards;
neighboring guards alone would not establish either pair.

Four articles receive bounded corrections: two direct exclusions,
the rarity label, the citation and the character/reading separation.
No primary identity, reading, title, level, selected/additional sense,
TSV mapping, baseline exclusion or kanji metadata changes.
Extra examples, origin notes, specialized senses and unestablished
parity suggestions remain optional rather than forced expansions.
Different comparison depth prevents model rankings or measured
bias-reduction claims.

### Batch 58 - confirmed and closed

Both original sessions accepted corrected commit
`b148e3670c00c73701ec5a84c95b2b4b0968ae33`.
The complete native reports are archived as
[GPT confirmation](n2-vocabulary-reviews/batch-58-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-58-claude-confirmation.md).
All twenty exact source-ID/article associations have separate
correctness, scoped-coverage and comprehensibility CLEAN verdicts.
No actionable defect or consequential unresolved teaching claim
remains within the stated scope.

Both actually returned the four complete corrected articles, full
correction patch, six complete corrective families/18 senses, both
complete 成長/揃う bodies and the exact TSV header/twenty rows.
All unchanged teaching and five reciprocal pairs inherit initial
complete-body judgments; Claude additionally rechecked the links.
The two older articles were already in each reviewer's initial
inventory, so distinct older-body counts remain GPT 117 and Claude
10. Author reconciliation adds two families/five senses and two
distinct older bodies, giving 222 families/542 senses and 113 bodies.

GPT accepts the additional 揃う guard and revises its initial pair
assessment. Claude explicitly withdraws neighboring guards as
sufficient evidence for either new pair; complete direct meanings
and actual titles/bodies decide. Citation severity differs between
the initial reports, not the underlying observation. Extra teaching
and unestablished parity edges remain optional.

The native reports are preserved unchanged. Claude's final limit
says 16 unchanged bodies, but its detailed scope and returned
evidence establish 18: 13 new words, two reuses and three kanji.
This arithmetic slip does not change a teaching judgment.
Git/hash/equivalence/manifest checks remain author-executed, not
independent reviewer execution or linguistic certification.

No teaching changes follow confirmation. All 3,273 baseline
identities/readings/titles/exclusions remain preserved. The global
audit tracks 255 reciprocal N2 pairs for new articles; reused
照らす is additionally checked in this batch's five dual-surface
pairs. Closed totals are 1,160 rows, zero draft or unresolved,
and 652 pending. No model ranking or measured bias reduction
is inferred from complementary observations and unequal depth.

## Batch 57: N2:1122-N2:1141

**Status:** closed after authenticated independent reviews, evidence-based
corrections and original-session confirmations.

Seventeen new articles: 強気, 釣り合う, 吊る, 吊るす, 手洗い,
定員, 定価, 低下, 定期券, 定休日, 停止, 停車, 停電,
出入り, 手入れ, テーマ and 出来上がり. Three narrow reuses:
出会い explicitly recognizes raw 出合い while retaining N3;
出かける recognizes 出掛ける and imminent departure while retaining
N5; 出入口 receives sourced N2, translated examples and a bounded
correction to its unsupported single-shared-door claim. All three
retain their primary identities, readings, titles and kanji arrays.
Original baseline exclusions remain unchanged.

The [batch packet](n2-vocabulary-batch-sources/batch-57.json)
preserves all twenty raw rows and complete principal families:
20 families/42 senses. Author inspection covered 123 original
complete families/297 senses and 13 support families/61 senses,
giving 136 distinct complete families/358 senses including the
principals. All 223 original labels plus eleven further labels in
inspected front matter were read: 234 distinct labels. All 74
original and ten support complete older bodies, 30 complete
component records and the three complete related kanji bodies
were actually read.

Twenty-three public endpoint attempts yielded 22 positive lexical
captures from one dictionary service, not 22 independent dictionaries.
The raw 吊す endpoint yielded no Digital Daijisen body; a separately
captured canonical 吊るす body supplies the definition. The thin
定休日 cross-reference is supplemented by the complete 定休
body, and 定期乗車券 supplies the period/section conditions and
abbreviation. Mixed headings, spelling/reading restrictions and
unequal evidence depth remain explicit.

Teach 出来上がり as a noun, not a general predicate inferred from
the loose raw gloss. Keep 停止's mourning sense restricted to
ちょうじ; do not transfer it to ていし. Source-specific POS labels
do not override directly attested broader usage, notably 手洗いする
and transitive 停車. 手入れ's police-raid sense is an explicitly
additional sense, not independently assigned N2.

Add five reciprocal pairs: 低/低下, 券/定期券, 停/停止,
停/停車 and 停/停電, at their actual whole-word readings.
Baseline kanji metadata is unchanged; existing written components
are linked substantively, and missing cards are not fabricated.

Current totals: 1,131 mapped articles = 1,052 new and 79 reused
baseline identities; 4,325 total word articles.

### Batch 57 - initial reviews and corrections

The initially blind [GPT](n2-vocabulary-reviews/batch-57-gpt-initial.md)
and [Claude](n2-vocabulary-reviews/batch-57-claude-initial.md) reports
reviewed authored commit `2a1d30f2abe197b94ac8a92730fd8e69086ae30a`.
Actual models were `gpt-6.1-sol` and `claude-opus-5.5`; isolated
processes ran sequentially and exited without edits. Complete native
messages, exact common prompts, actual models, committed hashes,
patch and blind evidence equivalence were authenticated. Their file
tools could not execute Git, hash or worktree checks; those checks
were author-executed, not independent reviewer claims.

Both read all twenty assigned articles, three complete kanji cards
and complete principal/comparison family renderings. GPT additionally
read 82 complete older word bodies; Claude read complete older bodies
only for 揃う and 下降, using title/guard checks for about 150 others.
Both read compact components/labels and public capture text. Partial
reads of the large evidence JSON and Claude's unread permitted source
documents remain explicit in the complete reports.

Shared findings correct 出入り's nonexistent 出入 attribution in
pinned family 1339910, add three required reading-row examples and
guard 低下 against 落ちる. Correct the current source note and its
packet mirrors without erasing the immutable initial evidence or
asserting that other Japanese sources prohibit 出入. Do not adopt a
"less common reading" claim from dictionary ordering alone.

Accept Claude's 手洗いをする versus 手洗いする precision and
低下/下げる guard, and GPT's direct 停止/上がる, 壊れる,
落ちる and 釣り合う/揃う, 適当 guards. Seven direct guards are
added, with no baseline exclusion edits or transitive propagation.
The 出かける construction was already explicitly qualified; treat
Claude's concern as a partial clarity improvement, not proof that
the original example is wrong. Explain the general ところ pattern
and add a tense-adjusted form of the actual departure-starting
dictionary example.

Reconciliation actually read fourteen complete families/89 senses
and eight complete older bodies. Deduplicating against the original
inspection gives 141 families/371 senses and 89 complete older
bodies, not the sum of overlapping captures. Their actual meanings
do not establish required 釣り合う/差し引き or 低下/断る guards
merely because English "balance" and "decline" are polysemous.
Those remain low-confidence optional hypotheses, not proof of zero
contextual overlap. Spelling-frequency claims, extra unselected
senses, parking comparisons and unrelated baseline guard redesign
are not required corrections.

The reports supplied shared and complementary useful observations,
but unequal actual comparison depth and interpretive suggestions
prevent model rankings or controlled bias-reduction claims.
Mappings, raw fields, selected/additional senses, easier levels and
primary identities remain unchanged; only N2:1136's explanatory
source note and the corresponding index hash change. Confirmation
must assess the actual changed passages, exact twenty associations
and all five required reciprocal reading-row/Common words pairs.
Initial reports and author corrections alone do not close the batch.

### Batch 57 - confirmed and closed

Both original sessions confirmed corrected commit
`e2315ebd92a28ebbea5ccfd9a69218bbf5ea1cce`:
[GPT](n2-vocabulary-reviews/batch-57-gpt-confirmation.md) and
[Claude](n2-vocabulary-reviews/batch-57-claude-confirmation.md).
The processes ran sequentially and exited without edits. All four
complete native reports, exact prompts, actual models, committed
snapshots, patches and blind derivatives were authenticated.
Both final tables contain the exact twenty source-ID/article
associations with all three facets CLEAN. No consequential
unresolved teaching claim remains; CLEAN is bounded review,
not exhaustive correctness.

Both confirmations completely reread the six changed articles,
all three kanji bodies, the actual correction patch, fourteen
complete corrective families/89 senses, eight complete older
bodies and the original captured public lexical headings. Successful
native returned content was checked against those complete files,
not merely requested paths. Both received all twenty exact committed
TSV rows and the header; GPT incidentally saw one adjacent pending
row without reviewing it. Unchanged judgments were explicitly
inherited. GPT additionally checked current word-side component
passages; Claude inherited their complete initial reads.

Both accepted the spelling and washing corrections, all seven
direct guards and all five reciprocal pairs at their actual readings.
Claude explicitly agreed the original 出かけるところです
construction was never wrong and accepted the context-bounded
departure example with no consequential disagreement. Further
contrast with a completed-departure context remains optional.
Priority-based frequency ranking was withdrawn. Bare-English
balance/decline guard hypotheses remain weak optional suggestions,
not unresolved defects or proof of zero contextual overlap.

Actual older-body depth remains unequal: GPT initially read 82
distinct complete bodies and cumulatively 84; Claude initially
read two and cumulatively nine. Claude's two initial plus eight
corrective reads include 揃う twice: ten reading occurrences,
not ten distinct comparisons. The native report is preserved
unchanged with that count qualification. The deduplicated author
inspection remains 141 families/371 senses and 89 complete older
bodies, not either reviewer's independent inventory.

Closure changes only the twenty row statuses, packet closure
receipt, source-index hash and coverage, ledger/notes and confirmation
archives. Teaching, mappings, exclusions and the manifest are
unchanged after confirmation. All 3,273 baseline identities remain
preserved, and 251 distinct reciprocal N2 pairs are tracked.
There are 1,140 closed rows, no drafts or unresolved rows and
672 pending. The full 1,812-row expansion and final audit remain
incomplete.

## Batch 56: N2:1102-N2:1121

**Status:** closed after authenticated independent reviews, evidence-based
corrections and original-session confirmations.

Fourteen new articles: 伝わる, 突っ込む, 務める, 努める, 綱,
繋がり, 繋がる, 繋げる, 潰す, 潰れる, つまずく, 詰まる,
爪 and 艶. Five reused articles cover six source rows: 作る recognizes
造る; 付ける explicitly recognizes 着ける and 点ける; unchanged
漬ける already teaches 浸ける soaking. Preserve their N5/N5/N4
levels and primary identities. 粒 and 積む receive sourced N2 only;
their original teaching and exclusions are retained, not newly authored.

The [batch packet](n2-vocabulary-batch-sources/batch-56.json)
retains all raw fields. Twenty source principal families have 99 senses;
the corrected 務める teaching family gives 21 source/teaching families
and 100 sense records. Author inspection covered all 131 original
families/524 senses plus eight supplemental families/33 senses:
139 distinct complete families/557 senses, including the principals.
All 263 original labels and 26 further labels in inspected article
front matter were read, giving 289 distinct labels. All 95 selected
original and seven supplemental complete older bodies, 29 component
records, three complete related kanji bodies and twenty public lexical
captures were actually read. The public captures come from one
dictionary service, not twenty independent dictionaries.

The raw 務める row supplies 1240825, whose pinned spelling is only
勤める. Correct teaching to separately inspected 2872052, retaining
the erroneous supplied identity rather than treating it as an alias.
努める's repeated employment gloss is retained as source data but
corrected to effort in teaching. 点ける 1610400:1 is a real separate
entry cross-referenced to 付ける 1495770:13, not an erroneous identity.
Preserve the 浸ける soaking versus 漬ける-only pickling restriction.

Add substantive 詰/詰まる reciprocity at つまる and link the 造る
examples on 造 to the stable 作る article. Baseline kanji metadata is
unchanged. Other existing written components are linked word-side;
missing cards are not fabricated. Explicit baseline guard additions
on 作る and 付ける are recorded separately; original exclusions
are preserved. The unchanged 粒 guards are not claimed as newly
researched comparisons.

Current totals: 1,111 mapped articles = 1,035 new and 76 reused
baseline identities; 4,308 total word articles.

### Batch 56 - initial reviews and corrections

The initially blind [GPT](n2-vocabulary-reviews/batch-56-gpt-initial.md)
and [Claude](n2-vocabulary-reviews/batch-56-claude-initial.md) reports
reviewed authored commit `3e67155e0a83c666b61719eca7eb3377fd649ce9`.
Actual models were `gpt-6.1-sol` and `claude-opus-5.5`; isolated
processes ran sequentially and exited without edits. Complete native
reports, exact prompts, sessions, models, frozen source derivatives,
patches and hashes were authenticated. Initial defects remain in the
archived reports, not relabelled as clean.

Both found the missing 努める/苦心 and 潰れる/ぺちゃんこ guards.
Both also mentioned the unlinked 勉/力 variant components, although
Claude labelled that optional; it is not a unique GPT discovery.
Add those two guards and links. Claude uniquely proposed 作る/生産;
the complete actual 生産 article and 1378990 production/manufacture
sense support that direct guard, independently of neighboring edges.
Also accept its optional 潰す/ぺちゃんこ and 詰まる/渋滞 hypotheses
after inspecting physical crushing/flattening and congested-state
meanings respectively. These five direct additions do not claim
unrestricted Japanese interchangeability or transitive exclusions.
Adopt its optional 艶 performance-charm wording, grounded in the
captured つや heading, not as a newly discovered correctness defect.

Do not add 繋がり's three proposed verb guards merely because 関係
and 接続 have noun-and-する uses. Actual 繋がり is the connection
itself, not connecting/being connected; its noun-only family has no
secondary connecting-verb use. Likewise 役, 役割 and 務め identify
a role or duty, not the predicate "serve as; play a role" of 務める.
Existing 勤め/勤める protection concerns overlapping work/service
meanings; it is not a universal same-root or noun/verb rule.
通信's channel activity versus 伝わる's conveyed thing remains a
weaker optional hypothesis, not an established missing guard.

All 21 corrective families/58 senses and fourteen complete older
bodies were actually read. Deduplicated family totals are now
144/565, including the twenty-one source/teaching principals.
The old-body union is 106: 苦心, ぺちゃんこ, 生産 and 渋滞 add
four new reads to the previous 102; the other ten are rereads.
Initial GPT fully read 76 additional older comparison bodies;
Claude fully read one and used targeted title/guard searches.
Those are their actual scopes, not the author's counts. Claude
did not read the family-inspection renderings or fetch fresh pages.
The allowed but absent redundant `principal-reading.txt` was a
prompt limitation; the complete principals JSONL was available and
read. These unequal depths and optional/unsupported hypotheses
limit any model-bias conclusion.

### Batch 56 - confirmed and closed

The original [GPT](n2-vocabulary-reviews/batch-56-gpt-confirmation.md)
and [Claude](n2-vocabulary-reviews/batch-56-claude-confirmation.md)
sessions confirmed `bee40f02c2313d736a8c8f1f726b417056466260`,
parent authored commit `3e67155e0a83c666b61719eca7eb3377fd649ce9`.
Actual models remained `gpt-6.1-sol` and `claude-opus-5.5`.
Both native processes exited sequentially with no edits; exact
prompts, models, reports, frozen hashes, derivatives, patches and
allowlisted access were authenticated for all four reports.

Both fully reread six changed articles, five unchanged hypothesis
articles, the actual patch, all 21 complete corrective families/
58 senses, all fourteen older bodies and the captured 艶 headings.
Complete required reads and exact twenty source-ID/article
associations were checked against authenticated access records and
the committed TSV. Both final tables mark all three facets CLEAN
for every association; unchanged initial judgments are explicitly
inherited, not misreported as fresh complete rereads.

All three GPT findings are resolved. Claude resolved B56-Q1,
B56-Q3 and B56-Q5, and explicitly withdrew B56-Q2 and B56-Q4
after reading complete comparisons. Both accept the five direct
guards and rare-component links, the optional performance wording,
and no required connection/role-family guard on the actual meanings.
通信 remains a weaker optional hypothesis; extra 突/込 backlinks
remain optional. No teaching changes follow these confirmations.

Claude's final reference to noun/predicate reasoning is not a
blanket exemption: 通信 itself has a する use, and the actual
activity/conveyed-thing distinction remains the bounded basis.
Its closing one-service shorthand applies to public captures,
not the separately read pinned JMdict families. Preserve the
complete native report rather than silently rewriting that scope.
Git/hash/manifest checks are author-executed; no runtime quiz draws,
exhaustive synonym certification, native-speaker approval or
controlled model-bias reduction is claimed.

## Batch 55: N2:1082-N2:1101

**Status:** closed after authenticated independent reviews, evidence-based
corrections and original-session follow-up confirmations.

Eighteen new articles: 散らす, ちり紙, 散る, 追加, ついで,
通貨, 通勤, 通知, 通帳, 通訳, 通用, 通路, 付き合う,
突き当たり, 突き当たる, 点く, 突く and 次ぐ.
Reuse 通じる for narrow visible 通ずる recognition, preserving its
primary つうじる, N3, title and original teaching. Reuse 月日,
adding sourced N2 and provenance for つきひ while preserving its
identity and separately attributed がっぴ date reading.

The [batch packet](n2-vocabulary-batch-sources/batch-55.json)
preserves all raw fields and twenty source principal families/
56 senses. Including the retained 通じる teaching family gives
21 source/teaching families and 70 sense records. Author inspection
covered 221 selected original families/669 senses plus six distinct
supplemental families/16 senses: a deduplicated union of 227/685,
including the principals. All 127 original and four supplemental
labels, 116 selected original and four supplemental full old bodies,
26 component records, the complete 貨 kanji card and twenty public
lexical endpoint bodies were read. The other captured families and
eleven irrelevant original label matches are not claimed as complete
reads. Public endpoints are one dictionary service, not twenty
independent dictionaries.

Raw 通ずる has an empty source gloss. Entry 1983740 explicitly
crossreferences corresponding 通じる senses, supporting reuse;
selected connection/communication/expertise recognition is
nonexhaustive author scope, not recovered compiler intent.
Teaching entry 1432880 matches the preserved primary つうじる;
1983740 is separately recorded as a validated source alias.
Do not regularize the public サ変 通ずる form as ichidan.

Normalize source 塵紙 to ちり紙, 序で to kana-primary ついで,
and search-only 付合う to 付き合う, visibly retaining each raw
spelling and reading. Distinguish incidental 序で from subsequent
次いで, broad public 付く/着く from the lighting use of 点く,
and つく from a separately headed つつく. Public credit-account
通帳 recognition is not a fabricated second pinned sense.
Additional senses do not independently acquire an N2 label.

Add 貨/通貨 with つうか in the カ reading row and Common words,
preserving baseline kanji metadata. Other existing primary components
are substantively linked word-side; missing cards are not invented.
Current totals: 1,092 mapped articles = 1,021 new and 71 reused
baseline identities; 4,294 total word articles. A draft is not
review-closed merely because it is committed or structurally valid.

### Batch 55 - initial reviews and reconciliation

Common authored snapshot: `f467750c0645c7d3f0f07d24068f418a84887b0e`,
parent `b005473a6a1dda6e0b52dd1f43c94bf7d7b22d75`. Actual
`gpt-6.1-sol` and `claude-opus-5.5` reviewed sequentially with
identical blind prompts apart from model/family substitutions.
Both processes exited without edits. Complete
[GPT](n2-vocabulary-reviews/batch-55-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-55-claude-initial.md) native
final reports are archived; public formatting only replaces
two-space hard line breaks with blank lines. Author checks
authenticate actual models, native sessions, exact prompts,
frozen file hashes, patches, blind derivatives, private-file
allowlists and zero edits.

Dispositions below are subject to original-session confirmation:

- **F001 / B55-02: resolved.** Add 通知/届ける. The complete
  older article actually teaches notifying an authority, supported
  by 1457210:2, not merely the delivery topic.
- **F002 / B55-01: resolved.** Add 通訳/解釈 and /読み.
  Unqualified English interpretation is a valid oral-translation
  gloss in 1433560:1. The Japanese distinction remains useful;
  body explanations and 解釈/読み protection do not resolve these
  direct quiz ambiguities. Claude mentioned 読み too.
- **F003: resolved.** Add 通用/働く. Actual 1433570:2 and
  ordinary functioning/effectiveness in 1451150:2 support English
  work, despite the older article's employment emphasis.
- **F004: resolved.** Add 散らす/広がる. Actual spread meanings
  in 1303460:2 and 1602360:1 support the bare English spread-out
  ambiguity; Japanese transitivity remains explicitly taught.
- **B55-03: resolved as comprehension improvement.** Explain
  separate つつく, also written 突く, with light/repeated poking
  and pecking recognition from 1456895:1-2. Do not infer that the
  original light single-poke つく example is wrong or that
  repetition is an absolute requirement. Record the extra identity
  separately without assigning it another N2 level.
- **B55-04: resolved.** Add the に construction and the actual
  captured 世界に通用する新技術, with kana and English.
  Retain the で setting construction, not a substitution rule.
- **B55-05: resolved.** Gloss サ変 as an irregular conjugation
  class and direct practical conjugation to the already taught
  通じ- forms. Preserve the primary つうじる and easier N3.
- **B55-06: optional, outside this batch's changed teaching.**
  The unchanged 月日 claim about reversing 日月 is overbroad:
  the two complete entries also overlap in celestial/time uses.
  Record a future baseline correction rather than silently
  expanding this narrow reuse into a whole-card rewrite.
- **Claude optional guards, author-adjudicated:** Add 突く/当たる
  on ordinary hit/contact meanings (1448810:1-2), 通路/通行 on
  the underspecified English passage label (1433180:1),
  突き当たる/届く on actual reach/arrive meanings (1457200:1-2),
  and 通用/通貨 on English currency (1433570:1/1433050:1).
  These are direct label ambiguities, not unrestricted Japanese
  synonymy or automatic propagation through existing guards.
  No required ついで/せっかく or 散らす/散らかる pair is
  established: the actual valuable/effort uses and explicit
  untidy/scattered-state wording do not establish the proposed
  incidental-occasion or active-distribution equivalences.
- **Other optional:** Clarify 散らす's ます-stem wording.
  Further spellings, accompaniment constructions, terminology
  and baseline expansions remain optional; no demonstrated
  selected-sense mismatch requires changing the ついで mapping.

Seventeen guarded new articles now declare 88 pairs, versus 79:
nine direct additions and no removals. Seven new word articles
and reused 通じる change. Only N2:1100 gains additional
1456895:1-2 recognition, with a corresponding source-note
clarification and index hash update. Other raw fields, selected
source senses, article identities and levels remain unchanged;
no new kanji teaching edits.

**Usefulness and limits:** Both models independently identify
notification/interpretation gaps, including Claude's tentative
読み suggestion. GPT uniquely establishes work/spread gaps;
Claude uniquely surfaces the three explanatory omissions and
the additional optional guard hypotheses adjudicated above.
This is complementary evidence on one sample, not a controlled
bias-reduction result or general model ranking. GPT completely
read 96 older bodies; Claude read four and parts of two more,
using labels for most other comparisons. Both read all assigned
content and family renderings, but their partial packet/snapshot
reads differ. Claude's broad `.github` search surfaced two
unassigned agent files; it claimed no reliance, and the
deviation is retained rather than certified away. Neither
review supplies native-speaker certification or runtime quiz
draws. Author corrective rereads do not increase the deduplicated
227-family/685-sense or 120-old-body inspection totals.

### Batch 55 - first confirmations and follow-up

Corrected snapshot: `cab666775db68a2cf5233ca1f8f4d13a1ff7bb40`,
parent `f467750c0645c7d3f0f07d24068f418a84887b0e`. The complete
[GPT confirmation](n2-vocabulary-reviews/batch-55-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-55-claude-confirmation.md)
are authenticated native reports from their original sessions.
Both accept all original fixes and the four author-adjudicated guards.
GPT finds no new actionable defect. Claude establishes low-severity
B55-07: the added functioning comparison needs a clearer contrast with
an excuse being accepted. Add that contrast and put the general
non-substitution warning after all the comparisons. Do not adopt an
unverified universal claim that a particular invented sentence is
ungrammatical.

Author inspection of Claude's further optional hypotheses establishes
four more direct guards: 突き当たる/至る and /達する on actual
spatial reaching uses (1311870:1-2, 1416230:1), 通用/効く on
English work/effectiveness (1591100:1-2), and 通訳/受け取る on
underspecified English interpret (1329650:2). The latter protects the
direction in which bare interpret can suggest interlanguage interpreting;
it does not claim that 受け取る means translating between languages.
Add short linked comparisons and exact dictionary attribution.

No required 通用/働き guard is established by the actual work,
performance or operation noun senses (1451040:1-2,4); these do not
establish an accepted-use or validity meaning. Nor does 通過's
explicit passing-through activity (1433070:1) establish a physical
passageway answer for 通路. These are individual label-and-meaning
judgments, not categorical part-of-speech exclusions, transitive guard
inference or denials of every contextual overlap.

The final draft has 92 declarations across seventeen guarded new articles:
four more additions after the first correction's 88, with none removed.
The source mappings, raw fields, article identities and levels are
unchanged from the first correction. Six follow-up complete families/
19 senses include two already inspected families; four new families/
14 senses raise the deduplicated author union to 231/699.
Six comparison bodies include two rereads; four new complete bodies
raise the old-body total to 124.

Both confirmation readers completely read the eight changed articles,
unchanged 通貨 and ついで, all 22 corrective families/97 senses,
all ten supplied old bodies and the three original public captures.
Unchanged judgments are explicitly inherited. GPT additionally checks
all twenty headers and reaches 97 distinct full old-body reads;
Claude checks nine of the seventeen current guard declarations on disk,
reads five extra comparison bodies, and makes an unsuccessful fresh
働く fetch that supplies no dictionary evidence. Their partial
derivative reads and initial scope limits remain disclosed. This is
additional sample usefulness, not a blind new discovery or controlled
bias-reduction measurement.

### Batch 55 - confirmed and closed

Final teaching snapshot: `3523c2ed00b37d358f40b54d8ca749f35e0007a9`,
parent `cab666775db68a2cf5233ca1f8f4d13a1ff7bb40`.
Both original sessions accepted B55-07's local clarification and all
four further direct guards. The complete
[GPT follow-up](n2-vocabulary-reviews/batch-55-gpt-followup.md) and
[Claude follow-up](n2-vocabulary-reviews/batch-55-claude-followup.md)
each give the exact twenty source-ID/article associations CLEAN for
correctness, scoped coverage and comprehensibility. Both completely
reread the three changed articles, unchanged 通路, the actual patch,
all eight complete follow-up families/26 senses and seven full old
bodies. Other judgments are explicitly inherited, not fresh complete
rereads. No teaching changes follow those confirmations.

Both accept the individual decisions not to require 通用/働き or
通路/通過; this does not certify zero contextual overlap or make an
added guard intrinsically wrong. Claude qualifies the passage distinction
as slim. Optional future 働く functioning coverage and the unchanged
月日/日月 baseline correction remain outside this batch.

Author authentication verifies all six complete native final reports,
actual models, exact prompts, original-session continuity, three frozen
snapshots, patches, equivalent derivatives, private allowlists and zero
edits. The first Claude confirmation's NEEDS FIX is preserved, not
rewritten into a clean verdict. Historical evidence and unequal read
depths remain explicit, including the initial `.github` scope deviation.
This sample shows complementary findings and a useful follow-up catch,
not controlled bias reduction or a general model ranking.

Closure preserves all 3,273 baseline identities/readings/titles/exclusions,
245 tracked reciprocal N2 pairs for newly authored words, the separate
narrow reused identities, and the confirmed teaching/manifest unchanged.
The manifest has 6,922 entries: 6,325 content files, 396 images and
201 scene catalogs, content version `b13b877fb969383b`.
All 1,100 rows through batch 55 are closed; 712 remain pending.
There is no native-speaker certification, live-quiz draw or exhaustive
semantic-uniqueness claim.

## Batch 54: N2:1062-N2:1081

**Status:** closed after authenticated independent reviews, evidence-based
corrections and original-session confirmations.

Nineteen new articles: 長所, 長女, 調整, 調節, 頂点, 長男,
長方形, 調味料, チョーク, 直後, 直線, 直前, 直通, 直流,
貯蔵, 直角, 直径, 散らかす and 散らかる. Existing 長短
already covers relative length and pros/cons; add only sourced N2
and dictionary/public provenance, preserving its identity, primary
reading, title, original teaching and exclusions.

The [batch packet](n2-vocabulary-batch-sources/batch-54.json)
preserves all raw fields and twenty complete principal families/
26 senses. Actual author reads cover 238 selected original families/
563 senses and 30 complete supplemental families; three are duplicates,
so the inspected union is 265 families/633 senses, including the
principals. All 91 original and 18 supplemental labels were read,
as were 82 selected original and 18 supplemental full old bodies,
25 component records, five complete related N2 kanji cards and
twenty public lexical endpoint captures. Not all 251 original
captured families or all 91 original old bodies are asserted read.
The public captures are one dictionary service, not twenty
independent dictionaries.

Add reciprocal reading-row and Common-words examples for 線/直線
with ちょくせん, 貯/貯蔵 and 蔵/貯蔵 with ちょぞう, and
角/直角 with ちょっかく. Existing 短/長短 with ちょうたん
is already complete and remains unchanged. Missing 整, 節 and 径
remain in word metadata without fabricated kanji cards.

The raw チョーク gloss spans chalk entry 1078240 and chock
entry 2854421, not two senses of the principal entry. Separate
2854422 supplies chokehold/engine choke. The public capture
supports chalk/choke headings; pinned evidence establishes chock.
直後's additional spatial use is publicly attributed, not invented
as a second pinned sense. Geometry and figurative 頂点, spatial
直前 and unproductive-hoarding 貯蔵 are separately allocated;
additional teaching is not independently N2-classified.

Current totals are 1,072 distinct mapped articles: 1,003 new and
69 reused baseline identities; 4,276 total word articles.
Review closure is a bounded evidence-based judgment, not an exhaustive
semantic-uniqueness guarantee or native-speaker certification.

### Batch 54 - initial reviews and reconciliation

Common authored snapshot: `a01a7787528d7f77f7c415d08747e06d75bb3dde`,
parent `23d10580d5115175392fe407e21cba9fe94d4fd0`. Actual
`gpt-6.1-sol` and `claude-opus-5.5` reviewed sequentially with
identical blind prompts apart from model/family substitutions,
scope and available evidence. Both exited without edits. The complete
[GPT report](n2-vocabulary-reviews/batch-54-gpt-initial.md) and
[Claude report](n2-vocabulary-reviews/batch-54-claude-initial.md)
are archived. Author-executed checks authenticate models, native
sessions, exact prompts, frozen hashes, blind evidence derivatives,
private-file allowlists, no named forbidden reads and zero edits.
Public archives only replace two-space hard line breaks with blank
lines; native private outputs and event text remain unchanged.

Evidence-based dispositions, subject to original-session confirmation:

- **N2-54-GPT-01: resolved.** Add direct 散らかる/汚い and
  散らかる/ぐしゃぐしゃ guards. Actual bodies and complete pinned
  1178940:2/2097580:3 establish ordinary untidiness, not just dirt,
  crumpling or wetness. Do not propagate this judgment to the
  causative 散らかす merely by transitivity.
- **B54-F01: resolved.** Add 調味料/酢, /食塩 and /しょうゆ.
  Full actual bodies and 1370270:1/1358410:1/1595020:1 identify
  the particular condiments. The broad seasoning label can answer
  these ingredient words; shared tags only affect likelihood.
  This is not a claim that the ingredient names are interchangeable
  or a rule to exclude every member of any shared category.
- **B54-F02: resolved.** Link 醤油 to the existing kana-primary
  しょうゆ article, preserving the actual spelling and reading.
- **B54-F03: resolved.** Add direct 直前/以前 protection.
  Actual before/prior-to uses and complete 1155150:1-2 support
  the broader overlapping time label. 前 protection is nontransitive;
  matching the 直後/以後 arrangement alone would not be evidence.
- **B54-F04: partially resolved, calibrated as editorial improvement.**
  Replace the insect example with 車の直前を横断しました and
  its actual reading/translation, closely inflecting the captured
  Daijisen pattern 車の―を横断する. The initial suggested
  横切る wording was not the captured attestation. No native
  judgment or evidence proves the previous sentence ungrammatical.
- **B54-F05: not adopted; original reviewer reassessment pending.**
  Complete 1310270 includes rule/domination, direction/management
  and governing influence. Neither the actual 支配 article nor
  this broad range establishes a level-adjustment synonym in
  1429240's sense. Shared English control, related tags and an
  existing 管理 guard do not establish the proposed direct pair.
  Retain the qualified control-versus-domination contrast.
- **B54-F06: resolved as small comprehension polish.** Name and
  link ぱらぱら in the rain/grain comparison; complete 1102580:1,3-4
  supports the contrast without treating all scattering as untidiness.
- **Optional suggestions:** Remove 長方形's potentially misleading
  "both long vowels" count, retaining the complete チョウ + ホウ + ケイ
  reading. No further guards are established by 有利's favorable/
  profitable uses, 次's next-in-sequence relation or 流れ's fluid/
  gas current. Retain 長所/味噌: ordinary secondary key-point
  usage matters despite the old miso-paste title and usual ミソ
  spelling. No baseline rewrites or extra 直角 construction are
  required for the assigned scope.

Corrective author reads: twenty-two complete families/51 senses,
twelve complete old articles and the complete original captured
直前 heading, not a fresh public retrieval. Fifteen corrective
families were already inspected: the deduplicated author total is
272 families/649 senses. Four old bodies were rereads, so the
deduplicated total is 108, not 112. Historical initial counts remain
unchanged in the packet.

Model-diversity observation across both complete reports: GPT uniquely
identified the two ordinary messy/untidy gaps; Claude uniquely
identified the additional condiment/before pairs, kana-primary link
and unnamed mimetic comparison. Claude also supplied the spatial
example and vowel-count improvements, but the control-pair proposal
is not adopted merely on English overlap. These are different
observations even where both reports discuss 散らかる. Actual
inspection depth differed: GPT reports 111 complete comparison
articles beyond the twenty assigned cards, while Claude read twelve.
GPT read the compact families/public renderings; Claude read the
entire blind JSON packet and public text, but not the compact
renderings or source snapshots. Claude disclosed reading that
packet before the frozen snapshot. Complementary findings were
useful; unequal depth and unsupported suggestions do not establish
controlled bias reduction or a general model ranking.

### Batch 54 - confirmed and closed

Both original sessions assessed corrected commit
`1fcf2decfeb120c621058a587d18178f31c1f3ef`, parent
`a01a7787528d7f77f7c415d08747e06d75bb3dde`, sequentially without
edits. The complete [GPT confirmation](n2-vocabulary-reviews/batch-54-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-54-claude-confirmation.md)
are archived. Both return the exact twenty source-ID/article
associations with all three facets CLEAN. Author-executed checks
authenticate complete native final messages, actual models, exact
common prompts, original-session continuity, snapshots, private
allowlists, no named forbidden reads and zero edits.

Both completely reread the four changed new articles, unchanged
調節, the actual correction patch, twenty-two complete corrective
families/51 senses, twelve complete old bodies and the complete
original captured 直前 heading. Both reread all twenty exact TSV
rows and spot-check all five reciprocal kanji pairs. Other full
teaching judgments are inherited from initial reads, not silently
reported as fresh rereads. GPT additionally fully rereads 長所,
直後 and 直流 and the complete 味噌 family; Claude only reads
snapshot headers, not entire previously uninspected snapshot files.
Neither reads the entire corrected derivative. These differences
remain explicit; author deduplicated counts are not reviewer counts.

Both accept the six direct guard additions, existing alias link,
named mimetic contrast, sourced spatial replacement and vowel-count
polish. GPT revises its initial bounded no-defect judgments for the
additional seasoning/before omissions. Claude explicitly withdraws
B54-F05's English-control rationale and revises the optional
長所/味噌-removal rationale after actual secondary-sense inspection.
B54-F04 is closed as an accepted source-aligned improvement, not
proof that the old insect sentence was ungrammatical; Claude also
withdraws the unattested 横切る replacement suggestion.

Do not promote ancillary confirmation reasoning into general rules:
Claude's starred 温度を支配する illustration was not independently
verified and is not a claim that every such string is ungrammatical.
Its seasoning-tag search does not establish exhaustive category
coverage. A part-of-speech difference alone neither requires nor
forbids an exclusion; the unextended 散らかす title explicitly
expresses causing a mess, unlike the untidy-state alternatives.
The unchanged qualified 調節 lesson does not depend on these
stronger reviewer generalizations.

Remaining construction, wording, usual ミソ spelling and baseline
link suggestions are optional; no additional required defect or
consequential unresolved teaching claim remains. There are no
post-confirmation teaching or manifest changes. The shared audit
retains 244 primary reciprocal pairs for new word articles; reused
短/長短 is checked separately, not counted as a 245th new pair.
The independently useful initial contributions and explicit
withdrawals support a bounded usefulness observation, not a model
ranking or controlled bias-reduction experiment. Confirmations
share adjudications and are not blind discoveries.

## Batch 53: N2:1042-N2:1061

**Status:** closed after authenticated independent reviews, evidence-based
corrections and original-session confirmations.

Eighteen new articles: 知人, 地帯, 縮む, 縮める, 縮れる,
チップ, 地点, 地名, 茶色い, 着々, 中間, 中旬, 抽象,
中世, 中性, 中途, 中年 and 彫刻. Reuse unchanged N5 ちゃわん
for 茶碗 and add sourced N2 provenance to existing 超過 without
changing its identity, reading, title, original teaching or exclusions.

The [batch packet](n2-vocabulary-batch-sources/batch-53.json) keeps
all original fields and twenty complete principal families/28 senses.
Actual author reads cover 244 selected complete original families/
614 senses plus two distinct supplementary families/four senses:
246 families/618 senses in all. The separately reread 御礼 family
was already selected and is not counted twice. All 173 original
labels and three supplementary labels were inspected, as were
113 selected original full old articles and three supplementary full
articles, 24 component records, three complete primary N2 kanji
cards and twenty public lexical captures. This does not claim that
all 359 original captured families or all 173 original captured old
bodies were read. The public captures are one dictionary service,
not twenty independent dictionaries. Failed exact requests 賭け札
and 雕刻 were explicitly removed; they verify nothing positively.

New reciprocal reading-row/Common-words pairs are 帯/地帯 with
ちたい and 象/抽象 with ちゅうしょう. Existing 超/超過 with
ちょうか is already complete and needs no kanji-card change.
Missing 縮, 旬, 抽, 彫 and 碗 cards are not fabricated.
All written components remain in the new words' metadata;
the unchanged kana-primary ちゃわん retains its original metadata.

Raw source fields are not repaired in place. 茶色い retains a blank
raw gloss, with ordinary brown supported by the inspected public
adjective entry alongside pinned light-brown/tawny wording.
中性's raw "sterility" is not taught as medical infertility.
チップ explicitly separates tip entry 1077740 from chip entry
2850287. Selected primary senses and separately attributed additional
or derived teaching remain distinct; extra teaching does not
automatically acquire an independent N2 assignment.

Current totals: 1,052 distinct mapped articles, comprising 984 new
and 68 reused baseline identities; 4,257 total word articles.
Review closure is a bounded evidence-based judgment, not a
semantic-uniqueness guarantee.

### Batch 53 - initial reviews and reconciliation

Common authored snapshot: `d67609747e671278f9a6a4e973ea0a0832a8cad8`,
parent `6f5e4cdeb1de5be236364fde7ed1b3e6e95453a1`. Actual
`gpt-6.1-sol` and `claude-opus-5.5` reviewed sequentially with identical
blind prompts apart from model/family substitutions, scope and source
access. Both processes exited without edits. The complete native
[GPT report](n2-vocabulary-reviews/batch-53-gpt-initial.md) and
[Claude report](n2-vocabulary-reviews/batch-53-claude-initial.md) are
archived. Author-executed checks authenticate the actual models,
sessions, exact prompts, frozen hashes, blind derivative, private-file
allowlists, no named forbidden reads and zero edits. Public archives
only replace two-space hard line breaks with blank lines; native
private reports and event text remain unchanged.

Evidence-based dispositions:

- **GPT53-001 and B53-C-01: resolved shared omission.** Add direct
  チップ/端 protection. The actual articles and complete pinned
  1077740:3/1581610:1 support the physical-tip overlap. Indirect
  先 or 先端 paths are not protection.
- **GPT53-001: resolved additional omission.** Add チップ/末.
  Actual 末/すえ teaches an end or tip, supported by complete
  1525250:1 without an archaic flag. This is not 末/うら or
  an inference from its temporal uses.
- **B53-C-02: resolved.** Add 地帯/ベルト. Complete 1120070:3
  supplies the geographical belt/zone/area use, beyond the old
  card's clothing and machine examples. A shared English word
  alone would not establish that Japanese overlap.
- **B53-C-03: resolved with corrected evidence.** Add 着々/徐々に.
  The review's 1345600 徐々 steady sense is archaic and is not
  evidence about unrestricted modern 徐々に. Complete modern
  1595480:1 independently includes steadily and step by step;
  its actual article teaches a developing process. This supports
  the direct quiz judgment without deriving it transitively
  from だんだん or asserting universal interchangeability.
- **B53-C-04: resolved.** Link substantive 酸性 comparison in 中性
  to the existing article, retaining correct さんせい and teaching.
- **Optional suggestions: no required expansion.** Abstract-suru
  register, a further 中性 example, 集合地点, straight-hair terminology,
  historical-period contrasts and provenance rewording do not establish
  defects in the practical scope. Existing natural examples and
  learner-facing source convention are retained, not certified as
  the only possible wording.

The author actually read all eleven complete corrective families/
29 senses, plus full 端, 末, ベルト, 徐々に and 酸性 articles.
Do not replace the historical initial inspection counts with these
later reads. The initial reviewer reports remain historical, including
Claude's unverified public-backed 茶色い qualification.

Model-diversity observation across the complete reports: チップ/端
was shared; GPT additionally found チップ/末; Claude additionally
found the geographical-belt and modern gradual-progress pairs and
the existing 酸性 link. Severity/facet differences do not make the
shared omission two discoveries. Both read the twelve selected
family renderings and supplemental rendering, but actual old-body
depth differed sharply: GPT reports 100 additional complete articles,
Claude one (ベルト), beyond the assigned reuses. GPT read the public
captures; Claude did not and checked mappings via blind JSONL
rather than the TSV. Complementary suggestions were useful, but
unequal inspection and the corrected archaic-entry rationale do
not demonstrate controlled bias reduction or a general model ranking.

### Batch 53 - confirmed and closed

Both original sessions assessed corrected commit
`2be7616abc9dcef1ec5d2ab8219736e0ebca4d80`, parent
`d67609747e671278f9a6a4e973ea0a0832a8cad8`, sequentially without
edits. The complete [GPT confirmation](n2-vocabulary-reviews/batch-53-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-53-claude-confirmation.md)
are archived. Both final tables contain the exact twenty source-ID/article
associations and three CLEAN facets per row; these were checked against
the committed TSV rather than inferred from a CLEAN count.

Both completely reread the four changed cards, correction patch,
eleven complete corrective families/29 senses and five full old bodies.
They explicitly inherited the fourteen unchanged new cards, two reuses
and three primary kanji cards, with fresh reciprocal/mapping spot-checks.
Both inspected the exact twenty TSV rows. GPT reread all twenty
principals and relevant additional families; Claude additionally read
all twenty original public captures, resolving its earlier public-evidence
and brown-adjective qualifications. Neither made a fresh public
retrieval in confirmation. Author totals deduplicate to 257 complete
families/647 senses and 121 full old articles; reviewer scope is
reported separately, not equated to those totals.

Both accept four direct guard additions and the 酸性 link. GPT
acknowledges the additional geographical-belt and modern 徐々に
pairs missed in its initial pass. Claude explicitly corrects the
archaic 徐々 citation and accepts the independent modern family;
it also accepts the previously missed 末/すえ pair. Its provenance
style concern is withdrawn after inspecting an existing 大木 precedent.
Remaining optional register/example/contrast suggestions do not
establish required defects. The confirmation prompt's relative
"other reviewer" wording is ambiguous for a common two-model prompt;
the reports and dispositions correctly identify the contributions
above, and the historical prompt is preserved unchanged.

No teaching changed after confirmation. Closure preserves all
3,273 baseline identities/readings/titles/exclusions and easier
levels, exact raw source fields, selected/additional mappings and
the deterministic content manifest. The shared audit tracks 240
new-article primary reciprocal N2 pairs; existing 超/超過 is checked
separately, not incorrectly included as a 241st new-article pair.
The four complete native reports, actual models, exact prompts,
session continuity, allowlists, frozen inputs and zero edits are
authenticated by the author, not reviewer-executed Git checks.
Confirmations share adjudications and are not blind discoveries.
No live quiz draws, exhaustive ambiguity audit, controlled model
benchmark or native-speaker certification is claimed.

## Batch 52: N2:1022-N2:1041

**Status:** closed after authenticated independent reviews, evidence-based
corrections and original-session confirmations.

Twenty new articles: 足る, 段階, 短期, 炭鉱, 短所, たんす,
淡水, 断水, 単数, 団地, 断定, 短編, 誓う, 地下水, 近々,
近付ける, 近寄る, 力強い, 千切る and 地質. No existing
identity is reused or renamed.

The [batch packet](n2-vocabulary-batch-sources/batch-52.json) preserves
all raw fields and complete principal families. Actual author inspection
covered 203 selected complete families/517 senses, including twenty
principals/33 senses; all 150 comparison labels; 92 complete existing
articles; 34 component records; six complete kanji cards; and twenty
public lexical endpoint captures. Not all 295 captured families or all
150 captured old bodies are claimed read. Exact extraction failed for
近日中; its explicit removal reduced 258 requests to 257 and supplies
no positive lexical verification.

Eight primary reciprocal pairs appear in reading rows and Common words:
階/段階, 短/短期, 炭/炭鉱, 鉱/炭鉱, 短/短所, 団/団地,
短/短編 and 編/短編. Existing plain-text 短所/短期 examples are
linked rather than duplicated. Actual 短編 たんぺん is qualified
under 編's dictionary ヘン. All baseline kanji metadata is preserved.
Missing 淡 and 誓 cards remain plain text in teaching and present in
written-kanji metadata.

Selected source senses are separated from additional teaching:
単数 anchors grammatical sense 2; 力強い anchors reassuring sense 2.
Both near-future and spatial 近々 senses match the raw gloss, but
spatial sense 2 permits only ちかぢか, not きんきん. 炭坑-only
shaft sense 2 is not generalized to source 炭鉱. Public-backed estate,
target-state and social-association extensions do not invent pinned
sense numbers. 地質 ちしつ remains distinct from fabric-quality
じしつ. Raw "cut up fine" for 千切る is preserved without teaching
knife mincing as its ordinary action.

### Batch 52 - initial reviews and reconciliation

Common authored snapshot: `3d66845af7cc97508b6a8d4348f0792e2cbdb9c6`,
parent `ba5b4d4cb75a542fe74572dfb1efff1fe0788693`. Actual
`gpt-6.1-sol` and `claude-opus-5.5` reviewed sequentially with identical
blind prompts apart from model/family substitutions, scope and source access.
Both processes exited without edits before reconciliation. Native reports:
[GPT](n2-vocabulary-reviews/batch-52-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-52-claude-initial.md).
Exact prompts, actual models, frozen hashes/patch/blind derivative, permitted
private reads, absence of named forbidden reads and zero edits were
authenticated against native events. Private outputs remain unchanged;
public Markdown only replaces two-space hard line breaks with blank lines.
These are author-executed provenance checks, not reviewer-executed Git.

| Finding | Evidence-based disposition |
|---|---|
| GPT F01 | Add 段階/クラス: selected 1419950:2 is level/rank/grade; the old クラス body explicitly includes category/rank. Its complete 1044070:1 is not school-only. |
| GPT F02 | Add 短所/粗: complete 1586730:2 and the actual あら article teach personal/work flaws, not only fish trimmings. Existing 欠点 paths are nontransitive. |
| GPT F03; Claude B52-01 | Correct the shared 魚 explanation defect: ギョ is its ordinary on reading, not a compound-induced voicing change. Keep the correct whole reading たんすいぎょ. |
| GPT F04 | Add 単数/一: additional general 1417670:1 includes single/one; old 一's numeral 1160790:1 applies despite the grammatical source anchor. 一つ does not protect this pair. |
| GPT F05 | Add 断定/審判: complete 1360410:1 and the old body explicitly teach judgment/decision beyond sports officials. Broad judgment labels overlap. |
| GPT F06 | Add 短編/詩: selected 1597300:1 explicitly includes a short poem. Old 詩 and complete 1929950:1 teach poem/poetry, not merely a related literary topic. |
| GPT F07 | Remove all four 近付ける exclusions: its displayed bring-close/let-approach label preserves causation against the actual approaching labels. Complete movement families and old bodies do not establish interchangeable answers. Transitivity is not a universal disambiguator. |
| Claude B52-02 | Remove 力強い/がんがん: complete 1040570:3 does include colloquial vigorous activity, but the actual sound/headache title is not defensible for powerful/reassuring or vice versa. This is not denial of that secondary sense. |
| Claude B52-03 | Link all three substantive comparisons: 不足する to 不足, 遠く directly, and displayed 押入れ to the actual 押し入れ filename. Complete families and old bodies verify their identities. |
| Optional 短編 duration | Adopt 10分 for clarity; retain existing correct じゅっぷん and duration meaning. |
| Optional 足る constructions; 誓う addressee | No expansion: the existing practical constructions are sufficient; noun + に足る is not in the captured public evidence. Additional phrases are not repairs to incorrect current teaching. |
| Optional 地下水 naturalness | No change: the well-draws-up-water wording is comprehensible. The low-confidence から alternative does not establish a consequential defect or native-speaker judgment. |
| Optional 千切る split | No change: the article teaches whole ちぎる and explicitly rejects productive 千 = ちぎ. The warning is not a claimed constituent split; isolated 千 = ち does not justify a new allocation. |
| Optional 短所/下手; 段階/程度; 団地/住宅/アパート | No extra guards or removal of 程度: 下手 describes lack of skill rather than general shortcomings; complete 程度 includes grade/degree; generic housing or an individual apartment/building is not necessarily the grouped estate taught by 団地. These are bounded judgments, not absolute nonoverlap claims. |

The author read all 27 complete corrective families and sixteen complete old
word bodies, plus the full 魚 kanji card. Exact counts and hashes are recorded
and deduplicated against prior inspections. The eleven corrected new cards
add five and remove five direct declarations: fourteen guarded articles and
72 declarations remain. Raw source rows, mappings, baseline words and the
six reciprocal kanji edits are unchanged. At that point confirmation
remained pending; its outcome follows.

**Model contribution note:** across all report sections, both found the 魚
reading defect. GPT uniquely supplied five missing direct guards and removal
of four excessive movement guards. Claude uniquely supplied one different
excess-guard removal and three existing-card links, plus optional 10分
clarity. Both completely read twenty new cards and six kanji cards.
GPT read all nine family renderings and 112 old word bodies; Claude read
none of those renderings and seven old word bodies plus 魚 kanji.
Complementary coverage was useful, but unequal actual depth does not
establish controlled bias reduction or a general model ranking.

### Batch 52 - confirmed and closed

Both original sessions assessed corrected commit
`960be0a8245a50449de9d40f98a6706c933e966e`, parent
`3d66845af7cc97508b6a8d4348f0792e2cbdb9c6`, sequentially without edits.
[GPT confirmation](n2-vocabulary-reviews/batch-52-gpt-confirmation.md) and
[Claude confirmation](n2-vocabulary-reviews/batch-52-claude-confirmation.md)
each have twenty exact source-ID/article associations with all three
facets CLEAN. Both fully reread eleven changed articles, the actual patch,
27 complete corrective families/71 senses and sixteen complete old word
bodies plus 魚 kanji. Nine unchanged articles and six full kanji cards
are explicitly inherited, with fresh reciprocal/mapping spot-checks.
GPT also reread twenty complete principals/33 senses and all mappings;
Claude inherited principal evidence and rechecked the twenty TSV rows.
Tool requests and native usage support these read distinctions.

Both accept the corrections. GPT revises its initial acceptance of
力強い/がんがん. Claude accepts the 近付ける removals with medium
confidence after explicitly comparing the shared-English-verb
開く/開ける precedent; it considers short-poem protection borderline
but establishes no defect. Its remaining 足る/誓う/地下水 suggestions
are optional expansions, not required repairs. No actionable defect or
consequential unresolved claim remains in the assigned scope.

All four complete reports, exact prompts, actual models, original-session
continuity, private allowlists, absence of named forbidden reads and zero
edits are authenticated. Shared-adjudication confirmations are not blind
discoveries. No teaching change follows confirmation. Deduplicated author
totals are 220 complete families/559 senses, 156 labels and 101 complete
old word bodies, plus the additional 魚 card; these are not reviewer totals.
Closure changes only twenty draft statuses and audit documentation.
No live quiz, exhaustive ambiguity audit or native-speaker certification
is claimed.

## Batch 51: N2:1002-N2:1021

**Status:** closed after authenticated independent reviews, two correction
rounds and final original-session confirmations.

Twenty new articles: 助かる, 但し, 畳む, 立ち止まる, たちまち,
建つ, 発つ, 脱線, 妥当, 例える, 頼もしい, 足袋, ダブル,
だます, 溜まる, ダム, ため息 (source 溜息), ためらう,
溜める, だらしない. No existing identity is reused or renamed.

The [batch packet](n2-vocabulary-batch-sources/batch-51.json) preserves
the original source fields and complete principal families. The author
actually inspected 218 selected complete families/482 senses, including
twenty principals/36 senses; 178 existing labels; 108 complete existing
articles; 30 component records; three complete kanji cards; and twenty
public lexical endpoint captures. Not all 321 captured families or all
178 captured old bodies are claimed read. Public captures are author
retrievals, not fresh independent reviewer retrievals or frequency evidence.

Add primary reciprocal pairs 畳/畳む, 線/脱線 and 袋/足袋. 足袋
appears as a qualified whole-word reading たび rather than an invented
individual reading of 袋. Preserve all baseline kanji metadata.
Raw source errors remain auditable while the cards teach intransitive
建つ and ダム "dam." Source 溜息 is explicitly recognized in ため息.
At initial authoring, no independent review or model-comparison outcome
was claimed. Runtime quiz certification is not claimed.

### Batch 51 - initial reviews and reconciliation

Common authored snapshot: `9de757c1fdaff0d2012091652d43247998307d29`,
parent `e2edfb235baf79faefae1a7df0785d6f394cf2d4`. Actual
`gpt-6.1-sol` and `claude-opus-5.5` reviewed sequentially, with identical
blind prompts apart from model/family substitution, scope and source access.
Both processes exited without edits before reconciliation. Native reports:
[GPT](n2-vocabulary-reviews/batch-51-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-51-claude-initial.md).
Exact prompts, actual models, frozen hashes/patch/blind derivative,
permitted private reads, absence of named forbidden reads and zero edits
were authenticated against native events. These are author-executed checks,
not reviewer-executed Git or runtime quiz tests.

| Finding | Evidence-based disposition |
|---|---|
| GPT F01 | Accepted: add たちまち/すっと. Complete 1006140:1 and actual old body explicitly include "all of a sudden," not just smooth movement. |
| GPT F02 | Accepted: add 妥当/成立 and 妥当/適する. Complete 1375880:3 concerns valid/holding arguments; 1437340:1 and its old article concern suitability. Different grammatical forms do not settle these broad English labels. |
| GPT F03 | Accepted: add both 溜まる/重なる and 溜める/重なる directly. Complete 1335800:2 and the old body explicitly teach accumulation; indirect 重ねる/積もる paths do not protect either pair. |
| GPT F04 | Accepted: add ためらう/ぐずぐず. Complete 1004040:1 and the old body teach hesitation, not merely slow movement. |
| GPT F05 | Accepted: add だらしない/ぐしゃぐしゃ and だらしない/だらだら. Complete 2097580:3 is non-wet untidiness; 1007510:4 includes slovenly/lazy activity. Do not conflate wetness and untidiness merely through English "sloppy." |
| Claude B51-F1 | Accepted: add 例える/例え. Complete 1597120:2 and actual old teaching cover figurative comparison/metaphor, directly related to the broad new comparison label; not every shared-kanji noun/verb warrants a guard. |
| Claude B51-F2 | Accepted: add たちまち/一瞬. Complete 1163340 and old article include adverbial use and rapid-result 一瞬で. Noun-only reasoning does not account for the actual construction. |
| Claude B51-F3 | Adopted low-impact source-list consistency: append 足袋 entry 1404920 to 袋's final list. The same entry was already cited inline; no missing lexical evidence or changed reading is implied. |
| Author A51-01 | Add 妥当/立つ after complete follow-up inspection: 1597040:13 explicitly includes valid/logical/reasonable arguments. Not credited to either initial reviewer; distinct from the building-standing optional suggestion. |
| Optional 建つ/立つ | Not adopted: complete 1597040:2 is standing/situation, not being built or erected. Homophony and the shared building topic alone do not establish the new quiz pair. |
| Optional たちまち/瞬間 | Not adopted: actual old teaching and complete 1341210 distinguish an instant/point in time or momentary duration; no equivalent rapid-result construction was established here. This is a bounded decision, not a universal nonoverlap claim. |
| Optional 頼もしい/頼る and 助かる comparisons | No expansion: being reassuring/dependable, relying on help, and attributing help to a cause are different perspectives. Optional cautiousness was not established as a mandatory guard or excessive exclusion. |

The author actually read all fourteen complete corrective families and thirteen
old bodies, including optional candidates. Counts and hashes are retained in
the correction evidence, deduplicated against earlier inspections. Failed
reviewer retrievals are not positive evidence. No source mapping or practical
teaching prose changes were required.

**Model contribution note:** comparing findings, optional passages and limits,
GPT supplied eight required direct quiz pairs not reported by Claude; Claude
supplied two different required pairs not reported by GPT, plus the low-impact
source-list observation. There was no shared required pair. The additional
author-found valid-argument pair is not a model contribution. Both completely
read the twenty new cards and three kanji cards; GPT read all ten family
renderings and 116 old bodies, while Claude read targeted family records and
three old bodies. Complementary coverage was useful in this batch, but this
unequal actual depth does not establish bias reduction or a general model ranking.

### Batch 51 - first confirmation and follow-up

Both original sessions assessed corrected commit
`0e73b4e0028a0bb74940f2dbdc10e7890bb24ef9`, parent
`9de757c1fdaff0d2012091652d43247998307d29`, sequentially and without edits.
[GPT confirmation](n2-vocabulary-reviews/batch-51-gpt-confirmation.md)
accepted all corrections with twenty correctly associated all-CLEAN rows.
[Claude confirmation](n2-vocabulary-reviews/batch-51-claude-confirmation.md)
also accepted all corrections without regressions but found two original
quiz omissions. Its NEEDS FIX verdicts remain preserved, not rewritten.
Both fully reread the seven changed cards, 袋, fourteen complete corrective
families and thirteen old bodies; unchanged whole-body judgments were inherited.
GPT reread all twenty principals; Claude inspected targeted original passages,
five more old bodies and narrower mapping/evidence sections. Its fresh おどおど
fetch yielded navigation only, not positive lexical verification.
The four native reports, exact prompts, actual models, session continuity,
permitted private reads and zero edits were author-authenticated.

The first author reconciliation union was 227 complete families/507 senses,
185 labels and 116 complete old bodies. The author then read all five
complete follow-up families and five old bodies, including optional candidates;
the appended evidence records deduplicated totals and exact hashes.

| Follow-up observation | Disposition |
|---|---|
| Claude B51-C1, たちまち/一度に | Accepted: add the direct guard. Exact old title "all at once" collides with pinned 1288480:2 and the new card's acknowledged English rendering, despite meaningful Japanese grouping/suddenness distinctions. 1609210:1 confirms the unqualified label. |
| Claude B51-C2, ためらう/おどおど | Accepted: add the direct guard. The old title/body explicitly teach hesitant behavior, now also checked against complete 1001400:1. Not all nervousness is indecision, but the actual broad hesitation labels overlap. |
| Claude optional たちまち/さっさと | Adopted after author inspection as A51-02: 1005190:1 explicitly includes quickly, promptly, immediately and without delay. Actual prompt-action teaching directly overlaps immediate/rapid development; the absence of a surprise sense is not sufficient to reject all overlap. This began as an optional candidate, not an independent mandatory reviewer finding. |
| Claude optional 妥当/効力 and たちまち/一斉 | Not adopted: actual efficacy/legal-force and qualified simultaneous/group-action labels retain meaningful distinctions. Complete 1275250/1164040 and old bodies were inspected. No transitive inference from existing 有効/成立 or 一度に guards. |
| Claude optional stale N2:1006 source note | Refresh the current note to acknowledge 一瞬で, the unqualified 一度に label and prompt さっさと. Selected/additional senses and immutable source fields do not change; frozen earlier evidence remains historical. |

Current declarations become 105 on eighteen new cards: fourteen additions
from the authored snapshot, no removals or baseline-word guard changes.
Only two guard lists and one appended mapping note change in this follow-up;
no practical teaching prose or primary mapping changes.
The two new required pairs were not present anywhere in GPT's initial or
confirmation reports. They are useful additional Claude coverage, not
proof of depth-equivalent review or model superiority. Original-session
confirmation of this follow-up was required before closure.

### Batch 51 - confirmed and closed

Both original sessions confirmed final teaching snapshot
`0a2b27a7c7a86ac430f1ef367f5a0928607b8aba`, parent
`0e73b4e0028a0bb74940f2dbdc10e7890bb24ef9`, sequentially and without edits:
[GPT final confirmation](n2-vocabulary-reviews/batch-51-gpt-confirmation2.md)
and [Claude final confirmation](n2-vocabulary-reviews/batch-51-claude-confirmation2.md).
Each supplies twenty correctly associated all-CLEAN three-facet rows,
accepts both new required guards, the author-adopted promptness guard
and the refreshed note, and finds no new actionable defect.
GPT explicitly acknowledges its preceding CLEAN assessment missed the
two later omissions. Both keep original contribution attribution rather
than claiming shared-evidence confirmations as new blind discoveries.

Both completely reread the two changed cards, actual follow-up patch,
five complete families/six senses and five old bodies. GPT additionally
read all twenty principals and current mapping rows; Claude read selected
principal passages, the changed mapping row and broader targeted comparisons.
Unchanged whole-body judgments remain explicitly inherited.
Claude's fresh 急速 API retrieval was not the pinned snapshot; the author
separately read complete pinned 急速/どんどん families and actual old bodies.
Their final optional rate-of-progress/momentum candidates remain unadopted
within the qualified labels: neither established a required direct guard
or a reason to rewrite otherwise correct rapid-result teaching. This
is a bounded disposition, not a universal nonoverlap claim.
Optional efficacy/legal-force 効力 remains unadopted for the same
previously recorded evidence-based distinction.

All six complete native reports, exact prompts, requested/actual models,
same-session continuity, permitted private-file access, frozen snapshots,
patches, equivalent derivatives and zero edits were author-authenticated.
The twenty exact source-ID/article associations and three CLEAN cells per
row in both final reports were checked against the committed TSV, not
merely counted. Every reviewer process exited before the next began.

The author separately verified source preservation and note-only change,
all 3,273 baseline identities/readings/titles/exclusions, exact selected/
additional mappings, 230 tracked reciprocal N2 pairs, 4,219 word articles,
zero structural errors and deterministic manifest `5292fc0539eb3378`.
No confirmed teaching or manifest changes during closure. The batch
packet records precise deduplicated inspection totals, final optional
reads and all six authenticated report receipts. These are author-executed
checks, not reviewer Git execution, live quiz or native-speaker certification.
The project now has 1,020 closed rows and 792 pending; none are draft or
unresolved. The 1,012 mapped articles comprise 946 new and 66 reused articles.

## Batch 50: N2:982-N2:1001

**Status:** closed after authenticated independent reviews, reconciliation and bounded confirmation.

Scope: 体操, 大分 (reused だいぶ), 大木, 題名, 代名詞, タイア
(normalized タイヤ), ダイヤグラム, ダイヤモンド, ダイヤル, 対立,
田植え, 絶えず, 楕円, 高める, 耕す, 滝, 炊く, 焚く, 蓄える and 竹.

Sixteen new articles and four reuses bring the collection to 4,199 word
articles. Existing N4 だいぶ is byte-for-byte unchanged. 大木, 耕す and
竹 gain only sourced N2 metadata and appended coverage citations/notes;
their identities, primary readings/titles, original bodies and guards remain.
Two new reciprocal primary N2 pairs are 詞/代名詞 and 植/田植え.
Existing 耕/耕す and 竹/竹 reciprocity is preserved without new kanji edits.

The [batch evidence](n2-vocabulary-batch-sources/batch-50.json) preserves
all twenty raw rows, complete principal families and selected/additional
senses. The author actually inspected 240 complete dictionary families/
663 senses including twenty principals/33 senses, 176 existing labels,
122 complete old articles, 27 component records, four related kanji cards
and 22 public lexical endpoint captures. These are deduplicated inspection
counts, not independent verification or a claim that all 302 original
captured families were read. Public captures can include mixed headings.

Rare source タイア is explicitly recognized under タイヤ.
ダイヤグラム's transport-chart teaching is public-dictionary-backed,
not a fabricated second JMdict sense. Additional figurative, sports,
regional, heating, camera-flash, development and beard uses are identified
separately from their N2 source anchors where applicable.
No runtime quiz uniqueness is claimed.

### Initial review and reconciliation

Both short-lived processes reviewed clean authored snapshot
`8c71fae49b615f2d6f0de34c6b00d1b20d17dd7e`, parent
`89c812eed40575c62f9f24cf97f3f6866473ecd0`, sequentially with the same
scope, rubric and source access. GPT exited before Claude started.
Exact native prompts, snapshots, models, permitted private-file access,
absence of named forbidden reads, complete final reports and zero edits
were author-authenticated. File-only reviewers could not execute Git.

- [GPT initial report](n2-vocabulary-reviews/batch-50-gpt-initial.md):
  actual `gpt-6.1-sol`; one low-severity quiz finding.
- [Claude initial report](n2-vocabulary-reviews/batch-50-claude-initial.md):
  actual `claude-opus-5.5`; one quiz omission and one mapping defect.

| Initial observation | Evidence-based disposition |
| --- | --- |
| GPT B50-GPT-01: excessive 体操/体育 guard | Remove 体育 only. Complete 1409580 marks PE-class sense 3 obsolete; complete 1409200 and the actual 体育 body identify modern education/the subject. Keep the useful comparison and historical qualification. GPT also fetched the precise Kotobank 体育 entry; failed Weblio lexical extractions are not positive verification. |
| Claude B50-QZ-01: ダイヤグラム schedules | Add direct スケジュール and 時間割 exclusions after full-body and complete-family inspection (1068870/1315960). The original Digital Daijisen passage explicitly includes the operating schedule itself, not only its chart. Make that qualification explicit and link both comparisons; do not infer the pair transitively through ダイヤ or invent JMdict sense 2. |
| Claude B50-MAP-01: 竹 sense selection | Select 1422230 senses 1,2 and clear additional senses: the raw source gloss explicitly names both bamboo and the middle rank. Correct only the appended coverage note and mapping fields; preserve all original teaching and exclusions. |
| Claude optional sequence, lifting, increase and quarrel guards | No additional declaration adopted. Sequence versus continuity, physical lifting versus level enhancement, quantity increase versus degree enhancement, and a quarrel versus confrontation retain meaningful distinctions in the actual qualified labels. These suggestions were explicitly nondefects, not unresolved findings or proof of exhaustive nonoverlap. |
| Claude optional variant navigation and inherited 大木 wording | Nonblocking 貯 navigation is not required for the primary 蓄える mapping. Do not rewrite the preserved 大木 explanation outside this batch's narrow reuse. |

The [batch evidence](n2-vocabulary-batch-sources/batch-50.json) retains
exact corrective records and decisions. Thirteen new cards now declare
72 exclusions: two additions and one removal from the initial 71.
No baseline exclusion is changed. Only 竹's selected/additional sense
classification changes; all twenty original source rows remain intact.

The full reports, including Optional and Limits, contain no shared initial
actionable observation. GPT uniquely found the excessive modern PE guard;
Claude uniquely found the two schedule-label candidates and the explicit
source-gloss mismatch. Both inspected all assigned teaching files and
complete selected/supplemental family renderings, but GPT read 113
additional complete old bodies while Claude read four and mostly labels
for the rest. This is useful complementary signal on this sample, not
a controlled model-bias experiment or a general model ranking.
GPT explicitly acknowledges that its initial CLEAN assessments missed the
schedule guards and bamboo mapping; Claude accepts GPT's excessive PE guard
finding. These corrections remain complementary initial contributions,
not new independent discoveries during shared-adjudication confirmation.

### Batch 50 - confirmed and closed

Both original sessions confirmed correction commit
`bfc6d3d3e00525bc21aac101af8d06d7241b88f4`, parent
`8c71fae49b615f2d6f0de34c6b00d1b20d17dd7e`, sequentially and without edits.
Both completely reread the three changed articles, actual correction patch,
two new complete comparison families, three captured old bodies and precise
original relevant dictionary passages. Both accept all three corrections,
count 72 declarations on thirteen new cards and find no new actionable defect.
Unchanged whole-body judgments are inherited, not claimed as new full reads.

- [GPT confirmation](n2-vocabulary-reviews/batch-50-gpt-confirmation.md):
  actual `gpt-6.1-sol`; twenty correctly mapped all-CLEAN three-facet rows.
- [Claude confirmation](n2-vocabulary-reviews/batch-50-claude-confirmation.md):
  actual `claude-opus-5.5`; substantive corrections accepted, but four
  source-ID/article labels in its table were misassigned.
- [Claude corrected addendum](n2-vocabulary-reviews/batch-50-claude-confirmation-addendum.md):
  the same original session checks the actual TSV associations on the unchanged
  snapshot and supplies twenty correctly mapped all-CLEAN three-facet rows.
  N2:983 is だいぶ, 984 大木, 985 題名 and 986 代名詞.
  The original report remains unmodified. This bookkeeping correction changes
  no linguistic judgment and claims no new body reads.

All five complete native reports, exact prompts, actual models, session
continuity, permitted private-file access, absence of named forbidden reads
and zero edits were author-authenticated. Exact source-ID/article associations,
not only a set of twenty IDs and CLEAN cells, were checked before closure.
All short-lived reviewer processes have exited.

The two corrective families and two newly inspected old bodies bring the
author's deduplicated totals to 242 families/665 senses, 178 labels and
124 complete old articles. GPT's cumulative additional old-body scope is
115 beyond the four assigned reuses; Claude's narrower reads remain explicit.
There were no fresh public retrievals during confirmation.

The author separately checked exact raw-row preservation, selected/additional
senses, source-index hash, all 3,273 baseline identities/readings/titles and
established exclusions, reciprocal links and the deterministic manifest.
No teaching file changed after confirmation. File-only reviewers did not
independently execute those Git/hash checks; no live-quiz, exhaustive semantic
uniqueness or native-speaker certification is claimed. The batch's twenty
rows are now closed, giving 1,000 closed and 812 pending rows overall.

## Batch 01: N2:2-N2:21

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: あいかわらず, アイデア, アイディア, 曖昧, 遭う, 扇ぐ, 青白い,
あかんぼう, 明き, あきれる, アクセント, 欠伸, 飽くまで, 明け方, 揚げる,
挙げる, 憧れる, 足跡, 味わう, 預かる.

The draft adds **17 articles** and reuses `会う` (N5), `赤ん坊` (N4), and `空き` (N3).
The first two already teach the applicable source identities; `空き` gains explicit `明き`
alias teaching without changing its stable written form, primary reading, or level.
The collection now contains 3,290 word articles.

The [batch evidence](n2-vocabulary-batch-sources/batch-01.json) preserves the original rows,
selected mappings, complete relevant JMdict entry families and component evidence.
Ten existing kanji pages gain useful links, including reciprocal N2 links for
`伸`/`欠伸`, `跡`/`足跡`, and `預`/`預かる`. The existing `預ける` comparison gains a word link.

### Initial review

Both reviewers examined committed snapshot
`fe744d204feaeb554fce6df934cfafed81419be5`, parent
`94a175cdc06f3c7d1d09cbd8891b2a5ef370b18f`, with the same scope, rubric and source access.
They ran in separate short-lived processes, sequentially, with no nested agents or file edits.
The first process exited before the second began. Usage receipts verified the actual models:

- [GPT report](n2-vocabulary-reviews/batch-01-gpt-initial.md): `gpt-6.1-sol`.
- [Claude report](n2-vocabulary-reviews/batch-01-claude-initial.md): `claude-opus-5.5`.

All 17 new articles received three-facet verdicts. Both also assessed the changed passages,
the explicit 明き reuse, and the narrow unchanged 会う/赤ん坊 coverage claims.
The file-only reviewers could not independently run Git or verify frozen hashes; their reports
disclose that limit. The author checked the clean committed snapshot and exact changed-file scope.

### Reconciliation

The following changes are implemented and confirmed on the corrected snapshot:

| Initial finding | Decision and evidence |
| --- | --- |
| GPT F01 / Claude F1: あきれる and うんざり | Add their direct exclusion. Entry 1515580 sense 1 and the two actual articles teach the same "fed up" use. |
| GPT F02: 挙げる and 示す/収める/得る | Add all three direct exclusions. Entry 2864818 senses 1 and 11 explicitly cover showing examples and achieving/obtaining; the comparison articles' displayed labels overlap. |
| GPT F03: 味わう and 味 | Add a direct exclusion for the English "taste" ambiguity without changing the established noun label or pretending the Japanese noun and verb are interchangeable. |
| GPT F04: 曖昧 and 疑わしい | Add a direct exclusion for the separate suspicious/disreputable sense. Entry 1567920 sense 2 and Seisenban Nihon Kokugo Daijiten's 曖昧 sense 3 support the overlap; neither establishes its frequency or an independent N2 level. |
| GPT F05 / Claude Optional: missing navigation | Link 相 at the introduced spelling 相変わらず (shared observation); also link 示す in the explicit comparison (GPT-only observation). Keep kana-headword metadata unchanged. |
| Claude F2 and its weaker optional 普段 candidate | Add direct pairs with いつも and 普段 after inspecting their actual labels and complete entries 1188890 and 1497180. Their usual/habitual/always senses overlap the source entry's "as usual/as always" labels. This is not transitive inference through an existing exclusion. |
| Claude F3: 飽くまで wording | Clarify the mnemonic warning and identify あくまで, not an English gloss, as the potential mistaken substitute for やはり. Treat this as a clarity improvement: the original "not ... in every sentence" did not itself establish a false historical or modern meaning. |

The supplemental comparison entries and the exact external dictionary check are retained in the
[batch evidence](n2-vocabulary-batch-sources/batch-01.json). None of these changes alters the
original source fields, stable existing identities, readings or easier levels.

Optional expansions were not required for closure: more spellings/homophones for 扇ぐ, a figurative
そくせき lesson, a set phrase for あきれる, alternative 味わう examples, and dash style.
The suggested アイディア spelling-note polish is also optional. Counts of priority tags are not
used as a measured ranking of spelling frequency.

### Confirmation and closure

Both original model families independently checked correction commit
`2ca51500880851eae1d5cd3e6eef9ff7165d1329`, parent
`fe744d204feaeb554fce6df934cfafed81419be5`, against the actual six-article correction diff.
Each received only its own initial report, with the same bounded scope and source access:
eight direct exclusions, two navigation links and two clarified warnings. Neither received
the other review or the author's adjudication. GPT exited before Claude started; usage
receipts confirmed the requested models and no file edits.

- [GPT confirmation](n2-vocabulary-reviews/batch-01-gpt-confirmation.md):
  `gpt-6.1-sol`; initial F01-F05 resolved, all six changed-passage verdicts CLEAN.
- [Claude confirmation](n2-vocabulary-reviews/batch-01-claude-confirmation.md):
  `claude-opus-5.5`; initial F1-F3 resolved, all six changed-passage verdicts CLEAN.

Both found no actionable regression or consequential unresolved claim in the assigned changes.
The original whole-article verdicts and these bounded confirmations together support closure;
confirmation is not represented as a new full-pilot review. Their file-only Git/hash and
unexecuted-runtime limits remain explicit in the reports. The author verified the committed
snapshot, source/index integrity, baseline preservation and reciprocal links separately.

Claude's remaining wording polish for 飽くまで and optional 相 reading, comparison candidates
たいてい/普通, set phrase and alternative example are nonblocking suggestions. They do not
establish a defect in the reviewed snapshot and were not added merely to prolong review.
The first 20 source rows and batch evidence are now marked closed.

### Usefulness of two model families

The reports overlapped on the fed-up quiz collision and the 相 link, including Claude's Optional
section; those are not unique discoveries. GPT additionally identified the example/achievement,
taste-label and suspicious-sense collisions and the 示す link. Claude additionally identified the
habitual-adverb candidates and prompted clearer 飽くまで wording. The second review therefore
added useful signal on this shared pilot, but the sample is not a model ranking or proof of
exhaustive quiz-pair coverage. Severity differences were adjudicated by learning impact, not votes.

## Batch 02: N2:22-N2:41

**Status:** review-closed after sequential changed-passage confirmation.

Scope: 暖まる, 暖める, あたりまえ, あちらこちら, 厚かましい, 圧縮, 宛名,
あてはまる, あてはめる, 暴れる, 脂, あぶる, あふれる, 雨戸, 甘やかす, 余る,
編物, 編む, 危うい, 怪しい.

The batch adds **14 articles** and reuses six: あちこち (N3, explicitly teaching
あちらこちら), 怪しい (N2), and previously vocabulary-unclassified 暴れる, 脂, 余る
and 編む. Only the latter four gain explicit N2 metadata from these verified source rows;
their teaching text, stable identities and primary readings are unchanged.
No harder kanji-derived fallback is treated as vocabulary provenance.

The [batch evidence](n2-vocabulary-batch-sources/batch-02.json) retains the exact rows,
complete relevant dictionary families, restrictions and component evidence.
Ten existing kanji pages gain useful word links or examples. Reciprocal N2 links cover
厚/厚かましい, 圧/圧縮, 戸/雨戸, 甘/甘やかす and 編/編物; 温 also links the explicitly
taught 温まる/温める spellings to the new 暖まる/暖める articles.
The collection now contains 3,304 word articles. All 20 rows in this batch are review-closed.

### Initial review and reconciliation

Both reviewers independently read authored snapshot
`a0423388624ed50b0a348ad6f7dd7c212b3850b9` with the same assignment and evidence:
all 14 new articles, the actual ten-kanji/four-level-only diff and six narrow reuse claims.
The isolated `gpt-6.1-sol` process fully exited before `claude-opus-5.5` started.
Usage receipts verify those actual models and zero file edits; the author checked the clean
unchanged snapshot between runs.

Reports are archived without rewriting:
[GPT initial](n2-vocabulary-reviews/batch-02-gpt-initial.md) and
[Claude initial](n2-vocabulary-reviews/batch-02-claude-initial.md).
Both found the source mappings, related kanji passages and six reuse claims covered.

| Finding | Disposition | Evidence and change |
| --- | --- | --- |
| GPT B02-GPT-01 / Claude B02-CL-01 | Resolved; confirmed | あてはめる and 適用 both teach applying a rule to a case. Add the direct guard and comparison link. This is one shared finding, not two independent defects. |
| GPT B02-GPT-02 | Resolved; confirmed | 宛名 explicitly includes the recipient's name alone. Add direct guards against 名前 and 名, plus a qualified comparison; the existing 名/名前 guard is not transitive. |
| Claude B02-CL-02 | Resolved; confirmed | あたりまえでしょう is taught as "of course," also もちろん's displayed label. Add that direct guard and link without claiming unrestricted grammatical substitution. |
| Claude B02-CL-03 | Guidance gap resolved; unsupported body preference withdrawn | Inspect the actual official 2014 PDF, entry 007, which covers both verbs as well as adjectives. Add qualified room/air versus food/drink spelling guidance and examples of 温. The body/hand spelling preference was not established by this source: replace those examples without declaring their former spelling wrong or asserting an exclusive body rule. |

The four direct quiz guards address localized answer ambiguity; they are treated as minor
editorial defects rather than general quiz failure. The spelling issue is missing contextual
guidance, not an established false dictionary spelling. The supplementary
`reviewEvidence` retains complete comparison entry families, the inspected PDF's hash,
exact location and the body/hand limitation.

**Optional, not blocking:** broader 危うい constructions/register, additional figurative overflow,
編み物 frequency guidance, あちらこちら register, a transitive title paraphrase and other prose polish.
No frequency claim is added from a dictionary spelling list alone. The 温 card's "also teaches"
links already identify the destination spelling; reversing that wording is not necessary for correctness.

**Model-usefulness note:** both found あてはめる/適用. GPT uniquely identified the two missing
recipient-name guards. Claude uniquely identified the "of course" label guard and the actionable
暖/温 guidance gap, while its proposed body-specific preference exceeded the inspected evidence.
These observations include the reports' optional notes and limits; they are shared-sample evidence
for complementary review signal, not a ranking or proof of exhaustive coverage.

### Changed-passage confirmation

Correction snapshot: `ae22a9861e76507bf8080c062b85a587c1ddaddd`, with the actual five-file
diff and each model's own initial report. Fresh bounded `gpt-6.1-sol` and `claude-opus-5.5`
processes ran sequentially on that unchanged clean snapshot and exited with zero file edits.
Both found all five changed article contexts **CLEAN / CLEAN / CLEAN** for correctness,
scoped coverage and comprehensibility; no actionable regression or consequential unresolved
claim remained in those passages.

[GPT confirmation](n2-vocabulary-reviews/batch-02-gpt-confirmation.md) resolves both original
GPT findings. [Claude confirmation](n2-vocabulary-reviews/batch-02-claude-confirmation.md)
resolves all three original Claude findings, explicitly withdraws the unverified body-spelling
guess and supports the additional 宛名 guards. Remaining suggestions about example sequencing,
kana presentation, explanatory wording and grammatical detail are optional, not new defects.
The body/hand preference remains unestablished but is no longer asserted by these cards.

Limits: file-only reviewers relied on author-verified snapshot/hash receipts and the supplied
short extract from the inspected official PDF; neither independently parsed that PDF or ran
the app. Closure is scoped editorial acceptance, not a native-speaker or whole-corpus guarantee.
The mechanical audit preserves all 3,273 baseline identities/readings/titles/exclusions and
established levels, separately recording the four source-backed formerly absent levels.
Validation reports zero errors; manifest generation is deterministic at `275a7b984b18b4c8`.
Coverage is **40 closed, 0 draft, 1,772 pending, 0 unresolved**: 31 new and nine reused articles.

## Batch 03: N2:42-N2:61

**Status:** review-closed after sequential changed-passage confirmation.

Scope: 荒い, 粗い, あらすじ, 争う, 改めて, 改める, 著す, 有難い, 在る,
あれこれ, あわただしい, あわてる, 安易, 案外, アンテナ, 言い出す, 言い付ける,
意義, 生き生き, いきなり.

The batch adds **19 articles** and reuses unchanged ある (N5), which already teaches the
source spelling 在る and the relevant existence/location meaning. It is not merged with
the separate lexical item 或. Original source wording and dictionary restrictions are retained
in the [batch evidence](n2-vocabulary-batch-sources/batch-03.json); neither a shared reading
nor the source's English "live" establishes an unrestricted human-residence definition.

Twelve existing kanji cards gain useful linked examples. Required reciprocal N2 links cover
荒/荒い, 改/改めて, 改/改める and 著/著す. The existing 戦う comparison gains a link
to 争う. No kanji metadata or stroke data changes. The actual PDF of the official 2014
異字同訓 guidance was inspected for entries 014-016; the packet records the hash, location,
brief extracts and inspection limits.

The collection contains 3,323 word articles. Coverage is **60 closed, 0 draft, 1,752 pending,
0 unresolved**: 50 new and ten reused articles overall. All 20 rows in this batch are closed.

### Initial review and reconciliation

Both reviewers independently assessed authored snapshot
`eabe2e942e8e6fa67cc4dd4093c3e6ea14edaf3c`, parent
`f8eaca3bef6d3c90b5002e0d3b50b206acc73d5d`, on the same unchanged clean worktree.
The short-lived `gpt-6.1-sol` process exited before `claude-opus-5.5` began.
Usage receipts verify those actual models and no file edits. Reports are archived verbatim:
[GPT initial](n2-vocabulary-reviews/batch-03-gpt-initial.md) and
[Claude initial](n2-vocabulary-reviews/batch-03-claude-initial.md).

All 19 new articles received separate correctness, scoped-coverage and comprehensibility
verdicts. Both also assessed the twelve-kanji/one-word related diff and the narrow unchanged
ある reuse claim. Neither established a defect in the source mappings or related edits.

| Initial observation | Decision and evidence |
| --- | --- |
| GPT B03-GPT-01 / Claude Optional: 粗い and かさかさ | Add a direct guard for their rough-texture answer overlap. Inspect complete entries 1396910 and 1037130 and the actual cards; the guard does not say that 粗い implies dryness. |
| GPT B03-GPT-02: 争う and 議論 | Add a direct guard for the documented dispute/argument use. Entry 1400620 sense 2 and entry 1226160 sense 1 support it; the existing 論争 relationships are not transitive. |
| GPT B03-GPT-03: 生き生き and もりもり/ばりばり | Add both direct energetic-activity guards. Entry 1609130 sense 1, 1012700 sense 2 and 1010340 sense 4 support the actual working/activity meanings, not just an energy-related topic. |
| Claude F1: 著す and 著者 | Add a direct guard for the English noun/verb label "author." Keep stable labels and the distinct Japanese roles; entries 1427080 and 1427110 do not make a person and an action grammatically interchangeable. |
| Claude F2: あわただしい and あわてる | Add a direct guard after checking the actual hurried/hurrying uses in entries 1278810 and 1278830. A common exclusion with 急ぐ is not itself evidence or transitive protection. |
| Claude F3: unexplained "source" references | Rewrite the three learner-facing passages in あわただしい, 安易 and 言い出す as direct spelling/meaning guidance. The public cards need no knowledge of the contributor's source CSV. |
| Claude F4 / GPT Optional: 徐々に navigation | Link the existing comparison article from いきなり. This is the same observation in both reports despite different severity. |

The six quiz pairs address localized English-answer ambiguity; no lexical definition or
existing card's stable identity, reading, title, exclusion list or easier level changes.
Complete comparison families from the pinned hash-verified JMdict bytes are retained in the
batch packet. The roughness and 徐々に observations are shared, not unique model discoveries.
GPT additionally found the dispute and two energetic-activity guards. Claude additionally
found the author-role and hurried-activity guards and the unclear source references.
This is useful complementary signal on one common sample, not a model ranking.

Optional expansions remain nonblocking: additional semantic ordering or examples, historical
derivation, 生きる navigation, clearer "usually written" wording and polishing 彼 explanations.
Claude's optional gratitude candidates were checked against the actual 御礼 and ありがとう
cards and complete entry families. They teach related thanks or thanking expressions, but
that alone does not establish another missing direct answer-label guard for "grateful;
appreciated"; no additional defect is claimed or exclusion inferred through 感謝.

Initial-review limits remain explicit: neither reviewer ran Git, recomputed frozen hashes
or executed the app; both relied on the author-inspected official PDF extract. GPT's independent
live Jisho checks are JMdict-derived, not an independent dictionary tradition. Claude's
naturalness impressions for two constructions are not native-speaker certification; no contrary
evidence or consequential unresolved claim was established in the practical teaching scope.
GPT disclosed an incidental one-row TSV overread, which it did not assess or use.

### Changed-passage confirmation and closure

Correction snapshot: `f1bd2eb788772ddeb743f32cd818bb9b3d896081`, parent
`eabe2e942e8e6fa67cc4dd4093c3e6ea14edaf3c`. Both original model families received
the same actual eight-word correction diff, their own original report and the same bounded
evidence access. Fresh short-lived processes ran sequentially: GPT fully exited before Claude
started. Usage receipts confirm `gpt-6.1-sol`, `claude-opus-5.5` and zero file edits.

[GPT confirmation](n2-vocabulary-reviews/batch-03-gpt-confirmation.md) resolves B03-GPT-01
through B03-GPT-03, including both energetic-activity pairs, and confirms its optional 徐々に
link was implemented. [Claude confirmation](n2-vocabulary-reviews/batch-03-claude-confirmation.md)
resolves F1-F4 and confirms its optional roughness guard was implemented.
Each report accepts all six direct pairs and all eight changed contexts as
**CLEAN / CLEAN / CLEAN**. Neither establishes an actionable regression or consequential
unresolved claim within the assigned scope.

Claude's remaining warning-context wording, gratitude candidates, 生きる link and other
initial optional expansions remain nonblocking; confirmation does not turn them into defects.
No full-batch rereview or independent PDF/app execution is claimed. The initial full-article
assessments and bounded confirmations jointly support closure, with their file-only snapshot
and linguistic-certification limits preserved.

The author separately verified all 3,273 baseline identities/readings/titles/exclusions and
established levels, source/index integrity, twelve cumulative reciprocal N2 word pairs and
`stop-cran` authorship. The validator reports zero errors and repeated manifest generation is
deterministic at `ebc4e3f59c4d7584`. Source rows and the packet are now marked closed.

## Batch 04: N2:62-N2:81

**Status:** review-closed after sequential changed-passage and supplementary confirmation.

Scope: 育児, 幾分, 生け花, 以後, 以降, イコール, 勇ましい, 衣食住,
意地悪, いちいち, 一応, 一段, 一流, 佚, 一昨日, 一昨年, 一斉, 一旦,
一定, いってらっしゃい.

The batch adds **18 articles** and reuses the unchanged N5 一昨日 and 一昨年.
Both existing articles already explicitly teach the source on-readings
いっさくじつ and いっさくねん. Their primary native readings and levels remain
unchanged. The collection contains 3,341 word articles.
Three existing N2 kanji pages gain useful reciprocal word links:
児/育児, 勇/勇ましい, and 衣/衣食住.

The [batch evidence](n2-vocabulary-batch-sources/batch-04.json) preserves every
original field and complete relevant dictionary family. Source row N2:75 is
the noun 佚/いつ, not the unrelated N5 question word いつ. Its supplied gloss
resembles character meanings and does not match the supplied lexical entry.
The article teaches the noun established by pinned JMdict and the inspected
Seisenban Nihon Kokugo Daijiten entry, with a classical expression actually
found in Koji Seigo o Shiru Jiten. No modern frequency claim is inferred.
The blank original gloss for いってらっしゃい also remains blank in provenance.

Selected practical senses, spelling/reading restrictions, qualified temporal
boundaries, and direct quiz guards were independently reviewed. An authored
commit or successful structural check alone does not establish review closure.

### Initial review and reconciliation

Common frozen snapshot: `a14eb7276298c2231ac00aa70cea55948bb3e7fc`, parent
`760cf55d180e2ce3105ea569f9443632c653408c`. The same 18 articles, three
changed kanji contexts and two unchanged reuse claims were assigned to fresh
isolated `gpt-6.1-sol` and `claude-opus-5.5` processes. GPT fully exited before
Claude started, with no intervening repository edits. Usage receipts confirm
the actual models and zero file edits. Both [GPT](n2-vocabulary-reviews/batch-04-gpt-initial.md)
and [Claude](n2-vocabulary-reviews/batch-04-claude-initial.md) reports are archived
verbatim; neither initial reviewer saw the other report or author reconciliation.

The author checked the actual comparison articles and complete hash-verified
dictionary families before accepting direct guards:

| Initial observation | Decision and evidence |
| --- | --- |
| GPT04-01 / Claude F1: 幾分 reading classification | Resolve with the established native-first `wago` grouping and mixed-reading tag, explicitly explaining native いく + on ブン. KANJIDIC2 and the existing 場所 treatment support this; it is not a claim that both readings are native. |
| GPT04-02: 幾分 / 気持ち | Add a direct guard for 気持ち's ordinary slight-degree sense (entry 1591430, sense 4), not its unrelated feeling sense. |
| GPT04-03 / Claude F4: temporal cards / 来 | Add separate direct guards on both 以後 and 以降 for the "since" label taught by 来, entry 1547710 sense 2. Claude flagged 以降; GPT also flagged 以後. |
| GPT04-04 / Claude Optional: イコール / 同一 and 同様 | Add both direct equal/equivalent-label guards, supported by entries 1451900 and 1453550 sense 1. They were shared observations despite different severity labels. |
| GPT04-05: いちいち / あらゆる | Add a direct guard for the every-single/every label overlap, entries 1587320 sense 2 and 1586780 sense 1; keep the different attachment forms. |
| GPT04-06 / Claude F5: 一応 / およそ | Add the direct rough-assessment/roughly-label guard, entries 1161170 sense 1 and 1523450. Existing 大体 protection is not transitive. |
| Claude F5: 一応 / 約 and ほぼ | Add both guards after checking actual approximation titles and entries 1538100 sense 1 and 1551940 sense 2. Keep the valid "roughly" title rather than relabel it to disguise English-answer ambiguity. The guards do not turn 一応 into a general numerical estimator. |
| GPT04-07 / Claude F6 and Optional: 一流 / 上等 and 優秀 | Add two direct quality-evaluation guards, supported by entries 1354030 and 1539230 sense 1. 上等 was shared under Findings and 優秀 was shared across Findings/Optional. |
| GPT04-08: 佚 / ゆっくり | Add a direct guard for the leisure/rest use in entry 1013050 senses 1/3, not every slow-speed use. |
| Claude F2: 衣食住 collective gloss | Change the new title to "food, clothing and shelter," matching the heading and entry 1158780, rather than suggest independent alternative definitions separated by a semicolon. |
| Claude F3: comparison navigation | Add five missing link occurrences across 育児, 以後, 以降, 衣食住 and 一定, targeting the four existing cards 教育, 以前, 生活 and 変化. |
| Claude Optional: イコール / 平等 | Add a guard for the context-free equal/equality labels after checking actual equal-treatment/distribution teaching and entry 1507670 sense 1. This is not a claim that mathematical identity and equal treatment are identical concepts. |
| Claude Optional: 一斉 / 一緒 | Add a guard after verifying 一緒's ordinary same-time sense, entry 1163400 sense 4, as well as its actual together-action title. |
| Claude Optional: 一定 / 安定 | Add a guard for the fixed/constant versus stable-state answer overlap, entries 1164950 sense 2 and 1154120 senses 1/2. It does not impose exact numerical constancy on every 安定 situation. |
| Claude Optional: 一定 / 常に | No additional guard established: the inspected entry 1355970 and actual card concern always/constantly as frequency or continuity, not the fixed or prescribed value described by 一定. A related constancy theme alone does not establish another interchangeable answer label. |

The correction changes twelve new articles, adding fifteen direct quiz pairs,
five comparison links, one collective title correction and an explicit
native-first reading explanation. It preserves every baseline identity,
primary reading, title, exclusion list and established level. Complete newly
needed comparison families are retained in the packet; dictionary presence
is not itself a pairing decision.

The models supplied useful complementary signal on this common sample:
both caught the mixed reading, 来 on 以降, approximation and quality guards;
同一/同様 and 優秀 are shared even though Claude called them Optional.
GPT uniquely proposed 気持ち, 来 on 以後, あらゆる and ゆっくり.
Claude uniquely proposed the collective title fix, missing comparison links,
約/ほぼ and the additional 平等/一緒/安定 candidates.
No ranking or general model-performance conclusion follows from one batch.

Other optional collocation, register, polite-greeting and kanji-stem expansions
remain nonblocking and are not used to extend unchanged cards' review scope.
Both initial reviewers independently retrieved the relevant Kotobank
temporal and 佚 entries. GPT also retrieved Jisho comparison entries; that
is independent retrieval of JMdict-derived data, not another dictionary
tradition. Neither executed Git, recomputed hashes or ran the app. Claude's
wrong 一定 lookup is explicitly not evidence; the article's の/suru patterns
remain supported by the pinned dictionary. Naturalness judgments are not
native-speaker certification.

### Changed-passage confirmation

Correction snapshot: `68380b7c43f3dc42c56f88e5639b525357dd4e85`, parent
`a14eb7276298c2231ac00aa70cea55948bb3e7fc`. Fresh original-family processes
ran sequentially on the unchanged corrected commit, with their own initial
reports and the actual twelve-file diff. Usage receipts verify `gpt-6.1-sol`,
`claude-opus-5.5` and zero file edits. Both reports are archived verbatim:
[GPT confirmation](n2-vocabulary-reviews/batch-04-gpt-confirmation.md) and
[Claude confirmation](n2-vocabulary-reviews/batch-04-claude-confirmation.md).
Both accept all twelve changed contexts and fifteen direct pairs as
**CLEAN / CLEAN / CLEAN**, with no actionable regression or consequential
unresolved claim in scope. They resolve their original findings and independently
support leaving the frequency adverb 常に unguarded against 一定.

Claude's optional confirmation notes identify two further approximation-label
candidates, くらい and ほど. Their actual cards and complete pinned entries
1154340 sense 1 and 1436510 sense 6 support cautious direct guards against
一応's "roughly" label. Different syntax and fewer shared candidate-selection
features do not eliminate fallback answer-label ambiguity. These two pairs
are added in a separate one-file follow-up; they do not turn 一応 into a
general numerical approximation particle or alter either baseline card.
They receive the supplementary changed-passage confirmation recorded below.

Other confirmation suggestions about 幾分 wording and teaching 気持ち's
additional adverb sense remain optional. Neither report independently verifies
Git, frozen hashes or app execution; no new full-batch review is claimed.

### Supplementary confirmation and closure

Supplementary snapshot: `dd4d6de435d91c2ab362a89660d97b173a9cf8d1`, parent
`68380b7c43f3dc42c56f88e5639b525357dd4e85`. The actual one-line diff
adds only the two 一応/くらい and 一応/ほど guards. Fresh `gpt-6.1-sol`
and `claude-opus-5.5` processes reviewed that same unchanged commit
sequentially, with each model's own reports and the same bounded evidence.
Usage receipts confirm actual models and zero file edits. Their verbatim
[GPT supplement](n2-vocabulary-reviews/batch-04-gpt-supplement.md) and
[Claude supplement](n2-vocabulary-reviews/batch-04-claude-supplement.md)
both accept correctness, scoped coverage and comprehensibility as **CLEAN**.
No actionable regression or consequential unresolved claim remains in scope.
Claude explicitly withdraws its earlier optional retitling alternative;
English-label ambiguity should not be hidden by cosmetic rewording.

The eighteen initial whole-article reviews, three related kanji-context
assessments, two unchanged reuse checks, twelve-file confirmations and
one-line supplementary confirmations jointly support this batch's closure.
All six reports retain their file-only snapshot/hash and app-execution
limits; scoped acceptance is not native-speaker certification or an
exhaustive whole-corpus semantic guarantee.

The author separately verified all 3,273 baseline identities, readings,
titles, exclusion lists and established levels, exact source/index
integrity, fifteen cumulative reciprocal N2 word pairs and `stop-cran`
authorship. The seventeen correction pairs preserve all baseline metadata.
Validation reports zero errors and repeated manifest generation is
deterministic at `8d6cfcd10efadd70`. Coverage is **80 closed, 0 draft,
1,732 pending, 0 unresolved**: 68 new and twelve reused articles overall.
The collection contains 3,341 word articles; all twenty batch rows and the
evidence packet are marked closed.

## Batch 05: N2:82-N2:101

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

The twenty rows add **nineteen articles**: いってまいります, いつのまにか,
移転, 井戸, 緯度, 従姉妹, 威張る, 嫌がる, いよいよ, 煎る,
入れ物, インキ, インタビュー, 引力, ウーマン, ウール, ウェイトレス,
植木, 飢える. Source 煎る and 炒る explicitly share the cooking article;
neither maps to the unrelated existing existence verb いる.

The [evidence packet](n2-vocabulary-batch-sources/batch-05.json) retains
the original source fields, complete relevant families, exact sense mappings,
component records and complete comparison families. Source ウエートレス
maps to primary dictionary reading ウェイトレス with explicit search-variant
teaching; the original form remains unchanged in provenance. The departing
speaker's formal greeting is distinguished from the send-off reply, and the
female-cousin article preserves the whole-word reading いとこ.

Three N2 kanji pages gain reciprocal links: 移/移転, 戸/井戸, 植/植木.
Existing 従兄弟 and インク gain narrowly related comparison links.
No baseline identity, primary reading, title, exclusion list or sourced
level changes. The collection contains 3,360 word articles.

Actual Digital Daijisen entries for 煎る and 炒める support the qualified
cooking comparison. The failed initial search endpoint and an unsupported
always-without-oil search-summary claim are not treated as evidence.
These twenty rows remained draft until correction confirmation and the
separate author coverage audit were complete.

### Initial review

Both reviewers examined the same unchanged clean authored snapshot
`7cc99e2535f9e4ac917278a5b4f2e49db954e4fa`, parent
`5a85c2bc96780a9d2fdb2df0e64d33887bbb7902`, with identical scope,
rubric and source access. Separate short-lived processes ran sequentially:
GPT exited before Claude started. Usage receipts verify actual models
`gpt-6.1-sol` and `claude-opus-5.5` and zero file edits.

The verbatim [GPT report](n2-vocabulary-reviews/batch-05-gpt-initial.md)
finds no actionable defect. The verbatim
[Claude report](n2-vocabulary-reviews/batch-05-claude-initial.md) makes
four localized recommendations in three new articles. Both assess all nineteen
articles, the five existing-card passages and the explicit alias mappings;
neither claims comprehensive review of unchanged comparison cards.

### Reconciliation

| Initial observation | Decision and evidence |
| --- | --- |
| Claude R1: いつのまにか/こっそり English-answer ambiguity | Add the direct exclusion. Actual titles overlap through "unnoticed"/"without being noticed"; complete entries 1188850 and 1004520 distinguish observer unawareness from secret action without removing that English-label ambiguity. |
| Claude R2: unexplained departure/secrecy sentence | Replace the dangling departure reference with a named, linked こっそり comparison. Explain the contrast directly without asserting that an unnoticed event must be secret or that the Japanese adverbs substitute unrestrictedly. |
| Claude R3: "Uman" obscures vowel length | Keep ウーマン itself in the English translation. The existing long-vowel explanation remains unchanged; no competing romanization convention is introduced. |
| Claude R4: missing practical インキ/インク usage guidance | Add qualified consumer stationery/home-printer versus printing-industry terminology guidance. Actual T&K TOKA and Printing/Binding Terminology Online Dictionary pages corroborate the convention. Do not adopt a blanket ban on プリンターのインキ, measured frequency, unverified historical dating, or a material-composition boundary. |

The added complete comparison family and exact external inspections are
retained in the evidence packet. The search response contained inconsistent
alternate URLs; those were not treated as evidence. Only actually fetched,
relevant pages support the usage note. The separate インキ article is
justified by its distinct source entry, not by inventing a different
substance or requiring an absolute register split.

Claude's optional expansion candidates remain nonblocking: additional
いよいよ senses, a 鉢 gloss or 植木鉢 example, another 戸 voicing note,
additional cousin spellings and reciprocal インク usage guidance. Its
tentative えばる register and ウエートレス frequency suggestions were
not verified and are not promoted into teaching claims.

**Model-usefulness note:** the three correction groups are unique
to Claude in this sample, including comparison against GPT's Optional
and Limits sections. R1 and R2 concern the same comparison, affecting
the quiz and explanation respectively; they are not counted as two
independent discoveries. Both independently support the alias mappings,
component links and qualified cooking contrast. This is useful
complementary coverage, not a general ranking or a reason to adjudicate
future disagreements by model identity.

### Confirmation and closure

Correction commit `52b52704688827a30f8937a5930433b2f7cef8f0` directly
follows the authored snapshot. The actual frozen content diff contains
only the three correction contexts above. Each original model family
received its own initial report, the same bounded prompt, revised source
evidence and exact diff, without the other report or author adjudication.

The verbatim [GPT confirmation](n2-vocabulary-reviews/batch-05-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-05-claude-confirmation.md)
are CLEAN in all three facets for those contexts. Claude explicitly marks
R1-R4 resolved; GPT independently accepts the revisions without inventing
an original finding. Both fetched and inspected the actual two usage pages.
Neither claims another full-batch review or native-speaker certification.
Sequential processes exited without file edits; usage receipts verify
the actual original models.

The proposed viscosity detail and reciprocal インク note remain optional.
Technical properties of particular printing inks are not needed for this
lexical distinction and should not become a new spelling-based material
boundary. No actionable defect or consequential unresolved claim remains
in the assigned scope.

The author separately verified the exact source/index mappings, all
3,273 baseline identities, readings, titles, kanji arrays, exclusion lists
and established levels, eighteen cumulative reciprocal N2 pairs and
`stop-cran` authorship. The corrected content validates with zero errors;
repeated manifest generation is deterministic at `a7c3668223ea557e`.
Coverage is **100 closed, 0 draft, 1,712 pending, 0 unresolved**:
87 new and twelve reused articles overall. The collection contains
3,360 word articles; all twenty batch rows and the packet are closed.

## Batch 06: N2:102-N2:121

**Status:** closed after independent initial reviews, corrections and bounded confirmations.

The twenty rows add **sixteen articles**: 浮かぶ, 浮かべる, 承る,
受け取り, 受け持つ, 薄暗い, 薄める, 打ち合わせ, 打ち消す, 映す,
写る, 映る, うどん, 有無, 敬う, 裏返す. Explicit spelling mappings are
浮ぶ to 浮かぶ, 受取 to 受け取り, and 打合せ to 打ち合わせ.
The existing 浮く, うっかり and 埋める gain sourced N2 labels;
討つ already covers its source row and retains N3 unchanged.
No existing identity, reading, title or exclusion list changes.
The collection now contains 3,376 word articles.

The [evidence packet](n2-vocabulary-batch-sources/batch-06.json) retains
all original rows, complete main and comparison families, selected senses,
component records and actual external inspections. The actual Daijisen
受取 entry supports a written receipt as well as receiving; its unrelated
reading and failed search-generated URLs are not evidence for this noun.
Seisenban supports the humble uses of 承る.
Official 異字同訓 entry 025, printed page 8, supports the practical
recording/display distinction and explicitly admits overlapping camera
contexts. The encyclopedia's Chinese-derived name history supports
うどん's grouping, not invented modern character readings.

Five new reciprocal N2 pairs are 承/承る, 薄/薄暗い, 薄/薄める,
敬/敬う and 裏/裏返す. Existing N3 浮 gains useful linked examples;
会議 and 写す gain narrow word-comparison links.
埋/埋める was already reciprocal. Direct exclusions were assessed
against actual English labels and complete entries, including receiving,
floating, responsibility, image, respect and sound-negation uses.
All twenty source rows are review-closed after the confirmations recorded below.

### Initial review

Both initial reviewers examined clean authored commit
`4c40b75eb68980ad3744c172f8adac8c32016342`, parent
`59801b4d48ce48f27a165f6e9431e6e082bc5fec`, with the same frozen
scope, rubric and source access. Sequential isolated processes used
`gpt-6.1-sol` and `claude-opus-5.5`; each exited without editing files.
The verbatim [GPT report](n2-vocabulary-reviews/batch-06-gpt-initial.md)
and [Claude report](n2-vocabulary-reviews/batch-06-claude-initial.md)
cover all sixteen new articles, ten related passages, four reuse claims
and three aliases. Neither claims comprehensive review of unchanged
comparison cards.

### Reconciliation

| Initial observation | Decision and evidence |
| --- | --- |
| GPT F01a: 浮かぶ/現れる and 浮かぶ/出る | Add both direct guards. Complete entries 1497430 sense 2, 1263510 and 1338240 support appearance; the actual Seisenban 浮ぶ entry [1][二]② corroborates outward appearance. Their existing mutual guard is not transitive. |
| GPT F01b: 浮かべる/表す | Add the direct guard for facial expression. Complete entries 1497360 sense 2 and 1263490 sense 3, plus actual Daijisen 浮べる sense 2, support the overlap. This does not assert unrestricted Japanese substitution. |
| GPT F01c: receiving/acceptance labels | Add 受け取り/頂戴, 承る/頂戴 and 承る/受付. Complete receiving, humble accepting and request-acceptance families support these context-dependent overlaps; existing guards through いただく or 受け取り do not close them. Humble formulas remain construction-sensitive. |
| Both: 打ち合わせ/会合 | Add the direct guard. Complete entries 1588140 sense 1 and 1198530 sense 1, and actual Seisenban 会合 sense ①, support a meeting for consultation/discussion despite the preparatory nuance. |
| GPT F01e: 映る/似合う | Add the guard for recognized visual harmonizing, supported by 1173710 sense 1, 1314680 and actual Seisenban 映る sense ②. Keep the reflection/display lesson focus; neither older example dates nor absence of an archaic flag measures current frequency. |
| Both: missing 合わせる and 肯定 links | Link the substantive component explanation and antonym to their existing articles. Their teaching and actual complete comparison families support the uses. |
| Claude B06-02: unnamed homophone warning in 有無 | Name 生む・産む (うむ), "give birth; produce," with complete family 1588410 as evidence. Remove the unrelated computer-flag aside, which Claude also identified as optional polish. No new homophone article is needed. |
| Both: official PDF returned unreadable binary | Expose the same exact cached-page extraction to both confirmation reviewers with source URL, PDF SHA256, page locator and extraction hash. They can independently interpret entry 025 and its footnote, but shared author-extracted evidence is not independent reviewer retrieval. No demonstrated spelling error calls for changing the supported recording/display guidance. |

The packet retains eight additional complete comparison families (including
the separate 表す/ひょうす family, not used for あらわす), four exact
monolingual inspection receipts and provenance for the readable official page.
The actual footnote supports recording versus reproduction/display, including
playback and live-camera viewpoints. It does not impose a photograph/video
partition. The PDF's adjacent 生む/産む entry is not used to invent a
spelling division beyond the simple homophone warning.

Claude's optional extra examples and lexical expansions remain nonblocking:
tone-down 薄める, vacancy-filling 埋める, receipt-document preferences,
かき消す, 思い浮かべる, 裏返る and additional N4 backlinks.
The comment about 出会い does not establish an exclusion: its encounter
meaning is distinct from a preparatory meeting. No measured frequency
claim or new general substitution restriction is adopted.

**Model-usefulness note:** both independently found the 会合 guard,
both missing links and the unreadable-PDF evidence gap. Compared across
the entire reports, GPT uniquely proposed seven additional direct guards
for appearance, expression, receiving/acceptance and harmonizing.
Claude mentioned 領収書 preferences, not these 頂戴/受付 pairs.
Claude uniquely identified the unnamed 有無 homophone warning and
the removable computer aside; these form one local clarity correction.
Both independently accepted the aliases, reuse claims, conjugations,
transitivity and written-kanji metadata. This is complementary evidence
on one sample, not a general model ranking.

### Confirmation and closure

Correction commit `2a93457f855a5e6a92ee3b09287db81a29e53ab3`
directly follows the authored snapshot. Each original family received its
own initial report, the identical bounded prompt, actual eight-file diff,
revised evidence and identical readable official passage, not the other
report or author adjudication.

The verbatim [GPT confirmation](n2-vocabulary-reviews/batch-06-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-06-claude-confirmation.md)
are CLEAN on all three facets for the eight changed contexts and the
exact unchanged guide attributions in 映す, 写る and 映る.
Each reconciles its original findings and independently interprets the
readable entry and footnote. Both expressly distinguish shared cached
extraction from independent PDF retrieval; the precise attribution gap
is resolved without rewriting the supported teaching. Both processes
exited without edits and used the original actual models.

Claude additionally proposed optional generic-appearance guards for
写る/映る against 出る/現れる. Inspection of the actual titles,
photographic/screen appearance examples and complete entries supports
these four narrower/broader English-answer overlaps. They are adopted
as a bounded metadata supplement, not a demand to expand the lexical
lessons or a defect in the preceding correction. These were unique
useful optional observations by Claude in the confirmation, not a blind
initial-review discovery. The suggested "image being played back"
wording is optional; the existing displayed-image sentence is accurate
in its recording/playback context.

Supplement commit `b75d1d1f75d56c67f2b5fc14b2c4d681c7c4da52`
directly follows the correction commit. Both original families independently
checked its exact two-file, two-line metadata diff, actual comparison cards
and complete pinned dictionary families. Each received the same bounded
prompt and only its own preceding confirmation, not the other report
or the author's adjudication. GPT exited before Claude started; usage
receipts verified `gpt-6.1-sol` and `claude-opus-5.5`, with no file edits.

The verbatim [GPT supplement](n2-vocabulary-reviews/batch-06-gpt-supplement.md)
and [Claude supplement](n2-vocabulary-reviews/batch-06-claude-supplement.md)
are CLEAN on all three facets for all four direct pairs. Both distinguish
image-appearance overlaps from unrestricted Japanese substitution.
Neither adds an optional expansion or establishes a regression.
Their file-only Git/hash limits remain explicit. Claude also notes that
the generated manifest is outside its allowed two-line content diff;
the author independently checked the full committed scope and regenerated
manifest, rather than attributing that check to the reviewer.

No actionable defect or consequential unresolved claim remains in the
assigned scope. These twenty rows are closed; no full-batch re-review
or native-speaker certification is claimed. Cumulative coverage is
**120 closed, 0 draft, 1,692 pending and 0 unresolved** source rows,
mapped to 119 articles (103 new and sixteen reused).

## Batch 07: N2:122-N2:141

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 裏口, 占う, 恨み, 恨む, 羨ましい, 羨む, 売上, 売り切れ,
売り切れる, 売行き, うろうろ, 運河, うんと, 英文, 英和, ええと,
液体, エチケット, 絵の具 and エプロン.

The batch adds **eighteen articles** and reuses the established うろうろ
and 液体 articles, adding only newly sourced N2 metadata to those two.
Source 売上 is explicitly taught under 売り上げ. Search-only source
spellings 売行き and ええと are explicitly recognized under 売れ行き
and えっと, without being promoted to preferred production spellings.
The collection now contains 3,394 word articles.

The [batch packet](n2-vocabulary-batch-sources/batch-07.json) preserves
all twenty original rows, complete relevant main and comparison JMdict
families, spelling/reading restrictions, selected senses and hash-verified
KANJIDIC2 component evidence. Actual-entry inspection receipts support
the qualified 売り上げ/売れ行き comparison, the broader purposes of
canals and the quantity/degree uses of うんと.

Three N2 kanji pages gain reciprocal examples: 裏/裏口, 占/占う and
河/運河. 液/液体 is already reciprocal. 恨 and 羨 remain in word
metadata but have no existing kanji cards; no broken links or additional
kanji scope are introduced. Four existing word passages gain useful
links: ペンキ to 絵の具, and あの/さあ/まあ to the explicitly taught
ええと variant under えっと. Together with the two metadata changes,
the related content scope is nine existing files.

The authored commit did not claim review closure. All twenty source
rows are now closed after the confirmations below.

### Initial review

Both initial reviewers examined clean authored commit
`0648ec4f05747bfcfbc7d56fb82cf6ad20076ea7`, parent
`2500e68f52564eafccb432331df5b1681b5bf11b`, with the same scope,
rubric and source access. The GPT process exited before Claude started.
Usage receipts verify `gpt-6.1-sol` and `claude-opus-5.5`, with no file
edits. Both read all eighteen new articles and assessed the nine related
passages, two reuse claims and three explicit aliases.

The verbatim [GPT report](n2-vocabulary-reviews/batch-07-gpt-initial.md)
and [Claude report](n2-vocabulary-reviews/batch-07-claude-initial.md)
record their independent assessments. Both independently retrieved the
four relevant Kotobank passages; neither independently executed Git,
verified the frozen hashes, or ran the app.

### Reconciliation

| Initial observation | Decision and evidence |
| --- | --- |
| GPT N2B07-GPT-001: three degree guards | Add うんと/大変, うんと/実に and うんと/相当. Complete pinned entries 1415000 sense 1, 2820720 sense 1 and 1401240 sense 5 support the actual cards' very/high-degree uses. The separate 実に/まことに and 実に/げに families are preserved but not used for the じつに claim. |
| Claude F-01: 英和/字引 | Add the direct guard. 字引's actual title and complete family 1315140 say dictionary; English-Japanese dictionary is an ordinary abbreviated 英和 use. An existing 辞書 guard cannot transitively cover 字引. |
| Claude F-02: sold-out/run-out labels | Add 売り切れ/無くなる and 売り切れる/無くなる. Complete entry 1529550 sense 2 supports exhausted supply, overlapping the sold-out result in the actual new articles. This does not make every disappearance a selling-out event. |
| Claude F-03: 裏口/玄関 | Add the direct English-answer guard. The actual 玄関 title says entrance/entryway, and complete family 1263400 includes those broad glosses. This resolves a standalone English-label ambiguity, not an asserted equivalence between an ordinary home's front entrance and rear service entrance. |
| Claude Optional: 売れ行き/売れる | Adopt the direct guard after inspecting both complete families and actual sales-performance examples. The displayed how-well-goods-sell and sell/sell-well answers can overlap without making the noun and verb interchangeable or claiming all 売れ行き is good. |
| Claude Optional: localized wording | Use natural English "read the future" for the card-divination example. Remove the unmotivated profit warning in 売り上げ's formation paragraph and the unnecessary i-adjective/verb negatives in 英和 and えっと. No Japanese example or lexical scope is changed. |

Seven additional complete comparison families are retained in the packet;
the two other inspected families were already in the initial evidence.
Both compressed and expanded source hashes were checked again.

The remaining optional expansions are not defects: 羨ましがる, figurative
裏口, English-literature 英文 and 咳エチケット are outside the selected
practical focus. No frequency or register rule is added for うんと, and
the search-only flag on ええと is not turned into a claim that the form
is incorrect or rare. Claude's failed additional headword lookup does
not establish commonness either.

**Model-usefulness note:** no initial actionable finding was shared.
GPT uniquely established three high-degree answer overlaps. Claude
uniquely proposed four further direct pairs in Findings and one adopted
sales-performance pair in Optional, as well as the four small wording
improvements. Attribution compares the complete reports, including
Optional and Limits; it is not a general model ranking. Both accepted
the source mappings, aliases, written-kanji metadata, reciprocal links
and scoped reuse claims.

### Confirmation and closure

Correction commit `db3b5da1cc064a8d9e58742643378e13b3850bea`
directly follows the authored snapshot. Each original model family
received its own initial report, the same bounded confirmation prompt,
the exact nine-file content diff and the same revised evidence.
Neither received the other report or author adjudication. Separate
short-lived read-only processes again ran strictly sequentially;
GPT exited before Claude started. Usage receipts verify the actual
models and no file edits.

The verbatim [GPT confirmation](n2-vocabulary-reviews/batch-07-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-07-claude-confirmation.md)
are CLEAN on all three facets for all nine changed contexts. Each
independently assesses all eight new direct pairs and four prose edits,
reconciles its original findings and identifies no regression. Both
distinguish the actual 実に/じつに family from the other readings and
English-answer ambiguity from unrestricted Japanese substitution.
Their file-only provenance and unexecuted-app limits remain explicit.

Claude's additional past-tense wording suggestion is optional: English
"read" is a valid past tense in the translated 占いました example,
although its spelling also permits a present-tense reading in isolation.
No further correction is necessary; this observation is not counted as
a newly discovered defect.

No actionable defect or consequential unresolved claim remains in the
assigned scope. Cumulative coverage is **140 closed, 0 draft, 1,672
pending and 0 unresolved** rows, mapped to 139 articles (121 new and
eighteen reused). The collection has 3,394 word articles and 26 new
reciprocal N2 kanji-word pairs across these seven batches. This is not
whole-corpus or native-speaker certification.

## Batch 08: N2:142-N2:161

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 偉い, 宴会, 園芸, 演劇, 円周, 遠足, 延長, 煙突,
追い掛ける, 追い越す, オイル, 応援, 王女, 応ずる, 応接,
応対, 往復, 欧米, 応用, オーケストラ.

Nineteen new articles and the existing 偉い article cover the twenty
rows. 偉い gains only its sourced N2 level; its identity and teaching
are unchanged. 追い掛ける explicitly teaches 追いかける as well.
応ずる has its own source identity and article, linked to existing 応じる;
the 応じ- forms are not treated as evidence of an unrelated action.

Seven N2 kanji pages gain reciprocal examples:
芸/園芸, 劇/演劇, 周/円周, 延/延長, 接/応接, 復/往復 and 欧/欧米.
Existing パーティー, 芝居, 女王, 追う, 延期 and 西洋 gain links
at their existing substantive comparisons. 応じる gains a narrow
related-form note and link. No existing stable ID, primary reading,
title, easier level or exclusion list changes.

The [batch evidence](n2-vocabulary-batch-sources/batch-08.json)
preserves the original rows, complete principal families, component
records, 142 complete comparison families and nine actual-entry
inspection receipts. Homographs, sense restrictions and qualifications
are retained: 女王's law-specific princess use does not redefine queen,
and 回り does not inherit 周り's circumference sense merely by reference.
The receipts distinguish the dictionary sections that actually rendered;
they are author observations, not independent reviewer retrieval.

Structural, baseline, mapping and reciprocal-link checks pass. Two
manifest builds agree: 6,041 files, including 396 images and 201 scene
catalogs; content version `a8cbab29dc491588`. There are now 3,413 word
articles. Cumulative drafted/closed mappings cover 159 articles:
140 new and nineteen reused, with 33 reciprocal N2 kanji-word pairs.
These authored counts do not claim review closure.

### Initial reviews and evidence-based corrections

The [GPT report](n2-vocabulary-reviews/batch-08-gpt-initial.md)
(`gpt-6.1-sol`) and
[Claude report](n2-vocabulary-reviews/batch-08-claude-initial.md)
(`claude-opus-5.5`) independently assessed authored commit
`c3e705025de8ed252789968a9a37ab0535ddf3a3`. They received the same
snapshot, assignment and source access without the other report or
author adjudication. The isolated read-only processes ran strictly
sequentially; GPT exited before Claude started. Usage receipts verify
the actual models and no edits. The author verified the unchanged
clean worktree and HEAD between runs.

All six initial findings are accepted as minor, localized defects:

| Report ID | Supported issue | Correction authored |
|---|---|---|
| GPT-B08-01 | 延長's continuation sense overlaps 続き's answer label. | Add the direct 延長/続き guard. |
| GPT-B08-02 | 応ずる's acceptance label overlaps ordinary 受ける acceptance. | Add 応ずる/受ける; do not generalize the separate Go sense. |
| GPT-B08-03 | 応接 and 応対 overlap 扱う's person-handling/treatment sense and label. | Add both direct pairs, not a transitive exclusion chain. |
| GPT-B08-04 | 往復's correspondence sense overlaps 便り's label. | Add 往復/便り without equating an exchange and an individual letter. |
| Claude F1 | N2:148's omitted-sense note names human life and classical music incorrectly. | Correct both provenance records to mathematics, philosophy and the Encho era, senses 4-6; refresh the index hash. |
| Claude F2 | 追い越す's surpass label overlaps 越える's applicable sense. | Add 追い越す/越える; "especially 超える" is not a spelling restriction. |

The author inspected the complete correction families and all five
comparison articles. Three new families (扱う, 便り and 続き) are
preserved in the packet; re-extracted 受ける and 越える exactly match
the existing complete evidence. Both pinned JMdict hashes were checked
again. The actual main 延長 family confirms the provenance correction;
selected senses 1, 2, 3 and 7 and the learner-facing lesson are unchanged.
The private mapping record is synchronized as well.

Four additional actual-entry inspections independently corroborate
continuation, acceptance, attending to people and correspondence.
The receipts distinguish Daijisen definitions from the Seisenban
sections that actually rendered for 受ける and 扱う. These dictionary
uses support the context-free English quiz guards, not unrestricted
Japanese substitution. No existing baseline identity, reading, title,
easier level or exclusion list changes.

Claude's Optional O1 is accepted as precision polish: 応対 now says
"In the second example, を" rather than implying a second occurrence
of the particle. Optional O2 does not request a 往復/帰り guard:
the existing travel distinction remains sufficient in the reviewed
scope. It is not equivalent to GPT's different 便り finding.

Comparing the entire initial reports, GPT uniquely supplied five
supported direct pairs; Claude uniquely supplied the provenance
correction and the 越える pair. No equivalent observation was found
elsewhere in the other report. Both families therefore added useful,
different signal in this sample, not evidence for a general ranking
or a quantified reduction in model bias. GPT independently fetched
all nine original external-receipt headwords plus additional evidence;
Claude re-fetched 応接 but left eight receipts as author assertions
and inspected only selected comparison families. Claude's failed
GitHub-raw lookups did not supply evidence. Neither file-only reviewer
executed Git, hash verification or app checks. Unequal retrieval and
comparison depth limit the comparison despite identical access.

### Bounded confirmation and closure

Correction commit `5cabdf7ea6ee50bf59bc1a743c76f7797dfcbd6f`
directly follows the authored snapshot. The frozen confirmation
included the actual six-card diff and all three changed provenance
files, not only the app-facing changes. The correction packet retains
the original evidence and adds the three complete comparison families
and four actual-entry receipts described above.

The verbatim [GPT confirmation](n2-vocabulary-reviews/batch-08-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-08-claude-confirmation.md)
are CLEAN on all three facets for every changed card and the
provenance correction. Both read all five comparison cards, assess
all six pairs and the particle clarification, and reconcile their
own initial findings as resolved. Both independently retrieved the
four new external entries and distinguished the dictionary sections
that actually rendered. No regression or consequential unresolved
claim was identified in the assigned scope.

Fresh processes of the original model families again ran strictly
sequentially, each with only its own initial report and the same
correction scope/evidence. Usage receipts verify the actual models
and no edits. The author checked the unchanged clean worktree and
HEAD between runs. The reviewers' commit/hash and unexecuted-app
limits remain explicit; reading a supplied hash is not recomputing it.

Claude's possible additional body contrasts for 延長/続き or 往復/便り
are optional expansion, not a remaining defect. The existing scoped
teaching and supported quiz guards require no further change.

The deterministic corrected manifest contains 6,041 files, including
396 images and 201 scene catalogs; content version `d8c20b214da8a2ac`.
All 3,273 baseline identities, readings, titles and exclusions are
preserved. Cumulative coverage is **160 closed, 0 draft, 1,652 pending
and 0 unresolved** rows, mapped to 159 articles (140 new and nineteen
reused). There are 3,413 word articles and 33 new reciprocal N2
kanji-word pairs across these eight batches. This closure does not
certify the whole corpus or native-speaker naturalness.

## Batch 09: N2:162-N2:181

**Status:** review-closed after independent initial reviews and bounded confirmations.

Scope: おおざっぱ, 大通り, オートメーション, オーバーコート,
おおよそ, お帰り, おかけください, おかげさまで, おかず, 拝む,
お代わり, 補う, お気の毒に, 屋外, 奥さん, 送り仮名, 元気でね,
怠る, 押さえる and お先に.

Nineteen new articles and the unchanged N5 奥さん article cover the
twenty rows. The source spellings 大凡 and 押える are explicitly taught
in おおよそ and 押さえる; the original source fields and ordering remain
unchanged, including 元気でね's position among お-readings.
Kana-only おおざっぱ recognizes 大雑把 and 大ざっぱ without assigning
their kanji to its kana headword metadata.

Three N2 kanji pages gain reciprocal examples: 拝/拝む, 補/補う and
毒/お気の毒に. Five existing word pages gain only navigation links at
substantive comparisons: オーバー, コート, おかげ, 気の毒 and 外.
No existing identity, primary reading, title, easier level or exclusion
list changes. The absent 仮 and 怠 character cards do not remove those
characters from the new words' complete metadata.

The [batch evidence](n2-vocabulary-batch-sources/batch-09.json) preserves
the exact rows, complete principal families, component records,
121 complete comparison families and four qualified actual-entry
inspection receipts. The receipts distinguish rendered Daijisen
definitions from the Seisenban or encyclopedia sections that actually
provided evidence. Failed, irrelevant and heading-only retrievals are
recorded as limits, not dictionary confirmation.

The teaching qualifies 怠る's dated illness sense, keeps おかげさまで's
social use distinct from any necessary religious interpretation, and
does not reduce 送り仮名 to changing inflections. The 押さえる/抑える
comparison is not an absolute physical/mental partition. English
borrowing histories are not inferred from empty dictionary loan-source
fields or unrendered etymology headings.

Structural, baseline, mapping and reciprocal-link checks pass.
The authored manifest has 6,060 files, including 396 images and
201 scene catalogs; content version `14bca6a4211fe1e3`. There are
3,432 word articles. Cumulative drafted/closed mappings cover
179 articles: 159 new and twenty reused, with 36 reciprocal N2
kanji-word pairs. These authored counts do not claim review closure.

### Independent initial reviews and reconciliation

Authored snapshot `ac708ffd2a4153211b420e63c2b0b8766319342d`
was reviewed by GPT-6.1 Sol (`gpt-6.1-sol`) and Claude Opus 5.5
(`claude-opus-5.5`) in fresh, strictly sequential processes. Both
received the same frozen nineteen-article scope, eight related
passages, narrow reuse claim, rubric and source access. Usage
receipts confirm the actual models and no edits. The author verified
the unchanged HEAD and clean worktree after both initial reviews.

The verbatim [GPT initial report](n2-vocabulary-reviews/batch-09-gpt-initial.md)
and [Claude initial report](n2-vocabulary-reviews/batch-09-claude-initial.md)
support all twenty mappings, including the aliases and anomalous
source order. Both independently retrieved the four external
entries. Their file-only access did not independently establish Git
history, hashes or worktree cleanliness.

All four GPT findings are accepted as localized quiz safeguards:
おおざっぱ/およそ and /一応, おおよそ/ばかり and /程度,
お代わり/代わり, and お先に/どうぞ. Claude's optional どうぞ
observation identifies the same last pair; it is shared, not uniquely
GPT's because of different report placement.

Claude's three findings are also accepted: direct お気の毒に guards
against すみません and ごめんなさい address ambiguous English apology
labels without treating the Japanese expressions as synonyms;
オートメーション/自動 protects automation versus automatic operation;
and お先に's unexplained word "historical" is replaced by a precise
dictionary-gloss versus interaction explanation. The source does
not mark "previously" as archaic or dated.

Claude's optional おおよそ/ころ pair is accepted after inspecting the
complete time-related family and actual "approximate time; around"
label. Its unrelated calabash, roller and whale-blubber homographs
are not evidence. The optional 替 link in お替わり is also added.
The 菜 link already existed in the authored おかず article, so that
suggestion identifies no missing link. Additional 把 discussion,
farewell expansion and redundant kana for entirely kana-written
examples remain optional, not coverage defects.

The correction adds **ten direct pairs across six new cards**, one
prose clarification and one alternate-spelling navigation link.
Thirteen complete families were re-extracted after checking both
pinned JMdict hashes: six match the original evidence exactly and
seven are new. Two qualified Jisho actual-entry receipts corroborate
ばかり and 程度, without pretending that a JMdict-backed service is
independent lexicography. No raw row, mapping, selected sense,
baseline identity, title, reading or easier level changes.

Across equivalent observations anywhere in both reports, GPT uniquely
supplied five supported direct pairs. Claude uniquely supplied four
pairs, the prose clarification and the useful 替 link; one pair was
shared. Both families added useful different signal in this sample,
not evidence of a general ranking or quantified bias reduction.
Claude's already-present 菜-link suggestion and speculative source
sort-key explanation add no verified discovery. The original Waller
item behind 元気でね remains unverified; no reconstruction is taught.
Neither reviewer executed the app or independently hashed downloads.

### Bounded confirmation and closure

Correction commit `c23eb2ff4638c41dac20a187c43d81bfeeb1dfaf`
directly follows the authored snapshot. The frozen correction includes
the complete six-card diff and packet additions. Both model families
ran again in fresh, strictly sequential processes, each receiving only
its own initial report, the same correction scope and actual evidence.
Usage receipts verify their actual models and zero edits; the author
verified the unchanged clean worktree and HEAD after both confirmations.

The verbatim [GPT confirmation](n2-vocabulary-reviews/batch-09-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-09-claude-confirmation.md)
are CLEAN on all three facets for every changed card and the packet
additions. Both read all ten comparison cards and the 替 target,
assessed every correction, and reconciled their initial findings as
resolved. Claude independently fetched the two new Jisho receipts;
GPT assessed them as supplied assertions. Neither established
independent hash or Git verification. No actionable regression or
consequential unresolved claim remains in the assigned scope.

Claude withdrew the redundant kana suggestion. Its carried-over 菜
suggestion still concerns an already-present link, not a defect.
The additional low-confidence およそ/ばかり and /ころ suggestions
concern an unchanged baseline card and are outside this correction.
They do not invalidate the new direct guards; no unrelated baseline
exclusions are changed.

The corrected deterministic manifest has 6,060 files, including
396 images and 201 scene catalogs; content version `f699c433ea7ac26c`.
All 3,273 baseline identities, readings, titles and exclusion lists
remain preserved. Cumulative coverage is **180 closed, 0 draft,
1,632 pending and 0 unresolved** rows, mapped to 179 articles:
159 new and twenty reused. There are 3,432 word articles and 36
reciprocal N2 kanji-word pairs. This is bounded batch closure, not
whole-corpus or native-speaker certification.

## Batch 10: N2:182-N2:201

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 納める, 治める, 惜しい, 御辞儀, 伯父さん, 小父さん,
叔父さん, おしゃれ, おじゃまします, 教わる, おだいじに,
落着く, 御手洗, お出掛け, お手伝いさん, おどかす,
落し物, おととい, おととし and おとなしい.

Fifteen new articles and five reused rows cover this batch. The three
uncle/man spellings share the unchanged N5 おじさん article, with the
applicable uncle or unrelated-man sense selected per row. The kana
date rows reuse unchanged N5 一昨日 and 一昨年, also mapped in batch 04.
The twenty rows therefore map to eighteen distinct articles; cumulative
mapping totals do not count the date articles twice.

New teaching IDs お辞儀, 落ち着く, お出かけ and 落とし物 explicitly
recognize source 御辞儀, 落着く, お出掛け and 落し物. 納める receives
a separate spelling-specific article rather than inheriting the
achievement sense restricted to 収める. The raw source gloss remains
unchanged. 御手洗 is taught at the source's actual みたらし reading for
the shrine purification place, not silently remapped to おてあらい.

Seven existing word articles gain comparison navigation; 習う also
gains one brief 教わる comparison, and 手伝い a domestic-worker contrast.
The existing 治 page links its two already-present 治める examples.
CW005 gains links to 教わる and 学ぶ. No existing identity, primary
reading, title, easier level or exclusion list changes. No new primary
word contains an N2 character card, so this batch adds no N2 reciprocal
pairs; it does not manufacture pairs from kana-headword aliases.

The [batch evidence](n2-vocabulary-batch-sources/batch-10.json) preserves
all raw rows, complete principal families and component records,
118 complete comparison families and four qualified actual-entry
inspection receipts. The receipts identify the rendered dictionary
or encyclopedia section and do not treat failed requests or a
definition-less heading as verification.

The authored checks preserve all 3,273 baseline identities, readings,
titles and exclusion lists. The deterministic manifest has 6,075 files,
including 396 images and 201 scene catalogs; content version
`21e74fb574f138f9`. There are 3,447 word articles. Cumulative mappings
cover 195 distinct articles: 174 new and 21 reused, with 36 reciprocal
N2 kanji-word pairs. Coverage is 180 closed, twenty draft, 1,612 pending
and zero unresolved rows. These are authored counts, not review closure.

### Initial independent review

Both families reviewed authored commit
`c53e61946e7229fafbf9401901cfbebe48c2c19e`, parent
`a5be09f25b54da66e35037028d4e171b726ec5fb`, with identical frozen scope,
rubric and source access. The short-lived GPT process exited before
the Claude process began; neither delegated or edited files. Usage
receipts verified the actual models:

- [GPT initial report](n2-vocabulary-reviews/batch-10-gpt-initial.md):
  `gpt-6.1-sol`.
- [Claude initial report](n2-vocabulary-reviews/batch-10-claude-initial.md):
  `claude-opus-5.5`.

Both supplied three-facet assessments of all fifteen new articles,
the eight related content edits, CW005, the five reuse claims and
the twenty mappings. All mapping/reuse claims and the related edits
were clean in that bounded scope. Neither reviewer could execute
Git or independently hash the frozen files; the author checked
committed identity, clean state and unchanged HEAD. Public-entry
retrieval and its limits are distinguished from author receipts.

### Reconciliation and implemented correction

The following decisions are implemented and independently
confirmed. Quiz findings are localized ambiguity defects rather
than evidence that the teaching prose or Japanese words are interchangeable.

| Initial finding | Decision and evidence |
| --- | --- |
| GPT B10-GPT-01: 納める delivery/completion | Add direct guards with 配達, 終える and 済ませる. Entry 1589090 restricts payment/delivery sense 4 and completion sense 9 to 納める; the actual comparison labels overlap. Weblio's actual 収める/納める definition also corroborates finishing a year's work. |
| GPT B10-GPT-01 / Claude B10-01: settlement spellings | Add 治める/収める and 治める/納める guards. Clarify in 治める that 収める also writes dispute settlement, and link it in 落ち着く's dispute comparison. Entry 1589090 sense 8 has no spelling restriction and cross-references 治める sense 2; Weblio's actual definition corroborates calming conflict/anger. Neither spelling examples nor dictionary recognition establish frequency or unrestricted substitution. |
| GPT B10-GPT-02: bowing | Add お辞儀/ぺこぺこ: entry 1011540 sense 2 and the actual card explicitly teach repeated bowing. A repetition/fawning nuance does not invalidate the generic bowing label. |
| GPT B10-GPT-03: learning | Add 教わる/学習: 1206820 sense 1 and the broad learning/study label overlap instruction-based learning. |
| GPT B10-GPT-04 / Claude B10-02: composure | Add 落ち着く/冷静. Both actual cards teach composure; 1557050 sense 1 corroborates it. |
| GPT B10-GPT-04: matching and quiet composure | Add 落ち着く/合う and /しっとり. Entries 1284430 sense 2 and 2121280 sense 2 overlap the already-recognized fitting and calm/quiet senses. Moisture is not the evidence for しっとり. |
| GPT B10-GPT-05 / Claude B10-03: well-behaved | Add おとなしい/利口. Both titles explicitly say well-behaved, and 1549550 sense 2 supports the child/pet use with its usual お- qualification. |
| GPT B10-GPT-05: gentle/quiet manner | Add おとなしい/しっとり, supported by the latter's sense 2 and actual softly-composed label. |
| GPT B10-GPT-06 and -07: lost property | Add 落とし物/落す for the accidental-dropping action sense, and link the explicitly introduced 落とす to stable 落す, whose article explicitly teaches that fuller spelling. Complete entry 1589260 sense 1 supports the construction. |
| Claude B10-03: そっと candidate | Add おとなしい/そっと after inspecting the actual gently/quietly label and complete adverb family 1006810 sense 1. The new card already teaches おとなしく待つ, wait quietly. This is not evidence that all gentle handling means docility; literary noun 率土 is not the relevant homograph. |
| Claude B10-04: outing candidates | Add お出かけ/遠足 and /デート. Entries 1178260 sense 1 and 1081430 sense 1, and both actual cards, teach outing uses. A broad outing label can fit these subtypes without making every outing a school trip or date. |
| Claude B10-05: helper candidate | Add お手伝いさん/助手. The actual generic helper label and entry 1344650 at じょしゅ support the ambiguity; the different たすけて/すけて family is retained but not the target card. This does not make every assistant a domestic worker. |
| Claude Optional: 教わる/就く | Add the direct pair. The actual 就く title explicitly includes study under, and entry 1331530 sense 4 restricts that teacher/apprentice sense to 就く. |
| Author follow-up: payment noun | Add 納める/支払 after checking the actual payment label and complete family 1594480. The existing 支払う exclusion is not transitive. |
| Claude Optional: お出かけ wording | Replace the awkward negative about already being outside with a scoped contrast between the greeting's going-out use and merely locating someone outdoors. No new register or historical claim is added. |

This is **nineteen new direct pairs across nine new cards**, a
spelling-overlap clarification with related navigation, one base-verb
link and greeting polish. Twenty-three complete families were
re-extracted for twenty forms after checking both pinned JMdict
hashes: the original 落とす family matches exactly, and twenty-two
families are added. One qualified actual-entry receipt records the
usable Weblio 収める definition without claiming a named dictionary
heading that was absent from the extraction. The unusable 治める
lookup is recorded as a limit, not verification. Raw rows, mappings,
selected senses and baseline metadata remain unchanged.

The weaker おどかす/ぎょっと or /びっくり suggestions are not adopted:
their actual labels and records describe experiencing surprise, not
the transitive act of startling another person. Nor does お見舞い's
get-well visit/sympathy label establish the recovery-wish formula
おだいじに as its answer. あの's tentative attention-getting use
does not establish おじゃまします's intrusion-specific title as an
answer. These decisions concern the actual labels, not a claim that
the words can never co-occur in discourse.

御手洗 expansions (手水舎, sweets, a different type grouping),
additional kanji backlinks and an おさめる confusable row remain
optional. The native-word grouping does not assert constituent
readings. The 納める guard on 落ち着く is retained: the complete
settlement sense exists even though the payment-focused title differs.
No frequency or exhaustive semantic-uniqueness claim is made.

Comparing equivalent observations anywhere in both reports, the
冷静, 利口 and shared-settlement observations overlap. GPT supplies
additional supported delivery/completion, bowing, learning, matching,
quiet-manner and dropping guards plus the missing base-verb link.
Claude adds useful spelling-contrast wording and supported そっと,
outing, helper and study-under candidates, several in Optional;
its greeting wording suggestion also improves clarity. The payment
noun guard is author follow-up, not credited as a unique model finding.
Both families add useful different signal in this sample, not proof
of a general model ranking or measured bias reduction.

### Bounded confirmation and closure

Both families examined corrected commit
`7132eedd62f20b68eb13b08be9d61fb0b1803483`, directly following the
authored snapshot, with the actual correction diff, their own initial
report and the same bounded assignment. GPT exited before Claude
started. Usage receipts verified the actual models and no edits:

- [GPT confirmation](n2-vocabulary-reviews/batch-10-gpt-confirmation.md):
  `gpt-6.1-sol`.
- [Claude confirmation](n2-vocabulary-reviews/batch-10-claude-confirmation.md):
  `claude-opus-5.5`.

Each read the nine changed new articles, seventeen existing comparison
articles, complete correction patch and twenty-two additional dictionary
families. Both marked all nine articles and the packet additions CLEAN
on correctness, scoped coverage and comprehensibility; no actionable
regression or consequential unresolved claim remained in that scope.
Each independently retrieved the usable Weblio settlement definition,
without asserting an absent named-dictionary heading. File-only reviews
do not independently establish the pinned hashes, clean Git state or
validator result; the author verified those separately.

Claude withdrew the three weaker surprise, get-well and attention-getting
hypotheses after checking the distinct functions. Its additional remarks
about completion teaching, a settlement example on the existing 収める
page and smoother wording remain optional expansion or polish, not
unresolved defects in the mapped source senses. Claims about unreported
working-note candidates do not retroactively change the initial-model
contribution comparison above.

The corrected deterministic manifest has 6,075 files, including
396 images and 201 scene catalogs; content version `00fc913af0ab1037`.
All 3,273 baseline identities, readings, titles and exclusion lists
remain preserved. Cumulative coverage is **200 closed, 0 draft,
1,612 pending and 0 unresolved** rows, mapped to 195 articles:
174 new and 21 reused. There are 3,447 word articles and 36 reciprocal
N2 kanji-word pairs. This closes the bounded batch, not the whole
expansion or a native-speaker certification.

## Batch 11: N2:202-N2:221

**Status:** closed after sequential independent reviews, evidence-based
corrections and bounded confirmations.

Scope: 驚かす, おねがいします, 各々, 叔母さん, おはよう,
お参り, おまたせしました, おまちどおさま, おめでたい,
思い掛けない, 思い込む, 思いっ切り, 思い付く, 重たい,
おやすみ, おやつ, 親指, オルガン, 卸す and 恩恵.

Nineteen new articles and the unchanged N5 伯母さん cover the twenty
rows. The existing aunt article already explicitly teaches younger-aunt
叔母さん at おばさん. Its identity, primary reading and easier level
remain unchanged. The raw source's unrelated-woman gloss belongs to
separate 小母さん evidence, not an extra meaning silently assigned to
the aunt spelling.

Written teaching IDs お願いします, お待たせしました and
お待ちどおさま retain their source readings. 思いがけない explicitly
recognizes 思い掛けない; 思いっきり recognizes rare 思いっ切り
without manufacturing the source's blank gloss. おめでたい distinguishes
the adjective from happy-event/pregnancy noun おめでた. 卸す covers
wholesale selling and cooking uses while acknowledging the cooking
overlap in the complete 下ろす/降ろす family.

Seven existing word articles gain comparison navigation. 各 gains
linked 各々 examples at the actual おのおの reading, adding one useful
reciprocal N2 pair. Alias spellings do not add primary-headword kanji
metadata or manufacture additional N2 reciprocal pairs.

The [batch evidence](n2-vocabulary-batch-sources/batch-11.json) preserves
every raw row, twenty complete principal families, component records,
117 complete comparison families and four qualified actual-entry
inspection receipts. Failed or irrelevant fetches are recorded as
limits, not verification. Numeric article citations have been checked
against the extracted families and actual headwords.

All 3,273 baseline identities, primary readings, titles and exclusion
lists remain preserved. There are 3,466 word articles. The deterministic
manifest has 6,094 files, including 396 images and 201 scene catalogs;
content version `2251640eb85b0d7e`. Cumulative mappings cover 215
distinct articles: 193 new and 22 reused, with 37 reciprocal N2
kanji-word pairs. Coverage is **200 closed, twenty draft, 1,592 pending
and zero unresolved** rows. These are authored counts, not review closure.

### Initial independent reviews

Authored commit: `2eccc7af442aeb9cbcb7c064650a2e6b63b11e1e`.
The [GPT initial report](n2-vocabulary-reviews/batch-11-gpt-initial.md)
and [Claude initial report](n2-vocabulary-reviews/batch-11-claude-initial.md)
are archived verbatim. GPT `gpt-6.1-sol` exited before Claude
`claude-opus-5.5` started. Both read the same frozen nineteen-article,
eight-related-change and twenty-mapping assignment, with no other
reviewer's findings or author adjudication. Actual-model usage receipts
record zero edits. Reviewers could not independently execute Git or
verify the receipt hashes.

GPT reported five minor quiz findings affecting five articles and six
direct pairs. Claude reported two minor quiz findings and a recall
comprehensibility gap, plus optional guard and wording hypotheses.
Their reports categorize quiz fairness under different facets; the
archives preserve those original verdicts rather than rewriting them.

### Evidence-based reconciliation

The prepared correction addresses eleven direct pairs across eight new
articles. It also clarifies memory production on 思い付く and links the
already-taught request formula from the existing 願う article.
Confirmations are still pending; the following is author adjudication,
not a claim that either reviewer has accepted the revised snapshot.

| Observation | Adjudication and prepared correction |
| --- | --- |
| GPT-01: お待たせしました / どうも | Supported: the generic English thanks label overlaps the taught wait acknowledgment. Add the direct guard. |
| GPT-02: 思い込む / 決める | Supported: complete 決める sense 5 includes assumption; its decision sense also overlaps determination. Add the direct guard. |
| GPT-03: 思いっきり and 思い込む / 覚悟 | Supported: the recorded resolution/determination senses overlap resolve. Add both direct guards without equating all Japanese constructions. |
| GPT-04: 重たい / 大変 | Supported: both complete families contain the ordinary serious sense. Add the direct guard. |
| GPT-05 and Claude optional: 恩恵 / おかげ | Supported: the complete おかげ record includes blessing, not merely the displayed help/thanks label. Add the direct guard. |
| Claude R1: お願いします / 願う and 願い | Supported as context-free request-label guards, consistent with the existing 頼む guard. Shared kanji do not establish measured candidate probability. |
| Claude R2: 思い付く recall guidance | Address the learning concern with an explicit, translated known-name example using 思い出す and qualified practical guidance. Retain the dictionary recall sense; do not invent the proposed modern errand-recall collocation or an only-spontaneous/never-deliberate rule. |
| Claude R3 and optional: おはよう / 朝 and 午前 | Supported English-label ambiguity: the actual Oxford good-morning entry records informal morning as a greeting. Guard both time-period cards without claiming they are Japanese greetings. |
| Claude optional: お願いします attachment wording | Adopt: explicitly acknowledge noun + を with both expressions, then identify the verb て-form contrast already taught below. |
| Claude optional: 卸す / 売れる | Adopt a direct generic English sell-label guard. This does not make the transitive wholesale verb and intransitive 売れる unrestricted substitutes. |

Nine complete correction families, including all three 朝 homographs,
are added separately from the original comparison evidence. Only
1428280 at あさ is the existing morning card; dynasty ちょう and
poetical あした are not conflated. The twenty raw rows, selected senses,
principal families, components and original 117 comparison families are
unchanged.

Five qualified actual-page receipts support the memory-production
contrast and English greeting ambiguity. The usable Kotobank material
is Seisenban's transitive thought-coming-to-mind sense, including recall;
its historical examples do not establish a modern errand collocation.
The teaching comparisons support ordinary name/past-event recollection
with 思い出す. An AI search synopsis claiming no reputable recall sense
contradicted the actually inspected dictionary evidence and was rejected.
Definition-less headings and unusable fetches do not become verification.

Claude's additional derivatives, historical explanations and a broader
重たい/重い tendency note remain optional expansion. No supported
consequential claim requires them for this bounded lesson. The minimal
memory correction differs from the literal suggestion because a suitable
attested modern positive recall example was not established.

### Model-contribution comparison

Both reports identified 思いっきり / 覚悟 and 恩恵 / おかげ,
although Claude placed them under Optional. They are shared observations,
not unique GPT discoveries. GPT additionally identified どうも,
決める, 覚悟 against 思い込む, and 大変. Claude additionally supplied
the request and greeting guards, the optional 売れる guard, the recall
teaching gap and the attachment-wording clarification. These are useful
complementary observations on this common sample, not a general model
ranking or proof of reduced bias. Candidate-frequency inferences and
unattested suggested examples still require author adjudication.

The correction passed structural validation and the cumulative
baseline, mapping, reciprocal-link and authorship audit. Its deterministic
manifest has 6,094 files, with content version `1a0448d48a8be1c3`.
At that prepared snapshot the counts were 200 closed and twenty draft
rows; none was promoted before the bounded confirmations.

### Bounded confirmations and closure

Corrected commit: `b9f336419a555cd151f5f05eee4a1a395bfd3817`.
The [GPT confirmation](n2-vocabulary-reviews/batch-11-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-11-claude-confirmation.md)
are archived verbatim. The same actual models ran sequentially, each
receiving its own original report, the actual ten-card correction diff
and packet additions, not the other model's findings. Both usage
receipts record zero edits; each process exited before the next began.

Both marked all ten changed contexts and packet additions CLEAN on
correctness, scoped coverage and comprehensibility. GPT resolved its
five original findings. Claude resolved R1-R3 and explicitly withdrew
the unsupported parts of its literal recall remedy: no modern errand
example was established, and deliberate-versus-spontaneous recall is
not the supported distinction. The practical memory-production guidance
addresses the learning concern without manufacturing that evidence.

The adopted optional guards and attachment clarification are covered by
the clean changed-context verdicts. Claude's suggested inline naming of
Seisenban remains optional attribution polish: the source line already
identifies it, and the packet separates its grouping from JMdict's
separate recall sense. The remaining derivatives, history and broader
重たい/重い lesson remain nonblocking expansion. No actionable defect
or consequential unresolved claim remained in this bounded scope.

GPT independently retrieved all five added pages; Claude independently
retrieved Seisenban, the two Japanese-teaching comparisons and Oxford's
good-morning entry. The separate Oxford morning noun page was not
independently fetched by Claude. Neither file-only reviewer independently
verified Git ancestry, dictionary hashes, manifest generation or app
execution. The author separately verified the frozen content/provenance
hashes unchanged after both processes and the clean corrected commit.

Cumulative coverage is **220 closed, 0 draft, 1,592 pending and
0 unresolved** rows, mapped to 215 distinct articles: 193 new and
22 reused. There are 3,466 word articles and 37 reciprocal N2
kanji-word pairs. All 3,273 baseline identities, readings, titles and
exclusion lists remain preserved. The manifest is unchanged from the
confirmed correction. This closes batch 11, not the full expansion or
a native-speaker certification.

## Batch 12: N2:222-N2:241

**Status:** closed after sequential independent reviews, evidence-based
corrections and bounded confirmations.

Scope: 温室, 温泉, 温帯, 御中, 女の人, 蚊, カーブ, 貝,
開会, 会館, 改札, 解散, 海水浴, 回数, 回数券, 改正, 快晴,
解説, 改造 and 開通.

Nineteen new articles and the existing 貝 cover the twenty rows. 貝
already teaches both source senses at かい; only its previously absent
level becomes source-backed N2. Its body, identity, title, reading and
original exclusions remain unchanged. This is a level-only reuse,
not an unchanged-metadata reuse.

Nine N2 kanji cards gain thirteen reciprocal word pairs. Eight existing
word articles gain links on already-taught comparisons. The imported
content changes do not add kanji/stroke files or rename existing IDs.

The [batch evidence](n2-vocabulary-batch-sources/batch-12.json) retains
all twenty raw rows and complete principal families, the component
records, complete comparison families and qualified actual-page
inspection receipts. The original 御中 correspondence gloss is
interpreted as an organizational address suffix, not an unrestricted
translation of English "and company." The 快晴 explanation follows
the observed low-cloud meaning rather than an absolute zero-cloud rule.

Coverage is **220 closed, twenty draft, 1,572 pending and zero
unresolved** rows. Cumulative mappings cover 235 distinct articles:
212 new and 23 reused. There are 3,485 word articles and fifty
reciprocal N2 kanji-word pairs. These are authored counts, not review
closure or linguistic certification.

### Initial independent reviews

Authored commit: `6aa54a72f1f89170d85ef3f0b42af79427018d66`.
The [GPT initial report](n2-vocabulary-reviews/batch-12-gpt-initial.md)
and [Claude initial report](n2-vocabulary-reviews/batch-12-claude-initial.md)
are archived verbatim. GPT `gpt-6.1-sol` exited before Claude
`claude-opus-5.5` started. Both received the same nineteen new
articles, eighteen related changes, twenty mappings, rubric and source
access, without author adjudication or the other report. Actual-model
usage receipts record zero edits.

GPT reported four quiz findings affecting five cards. Claude reported
one quiz finding and one link-target comprehensibility defect, both
on 御中. Both found the source mappings and lesson bodies within scope
clean apart from that navigation issue. Their original verdicts and
severity labels remain in the reports; localized quiz-label safeguards
do not imply incorrect Japanese definitions.

### Evidence-based reconciliation

Six direct quiz pairs across six new articles and one link target are
corrected. No baseline titles, readings, levels or exclusion lists
change in the correction. The following records the pre-confirmation
author adjudication.

| Observation | Adjudication and prepared correction |
| --- | --- |
| GPT-01: 温泉 / 春 | Supported English-label ambiguity: the displayed bare "spring" can name a water source. The existing 泉/春 guard is not transitive. Add the direct guard without making seasonal 春 a water-source word. |
| GPT-02: 開会 and 開通 / 最初 | Supported broad beginning-label overlap. The complete 最初 family and actual Seisenban さいしょ definition recognize beginning/outset. Add both direct guards without equating their constructions. |
| GPT-03: 解散 / 溶ける | Supported English polysemy: Oxford's actual dissolve entry distinguishes physical dissolving from ending a parliament and dispersing a crowd. Add the direct guard, retaining the Japanese distinction. |
| GPT-04: 解説 / 注 | Supported written-explanation overlap: 注's complete family and actual definitions recognize explanatory commentary attached to a text. Add the direct guard; not every 解説 is an annotation. |
| Claude F1: 御中 / 氏 | Supported generic respectful-name-suffix label ambiguity. Add the direct guard, preserving the organization/person distinction. Shared tags do not establish actual candidate frequency. |
| Claude F2: 御中's さま link | Supported navigation defect. The word target teaches よう and only warns against confusing it with さま. Point to the existing 様 kanji card, which actually teaches the suffix and a personal-name example; remove the distracting parenthetical. |

Six complete correction families for five forms retain both 氏
homographs: 2101130 at し is the suffix card, not 1311010 at うじ.
The original rows, mappings, selected senses, components, principal
families and 133 original comparison families are unchanged. Three
qualified actual-page inspection receipts support the added English
polysemy and Japanese comparison evidence.

The missing original `jlpt` on 貝 establishes only its undeclared
baseline level, not a search of all easier-level sources. Likewise,
the missing 蚊 kanji card alone does not establish its kanji level.
Neither stronger inference is required by the content: the mapped
N2 word level is sourced, and the full written-kanji metadata is kept.

Claude's 寒帯 gloss consistency and 会館/会議室 suggestions remain
optional. "Cold" and "frigid" both describe the climate-zone contrast;
hall versus meeting-room labels do not establish an additional
defensible quiz answer. No literal zero-cloud rule, all-native 御中
claim, or unrestricted synonym partition is introduced.

### Model-contribution comparison

GPT supplied the accepted 最初 and 注 guards. Claude supplied the
accepted 氏 guard and wrong-word link catch. Claude also explicitly
considered the 春 and 溶ける label leads in its recorded output but
did not promote them to findings. Those are shared examined leads
with different actionability judgments, not uniquely discovered
GPT observations. The author accepted the guards from their actual
displayed-label ambiguity and evidence, not model vote.

The two families therefore contributed complementary accepted
corrections on this common sample. This does not establish a general
model ranking, measured candidate probability or proof of reduced bias.
Both file-only reviewers relied on the authored snapshot receipt rather
than independently executing Git. Claude independently fetched the JMA,
御中 and Japan Post pages; GPT reports independent retrieval of all six
original usage pages. Neither rehashed the full source archives.

The prepared correction passed structural and cumulative preservation,
mapping, reciprocal-link and authorship checks. Two manifest builds
were byte-identical: 6,113 files, 396 images and 201 scene catalogs,
content version `cb342dac9eccaa25`. At that snapshot the counts remained
220 closed and twenty draft rows, pending confirmation.

### Bounded confirmations and closure

Corrected commit: `6e9cb41ad714a647f88d1464e41d9d2872e77c96`.
The [GPT confirmation](n2-vocabulary-reviews/batch-12-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-12-claude-confirmation.md)
are archived verbatim. Each original reviewer session was resumed
sequentially in a short-lived process, with its own initial report,
the same actual six-card-plus-provenance diff, and no other-family
report or author adjudication. Actual-model receipts again show
`gpt-6.1-sol` and `claude-opus-5.5`, with zero edits. GPT exited before
Claude began.

Both marked every changed card and the packet additions CLEAN on
correctness, scoped coverage and comprehensibility. GPT resolved
B12-GPT-01 through B12-GPT-04 and confirmed the additional 御中
guard and link. It explicitly withdrew its initial acceptance of the
old target's warning as sufficient destination teaching. Claude
resolved F1 and F2, confirmed all six guards, and corrected the
shared-tag rationale: actual label overlap, not measured selection
probability, supports the exclusion.

Claude also narrowed its 貝 assertion to preservation of the declared
baseline level and withdrew the unnecessary 蚊 classification
inference. Its 寒帯 wording and hall/meeting-room suggestions remain
optional. The newly noticed unchanged 説明/注 pair was not assessed
as a defect in this correction and is outside its new-card scope;
no baseline exclusion list was changed. No actionable defect or
consequential unresolved claim remains in the assigned batch scope.

Both independently retrieved all three new cited pages and retained
the reading-specific Seisenban qualification for 最初. Neither
reviewer independently executed Git, rehashed the dictionary
archives or ran the app. The author separately checked both frozen
snapshots against their commits, and verified the confirmed content,
packet, prompt and patch hashes unchanged after the two processes.
The generated manifest remains identical to the confirmed correction.

Cumulative coverage is **240 closed, 0 draft, 1,572 pending and
0 unresolved** rows, mapped to 235 distinct articles: 212 new and
23 reused. There are 3,485 word articles and fifty reciprocal N2
kanji-word pairs. All 3,273 baseline identities, primary readings,
titles and exclusion lists remain preserved. This closes batch 12,
not the full vocabulary expansion or native-speaker certification.

## Batch 13: N2:242-N2:261

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 回転, 解答, 回答, 外部, 解放, 開放, 海洋, 概論,
帰す, 却って, 代える, 反る, 家屋, 係わる, 書留, 書取,
垣根, 掻く, 嗅ぐ and 架空.

Nineteen new articles and unchanged N3 替える cover the twenty
source rows. 替える already explicitly teaches 代える (かえる)
for person/player substitution, the selected third sense of their
shared family. Its identity, reading, level, teaching, title and
exclusions are unchanged.

The new teaching spellings かえって, 返る, 関わる and 書き取り
explicitly recognize source 却って, 反る, 係わる and 書取 at
their supplied readings. The 反る row's raw warping gloss conflicts
with its verified かえる reading and supplied entry 1512150.
The card teaches that return/reversal identity and separately
distinguishes 反る/そる, entry 1480170. The original row is preserved;
the historical compiler's intent is not claimed to be recovered.
Additional contrast senses do not establish a separate N2 assignment.

根 gains the reciprocal 垣根 example. 書く, におい, the existing
kaeru comparison and confusable-word row CW011 gain links on
already-taught comparisons. No existing word IDs, primary readings,
titles, original exclusion lists or easier levels change.

The [batch evidence](n2-vocabulary-batch-sources/batch-13.json)
retains all twenty original rows and complete principal families,
126 complete comparison families, component records and five
qualified actual-entry inspection receipts. 関わる/係わる
excludes the sticking-to sense restricted to 拘る. 架空 preserves
the fictitious sense's かくう reading restriction. Neither missing
kanji cards nor dictionary flags become unsupported level,
frequency or etymological claims.

Coverage is **240 closed, twenty draft, 1,552 pending and zero
unresolved** rows, mapped to 255 distinct articles: 231 new and
24 reused. There are 3,504 word articles and 51 reciprocal N2
kanji-word pairs. These are authored counts, not review closure.

### Initial review

Both reviewers examined committed snapshot
`033d125b6c4aa4438587e603296d582f2750195d`, parent
`6f9f96981807319a347cd3c202d2d94cfb48c92e`, with the same
scope, rubric and source access. Separate read-only processes ran
sequentially; GPT exited before Claude started. Actual-model,
zero-edit usage receipts identify:

- [GPT initial report](n2-vocabulary-reviews/batch-13-gpt-initial.md):
  `gpt-6.1-sol`.
- [Claude initial report](n2-vocabulary-reviews/batch-13-claude-initial.md):
  `claude-opus-5.5`.

Both read all nineteen new cards and assessed the twenty mappings,
five related edits and unchanged reuse. Their file-only access did
not independently authenticate Git or frozen hashes. GPT revisited
the five initial actual-page sources; Claude independently consulted
Jisho and Weblio and disclosed unsuccessful additional retrievals.
Neither claimed an exhaustive comparison-family or corpus audit.

### Reconciliation

| Observation | Adjudication and correction |
| --- | --- |
| GPT G13-01: 回転 / ぐるぐる | Resolved: add the direct guard for rotation/round-and-round English overlap. Complete family 1004140:1 supports the turning sense; noun and adverb constructions remain distinct. |
| GPT G13-02: 外部 / 表面 and 表 | Resolved: add both direct guards. Outside/exterior belongs to 1489880:2 at ひょうめん and 1489340:4 at おもて, not their other homographs. |
| GPT G13-03: 開放 / 口 | Resolved: add a direct guard for English opening's aperture/beginning ambiguity, supported by 1275640:2,11. This does not make the Japanese nouns synonyms. |
| GPT G13-04: 概論 / 大体 | Resolved: add a direct guard for 1414470:3's outline/main-points noun sense, not just 大体's primary adverbial title. |
| GPT G13-05: 返る / 戻す | Resolved: add a direct guard for unmarked English return. Complete family 1535850:1 supports it; Japanese transitivity is unchanged. |
| GPT G13-06 / Claude B13-03: 家屋 / 住宅; GPT also 宅 | Resolved: add both direct guards for ordinary house/residential-building overlap, supported by 1334150:1 and 1415750:1. The 住宅 observation is shared. |
| GPT G13-07: 垣根 / 壁 | Resolved: add a direct guard for figurative barrier, 1509290:2 at かべ. Existing guards through 塀 do not propagate. |
| GPT G13-08 / Claude B13-05: 参加 link | Resolved: link the existing 参加 article at the substantive 参加する comparison. Shared finding, not two discoveries. |
| Claude B13-01: separate 帰す / きす | Useful clarification implemented, with complete family 2410530:1,2. The original "this reading" already scoped itself to the send-home verb; it was not an explicit universal denial of every homograph. No unsupported literary-frequency or N2 claim is added. |
| Claude B13-02: turn-over illustration | Resolved as a practical illustration gap: add an original, translated, kana-supported coat-hem example using the independently inspected 裾が返る construction. The prior explicit sense/alias teaching was not an absent source mapping, and the original sentence is not claimed corpus-attested. |
| Claude B13-04: 命に関わる translation | Clarified to life-or-death and survival stakes. The original broad "affecting someone's life" was less precise, not proof of a false general lexical definition. Complete family 1589880:3 supplies the serious-bearing sense. |
| Claude optional: 開放's opening-up paraphrase | Adopt as nonblocking clarity: describe the two actions directly and reject interchangeability from pronunciation, without the loose English paraphrase. |
| Claude optional: guest example and 送る | Remain optional, not established defects. 客を帰す teaches sending someone home; rewriting it as 客が帰る would change the target construction. Complete 送る family 1402730 retains send/escort senses but does not by itself establish unrestricted equivalence with the specifically homeward label. |
| Claude optional: cage-release 解放 and 根 reading-row example | Remain optional. An alternative release verb does not invalidate the stated captivity context; a useful reciprocal 垣根 example already exists in Common words. No extra unchanged-card review is claimed. |
| Claude optional: stagk typo | Declined: stagk is JMdict's actual sense-spelling restriction element, already explained in the authoring notes; it is not a spelling error. |

The packet adds sixteen complete correction families for twelve
forms, retaining all homographs, and one qualified actual-entry
inspection receipt. The nine new direct quiz pairs concern actual
labels and applicable meanings, not transitive inference or general
Japanese substitutability. No original source field, mapping,
selected/additional sense or principal family changes.

### Multi-model usefulness

The 住宅 guard and 参加 navigation finding are shared. GPT uniquely
identified the other eight direct pairs; Claude uniquely contributed
the homograph clarification, concrete turn-over illustration and
more precise survival translation, plus adopted optional comparison
wording. Some initial severity/correctness framing was stronger than
the evidence required, and the stagk suggestion was unsupported.
This batch shows complementary useful coverage and review noise,
not a general model ranking or proof of native-speaker correctness.

### Confirmation and closure

Both original reviewers checked correction commit
`2a0eaee7685c42e869db924831dbb4bb71050e20`, parent
`033d125b6c4aa4438587e603296d582f2750195d`, against the actual
nine-card and provenance diff. They received the same bounded
scope, their own initial reports and the same source access,
without the other family's report or the author's reconciliation:

- [GPT confirmation](n2-vocabulary-reviews/batch-13-gpt-confirmation.md):
  `gpt-6.1-sol`; all eight original findings resolved.
- [Claude confirmation](n2-vocabulary-reviews/batch-13-claude-confirmation.md):
  `claude-opus-5.5`; all five original findings resolved.

Both found no actionable regression or consequential unresolved
claim in the changed scope. Actual-model usage receipts record
zero file edits; the processes ran sequentially and exited.
The first GPT confirmation attempt was interrupted without a
completed report; it exited before the same original session
was retried successfully. It supplies no additional verdict.

Both independently retrieved the Weblio turn-over construction.
GPT also checked the life-or-death phrase and the official
JMdict DTD. Claude withdrew its guest-example, alternative-release,
mandatory-send/escort and stagk-defect interpretations. The
remaining suggestions are nonblocking: explicitly repeating that
both 返る and 反る can express turning over, another 根 reading-row
example, and deduplicating identical families across the initial
and correction evidence. The present card already introduces the
turn-over sense under 返る and recognizes 反る; the separate
correction-family set is intentionally self-contained. A
cross-reference to 帰する alone does not establish a literary
register for 帰す/きす, so that suggested label is not added.

File-only reviewers did not independently execute Git, extraction,
hash or app checks. Before closing, the author verified both
frozen snapshots against their commits and checked the confirmed
cards, packet, manifest, prompt and actual patch hashes unchanged.
The generated manifest remains identical to the confirmed correction.

Cumulative coverage is **260 closed, 0 draft, 1,552 pending and
0 unresolved** rows, mapped to 255 distinct articles: 231 new and
24 reused. There are 3,504 word articles and 51 reciprocal N2
kanji-word pairs. All 3,273 baseline identities, primary readings,
titles and original exclusion lists remain preserved. This closes
batch 13, not the full vocabulary expansion or native-speaker
certification.

## Batch 14: N2:262-N2:281

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 各自, 拡充, 学術, 各地, 拡張, 角度, 学年, 学部,
格別, 確率, 学力, 掛け算, 可決, 火口, 下降, 重なる,
重ねる, 飾り, 火山, かしこまりました.

The draft adds **18 articles**. Existing `各地` receives only a
source-backed N2 field; existing `火山` receives that field and
a link on its existing 火口 comparison. Their stable identities,
readings, titles, prior teaching and original exclusions remain
unchanged. There are now 3,522 word articles.

The [source packet](n2-vocabulary-batch-sources/batch-14.json)
retains twenty raw rows, twenty complete principal families,
144 complete comparison families, verified component records and
ten qualified actual-entry inspection receipts. These receipts
describe author inspection, not independent reviewer retrieval.

The supplied 火口/かこう entry supports crater and boiler burner;
the raw source's origin-of-a-fire gloss belongs to separate
火口/ひぐち. The article retains かこう, recognizes the other
readings explicitly and does not claim to recover compiler intent.
The complete 拡張 technical escape/ESC sense remains in provenance
outside the selected practical enlargement lesson.

学部's undergraduate-division use is supported by the actual
Seisenban definition, not interpreted as an individual student.
The exact かしこまりました expression entry supports respectful
acceptance of requests, not universal truth-asserting "certainly."
掛け算 explicitly teaches a native-first mixed reading and voiced
ざん rather than misclassifying both components as on readings.

Three N2 kanji receive reciprocal examples and citations:
`各`/`各自`, `角`/`角度`, and `算`/`掛け算`. Existing plain-text
comparisons in `積む`, `級`, `アクセサリー`, and `能力` gain
links without changing their teaching. Missing written components
remain in word metadata without speculative new kanji cards.

The original source and all baseline word identities, primary
readings, titles, easier levels and exclusion declarations remain
preserved. Draft coverage is not review closure.

### Initial review

Both reviewers examined committed snapshot
`11d1b0ae8caf19e6aac628e1774a9f21d8ab503e`, parent
`8df57903f716932690acdff28f84b6e285924d94`, with the same
scope, rubric and source access. Separate read-only processes
ran sequentially and exited. Actual-model, zero-edit receipts
identify:

- [GPT initial report](n2-vocabulary-reviews/batch-14-gpt-initial.md):
  `gpt-6.1-sol`.
- [Claude initial report](n2-vocabulary-reviews/batch-14-claude-initial.md):
  `claude-opus-5.5`.

Both read all eighteen new articles, the nine-file related patch
and all twenty mappings. The reuse claims were not whole-card
recertification. File-only access could not authenticate Git or
hashes; the author subsequently checked all 33 frozen files
against the authored commit and current worktree, plus the
original prompt and related patch hashes.

GPT independently fetched nine article-cited Kotobank entries
and the additional dictionaries cited in its findings. Claude
fetched seven Kotobank entries and disclosed selective comparison
entry reading and an inference about easier-level absence, not an
independent lower-level source audit. Neither report certifies
every example's naturalness or exhaustive quiz safety.

### Reconciliation

| Observation | Adjudication and correction |
| --- | --- |
| GPT B14-GPT-01 / Claude B14-R01: 角度 / 立場 | Resolved: add the direct guard for viewpoint/standpoint overlap. Complete 1551710:2 at たちば supports the comparison, not the separate たてば identity. |
| GPT B14-GPT-02: 下降 / 下りる | Resolved: add the direct guard for ordinary descent. Complete 1589500:1 permits both spellings; the existing 降りる guard does not protect the separate 下りる card ID. |
| GPT B14-GPT-02 / Claude B14-R02: 下降 / 断る | Resolved: add the direct guard for English decline's downward-change/refusal polysemy. Complete 1419570:1 supports refusal; the Japanese verbs are not declared synonymous. |
| GPT B14-GPT-03 / Claude B14-R03: 学年 / 位 | Resolved: add the direct guard for school-grade versus quality-grade English polysemy. Complete 1155400:4 at くらい supports the latter, not the approximating particle or counter identities. |
| Claude optional: かしこまりました / 分かる | Adopt a direct guard and a linked acknowledgment comparison. Complete 1606560:1 and the existing 分かりました teaching support understanding overlap with 1002790:1. The respectful acceptance formula is not reduced to a general understanding verb. |
| Claude optional: 可決 / 可 | Adopt a direct guard. Complete 1190710:2 explicitly supplies approval/a vote in favor, beyond the existing card's foregrounded permission and grading senses. Shared written 可 alone would not justify it. |
| Claude optional: 飾り English article | Correct "an 飾り" to "a 飾り"; a small English-language polish, not a Japanese lexical defect. |
| Claude optional: a decoration compound example | Remains nonblocking expansion. Two translated examples already illustrate the decoration noun; no extra compound or unsupported frequency claim is required for the mapped sense. |
| Claude optional: 火口 title weighting | No title change. Both senses belong to the selected pinned family; the body explicitly separates the JMdict boiler-burner sense from the crater lesson and distinguishes the other readings. Listing senses does not assert equal frequency, and the inspected Japanese crater definition does not invalidate the separate pinned sense. |
| Claude optional: かしこまりました / 確か | Not established as an additional defect. Complete 1596930 distinguishes certain/reliable adjective senses and a tentative-recollection adverb; those are not themselves the respectful acknowledgment. Related English certainty wording alone is insufficient to assert another pair. |

The correction retains the initial twenty principal and 144
comparison families, original mappings and selected/additional
senses. Seven complete correction families for four forms were
re-extracted after both pinned dictionary hashes were verified;
all homographs and sense-local qualifications are retained.
Six new direct quiz pairs are added across five new articles;
飾り receives only the English article correction. No baseline
card, title, reading or original exclusion declaration changes.

The quiz safeguards are localized minor editorial defects or
supported optional improvements, not proof of a generally broken
quiz. The initial severity labels remain verbatim in the reports.
The rationale concerns displayed answers and applicable meanings,
not unrestricted Japanese substitution or measured candidate draws.

### Multi-model usefulness

The viewpoint, decline and grade findings are shared. GPT uniquely
identified the separate 下りる card-ID gap. Claude uniquely supplied
the useful optional 分かる and 可 leads and the adopted English
article polish. The compound example and title weighting remain
nonblocking preferences, and the certainty-adjective lead did not
establish a defect. Comparing the entire reports, rather than just
their Findings sections, shows modest complementary value here,
not a general model ranking or native-speaker certification.

### Confirmation and closure

Both original reviewers checked correction commit
`b25fe7bb94f433d618174553c1f5c13f46d8c0b1`, parent
`11d1b0ae8caf19e6aac628e1774a9f21d8ab503e`, against the
actual six-card and provenance diff. They received the same
bounded assignment, their own original reports and the same
source access, without the other family's report or the author's
reconciliation:

- [GPT confirmation](n2-vocabulary-reviews/batch-14-gpt-confirmation.md):
  `gpt-6.1-sol`; all three original findings resolved.
- [Claude confirmation](n2-vocabulary-reviews/batch-14-claude-confirmation.md):
  `claude-opus-5.5`; all three original findings resolved.

Both found the six changed contexts and packet additions CLEAN
for correctness, scoped coverage and comprehensibility, with no
actionable regression or consequential unresolved claim. Actual
model receipts record zero file edits; both processes ran
sequentially and exited.

Both independently retrieved the approval/vote sense of 可;
GPT also revisited the exact acknowledgment expression. Claude's
位 lookup returned unrelated material and supplied no evidence.
The pinned complete noun family, not that failed retrieval,
supports the grade guard. Claude withdrew its 確か guard lead.
Its further suggestions to link 下りる in the descent comparison,
expand 分かりました's agreement function and add a decoration
compound remain nonblocking, not additional closure conditions.

The manifest's absence from the linguistic patch is intentional:
the patch contains the assigned articles and source evidence,
while the generated manifest is separately hash-pinned and
included in the correction commit. Before closure, the author
authenticated both frozen commits and parentage, all confirmed
file and manifest hashes, both prompts, the actual patches and
all four model/zero-edit receipts. File-only reviewers did not
independently execute Git, extraction, hash or app checks.

Cumulative coverage is **280 closed, 0 draft, 1,532 pending and
0 unresolved** rows, mapped to 275 distinct articles: 249 new and
26 reused. There are 3,522 word articles and 54 reciprocal N2
kanji-word pairs. All 3,273 baseline identities, primary readings,
titles and original exclusion lists remain preserved. This
closes batch 14, not the full vocabulary expansion or
native-speaker certification.

## Batch 15: N2:282-N2:301

**Status:** closed after independent review, evidence-based
reconciliation and bounded confirmation.

Scope: 貸し出し, 過失, 果実, 貸間, 貸家, 個所, 過剰,
かじる, 課税, 下線, カセット, 加速, 加速度, 片仮名,
片付く, 塊, 固まる, 片道, 傾く, 片寄る.

The draft adds **20 articles**, with no reused principal articles.
There are now 3,542 word articles. The
[source packet](n2-vocabulary-batch-sources/batch-15.json) retains
twenty raw rows, twenty complete principal families, 181 complete
comparison families, verified component records and eleven
qualified author-inspection receipts. The heading-only 箇所
lookup is explicitly not independent lexical verification.

The raw transitive-sounding 片付く gloss is preserved but not
taught as modern transitive usage. The lesson selects intransitive
tidying, resolution and completion, leaving the marriage use
outside scope. 個所 distinguishes noun spelling restrictions
from counter variants. 片仮名 recognizes カタカナ without
transferring a kana-only reading record unrestrictedly to kanji.
片寄る recognizes 偏る without a rigid physical/mental partition.
加速度 includes directional velocity change; the everyday 加速
speeding-up lesson is not presented as the full physics definition.

Seven N2 kanji pages receive ten primary-form reciprocal pairs:
`個`/`個所`, `課`/`課税`, `税`/`課税`, `線`/`下線`,
`片`/`片仮名`, `片`/`片付く`, `固`/`固まる`,
`片`/`片道`, `傾`/`傾く` and `片`/`片寄る`.
固 also links its existing 固まり example to the 塊 article,
which explicitly recognizes that spelling. This additional alias
link is not counted as a primary-written-component reciprocal pair.

Existing mentions in 貸す, 片付ける, 噛む, 食べる, 往復,
テープ, ラジオカセット and ラジカセ gain narrow navigation links.
No speculative character or stroke cards are added for missing
components. All original source fields and baseline word identities,
primary readings, titles, easier levels and exclusion declarations
remain preserved.

At the authored snapshot, coverage was **280 closed, 20 draft,
1,512 pending and 0 unresolved**
rows, mapped to 295 distinct articles: 269 new and 26 reused.
There are 64 primary-form reciprocal N2 kanji-word pairs. These
draft and mechanical audit counts are not review closure.

### Initial reviews

The authored snapshot is
`88300af9b018b8735962595c837167bcad9e03bf`, directly after
`e85977a13ce629196d3e2b922e376a26056a3473`.
The same frozen snapshot, twenty complete articles, twenty
principal mappings, fifteen-file related patch and public evidence
were independently assigned to **GPT-6.1 Sol (`gpt-6.1-sol`)**
and **Claude Opus 5.5 (`claude-opus-5.5`)**. They ran as
isolated read-only processes, sequentially, with no delegation or
other-model report access; each exited without file edits.

The [GPT initial report](n2-vocabulary-reviews/batch-15-gpt-initial.md)
finds five direct quiz pairs and two missing substantive links.
The [Claude initial report](n2-vocabulary-reviews/batch-15-claude-initial.md)
finds two learner-wording problems, three direct quiz leads
(one shared with GPT), and a proposed spelling-frequency claim.
Both read all twenty principal articles and the actual related
patch, and judged every mapping and related change clean in all
three facets. Comparison families were selectively inspected;
neither reviewer claims exhaustive comparison/corpus coverage.

### Evidence-based reconciliation

Finding IDs below are qualified by model because both reports
number independently.

| Initial observation | Adjudication and correction |
| --- | --- |
| GPT B15-01: 固まる settlement labels | Accepted: add direct 済む and 落ち着く guards. The plan-becoming-firm sense 1266550:2 overlaps their actual settled/settle labels; indirect paths do not protect the pair. |
| GPT B15-02; Claude B15-05: 片付く | Accepted: add 落ち着く and 済ませる. Both models find the settled-arrangement pair; GPT additionally finds the unmarked English finish label. The Japanese transitivity distinction remains explicit. |
| GPT B15-03: 塊/具体 | Accepted: add the direct embodiment guard. Principal 1590410:3 expressly teaches the figurative sense and 1245020:1 supplies the existing comparison label. |
| GPT B15-04: navigation | Accepted: link 出す at its constituent introduction in 貸し出し and 不足 at its contrast introduction in 過剰. |
| Claude B15-01: 貸家 readings | Accepted: explain 家 as や in かしや and いえ in かしいえ. Replace dictionary-storage jargon with the actual restricted-spelling consequence. |
| Claude B15-02: 偏る frequency | Frequency claim not established by the supplied evidence: headword order and priority tags do not measure frequency or sense-specific spelling use. Treat the example suggestion as optional recognition improvement: show 偏った見方, retain both spellings and their shared meanings, and add no frequency claim. |
| Claude B15-03: 片仮名 | Accepted: state the usual カタカナ spelling and shared かたかな pronunciation directly; remove the confusing dictionary-record explanation. |
| Claude B15-04: 個所/位置 | Accepted: add 位置 for place/location answer-label overlap, using complete 1587310:1. |
| Claude B15-06: 貸家/家屋; optional 住宅 | Accepted: add 家屋 and 住宅. A bounded author follow-through adds 宅 and 建物 for the same broad house/building/residence labels, not every building subtype. |
| Claude optional wording | Tighten 傾く's agreement example and translation without an unstated proposal; make 課税's subject/item explanation positive; specify right-side luggage distribution and make 片寄る's shared-spelling guidance positive. |
| Claude optional 箇所 and 塊 wording | No preference claim inferred from dictionary order. The supported group-of-people example remains; ひとかたまり is optional polish, not an established lexical correction. |

Ten complete correction families for ten forms were re-extracted
after verification of both pinned JMdict hashes, read completely,
and attached to the packet: 1191780, 1245020, 1257540, 1295040,
1334150, 1338180, 1415750, 1493700, 1587310 and 1589220.
The initial 済む family 1295070 is retained. All twenty original
rows/mappings, selected senses, principal families, 181 initial
comparison families, component records and eleven qualified
inspection receipts remain unchanged. No new independent N2
classification is inferred from a comparison or secondary sense.

The correction changes eleven new article contexts, adds ten
direct quiz pairs and two substantive links, and preserves every
baseline identity, title, primary reading, easier level and original
exclusion. Its wording changes do not alter source coverage.

### Multi-model usefulness

Across the complete reports, the 片付く/落ち着く guard is a
shared useful discovery. GPT uniquely contributes four further
supported direct pairs (two 固まる guards, 片付く/済ませる
and 塊/具体) and the two substantive links. Claude uniquely
contributes the 貸家/家屋 and 個所/位置 guards, the optional
住宅 guard, and the 貸家/片仮名 comprehensibility corrections.
Claude's optional wording suggestions also improve the displayed
examples and remove author-defensive language. 宅 and 建物
are author follow-through, not unique reviewer discoveries.

The frequency recommendation is not accepted as an established
fact. Diversity is useful on this shared sample, but agreement is
not evidence by itself and these observations are not a general
model ranking. Both reviewers disclose file-only Git/hash limits,
unexecuted app behavior, selective comparisons and lack of
native-speaker/corpus certification.

### Bounded confirmation and closure

Both original models reviewed correction commit
`3491d8cb71d19115fcbfe8450b10097cac434110`, directly after
the authored snapshot. Each received its own original report,
the same bounded eleven-article assignment, the actual content
and provenance diff, and the same source access, without the
other model's report or the author's review ledger:

- [GPT confirmation](n2-vocabulary-reviews/batch-15-gpt-confirmation.md):
  `gpt-6.1-sol`; all four original findings resolved.
- [Claude confirmation](n2-vocabulary-reviews/batch-15-claude-confirmation.md):
  `claude-opus-5.5`; all six original findings reconciled, with
  the unsupported frequency remedy withdrawn.

Both read every changed article and all eleven assigned comparison
cards. They found all eleven changed contexts and packet additions
CLEAN for correctness, scoped coverage and comprehensibility,
without actionable regression or consequential unresolved claim.
Actual-model receipts record zero file edits; the reviewer
processes ran sequentially and exited.

Claude explicitly withdraws the frequency inference from dictionary
order/priority, while accepting the spelling-recognition improvement.
Its follow-up suggestion to show 片寄った見方 as another
possible form remains optional: the article already explicitly
allows both spellings for biased judgment. Removing the negative
カ + カ reading warning in 貸家 is also optional; neither
allowed reading is described as using those on readings. The
箇所 preference and ひとかたまり wording remain nonblocking.
No such optional lead establishes a remaining lexical defect.

GPT independently revisited the cited 片寄る and 片仮名 pages;
Claude used the supplied complete records without refetching them.
Neither provides corpus or native-speaker certification. The
linguistic patch intentionally excludes the generated manifest:
the manifest is separately hash-pinned and committed. Before
closure, the author authenticated both frozen commits and
parentage, every frozen file hash, both prompts, the actual
patches, the confirmed worktree/manifest hashes and all four
model/zero-edit receipts. The manifest was rebuilt twice
deterministically; file-only reviewers did not independently
execute Git, extraction, hashing or app behavior.

Cumulative coverage is **300 closed, 0 draft, 1,512 pending and
0 unresolved** rows, mapped to 295 distinct articles: 269 new
and 26 reused. There are 3,542 word articles and 64 primary-form
reciprocal N2 kanji-word pairs. All 3,273 baseline identities,
primary readings, titles, easier sourced levels and original
exclusion lists remain preserved. This closes batch 15, not the
full vocabulary expansion.

## Batch 16: N2:302-N2:321

**Status:** closed after initial, correction and follow-through review.

Scope: 学科, 学会, 楽器, 学級, 担ぐ, 括弧, 活字, 活躍,
活力, 仮定, 過程, 課程, 仮名, 仮名遣い, 鐘, 加熱,
兼ねる, カバー, 過半数 and 被せる.

This batch adds **20 articles**, with no reused principal articles.
The [source packet](n2-vocabulary-batch-sources/batch-16.json)
preserves twenty exact source rows, twenty complete principal
families, 146 complete comparison families, verified component
records and eleven qualified author-inspection receipts.

Two source-gloss problems require explicit qualification. 学級
teaches an organized school class, not the entire year implied by
"grade in school." For 仮名, the reading かな and entry 1590540
agree on kana scripts; the raw alias/pseudonym gloss belongs to
separate かめい entry 1577090. The raw rows are preserved
verbatim rather than silently repaired, and no independent N2
classification is assigned to that alias word.

仮名 explains its contraction without inventing freely reusable
individual readings. 仮名遣い retains づ and recognizes the
dictionary variants. Its official scope and particle-spelling
sources were decoded using the declared Shift-JIS charset after
an initial garbled extraction; a guessed missing page and
heading-only dictionary sections are not lexical verification.
The packet records the actual source sections and retrieval limits.

兼ねる separates concurrent functions/posts from the verb-stem
difficulty suffix and the possibility construction ～かねない.
被せる teaches かぶせる and distinguishes the separate きせる
homograph. 活字 distinguishes printing type from printed text
and preserves かつじ without a small っ. 過半数 explicitly
excludes equality with half and a merely largest plurality; its
denominator still depends on context.

Three primary-form reciprocal N2 pairs are added:
`担`/`担ぐ`, `課`/`課程` and `被`/`被せる`.
Nine existing word pages gain narrow navigation/comparison
updates: 学部, クラス, ベル, 片仮名, 送り仮名, 漢字,
ピアノ, バイオリン and 被る. Missing component cards do not
remove written characters from metadata or prompt speculative
kanji/stroke additions.

At the authored snapshot, coverage is **300 closed, 20 draft,
1,492 pending and 0 unresolved** rows, mapped to 315 distinct
articles: 289 new and 26 reused. There are 3,562 word articles
and 67 primary-form reciprocal N2 kanji-word pairs. Baseline
identities, primary readings, titles, easier sourced levels and
original exclusions are preserved. These are draft/mechanical
counts, not linguistic certification or review closure.

### Initial reviews

The authored snapshot is
`a3f5bd39d72e1dfc5361a8d2c213ef0f7cb79cc5`, directly after
`f0c4257b1097bb0cde57718096f0a1ecbb0e0d14`.
The same frozen twenty articles, twenty principal mappings,
twelve-file related patch and source access were independently
assigned to **GPT-6.1 Sol (`gpt-6.1-sol`)** and
**Claude Opus 5.5 (`claude-opus-5.5`)**. Their isolated,
read-only processes ran sequentially, delegated nothing and
exited without file edits.

The [GPT initial report](n2-vocabulary-reviews/batch-16-gpt-initial.md)
finds four direct quiz ambiguities. The
[Claude initial report](n2-vocabulary-reviews/batch-16-claude-initial.md)
finds two of the same pairs, another difficulty-label pair, and
overrestrictive attachment wording in 仮定. Both read all twenty
principal articles and the actual related patch; both judge all
twenty mappings and twelve related changes clean in the three
facets. Their comparison-family inspection is selective, not
exhaustive.

### Evidence-based reconciliation

| Initial observation | Adjudication and correction |
| --- | --- |
| GPT B16-GPT-01; Claude F2: 被せる/浴びせる | Accepted: add the direct guard. Principal 1484320:3 explicitly teaches pouring over, and 1547440:1 supports the actual pour-over answer label. |
| GPT B16-GPT-02: 学会/大会 | Accepted: 大会 1413180:1 includes convention/conference, not only tournament. Add the direct guard. |
| GPT B16-GPT-03; Claude F4: 学級/授業 | Accepted: the existing class/lesson label is ambiguous in the quiz. Add 授業 while preserving the explicit class-group versus lesson distinction. |
| GPT B16-GPT-04: 活躍/参加 | Accepted: active participation is explicit in 1208450:1 and overlaps the existing participation label. Add 参加 without equating mere attendance with an active contribution. |
| Claude F1: 仮定 attachment | Accept the overstatement concern, not the proposed frequency remedy. Present plain clause + と仮定する as one useful pattern and explain the actual 一万円だ example. Both original examples remain correct and unchanged. |
| Claude F3 and optional どうしても | Add 難しい for difficult/hard-to-do overlap and どうしても for its actual simply-cannot label. The latter needs a negative predicate; the guard does not erase that grammatical condition. |
| Claude optional カバー/皮 | Accepted: the broad covering label overlaps the actual outer-covering label and wrapping/sheath sense 1483800:3, not just the topic of skin. |
| Claude optional 仮定/もし and もしも | Accepted as conservative supposition/supposing answer-label guards, not Japanese noun/adverb interchangeability. Add both direct pairs; their shared exact title does not protect either from 仮定. |
| Claude optional 被せる/着る and 乗せる | Accepted for the actual unmarked put-on labels. The Japanese wearer, clothing/headwear and placement constructions remain distinct. |
| Claude optional 学会/組合 | Accepted: 1397620:1 expressly includes association, not only labor union. Add the direct association-label guard. |
| Claude optional 仮名遣い/送り仮名 | No overlapping answer established: kana orthography and kana endings after kanji describe a system and one spelling device. Keep their explanation, without making a whole-topic exclusion clique. |
| Claude optional 括弧 and 担ぐ examples | Remain optional expansion. The する possibility and fooling sense are already explained; no incorrect existing example or necessary construction gap was established. |

Thirteen complete correction families for eleven forms were
re-extracted after verification of both pinned JMdict hashes,
read completely and attached to the packet. This preserves the
additional mock-exam and calling-out homographs matched by
もし without importing their senses into the lesson. Initial
授業 family 1330290 remains available. All twenty original
rows/mappings, selected senses, principal families, 146 initial
comparison families, component records and eleven original
inspection receipts remain unchanged.

The author re-fetched the actual 仮定 entries. The historical
Seisenban nominal-complement example qualifies an overbroad
instruction but does not establish modern omission frequency.
The visible Bunpro entry supplies ordinary clause examples
and a mathematical-notation example, not the optional
XをYと仮定する construction. A search-generated university
PDF lead failed to fetch and is not verified evidence. No
new frequency or unrestricted copula-omission rule is added.

The correction changes seven new articles, adding twelve
direct quiz pairs and narrowing one explanatory passage.
It preserves baseline identities, titles, primary readings,
easier levels and original exclusion lists. Source coverage
and all reciprocal N2 links are unchanged.

### Multi-model usefulness

Across the complete reports, 被せる/浴びせる and 学級/授業
are shared useful discoveries. GPT uniquely contributes the
学会/大会 and 活躍/参加 pairs. Claude uniquely contributes
the 難しい guard and 仮定 wording concern, plus seven
accepted direct pairs from its optional leads: どうしても,
皮, both conditional adverbs, both put-on labels and 組合.
These optional observations count as Claude contributions,
not new author discoveries or findings unique to a later pass.

The suggested often-keeps-だ remedy is not adopted as an
established usage fact. The orthography-device guard and two
extra examples remain nonblocking. Diversity is useful on this
matched sample, but neither agreement nor a larger finding
count establishes correctness or a general model ranking.
Both reviewers disclose file-only Git/hash limits, selective
comparison coverage, unexecuted app behavior and lack of
native-speaker/corpus certification.

### Bounded confirmation and follow-through

The original reviewer sessions independently confirmed
`d93bc31ff036cc2588f162183abd9ab10182e32f`, directly after
the authored snapshot. Each received its own initial report,
the same seven-article assignment, the actual content/source
diff and source access, without the other model's report or
the author's review ledger.

The [GPT confirmation](n2-vocabulary-reviews/batch-16-gpt-confirmation.md)
resolves all four original findings. The
[Claude confirmation](n2-vocabulary-reviews/batch-16-claude-confirmation.md)
resolves all four of its original findings, explicitly rejects
its earlier frequency implication, and withdraws the optional
仮名遣い/送り仮名 guard. Both read every changed article,
all twelve comparison cards, both orthography cards, all
thirteen complete correction families and relevant principal
records. Both find the seven changed contexts and evidence
additions CLEAN in all three facets, with no actionable
regression. Their actual-model receipts record zero file
edits; the processes ran sequentially and exited.

GPT independently re-fetched the actual Kotobank and Bunpro
pages. Claude relied on its original Kotobank inspection and
the supplied new records, without a fresh Bunpro fetch.
The original extra-example suggestions remain optional.

Claude also raises 困難 and 無理 as nonblocking further
guards. Reading their complete existing cards and re-extracting
both complete families establishes the same difficulty/inability
label class: 困難 1289620:1-2 includes euphemistic inability
to carry out, and 無理 1530970:2 covers impossibility under
the circumstances. Their different word classes do not by
themselves disambiguate an English answer. The author therefore
adds both direct guards on 兼ねる, without changing its
teaching or the baseline comparison cards.

This bounded follow-through appends two complete families
and two pair records, bringing correction totals to fifteen
families and fourteen pairs. Both pinned source hashes were
verified again. The first thirteen families, first twelve
pair records, both new inspection receipts and all authored
evidence remain unchanged. These are confirmation-stage
leads, not additional blind-initial discoveries in the model
comparison above.

Before the follow-through, the author authenticated both frozen
commits and parentage, every frozen file, prompt and patch
hash, the confirmed tree/manifest hashes and all four actual
model/zero-edit receipts. The initial linguistic patch omitted
the generated manifest deliberately; the regenerated manifest
was committed and separately hash-pinned. Claude's inability
to establish that from the linguistic patch is a disclosed
review limit, not an uncommitted-manifest finding. Neither
reviewer executed Git, extraction, hashing, the app or its
manifest generator.

The same sessions then independently reviewed the bounded
follow-through at `2ccbec538c3ee9d5aa99192fc34a4642cd60a60e`,
directly after the first correction. The
[GPT follow-through](n2-vocabulary-reviews/batch-16-gpt-followthrough.md)
and [Claude follow-through](n2-vocabulary-reviews/batch-16-claude-followthrough.md)
read all three full cards, both complete new families, the
relevant principal sense, both appended rationales and the
actual patch including its generated manifest change. Both
find the changed card and packet additions CLEAN in all three
facets, without an actionable defect or consequential
unresolved claim. Claude also checks the current public
Jisho display, explicitly not a replacement for the pinned
dictionary extraction.

Claude withdraws its earlier grammatical-class hedge: the
English difficulty labels do not identify grammatical class,
and the adopted two guards resolve its confirmation-stage
lead. Its optional count-wording polish is not adopted:
the earlier thirteen-family/twelve-pair descriptions identify
the first correction, while the appended follow-through
explicitly records the fifteen-family/fourteen-pair totals.
These are stage-specific provenance, not conflicting final
counts or a new linguistic issue.

The author authenticates all three frozen commits and direct
parents, historical and current file hashes, all three prompt
hashes and actual patches, and six actual-model/zero-edit
receipts. Removing only the two appended families, two pair
records and follow-through note reconstructs the first
correction packet exactly. All twenty authored contexts and
twelve related content files match their appropriate
reviewed snapshots. Both final processes ran sequentially,
delegated nothing and exited without file edits. Their
file-only Git/hash and unexecuted-app limits remain explicit;
Claude marks manifest hash recomputation UNVERIFIED rather
than treating textual agreement as independent regeneration.

Cumulative coverage is **320 closed, 0 draft, 1,492 pending
and 0 unresolved** rows, mapped to 315 distinct articles:
289 new and 26 reused. There are 3,562 word articles and
67 primary-form reciprocal N2 kanji-word pairs. All 3,273
baseline identities, readings, titles, easier sourced levels
and original exclusions remain preserved. This closes
batch 16, not the full vocabulary expansion.

## Batch 17: N2:322-N2:341

**Status:** closed after independent GPT/Claude review and confirmation.

Scope: 釜, 紙屑, 神様, 剃刀, ガム, 貨物, かゆい, 歌謡,
殻, カラー, からかう, 空っぽ, かるた, 枯れる, カロリー,
かわいがる, 乾かす, 渇く, 為替 and 瓦.

This batch adds **19 articles** and reuses 枯れる for its
already explicit plant-withering sense, adding only the
sourced N2 level. The [source packet](n2-vocabulary-batch-sources/batch-17.json)
preserves twenty exact rows, twenty complete principal
families, 141 complete comparison families, verified
component evidence and ten qualified author-inspection
receipts. Comparison extraction includes candidates inspected
and declined, not only adopted quiz guards.

The raw カラー gloss bundles color and collar. Principal
1038500 supplies color, characteristic/atmosphere and hair
coloring; separate 2853151 supplies explicitly recorded
additional collar teaching. No independent N2 assignment is
inferred for the second family. Botanical homograph 2853152
remains comparison evidence, not an extra lesson.

剃刀 and 為替 use whole-word readings without invented
constituent readings. かるた explains its Portuguese origin
despite the hiragana spelling, while qualifying the generic
playing-cards gloss. かわいがる distinguishes affectionate
treatment from mere cuteness and flags its ironic harsh-use
sense as recognition guidance.

乾く's earlier absolute throat-spelling prohibition is
narrowly corrected: complete phrase family 1277350 records
喉が乾く as well as 喉が渇く. The useful ordinary-drying
versus-thirst distinction remains, including on 乾.
FDA food-energy evidence and NIST calorie/prefix evidence
support separate claims; they do not silently establish a
capital-C nutritional-Calorie convention.

Three new primary-form reciprocal N2 pairs are added:
`貨`/`貨物`, `乾`/`乾かす` and `替`/`為替`.
`枯`/`枯れる` was already linked. Existing 干す, 色 and
いじめる gain narrow navigation links; missing component
cards do not remove written kanji from metadata.

At the authored snapshot, coverage is **320 closed,
20 draft, 1,472 pending and 0 unresolved** rows, mapped
to 335 distinct articles: 308 new and 27 reused.
There are 3,581 word articles and 70 primary-form
reciprocal N2 kanji-word pairs. All 3,273 baseline identities,
primary readings, titles, easier sourced levels and original
exclusions remain preserved. These are draft/mechanical
counts, not linguistic certification or review closure.

### Initial independent reviews and reconciliation

Both initial reviewers assessed authored commit
`4fa37301b6863b299555ce1e9bc3e4855e0167d9`
against the same blind prompt, scope and source access.
They ran sequentially in isolated read-only processes;
actual-model receipts record `gpt-6.1-sol` and
`claude-opus-5.5`, each with zero file edits.

- [GPT initial](n2-vocabulary-reviews/batch-17-gpt-initial.md):
  nineteen complete new articles, eight related changes,
  the scoped reuse claim and all twenty mappings.
- [Claude initial](n2-vocabulary-reviews/batch-17-claude-initial.md):
  the same assigned content; it explicitly disclosed reading
  fewer complete comparison families and a partly unverified
  collar-usage hypothesis.

Five articles receive narrowly supported corrections:

| Finding | Reconciliation confirmed at f4d119b |
|---|---|
| B17-GPT-01 | Add the direct 剃刀/鋭い guard: the ordinary mental-sharpness sense can fit the unmarked sharp/keen answer even though the practical lesson teaches the razor tool only. |
| B17-GPT-02; B17-02 | Add direct 渇く/飢える and 渇く/憧れる guards for figurative craving and actual hunger-for/yearn-for labels. Both reports identified both leads, with different confidence; these are shared observations, not model-unique discoveries. Literal hunger, thirst and aspirational admiration remain distinct. |
| B17-01 | Replace the collar-only interpretation of シャツのカラー with explicit context dependence; add 襟 (えり) as another collar noun. No unverified shopping-frequency rule or failed lookup becomes evidence. |
| B17-03 | Demonstrate a person taking を with からかう and explicitly acknowledge the existing feature-object example. Do not imply two simultaneous を objects. |
| B17-04 | State usually-kana spelling directly and show 痒い (かゆい); remove the unclear speaking/kanji-reading instruction. The original mapping note is now demonstrated rather than weakened. |

Four complete correction families support 鋭い, 飢える,
憧れる and 襟, with both pinned dictionary hashes verified.
The packet appends those records, three direct-pair rationales
and three teaching clarifications without rewriting the
original mappings, principal families, initial comparisons,
component records or inspection receipts.

Optional additions for 殻, passive からかわれる and a
written 剃刀 example remain nonblocking expansion. The
為替/案 guard stays: the financial-draft/document-draft
ambiguity does not disappear merely because the main title
omits the word draft.

**Model-diversity note:** GPT uniquely established the
剃刀/鋭い issue; Claude uniquely identified the collar
interpretation, missing person-object demonstration and
unclear かゆい spelling instruction. The craving guards
were shared, including the weaker 憧れる lead. This is
useful complementary evidence on this sample, not a general
model ranking, exhaustive quiz audit or native-speaker
certification. The author-stage narrowing of named-color
and 物 guards preceded review and is not credited to either
reviewer.

### Independent confirmation and closure

The same original reviewers confirmed corrected commit
`f4d119b03e77fd032334cb737ea83cffc21c9445`
in bounded sequential sessions, each reviewing all five
changed articles, the actual diff and appended evidence:

- [GPT confirmation](n2-vocabulary-reviews/batch-17-gpt-confirmation.md):
  both original findings resolved; all five articles and
  packet additions CLEAN on each facet.
- [Claude confirmation](n2-vocabulary-reviews/batch-17-claude-confirmation.md):
  all four original findings resolved; all five articles
  and packet additions CLEAN on each facet. It withdrew
  its unsupported shopping-frequency assertion and the
  為替/案 redundancy suggestion. Reading the complete
  憧れる record increased its confidence in that guard.

No actionable defect, consequential unresolved teaching
claim or regression remains in the assigned scope.
Additional compounds, passive forms, spelling examples and
longer comparisons remain optional; no further expansion
was required merely to force agreement.

The author authenticated both committed snapshots, their
parentage, normalized file hashes, actual patches, prompt
hashes and four archived-report hashes against Git. Four
usage receipts confirm the requested actual models and
zero edits; all reviewer processes exited. The original
source packet is exactly preserved except for the appended
correction evidence. File-only reviewers explicitly did
not claim independent Git/hash or raw-source verification.
Structural checks, source records and lexical review are
not an executed app draw, frequency measurement or
native-speaker certification.

Closure coverage is **340 closed, 0 draft, 1,472 pending
and 0 unresolved** source rows, mapped to 335 distinct
articles: 308 new and 27 reused. There are 3,581 word
articles and 70 primary-form reciprocal N2 kanji-word
pairs. All 3,273 baseline identities, primary readings,
titles, easier sourced levels and original exclusions
remain preserved. This closes batch 17, not the full
vocabulary expansion.

## Batch 18: N2:342-N2:361

**Status:** closed after independent review, correction and bounded confirmation.

Scope: 代る mapped to 代わる, 間隔, 換気, 感激, 関西,
鑑賞, 感ずる, 間接, 乾燥, 感想, 観測, 寒帯, 官庁,
勘違い, 缶詰, 乾電池, 関東, 観念, 乾杯 and 看板.

This batch adds **19 articles** and reuses 乾燥 for its
explicit physical drying/dryness and figurative insipidity
senses, adding only the sourced N2 level.
The [packet](n2-vocabulary-batch-sources/batch-18.json)
retains twenty exact source rows, twenty complete principal
families, 109 complete comparison families, verified component
evidence and ten qualified author-inspection receipts.

代る is explicitly taught as an alias, with useful 替わる
and 換わる backlinks. 感ずる distinguishes JMdict's
ずる/じる framework from the Japanese サ変 analysis
without inventing godan forms. 勘違い and 缶詰 follow
the format's on-first `kango` convention while explaining
their mixed formations; 缶's loan origins remain qualified.

Regional entries separate modern 関西/関東 from variable
historical extents. Technical and social notes avoid literal
overreach: dry cells retain electrolyte, and 乾杯 does not
require drinking a whole glass at once. The 缶詰 food-science
lookup does not independently verify figurative confinement;
the complete pinned family supports that sense.

Twelve primary-form N2 pairs accompany new articles.
乾/乾燥 is additionally linked for the reused article;
燥/乾燥 was already linked. Alias backlinks do not increase
primary-form counts. Missing 隔, 激, 鑑, 勘 and 看 cards
remain represented in word metadata without speculative
character additions.

Existing 感覚, 缶, 意見, 感じる and the kaeru comparison
receive narrow navigation changes. Baseline identities,
readings, titles, easier levels and original exclusions
remain preserved.

Draft coverage is **340 closed, 20 draft, 1,452 pending
and 0 unresolved** rows, mapped to 355 distinct articles:
327 new and 28 reused. There are 3,600 word articles
and 82 tracked primary-form reciprocal N2 pairs on new
articles, plus the two checked 乾燥 pairs on the reused
article. All 3,273 baseline identities, primary readings,
titles and original exclusions are preserved; fifteen
previously unclassified baseline words now have explicit
source-backed N2 assignments. These are mechanical counts,
not independent linguistic certification or review closure.

### Initial reviews and evidence-based reconciliation

The blind initial reviews examined authored commit
`b002896e6b26b58dd7bd5b73194d73ec834c8997`.
[GPT](n2-vocabulary-reviews/batch-18-gpt-initial.md)
actually used **gpt-6.1-sol**; [Claude](n2-vocabulary-reviews/batch-18-claude-initial.md)
actually used **claude-opus-5.5**. They ran strictly
sequentially and exited without file edits. Each reviewed
all nineteen new articles, the twenty mappings and the
eighteen-file related diff; comparison-family inspection
was selective, and Claude did not fully read the component
records. Their commit/hash claims are receipt-supported,
not independently executed Git checks.

| Finding | Adjudication and bounded correction |
| --- | --- |
| GPT-01: 感激/感じる | Resolved: add the direct guard. Complete 1212260 sense 2 includes being moved, touched or impressed; the feel/sense title does not restrict the quiz to physical sensing. |
| GPT-02 / Claude F3: 観測/予報 and 占う | Resolved: add both direct guards. Complete 1543630 and 1389430 include prediction/forecasting, including 占う's nonsupernatural sense 2. Existing 予想/予測 guards are not transitive. |
| GPT-03 / Claude F2: 換気/干す | Resolved: add the direct guard for the unqualified English air-out label. This is not unrestricted Japanese interchangeability. |
| GPT-04: 看板/模様 | Resolved: add the direct appearance-label guard. A situation's appearance and an outward show remain distinct Japanese uses. |
| Claude F1: 代わる demonstrations | Resolved in the correction: add original role-replacement, driving-takeover and seat-switch examples for the selected senses and alias backlinks. Digital Daijisen's actual raw-HTML entry verifies the driving を construction; the full examples remain original, not corpus quotations. |
| Claude F4: opaque 換気 classification sentence | Resolved: delete the sentence rather than introducing an unnecessary new transitivity rule. |
| Claude F5: 感ずる and 感想/気味 | Resolved: add both direct guards. Complete 1222640 sense 1 is the noun きみ, sensation/feeling; neither suffix ぎみ nor market-reading きあじ supplies this evidence. 感想's principal family genuinely includes feelings. |
| Claude F6: 看板/兆候 | Resolved: add the direct sign/indication-label guard. Low shared-tag probability does not remove fallback ambiguity; a signboard is not thereby a symptom or omen. |

The packet appends **seven complete comparison families**
for five forms after both pinned source hashes were checked.
It retains the original rows, mappings, principal families,
component evidence, 109 initial comparison families, ten
initial inspections and initial quiz declarations/rationale
without silently backdating the corrections.
Two additional qualified inspection records distinguish the
actual Daijisen entry from Weblio's incomplete simplified
extraction, and the Culture Council's 2014 main entry from
its older reference appendix. Neither supports a universal
particle rule or proves the full original seat sentence
corpus-attested.

The reused 乾燥 article already explicitly covers insipidity
as well as physical drying. Pinned sense 2 is **insipidity**,
not another dryness sense: Claude's detailed reuse verdict
is correct. Shorthand in the initial reports' scope/reuse
summaries does not alter that identity or justify changing
the baseline teaching.

### Model-diversity usefulness

Compared across the whole reports, both models identified
換気/干す and 観測/予報/占う. GPT uniquely supplied the
supported 感激/感じる and 看板/模様 leads. Claude uniquely
supplied the missing 代わる demonstrations, the opaque
換気 sentence, and the 気味 and 兆候 guard leads. All were
adjudicated against exact meanings and labels, not accepted
by vote. This is complementary usefulness on this sample,
not a general model ranking.

Optional extra links from non-N2 components, more 感ずる
register teaching, 関西学院 and a poster comparison remain
nonblocking expansion. Failed or irrelevant dictionary
fetches and search pages were not counted as verification.
No measured frequency, executed app draw or native-speaker
certification is claimed.

### Independent confirmation and closure

The same original reviewers confirmed corrected commit
`f88b0591e38656b386b9a08d4a0f1a3a240751df`
in strictly sequential, bounded sessions:

- [GPT confirmation](n2-vocabulary-reviews/batch-18-gpt-confirmation.md):
  all four original findings resolved; all seven changed
  articles and packet additions CLEAN on each facet.
- [Claude confirmation](n2-vocabulary-reviews/batch-18-claude-confirmation.md):
  all six original findings resolved; all seven changed
  articles, packet additions, alias demonstration and
  narrow reuse clarification CLEAN on each facet.

Both independently inspected Weblio's actual raw-HTML
Daijisen entry and verified the driving construction.
Neither independently inspected the Culture Council PDF;
its main-entry/appendix qualification remains supported by
the author's recorded inspection. The full seat-switch
sentence remains editorially assessed against the pinned
change-places sense, not independently corpus-attested.
Claude's optional alternative-spelling remark is not
treated as measured frequency evidence.

No actionable defect, consequential unresolved teaching
claim or regression remains in the assigned scope. Extra
navigation, register teaching and other optional expansions
were not required merely to force agreement.

The author authenticated both committed snapshots, their
parentage, normalized file hashes, actual patches, prompt
hashes and all four archived reports. Four usage receipts
confirm the requested actual models and zero edits; the
original session identities were retained and all reviewer
processes exited. Original source claims and mappings are
unchanged; the correction evidence was appended rather
than backdated. File-only reviewers explicitly did not
claim independent Git, hash or raw-source authentication.
These checks do not constitute an executed app draw,
frequency measurement or native-speaker certification.

Closure coverage is **360 closed, 0 draft, 1,452 pending
and 0 unresolved** source rows, mapped to 355 distinct
articles: 327 new and 28 reused. There are 3,600 word
articles and 82 tracked primary-form reciprocal N2
kanji-word pairs on new articles, plus the two checked
乾燥 pairs on the reused article. All 3,273 baseline
identities, primary readings, titles, easier sourced
levels and original exclusions remain preserved. This
closes batch 18, not the full vocabulary expansion.

## Batch 19: N2:362-N2:381

**Status:** closed after independent review, correction and bounded confirmation.

Scope: 看病, 冠, 漢和, 気圧, 器械 mapped to 機械,
着替え, 機関車, 飢饉, 器具, 期限, 記号, 刻む,
儀式, 基準, 規準 mapped to 基準, 起床, 着せる,
基礎, 気体 and 基地.

This batch adds **18 articles** and makes a narrowly scoped
addition to existing N3 機械 for the 器械 apparatus sense.
The [packet](n2-vocabulary-batch-sources/batch-19.json)
retains twenty exact source rows, nineteen complete
principal families, 127 complete comparison families,
verified component records and seven qualified
author-inspection receipts. These receipts are not
independent reviewer retrieval.

冠 keeps primary かんむり distinct from supplementary
かんたる. 漢和 explains a Japanese-language kanji
dictionary rather than silently equating it with modern
Chinese-to-Japanese translation. 基準 and 規準 share
one article with explicit usage and a qualified spelling
contrast. 着せる/きせる remains distinct from existing
被せる/かぶせる despite its recognized shared spelling.
Original examples are teaching sentences, not corpus
quotations or measured-frequency evidence.

Four new primary-form N2 pairs accompany the new articles:
圧/気圧, 替/着替え, 準/基準 and 床/起床.
Existing 械/機械 remains reciprocal and gains explicit
器械 navigation. 規/規準 and 被/被せる at きせる
are useful alias backlinks, not additional primary-form
counts. 着 gains useful clothing links. Missing 儀,
冠, 器, 基, 看, 礎, 飢, 饉 and 饑 cards are not
manufactured; written primary-form characters remain
in word metadata.

The ten-file related scope comprises eight kanji cards
(圧, 床, 替, 械, 準, 着, 被 and 規) and two existing
word articles (機械 and 被せる). Edits are limited to
the new apparatus example, qualified comparisons,
navigation and applicable source attribution.
Existing identities, primary readings, titles, easier
levels and original exclusions remain unchanged.

Authored-snapshot coverage is **360 closed, 20 draft, 1,432 pending
and 0 unresolved** rows, mapped to 374 distinct articles:
345 new and 29 reused. There are 3,618 word articles
and 86 distinct tracked primary-form reciprocal N2
pairs on new articles, plus previously checked pairs
on reused articles. All 3,273 baseline identities,
primary readings, titles, easier sourced levels and
original exclusions remain preserved. These are
mechanical counts, not independent linguistic
certification or review closure.

### Initial reviews and evidence-based reconciliation

The blind initial reviews examined authored commit
`bec5240238e832cc953cbb1f04dbaaf3609a830c`.
[GPT](n2-vocabulary-reviews/batch-19-gpt-initial.md)
actually used **gpt-6.1-sol**; [Claude](n2-vocabulary-reviews/batch-19-claude-initial.md)
actually used **claude-opus-5.5**. They ran strictly
sequentially and exited without edits. Each read all
eighteen new articles, the ten-file related diff and
twenty mappings, with targeted comparison inspection.
Both rated all eighteen new articles CLEAN on each
facet. Their snapshot/hash identities are receipt-based,
not independently executed Git verification.

| Finding | Adjudication and bounded correction |
| --- | --- |
| GPT-01: 機械/道具 | Resolved in the correction: append the direct guard to 機械. Complete 1220810 sense 2 and 1454180 sense 1 share instrument/apparatus meanings. Existing 器具 declarations are not transitive. This is a pre-existing ambiguity exposed by the assigned 器械 reuse assessment, not a defect in the new example. |
| Claude O-01: 基地 wording | Optional, adopted: replace internal "musical bass identity" wording with an explicit separate-word explanation and cite already retained complete 2845313. This is a clarity improvement, not an actionable initial defect or new level assignment. |

The correction appends evidence without changing the
twenty rows, mappings, nineteen principal families,
component records, 127 comparison families or seven
initial inspection receipts. Initial declarations and
rationale remain evidence of the authored snapshot.
No additional extraction was needed.

All original baseline exclusion declarations remain in
their original order. **One baseline list gains an
evidenced addition:** 機械 changes from `[装置]` to
`[装置, 道具]`. The preservation audit explicitly
allows only that recorded addition; it still rejects
other list changes. This is not a claim that the
corrected list is byte-for-byte unchanged. Stable
IDs, readings, titles, written-kanji metadata and
easier levels remain unchanged.

### Model-diversity usefulness

Compared across the full reports, GPT uniquely
identified the supported direct 機械/道具 ambiguity.
Claude explicitly rated the reuse CLEAN and did not
raise that pair in findings, optional remarks or limits.
Claude uniquely suggested the adopted nonblocking
基地 clarity improvement. There is no shared actionable
finding in this sample. This is complementary use,
not a model ranking or proof that two clean verdicts
would certify exhaustive correctness.

Claude's extra term/abbreviation/naming examples,
気圧 wording, dash consistency and non-N2 backlinks
remain optional expansion or polish. Dictionary
recognition alone does not make a suggested new rare
collocation independently attested.

GPT independently inspected the relevant dictionary
bodies. Claude independently confirmed the Daijisen
基準, 規準 and 恩に着せる bodies; it explicitly read
only eight comparison families and relied on author
receipts, pinned families and editorial judgment for
the remaining stated claims. Irrelevant Kotobank
fetches and empty search pages are not verification.
No executed app draw, measured frequency or
native-speaker certification is claimed.

### Independent confirmation and closure

The original reviewers confirmed corrected commit
`976c03d8607af5db578c9ea79ba25650df59f42e`
in strictly sequential, bounded sessions:

- [GPT confirmation](n2-vocabulary-reviews/batch-19-gpt-confirmation.md):
  original GPT-01 resolved; both changed articles and
  appended packet evidence CLEAN on all three facets.
- [Claude confirmation](n2-vocabulary-reviews/batch-19-claude-confirmation.md):
  both changed articles and appended evidence CLEAN;
  it acknowledged the missed direct pair in its original
  reuse assessment and confirmed the guard's resolution.
  Its adopted O-01 is resolved; remaining suggestions
  stay optional.

The additional optional pronoun clarification is not
required to close the already clear separate-word
explanation. No actionable defect, consequential
unresolved teaching claim or regression remains in
the bounded scope. Neither confirmation performed
new public-source retrieval or an executed app draw.

The author authenticated both commits, their parentage,
normalized file hashes, actual patches, prompt hashes
and all four archived reports. All usage receipts
identify the requested actual models and zero edits.
The original reviewer sessions were retained and
all processes exited. A two-space Markdown line break
in one archived finding heading was normalized for
the whitespace check; report wording is unchanged.
Author-executed provenance checks are not reviewer
Git verification or linguistic certification.

Closure coverage is **380 closed, 0 draft, 1,432 pending
and 0 unresolved** source rows, mapped to 374 distinct
articles: 345 new and 29 reused. There are 3,618 word
articles and 86 distinct tracked primary-form reciprocal
N2 pairs on new articles, plus checked reused-article
pairs. All 3,273 baseline identities, primary readings,
titles, written-kanji metadata and easier sourced levels
remain preserved. All original exclusion declarations
remain, with only the explicitly recorded 機械/道具
addition. This closes batch 19, not the full expansion.

## Batch 20: N2:382-N2:401

**Status:** closed; both original reviewers confirmed the corrections.

Scope: きっかけ, ぎっしり, 基盤, 客席, 客間,
ギャング, キャンパス, 休業, 休講, 休息, 給与,
休養, 清い, 強化, 境界, 行事, 恐縮, 教養,
行列 and existing 漁業.

This batch adds **19 articles** and only the sourced
N2 level on the existing unclassified 漁業 article.
The [packet](n2-vocabulary-batch-sources/batch-20.json)
retains twenty exact source rows and complete principal
families, 178 complete comparison families, component
records and ten qualified author-inspection receipts.
These are not independent reviewer retrieval.

給与 preserves the raw provision sense and adds the
pay sense explicitly; its uniform-provision collocation
is supported by the actual Daijisen definition.
行列 teaches both queue/procession and matrix, with an
original three-row/two-column example. 客間 retains its
on-first mixed reading. 休息/休憩/休養 differ in
perspective without an invented duration rule.
恐縮 covers gratitude and the apologetic request preface.

The three newly reciprocal primary N2 pairs are
講/休講, 清/清い and 境/境界. Existing 漁/漁業
remains reciprocal. Missing 基, 盤, 養 and 縮 cards
are not manufactured, and their primary written
characters remain in metadata.

The related content scope is the three kanji cards
講, 清 and 境 plus the one-line 漁業 level addition.
Stable baseline identities, primary readings, titles,
written-kanji arrays and easier levels remain unchanged.
All original exclusions remain, with only the already
recorded batch-19 機械/道具 addition; this batch makes
no new baseline exclusion change.

Authored-snapshot coverage is **380 closed, 20 draft,
1,412 pending and 0 unresolved** rows, mapped to
394 distinct articles: 364 new and 30 reused.
There are 3,637 word articles and 89 distinct tracked
primary-form reciprocal N2 pairs on new articles,
plus checked reused pairs. These are mechanical
counts, not review closure or linguistic certification.

### Blind initial reviews and reconciliation

Both reviewers assessed the common authored snapshot
`bc40a3a045024123d13d384bc98ee982d085da28`,
all nineteen new articles, twenty mappings and the
same four-file related patch, one process at a time.
The [GPT report](n2-vocabulary-reviews/batch-20-gpt-initial.md)
records actual model `gpt-6.1-sol`; the
[Claude report](n2-vocabulary-reviews/batch-20-claude-initial.md)
records `claude-opus-5.5`. Both processes exited and
reported zero file edits.

| Observation | Evidence-based disposition |
|---|---|
| Claude B20-01: positive embarrassed/abashed use of 恐縮 missing | Resolved in the correction: JMdict 1236740 sense 2 expressly includes embarrassment from compliments or hospitality and shame about an error. Add the modest praise example with kana and translation, without treating ordinary stage embarrassment as equivalent. |
| Claude B20-02: 恐縮/恩 and 恐縮/申し訳 direct guards | Resolved: complete 1183090 and 1363050 support obligation/gratitude and apology/excuse overlaps. Add both direct pairs; do not infer them transitively. |
| Claude B20-03: 給与/納める direct guard | Resolved: complete 1589090 sense 4 supports pay/delivery/supply for 納める itself, without transferring the 収める-only achievement sense. Add the direct pair. |
| Claude optional 行事/機能 | Adopted: add a direct English-"function" guard and explain social event versus capability/operation. |
| Claude optional 休講/おやすみ | Adopted conservatively: the polite noun's day-off/absence use can describe time off, not just the good-night greeting. Add the direct guard; retain the class-status versus student-nonattendance distinction. |
| Claude optional きっかけ cue/合図 | Partly adopted as nonblocking clarification: principal 1591290 already includes "cue"; add a general starting-cue comparison and direct 合図 guard from complete 1284930. Specialist kabuki history or theater examples are not required. |
| Claude optional キャンパス wording | Adopted: remove "university life"; retain the independently inspected Daijisen extended "university" use. |
| Claude optional 客間/応接 | Not adopted: the inspected entries distinguish reception room from receiving visitors. The shared substring "reception" alone does not establish interchangeable actual titles. 応接間/応接室 are room compounds, not the bare activity noun. |
| Claude optional 境 reading example and psychology 強化 example | Remain optional: the existing 国境 reading example is valid, 境界 is already linked under common words, and the additional psychology sense is explicitly identified without claiming a conditioning lesson. |

The correction extraction inspected seven complete
comparison families; six newly needed families are
appended to the packet with exact direct pairs and
source qualifications. おやすみ was already present.
Initial rows, principal families, mappings, inspection
receipts, quiz declarations and author rationale remain
historical authored-snapshot evidence, not backdated.
All six changed content files are new batch-20 articles;
no baseline metadata or related kanji content is altered.

**Model-diversity note:** Comparing both complete initial
reports, including optional observations and limits,
GPT established no actionable finding or optional
suggestion. Claude uniquely identified the three
supported minor findings and the adopted optional
clarifications above. This is complementary value in
this sample, not a general model ranking or proof that
the GPT review covered every comparison.

**Limits:** Both initial reviews were file-only and did
not execute Git, hashes or app draws. Neither read all
178 comparison families completely. GPT independently
retrieved the three Daijisen bodies and seven Seisenban
bodies. Claude independently retrieved 恐縮, used
community Wiktionary pages for three words, and honestly
identified the footer-only きっかけ fetch as failed.
Claude also disclosed one accidental grep hit in the
excluded 行列 rationale after assessing that article;
no finding relied on it. Its peripheral inference that
absent component cards are necessarily not N2 is not
adopted: absence is not independent level evidence.
The completed kanji cohort is the selected community
list, not an official exhaustive modern JLPT syllabus.
Dictionary meanings support the original praise
example's use, not an independent corpus occurrence
of the full sentence or native-speaker certification.

### Independent confirmation and closure

The original reviewers confirmed corrected commit
`635730f7ae45b71057a903a3878adf5e66464aff`,
strictly sequentially in their original sessions:

- [GPT confirmation](n2-vocabulary-reviews/batch-20-gpt-confirmation.md):
  all six changed articles and appended evidence CLEAN
  on all three facets. It confirmed the correction
  without retrospectively claiming the initial findings.
- [Claude confirmation](n2-vocabulary-reviews/batch-20-claude-confirmation.md):
  B20-01, B20-02 and B20-03 resolved; all six articles
  and additions CLEAN. It withdrew the optional
  客間/応接 guard and its unsupported general
  inference from absent cards to universal N2 status.

The other example expansions remain optional, including
Claude's additional error-shame example for 恐縮.
No actionable defect, consequential unresolved teaching
claim or regression remains in the bounded scope.
GPT independently re-fetched the actual 恐縮 Seisenban
and キャンパス Daijisen bodies in confirmation.
Claude performed no new public retrieval in this pass
and relied on its original reading for three comparison
card bodies; its report states that limitation.

The author authenticated both commits and parentage,
normalized file hashes, actual patches, prompt hashes,
all four unchanged final report bodies and usage
receipts. Only report progress preambles were removed.
The original packet is preserved except for the appended
six complete comparison families and correction record.
All usage receipts identify the requested actual models
and zero edits. Original sessions were retained and
every reviewer process exited. These author-executed
checks are not reviewer Git verification, executed
app draws or linguistic certification.

Closure coverage is **400 closed, 0 draft, 1,412 pending
and 0 unresolved** rows, mapped to 394 distinct
articles: 364 new and 30 reused. There are 3,637 word
articles and 89 distinct tracked primary-form reciprocal
N2 pairs on new articles, plus checked reused pairs.
All 3,273 baseline identities, primary readings, titles,
written-kanji arrays and easier levels remain preserved.
All original exclusions remain with only the already
recorded batch-19 機械/道具 addition. This closes
batch 20, not the full vocabulary expansion.

## Batch 21: N2:402-N2:421

**Status:** closed after independent original-session
confirmation and author-executed provenance checks.

Scope: 曲線, 規律, 斬る, 気を付ける, existing 金魚,
区域, 偶数, 空想, 空中, クーラー, 釘, 区切る, 櫛,
くしゃみ, 苦情, 苦心, 屑, 崩す, 薬指 and 崩れる.

This batch adds **19 articles** and only the sourced
N2 level on existing 金魚. The
[packet](n2-vocabulary-batch-sources/batch-21.json)
retains twenty exact rows and complete principal
families, 217 complete comparison families, component
records and seven qualified author-inspection receipts.
All families were inspected, including restrictions
and ordinary secondary senses. These are author
access receipts, not independent reviewer retrieval.

規律 teaches both orderly discipline and governing
rules; クーラー teaches room air conditioning and a
portable cooler. 区切る covers spatial boundaries and
linguistic pauses, with raw stopping glosses qualified.
崩す explicitly preserves demolition and breaking a
banknote into equal-value smaller denominations.
苦心 is painstaking effort, not bodily pain; 苦情
acknowledges the dictionary's difficult-circumstances
coverage without turning it into every personal worry.
くしゃみ does not inherit the くさめ-restricted charm
sense. Additional senses are separately recorded,
not independently assigned an N2 level.

Five newly reciprocal primary-form N2 pairs are
線/曲線, 律/規律, 区/区域, 域/区域 and 区/区切る.
The related scope is four kanji cards, the one-line
金魚 level addition and a link around the existing
曲線 comparison in カーブ. Missing 斬, 釘, 櫛, 屑
and 崩 component cards are not manufactured; their
written characters remain in metadata. Missing
comparison articles remain plain text.

Stable baseline identities, primary readings, titles,
written-kanji arrays and easier levels are preserved.
All original exclusions remain with only the established
batch-19 機械/道具 addition; no new baseline exclusion
change is made.

Authored-snapshot coverage is **400 closed, 20 draft,
1,392 pending and 0 unresolved** rows, mapped to 414
distinct articles: 383 new and 31 reused. There are
3,656 word articles and 94 distinct tracked primary-form
reciprocal N2 pairs on new articles, plus checked reused
pairs. These are mechanical counts, not review closure
or linguistic certification.

Both blind initial reviewers received the same frozen
snapshot and evidence derivative, with only the
canonical packet's author quiz rationale removed.
The derivative's equivalence and hash are recorded
by the author process; this does not give file-only
reviewers independent Git or hash execution.

### Blind initial reviews and reconciliation

Both reviewers assessed the common authored commit
`b0dcca6434845e2b41b0161a8f0249502b182e46`,
nineteen complete new articles, twenty mappings,
the scoped 金魚 reuse and the same six-file related
patch, strictly one native process at a time.
The [GPT report](n2-vocabulary-reviews/batch-21-gpt-initial.md)
records `gpt-6.1-sol`; the
[Claude report](n2-vocabulary-reviews/batch-21-claude-initial.md)
records `claude-opus-5.5`. Both processes exited with
zero edits. The evidence derivative was equivalent
to the original packet except for removal of the
author's quiz rationale.

| Observation | Evidence-based disposition |
|---|---|
| GPT21-01: 崩れる/下降 | Resolved: add the direct guard. Principal 1516270 sense 4 includes financial decline/slump; complete 1184940 and the actual 下降 title include decline. Shared 下がる exclusions are not transitive. This does not promote the financial sense into the N2 lesson. |
| GPT21-02: 崩す/笑い | Resolved: add the direct guard. Principal 1516260 sense 6 is qualified by 顔を崩す; complete 1351280 sense 2 and the actual 笑い article teach a smile. Existing 笑う/笑顔/微笑む guards do not cover this noun. No unrestricted smiling/laughing substitution is asserted. |
| GPT21-03: 空中/架空 | Resolved: add the direct physical-sense guard, not an imaginary-sense or shared-kanji guard. Complete 1193130 sense 2 permits aerial/overhead at かくう; the imaginary sense's reading restriction does not apply to that physical sense. |
| Claude B21-R01: 崩す wording | Resolved: replace the opaque "license every same-object use" sentence with plain English about learning usual expressions separately. Definitions, transitivity, examples and the qualified substance are unchanged. |
| Claude optional 崩す/故障 | Adopted conservatively for English "break down"/"breakdown" ambiguity. Complete 1267180 supports equipment failure. The teaching continues to distinguish structural/disorder uses from a machine simply ceasing to function; the Japanese words are not declared general synonyms. |
| Claude optional 気を付ける/かまう | Adopted conservatively for the actual "mind; be concerned" title and ordinary care/attention senses in complete 1279680. Permission and childcare uses are not transferred to 気を付ける. |
| Claude optional 気を付ける/警告 | Not adopted: complete 1252360 and the actual title concern a communicated warning/admonition, not being careful. A shared 注意 comparison or exclusion is not direct evidence. |
| Claude optional 気を付ける/そろそろ | Not adopted: complete 1345605 and the actual title concern approaching time or a manner of slow movement. Shared carefulness does not establish interchangeable answers. |
| Claude optional figurative 斬る and 薬指/指輪 distractor | Remain nonblocking expansion, not defects in the declared physical-blade lesson or required link/ambiguity work. No invented collocation or new quiz configuration is needed. |

The correction extraction inspected seven complete
comparison families and appended six newly needed
families to the packet; 架空 was already present.
The original rows, families, component records,
selected/additional senses, seven inspection receipts,
quiz declarations and author rationale remain
historical authored-snapshot evidence, not backdated.
Five direct pairs and the wording clarification are
recorded separately. All four changed content files
are new articles; the six original related edits and
baseline metadata/exclusions remain untouched.

**Model-diversity note:** Comparing the complete
reports, including optional observations and limits,
GPT uniquely identified the three supported direct
quiz gaps. Claude uniquely identified the minor
comprehensibility defect and both adopted optional
guard clarifications. Neither report independently
contained the other's observations. This is useful
complementarity in this sample, not a general ranking.

**Limits:** Both initial reviewers were file-only and
could not execute Git, hashes or app draws. Neither
read all 217 comparison families. GPT independently
retrieved relevant Daijisen bodies; Claude's attempted
Weblio/Kotobank extractions yielded no usable bodies
and are not verification. Claude did not read component
evidence or author inspection receipts, checking kanji
against repository files instead. Its easier-level
check for 金魚 inspected the expected sorted sections
of the pinned N3/N4/N5 lists, not every source ID.
The author correction pass rechecked complete pinned
families and actual cards; two failed English-dictionary
lookups are recorded without verification credit.
The quiz fixes address possible ambiguous choices,
not observed generated questions or native-speaker
certification.

### Original-session confirmation and closure

Both original sessions resumed strictly sequentially
against corrected commit
`3ab605d7a0dadd2480ec891948c72b0a04abd218`,
directly following the authored snapshot. The
[GPT confirmation](n2-vocabulary-reviews/batch-21-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-21-claude-confirmation.md)
both report **CLEAN** for correctness, scoped coverage
and comprehensibility of all four changed articles and
the inspected packet additions. No actionable regression
or consequential unresolved claim remains in that scope.
Actual models remain `gpt-6.1-sol` and `claude-opus-5.5`;
both processes exited with zero edits.

GPT confirmed all three original direct-pair findings
resolved, accepted the two conservative optional guards
and established no need for the declined guards.
Claude confirmed B21-R01 resolved, accepted both adopted
optional guards and the 警告 disposition, and withdrew
the そろそろ suggestion. Claude regards 崩す/笑い as a
conservative safeguard rather than a necessary addition
to the selected lesson. That difference in calibration
is retained; neither reviewer requests its removal.
Figurative 斬る and the intentional distractor remain
nonblocking, not deferred defects.

The author authenticated both commits and parentage,
`stop-cran` author/committer identities, normalized
committed and current file hashes, original and correction
patches, both common prompts and both evidence derivatives.
Each derivative matches its snapshot's canonical packet
except for removal of the original author quiz rationale.
The original packet is preserved except for the six
complete appended comparison families and the separate
correction record. Unchanged new articles and all six
original related edits match their authored hashes.
All four reports match raw stdout after removing progress
preambles and normalizing Markdown two-space hard breaks
to blank lines; substantive text is unchanged. Usage
receipts match the original session timestamps, contain
only the stated models and record zero edits.

These are author-executed provenance checks, not
independent reviewer Git execution. GPT read the six new
families and relevant complete principal/comparison
families; Claude read the six appended families in the
patch, rechecked three relevant complete entries and
spot-checked the derivative's appended section. Neither
performed new successful public retrieval, app draws,
frequency measurement or a fresh whole-batch audit.
The initial review limits remain applicable.

Closed coverage is **420 closed, 0 draft, 1,392 pending
and 0 unresolved** rows, mapped to 414 distinct articles:
383 new and 31 reused. There are 3,656 word articles
and 94 distinct tracked primary-form reciprocal N2 pairs
on new articles, plus checked reused pairs. All 3,273
baseline identities, primary readings, titles,
written-kanji arrays and easier levels remain preserved.
All original exclusions remain with only the established
batch-19 機械/道具 addition. This closes batch 21,
not the full vocabulary expansion.

## Batch 22: N2:422-N2:441

**Status:** closed after sequential independent review
and original-session correction confirmations.

Scope: 砕く, 砕ける, くたびれる, くだらない, 下る,
唇, 口紅, くっつく, くっつける, くどい, 句読点,
配る, 工夫, 区分, 組み合わせ, 組み立てる, 汲む,
酌む, 悔しい and 悔やむ.

This batch adds **20 articles**, with no reused
principal article. The
[packet](n2-vocabulary-batch-sources/batch-22.json)
retains twenty exact rows and complete principal
families, 269 complete comparison families, component
records, 146 existing comparison labels/exclusions
and seven qualified public-inspection receipts.
All families and component records were inspected;
these author-access receipts do not imply independent
reviewer retrieval.

工夫 preserves the raw "labourer,worker" gloss but
explicitly corrects that homograph mismatch. Both
the source reading くふう and supplied entry 1278220
identify devising a method or its resulting idea.
Worker belongs to separate dated/sensitive
こうふ/1278230 and does not thereby gain N2.
組合せ maps to the explicitly taught 組み合わせ
alias, with all four unrestricted spellings retained.

悔やむ positively teaches the source-selected
mourning sense, with regret separately additional.
汲む and 酌む preserve genuine pouring/drinking
and feelings-consideration overlap without an
absolute water/sake or literal/figurative partition.
くどい retains both insistent expression and heavy
taste. Source-local dictionary numbering and the
partial 句読点 public inspection are qualified.
Additional senses do not independently gain N2.

Two new primary-form reciprocal N2 pairs are
紅/口紅 and 区/区分. The related three-file scope
is 紅 and 区 reading/common-word examples and a
link around 読's existing 句読点 example at トウ.
Missing 砕, 唇, 句, 汲, 酌 and 悔 cards are not
manufactured; written characters remain in metadata.
Missing comparison articles remain plain text.

All 3,273 baseline identities, primary readings,
titles, written-kanji arrays and easier levels are
preserved. No new baseline exclusion change is
made beyond the established batch-19 機械/道具 pair.

Authored-snapshot coverage is **420 closed, 20 draft,
1,372 pending and 0 unresolved** rows, mapped to
434 distinct articles: 403 new and 31 reused.
There are 3,676 word articles and 96 distinct tracked
primary-form reciprocal N2 pairs on new articles,
plus checked reused pairs. These mechanical counts
are not review closure or linguistic certification.

Both blind reviewers will receive the same frozen
snapshot, twenty whole articles, three-file related
patch, mappings and equivalent evidence derivative
with only the canonical author's quiz rationale
removed. Reviews run strictly one process at a time.

### Initial independent reviews and reconciliation

Authored commit:
`c84fdd3ce4b8467016517e5a21219a0dc54ea5da`.
Fresh sequential native processes used **gpt-6.1-sol**
and **claude-opus-5.5** on that same snapshot and
common prompt/evidence. Both exited without edits
before author reconciliation. Reports:
[GPT](n2-vocabulary-reviews/batch-22-gpt-initial.md)
and [Claude](n2-vocabulary-reviews/batch-22-claude-initial.md).
Both read all twenty new articles, all twenty mappings
and the scoped three-file patch with changed passages
in context. Neither read all 269 comparison families.
Neither had executable Git/hash access.

| Item | Reconciliation |
| --- | --- |
| GPT22-F01 / B22-01: 工夫/知恵 ingenuity overlap | Resolved by a direct 知恵 guard on 工夫; the actual titles and complete families support the overlap. |
| GPT22-F02 / Claude optional: くっつく/べたべた | Resolved by a direct べたべた guard. Physical adherence and interpersonal clinging overlap; no unrestricted substitution rule is inferred. |
| GPT22-F03: 組み立てる/セット | Resolved by a conservative direct セット guard for the broad setting-up English answer, not by equating furniture assembly with configuring every alarm. |
| B22-02: 悔しい's "mortified" label | Resolved by frustrated/disappointed in title and heading. A retrieved English adjective entry supports an embarrassment reading; this is a learner-facing ambiguity fix, not proof that JMdict's "mortifying" gloss is obsolete or an absolute division between frustration and humiliation. |
| Claude optional: くっ付く pronunciation sentence | Resolved by the plain statement that this spelling is still read くっつく. |

The first three corrections add guards only to new
articles. No baseline metadata/exclusions change.
The title revision keeps the existing disappointment
guards and does not add 恥ずかしい merely because
the removed English label was ambiguous. No source
mapping, selected/additional sense, level or identity
changes. The original source packet remains historical,
with three complete new comparison families and a
separate correction record appended, not backdated.

Nonblocking expansions not adopted: 汲む's tradition
inheritance lesson and a separate literary 口惜しい
discussion. The former complete family was already
available; the latter distinct-word/register proposal
was not separately verified and is not promoted into
teaching or a correctness conclusion. Claude
found no need for a punctuation/dividing or
water-drawing/picture-drawing guard based only on
English substrings or related concepts.

Model-diversity signal is useful but bounded. Shared
工夫/知恵 is one defect, not two. The clinging guard
appears in both reports, including Claude's Optional
section, so it is not GPT-unique. GPT uniquely supplied
the adopted 組み立てる/セット guard; Claude uniquely
supplied the adopted 悔しい title-ambiguity fix and
pronunciation-sentence simplification. This sample is
not a general model ranking. Claude's inference that
omission from selected evidence proves the author
"never considered" a pair is not independently
established and receives no additional discovery credit.

GPT independently inspected the cited Japanese public
bodies for its findings. Claude did not independently
retrieve those Japanese entries; its English-dictionary
access was mixed. Author reconciliation read five
complete extracted families and the actual four
comparison cards. A first simplified Wiktionary fetch
and a first raw footer range were not lexical
verification; the subsequent actual English adjective
body was inspected. No executed app draw, measured
frequency or native-speaker certification is claimed.

### Correction confirmations and closure

Corrected commit:
`fe0722835c3bb39ad8caf90433c2936658141bdb`.
The original sessions resumed sequentially, without
edits or access to one another's reports:
[GPT confirmation](n2-vocabulary-reviews/batch-22-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-22-claude-confirmation.md).
Both assessed all four changed articles, necessary
comparison cards and the appended evidence as
**CLEAN / CLEAN / CLEAN** within the bounded scope.
GPT resolved all three original findings. Claude
resolved both findings and withdrew the alternative
恥ずかしい guard after the ambiguous English label
was removed. Both accepted the adopted
clinging guard and pronunciation simplification.

GPT read four complete relevant principals and four
complete comparisons and independently inspected the
English adjective body. Claude read three complete
principals and four complete comparisons, checked
nearby emotion labels and compared manifest/receipt
hash strings without computing them. Neither
performed a fresh whole-batch audit or executable
Git/hash verification.

Claude's new optional しょんぼり guard remains
nonblocking. The actual card teaches a subdued,
downcast manner, not necessarily bitter frustration;
the words can occur after the same defeat without
being an unrestricted semantic match. No absolute
non-overlap rule or additional N2 teaching is inferred.
The unchanged card was inspected during author
reconciliation. No further content change was made.

Author-executed authentication verifies both commit
identities/parents and `stop-cran` author/committer
trailers, committed file hashes, common prompts,
actual scoped patches and both sanitized evidence
derivatives. The correction's four files match the
confirmed tree, including the tracked manifest
omitted deliberately from the narrow reviewer patch.
All sixteen untouched new articles and the three
original related edits retain authored hashes.
Through confirmation, the original packet is preserved
except for three appended complete comparison families
and its separate correction record.

All four archived reports match raw stdout after
removing progress preambles and normalizing Markdown
two-space hard breaks to blank lines. Substantive
report text is unchanged. Usage receipts show only
the stated actual model, the original session start
timestamp, one initial request and two cumulative
requests at confirmation, and zero file edits. These
checks authenticate provenance; they do not certify
linguistic correctness.

Closed coverage is **440 closed, 0 draft, 1,372 pending
and 0 unresolved** rows, mapped to 434 distinct
articles: 403 new and 31 reused. There are 3,676 word
articles and 96 distinct tracked primary-form
reciprocal N2 pairs on new articles, plus checked
reused pairs. All 3,273 baseline identities, primary
readings, titles, written-kanji arrays and easier
levels remain preserved. The only established baseline
exclusion addition remains batch-19 機械/道具.
This closes batch 22, not the full expansion.

## Batch 23: N2:442-N2:461

**Status:** closed after independent initial reviews,
evidence-based reconciliation and bounded confirmation.

Scope: クリーニング, くるむ, くれぐれも, 咥える,
郡, 稽古, 敬語, 蛍光灯, 形式, 継続, 毛糸, 経度,
系統, 芸能, 競馬, 警備, 形容詞, 形容動詞, 外科, 毛皮.

This batch adds **19 articles** and reuses 形式.
That baseline article retains its identity, title,
primary reading, kanji array, tags and previous
teaching; it gains the sourced N2 level and bounded
formality/mathematical-form coverage. Existing
包む remains N4 つつむ: separate usual-kana くるむ
is not a replacement for that identity.

The [batch evidence](n2-vocabulary-batch-sources/batch-23.json)
preserves original source rows, selected/additional
senses, complete principal/comparison families,
component readings and qualified public-inspection
receipts. Corrections/qualifications address
くるむ's transitivity, 郡's raw "country",
形式's broad "math expression", 系統's unestablished
geology gloss and 芸能's cultivated accomplishments.
The source-selected 蛍光灯 person label is positively
taught with its dated qualification.

Nine existing N2 kanji cards receive useful links:
包, 敬, 灯, 毛, 糸, 芸, 競, 詞 and 皮.
There are ten new primary-form reciprocal pairs,
plus 包/くるむ through the recognized 包む spelling.
Missing component cards are not invented.
All other existing written components are linked
substantively; rare alias 毛革 does not create a
primary-form 革 pair. Baseline quiz exclusions
were unchanged at the authored snapshot.

Initial reviewers received one common frozen snapshot,
equivalent source access and the same three-facet
rubric, with only the author's quiz-guard rationale
removed from the initial evidence derivative.
They ran strictly sequentially and exited
before the next reviewer started.

### Initial independent reviews and reconciliation

Authored commit:
`5319eaaa54325198f3ac7a4d0b92a61373495a17`.
Fresh sequential processes used **gpt-6.1-sol**
and **claude-opus-5.5** with the same frozen
snapshot, common prompt, scope and sanitized
evidence. Both exited without edits before
reconciliation. Reports:
[GPT](n2-vocabulary-reviews/batch-23-gpt-initial.md)
and [Claude](n2-vocabulary-reviews/batch-23-claude-initial.md).
Both read all nineteen new articles, twenty mappings
and the ten related changes in context. Neither
independently executed Git/hash checks or read every
complete comparison family. Their differing source
inspection limits remain in the reports.

| Item | Reconciliation |
| --- | --- |
| B23-GPT-01: 系統/筋 | Resolved by a direct 筋 guard. Complete 筋/すじ sense 7 supports lineage even though the existing card selects other senses. |
| B23-GPT-02 / B23-OPUS-02: form labels | Resolved with all six direct pairs among 形式, 形, 型 and 式. This protects comparison-to-comparison choices too, without asserting unrestricted Japanese substitution. |
| B23-GPT-03: substantive navigation | Resolved by 位置 and 嫌い links in 経度 and 形容詞. |
| B23-OPUS-01: 芸能/能 | Resolved by a direct 能 guard for the broad talent/accomplishments overlap; not merely because noh belongs to performing arts. |
| B23-OPUS-03: 何郡 reading | Resolved locally by どの郡/どのぐん. The proposed categorical なん/なに rule remains unestablished because no direct 何郡 entry was found. |
| B23-OPUS-04: kanji source footers | Resolved by adding the applicable principal IDs to 毛, 灯, 皮, 芸 and 詞. This is provenance consistency, not a learner-facing reading defect. |
| Claude optional: 青/赤 color-family wording | Adopt the exact Daijisen 青系統の色 pattern with kana/English; do not claim a measured naturalness ranking. |
| Claude optional: 敬語/御中/氏 and 芸能/教養 | Adopt conservative direct guards based on the actual respectful-expression and cultivated-accomplishment senses, not related topics alone. |
| Claude optional: 形式を整える translation | Adopt putting something into proper form without implying that every occurrence processes formalities. |
| Claude limit: 芸能を身につける | Remove the unverified illustrative collocation. Both principal senses remain positively taught; dictionary recognition alone does not certify an invented example's naturalness. |

The optional classical-origin expansion for 稽古 is
not adopted. Its current mnemonic is expressly
labelled; it does not deny a historical account.
No new etymological conclusion is asserted.

Reconciliation inspected fifteen complete extracted
families for nine forms, all 106 derivative records
and the actual comparison cards. Both pinned
JMdict hashes were rechecked, and already available
families compare exactly. Only new families and a
separate correction record are appended. Original
rows, mappings, selected/additional senses, labels,
inspection receipts and quiz declarations remain
historical rather than silently rewritten.

The form-quartet fix deliberately extends three
baseline lists: 形式 gains [形, 型, 式], 形 gains
[型, 式], and 型 retains [タイプ, 種類] and adds
式. These exact exceptions supplement batch-19's
機械/道具 addition. No baseline identity, reading,
title, written-kanji array or easier sourced level
changes. All other new guards are declared on new
articles. There are eleven direct new pairs total.

Model diversity was useful on this sample. The
形式/形 observation is shared and counted once.
GPT uniquely supplied the additional five
form-quartet pairs, 系統/筋 and the two missing
substantive links. Claude uniquely supplied the
adopted 芸能/能 guard, disputed-reading rephrase,
source-footer consistency fix and optional
honorific/cultivation guards and wording refinements.
Its unverified 芸能 example concern also led to a
prudent removal. Findings, Optional and Limits were
compared together; severity labels do not create
new discoveries. This is not a general model ranking.

The two new author public inspections read complete
Daijisen 芸能 and 系統 bodies. They support the
cultivated-ability teaching and adopted color pattern,
not corpus frequency or proof that removed wording
was impossible. Reviewer access and author retrieval
remain distinct. No executed app draw or
native-speaker certification is claimed.

### Confirmation, authentication and closure

Both original sessions independently confirmed
correction commit
`9f8d7d12e2704a7265cd5d2be9e03ee6d397b98b`,
whose parent is the authored commit above.
The shared bounded assignment covered nine word
articles, five kanji source footers, necessary
unchanged comparisons and appended evidence.
Each reviewer received its own original report,
the actual correction patch and the same sanitized
confirmation packet, not the other family's report.
GPT exited fully before Claude resumed; both
confirmation processes exited without edits.

- [GPT confirmation](n2-vocabulary-reviews/batch-23-gpt-confirmation.md):
  actual `gpt-6.1-sol`; B23-GPT-01 through 03 resolved.
  All fourteen changed content items and both packet
  additions received CLEAN three-facet verdicts.
- [Claude confirmation](n2-vocabulary-reviews/batch-23-claude-confirmation.md):
  actual `claude-opus-5.5`; B23-OPUS-01 through 04
  resolved, along with the adopted optional and
  uncertain-example corrections. All fourteen
  content items and packet additions were CLEAN.

Neither found an actionable regression or a
consequential unresolved linguistic claim within
the changed passages. Claude's additional example
for formality is optional polish; the current
positive explanation is adequate. Its tentative
式/方法 and 筋/才能 comparisons concern unchanged
baseline material, remain unverified and are not
newly approved or asserted as established defects.
No unrelated baseline expansion was made.

Author-executed authentication checked both commits'
parents, stop-cran identities and required trailers;
committed file hashes; unchanged authored content;
both exact patches and prompt hashes; and both
sanitized evidence derivatives. Removing only the
two appended evidence sections reproduces the
original canonical packet exactly. The eight new
complete families match extraction; all seven
previously available families compare exactly.
The eleven direct pairs, three exact baseline
exclusion extensions, two substantive links and
five footer corrections agree with their record.

All four archived reports match their original
output after removing progress preambles and
normalizing Markdown hard breaks. Original session
IDs and start times, actual model metrics, zero-edit
receipts and cumulative one/two-request counts agree.
Both exact common prompts were also checked against
the original sessions' recorded user messages.
These are author-executed provenance checks, not
reviewer-executed Git or linguistic certification.

Closed coverage is **460 closed, 0 draft, 1,352 pending
and 0 unresolved** rows, mapped to 454 distinct
articles: 422 new and 32 reused. There are 3,695 word
articles and 106 distinct tracked primary-form
reciprocal N2 pairs on new articles, plus checked
reused pairs and the 包/くるむ alias-reading pair.
All 3,273 baseline identities, primary readings,
titles, written-kanji arrays and easier levels
remain preserved. Baseline exclusion additions
are exactly batch-19 機械/道具 and this batch's
形式, 形 and 型 extensions described above.
This closes batch 23, not the full expansion.

## Batch 24: N2:462-N2:481

**Status:** closed after independent initial reviews,
evidence-based reconciliation and bounded confirmation.

Scope: 激増, 下車, 下旬, 下水, 削る, 桁, 下駄, 血圧, 血液, 月給,
傑作, 月末, 気配, 下品, 煙い, 蹴る, 険しい, 見学, 謙虚, 原稿.

Twenty new articles cover the twenty original rows. No existing word
identity, primary reading, title, easier level or exclusion list is changed.
The collection has 3,715 word articles. Four primary reciprocal N2 pairs
are added on 圧, 血 and 液, with exact whole-word readings and source footers.
Existing 増 is also linked substantively from 激増; missing component cards
are not manufactured.

The [source packet](n2-vocabulary-batch-sources/batch-24.json) retains
raw source rows, complete principal and comparison families, verified
component records, actual comparison labels and seven qualified author
public-entry receipts. The original 削る percentage gloss is resolved to
separate はつる/1298100, not taught at selected けずる/1298090.
桁's column and 険しい's sharp eyes receive context-sensitive teaching.
気配 positively includes market tone while raw worry remains unestablished.
下水's two senses, 傑作's qualified humorous use and 険しい's stern expression
are positively covered. Additional senses are explicitly separated from
independent N2 assignments.

### Initial independent reviews and reconciliation

Both blind initial reviews inspected authored commit
`15d8c88a4e49aef85600feb3a6cb1886f7425b14`, GPT-6.1 Sol then
Claude Opus 5.5, in independent sequential processes with no file edits.
The source derivative removed only `quizGuardRationale`; no prior
findings, author adjudication or other-family report was supplied.
The [GPT report](n2-vocabulary-reviews/batch-24-gpt-initial.md) established
three direct quiz gaps: 傑作/愉快, 気配/調子 and 原稿/テキスト.
The [Claude report](n2-vocabulary-reviews/batch-24-claude-initial.md)
established 見学/訪問・訪ねる and raised an unverified market example.
Both read all twenty new articles, the twenty mappings and all three
related kanji changes. Neither independently executed Git/hash checks
or inspected every complete comparison family. Claude disclosed an
accidental read of neighboring TSV rows; those rows were not assessed
and do not enlarge the review scope.

| Item | Reconciliation |
| --- | --- |
| N2B24-GPT-01: 傑作/愉快 | Resolved with a direct 愉快 guard for the actual amusing answer and selected humorous sense; jocular/dated qualifications remain. |
| N2B24-GPT-02: 気配/調子 | Resolved with a direct 調子 guard for the actual tone/condition label and financial market tone. This does not assert unrestricted Japanese financial substitution. |
| N2B24-GPT-03: 原稿/テキスト | Resolved with a direct テキスト guard for prepared manuscript/speech text; the comparison's ordinary text sense is not restricted to textbooks. |
| B24-Q-01: 見学/訪問・訪ねる | Resolved with both direct guards. The comparison titles are identical to each other, not to 見学; exact-title deduplication does not protect these two new pairs. |
| B24-C-02: 気配 market example | Resolved by replacing the uncertain sentence with the actually inspected 買い気配 compound and making the financial きはい cross-reference explicit. The removed sentence is not proven incorrect, and けはい is not excluded from finance. |

Reconciliation adds the five direct guards after inspecting all five
comparison cards and complete pinned families. The uncertain 気配
sentence is replaced by Daijisen's actually inspected 買い気配 compound.
The financial きはい cross-reference is now explicit, without claiming
that けはい is incorrect in finance or that the removed sentence was
demonstrably wrong. Two exact public-entry inspection receipts and
qualified correction evidence are appended without changing original
rows or mappings. Optional examples, disclaimer polish and extra
lower-level backlinks are not required for closure and are not added.

The reconciliation extracted five complete comparison families for
five exact forms and inspected all 25 derivative records, plus the
actual five comparison cards and labels. Both pinned JMdict hashes
were checked. The five families are new to the packet; original rows,
mappings, selected/additional senses, comparison records and initial
quiz declarations remain historical rather than silently rewritten.
There are now 86 directional declarations on seventeen new articles.
No existing word exclusion list or other baseline field changes.

The actual complete Daijisen bodies positively license financial
けはい and cross-reference きはい; the separate latter entry points
back to both けはい senses. A finance-only-きはい rule is not adopted.
The compound 買い気配 is supported by its own inspected Daijisen
entry, not a fabricated pinned-JMdict record. Failed attestation
searches justify removing uncertainty, not declaring an expression
impossible or making comparative frequency claims.

Model diversity was useful on this sample. GPT uniquely established
the three first-listed direct quiz gaps. Claude uniquely supplied
the two visit guards and the uncertain market-example concern,
which led to a prudent replacement and clearer reading qualification.
There was no shared actionable initial finding. Findings, Optional,
Limits and per-card observations were compared together; later
confirmation of a correction is not a second independent discovery.
This is not a general model ranking.

### Confirmation, authentication and closure

Both original sessions independently confirmed correction commit
`423cdee6300551714862d84d66f31bde3bb01a05`, directly following the
authored commit above. The common bounded assignment covered all
four changed articles, five necessary unchanged comparison cards
and appended evidence. Each received its own initial report, the
actual patch and equivalent sanitized evidence, not the other
family's report. GPT exited fully before Claude resumed; both
processes exited without file edits.

- [GPT confirmation](n2-vocabulary-reviews/batch-24-gpt-confirmation.md):
  actual `gpt-6.1-sol`; all three original findings resolved.
  All four changed articles and both packet additions received
  CLEAN correctness, scoped-coverage and comprehensibility verdicts.
- [Claude confirmation](n2-vocabulary-reviews/batch-24-claude-confirmation.md):
  actual `claude-opus-5.5`; B24-Q-01 and B24-C-02 resolved.
  All four changed articles and packet additions were CLEAN on
  all three facets. Optional expansions remain optional.

Neither found an actionable regression or consequential unresolved
claim within the changed passages. Both independently inspected the
relevant 気配 and 買い気配 public lexical bodies; Claude additionally
closed its original 桁 and 下駄 source-access limits. Its qualified
伺う comparison did not establish a new defect and caused no
unrelated baseline expansion.

Author-executed authentication checked both commits' parents,
stop-cran author/committer identities and required trailers;
committed and current file hashes; unchanged authored content;
both exact patches and prompt hashes; and both sanitized evidence
derivatives. Removing only the two appended evidence sections
reproduces the original canonical packet exactly. All five new
complete comparison families match the pinned extraction, and
the exact five direct additions match the current article headers.
No primary title, reading, level, kanji array or source mapping changed.

All four archived reports match original output after progress
preambles are removed and Markdown hard breaks are normalized.
Original session IDs and start times, actual model metrics,
zero-edit receipts and cumulative one/two-request counts agree.
Both exact common prompts match the original sessions' recorded
user messages. These are author-executed provenance checks,
not reviewer-executed Git or linguistic certification.

Closed coverage is **480 closed, 0 draft, 1,332 pending and
0 unresolved** rows, mapped to 474 distinct articles: 442 new
and 32 reused. There are 3,715 word articles and 110 distinct
tracked primary-form reciprocal N2 pairs on new articles, plus
checked reused pairs and the prior 包/くるむ alias-reading pair.
All 3,273 baseline identities, readings, titles, written-kanji
arrays and easier sourced levels remain preserved. Prior
baseline exclusion exceptions are unchanged; this batch adds none.
No executed app draw, selection-frequency measurement, full-corpus
rereview or native-speaker certification is claimed.
This closes batch 24, not the full vocabulary expansion.

## Batch 25: N2:482-N2:501

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 原産, 原始, 研修, 厳重, 謙遜, 県庁, 限度, 現に,
顕微鏡, 原理, 原料, 碁, 恋しい, 請う, 工員, 強引, 公害,
高級, 公共, 工芸.

Twenty new articles bring the collection to 3,735 word articles.
No existing principal article is reused. Four useful reciprocal N2
pairs are added: 県/県庁, 庁/県庁, 恋/恋しい and 芸/工芸.
Every written component remains in metadata, including the ten
primary components without existing kanji cards.

The [batch evidence](n2-vocabulary-batch-sources/batch-25.json)
preserves the twenty raw rows and complete principal families,
307 complete comparison families, 136 actual existing labels and
exclusions, and 35 complete component records. All complete
comparison families and labels were inspected; full existing-card
bodies were captured but only selected bodies were read.
Thirteen qualified public-inspection receipts cover twelve
Daijisen headwords and the actual English Wiktionary 請う tables.
These are author observations, not independent reviewer retrieval.

Source qualifications are explicit: 原産's habitat concerns native
provenance; 原始 selects both origin and primeval senses; 厳重's
firm/strong concerns serious handling or protest; 恋しい's
dear/beloved retains longing. 現に emphasizes actuality,
原理's theory concerns an explanatory foundation, 公共's
society/community concerns public or shared affairs, and 工芸's
industrial arts is not all manufacturing industry.
請う's special こうて/こうた conjugation is positively taught.
Its praying/wishing sense and 高級's high-rank sense are additional,
not separately assigned N2. The latter's quality sense is the
explicit selected source mapping.

The authored snapshot is `c6d44ce4b6dd2e8fceb2fa8ffae7c632ed87e801`.
Its seventeen guarded articles declared 102 direct exclusions.
The blind review derivative removed only the author's quiz rationale.
Both models received the same snapshot, scope, rubric and evidence
access, sequentially and without either initial report.

### Independent initial review and reconciliation

The [GPT initial report](n2-vocabulary-reviews/batch-25-gpt-initial.md)
used `gpt-6.1-sol`; the
[Claude initial report](n2-vocabulary-reviews/batch-25-claude-initial.md)
used `claude-opus-5.5`. Both read all twenty articles, principal
families, mappings, 136 comparison labels and four related kanji changes.
Comparison-family and existing-body review beyond that was selective,
not a complete reread of all 307 families. The isolated GPT process
exited before Claude started; both reported zero edits.

- **GPT25-01 / F1, resolved:** add the shared 請う/拝む begging guard.
- **GPT25-02, resolved:** add 公共/世の中 for the applicable society
  meaning, not merely a shared social topic.
- **F2, resolved by replacement:** scope 請う's particle explanation to
  the request construction and replace the unexplained, unverified
  invited-person/role example with the inspected 許しを請う expression.
  Inviting remains positively taught from JMdict 1592920:1. Daijisen's
  omission does not disprove it or establish that the removed example
  was wrong. Reinspection also caught an over-attribution of inviting
  in the author's first Daijisen receipt; appended correction evidence
  explicitly supersedes that clause without rewriting history.
- **F3, resolved with qualified reasoning:** add 原始/原産 and
  原始/天然. The exposed broad origin answer omits the distinction
  between beginning and native provenance; the inspected primeval,
  unmodified-natural-state use also overlaps the nature answer.
  Shared 原, tags or a substring alone are not the justification,
  nor are these claims of unrestricted Japanese substitution.
- **F4, resolved:** add 高級/一流 for the source-backed quality overlap.
- **F5, resolved:** use positively sourced 生物/せいぶつ in
  顕微鏡's science-example kana. Missing dictionary forms do not prove
  an unlimited ban on every historical or nonstandard reading.
- **F6, lexical-contradiction claim withdrawn; polish applied:**
  the full 故郷 card explicitly recognizes valid ふるさと while teaching
  こきょう as primary. Align the incoming label with that primary
  reading; do not count the original as a lexical error.
- **Claude Optional secure observation, resolved:** add 厳重/押さえる
  for the actual context-free "secure" answer ambiguity. Their Japanese
  constructions differ; the report's unmeasured low-draw-probability
  suggestion is not a reason to leave this direct pair unguarded.

The remaining suggestions stay **optional**: another 原始 beginning
example / 原始的, a 原料/材料 shape-retention tendency, a
恋しい/寂しい comparison and a 公共/個人 contrast link. The existing
meaning coverage and overlap qualifications do not require those
expansions. 工員 datedness is unverified and is not claimed in teaching.
No native-speaker check, executed quiz or selection-frequency study is
claimed.

The correction packet appends nineteen complete family inspections for
seventeen exact forms, preserving ten genuinely new complete families,
fifteen inspected actual labels/full card bodies, and two qualified
public-entry receipts. Original evidence remains unchanged except those
explicit additions. Six direct guards bring the seventeen guarded
articles to 108 declarations. Three prose corrections and the guards
affect seven new word articles; no baseline article, kanji passage,
title, reading, level, mapping or selected/additional sense changes.

**Model-diversity note:** both models independently found the begging
guard. GPT uniquely supplied the society guard. Claude additionally
supplied the particle/example mismatch, two broad-origin guards,
quality guard, science-example reading, and the secure-label observation
under Optional. Its alleged 故郷 contradiction did not survive full-card
inspection. Contributions are compared across every report section,
not by severity labels or counts alone. This sample shows complementary
useful findings and the need for adjudication, not a model ranking.

### Confirmation, authentication and closure

Both original sessions confirmed correction commit
`272330a5b0ba79b56c8d03b7d8600f7ba2ccf32c`, directly following
the authored commit above. The common bounded assignment covered
all seven changed articles, eight necessary unchanged comparison
cards and appended evidence. Each received its own initial report,
the actual patch and equivalent sanitized evidence, not the other
family's report. GPT exited fully before Claude resumed; both
processes exited without file edits.

- [GPT confirmation](n2-vocabulary-reviews/batch-25-gpt-confirmation.md):
  actual `gpt-6.1-sol`; both original findings resolved. All seven
  changed articles and packet additions were CLEAN on all three facets.
  It independently retrieved Kanjipedia 請う and the relevant Daijisen
  請う, 原始 and 公共 bodies.
- [Claude confirmation](n2-vocabulary-reviews/batch-25-claude-confirmation.md):
  actual `claude-opus-5.5`; F1-F5 and the secure guard resolved;
  F6 withdrawn on full-card evidence. All seven changed articles
  and packet additions were CLEAN on all three facets. It independently
  retrieved Kanjipedia 請う and retained its initial Daijisen inspection.

Neither found an actionable regression or consequential unresolved
claim within the revised teaching. Claude's later sourced invite-example
suggestion remains optional. Its two documentation observations receive
append-only closure clarifications: the captured comparison labels are
pre-correction observations, not replacement current headers; and
JMdict 1273510:1 directly glosses public/communal, while society-generally
support comes from the inspected Daijisen 公共 body together with
1373850:1 for 世の中. No exact English society gloss is attributed to
1273510:1. These clarifications do not alter reviewed teaching or the
frozen correction evidence.

Author-executed authentication checked both commits' parents,
stop-cran author/committer identities and required trailers;
committed/current file hashes and unchanged authored passages;
both exact patches and prompt hashes; and both sanitized evidence
derivatives. Removing only the two appended evidence sections
reproduces the authored packet exactly. The ten new complete
comparison families match the pinned extraction, and the six
direct additions match the current headers.

All four archived reports match original output after progress
preambles are removed and Markdown hard breaks are normalized.
Original session IDs and start times, actual model metrics,
zero-edit receipts and cumulative one/two-request counts agree.
Both exact common prompts match the original sessions' recorded
user messages. These are author-executed provenance checks,
not reviewer-executed Git or linguistic certification.

Closed coverage is **500 closed, 0 draft, 1,312 pending and
0 unresolved** rows, mapped to 494 distinct articles: 462 new
and 32 reused. There are 3,735 word articles and 114 distinct
tracked primary-form reciprocal N2 pairs on new articles, plus
checked reused pairs and the prior 包/くるむ alias-reading pair.
All 3,273 baseline identities, readings, titles, written-kanji
arrays and easier sourced levels remain preserved. Prior
baseline exclusion exceptions are unchanged; this batch adds none.
No executed app draw, selection-frequency measurement, full-corpus
rereview or native-speaker certification is claimed.
This closes batch 25, not the full vocabulary expansion.

## Batch 26: N2:502-N2:521

**Status:** closed; both original reviewers confirmed the corrected snapshot.

Scope: 孝行, 交差, 講師, 工事, 公式, 口実, こうして, 校舎,
公衆, 香水, 公正, 功績, 光線, 高層, 構造, 交替, 耕地,
交通機関, 校庭, 肯定.

Nineteen new articles bring the collection to 3,754 word articles.
The existing 肯定 article already teaches affirmation and logical
affirmative; only its sourced N2 level is added. Its identity,
primary reading, title, written-kanji array, exclusions and full body
remain unchanged. Eight new reciprocal N2 pairs are added:
講/講師, 香/香水, 績/功績, 線/光線, 層/高層, 造/構造,
替/交替 and 耕/耕地. The existing 肯/肯定 pair remains linked.
Missing 孝, 舎, 衆 and 功 cards do not remove those characters
from the words' metadata.

The [batch packet](n2-vocabulary-batch-sources/batch-26.json)
preserves all twenty raw source rows and complete principal families,
379 complete comparison families, 143 actual existing labels/exclusions,
38 complete component records and fifteen public-entry inspection
receipts. All extracted comparison families, component records and
labels were inspected. Existing full bodies were captured, but only
selected main bodies and all four supplemental bodies were read.
No 143-card or whole-corpus rereview is claimed.

All fifteen Daijisen receipts refer to complete relevant lexical
containers identified by publisher code, not simplified Wikipedia
content, navigation or copyright footers returned on some initial
lookups. A standard-library parser avoided a new dependency.
Public observations are concise original paraphrases; the full
copyrighted bodies remain private evidence. These receipts describe
author access, not independent reviewer retrieval.

Mappings explicitly qualify broad source glosses: 公式's formality
concerns official/publicly established forms; 構造's construction
concerns how parts are put together; 交替's relief concerns taking
over a role and its rotation can concern duties. 校庭's campus
means outdoor school grounds. 高層's bare upper selects pinned
JMdict sense 2, with building sense 1 additionally taught;
Daijisen's opposite sense order is not transferred to those indices.
講師's school part-time and cram-school uses are additional
senses 3-4. None of these extra meanings receives a separate N2
assignment.

The initial review derivative removes only the author's quiz
rationale. GPT-6.1 Sol (`gpt-6.1-sol`) and Claude Opus 5.5
(`claude-opus-5.5`) reviewed authored commit
`54389ef6c76d3ca5f14c89bc8ad04ee59fe1f9dd`, with the same nineteen
new articles, reused-source coverage claim, eight related kanji changes,
twenty mappings, rubric and evidence access. GPT exited before Claude
started; both processes were blind, read-only and used only the requested
model. Native session records identify the original sessions as
`21aed4b7-e161-408f-918a-46cd26220f79` and
`3b741d6f-54d7-4ed3-9a47-8fc1a6278630`.

Initial reports:
[GPT](n2-vocabulary-reviews/batch-26-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-26-claude-initial.md).
Archives remove progress preambles and normalize Markdown hard breaks,
without rewriting substantive reports. GPT's explicitly rejected
abbreviated-hash typo and immediately stated correct full hash remain
verbatim. Claude's paired-row table covers all nineteen new articles;
its mention of missing 斯 does not make that rare mentioned spelling
part of こうして's kana-only primary metadata.

**Evidence adjudication and content changes**

- **GPT-01, 公衆/一般: resolved in content.** 一般's actual body
  explicitly teaches the general public. The complete Daijisen noun sense
  2(b) positively supports that ordinary public use. Add the direct guard.
  Claude considered and rejected the pair because JMdict/Jisho lacked the
  exact English gloss; that omission does not refute the positive evidence.
- **GPT-02 and Claude F1, こうして/こちら・こっち: resolved in content.**
  Add both direct guards for the unqualified this-way English labels.
  The Japanese manner/direction distinction was already correct.
- **GPT-03, 功績/働き: resolved in content.** The actual card and pinned
  JMdict 1451040:2 teach achievement/performance; inspected Daijisen sense
  2 independently supports work results. Add the direct guard, without
  equating all functioning or effort with meritorious accomplishment.
- **Claude F2, 高層/ビル: resolved in content.** The actual high-rise and
  multistory-building answers overlap the ordinary building meanings.
  Add the direct guard; the bill homograph is not transferred to ビル.
- **Claude Optional, 交差/越える・越す: accepted.** Add two actual
  crossing/cross-over English-label guards. The reason is the exposed
  labels' ambiguity, not mere consistency with the existing 渡る guard,
  spelling or membership in a crossing-related topic.
- **Claude Optional and naturalness limit, 高層: addressed.** Use
  dictionary-attested 高層気流 with kana and an air-current example,
  instead of the unverified 高層の大気 construction. The complete
  Daijisen body positively records the compound; the whole new sentence
  is authored, not a corpus quotation. Do not call the removed construction
  wrong or claim that 高層大気 is common without evidence.
- **Claude Optional, 孝行: editorial polish accepted.** Group noun,
  する and な-modifier uses explicitly and say not merely obedience.
  All three uses were already demonstrated; no missing sense is claimed.
- **Other optionals: not required.** Do not expand 交替 with a transitive
  sports example, 耕地 with another English plantation gloss, or 公式
  with an adverbial example merely to increase coverage. Their selected
  senses remain taught. JMdict's vt/vi status is acknowledged, but its
  spelling-priority tags do not establish measured comparative frequency.

The follow-up extraction contains fifteen complete families for fourteen
exact forms. All 81 compact records and seven actual comparison labels
and bodies were inspected. Nine already-known families compare exactly;
six genuinely new complete families are appended. Three public inspection
receipts cover 一般, 働き and a 高層 reinspection. Original authored
evidence and rationale remain unchanged; additions are separate.

The first private follow-up collector incorrectly retained SGKDJ across
the later NHGKT section on the 働き page. Its extra machine-generated
conjugation container is not lexical evidence. Resetting publisher at
explicit named dictionary-section anchors fixes that attribution.
All fifteen original pages plus the two new pages were retrieved again:
seventeen actual SGKDJ bodies were confirmed, with every original first
lexical body unchanged. The actual Daijisen 働き sense 2, not the
machine-generated container, supports the accepted guard.

**Model-diversity observation:** shared manner/direction catch; GPT-only
accepted 公衆/一般 and 功績/働き hypotheses; Claude-only accepted
高層/ビル, optional crossing-label guards and the attested-compound
improvement. Compare Findings, Optional and Limits together. 孝行 polish
is not a correctness save. This sample supports complementary coverage,
not a general model ranking or a majority-vote method.

Only six newly authored cards change. Seven direct guards bring the
eighteen guarded articles to 96 directional declarations. No baseline
article, kanji, identity, title, reading, level or mapping changes.
### Confirmation, authentication and closure

Both original sessions confirmed correction commit
`9d270cbd0596af1c3259ba13ec23e46dedeef9db`, directly following
the authored commit above. Each received its own report, the actual
six-word-plus-provenance diff and the same sanitized appended evidence.
GPT exited fully before Claude resumed; both processes exited without
file edits. This was a bounded changed-passage confirmation, not another
full-batch or whole-corpus review.

- [GPT confirmation](n2-vocabulary-reviews/batch-26-gpt-confirmation.md):
  actual `gpt-6.1-sol`; all three original findings resolved. All six
  changed articles and inspected packet additions were CLEAN on all
  three facets. It independently retrieved and inspected the actual
  complete Daijisen bodies for 一般, 働き and 高層, including publisher
  boundaries.
- [Claude confirmation](n2-vocabulary-reviews/batch-26-claude-confirmation.md):
  actual `claude-opus-5.5`; F1/F2 resolved, the 公衆/一般 rejection and
  斯 metadata observation withdrawn. All six changed articles were
  CLEAN on all three facets. Its own Daijisen retrieval remained
  unsuccessful, so it expressly leaves those three inspection receipts
  independently UNVERIFIED by itself. Author inspection and GPT's
  actual independent retrieval supply that evidence; agreement is not
  manufactured by relabelling failed source access.

Neither found an actionable regression or consequential unresolved
claim within the retained teaching. 高層's sourced の-modifier status
does not require another example to complete this scope; the additional
construction suggestion remains optional. The newly noted
こちら/こっち pair concerns unchanged baseline cards outside this
correction and is not silently added to either card or counted as an
accepted batch finding. Extra 高層大気, transitive sports usage,
plantation wording and 公式に remain optional. No comparative spelling
frequency assertion is adopted from dictionary priorities alone.

Author-executed authentication checked both commits' parents,
stop-cran author/committer identities and required trailers;
committed/current file hashes and unchanged authored passages;
both exact patches and prompt hashes; and both sanitized evidence
derivatives. Removing only the two appended evidence sections
reproduces the authored packet exactly. The six new complete families
match the pinned extraction and all seven guard additions match the
current headers.

All four archived reports match the original output after progress
preambles are removed and Markdown hard breaks are normalized.
Original session IDs/start times, actual model metrics, zero-edit
receipts and cumulative one/two-request counts agree. Both exact
common prompts match the native sessions' recorded user messages.
These are author-executed provenance checks, not reviewer-executed
Git or linguistic certification.

Closed coverage is **520 closed, 0 draft, 1,292 pending and
0 unresolved** rows, mapped to 514 distinct articles: 481 new
and 33 reused. There are 3,754 word articles and 122 distinct
tracked primary-form reciprocal N2 pairs on new articles, plus
checked reused pairs and the prior 包/くるむ alias-reading pair.
All 3,273 baseline identities, readings, titles, written-kanji
arrays and easier sourced levels remain preserved. Prior baseline
exclusion exceptions are unchanged; this batch adds none.
No executed app draw, selection-frequency measurement, full-corpus
rereview or native-speaker certification is claimed.
This closes batch 26, not the full vocabulary expansion.

## Batch 27: N2:522-N2:541

**Status:** review-closed after sequential independent initial reviews,
evidence-based corrections and two original-session confirmation rounds.

Scope: 高度, 高等, 合同, 後輩, 公表, 鉱物, 公務, 項目,
紅葉, 合理, 交流, 合流, 効力, 超える, コース, コーラス,
焦がす, 国王, 国籍, 国立.

Nineteen new articles bring the filesystem collection to 3,773 word
articles. Source 超える reuses the existing 越える article, which
already teaches the spelling, こえる reading, exceeding construction
and both selected senses. A narrow addition links its alternative
超 component; the primary identity, title, reading, [越] array,
exclusions, full existing teaching and easier N3 level are preserved.
Four new primary-form reciprocal N2 pairs are 鉱/鉱物, 紅/紅葉,
効/効力 and 籍/国籍. The separate 超/越える alias-reading pair
uses a 超える link label and actual こえる reading. Missing 輩,
項 and 焦 remain included in primary written-kanji metadata.

The [source packet](n2-vocabulary-batch-sources/batch-27.json)
preserves all twenty raw rows and complete principal families,
267 distinct complete comparison families, 113 actual existing
labels/exclusions, 29 complete component records and twenty-one
public-entry inspection receipts. All extracted complete comparison
families, components and labels were inspected; captured existing
full bodies were read selectively, not as a 113-card rereview.
Three extractions' overlapping family/label records compare exactly.
Public observations are original concise paraphrases; copyrighted
lexical bodies remain private.

紅葉's raw entry 1578780 and こうよう reading concern autumn
coloring/leaves, but its raw gloss is "(1) (Japanese) maple."
The separately inspected complete family 2857870 supports maple
and foliage under もみじ; that reading is explicitly taught and
mapped as additional senses. The single Daijisen container's several
reading headings are not treated as one unrestricted lexical identity.
Historical compiler intent is not recovered or silently replaced.

Other qualifications preserve raw scope: 合理 is a noun, with
separately sourced 合理的 supplying adjective uses; 合同's joint
and congruence senses are additional to union/combination. コース
explicitly selects route/study senses 1-2 and additionally teaches
individual meal course, full-course meal and offered plan senses
5-7, not every sports/policy/baseball meaning. 国籍's ship/aircraft
national affiliation is additional to personal nationality.
Secondary senses do not receive independent N2 assignments.

At the authored snapshot, fifteen new articles declared 106 directional quiz guards.
They account for actual broad English labels and ordinary secondary
senses, including 皿's serving/course, 焼く's burn, 公立's
broader public category and 国王's positively recorded queen gloss.
Those were author hypotheses, not reviewer findings or an assertion
of unrestricted synonymy. No baseline exclusion is changed.

The blind derivative removes only the author's quiz rationale.
Both model families received the same authored snapshot,
nineteen new articles, reused-source claim, six related content
changes, twenty mappings, rubric and equivalent source access.
The actual models were **gpt-6.1-sol**, then **claude-opus-5.5**.
The GPT process fully exited before Claude started; both were read-only,
undelegated, and recorded zero edits. Their genuine initial reports are
[GPT](n2-vocabulary-reviews/batch-27-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-27-claude-initial.md).
Snapshot/hash assertions were author receipts, not reviewer-executed Git.
GPT checked the 113 labels against files and selected comparison families;
Claude searched, rather than completely reading, the comparison families.
Neither performed a corpus or native-speaker review.

### Initial findings and adjudication

GPT's B27-GPT-01 is **resolved** by a direct 高等/松 guard.
The actual 松 title and teaching, complete JMdict 1349860:2, and
the actual 精選版日本国語大辞典 松/まつ [1]11 support the
highest-of-three ranking. The Daijisen receipt's historical rank
material is not substituted for that modern tier evidence.

Claude's B27-01 is **resolved** by directly explaining 合同 as
merging into one body, replacing the source-facing double negative,
and adding a political-party merger example with kana and English.
The meaning is positively evidenced; the whole sentence is original,
not represented as a corpus quotation.
Claude's B27-02 is **resolved** by direct 公務/務め・勤め guards.
Its tentative 義務 observation is also adopted: the actual broad
duty label and positive position-based duty sense support that pair
independently, not by transitivity. Substantive comparisons are linked.

All optional observations are explicitly disposed in the appended
correction evidence. Four 高度/高等 guards against 立派 and 偉い
are removed: admiration, importance, or prestige alone is insufficient.
Good/excellent/superior labels remain protected on the positive
high-grade/high-class quality sense, not on every advanced use.
コース/選択・予定 remain protected by its explicit option/plan/program
senses and the actual broad choice/plans labels, not unrestricted
Japanese substitution. The two "An 項目" articles are editorially
changed to "A 項目". 合理/訳 gains a direct guard and qualified
comparison, positively supported by 訳 1538330:3 good sense/reason.
国籍/市民 is not guarded: a nationality is not a citizen-person.

Not expanded: 国立's noun-compatible short title, an extra もみじ
foliage example, or the preexisting unlinked 越す mention. The two
expressly unverified modern-collocation preferences for 合理 and
効力 are not adopted without positive evidence of an error or a
necessary replacement. Actual lexical entries recognize the nouns;
the historical 合理 example does not establish a modern adjective.
No comparative frequency or whole-sentence certification is claimed.

Follow-up evidence contains 24 complete families for seventeen forms,
sixteen actual labels, and eight qualified public-entry receipts.
Eighteen family overlaps compare exactly; only six genuinely new
families are appended. Original rows, families, labels, receipts and
rationale remain unchanged. The correction derivative again removes
only initial quiz rationale. At the first correction, sixteen new articles declared
**107 directional guards**: five additions and four removals.
Six new articles change; no baseline word, kanji, primary title,
reading, level, source mapping or reciprocal pair changes.

### Model-diversity observation

Across the entire reports, including Optional and Limits, GPT uniquely
identified 高等/松; Claude uniquely identified merger clarity and
the public-duty guards, and supplied the useful tentative 合理/訳,
guard-pruning and English-article observations. No duplicated actionable
finding was identified. Other preferences remain optional or unsupported
as defects. This is useful complementary evidence on this batch, not a
model ranking or a claim that either model reviewed every comparison.
### First confirmations and bounded follow-through

Both original sessions were resumed sequentially on correction
`ac74524ac2d47d12c0b2caf8bd430f47f9ab580b`, with their own reports,
the same actual six-card/provenance diff, rubric and sanitized evidence.
The [GPT confirmation](n2-vocabulary-reviews/batch-27-gpt-confirmation.md)
resolved its original finding and found no actionable regression.
The [Claude confirmation](n2-vocabulary-reviews/batch-27-claude-confirmation.md)
resolved both original findings but identified **B27-03**, a missed
公務/役 duty-label pair. This predates the correction, not a regression.
Claude also raised 役割 tentatively. Both processes fully exited with
zero edits.

Positive complete-family and actual-card inspection supports those two
pairs independently: 役 1537970:1 explicitly records duty/assignment,
and 役割 1538000:1 records duties. A bounded duty/responsibility-title
sweep also established 係/公務 and 責任/公務: 係's actual answer
includes assigned duty and 1589840:1 explicitly supports that task
sense, while 責任 1383180:1 and its body positively teach duty/
responsibility, not only blame. The person-in-charge sense alone
would not justify a task-word guard. All four receive direct guards
and qualified links in 公務, not transitive protection through other
duty words.

The follow-through appends six complete families for four forms,
four actual labels and explicit dispositions; all thirty compact
family records and all four full card bodies were read. Historical
えき/えだち and suffix がかり identities are not transferred to
primary やく/かかり cards. Initial correction evidence remains intact.
There are now **111 directional declarations** on sixteen new cards.
Only 公務 and appended provenance change in this follow-through.
No baseline word, primary mapping, easier level, kanji or reciprocal
pair changes.

This additional pass was useful: Claude exposed a first-review miss,
its tentative role/duties observation gained positive support, and
the author's bounded class-level sweep found two more task-label
overlaps. Neither report's original CLEAN verdict is treated as
exhaustive certification.

### Final bounded confirmations and closure

Both original reviewers resumed sequentially on
`c98832d1bc9f30ea040829e23a1fe79d8db85f7e`, after the six-card
correction at `ac74524ac2d47d12c0b2caf8bd430f47f9ab580b`.
The [GPT follow-through](n2-vocabulary-reviews/batch-27-gpt-followup.md)
and [Claude follow-through](n2-vocabulary-reviews/batch-27-claude-followup.md)
report CLEAN correctness, scoped coverage and comprehensibility for
the single changed 公務 passage and appended evidence. B27-03 and
the four direct duty-label pairs are resolved; no actionable defect
or consequential unresolved claim remains in scope. These are bounded
confirmations, not renewed whole-batch reviews.

GPT read all six appended families and four comparison cards. Claude
read the patch and cards, spot-checked bounded derivative sections,
performed its own title sweep and retrieved selected Jisho entries.
Its suggested closing scope sentence remains optional: 公務's Meaning
section already defines the public/official boundary, and each comparison
is qualified. No content change is needed. Claude could not reconcile
the author's "thirty readable records" count. That count is thirty
nonempty lines in the private rendering: six ENTRY headings, six spelling
arrays, six reading arrays and twelve sense lines, not thirty lexical
senses. This reporting-unit clarification does not change source data;
the genuine report and historical evidence remain unchanged.

Author-executed authentication checked the authored
`84a79c01fe6b2b669652802823ca0fc09c25fe98` and both correction
commits, their parent chain, stop-cran identities, trailers, committed
file hashes, actual patches, common prompts and all three derivatives.
It verified append-only preservation of original and first-correction
evidence, both six-family additions against complete extraction outputs,
nine direct additions, four removals and the final 111 declarations.
Each original native session contains exactly the three expected common
requests with the actual model and start time, zero edits, and final
assistant text matching its genuine archive after disclosed preamble/
Markdown normalization. These checks were executed by the author, not
by the file-only reviewers.

Dual-family review was complementary on this batch, including Claude's
late duty-label catch and independent follow-through. GPT acknowledged
its earlier missed gaps. Neither convergence nor the author's provenance
checks establish exhaustive dictionary coverage or native-speaker/
corpus certification. 紅葉's unrecovered historical compiler intent
remains explicitly qualified and nonblocking, rather than silently
asserted resolved.

Closure checks preserve all 3,273 baseline identities, readings, titles,
kanji arrays and easier levels, with only previously documented earlier
batch exclusion exceptions. The 3,773-word collection retains all
tracked reciprocal N2 links, including 126 distinct primary-form pairs
on new articles. Structural validation, coverage/preservation audit,
deterministic manifest regeneration and whitespace checks passed.

Current index: **540 closed, 0 draft, 1,272 pending and 0 unresolved**
rows, mapped to 534 distinct articles: 500 new and 34 reused.
This closes batch 27, not the full vocabulary expansion.

## Final verification

Not started. Final closure requires all original rows accounted for, no consequential unresolved
claims, independent review coverage of every addition and changed passage, baseline preservation,
source/reading/sense and cross-reference audits, a deterministic manifest, and `stop-cran` authorship.
## Batch 28: N2:542-N2:561

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: ごくろうさま, 焦げる, 凍える, 心当たり, 心得る,
腰掛け, 腰掛ける, 五十音, 胡椒, こしらえる, 超す, 擦る,
個体, 御馳走, ごちそうさま, こちらこそ, 小遣い, コック,
こっそり, 古典.

Seventeen new articles bring the filesystem collection to 3,790 word
articles. Three source rows reuse stable articles: 超す is actually
taught at 越す with a quantity example and difficult-obstacle account;
御馳走 is already taught at ごちそう; こっそり gains only its sourced
N2 level. The first two retain easier N3/N4 levels, primary identity,
title, reading and written-kanji arrays. Existing exclusions, images
and scene bytes remain unchanged. Four new primary reciprocal N2 pairs
are 凍/凍える, 腰/腰掛け, 腰/腰掛ける and 個/個体.
The separate 超/越す alias pair uses the actual 超す/こす label.

The [source packet](n2-vocabulary-batch-sources/batch-28.json) preserves
all twenty raw rows, complete principal families, 102 distinct complete
comparison families, 64 actual existing labels/exclusions, 27 complete
component records and twenty public-entry receipts. Nineteen receipts
are actual positive lexical containers; the こちらこそ lookup failed
to yield a lexical body. Complete JMdict evidence positively establishes
that expression. All complete family renderings, component records and
labels were inspected; existing full bodies were read selectively,
not as a 64-card rereview. Public observations are concise original
paraphrases, not copied lexical bodies.

Source mismatches remain explicit. The 擦る row keeps こする and
1298910, but match-striking/chafing/filing/frosting is additionally
taught at する under 1595910:1. コック retains primary cook entry
1050310 and adds valve entry 2862559:1; Dutch and English origins do
not become one identity. ごちそうさま's raw "feast" remains intact
but is not assigned as an interjection's grammatical function.
Search-only forms are not promoted, こづかい preserves づ, and
missing primary characters remain in metadata.

Practical qualifications distinguish intense bodily 凍える from
literal freezing, lead-based 心当たり from creative proposals,
knowing skills from a guarantee of expert mastery, and classics from
any physically old book. The traditional 五十音 arrangement is not
an exact fifty-character modern inventory. Additional senses are
indexed without independent N2 assignments.

At the authored snapshot, fourteen new cards declare sixty directional
quiz exclusions, based on actual labels and ordinary meanings, not
topic cliques, homophones or transitivity alone. Those are author
hypotheses for assessment. The blind initial derivative removes only
the author's quiz rationale. Both families will receive the same
snapshot, seventeen new articles, three reuse claims, seven related
content edits, twenty mappings, rubric and equivalent source access.

### Initial review and reconciliation

The authored commit is `1347683020fb124c01d8279169a855e60b33ab10`.
[GPT-6.1 Sol](n2-vocabulary-reviews/batch-28-gpt-initial.md)
(`gpt-6.1-sol`) and
[Claude Opus 5.5](n2-vocabulary-reviews/batch-28-claude-initial.md)
(`claude-opus-5.5`) reviewed it in separate sequential read-only
processes. Each exited before the next began and recorded zero edits.
Initial prompts, scope and source access were equivalent and blind;
neither family received the other report or initial author quiz rationale.
Git identity and hashes were author-attested rather than independently
executed by either file-only reviewer.

GPT established two supported defects: missing direct
腰掛ける/掛ける protection despite 掛ける's ordinary seating sense,
and missing navigation from both explained 様 suffixes to its card.
Both are corrected without changing baseline exclusions or kana-primary
metadata.

Claude established that the claimed building selection of こしらえる
lacked a concrete building construction. 家をこしらえる now supplies
one, with kana and English, grounded in the previously inspected
Daijisen entry. Its related spelling observations exposed a more useful
source mapping: source 超す now selects quantity sense 1175300:4,
the actual 超しました example, rather than attributing 越す crossing,
hardship or time uses to that spelling. Those and moving remain indexed
as additional 1,2,3,5 under 越す. Raw source fields, stable identity
and easier N3 level are preserved. Standard spelling guidance replaces
ambiguous preference language without claiming that JMdict explicitly
restricts these senses or that every nonstandard spelling is impossible.

Claude's optional observations also prompted six supported direct pairs:
こしらえる/備える, 心得る/マスター, 心得る/詳しい,
心当たり/勘, 個体/生物, and independently 個体/生き物.
Actual labels and complete positive families, not an exclusion clique,
support them. Qualified comparisons preserve provision versus making,
knowledge versus guaranteed mastery, leads versus intuition, and
individual entities versus living things. Fourteen new cards now
declare **67 directional exclusions**, up from sixty; none is added
to a baseline article.

No 焦げる/じりじり guard is established merely by "scorching":
the latter's complete relevant sense describes the sun's manner, not
becoming charred. コック/料理 remains a person/activity distinction;
擦る/掻く is not inferred from shared surface contact. The existing
formal qualification of 心得ました and the practical selected scope
remain; no optional regard-as expansion is needed. "Tap valve" is
retained as readable equipment terminology, and the cited こしらえる
senses already agree with its mapping. Preexisting unlinked mentions
on unchanged 越 are outside this edit.

The correction appends follow-up evidence and preserves the original
N2:552 mapping explicitly alongside its correction. Eleven complete
comparison families for ten forms and all ten actual comparison bodies
were inspected. Existing family overlaps compare exactly; only genuinely
new families are appended. The original authored packet and sanitized
derivative remain frozen. Both original reviewer sessions will receive
the same eight-article correction scope, actual diff and common evidence
for bounded confirmation, not a second full-batch review.

### Confirmation and provenance follow-through

Both original sessions reviewed correction
`f97be4e9b16d7aba1282551c4afe9610a21806f7` sequentially with zero
edits. The [GPT confirmation](n2-vocabulary-reviews/batch-28-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-28-claude-confirmation.md)
accepted all eight article corrections, the revised sense selection
and all seven added direct pairs. Both independently caught the same
new minor provenance error: the N2:552 note claimed an audience-related
raw gloss, while the exact frozen field is `to cross,to pass,to tide over`.

The current note and corrected-record copy now name that exact field.
The original record remains intact; the previous corrected note is
retained in appended follow-through evidence and the frozen correction
snapshot. No article, source field, sense selection, exclusion or
reciprocal link changes in this follow-through. The snapshot's coverage
index hash follows the corrected TSV. Both original sessions will
receive the same provenance-only diff and evidence for a final bounded
check; unrelated baseline prose and optional polish remain outside scope.

### Closure

The [GPT follow-through](n2-vocabulary-reviews/batch-28-gpt-followup.md)
and [Claude follow-through](n2-vocabulary-reviews/batch-28-claude-followup.md)
examined `77294a7957b94d1102e421fb5cfca231431abb0a` in the original
sessions, sequentially and with zero edits. Both resolve the provenance
finding and report CLEAN correctness, scoped coverage and comprehensibility
for the changed note, preserved records and appended evidence. Previously
accepted article verdicts carry over; these are not renewed whole-batch
reviews. No actionable defect or consequential unresolved claim remains
in the assigned scope.

Claude's suggestion that "does not explicitly name" would be more
precise than "does not describe" remains optional: English "pass" can
extend to exceeding, but the exact raw gloss and selected Japanese
quantity use are separately stated. No source field or mapping is
misrepresented by the conservative qualification. The unchanged baseline
article's other source-list reference and tap/valve polish remain outside
this correction.

Author-executed authentication checked all three commits and their
parent chain, stop-cran author/committer identities, required trailers,
committed file hashes, exact actual patches, common prompts and all
three sanitized evidence derivatives. It verified the explicit N2:552
mapping and provenance-note transformations against their preserved
records, unchanged remaining evidence, eleven newly extracted complete
families, seven direct guard additions and the final 67 declarations.
Each original native session contains exactly the three expected
requests with the actual model/start time, zero edits and final
assistant text matching the genuine archives after disclosed
preamble/Markdown normalization. These are author-executed checks,
not Git or hash execution by the file-only reviewers.

Dual-family review was useful on this batch. Comparing observations
throughout both initial reports, GPT uniquely established the ordinary
secondary seating collision and missing 様 navigation. Claude uniquely
established the concrete building-teaching gap and source-spelling
mapping/boundary problem. Its optional hypotheses prompted additional
supported guards after inspection; 個体/生き物 was independently
added by the author's bounded comparison follow-through, not inferred
transitively from 生物. Both confirmations independently caught the
same inaccurate provenance sentence. Some initial CLEAN judgments were
therefore incomplete; GPT explicitly withdrew the former source-sense
approval. These complementary observations concern this shared sample,
not a model ranking or proof against model bias.

Both initial reviewers read all assigned articles and twenty mappings,
but their dictionary/component reading and independent retrieval were
not exhaustive or identical. The original failed public こちらこそ
lookup remains disclosed, with positive pinned JMdict evidence.
Convergence does not establish native-speaker, corpus or app-draw
certification, nor an official modern JLPT syllabus.

Closure preserves the 3,273 baseline identities, readings, titles,
kanji arrays and easier sourced levels, with previously documented
earlier-batch exclusion exceptions unchanged. The collection has
3,790 word articles, including 517 new mapped articles, and retains
130 distinct tracked primary reciprocal N2 pairs. The four new
primary pairs and separate 超 alias link remain useful actual-reading
examples.

Current index: **560 closed, 0 draft, 1,252 pending and 0 unresolved**
rows, mapped to 554 distinct articles: 517 new and 37 reused.
This closes batch 28, not the full vocabulary expansion.

## Batch 29: N2:562-N2:581

**Status:** closed; both original reviewers confirmed the supported corrections and narrow follow-through.

Scope: 琴, 言付ける, 言葉遣い, こないだ, 御無沙汰, こぼす,
零れる, ゴム, ごめん, ごめんください, 小指, こらえる, 娯楽,
御覧, コレクション, 転がす, 転がる, 紺, コンクール,
コンクリート.

Twenty standalone additions bring the filesystem collection to 3,810
word articles. No reused principal articles are claimed. Source 御免
is explicitly taught in kana-primary ごめん; its metadata remains
empty while the recognized spelling substantively links 御.
All written primary characters remain metadata even without cards.
One new primary reciprocal N2 pair, 零/零れる at こぼれる, is added.
The separate alias 零す/こぼす links the kana-primary article without
being counted as another primary pair.

The source packet preserves all twenty exact raw rows and complete
principal families, complete comparison families from 77-form and
ten-form extractions, 66 actual existing labels/exclusions, 36 complete
component records and 23 successful actual public lexical containers.
Complete family renderings, all captured comparison bodies and
supplemental bodies, component records, labels and public containers
were inspected. This is not a renewed full linguistic review of every
baseline comparison article. Public observations are concise original
paraphrases; full lexical bodies remain private.

Source qualifications are explicit. 琴/こと is taught as a zither
rather than an upright Western harp; そう and the Chinese zheng sense
are not transferred from 箏/筝 to 琴. コレクション's raw correction
gloss has positive support under Daijisen's separate English-derived
homograph, not as another current JMdict1051540 sense. That external
recognition has its own heading/URL/hash receipt without a fabricated
JMdict identity or independent level. Only fashion is mapped to
additional 1051540:2.

Practical contrasts retain づ in ことづける and ことばづかい,
intermediary message delivery, the contact-specific 御無沙汰 greeting,
transitive/intransitive spilling, and the tipped-cup versus overflowing
distinction. ゴム's material/eraser uses do not import every English
gum meaning. 小指 includes the little toe; こらえる distinguishes
enduring, restraining and forgiving. 御覧's actual constructions and
social direction are separated, not made universally formal by its
origin. 転がる is godan, and its resulting-position use need not
describe continued movement. 紺 takes の rather than an invented
い-adjective; コンクリート is the material, not abstract 具体.

Seventeen new cards declare 72 directional quiz exclusions, based on
direct ordinary-meaning and actual-label checks rather than topic
cliques or transitivity alone. No baseline exclusion is changed.
These declarations are author hypotheses for independent assessment.
The blind initial evidence derivative removes only the author's quiz
rationale. Both families receive the same frozen snapshot, twenty
new articles and mappings, narrow 零 diff, rubric and equivalent
source access, in separate sequential processes.

### Independent initial reviews and reconciliation

The authored snapshot is
`abb39bbd85d529380cb2506b9ca7f3c2df59c8b3`.
The [GPT initial report](n2-vocabulary-reviews/batch-29-gpt-initial.md)
used `gpt-6.1-sol`; the
[Claude initial report](n2-vocabulary-reviews/batch-29-claude-initial.md)
used `claude-opus-5.5`. Both read all twenty articles, all mappings and
the narrow 零 edit. GPT reports reading all 66 existing comparison
bodies; Claude inspected actual neighbouring cards and spot-checked
the complete comparison families. Each disclosed public-source and
file-only Git/hash limits. GPT exited before Claude began; both
processes reported zero edits.

- **B29-GPT-03 / B29-CL-01, resolved:** replace the unsupported
  older-character claim about 筝 with variant. The missing JMdict
  age flag does not disprove chronology, and the Chinese
  simplified/traditional relation does not prove Japanese ordering.
- **B29-GPT-01, resolved:** add 転がす/裏返す for positive
  tipping/turn-over meaning and the actual broad English label.
- **B29-GPT-02, resolved:** add 転がる/返る for roll-over/turn-over
  label ambiguity, not through a chain of other guards.
- **B29-CL-02, resolved:** add 琴/楽器 for a real instrument and
  the broad musical-instrument answer.
- **B29-CL-03, resolved:** independently guard こないだ against
  近頃 and このごろ; preserve occasion versus current-tendency use.
- **B29-CL-04, resolved:** add 言付ける/任せる for positive
  entrusting senses and actual labels, without equating general
  responsibility with onward delivery.
- **B29-CL-05, resolved:** independently guard ごめん against both
  waiting-apology formulas. Its optional あいにく candidate is also
  accepted for the underqualified sorry/refusal versus sorry-but
  fragments; the added comparison preserves circumstance framing
  versus general apology and direct rejection.
- **Claude Optional / Limits, resolved by replacement:** use the
  short familiar visiting formula actually attested in Daijisen's
  御免 heading instead of the invented mixed-register greeting.
  This removes the need to establish that sentence's naturalness,
  not proof that it is impossible. Link existing 弾く substantively
  at its actual ひく reading in 琴.

The optional 御無沙汰/久しぶり guard is not established from
shared greeting context alone: their actual labels retain
not-having-been-in-touch versus first-time-in-a-long-while meanings.
The body already explains the contact-specific difference.
此間 spelling recognition and technical 琴/箏 taxonomy remain
optional expansions. N2:573 already names the same principal entry
and correctly limits distinct こたえる to 堪える; distinct reading
does not assert a separate entry.

The correction appends twelve complete follow-up family inspections
for eleven forms, only genuinely new families, and all eleven actual
labels/full-body inspections. Original source mappings, evidence and
initial guard declarations remain historical records; the current
eighteen guarded cards / 81 declarations are recorded separately.
Nine direct additions and narrow teaching/link changes affect six
new articles. No baseline card/exclusion, title, level, reading,
selected/additional sense, primary metadata or kanji passage changes.
Source 御免 is an explicitly taught alias at kana-primary ごめん;
its primary array remains empty, not an invented primary 免.

**Model-diversity note:** both families independently identified
the unsupported variant chronology. GPT uniquely supplied the two
rolling/reversal guards. Claude supplied the instrument, recent-time,
entrusting and waiting-apology guards, the optional sorry-but
candidate, and the greeting-naturalness/link observations. The
optional greeting-context guard did not establish a defect.
Contributions are compared across Findings, Optional and Limits,
not only headline findings or severity. This sample shows
complementarity and the continuing need for evidence-based
adjudication, not a model ranking.

### Corrected-passage confirmation and narrow follow-through

The corrected snapshot is
`790d3d1cd94e28f1a06c2aa55ec7d5eea8c8693b`.
The [GPT confirmation](n2-vocabulary-reviews/batch-29-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-29-claude-confirmation.md)
resumed their own original sessions, sequentially, on the same actual
six-article correction diff and equivalent evidence. Both resolved
their original findings and found no correction-induced regression.
GPT independently retrieved the actual Daijisen greeting body.
Claude relied on its earlier actual retrieval and the original-body
reinspection receipt. Both reported zero edits and bounded file-only
Git/hash limits.

**B29-CL-06, resolved and confirmed:**
Claude identified the missing direct ごめん/恐縮 exclusion as an
initial-review miss, not a regression. The author read both actual
full cards and the complete pinned 1236740 family. Sense 2 explicitly
records feeling sorry for troubling someone, often before a request
with ～ですが; the existing body teaches that construction. This
supports protection against the actual sorry/apologetic labels, not
unrestricted substitution. Add one direct guard and a qualified
linked comparison separating courteous requests and gratitude from
the familiar apology and ～はごめんだ refusal.

The complete 申し訳 family and actual body were also inspected.
Its noun title, apology/excuse, is explicitly distinguished from the
complete negative apology formulas. Shared context and inconsistent
older third-card guards do not establish a necessary bare-noun pair
with ごめん; that candidate remains optional. Cross-transitivity
reversal pairs, 届ける/言付ける and inside-out wording polish likewise
established no further defect.

Two exact complete pinned comparison families were extracted with
both source hashes checked. New evidence and current declarations
are appended under confirmation follow-through without overwriting
the original packet or the first correction. Eighteen cards now
declare 82 directional exclusions, one more than the first correction.
Only ごめん changes in this follow-through; no baseline exclusion,
identity, title, reading, level, mapping, kanji or reciprocal example
changes. The new finding is another useful Claude contribution in
this sample, while also demonstrating that an initial CLEAN report
does not imply exhaustive semantic or quiz coverage.

### Final confirmation and closure

The follow-through snapshot is
`a2ce2462ad5b3f10cc9e10710eccbf9ff1a06c80`.
The [GPT follow-through](n2-vocabulary-reviews/batch-29-gpt-followup.md)
and [Claude follow-through](n2-vocabulary-reviews/batch-29-claude-followup.md)
resumed the same original sessions, one process at a time. Both read
the complete changed ごめん article, actual 恐縮 and 申し訳 bodies,
three complete relevant families and the actual narrow diff. Both
confirmed the direct guard and qualified comparison, retained their
earlier resolutions, accepted 申し訳 as optional and reported no
new actionable defect or consequential unresolved claim in scope.
Both returned CLEAN for correctness, scoped coverage and
comprehensibility of the changed card and appended evidence.

The author authenticated all six final reports and exact common
prompts against the two native sessions, actual model usage and
zero-edit receipts. The three commits' parent chain, stop-cran author
and committer identities, trailers, normalized file hashes, actual
patches and equivalent evidence derivatives were checked. Original
evidence is preserved exactly; eleven first-correction and two
follow-through complete comparison families are appended. The
current 18-card / 82-declaration headers match the historical 72,
then nine and one direct additions.

The narrow reviewer patches deliberately contain article and source
evidence changes, not the generated manifest diff. File-only
reviewers could not execute Git or hash checks. The author separately
verified the actual committed manifest hash and regenerated it
deterministically; this does not become reviewer-executed verification.
No app draws, corpus-frequency measurement, native-speaker
certification or official modern JLPT syllabus coverage is claimed.
The two sessions have exited. No specifically named existing
reviewer temporary artifacts were found in their tool-result scan;
no broad temporary-directory cleanup was performed.

Closure brings the pinned community-list coverage to **580 closed /
0 draft / 1,232 pending / 0 unresolved**, mapped to 574 distinct
articles: 537 new and 37 reused. There are 3,810 word articles and
131 distinct tracked primary reciprocal N2 pairs. The remaining
list is not claimed complete.

**Final diversity assessment:** the shared chronology catch and
different supported guards remain complementary in this sample.
Claude's confirmation supplied one additional initially missed
ordinary-secondary-meaning pair, which GPT also confirmed against
the pinned evidence. Optional observations were compared across
whole reports and not credited as unique solely by section labels.
This is evidence for using both families and reconciling their
claims, not a benchmark or a guarantee against further misses.

## Batch 30: N2:582-N2:601

**Status:** closed after sequential independent reviews and confirmations.

Scope: 混合, コンセント, 献立, こんばんは, サークル, 在学, 再三,
祭日, 催促, 採点, 災難, 裁縫, 材木, サイレン, 逆さ, 逆様,
捜す, 遡る, 酒場, さきおととい.

Nineteen standalone additions bring the collection to 3,829 word
articles. Exact existing 捜す is reused with only sourced `jlpt: 2`
added; its body, title, reading and guards remain. The separate
探す article retains N4. Source 逆様 is explicitly taught at
primary 逆さま, with the rare source spelling and actual whole-word
reading preserved. Kana-primary こんばんは and さきおととい
teach their kanji spellings without inventing primary metadata.

Six N2 kanji cards receive useful linked examples and citations:
混, 再, 祭, 採, 材 and 逆. Seven newly tracked primary reciprocal
pairs bring the distinct total to 138; 逆 has both 逆さ and 逆さま.
The existing 捜/捜す backlink needs no change. Missing 献, 催,
促, 災, 裁, 縫 and 遡 remain written-primary metadata where
applicable; no new kanji/stroke cards are fabricated.

The [source packet](n2-vocabulary-batch-sources/batch-30.json)
retains twenty exact raw rows and complete principal families,
157 distinct complete comparison families from four extractions,
101 actual existing labels/exclusions, 35 complete component
records and 22 actual public lexical containers. Complete family
renderings and captured comparison bodies were inspected through
their boundaries. Public observations are original concise
paraphrases, not copied full dictionary bodies. This does not
claim a renewed full linguistic review of every baseline card.

コンセント's source consent gloss has positive support under a
separate Daijisen heading and in the informed-consent expression.
It is not an extra current JMdict1052330 sense. The raw concentric
gloss is retained and distinguished from that electrical entry's
loan-source fragment. 採点's assigned-score recognition likewise
has positive external support without an invented current sense
number. サイレン does not deny separately attested mythological
homographs merely because its principal entry is short.

Practical teaching distinguishes on-first mixed 献立 from two
on readings, greeting は pronounced わ, enrollment state from
entry/commuting, repeated 再三 from exactly three occurrences,
festival days from events without inventing a strict 祝日 split,
pressing for action from every initial request, and sewing from
its individual tools. 材木/木材 keep their actual reversed readings.
逆さ/逆さま cover orientation and order. 遡る retains intransitive
grammar despite route を and retroactive English wording.
さきおととい explicitly counts three days before today.

Sixteen new cards declare 71 directional quiz exclusions, based
on direct ordinary-meaning and actual-label checks. Existing
baseline guards remain unchanged. These are author judgments for
independent assessment, not reviewer conclusions. Both families
will receive the same frozen snapshot, nineteen articles, reused
source claim, seven related diffs, rubric and source access in
sequential processes. Their evidence derivative removes only the
author's quiz-guard rationale.

Coverage is **580 closed / 20 draft / 1,212 pending / 0 unresolved**,
mapped to 594 distinct articles: 556 new and 38 reused. The batch
and remaining list are not yet claimed review-closed.

### Initial independent reviews and reconciliation

Both reviewers assessed authored snapshot
`787b93e13814f9f2052f641645fad70e6962007d`, parent
`6c66db7f90abc63b28fa7aa376eb78fe12a189ce`, using the same
nineteen-article scope, exact reuse claim, related seven-file
patch, twenty mappings, rubric and blind evidence derivative.
The derivative removes only `quizGuardRationale`. The processes
ran sequentially and exited with zero reported edits.

- GPT: **gpt-6.1-sol**, native session
  `44ae0271-abe5-4d69-a57c-8077da760781`; [initial report](n2-vocabulary-reviews/batch-30-gpt-initial.md).
- Claude: **claude-opus-5.5**, native session
  `8129cdc0-cd08-4d6a-9488-dd254f642c4d`; [initial report](n2-vocabulary-reviews/batch-30-claude-initial.md).

GPT established a missing direct 献立/計 and 献立/プラン
quiz guard. Claude questioned the air-mixture example and
requested usable context for 献立's nonmeal sense. GPT had already
made the equivalent nonmeal-example observation under Optional;
it is shared, not a Claude-unique discovery. Claude's optional
サイレン/合図 signal hypothesis was followed through against actual
labels and the emitted-sound use, rather than accepted from a
shared topic alone.

| Observation | Disposition |
| --- | --- |
| G30-01: 献立 planning labels | Resolved: add direct 計 and プラン guards for applicable planning senses and actual broad plan labels. |
| B30-C2 and GPT Optional: nonmeal 献立 | Resolved: explain planning/preparation/arrangements and give the attested meeting construction, reading and English. |
| B30-C1: air mixture wording | Replaced with 混合物 and explained the compound. Its positive dictionary support does not prove the former sentence impossible; the original naturalness criticism remains medium-confidence. |
| Claude Optional: サイレン/合図 | Resolved after bounded follow-through: add 合図 and independently 信号 guards for broad signal labels versus the actual emitted-sound use; retain device/sound and broader-signal distinctions. |
| Claude Optional: festival/day and greeting/evening labels | No actionable collision established: actual labels preserve event/day and greeting/time distinctions. Shared characters or an older unrelated guard do not prove these pairs. |
| Claude Optional: another mixing example, sports, 倒 spelling and an extra reading-row placement | Optional expansion; existing selected source coverage, grammar and reciprocal links remain. |

Five complete additional families for four exact comparison forms
were extracted with both pinned dictionary hashes verified; full
compact records and seven actual comparison bodies were inspected.
The unrelated 計/はか family is retained but not used as evidence
for 計/けい. Four further public lexical containers were retrieved
and inspected through their relevant bodies: 混合, 献立, 計 and
プラン. The noun 計 heading is distinguished from its character
heading. Full public bodies stay private; the public appendix
records concise observations, URLs and response hashes.

Only 混合, 献立 and サイレン change. Four direct guard additions
bring seventeen guarded new cards to 75 directional declarations.
No baseline card, title, primary reading, identity, level, mapping,
selected/additional sense or kanji passage changes. Initial
evidence is preserved exactly and corrections are appended;
current guard declarations are recorded separately from the
historical initial declarations.

**Preliminary diversity assessment:** GPT uniquely supplied the
supported plan-label guards; the nonmeal teaching observation is
shared across report sections. Claude supplied the separately
useful substance-wording concern and tentative signal comparison,
which produced a bounded supported improvement after investigation.
Neither report nor source receipt establishes exhaustive
naturalness, measured frequency, native certification or executed
app behavior. GPT independently retrieved relevant public bodies;
Claude disclosed failed/irrelevant retrievals and did not claim
independent verification of the consent or other external headings.
Both disclosed that file tools cannot independently authenticate
Git or hashes. Confirmation of the changed passages is pending;
the twenty source rows remain draft.

### First confirmation and bounded follow-through

Both original sessions resumed separately on corrected
`6f731b2640fa2752c6bbbf9f11e62515727eb9d3`, with their own
original report, the same actual three-article/evidence diff and
the same equivalent derivative. Both returned CLEAN for the three
changed articles and appended evidence and reported zero edits:
[GPT confirmation](n2-vocabulary-reviews/batch-30-gpt-confirmation.md),
[Claude confirmation](n2-vocabulary-reviews/batch-30-claude-confirmation.md).
The first findings are resolved; Claude explicitly accepted that
the air-example criticism was naturalness preference rather than
established ungrammaticality. Its greeting/time and festival/day
collision hypotheses were withdrawn.

Claude's confirmation also disclosed additional optional
planning/preparation and signal labels. Different leading glosses
do not establish uniqueness when a displayed trailing meaning is
applicable. Bounded inspection of all six actual comparison cards
and seven complete families supported five direct 献立 pairs:
打ち合わせ, 設計, 準備, 用意 and 支度; and one independent
サイレン/サイン pair for its ordinary secondary signal use.
The unrelated mathematical サイン family is not signal evidence.
Original and first-correction evidence remains exact; follow-through
is appended separately.

Two articles receive those six guards and substantive linked
comparisons preserving design/discussion/getting-ready and
signature/signal distinctions. 献立's Daijisen link label now
acknowledges both meal and broader planning uses. Seventeen new
cards now declare 81 directional exclusions. No baseline card,
primary identity, title, reading, level, mapping, selected/additional
sense or kanji passage changes. Confirmation of this bounded
follow-through remains pending; rows are still draft.

### Final confirmation and closure

The final follow-through snapshot is
`c8eb5d54473f157441bef875774b22b47ae50048`.
The [GPT follow-through](n2-vocabulary-reviews/batch-30-gpt-followup.md)
and [Claude follow-through](n2-vocabulary-reviews/batch-30-claude-followup.md)
resumed the original sessions sequentially. Both read the two
complete changed articles, six actual comparison bodies, seven
complete follow-through families and the actual narrow diff.
Both confirmed all six additional direct guards and linked
distinctions, retained their earlier resolutions and returned
CLEAN for correctness, scoped coverage and comprehensibility of
the changed articles and appended evidence. No actionable defect
or consequential unresolved claim remains in that bounded scope.

Claude revised its earlier optional planning/preparation judgment
after considering the article's positively supported nonmeal
teaching and all displayed meanings. Its suggestions for further
signal examples and formal-plan phrasing remain optional polish;
the pre-existing unguarded comparison between two unchanged
baseline signal cards is outside this batch. Extra mixing/sports
examples, spelling recognition and duplicate reading-row placement
likewise remain nonblocking, not unreported closure requirements.

The author authenticated all six reports and exact common prompts
against the native sessions, actual model usage and zero-edit
receipts. The three commits' parent chain, stop-cran author and
committer identities, trailers, normalized file hashes, actual
patches and equivalent evidence derivatives were checked.
Original evidence remains exact: five first-correction families
and seven follow-through families were appended. Current headers
match the historical 71 declarations plus four and six direct
additions: seventeen guarded cards and 81 directional declarations.

The narrow reviewer patches omit the generated manifest diff;
the author separately checked its committed hash and deterministic
regeneration. These checks are not reviewer-executed Git/hash
verification or linguistic certification. GPT independently
retrieved the relevant Daijisen bodies; Claude disclosed its
Weblio extraction limitation and relied on the inspected evidence
and previously retrieved alternative nonmeal support. No app
draws, frequency measurements, native-speaker certification or
official modern JLPT syllabus coverage is claimed. Both processes
have exited. The three specifically identified raw-fetch temporary
paths were already absent; no broad cleanup was performed.

Closure brings the pinned community-list coverage to **600 closed /
0 draft / 1,212 pending / 0 unresolved**, mapped to 594 distinct
articles: 556 new and 38 reused. There are 3,829 word articles and
138 distinct tracked primary reciprocal N2 pairs. The remaining
list is not claimed complete.

**Final diversity assessment:** GPT uniquely supplied the initial
plan-label guards; both reports supplied the nonmeal-context
observation, regardless of its placement or severity. Claude's
substance-wording suggestion improved the example without proving
the former sentence impossible. Its tentative signal comparison
and later optional labels led to supported direct guards after
bounded investigation; GPT independently confirmed the changes.
Using both families was useful on this sample, but their initial
CLEAN judgments did not exhaust secondary-meaning ambiguities.
This is a case record, not a general model ranking.

## Batch 31: N2:602-N2:621

**Status:** closed after independent review and reconciliation.

Scope: 先程, 裂く, 索引, 作者, 削除, 作成, 作製, 探る,
囁く, 刺さる, 匙, 座敷, 差し支え, 差し引き, 刺身, 刺す,
挿す, 注す, 射す, 流石.

Nineteen standalone additions bring the collection to 3,848 word
articles. Exact existing 作者 is reused unchanged, including its
N2 level, reading, creator-of-a-work teaching and 作家 guard.
Kana-primary ささやく, さじ and さすが explicitly teach their
source spellings 囁く, 匙 and 流石 at the actual readings.

刺 receives three useful reciprocal links, for 刺さる, 刺身 and
刺す, bringing distinct tracked primary N2 pairs to 141.
All its existing reading rows remain. Missing primary 裂, 索,
削, 製, 敷, 身, 挿 and 射 remain metadata; no kanji/stroke
articles are fabricated.

The [source packet](n2-vocabulary-batch-sources/batch-31.json)
preserves twenty raw rows and complete principal families, 154
distinct complete comparison families merged consistently from
two extractions, 90 actual existing comparison labels and 37
complete component records. All 93 captured comparison bodies
(including repeated captures), complete relevant family renderings
and public containers were inspected through their boundaries.
Twenty-one positive public receipts distinguish internal headwords
and readings. A failed standalone さすがに extraction remains
explicit, not positive verification; current JMdict2140120 and
the actual 流石 body provide support instead. Public observations
are original concise paraphrases, not copied full bodies.

Practical teaching keeps recent 先程 distinct from an arbitrary
distant past, 裂く tearing separate from 割く-only allocation,
and content deletion separate from event cancellation. 作成 and
作製 retain their practical distinction without a rigid
nonphysical/physical boundary; 作製 includes design drawings.
探る includes tactile search, inquiry and exploration. 囁く's
intransitive classification and quoted と remain distinct.

さじ's kango classification follows the positively inspected
茶匙-origin statement, not an invented sound derivation or an
inference from KANJIDIC's character-reading category. 座敷 is
on-first mixed. 差し引き's deduction and fluctuation senses keep
their separate transitivity. The four new さす verbs keep actual
constructions, including cuttings, sword-wearing, small liquid
additions, 点す-preferred color application and intransitive
sunlight. Emotional 刺さる need not be praise. さすが gives actual
expectation, さすがに and さすがの...も constructions rather than
an unrestricted adjective meaning clever.

Seventeen new cards declare 85 directional exclusions from
direct ordinary-meaning and actual-label checks. Exact spoon
titles already deduplicate; no baseline guard is changed.
These remain author judgments for independent assessment.
Both families will receive the same frozen snapshot, nineteen
articles, exact reuse claim, one-file related diff, twenty
mappings, rubric and source access in sequential processes.
The evidence derivative removes only `quizGuardRationale`.

Coverage is **600 closed / 20 draft / 1,192 pending / 0 unresolved**,
mapped to 614 distinct articles: 575 new and 39 reused. This batch
and the remaining list are not yet claimed review-closed.

### Independent initial reviews and reconciliation

The common authored snapshot is
`e0c3e67907cd8aa09f1c610f70c840e6f64aee74`.
Fresh, isolated **gpt-6.1-sol** and **claude-opus-5.5** processes
reviewed it strictly sequentially, with no edits or delegation.
Both read all nineteen new articles and twenty principal families;
comparison-family coverage was selective, not exhaustive.
Their [GPT](n2-vocabulary-reviews/batch-31-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-31-claude-initial.md) reports
are preserved without rewriting their findings or limitations.

GPT31-01 and B31-R-04 are the same resolved direct 削除/削る
quiz omission. GPT31-02 additionally establishes 作成/書く.
GPT31-03 and B31-R-06 share the 箸 and 足す navigation omissions;
GPT also identified 生, whose なま qualification is retained.
The same link-only follow-through covers the substantive 先
comparison in 先程.

B31-R-01 is resolved with 刺す's target-を/instrument-で pattern,
a needle/finger example and explicit stab recognition. The
pointed-object/destination example and insect-passive explanation
remain distinct. B31-R-02 is resolved by classifying kana-primary
さすが as native-origin `wago`, supported by the actual Nikkoku
entry, without losing 流石's irregular whole-word reading or
inventing a universal kana-type rule. B31-R-03 is resolved by
giving the antecedent for English "still." B31-R-05 is resolved
with attested 杯をさす and no rice distraction; the former
酒をさす was not established to be impossible.

Claude's Optional party/gathering lead receives bounded
follow-through. Twenty-five complete families for sixteen forms
were extracted and read; thirteen families are new to this packet,
with exact equality checked for overlaps. Six complete actual
Daijisen containers were inspected. The separately fetched Nikkoku
origin observation is attributed separately, not passed off as a
hashed Daijisen capture.

座敷 receives direct guards with 宴会, パーティー, 会/かい,
会合 and 集まり from its taught party sense and their actual
party/gathering labels, not a transitive room/festival clique.
差し支え receives direct 迷惑 and 面倒 guards for the applicable
inconvenience/trouble labels; 不自由's affected-state label was
not established as a collision. ささやく/ざわざわ guards the
actual shared murmur labels without equating quiet speech and
collective commotion.

挿す/生け花 remains optional: generic inserting/planting-cutting
labels versus the specifically Japanese art/arrangement are not
established as mutually defensible answers merely by a related
flower activity. Likewise, acknowledging an expectation with
さすが is not the modal expected/should-be use of はず.
The inspected 先程 body does not itself establish GPT's optional
formality claim; no stronger register claim is added. 差引's
irregular-okurigana note and figurative 刺す are nonblocking
expansion, not forced additional scope. 作者/著者 and the existing
書く article's mismatched dictionary citation are pre-existing
outside this batch and are not silently repaired.

Twelve new articles change; no baseline article, kanji passage,
title, spelling, reading, level or sense mapping changes.
Seventeen new cards now declare 95 directional exclusions.
Original source records and initial declarations remain historical;
the packet appends correction evidence, adjudications and current
declarations.

**Model-diversity note:** Both models found 削除/削る and the
箸/足す omissions. GPT uniquely supplied the actionable 作成/書く
pair and 生 link. Claude uniquely supplied the argument-pattern,
native-origin metadata, dangling-English and distracting-example
observations, plus the optional party-label lead and borderline
comparisons. Credit compares every report section, including
Optional. These are useful complementary findings in this sample,
not a model ranking or proof of exhaustive review. Severity for
localized navigation and presentation fixes remains minor.

The corrections still require original-session confirmations;
the twenty rows remain draft and this batch is not closed.

### Original-session confirmations and provenance correction

At corrected snapshot
`51c96bc0b0f9ce230db86a55971efe258c17d61e`,
the original GPT and Claude sessions both found all twelve changed
articles CLEAN on all three facets, accepted the ten new direct
guards and resolved their original findings. Their complete
[GPT](n2-vocabulary-reviews/batch-31-gpt-confirmation.md) and
[Claude](n2-vocabulary-reviews/batch-31-claude-confirmation.md)
confirmations are archived. Work remained strictly sequential;
neither process edited files or independently executed Git.

GPT31-04 establishes a low-severity provenance error, not a missing
lexical sense or learner-card defect: the source appendix claimed
137 sense records in the compact follow-up rendering, but its
twenty-five complete families contain **62**. Independent parsing
of the extraction and rendering agrees: thirteen new families
contain 27 senses, and twelve previously captured families contain
35. The 162 physical lines are not 162 sense objects.

The current provenance statement is corrected to 62. An appended
counting receipt preserves the former false statement explicitly,
records input hashes and explains the counted units. Every
dictionary family, card, guard, mapping and manifest byte remains
unchanged. Historical prompts, frozen snapshots and both reports
are preserved, including Claude's repetition of the incoming
137-sense claim. This is additional useful GPT signal and a
concrete limit on model agreement, not a general model ranking.

The bounded evidence-only correction still requires confirmation;
no whole-batch closure is claimed yet.

### Final confirmation and closure

At evidence-only follow-through
`fd0bfd6ca17d51c7500eb72b5602f6af65dafb42`,
the original sessions confirmed the corrected count sequentially:
[GPT](n2-vocabulary-reviews/batch-31-gpt-followup.md) and
[Claude](n2-vocabulary-reviews/batch-31-claude-followup.md).
Both found the bounded evidence CLEAN on all three facets and no
regression. GPT31-04 is resolved. Claude explicitly withdrew its
earlier 137-sense statement and acknowledged the missed count
error; its prior lexical conclusions are unaffected.

The optional suggestion to add a nonblank-line count is not
required: the receipt already distinguishes families, indexed
records and physical lines. Other stated nonblocking expansions
remain optional, with no consequential unresolved claim in scope.
No article changes followed the jointly confirmed `51c96bc`
content snapshot.

All six archived final reports were authenticated against their
actual native sessions, common prompts, usage models, request
counts and zero-edit records. All three commits, file hashes,
actual patches and evidence derivatives were authenticated. The
authored source evidence remains unchanged; the later provenance
count correction preserves its former false statement explicitly.
These are author-executed mechanical provenance checks, not
independent reviewer Git execution or linguistic certification.
All commits use stop-cran as author and committer.

Structural validation, deterministic manifest bytes and the
comprehensive source/identity/level/sense/reciprocal-link audit
remain clean. No app draws or native certification are claimed.
Initial comparison coverage was selective; closure means no
actionable defect or consequential unresolved claim remains within
this assigned scope, not exhaustive corpus correctness.

Final coverage: **620 closed / 0 draft / 1,192 pending /
0 unresolved**, mapped to 614 distinct articles: 575 new and
39 reused. The repository has 3,848 word articles and 141 distinct
tracked primary reciprocal N2 pairs. Overall N2 vocabulary coverage
is still incomplete.

## Batch 32: N2:622-N2:641

**Status:** review-closed after sequential independent reviews,
evidence-based reconciliation and original-session confirmations.

### Batch 32 authored snapshot

Scope: 撮影, 雑音, さっさと, 早速, 錆, 錆びる, 座布団,
冷ます, 妨げる, 冷める, さようなら, 再来月, 再来週,
再来年, サラリーマン, 騒がしい, さわやか, 三角, 算数, 酸性.

Seventeen standalone additions bring the collection to 3,865 word
articles. Exact existing 再来月, 再来週 and 再来年 are reused
unchanged at their easier N4, N4 and N5 levels. Their calendar-period
meanings, component links and existing reciprocal 再 examples remain.
Kana-primary さわやか explicitly teaches 爽やか.

Four useful new reciprocal pairs are 布/座布団, 団/座布団,
角/三角 and 算/算数. The audit now tracks 145 distinct primary
N2 pairs for new articles; the three reused 再 examples are verified
separately, not added to that new-article count. All existing reading
rows remain. Missing primary 撮, 影, 錆, 妨, 騒 and 酸 remain
metadata; no kanji/stroke cards are fabricated.

The [source packet](n2-vocabulary-batch-sources/batch-32.json)
preserves twenty raw rows, twenty complete principal families
containing 30 indexed senses, 123 complete comparison families
containing 284 indexed senses, 90 actual existing labels/full
articles and 35 complete component records. All captured family
renderings, full comparison bodies and public containers were read
through their boundaries. Counts come from parsed records and body
markers, with exact capture hashes and physical-line counts.

Sixteen actual public lexical containers yielded positive receipts.
The さっさと Weblio extraction failed; a subsequent Kotobank rendering
showed attribution without a definition. Neither is positive lexical
verification. That article stays within current JMdict's prompt/brisk
action and indifferent/cold-manner senses, without an unsupported
universal command-register rule. Public observations are original
concise paraphrases, not copied dictionary bodies.

Practical teaching distinguishes photography activity from finished
media without denying 写真's photography sense. 雑音 includes
figurative criticism. Prompt timing is not simply vehicle speed.
錆's raw color gloss is preserved separately from the current rust
family and the distinct color word 錆色. 座布団 uses the whole
ateji-marked 布団, with voicing; 布団's meditation-cushion sense
prevents an absolute bedding/cushion boundary.

冷ます and 冷める have explicit transitivity, conjugation and
physical/emotional uses. 妨げる need not prevent an activity
completely. The conventional さようなら classification does not
claim an exclusively native origin for every older phrase element.
サラリーマン is explicit wasei-eigo, not every paid occupation.
騒がしい includes troubled times, さわやか includes voice/speech,
算数 includes quantities and shapes, and 酸性 uses の before nouns.

Thirteen new cards declare 59 directional quiz exclusions based on
direct ordinary-meaning and actual-label judgments; no baseline
declaration changes. These judgments remain for independent
assessment, not an exhaustive synonym certification.
Both model families will receive the same frozen snapshot, seventeen
articles, three exact reuse claims, four-file related diff, twenty
mappings, rubric and source access, in sequential processes. The
initial evidence derivative removes only `quizGuardRationale`.

Authored-stage coverage was **620 closed / 20 draft / 1,172 pending /
0 unresolved**, mapped to 634 distinct articles: 592 new and 42
reused. Review closure had not yet been claimed at that stage.

### Batch 32 initial reviews and reconciliation

Common frozen authored snapshot:
`f6d1ef9efca4ffa026bcdb0fe4eb4e768ade64c8`, parent
`dd03c892652a0deb17b1261dd10e0fb33d5328b8`.
Fresh native processes ran sequentially and exited without edits:
[GPT-6.1 Sol (`gpt-6.1-sol`)](n2-vocabulary-reviews/batch-32-gpt-initial.md),
then [Claude Opus 5.5 (`claude-opus-5.5`)](n2-vocabulary-reviews/batch-32-claude-initial.md).
Both received the same prompt, seventeen articles, three reuse
claims, four-file diff, twenty mappings and sanitized evidence.
Both disclosed file-only snapshot verification and scoped source
access; their Git/hash claims remain author-receipt-backed.

All initial report sections were compared, including optional
observations and limits:

| Observation | Reconciliation |
| --- | --- |
| GPT F01 / Claude B32-QZ-01: さっさと/すっと | Resolved: add the direct guard. Actual quick/direct and unhesitating teaching overlaps; both models independently found the previously uncaptured comparison. |
| GPT F02: さわやか/すっと | Resolved: add the separate direct guard for the ordinary refreshed-feeling sense. Other refreshing-word guards are nontransitive. |
| Claude B32-RG-01: farewell-context guidance | Optional bounded clarification: contrast the original teacher/pupil example with お先に失礼します when leaving work first. No unsupported universal frequency, adult-use or final-parting rule is added. |
| GPT optional サラリーマン citation | Resolved citation precision: JMdict's explicit wasei-eigo annotation supports coinage; the Daijisen citation is labelled Definition. |
| Claude optional 雑音/じゃま label overlap | Resolved with accurate noise; static title, retaining signal-interference and figurative prose. No generic interference clique. |
| Claude optional 錆 chain wording | Resolved optional polish: use bicycle チェーン consistently with 錆びる, without claiming 鎖 impossible. |
| Claude other optional additions | Optional, unchanged: extra idioms, command examples, derived noun and a related reading are outside the practical requirements. |
| Claude mapping summary groups N2:640 with additional senses | Clarified without mapping changes: both 算数 senses are already selected; its additional-senses field is empty. |

The correction appends the complete pinned すっと family 1006140:
**one family / three indexed senses**, extracted with both dictionary
hashes checked. The complete rendering and existing article were read.
Sense 1 supports quick/direct movement; sense 3 explicitly supports
feeling refreshed. Initial authored records and initial reports are
preserved; new evidence and adjudications are appended. Thirteen
guarded cards now declare 61 directional exclusions, two more than
the original 59; no baseline card declaration changes.

The captured Daijisen さようなら container supports its conditional
formation and farewell use, not a general register survey. Claude's
different live rendering did not show that dictionary container.
Failed/heading-only retrievals remain limits, not lexical proof.
The farewell clarification uses already evidenced concrete settings
rather than the unsupported broader register proposal.

Model diversity helped in this sample: one quiz defect was shared,
and GPT alone identified the distinct refreshed-feeling guard anywhere
in its report. Claude supplied useful optional title/wording/context
observations; GPT supplied citation precision. The register proposal
needed evidence-based narrowing, not majority voting. These are
sample observations, not a model benchmark. Confirmation and final
provenance authentication remain pending.

### Batch 32 confirmations and closure

Corrected snapshot:
`7c8589f091e37b73a1945e696624e32c1168d8e6`, direct child of
`f6d1ef9efca4ffa026bcdb0fe4eb4e768ade64c8`.
The original native sessions resumed sequentially against the same
corrected snapshot and actual six-file/provenance diff:
[GPT confirmation](n2-vocabulary-reviews/batch-32-gpt-confirmation.md),
then [Claude confirmation](n2-vocabulary-reviews/batch-32-claude-confirmation.md).
Both processes exited with zero edits.

Both confirmed all six changed articles CLEAN on correctness, scoped
coverage and comprehensibility, found no correction regression, and
explicitly carried forward the eleven unchanged new articles, three
reuse claims, four original narrow kanji edits and twenty mappings.
GPT closed F01 and F02; Claude closed its shared quiz finding and
the bounded farewell-context concern, explicitly reclassifying its
broader unverified register proposal as optional.

Claude corrected its initial tracking summary: additional senses
belong to N2:623, N2:624 and N2:631; both 算数 senses were already
selected at N2:640. This required no mapping change. The second
すっと guard is supported specifically by the refreshed-feeling
sense and actual teaching, not merely English smoothly/fluent
similarity. Remaining idioms, derived forms and broader register
surveys are optional; neither reviewer left a consequential
unresolved claim in its assigned scope.

Author-executed authentication checked both commit identities and
parents, stop-cran authorship/committer identity and trailers,
all frozen file hashes, common prompts and actual patches,
both sanitized evidence derivatives, and preservation of every
original authored evidence record with only appended corrections.
The full pinned supplementary family contains three senses;
current front matter has thirteen guarded cards / 61 declarations.
Manifest hashes match committed content for all seventeen new
articles and four related kanji files.

All four archived reports were matched against native session events
and usage records, including actual models, exact prompts,
initial commit context, request counts, zero edits and report text:
GPT session `91216ed4-b7d6-4e68-b6b2-8ed478070164`;
Claude session `72bd5579-de5d-4830-9718-7ad6c3463816`.
Only progress/title preambles and Markdown hard-break normalization
were removed from archives; substantive reports remain unchanged.
These are author provenance checks, not reviewer-executed Git,
runtime quiz testing or native-speaker certification.

Final coverage: **640 closed / 0 draft / 1,172 pending /
0 unresolved**, mapped to 634 distinct articles: 592 new and
42 reused. There are 3,865 word articles and 145 distinct tracked
primary reciprocal N2 pairs for new articles. Existing 再 reuse
examples remain separately verified. Overall N2 vocabulary coverage
is still incomplete.

## Batch 33: N2:642-N2:661

**Status:** review-closed after sequential independent reviews,
evidence-based corrections and original-session confirmations.

### Batch 33 authored snapshot

Scope: 産地, サンプル, 山林, 仕上がる, しあさって, シーズン,
シーツ, 寺院, しいん, 自衛, 塩辛い, 司会, 四角, 四角い,
時間割, 四季, 敷地, 至急, 敷く, 茂る.

Nineteen standalone additions bring the collection to 3,884 word
articles. Source しいん maps to existing しーん, whose body already
explicitly teaches that variant and the complete-silence meaning.
Only sourced `jlpt: 2` is added: identity, primary reading, title,
image and baseline exclusions remain. This is metadata-enriched
reuse, not wholly unchanged reuse.

Seven useful new reciprocal pairs are 林/山林, 寺/寺院,
塩/塩辛い, 辛/塩辛い, 角/四角, 角/四角い and 季/四季.
They bring the distinct tracked primary N2-pair count to 152 across
the expansion. All existing reading rows remain. Missing primary
衛, 司, 敷, 至 and 茂 remain metadata/plain text; no kanji or
stroke cards are fabricated.

The [source packet](n2-vocabulary-batch-sources/batch-33.json)
preserves twenty raw rows, twenty complete principal families with
36 indexed senses, 153 complete comparison families with 467
indexed senses, 100 actual existing labels/full articles and 32
complete component records. Original, supplementary and follow-through
comparison captures were read through their boundaries. Volumes
are calculated from parsed records and `CARD` markers, deduplicated
by identity; repeated component captures are not double-counted.
Capture hashes and physical-line counts preserve the inspected
boundaries. Nineteen positive public lexical-container receipts use
original concise paraphrases, not copied full dictionary bodies.

Teaching keeps product-origin and personal-origin uses qualified;
samples need not be free or edible, and woodland has no universal
altitude/tree-count threshold. 仕上がる is explicitly intransitive,
contrasted with 仕上げる. Standard しあさって is day +3; inclusive
fourth-day counting and regional day +4 remain distinct. シーズン
is not sport-only and シーツ is specifically bedding.

寺院's Buddhist default does not erase the broader religious-building
sense. 自衛 is not only military or a legal certification.
塩辛い's rare-spelling reading restrictions remain explicit.
司会 covers proceedings and the role-holder. 四角/四角い include
rectangles, with noun/adjective attachment and mixed formation
explained. 時間割's on-first and 敷地's kun-first mixed readings
are explicitly qualified rather than represented as homogeneous.

至急 takes direct adverbial use or の, not な. 敷く keeps its core
transitive pattern distinct from bounded extensions and the formal
intransitive sense. Search-only spellings are not recommended.
茂る concerns luxuriant vegetation, not an expensive lifestyle;
current alternatives and obsolete spelling are distinguished.
Additional meanings remain separate from the selected source senses
and do not acquire independent N2 assignments.

Sixteen new cards declare 64 directional quiz exclusions based on
direct ordinary-meaning and actual-label judgments; no baseline
declaration changes. These remain author judgments for independent
assessment, not exhaustive synonym certification. Both model families
will receive the same frozen snapshot, nineteen new articles, one
metadata-enriched reuse claim, seven-file related diff, twenty
mappings, rubric and source access in sequential short-lived processes.
The initial evidence derivative removes only `quizGuardRationale`.

Authored-stage coverage: **640 closed / 20 draft / 1,152 pending /
0 unresolved**, mapped to 654 distinct articles: 611 new and 43 reused.
No review closure is claimed at this stage.

### Batch 33 initial reviews and reconciliation

Both families independently reviewed authored commit
`59bd8cbbcce388fd2c1375a3b0b1577fb9138e77`, parent
`03b1c83a17bdf00335484d77d818c34b628ffaac`, on the same frozen
scope, rubric and source access. The isolated GPT process exited
before Claude started; both were read-only, with no delegation.
Native session records and usage receipts authenticate the actual
models, common prompt and zero edits:

- [GPT initial](n2-vocabulary-reviews/batch-33-gpt-initial.md):
  `gpt-6.1-sol`.
- [Claude initial](n2-vocabulary-reviews/batch-33-claude-initial.md):
  `claude-opus-5.5`.

Both read all nineteen new articles, the metadata-enriched reuse
claim, seven-file related diff, six kanji cards and twenty mappings.
All mappings, reuse coverage and narrow kanji edits were CLEAN.
No incorrect taught definition, reading, inflection or example was
established. Each report retains separate three-facet verdicts.
The archives preserve complete native final messages, including
Claude's substantive paragraph before Snapshot; only Markdown
hard-break spacing is normalized. CLI progress output is not a
substitute for the native final report.

GPT inspected complete relevant principal/comparison families and
independently retrieved ten actual lexical bodies. Claude read
principal records but only partly inspected comparison renderings
and component evidence; its attempted public retrievals did not
independently verify the author's Daijisen receipts. These different
actual inspection limits remain in their reports. Neither could
execute Git, compute receipt hashes or run the app; the author
performs those mechanical provenance checks separately.

| Initial observation | Adjudication and correction |
| --- | --- |
| GPT B33-G01; Claude Optional: 産地/出 | Add the direct 出 guard. Principal 1303820:3 and comparison 1896380:4, plus actual origin labels and 地方の出 teaching, support ordinary personal-origin overlap. Existing origin edges are not transitive. |
| GPT B33-G02; Claude Optional: 仕上がる/しまう | Add the direct しまう guard. Actual finish label and complete 1305380:1,4 establish English-answer overlap without making intransitive, transitive and auxiliary constructions interchangeable. |
| GPT B33-G03; Claude B33-03: 至急/はきはき | Remove the edge. The actual clear/brisk-speaking label is not urgent/as-soon-as-possible timing. A loose promptly gloss is insufficient. Claude's proposed copied-from-other-cards cause is unestablished; accepting the semantic correction does not ratify that causal story. |
| GPT B33-G04; Claude B33-01 and B33-02: missing navigation | Link existing あさって and 明日 at the day-sequence teaching and 式 at the homophone comparison. Different days and homophones do not themselves require quiz guards. |
| Claude Optional: シーズン example | Add a professional-baseball league-season example for selected sense 1. Existing sporting-season definition was accurate; this is useful scoped illustration, not a mapping repair. |
| Claude Optional: 四角 attribution | Name the already inspected Daijisen source in 四角 and the parallel 四角い passage. No new figurative claim or invented JMdict index. |

The extra しいん example remains optional: the existing alias
already follows the applicable と/する pattern. No baseline body
edit is required. The tentative 寺院/神社 category/title concern
does not establish a synonymous answer; the accurate broader sense
and explicit Shinto-shrine contrast remain. This bounded decision
does not certify every possible religious-building context.

The correction changes eight new articles, adding two direct quiz
pairs and removing one. Sixteen cards now declare **65 directional
exclusions**, rather than the authored 64. All three consequential
comparison families were already complete in the initial evidence;
no additional family is claimed. Original evidence/declarations
remain unchanged, with correction evidence appended. The updated
review derivative still removes only `quizGuardRationale`.
All twenty source mappings, reuse metadata, six kanji edits and
baseline word declarations are unchanged.

Comparing equivalent observations across **all report sections**,
both models identified the omitted 出/しまう pairs, unsupported
はきはき pair and missing day/homophone links. GPT classified the
first two as actionable; Claude listed them as optional. They are
not GPT-unique discoveries. Claude supplied useful optional
baseball-example and source-attribution polish. This batch shows
reinforcing and differently prioritized observations, not a
verified model-unique actionable defect, general ranking or
measurement of eliminated model bias. These author adjudications
still required the bounded confirmations recorded below.

### Batch 33 confirmations, authentication and closure

Both original sessions confirmed corrected commit
`897af874e6803c47dc933b7a52f0bb2d55752e79`, directly following
the authored snapshot. GPT exited before Claude started; both
remained read-only, without delegation:

- [GPT confirmation](n2-vocabulary-reviews/batch-33-gpt-confirmation.md):
  `gpt-6.1-sol`.
- [Claude confirmation](n2-vocabulary-reviews/batch-33-claude-confirmation.md):
  `claude-opus-5.5`.

Each read its own initial report, the complete correction patch,
all eight changed articles, the three complete consequential
comparison families and their actual 出/しまう/はきはき articles.
Both confirmed all eight articles CLEAN on correctness, scoped
coverage and comprehensibility, resolved their original findings
and found no correction regression or consequential unresolved
claim. The eleven unchanged new articles, metadata-enriched reuse,
six original kanji edits and twenty mappings explicitly retain
their earlier verdicts; this is not a renewed whole-article audit.

Claude now classifies the two formerly optional missing guards as
actionable and explicitly withdraws its speculative copying
explanation. The additional しいん example and generic 寺院/神社
category/title concern remain nonblocking. Neither agreement nor
reclassification retroactively creates a unique initial discovery.

GPT independently inspected actual Daijisen 四角/四角い entries.
Claude inspected the 四角い body but only a truncated 四角
sense-3 meta description; its full source-access qualification
remains explicit. Confirmation does not imply reading the entire
large evidence derivative, independent Git/hash execution, runtime
quiz draws, frequency testing or native-speaker certification.

Author-side authentication matched all four complete final reports
to the corresponding native-session turns, both actual models,
common prompts and zero-edit usage receipts. It verified the
two commit identities, stop-cran author/committer details and
trailers, frozen hashes, actual patches, exact corrected content
scope, both sanitized derivatives and unchanged original evidence
with only the appended correction record. All nineteen new and
seven related content hashes match the corrected manifest.

Mechanical closure changes only the twenty row statuses and
their tracking hash/counts, packet status and closure records.
Teaching content is unchanged from the confirmed snapshot.
The deterministic manifest remains **6,512 files**, including
396 images and 201 scene catalogs; version `5b9e1edd37000003`.
The complete coverage/identity/restriction/link audit preserves
baseline identities/readings/titles and the previously documented
metadata and quiz exceptions.

Final coverage: **660 closed / 0 draft / 1,152 pending /
0 unresolved**, mapped to **654 distinct articles: 611 new and
43 reused**. There are **3,884 word articles** and **152 distinct
tracked reciprocal primary N2 kanji-word pairs**. This closes
batch 33, not the remaining vocabulary expansion.

## Batch 34: N2:662-N2:681

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 持参, 磁石, 四捨五入, 始終, 自習, 静まる, 姿勢,
自然科学, 時速, 子孫, 死体, 下書き, 下町, 自治, 実感,
湿気 (しっけ and しっき), しつこい, 実習, 実績.

Nineteen new articles cover twenty separately preserved source rows.
Both 湿気 readings belong to one article, with primary しっけ and
explicit alternate しっき; no second same-ID card or frequency
ranking is manufactured. The collection now has 3,903 word articles.
Five reciprocal primary N2 pairs are 捨/四捨五入, 勢/姿勢,
孫/子孫, 湿/湿気 and 績/実績, bringing the tracked distinct
pair count to 157. Existing kanji reading rows and source-only
qualifications remain; missing 磁 and 姿 stay metadata/plain text.

The [source packet](n2-vocabulary-batch-sources/batch-34.json)
preserves twenty raw rows, nineteen complete principal families
with 28 indexed senses, 255 complete comparison families with
563 indexed senses, 130 actual existing labels/full articles and
38 complete component records. Original and supplemental families
and comparison articles were inspected through their boundaries.
Identity-deduplicated volumes, exact capture hashes and physical
line counts are machine-computed. The identical supplemental
component capture is verified rather than counted twice.
Nineteen positive Digital Daijisen lexical-container receipts
retain original concise observations, not copied full entries.

四捨五入 teaches place value and half-away-from-zero ties, not
always rounding upward. 始終 covers habitual frequency as well
as continuity. 自習's classroom sense has its actual spelling
restriction, while 静まる/鎮まる preferences are not absolute
semantic compartments. 姿勢 covers physical and figurative
stances. 自然科学 is not all scholarship; 時速 is a rate
with an independently specified distance unit.

子孫 is broader than grandchildren. 死体 includes humans and
animals, with respectful-wording tendencies qualified.
下書き's drawing extension is separately attributed to Daijisen,
not assigned an invented JMdict index. Both general 下町 and
Tokyo Shitamachi senses are selected by the actual source gloss.
自治 need not mean national independence; 実感 does not verify
objective truth. Kana-primary しつこい retains empty component
metadata and the alternate reading's kana-only restriction.
実習 and 自習 describe different learning axes, and 実績
does not guarantee uniformly excellent results.

Seventeen new cards declare 104 directional quiz exclusions.
These direct ordinary-meaning/actual-label judgments remain
subject to independent assessment; no baseline declarations change.
Both families will receive the same frozen snapshot, nineteen
complete new articles, five-file narrow kanji diff, twenty
mappings, rubric and source access, sequentially without
delegation or edits. The evidence derivative removes only
`quizGuardRationale`.

Authored-stage coverage: **660 closed / 20 draft / 1,132 pending /
0 unresolved**, mapped to **673 distinct articles: 630 new and
43 reused**. This is not review closure.

### Batch 34 initial review and reconciliation

Both independent models reviewed authored commit
`7c8c93f153dd5909bc467106d1c6f2ecdb386f89`, parent
`e99ab822cef8fb4819f24dc0f688d7ac3326da49`, sequentially in
separate read-only native processes, without delegation:

- [GPT initial](n2-vocabulary-reviews/batch-34-gpt-initial.md):
  `gpt-6.1-sol`.
- [Claude initial](n2-vocabulary-reviews/batch-34-claude-initial.md):
  `claude-opus-5.5`.

Both assessed all nineteen new articles, twenty mappings and five
narrow kanji edits. Both found the mappings and kanji edits CLEAN
on all three facets. GPT inspected the complete supplied principal,
comparison and component records, actual comparison metadata and
consequential bodies; it independently inspected eight assigned
public headwords and the 遺体 comparison. Claude selectively
inspected consequential comparison/component records and actual
additional labels. Its public retrieval yielded only truncated
Kotobank summaries for 静まる/始終 and no Weblio entry text.
Neither file-only reviewer independently executed Git or hashes.
Author-side authentication matched the complete native final
messages, prompts, models, zero-edit usage and authored evidence;
substantive text before Snapshot is preserved.

GPT F1 is **resolved** by removing five unsupported 始終 edges:
継続, 続く, 続ける, 繰り返す and 重ねる. Continuation or
doing something again is not itself the temporal-extent/frequency
answer. This is a semantic distinction, not a parts-of-speech
shortcut. Claude independently questioned three of those edges
in Optional; those three observations are shared, while GPT
additionally identified 継続 and 繰り返す.

Claude R01-R03 are **resolved** by adding direct 静まる/止む,
持参/連れる and 始終/いつでも guards. Three additional complete
families and actual articles were captured and inspected:
1310640:1, 1559290:1 and 1577130:1-2. Their cessation, bringing
along and all-times senses support the actual English-label
ambiguities independently of existing guards or shared tags.
持参 explicitly contrasts an item with accompanying a person;
the English-label guard does not make the Japanese constructions
interchangeable.

Claude R04 is **resolved as learner-facing spelling clarity**:
the subsiding example now uses 静まる before 鎮まる is introduced.
The original alternate-spelling sentence was not linguistically
wrong and did not invalidate the mapping; neither spelling is
made a strict sense restriction. R05 is **resolved** by recognizing
current noun 始終 for the full course of events, alongside
一部始終. The suggestion that 一部始終 is more common is not
adopted without frequency evidence. R06 and GPT's corresponding
Optional are **resolved** by showing シュウ voiced to ジュウ.
R07 is **resolved** with katakana ケ for the on reading.

The optional 孫 and member-science guards are not added merely
for a general/specific relationship; this is not an unrestricted
single-best-answer exemption. The tentative 実習/学・学問 and
姿勢/形・様子 removals remain **optional, not established
defects**: their broader learning and outward-form/appearance
labels remain reasonable answers at the quiz's coarse gloss
granularity. This does not equate every Japanese use or endorse
transitive exclusions. The existing 収める guard retains its
independently captured settle/subdue sense.

Additional 自治 abbreviation and 持参 register examples remain
**optional**; neither is needed for the accepted source mappings.
The priority-tag-only proposal to rank 湿気 readings is not adopted:
dictionary recognition/priority does not measure their relative
frequency. No baseline article or kanji reading is changed.

The correction changes four articles. Seventeen cards now declare
**102 directional exclusions**, net -2 from historical 104:
three direct additions and five removals. Original evidence,
declarations and rationale are preserved, with correction evidence
appended. Deduplicated comparison totals become **258 complete
families / 567 indexed senses / 133 actual comparison labels**;
the repeated component capture is verified equal, not recounted.
The updated review derivative still removes only
`quizGuardRationale`. All twenty mappings, other fifteen articles,
five kanji edits and baseline declarations remain unchanged.

Comparing equivalent observations across all report sections,
both models contributed voicing clarification and three tentative
overguard observations. GPT uniquely identified two further
unsupported 始終 edges; Claude uniquely identified three
supported missing guards, current-noun clarity and the early
alternate-spelling presentation, plus on-reading typography.
Their different useful catches support retaining sequential
multi-model review on this sample, not a general model ranking
or a measurement that bias has been eliminated. These author
adjudications required the bounded confirmations recorded below.

### Batch 34 confirmations, authentication and closure

Both original sessions confirmed corrected commit
`7fb68ea9dcd83db0578b4999862046e8bf64f8b3`, directly following
the authored snapshot. GPT exited before Claude started; both
remained read-only, without delegation:

- [GPT confirmation](n2-vocabulary-reviews/batch-34-gpt-confirmation.md):
  `gpt-6.1-sol`.
- [Claude confirmation](n2-vocabulary-reviews/batch-34-claude-confirmation.md):
  `claude-opus-5.5`.

Each read its own initial report, the complete correction patch,
all four changed articles, the three additional complete comparison
families and their actual articles, and the relevant earlier
families. Both found the four articles CLEAN on correctness,
scoped coverage and comprehensibility, confirmed resolution of
their original findings, accepted the retained optional guards,
and identified no correction regression or consequential unresolved
claim. Both independently recounted seventeen guarded cards and
102 directional declarations. The fifteen unchanged articles,
five original kanji edits and twenty mappings explicitly retain
their earlier verdicts, not renewed whole-content reviews.

Claude's confirmation says it originally raised all five removed
edges. Its preserved initial Optional names only 続く, 続ける
and 重ねる. The initial record governs attribution: 継続 and
繰り返す remain GPT-only initial observations. Later acceptance
does not retroactively create a shared discovery. Claude also
discloses the other reviewer's finding labels in the assigned
adjudication patch; confirmations assess corrections and are not
new blind initial reviews. Neither read the other family's report.

GPT independently inspected actual Daijisen 始終/静まる bodies.
Claude's external evidence remains the truncated Kotobank
descriptions fetched initially; its Weblio entry text was not
retrieved. The additional comparison captures are author-provided.
Confirmation does not imply full-derivative inspection, independent
Git/hash execution, runtime quiz draws, usage-frequency testing
or native-speaker certification.

Author-side authentication matched all four complete final reports
to exact native-session turns, actual models, common prompts and
zero-edit usage receipts. Native message boundaries exclude CLI
progress text; the complete final messages are preserved rather
than extracted by a Snapshot substring. Authentication verified
both commit identities, stop-cran authorship/committer details and
trailers, frozen hashes, actual patches, exact correction scope,
both sanitized derivatives and unchanged authored evidence with
only appended corrections. All nineteen new and five related
content hashes match the corrected manifest.

Mechanical closure changes only the twenty row statuses and
their tracking hash/counts, packet status and closure records.
Teaching content remains identical to the confirmed snapshot.
The deterministic manifest remains **6,531 files**, including
396 images and 201 scene catalogs; version `a098aea1d9ca6275`.
The complete coverage/identity/restriction/link audit preserves
baseline identities/readings/titles and the previously documented
metadata and quiz exceptions.

Final coverage: **680 closed / 0 draft / 1,132 pending /
0 unresolved**, mapped to **673 distinct articles: 630 new and
43 reused**. There are **3,903 word articles** and **157 distinct
tracked reciprocal primary N2 kanji-word pairs**. This closes
batch 34, not the remaining vocabulary expansion.

## Batch 35: N2:682-N2:701

**Status:** closed after sequential initial reviews and two bounded confirmation rounds.

Scope: 湿度, 執筆, 実物, しっぽ, 実用, 実力, 実例,
失恋, 指定, 私鉄, 児童, 縛る, 地盤, しびれる, 紙幣,
しぼむ, 絞る, 縞, 地味 and しみじみ.

Eighteen new articles and two metadata-enriched reuses cover
twenty source rows. Existing 湿度 and 児童 gain only sourced
`jlpt: 2`; their stable IDs, primary readings, titles, teaching
and exclusions remain unchanged. The collection now has
**3,921 word articles**. Three narrow kanji edits add or link
筆/執筆, 恋/失恋 and 鉄/私鉄. These bring the historical
new-article-only reciprocal audit to **160 distinct pairs**.
The already reciprocal 湿/湿度, 児/児童 and 童/児童 links
are preserved but not added to that new-article-only count.

The [source packet](n2-vocabulary-batch-sources/batch-35.json)
preserves twenty raw rows, twenty complete principal families
with 44 indexed senses, 302 complete comparison families with
780 indexed senses, 150 actual comparison labels and 33 complete
component records. All those records and twenty positive public
Digital Daijisen containers were inspected. Of 150 captured full
comparison articles, **seventeen** were read in full, explicitly
listed in the packet; the other 133 captures are not claimed as
inspections. The two reused principal articles were read separately.
Capture hashes, physical line counts and volumes are computed.
Public observations are original concise paraphrases.

実力 selects both ability and force because the raw source
explicitly includes both. しぼむ retains one broad principal
sense rather than borrowing public subdivisions as new indices.
絞る/搾る preferences are not absolute spelling restrictions;
practical extensions are separately mapped. 私鉄 includes the
conventional non-JR distinction without calling today's JR
companies national railways. Separate public identities under
みもの, しべい and ちみ are not pooled into the teaching.

地盤 distinguishes supporting ground and additional support-base
uses; 地味 teaches な/に attachment and the separately indexed
colloquial degree use. しびれる's sleeping-limb gloss is numbness,
not literal sleeping. 縞's historical spellings do not reuse 島's
modern island identity; 柄 is がら in its pattern sense.
しみじみ permits optional と without inventing a suru entry.
Missing primary 執/縛/盤/幣/絞/縞 remain metadata/plain text.
Kana-primary しっぽ/しびれる/しぼむ/しみじみ keep empty arrays.

Eighteen new cards declare **77 directional quiz exclusions**;
reused declarations are unchanged. These direct ordinary-meaning
and actual-label judgments are pending independent assessment.
Both reviewers receive the same frozen snapshot, all eighteen
new articles, two narrow reuse claims, three kanji edits, twenty
mappings, rubric and source access. Processes run sequentially
without delegation or file edits; the evidence derivative removes
only `quizGuardRationale`.

Authored coverage: **680 closed / 20 draft / 1,112 pending /
0 unresolved**, mapped to **693 distinct articles: 648 new and
45 reused**. This is not review closure.

### Initial review

Both independent reviewers assessed committed snapshot
`978aed9979689800a07e505bf370846e4c3cc12c`, parent
`3c899fabf15e967b5f8d815dd0ad6247ad110f04`, with the same assigned
scope, rubric and source access. The isolated processes ran
sequentially, exited fully and reported zero edits. Actual models
and complete native final messages are retained:

- [GPT initial](n2-vocabulary-reviews/batch-35-gpt-initial.md):
  `gpt-6.1-sol`.
- [Claude initial](n2-vocabulary-reviews/batch-35-claude-initial.md):
  `claude-opus-5.5`.

Both read all eighteen new articles, twenty principal families
and the narrow related changes. GPT additionally read seventeen
comparison bodies, but not all captured bodies or families.
Claude read all 150 labels but no captured comparison bodies
and most comparison families were not inspected. Native tool
events show no application-code access; neither reviewer ran
a quiz. Their file-only Git/hash limitations remain explicit.

### Reconciliation

Eleven new articles are changed. Nineteen additional actual
comparison articles and 27 complete families were captured and
inspected after initial review. One family and one label duplicate
original records and were verified equal. The append-only
correction evidence adds **26 families / 56 indexed senses /
18 labels**, for **328 comparison families / 836 senses /
168 labels**. Thirty-six full comparison bodies were actually
inspected; this does not turn every capture into an inspection.
All 33 repeated component records equal the authored capture.

| Initial observation | Author decision and evidence |
| --- | --- |
| GPT 01: しっぽ/仕舞い | Add the direct tail-end/final-part precaution, supported by actual labels and 1594530:1; do not pool the separate suffix or dance identity. |
| GPT 02: 実用/用いる | Add the direct practical-use/use label precaution with 1546210:1; differing Japanese grammatical classes do not remove this English-label ambiguity. |
| GPT 03: 実力/能 | Add the ability/talent edge using 1470120:1 and the actual 能 article, independently of existing 才能/能力 guards. |
| GPT 04 / Claude Optional: 実例/ケース | Add the actual-case/instance edge using 1047880:2. The computing CASE identity is separate. This observation is shared, not GPT-unique. |
| GPT 05 / Claude Q2: 地盤/基・基本 | Add both foundation edges using actual labels, 1260670:2 at もと and 1219190:1. Other 基 readings are not pooled. |
| GPT 06 / Claude Q4: しびれる/凍える | Add the numb-with-cold overlap using 1446180:1 and 1569620:1; a cause-specific numb state remains a numb state. |
| GPT 07 / Claude Q1: 紙幣/金銭 | Add the broad money-answer precaution using 1243020:1 and the actual article, not merely shared finance tags. |
| GPT 08: 絞る/ぎゅうぎゅう | Add the squeezing-hard precaution using 1003600:2-3 and the actual article; mimetic manner versus action does not make the coarse label safe. |
| Claude C1: しみじみ construction | Teach positively attested しみじみとした + noun with 気持ち, reading and gloss. Narrow the moderate allegation to a minor construction/guidance omission. The [actual WURK section](https://eigobu.jp/magazine/simijimi) supports this pattern, not unrestricted standalone する, omission of と, or a “very common” ranking. Clarify only the TSV source note; preserve raw source fields and indices. |
| Claude C2: non-animal tail end | Replace vague しっぽの部分 with attested 列のしっぽ and its reading/gloss. [Seisen's しっぽ sense 4](https://kotobank.jp/word/尻尾-521708), not the separate しりお heading, supports it. |
| Claude C3: 絞る scope | Explicitly place extortion/exploitation outside the practical introduction, together with bow/sumo/go uses. Complete 1594520:4 and [Daijisen 2イ](https://kotobank.jp/word/絞る-523544) support the scope statement; no selected/additional index expansion. |
| Claude Q3: 地味/謙虚 | Not adopted as a required guard. Actual 地味 concerns unshowy appearance/living; actual 謙虚 and 1260190:1 concern a nonboastful, receptive attitude. “Modest” and shared tags alone do not establish equivalent answers; 謙虚 already distinguishes a modest dwelling. Await independent reassessment of this decision. |
| Claude Q5: しみじみ/感激・感動 | Add both coarse deeply-felt/deep-emotion precautions using complete 1005610:1, 1212360:1 and 1212570:1 and actual articles. This does not equate every reflective use with a strong emotional response. |
| Claude Optional: 実力/勢い and 実例/場合 | Add both precautions from actual force and case/situation labels and complete 1375040:1-2 and 1355810:1, not transitivity or topic membership. |
| Claude Optional: other proposed guards | Do not add 執筆/文字, 地味/原・野, 実例/事件 or 縛る/不自由 merely from shared English tokens or topics. Distinguish authoring from written representation, geographical plains from unshowy appearance, incident from illustrative instance, and active binding from an inconvenienced/restricted state. |
| Claude Optional: remove 縞/棒 | Retain the precaution and explain the actual drawn-line/dash sense already taught on 棒 and recorded in 1519750. The initial reviewer had not read that comparison body. Physical rods are not equated with stripe patterns. |
| Claude Optional: wording polish | Remove しぼむ's vacuous ichidan warning, 紙幣's unrelated no-money clause and しびれる's opaque diagnosis sentence; identify the sensation mimetics accurately. Extra electric-shock and tail-idiom examples remain optional. |

The corrected cards have **90 directional declarations across
eighteen new articles**, thirteen additions and no removals.
Baseline guards, identities, primary readings/titles, levels,
source identities and selected/additional indices are unchanged.
The original authored evidence and its 77 declarations remain
historical; current declarations and per-observation decisions
are appended rather than silently replacing them.

Across all report sections, **five accepted missing pairs are
shared**, **four are GPT-only** and **four are Claude-only**.
Claude also prompted the three teaching/scope clarifications
and tightly coupled polish. Several tentative suggestions and
the unsupported frequency claim were not adopted. Diversity
was useful on this sample, not a general model ranking or proof
of bias elimination. A Weblio example count or footer-only page
does not establish rendered examples, and an inaccurate generated
search summary is not substituted for actual source bodies.

The first corrected snapshot remained draft pending the
confirmations below.

### First confirmation and follow-through

The original reviewer sessions resumed sequentially on
`5d8e436a121ad5007143f771f76c3fcdff0a981e`, parent
`978aed9979689800a07e505bf370846e4c3cc12c`. Both exited with
the requested actual models and zero edits. Their complete
reports, including the disagreement, are preserved:

- [GPT confirmation](n2-vocabulary-reviews/batch-35-gpt-confirmation.md):
  all eight original findings resolved; no actionable regression
  established in the bounded correction.
- [Claude confirmation](n2-vocabulary-reviews/batch-35-claude-confirmation.md):
  C1-C3, Q1-Q2 and Q4-Q5 resolved; Q3 maintained. The reviewer
  explicitly withdraws the unsupported “very common” claim.

GPT inspected the complete actual patch and all eleven changed
articles. Claude read the content/TSV patch and the equivalent
readable comparison materials, but not the full appended JSON
patch; this is a disclosed inspection limit, not complete patch
inspection. Both inspected the nineteen comparison bodies.
The shared confirmation evidence exposed author adjudications
and model-origin IDs after the blind initial reviews; neither
reviewer read the other's reports.

The maintained Q3 was reassessed against the actual behavioral
sense, not settled by a model vote. The initial rejection gave
too much weight to unshowy living versus humility and too little
to **reserved/modest behavior**, explicitly taught by 地味 and
complete **1421490:2**. Add **地味/謙虚** as a defensible
coarse-label precaution. A linked contrast preserves that
unshowy appearance does not itself imply a nonboastful,
receptive attitude; the Japanese words are not made identical.

Also accept Claude's new optional **しびれる/感激** precaution:
the actual 感激 article's thrilled/deep-emotion use overlaps
the taught excited/enthralled **1569620:3**, supported by complete
**1212360:1**. This is direct evidence, not propagation through
感動. Sense 2 concerns electric shock, not emotional excitement.

These two new guards bring the final proposed declarations to
**92 across eighteen new cards**, fifteen cumulative additions
from authored 77. Five accepted pairs are shared across initial
reports, four are GPT-origin and six Claude-origin, including
the maintained Q3 and new confirmation optional pair. The
earlier thirteen-pair count and the first disagreement remain
historical rather than being retroactively rewritten.

Standalone-する frequency wording, duplicated TSV scope prose,
extra electric-shock examples and tail idioms remain optional.
Only 地味 and しびれる receive this follow-through; no TSV,
source identity/index, primary title/reading, level, reused-card
or kanji change. The source packet appends this round separately.
This snapshot remained draft pending the final checks below.

### Batch 35 final confirmations, authentication and closure

The original sessions resumed sequentially on
`5b7172746841f986ab642c5acfeed0bbc53314a1`, parent
`5d8e436a121ad5007143f771f76c3fcdff0a981e`.
GPT exited before Claude started; both actual requested models
remained read-only, without delegation:

- [GPT follow-through](n2-vocabulary-reviews/batch-35-gpt-followup.md):
  `gpt-6.1-sol`.
- [Claude follow-through](n2-vocabulary-reviews/batch-35-claude-followup.md):
  `claude-opus-5.5`.

Both read the complete actual follow-through patch, both changed
articles, both comparison articles and complete relevant families
1421490, 1569620, 1260190 and 1212360. Each rated 地味 and
しびれる CLEAN on correctness, scoped coverage and
comprehensibility, accepted both direct guards and found no new
regression or consequential unresolved claim. GPT explicitly
revises its prior judgment on Q3; Claude closes its maintained
finding. This is evidence-based reconciliation, not an erased
first-round disagreement or a forced initial consensus.

Both explicitly carry forward the sixteen other new articles,
five related changes and twenty mappings, not renewed whole-batch
inspection. Both recounted the supplied declarations as 92 across
eighteen cards. Claude's suggested 感激 mention in the comparison
prose remains nonblocking; no teaching change was made after
these final confirmations.

Author-side authentication matched all six complete final reports
to exact native-session turns, common prompts, actual models and
zero-edit usage receipts. Native message boundaries retain the
entire final messages, including substantive text before Snapshot,
while excluding CLI progress. All three snapshots, stop-cran
author/committer details and trailers, normalized hashes, actual
patches, exact content scopes and three sanitized derivatives
were authenticated. Authored records remain unchanged with only
appended corrections; the first correction's 90 declarations and
earlier adjudications remain unchanged with only the appended
follow-through.

The sole TSV correction before closure is N2:701's source-note
clarification, explicitly preserving its authored/current values.
Raw source fields, mapping identities and selected/additional
sense indices are unchanged. All eighteen new and five related
content hashes match each snapshot's corresponding manifest.
The follow-through changes no reused card, kanji, TSV or snapshot.

Mechanical closure changes only the twenty row statuses and
tracking hash/counts, packet status, reports and closure notes.
Teaching content remains identical to the confirmed snapshot.
The deterministic manifest remains **6,549 files**, including
396 images and 201 scene catalogs; version `911a538362fa5977`.
The complete coverage/identity/restriction/link audit preserves
the 3,273 baseline identities/readings/titles and documented
metadata/quiz exceptions.

Final coverage: **700 closed / 0 draft / 1,112 pending /
0 unresolved**, mapped to **693 distinct articles: 648 new and
45 reused**. There are **3,921 word articles** and **160 distinct
tracked reciprocal primary N2 kanji-word pairs**. This closes
batch 35, not the remaining vocabulary expansion. Neither model
executed Git/hashes or quiz draws; CLEAN is scoped review, not
exhaustive linguistic or native-speaker certification.

## Batch 36 - N2:702-N2:721

**Status:** closed; independent reviews and bounded confirmations reconciled.

Scope: 氏名, 締め切り, 締め切る, 湿る, ジャーナリスト,
社会科学, しゃがむ, 蛇口, 弱点, 車庫, 車掌, 写生, 社説,
しゃっくり, シャッター, しゃぶる, 車輪, 洒落, じゃんけん
and 集会.

Twenty new articles cover twenty source rows with no principal
reuse. Source 締切 is normalized to 締め切り, explicitly
teaching both 締切 and 締切り at しめきり. The collection now
has **3,941 word articles**. Four narrow kanji edits link
湿/湿る, 弱/弱点, 庫/車庫 and 輪/車輪 at the actual readings;
the distinct tracked primary reciprocal N2 total becomes **164**.

The [source packet](n2-vocabulary-batch-sources/batch-36.json)
preserves twenty raw rows, twenty complete principal families
with 26 indexed senses, 213 deduplicated complete comparison
families with 435 indexed senses, 110 actual comparison labels
and 29 complete component records. All those records and twenty
actual public Digital Daijisen lexical containers were inspected.
Of the original 102 captured comparison bodies plus ten
supplementary captures, **75 distinct full bodies** are counted
as inspected, explicitly listed in the packet. Two supplementary
labels repeat original labels and were checked equal; complete
repeated families were also checked before deduplication.
Partial-body reads are not counted as full-body inspections,
including a truncated source-URL continuation. Captures, hashes
and computed volumes do not substitute for independent review.

氏名 separates the practical しめい full name from the public
うじな surname heading. 蛇口 is mixed ジャ + くち, voiced to
ぐち, with the repository's on-first `kango` category explained.
洒落 is ateji, not an ordinary シャ + ラク on compound.
The joke sense is selected; style recognition is additional.
Separate public しゃら/しゃらく and 集会's historical Buddhist
headings are not pooled with the practical readings.

締め切る's raw “shut up” is physical closing, not silencing a
person; closing applications is separately mapped. 湿る teaches
godan 湿って and an additional figurative slump, with attested
打線が湿る and the exact しめる restriction. 写生 is not forced
into outdoor, pencil-only or rough-draft use; direct observed
depiction includes a qualified literary extension. 社説 concerns
institutional opinion. 車庫/駐車場 is not falsely divided into
indoor/outdoor facilities. しゃっくり permits recorded する.
しゃぶる qualifies the raw “chew” against suck/lick use.

All primary written characters remain in metadata, including
missing 氏/締/蛇/掌/洒. Kana-primary articles keep empty arrays
despite recognized rare kanji spellings. Additional senses do
not receive independent N2 assignments. No existing word ID,
primary reading, title, level, body or exclusion is changed.

Seventeen new cards declare **57 directional quiz exclusions**.
These direct ordinary-meaning and actual-label judgments await
independent assessment; they are not transitive synonym groups.
Both reviewers receive the same frozen committed snapshot,
twenty complete new articles, four narrow kanji edits, twenty
mappings, rubric and source access. The blind derivative
removes only `quizGuardRationale`. Processes run sequentially
without nested agents, author edits or concurrent reviewers.

Authored coverage: **700 closed / 20 draft / 1,092 pending /
0 unresolved**, mapped to **713 distinct articles: 668 new and
45 reused**. This is not batch or overall review closure.

### Independent initial review and authored reconciliation

Frozen authored commit:
`68a03b7c32e03b23a6aad5ff7edfbde37fa6ea03`.
Fresh isolated **gpt-6.1-sol** and **claude-opus-5.5**
processes reviewed that identical snapshot sequentially. Both
processes fully exited with zero file edits before authoring
resumed. Complete native final messages are archived:
[GPT initial](n2-vocabulary-reviews/batch-36-gpt-initial.md)
and [Claude initial](n2-vocabulary-reviews/batch-36-claude-initial.md).

Both read all twenty new articles, four kanji changes in full
context and twenty mappings, separating all three facets.
GPT reports reading all compact complete comparison families,
69 actual comparison articles, including all 57 distinct direct
targets, and actual public bodies for seven assigned headwords.
Claude read principal/component records and comparison labels,
but only part of the comparison families and few extra bodies;
its public fetches did not yield relevant entries. Claude also
searched wider actual titles and found an uncaptured candidate.
Equal access is not equivalent actual verification depth.

| Report item | Author adjudication before confirmation |
|---|---|
| GPT36-01: missing 姓 link in 氏名 | Addressed: link existing 姓 at the substantive surname comparison. Meaning was already correct. |
| B36-01: 集会/デモ quiz ambiguity | Addressed: add the direct guard and explain protest-rally overlap versus other gathering/demo uses. |
| B36-02: unexplained 洒落た morphology | Addressed: identify the separate ichidan verb, its noun-modifying た-form and おしゃれな. Verify the knowledge-only premise against complete dictionary and actual public entries. |
| Optional 締め切り notice wording | Adopted: closed acceptance can also concern the deadline. Preserve the raw source glosses and selected senses; no universal entry-prohibition rule. |
| Optional thin 締め切る/止す edge | Removed: the actual activity/giving-up label alone does not establish the closing/cutoff meanings. |
| Optional 洒落 English example | Adopted as polish: “This is not a joke.” The previous idiomatic translation was not established as a defect. |
| Optional 締め切り/締め切る edge | Not adopted: noun deadline/closing and verb close up/applications are meaningfully distinguished; stem/co-draw alone is insufficient. |
| Optional 水道 link and other 集会 candidates | Outside required reverse-link scope or not established: distinguish chance encounter, legislative institution and crowd/group from an event. No new baseline-body edit or speculative clique. |

Post-review capture includes **three complete families with
seven senses**. 洒落る1568670 was already in the original
comparison evidence for 洒落る/しゃれる and was checked equal;
only **two families / five senses** are new, for **215 distinct
comparison families / 440 sense records**.
Three actual articles (デモ, 姓, 止す) were read and recorded;
only デモ adds a new label and a new complete-body inspection.
Thus the historical 110 labels/75 complete bodies become
**111 distinct labels / 76 distinct inspected bodies** when
the supplement is included. Original records, declarations,
volumes and rationale remain preserved separately.

Claude's claim that 洒落る was absent from the packet is
incorrect; its report disclosed partial comparison-family
inspection. The useful finding is the unexplained article
construction, not discovery of a missing dictionary family.

Complete 1084000:1 and 1084080:1 support protest/demonstration;
the actual デモ and 集会 labels and parallel peace-event uses
establish the coarse rally ambiguity. Complete 1568670 records
ichidan/intransitive 洒落る. The actual public しゃれる verb
body identifies 下一 and a refined/stylish shop construction
at public sense 2; this is not pinned1568670:2 (joking).
No inferred frequency, new principal verb mapping or N2
assignment is introduced.

**Model-diversity observation:** no specific actionable defect
was shared after inspecting findings, optional observations,
limits and per-file notes in both complete reports. GPT alone
identified the 姓 navigation omission. Claude alone identified
the uncaptured デモ ambiguity and the missing verb explanation;
its optional notice/weak-edge remarks also prompted bounded
refinements. This sample supports complementary inspection
strategies, not a general model ranking or proof that one
family eliminates the other's bias.

Five new articles change. Fifteen new articles, four kanji
edits, all twenty source identities and selected/additional
indices, every baseline word and the TSV/snapshot are unchanged.
Current guards remain **17 cards / 57 directional declarations**:
one added 集会/デモ edge and one removed 締め切る/止す edge.
Original reviewers' bounded confirmations are still pending;
rows remain draft and this is not closure.

### Confirmation and closure

The original **gpt-6.1-sol** and **claude-opus-5.5** sessions
resumed sequentially against corrected committed snapshot
`458105a0a9e6ecb00b0de1a127da4566f49b5bdc`. Both fully
exited with zero file edits. Their complete final messages
are preserved as [GPT confirmation](n2-vocabulary-reviews/batch-36-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-36-claude-confirmation.md).

Both read the actual five-file patch and all five revised
articles, reporting **CLEAN / CLEAN / CLEAN** for correctness,
scoped coverage and comprehensibility. They carry forward,
rather than claim a renewed full inspection of, the fifteen
unchanged articles and four kanji edits. All twenty mappings
remain CLEAN on all three facets; Claude also rechecked the
affected mapping notes.

**GPT36-01, B36-01 and B36-02 are resolved.** Both accept
the direct 集会/デモ safeguard, removal of 締め切る/止す,
the qualified notice wording and the 洒落た explanation.
Both independently retrieved the actual public 洒落る verb
body and distinguished public sense 2 from JMdict1568670:2.
Claude explicitly withdraws its incorrect absence claim:
1568670 was already in the original evidence.
No actionable correction regression or consequential unresolved
claim remains within the assigned scope.

Claude's remaining suggestions are **optional**, not defects:
the style sense's recorded adjectival use could be expanded,
the N2:719 note could additionally name the related verb,
and the notice explanation could add concrete signs.
Current text rejects unrestricted joke-noun use, not every
style-sense construction; it explicitly teaches the verb and
keeps selected/additional indices consistent. The existing
qualification and examples suffice for this scope. The
baseline 水道 backlink remains outside required reciprocal
primary N2 links. None warrants a new baseline-body edit,
changed mapping or speculative quiz guard.

The author authenticated all **four complete final reports**
against the native sessions, exact common prompts, actual
assistant/usage models and zero-edit metrics. Both frozen
snapshots, Git parentage, normalized file hashes, actual patches,
sanitized derivatives and 24 manifest entries per snapshot
were checked. Original evidence is preserved with only the
documented appended supplement; the actual exclusion delta is
exactly +集会/デモ and -締め切る/止す. Named forbidden
report/ledger/note reads were absent from the recorded
read/search requests. These are author-executed provenance
checks, not reviewer-executed Git or linguistic certification.

Closure changes only coverage status and documentation.
The confirmed teaching content and manifest remain unchanged:
**6,569 files**, 396 images and 201 scene catalogs; manifest
version **`c0ea692866bfe14c`**. Structural, baseline-preservation,
reciprocal-link and coverage checks pass. Exclusions remain
**17 guarded articles / 57 directional declarations**.

Closed coverage: **720 closed / 0 draft / 1,092 pending /
0 unresolved**, mapped to **713 articles: 668 new / 45 reused**.
There are still **3,941 word articles** and **164 tracked
primary reciprocal N2 kanji-word pairs**.

**Limits and model-diversity conclusion:** confirmations
inspect the changed scope and carry forward unchanged verdicts.
Neither executes quiz draws or certifies native-speaker
naturalness; public-source access outside the successful verb
retrieval remains limited as described in the reports.
The initial GPT-only navigation catch and Claude-only quiz
and morphology catches remain complementary contributions;
later agreement does not convert them into shared discoveries.
The inaccurate absence premise is withdrawn, not silently
credited as useful new evidence. This batch supports the
value of different inspection strategies, not a model ranking.

## Batch 37 - N2:722-N2:741

**Status:** closed after independent initial reviews,
evidence-based corrections and changed-passage confirmations.

Scope: 住居, 集金, 集合, 習字, 修繕, 重体, 絨毯, 終点,
重点, 就任, 周辺, 重役, 終了, 重量, 重力, 熟語, 祝日,
縮小, 受験 and 主語.

Twenty new articles cover twenty source rows without reuse,
bringing the collection to **3,961 word articles**. Five narrow
kanji edits add reciprocal examples for 周/周辺, 辺/周辺,
了/終了, 量/重量 and 祝/祝日 at their actual readings.
No new kanji or stroke card is introduced.

The [source packet](n2-vocabulary-batch-sources/batch-37.json)
preserves twenty raw source rows and twenty complete principal
families with 26 indexed senses. The captured comparison union
contains **325 distinct complete families / 663 sense records**,
including those twenty principal families, checked equal.
There are therefore **305 nonprincipal families / 637 sense
records**, not 325 additional families. The original capture
has 298 families / 600 senses, and the extra capture adds
27 families / 63 senses with no overlapping entry IDs.
All captured families were inspected.

All 194 original actual labels, the selected デモ label and
supplemental おやすみ/学会 labels were inspected: **197 labels**.
Six selected bundles contain 118 distinct fully inspected
articles, including デモ outside the original label inventory.
With おやすみ and 学会, **120 distinct complete bodies** are
counted as inspected. The complete 194-body aggregate was
captured but not entirely read. All 36 complete component
records and twenty actual public Digital Daijisen containers
were inspected. Machine-computed counts and capture hashes
are author receipts, not independent linguistic certification.

住居 retains residential-address recognition without implying
ownership. 集合 separates meeting up from a mathematical set.
習字 includes pen and brush practice. 修繕 uses attested roof
repair rather than an invented clothes-only boundary.
重体 includes illness or injury and distinguishes 渋滞.
絨毯 separates rare from search-only spellings. 終点 is not
the last train of the day.

重点 selects important-point sense 1 and source-covered colon
sense 3; iteration-mark sense 2 is additional. Its different
public inventory does not establish absence or frequency.
重役 selects company-executive sense 1 at じゅうやく, with
important-role sense 2 additional; obsolete おもやく does not
inherit sense 1. Additional senses receive no independent
N2 assignment.

終了 teaches transitive/intransitive patterns without claiming
successful completion. 重量 preserves the community's raw
“heavyweight boxer” gloss but does not teach it as a licensed
bare-noun meaning: the complete family records only weight.
Separate heavyweight-class terms do not supply a person sense.
重力 is distinguished from weight, mass and broader attraction.
熟語 need not be nonliteral or four characters. 祝日 is not
every personal day off, 縮小 is not automatically data
compression, and 受験 does not guarantee passing.

主語 uses a non-agent property predicate, contextual omission
and an object-topic contrast. Public grammar-source inspection
is bounded: the returned が page was inspected, but only the
first 12,000 returned characters of the は/が comparison were
read. No claim is made about the unread remainder or every
grammatical framework; no archived response hash is available
for those two grammar fetches.

Missing primary 修/繕/絨/毯/就/熟/縮 remain in metadata without
links. Alternate 態 is also unlinked. No baseline word ID,
primary reading, title, level, body or exclusion is changed.
Sixteen new cards declare **81 directional quiz exclusions**,
subject to independent assessment of actual ordinary meanings,
not a transitive synonym grouping.

Both reviewers received the same frozen committed
snapshot, twenty complete new articles, five narrow kanji
changes, twenty mappings, rubric and source access. The blind
derivative removes only `quizGuardRationale`. Reviews run
sequentially without nesting, concurrent reviewers or author
edits during the initial reviews.

Authored coverage: **720 closed / 20 draft / 1,072 pending /
0 unresolved**, mapped to **733 distinct articles: 688 new /
45 reused**. This is not review closure or overall completion.

### Initial reviews and reconciliation

The complete native final messages are archived:
[GPT](n2-vocabulary-reviews/batch-37-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-37-claude-initial.md).
Actual models were **gpt-6.1-sol** and **claude-opus-5.5**,
run strictly sequentially on authored commit
`fa390bf5776402ca8a27fac55cb75990d1f37b1d`. Both processes
exited with zero edits. Session events authenticate the exact
common prompt, selected and actual models, permitted tools,
and absence of named forbidden reads. File-only reviewers
could not independently execute Git or hash checks.

Both inspected twenty articles, five kanji changes and twenty
mappings. GPT inspected all 325 captured families, 36 component
records, 197 labels, seven complete existing articles and nine
actual public lexical containers. Claude inspected the twenty
principal families and labels, but not most comparison families
or component records; its only successful independent lexical
check was 重点. Its failed 住居 lookups supplied no evidence.
These unequal actual inspection scopes limit model comparisons.

Author adjudication, pending changed-passage confirmation:

| Finding | Adjudication |
| --- | --- |
| GPT-01: 住居/宿 | **Resolved:** add the direct safeguard and a qualified comparison. Complete 宿1337190:2 explicitly includes home/dwelling despite the travel-focused existing title. |
| GPT-02 / Claude-04: 集金/コレクション | **Resolved:** add the direct safeguard for the unqualified English collection/collecting label; retain the Japanese payment-versus-hobby distinction. |
| GPT-03 / Claude-02 extra: 終点/仕舞い | **Resolved:** add the direct end/finish-label safeguard. This observation is shared even though Claude placed it in a lower-confidence extra. |
| GPT-03: 終点/終わる | **Resolved:** add the direct end/finish-label safeguard; do not claim unrestricted noun/verb substitution. |
| GPT-04 / Claude-05: 終了/結論 | **Resolved:** add the direct conclusion-label safeguard; retain the reasoned-conclusion distinction. |
| GPT-04: 終了/閉める・閉まる | **Resolved:** add both broad close-label safeguards, without teaching physical shutting as synonymous with ending every activity. |
| Claude-01: 住居 address demonstration | **Resolved:** remove address from the title and unrestricted-use claim; keep it as explicitly qualified JMdict recognition. Replace the example with the already attested 住居を定める pattern. The original mapping note now denotes that qualified recognition, not verified address-field substitution. |
| Claude-02: 終点/終了・端 | **Resolved:** add both safeguards and explain point versus activity and broader edge/end. The complete 端1581610:1 explicitly includes the end of a street, strengthening the tentative extra. |
| Claude-03: 周辺/郊外 | **Resolved:** add the direct outskirts safeguard and distinguish the city's center from an arbitrary reference point. |
| Claude-05: remove 終了/切る・切れる | **Partially resolved:** the conclusion omission is fixed, but proposed removals are not adopted. Actual 切る teaches hanging up, supported by 1384830:4; 切れる teaches expiry, supported by 1384860:6. Await confirmation of this evidence-based disagreement. |
| Claude optional remarks | **Optional:** no further 集合, 受験 or 熟語 changes. No actionable defect was established from generous gathering guards, an action/object distinction, or learners blurring idiom and proverb. No 宛名 guard is added after removing address from 住居's title and qualifying its recognition note. |

The correction capture contains 21 complete families: thirteen
repeats checked equal and **eight genuinely new families /
twenty senses**, including separate readings of 端 which are
not pooled into はし. The combined inventory is **333 distinct
families / 683 senses**, including the unchanged twenty
principal families / 26 senses. Four additional existing full
bodies (宛名, 端, 諺, 郊外) and two additional existing labels
(諺, 郊外) bring the inspected totals to **124 bodies /
199 labels**. The correction capture also contains the new
principal 終了 article, not counted as an existing article.
Original capture counts, declarations and rationale remain
unchanged; the source packet appends a correction supplement.

Five new cards change. Fifteen other new cards, all five kanji
edits, all raw source fields and all twenty mapping identities
and sense indices remain unchanged. Ten direct declarations
are added and none removed: **16 guarded cards / 91 directional
declarations**. Baseline word cards remain unchanged.

**Preliminary model-diversity evidence:** verified shared
observations are 集金/コレクション, 終点/仕舞い and 終了/結論.
GPT uniquely supplied 宿's dwelling sense, the 終わる endpoint
label, and both closing labels. Claude uniquely supplied the
address-demonstration remedy, 郊外, and the 終了/端 endpoint
precautions. Its proposed cut/expiry removals are not credited
as useful corrections. This compares all report sections,
including tentative extras, and supports complementary
inspection strategies on this sample, not a model ranking.

### Corrected-snapshot confirmation and closure

The complete native confirmation messages are archived:
[GPT](n2-vocabulary-reviews/batch-37-gpt-confirmation.md) and
[Claude](n2-vocabulary-reviews/batch-37-claude-confirmation.md).
The original reviewer sessions resumed strictly sequentially
on corrected commit
`916247bf6bbf7ffca6ba1cddc2ff2608f6b610b0`, using actual
models **gpt-6.1-sol** and **claude-opus-5.5**. Both exited
with zero edits. All five changed articles are **CLEAN** for
correctness, scoped coverage and comprehensibility. Both
carry forward the unchanged fifteen articles and five kanji
edits, rather than claiming a fresh complete rereview.
All twenty mapping verdicts are CLEAN; N2:722 was reassessed
against the narrower address qualification.

All four original GPT findings are **resolved**. Claude's
B37-01 through B37-04 are **resolved**, including its
lower-confidence endpoint extras. For B37-05, the 結論
omission is **resolved** and the proposed removal of
切る/切れる is **withdrawn**: both actual articles teach the
relevant termination/expiry meanings. GPT also accepts that
evidence-based retention. This closes the earlier partial
adjudication without rewriting either original report.
No new actionable defect or consequential unresolved claim
remains in the reviewed scope.

GPT reread all five changed articles, the complete 21-family
correction rendering, relevant principal records and thirteen
existing comparison articles. Claude read the five changed
articles, complete correction rendering and five existing
comparison articles; six other comparison checks used titles
and exclusion lines. These are different inspection scopes,
not identical complete dictionary audits.

住居 now demonstrates the attested 住居を定める pattern and
keeps JMdict's address gloss only as qualified dictionary
recognition, not free substitution for 住所 on forms or in
address questions. GPT reused its initially inspected
Daijisen evidence. Claude's new public lookups failed or
returned encyclopedia text, so its attestation assessment
relies on the author's earlier receipt and its own language
judgment. Claude's suggestion to reword the original mapping
note remains **optional**; both accept the unchanged note
only in the explicitly qualified sense. No source field,
mapping identity or sense index is changed at closure.

Author-executed authentication verifies all four complete
native final messages, exact common prompts, actual models,
zero edits, permitted tools and absence of named forbidden
reads. Both frozen snapshots, patches, sanitized derivatives,
append-only correction evidence and 25 manifest content
entries per snapshot were checked. These executable provenance
checks do not convert the file-only reviewers' receipt
assertions into independent Git/hash checks.

Closed coverage is **740 closed / 0 draft / 1,072 pending /
0 unresolved**, mapped to **733 distinct articles: 688 new /
45 reused**. There are **3,961 word articles** and **169 tracked
primary reciprocal N2 kanji-word pairs**. Closure leaves the
confirmed teaching content, five kanji edits and manifest
unchanged. The expansion as a whole is still incomplete.

**Final model-diversity conclusion:** the shared and unique
verified contributions above remain complementary. Later
agreement on corrections does not make an original discovery
shared; the withdrawn removal proposal is not credited as a
useful correction. Comparing all report sections prevents
misclassifying Claude's tentative extras as GPT-only catches.
This batch supports different inspection strategies, not a
general ranking of model families. Neither confirmation
executes quiz draws or certifies exhaustive linguistic
correctness or native-speaker naturalness.

## Batch 38 - N2:742-N2:761

**Status:** closed after sequential independent review,
evidence-based corrections and original-reviewer confirmations.

Scope: 出勤, 述語, 出張, 寿命, 主役, 受話器, 循環, 巡査,
順々, 順序, 純情, 純粋, 消化, 小学生, しょうがない, 将棋,
蒸気, 定規, 上級 and 商業.

Nineteen new articles and reuse of 定規 cover twenty source
rows, bringing the collection to **3,980 word articles**.
The reused article receives only the sourced explicit
`jlpt: 2` assignment; its identity, primary reading, title,
body and other metadata are preserved. Six narrow kanji
edits add eight reciprocal pairs: 述/述語 at ジュツ,
査/巡査 at サ, 順/順々 and 順/順序 at ジュン,
純/純情 and 純/純粋 at ジュン, 将/将棋 at ショウ,
and 蒸/蒸気 at ジョウ. Existing plain examples for 純粋,
将棋 and 蒸気 become links rather than duplicates.
No new kanji or stroke card is introduced.

The [source packet](n2-vocabulary-batch-sources/batch-38.json)
preserves twenty raw rows and twenty complete principal
families with **31 indexed senses**. The comparison union
contains **308 distinct complete families / 694 senses**,
including those twenty principals checked equal, leaving
**288 nonprincipal families / 663 senses**. The original
capture has 247 families / 540 senses; the supplemental
58-family capture has 140 senses and repeats two families,
checked equal. Four nuisance/commute families add 13 senses;
one gas family adds eight. The requested-form union is 261.
All complete captured families were inspected.

All 143 original and 33 supplementary labels, plus seven
additional labels, were inspected: **183 labels**.
The twelve selected bundles capture 89 bodies, but only the
explicitly inventoried 53 bodies were fully read. With 定規
and seven additional nuisance/commute/processing/gas articles,
**61 distinct complete existing bodies** were inspected.
The original 143-body aggregate was not all read. All 47
complete component records and 21 actual public lexical
retrievals were inspected. Hashes and counts are author
receipts, not native-speaker certification.

出勤 separates reporting/attendance from generic employment.
述語 uses verb, adjective and noun-plus-copula predicates,
with explicit school-grammar limits; grammar sense 1 is the
editorial anchor and logic sense 2 additional recognition,
not a claim that the raw predicate gloss disambiguates them.
出張 is work travel without an overnight minimum.
寿命 selects lifespan sense 1 and adds service-life sense 2.
主役 covers role and performer; its public figurative
extension is not assigned an invented pinned sense index.
受話器 is a receiving device, not the entire phone call.

循環 explains route-marker を with an intransitive verb.
巡査 retains both the lowest-rank and broader officer uses.
順々 teaches に and the iteration mark; 順序 covers sequence
and procedure, not commands or purchases. 純情 preserves but
does not adopt the unsupported raw devotion gloss. 純粋
covers material and mental purity rather than hygiene alone.
消化 anchors food sense 1, adds information/workload senses
2-3 and explicitly qualifies archaic sense 4.
小学生 names a pupil, not a building or a universal age.

しょうがない preserves the blank raw kanji and English fields.
Sense 2 is an explicit dictionary-backed editorial anchor,
not recovered compiler intent; senses 1 and 3-5 are additional.
The actual Bunpro page supports verb て, い-adjective くて
and な-adjective で attachment. The failed CAPTCHA and 404
retrievals provide no grammar evidence. No unverified
productive ようがない comparison is taught. That positive
grammar inspection has no archived response hash.

将棋 keeps its whole reading and the attested 将棋を指す
expression without inventing ギ as a standalone 棋 reading.
蒸気 is not water-only; transport sense 2 is an additional
abbreviation, not labeled archaic without evidence.
定規 does not import the separate public ていき heading.
上級 teaches a noun/の-modifier, not an automatic な form.
商業 is commercial activity, not a company by default.
Additional senses do not independently acquire N2 status.

Missing primary 張/寿/器/循/環/巡/序/粋/棋/級 remain in metadata
and plain text. Sixteen new cards declare **82 directional
quiz exclusions**, pending independent assessment. Guards
consider actual ordinary meanings, including 通う's circulation,
警察's officer and 清潔/きれい's moral-purity senses; they are
not transitive topic groupings.

Both reviewers will receive the same frozen committed
snapshot, nineteen new articles, the narrow 定規 change,
six kanji changes, twenty mappings, rubric and source access.
The blind derivative removes only `quizGuardRationale`.
Reviews run strictly sequentially without nesting,
concurrent reviewers or substantive author edits.

Authored coverage: **740 closed / 20 draft / 1,052 pending /
0 unresolved**, mapped to **753 distinct articles: 707 new /
46 reused**. There are **177 tracked primary reciprocal
N2 kanji-word pairs**. This is not review closure or overall
completion.

### Initial reviews and prepared corrections

Authored snapshot:
`4ec7f6f7dabbe669a42d686fbd9ada6da362326a`
(parent `368da250ef323ddef1609a7e0789a59c093fb6a7`).
Native **gpt-6.1-sol**, then **claude-opus-5.5**, reviewed
strictly sequentially with the same frozen prompt, scope,
source access and blind derivative. Both processes exited
before author corrections began. The complete native final
messages are archived, without replacing them with this
summary:
[GPT initial](n2-vocabulary-reviews/batch-38-gpt-initial.md)
and [Claude initial](n2-vocabulary-reviews/batch-38-claude-initial.md).

Both read all nineteen new articles, all twenty mappings,
the narrow 定規 reuse and six related kanji cards/patch.
Their actual evidence inspection differed. GPT reports
reading the complete comparison renderings and exclusion
targets; Claude reports targeted comparison records,
about 120 existing labels/exclusions and a keyword title
scan. Neither report is a claim that both independently
read every captured existing body or executed Git/hashes.

| Initial observation | Evidence-based reconciliation prepared for confirmation |
| --- | --- |
| GPT F01: 消化/詰める quiz ambiguity | Accept a direct safeguard. 詰める 1226510:5 and its existing details-resolution example support the broad "working through" label. This is not unrestricted substitution in Japanese. |
| Claude B38-QZ-01: 順々/どんどん | Accept a direct safeguard. Actual titles and 1009320:3 express succession; do not infer protection transitively through 次々. |
| GPT F02; Claude B38-LNK-01/02/03 | Link 小学校, 先輩 and 指す at substantive introductions/comparisons. |
| GPT F02; Claude optional 打つ | Link 打つ at the playing-verb comparison. This is shared initial signal, not a GPT-unique discovery merely because Claude labeled it optional. |
| Claude B38-MAP-01: N2:750 attribution | Clarify the sole pinned glosses as in order/in turn and attribute the additional succession rendering to the inspected Japanese entry. Raw CSV fields, identity, reading, level and selected index do not change. |
| Claude optional だめ safeguard | Accept after complete-family inspection: 1409110:1 "no good" and :2 "hopeless" overlap the しょうがない family. Its ordinary sense 2 matters even though the existing card selects 1/3/5. This does not equate prohibitions. |
| Claude optional 仕方, 碁 and 話 links | Add small navigation improvements at existing comparisons; complete target bodies and applicable families were inspected. |
| Claude optional vapor/vapour unification | Decline: both English spellings are standard; no unrelated existing kanji wording change is needed. |
| Claude's other-components N3-or-easier statement | Do not adopt this unsupported generalization. The eight actual reciprocal N2 pairs are checked against existing cards; missing primary cards establish no easier vocabulary or kanji level. |

The correction extraction contains **12 complete families /
55 senses**. Four families were already present and checked
equal; **eight new families / 41 senses** bring the union
to **316 complete families / 735 senses**. All twelve
correction families and ten complete existing bodies were
actually inspected. Six fresh labels bring the distinct
label inventory to **189**; eight additional full bodies
bring the author-inspected body union to **69**.
These are author inspection counts, not a replacement for
each reviewer's disclosed scope.

The source packet preserves original capture counts,
declarations and author rationale and appends the correction
evidence. It retains the original N2:750 mapping notes in
that supplement while clarifying the live mapping/TSV notes.
The three added direct guards are 消化/詰める,
順々/どんどん and しょうがない/だめ: **16 guarded new
cards / 85 directional declarations** now, compared with
the frozen initial **16 / 82**. No title or source-selected
sense changes. Seven new articles change; the other twelve,
the six kanji edits and narrow 定規 change remain untouched.
Coverage remains **740 closed / 20 draft / 1,052 pending /
0 unresolved** until confirmations and closure.

Model-diversity observation for this sample: GPT uniquely
raised the verified 消化/詰める collision. Claude uniquely
raised the verified 順々/どんどん collision, the mapping
attribution clarification and optional だめ/navigation
improvements. Four substantive link observations are
shared across findings and optional sections. The declined
English spelling preference and unsupported component-level
generalization are not credited as useful catches.
This is not a model benchmark; initial scope and source
inspection differed, and later agreement will not be counted
as shared initial discovery.

### Original-reviewer confirmations and closure

Correction snapshot:
`f3fb61f8589e4a233a0bdf518eb6198fa20e88f6`
(parent `4ec7f6f7dabbe669a42d686fbd9ada6da362326a`).
The original GPT session
`7bfc40d4-f76f-4b94-80ec-220dbb5ee41c` confirmed first;
the original Claude session
`68f242f9-23a6-480e-a6fb-ad30da9267b0` confirmed after
that process exited. No concurrent reviewer or substantive
author work occurred. Actual models remained **gpt-6.1-sol**
and **claude-opus-5.5**. Complete native final messages,
including introductory paragraphs, are archived:
[GPT confirmation](n2-vocabulary-reviews/batch-38-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-38-claude-confirmation.md).

Both original reviewers mark all seven corrected cards and
the N2:750 clarification **CLEAN / CLEAN / CLEAN** for
correctness, scoped coverage and comprehensibility. The
twelve unchanged new articles, six unchanged kanji edits,
narrow 定規 change and nineteen unchanged mappings inherit
their initial bounded assessments; they were not freshly
reviewed. Neither confirmation establishes an actionable
defect or consequential unresolved teaching claim.

| Observation | Final disposition |
| --- | --- |
| GPT F01; Claude B38-QZ-01 | Resolved: both reviewers accept the direct 消化/詰める and 順々/どんどん safeguards. Later agreement is not shared initial discovery. |
| GPT F02; Claude B38-LNK-01/02/03 and optional 打つ | Resolved: all four substantive destination links accepted. |
| Claude B38-MAP-01 | Resolved: pinned English glosses and the additional source-supported succession paraphrase are distinguished. |
| Claude optional だめ, 仕方, 碁 and 話 | Adopted and accepted by both original reviewers. |
| Claude confirmation citation precision | Accepted evidence-only clarification: 1409110:1 overlaps 1305510:3 in no-good/useless meaning; 1409110:2 overlaps 1305510:4 in hopeless meaning. The packet appends this qualification without rewriting the original reviewed correction evidence. No guard or teaching changes. |
| Claude component-level generalization | Withdrawn explicitly as unsupported; no easier level is inferred from missing cards. |
| Claude vapor/vapour suggestion | Withdrawn as an unnecessary spelling preference. |
| Claude confirmation optional prose contrasts | Remain optional: existing wording and direct guards already address the demonstrated ambiguities. No expanded contrast assignment. |
| Claude optional existing 打つ go sense | Remains outside the narrow reuse scope: 将棋 teaches the expression and 碁 already teaches 碁を打つ; no demonstrated new-card defect requires altering the baseline article. |

GPT reports reading all seven changed cards, twelve complete
correction families and ten complete destination/comparison
bodies. Claude reports the seven changed cards, all twelve
compact complete families and eight complete target bodies;
it checked 小学校/先輩 titles and existence without rereading
their bodies. GPT reached the relevant actual Daijisen
entry through raw HTML. Claude reached only its summary,
and its Kotobank attempt returned 404; do not count that
as a second full-entry inspection. The author's original
actual public lexical capture remains available.

Author-executed provenance checks authenticated exact native
prompts, actual models, original sessions, complete final
messages, restricted tools/no named forbidden reads, zero
edits, snapshot/patch hashes and blind derivative equivalence.
The initial derivative omits only `quizGuardRationale`;
the correction derivative preserves initial evidence and
appends its supplement. Twenty-six manifest content entries
were checked against each committed review snapshot.

| Complete final-message archive | LF-normalized SHA-256 |
| --- | --- |
| GPT initial | `df52ec991add1335bdee2793dc552dbbccb1000423b8820a549b6b9ce596733b` |
| Claude initial | `4124daf7a3fd02f7c1031b00ae6eb4c348ee5a12f26a607fbe3072b44d62c36b` |
| GPT confirmation | `6906cb4b69a1848460e4c44ffec6af8c43d2c3ed9fdc42ee5d5ee7c2580868ab` |
| Claude confirmation | `535b5a1da6d504982c9afcaa90abdb32afee1ebe448dbdf7155cc5dc8757d07a` |

Closure changes only statuses, coverage bookkeeping, this
reconciliation, the appended evidence-note qualification,
lessons and complete confirmation archives. No teaching,
kanji example, title, reading or exclusion changes after
the confirmed correction. The deterministic manifest stays
**`37e514b46e275909`**, with **6,608 assets:
6,011 files / 396 images / 201 scenes**.

Coverage is now **760 closed / 0 draft / 1,052 pending /
0 unresolved**, mapped to **753 distinct articles:
707 new / 46 reused**. There are **3,980 word articles**
and **177 tracked primary reciprocal N2 kanji-word pairs**.
The 3,273 baseline identities, readings, titles and
exclusions remain preserved under the recorded narrow
level/reuse rules.

The models' complementary initial catches remain useful on
this sample; Claude additionally caught the small author
citation precision during confirmation. These are
sample-specific observations with different disclosed
inspection depths, not a model-family benchmark.
Provenance and structural checks are author-executed,
not reviewer-executed Git, production quiz draws,
exhaustive linguistic validation or native-speaker
certification. Overall N2 vocabulary expansion remains open.

## Batch 39 - closed

Twenty consecutive community-list rows **N2:762-N2:781**
are drafted on parent
`7b18d016f6228355b174ee61f992abb29c706342`.
Eighteen original articles are new; existing 上下 and 商店
gain only a sourced explicit `jlpt: 2` assignment. Their
identities, primary readings, titles, teaching bodies and
other metadata are preserved.

| Source ID | Article | Selected pinned senses | Additional senses |
| --- | --- | --- | --- |
| N2:762 | 消極的 | 1350220:1 | - |
| N2:763 | 賞金 | 1351930:1 | - |
| N2:764 | 上下 | 1352710:1,2 | 1352710:4,6 |
| N2:765 | 障子 | 1352090:1 | - |
| N2:766 | 商社 | 1347080:1 | - |
| N2:767 | 乗車 | 1355270:1 | - |
| N2:768 | 上旬 | 1353410:1 | - |
| N2:769 | 生ずる | 1378660:1,2 | - |
| N2:770 | 小数 | 1348370:2 | 1348370:1 |
| N2:771 | 商店 | 1347180:1 | - |
| N2:772 | 焦点 | 1350810:1,2 | 1350810:3 |
| N2:773 | 消毒 | 1350270:1 | - |
| N2:774 | 勝敗 | 1346220:1 | - |
| N2:775 | 蒸発 | 1356960:1,2 | - |
| N2:776 | 賞品 | 1351960:1 | - |
| N2:777 | 勝負 | 1346230:1,2 | - |
| N2:778 | 小便 | 1580280:1 | 1580280:2 |
| N2:779 | 消防署 | 1350370:1 | - |
| N2:780 | 正味 | 1377980:2 | 1377980:1,3,4 |
| N2:781 | 正面 | 1378030:1 | - |

The [source packet](n2-vocabulary-batch-sources/batch-39.json)
keeps raw source fields separate from these selections.
Additional senses do not independently acquire N2 status.
Broad source glosses are qualified rather than silently
rewritten: 小数 is taught through mathematical decimal
notation, and 消毒 does not promise complete sterility.
生ずる acknowledges the two dictionaries' different
classification frameworks and supplies actual inflected
forms. Public alternate headings are not transferred into
the reused 上下 or the new 正面 article.

Author inspection covers **241 complete families / 556
sense records**, including the **20 principal families /
35 senses** checked equal, not counted twice. The original
selection was 239 / 552; the final ドア and 大会 supplement
adds two complete families / four senses. The broader
original 412-family / 1,117-sense capture is not all
inspected; 173 of those families remain capture-only.
All 230 original comparison labels and the supplemental
actual ドア label were inspected, giving **231 labels**.
All 72 selected full existing bodies and the complete
ドア / 大会 bodies were read: **74 full bodies**, not every
body in the 230-card capture. All **33 complete component
records** were inspected.

There were **25 actual Daijisen lexical retrieval
inspections** from 26 requests. 正面切って had no extracted
actual lexical body and is not positive verification.
Unmatched exact JMdict requests for 揚げ下ろし and 正しさ
are retained without claiming those forms are invalid.
The separately archived MHLW evidence covers only its
消毒 / 除菌 definition section, not its full page,
product instructions or a formal 滅菌 standard.
The original capture-stage pending-inspection plan remains
unchanged; a later receipt records completed inspections.

Seven reciprocal pairs are added at the actual reading
rows and in Common words on six N2 cards:
極 / 消極的 at キョク; 賞 / 賞金 and 賞品 at ショウ;
毒 / 消毒 at ドク; 蒸 / 蒸発 at ジョウ;
署 / 消防署 at ショ and 防 / 消防署 at ボウ.
Their metadata is unchanged. No kanji or stroke files
are added.

Initial quiz declarations comprise **15 guarded new
articles / 42 directional declarations**. These are
author hypotheses, not review conclusions. Direct ordinary
meanings and actual labels govern the symmetric,
nontransitive relation; neither homophony nor an inferred
transitive clique suffices. The blind evidence derivative
removes only `reviewEvidence.quizGuardRationale`.

Structural and author-executed checks establish **760
closed / 20 draft / 1,032 pending / 0 unresolved** rows,
mapped to **773 distinct articles: 725 new / 48 reused**.
There are **3,998 word articles** and **184 tracked primary
reciprocal N2 kanji-word pairs**. The **3,273 baseline**
identities, readings, titles and exclusions remain preserved
under the recorded narrow level/reuse rules.
The deterministic manifest is **`bf8090b9833357dd`**:
**6,626 assets = 6,029 files + 396 images + 201 scenes**.

Independent GPT and Claude reviews and evidence-based
reconciliation were pending at the authored snapshot. A valid draft or authored
commit is not review closure; no model-diversity conclusion
was claimed at that stage. Overall expansion remains open.

### Initial independent reviews and bounded corrections

Authored commit **`d04bcfce3419f3bea7158281ff32ba65f32ffdad`**
was frozen before review. The complete native reports are
[GPT initial](n2-vocabulary-reviews/batch-39-gpt-initial.md)
and [Claude initial](n2-vocabulary-reviews/batch-39-claude-initial.md).
The isolated **`gpt-6.1-sol`** process completed before
**`claude-opus-5.5`** began; neither overlapped author work
or the other reviewer. Both made zero edits. Native prompts,
actual models, complete final messages, tool restrictions,
named forbidden-read absence, usage and the common committed
snapshot were authenticated by the author.

Both reviewed all eighteen new articles, both narrow reuses,
the six kanji edits and twenty mappings. Their evidence
depth differed: GPT reported reading the complete supplied
241-family comparison union and label inventory, whereas
Claude explicitly used selected comparison bodies and
thirteen supplied public lexical bodies, not most evidence
JSON or the complete captured inventory. Claude also
independently retrieved the relevant MHLW and Kotobank
definitions; its unsuccessful or unrelated lookups remain
disclosed limits. This is not a controlled model ranking.

The author inspected all **19 complete correction families /
62 senses** and thirteen complete existing target bodies.
Nine duplicate families were checked equal; **10 additional
families / 35 senses** bring the inspected union to **251
families / 591 senses**, not 260 / 618. The current distinct
label and fully inspected existing-body totals are **239**
and **84**. Original reviewed evidence, mappings, initial
declarations and author rationale remain unchanged; the
packet appends the correction supplement. The confirmation
derivative again removes only the original quiz rationale.

Accepted corrections are:

- **Shared:** add direct 障子 / 戸 and 上旬 / 始まり quiz
  safeguards. Their protection cannot be inherited through
  ドア or 始め. Link 商社's substantive 輸入 introduction;
  this was a GPT finding and a Claude optional observation.
- **GPT-specific initial signal:** correct 賞品's 商品
  comparison ID from 1347190 to **1347310**; add substantive
  links to 開ける, 閉める, 生きる, the word article 便 and
  除く. Linking 便 preserves its stated びん contrast.
- **Claude-specific initial signal:** add 蒸発 / 無くなる
  and 生ずる / 原因 guards; replace 焦点's unsupported
  negative historical claim with its cited dictionary's
  naming explanation; display 起こす while preserving the
  stable `起す.md` target. Also adopt Claude's optional
  生ずる / 及ぼす guard after complete-family inspection.

These are direct English-label/ordinary-sense safeguards,
not claims of unrestricted Japanese substitution. 原因 is
a noun, 及ぼす has its own effect collocations, and the
無くなる pair does not make every use appropriate for a
person's unexplained disappearance. The retained beginning
guards do not redefine 上旬 as any unspecified beginning.
The current total is **15 guarded new cards / 47
directional declarations**; no baseline exclusions changed.

Claude's optional replacement of 小便's grammatical medical
test example was declined as a register optimization, not
a demonstrated factual defect: the article already names
尿 as common in medical/formal use. Suggested baseline
生じる / 戸 body expansions remain outside this batch.
Harmless conservative トイレ / 面 guards were not removed.

Model diversity was useful here: the source-grounded 焦点
correction and additional disappearance/cause overlaps were
not in GPT's initial report, while the incorrect 商品 ID
and several navigation targets were not in Claude's report.
The 輸入 link is shared signal even though its report
classification differs. Evidence depth and optionality
remain part of that observation; no superiority or measured
bias-reduction claim follows from this batch.

Nine new-card bodies changed; all identities, readings,
titles, selected sense indices and twenty row mappings
remain unchanged. The two level-only reuses and all six
kanji edits are untouched. Author checks retain **760
closed / 20 draft / 1,032 pending / 0 unresolved**, **3,998
word articles**, **184** tracked reciprocal pairs and the
**3,273** baseline identities under recorded exceptions.
The corrected deterministic manifest is **`38bd03a182b321be`**,
with unchanged asset counts. Bounded confirmations in the
original reviewer sessions remain pending; these rows are
not closed yet.

### Confirmation and closure

Correction commit **`bf21b1059519c5bf65df5fc051acba0cfa6ae761`**
was frozen with the nine-card patch and identical bounded
confirmation prompt. The original GPT session completed
before the original Claude session resumed; neither
overlapped author work or another reviewer. Their complete
native reports are [GPT confirmation](n2-vocabulary-reviews/batch-39-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-39-claude-confirmation.md).

Both re-read all nine corrected articles and the complete
nineteen-family correction rendering, accepted the fixes
and found no consequential remaining issue. Their unchanged
content assessments inherit the initial reviews. GPT
re-read all thirteen actual destination bodies; Claude
read six in full and selected front matter/citations for
others, retaining earlier full-body context where stated.
Neither re-read the whole 251-family/591-sense inventory
or 239-label inventory, nor executed Git, hashes, validators
or live quiz draws. Public corroboration in confirmation
used retained captures/initial fetches, not fresh retrievals.

Claude's scope list names 原因 as both a full-body re-read
and carried-over-only. The actual successful native
unbounded view returned its complete body
in confirmation. The archive is preserved unchanged; the
source packet appends this author-verified scope
clarification. It does not change learner content.
Both reviewers accepted the retained 小便 example; other
baseline improvements remain optional and out of scope.

All **four complete reports** were authenticated against
native final events, exact prompts, actual models and
usage, restricted tools, named forbidden-read absence,
zero edits and both committed content/evidence snapshots.
Original blind derivatives still differ from their
respective packets only by the original quiz rationale.
These are author-executed provenance checks, not
reviewer-executed Git verification.

Normalized SHA256 values of the complete archived reports:

| Report | SHA256 |
| --- | --- |
| GPT initial | `99296348c0da50b474b111c5dc273059a6338de59278f460a9e4a84e763d43a1` |
| Claude initial | `21fa2bdc0c129e6aafd951b23362671356b172588bccbf561906b8bc2d32c2c7` |
| GPT confirmation | `22be79a9fa1adef9373b5f80a6651e1c6d4ee78b6dff64b523c35944e143a5c9` |
| Claude confirmation | `248be50c200bb96bc2628b288d454aa36abe85b4c2b5ccc81534c9c9f1ee5126` |

Exactly twenty rows **N2:762-N2:781** close without changing
their raw fields, mappings or sense indices. Closure
changes only documentation, statuses, snapshot/index
metadata and confirmation evidence/archives. All confirmed
teaching, both narrow reuses, six kanji edits and manifest
**`38bd03a182b321be`** remain unchanged.
Coverage becomes **780 closed / 0 draft / 1,032 pending /
0 unresolved**, still mapped to **773 distinct articles:
725 new / 48 reused**. There remain **3,998 word articles**,
**184** tracked reciprocal N2 pairs and **3,273** preserved
baseline identities under the recorded exceptions.
This closes batch 39, not the overall vocabulary expansion.

## Batch 40 - closed after independent reviews

Source rows **N2:782-N2:801** cover 消耗, 醤油, 省略, 初級,
助教授, 食塩, 職人, 初旬, 書籍, 食器, ショップ, 書店,
書道, 白髪, 知合い, シリーズ, 私立, 資料, 汁 and 素人.
The [source packet](n2-vocabulary-batch-sources/batch-40.json)
preserves all raw fields separately from teaching identities
and one-based sense selections. This is the named community
list, not an official modern JLPT syllabus.

There are **16 new articles and four narrow reuses**.
しょうゆ retains its stable kana ID, reading, title, N5
level, empty kanji array and teaching. Its existing 醤油
explanation gains only the 油 link and the applicable ユ
reading. 書籍, 書店 and 資料 gain only sourced `jlpt: 2`;
their bodies and other metadata, including 書籍's seven
quiz exclusions, remain unchanged.

The canonical 知り合い article explicitly recognizes raw
知合い without equating its search-only dictionary flag
with invalidity or comparative frequency. 白髪 teaches the
documented white/gray-hair meaning; the raw bleaching gloss
is not promoted to a separate unsupported sense. 素人 uses
the whole-word irregular reading, not invented constituent
readings. 汁 selects the applicable しる juice/sap and
soup/broth senses; the つゆ-only dipping-sauce sense is not
transferred to しる or to the restricted alternate 液.

助教授 is explicitly historical. The actual inspected
Daijisen body supplies the April 2007 change to 准教授;
the separately inspected MEXT proposal explains reform
and distinct 助教 / 助手 roles, not its implementation date.
Other scoped distinctions include 初級 as a level rather
than a beginner person, 食器 including eating implements,
初旬 as days 1-10 inclusive, and skilled amateurs remaining
possible under 素人.

The inspected dictionary union is **121 complete families /
230 sense records**, including **20 principal families /
25 senses**, checked equal rather than added twice.
It comprises the original selected **111 / 200** and the
additional **10 / 30**. All **111 distinct existing labels**
and **66 complete existing bodies** were inspected:
59 selected bodies plus seven additional bodies.
The broader capture contains **209 families / 386 senses**
and 104 bodies; it was not all read. The original
capture-stage pending-inspection accounting is preserved,
with a separate completed-inspection receipt.

All **34 complete component records** and **26 actual
Digital Daijisen lexical-body retrievals** were inspected,
distinguishing separate headings and reading restrictions.
The actual 181-line fetched MEXT representation was read
separately. These are author inspections and retained
captures, not fresh independent-reviewer retrievals or
native-speaker certification.

Four N2 kanji cards change, without metadata changes.
省 / 省略 at ショウ, 略 / 省略 at リャク and 塩 / 食塩
at エン add three new-article reciprocal pairs. 油 gains
reused しょうゆ at ユ. Each is linked in its actual reading
row and Common words. Existing 籍 already reciprocally
links reused 書籍 at セキ; it needs no edit. No kanji or
stroke cards are added. Reused pairs are checked explicitly
outside the generic new-article-only reciprocal audit.

Initial quiz declarations comprise **11 guarded new
articles / 34 directional declarations**. These are author
hypotheses, not reviewer conclusions. Direct ordinary senses
and actual labels govern symmetric, nontransitive guards.
Exact equal titles already separate 初旬 / 上旬 and
ショップ / 店. No baseline exclusions change. The blind
evidence derivative removes only
`reviewEvidence.quizGuardRationale`.

Author checks establish **780 closed / 20 draft / 1,012
pending / 0 unresolved** rows, mapped to **793 distinct
articles: 741 new / 52 reused**. There are **4,014 word
articles** and **187 tracked new-article reciprocal N2
pairs**, with the two reused relationships verified
separately. The **3,273 baseline** identities, readings,
titles and exclusions remain preserved under the recorded
narrow level/reuse rules. The deterministic manifest is
**`58f07e0cea999d04`**: **6,642 assets = 6,045 files + 396
images + 201 scenes**.

The authored snapshot and its counts above are preserved
as the initial state. A valid draft or authored commit is
not review closure; the overall expansion remains open.

書店 was already committed entirely with CRLF. Its exact
byte delta inserts only `jlpt: 2` with the same line ending.
The whitespace check permits CR-at-EOL for that file only;
all other whitespace checks remain enabled. No unrelated
line-ending normalization is included.

### Initial independent reviews and bounded corrections

The native [GPT initial report](n2-vocabulary-reviews/batch-40-gpt-initial.md)
and [Claude initial report](n2-vocabulary-reviews/batch-40-claude-initial.md)
reviewed the same committed snapshot
`5769c83f86c2c719c8d38a4f6892cfeee848aab5`.
Actual models were **gpt-6.1-sol** and **claude-opus-5.5**,
run sequentially with zero edits; each exited before the
next substantive work. Native events authenticate their
exact prompts, original commit, actual models, restricted
tools and complete final-message archives. Initial access
excluded the author's quiz rationale and other reports.
These author-executed provenance checks are not
reviewer-executed Git verification.

Both read all sixteen new articles, the eight-file related
diff, narrow reuses and unchanged 籍 relationship. Their
source depths differ: GPT read the complete compact
121-family/230-sense renderings, all 34 component records,
labels, 26 public lexical captures, the MEXT representation
and 59 comparison bodies. Claude used targeted family and
JSON reads and public renderings; it did not read the
supplementary family rendering, snapshots, levels/confusable
guides or audit the 34 component records. Its original
verdict table groups fourteen CLEAN articles rather than
giving sixteen separate rows. The archive is unchanged;
confirmation requests individual rows and explicit
inherited-versus-newly-read scope.

The correction commit addresses all three formal findings:

| Observation | Adjudication |
|---|---|
| GPT B40-GPT-01: 食器 / 料理 | Add a direct guard for the polysemous English dish/dishes labels. The Japanese utensil/food distinction remains correct; this is a conservative static safeguard, not a reproduced quiz failure. |
| Claude B40-F1: 知り合い / ご存じ | Add a direct guard. Complete JMdict 1593570:2 explicitly includes acquaintance, and the existing ご存じ body teaches it; the support is stronger than a state/person analogy alone. |
| Claude B40-F2: 素人 inexperienced use | Add one affirmative Meaning sentence about a novice lacking experience or field skills. Retain the 初心者 distinction and the possibility of skilled amateurs. |

Claude's optional 食器 / 器具 observation is adopted after
checking the actual utensil label, complete family and
existing article. Shared 器 alone would not justify it.
The optional 職人 / 名人 pair is not added: the inspected
families and 名人 article distinguish a skilled occupational
role from exceptional mastery; a shared skills topic or 人
does not establish equivalent answer labels. This does not
claim those descriptions can never overlap in context.

The optional 知り合いになる construction and 消耗 reading
history are nonessential expansions, not demonstrated
defects. Claude's explicitly unchecked 白髪 Joyo-appendix
recollection is not promoted into a verified classification
finding. Existing whole-word guidance and metadata remain;
no new appendix or etymological claim is made.

The correction supplement preserves the original packet,
hypotheses and **11 / 34** declarations. It appends inspected
complete correction families with duplicates checked equal,
four complete existing comparison bodies and exact current
declarations. The correction capture has **12 complete
families / 18 senses**: seven duplicate families are checked
equal, and **five new families / nine senses** yield an
inspected union of **126 / 239**, including the twenty
principal families. The four new body inspections produce
**70 distinct complete existing bodies**; the distinct
inspected label union is **114**. These are author
inspection counts, not independent-reviewer reread counts.
Corrected state has **12 guarded new articles /
37 directional declarations**: three added pairs, with no
baseline exclusion deletion or title change. Mappings,
selected senses, levels and reciprocal relationships remain
unchanged.

Comparing equivalent observations across both entire reports,
GPT contributed the English dish ambiguity; Claude contributed
the acquaintance safeguard, inexperienced-person coverage and
optional utensil safeguard. The other model did not identify
those same issues elsewhere in its report. This is useful
complementary signal on one shared batch, not evidence of a
general model ranking or equal source-inspection depth.
Bounded sequential confirmations and final closure are
recorded below.

The corrected deterministic manifest is
**`200bdecf86266b25`**, with the asset count unchanged.

### Confirmation and closure

Both original reviewers resumed **sequentially** against
corrected commit `be09163bbaac80c0e58d21f91c5dddea0eb6fcce`,
accepted the three-card delta and reported no consequential
remaining defect or regression. Their complete native final
messages are archived as [GPT confirmation](n2-vocabulary-reviews/batch-40-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-40-claude-confirmation.md).
Exact resumed prompts, actual models, original sessions,
zero edits and all four complete reports were authenticated
against native events. Each process exited before further
substantive work.

Both completely reread 食器, 知り合い and 素人, the complete
twelve-family correction rendering and four comparison
bodies. GPT additionally read the correction JSON and 職人
as a dependency. Both inspected the appended correction
section, not the whole evidence inventory. GPT specifically
rechecked N2:801; Claude rechecked N2:791, N2:796 and N2:801.
Both now give sixteen individual article verdict rows,
explicitly carrying forward thirteen unchanged assessments
rather than pretending to reread them. Narrow kanji/reuse
verdicts and unchanged mappings remain scoped and inherited.
Claude acknowledges its initial grouped-table limitation.

**B40-GPT-01, B40-F1 and B40-F2 are resolved**, including
N2:801 coverage. The adopted optional 食器 / 器具 safeguard
is accepted. Nonadoption of 職人 / 名人 and the nonessential
construction/reading-history expansions is accepted.
Claude withdraws its earlier 白髪 consistency objection;
the appendix recollection itself remains unverified and is
not published as fact. An optional N2:801 source-note
expansion is unnecessary because unchanged selected sense 1
already includes novice and the article now teaches it.
No learner content changes after confirmation.

Closure advances **exactly twenty draft rows** to closed:
**800 closed / 0 draft / 1,012 pending / 0 unresolved**,
still mapped to **793 distinct articles: 741 new / 52 reused**.
The **4,014 word articles**, **187 tracked new-article N2
reciprocal pairs**, two explicitly checked reused pairs,
baseline preservation and **`200bdecf86266b25`** manifest
remain unchanged. Four changed kanji cards retain their
original metadata; existing 籍 needs no change.

The complementary initial-review contributions remain useful
on this batch, with unequal source-inspection depth disclosed.
Confirmation agreement is not another independent discovery
or a general model benchmark. No reviewer independently ran
Git, hashes, validators or production quiz draws; no fresh
confirmation web retrieval, corpus-frequency measurement or
native-speaker certification is claimed. The full vocabulary
expansion remains incomplete.
## Batch 41 - closed after original-session confirmations

Source rows **N2:802-N2:821** cover 芯, 新幹線, 真空,
信ずる, 心身, 申請, 人造, 寝台, 診断, 侵入,
人文科学, 人命, 深夜, 森林, 親類, 針路, 神話,
酢, 水産 and 炊事. All **twenty articles are new**;
there are no narrow reuses. The
[source packet](n2-vocabulary-batch-sources/batch-41.json)
retains the raw rows separately from teaching selections.
The pinned list is a named community resource, not an
official modern JLPT syllabus.

芯 selects JMdict senses 1-2, not its pistil/stamen senses.
真空 selects physical sense 1, not Buddhist sense 2.
The other principal selections are sense 1. Separately
attributed public senses support figurative 真空/針路/神話,
broader assessment under 診断, extended 親類, and broad
versus narrow 人文科学. They are not invented extra
JMdict indices or independent N2 assignments.

Consequential qualifications include actual low-pressure
vacuum rather than only literal zero matter; 信ずる's
distinct dictionary classifications and usable inflections;
administrative but not government-only 申請; nonfraudulent
人造; 寝台 beyond transport but not every sofa; intransitive
侵入/炊事; 人命 versus daily living; no universal 深夜 clock
boundary; no exact forest-size/naturalness taxonomy; and
freshwater as well as marine 水産.

The inspected union contains **195 complete families / 469
sense records**, including **20 principal families / 24
senses** checked equal rather than added twice. The
original selected **190 / 457** is supplemented by **five
complete families / twelve senses** for 試験, 晩, 水産業,
頼む and 適用. There are **149 distinct inspected existing
labels**, **92 complete existing article bodies** (88 in the
fifteen selected bundles plus four final bodies), **40
complete component records** and **30 actual Digital
Daijisen retrievals**.

The original broad comparison capture has **247 families /
568 senses**. The authenticated capture union is **258 /
623**; it is not all author-inspected. The original
capture-stage pending-inspection plan remains unchanged,
with a separate completed-inspection receipt. Alternate
headings, readings and surname lists are distinguished
from lexical senses. Captures and author receipts are not
independent-reviewer retrievals or native-speaker certification.

Five N2 kanji cards gain reciprocal teaching links in
their applicable reading rows and Common words:
線 / 新幹線 at セン; 造 / 人造 at ゾウ;
森 / 森林 at シン; 林 / 森林 at リン; and
針 / 針路 at シン. Existing kanji metadata is preserved.
No kanji or stroke cards are created; absent written
components remain in the word metadata.

Initial quiz declarations comprise **16 guarded articles /
56 directional declarations**. These are author hypotheses,
not review conclusions. Actual English labels and ordinary
senses, not a subject/category match alone, govern direct
symmetric, nontransitive safeguards. Exact titles already
deduplicate 寝台 / ベッド and 親類 / 親戚. No baseline
quiz exclusions change. The blind evidence derivative
omits only `reviewEvidence.quizGuardRationale`.

Author checks establish **800 closed / 20 draft / 992 pending /
0 unresolved** rows, mapped to **813 distinct articles:
761 new / 52 reused**. There are **4,034 word articles**
and **192 tracked new-article reciprocal N2 pairs**.
The **3,273 baseline** identities, readings, titles and
exclusions remain preserved under the recorded narrow
level/reuse rules. The deterministic manifest is
**`9f27e8afbebda035`**: **6,662 assets = 6,065 files + 396
images + 201 scenes**.

These are authored-state counts, not review closure. At
that checkpoint, both independent reviews were pending;
the overall expansion remains open.

### Independent initial reviews and bounded reconciliation

The common authored snapshot is
**`f36e1e751aee9d9853bf113bc8d7f11f4734bf8f`**.
[GPT initial](n2-vocabulary-reviews/batch-41-gpt-initial.md)
used **gpt-6.1-sol**, exited, and was followed by
[Claude initial](n2-vocabulary-reviews/batch-41-claude-initial.md)
using **claude-opus-5.5**. No substantive authoring ran
concurrently. Native session events authenticate the exact
common prompt, actual models, frozen snapshot and complete
final reports; usage receipts show zero reviewer edits.
The reports are archived without replacing their differing
scope disclosures with a uniform claim of coverage.

Both read all twenty new articles and the five-file patch.
GPT also reports reading all five resulting kanji cards,
all compact family renderings, all forty component records,
149 labels, thirty captured public bodies and 34 complete
existing comparison articles. Claude read all principal
families and captured principal bodies, but only targeted
comparison evidence, two resulting kanji excerpts and
selected existing articles. Claude freshly retrieved
信ずる material; GPT made no fresh retrieval. Neither
reviewer executed Git, hashes, validators or quiz draws.

Claude disclosed a private-directory wildcard grep that
exceeded the assigned evidence paths. Author inspection
of the complete native result found **51 data-only matching
lines**, including three unassigned derivative groups:
the broad comparison rendering, the existing-body capture,
and selected-existing bundles 08/13/14 (**five physical
files**). No other-reviewer report or author quiz rationale
was returned. The reviewer claims no reliance on the extra
lines. Blind-report separation is supported by that
inspection, but **strict file-allowlist compliance is not
claimed**; the report's "none opened" is not treated as
meaning no unassigned text was exposed.

Reconciliation, pending original-session confirmations:

- **GPT41-03 / B41-Q-02:** add 人文科学/芸術 for the
  documented academic-arts/artistic-arts English-label
  overlap and clarify the academic use. This is not
  unrestricted Japanese synonymy.
- **GPT41-01:** link existing 天然 in 人造's substantive
  manufacturing contrast.
- **GPT41-02:** link existing 嘘 in 神話's substantive
  comparison. A navigation defect does not establish a
  myth/lie exclusion.
- **B41-Q-01:** adopt direct 申請/応用 and 申請/適用
  safeguards for bare English "application." The qualifiers
  partly disambiguate, so this is a conservative static
  label precaution, not a reproduced runtime defect or a
  claim that the Japanese meanings are interchangeable.
  The actual contract includes both quiz directions;
  precedent alone does not establish a pair. Do not infer
  further あてはめる/塗る exclusions transitively.
- **Claude optional 芯 precision:** name the excluded
  pistil/stamen senses instead of seemingly excluding the
  already included plant pith. Clarify N2:802's source note:
  pencil lead and candle wick are translated example
  sentences; plant pith is listed in Meaning. Preserve the
  original packet note and append its exact current
  counterpart; spelling, reading, senses and level do not
  change.

Unchecked register suggestions for 信ずる/寝台 are not
promoted to facts. Additional conjugation, undercooked-core
and 親類 comparisons remain optional expansion. The
reviewer did not establish an excessive 芯/身 safeguard
or an obligatory 針路/科目 safeguard; no further exclusion
changes are inferred from shared English words or topics.

The two complete correction families (天然 and 応用,
**four senses / ten rendered records**) add **two families /
four senses**, yielding **197 complete families / 473
senses**. Four existing articles were read completely;
two were already in the inspected union, leaving **94
distinct bodies** and **150 labels**. The original authored
evidence and guard hypotheses remain unchanged; a separate
correction supplement records these additions, exact note
clarification, exposure audit and adjudications.

Corrected quiz metadata is **17 guarded articles / 59
directional declarations**, with exactly three new direct
pairs and no baseline-title/exclusion changes. Five new
teaching cards change; all other new cards and all five
kanji edits remain unchanged. Source identities, readings,
levels, selected senses and raw list fields remain intact.
Coverage is still **800 closed / 20 draft / 992 pending**.
The regenerated manifest is **`67cdc8372132f347`**, with
the same **6,662 assets**.

Model-diversity value on this sample: **one shared arts-label
concern**; GPT supplied **two useful missing-link findings**
not identified by Claude. Claude supplied the adopted
conservative application safeguards and **two optional
precision suggestions** for 芯. GPT had already recognized
the application/request-versus-rule distinction, so Claude
is credited for the additional guard recommendation, not
for uniquely discovering that polysemy. Compare all report
sections, not labels or severity alone. Unequal evidence
depth and the disclosed data-only search deviation prevent
treating this as a controlled model benchmark.

### Original-session confirmations and closure

The corrected committed snapshot is
**`d10d502fffb32af3a9a74c7ea30404f9bc68b4a4`**.
[GPT confirmation](n2-vocabulary-reviews/batch-41-gpt-confirmation.md)
completed and exited before
[Claude confirmation](n2-vocabulary-reviews/batch-41-claude-confirmation.md)
started. Both reused their respective original sessions,
read all five changed articles completely, supplied twenty
separate article verdict rows, and found no consequential
correction-related defect or regression.

Both retain all three facets as **CLEAN** for all twenty
articles, the five unchanged narrow kanji edits and twenty
teaching mappings. The fifteen unchanged article assessments
and kanji judgments are explicitly inherited, not silently
reported as new rereads. GPT reread the complete principal
rendering, two added families, 適用 and five actual comparison
articles. Claude reread the two-family correction rendering,
five actual comparison articles, targeted family/public
records and the correction supplement. Neither reread the
entire 197-family, 150-label, 94-body or forty-component
inventory.

GPT confirms GPT41-01/02/03 resolved. Claude confirms
B41-Q-01/02 resolved and accepts the two missing-link repairs.
**The 申請 judgment remains qualified:** GPT accepts the two
guards as conservative precautions but does not independently
establish them as necessary repairs; the qualifiers materially
disambiguate. Claude considers the bare-application safeguard
resolved. This is no remaining actionable dispute and is not
recorded as unanimous proof of a production quiz failure or
Japanese synonymy.

Both accept the adopted 芯 precision and note-only
clarification. Claude's further "rather than" wording
preference for 人文科学 remains optional; the reviewer
explicitly finds the current text defensible. No teaching
changes were made after confirmation. Claude also corrects
the initial exposure disclosure to five physical files;
the original report remains unchanged and its deviation
remains visible.

All four complete native final messages, exact prompts,
actual models, original-session continuity, zero edits,
normalized committed file hashes, both snapshots, both
patches and the blind evidence derivatives were
author-authenticated. These checks do not turn author
Git/hash receipts into reviewer-executed checks.

Exactly **N2:802-N2:821** are now closed, yielding **820
closed / 0 draft / 992 pending / 0 unresolved**. The
**813 mapped articles (761 new / 52 reused)**, **4,034
word articles**, **192 tracked reciprocal N2 pairs**,
**3,273 preserved baseline identities/readings/titles/
exclusions**, and deterministic manifest
**`67cdc8372132f347`** remain unchanged by closure.
This closes batch 41, not the full 1,812-row expansion.

## Batch 42 - closed

Source rows **N2:822-N2:841** cover 水蒸気, 水素, 垂直,
推定, 水滴, 水筒, 随筆, 水分, 水平, 水平線, 水曜,
ずうずうしい, ずうっと, 末っ子, スカーフ, 図鑑, 杉,
好き嫌い, 好き好き and 透き通る. There are **seventeen
new articles and three reuses**. The
[source packet](n2-vocabulary-batch-sources/batch-42.json)
preserves the exact community-list rows independently of
the teaching selections; this is not an official syllabus.

水滴 gains only its previously absent sourced N2 level.
水曜日 remains unchanged at N5 and already teaches the
shortened 水曜 (すいよう). These are **distinct valid
entries**, source 1372180 and article 1372190, not a
source-ID error. The explicit additional selection
`1372180:1` validates the source alias against its own
family, while the primary article is checked against
`1372190:1`. The original dictionary cache is not changed.
ずっと remains N3 with unchanged metadata and gains only
a paragraph explicitly recognizing search-only ずうっと.
The source's blank gloss remains blank; the continuity,
degree and distance anchor is editorial, not inferred
compiler intent.

Consequential qualifications include invisible water
vapor versus visible droplets; hydrogen versus water;
perpendicularity relative to a reference rather than
necessarily upright lines; evidence-based but not
numbers-only or future-only 推定; non-insulated and
non-water-only 水筒; reflective 随筆 without a rigid
エッセイ partition; contextual moisture/fluid translations;
horizontal 水平 rather than unqualified water height or
horizon; and separately attributed public instrument and
geometric-line uses. 図鑑 is an illustrated reference book,
not every illustrated story. 末っ子 is birth order, not
present youth. 好き好き is the noun すきずき. The clear
voice in 透き通った声 need not narrate a change of state.

The inspected comparison union contains **191 complete
families / 402 sense records**: the original **188 / 373**
plus **three / 29** from complete 線 and 本 lookups,
including the separate 本/もと family. The **twenty source
principals / 27 senses** are included, not added twice.
The packet's **21 source-plus-teaching families / 28
senses** additionally include 水曜日. Evidence includes
**104 actual existing labels**, **60 complete existing
article bodies** (58 selected plus 線/本), **29 complete
component records** (28 original plus 日 for the reused
article), and **31 actual Digital Daijisen retrievals**.
The original pending-inspection plan is preserved; a
separate receipt records completion. Broader unselected
body captures are not claimed as inspected.

Four N2 cards gain reciprocal reading-row and Common words
links: 蒸 / 水蒸気 at ジョウ, 筒 / 水筒 at トウ,
筆 / 随筆 at ヒツ, and 線 / 水平線 at セン.
Existing 滴 / 水滴 links and all kanji metadata remain.
Absent components stay in word metadata; no kanji or
stroke cards are added.

Initial quiz metadata has **15 guarded new articles / 42
directional declarations**. These are author hypotheses
about direct meanings and actual English labels, not
reviewer findings or reproduced runtime failures. Exact
titles deduplicate; exclusions are symmetric,
nontransitive, and protect both quiz directions and
co-choices. No baseline title or exclusion is changed.
The blind derivative omits only the author's quiz rationale.

Author checks establish **820 closed / 20 draft / 972
pending / 0 unresolved**, mapped to **833 distinct articles:
778 new / 55 reused**. There are **4,051 word articles**
and **196 tracked new-article reciprocal N2 pairs**.
The **3,273 baseline** identities, readings, titles and
exclusions remain preserved under the documented reuse
and source-level rules. The deterministic manifest is
**`d6a169274503a630`**: **6,679 assets = 6,082 files + 396
images + 201 scenes**.

Both independent reviews are pending. These are authored
counts, not review closure or native-speaker certification;
the full vocabulary expansion remains open.

### Independent initial reviews and reconciliation

The common committed authored snapshot is
**`1c55dc75c503046de66d6cf41e73bbe25c96fc62`**.
[GPT initial](n2-vocabulary-reviews/batch-42-gpt-initial.md)
used **gpt-6.1-sol** and exited before
[Claude initial](n2-vocabulary-reviews/batch-42-claude-initial.md)
used **claude-opus-5.5**. Both were read-only native
sessions with the same snapshot, scope, rubric and source
access; neither received the other's findings or the
author's quiz rationale.

Both read all seventeen new articles, three reuse bodies
within bounded scope, the six-file related patch and all
four affected kanji cards. GPT read the principal and all
ten selected-family renderings, supplemental families,
twenty mappings, 29 components, 104 labels and 31 captured
public bodies, plus 57 additional comparison articles.
Claude read the principal evidence, mappings, components
and public text captures, selected-family file 05 and part
of 09; it searched, rather than fully read, the other
family files and roughly forty comparison headers. It
did not read the blind packet, labels JSONL or snapshot
JSONs. Equal access is not equal inspection depth.

Both accepted the source identities, selected senses,
easier levels, distinct-entry 水曜 reuse and four reciprocal
kanji edits. Three bounded findings are addressed:

- **GPT42-01:** Add direct 推定/計算 and 推定/予定
  safeguards. Complete pinned entries corroborate
  estimation/estimate in ordinary senses; 計算's actual
  article also teaches the extension. Their primary labels
  alone had hidden the plausible reverse-direction answer.
- **GPT42-02:** Add direct 水平/線 protection for bare
  level-label ambiguity. Entry 1391780 sense 6 was already
  captured completely. Existing 水平線 guards are not
  transitive; this is not a claim that 線 means horizontal.
- **Claude F1:** Explain that ずうっと writes a lengthened
  う sound, like ずーっと; stretching can add emphasis.
  Retain ordinary ずっと and the search-only lookup flag.
  The initial paragraph did not explicitly assert a short
  pronunciation; the supported gap is incomplete
  explanation, not a demonstrated false pronunciation
  rule. JMdict explicitly marks ずーっと emphatic, not
  ずうっと separately. Claude found no fresh monolingual
  emphasis entry; the adopted wording stays qualified.

Two Claude optional suggestions are adopted: four exact
entry IDs are added to the four kanji source lists, and
existing 図々しい in 厚かましい plus 水平線 in 地平線
become links to the new articles. These are narrow
provenance/link changes, not required new teaching.
No category-only 水筒/container guards or component-only
好き嫌い/嫌い guard is added. Extra examples, legal/passive
uses, proverb, の forms and kana polish remain optional.

The complete correction lookups for 計算 and 予定 add
**two families / three senses**, giving **193 complete
families / 405 senses**. Four complete existing bodies
were read; 厚かましい and 地平線 were already counted,
giving **62 distinct bodies and 106 labels**. A separate
supplement preserves the original evidence, hypotheses and
reports while recording added evidence and adjudications.
The exact private-file allowlist was checked against both
native tool logs; no directory wildcard or named forbidden
read was found. Both complete final reports, actual models,
exact prompts and zero edits were authenticated by the
author; these are not reviewer-executed Git/hash checks.

Corrected metadata has **15 guarded new articles / 45
directional declarations**, exactly three direct pair
additions. Three scoped word passages/headers change;
two baseline words receive links only and the four kanji
receive citation IDs only. Source readings, identities,
levels, sense selections and raw glosses are unchanged.
Coverage remains **820 closed / 20 draft / 972 pending**,
with **4,051 words**, **196 tracked reciprocal N2 pairs**
and **3,273 preserved baseline metadata identities**.
The manifest is now **`36eb8f05991e3591`**, with unchanged
asset counts.

Model-diversity value on this sample: GPT uniquely
identified the two adopted quiz-pair concerns (three
pairs); Claude uniquely proposed the adopted vowel-length
clarification, four source-list additions and two backlinks.
Equivalent observations were compared across Findings,
Optional and Limits, not severity labels alone. Evidence
depth differed substantially; this is complementary sample
evidence, not a controlled model benchmark.

Original-session confirmations are pending; none of the
twenty rows is closed by this reconciliation.

### Original-session confirmations and closure

The corrected committed snapshot is
**`416bae390072e79df4dbf7cf8e161ce4fe9500cd`**.
[GPT confirmation](n2-vocabulary-reviews/batch-42-gpt-confirmation.md)
completed and exited before
[Claude confirmation](n2-vocabulary-reviews/batch-42-claude-confirmation.md)
started. Each resumed its original session, read all nine
changed cards completely, supplied twenty individual
all-**CLEAN** article judgments and accepted the four
kanji citation changes, two backlinks and all twenty
mappings. Seventeen unchanged article judgments are
explicitly inherited rather than reported as fresh full
rereads.

GPT confirms both original findings resolved. Claude
confirms F1 resolved and partially accepts the author's
severity qualification: the initial defect was an
incomplete explanation, not an explicit false short-vowel
rule. Both accept the qualified vowel-length/emphasis
wording while retaining the failed/irrelevant monolingual
lookups as limits. They do not fabricate fresh attestation.

The quiz judgments retain a meaningful difference in
strength. Claude calls 推定/計算 well supported but
推定/予定 weaker and 水平/線 a mild clash; it accepts
the latter two as defensible low-cost guards, not proven
necessary repairs. GPT retains its stronger label-based
assessment. This is no remaining actionable dispute, and
the record does not turn shared acceptance into unanimous
proof of a production failure.

All four complete native final messages, exact prompts,
actual models, original-session continuity, zero edits,
explicit private-file access, both committed snapshots,
patches, normalized hashes and blind derivatives were
author-authenticated. Neither reviewer independently ran
Git, hashes, the app or quiz draws. No teaching change
followed confirmation.

Exactly **N2:822-N2:841** are closed, yielding **840
closed / 0 draft / 972 pending / 0 unresolved**. The
**833 mapped articles (778 new / 55 reused)**, **4,051
word articles**, **196 tracked reciprocal N2 pairs**,
**3,273 preserved baseline identities/readings/titles/
exclusions**, and deterministic manifest
**`36eb8f05991e3591`** remain unchanged by closure.
This closes batch 42, not the full 1,812-row expansion.

## Batch 43 - drafted, independent review pending

Source rows **N2:842-N2:861** map to eighteen new
articles: 隙間, スクール, 少なくとも, 図形, スケジュール,
鈴, 涼む, スタート, スチュワーデス, 酸っぱい, ステージ,
ストッキング, ストップ, 素直, 頭脳, スピーカー, 図表
and スマート. Reuse すっきり with only its newly sourced
N2 level, and N4 捨てる with a narrow rare-spelling
棄てる recognition paragraph. The raw blank gloss remains
blank; discarding is an editorial anchor, not recovered
compiler intent.

The [batch evidence](n2-vocabulary-batch-sources/batch-43.json)
retains original fields, complete principal families,
one-based selections and restrictions. The author read
twenty principal families/forty senses within a
**249-family/581-sense** comparison union, **160 labels**,
**81 complete existing bodies**, **eighteen component
records**, and **twenty-five actual public dictionary
retrievals**. The original prepared/not-inspected plan
is preserved; a separate completion receipt records the
actual reads. Other broad captured bodies remain
capture-only. These are author assertions, not independent
review findings.

涼/涼む at すず.む and 脳/頭脳 at ノウ receive reciprocal
reading-row and Common words links. No kanji metadata,
new kanji cards or strokes change. Missing component
cards do not remove written kanji from word metadata.
The eighteen new articles receive direct, nontransitive
quiz safeguards where authored; identical school titles
already deduplicate. No production quiz failure is claimed.

Coverage is **840 closed / 20 draft / 952 pending /
0 unresolved**, mapped to **853 distinct articles:
796 new / 57 reused**. There are **4,069 word articles**
and **198 tracked reciprocal N2 pairs**. Source spellings
and existing easier levels remain preserved. This draft
has not yet passed independent GPT and Claude review.

### Batch 43 - independent initial reviews

Both reviewers assessed committed snapshot
**`8f03c81ff667930c81be8b0990ff6425b3b8c1d9`**,
sequentially in fresh native CLI sessions: actual
**`gpt-6.1-sol`**, then **`claude-opus-5.5`**. No reviewer
process overlapped another or the author's corrections.
Their exact common prompt, complete native final messages,
actual models, permitted private-file accesses, zero edits,
snapshot hashes, patches and blind derivative equivalence
were author-authenticated. Each initial process exited.
The archived reports are the complete final messages,
not stdout progress preambles:
[GPT](n2-vocabulary-reviews/batch-43-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-43-claude-initial.md).

Both read all eighteen new articles, both bounded reuses
and both narrow kanji edits. GPT's actual access includes
all thirteen complete-family renderings and the supplemental
ダイヤ rendering; Claude read only family bundle 01 and
the supplement, explicitly disclosing the other twelve
omissions. Both inspected the twenty-five supplied public
captures, mappings, components and labels, with different
targeted existing-body checks. GPT attempted fresh public
lookups; failed or unusable ones do not establish absence.
Neither reviewer executed Git, hashes or the app.

Definitions, conjugations, translations, source identities
and the two kanji edits had no established correctness
defect. GPT reported coverage gaps on 涼む, スタート and
酸っぱい; Claude on 隙間, スタート and 酸っぱい. Their
mapping verdict presentation differed: GPT separated
all-CLEAN mappings from article defects; Claude's mapping
summary carried the affected article-level coverage gaps.
Neither independently certified exhaustive correctness.

### Batch 43 - reconciliation

The author inspected the actual targeted articles and
twenty-seven complete correction-capture families. Of
these, twenty-four duplicate already inspected evidence;
only **three families/eight senses** extend the union,
to **252 families/589 senses**. Distinct author-inspected
existing full bodies increase to **89**, actual labels to
**162**; eighteen component records and twenty-five
public captures are unchanged. Separate supplemental
records retain original source fields, complete families,
authored hypotheses and the initial inspection history.

| Observation | Disposition and evidence |
| --- | --- |
| GPT F01; Claude optional 冷める | Resolved with direct 涼む/冷める protection. Complete 1554380:1 and 1556750:1 and actual titles support cooling-label ambiguity, not unrestricted Japanese substitution. |
| GPT F02 | Resolved with スタート/立ち上がる and スタート/頭. Computing start-up 1551370:5 and beginning/start 1582310:6 apply to the primary readings without rare flags. Preserve 頭's anatomy-focused lesson. |
| Claude F1 and optional 開通 | Add スタート/開会 and スタート/開通. Complete 1202560:1 supports meeting commencement; 1202850:1 explicitly includes beginning services. Shared tags or older guards alone would not justify either pair. |
| Claude F2 | Add 隙間/差 for the actual bare "gap" labels. Keep physical opening versus difference distinct; 1291070:1 does not claim that 差 means crevice. |
| GPT F03; Claude F3 | Link existing 甘い/苦い in 酸っぱい and ゴール in スタート without changing their comparisons. |
| Claude optional 埋める; dependent backlinks | Link 埋める in 隙間, 酸っぱい in existing 甘い and スタート in existing ゴール. Preserve baseline wording, metadata and levels. |
| Remaining Claude optional notes | Extra constituent-reading polish remains optional; complete すっぱい, small っ and the non-サン distinction are already taught. No unsupported ストップ/終点 or スケジュール/定期 safeguard is added. |

The correction changes four new cards and two directly
dependent baseline backlinks, adding six direct quiz
pairs: sixteen new guarded cards now declare **70**
exclusions. The two bounded reuses, two N2 kanji edits,
original mappings, raw glosses and easier levels are
unchanged. No production quiz draw or failure is claimed.
English-label safeguards do not erase lexical distinctions.

**Model-diversity note:** The three missing comparison
links and 涼む/冷める observation are shared, even though
Claude placed the latter under Optional at low confidence.
GPT uniquely found the two secondary-sense スタート
pairs. Claude uniquely found 開会 and 差 and proposed the
adopted 開通 and 埋める additions. Both families contributed
useful complementary observations on this batch. Different
evidence-reading depth and confidence prevent a controlled
model ranking. Original-session bounded confirmation is
still pending; these author adjudications are not reviewer
acceptance.

### Batch 43 - confirmed and closed

Both original native sessions resumed sequentially at
corrected commit
**`10d6abce1d35dab3b4dd84852b4f4ebaf85272a9`**,
parent **`8f03c81ff667930c81be8b0990ff6425b3b8c1d9`**:
[GPT confirmation](n2-vocabulary-reviews/batch-43-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-43-claude-confirmation.md).
Both read all six changed cards completely and gave
twenty individual all-CLEAN article verdicts across
correctness, scoped coverage and comprehensibility.
Four assigned articles were reassessed; sixteen
unchanged assigned judgments were inherited, including
the two reuses, not sixteen additional new-card reviews.
Both separately accepted the baseline backlinks,
unchanged N2 kanji links, bounded reuses and all twenty
mappings.

GPT reread complete comparison, kanji and reuse cards.
Claude reread complete 頭/立ち上がる, other comparison
front matter and the scoped kanji/reuse lines. Both
inspected complete correction-family evidence; neither
represented the full original evidence set as freshly
reread. Claude acknowledged missing 立ち上がる in its
initial title sweep, accepted 頭 as a conservative
safeguard and retained the distinction between its
optional 冷める observation and GPT's finding. Both
accepted 開会/開通 and 差 as supported English-label
precautions, not unrestricted Japanese synonym claims.
No actionable regression remained.

Exact native final messages, original-session continuity,
actual models, prompts, private-file access, zero edits,
committed snapshots, patches and blind derivatives were
author-authenticated. The correction round received the
shared author hypotheses; only the initial rounds were
blind. Neither reviewer independently ran Git, hashes,
the app or quiz draws. No post-confirmation teaching
changes were made.

Exactly **N2:842-N2:861** are closed, yielding **860
closed / 0 draft / 952 pending / 0 unresolved**. The
**853 mapped articles (796 new / 57 reused)**, **4,069
word articles**, **198 tracked reciprocal N2 pairs**,
**3,273 preserved baseline identities/readings/titles/
exclusions**, and deterministic manifest
**`7183aceabc0869b0`** remain unchanged by closure.
This closes batch 43, not the full 1,812-row expansion.

## Batch 44 - drafted, independent review pending

Source rows **N2:862-N2:881** map to eighteen new
articles: 住まい, すまない, 墨, 澄む, 相撲, スライド,
ずらす, ずらり, 刷る, ずるい, すれ違う, ずれる, 寸法,
税関, 製作, 制作, 性質 and 清書. The source spelling
清む shares the explicitly alias-aware 澄む article.
Reuse 姓 with only its newly sourced N2 level.
The three blank raw glosses remain blank; the selected
clarity/array/misalignment meanings are editorial anchors,
not recovered compiler intent.

The [batch evidence](n2-vocabulary-batch-sources/batch-44.json)
retains original fields, complete principal families,
restrictions and one-based selections. Actual author
reads covered **260 complete families/633 senses**,
including **nineteen distinct principal families/
42 senses**, **161 existing labels**, **104 complete
existing articles**, **26 component records**, and
**26 actual public captures**. The twenty source rows
include one duplicate alias family. The original
prepared/not-inspected plan remains separate from the
completed-read receipt. Other unselected broad captures
remain capture-only; the missing proper-name 田中
dictionary lookup is explicitly omitted. These are
author assertions, not independent reviewer findings.

Three new primary-spelling N2 pairs receive reciprocal
reading-row and Common words links: 刷/刷る at す.る,
税/税関 at ゼイ, and 清/清書 at セイ. Additional
清む navigation goes in 清's Common words and notes,
without adding a source-unsupported す.む reading or
inflating the primary-spelling pair count. Six old word
articles gain only substantive links: インク, インキ,
透き通る, 性格, 性 and 下書き. No kanji metadata,
new kanji cards or strokes change.

The new articles have direct pairwise quiz safeguards,
including ordinary secondary uses and broad English-label
precautions. Identical 住まい/住居 and 製作/作製
titles already deduplicate. No production quiz failure
or exhaustive semantic certification is claimed.

Coverage is **860 closed / 20 draft / 932 pending /
0 unresolved**, mapped to **872 distinct articles:
814 new / 58 reused**. There are **4,087 word articles**
and **201 tracked reciprocal N2 pairs**. This draft has
not yet passed independent GPT and Claude review.

### Batch 44 blind review and reconciliation

Authored snapshot **`519d183f9494ce149cab8317d46d7e3a7c6e41bf`**
passed the author-run format, source-preservation, exact
34-file scope, reciprocal-link and deterministic-manifest
checks. Its manifest is **`513393900c7de574`**. Those checks
are not independent linguistic or runtime certification.

The [GPT initial](n2-vocabulary-reviews/batch-44-gpt-initial.md)
and [Claude initial](n2-vocabulary-reviews/batch-44-claude-initial.md)
are complete native final messages, not summaries of
process output. Native event/usage checks authenticated
**gpt-6.1-sol** and **claude-opus-5.5**, exact expanded
prompts, the common frozen snapshot, permitted private
paths, no named forbidden reads, and zero edits. They
ran sequentially and exited; no reviewer pool remains.

Both read all eighteen new articles, the principal
families, mapping/label/component records, and actual
public text captures. GPT additionally read all thirteen
selected-family renderings, the supplement, the changed
old articles and many actual comparisons, with useful
fresh public dictionary retrievals. Claude explicitly
did not read the selected comparison families; it read
three complete comparison articles and used title/
exclusion searches for others, and read the six old
backlinks through the patch. Its naturalness limits
are retained. Equal access did not yield equal actual
evidence depth; this is not a controlled model benchmark.

| Observation | Disposition and evidence |
| --- | --- |
| GPT F01; Claude F3 | Resolved: add すまない's direct どうも/感謝/御礼/礼 pairs. JMdict 1610020:3 and the actual gratitude titles/bodies support the overlap. Existing ありがとう/恐縮 guards do not propagate. Preserve the different initial severities and confidence. |
| GPT F02 | Resolved: add 澄む/落ち着く and 澄む/安心. Selected 1373680:3 explicitly includes serenity and freedom from worry; complete 1589220 and あんしん 1153890 support the comparison. Do not use the separately captured Buddhist あんじん family as evidence for あんしん. |
| GPT F03 | Resolved: add 変える separately to スライド and ずらす. Actual meeting-time and schedule examples support the broad change label, not merely a shared topic or the existing 変更 guard. |
| Claude F1 | Resolved: replace 性質's ambiguously scoped negation with explicit statements that 性格 is not people-only and 性質 is not things-only. Preserve both words' qualified teaching rather than inventing a fixed partition. |
| Claude F2 | Adopted conservative English-label safeguard: 性質/天然 share the actual bare nature label, while 1439580 and both articles distinguish natural origin from inherent properties. Not an unrestricted Japanese synonym claim or proof from the old 自然 guard. |
| Claude F4 | Adopted conservative English-label safeguard: 刷る/活字. Complete 1208300:2 includes print/printed matter, and 活字's actual example translates small print. Preserve 刷る's verbal printing explanation and title; an old 印刷 guard alone would not establish this pair. |
| Other Claude suggestions | Optional, not required for closure: additional 住まい phrasing, a 寸法 construction example, and 税関/関税 comparison. No unsupported broad-guard deletion or claim of native-speaker certification is inferred from CLEAN. |

Author reconciliation read **fifteen complete captured
families** and the nine relevant existing comparison
articles. **Eight families/28 senses** are new to this
packet; seven duplicates are checked rather than
recounted. The resulting union is **268 families/
661 senses**, with unchanged original source, principal
and inspection fields plus a labeled correction
supplement. The ten direct guard additions produce
**sixteen guarded new articles/129 declarations**.
Only six new cards change: すまない, 澄む, スライド,
ずらす, 性質 and 刷る. Seven source-row article judgments
need reassessment because 清む shares 澄む; thirteen
are unchanged.

**Model-diversity observation:** the gratitude gap is
shared even though severity/confidence differ. GPT
uniquely identified the serenity and scheduling pairs;
Claude uniquely identified the ambiguous partition
sentence and proposed the adopted nature/print label
precautions. All Findings/Optional/Limits were compared,
not just finding counts. This is useful complementary
sample evidence, not a general model ranking.

The supported corrections await the original reviewers'
sequential bounded confirmations. Source rows remain
draft; neither mechanical checks nor author adjudication
alone closes them.

### Batch 44 - confirmed and closed

Both original native sessions resumed sequentially at
corrected commit
**`1ae25de5c02566e0926ecd865142175430c25de8`**,
parent **`519d183f9494ce149cab8317d46d7e3a7c6e41bf`**:
[GPT confirmation](n2-vocabulary-reviews/batch-44-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-44-claude-confirmation.md).
Both read the complete correction patch, all six changed
cards and all fifteen corrective comparison families.
Each gives twenty individual all-CLEAN article verdicts
across correctness, scoped coverage and comprehensibility.
Seven source-row judgments are reassessed because
清む shares 澄む; thirteen unchanged article judgments
are inherited, not thirteen fresh reviews.

GPT reread nine actual comparison bodies, all three
complete kanji cards, 姓 and the six backlink-bearing
old articles. Claude read the author-captured comparison
bodies and checked actual comparison front matter,
kanji/reuse/backlink lines and all twenty source rows.
Claude explicitly did not read the corrected evidence
derivative. Both separately accept the three unchanged
kanji edits, the bounded 姓 reuse, the six old-word
backlinks and all twenty mappings. Neither represents
the entire original evidence union as freshly reread.

Both accept all ten direct guard additions and the
explicit 性格/性質 wording. The nature and print pairs
remain conservative English-label precautions, not
unrestricted Japanese synonym claims. GPT's scheduling
justification uses スライド sense 4, ずらす sense 2
and the actual 変える meeting-time example; Claude
additionally cites スライド's sliding-scale sense 5.
That extra citation is not treated as the scheduling
sense or as independent proof of a runtime defect.
The further 住まい, 寸法, 税関 and repetition-trimming
suggestions remain optional. No consequential unresolved
linguistic claim or actionable regression remains in scope.

The complete native final messages, original-session
continuity, actual models, exact prompts, private-file
access, zero edits, committed snapshots, patches and
blind derivatives were author-authenticated. Confirmation
received shared correction hypotheses; only initial
reviews were blind. Neither reviewer independently
ran Git, hashes, the app or quiz draws. There are no
post-confirmation teaching changes or retained reviewer
processes.

Exactly **N2:862-N2:881** are closed, yielding **880
closed / 0 draft / 932 pending / 0 unresolved**. The
**872 mapped articles (814 new / 58 reused)**, **4,087
word articles**, **201 tracked reciprocal N2 pairs**,
**3,273 preserved baseline identities/readings/titles/
exclusions**, and deterministic manifest
**`9aad8d823f69032d`** remain unchanged by closure.
This closes batch 44, not the full 1,812-row expansion.

## Batch 45 - review-closed

Source rows **N2:882-N2:901** map to twenty new articles:
青少年, 整数, 清掃, 生存, 生長, 政党, 生年月日, 性能,
整備, 成分, 性別, 正方形, 正門, 成立, 西暦, 背負う,
赤道, せっかく, 接近 and 接する. The kana-primary
せっかく article explicitly recognizes source 折角.
All original CSV fields remain unchanged, including
政党's misleading parenthetical member wording.
背負う's restricted しょう/しょってる conceit sense is
recorded separately from primary せおう selections.

The [batch evidence](n2-vocabulary-batch-sources/batch-45.json)
retains complete principal families, restrictions and
one-based selections. Author reads covered **346 complete
families/891 senses**, including **twenty principal
families/38 senses**, **210 existing labels**, **131
complete existing articles**, **37 component records**,
and **27 actual public captures**. The original prepared/
not-inspected plan stays separate from the completed-read
receipt. Supplemental 応接 is an inspected complete
family/body; absent exploratory 接す is explicitly
recorded rather than replaced with fabricated evidence.
Unselected broad captured bodies remain capture-only.
These are author assertions, not independent findings.

Six new primary-spelling N2 pairs receive reading-row
and Common words links: 清/清掃 at セイ, 掃/清掃 at
ソウ, 党/政党 at トウ, 門/正門 at モン, and 接 with
接近 and 接する at セツ, explicitly explaining せっ.
Additional 角/折角 navigation targets kana-primary
せっかく and does not inflate that count. No kanji
metadata or stroke cards change. Seven existing word
articles gain only substantive backlinks: 青年, 小数,
誕生日, 性, 四角, 四角い and 門. 成長 additionally
gains a brief sourced comparison acknowledging plant
growth and broader/older 生長 uses, not a rigid spelling
partition.

Definitions distinguish integers from their notation,
main gates from every indoor doorway, enacted laws from
their entry into force, the equator from the tropical
zone, and ordinary effort/opportunity from necessarily
wasted effort. Quiz precautions use direct pairs,
ordinary secondary senses and actual English labels;
政党/党's identical titles already deduplicate.
No production quiz failure or exhaustive semantic
certification is claimed.

Coverage is **880 closed / 20 draft / 912 pending /
0 unresolved**, mapped to **892 distinct articles:
834 new / 58 reused**. There are **4,107 word articles**
and **207 tracked primary reciprocal N2 pairs**.
The initial independent reports and author reconciliation follow;
bounded confirmation remains pending.

### Blind initial reviews and author reconciliation

Both reviewers assessed committed snapshot
**`7ffb9fef77051410d247dfde7de6c8315ccb8e6f`**
sequentially, with the same scope, rubric, source access and
derivative omitting only the author's original guard rationale:
[GPT / gpt-6.1-sol](n2-vocabulary-reviews/batch-45-gpt-initial.md),
then [Claude / claude-opus-5.5](n2-vocabulary-reviews/batch-45-claude-initial.md).
Their complete native final reports, actual models, separate
sessions, exact prompts, snapshots, allowed private reads and
zero edits were authenticated. Both processes exited before
the next substantive work; no reviewer pool remains.

GPT reported four findings; Claude reported five plus optional
items. Both accepted the twenty mappings and original related
edits within their actual reviewed scope. CLEAN is a bounded
verdict, not exhaustive linguistic or runtime-quiz certification.
The following are author adjudications, awaiting the original
reviewers' correction confirmation.

| Initial observation | Author disposition and evidence-supported change |
|---|---|
| GPT45-01; Claude F1: せっかく's effort/opportunity labels | Resolved by adding 苦心, 一生懸命, 機会, チャンス and きっかけ directly. Actual labels and complete families support conservative English-label protection, not unrestricted Japanese noun substitution. |
| GPT45-02: 成立's formation/conclusion labels | Resolved by adding 誕生, 建設, 結論 and 終わり. Formation/establishment overlaps directly; conclusion/closing safeguards preserve the different agreement, reasoning and endpoint uses. |
| GPT45-03: 接する's contact and generic deal-with labels | Resolved by adding 当たる and 連絡, and qualifying the new title to **touch; border on; treat people**. 片付ける's matter-settling sense is not a reason to guard the now-qualified interpersonal title. |
| GPT45-04; Claude F3: 西暦's era-word safeguards | Adopt GPT's removal of 時代/年代; do not adopt Claude's suggested 世紀 expansion. The full qualified title identifies year numbering/a calendar, not any era or century. Complete source families and actual comparison bodies outweigh an existing guard clique's unsupported premise. Claude's conflicting recommendation awaits reassessment rather than being represented as agreement. |
| Claude F2 and optional related 角 note: 折角 history | Resolved with Daijisen's expressly attributed older-noun horn-breaking anecdote: 折 breaking + 角 horn. Align the existing 角 navigation note; do not infer every modern meaning from that history. |
| Claude F4/F5: existing contrast links | Resolved by linking 緯度/熱帯 in 赤道 and 死亡 in 生存. Actual existing bodies were inspected. |
| Claude optional transitive 接する example | Adopt the captured dictionary's ひざを接する and explain bringing knees close/sitting close together. This is an attested-example improvement, not proof that the replaced invented phrase is impossible. |
| Other optional additions | Remain optional: a 正方形 side-length example, 成立させる, more 背負う/しょう collocations and 生存's alternative reading. No need to expand the batch solely to prolong review. |

Corrective research reread **fifteen complete families**;
**ten duplicates** match the original records exactly.
Only **five new families/eight senses** are appended, yielding
**351 complete families/899 senses** in the union, not 351
additional entries. The eighteen affected comparison/link
bodies include nine not in the original full-read set:
**140 distinct existing full bodies** and **216 actual labels**
in total. The captured historical and transitive-example
passages were reread, not misrepresented as fresh retrievals.
Original source selections and author inspection assertions
remain intact beside the labeled correction evidence.
The current eighteen guarded new articles have
**123 declarations**; old baseline exclusions are unchanged.

Corrections affect **six new word articles and 角 only**.
The fourteen other new articles, five other kanji edits,
eight old-word edits, twenty source mappings, raw CSV fields
and primary reciprocal-pair count remain unchanged.

### Model-diversity observation

The complete reports were compared, including Optional,
Limits and per-file notes. Both found the shared effort/
opportunity gap; GPT additionally named きっかけ and
Claude additionally named 一生懸命. GPT also identified
the 成立 and 接する gaps. Claude identified the
historical-account mismatch and three missed links, and
suggested the adopted attested transitive example.
The era-safeguard disagreement was useful precisely
because it required evidence-based adjudication:
removing unsupported guards, not adding a third.

Equal source access did not mean equal evidence depth.
GPT read more comparison bodies/families and made fresh
lookups, with failed retrievals disclosed. Claude read
the principal/compact/public records but not the selected
comparison-family bundles or all old bodies, used many
title searches and disclosed its narrower scope.
These are complementary observations on this batch,
not a controlled benchmark, model ranking or proof
that using two families removes bias. Shared correction
confirmation will not be a second blind comparison.

### First correction confirmations and bounded follow-up

The original reviewers resumed sequentially against
**`5911eeab48dd93455a75ee54cab7b86113ac1266`**:
[GPT confirmation](n2-vocabulary-reviews/batch-45-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-45-claude-confirmation.md).
Their complete native finals, original-session continuity,
models, exact prompts/private reads, committed snapshots,
patches, derivatives and zero edits were authenticated.
Both processes exited.

Both accepted the initial corrections. GPT marked all
twenty article rows CLEAN in all three facets. Claude
resolved F1-F5, expressly withdrawing the proposed 世紀
expansion after reassessing the full qualified 西暦
label, but marked 成立's correctness NEEDS FIX for a
new **Low** issue: missing direct **効力** exclusion.
Therefore this first confirmation did **not** close
the batch. Its combined three-facet cells are retained
as the native report, not silently reformatted.

The new 成立/効力 issue predates the correction; both
initial reviewers missed it. Actual 効力's complete
body and JMdict **1275250:1** support its displayed
**efficacy; validity; potency** label. 成立's title
contains unqualified **validity**, while its source
**1375880:3** concerns valid arguments. The meanings
and constructions remain differentiated; protecting
the ambiguous English labels does not equate legal
force with logical validity. Add **効力** directly to
成立's exclusions; the existing 有効 safeguard does
not propagate. No other teaching edits follow.

Claude also suggested aligning 接's still-accurate
deal-with gloss to the new word title. This remains
optional: there is no requirement that kanji example
glosses duplicate quiz titles, and the contact/people
context is accurate. No optional scope expansion is
required. Both reviewers now receive the same bounded
one-card follow-up; unchanged judgments must be
identified as inherited rather than newly reviewed.
This discovery is useful additional review signal,
not credit for a blind-initial finding or proof that
either model alone would catch every label collision.

### Batch 45 - confirmed and closed

The final one-card follow-up snapshot is
**`aa5c94c85e6be5b6a847b302945d24d2d9bf434e`**,
parent **`5911eeab48dd93455a75ee54cab7b86113ac1266`**.
The original reviewers resumed sequentially and exited:
[GPT final follow-up](n2-vocabulary-reviews/batch-45-gpt-followup.md)
and [Claude final follow-up](n2-vocabulary-reviews/batch-45-claude-followup.md).
Both accept the direct 成立/効力 safeguard and report
no actionable regression or consequential unresolved
claim in their assigned scope. Each provides exactly
twenty individual all-CLEAN article rows with separate
correctness, scoped-coverage and comprehensibility
columns. No teaching changes follow these confirmations.

All six complete native reports were authenticated,
including actual models, exact prompts, original-session
continuity, allowed private-file access, zero edits,
committed snapshots, hashes, patches, manifest entries
and evidence derivatives. These are author-executed
provenance checks, not reviewer-executed Git or runtime
quiz checks. Reviewers ran singly in short-lived
processes; none remain.

In the first confirmation both reread the six changed
new cards and 角, with fourteen unchanged new-card
judgments inherited. Both read the complete fifteen-family
corrective rendering. GPT read the full eighteen-body
comparison rendering and reread all twenty current
mappings; Claude read seventeen complete comparison
bodies plus the beginning of 片付ける and inherited
the mappings. Both checked the reciprocal and old-word
link surfaces with their stated limits. The final
follow-ups freshly read complete 成立 and 効力,
the complete 効力 family and 成立's principal record.
Nineteen unchanged article judgments, six kanji,
eight old-word edits and twenty mapping judgments
were inherited, not falsely presented as fresh full
reviews.

Final dispositions preserve the historical disagreement:
Claude withdrew the proposed 世紀 expansion after
reassessment; both accept removal of unsupported
period guards from 西暦. Both also accept the other
initial corrections, sourced history, navigation links
and attested transitive example. Claude's subsequently
discovered Low validity-label issue is now resolved,
without erasing the first confirmation's NEEDS FIX.
Remaining optional expansions are nonblocking and
unadopted. Only the initial reviews were blind;
neither shared-hypothesis confirmation is another
blind comparison.

The final author evidence union is **352 complete
families/900 senses**, including the twenty principals,
**141 distinct existing full bodies** and **217 actual
labels**. These are not the reviewers' inspection
counts. Eighteen guarded new articles now have
**124 declarations**. All source selections, raw
fields, baseline metadata/exclusions and reciprocal
pair identities remain unchanged through closure.

Exactly **N2:882-N2:901** are closed. Coverage is
**900 closed / 0 draft / 912 pending / 0 unresolved**,
with **892 mapped articles (834 new / 58 reused)**,
**4,107 word articles**, **207 tracked primary
reciprocal N2 pairs**, and **3,273 preserved baseline
identities/readings/titles/exclusions**. The final
deterministic manifest is **`967ef25aed11394f`**;
the thirty-four assigned teaching files and manifest
are unchanged by the documentation-only closure.
This closes batch 45, not the full 1,812-row expansion.

## Batch 46 - authored and subsequently review-closed

Source rows **N2:902-N2:921** map to nineteen new articles:
接続, 瀬戸物, ぜひとも, 迫る, ゼミ, せめて, 攻める,
セメント, 栓, 前後, 洗剤, 全集, 全身, 扇子, 専制,
先々月, 先々週, 先祖 and 先端. Existing **せっせと**
receives only its sourced N2 level; its title, reading,
teaching, exclusions, scenes and images remain unchanged.
Kana-primary ぜひとも recognizes 是非とも/是非共.

All raw CSV fields remain unchanged. In particular,
せめて keeps supplied adverb entry **1006570** despite
the raw attack-method gloss belonging to the separate
**攻め手 1675160** identity. The article explains the
distinction without claiming to recover compiler intent.
先々週's blank gloss is preserved.

The [batch evidence](n2-vocabulary-batch-sources/batch-46.json)
retains complete families, restrictions and one-based
selections. Actual author reads cover **432 complete
families/1,068 senses**, including **twenty principal
families/36 senses**, **268 existing labels**, **113
complete existing articles** and **30 component records**.
All **22 public capture records** were inspected:
twenty have actual lexical bodies; せっせと and 先々週
have explicit extraction failures, not positive public
verification. The mixed せめて/攻め手 headings and
扇子's short redirect are qualified. The historical
prepared/not-inspected plan is retained separately
from the completed-read receipt. Unselected captured
old bodies remain capture-only. These are author
assertions, not independent review findings.

Three primary N2 pairs gain reciprocal reading-row
and Common words links: **接/接続** at セツ,
**戸/瀬戸物** at と within the place name, and
**専/専制** at セン. No character metadata or stroke
cards change. Seven old word articles gain links only:
繋ぐ, コンクリート, 少なくとも, せっけん, 責める,
先週 and 再来月. All baseline exclusions and easier
established levels are preserved.

Authored coverage was **900 closed / 20 draft / 892 pending /
0 unresolved**, mapping **912 distinct articles:
853 new / 59 reused**. There are **4,126 word articles**
and **210 tracked primary reciprocal N2 pairs**.
Sequential blind GPT and Claude reviews assessed
the same frozen snapshot and all three facets before
any source row was closed.

### Blind initial reviews and author reconciliation

Both models reviewed committed snapshot
**`97436ec4589201838df1b398046729a2c43d57fe`**,
sequentially and independently:
[GPT / gpt-6.1-sol](n2-vocabulary-reviews/batch-46-gpt-initial.md),
then [Claude / claude-opus-5.5](n2-vocabulary-reviews/batch-46-claude-initial.md).
They received the same scope, rubric, permitted evidence
and blind derivative omitting only the initial guard
rationale. The complete native final reports, actual
models, exact prompts, private-file access, snapshot
hashes and zero edits were authenticated. Both
processes exited before subsequent substantive work.

GPT reported two findings; Claude reported five and
optional suggestions. Both accepted the twenty
mappings, three reciprocal kanji edits, seven old
links and level-only reuse within their actual scope.
The following are author adjudications, not reviewer
confirmation or proof of a reproduced quiz failure.

| Initial observation | Author disposition and evidence-supported change |
|---|---|
| GPT F01: せめて/くらい | Add the direct guard. Complete particle entry 1154340:2 has an ordinary at-least sense, distinct from the rank noun and dark adjective; minimum requests overlap the qualified minimum-wish label of 1006570. Existing shared guards do not propagate. |
| GPT F02: 攻める's stem terminology | Replace native stem せ with the kanji's reading せ and explicitly identify the ichidan stem せめ. The written okurigana boundary differs from the inflectional boundary; existing correct conjugations remain. |
| Claude F1: 先端/トップ | Add direct protection for actual leading-edge/leading-position labels, supported by 1388110:2 and 1085030:2. The existing 頂上 guard does not cover this pair. No universal equivalence between tips, rankings and leadership is claimed. |
| Claude F2: ゼミ/授業 | Add a conservative direct English-label safeguard. The seminar class of 1075160 and the broader class/lesson of 1330290 can overlap; this does not mean every 授業 is a ゼミ. |
| Claude F3: 専制/支配 | Add a conservative direct safeguard for autocratic rule and the actual broad rule/control label, supported by 1389810:1 and 1310270:1. Arbitrary concentrated rule remains narrower than control in general. |
| Claude F4: 全集/シリーズ | Add direct protection for complete/collected-series and series labels, supported by 1395340:1 and 1062910:1. Not every series is a complete collected edition. |
| Claude F5: 前後 warning | Remove the warning's throughout wording; retain the contextual reversed-order warning. This is a comprehensibility improvement, not a conclusion that the original sentence explicitly defined 前後 as throughout. Raw source fields and selected senses remain unchanged. |
| Claude optional 攻める/戦う | Adopt a conservative direct precaution for the actual attack/take-on and fight/compete labels, using complete 1279130 and 1596960. The warfare/contest overlap does not erase attack versus defense, transitivity or resistance distinctions. This was an optional hypothesis, not an initial established defect. |
| Other optional suggestions | Leave non-N2 backlinks, extra wording/register expansion and the pre-existing 再来月/先月 link gap optional. Do not change 前後 to an unrestricted always-ぜんご claim: separate archaic まえしりえ is recorded. Existing German-origin wording remains accurate. |

Corrective research inspected **seventeen complete
families**. Thirteen duplicate records match the
initial evidence exactly; only **four additional
families/twelve senses** are appended. The resulting
union is **436 families/1,080 senses**, not 436
new records. Six actual old comparison bodies were
read: くらい, トップ, 授業, 支配, シリーズ and 戦う.
Their exact hashes, labels and relationship to the
original full-read inventory are recorded separately.
No new public retrieval is claimed.

Corrections affect **seven new articles only**.
There are **six added direct precautions**, giving
**fifteen guarded new articles/85 declarations**.
The twelve other new articles, reused teaching and
level, three kanji edits, seven old links, raw source
fields, twenty selected mappings and reciprocal-pair
count remained unchanged. At this reconciliation
checkpoint, bounded confirmation by both original
reviewers was still pending and all twenty source
rows remained draft.

### Model-diversity observation

Both complete reports were compared, including
Optional, Limits and per-file notes. Their initial
actionable findings do not identify a shared defect.
GPT uniquely identified the minimum-request particle
gap and stem terminology; Claude uniquely identified
four broader-label gaps and the warning's possible
implication, plus the adopted optional fight-label
precaution. These are contributions on this batch,
not a ranking of models or proof of bias elimination.

Source access was equal, but evidence depth differed:
GPT reported reading all selected-family renderings
and 94 old comparison bodies, including all declared
guard targets. Claude disclosed targeted family
reading and a narrower old-body scope rather than
the full comparison union. Fresh GPT retrievals were
supplementary and included failed or mixed results;
Claude used author captures. Neither review
establishes live quiz behavior, native-speaker
certification or exhaustive linguistic correctness.
Correction confirmations share author hypotheses
and are not a second blind comparison.

### Batch 46 - confirmed and closed

Both original reviewers resumed their own sessions
sequentially on correction commit
**`069fddd9213233078034643051e18ba9749cf354`**,
parent **`97436ec4589201838df1b398046729a2c43d57fe`**:
[GPT confirmation](n2-vocabulary-reviews/batch-46-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-46-claude-confirmation.md).
Each process exited before the next substantive step;
no reviewer process remains. Both complete native
reports, actual models, exact prompts, original-session
continuity, permitted private reads and zero edits were
authenticated alongside the frozen snapshots, patches,
blind derivatives and assigned manifest entries.

Each reviewer supplies **twenty individual all-CLEAN
three-facet article rows**, distinguishing seven
completely reread corrected cards from thirteen
inherited unchanged rows: twelve new cards and reused
せっせと. Both read all seventeen complete corrective
families and six complete comparison bodies. They
spot-checked the three reciprocal kanji edits, seven
old links and reused level. GPT reread all twenty TSV
and compact mappings; Claude inspected the twenty
mapping rows, fully read N2:908/N2:912 and inherited
the remaining detailed mapping judgments. Neither
claims a new complete read of all unchanged teaching
or the entire corrected evidence derivative.

GPT's **F01/F02** and Claude's **F1-F5** are resolved.
Both accept all six added direct precautions and the
two prose corrections without establishing a new
consequential regression. Initial severity and
confidence differences are preserved. In particular,
the adopted 攻める/戦う suggestion remains an optional
conservative precaution, not a retrospectively proven
initial defect. Removing the negative throughout
warning is a comprehensibility improvement, not proof
that the original explicitly defined that sense.
Claude expressly withdraws both the unrestricted
always-ぜんご proposal and the unsupported
uncommon-する qualifier. Other wording expansions,
non-N2 backlinks and the pre-existing 再来月/先月
link gap remain optional.

The corrective union totals **436 complete families/
1,080 senses**, including the original twenty principal
families/36 senses. Six corrective old-body reads
include one previously inspected body, yielding
**118 distinct complete existing bodies**. Four new
actual labels bring that inventory to **272**; a
new full-body read need not imply a new label.
These remain author inspection counts, not reviewer
scope or freshly retrieved public evidence.

The model-diversity observation above remains bounded:
the blind initial reports supplied complementary
observations, with no shared actionable defect and
different comparison depths. Confirmations assess
shared hypotheses rather than independently measure
bias reduction. No live quiz draw, native-speaker
certification or controlled model benchmark is
claimed. File-only reviewers cannot independently
verify Git, hashes or committed-file equivalence;
those checks were author-executed. Initial public
retrieval failures remain explicit limitations.

Exactly **N2:902-N2:921** are closed. Coverage is now
**920 closed / 0 draft / 892 pending / 0 unresolved**,
mapping **912 distinct articles: 853 new / 59 reused**.
There are **4,126 word articles**, **210 distinct
tracked primary reciprocal N2 pairs**, and **3,273
preserved baseline identities/readings/titles/exclusions**.
The deterministic manifest is **`3593322108dafa4d`**.
The thirty assigned teaching files and manifest are
unchanged by this documentation-only closure.
This closes batch 46, not the full 1,812-row expansion.

## Batch 47 - authored and subsequently review-closed

Source rows **N2:922-N2:941** map to nineteen new articles:
センチ, 宣伝, 先頭, 全般, 扇風機, 線路, 相違,
そういえば, 雑巾, 増減, 倉庫, 相互, 創作, 葬式,
造船, 騒々しい, 増大, 送別 and 草履.
Existing **そっと** gains explicit **そうっと**, そおっと
and そーっと recognition, an emphatic gentle-handling
example and its actual public definition. Its stable
ID, primary reading, title, N3, previous teaching and
baseline exclusions remain unchanged.

All raw source fields are preserved, including the
blank gloss at N2:939. センチ selects measurement
and prefix senses **1075060:1-2**, with sentimental
sense **3** separately recorded as additional teaching,
not an independent N2 assignment. Kana-primary
そういえば recognizes そう言えば without adding
unwritten primary metadata.

The [batch packet](n2-vocabulary-batch-sources/batch-47.json)
retains twenty principal families/**27 senses**,
restrictions and one-based selections. The completed
author inspection covers **194 complete families/
435 senses**, including those principals, **195 actual
existing labels**, **110 complete existing articles**,
and **36 component records**. The original selected
186-family/388-sense inventory and the eighteen-family
supplement overlap; only eight supplemental families
are new to the inspected union. The historical
prepared/not-inspected plan is retained separately
from the completed-read receipt. Unselected captured
families and old bodies are not inspected by implication.

All **21 public retrieval records** were inspected:
twenty contain actual lexical bodies, while
**そういえば** has an explicit extraction failure,
not positive public verification. センチ's mixed
homophone headings, そっと's historical/unrelated
headings and 草履's historical じょうり heading are
qualified. JMdict's intransitive 造船 label and
Daijisen's explicit direct-object example are preserved
as separate observations; the teaching does not
manufacture a universal object prohibition.
These counts and observations are author assertions,
not independent reviewer scope.

Five primary N2 pairs gain useful reciprocal
reading-row and Common words links: **般/全般**
(ハン appearing as パン), **線/線路** (セン),
**減/増減** (ゲン), **庫/倉庫** (コ), and
**造/造船** (ゾウ). No character metadata or stroke
cards change. Four existing word articles gain links
only: **広告, 頭, 扇子 and 下駄**.
The 言 link in そういえば's recognized written alias
does not inflate primary reciprocal-pair counts.

Draft coverage is **920 closed / 20 draft / 872 pending /
0 unresolved**, mapping **932 distinct articles:
872 new / 60 reused**. There are **4,145 word articles**
and **215 tracked primary reciprocal N2 pairs**.
All baseline identities/readings/titles/exclusions
and easier levels remain preserved.
The deterministic manifest is **`784f3b025dccd098`**.
Sequential blind GPT and Claude reviews must assess
the same frozen snapshot and all three facets before
any of these twenty rows is review-closed.

### Batch 47 - initial reviews reconciled; confirmation pending

Authored commit **`7f42dbaf6ee9651095fe53f7b0efaf32b346c068`**
was independently reviewed by **gpt-6.1-sol** and then
**claude-opus-5.5**, each in an isolated process that
exited before the next began. Exact native prompts,
actual models, complete final reports, zero edits,
permitted private-file reads and absence of named
forbidden reads were authenticated. Reports are
[GPT initial](n2-vocabulary-reviews/batch-47-gpt-initial.md)
and [Claude initial](n2-vocabulary-reviews/batch-47-claude-initial.md).
Claude additionally read the Git HEAD and branch-ref
files; those reads do not establish clean content,
blob hashes or equivalence. The provenance check
does not purport to enforce every repository-path
boundary merely by checking the private allowlist.

Both complete reports, including optional notes and
limits, were compared. **増大/激増** and **草履/下駄**
were shared guard findings. GPT additionally identified
**全般/丸**, **騒々しい/ざわざわ** and **創作/架空**.
Claude additionally proposed **先頭/表**. All six
receive direct safeguards after inspection of actual
titles, ordinary senses and complete comparison bodies.
Some are conservative broader-label precautions:
they do not merge footwear identities, front-of-object
and queue-head uses, or fabrication and every kind
of imaginary content. Older guards are not transitive.
Seventeen new cards now declare **82 direct exclusions**,
six more than the authored snapshot; original guards
are retained.

Both reports questioned 騒々しい's definite native
classification. GPT left origin unverified; Claude
proposed kango from the on-based form. The correction
uses **kango as the collection's on-first mixed study
category**, explains Japanese adjective formation,
and contrasts native さわ in 騒がしい. It does not
present modern spelling as a settled etymology.
A fresh actual read of **精選版日本国語大辞典,
騒騒しい** discusses competing origins and possible
ateji. This limits the literal proposed derivation
rather than deciding by model vote. Original source
records and the unsuccessful そういえば extraction
remain unchanged.

Claude's optional そっと wording change from
"not separate verbs" to "not separate words" is
adopted only within the new alias paragraph, not
recast as a demonstrated initial coverage defect.
Its original identity, primary reading, title, N3,
exclusions and teaching remain preserved. Optional
宣伝/相違 expansion is not required for closure.
葬式/サービス remains a conservative displayed-label
precaution, not a claim that Japanese サービス
has a religious-service sense.

Corrective inspection covers **nine complete families/
31 senses**, of which three families duplicate the
original union and six add 25 senses. The deduplicated
author total is **200 families/460 senses**, **197 actual
labels** and **114 complete old bodies**; six corrective
bodies add four distinct articles. Thirty-six component
records are unchanged. The separate fresh public
inspection supports a qualified formation discussion,
not a completed historical proof.

GPT reports all 194 initial comparison families and
90 additional complete old bodies read; Claude
discloses principal/label/component/public and
targeted old-label reads, without reading the complete
comparison-family renderings. The findings were
complementary within those different actual scopes.
They are useful sample observations, not a controlled
model ranking or proof of bias elimination.

Six new articles and the new alias sentence of
reused そっと change. Thirteen new articles, five
reciprocal kanji edits, four old-word link passages,
all titles/readings/levels and all twenty source
mappings are unchanged. Both original sessions
must assess the same corrected snapshot, actual
patch, new complete evidence and author adjudications.
Confirmation is resumed and shared, not another
blind initial review. Coverage remains **920 closed /
20 draft / 872 pending / 0 unresolved** until all
consequential findings are resolved.

The validator reports zero errors; deterministic
manifest regeneration gives **`642adf6cdb83fcb3`**.
The draft coverage/preservation audit retains all
**3,273 baseline identities/readings/titles/exclusions**,
**4,145 word articles** and **215 distinct tracked
primary reciprocal N2 pairs**. These are bounded
mechanical checks, not linguistic certification or
an executed runtime-quiz test.

### Batch 47 - confirmed and closed

Both original reviewers accepted corrected commit
**`ac0cd0dad60a22949c65d11e9f1c016e6d6c8a4d`**,
parent **`7f42dbaf6ee9651095fe53f7b0efaf32b346c068`**,
and reported no new actionable findings or
consequential unresolved claim in scope.
[GPT confirmation](n2-vocabulary-reviews/batch-47-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-47-claude-confirmation.md)
each supply exactly twenty individual all-CLEAN
correctness/coverage/comprehensibility rows.
All four complete native reports, exact actual models,
prompts, original-session continuity, permitted private
reads, zero edits and snapshot/patch/equivalence hashes
were authenticated by the author. Neither confirmation
used Git metadata; their commit/hash/cleanliness
statements remain receipt-based, not independent
Git execution.

Both completely reread the seven changed articles,
the actual correction patch, all nine complete
corrective families/31 senses and all six complete
old comparison bodies. Thirteen unchanged new-card
judgments are explicitly inherited. Both spot-checked
the five reciprocal kanji and four old links. GPT
additionally reread the actual six comparison cards
and 騒がしい, all twenty mappings/TSV rows and the
complete alias family. Claude spot-checked
N2:922/936/939/941 and inherited the remaining
detailed mapping judgments. Neither claims the
entire original evidence packet was reread.

All six new safeguards were accepted, preserving
the ordinary-sense/label qualifications recorded
above. Both independently fetched the actual
精選版日本国語大辞典 entry and accepted
騒々しい's explicit distinction between study
classification and uncertain historical derivation.
The separate-words alias polish is confirmed;
remaining optional expansions are nonblocking.
No teaching changes follow confirmation.

Exactly **N2:922-N2:941** transition from draft
to closed. Coverage is **940 closed / 0 draft /
872 pending / 0 unresolved**, mapping **932 distinct
articles: 872 new / 60 reused**. All source fields,
selected senses, baseline identities/readings/titles/
exclusions and easier levels remain preserved.
There are **4,145 word articles**, **215 distinct
tracked primary reciprocal N2 pairs**, and **6,773
manifest entries**, including 396 images and 201
scene catalogs. Deterministic manifest
**`642adf6cdb83fcb3`** and the **29 assigned teaching
files** are unchanged by documentation-only closure.

Review judgments remain bounded. The original
そういえば public extraction failure and separately
reported 造船 POS evidence remain explicit;
tool-rendered public reads are not byte-authenticated
historical proofs. No live quiz test, exhaustive
native-speaker certification or controlled model
benchmark is claimed. Both sequential reviewer
processes have exited. This closes batch 47, not
the full 1,812-row expansion.

## Batch 48 - authored; independent review pending

Twenty consecutive rows **N2:942-N2:961** are drafted on parent
**`2cd95674fa935003357fbd11e0f2ddf2121d9a11`**.
Nineteen articles are new. Existing **N3 備える** gains only explicit
rare 具える recognition, possession/endowment teaching and an updated
dictionary citation; its original teaching and metadata are preserved.

| Source ID | Article | Selected pinned senses | Additional senses |
|---|---|---|---|
| N2:942 | 総理大臣 | 1401820:1 | - |
| N2:943 | 送料 | 1402870:1 | - |
| N2:944 | 属する | 1405710:1 | - |
| N2:945 | 続々 | 1596730:1 | - |
| N2:946 | 速達 | 1405030:1 | - |
| N2:947 | 測定 | 1404570:1 | - |
| N2:948 | 測量 | 1404590:1 | - |
| N2:949 | 速力 | 1405080:1 | - |
| N2:950 | 素質 | 1397240:1,2 | - |
| N2:951 | 祖先 | 1396820:1 | - |
| N2:952 | そそっかしい | 1006740:1 | - |
| N2:953 | 率直 | 1596570:1 | - |
| N2:954 | 備える | 1244960:1,2,3 | - |
| N2:955 | そのうえ | 1006880:1,2 | - |
| N2:956 | そのころ | 2547920:1 | - |
| N2:957 | そのため | 1006850:1 | - |
| N2:958 | そのほか | 1006900:1,2,3 | - |
| N2:959 | 蕎麦 | 1238460:2 | 1238460:1,3 |
| N2:960 | 剃る | 1581900:1 | - |
| N2:961 | それなのに | 2055520:1 | - |

The [source packet](n2-vocabulary-batch-sources/batch-48.json)
preserves raw source fields, including the blank glosses for
N2:956 and N2:961. Rare source 卒直 maps to 率直 with explicit
recognition of the original spelling. 続々 and 蕎麦 are separate
identities, not reuse of shivering ぞくぞく or spatial 側.
The 其の頃 spelling is not in the selected pinned family and is
not taught. Search-only 其の他/其の外/其他 are distinguished from
recommended spellings. Additional 蕎麦 senses do not independently
acquire an N2 assignment.

Completed author inspection covers **231 complete families /
487 senses**, including the **20 principals / 29 senses**,
**207 actual labels**, **118 complete old article bodies** and
**32 complete components**. The eleven supplemental families
add ten distinct identities and eighteen senses to the original
221-family selection. Unselected captures are not reported
as inspected. The historical prepared/not-inspected plan remains
unchanged; a separate receipt records completed reads.

The **26 original public endpoint attempts** include **21 positive
lexical captures** and five missing extractions. Repeated alias
endpoints are not distinct lexical families. その他 returned
そのた rather than a direct そのほか heading; a separate
其の頃 HTTP404 is not positive alias evidence. The subsequent
actual Daijisen **率** character capture is counted separately:
its ソツ sense 3 explicitly exemplifies 率直. Simplified
rate-only extractions and a search summary did not establish
that character sense. These are author inspections, not
independent findings or frequency measurements.

Six primary reciprocal pairs are added at reading rows and
Common words: **総/総理大臣** at ソウ, **臣/総理大臣** at ジン,
**測/測定** and **測/測量** at ソク, **量/測量** at リョウ,
and **麦/蕎麦** at a separately labelled whole-word そば row.
No invented 麦=ば reading is introduced. **卒** gains qualified
rare-alias navigation only, not a primary pair or Common words
example. Six old articles change links only: 首相, ぞくぞく,
側, 先祖, 子孫 and うどん. No kanji metadata or stroke files change.

Initial quiz declarations comprise **17 guarded new articles /
87 declarations**. They are author hypotheses requiring
independent assessment, not certified quiz behavior. Actual
complete labels and ordinary senses govern direct symmetric,
nontransitive pairs; the blind derivative removes only
`reviewEvidence.quizGuardRationale`.

Author-executed structural and preservation checks establish
**940 closed / 20 draft / 852 pending / 0 unresolved**, mapped
to **952 distinct articles: 891 new / 61 reused**.
There are **4,164 word articles** and **221 distinct tracked
primary reciprocal N2 pairs**. The 3,273 baseline identities,
readings, titles and exclusions remain preserved under the
recorded narrow level/reuse rules. The deterministic manifest
is **`c4d36677ae5240cf`**: **6,792 entries =
6,195 files + 396 images + 201 scene catalogs**.

Independent GPT and Claude review, reconciliation and
confirmation are pending. An authored commit or successful
validator does not close these twenty rows. No model-diversity
conclusion is claimed yet; the overall expansion remains open.

### Batch 48 - initial reviews reconciled; confirmation pending

Both complete initial reports are archived:
[GPT](n2-vocabulary-reviews/batch-48-gpt-initial.md) and
[Claude](n2-vocabulary-reviews/batch-48-claude-initial.md).
They independently reviewed frozen authored commit
**`614bbb8394118e9e38ebb7b8c6ca2011a62be4bb`**, sequentially,
using actual models **`gpt-6.1-sol`** and **`claude-opus-5.5`**.
Exact prompts, native final messages, models, frozen hashes,
blind derivatives, permitted private-file access and zero edits
were author-authenticated. Neither report substitutes for an
independent Git/hash check or a live quiz test.

GPT identified nine direct guard gaps across five findings.
Claude independently identified the shared **測量/調査**
English-label overlap and five localized explanatory,
coverage or naturalness concerns. Complete reports, including
Optional and Limits, were compared before assigning contributions.

The bounded correction changes **eight new articles** and adds
only **`quiz_exclusions: [持つ, ある]`** to reused **N3 備える**:

- Add direct 属する/入る and 続々/ばたばた guards using
  category membership at はいる and successive falling,
  not merely topic or sound similarity.
- Protect both そのうえ and そのほか against both
  そして and そうして: older sequence-oriented titles
  do not exhaust the words' ordinary additive uses.
- Protect 測量/調査's English survey labels and the newly
  taught possession in 備える against 持つ and ある.
  This exact baseline guard addition is explicitly recorded;
  it is not a waiver of general preservation.
- Replace 続々's misleading voicing warning with the
  already attested on reading ゾク repeated.
  Add attested 人類の祖先 with kana and translation.
  Clarify そのころ's antecedent in two sentences.
- Explain しょくする's overlapping belonging sense
  without inventing a mostly-entrust frequency rule or
  deriving literary register from a dictionary symbol.
  Attribute 剃る's altered-pronunciation note to Daijisen
  without guessing a region or present-day frequency.

An additional **optional** そのころ/昔 label precaution is
adopted after reading the complete old article and family.
It does not equate future-reference そのころ with 昔,
or retrospectively establish a shared initial defect.
Together there are **ten additional direct pairs**:
**18 guarded new articles / 95 declarations**, plus the
two declarations on reused 備える. No existing guard is removed.

Ten complete corrective families / 43 senses contain four
duplicates and **six additional identities / 17 senses**.
The deduplicated author-inspected union is now **237 families /
504 senses**, with **123 complete old bodies** and **209 actual
labels**. The eight corrective old-body rereads add five
previously uninspected bodies. No fresh author public
retrieval is counted; original 属する, 祖先 and 剃る
passages and the actual 続 component record were rechecked.

GPT's eight uniquely identified additional guard pairs
complemented Claude's localized explanation and coverage catches;
the awkward-example suggestion is optional clarity improvement,
not a demonstrated grammar violation. Some proposed Claude
register/frequency remedies exceeded their evidence and were
narrowed rather than copied. Equal snapshot, scope, rubric
and source access did not yield equal actual reading depth:
GPT read the complete comparison union and 108 old bodies
besides 備える; Claude read assigned content and compact
records but not that full union or extra old bodies.
This is useful complementary evidence on this batch,
not a controlled bias experiment or a model ranking.

Eleven other new articles, all six kanji edits, all six old
link-only edits and all twenty mappings/raw source fields
remain unchanged. Optional footer expansion, extra spelling
variants and unproven over-exclusion claims are not required
to close the scoped review. Both original-session confirmations
are still pending; the twenty rows remain **draft**.

### Batch 48 - confirmed and closed

Both original reviewers accepted corrected commit
**`06ea875040a5484ccd27594c306884a3aa8958a9`**:
[GPT confirmation](n2-vocabulary-reviews/batch-48-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-48-claude-confirmation.md).
Each provides twenty individual **CLEAN / CLEAN / CLEAN**
rows for correctness, scoped coverage and comprehensibility.
No new actionable defect remains. Exactly **N2:942-N2:961**
are now closed; no teaching changes follow confirmation.

Both completely reread the nine changed articles, actual
correction patch, ten complete corrective families / 43 senses
and eight complete old bodies. Both independently count
**95 declarations on eighteen new cards**, plus exactly
two on reused 備える. Eleven unchanged new-card judgments
are explicitly inherited. GPT additionally checks current
headers and all twelve related passages; Claude inherits
the six kanji and six old link-only judgments. GPT rechecks
all twenty TSV/compact mappings and complete principal
records; Claude rechecks the twenty assigned TSV rows by grep.

All five initial GPT findings are resolved. Claude accepts
the direct guards missed in its initial narrower comparison
scope and confirms the shared 測量/調査 safeguard.
It accepts the source-backed prose corrections and explicitly
withdraws unsupported 先祖 register, mostly-entrust/literary
しょくする and regional/colloquial 剃る prescriptions.
Both treat the そのころ example as clarity polish and
the 昔 guard as an optional precaution. Other optional
expansions remain nonblocking, not unresolved defects.

All four complete native reports are archived and
author-authenticated for actual models, exact prompts,
permitted private-file access, zero edits and original-session
continuity. Initial reviews were blind; confirmations share
the adjudications. Both sequential reviewer processes exited.
Git/hash/equivalence checks remain author-executed, not
independent reviewer execution. Initial public extraction
gaps and the 其の頃 404 persist; no fresh confirmation
public fetch, live quiz or native-speaker certification
is claimed. Complementary catches do not constitute a
controlled model-bias benchmark.

Coverage is **960 closed / 0 draft / 852 pending /
0 unresolved**, mapped to **952 distinct articles:
891 new / 61 reused**. There are **4,164 word articles**
and **221 tracked primary reciprocal N2 pairs**.
All 3,273 baseline identities/readings/titles and
exclusions remain preserved under the documented narrow
level and guard exceptions, including this exact 備える
addition. The deterministic manifest is
**`796f7676ea4727ee`**: **6,792 entries =
6,195 files + 396 images + 201 scene catalogs**.
The entire 1,812-row vocabulary expansion remains open.

## Batch 49: N2:962-N2:981

**Status:** closed after independent initial reviews, corrections and bounded confirmation.

Scope: 逸れる, 揃う, 揃える, 算盤, 存じる, 存ずる, 損得,
田んぼ, 第一, 大学院, 大工, 体系, 太鼓, 対策, 大して,
対照, 大小, 体制, 体積 and 大層.

Nineteen new articles and narrow reuse of 大小 map twenty rows.
The original 大小 identity, primary reading/title, kanji, exclusions
and body remain unchanged; its previously absent level gains sourced
N2 and its selected size senses receive a dictionary citation.
Search-only source 田ぼ is explicitly normalized to 田んぼ,
with the pinned reading restriction explained rather than hidden.
存ずる's blank raw gloss is preserved. 算盤's figurative reckoning
and 存じる's thought/feeling use are separately additional coverage.

The [batch evidence](n2-vocabulary-batch-sources/batch-49.json)
contains twenty complete principal families / 41 senses and
the selected source mappings. The author actually inspected a
deduplicated union of **246 complete families / 543 senses**,
**246 actual old labels**, **145 complete old article bodies**,
**30 component records** and all four related kanji cards.
Twenty-one Weblio endpoint captures and two separately counted
Kanjipedia pages were inspected. The original inventory's unselected
captures are not silently promoted to actual reads.
These author receipts do not constitute independent review.

Four primary reciprocal N2 pairs are added: 算/算盤, 損/損得,
照/対照 and 層/大層. The whole-word 算盤 row preserves 算's
source-only そろ caveat rather than assigning a productive reading.
No old word has a link-only edit in this batch.

At the authored snapshot, draft coverage was **960 closed / 20 draft / 832 pending /
0 unresolved**, mapped to **972 distinct articles:
910 new / 62 reused**. There are **4,183 word articles**
and **225 tracked primary reciprocal N2 pairs**.
Structural and preservation checks do not establish linguistic
correctness or actual runtime-quiz uniqueness.

### Initial reviews and reconciliation

Both independent reviewers received committed snapshot
`88560e5b110c4e8b78922c8e3efedecbd1c99559`, the same assigned
scope, rubric and source access, blind to author quiz rationale
and each other's reports. They ran sequentially in isolated,
short-lived processes; the first exited before the second began.
Actual models and complete native final reports are authenticated:
[GPT](n2-vocabulary-reviews/batch-49-gpt-initial.md),
`gpt-6.1-sol`, then
[Claude](n2-vocabulary-reviews/batch-49-claude-initial.md),
`claude-opus-5.5`. Neither process edited files.

| Initial observation | Adjudication |
| --- | --- |
| GPT F49-01: 揃える/作る | Add the direct guard. Actual 作る title includes prepare, and complete 1597890 includes preparation of food and documents; 1406120:2 includes prepare/get ready. This does not equate assembling and manufacturing. |
| GPT F49-02: 体積/量 | Add the direct guard. Actual 量 teaching and 1554640:1 include physical volume; the three-dimensional qualifier does not separate it from 体積. |
| GPT F49-03: 大層/グランド | Add the direct guard for actual grand/large modifier 1046840, not sports-ground 1046340. Their shared exclusions through 大 do not protect this pair. |
| Claude B49-01: 揃う/揃える | Add the direct new-new guard on 揃う. Matching and completeness labels overlap even though the transitive/intransitive constructions remain distinct. |
| Claude B49-02: 太鼓/楽器 | Add a conservative direct safeguard for the broad musical-instrument label; do not treat it as lexical identity with every instrument. |
| Claude B49-03: 大層/ずっと | Remove the overly broad guard after checking the complete family, actual old body and newly captured Daijisen comparative sense. The conclusion does not validate the unsupported allegation that the list was copied or derived transitively. |
| Claude B49-04: 逸れる illustration | Replace awkward それた道 with the actually attested 話が脇道へそれる, kana, translation and an explanation of へ. Do not replace it with an equally unverified collocation. |
| Claude B49-05: 太鼓 source-list wording | Adopt localized clarity polish: teach the specific タンバリン name directly, without requiring the learner to see the compiler's list. No universal instrument-taxonomy ban is inferred. |
| Claude optional 体制/政府 and 対策/予防 | Add two conservative direct safeguards after reading both actual bodies and complete 1376070/1543660. Ruling-regime/government and preventive-measure/precaution labels overlap without making all setups governments or all strategies prevention. These remain optional precautions, not retroactive shared findings. |
| Claude optional 大して wording | Clarify affirmative degree expression and retain 大層's formal/old-fashioned qualification. This is polish, not evidence that the original sentence asserted everyday register. |
| Other optional observations and limits | Do not rewrite preserved 大小 or demand a new を example merely for completeness. Recheck the supplied actual Daijisen 対策 heading, which explicitly has 名(スル); failed fresh extraction neither verifies nor contradicts it. This is supplied evidence, not a fresh successful reviewer retrieval. |

The correction changes nine new articles. Seven direct declarations
are added and one removed, leaving **141 declarations on all
nineteen new articles**. Ten other new articles, all four kanji
edits, reused 大小 and all twenty mappings/raw fields are unchanged.

The models supplied complementary useful observations, with no
shared initial actionable finding after comparing the complete
reports, including Optional and Limits. GPT uniquely identified
three missing direct guards; Claude uniquely identified the
new-new pair, broad instrument safeguard, comparative over-guard
and localized explanatory issues, plus optional precautions/polish.
Its copying allegation is not supported and is not adopted.
GPT read all complete-family renderings and reports 134 complete
old-body reads; Claude read one of ten selected-family renderings,
the supplemental rendering and mostly old front matter.
Both read assigned articles and related edits, but their actual
comparison depth differs. This demonstrates usefulness on this
sample, not a controlled model-bias experiment or general ranking.

### Batch 49 - confirmed and closed

Both original reviewers independently confirmed corrected commit
`4917e82133f4f6e88fd8f4e5409a1109689411ae`, parent
`88560e5b110c4e8b78922c8e3efedecbd1c99559`.
Their complete final messages are archived:
[GPT confirmation](n2-vocabulary-reviews/batch-49-gpt-confirmation.md)
and [Claude confirmation](n2-vocabulary-reviews/batch-49-claude-confirmation.md).
All twenty source rows have individual **CLEAN / CLEAN / CLEAN**
judgments. All four kanji edits, narrow 大小 reuse and mappings are
also accepted. No post-confirmation teaching change is made.

Both completely reread the nine changed articles, actual correction
patch, **fifteen complete corrective families / 42 senses**, and
**seven complete old bodies**. They rechecked the original 逸れる
example, original 対策 heading and new author ずっと capture.
Both independently counted **141 declarations** and accepted all
seven additions and the one removal. The corrective union adds five
family identities / eighteen senses, yielding **251 families /
561 senses** overall, not fifteen wholly new families.

GPT also rechecked all current headers, twenty TSV/derivative
mappings, consequential principal records, full 大小, the original
related patch and four kanji passages. Claude spot-checked assigned
TSV rows, unchanged exclusions, the four kanji edit lines and 大小
additions. Ten unchanged new bodies and broader related judgments
are explicitly inherited, not silently reported as complete rereads.

Claude expressly withdrew the copying allegation and the optional
demand for another を example. Its 対策 uncertainty is resolved by
the actual supplied Daijisen heading with 名(スル). That does not
turn its earlier failed extraction into a successful independent
fetch. Both accept the optional 体制/政府 and 対策/予防 safeguards
without retrospectively making them shared initial findings.

All four complete native reports, exact prompts/models/private
file allowlists, original-session continuity, snapshots/patches,
blind derivatives and zero edits are authenticated. Both reviewer
processes exited sequentially. File-only reviewers did not execute
Git/hash checks; those remain author-executed. No confirmation
web fetch, live quiz, exhaustive semantic-uniqueness check or
native-speaker certification is claimed. The new author ずっと
capture is separate from 21 original lexical endpoint captures and
two Kanjipedia pages. Equal initial access did not imply equal
actual reading depth or establish a controlled model-bias benchmark.

Coverage is **980 closed / 0 draft / 832 pending /
0 unresolved**, mapped to **972 distinct articles:
910 new / 62 reused**. There are **4,183 word articles**
and **225 tracked primary reciprocal N2 pairs**.
All 3,273 baseline identities/readings/titles and exclusions
remain preserved under the established narrow exceptions; this
batch adds no baseline guard exception. The deterministic manifest
is **`16a455642382ebbb`**: **6,811 entries =
6,214 files + 396 images + 201 scene catalogs**.
The entire 1,812-row vocabulary expansion remains open.
