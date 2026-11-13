# Batch 113 revision: what changed from fdec1c02 to b750f350

Revised snapshot: `b750f3509ed8bff0a0a2ee1e1ad73f33f6798946`, a child of the reviewed snapshot
`fdec1c02f9b02f29659b56551cd0a1fd927cced1`. Nothing is published.

- 13 of the 15 kanji cards changed: 慢, 縫, 飢, 恩, 盆, 誕, 系, 徹, 討, 謝, 握, 寧 and 援. The other two (隊 and 需) are
  unchanged, and so are all 15 stroke files, all titles, all `distractors`, all reading rows and selections, every word
  article, and the two existing cards whose remarks the batch edits (応 and 統).
- Front matter changed only in `quiz_exclusions` (line 14) of 12 cards: every changed card except 飢. Each list only
  gained entries; none was removed. 飢's front matter is unchanged. Titles, tags, `distractors` and metadata readings are
  unchanged on all 15 cards.
- Body text changed only in Notes bullets, and in 飢's opening paragraph (lines 23-25) and its conjugation sentence (lines
  49-51). No Common words, Readings or Metadata line changed.
- `manifest.json` was regenerated (contentVersion `8fe45e2ba015abcc`); it is a generated index and outside the review.
- Line numbers below refer to `snapshot\kanji\<card>.md` in this packet (the revised snapshot).
- `diffs\fix.patch` is the exact patch. `diffs\changed-lines.txt` lists the changed lines per file.
- Links: `checks\link-targets.tsv` lists every link on a changed line (47 links, 0 unresolved, 0 mismatched). That table
  compares only a gloss whose quotation marks open and close on the same line as the link: 36 such glosses equal the
  linked card's `title:`. The other 11 rows show `n/a` because the quoted title wraps onto the next line (寧:73 御, 寧:83
  念, 徹:73 終, 徹:74 卒, 徹:81 達, 慢:68 軽, 援:70 守, 援:72 貯, 討:79 学, 討:84 思 and 謝:82 変). The author's script joined
  each such line with the next and compared the quoted gloss with the real title: all 11 match.
