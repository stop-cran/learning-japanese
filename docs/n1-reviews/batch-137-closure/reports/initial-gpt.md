Snapshot: `d3c7394d38992b24d3689bc984fdb4a6cf60bc54` — batch 137. Reviewer: OpenAI GPT, operating as GitHub Copilot; the exact deployed model/version is not exposed to me. Packet manifest SHA-256 verified as `bd69f948c5d0920d042cb2aa100d6e30d788f65e9783e1049cf399f491fb3dfb`.

Scope:

Reviewed all 15 new kanji cards, their 15 stroke files, all 21 modified word articles, and all 23 diffs. The two existing kanji cards were reviewed only around their changes. Facets 3 and 4 received the deepest examination, including actual displayed meaning options, all 16 selected reading prompts, exclusions in both directions, and beginner-facing explanations.

The following inventory lists every packet file opened. Braces enumerate individual filenames; they do not mean a directory scan.

**Read in full:**

- `INSTRUCTIONS.md`
- `mechanical-checks.md`
- `rubric\copilot-instructions.md`, through successive ranges.
- `snapshot\kanji\{丁,井,仰,但,傑,傷,僕,卸,司,吐,呂,哀,哲,唯,善}.md`
- `snapshot\strokes\{丁,井,仰,但,傑,傷,僕,卸,司,吐,呂,哀,哲,唯,善}.json` — complete structured parsing, including every point; 傷 also received a complete textual read.
- `snapshot\words\{お風呂,丁寧,井戸,但し,信仰,傑作,傷,僕,包丁,卸す,司会,吐き気,吐く,哀れ,哲学,唯一,善,改善,火傷,風呂,風呂敷}.md`
- `diffs\{kanji__寧.md.diff,kanji__敷.md.diff}`
- `diffs\{words__お風呂.md.diff,words__丁寧.md.diff,words__井戸.md.diff,words__但し.md.diff,words__信仰.md.diff,words__傑作.md.diff,words__傷.md.diff,words__僕.md.diff,words__包丁.md.diff,words__卸す.md.diff,words__司会.md.diff,words__吐き気.md.diff,words__吐く.md.diff,words__哀れ.md.diff,words__哲学.md.diff,words__唯一.md.diff,words__善.md.diff,words__改善.md.diff,words__火傷.md.diff,words__風呂.md.diff,words__風呂敷.md.diff}`
- `evidence\source-metadata.json`
- `evidence\joyo-pages.md`, through successive ranges, including front matter and appendix.
- `evidence\kanjipedia-outside-readings.json`
- `evidence\daijisen-heads.txt`
- `evidence\okurigana-scan.txt`
- `evidence\audits\quiz-safety.txt`
- `evidence\audits\reading-exposure.txt`
- `evidence\audits\reading-options.txt`
- `evidence\app-code\QuizBuilder.kt`
- `evidence\app-code\KanjiMeaningMetadata.kt`
- `evidence\public-source\{weblio-丁.txt,weblio-井.txt,weblio-仰.txt,weblio-但.txt,weblio-傑.txt,weblio-傷.txt,weblio-僕.txt,weblio-卸.txt,weblio-司.txt,weblio-吐.txt,weblio-呂.txt,weblio-哀.txt,weblio-哲.txt,weblio-唯.txt,weblio-善.txt}`
- `titles\kanji-titles.tsv` and `titles\word-titles.tsv` — complete structured indexes used for title uniqueness, referenced labels, links, and available word identities; unrelated rows were not individually linguistically reviewed.

**Read in part:**

- `packet-manifest.json` — identity fields, returned opening material, and complete byte hash; not its entire file listing.
- `repo\docs\content-format.md` — the kanji-format and quiz-authoring material, reliably returned lines 71–139.
- `repo\docs\confusable-words.md` — opening material, reliably returned lines 1–32.
- `evidence\provenance.json` — lines 1–100.
- `evidence\kanjidic2-records.xml` — opening lines and structured metadata/readings/meanings for all 15 new characters and selected comparison characters; not every field of every record.
- `evidence\jmdict-families.xml` — opening lines, all families cited by the 15 new cards, and selected additional reading-audit/word records. Forms, reading restrictions, senses and register labels were examined; the complete evidence collection was not read entry by entry.
- `evidence\jmdict-digest.tsv` — header/opening rows and the first six prioritized rows for each batch character.
- `evidence\app-code\KanjiReadings.kt` — lines 1–130.
- `evidence\app-code\Words.kt` — lines 1–145 and 200–302, plus an earlier line-count operation.
- `snapshot\kanji\寧.md` — lines 70–95, including the changed bullet and surrounding Notes.
- `snapshot\kanji\敷.md` — lines 40–56, including the changed bullet and surrounding passage.
- `repo\kanji\{日,額,上,見,擦,削,冴,凌}.md` — first 22 lines of each.
- `repo\kanji\互.md` — first 20 lines.

**Independent public verification:**

