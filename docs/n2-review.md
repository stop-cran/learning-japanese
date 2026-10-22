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

Status: **reviewed and reconciled**. Both models received the same
frozen checkpoint, all 15 new kanji and the three new supporting word articles for correctness, scoped coverage
and comprehensibility.
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

### Independent initial reviews

Both reviewed clean checkpoint `d9f323abaec692983e6ca2d31f419edb644974f5` with the same scope, rubric and source
access. Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. The isolated read-only processes ran sequentially,
exited before the next started and made no changes. Neither received the other report or the author's adjudication.
Preserved initial reports: [GPT](n2-reviews/batch-05-gpt-initial.md) and
[Claude](n2-reviews/batch-05-claude-initial.md).

GPT found one minor coverage issue on 城; Claude found no actionable defect and supplied eight optional points.
These are judgments about the initial snapshot, not the following corrections.

### Initial-finding reconciliation

| Report | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT F01 | 傾城's courtesan example lacks historical-register context | Resolved and confirmed by both reviewers. The author fetched the exact Kotobank page and inspected the Nipponica heading 傾城（花魁、娼妓） けいせい, not the page's separate けいせん heading or dance entry. It explicitly says the term largely fell out of use from the Meiji period onward. The row and note now qualify the courtesan term; セイ and the valid example are retained. The external source and exact short evidence are recorded in batch-05.json. |
| Claude B05-O-04 | The 姓 card cites the 名字/苗字 entry without mentioning either word | Optional source/text alignment adopted: the note briefly compares the family-name word's two spellings with 姓名. The two exact spelling/reading records were already inspected and retained before review, chiefly for the companion word article. No new frequency or register claim is inferred. |
| Claude B05-O-08 | The 記入 comparison gives only an abstract attachment pattern | Optional clarity adopted: a concrete blank-field example with kana and translation now contrasts the particles in 空欄に名前を記入する and 空欄を埋める. The general particle distinction is preserved, not replaced with a universal substitution rule. |
| Claude B05-O-01, O-02 | Add castle-name じょう and 心境 examples | Optional expansion not adopted. Existing companion articles already explain the uses; the current cards have verified examples for all their indicated readings. |
| Claude B05-O-03 | Add 塊 as another かたまり spelling | Optional expansion not adopted. The existing 固まり example is valid; the report does not establish that its omission is a defect. Priority flags do not independently establish relative frequency. |
| Claude B05-O-05, O-06 | Add name-order and 姓-versus-名字 register guidance | Optional expansion not adopted. The position warning already distinguishes the family-name category from ordering. The proposed register comparison lacks inspected evidence, as the report acknowledges. |
| Claude B05-O-07 | Add プレッシャー as a near-synonym | Optional expansion not adopted. The current physical/social pressure distinction is complete within scope; no existing near-synonymous article was established as a missing direct exclusion. |

### Dual-model usefulness and limits

After comparing all findings, optional points, limits and per-card observations, GPT alone established the
historical-register omission with an external encyclopedia entry. Claude supplied two uniquely useful optional
clarifications: direct source/text alignment on 姓 and a concrete particle contrast in 埋める. These are not
three equivalent defects, nor evidence of a general model ranking. The comparison shows complementary observations
on this matched sample; it does not prove that model bias has been eliminated.

Both reviewed all 45 distractor assignments and the 16 related link passages. The author mechanically verified
the legacy word changes as links only and 中's change as a single distractor-line update, and authenticated the
clean snapshot. Reviewers could not run Git. Claude checked stroke counts and the pinned revision; neither
reviewer exhaustively inspected geometry. Claude fetched no public dictionary pages, while GPT's consequential
register finding used an independently inspected public entry.

### Changed-passage confirmation

Both original contexts resumed sequentially at clean correction snapshot
`ae79da1aa5ea5b20c91d356f3490e1bababa46de`, receiving their own initial report and the actual 59-line,
four-hunk teaching diff. Both reviewed 城, 姓 and 埋める on all three facets, returned CLEAN and confirmed
the substantive correction and both adopted optional points. Both independently fetched the exact Nipponica entry.
Preserved reports: [GPT](n2-reviews/batch-05-gpt-followup.md) and
[Claude](n2-reviews/batch-05-claude-followup.md). Both processes exited without changes.

Both noted one optional translation precision: 明治以後 means from Meiji onward, not strictly after that
period ended. The teaching note and source claim now use the exact chronology. Claude also suggested making
名字/苗字's shared lexical identity explicit, naming the 空欄を埋める example instead of an ambiguous
"form-filling example," and using 記入する rather than describing the noun 記入 as a verb.
These narrow improvements are adopted and confirmed.

Both original contexts then resumed sequentially at clean snapshot
`91fc5e959ff73ca7ba6e75d0b7cc0874bd425fef`, receiving the actual 49-line, three-hunk precision diff.
Both reviewed the three revised pages on all three facets and returned CLEAN with no remaining optional point
within this bounded scope. Preserved final reports:
[GPT](n2-reviews/batch-05-gpt-final.md) and [Claude](n2-reviews/batch-05-claude-final.md).
Neither process changed files or remained running. The other 15 new pages retain initial dual-model coverage;
the three revised pages retain first-follow-up coverage outside the final changes. The author authenticated
the clean snapshots, actual diffs and unchanged other teaching content; file-only reviewers could not run Git.

## Batch 06

Cards: 委 季 孫 宇 宝 寺 封 専 将 尊 導 届 層 岩 岸.

Status: **closed after independent dual-model review**. The common review scope was all 15 new kanji,
all three facets, all 45 curated distractor assignments, and the 19 existing word-article link passages.
There are no new supporting word articles: every new kanji already has a relevant existing article.
Evidence: [batch-06.json](n2-batch-sources/batch-06.json), with 37 exact Japanese reading rows and
41 inspected dictionary spelling/reading pairs. Stroke files use the same pinned converter and 16-point format.

### Authored scope and checks

- All KANJIDIC2 readings are retained. 将's ソウ, まさ, ひきい.る and もって, and 届's カイ remain
  source-only lookup readings: no suitable word example was established in the inspected JMdict snapshot.
  The card does not infer that no such example can exist elsewhere.
- 将に まさに and 専ら もっぱら retain JMdict's usual-kana qualification. The separate 将 はた
  adverb is not conflated with the commander noun 将 しょう. The author inspected both precise Daijisen
  headings on the live Kotobank page; this evidence does not establish frequency or a register classification.
- 尊's two adjective readings and two verb readings have independent exact pairs. The card does not invent
  fixed meaning compartments for the pronunciation variants.
- 届's suffix row gives the verified compound 婚姻届 こんいんとどけ and explains the notification suffix.
  The 届く/届ける particle contrast has kana and English translations.
- 寺 uses 古寺 こじ for ジ rather than linking the separate counter entry to the てら article.
  一層 retains the distinction between the noun one layer and adverb even more.
- Every new kanji has three semantically wrong curated answers. The currently two-distractor legacy cards
  were considered for newly activated fallback overlap; no new direct synonymous choice was established.
