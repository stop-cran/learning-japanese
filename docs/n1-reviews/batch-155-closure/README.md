# Batch 155: textual-review closure

The six cards are textually review-closed. Both families' last confirmations
of the reviewed snapshot are **CONFIRMED**, with no remaining finding.
`origin/main` moved past the published base, so publication goes through a
signed integration merge (see "Integration with current main"). Publication
is **pending** at this closure commit; the later receipt establishes the
remote commit, CI and served ZIP. No JVM, native, device or phone acceptance
is implied.

## Snapshot and scope

- Members: **卑 汰 沙 沢 胡 鼓** (source rows 127, 599, 602, 604, 894, 1232).
- Published base: `6cbc14fe25c05447674a90c6c3173060d5b4c621`, the owner's
  commit after the B154 receipt.
- Blind-review freeze: `97c49eb27abbd2961ed93de7c67ece0fa53b5c8a`.
- Fix commit: `25609582e7d44eed71b10b3fe8ab7e9a5a3931e9`, the reviewed
  snapshot. It changes all six cards (line 23 and Notes, and two exclusion
  lists) and the derived `manifest.json`. The six stroke files and the six
  word articles are unchanged from the freeze.
- Merge: `37c71f81120d29f675465d587dc8572e4a6935d4`, a signed merge of
  `origin/main` at `2cb17a36` after review (see "Integration with current
  main").
- After the freeze, only two `quiz_exclusions` lists changed in front matter:
  卑 lost 底, and 沙 lost 漠. No title, tag, distractor list, metadata
  reading, quizzed reading or stroke file changed.

The batch adds six cards and stroke files. Six existing word articles each
change in one line, which gains links to the new cards: 卑怯, 太鼓, 胡椒 and
贅沢 link one kanji each, 御無沙汰 links 沙 and 汰 separately, and 無沙汰
links 沙汰 as 沙 and 汰, eight links in all. The same line of 無沙汰 also
changes its remark: “None of these written characters has a card yet”
becomes “無 does not have a card yet”. No other line of these articles
changes, no word article is added and no existing kanji card changes.
`n1_linkplan.py verify --remarks` checks the links and the one declared
remark, and the author's `kanji_remarks.py` finds six new cards and no
changed existing card.

Selection follows the issue #60 rule from batch 137: the remaining rows whose
existing declaring word articles use one of the kanji's KANJIDIC2 readings.
At the base, `coverage.py` found 12 remaining rows with a declaring article:
鼓 (太鼓) aligned, and 11 rows marked as not aligned. Five of those 11 were
misclassified, because the lean alignment had no readings for 怯, 贅, 椒 and
無, which have no cards and are outside the N1 set. With KANJIDIC2's 怯
キョウ, 贅 ゼイ, 椒 ショウ and 無 ム/ブ, the articles 卑怯 ひきょう, 贅沢
ぜいたく, 胡椒 こしょう, 無沙汰 ぶさた and 御無沙汰 ごぶさた use 卑 ヒ, 沢 タク,
胡 コ, 沙 サ and 汰 タ. The pinned JMdict marks none of these spellings as
ateji and none of the readings as gikun. This corrects the batch 149 record,
whose selection reason says that 胡椒 uses none of 胡's KANJIDIC2 readings;
こしょう uses コ. The batch 149 ledger is left unchanged, and the batch 154
comment on issue #60 already disclosed the misclassification. The other six
rows marked as not aligned (伯 戯 撲 皇 眼 邪) are not part of this batch.

Before the freeze, the author checked the quoted glosses and Japanese phrases
against their sources and every mnemonic against its KanjiVG tree, and ran
the author's claim audits. Design changes before drafting: 汰 does not
exclude 沙, because the sibling pair is declared on 沙, the later source row,
and 汰 carries the sibling sentence instead; a sweep of title keywords added
近 and 軽 to 卑's exclusions and 激 and 扇 to 鼓's; and 虚 was dropped from
胡's, because no verbatim source ties 胡's sense でたらめ to 虚 (KANJIDIC2
glosses 虚 “untruth”, JMdict でたらめ “nonsense”). The design check reports
no issue and ten accepted warnings, all for 汰: its title “sift; weed out”
shares the English word “out” with the titles of 出, 吐, 呼, 執, 履, 敷, 施,
滅, 眺 and 裁, an English homograph only. The drafts dropped 卑しさ, which
has no JMdict entry, and the author's read restored the ▽ mark (a reading
outside the official table) in the quotation of Digital Daijisen's
すな【砂／▽沙】, which G3 later moved to `exclusion-proofs.md`. The reading
audits also take, from an okurigana scan of JMdict headwords, the readings 卑
ひ.わい, 汰 ゆ.る and 鼓 こ.す and こ.する; none of them collides with a reading
another card offers.

