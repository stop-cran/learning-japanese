# N2 expansion review ledger

Scope: the 365 missing cards in the [selected source set](n2-source-snapshot.json), plus directly related supporting content.
The existing 珍 and 短 cards are not claimed as newly reviewed. Follow the [review contract](../.github/copilot-instructions.md).

## Batch 01 - pilot

Cards: 並 丸 久 乱 乳 乾 了 介 仏 令 仲 伸 伺 低 依.

Status: **reviewed**. Both models confirmed the corrected passages with no actionable remaining defect in scope.

Evidence: [batch-01.json](n2-batch-sources/batch-01.json).
Related edits: third quiz distractors on 下 and 長; component links in 22 existing word articles.

Both initial reviewers inspected `a73354e75917d4758b386c870a4284cd70dfacee`, with no uncommitted content changes.
The author confirmed the clean worktree; the read-only reviewers could not independently run Git. Both reviewed all 15
new cards for correctness, scoped coverage and comprehensibility, using identical instructions and source access.
They ran sequentially in isolated processes, exited before the next started, and did not see one another's reports
or the author's adjudication. Actual models: **gpt-6.1-sol** and **claude-opus-5.5**.

Initial reports, preserved before corrections: [GPT](n2-reviews/batch-01-gpt-initial.md) and
[Claude](n2-reviews/batch-01-claude-initial.md). These describe the initial snapshot, not the corrected cards.

### Initial-finding reconciliation

These are the author's evidence-based dispositions, not a rewriting of either preserved report's initial verdict.
The changed-passage reviews below confirmed the actual corrections.

| Reports | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT F01 | 仲's 中 distractor can be correct in a secondary sense | Resolved: replace 中 with 住. Kanjipedia's 仲 entry includes the middle of a season; comparing the two quiz titles alone would miss this. |
| GPT F02; Claude F1 | 乾す and 乾る need spelling/reading qualifications | Resolved: retain the recognized variants, compare 干す/干る, and explain the outside-Joyo readings. Daijisen's exact entries and notation guide support these claims; no numerical frequency is inferred. |
| GPT F03; Claude O3 in part | 伺候 needs context | Resolved: attendance/service upon a high-ranking person, supported by the しこう entry in Seisenban Nihon Kokugo Daijiten. Missing JMdict priority is not evidence of obsolescence or rarity. |
| GPT F04; Claude F5 and O2 | 丸薬 and standalone 依怙 under "Common words" lack commonness evidence | Resolved conservatively: remove them from that list but keep their valid reading examples. This does not establish that either word is rare, or that 依怙 appears mainly in a particular compound. |
| Claude F2 | 仏語 needs homograph clarification | Optional clarification adopted: explicitly distinguish ふつご from ぶつご with both JMdict entries. The original note identified ふつご, so the stronger diagnosis that it denied the other reading is withdrawn. |
| Claude F3 | Include 乳房 ちぶさ | Optional coverage adopted, with the exact JMdict pair. The original にゅうぼう reading was valid; exhaustive alternate word readings are not the card's scope. |
| Claude F4, ロン part | 胡乱 うろん supplies a real example | Resolved: add the pair and retain JMdict's "usually written in kana" qualification. This also fixes the word-initial candidate-search blind spot. |
| Claude F4, tentative みだりに part | 乱りに might exemplify `みだ.る` or `みだ` | Optional, not adopted: the word is recognized, but the initial report did not establish allocation to either exact source reading. Retain the qualified dictionary-only rows rather than forcing a match. Claude's follow-up downgrades this to optional; GPT's optional proposal is narrower, `みだ` only. Neither establishes an actionable defect in the retained wording. |
| GPT optional; Claude O1 | 久遠 context and remote-past/future gloss | Optional context adopted: identify Buddhist terminology and cite Seisenban Nihon Kokugo Daijiten. Its くおん entry supports the existing expanded gloss; JMdict's shorter gloss did not disprove it. |
| GPT optional; Claude O4 | 依る qualification conflates spelling and pronunciation | Resolved: "rare kanji spelling", not "rare spelling/reading"; retain the usually-kana qualification. |
| Claude O3, 低まる part | Label 低まる uncommon | Optional, not adopted: the cited absence of priority flags does not support that inference. No frequency label added. |
| Claude O5 | Add フランス語 | Optional, not adopted: an everyday-equivalent expansion is not necessary to distinguish the two readings of 仏語. |
| Claude O6 | Replace 伸べる's futon example with 差し伸べる | Optional, not adopted: the report supplied no contrary attestation or evidence that the original construction was unnatural. No representativeness claim is inferred. |

