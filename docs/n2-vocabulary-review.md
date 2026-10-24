# N2 vocabulary expansion and review ledger

## Status

**Batches 01-32 review-closed.** The target is all 1,812 source rows,
not 1,812 necessarily distinct new articles. The [source index](n2-vocabulary-sources.tsv)
preserves every row; empty teaching columns mean the mapping has not yet been established.
The first 640 rows are review-closed; none are draft and 1,172 remain pending.

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
