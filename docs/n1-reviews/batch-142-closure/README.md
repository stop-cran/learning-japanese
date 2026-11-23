# Batch 142: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **挙 振 挿 掌 推 描 提 揮 揺 操 故 敵 斉 斎 斜**
  (source rows 431, 432, 433, 438, 441, 444, 445, 448, 450, 463, 467, 473,
  475, 476, 479).
- Published base: `ed966c3e4ad280a7463da6e6861e73077c413b0e`.
- Blind-review freeze: `9d393a8f7bbf04114668b40f84b67a9a4b2ef7e3`.
- Fix: `3a0399bd8fcdc7258e2eed41236ccc1c0f0369f0` (the cards 描, 提, 揺, 斉
  and 斎, and the generated `manifest.json`), the reviewed snapshot. There is
  one fix and one confirmation round.

The freeze adds fifteen cards and stroke files. Twenty-four existing word
articles each gain one link to a new card, and no word article is added. The
Notes remark of the existing 仮 card that said 振 and 遣 had no cards now links
振 and names only 遣. No other existing kanji card changes. The fix changes no
front matter and no stroke file.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All four
runs ran one after the other (no two overlapped), the first time since B137
that the confirmations did too. The two initial runs reviewed the same frozen
packet (`packet/`) without seeing each other's work. Each confirmation was run
by a **fresh agent of the same model family**, not a later turn of the initial
agent. It received a new packet with the author's statement answering its
family's initial report (`RESPONSE.md`), the list of changes (`CHANGES.md`),
the revised cards and the exact diff, and was allowed to read the original
packet and its own family's initial report, and never the other family's
reports. `confirm-packet/` holds the two packets; files they share are in
`common`. The revised cards are not stored again, because they are the blobs at
`3a0399bd`. Models and times come from the runtime session records, not from the
reports.

| Run | Model | Snapshot | Window, 2026-11-19 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `9d393a8f` | 05:52:13–06:00:24 | 53 | 52 | 1 | NEEDS FIX (C1, C2, both minor) |
| initial-gpt | gpt-6.1-sol | `9d393a8f` | 06:00:34–06:19:29 | 139 | 138 | 1 | NEEDS FIX (G1 to G4, all minor) |
| confirm-claude | claude-opus-5.5 | `3a0399bd` | 06:39:00–06:43:11 | 35 | 35 | 2 | CONFIRMED (two optional notes) |
| confirm-gpt | gpt-6.1-sol | `3a0399bd` | 06:44:57–06:50:41 | 40 | 39 | 1 | CONFIRMED (no optional point) |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: the meaning-quiz distractors of 揺 and 斎 are unrelated Starter kanji | Claude, initial (minor) | Not changed. The collection convention is to pick the curated distractors for the reading question and to say so in Notes, as the published cards 脱 (脱.md:57: 飲 読 聞) and 致 (致.md:58: 話 買 学) do; 揺.md:60 and 斎.md:65 state it. Changing them would change both question types and need new reading audits. Claude accepted the decline |
| C2: 斎's summary of Daijisen さい【斎】 omitted the pen names | Claude, initial (minor) | Changed: 斎.md:34 now says the noun also follows the names of rooms and the pen names of writers and artists (Daijisen `居室の名や文人などの雅号に添えて用いる`). Claude marked it resolved |
| O1: lead with 斉行 in the サイ row of 斉 | Claude, initial (optional) | Not changed: 斉.md:40 follows the JMdict headword order of 2798990 (斎行, 斉行) and says 斉行 is also a spelling. Decline accepted |
| O2: add たなそこ for 掌 | Claude, initial (optional) | Not changed: the card says it does not list every Daijisen reading; たなそこ is not a KANJIDIC2 reading. Decline accepted |
| O3: 操's 品 and 木 distractors | Claude, initial (optional) | Not changed, as for C1: a deliberate visual lure, disclosed in Notes. Decline accepted |
| O4: let the older reading-options check count slots that curated distractors fill | Claude, initial (optional) | Not changed here: a change to the author's audit tool, not to the batch; the pool-aware reading-exposure audit stays the authoritative check for 斎 い. Decline accepted |
| G1: 提's チョウ row said ちょうちん belongs to the whole word and that no source assigns ちょう to 提 | GPT, initial (minor) | Changed: 提.md:40 now says チョウ is listed by KANJIDIC2 and, as outside the official table, by Kanjipedia, and is the reading of 提 in 提灯, which Daijisen writes ▽提▽灯 and labels 唐音 (`confirm-packet/common/evidence/weblio-chouchin.txt`; JMdict 1446650 for 唐音); 提.md:46 says no word article has 提灯 yet; 提.md:62 gains JMdict 1734790, 1734800 and 1446650. GPT marked it resolved |
| G2: 斎.md:32 said 斎宮 and 斎王 are not split between the kanji | GPT, initial (minor) | Changed: 斎.md:32 says that in 斎宮, 斎 is read いつき, the の is not written and 宮 is みや (`confirm-packet/common/evidence/weblio-saigu.txt`); no sentence claims indivisibility any more. GPT marked it resolved |
| G3: 揺's 缶-shaped part is a five-stroke shape, not 缶 | GPT, initial (minor) | Changed: 揺.md:31 says "a shape like 缶 with one stroke fewer" and 揺.md:60 says 缶 has six strokes and the bottom of the right part of 揺 is a five-stroke shape like it (`confirm-packet/common/evidence/stroke-types.txt`). GPT marked it resolved |
| G4: long single paragraphs in 斎, 斉 and 揺 | GPT, initial (minor) | Changed in part: the paragraphs are split (斎.md:32, 34, 36; 斉.md:25, 27, 29; 揺.md:25, 27 and 49, 51). The source inventories were not moved into bullets at the end of Notes. GPT marked it resolved and called the move a proposed remedy, not a required format |
| Optional 1: cite JMdict 2751570 on 描 | GPT, initial | Applied: 描.md:52 lists 2751570 (すがき, 素描). GPT marked it resolved |
| Optional 2: favour useful compounds over repeated disclaimers | GPT, initial | Not changed: guidance for future shortening. Decline accepted |
| Optional 3: prune the exclusions 挿 and 苗, 敵 and 恨 | GPT, initial | Not changed: direct exclusions, not distractors. Decline accepted |
| 提's チョウ cell quotes the JMdict 唐音 gloss, which is dense | Claude, confirmation (optional) | Deferred: wording polish, recorded for a later pass |
| `quiz-safety.txt` says 故 コ has "3/3 curated" although only two of its three curated cards can serve, since 攻 offers only こう, which the quiz skips as a long-vowel variant of the answer | Claude, confirmation (optional) | Not a card defect: a quirk of the checker's output, unchanged from the freeze; the ledger states the fact (the random fallback fills one slot) |

