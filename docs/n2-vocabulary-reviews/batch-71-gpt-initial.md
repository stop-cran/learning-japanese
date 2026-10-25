## Snapshot: 88aea28d8f5e1d4d17088835c03b9c93d19eb6cd; committed content only

Reviewed the supplied frozen committed snapshot, with reported parent `0e8e0b43c74d97a7367c5438012d09d495f34b18`. **Two actionable findings:** missing quiz exclusions for 捻る’s “devise” sense, and an inaccurate reading description in 日にち. No files were changed.

## Scope: gpt-6.1-sol; family gpt

Read `frozen-snapshot.json` first; both required instruction files; `docs\content-format.md:18–103`; the TSV header and exactly physical rows **1402–1421**; all twenty assigned articles completely; complete edited `kanji\筆.md` and `kanji\皮.md`; and the complete related patch.

Read all twenty blind mappings and twenty complete principal families, including raw fields, spelling/reading restrictions, flags, POS inheritance and selected/additional senses; all thirty component records; all 259 navigation metadata records; the three permitted repository snapshots; and the allowed JLPT/confusable-word documentation. Full comparison reads covered all eighteen family renderings plus the six-family supplement—the reported **473 families/1,115 senses**—and all twenty older-body renderings containing 155 articles. Also read the twelve specified supplementary older articles directly, additional actual comparisons including いつも, 工夫, 考える and まず, and complete `kanji\日.md`. Navigation labels were not counted as inspected bodies.

Read all 22 frozen public captures and their receipts, selecting the applicable lexical headings. These captures represent **Digital Daijisen through Weblio, one authority**, not 22 dictionaries. Additional applicable live evidence came from Digital Daijisen and *Seisenban Nihon Kokugo Daijiten* through Kotobank.

No agents, delegation, edits or prohibited ledgers/rationale-bearing batch source were used. The large `review-evidence.json` was not read completely; its compact records and complete bounded renderings supplied the substantive evidence instead.

## Verdicts:

All articles below are `words\<Article>.md`. **S** denotes selected one-based JMdict senses; **A** denotes additional recognition senses, not independent N2 assignments. CLEAN means no actionable defect established within this review’s actual scope.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1402 | 筆記 | CLEAN | CLEAN | CLEAN | 1487800: S1; A2–3. Writing down, resulting writings and abbreviated written-exam use distinguished. |
| N2:1403 | ひっくり返す | CLEAN | CLEAN | CLEAN | 1601870: S1–3. Transitive construction sound; raw 引っ繰り返す correctly recognized as rare. |
| N2:1404 | ひっくり返る | CLEAN | CLEAN | CLEAN | 1169320: S1–2. Intransitive construction sound; raw spelling’s status not borrowed from the transitive family. |
| N2:1405 | 引っ越し | CLEAN | CLEAN | CLEAN | 1601880: S1. Raw 引越し recognized as an ordinary alternative; existing 引っ越す identity/level preserved. |
| N2:1406 | 引っ込む | CLEAN | CLEAN | CLEAN | 1169390: S1; A2–3. Recession, setback positioning and indoor withdrawal appropriately scoped. |
| N2:1407 | 筆者 | CLEAN | CLEAN | CLEAN | 1487830: S1. Writer of the relevant text and self-reference explained without a professional-author requirement. |
| N2:1408 | 必需品 | CLEAN | CLEAN | CLEAN | 1487500: S1. Necessary articles depend on context; 需 remains in metadata despite its absent card. |
| N2:1409 | 人差し指 | CLEAN | CLEAN | CLEAN | 1601940: S1; A2. Raw 人差指’s search-only status and additional second-toe recognition kept separate. |
| N2:1410 | 一通り | CLEAN | CLEAN | CLEAN | 1164910: S1,3; A2,4. General pass, ordinary, whole range and one method distinguished by construction. |
| N2:1411 | 人通り | CLEAN | CLEAN | CLEAN | 1368820: S1. Pedestrian passage/flow does not falsely require crowding. |
| N2:1412 | ひとまず | CLEAN | CLEAN | CLEAN | 1601990: S1; A2. Blank raw spelling preserved; provisional action and additional unsatisfactory-result use distinguished. |
| N2:1413 | 瞳 | CLEAN | CLEAN | CLEAN | 1453900: S1; A2. Anatomical pupil and expressive “eyes” distinguished; primary 瞳 retained without an invented link. |
| N2:1414 | 一休み | CLEAN | CLEAN | CLEAN | 1161830: S1. Short pause and intransitive する use explained without invented timing. |
| N2:1415 | 独り言 | CLEAN | CLEAN | CLEAN | 1455670: S1. Self-directed speech and 独り言を言う taught; not equated with all whispering or public monologues. |
| N2:1416 | ひとりでに | CLEAN | CLEAN | CLEAN | 1455660: S1. Blank raw spelling preserved; spontaneity distinguished from deliberately acting alone. |
| N2:1417 | ビニール | CLEAN | CLEAN | CLEAN | 1105580: S1. Blank raw spelling preserved; record sense restricted to バイナル is not transferred to ビニール. |
| N2:1418 | 皮肉 | CLEAN | CLEAN | CLEAN | 1483900: S1; A2–4. Sarcasm, contrary outcome, superficiality and archaic body sense appropriately separated. |
| N2:1419 | 日にち | NEEDS FIX | CLEAN | CLEAN | 1611370: S1; A2. Date/day-count mapping sound; “native reading” description needs correction—F02. |
| N2:1420 | 捻る | CLEAN | NEEDS FIX | CLEAN | 1469530: S1; A2–7. Physical source teaching and whole 頭をひねる guidance sound; direct quiz guards missing—F01. |
| N2:1421 | 日の入り | CLEAN | CLEAN | CLEAN | 1463800: S1. Sunset event/time distinguished from the broader evening period. |

