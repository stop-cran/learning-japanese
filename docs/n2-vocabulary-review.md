# N2 vocabulary expansion and review ledger

## Status

**Batches 01-11 review-closed; expansion in progress.** The target is all 1,812 source rows,
not 1,812 necessarily distinct new articles. The [source index](n2-vocabulary-sources.tsv)
preserves every row; empty teaching columns mean the mapping has not yet been established.
The first 200 rows are review-closed; twenty are draft and 1,592 remain pending.

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

## Final verification

Not started. Final closure requires all original rows accounted for, no consequential unresolved
claims, independent review coverage of every addition and changed passage, baseline preservation,
source/reading/sense and cross-reference audits, a deterministic manifest, and `stop-cran` authorship.
