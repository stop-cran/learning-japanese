## Snapshot: 519d183f9494ce149cab8317d46d7e3a7c6e41bf — committed content only

**Four new articles need quiz-exclusion fixes, affecting five source rows because 澄む and 清む share one article.** No actionable defect was established in the source mappings, instructional prose, bounded reuse, three kanji edits, or six link-only edits.

The frozen receipt identifies parent `f6a426242ab36af935708baa50f51a9a194861c0`. Snapshot identity and committed-file equivalence are accepted from that receipt, not independently verified with Git.

## Scope: independent, read-only review

Actual model: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`, family `gpt`. No delegation, file edits, or Git execution.

I completely read the eighteen new articles, reused 姓 article, three changed kanji cards, six link-edited word articles, actual related patch, required repository instructions, and specified content-format range. I reviewed all twenty assigned mappings against the principal evidence and repository TSV.

Evidence reading included the complete principal rendering, all thirteen selected-family renderings, supplemental comparison rendering, twenty mapping records, 26 component records, 161 label/exclusion records, and 26 supplied public lexical captures—including the actual ずらっと definition rather than its redirect alone. The supplied counts describe nineteen principal families/42 senses and a comparison union of 260 families/633 senses; these are not independently recomputed archive counts.

I also read actual comparison articles across housing, apology/gratitude, clarity/calmness, movement, queuing, production, properties, dimensions and copying. Consequential findings below use those actual titles, bodies and direct declarations. Fresh Kotobank retrievals supplied usable **精選版 日本国語大辞典** entries for the gratitude and calmness comparisons. Prohibited author rationale, notes and reviewer outputs were not read.

## Verdicts: twenty rows and related edits

Article verdicts include quiz metadata. **CLEAN** means no actionable defect established in the reviewed scope, not exhaustive correctness or native-speaker certification. Mapping verdicts assess source identity, spelling, reading, selected meanings and level separately from quiz configuration.

In the final column, the order is **correctness / scoped coverage / comprehensibility**.

| Source row | Article and status | Correctness | Scoped coverage | Comprehensibility | Mapping verdicts |
|---|---|---|---|---|---|
| N2:862 | 住まい — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:863 | すまない — new | NEEDS FIX — F01 | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:864 | 墨 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:865 | 澄む — new | NEEDS FIX — F02 | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:866 | 清む → 澄む — shared new article | NEEDS FIX — F02 | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:867 | 相撲 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:868 | スライド — new | NEEDS FIX — F03 | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:869 | ずらす — new | NEEDS FIX — F03 | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:870 | ずらり — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:871 | 刷る — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:872 | ずるい — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:873 | すれ違う — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:874 | ずれる — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:875 | 寸法 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:876 | 姓 — bounded reuse | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:877 | 税関 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:878 | 製作 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:879 | 制作 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:880 | 性質 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |
| N2:881 | 清書 — new | CLEAN | CLEAN | CLEAN | CLEAN / CLEAN / CLEAN |

All twenty source spellings/readings and applicable meanings are taught or explicitly recognized. Blank source glosses remain blank rather than being presented as recovered compiler intent. The mappings appropriately distinguish usual-kana presentation, aliases, restricted senses and separately supported public-dictionary extensions. The N2 classification is from a community study list, not an official modern JLPT syllabus.

The following verdicts concern **only the assigned changes**, not wholesale approval or redesign of their older articles.

| Related change | Correctness | Scoped coverage | Comprehensibility | Assessment |
|---|---|---|---|---|
| `kanji\刷.md` | CLEAN | CLEAN | CLEAN | Reciprocal 刷る links at す.る and Common words; metadata, suffix readings and brush-use qualifications preserved. |
| `kanji\税.md` | CLEAN | CLEAN | CLEAN | 税関 linked at ゼイ and Common words; reciprocal word link and metadata preserved. |
| `kanji\清.md` | CLEAN | CLEAN | CLEAN | 清書 linked at セイ and Common words. 清む navigation targets 澄む without inventing a KANJIDIC2 す.む reading. |
| `words\姓.md` reuse | CLEAN | CLEAN | CLEAN | Patch adds only `jlpt: 2`; primary identity, title, reading, body, tags and exclusions preserved. No historical sense is counted as newly authored or independently assigned N2. |
| `words\インク.md:30` | CLEAN | CLEAN | CLEAN | Existing traditional-ink mention correctly links 墨. |
| `words\インキ.md:34` | CLEAN | CLEAN | CLEAN | Existing traditional-ink mention correctly links 墨. |
| `words\透き通る.md:29` | CLEAN | CLEAN | CLEAN | Existing water/sound comparison correctly links 澄む. |
| `words\性格.md:30` | CLEAN | CLEAN | CLEAN | Existing nature/property comparison correctly links 性質. |
| `words\性.md:28` | CLEAN | CLEAN | CLEAN | Existing nature/property mention correctly links 性質. |
| `words\下書き.md:37` | CLEAN | CLEAN | CLEAN | Existing neat/final-copy comparison correctly links 清書. |

## Findings: three actionable quiz issues

**F01 — Medium severity — Correctness: gratitude meanings remain valid wrong choices.**

**Location:** `words\すまない.md:9`, with the taught function at lines 16–21.

すまない explicitly teaches apologetic thanks, and pinned JMdict entry **1610020, sense 3** includes “thank you.” Nevertheless, its exclusions omit **どうも, 感謝, 御礼 and 礼**, and none of those cards directly excludes すまない. Their displayed labels include “thanks,” “gratitude” and “appreciation”: see `words\どうも.md:4,15`, `words\感謝.md:4,16–20`, `words\御礼.md:4,15–20` and `words\礼.md:4,16–19`. These can describe the gratitude use actually taught, even though grammatical construction and register differ. Excluding ありがとう or 恐縮 does not protect these pairs transitively.

**Minimal remedy:** Add direct exclusions for those four IDs on すまない; retain the useful distinctions in the prose. Additional lexical support comes from the actual [どうも entry, sense ④](https://kotobank.jp/word/どうも-581516), [感謝](https://kotobank.jp/word/感謝-470035) and [御礼, sense ①](https://kotobank.jp/word/御礼-455498), not merely their headings. **Confidence: high.**

**F02 — Medium severity — Correctness: the selected mental-state sense lacks direct safeguards.**

**Location:** `words\澄む.md:9`, with the mental-state teaching at lines 16–18. Affects **N2:865 and N2:866 through one article**.

Pinned JMdict entry **1373680, sense 3** explicitly includes becoming serene/tranquil and being free of worries. The existing labels **落ち着く — “calm down; settle”** and **安心 — “peace of mind; relief”** therefore overlap this selected meaning, not merely its topic. Their actual bodies confirm those uses: `words\落ち着く.md:16–18,33` and `words\安心.md:15,28`. Neither side declares the relevant pair. Existing safeguards through 穏やか, 静か or すっきり do not extend transitively.

**Minimal remedy:** Directly exclude **落ち着く and 安心** on 澄む. This preserves the valid serenity sense rather than narrowing it artificially. Fresh evidence: [落着く, 精選版 definition [1]③ロ](https://kotobank.jp/word/落着く-452941), and [安心, あんしん definitions ①–②](https://kotobank.jp/word/安心-29217)—not the separate Buddhist あんじん heading. **Confidence: high.**

**F03 — Medium severity — Correctness: rescheduling can still compete with “change something.”**

**Locations:** `words\ずらす.md:9` and `words\スライド.md:9`.

Both articles directly protect 変更 but omit **変える**, whose actual title is “change something” (`words\変える.md:5`). This is not based solely on a generic change category: 変える explicitly teaches changing a meeting time at lines 16–20, while ずらす teaches moving a meeting earlier at lines 21–26, and スライド teaches shifting a schedule at lines 23–28. “Change something” remains a defensible broad label for those ordinary scheduling uses. The reverse declaration on 変える contains only 変更 and 変化; its connection to 変更 supplies no transitive protection.

**Minimal remedy:** Add **変える** directly to each new article’s exclusions. No prose or source-mapping change is needed. Evidence is the actual articles and their declarations, alongside the selected scheduling meanings of JMdict entries **1006420** and **1073760**. **Confidence: high.**

These findings apply the documented pairwise, symmetric exclusion rule and exact-title-only semantic limitation. They concern possible ambiguous choices under that contract, not a freshly executed app reproduction.

## Optional: none

No nonblocking expansion is proposed. I did not establish an actionable excessive-exclusion defect; shared topics, homophony and spelling alone were not treated as sufficient grounds for adding pairs.

## Limits: provenance and bounded verification

I had **file tools, not Git execution**. Commit identity, clean committed state, hashes and derivative equivalence remain author-executed receipt assertions; I did not independently execute Git or hash checks.

The 26 supplied public bodies are **author captures**, although I read their actual lexical contents. Successful fresh Kotobank checks are distinguished above. Several live Weblio requests returned scaffolding or irrelevant encyclopedia text, and fresh 変える/変わる lookups yielded no usable lexical entry; those responses were not evidence.

I did not read the entire dictionary, every repository article, or every author-captured comparison body. Absence from selected evidence was not treated as proof of dictionary absence. No app execution or independent technical validation was performed. The CLEAN judgments remain bounded editorial findings, not exhaustive certification.
