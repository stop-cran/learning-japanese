# Author's statement for the reviewer of `reports-113\initial-gpt.md`

This statement answers only the points in YOUR initial report. F1, F2, F3, O1 and L1 to L4 are your report's own labels.
The statement is the author's claim about what changed and why. Verify each claim against the revised card text in
`snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Line numbers refer to
the revised cards in this packet. 13 of the 15 cards changed (慢 縫 飢 恩 盆 誕 系 徹 討 謝 握 寧 援); 隊 and 需 did not (see
`CHANGES.md`). Give a disposition for each of F1, F2, F3, O1 and L1; L2, L3 and L4 need none, but see the notes below.

## Findings

### F1 (medium): missing direct meaning-label exclusions

Author action: **changed, as proposed: all 30 pairs are declared**, each once, on the batch card's side, each with a
Notes sentence that says which sense or English label overlaps and what is not claimed. Six further pairs were added by
the author; they are listed under "Changes that do not answer a point" below.

No counterpart card changed, and no exclusion was added between two counterparts, so no group or transitive chain was
formed. Author's script over all 1,206 cards at the revised snapshot: no counterpart lists its batch card in
`quiz_exclusions` or `distractors`; no batch card lists a counterpart in `distractors`; no card lists both members of a new
pair in `distractors`; every counterpart still has three `distractors`. The three wrong options shown for each of the 15
cards in the full pool are unchanged (`checks\quiz-safety.txt` is the same as in the original packet). One declaration
guards both directions: `excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other.

| Card | Pairs added (line 14) | Notes text (revised lines) |
| --- | --- | --- |
| 慢 | 軽 | 68-71: looking down on others; 軽んじる (JMdict 1252570); "slight" as a snub; "Arrogance is not low physical weight." |
| 縫 | 結 接 修 | 67-70: joining or mending cloth; 縫合 (1517710); 修繕 (1332170); "Tying a knot or repairing a machine is not sewing." |
| 恩 | 愛 | 67-69: the affection and benevolence in いつくしみ overlap 愛, "whose card covers affection and care, not only romance" (愛.md lines 20 and 36-37); "恩 is still a kindness received, not love in general." |
| 盆 | 缶 | 69-70: shares "container" with a shallow vessel, "although 盆 is never a can." |
| 誕 | 造 始 緒 | 68-70: making and beginning, continuing the bullet that quotes JMdict 1419080's "creation; formation; birth; origin; making"; "誕 never means building something or a cord." |
| 系 | 種 般 | 74-77: the colloquial "-type; -ish" sense, "through 'kind' and 'category,' not through seeds or generality." |
| 徹 | 終 済 卒 専 到 | 73-77: carrying through to the end (貫徹, 1215090) "through 'finish,' without making 徹 a word for graduating"; exclusive devotion (徹する, 1598340) for 専. 81-82: 到 joins the reaching bullet. The non-standard penetration sense of 貫徹 is not relied on. |
| 討 | 思 話 評 | 82-86: talking, thinking a proposal over and appraising it; "討 does not mean reputation." |
| 謝 | 変 給 | 78-79: paying an honorarium or a fee (謝礼 1323070, 月謝 1255690). 82-83: "replacing the old with the new is a change" (代謝, 新陳代謝). The dated senses of 謝る are not extended. |
| 握 | 扱 管 知 識 | 74-77: the English word "handle" (握り 1152660; 扱う 1153440), "it does not make those Japanese words interchangeable." 80-81: 管 joins the control bullet. 82-84: grasping a situation (把握 1470910) or holding the answer; "握 is still a grip, not knowledge in general." |
| 寧 | 御 和 念 | 67-68: 和's peace sense, as in 平和 (1508070), "not Japanese style." 73-78: 御 adds a polite prefix; "not governing." 83-84: careful attention overlaps 念. |
| 援 | 守 防 | 70-72: protection and rescue, "not every act of aid is defense." |

