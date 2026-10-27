## Snapshot: `c84fdd3ce4b8467016517e5a21219a0dc54ea5da`; committed content only

Parent: `2101fdd861825c254d34132e8586b030d2ac460a`.

Snapshot identity rests on the frozen receipt. **File tools were available, but not Git execution or executable hash verification**, so I could not independently confirm that the accessible files equal that commit.

## Scope:

Independent, read-only review by **GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`**; no delegation or edits.

Read all twenty new articles completely, all twenty assigned TSV mappings and complete principal dictionary families, the supplied three-file patch, and changed passages in context. Also inspected component evidence, all 146 supplied comparison-card labels/exclusions, targeted complete comparison families, relevant existing cards, vocabulary-title searches restricted to `words\`, and public dictionary entries.

Read the required repository instructions and format reference. No prohibited authoring material or other reviewer’s output was accessed. The related-file verdicts below concern **only the specified changes**, not unchanged teaching.

## Verdicts:

**Three quiz-exclusion gaps need fixes.** No actionable defect was established in the twenty source-use mappings or the articles’ explanatory prose within their practical scope. Correctness below includes quiz metadata.

| Source row | New article under `words\` | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:422 | `砕く.md` | CLEAN | CLEAN | CLEAN |
| N2:423 | `砕ける.md` | CLEAN | CLEAN | CLEAN |
| N2:424 | `くたびれる.md` | CLEAN | CLEAN | CLEAN |
| N2:425 | `くだらない.md` | CLEAN | CLEAN | CLEAN |
| N2:426 | `下る.md` | CLEAN | CLEAN | CLEAN |
| N2:427 | `唇.md` | CLEAN | CLEAN | CLEAN |
| N2:428 | `口紅.md` | CLEAN | CLEAN | CLEAN |
| N2:429 | `くっつく.md` | **NEEDS FIX** | CLEAN | CLEAN |
| N2:430 | `くっつける.md` | CLEAN | CLEAN | CLEAN |
| N2:431 | `くどい.md` | CLEAN | CLEAN | CLEAN |
| N2:432 | `句読点.md` | CLEAN | CLEAN | CLEAN |
| N2:433 | `配る.md` | CLEAN | CLEAN | CLEAN |
| N2:434 | `工夫.md` | **NEEDS FIX** | CLEAN | CLEAN |
| N2:435 | `区分.md` | CLEAN | CLEAN | CLEAN |
| N2:436 | `組み合わせ.md` | CLEAN | CLEAN | CLEAN |
| N2:437 | `組み立てる.md` | **NEEDS FIX** | CLEAN | CLEAN |
| N2:438 | `汲む.md` | CLEAN | CLEAN | CLEAN |
| N2:439 | `酌む.md` | CLEAN | CLEAN | CLEAN |
| N2:440 | `悔しい.md` | CLEAN | CLEAN | CLEAN |
| N2:441 | `悔やむ.md` | CLEAN | CLEAN | CLEAN |

**Mapping-only verdicts:** Each mapping N2:422–N2:441 is **CLEAN / CLEAN / CLEAN** for correctness, scoped coverage and comprehensibility. Each source spelling/reading/use is explicitly taught, not merely matched by an entry ID.

Important qualifications are handled correctly: 工夫 follows the agreeing `くふう` reading and entry 1278220 rather than teaching the contradictory worker gloss; the separate `こうふ` entry does not acquire N2 status. 組合せ is explicitly covered as an unrestricted spelling of 組み合わせ. 汲む/酌む overlap is supported by their individual families rather than inferred solely from a combined heading. 悔やむ positively teaches source-selected mourning. Selected senses are non-exhaustive; additional senses are distinguished without independently assigning each one N2.

Written-kanji arrays are complete. The six stated missing primary component cards are absent; their characters remain in metadata. Substantive article links and declared exclusion targets exist.

| Related change reviewed | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\紅.md:32,39,49`: 口紅 at kun べに; entry 1276110 attribution | CLEAN | CLEAN | CLEAN |
| `kanji\区.md:30,42,50`: 区分 at on ク; entry 1244230 attribution | CLEAN | CLEAN | CLEAN |
| `kanji\読.md:31`: link around existing 句読点 at トウ | CLEAN | CLEAN | CLEAN |

