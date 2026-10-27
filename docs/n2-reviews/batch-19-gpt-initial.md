## Snapshot: `42a8e121fad9901d0738f130164809fb926bc46c` — committed files only

The frozen marker reports `cleanWorktree: true`, 51 scoped files, and baseline `ccc1f7dd951e07be4dbb3f5fb80463ad9ca6c89f`. **I have file tools, not Git execution:** committed-file identity, cleanliness and the exact diff were not independently Git-verified.

## Scope:

**Actual model:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. Independent, read-only review; no delegation or edits.

Read all 19 assigned new pages completely. Compared all 15 kanji metadata records and 40 reading rows—34 lexical examples and six qualified source-only rows—with the supplied evidence. Inspected all 45 distractor assignments, useful word links, relevant vocabulary answer labels and direct exclusions, and the 13 older two-distractor cards for newly introduced direct-synonym fallback risks.

Inspected the related passages in `words\腕.md`, `words\腰.md`, `words\心臓.md`, `words\大臣.md`, `words\航空.md`, `words\一般.md`, `words\芸術.md`, `words\荷物.md`, `words\お菓子.md`, `words\菓子.md`, `words\著者.md` and `words\野菜.md`. This was **not** a comprehensive review of their unchanged teaching material.

Read the required instructions and format reference, both permitted source records, and relevant comparison pages. Did **not** read `docs\n2-authoring-notes.md`, `docs\n2-review.md`, `REVIEW.md`, `docs\n2-reviews\`, session authoring inputs, author-check receipts or another reviewer’s output. Nanori, obsolete JLPT assignments and exhaustive review of the 15 generated stroke files were omitted as assigned.

## Verdicts:

Quiz-answer ambiguity is classified below as a **correctness** defect. CLEAN means no established actionable defect within this scope, not exhaustive truth or native-speaker certification.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\脳.md` | CLEAN | CLEAN | CLEAN |
| `kanji\腕.md` | CLEAN | CLEAN | CLEAN |
| `kanji\腰.md` | CLEAN | CLEAN | CLEAN |
| `kanji\膚.md` | CLEAN | CLEAN | CLEAN |
| `kanji\臓.md` | CLEAN | CLEAN | CLEAN |
| `kanji\臣.md` | CLEAN | CLEAN | CLEAN |
| `kanji\舟.md` | NEEDS FIX | CLEAN | CLEAN |
| `kanji\航.md` | CLEAN | CLEAN | CLEAN |
| `kanji\般.md` | CLEAN | CLEAN | CLEAN |
| `kanji\芸.md` | CLEAN | CLEAN | CLEAN |
| `kanji\荒.md` | CLEAN | CLEAN | CLEAN |
| `kanji\荷.md` | CLEAN | CLEAN | CLEAN |
| `kanji\菓.md` | CLEAN | CLEAN | CLEAN |
| `kanji\菜.md` | CLEAN | CLEAN | CLEAN |
| `kanji\著.md` | CLEAN | CLEAN | CLEAN |
| `words\脳.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\皮膚.md` | CLEAN | CLEAN | CLEAN |
| `words\舟.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\荒れる.md` | NEEDS FIX | CLEAN | CLEAN |

All requested reading lists, primary stroke counts, canonical radicals and grade tags match the supplied records. No additional actionable defect was established in the twelve related passages or the older two-choice fallback inspection.

## Findings:

**B19-GPT-01 — Medium; correctness; `words\脳.md:4–8` — Missing direct exclusion with 気.**  
The new answer label **“brain; mind”** can supply a defensible *mind* answer for existing 気, despite 気’s displayed label being “spirit; mood.” 気 explicitly has that noun sense; this is not the unrelated English verb *mind*. Neither card excludes the other. 脳’s exclusion with 精神 and 精神’s exclusion with 気 do not protect 脳/気 transitively.

**Minimal remedy:** Add `気` to 脳’s `quiz_exclusions`.

