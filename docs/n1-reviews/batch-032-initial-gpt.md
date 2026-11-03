**Snapshot:** `2cbbb0b836a5a2363a175a0df7cd14f12c5f99fc`, as identified by the task; no uncommitted teaching included. Read-only review; no edits, commands, delegation, commits or issues.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`); correctness, scoped coverage and textual phone comprehensibility of all three complete teaching files. Fully read the prescribed instructions and format/level guidance, complete 鶏・鳥・酉 metadata, both complete XML packets—2,352 and 470 lines, 115 + 16 families—and all four kanji and seven word comparison cards. XML reads used consecutive explicit ranges of at most 200 lines, through both closing tags; no returned-range truncations observed.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鶏.md` | CLEAN | CLEAN | CLEAN |
| `words\鶏.md` | CLEAN | NEEDS FIX | CLEAN |
| `words\鶏肉.md` | CLEAN | CLEAN | CLEAN |

**Findings:** **Minor; scoped coverage/navigation; `words\鶏.md:22,29`.** The substantive explanations introduce 鳴く and the component word 肉 without links to their existing articles. This misses the repository’s linked-support contract, although the local explanations remain comprehensible. **Remedy:** link these occurrences to `鳴く.md` and `肉.md`. **Evidence:** the complete comparison articles exist and directly explain the animal-call verb and on-reading ニク; `.github\instructions\content-structure.instructions.md:20–21` requires linking existing cards at substantive introductions or comparisons. **Confidence:** high. This does not require linking every inflected example or incidental compound.

The substantive teaching checks otherwise passed within scope:

- Full readings preserve **ケイ / にわとり / とり**, including order. Both selected kun readings have separate rows and appropriate linked support. Recognition-only ケイ in 養鶏 is supported by KANJIDIC2, JMdict 1547120 and the independently fetched whole-headword entry.
- Radical 196, 鳥 on the right, 19 strokes and grade 8 match the supplied metadata. The eight-stroke left-side description is consistent with the shape; its association is explicitly a mnemonic, not historical or phonetic evidence.
- JMdict 1252990 supports domestic chicken and chicken meat. Entry 1253020 supports 鶏肉/とりにく; the broader bird-meat sense is restricted to 鳥肉. The native-first mixed classification is explicitly qualified and does not misclassify ニク as kun.
- **The proposed 鶏/鶏肉 exclusion is justified:** the actual labels “chicken” and “chicken meat” overlap with 鶏’s documented ordinary meat sense. A one-sided declaration protects both directions. No additional exclusions were established merely from the broader labels “bird” or “meat; flesh.”
- Default kanji distractors “fish,” “station” and “black” are semantically distinct; three are supplied, avoiding default four-choice fallback. 鳥 is appropriately retained as a comparison rather than a wrong answer.
- All four required directed kanji–word links exist for the two support words. The reused 鶏肉 card retains explicit N5 vocabulary metadata; the new word does not inherit N1 from its kanji.
- Examples, readings, translations and particle explanations are sound. Rooster/hen distinctions respect the spelling-restricted broader male/female-bird senses. Special whole readings and specialist, foreign-food, historical or proverb families do not establish additional literal readings or require vocabulary expansion here.

**Optional:** None.

**Limits:** Source packets and snapshot provenance are frozen supplied evidence, not fresh upstream dictionary retrieval; hashes were not independently recomputed. Independently fetched and inspected the actual Nikkoku にわとり heading and shorter とり supplementary note, the separate archaic headings, and the 養鶏 whole-headword opening. Coordinator-preserved raw HTML was not read or hash-verified; historical and husbandry material was not adopted as teaching evidence.

The scoped `confusable-words.md` search returned no matches for the assigned words or chicken/poultry terms; the remaining inventory was not reviewed. Comparison cards were inspected for this batch’s contrasts and quiz exposure, not comprehensively recertified. Snapshot identity and the stated one-link baseline diff were supplied, not independently checked with Git.

This is textual review, not fresh font, native-rendering or physical-phone certification. The supplied inherited font evidence and existing 炒 limitation remain distinct from pending batch-032 Android, combined-main, CI and public-ZIP checks. No overlapping tool calls were observed in this review; other process execution evidence was unavailable.
