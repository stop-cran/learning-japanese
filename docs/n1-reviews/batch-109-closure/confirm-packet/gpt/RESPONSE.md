# Author's statement for the reviewer of `reports-109-gpt\initial-gpt.md`

This statement answers only the points in YOUR initial report. Your report numbers its findings 1 and 2; the author's
labels are: Finding 1 = **#1**; Finding 2 = **#2**, whose eight table rows are **#2a-#2h** in the order of your table; the
three bullets under Optional = **OA, OB, OC** in order; the first and second bullets under Limits = **L1** (撃/敗) and
**L2** (攻/批); the remaining Limits bullets = **L3**. The statement is the author's claim about what changed and why.
Verify each claim against the revised card text in `snapshot\kanji\`, `diffs\fix.patch` and independent sources; do not
rely on this text as evidence. Line numbers refer to the revised cards in this packet. All 15 cards are in
`snapshot\kanji\` (批 and 択 are unchanged). Give a disposition for each of #1, #2a-#2h, OA-OC, L1 and L2; L3 needs none.

## Findings

### #1 (major, quiz safety): 影 curated option 形 is a valid meaning of 影

Author action: **changed.**

- `影.md:13`: `distractors: [景, 英, 京]`. 形 is replaced by 英, "English; outstanding": an エイ sound-alike whose title
  has nothing to do with shadows, images or light.
- `影.md:14`: `quiz_exclusions: [映, 形, 像, 象, 光, 跡]` (the direct 影/形 exclusion you asked for, plus #2e).
- `影.md:45-46`: the 形 bullet now says JMdict's first sense of かげ includes "figure; shape", and a new bullet explains 英.
- The default options now shown for 影 are on the 影 line of `checks\quiz-safety.txt`.

### #2 (major, quiz safety): missing direct `quiz_exclusions` pairs

Author action: **changed, every pair in your table.** Each pair is listed on ONE card only (the repository convention;
`evidence\QuizBuilder.kt` treats an exclusion as symmetric). No group was made a clique. The validator rule that an
exclusion may not also be a distractor of the same card passes.

| ID | Pair | Where the exclusion is listed | New explanatory bullet |
| --- | --- | --- | --- |
| #2a | 催/促 | `催.md:14` `[促]` | `催.md:44` (the bullet cites the Daijisen first sense うながす of 催) |
| #2b | 促/責 | `促.md:14` `[勧, 励, 責]` | `促.md:45`; links `../words/責める.md`; Metadata adds JMdict 1383160 (`促.md:47`) |
| #2c | 括/包, 括/囲 | `括.md:14` `[結, 束, 包, 囲]` | `括.md:45` |
| #2d | 抵/反, 抵/対 | `抵.md:14` `[抗, 反, 対]` | `抵.md:42` |
| #2e | 影/像, 影/象, 影/光, 影/跡 | `影.md:14` | `影.md:48` |
| #2f | 摩/研 | `摩.md:14` `[擦, 磨, 研]` | `摩.md:46` (cites JMdict 1592730 研磨 in `evidence\jmdict-cited-entries.xml`) |
| #2g | 攻/研 | `攻.md:14` `[戦, 研, 批]` | `攻.md:48` |
| #2h | 掲/刷 | `掲.md:14` `[刊, 示, 置, 刷]` | `掲.md:44` (cites JMdict 1250600 sense "to publish; to print; to carry") |

To verify: that each pair is justified by the cited evidence and not over-broad, and that no listed exclusion removes
the only plausible wrong answers so that the options degrade (see `checks\quiz-safety.txt`).

## Optional points

| ID | Author action | Where | Change |
| --- | --- | --- | --- |
| OA | **changed** | `抵.md:23`; `促.md:23`; `影.md:34` | 抵当 gloss shortened to "mortgage; security"; "geminate consonant" became "doubled consonant sound"; "Go-on" is now explained as "older Chinese-derived (Go-on) reading ヨウ". |
| OB | **changed** | `擦.md:23` | 擦過傷 is called "the formal term". |
| OC | **changed** | `掲.md:25` | "a variant of 曷 at the right, drawn as a wide 日-like box (曰) above 匂". KanjiVG records are in `evidence\kanjivg\` (`063b2.svg` 掲, `066f7.svg` 曷). |

## Limits

### L1: 撃/敗 (UNVERIFIED in your report)

Author action: **disputed as attributed; a defensive exclusion was added anyway.**

- In the reviewed snapshot, `撃.md:13` was `distractors: [投, 殺, 設]` (original packet, `snapshot\kanji\撃.md`), and the
  options shown for 撃 were "throw | kill | establish; provide" (original packet `mechanical-checks.md`, line 142).
- 敗, "failure; defeat", is a curated distractor of **攻** (`攻.md:13`: `distractors: [功, 放, 敗]`; options "merit;
  achievement | release | failure; defeat", `mechanical-checks.md`, line 139). The author therefore reads L1 as attributing
  攻's option to 撃. Nothing about 攻's distractors changed.
- Added anyway: `撃.md:14` `quiz_exclusions: [打, 攻, 敗]` and the bullet `撃.md:44`, because KANJIDIC2 lists "defeat"
  among the meanings of 撃 (see 撃退 and 撃破 in `evidence\jmdict-cited-entries.xml`). This guards the fallback pool only.

To verify and answer: (a) a disposition on L1 as stated (`DISPUTE ACCEPTED` or `DISPUTE REJECTED`); (b) your own judgment,
as a fresh check, of every post-fix option for 撃 (投, 殺, 設) and for 攻 (功, 放, 敗): is each one defensibly wrong?

### L2: 攻/批 (UNVERIFIED in your report)

Author action: **changed.** `攻.md:14` now lists 批 and `攻.md:49` explains it (KANJIDIC2 lists "criticize" among the
meanings of 攻; JMdict 1279170 sense 2 "criticism; censure"; the JMdict entry is in `evidence\jmdict-cited-entries.xml`).
批.md is unchanged. Please say whether this settles your UNVERIFIED consistency verdict for 批.

### L3: other limits in your report

Stroke arcs, sentence grammar, native-speaker and phone trials: no stroke file, example sentence or word article changed in
this revision, so no action is claimed and no disposition is needed.
