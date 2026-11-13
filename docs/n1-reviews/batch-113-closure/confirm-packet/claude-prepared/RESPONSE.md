# Author's statement for the reviewer of `reports-113\initial-claude-m5.md`

This statement answers only the points in YOUR initial report. F1, O1 to O12 and L1 to L8 are your report's own labels.
The statement is the author's claim about what changed and why. Verify each claim against the revised card text in
`snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not rely on this text as evidence. Line numbers refer
to the revised cards in this packet unless marked otherwise. 13 of the 15 cards changed (慢 縫 飢 恩 盆 誕 系 徹 討 謝 握
寧 援); 隊 and 需 did not (see `CHANGES.md`). The revision declares 36 new `quiz_exclusions` pairs, each once, on the
batch card's side (a pair written 討–話 means that 討 lists 話). 14 of them answer a point in your report (card, then
counterparts: 討 話 争 評 思; 寧 和 尊 拝; 系 種 般; 誕 造 始; 盆 盤; 縫 結; 援 守) and 22 were added by the author (listed
at the end). Give a disposition for each of F1, O1 to O11 and L1; O12 and L2 to L8 need none, but see the notes below.

## Findings

### F1 (minor): 討 consistency / quiz safety

Author action: **changed, as proposed and slightly further.** 討's `quiz_exclusions` (line 14) now also lists 話 and 争,
the two pairs your report names, and 評 and 思 (see O4). The discussion bullet (lines 76-86) states the overlap in its
new sentences, quoted in `CHANGES.md`: 争う can mean to argue or compete, so 争 'contend; dispute' overlaps debate and
contention; discussion is also talking, and considering a proposal involves thinking it over and appraising it, so 討
overlaps 話 'talk, speak', 思 'think, feel' and 評 'appraise; reputation'; and 討 does not mean reputation. 争 is also
added to the list of discussion kanji in that bullet, before 考. 争う is JMdict 1400620 (sense 1 'compete; contest;
contend'; sense 2 'quarrel; argue; dispute; be at variance; oppose').

The original packet's frozen `snapshot\kanji\討.md` has the exclusion list on line 14 and the discussion bullet on lines
76-80 (your report cites 15 and 68-71); the revised file has the list on line 14 and the bullet on lines 76-86.

Checks (they cover all 36 new pairs, not only 討's four): `checks\quiz-safety.txt` is the same as in the original
packet, so 計, 村 and 寺 still fill all three options for 討 in the full pool, and the new pairs act only on fallback
candidates and, being symmetric, on the counterparts' own questions. One declaration guards both directions:
`excluded(a, b)` in `evidence\QuizBuilder.kt` (line 26) is true if either card lists the other, and `tryAdd` (lines
28-32) refuses such a candidate, curated or fallback (lines 34-36). Author's script over all 1,206 kanji cards at the
revised snapshot: no counterpart lists its batch card in `quiz_exclusions` or `distractors`; no batch card lists a
counterpart in `distractors`; no card lists both members of a new pair in `distractors`; every counterpart still has
three `distractors`; no exclusion was added between two counterparts.

To verify: that `tryAdd` refuses 話 and 争 for a 討 question and 討 for theirs; that the new sentences are accurate
(`evidence\jmdict-cited-entries.xml`, JMdict 1400620); and that the four new 討 pairs add no exclusion between two
counterparts.

## Optional

### O1: 寧 with 和, 尊 and 拝

Author action: **changed.** 寧's `quiz_exclusions` (line 14) now lists 和, 尊 and 拝, and also 御, 様 and 念, which your
report did not request (see the end). 敬 and 礼 stay excluded. Revised text: lines 67-68 end the peace bullet (from line
64) with "[和], 'harmony; Japanese style,' also has a peace sense, as in 平和; the comparison is with peace, not Japanese
style" (平和 is JMdict 1508070, 'peace; harmony'). Lines 73-78 are a new bullet on respectful wording that names 御, 様,
尊 and 拝; for the last two it reads "[尊], 'revere;
esteem,' concerns respect, and [拝], 'worship; bow in respect,' also appears in humble expressions such as 拝見" (拝見 is
JMdict 1472270). It ends "These comparisons concern respect and courtesy, not governing, every manner, or religious
worship."

To verify: that the three pairs are in line 14 and that the new text is accurate for 平和 and 拝見
(`evidence\jmdict-cited-entries.xml`).

### O2: shared-word and dated-sense exclusions applied unevenly

Author action: **declined; no pair was pruned, and none was added to equalise these cases.** Nothing was removed from any
`quiz_exclusions` list in this revision; each list only gained entries. The policy is stated once here, as your report
suggests. Note that line 94 of the original packet's `repo\docs\content-format.md` is only the `### Quiz authoring`
heading; the wording your report refers to is at lines 109-110.

