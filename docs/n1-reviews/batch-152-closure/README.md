# Batch 152: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. The reviewed snapshot was merged with the current `origin/main`
without changing any batch file (see "Integration with current main").
Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **趣 跳 踏 躍 較 載 輝 輩 迫 逸 遂 遣 避 郡 郷**
  (source rows 1056, 1058, 1060, 1061, 1064, 1065, 1067, 1068, 1074, 1081,
  1082, 1085, 1093, 1102, 1104).
- Published base: `d59c45576d5438036e317dfbbc3c353ea4fc74a6` (the B151 receipt).
- Blind-review freeze: `cdd8fd016161d54a3d21cbf46450a6219f5bbedb`.
- Fix commit: `b81299f38d9d5184b94f7c05e6355ca7de085466`, the reviewed
  snapshot. It changes eight of the fifteen cards (跳 踏 載 輝 迫 遂 遣 避) and
  the derived `manifest.json`. 趣 躍 較 輩 逸 郡 郷, the three existing cards
  with remark edits, the fifteen stroke files and the twenty word articles are
  unchanged from the freeze.
- Integration merge: `197e91d860b7f4ea01046e7d77995a62bea3955c` (parents
  `b81299f3` and `origin/main` `e9ca5450`).
- After the freeze, only `quiz_exclusions` changed in front matter: seven
  cards gained entries and none lost any. No title, tag, distractor list,
  metadata reading, quizzed reading or stroke file changed.

The batch adds fifteen cards and stroke files. Twenty existing word articles
each gain one link to a new card (趣味, 跳ねる, 踏む, 踏切, 活躍, 比較, 比較的,
載る, 輝く, 先輩, 後輩, 迫る, 逸れる, 遂に, 仮名遣い, 小遣い, 言葉遣い, 避ける,
郡 and 故郷), and no other line of them changes. No word article is added.
Three existing kanji cards change in their remarks, four edits in all: 仮's
remark now links 遣 in 仮名遣い, 故's links 郷 in 故郷, and 響 links 郷 in its
mnemonic and drops the sentence saying that 郷 had no card here.
`n1_linkplan.py verify --remarks` checks the article links, and the author's
`kanji_remarks.py` checks that each existing card changes only by its declared
remarks.

Before the freeze, the author checked the quoted glosses and Japanese phrases
against their sources and every mnemonic against its KanjiVG tree, and ran the
author's claim audits (quoted glosses, KANJIDIC2 claims and verbatim
quotations). The first check run found three attested readings that a Starter
practice session borrowing one holder card could offer as wrong reading
options: 迫 せる (by 競), 逸 はしる (by 走) and 逸 すぐれる (by 優). 迫's
distractors 譲 戻 離 therefore became the Starter cards 出 入 休, and 逸's 戻 従
求 became 会 供 道, so that their curated options fill every wrong reading slot
in the N1, All and Starter pools. 載 also excludes the Starter card 書, and 輩
excludes 人. A scan of all 105 pairs of new cards, comparing KANJIDIC2 meanings
with titles, added 避 to 逸's exclusions (KANJIDIC2 lists “evade” for both); it
came after a first freeze commit, `738b257f`, which was amended to `cdd8fd01`
before any review. Six JMdict entry ids were added to Metadata lines, and 迫
gained the JMdict gloss of 追い詰める.

## Review execution

Reviewers of two model families, Claude and GPT, worked independently. All four
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's report (`RESPONSE.md`), the list of changes
(`CHANGES.md`), the revised cards and the exact diff, and was allowed to read
the original packet and its own family's initial report, and never the other
family's report. Models and times come from the runtime session records, not
from the reports.

| Run | Model | Snapshot | Window, 2026-11-20 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `cdd8fd01` | 20:22:36-20:32:44 | 70 | 71 | 2 | CLEAN on all four facets; seven optional suggestions (O1-O7) |
| initial-gpt | gpt-6.1-sol | `cdd8fd01` | 20:33:48-20:50:33 | 66 | 65 | 1 | NEEDS FIX (G1, G2); one link target unverified (L1) |
| confirm-claude | claude-opus-5.5 | `b81299f3` | 21:17:39-21:21:38 | 37 | 36 | 1 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `b81299f3` | 21:22:33-21:30:55 | 60 | 59 | 1 | CONFIRMED |

