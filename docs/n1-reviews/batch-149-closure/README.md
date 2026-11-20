# Batch 149: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. The reviewed snapshot was merged with the current `origin/main`
without changing any batch file (see "Integration with current main").
Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **翻 翼 脈 腐 臨 臭 興 舌 舎 艶 芝 芽 茂 荘 華**
  (source rows 875, 876, 898, 903, 907, 908, 911, 912, 913, 919, 922, 925,
  928, 934, 941).
- Published base: `090faab2ce29168e9d9bbcee0021e5ecf1d7b798` (the B148 receipt).
- Blind-review freeze: `070b6f694216c7580346cc1b1432519b3284e919`.
- Fix commits, each confirmed or checked before the next was written:
  `b007a0a6` (the review fixes on all fifteen cards and two word articles)
  and `06b2db87bfd9f516f313f63101c40f1fe724f40f` (one distractor on 荘), the
  reviewed snapshot. The fifteen stroke files and fifteen of the seventeen word
  articles are unchanged from the freeze.
- Integration merge: `7f3c0922c7899a4897e975c45ede6414dd727390` (parents
  `06b2db87` and `origin/main` `65b144b3`).
- After the freeze, nine front-matter lists changed and nothing else in front
  matter. `quiz_exclusions`: 腐 gains 甘 and 傷, 興 gains 復, and 茂 gains 密,
  盛 and 豊. `distractors`: 舎 雨 木 山 → 道 京 雨; 芝 犬 石 山 → 田 木 花; 芽 犬
  山 水 → 木 土 雨; 茂 犬 山 水 → 山 川 土; 荘 犬 日 雨 → 校 駅 海; 華 犬 月 水 → 月 天
  川. No title, tag, metadata reading or stroke file changed.

The batch adds fifteen cards and stroke files. Seventeen existing word
articles each gain one link to a new card, and no word article is added. Two
of them also change in one remark each, after the freeze and at a reviewer's
request: the 艶 word article loses the stale sentence "There is no separate 艶
card in the current collection." (GPT G1), and 芝居 quotes 芝 as "turf; lawn,",
the new card's title, instead of "grass; turf," (Claude O11). No existing
kanji card changes. `n1_linkplan.py verify --remarks` and the author's
`kanji_remarks.py` confirm that these are the only changes to existing texts.

## Preliminary round

Before the formal review, an earlier round ran on the first candidate
`0a2d710c`. Its four reviewers were all gpt-6-luna agents: two initial
reviewers ran one after the other (07:00:44-07:07:33 and 07:07:43-07:17:34
UTC), and two confirmations of the fix commit `53664748` ran at the same time
(07:26:21-07:32:26 UTC). The round used one model family, and its
confirmations overlapped, so it does not count as the contract's
two-family serial review. Its four reports are kept verbatim in
[`preliminary/`](preliminary/) as evidence only.

The round found that 翼's "flank" could overlap 側 and that 舌's "speech" could
overlap 話, 言, 語, 詞, 辞 and 弁 (fixed in `53664748` and `5dc936a8`). It also
raised word-quiz overlaps between existing word articles (芝生 and 草, 田舎 and
故郷, optionally 別荘 and 住宅), which are deferred (see Limits). The author
then reworked the batch before the freeze:

- `90582ff0`: every card claim was checked against the pinned sources;
  claims that could not be verified were dropped or rewritten; neighbouring
  titles are quoted exactly. The titles were narrowed to "wing" (翼, so the 側
  exclusion was dropped) and "tongue" (舌, which keeps its speech exclusions
  because the card still documents the speech sense). 臭 gains the exclusion
  怪.
- `174c4675`: Starter distractors for 脈 (目 手 足) and 荘, so that an outside
  reading (脈 ばく, 荘 そ) cannot be offered by a borrowed card.
- `07cda93a`: 腐's distractor 甘 replaced by 煮.
- `070b6f69`: modern-shape mnemonics on all fifteen cards, labelled "not
  etymology", with KanjiVG component evidence added to the packet.

## Review execution

Two reviewer agents, one Claude and one GPT, worked independently. All four
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's report (`RESPONSE.md`), the list of changes
(`CHANGES.md`), the revised cards and the exact diff, and was allowed to read
the original packet and its own family's initial report, and never the other
family's report. Models and times come from the runtime session records, not
from the reports.

