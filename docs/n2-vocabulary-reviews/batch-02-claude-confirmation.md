## Snapshot
- **Revised commit:** ae22a9861e76507bf8080c062b85a587c1ddaddd. The parent is the original shared snapshot a0423388624ed50b0a348ad6f7dd7c212b3850b9.
- **Content:** committed content only, as stated in the receipt.
- **Git limit:** I had file tools but no Git, so I couldn't confirm the commit or check its hashes. The five files I read match the patch's added lines exactly.

## Scope
- **Reviewer:** claude-opus-5.5 (Claude family), working alone with no edits.
- **Articles:** the changed passages of あてはめる, 宛名, あたりまえ, 暖まる and 暖める, each read in full article context.
- **Comparison cards:** 適用, 名前, 名, もちろん and 暖かい, plus the 温 kanji card's lines on 暖.
- **Evidence:** the batch-02.json reviewEvidence section (lines 2419–2717) and dictionary entries 1586430 and 1586440.
- **Prior findings:** I checked my own B02-CL-01 to B02-CL-03 against the changes.
- **Not covered:** this is not a re-review of the unchanged batch. I didn't read other models' reports or any of the excluded documents.

## Verdicts
| Article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| あてはめる | CLEAN | CLEAN | CLEAN |
| 宛名 | CLEAN | CLEAN | CLEAN |
| あたりまえ | CLEAN | CLEAN | CLEAN |
| 暖まる | CLEAN | CLEAN | CLEAN |
| 暖める | CLEAN | CLEAN | CLEAN |

These verdicts cover the changed passages only.

## Findings

**B02-CL-01 (あてはめる / 適用): resolved**
- 適用 is now excluded (あてはめる.md:9) and a comparison sentence was added (:37–38).
- The exclusion is supported by the cards themselves:
  - The titles are "apply a rule; fit into" and "application of a rule or method".
  - The dictionary sense for 適用 is "application (of a rule, law, method…)".
  - The two cards use nearly the same rule-to-case pattern.

**B02-CL-02 (あたりまえ / もちろん): resolved**
- もちろん is now excluded (あたりまえ.md:9), with a hedged sentence at :43–44.
- もちろん's title is "of course", and its dictionary entry also lists "naturally".
- The article itself translates あたりまえでしょう as "of course", so a learner could defend either answer.

**B02-CL-03 (暖/温 spelling guidance): resolved**
- Both articles now carry a hedged tendency statement: 暖まる.md:30–32 and 暖める.md:31–33.
- Both cite official entry 007 (暖まる.md:48–49, 暖める.md:49–50). The statement matches the supplied extract: 暖 for weather and air (暖まった空気, 室内を暖める), 温 for food (スープを温める).
- Each article now has a room example and a food or drink example, so the examples show the tendency being described.
- 暖める links 暖かい; 暖まる already did at :39.
- **Withdrawn:** my earlier guess that 温 is "often" used for the body. It was never verified, and the revision makes no claim about body spelling either way.
- The replaced body and hand examples are not shown to have been wrong. The dictionary records both spellings for "warm oneself".

**New 宛名 exclusions (名前, 名): supported, no regression**
- Each pair is backed directly by the labels: 宛名's title includes "name", and the article translates 宛名 as "the recipient's name".
- 名前 is titled "name" and 名 is titled "name; renown".
- None of these titles are exact matches, so the app would not already keep them apart.
- 名 already excludes 名前, but that doesn't make these exclusions redundant, because exclusions aren't transitive.

**Overall:** the changes are minimal and no title, reading, level or kanji metadata changed. I found no new actionable regression.

## Optional
- **暖まる.md:43–45:** the paragraph opens with "I warmed myself" but now illustrates with a room, which repeats the contrast at :36–37. Either give a person example or reword the English opening.
- **暖まる.md:20:** the kana reading writes スープ as すーぷ. 暖める.md:23 and most of `words\` keep it in katakana.
- **暖まる.md:20:** the 温 spelling appears before it is explained at :28–32. A short note in the example line would help.
- **あたりまえ.md:43–44:** say concretely that もちろん is an adverb, while あたりまえ is normally a predicate or modifier.
- **Earlier optional items** outside the changed passages, such as 暖める's "warm" label, remain optional and unassessed.

## Limits
- Without Git I couldn't verify the commit identity, the file, diff or prompt hashes, or whether manifest.json was regenerated.
- The official PDF came back as compressed bytes, so I relied on the supplied extract and the reviewEvidence record. I did not read entry 007 myself.
- I didn't run the validator or the app's quiz builder; the effect of the exclusions is inferred from docs\content-format.md.
- Which spelling is preferred for body and hands remains unestablished, but these cards no longer make any claim about it.
- These verdicts are not a native-speaker certification.