- The related legacy word edits add component links only. Their spelling, reading, metadata and teaching prose
  are preserved; no legacy kanji teaching passage is changed in this batch.

### Independent review and reconciliation

Both reviewed clean checkpoint `da00a42474b6b3bf8cb6acacfc5d9d31c549aca4` against baseline
`63e437c54759373a7f32983908e425014e214444`, with identical scope, rubric and source access.
Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. The read-only processes ran sequentially,
exited before the next started and made no changes. Neither initial reviewer received the other report
or the author's adjudication. Preserved reports: [GPT](n2-reviews/batch-06-gpt-initial.md) and
[Claude](n2-reviews/batch-06-claude-initial.md).

Both returned CLEAN on every card and all three facets, with no actionable finding. GPT supplied no optional
point; Claude supplied ten. No teaching changes were needed, so no changed-passage confirmation was required.

| Report | Observation | Disposition and evidence |
| --- | --- | --- |
| Claude O-01, O-02, O-04, O-05, O-08 | Add committee, specialist, temple-name, social-layer and standalone-notification examples | Optional expansion not adopted. Current reading rows have verified examples, including 届's usable notification suffix; these proposals do not establish missing prerequisites. No new dictionary pairs are asserted from suggestions alone. |
| Claude O-03 | Rephrase the 将来 replacement warning; add a literary label and 将軍 | Optional polish/expansion not adopted. The note already separates the lexical items and qualifies extended readings as lookup material. The proposed literary label and はたまた comparison are not established by the inspected Daijisen sense; lack of a register label does not prove neutrality either. |
| Claude O-06 | Replace 岩塩 with a more common on-reading example | Optional expansion not adopted. 岩塩 is an exact valid pair; the report does not establish a comparative-frequency defect. |
| Claude O-07 | Simplify 季's character-by-character translation warning | Optional polish not adopted. Its separate Notes example already states the intended warning concretely. |
| Claude O-09 | Potential synonym collisions in automatic distractors | Optional future-risk observation, not a current defect. All new cards have three curated wrong answers. GPT independently checked all remaining two-choice legacy cards; no new direct fallback collision was established. The proposed 親/close association is not supported by 親's ordinary meanings and was not adopted. |
| Claude O-10 | Add more cross-links to existing component cards | Optional expansion not adopted. Each new card already has a useful word article and all 19 required existing component passages are linked. Extra association links are not required backlinks. |

### Dual-model usefulness and limits

Comparison included findings, optional points, limits and per-card observations. This matched sample yielded no
verified unique defect from either model; Claude supplied optional expansion and polish, not demonstrated corrections.
Both independently confirmed the consequential 将 lexical distinction. Dual-model review added independent scrutiny,
but this batch supplies no evidence of a unique corrective contribution or elimination of model bias.

Both read all 15 cards, 41 selected evidence records, 45 curated distractor assignments and 19 related passages.
GPT screened all 21 remaining two-choice legacy cards, while Claude's documented legacy check was narrower.
Claude additionally checked all 15 stroke-file counts; neither exhaustively reviewed drawing geometry.
Both disclosed that file tools could not verify Git provenance. The author authenticated the clean frozen commit
before and after the reviews and mechanically verified link-only preservation before checkpointing.
Claude's additional Jisho lookup is version-limited and cannot establish absence from the full pinned dictionary;
the source-only qualification rests on the author's inspected snapshot, not that negative lookup.

## Batch 07

Cards: 島 州 巨 巻 布 希 帯 帽 幅 干 幼 庁 床 底 府.

Status: **closed after independent dual-model review and changed-passage confirmations**. The common scope is all 15 new kanji,
the three new supporting articles 巻く, 干す and 庁, all three facets, all 45 curated distractor
assignments, and 17 existing word-article component-link passages. The only legacy kanji edit is
大's third wrong answer, 犬, to prevent 巨's size synonym from becoming a defensible default fallback.

Evidence: [batch-07.json](n2-batch-sources/batch-07.json), with 45 exact Japanese reading rows
and 54 inspected dictionary spelling/reading records after adding 布地 ぬのじ. All 15 stroke files use the pinned converter
and 16-point format.

### Authored scope and checks

- Every source reading is retained. 州's on ス remains source-only; the separate native sandbank
  noun す is not independent evidence of an on-reading word.
- 布's し.く is retained with its search-only JMdict spelling qualification. 布地 きれじ
  demonstrates the bound きれ reading; historical 布衣 ほい is not presented as ordinary modern clothing.
  The existing 布団 ateji explanation and all other legacy teaching prose remain unchanged.
- 帽's モウ, ずきん and おお.う and 庁's テイ and やくしょ remain source-only lookup information.
  Missing selected examples are not claims that no such word can exist.
- 希 まれ retains its usual-kana qualification. The exact Japanese dictionary entry for 希う
  supports an earnest-wish distinction; its old quotations are not used to infer current frequency or register.
- 巻's native noun spellings are distinguished from the verb and from the on-reading example 一巻.
  干's prefix and suffix each have a usable verified compound, with written し explained explicitly.
  床 とこ does not link to the separate ゆか article or imply fixed semantic compartments.
- All new kanji have three semantically wrong curated answers. The supporting articles add direct
  quiz exclusions for 巻く/包む and 庁/局, 庁/事務所 and 庁/オフィス, without assuming transitivity.
  Their vocabulary JLPT levels are not inferred from the characters.
- The author mechanically verified all 17 legacy word changes as links only, and 大's edit as one
  distractor-line change. No other legacy teaching passage is edited.

### Independent review and reconciliation

Both reviewed clean checkpoint `860f2cdc0f63e420ebc83e6e2a719cc66d1f58a6` against baseline
`52077285b9ca0f43adea4e1c9cd56e096b72ca6b`, with identical scope, rubric and source access.
Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. The read-only processes ran sequentially,
exited before the next started and made no changes. Neither initial reviewer received the other report
or the author's adjudication. Preserved reports: [GPT](n2-reviews/batch-07-gpt-initial.md) and
[Claude](n2-reviews/batch-07-claude-initial.md).

GPT returned CLEAN for every page and facet, with no optional point. Claude raised three minor findings
and five optional observations. The author inspected the full pinned JMdict entries for 布く and both
布地 readings, including the omitted non-N2 spelling aliases and the cross-reference between entries.

