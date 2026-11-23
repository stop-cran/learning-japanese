# Batch 143: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with no remaining finding. Publication is **pending** at this
closure commit; the later receipt establishes the remote commit, CI and served
ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **施 旋 旗 既 旦 旨 暑 暦 朗 条 架 柄 染 株 桜**
  (source rows 483, 484, 485, 486, 487, 488, 508, 511, 518, 526, 531, 532,
  535, 542, 550).
- Published base: `ef2b1b9fc9c5d40def44c4c9734f62004958a4a2`.
- Blind-review freeze: `6b5934e71945ed215cf57a8291117762e67b1d9e`.
- Fix: `9b8f50a8b9ddb2123137573ccb26761e05954491` (the cards 旋 既 旦 旨 暑
  朗 条 架 柄 染 株 桜 and the generated `manifest.json`), the reviewed
  snapshot. 施, 旗 and 暦 are unchanged from the freeze.
- Front matter changed in two cards, 旋 (`quiz_exclusions` loses 凱) and 既
  (loses 在, 存 and 有); no title, tag, metadata reading, curated distractor or
  stroke file changed.

The freeze adds fifteen cards and stroke files. Seventeen existing word
articles each gain one link to a new card, and no word article is added. The
existing 西暦 article also has one declared edit: the sentence that said 暦 had
no card here now links 暦. No other existing kanji card changes.

There were two confirmation rounds on the Claude side. The first fix commit
`5bede460` was reviewed by the first Claude confirmer (`confirm-claude-1`),
which found one new minor defect in unchanged text (条.md:61). A second fix
commit replaced it before any push, by amending the unpushed commit, so
`5bede460` is not in the history. The reviewed snapshot above is that second
commit; the round-1 packet bytes are not retained, and `confirm-packet/` holds
the packets rebuilt at the same paths for `9b8f50a8`. The GPT confirmation
and the second Claude confirmation both saw `9b8f50a8`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All five
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's report (`RESPONSE.md`), the list of changes
(`CHANGES.md`), the revised cards and the exact diff, and was allowed to read
the original packet and its own family's earlier reports, and never the other
family's reports. `confirm-packet/` holds the two packets; files they share
are in `common`. The revised cards are not stored again, because they are the
blobs at `9b8f50a8`. Models and times come from the runtime session records,
not from the reports.

| Run | Model | Snapshot | Window, 2026-11-19 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `6b5934e7` | 07:31:35–07:42:03 | 51 | 50 | 1 | NEEDS FIX (C1 to C9, all minor) |
| initial-gpt | gpt-6.1-sol | `6b5934e7` | 07:42:40–07:56:12 | 68 | 67 | 1 | NEEDS FIX (G1 to G4, all minor) |
| confirm-claude-1 | claude-opus-5.5 | `5bede460` | 08:16:24–08:21:43 | 39 | 38 | 1 | NEEDS FIX (one new minor finding, 条.md:61) |
| confirm-gpt | gpt-6.1-sol | `9b8f50a8` | 08:27:23–08:34:10 | 41 | 40 | 1 | CONFIRMED (no optional point) |
| confirm-claude | claude-opus-5.5 | `9b8f50a8` | 08:34:26–08:38:59 | 36 | 36 | 2 | CONFIRMED (three optional notes) |