| Run | Model | Snapshot | Window, 2026-11-20 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `070b6f69` | 09:10:41-09:35:41 | 112 | 111 | 1 | NEEDS FIX (C1 to C6, all minor) |
| initial-gpt | gpt-6.1-sol | `070b6f69` | 09:37:12-10:00:39 | 91 | 90 | 1 | NEEDS FIX (G1 to G4) |
| confirm-claude | claude-opus-5.5 | `06b2db87` | 10:44:45-10:50:09 | 32 | 32 | 2 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `06b2db87` | 10:50:41-10:58:02 | 41 | 40 | 1 | CONFIRMED |

Both families confirmed the same final commit. `06b2db87` was written before
either confirmation: the author's gates on `b007a0a6` showed that 荘's new
distractors 校 and 京 share the reading キョウ, so one reading-quiz outcome
could leave a wrong slot open for 荘's name-only reading そ, and 京 was replaced
by 駅. `confirm-packet/` holds the two packets (`c1claude`, `c1gpt`; shared
files are stored once in `common/`). `reports/` holds the verbatim reports,
`prompts/` the exact prompts and `scope-audits/` each run's read-scope audit.
`provenance.json` hashes the files with the packets. Raw session logs stay
local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1 and G2: 荘 says the small っ of べっそう comes "after ベツ" | Claude (C1); GPT (G2) | Changed in b007a0a6: the ツ of 別 (ベツ) becomes a small っ before ソウ. Resolved by both |
| C2: "source-only" applied inconsistently and spelled several ways | Claude | Changed in b007a0a6: "source-only here" marks only readings with no checked JMdict word example, the corpus spelling; readings that have one are plain on or kun and say they are not selected for questions. Resolved |
| C3: 豆腐 missing from 腐 | Claude | Changed in b007a0a6: 豆腐 とうふ on the フ row and in Common words (JMdict 1450070). Resolved |
| C4: 艶やか shown only as あでやか | Claude | Changed in b007a0a6: both readings of 艶やか are given, あでやか marked as usually written in kana; JMdict 2682080 added to Metadata. Resolved |
| C5: implausible Starter distractors on 芝 芽 茂 荘 華 and 舎 | Claude | Changed in b007a0a6 to Starter cards from a related field (the six distractor changes listed above); 荘 校 京 海 became 校 駅 海 in 06b2db87. Resolved |
| C6: 翼 quotes an English "help" that the Japanese sources do not print | Claude | Changed in b007a0a6: "list this reading, meaning to help", unquoted. Resolved |
| G1: stale "no separate 艶 card" sentence in the 艶 word article | GPT | Changed in b007a0a6 as a declared word-remark edit. Resolved |
| G3: 興/復, 茂/密 and 茂/盛 overlap without an exclusion | GPT | Changed in b007a0a6: 興 excludes 復, 茂 excludes 密 and 盛, each pair declared once with its glosses in the Notes. Resolved |
| G4: 臨 and 艶 Notes paragraphs of about 240 and 180 words | GPT | Changed in b007a0a6: short reading bullets and an "excluded from meaning choices" list with one reason per group; the same layout on 華 翻 舎 荘 (GPT optional; Claude O9). Resolved |
| O1: author-facing wording in learner prose | Claude | Applied on 臭 and 舎, and 荘's "Do not merge these distinct scopes" dropped |
| O2: the senses of 艶めく overlap | Claude | Applied: described as overlapping; the つやめく row adds "look alluring" |
| O3: possible further exclusions | Claude | Applied where a dictionary supports the overlap: 腐 excludes 甘 (JMdict 甘やかす "to pamper; to spoil") and 傷 (傷む "to be spoiled (e.g. food)"); 茂 excludes 豊 (KANJIDIC2 "be luxuriant"); 興 excludes 復, as under G3 |
| O5: coverage extras | Claude | Partly applied: 山脈, 動脈 and 華やか added; 中華, 芽生える, 新芽, 茂み, 生い茂る, 色艶 and 艶々 not added |
| O6: Metadata ids with no word on the card | Claude | Applied: 脈絡 and 臨床 named on the cards |
| O8: "outside the Jōyō readings" attributed to KANJIDIC2 | Claude | Applied on 脈, and the same misattribution fixed on 翻 |
| O11: 芝居 quotes 芝 as "grass; turf" | Claude | Applied as a declared word-remark edit |
| O12: 脈's ばく is safe only while 目 手 足 fill every slot | Claude | Noted; recorded in the limits |
| O4, O7, O10 | Claude | Not applied (harmless exclusions kept; Metadata format unchanged; no Jōyō ⇔ contrast on 興); accepted in the confirmation |
| GPT optional: rotate repeated distractors; simplify 舎 荘 華 Notes; reword the 舌 contrast; keep the pool boundary in summaries | GPT | Applied with C5 and G4; 舌 now says none of the titles names the tongue, speech or language; the limits keep the pool boundary |
| Confirmation optional: 腐 "kun suffix" against 臭 "kun (suffix)"; 腐 mixes "not selected" and "not selected for questions here"; 舎 雨 and 華 月 天 川 are weak distractors | Claude | Not applied; cosmetic, recorded here |

