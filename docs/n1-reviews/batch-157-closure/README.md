# Batch 157: textual-review closure

Batch 157 of the N1 kanji work (governing [issue 60](https://github.com/stop-cran/learning-japanese/issues/60)) adds the cards
**佐 佳 併 侍 侮 侯 俊 俗 俵 倫** and one new word article for each. Its status
is **review closed with disclosed limits, publication pending**. The reviewed
snapshot is `2420189965098bd34bdb227a0efbe320d558c612` (`24201899`). In the
second confirmation round (c2), reviewers of all three model families, Claude,
GPT and Grok, each **CONFIRMED** that snapshot with no remaining actionable
finding. The way there was longer than for batch 156: one three-family blind
review (r1), four GPT-only intermediate rounds (r2-r5) and two three-family
confirmation rounds (c1, c2). The limits of that process are listed under
"Limits". Publication happens later; its receipt will record the pushed
commit, a green CI run on it and the served ZIP. No Android JVM test, Kotlin cross-check, device or phone check was run.

## Snapshot and scope

- Members: **佐 佳 併 侍 侮 侯 俊 俗 俵 倫** (source rows 38, 40, 41, 43, 46,
  47, 50, 51, 55, 60), the first ten remaining Joyo rows after B156, as the
  [issue 60 selection proposal](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7058679348) requires.
- Support articles, all new, one per kanji: 補佐, 佳作, 併用, 侍, 侮る, 諸侯,
  俊足, 俗語, 俵 and 倫理. Each article's other kanji already has a card. 諸侯
  (JMdict 1344250) is the only support word without a qualifying priority tag;
  the ledger's `selectionReason` and the `exceptionReason` on its
  `supportMappings` row explain why (侯爵 and 王侯 carry only news2/spec2,
  侯爵 would also need 爵, which has no card, and 侯補 is only a search-only
  spelling of 候補).
- Quizzed readings: 佐 サ, 佳 カ, 併 ヘイ, 侍 さむらい, 侮 あなど.る, 侯 コウ,
  俊 シュン, 俗 ゾク, 俵 たわら, 倫 リン (ledger `curatedProjection`).
- Existing files changed: the kanji cards 作, 助, 理, 用, 補, 語, 諸 and 足,
  and `tools/audit_n1_batch.py`. With the ten cards, ten stroke files and ten
  articles, the batch touches 38 runtime paths. The merge proof's 40
  `b157RuntimeFiles` (`integration/merge-proof.json`) also count the tool and
  the word article 速い, which gained a 俊足 quiz exclusion in `f1a69909`
  before the merge; the redesign `689f0d4d` removed it again, because the
  exclusion declared on 俊足 covers the pair both ways.
- Published base: `e2c25363285fd8fa100d1c4178e7289592562a31`, the B156
  receipt.
- Blind-review freeze: `a5c6a0ff970ab61e81d82e0d9a1c5ce06d7c96a0`
  (authored 07:32:58 UTC on 2026-11-22).
- Pre-merge fix commits, in order (re-signed SHA, then the original SHA; the
  r2-r5 reviewers saw the first four original SHAs):
  - `2798cfbc6a135f55d59215d64a07f353f52fe05d` (was `77ff93d9`), "Reconcile
    B157 review findings": the r1 fixes, including the 合併 supplement; the
    r2 snapshot;
  - `c89376693d22c5155edc4de434f8ede7faecfbb8` (was `77f56733`): the r2
    fixes; the r3 snapshot;
  - `967b8603c88781d7ba1a3c5a40afe1e46c8a11e1` (was `4bf9db0c`): the r3
    fixes; the r4 snapshot;
  - `e2ef32e545d7c3f3a8e5f39d9b2fbbfdba7672e0` (was `f811f8eb`): the r4
    fixes; the r5 snapshot;
  - `f1a699094f4a7dd3aa4490ef83247f95c3af6bea` (was `970bb0dc`), "Close final
    B157 review findings": the r5 fixes.
- Re-signing: these five commits were first signed with key
  `AD3E63ADB89CAE86` and then re-signed with `9D94B9D311BD26A7`, the key that
  signed the freeze and every other commit in the range. The trees are
  identical. The r2-r5 reviewers saw the first four originals; the original
  r5 fix `970bb0dc` was never reviewed as a snapshot, because c1 reviewed the
  merged result. All five originals exist only on the unpushed local branch
  `b157-candidate-pre-resign`.
- Merge: `684d754ce6181f1cd4ac8e26b0561697df55872c`, first parent `f1a69909`,
  second `origin/main` at `2bc61140` (see "Integration with current main").
- After the merge: 14 commits from `bf910786` to
  `cd5d75d186efa11b89e64e215dbb239a09d93639` (the c1 snapshot, authored
  15:47:42 UTC)
  finish the r1 dispositions, tie wording to sources and redesign the
  distractors; then `81142e4a` and `0daebfba` apply the c1 findings and
  `24201899` refreshes the ledger's manifest version (authored 17:48:24 UTC).
  The c2
  runs started at 18:35. `git log e2c25363..24201899` lists all subjects.

After the freeze, every kanji card's `distractors` list changed (the frozen
same-sound sets 左 差 査, 価 加 果 and so on were replaced by Starter cards; see
"Findings"), and quiz exclusions were added on all ten cards and on every
article except 諸侯. The 倫 title changed from "ethics; moral order" to "ethics;
moral principles" and the 侮る title from "look down on; underestimate" to
"look down on; make light of". No other title, metadata reading, quizzed
reading or stroke file changed. The ledger is
[`docs/n1-sources/batch-157-progress.json`](../../n1-sources/batch-157-progress.json).

### This folder

- [`provenance.json`](provenance.json) records every run (model, session,
  window, API requests, tool calls, maximum calls in flight, snapshot, which
  run it confirms, flags) and the SHA-256 of each prompt, report, scope audit
  and stored packet file. `runsInChronologicalOrder` is the run list;
  `packet`, `roundPackets` and `confirmPacketFilesStored` describe the stored
  packets; `sameAs` maps a packet path to the stored copy with identical bytes.
- [`packet/`](packet/) is the initial blind-review packet built from the
  freeze (07:37:23 UTC; 6,863 files). `608133e4…` in `provenance.json` is the
  SHA-256 of the full manifest's canonical JSON; that manifest is not stored.
  The stored `packet-manifest.json.gz` is a reduced copy in which the 6,792
  copies of repository kanji and word files are folded into one aggregate
  hash. The instructions, mechanical checks, diffs and evidence are stored;
  card files are Git blobs at the snapshot, and the rubric and title files
  are recorded by hash only.
- [`round-packet/`](round-packet/) holds the r2-r5 packets as deltas: each
  round stores only the files not stored before (14, 4, 3 and 3 files). Each
  round's `manifest-delta.json` lists the manifest entries that differ from
  the initial packet; [`round-packet/provenance.json`](round-packet/provenance.json)
  records the 18 files equal to the initial packet and, for r3-r5, the 12, 13
  and 13 files reused from earlier rounds. Its candidates are the original
  SHAs; the re-signed commits have the same trees.
- [`confirm-packet/`](confirm-packet/) (layout in its `provenance.json`)
  holds the six confirmation packets
  (`c1claude`, `c1gpt`, `c1grok`, `c2claude`, `c2gpt`, `c2grok`). Each has
  `INSTRUCTIONS.md` and `RESPONSE.md`, the author's disposition of that
  family's last report. Files identical in every packet are in `common/`; a
  file whose bytes were already stored for another packet is listed in
  `sameAs` instead of being copied. `c1claude/CHANGES.md` and
  `c2claude/CHANGES.md` carry the change lists, and their `checks/` folders
  the check outputs.
- [`reports/`](reports/) holds the 21 verbatim reports, [`prompts/`](prompts/)
  the exact prompts (including `c2-claude-followup-1.txt`),
  [`scope-audits/`](scope-audits/) each run's read-scope audit, and
  [`integration/`](integration/) the merge proof and its script. Raw session
  logs stay local because they may hold private context.

## Review execution

The repository's review rule for new word cards and learner articles
(`.github/copilot-instructions.md`) calls for three reviewers of different
families, so, as for B156, a Grok reviewer was added to the Claude and GPT
reviewers that the issue 60 proposal keeps. Models and times below come from
the runtime session records, not from the reports. All times are 2026-11-22
UTC.

| Run | Model | Snapshot | Window | API req | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| r1-claude | claude-sonnet-5.5 | `a5c6a0ff` | 07:37:55-07:41:43 | 18 | 39 | 7 | NEEDS FIX: ten findings C1-C10 (C1, C2 major; C3 minor-to-major); O1-O5, L1-L3 |
| r1-gpt | gpt-6.1-sol | `a5c6a0ff` | 07:41:52-07:54:13 | 64 | 63 | 1 | NEEDS FIX: nine findings G1-G9 (G1-G7 major) |
| r1-grok | grok-4.7 | `a5c6a0ff` | 07:54:28-08:11:37 | 93 | 99 | 3 | NEEDS FIX: eleven findings X1-X11 (X1-X5 major); O1-O6 |
| r2-gpt-quiz-safety | gpt-6-luna | `77ff93d9` | 08:38:08-08:45:33 | 50 | 49 | 1 | NEEDS FIX: two minor (佐/助; 王侯, 俊英) |
| r2-gpt-correctness | gpt-6-luna | `77ff93d9` | 08:38:08-08:45:14 | 63 | 62 | 1 | NEEDS FIX: one minor (俊英, 王侯 called common) |
| r2-gpt-coverage | gpt-6-luna | `77ff93d9` | 08:38:08-08:45:06 | 52 | 51 | 1 | NEEDS FIX: two minor (俊英; 不倫 missing) |
| r3-gpt-coverage | gpt-6-luna | `77f56733` | 09:02:07-09:10:49 | 60 | 59 | 1 | NEEDS FIX: two minor (佐ける; 侮る example) |
| r3-gpt-quiz-safety | gpt-6-luna | `77f56733` | 09:02:07-09:08:09 | 52 | 51 | 1 | CLEAN |
| r3-gpt-correctness | gpt-6-luna | `77f56733` | 09:02:07-09:08:57 | 55 | 54 | 1 | CLEAN |
| r4-gpt-correctness | gpt-6-luna | `4bf9db0c` | 09:16:03-09:22:07 | 77 | 76 | 1 | CLEAN |
| r4-gpt-coverage | gpt-6-luna | `4bf9db0c` | 09:16:03-09:22:11 | 56 | 55 | 1 | NEEDS FIX: one minor (佳い) |
| r4-gpt-quiz-safety | gpt-6-luna | `4bf9db0c` | 09:16:03-09:24:19 | 96 | 95 | 1 | NEEDS FIX: two minor (佳い; 諸侯 exception) |
| r5-gpt-correctness | gpt-6-luna | `f811f8eb` | 09:29:23-09:36:21 | 73 | 72 | 1 | NEEDS FIX: one minor (理, 助 Readings rows) |
| r5-gpt-quiz-safety | gpt-6-luna | `f811f8eb` | 09:29:23-09:36:14 | 53 | 52 | 1 | NEEDS FIX: two minor (俊足 claim; 俊足/速い) |
| r5-gpt-coverage | gpt-6-luna | `f811f8eb` | 09:29:23-09:35:58 | 89 | 88 | 1 | CLEAN |
| c1-claude | claude-sonnet-5.5 | `cd5d75d1` | 16:08:06-16:13:48 | 77 | 78 | 2 | CONFIRMED r1 items; one minor F1 (五倫); O1-O5 |
| c1-gpt | gpt-6.1-sol | `cd5d75d1` | 16:14:21-16:31:18 | 88 | 87 | 1 | NEEDS FIX: two minor (五倫; 倫理/仁); G1-G9, L1, L2 resolved |
| c1-grok | grok-4.7 | `cd5d75d1` | 16:32:04-16:47:19 | 128 | 127 | 1 | CONFIRMED, no findings; optional O1-O3 |
| c2-claude | claude-sonnet-5.5 | `24201899` | 18:35:38-18:40:03 | 40 | 44 | 2 | CONFIRMED, no findings; three optional points |
| c2-gpt | gpt-6.1-sol | `24201899` | 18:40:59-18:50:07 | 74 | 73 | 1 | CONFIRMED, no findings |
| c2-grok | grok-4.7 | `24201899` | 18:51:01-19:03:18 | 79 | 78 | 1 | CONFIRMED, no findings, no optional points |

r2-r5 snapshots are the original SHAs of the re-signed commits.

**r1.** The three initial runs reviewed the same frozen packet one after the
other, without seeing each other's work. Each covered all four facets
(correctness, scoped coverage, consistency and quiz safety,
comprehensibility), with an assigned emphasis
([`prompts/r1-*.txt`](prompts/)): Claude on correctness, GPT on consistency
and quiz safety, Grok on comprehensibility.

**r2-r5.** After the r1 fixes the author ran four more rounds on intermediate
snapshots. Each round ran three GPT-family reviews in parallel, one per facet
(correctness, coverage, quiz safety). No model was requested; the model was
inherited from the session, and the session records show gpt-6-luna. These
rounds **do not meet the three-family rule**; they are extra checks, and their
findings were fixed in the commits listed above. The three-family
confirmations are c1 and c2.

**c1 and c2.** Each confirmation was run by a fresh agent of the same family
as the r1 reviewer, one family at a time (no two confirmation runs
overlapped). Each received a packet with the author's `RESPONSE.md` to its
family's last report, the change list, the revised files, the exact diff and
the check outputs, and could read the original packet. c1 reviewed
`cd5d75d1`; c2 reviewed `24201899`, which was committed before c2 started.
c2-claude's first pass did not cover the scope its instructions required, so
it received one follow-up prompt
([`prompts/c2-claude-followup-1.txt`](prompts/c2-claude-followup-1.txt)) that
asked it to complete the reading and to correct its execution record, and
said it was not a request to change any verdict. It then confirmed.

## Findings and dispositions

The disposition source is each family's `RESPONSE.md` in
[`confirm-packet/`](confirm-packet/) and the change lists in
`c1claude/CHANGES.md` and `c2claude/CHANGES.md`. The r1 fixes landed in
`2798cfbc` and in the post-merge commits up to `cd5d75d1`; the response files
give the fixed lines at `cd5d75d1`, not a commit per finding. c1 judged every
r1 item below as stated.

### r1

The three families largely found the same quiz-safety gaps: meaning overlaps
between the new titles and existing cards that no `quiz_exclusions` entry
guarded.

| Item | Disposition |
|---|---|
| C1, G3, X2: word 侍 "samurai" against 武士 "samurai; warrior" | `words/侍.md` excludes 武士; the 侍 card adds 武 (士 was already excluded at the freeze). Resolved |
| C2, G4, X3: 侮る against 見下ろす "look down on" | `words/侮る.md` excludes 見下ろす. Resolved |
| C3, G5, X7: 補佐 also overlaps 助手, 手伝い, 世話 and others | 補佐 excludes 援助, 助手, 手伝い, 世話, 手伝う, 助ける, 支える, 応援; 併 excludes 兼; the unsourced role-contrast sentence was removed. Resolved |
| C4, G1, G2, X4, X5: kanji titles overlap unguarded cards, including secondary senses | Exclusions now: 佐 [丞 助 援 支 副], 佳 [美 良 善 宜 優 俊 傑 秀 英 卓 豪 偉 華], 併 [合 兼 結 並 共 協 接 括 統 斉], 侍 [士 武 臣 仕 僕 兵], 侮 [卑], 侯 [殿], 俊 [秀 英 傑 才 優 卓 豪 賢 偉 哲], 俗 [凡 卑], 俵 [袋], 倫 [伴 輩 徳 義 善]. The ledger lists them under `kanjiQuizAudit`, and `audit_n1_batch.py` fails on a mismatch. Resolved |
| C5: 諸侯 has no priority tag | Kept as the sole, explicit exception; the ledger records why. Resolved (c1-claude; c1-gpt L1) |
| C6: 倫 "moral order" is not a source gloss | Title "ethics; moral principles". Resolved |
| C7, Claude O1: 倫 omits 不倫 and the companion sense; 佐 omits the military rank; short lines for 不倫 and 大佐 | 不倫, 絶倫, the companion sense and 大佐 added. Resolved |
| C8, X1: 侮る taught as "underestimate" | Title "look down on; make light of"; examples glossed from JMdict. Resolved |
| C9: 併用 drifts into medical advice | The Distinctive-meaning sentence was replaced; example 1 (medicine) kept. DECLINE ACCEPTED |
| C10, Grok O1: filler synonyms; vague mnemonics | Synonym sections rewritten; the 佳 and 併 mnemonics removed; 佐's labelled shape note kept. Resolved |
| G6, X6: 佳作 excludes 傑作 but not 名作 | 佳作 excludes 傑作, 名作, 作品, 制作. Resolved |
| G7: 俵 against 袋 "bag; sack" | Word 俵 excludes 袋, バッグ, 鞄; the card excludes 袋. Resolved |
| G8: 佐's military-rank branch missing | 大佐 added (JMdict 1413740); 少佐 and 中佐 not added. Resolved |
| G9, X9: 俗's vulgar branch missing | Explained, with 風俗's senses; no example word, because the candidates fail the common-word rule. Resolved |
| X8, Claude O2: 合併, the most frequent 併 word, missing | 合併 がっぺい (JMdict 1578970) added with a dictionary supplement. Resolved |
| X10: 俊足 combination unexplained | Combination sentence added; the gifted-person sense labelled, no example. Resolved |
| X11: "source-only" jargon in Readings rows | Removed from the batch rows; あなず.る explained as Daijisen's older form of あなどる. Resolved |
| Claude O3, O4: sense citations; unsourced nuance claims | Sense-1 citations on 補佐, 倫理, 諸侯; the 補佐/援助 nuance claims removed. Resolved |
| Claude O5: 理 lacks ことわり; 語 phonetic | 理 ことわり row added; the 語 phonetic key is outside the batch. Resolved for 理, DECLINE ACCEPTED for 語 |
| Grok O2: 倫's note explains a quiz decision | Rewritten. Resolved |
| Grok O3, O4, O5: per-kanji contributions in 倫理/補佐; a noun example for 補佐; em dashes | Not changed. DECLINE ACCEPTED by c1-grok |
| Grok O6: 土俵 as the ヒョウ example | Already met. Resolved |
| Claude L1-L3, GPT L1-L2, Grok L1-L2: evidence for 内侍, the selection policy, quiz mechanics, the 諸侯 justification, manifest, budget and signatures, and the 理/語 lint errors | Evidence supplied in the c1 packets. Resolved; Grok L2 DECLINE ACCEPTED for 語 |

Changes no r1 report asked for: the author's own quiz-safety check failed the
frozen distractors (29 errors, 1 warning: missing Notes sentences, excluded
pairs inside option sets, and same-sound sets that pushed the reading question
onto fallback cards). `689f0d4d` replaced all ten sets with Starter cards far
from the card's meaning and reading. Word exclusions 併用 [使用 利用 使う 用いる
用 用途] and 俗語 [言葉 単語 語] were added, and 倫理 gained 善 next to the
frozen 道徳 (仁 was also added, then dropped after c1); 俊足 [速い] came from
r5. The mirror declarations on 助 and 速い were removed, because a declaration on
either card already excludes the pair both ways. Unverifiable frequency and
comparison wording was removed or tied to JMdict entries (佳い 1605820, 佐ける
1344410, 併せる 1284480, 併せて 1506010, 俵 ひょう 1583390, 内侍 1582520), and
助 and 理 use the existing "kun, source-only here" label (`dc34fa86`).