`confirm-claude-1` confirms `initial-claude` and `confirm-claude` is the fresh
agent that confirms `confirm-claude-1`'s result; `confirm-gpt` confirms
`initial-gpt`. `reports/` holds the verbatim reports, `prompts/` the exact
prompts and `scope-audits/` each run's read-scope audit. The report of
`confirm-claude-1` is stored under that name; its prompt
(`prompts/confirm-claude-1.txt`) is reconstructed from the final confirmation
prompt by swapping in the `5bede460` snapshot, because the packet and prompt
were rebuilt at the same paths. `provenance.json` hashes the files with the
packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 既 and 朗 call the Joyo parenthesised form a "compatibility ideograph" | Claude, initial (minor) | Changed: 既.md:38 and 朗.md:43 say the table adds the traditional (Kangxi dictionary) form in parentheses (`confirm-packet/common/evidence/joyo-item6.txt`, 表の見方 item 6). Resolved |
| C2: 桜's whole-word caveat covers 桜ん坊 | Claude, initial (minor) | Changed: 桜.md:37 limits the caveat to 桜桃 read さくらんぼ; in 桜ん坊 桜 is さくら followed by ん and 坊 read ぼ (JMdict 1298460). Resolved |
| C3: 桜 "mizaru cherry" | Claude, initial (minor) | Changed: 桜.md:25 says "the fruit-cherry tree (ミザクラ, mizakura)", following Daijisen's 「木の名。ミザクラ」. Resolved |
| C4: 染's 愛染 called a whole-word reading although Daijisen records ゼン | Claude, initial (minor) | Changed: 染.md:34, 40 and 42 say 染 is read ゼン in 愛染, an on reading outside the Joyo table, recorded by Daijisen and Kanjipedia (JMdict 2583650). Resolved |
| C5: 旨味 is a separate JMdict entry; 上手い/巧い spelling | Claude, initial (minor) | Changed: 旨.md:37 cites the separate うまみ entry (1310520: 旨み and 旨味, 旨味 tagged ateji; 旨 is read うま) and drops "not a reading to split"; 旨.md:25 says JMdict marks the skillful sense as especially written 上手い or 巧い. Resolved |
| C6: 株's 守株 is 守 シュ + 株 シュ | Claude, initial (minor) | Changed: 株.md:25 presents 守株 しゅしゅ as 守 シュ + 株 シュ, an idiom from the fable of guarding a stump (JMdict 1882040). The suggested 株を守る mention was not added. Resolved |
| C7: 旗's title shares "standard" with 準, 範 and 規 | Claude, initial (minor) | Not changed. The curated distractors 施, 旋 and 旅 fill all three slots of the 旗 prompt, quiz safety reports 0/0, and dropping a word from a published title changes the title index that every linking card and word article uses. Decline accepted |
| C8: 旦's garbled sentences; ダンナ in katakana | Claude, initial (minor) | Changed: 旦.md:25 and 52 say that no ordinary JMdict word using あした was found and that 一旦 is read いっ + タン; 旦.md:41 writes だんな. Resolved |
| C9: 柄's Common words pairs え with "pattern" | Claude, initial (minor); GPT, initial (G1) | Changed: 柄.md:48-49 are two bullets, 柄 え — handle; grip (1508290) and 柄 がら — pattern; design (1508300), linking the same article. Resolved by both |
| O1: lead the 条 すじ row with "line; stripe" | Claude, initial (optional) | Not changed: the row follows JMdict's 筋 entry order and the card says no word article exists yet. Decline accepted |
| O2: 条's stroke wording and jargon paragraph | Claude, initial (optional) | Partly applied: 条.md:58 says "an added horizontal stroke"; the paragraph is untrimmed. Accepted |
| O3: 架's attribution | Claude, initial (optional) | Applied: 架.md:25 uses 書架 しょか, bookshelf, from the Daijisen extract. Resolved |
| O4: name the 朗 distractors | Claude, initial (optional) | Applied: 朗.md:51 says the cards 月, 有 and 朝 supply the distractors. Resolved |
| O5: odd English in copied word-article titles | Claude, initial (optional) | Not changed: word articles are outside this batch's scope. Decline accepted |
| O6: 施's title overlaps | Claude, initial (optional) | No change; the author judged the meanings distinct. Accepted |
| O7: add 菌株 to 株 | Claude, initial (optional) | Not applied: 雌雄異株 is the Daijisen example and 菌株 is not in the extract. Decline accepted |
| O8: account for 朗's name readings | Claude, initial (optional) | No change: name readings need no account on the card. Accepted |
| G1: 柄 え paired with "pattern" | GPT, initial (minor) | Changed as for C9. Resolved |
| G2: 旦つく presented simply as "husband" | GPT, initial (minor) | Changed: 旦.md:34 reads "husband (a slighting word)" (Daijisen 「旦那」を軽んじていう語, `evidence/weblio-dantsuku.txt`). Resolved |
| G3: 暑 "蒸 supplies むし" | GPT, initial (minor) | Changed: 暑.md:36 says 蒸 writes む and し is okurigana (JMdict 1356870). Resolved |
| G4: association-based exclusions 既–在, 既–存, 既–有 and 旋–凱; 旋's false comparison | GPT, initial (minor) | Changed: those four exclusions are removed from 既.md:14 and 旋.md:14 with the matching Notes sentences (既.md:48, 旋.md:54); 凱 is still explained on 旋.md:41 and 51. The three audits reran unchanged apart from command lines. Resolved |
| O-A: compress the 条 and 架 prose | GPT, initial (optional) | Not applied: the paragraphs are the card's support for its readings. Decline accepted |
| O-B: 朗's 良 at the left | GPT, initial (optional) | Not applied: the mnemonic is labelled a memory aid, and 朗.md:51 names 月, 有 and 朝 as the distractors. Decline accepted |
| N1: 条.md:61 called 条彫り, 条播き and 発条 all whole-word readings | Claude, first confirmation (minor, in unchanged text) | Changed in the second fix: in 条彫り and 条播き 条 is read すじ, the kun reading in the table, not selected for questions here (Daijisen 「［難読］条彫(すじぼ)り・条播(すじま)き・発条(ばね)」); the whole-word caveat stays for 発条 ばね only. Both later confirmers resolved it |
| N2: 旨.md:25 wording "esp." | Claude, first confirmation (optional) | Applied: "JMdict marks its skillful sense as especially written 上手い or 巧い" |
| N3: trim 株.md:36; mention さくらんぼう on 桜 | Claude, first confirmation (optional) | Not applied |
| N4: 条.md:61 "table above" could say "Readings table"; the 株.md:36 守株 echo could be dropped; 旨.md:37 could quote JMdict's tag "ateji (phonetic) reading" | Claude, second confirmation (optional) | Not applied, because any card change needs an amend, a new gate run and another confirmation round for wording that is not wrong. Recorded for a later pass |

