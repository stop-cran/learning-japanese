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

## Batch 004: textual review closed, unpublished

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

**These are textually review-closed local cards, not delivered additions.**
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

Validator, fresh manifest, vocabulary consistency, exact source/baseline/batch
and review-execution audits, archive-budget checks and 353 Python tests pass.
Fresh non-skipped Android tests and combined-main/publication acceptance
remain required. Published additions stay **19/1,228**, with **1,209 still
to deliver**. No next batch or fresh native/phone acceptance is claimed.

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