### r2-r5

- r2 (`2798cfbc`): 俊英 and 王侯 were presented as common although they carry
  only news2/spec2 (correctness, coverage, quiz safety); 倫 lacked 不倫; 佐
  should exclude 助. Fixed in `c8937669`: the 俊英 and 王侯 lines removed,
  不倫 added, 佐/助 excluded, the audit tool extended.
- r3 (`c8937669`): the rare spelling 佐ける on 佐, and the 侮る example
  translation. Fixed in `967b8603`.
- r4 (`967b8603`): the rare spelling 佳い, and a documented exception for the
  untagged 諸侯. Fixed in `e2ef32e5`.
- r5 (`e2ef32e5`): 理 ことわり and 助 す.ける/すけ lacked Readings rows; the
  俊足 note said the "swift horse" sense belongs only to 駿足, which did not
  reflect Daijisen's 俊足 entry (it points to 駿足 sense 2, swiftness of foot);
  the note now cites both entries; 俊足 needed an exclusion against 速い. Fixed in `f1a69909`.

### c1

| Item | Raised by | Disposition |
|---|---|---|
| F1: `kanji/倫.md:38` reduces 五倫 to filial piety | c1-claude, c1-gpt (minor) | `81142e4a` removed the 五倫 sentence and entry 1593605; 不倫 now reads "immorality; especially infidelity, an extramarital affair", with Daijisen's broader clause at lines 34 and 38. RESOLVED by c2-claude and c2-gpt |
| F2: excluding 仁 on 倫理 is not a direct overlap | c1-gpt (minor) | `81142e4a` removed it; 倫理 excludes 道徳 and 善; the comparison with 仁 in the body stays. RESOLVED by c2-gpt |
| Claude O1, GPT P2, Grok O1: sets rejectable by category (侍 父母子 and 佐 母友子 from all three; 俵 田土木 from c1-claude and c1-gpt; 俊 安少多 from c1-claude; 侯 国京社 from c1-gpt) | all three | `81142e4a`: 侯 [女 国 金], 俵 [田 車 本], 侍 [父 男 魚]; `0daebfba` replaced the generic 男 with 雨, giving 侍 [父 雨 魚]. 佐 [母 友 子] and 俊 [安 少 多] kept. RESOLVED for the changed sets, DECLINE ACCEPTED for 佐 and 俊 |
| Claude O2: 事 "matter, affair" next to 不倫 | c1-claude | 倫 now [力 時 名] (`81142e4a`). RESOLVED |
| Grok O3: Daijisen's broader 不倫 clause | c1-grok | Added (`81142e4a`). RESOLVED |
| Claude O3: over-exclusions; 憎/侮 and 無視/侮る | c1-claude | Not changed: conservative guards; the curated set fills every wrong slot. DECLINE ACCEPTED |
| Claude O4, GPT P4, Grok O2: labels and quiz selection for 助 and 理 | all three | Not changed: the batch keeps plain-language rows, 助 and 理 keep the repository label, and their legacy quiz selection is untouched. DECLINE ACCEPTED |
| Claude O5: the sex-service sense of 風俗 on 俗 | c1-claude | Not changed: sourced and stated as a separate third sense. DECLINE ACCEPTED |
| GPT P1, P3, P5: "only reading" on 俵; 言語 on 俗語; shorten `併.md:39` and `俊足.md:32` | c1-gpt | Not changed. DECLINE ACCEPTED |
| Claude L1-L3; GPT L1 (four latent readings) | c1-claude, c1-gpt | Evidence supplied; Claude's RESOLVED, GPT's L1 DECLINE ACCEPTED (still disclosed) |

