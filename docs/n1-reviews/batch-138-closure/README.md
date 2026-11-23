# Batch 138: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **噴 垂 垣 執 堅 塊 墨 壁 壊 奏 契 奨 奪 妨 威**
  (source rows 174, 181, 182, 183, 187, 193, 199, 202, 204, 213, 214, 216,
  217, 226, 230).
- Published base: `e7eb6886e0b05cb84d9b60d268513b316ad71a82`.
- Blind-review freeze: `b6020f9e490298de1756e33c51bf9ce314132f4e`.
- Fix 1: `acf7297ef66a82f620a6c5551d95a2e3fa356bc7` (10 cards).
- Fix 2: `3158b2b97cc9ba61368b722d0c45c37536a909c5` (one line of 契), the
  reviewed snapshot.

The freeze adds fifteen cards and stroke files. Seventeen existing word
articles each gain one link to a new card, and no word article is added. The
existing 張 card's sentence that said 威 had no card now links it. The two fix
commits change only the ten named cards and the generated `manifest.json`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. The two
initial runs ran one after the other and reviewed the same frozen packet
(`packet/`) without seeing each other's work. In each of the two confirmation
rounds both agents ran at the same time, each making its own calls serially.
Each confirmation was a later turn of the same agent. It received a new packet with the author's
statement answering its own previous report (`RESPONSE.md`), the revised cards
and the exact diff, and never the other family's reports. Models and times
come from the runtime session records, not from the reports.

Both reviewers confirmed fix 1. Claude's only optional point, P1, was applied
in fix 2. Before closing, the author found that the reading audits had left
out some extra readings (A1), so both reviewers ran a second confirmation on
fix 2 with corrected audits. `confirm-packet/` holds four packets: `claude` and
`gpt` (fix 1), `claude2` and `gpt2` (fix 2); files they all share are in
`common`.

| Run | Model | Snapshot | Window, 2026-11-18 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `b6020f9e` | 11:01:35–11:12:38 | 94 | 95 | 2 | minor defects (C1–C4) |
| initial-gpt | gpt-6.1-sol | `b6020f9e` | 11:13:24–11:33:22 | 102 | 101 | 1 | NEEDS FIX (minor, G1 and G2) |
| confirm-claude | claude-opus-5.5 | `acf7297e` | 11:56:59–12:00:51 | 31 | 30 | 1 | CONFIRMED (optional P1) |
| confirm-gpt | gpt-6.1-sol | `acf7297e` | 11:57:45–12:06:59 | 38 | 37 | 1 | CONFIRMED (L1) |
| confirm2-claude | claude-opus-5.5 | `3158b2b9` | 12:35:09–12:36:52 | 8 | 7 | 1 | CONFIRMED |
| confirm2-gpt | gpt-6.1-sol | `3158b2b9` | 12:35:09–12:42:00 | 23 | 22 | 1 | CONFIRMED |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 堅 called 硬い and 固い the other two spellings in JMdict's かたい entry, which also lists 緊い | Claude, initial | Changed: 緊い is named as irregular kanji usage |
| C2: 契 said the reading of 契丹 belongs to the whole word, and did not name Kanjipedia's outside readings | Claude, initial | Changed in part: 契 supplies きっ, from キツ; Kanjipedia's キツ and ケツ are named, and JMdict's けいたん. Claude's セツ is not a Kanjipedia reading; it is the reading of Daijisen's proper-name headword せつ【契】, so it is not added; Claude accepted the dispute |
| C3: 妨 gave 妨害 as the only example in Daijisen's character entry | Claude, initial | Changed: 押妨 added, glossed from Daijisen's おうぼう entry |
| C4: 壊's mnemonic said the bottom right is like the lower part of 衣 | Claude, initial | Changed: the right side is 十, 罒 and the full shape of 衣 below it, a modern-shape description rather than Claude's split-衣 etymology |
| G1: no direct 垣–壁 exclusion, although 垣's second sense is "barrier; wall" | GPT, initial | Changed: 壁 added to 垣's exclusions and Notes |
| G2: no direct 奪–魅 exclusion, although 奪う's second sense includes "to charm" | GPT, initial | Changed: 魅 added to 奪's exclusions and Notes |
| 塊–組: 塊's second sense "group; crowd" overlaps 組 "group; assemble" | author, during the fix | Changed: 組 added to 塊's exclusions and Notes; both reviewers checked it |
| O1, O2: 威's frame strokes had their lengths swapped; 威張る was called a native verb although 威 supplies い | Claude, initial | Changed |
| O4, O8: 執り行う for 執 と.る; 功を奏する for 奏 | Claude, initial | Changed, with their JMdict ids (1319610, 2080870) |
| O3: 威's armor-lacing sense of おどし | Claude, initial | Declined: a specialist term, written 威 as ateji (JMdict 2581990), on the second-longest card of the batch; Claude accepted |
| O5–O7: Kanjipedia-only readings (噴 ホン and は.く, 垂 しで, 壁 がけ, 墨 モク, 奪 タツ) | Claude, initial | Declined: each card names every KANJIDIC2 reading and every Daijisen ［音］［訓］ reading; Kanjipedia-only readings are named selectively and all go to the exposure audit; Claude accepted each |
| O9: the reading-options audit labels 噴 ほん and 契 けつ HIT while the exposure audit shows them undrawable | Claude, initial | Not changed, so the audit outputs stay comparable; the tool fix is deferred; Claude accepted |
| OP: move or shorten long sense inventories for phone use | GPT, initial | Declined: it is the collection-wide card layout (the closing Daijisen reference bullet is in 9 batch and 21 published cards); GPT accepted the decline |
| OR: keep the latent collisions as regression cases | GPT, initial | Accepted as practice: they stay in every exposure-audit run and in the limits below. GPT marked it resolved for case retention with eight cases; the corrected audit records nine (A1); its second confirmation marked it resolved again with all nine |
| P1: 契's reading of 契闊 was in katakana (ケッカツ), its other word readings in hiragana | Claude, confirm | Changed in fix 2 to けっかつ; Claude marked it resolved |
| A1: the reading audits in `packet/` and the first confirmation packets left out some extra readings of 垂, 執, 壊, 奏 and 奪 | author, before closure | Audit tools fixed outside the repository; no card change. The corrected audits add one latent collision, 壊 やぶれる; both reviewers marked it resolved, and GPT reproduced the twelve readings the old audits dropped |
| L1: the first confirmation packets said the meaning-quiz audit was unchanged "line for line", but their copy had one blank line fewer | GPT, confirm | Corrected: the packet builder dropped every blank line from the check outputs it summarized; the second packets copy `quiz-safety.txt` byte for byte; GPT marked it resolved after comparing that copy byte for byte with the original packet's |

