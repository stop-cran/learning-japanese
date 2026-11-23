# Batch 154: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. `origin/main` had not moved from the published base when the review
closed, so publication is a fast-forward and no integration merge is needed.
Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **随 隠 隣 雄 雷 霧 項 顕 飼 飽 飾 驚 鬼 鮮 黙**
  (source rows 1158, 1161, 1162, 1165, 1171, 1176, 1182, 1188, 1192, 1193,
  1194, 1205, 1207, 1213, 1230).
- Published base: `45de81cd99a8dc310f10eeafffa7f7495a3f6fe0` (the B153 receipt).
- Blind-review freeze: `f8f3db8c9ae7d88d72cdc3d8eaae84c8f736ca5f`.
- Fix commit: `e5c945d6d3f83b97145100528e448747424fded5`, the reviewed
  snapshot. It changes seven of the fifteen cards (随 隣 雄 項 飽 飾 黙) and
  the derived `manifest.json`. 隠 雷 霧 顕 飼 驚 鬼 鮮, the existing cards 塊,
  微 and 鏡 with their remark edits, the fifteen stroke files and the nineteen
  word articles are unchanged from the freeze.
- After the freeze, only two `quiz_exclusions` lists changed in front matter:
  随 gained 追, and 隣 gained 辺 and 側. No title, tag, distractor list,
  metadata reading, quizzed reading or stroke file changed.

The batch adds fifteen cards and stroke files. Nineteen existing word articles
each change in one line, which gains a link to a new card (新鮮, 随筆, 隠す,
隠れる, 隣, 雄勁, 雷, 霧, 項目, 顕微鏡, 飼う, 飽きる, 飽くまで, 飾り, 飾る,
驚かす, 驚く, 鬼 and 黙る). No other line of them changes, and no word article
is added. Three existing kanji cards change in their remarks: 塊's mnemonic
now links 鬼, with its title, instead of saying that 鬼 has no card yet; 微's
note on 顕微鏡 now says that 顕 supplies けん instead of saying that 顕 has no
card here yet; and 鏡's note on the other kanji in its common words now links
顕, with its title, and says only that 眼 has no card here yet.
`n1_linkplan.py verify --remarks` checks the article links, and the author's
`kanji_remarks.py` checks that 塊, 微 and 鏡 change only by their declared
remarks.

Before the freeze, the author checked the quoted glosses and Japanese phrases
against their sources and every mnemonic against its KanjiVG tree, and ran the
author's claim audits. Design changes before drafting replaced four
distractor candidates: 雄 takes 柔, 飽 takes 祝 and 黙 takes 踊 instead of
candidates that overlapped an exclusion or a title, and 項 takes 預 instead of
領, whose kun reading えり (JMdict files it under 襟, “collar”) also means
“nape of the neck”, like 項's うなじ. The titles avoid “neighbor” for 隣 (町
is excluded as “town, neighborhood”), “raise” for 飼 (挙 is “raise; cite;
hold (an event)”) and “fall silent” for 黙 (落 is “fall down” and 陥 “fall
into; cave in”). Kanjipedia's antonyms (雌 for 雄; 微, 隠 and 密 for 顕) are
neither excluded nor used as distractors. The author's read of the drafts
corrected two mnemonics
against KanjiVG (in 随, ⻌ runs under 有 only; in 雄, 厷 is described only as a
shape that ends in 厶) and replaced two exclusion reasons with sourced ones:
隣/近 now rests on 近隣 and 比隣, which Kanjipedia lists among 隣's compounds,
and 項/個 on Digital Daijisen's second sense of 項, 小分けした一つ一つ. The
reading audits also take, from an okurigana scan of Digital Daijisen
headwords, the readings 随 まま.に, 隠 いん.ぺい, こも.る and なま.る, 雷
らい.こう, 顕 あら.わ and 黙 だんま.り, もく.する and もく.とう; of these only 隠
なまる (by 鈍) collides with a reading another card offers, and no audited
pool can draw it.

## Review execution

Reviewers of two model families, Claude and GPT, worked independently. All four
runs ran one after the other (no two runs overlapped). The two initial runs
reviewed the same frozen packet (`packet/`) without seeing each other's work.
Each confirmation was run by a **fresh agent of the same model family**, not a
later turn of an earlier agent. It received a new packet with the author's
statement answering its family's report (`RESPONSE.md`), the list of changes
(`CHANGES.md`), the revised cards and the exact diff, and was allowed to read
the original packet and its own family's initial report, and never the other
family's report. Models and times come from the runtime session records, not
from the reports.

