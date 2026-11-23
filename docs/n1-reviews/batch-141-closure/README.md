# Batch 141: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **悔 悟 惑 惜 愉 慎 慮 慰 憧 憩 懐 懸 扇 抽 拡**
  (source rows 365, 366, 371, 372, 378, 382, 387, 388, 392, 393, 398, 400,
  405, 418, 426).
- Published base: `466b7b283661febf8f93fa2d9675ea0a14767cde`.
- Blind-review freeze: `a92d134afd93566ba705b586daf8d7969c683a5f`.
- Fix 1: `65b47299831240115de12f5c9c5f0f6ed0e2065d` (懐, 懸, 扇, 抽, the
  existing card 張 and the word articles 悔しい and 悔やむ).
- Fix 2: `094a1649552f7773f0a636a104cc797a765bec6e` (懸 and 抽), the reviewed
  snapshot.
- Integration merge with current main:
  `a366ac8aaf85462c41d7ac39cbea7db4da8584c1` (see below).

The freeze adds fifteen cards and stroke files. Twenty-one existing word
articles each gain one link to a new card, and no word article is added. The
Notes bullet of the existing 張 card that said 緊 and 拡 had no cards now names
only 緊. No other existing kanji card changes. Each fix changes only the files
named above and the generated `manifest.json`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. The two
initial runs ran one after the other and reviewed the same frozen packet
(`packet/`) without seeing each other's work. In each of the two confirmation
rounds both agents ran at the same time, a departure from the contract (see
Limits). Each confirmation was a later turn of
the same agent. It received a new packet with the author's statement answering
its own previous report (`RESPONSE.md`), the list of changes (`CHANGES.md`),
the revised cards and the exact diff, and never the other family's reports.
`confirm-packet/` holds the four packets: `claude` and `gpt` for fix 1,
`claude2` and `gpt2` for fix 2; files they share are in `common`. The revised
cards are not stored again, because they are the blobs at `65b47299` and
`094a1649`. Models and times come from the runtime session records, not from
the reports.

| Run | Model | Snapshot | Window, 2026-11-18 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `a92d134a` | 20:28:38–20:38:45 | 64 | 63 | 1 | NEEDS FIX (C1 moderate, C2 minor) |
| initial-gpt | gpt-6.1-sol | `a92d134a` | 20:39:42–20:56:27 | 74 | 73 | 1 | NEEDS FIX (G1 minor) |
| confirm-claude | claude-opus-5.5 | `65b47299` | 21:10:32–21:14:21 | 20 | 19 | 1 | NEEDS FIX (minor, F1, F2) |
| confirm-gpt | gpt-6.1-sol | `65b47299` | 21:10:32–21:17:12 | 38 | 37 | 1 | NEEDS FIX (minor, G2) |
| confirm2-claude | claude-opus-5.5 | `094a1649` | 21:31:40–21:33:27 | 8 | 7 | 1 | CONFIRMED (two optional nits) |
| confirm2-gpt | gpt-6.1-sol | `094a1649` | 21:31:40–21:36:17 | 24 | 23 | 1 | CONFIRMED (no optional point) |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 悔しい and 悔やむ still said there was no 悔 card, beside the new link to it | Claude, initial (moderate); independently GPT's G1 (minor) | Changed: the sentences "There is no 悔 card in the current collection." (悔しい:25) and "No 悔 kanji card is currently available." (悔やむ:28) are deleted and declared in `word-remarks.json`. The author's scan of every published word article and kanji card found no other such sentence for the batch's kanji. Both reviewers marked it resolved |
| C2: 抽's ひき- row was illustrated with 抽き出し, where 抽 writes only ひ | Claude, initial | Fix 1 used 抽斗 and split it as 抽 ひき, 斗 だし, following Claude's own first remedy; Claude marked it partially resolved and raised F1. Resolved by fix 2 (see F1) |
| F1 and G2: the 抽斗 split gives 斗 a reading だし it does not have | Claude and GPT, first confirmation, independently | Changed in fix 2: the ひき- row (抽:34) uses 抽出し, which JMdict lists as a search-only form and the card says is not a recommended word example; 抽:36 calls 抽斗 ひきだし a reading of the whole word and says KANJIDIC2 gives 斗 no reading だし (`confirm-packet/claude2/evidence/kanjidic2-斗.xml`). Both reviewers marked it resolved |
| O1: 張's Notes could name 拡 as the other kanji in 拡張 | Claude, initial (optional) | Changed in fix 1: 張:59 names 拡, "expand; enlarge; widen," as the other kanji in 拡張, and only 緊 is left without a card; Claude marked it resolved |
| O2: 悔 could cite 悔過 けか for ケ | Claude, initial (optional) | Not changed: 悔:27 presents ケ with 懺悔 and says it is voiced to げ there; 悔過 (JMdict 2865883) is a Buddhist term with no word article. Decline accepted |
| O3: 懸 said "the common words" for a section with one word | Claude, initial (optional) | Changed: 懸:56 says "the common word"; Claude marked it resolved |
| O4: 慎 could add つつましやか and 要慎 | Claude, initial (optional) | Not changed: つつましやか (JMdict 2201680) is a relative of 慎ましい, which the つつ.ましい row covers, and 要慎 is a search-only form in JMdict's 用心 entry (1546310). Decline accepted |
| O5: 懸 could mention the reading けんねん of 懸念 | Claude, initial (optional) | Fix 1 added it at 懸:46 (JMdict 1257720). Claude marked it partially resolved and raised F2 |
| F2 and P1: けんねん was presented without JMdict's irregular-kana tag | Claude (F2, minor) and GPT (an optional point, answered as P1), first confirmation, independently | Changed in fix 2: 懸:46 says JMdict lists けねん first and also けんねん, "which it marks as irregular kana usage". Both reviewers marked it resolved |
| Optional 1: shorten or restructure the long reference inventories | GPT, initial | Changed for 懐 (the reference bullet at 懐:66-69 is split into four) and 扇 (split before "Under おうぎ"); 悟:25, 惑:51 and 慮:53 are left as they are. GPT marked it resolved |
| Optional 2: compress the practice-selection explanations and mnemonic disclaimers | GPT, initial | Not changed: these are collection-wide conventions, on 732, 214 and 116 of the 1,367 published cards. Decline accepted |
| Optional 3: no expansion needed for name readings or unquizzed extras | GPT, initial | Agreed; no change |
| 抽:34 calls 抽出し "this index form", new jargon after "search-only kanji form" | Claude, second confirmation (optional) | Deferred: wording polish, recorded for a later pass |
| 抽:36 "Daijisen lists the rarely used spelling 抽斗" can read as if Daijisen said "rarely used"; that label is JMdict's, and Daijisen lists 抽斗 as hard to read (難読) | Claude, second confirmation (optional) | Deferred: the sentence is true and the label is attributed to JMdict at 抽:34; recorded for a later pass |

