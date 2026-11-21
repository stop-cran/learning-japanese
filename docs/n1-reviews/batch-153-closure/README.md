# Batch 153: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. `origin/main` had not moved from the published base when the review
closed, so publication is a fast-forward and no integration merge is needed.
Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **酌 酔 酢 醜 釈 釣 鈴 銃 銭 鎖 鐘 鑑 附 陥 陰**
  (source rows 1106, 1107, 1108, 1114, 1117, 1118, 1119, 1122, 1125, 1135,
  1138, 1139, 1147, 1150, 1152).
- Published base: `67b9567098ae1a2fe357f53fac530188788ba1ba` (the B152 receipt).
- Blind-review freeze: `cdab83b375e68d14d6d58a4866959611e949c41a`.
- Fix commit: `3f8b951d38944704afbc74ed8e874e464b579956`, the reviewed
  snapshot. It changes four of the fifteen cards (醜 釈 鎖 陥) and the derived
  `manifest.json`. 酌 酔 酢 釣 鈴 銃 銭 鐘 鑑 附 陰, the existing card 属 with
  its remark edit, the fifteen stroke files and the twenty word articles are
  unchanged from the freeze.
- After the freeze, only 陥's `quiz_exclusions` changed in front matter: it
  gained 捕 and 釣. No title, tag, distractor list, metadata reading, quizzed
  reading or stroke file changed.

The batch adds fifteen cards and stroke files. Twenty existing word articles
each change in one line, which gains a link to a new card (酌む, 酔う, 酔っ払い,
酢, 醜い, 解釈, 釣り, 釣り合う, 釣る, 鈴, 銃, 金銭, 鎖, 鐘, 図鑑, 鑑賞, 附属, 欠陥,
日陰 and 陰). In two of them that line also loses a sentence saying that the new
card did not exist yet: 附属 drops “附 has no card yet.” and 酌む drops “There
is no 酌 kanji card in the current collection.” No other line of them changes,
and no word article is added. One existing kanji card changes in its remarks:
属 now links 附, with its title, in 附属 instead of saying that 附 has no card
yet. `n1_linkplan.py verify --remarks` checks the article links and the two
article remarks, and the author's `kanji_remarks.py` checks that 属 changes
only by its declared remark.

Before the freeze, the author checked the quoted glosses and Japanese phrases
against their sources and every mnemonic against its KanjiVG tree, and ran the
author's claim audits. Three design changes came before drafting: 酢 also
excludes 償 and 附 also excludes 仕, from their Kanjipedia senses, and 陥
excludes 滑; a group of 陰 exclusions resting only on the compound おかげ was
dropped. The first check run found three attested readings that a Starter
practice session borrowing one holder card could offer as wrong reading
options: 醜 たぐい (by 双 or 類), 釈 おく (by 億, 屋 or 憶) and 附 ぶ (by 武, 舞
or 部). 醜's distractors 賢 鋭 美 therefore became the Starter cards 短 赤 新,
釈's 誇 測 祝 became 書 聞 学, and 附's 削 離 除 became 外 出 間, so that their
curated options fill every wrong reading slot in the N1, All and Starter
pools. 酢's distractor 粉 became 麦, because KANJIDIC2 lists デシメートル among
粉's kun readings, which would mark it as a wrong option in 酢's kun quiz. A
scan comparing the KANJIDIC2 meanings of every card with the new titles added
踏 to 鑑's exclusions (KANJIDIC2 lists “appraise” for 踏) and 覆 to 陰's
(KANJIDIC2 lists “shade” for both) before the freeze commit.

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
| initial-claude | claude-opus-5.5 | `cdab83b3` | 00:38:15-00:48:21 | 67 | 66 | 1 | CLEAN on all four facets; six optional suggestions (O1-O6) |
| initial-gpt | gpt-6.1-sol | `cdab83b3` | 00:49:39-01:06:46 | 86 | 85 | 1 | NEEDS FIX (G1); one link target unverified (L1) |
| confirm-claude | claude-opus-5.5 | `3f8b951d` | 01:29:22-01:33:30 | 32 | 32 | 2 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `3f8b951d` | 01:34:37-01:38:33 | 34 | 33 | 1 | CONFIRMED |

