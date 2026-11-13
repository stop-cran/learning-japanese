# Batch 114 revision: what changed from 8c2bdc27 to ac38b8e4

Revised snapshot: `ac38b8e4427afc2c10a957871c5ec99e9cb92bda`, a child of the reviewed snapshot
`8c2bdc27e5d556e639a4d0e9239ae5f2009c400f`. Nothing is published.

- 6 of the 15 kanji cards changed: 寮, 穫, 魅, 穀, 碁 and 症. The other nine (娯, 廊, 栓, 汽, 砲, 磁, 糖, 紺 and 雰) are
  unchanged, and so are all 15 stroke files, all titles, all `distractors`, all reading rows and selections, and every
  word article.
- Front matter changed only in `quiz_exclusions` (line 14) of five cards: 寮, 穫, 魅, 穀 and 碁. Each list only gained
  entries; none was removed. 症's front matter is unchanged.
- Body text changed only in Notes bullets, and in one Common words gloss of 症 (line 50). No Meaning, Readings or
  Metadata line changed.
- No existing card outside the batch changed. Every pair added in this revision is declared on the batch card's side.
- `manifest.json` was regenerated (contentVersion `c78ebbacf53520b6`; it was `20f92e77ce1686f0`); it is a generated index
  and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Links: `checks\link-targets.tsv` lists every link on a changed line. The new links are followed by unquoted descriptive
  phrases, not quoted titles, so the table's title comparison shows `n/a` for them. The author compared each phrase with
  the linked card's real `title:`: 盤 "board/disc" (title `board; disc`), 板 "plank" (`plank; board`) and 怪
  "suspicious/uncanny" (`suspicious; uncanny`).
- `checks\quiz-safety.txt` and `checks\reading-exposure.txt` are byte-identical to the original packet's
  `checks\quiz-safety.txt` and `checks\reading-exposure-final.txt`: no curated wrong option and no modelled reading draw
  changed. `checks\reading-options.txt` is new in this round; it was produced at the revised snapshot.
- New evidence in this packet is everything under `evidence\`: the complete JMdict entries cited by the new text or by
  the author's statement (see `evidence\README.md`) and the app's `QuizBuilder.kt`. No Joyo page or KanjiVG record is
  supplied, because no reading or stroke file changed. All other evidence stays in the original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 寮 | 14, 63-64, 66-70 | Line 14: `quiz_exclusions` gains 房 after 室, and 庁, 部 and 課 at the end: `[宿, 宅, 住, 家, 室, 房, 館, 亭, 官, 局, 署, 府, 庁, 部, 課]` (it read `[宿, 宅, 住, 家, 室, 館, 亭, 官, 局, 署, 府]`). Lines 63-64: the room clause now reads `Room and accommodation uses connect with [室](室.md), [房](房.md) and [館](館.md); the tea-pavilion sense connects with [亭](亭.md).` (it named only 室 and 館). Lines 65-70: the bureau bullet now reads `Historical official or bureau senses overlap [官](官.md), [局](局.md), [署](署.md), [府](府.md) and [庁](庁.md). A bureau beneath a ministry also overlaps the organizational units [部](部.md) and [課](課.md). These direct comparisons are excluded from choices; the exclusion does not equate every modern institution or authorize swapping its name.` (it named 官, 局, 署 and 府 only, and its last sentence is unchanged apart from line wrapping). |
| 穫 | 14, 58-66 | Line 14: gains 集 and 拾 after 取, 利 after 得, and 績 at the end: `[刈, 収, 採, 取, 集, 拾, 得, 利, 捕, 果, 実, 績]` (it read `[刈, 収, 採, 取, 得, 捕, 果, 実]`). Lines 58-61: the gathering bullet now lists `[収](収.md), [採](採.md), [取](取.md), [集](集.md) and [拾](拾.md)` as overlapping "gathering or taking in"; its 刈 sentence is unchanged. Lines 62-66: the 収穫 bullet now reads `In the extended uses of 収穫, gains connect with [得](得.md) and [利](利.md), a catch with [捕](捕.md), and fruitful results with [果](果.md), [実](実.md) and [績](績.md).`; its last sentence is unchanged apart from line wrapping. |
| 魅 | 14, 60-61, 63 | Line 14: gains 怪: `[妖, 怪, 符]` (it read `[妖, 符]`). Lines 60-61: the bullet now reads `[妖](妖.md) overlaps bewitching attraction and supernatural beings; [怪](怪.md), suspicious/uncanny, overlaps the supernatural sense.` (it ended after "supernatural beings."). Line 63: `Both comparisons are excluded` became `These comparisons are excluded`. |
| 穀 | 14, 69-72 | Line 14: gains 穂 after 稲: `[米, 麦, 稲, 穂, 種, 粒, 実]`. Lines 68-70: the 穂 bullet keeps its first sentence and now continues `Like the rice plant, its displayed grain wording is close enough that the pair is excluded from choices.` Lines 71-72: the sentence about the indexing key (`The source's classical indexing key is 禾; its separate Nelson classification under 殳 does not replace that key.`), which closed the 穂 bullet, is now its own bullet, unchanged in wording. "The rice plant" refers to 稲, named in the bullet at lines 61-63. |
| 碁 | 14, 59-62 | Line 14: `quiz_exclusions: [盤]` (it was empty). Lines 59-62 are a new bullet: `- [盤](盤.md), board/disc, names the Go board itself, as in 碁盤 ごばん. Because it is the game's own equipment and the title also says board, this direct pair is excluded from choices; the game and its board remain different meanings. [板](板.md), plank, is not that equipment.` The unchanged bullet at lines 65-67 still says that a shared game-related topic alone is not an exclusion rule. |
| 症 | 50 | The Common words row `重症 じゅうしょう - serious illness; severe condition` now reads `重症 じゅうしょう - serious illness`. |
