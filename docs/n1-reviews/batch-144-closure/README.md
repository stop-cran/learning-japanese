# Batch 144: textual-review closure

The fifteen cards are textually review-closed. Both final confirmations are
**CONFIRMED**, with no remaining finding. Publication is **pending** at this
closure commit; the later receipt establishes the remote commit, CI and served
ZIP. No JVM, native, device or phone acceptance is implied.

## Snapshot and scope

- Members: **棋 棚 検 概 欄 歓 殊 殻 汁 沖 泡 泣 淡 渇 渋**
  (source rows 558, 559, 564, 571, 582, 587, 589, 592, 596, 601, 608, 609,
  626, 629, 631).
- Published base: `1d262eb60ff8bae674781ce2e7635e002542c36e`.
- Blind-review freeze: `b073abd8f2ab578f29cf2b5e25f36e02fc1aab58`.
- First fix: `2be716f0` (the cards 棋 棚 欄 歓 殻 汁 沖 淡 渋, the existing
  card 討 and the generated `manifest.json`).
- Second fix: `8db07f740a2071609b29539cc1a29e4420bc43e5` (one line each in 欄
  and 棚, and the manifest), the reviewed snapshot. 検, 概, 殊, 泡, 泣 and 渇
  are unchanged from the freeze.
- Merge: `7059712f6fa68717c090c0f091cf6628085d03b5`, a signed merge of
  `origin/main` at `7b48e5da` after review (see "Integration with current
  main").
- No front matter changed in any card; no title, tag, metadata reading,
  curated distractor, quiz exclusion or stroke file changed after the freeze.

The freeze adds fifteen cards and stroke files. Eighteen existing word
articles each gain one link to a new card, and no word article is added. Two
existing texts change in one remark each: the 特殊 article said 殊 had no card
here and now links 殊, and the 討 card said 検 had no card here and now links
検. The fix rewrote the 討 bullet further (C5 below), so the 討 card changes
only in that remark, as `kanji_remarks.py` checks. No other existing kanji
card changes.

There were two confirmation rounds on the Claude side. The first Claude
confirmer (`confirm-claude-1`) reviewed `2be716f0` and found two minor points,
so a second fix commit `8db07f74` was added on top of it (not an amend,
because `2be716f0` had been reviewed). A fresh Claude agent (`confirm-claude`)
then confirmed `8db07f74`. GPT confirmed `8db07f74` once, against the
cumulative change from the freeze. `confirm-packet/` holds three packets: the
round-1 packet for `2be716f0` (`claude`), the round-2 packet for `8db07f74`
(`claude2`) and the GPT packet for `8db07f74` (`gpt`); shared files are stored
once in `common/`.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All five
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's latest report (`RESPONSE.md`), the list of
changes (`CHANGES.md`), the revised cards and the exact diff, and was allowed
to read the original packet and its own family's earlier reports, and never the
other family's reports. The revised cards are not stored again, because they
are the blobs at `8db07f74` (and `2be716f0` for the round-1 packet). Models and
times come from the runtime session records, not from the reports.

| Run | Model | Snapshot | Window, 2026-11-19 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `b073abd8` | 10:05:36–10:19:12 | 74 | 73 | 1 | NEEDS FIX (C1 to C8, all minor) |
| initial-gpt | gpt-6.1-sol | `b073abd8` | 10:19:56–10:39:55 | 73 | 72 | 1 | NEEDS FIX (G1 to G3, all minor) |
| confirm-claude-1 | claude-opus-5.5 | `2be716f0` | 10:51:28–10:57:14 | 34 | 33 | 1 | NEEDS FIX (C7 point 3, one new minor finding F1) |
| confirm-claude | claude-opus-5.5 | `8db07f74` | 11:04:07–11:05:32 | 17 | 16 | 1 | CONFIRMED (one cosmetic optional note) |
| confirm-gpt | gpt-6.1-sol | `8db07f74` | 11:05:45–11:12:57 | 46 | 45 | 1 | CONFIRMED (no optional point) |

`confirm-claude-1` confirms `initial-claude`; `confirm-claude` is the fresh
agent that confirms `confirm-claude-1`'s result; `confirm-gpt` confirms
`initial-gpt`. `reports/` holds the verbatim reports, `prompts/` the exact
prompts and `scope-audits/` each run's read-scope audit.
`provenance.json` hashes the files with the packets. Raw session logs stay
local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 棚 says 氷棚 is the only JMdict ほう word, but 陸棚 りくほう exists | Claude, initial (minor) | Changed: 棚.md:33 names 陸棚 りくほう (also りくだな), "continental shelf", and 氷棚 ひょうほう (JMdict 1551120). Resolved; F1 below followed from it |
| C2: 棚 misreads the Daijisen ▽ mark | Claude, initial (minor); GPT, initial (G2) | Changed: 棚.md:25 writes たな【▽店／棚】 and says the ▽ marks 店, the spelling whose reading is outside the Joyo table, not 棚. Resolved by both |
| C3: 歓 says 権 has a similar-looking left part | Claude, initial (minor); GPT, initial (G1) | Changed: 歓.md:45 says 権 has a part at its right that looks like the left part of 歓. Resolved by both |
| C4: 淡 calls あわ a name-only reading | Claude, initial (minor) | Changed: 淡.md:32 says Daijisen lists あわ in 淡雪 あわゆき (JMdict 1418470) and, separately, the name readings あわし and あわじ. Resolved |
| C5: the rewritten 討 bullet keeps a sentence without a referent | Claude, initial (minor); GPT, initial (O-D, optional) | Changed: 討.md:95 reads "In 検討, 検 supplies ケン and 討 supplies トウ."; the declared remark edit in `kanji-remarks.json` was updated. Resolved by both |
| C6: the 殻 curated distractors 休 本 木 are not plausible wrong answers | Claude, initial (minor); GPT, initial (O-B, optional) | Not changed. They are Starter cards, so they fill all three slots of every 殻 reading prompt and keep 貝 かい (Daijisen かい【▽卵／▽殻】, JMdict 2647520) undrawable (0 production, 0 padded, 0 one-holder hits). Look-alike non-Starter kanji would reopen that exposure, and no Starter kanji looks like 殻. Both reviewers accepted the decline |
| C7: 欄 misquotes the おばしま gloss and calls the bracketed form a compatibility form | Claude, initial (minor) | Point 1 changed (欄.md:42 quotes "handrail; railing; banister; balustrade" and the archaic tag, JMdict 2844081); point 2 (the Daijisen ［訓］おばしま mention) not applied, accepted. Point 3 was first declined; the first confirmer rejected the decline (the table's round-bracketed forms are the Kangxi-dictionary forms, and the siblings say "older form"), and the second fix changed 欄.md:44 to "It prints the older form of 欄 in parentheses; this card does not teach that form separately." Resolved |
| C8: 棋 ご and 沖 ちゅう.する are typed kun without qualification | Claude, initial (minor) | Changed in the table cell only: 棋.md:32 says KANJIDIC2 files ご under kun but Kanjipedia lists ゴ as an on reading; 沖.md:34 says KANJIDIC2 files ちゅう.する under kun but the Joyo table files 沖する under チュウ. The kun type and metadata lists follow KANJIDIC2 and are unchanged. Resolved |
| G3: 殻, 汁 and 渋 bury the reading guidance in unbroken reference paragraphs | GPT, initial (minor) | Changed by splitting only: 殻.md:37 and 39, 汁.md:36, 38 and 40, 渋.md:44, 46 and 48 start a new paragraph at each change of topic; no sourced qualification or example was removed. Resolved |
| F1: 棚 Metadata line lacks JMdict entry 1551120 | Claude, first confirmation (minor, introduced by the fix) | Changed in the second fix: 棚.md:53 ends "…, 1579640, 1499260 and 1551120." The meta scan reports 0 whole-run gaps. Resolved |
| O-A: 棚's Daijisen sense list, the 明 note, the 店 sentence | Claude, initial (optional) | Not applied; the list is a stated selection and the sentences are accurate. Decline accepted |
| O-B: 検's exclusions 点 and 剖 | Claude, initial (optional) | No change: both are real direct pairs (点検, 剖検) and exclusions only remove options. Accepted |
| O-C: 概's "bearing" explanation | Claude, initial (optional) | Not applied; low risk. Accepted |
| O-D: 欄's weak exclusions 井 額 件 条, "form field" | Claude, initial (optional) | No change. Accepted |
| O-E: mention 合歓 on 歓 | Claude, initial (optional) | Not applied; 合歓木 is already listed as a hard-to-read whole word. Accepted |
| O-F: "One example of each:" in 淡 and 渋 (also GPT's 淡 "plain" point, O-C) | Claude, initial (optional); Claude, first confirmation (O-M); GPT, initial (O-C) | Not applied; cosmetic, the bullets are labelled by sense, and the GPT reviewer did not establish that the default quiz confuses 淡 with 原. Declines accepted |
| O-G, O-H, O-I: 渇 and 渋 mnemonic detail; 渇 渇する; 泡 あぶく | Claude, initial (optional) | No change or not applied: the mnemonics carry the modern-shape label, and 渇する and あぶく are not quizzed and are fed to the audits as extra readings. Accepted |
| O-J: a 殻 かい discussion | Claude, initial (optional) | Not applied; the reviewer said leaving it out is acceptable and かい is tracked as a latent collision. Accepted |
| O-K: attribution of "juice" on 汁 | Claude, initial (optional) | Not applied. Accepted |
| O-L: title overlaps 淡/原, 沖/高, 沖/剖 爆 野 開, 汁/渋 | Claude, initial (optional) | No change; the reviewer's judgement matched the author's. Accepted |
| O-A (GPT): a direct 汁–渋 exclusion | GPT, initial (optional) | Not applied: both cards' meaning prompts fill all three distractor slots with curated cards, so neither can draw the other, and no titles display the kakishibu sense. Accepted |
| O-N: say where the older 欄 differs (the part inside 門) | Claude, first confirmation (optional) | Not applied; the card does not teach the older form and the siblings do not describe theirs. Accepted |
| Cosmetic: 欄.md:44 says "in parentheses" while 検, 概, 渋 and 渇 say "in round brackets" | Claude, second confirmation (optional) | Not applied, because any card change needs a new commit, a gate run and another confirmation round for wording that is not wrong. Recorded for a later pass |

Claude raised all eight initial findings and twelve optional points; GPT
independently raised the 歓 side of 権, the 棚 ▽ mark and the 討 bullet, and
alone raised the three dense reference paragraphs. Only Claude's first
confirmer found the 欄 "compatibility form" and 棚 Metadata points. These are
contributions to this sample, not model rankings.

## Integration with current main

`origin/main` moved after review. The owner's signed commit `7b48e5da`
("Clarify common word-initial reading of 手", 2026-11-19 10:07 UTC) changed
`kanji/手.md` and `manifest.json` only. The signed merge `7059712f` has the
reviewed snapshot `8db07f74` as its first parent and `7b48e5da` as its second.
The only conflict was the derived `manifest.json`, which was regenerated with
`tools/build_manifest.py`. Relative to `8db07f74` the merge changes only
`kanji/手.md` and the manifest.

`integration/merge_proof.py` and `integration/merge-proof.json` show
mechanically that every non-derived path equals one parent byte for byte (46,700
paths compared, none unmatched), that none of the 49 batch runtime paths or
280 link targets was changed by main, that no main-changed non-derived file
mentions a batch kanji or word, and that the manifest lists every batch file.
No teaching text changed and no substantive conflict arose, so under the issue
#60 contract no integration review was needed. The gates were rerun on
`7059712f`: the quiz-safety, reading-exposure, reading-options and meta-scan
outputs are line for line identical to those at `8db07f74` apart from the
command lines.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family, so it had no memory of its own earlier reading. The two Claude
  confirmers are different agents: `confirm-claude` did not see
  `confirm-claude-1`'s reasoning, only its report and the author's answer. The
  confirmations of the two families are independent of each other.
- **Execution.** Every run was serial, with one tool call in flight. No GPT
  report names the exact model; the runtime records gpt-6.1-sol. initial-gpt's
  audit flags one recursive shell command over packet directories.
  confirm-gpt's audit reports one path outside the packet
  and report, a false positive from the packet-root folder used as a base-path
  variable in its shell commands. The other three runs have no flag. All five
  reports equal the runs' final messages.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. The second Claude confirmation covered only the two
  changed lines, and the GPT confirmation the cumulative change; neither
  re-read the unchanged cards or any word article.
- **Reviewers' own limits.** The meaning of the round-bracketed forms
  (いわゆる康熙字典体) rests on a secondary source that quotes note 6 of the Joyo
  table, because the official PDF fetch timed out. Neither reviewer ran a JVM
  or Android build or could certify the pool construction beyond the supplied
  audits.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `8db07f74` and at the merge
  they report 0 production, 0 padded-session and 0 one-holder hits, one
  labelled reading option (殻 かい from 貝, not drawable) and six latent
  collisions: 欄 わく (惑); 歓 ぶ, a KANJIDIC2 name reading (不 分 夫 武 歩 舞 豊
  部); 殊 け (化 家 希 怪 気 花); 殻 かい (貝); 沖 とぶ (飛); and 沖 むなしい (空).
  The first gate run showed 殻 かい drawable and one one-holder padded hit,
  because the original distractors 段, 投 and 役 are not Starter cards; they
  were replaced by the Starter cards 休, 本 and 木 before review. No quiz-option
  or reading-exposure line changed between the freeze and the fixes apart from
  the command lines. Sampled seeds are not exhaustive.
- **Source-only readings.** Disclosed on the cards: 欄 てすり (おばしま 2844081
  is mentioned, not added), 殻 コク and バイ, 沖 わく, 渋 シュウ and 泡
  発泡 ぽう; 滞 has no card, so 渋 names it as plain text. 泡 and 淡 share
  淡雪/泡雪 あわゆき (1418470), and 汁 and 渋 may share a kakishibu overlap;
  neither pair is excluded.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  both fix commits remain in the history; the reports of both Claude
  confirmers are kept.

## Validation and accounting

At the merge `7059712f`: 439 host tests pass; validation 0 errors; lint 0
errors and 3 warnings, all on untouched, wrapped Dictionary lines (戸棚, 淡水,
特殊); quiz safety 0/0; manifest rebuild unchanged (version
`6147644f9beaec4c`); vocabulary 3201/3336; link plan 18 links and 1 declared
remark edit, 0 problems; kanji remarks 15 of 15 present, 討 the only modified
card, 0 problems; budget 9,110 entries, 51,640,720 retained, 51,999,811
inflated and 32,337,989 local-ZIP bytes; the Metadata scan finds no
whole-run gap.

After publication, delivery becomes **422/1,228**, with **806 remaining**.
Until the receipt it stays 407/1,228.