| Report | Observation | Disposition and evidence |
| --- | --- | --- |
| Claude B07-F1 | The automatic 布く gloss uses the futon sense instead of the spelling-specific senses | Resolved in the correction draft. The reading row now names promulgating, railway tracks and troop deployment; the note identifies senses 3, 5 and 6 and retains the search-only qualification. JMdict 1497020's explicit sense notes support the change. |
| Claude B07-F2 | 布地 きれじ could be mistaken for the spelling's only reading | Resolved in the correction draft by adding 布地 ぬのじ (1591910) and the alternate spelling 切れ地 (2859268). The report's proposed "usual"/"less common" ranking is not adopted: entry order, absent priorities and a rare label on the separate scraps sense do not establish comparative frequency. Both exact readings remain valid. |
| Claude B07-F3 | The displayed English "wind" label permits both 風 and 巻く | Resolved in the correction draft by a direct 巻く/風 exclusion. This is an English-label ambiguity, not a claim that the Japanese weather noun and winding verb are synonyms. |
| Claude O1 | 干す's bare "air" label could collide with air nouns | Optional disambiguation adopted: "hang out to dry; air out" retains the intended verb meaning without the bare noun-like answer label. |
| Claude O2 | 巻く and くるくる have partially overlapping coiling labels | Optional conservative quiz safeguard adopted as a direct exclusion; it does not equate the adverb with the verb or assert unrestricted substitution. |
| Claude O3 | Cite only sense 1 for 干す | Optional not adopted. The article also explicitly mentions draining, supported by sense 2, so the existing senses 1-2 citation covers the actual text. |
| Claude O4 | Use a named agency instead of standalone 庁 in the example | Optional naturalness polish not adopted. The source supports the noun use; the report does not establish the existing sentence as defective. |
| Claude O5 | Government and agency are distinguishable | No action needed, as the report itself states. |

### Dual-model usefulness and limits

Comparison included findings, optional points, limits and per-page observations. Claude uniquely established
the 布く sense mismatch, a useful alternate-reading clarification and the English wind-label collision;
GPT had no equivalent observation. These are sample-specific complementary contributions, not proof that one
model is universally better or that dual review eliminates bias. Claude's comparative-frequency inference was
not adopted, illustrating why findings still require evidence-based adjudication.

Both read all 18 new teaching pages, the original 53 selected dictionary records, all 45 distractor
assignments and all 17 related passages. Both considered overlapping legacy answers, including 大's repair.
Neither reviewed stroke geometry exhaustively or could independently authenticate Git provenance with file-only
tools. The author authenticated the clean frozen commit around the reviews. Public lookups are supplemental;
the correction's spelling and sense conclusions rest on the exact pinned dictionary, not search ordering.
Changed-passage confirmations are recorded below against the committed corrections and actual teaching diffs.

Both original reviewers were resumed sequentially at correction `cce24eef4c57704c3a40fbc490fa80dc694bec50`,
with their own initial report and the actual three-page teaching diff. Preserved confirmations:
[GPT](n2-reviews/batch-07-gpt-followup.md) and [Claude](n2-reviews/batch-07-claude-followup.md).
Both confirmed the 布 corrections and 干す title. Claude explicitly withdrew the comparative-frequency
wording and the suggestion to remove sense 2 from 干す's citation. GPT confirmed every changed facet CLEAN.
Claude established one additional direct quiz gap, B07-R1: ぐるぐる's winding label and quiz-eligible
string-winding picture also admit 巻く. Its exclusion through くるくる is not transitive. The final
correction adds the direct 巻く/ぐるぐる pair. Claude's new O6/O7 wording and table-placement proposals
remain optional and are not adopted; the existing notes already convey the alternate reading.

Both original reviewers then confirmed the final one-line exclusion change at
`ddd5f71dc59f48ebf43d560c4ce3b1c3fbf83827`, sequentially and read-only:
[GPT](n2-reviews/batch-07-gpt-final.md) and [Claude](n2-reviews/batch-07-claude-final.md).
Both returned CLEAN on all three facets, with no remaining actionable finding or optional point.
Claude's B07-R1 is resolved. Both inspected the scene declaration/description, not image bytes or runtime
selection frequency. The author regenerated the manifest and audited all 105 additions and 316 exact
source-reading rows; 260 source-set additions remain unauthored.

## Batch 08

Cards: 庫 延 弱 律 復 快 恋 患 悩 憎 戸 承 技 担 拝.

Status: **reviewed and reconciled**. Scope: all 15 new kanji,
the new supporting article 憎む, all three facets, all 45 curated distractor assignments, and
22 existing word-article component-link passages. No legacy kanji card is edited.

Evidence: [batch-08.json](n2-batch-sources/batch-08.json), with 50 exact Japanese reading rows
and 58 inspected dictionary spelling/reading records. All 15 stroke files use the pinned converter
and 16-point format.

### Authored scope and checks

- All source readings are retained. 拝's おろが.む remains source-only lookup information:
  the inspected 拝む record establishes おがむ, not the different source reading.
- 庫裏 くり demonstrates on ク without conflating it with native くら. 律 has separate examples
  for リツ, リチ and レツ. 承和 じょうわ is explicitly an era name, without extra calendar claims.
- 延びる/延ばす retain their intransitive/transitive distinction and spelling-specific postponement
  senses. 延べ uses its aggregate prefix sense with the usable count 延べ三日 のべみっか,
  not the entry's first futures-trading sense.
- 復 また retains rare-spelling and usual-kana qualifications. 悩み retains its actual written み
  despite the character source's undotted なやみ row. 悩ましい and the 憎 adjectives retain
  qualifications for meanings outside the selected table gloss.
- The full pinned JMdict spelling list for 承ける is preserved alongside its sense-specific notes;
  recognition of the spelling is not an unrestricted substitution rule for every sense of うける.
- 一戸 いっこ gives a usable house/household count. 戸's canonical radical remains 戶 with an
  explanation of the modern visible shape. Other positional radical variants are also identified.
- All new kanji have three semantically wrong curated answers. No newly activated direct synonym
  was established for the remaining two-choice legacy cards. 憎む has direct exclusions with
  嫌う and 嫌い; its vocabulary JLPT level is not inferred from 憎.
- The author mechanically verified all 22 existing word edits as component links only. The content
  validator reports zero errors; the audit covers all 120 additions and 366 exact source-reading rows.
  Structural success does not establish linguistic correctness; independent review and its limits are recorded below.

### Independent initial reviews

Both reviewed clean frozen checkpoint `92300150bee23b62f8c0558f97ddd224d0d48498` against baseline
`43e664c8994edc45de427bed0d1e4b3fd40b03d0`, with the same files, facets, rubric and source access.
Actual models: **gpt-6.1-sol** and **claude-opus-5.5**. The isolated read-only processes ran sequentially,
exited before the next started, and made no changes. Neither received the other's report or the author's
adjudication. Preserved reports: [GPT](n2-reviews/batch-08-gpt-initial.md) and
[Claude](n2-reviews/batch-08-claude-initial.md).

GPT found one minor register-coverage omission on 恋. Claude found two minor spelling-context omissions
on 庫 and 承 and supplied seven optional observations. These judgments describe the frozen draft, not
the corrected passages.

### Initial-finding reconciliation

The following adopted corrections are resolved and confirmed by both reviewers.

