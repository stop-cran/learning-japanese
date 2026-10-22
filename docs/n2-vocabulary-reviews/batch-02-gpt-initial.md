## Snapshot: a0423388624ed50b0a348ad6f7dd7c212b3850b9 — committed content only

Parent: `04aed4865849ea4b8362dd1dff068d8066f2f681`.

The frozen receipt declares this snapshot clean and committed. **I have file tools, not Git execution**; snapshot identity, cleanliness and hash verification therefore rely on that receipt rather than an independent Git check. No files were edited.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed all 14 new articles below completely, including metadata, examples, comparisons, displayed meanings and quiz exclusions. Checked mappings **N2:22–N2:41**, the complete supplied JMdict entry families, spelling/reading/sense restrictions, and relevant KANJIDIC2 component records. The vocabulary classification is a pinned **community study list**, not an official modern JLPT syllabus.

Read the actual related patch and inspected changed passages in context on kanji **厚, 圧, 戸, 甘, 編, 温, 雨, 名, 物, 危**. Reviewed the four vocabulary-level additions and the six specific reuse claims separately. Consulted existing comparison/quiz-candidate cards and public dictionaries where relevant.

Work was sequential, without delegation. Explicitly excluded forbidden reports, ledgers, private authoring inputs and other reviewers’ output; unassigned source rows; comprehensive review of unchanged teaching; and stroke-file review.

## Verdicts

**Two missing quiz-exclusion guards need fixing.** All 20 source rows have explicit coverage of their mapped spelling or alias, reading and intended lexical use. No actionable defect was established in the new articles’ teaching prose.

| New article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `words\暖まる.md` | CLEAN | CLEAN | CLEAN |
| `words\暖める.md` | CLEAN | CLEAN | CLEAN |
| `words\あたりまえ.md` | CLEAN | CLEAN | CLEAN |
| `words\厚かましい.md` | CLEAN | CLEAN | CLEAN |
| `words\圧縮.md` | CLEAN | CLEAN | CLEAN |
| `words\宛名.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\あてはまる.md` | CLEAN | CLEAN | CLEAN |
| `words\あてはめる.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\あぶる.md` | CLEAN | CLEAN | CLEAN |
| `words\あふれる.md` | CLEAN | CLEAN | CLEAN |
| `words\雨戸.md` | CLEAN | CLEAN | CLEAN |
| `words\甘やかす.md` | CLEAN | CLEAN | CLEAN |
| `words\編物.md` | CLEAN | CLEAN | CLEAN |
| `words\危うい.md` | CLEAN | CLEAN | CLEAN |

The **ten changed kanji passages** are **CLEAN / CLEAN / CLEAN** for correctness, scoped coverage and comprehensibility. Their added examples preserve whole-word readings and supply the required reciprocal links. The 温まる/温める links legitimately reach articles that explicitly teach those alternative spellings.

The **four level-only edits** are likewise **CLEAN / CLEAN / CLEAN** within their narrow scope: the patch adds only `jlpt: 2`, replacing no established vocabulary level and changing no identity, reading, title, teaching or exclusion.

| Reuse claim | Correctness | Scoped coverage | Comprehensibility | Basis |
|---|---|---|---|---|
| N2:25 あちらこちら → `あちこち.md` | CLEAN | CLEAN | CLEAN | Explicit alternate-form teaching connects it to the here-and-there expression; existing N3 is preserved. |
| N2:31 暴れる → `暴れる.md` | CLEAN | CLEAN | CLEAN | Violent/wild behavior, raging and physical struggling are explicitly taught. |
| N2:32 脂 → `脂.md` | CLEAN | CLEAN | CLEAN | Fat, grease, tallow and lard are explicit; oil distinctions remain qualified. |
| N2:37 余る → `余る.md` | CLEAN | CLEAN | CLEAN | Surplus and amounts left beyond need are explicit. |
| N2:39 編む → `編む.md` | CLEAN | CLEAN | CLEAN | Knitting is explicitly taught; existing compilation teaching does not independently establish that sense’s N2 membership. |
| N2:41 怪しい → `怪しい.md` | CLEAN | CLEAN | CLEAN | Suspicious and doubtful uses are explicit; existing N2 and stable identity are preserved. |

These reuse verdicts concern the assigned coverage claims, not comprehensive certification of those existing articles.

## Findings

**B02-GPT-01 — Minor; correctness, quiz-answer ambiguity**  
**Location:** `words\あてはめる.md:4,9,16–21`; comparison `words\適用.md:4,15–19`.

The new title **“apply a rule; fit into”** overlaps directly with 適用’s **“application of a rule or method”**, but neither card excludes the other. Both articles teach applying a rule to a case. Consequently, a quiz can offer two defensible answers; different wording and noun/verb presentation do not establish distinct lexical answers here.

**Minimal remedy:** Add `適用` to あてはめる’s `quiz_exclusions`. One declaration protects both directions.

**Evidence:** The supplied JMdict entry **1586530, sense 1** records the transitive application/adaptation use. [デジタル大辞泉, 当て嵌める, sense 1](https://kotobank.jp/word/当て嵌める-425770) explicitly defines it using **適用する** and gives formula/rule constructions. [Jisho’s actual 適用 entry](https://jisho.org/search/適用), JMdict **1437500**, identifies **てきよう**, a noun/transitive suru verb, with “application (of a rule, law, method, etc.).” The inspected headers contain no direct guard.

**Confidence:** High.

**B02-GPT-02 — Minor; correctness, quiz-answer ambiguity**  
**Location:** `words\宛名.md:4,9,16–21`; comparison `words\名前.md:5,15`; `words\名.md:4,9,16`.

宛名 explicitly includes the **recipient’s name alone**, not only a complete name-and-address block. Nevertheless, its only exclusion is 住所. Existing answer labels **“name”** (名前) and **“name; renown”** (名) can therefore appear as competing answers for 宛名’s ordinary name-only use.

This is not merely correspondence-related vocabulary sharing a topic: “name” names an explicitly taught dictionary sense. The existing 名/名前 exclusion does not protect either pair involving 宛名, because exclusions are not transitive.

**Minimal remedy:** Add both `名前` and `名` to 宛名’s `quiz_exclusions`, retaining its accurate teaching and title.

**Evidence:** Supplied JMdict **1586520, sense 1**, explicitly includes **“(addressee’s) name”** alongside name-and-address and addressee. The [actual 宛名 entry on Jisho](https://jisho.org/search/宛名) confirms **あてな** and those senses. The article’s 宛名の漢字 example itself demonstrates the name-only interpretation. Neither existing name card declares an exclusion with 宛名.

**Confidence:** High for the lexical overlap and missing guards; moderate-to-high for the quiz-label judgment.

## Optional

None.

## Limits

Snapshot membership and clean committed status could not be independently verified without Git execution or local hash computation. The supplied receipt is the boundary identifying the reviewed files as committed content.

No application runtime or generated quiz was executed; quiz findings follow the documented exact-title deduplication and symmetric, non-transitive exclusion behavior. Initial simplified public-dictionary extractions were incomplete; findings use the subsequently inspected actual entries and supplied records, not those incomplete extracts.

No consequential linguistic claim remains unresolved within the assigned scope. **CLEAN** means no actionable defect established here—not exhaustive dictionary coverage, a whole-corpus quiz audit, or native-speaker certification.
