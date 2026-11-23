# Batch 146: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **煮 熟 牧 狂 狭 献 玄 環 甚 癖 益 盛 盾 眺 睡**
  (source rows 672, 675, 682, 685, 688, 692, 698, 715, 716, 730, 735, 736,
  741, 745, 747).
- Published base: `ffbf576ee0531e56f8f36e0a7287b53f443b0d29` (the B145 receipt).
- Blind-review freeze: `38833c7f58bdd2406dbb808c6b2a74257ef29f12`.
- Fix commits, each reviewed or confirmed before the next was written:
  `5e61ef07` (the nine cards 煮 熟 牧 玄 甚 癖 益 盛 睡 and the manifest),
  `872d6502` (甚, 牧, 盛), `09e376bd` (牧), `8d16c582` (牧), `d276f63b` (牧) and
  `1c941a7a15e9eb53179d4fe37b596dc97c14b1f6` (牧 again), the reviewed
  snapshot. 狂 狭 献 環 盾 眺 and the changed 潔 remark are unchanged from the
  freeze.
- `origin/main` did not move during the batch (still the B145 receipt
  `ffbf576e` at closure), so there is no merge and no integration proof.
- After the freeze only one front-matter field changed: the 牧
  `quiz_exclusions` list (17 at the freeze, 12 at the end, see below). No
  title, tag, metadata reading, curated distractor or stroke file changed.

The freeze adds fifteen cards and stroke files. 皇 (row 731) and 眼 (row 746)
are skipped because their only declaring articles (天皇, 眼鏡) align none of
their KANJIDIC2 readings; 睡 (row 747) is the fifteenth member instead. Twenty-three
existing word articles each gain one link to a new card, and no word article is
added. One existing card, 潔, changes in one remark (it said 癖 in 潔癖 had
no card and now links 癖); `kanji_remarks.py` and `n1_linkplan.py verify`
confirm that this is the only change to an existing text besides the
twenty-three links.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All eleven
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
| initial-claude | claude-opus-5.5 | `38833c7f` | 15:14:35-15:26:42 | 69 | 68 | 1 | NEEDS FIX (C1 to C9) |
| initial-gpt | gpt-6.1-sol | `38833c7f` | 15:27:16-15:47:10 | 85 | 84 | 1 | NEEDS FIX (G1 to G3) |
| confirm-claude-1 | claude-opus-5.5 | `5e61ef07` | 16:01:17-16:06:13 | 32 | 31 | 1 | NEEDS FIX (one new finding on 甚) |
| confirm2-claude | claude-opus-5.5 | `872d6502` | 16:13:52-16:15:40 | 16 | 15 | 1 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `872d6502` | 16:15:50-16:23:02 | 45 | 44 | 1 | NEEDS FIX (G3 and one new finding on 牧) |
| confirm3-gpt | gpt-6.1-sol | `09e376bd` | 16:30:39-16:36:05 | 29 | 28 | 1 | NEEDS FIX (坊) |
| confirm4-claude | claude-opus-5.5 | `8d16c582` | 16:40:31-16:43:41 | 17 | 16 | 1 | NEEDS FIX (僧 against 坊) |
| confirm5-claude | claude-opus-5.5 | `d276f63b` | 16:49:48-16:51:55 | 10 | 9 | 1 | CONFIRMED |
| confirm5-gpt | gpt-6.1-sol | `d276f63b` | 16:52:13-16:57:21 | 28 | 27 | 1 | NEEDS FIX (restore 僧) |
| confirm6-claude | claude-opus-5.5 | `1c941a7a` | 17:03:00-17:05:05 | 15 | 14 | 1 | CONFIRMED |
| confirm6-gpt | gpt-6.1-sol | `1c941a7a` | 17:05:24-17:09:04 | 29 | 28 | 1 | CONFIRMED |

