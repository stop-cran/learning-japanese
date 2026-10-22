## Snapshot: f5541b56583c3803328ed0c58c422c1344dcab89; committed files only

Snapshot identity and clean, committed-only status are **as supplied**, not independently Git-verified. The correction comparison is against `d3166cb43733fa6c45908151ec3633044200d54f`.

## Scope: gpt-6.1-sol; family gpt

Read all three revised pages completely: `kanji\星.md`, `words\挟む.md`, and `words\昇る.md`. Read my preserved initial report, `docs\n2-reviews\batch-09-gpt-initial.md`, and the complete supplied `n2-batch-09-correction.diff` covering those pages and the source packet.

Checked the relevant records in `docs\n2-batch-sources\batch-09.json`, including complete 客星 record **2563200**, 昇る’s applicable senses, 挟む/挟まる, 星, 衛星 and 白星; checked comparison labels and direct exclusions against `docs\content-format.md:79-98`.

No assigned revised page or diff hunk was omitted. Other reports, contributor-documentation changes, unchanged batch pages, stroke files and generated-manifest integrity were not reviewed. No edits or delegation were performed.

## Verdicts:

**Both original actionable findings are resolved. No remaining defect or regression was established in the corrected scope.**

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\星.md` | CLEAN | CLEAN | CLEAN |
| `words\挟む.md` | CLEAN | CLEAN | CLEAN |
| `words\昇る.md` | CLEAN | CLEAN | CLEAN |

## Findings:

### G09-001 — RESOLVED
**Original severity:** Medium. **Facets:** Correctness / scoped coverage.  
**Location:** `words\挟む.md:8`.

The revised list directly excludes **掴む, 捕まえる and サンドイッチ**, while retaining 握る and 持つ. All targets exist, and the declaration contains no duplicate or self-reference. These direct edges resolve the original grasping, catching and English “sandwich” collisions without relying on transitive exclusions or changing the accurate teaching text.

**Evidence:** The revised header and comparison headers; JMdict **1600740**, senses 1–3, at `docs\n2-batch-sources\batch-09.json:929-1003`; symmetric, pairwise exclusion behavior at `docs\content-format.md:85-98`. The declared pairs are excluded in both quiz directions on exclusion-aware clients. **Confidence: High.**

### G09-002 — RESOLVED
**Original severity:** Medium. **Facets:** Correctness / scoped coverage.  
**Locations:** `words\昇る.md:4,8,11,15-19,30-38`.

The displayed title and heading now agree on **“rise (sun/moon); be promoted.”** This removes the context-free numerical-increase and getting-to-one’s-feet interpretations behind the original collisions with 増える, 増す, 伸びる, 起きる, 立つ and 立ち上がる. Their existing labels do not supply the qualified astronomical-rising or promotion meanings in either quiz direction. Direct exclusions with 上がる, 登る and 増加 remain intact.

The body correctly retains the broader **natural-rising** explanation: sun/moon examples in the short label do not become a claim that those are the verb’s only possible subjects. The spelling restrictions and promotion example remain consistent with that explanation.

**Evidence:** Revised title, heading, examples and exclusions; comparison headers; JMdict **1352570**, applicable senses 2 and 4, at `docs\n2-batch-sources\batch-09.json:3650-3716`; quiz-label rules at `docs\content-format.md:79-98`. **Confidence: High.**

### Additional changed passages — No regression established

**Locations:** `kanji\星.md:20,29,42`.

The revised meaning paragraph clearly introduces the spot/mark use as another vocabulary use rather than paraphrasing the astronomical definition. 白星 provides a supported victory-mark example.

The ショウ row still realizes the indicated reading through **客星・きゃくしょう**. Its note accurately lists **かくせい, きゃくせい and きゃくしょう**, explicitly distinguishing a dictionary-listed alternative from an assertion about the usual pronunciation. It neither infers frequency from dictionary order nor labels the pronunciation rare without evidence.

**Evidence:** Complete JMdict **2563200** record at `docs\n2-batch-sources\batch-09.json:3772-3808`, including all three readings; **1841410** at lines `3989-4048`, including “victory mark” and “victory”; 星 metadata and **1376310** support the spot/mark meanings. **Confidence: High.**

## Optional:

None.

## Limits:

I have **file tools but no Git execution**. I could inspect the supplied complete correction diff and current file contents, but could not independently verify either checkout, the diff’s provenance, the clean worktree or the exact ten-file commit scope.

Quiz conclusions use the documented label/exclusion behavior, not an executed app. Earlier clients that ignore exclusions remain outside that mechanism’s guarantee. This was a focused correction review, not a fresh audit of unchanged content or linguistic certification. **No consequential claim remains unresolved within the corrected scope.**