| Run | Model | Snapshot | Window, 2026-11-21 UTC | API requests | Tool calls | Max in flight | Verdict |
|---|---|---|---|---:|---:|---:|---|
| initial-claude | claude-opus-5.5 | `f8f3db8c` | 04:20:18-04:29:57 | 59 | 58 | 1 | NEEDS FIX (scoped coverage): two minor findings (C1, C2); six optional suggestions (O1-O6) |
| initial-gpt | gpt-6.1-sol | `f8f3db8c` | 04:31:25-04:43:50 | 70 | 69 | 1 | NEEDS FIX (consistency and quiz safety): two minor findings (G1, G2); three optional suggestions (GO1-GO3) |
| confirm-claude | claude-opus-5.5 | `e5c945d6` | 05:19:30-05:23:05 | 32 | 32 | 2 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `e5c945d6` | 05:24:14-05:29:52 | 42 | 41 | 1 | CONFIRMED |

Both families confirmed the same final commit `e5c945d6`, which was written
(04:59:40 UTC) before either confirmation started. `confirm-packet/` holds the
two packets (`c1claude`, `c1gpt`; shared files are stored once in `common/`).
`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes the files
with the packets. Raw session logs stay local because they may hold private
context.

## Findings and dispositions

The GPT report did not number its three optional points; `GO1` to `GO3` follow
their order in the report, as in the author's statement and the confirmation.

| Item | Raised by | Disposition |
|---|---|---|
| C1: 雄 omits 英雄 and 雄大, which the Joyo table prints as examples of ユウ; its ユウ row names only the rare 雄勁 | Claude | Applied in e5c945d6: the Common words add 英雄 えいゆう “hero; heroine; great person” (JMdict 1174680, sense 1) and 雄大 ゆうだい “grand; magnificent; majestic”, the first three glosses of JMdict 1542540 (`雄.md:39-40`); the Joyo note names 雄大, 英雄 and 雌雄 (`雄.md:45`), as the Joyo table (p. 150) prints them; 1174680, 1542540 and 1312940 (雌雄) join the Metadata ids (`雄.md:61`). 雄勁 still establishes the quiz reading. The optional sub-remedy, naming 英雄 in the 英 exclusion note, was declined: a shared compound is not a shared meaning. Resolved |
| C2: 随 omits 随分 ずいぶん | Claude | Applied (`随.md:38`): 随分 ずいぶん “very; considerably”, shortened from JMdict 1372800 sense 1, with JMdict's note that it is usually written in kana; 1372800 joins the Metadata ids (`随.md:60`). 随時 and 随所, which the report called less important, were not added. Resolved |
| G1: 随 (“follow; at will”) lacks a direct exclusion of 追 (“chase; pursue”), though the first sense of 追う includes “to follow after”; the report showed a reduced pool {追, 近, 週, 随} in which 随's title would fill a wrong slot of 追's meaning question | GPT | Changed in e5c945d6: 随 excludes 追 (`随.md:14`, now eleven cards, `随.md:45`), with a new bullet citing JMdict 1432410 (`随.md:56`); 1432410 joins the Metadata ids (`随.md:60`). 逮 (“arrest; chase”) was checked as well and not added: KANJIDIC2 gives it no sense of following. Resolved |
| G2: 隣 (“next door; adjoining”) lacks a direct exclusion of 側 (“side”), though 側 そば includes “(place) right next to” and “beside”; the report showed a reduced pool {側, 内, 右, 隣} | GPT | Changed in e5c945d6: 隣 excludes 側, with a new bullet citing JMdict 1403830 (`隣.md:14`, `隣.md:50`). While checking it, the author also excluded 辺 (“vicinity; edge”): JMdict glosses 辺り あたり with “(in the) neighbourhood; neighborhood; vicinity; nearby; surroundings” (1512080), the basis on which 隣 already excludes 町, so the 町 bullet now covers 辺 (`隣.md:49`); now seven cards (`隣.md:44`); 1512080 and 1403830 join the Metadata ids (`隣.md:54`). confirm-gpt judged 隣/辺 a direct overlap on its own terms. Resolved |
| O1: 隣's とな.る row gives only the archaic 隣る; the Joyo example 隣り合う appears only in Notes | Claude | Applied (`隣.md:32`): the row leads with 隣り合う となりあう “to adjoin each other; to sit side by side” (JMdict 1598830), the Joyo example, and gives 隣る as archaic (JMdict 2163190); the Joyo note no longer repeats the gloss (`隣.md:41`). Resolved |
| O2: 飾's Meaning section quotes three of 飾る's four senses without numbering them, while the 華 note speaks of the “fourth sense” | Claude | Applied (`飾.md:23`): the sentence now numbers the first, second and fourth senses of JMdict 1357210. Resolved |
| O3: 黙 names neither 暗黙 (a Joyo example) nor 黙祷, and its もだ.す row does not say that Kanjipedia marks もだす 外 | Claude | Applied in part: the もだ.す row notes the 外 mark (`黙.md:34`); the Common words add 沈黙 ちんもく (JMdict 1431810) and 暗黙 あんもく “tacit; unspoken; implicit” (JMdict 1154700) (`黙.md:39-40`); the Joyo note names 暗黙 and 沈黙 (`黙.md:44`); 1154700 joins the Metadata ids (`黙.md:54`). 黙祷 was not added: in JMdict 1535010 only the spelling 黙とう carries a priority mark. Resolved |
| O4: 黙's distractor 走 “run” is far from “be silent” and does little work | Claude | Not changed: it is clearly wrong in both directions, and how hard distractors should be is a corpus-wide choice. Accepted in the confirmation |
| O5: 項's mnemonic calls 頁 only “a shape” | Claude | Applied (`項.md:25`): 頁 is described as a horizontal stroke and a left-falling stroke over 貝, and 貝 as 目 over 八, as KanjiVG 09805 draws them; there is no 頁 card. Resolved |
| O6: the exclusion notes make every card dense on a phone | Claude | Not changed: the report notes that this is the corpus style; shortening it would be a corpus-wide change. Accepted in the confirmation |
| L1: Claude's working assumption that Common words lists only existing word articles, on which C1 and C2 asked for mentions rather than new links | Claude | Disputed, with no card change beyond C1 and C2: Common words bullets without a link are an established pattern (1,812 such bullets on 1,003 cards of the reviewed packet's corpus, such as 釈放 and 会釈 on 釈, `釈.md:40-41`), so the C1, C2 and O3 words were added as plain-text bullets. Accepted in the confirmation, which checked the pattern on 釈 but did not recount the bullets |
| GO1: gloss …に飽かして on 飽かす, and mark the independent verb 飽く as written style without implying that あくまで is | GPT | Applied (`飽.md:33-34`): the あ.かす row adds the second sense of 飽かす, “to use lavishly (and without regret)”, and the form 〜に飽かして (JMdict 1518280); the あ.く row adds, directly after 飽く and before 飽くまで, Digital Daijisen's note that standard Japanese generally uses あきる and that あく is written style (「あく」は文章語的な表現); the Metadata line links the Digital Daijisen 飽く entry (`飽.md:56`). Resolved |
| GO2: add 英雄 to 雄 | GPT | Covered by C1. Resolved |
| GO3: shorten the dictionary-by-dictionary explanations and exclusion rationales | GPT | Not changed: each excluded card gets one bullet with its source reason, the format of the existing N1 cards' Notes. Accepted in the confirmation |
| Claude confirmation | Claude | No finding and no optional item |
| GPT confirmation | GPT | No finding and no new optional item |

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The two
  initial runs and `confirm-gpt` had at most one tool call in flight.
  `confirm-claude` once issued two read-only calls at once, at 05:20:26 UTC:
  two `grep` searches of the original packet's `titles/kanji-titles.tsv` for
  the rows of 追, 辺, 側, 英 and 逮 (the first also for 雌, 沈, 暗 and the
  header). Its report discloses this. The final messages of the two Claude
  runs are not identical to their saved reports but contain them (the
  audits' similarity is 0.99 and 0.98); `reports/` keeps the saved reports.
  The `confirm-gpt` audit flags one path outside the allowed folders: the
  parent `review-packets` folder, which its shell commands used as a base
  path. This is a false positive: every path built on it lies in the
  confirmation packet, the original packet or its family's initial report.
  The audits find no corpus scan.
- **Prompts.** Every prompt was saved to a file before use; each file matches
  the message its agent received, apart from the final newline.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists as unread some files that the reports
  say were read. Both initial audits list the stroke files, the word articles
  and the 22 diffs as unread. `initial-claude` parsed every stroke file and
  read every changed line of the diffs, but not their unchanged context; it
  read 塊, 微 and 鏡 only around their remark edits, read `reading-exposure.txt`
  and `reading-options.txt` only in part, and did not open
  `daijisen-heads.txt`, `kanjivg-svgs.txt`, the app code or the full word
  articles. `initial-gpt` parsed every stroke file and compared it with its
  KanjiVG SVG, read all 22 diffs in full, and loaded the word articles and the
  three remark-edited cards for replacement checks, reading closely only their
  changed passages. The `confirm-gpt` audit lists all fifteen revised cards as
  unread; its report says it read the seven changed cards in full, and the
  eight unchanged cards in full from the original packet. `confirm-claude`
  read six of the changed cards in full and 項 around its only hunk. It read
  every hunk header and changed line of `fix.patch`, except removed lines
  starting with “--”, which its search filtered out; it judged the revised
  Joyo lines directly instead. It did not reopen the eight unchanged cards
  beyond their quiz options, and did not open `meta-scan.txt`,
  `KanjiMeaningMetadata.kt`, `KanjiReadings.kt` or `Words.kt`. `confirm-gpt`
  read 追, 側 and 辺 in full and the opening metadata of every curated option
  card, read
  `KanjiReadings.kt` to line 240 and `Words.kt` at lines 216-240, and did not
  open one oversized read that the tool captured automatically.
- **Dictionary text.** Several judgments rest partly on live reads of
  Kanjipedia, Digital Daijisen (Weblio), Jisho and kanjiapi.dev pages, not on
  pinned copies in the packet. `initial-claude` fetched Kanjipedia only for
  黙 and 顕 and checked the other thirteen cards' Kanjipedia quotations
  against the packet's evidence only. `initial-gpt` read Kanjipedia and
  Weblio for all fifteen kanji and Jisho for the words and several kanji,
  mostly from Python, which the audit's list of web reads does not count;
  five kanjiapi.dev requests returned 403. `confirm-claude` fetched the
  Weblio page for 飽く, and `confirm-gpt` fetched Kanjipedia for the seven
  changed kanji and the same Weblio page. Both confirmations checked the Joyo
  table only in the packet's extract, not the PDF.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `e5c945d6` they report 0
  production, 0 padded-session and 0 one-holder hits for ordinary readings.
  Three KANJIDIC2 name-only readings can be offered as wrong reading options
  only in a Starter practice session that also borrows a card holding them:
  雄 ゆ (by 愉 or 輸), 雄 よう (by any of its eighteen holders, such as 容 or
  様) and 飼 かい (by 貝); in the N1 and All pools the curated options of 雄 and
  飼 fill every wrong slot. The audits also record eight latent collisions:
  attested readings that other cards offer but no audited pool can draw (隠 お
  and なまる, 雄 かつ, ゆ and よう, 飼 かい, 飽 あき, 飾 しか).
  `reading_options.py`, which does not model curated options, reports no
  problem. The meaning-quiz check reports 0 errors and 0 warnings. 鮮's セン
  quiz takes one of its three wrong options from its curated cards (淡 タン),
  because 腐 and 濁 quiz no reading; the other two come from other cards.
  Sampled seeds are not exhaustive, and the claim covers the documented
  shipped pool configurations only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. Five cards quiz only their on reading (随 ズイ,
  雄 ユウ, 項 コウ, 顕 ケン, 鮮 セン) and ten only their kun reading (隠 かく.す,
  隣 となり, 雷 かみなり, 霧 きり, 飼 か.う, 飽 あ.きる, 飾 かざ.る, 驚 おどろ.く,
  鬼 おに, 黙 だま.る). All fifteen quizzed readings are in the official Joyo
  table. 隠れる, 飽くまで, 飾り and 驚かす are linked on their own rows, which
  are not quizzed, because the app asks one question per stem.
- **Exclusions.** No two new cards exclude each other, and every exclusion
  between a new and an existing card is declared on the new card; the app
  applies an exclusion in both directions.
- **Source-only readings.** 隠 よ.る, 雷 いかづち, 霧 ボウ, 顕 あきらか and 黙
  ボク have no checked JMdict example and are labelled “source-only here” on
  the cards.
- **Metadata ids.** Every word named on the cards as a whole run outside a
  quotation has its JMdict entry id on the card's Metadata line. Not listed
  are 10 words that occur only inside quoted Kanjipedia or Digital Daijisen
  text (such as 悪神 on 鬼, 首筋 on 項 and the label 学習漢字 on 飼) and 82
  shorter words that occur only inside longer phrases and headwords.
- **Lint warnings.** Three warnings, none on the new cards or on 塊, 微 and
  鏡, are older than the batch and out of scope: the word article 隣, which
  gains a link here, and 眼鏡 and 鏡, which declare the edited 鏡 card and are
  checked with it, have no Dictionary line.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten, and the fix
  commit was not amended. The Claude confirmation packet was rebuilt once
  before its run, after the author's statement was changed to cite
  original-packet paths; the earlier build was never given to a reviewer.
  The freeze and the fix commit remain in the history, and every report is
  kept.

## Validation and accounting

At the reviewed snapshot `e5c945d6`: 439 host tests pass; validation 0 errors;
lint 0 errors and 3 warnings (above); quiz safety 0/0; reading options 0
problems; manifest rebuild unchanged (version `86efb6075a9da228`, 9,701 files,
SHA-256 `A5C5F9ABA746FE6A3B96B670C09C8AC9D0E4E2039BE347775A28D204DD55FEEE`);
budget 9,724 entries, 56,447,121 retained, 56,876,685 inflated and 36,272,051
local-ZIP bytes; vocabulary 3201/3539; link plan 19 links, 0 problems; kanji
remarks 15 of 15 present, 3 existing cards changed only by their 3 declared
remark edits.

After publication, delivery becomes **572/1,228**, with **656 remaining**.
Until the receipt it stays 557/1,228.