Claude raised both initial findings, all five numbered optional points and the
two confirmation findings; GPT independently raised the stale 悔 sentences, the
抽斗 split and the missing irregular-kana label, and raised the
reference-inventory point. These are contributions to this sample, not model
rankings.

## Integration with current main

After the reviewed fix 2, `origin/main` moved from the base `466b7b28` to
`ddc7da27cb316bf341edf79913979976fb2d7a4a`: eight signed owner commits adding
the N5 Momotaro reading pilot (`.gitattributes`, `docs/content-format.md`,
`docs/reading-n5.md`, `manifest.json`, `reading/momotaro-n5.json`,
`tools/build_manifest.py`, `tools/test_reading.py`, `tools/validate.py` and
`tools/validate_reading.py`). Following step 4 of the issue #60 contract, the
merge `a366ac8a` (parents `094a1649` and `ddc7da27`) is a non-rewriting merge.
`manifest.json` was the only conflict and was regenerated with
`tools/build_manifest.py` (version `e746f081400dd921`).

[`integration/merge-proof.json`](integration/merge-proof.json) is produced by
[`integration/merge_proof.py`](integration/merge_proof.py):
`python -X utf8 merge_proof.py <repo> a366ac8a merge-proof.json`.

- Of the 46,212 paths compared, every one except the derived `manifest.json`
  equals one parent byte-for-byte.
- The 52 batch runtime files (15 new cards, 張, 15 stroke files and 21 word
  articles) equal `094a1649`, and none was changed by main.
- None of the 218 paths the batch files link to was changed by main, and no
  file main changed mentions a batch kanji or a changed word.
- The regenerated manifest lists all 52 files.

The contract requires a bounded independent review only for changed teaching or
an overlapping substantive conflict. Neither applies here: the reviewed
teaching is byte-identical, main's changes touch no batch file, link target or
mention, and the only conflict is the derived manifest. No integration review
was held, as for the earlier non-overlapping merges in B023, B054 and B055;
B134 held a bounded integration review of a merge made after a cross-PC
handoff.

Gates on `a366ac8a`: 439 host tests pass (main added three); validation 0
errors; lint 0 errors and the same 2 warnings; manifest rebuild unchanged
(SHA-256 `C330AECDFDC23BB769C118E860D79E77E3550E24AC0AB0BD8580236E2420F193`);
budget 9,020 entries, 51,265,845 retained, 51,624,936 inflated and 32,157,201
local-ZIP bytes. Every batch audit (quiz safety, reading exposure, reading
options, link plan, kanji remarks, Metadata scan, okurigana scan, vocabulary
and lint) is identical to its run at `094a1649` apart from the command line.

## Limits

