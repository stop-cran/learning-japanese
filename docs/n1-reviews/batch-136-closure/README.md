# Batch 136: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **炊 焦 異 端 筋 粗 納 脱 膨 致 請 透 鉢 隔 駄**
  (source rows 666, 670, 721, 801, 806, 814, 823, 901, 906, 910, 1022, 1076,
  1121, 1159, 1198).
- Published base: `8563b6fd34be43dcebb1b398e0ca576d3673f41d`.
- Blind-review freeze: `420a6669a2f1dafcc3a237e8b8604ff8cbc4201e`.
- Fix: `7a525b065ee613535c71d559bfc4ce0aea00beb1` (炊 端 粗 請 駄 and the
  word article 透明), the reviewed snapshot.

The freeze adds fifteen cards and stroke files. Thirty-four existing word
articles each gain one link to a new card, and no word article is added. The
fix changes the five named cards and `manifest.json`, and removes one stale
sentence from 透明 (finding G2); that is the batch's only word-article text
change besides the links.

## Review execution

Two reviewer agents, one Claude and one GPT, ran one at a time, Claude before
GPT. Both initial runs reviewed the same frozen packet (`packet/`) without seeing
each other's work. Each confirmation was a later turn of the same agent. It
received a new packet (`confirm-packet/`) with the author's statement answering
its own previous report (`RESPONSE.md`), the revised cards and the exact diff,
and never the other family's reports. Models and times come from the runtime
session records, not from the reports.

| Run | Model | Snapshot | Window, 2026-11-18 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `420a6669` | 00:36:04–00:46:57 | 69 | 69 | 2 | NEEDS FIX (minor, C1) |
| initial-gpt | gpt-6.1-sol | `420a6669` | 00:48:46–01:03:06 | 84 | 83 | 1 | NEEDS FIX (minor, G1–G3) |
| confirm-claude | claude-opus-5.5 | `7a525b06` | 05:59:15–06:02:19 | 15 | 14 | 1 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `7a525b06` | 06:03:25–06:12:07 | 31 | 30 | 1 | CONFIRMED |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1 / G3: 炊く's Kansai "boil" sense was presented as general Japanese | both, initial | Changed: 炊 says JMdict marks that sense as Kansai dialect and names standard 煮る |
| G1: 請 said that 静 has 青 at the right | GPT, initial | Changed: 静 has 青 at the left (KanjiVG 09759 in the confirmation packet) |
| G2: 透明 said there is no 透 card | GPT, initial | Changed: the sentence is removed |
| O1, O3: 駄 においうま; 端 はした | Claude, initial | Partly changed: both Daijisen kun readings added; Kanjipedia-only の.せる and the name reading はじめ not added |
| O5, O6: 粗 kana note; full 雑炊 gloss | Claude, initial | Changed |
| O2, O4, O7, O9, O10: 膨 ホウ; a ノウ word for 納; look-alike meaning distractors; 炊 い; exclusions | Claude, initial | Declined or no change, with reasons; Claude accepted each |
| O8 / LD: 端 はじめ and 致 おこす as drawable wrong answers | Claude, initial | Premise disputed: curated distractors fill every slot of both prompts; Claude accepted |
| O11: link placement in 鉢 | Claude, initial | Declined: every wrap uses the first occurrence in "How the kanji combine"; Claude accepted |
| OA: move source inventories into a reference block | GPT, initial | Declined: a restructure of ten reviewed cards for style; GPT accepted |
| Claude confirm Optional 1: the 炊 title "cook rice; boil" beside the Kansai note | Claude, confirm | Not applied: the title gives the kanji's meaning, and KANJIDIC2 lists "cook; boil"; editorial |
| Claude confirm Optional 2: `checks/quiz-safety.txt` "identical" but one trailing blank line shorter | Claude, confirm (GPT noted the same) | Disclosed here; the content is identical |
| GPT confirm Optional: `checks/unittest.txt` shows "Ran 436 tests" but no "OK" | GPT, confirm | Evidence defect, disclosed under Limits; the full log and a clean rerun at `7a525b06` both show OK |

Both families found the 炊く defect. GPT also found the two wrong statements
about other content (請's 静, 透明's 透 card); Claude raised most of the
source-coverage and wording points. These are contributions to this sample,
not model rankings.

## Limits

- **Execution.** initial-claude had two `view` calls in flight once; every
  other run was strictly serial. GPT's reads through shell and Python are not
  counted in its audit's packet coverage, and its live web fetches went through
  Python `urllib`; the author checked its scope claims against the session
  events. In confirm-gpt those fetches read weblio, the jisho.org API and
  KanjiVG files at the pinned commit `70a0b7ae`. Three of its Python reads
  used the parent `review-packets` folder as a base path, which the audit
  flags; each joined only the two allowed packets. confirm-gpt's report
  names its model only as "GPT (OpenAI; exact runtime model identifier
  unavailable)".
- **Partial confirmation reads.** confirm-claude re-read only the changed cards,
  the changed word article and the diff; it relied on CHANGES.md for the lint
  and other check logs and did not check the O11 placement rule across all 34
  articles. Its report says it re-read 致す live; the session events show that
  fetch in its initial run. confirm-gpt read `KanjiReadings.kt` lines 1–165,
  `Words.kt` lines 205–310 and only the front matter of the ten unchanged
  cards. Both confirmations checked においうま in JMdict only through the
  packet's 駄 family extracts and live jisho.org queries; the author then
  searched the full pinned JMdict (xml sha256 `79f8439e…`) and found no entry
  with においうま.
- **Unit-test evidence.** Both confirmation packets' `checks/unittest.txt`
  ends at "Ran 436 tests" without "OK". PowerShell had turned a blank stderr
  line into a `System.Management.Automation.RemoteException` line, which
  pushed "OK" out of the three-line excerpt. The complete gate log has "OK"
  right after that line, and a rerun at `7a525b06` with stdout and stderr
  captured separately gives "Ran 436 tests … OK". GPT flagged the excerpt;
  no reviewer ran tests.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder. At `7a525b06` they report 0 production, 0 padded-session and
  0 one-holder hits, and 17 latent collisions. Two KANJIDIC2 name-only readings
  are disclosed, not fixed: 炊 い on the スイ prompt in the N1 and All stacks,
  and 納 ろ in a Starter session that also borrows 路. `reading-options.txt`
  still labels 端 はじめ and 致 おこす hits because that older check ignores
  filled slots; both prompts are filled by three curated distractors.
- **Sources.** Each card mentions every KANJIDIC2 reading and every reading
  in its Daijisen character entry; readings only Kanjipedia lists are
  mentioned selectively (in this batch only 脱 タツ).
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- Two bugs in the author's confirmation-packet build script (a non-UTF-8 parse
  and a report path that pointed at the initial report) were caught and the
  packets rebuilt before either reviewer was sent one.
- Reviewers also read public web pages, such as weblio, Kanjipedia and
  jisho.org; their reports list those reads.

## Validation and accounting

At `7a525b06`: 436 host tests pass; validation 0 errors; lint 0 errors and 8
warnings, all on untouched Dictionary lines of existing word articles; quiz
safety 0/0; manifest rebuild unchanged; vocabulary 3201/3336; budget 8,868
entries, 50,636,032 retained and 31,843,464 local-ZIP bytes. `origin/main` is
still `8563b6fd`, an ancestor, so no integration merge is needed.

After publication, delivery becomes **302/1,228**, with **926 remaining**.
Until the receipt it stays 287/1,228.
