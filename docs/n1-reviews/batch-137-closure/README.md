# Batch 137: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **丁 井 仰 但 傑 傷 僕 卸 司 吐 呂 哀 哲 唯 善**
  (source rows 1, 14, 26, 37, 69, 73, 74, 133, 145, 149, 151, 154, 156, 160,
  164).
- Published base: `2532beecec978156528e83252bf05eb0bc0f8e21`.
- Blind-review freeze: `d3c7394d38992b24d3689bc984fdb4a6cf60bc54`.
- Fix 1: `2bc8e9b13ea85b39c533735f63643af44d1ce690` (11 cards).
- Fix 2: `48332d3258953779dda24c0df6fb1c649e6defbb` (the Metadata lines of 丁,
  呂 and 唯), the reviewed snapshot.

The freeze adds fifteen cards and stroke files. Twenty-one existing word
articles each gain one link to a new card, and no word article is added. Three
older texts also lose or update a sentence that said there was no 丁, 傷 or 呂
card: the kanji cards 寧 and 敷 and the word article 火傷. The two fix commits
change only the 12 named cards and the generated `manifest.json`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. The two
initial runs and Claude's first confirmation ran one after another; the last
two confirmations, confirm2-claude and confirm-gpt, ran at the same time, each
agent making its own calls serially. Both initial runs reviewed the same frozen packet (`packet/`) without seeing each other's
work. Each confirmation was a later turn of the same agent. It received a new
packet with the author's statement answering its own previous report
(`RESPONSE.md`), the revised cards and the exact diff, and never the other
family's reports. Models and times come from the runtime session records, not
from the reports.

Claude confirmed fix 1 with one optional point, P1. The author applied it and
two related additions in fix 2, so Claude ran a second confirmation on fix 2.
GPT's only confirmation packet was built after fix 2 and covers both fix
commits. `confirm-packet/` holds the three packets: `claude` (fix 1), `gpt` and
`claude2` (fix 2).

| Run | Model | Snapshot | Window, 2026-11-18 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `d3c7394d` | 07:40:36–07:51:47 | 62 | 62 | 2 | NEEDS FIX (minor, C1) |
| initial-gpt | gpt-6.1-sol | `d3c7394d` | 07:58:46–08:25:54 | 83 | 82 | 1 | NEEDS FIX (minor, G1 and G2) |
| confirm-claude | claude-opus-5.5 | `2bc8e9b1` | 08:46:55–08:51:41 | 28 | 27 | 1 | CONFIRMED |
| confirm2-claude | claude-opus-5.5 | `48332d32` | 09:27:09–09:28:57 | 8 | 7 | 1 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `48332d32` | 09:27:09–09:38:04 | 32 | 31 | 1 | CONFIRMED |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1 / G2: 16 quoted card titles in ten cards lost the space after a comma | both, initial | Changed: each quotation copies the linked card's title. A script then compared all 143 quoted titles in the 15 cards with their targets and found no other mismatch |
| G1: 仰's example 仰山 lacked JMdict's Kansai-dialect label on the "a lot" sense | GPT, initial | Changed |
| O1: 丁 said JMdict has no entry for よほろ | Claude, initial | Changed: no standalone entry; it appears only as つかえのよほろ, an archaic reading of 仕丁 (JMdict 2829360) |
| O2, O3: 傑作's second sense is jocular and dated; 卸下 is a military term | Claude, initial | Changed: both labels added |
| OW: the wording of Daijisen's definition of おろし on 卸 | GPT, initial | Changed: "the act of a wholesaler selling goods to retail shops" |
| LW: the packet's 卸 Weblio extract lacked the Daijisen おろし block | Claude, initial (limit) | Evidence added to the confirmation packets; no card change; Claude marked it resolved |
| O4–O7: two weak exclusions (井–額, 司–営/治/御); 何の変哲もない; five Kanjipedia-only readings; collection-wide boilerplate | Claude, initial | Declined with reasons; Claude accepted each |
| OP: move long reference material down for phone use | GPT, initial | Declined: it is the collection-wide card layout; GPT accepted the decline |
| LE: the exposure audit labels every extra reading "(card text)" | Claude, initial (limit) | Not changed, so the audit outputs stay comparable; Claude accepted. The tool fix is deferred |
| P1: 丁's Metadata line lacked 2829360 (仕丁), which line 40 now cites | Claude, confirm | Changed in fix 2; Claude's second confirmation marked it resolved |
| 呂 and 唯 Metadata lines lacked 1448890 (当て字), 2672330 (唯々) and 1623580 (諾々) | author, after P1 | Changed in fix 2; both reviewers checked the additions |

