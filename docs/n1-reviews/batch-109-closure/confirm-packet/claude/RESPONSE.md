# Author's statement for the reviewer of `reports-109\initial-claude.md`

This statement answers only the points in YOUR initial report. IDs F1-F5 and O1-O10 are your report's own labels. L1 is a
question the author adds, based on the impact statement in your F2. The statement is the author's claim about what
changed and why. Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and
independent sources; do not rely on this text as evidence. Line numbers refer to the revised cards in this packet. All 15
cards are in `snapshot\kanji\` (批 and 択 are unchanged). Give a disposition for each of F1-F5, O1-O10 and L1.

## Findings

### F1 (major, quiz safety): 影 distractor 形 is a defensible meaning

Author action: **changed.**

- `影.md:13`: `distractors: [景, 英, 京]`. 形 is replaced by 英, "English; outstanding": an エイ sound-alike whose title
  has nothing to do with shadows, images or light.
- `影.md:14`: `quiz_exclusions: [映, 形, 像, 象, 光, 跡]`. Your suggested [映, 形] is extended by 像, 象, 光 and 跡, which
  the author matched to the secondary senses of かげ in JMdict 1590145 (see `evidence\jmdict-cited-entries.xml`).
- `影.md:45-46, 48`: the Notes explain why these cards are kept out of the quiz options.
- The default options now shown for 影 are on the 影 line of `checks\quiz-safety.txt`.

To verify: that the default options contain no defensible answer, that 英 is defensibly wrong, and that the new Notes
claims are true.

### F2 (minor, quiz safety): 括 shares "enclose" with 包 and 囲

Author action: **changed** (exclusions added; the title "tie together; enclose" is kept).

- `括.md:14`: `quiz_exclusions: [結, 束, 包, 囲]`.
- `括.md:45`: new Notes bullet that says why.

### F3 (minor): 摩 readings paragraph contradicts the rows

Author action: **changed.**

- `摩.md:36`: rewritten. マ is stated to be the only reading of 摩 in the Joyo table; the three kun readings are kept for
  recognition only; 摩する まする is described as マ plus the verb する, 摩る さする as usually kana, and 摩る す.る as a
  rarely used kanji form of 擦る する. The sentence "not a claim that those readings are invalid, obsolete or rare" is gone.
- `摩.md:50-51`: new `Usage evidence:` line linking Joyo PDF p. 144 (extract: `evidence\joyo\p144.txt`).
- `摩.md:46`: new 研 bullet (a separate change; see the regression check).

### F4 (minor): 擦 こす.る is unqualified

Author action: **changed.**

- `擦.md:23`: こする is "an everyday verb ... though it is usually written in kana"; 擦過傷 is "the formal term".
- `擦.md:35`: the こす.る row now ends "usually written in kana".
- `擦.md:38`: the readings paragraph states the Joyo-table readings (サツ, す.る, す.れる; not こす.る or こす.れる) and that
  こす.る is practised as the reading of the spoken verb こする.
- `擦.md:52-53`: new `Usage evidence:` line linking Joyo PDF p. 62 (extract: `evidence\joyo\p62.txt`).

### F5 (minor, medium confidence): 撮 and 掲 call the top element 日 where it is conventionally 曰

Author action: **changed (wording).**

- `撮.md:25`: "made of a wide 日-like box (曰) above 取".
- `掲.md:25`: "a variant of 曷 at the right, drawn as a wide 日-like box (曰) above 匂". The link to the 日 card is removed.
- KanjiVG records in `evidence\kanjivg\`: the standalone 最 (`06700.svg`) and standalone 曷 (`066f7.svg`) mark their top
  element as `日` with `kvg:original="曰"`. In the 撮 record (`064ae.svg`) the top of 最 is plain `日` with no `original`
  attribute. In the 掲 record (`063b2.svg`) the right-hand part is `曷` with `kvg:variant="true"`, then `日` above `匂`.

To verify: whether the revised wording is accurate and not misleading to a beginner.

## Optional points

| ID | Author action | Where | Reason |
| --- | --- | --- | --- |
| O1 | no change | n/a | You said no change is needed. |
| O2 (title) | **declined** | `抵.md:3` | The title "resist; collide" is kept. Digital Daijisen 抵 (original packet, `evidence\public-source\weblio-抵.txt`) lists 1 ぶつかって張り合う (抵抗) and 2 突き当たる (抵触); KANJIDIC2 lists "resist, reach, touch"; JMdict 抵触 includes "running afoul". |
| O2 (link) | **changed** | `抵.md:23` | 大抵 is linked to the existing `../words/たいてい.md`. |
| O3 (older) | **changed** | `弧.md:23` | "an older sense of 'bow'" became: Daijisen lists "bow" (ゆみ) as its first sense and the curved line as its second. |
| O3 (弱 framing) | **declined** | `弧.md:42` | The bullet claims only that 引, 弱 and 強 "also have 弓 at the left"; the KanjiVG records of these three characters (original packet context) support that claim. |
| O4 | **changed** | `抗.md:23` | 抗がん剤 こうがんざい (also written 抗癌剤). |
| O5 | **declined** | `促.md:13` | 速 is kept; you rated the risk low and the card explains urging versus speed. |
| O6 (集) | **declined** | `催.md:13` | 集 "gather" is kept as a distractor; you judged it defensibly wrong. |
| O6 (催/促) | **changed** | `催.md:14, 44` | New `quiz_exclusions: [促]` and an extended 促 bullet (Daijisen lists うながす as the first sense of 催). |
| O7 | **changed** | `攻.md:44`, `撃.md:42` | The wording of the shared-sense bullet was changed so it no longer says "hitting at a target". |
| O8 | **declined** | `催.md:32` | もよう.す is already marked source-only. |
| O9 | no change | n/a | Pre-existing, out of scope: 括弧 uk, and `words/撮る.md` has no Dictionary line. Recorded in the closure. |
| O10 | **changed** | `抵.md:14, 42` | `quiz_exclusions: [抗, 反, 対]` and a new 反/対 bullet. |

## Limits

### L1: does the app use fallback options when all three curated distractors are present? (author's question)

Your F2 impact statement relied on `content-format.md` lines 96-106 for how options are filled. `evidence\QuizBuilder.kt`
is the app's option builder. Please read it and say whether it changes your F2 impact analysis (the author kept the F2
change either way, as a direct-title-overlap exclusion), and give a disposition for L1 itself:
`RESOLVED` (nothing remains open), or a statement of what remains.