## Review execution

Reviewers of two model families, Claude and GPT, worked independently. All four
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's report (`RESPONSE.md`), the list of changes
(`CHANGES.md`), the revised cards and the exact diff, and was allowed to read
the original packet and its own family's initial report, and never the other
family's report. The statement to Claude also described the changes made for
GPT's findings, which `confirm-claude` judged as a reviewer of the revised
cards. Models and times come from the runtime session records, not from the
reports.

| Run | Model | Snapshot | Window, 2026-11-21 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `97c49eb2` | 08:06:33-08:13:29 | 43 | 42 | 1 | CLEAN on all four facets: no finding; four optional suggestions (O1-O4) |
| initial-gpt | gpt-6.1-sol | `97c49eb2` | 08:14:43-08:26:50 | 64 | 63 | 1 | NEEDS FIX (consistency and quiz safety; comprehensibility): three minor findings (G1-G3); no optional suggestion |
| confirm-claude | claude-opus-5.5 | `25609582` | 08:58:59-09:04:02 | 33 | 33 | 2 | CONFIRMED; four optional suggestions (CO1-CO4) |
| confirm-gpt | gpt-6.1-sol | `25609582` | 09:04:29-09:09:43 | 40 | 39 | 1 | CONFIRMED |

Both families confirmed the same final commit `25609582`, which was written
(08:40:36 UTC) before either confirmation started. `confirm-packet/` holds the
two packets (`c1claude`, `c1gpt`; shared files are stored once in `common/`).
`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes the files
with the packets. Raw session logs stay local because they may hold private
context.

## Findings and dispositions

The Claude confirmation numbered its optional points 1 to 4; `CO1` to `CO4`
follow that order.

| Item | Raised by | Disposition |
|---|---|---|
| G1: 卑 (“lowly; despicable”) excludes 底 (“bottom; base”) only because both glosses contain the English word “base”, although 卑 is low in a moral sense and 底 is a physical bottom | GPT | Changed in 25609582: 底 is removed (`卑.md:14`; now eleven cards, `卑.md:45`). The removed bullet and the contrast between moral baseness and a physical base are kept in `confirm-packet/common/evidence/exclusion-proofs.md` (“Exclusions removed by the fix”), not on the card, whose Notes G3 shortened. 底 declares no exclusion of 卑, so the pair is no longer excluded anywhere. Resolved |
| G2: 沙 excludes 漠 (“desert; vague”) by transferring the meaning of the whole word 沙漠, “desert”, onto 沙 | GPT | Changed in 25609582: 漠 is removed (`沙.md:14`; now nine cards, `沙.md:49`). A new Notes line keeps the spelling: JMdict lists 沙漠 as a rarely used spelling of 砂漠 さばく, “desert”, Digital Daijisen gives 沙漠 as an example of 沙 meaning sand, and sand is a material while a desert is a region, with a link to the 漠 card (`沙.md:47`; JMdict 1593800 stays on the Metadata line). `confirm-claude` also accepted this change. Resolved |
| G3: every card embeds an editorial proof dossier: a dictionary-comparison paragraph at line 23 and Notes that prove each exclusion with source names, entry ids and Japanese definition fragments, too dense for the N5-N4 reader on a phone | GPT | Changed in 25609582 on all six cards: line 23 is plain English with kana, and the Notes give one short reason per excluded group, the layout adopted for batch 149 (its G4). The replaced text is kept verbatim in `exclusion-proofs.md`. The six cards are 11,466 bytes shorter in total, and their Notes sections shrink from 2,365 to 1,328 whitespace-separated words. Sixteen Metadata ids whose words the cards no longer name were removed (see Limits). `confirm-claude` also accepted this change. Resolved |
| O1: 胡's distractors 甘, 柔 and 静 are defensibly wrong but teach little; 古 or 貴 would be nearer | Claude | Not changed: a new distractor would be an unreviewed quiz change in a round limited to the fixes. Deferred: recorded for a later pass. Accepted in the confirmation |
| O2: the 卑/底 exclusion rests only on the English word “base” | Claude | Covered by G1. Resolved |
| O3: 醜 (“ugly; unsightly”) is a borderline neighbour of 卑, noted for awareness only | Claude | No change, as the note asked. Accepted in the confirmation |
| O4: `words/御無沙汰.md:26` says that some of the characters do not yet have cards; now only 無 lacks one | Claude | Not changed: the line is outside the batch's diff and still true. Deferred: recorded for a later pass. Accepted in the confirmation |
| CO1: `沙.md:23` cites 沙汰 for the sense of sifting but never gives its modern meaning, “affair; matter” | Claude | Deferred: recorded for a later pass. The 汰 card gives the meaning (`汰.md:44`) |
| CO2: `汰.md:44` says that 沙汰 is “first glossed” as “affair; state; incident; issue; matter” without naming JMdict, now that the entry id is on the Metadata line only | Claude | Deferred: recorded for a later pass. JMdict 1291480 is on 汰's Metadata line |
| CO3: `鼓.md:46` quotes 鼓動's gloss for the 脈 exclusion without making the link to “pulse” explicit | Claude | Deferred: recorded for a later pass |
| CO4: `卑.md:49` could give Kanjipedia's example 卑見 (“my humble opinion”) for the humble sense | Claude | Deferred: recorded for a later pass |
| GPT confirmation | GPT | No finding and no optional item |

## Integration with current main

`origin/main` moved past the published base before publication. The owner's
signed commit `2cb17a36` ("Improve N5 reading support and questions",
2026-11-21 07:14 UTC) changed `docs/reading-n5.md`,
`reading/community-garden-n5.json`, `reading/letter-for-grandmother-n5.json`
and `manifest.json` only. The signed merge `37c71f81` has the reviewed
snapshot `25609582` as its first parent and `2cb17a36` as its second. The
only conflict was the derived `manifest.json`, which was regenerated with
`tools/build_manifest.py`. Relative to `25609582` the merge changes only
those four files.

`integration/merge_proof.py` and `integration/merge-proof.json` show
mechanically that every non-derived path equals one parent byte for byte
(48,914 paths compared, none unmatched), that none of the 18 batch runtime
paths or 96 link targets was changed by main, that no main-changed
non-derived file mentions a batch kanji or word, and that the manifest lists
every batch file. The merge changed no reviewed batch text and resolved no
substantive conflict, so, as for batch 144, no integration review was needed
under the issue #60 contract. The gates were rerun on `37c71f81`: the
quiz-safety, lint, link-plan, vocabulary and validation outputs are identical
to those at `25609582`, and the reading-exposure, reading-options, meta-scan,
kanji-remarks and okurigana-scan outputs differ only in their command lines.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The two
  initial runs and `confirm-gpt` had at most one tool call in flight.
  `confirm-claude` once issued two read-only calls at once, at 09:00:29 UTC:
  two `view` calls of its packet's `evidence/exclusion-proofs.md`, for lines
  1-50 and 50-140. Its report says that every assistant response contained
  exactly one tool call, which is inaccurate on this point. The final
  message of `initial-claude` is not identical to its saved report but
  contains it (the audit's similarity is 0.98); `reports/` keeps the saved
  report. The other three final messages equal their reports. The
  `initial-gpt` audit flags one recursive shell command over the packet
  folder and counts it as a corpus scan. This is a false positive: the
  audit's pattern matched `**` in Python exponentiation and in a quoted
  Markdown string, in a script that compared the stroke files with their
  KanjiVG SVGs and opened named files only. The `confirm-gpt` audit flags one
  path outside the allowed folders: the parent `review-packets` folder, which
  its shell commands used as a base path. This is also a false positive:
  every path built on it lies in the confirmation packet, the original packet
  or its family's initial report.
- **Prompts.** Every prompt was saved to a file before use. The two initial
  prompt files equal the messages their agents received, byte for byte. The
  two confirmation prompt files were saved with CRLF line ends; their agents
  received the same text with LF line ends.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists as unread some files that the reports
  say were read. The `initial-claude` audit lists the stroke files, the word
  articles and the six diffs as unread; its report says that it read the
  cards, the word articles and the diffs in full and parsed every stroke
  file. It relied on `kanjivg-components.txt` without opening
  `kanjivg-svgs.txt`, did not open `quiz-safety.txt` or the app code, read
  the XML, digest and TSV evidence by targeted extraction, read
  `reading-options.txt` to line 60 and searched `reading-exposure.txt`.
  `initial-gpt` read the cards in full and compared all 52 strokes (832
  coordinate pairs) with their KanjiVG SVGs, to within 0.071 units; some
  command output exceeded the tool's cap, and it did not open the files the
  tool saved it to. `confirm-claude` read the six revised cards,
  `exclusion-proofs.md`, `QuizBuilder.kt`, `KanjiReadings.kt`,
  `KanjiMeaningMetadata.kt`, `quiz-safety.txt`, `reading-options.txt`,
  `link-targets.tsv` and `changed-lines.txt` in full, `fix.patch` to line 70
  and every hunk header, and `reading-exposure.txt`, the batch 149 README and
  24 JMdict entries in part. Its report says it read the patch in full only
  for 卑 and compared the other five cards with `exclusion-proofs.md`. It did
  not open `Words.kt`, `meta-scan.txt`, `evidence/README.md` or the lint,
  test, validation, manifest, budget, vocabulary, link-plan and kanji-remarks
  outputs, and took their results from `CHANGES.md`. The `confirm-gpt` audit
  lists the six revised cards as unread; its report says that it read them
  in full, rebuilt the revised files from `fix.patch` with matching hashes,
  read `QuizBuilder.kt` and `KanjiMeaningMetadata.kt` in full,
  `KanjiReadings.kt` to line 210 and `Words.kt` at lines 216-240, checked all
  45 cited JMdict entries, and read 底 and 漠 in full and the front matter of
  the 18 distractor cards from the original packet.
- **Dictionary text.** Several judgments rest partly on live reads of
  Kanjipedia, Digital Daijisen (Weblio) and Jisho pages, not on pinned copies
  in the packet. `initial-claude` fetched only Jisho's page for 胡 and checked
  the other quotations against the packet's evidence. `initial-gpt` read
  Kanjipedia for the six kanji, Weblio for them and for 底, 漠, 慢 and 採,
  Jisho for 卑怯 and the 沢 kanji page, and 22 entries from Jisho's API; its
  kanjiapi.dev requests returned 403. `confirm-claude` fetched the Weblio page
  for 沙, and `confirm-gpt` fetched Kanjipedia for the six kanji. Both
  confirmations checked the Joyo table only in the packet's extract, not the
  PDF.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `25609582` and at the merge
  they report 0 production, 0 padded-session and 0 one-holder hits, also for
  KANJIDIC2 name-only readings, and one latent collision: 沢 さ, a KANJIDIC2
  name reading that 作, 再, 左, 差, 査, 沙, 砂 and 茶 offer, which no audited
  pool can draw. `reading_options.py`, which does not model curated options,
  reports no problem. The meaning-quiz check reports 0 errors and 0 warnings.
  The reading questions of 卑, 汰, 沙 and 胡 take all three wrong options
  from their curated cards. 沢's タク question takes two (岩 and 丘; 霜 has
  no on reading) and 鼓's コ question one (筆; 笛 and 琴 have no on reading);
  the other options come from other cards. Sampled seeds are not exhaustive,
  and the claim covers the documented shipped pool configurations only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. All six cards quiz only their on reading (卑
  ヒ, 汰 タ, 沙 サ, 沢 タク, 胡 コ, 鼓 コ). Five of them are in the official
  Joyo table. 胡 is not a Joyo kanji: KANJIDIC2 gives it grade 9, Digital
  Daijisen labels it ［人名用漢字］, and its card has no Joyo link.
- **Exclusions.** The six cards declare 64 exclusions. The only pair of new
  cards is the sibling pair 汰/沙, declared on 沙, the later source row; the
  app applies an exclusion in both directions. No existing card lists any of
  the six kanji in its `quiz_exclusions` or `distractors`; `confirm-claude`
  took this from `CHANGES.md`, and the author rechecked it on the merge.
- **Source-only readings.** 汰 タイ, おご.る, にご.る and よな.げる, 沙
  よなげる, 沢 うるお.い, うるお.す and つや, and 胡 なんぞ have no checked
  JMdict example and are labelled “source-only here” on the cards. Kanjipedia
  also lists 卑 ひくい and 沙 みぎわ outside the table; neither is a KANJIDIC2
  reading, so the cards explain them in Notes and give them no table row.
- **Metadata ids.** Every word named on the cards as a whole run outside a
  quotation has its JMdict entry id on the card's Metadata line. Not listed
  are 人名用漢字, which occurs only inside Digital Daijisen's bracketed label
  on 胡, and eight shorter words that occur only inside longer phrases: 梵語
  and 音訳 in 梵語の音訳字 on 沙; 臭い in 胡散臭い, 人名 and 漢字 in 人名用漢字
  and 民族 in 異民族 on 胡; and 異体 and 異体字 in the quotation 「皷」は異体字
  on 鼓. The fix removed sixteen ids whose words the revised cards no longer
  name: 卑 1434180, 2080200, 1178940, 1151260 and 1242130; 汰 1415960; 沢
  1390020, 2843433 and 1224010; 胡 1203620, 2740960, 1267590 and 1610940; and
  鼓 1253760, 1609000 and 1390750.
- **Lint warnings.** Two warnings, on the word articles 卑怯 and 太鼓, which
  gain links here, are older than the batch and out of scope: their
  Dictionary lines are wrapped, so the first line cites no JMdict entry id.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten, and neither the
  freeze nor the fix commit was amended. Both confirmation packets were
  rebuilt once before the runs, after `CHANGES.md` was corrected to list 卑's
  changed lines as 14, 23, 42, 45-52 and 56; the earlier build was never
  given to a reviewer. The freeze and the fix commit remain in the history,
  and every report is kept. The batch 149 record is not rewritten; this
  closure and its ledger carry the 胡 correction.

## Validation and accounting

At the merge `37c71f81`: 439 host tests pass; validation 0 errors; lint 0
errors and 2 warnings (above); quiz safety 0/0; reading options 0 problems;
manifest rebuild unchanged (version `8260f7beacd371e3`, 9,713 files, SHA-256
`A577582292890D1FF629B72429B4B0D463E6F2F58CB461100D87B7288F0131CD`); budget
9,736 entries, 56,489,356 retained, 56,920,598 inflated and 36,293,081
local-ZIP bytes; vocabulary 3201/3539; link plan 8 links and 1 declared
remark edit, 0 problems; kanji remarks 6 of 6 new cards present, no existing
card changed, 0 problems; the Metadata scan finds no whole-run gap outside a
quotation.

After publication, delivery becomes **578/1,228**, with **650 remaining**.
Until the receipt it stays 572/1,228.
