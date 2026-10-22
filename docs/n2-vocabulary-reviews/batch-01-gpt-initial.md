## Snapshot: fe744d204feaeb554fce6df934cfafed81419be5; committed content only

Parent: `94a175cdc06f3c7d1d09cbd8891b2a5ef370b18f`.

The frozen receipt identifies this commit and declares `cleanCommittedContent: true`. **Snapshot identity and cleanliness are receipt-attested, not independently Git-verified:** I have file tools, not Git execution. No files were edited.

## Scope: GPT-6.1 Sol — `gpt-6.1-sol`, family `gpt`

Independent, sequential review without delegation. I read all 17 new articles listed below completely, the required repository guidance, the first 20 mappings (`N2:2–N2:21`), and the complete relevant JMdict entry families and component records in the supplied batch evidence.

I inspected the actual related-file patch and changed passages in context: the 明き alias teaching in `words\空き.md`, the comparison link in `words\預ける.md`, and word links/examples on kanji pages **伸, 跡, 預, 青, 白, 欠, 明, 方, 足, 味**. For unchanged `会う.md` and `赤ん坊.md`, I assessed only the specified reuse claims. Other word/kanji pages were consulted for comparisons, links, and quiz candidates.

I did not read prohibited authoring/review files, private inputs, other reviewers’ outputs, or later source mappings. This is not a comprehensive review of unchanged teaching.

## Verdicts: four quiz defects and two missing navigation links

**CLEAN** means no actionable defect established in the assessed facet and scope—not exhaustive correctness or native-speaker certification.