- New evidence in this packet is everything under `evidence\`: the complete JMdict entries cited by the new text (see
  `evidence\README.md` for the list) and the app's `QuizBuilder.kt`. No Joyo page extract is supplied, because no reading
  changed. All other evidence stays in the original packet.

| Card | Changed lines | Change |
| --- | --- | --- |
| 慢 | 14, 68-71 | Line 14: `quiz_exclusions` gains 軽: `[遅, 鈍, 凌, 負, 節, 永, 軽]` (it read `[遅, 鈍, 凌, 負, 節, 永]`). Lines 68-71 are a new bullet: `- Conceit that looks down on others overlaps [軽](軽.md), "lightweight; slight," whose 軽んじる means to look down on or make light of something, and whose "slight" can also name a snub. Arrogance is not low physical weight.` |
| 縫 | 14, 67-70 | Line 14: gains 結, 接 and 修: `[針, 経, 通, 結, 接, 修]` (it read `[針, 経, 通]`). Lines 67-70 are a new bullet: `- Sewing joins or mends cloth, and 縫合 is sewing together, so 縫 overlaps [結](結.md), "tie; join; conclude," [接](接.md), "touch; join," and [修](修.md), "repair; amend; cultivate," whose 修繕 is repair or mending. Tying a knot or repairing a machine is not sewing.` |
| 飢 | 23-25, 49-51 | Lines 23-25 replace the one-line opening `飢 concerns hunger severe enough to amount to starvation.` with `飢 concerns hunger from a lack of food, ranging from being hungry to starving; its words usually describe serious deprivation, and for everyday hunger お腹が空く おなかがすく is the usual expression.` The next sentence (line 26, `[飢える](../words/飢える.md) うえる means to starve or be famished, ...`) is unchanged. Lines 49-51 replace `... it is an intransitive ichidan verb, so える stays in forms such as 飢えて and 飢えない. JMdict also lists かつえる,` with `... it is an intransitive ichidan verb, so the final る changes while the stem うえ- stays: うえる becomes うえて, 飢えて, and うえない, 飢えない. JMdict also lists かつえる,`. The rest of that paragraph is unchanged. |
| 恩 | 14, 67-69 | Line 14: gains 愛: `[利, 享, 福, 幸, 好, 良, 礼, 謝, 義, 役, 愛]` (it ended at 役). Lines 67-69 are a new bullet: `- The affection and benevolence in いつくしみ overlap [愛](愛.md), "love," whose card covers affection and care, not only romance. 恩 is still a kindness received, not love in general.` |
| 盆 | 14, 67-70 | Line 14: gains 盤 and 缶: `[皿, 器, 盤, 缶, 凹, 谷, 祭, 家, 戸, 族, 氏, 姓]` (it read `[皿, 器, 凹, 谷, 祭, 家, 戸, 族, 氏, 姓]`). Lines 67-70: the bullet that begins at line 65 kept its first two sentences and now continues `[盤](盤.md), "board; disc," also has a documented vessel sense, which overlaps 盆's shallow vessel or tray; this does not make every board or disc a tray. [缶](缶.md), "tin can; container," shares the word "container" with a shallow vessel, although 盆 is never a can.` (it ended at `sense.`). |
| 誕 | 14, 68-70 | Line 14: gains 造, 始 and 緒: `[生, 産, 創, 作, 元, 本, 原, 造, 始, 緒, 寝]` (it read `[生, 産, 創, 作, 元, 本, 原, 寝]`). Lines 68-70 continue the bullet that begins at line 64: `Making and beginning also overlap [造](造.md), "make; construct," [始](始.md), "begin, start," and [緒](緒.md), "cord; beginning," though 誕 never means building something or a cord.` |
| 系 | 14, 74-77, 81-83 | Line 14: gains 種, 般 and 列 (`... 係, 型, 種, 般, 番, 線, 並, 列, 弧, ...`). Lines 74-77: after the unchanged `This card declares the pair 系–隊.` the bullet continues `The colloquial "-type; -ish" sense also overlaps [種](種.md), "seed; kind," and [般](般.md), "general; kind; category," through "kind" and "category," not through seeds or generality.` Lines 81-83: the relation/series bullet now names `[列](列.md), "row; queue,"` before 弧 and ends `列 names an ordered line or row; 系 concerns connected lines and series, as in 系列, without making every queue a lineage or system.` |
| 徹 | 14, 73-77, 81-82 | Line 14: gains 終, 済, 卒 and 専 after 了, and 到 at the end. Lines 73-77 are a new bullet: `- Carrying something through to the end, as in 貫徹, overlaps [終](終.md), "end; finish," [済](済.md), "settle; finish," and [卒](卒.md), "graduate; finish," through "finish," without making 徹 a word for graduating. Devoting oneself exclusively, as with 徹する, overlaps [専](専.md), "specialize; exclusive."` Lines 81-82: the piercing/reaching bullet now ends `[届](届.md), "reach; deliver; notify," [達](達.md), "reach, plural suffix," and [到](到.md), "arrive; attain."` (it ended `... and [達](達.md), "reach, plural suffix."`). |
| 討 | 14, 79-86 | Line 14: gains 話, 争 and 評 after 談, and 思 after 考. Lines 79-86: the discussion bullet (from line 76) now lists `[争](争.md), "contend; dispute,"` before 考 and continues after 研 `争う can mean to argue or compete, overlapping debate or contention; not every discussion is a dispute, and not every dispute is an armed attack. Discussion is also talking, and considering a proposal involves thinking it over and appraising it, so 討 overlaps [話](話.md), "talk, speak," [思](思.md), "think, feel," and [評](評.md), "appraise; reputation." 討 does not mean reputation.` |
| 謝 | 14, 78-79, 82-83 | Line 14: gains 変 after 更 and 給 after 料. Lines 78-79: after `because of 謝礼 and 月謝.` the bullet adds `Paying an honorarium or a fee also overlaps [給](給.md), "pay; bestow."` Lines 82-83: the replacing/renewing bullet now ends `[更](更.md), "renew; grow late," and [変](変.md), "change; strange," because replacing the old with the new is a change.` (it ended at 更's title). |
| 握 | 14, 74-77, 80-84 | Line 14: gains 扱 after 責, and 管, 知 and 識 after 治. Lines 74-77 are a new bullet: `- [扱](扱.md), "handle; deal with," shares the English word "handle" with 握り. Here 握り names a grip or handle, while 扱う is the verb for handling or dealing with something. This exclusion separates the English labels; it does not make those Japanese words interchangeable.` Lines 80-81: the control bullet (from line 78) now ends `[治](治.md), "govern; heal," [圧](圧.md), "pressure; oppress," and [管](管.md), "pipe; supervise," through control and supervision.` Lines 82-84 are a new bullet: `- Grasping a situation, as in 把握, or holding the answer overlaps [知](知.md), "know," and [識](識.md), "knowledge; awareness." 握 is still a grip, not knowledge in general.` |
| 寧 | 14, 67-68, 73-78, 83-84 | Line 14: gains 和 after 凪, 御, 様, 尊 and 拝 after 礼, and 念 at the end. Lines 67-68 end the peace bullet (from line 64): `[和](和.md), "harmony; Japanese style," also has a peace sense, as in 平和; the comparison is with peace, not Japanese style.` Lines 73-78 are a new bullet: `- Respectful wording also connects courtesy with [御](御.md), "honorific; govern," and [様](様.md), "manner; honorific suffix": 御 can add a polite prefix and 様 a respectful suffix. [尊](尊.md), "revere; esteem," concerns respect, and [拝](拝.md), "worship; bow in respect," also appears in humble expressions such as 拝見. These comparisons concern respect and courtesy, not governing, every manner, or religious worship.` Lines 83-84: the care bullet (from line 79) adds `Careful attention also overlaps [念](念.md), "thought; attention."` before its unchanged closing sentence. |
| 援 | 14, 70-72 | Line 14: gains 守 and 防 after 保. Lines 70-72: the helping bullet (from line 66) now reads `[保](保.md), "protect; preserve," overlaps the "save" sense, as do [守](守.md), "guard; obey," and [防](防.md), "defend; ward off," through protection and rescue; not every act of aid is defense. [貯](貯.md), "save up; store," ...` (it read `... overlaps the "save" sense, and [貯](貯.md), "save up; store," ...`). |

## Checks run on the revised snapshot (outputs in `checks\`)

- `lint.txt`: the batch linter on 17 kanji cards (the 15 batch cards and 応 and 統) and 40 word articles: 0 errors, 10
  warnings, all of the kind "Dictionary: line cites no JMdict entry id" on word articles. The output is the same as the
  original packet's `checks\lint.txt`; no word article changed.
- `unittest.txt`: 431 tests, OK. `validate.txt`: 0 errors. `budget.txt`: content archive budgets met (8,638 files).
  `vocabulary.txt`: vocabulary coverage check passes (2122 of 2431 reviewed prompts, stage pilot). `manifest.txt`:
  `manifest.json` regenerated (8631 files, version 8fe45e2ba015abcc) and committed; a second rebuild changed nothing.
- The Android app's JVM tests were not run for this revision, so there is no `jvm.txt`. JVM and emulator work is held, as
  the original packet's `REVIEW.md` says for the reviewed snapshot.
- `link-targets.tsv`: see the Links bullet above.
- `quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt` and `reading-options-freeze.txt`: see the next section.

## Quiz mechanics the changes rely on

- The repository validator's rules (all pass; `validate.txt`: 0 errors): `quiz_exclusions` has no duplicates, no self,
  every entry has a card, and no entry may also be one of the same card's `distractors`.
- Meaning quiz: the app's `QuizBuilder` is in `evidence\QuizBuilder.kt` (Android checkout at commit `10d98d0`).
  `excluded(a, b)` (line 26) is true if **either** card lists the other, so a pair needs to be listed on one side only.
  `tryAdd` (lines 28-32) skips any candidate excluded against the target or against an option already chosen (line 30).
  The curated `distractors` present in the pool `all` are tried first, in order (line 34); then the other cards of that
  pool, shuffled and ordered by the number of shared tags (lines 35-36). The documented contract is in the original
  packet's `repo\docs\content-format.md`, lines 102-107 (symmetric, not transitive; All, level and custom pools; an
  excluded card is never restored; meaning choices only) and lines 109-112 (older APKs do not enforce the field).
