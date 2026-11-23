# Batch 139: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **嫁 嬢 宗 宜 宣 宴 寂 密 審 尋 屈 属 岬 峠 崩**
  (source rows 237, 241, 246, 248, 249, 253, 255, 257, 261, 266, 275, 277,
  281, 283, 290).
- Published base: `d65a9931d4231bf56f76c2c2a975b8bdd75eb3cd`.
- Blind-review freeze: `a47efe9af926316eaa86656033bf6e109f2be697`.
- Fix 1: `3b6f972767928e01261440466899f32df398d7f1` (嫁, 嬢, 宣 and 峠, and the
  宴会 word article).
- Fix 2: `f1b2bdb84f7e932dfe59cb68829fc004415d0a74` (one line of 嬢), the
  reviewed snapshot.

The freeze adds fifteen cards and stroke files. Twenty existing word articles
each gain one link to a new card, and no word article is added. In 宴会, 崩す
and 崩れる the sentence that said the character had no card is dropped; 附属
now says only that 附 has no card yet. No existing kanji card changes. The two
fix commits change only the four named cards, 宴会 and the generated
`manifest.json`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. The two
initial runs ran one after the other and reviewed the same frozen packet
(`packet/`) without seeing each other's work. In each of the two confirmation
rounds both agents ran at the same time, each making its own calls serially.
Each confirmation was a later turn of the same agent. It received a new packet
with the author's statement answering its own previous report (`RESPONSE.md`),
the list of changes (`CHANGES.md`), the revised cards and the exact diff, and
never the other family's reports. Models and times come from the runtime
session records, not from the reports.

In the first confirmation round Claude confirmed fix 1 with one optional point,
P1, and GPT found one new minor defect, G2; both concern the same shortened
gloss on 嬢. Claude's run had a second user turn
(`prompts/confirm-claude-followup.txt`): its report said it had not read
`CHANGES.md`, which the round asked for, so it was asked to read the file in
full, check every claim and rewrite its report. It stayed CONFIRMED and noted
two wording slips in `CHANGES.md`, W1 and W2. Fix 2 changes the one 嬢 line,
and its `CHANGES.md` corrects W1 and W2; both reviewers confirmed fix 2.
`confirm-packet/` holds four packets: `claude` and `gpt` (fix 1), `claude2` and
`gpt2` (fix 2); files they all share are in `common`.

| Run | Model | Snapshot | Window, 2026-11-18 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `a47efe9a` | 14:28:25–14:37:51 | 58 | 57 | 1 | PASS with minor findings (C1, C2) |
| initial-gpt | gpt-6.1-sol | `a47efe9a` | 14:39:44–14:54:16 | 71 | 70 | 1 | NEEDS FIX (minor, G1) |
| confirm-claude | claude-opus-5.5 | `3b6f9727` | 15:32:23–15:37:35 | 21 | 19 | 1 | CONFIRMED (optional P1; W1, W2) |
| confirm-gpt | gpt-6.1-sol | `3b6f9727` | 15:32:23–15:40:49 | 34 | 33 | 1 | NEEDS FIX (minor, G2) |
| confirm2-claude | claude-opus-5.5 | `f1b2bdb8` | 15:51:38–15:53:00 | 6 | 5 | 1 | CONFIRMED |
| confirm2-gpt | gpt-6.1-sol | `f1b2bdb8` | 15:51:38–15:54:32 | 19 | 18 | 1 | CONFIRMED |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 宣's のたまう row omitted JMdict's note that 宣う was originally respectful and is now often used sarcastically | Claude, initial | Changed: the row adds the note (JMdict 2842102); Claude marked it resolved |
| C2: 嫁 did not say that JMdict marks its third sense, "wife", as Kansai dialect | Claude, initial | Changed; Claude marked it resolved |
| G1: 峠 excluded 通 and 経 from its quiz options, although they share only the English word "pass" with it | GPT, initial | Changed: both removed from 峠's exclusions, and a new Notes bullet separates a mountain pass from the verbs 通る and 経る (JMdict 1433030, 1251110); GPT marked it resolved |
| O1: 嬢 named none of お嬢様, 嬢ちゃん and 嬢さん | Claude, initial | Changed: a Notes bullet quotes their JMdict glosses, including 嬢さん read とうさん as a Kansai honorific (1694880, 2836096, 2230740, 2216510) |
| O2: 宣 did not name the Daijisen kun readings besides のたまう | Claude, initial | Changed: it names のべる, のる and のたまう, says JMdict has 宣べる only as a rare spelling of 述べる and has no のる entry with 宣, and adds 宣べ伝える (1340820, 2096040) |
| O3: in the 宴会 article, a colon made エン + カイ read as the "kind of gathering" | Claude, initial | Changed: a full stop and "The on readings are"; the wording predates the batch |
| O4: 峠's title word "peak" may suggest a summit | Claude, initial | Not changed: Claude had already judged the title acceptable; decline accepted |
| Optional 1: shorten long reference inventories, such as 密's last bullet, for phone reading | GPT, initial | Declined: published N1 cards use the same layout, so it is a format change for all N1 cards, recorded for a later format pass; GPT accepted the decline |
| Optional 2: 崩 selects both くずれる and くずす, while the scheduled queue keeps one くず stem | GPT, initial | Declined: the card names the two metadata selections, as 184 cards do; the scheduling behaviour belongs in app or format documentation; GPT accepted the decline |
| Optional 3: keep English-homonym rationales explicit | GPT, initial | No action needed: the revised 峠 separates the two senses of "pass", and 宴 still says 党 shares only the English word "party"; GPT marked it resolved |
| 岬: Claude could not verify Daijisen's character entry, which the packet's Weblio extract lacked | Claude, initial (limit) | The fix-1 confirmation packets add `evidence/weblio-岬-character.txt`; Claude marked the limit resolved |
| E1: the extra readings fed to the reading audits left out two Daijisen kun readings, 宗 たっとぶ and 宣 のる | author, at fix 1 | Audits rerun with both; no hit or collision count changed, and both reviewers checked every differing line (`evidence/extras-correction.txt` in `confirm-packet/claude` and `gpt`) |
| P1, G2: 嬢's new bullet shortened the second gloss of 嬢さん じょうさん to "young lady" | Claude (optional P1) and GPT (G2), confirm | Changed in fix 2 to "young lady (esp. of respectable upbringing)", as JMdict 2230740 gives it; both reviewers marked it resolved |
| W1, W2: the first `CHANGES.md` said two Metadata ids "move before" the new ones, and that 宴会 changed "only the colon" | Claude, confirm follow-up | Corrected in the fix-2 `CHANGES.md`: the ids stayed and the new ones were appended; 宴会 also gained "The on readings are"; Claude marked both resolved |

