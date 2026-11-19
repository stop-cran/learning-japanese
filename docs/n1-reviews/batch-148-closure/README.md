# Batch 148: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **絞 継 綱 緊 締 緩 緯 縁 縄 縛 縦 織 繕 繰 罰**
  (source rows 838, 842, 845, 850, 852, 853, 854, 855, 856, 857, 858, 863,
  864, 866, 867).
- Published base: `a0f8d72a8206c24a6fcb81e3a9efec4c94c89bd1` (the B147 receipt).
- Blind-review freeze: `8408b3a5a52cccea74fe2eaf65601568968b6b26`.
- Fix commits, each reviewed or confirmed before the next was written:
  `cc286cc3` (eleven cards: 継 綱 緊 締 緯 縁 縄 縦 織 繕 罰),
  `4162ea2c` (one line each in 締 and 緊) and
  `04900b9ce968180c6ab8a7f271b5c3c80d30e6e8` (one exclusion and its note in
  緊, one line in 締), the reviewed snapshot. 絞 緩 縛 繰, the three changed
  remarks in existing cards (張 慢 修), the seventeen word articles and the
  fifteen stroke files are unchanged from the freeze.
- `origin/main` did not move during the batch (still the B147 receipt
  `a0f8d72a` at closure), so there is no merge and no integration proof.
- After the freeze, five front-matter fields changed, all `quiz_exclusions`
  lists: 緊 (筋 removed), 罰 (犯 removed), 緯 (経 and 織 removed), 綱 (科
  removed) and 縦 (経 added). No title, tag, metadata reading, curated
  distractor or stroke file changed. 緊 briefly had 縛 added (`cc286cc3`) and
  lost it again (`04900b9c`), so its net change is the removal of 筋.

The freeze adds fifteen cards and stroke files. Seventeen existing word
articles each gain one link to a new card, and no word article is added.
Three existing cards (張, 慢, 修) change in one remark each: a sentence that
said the kanji (緊, 緩, 繕) had no card here now links it. `kanji_remarks.py`
and `n1_linkplan.py verify` confirm that these are the only changes to
existing texts besides the seventeen links.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All seven
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
| initial-claude | claude-opus-5.5 | `8408b3a5` | 20:11:23-20:22:40 | 64 | 63 | 1 | minor findings (C1 to C6) |
| initial-gpt | gpt-6.1-sol | `8408b3a5` | 20:23:18-20:44:05 | 67 | 66 | 1 | NEEDS FIX (G1 to G5) |
| confirm-claude-1 | claude-opus-5.5 | `cc286cc3` | 21:00:17-21:06:16 | 44 | 44 | 2 | NEEDS FIX (one new minor finding on 締) |
| confirm2-claude | claude-opus-5.5 | `4162ea2c` | 21:12:22-21:15:12 | 21 | 21 | 2 | CONFIRMED |
| confirm-gpt-1 | gpt-6.1-sol | `4162ea2c` | 21:16:30-21:24:17 | 53 | 52 | 1 | NEEDS FIX (one new minor finding on 緊) |
| confirm2-gpt | gpt-6.1-sol | `04900b9c` | 21:30:18-21:33:58 | 31 | 30 | 1 | CONFIRMED |
| confirm3-claude | claude-opus-5.5 | `04900b9c` | 21:34:08-21:35:57 | 19 | 19 | 2 | CONFIRMED |

