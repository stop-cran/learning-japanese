## Snapshot
**Frozen commit:** `1347683020fb124c01d8279169a855e60b33ab10` (parent `cd7539603e4e9afee9bd656a8011bea9fbbabdd2`). I reviewed committed content only.

I had file tools only and could not run Git or compute hashes. So I could not confirm that the files I read match the commit exactly, and the patch and evidence packet are taken as given.

## Scope
**Model:** claude-opus-5.5 (claude family), in a fresh process that did no authoring.

**Read in full:**
- The 17 new articles
- The 3 reused articles (越す, ごちそう, こっそり)
- The 7-file related patch
- The kanji cards 凍, 腰, 個 and 超, plus 越 for context
- TSV rows N2:542–561
- copilot-instructions, the content-structure instructions, content-format:18-119, and jlpt-levels.md
- A grep of confusable-words.md (no hits)

**Evidence packet sections read:**
- The rows and the 20 principal entry families
- The comparison families 1595910 and 2862559
- The existing comparison labels
- actualEntryInspections, quizDeclarations and sourceAccessLimits

**Collision checks:** I grepped word titles and read the bodies of 勘, 備える, 生物, 掻く and マスター.

**Fetched myself:** Daijisen entries for 越す and 拵える.

**Not read:** I did not open any forbidden file, and did not read every one of the 102 comparison families or 27 component records.

## Verdicts
**New articles** (correctness / scoped coverage / comprehensibility)

| Article | Correctness | Coverage | Comprehensibility |
|---|---|---|---|
| ごくろうさま | CLEAN | CLEAN | CLEAN |
| 焦げる | CLEAN | CLEAN | CLEAN |
| 凍える | CLEAN | CLEAN | CLEAN |
| 心当たり | CLEAN | CLEAN | CLEAN |
| 心得る | CLEAN | CLEAN | CLEAN |
| 腰掛け | CLEAN | CLEAN | CLEAN |
| 腰掛ける | CLEAN | CLEAN | CLEAN |
| 五十音 | CLEAN | CLEAN | CLEAN |
| 胡椒 | CLEAN | CLEAN | CLEAN |
| こしらえる | NEEDS FIX (B28-01) | NEEDS FIX (B28-01) | CLEAN |
| 擦る | CLEAN | CLEAN | CLEAN |
| 個体 | CLEAN | CLEAN | CLEAN |
| ごちそうさま | CLEAN | CLEAN | CLEAN |
| こちらこそ | CLEAN | CLEAN | CLEAN |
| 小遣い | CLEAN | CLEAN | CLEAN |
| コック | CLEAN | CLEAN | CLEAN |
| 古典 | CLEAN | CLEAN | CLEAN |

For こちらこそ, the only lexical evidence is the pinned JMdict entry; the public lookup failed (see Limits).

**Reuse claims**
- **越す (N2:552):** level 3, the identity, the title, [越] and the existing exclusions are unchanged.
  - Correctness: CLEAN. 難関を越す is attested in Daijisen sense 1, and 百人を超しました is a natural quantity sentence.
  - Coverage: the 超す spelling is taught with the こす reading, but the mapping's sense qualification needs a fix (B28-02).
  - Comprehensibility: NEEDS FIX (B28-03).
- **ごちそう (N2:555):** CLEAN on all three facets. It already teaches the treating and feast senses. Level 4, the empty kanji list and the identity are unchanged. The 御/走 notes are accurate: 走 is read ソウ in 馳走.
- **こっそり (N2:560):** CLEAN. Only `jlpt: 2` is added; the word had no earlier level.

**Kanji changes:** 凍, 腰, 個 and 超 are all CLEAN. Each links its words at the correct reading, and the source IDs are correct. 超's 超す label links to 越す.md, which does teach 超す.

**Mappings:** N2:542–550 and N2:553–561 are CLEAN on all three facets.
- N2:551 needs a fix for its additional sense 2 (B28-01).
- N2:552 needs a fix for its selected-sense choice (B28-02).

## Findings
**B28-01**
- **Severity / facets:** Low; correctness and scoped coverage, plus the N2:551 mapping.
- **Where:** `words\こしらえる.md:17,50,54`; `docs\n2-vocabulary-sources.tsv:551`.
- **Problem:** Line 50 says the examples teach "making, building, preparing, and making up", but there is no building example. The wooden box is the "make" sense (JMdict 1567390 sense 1), and the packed lunch is make/prepare.
  - Building is only stated in passing at line 17, with no object or construction.
  - Even so, N2:551 claims 1567390 sense 2 (build/construct) as an additional taught sense.
