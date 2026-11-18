# Author's statement for the reviewer of `reports-112\initial-claude.md`

This statement answers only the points in YOUR initial report. IDs F1, F2 and F3 are your report's own labels, and so are
O1, O2 and O3 in your Optional section; the two sub-bullets of O2 are called **O2(a)** (展 and 敷) and **O2(b)** (妙 and
技/腕). **L1** is the second bullet of your Limits section (custom or caller-built pools, multi-borrow Starter, actual
Kotlin draws and fallback level-pool behaviour, native execution and phone acceptance). The statement is the author's claim
about what changed and why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and
independent sources; do not rely on this text as evidence. Line numbers refer to the revised cards in this packet. Eight of
the 15 cards changed (妙 就 展 微 態 盤 診 障) and the other seven did not (see `CHANGES.md`). Give a disposition for each of
F1, F2, F3, O1, O2(a), O2(b), O3 and L1.

## Findings

### F1 (moderate): 微 "minute; faint" collides with 分 "minute, part"

Author action: **changed, by your first remedy** (a quiz exclusion). The title `minute; faint` is unchanged.

- `微.md:14`: `quiz_exclusions: [細, 小, 少, 薄, 弱, 分, 軽]`. 分 and 軽 are the additions; the list ended at 弱 before. For
  軽, see "Changes that do not answer a point" below.
- `微.md:68-71` is a new Notes bullet: `- Here English "minute" means tiny, not the unit of time associated with
  [分](分.md). That card's title is "minute, part"; the shared English spelling is excluded from meaning choices without
  treating the Japanese meanings as interchangeable.`