**Exact evidence:** `words\気.md:3–5,16,35`; `words\精神.md:9`; pinned JMdict entry **1470380**, sense 2, in `docs\n2-batch-sources\batch-19.json:1042–1110`; fetched [Jisho/JMdict 気](https://jisho.org/api/v1/search/words?keyword=%E6%B0%97), actual headword **気・き**, noun sense 1 “spirit; mind; heart.” The pairwise, nontransitive contract is in `docs\content-format.md:88–105`. **Confidence: high.**

**B19-GPT-02 — Medium; correctness; `kanji\舟.md:11`; `words\舟.md:8,40–50` — 舟’s secondary senses leave unsafe quiz options.**  
The assigned kanji distractor 缶 displays **“tin can; container”**. 舟 has an independently documented container meaning, so *container* is not reliably wrong—not merely because a boat can carry things. The word quiz likewise leaves existing ケース’s **“case; container; instance”** available. Existing 箱’s **“box; case”** overlaps the explicitly documented box uses. Excluding ケース would not automatically exclude 箱.

There is also an unguarded aircraft overlap: the restriction-aware source explicitly permits **“seaplane”** for **舟・ふね**, while existing 飛行機 displays **“airplane.”** That broader label can describe the documented secondary referent. This does not mean 舟 is an ordinary replacement for every airplane.

**Minimal remedy:** Replace 缶 with an existing semantically unrelated kanji distractor; add direct word exclusions for `ケース`, `箱` and `飛行機` on 舟.

**Exact evidence:** `kanji\缶.md:3`; `words\ケース.md:4,9,16`; `words\箱.md:4,15–17`; `words\飛行機.md:4,15`. Pinned JMdict entry **1602800**, complete retained 舟 record at `docs\n2-batch-sources\batch-19.json:2762–2858`: sense 1 includes *seaplane* and expressly applies to 舟; unrestricted sense 2 includes *tank, tub, vat, trough*. Fetched [精選版 日本国語大辞典, ふね【船・舟・槽】](https://kotobank.jp/word/%E8%88%B9-125569), sense ②, defines a box-shaped container and specifically identifies sake-press boxes and shallow fish boxes. Fetched [Jisho/JMdict 飛行機](https://jisho.org/api/v1/search/words?keyword=%E9%A3%9B%E8%A1%8C%E6%A9%9F) confirms **ひこうき**, “airplane; aeroplane; plane; aircraft.” **Confidence: high for the container/box overlaps; medium for the broader airplane-label risk.**

**B19-GPT-03 — Medium; correctness; `words\荒れる.md:4–8,20` — The skin sense needs a direct exclusion with かさかさ.**  
The article correctly teaches skin becoming rough, but existing かさかさ displays **“dry and rough; rustling”** and explicitly teaches rough, moisture-deprived skin. Neither card excludes the other. This is an attested shared skin-condition meaning, not an inference that noisy rustling and stormy weather are synonymous. A context-free meaning quiz can offer two defensible rough-skin answers.

**Minimal remedy:** Add `かさかさ` to 荒れる’s `quiz_exclusions`.

**Exact evidence:** `words\かさかさ.md:4,8,15–17,26`; pinned JMdict entry **1281490**, sense 3, in `docs\n2-batch-sources\batch-19.json:4217–4339`, “to become rough (of skin); to get chapped.” Fetched [精選版 日本国語大辞典, あれる【荒】](https://kotobank.jp/word/%E8%8D%92%E3%82%8C%E3%82%8B-428813), sense ⑤, explicitly explains this use as skin losing smoothness and **かさかさしている**. Fetched [Jisho/JMdict かさかさ](https://jisho.org/api/v1/search/words?keyword=%E3%81%8B%E3%81%95%E3%81%8B%E3%81%95) confirms the applicable “dry and rough” sense and suru-verb use. **Confidence: high.**

## Optional:

None.

## Limits:

The frozen marker and author-provided 51-file scope were accepted; Git status, baseline diff, file hashes and source-download hashes could not be independently checked. Stroke-converter provenance was read, but drawing paths were not reviewed.

The selected dictionary evidence is not the complete dictionary and does not establish usage frequency or native-speaker naturalness certification. Failed or irrelevant public lookups were discarded; the findings above use inspected headwords, readings and applicable senses. The airplane-label judgment is less certain than the direct container and rough-skin overlaps, as identified in B19-GPT-02.
