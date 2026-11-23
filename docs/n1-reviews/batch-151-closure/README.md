# Batch 151: textual-review closure

The fifteen cards are textually review-closed. Both families' last
confirmations of the reviewed snapshot are **CONFIRMED**, with no remaining
finding. `origin/main` had not moved from the published base when the review
closed, so publication is a fast-forward and no integration merge is needed.
Publication is **pending** at this closure commit; the later receipt
establishes the remote commit, CI and served ZIP. No JVM, native, device or
phone acceptance is implied.

## Snapshot and scope

- Members: **訴 証 詩 詳 誇 誓 誘 謙 謡 譲 護 豆 豪 貢 貴**
  (source rows 1003, 1005, 1011, 1013, 1014, 1016, 1018, 1030, 1032, 1035,
  1036, 1037, 1039, 1041, 1043).
- Published base: `b9f0e3403cf692850df678db3a3fd7544c3e0323` (the B150 receipt).
- Blind-review freeze: `b624890f8aea8cfb6b5a08ee6beff21df5f8c807`.
- Fix commit: `15441514ec9a0a3835921e2031f7d79bec6c8920`, the reviewed
  snapshot. It changes nine of the fifteen cards (誓 誘 謙 譲 護 豆 豪 貢 貴)
  and the derived `manifest.json`. 訴 証 詩 詳 誇 謡, the ten existing cards
  with a remark edit, the fifteen stroke files and the nineteen word articles
  are unchanged from the freeze.
- After the freeze, two front-matter lists changed and nothing else in front
  matter: 誘's `quiz_exclusions` lose 訪, and 譲's `distractors` 食 行 来 become
  買 話 読. No title, tag, metadata reading, quizzed reading or stroke file
  changed.

The batch adds fifteen cards and stroke files. Nineteen existing word articles
each gain one link to a new card (訴える, 保証, 証明, 詩, 詩人, 詳しい, 誇り,
誓う, 誘う, 謙虚, 謙遜, 歌謡, 民謡, 譲る, 看護婦, 豆, 豪華, 貢献 and 貴重), and
no other line of them changes. No word article is added. Ten existing kanji
cards (献 仮 推 縫 憩 熟 級 長 義 養) each change in one remark: a sentence
saying that a kanji had no card here now links that kanji's card. Only 献's
remark concerns this batch (貢); the other nine had gone stale when earlier
work added 虚, 薦 and 裁 (batch 150), 舌 (batch 149), 慮 (batch 141), 及 and 我
(batch 135), 羊 (commit `1359b467`) and 短 (before the N1 work). 縫's remark
shrinks from two lines to one, because its second clause only qualified the
old statement. `n1_linkplan.py verify --remarks` checks the article links, and
the author's `kanji_remarks.py` checks that each existing card changes only by
its declared remark.

Before the freeze, the author checked the quoted glosses and Japanese phrases
against their sources and every mnemonic against its KanjiVG tree, and three
claim auditors re-read the cards against the sources. 証 lost the planned
exclusions 確 認 券, which had no verifiable overlap, and its distractors became
罪 刑 損, because the quiz-safety check found 罪 and 罰 excluded from each other.
譲's first distractors 奪 拾 握 let a Starter practice session that also borrows
攻 or 責 offer せめる, an attested reading of 譲, so they became 食 行 来. The
譲 mnemonic was reworded to follow KanjiVG's split of 三; the reasons for five
exclusions (申 on 訴, 徴 on 証, 慢 on 誇, 返 on 譲, and 価 and 値 on 貴) were
narrowed to what the cited glosses and titles say; quotations on 訴 詩 誘 豆
and the 誇 mnemonic were aligned with their sources; and four JMdict entry ids
were added to Metadata lines (梵語 on 護, 大いに on 豪, 献じる on 貢, 大切にする
on 貴).

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
| initial-claude | claude-opus-5.5 | `b624890f` | 16:31:40-16:40:08 | 77 | 76 | 1 | NEEDS FIX (minor): the 貴 mnemonic (C1); CLEAN on the other cards and facets |
| initial-gpt | gpt-6.1-sol | `b624890f` | 16:41:13-16:58:06 | 67 | 66 | 1 | NEEDS FIX (G1, G2); one link target unverified (L1) |
| confirm-claude | claude-opus-5.5 | `15441514` | 17:47:02-17:51:31 | 34 | 33 | 1 | CONFIRMED |
| confirm-gpt | gpt-6.1-sol | `15441514` | 17:52:06-17:57:23 | 40 | 39 | 1 | CONFIRMED |

Both families confirmed the same final commit `15441514`, which was written
before either confirmation started. `confirm-packet/` holds the two packets
(`c1claude`, `c1gpt`; shared files are stored once in `common/`). `reports/`
holds the verbatim reports, `prompts/` the exact prompts and `scope-audits/`
each run's read-scope audit. `provenance.json` hashes the files with the
packets. Raw session logs stay local because they may hold private context.