On 恩/愛, your F1 offered two remedies: verify the Daijisen affection attribution and exclude the pair, or correct that
wording. The author took the exclusion and kept the existing affection wording; the Daijisen attribution itself was not
re-verified in this revision (it remains under your L2). JMdict 1315270 慈しみ いつくしみ ("affection; love; fondness;
tenderness") is supplied in `evidence\jmdict-cited-entries.xml` as context for the Japanese word the new bullet
names; it is not offered as the source of 恩's sense.

To verify: that each of the 30 pairs is declared, that each new Notes sentence is accurate and does not overclaim, and
that no transitive group is implied.

### F2 (medium): the conjugation explanation says the wrong substring remains

Author action: **changed, as proposed.**

- `飢.md:49-51` now read: `う with 飢 and える in kana; it is an intransitive ichidan verb, so the final る changes while the
  stem うえ- stays: うえる becomes うえて, 飢えて, and うえない, 飢えない. JMdict also lists かつえる,`
- It read: `... it is an intransitive ichidan verb, so える stays in forms such as 飢えて and 飢えない.`
- JMdict 1224080 (`evidence\jmdict-cited-entries.xml`) marks 飢える as an ichidan, intransitive verb. The reused word article
  `words\飢える.md` is unchanged.

To verify: that the rule now agrees with its examples.

### F3 (medium): an absolute starvation threshold overnarrows 飢

Author action: **changed, as proposed.**

- `飢.md:23-25` now read: `飢 concerns hunger from a lack of food, ranging from being hungry to starving; its words usually
  describe serious deprivation, and for everyday hunger お腹が空く おなかがすく is the usual expression.`
- It read: `飢 concerns hunger severe enough to amount to starvation.`
- The breadth follows JMdict 1224080 sense 1 and KANJIDIC2's "hungry". お腹が空く おなかがすく is JMdict 2021520
  (`evidence\jmdict-cited-entries.xml`). Line 26 (`[飢える](../words/飢える.md) うえる means to starve or be famished, ...`)
  and the card's title `starve; be hungry` are unchanged.

To verify: that the opening keeps the hungry sense without suggesting 飢える for casual hunger, and that the お腹が空く
contrast is accurate.

## Optional

### O1 (low): sense-local wording in 盆's opening

Author action: **deferred, no change.** The editing scope available for this revision was limited to `quiz_exclusions`,
Notes and 飢's two sentences, so 盆's opening paragraph (lines 23-27) and its Common words section are unchanged. The
author accepts the point: JMdict 1002690 attaches the polite flag to the tray sense. It is recorded as a follow-up for a
later revision of 盆, not adopted here.

To answer: whether deferral is acceptable for this batch.

## Limits

### L1: execution and pool limits

The revision adds meaning-quiz exclusions and changes no reading, reading selection, distractor or title. The packet now
carries the app's meaning-quiz source, `evidence\QuizBuilder.kt` (Android checkout at commit `10d98d0`), so the static
mechanics of the new pairs can be read directly: `excluded(a, b)` (line 26) is symmetric, and `tryAdd` (lines 28-32)
refuses a candidate excluded against the target or against any option already chosen, for curated and fallback
candidates alike (lines 34-36). The file does not show how the app builds `all` for a given pool, so no claim is made about
which cards any custom or caller-built pool holds.

Reading side: `checks\reading-exposure.txt` is the same as the original packet's copy, and the new
`checks\reading-options.txt` (revised snapshot) and `checks\reading-options-freeze.txt` (reviewed snapshot) are
byte-identical. The one reported problem in both is the 援 `おん` scenario you already name. No Kotlin, JVM, native, phone
or emulator execution occurred for this revision either. `quiz_exclusions` are not enforced by older APKs
(`content-format.md` lines 109-112), including `5c000bd`, so the 30 remedies do not protect that build; no claim is made
about any installed build.

To answer: whether `QuizBuilder.kt` settles the static meaning-quiz part of L1 for the new pairs, what still cannot be
shown, and a disposition for L1: `RESOLVED` (nothing remains open), or a statement of what remains.

### L2, L3 and L4

No action is claimed, and no disposition is needed. Two notes:

- L2: the 恩 affection attribution stays unverified (see F1 above). No other sentence your L2 names changed.
- L3: none of the unread leads (願 絡 宅 浅 様 楽 休 払 退 権 優 択 選 贈 与 費 報 抜) was added as an exclusion for the card
  you associated it with. 様 was added to 寧 for a different reason (see below), not to 系.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and why.

- `盆.md:14` and `:67-69`: 盤 was added: `[盤](盤.md), "board; disc," also has a documented vessel sense, which overlaps 盆's
  shallow vessel or tray; this does not make every board or disc a tray.` 盤's own card records the vessel sense
  (`盤.md` line 28 in the original packet's `repo\kanji\`: `The character dictionary also records vessel, ...`), and
  KANJIDIC2 glosses 盤 "tray", "shallow bowl", "platter" and "tub". Your report treated 盆/盤 as harmless without a declaration; the
  author added it as a precaution against the shared tray reading of the two labels.
- `系.md:14` and `:81-83`: 列 `row; queue` was added to the relation/series bullet: `列 names an ordered line or row; 系
  concerns connected lines and series, as in 系列, without making every queue a lineage or system.` 系列 けいれつ is JMdict
  1251080 (sense 1: "series; sequence; system; succession").
- `討.md:14` and `:79-82`: 争 `contend; dispute` was added: `争う can mean to argue or compete, overlapping debate or
  contention; not every discussion is a dispute, and not every dispute is an armed attack.` 争う is JMdict 1400620 ("to
  compete; to contest; to contend", "to quarrel; to argue; to dispute; to be at variance; to oppose").
- `寧.md:14` and `:73-78`: 様 `manner; honorific suffix`, 尊 `revere; esteem` and 拝 `worship; bow in respect` were added
  in the bullet that also answers 寧/御: `様 a respectful suffix. [尊](尊.md), "revere; esteem," concerns respect, and
  [拝](拝.md), "worship; bow in respect," also appears in humble expressions such as 拝見. These comparisons concern respect
  and courtesy, not governing, every manner, or religious worship.` 拝見 はいけん is JMdict   1472270 (humble and polite
    language for "seeing; looking at"). The author's reason: once 御's honorific label is excluded for the courtesy sense, the other respect and
  honorific labels sit just as close to "polite".
