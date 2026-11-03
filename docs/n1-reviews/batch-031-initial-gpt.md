**Snapshot:** `55948b53b86d06e5385059208557d5d9fb707e0f`, as identified by the frozen task. Committed teaching only; no uncommitted content included. Read-only review; no files changed.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`), reviewing correctness, scoped coverage and textual phone comprehensibility of both complete teaching files: `kanji\猿.md` and reused `words\猿.md`.

Completed all required instruction/reference ranges, including the specified tails; complete input metadata containing 猿・園・申; and every line of all three frozen dictionary packets, using explicit XML ranges of at most 200 lines. Family counts independently confirmed: **155 + 18 + 4 = 177**. Read all five complete comparison kanji articles (園・鳥・風・申・犬) and all ten complete comparison word articles (人間・動物・動物園・見る・登る・木・馬鹿・ずるい・くだらない・ばからしい). Also inspected the source snapshot and confirmed 猿’s community-list membership.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\猿.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\猿.md` | **CLEAN** | **CLEAN** | **CLEAN** |

**Findings:** None established within scope.

The consequential checks supporting these verdicts are:

- **Readings and metadata:** The new card preserves KANJIDIC2’s complete Japanese lists and order, `[エン]` and `[さる]`, together with 13 strokes, grade 8 and indexing radical 94. It explains 犬’s visible 犭 form. The selected `さる` row has dictionary-supported linked word evidence; both relative directions of the 猿 kanji/word pair are present. Nanori are not promoted into quiz readings.
- **Lexical scope and examples:** JMdict 1177390, sense 1, and the independently fetched Nikkoku **さる【猿】** entry support the broad nonhuman-primate usage. The articles avoid imposing a strict English monkey/ape division. Both animal sentences, kana readings and translations are natural and consistent; the climbing example supports its progressive interpretation. JMdict 1643040 supports 日本猿／にほんざる and standalone ニホンザル. The explanation correctly distinguishes compound voicing from independent さる.
- **Recognition and contrasts:** JMdict 1556110 and the independently fetched **類人猿（るいじんえん）** heading support the recognition example. No constituent reading is inferred merely from a kana substring. JMdict 1362820 and the actual 申 article support the separate zodiac use. The mnemonic is explicitly modern-shape imagery, not asserted etymology. The three curated kanji labels—“park; garden,” “bird,” and “wind; style”—are defensibly wrong for 猿; the inspected comparison meanings establish no additional ambiguity.
- **Word exclusion:** `words\猿.md:9` independently warrants `[馬鹿]`: 猿’s derogatory noun “idiot” sense overlaps 馬鹿’s ordinary noun “fool/idiot” sense and actual displayed title, “fool; foolish.” Animal prose cannot disambiguate that context-free quiz. The guard is direct and bidirectional under the documented client contract. The inspected adjective labels for ずるい・くだらない・ばからしい do not establish equivalent person-denoting nouns requiring additional 猿 exclusions; 馬鹿’s existing relationships do not create transitive exclusions.
- **Restricted and peripheral families:** The complete packets distinguish poetical 猿／ましら (2743210), search-only 猨, restricted 猿滑／しび and search-only 猿滑り, 猿子’s rosefinch and rare-monkey senses, and 猿楽’s spelling/reading/sense restrictions. None contradicts the bounded teaching or requires exhaustive species, technical, historical or vocabulary expansion.

**Optional:** None.

**Limits:** Snapshot identity and unchanged N3 vocabulary provenance were supplied by the task, not independently verified through Git or upstream vocabulary retrieval. Frozen XML and recorded hashes are source evidence, not fresh upstream downloads or independently recomputed hashes. Both Kotobank entries were independently fetched and their relevant headings/body inspected; dated taxonomy, historical citations and origin theories were not adopted as general teaching conclusions. Preserved raw HTML was not read.

The `confusable-words.md` inspection was a scoped search for the relevant terms, returning no matches—not a complete inventory review. Default four-choice curation was assessed against the documented contract and assigned comparisons, not every repository fallback candidate.

Comprehensibility verdicts concern text, not fresh font/native/physical-phone certification. Supplied bundled-cmap evidence remains inherited; batch-031 Android, combined-main, CI and public-ZIP checks remain pending, with physical-phone/general-release acceptance outstanding. No overlapping tool calls were observed in this session; tool-internal execution and other processes were not inspected. No other reviewer reports or author adjudication records were opened.