The Claude chain is `initial-claude` → `confirm-claude-1` → `confirm2-claude`
→ `confirm4-claude` → `confirm5-claude` → `confirm6-claude`; the GPT chain is
`initial-gpt` → `confirm-gpt` → `confirm3-gpt` → `confirm5-gpt` →
`confirm6-gpt`. Each is a fresh agent of its family. Packets for later rounds
were built for the family whose finding the previous fix answered, and the
other family's packet was built only when that family had to confirm; so the
two families confirmed different intermediate commits, and both confirmed the
final one. `confirm-packet/` holds nine packets (`c1claude`, `c2claude`,
`c1gpt`, `c3gpt`, `c4claude`, `c5claude`, `c5gpt`, `c6claude`, `c6gpt`; shared
files are stored once in `common/`). Two packets that were built but never
launched (`confirm3-146-claude`, `confirm4-146-gpt`) are not part of the record.
`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes the files
with the packets. Raw session logs stay local because they may hold private
context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 甚 teaches the okurigana of 甚だしい wrongly | Claude (C1, major); GPT (G1, minor) | Changed: 甚 writes はなは and だしい is okurigana, likewise 甚だ; the aligner wording was removed. The first confirmation found the cell on the はなは.だ row still contradictory, so 872d6502 states that はなは.だしい shares the stem はなは with はなは.だ and is not selected separately. Resolved by both families |
| C2: ジン and ヘキ labelled "source-only" | Claude (C2); GPT (O-B) | Changed: plain `on` in 甚 and 癖; "no word article yet" kept. Resolved |
| C3: 益体 as whole-word reading | Claude (minor) | Changed: 益体 is 益 ヤク + 体 タイ; only 益荒男 is whole-word. Resolved |
| C4: 煮凝り as whole-word reading | Claude (minor) | Changed: 煮凝り is に + こごり. Resolved |
| C5: 熟 "linked words" | Claude (minor); GPT (O-C) | Changed: 熟語 is the linked word; 熟練 and 熟慮 are "examples without word articles". Resolved |
| C6: 玄 "cap stroke" | Claude (minor) | Changed: "two-stroke lid". Resolved |
| C7 and G2: 癖 sound statements | Claude (minor); GPT (G2) | Changed: ぐせ "often becomes"; 手癖 てくせ or てぐせ; 難癖 keeps くせ; ペキ after the small っ; the 潔 card links back. Resolved by both |
| C8: 牧 title "pastor", kana, exclusions | Claude (minor) | Changed: kana for 牧童 and 牧羊; five exclusions without support in a displayed label (治 御 官 司 導) removed in 5e61ef07 (see the 牧 exclusion history below); title kept (牧師 is the Joyo example and Daijisen's second sense is 人々を治め導く). Decline of the title accepted |
| C9: 盛ん filed under さか.る | Claude (minor) | Changed: 盛ん is on the さか.ん row, which shares the stem さか with さか.る. Resolved |
| G3: 牧 exclusions 牛 馬 羊 | GPT (minor) | Kept at first (牛 馬 羊 草 stayed through 5e61ef07 and 872d6502); removed in 09e376bd, with 草 (see the history below). Resolved |
| New in confirm-gpt: removing 治 and 御 was not justified, because Daijisen gives 牧 the sense 人々を治め導く and the 治 and 御 titles show "govern" | GPT (minor, introduced by the fix) | Changed in 09e376bd: 治 御 官 司 導 restored. Resolved |
| New in confirm3-gpt: 坊 "Buddhist priest; boy" is not a meaning of 牧 | GPT (minor) | Changed in 8d16c582: 坊 removed. Later see 僧 |
| New in confirm4-claude: excluding 僧 but not 坊 is inconsistent | Claude (minor) | Changed in d276f63b: 僧 removed too (Claude's alternative remedy) |
| New in confirm5-gpt: Daijisen's 僧 entry also gives the general sense 聖職者 (clergy) and the word entry's sense 2 covers Catholic monks, so 僧 overlaps "pastor"; 坊 stays out | GPT (minor) | Changed in 1c941a7a: 僧 restored; 牧.md:54 says 僧 has the general clergy sense and 坊 only means a Buddhist priest or a boy, so it is not excluded. Confirmed by both families |
| C-O1 to C-O9 (Claude initial, optional) | Claude | O1 jargon applied in 煮 甚 盛 睡; the rest (kana in Notes, 玄孫, 狭霧, reading-exposure labels, 環/鳴, 眺/相, 癖 exclusions, 眺める link) declined and accepted |
| O-A (GPT, shorten audit explanations) | GPT | Aligner sentences removed; exclusion inventories kept. Decline accepted |
| 牧.md l.26 label and l.53 miscount (Claude, optional, first confirmation) | Claude | Applied: l.26 reads "Govern and guide people"; l.53 reads "Kanji related to the first sense…" |
| 盛 duplicated "thriving" (Claude, optional) | Claude | Applied |
| 甚 l.34 long cell; 牧 "nine kanji" wording (Claude, second confirmation, optional) | Claude | Applied or moot after the 牧 rewrites |
| Optional: 掌 府 公 as other possible overlaps (Claude, fourth confirmation) | Claude | No change; exclusions are direct pairs |
| Optional: a clause on why 師 overlaps 牧 (Claude, fifth confirmation) | Claude | Not applied; defensible without it |
| Optional: l.54 "only a Buddhist priest or a boy" is not exhaustive for 坊; a link to the Daijisen 僧 entry (Claude, sixth confirmation) | Claude | Not applied; recorded |
| Remedy note (Claude, sixth confirmation) | Claude | If 坊 is ever wanted excluded too, it is an editorial one-word addition; both families judged the final list defensible |

### 牧 exclusion history

The 牧 `quiz_exclusions` list changed through six states, which this record
keeps in full because the two reviewers' views differed:

| Commit | List | Change |
|---|---|---|
| `38833c7f` freeze | 17: 畜 養 育 農 牛 馬 羊 草 野 僧 坊 治 御 官 司 導 師 | |
| `5e61ef07`, `872d6502` | 12: 畜 養 育 農 牛 馬 羊 草 野 僧 坊 師 | five governance entries removed |
| `09e376bd` | 13: 畜 養 育 農 野 僧 坊 治 御 官 司 導 師 | 牛 馬 羊 草 removed, governance entries restored |
| `8d16c582` | 12: 畜 養 育 農 野 僧 治 御 官 司 導 師 | 坊 removed |
| `d276f63b` | 11: 畜 養 育 農 野 治 御 官 司 導 師 | 僧 removed |
| `1c941a7a` final | 12: 畜 養 育 農 野 僧 治 御 官 司 導 師 | 僧 restored |

The principle that both families accepted at the end: an exclusion needs a
direct overlap between a displayed label (or a dictionary sense of the other
kanji) and a taught sense of 牧. Exclusions are symmetric, direct and not
transitive, and they can only remove wrong options, so none of the changes
created a second correct answer. 僧 is excluded and 坊 is not because
Daijisen's 僧 entry gives a general clergy sense, like the "clergyman" of 牧師,
while 坊 reaches clergy only through 僧. Claude judged the two alike in the
fourth confirmation and accepted the final state in the sixth; GPT asked for 僧
in the fifth and confirmed in the sixth.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended, with one tool
  call in flight at a time. The audit of `initial-claude` flags a temporary
  script it created and deleted inside `reports-146` and a temporary file it
  removed; `confirm5-gpt` wrote its report through a relative `apply_patch`
  path to the report file; four GPT audits report one path outside the packet
  and report, a false positive from the `review-packets` folder used as a base
  path in shell commands. No GPT report names the exact model; the runtime
  records gpt-6.1-sol. Every report equals its run's final message.
- **Prompts.** The prompts of `confirm3-gpt` and `confirm4-claude` were given
  inline and were recovered from the runtime session record afterwards, not from
  a saved file.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards and other files as unread that the
  reports say were read. Later confirmations covered only the changed lines
  and the cumulative change; they did not re-read the unchanged cards or any
  word article beyond the linked ones.
- **Dictionary text.** The 僧 and 牧 judgments in the last rounds rest partly
  on Digital Daijisen text read live on Weblio, not on a pinned copy in the
  packet.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `1c941a7a` they report 0
  production, 0 padded-session and 0 one-holder hits and ten latent
  collisions, counted per quiz prompt (nine distinct card-and-reading pairs):
  牧 ま, まい and もく; 狂 ふれる; 狭 せ; 甚 じ and いたい; 益 よう; 盛 もり (for
  both prompts). Sampled seeds are not exhaustive.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as source-only on the cards where
  they appear (狭 コウ; 献 たてまつ.る; 玄 くろ.い). Readings with no declaring
  word article are listed and illustrated but not quizzed.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  all six fix commits remain in the history, and every report is kept.

## Validation and accounting

At the reviewed snapshot `1c941a7a`: 439 host tests pass; validation 0 errors;
lint 0 errors and 3 warnings, all on untouched, wrapped Dictionary lines (煮る,
矛盾 and 不潔); quiz safety 0/0; reading options 0 problems; manifest rebuild
unchanged (version `efe2d5ed43c194e2`); vocabulary 3201/3336; link plan 23
links, 0 problems; kanji remarks 15 of 15 present, 潔 the only modified card;
budget 9,170 entries, 51,901,020 retained, 52,260,111 inflated and 32,462,067
local-ZIP bytes.

After publication, delivery becomes **452/1,228**, with **776 remaining**.
Until the receipt it stays 437/1,228.
