# Review process

How the kanji and word content is reviewed. The reviewers are Copilot custom agents stored in [.github/agents](.github/agents); the report format and evidence rules are in [.github/copilot-instructions.md](.github/copilot-instructions.md).

## Reviewers

| Agent | Looks at | Typical question |
| --- | --- | --- |
| [kanji-accuracy-reviewer](.github/agents/kanji-accuracy-reviewer.agent.md) | One batch of cards and their words | Are readings, stroke counts, radicals, word types, origins, look-alikes and examples true? |
| [kanji-comprehension-reviewer](.github/agents/kanji-comprehension-reviewer.agent.md) | One batch of cards and their words | Can an N5 learner on a phone follow it? Is jargon explained, are rare items marked, is the quiz title unambiguous? |
| [content-consistency-reviewer](.github/agents/content-consistency-reviewer.agent.md) | The whole repository | Do schema, links, titles, distractors, coverage, strokes and the manifest agree? |

Reviewers are read-only. They report; the maintainer decides what to apply.

## Running a review

1. Run `python tools/validate.py` (on Windows set `PYTHONIOENCODING=utf-8`).
2. Start one accuracy and one comprehension reviewer per batch of about 15 kanji, and one consistency reviewer for everything. Point each at its scope, for example "kanji cards for 右左高安新… plus the words whose `kanji:` contains any of them".
3. Collect findings; treat them as hypotheses and check disputed claims against a dictionary (kanjiapi.dev, Jisho/JMdict, Wiktionary, KanjiVG).
4. Apply fixes, run `validate.py`, then `python tools/build_manifest.py` and commit the manifest with the change.

For large additions, reviewers may handle several explicitly enumerated small batches within one bounded facet. Assign accuracy
and comprehension coverage to every batch, plus a whole-set consistency pass; use at least two model families for each batch.
Do not send the entire repository to every reviewer as an unspecified "check everything" task.

When comparing models, first freeze a shared sample and send the same files and rubric to each model independently. Preserve the
initial reports before sharing findings or applying fixes. Record actual model IDs and unavailable-model failures, without silently
substituting another model under the requested name. For each underlying issue, record severity, evidence, confidence, which reviewers
found it, and disposition (resolved, partial, unresolved, withdrawn, or optional). Count a unique contribution only after adjudication;
different assigned facets are a confound, not evidence that one model is better. Send changed passages and the diff back to the original
reviewers for reconciliation. The comparison describes this sample, not a general ranking of model quality.

