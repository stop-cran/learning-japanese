# Batch 140: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with four CLEAN facets and no remaining finding. Publication is
**pending** at this closure commit; the later receipt establishes the remote
commit, CI and served ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **嵐 巣 帳 幕 幣 序 弁 往 径 徐 従 徴 志 怠 恨**
  (source rows 291, 297, 306, 307, 308, 313, 321, 340, 342, 343, 344, 348,
  352, 356, 360).
- Published base: `f37cd97f43e8e2b2792cbe3d89e728c76e453646`.
- Blind-review freeze: `28831314c9b8203cf7dd66c4eec16f23ef0fef22`.
- Fix: `1b24a5f97a396d7121689f3928c7aa500e0054ef` (帳, 幕, 幣, 弁, 径, 徐, 従
  and 徴), the reviewed snapshot.

The freeze adds fifteen cards and stroke files. Twenty-three existing word
articles each gain one link to a new card, and no word article is added. 半径
and 往復 also drop the sentence that said 径 or 往 had no card, and the Notes
bullet of the existing 慢 card that said 怠 and 緩 had no cards now names only
緩. No other existing kanji card changes. The fix changes only the eight named
cards and the generated `manifest.json`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. The two
initial runs ran one after the other and reviewed the same frozen packet
(`packet/`) without seeing each other's work. In the one confirmation round
both agents ran at the same time. Each confirmation was a later turn of the
same agent. It received a new packet with the author's statement answering its
own previous report (`RESPONSE.md`), the list of changes (`CHANGES.md`), the
revised cards and the exact diff, and never the other family's reports.
`confirm-packet/` holds the two packets, `claude` and `gpt`; files they share
are in `common`. The revised cards are not stored again, because they are the
blobs at `1b24a5f9`. Models and times come from the runtime session records,
not from the reports.

| Run | Model | Snapshot | Window, 2026-11-18 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `28831314` | 17:51:39–18:05:08 | 104 | 104 | 2 | NEEDS FIX (minor, C1–C3) |
| initial-gpt | gpt-6.1-sol | `28831314` | 18:06:21–18:26:51 | 63 | 62 | 1 | NEEDS FIX (minor, G1, G2) |
| confirm-claude | claude-opus-5.5 | `1b24a5f9` | 19:05:44–19:09:15 | 27 | 27 | 2 | CONFIRMED (optional O-A) |
| confirm-gpt | gpt-6.1-sol | `1b24a5f9` | 19:05:45–19:14:39 | 27 | 26 | 1 | CONFIRMED (one optional point) |