- **Fix:** Either add one building example, such as 庭に棚をこしらえた or 家をこしらえる (Daijisen ①), or remove "building" from line 50 and drop sense 2 from N2:551.
- **Evidence:** JMdict 1567390 sense 2 is "to build; to construct". Daijisen 拵える ① (which I fetched) lists 藤棚を拵える and 家を拵える.
- **Confidence:** high.

**B28-02**
- **Severity / facets:** Low; the mapping qualification for scoped coverage.
- **Where:** `docs\n2-vocabulary-sources.tsv:552`; `words\越す.md:32-34`.
- **Problem:** The source row is spelled 超す, and the mapping selects 1175300 senses 1–3 (cross, get over hardship, pass time). But the article uses 超 only in the quantity sentence, which is sense 4. The mapping's own note admits that 超 is not extended to crossings, time or hardship. So the selected senses are not the ones taught with the source spelling.
- **Fix:** Make 1175300 sense 4 the selected sense for this row. Record cross/pass/tide over as a mismatch in the raw gloss, as N2:556 already does for ごちそうさま. Treat senses 1–3 and 5 as teaching under the 越 spelling.
- **Evidence:**
  - Daijisen 越す (which I fetched) marks senses 1 (including 難関を越す), 3 (time), 4 (overtaking) and 6 (moving, honorific) as written （越す）. Only sense 2, exceeding a quantity or standard (一万人を―す), has no spelling mark.
  - JMdict sense 4 carries the note "often 超す".
  - jlpt-levels.md:59-62 requires checking spelling-restricted senses against the spelling actually taught.
- **Confidence:** medium. JMdict itself has no spelling restrictions on these senses, so the current mapping is defensible under an entry-level reading of the rules.

**B28-03**
- **Severity / facets:** Low; comprehensibility of the newly added 越す passage.
- **Where:** `words\越す.md:30` (existing text) and `:34` (new text).
- **Problem:** Line 30 says the preference "is not a blanket spelling prohibition", and line 34 says 越 is "the useful starting point" for crossing a mountain or the new year. Together they suggest 超す also works there (年を超す, 山を超す), but Daijisen limits those senses to 越す. This matters more now that the card is the coverage target for 超す.
- **Fix:** Rewrite line 34 along these lines: "write 越す for crossing, getting through difficulties, passing time and moving; 超す is for exceeding a number or level, where 越す also occurs."
- **Evidence:** the Daijisen spelling marks described in B28-02.
- **Confidence:** medium.

## Optional
- **Possible quiz overlaps**
  - こしらえる and 備える share the word "prepare". The 準備, 用意 and 支度 overlaps are already excluded, but 備える is not; this is inconsistent but not decisive.
  - 個体 and 生物 share "organism"; this pair may actually be a useful distractor.
  - 心得る overlaps マスター ("have a command of" / "master a skill") and 詳しい ("knowledgeable").
  - 心当たり and 勘 overlap as "inkling" / "hunch".
  - Weaker overlaps: 焦げる and じりじり ("scorching"); コック and 料理 ("cook").
- **Content and wording polish**
  - 心得る could add a full example for sense 2. 心得ました can also sound stiff or old-fashioned, and the 〜と心得る ("regard as") use is untaught, which is fine outside the selection.
  - The コック title "tap valve" would read better as "tap; valve".
  - `越す.md:26` mentions "tides or audience approval", a reference to source quirks that learners may find opaque.
  - `こしらえる.md:54` cites "senses 1-3", while the TSV lists sense 1 as selected and 2, 3 and 7 as additional; these could be aligned.
- **Outside this batch:** in the existing `kanji\越.md:33,38`, 越す is not linked, even though 超.md now links to 越す.md.

## Limits
- **No Git or hashes:** I could not confirm that the files I read match the frozen commit, and I could not verify the receipt or component hashes.
- **Partial evidence:** I did not read all 102 comparison families or the 27 component records in full. Selected evidence is not the whole dictionary.
- **Public lookups:** my own こちらこそ lookup returned no dictionary text, only page chrome. The author's other Daijisen receipts were not re-fetched and remain author assertions.
- **Judgement, not certification:** whether examples sound natural is my reviewer judgement, not corpus or native-speaker certification. I did not run the app's quiz.
- **Collision search:** this was a title grep plus targeted reads, not a semantic scan of every card.
