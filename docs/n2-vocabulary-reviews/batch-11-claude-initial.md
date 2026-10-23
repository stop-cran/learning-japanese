## Snapshot
Frozen commit: **2eccc7af442aeb9cbcb7c064650a2e6b63b11e1e** (parent 1aaf5435e579a352cfdc3069e0656be0d5f4fc2c). I reviewed committed content only. I had file tools but no Git, so I could not check out the commit or confirm the receipt's file hashes. I assumed the working-tree files match that commit.

## Scope
- **Model:** claude-opus-5.5 (Claude family), fresh process, sequential, no delegation, no edits.
- **New articles:** all 19 read in full.
- **Related edits:** the 8 changed passages, read in context from the patch: おどかす, お菓子, ください, どうぞ, 休日, 宜しく, 菓子 and kanji 各. I did not re-review unchanged teaching in those files.
- **Reuse claim:** 叔母さん→伯母さん, assessed for aunt coverage only.
- **Mappings:** N2:202–221 checked against batch-11.json rows and principal families, plus the comparison families needed for quiz and link checks.
- **Forbidden files:** none of the forbidden docs or reports were read.

## Verdicts
Columns are correctness / scoped coverage / comprehensibility.

| Article | Verdict |
|---|---|
| 驚かす | CLEAN / CLEAN / CLEAN |
| お願いします | CLEAN / CLEAN / NEEDS FIX (R1) |
| 各々 | CLEAN / CLEAN / CLEAN |
| おはよう | CLEAN / CLEAN / NEEDS FIX (R3) |
| お参り | CLEAN / CLEAN / CLEAN |
| お待たせしました | CLEAN / CLEAN / CLEAN |
| お待ちどおさま | CLEAN / CLEAN / CLEAN |
| おめでたい | CLEAN / CLEAN / CLEAN |
| 思いがけない | CLEAN / CLEAN / CLEAN |
| 思い込む | CLEAN / CLEAN / CLEAN |
| 思いっきり | CLEAN / CLEAN / CLEAN |
| 思い付く | CLEAN / CLEAN / NEEDS FIX (R2) |
| 重たい | CLEAN / CLEAN / CLEAN |
| おやすみ | CLEAN / CLEAN / CLEAN |
| おやつ | CLEAN / CLEAN / CLEAN |
| 親指 | CLEAN / CLEAN / CLEAN |
| オルガン | CLEAN / CLEAN / CLEAN |
| 卸す | CLEAN / CLEAN / CLEAN |
| 恩恵 | CLEAN / CLEAN / CLEAN |

- **Eight related changes: CLEAN ×3.** The links are useful and target taught spellings or uses; for example, 休日 links to [お休み] at おやすみ, which teaches that spelling. 各 now has a reciprocal link to 各々 at the reading おのおの.
- **Reuse claim: CLEAN ×3.** 伯母さん.md explicitly teaches 叔母さん at おばさん. The source's "middle-aged lady" gloss belongs to the separate entry 2261510 (小母さん) and is not claimed.
- **Twenty mappings: CLEAN ×3,** except that N2:214's comprehensibility depends on R2.
  - Rows match the TSV exactly.
  - Explicit alias teaching is present for 思い掛けない, 思いっ切り, お早う, お休み, 思いつく, 各各/各 and お待ち遠様.
  - Kana-formula rows map to written IDs from the same entry.

## Findings
**R1: Minor, comprehensibility (quiz).** Files: お願いします.md:9,16,21,25; 願う.md:4,9; 願い.md:4,9.
- **Claim:** 願う ("wish for; request") and 願い ("wish; request") are not excluded from お願いします ("please").
- **Learning impact:** The article itself calls お願いします a deferential request ("I would like to ask for this") and ties it to 願う. Both cards share the kanji 願, so they are likely quiz candidates. Picking "request" for お願いします, or お願いします for "request", is defensible in either direction. 頼む ("request; ask a favor") is already excluded for the same reason.
- **Remedy:** Add 願う and 願い to the お願いします quiz_exclusions.
- **Confidence:** medium-high.

**R2: Minor, comprehensibility.** File: 思い付く.md:4,16,29,33.
- **Claim:** The title and the N2:214 mapping (senses 1–2) promise "recall", but line 16 only says a recall meaning exists. There is no example and no guidance on when to use it instead of 思い出す, which line 29 describes as recalling.
- **Learning impact:** Learners may use 思い付く for ordinary remembering, such as 名前を思い付いた for "I remembered the name."
- **Evidence:** JMdict 1589330 sense 2 is "to remember; to recall". Kotobank 精選版日本国語大辞典 [2] lists 思い出す under ある考えが心に浮かぶ, i.e. something coming to mind.
- **Remedy:** Add one attested example of recall as something suddenly coming to mind (for example, an errand). Add one sentence saying that deliberately recalling names or past events normally uses 思い出す.
- **Confidence:** medium.

**R3: Minor, comprehensibility (quiz).** Files: おはよう.md:2-8,17-18; 朝.md:5,8.
- **Claim:** Both example translations render おはよう as "Morning." 朝 has the title "morning", shares the wago type and tag, and is not excluded.
- **Learning impact:** In the English→Japanese direction, おはよう is a defensible answer for "morning" ("Distinct wording does not establish distinct answers").
- **Remedy:** Add `quiz_exclusions: [朝]`; 午前 ("morning, a.m.") is optional.
- **Confidence:** medium.

## Optional
- **お願いします:29:** "its constructions differ" is imprecise, because noun + を works with both forms. The real difference is the te-form, which the Distinctive section already states.
- **重たい:** 精選版日本国語大辞典 says its meaning and usage are narrower than 重い. A tendency note could help.
- **思いっきり:** consider excluding 覚悟 ("mental preparedness; resolve") because of noun sense 2.
- **Other quiz exclusions to consider:** 恩恵 vs おかげ; 卸す vs 売れる.
- **Possible additions:**
  - 驚かせる next to 驚かす.
  - 思いがけず under 思いがけない.
  - 思い込み under 思い込む.
  - お八つ (the "three o'clock" origin) under おやつ.
  - That どお in お待ちどおさま comes from 遠い.

## Limits
- I could not verify the commit or the file hashes (no Git).
- The Daijisen text for 思い付く and 重たい did not render on Kotobank, and the Weblio fetch for 思い付く returned only boilerplate. These count as limits, not evidence.
- I independently confirmed the author's Kotobank receipts for おめでたい-222110 and 御待遠様-454401. I did not fetch the receipts for おめでた-222109 or Weblio 卸す; those remain author assertions.
- Quiz-candidate likelihood is inferred from the documented selection rules; I did not run the quiz.
- This is not a native-speaker certification. Unchanged teaching in the related files and in 伯母さん was not recertified.
