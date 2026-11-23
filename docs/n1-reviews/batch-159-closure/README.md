# Batch 159: textual-review closure

Batch 159 of the N1 kanji work (governing [issue 60](https://github.com/stop-cran/learning-japanese/issues/60)) adds the cards
**厘 又 叔 叙 吉 后 吏 吟 呈 呉**, nine new word articles, and links two
existing kana-headed articles as the support words of 又. Its status is
**review closed with disclosed limits, publication pending**. The reviewed
snapshot is `33c3b5829887b2e49e0f67ce649fad8b2a722ea7` (`33c3b582`).
Reviewers of all three model families, Claude, GPT and Grok, each
**CONFIRMED** that snapshot with no remaining actionable finding. The way
there was one three-family blind review (r1) and then confirmation rounds on
seven successive commits: five for Claude (c1-c5), six for GPT (c1-c6) and
three for Grok (c1-c3). All 17 runs ran one after the other. After the three
families had confirmed `bad899ea`, the author found five stale "no card"
remarks; `33c3b582` turned them into links, and a fresh round of all three
families confirmed it. Main moved during the review; the signed merge
`3ecba19c` came after the last confirmation and changes no batch file (see
"Integration with current main"). The limits of that process are listed
under "Limits". Publication happens later; its receipt will record the pushed
commit, a green CI run on it and the served ZIP. No Android JVM test, Kotlin
cross-check, device or phone check was run.

## Snapshot and scope

- Members: **厘 又 叔 叙 吉 后 吏 吟 呈 呉** (source rows 135, 137, 139, 140,
  146, 147, 148, 150, 152, 153), the first ten remaining Joyo rows after B158,
  as the [issue 60 selection proposal](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7058679348) (below, "the rule") requires.
- Support articles: nine new articles, 厘 (JMdict 1555420), 叔母 (1607100),
  叙情 (1595470), 不吉 (1491910), 太后 (1787360), 官吏 (1211850), 吟味
  (1243390), 贈呈 (1403570) and 呉服 (1269190). Each article's other kanji
  already has a card. 又 has no new article: under point 2 of that proposal
  (an existing article, including a kana-headed one, that already teaches a
  suitable word is linked instead of adding one) its supports are the
  existing articles または (1524990,
  spelling 又は, ichi1/news1) and また (1524930, spelling 又, which carries no
  priority tag; ledger note at line 67). Two supports take the rule's
  untagged route: 太后 (no priority tags) and 官吏 (news2/spec2 only). The
  ledger's `selectionReason` (line 29) and the `exceptionReason` of each row
  (lines 117 and 131) explain why. 叔母 relies on the spelling-level
  ichi1/news1 tags of 叔母; the taught reading しゅくぼ, restricted to that
  spelling, carries no tag (ledger note at line 81).
- Quizzed readings: 厘 リン, 又 また, 叔 シュク, 叙 ジョ, 吉 キツ, 后 コウ,
  吏 リ, 吟 ギン, 呈 テイ, 呉 ゴ (ledger `curatedProjection`).
- Existing files changed: the kanji cards 不, 味, 太, 官, 情, 服, 母 and 贈,
  each gaining one line that links a new article; the kana-headed articles
  または and また, which now link the 又 card and show the spellings 又は and
  又; and the cards 及, 堅, 暇, 狭 and 節, where a stale remark that 又, 偏 or
  即 has no card became a link (`33c3b582`). The ledger's
  `changedReusedPassages` (line 217) lists them. With the ten cards, ten
  stroke files and nine new articles, the batch touches 44 runtime paths
  (23 kanji cards, 10 stroke files and 11 word articles). The merge proof's
  46 `b159RuntimeFiles` (`integration/merge-proof.json`) also count
  `tools/audit_n1_batch.py` and `tools/test_audit_n1_batch.py`, which learned
  the kana-headed support case. The batch also regenerates `manifest.json`
  and adds four files under `docs/n1-sources/`: `batch-159-membership.json`,
  `batch-159-jmdict.xml`, `batch-159-jmdict-selection.json` and
  `batch-159-progress.json`.
- Published base: `2787e43b5706a569d83627849aa40ed3582a7d18`, the B158
  publication receipt.
- Blind-review freeze: `1a9bb910d1bbff162f4e3920e64e8821f635a58d`, "Draft
  JLPT N1 batch 159 candidate" (authored 04:02:16 UTC on 2026-11-23; all
  times below are UTC on that day).
- Fix commits, in order:
  - `5c04be73367f8c149001318ec2ad67cf2f623ef0` (05:59:46), "N1 B159: apply
    first-round review fixes": the r1 fixes; the c1-claude, c1-gpt and
    c1-grok snapshot;
  - `4f8ebea76b9998de64d39b94df0fbaedfd50fa5d` (08:08:30), "N1 B159: apply
    second-round review fixes": the answers to c1-gpt and the c1 optional
    points; the c2-claude and c2-gpt snapshot;
  - `54b00e0ca0425b1490e5decaa58505b6e469ab72` (08:57:00), "N1 B159: apply
    third-round review fixes": the 叔母 support and two sentence splits; the
    c3-claude snapshot;
  - `f85ff382097a76e63a3bef2bc5e5b018ad96fd28` (09:20:09), "N1 B159: apply
    a third-round review note": c3-claude's optional point 1; the c3-gpt
    snapshot;
  - `0ba7df6393382bf25f8446d28c07ec9a04b55519` (09:45:30), "N1 B159:
    correct the ledger's lint warning count": c3-gpt's finding; the c4-gpt
    snapshot;
  - `bad899ea96a9a0310052bd290e50285e02acc161` (10:03:40), "N1 B159:
    correct the ledger's reading-options note": c4-gpt's optional point; the
    c5-gpt, c2-grok and c4-claude snapshot;
  - `33c3b5829887b2e49e0f67ce649fad8b2a722ea7` (12:03:58), "N1 B159: link
    the new 又, 偏 and 即 cards from stale remarks": the post-confirmation
    revision; the c6-gpt, c3-grok and c5-claude snapshot.
- Merge with main: `3ecba19ca48d16380db5f07e602a6fc8fa0f95a5` (12:56:59),
  "Merge main into N1 batch 159 candidate", with first parent `33c3b582` and
  second parent `f5caf53c`.
- Signatures and history: the freeze, the seven fix commits and the merge
  are signed with key `9D94B9D311BD26A7` (main's seven commits, which the
  same log lists, are the owner's; see "Integration with current main"); the
  history from the base to `33c3b582` is linear.
  Commits were amended only before their review round started, so every SHA a
  reviewer saw is in this history. `git log 2787e43b..3ecba19c` lists all
  subjects.

After the freeze, the supports of two kanji changed. 又's freeze support, a
new article 又聞き, was justified as "usually written in kana", which is not
one of the rule's exclusions; `5c04be73` replaced it with the existing
articles または and また, removed the frozen line on 聞 and the two JMdict
entries only that text cited (1442420 and 2025400), and changed 又's
`quizKunyomi` from また- to また. 叔's freeze support 伯叔 was kept in
`5c04be73` and recorded as an author's exception in `4f8ebea7`; `54b00e0c`
replaced it with 叔母 and withdrew the exception. 又聞き and 伯叔 have no
article, and 伯.md and 聞.md equal the base. Two other front-matter fields
changed: 吟's `quiz_exclusions` gained 検 審 査 調 究 研 (`5c04be73`) and 験
(`4f8ebea7`), and 吟味's gained 試験 and 確認 (`5c04be73`). No other quizzed
reading and no stroke file changed. The ledger is
[`docs/n1-sources/batch-159-progress.json`](../../n1-sources/batch-159-progress.json).

### This folder

- [`provenance.json`](provenance.json) records every run (model, session,
  window, API requests, tool calls, maximum calls in flight, snapshot, which
  run it confirms, flags) and the SHA-256 of each prompt, report, scope audit
  and stored packet file. `runsInChronologicalOrder` is the run list;
  `packet` and `confirmPacketFilesStored` describe the stored packets.
- [`packet/`](packet/) is the initial blind-review packet built from the
  freeze (04:37:01 UTC; 6,920 files). `3b9ff393…` in `provenance.json` is the
  SHA-256 of the full manifest's canonical JSON; that manifest is not stored.
  The stored `packet-manifest.json.gz` is a reduced copy in which the 6,832
  copies of repository kanji and word files are folded into one aggregate
  hash. The instructions, mechanical checks, diffs and evidence are stored (39
  files); the 39 snapshot files are the freeze's files, which Git reproduces
  (38 of them after LF-to-CRLF conversion, as checked out), and the four
  repository documents, four rubric files and two title files are recorded by
  hash only. Thirteen stored files (the nine diffs, `selection-order.tsv` and
  the three gzipped dictionary extracts, once decompressed) have exactly the
  manifest's bytes. Twenty-five are text files stored with LF line endings;
  the manifest hashes the CRLF bytes the reviewers saw, which converting LF
  back to CRLF reproduces. The last, `evidence/selection/rule-7058679348.md`,
  is also an LF copy, but its original mixes CRLF and LF line endings, so the
  conversion does not reproduce it; its exact bytes are stored as
  [`confirm-packet/common/evidence/rule-7058679348.md`](confirm-packet/common/evidence/rule-7058679348.md).
  `recordedFileSha256` in `provenance.json` hashes the stored bytes. The
  three dictionary extracts and `evidence/audits/word-quiz.txt` are stored
  gzipped.
- [`confirm-packet/`](confirm-packet/) (layout in its `provenance.json`)
  holds the 14 confirmation packets (`c1claude`, `c1gpt`, `c1grok`,
  `c2claude`, `c2gpt`, `c2grok`, `c3claude`, `c3gpt`, `c3grok`, `c4claude`,
  `c4gpt`, `c5claude`, `c5gpt`, `c6gpt`). Each has `INSTRUCTIONS.md` and
  `RESPONSE.md`, the author's disposition of that family's last report. Files
  identical in every packet are in `common/`; a file whose bytes were already
  stored for another packet is listed in `sameAs` instead of being copied (256
  entries). Files of 65,536 bytes or more are stored gzipped (`gzipped`; the
  recorded hashes are of the uncompressed bytes). `CHANGES.md` carries the
  change list and `checks/` the check outputs; both are stored in `c1claude`,
  `c2claude`, `c2grok`, `c3claude`, `c3gpt`, `c3grok` and `c4gpt`, while
  `c4claude` stores only the link-target check and `c5gpt` no checks, and the
  other packets list them in `sameAs`. The `c3grok` packet adds the
  stale-remark check (`checks/stale-remarks.txt`), the scan script, the
  cards 偏 and 即 and four KanjiVG files.
- [`reports/`](reports/) holds the 17 verbatim reports, [`prompts/`](prompts/)
  the 17 exact prompts, [`scope-audits/`](scope-audits/) each run's read-scope
  audit, [`integration/`](integration/) the merge proof and the batch audit at
  the merge with their scripts, and [`supplement/`](supplement/README.md) the
  condensed copy of r1-gpt's report that c1-gpt received (see "Limits"). Raw
  session logs stay local because they may hold private context.

## Review execution

The repository's review rule for new word cards and learner articles
(`.github/copilot-instructions.md`) calls for three reviewers of different
families, so, as for B156-B158, a Grok reviewer was added to the Claude and
GPT reviewers that the issue 60 proposal keeps. Models and times below come
from the runtime session records, not from the reports. Times are UTC on
2026-11-23.

| Run | Model | Snapshot | Window | API req | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| r1-claude | claude-sonnet-5.5 | `1a9bb910` | 04:39:33-04:44:46 | 31 | 32 | 2 | NEEDS FIX: two findings (1 major: the 又聞き support; 2: the 叔 reason); item 3 accepts 后 and 吏; three optional points, six limits |
| r1-gpt | gpt-6.1-sol | `1a9bb910` | 04:46:18-05:00:37 | 56 | 55 | 1 | NEEDS FIX: five findings F1-F5 (F1, F2 major); O1, L1-L3 |
| r1-grok | grok-4.7 | `1a9bb910` | 05:02:48-05:29:46 | 178 | 185 | 4 | NEEDS FIX: six minor findings F1-F6; O1-O4, L1-L3 |
| c1-claude | claude-sonnet-5.5 | `5c04be73` | 07:23:23-07:26:42 | 39 | 48 | 3 | CONFIRMED, no findings; three optional points |
| c1-gpt | gpt-6.1-sol | `5c04be73` | 07:27:08-07:37:19 | 85 | 84 | 1 | NEEDS FIX: F2, F4 partly resolved; L2, L3 partly resolved; one optional point |
| c1-grok | grok-4.7 | `5c04be73` | 07:39:54-08:02:53 | 144 | 143 | 1 | CONFIRMED, no findings; three optional points |
| c2-claude | claude-sonnet-5.5 | `4f8ebea7` | 08:31:10-08:33:10 | 26 | 28 | 2 | CONFIRMED; one minor wording note |
| c2-gpt | gpt-6.1-sol | `4f8ebea7` | 08:33:37-08:39:41 | 38 | 37 | 1 | NEEDS FIX: F4 partly resolved (fallback or owner acceptance needed); L2, L3 partly resolved; one optional point |
| c3-claude | claude-sonnet-5.5 | `54b00e0c` | 09:14:22-09:16:10 | 18 | 18 | 2 | CONFIRMED; three optional points |
| c3-gpt | gpt-6.1-sol | `f85ff382` | 09:37:13-09:43:30 | 44 | 43 | 1 | NEEDS FIX: one minor finding (the ledger's lint count) |
| c4-gpt | gpt-6.1-sol | `0ba7df63` | 09:55:41-09:59:01 | 25 | 24 | 1 | CONFIRMED, no findings; two optional points |
| c5-gpt | gpt-6.1-sol | `bad899ea` | 10:16:46-10:19:50 | 31 | 30 | 1 | CONFIRMED, no findings |
| c2-grok | grok-4.7 | `bad899ea` | 10:20:32-10:34:39 | 78 | 77 | 1 | CONFIRMED, no findings; three optional points |
| c4-claude | claude-sonnet-5.5 | `bad899ea` | 10:35:42-10:36:55 | 17 | 21 | 2 | CONFIRMED, no findings |
| c6-gpt | gpt-6.1-sol | `33c3b582` | 12:32:46-12:37:17 | 30 | 29 | 1 | CONFIRMED, no findings |
| c3-grok | grok-4.7 | `33c3b582` | 12:37:52-12:48:53 | 79 | 78 | 1 | CONFIRMED, no findings |
| c5-claude | claude-sonnet-5.5 | `33c3b582` | 12:49:20-12:51:08 | 21 | 21 | 2 | CONFIRMED, no findings |

**r1.** The three initial runs reviewed the same frozen packet one after the
other, without seeing each other's work. Each covered all four facets
(correctness, scoped coverage, consistency and quiz safety,
comprehensibility), with an assigned emphasis
([`prompts/r1-*.txt`](prompts/)): Claude on correctness, GPT on consistency
and quiz safety, Grok on comprehensibility.

**Confirmations.** Each confirmation was run by a fresh agent of the same
family as the r1 reviewer. Each received a packet with the author's
`RESPONSE.md` to its family's last report, the revised files, the exact diff
and, where the round changed them, the change list and check outputs. It could
read the original packet and its own family's earlier report, but no other
family's report. Rounds are numbered per family because the families did not
move in step. All three confirmed `5c04be73` or returned NEEDS FIX on it (c1).
Claude and GPT then reviewed `4f8ebea7` (c2); Claude confirmed `54b00e0c`
(c3); GPT reviewed `f85ff382` (c3) and confirmed `0ba7df63` (c4); and all
three confirmed `bad899ea` (c5-gpt, c2-grok, c4-claude). Grok skipped the
snapshots `4f8ebea7` to `0ba7df63`: c2-grok covered the five commits
`4f8ebea7` to `bad899ea` in one round, and a Grok packet built for
`4f8ebea7` was never run. The last round, on `33c3b582` (c6-gpt, c3-grok,
c5-claude), followed the post-confirmation revision. No two runs overlapped
in time, and each snapshot was committed before its runs started. No run
needed a follow-up prompt.

## Findings and dispositions

The disposition source is each family's `RESPONSE.md` in
[`confirm-packet/`](confirm-packet/) and the change lists in the `CHANGES.md`
files; the reviewer's label comes from that family's next report. The r1
fixes landed in `5c04be73`; line numbers below are at `33c3b582`.

### r1

The three reports converged on the supports of 又 and 叔, on quiz exclusions
around 吟 and 吟味, and on plain explanations for 太后, 官吏 and 伯叔.

| Item | Disposition |
|---|---|
| Claude 1 (major), GPT F3: 又's untagged-route reason "usually written in kana" is not a rule exclusion; an existing article should come first | The article 又聞き and its line on 聞 were removed; 又 is supported by the existing kana-headed articles または and また under point 2 of the rule. `又.md:23` and the また row (line 30) link both; `quizKunyomi` is [また] (line 12); the また- row (line 31) keeps 又聞き and 又貸し unlinked. `tools/audit_n1_batch.py` gained `support_spelling()` (lines 60-67), which accepts a mapping's spelling only for a kana-headed article whose text shows a spelling with the kanji, with five new tests. RESOLVED (c1-claude, c1-gpt) |
| Claude 2, GPT F4, Grok F2: the 叔 reason, the tags on the spellings 叔父 and 叔母, and 伯叔's senses | `5c04be73` corrected the reason and gave 伯叔 Digital Daijisen's two senses; c1-claude and c1-grok RESOLVED. c1-gpt PARTIALLY RESOLVED F4; see "c1" for how 叔母 replaced 伯叔 |
| Claude 3: the 后 and 吏 exceptions | No action; found acceptable. RESOLVED |
| Claude O1: 吏員 or 能吏 instead of 官吏 | Not changed: 官吏 shows 吏's main meaning through 官, and all three are untagged. DECLINE ACCEPTED |
| Claude O2, Grok F3, F4: 太后 is obscure; 太's new line has no bridge from "thick" | `太后.md:15` explains 皇太后 and 太皇太后 in plain terms from Digital Daijisen; `太.md:38` adds that here 太 is added to an honored person's title and does not mean "thick" (Daijisen sense 4 of 太). Resolved (c1-claude, c1-grok); the 太后 wording was refined in `4f8ebea7` and `54b00e0c` (see "c1") |
| Claude O3: JMdict's "one's father's brothers" against Daijisen's "parent's brothers" | 伯叔 gave both senses; the article was later replaced by 叔母. RESOLVED |
| Claude L1-L5 (the sixth limit, example naturalness as the reviewer's own judgement, needed no answer): Daijisen only through Weblio, 太's honorific sense, the Joyo notes, KANJIDIC2 records, 叙's ついず/ついで and 厘's "分 = next larger" | Evidence added: Digital Daijisen sections from kotobank.jp, the cited Joyo PDF pages under `evidence/joyo/`, a JMdict scan for ついず/ついで (no 叙 spelling). `厘.md:42` now says 分 ぶ is the fractional unit ten times larger, and `words/厘.md:28` that one 分 equals ten 厘. RESOLVED |
| GPT F1: 吟味 lacks an exclusion against 試験 | `吟味.md:8` excludes 試験 and, for consistency with 確かめる, 確認. RESOLVED |
| GPT F2: 吟 excludes only poetry neighbours | `吟.md:14` excludes 検 審 査 調 究 研, named with their titles at line 42 (Daijisen sense 4 of 吟, 内容を探り確かめる). PARTIALLY RESOLVED by c1-gpt (験 asked for); see "c1" |
| GPT F5: Dictionary lines omit the Digital Daijisen link | Line 34 of all nine new articles links the kotobank entry. RESOLVED |
| GPT O1: no merged card warranted; the 后 and 吏 exceptions supported | No action. DECLINE ACCEPTED |
| GPT L1: naturalness of the 伯叔 examples | Examples labeled with sense 2; naturalness remains the reviewer's judgement. DECLINE ACCEPTED |
| GPT L2, L3: manifest and app code; packet hashes do not authenticate the Git signature | Manifest rebuild and audit output, `QuizBuilder.kt` and `Words.kt`, and `git verify-commit -v` output added. PARTIALLY RESOLVED by c1-gpt; see "c2-c5" |
| Grok F1: 又's sense list "and, or or" | `又.md:23` quotes the senses one by one; the distractor note (line 48) says none of 北 国 男 means "again," "also" or "or." RESOLVED |
| Grok F5: which sense of 吟 applies in 吟味 | `吟味.md:24` says 吟 here means examining contents closely, the sense under which Daijisen lists 吟味; reciting is the original meaning. RESOLVED; the attribution was refined in `4f8ebea7` |
| Grok F6: 官吏's second example reads as modern usage; 官's line lacks "dated" | `官吏.md:18` is framed as history; `官.md:37` adds "(dated)"; `官吏.md:28` already names 公務員. RESOLVED |
| Grok O1: "obi" and "kimono section" in 呉服 | `呉服.md:18` explains the obi and the kimono-fabric counter. RESOLVED |
| Grok O2: 呈's compressed glosses | `呈.md:40` quotes 呈する's JMdict glosses in full (entry 2012430). RESOLVED |
| Grok O3, O4: 居 against 呈 ("present"); 吟味's JMdict sense 3 | Not changed; the author agreed with the reviewer. DECLINE ACCEPTED |
| Grok L1-L3: the Joyo PDF, the idiom of the examples, other Daijisen pages | Joyo page texts and kotobank sections added; the examples changed as above. RESOLVED |

### c1

| Item | Raised by | Disposition |
|---|---|---|
| F2: 験 "test; verify" also overlaps 吟's taught sense | c1-gpt | `4f8ebea7` excludes 験 (`吟.md:14`, named at line 42). RESOLVED by c2-gpt |
| F4: the 叔 row and point 2 | c1-gpt | `4f8ebea7` recorded 伯叔 as a disclosed author's exception; c2-gpt kept it PARTIALLY RESOLVED, asking for the qualifying fallback or the owner's acceptance before publication. `54b00e0c` replaced 伯叔 with 叔母 しゅくぼ (1607100), whose spelling carries ichi1/news1, and withdrew the exception. 叔母 was preferred to 叔父 because Nikkoku gives 叔父 the variant reading しゅくぶ, which the word reading quiz would offer as a wrong look-alike in 4 of 10 pairs. `叔.md` lines 29, 34 and 38 and `母.md:38` link or explain it; `words/叔母.md:32` says it is also read おば. RESOLVED by c3-gpt; c3-claude accepted the change, and c2-grok found the revised 叔 card clean |
| OPT: the ledger's `quizSafety` note (line 946 at `5c04be73`) overstated reading-option completeness | c1-gpt | Corrected in `4f8ebea7`: for 吟's ギン prompt, 二 and 自 both show ジ in one of four outcomes and the fallback fills the open slot; `KanjiReadings.kt` added as evidence. RESOLVED by c2-gpt |
| L2, L3: manifest and builder; Git object and key authenticity | c1-gpt | `KanjiReadings.kt` and an extended `verify-commit.txt` added. c2-gpt PARTIALLY RESOLVED both; c3-gpt DECLINE ACCEPTED L2; c4-gpt DECLINE ACCEPTED L3 (a local packet cannot authenticate the key) |
| O1: 太后 wording read as two different people | c1-claude, c1-grok | `4f8ebea7` rewrote `太后.md:15` ("in a narrower sense"); `54b00e0c` split the sentence for c2-gpt. RESOLVED by c2-claude and c2-grok |
| O2: 吟 exclusions as over-exclusion | c1-claude | One exclusion added (験), none removed; they act only in fallback or custom pools. RESOLVED by c2-claude |
| O3: `support_spelling` only checks that the spelling appears | c1-claude | Not changed. RESOLVED (no change; accepted) by c2-claude |
| O2: 吟味 attributes "savoring its flavor" to both sources | c1-grok | `4f8ebea7` rewrote the end of `吟味.md:24`; `54b00e0c` split it. RESOLVED by c2-grok |
| O3: 確認 on 吟味 is not a displayed-title overlap | c1-grok | Kept; it only removes a distractor. DECLINE ACCEPTED by c2-grok |

### c2-c5

- c2-claude (`4f8ebea7`) confirmed with one minor wording note on the 叔
  exception text ("reported to the owner") and called the new 験 exclusion
  an optional over-exclusion; `54b00e0c` withdrew the exception and kept 験,
  and c3-claude RESOLVED the note and DECLINE ACCEPTED 験, which acts only in
  fallback or custom pools.
- c2-gpt (`4f8ebea7`) also asked, as an optional point, to split long
  sentences in 太后 and 吟味; `54b00e0c` did so, and c3-gpt RESOLVED it.
- c3-claude (`54b00e0c`) confirmed with three optional points. Point 1, list
  おば first on the 母 card, was applied in `f85ff382` (`母.md:38`, "おば,
  also しゅくぼ"). Points 2 (annotate the 叔母 examples) and 3 (add "also
  しゅくふ" for 叔父 on the 叔 card) were declined: a note on spoken use would
  need a frequency source, and 叔父 has no article. c4-claude DECLINE
  ACCEPTED both and RESOLVED point 1.
- c3-gpt (`f85ff382`) found that the ledger still gave 37 lint warnings, 35
  on reused files; `0ba7df63` corrected it to 42 and 40, and c4-gpt RESOLVED
  it. (At `33c3b582`, whose five relinked cards bring more files into lint's
  scope, the counts are 44 and 42.)
- c4-gpt (`0ba7df63`) confirmed with two optional points: the ledger's
  reading-options summary named only 呉, and the packet's `CHANGES.md`
  overlooked `checks/link-targets.tsv`. `bad899ea` names 吉 き and 呉 ぐ, and
  the packet text was corrected; c5-gpt RESOLVED both.
- c2-grok (`bad899ea`) RESOLVED the 太后 and 吟味 wording and its limits and
  confirmed with three optional points: 親戚 and 親類 are hypernyms of 叔母,
  not title overlaps; example 2 of `words/叔母.md` reads 伯母 as はくぼ; and
  `叔.md:34` glosses 叔母 differently from the article title. None was
  changed; c3-grok DECLINE ACCEPTED all three.
- c5-gpt and c4-claude confirmed `bad899ea` with no findings and no optional
  points.

### Post-confirmation revision and the last round

After c5-gpt, c2-grok and c4-claude confirmed `bad899ea`, the author ran a
scan for sentences saying that a kanji has no card, which the B157 and B158
publication checks had not run. It found five remarks that were no longer
true: 又 in `及.md:27`, `堅.md:29` and `暇.md:27`, 偏 in `狭.md:46` and 即 in
`節.md:55` (偏 and 即 were carded by the B158 draft `60d2cd5a`). `33c3b582`
rewrote each into a link to the card followed by its title and recorded the
five lines in `changedReusedPassages`, so the audit's changed reused articles
grew from 10 to 15. The scan now runs in the author's check runner. c6-gpt,
c3-grok and c5-claude CONFIRMED `33c3b582` with no findings; c6-gpt also
fetched the four pinned KanjiVG files and found them byte-identical.

The author then checked the points the last round could not see:

- The three reviewers could not see the sentences behind the 37 remarks the
  scan lists at `33c3b582` (c5-claude suggested 無, 浪, 潮, 謹, 懺 and 憬
  might be misattributed). The author reread each one: each is about the
  listed kanji or part, `漫.md:56` names 爛 and 浪 together, and neither the
  listed subjects nor 爛 has a card. At the merge the scan lists 36, because
  main's `4797b35d` rewrote `癖.md:27`; their 33 distinct subjects still have
  no card. The scan reports separately 8 remarks whose subject it cannot
  resolve and the reviewed exception `悟.md:46`; the author read these too.
  Seven of the 8 are about the right parts of 暇 (叚), 敵 (啇) and 瞬 (舜),
  the lower part of 礎 (疋) and the kanji of the words 塞ぐ, 櫛 and 釘; the
  eighth, in `こっそり.md`, means a greeting card; and the exception is about
  the right part of 悟 (吾). None of these has a card.
- `jmdict-scan-cN.txt` is named after the check runner's round, so the file
  is renamed for each round, but its bytes have not changed since the c2
  packets (SHA-256 prefix `1eec83ea9bc69204`; c5-gpt's packet held it as
  `jmdict-scan-c6.txt`). c6-gpt could not verify the c8 packet's statement
  that `jmdict-scan-c8.txt` equals the earlier file, because its previous
  packet held the file under another name; the statement holds.
- Every coordinator copy of an earlier report that a later run read equals
  the stored report apart from line endings and trailing whitespace, except
  r1-gpt's condensed copy (see "Limits").

## Integration with current main

`origin/main` moved during the review, from the base `2787e43b` to
`f5caf53c`, through seven owner commits signed with key `AD3E63ADB89CAE86`:
`c98cfccd`, `52929231` and `174d87b9` (the sourced origin of 集, its 隹/鳥
note and the register of 集う), `4797b35d` (illness-radical mnemonics on 疲
病 症 痛 療 癖, with `docs/illness-radical-mnemonics-sources.json`),
`d513049c` (bird-component mnemonics on 唯 椎 護 雄 鳴), and `5db62b1a` and
`f5caf53c` (the 空 mnemonic and its 空手 and hunger examples). They change 13
kanji cards, one docs file and `manifest.json`, and no batch file.
`3ecba19c` is a signed merge of main into the batch branch, made after the
last confirmation, with first parent `33c3b582` and second `f5caf53c`; the
merge base is `2787e43b`. The only conflict was the derived manifest,
regenerated with `tools/build_manifest.py`. Main changed no batch file, link
target or quiz field, so, as for batches 144, 155, 156 and 157, no separate
integration review was needed.

[`integration/merge-proof.json`](integration/merge-proof.json), produced by
[`merge_proof.py`](integration/merge_proof.py), passes:

- 44,019 paths compared; every non-derived path equals one parent byte for
  byte, and none matches neither.
- Main changed 15 kept paths (the docs file, the 13 cards 唯 椎 疲 病 症 痛 療
  癖 空 護 雄 集 鳴 and `manifest.json`) and deleted none.
- The 46 batch paths are identical to `33c3b582` and not changed by main; the
  152 link targets are untouched; the manifest lists the batch files. Among
  the front matter of the 13 cards, main changed only 集's tags, and no quiz
  field.
- The one changed main line that mentions a batch kanji is in `護.md`, where
  `d513049c` rewrote "the shape 又 below it" as "隻 is the bird shape 隹 above
  the hand shape 又". It does not link `又.md` and makes no claim about its
  title, readings or quiz fields, and calling 又 a hand shape matches `右.md`
  and `寂.md`; the proof passes only if the flagged lines equal this reviewed
  entry. `雄.md` mentions the word また only on lines main left alone, and
  `狭.md` (a batch file since `33c3b582`) mentions 症, whose card main
  changed, but not its front matter.

The stock batch audit stops at the merge, because it compares the runtime
with the base manifest and main changed 13 cards after the base.
[`integration/audit-at-merge.json`](integration/audit-at-merge.json),
produced by [`audit_at_merge.py`](integration/audit_at_merge.py), proves that
main's runtime changes since the base are exactly the 13 non-docs files it
changed and that none is a batch file, then reruns the unchanged audit with
`manifest.json` read from main's head `f5caf53c`; it passes with the reviewed
counts.

Main's CI at `f5caf53c` is green
([run 45167204321](https://github.com/stop-cran/learning-japanese/actions/runs/45167204321)),
and `git ls-remote` shows `main` still at `f5caf53c` at this closure, so no
further integration is needed.

## Limits

- **The 后 and 吏 exceptions.** Two supports take the rule's untagged route:
  太后 for 后 (JMdict 1787360, no priority tags; the tagged 皇后 and 皇太后
  need 皇, which has no card, and the other tagged 后 spellings are rarely
  used or search-only forms of 後 words) and 官吏 for 吏 (1211850, news2 and
  spec2 only; no 吏 entry carries news1, ichi1, spec1 or gai1). r1-claude,
  r1-gpt, r1-grok and c1-gpt found the row-specific justifications
  sufficient, and c2-grok noted that they remain the batch's untagged
  exceptions; the owner's acceptance is not recorded. 又 needs no exception:
  its support is the existing kana-headed article または (spelling 又は,
  ichi1/news1), linked under point 2 of the rule, and the existing article
  また (spelling 又, untagged) is mapped as well.
- **The 叔母 support.** It relies on the spelling-level ichi1/news1 tags of
  叔母: the tagged reading is おば, and the taught reading しゅくぼ,
  restricted to that spelling, carries no tag. c3-gpt found that this meets
  point 2 without an exception, and c3-claude, c4-claude and c2-grok
  confirmed it. The B156 伯 row (伯仲) was not revisited; c2-grok noted that
  it lies outside this diff and is the owner's decision.
- **Changed supports.** Two supports changed during review: 又聞き became
  または and また in `5c04be73`, with `tools/audit_n1_batch.py` extended to
  accept a kana-headed article; 伯叔 was kept with a corrected reason, then
  recorded as an author's exception in `4f8ebea7`, and after c2-gpt asked for
  the qualifying fallback or the owner's acceptance, `54b00e0c` switched to
  叔母 and withdrew the exception.
- **Uneven rounds.** The families confirmed different intermediate
  snapshots: Claude confirmed `5c04be73`, `4f8ebea7`, `54b00e0c`, `bad899ea`
  and `33c3b582`; GPT returned NEEDS FIX on `5c04be73`, `4f8ebea7` and
  `f85ff382` and confirmed `0ba7df63`, `bad899ea` and `33c3b582`; Grok
  confirmed `5c04be73`, `bad899ea` and `33c3b582`, so c2-grok covered five
  commits in one round. All 17 runs were sequential, and each saw only its
  own family's reports.
- **The copy of r1-gpt's report given to c1-gpt.** c1-gpt received, as its
  "own initial report", a condensed coordinator copy of r1-gpt's final
  message (2,342 of 5,329 characters) that wrongly calls itself verbatim. It
  keeps every finding's number, severity, files, claim and remedy but drops
  most evidence. `RESPONSE.md` answered the full report, and c1-gpt gave a
  disposition for every point. The copy is stored in
  [`supplement/`](supplement/README.md); the full report is
  [`reports/r1-gpt.md`](reports/r1-gpt.md). Every other copy of an earlier
  report given to a later run equals the stored report apart from line
  endings and trailing whitespace.
- **Unnamed models.** No report names an exact model version: the Claude
  reports say Claude or Claude (Anthropic), the GPT reports say the model
  identifier is not exposed, and the Grok reports say no model id was
  exposed. The models in the table (claude-sonnet-5.5, gpt-6.1-sol and
  grok-4.7 in every run) come from the session events.
- **Execution.** Several runs had overlapping tool calls (r1-claude, r1-grok
  and c1-c5 Claude; at most 4 in flight) or recursive shell commands over
  packet directories (r1-claude 2, r1-gpt 5, c1-grok 1); see
  [`scope-audits/`](scope-audits/). Each run wrote at most its own report
  file. The outside-path flags of r1-grok, c1-grok, c2-grok and c3-grok are
  false positives: a runtime tool-output file, the reviewer's own report
  folder, and packet or allowed paths that the audit read from JSON-quoted
  arguments. The audits attribute packet reads only to view and grep calls,
  so files that GPT runs read through shell commands appear as unread in
  their coverage tables; the shell commands are listed in each audit.
- **Reports.** GPT wrote no report file in any round; every stored GPT report
  is the run's final message. The c1-c5 Claude report files differ in wording
  from their final messages, with the same labels and verdicts; the files are
  stored. The r1-claude and Grok report files equal their final messages
  apart from whitespace.
- **Web use.** Reviewers fetched public dictionary pages and data (Weblio,
  Kotobank, jisho.org, kanjiapi.dev, the Japanese Wikipedia list of joyo
  kanji and the Agency for Cultural Affairs Joyo PDF), the four pinned
  KanjiVG files (c6-gpt) and public files of this repository and of the app
  repository on GitHub (r1-gpt and c3-gpt; c1-grok's one attempt failed),
  some through shell downloads; each run's web calls and shell commands are
  listed in its scope audit. c2-claude, c3-claude, c4-claude, c5-claude,
  c4-gpt, c5-gpt and c3-grok made none.
- **Context compaction.** The runtime compacted the context twice in r1-grok
  and once in r1-claude, c1-gpt, c1-grok and c2-grok; those runs continued
  from a summary of their earlier reading. The other 12 runs were not
  compacted. These counts come from the local session log; `provenance.json`
  does not record compaction.
- **Prompts.** Every prompt was saved to a file before use. Each stored
  prompt equals, byte for byte, the first message recorded in its reviewer
  session.
- **Quiz evidence.** 10 latent reading collisions are not drawable in the
  checked N1, All and Starter pools: 厘 り; 又 やす, ふたたび; 吉 え, き, と,
  よ, えい; 吏 し; 呉 ぐ. 吟's ギン prompt can fill one wrong slot from the
  fallback (61 drawable options, no exposure hit). The reading-exposure audit
  samples 200 seeds and is not exhaustive. The reading audits are the
  author's Python ports of the Kotlin builder, kept outside the repository.
- **Lint.** Lint reports 11 errors and 73 warnings at the merge `3ecba19c`
  (3 and 44 at the reviewed `33c3b582`). None is on the nine new articles,
  and no error is on the ten new cards. Three errors are metadata readings
  without a Readings row on 太 (タ) and 情 (セイ, なさ.け), older than the
  batch, which only adds one line to each. The other eight are the same kind
  of error on 疲, 病, 痛, 空 and 鳴, cards that main changed and lint
  therefore checks at the merge; main added none of those readings. Of the
  warnings, 42 are on reused files, 2 on 又's kana-headed examples, and 29 on
  main's cards and the words they list.
- **Unreviewed merge.** The merge `3ecba19c` came after the last
  confirmation and was not reviewed; the merge proof shows that main changed
  no batch file or link target, and the one changed main line naming a batch
  kanji (`護.md`, 又 as a hand shape, unlinked) is recorded as reviewed by
  the author. The stock batch audit fails at the merge; `audit_at_merge.py`
  passes with main's head as the runtime baseline. CI does not run the batch
  audit.
- **Stale remarks.** The publication checks of B157 and B158 did not run the
  stale-remark scan, so their cards 偏 and 即 left two "no card" remarks
  stale until `33c3b582`; the scan now runs in the author's check runner. It
  finds only sentences worded with its phrase list, and the author read the
  37 remarks it lists at `33c3b582` (36 at the merge) and the 8 it cannot
  attribute.
- **Unlinked mentions of 又.** 27 older cards mention 又 in their text
  without linking the new 又 card (伎 努 友 双 反 収 取 受 右 寂 度 径 怒 怪 慢
  投 捜 支 桑 耳 護 賢 趣 軽 隻 騒 鼓). None says that 又 has no card, so the
  stale-remark scan does not flag them; linking them is left as an optional
  follow-up. The batch cards 叔 and 叙 name 又 only in their radical lines,
  which no card links.
- **Confirmation evidence.** The gate results come from the author's runs
  included in the packets and in this closure, not from reviewer reruns.
- **Checks not run.** No Android JVM test, Kotlin reading cross-check (no JDK
  on the continuation machine), native, rendered-font, device or phone check
  was run. Phone acceptance is outstanding, not inferred.
- **Closure storage.** Confirmation packets are deduplicated by content
  (`sameAs` in `confirm-packet/provenance.json`, 256 entries), and files of
  64 KiB or more are gzipped. A check of the 712 stored or referenced
  confirmation-packet files (snapshot copies excluded) against each packet
  manifest found 0 errors. In the initial packet, 13 stored files have the
  bytes the reviewers saw and 25 are LF copies of CRLF files that convert
  back to the manifest's hashes; the rule text is an LF copy of a file with
  mixed line endings, whose exact bytes (SHA-256 prefix `77d5bc8b`) are in
  `confirm-packet/common/` (see "This folder"). Snapshot files are
  reproducible from Git at the freeze; rubric, repository-document and
  title files are recorded by hash only.
- **Superseded material.** No published commit is rewritten, no reviewed
  commit was amended, and every run's final report is kept.
- **Scope of verification.** The publication receipt will verify this exact
  published runtime and ZIP, not the remaining N1 set. A later
  contributor-only receipt commit needs its own CI and exported-tree equality
  check.

## Validation and accounting

At the merge `3ecba19c` (the author's check runner, round c9; the reviewed
`33c3b582` was round c8): validation 0 errors; 444 unit tests pass; manifest
rebuild no diff (9,842 files, version `2113084de3ce05a4`, SHA-256
`4d3efd69a7271c2be3f1db64df80c3300c4d5ccfb350aff8f4ffad9a8bc106f5`; at
`33c3b582` version `44a04d20d52264cd`, SHA-256
`01433ac8317c2033b01d112c7f44056e5c64a24563f81e2998bde3967bb56cc5`); budget
9,849 files, 9,865 entries, 56,884,466 retained, 57,320,538 inflated,
36,537,070 local-ZIP and 5,893,602 listening-media bytes (56,881,479,
57,317,551 and 36,535,569 at `33c3b582`; CI limits 62 MiB retained, 80 MiB
inflated, 42 MiB compressed); vocabulary 3201/3539, exit 0; batch audit
(at `33c3b582`, and at the merge through `audit_at_merge.py`) pass with 10
kanji, 9 new words, 15 changed reused articles, 11 reciprocal pairs, 0
activated baseline pairs, 21 reading dispositions, 10 curated offered keys,
0 source-only keys and 87 dictionary families; `diff --check` with
`cr-at-eol` from the base to the merge clean; stale-remark scan 0 stale
remarks over 6,831 articles (1,608 kanji cards), 1 reviewed exception
(`悟.md:46`), 36 listed remarks (37 at `33c3b582`) and 8 without a kanji;
lint 11 errors and 73 warnings (3 and 44 at `33c3b582`; see "Limits"); quiz
safety 10 cards, 0 errors, 0 warnings, with every meaning question taking its
three wrong options from curated distractors and only 吟's ギン prompt
filling one reading slot from the fallback, while 11 existing cards (人 休 何
入 出 口 女 日 月 男 買) fill one slot from the fallback, as before; reading
exposure 200 seeds, 0 production, 0 padded and 0 one-holder hits, 10 latent
collisions; reading options 100 seeds, 0 problems, exit 0, with two
informational notes on 吉 き (offered by 28 cards) and 呉 ぐ (供 具 工 求).
Validation, unit tests, quiz safety, reading exposure, reading options,
vocabulary, the diff check, the word-quiz audit and the distractor evidence
gave identical results at `33c3b582`. Rerun on the closure commit, the other
checks above, including `integration/audit_at_merge.py`, give the same
results. There, `git diff --check` from the base flags 34 files, all captured
patches, diff excerpts and evidence copies in this folder that keep their
recorded bytes (as in B156-B158): trailing whitespace and, in 12 of them, a
blank line at the end of the file. Outside this folder it is clean. CI does
not run `diff --check`.

After publication, delivery becomes **618/1,228**, with **610 remaining**.
Until then it stays at 608 published, plus these 10 review-closed cards.

Left for a later pass, outside this batch: the lint errors on the reused
cards 太 and 情 and on main's cards 疲, 病, 痛, 空 and 鳴; the 10 latent
reading collisions above; the declined optional points (吏員 or 能吏 for 官吏,
居 on 呈, 吟味's JMdict sense 3, the 験 and 確認 exclusions, the 叔母
annotations and 叔父's "also しゅくふ", 親戚 and 親類 on 叔母, はくぼ in
叔母's example 2, the gloss on `叔.md:34`, and a stricter `support_spelling`
check); the 27 older cards that mention 又 without linking it; and the
owner's acceptance of the untagged supports 太后 for 后 and 官吏 for 吏.