## Integration with current main

After the reviewed snapshot, `origin/main` moved from the base `090faab2` to
`65b144b3306e72adecf91870cf29a9b21a69433e`: two signed owner commits.
`47ca9f1c` adds 100 onomatopoeia word articles with images, scenes and
grammar drills; `65b144b3` adds `articles/compound-sound-changes.md` and links
it from the README, three articles, the kanji cards 井 and 傑 and the word articles 失敗,
学校 and 花火, whose gemination and rendaku lines now say "corresponds to"
instead of "becomes". Neither commit changes a contract document. Following step
4 of the issue #60 contract, the merge `7f3c0922` (parents `06b2db87` and
`65b144b3`) is a non-rewriting merge. `manifest.json` was the only conflict
and was regenerated with `tools/build_manifest.py` (version
`41accf36d55f0b50`). An earlier local merge with `47ca9f1c` alone (`6f98ae3a`)
was discarded before publication, when main moved again; it was never pushed.

[`integration/merge-proof.json`](integration/merge-proof.json) is produced by
[`integration/merge_proof.py`](integration/merge_proof.py):
`python -X utf8 merge_proof.py <repo> 7f3c0922 merge-proof.json`.

- Of the 48,050 paths compared, every one except the derived `manifest.json`
  equals one parent byte-for-byte.
- The 47 batch runtime files (15 cards, 15 stroke files and 17 word articles)
  equal `06b2db87`, and none was changed by main.
- The regenerated manifest lists all 47 files.
- Of the 116 paths the batch files link to, main changed one, `words/学校.md`.
  It is linked from line 31 of the 校舎 word article, a sentence older than
  the batch, and main changed only its "How the kanji combine" line (the
  gemination wording and the new link); its front matter and title are
  unchanged.
- Two of the 341 files main changed mention a batch kanji or word:
  `articles/numbers-and-counters.md` (腐, inside an existing 豆腐 source link)
  and `words/学校.md` (舎 and 校舎, in an existing line). No line that main
  added mentions one. The 100 main-changed images were counted but not
  scanned.

