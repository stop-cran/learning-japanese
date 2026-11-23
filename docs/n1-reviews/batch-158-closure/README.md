# Batch 158: textual-review closure

Batch 158 of the N1 kanji work (governing [issue 60](https://github.com/stop-cran/learning-japanese/issues/60)) adds the cards
**偏 偽 傍 債 勲 匠 匿 升 即 却** and one new word article for each. Its status
is **review closed with disclosed limits, publication pending**. The reviewed
snapshot is `ef00345d1adda1a32524ba7f81091621d49ddaf3` (`ef00345d`).
Reviewers of all three model families, Claude, GPT and Grok, each
**CONFIRMED** that snapshot with no remaining actionable finding. The way
there was one three-family blind review (r1) and then confirmation rounds on
four successive fix commits: four for Claude (c1-c4) and three each for GPT
and Grok (c1-c3). Unlike B157, no single-family intermediate round ran and no
merge was needed. The limits of that process are listed under "Limits".
Publication happens later; its receipt will record the pushed commit, a green
CI run on it and the served ZIP. No Android JVM test, Kotlin cross-check,
device or phone check was run.

## Snapshot and scope

- Members: **偏 偽 傍 債 勲 匠 匿 升 即 却** (source rows 63, 67, 68, 72,
  120, 123, 125, 126, 131, 132), the first ten remaining Joyo rows after B157,
  as the [issue 60 selection proposal](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7058679348) requires.
- Support articles, all new, one per kanji: 偏見 (JMdict 1510380), 偽造
  (1224580), 傍観 (1518800), 負債 (1498080), 勲章 (1247240), 師匠 (1308900),
  匿名 (1454470), 升 (1346290), 即座 (1404180) and 返却 (1512180). Each
  article's other kanji already has a card. 升 ます is the only support word
  without a qualifying priority tag: it carries only news2/spec2, which the
  rule does not count. The ledger's `selectionReason` and the
  `exceptionReason` on its `supportMappings` row explain why: no entry written
  with 升 carries news1, ichi1, spec1 or gai1, 1346290 is the only 升 entry
  with any priority marker, and the alternatives 升 しょう (2248100), 一升
  (1163460), 一升瓶 (1163470) and 升目 (1654590) are untagged.
- Quizzed readings: 偏 ヘン, 偽 ギ, 傍 ボウ, 債 サイ, 勲 クン, 匠 ショウ,
  匿 トク, 升 ます, 即 ソク, 却 キャク (ledger `curatedProjection`).
- Existing files changed: the kanji cards 名, 師, 座, 章, 見, 観, 負, 返 and
  造, each gaining one line that links the new article, and the word article
  片寄る, whose 偏る sentence now links the 偏 card. With the ten cards, ten
  stroke files and ten articles, the batch touches 40 runtime paths; it also
  regenerates `manifest.json` and adds four files under `docs/n1-sources/`.
- Published base: `ad1694c1fe537a090c712065e77c480deb9edf4d`, the B157
  closure correction made after the B157 receipt.
- Blind-review freeze: `60d2cd5ae62371e2713ef666d41de75a91f9b9fb`, "Draft
  JLPT N1 batch 158 candidate" (authored 21:15:54 UTC on 2026-11-22).
- Fix commits, in order:
  - `6605a8b089fe174b9fd2f1159e3bb917612cf379` (22:31:50), "N1 B158: apply
    first-round review fixes": the r1 fixes; the c1-claude snapshot;
  - `ccc046bbed099e2d610404c6e2392ac47f65498e` (23:41:52), "N1 B158: justify
    the 升 quiz exclusion of 腰掛け": the answer to c1-claude's finding; the
    c1-gpt, c1-grok and c2-claude snapshot;
  - `348c4f70465633c63706133babacda198eedaa27` (00:34:27 on 2026-11-23),
    "N1 B158: drop two homograph-only quiz exclusions": the c1-gpt fixes and
    two optional points; the c2-gpt, c3-claude and c2-grok snapshot;
  - `ef00345d1adda1a32524ba7f81091621d49ddaf3` (01:07:46), "N1 B158: name 升
    in the 腰掛け contrast sentence": one optional wording change
    (`words/升.md:28`); the c3-gpt, c4-claude and c3-grok snapshot.
- Signatures and history: every commit is signed with key
  `9D94B9D311BD26A7`; the history from the base is linear. Commits were
  amended only before their review round started, so every SHA a reviewer saw
  is in this history. `git log ad1694c1..ef00345d` lists all subjects.

After the freeze, four front-matter values changed: 偏 gained the exclusion
側, 偽's distractor 犬 became 耳, 偏見 gained the exclusion 意見, and the 升
article's title changed from "measuring box; box seat" to "measuring box".
Two more exclusions were added in `6605a8b0` and removed again in `348c4f70`:
腰掛け on the 升 article and 皮 on the 匿 card (see "Findings"). No metadata
reading, quizzed reading or stroke file changed. The JMdict selection grew
from 73 entries at the freeze to 86 in `6605a8b0` and 87 from `ccc046bb`. The
ledger is [`docs/n1-sources/batch-158-progress.json`](../../n1-sources/batch-158-progress.json).

### This folder

- [`provenance.json`](provenance.json) records every run (model, session,
  window, API requests, tool calls, maximum calls in flight, snapshot, which
  run it confirms, flags) and the SHA-256 of each prompt, report, scope audit
  and stored packet file. `runsInChronologicalOrder` is the run list;
  `packet` and `confirmPacketFilesStored` describe the stored packets.
- [`packet/`](packet/) is the initial blind-review packet built from the
  freeze (21:37:48 UTC; 6,900 files). `7e2a4e38…` in `provenance.json` is the
  SHA-256 of the full manifest's canonical JSON; that manifest is not stored.
  The stored `packet-manifest.json.gz` is a reduced copy in which the 6,812
  copies of repository kanji and word files are folded into one aggregate
  hash. The instructions, mechanical checks, diffs and evidence are stored (38
  files); the 40 snapshot files are Git blobs at the freeze, and the four
  repository documents, four rubric files and two title files are recorded by
  hash only. Thirteen stored files (the ten diffs and the three gzipped
  dictionary extracts, once decompressed) have exactly the manifest's bytes.
  The other 25 are text files stored with LF line endings; the manifest hashes
  the CRLF bytes the reviewers saw, which converting LF back to CRLF
  reproduces. `recordedFileSha256` in `provenance.json` hashes the stored
  bytes. The three dictionary extracts and `evidence/audits/word-quiz.txt`
  are stored gzipped.
- [`confirm-packet/`](confirm-packet/) (layout in its `provenance.json`)
  holds the ten confirmation packets (`c1claude`, `c1gpt`, `c1grok`,
  `c2claude`, `c2gpt`, `c2grok`, `c3claude`, `c3gpt`, `c3grok`, `c4claude`).
  Each has `INSTRUCTIONS.md` and `RESPONSE.md`, the author's disposition of
  that family's last report. Files identical in every packet are in
  `common/`; a file whose bytes were already stored for another packet is
  listed in `sameAs` instead of being copied. Files of 65,536 bytes or more
  are stored gzipped (`gzipped`; the recorded hashes are of the uncompressed
  bytes). The `c3gpt` files under `evidence/integrity/manifest/` and
  `evidence/integrity/trees/` are raw `git cat-file` output of commits in this
  history and are kept by hash only (`gitDerived`). `CHANGES.md` in `c1claude`,
  `c1gpt`, `c2claude`, `c2gpt` and `c3gpt` carries the change list, and their
  `checks/` folders the check outputs (`c2claude` has only the link-target
  check).
- [`reports/`](reports/) holds the 13 verbatim reports, [`prompts/`](prompts/)
  the 14 exact prompts (including `c3-claude-followup-1.txt`), and
  [`scope-audits/`](scope-audits/) each run's read-scope audit. Raw session
  logs stay local because they may hold private context.

## Review execution

The repository's review rule for new word cards and learner articles
(`.github/copilot-instructions.md`) calls for three reviewers of different
families, so, as for B156 and B157, a Grok reviewer was added to the Claude
and GPT reviewers that the issue 60 proposal keeps. Models and times below
come from the runtime session records, not from the reports. Times are UTC;
windows that start before midnight are on 2026-11-22, the rest on
2026-11-23.

| Run | Model | Snapshot | Window | API req | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| r1-claude | claude-sonnet-5.5 | `60d2cd5a` | 21:38:23-21:43:45 | 34 | 35 | 2 | NEEDS FIX: three findings C1-C3 (C1 major); O1-O5, L1 |
| r1-gpt | gpt-6.1-sol | `60d2cd5a` | 21:44:59-21:56:36 | 43 | 42 | 1 | NEEDS FIX: six findings G1-G6 (G1, G2, G5 major); O1-O2, L1-L2 |
| r1-grok | grok-4.7 | `60d2cd5a` | 21:58:12-22:20:23 | 146 | 151 | 3 | NEEDS FIX: nine findings X1-X9 (X1-X5 major); O1-O7 |
| c1-claude | claude-sonnet-5.5 | `6605a8b0` | 23:33:50-23:37:32 | 47 | 54 | 3 | CONFIRMED; one minor F1 (腰掛け exclusion); one optional point |
| c1-gpt | gpt-6.1-sol | `ccc046bb` | 00:11:49-00:19:32 | 49 | 48 | 1 | NEEDS FIX: two minor (匿/皮, 升/腰掛け); L1 partly resolved; O1 |
| c1-grok | grok-4.7 | `ccc046bb` | 00:13:19-00:31:16 | 145 | 144 | 1 | CONFIRMED, no findings; optional P1-P4 |
| c2-claude | claude-sonnet-5.5 | `ccc046bb` | 00:18:24-00:19:32 | 17 | 16 | 1 | CONFIRMED, no findings; one optional point |
| c2-gpt | gpt-6.1-sol | `348c4f70` | 00:56:32-01:01:33 | 40 | 39 | 1 | UNVERIFIED: F1, F2 resolved, no new defect; L1 limits remain |
| c3-claude | claude-sonnet-5.5 | `348c4f70` | 00:56:32-01:00:02 | 29 | 29 | 2 | CONFIRMED, no findings |
| c2-grok | grok-4.7 | `348c4f70` | 00:56:32-01:06:49 | 65 | 64 | 1 | CONFIRMED, no findings; one optional point |
| c4-claude | claude-sonnet-5.5 | `ef00345d` | 01:26:34-01:27:06 | 9 | 8 | 1 | CONFIRMED, no findings |
| c3-grok | grok-4.7 | `ef00345d` | 01:26:34-01:31:23 | 29 | 28 | 1 | CONFIRMED, no findings |
| c3-gpt | gpt-6.1-sol | `ef00345d` | 01:26:34-01:38:37 | 79 | 78 | 1 | CONFIRMED, no findings; all four facets CLEAN |

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
move in step: c1-claude ran alone on `6605a8b0`, and its minor finding was
answered in `ccc046bb` before the GPT and Grok confirmations started. From
then on, the runs of different families ran in parallel on the same snapshot:
c1-gpt, c1-grok and c2-claude on `ccc046bb`; c2-gpt, c3-claude and c2-grok on
`348c4f70`; c3-gpt, c4-claude and c3-grok on `ef00345d`. Each snapshot was
committed before its runs started. c3-claude's first report confirmed, but
its Limits said it had not made some reads its instructions required, so it
received one follow-up prompt
([`prompts/c3-claude-followup-1.txt`](prompts/c3-claude-followup-1.txt))
asking it to read `勲章.md` in full, 腰掛け's front matter, the two ledger
exclusion rows and the quiz code, and then to revise its dispositions,
verdicts and Limits as those reads required. Its revised report gives the
same dispositions and verdict.

## Findings and dispositions

The disposition source is each family's `RESPONSE.md` in
[`confirm-packet/`](confirm-packet/) and the change lists in the `CHANGES.md`
files. The r1 fixes landed in `6605a8b0`; line numbers below are at
`ef00345d`. The c1 reviewers judged every r1 item below as stated.

### r1

The three reports converged on the support word 升 (its missing priority tag,
its seating sense and the jargon about tags) and on quiz-safety gaps where an
existing card's title overlapped a new one.

| Item | Disposition |
|---|---|
| C1, G5, X3: the support word 升 ます carries only news2/spec2 | Kept as the sole, explicit exception under the rule's untagged route (rule point 2); the ledger's `selectionReason` (line 29) and `exceptionReason` (line 132) record why and cite the precedents 仙人 and 伯仲 (B156) and 諸侯 (B157). Resolved (c1-claude, c1-gpt, c1-grok); the owner's acceptance is not recorded |
| C2, X8: priority-tag jargon in the 升 Notes | The tag sentence was removed from `kanji/升.md:40`; no frequency wording replaces it, because the tags are not frequency evidence. Resolved |
| C3, Claude O4: readings the cited sources give but the cards do not show | One Notes line each: 偏 ひとえに, spelled 偏に in JMdict 1510320 (`偏.md:42`); 傍 ホウ with 傍輩 (1517130) and そ.う (`傍.md:46`); 匿 匿す (1170650), ジョク and かく.れる (`匿.md:42`); 即 ショク (`即.md:45`); 升 のぼ.る (`升.md:40`). None is quizzed. Resolved |
| Claude O1: 返却's "How the kanji combine" line | Not changed; the line ties the combination to the Daijisen sense of 却 that lists 返却, and no source was found for the suggested wording. DECLINE ACCEPTED |
| Claude O2: "a wooden masu" | "a wooden masu (measuring box)" at `words/升.md:18`. Resolved |
| Claude O3: 隠す and 隠れる as 匿名 exclusions | Not changed: they mean hiding, not anonymity, and appear nowhere in the word-quiz audit. DECLINE ACCEPTED |
| Claude O5: checks with no defect found | No answer needed |
| Claude L1: JMdict entries cited but not in the packet | The nine entries were added to the c1 packet's `jmdict-cited-entries.xml`. Resolved |
| G1: 偏見 against 意見 "opinion" | 偏見 excludes 意見 (1156530); `偏見.md:28` states the difference. Resolved |
| G2, X1: the seating sense (G2) and the grid-square sense (X1) of the word 升 | Title "measuring box" instead of "measuring box; box seat"; line 15 explains the box-seating sense with 升席 (1706800); the grid-square sense (1346290 sense 3) is no longer taught on the article; the kanji card's ます row reads "measuring box; also box seating at a theatre". 席, 座席 and 客席 score 2 in the word-quiz audit and are not drawn. Resolved |
| G3: 偏 against 側 | 偏 excludes 側 (`偏.md:14`; reason at line 40). Resolved |
| G4: 偽's distractor 犬, whose JMdict sense 4 is "counterfeit" (1258330) | Replaced by 耳 (1317170). Resolved |
| G6, X5: 債権 described as held by the lender; 債権 against 債券 | `債.md:40` cites JMdict's antonym marks between 債務 and 債権; line 23 gives the readings and says 債権 and 債券 sound the same but are different words; the サイ row adds 債券 (1292070). Resolved |
| GPT O1, Grok O1: "order" in 勲章 | `勲章.md:15` says it is an order of merit, not a command. Resolved |
| GPT O2, Grok O2: stable master and Rakugo in 師匠 | `師匠.md:15` explains the stable master; line 18 glosses Rakugo. Resolved |
| GPT L1, L2: manifest, app code and signatures; the selection order | Evidence supplied in the c1 packet, including `selection-order.tsv`. L2 Resolved; L1 PARTIALLY RESOLVED at c1 and resolved at c3 (see "c2-c4") |
| X2: the 昇 interchange on 升 | `升.md:23` limits it to Daijisen's senses 2-3 (rising; a peaceful age). Resolved |
| X4: 即's opening | `即.md:23` uses つく with 即位, then すなわち; 色即是空 dropped. Resolved |
| X6: 勲's rank example | `勲.md:23` uses 元勲 (1260770) and 勲一等 (1247200) instead of 叙勲. Resolved |
| X7: 却's "completely" sense illustrated with 冷却 | Illustrated with 忘却 (1519260). Resolved |
| X9: 匿 "hide; shelter" against 皮 "skin; hide" | Excluded in `6605a8b0` (RESOLVED by c1-grok); removed again in `348c4f70` after c1-gpt's finding (see "c1"). DISPUTE ACCEPTED by c2-grok |
| Grok O3: kana at first mention | Readings added for 偏狭, 人偏, 傍系, 傍流 and 元勲. Resolved |
| Grok O4: 座 in 即座 | `即座.md:24` says 座 means a seat or to sit. Resolved |
| Grok O5: the 傍観 example translation | "You must not just stand by…" at `傍観.md:17`. Resolved |
| Grok O6: "spurious article" and "source-only" | 偽物 glossed "forgery; counterfeit; imitation" (1577800) at `偽.md:32`; "source-only" defined at `偽.md:44` and `却.md:43`. Resolved |
| Grok O7: the repeated "meaning-quiz distractors are…" sentences | Kept; 126 kanji cards use the pattern. DECLINE ACCEPTED |

Changes no r1 report asked for: Notes lines of the C3 kind on 債 (か.り and
か.し, `債.md:42`) and 勲 (いさおし, `勲.md:42`), added for consistency.

### c1

| Item | Raised by | Disposition |
|---|---|---|
| F1: the 升 article still excluded 腰掛け "seat; bench" after its title became "measuring box" | c1-claude (minor) | `ccc046bb` kept the exclusion and stated the reason at `升.md:28` (JMdict 1288370); c2-claude RESOLVED it. Reversed by the next row in `348c4f70`; c3-claude RESOLVED the reversal |
| F1, F2: 匿 excluded 皮, and the 升 article excluded 腰掛け, without a direct meaning overlap in the displayed titles | c1-gpt (minor) | `348c4f70` removed both; the sourced contrasts stay in the bodies (`匿.md:40`, `升.md:28`). The rule: `docs/content-format.md` lines 115, 124 and 129, the B139 峠 fix `3b6f9727`, and B130's note that English homographs alone do not compel guards (excerpts in `c2gpt/evidence/exclusion-precedents.md`). For the 升 article, 腰掛け is now one of 669 words tied at the last-slot score 5, with 俵 the one candidate above them; 匿's curated distractors are 父 魚 年 and 皮's are 波 彼 坂. RESOLVED by c2-gpt; c2-grok DISPUTE ACCEPTED (X9) and RESOLVED (E2, its item on 腰掛け) |
| L1: the manifest, signed Git objects and kanji-reading builder were not reproduced | c1-gpt | PARTIALLY RESOLVED at c1; see "c2-c4" |
| O1: replace "not in this card's metadata" | c1-gpt | Kept; 12 published cards use it (救 椋 泡 淡 渇 滅 滑 漫 潔 炎 甚 環). DECLINE ACCEPTED by c2-gpt |
| Optional: split `偏見.md:28` | c1-claude | Not changed; each batch article keeps a one-paragraph Synonyms section. DECLINE ACCEPTED by c2-claude |
| P1: 勲章 "honour" against 勲 "honor" | c1-grok | "honor" from `348c4f70`; 186 corpus lines use "honor" and 8 "honour". RESOLVED by c2-grok |
| P2: 傍系 compresses JMdict 1518840 | c1-grok | Not changed; the reviewer noted it is not false. DECLINE ACCEPTED |
| P3: the 意見 and 腰掛け exclusions are precautionary | c1-grok | 腰掛け removed (above); 意見 kept. DECLINE ACCEPTED |
| P4: 耳 山 白 can be rejected by category | c1-grok | Not changed; not a meaning collision. DECLINE ACCEPTED |

### c2-c4

- c2-claude (`ccc046bb`) confirmed with one optional point, to split
  `升.md:28`; `348c4f70` applied it with different wording, and c3-claude
  RESOLVED it.
- c2-grok (`348c4f70`) confirmed with one optional point, that "its" in
  `升.md:28` could be read as 腰掛け. `ef00345d` rewrote the sentence as "The
  second sense of 升 is a whole box of seating, such as a 升席, not a single
  seat or bench."; c3-grok and c4-claude RESOLVED it. The suggested "In 升's
  second sense" was not used because the sentence would then name 升 twice.
- c2-gpt (`348c4f70`) resolved F1 and F2 and accepted the O1 decline, but
  returned UNVERIFIED because L1's integrity limits remained. The c3-gpt
  packet added `evidence/integrity/`: the six signed commit objects from the
  base to `ef00345d` with their payloads and signatures, the signing key, the
  manifest blobs and trees, the manifest builder, 14 Kotlin files of
  `stop-cran/kanji-cards-android` at
  `91e1d4b578859f7bfb582f7b9c6acf48c6ca6a75` (the kanji-reading builder and
  the quiz, padding and content-loading code it depends on; `QuizBuilder.kt`
  and `Words.kt` are stored once, in `confirm-packet/common/evidence/`),
  the Python ports, and a read-only `verify.py`. c3-gpt ran `verify.py
  --prior-packet`, which checked the commit hashes and signatures (with
  `gpgv` against the supplied key), the linear parent chain, the trees, the
  signed manifests and the snapshot files; it matched the supplied key to the
  key GitHub publishes for the owner and the base commit to the GitHub API,
  and RESOLVED L1. It confirmed with all four facets CLEAN.
- c3-claude, c3-grok and c4-claude raised no findings and no optional points.

## Integration with current main

`origin/main` did not move during the review: it stayed at `ad1694c1`, the
batch base, from the freeze to this closure, so the batch needed no merge and
no integration review. `git ls-remote` shows `main` still at `ad1694c1` at
this closure.

## Limits

- **The 升 exception.** All three c1 reviewers found the row-specific
  justification for the untagged support word sufficient under the rule's
  untagged route; the owner's acceptance of the exception is not recorded.
- **Reversed decisions.** Two exclusions that reviewers had accepted were
  removed after a later finding: 腰掛け on the 升 article (accepted by
  c1-claude and c2-claude in its justified form) and 皮 on 匿 (requested by
  r1-grok, RESOLVED by c1-grok). The later rounds of both families confirmed
  the removals.
- **Uneven rounds.** The families confirmed different intermediate snapshots
  (c1-claude `6605a8b0`, c1-gpt and c1-grok `ccc046bb`), and confirmation runs
  of different families overlapped in time. Each run saw only its own
  family's reports.
- **c2-gpt UNVERIFIED.** GPT returned UNVERIFIED on `348c4f70` because it
  could not reproduce the manifest, the signed objects or the reading builder
  from the packet; c3-gpt confirmed `ef00345d` with the added integrity
  evidence. Its remaining limits: only the snapshot is bound by content, the
  Kotlin code was not compiled, no phone check was run, and the served ZIP
  does not exist yet.
- **Unnamed models.** The GPT reports and all Claude reports but one name
  only the vendor; c3-claude names itself claude-opus-5.5, "not verifiable
  from inside the session", while the session records show
  claude-sonnet-5.5. The r1 Grok report says its model version was not
  identified; the c1-c3 Grok reports name Grok 4.7. The models in the table
  come from the session events.
- **Execution and reports.** Several runs made overlapping or recursive
  commands ([`scope-audits/`](scope-audits/)). r1-claude created, ran and
  removed a scratch script in its temporary folder; c3-claude created and
  removed a temporary copy of its report; c1-grok created its report folder
  and listed it, and c2-grok listed its own, file names only; c3-grok wrote
  its report with a PowerShell here-string. r1-grok's "outside path" flags
  are false positives. GPT wrote no report file in any round; every GPT report
  was recovered from the final message and equals it exactly. r1-claude and
  the four Grok reports equal their final messages apart from whitespace. The
  c1-c4 Claude report files differ in wording from their final messages
  (9,167 against 3,607 characters for c1, 4,429 against 2,419 for c2, 6,303
  against 4,282 for c3 and 1,648 against 1,834 for c4), with the same labels
  and verdicts; the files are stored. The copy of r1-grok's report given to
  c1-grok began with a one-line coordinator note naming its source agent and
  model; the stored report does not have it.
- **c3-claude** needed one follow-up to complete required reads; its
  dispositions and verdict did not change.
- **Web use.** Reviewers consulted public sources: r1-claude (4 fetches:
  Jisho, EDRDG), r1-gpt (7: Kanjipedia, Weblio), r1-grok (1: Jisho), c1-gpt (2:
  Kanjipedia, Weblio), c1-grok (13: Wikipedia, Jisho, Kanjipedia), c2-gpt (4:
  Weblio), c2-grok (2: Wiktionary, Jisho) and c3-gpt (12 fetches and one
  search: GitHub API, GitHub, raw GitHub content, Weblio). The other runs made
  no web calls.
- **Context compaction.** The runtime compacted the context once in
  r1-claude, r1-grok and c1-grok; those runs continued from a summary of
  their earlier reading. The other 10 runs were not compacted. These counts
  come from the local session log; `provenance.json` does not record
  compaction.
- **Prompts.** Every prompt was saved to a file before use. Each stored
  prompt equals, byte for byte, the first message recorded in its reviewer
  session; `c3-claude-followup-1.txt` equals that session's second message.
- **Reading options.** The reading-options check exits 1 with 2 problems at
  every snapshot from the freeze on: in the full-pool fallback, 傍's prompt
  ボウ could be offered そう and 即's prompt ソク could be offered しょく, both
  readings Kanjipedia marks as outside the Joyo table. The shipped N1, All and
  Starter pools never reach the fallback for these cards (reading exposure: 0
  production and 0 padded hits), and both cards say the reading is not
  quizzed (`傍.md:46`, `即.md:45`).
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository; the reading-exposure audit
  samples 200 seeds and is not exhaustive. It reports 4 latent collisions that
  no checked N1, All or Starter pool can draw: 傍 び (a KANJIDIC2 name
  reading) and そう, 升 のぼる, 即 しょく.
- **Lint on reused cards.** The 4 lint errors are on the reused cards 師
  (いくさ), 観 (み.る, しめ.す) and 負 (ま.かす): metadata readings without a
  Readings row, older than the batch, which only adds one link line to each.
- **Confirmation evidence.** The gate results come from the author's runs
  included in the packets (`checks/`), not from reviewer reruns.
- **Checks not run.** No Android JVM test, Kotlin reading cross-check (no
  JDK), device or phone check was run. Phone acceptance is outstanding, not
  inferred.
- **Closure storage.** Confirmation packets are deduplicated by content
  (`sameAs` in `confirm-packet/provenance.json`); large files are gzipped and
  the `c3gpt` manifest blobs and trees are rebuilt from Git. A check of the 386
  stored, referenced or rebuilt confirmation-packet files (snapshot copies
  excluded; 10 rebuilt with `git cat-file`) against each packet manifest found
  0 errors. The initial packet was not checked this way; its stored text files
  are LF copies (see "This folder"). Snapshot files are Git blobs; rubric,
  repository-document and title files are recorded by hash only.
- **Superseded material.** No published commit is rewritten, and no reviewed
  commit was amended. Every run's final report is kept.

## Validation and accounting

At `ef00345d` (c3-gpt packet checks, `confirm-packet/c3gpt/checks/`):
validation 0 errors; 439 unit tests pass; manifest rebuild no diff (9,813
files, version `cdd61116919da088`, SHA-256
`d98bb0fba411ba8e69fae13b043a5271b4b804441175049334985996139a15c7`); budget
9,820 files, 9,836 entries, 56,811,680 retained, 57,247,752 inflated,
36,498,286 local-ZIP and 5,893,602 listening-media bytes (limits: 62 MiB
retained, 80 MiB inflated, 42 MiB compressed, 20 MiB listening media, 18,000
entries); vocabulary 3201/3539, exit 0; batch audit pass (10 kanji, 10 new
words, 10 changed reused articles, 10 reciprocal pairs, 30 reading
dispositions, 87 dictionary families); `diff --check` clean; lint 4 errors,
all on the reused cards 師, 観 and 負 (see "Limits"), and 59 warnings, all on
pre-existing reused files, none on the ten new cards or articles; quiz safety
10 cards, 0 errors, 0 warnings, every reading question taking 3/3 wrong
options from curated distractors, while 11 existing cards fill one slot from
the fallback, as before; reading exposure 0 production, 0 padded and 0
one-holder hits, 4 latent collisions; reading options 2 problems, exit 1 (see
"Limits"). Rerun on the closure commit, the checks above give the same
results. There, `git diff --check` from the base flags only trailing spaces
inside captured patches, evidence and verbatim reports in this folder, which
keep their recorded bytes (as in B156 and B157); outside this folder it is
clean. CI does not run `diff --check`.

After publication, delivery becomes **608/1,228**, with **620 remaining**.
Until then it stays at 598 published, plus these 10 review-closed cards.

Left for a later pass, outside this batch: the lint errors on the reused
cards 師, 観 and 負; the two reading-options fallback problems and four latent
collisions above; and the declined optional points (返却's combination line,
隠す/隠れる on 匿名, the repeated distractor sentences, splitting
`偏見.md:28`, the "metadata" wording, 傍系, the 意見 exclusion and 偽's
distractor set).