Claude raised both initial findings and all four optional points; GPT
independently raised the 提 account of チョウ, 斎宮 and 揺's shape, and was the
only one to raise the long paragraphs. These are contributions to this sample,
not model rankings.

## Integration with current main

`origin/main` had not moved since the base `ed966c3e` (checked with `git fetch`
at closure), so no merge and no integration review were needed.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family rather than a later turn of the initial agent (B141's rounds used the
  same agent), so it had no memory of its own earlier reading; it was handed
  its family's initial report and the original packet. The confirmations are
  independent of each other.
- **Execution.** Every run was serial. No GPT report names the exact model; the
  runtime records gpt-6.1-sol. confirm-claude's audit flags overlapping tool
  calls (maximum two in flight, one overlapping start); the report discloses
  that its first reads of `CHANGES.md` and `RESPONSE.md` were issued in one
  response. Both initial runs' audits flag one recursive PowerShell listing of
  their own packet directory (6,593 files, which includes the `repo` context
  corpus) and one read of their assignment prompt file
  (`prompts/initial-<family>.txt`), counted as a path outside the packet; the
  prompt text is part of this record. The confirmation prompts forbade
  recursive listings, and confirm-gpt's audit has no flag.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. The initial reports describe their own read scope.
  confirm-gpt viewed the five changed cards in full; confirm-claude's audit shows
  four of them read in full and one partly. The confirmation mandate
  covered the changed cards, so the prose of the ten unchanged cards and every
  word article were not re-read; confirm-gpt compared the front matter of all
  fifteen cards in Python and its report says the quiz checks were read in full.
- **Reviewers' own limits.** Claude checked C1's convention only against the
  copies of 脱 and 致 in the original packet's `repo` folder and Weblio only
  through the packet's extracts. GPT checked the practice pools only as far as
  the supplied audits model them, ran no JVM or Android build and could not
  certify the pool construction.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `3a0399bd` they report 0
  production, 0 padded-session and 0 one-holder hits and 12 latent collisions:
  振 すくう, 挿 さしはさむ and いれる, 揺 ゆ and よる, 故 え and け, 斎 い and
  ゆ, and the KANJIDIC2 name readings 挙 たか, 振 ふり and 斎 いつ. The older
  reading-options check still lists 斎 い as a HIT: it ignores slots that
  curated distractors fill, and 海 毎 買 fill all three of them. On 故 コ the
  curated card 攻 offers only こう, which the quiz skips, so the random fallback
  fills one slot. No quiz-option or reading-exposure line changed between the
  freeze and the fix apart from the command line. Sampled seeds are not
  exhaustive.
- **Evidence made for the confirmation.** The two Weblio extracts
  (`weblio-chouchin.txt`, `weblio-saigu.txt`) were fetched by the author after
  the first review, because the original packet held no Daijisen entry for
  提灯 or 斎宮; `stroke-types.txt` lists the KanjiVG stroke types of 缶 and 揺.
  GPT independently fetched Kanjipedia, Daijisen and the pinned KanjiVG SVG.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** None of the batch's published commits is rewritten:
  the freeze `9d393a8f` and the fix `3a0399bd` were both made before any push.
  The fix amended an earlier unpushed fix commit once, before the confirmation
  packets were built; the reviewed snapshot is the commit named above.

## Validation and accounting

At `3a0399bd`: 439 host tests pass; validation 0 errors; lint 0 errors and 6
warnings, all on untouched Dictionary lines (一斉, 体操, 振り仮名, 振舞う, 斜 and
平仮名); quiz safety 0/0; manifest rebuild unchanged (version
`8e9e517db93c57cb`); vocabulary 3201/3336; link plan 24 links and 1 declared
remark edit, 0 problems; kanji remarks 0 problems; budget 9,050 entries,
51,415,449 retained and 32,226,868 local-ZIP bytes; the Metadata scan finds no
whole-run gap.

After publication, delivery becomes **392/1,228**, with **836 remaining**.
Until the receipt it stays 377/1,228.
