## Snapshot: d47b7bcdf38197653989bf160bb744bd70b8fd51; committed files only

**All four revised pages are CLEAN within this correction scope.** No actionable defect or consequential unresolved claim remains.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Reviewed sequentially, read-only, without delegation. Read my preserved initial report, the complete 101-line/six-hunk correction diff against `586989dc37529aaa66ff39ba9d84d0560f2a244d`, and all four revised teaching pages completely.

Read relevant JMdict and external-source records in `docs\n2-batch-sources\batch-11.json`; the comparison articles `words\輝く.md`, `words\光る.md`, and `words\決める.md`; and the applicable quiz-format rules. Fetched Kanjipedia’s actual 極 character entry and character-notation guide, plus the referenced app’s word-option label logic.

**Omissions:** No assigned revised passage was omitted. This was not a fresh audit of unchanged batch pages, metadata, drawing paths, or all quiz candidates. Other reports, contributor-documentation changes, prohibited archives, and authored session inputs were not read.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\栄.md` | CLEAN | CLEAN | CLEAN |
| `kanji\極.md` | CLEAN | CLEAN | CLEAN |
| `words\栄える.md` | CLEAN | CLEAN | CLEAN |
| `words\極める.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no established actionable defect in this assigned scope, not exhaustive truth or linguistic certification.

## Findings:

**Original actionable findings:** None were recorded, so there are no original finding IDs to close. However, my initial report’s assertion that no additional quiz exclusions were required was too strong. I withdraw that assertion for the three homograph-related pairs below.

**B11-GPT-R1 — RESOLVED; Moderate; correctness/quiz integrity.**  
`words\栄える.md:8`; `words\極める.md:8`.

The added direct exclusions appropriately protect **栄える–輝く**, **栄える–光る**, and **極める–決める**. JMdict entry **1600620** explicitly permits 栄える／はえる with “shine/glow”; entry **1254180** permits 極める／きめる with “decide/settle.” Those meanings overlap the existing English labels at `words\輝く.md:4`, `words\光る.md:4`, and `words\決める.md:5`.

The established ambiguity is clearest when a Japanese-to-English prompt supplies the written form without disambiguating its reading. The referenced reverse-choice labels include readings—such as 栄える (さかえる) and 極める (きわめる)—so I do **not** claim equal ambiguity in every reverse presentation. Nevertheless, symmetric exclusions correctly keep these pairs apart in both directions. Each pair is declared directly; neither transitivity nor candidate scores are relied upon. **Remedy:** implemented; nothing further required. **Confidence: high.**

**B11-GPT-R2 — ACCEPTED CLARIFICATION; no remaining defect; correctness/scoped coverage.**  
`kanji\栄.md:36`.

The revised qualification accurately acknowledges **見栄／みえ**, its show/vanity sense, and the spelling-level ateji label in JMdict entry **1578350** (`batch-11.json:756–819`). It does not incorrectly characterize 見栄 as unsuitable for everyday use or infer that every component is purely phonetic. Its distinction between attested whole-word spelling and independently established historical reading allocation is appropriately cautious. Keeping **え** lookup-only does not assert dictionary absence; the separate **ヨウ** qualification remains bounded to the inspected evidence. **Remedy:** none. **Confidence: high.**

**B11-GPT-R3 — ACCEPTED CLARIFICATION; no remaining defect; correctness/comprehensibility.**  
`kanji\極.md:36,48–50,55`; `docs\n2-batch-sources\batch-11.json:545–562`.

The fetched [極 entry](https://www.kanjipedia.jp/kanji/0001577800) shows **キョク、ゴク、きわめる、きわまる、きわみ** as table readings and **きめる、きまる** under the outside-table marker. Its [notation guide](https://www.kanjipedia.jp/include/popup_kanji.html) confirms those conventions. The revised note matches this evidence without assigning unsupported status to every derived form or inferring frequency. The neutral 決める／極める spelling statement matches entry **1254180**, including its unrestricted **きめる** reading; the kana-only alternate is not misapplied. **Remedy:** none. **Confidence: high.**

No remaining or regression finding was established in the revised passages.

## Optional:

None.

## Limits:

**File tools were available; Git execution was not.** I could not independently verify HEAD, cleanliness, diff provenance, or the exact ten-file commit scope. Those facts rely on the author-verified checkpoint and supplied diff.

App behavior was assessed from the documented exclusion contract and referenced label implementation, not a running app. Dictionary evidence establishes the cited spellings, readings, senses, and notation—not spelling frequency or historical reconstruction. No consequential claim remains unverified within this revised scope.