Both families found the 16 title quotations. GPT also found the missing
Kansai-dialect label; Claude raised most of the source-nuance points and the
Metadata gap. These are contributions to this sample, not model rankings.

## Limits

- **Execution.** initial-claude had two `view` calls in flight once; every
  other run was strictly serial. initial-claude's context was compacted midway,
  and its report says its notes on 丁 to 卸 were summarized; six of those eight
  cards changed and were re-read in full in its confirmations. Its final
  message is the report preceded by a 360-character summary that says "12 of
  the 15 new cards" where the report says ten; the report file is the record.
  Neither GPT report can name the exact model; the runtime records
  gpt-6.1-sol. confirm-gpt's first patch read was truncated and recovered by an
  overlapping range. It did not verify the 42 and 10 published-card counts
  behind the OP decline, which would need a corpus scan, and it read
  `meta_scan.py` without running it, checking the four added ids directly.
- **Scope audits.** The audit script does not attribute reads made through
  shell loops over composed paths, so the confirm-claude and confirm2-claude
  audits list cards as unread that the reports say were read. The author
  checked those claims against the session events. confirm-claude read 丁 仰
  但 傑 僕 in full, 司 吐 呂 哲 善 and again 但 僕 from line 16 (after the
  unchanged front matter) and 卸 through `view`, and byte-compared the
  unchanged 井 傷 哀 唯. confirm2-claude read 丁 呂 唯 in full and compared all
  15 cards line by line with the previous packet. initial-gpt's audit has two
  false flags: a "recursive" pattern that matched the `**` power operator in
  its Python stroke-geometry code, and a "write outside the report path" that
  is a relative path to the report itself. confirm-gpt's audit has the same
  write flag, and lists cards as unread because GPT read them through Python;
  the session events show it printed all 12 changed cards in full.
- **Sources.** "Only in つかえのよほろ" rests on the author's search of the
  pinned JMdict; Claude found no other よほろ headword in WWWJDIC. Each card
  mentions every KANJIDIC2 reading and every reading in its Daijisen character
  entry (卸 has none; its only Daijisen entry is the word おろし); readings only
  Kanjipedia lists are mentioned selectively.
- **Metadata lines.** The rule that the Metadata line lists the JMdict entry of
  every word a card names is the author's writing rule; lint checks only that
  the listed ids exist. From fix 2 the author's `meta_scan.py` (in the
  confirmation packets' `evidence/`) checks it for whole runs of Japanese
  script with a kanji; kana-only and single-kanji words are not checked. It
  finds no gap in this batch. `meta-scan-b134-b136.txt` records 19 such gaps
  in the 31 published cards of batches 134–136, some of them source titles
  (字通, 日本国語大辞典) or verbs in grammar examples. They are not changed
  here; from batch 138 the scan runs before freeze.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder. At `48332d32` they report 0 production, 0 padded-session and
  0 one-holder hits, and 8 latent collisions. One KANJIDIC2 name-only reading is
  disclosed, not fixed: 唯 ゆ on the ユイ prompt in a Starter session that also
  borrows 油 or 輸. Sampled seeds are not exhaustive: GPT notes that 200 seeds
  of the 呂 Starter case drew 71 of its 80 possible wrong readings.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** Fix 2 had two earlier local versions, `0c7f25fe`
  and `fa9be05c`; a GPT confirmation packet built for fix 1 was replaced before
  sending. None of them was reviewed or published.
- Reviewers also read public web pages, such as weblio, Kanjipedia, jisho.org,
  WWWJDIC and KanjiVG; their reports list those reads.

## Validation and accounting

At `48332d32`: 436 host tests pass; validation 0 errors; lint 0 errors and 4
warnings, all on untouched Dictionary lines of existing word articles; quiz
safety 0/0; manifest rebuild unchanged; vocabulary 3201/3336; budget 8,898
entries, 50,747,628 retained and 31,898,933 local-ZIP bytes. `origin/main` is
still `2532beec`, an ancestor, so no integration merge is needed.

After publication, delivery becomes **317/1,228**, with **911 remaining**.
Until the receipt it stays 302/1,228.