The machine checks cover app format, not the truth of origins or naturalness of examples. Source records must identify actual dictionary
entries and preserve spelling/reading restrictions. See the [authoring checks](.github/instructions/content-structure.instructions.md#authoring-checks)
and [JLPT policy](docs/jlpt-levels.md). These additions address the observed YAML/parser gap, incomplete word metadata, and the requested
N4 cross-model review (2026-10-08); the older review records below remain historical rather than guarantees for new content.

## Review of the first starter set (106 kanji, 159 words)

Done once after the content was drafted: 6 accuracy, 3 comprehension and 1 consistency review.

What it found and what was fixed:

- Wrong or misleading facts: 年上 used for "elderly", 校正 read きょうせい, 話 analysed as containing 舌, 店's phonetic 占 given a テン reading, 銀行 explained with 商行為, 北海道 called "one of the few" 道 prefectures, 九 vs 力 stroke counts, 駅 called a bound noun.
- Reading-table errors: words in the wrong on/kun row, special readings listed as ordinary on readings (今年, 人間, 千葉).
- Comprehension: unexplained jargon (jukujikun, ateji, okurigana, "KANJIDIC"), unmarked rare readings, vague or untrue look-alike notes, duplicate prose.
- Consistency: stale manifest; `distractors` missing on one card.

Status and gaps recorded after that review (historical; see the N4 update below):

- The twelve kanji that words needed (側 海 達 供 旅 京 自 動 物 銀 短 事) now have cards; 118 kanji in total.
- Some word `kanji:` lists omit characters without cards (地, 曜, 心).
- Many words link to a kanji card that does not list the word under Common words (backlinks are not required for every prose link).
- Words that mix on and kun readings (半年, 駅前, 毎月) are typed `kango`; the schema has no on+kun type.
- Radicals were checked against the Kangxi table, not fetched per kanji from KANJIDIC2/Unihan. Word readings were checked from memory and spot lookups, not every entry in JMdict.
- Resolved afterwards: `jlpt` now follows the community lists mirrored by kanjiapi.dev, so cards for kanji such as 安, 新, 古, 多 and 会 are N4 (and 短 N2); all 118 cards in that original cohort carry the `starter` tag.

## Cross-model review (12 new cards plus 12 older ones)

The same accuracy and comprehension prompts were run on gpt-6.1-sol and grok-4.7, in three chunks of 8 cards plus their words, after the earlier Claude-based review and fixes. All three families found real errors the previous round had missed, including in already-reviewed articles (the 東京/京都 "same kanji reversed" claim, the 北 compass-order rule, 下さい filed under くだ.る, 来てください listed as an imperative, 九人 explained via 苦, 三和土 as an example of ゾウ).

- Both models found: 東京/京都, the 北 ordering rule, 犬 listing 犯 as an animal kanji, 食事 "ジ in compounds", the 中 うち example, 円高 reading and type, 銀行 "only" claims, the stale 長短 note.
- Only gpt-6.1-sol found: the 来る request row, 子供/幼児 wording, 水中 contrast, 高 description.
- Only grok-4.7 found: 下 ください, 発達, 九/苦, 三和土, 未/末, 北海道 etymology, 円 shape, 自 kun reading.

Conclusion: no single model is a reliable sole reviewer; each caught roughly half. Run at least two model families per batch and treat findings as hypotheses. Fixes were applied by file group and are not independently re-reviewed.

## N4 expansion (2026-10-08; reconciled)

The addition contains 134 kanji cards, 120 word articles and 134 generated stroke files. Together with the existing cards, this gives
252 kanji and 279 words, including all 166 characters in the named community N4 set. The [source snapshot](docs/n4-source-snapshot.json)
records dictionary versions, hashes, the exact target set and transformations; this is not an official JLPT syllabus.

All 134 new cards' readings, primary stroke counts, classical radical numbers and canonical radical glyphs were compared with the
inspected KANJIDIC2 records. All 120 new word articles' spelling/reading pairs were checked against restriction-aware JMdict lookups.
The new explanations use explicitly labelled modern-shape mnemonics rather than asserting unverified historical origins or phonetic roles.
Dictionary inclusion alone does not establish example naturalness. The independent linguistic reviews covered all new articles;
the original reviewers subsequently reconciled the corrected passages and quiz sets against the actual diffs.

The four incomplete word-kanji arrays for 土地, 安心, 土曜日 and 金曜日 are repaired, with links to their newly added cards.
分 is N5 under the documented source exception. App-format checks now distinguish restricted front matter from full YAML, enforce
complete written-kanji metadata and valid imported-page links, and cover distractors, headings and basic metadata consistency.
These structural checks are not a linguistic-correctness verdict.

### Independent coverage

All eleven initial reports are complete. The reviewers used the same immutable snapshot, based on `8279eaa` plus the uncommitted
expansion: app content version `8e028ca1b338df0b`, snapshot SHA-256
`a3e8eab2d3aa40042e62bcb51a27a338bfca89cda3be2e13f7ab84834b694134`.
Initial reports remain separate, fingerprinted artifacts rather than being overwritten during reconciliation.
Reported file lists match the assigned linguistic scopes.

| Scope | Accuracy | Comprehension and scoped coverage |
| --- | --- | --- |
| Shared: 18 kanji + 18 words | Each of `claude-opus-5.5`, `gpt-6-astra`, `grok-4.7` checked all facets independently | Same three reviewers and rubric |
| A: 39 kanji + 37 words | `claude-opus-5.5` | `gpt-6-astra` |
| B: 39 kanji + 34 words | `gpt-6-astra` | `grok-4.7` |
| C: 38 kanji + 32 words | `grok-4.7` | `claude-opus-5.5` |

The shared words include 17 new articles and the existing 土地 article. Every one of the 134 new kanji and 120 new word articles
therefore received coverage from at least two model families. A separate `gpt-6-astra` pass checked whole-set consistency;
`claude-opus-5.5` reviewed the validator, tests, CI and importer assumptions. These are the actual models used, not substituted aliases.

Reconciliation used a separate immutable snapshot: app content version `7327a218a0a9c842`, snapshot SHA-256
`e0fec24bf7e5b1604dc2cb96c1acdd6f851683a64676809cd8987590848fe19a`. The shared/A/B/C diffs contain 22/41/39/40 changed
files respectively: all 134 new kanji and eight word passages, including existing 土地. Each original linguistic reviewer checked
their assigned changes; reported changed-file lists match the exact diffs. The consistency reviewer confirmed implementation and
coverage, and the tooling reviewer closed the validator changes separately. No actionable in-scope defect remains open.
The final review-record update is outside the app manifest; imported content remains byte-identical to the reconciled snapshot.

### Adjudicated changes

- Correct the default nearby-shop construction to 近くの店, while preserving qualified direct modification such as 駅に近い店.
  Clarify the usual local-government 公立 versus national 国立 distinction.
- Remove misleading "godan despite ending in る" wording from 止まる and the parallel 作る passage. Distinguish the i-sound in
  知る from literally writing いる. Add useful standalone ほう comparison/advice coverage and the polite ご主人 contrast.
- Supply missing kana, explain visible radical forms without changing canonical metadata, clarify modern component comparisons,
  and remove unsupported frequency/register qualifications in 土地. Removing an unverified qualification is not proof that its
  opposite is true.
- Repair ambiguous quiz choices, including 地/土, 屋/店, 問/聞, 題/問 and 言/語. The actual app shows a kanji and offers English
  titles as answers. Its default four-choice quiz fills missing distractors automatically, so merely replacing one synonym while
  retaining two curated choices does not guarantee a safe complete question. Three explicit choices are now present on every
  new card, with every revised set reconciled by the assigned reviewers. The class-level pass also removed ambiguous 研/究 and 洋/海 choices and excluded
  試/験 and 館/堂 as mutual choices; related meanings remain available for comparison in the prose.
  The 25 older two-distractor cards were checked separately: their highest eligible shared-tag band contains only original cards,
  so no new card can win the remaining slot under the inspected inputs. Their lists are left unchanged; optional stabilization
  would not fix a demonstrated expansion regression.
- Repair validator/importer disagreement around Unicode whitespace, header boundaries and free-form articles; strengthen stroke
  identity/geometry checks and their fixtures, and report malformed input explicitly. No current source card was shown to trigger
  the Unicode mismatch; it was reproduced with targeted malformed headers.

These fixes were reconciled against the actual changes, not closed by accepting a majority vote. Adopted optional improvements
remain distinct from corrected defects; other nonblocking suggestions are not presented as completed work.

The tooling reconciliation is complete: the original reviewer confirmed the parser, stroke and error-reporting fixes. That pass
also caught a new platform-dependent test assumption: a 3,000-deep JSON array raised a recursion error on Windows but parsed on Linux,
so the test would fail in CI. The test now injects `RecursionError` deterministically while retaining real deep-YAML inputs.
All 46 tests pass on Windows Python 3.13.14/PyYAML 6.0.2 and Ubuntu Python 3.12.3/PyYAML 6.0.1; the original reviewer independently
confirmed the repair and that removing the error handler still fails the test. Optional dependency pinning remains deferred.

### Model contributions in this sample

The matched sample, rather than the disjoint A/B/C assignments, supports the comparison.

| Model | Additional useful observations in the shared sample |
| --- | --- |
| `claude-opus-5.5` | Standalone ほう coverage and the misleading 止まる verb-ending explanation were not raised by the other shared reviewers. |
| `gpt-6-astra` | Missing ひろい in 広い土地; also explicitly left the "ト occurs in few words" frequency qualification unverified rather than treating it as established. |
| `grok-4.7` | Actionable quiz concerns corroborated concerns raised elsewhere; its two other shared-sample findings were withdrawn as defects after evidence-based discussion. They remain optional presentation suggestions, not unique verified errors. |

Overlap was counted across all report sections. All three noticed 地/土, although Claude initially treated it as a hypothesis.
Claude and Grok raised 屋/店 as an actionable ambiguity; Astra noticed but dismissed it using a full-meaning-prompt interpretation.
Inspection of the actual kanji-to-English UI settled that disagreement. The ご主人 suggestion was shared by Claude and Grok;
the unsupported 地所 register qualification was raised by Claude and separately recorded as unverified by Astra.

Grok's 同じ finding cited the wrong JMdict entry: it supplied the entry for 雷雨. The reviewer corrected the reference to entry
1451750 and withdrew the grammatical-error claim; the original wording already allowed, rather than universally required, な
before の. Its demand for full-sentence 土地 examples was also withdrawn: the authoring rule requires translations, not only complete
sentences. The narrower explanatory-の wording and clearer example layout were adopted as optional improvements.

Outside the matched sample, useful findings included Claude's 近い usage correction, Astra's 問/聞 quiz concern, the 公立 distinction
raised independently by Claude and Astra, and Grok's 知る spelling-versus-sound clarification. Different facets and files prevent
turning those results into a fair numerical ranking. This is a small, task-specific comparison, not a general model benchmark.

### Limits and legacy observations

The reviews are not an exhaustive native-speaker/corpus study, historical reconstruction, pitch-accent audit or Android device test.
Structural checks covered the full 252-kanji/279-word corpus; that does not constitute a fresh linguistic audit of every older article.
The larger-quiz and future-app fallback limits are documented in the [quiz-authoring rule](docs/content-format.md#quiz-authoring).
Quiz judgments concern ordinary learner-facing meanings, not every rare or historical sense. For example, the accuracy-B reviewer
left 曜/明's wider "shine" association as an optional improvement rather than an ordinary-sense defect. Visual resemblance is
editorial judgment, not measured learner-confusion data; several third choices are moderate component/layout contrasts.

The consistency reviewer also reported two pre-existing issues outside this expansion's changes: 六 uses the Nelson indexing radical
亠/8 rather than the selected classical 八/12, and 16 older word articles omit useful component links. All 15 distinct missing-link
targets already existed at `8279eaa`; none became available through the 134-card addition. Those legacy items are left unchanged
rather than silently broadening the N4 task. The alternate radical is not claimed to be invalid in every indexing scheme.
The missing-link articles are 先生, 内側, 出入口, 北海道, 友達, 名前, 国内, 外国, 子供, 旅行, 来年, 自動車, 見物, 買い物, 銀行 and 飲み物.