## Snapshot
- **Revised commit:** `d93bc31ff036cc2588f162183abd9ab10182e32f`, parent `a3f5bd39d72e1dfc5361a8d2c213ef0f7cb79cc5`. I reviewed committed content only.
- **Provenance limit:** I can read files but cannot run Git. The commit identity, the parent link, the receipt's normalized SHA-256 values and its diff hash are all checks the author ran, not ones I ran.
- **What I did confirm:** the working-tree files match the patch's final versions for all seven articles and for the appended JSON. The only lines removed are the seven changed exclusion lines, the old 仮定 explanation line, and the JSON `]` that became `],`.

## Scope
- **Model:** claude-opus-5.5 (family: claude). I worked sequentially, delegated nothing and edited nothing.
- **Changed articles:** I read all seven in full: 被せる, 学会, 学級, 活躍, 兼ねる, カバー and 仮定.
- **Comparison cards:** I read all twelve in full: 浴びせる, 大会, 授業, 参加, 難しい, どうしても, 皮, もし, もしも, 着る, 乗せる and 組合. I also read 仮名遣い and 送り仮名, and checked the titles of 困難, 大変, 無理, 置く, 履く and 被る.
- **Source packet (`batch-16.json`):**
  - all thirteen added comparison families (lines 15302–16510);
  - the full correction record (16511–end): the twelve exclusion pairs, the teaching clarifications, the two new source-check notes and the notes on optional leads;
  - the existing 授業 entry (1330290);
  - the main entries for 仮定 (1187870), 学会 (1206610), 学級 (1206680), 活躍 (1208450), 兼ねる (1256520), カバー (1037960) and 被せる (1484320).
- **Other checks:** the quiz-exclusion rules in `docs/content-format.md`, and a search of `words\` for `quiz_distractors` conflicts (none).
- **Not done:** no fresh full-batch review. I read the comparison cards, but my verdicts don't cover them as whole cards.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 被せる | CLEAN | CLEAN | CLEAN |
| 学会 | CLEAN | CLEAN | CLEAN |
| 学級 | CLEAN | CLEAN | CLEAN |
| 活躍 | CLEAN | CLEAN | CLEAN |
| 兼ねる | CLEAN | CLEAN | CLEAN |
| カバー | CLEAN | CLEAN | CLEAN |
| 仮定 | CLEAN | CLEAN | CLEAN |
| Packet additions | CLEAN | CLEAN | CLEAN |

- **Exclusion lists:** the twelve new pairs match the twelve declared pairs exactly. Every target exists, and there are no duplicates, self-references or `quiz_distractors` conflicts.
- **Source senses:** each pair cites a sense that actually carries the overlapping English meaning. Examples: 大会 sense 1 "convention, conference"; 組合 sense 1 "association"; 皮 sense 3 "sheath, wrapping"; 着る sense 1 "put on"; 乗せる sense 1 "place on".
- **どうしても:** the cited sense 3 carries the note "with neg. verb", which the stated reason reflects.
- **もし:** the separate 模試 and interjection entries read もし are kept but correctly not used to justify anything.

## Findings
**My original findings**
- **F1 (仮定.md:21): resolved.** Line 21 now presents "plain clause + と仮定する" as one useful way to state a premise. It explains the existing 一万円だ example without turning it into a rule, and both examples and their translations are unchanged.
  - My suggested wording ("often keeps だ") would itself have been an unsupported frequency claim, so it was right not to adopt it.
  - My evidence, the 1887–88 example on the dictionary page, only justifies dropping the overbroad rule. It does not support a modern frequency claim.
- **F2 (被せる/浴びせる): resolved.** 被せる.md:9 now excludes 浴びせる, which directly protects the taught "pour over" sense (JMdict 1484320 sense 3 vs 1547440 sense 1).
- **F3 (兼ねる): resolved.** 兼ねる.md:9 now excludes 難しい ("hard to do") and どうしても ("simply cannot"). No new construction teaching was added.
- **F4 (学級/授業): resolved.** 学級.md:9 now excludes 授業. Line 29 still keeps the group/lesson distinction.

**My original optional suggestions**
- カバー/皮, 仮定/もし and もしも (each excluded directly), 被せる/着る and 乗せる, and 学会/組合: all adopted.
- 仮名遣い/送り仮名: **withdrawn.** The two answer labels describe a whole spelling system versus one spelling device, and they don't overlap. That matches the separate official standards 現代仮名遣い and 送り仮名の付け方 (from my own knowledge).
- 括弧 する example and 担ぐ "fool someone" example: still optional. Neither article changed.

**New pairs I hadn't proposed**
- 学会/大会: justified by 大会's "convention" sense.
- 活躍/参加: justified by 活躍's "active participation" gloss. 参加.md already says participation does not imply a large contribution.

**Regressions:** none found.

## Optional
- 兼ねる vs 困難 ("difficulty; difficult") or 無理 ("impossible"): a low-risk extra exclusion. I didn't treat it as a defect, because those are adjective-style labels rather than "hard to do".
- 仮定: an XをYと仮定する example is still optional.
- The original `quizDeclarations` block was deliberately left unchanged. A reader needs the correction record's exclusion pairs alongside it to see the current lists.

## Limits
- I couldn't run Git or hash files, so commit identity, the parent link and all hashes are the author's claims.
- **Manifest:** the receipt lists a hash for `manifest.json`, but the supplied diff doesn't include that file. The repository rules require committing a regenerated manifest; otherwise CI fails and the app drops cards whose hashes changed. I couldn't confirm it was regenerated in `d93bc31`.
- I didn't fetch JMdict myself, so I couldn't confirm the thirteen added entries are complete.
- In this pass I didn't fetch the Bunpro page. The failed university PDF is not evidence. I fetched the Kotobank 仮定 page in my original review.
- I didn't run the app, the validator or a quiz draw. Whether the examples sound natural is my judgment, not native-speaker certification.