| Report | Observation | Disposition and evidence |
| --- | --- | --- |
| GPT B08-GPT-01; Claude O5 and Limits | 恋う's register is unexplained; special conjugations could be shown | Resolved. The author fetched the exact English Wiktionary Japanese こう verb entry, which explicitly labels its miss/love sense literary and gives 恋うて/恋うた. The row and note now state these facts and cite that secondary source. The pinned JMdict establishes the verb and special-class godan classification, not the literary label. Attempts to find a rendered publisher-dictionary register label did not establish one; a generated search claim about Kenkyusha was not accepted as an inspected entry. |
| Claude B08-01 | 庫 くら lacks spelling/reading-status context | Resolved as recognition guidance, not a frequency finding. The author downloaded and extracted the official 2010 Joyo table: PDF p. 50 lists コ and ク for 庫, not くら. The complete pinned JMdict entry 1592380 confirms 蔵/倉/庫, now preserved in the packet. The card qualifies 庫 くら without claiming that dictionary order or table absence proves which spelling is usual or rare. |
| Claude B08-02 | 承ける lacks spelling/reading-status context | Resolved as recognition guidance, not a comparative-frequency finding. Official-table PDF p. 79 lists ショウ and うけたまわる for 承, not ジョウ or うける. The note distinguishes a recognition example from a general replacement for 受ける. Full pinned entry 1329590 already preserves 受ける/請ける/承ける/享ける and its sense notes; the linguistic be-modified-by note is now identified without an invented example. |
| Claude O1 | "Specifically associates/assigns" overstates JMdict's "esp." | Optional precision adopted in 延 and 承: use especially and explicitly avoid an exclusive spelling rule. The pinned sense notes, not a live mirror's entry order, support the change. |
| Claude O2 | 悩's "undotted row" wording is source jargon | Optional clarity adopted: explain the actual spelling 悩み and final kana directly. |
| Claude O3 | 戸's "house counter" title can suggest a countertop | Optional clarity adopted: "door; counter for households." Meaning, readings and curated wrong choices remain unchanged; the title remains unique. |
| Claude O4 | Loosely overlapping kanji meanings can matter in larger quizzes | Optional future-app limitation, not a demonstrated defect in the current four-choice assignments. No unsupported kanji-exclusion field or unrelated legacy rewrite is added. |
| Claude O6 | Label おろがむ archaic if a suitable source is found | Optional expansion not adopted. The existing source-only qualification makes no current-neutral-use claim; no independently inspected archaic-register entry was established. |
| Claude O7 | Three existing articles write on readings in hiragana | Optional cosmetic legacy change not adopted. Their batch edits are component links only; lexical content remains preserved. |

The official PDF was retrieved on 2026-10-22 from the government URL retained in the source packet;
SHA256 `d9f28aeb4ce8250dbde07de20ac66cca71805ba09d94e4942c752dffa84d8d42`.
PDF page numbers above are one-based file pages. The table supports reading status, not comparative spelling
frequency, an exhaustive word inventory or a prohibition on outside-table readings. A generated web-search
answer incorrectly claimed all three disputed readings were in the table; it was rejected against the actual PDF.

### Dual-model usefulness and limits

The underlying 恋う register topic is shared: GPT established an explicit secondary-source label, while Claude
raised it optionally and left its evidence unresolved. It is not a uniquely noticed GPT defect merely because
the reports used different headings. Claude uniquely supplied the two adopted recognition-context observations
and three optional precision/clarity observations. The author independently established the table facts and rejected
unsupported frequency implications. This is complementary evidence on this matched sample, not a model ranking
or proof that model bias has been eliminated.

Both reviewed all 16 teaching pages, all 45 distractors and the 22 related component passages. The author
authenticated the clean Git snapshot and exact 58-file scope, mechanically verified link-only legacy edits,
and audited source readings and strokes. File-only reviewers could not authenticate Git or reproduce upstream
downloads; neither exhaustively inspected stroke geometry. External register evidence remains secondary,
not native-speaker certification or an exhaustive corpus result.

### Changed-passage confirmation

Both original reviewer contexts resumed sequentially at clean correction snapshot
`be11959de0714d98c0f7a7d95bdbc8e687d86fc6`, receiving their own initial report, the actual
146-line, seven-hunk teaching diff and the six corrected pages. Both returned CLEAN on correctness,
scoped coverage and comprehensibility, confirmed the adopted observations, and established no new defect
or regression. Preserved reports: [GPT](n2-reviews/batch-08-gpt-followup.md) and
[Claude](n2-reviews/batch-08-claude-followup.md). Both processes exited without changes before the next
started. The remaining nine kanji, supporting word and legacy passages retain initial dual-model coverage.

Both fetched the exact Wiktionary verb entry. Neither independently reproduced the binary government PDF
extraction: GPT read the author's bounded receipt; Claude also attempted the official fetch, which timed out,
and retained its earlier independent dictionary-table check. The author downloaded, hashed and extracted
the government PDF directly. Both reports disclose this evidence boundary instead of treating a supplied
hash as a reproduced one. The linguistic description of JMdict's be-modified-by sense follows its gloss;
the packet does not supply a separate Linguistics field tag.

Claude additionally checked teaching-directory title/distractor headers and relevant house-related cards
for the revised 戸 title. It offered four optional points, not defects: quotation marks around especially
and be modified by, an added 伸ばす contrast, a repeated table-status label in 承's ジョウ row, and a shorter
悩 note. No further teaching edit is needed: the current notes already state the relevant qualifications.
The proposed absolute "悩 alone is not read なやみ" is not adopted because the source retains that character
reading; the current note correctly concerns the noun's written spelling rather than denying the metadata.
No actionable defect or consequential unresolved claim remains in the corrected scope.

## Batch 09

Cards: 拾 挟 捜 捨 掃 掘 採 接 換 損 改 敬 旧 昇 星.

Status: **closed after independent review and changed-passage confirmation**. Scope: all 15 new kanji and four supporting
articles, 挟む, 捜す, 採掘 and 昇る; all three review facets and 45 curated distractor assignments.
Related edits: component links in 15 existing word articles and a third curated wrong answer on 上.

Evidence: [batch-09.json](n2-batch-sources/batch-09.json), with 50 exact reading rows and
52 selected restriction-aware dictionary spelling/reading records. The complete pinned spelling lists
for nine relevant entry families are retained, including 挟む/差し挟む, 探す/捜す, 上る/登る/昇る,
愛嬌/愛敬 and the かわる variants. 客星's complete pinned reading list is also retained.

### Authored scope and checks

- All KANJIDIC2 readings, primary strokes, radicals and grade tags are retained. Six readings remain
  explicitly qualified source-only lookup information: 挟's ショウ and わきばさ.む, 捜's シュ and
  シュウ, 掃's シュ, and 接's ショウ. Missing examples are not manufactured from an unrelated kana match.
- 拾 じゅう is identified as the legal-document numeral ten, separate from 拾う ひろう. 挟む さしはさむ
  is recognition spelling in the same entry as 差し挟む, not the reading of the linked はさむ article.
- 損's two okurigana boundaries have their actual written forms: 損なう and irregular 損う.
  Bound suffixes have complete examples 取り損なう and 見損ねる with kana and stem explanations.