(a) The meaning quiz shows only English titles. The author declares a pair, once and on the batch card's side, when a
counterpart's displayed title could be a defensible answer for the card's displayed title, or for a sense that the
card's Notes state from a cited source (KANJIDIC2 glosses, JMdict senses of named words, the Joyo table, Digital
Daijisen).

(b) Pairs that rest on a shared English word or on a dated or non-displayed sense (誕–寝, 隊–秒, 援–根, 援–貯, 徹–家,
徹–帰, 系–校, 系–級, 系–封, 寧–封, 寧–親, 謝–失, 謝–損, 謝–敗, 謝–負) are deliberately over-cautious. Each only removes
fallback candidates, in both directions; all 15 batch cards keep three curated distractors in the full pool
(`checks\quiz-safety.txt`), so no shown option is lost. Each is explained in the card's Notes, which name the shared
word or sense: `誕.md:71-74`, `徹.md:90-95`, `謝.md:84-88`, `隊.md:75-80`, `援.md:66-79`, `系.md:84-88` and `92-95`,
`寧.md:79-85`. Two unchanged published cards in the original packet's `repo\kanji\` use the same convention: `括.md:45`
(包 and 囲 share 'enclose' with the card's title) and `障.md:60-63` (関's title includes 'barrier'). That is precedent
for the convention, not evidence that the convention is right.

(c) Coverage is not exhaustive. The original packet's `content-format.md` (lines 109-110) says the mechanism is "not
automatic synonym discovery or a guarantee for uncurated pairs", so an undeclared pair is not asserted to be safe or
unsafe. The author did not extend association-only pairs, for example 糸 for 縫 (see O10); the earlier 縫–針 pair stays
as authored.

(d) The author agrees that the application is uneven. 当 and 射 (against the 'strike home' sense, `徹.md:90-95`)
qualify under (a) as much as the already excluded 打 and 撃, and were not found during authoring. 夕 (against 晩) and 困
(against the dated 'be at a loss' of 謝る, `謝.md:84-88`, where 失, 損, 敗 and 負 are already excluded) are not declared
either. 済 against 了 is closed, because this revision adds 徹–済 for another reason (see the end). These are known
gaps, not safe pairs.

To answer: `DECLINE ACCEPTED`, or `DECLINE REJECTED` if you judge the uneven coverage an actionable defect; in that case
name the pairs you consider necessary, added or pruned. If the decline is accepted, the author will record this policy in
`docs\n1-authoring-notes.md` at closure (a docs-only ledger outside the reviewed snapshot; it changes no card).

### O3: 系 with 種 and 般

Author action: **changed.** 種 and 般 are now in 系's `quiz_exclusions` (line 14). Lines 74-77 continue the group bullet
(from line 70) after "This card declares the pair 系–隊.": "The colloquial '-type; -ish' sense also overlaps [種], 'seed;
kind,' and [般], 'general; kind; category,' through 'kind' and 'category,' not through seeds or generality." The sense
is JMdict 1251000 sense 5 ('-type; -ish', tagged colloquial). 類 stays excluded, so your report's alternative of
dropping 系–類 was not taken. The author also added 列 (lines 81-83; see the end).

