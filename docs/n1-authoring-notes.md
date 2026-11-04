# N1 kanji expansion

## Frozen scope

[Issue #60](https://github.com/stop-cran/learning-japanese/issues/60) authorizes the
kanji-only expansion: **1,228 additions**, necessary supporting word articles and
the specified review, native-acceptance and publication gates. It does not
authorize the separate N1 vocabulary, grammar or listening projects.

The [source snapshot](n1-source-snapshot.json) pins the actual implementation
downloads, including JMdict created **2026-11-02** and Unicode **17.0.0**.
The [raw community response](n1-sources/community-list-20261102.json) contains
1,232 distinct characters. Preserve existing 士・奇・怪・訳 and the separately
documented 妖 exception. Expected final counts remain 2,213 kanji / 1,233
N1-labelled cards, absent explicitly reconciled intervening changes.

The immutable [baseline inventory](n1-sources/baseline-inventory.json) records
all 985 kanji, 4,942 word articles and 985 stroke files at
`57dcc2aaedd8d6b0f141d5b4c3cb9c13f6f797b2`, including full card metadata,
Git blob identities and SHA-256 hashes of repository bytes. Its complete
baseline manifest also pins other runtime content. Existing bodies remain
available at that Git commit; inventory hashes are not a linguistic review.

The [source index](n1-sources/source-index.json) preserves source order, full
on/kun metadata order, radical mappings, stroke-count annotations and canonical
KanjiVG SVG blob identities. All 1,228 additions are **pending** at this freeze.
The index's `statusAtFreeze` and `assignedBatchAtFreeze` are historical, not
mutable completion counters. Later batch source/review records must distinguish
pending, drafted and review-closed states and record published SHAs separately.
No card is review-closed or published by this preparation checkpoint.

[Selected KANJIDIC2 records](n1-sources/kanjidic2-selected.xml) retain the complete
parsed character records for every source member plus 妖, including fields not
transported into teaching metadata. XML is reserialized, not a byte-identical
slice of the original compressed dictionary. The snapshot pins both original
compressed and decompressed hashes. Raw dictionary downloads remain outside
runtime content and outside Git; selected complete applicable JMdict families
will be retained in each batch before lexical authoring.

## Batch 054: local unreviewed runtime draft

The [draft audit](n1-sources/batch-054-draft-audit.json) and
[execution 299](n1-sources/execution-299.json) record one **且** card,
one necessary **且つ（かつ）** support article and five strokes generated
from the qualified pinned SVG by the unchanged converter. Full source
**ショ・ソ・ショウ / か.つ** order is preserved; only **か.つ** is selected
for practice. There is one selected reciprocal pair, no baseline activations
and no changed reused runtime article.

The support article uses the two inspected dictionary example frames rather
than inventing a broad attachment or register rule. Its nine direct
exclusions protect actual additive labels and secondary senses; they do not
form a transitive clique. The three kanji distractors are **目・日・助**.
All twelve short-card legacy fallback labels were compared at author stage.
The final authored Han audit explicitly retains **苟** as requiring native
fallback/readability inspection; font cmap coverage is not rendering acceptance.
The unverified comparative register claim is omitted, not converted into a
formal-only or written-only prohibition.

This is a **validated, local UNREVIEWED draft**, not published coverage.
Two serial blind model-family reviews of the same frozen teaching and all
applicable Android/native/visual/current-main/publication gates remain.
Published additions stay **80/1,228; 1,148 remaining**. Physical-phone,
general-release and whole-set acceptance remain outstanding.

### Historical source qualification

The [membership](n1-sources/batch-054-membership.json) selects **且**,
frozen source row 3, against published `672266d5`. The
[source ledger](n1-sources/batch-054-progress.json) records inspection of
**24 complete frozen JMdict families**: six lexical / 160 lines and
18 comparison / 663 lines, eight raw character records and sixteen actual
existing articles. Full **ショ・ソ・ショウ / か.つ**, five strokes and
canonical **一 (1)** remain intact.

The minimal support candidate is **且つ（かつ）**, also spelled 且 and
marked usually kana. **暫且（ざんしょ）** is obsolete and
**苟且（こうしょ）** archaic; **苟且（かりそめ）** belongs to a
separate whole-word family and does not allocate ソ to 且.
The [qualified source evidence](n1-sources/batch-054-dictionary-evidence.json)
now verifies the exact Japanese headings and additive constructions.
Daijisen and Kanjipedia allocate **ショ** through **苟且（こうしょ）**;
it remains archaic recognition, not proposed practice. **ソ・ショウ**
remain explicitly limited source-only metadata, not invented word examples.
Proposed practice is on `[]` / kun `[か.つ]`, with one new support article
and one reciprocal pair; none is runtime metadata yet.

Existing また・しかも・更に and other connective articles expose overlapping
quiz labels; their distinct spellings, senses, easier levels and exclusions
must remain intact. Seven additional complete frozen families and ten actual
additive articles were inspected, bringing the extracted packet to **31 distinct
families**. Nine direct word-guard proposals remain subject to the final draft
title audit; they are not a transitive exclusion clique.

The full pinned five-path SVG matches its inventory blob and was converted
outside runtime content by the unchanged converter. Candidate font cmaps are
mechanical evidence only: **苟** is absent from all three bundled fonts and
requires actual fallback inspection if retained. Every final authored Han and
native readability still need checking. An explicit comparative register claim remains **unverified**:
failed or irrelevant navigation is retained, not treated as an inspected lesson.
Do not repeat that search loop or invent a formal-only rule; acquire exact
evidence if available or keep the draft's teaching claim narrowly additive.
Historical preparation-ledger pending fields remain distinguishable from this
later qualification.

At that source-only checkpoint there were no runtime teaching, manifest,
independent review, fresh Android/native check or publication changes.
Published coverage stayed **80/1,228; 1,148 remaining**.
Compatible Android `f9b59a2` or later and outstanding physical-phone,
general-release and whole-set qualifications remain unchanged.

## Batch 053: accepted bounded owner-testing publication

The [publication record](n1-sources/batch-053-publication.json) records signed
accepted commit `381996ab63d54bec6e39f7ba58be2655ae71b53a`, green CI
`41887646248` and its immutable public ZIP: all **8,287 runtime hashes** match,
**8,309 entries**, original archive budgets unchanged. Published coverage is
now **80/1,228; 1,148 remaining**: 1,065 kanji / 5,023 word articles /
85 N1 labels, including 84 named-source members and the separate 妖 exception.
The two new word articles are necessary kanji support, not an N1 vocabulary deck.

Both original independent textual reviews and dependent visual confirmations
are closed with no actionable teaching defect. Their complete reports and
process limitations remain in the [reconciliation](n1-reviews/batch-053-reconciliation.json).
Fresh combined-tree **368 Python tests**, source/baseline/membership,
readings/links/strokes/fonts, vocabulary, validator and manifest checks passed.
Accepted Android **3+1** and native **two terminal case-0** results were
reverified without rerunning them. The full archive passed production
ContentSync once; the actual reading session exercised both curated kinds.
Actual meaning wrong labels differed from the authored trio; the observed
choices had one defensible answer, not certification of every quiz pool.

The [native record](n1-reviews/batch-053-native-acceptance.json) preserves
21 distinct viewports, clipped-table limits and geometry-only drawing:
reference touches and a recall miss are not ML Kit recognition or human
successful recall. Compatible Android `f9b59a2` or later is required.
Physical-phone/general-release and whole-set acceptance remain outstanding.
Terminal publication receipts are recorded separately before the next batch.
The earlier draft and preparation checkpoints below are historical.

### Retained local unreviewed draft

The [draft ledger](n1-sources/batch-053-progress.json) now records **丙** and
exactly two necessary support articles, **丙（へい）** and **丙午（ひのえうま）**.
Both full readings remain in source order and both are selected for practice.
Two selected 丙 support pairs link both ways; 丙午 also links its existing 午
component without assigning that N5 card new support ownership.
No supporting-word vocabulary level is inferred.

The card uses a labelled modern-shape mnemonic and `structure-unclassified`;
the pinned unchanged converter supplies five runtime strokes. The actual
wrong labels are 内 “within, inner”, 肉 “meat; flesh” and 病 “illness”.
The ledger distinguishes their author-stage semantic check from unperformed
native quiz acceptance and records the specific word-title/guard decisions.
The label and calendar examples are original explanatory examples, not corpus
attestations or independent transfer evidence.

This is **unreviewed local teaching**, not accepted or published content.
Two serial blind different-model-family reviews, reconciliation, fresh
Android/native/visual checks and all integrated publication gates remain.
Published coverage stays **79/1,228; 1,149 remaining**. Compatible Android
`f9b59a2` or later and outstanding physical-phone, general-release and
whole-set qualifications remain unchanged.

### Retained qualified-source checkpoint (before drafting)

The [qualified-source record](n1-sources/batch-053-dictionary-evidence.json)
inspects eight named Japanese dictionary sections across seven raw pages.
Exact **丙（へい）** is a third-rank/class label; **丙（ひのえ）**
is the third heavenly stem. Exact **丙午（ひのえうま）**, also **へいご**,
combines that stem with the Horse branch and is term 43 in the sixty-term
cycle. Ten stems, twelve branches and sixty combined terms remain distinct.
The frozen contract-label sense is restricted to へい; the newly inspected
Japanese entries corroborate rank, not a mandatory legal convention.

Proposed practice selects both **ヘイ / ひのえ**, with exactly two necessary
new support articles: **丙（へい）** and **丙午（ひのえうま）**. No vocabulary
level is inferred from the N1 kanji. These are qualified proposals, not
authored cards or runtime selections. Both 丙 support pairs must link both
ways; the new 丙午 article must also link the existing 午 component, without
silently assigning or rewriting that N5 card. Alternate へいご recognition
must not be presented as the primary reading of a linked ひのえうま model.
Final quiz titles, wrong choices, exclusions and full authored-Han inspection
remain draft-stage work.

The entire pinned five-path SVG agrees with canonical **一 (1)** and the
frozen stroke count: the top bar is stroke 1; the 内-like group is strokes
2–5, with its inner descending stroke reaching the top bar. The unchanged
converter's candidate remains outside runtime content. Shinjigen's fish-tail
and Jitsu's pedestal/shaft-foot origin accounts are not adjudicated: use a
labelled modern-shape mnemonic and `structure-unclassified`, not a settled
origin or phonetic claim. Of 18 candidate characters, **冂** is absent from
all three bundled fonts; supported-native fallback readability remains
necessary if it appears in the future teaching. The other 17 have cmap
entries in all three fonts, not native-readability acceptance.
No runtime teaching, manifest, independent review, Android/native acceptance
or publication is changed. Published coverage stays **79/1,228; 1,149 remaining**.
Compatible Android `f9b59a2` or later and the outstanding physical-phone,
general-release and whole-set qualifications remain unchanged.

### Retained source-preparation checkpoint

The [membership](n1-sources/batch-053-membership.json) selects **丙**,
frozen source row 5, against published `e16c95b3`. The
[source ledger](n1-sources/batch-053-progress.json) records inspection of
**33 complete frozen JMdict families**: 11 lexical / 195 lines and
22 comparison / 687 lines, nine raw character records and eight existing
articles. Full **ヘイ / ひのえ**, five strokes and canonical **一 (1)**
remain intact. No runtime draft, quiz selection or support edit is made.

The standalone family's rank/class/contract-party sense is restricted to
**へい**; its separate calendar sense says especially **ひのえ**.
Candidate support is **丙（へい）** and **丙午（ひのえうま）**, subject
to exact Japanese dictionary qualification and a minimal-support decision.
丙午 also has the documented reading へいご; neither a shared spelling
nor a kana substring establishes unrestricted interchange. The ten stems,
twelve animal branches and sixty-term cycle must not be conflated.

There are no baseline declared 丙/word pairs or existing 丙 word article.
The existing 病 card mentions 丙 only in a labelled modern-shape mnemonic;
that is not lexical support or evidence of historical formation. 三's
quantity meaning must not be treated as an automatically safe wrong answer
for a third-rank title. Pinned SVG inspection, font/native acceptance,
independent reviews and all publication gates remain pending.
Published coverage stays **79/1,228; 1,149 remaining**. Compatible Android
`f9b59a2` or later is required; physical-phone/general-release and whole-set
acceptance remain outstanding.

## Batch 052: published and verified for bounded owner testing

The [publication record](n1-sources/batch-052-publication.json) closes **弐**
at signed acceptance `92d64ec0`, with the narrow existing **二（に）, N5**
reuse and no new word article. Published coverage is **79/1,228 additions;
1,149 remaining**: **1,064 kanji / 5,021 words / 84 N1 labels**, comprising
83 named source members plus the separate 妖 exception.

The [combined acceptance audit](n1-sources/batch-052-acceptance-audit.json)
records a fresh latest-main fetch/non-rewriting merge without conflicts,
368 passing Python tests, validator/vocabulary/fresh-manifest checks,
frozen sources, exact original baseline/exclusion guards, readings, reciprocal
links, pinned strokes, whole-authored-text fonts and unchanged archive budgets.
The exact immutable public ZIP matches the manifest and all **8,283 runtime
hashes**; relevant CI completed successfully.

Fresh Android execution 283's **3+1 non-skipped cases**, accepted native
attempt 3's **two cases**, and both original-session visual confirmations
were reverified, not rerun. The full production import occurred once per article
attempt. Both actual models, **claude-opus-5.5** then **gpt-6.1-sol**, returned
23 serial visual calls and 16 PNG payloads each, without overlap. Original
reports, failures and the initial Claude internal overlap remain preserved.
The [native acceptance record](n1-reviews/batch-052-native-acceptance.json)
distinguishes source PNGs from resized returned payloads and corrects Claude's
self-reported 22 calls to the observed 23 without editing its report.

弋 is readable through a shared fallback of unidentified face; the table's
clipped columns do not establish full-article rendering. Actual meaning choices
use fallback labels, not the authored 式・武・三 trio. Reference-touch tracing,
geometry-only ungraded feedback, recall miss and grade persistence are not
MLKit recognition, successful unaided recall or negative-geometry testing.
Source-only そえ and the independent Japanese whole-heading limit for 弐つ
remain qualified outside practice. Compatible Android `f9b59a2` or later is
required; physical-phone/general-release and whole-set acceptance remain
outstanding. No batch 053 starts in this checkpoint.

### Retained textual-review checkpoint

The bounded draft adds **弐**, six strokes generated by the unchanged pinned
converter, and a narrow alternative-spelling note/backlink in existing
**二（に）, N5**. No duplicate 弐 word article is created. 二 retains its
stable identity, primary reading, title, easier level and written metadata
**[二]**. Exactly one selected support pair links both ways; there are no
activated baseline declared 弐/word pairs. The incidental ordinary 二つ
comparison is not an additional support assignment.

The card preserves full ordered **ニ・ジ / ふた.つ・そえ**, canonical
**弋 (56)** and six strokes. Practice is **ニ only**, with empty kun practice.
弐心's **じしん pronunciation** is marked obsolete, not its entire family.
弐つ remains qualified old/documentary recognition with the Japanese whole-heading
limit disclosed; **そえ** stays source-only without a verified lexical example.
The title **two (formal numeral)** describes a spelling distinction, not a
new numeral meaning. The three actual wrong labels are **式 / ceremony; formula**,
**武 / military; warrior**, and **三 / three**. 二 and 双 already have three
curated wrong choices; their labels are not treated as safe random alternatives.
参's numeral sense is not erased by its participation title. No new word title,
word exclusion, historical formation or modern legal mandate is introduced.

The [draft ledger](n1-sources/batch-052-progress.json) records the exact reused
passage delta, source/reading/quiz/link decisions and pending acceptance gates.
The [draft audit](n1-sources/batch-052-draft-audit.json) records 368 passing
Python tests, validator/vocabulary/manifest checks, exact source and baseline
preservation, all **8,283 runtime hashes** and unchanged archive guards.
The [stroke/font audit](n1-sources/batch-052-stroke-audit.json) checks the
complete new card and changed reused article: **15 of 16 authored Han** are
present in all three bundled fonts; **弋** needs supported-native fallback
readability evidence. Cmap presence and inherited occurrences are not native
acceptance. The local tree has **1,064 kanji / 5,021 words / 84 N1 labels**,
including this unpublished addition, not an increase in delivered coverage.
The historical source records below remain intact.

The [textual reconciliation](n1-reviews/batch-052-reconciliation.json) preserves
both blind initial reports on signed `c7aeff7`: actual **claude-opus-5.5** and
**gpt-6.1-sol** found no actionable defect in either complete teaching file,
including both reused passages, across correctness, scoped coverage and textual
comprehensibility. No teaching changes or correction confirmations were needed;
three Claude optional groups were not adopted. Both processes exited serially,
and the first report was archived before the second launch. Each used **29 tool
calls**, with all **23 assigned resources** returned without truncation or failed
tools. Claude's first two teaching reads overlapped internally, explicitly
self-disclosed; GPT had no overlap. Strict internal serialization was therefore
not fully achieved, and the original deviation is retained. Returned bytes do
not prove comprehension or native readability.

The [fresh mechanical recheck](n1-sources/batch-052-review-source-audit.json)
confirms unchanged runtime/source/baseline/reading/link/geometry/font/manifest
and budget evidence; the 368-test, validator and vocabulary receipts remain
explicitly inherited from the byte-identical draft, not fresh execution-282 tests.
The next checkpoint is fresh Android **3+1** and supported-native full-archive
import, **弋** fallback/readability, meaning/reading/drawing/article/reciprocal/
Back/offline routes and bounded original-reviewer visual confirmation. Latest-main
integration, combined validation, CI and exact public-ZIP acceptance still follow.
Physical-phone/general-release and whole-set acceptance remain outstanding.
Published coverage stays **78/1,228 additions; 1,150 remaining**. No batch 053
or second runner is started.

### Retained qualified-source checkpoint

The [membership](n1-sources/batch-052-membership.json) freezes **弐**,
source row 323, against published `77e9ccf2b86dce58abc09e5eb3c399e79320fe37`.
It is a bounded formal-numeral/shared-identity/rare-reading case, selected
after comparing remaining source candidates rather than source order.
The [source ledger](n1-sources/batch-052-progress.json) records inspection
of all **16 complete frozen JMdict families**: six lexical / 158 lines
and ten comparison / 328 lines, plus nine raw character records and nine
actual existing articles.

Full metadata stays ordered **ニ・ジ / ふた.つ・そえ**, six strokes,
canonical **弋 (56)**. The numeral family includes 弐 alongside 二,
but that does not make every family reading an ordinary reading of each
spelling. 弐つ（ふたつ） has an old/legal-document usage note;
弐心's **じしん** has an obsolete-reading flag. Archaic 副弐（ふくじ）
does not establish **そえ** merely through its English backup gloss.
The [qualified-source record](n1-sources/batch-052-dictionary-evidence.json)
now retains six inspected Japanese dictionary sections across four raw
pages. Daijisen explicitly gives **に【二／弐】**, the documentary
alternative-spelling note, and **弐心（じしん／にしん）**. Kanjipedia
corroborates ニ・ジ and ふたつ. Proposed practice is **ニ only**, with
empty kun practice; all four raw readings remain intact.

**そえ** remains explicitly source-only lookup information: KANJIDIC2
lists it, but no lexical example is established here. Jitsu's **そえる**
and supplement/secondary senses provide related character-dictionary
context, not an exact modern **弐（そえ）** word or productive inflection.
The exact **弐つ（ふたつ）** spelling and old/legal-document note are
verified in the complete frozen JMdict entry, not an independently acquired
Japanese whole-headword entry. These limits must survive drafting.

Existing **二（に）** is a genuine same-family reuse candidate, not an
automatic reason to create a duplicate word article for 弐. A future narrow
alternative-spelling explanation and backlink must preserve 二's identity,
primary reading, N5 level and written-word kanji metadata. No support edit
or quiz selection is committed. 二 and 弐 cannot be treated as different
numeral meanings merely to manufacture wrong answers. Formal-number
comparisons are not extra assignments; no legal mandate, current frequency
or historical formation is inferred.

There are no baseline declared 弐/word pairs or existing 弐 teaching
occurrences. Proposed support is one narrow **二（に）** reuse note, with
the future 弐-card/二-word pair linked in both directions; no duplicate
word identity is needed. The full pinned six-path SVG was inspected:
canonical 弋 consists of stroke 2 and strokes 5–6; the alternative Nelson
一 is stroke 1 and inner 二 is strokes 3–4. Conversion is an external
candidate only, using the unchanged converter. Candidate font coverage is
mechanical evidence, not native readability; standalone 弋 and any other
missing candidate glyphs need supported-native inspection if actually used.
The future entire authored/changed text still needs its own font audit.
No runtime card, independent review, Android/native run or publication occurs here.
Published batch 051 remains delivered: **78/1,228 additions; 1,150 remaining**,
with **1,063 kanji / 5,021 words / 83 N1 labels**. Compatible Android
`f9b59a2` or later is required; physical-phone/general-release and whole-set
acceptance remain outstanding. Continue the same 052 bounded draft cycle.

## Batch 051: retained textual-closure checkpoint

The bounded draft adds **匁**, one necessary **匁（もんめ）** mass-unit
article, and four strokes generated by the unchanged pinned converter.
The [draft ledger](n1-sources/batch-051-progress.json) retains the full
empty on'yomi list and ordered **もんめ・め**. Only **もんめ** is selected
for practice, with its own linked support. **百匁（ひゃくめ／ひゃくもんめ）**
is qualified recognition: the complete JMdict family marks it archaic
and flags **ひゃくめ** as irregular kana usage. Character/suffix dictionaries
support shortening, including the spelling **目（め）**, but no separate
Japanese 百匁 heading was independently verified.

The mass spelling stays **匁**, not the family's historical 文目 spelling.
Pearl use is distinguished from historical silver-money values; no
frequency ranking, legal rule, fixed money conversion or historical
formation is taught. Canonical **勹 (20)** is retained with a labelled
modern-shape mnemonic. Three actual wrong labels are **久** / a long time,
**文** / sentence, writing, and **包** / wrap; enclose. Similar shape or
shared radical does not make their meanings answers to the unit question.
The support word has no inferred vocabulary level.

Exactly one reciprocal kanji/word pair is required; no baseline declared
word pair is activated and no reused teaching passage is changed.
The gram comparison distinguishes unit size rather than treating grams
as synonymous with monme. Direct exclusions must follow actual label
overlap, not shared measurement tags.

The [reconciliation](n1-reviews/batch-051-reconciliation.json) preserves
blind initials by actual **claude-opus-5.5** and **gpt-6.1-sol** at
`07b359c`, followed by both original-session confirmations of `ca54f1e`.
Claude diagnosed a minor omitted qualification; both initials had observed
the irregular-kana evidence, so it is not a uniquely discovered source fact.
The two-line fix explains that flag and the dictionary's shortened-unit
spelling without adopting the unsupported frequency word "usually."
Both original sessions now judge both complete articles CLEAN on all three
facets. Six optional expansion/polish groups remain optional and unadopted.

Reviewer processes were serial, with each original report archived before
the next launch. Initial tool calls were **38/40**: Claude had **one internal
guidance-view overlap**, despite its initial self-report; GPT had none.
Both HTML reads truncated. GPT recovered its final line during the initial;
Claude's partial line 1876 was recovered only in its original-session
confirmation. That incidental line is 目 sense 11, not sense 13 as the
coordinator's confirmation prompt mistakenly said; the unit sense is 1888.
Original reports and corrections are preserved without rewriting history.
Both dependent confirmations used **9 serial view calls**, with no overlap,
failure or truncation. All 23 assigned resources returned after recovery,
not every initial response complete or strictly serial. Supplied dictionary
pages are not fresh retrievals; returned bytes do not prove comprehension.

The [review audit](n1-sources/batch-051-review-audit.json) records fresh
368 passing Python tests, validator/vocabulary/manifest checks, exact source
and baseline preservation, all **8,281 runtime hashes** and original archive
budgets. The [current stroke/font audit](n1-sources/batch-051-review-stroke-audit.json)
checks every authored Han character: **six of seven** are in all three bundled
fonts; **勹** needs supported-native fallback readability evidence.
Its inherited occurrence is not that evidence. No font or app code changed.

This is **local textual closure**, not native acceptance or publication.
Fresh Android/native/visual checks and latest-main/combined-tree/CI/
exact-public-ZIP acceptance remain pending. The source-only checkpoints
and original draft audits are historical, not current unauthored or
unreviewed status. No Android/native run, content push or batch 052 occurs here.
Published coverage remains **77/1,228 additions; 1,151 remaining**.
Continue the same 051 cycle, not 052.

### Retained qualified-source checkpoint

The [qualified-source record](n1-sources/batch-051-dictionary-evidence.json)
and [audit](n1-sources/batch-051-qualified-source-audit.json) add six exact
Japanese dictionary sections from four externally saved raw pages.
Daijisen and Nikkoku qualify **もんめ** as the traditional mass unit;
Daijisen and Nipponica explicitly mention pearl use, so the mass sense is
not labelled wholly obsolete. Keep the frozen JMdict mass spelling
restriction **匁** rather than generalizing the combined 匁／文目 heading.
Historical silver-money uses stay separate, with no fixed yen or universal
ryō conversion and no detailed current legal claim.

Kanjipedia explicitly lists **もんめ・め**. Nikkoku identifies shortened
目（め）, and Daijisen's number-attached suffix gives 百目. Together with
the complete frozen 百匁 family, these qualify bounded shortened-reading
recognition, not an unrestricted number paradigm. A separate Japanese
百匁 headword was not found: machine-generated examples, missing pages
and 百目 pages about a yōkai are not unit-heading evidence. Proposed
practice is only **もんめ**, preserving both full readings and their order;
one necessary standalone mass-unit word article remains unauthored.

The entire pinned four-path SVG was inspected and verified against its
Git blob before unchanged-converter generation of an **external-only**
candidate. Its 勹 group contains strokes 1–2 and agrees with canonical
radical 20; the nested 丿 alternate-index annotation does not replace it.
Kanjipedia and Nipponica give different historical formation accounts;
neither is adopted. Use `structure-unclassified` and a labelled
modern-shape mnemonic, not a component-based etymology.
All three unchanged bundled font cmaps cover 匁, but lack the candidate
component characters **勹・乂・丿**. This is a future native-fallback
obligation if those components are written, not proof of glyph failure
or readable rendering. Eleven candidate characters were checked; a future
draft must audit every character it actually introduces.

No runtime draft, independent review, Android/native run or publication
occurred. The full source/baseline audit, exact 21-family re-extraction
and all 8,278 runtime hashes remain preserved; the original preparation
audit is byte-preserved. Published coverage is still **77/1,228 additions;
1,151 remaining**. Continue the same 051 draft/review/acceptance cycle,
not 052.

### Retained source preparation

The [membership](n1-sources/batch-051-membership.json) freezes **匁**,
source row 122, against published `6af98cb717755690a9ca793e5454a96ebd7a8f9f`.
It is a bounded mass-unit, shortened-reading and spelling-restriction case,
selected after comparing remaining candidates rather than source order.
The [source ledger](n1-sources/batch-051-progress.json) records coordinator
inspection of all **21 complete frozen JMdict families**: three lexical
families / 63 lines and eighteen comparison families / 676 lines. Nine
complete raw character records and nine actual existing articles were also
inspected. The initial escaped 目 metadata line was truncated; targeted
recovery returned it and the remaining 匁/勹 records completely.

Full metadata remains empty on'yomi and ordered **もんめ・め**, four strokes,
canonical **勹 (20)** and source grade 9. The mass sense in JMdict 1536280
is restricted to 匁, unlike the family's historical-money sense; its 文目
alternative must not be generalized to mass. 百匁 has whole readings
ひゃくもんめ / ひゃくめ with separate archaic-sense and irregular-kana
annotations. Exact Japanese headings must still qualify the shortened
reading, usable number forms, spelling and present-day/register boundaries.
No historical money conversion, etymology, legal status or frequency is
inferred from those records. Existing 文/目 articles are not unit-support
articles merely because their characters or readings resemble 文目.

No runtime card, support word, quiz selection, SVG conversion or font/native
acceptance is created here. There are no baseline declared 匁 word pairs or
current 匁/もんめ teaching occurrences. A single necessary standalone
mass-unit article is only a candidate, pending source qualification.
Published coverage remains **77/1,228 additions; 1,151 remaining**.
Continue the same 051 source gate before drafting, independent review and
fresh acceptance; no 052, second runner or premature publication.

## Batch 050: published for bounded owner testing

The [combined acceptance audit](n1-sources/batch-050-acceptance-audit.json)
and [publication ledger](n1-sources/batch-050-publication.json) record signed
accepted commit `5391847e65b1484d0789f5cdbcceba4ab87c3e58`. A fresh
fetch and normal merge found main already integrated, with no teaching changes.
All 368 Python tests, validator, vocabulary consistency, fresh manifest,
frozen-source membership, baseline readings/levels/exclusions, exact links,
stroke conversion, font dispositions and unchanged budgets pass.
[CI run 41835434229](https://github.com/stop-cran/learning-japanese/actions/runs/41835434229)
completed successfully. Its immutable public ZIP matches the manifest and
all **8,278 runtime hashes**: 8,300 entries, 30,608,068 compressed bytes,
44,190,545 inflated bytes and 43,922,207 retained bytes. Contributor evidence
is excluded; safe paths and per-file limits pass. Terminal evidence-commit
CI/ZIP and owner issue readback are recorded by the execution checkpoint
before the next batch; this ledger cannot embed its own eventual commit SHA.

The [native acceptance record](n1-reviews/batch-050-native-acceptance.json)
and [execution 269](n1-sources/execution-269.json) preserve the recovered
native/Android evidence and both original-session visual confirmations.
The original compile permission denial remains historical. Genuine native
attempts 1 and 2 failed on an uncomposed paragraph and an ambiguous selector;
their logs, fixtures and artifacts are retained. The separate accepted
fixture adds an explicit scroll before the unchanged ジン assertion and
narrows the 辰巳 selector. No production, teaching, heap or guard changed.
Attempt 3 has two terminal case-zero results, no skips, in 35.722 seconds.
The full archive passes through production ContentSync once per article
attempt: 1,062 kanji, 5,020 words, 82 N1 cards, no problems, reading epoch 1,
full ordered シン・ジン / たつ and empty on / sole たつ practice. Offline
reciprocal navigation, both 農/震 component links and System Back pass.
Fresh execution-267 Android 3+1 XML names, timestamps and source/copy hashes
were reverified, not rerun or replaced by batch-049 results. The historical
512-MiB host-test OOM and bounded 1-GiB host-only headroom remain distinct
from unchanged native guest/app heaps; that host init was not used for native.

Original **claude-opus-5.5**, then **gpt-6.1-sol**, each inspected the same
twelve accepted screenshots after reading their own original report,
unchanged teaching and actual diff. Their processes exited serially; the
first report was archived before the second launch. Each made **19 serial
view calls**, with zero overlaps, failures or truncations, returning twelve
actual image payloads. Complete reports and read receipts are preserved.
These are dependent visual confirmations, not new blind initial reviews
or reviewer-executed native tests. Source PNGs are 1,080 × 2,400; the view
tool returned 900 × 2,000 PNGs. Both byte sets and their separate hashes and
dimensions are archived, not falsely equated.

No actionable visual defect was established. 辰/農/震/長 are distinguishable
in four production font rows; 28 Paint probes support four raster styles
for those characters and one shared Gothic-like fallback for 厂/氵/已.
That fallback is readable, but its actual face is unknown, not four bundled
designs. The reading table's right edge and initial bottom input toolbar
limit the viewports; hidden columns, whole articles, quiz/drawing sessions
and physical phones are not certified. Twelve additional hash-equivalent
viewports are not extra independent reads. Exact temporary cleanup and
owned-helper shutdown receipts are retained; the Android worktree is clean.

**Published:** **77/1,228 additions delivered, 1,151 remaining**, including
batch 050's 辰 card, generated strokes, necessary 辰 word article and the
two reviewed 農/震 component links. Current totals are 1,062 kanji,
5,020 words and 82 N1-labelled cards: 81 named source members plus 妖.
No batch 051 begins in this checkpoint.
Compatible Android `f9b59a2` or later remains required; physical-phone,
general-release and whole-set acceptance remain explicitly outstanding.

### Retained textual closure

Two blind, read-only initials using actual **claude-opus-5.5** and
**gpt-6.1-sol** reviewed the same signed draft `cc51de4`.
Both complete new articles and **both exact 農/震 component-link additions**
were assigned from the start and separately judged CLEAN for correctness,
scoped coverage and textual comprehensibility. No actionable defect or
consequential unsupported teaching claim was established. The explicitly
source-only ジン row still has no verified lexical allocation; closure does
not convert that disclosed limit into a verified usage.

The [reconciliation](n1-reviews/batch-050-reconciliation.json) preserves both
complete original reports and one Claude optional wording/voicing group,
not adopted. No teaching fix or changed-text confirmation was necessary.
The reviewers exited serially, with **34/36 tool calls**, zero internal
tool overlaps and zero XML-range violations. Each initial metadata call
truncated within the final 龍 element; targeted recovery completed it.
All **21 assigned resources** were returned after recovery, not every
individual call untruncated. Exact returned prefixes/ranges and process
receipts establish byte coverage, not comprehension. Both reviewers used
the supplied dictionary pages; neither freshly retrieved them upstream.
Claude's reused-passage line citations are off by one; both actual deltas
are at line 22. Original reports remain unchanged.

The [fresh review audit](n1-sources/batch-050-review-audit.json) records
368 passing Python tests, validator/vocabulary/manifest/budget checks,
complete source/baseline/reading/link/stroke/font checks and all
**8,278 runtime hashes**. Teaching and runtime are unchanged.
At that textual checkpoint, fresh non-skipped Android 3+1, supported-native shape/fallback readability,
full-archive single production import, article/reciprocal/Back/offline
routes and bounded independent visual review remained next; the evidence
checkpoint above now closes those gates. Latest-main,
combined checks and publication gates follow, not precede, that acceptance.
The batch remains local and unpublished: **76/1,228 additions delivered;
1,152 remaining**. No 051 or reopening of accepted 049.

### Retained draft evidence

The qualified sources now support one necessary **辰 たつ** sign article,
one kanji card and **seven exact pinned-converter strokes**. Full
シン・ジン / たつ metadata and order are preserved; only たつ is selected
for practice. The ジン row explicitly retains the source-only lexical
allocation limit instead of inventing an example. No vocabulary level
is inferred from the N1 kanji.

The actual three wrong labels are 農 / agriculture; farming,
震 / quake; tremble, and 長 / long, chief. Their ordinary secondary
senses do not make those labels answers to the Dragon-sign question.
There is no standalone 竜/龍 word card and no established direct
word-label collision requiring an exclusion. The one declared 辰 pair
links both ways; there are no baseline declared pairs to activate.
Only the substantive component introductions in **both 農 and 震**
gain a link. Both exact deltas belong in the initial review scope.

The [draft audit](n1-sources/batch-050-draft-audit.json) records complete
frozen-source re-extraction, baseline/metadata/reading/link checks,
all runtime hashes, generated geometry, whole-authored-text font cmaps
and combined-tree checks. The [stroke audit](n1-sources/batch-050-stroke-audit.json)
keeps actual missing cmap characters and their native-fallback obligations:
32 of 34 Han characters across both new and both changed articles occur
in all three fonts; **厂 and 氵** need supported-native readability evidence.
All 368 Python tests, validator, vocabulary check, fresh manifest and local
archive budgets passed at the draft checkpoint; all **8,278 runtime hashes**
matched. Those historical checks were not linguistic or native acceptance.
The textual closure above now follows that draft; Android/native,
integration and publication acceptance remain pending.

### Retained source qualification

The [qualified-source record](n1-sources/batch-050-dictionary-evidence.json)
adds eight exact Japanese dictionary/encyclopedia sections from seven saved
raw pages. Actual 辰 たつ and 辰年 たつどし headings qualify the sign and
year expression; the character entry's explicit 戊辰 ぼしん example and
separate compound heading qualify シン without substring allocation.
Full **シン / ジン / たつ** remains unchanged. ジン has no independently
verified lexical example in this bounded evidence: retain it as explicitly
qualified character-source lookup information, not an invented example or
an invalid/obsolete/name-only reading claim. Proposed practice selects only
たつ with one necessary standalone sign article; no extra calendar article.

The complete pinned **seven-path SVG** was inspected before external
unchanged-converter candidate generation. Its general-radical group is
the whole 辰 (161), not the visible 厂 group. Use a labelled modern-shape
mnemonic and `structure-unclassified`; no historical/phonetic account is
adopted. All three packaged cmaps cover nine of ten candidate characters;
**厂 is absent** and needs actual fallback/readability evidence if authored.
Cmap absence is not a glyph failure, and no native result is claimed here.
Historical hour alternatives, traditional bearing versus modern
compass points, 辰巳 southeast and lunar-month boundaries remain explicit.
Those source-stage candidate checks are now followed by the unreviewed
draft above. No teaching or runtime acceptance is claimed; published
coverage is unchanged.

[Batch 050](n1-sources/batch-050-progress.json) selects only **辰**,
frozen source row **1070**, on published base `b189ed6`.
The [membership](n1-sources/batch-050-membership.json) records the fresh
complexity comparison: 辰 has 26 complete lexical families and three
source readings, versus 竜's 174 families and five readings.
Navigation probes 戌 and 龍 are outside the frozen named set and are not
selected. Neither source-order position nor a shared reading establishes
membership or a need for another card.

The packet preserves full **シン / ジン / たつ**, seven strokes,
grade 9 and canonical radical **辰 (161)**. Coordinator inspection covers
**26 lexical and 17 disjoint comparison families**, eight complete raw
character records and fifteen actual existing articles.
There is no activated baseline declared word pair.
Existing 農 and 震 contain substantive 辰-shaped component descriptions;
the two link-only edits must be assigned explicitly in initial reviews.
The incidental branch sequence in 午 does not require broad backlink work.

The dispositions distinguish the Dragon sign from the creature 竜/龍,
historical 辰 east-southeast from 辰巳 southeast, the twelve signs from
sixty calendar combinations, and lunar month three from Gregorian March.
The source retains competing historical hour mappings.
Whole-word 壬辰 じんしん and 時辰 じしん do **not** by themselves establish
辰's ジン allocation; that lexical allocation remains explicitly unverified.
No reading is dropped or labelled obsolete/name-only by assumption.
辰砂/辰沙 preserve the spelling restriction on しんさ; 辰星's multiple
astronomical senses remain separate rather than becoming a universal gloss.

Standalone 辰 たつ support and sole-kun practice were proposed at the
source stage and are now authored in the unreviewed local draft.
No extra dragon, astronomy, historical or mineral article is
committed; support-word levels are not inferred from N1 kanji.
The [preparation audit](n1-sources/batch-050-preparation-audit.json)
checks exact frozen inputs, complete re-extraction, original baseline
invariants and unchanged runtime hashes. It is not independent linguistic,
font, native or publication acceptance. Japanese-heading and SVG qualification
now have the bounded evidence above; all post-draft acceptance gates remain.
Published coverage stays **76 / 1,228**, with **1,152 remaining**.
Batch 049 is not reopened; physical-phone, general-release and whole-set
acceptance remain explicitly outstanding.

## Batch 049: published for bounded owner testing

The [publication receipt](n1-sources/batch-049-publication.json) records accepted
commit `228d5fa`, published recovery head `8af945e`, green content CI
`41820500539` and all **8,275 runtime hashes** in the exact immutable public ZIP.
Both original GitHub server-error request IDs remain historical evidence.
One authorized ordinary owner-scoped fast-forward succeeded after service
backoff and fresh unchanged-main verification; no authorization, signing,
permission or archive guard was changed. Accepted teaching/runtime bytes were
unchanged, so reviewers, Android and native checks were not repeated.

This brings bounded published additions to **76 / 1,228**, with **1,152 remaining**.
The [native acceptance](n1-reviews/batch-049-native-acceptance.json) and original
review reports retain their viewport, fallback-face and source-inspection limits,
including the host-only memory retry. Compatible Android `f9b59a2` or later is
required. Physical-phone, general-release and whole-set acceptance remain
explicitly outstanding. Final evidence-commit CI/archive and owner issue readback
are recorded externally before checkpointing for batch 050.

[Batch 049](n1-sources/batch-049-progress.json) selects only **丑**,
frozen source row 2, on accepted published base `e91eec0`.
Selection compared 丑's 19 complete lexical families and two source readings
with 辰's 26 families and three readings; it was not source-order selection.
A navigation probe of 戊 was rejected because it is outside the frozen named set.
The [membership](n1-sources/batch-049-membership.json) preserves full
**チュウ / うし**, four strokes, grade 9 and canonical radical **一 (1)**.
The packet retains **19 lexical and 19 disjoint comparison families**,
seven complete raw character records and coordinator inspection of seventeen
actual existing articles. No baseline declared word pair is activated.

The source dispositions separate the second/Ox sign from the existing animal
noun 牛 (うし), whose sourced N3 vocabulary level and direct 牛肉 exclusion
remain unchanged. Calendar compounds are whole-word candidates until exact
Japanese headings establish allocation; the raw 丁丑 reading ひのとのうし
is retained rather than silently normalized. Historical north-northeast differs
from 丑寅's northeast; competing hour mappings and the twelfth lunar month
must not become one universal modern interval or Gregorian December.
Night expressions retain broad versus clock-specific senses, rare ateji and
search-only spelling flags. Seasonal day expressions do not make every
丑の日 a summer-only date or 土用 a synonym of Saturday.
No historical ritual instruction is selected.

At source preparation, standalone support, practice keys, distractors,
direct exclusions and link changes were still unselected. The
[preparation audit](n1-sources/batch-049-preparation-audit.json) checks exact
frozen inputs/re-extractions, source membership, baseline invariants and
unchanged runtime hashes; it is not linguistic or native acceptance.
The subsequent [qualified evidence](n1-sources/batch-049-dictionary-evidence.json)
and [audit](n1-sources/batch-049-qualified-source-audit.json) resolve eight exact
Japanese dictionary sections on seven saved raw pages. Daijisen and Kanjipedia
qualify standalone うし; Daijisen qualifies whole 丑年 うしどし. Daijisen's
explicit 丁丑 character example plus the actual Nikkoku heading ていちゅう
qualify チュウ allocation; Nikkoku 辛丑 しんちゅう corroborates calendar use.
Nikkoku's alternative ひのとうし differs from frozen JMdict ひのとのうし:
both remain recorded, without a silent source correction. Inline recognition
can use ていちゅう without selecting that alternative or another word article.

The draft now supplies one `words/丑.md` sign article, sole うし practice and
`quizOnyomi: []`, retaining full チュウ / うし metadata. Omission from practice
is a bounded usefulness decision, not an obsolete, invalid or name-only label.
The kanji and word titles are **Ox zodiac sign**. Three wrong labels are
五 **five**, 互 **mutual** and 土 **earth, soil**, checked against actual
comparison cards and applicable frozen families. A conservative direct
丑/牛 word guard protects associated-animal label overlap; 牛/牛肉 is not
a transitive exclusion. Existing 牛's reading, N3 vocabulary level and
original 牛肉 guard remain unchanged. The one required reciprocal pair
is 丑 ↔ `words/丑.md`; no baseline declared pair is activated. Both existing
寅 articles receive only a narrow link at their substantive 丑寅 comparison.
These exact link diffs belong in the initial reviews, not a reopening of 048.
The historical hour alternatives and lunar-month boundary are qualified;
traditional 北北東 and the dictionary's thirty-degree bearing are not
silently equated to an exact modern sixteen-point compass bearing.
丑寅 うしとら is independently qualified as northeast.

The complete pinned four-path SVG was inspected before generating the runtime
stroke file with the unchanged converter; it equals the qualified external
candidate exactly. Its general-radical 一 group is the middle horizontal,
stroke 3. The draft uses a labelled modern-shape mnemonic and
`structure-unclassified`; no historical or phonetic account is selected.
Fresh draft inspection covers all 38 complete families, seven raw character
records, eight actual pre-existing articles, all eight qualified Japanese
sections and the full SVG. Full authored/touched-text font checks find 23 of
25 Han characters in all three unchanged fonts; inherited 宀/氵 require an
explicit supported-native/visual disposition. Cmap presence is not readability.

The [draft audit](n1-sources/batch-049-draft-audit.json) records complete
baseline preservation, exact membership/reading/link/geometry checks and all
**8,275 runtime hashes**. Current main `5f460b8` was merged normally at
signed `dae3cf7`, including language-metadata tooling. Combined-tree validation,
vocabulary consistency, manifest regeneration, archive budgets and **368 Python
tests** pass; EN remains schema 1 with explicit en/ja language fields.
The initial exact reused-text audit detected Git CRLF versus `read_text` LF;
the external adapter normalizes line endings before enforcing the exact two
link edits, without changing repository tooling or permitting extra edits.
An intermediate external-adapter indentation error was corrected before the
successful audit; neither failed attempt is an acceptance.

The [textual reconciliation](n1-reviews/batch-049-reconciliation.json) now
closes two blind initial reviews on signed draft `0e73a41`, using actual
`claude-opus-5.5` and `gpt-6.1-sol`. Both reviewed the two new articles and
both exact 寅 link changes from the start, returning separate correctness,
scoped-coverage and comprehensibility verdicts for all four scopes.
No actionable defect or consequential unresolved claim was established.
Four Claude optional groups remain nonblocking and were not adopted; no
teaching changes or repeat confirmations were needed.

The [review audit](n1-sources/batch-049-review-audit.json) preserves both
complete original reports and execution receipts: serial process exits,
39/38 tool calls, zero internal overlaps or XML-range violations, and all
24 assigned resources returned per reviewer. Returned bytes do not prove
comprehension. The first report was archived before the second launch.
A launcher-wrapper failure occurred before Copilot started; its record is
preserved, and it was not a reviewer or a permission denial. Claude fetched
the pinned SVG independently; GPT fetched the actual Nikkoku 丁丑 entry.
The supplied seven dictionary pages are not independent fresh retrievals.

This is local **textual closure**, not publication or native acceptance.
Fresh combined-tree checks still pass all 368 Python tests and all 8,275
runtime hashes without a teaching or manifest change. Every fresh
Android/native/visual, latest-main and publication gate remains. No
Android/native run, push or batch 050 occurs here. Batch 048 is already
published and verified for bounded owner testing, not reopened by the
historical draft section below.
Published coverage remains **75 additions; 1,153 still to deliver**.
Physical-phone/general-release and whole-set acceptance remain outstanding.
Earlier sections retain historical checkpoint wording; their publication
ledgers record subsequent acceptance.

## Batch 048: local unreviewed draft

[Batch 048](n1-sources/batch-048-progress.json) bounds the next addition to
**寅**, frozen source row 256, on accepted published base `3b2f689`.
The [membership](n1-sources/batch-048-membership.json) fixes one character
after a fresh comparison of 寅 (12), 丑 (19) and 辰 (26) complete
lexical-family workloads. The frozen packets retain **12 lexical and 14
disjoint comparison families**, seven complete raw character records and
preparation-stage coordinator inspection of twenty actual existing articles.
This draft execution reread all 26 families, seven raw records, nine actual
existing articles, all eight qualified Japanese sections and the full SVG.
Full source
readings **イン / とら**, eleven strokes, grade 9 and canonical radical
**宀 (40)** are preserved.

The packet distinguishes the Tiger sign from the existing animal noun
`words/虎.md`, also とら, whose sourced N3 level and approved 酔っ払い
exclusion remain untouched. Standalone 寅's historical east-northeast sense
differs from 丑寅 (うしとら), northeast. Its first-lunar-month sense is
not Gregorian January; the historical hour has competing dictionary
mappings. The [qualified-source evidence](n1-sources/batch-048-dictionary-evidence.json)
records eight exact Japanese dictionary sections across seven raw pages.
Daijisen explicitly gives 甲寅 (こういん); the actual Nikkoku 甲寅
heading corroborates term 51 and きのえとら. イン is qualified calendar
recognition, omitted from practice by bounded usefulness choice,
not invalid, obsolete or name-only. Full イン / とら metadata remains.
One necessary standalone とら sign article and sole-kun practice are now
drafted; no vocabulary JLPT level is inferred.

Daijisen's ウ冠 (うかんむり) heading and the complete pinned eleven-path
SVG qualify the visible 宀 top radical. Runtime geometry is generated
with the unchanged converter and equals that pinned candidate. All three
bundled fonts cover 寅 but lack standalone 宀 and 氵 in the authored
text, including the changed 演 article. Both occur in accepted base
content; the whole comparison audit also flags 虍 and 黃. Carry their
system-fallback readability into fresh native/visual acceptance; cmap checks are not that
acceptance. Kanjipedia's additional つつしむ is recorded as
an external inventory difference, not silently added to frozen readings
or illustrated with an invented word. Its historical formation account
is not selected for teaching. Traditional 東北東 remains distinct from
丑寅's northeast; Daijisen's thirty-degree description must not become
an exact modern sixteen-point compass equivalence.

At the accepted base there was no declared word pair or standalone sign-support
article. The new `words/寅.md` gives two translated examples, a direct
虎 quiz guard and one reciprocal pair with the new kanji card. No
transitive 寅/酔っ払い guard is inferred; original 虎/酔っ払い and
猿/馬鹿 guards remain unchanged. Actual kanji choices 演 / 黄 / 申
mean perform/stage, yellow and humbly say; 申's additional Monkey sign
does not identify the Tiger. Full applicable character records, dictionary
families and actual displayed labels support the bounded quiz audit.
The substantive 寅-shaped mnemonic in the existing N3 演 article gains
only a component link; its performance teaching and metadata are untouched.
午's incidental branch sequence does not by itself require a backlink.
The historical
[preparation audit](n1-sources/batch-048-preparation-audit.json) stays byte-preserved;
the [qualified-source audit](n1-sources/batch-048-qualified-source-audit.json)
adds exact Japanese sections, pinned SVG/converter and candidate font receipts
to fresh source/re-extraction, baseline and unchanged runtime checks.
The [draft audit](n1-sources/batch-048-draft-audit.json) records the current
source/baseline/readings/links/geometry/font, validation and archive checks.
This is an unreviewed local teaching draft, not linguistic acceptance,
native/phone acceptance or publication. Next conduct the same 048's
two serial blind different-model-family reviews on its signed snapshot;
fresh Android/native and publication gates still follow. Do not start 049. Accepted 047
is not reopened. Published coverage
remains **74 additions; 1,154 still to deliver**, not complete N1 coverage.
Earlier sections below retain their historical draft-stage wording;
their batch publication ledgers identify subsequent acceptance.

## Batch 047: local unreviewed draft

[Batch 047](n1-sources/batch-047-progress.json) bounds the next addition to
**卯**, frozen source row 130, on accepted published base `ab874b6`.
The [membership](n1-sources/batch-047-membership.json) fixes one character
after a complexity comparison of 辰・卯・丑・寅, not source-order selection.
The complete frozen packets retain **22 lexical and 17 disjoint comparison
families**, seven raw character records and coordinator inspection of nineteen
actual existing articles. Full source readings **ボウ・モウ / う**, five
strokes, grade 9 and canonical radical **卩 (26)** are preserved.

The packet separates the Rabbit sign from the living animal noun
`words/兎.md` (うさぎ), restricted year readings and search-only spellings.
Standalone 卯 has a second-lunar-month sense; the whole word 卯月 (うづき)
names the fourth lunar month. Neither is simply a Gregorian month number.
The [qualified-source evidence](n1-sources/batch-047-dictionary-evidence.json)
records eight exact Japanese dictionary sections across seven raw pages.
Daijisen explicitly allocates ボウ in 己卯・丁卯; an actual 辛卯 (しんぼう)
heading corroborates calendar recognition. ボウ remains recognition-only by
bounded usefulness choice, not obsolete or name-only. モウ remains explicitly
raw-source-only without an independently established word; no invented example,
invalidity claim or historical reading-class assertion is authorized.
卵・柳・印 supply inspected shape/component comparisons, not etymology.

Exact standalone う headings support one necessary sign article and sole-kun
practice in the local draft. Full ボウ・モウ / う metadata remains.
Daijisen 節旁 and the raw 卩 record agree on ふしづくり; the entire pinned
five-path SVG confirms the right-side 卩. Runtime geometry is generated with
the unchanged converter and must exactly match the qualified external candidate.
This is not visual or native acceptance. No baseline declared word pair is
activated and no existing runtime article changes.
The [preparation audit](n1-sources/batch-047-preparation-audit.json)
checks exact source bytes and complete re-extractions, baseline invariants
and unchanged runtime hashes; its historical bytes are preserved by the
[qualified audit](n1-sources/batch-047-qualified-source-audit.json).
The draft adds only `kanji/卯.md`, `words/卯.md` and `strokes/卯.json`.
No vocabulary level is inferred from the N1 kanji. One required reciprocal
pair connects the new kanji and sign article. Actual 卵, 柳 and 印 cards
provide three wrong kanji labels after their full meanings were checked;
the generic mark/sign of 印 is not the Rabbit branch. Direct 卯/兎 and
卯/東 word guards protect associated-animal and historical-east overlap
without asserting synonymy or transitive exclusions. Existing exclusions,
including 虎/酔っ払い and 猿/馬鹿, remain unchanged.

The [draft audit](n1-sources/batch-047-draft-audit.json) and
[stroke/font audit](n1-sources/batch-047-stroke-audit.json) record source,
baseline, exact membership, reading/link, manifest, budget and font checks.
Fresh complete frozen-family, selected Japanese-section and actual comparison
reads are distinguished from inherited historical receipts. Of 23 authored Han
characters, 21 occur in all three bundled fonts; 卩 and the source-link label's
旁 require fallback, with 旁 new to the exact base. Those glyphs require explicit
supported-native/visual disposition before publication, not a font substitution
or an inferred acceptance. Font cmap presence is not native readability.
This is an unpublished, independently unreviewed
draft; two serial blind different-model-family reviews, reconciliation,
fresh Android and applicable native/visual/integration/publication gates remain.
Do not begin 048. Published coverage remains
**73 additions; 1,155 still to deliver**, not complete N1 coverage.

## Batch 046: local unreviewed draft

[Batch 046](n1-sources/batch-046-progress.json) bounds the next addition to
**酉**, frozen source row 1105, on accepted published base `d76f2dd`.
Its [membership](n1-sources/batch-046-membership.json) and complete frozen
packets retain **16 lexical and 17 disjoint comparison families**, seven
raw character records and coordinator inspection of sixteen actual existing
articles. Full source readings are on **ユウ** and kun **とり**; seven
strokes, grade 9 and canonical radical **酉 (164)** are preserved.

The source packet distinguishes the Rooster sign from the living bird 鳥
and domestic chicken 鶏, and retains their food senses for later quiz review.
The [dictionary evidence](n1-sources/batch-046-dictionary-evidence.json)
records eight exact Japanese dictionary sections across seven raw pages.
Standalone **酉 とり** is verified; the character heading explicitly allocates
**ユウ** in **辛酉 しんゆう**, also read **かのととり**.
One necessary `words/酉.md` sign article and sole kun practice are drafted,
not independently reviewed. ユウ remains corroborated recognition, not source-only,
obsolete or name-only. The historical hour has multiple dictionary
mappings; its west and lunar-eighth-month senses do not make 酉 a replacement
for ordinary 西 or Gregorian August. Raw KANJIDIC2 radical-name
**ひよりのとり** differs from the verified Japanese heading **ひよみのとり**;
preserve the raw string rather than silently correcting it or teaching it as
established. **とりへん** is verified as a positional component name.
The alcohol sense of the whole expression 日読みの酉 does not make the
standalone sign noun an ordinary word for alcohol.
Pinned KanjiVG geometry verifies seven paths; the runtime strokes are generated
with the unchanged converter and exactly match the qualified external candidate.
Six-path 西 supplies a modern-shape comparison. 酉's extra interior
horizontal is not proof of historical derivation from 西.

The [draft audit](n1-sources/batch-046-draft-audit.json) and
[stroke/font audit](n1-sources/batch-046-stroke-audit.json) cover the three
runtime additions, fresh manifest, exact source membership, all baseline
metadata/strokes and authored-Han font coverage. The preparation and
qualified-source receipts remain byte-preserved historical records.
One reciprocal pair, 酉 / `words/酉.md`, is required; no baseline pair is
activated and no existing runtime article changes. Complete actual 配, 曲
and 画 cards supply three wrong kanji labels. Direct 酉/鳥 and 酉/鶏 word
guards conservatively protect the sign/associated-animal labels; 酉/西
protects the historical west sense. These are direct pairs, not transitive
synonym claims. Existing exclusions and both original 虎/酔っ払い and
猿/馬鹿 safeguards are unchanged.

Two serial blind different-family initial reviews, evidence-based reconciliation,
fresh non-skipped Android, applicable native/visual checks and all combined-main
publication gates remain pending. Font cmap presence is not native readability
or physical-phone acceptance. Do not push this unreviewed draft or begin 047.
Published coverage remains **72 additions; 1,156 still to deliver**.

## Batch 045: local unreviewed draft

[Batch 045](n1-sources/batch-045-progress.json) bounds the next addition to
**巳**, frozen source row 300, on accepted published base `a4f16c4`.
Its [membership](n1-sources/batch-045-membership.json) and complete frozen
packets retain **16 lexical and 16 disjoint comparison families**, six raw
character records and inspection of nine actual existing articles.
Full source readings are on **シ** and kun **み**; three strokes, grade 9
and canonical radical **己 (49)** are preserved. 己 and 已 remain separate
comparison characters, not additional batch members or replacement IDs.

The [dictionary evidence](n1-sources/batch-045-dictionary-evidence.json)
records **nine exact dictionary entries and one attributed editorial section
across eight raw pages**, not ten independent dictionaries or full-page reads.
Daijisen and Kanjipedia verify standalone **巳 み**, and explicitly allocate
**シ** in **上巳 じょうし**; Daijisen also verifies its alternative じょうみ.
The standalone JMdict family includes both み and し: シ is genuinely
corroborated recognition, not source-only, obsolete or name-only.
One necessary `words/巳.md` sign article and sole kun practice are now drafted,
not independently reviewed; no festival article is needed merely to offer another key.
The calendar families distinguish the Snake sign,
the living animal 蛇, the twelve-sign set and the sixty-term cycle.
Year expressions retain whole-word alternatives and spelling restrictions;
search-only へび年/ヘビ年 are not ordinary example spellings.
The actual Daijisen み entry permits approximately 10 a.m., an interval
around that time, or 10 a.m.–noon: no universal 9–11 a.m. conversion.
Lunar month four is not simply Gregorian April. 巳の日's frozen archaic
label is recorded, not generalized
to every contemporary cultural use. 辰巳's southeast sense is not
standalone 巳's historical south-southeast sense.

The complete pinned target SVG has three paths, inside a variant 己
radical group. The runtime stroke file is generated with the unchanged
converter and matches the qualified external candidate exactly.
Separate pinned 己/已 SVGs and the attributed look-alike editorial
support a modern third-stroke **upper-start** distinction, not different
bottom finishing endpoints or an all-font/native acceptance claim.
Kanjipedia's radical-image filename `48.png` is an asset name, not authority
to replace frozen canonical **己 (49)**. Prefer a labelled modern-shape
mnemonic and `structure-unclassified` rather than claim a settled origin.

The [qualified-source audit](n1-sources/batch-045-qualified-source-audit.json)
records the earlier exact inputs, complete re-extraction, baseline safeguards
and unchanged runtime hashes; the historical
[preparation audit](n1-sources/batch-045-preparation-audit.json) is byte-preserved.
The [draft audit](n1-sources/batch-045-draft-audit.json) and
[stroke/font audit](n1-sources/batch-045-stroke-audit.json) check the current
three runtime additions and fresh manifest. One reciprocal pair,
巳 / `words/巳.md`, is required; no baseline word pair is activated and
no existing teaching passage changes. Actual existing 包, 巻 and 記
provide three semantically wrong kanji choices. The direct 巳/蛇 word
guard conservatively protects the displayed Snake-sign/animal labels;
it is not a claim that the Japanese nouns are interchangeable.
Both original 虎/酔っ払い and 猿/馬鹿 safeguards remain unchanged.

The draft retains full シ/み metadata, selects only み, and supplies
qualified historical hour/direction/month recognition rather than ordinary
scheduling examples. Native 巳/己/已 and radical/font readability remain
unverified; cmap checks and pre-existing occurrences are not native evidence.
Two serial blind different-model-family initial reviews, evidence-based
reconciliation, fresh non-skipped Android, applicable native/visual checks
and all combined-main/publication gates remain pending. Do not push this
unreviewed draft, reopen accepted 044 or begin 046.
Published coverage remains **71 additions; 1,157 still to deliver**.

## Batch 044: local unreviewed draft

[Batch 044](n1-sources/batch-044-progress.json) bounds the next addition to
**亥**, frozen source row 17. Its [membership](n1-sources/batch-044-membership.json)
and complete source packets retain **17 lexical and 19 disjoint comparison
families**, seven raw character records and inspection of nine actual existing
articles. Full source readings remain on **ガイ, カイ** and kun **い**, in that
order; six strokes, radical 亠 (8) and grade 9 are preserved.
The [dictionary evidence](n1-sources/batch-044-dictionary-evidence.json) now
records five exact Japanese entry sections across four raw pages, not five
independent dictionaries or full-page inspections. One necessary **亥 い**
sign-noun article and sole kun practice are now drafted, not independently
reviewed. ガイ is
independently allocated in 辛亥 しんがい and 癸亥 きがい but remains recognition-only;
カイ is retained as frozen-KANJIDIC2-only and unselected, without an invented
example or a claim that its omission elsewhere invalidates it.

The draft compares the sign with accepted 猪 and 豚 without substituting a
sign noun for a live-animal noun. It distinguishes the twelve-sign cycle from
the sixty-term sense of 干支; it does not extend the twelve-sign えと sense to
every reading of that word.
Historical hour, direction and lunar-month senses retain their local register
labels. The packet supplies alternative historical hour intervals, not a
universal modern-clock conversion. Daijisen's actual い entry permits both a
two-hour interval around 10 p.m. and one following 10 p.m.; use a qualified
historical explanation, not a universal 9–11 p.m. rule. Its historical kana
ゐ is not a new modern reading, and lunar month ten is not simply October.
The pinned SVG has six paths, including the top 亠 group. Runtime geometry
generated by the unchanged converter must match the qualified non-runtime
candidate exactly. The [stroke audit](n1-sources/batch-044-stroke-audit.json)
records conversion and whole authored/comparison Han font-cmap checks, not
native tracing or visual acceptance.
No カイ compound occurs in these 17 lexical
families; that is not proof of global lexical absence or permission to erase
the sourced reading. The [preparation audit](n1-sources/batch-044-preparation-audit.json)
checks exact frozen inputs, complete re-extraction, baseline safeguards and
unchanged runtime hashes. It is not independent linguistic or native acceptance.
The [qualified-source audit](n1-sources/batch-044-qualified-source-audit.json)
adds exact entry/range/hash and geometry checks without replacing that
historical preparation receipt. The draft maps exactly one reciprocal
亥 / words/亥.md pair, with no activated baseline pair or reused passage.
The three inspected kanji choices are 刻, 交 and 亡; animal and calendar
labels are not made synonymous merely by their topics. The sign-specific
word label has no established ordinary synonymous current choice, so no
new direct exclusion is added. Independent review must still check this
decision against actual meanings and fallback choices.
The [draft audit](n1-sources/batch-044-draft-audit.json) records mechanical
checks; two-family review and acceptance/publication gates remain pending.
Published coverage remains **70 additions; 1,158 still to deliver**.

## Batch 043: local unreviewed draft

[Batch 043](n1-sources/batch-043-progress.json) bounds the next addition to
**麟**, frozen source row 1226, with one necessary **麒麟 きりん** word
article and 24-stroke geometry from the existing converter. The coordinator
inspected **50 complete frozen JMdict families**: 13 lexical, 12 initial
comparison and 25 additional disjoint comparison families, plus six raw
character records, 18 actual word articles and three kanji distractor
articles. The [membership](n1-sources/batch-043-membership.json) and historical
[preparation audit](n1-sources/batch-043-preparation-audit.json) remain intact.
This is author inspection, not independent review or publication.

The frozen full metadata remains **リン**, with no kun-reading. Radical 鹿 (198),
grade 9 and both source stroke-count annotations, **24 then 23**, are retained.
The [dictionary evidence](n1-sources/batch-043-dictionary-evidence.json)
records seven exact Japanese source sections and the pinned SVG. Its
verified blob has 24 paths, matching the primary count. Kanjipedia separately
labels a 23-stroke old form; this does not identify the exact glyph intended
by KANJIDIC2's unlabelled alternate annotation. The converted geometry
matches the pinned 24-path SVG; alternate evidence is not silently discarded.
Kanjipedia attributes a 鹿 plus phonetic 粦 analysis to Shinjigen; adopting
that analysis is optional, not permission to invent component history.

麒麟 きりん is the sole support article, with only **リン** offered for
practice and its own linked reading-table row. Its giraffe sense is usually
kana; the separate qilin sense
does not carry that flag. The archaic extraordinary-horse sense is restricted
to alternate 騏驎 in the frozen entry. 麒麟児 names a child prodigy;
botanical names, astronomical usage and the proverb have their own
restrictions, not a general rule that every compound means giraffe or genius.
Exact Japanese headings now corroborate キ plus リン allocation and both
animal identities. Daijisen additionally recognizes a gifted-person sense
of bare 麒麟, broader than the young-person 麒麟児 compound; retain that
source distinction when inspecting quiz choices. The word has no inferred
vocabulary level and does not invent a casual gifted-person example.
Usual-kana spelling applies to the giraffe sense, not a claim that the
pronunciation is rare. Kanjipedia's additional kun きりん differs from the
frozen empty kun list: document it without silently adding a practice key.

No baseline 麟 pair was activated. The sole new support pair is reciprocal;
no out-of-batch 麒 card was added. Eleven direct word-choice guards cover
four broad animal/creature labels, six person/individual labels and 鴻鵠's
great-person sense. 人物's ordinary talented-person secondary sense was
inspected, not dismissed because its title differs. Abstract 才能/能 and
adjectival 偉大 are not person nouns; 鹿 and 鳳凰 are distinct identities.
These guards are direct pairs, not transitive synonym cliques, and all
existing comparison articles remain unchanged. The actual kanji distractors
鹿/米/舞 have distinct meanings and already have three choices of their own.

The [draft audit](n1-sources/batch-043-draft-audit.json) records source,
baseline, exact tiger/monkey safeguards, metadata/readings, links, geometry,
whole authored/comparison Han and font coverage, validator/manifest,
Python/vocabulary and unchanged archive-budget checks. It is not linguistic
certification. **23 of 28 authored Han** are present in every bundled font.
New **粦・騏・驎・麒** and inherited **凰** require actual supported-native
fallback/readability and visual evidence before publication; inherited
comparison-only **广** also remains applicable. Cmap absence is neither a
demonstrated tofu failure nor a fallback pass. The initial reused zero-new-glyph
audit assertion exposed these four additions; they remain explicit pending
gates, not removed teaching or a silent font-acceptance claim.
Resume this same 043 at the signed unreviewed snapshot for
serial blind two-family reviews; fresh applicable Android/native/visual,
combined-main and publication checks still belong to later checkpoints.
No reviewer or Android/native process ran during drafting; nothing was pushed.
Accepted [batch 042](n1-sources/batch-042-publication.json) remains published
at terminal `be775040`: **69 additions delivered; 1,159 remain**.
Physical-phone/general-release qualifications remain outstanding; this local
source checkpoint does not change delivery or acceptance.

## Batch 042: historical textual-stage checkpoint

The bounded 雛 draft adds one kanji card, one necessary word article and
18-stroke geometry converted from the pinned SVG. It preserves all five
full readings and offers only **ひな・ひよこ**, with a separate linked
reading-table row and example for each. スウ is technical recognition in
post-hatching 育雛; ス and ジュ retain explicit source-only qualifications.
The word article keeps bird/doll/novice senses and usual-kana flags local to
their readings rather than presenting unrestricted substitution.

The coordinator inspected another **24 complete disjoint frozen families**
and the actual additional comparison cards: **67 families total**, not
67 supporting words. One support mapping, one reciprocal pair and 14 direct
word-choice safeguards are recorded in the
[draft ledger](n1-sources/batch-042-progress.json). Baseline articles, easier
levels and the tiger/monkey safeguards remain unchanged. Mechanical draft
checks cover all 34 authored Han characters; 33 are in every bundled font,
while the inherited radical glyph 隹 still needs applicable native/fallback
confirmation. They do not establish Android/native or physical-phone acceptance.

Two blind, different-family initial reviewers assessed the same signed
`79091e7` teaching snapshot. Both found no actionable teaching defect; their
[reconciliation](n1-reviews/batch-042-reconciliation.json) retains three optional
groups, complete original reports and source-based qualifications. Teaching
is unchanged, so no changed-passage confirmation was necessary. Exact execution
records verify all 41 assigned resources returned, including all 67 families,
24 comparison cards/articles and seven supplied Japanese dictionary sections.
The processes exited serially, with Claude's report archived before GPT started.
Claude's first two teaching reads overlapped once; the recorded 55/54 calls
and 1/0 internal overlaps do not establish strict tool serialization.
Supplied-source inspection is not independent upstream retrieval or proof
of comprehension. The original report's compressed usually-kana summary is
qualified against the actual entries: only the bird sense for ひな, both
bird and novice senses for ひよこ. The teaching already states this correctly.
Two failed launcher starts are preserved separately from successful reviews.

Fresh non-skipped Android, applicable native/article/visual acceptance and
combined-main publication gates remain pending. This is local textual
closure, not publication; public delivery remains **68 additions, 1,160 remaining**.

## Batch 042: historical source-preparation checkpoint

[Batch 042](n1-sources/batch-042-progress.json) freezes **雛**, source row
1168, for one evidence-bounded addition. All **43 complete frozen JMdict
families** were coordinator-inspected: 36 lexical families across all spelling
positions and seven disjoint comparisons. Five raw character records and six
existing bird/doll/child articles were inspected. The
[membership](n1-sources/batch-042-membership.json) and
[preparation audit](n1-sources/batch-042-preparation-audit.json) keep this
source-only work separate from teaching acceptance.

Full readings remain **スウ・ス・ジュ; ひな・ひよこ**, with 18 strokes,
radical 隹 (172) and grade 9. The exact ひな family has bird and festival-doll
senses; the separate ひよこ family has bird and novice senses. Shared 雛
spelling does not authorize unrestricted sense transfer. Bird-sense usual-kana
notation does not make the doll sense usually kana; the search-only ひよっ子
form is not ordinary spelling evidence. Small birds are not necessarily young
birds, and domestic chicken is not the entire chick category.

育雛 いくすう and 鳳雛 ほうすう are possible スウ anchors, not accepted
practice yet. Exact Japanese headings, allocation, register and useful examples
remain pending, especially the ambiguous equipment gloss in 育雛器. No lexical
ス or ジュ anchor was established in this packet; preserve the readings without
calling them invalid or name-only. Festival voicing, botanical names, technical
terms and promising-person idioms retain their own boundaries. No mandatory
extra support articles or historical/phonetic explanation has been adopted.

No declared baseline 雛 pair or existing 雛 word article was found. Runtime
cards, strokes and manifest remain unchanged. All source/baseline/runtime
mechanical checks and the extraction tests are recorded separately; they do
not establish linguistic correctness or native rendering acceptance.
Resume the same 042 with exact dictionary qualification before drafting.

Accepted [batch 041](n1-sources/batch-041-publication.json) is published at
terminal `035d6b0`: **68 additions delivered; 1,160 remain**. This new source
checkpoint does not increase delivery or claim physical-phone/general-release
acceptance. The older 041 narrative below preserves its textual-stage snapshot.

## Batch 041: historical textual-stage checkpoint

The bounded [draft ledger](n1-sources/batch-041-progress.json) now records
one 隼 card and one necessary はやぶさ word article, with ten strokes generated
from the pinned KanjiVG revision. All three readings remain in source order;
practice selects only はやぶさ. シュン has an archaic-compound recognition row;
ジュン is qualified character-source information without a selected lexical
anchor, not an invalid or name-only reading.

The coordinator inspected **25 complete frozen families**, including seven
additional broad-category and secondary-person comparisons. One reciprocal
pair and five direct word-quiz safeguards are recorded. Existing comparison
articles, their easier levels/readings and both accepted tiger/monkey guards
remain unchanged. The shape mnemonic is not etymology; the bird-name
explanation does not impose exclusive hawk/falcon taxonomy.

Both blind initial model-family reviews found no actionable defect in the
same frozen teaching snapshot, `75b4ae8`. The
[reconciliation](n1-reviews/batch-041-reconciliation.json) preserves both
complete reports, four nonblocking optional groups and actual process limits.
The two reviewer processes ran serially; Claude's one overlapping pair of
bounded XML reads is disclosed, not reported as strict tool serialization.
Both assigned scopes returned completely. Source access was supplied frozen
evidence, not independent upstream retrieval. Teaching remains unchanged.

This is **local textual closure**, not another published addition.
Fresh applicable Android/native/visual and combined-main/publication gates
remain pending. Published progress remains
67/1,228 additions, with 1,161 remaining. Physical-phone/general-release
acceptance remains explicitly outstanding.

### Preserved source qualification

The following source-stage observations preserve executions 182/183.
Their pending proposals describe those earlier snapshots, not the current draft.

[Batch 041](n1-sources/batch-041-progress.json) freezes **隼**, source row
1164, as one evidence-bounded addition. The coordinator inspected all
**18 complete JMdict families**: seven containing 隼 in any spelling position
and eleven disjoint exact comparison families. Seven complete raw KANJIDIC2
character records and nine existing comparison articles were also inspected.
The [membership](n1-sources/batch-041-membership.json) and
[preparation audit](n1-sources/batch-041-preparation-audit.json) separate
source inspection from teaching acceptance. 鷲, 鳶 and 鷺 were tentative
navigation candidates absent from the frozen named set, not added scope.

All source readings remain ordered: **シュン, ジュン; はやぶさ**.
The ordinary native falcon noun has usual-kana notation; grade-9/name-use
metadata does not make it name-only. A single はやぶさ support article is a
candidate, not yet authored. 鷹隼 ようしゅん is explicitly archaic in JMdict;
it must not become a "common words" anchor merely to force on-reading practice.
No ジュン word anchor was established in the inspected lexical families.
At the preparation checkpoint, exact Japanese character/word headings,
allocation, qualified lookup-only wording and final quiz subsets were pending.

Execution 183's [dictionary evidence](n1-sources/batch-041-dictionary-evidence.json)
now qualifies those reading proposals from five exact named Japanese source
sections. Daijisen and Kanjipedia independently list both on-readings and
はやぶさ. Daijisen marks ジュン as a conventional reading classification,
not name-only or measured commonness. The exact 鷹隼 ようしゅん entry in
Nihon Kokugo Daijiten supplies the hawk-and-falcon noun and historical evidence;
the archaic flag remains specifically JMdict's. Keep シュン as recognition-only
and ジュン as qualified character-dictionary information, each in its own row.
The proposed quiz lists are **empty on / はやぶさ kun**, not metadata deletion.
Only one necessary native noun article is proposed; no archaic compound article
is needed merely to populate practice.

The native noun sources distinguish a particular falcon from broader collective
use. Neither every occurrence's exact species nor an exclusive contrast with
鷹 is established. Actual 鷹 and 鳥 word labels support two proposed direct
guards; additional broad-category and secondary-person labels still need their
own full-family/quiz inspection at draft time. Kanjipedia's source-specific
origin analysis and alternative 鶻 spelling are recorded, not required
learner material or an excuse to expand the font/etymology scope.
The original lookup failures and misleading simplified Weblio extraction remain
explicit; successful raw headings, not URL success alone, support qualification.

Accepted 鷹 already teaches **hawk; falcon**. Do not manufacture an exclusive
hawk-versus-falcon distinction or use that label as a wrong falcon answer.
鳥 is the broader category. Any new support needs direct applicable quiz
guards, not transitive assumptions. 隹 is the canonical radical; comparisons
with 集's 木 base, 十 and 準 do not establish a historical or phonetic origin.
The complete packets also distinguish historical 隼人 and plant-name 隼人瓜
from per-character reading allocation, and kana-only spacecraft はやぶさ
from the native bird noun. Exact 速 そく is a gear suffix here, not source
evidence for 速い はやい or a はやぶさ etymology.

No declared baseline 隼 pair was found. At the source-only checkpoint, runtime
cards, strokes and manifest were unchanged; SVG conversion, independent teaching
review and fresh native acceptance had not started. Source inputs, exact packets, all original
metadata/strokes (with the two previously reviewed word exclusions) and every
current runtime hash are audited separately. Source-only extraction tests do
not certify linguistic correctness.

Accepted [batch 040](n1-sources/batch-040-publication.json) is published at
terminal `a93d39d`: **67 additions delivered; 1,161 remain**. The older batch
narratives below preserve their earlier local checkpoints. The current local
draft does not increase the delivered count or claim phone/general-release
acceptance. Continue the same 041 with serial blind independent review of the
signed draft; no batch 042 or second runner.

## Batch 040: peng textual review closed, acceptance pending

[Batch 040](n1-sources/batch-040-progress.json) freezes **鵬**, source row
1220, for a bounded mythical-bird and source-gloss check. All **25 distinct
complete JMdict families** were coordinator-inspected: nine lexical families
and sixteen disjoint comparison families. This initial source preparation was
not independent content review or publication. Execution 175 adds the
bounded local draft [鵬](../kanji/鵬.md) and one necessary
[鵬 (ほう)](../words/鵬.md) support article, without a vocabulary-level claim.
Both source readings remain ordered; practice selects only ホウ. The
おおとり row and word explanation retain its documented lexical alternate.
Direct broad-category quiz guards are recorded individually; comparison
articles remain unchanged. Draft validation and pinned stroke/font evidence
are recorded separately from two-family review, pending fresh Android,
applicable native/visual and combined-main publication acceptance.
Four supplemental complete dictionary families cover 動物, 生き物 and the
distinct せいぶつ／なまもの identities spelled 生物, for 29 families in all.

The frozen KANJIDIC2 gloss is "phoenix"; the applicable JMdict families
distinguish the **peng**, a giant mythical bird, from 鳳凰's fenghuang.
The raw gloss remains intact. The subsequent
[qualified-source record](n1-sources/batch-040-dictionary-evidence.json)
preserves seven exact Japanese dictionary sections and their inspection
ranges/hashes. Daijisen distinguishes the 鵬 of *Zhuangzi* from 鳳 referring
to 鳳凰; Kanjipedia independently documents 鵬 as an imaginary giant bird,
with **ホウ** and lexical **おおとり**. Full metadata remain in source order.
The shared おおとり family does not permit unrestricted bird-spelling
substitution or the performer spelling 大トリ.

Only **鵬 (ほう)** is drafted as necessary support and selected on-reading
material. おおとり is a documented lexical alternate, retained for recognition
rather than a second question; it is not name-only or invalid. The word-level
ぼう variant does not change the frozen sole on-reading. 鵬翼 and 鵬程 are
verified alternative literary anchors, not mandatory additions or ordinary
aviation/travel vocabulary. A historical literary 鵬程 example supports that
use, not invented casual collocations. Both independent initial reviewers
accepted this bounded teaching; no vocabulary-level assignment is inferred.

No declared baseline 鵬 pair was found. Existing bird and wing comparisons
were inspected unchanged; 翼's article teaches つばさ, not 鵬翼 ほうよく.
The pinned nineteen-stroke SVG has been converted with the existing generator;
the [draft audit](n1-sources/batch-040-draft-audit.json) and
[stroke/font audit](n1-sources/batch-040-stroke-audit.json) record exact checks.
The [textual reconciliation](n1-reviews/batch-040-reconciliation.json)
preserves two blind different-family initial reviews on signed `baa525f`,
with no actionable defect and four nonblocking optional groups. Both complete
reports and actual model/process/read evidence remain intact: 39/44 tool
calls, zero internal overlaps and zero XML-range violations. All assigned
teaching, 29 complete families, raw metadata, comparisons, guidance and seven
supplied Japanese sections returned. GPT's missing auxiliary source-file
lookup and irrelevant simplified web extractions remain explicit limits;
the coordinator separately reverified exact frozen membership and hashes.
The sourced phonetic explanation is valid optional enrichment, not a reason
to call the labelled mnemonic incorrect. Teaching is unchanged; no follow-up
review was needed. Fresh Android and applicable native/visual/combined-main
publication gates remain pending.
The historical [preparation audit](n1-sources/batch-040-preparation-audit.json)
checks frozen inputs, full-family membership and exact baseline/runtime
preservation, not linguistic certification.

Accepted [batch 039](n1-sources/batch-039-publication.json) remains published
at terminal `3c1735f`: **66 additions delivered; 1,162 remain**. This
local textually review-closed draft is not added to that delivered count and makes no new
Android/native/phone claim. Compatible Android `f9b59a2` or later remains
required; physical-phone/general-release acceptance is explicitly outstanding.

## Batch 039: many-reading goose unreviewed local draft

Batch 039 now drafts **鴻**, source row 1219, with two necessary support
articles, without independent acceptance or publication. Its [membership](n1-sources/batch-039-membership.json) selects one
grade-9, five-reading character after comparing the frozen 鴻 and 鵬 records;
this is not alphabetical selection. Full コウ・ゴウ and
おおとり・ひしくい・おおがり order is preserved.

The [source ledger](n1-sources/batch-039-progress.json) records all 17 complete
lexical families containing 鴻 at any written position and 20 disjoint
comparison families, fully coordinator-inspected. It distinguishes the
usually-kana ひしくい species noun, shared おおとり spellings, figurative
鴻鵠/鴻毛 candidates, poetic/historical compounds and the ホンモン product
name. Frozen taxonomy and proverb translations are evidence to qualify,
not independently certified teaching. The original frozen packet did not
establish ゴウ or おおがり anchors; absence there was not invalidity.

The [exact Japanese evidence](n1-sources/batch-039-dictionary-evidence.json)
now qualifies all five readings without changing metadata. Actual Daijisen
**大雁／鴻（おおがり）** verifies an alternate name for ヒシクイ and, separately,
ガチョウ; this reading is lexical recognition, not merely source-only.
Kanjipedia and Daijisen support コウ in **鴻鵠（こうこく）**, large birds
figuratively representing great persons, with an attested proverb context.
The authored support is one native **鴻（ひしくい）** article and one
**鴻鵠** article, not a required additional 鴻毛 article. Practice selects
コウ・ひしくい; both have their own linked reading rows.
おおとり and おおがり remain documented but unselected.
ゴウ is narrowly character-source-only in this bounded inspection, not
invalid, universally absent or name-only.

Usually-kana spelling does not make ひしくい a rare pronunciation. Current
scientific taxonomy remains unverified and excluded from proposed teaching.
The shared おおとり spelling family does not license unrestricted substitution
of 鴻 for 鳳凰, and the frozen proverb's phoenix gloss is not established
component taxonomy. The exact Japanese proverb uses large birds as its
metaphor. No everyday-frequency or vocabulary-level claim follows.

Eleven named external entry sections and both complete frozen packets
were freshly coordinator-inspected for this qualification; whole downloaded
HTML pages and independent reviewer retrieval are not claimed. Actual
support/comparison quiz labels and secondary senses are now inspected against
the actual articles, with ten additional disjoint complete families (47 total).
Two reciprocal pairs are accounted for, with no declared baseline 鴻 pairs.
Direct generic-bird/animal/living-thing guards, the shared large-bird new-word
pair and the magnanimous secondary-sense 鴻鵠/鷹揚 guard are recorded without
changing existing cards or making exclusions transitive.

The [draft audit](n1-sources/batch-039-draft-audit.json) and
[stroke/font audit](n1-sources/batch-039-stroke-audit.json) record source
identity, baseline preservation, exact pinned 17-stroke reconversion, whole
authored Han/font inspection and local checks: 28 of 29 authored Han are in
all three bundled fonts; only inherited 凰 is missing, with no new fallback
glyph. This is not fresh native acceptance. The labelled modern-shape
mnemonic is not etymology; vocabulary levels and current Latin taxonomy are
not inferred. The native examples use ordinary kana spelling; 鴻鵠 uses the
attested 鴻鵠の志 phrase rather than an invented casual collocation.
Fresh independent reviews, any new fallback's supported native disposition,
Android and combined-tree/public-archive gates remain pending. The original
source-only audits remain historical, not current no-draft assertions.
Published coverage remains **65 additions;
1,163 still to deliver**, with compatible Android and outstanding
physical-phone/general-release qualifications unchanged.

## Batch 038: mythical-bird published with bounded native acceptance

Batch 038 now has one **鳳** card and one necessary **鳳凰（ほうおう）**
support article, without an inferred vocabulary level. Full ホウ・フウ order
and the empty kun list remain unchanged; only ホウ is selected with its own
linked example. Traditional male/female pairing, lexical おおとり and the
Chinese-versus-Western phoenix distinction are qualified in the teaching.
One reciprocal pair and a conservative direct 鳳凰/鳥 quiz-label guard are
recorded; no baseline article is changed and no 凰 kanji card is added.

The three kanji distractors are 風, 鶴 and 鷹, with their actual titles and
complete articles inspected. Six existing word articles support comparison
and the original picture/cloth-pattern examples. The full pinned 82-line
SVG converts to 14 strokes with the existing generator, with exact
reconversion recorded in the [stroke/font audit](n1-sources/batch-038-stroke-audit.json).
All 14 Han in the two authored files and all 79 across the ten unchanged
comparison articles were checked against the three pinned bundled fonts.
**凰 is newly introduced and absent from all three cmaps:** actual bounded
native fallback and original-reviewer visual acceptance now pass in the
[native record](n1-reviews/batch-038-native-acceptance.json). The character
is readable and distinct from 皇, 鳳 and 風 under four configured production
families, but uses the same unidentified Gothic-like system fallback raster,
not four bundled font designs. Cmap absence alone is not a glyph failure.

The [mechanical draft audit](n1-sources/batch-038-draft-audit.json) checks
exact source membership, baseline preservation, mappings, readings, runtime
changes and budgets. It does not establish linguistic closure.
Two blind initial reviews, **Claude Opus 5.5** and **GPT-6.1 Sol**, reviewed
the same unchanged signed teaching snapshot `e18a46a`. Their
[reconciliation](n1-reviews/batch-038-reconciliation.json) establishes no
actionable textual defect; four optional expansion groups remain nonblocking.
Both complete original reports and actual model/read/process receipts are
preserved. The first process exited and its report was archived before the
second launch. Claude's one internal two-tool overlap is recorded, not
misrepresented as serial tool compliance; GPT had none. Both used supplied
dictionary evidence, not independently retrieved upstream sources.

The [review audit](n1-sources/batch-038-review-audit.json) verifies returned
ranges for both complete teaching files, all 45 distinct dictionary families,
seven raw character records, ten comparison articles, guidance and six supplied
Japanese entry ranges. The seven-family core overlaps the lexical packet and
was not reread or counted separately by either reviewer. Fresh 361 Python
tests, content/vocabulary checks, unchanged manifest, source/baseline/link/
reading/stroke/font audit and original budgets pass. No teaching correction
or unnecessary textual follow-up was made.

Two native terminal cases pass with no skips: one full production import
offline, reciprocal/system-back navigation and 16 native glyph probes.
The exact complete archive imports once with 1,050 kanji, 5,007 words,
70 N1-labelled cards, zero problems and accepted-reading parser epoch 1.
Eight original-Claude visual returns support bounded readability; their
900×2000 bytes are separately archived from the 1080×2400 sources.
Offscreen article/table contents, including horizontal clipping, are not
certified.

Fresh named Android tests pass 3+1 with no failures, errors or skips.
The [combined-tree acceptance audit](n1-sources/batch-038-acceptance-audit.json)
rechecks their exact XML/log/root/timestamp/hash evidence against unchanged
runtime, without rerunning resolved native/Android gates. Fresh 361 Python
tests, content checks, pilot vocabulary coverage (2,122/2,431), manifest,
source/baseline/link/reading/stroke/font audit and original budgets pass after
latest-main integration. The normally signed accepted commit `de06fc0c`
is owner-published with exact green CI and all **8,241** runtime hashes
verified in its immutable public ZIP. Original archive budgets, safe paths
and per-file limits pass; contributor-only evidence remains excluded.
The [publication record](n1-sources/batch-038-publication.json) preserves
these receipts. Terminal evidence publication is checked separately before
the coordinator yields; no batch 039 is started here.
Published coverage is now **65 additions; 1,163 to deliver**.
Compatible Android `f9b59a2` or later is required; physical-phone/
general-release acceptance remains explicitly outstanding.

### Preserved qualified-source preparation

The [frozen batch 038](n1-sources/batch-038-membership.json) selects **鳳**,
source row 1218, with grade-9/name-use classification, 14 source strokes and
ordered ホウ・フウ readings; its frozen kun list is empty.
The [source ledger](n1-sources/batch-038-progress.json) records complete
coordinator inspection of 34 lexical and 11 disjoint comparison JMdict
families. The seven-family core overlaps lexical evidence.

At the preceding source checkpoint, one necessary 鳳凰（ほうおう）support
article was proposed, not authored.
Six [exact dictionary entry/range/hash receipts](n1-sources/batch-038-dictionary-evidence.json)
now support ホウ allocation in that compound and the qualified traditional
male 鳳 / female 凰 explanation. This does not require every modern motif
to depict two separate birds or assign a fixed sex to a fictional character.
Use **Chinese phoenix / fenghuang** without importing the Egyptian/Western
phoenix's rebirth-from-ashes account; contextual or fantasy overlap is not
categorically ruled out. The exact Daijisen compound also records a crest
depicting the bird, supporting a scoped decorative-motif explanation.
JMdict recognizes lexical 鳳（おおとり）, although KANJIDIC2 places おおとり
under nanori rather than kun; do not silently change metadata classification.
Daijisen and Kanjipedia call it kun; this is not evidence that it is name-only.
The separate 大取（り）/大トリ last-performer entry does not make 鳳 its
ordinary spelling. No confidently allocated フウ example was established in
the bounded packet or inspected Japanese sections, not proof that it is
invalid or absent elsewhere. Kanjipedia lists ホウ・ブウ; its origin
paragraph's 凡（ハン→フウ） concerns the component, not an allocated 鳳
reading example. Preserve frozen ホウ・フウ and the empty kun list, with
only ホウ proposed for practice; do not manufacture a フウ anchor.
The search-only 鳳蓮草
spinach spelling and irregular species spellings are not teaching anchors.
凰 is not an addition in the frozen named set.

The complete core seven and comparison eleven families were freshly read;
the full 34-family lexical inspection is inherited from execution 157,
not claimed as a fresh whole reread. Distinct membership remains 45.
Original partial, unrelated and failed lookups are retained explicitly;
downloaded full pages are not claimed as fully inspected. Actual comparison
cards/quiz labels, support examples, strokes and all authored Han/font checks
were still pending at that source-only checkpoint.

That source-only checkpoint claimed no runtime, manifest, stroke, independent
review, fresh Android/native or publication change. Published coverage remains **64 additions;
1,164 still to deliver** after batch 037. Preserve the compatible-client
and outstanding physical-phone/general-release qualifications.

## Batch 037: snake published for bounded owner testing

The [frozen batch 037](n1-sources/batch-037-membership.json) contains only
**蛇**, source row 970. Its [source ledger](n1-sources/batch-037-progress.json)
records 108 complete lexical, eight original comparison and 23 disjoint
supplemental comparison JMdict families: **139 distinct families**.
Execution 149's complete original inspection is inherited, not a fresh
execution 151 lexical reread. The latter freshly inspected the complete core,
original comparison and supplemental packets. The eight-family core overlaps
lexical evidence; it does not increase the distinct count.
All four on-readings and the native へび remain in frozen source order.

Existing N2 蛇口 (じゃぐち) is the one baseline activation, with only its
substantive component backlink added; identity, vocabulary level and コック
exclusion remain unchanged. Necessary 蛇 (へび) and 蛇行 (だこう) support
articles are now reviewed without inferred vocabulary levels. Three reciprocal
pairs are recorded. Practice selects ジャ, ダ and へび with separate linked
reading rows; the complete source inventory remains unchanged.
The [qualified dictionary evidence](n1-sources/batch-037-dictionary-evidence.json)
now records seven exact Japanese entry/range/hash receipts. Daijisen assigns
蛇口 to ジャ and 蛇行 to ダ; じゃこう is a documented alternative, not an error.
委蛇 (いい／いだ), flagged obsolete in frozen JMdict, has ト・タル/classical
タリ constructions; Kanjipedia's character examples support 蛇's イ allocation.
It remains recognition-only. The frozen ヤ remains explicitly source-only:
no confidently allocated word was established, not a universal absence claim.
Kanjipedia's differing タ/イ inventory does not replace the frozen イ/ヤ.
Daijisen's separate じゃ lexical sense documents a heavy drinker, shortened
from 蛇之助; its historical quotation does not alone prove obsolete usage.
This is not ordinary へび meaning a drunk person. Actual full comparison cards,
displayed labels and complete applicable families support eight direct quiz
safeguards: broad animal/creature/organism and separate drunk-label overlaps
for 蛇, and broad bend/curve/wandering/unsteadiness labels for 蛇行. These are not unrestricted synonym
claims or transitive cliques. 虫・蚊・蛍 provide three distinct incorrect kanji
labels. The apparent 蛇スープ/えびスープ source discrepancy is retained but
excluded from teaching, not silently corrected.

The [draft audit](n1-sources/batch-037-draft-audit.json) records exact source
membership, frozen hashes, complete re-extractions, all original baseline
metadata/geometry and the two accepted 虎/猿 guards. The
[stroke/font audit](n1-sources/batch-037-stroke-audit.json) verifies the pinned
eleven-stroke reconversion and all 31 Han in the complete new and changed
articles. Thirty have glyphs in all three unchanged bundled fonts; **它 has
fresh bounded native fallback acceptance** in the
[native record](n1-reviews/batch-037-native-acceptance.json). Its system fallback
is readable and distinct, not four bundled designs or an identified face.
The modern-shape mnemonic is not an etymology. Cmap checks
and source hashes do not certify readability or linguistic correctness.

Batch 036 is [published and verified](n1-sources/batch-036-publication.json)
at terminal `8a8b538`: **63 additions delivered; 1,165 remain**.
Batch 037 has [combined-tree local acceptance](n1-sources/batch-037-acceptance-audit.json),
361 passing Python tests, unchanged runtime manifest and archive guards,
two serial blind different-family reviews with original-session confirmations,
and [evidence-based reconciliation](n1-reviews/batch-037-reconciliation.json).
Two findings are resolved; three optional groups and the original process,
source-access, disagreement and launcher-bound snapshot limitations remain.
Fresh Android checks passed three real-content cases and one rare-Han case.
Two actual native terminal cases verify the single full import, glyph probes,
offline support routes, reciprocal navigation and system Back. Eight images
received dependent original-Claude visual confirmation; returned images were
downscaled, and offscreen table/full-article contents remain unverified.
[Normal signed owner publication](n1-sources/batch-037-publication.json)
at accepted `a1871eac` passed exact green CI and immutable-public-ZIP
verification: all **8,238 runtime hashes**, manifest equality and unchanged
archive guards. This delivers **64 additions; 1,164 remain**, with
1,049 kanji, 5,006 words and 69 N1-labelled cards (68 named source members
plus the separate 妖 exception). Two necessary support words bring the
project's new-support total to 64; one reused support article changed.
Terminal evidence-only publication and its own CI/archive/issue receipts
are recorded in the live coordinator checkpoint; no teaching is changed.
Compatible-client and outstanding physical-phone/general-release limits
remain unchanged. Batch 038 had not started at that publication checkpoint.

## Batch 036: historical beast textual review

The account below preserves its earlier textual checkpoint; the publication
record above supersedes the pending delivery status without erasing evidence.

The [frozen batch 036](n1-sources/batch-036-membership.json) contains only
**獣** and needs two support articles: 獣 (けもの) and 獣医 (じゅうい).
Its [draft ledger](n1-sources/batch-036-progress.json) preserves all three
source readings in order; questions select ジュウ and けもの.
The alternate けだもの is genuinely attested for animals, not unmatched,
obsolete or insult-only. Exact Digital Daijisen headings also document its
abusive person sense. The alternate is explained on the same lexical article,
not duplicated or hidden by changing full metadata.

The initial source packet has 167 distinct complete JMdict families: the original
139 inspected at execution 144 and 28 supplemental comparisons inspected
at execution 145. Core families overlap rather than add to that count.
The [external evidence](n1-sources/batch-036-external-evidence.json) records
actual raw dictionary headings because simplified extraction omitted the
definitions. Dictionary inclusion is not a usage-frequency ranking.
Both blind model-family initials read that same signed snapshot. The
[reconciliation](n1-reviews/batch-036-reconciliation.json) preserves all four
original reports and the two original-session correction confirmations.
The source-backed corrections explain that writing 獣 for けだもの is outside
Joyo reading guidance, not a rare or obsolete pronunciation, and add the direct
獣/生き物 creature-label safeguard. One disjoint complete comparison family
brings the reviewed union to **168**, not another fresh read of the original
167. The actual Daijisen notation guide verifies its ▽ mark.

There are two required reciprocal pairs, no activated baseline pairs and
no reused article edits. Sixteen conservative direct word-quiz guards protect
the general beast label against animal/category labels; they do not make
different species synonyms. No vocabulary level is inferred from the kanji.
Pinned 16-stroke conversion and whole authored-text font checks are recorded
separately from independent linguistic or native acceptance.

Batch 035 is [published and verified](n1-sources/batch-035-publication.json)
at terminal `285df83`: **62 additions delivered; 1,166 remain**.
This textually closed local batch is not another delivered addition.
Fresh Android/combined-main/publication gates remain pending; compatible-client
and outstanding physical-phone/general-release limits are unchanged.
The initial Claude process had one internal tool overlap and a partial
Wiktionary retrieval; both are preserved, not claimed as serial/full lookup.
Its confirmation inherited the original two dictionary excerpts, while GPT
freshly reread them. All changed teaching, new family and notation-guide
confirmation reads returned completely. These are textual checks, not
native-speaker certification or physical-phone evidence.

## Batch 035: historical deer source preparation

The original source-only account below is historical; its publication record
above supersedes the pending status and totals without erasing that checkpoint.

The [frozen batch 035](n1-sources/batch-035-membership.json) contains only
**鹿**. Its [source-preparation ledger](n1-sources/batch-035-progress.json)
preserves 202 complete frozen JMdict families: 193 lexical families and nine
comparison families. Nine core lexical families and all nine comparison
families were inspected; the other 184 lexical families remain explicitly
pending. Extraction and hashes are not full linguistic review.

The initial inspection verifies 鹿/しか as a useful native animal noun and
identifies the existing N3 馬鹿 article's required component-link activation.
馬鹿 is whole-word ateji, not evidence that 鹿 supplies か in ばか.
Standalone 鹿/か is archaic; 鹿の子/かのこ has separate pattern, cloth,
mochi and archaic fawn senses. Full ロク/しか/か source order is frozen,
but final reading dispositions, support, quiz choices and teaching remain
pending. No card, support article, stroke file or runtime manifest changes
have been made in this source checkpoint.

Batch 034 is now [published and verified](n1-sources/batch-034-publication.json)
at terminal `e8176eb`: **61 additions delivered; 1,167 remain**.
Batch 035 is not another delivered addition. Resume the same bounded batch
for remaining family inspection and authoring before independent review;
compatible-client and outstanding physical-phone/general-release limits
remain unchanged.

## Batch 034: historical draft checkpoint

The account below preserves the pre-review checkpoint; its publication
record linked above supersedes the pending gates and totals.

The [frozen batch 034](n1-sources/batch-034-membership.json) adds **猪**
and one necessary 猪 (いのしし) article. All three readings remain in source
order: チョ, い and いのしし. Only いのしし is selected; チョ has verified
compound recognition, while the separately attested い noun is archaic.
The grade-9 name-use classification does not make the animal noun name-only.
No supporting-word vocabulary level is inferred from the kanji.

The [draft ledger](n1-sources/batch-034-progress.json) records 60 complete
frozen dictionary families in two packets, three reading dispositions and
one reciprocal pair. There are no activated baseline word pairs or reused
teaching edits. All original metadata, geometry and the two accepted
tiger/monkey safeguards remain preserved. Actual raw Digital Daijisen
headings were inspected because simplified extraction returned Wikipedia
or omitted definitions; those unsuccessful extractions are not evidence.

The [draft audit](n1-sources/batch-034-draft-audit.json) verifies source
membership, baseline/runtime preservation, links, readings, pinned 11-stroke
reconversion and unchanged budgets. All 17 displayed Han were audited:
16 occur in all three bundled cmaps; 犭 already appears in exact-base cards.
This does not constitute fresh native rendering or physical-phone acceptance.
361 Python tests, validation and manifest regeneration passed.
Two serial blind different-family reviews, fresh Android and combined-main
publication gates remain pending. No unreviewed content is published.

Batch 033 is now [published and verified](n1-sources/batch-033-publication.json)
at terminal `5f4ee985`: **60 additions delivered; 1,168 remain**.
The local batch-034 draft is not another delivered addition.
Compatible Android `f9b59a2` or later is required; physical-phone/general-release
acceptance and final whole-set reconciliation remain outstanding.

## Batch 033: historical textual closure checkpoint

The account below preserves the pre-publication checkpoint; the publication
record linked above supersedes its pending publication gates and totals.

The [frozen batch 033](n1-sources/batch-033-membership.json) adds **豚**
and one necessary 豚 (ぶた) word article. The existing N5 豚肉 (ぶたにく)
article changes only its component backlink. Both full source readings,
トン and ぶた, remain in order; only ぶた is selected. 養豚 (ようとん)
supplies compound recognition without an extra support article or a claim
that the unselected reading is rare.

Both blind model-family initials established no actionable defect in the
unchanged teaching and accepted the two drafted direct word-quiz guards:
豚/豚肉 for the ordinary pork sense and 豚/ぶうぶう for the child-language
pig noun. Digital Daijisen's actual noun definition supports the latter;
JMdict's car-only noun sense does not negate that separate evidence.
The [reconciliation](n1-reviews/batch-033-reconciliation.json) preserves
both original reports, three nonblocking suggestions and actual execution
receipts. All assigned teaching, 160 complete dictionary families, raw
metadata, three kanji/eight word comparisons and current guidance returned.
Both reviewer processes and their internal tool calls were serial.
Claude relied on supplied external evidence; GPT independently fetched the
豚 and 養豚 entries and directly inspected the supplied raw Daijisen section.
Returned text and model agreement are not linguistic or native certification.
No teaching change or unnecessary confirmation was required.

The [fresh audit](n1-sources/batch-033-review-audit.json) verifies 361 Python
tests, validation, unchanged manifest, exact source/baseline/link/reading
checks, pinned 11-stroke reconversion and archive budgets. All 22 displayed
Han were audited: 20 occur in all three unchanged bundled cmaps; missing
炒 and 豕 already appear in exact-base cards. Inherited pilot/font evidence
is limited to unchanged production scope, not new native acceptance.
The two earlier reviewed baseline guards, 虎/酔っ払い and 猿/馬鹿, remain
preserved. Fresh batch-033 Android, latest-main integration, signing,
owner publication, green CI and every immutable public ZIP runtime hash
remain pending. Public coverage stays **59 additions; 1,169 to deliver**;
local drafted coverage is not delivery. Compatible Android `f9b59a2` or
later is required; physical-phone/general-release acceptance and final
whole-set reconciliation remain explicitly outstanding.

## Batch 031: monkey published and verified for bounded owner testing

The [frozen batch 031](n1-sources/batch-031-membership.json) adds **猿**
and activates the component link in the existing N3 猿 (さる) article.
No new support word or vocabulary level is added. Both full readings remain
in source order; only さる is selected. 類人猿 (るいじんえん), "ape,"
supplies compound recognition for エン. Broad animal usage, the Monkey sign
written 申, compound voicing in 日本猿 and insulting person uses are kept
distinct.

The [draft ledger](n1-sources/batch-031-progress.json) records 177 complete
dictionary families in three bounded packets, two reading dispositions and
one activated reciprocal pair. A narrow additive 猿/馬鹿 exclusion addresses
the existing derogatory fool/idiot sense in an uncontextualized word quiz.
All other reused metadata, easier levels, titles, readings and prose remain
unchanged. Both blind model-family initials independently accepted this exact
guard and established no actionable defect in the unchanged teaching.
The [reconciliation](n1-reviews/batch-031-reconciliation.json) preserves both
complete original reports and two optional navigation/spelling-presentation
suggestions. All assigned teaching, 177 full families, raw metadata, five
kanji/ten word comparisons and current guidance returned completely.
Reviewer processes exited serially; Claude started the two teaching-file
reads together once and disclosed that breach, while GPT had no internal
overlaps. Both independently fetched the actual 猿 entry; only GPT fetched
類人猿 and independently counted the families. No equal-depth, wholly serial
internal-tool or native-speaker certification is claimed. No teaching fix or
unnecessary full-packet confirmation was required.
The 13 generated strokes match the pinned SVG reconversion. All 20 Han in the
new/changed files were audited: 18 occur in all three bundled font cmaps;
missing 犭 and 袁 already appear in the exact-base 犬 and 園 cards,
respectively. No new fallback code point or native certification is claimed.
The [acceptance audit](n1-sources/batch-031-acceptance-audit.json) preserves
the original execution-125 permission denial and exact parent recovery:
all three RealContentTest cases and one RareHanTest case passed without
failures, errors or skips against this dedicated content checkout.
The fresh combined-main checks passed 361 Python tests, validation,
vocabulary consistency, exact baseline/source/link/reading/stroke/font
audits and manifest/archive budgets. Both reviewed additive baseline
quiz guards, 虎/酔っ払い and 猿/馬鹿, remain explicit exceptions.

The [publication record](n1-sources/batch-031-publication.json) verifies
normal signed owner publication at accepted `29775f9`, green CI and all
8,218 runtime hashes in the exact immutable public ZIP. This delivers
**58 additions; 1,170 still to deliver**: 1,043 kanji, 4,998 word articles,
63 N1 labels and 62 named-source members plus the separate 妖 exception.
Compatible Android `f9b59a2` or later is required; physical-phone/general-release
acceptance and final whole-set reconciliation remain explicitly outstanding.
Earlier sections retain their historical states.

## Batch 030: tiger textually review-closed, not published

The [frozen batch 030](n1-sources/batch-030-membership.json) adds **虎**
and activates the component link in the existing 虎 (とら) article.
That word retains its N3 vocabulary label, identity, readings and teaching.
The reciprocal link and one narrowly justified additive quiz exclusion change;
no new word article is needed.
Both sourced readings remain in order; only とら is selected. コ has
the verified 虎穴 (こけつ) recognition example, with literal tiger-den
and figurative dangerous-place meanings separated from English "lion's den."
The animal and colloquial drunk-person senses remain distinct.

The [draft ledger](n1-sources/batch-030-progress.json) records 136 complete
lexical/comparison families, both reading dispositions and one activated
baseline/reciprocal pair. The eight strokes are generated at the pinned
KanjiVG revision. Of 14 displayed Han, 13 are in all three unchanged bundled
cmaps; 虍 already appears in the exact baseline 劇 card. This is not new
native or phone certification. Two blind model-family initial reviews both
identified the 虎/酔っ払い secondary-sense overlap: Claude called it optional,
whereas GPT established a minor ambiguity in an uncontextualized word quiz.
Animal-focused article prose does not contextualize a quiz showing only 虎.
The direct exclusion is added on 虎; 酔っ払い/酔う remains unchanged.
Both original sessions confirmed the exact safeguard and preserved
酔っ払い/酔う comparison; Claude withdrew its no-guard judgement.
The [reconciliation](n1-reviews/batch-030-reconciliation.json) retains
all four original reports. This is a shared observation, not a unique
model discovery merely because the initial labels differed.
The initial Claude run had one internal read overlap; later runs had none.
All prescribed initial scope returned; supplied versus independently
fetched dictionary evidence and bounded confirmation limits remain explicit.
Fresh Android/combined-main/publication gates remain pending.

The batch audit now applies all recorded exact replacements for a reused
article together. Its only permitted metadata exception is an explicitly
recorded, distinct, strictly additive `quiz_exclusions` safeguard; every
original exclusion and other metadata field must remain unchanged.
This is grounded in batch 030's inherited secondary-sense finding, not
permission to rewrite existing cards or widen exclusions transitively.
Fresh 361 Python tests and source/baseline/link/reading/stroke/font/manifest/
budget checks passed at the corrected teaching snapshot `ad82bdd`.
The conservative whole-file Han check includes the new nonrendered
exclusion metadata: 16 characters, 15 in all three bundled cmaps.
The original learner-visible body and inherited 虍 disposition are unchanged.

Batch 029 is now [published and verified](n1-sources/batch-029-publication.json)
at terminal `625cc32`: **56 additions delivered; 1,172 still to deliver**.
This local draft does not increase the published count. Compatible Android
`f9b59a2` or later is required; physical-phone/general-release acceptance
remains explicitly outstanding. Earlier sections retain historical states.

## Batch 029: bear textually review-closed, not published

The [frozen batch 029](n1-sources/batch-029-membership.json) adds **熊**
and one necessary 熊 (くま) word article. Both full readings remain in
source order; only くま is selected. ユウ has the specialized 熊胆
(ゆうたん) recognition example, not an animal-noun question or a medical
recommendation. The animal meaning, kana spelling, cub voicing and lexicalized
rake name are distinguished from English verbal "bear." No word level is
inferred from the kanji.

The [ledger](n1-sources/batch-029-progress.json) retains 113 complete
lexical/comparison families, one reciprocal pair, zero baseline activations
and one direct animal-category guard. The
[reconciliation](n1-reviews/batch-029-reconciliation.json) preserves both
blind different-family initial reports: no actionable defect, two optional
alternate-reading/repetition suggestions and unchanged teaching. The alternate
熊胆 heading is observed in both reports, not a unique model discovery.
All assigned local ranges returned completely. Reviewer processes exited
serially; Claude issued two bounded XML reads together (one overlapping
start), while GPT had none. Both independently inspected 熊胆; only GPT
independently fetched the 熊 animal entry. Exact process and source limits
remain explicit rather than claiming equal-depth or wholly serial tool work.

Batch 028 is [published and verified](n1-sources/batch-028-publication.json)
at terminal `d7c6c89`: **55 additions delivered; 1,173 still to deliver**.
Local batch 029 does not increase that count. Fresh 353 Python tests,
source/baseline/link/reading/stroke/font/manifest/budget checks passed.
Of 26 displayed Han, 25 are in all three unchanged bundled cmaps;
灬 is already displayed in the exact baseline 火/熱/照/点 cards.
This is not new native certification. Fresh Android/combined-main/CI/public-ZIP
gates remain pending. Compatible Android `f9b59a2` or later is required;
physical-phone/general-release acceptance remains explicitly outstanding.
Earlier sections retain their historical checkpoint states.

## Batch 028: turtle/tortoise textually review-closed, not published

The [frozen batch 028](n1-sources/batch-028-membership.json) adds **亀**
and one necessary native-noun support article in a local textually review-closed batch.
All four readings remain in source order; only かめ is selected.
キ has a verified 亀裂 (きれつ), "crack; fissure; rift," recognition
example. キュウ and キン remain source-only within this lesson, not
claimed absent from dictionaries or offered as animal-noun alternatives.
The broad animal meaning includes aquatic turtles and land tortoises.
The unexpected 乙 indexing radical stays separate from the animal meaning
and the explicitly labelled modern-shape mnemonic.

The [ledger](n1-sources/batch-028-progress.json) preserves 108 complete
lexical/comparison JMdict families, all reading dispositions, one reciprocal
pair and a direct animal-category quiz guard. No baseline component pair
is activated, no reused teaching changes and no vocabulary level is inferred.
The [external evidence](n1-sources/batch-028-external-evidence.json) records
actual sections, simplified-extraction omissions and an excluded wrong-entry
redirect. Source/draft checks are not independent review or native evidence.

Batch 027 is [published and verified](n1-sources/batch-027-publication.json)
at terminal `55ca3c1`: **54 additions delivered; 1,174 still to deliver**.
This local batch does not increase that count. The
[reconciliation](n1-reviews/batch-028-reconciliation.json) preserves both
blind different-family initial reports: no actionable defect, four optional
taxonomy/navigation/attribution/order proposals, unchanged teaching. All
assigned local ranges returned completely. Reviewer processes exited
serially, but Claude issued four concurrent guidance reads (three overlapping
starts); GPT had none. Original reports and actual model/read/process limits
remain preserved. Both independently fetched the actual Nikkoku animal/crack
definitions; simplified Daijisen/Jitsu bodies were absent, so their raw
reading lists remain supplied evidence, not independent reviewer retrieval.
Fresh Android/combined-main/publication gates remain pending.
Compatible Android `f9b59a2` or later and the explicitly
outstanding physical-phone/general-release status remain unchanged.
Earlier sections retain their historical checkpoint states.

## Batch 027: pigeon/dove draft, not reviewed or published

The [frozen batch 027](n1-sources/batch-027-membership.json) adds **鳩**
and one necessary word article, 鳩 (はと), in a local unreviewed draft.
All four source readings remain in order; only はと is selected for questions.
キュウ has a verified 鳩舎 (きゅうしゃ) recognition example. ク and
あつ.める remain explicitly source-only within this lesson, not invented
ordinary bird-name readings or a recommendation to replace 集める's spelling.
The gathering sense in 鳩首 is separately supported by actual dictionary notes;
grade-9 metadata does not make the ordinary noun a name-only reading.

The [ledger](n1-sources/batch-027-progress.json) retains 70 complete
JMdict lexical/comparison families, all four reading dispositions, one
reciprocal pair and two direct bird/animal category-label safeguards.
No baseline component pair is activated and no word level is inferred.
The [external evidence](n1-sources/batch-027-external-evidence.json) distinguishes
actual inspected definitions from empty extracted dictionary headings.
The [draft audit](n1-sources/batch-027-draft-audit.json) verifies frozen
inputs, exact baseline/runtime preservation, membership, readings, links
and unchanged archive guards. The [stroke/font record](n1-sources/batch-027-stroke-audit.json)
checks pinned 13-stroke geometry and all 28 displayed Han in all three
unchanged bundled cmaps. These are not independent review or native evidence.

Batch 026 is [published and verified](n1-sources/batch-026-publication.json)
at terminal `bfd9820`: **53 additions delivered; 1,175 still to deliver**.
Batch 027 does not increase that count. Two serial blind different-family
reviews, reconciliation, fresh Android and combined-main/publication gates
remain pending. Compatible Android `f9b59a2` or later is required;
physical-phone/general-release acceptance is explicitly outstanding.
Earlier sections below retain their historical checkpoint states.

## Batch 026: crane textually review-closed, not published

The [frozen batch 026](n1-sources/batch-026-membership.json) adds **鶴**
and one necessary word article, 鶴 (つる), in a local textually review-closed batch.
Both full readings remain in source order; only つる is selected. カク
has a qualified 鶴翼 (かくよく) recognition example, not a quiz key.
The [ledger](n1-sources/batch-026-progress.json) records all 57 complete
lexical/comparison families, one reciprocal pair, no activated baseline
pair and two direct category-label exclusions. No vocabulary level is inferred.

The raw KANJIDIC2 crane/stork glosses remain preserved. Actual modern
dictionary entries establish the ordinary crane noun separately from
コウノトリ, stork; poetic たず and origami おりづる are qualified rather
than silently added to the metadata. The [external evidence](n1-sources/batch-026-external-evidence.json)
distinguishes inspected dictionary sections from empty headings and preserves
raw-download provenance without claiming identical simplified output.

The [draft audit](n1-sources/batch-026-draft-audit.json) verifies exact source
membership, baseline/runtime preservation, reading/link dispositions and
archive budgets. The [stroke/font record](n1-sources/batch-026-stroke-audit.json)
verifies pinned 21-stroke geometry and all 13 displayed Han in all three
unchanged bundled cmaps. These checks are not new native or phone evidence.
The [reconciliation](n1-reviews/batch-026-reconciliation.json) preserves both
blind different-family initial reports: no actionable defect, three optional
shape/style/navigation proposals, unchanged teaching. All assigned local
ranges returned completely. Reviewer processes exited serially, but Claude
issued three concurrent guidance reads (two overlapping starts); GPT had
none. The original reports and actual model/read/process limits are retained.
Both independently fetched the crane/poetic/stork dictionary sections; GPT
also fetched the two compound definitions, while Claude used identical supplied
facts and frozen families for those. These are not equal-depth or native
certification. Fresh non-skipped Android and combined-main/publication gates
remain pending.

Batch 025 is [published and verified](n1-sources/batch-025-publication.json):
**52 additions delivered; 1,176 still to deliver**. This new local draft
does not increase published coverage. Compatible Android `f9b59a2` or later
is required; physical-phone/general-release acceptance remains explicitly
outstanding, not a blanket veto on bounded owner testing.

## Batch 024: sea-bream draft, not reviewed or published

The [frozen batch 024](n1-sources/batch-024-membership.json) adds **鯛**
and one necessary support article, 鯛 (たい), sea bream, in a local
unreviewed draft. Both complete source readings, チョウ and たい, remain
in order; only たい is selected, with its own linked reading row.
The [ledger](n1-sources/batch-024-progress.json) distinguishes this draft
from the **50 published additions; 1,178 still to deliver** after batch 023.

All 71 applicable lexical families and ten comparison families are retained
and author-inspected. They support the sea-bream noun, voiced まだい compound,
and the distinction between fish and fish-shaped たい焼き. Names containing
鯛 do not all designate sea bream; the raw source's English "red snapper"
gloss is preserved separately, not generalized into an unrestricted translation.
The [external evidence](n1-sources/batch-024-external-evidence.json) records
actual dictionary headings, the initial URL redirect and omitted simplified
page sections. Unavailable historical gaiji are not evidence for an origin claim.

The [draft audit](n1-sources/batch-024-draft-audit.json) verifies frozen inputs,
exact dictionary extractions, original baseline preservation, all prior runtime,
one reciprocal pair, no activated baseline pair and one direct 鯛/魚 quiz guard.
The [stroke/font record](n1-sources/batch-024-stroke-audit.json) verifies
19 generated pinned strokes and all 14 displayed Han in all three unchanged
bundled cmaps. This is not new native or physical-phone evidence.
353 Python tests, structural validation, manifest freshness and local budgets
pass. Vocabulary coverage remains the existing incomplete pilot stage.
Two serial blind model-family reviews, reconciliation, fresh non-skipped
Android checks and combined-main/publication gates remain pending.
No word level is inferred; compatible-client and outstanding physical-phone/
general-release qualifications remain unchanged.

## Batch 023: sweetfish published and verified

The [frozen batch 023](n1-sources/batch-023-membership.json) contains **鮎**
and one necessary support article, 鮎 (あゆ), sweetfish/ayu. Its
[batch ledger](n1-sources/batch-023-progress.json) preserves all four
metadata readings in source order and selects only **あゆ**. The complete
28 lexical/comparison families and exact external dictionary evidence
distinguish the Japanese fish noun from the character's catfish sense.
The raw KANJIDIC2 English glosses remain preserved; the teaching gloss uses
the exact JMdict species identity instead of generalizing to trout or smelt.
Historical formation explanations are not adjudicated; the visible-shape
mnemonic is explicitly not etymology.

One reciprocal support pair and one direct 鮎/魚 category safeguard are
recorded, with no activated baseline pair, reused teaching change or inferred
vocabulary level. Pinned 16-stroke geometry and original baseline preservation
are checked mechanically. The displayed 广 and 鯰 forms are absent from the
bundled font cmaps; their bounded supported-native disposition is now recorded
separately, not inferred from cmap absence or previous unrelated tests.

Both blind initial reviewers, actual `claude-opus-5.5` and `gpt-6.1-sol`,
reviewed the same signed teaching snapshot `43428b8`: both articles, all
28 complete dictionary families, five kanji/five word comparisons and all
three textual facets. Neither established an actionable defect or consequential
textual uncertainty. The [reconciliation](n1-reviews/batch-023-reconciliation.json)
preserves both original reports and four nonblocking Claude suggestions;
teaching remains unchanged without unnecessary confirmation reviews.

Reviewer processes exited serially and the first report was archived before
the second launch. Actual internal overlapping starts were **1/0**: Claude
read two bounded guidance passages together despite the one-call instruction.
The [execution audit](n1-sources/batch-023-review-audit.json) preserves that
deviation, zero XML range violations and complete returned assigned ranges;
returned bytes are not comprehension or native certification.

Fresh 353 Python tests, validator, unchanged manifest, vocabulary consistency
at its existing pilot stage and source/baseline/reading/link/stroke/font/budget
audits passed. Neither 广 nor 鯰 belongs to the inherited 40-character
fallback target set; no exact prior native disposition for them was established.

This batch is **published and verified for bounded owner testing**.
The [native acceptance](n1-reviews/batch-023-native-acceptance.json) retains
two actual terminal-status-0 cases, sixteen glyph/look-alike probes and one
complete production import per article attempt. Original-Claude directly
inspected five final screenshots in its original session: seven serial calls,
no actionable visual defect. 广 and 鯰 are legible and distinct in all four
configured families, with Gothic-like fallback rather than four bundled
designs. Offscreen table cells and the continuing row remain unverified.
The initial punctuation-selector failure and exact one-line harness-only fix,
both execution denials and parent recovery remain preserved.

The [combined-tree audit](n1-sources/batch-023-acceptance-audit.json) verifies
fresh Android 3+1 with no failures, errors or skips, 353 Python tests and
all source/baseline/reading/link/stroke/font/manifest/budget checks. Latest
main added only localization instructions through a normal signed merge;
N1 teaching and runtime stayed unchanged, so successful native/Android
checks were not redundantly repeated.

The [publication record](n1-sources/batch-023-publication.json) retains
signed acceptance `5fa725f`, green CI `41611151264` and every **8,195 runtime
hash** in the exact immutable public ZIP. All unchanged guards passed:
8,216 entries, 30,473,634 compressed bytes, 43,943,856 inflated bytes and
43,675,573 retained bytes. Published coverage is **50 additions; 1,178 still
to deliver**: 54 named source members plus the separate 妖 exception.
Compatible Android `f9b59a2` or later is required. No new session/drawing
retest or physical-phone evidence is claimed.
Physical-phone/general-release acceptance remains explicitly outstanding.

## Batch 021: silkworm published and verified

The [frozen batch 021](n1-sources/batch-021-membership.json) contains **蚕**
and one necessary support article, 蚕 (かいこ), silkworm. Its
[draft ledger](n1-sources/batch-021-progress.json) preserves all four source
readings in their original order. Only **かいこ** is selected for questions;
サン in 養蚕 and older/bound こ in 春蚕 remain recognition material, while
テン is explicitly source-only without an allocated teaching example.
The animal, cocoon, silk material and broader insect category are distinguished.
The support article has no vocabulary level inferred from its kanji and adds
one direct 蚕/虫 quiz safeguard.

The four bounded packets preserve 64 complete frozen JMdict families,
including all 48 with an 蚕-containing spelling. Historical standalone and
broader moth senses are kept separate from the ordinary larva lesson.
No existing baseline word declares 蚕, so no baseline component pair is
activated; the necessary new support pair links both ways. Existing accepted
繭 and 桑 teaching is unchanged. Source checks, generated strokes and font
cmaps are not independent review or phone evidence.

Both blind different-family initial reviews covered the same frozen teaching,
all 64 families and the actual comparison cards. The
[reconciliation](n1-reviews/batch-021-reconciliation.json) preserves both
complete original reports, three nonblocking optional dispositions and the
initial Claude internal read overlaps (7, versus GPT's 0). Reviewer processes
exited serially; the internal overlap is not reported as strict compliance.
No actionable defect or consequential unresolved claim remains.

The exact execution083 Gradle permission denial and parent exact-command
recovery are retained. Fresh RealContentTest 3/3 and RareHanTest 1/1 passed
without errors, failures or skips against this sibling checkout. The
[combined-tree acceptance audit](n1-sources/batch-021-acceptance-audit.json)
records 353 Python tests, frozen-source/baseline/reading/link/pinned-stroke/font
checks, manifest freshness and unchanged budgets. Latest main was already
integrated; runtime is unchanged from the recovered Android check.

The [publication record](n1-sources/batch-021-publication.json) records
accepted signed commit `f479944`, green CI `41601039760` and all 8,189
immutable public ZIP runtime hashes, with manifest version
`964691d97d61fa10`. All unchanged publishing guards pass.
This is **published and verified for bounded owner testing**:
**48 additions; 1,180 still to deliver**, with 52 named source members plus
the separate 妖 exception. Physical-phone/general-release acceptance is
explicitly outstanding; compatible Android `f9b59a2` or later is required.
Cmap checks do not establish a new native or phone pass.

## Batch 020: butterfly published and verified

The [frozen batch 020](n1-sources/batch-020-membership.json) contains **蝶**
and one necessary supporting article, 蝶 (ちょう), butterfly. Its sole
sourced on-reading **チョウ** is selected; both full and curated kun lists
are empty. The grade-9 classification is not a name-only restriction.
The [batch ledger](n1-sources/batch-020-progress.json) distinguishes this
review-closed teaching from published coverage and preserves 96 complete
lexical/comparison families across four bounded packets.

The support article has no vocabulary level inferred from its kanji.
One reciprocal pair and one direct 蝶/虫 category exclusion are recorded;
existing cards, metadata and exclusions are unchanged. The new meaning quiz
uses the actual 葉・世・採 labels, not the broader overlapping 虫 category.
The historical kana spelling てふ and word forms ちょうちょう/ちょうちょ
are separated from the modern single-character reading prompt.

Both blind different-family initial reviews covered the same frozen teaching,
all 96 families and actual comparison cards. The
[reconciliation](n1-reviews/batch-020-reconciliation.json) preserves both
complete original reports, five nonblocking optional dispositions and the
initial Claude internal read overlaps (2, versus GPT's 0). No teaching
correction or consequential unresolved claim remains; no unnecessary repeat
review was performed.

The exact execution079 Gradle permission denial is preserved alongside its
parent exact-command recovery. Fresh RealContentTest 3/3 and RareHanTest 1/1
passed without errors, failures or skips against this sibling checkout.
The [combined-tree acceptance audit](n1-sources/batch-020-acceptance-audit.json)
records 353 Python tests, source/baseline/reading/link/pinned-stroke/font checks,
manifest freshness and unchanged archive budgets. Latest main was already
integrated; no runtime change required repeating the recovered Android checks.

The [publication record](n1-sources/batch-020-publication.json) records
accepted signed commit `e3eeeb3`, green CI `41597325069` and every
immutable public ZIP runtime hash (8,186), with manifest version
`1021a2b2a00be884`. All unchanged publishing guards pass.
Published coverage is **47 additions; 1,181 still to deliver**.
Compatible Android `f9b59a2` or
later is required; physical-phone/general-release acceptance remains
explicitly outstanding, not inferred from source, cmap or JVM checks.

## Batch 019: mosquito published and verified

The [frozen batch 019](n1-sources/batch-019-membership.json) adds **蚊** and
reuses the existing N2 word article 蚊 (か), adding only its substantive
component link. No new support article, word level, primary reading or
exclusion is introduced. The [draft ledger](n1-sources/batch-019-progress.json)
preserves both ブン and か, selecting only the native animal noun for practice.
Digital Daijisen explicitly assigns 飛蚊症 (ひぶんしょう), seeing floaters,
to ブン; this medical recognition example is not a source-only reading.

Four complete packets preserve 65 lexical/comparison/example families,
including all 44 containing 蚊. Existing 虫 remains excluded against the
mosquito word; the new kanji uses three distinct wrong labels, 文・枚・改.
Both blind model-family initial reviews covered the same signed snapshot,
the new card and complete reused article, all 65 families and eight actual
comparison cards. The [reconciliation](n1-reviews/batch-019-reconciliation.json)
retains both original reports and a bounded original-Claude confirmation.
The modern short-reading source limitation and contextual counting-gloss
suggestion were withdrawn; whole-word reading polish remains optional.
No teaching change was needed. Claude's initial paired guidance reads remain
a disclosed process deviation, not retroactively corrected by the follow-up.

This is **published and verified for bounded owner testing**. The
[acceptance audit](n1-sources/batch-019-acceptance-audit.json) preserves the
exact execution 075 Gradle denial and parent-approved execution of that command:
fresh RealContentTest 3/3 and RareHanTest 1/1, zero errors, failures or skips,
with exact XML/log hashes, timestamps and the dedicated sibling root verified.
The fresh normal main merge was already up to date. Reviewed runtime is
unchanged; 353 Python tests, validation, manifest freshness, exact source/
baseline/reading/link/stroke/font audits and unchanged budgets passed.
The [publication record](n1-sources/batch-019-publication.json) records signed
accepted `78ef50d`, green CI `41593736884` and every **8,183 runtime hash**
from its exact immutable public ZIP. All nineteen learner-visible Han are
covered in the unchanged bundled cmaps; inherited pilot/native/all40/160font
scope is not a fresh native or phone pass.
**46 additions are published, 1,182 remain**. Compatible Android `f9b59a2`
or later is required; physical-phone/general-release acceptance remains
explicitly outstanding. Whole-set reconciliation and overall completion
remain pending.

## Batch 018: cocoon published and verified

The [frozen batch 018](n1-sources/batch-018-membership.json) contains **繭**
and one necessary standalone support article, 繭 (まゆ). No existing article
is changed. The [draft ledger](n1-sources/batch-018-progress.json) preserves
ケン・まゆ・きぬ in full source order and offers only まゆ.
The native Daijisen character heading explicitly assigns ケン to 繭糸;
that silk-production example is retained for recognition, not an extra quiz.
The source-only きぬ disposition acknowledges JMdict's whole-word
繭糸/きぬいと record without inferring ordinary standalone 繭/きぬ
spelling or character allocation from a kana substring.

Four complete packets retain **44 dictionary families**, including all
nineteen containing 繭. The teaching separates the cocoon covering, insect,
pupa and silk material, and distinguishes the eyebrow homophone 眉.
The [draft audit](n1-sources/batch-018-draft-audit.json) verifies exact source
membership, preserved baseline metadata/geometry, one reciprocal support
pair and the regenerated manifest. The
[stroke/font record](n1-sources/batch-018-stroke-audit.json) verifies the
pinned eighteen-stroke conversion and all twelve learner-visible Han
characters in all three unchanged bundled fonts; there is no new
outside-subset glyph. Cmap checks are not fresh native or phone evidence.

Both blind model-family initial reviews covered the same signed snapshot,
both teaching files, all forty-four families and the actual comparison cards.
The [reconciliation](n1-reviews/batch-018-reconciliation.json) preserves the
original reports, Claude's initial paired-read deviation and a bounded
original-session confirmation of the actual Daijisen character heading.
No teaching correction was needed; the proposed source-attribution change
and optional specialist/history expansions were withdrawn.

This is **published and verified for bounded owner testing**. Its
[publication record](n1-sources/batch-018-publication.json) preserves the
exact execution 071 Gradle denial and parent recovery, fresh non-skipped
Android 3+1 cases, combined-main checks, green CI and all 8,181 immutable
public ZIP runtime hashes at terminal `6855aed`.
At that checkpoint **45 additions were published; 1,183 remained**.
The compatible-client and outstanding physical-phone/general-release
qualifications remain unchanged; this is not complete N1 coverage.

## Batch 017: firefly published and verified

The [frozen batch 017](n1-sources/batch-017-membership.json) contains **蛍**,
one necessary animal-noun article and a single component link in the existing
N2 vocabulary article 蛍光灯. Its metadata, level, reading and exclusions
remain unchanged. The [draft ledger](n1-sources/batch-017-progress.json)
records both full source readings, ケイ and ほたる, and two reciprocal pairs.
Both readings are selected using exact lexical identities and the explicit
native character heading, not a substring of a compound's pronunciation.

Four complete dictionary packets retain 72 families. The
[native source record](n1-sources/batch-017-external-evidence.json) separates
the usually-kana noun, older 螢 spelling, firefly-family scope and historical
secondary senses. Two direct word guards protect the broader 虫 label and
the documented remaining-fire sense against 火; they are not unrestricted
synonym claims. No incomplete historical gaiji rendering is used as etymology.

The [stroke/font audit](n1-sources/batch-017-stroke-audit.json) verifies the
pinned eleven-stroke conversion. All 27 Han characters in the teaching were
checked against the unchanged bundled fonts: 26 are present; the older 螢
needs system fallback. Its [bounded native acceptance](n1-reviews/batch-017-native-acceptance.json)
now records eight probes across four configured production families: 螢 is
readable and distinguishable from 蛍, with the same Gothic fallback rather
than four distinct bundled older-form designs. The pilot's forty-target
font evidence is not extended to cover it by assumption.

This is **published and verified for bounded owner testing**.
The [reconciliation](n1-reviews/batch-017-reconciliation.json) preserves two
blind different-family initials on the same unchanged signed snapshot, all
three teaching files and all 72 dictionary families. Neither established an
actionable defect; four optional observations remain nonblocking. A bounded
original-Claude confirmation withdraws its mistaken dynamic-body inference
after inspecting the actual static Daijisen character and noun entries.
The [review audit](n1-sources/batch-017-review-audit.json) records serial
reviewer process exits and complete assigned returned ranges. Claude's initial
six-comparison-read overlap and GPT's truncated optional inventory introduction
remain disclosed; later serial work does not retroactively establish strict
initial compliance. Original-Claude dependent inspection of five native PNGs
found no actionable viewport defect; it is not another blind source review.
The original envelope, ambiguous-selector and ghosted-dialog attempts remain
preserved separately from the final two genuine terminal-status-0 cases.
The final attempt imported the entire exact archive through production
ContentSync once and exercised offline article, reciprocal-link and Back routes.
It does not claim a new meaning/drawing session or physical-phone test.

The [publication record](n1-sources/batch-017-publication.json) preserves fresh
non-skipped Android 3+1, combined-main source/baseline/reading/link/stroke/font
checks, 353 Python tests, green CI and every immutable public ZIP runtime hash
at accepted `becadff`. Published coverage is **44 additions; 1,184 still to
deliver**: 48 named source members plus the separate 妖 exception. Supporting
word levels are not inferred from kanji. Compatible Android `f9b59a2` or later
is required; physical-phone/general-release acceptance remains explicitly
outstanding. This is not complete N1 coverage.

## Batch 016: historical textual-closure checkpoint

The [frozen batch 016](n1-sources/batch-016-membership.json) contains **菊**
and one necessary supporting plant-noun article, 菊 (きく). Its
[draft ledger](n1-sources/batch-016-progress.json) preserves the single
source on-reading **キク** and explicitly empty kun list. Actual native
dictionary headings independently establish that the standalone noun uses
an on-reading; no native reading or vocabulary level is inferred.

Four full dictionary packets retain 152 families, including all 96
families containing 菊. Main-word spelling flags are kept distinct from
compound flags. The [native evidence](n1-sources/batch-016-external-evidence.json)
qualifies ornamental/food uses and historical or specialist secondary senses.
Seventeen conservative direct word guards protect broad plant labels and
documented secondary overlaps, not unrestricted equivalence or frequency.
One reciprocal pair is required; no baseline article is edited.

This is **textually review-closed local teaching**, not another published addition.
The [draft audit](n1-sources/batch-016-draft-audit.json) and
[stroke/font record](n1-sources/batch-016-stroke-audit.json) retain source,
baseline, reading, link, pinned-geometry and cmap checks. The
[reconciliation](n1-reviews/batch-016-reconciliation.json) preserves two blind
different-family initial reports on the same unchanged signed teaching,
with no actionable defect. Three optional suggestions remain nonblocking.
An original-Claude bounded confirmation completes its missing historical
guidance tail and confirms those dispositions, without a full packet rereview.
The [review audit](n1-sources/batch-016-review-audit.json) preserves actual
serial process exits, complete assigned teaching/family/comparison returns,
and the initial instruction-read overlap and guidance omission. Later tail
completion is not retroactive process compliance. Fresh Android and
combined-main/CI/immutable-public-ZIP gates remain pending. Published
coverage remains **42 additions; 1,186 still to deliver**.
Physical-phone/general-release acceptance remains explicitly outstanding.

## Batch 015: tree and resin published and verified

The [frozen batch 015](n1-sources/batch-015-membership.json) contains **樹**
and one necessary supporting article, 樹脂 (じゅし), resin. Its
[batch ledger](n1-sources/batch-015-progress.json) preserves both source
readings and selects only **ジュ**. The native spelling 樹/き is explained
as a dictionary-recognized alternative to 木/き; the material sense's
restriction to 木 is kept separate from broader character glosses.
No duplicate native-tree article or vocabulary level inferred from kanji
is added.

Four complete dictionary packets retain 234 families, including all
185 families with a 樹 spelling, their restrictions and all senses.
The [native evidence](n1-sources/batch-015-external-evidence.json) distinguishes
natural and synthetic resin and preserves failed or irrelevant lookups.
The new material article has four direct quiz safeguards, including 脂's
separate やに resin identity. One reciprocal pair is required; no reused
article or baseline metadata is changed.

These cards are **published and verified for bounded owner testing**.
The [reconciliation](n1-reviews/batch-015-reconciliation.json) preserves both
blind model-family initial reports on the unchanged signed teaching.
Neither established an actionable defect. Five optional suggestions were
adjudicated against the exact native bodies and complete frozen families;
the original Claude session clarified that its naturalness limit meant no
corpus/native-speaker check, not a consequential text-level uncertainty.

The [review audit](n1-sources/batch-015-review-audit.json) verifies serial
reviewer process exits and complete assigned text returned. It preserves
Claude's original one internal read overlap and three overlong XML ranges,
plus one limited read overlap in the dependent follow-up. The six bounded
XML tail rechecks were individually awaited and at most 200 lines each.
The original inaccurate range-limit claim was expressly withdrawn, not
rewritten as compliant initial review. No teaching or geometry was changed,
and no full packet rereview or native certification is claimed.

The [acceptance audit](n1-sources/batch-015-acceptance-audit.json) records
353 passing Python tests, exact frozen inputs and full dictionary extractions,
baseline/reading/link/stroke/font preservation and unchanged reviewed runtime.
Fresh Android RealContentTest (3 cases) and RareHanTest (1 case) passed with
no failures, errors or skips against this dedicated content checkout.
The original execution denial and the parent's exact-command recovery are
preserved separately; unchanged successful tests were not repeated.

The [publication receipt](n1-sources/batch-015-publication.json) records
normally signed acceptance `8c79b81`, green CI and verification of every
**8,172 runtime hash** in its immutable public ZIP. All original archive
guards passed: 8,193 entries, 30,436,446 compressed bytes, 43,875,726 inflated
bytes and 43,607,443 retained bytes. Published coverage is now
**42 additions; 1,186 still to deliver**. Earlier batch descriptions below
retain their historical checkpoint scope; their publication ledgers govern
actual delivery.
Compatible Android `f9b59a2` or later is required; physical-phone/
general-release acceptance remains explicitly outstanding. Pilot native
and all-40/160-font evidence is inherited only for unchanged production,
not claimed as fresh visual or phone testing.

## Batch 014: anatomical reading review closed, publication pending

The [frozen batch 014](n1-sources/batch-014-membership.json) contains **椎**
and one necessary anatomical support article, 椎骨 (ついこつ), vertebra.
Its [batch ledger](n1-sources/batch-014-progress.json) preserves all four
source readings in order and selects only **ツイ**. スイ and う.つ remain
explicitly source-only within this bounded lesson; 椎/つち is a verified
rare spelling of the mallet noun, not a rare pronunciation claim.

The source places しい under nanori, but complete JMdict families and
[actual native plant entries](n1-sources/batch-014-external-evidence.json)
independently establish 椎/しい and 椎茸/しいたけ as non-name lexical uses.
The draft explains that distinction without adding or reclassifying raw
metadata. Its four complete dictionary packets retain 117 families, one
required reciprocal pair and one direct broad-bone quiz safeguard.
No baseline metadata or reused teaching is changed; no word level is
inferred from the kanji level.

This is **textually review-closed local work**, not delivered coverage.
The [reconciliation](n1-reviews/batch-014-reconciliation.json) preserves both
blind model-family initials and both original-session confirmations.
Claude's localized tree-spelling omission and GPT's missing source-only
character gloss were corrected: the tree word is usually written in kana
according to JMdict, and Jitsu gives うつ "strike; hit with a mallet" without
establishing an ordinary modern spelling with that exact boundary.
The optional rare-mallet-spelling wording was also clarified.
Full metadata, order, quiz selections, supporting word and geometry are unchanged.

The [review audit](n1-sources/batch-014-review-audit.json) confirms serial
reviewer process exits and complete returned assigned text, but preserves the
initial internal parallel-call violations (1/32 overlapping starts).
Both bounded dependent confirmations ran internally serially (0/0);
this does not retroactively certify strict initial process compliance.
Fresh Android/combined-main/publication gates remain pending. Published additions
remain **40; 1,188 still to deliver**. Compatible Android `f9b59a2` or later
is required; physical-phone/general-release acceptance remains explicitly
outstanding. The older batch descriptions below retain their checkpoint
scope; batch 013's actual publication is recorded in its
[accepted receipt](n1-sources/batch-013-publication.json).

## Batch 013: textual review closed, publication pending

The [frozen packet](n1-sources/batch-013-membership.json) contains **榛**,
one grade-9 character bounded by hazel/alder homographs and reading-layer
complexity. Its necessary supporting article teaches はしばみ, Asian hazel;
the old alder name はり and established 榛の木 はんのき remain distinct.
All four source readings and their order are preserved; only **はしばみ**
is selected for questions. The source's ハン on classification is explicitly
attributed, not reconstructed from the whole word's kana.

The [draft ledger](n1-sources/batch-013-progress.json) records **41 complete
JMdict families** across four packets, one reciprocal pair, four direct
broader-label safeguards and no changed reused article or baseline metadata.
The [external evidence](n1-sources/batch-013-external-evidence.json) identifies
actual native dictionary headings and preserves failed navigation limits.
An optional unbundled character in the archaic vegetation compound is omitted
from runtime text, while its exact spelling/family remains in contributor
evidence and its dictionary link. No font or archive guard changes.

This batch is **textually review-closed locally**, not published coverage.
The [reconciliation](n1-reviews/batch-013-reconciliation.json) preserves two
serial blind different-family initial reports and both original-session
confirmations. GPT established one minor navigation omission: the substantive
実 (み) introduction now links the existing fruit/nut/substance companion.
Both reviewers confirmed the exact link-only correction; all other teaching,
metadata, exclusions and geometry are unchanged. Three Claude observations
remain optional, not expansion requirements.
The [review audit](n1-sources/batch-013-review-audit.json) verifies actual model,
process and returned-text receipts, source/baseline preservation and local
budgets. Fresh Android and combined-main/CI/immutable-public-ZIP acceptance
remain pending. Published coverage stays **39/1,228; 1,189 remaining**.
Supporting-word levels are not inferred from kanji. Compatible Android
`f9b59a2` or later is required; physical-phone/general-release acceptance is
explicitly outstanding, with pilot native/font evidence inherited only for
unchanged production scope.

## Batch 012: published and verified

The [frozen packet](n1-sources/batch-012-membership.json) is **桂・梢**:
a tree name with aromatic-tree, shogi and homophone layers, contrasted with a
tree extremity and an additional source-only kun reading. Two necessary support
articles supply two reciprocal pairs; no baseline-declared pair is activated
and no reused article or baseline metadata is changed.

The [batch ledger](n1-sources/batch-012-progress.json) preserves all five
metadata readings in order and selects **かつら・こずえ**. ケイ and ショウ
have verified non-name recognition examples; 梢's くすのき remains explicit
source-only lookup information without a manufactured camphor-tree example.
Four packets retain **88 complete JMdict families**. The
[external evidence](n1-sources/batch-012-external-evidence.json) identifies
the actual native/character/compound headings and their returned limits.
Eleven direct word safeguards address broader tree/plant/branch/tip/top labels,
not a transitive synonym clique. Optional ancillary spelling and water-form
literals outside the bundled cmaps were omitted from runtime text, with full
source spellings retained in contributor evidence and no font or guard changes.

These cards are **published and verified for bounded owner testing**.
The [reconciliation](n1-reviews/batch-012-reconciliation.json) preserves two
serial blind different-family initial reports and both original-session
confirmations. Two minor issues in 桂 were corrected: ambiguous English
"In other words" and a one-stroke description of 掛's two-stroke far-right
component. All four teaching files are CLEAN in the bounded textual scope.
Actual execution receipts retain the denied Claude Git HEAD view and partial
dictionary fetches; returned text is not comprehension or native acceptance.
The [publication record](n1-sources/batch-012-publication.json) retains the
exact parent-approved discovery recovery, fresh non-skipped Android cases,
combined-main validation, green CI and every immutable public ZIP runtime
hash at terminal `0410011`. Published coverage is **39/1,228; 1,189 remaining**.
Supporting-word levels are not inferred from their kanji. Compatible Android
`f9b59a2` or later is required; physical-phone/general-release acceptance
remains explicitly outstanding. Prior pilot native/font evidence is inherited
only for unchanged production scope, not a fresh native or visual pass.

## Batch 011: published and verified

The [frozen packet](n1-sources/batch-011-membership.json) is **梓・橘**,
two remaining grade-9 plant characters with printing, botanical naming,
historical citrus and name-use risks. Two necessary plant-noun support articles
provide two reciprocal pairs; neither activates a baseline-declared pair.
No reused teaching or baseline metadata changes.

The [draft ledger](n1-sources/batch-011-progress.json) preserves all **four**
source readings in order and offers **あずさ・たちばな**. シ and キツ
have actual printing/citrus examples and are retained for recognition, not
declared source-only or inferred from names. Four frozen packets contain
**71 complete JMdict families**. The
[external evidence](n1-sources/batch-011-external-evidence.json) distinguishes
actual native/on/character headings, empty extracted sections and a truncated
encyclopedia overview. Teaching separates Japanese azusa-tree naming from the
Chinese catalpa/printing layer and modern wild tachibana from older edible
mandarin uses, without manufacturing universal species or substitution rules.
Twelve direct word safeguards cover actual broader tree/plant/fruit/flower
labels; different species and named historical perfumes are not a synonym clique.
The first glyph audit caught ancillary 巫 and 枸 outside the bundled cmaps;
the optional runtime spellings were replaced with kana and English descriptions,
while the complete dictionary spellings remain in contributor evidence.
Source readings and selected questions are unchanged; no font or guard is modified.

Both blind model-family initials reviewed all four teaching files, all 71
complete families and the assigned twelve word/eight kanji comparisons on
signed `69f0b3b`. The
[reconciliation](n1-reviews/batch-011-reconciliation.json) preserves both
original reports, actual model/process/read receipts and six optional
observations; neither reviewer established an actionable defect.
Coordinator lookup corroborates the broader ordinary-bow sense of 梓弓
without invalidating the selected spirit-bow example. Incense wording,
additional botanical aliases and historical shape analysis remain optional
expansions, not mandatory corrections. Teaching is unchanged, so no changed-
passage confirmation is claimed or needed.
Both reviewer processes exited before successive launches, with zero observed
internal tool overlaps. Claude searched the confusable inventory; GPT recovered
its complete text after truncation and obtained citrus dictionary bodies through
raw HTML. GPT's denied `.git/HEAD` view is preserved, not represented as
independent Git verification or retried through another tool.

These cards are **published and verified for bounded owner testing**.
The [review audit](n1-sources/batch-011-review-audit.json) preserves textual
closure separately from [execution 041](n1-sources/execution-041.json) and its
[acceptance audit](n1-sources/batch-011-acceptance-audit.json): fresh
RealContentTest 3/3 and RareHanTest 1/1, with zero failures, errors or skips,
against the dedicated sibling content checkout. The actual combined-main tree
passed 353 Python tests, validation, unchanged pilot-stage vocabulary consistency,
manifest freshness and exact source/baseline/reading/link/stroke/cmap audits.
The [publication record](n1-sources/batch-011-publication.json) preserves
normally signed acceptance `84bdf2a`, green CI `41561580072` and all
**8,157 runtime hashes** from the exact immutable public ZIP, within unchanged
archive, per-file and path budgets. Reviewed teaching remains unchanged.
Published coverage is **37/1,228; 1,191 still to deliver**.
Supporting-word levels are not inferred from kanji. Compatible Android
`f9b59a2` or later is required; accepted pilot native/all40/160font evidence
is inherited only for unchanged production scope, not a fresh native or visual
pass. Physical-phone/general-release acceptance remains explicitly outstanding.

## Batch 010: textual review closure checkpoint (historical)

The [frozen packet](n1-sources/batch-010-membership.json) is **笹・椋**,
two grade-9 plant characters with complementary bamboo/category and tree/bird
risks. Two necessary support articles supply two reciprocal pairs; neither
character activates a baseline-declared pair. No reused teaching or baseline
metadata is changed.

The [draft ledger](n1-sources/batch-010-progress.json) preserves all **three**
source readings and selects **ささ・むく**. 椋's リョウ is independently
attested in the character-dictionary compound 椋樹 and retained for recognition,
not declared source-only or nonexistent because JMdict lacks that compound.
Three packets preserve **73 complete JMdict families**. The
[external record](n1-sources/batch-010-external-evidence.json) distinguishes
actually returned definitions from empty headings and an initial wrong-headword
redirect. Teaching qualifies the bamboo/sheath distinction, old court-language
alcohol sense and muku tree/fruit/abbreviated-starling uses.
Sixteen direct word safeguards address those actual senses and broader labels,
not a plant/fruit/bird synonym clique.

Both blind model-family initials reviewed all four teaching files, all 73 complete
families and the assigned actual comparisons on signed `6964071`. The
[reconciliation](n1-reviews/batch-010-reconciliation.json) records a localized
reading-restriction clarification: the short むく is restricted to 椋, whereas
the longer むくのき is unrestricted across all four listed spellings, including
椋 itself. Both original sessions confirmed the exact paragraph at `cdb179f`.
The subsequent font audit found that explicitly listing ancillary 樸樹 introduced
an unbundled glyph. The full spelling stays in contributor evidence; the final
paragraph says **all** listed spellings and gives the already taught examples,
without adding that unnecessary runtime alias. Both original sessions confirm
the final teaching at signed `3e23d42`; all 32 learner-text Han remain covered
by all three unchanged bundled fonts.
Claude withdrew the initial "backwards" characterization and recalibrated the
concern to comprehensibility; no reversed source restriction was established.
All six reviewer processes exited serially. The final Claude confirmation
discloses one internal two-read overlap; it is preserved, not claimed serial.
Unchanged files inherit their initial review rather than a claimed fresh reread.

These cards are **locally textually review-closed**, not delivered additions.
Fresh applicable Android and combined-main/CI/immutable-ZIP publication gates
remain pending. Published coverage stays
**33/1,228; 1,195 still to deliver**. Supporting-word levels are not inferred
from their kanji. Compatible-client and outstanding physical-phone/general-release
qualifications remain unchanged.

## Batch 009: published and verified

The [frozen packet](n1-sources/batch-009-membership.json) is **杏・李**,
two grade-9 fruit/tree characters with different lower components.
Two necessary standalone plant-noun support articles provide two reciprocal pairs;
neither character activates a baseline-declared pair. No reused article
or baseline metadata is changed.

The [ledger](n1-sources/batch-009-progress.json) preserves all **six**
metadata readings in source order and offers **あんず・すもも**.
杏's キョウ and アン remain useful compound-recognition information,
including both readings of 杏仁豆腐, without adding a kernel or dessert
article merely to generate a question. コウ is explicitly source-only;
李's リ is demonstrated by 李下 and its proverb, not by an inferred
personal-name reading. Question selection is separate from validity.

Two frozen packets preserve **66 complete JMdict families**. The
[external evidence](n1-sources/batch-009-external-evidence.json) records
actual headings and extraction limitations. The teaching distinguishes
apricot from ume despite overlapping English labels, and qualifies
すもも's broader botanical scope rather than making one species universal.
Sixteen direct word safeguards protect actual broader fruit/tree labels
and conservative ume/garden-tree overlaps, not a botanical synonym clique.

Both stroke files are generated at the pinned revision with seven strokes.
The [draft audit](n1-sources/batch-009-draft-audit.json) checks exact
dictionary extraction, source/baseline preservation, reading/link membership,
stroke reconversion, unchanged font cmaps and local archive budgets.
Both blind initial reviews covered all four teaching files, the full source
families and assigned actual comparisons on signed `09e480a`.
The [reconciliation](n1-reviews/batch-009-reconciliation.json) records one
minor lexical-origin correction: あんず is Chinese-derived even though
KANJIDIC2 lists it as kun. New 杏 word type/tag now uses kango, with the
source-backed distinction explained in both affected pages at `8534b89`.
Both original sessions confirm the precise correction without regressions.
The [origin evidence](n1-sources/batch-009-origin-evidence.json) identifies
the actual noun/history passages, not merely the plant's foreign origin.
Full readings/order, quiz keys, identities, examples and exclusions stay.

The five reviewer processes exited before successive launches. Both initials
had serial internal tools; Claude's confirmation had one approximately
7-ms view/fetch overlap. Its original report is preserved, and its inaccurate
seriality assertion is withdrawn in a bounded original-session supplement.
This disclosed deviation is not rewritten as perfect serial execution.

These two cards are now **published and verified for bounded owner testing**.
[Execution 035](n1-sources/execution-035.json) and the
[acceptance audit](n1-sources/batch-009-acceptance-audit.json) preserve fresh
RealContentTest 3/3 and RareHanTest 1/1, with no failures, errors or skips,
against this dedicated sibling checkout. The actual combined-main tree passed
353 Python tests, validation, unchanged pilot-stage vocabulary consistency,
manifest freshness and exact source/baseline/reading/link/font/stroke audits.
The [publication record](n1-sources/batch-009-publication.json) preserves
normally signed acceptance `add0c53`, green CI `41552908004` and all
**8,145 runtime hashes** from the exact immutable public ZIP within unchanged
archive, per-file and path budgets. Reviewed teaching remains unchanged.
Published coverage is **33/1,228; 1,195 still to deliver**.
Supporting-word levels are not inferred from their kanji. Compatible Android
`f9b59a2` or later is required; accepted pilot native/font evidence is inherited
only for unchanged production scope, not a fresh device or visual pass.
Physical-phone and general-release acceptance remain explicitly outstanding.

## Batch 008: published and verified

The [frozen packet](n1-sources/batch-008-membership.json) is **楓・楠**.
Two necessary new support articles provide two reciprocal pairs; neither
character activates a baseline-declared word pair. No reused teaching or
baseline metadata changes. The [ledger](n1-sources/batch-008-progress.json)
retains all **eight** source readings and selects **かえで・くす・くすのき**.
The two camphor-tree readings share one lexical identity, not independent
transfer or mastery evidence.

Two pinned packets preserve **52 complete JMdict families**. 楓's native
maple sense is distinguished from the separately indexed sweetgum noun ふう;
楠's four on readings remain explicitly source-only rather than being
manufactured from 石楠花 or name readings. Actual broader tree, plant and
material labels motivate twelve direct new-word safeguards, with conservative
contextual guards qualified separately from unrestricted synonym claims.
The [external evidence](n1-sources/batch-008-external-evidence.json) distinguishes
the irrelevant surname/place-name 楠 page from the verified native 樟・楠
headings. The unnecessary alternate spelling containing 槭 stays in the full
dictionary family, not learner text: it would introduce a new missing-cmap
character outside the existing forty-target evidence.

Both new cards use thirteen pinned generated strokes, without manual
geometry. New native spellings retain source metadata and dictionary-verified
allocations; supporting words have no vocabulary level inferred
from their kanji.
Two serial blind different-family initial reviews and both original-session
confirmations are [reconciled](n1-reviews/batch-008-reconciliation.json).
Claude identified a minor unclear reference to a maple-tree example in the
linked 紅葉 article; the new 楓 word article now states the conditional
もみじ/こうよう distinction directly. GPT did not identify that initial
defect and independently confirmed the exact correction without regression.
Optional expansions remain nonblocking and unadopted. Four actual review
processes exited successfully with no observed internal tool overlaps;
unequal inventory/live-source read depth is disclosed, not a model ranking.
The [publication record](n1-sources/batch-008-publication.json) preserves
fresh non-skipped Android, current-main, green CI and every immutable public
ZIP runtime hash at terminal `7d0fd6f`. Published coverage is
**31/1,228; 1,197 remain to deliver**.
The [draft audit](n1-sources/batch-008-draft-audit.json) and
[execution record](n1-sources/execution-030.json) distinguish 353 passing Python
tests and exact source/baseline/link/reading/font/stroke/local-budget checks
from textual closure and the later completed bounded owner-testing
publication gates. Physical-phone/general-release acceptance is not inferred.

## Batch 007: published and verified

The [frozen packet](n1-sources/batch-007-membership.json) is **柚・椿**.
Both have useful native plant nouns alongside more specialized source readings;
this is not an alphabetical slice or a claim that grade-9 characters are only
personal names. Two necessary new support articles, **柚・椿**, provide two
reciprocal pairs. Neither character activates a baseline-declared word pair,
and no reused article or baseline metadata is changed.

The [draft ledger](n1-sources/batch-007-progress.json) retains all **seven**
full readings in order, selecting only **ゆず・つばき** as question keys.
ジク and チュン remain explicitly source-only; the other on readings have
qualified recognition examples without unnecessary new word articles.
Two frozen packets preserve **30 complete JMdict families**, including
spelling/reading/sense restrictions, archaic forms and comparison identities.
The [external evidence](n1-sources/batch-007-external-evidence.json) separates
actual dictionary headings from two failed culinary lookups and an irrelevant
successful page extraction. Yuzu is not equated with every English "citron";
椿's mountain-tea and incident uses are not imported into native つばき.
The initial ten direct new-word guards cover fitting generic tree, plant,
fruit and flower labels, not transitive synonym groups. A supplemental
complete 植木 family now supports two conservative direct garden-tree
guards, bringing the totals to **31 families and twelve direct guards**.

The [pre-freeze iteration](n1-sources/batch-007-draft-iteration.json) records
an initial glyph-audit failure: the optional spelling 海石榴 introduced 榴,
outside both the bundled cmaps and the accepted forty-target fallback
evidence. That unnecessary alias was omitted from learner text, not from
the complete source family; the unchanged audit still checks every new
runtime character. This is not a native rendering failure or new fallback
acceptance. Pinned strokes use 9/13 source strokes with no manual geometry.
The [draft audit](n1-sources/batch-007-draft-audit.json) and
[execution 026](n1-sources/execution-026.json) record 353 passing Python tests,
validator/vocabulary/manifest checks, exact source/baseline membership and
reading/link integrity, and local budgets. Both new card glyphs are in all
three unchanged bundled cmaps; existing 椒/氵 omissions are not newly accepted
fallbacks. These local checks do not replace the remaining acceptance gates.

Independent `claude-opus-5.5` and `gpt-6.1-sol` initial reviews covered the
same signed `33e9c94` snapshot: all four teaching files, thirty complete
families, eleven actual kanji and thirteen word comparisons. Both original
sessions confirmed signed correction `267bbbf`: only 植木 was appended to
each new word's exclusions. All four processes actually exited serially,
with zero observed internal tool overlaps.

The [reconciliation](n1-reviews/batch-007-reconciliation.json) preserves
the original reports, actual read/model/process receipts and all optional
dispositions. Claude's minor, medium-confidence garden-tree ambiguity signal
motivated the conservative guards. GPT accepted them without regression while
retaining its narrower judgment that a mandatory omission defect had not been
established. This is not manufactured initial agreement or unrestricted
synonymy. Initial oversized reads and GPT's failed administrative-path
verification remain disclosed; coordinator verification supplies the exact
snapshot, not a successful canonical-repository read by the reviewer.

All four files are now CLEAN across the three textual facets, with no
consequential in-scope unresolved claim. They subsequently passed the exact
parent Android recovery, current-main, CI and immutable public ZIP gates in
the [publication record](n1-sources/batch-007-publication.json).
The historical execution denial and qualified original review disagreement
remain preserved; neither is rewritten as fresh coordinator Android execution
or initial reviewer agreement. All four Android cases passed without skips
and every runtime archive hash was verified under unchanged guards.
Terminal publication at `ef4b03b` delivered **29/1,228 additions;
1,199 remain to deliver**. Batch 008's local drafts above do not increase
that count. Compatible Android `f9b59a2` or later is required;
physical-phone/general-release acceptance is explicitly outstanding.

## Batch 006: published and verified

The [frozen packet](n1-sources/batch-006-membership.json) is **栗・梨**,
chosen to bound source-only reading and lexical work rather than continue
alphabetically. Both have a useful native tree/food noun, while 栗's grade-9
classification and additional readings need separate treatment. The
[draft ledger](n1-sources/batch-006-progress.json) retains all six source
readings in order and selects only **くり・なし** as question keys.
Three 栗 readings remain explicitly source-only; 梨's リ has the verified
recognition example 梨園 without a new theatre article or question.

Two necessary new word articles, **栗・梨**, give two reciprocal pairs;
neither character activates a baseline-declared pair. No reused article
or metadata is changed. Four frozen packets contain **18 complete JMdict
families**. The [external evidence](n1-sources/batch-006-external-evidence.json)
distinguishes actual dictionary headings from unsuitable initial Weblio
extraction, tree/nut/fruit and colour senses, and 梨's nonexclusive species
scope. Sixteen direct new-word exclusions guard fitting generic tree,
plant, fruit/nut, timber and brown labels; these are not transitive cliques.

Independent `claude-opus-5.5` and `gpt-6.1-sol` initial reviews covered the same
normally signed `8602dc7` snapshot: all four teaching files, all 18 complete
families, seven actual kanji comparisons and fourteen word comparisons.
Both processes exited before the next launch. One initial Claude group of
four teaching reads overlapped, contradicting its original serial claim;
the original report is preserved unchanged. An original-session supplement
reread those four files serially and acknowledges the breach without claiming
retroactive compliance. GPT's internal calls were serial.

The [reconciliation](n1-reviews/batch-006-reconciliation.json) retains all
three complete reports, actual model/read/process receipts and three optional
dispositions. No actionable defect was established; all four files are CLEAN
across correctness, scoped coverage and textual comprehensibility. Teaching
is unchanged, not native-speaker or exhaustive quiz certification.
[Execution 023](n1-sources/execution-023.json) and the
[review-closed audit](n1-sources/batch-006-review-closed-audit.json) record the
bounded textual closure and local checks.

The preceding paragraphs describe its earlier textual checkpoint.
Batch 006 is now **published for bounded owner testing**.
[Execution 025](n1-sources/execution-025.json) and the
[publication record](n1-sources/batch-006-publication.json) preserve the exact
parent Android recovery, all four fresh named cases without skips, normal
signed acceptance `9d05d18`, green CI and every immutable public ZIP runtime
hash within unchanged budgets. Terminal receipts were published at
`7b9f503`; historical permission denial, original review overlap and incorrect
serial claim remain preserved, not rebranded as compliant.
Published additions are **27/1,228; 1,201 remain to deliver**.
These are batch 006's historical publication counts; subsequent accepted
batch 007 coverage is recorded above.
Compatible Android `f9b59a2` or later remains required;
physical-phone/general-release acceptance is explicitly outstanding.

## Batch 005: published and verified

The [next frozen packet](n1-sources/batch-005-membership.json) is
**松・桃・梅**. Six full metadata readings remain in source order, with
six approved useful question keys. Three necessary new support articles,
**桃・白桃・松竹梅**, and three component backlinks in existing
**松・梅・梅雨** form seven reciprocal pairs, including all three activated
baseline-declared pairs. Reused identities, primary readings, sourced N3
levels and all original metadata remain unchanged. 梅雨 still has primary
つゆ and explicitly teaches alternate ばいう; a link does not allocate
つゆ to 梅.

The [draft ledger](n1-sources/batch-005-progress.json) records every reading,
support and quiz disposition. Three packets retain **26 complete JMdict
families**; the [external evidence](n1-sources/batch-005-external-evidence.json)
separates exact dictionary headings, 桃's pink abbreviation, 白桃's separate
readings and an unnecessary cultivar-date disagreement. Fourteen direct
new-word exclusions protect fitting tree/plant/fruit/peach and pink labels;
they are not transitive synonym groups.

[Pinned stroke receipts](n1-sources/batch-005-stroke-audit.json) verify
8/10/10 strokes, original SVG blobs and exact reconversion. All three
glyphs are present in the unchanged bundled font cmaps. 氵 is absent but
already appears in baseline 海; this is not fresh native visual acceptance.
[Execution 018](n1-sources/execution-018.json) and the
[draft audit](n1-sources/batch-005-draft-audit.json) preserve the earlier local
draft checks. Independent `claude-opus-5.5` and `gpt-6.1-sol` initial reviews
now cover all nine teaching files, all 26 complete dictionary families and
actual comparison passages on the same signed `29b2b475` snapshot. Both
reviewer processes exited before the next launch. One initial Claude pair of
overlapping small reads is preserved as a process breach; an original-session
serial supplement confirms those two word guards without rewriting history.

The [reconciliation](n1-reviews/batch-005-reconciliation.json) retains all
three original reports, optional dispositions and source/read limitations.
No actionable defect was established and teaching remains unchanged.
All nine files are CLEAN across the three textual facets, with reused
松・梅・梅雨 limited to changed-link/new-support integration. This is not
native-speaker or exhaustive quiz certification.
[Execution 019](n1-sources/execution-019.json) and the
[review-closed audit](n1-sources/batch-005-review-closed-audit.json) record
textual closure and exact local checks, not publication by those checkpoints.

**These three cards are now published for bounded owner testing.**
[Execution 020](n1-sources/execution-020.json) preserves the historical
pre-execution Android permission denial. The
[parent recovery](n1-sources/batch-005-parent-android-recovery.json) records
the exact command's successful approval-capable run: exit 0, 41 tasks executed,
RealContentTest 3/3 and RareHanTest 1/1 with no skips, failures or errors.
[Execution 021](n1-sources/execution-021.json) inspected the complete build log
and all four named XML cases, verified source/artifact hashes and this sibling
content root, and preserved that provenance rather than claiming a coordinator
rerun or relaxing the gate. Runtime remained exactly the reviewed `29b2b475`.

The [publication record](n1-sources/batch-005-publication.json) pins normally
signed accepted `c02086e`, green CI `41532631695` and the actual immutable
GitHub ZIP: all **8,121 runtime hashes** verified within unchanged archive,
per-file and path budgets. Fresh combined-main checks passed 353 Python tests,
validator, vocabulary consistency, manifest freshness and exact source,
baseline, membership, reading and link audits. The historical denial and
original review limitations remain intact.
**Published additions are 25/1,228; 1,203 remain to deliver.**
Batch 006's later draft is recorded separately above. Compatible Android `f9b59a2` or later is required;
physical-phone/general-release acceptance remains explicitly outstanding.

## Batch 004: published and verified

The [frozen tree packet](n1-sources/batch-004-membership.json) is
**杉・桐・柳**. Its [draft ledger](n1-sources/batch-004-progress.json)
keeps all seven full metadata readings and selects four useful question keys.
Three necessary new support articles, **桐・柳・川柳**, and one component
backlink in existing **杉** form four reciprocal pairs, including one activated
baseline-declared pair. The reused 杉 article preserves its identity, primary
すぎ, sourced N2 level, title and original exclusion.

Two packets preserve **23 complete JMdict families**, including the distinct
川柳 poem/tree/tea families and reading/sense restrictions. The
[external evidence](n1-sources/batch-004-external-evidence.json) identifies exact
Japanese dictionary headings and unsuitable extractions rather than treating
successful URLs as verification. [Pinned stroke receipts](n1-sources/batch-004-stroke-audit.json)
verify 7/10/9 counts and exact reconversion. All three card glyphs and 卯 are
present in the unchanged bundled font cmaps; 彡 is absent but already appears
in baseline 形. This is not a fresh native visual check.

**These three cards are published for bounded owner testing.**
Independent `claude-opus-5.5` and `gpt-6.1-sol` initial reviews covered the same
signed `bfea505` teaching snapshot. Both read all seven teaching files and
both complete dictionary packets; an original-Claude-session supplement
completed its initially omitted required お茶 comparison. All three actual
processes and internal tool calls were serial. The complete original reports,
optional dispositions and unequal comparison/live-source limits remain in the
[reconciliation](n1-reviews/batch-004-reconciliation.json). No actionable
in-scope defect was established and teaching did not change. All seven files
are CLEAN across the three textual facets, with reused 杉 limited to its
changed-backlink integration; this is not exhaustive quiz or native-speaker
certification.

The [publication record](n1-sources/batch-004-publication.json) pins accepted
`05bb0e1`, green CI `41526080210` and the actual immutable GitHub ZIP:
all **8,112 runtime hashes** verified within unchanged archive/per-file/path
budgets. [Execution 017](n1-sources/execution-017.json) records fresh non-skipped
RealContentTest 3/3 and RareHanTest 1/1 against this isolated sibling tree,
353 Python tests, validator, vocabulary consistency, fresh manifest and exact
source/baseline/membership/reading/link audits on the combined current-main tree.
Reviewed teaching remains exactly `bfea505`; no integration correction was
needed. At that checkpoint, published additions were **22/1,228**, with
**1,206 still to deliver**.
No next batch or fresh native/phone acceptance is claimed. Compatible Android
`f9b59a2` or later remains required; physical-phone/general-release acceptance
is explicitly outstanding.

## Batch 003: published and verified

The next [frozen packet](n1-sources/batch-003-membership.json) is
**苗・畔・畝**: young plants, paddy boundaries and raised planting rows.
Fourteen full metadata readings remain in source order; seven selected
question keys have linked, dictionary-backed examples. Three unmatched
on readings of 畝 remain explicitly source-only and unselected.

Six necessary support articles, **苗・育苗・苗代・畔・湖畔・畝**, and a narrow
alternate-spelling link/allocation clarification in existing **名字** form
seven reciprocal pairs. The stable 名字 article already teaches 苗字:
it is reused without a duplicate article or any metadata, primary-reading,
easier N2-level or exclusion change.

The [batch ledger](n1-sources/batch-003-progress.json) retains all reading,
support and quiz dispositions. Two initial packets preserve **35 complete JMdict
families**, and a later two-family supplement supports reviewed label safeguards;
the [external evidence](n1-sources/batch-003-external-evidence.json)
separates exact dictionary headings from unsuccessful/misleading extractions.
The [stroke receipt](n1-sources/batch-003-stroke-audit.json) verifies the
original pinned SVG blobs, exact reconversion and 8/10/10 stroke counts.

**These three cards are published for bounded owner testing.**
Independent `claude-opus-5.5` and `gpt-6.1-sol` reviews cover the same signed
`6ce5676` teaching snapshot; both original sessions confirmed the exact
two-pair correction at signed `b99945c`. All four processes and their internal
tool calls were serial, with complete original reports and actual read/model
receipts retained in the [reconciliation](n1-reviews/batch-003-reconciliation.json).
The minor unqualified "plant" label collision is resolved on new 苗 only;
the optional-origin rice-plant guard is adopted without changing any reused
metadata. Other optional polish remains nonblocking, not manufactured defects.
All ten assigned files are CLEAN across the three textual facets; this is not
native-speaker or measured-learning certification.

The [publication record](n1-sources/batch-003-publication.json) pins accepted
`6526427` and [execution 014](n1-sources/execution-014.json) records fresh
non-skipped RealContentTest 3/3 and RareHanTest 1/1 against this isolated
content tree, 353 Python tests and combined-main acceptance. Terminal receipt
`c7b7bdc` has green CI `41521646661`; its exact immutable GitHub ZIP preserves
all 8,103 runtime hashes within the unchanged budgets. None of these three
characters is in the forty-character fallback set; no fresh native or phone
check is claimed. Published additions are **19/1,228**, with **1,209 still
to deliver**.

## Batch 002: published and verified

The next [frozen packet](n1-sources/batch-002-membership.json) is deliberately
small: **稲・穂・桑・芋**, an agriculture/plant comparison rather than an
alphabetical slice. Four new support articles, **稲穂・水稲・桑・芋**, and the
single component-link addition in existing **稲** form six reciprocal pairs.
The [draft ledger](n1-sources/batch-002-progress.json) retains all ten full
reading dispositions, six selected question keys, three wrong meaning choices
per card and four direct word-quiz exclusions. The reused 稲 article keeps its
primary いね and sourced N3 vocabulary level.

Three dictionary packets retain **19 complete applicable JMdict families**,
including spelling/reading restrictions and comparison senses.
[Pinned stroke verification](n1-sources/batch-002-stroke-audit.json) checks
each original SVG Git blob, exact reconversion and the 14/15/10/6 counts.
No stroke geometry was edited manually.

**These four cards are published for bounded owner testing.**
Original initial reviews by `claude-opus-5.5` and `gpt-6.1-sol` cover the same
frozen `9fee517` teaching; both original sessions confirmed the bounded
corrections at `0a5f2e2`. The [reconciliation](n1-reviews/batch-002-reconciliation.json)
preserves complete reports, actual read scopes, two minor findings, the adopted
optional safeguard and limitations. Reviewer processes were serial; Claude's
initial overlapping pair of small card reads was a disclosed process breach,
not rewritten as compliant execution. Both confirmations used serial reads.

The [publication record](n1-sources/batch-002-publication.json) pins accepted
`30faea0` and the [execution receipt](n1-sources/execution-011.json) records
fresh non-skipped RealContentTest 3/3 and RareHanTest 1/1 against this isolated
content tree, 353 Python tests and combined-main validation. The terminal
receipt commit `fd75a67` has green CI `41515516468`; its exact immutable GitHub
ZIP preserves all 8,091 runtime hashes within the unchanged budgets.
The published count is sixteen additions, with 1,212 still to deliver.
No new native or physical-phone acceptance is inferred from these checks.

For later bounded packets, run `python -B tools/audit_n1_batch.py --batch 002`
with that packet's ledger. It compares the whole runtime payload against the
exact batch base and permits only its listed additions and exact reused-passage
edits; it also checks source metadata, full reading dispositions, dictionary
pair restrictions, reciprocal links, curated projections and labels.
The earlier `audit_n1_pilot.py` intentionally remains pilot-bounded: its
runtime-addition check is not applicable to a tree containing later drafts.
Neither audit establishes linguistic correctness.

## Pilot

### Current pilot acceptance checkpoint

The same twelve-card pilot now has explicit, source-backed
[quiz subsets](n1-sources/pilot-curated-readings.json): **19 offered keys**,
with **zero source-only keys offered**, while all **47 full metadata entries**
and their order remain unchanged. The separately published
[curated-reading prerequisite](n1-reviews/curated-reading-prerequisite.json)
is delivered and CI-green; compatible Android `f9b59a2` is required because
older APKs ignore the optional fields.

Four necessary support articles, **幹・凹凸・矛・鷹揚**, bring the pilot to
**nine distinct new support articles, eight reused articles and 19 reciprocal
kanji/support pairs**. The reused 氏 article explicitly distinguishes the
うじ noun from its unchanged primary し suffix identity. No vocabulary level
is inferred from kanji membership.

Two serial independent curation/support-diff reviews used actual
`claude-opus-5.5` and `gpt-6.1-sol` at `b43173e`, preserving the original
teaching reviews below. Seven source-verified direct quiz exclusions and
two optional wording clarifications were confirmed in both original sessions
at corrected teaching snapshot `bb448a2`. The complete
[reports and reconciliation](n1-reviews/pilot-curation-reconciliation.json)
retain actual models, process exits, full returned-packet receipts and the
limited accidental exposure to unrelated N2 review snippets. All consequential
in-scope textual findings are resolved; this is not native-speaker certification.

**The pilot is published and verified for bounded owner testing** at
`bfd2526ed943c065ff25043b483782de50b7f60d`; the
[publication record](n1-sources/pilot-publication.json) pins green CI and
the exact public ZIP's 8,080 runtime hashes. Twelve additions are delivered,
**1,216 remain**; full N1 coverage is not claimed.
The [single-import native retry](n1-reviews/pilot-native-single-import-acceptance.md)
has terminal per-case status 0 for the combined N1 selection, meaning, curated
reading, drawing, article/system-Back and offline routes. Actual production
ContentSync accepted the full exact Git archive once, with 997 kanji / 4,951 words,
zero problems and the expected Room manifest metadata. Four route executions
retain two passes and two harness-readiness failures; the final pass includes
eleven exported artifacts and nine visually inspected screenshots. The offline
drawing check uses the production shape-only fallback, not handwriting-model
recognition or human drawing.

The previous all-40/four-family glyph inspection is inherited honestly.
Fresh RealContentTest 3/3 and RareHanTest 1/1 checks passed without skips against
this sibling content tree; all temporary Android inputs are cleaned.
Physical-phone/general-release acceptance remains explicitly outstanding;
approved issue #60 permits that distinction for bounded owner testing.
The [updated estimate](n1-sources/pilot-accepted-recalibration.json) records
the nine-support-word pilot and 47.100–49.312-MiB retained capacity sensitivities,
not forecasts. At the maximum later cap, the floor remains 83 batches / 166
initial assignments, plus the already necessary separate pilot curation pair
and further confirmations. The first publication's CI lacked the documented
fontTools dependency; its failure and the narrow green correction are preserved.
The next coordinator starts one bounded later batch after this delivery checkpoint.
During receipt publication, owner main `7f40d40` retired one unrelated
ぶらぶら illustration and its scene entry. The original source freeze is not
rewritten: the pilot ledger pins the exact two before/after manifest changes
and their source commit. The audit accepts only those recorded image/scene
differences, never overrides kanji or word metadata, and still rejects mismatched
hashes. The actual integrated tree passes 343 Python tests and fresh non-skipped
Android content/glyph checks. N1 teaching, full readings and stroke geometry
remain byte-identical to the accepted pilot; the native evidence is inherited
with that boundary, not claimed rerun against the unrelated scene retirement.

### Earlier pilot preparation and gate history

The following preserves the earlier five-support-word checkpoint and its
then-undelivered reading prerequisite as historical evidence, not current
blockers or current support counts.

The frozen [12-character pilot](n1-sources/pilot-membership.json) is
**幹・氏・扱・乃・凹・凸・矛・鷹・彗・漱・栞・莉**. Its assignments deliberately
mix existing-compound reuse, bound forms, primary-reading identity risks,
many/source-only readings, grade-9/name-use classification, the source's maximum
stroke count and four system-font-fallback characters. These are inspection
assignments, not findings about modern frequency or usable name readings.
Split the pilot further if its complete evidence becomes too large.

The [810 declared candidate pairs](n1-sources/baseline-word-candidates.json)
cover 757 baseline word articles and 490 missing characters. They are
**unverified candidates**, not established support mappings or required new
article counts. Inspect exact spellings, primary readings, full dictionary
families and restrictions before reuse; search kana-headed articles as well.
Activated links and reciprocal pairs must cover reused articles too.

The [font inventory](n1-sources/font-coverage.json) independently reproduces all
40 characters absent from all three bundled kanji-font cmaps at Android
`2bc0234bffcb3c4a0cbafde80367d24d2638a93a`. Its pending native dispositions
describe the immutable source freeze, not current progress. The separate
[native inspection](n1-reviews/pilot-native-acceptance.md) now records all
40 characters in all four production font-family choices on an API-35 emulator,
with seven visually inspected screenshots and 160 passing glyph/raster probes.
No missing or materially misleading glyph was established in that environment.
This is not phone acceptance or a passing navigation/drawing smoke test.

The [mutable pilot ledger](n1-sources/pilot-progress.json) now records all
**12 cards as drafted, none review-closed**. Twelve pinned stroke files were
generated without geometry edits; all counts match the frozen metadata.
Fourteen reciprocal pairs span eight reused and five new word articles,
including the kana-headed でこぼこ and うがい articles. Existing primary readings,
levels, titles and exclusions are preserved. In particular, 凹む remains
**へこむ**, and the separate くぼむ example is not linked as though it shared
that identity. New support articles are **乃至・鷹・彗星・栞・茉莉花**; no word
JLPT level is inferred from a character's N1 membership.

The [40-family lexical packet](n1-sources/pilot-jmdict.xml) preserves complete
selected JMdict entries, not only chosen glosses. Its
[selection](n1-sources/pilot-lexical-selection.json) and
[inspection record](n1-sources/pilot-external-evidence.json) document restrictions
and lookup limits. Eleven additional complete comparison families and five
broad-label families are preserved in
[comparison](n1-sources/pilot-comparisons-jmdict.xml) and
[label](n1-sources/pilot-label-jmdict.xml) packets. All **56 families** were
inspected by the author and supplied in full to both initial reviewers. The older suffix -うじ is
illustrated from an inspected Japanese dictionary and contrasted with modern
し. Kanjipedia's returned character-page headings independently establish the
written boundaries of 漱ぐ くちすすぐ and 漱ぐ すすぐ; blank word-page
extractions are explicitly not counted as inspected definitions. An attempted
radical-number inference from an image filename was removed after inspection of
the actual glyph. Historical analysis is not inferred from that image.

All **47 metadata readings** have draft dispositions and explicit table rows.
Fifteen remain qualified source-only entries, without manufactured compounds
or personal-name readings. Direct exclusions on new support articles protect
their overlapping alternative/book/bird/flower labels; baseline exclusions
remain untouched. Both initial reviewers found these text safeguards defensible;
the reading-prompt acceptance gate below remains unmet.

The ledger records the source-order offered-key projection for all twelve
characters against the actual Android reading adapter and queue implementation.
氏's うじ/-うじ entries collapse to one offered stem; uncommon/source-only
readings elsewhere are **not** filtered by article prose. Twelve source-only
keys remain within the **41 projected offered keys**, including 扱 ソウ/キュウ,
彗 エ/ケイ, 栞 カン and 莉 ライ/レイ. The ledger enumerates every one.
Both reviewers identify the same prompt-suitability gap: recognition metadata
does not itself justify asking learners these source-only readings. In 漱,
the first-three cap retains unestablished くちそそぐ while omitting supported
すすぐ. The [reconciliation](n1-reviews/pilot-reconciliation.json) therefore
requires the narrow [issue-#1 prerequisite](https://github.com/stop-cran/learning-japanese/issues/1):
preserve full dictionary metadata while transporting an explicitly approved
prompt subset through the importer, storage, adapter and actual queue.
An intentionally empty approved kind must not silently fall back to all readings.
No companion feature is implemented here, and current prompting is **not accepted**.
No metadata was silently dropped or reordered to alter the quiz.

The draft has five new support articles for twelve characters, not a forecast
of the entire expansion. With a 12-character pilot and later batches capped
at 15, the planning floor becomes **83 total batches / 166 initial reviewer
assignments**, before necessary splits or confirmations. The [recalibration](n1-sources/pilot-recalibration.json) now records actual
pilot bytes and conditional capacity sensitivities: 5, 512 or 1,228 total new
support words give approximately 47.014, 47.908 or 49.171 MiB retained at the
pilot's mean card/stroke/manifest sizes. These are not lexical forecasts or
upper bounds; future reuse corrections, larger cards and further support are
unknown. Smaller review packets increase the 83-batch/166-initial-review floor.
No defensible elapsed-time or credit promise follows from the observed process
times. Neither these measurements nor the font inspection authorize full rollout.

Two initial reviewers now cover every pilot card, all five new support articles
and changed passages in eight reused articles at the same frozen teaching
snapshot, `6855b42fa2c4e4cae6fd01a2697d10ee42011abb`.
The original [Claude Opus 5.5](n1-reviews/pilot-initial-claude.md) and
[GPT-6.1 Sol](n1-reviews/pilot-initial-gpt.md) reports assess correctness,
scoped coverage and **textual** phone comprehensibility. Actual requested models
`claude-opus-5.5` and `gpt-6.1-sol` are confirmed by execution events and usage,
not inferred from Auto. Processes did not overlap; observed tool calls were also
serial. Every supplied packet/range was returned in full after LF normalization.
This transport audit is not proof of comprehension or native-speaker review.

Neither initial review established a teaching-text correctness defect.
Claude's reverse-exclusion hypothesis was withdrawn in a bounded
[original-session confirmation](n1-reviews/pilot-confirmation-claude.md)
after inspecting supplied pinned app code and actual passing JVM tests:
one-sided exclusions already operate symmetrically. No redundant baseline
exclusions or optional teaching expansions were added. Both reports'
source-only reading concerns are one shared unresolved prerequisite, not
unique discoveries credited by differing severity or report section.

The [review/execution audit](n1-reviews/pilot-review-and-jvm-audit.json)
also retains actual XML results: **RealContentTest 3, WordsTest 22 and
RareHanTest 1**, all passing with **zero skips**. Both module-relative content
paths resolve to this dedicated content worktree. These are actual JVM
import/quiz/rare-code-point checks, not native glyph or phone acceptance.

The first attempt to capture the installed CLI's `--help` was permission-denied
before execution. That historical receipt is unchanged. The parent subsequently
supplied successful installed `copilot --help` and `copilot help config`
captures in the external control inputs. They document `--model`,
`--session-id`, `--available-tools` and named GPT/Claude models, resolving catalog
discovery; the independent reviews above subsequently executed successfully.
Claude's first review had one transient transport failure retried by the CLI;
it did not substitute another model. Original reports and observed read limits
remain preserved rather than rewritten as author consensus.

## Reproduction and next work

From this dedicated content worktree, with the approved downloads in the
external control input directory and the clean pinned sibling Android tree:

```powershell
python -X utf8 -B tools\freeze_n1_sources.py --inputs C:\Users\stop-\n1-kanji-workspace\control\inputs --android C:\Users\stop-\n1-kanji-workspace\kanji-cards-android --check
```

The authoring helper requires PyYAML and fontTools. It verifies all source
hashes, exact baseline counts, membership, reading workloads, candidate-pair
counts and font cmaps. Without `--check`, it only creates missing identical
freeze outputs and refuses to replace different evidence. It does not download,
rewrite cards, choose teaching readings or certify linguistic correctness.
Contributor evidence and tools remain excluded from downloadable runtime ZIPs.

The lexical packet is reproducible with the frozen dictionary:

```powershell
python -X utf8 -B tools\extract_n1_jmdict.py --input C:\Users\stop-\n1-kanji-workspace\control\inputs\n1-implementation-JMdict_e.gz --selection docs\n1-sources\pilot-lexical-selection.json --output docs\n1-sources\pilot-jmdict.xml --check
```

The extractor verifies the frozen compressed hash, preserves every selected
family in full with expanded entity descriptions, and refuses different existing
output. It is not a linguistic review. Repeat with
`pilot-comparison-selection.json` / `pilot-comparisons-jmdict.xml` and
`pilot-label-selection.json` / `pilot-label-jmdict.xml` for the additional packets.

The complete draft has a separate reproducible mechanical audit:

```powershell
python -X utf8 -B tools\audit_n1_pilot.py
```

It compares every baseline card/word metadata record and original stroke hash,
all unrelated baseline manifest entries, exact pilot additions, every source
metadata reading/table row, actual source-order key projections, all activated
baseline candidate pairs, all selected reciprocal pairs and manifest freshness.
It does not establish semantic correctness, execute Kotlin, inspect native
fonts or approve a source-only quiz key. The
[draft audit output](n1-sources/pilot-draft-audit.json) and
[execution receipt](n1-sources/execution-003.json) preserve this checkpoint.

**Blocked at the same independently reviewed but unaccepted pilot.**
The [native gate record](n1-reviews/pilot-native-acceptance.md) preserves two
API-35 emulator-host access violations, a corrected test-helper scroll failure,
and an API-29 alternative's reported 16-MiB runtime-heap OOM before activity
launch. None is a passing selection/session/article/Back or drawing receipt;
the emulator failures are not attributed to an unproven app/content defect.
All-40 font inspection and the conditional estimate are now durable.
Resume only when the narrow issue-#1 reading compatibility prerequisite and
a stable supported native acceptance environment are available; real-phone
acceptance remains separate and outstanding. Preserve the existing review
reports and teaching snapshot. Do not start later batches or push this
unaccepted draft branch.