Claude raised all nine initial findings and all eight optional points; GPT
independently raised the 柄 pairing, the 旦つく label, the 蒸し暑い reading and
the four exclusion pairs. Only Claude's first confirmer found the 条.md:61
defect, in text that neither initial reviewer reported. These are
contributions to this sample, not model rankings.

## Integration with current main

`origin/main` had not moved since the base `ef2b1b9f` (checked with `git fetch`
at closure), so no merge and no integration review were needed.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family, so it had no memory of its own earlier reading. The two Claude
  confirmers are different agents: `confirm-claude` did not see
  `confirm-claude-1`'s reasoning, only its report and the author's answer. The
  confirmations of the two families are independent of each other.
- **Execution.** Every run was serial. No GPT report names the exact model; the
  runtime records gpt-6.1-sol. confirm-claude's audit flags two overlapping
  `view` calls (maximum two in flight, one overlapping start at 08:35:33Z)
  although its Limits section says it made no parallel calls; this is
  disclosed, not rerun, as in B140. initial-claude's audit flags one recursive
  PowerShell listing of its own packet directory (6,592 files, which includes
  the `repo` context corpus) and one write-like shell command, which is the
  here-string that wrote its own report file. confirm-claude-1's audit flags a
  create or edit outside its report path: the report was written to
  `confirm-claude.md` and the author renamed it to `confirm-claude-round1.md`
  before the final round, so the audit's allowed path no longer matches. confirm-gpt's audit reports one path
  outside the packet and report, a false positive from the packet-root folder
  used as a base-path variable in its shell commands. All five reports equal
  the runs' final messages.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. The confirmation mandate covered the changed cards, so
  the prose of the three unchanged cards (施, 旗, 暦) and every word article
  were not re-read by the confirmers.
- **Reviewers' own limits.** The 旦 claim that no ordinary JMdict word uses あした
  rests on an initial-round scan of the pinned JMdict. 染 ゼン was accepted
  from the packet's Kanjipedia extract. Neither reviewer ran a JVM or Android
  build or could certify the pool construction beyond the supplied audits.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `9b8f50a8` they report 0
  production, 0 padded-session and 0 one-holder hits, no labelled reading
  option and 10 latent collisions counted per quiz prompt (seven distinct
  pairs): 旋 せ (offered by 世), 朗 あき (秋 空) and お (小 御 男 緒), 柄 ら (等),
  いきおい (勢) and つく (付 就 点 着 突), and 桜 さ (小 早 然). The first gate
  run showed 柄 ら drawable on the がら prompt of a Starter practice session
  that borrows 等, because the third curated distractor 札 is not a Starter
  card; it was replaced by 休 before review, and the curated 木 本 休 now fill
  every slot. No quiz-option or reading-exposure line changed between the
  freeze and the fix apart from the command line. Sampled seeds are not
  exhaustive.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The first fix
  `5bede460` was amended into `9b8f50a8` while unpushed; the freeze is
  unchanged, and the reports of both Claude confirmers are kept.

## Validation and accounting

At `9b8f50a8`: 439 host tests pass; validation 0 errors; lint 0 errors and 4
warnings, all on untouched Dictionary lines (一旦, 凱旋, 蒸し暑い, 西暦); quiz
safety 0/0; manifest rebuild unchanged (version `bc3d69f584d0420e`);
vocabulary 3201/3336; link plan 17 links and 1 declared remark edit, 0
problems; kanji remarks 15 of 15 present, 0 problems; budget 9,080 entries,
51,521,586 retained and 32,279,176 local-ZIP bytes; the Metadata scan finds no
whole-run gap.

After publication, delivery becomes **407/1,228**, with **821 remaining**.
Until the receipt it stays 392/1,228.