- **Concurrent confirmations.** The issue #60 contract says to run the
  reviewers serially, with at most one active reviewer at any instant. In both
  confirmation rounds the Claude and GPT confirmations overlapped (21:10:32 to
  21:14:21 and 21:31:40 to 21:33:27), as they did in B137 to B140, where it was
  disclosed but not flagged as a departure. Each reviewer still worked only
  from its own packet and never saw the other's reports, so the confirmations
  stay independent; the departure is in execution, not in evidence. From B142
  on, confirmations run one after the other.
- **Execution.** Every run made its calls one at a time. No GPT report names
  the exact model; the runtime records gpt-6.1-sol. The confirmation prompts
  for round 2 also forbade recursive listings inside a packet, after
  confirm-claude made one (`Get-ChildItem … -Recurse -Name`) over the
  snapshot folder of its own packet, which its audit flags; the listing stayed
  within its allowed packet. confirm2-gpt's report file adds one word
  ("reading") and a trailing newline to its final message; the file is the
  record.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python. The session events show:
  - initial-claude viewed all fifteen new cards in full and read 張 only
    through its diff (lines 56-62). It read the changed lines of the
    twenty-one word diffs through PowerShell; for nine words (休憩, 愉快, 慎重,
    惜しい, 一生懸命, 覚悟, 遠慮, 拡充 and 拡張) it read only the changed line. It
    parsed the stroke files for their keys and stroke counts and did not
    inspect them visually. A temporary file created by the runtime outside
    the packet was not opened.
  - initial-gpt printed all sixteen cards through PowerShell and analysed the
    stroke files, word articles and dictionary data in Python, so its audit
    lists every card as unread.
  - confirm-claude read the cards through PowerShell, so its audit lists all
    sixteen as unread.
  - confirm-gpt viewed the five changed cards (張, 懐, 懸, 扇, 抽) and the two
    changed word articles in full and checked the eleven unchanged cards'
    front matter in Python.
  - confirm2-claude read only through PowerShell. Its comparison of the check
    outputs stopped at `validate.txt`; it then read the validation, unit-test,
    link-plan and kanji-remark outputs directly but did not check the
    vocabulary, manifest and budget outputs or the hash of `QuizBuilder.kt`.
    It did not verify the 191-byte and 77-byte budget deltas (the author's
    checks at `65b47299` and `094a1649` confirm them), the moved Metadata-scan
    line or the claim that the wording follows 双, 圧 and 訓, and it did not
    re-read the thirteen cards unchanged by fix 2.
  - confirm2-gpt viewed 抽 and 懸 in full and compared the other files in
    Python.
  - The first round-1 confirmation audit was run with relative paths, which
    falsely flagged every path; it was rerun with absolute paths, and those
    files are the record.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `094a1649` they report 0
  production, 0 padded-session and 0 one-holder hits and 5 latent collisions:
  悔 け on two prompts, 慎 みつ, 懐 かね and 扇 おう. Fallback options fill one
  slot each on four prompts: 慮 リョ (虎), 慰 なぐさ.める (封), 憧 あこが.れる (慢)
  and 懐 なつ.かしい (慢). Neither tool models a custom pool without a target's
  curated distractor cards. Sampled seeds are not exhaustive.
- **Packet tooling.** `n1_confirm_packet.py` was changed during this batch so
  that a changed card outside the batch, such as 張, is handled as a file
  outside the batch cards, and so that a round-2 packet also carries the files
  changed by an earlier revision (張, 悔しい and 悔やむ).
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** The freeze replaced an earlier local commit,
  `99087e7a`, before any packet was built; it was amended once only to carry
  the freeze budget. Neither the earlier commit nor the pre-commit check run on
  the uncommitted fix-1 tree was reviewed or published.
- Reviewers also read public web pages: Weblio (Digital Daijisen), Kanjipedia
  (one direct request returned HTTP 500 before the entry was fetched), jisho.org,
  Wiktionary, two news pages found by a search for 抽斗, the pinned KanjiVG
  revision on GitHub and kanjiapi.dev (which failed). The GPT runs made some of
  these reads through Python, so the scope audits list only the `web_fetch` and
  `web_search` calls; the reports describe them.

## Validation and accounting

At `094a1649`: 436 host tests pass; validation 0 errors; lint 0 errors and 2
warnings, both on untouched Dictionary lines (扇風機 and 威張る); quiz safety
0/0; manifest rebuild unchanged (version `d8fc2aa7f5ca5c49`); vocabulary
3201/3336; link plan 21 links and 2 declared remark edits, 0 problems; kanji
remarks 0 problems; budget 9,018 entries, 51,265,730 retained and 32,146,429
local-ZIP bytes; the Metadata scan finds no whole-run gap. The gates on the
integration merge are listed above.

After publication, delivery becomes **377/1,228**, with **851 remaining**.
Until the receipt it stays 362/1,228.