- `分.md` is unchanged: title `minute, part`, `distractors: [今, 半, 木]`, no `quiz_exclusions`. One declaration guards
  both directions, because `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other:
  分 cannot be offered as a wrong option in a 微 question, and 微 cannot be offered in a 分 question.
- Why the title was kept. "Minute" in the sense of tiny is supported by KANJIDIC2, which gives 微 the meanings "delicate",
  "minuteness" and "insignificance" (`evidence\kanjidic2-records.xml` in the original packet), and the card's first
  sentence (`微.md:23`) says `微 concerns something very small, slight or difficult to notice.` Your first example title,
  "tiny; faint", would also remove the shared word; it was not taken because the exclusion keeps 分 and 微 apart in both
  directions in exclusion-aware builds and the present title follows KANJIDIC2. Your second example, "slight; faint",
  would put "slight" into a second title: 軽 is `lightweight; slight`. Author's title scan over all 1,191 cards: the only
  titles containing "minute", "slight", "tiny", "faint" or "subtle" are those of 分, 微 and 軽.
- Disclosure: older APKs do not enforce `quiz_exclusions` (`content-format.md` lines 109-112 in the original packet's
  `repo\docs\`), so this remedy does not protect the 5c000bd APK your third Limits bullet mentions; a retitle would. The
  same holds for every other `quiz_exclusions` entry in the repository. No claim is made about any installed build.

To verify: that the exclusion removes the collision in both directions, that `微.md:68-71` is accurate and clear, and
whether keeping the title is acceptable.

### F2 (moderate): 就 shares "undertake" with 企 and 承

Author action: **changed, by exclusion**, including the two pairs you suggested considering (担 and 職) and the weaker one
you named (位). 就's title `take a position; undertake` is unchanged.

- `就.md:14`: `quiz_exclusions: [着, 付, 任, 定, 成, 始, 去, 発, 学, 企, 承, 担, 職, 位, 了, 完, 済]`; the list ended at 学
  before. For 了, 完 and 済, see "Changes that do not answer a point" below.
- `就.md:74-78` is a new Notes bullet: `- "Undertake" also appears in the titles of [企](企.md), plan/undertake, and
  [承](承.md), accept/undertake. [担](担.md), shoulder/take on, overlaps taking on a responsibility. [職](職.md),
  employment/post, and [位](位.md), rank/position, overlap the position sense. These comparisons are also excluded; the
  complete words still differ in use.`
- 位: you called "rank; position" against "take a position" weak. It was added because the card teaches the position
  sense itself: `就 concerns taking up a position or beginning an activity.` (`就.md:23`) and `[就任](../words/就任.md)
  しゅうにん is assuming a particular post.` (`就.md:25`). Please say if you judge the pair over-broad.
- The counterpart cards are unchanged and none lists 就 in `quiz_exclusions` or `distractors`: 企 `plan; undertake`
  `[危, 休, 全]`, 承 `accept; undertake` `[水, 手, 了]`, 担 `shoulder; take on` `[指, 押, 招]`, 職 `employment; post`
  `[耳, 聞, 音]`, 位 `rank; position` `[立, 住, 体]`. 就's own `distractors` are `[京, 秋, 州]` and its shown options are
  unchanged (`checks\quiz-safety.txt`, line 8).

To verify: that each added pair is a real direct overlap and not over-broad, and that 就 keeps three defensible wrong
options.

### F3 (polish): the 態 Notes call the てい, なり and ざま entries "separate 態 entries"

Author action: **changed, with different wording.**

- `態.md:62-63` now read `- JMdict also lists 態 as an additional spelling in the entries headed by 体 (てい), 形 (なり) and
  様 (ざま).` They read `- Dictionaries also have separate 態 entries read てい, なり and ざま.` The next line (64), `They are
  not alternate pronunciations to insert into 態度 or 状態;`, is unchanged.
- Your suggested "less common alternative spelling" was not used. In the three entries (JMdict 1409160 体/態 てい, 2138450
  形/態 なり and 1410750 様/態 ざま; complete in `evidence\jmdict-cited-entries.xml`) 態 is the second kanji form, and its
  kanji element carries no information tag such as a rare-form or irregular-form tag, so the packet has no source for
  "less common". "Additional spelling" says only that 態 is a further kanji form of entries headed by another kanji.
- The Metadata line (`態.md:71`) already listed 1409160, 1410750 and 2138450.

To verify: that lines 62-64 are accurate against the three entries.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | **changed** | `障.md:14`, `障.md:61-63` | `quiz_exclusions: [害, 防, 関]` (it read `[害, 防]`). The overlap bullet gains `The barrier sense also overlaps [関](関.md), whose title includes "barrier."`. The barrier and partition text at lines 28-30 is unchanged. `関.md` is unchanged: title `involve; barrier`, `distractors: [開, 間, 問]`; it does not list 障. |
| O2(a) | **changed** | `展.md:14`, `展.md:66-67` | 敷 is added at the end of `quiz_exclusions`, and a new bullet reads `- Spreading something out flat also overlaps [敷](敷.md), spread/lay out. That direct meaning comparison is excluded too.` Line 23, `展 concerns spreading out, unfolding or developing something.`, is unchanged. `敷.md` is unchanged: title `spread; lay out`, `quiz_exclusions: [布, 普, 散, 床]`, `distractors: [放, 敬, 敗]`. |
| O2(b) | **changed** | `妙.md:14`, `妙.md:67-69` | 技 and 腕 are added at the end of `quiz_exclusions`, and a new bullet reads `- JMdict also gives the word 妙 みょう a skill or cleverness sense, which overlaps [技](技.md), skill/technique, and [腕](腕.md), arm/skill. These direct comparisons are excluded from meaning choices too.` The sense is sense 3 of JMdict 1528490, "cleverness; adroitness; knack; skill" (`evidence\jmdict-cited-entries.xml`). The title `strange; exquisite` is unchanged; lines 23-25 already teach the skillful side (`wonderfully skillful and fine`, `a clever touch`). `技.md` (`skill; technique`) and `腕.md` (`arm; skill`) are unchanged. |
| O3 | **declined** | `態.md` | Your report calls it an optional enrichment, not a defect for N1 scope. The card's linked words are 事態, 態度 and 状態, and the repository has no word article for 受動態 or 能動態 (in the original packet's `repo\words\`, no other article name contains 態), so a voice example would be an unlinked compound with no article to support it. |

## Limits

### L1: custom and caller-built pools, multi-borrow Starter, Kotlin draws (your second Limits bullet)

Your bullet says the Python reading audit models only the N1 and All pools and Starter with one borrowed target, and lists
what is not verified. The revision adds meaning-quiz exclusions, so the part of the bullet that bears on them is the
actual Kotlin draws and the fallback in level and custom pools. The packet now carries the app's meaning-quiz source,
`evidence\QuizBuilder.kt`, taken from the Android checkout at commit `10d98d0`, which contains `2edbf36` ("Honor explicit
kanji meaning pair exclusions"). In it, `excluded(a, b)` (line 26) is true if either card lists the other, and `tryAdd`
(lines 28-32) returns without choosing a candidate excluded against the target or against any option already chosen
(line 30). The curated `distractors` are looked up in `all`, the pool passed in, so a curated card missing from the pool is
skipped (line 34); the fallback candidates are the other cards of the same pool, shuffled and then ordered by shared tags
(lines 35-36). Both go through `tryAdd`. The field's documented contract (original packet, `repo\docs\content-format.md`,
lines 102-107) says the same for All, level and custom pools, and that a small pool may yield fewer choices. The file does
not show how the app builds `all` for a given pool, so the author makes no claim about which cards any pool holds.

The reading side of your bullet is unchanged by this revision: no reading, reading selection, distractor or title changed,
and `quiz_exclusions` do not affect reading prompts (`content-format.md` line 107). `checks\reading-exposure.txt` is the
same as for the reviewed snapshot, with the same limits: the app's reading-quiz sources are not supplied in either packet,
and multi-borrow Starter, custom pools for reading prompts, native execution and phone acceptance remain unverified. The
Android JVM tests were not run for this revision either (see `CHANGES.md`). For the older APK, see the F1 disclosure.

To verify and answer: whether reading `QuizBuilder.kt` settles the meaning-quiz part of the bullet for the new pairs, what
still cannot be shown, and a disposition for L1 itself: `RESOLVED` (nothing remains open), or a statement of what remains.

### Other limits in your report

Your first Limits bullet (the check outputs are mechanical evidence), the third (the 5c000bd APK predates
`quiz_exclusions`; see the F1 disclosure) and the fourth (F1 and F2 are judgments, not runtime-reproduced failures), and
the reads and temporary file disclosed in your Scope section: no action is claimed and no disposition is needed. One fact
for this round: public web sources are allowed (`INSTRUCTIONS.md`), so you can open the Digital Daijisen pages you did not
fetch.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and why.

- `就.md:14` and `:79-82`: 了, 完 and 済 were added to 就's `quiz_exclusions`, and a new bullet reads `- The completion side
  shown by 成就 also overlaps [了](了.md), completion/settling, [完](完.md), complete, and [済](済.md), settle/finish. They
  are excluded from meaning choices as well; this does not make 就 a substitute for those characters in their own words.`
  The card already teaches that completion side at lines 29-31 (`成就 じょうじゅ, fulfillment or successful completion`;
  JMdict 1375720 "fulfillment; fulfilment; realization; realisation; completion") and in the ジュ row (line 43). 了
  `completion; settling`, 完 `complete` and 済 `settle; finish` are unchanged, and none lists 就.
- `微.md:14`, `:65-67` and `:80`: 軽 was added to 微's `quiz_exclusions`, and a new bullet reads `- A slight degree also
  overlaps [軽](軽.md), lightweight/slight; both characters appear in 軽微 けいび, slight or insignificant. That direct
  comparison is excluded too, without claiming that 微 means light in weight.` 軽微 けいび is JMdict 1615650, glossed
  "slight; little; insignificant" (`evidence\jmdict-cited-entries.xml`), now added to the Metadata line (line 80). 軽's
  title is `lightweight; slight`; `軽.md` is unchanged.
- `診.md:14` and `:58-59`: 査 (`investigate; inspect`) was added to 診's `quiz_exclusions` and to the bullet that names
  cards with examination or investigation meanings. The medical-specific text at lines 23-27, 43-44 and 61 is unchanged.
  `査.md` is unchanged.
- `盤.md:14` and `:63-65`: 乗 was added to 盤's `quiz_exclusions`, and a new bullet reads `- English "board" here is a flat
  object, not boarding a vehicle as in [乗](乗.md), ride/board. The shared English spelling is excluded from meaning
  choices; it is not a shared Japanese meaning.` The titles `board; disc` and `ride; board` share the English word in two
  different senses. `乗.md` is unchanged.