- 換わる uses the exchange sense rather than an unqualified first-sense replacement gloss.
  The 探す/捜す and かえる/かわる notes preserve spelling tendencies rather than exclusive compartments.
- The 昇る comparison preserves the dictionary's actual spelling-restricted senses. 旧い retains
  its rare-spelling qualification; 旧 もと does not link as if the existing きゅう article taught it.
  星's -ぼし has 白星 しろぼし, not an unexplained standalone suffix.
- New supporting articles have no inferred vocabulary JLPT. Direct exclusions account for 挟む with
  握る and 持つ, 捜す with 探す and 求める, and 昇る with 上がる, 登る and 増加. The last group also
  considers the broad English answer label rise; exclusions are pairwise, not inherited transitively.
- All new kanji have three existing semantically wrong curated choices. 上 also gains a third to
  avoid newly activated upward-movement fallback. No unrelated legacy content is rewritten.
- Stroke data uses the pinned converter and 16 points per stroke. Structural validation reports
  zero errors; the metadata/reading/stroke audit covers 135 additions and 416 exact reading rows.
  These checks are not independent linguistic review or exhaustive stroke-path inspection.

### Independent initial review

Both models received the same frozen `d3166cb43733fa6c45908151ec3633044200d54f` snapshot,
19-page full-content scope, 15 link-only passages, 上's third choice, three facets and pinned evidence.
Reports are preserved unchanged apart from extracting the six-heading final report:

| Reviewer | Actual model | Preserved report | Initial result |
| --- | --- | --- | --- |
| GPT | `gpt-6.1-sol` | [initial report](n2-reviews/batch-09-gpt-initial.md) | 17 pages CLEAN; two word-quiz metadata issues |
| Claude | `claude-opus-5.5` | [initial report](n2-reviews/batch-09-claude-initial.md) | 18 pages CLEAN; two localized 星 qualifications/clarity findings |

The processes ran sequentially and exited before the next began; usage receipts confirm the actual models
and zero code edits. Each reviewed all assigned teaching pages, all 45 new distractor assignments and the
related passages. Claude explicitly did not open the separate source-snapshot file. Neither could verify
Git state, recompute source hashes or exhaustively inspect stroke paths; the author verified the frozen
clean checkpoint and exact 55-file draft, source metadata/reading/stroke audit and deterministic manifest.

### Reconciliation and authored corrections

| Finding | Adjudication and correction | Status |
| --- | --- | --- |
| GPT G09-001: missing 挟む exclusions | Pinned JMdict 1600740 explicitly includes gripping from both sides, catching a finger and sandwiching between. Existing 掴む, 捕まえる and サンドイッチ answer labels permit these overlaps. Add all three direct exclusions; sharing an exclusion through 握る is insufficient. The sandwich pair concerns English noun/verb ambiguity, not unrestricted Japanese synonymy. | Resolved |
| GPT G09-002: broad 昇る answer | The English rise can mean quantitative increase or getting to one's feet. Adopt the narrower proposed answer strategy: title and heading become rise (sun/moon); be promoted. Preserve the broader, source-supported natural-rising explanation. This avoids adding six unrelated increase/posture exclusions merely to preserve an overly broad answer label. | Resolved |
| Claude B9-01: 客星 qualification | Adopt the factual alternative-reading clarification, not an unsupported frequency ranking. Direct inspection of pinned JMdict 2563200 establishes かくせい, きゃくせい and きゃくしょう with no reading-rarity tags. Retain all three in the source packet; explain why the table uses きゃくしょう and explicitly disavow an only/usual-reading claim. Dictionary ordering and the reviewer's reported headword arrangement do not by themselves establish pronunciation frequency. | Resolved by qualified adoption |
| Claude B9-02: In other words | Replace the ambiguous English transition with In some vocabulary, such as 白星 しろぼし, so a different word's mark/victory sense is not presented as a paraphrase of visible planets. | Resolved |

The author inspected the complete pinned XML entries for 1600740, 1352570 and 2563200, and the actual
existing quiz labels. Source-packet omissions were not treated as dictionary absence. No categorical
claim that きゃくしょう is rare or that かくせい is most frequent is added; the reported Kotobank
headword arrangement was not independently reproduced by the author.

Claude's optional 採 phrasing, extra 愛敬/旧 ordering context and additional 挟む sense are nonblocking
expansion or polish and are not adopted. Its larger-kanji-quiz comparisons are a disclosed existing limit,
not defects in the current three curated choices. The promotion sentence's lack of independent corpus
attestation is preserved as a review limit, not converted into a claim that the ordinary construction is wrong.

### Model-usefulness observation

GPT uniquely identified the two actionable word-quiz gaps; Claude explicitly reported no further English
label clash. Claude uniquely identified the 客星 alternative-reading context and ambiguous English
transition; GPT had called that page CLEAN. These observations are compared across findings, optional
points and limits, not merely issue labels. The complementary catches are useful in this batch, but the
frequency implication still required source-based qualification. Neither family alone found every adopted
improvement, and this matched sample does not establish a general ranking or removal of model bias.

### Changed-passage confirmation and closure

Corrections are committed at `f5541b56583c3803328ed0c58c422c1344dcab89`. Each original reviewer resumed
sequentially with its own initial report, the same revised clean checkpoint and the actual complete
87-line/10-hunk teaching/evidence diff. Both read all three revised pages and the changed source evidence,
confirmed their original findings resolved, and found no regression in the other changed passages.

| Reviewer | Preserved report | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- | --- |
| GPT | [changed-passage confirmation](n2-reviews/batch-09-gpt-followup.md) | CLEAN | CLEAN | CLEAN |
| Claude | [changed-passage confirmation](n2-reviews/batch-09-claude-followup.md) | CLEAN | CLEAN | CLEAN |

The author verified zero validation errors, all 135 additions/416 exact reading rows, the three 客星
readings, direct exclusion targets, exact ten-file correction scope and a byte-identical repeated manifest
(`25d203f4b62d543e`). Reviewer limitations remain explicit: the supplied diff was not independently
regenerated, the pinned XML was not re-parsed by the reviewers, and app execution and drawing-path
inspection were not performed. Neither report claims native-speaker certification.

Claude's optional suggestion to add a moon example is not required to interpret the short answer label;
the body already says natural rising, such as the sun, rather than restricting the subject to that example.
No actionable defect or consequential unresolved claim remains in the corrected scope.

## Batch 10

Cards: 普 暴 曇 替 札 机 材 村 板 林 枚 枝 枯 柔 柱.

Status: **closed; both original reviewers confirmed the revised passages**. Scope: all 15 new kanji and four supporting articles,
暴れる, 枚, 枯れる and 柱; all three review facets and 45 curated distractor assignments.
Related edits: component links in 17 existing word articles and a third curated wrong answer on 木.

Evidence: [batch-10.json](n2-batch-sources/batch-10.json), with 40 exact reading rows and
51 selected restriction-aware dictionary spelling/reading records. Thirteen sensitive entry families retain
their complete spelling and reading lists, spelling flags and reading details, including kana-only
restrictions. These selected records are not the entire dictionary.

