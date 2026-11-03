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

## Batch 031: monkey textually review-closed, not published

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
Fresh Android and combined-main/publication gates remain pending.

Batch 030 is now [published and verified](n1-sources/batch-030-publication.json)
at terminal `b7dd333`: **57 additions delivered; 1,171 still to deliver**.
This local textual closure does not increase those counts. Compatible Android `f9b59a2` or
later is required; physical-phone/general-release acceptance remains
explicitly outstanding. Earlier sections retain their historical states.

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