### Dual-model usefulness

After comparing findings, optional suggestions, limits and per-card notes together, two verified issues were complementary:
GPT alone identified the 仲/中 quiz ambiguity; Claude alone identified the missing 胡乱 example. The latter was missed
both by the authoring heuristic and by GPT's positive source-only assessment. Shared useful observations include the
乾 qualifications, 丸薬/依怙 commonness gap, 伺候 context and 依る spelling distinction. Both also raised the 久遠 passage,
but Claude's gloss-evidence concern and GPT's Buddhist-context suggestion were not identical claims.

Claude also suggested useful optional homograph/alternate-reading explanations, but the valid original readings do not
become errors because another reading exists. Absence of dictionary priorities does not substantiate the report's
frequency claims. These results support using both families for this pilot; they neither rank models generally nor
demonstrate that model bias has been eliminated.

### Changed-passage confirmation

Both reviews used the corrected content at `455bfb27a10d61be997b75261e180cb089a8bbf7` and the actual 168-line
card diff from the initial checkpoint. Each covered all changed passages in 丸, 久, 乱, 乳, 乾, 仏, 仲, 伺 and 依,
with surrounding context and the replacement distractor's actual title. Each reported correctness, scoped coverage and
comprehensibility CLEAN for all nine, with no new actionable finding. The six unchanged pilot cards retain their initial
same-snapshot dual-model coverage; they were not needlessly re-reviewed.

Completed reports: [GPT](n2-reviews/batch-01-gpt-followup.md) and
[Claude](n2-reviews/batch-01-claude-followup.md). Claude resumed the original initial-review context. GPT's first
changed-passage process could not open the external-session diff because of a scoped path-permission failure; that
process was resumed with the artifact directory allowed and successfully inspected every hunk. Its completed report
replaces the incomplete pass for closure. All processes exited sequentially; none were retained running.

The follow-ups' remaining suggestions are **optional**, not required corrections: adding 乱りに for `みだ` only;
duplicating ちぶさ in Common words; rephrasing "established" as "assigned"; adding 仲秋 or 依怙贔屓; and choosing
different contextual wording for 伺候 or 久遠. They were not adopted. The selected 久遠 example's Buddhist context
does not assert that all uses are Buddhist; the 伺 card explicitly teaches humble usage. No unsupported "dated" label
was added. The stronger initial homograph/alternate-reading diagnoses remain calibrated as described above, even though
Claude labels their adopted clarifications resolved.

### Limits

Neither review certifies native-speaker naturalness across the corpus, exhaustively audits stroke geometry, or independently
re-extracts the pinned upstream dictionaries. Dictionary-only reading rows remain explicitly qualified, not ordinary-usage
recommendations. The 22 existing word-link edits and two legacy distractor changes received narrower related-context review,
not a fresh comprehensive review of their teaching text. Reconciliation is not a vote on the initial verdict labels.

The author confirmed clean, unchanged committed content before both review stages. File-only reviewers could read the
HEAD reference and supplied diff, not independently run Git. Source-record changes received current-record inspection,
not a separate upstream re-extraction. Their remaining optional 乱りに allocation is not used as teaching evidence.

## Batch 02

Cards: 個 倍 停 傾 像 億 兆 児 党 兵 冊 再 凍 刊 刷.

Status: **reviewed**. Both models confirmed the corrected passages with no actionable remaining defect in scope. Evidence:
[batch-02.json](n2-batch-sources/batch-02.json). New supporting word articles:
[兆候](../words/兆候.md), [児童](../words/児童.md), [兵士](../words/兵士.md),
[冊子](../words/冊子.md) and [刊行](../words/刊行.md).
These five articles do not claim vocabulary JLPT levels without a selected vocabulary source.