### Authored scope and checks

- All KANJIDIC2 readings, primary strokes, canonical radicals and grade tags are retained.
  普's あまねし remains source-only lookup information; 普く あまねく is marked usually written in kana.
  普段's ateji qualification is preserved rather than replaced with a literal character derivation.
- 替 retains 曰, no. 73, as its indexing radical, with the 日 resemblance explained.
  Its bound かえ- has the complete example 替え歌. The かえる/かわる families retain spelling
  tendencies and transitivity distinctions rather than exclusive compartments.
- 札 ふだ remains separate from the linked さつ article. 板木 はんぎ has its 版木 alternative,
  without a dictionary-order frequency claim. 村長 and 森林 supply concrete compound examples
  rather than forcing every on reading into an independent native noun.
- 枚 has usable 一枚, 二枚 and 三枚 counts and complete sentence examples. Its バイ is supported
  by explicitly archaic 枚を含む, not presented as a counter alternation or everyday expression.
- 柔 distinguishes the na-adjective 柔らか, i-adjective 柔らかい, usually-kana adjective やわ
  and separate martial-arts noun 柔ら やわら. The last is recognition context, not a usual-name claim.
- New supporting articles have no inferred vocabulary JLPT. Direct word-quiz exclusions account
  for 暴れる's physical-struggle/commotion overlaps, 枯れる with 死ぬ and 乾く, and 柱 with the broad
  English support labels of 支える, 援助 and 賛成. These are contextual overlaps and English-label
  safeguards, not assertions that all the Japanese words are unrestricted synonyms.
- Every new kanji has three existing semantically wrong curated choices. 木 gains 米 alongside
  人 and 水 to avoid newly activated timber/wood fallback from 材; its teaching text is unchanged.
  The 17 existing word edits preserve lexical metadata and teaching prose while adding component links.
- Stroke data uses the pinned converter and 16 points per stroke. Author inspection covers all
  19 generated teaching pages. Structural validation reports 0 errors; the accumulated audit covers
  150 additions and 456 exact source-reading rows, with 215 selected characters still unauthored.
  The 57-file draft preserves the 17 legacy word articles after stripping only their new component
  links, and 木 changes only its curated distractors. Two manifest builds are byte-identical.
  These checks do not substitute for independent review.

### Independent initial reviews and reconciliation

Both reviewers independently read the same clean draft, `013263037da18cd9f5f25e199685493011f94df5`,
with the same 19-page scope, related passages, rubric and 48-record initial evidence packet.
Each ran alone in a fresh short-lived process and exited before the next started. Both report no assigned
teaching-page omission; neither independently executed Git, the validator or the manifest builder.

- GPT, actual `gpt-6.1-sol`, session `ce8a660c-011a-4701-a4e9-52e86b9f7099`:
  [initial report](n2-reviews/batch-10-gpt-initial.md). All 19 pages CLEAN on all three facets;
  no findings or optional suggestions.
- Claude, actual `claude-opus-5.5`, session `6de31bb4-146c-4e13-9e52-548a2bbe2ae2`:
  [initial report](n2-reviews/batch-10-claude-initial.md). One minor 板 homograph finding;
  otherwise CLEAN. Its arithmetic description that all 40 reading rows have JMdict pairs should
  be read with the stated exception: 39 lexical examples and 普's one source-only あまねし.

`B10-板-01` is **resolved and confirmed by both reviewers**, with calibration:
the printing-woodblock example 板木 はんぎ was valid and sense-qualified, not an incorrect reading.
The competing separate word 板木 ばんぎ is confirmed in pinned JMdict entry 2868686, not just a live
search result. The revised notes explicitly distinguish the signal board and avoid a one-spelling/one-reading
shortcut. This is a localized coverage/comprehensibility improvement rather than invalidation of the ハン row.

Claude's optional suggestions were assessed separately:

- **Adopted optional context:** 枝葉 えだは and the dictionary's "esp. しよう" qualifier for the
  figurative sense, without exclusive reading compartments. Pinned entry 1579520 confirms both readings;
  its complete spelling/reading family and the additional pair are retained.
- **Adopted direct quiz safeguard:** 柱 gains 棒, whose stick/rod/pole answer can overlap with a
  structural post. The new comparison distinguishes shape from load-bearing role and cites entry 1519750.
  This is one direct exclusion, not a transitive propagation to related words.
- **Not adopted:** 激しい is an adjective, not the verb "act violently"; 台 is a supporting base,
  骨 a supporting frame, and 基 a basis/foundation. Their related properties do not alone establish a
  valid alternative to the displayed "pillar; mainstay" or "act violently; thrash about" answers.
  No new direct ambiguity was established for those proposals.
- **Optional, not required:** 人材, 千円札, 電柱 and additional 替 links. The existing examples and linked
  supporting articles already satisfy the stated scope; no missing prerequisite was established.

The revised packet has 51 selected pairs rather than 48 and 13 complete families rather than 12;
the reading inventory and all 45 curated kanji choices are unchanged. Four teaching files change:
板 and 枝 notes, 柱's metadata-source footer, and the supporting 柱 article.

### Changed-passage confirmation and closure

Corrections are committed at `a61167fec3c034abee9580d7edac20e2c077fe17`. Each original reviewer resumed
sequentially with its own preserved initial report, the same clean revised checkpoint and the actual complete
358-line/11-hunk teaching/evidence diff. Both read all four revised pages and the changed source evidence,
accepted the sense-qualified 板木 and 枝葉 explanations, and confirmed the direct 柱/棒 safeguard without regressions.

| Reviewer | Preserved report | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- | --- |
| GPT | [changed-passage confirmation](n2-reviews/batch-10-gpt-followup.md) | CLEAN | CLEAN | CLEAN |
| Claude | [changed-passage confirmation](n2-reviews/batch-10-claude-followup.md) | CLEAN | CLEAN | CLEAN |

The author verified zero validation errors, all 150 additions/456 exact reading rows, 51 selected pairs,
13 complete dictionary families, exact eleven-file correction scope, and a byte-identical repeated manifest
(version `b6468ed6e9b1bae2`). The original 48 selected pairs and all character metadata are preserved;
only the intended 枝葉 family details are added to an existing record.

**Observed model usefulness:** Claude uniquely raised the useful 板木 homograph context, optional 枝葉 reading
context, and pole/post quiz overlap adopted here. GPT raised no initial defect but independently confirmed
the complete revised scope and the calibrated sense distinctions. This is useful complementary review
on this sample, not evidence of general model superiority or elimination of model bias.

Claude's final optional source-footer observation is nonblocking: the 棒 entry supports the linked 柱
word article and is deliberately retained in the per-card evidence. Its remaining optional 台/骨/基 proposals
establish no new direct ambiguity. No further teaching expansion is required.