To verify: that the pairs are in line 14 and that the new sentence and the JMdict sense are accurate
(`evidence\jmdict-cited-entries.xml`).

### O4: 討 with 評, 想, 察 and 思

Author action: **changed in part.** 評 and 思 are now in 討's `quiz_exclusions` (line 14) and named in the discussion
bullet (lines 76-86; see F1). 想 and 察 were declined. The author judged that the displayed titles 'thought; conception'
and 'observe; infer' do not name a sense that 討's Notes state from a cited source (KANJIDIC2 glosses, JMdict 検討,
討議 and 討論), and your report rates both below F1. That is a judgment call, not a claim of safety: 想 is the nearer of
the two to the 'thinking it over' wording that supports 思, and the line between 思 and 想 is thin. Both stay
fallback-only, like other undeclared pairs.

To answer: a disposition for the changed part (評, 思) and for the declined part (想, 察).

### O5: 誕 with 造 and 始

Author action: **changed.** 造, 始 and 緒 are now in 誕's `quiz_exclusions` (line 14); lines 68-70 continue the bullet
that begins at line 64: "Making and beginning also overlap [造], 'make; construct,' [始], 'begin, start,' and [緒],
'cord; beginning,' though 誕 never means building something or a cord." 造 and 始 are your report's pairs; 緒 was added by
the author (see the end). Basis: JMdict 1419080 誕生, sense 2 ('creation; formation; birth; origin; making').

To verify: that the pairs are in line 14 and that the new sentence is accurate.

### O6: 盆 with 盤