## Findings:

**GPT22-F01 — Moderate; correctness: unguarded ingenuity labels.**

**Location:** `words\工夫.md:4,9,16`; comparator `words\知恵.md:4,15–18`.

工夫 displays **“ingenuity; devising a method”**, while 知恵 displays **“wisdom; practical ingenuity.”** Neither side excludes the other. “Ingenuity” is therefore a defensible answer for 知恵, despite the titles not being exactly equal. This can penalize a correct understanding; it does not require treating the Japanese words as unrestricted synonyms.

**Minimal remedy:** Add `知恵` directly to 工夫’s `quiz_exclusions`, preserving both meanings and 知恵’s existing N3 level.

**Evidence:** The actual titles and explanations above; complete principal JMdict 1278220, senses 1–2. Independently inspected [Daijisen 工夫](https://www.weblio.jp/content/工夫), `くふう`, definition 1, and [Daijisen 知恵](https://www.weblio.jp/content/知恵), `ちえ`, definition 1: practical method-finding and the capacity to plan/resolve matters substantiate the displayed English overlap. `docs\content-format.md:80–96` requires semantic safeguards beyond exact-title deduplication. **Confidence: high.**

**GPT22-F02 — Moderate; correctness: unguarded sticking/clinging labels.**

**Location:** `words\くっつく.md:4,9,16–19`; comparator `words\べたべた.md:4,8,15–19`.

くっつく displays **“stick to; keep close to”** and explicitly teaches clinging/staying beside someone. Existing べたべた displays **“sticky; clingy”** and teaches closely clinging people. Neither declares this pair. The overlap is an ordinary taught use, not merely a shared texture category; “clingy” can reasonably describe the human use of くっつく.

**Minimal remedy:** Add `べたべた` directly to くっつく’s `quiz_exclusions`.

**Evidence:** Complete principal JMdict 1003860, senses 1–3; the two actual cards. Independently inspected [Daijisen べたべた](https://www.weblio.jp/content/べたべた), adverbial definitions 1–2, including its explicit くっつく construction, and [Daijisen くっ付く](https://www.weblio.jp/content/くっつく), reading `くっつく`, definitions 1–2. These establish physical adherence and interpersonal clinging, not just similar spellings. **Confidence: high.**

**GPT22-F03 — Moderate; correctness: unguarded “setting up” answer.**

**Location:** `words\組み立てる.md:4,9,16`; comparator `words\セット.md:4,9,16–18`.

組み立てる is not excluded from セット, whose displayed title is **“set; setting up.”** The complete principal family explicitly includes **“to set up”** in 組み立てる’s ordinary assembly/construction sense. Without a sentence identifying assembly versus configuration, “setting up” remains a defensible English answer. The different Japanese usages do not remove this label ambiguity.

**Minimal remedy:** Add `セット` directly to 組み立てる’s `quiz_exclusions`; retain the useful distinction between assembling parts and configuring something.

**Evidence:** Complete pinned JMdict 1397580, sense 1, and comparison family 1074600, sense 2 (“setting up,” “preparing,” “arranging,” “configuring”); both actual card headers. This concerns the overlapping English answer, not a claim that setting an alarm means assembling it. **Confidence: medium-high.**

All three pairs lack protection in either direction. Existing exclusions through other words do not repair them: exclusions are pairwise, not transitive, and must also prevent ambiguous pairs appearing together as other choices.

## Optional:

None.

## Limits:

The receipt’s Git identity, clean-content assertion, hashes and evidence equivalence were not independently executable. Preservation against the parent was directly inspectable only through the supplied three-file patch; I did not retrieve a separate parent tree.

Comparison work was targeted, not a complete reread of all 269 comparison families or an exhaustive audit of the entire vocabulary collection. Public dictionary bodies were independently inspected where cited; author inspection receipts were not treated as independent retrieval.

No app draws were executed. Findings establish ambiguous pairs permitted by the documented title/exclusion rules, not their occurrence frequency. CLEAN means no actionable defect established within this scope—not exhaustive correctness, corpus validation or native-speaker certification.
