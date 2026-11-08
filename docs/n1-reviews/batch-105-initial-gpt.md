## Snapshot

`27e252daa091e21c907ff6799818f6b2da74c7aa`, identified by the supplied packet as the signed teaching snapshot. Its teaching diff adds only `kanji\勁.md` and `words\雄勁.md`; it shows no baseline edits or changed reused passages. Signature, Git state and hashes were not independently verified.

## Scope

**Reviewer:** GPT-6.1 Sol (`gpt-6.1-sol`), independently reviewing the supplied text.

Read exactly one resource, using one `view` call with `forceReadLargeFiles=true` and no range: `C:\Users\stop-\n1-kanji-workspace\control\batch-105-initial-packet.txt`. The response showed no truncation marker; I read the returned packet through its final `docs\jlpt-levels.md:1–23` block. The stated 257,669-byte/5,129-line dimensions were not independently counted.

Inspection covered both complete new articles, all 49 complete existing comparison/fallback bodies, nine member and 28 comparison JMdict occurrences—36 distinct complete families—the supplied complete character records, four extracted public dictionary entries and provenance receipts, generated stroke data and source SVG, and the supplied Android reading implementation. Existing comparison articles were context, not rewrite assignments.

## Verdicts

| New article | Correctness | Scoped coverage | Phone-TEXT comprehensibility |
|---|---|---|---|
| `kanji\勁.md:1–47` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\雄勁.md:1–37` | **CLEAN** | **CLEAN** | **CLEAN** |

**CLEAN** means no established actionable defect within this textual review, not exhaustive correctness or device acceptance.

### Readings, identity and metadata

- 勁 preserves the complete sourced Japanese lists and order: on `[ケイ]`, kun `[つよ.い]`. Explicit selections `[ケイ]` and `[]` produce **one on-reading key, `けい`, and no kun-reading key**, under the supplied `ReadingCard.quizReadings`/`ReadingKey` implementation. The full kun reading remains metadata; selecting no kun questions does not invalidate it.
- The selected ケイ has its own table row and linked example at `kanji\勁.md:31`. JMdict 1839950 establishes **雄勁・ゆうけい**. Independently of kana-substring matching, the supplied character records and public character entries establish 雄 **ユウ** and 勁 **ケイ**, supporting the allocation ユウ＋ケイ.
- JMdict 1236070 flags **勁い**, **剛い** and **毅い** as search-only spellings. Its seven complete senses and the `…に～` qualification do not turn those spellings into ordinary recommended usage. The article correctly preserves documented **勁い・つよい**, recommends ordinary **強い**, and explicitly distinguishes navigation to 強い from an example written with 勁.
- Other lexical identities remain separate: 強い **こわい** is not imported into the つよい family; 強力 **きょうりょく** is not ごうりき; 力 **ちから**, **りき** and suffix **りょく** are not interchangeable reading assignments.
- The N1 label is explicitly a **community classification**, not an official published syllabus. Grade 9 is correctly explained as name-use classification, not a frequency claim or a restriction of every occurrence to personal names. No supporting-word JLPT level is inferred.
- 雄勁 correctly includes **both written kanji**, `[雄, 勁]`, without demanding a nonexistent 雄 card or link.

### Meaning, grammar and comprehensibility

The supplied Daijisen 勁 entry directly supports both **strength** and **tautness**. 雄勁’s description of vigorous, forceful expression in calligraphy, painting, poetry and prose matches the supplied dictionary text. These are characteristic contexts, not an absolute restriction; `words\雄勁.md:33` makes that qualification explicit.

JMdict 1839950 and Daijisen support noun/na-adjective treatment. **雄勁な筆跡**, its reading **ゆうけいなひっせき**, and “vigorous handwriting” accurately expand and translate the dictionary’s abbreviated example. The explanation identifies な attachment and supplies polite **雄勁です**, without inventing an i-adjective or automatic する verb.

The component explanation is a defensible meaning aid: 雄’s supplied strength/imposing-quality sense and 勁’s strength reinforce the interpretation. It neither claims historical derivation nor makes the compound male-only. The comparisons correctly distinguish ordinary broad 強い and broader 力強い, including the latter’s separate **reassuring/encouraging** sense.

The short sections, kana support, translated attested phrase and explicit attachment guidance are comprehensible as phone **text**. No additional example or unsupported frequency requirement is necessary for this scope.

### Meaning-choice guards

The actual displayed target **“strong; taut”** is distinct from curated wrong labels **功 “merit; achievement,” 劾 “censure; impeach,” 剖 “dissect; split open.”** Their supplied bodies and character records do not reveal an ordinary secondary strength/tautness meaning that defeats those choices. Sharing 力 or another visual feature does not create semantic equivalence.

The four direct kanji guards **勁–強/剛/力/勢** are justified by ordinary strength, power and force overlap. The six direct word guards **雄勁–強い/強力/力強い/剛健/力/勢い** are defensible protections against broad strength/vigor answers; they do not assert universal substitutability.

I inspected the remaining supplied candidates rather than treating different labels or parts of speech as automatic safety:

| Comparisons | Bounded assessment |
|---|---|
| 硬, 固; 硬い/固い/堅い family | Hardness, stiffness and firmness deserve attention, including the family’s noninitial “strong” sense. That evidence does not by itself establish equivalence between the **character labels** and 勁’s strong/taut teaching target. No additional direct pair established. |
| 精, 勇, 凌 | Refinement/vitality, courage/high spirits, and endurance/surpassing are distinguishable from the target labels. No additional direct pair established. |
| 活気, 活力, 元気 | Their energy/vigor senses were considered, not dismissed because of grammar. Liveliness, vitality and well-being do not alone establish 雄勁’s forceful stylistic quality. |
| 体力, 実力 | Physical stamina, broader organizational strength, actual ability and coercive force were all considered. These are not established equivalents of the offered stylistic gloss. |
| 勇ましい, 生き生き | The noninitial rousing/vigorous sense and vivid expressive use are relevant comparisons. Neither courage/rousing effect nor animation/vividness is identical to forceful style merely because English descriptions overlap. |
| ぐいぐい, ばりばり, もりもり | Strong pulling/progress, vigorous work and welling strength were inspected alongside drinking, sound, stiffness and appetite senses. Shared vigor alone does not establish a missing direct guard. |
| エネルギー | Its ordinary strength/power/stamina sense—not only physics—was considered. It does not establish equivalence to vigorous artistic/prose style. |

Restrictions and flags were kept local: for example, the かたい family’s spelling-restricted predicted-outcome and Go senses, ごうりき’s 強力-only carrier-guide sense, 筆跡’s restricted ふであと reading, and search-only/irregular/usually-kana forms were not generalized across families. The martial-arts member entries likewise do not broaden the selected lesson into ordinary unrestricted usage.

**No missing or excessive direct pair is established from the supplied comparisons.** This is not exhaustive pool certification. Exclusions remain symmetric **direct, nontransitive pairs**, not synonym cliques.

### Links and shape evidence

The single all-mapped required reciprocal pair **勁–雄勁** is present in **both directions**: the kanji’s linked example and the word’s substantive 勁 link. The supplied diff introduces zero activated baseline pairs and zero baseline edits. Incidental mentions do not require backlinks.

Canonical radical **力, no. 19**, its right-hand position, and **nine strokes** agree with the character record and SVG. The generated JSON contains nine ordered paths consistent in endpoints, sequence and component placement with the supplied SVG. The 巠-left/力-right description and contrast with right-hand 刂 are supported. The mnemonic is explicitly modern-shape—not an unsupported origin or phonetic claim.

## Findings

**Proved defects: none.**

**Actionable hypotheses: none established.** The potential semantic overlaps discussed above do not, on this evidence, justify declaring additional exclusions mandatory.

## Optional

None.

## Limits

- No independent Git/signature/hash verification, upstream retrieval, archive decompression or external source consultation occurred. Public dictionary evidence was the coordinator-supplied extracted text and provenance, not independently fetched pages.
- No truncation was indicated in the returned read; packet dimensions and completeness beyond that returned evidence were not independently measured.
- The stated absence of 勁/巠/刂 from all three bundled font cmaps was supplied task context, not independently inspected font data. **Cmap absence is not evidence of glyph failure or unreadability.**
- Native four-font/default fallback, actual glyph appearance, rendered drawing, drawing interaction, rendered UI and physical-phone readability/acceptance remain unverified.
- Actual default-N1/All/custom live pools and finite semantic option-set acceptance were not executed. No exhaustive future-pool safety, commonness, historical reconstruction or measured learning effectiveness is claimed.
- This review made no edits and does not certify publication or runtime acceptance.