Related edits: component links in 13 existing word articles. The 15 new kanji cards have three curated wrong answers
each; no direct synonymous label was established between this batch and a remaining legacy two-distractor card.
The source record retains 47 exact Japanese reading rows and 65 inspected word pairs.
Unmatched character-dictionary readings remain explicitly qualified: 児 ゲイ, 党 なかま/むら,
冊 ふみ and 凍 こごる. They are not presented as ordinary word-use recommendations.

### Independent initial reviews

Both reviewers inspected the clean committed snapshot `3ec3eeab4373dc84ade3cd189534d1eae55f4033`,
with identical scope and evidence access: all 15 new kanji and all five new supporting word articles,
all three review facets, and the 13 existing component-link passages in their narrower related context.
Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. The isolated processes ran sequentially,
exited before the next started, made no changes, and did not see one another's reports or the author's rationale.
The author confirmed the snapshot and clean worktree; file-only reviewers could not independently run Git.

Preserved initial reports: [GPT](n2-reviews/batch-02-gpt-initial.md) and
[Claude](n2-reviews/batch-02-claude-initial.md). Their verdicts describe that initial snapshot.

### Initial-finding reconciliation

| Reports | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT G01; Claude O-02, symptom part | 兆候 competes with 症状 and サイン | Resolved: add both direct exclusions and explain their overlapping senses. JMdict 1597620 includes symptom; サイン's separate sign/indication sense is taught in its existing article and confirmed in the inspected JMdict API result. This is not its mathematical sine entry. |
| GPT G02; Claude F-03 | 児童 and 少年 overlap in juvenile | Resolved: add the direct exclusion and a contextual comparison. Both actual titles include juvenile; this does not erase the everyday boy sense of 少年 or impose a universal legal age. |
| Claude F-03, tentative 生徒 part | The school-pupil sense also overlaps with 生徒 | Optional safeguard adopted: add a direct exclusion and distinguish institutional school terminology from 生徒's broader learner sense. The existing 生徒 article explicitly teaches that broader sense; shared education tags alone would not justify the pair. |
| GPT G03; Claude F-04 | 冊子 and 図書 overlap in book | Resolved: add the direct exclusion and comparison. JMdict 1298530 includes book; the existing 図書 article allows one book as well as books. Exclusions through 本 are not transitive. |
| GPT G04; Claude F-02 | 兵士 omits the ordinary rank-and-file distinction | Resolved as a localized coverage/qualification issue: state ordinarily rank-and-file under officers, without specifying an exact rank or prohibiting every broader use. The inspected Seisenban へいし entry, sense 1, supports this; the separate historical ひょうじ entry is not the evidence. The initial examples remain valid. |
| Claude F-01 | 兵法 also has the reading へいほう | Optional clarification adopted with both exact pairs from JMdict 1506680. The original explicitly said ヒョウ "also occurs" and did not deny へいほう, so the stronger incorrect-reading diagnosis is withdrawn. Dictionary reading order alone is not frequency evidence. |
| Claude F-05 | 億万長者 lacks kana | Resolved: add おくまんちょうじゃ, already supported by the retained exact pair. |
| GPT optional | 刷る's inflections make the contrast with する usable | Optional clarification adopted: 刷ります すります and 刷って すって versus します and して. JMdict 1298670 identifies the printing verb as a godan verb ending in る, not general-purpose irregular する. |
| Claude O-01 | Consider excluding 軍隊 from 兵士 | Optional, not adopted: the inspected articles distinguish an individual soldier from organized armed forces. Sharing a military tag, or the broader meanings of the character 兵, does not establish interchangeable compound-word meanings. No contrary lexical evidence was supplied. |
| Claude O-02, 徴候 part | Add the alternate 徴候 spelling | Optional, not adopted: not necessary for this article's stated scope. The symptom overlap is addressed separately above. |
| Claude O-03 | 冊子 "names a publication" can suggest the publishing process | Optional polish adopted: say it names a book or booklet. The existing explicit object/process distinction was already correct; no exclusion from 出版 or 刊行 is established. |
| Claude O-04 | Add 短冊, 兵器, 兵隊 and 刷毛 | Optional, not adopted: the existing examples already cover the readings and useful linked vocabulary. 冊封 remains explicitly historical; its valid reading need not be replaced to make coverage exhaustive. |
| Claude wording polish | Mixed-language article, radical and location wording | Optional polish adopted for 像's "an 像", 党's radical and source-only-row wording, and 兵士's closing description. The remaining 冊, 停, 傾 and 兆候 preferences did not establish a consequential error and were not adopted. 停まる retains its adjacent rare-spelling qualification. |