Limits remain explicit. Neither reviewer regenerated Git diffs, hashes, the original dictionary extraction,
or the app runtime. Claude could not confirm entry ID 2868686 on the public services it tried; the author
confirmed that ID, headword, reading and sense directly in the pinned XML. A Kotobank alternative calling
the signal board はんぎ does not contradict the nonexclusive card wording or the pinned ばんぎ example.
Neither report claims native-speaker certification. No actionable defect or consequential unresolved claim
remains in the revised scope.

## Batch 11

Cards: 査 栄 根 械 棒 森 植 極 橋 欧 武 歴 殿 毒 比.

Status: **closed after independent reviews and changed-passage confirmations**. Scope: all 15 new kanji and four supporting articles,
栄える, 極める, 欧州 and 御殿; all three review facets and 45 curated distractor assignments.
Related edits: component links in 21 existing word articles, with lexical metadata and teaching text preserved.

Evidence: [batch-11.json](n2-batch-sources/batch-11.json), with 46 exact reading rows:
40 JMdict-backed lexical examples, one externally verified written-boundary example, and five explicitly
qualified source-only readings. The packet retains 52 selected restriction-aware spelling/reading records;
14 sensitive families also retain complete spelling/reading lists, spelling flags and reading restrictions.
These selected records are not the entire dictionary.

### Authored scope and checks

- All KANJIDIC2 readings, primary strokes, canonical radicals and grade tags are retained.
  極 uses the primary 12-stroke count; 毒 keeps 毋, no. 80, with its 母-like visible lower portion explained.
  Origins remain labelled modern-shape mnemonics rather than unverified historical or phonetic claims.
- 栄's ヨウ and え, 欧's うたう and はく, and 武's bare たけ remain qualified source-only readings.
  栄養 does not allocate its よう to 栄. The investigated 栄耀 えよう has an outdated-kana flag;
  見栄 みえ is marked ateji. Neither is treated as independent proof of the unresolved native allocation.
  The revised え qualification explicitly names 見栄 and does not discourage that spelling's everyday use.
- 出来栄え, 屋根 and 月極め provide complete bound-reading examples. 殿 distinguishes the building
  compound 仮殿 from the formal address suffix -どの, with an attached-title example and no universal
  claim of greater respect than 様.
- 極 keeps the ごく adverb separate from きょく and the きわめる/きめる entries separate.
  Kanjipedia explicitly verifies 極まる きまる; JMdict's corresponding family instead spells 極る.
  The external notation guide establishes an outside-Joyo reading, not rarity.
  月極's irregular げっきょく is not presented as an unqualified alternative to つきぎめ.
- 械's rare-spelling flag is not a rare-pronunciation claim. 武し is explicitly archaic, and 歴とした
  is identified as usually written in kana. Reading-sensitive links do not redirect はえる to さかえる
  or きめる to the new きわめる article.
- Supporting vocabulary has no inferred JLPT labels. Direct quiz safeguards cover 栄える with 盛ん/豊か
  and 極める with 達する/至る; sentence patterns remain distinct despite contextual English overlap.
  Revised safeguards additionally cover the written homographs: 栄える with 輝く/光る, and 極める with 決める/選ぶ.
  欧州 and ヨーロッパ share the exact answer Europe, so the existing identical-title deduplication applies.
  No newly activated direct synonym was established among the remaining two-distractor legacy kanji.
- All 19 new teaching pages were inspected by the author. Structural validation reports 0 errors;
  the accumulated source/stroke audit covers 165 additions and 502 exact reading rows, with 200 selected
  characters still unauthored. The 21 existing word articles match their preceding versions after removing
  only the new component links and normalizing CRLF. These checks do not substitute for independent review.

### Independent initial reviews and reconciliation

Both reviewers independently assessed the clean draft `586989dc37529aaa66ff39ba9d84d0560f2a244d`,
with the same 19-page scope, 21 linked passages, rubric and source access. Each ran alone and exited before
the next started. Neither independently executed Git or the repository validation commands.

- GPT, actual `gpt-6.1-sol`, session `2ee345bc-1863-4c82-91a6-d46885b43ef6`:
  [initial report](n2-reviews/batch-11-gpt-initial.md). All 19 pages CLEAN on all three facets;
  no findings or optional suggestions.
- Claude, actual `claude-opus-5.5`, session `2ee199ad-f493-4216-b911-9cf44bf88107`:
  [initial report](n2-reviews/batch-11-claude-initial.md). Three minor findings concerning the
  栄 qualification, 極 reading-status wording and 栄える quiz metadata.

| Observation | Evidence-based adjudication |
| --- | --- |
| B11-01, 見栄 and the え qualification | Clarification adopted: explicitly retain the attested 見栄 みえ spelling and its show/vanity sense, and do not imply that spelling is unsuitable for everyday use. The proposed claim that a whole-word ateji flag proves each character's purely phonetic role, or establishes 栄's regular native allocation, is not adopted. The narrower allocation remains explicitly unverified lookup information, not a claim that the word is absent. |
| B11-02, 極 reading status | Consistency improvement adopted: one note gives the actual five Joyo readings on Kanjipedia's 極 page and its explicit outside-table marks for きめる/きまる. No status is inferred for every derived form. The single reading-row marker is removed, and JMdict's 決める/極める spelling list is stated neutrally, without a primary-spelling or frequency claim. |
| B11-03, 栄える and 輝く | Direct exclusion adopted. The separate はえる entry admits shine/glow for the displayed written form. The same direct reasoning adds 光る, without treating the 輝く/光る pair as transitive. Exact candidate probabilities are not required by the authoring contract and are not independently reproduced here. |
| Claude's checked-and-cleared 極める/決める observation | Additional safeguard adopted after author adjudication: the きめる homograph admits decide/settle for the same written form. A low current score does not invalidate this direct ambiguity or guarantee future exclusion. |
| Optional 欧州/西洋 | Not adopted: Europe and the Western world are related geographical/cultural concepts, not established interchangeable answer labels. No direct ambiguity was demonstrated. |
| Optional 御殿 figurative sense, 極まる homograph note and 歴とした gloss | No additional expansion required. The 極 card already gives both 極まる readings and meanings; 歴とした's genuine gloss is compatible with the established senses. The assigned scope does not require every figurative 御殿 use. |

The corrections affect four teaching pages: 栄 and 極 plus the two supporting verb articles.
The selected 52 JMdict pairs, 14 complete families, all 46 reading rows, five source-only qualifications
and all 45 curated kanji choices remain intact. One external character-reading-status record is added.
Original reports are preserved unchanged.

### Four-page correction confirmations

Corrections are committed at `d47b7bcdf38197653989bf160bb744bd70b8fd51`. Each original reviewer resumed
sequentially with its own report, the same clean checkpoint and the actual 101-line/six-hunk teaching/evidence
diff. Both read the four revised pages and confirmed all three facets CLEAN without a regression.

| Reviewer | Preserved report | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- | --- |
| GPT | [changed-passage confirmation](n2-reviews/batch-11-gpt-followup.md) | CLEAN | CLEAN | CLEAN |
| Claude | [changed-passage confirmation](n2-reviews/batch-11-claude-followup.md) | CLEAN | CLEAN | CLEAN |