GPT found both missing exclusions and the "line for line" error; Claude raised
the source-wording points and most of the optional ones. These are contributions to this sample, not
model rankings.

## Limits

- **Execution.** initial-claude had two calls in flight twice (a `view` with a
  `web_fetch`, and two `view` calls); its report discloses only the first.
  Every other run was strictly serial. No GPT report names the exact model; the
  runtime records gpt-6.1-sol. Claude's second report file is titled
  "Batch 138 — second confirmation review", its final message "Batch 138:
  second confirmation review"; the rest is identical, and the file is the
  record.
- **Scope audits.** The audit script does not attribute reads made through
  shell loops over composed paths or through Python, so initial-gpt's audit
  lists all sixteen snapshot cards as unread; the session events show GPT
  printed every card in full through PowerShell loops. The confirmation
  audits show the same gap: confirm-gpt printed the ten changed cards in full
  through PowerShell and read all fifteen through Python; confirm2-claude and
  confirm2-gpt printed 契 in full and compared the other fourteen byte for
  byte. confirm-claude read the ten changed cards in full; its `view` of
  `fix.patch` was refused as too large, as its report says. confirm2-gpt's
  audit flags the `review-packets` folder only because a Python script used it
  as a base path; every file it opened is in its allowed packets and reports.
- **Sources.** Each card mentions every KANJIDIC2 reading and every reading in
  its Daijisen character entry; readings only Kanjipedia lists are mentioned
  selectively. The 押妨 gloss rests on the Weblio page for 押妨 (Digital
  Daijisen and a dictionary of historical terms); 押妨 has no JMdict entry.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. The audits in
  `packet/evidence/audits/` and in the first confirmation packets are
  superseded: a second `--extra` argument for a kanji replaced the first
  instead of adding to it, so eight extra readings of 垂, 執, 壊 and 奏 were
  never checked (A1; `evidence/extras-merge-fix.txt` in `confirm-packet/claude2` and
  `gpt2`).
  The corrected audits are `checks/reading-exposure.txt` and
  `checks/reading-options.txt` in the second packets. At `3158b2b9` they report
  0 production, 0 padded-session and 0 one-holder hits, and 9 latent
  collisions: 噴 ほん and はく, 塊 ほど, 壁 がけ, 壊 やぶれる, 契 きつ, けつ and
  せつ, and 奪 とる. The same command at `b6020f9e` gives the same results. One
  KANJIDIC2 name-only reading is disclosed, not fixed: 執 し on the シツ prompt
  in a Starter session. The reading-options check still labels 噴 ほん and
  契 けつ HIT because it ignores slots that curated distractors fill (O9).
  Neither tool models a custom pool without a target's curated distractor
  cards, where these latent readings could be offered as wrong options.
  壊 fills one of its three kun options from the fallback in every pool,
  because its curated card 塔 has no usable kun reading; in the checked pools,
  higher-ranked fallback readings keep やぶれる out (Claude, second
  confirmation; GPT reproduced this with the Starter cards 出, 話 and 足).
  Sampled seeds are not exhaustive.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** Fix 1 had an earlier local version, `f8f488d1`,
  with a different 押妨 gloss; it was replaced before any confirmation packet
  was built. Fix 2 had an earlier local version, `a93ce9c0`, with the same
  card change and a different commit message. Neither was reviewed or
  published.
- Reviewers also read public web pages, such as Weblio, Kanjipedia, Kotobank,
  jisho.org and kanjiapi.dev; their reports list those reads.

## Validation and accounting

At `3158b2b9`: 436 host tests pass; validation 0 errors; lint 0 errors and 3
warnings, all on untouched Dictionary lines of existing word articles (噴火,
墨, 威張る); quiz safety 0/0; manifest rebuild unchanged; vocabulary
3201/3336; budget 8,928 entries, 50,872,616 retained and 31,959,557 local-ZIP
bytes; the Metadata scan finds no whole-run gap. `origin/main` is
still `e7eb6886`, an ancestor, so no integration merge is needed.

After publication, delivery becomes **332/1,228**, with **896 remaining**.
Until the receipt it stays 317/1,228.