`24201899` changes only ledger line 127 (the audit sentence and manifest
version). No review ran on `81142e4a` or `0daebfba`; c2 reviewed their net
effect.

### c2

All three families confirmed `24201899` with no actionable finding. Points
raised and not applied: c2-claude noted that `倫.md:38` is a little formal,
that `倫.md:34` repeats itself and that the reasoning for 友 is not uniform
with the other sets; c2-gpt noted that 女 is a search-only form in JMdict
1344370; c2-grok noted, in its Limits, the label-count slip in the c2 response.
None was applied.

## Integration with current main

`origin/main` moved once during the review, to `2bc61140`, the owner-requested
prune of raw N1 review screenshots, transcripts and archives (docs only; CI
green, [run 45013027506](https://github.com/stop-cran/learning-japanese/actions/runs/45013027506)). `684d754c` is a signed merge of it into the batch
branch, with first parent `f1a69909` and second `2bc61140`; the merge base is
`e2c25363`. Because c1 and c2 reviewed post-merge snapshots, the merge lies
inside the reviewed diff `e2c25363..24201899`. The merge had no conflicts:
its tree `82d52d8f` equals git's automatic merge of the two parents. Main
changed no runtime path and no reviewed batch text, so, as for B156, no
separate integration review was needed under the issue 60 contract.

[`integration/merge-proof.json`](integration/merge-proof.json), produced by
[`merge_proof.py`](integration/merge_proof.py) (adapted from B156's), passes:

- 49,469 paths compared; none matches neither parent.
- Main changed three kept paths: `README.md`, `docs/n1-authoring-notes.md` and
  `docs/n1-reviews/README.md`; it deleted 5,998 paths, 5,936 of them binary.
- The 40 batch runtime paths are identical to `f1a69909` and not changed by
  main; the 68 link targets are untouched; the manifest lists the batch files.
- No line main changed mentions a batch kanji or word. The notes file
  mentions 速い only on unchanged lines; the deleted raw transcripts mention
  batch kanji.

`git ls-remote` shows `main` still at `2bc61140` at this closure, so no
further integration is needed.

## Limits

- **r2-r5 are single-family.** They used GPT only, with the model inherited
  from the session rather than requested, and ran their three facets in
  parallel, so runs overlapped. r2's start event logged gpt-6.2-astra, while
  gpt-6-luna ran. The three-family rule is met only by c1 and c2.
- **Re-signed commits.** The five pre-merge fix commits were re-signed
  with identical trees (mapping under "Snapshot and scope"). The SHAs the
  r2-r5 reviewers saw, `77ff93d9`, `77f56733`, `4bf9db0c` and `f811f8eb`,
  and the original r5 fix `970bb0dc`, which no reviewer saw as a snapshot,
  exist only on an unpushed local branch.
- **Unnamed models.** The r1 GPT and Grok reports do not name their model;
  the models in the table come from the session events.
- **Execution and reports.** Several runs made overlapping or recursive
  commands ([`scope-audits/`](scope-audits/)). Some reports were not written
  to file and were recovered from the final message: r1-gpt,
  r3-gpt-quiz-safety, all r4 and r5 runs, c1-gpt and c2-gpt. GPT wrote neither
  its c1 nor its c2 report file; their scope audits show no missing-report
  flag because the author had already saved the recovered text at the report
  path before the audit ran.
- **r1-claude's two texts.** Its report file has 8,908 characters and its
  archived final message 6,209. Both have the same ten findings; the extra
  details (結/接/協, 助, 圭) are covered by the current exclusions, and 佳 has
  no mnemonic.
- **c1-gpt** read whole files.
- **c1-claude** wrote that it made one call at a time; it had up to two in
  flight.
- **c2-claude** needed one follow-up because its first pass was shallow. It
  made six overlapping starts and deleted and recreated its report file.
- **c1-grok** listed the reports folder.
- **c2-grok's stray grep.** One grep without a path (pattern
  `quizExclusions`, glob `Words.kt`) searched the session's working directory
  and hit the author's workspace copy of `Words.kt`. The 52.4 KB output went to
  a temporary file Grok never opened; it saw a three-line preview, disclosed
  this accurately and did not use it as evidence. Its five "outside path"
  scope-audit flags are false positives (packet paths passed as JSON lists).
- **A c1 fix introduced a generic distractor.** `81142e4a` gave 侍 the
  distractor 男; `0daebfba` replaced it with 雨 before c2.
- **助 and 理 quiz selection** is the legacy one and is unchanged; the author
  declined to change it, and all three c2 reviewers accepted the decline.
- **Packet-builder bug.** A bug in the author's confirmation-packet builder
  (`n1_confirm_packet.py`, outside the repository) was fixed before c2.
- **女 on 侍.** JMdict 1344370 lists 女 only as a search-only form, so
  rejecting 女 as a distractor for 侍 was a precaution.
- **Count slip.** c2 `RESPONSE.md` lines 68-69 say "97 other kanji cards",
  70 kun and 43 on. In the freeze packet the exact labels are on 98 cards (70
  "kun, source-only here", 44 "on, source-only here", 16 with both), and two
  more cards (潜, 狭) use different wording, 100 in all. It affects only the
  reviewer-facing text; c2-grok raised it.
- **Checks not run.** No Android JVM test, Kotlin reading cross-check (no
  JDK), device or phone check was run. Phone acceptance is outstanding, not
  inferred.
- **Optional polish not applied:** `倫.md:34` repeats itself and `倫.md:38`
  is a little formal.
- **Grok reviewer.** Grok was added because the batch adds word articles, the
  same reason as for B156.
- **Closure storage.** Confirmation packets are deduplicated by content
  (`sameAs` in [`provenance.json`](provenance.json)); r2-r5 packets are stored
  as per-round deltas. A dedupe check of the 356 stored or referenced
  confirmation and round-packet files (222 and 134, snapshot copies excluded)
  found 0 errors; 72 of the round files were matched by hash to the initial
  manifest. The initial packet was not checked this way. Snapshot files are
  Git blobs; rubric and title files are recorded by hash only.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository; the reading-exposure audit
  samples 200 seeds and is not exhaustive. It reports 4 latent collisions
  that no checked N1, All or Starter pool can draw: 佳 けい and えい, 侍 かみ,
  俗 しょく.
- **諸侯.** The c1 reviewers found the row-specific justification for the
  untagged support word sufficient; the owner's acceptance of the exception
  is not recorded.
- **Confirmation evidence.** The gate results come from the author's runs
  included in the packets (`checks/`), not from reviewer reruns.
- **Context compaction.** The runtime compacted the context once in
  r1-grok, c1-claude, c1-gpt and c1-grok; those runs continued from a summary
  of their earlier reading. The other 17 runs were not compacted. These counts
  come from the local session log; `provenance.json` does not record
  compaction.
- **Prompts.** Every prompt was saved to a file before use. Each stored
  prompt equals, byte for byte, the first message recorded in its reviewer
  session; `c2-claude-followup-1.txt` equals that session's second message.
- **Superseded material.** No published commit is rewritten. The five
  pre-merge fix commits were re-signed after r5 and before the merge
  (above). Every run's final report is kept.

## Validation and accounting

At `24201899` (c2 packet checks, `confirm-packet/c2claude/checks/`):
validation 0 errors; 439 unit tests pass; manifest rebuild no diff (9,783
files, version `b6a770ce2d8d0049`, SHA-256
`362934d52dd70786f50939c2a7a26b59a5c4c34595aea64a32fb543d8200b4c5`); budget 9,790 files, 9,806 entries,
56,739,555 retained, 57,175,627 inflated, 36,459,996 local-ZIP and 5,893,602
listening-media bytes (limits: 62 MiB retained, 80 MiB inflated, 42 MiB
compressed, 20 MiB listening media, 18,000
entries); vocabulary 3201/3539, exit 0; batch audit pass
(10 kanji, 10 new words, 8 changed reused articles, 10 reciprocal pairs, 17
reading dispositions, 27 dictionary families); `diff --check` clean; lint 1
error, the pre-existing unknown `phonetic` key in `kanji/語.md` outside the
batch (語 only gains a link line), and 44 warnings, all on pre-existing reused
files, none on the ten new cards or articles; quiz safety 10 cards, 0 errors,
0 warnings, every reading question taking 3/3 wrong options from curated
distractors, while 11 existing cards fill one slot from the fallback, as
before; reading exposure 0 production, 0 padded and 0 one-holder hits, 4
latent collisions; reading options 0 problems. Rerun on the closure commit,
the checks above give the same results. There, `git diff --check` from the base
flags only trailing spaces inside captured patches, evidence and verbatim
reports in this folder, which keep their recorded bytes (as in B156); outside
this folder it is clean. CI does not run `diff --check`.

After publication, delivery becomes **598/1,228**, with **630 remaining**.
Until then it stays at 588 published, plus these 10 review-closed cards.

Left for a later pass, outside this batch: the labels and quiz selection of
the legacy 助 and 理 readings, and the declined optional wording points
above.
