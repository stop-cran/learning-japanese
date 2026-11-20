# Author's statement for the reviewer of `reports-151\initial-gpt.md`

This statement answers only the points in YOUR initial report. G1 and G2 are your report's own Findings labels; your Optional
section has two bullets, called GO1 (shorten the audit-style Notes; "declaring word" could be "example word") and GO2 (prefer a
current example over 看護婦 later) below, and L1 is the 貢 article link in your Limits. The statement is the author's claim about
what changed and why. Verify each claim against the revised text in `snapshot\`, `diffs\fix.patch`, the `checks\` outputs and
independent sources; do not rely on this text as evidence. Card line numbers refer to the revised cards in this packet. Nine of
the 15 new cards changed (誓 誘 謙 譲 護 豆 豪 貢 貴); 訴 証 詩 詳 誇 謡, every existing kanji card, every stroke file and every word
article are unchanged. One `quiz_exclusions` list (誘) and one `distractors` list (譲) changed; no title, tag, metadata reading,
`quizOnyomi` or `quizKunyomi` changed. See `CHANGES.md`. Give a disposition for each of G1, G2, GO1, GO2 and L1.

## Findings

### G1: 誘/訪 exclusion

Author action: **changed** as you proposed. 訪 is removed from 誘's exclusions (`誘.md:14`), the count reads "These thirteen cards"
(`誘.md:45`), and the visiting comparison is gone. The 呼 exclusion is kept, with its own justification instead of the shared English
word: "JMdict 誘う includes “to call (for)”, and JMdict 呼ぶ sense 3 is “to invite” (entry 1266440)." (`誘.md:51`); entry 1266440
is added to the Metadata ids (`誘.md:59`). `checks\quiz-safety.txt` shows 誘's three curated distractors still fill every wrong
meaning slot.

### G2: 譲 distractors

Author action: **changed.** `譲.md:13` now lists 買 (“buy”), 話 (“talk, speak”) and 読 (“read”), and `譲.md:57` says why each is a
credible but wrong choice: buying is the other side of selling (譲る can mean “to sell”, JMdict 1357030 sense 4), and 話 and 読 share
the radical 言 with 譲, but none of them means handing over or yielding. None of the three is excluded on 譲.

As your remedy asked, reading exposure was rechecked, and it decided the choice. Sets built from transfer verbs that are not
Starter cards (奪, 受, 借, 拾, 握) were tried first: each of the six such sets tried lets a Starter practice session that also
borrows the card 攻 or 責 offer せめる, an attested reading of 譲, as a wrong answer to the ゆず.る prompt. Every set of Starter
cards tried, including the committed one, has no such hit. `evidence\distractor-trials.txt` records all eleven trials (each swaps
only the `distractors` line and restores the file afterwards). For the committed set, `checks\reading-exposure.txt` reports 0
production, padded-session and one-holder hits for 譲; the latent せめる collision (offered by 攻 数 責, not drawable in any shipped
pool) is unchanged from the freeze.

## Optional

- **GO1, shorter Notes: not changed.** The exclusion list with one reason per excluded card, and the paragraph naming each
  distractor, is the Notes format used across the existing N1 cards, and `quiz_safety.py` checks that each distractor is named in Notes;
  shortening them in one batch would make it inconsistent with the rest.
- **GO1, "declaring word": applied.** "Declaring word" is replaced by "example word", and "both characters write the declaring word
  X" by "both characters appear in the example word X", on `護.md:23,51`, `豆.md:23`, `豪.md:23,52`, `貢.md:23,46` and `貴.md:23`.
  No other card in this batch used the phrase.
- **GO2 (看護婦): not changed.** 看護婦 is the only word article in the repository that contains 護, so it remains the example word
  for ゴ; the card states the obsolete status and points to 看護師, and gives 保護 as a Joyo example (`護.md:23`). A newer word
  article can replace it when one exists.

## Limits

- **L1 (貢's link to `../articles/compound-sound-changes.md`): verified, no change needed.** The article is tracked in the
  repository at the reviewed snapshot and at this revision with the same blob (`6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`); it is
  also linked from the existing cards 井 and 傑. This packet includes it unchanged as `evidence\compound-sound-changes.md`. The
  repository is public, and the published copy is at
  https://github.com/stop-cran/learning-japanese/blob/main/articles/compound-sound-changes.md (raw:
  https://raw.githubusercontent.com/stop-cran/learning-japanese/main/articles/compound-sound-changes.md).

## Other changes in this revision (from the other review)

These were not raised by you; they are listed so that every hunk is accounted for. 貴's mnemonic now places 中 on a horizontal
stroke 一 above 貝, which accounts for KanjiVG stroke 5 (`貴.md:25`). 謙's mnemonic accounts for every stroke of 兼 (`謙.md:25`). 誓's
on reading ゼイ is listed directly after セイ, before the kun reading ちか.う (`誓.md:31-33`; no row text changed).