### Dual-model usefulness

Deduplicating observations across the entire reports, shared useful findings include 少年, 図書 and the
兵士 rank-and-file distinction. 症状 is also shared: Claude raised it under Optional, not Findings.
GPT alone identified the consequential secondary-sense overlap with サイン; Claude alone identified
the missing 億万長者 kana. Claude's 生徒 suggestion also supplied a useful optional quiz safeguard.
These complementary results support using both families for this batch, not a general ranking or a claim
that model bias is eliminated. The optional 兵法 clarification must not be counted as proof that its
documented original pronunciation was wrong.

Both initial reviews leave stroke-path geometry and corpus-wide/native-speaker naturalness outside their guarantees.
The author's metadata check confirmed that this batch and the remaining legacy two-distractor cards share no tags,
as Claude reported; absence of shared tags does not itself prevent fallback selection.
The relevant semantic check found no established direct synonymous answer among those legacy cards.

### Changed-passage confirmation

Both original reviewer contexts were resumed sequentially against the clean committed correction snapshot
`8f857fe0b6df3afa2847f3733cf56e9d714d9140`. Each received its own preserved initial report and the actual
179-line, 14-hunk teaching-content diff from `3ec3eeab4373dc84ade3cd189534d1eae55f4033`.
Both read all nine changed pages with surrounding context: 像, 億, 党, 兵, 刷, 兆候, 児童, 兵士 and 冊子.
Both reported correctness, scoped coverage and comprehensibility CLEAN for all nine, with no actionable finding.
The eleven unchanged new pages retain their initial dual-model coverage; the legacy links were not needlessly re-reviewed.

Completed reports: [GPT](n2-reviews/batch-02-gpt-followup.md) and
[Claude](n2-reviews/batch-02-claude-followup.md). Both processes exited and made no changes.
The author verified Git state and diff provenance; file-only reviewers could not independently run Git.
GPT's report counts 15 hunks, but the generated diff contains 14; its nine-page coverage matches the actual changed files.

Remaining suggestions are optional: the unadopted initial expansions/polish, labelling the 兵士 evidence link more explicitly
on the 兵 card, and moving 兵士's scope caution to another section. They were not adopted because no actionable defect
was established. Claude confirmed that 学生's usual university-student meaning makes it distinguishable from 児童;
it did not recommend adding that exclusion. Both confirmed the adopted 生徒 safeguard and the サイン overlap.
Claude labels the 兵法 clarification resolved; the stronger initial diagnosis remains calibrated as optional above.

### Limits

No live-app quiz execution, native-speaker certification or exhaustive stroke-path audit is claimed.
The source packet's new 兵法 pair and 兵士 citation received current-record inspection, not an independent
re-extraction of the upstream dictionaries. Public dictionary corroboration may change after retrieval.
The source-only character readings remain qualified, not ordinary-use recommendations.
The 13 legacy word-link edits received related-context review, not fresh comprehensive teaching-text review.

## Batch 03

Cards: 券 刺 則 副 劇 効 勇 募 勢 包 匹 区 卒 協 占.