The strict form of the last two checks ("no link target changed", "no
mention anywhere in a changed file") fails on these older lines, and the
proof records it as `strictPass: false`. `pass: true` applies the two narrower
rules stated in the script: a changed link target passes when no batch line
links it and its front matter is unchanged by main, and a mention passes when it is not
on a line main added. Both results and the line-level details are in the
JSON.

The contract requires a bounded independent review only for changed teaching or
an overlapping substantive conflict. Neither applies here: the reviewed
teaching is byte-identical, main's changes touch no batch file, and the only
conflict is the derived manifest. No integration review was held, as for the
earlier non-overlapping merges in B023, B054, B055 and B141.

Main's new article describes small っ and rendaku as correspondences between
readings. Two reviewed lines use the older wording: 荘 line 23 says the ツ of
別 (ベツ) "becomes a small っ" before ソウ, and 舌 line 43 calls じた "a
context-specific voiced form". Neither links the new article. The owner kept
similar wording on 傑 ("ケツ is shortened to") and added only a link, so this
is not a conflict. The lines were left as confirmed; later batches will use the
"corresponds to" wording and link the article.

Gates on `7f3c0922`: 439 host tests pass; validation 0 errors; lint 0 errors
and the same 3 warnings; manifest rebuild unchanged (SHA-256
`914481BDD6CA98C8C68172485DAEF67DC67042C065263EF682C380D37EC36529`, 9,549
files); budget 9,572 entries, 55,836,799 retained, 56,196,095 inflated and
35,973,776 local-ZIP bytes; vocabulary 3201/3539 (main added 203 prompts).
Every batch audit (lint, quiz safety, reading exposure, reading options, link
plan, kanji remarks, Metadata scan and okurigana scan) is identical to its run
at `06b2db87` apart from the command line.

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The
  `confirm-claude` audit flags one overlapping tool-call start (a shell command
  and a file view started together at 10:45:19.846, maximum two in flight); the
  reviewer disclosed it. The `initial-gpt` audit flags one "recursive shell
  command over packet directories". This is a false positive: the audit's
  pattern matches `**`, and the matched command (09:49:53) used `**` as
  Python exponentiation to sample Bézier curves of the fifteen stroke files; no
  recursive listing ran.
- **Prompts.** Every prompt was saved to a file before use.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists cards as unread that the reports say
  were read (all fifteen in both confirmation audits; nine of fifteen in the
  `initial-gpt` audit, which read them in `Get-Content` loops). The
  confirmations read the changed lines and the cumulative change, and could
  read the original packet and their own family's initial report.
- **Packet errata.** Both confirmation packets' `CHANGES.md` describe all three
  lint warnings as Dictionary lines without a JMdict entry id; for 翻訳 the
  warning is that the article has no Dictionary: line. Neither reviewer relied
  on the difference.
- **Dictionary text.** Several judgments rest partly on live reads of Digital
  Daijisen, Kanjipedia and Jisho pages, not on pinned copies in the packet.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `06b2db87` they report 0
  production, 0 padded-session and 0 one-holder hits and sixteen latent
  collisions, readings that other cards offer but no audited pool can draw:
  翼 たすける, 脈 ばく, 臨 み, 舌 ことば, 舎 さ, 舎 おく, 艶 もろ, 艶 よし, 芽 じ,
  芽 めぐむ, 茂 き, 茂 む, 茂 すぐれる, 荘 そ, 華 わ and 華 げ. The older
  reading-options check reports one problem, 脈 ばく, because it does not model
  curated distractor slots; 脈's three Starter options 目 手 足 fill every wrong
  slot. 脈 ばく and 荘 そ stay safe only while their curated options fill every
  slot, and the curated options on one card must not share a reading. Sampled
  seeds are not exhaustive, and the claim covers the documented shipped pool
  configurations only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. Seven cards quiz only their on reading (翻 ホン,
  脈 ミャク, 臨 リン, 興 キョウ, 舎 シャ, 荘 ソウ, 華 カ) and eight only their kun
  reading (翼 つばさ, 腐 くさ.る, 臭 くさ.い, 舌 した, 艶 つや, 芝 しば, 芽 め, 茂
  しげ.る).
- **Word-quiz overlaps.** 芝生 and 草, 田舎 and 故郷, and 別荘 and 住宅 do not
  exclude each other. These existing word articles change only by a link, so
  the overlaps are pre-existing and deferred.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as such on the cards.
- **Metadata ids.** Fifteen words named on the cards have no JMdict id on the
  Metadata line, because they are cited from Digital Daijisen or Kanjipedia or
  named only for contrast; the cards make no JMdict claim about them (listed
  in the ledger).
- **Lint warnings.** Three Dictionary-line warnings on the existing word
  articles 校舎, 艶 and 翻訳 are older than the batch and out of scope.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The preliminary
  candidate and fixes, the round-2 commits, the freeze and both fix commits
  remain in the history, and every report is kept. A packet built at
  `174c4675` was never sent to a reviewer. The local merge `6f98ae3a` was
  replaced by `7f3c0922` before anything was pushed.

## Validation and accounting

At the reviewed snapshot `06b2db87`: 439 host tests pass; validation 0 errors;
lint 0 errors and 3 warnings (above); quiz safety 0/0; reading options 1
problem (脈 ばく, above); manifest rebuild unchanged (version
`5acf5148433cf390`); vocabulary 3201/3336; link plan 17 links and the 2
declared remark edits, 0 problems; kanji remarks 15 of 15 present, no existing
card modified. Gates at the merge are listed above.

After publication, delivery becomes **497/1,228**, with **731 remaining**.
Until the receipt it stays 482/1,228.