**Related kanji edits:** For both 筆 and 皮, correctness, scoped coverage and comprehensibility are **CLEAN**. The three additions are substantively reciprocal at actual whole-word readings: 筆/筆記 **ひっき**, 筆/筆者 **ひっしゃ**, and 皮/皮肉 **ひにく**. Dictionary footer IDs match **1487800**, **1487830** and **1483900**, respectively. The notes do not mistake component associations for established etymology.

**Baseline preservation:** **CLEAN within the supplied related patch:** existing kanji headers, readings, examples and prior content are retained; additions are additive. Primary written Han characters remain in word metadata, including characters without cards. Alternative spellings do not replace primary metadata, and missing cards are not fabricated. Repository-wide preservation against the parent is **UNVERIFIED independently**, because Git execution is unavailable.

**Mappings:** Each of the twenty source-to-canonical mappings is **CLEAN for correctness, scoped coverage and comprehensibility as a mapping record**. Raw fields—including the three blank spellings—are preserved; aliases remain associated with the correct readings/families. Selected teaching and additional recognition are distinguished. The 日にち mapping correctly represents pinned JMdict entry 1611370’s date/day-count senses; this establishes a database-family discrepancy, not the source compiler’s intent or a universal prohibition on other dictionary-attested uses.

## Findings:

**F01 — Moderate; scoped coverage; `words\捻る.md:4,9,22–26`. Missing direct quiz exclusions for 工夫 and 考える.**

The displayed title includes **“devise”**, but neither pair is excluded from either endpoint. 工夫’s actual title is “ingenuity; devising a method,” and its complete body explicitly teaches devising a method (`words\工夫.md:4,9,16–21`). 考える’s complete body includes working out an idea (`words\考える.md:4–9,15`), and its complete JMdict family 1281020 includes devising/contriving in sense 6. Thus 捻る’s full title can supply a defensible alternative answer for an ordinary devising use, despite the different primary labels.

**Minimal remedy:** Add **工夫** and **考える** to 捻る’s `quiz_exclusions`. A declaration on one endpoint is sufficient because guards are symmetric. 工夫’s existing exclusion of 考える does not protect either new pair: exclusions are nontransitive.

**Exact corroboration:** [Seisenban, ひねる [1]③](https://kotobank.jp/word/捻る) explicitly includes 考案する and 考え工夫する; [Digital Daijisen, 考える sense 3](https://kotobank.jp/word/考える) describes devising/creating through ingenuity. This finding does **not** treat 捻る as an unrestricted replacement for “think,” infer a blanket noun/verb exemption, or inherit 工夫’s entire exclusion list. **Confidence: high.**

**F02 — Minor; correctness; `words\日にち.md:27–29`. “Native reading” inaccurately characterizes the complete ひにち reading.**

The wording calls ひにち a “complete native reading.” The recognized spelling 日日 combines **ひ**, a kun reading, with **にち**, an on reading: a mixed kun–on pattern, not an entirely native reading.

**Minimal remedy:** Replace “native reading” with **“word reading”** or simply “reading.” Optionally explain ひ＋にち as mixed reading. No canonical spelling, pronunciation, metadata or app lexical-type change is required, and no historical derivation needs to be asserted.

**Exact evidence:** Complete principal entry **1611370** associates both 日にち and 日日 with ひにち. The complete component record for 日 identifies ニチ as `ja_on` and ひ as `ja_kun`; the existing `kanji\日.md:9–10,34–36` agrees. The applicable [Seisenban 湯桶読み heading](https://kotobank.jp/word/湯桶読み) defines the kun-first/on-second pattern. This is a reading-description correction, distinct from the repository’s coarse `type` classification. **Confidence: high.**

## Optional:

In `words\日にち.md:42–45`, explicitly name **the pinned JMdict snapshot** when contrasting families. The present comparison is supported for entries 1611370 and 1602120, but broader lexical exclusion would be too strong: [Seisenban’s **ひにち** heading, sense ③](https://kotobank.jp/word/日日), also records “daily,” especially in **毎日ひにち／ひにち毎日**. A brief recognition caveat would prevent overreading the database distinction. It would not establish frequency, unrestricted substitution, compiler intent or an independent N2 assignment.

## Limits:

File tools cannot execute Git. The full commit, parent, committed-only status, clean worktree and artifact hash/equivalence claims therefore remain **supplied provenance, not independently executed reviewer checks**. No shell commands or executable validation were run.

Comparison coverage was substantial but not repository-exhaustive; uninspected candidate bodies cannot establish absence of further ambiguity. Existing quiz exclusions were assessed pairwise for both missing and excessive guards, without treating topic proximity, homophony, differing POS or neighboring exclusion cliques as decisive.

Some live requests failed or returned navigation/empty lexical sections—including the attempted 日にち etymology page—and were not counted as verification. Dictionary inclusion does not establish frequency, unrestricted substitution, every example’s naturalness or historical derivation. CLEAN is bounded editorial judgment, not exhaustive correctness or native-speaker certification.