- Retrieved and inspected the live Digital Daijisen/Weblio and Kanjipedia character entries for all 15 new characters. These were fresh lookups, not merely the supplied extracts.
- Inspected actual live word entries through the Jisho API for all 21 modified word identities, plus 仰山, 卸下, 丁幾 and 善い人, including readings, senses, restrictions and register labels.
- Supplementary live Daijisen checks included 仰山, 丁年, 丁々, 唯々諾々, 天井, 油井, 仰ぐ, 仰せ, 仰る, 傷む, 傷める, 火傷, 卸す, 棚卸し, 司る, 吐く, 哀れ, 哀れむ, 哀しい, 唯一, 唯でさえ, 善い and 善く. Also inspected the public KANJIDIC-derived reading blocks for 丁, 呂, 哲 and 善.
- Retrieved each character's public KanjiVG SVG at the revision declared in its stroke JSON. Compared stroke counts, ordered starts, endpoints and every stored point against densely sampled source curves. All 15 passed; the largest point-to-curve distance was approximately 0.165 on the 109-unit canvas.

Verdicts:

- **Correctness: NEEDS FIX** — 仰's 仰山 example omits a consequential regional qualification, G1. No other substantive linguistic defect established.
- **Scoped coverage: NEEDS FIX** — 仰 needs that qualification, G1. Metadata readings and appropriate source-only/rare qualifications are otherwise covered across all 15 cards.
- **Consistency and quiz safety: NEEDS FIX** — G2 concerns verbatim title quotations only. The actual meaning and reading answer options are CLEAN within the reviewed snapshot.
- **Comprehensibility: CLEAN** — all 15 cards introduce a central idea, explain their mnemonics as modern-shape aids, and provide intelligible examples. Density improvements are optional below.

Per-card verdicts:

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 丁 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 井 | CLEAN | CLEAN | CLEAN | CLEAN |
| 仰 | NEEDS FIX — G1 | NEEDS FIX — G1 | NEEDS FIX — G2 | CLEAN |
| 但 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 傑 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 傷 | CLEAN | CLEAN | CLEAN | CLEAN |
| 僕 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 卸 | CLEAN | CLEAN | CLEAN | CLEAN |
| 司 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 吐 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 呂 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 哀 | CLEAN | CLEAN | CLEAN | CLEAN |
| 哲 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 唯 | CLEAN | CLEAN | CLEAN | CLEAN |
| 善 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |

The scoped changes to 寧 and 敷, all 21 word articles, and all 15 stroke files are CLEAN. The 20 ordinary word diffs contain only the intended first-mention link wrap. 火傷 additionally removes exactly the stated stale paragraph. The two kanji diffs contain only their stated replacements; their linked titles are exact and their surrounding passages remain coherent. No Dictionary line changes occur.

Specific review conclusions:

- Metadata grades, strokes, radical numbers and ordered on/kun lists match the pinned records. Selected quiz readings belong to those lists, and every selected reading has its own linked word example. All new-card titles are unique in the title index; checked links resolve to the intended identities.
- The complete meaning simulation's displayed choices are defensibly wrong in both directions. The flagged shared-component distractors are plausible without becoming synonyms. I found no demonstrated unsafe exclusion or transitive-clique inference. Broad pairs such as 井–額 and 仰–上 concern English-label confusability, not a claim that the Japanese characters are interchangeable. 擦's ordinary “grate” sense supports 卸–擦.
- The reading audits report no production collisions in the shipped N1/All pools and none in the ordinary padded Starter scenarios. I checked the relevant builder logic rather than treating those totals alone as a linguistic verdict.
- The eight latent offered readings are 井ひ, 傷そこなう, 司つ, 司す, 吐ぬかす, 哀かなしむ, 唯ゆ and 善えい. Their attestation or name-only status does not establish that they can occupy a wrong slot in this snapshot's shipped pools. The additional one-holder padded 唯ゆ scenario remains name-only, not an ordinary on/kun reading that must be accepted. I found no established current false-negative quiz answer.
- 丁 correctly distinguishes its source-only/rare readings from the two practiced readings. よほろ is a Daijisen lexical headword, not a missing pinned KANJIDIC2 reading. 呂 correctly distinguishes sound-based 風呂 spelling from a literal “wind + spine” explanation; ロ is usable in the linked examples. 火傷やけど is treated as an irregular whole-word reading, not an independent 傷 reading.
- 唯's イ, rare 唯 spelling of ただ, and name-only ゆ are distinguished appropriately. The remaining source-only readings, alternative okurigana splits and extra dictionary readings are not wrongly promoted into ordinary practiced readings. The official-table claims checked against the supplied pages, including bracketed forms and appendix material, match.

Findings:

1. **G1 — minor; correctness / scoped coverage; `snapshot\kanji\仰.md:59`.**

   **Claim and impact:** The Common words list gives 仰山 ぎょうさん as “a lot; plenty; abundant; great many” and qualifies its spelling as usually kana, but does not qualify that quantity sense as Kansai dialect. A beginner can therefore take this as unmarked standard vocabulary. This matters particularly because the example helps explain the otherwise unfamiliar ギョウ reading.

   **Remedy:** Add “Kansai dialect; usually kana” to this sense. There is no need to remove the example or change the quiz selection.

   **Evidence:** Pinned JMdict entry **1238920**, first sense, explicitly carries **Kansai-ben**. The independently retrieved [live Jisho entry](https://jisho.org/search/%E4%BB%B0%E5%B1%B1), also inspected through its [structured API](https://jisho.org/api/v1/search/words?keyword=%E4%BB%B0%E5%B1%B1), gives the same quantity glosses with “Kansai dialect” and “Usually written using kana alone.” Its separate “exaggerated; grandiose” sense does not carry the Kansai label. The finding is restricted to the quantity sense actually taught here.

   **Confidence:** High.

2. **G2 — minor; consistency; verbatim linked-title quotations in ten new cards.**

   **Claim and impact:** Sixteen quoted linked-card titles omit their internal comma spaces. The words remain understandable, and the actual quiz labels are unaffected, but these are not exact quotations of the linked titles as required by the assignment. The compressed forms also make the contrastive Notes less readable.

   | Location | Printed quotation | Actual linked title |
   |---|---|---|
   | `snapshot\kanji\丁.md:68` | `town,neighborhood` | `town, neighborhood` |
   | `snapshot\kanji\仰.md:58` | `see,look` | `see, look` |
   | `snapshot\kanji\仰.md:58` | `up,above` | `up, above` |
   | `snapshot\kanji\但.md:27` | `sun,day` | `sun, day` |
   | `snapshot\kanji\但.md:47` | `daytime,midday` | `daytime, midday` |
   | `snapshot\kanji\傑.md:27` | `tree,wood` | `tree, wood` |
   | `snapshot\kanji\傑.md:46` | `make,produce` | `make, produce` |
   | `snapshot\kanji\傑.md:47` | `body,form` | `body, form` |
   | `snapshot\kanji\僕.md:50` | `serve,attend` | `serve, attend` |
   | `snapshot\kanji\司.md:55` | `same,equal` | `same, equal` |
   | `snapshot\kanji\司.md:56` | `public,official` | `public, official` |
   | `snapshot\kanji\吐.md:48` | `spirit,air` | `spirit, air` |
   | `snapshot\kanji\吐.md:49` | `company,shrine` | `company, shrine` |
   | `snapshot\kanji\呂.md:52` | `goods,refinement` | `goods, refinement` |
   | `snapshot\kanji\哲.md:55` | `reason,logic` | `reason, logic` |
   | `snapshot\kanji\善.md:58` | `correct,proper` | `correct, proper` |

   **Remedy:** Copy the title strings verbatim, restoring the spaces. No title metadata, exclusion or quiz behavior needs changing.

   **Evidence:** The quoted lines versus the corresponding records in `titles\kanji-titles.tsv`; selected original card headers were also checked directly. This comparison ignores normal sentence punctuation surrounding a quotation and flags only missing internal spaces.

   **Confidence:** High.

Optional:

- For phone use, move or visually subordinate the long sense inventories and repeated explanations of metadata versus practiced readings. The practical reading examples are useful, but cards such as 丁, 仰 and 善 require substantial scrolling through reference detail. This is a presentation improvement, not a demand to discard rare-reading coverage.
- `snapshot\kanji\卸.md:25`: “the act of selling goods wholesale to retail shops” would express the Daijisen definition of おろし more clearly than “a wholesale dealer selling goods to retail shops.” The present wording can be read as an event description, so I have not treated it as an established actor-versus-activity mistranslation.

Limits:

- The exact deployed GPT model identifier is unavailable; I cannot truthfully supply a version number or independently certify model-family separation.
- This was a blind review. I did not seek another reviewer's report, the author's batch rationale, another packet or an external local checkout.
- All tool calls were serial, one per assistant response, with results received before proceeding. No parallel calls, agents, other sessions, background jobs, recursive directory listings or corpus-article scans were used.
- Initial oversized combined local reads and one oversized web result were tool-truncated. I did not open the tool-generated overflow files. Relevant material was subsequently retrieved in bounded form; files not fully reviewed remain explicitly marked partial above.
- The public kanjiapi endpoint returned HTTP 403. Live Kanjipedia and Weblio dictionary entries supplied independent substitutes. Failed or irrelevant public lookups were not counted as verification; Jisho entries subsequently resolved the consequential word checks.
- Pinned metadata was not silently replaced with differing online KANJIDIC-derived lists. A source-only reading is not, by itself, evidence of a common learner spelling or a valid ordinary quiz answer.
- I inspected the supplied full audits and relevant app code, but did not independently rebuild whole-corpus quiz pools. The zero-hit statements above are scoped to the supplied snapshot scenarios, not every hypothetical future pool.
- Stroke geometry was checked against the declared public KanjiVG sources, not exercised in a rendered phone drawing interaction. No device-layout or native-speaker certification is claimed.