`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes them with
the packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 幣's distractors 中, "middle, inside," and 内, "within, inner," overlap in meaning, and their link to 幣's shape is thin | Claude, initial; also GPT's Optional 1 | Changed: 内 is replaced by 雨, "rain," a Starter card with a vertical stroke from its top bar through the middle of 冂, and the Notes bullet says so. Claude's suggested 常, 帯 and 希 were not used: none is a Starter card, and a local version with them let a Starter session offer まい on the ヘイ prompt (`confirm-packet/common/evidence/superseded-775debde.txt`). Both reviewers marked it resolved |
| C2: the titles of 徴 and 署 both begin with "sign", and 徴 kept 署 as an ordinary wrong option | Claude, initial | Changed: 署 is added to 徴's quiz exclusions, and the Notes bullet says it is kept out; Claude marked it resolved |
| C3: 帳 and 幕 share a hanging-curtain sense but did not exclude each other | Claude, initial | Changed: 幕 is added to 帳's quiz exclusions, and both cards' Notes say the two are kept out of each other's options; Claude marked it resolved |
| G1: 幕 and 徐 quoted "covering cloth" and "slow, unhurried" as glosses, but neither is a source gloss | GPT, initial | Changed: 幕 now speaks of "the covering-cloth sense in the Daijisen entry" and 徐 of "the slow, unhurried sense", both unquoted; GPT marked it resolved |
| G2: 弁 and 従 put long lists of Daijisen senses (about 378 and 455 words) before the mnemonic and reading table | GPT, initial | Changed: each card sums up its senses in one paragraph, and the full lists move unchanged to a "For reference" bullet at the end of the Notes; GPT marked it resolved |
| O1: 径's example for the path sense, 径庭, "great difference," does not show the path idea | Claude, initial | Changed: the example is 小径 しょうけい, "path; lane," marked formal or literary by JMdict (2859605); 径庭 moves to the reference bullet |
| O2: 幣 did not mention ぜに (Kanjipedia) or にきて (Daijisen) | Claude, initial | Changed: 幣 names both as readings in neither KANJIDIC2 nor JMdict; JMdict writes ぜに as 銭 (2175880), and にきて is also written 和幣 or 幣帛 |
| O3: on 幕's マク reading question the fallback fills two of the three slots | Claude, initial | Not changed: the curated 墓, 暮 and 募 serve the meaning question, and the reading-exposure audit finds no hit or latent collision for 幕 in any pool; decline accepted |
| O4: 弁's title omitted the bento sense of its linked words 弁当 and お弁当 | Claude, initial | Changed: the title is "speech; discern; valve; bento"; four-part titles exist on published cards, and no other card quotes the old title |
| O5: 怠's distractor 治, "govern; heal," brushes against a dated sense of 怠る | Claude, initial | Not changed: the sense belongs to the word, not to 怠's title "neglect; be lazy"; decline accepted |
| Optional 2: 弁護士 would be a more useful example than an esoteric one | GPT, initial | Changed: 弁's summary names 弁護士 べんごし, "lawyer; attorney" (JMdict 1512850) |
| Optional 3: link 徐's dotted reading おもむ.ろに to the spelling 徐ろに | GPT, initial | Changed: 徐 says 徐ろに is the spelling that KANJIDIC2's おもむ.ろに reflects |
| O-A: 弁 says Daijisen's eleven senses fall "in a few main groups", but the groups named cover senses 1–8 | Claude, confirm (optional) | Deferred: the paragraph points to the full list at the end of the Notes; recorded for a later pass |
| Split the long sense-summary paragraphs of 弁 and 従 | GPT, confirm (optional) | Deferred: presentation polish, recorded for a later format pass |

Claude raised the three quiz-option points and most of the optional ones; GPT
raised the quotation and front-loading points and, independently, the weak
distractor set of 幣. These are contributions to this sample, not model
rankings.

## Limits

- **Execution.** Claude's initial and confirmation reports each say every
  response made one tool call, but the session events show one response in
  each run with two parallel `view` calls on adjacent ranges of one packet
  file (`joyo-pages.md` in the initial run, `diffs/fix.patch` in the
  confirmation); both were read-only. The GPT runs were strictly serial. No GPT
  report names the exact model; the runtime records gpt-6.1-sol. The final
  message of initial-claude adds a one-line preface before the report; the
  file is the record. Both GPT runs say they did not open the spool files of
  truncated tool output and reread the passages in bounded output.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python. The session events show:
  - initial-claude viewed all fifteen cards in full, read the changed lines of
    all twenty-four diffs in one PowerShell loop, parsed the stroke files
    structurally and read 慢's changed bullet and the 半径 and 往復 passages
    through PowerShell, so its audit lists 慢, fourteen stroke files, the
    twenty-four diffs and the twenty-three word snapshots as unread.
  - initial-gpt printed all fifteen cards and all twenty-four diffs in full
    through PowerShell loops and analysed the word snapshots, stroke files,
    JMdict and KANJIDIC2 data in Python; its audit lists every card, diff,
    stroke file and word snapshot as unread.
  - confirm-claude viewed 弁 in full and parts of 従, 幣 and 徴, printed 帳
    and 幕 in full and 径 and 徐 from line 17 through PowerShell, and relied on
    `fix.patch` for the seven unchanged cards. Its report says it checked 幣's
    Notes, 徴 line 56 and 従's front matter through the patch and
    `link-targets.tsv`, and did not reopen `QuizBuilder.kt`.
  - confirm-gpt printed the eight changed cards, `fix.patch`,
    `QuizBuilder.kt` and `KanjiReadings.kt` in full through PowerShell,
    replayed `fix.patch` in Python against the original cards and checked the
    other seven cards' front matter there, so its audit lists every packet
    file as unread.
  - initial-gpt's audit flags a recursive scan, but the matched `**` was Python
    exponentiation in a stroke-geometry calculation. confirm-gpt's audit flags
    the `review-packets` folder because a Python script used it as a base path
    to reach its own packets. Both flags are false positives.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `1b24a5f9` they report 0
  production, 0 padded-session and 0 one-holder hits, no drawable KANJIDIC2
  name-only reading, and 4 latent collisions: 幣 まい, 弁 とく, 従 ひろい and
  the name reading 志 じん. The reading-options check labels 幣 まい HIT
  (offered by 埋, 妹, 枚, 毎 and 米) because it ignores slots that curated
  distractors fill; 幣's curated 中, 南 and 雨 are Starter cards and fill every
  reading slot, so it cannot be drawn. Neither tool models a custom pool
  without a target's curated distractor cards. Sampled seeds are not
  exhaustive.
- **Coverage of the old 弁 title.** confirm-gpt did not search the whole
  corpus for quotations of the old title; the author's `git grep` over
  `kanji/`, `words/` and `docs/` at `1b24a5f9` finds none outside the batch.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** The fix had two earlier local versions, `775debde`
  and `88ab6f48`, both amended before any confirmation packet was built and
  both differing only in 幣. The first used the distractors 常, 帯 and 希 (see
  C1); the second had the final distractors but not yet the ぜに and にきて
  sentence. Neither was reviewed or published.
- Reviewers also read public web pages and APIs: Weblio (Digital Daijisen),
  Kanjipedia, jisho.org, kanjiapi.dev (which refused with HTTP 403) and the
  pinned KanjiVG revision on GitHub. The GPT runs made most of these reads
  through Python, so the scope audits list only the `web_fetch` calls; the
  reports describe them.

## Validation and accounting

At `1b24a5f9`: 436 host tests pass; validation 0 errors; lint 0 errors and 4
warnings, all on untouched Dictionary lines of existing word articles (往復,
従姉妹, 直径, 通帳); quiz safety 0/0; manifest rebuild unchanged; vocabulary
3201/3336; link plan 23 links and 2 declared remark edits, 0 problems; budget
8,988 entries, 51,129,062 retained and 32,082,770 local-ZIP bytes; the
Metadata scan finds no whole-run gap. `origin/main` is still `f37cd97f`, the
base, so no integration merge is needed.

After publication, delivery becomes **362/1,228**, with **866 remaining**.
Until the receipt it stays 347/1,228.