- `checks\quiz-safety.txt` shows, for each of the 15 cards, the correct title in parentheses after the kanji, followed by
  the three wrong meaning options now offered in the full pool. It is the same as the original packet's copy: every card
  still shows its three curated distractors, and no shown option changed. So in the full pool the new exclusions act only
  on fallback candidates (drawn when fewer than three curated distractors are usable, for example in a pool that lacks
  some of them) and, being symmetric, on the counterparts' questions as well.
- Reading quiz: `quiz_exclusions` affect only the meaning quiz (`content-format.md` line 107), and no reading, reading
  selection, distractor or title changed. `checks\reading-exposure.txt` is the same as the original packet's copy (line
  222: 0 production hits, 0 padded-session hits, 7 latent collisions). `checks\reading-options.txt` (every card in
  `kanji\` as the pool, 100 seeds per prompt) was run on the revised snapshot, and `checks\reading-options-freeze.txt` on
  the reviewed snapshot; the two outputs are byte-identical. Both report one problem, unchanged by this revision: 援's
  `おん` (card text) can be drawn as a wrong option on the エン prompt, offered by 恩 温 遠 音 飲 (line 251), the scenario
  described in your L2. The helper labels every extra reading "(card text)" whatever its origin; this `おん` comes from a
  saved Wiktionary snippet that the card does not state, as the original packet's `REVIEW.md` (lines 76-86) says.
- Exclusion changes in this revision: 36 new pairs, each declared once, on the batch card's side: 慢/軽, 縫/結, 縫/接,
  縫/修, 恩/愛, 盆/盤, 盆/缶, 誕/造, 誕/始, 誕/緒, 系/種, 系/般, 系/列, 徹/終, 徹/済, 徹/卒, 徹/専, 徹/到, 討/思, 討/話,
  討/評, 討/争, 謝/変, 謝/給, 握/扱, 握/管, 握/知, 握/識, 寧/御, 寧/和, 寧/念, 寧/様, 寧/尊, 寧/拝, 援/守 and 援/防. The 36
  counterpart cards are unchanged; the original packet's `repo\kanji\` holds all 1,206 cards of the reviewed snapshot, and
  only the 13 cards above differ from it. Author's script over all 1,206 cards at the revised snapshot: no counterpart
  lists its batch card in `quiz_exclusions` or `distractors`; no batch card lists a counterpart in `distractors`; no card
  lists both members of a new pair in `distractors`; every counterpart has three `distractors`. No exclusion was added
  between two counterparts.