| New article under `words\` | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| あいかわらず.md | CLEAN | NEEDS FIX — F05 | CLEAN |
| アイデア.md | CLEAN | CLEAN | CLEAN |
| アイディア.md | CLEAN | CLEAN | CLEAN |
| 曖昧.md | NEEDS FIX — F04 | CLEAN | CLEAN |
| 扇ぐ.md | CLEAN | CLEAN | CLEAN |
| 青白い.md | CLEAN | CLEAN | CLEAN |
| あきれる.md | NEEDS FIX — F01 | CLEAN | CLEAN |
| アクセント.md | CLEAN | CLEAN | CLEAN |
| 欠伸.md | CLEAN | CLEAN | CLEAN |
| 飽くまで.md | CLEAN | CLEAN | CLEAN |
| 明け方.md | CLEAN | CLEAN | CLEAN |
| 揚げる.md | CLEAN | CLEAN | CLEAN |
| 挙げる.md | NEEDS FIX — F02 | NEEDS FIX — F05 | CLEAN |
| 憧れる.md | CLEAN | CLEAN | CLEAN |
| 足跡.md | CLEAN | CLEAN | CLEAN |
| 味わう.md | NEEDS FIX — F03 | CLEAN | CLEAN |
| 預かる.md | CLEAN | CLEAN | CLEAN |

No source-mapping defect was established across the 20 assigned rows. Explicit alias teaching supports reuse; matching kana or entry IDs alone was not treated as sufficient. The articles appropriately qualify problematic source glosses, including “flap” for 扇ぐ and “fly” for 挙げる.

| Related passage or unchanged reuse claim | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `空き.md:34–36`: 明き／あき alias and retained N3 | CLEAN | CLEAN | CLEAN |
| `預ける.md:28`: 預かる comparison link | CLEAN | CLEAN | CLEAN |
| Changed links/examples on the ten assigned kanji pages | CLEAN | CLEAN | CLEAN |
| `会う.md:2–5,27,31`: 遭う／あう, undesirable encounters; retained N5 | CLEAN | CLEAN | CLEAN |
| `赤ん坊.md:2–5,15–19`: あかんぼう, baby/infant; retained N4 | CLEAN | CLEAN | CLEAN |

The changed kanji passages supply useful reciprocal examples, including 欠伸／あくび, 足跡／あしあと, and 預かる／あずかる. Whole-word readings are not presented as invented constituent readings. Written-headword kanji metadata is complete.

## Findings:

**F01 — Medium; correctness, quiz ambiguity — `words\あきれる.md:9,16–21`.**  
The exclusions protect 驚く and びっくり but not **うんざり**. The new article explicitly teaches “fed up,” including repeated excuses; `words\うんざり.md:4,8,19` displays “fed up; weary of something,” gives the closely corresponding repeated-explanation example, and has no reciprocal exclusion. Thus a defensible answer can appear as a wrong choice. **Minimal remedy:** add a direct あきれる／うんざり exclusion. **Evidence:** pinned batch entry **1515580, sense 1**, expressly includes “to be exasperated” and “to be fed up” (`batch-01.json:1066–1073`); [Daijisen, うんざり, sense 1](https://kotobank.jp/word/うんざり-442573) confirms becoming thoroughly tired of something. **Confidence: high.**

**F02 — Medium; correctness, quiz ambiguity — `words\挙げる.md:9,16–24,35`.**  
The exclusions cover raising, arresting, and recommending, but omit demonstrated overlaps with **示す, 収める, and 得る**. The article itself compares 例を挙げる with 例を示す and teaches 成果を挙げる, “achieve results.” The other displayed labels are “show; indicate” (`示す.md:4,19–23`), “put away; achieve” (`収める.md:4,16–19`), and “obtain; gain” (`得る.md:4,15,28`). None directly excludes 挙げる. These are applicable ordinary senses, not merely shared topics. **Minimal remedy:** add direct exclusions for these three pairs; 収める’s existing exclusion of 得る does not protect either pair with 挙げる. **Evidence:** pinned entry **2864818, sense 1** includes showing/citing examples (`batch-01.json:1963–1969`), and **sense 11** includes achieving a result and obtaining (`2180–2183`). [Daijisen, 収める, sense 2](https://kotobank.jp/word/収める-452207) independently supports acquiring/achieving, illustrated by 勝利を収める. **Confidence: high.**

**F03 — Minor; correctness, English-label ambiguity — `words\味わう.md:9,16,34–36`.**  
The noun **味** is correctly distinguished in the prose, but its displayed title is the unqualified **“taste, flavor”** (`words\味.md:5`). “Taste” can be read as an English verb and is a valid translation of 味わう. Consequently, the genuine Japanese noun/verb distinction does not ensure a uniquely defensible English answer. Neither card directly excludes the other. **Minimal remedy:** add 味 to 味わう’s exclusions, or explicitly disambiguate the noun’s displayed label. **Evidence:** pinned entry **1527010, sense 1** gives “to taste; to savor” (`batch-01.json:1195–1206`); `味.md:22–24` confirms the noun/verb distinction. This finding concerns the labels, not a claim that the Japanese words are interchangeable. **Confidence: high.**

**F04 — Minor; correctness, secondary-sense quiz ambiguity — `words\曖昧.md:9,37–39`.**  
The article explicitly includes the separate shady/disreputable sense, but its exclusions leave **疑わしい**, titled **“doubtful; questionable,”** eligible (`words\疑わしい.md:4,8,15–16`). That label is defensible for the suspicious/questionable secondary use of 曖昧. Protection through 怪しい or いかがわしい is not transitive. **Minimal remedy:** add a direct 曖昧／疑わしい exclusion; retain the useful distinction between unclear wording and dishonesty. **Evidence:** pinned entry **1567920, sense 2** (`batch-01.json:1498–1514`); [Seisenban Nikkoku, 曖昧, sense ③](https://kotobank.jp/word/曖昧-23877) explicitly defines this use with 怪しげな、疑わしい. This does not assign that secondary sense independently to N2. **Confidence: high for the lexical overlap and missing guard; no frequency claim.**

**F05 — Minor; scoped coverage, existing-card navigation — `words\あいかわらず.md:27–29`; `words\挙げる.md:35`.**  
Two substantive introductions/comparisons leave existing cards unlinked: **相** in the introduced spelling 相変わらず, and **示す** in the explicit 例を示す comparison. `kanji\相.md` and `words\示す.md` both exist. Learners cannot navigate directly to those relevant explanations, contrary to the repository’s existing-card linking rule. **Minimal remedy:** link 相 and 示す at those passages. Keep あいかわらず’s kana-headword metadata as `kanji: []`; no new card, decomposition lesson, or backlink is required. **Evidence:** the passages and existing target cards, together with `.github\instructions\content-structure.instructions.md`’s substantive-introduction/comparison linking requirement. **Confidence: high.**

## Optional: none

## Limits:

I could not execute Git or recompute receipt hashes, so I cannot independently certify the checkout’s correspondence to the frozen commit, cleanliness, or parent diff. The review relies on the supplied receipt and related patch for that boundary.

Dictionary evidence establishes the cited identities, senses, restrictions, and flags—not corpus frequency or native-speaker certification of every example. Failed or irrelevant external lookups were not used as evidence. Quiz assessment applied the supplied symmetric, nontransitive exclusion behavior without running the app; targeted searches and comparison-card inspection do not establish exhaustive whole-corpus quiz-pair completeness.