## Findings and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| C1: 貴's mnemonic leaves out KanjiVG stroke 5, the horizontal stroke between 中 and 貝 | Claude | Changed in 15441514: 中 "sits at the top on a horizontal stroke 一" above 貝, which accounts for all 12 strokes. Resolved |
| G1: 誘 excludes 訪 only through the English word "call" (JMdict 誘う "to call (for)", 訪 "visit; call on"), though inviting someone is not visiting them | GPT | Changed in 15441514: 訪 removed from the exclusions and its bullet; the 呼 exclusion now rests on JMdict 呼ぶ sense 3 "to invite" (entry 1266440, added to the Metadata ids). 訪 declares no exclusions of its own, so the pair is no longer excluded. Resolved |
| G2: 譲's distractors 食 行 来 are remote basic actions that give no credible contrast | GPT | Changed in 15441514: 買 話 読. Buying is the other side of selling (譲る sense 4 "to sell", JMdict 1357030), and 話 and 読 share the radical 言, but none means handing over. Eleven trial sets chose them: each of the six sets with a transfer verb that is not a Starter card (奪 受 借 拾 握) lets 攻 or 責 offer せめる in a Starter practice session, and none of the five Starter sets does. Resolved |
| L1: 貢 links `../articles/compound-sound-changes.md`, which the packet did not include | GPT | Verified, no card change: the article is tracked at both snapshots with the same blob `6d5e1f06`, is linked from 井 and 傑, and was supplied in the confirmation packet. Resolved |
| O1: 謙's mnemonic omits strokes 10 and 16-17 of 兼 | Claude | Applied: 八, then a horizontal stroke, ⺕, two vertical strokes 丨 and two final sweeping strokes, checked against KanjiVG |
| O3: 誓 lists ゼイ after the kun reading ちか.う | Claude | Applied: ゼイ directly after セイ; no row text changed. Three earlier cards (脈 華 覆) keep the old order (Limits) |
| O5: closer distractors for 譲, such as 奪 or 受 | Claude | Applied with a different set (G2); 奪 and 受 were tried and rejected because of the せめる exposure. Resolved in the confirmation |
| O2 and GO2: 看護婦, 護's only example word, is obsolete | Claude, GPT | Not applied: 看護婦 is the only word article containing 護; the card labels it obsolete, names 看護師 as the current word and gives 保護 as a Joyo example. A new article can replace it later. Accepted in both confirmations |
| O4: further words (告訴, 起訴, 控訴, 誘拐, おびき出す, 宣誓) | Claude | Not applied: they would add new sourced claims to a revision whose coverage both reviews judged clean. Accepted in the confirmation |
| O6: the 縫 remark diff drops a clause | Claude | No change needed: the clause only qualified the old statement that 裁 had no card. Accepted in the confirmation |
| GO1: shorten the audit-style Notes; "declaring word" could be "example word" | GPT | The shortening was not applied, for consistency with the existing N1 cards; "example word" was applied at all eight places on 護 豆 豪 貢 貴. Accepted in the confirmation |
| Confirmation optional: on 護 and 豪 line 23, "example word" names both the linked article and a Joyo example; 話 and 読 relate to 譲 only visually, through 言 | Claude | Not applied; editorial, recorded here. The reviewer judged the distractors acceptable given the documented exposure constraint |
| GPT confirmation | GPT | No finding and no new optional item |

## Limits

- **Fresh confirmers.** Each confirmation ran as a new agent of the same model
  family and had no memory of its own earlier reading. The confirmations of
  the two families are independent of each other.
- **Execution.** Every run started after the previous one ended, and no run
  had more than one tool call in flight. The `initial-gpt` audit flags two
  "recursive shell commands over packet directories". These are false
  positives: the audit's pattern matches `**`, and the two matched commands
  (16:50:55 and 16:51:07) used `**` as Python exponentiation to sample Bézier
  curves of the stroke files; no recursive listing ran. The `confirm-gpt`
  audit flags one path outside the packet and report: the parent
  `review-packets` folder, used only as a base variable to build paths into
  the original packet and the confirmation packet.
- **Prompts.** Every prompt was saved to a file before use.
- **Scope audits.** The audit script does not attribute reads made through
  shell commands or Python, so it lists files as unread that the reports say
  were read: the 29 diffs and the 15 Digital Daijisen extracts in the
  `initial-claude` audit; all fifteen cards, stroke files, word articles and
  diffs in the `initial-gpt` audit (read in `Get-Content` loops and parsed in
  Python); and the nine changed cards in both confirmation audits (and the
  fix patch in the `confirm-claude` audit), which both reports say were read
  in full. The stroke files were checked point by point only by
  `initial-gpt`; `initial-claude` checked the mnemonics against the KanjiVG
  component list, and reviewed the nineteen word articles through their
  one-line diffs without opening the articles. The confirmations read the
  changed cards and the cumulative change, and could read the original packet
  and their own family's initial report; neither re-read the six unchanged
  cards (訴 証 詩 詳 誇 謡) in full, and both checked them through the quiz
  audits.