The Claude chain is `initial-claude` → `confirm-claude-1` → `confirm2-claude` →
`confirm3-claude`; the GPT chain is `initial-gpt` → `confirm-gpt-1` →
`confirm2-gpt`. Each is a fresh agent of its family. The two families first
confirmed different intermediate commits (Claude `cc286cc3`, GPT `4162ea2c`),
because the GPT packet was built after Claude's first confirmation had led to
`4162ea2c`; the GPT first confirmation then found one more point, which led to
`04900b9c`. Claude's second confirmation covered `4162ea2c`, so Claude
confirmed `04900b9c` in a third round, and both families confirmed the final
commit. `confirm-packet/` holds five packets (`c1claude`, `c1gpt`, `c2claude`,
`c2gpt`, `c3claude`; shared files are stored once in `common/`). `reports/`
holds the verbatim reports, `prompts/` the exact prompts and `scope-audits/`
each run's read-scope audit. `provenance.json` hashes the files with the
packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C2 and G1: 締 does not say what 締 and 切 supply in 締め切り and 締め切る | Claude (C2); GPT (G1) | Changed in cc286cc3: 締 supplies し (め is okurigana) and 切 supplies き (り and る are okurigana). Resolved by both |
| C1 (and optional O-B): 締 "quiz tool" sentence | Claude (C1); GPT (O-B) | Deleted in cc286cc3. Resolved |
| C3: 締 quotes two Daijisen paraphrases | Claude | Changed in cc286cc3: the paraphrases are unquoted and "tie" and "conclude an agreement" are no longer quoted. Resolved |
| C4: 縄 relation to the Daijisen variant | Claude | Changed in cc286cc3: Daijisen, like the Joyo table, prints the traditional form 繩 in brackets. Resolved |
| C5: 織 gloss quoted with a tag | Claude | Changed in cc286cc3: the 織豊時代 gloss is quoted exactly and "historical term" is given as a tag. Resolved |
| C6: 罰 dangling cross-reference | Claude | Changed in cc286cc3: the Daijisen examples are listed and the fragment is a full sentence. Resolved |
| G2: 縁取る okurigana | GPT | Changed in cc286cc3: 縁 supplies ふち, 取 supplies ど and only る is okurigana; JMdict also spells the word 縁どる. Resolved |
| G3: 継 sense 1 reads "take over what follows" | GPT | Changed in cc286cc3: "take over from what came before and carry it on". Resolved |
| G4: association-only exclusions (緊 筋, 罰 犯, 緯 経 and 織, 綱 科) | GPT | Changed in cc286cc3: all removed, with the notes that named them. Resolved |
| G5: 縦 lacks an exclusion against 経 (the warp thread, たていと) | GPT | Changed in cc286cc3: 経 added to the 縦 exclusions and named in the notes. Resolved |
| Remainder of C3, found in confirm-claude-1: 締 line 52 still quotes "bind" | Claude (minor) | Changed in 4162ea2c: 縛's exact title "bind; tie up; restrain," is quoted. Resolved |
| New in confirm-gpt-1: 緊 and 縛 are excluded from each other only by association (the compound 緊縛), and 緊 line 54 asserted an overlap | GPT (minor) | Changed in 04900b9c: 縛 removed from the 緊 exclusions and from the overlap list of line 54; the 緊縛 compound may stay as an example. Resolved. Claude's third round confirmed the removal |
| O1 (Claude initial, optional): add 縛 to the 緊 exclusions | Claude | Applied in cc286cc3, then reversed in 04900b9c on the stricter GPT finding above; Claude's third confirmation accepted the reversal |
| Claude initial, optional O5 (partly), O6, O7 (partly), O8 | Claude | Applied: the raw entry id of 閉める removed; 綱 says short two-kana kun readings (うみ, なつ); the 縦 spelling sentence reworded; the 織 mnemonic speaks of a 戈-like shape |
| Claude initial, optional O2, O3, O4, O5 (限 and 期), O7 (じゅうじく), O9 | Claude | Not applied (the 張 and 慢 remark edits, 紙 on eight cards, harmless 締 exclusions, the 縦軸 reading, extra 繰 compounds); declines accepted in the first confirmation |
| GPT initial, optional O-C | GPT | Applied: 繕 is about mending and putting things in order |
| GPT initial, optional O-A (shorter dense paragraphs), O-D (紙 on eight cards), O-E (綱 wording about 級) | GPT | Not applied; declines accepted in the first confirmation |
| Optional: 筋 should carry its title on 緊 line 56 (Claude, first confirmation) | Claude | Applied in 4162ea2c: "muscle; sinew; line; plot," |
| Optional: 締 line 40 should say める, not め, is the okurigana of しめる (GPT, first confirmation) | GPT | Applied in 04900b9c: "し.める with める as okurigana" (KANJIDIC2's "." marks the okurigana portion) |
| Optional: 縁 line 43 table-row hint; 罰 line 57 wording; 罰 line 58 JMdict ids (Claude, first confirmation) | Claude | Not applied; accepted as polish in the second confirmation |

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The audits of
  `confirm-claude-1`, `confirm2-claude` and `confirm3-claude` each flag one
  overlapping tool-call start (two reads started together, maximum two in
  flight); the audits of `confirm-gpt-1` and `confirm2-gpt` each report one
  path outside the packet and report, a false positive from the
  `review-packets` folder used as a base path in shell commands. The final
  message of `confirm-claude-1` equals its report plus one introductory
  paragraph naming the report file.
- **Prompts.** Every prompt was saved to a file before use. The GPT first
  confirmation used `confirm-gpt-1.txt`, written for the `4162ea2c` packet;
  an earlier prompt written for a `cc286cc3` packet was never sent to an agent.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. Later confirmations covered only the changed lines
  and the cumulative change; they did not re-read the unchanged cards or any
  word article beyond the linked ones.
- **Dictionary text.** Several judgments rest partly on live reads of Digital
  Daijisen, Kanjipedia and Jisho pages, not on pinned copies in the packet.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `04900b9c` they report 0
  production, 0 padded-session and 0 one-holder hits and nine latent
  collisions: 締 むすぶ, 縁 よる, 縁 え, 縁 よし, 縛 いましめる, 縦 はなつ,
  縦 ゆるす, 縦 よし and 繰 くり. The older reading-options check reports 0
  problems. Sampled seeds are not exhaustive, and the claim covers the
  documented shipped pool configurations only.
- **締 reading.** The card quizzes し.める (締める, 締め切り, 締め切る), while an
  automatic alignment of the same words labels them し.まる; the card states
  the choice, and both families accepted it.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as such on the cards where they
  appear. Readings with no declaring word article are listed and illustrated
  but not quizzed.
- **Metadata ids.** Eight compounds named as examples on 罰 line 58 (厳罰
  重罰 賞罰 体罰 懲罰 信賞必罰 神罰 冥罰) have no JMdict id on the Metadata
  line; the card makes no JMdict claim about them (Claude optional, declined).
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  all three fix commits remain in the history, and every report is kept.

## Validation and accounting

At the reviewed snapshot `04900b9c`: 439 host tests pass; validation 0 errors;
lint 0 errors and 3 warnings, all on untouched Dictionary lines of existing
word articles (綱, 緯度, 威張る); quiz safety 0/0; reading options 0
problems; manifest rebuild unchanged (version `8be38471e9994238`);
vocabulary 3201/3336; link plan 17 links, 0 problems; kanji remarks 15 of 15
present, 張 慢 修 the only modified cards.

After publication, delivery becomes **482/1,228**, with **746 remaining**.
Until the receipt it stays 467/1,228.