Status: **reviewed**. Both models confirmed the final corrected passages with no actionable remaining defect in scope.
Evidence: [batch-03.json](n2-batch-sources/batch-03.json), retaining 44 exact Japanese reading rows and
63 inspected word pairs. Supporting word articles:
[副作用](../words/副作用.md), [募集](../words/募集.md) and [匹敵](../words/匹敵.md).
No vocabulary JLPT levels are inferred. Related edits add component links in 20 existing word articles without
changing their lexical metadata or teaching text. All 15 new kanji have three curated wrong answers;
no direct synonymous label was established with the remaining legacy two-distractor cards.

The lookup-only rows are 効 `ききめ`/`なら.う`, 勢 `はずみ`, 区 `オウ`/`コウ`,
and 卒 `お.える`/`ついに`/`にわか`. Search-only 卒える is not a recommended word example.
Kanjipedia independently supports 卒わる for `お.わる`; the source record identifies that external evidence
separately from JMdict. Alternate-reading examples link only when they match the existing word article's reading.

### Independent initial reviews

Both reviewers inspected `408be09e0156fc6ed3c0ed1b1b0ac67f592eb1a9`, with identical scope and evidence access:
all 18 new pages for correctness, scoped coverage and comprehensibility, plus the 20 legacy link passages in their
narrower scope. Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. The isolated read-only processes ran sequentially,
exited before the next started and made no changes. Neither saw the other's report or the author's adjudication.
The author verified the clean committed snapshot; the reviewers could not independently execute Git.

Preserved initial reports: [GPT](n2-reviews/batch-03-gpt-initial.md) and
[Claude](n2-reviews/batch-03-claude-initial.md). These describe the initial snapshot, not the corrections.

### Initial-finding reconciliation

| Reports | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT R01; Claude O-4 | 匹敵's equality label overlaps with 同様 and 同一 | Resolved: add both direct exclusions and contextual comparisons. Their existing articles and inspected Jisho/JMdict records include equality; exclusion through 同じ is not transitive. GPT calls this required and Claude optional, but the underlying observation is shared. |
| GPT R02; Claude F-01 | 匹 warns about changed pronunciations without a usable count | Resolved: add 二匹 にひき in the reading row and 一匹 いっぴき / 二匹 にひき / 三匹 さんびき in Notes. The inspected Tofugu pronunciation table supports all three, identified separately from the isolated JMdict counter entry. |
| Claude O-1 | 刺し's learner-facing "sense 3" label is opaque | Optional polish adopted: remove the internal sense number from the row; retain the piercing gloss and adjacent explanation. The source packet still retains all exact senses. |
| Claude O-2 | 勢い has an adverb sense as well as noun senses | Optional qualification adopted: specify that the force/momentum sense is a noun, not an i-adjective. JMdict 1375040 explicitly distinguishes noun senses 1-3 from adverb sense 4. No exhaustive new word article is needed. |
| Claude O-3 | 卒去 also has the reading そっきょ | Optional, not adopted: the selected しゅっきょ pair validly demonstrates シュツ and does not deny another word reading. Exhaustive alternate readings of each example word are outside this card's scope. |
| Claude O-5 | Consider excluding 招く and 誘う from 募集 | Optional, not adopted: the report offers a conservative extension from English "invitation" but does not establish that the existing title/construction distinctions are defective. 募集 teaches seeking applications, not an unrestricted substitution for inviting someone. Existing 招待 and 集める safeguards remain. |
| Claude Limits, 則 | Standalone 則 のり's literary status is not established | No defect established: the page already identifies a dictionary reading and makes no literary or frequency claim. Do not add an unsupported register label. |
| Claude Limits, 副作用 | Non-medical figurative use lacks verified evidence in the inspected sources | Resolved conservatively: remove that additional claim from this medicine-focused supporting article. This is not evidence against figurative use and does not assert medical exclusivity. The initial CLEAN verdict did not certify the claim identified as unverified in Limits. |