Author action: **changed.** 盤 is now in 盆's `quiz_exclusions` (line 14), together with 缶 (see the end). The vessel
bullet (from line 65) now continues "[盤], 'board; disc,' also has a documented vessel sense, which overlaps 盆's
shallow vessel or tray; this does not make every board or disc a tray." The vessel sense rests on 盤's own card in the
original packet (`repo\kanji\盤.md`, lines 28-30: "The character dictionary also records vessel, flat-rock, game-stage
and coiling senses. Learn the particular word rather than translating every occurrence as a disc."). The original
packet's `evidence\kanjidic2-records.xml` has no 盤 record, so the author asserts no KANJIDIC2 gloss for 盤.

To verify: that the pair is in line 14 and that the new sentence is accurate against 盤.md lines 28-30 and claims no more.

### O7: 需 with 願

Author action: **declined; no change.** 需 is unchanged in this revision. Its `quiz_exclusions` `[要, 求, 頼, 欲]` rest
on the need-and-necessity bullet (`需.md` from line 62: "Need and necessity overlap [要], 'necessity; essentials,' and
the wanting in 需要 overlaps [欲], 'desire.'") and on the asking bullet that follows it ("Asking for something overlaps
[求], 'seek; request,' and [頼], 'request; rely.'"). 願 'wish; petition' would be an optional parity extension: it is
fallback-only for 需, and the author does not claim the pair is safe. The author does not claim 願 is covered through 欲:
exclusions are pairwise and not transitive (original `content-format.md`, lines 102-107). `願.md` line 45 in the
original packet compares 頼, not 需 (your report cites line 47).

To answer: `DECLINE ACCEPTED`, or `DECLINE REJECTED` if you judge the pair necessary.

### O8: 隊 with 派

Author action: **declined; no change.** 隊 is unchanged in this revision. Its 党 pair rests on a sense the card states
(`隊.md:67-71`: "A group or party overlaps [団], 'group; association,' [組], 'group; assemble,' [党], 'political party;
faction,' ..."). 派 'faction; school of thought' does not name a sense that the card states, so the author left it
undeclared. That is a judgment, not a claim that the pair is safe; it stays fallback-only.

To answer: `DECLINE ACCEPTED`, or `DECLINE REJECTED` if you judge the pair necessary.

### O9: 援 with the curated distractor 授

Author action: **declined; no change.** 授 'grant; impart; teach' is a curated look-alike distractor (`援.md:13`:
`[暖, 授, 担]`), and the components bullet (`援.md:63-65`) says "Their meanings differ from 援's." Its title is verbal,
while 援's is a noun ('aid; assistance'). This revision changed no `distractors`, titles or readings, and the author did
not change a distractor for a hypothesis that your report itself rates probably harmless. The author does not claim the
doubt is impossible: a learner who reads 'grant' as a grant of aid sees an arguable option.

To answer: `DECLINE ACCEPTED`, or `DECLINE REJECTED` if you judge a replacement distractor necessary (that would be a
new change).

### O10: 縫 with 糸

Author action: **declined; no change.** 糸 names a material, not a sense of 'sew; stitch' that the card states: the Notes
at `縫.md:61-63` say only that 縮, 練 and 緒 share the left-hand 糸 component and differ in meaning. The existing 針
pair (`縫.md:64-66`: "A needle is the sewing tool, not the act") stays as authored; it was in the reviewed snapshot.
This is parity only, since the curated 縮, 練 and 緒 fill the options in the full pool, and the pair is not claimed safe.

To answer: `DECLINE ACCEPTED`, or `DECLINE REJECTED` if you judge the pair necessary.

### O11: 恩 with 援

Author action: **declined; no change.** 'favor; debt of gratitude' against 'aid; assistance' is a low-probability pair.
Neither card is the other's curated distractor, so it is fallback-only; it is not asserted to be safe. Neither card's
Notes links to the other (checked by searching `恩.md` and `援.md` for links to each other).

To answer: `DECLINE ACCEPTED`, or `DECLINE REJECTED` if you judge the pair necessary.

### O12: pre-existing lint noise on five word articles

No action and no disposition requested. `checks\lint.txt` shows the same ten warnings as the original packet's copy,
and no word article changed in this revision.

## Limits

### L1: execution and pool limits

The revision adds 36 meaning-quiz exclusion pairs and changes no reading, reading selection, distractor or title. The
packet now carries the app's meaning-quiz source, `evidence\QuizBuilder.kt` (Android checkout at commit `10d98d0`), so
the static mechanics of the new pairs can be read directly: `excluded(a, b)` (line 26) is symmetric, and `tryAdd` (lines
28-32) refuses a candidate excluded against the target or against any option already chosen, for curated and fallback
candidates alike (lines 34-36). The file does not show how the app builds `all` for a given pool, so no claim is made
about which cards any custom or caller-built pool holds. Where the fallback of a padded Starter session uses `tryAdd`,
as your report infers, the same refusal applies there to 話 and 争 for a 討 question; that is read from the source, not
executed. Reading side: `checks\reading-exposure.txt` is the same as the original packet's copy, and the new
`checks\reading-options.txt` (revised snapshot) and `checks\reading-options-freeze.txt` (reviewed snapshot) are
byte-identical. Both report one problem, unchanged by this revision: the 援 `おん` scenario in your L2. No Kotlin, JVM,
native, phone or emulator execution occurred for this revision either. `quiz_exclusions` are not enforced by older APKs
(original `content-format.md`, lines 109-112), including `5c000bd`, so the 36 new pairs do not protect that build; no
claim is made about any installed build.

To answer: whether `QuizBuilder.kt` settles the static meaning-quiz part of L1 for the new pairs, what still cannot be
shown, and a disposition for L1: `RESOLVED` (nothing remains open), or a statement of what remains.

### L2: 援 `おん` (no disposition requested)

No change and no action. `checks\reading-options.txt` and `checks\reading-options-freeze.txt` both show the offer at
line 251 (the エン prompt, with 恩 温 遠 音 飲). The helper labels every extra reading "(card text)" whatever its origin;
this `おん` comes from a saved Wiktionary snippet that the card does not state (original `REVIEW.md`, lines 76-86).

### L3: unfetched Daijisen and Weblio claims (no disposition requested)

On 2026-11-13, at snapshot `b750f350`, the author fetched three of these pages directly. These are author checks, not
independent evidence.

| Card | Claim checked | Source page | Author's result |
| --- | --- | --- | --- |
| 需 | もとめる as a reading of 需 in Digital Daijisen | https://www.weblio.jp/content/需 | Entry じゅ【需】 lists もとめる and defines needing and demand. |
| 徹 | とおる and とおす as readings of 徹 in Digital Daijisen | https://www.weblio.jp/content/徹 | In the Digital Daijisen section, entry てつ【徹】 lists とおる and とおす; the check does not rely on the separate practical-expression dictionary that precedes it on the page. |
| 討 | たずねる as a reading of 討, and thorough investigation as its second sense | https://www.weblio.jp/content/討 | Entry とう【討】 lists うつ and たずねる, and thorough investigation is its second sense. |

A live read does not authenticate the original frozen retrieval, establish how common a reading is, or prove membership
in the Joyo table. No teaching text or quiz selection changed because of these checks. Not checked by the author: the
慢 我慢 filing (`慢.md:28-31`), 寧 ニョウ, 援 たすける and ひく with the 捐 and 掩 note, 飢 饑 interchangeability, 水飢饉,
and the めぐみ, いつくしみ and 情け glosses on 恩. The new 恩–愛 bullet relies on the card's existing wording about
いつくしみ (`恩.md:29-30`) and adds no new Daijisen claim; JMdict 1315270 慈しみ is context for it, not the source of
恩's sense. You may use the optional fetches your instructions allow on any of these.

### L4 and L5: SVG appendix, Joyo PDF, and `content-format.md` beyond line 139 (no disposition requested)

By design of the review; no action.

### L6: unread collision candidates (no disposition requested)

A note, not a disposition. 結 and 守 are now declared (縫–結 and 援–守). 支 and 協 were already excluded for 援 before
this revision (`援.md:14`). Not added, and not claimed safe: 局, 賛, 関, 続, 食, 眠, 担, 宅, 頼 and 流. The card itself
states that eating and food are not meanings of 飢 (`飢.md:69-70`); 担 is one of 援's curated distractors (`援.md:13`).

### L7 and L8 (no disposition requested)

Informational; no action.

## Changes that do not answer a point in your report

They are listed in `CHANGES.md`; please review them like any other changed hunk. Each states what the author claims and
why. The 22 author-added pairs, one row per card:

| Card | Pairs | Revised lines | Author's reason and source |
| --- | --- | --- | --- |
| 慢 | 軽 | 14, 68-71 | 軽んじる (JMdict 1252570: 'to look down on; to make light of') names looking down on others, which is the card's conceit sense; 軽's title also has 'slight', which can name a snub. The text says arrogance is not low physical weight. |
| 縫 | 接, 修 | 14, 67-70 | 縫合 (JMdict 1517710: 'sewing together; stitching up (a wound); suture') is joining, so 接 'touch; join' overlaps; 修繕 (JMdict 1332170: 'repair; mending') overlaps 修 'repair; amend; cultivate'. The text says tying a knot or repairing a machine is not sewing. (縫–結 answers your L6.) |
| 恩 | 愛 | 14, 67-69 | The card's existing wording about いつくしみ (`恩.md:29-30`, Daijisen: "めぐみ (grace; blessing), いつくしみ (affection; benevolence) and 情け (compassion)"; not re-verified in this revision, see L3) and `愛.md` (lines 20 and 36-37: 愛 names love, affection or care, not only romance). JMdict 1315270 慈しみ ('affection; love; fondness; tenderness') is context only. The text says 恩 is still a kindness received, not love in general. |
| 盆 | 缶 | 14, 69-70 | 缶's title 'tin can; container' shares 'container' with the card's own 'shallow vessel' wording; the text says 盆 is never a can. (盤 answers your O6.) |
| 誕 | 緒 | 14, 68-70 | 緒's title 'cord; beginning' names a beginning, near-synonymous with the 'origin' sense of 誕生 (JMdict 1419080 sense 2); declared in the same bullet as 始 (O5). The text says 誕 never means a cord. |
| 系 | 列 | 14, 81-83 | 系列 (JMdict 1251080 sense 1: 'series; sequence; system; succession'); 列 'row; queue' names an ordered line. The text says this does not make every queue a lineage or system. (種 and 般 answer O3.) |
| 徹 | 終, 済, 卒, 専, 到 | 14, 73-77 (終 済 卒 専), 81-82 (到) | 貫徹 (JMdict 1215090 sense 1: 'accomplishment; realization; attainment; fulfillment; achievement') is carrying something through to the end, so 終 'end; finish', 済 'settle; finish' and 卒 'graduate; finish' overlap through 'finish'; 徹する (JMdict 1598340 sense 2: 'to devote oneself (to); to do intently and exclusively') overlaps 専 'specialize; exclusive'; 到 'arrive; attain' joins the reaching labels 届 and 達. The 済 pair also closes the 済–了 parity case in your O2. |
| 謝 | 変, 給 | 14, 82-83 (変), 78-79 (給) | 代謝 (JMdict 1411920 sense 2: 'renewal; regeneration; replacing the old with the new') and 新陳代謝: replacing the old with the new is a change, so 変 'change; strange' overlaps; 謝礼 (JMdict 1323070: 'reward; honorarium; remuneration') and 月謝 (JMdict 1255690: 'monthly tuition fee') make paying a fee overlap 給 'pay; bestow'. The dated 謝る senses (lines 84-88) are unchanged. |
| 握 | 扱, 管, 知, 識 | 14, 74-77 (扱), 80-81 (管), 82-84 (知 識) | 握り (JMdict 1152660 sense 3: 'handle; grip; knob') shares the English word 'handle' with 扱 'handle; deal with', whose verb 扱う is JMdict 1153440; 握る sense 3 (JMdict 1152720: 'seize (power); hold (the reins); dominate; control') overlaps 管 'pipe; supervise' through control and supervision; 把握 (JMdict 1470910: 'grasp (of the situation, meaning, etc.); understanding; control; hold; grip') and 握る sense 2 ('hold (the answer); have (e.g. the solution)') overlap 知 'know' and 識 'knowledge; awareness'. The text says 握 is still a grip, not knowledge in general. |
| 寧 | 御, 様, 念 | 14, 73-78 (御 様), 83-84 (念) | 御 'honorific; govern' and 様 'manner; honorific suffix' belong to respectful wording (御 can add a polite prefix and 様 a respectful suffix) and are declared together; 念 'thought; attention' overlaps the careful-attention sense of 丁寧 (JMdict 1427360 sense 2: 'careful; close; thorough; conscientious'). The text says these comparisons are not about governing, every manner, or worship. |
| 援 | 防 | 14, 70-72 | KANJIDIC2 glosses 援 'help' and 'save', and 救援 (JMdict 1229070) is relief or rescue, so 防 'defend; ward off' overlaps through protection and rescue, like 保 and 守. The text says not every act of aid is defense. (守 answers your L6.) |

Two text edits on 飢 (no `quiz_exclusions` change; its front matter is unchanged):

1. Opening, `飢.md:23-25`. Old: `飢 concerns hunger severe enough to amount to starvation.` New: `飢 concerns hunger from a lack of
   food, ranging from being hungry to starving; its words usually describe serious deprivation, and for everyday hunger
   お腹が空く おなかがすく is the usual expression.` Reason: the old sentence set a starvation threshold that is
   narrower than the card's own title ('starve; be hungry'), than JMdict 1224080 sense 1 ('starve; be famished; be
   hungry') and than KANJIDIC2's 'hungry' and 'starve'; JMdict 2021520 お腹が空く is 'get hungry; become hungry'.
2. Conjugation, `飢.md:49-51`. Old: `... it is an intransitive ichidan verb, so える stays in forms such as 飢えて and
   飢えない.` New: `... it is an intransitive ichidan verb, so the final る changes while the stem うえ- stays: うえる
   becomes うえて, 飢えて, and うえない, 飢えない.` Reason: the old wording said える stays, but the final る is replaced in
   these forms (JMdict 1224080: ichidan, intransitive; readings うえる and かつえる).
