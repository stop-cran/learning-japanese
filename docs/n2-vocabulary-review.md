# N2 vocabulary expansion and review ledger

## Status

**Batches 01-15 review-closed.** The target is all 1,812 source rows,
not 1,812 necessarily distinct new articles. The [source index](n2-vocabulary-sources.tsv)
preserves every row; empty teaching columns mean the mapping has not yet been established.
The first 300 rows are review-closed; none are draft and 1,512 remain pending.

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

**Status:** independently reviewed and corrected; bounded confirmations pending.

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
certification is claimed. Bounded confirmations remain
pending, so the twenty source rows are still draft.

## Final verification

Not started. Final closure requires all original rows accounted for, no consequential unresolved
claims, independent review coverage of every addition and changed passage, baseline preservation,
source/reading/sense and cross-reference audits, a deterministic manifest, and `stop-cran` authorship.