B11-01, B11-02 and B11-03 are **resolved**, with calibration. Claude withdraws its overextended
character-by-character ateji allocation, the inferred status of the derived 極 forms, and its low-score
clearance of 極める/決める. GPT withdraws its initial assertion that no additional quiz exclusions were required.
Both distinguish the written-form-only Japanese-to-English ambiguity from reverse choices that include readings;
symmetric exclusions remain correct without claiming equal ambiguity in every presentation.

The author verified zero validation errors, all 165 additions/502 exact reading rows, preservation of all
52 selected pairs and character metadata, the exact ten-file correction scope, and a byte-identical repeated
manifest (version `bcb443e33c2a17a9`). These are author checks, not independently executed reviewer tests.

Claude's final optional suggestions were adjudicated separately:

- **Adopted:** 極める/選ぶ. Pinned entry 1254180 explicitly includes "to choose" in the applicable きめる
  sense, while 選ぶ's actual answer title is "choose". Its position among eleven glosses does not make the
  direct written-homograph ambiguity irrelevant. This is an independent pair, not transitive propagation
  through 決める.
- **Not adopted:** 栄える/似合う. The latter's "suit; look good on" evaluates a wearer/item match, not
  the mere shining or attractive appearance in the inspected はえる sense. No direct equivalent answer
  was established; shared appearance subject matter alone is insufficient.
- **Optional wording:** merging the two 極 status notes is nonblocking polish. One gives the character
  reading table; the other documents the exact written 極まる boundary and its independent source.

The additional 選ぶ exclusion changes only one metadata list in words/極める.md, with no new teaching prose.
It was committed at `c81161be3a918430076da745d079fca534a520e8`. Both original reviewers resumed sequentially
on that clean checkpoint and the actual one-hunk diff, inspected the exact unrestricted spelling/reading/sense
and 選ぶ's answer label, and confirmed the correction CLEAN on all three facets:
[GPT final confirmation](n2-reviews/batch-11-gpt-final.md) and
[Claude final confirmation](n2-reviews/batch-11-claude-final.md).
Claude withdrew its earlier borderline framing; GPT superseded its earlier no-remaining-pair conclusion.
There was no new teaching prose and no established regression. The author verified the exact seven-file
commit, zero validator errors and a byte-identical repeated manifest, version `5c0699d25fad591e`.
Neither reviewer executed the app or the validator; numerical candidate-pool assertions were not reproduced.

### Model usefulness and closure

Claude uniquely surfaced the qualification/context gaps and the written-homograph quiz risk in the initial
shared sample; GPT's initial report missed those issues. Claude's reports also exposed the 光る, 決める and 選ぶ
relationships, but initially dismissed or weakened them using candidate scores or the gloss's position.
Author reconciliation adopted the directly supported pairs and rejected unsupported allocation/status
inferences. GPT independently confirmed the revised passages and explicitly calibrated its earlier clearance.
These observations are useful complementary review evidence for this batch, not a general model ranking
or proof that model bias has been eliminated.

All 15 new kanji pages and four supporting articles now have independent GPT/Claude coverage; all corrected
passages have confirmation, with no actionable defect or consequential unresolved claim remaining in scope.
Batch 11 is **closed**: 165 additions review-closed, 167 selected N2 cards present, and 200 additions unauthored.

## Batch 12

Cards: 毛 氷 永 汗 汚 池 沈 河 沸 油 況 泉 泊 波 泥.

Status: **authored; independent GPT/Claude reviews pending**. Scope: all 15 new kanji and three supporting articles,
汚す, 沈める and 泊める; all three review facets and 45 curated distractor assignments.
Related edits: component links in 24 existing word articles, preserving their lexical metadata and teaching text,
and a third curated wrong answer on legacy 川 to prevent the new 河 answer from filling its fallback slot.

Evidence: [batch-12.json](n2-batch-sources/batch-12.json), with 48 exact reading rows:
44 JMdict-backed lexical examples and four explicitly qualified source-only readings. The packet retains
52 selected restriction-aware spelling/reading records. Sixteen inspected sensitive families additionally retain
complete spelling/reading lists, spelling flags and reading restrictions, not every sense of the entire dictionary.

### Authored scope and checks

- All KANJIDIC2 readings, primary stroke counts, canonical radicals and grade tags are retained.
  毛 keeps radical 毛, no. 82; the other fourteen keep 水, no. 85. The cards distinguish visible
  left-hand 氵 from the water-like forms in 氷, 永 and 泉. Mnemonics are labelled modern-shape aids,
  not unverified historical or phonetic derivations.
- 氷 distinguishes everyday こおり from the archaic ice sense ひ and the rare spelling 氷る こおる.
  The latter's spelling flag is not a pronunciation-frequency claim. 永い's selected sense is temporal,
  not an instruction to replace 長い for physical length.
- 汗 uses 発汗 はっかん for カン and 河 uses 河川 かせん for カ. Matching a native noun's initial
  kana would not independently establish those on readings. 沸騰 preserves its full ふっとう reading;
  bath-heating examples do not require boiling-temperature water.
- 汚 keeps all six native source readings and their exact dictionary pairs. 汚す's two readings share
  an entry whose disgrace/defile sense says especially けがす, not exclusively. The separately indexed
  汚れる けがれる is not redirected to the existing よごれる article.
- 沈香 じんこう/じんこ is agarwood, not the aloe plant. 油然 ゆうぜん illustrates ユウ in its
  adverb-with-と construction rather than claiming it is a second native pronunciation of oil.
- 況's `まし.て` and `おもむき` remain lookup-only with precise limits. Attested 況して まして is
  explicitly retained, with its rare-kanji-spelling and usually-kana flags; it does not establish the
  exact dotted boundary. 況んや いわんや has its own usually-kana qualification.
- 泥 uses 汚泥 おでい for デイ and specialized 泥洹 ないおん for ナイ. No suitable デ or ニ
  example was established. An initial でい in 泥水 cannot prove the shorter デ reading. 泥む retains
  the dated qualification, separate from 滞む's rare-spelling flag.
- Supporting vocabulary has no inferred JLPT labels. Each new verb explains its object pattern,
  counterpart and conjugation. Direct quiz exclusions cover the bare English soil label with 土,
  and the sinking labels of 沈める/沈む. Related meanings do not create transitive exclusion groups.
- All 18 new teaching pages were inspected by the author. Structural validation reports 0 errors;
  the accumulated source/stroke audit covers 180 additions and 550 exact reading rows, with 185 selected
  characters still unauthored. All 24 existing word articles match the preceding versions after removing
  only the new component links and normalizing CRLF. 川 differs only by its third distractor.
  These author checks do not substitute for the pending independent reviews.

### Review status

Initial GPT and Claude reviews will use the same clean committed checkpoint, complete 18-page scope,
related passages, rubric and evidence access. Each reviewer must run alone and exit before the next starts.
The first eleven batches remain review-closed; these 15 additions are not yet claimed as reviewed.