Equality corroboration inspected on 2026-10-21:
[同様](https://jisho.org/api/v1/search/words?keyword=%E5%90%8C%E6%A7%98), sense 1, and
[同一](https://jisho.org/api/v1/search/words?keyword=%E5%90%8C%E4%B8%80), sense 1, both include "equal".
Their exact spellings/readings and unrestricted applicable senses were inspected, not inferred from a search summary.

### Dual-model usefulness

The two established corrections are **shared**, not unique contributions: Claude's Optional section contains the equality
observation that GPT puts in Findings, and both identify the missing usable counter forms. The different severity/facet
labels do not make distinct discoveries. Claude additionally supplied useful optional sense qualification and wording
polish, and uniquely surfaced the 副作用 evidence gap; the author removed that unsupported extra claim.
No verified GPT-only defect was established in this batch. This sample demonstrates cross-checking and some complementary
coverage, not a model ranking or proof that model bias has been eliminated.

### Changed-passage review and localized correction

Both original reviewer contexts resumed sequentially at the clean correction snapshot
`35e794f234701002bb2d09b54ce20ce2ad8506c0`. Each received its own initial report and the actual 83-line,
seven-hunk teaching-content diff from the initial checkpoint. Both inspected all five changed pages:
刺, 勢, 匹, 副作用 and 匹敵, with surrounding context and current evidence. Both confirmed the initial counter
and equality-exclusion issues resolved. GPT reported all three facets CLEAN for all five; Claude reported a new
minor comprehensibility issue on 匹敵 and CLEAN elsewhere. Both processes exited without changes.

Preserved first follow-ups: [GPT](n2-reviews/batch-03-gpt-followup.md) and
[Claude](n2-reviews/batch-03-claude-followup.md). Claude F-02 correctly identifies that contrasting matching with
identity does not distinguish 匹敵 from 同様, whose existing article expressly allows non-identical similarity.
The correction now contrasts kind/manner and `Bと同様` with reaching a comparison standard's level and
`Bに匹敵する`, and removes the unclear "equality labels" phrase. This is a localized contrastive-explanation issue,
not evidence that the equality senses or direct exclusions were wrong.
This second-stage issue was uniquely identified by Claude on the common corrected snapshot; do not conflate that
observation with the shared initial equality-exclusion finding.

Both original contexts then resumed sequentially at the clean final correction snapshot
`c887594020787d735d4dc3cbc8321bffba5ee7b8`. Each inspected the actual 13-line, one-hunk teaching diff and
the revised 匹敵 paragraph with the referenced 同様/同一 articles. Both reported all three facets CLEAN and
no actionable finding; Claude F-02 is resolved. Completed final reports: [GPT](n2-reviews/batch-03-gpt-final.md)
and [Claude](n2-reviews/batch-03-claude-final.md). Both processes exited and made no changes.
The thirteen unchanged new pages retain their initial dual-model coverage; the other four corrected pages retain
their first follow-up coverage. No unrelated comprehensive re-review is implied.

The remaining expansions are optional: 卒去 そっきょ, extra 募集 exclusions, 串刺し, additional 匹 counts,
and an adverb note on 勢い. They were not adopted; the qualified noun passage already avoids denying the adverb sense.
The author verified Git snapshot, diff provenance and unchanged teaching content across both confirmation stages.
File-only reviewers could not independently run Git. The first GPT follow-up's two Markdown hard-break spaces were
removed for the whitespace gate; no report claim was altered.

### Limits

The author mechanically verified that all 20 legacy word changes are component links only. Neither reviewer ran Git.
Claude refers to 45 distractor cards; those are 45 assignments over 42 distinct cards, not 45 distinct files.
Neither review exhaustively audits stroke geometry or certifies native-speaker/corpus-wide naturalness.
The external pronunciation and equality evidence received direct current-source inspection, not a new pinned dictionary
extraction. Initial source-only readings remain qualified as lookup information.

## Batch 04

Cards: 印 卵 厚 双 叫 召 史 各 含 周 咲 喫 営 団 囲.

Status: **reviewed**. Both models confirmed the final corrected passages without an actionable remaining defect.
Evidence: [batch-04.json](n2-batch-sources/batch-04.json), retaining 42 exact Japanese reading rows and
47 inspected word pairs. New supporting word article: [各地](../words/各地.md), without an inferred vocabulary
JLPT level. Related edits add component links in 22 existing word articles, preserving their lexical metadata
and teaching text. 毎 receives 海 as its third curated wrong answer so that new 各 cannot become a defensible
random fallback. The existing 海 card's sea/ocean answer was inspected.

Every new kanji has three curated wrong answers. The lookup-only rows are 厚 `あか`, 双 `たぐい`/`ふたつ`,
and 団 `かたまり`/`まる.い`. 双つ is retained only as search-index evidence. The rare spelling 双ぶ ならぶ
is qualified separately from pronunciation; 双子 ふたご provides the bound stem ふた.
The written き in 早咲き is preserved despite the character dictionary's suffix notation `-ざき`.
Dictionary evidence for 巧咲 demonstrates ショウ without establishing ordinary frequency.

各地's direct exclusions cover あちこち and 方々's separate place word ほうぼう, not its respectful people word
かたがた. These do not depend on the existing exclusion between the two older articles.
Fifteen new stroke files were generated by the pinned repository converter; no manual path edits were made.
Both blind reviewers received all 16 new pages for all three facets and the related edits in their narrower scope.

### Independent initial reviews

Both inspected the clean checkpoint `0a51f4fa06d97f4fd6af3889952f504f536eb696`, with the same scope, rubric
and evidence access. Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. Their isolated read-only processes ran
sequentially, exited before the next started, and made no changes. Neither received the other's report or the author's
adjudication. Initial reports: [GPT](n2-reviews/batch-04-gpt-initial.md) and
[Claude](n2-reviews/batch-04-claude-initial.md). GPT reported all 16 pages CLEAN on all facets; Claude reported one
minor correctness issue on 咲 and CLEAN elsewhere. These reports describe the draft, not the following clarifications.

### Initial-finding reconciliation

| Report | Observation | Disposition and evidence |
| --- | --- | --- |
| Claude B04-01 | 巧咲's alternative spelling 巧笑 is not explained | Adopted as a minor spelling-context clarification, not an invalid-reading finding. The complete pinned JMdict entry 2397140 contains both spellings, without spelling, reading or sense restrictions or frequency flags. The 咲 note names both and links 笑; the source record now retains `entrySpellings`. Dictionary order does not establish which spelling is usual. |
| Claude Optional, 厚 | English "kind" can mean a category as well as kindhearted | Optional polish adopted: use the unambiguous title "thick; cordial", consistent with the existing kindness/courtesy explanation. No quiz collision was established. |
| Claude Optional, 双 | A source-only paragraph follows a cited search-only index form | Optional clarification adopted: say no suitable **non-index** example was established. This preserves the search-only evidence and does not claim that no matching dictionary spelling exists. |
| Claude Optional, 団 | A whole-word ateji label need not mean every component is purely phonetic | Optional precision adopted: state the whole-spelling JMdict label for 布団 without a component-by-component phonetic claim. |
| Claude Optional, 各地 | 全国 partly overlaps English "all parts" | Optional, not adopted: both reports find the actual lexical meanings distinct; no new direct exclusion is required. |

The author inspected entry 2397140 in the same pinned `JMdict_e.gz`, not merely the live WWWJDIC result.
Its spellings are 巧笑 and 巧咲, reading こうしょう, one noun sense with "courteous laughter" and "forced laughter".
This validates the spelling clarification, not a relative-frequency claim or a new etymology.
The extraction's omission of a non-N2 alias is not a dictionary absence.

### Dual-model usefulness and limits

The spelling-context observation and three adopted optional clarifications are unique to Claude in this matched
sample; no equivalent appears elsewhere in GPT's report. GPT supplied a clean independent cross-check but no unique
established defect. The narrower useful distinction is between spelling context and an incorrect word: 巧咲 was an
attested dictionary example before correction. This is complementary review on this sample, not proof of reduced
model bias or a general model ranking.

Both inspected 45 distractor assignments over 40 distinct cards. The author separately verified all 22 legacy word
changes mechanically as links only, and authenticated the clean Git snapshot. File-only reviewers could not run Git.
Claude inspected stroke-file existence, source revision and counts; neither reviewer exhaustively audited geometry.
The source-only readings remain qualified; dictionary attestation is not native-speaker or corpus-wide certification.

### Changed-passage review and localized correction

Both original reviewer contexts resumed sequentially at the clean correction snapshot
`3ba67bec5c4de79238be4ef25c3b2929d541485c`, with their own original reports and the actual 60-line,
five-hunk teaching diff. Both read the four changed pages and the relevant evidence. Reports:
[GPT](n2-reviews/batch-04-gpt-followup.md) and [Claude](n2-reviews/batch-04-claude-followup.md).
Both confirmed the spelling clarification and initial optional points addressed; GPT found all four pages CLEAN.
Claude found new minor comprehensibility issue B04-02 on 団: removing the overbroad explanation had also removed the
only gloss for "ateji". This was a regression in the adopted suggestion, not evidence against the whole-word label.

The new note restores a qualified plain-language gloss and quotes "cloth association" to identify the literal
component translation being rejected. 咲's note now names こうしょう rather than using "this word" after a different
example. These are two localized Notes changes, not a reopened full-batch assignment.
Claude's second-stage term-gloss finding is a useful unique contribution on the common corrected snapshot.
The author accepted it against the changed paragraph and the repository's explain-technical-terms guidance.

Both processes exited without changes. Claude discloses that a repo-wide search incidentally returned one forbidden
ledger line about the 厚 title; it did not open the ledger or rely on that line. This affects the first follow-up's
strict access claim, not the blind initial comparison. Subsequent confirmation searches are restricted to the
specific teaching directories and evidence file.

Both original contexts then resumed sequentially at clean snapshot
`2ba6cbb6e7c5e0af47bd548ea864af8757ba559c`. Each inspected the actual 26-line, two-hunk diff,
the two revised Notes passages and relevant records. Both returned CLEAN on all three facets; Claude B04-02
and both remaining localized optional wording points are resolved. Preserved final reports:
[GPT](n2-reviews/batch-04-gpt-final.md) and [Claude](n2-reviews/batch-04-claude-final.md).
Neither final confirmation searched the forbidden ledgers/reports. Both processes exited and made no changes.
The other 12 new pages retain initial dual-model coverage; 厚 and 双 retain first-follow-up coverage.
The author authenticated the Git snapshots, actual diffs and absence of unrelated teaching changes.

## Batch 05

Cards: 固 圧 坂 均 型 埋 城 域 塔 塗 塩 境 央 奥 姓.

Status: **drafted; independent review pending**. Both models will receive the same frozen checkpoint, all
15 new kanji and the three new supporting word articles for correctness, scoped coverage and comprehensibility.
Evidence: [batch-05.json](n2-batch-sources/batch-05.json), with 47 exact Japanese reading rows and 52 inspected
word pairs, including the full-entry spelling evidence for 固い and the 名字/苗字 pair.

Supporting articles: [圧力](../words/圧力.md), [埋める](../words/埋める.md) (うめる), and [姓](../words/姓.md)
(せい), without inferred vocabulary JLPT levels. 埋める directly excludes 詰める and 記入; 姓 directly excludes
名 and 名前. These protect overlapping answer meanings, not transitive synonym groups or unrestricted
substitution rules.

Related edits add component links in 16 existing word articles without changing lexical metadata or teaching text.
中 receives 申 as its third curated wrong answer: its existing middle/inside title overlaps new 央 and 奥 answers
that could otherwise enter random fallback. The existing 申 card's humbly-say answer was inspected.

All 15 new kanji have three curated wrong answers. The source-only rows are 圧 `エン`, `お.す`, `おさ.える`,
`お.さえる`, and 奥 `くま`; 圧す おす and 圧さえる おさえる remain search-index evidence, not ordinary
spelling recommendations. 圧す へす and the document sense of 圧状 おうじょう retain their archaic labels.
埋's reading rows preserve distinct whole-word readings and sense restrictions; 姓's 百姓 example carries
the dictionary's sensitive-usage qualification. Canonical radicals include 大 for 央 and 奥 and 土 for 塗.
