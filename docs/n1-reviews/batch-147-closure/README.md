# Batch 147: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **瞬 瞳 矢 砕 礎 秀 秘 稚 稼 稿 穏 穴 笛 粋 糧**
  (source rows 750, 752, 754, 756, 767, 776, 777, 784, 787, 788, 791, 794,
  803, 813, 818).
- Published base: `d97126fe54f7c060df157b933736c71e4f2caed9` (the B146 receipt).
- Blind-review freeze: `6a2323e759d4e4f2e78bc039c8b9eb8914ac2d0c`.
- Fix commits, each reviewed or confirmed before the next was written:
  `0df56686` (the cards 矢 砕 礎 秀 秘 稚 穏 粋 and the manifest),
  `99487bb5` (穏 稚 糧 穴 and 秀) and
  `886671da825c2da9ccbbf34506cf0b7747d7804c` (穏 and 稚, one line each), the
  reviewed snapshot. 瞬 瞳 稼 稿 笛, the three changed remarks in existing
  cards (基 密 透) and the three in existing word articles (矢印 砕く
  砕ける) are unchanged from the freeze.
- `origin/main` did not move during the batch (still the B146 receipt
  `d97126fe` at closure), so there is no merge and no integration proof.
- After the freeze, five front-matter fields changed, all `quiz_exclusions`
  lists: 矢 (方 恋 念 removed), 砕 (単 易 簡 悩 removed), 稚 (熟 removed),
  糧 (貯 備 removed) and 穴 (秘 added). No title, tag, metadata reading,
  curated distractor or stroke file changed.

The freeze adds fifteen cards and stroke files. Eighteen existing word
articles each gain one link to a new card, and no word article is added.
Three existing cards (基, 密, 透) and three existing word articles (矢印,
砕く, 砕ける) change in one remark each: a sentence that said the kanji had no
card here now links it or says it has one. `kanji_remarks.py` and
`n1_linkplan.py verify` confirm that these are the only changes to existing
texts besides the eighteen links.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All five
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's latest report (`RESPONSE.md`), the list of
changes (`CHANGES.md`), the revised cards and the exact diff, and was allowed
to read the original packet and its own family's earlier reports, and never the
other family's reports. Models and times come from the runtime session
records, not from the reports.

| Run | Model | Snapshot | Window, 2026-11-19 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `6a2323e7` | 18:17:23-18:28:50 | 72 | 71 | 1 | NEEDS FIX (C1 to C7) |
| initial-gpt | gpt-6.1-sol | `6a2323e7` | 18:31:45-18:49:12 | 64 | 63 | 1 | NEEDS FIX (G1 to G6) |
| confirm-claude-1 | claude-opus-5.5 | `99487bb5` | 18:57:01-19:02:04 | 28 | 28 | 2 | NEEDS FIX (one new finding on 穏) |
| confirm-gpt | gpt-6.1-sol | `886671da` | 19:06:37-19:14:19 | 47 | 46 | 1 | CONFIRMED |
| confirm2-claude | claude-opus-5.5 | `886671da` | 19:14:31-19:16:43 | 15 | 14 | 1 | CONFIRMED |

