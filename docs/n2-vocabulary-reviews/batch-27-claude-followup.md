## Snapshot
- **New commit:** `c98832d1bc9f30ea040829e23a1fe79d8db85f7e`. Its parent is the previously confirmed `ac74524ac2d47d12c0b2caf8bd430f47f9ab580b`.
- I only had file, search and web tools, so I could not run Git. The commit identity, the clean tree and all hashes are the author's claims, including file hash `1e42d2e0…` for 公務, diff hash `1e1a885d…` and evidence hash `25c56e32…`. The claim that the evidence derivative matches the canonical file is also the author's.

## Scope
- **Model:** claude-opus-5.5, Claude family, working alone. This is a bounded follow-through on one changed passage, not another nineteen-card review.
- **Read in full:** my previous confirmation, the receipt, the whole patch (both hunks) and the 公務 article.
- **Comparison cards read in full:** 役, 役割, 係 and 責任, all unchanged.
- **Evidence derivative:** I located the appended section (lines 25449–26130) and spot-checked its new families, adjudication and limits against the patch. They match.
- **My own checks:**
  - I searched `words\` titles for duty, responsibility, service, official, office, job, work, role, position, charge and public.
  - I looked up 役, 責任 and 係/がかり through Jisho's API, which serves JMdict data.

## Verdicts
| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 公務 guards (line 9) and comparisons (lines 40–43) | CLEAN | CLEAN | CLEAN |
| Appended packet evidence (six families, four labels, pairs, adjudication) | CLEAN | CLEAN | CLEAN |

## Findings
- **B27-01 (合同) and B27-02 (公務: 務め, 勤め, 義務):** still resolved and untouched by this commit.
- **B27-03 (公務/役): resolved.**
  - 役 is now excluded at `words\公務.md:9`, and lines 40–41 add the comparison.
  - My Jisho lookup confirms 1537970:1 lists "role; assignment; responsibility; duty".
  - The 役 card teaches roles, responsibility and positions.
- **公務/役割 (my earlier optional note): resolved.** 1538000:1 lists "duties", and the card title says "allotted duties".
- **公務/係: justified on its own evidence.** 1589840:1 lists "duty", which my lookup confirms, and the title includes "assigned duty". The comparison text, "an assigned duty or the person responsible", matches the 係 card.
- **公務/責任: justified on its own evidence.** 1383180:1 lists "duty; responsibility", which my lookup confirms. The 責任 card explicitly teaches responsibility and duty, not only blame. Its bare "responsibility" label makes it the weakest of the four pairs, but it is consistent with the existing guard on 務め ("duty; responsibility").
- **My own title sweep:** I found no other pair that needs a guard.
  - These titles share only an English word with "official public duties" ("official", "office", "work", "charge"), which is not enough: 作業, 職, 担当, 公式, 正式, 官庁, 庁, 用事 and 公務員.
- **Regression check:**
  - None of the four partner cards already declares 公務, so there are no duplicate declarations.
  - All four links resolve.
  - The 16 articles carry 111 exclusions in total, matching the claim.
  - No regression found.
- **Earlier optional items:** 高度/良い, 高等/偉い, 合理/理由 and the naturalness questions remain optional. I accept the no-change decisions.

## Optional
At `words\公務.md:38–39`, the sentence "These are broader…" covers only 務め, 勤め and 義務. The four new comparisons don't state how they differ from 公務. A short closing sentence would help, such as "None of these by itself specifies official public business." This is not blocking, because the Meaning section defines the public and official scope clearly.

## Limits
- I could not run Git or check any hashes.
- My only independent sources were Jisho's API, whose JMdict version may differ from the pinned snapshot, and my earlier Kotobank 松 lookup. I retrieved no Daijisen pages.
- I could not reconcile the author's tally of "thirty readable family records". I count 28 spelling, reading and sense records. This doesn't affect content.
- I read the evidence derivative only in bounded sections.
- I did not run the app's quiz draws or measure selection frequency.
- Nothing here is certified by a native speaker or by corpus data, and the community N2 list is not an official JLPT syllabus.