- **Dictionary text.** Several judgments rest partly on live reads of
  Kanjipedia, Digital Daijisen and Jisho pages, not on pinned copies in the
  packet. `confirm-claude`'s one live fetch returned no entry and verified
  nothing; it relied on the pinned JMdict and KanjiVG extracts.
- **Quiz evidence.** The reading audits are the author's Python ports of the
  Kotlin builder, kept outside the repository. At `15441514` they report 0
  production, 0 padded-session and 0 one-holder hits for an ordinary reading
  and three latent collisions, attested readings that other cards offer but no
  audited pool can draw: 詳 よし (由; KANJIDIC2 name reading), 譲 せめる (攻 数
  責; Digital Daijisen) and 貴 ぎ (儀 技 疑 義 議; KANJIDIC2 name reading). Two
  KANJIDIC2 name-only readings can be offered only in a Starter practice
  session, which has no curated options: 豆 ま (by 目 真 間 馬) and 豪 ご (by 互
  五 午 娯 後 御 悟 期 碁 語 誤 護 降); in the N1 and All pools the curated
  options (芋 卵 塩 on 豆, 弱 静 暗 on 豪) fill every wrong slot. The older
  reading-options check lists both for information and reports 0 problems.
  The meaning-quiz check reports full-pool options only; `confirm-claude`
  noted that it cannot show what the tag fallback draws in a Starter session.
  The Starter titles that come close to a new card's sense are excluded on that
  card (聞 on 誘, 小 and 子 on 豆, 力 on 豪, 供 on 貢, 高 on 貴), and 訪 is not
  a Starter card. Sampled seeds are not exhaustive, and the claim covers the
  documented shipped pool configurations only.
- **Quizzed readings.** Readings with no declaring word article are listed and
  illustrated but not quizzed. Eight cards quiz only their on reading (証
  ショウ, 詩 シ, 謙 ケン, 謡 ヨウ, 護 ゴ, 豪 ゴウ, 貢 コウ, 貴 キ) and seven only
  their kun reading (訴 うった.える, 詳 くわ.しい, 誇 ほこ.る, 誓 ちか.う, 誘
  さそ.う, 譲 ゆず.る, 豆 まめ).
- **Example word.** The only word article for 護 is 看護婦, which JMdict marks
  as obsolete; no article for a current 護 word is added in this batch.
- **One-way exclusions.** Two pairs of new cards declare their exclusion on one
  card only (謡 lists 詩, 譲 lists 謙); the app applies an exclusion in both
  directions.
- **Reading order.** Three earlier cards (脈 華 覆) still list an on reading
  that is outside the official table after their kun rows; only 誓 was
  reordered in this batch.
- **Source-only readings.** Some readings rest on a single dictionary entry or
  a Kanjipedia-only entry and are labelled as such on the cards.
- **Metadata ids.** Every word named on the cards as a whole run has its JMdict
  entry id on the card's Metadata line; 61 shorter words that occur only
  inside longer quoted phrases and headwords are not listed.
- **Lint warnings.** Nineteen warnings, none on the new cards, are older than
  the batch and out of scope: four on the existing card 長, which changes only
  by its remark; thirteen on word articles whose Dictionary line cites no
  JMdict entry id; and two on 看護婦 and 校長, which have no Dictionary line.
- **Not run.** Android JVM tests and the Kotlin reading cross-check (no JDK);
  native, rendered, device or phone acceptance.
- **Superseded material.** No published commit is rewritten. The freeze and
  the fix commit remain in the history, and every report is kept.

## Validation and accounting

At the reviewed snapshot `15441514`: 439 host tests pass; validation 0 errors;
lint 0 errors and 19 warnings (above); quiz safety 0/0; reading options 0
problems; manifest rebuild unchanged (version `be2f3cccfca84a39`, 9,609 files,
SHA-256 `64CF8C247981DFE754BF904FF955EC02F10DD4A17142E53F5EDC29A5B22A8411`);
budget 9,632 entries, 56,066,773 retained, 56,426,069 inflated and
36,082,651 local-ZIP bytes; vocabulary 3201/3539; link plan 19 links, 0
problems; kanji remarks 15 of 15 present, 10 existing cards changed only by
their declared remark.

After publication, delivery becomes **527/1,228**, with **701 remaining**.
Until the receipt it stays 512/1,228.