The Claude chain is `initial-claude` → `confirm-claude-1` →
`confirm2-claude`; the GPT chain is `initial-gpt` → `confirm-gpt`. Each is a
fresh agent of its family. The Claude confirmation of `99487bb5` was built
before the 穏 line 25 finding was fixed, so the two families confirmed
different intermediate commits, and both confirmed the final one.
`confirm-packet/` holds three packets (`c1claude`, `c1gpt`, `c2claude`; shared
files are stored once in `common/`). `reports/` holds the verbatim reports,
`prompts/` the exact prompts and `scope-audits/` each run's read-scope audit.
`provenance.json` hashes the files with the packets. Raw session logs stay
local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1 and G1: 秀 mnemonic places 禾 and 乃 left and right | Claude (C1); GPT (G1) | Changed in 0df56686: 禾 on top, 乃 below. Resolved by both |
| C2 and G2: 粋 mnemonic names the full 卒 | Claude (C2); GPT (G2) | Changed in 0df56686: a shape like 九 above 十 (simplified 卒), and 卒 itself is not written in 粋. Resolved by both |
| C3 and G3: 稚 okurigana split | Claude (C3); GPT (G3) | Changed in 0df56686: 稚い is いとけな + い and 稚けない the いとけ split. Resolved by both |
| C4: 矢 has no vertical stroke | Claude | Changed in 0df56686: the mnemonic and the distractor note speak of a long sweeping stroke and crossing bars. Resolved |
| C5: quoted titles in 礎 and 砕 are not exact | Claude | Changed in 0df56686: "grove; woodland" and "perish; destroy; die out". Resolved |
| C6: over-broad exclusions on 矢 and 砕 | Claude | Changed in 0df56686: 方 恋 念 removed from 矢; 単 易 簡 悩 removed from 砕. Resolved |
| C7: 穏 distractor reason | Claude | Changed in 0df56686: the three Starter distractors fill every wrong slot of the おだ.やか question. Resolved |
| G4: 穏 attributes the 温和 climate sense to 穏和 | GPT | Changed in 99487bb5: 穏和 carries the personality and statement senses; the climate sense is written 温和 only (JMdict 1589620 sense restrictions). Resolved |
| G5: unjustified exclusions (矢 恋 念, 稚 熟, 糧 貯 備) | GPT | Changed: 矢 恋 念 removed in 0df56686; 稚 熟 (an antonym) and 糧 貯 備 (association) removed in 99487bb5. Resolved |
| G6: 穴 cites the sense "well-kept secret" but does not exclude 秘 | GPT | Changed in 99487bb5: 秘 added to the 穴 exclusions, with a Notes sentence. Resolved |
| New in confirm-claude-1: 穏 line 25 lists Daijisen's examples without 静穏 | Claude (minor) | Changed in 886671da: "include" and 静穏 added; 稚 line 40 reads "the JMdict spelling 稚けない". Resolved |
| C-O1 and C-O3 (Claude initial, optional) | Claude | Applied: 砕 quoted translation, 秘 ひそ.か labelled "outside the official table" |
| C-O2, C-O5, C-O6, C-O7 (Claude initial, optional) | Claude | Not applied (矢 無理矢理 and 矢張り, 穴 JMdict 1254490 tags, 礎 title in the 基 remark, 純粋 article); declines accepted in the first confirmation |
| C-O4 (穏 line 25 list and 温和 heading) | Claude | 温和 stated in 99487bb5; the list wording fixed in 886671da. Resolved |
| G-O-B (秀 "reading overlap" wording) | GPT | Applied in 99487bb5: the overlap is of the meaning of すぐれる |
| G-O-A, G-O-C (GPT, shorter reference text; 基 sentence about 礎) | GPT | Not applied; declines accepted |
| Optional: 矢 "long sweeping stroke" wording; 穴/秘 exclusion asymmetry against the removed 矢 exclusions; 粋 reading prompt can show メエトル from 米 (Claude, first confirmation) | Claude | Not applied; accepted as polish or harmless in the second confirmation |
| Optional: kana readings せいおん (and あんのん) for 静穏 on 穏 line 25; JMdict id 1381850 for 静穏 in the Metadata line (Claude, second confirmation) | Claude | Not applied; recorded. The card makes no JMdict claim about 静穏 |

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The audit of
  `confirm-claude-1` flags one overlapping tool-call start (maximum two in
  flight); the audit of `confirm-gpt` reports one path outside the packet and
  report, a false positive from the `review-packets` folder used as a base
  path in shell commands. `initial-claude` edited its own report twice after
  creating it. No GPT report names the exact model; the runtime records
  gpt-6.1-sol. Every report equals its run's final message.
- **Prompts.** The prompt of `confirm-gpt` was given inline and was saved to a
  file afterwards with the same text.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. Later confirmations covered only the changed lines
  and the cumulative change; they did not re-read the unchanged cards or any
  word article beyond the linked ones.
- **Dictionary text.** Several judgments rest partly on live reads of Digital
  Daijisen, Kanjipedia and Jisho pages, not on pinned copies in the packet.
  The GPT confirmation notes that the 砕 and 悩 exclusion removal depends on
  the 悩 sense of 砕ける (JMdict 1295190) being classical; no exclusion was
  added for it.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `886671da` they report 0
  production, 0 padded-session and 0 one-holder hits and seven latent
  collisions: 矢 さ, 秀 ほ, 稚 わく, 稼 うえる, 穏 やすらか, 穴 しし and
  笛 う. The older reading-options check reports one problem, the 穏 prompt
  おだ.やか with やす.らか (held by 安) as a fallback candidate; the curated
  distractors 木 田 花 fill every wrong slot in every checked pool, so it
  cannot be drawn (the 穏 Notes say so). Sampled seeds are not exhaustive, and
  the claim covers the documented shipped pool configurations only.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as such on the cards where they
  appear. Readings with no declaring word article are listed and illustrated
  but not quizzed.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  all three fix commits remain in the history, and every report is kept.

## Validation and accounting

At the reviewed snapshot `886671da`: 439 host tests pass; validation 0 errors;
lint 0 errors and 2 warnings, both on untouched Dictionary lines of existing
word articles (瞳, 透明); quiz safety 0/0; reading options 1 known problem
(the 穏 artifact above); manifest rebuild unchanged (version
`6802b2c496df99d7`); vocabulary 3201/3336; link plan 18 links, 0 problems;
kanji remarks 15 of 15 present, 基 密 透 the only modified cards.

After publication, delivery becomes **467/1,228**, with **761 remaining**.
Until the receipt it stays 452/1,228.
