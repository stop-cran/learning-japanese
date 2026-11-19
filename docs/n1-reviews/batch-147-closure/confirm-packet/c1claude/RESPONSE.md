# Author's statement for the reviewer of `reports-147\initial-claude.md`

This statement answers only the points in YOUR initial report. C1 to C7 are your report's own Findings labels; your
Optional section has seven bullets, called O1 to O7 below in the order of the report (O1 the 砕 quoted translation, O2 the
矢 coverage, O3 the 秘 ひそ.か label, O4 the two 穏 points, O5 the 穴 JMdict entry 1254490 senses, O6 the 礎 title in the 基
diff, O7 the 純粋 article). The statement is the author's claim about what changed and why. Verify each claim against the
revised text in `snapshot\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Card line
numbers refer to the revised cards in this packet. Ten cards changed (矢 砕 礎 秀 秘 稚 穏 穴 粋 糧) and five
`quiz_exclusions` lists changed (矢 砕 稚 糧 穴); see `CHANGES.md`. Give a disposition for each of C1 to C7 and O1 to O7.

## Findings

### C1: 秀 mnemonic places 禾 and 乃 left and right

Author action: **changed** as you proposed. `秀.md:27` says 禾 is at the top and 乃 below it.

### C2: 粋 mnemonic names 卒

Author action: **changed**. `粋.md:33` now describes a part that looks like 九 above 十 and says it is a simplified form of 卒
and that 卒 itself is not written in 粋.

### C3: 稚 okurigana sentence

Author action: **changed** as you proposed. `稚.md:40`: 稚い is いとけな + い; 稚けない is the いとけ split.

### C4: 矢 has no vertical stroke

Author action: **changed**. `矢.md:27` speaks of a long sweeping stroke through the middle; `矢.md:47` (distractor note) says
午 and 牛 share a long central stroke and crossing bars, and 天 shares the two bars and the spreading lower strokes.

### C5: quoted titles not exact

Author action: **changed**. `礎.md:27` quotes 林 as "grove; woodland"; `砕.md:49` quotes 滅 as "perish; destroy; die out".

### C6: over-broad exclusions on 矢 and 砕

Author action: **changed**. 方 恋 念 removed from 矢 (`矢.md:14`, note `46`); 単 易 簡 悩 removed from 砕 (`砕.md:14`, note `49`).

### C7: 穏 distractor reason

Author action: **changed**. `穏.md:48` now says all three distractors are Starter cards with kun readings that fill every
wrong slot of the おだ.やか question, so the reading やす.らか of 安 cannot be drawn.

## Optional

- **O1 (砕 quoted translation): applied.** `砕.md:25` reads `fine or small` with no quotation marks.
- **O2 (矢 coverage of 無理矢理 and 矢張り): not applied.** Optional extra words; the card already teaches the quizzed readings.
- **O3 (秘 ひそ.か label): applied.** `秘.md:41` reads "kun, outside the official table".
- **O4 (穏 line 25 examples; 温和 heading): partly applied.** The 温和 spelling is now stated on `穏.md:39`. The line 25 list is Daijisen's own and is not changed.
- **O5 (穴 JMdict 1254490 tags and fourth sense): not applied.** Polish.
- **O6 (礎 title in the 基 diff): not applied.** The declared remark edit stays as it is.
- **O7 (純粋 article): not applied.** Outside the diff.

## Process notes

- `0df56686` and `99487bb5` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `6a2323e7`.
- `99487bb5` also follows a later review round (not shown to you); see `CHANGES.md` for all changed lines.
- The checks in `checks\` were run on the committed revision.
