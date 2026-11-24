**Snapshot:** B162, candidate `4dcff959aaa5394e35342e11b9f2c48d846f395e` (base `2eb37d43`). I used only the supplied packet. I made no edits, ran no subprocesses and delegated nothing.

**Scope:** One reviewer, Claude Sonnet 5.5 (`claude-sonnet-5.5`). Facet: linguistic correctness, restricted senses, reading allocation and scoped coverage.
- Read in full: the 19 new cards (10 kanji, 9 words), `reused-word.txt`, `changed.txt`, `sources.json`, `support-families.xml`, `quiz.txt`, `related-labels.txt`.
- Read selectively: `all-families.xml`, to confirm the entries cited below.
- Comprehensibility, consistency and manifest integrity were not assigned. I give only incidental notes on them.

**Verdicts** (the first label is correctness, the second is scoped coverage):

| Article | Verdict |
|---|---|
| 塁 | NEEDS FIX / NEEDS FIX (F1, F4) |
| 墜 and reused 落ちる | NEEDS FIX / NEEDS FIX (F2, F4) |
| 彫塑 | NEEDS FIX / CLEAN (F3) |
| 壇 (word) | UNVERIFIED (naturalness of the examples) / CLEAN (F5) |
| 塑, 塚, 塾, 墳, 壌, 壮 (kanji) | CLEAN / CLEAN |
| 墾 (kanji) | CLEAN / CLEAN (F4, minor) |
| 壇 (kanji) | CLEAN / CLEAN |
| 一塁, 塚, 塾, 古墳, 開墾, 土壌, 壮大 (words) | CLEAN / CLEAN |
| Reused 一, 古, 土, 大, 開, 彫 | Added lines CLEAN; whole cards UNVERIFIED (diffs only) |

All metadata readings for the 10 new kanji appear in their reading tables or source-only rows. 壇 タン is correctly allocated to 土壇場 (JMdict 1445460).

**Findings**

1. **Medium. Reading allocation. `kanji-1.txt`, 塁 (Readings, Meaning, Notes).**
   - **Claim:** The card gives the fortification sense only to 塁 とりで ("JMdict also lists 砦") and keeps ルイ for baseball only. The Notes sentence "neither word for a defensive structure…" has no clear referent.
   - **Evidence:** JMdict 1555910 (塁 るい, news1) has sense 1 "base" (baseball) and sense 2 "fortress; stronghold", with no restriction. JMdict 1295240 makes 砦 the headword for とりで, and 塁 is only a "rarely used kanji form". 本塁 (1523300) also has "main fort".
   - **Impact:** A learner would treat 塁=とりで as the standard way to write "fort" and would not know ルイ also covers it.
   - **Remedy:** Add "fortress" to the ルイ row. Say 砦 is the usual spelling and 塁 is rare. Reword the Notes sentence.
   - **Confidence:** High.

2. **Minor. 墜 and 落ちる. `kanji-2.txt`; `reused-word.txt` ("How the kanji combine").**
   - **(a)** The card gives 墜ちる as the only common word. `sources.json` marks お.ちる as outside the table, but the card does not say so. JMdict gives 墜ちる no priority tags, while 墜落 is ichi1/news1/nf09 and is not linked. ツイ is not quizzed (`quizOnyomi` is empty), but お.ちる is.
   - **(b)** "For a fall from a height… 墜ちる" is not a JMdict restriction, because 1548550 lists 墜ちる for the whole entry. It also conflicts with the card's own examples (a glass off a desk, a leaf from a tree), where 落ちる is required.
   - **Remedy:** Present it as a rarer spelling for a plunge or crash, such as an aircraft, and state that this is teaching guidance. Flag お.ちる as outside the table. Consider listing 墜落 first.
   - **Confidence:** Medium-high on the inconsistency. Medium on the usage nuance, since I could not check Daijisen or a corpus.

3. **Minor. `words-1.txt`, 彫塑 (Distinctive meaning).**
   - **Claim:** "A narrower dictionary use refers to making a model for a sculpture."
   - **Evidence:** JMdict 1428070 sense 2 is "clay model", which is not the same. The claim names no dictionary. Priority tags: 彫塑 is news2/nf44; 彫刻 is ichi1/news1/nf06.
   - **Impact:** The claim is not checkable, and the card gives no hint that 彫刻 is the everyday word.
   - **Remedy:** Align the wording to the source or cite the exact Daijisen wording. Add a short register note.
   - **Confidence:** Medium.

4. **Minor. Cross-card.** 塑 でく, 塚 チョウ and 壌 つち are flagged as outside the table. 塁 とりで, 墜 お.ちる, 墾 ひら.く and 壮 さかん are not, although `sources.json` lists all of them as "outside". The JMdict "rare" notes on 墾く and 壮ん partly cover those two. Remedy: flag them consistently. Confidence: high on the evidence.

5. **Minor, unverified. `words-3.txt`, 壇.**
   - **Claim:** 先生は壇に上がった and 壇を下りた use the bare noun.
   - **Evidence:** JMdict supports 壇 (ichi1) and 壇上 (1802300). It does not attest these collocations.
   - **Remedy:** Confirm they are attested. Otherwise add a 壇上 example or say that 壇 is mostly met in compounds.
   - **Confidence:** Low.

6. **Conditional quiz ambiguity. `quiz.txt`, `related-labels.txt`.**
   - **Claim:** Exclusions are one-way in the files. 塚 excludes 古墳, but 古墳 excludes only 墓. 土 and 彫刻 do not exclude 土壌 and 彫塑 (彫刻 excludes only 刻む). 墳 lacks 塚, and 台 and 舞台 are unchecked against 壇.
   - **Evidence:** The labels "ancient burial mound" and "mound; burial mound" overlap. So do "earth; soil" and "soil; ground for growth", and "carving; engraving; sculpture" and "sculpture; carving and modeling".
   - **Impact:** If the app applies exclusions only from the target card, two answers could look correct. I could not verify how the app applies them.
   - **Confidence:** Unverified.

**Optional (not defects)**
- 一塁: JMdict sense 2 "first baseman" has no example.
- 壮: the title says "robust", but no word shows that sense.
- 開墾: "Reclamation" appears in the Distinctive meaning without being introduced. It is JMdict's third gloss.
- 墾: ひら.く could point to 開く sense 9, "open up new land".
- 古墳: no Kofun-period note.

**Limits**
- Digital Daijisen and Kanjipedia pages were not opened. Claims resting on them are unverified: おつ as the classical form, the narrower 彫塑 sense, and 塑 vs 彫.
- For 一, 古, 土, 大, 開 and 彫 I read only the diffs. I could not confirm their reading tables contain イチ, コ, ド, ダイ, カイ and チョウ.
- 彫 "Additional word entries: 1497380" is 浮き ("float; buoy"). I could not tell what it is cited for.
- I did not check that link targets exist: 盛ん, 耕す, 舞台, 学校, 立派, 土地, 台, 丘, 墓.
- I did not review shape and look-alike claims or stroke data.
- `all-families.xml` ranges not read: 120–300, 640–1020, 1420–1500, 1520–1760, 2090–2255, 2560–2700, 2860–2990, and the end of the file after line 3510. Entry 2832593 was checked only in `support-families.xml`.
- The packet has no native-speaker or Android evidence.
