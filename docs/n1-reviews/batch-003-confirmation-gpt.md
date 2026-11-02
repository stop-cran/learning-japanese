**Snapshot:** Corrected committed teaching `b99945c23eb8eb9a3cdd10a8a736a51d6c6cce71`, compared with original `6ce567650e6663d712bac25bebd5bead0d0af655`. No uncommitted teaching included. Snapshot identity and frozen status are supplied, not independently Git-verified.

**Scope:** Bounded changed-passage confirmation by GPT-6.1 Sol (`gpt-6.1-sol`), read-only. Read completely: `docs\n1-reviews\batch-003-confirmation-prompt.txt`, `batch-003-confirmation.diff`, `words\苗.md:1–38`, `words\植える.md:1–34`, `words\稲.md:1–34`, `words\植物.md:1–49`, and `docs\n1-sources\batch-003-review-supplement-jmdict.xml:1–73`. No truncation remained. Used my own original review and its previously inspected complete 苗 dictionary family; did not reread the earlier dossier or access another report/progress record.

**Verdicts:**

| Changed file | Correctness | Scoped coverage | Textual comprehensibility |
|---|---|---|---|
| `words\苗.md` | CLEAN | CLEAN | CLEAN |

**Findings:** None remaining in the changed passage or its integration.

**Reconciliation:**

| Observation | Status | Evidence and assessment |
|---|---|---|
| Original **F1**, Minor, correctness/scoped coverage, original `words\苗.md:8`: missing direct 苗/植える exclusion | **Resolved** | Corrected line 8 explicitly includes `植える`. Its actual title remains **“plant”** (`words\植える.md:4`), which does not expose the intended verbal interpretation. JMdict **1490470, sense 1**, supports 苗 as “seedling; young plant”; supplementary **1357250, sense 1**, identifies 植える as a transitive verb, “to plant/to grow/to raise.” The direct exclusion prevents the demonstrated English-label ambiguity without claiming lexical synonymy. Existing 苗/植物 and 植物/植える edges alone would not protect this pair. Confidence: high. |
| Additional direct 苗/稲 safeguard, independently assessed here | **Optional safeguard accepted; no defect established** | Corrected line 8 includes `稲`, whose actual title is **“rice plant”** (`words\稲.md:4`). JMdict **1490470, sense 2**, explicitly includes “rice seedling” for 苗; supplementary **1167820, sense 1**, defines 稲 as “rice plant (Oryza sativa).” This supports the narrow guard against a defensible alternative label for 苗’s documented rice-seedling sense. It does not imply unrestricted interchangeability or require excluding every taxonomic relationship. Confidence: high. |

The supplied exact diff changes only the exclusion list, retaining `芽`, `植物` and `木`. Both added IDs correspond to the inspected existing cards. No body, title, reading, example or navigation change introduces a textual regression.

The 稲 safeguard was **not a finding or optional observation in my original report**; accepting it here does not retrospectively add an initial defect or change my original severity.

**Optional:** None further.

**Limits:** This is confirmation of the exact correction, not a fresh ten-file review. My original ten-file textual verdict now needs no remaining defect qualification: 苗’s correctness and scoped-coverage verdicts become CLEAN; the other verdicts remain unchanged within their original scope. Original evidence and execution limitations still apply. The seven previously assessed reading keys and their support mappings are unaffected, not freshly revalidated here.

The supplementary dictionary families are coordinator-extracted frozen evidence, not my own upstream retrieval or hash verification. No commands, edits, app execution, manifest verification, physical-phone/native-speaker testing or measured-learning assessment was performed. **No consequential in-scope textual claim remains unresolved.**
