**Snapshot:** `bfd617ab00c75b9f7a74decd865f1f813b0eabed`, read from the exact authorized branch-ref file after reading `.git` and worktree `HEAD` serially. This authenticates the **ref’s returned commit ID**; I did not verify its cryptographic signature. “Signed checkpoint” is the coordinator’s attestation.

**Scope:** Dependent follow-up by **GPT-6.1 Sol (`gpt-6.1-sol`)**, not another blind initial review. I read the complete returned correction packet and my complete original report, without reported truncation, plus the three authorized metadata files. Assessment also uses the original common packet already read. No other reviewer report, ledger or adjudication was read. Source entries, normalized hashes, Android excerpts and host output are supplied evidence, not independently retrieved, hashed or executed.

## Verdicts

**The original two exclusion findings are resolved. One additional direct exclusion, 勘定/料金, is warranted as a conservative context-free quiz safeguard.** This does not establish unrestricted synonymy.

| Direct pair | Verdict | Specific evidence and reasoning | Confidence |
|---|---|---|---|
| **勘/感覚** | **Resolved; guard justified** | `words\勘.md:9` now directly excludes 感覚. JMdict **1210590 §1** gives perception/intuition/sixth sense; **1212330 §1** includes sense/sensation/feeling/**intuition**. The labels “intuition; hunch” and “sense; sensation” can supply competing answers for intuitive perception. This is ordinary semantic overlap, not equivalence in every bodily-sensation context. | High |
| **勘定/支払う** | **Resolved; guard justified** | `words\勘定.md:9` directly excludes 支払う. **1210750 §2** includes payment/settlement and permits transitive する; **1310300 §1** means “to pay.” Thus “pay” can answer the payment use of 勘定する. Different inflection/POS does not establish safety for these context-free choices. | High |
| **勘定/給与** | **Accept as a conservative safeguard; not a synonym finding** | The direct guard is present at `words\勘定.md:9`. **1230350 §1** is employment pay/salary/wages; §2 is allowance/grant/supply/provision. **1210750 §2** concerns a bill/account and its settlement. Those are meaningfully different. Nevertheless, 給与’s displayed “**pay**; provision of money or goods” can collide with an English payment interpretation of 勘定. The safeguard protects against label ambiguity; it does not prove that restaurant 勘定 and employment 給与 are interchangeable. | Medium |
| **勘定/払う** | **Guard justified; an omission in my initial review is now addressed** | **1501620 §1** explicitly means paying money/a bill; **1210750 §2** supplies the corresponding settlement use. `words\払う.md:4,15` displays “pay” and teaches financial payment. Its additional brushing/removal senses do not eliminate this overlap. The new direct guard is appropriate independently of 支払う. | High |
| **勘定/代金** | **Guard justified; an omission in my initial review is now addressed** | **1411790 §1** expressly includes payment/**bill**/charge/fee; **1210750 §2** includes bill/check/account/payment. The actual labels “reckoning; **bill**” and “price; **payment due**” overlap for an amount owed. `words\代金.md:16,33` confirms the sum-versus-payment-act distinction, but that distinction does not make these labels reliably exclusive. | High |

The supplied `Words.kt:175–185` enforces each declaration symmetrically, both against the target and between distractors. No reciprocal declaration is required, and no transitive inference was used. The existing 計算 guard remains intact.

### 勘定/料金: direct exclusion needed

**NEEDS FIX; moderate quiz-correctness issue; medium-high confidence.**

At `words\勘定.md:9`, 料金 remains unexcluded. Its actual label is **“fee; charge; fare”**, not “payment.” Nevertheless:

- 勘定’s **“bill”** sense includes the amount charged or owed, not only the act of paying.
- 料金’s **“charge”** can be a defensible English answer for that amount in an ordinary service transaction.
- Conversely, an English **“bill”** prompt can reasonably lead a learner toward 料金 when no context distinguishes the amount charged from its account/bill.

This is strongest for **charge/bill**, not for every “fare” or abstract “reckoning” use. JMdict **1210750 §2** supplies bill/check/account/payment; **1554280 §1** supplies fee/charge/fare. The article definitions at `words\勘定.md:16` and `words\料金.md:15` support the contextual overlap. This conclusion does **not** follow from either word’s relation to 代金.

**Minimal remedy:** append `料金` to `words\勘定.md:9`; preserve both titles and their useful distinctions. The supplied reduced-pool output demonstrates that the unguarded pair can appear in **both quiz directions**. It demonstrates reachability, not linguistic ambiguity by itself.

## Findings and reconciliation

**Original findings 1–2: resolved.** The exact requested direct guards are present. Supplied code and bounded test material support the mechanism; I did not independently run it.

**Original findings 3–4: unresolved, minor and pre-existing; nonblocking for this batch’s bounded additions.**

| Article | Accurate remaining gap | Offered-stem consequence |
|---|---|---|
| `kanji\定.md:10,26–33` | さだ.か still lacks its own explanation/example. | `ReadingKey.stem` collapses all three さだ forms; supplied host output offers **さだ.める only**. My initial rationale overstated the likelihood of a separate さだ.か question. |
| `kanji\違.md:10,28–33,46` | ちが.える, -ちが.える, たが.う and たが.える remain unexplained individually. | The supplied algorithm/output offers **ちが.う and たが.う**, not six independent kun questions. The unexplained たが.う therefore remains directly relevant to an offered stem. JMdict **2109290** verifies that reading and its differ/run-counter-to senses. |

The broad authoring instruction **does require every raw kun entry to be explained**. The narrower curated-reading contract requires own rows and linked examples for **explicit selections**; it does not retroactively impose that particular structural validator on every legacy reading. Neither fact cancels the broad editorial gap.

These omissions were not introduced or worsened by the correct new 勘定/勘違い bullets. They therefore **do not require expanding this batch into legacy reading remediation**. Their minimal eventual remedies remain verified rows/examples or appropriately qualified explanations, retaining the raw metadata. They are not “resolved” merely because validator coverage is narrower or offered stems collapse.

**Unchanged 支払う/支払 sample:** the supplied host output places “pay” and “payment” together in both directions. **1310300 §1** and **1594480 §1** establish the verb/payment-noun relationship. That is a credible pre-existing context-free ambiguity, although the words are grammatically distinct. It is **nonblocking for these changed direct pairs**, which neither create nor repair it. A bounded repair would add the direct 支払う/支払 exclusion, without inventing a separate 支払い identity. My initial review did not establish this sample’s production behavior; the supplied follow-up now does.

**Other material omissions:** no further defect established within this bounded follow-up. The initial review missed the 払う and 代金 comparisons; those guards now address them. The 料金 comparison above remains actionable.

**Article facets:** 勘’s original correctness/coverage/text-comprehensibility verdicts remain CLEAN; corrected `words\勘.md` is CLEAN on all three. `words\勘定.md` remains **NEEDS FIX for quiz correctness**, with coverage and textual comprehensibility CLEAN. 勘違い remains CLEAN on all three. 定 and 違 retain the disclosed whole-article coverage/comprehensibility gaps, while their **batch-added teaching is CLEAN**.

## Optional

None beyond the separately scoped legacy remedies identified above.

## Limits

The packet distinguishes older host output from current content version `db93cd80ee101b73`; I have not treated older samples as current-checkpoint tests. Current supplied tests/output provide bounded evidence for guards, reduced pools and both word directions—not exhaustive semantic acceptance or independently verified execution.

No claim is made of native review, phone/font/UI acceptance, handwriting recognition, merged-tree validation, publication, signature verification, or global quiz safety.