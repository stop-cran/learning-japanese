# Batch 147 revision: what changed from 6a2323e7 to 99487bb5

Revised snapshot: `99487bb5` (full hash `99487bb5bef47b4e43be5b3223db7cb4dbb3bec1`; also in `packet-manifest.json`). It is reached from the
reviewed snapshot `6a2323e759d4e4f2e78bc039c8b9eb8914ac2d0c` by two commits, `0df56686` (made after an earlier review round) and `99487bb5` (made after a later review round). `diffs\fix.patch` is their combined patch.
Nothing is published.

- Ten new kanji cards changed (矢 砕 礎 秀 秘 稚 穏 穴 粋 糧). The other five new cards (瞬 瞳 稼 稿 笛), the three
  modified existing cards (基 密 透), all word articles and all 15 stroke files are unchanged from the reviewed snapshot.
- **Front-matter changes (quiz_exclusions only):**
  - 矢: `[印, 示, 標, 符, 方, 恋, 念]` became `[印, 示, 標, 符]` (3 removed: 方 恋 念).
  - 砕: `[壊, 破, 割, 崩, 倒, 滅, 粉, 細, 単, 易, 簡, 悩, 磨]` became `[壊, 破, 割, 崩, 倒, 滅, 粉, 細, 磨]` (4 removed: 単 易 簡 悩).
  - 稚: 熟 removed (now `[幼, 若, 児, 童, 苗, 嬢, 子]`).
  - 糧: 貯 and 備 removed (now `[食, 飯, 穀, 養, 給]`).
  - 穴: 秘 added (now `[凹, 巣, 欠, 差, 窓, 秘]`).
  No title, tag, metadata reading or `distractors` list changed in any card.
- `manifest.json` was regenerated; it is a generated index and outside the review.
- Line numbers below refer to the revised snapshot in this packet. No card gained or lost a line.
- `diffs\fix.patch` is the exact patch from `6a2323e7` to `99487bb5`. `diffs\changed-lines.txt` lists the changed lines per file.
- No Metadata line changed. New evidence in this packet is everything under `evidence\`; `evidence\README.md` describes each file.

| File | Changed lines | Change |
| --- | --- | --- |
| 矢 | 14, 27, 46-47 | Line 14: exclusions as above. Line 27: the mnemonic speaks of a long sweeping stroke through the middle (was "vertical stroke"). Lines 46-47: the exclusion note no longer names 方 恋 念; the distractor note says 午 and 牛 share a long central stroke and crossing bars, and 天 shares the two bars and the spreading lower strokes. |
| 砕 | 14, 25, 49 | Line 14: exclusions as above. Line 25: `fine, small` is now `fine or small` (no quotation marks). Line 49: the exclusion note no longer names 単 易 簡 悩, and the title of 滅 is quoted exactly ("perish; destroy; die out"). |
| 礎 | 27 | The title of 林 is quoted exactly ("grove; woodland"). |
| 秀 | 27, 46 | Line 27: 禾 is at the top and 乃 below it (was left and right). Line 46: the 優 sentence says the title and the meaning of すぐれる overlap this card's meaning. |
| 秘 | 41 | The ひそ.か row is labelled "kun, outside the official table". |
| 稚 | 14, 40, 52 | Line 14: 熟 removed. Line 40: the okurigana sentence now reads 稚い as いとけな + い, and 稚けない as the いとけ split. Line 52: the exclusion note drops 熟 and says it is the opposite of "immature". |
| 穏 | 39, 48 | Line 39: 穏和 is given its personality and statement senses, and the climate sense is said to be written 温和 only. Line 48: the note says that all three distractors are Starter cards with kun readings, so やす.らか of 安 cannot be drawn. |
| 穴 | 14, 50 | Line 14: 秘 added. Line 50: the note says 秘 overlaps the figurative sense "well-kept secret" of the word 穴. |
| 粋 | 33 | The mnemonic describes a part that looks like 九 above 十 (a simplified form of 卒; 卒 itself is not written here). |
| 糧 | 14, 49 | Line 14: 貯 and 備 removed. Line 49: the exclusion note drops them. |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: 0 errors, 2 warnings (the existing word articles 瞳 and 透明: "Dictionary: line cites no JMdict entry id"),
  as at the freeze. `unittest.txt`: 439 tests, OK. `validate.txt`: 0 errors. `manifest.txt`: `manifest.json` regenerated,
  rebuild idempotent. `linkplan.txt` and `kanji-remarks.txt`: 0 problems.
- `quiz-safety.txt`: 0 errors, 0 warnings (rerun because exclusions changed).
- `reading-exposure.txt`: 0 production hits, 0 padded-session hits, 7 latent collisions, as at the freeze.
- `reading-options.txt`: the same one problem as at the freeze (the older check flags the unlisted reading やすらか of 穏
  as offered by 安; the authoritative reading-exposure audit shows it cannot be drawn).
- The Android JVM tests that read the real content were not run, as at the freeze.

## Process notes

- `0df56686` and `99487bb5` are the two fix commits; `diffs\fix.patch` is the whole change from the reviewed snapshot `6a2323e7`.
- The checks in `checks\` were run on the committed revision `99487bb5`.