Both families confirmed the same final commit `b81299f3`, which was written
(21:02:26 UTC) before either confirmation started. `confirm-packet/` holds the
two packets (`c1claude`, `c1gpt`; shared files are stored once in `common/`).
`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes the files
with the packets. Raw session logs stay local because they may hold private
context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| G1: 踏 and 遂 lack direct “carry out” exclusions: 踏/遂, 踏/執, 踏/施, 遂/執, 遂/施 and 遂/履 (執 “take hold; carry out; cling”, 施 “carry out; give; alms”, 履 “footwear; put on shoes; carry out”) | GPT | Changed in b81299f3: 踏 excludes 執 施 遂, citing Kanjipedia's ふみ行う, KANJIDIC2's “carry through” and JMdict 踏む sense 4 “to complete”; 遂 excludes 執 施 履, citing JMdict 遂げる “to accomplish; to achieve; to carry out” (entry 1372620). Each pair is declared once, on the new card. Resolved |
| G2: 載 lacks a 運 (“carry; luck”) exclusion, though JMdict 1600270 sense 3 includes “to carry” | GPT | Changed in b81299f3: 運 joins 載's 積/荷 bullet, whose evidence already documents the carrying sense. Resolved |
| L1: 載, 輩 and 遣 link `../articles/compound-sound-changes.md`, which the packet did not include | GPT | Verified, no card change: the article is tracked at both snapshots with the same blob `6d5e1f06`, and both confirmation packets supply it. Resolved |
| O1: mention 迫力 on 迫 | Claude | Not applied: it would add a new sourced claim to a revision scoped to the quiz-exclusion fixes. Accepted in the confirmation |
| O2: exclude 押 on 迫 | Claude | Applied: JMdict 押す sense 5 “to push (someone for something); to press; to put pressure on (someone)” (entry 1180470), close to 迫る sense 2. Resolved |
| O3: exclusion candidates 避/脱, 輝/艶, 跳/弾 and 輝/映 | Claude | Applied for 脱 on 避 (Kanjipedia のがれる, KANJIDIC2 脱 “escape from”, JMdict 脱税 “tax evasion”), 艶 on 輝 (JMdict 艶 “gloss; luster; lustre; shine; sheen; polish”) and 弾 on 跳 (JMdict 弾む “to spring; to bound; to bounce”); 華 added on 輝 (KANJIDIC2 lists “shine” and “luster” for 華). 映 not excluded: its title “reflect, project” names no sense of 輝, and the existing shine cards 光 照 華 艶 do not exclude it either. Accepted in the confirmation |
| O4: the Starter distractors of 迫 (出 入 休) and 逸 (会 供 道) are easy | Claude | Not changed: both sets are defensibly wrong, and as Starter cards they fill every wrong reading slot, which keeps 迫 せる and 逸 はしる, すぐれる from being drawn. Accepted in the confirmation |
| O5: 人形遣い, 遣's -つか.い example, is usually read にんぎょうづかい | Claude | Applied: the row gives 蛇遣い へびつかい “snake charmer” (JMdict 1753470, which also spells it 蛇使い and has only the unvoiced reading); JMdict 1367140 gives its priority tags to the voiced にんぎょうづかい. Resolved |
| O6: the Digital Daijisen name readings are missing from the `--extra` lists | Claude | Checked, no card change: an exposure run adding 載 こと, 迫 とお, 郷 あき and のり, 輩 とも, 較 あつ, とお and なお, and 趣 とし found no production, padded-session or new one-holder hit. Resolved |
| O7: 郷/区 may over-exclude | Claude | Not changed: KANJIDIC2 lists “district” for 郷 and Kanjipedia gives an old administrative division, so 区 “ward; district” is a defensible answer for 郷. Accepted in the confirmation |
| GO1: shorten or separate the source-audit material in Notes, translate source quotations, gloss “ateji” | GPT | Not applied, for consistency with the existing N1 cards, whose Notes use the same sourced-exclusion format and use “ateji” without a gloss (for example 供); a glossary pass belongs to separate work. Accepted in the confirmation |
| GO2: 迫's distractor sentence says “going out moves away” | GPT | Not changed: the sentence contrasts the typical motion of each word, and its conclusion that none means to press or approach is sound. Accepted in the confirmation |
| Confirmation optional: 踏/遂, 踏/執 and 踏/施 are weak but harmless over-exclusions; 蛇遣い is the less common spelling | Claude | Not applied; recorded here. The row already names the spelling 蛇使い |
| GPT confirmation | GPT | No finding and no new optional item |

## Integration with current main

After the reviewed snapshot, `origin/main` moved from the base `d59c4557` to
`e9ca545032292083325e733d9dcd43dbf186ec35`: one signed owner commit. It adds
two original N5 reading packages (`reading/community-garden-n5.json` and
`reading/letter-for-grandmother-n5.json`) and their manifest entries, adds an
"N5 follow-up drafts" section to `docs/reading-n5.md`, and rewords one line of
the Reading section of `docs/content-format.md` to call `reading-n5.md` the N5
authoring record. It changes no kanji card, word article or stroke file, and
nothing in the rules for kanji cards, word articles or quizzes. Following step
4 of the issue #60 contract, the merge `197e91d8` (parents `b81299f3` and
`e9ca5450`) is a non-rewriting merge. `manifest.json` was the only conflict
and was regenerated with `tools/build_manifest.py` (version
`9326f58c43f62815`).

[`integration/merge-proof.json`](integration/merge-proof.json) is produced by
[`integration/merge_proof.py`](integration/merge_proof.py), the B149 script
with the B152 base, snapshot and kanji:
`python -X utf8 merge_proof.py <repo> 197e91d8 merge-proof.json`.

- Of the 48,490 paths compared, every one except the derived `manifest.json`
  equals one parent byte-for-byte.
- The 53 batch runtime files (15 cards, 15 stroke files, 20 word articles and
  the 3 existing cards with remark edits) equal `b81299f3`, and none was
  changed by main.
- The regenerated manifest lists all 53 files.
- None of the 249 paths the batch files link to was changed by main.
- Of the four non-derived files main changed, one mentions a batch kanji:
  `docs/content-format.md` (遣, in 遣う on line 1119, an existing grammar-drill
  note on accepted spellings). No line that main added mentions a batch kanji
  or word.

The strict form of the mention check ("no mention anywhere in a changed
file") fails on this older line, and the proof records it as
`strictPass: false`. `pass: true` applies the narrower rule stated in the
script: a mention passes when it is not on a line main added. Both results
are in the JSON.

The contract requires a bounded independent review only for changed teaching or
an overlapping substantive conflict. Neither applies here: the reviewed
teaching is byte-identical, main's changes touch no batch file, and the only
conflict is the derived manifest. No integration review was held, as for the
earlier non-overlapping merges in B023, B054, B055, B141 and B149.

Gates on `197e91d8`: 439 host tests pass; validation 0 errors; lint 0 errors
and the same 7 warnings; manifest rebuild unchanged (SHA-256
`4E07FC668DFFBC45D94FA45EBF583580950DBBFF5856682AFEE161D32E64D1C6`, 9,641
files); budget 9,664 entries, 56,189,536 retained, 56,619,100 inflated and
36,153,523 local-ZIP bytes; vocabulary 3201/3539. Every batch audit (lint,
quiz safety, reading exposure, reading options, link plan, kanji remarks,
Metadata scan and okurigana scan) is identical to its run at `b81299f3` apart
from the command line.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The
  `initial-gpt` run and both confirmations had at most one tool call in
  flight. The `initial-claude` run twice issued two read-only `view` calls at
  once, inside the packet: at 20:23:08 (`repo/docs/content-format.md` lines
  86-155 with `snapshot/kanji/趣.md`) and at 20:26:36 (`郡.md` with `郷.md`).
  Its report discloses the second pair and says its earlier turns had been
  compacted out of its context. It also wrote a temporary helper script,
  `reports-152/_jm.py`, that only parsed the packet's JMdict extract, and
  deleted it before writing the report, as the report discloses; the audit's
  two write-like shell commands and two paths outside the packet are that
  script and its folder. The `initial-gpt` audit flags one write outside the
  report path. This is a false positive: the report was written through a
  relative path that resolves to `reports-152/initial-gpt.md`.
- **Prompts.** Every prompt was saved to a file before use; each file matches
  the message its agent received, apart from line endings and the final
  newline.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists as unread some files that the reports
  say were read. In the `initial-claude` audit these are the 23 diffs (every
  changed line and hunk header), the 15 stroke files (parsed by script and
  compared with the KanjiVG paths), the 15 Digital Daijisen extracts (read in
  full or searched) and lines 25-43 of 響.md. That run judged 仮.md, 故.md and
  the twenty word articles only through their diffs and hunk context, and
  searched the app code in part. In the `initial-gpt` audit they are all
  fifteen cards, the 23 diffs and the 15 Daijisen extracts, which its report
  says it read in full, and the stroke files and word articles, which it
  loaded in Python and reviewed through the diffs. The confirmations read the
  eight changed cards in full and the change itself, and could read the
  original packet and their own family's initial report. Neither reopened the
  seven unchanged cards (趣 躍 較 輩 逸 郡 郷) in full: `confirm-gpt` re-read
  their front matter and distractor explanations, and `confirm-claude` relied
  on its initial review and on `CHANGES.md` and `fix.patch` for the fact that
  they are unchanged. `confirm-claude` read `fix.patch` by hunk headers and
  removed lines, with the full revised cards.
- **Dictionary text.** Several judgments rest partly on live reads of
  Kanjipedia, Digital Daijisen, Jisho and kanjiapi.dev pages, not on pinned
  copies in the packet. `confirm-claude`'s Kanjipedia lookup of 映 returned
  HTTP 500 and verified nothing, and it did not check the Daijisen entry for
  へびつかい; `confirm-gpt` did, on Weblio. `confirm-gpt`'s fetch of the L1
  article from GitHub at `b81299f3` returned 404 because that commit was not
  yet pushed; it checked the supplied copy's blob hash and the public copy on
  `main` instead.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `b81299f3` they report 0
  production, 0 padded-session and 0 one-holder hits for an ordinary reading,
  and twenty latent collisions: attested readings that other cards offer but
  no audited pool can draw. Two KANJIDIC2 name-only readings can be offered
  only in a Starter practice session that also borrows a holder card: 載 のり
  (by 則, 法 or 準) and 輝 ひかる (by 光). `reading_options.py`, which does not
  model curated options, reports one problem, 迫 せる offered by 競; it cannot
  be drawn, because 迫's curated Starter options 出 入 休 fill every wrong slot
  in every audited pool. The meaning-quiz check reports 0 errors and 0
  warnings; the curated distractors still fill every wrong meaning slot of the
  seven cards whose exclusions grew. Sampled seeds are not exhaustive, and the
  claim covers the documented shipped pool configurations only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. Six cards quiz only their on reading (趣 シュ,
  躍 ヤク, 較 カク, 輩 ハイ, 郡 グン, 郷 キョウ) and nine only their kun reading
  (跳 は.ねる, 踏 ふ.む, 載 の.る, 輝 かがや.く, 迫 せま.る, 逸 そ.れる, 遂 つい.に,
  遣 -づか.い, 避 さ.ける). 逸 そ.れる and 遂 つい.に are outside the official
  Joyo table, as Kanjipedia marks and both cards say; they are quizzed because
  the declaring articles 逸れる and 遂に use them.
- **One-way exclusions.** Four pairs of new cards declare their exclusion on
  one card only (躍 lists 跳, 郷 lists 郡, 逸 lists 避, 踏 lists 遂); the app
  applies an exclusion in both directions.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as such on the cards.
- **Metadata ids.** Every word named on the cards as a whole run has its JMdict
  entry id on the card's Metadata line; 71 shorter words that occur only
  inside longer quoted phrases and headwords are not listed.
- **Lint warnings.** Seven warnings, none on the new cards or the three
  existing cards with a remark edit, are older than the batch and out of
  scope: all are on existing word articles whose Dictionary line cites no
  JMdict entry id (比較的, 踏切 and 逸れる, which gain a link here, and 平仮名,
  振り仮名, 響き and 響く, which declare 仮 or 響).
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The first freeze
  `738b257f` was amended before any review and never pushed; the freeze
  `cdd8fd01` and the fix commit remain in the history, and every report is
  kept.

## Validation and accounting

At the reviewed snapshot `b81299f3`: 439 host tests pass; validation 0 errors;
lint 0 errors and 7 warnings (above); quiz safety 0/0; reading options 1
problem that cannot be drawn (above); manifest rebuild unchanged (version
`331f03fabd26f6dc`, 9,639 files, SHA-256
`5DA41C1D0A7A5A4B8C97C551F9B011A007765188007AF5BFA7007A38C76C3776`); budget
9,662 entries, 56,189,318 retained, 56,548,614 inflated and 36,139,911
local-ZIP bytes; vocabulary 3201/3539; link plan 20 links, 0 problems; kanji
remarks 15 of 15 present, 3 existing cards changed only by their 4 declared
remark edits. Gates at the merge are listed above.

After publication, delivery becomes **542/1,228**, with **686 remaining**.
Until the receipt it stays 527/1,228.