Both families confirmed the same final commit `3f8b951d`, which was written
(01:15:18 UTC) before either confirmation started. `confirm-packet/` holds the
two packets (`c1claude`, `c1gpt`; shared files are stored once in `common/`).
`reports/` holds the verbatim reports, `prompts/` the exact prompts and
`scope-audits/` each run's read-scope audit. `provenance.json` hashes the files
with the packets. Raw session logs stay local because they may hold private
context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| G1: 陥 lacks direct exclusions for 捕 (“capture”) and 釣 (“angling; lure”), though JMdict 1216130 glosses 陥れる with “to lure (into a trap)” (sense 1) and “to capture (a castle, fortress, etc.)” (sense 2); the report showed custom pools {陥, 捕, 酢, 鈴} and {陥, 釣, 酢, 鈴} in which a defensible answer would be marked wrong | GPT | Changed in 3f8b951d: 陥 excludes 捕 and 釣 (`陥.md:14`, now fourteen cards, `陥.md:44`), with a new bullet citing entry 1216130 (`陥.md:52`). Each pair is declared once, on 陥. Resolved |
| L1: 酢 links `../articles/compound-sound-changes.md` (`酢.md:40`), which the packet did not include | GPT | Verified, no card change: the article is tracked at both snapshots with the same blob `6d5e1f06`, is also linked from 井 傑 貢 載 輩 遣, and both confirmation packets supply it. Resolved |
| O1: move 鐘's on row シュ up, directly under ショウ | Claude | Not changed: on the N1 cards a reading that is not in KANJIDIC2 gets its row after the KANJIDIC2 rows (華 ゲ, 覆 フウ and フ, and 附 ブ in this batch); シュ comes from Kanjipedia and Digital Daijisen. Accepted in the confirmation |
| O2: 醜's Joyo note leaves out 醜さ, which the Joyo table prints beside 醜い | Claude | Applied (`醜.md:41`): the Joyo table (p. 74) prints “みにくい 醜い，醜さ”. 醜さ has no JMdict entry, so no id was added. Resolved |
| O3: 釈 gives only 解釈 as a common word | Claude | Applied: 釈放 しゃくほう (JMdict 1324260, already cited) and 会釈 えしゃく “slight bow; nod”, shortened from JMdict 1198600 sense 1 (`釈.md:40-41`); 1198600 joins the Metadata ids (`釈.md:66`). Resolved |
| O4: the card does not mention 鎖 read じょう, “lock, padlock” (JMdict 1633480) | Claude | Applied as a Notes line (`鎖.md:43`) on the Digital Daijisen headword じょう【錠／▽鎖／×鏁】 and its note that this sense was originally written 鎖, with 錠 applied later; JMdict 1633480, headed 錠, lists 鎖 as a rarely used kanji form, and joins the Metadata ids (`鎖.md:58`). There is no 錠, 鍵 or 鑰 card, so no new meaning-choice pair arises. Resolved |
| O5: weakly anchored exclusions: 酢/賞, 醜's 同 似 等 匹, 陥/滑 and 鑑's book sense | Claude | Not changed: each pair cites a source sense, and each card's three curated distractors still fill every wrong meaning slot. Accepted in the confirmation |
| O6: the audit's extra Digital Daijisen readings lack 鎖 じょう | Claude | Fixed in the author's audit tooling, no card change: the headword parser rejected katakana or ｜ inside the 〔〕 kana note. With it fixed, only the 醜 しゅう〔シウ〕 and 鎖 じょう headword lines change, the extras gain only 鎖 じょう, and the audit totals are unchanged. Rerun on the headwords of batches 144-152, it adds one reading not already on a card, 益 よう (batch 146, already tested there from JMdict 1576560); an exposure run with `--extra 益=よう` finds 0 production, 0 padded-session and 0 one-holder hits and 1 latent collision. Resolved |
| GO1: shorten the exclusion explanations, especially on 鑑 and 附 | GPT | Not changed: each excluded card gets one bullet with its source reason, the format of the existing N1 cards' Notes. Accepted in the confirmation |
| GO2: the Starter distractors of 醜, 釈 and 附 are unusually easy | GPT | Not changed: they are plausible and unambiguously wrong, and as Starter cards they fill every wrong reading slot, which keeps 醜 たぐい, 釈 おく and 附 ぶ from being drawn. Accepted in the confirmation |
| Confirmation optional: 陥/釣 rests on a single JMdict word gloss (weak but harmless; 陥/捕 is better anchored); on `鎖.md:43` a beginner may wonder why さす has a row and じょう does not, and the ▽ and × markers are not explained | Claude | Not applied; recorded here |
| GPT confirmation | GPT | No finding and no new optional item |

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended. The two
  initial runs and `confirm-gpt` had at most one tool call in flight.
  `confirm-claude` once issued two read-only calls at once, at 01:30:59 UTC: a
  `Select-String` search of the original packet's `titles/kanji-titles.tsv`
  for bow, nod, greet, salut, acquit and liberat, and a `view` of the revised
  `醜.md`. Its report discloses this. Its final message is not identical to
  its saved report but contains it (the audit's similarity is 0.98);
  `reports/` keeps the saved report. The `initial-gpt` audit flags one write
  outside the report path. This is a false positive: the report was written
  through a relative path that resolves to `reports-153/initial-gpt.md`. The
  audits find no path outside the allowed folders and no corpus scan.
- **Prompts.** Every prompt was saved to a file before use; each file matches
  the message its agent received, apart from the final newline of the two
  initial prompts.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists as unread some files that the reports
  say were read. In the `initial-claude` audit these include thirteen of the
  new cards and 属, the 21 diffs and the 15 Digital Daijisen extracts, all of
  which its report says it read in full. That run parsed the stroke files for
  their keys without inspecting the path data, judged the word articles only
  through their diffs, took the
  quiz rules from `content-format.md` and the audits without opening the app
  code, and did not open `quiz-safety.txt` in full. In the `initial-gpt`
  audit they include the diffs and the Daijisen extracts, which its report
  says it read in full; it checked the stroke files by script, read each word
  article's changed line and its section on how the kanji combine, and read
  属's changed Notes passage. The confirmation audits likewise list as unread
  several evidence files (among them `QuizBuilder.kt`, `daijisen-joo.txt`,
  `daijisen-heads-diff.txt` and `link-targets.tsv`) that their reports say
  were read in full. Both confirmations read `fix.patch` and the four revised
  cards in full and could read the original packet and their own family's
  initial report. Neither reopened the eleven unchanged cards in full:
  `confirm-gpt` read the front matter of all fifteen cards, the exclusion
  notes of 鑑 and 附 and 酢's link passage, and read 捕 and 釣 in full;
  `confirm-claude` read 釣's front matter and the readings rows of 附 and 鐘,
  and relied on its initial review and on `CHANGES.md` for the rest. Its
  report says it did not open `meta-scan.txt`, the article
  `compound-sound-changes.md`, the KANJIDIC2 extract or the gate outputs
  (lint, tests, validation, manifest, budget, vocabulary, link plan and kanji
  remarks), relying on `CHANGES.md` for those results, and did not read
  `Words.kt` in full.
- **Dictionary text.** Several judgments rest partly on live reads of
  Kanjipedia, Digital Daijisen (Weblio), Jisho and kanjiapi.dev pages, not on
  pinned copies in the packet. `initial-claude` fetched Kanjipedia for twelve
  of the kanji (the fetch for 釈 failed twice before it succeeded) and used
  the packet's extracts for 鈴, 銃 and 陥. `initial-gpt` fetched Kanjipedia
  for all fifteen, Jisho once and Weblio twice, and also read Jisho,
  kanjiapi.dev and Weblio from Python, which the audit's list of web reads
  does not count. `confirm-claude` checked the “rarely used” marker of JMdict
  1633480 only in the pinned extract (the online JMdict editor page asks for
  a login) and the Joyo table only in the packet's extract, not the PDF. The
  fetches of the L1 article from GitHub at the unpushed commits returned 404
  for both `initial-gpt` and `confirm-gpt`; `confirm-gpt` checked the
  supplied copy's blob hash and the public copy on `main` instead.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `3f8b951d` they report 0
  production, 0 padded-session and 0 one-holder hits, for ordinary and
  KANJIDIC2 name-only readings, and eight latent collisions: attested readings
  that other cards offer but no audited pool can draw (醜 にくむ and たぐい, 釈
  しゃ and おく, 鎖 さす, 附 ぶ, 陰 おん and くらい). `reading_options.py`, which
  does not model curated options, reports two problems, 醜 たぐい and 釈 おく;
  neither can be drawn, because the curated Starter options of 醜 and 釈 fill
  every wrong slot in every audited pool. The meaning-quiz check reports 0
  errors and 0 warnings; 陥's three curated distractors 昇 跳 浮 still supply
  all three wrong meaning options after its exclusions grew. Sampled seeds are
  not exhaustive (200 seeds saw 48 of the 58 drawable wrong options of 陥's
  on prompt), and the claim covers the documented shipped pool configurations
  only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. Six cards quiz only their on reading (釈
  シャク, 銃 ジュウ, 銭 セン, 鑑 カン, 附 フ, 陥 カン) and nine only their kun
  reading (酌 く.む, 酔 よ.う, 酢 す, 醜 みにく.い, 釣 つ.る, 鈴 すず, 鎖 くさり, 鐘
  かね, 陰 かげ). All fifteen quizzed readings are in the official Joyo table.
  酔っ払い, 釣り and 釣り合う are linked on their own rows, which are not
  quizzed, because the app asks one question per stem.
- **One-way exclusions.** Two pairs of new cards declare their exclusion on
  one card only (鈴 lists 鐘, and 陥 lists 釣, added in review); the app
  applies an exclusion in both directions.
- **Source-only readings.** 釈 とく, す.てる and ゆる.す and 銭 ゼン and すき
  have no checked JMdict example and are labelled “source-only here” on the
  cards.
- **Metadata ids.** Every word named on the cards as a whole run outside a
  quotation has its JMdict entry id on the card's Metadata line. Not listed
  are 17 words that occur only inside quoted Kanjipedia or Digital Daijisen
  definitions (such as 鉄砲 on 銃 and 錠前 on 鎖) and 64 shorter words that
  occur only inside longer phrases and headwords.
- **Lint warnings.** Three warnings, none on the new cards or 属, are older
  than the batch and out of scope: all are on existing word articles that gain
  a link here and whose Dictionary line cites no JMdict entry id (日陰, 醜い and
  鑑賞).
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The fix was first
  committed as `4accddbf` (01:09:34 UTC) and amended to `3f8b951d` before
  either confirmation, adding the spelling ×鏁 to the headword quoted on
  `鎖.md:43`; `4accddbf` was never pushed or reviewed. The freeze and the fix
  commit remain in the history, and every report is kept.

## Validation and accounting

At the reviewed snapshot `3f8b951d`: 439 host tests pass; validation 0 errors;
lint 0 errors and 3 warnings (above); quiz safety 0/0; reading options 2
problems that cannot be drawn (above); manifest rebuild unchanged (version
`d7282da57f5203a3`, 9,671 files, SHA-256
`457ADC9901C3C94BAB7F11153F8639D08E8D12FE5E5B7D5B7B9F6D4F54E442E5`); budget
9,694 entries, 56,316,377 retained, 56,745,941 inflated and 36,212,227
local-ZIP bytes; vocabulary 3201/3539; link plan 20 links, 0 problems; kanji
remarks 15 of 15 present, 1 existing card changed only by its 1 declared
remark edit.

After publication, delivery becomes **557/1,228**, with **671 remaining**.
Until the receipt it stays 542/1,228.