GPT found the 峠 exclusion defect and the shortened 嬢さん gloss; Claude raised
the source-wording points and most of the optional ones, and also flagged the
嬢さん gloss as optional. These are contributions to this sample, not model
rankings.

## Limits

- **Execution.** Every run was strictly serial. No GPT report names the exact
  model; the runtime records gpt-6.1-sol. confirm-claude's rewrite replaced
  its first report file, so `reports/confirm-claude.md` is the report after the
  follow-up turn. The final messages of confirm-claude and confirm2-claude add
  a short preface before the report; the files are the record.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, or writes made through PowerShell. The session
  events show:
  - initial-claude printed all fifteen cards in full through PowerShell, 嫁
    inside its first listing command, so its audit lists 嫁 as unread; it read
    the changed lines of all twenty word-article diffs in one loop and the
    宴会 diff in full, so the twenty word snapshots are listed as unread. Its
    eight write-like flags are `-replace` text operations inside read
    commands.
  - initial-gpt printed all fifteen cards, twenty word articles and fifteen
    stroke files in full through PowerShell loops, and analysed them in
    Python; its audit lists 14 cards as unread.
  - confirm-claude printed the four changed cards and 宴会 in full, read
    lines 21–27 of 岬, and compared the other cards by hash with the original
    packet. confirm-gpt viewed the four changed cards and 宴会 in full,
    rebuilt them from `fix.patch` in Python and checked the other eleven
    cards' front matter and selected lines there. confirm2-claude printed 嬢
    in full and compared the other fourteen with the fix-1 packet's copies;
    confirm2-gpt viewed 嬢 and compared the other fourteen byte for byte.
    confirm-claude and confirm2-claude wrote their reports through
    PowerShell: the first audit flags that write only as write-like, and the
    second records no write.
  - confirm-gpt and confirm2-gpt's audits flag the `review-packets` folder
    because a Python script used it as a base path to reach their own
    packets; the flag is a false positive.
- **Sources.** The 岬 card's claims about its Daijisen character entry rest on
  `evidence/weblio-岬-character.txt` in `confirm-packet/claude` and `gpt`; the
  original packet's Weblio extract held only another dictionary's block.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. The audits in
  `packet/evidence/audits/` are superseded because their extra readings left
  out 宗 たっとぶ and 宣 のる (E1). The corrected audits are
  `checks/reading-exposure.txt` and `checks/reading-options.txt` in the
  confirmation packets. At `3b6f9727` and `f1b2bdb8` they report 0
  production, 0 padded-session and 0 one-holder hits, and 11 latent
  collisions: 嫁 かす, 宗 そ, 宜 き, たか, のり, よし and よい, 寂 しずか,
  尋 つぐ and つね, and 岬 さき. One KANJIDIC2 name-only reading is disclosed,
  not fixed: 宗 し on the シュウ prompt, offered by the curated distractor 示
  in the N1 and All stacks; both reviewers judged it not a defect. The reading-options check labels 岬 さき HIT (offered by 先)
  because it ignores slots that curated distractors fill; 岬's curated 山, 田
  and 中 fill every reading slot, so it cannot be drawn. Neither tool models
  a custom pool without a target's curated distractor cards, where these
  latent readings could be offered as wrong options. Sampled seeds are not
  exhaustive.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** Fix 1 had three earlier local versions,
  `c2b9973b`, `8530c8bb` and `2dacd6e5`, each amended before any confirmation
  packet was built. The first quoted the glosses of 通る and 経る in part,
  called both senses of お嬢様 polite language and did not name 宣べ伝える;
  the second changed only the 通る and 経る wording; the third did not yet
  include the 宴会 change. None was reviewed or published.
- Reviewers also read public web pages and APIs: Weblio (Digital Daijisen),
  jisho.org, kanjiapi.dev (which refused with HTTP 403) and the pinned KanjiVG
  revision on GitHub. The GPT runs made most of these reads through Python, so
  the scope audits list only the `web_fetch` calls; the reports describe them.

## Validation and accounting

At `f1b2bdb8`: 436 host tests pass; validation 0 errors; lint 0 errors and 2
warnings, both on untouched Dictionary lines of existing word articles (宣伝,
宴会); quiz safety 0/0; manifest rebuild unchanged; vocabulary 3201/3336;
budget 8,958 entries, 50,999,192 retained and 32,020,620 local-ZIP bytes; the
Metadata scan finds no whole-run gap. `origin/main` is still `d65a9931`, the
base, so no integration merge is needed.

After publication, delivery becomes **347/1,228**, with **881 remaining**.
Until the receipt it stays 332/1,228.
