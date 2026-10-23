## Snapshot: c3e705025de8ed252789968a9a37ab0535ddf3a3 — committed content only, as designated by the frozen receipt

Parent: `9ceeb5366693090d9abd54de08d75970da59dda0`.

**Four actionable quiz-ambiguity findings affect five new articles.** No other actionable defect was established in the assigned prose, source mappings, kanji metadata/backlinks, or fifteen related edits. Snapshot identity and cleanliness remain receipt-based; independent Git verification was unavailable.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`

Read all nineteen new articles listed below completely, the actual fifteen-file related patch and changed passages in context, and the existing `偉い` teaching supporting the reuse claim. Reviewed all twenty explicit mappings, N2:142–N2:161.

Read the required repository instructions and `docs\content-format.md:18–119`, plus the permitted source/provenance evidence. Checked relevant dictionary spelling/reading restrictions, sense qualifications, inflections, component readings, comparison cards, displayed answer labels and direct quiz exclusions. Independently retrieved the nine dictionary/borrowing headwords associated with the supplied inspection receipts, plus additional evidence for the findings.

This was read-only: no edits or delegation. Unchanged teaching on existing cards was inspected only as needed for the assigned changes, comparisons and quiz candidates—not comprehensively reviewed. No prohibited authoring/review documents, private inputs or other reviewer output were consulted.

## Verdicts:

**CLEAN** means no actionable defect established within the assigned scope, not exhaustive correctness or native-speaker certification. The **NEEDS FIX** cells below concern quiz answer ambiguity; the corresponding source-row teaching remains covered.

All article paths in the first table are under `words\`.

| Source row | New article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:143 | 宴会.md | CLEAN | CLEAN | CLEAN |
| N2:144 | 園芸.md | CLEAN | CLEAN | CLEAN |
| N2:145 | 演劇.md | CLEAN | CLEAN | CLEAN |
| N2:146 | 円周.md | CLEAN | CLEAN | CLEAN |
| N2:147 | 遠足.md | CLEAN | CLEAN | CLEAN |
| N2:148 | 延長.md | NEEDS FIX | CLEAN | CLEAN |
| N2:149 | 煙突.md | CLEAN | CLEAN | CLEAN |
| N2:150 | 追い掛ける.md | CLEAN | CLEAN | CLEAN |
| N2:151 | 追い越す.md | CLEAN | CLEAN | CLEAN |
| N2:152 | オイル.md | CLEAN | CLEAN | CLEAN |
| N2:153 | 応援.md | CLEAN | CLEAN | CLEAN |
| N2:154 | 王女.md | CLEAN | CLEAN | CLEAN |
| N2:155 | 応ずる.md | NEEDS FIX | CLEAN | CLEAN |
| N2:156 | 応接.md | NEEDS FIX | CLEAN | CLEAN |
| N2:157 | 応対.md | NEEDS FIX | CLEAN | CLEAN |
| N2:158 | 往復.md | NEEDS FIX | CLEAN | CLEAN |
| N2:159 | 欧米.md | CLEAN | CLEAN | CLEAN |
| N2:160 | 応用.md | CLEAN | CLEAN | CLEAN |
| N2:161 | オーケストラ.md | CLEAN | CLEAN | CLEAN |

Each file in the following groups receives the stated verdict independently, limited to its changed passage and necessary context.

| Related edits | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\芸.md`, `劇.md`, `周.md`, `延.md`, `接.md`, `復.md`, `欧.md`: reciprocal word examples and links | CLEAN | CLEAN | CLEAN |
| `words\パーティー.md`, `芝居.md`, `女王.md`, `追う.md`, `延期.md`, `西洋.md`: comparison links | CLEAN | CLEAN | CLEAN |
| `words\応じる.md`: related-form note and shared inflections | CLEAN | CLEAN | CLEAN |
| `words\偉い.md`: N2 metadata only | CLEAN | CLEAN | CLEAN |

**Explicit mappings and reuse:** All twenty mappings are CLEAN for correctness, scoped coverage and comprehensibility. N2:142 maps to existing `words\偉い.md`, which already teaches admiration and high status at **えらい**; the supplied diff adds only `jlpt: 2`. Its anomalous source glosses do not justify assigning every usually-kana or dialect-qualified dictionary sense to this article.

The source spelling **追い掛ける** and explicitly taught **追いかける** are both covered, rather than inferred merely from matching pronunciation or entry identity. **応ずる** and **応じる** remain distinct dictionary forms; the taught 応じます／応じて／応じた／応じない forms are correct. Existing easier-level metadata in the related cards is preserved.

Written headword kanji are represented in metadata, existing applicable kanji cards receive substantive links, and the seven relevant N2 cards have useful reciprocal examples at the article readings. No invented constituent reading or missing required backlink was established.

## Findings:

### GPT-B08-01 — Minor · Correctness: missing 延長–続き quiz exclusion

**Location:** `words\延長.md:4–9,52–54`; comparison `words\続き.md:4–9,15`.

延長 expressly recognizes its **continuation** use, while 続き displays **“continuation; rest of a story or task.”** Neither card directly excludes the other. A question presenting bare 延長 can therefore offer an English answer that is valid for an acknowledged secondary sense but belongs to the distractor card.

**Evidence:** JMdict entry **1176510, sense 3**, records “extension (e.g. of one's work), continuation,” without a restrictive qualifier (`docs\n2-vocabulary-batch-sources\batch-08.json:923–939`). Independently retrieved [Daijisen 続き, sense 1](https://kotobank.jp/word/続き-571885), defines it using **あるものの延長**. This is lexical overlap, not merely a shared topic.

**Minimal remedy:** Add `続き` directly to 延長’s `quiz_exclusions`. No prose expansion is necessary.

**Confidence:** High.

### GPT-B08-02 — Minor · Correctness: missing 応ずる–受ける quiz exclusion

**Location:** `words\応ずる.md:4–9,16–17`; comparison `words\受ける.md:2–9,15–16`.

The displayed **“respond; comply; accept”** prompt can admit 受ける through its ordinary accepting/answering uses. The existing card’s narrower displayed title, **“receive; undergo,”** does not eliminate those uses when 受ける appears as a Japanese answer choice.

**Evidence:** JMdict **1329590, sense 5**, includes accepting a challenge (`docs\n2-vocabulary-batch-sources\batch-08.json:6986–7002`). Independently retrieved [Seisenban 受ける](https://kotobank.jp/word/受ける-439397), section [1][一]③–④, covers acceptance/assent and responding to a question, command or telephone call. This does **not** depend on its separate Go-specific response sense.

There is no direct exclusion. The existing 応ずる–承る–受ける exclusion chain is insufficient because exclusions are non-transitive.

**Minimal remedy:** Add `受ける` directly to 応ずる’s `quiz_exclusions`.

**Confidence:** High.

### GPT-B08-03 — Minor · Correctness: missing direct guards against 扱う on 応接 and 応対

**Location:** `words\応接.md:4–9,16–18`; `words\応対.md:4–9,16–18`; comparison `words\扱う.md:4–9,15`.

Both new cards can encounter 扱う’s **“handle; deal with; treat”** answer label despite genuine overlap in attending to or dealing with people. Their mutual exclusion does not protect either card against 扱う.

**Evidence:** JMdict **1179930:1** includes “dealing with” for 応接; **1179980:1** explicitly includes dealing with people/customers and handling for 応対 (`docs\n2-vocabulary-batch-sources\batch-08.json:1520–1525` for the latter). Independently retrieved [Seisenban 扱う, sense ②](https://kotobank.jp/word/扱う-425433), describes talking to or entertaining someone and explicitly gives **応対、待遇する**. The existing 扱う article also teaches treating a person, not just operating machinery.

This does not assert unrestricted substitution between the Japanese constructions. It establishes an overlapping answer label for an uncontextualized word quiz.

**Minimal remedy:** Add `扱う` directly to **both** new cards’ `quiz_exclusions`.

**Confidence:** High.

### GPT-B08-04 — Minor · Correctness: missing 往復–便り quiz exclusion

**Location:** `words\往復.md:2–9,43–45`; comparison `words\便り.md:4–9,16`.

往復 correctly acknowledges exchanging letters, but has no quiz exclusions. 便り displays **“news; correspondence”** and excludes only ニュース and 手紙. Thus its English label can supply a valid secondary translation for bare 往復 while being treated as a wrong answer.

**Evidence:** JMdict **1179760, sense 3**, gives “correspondence, exchanging (of letters)” without a restrictive qualifier (`docs\n2-vocabulary-batch-sources\batch-08.json:1308–1317`). Independently retrieved [Daijisen 往復, sense 2](https://kotobank.jp/word/往復-449276), covers exchanging letters; the actual [Wiktionary 便り noun entry](https://en.wiktionary.org/wiki/便り) gives “news from, correspondence.”

The distinction between a communication and reciprocal exchange remains useful teaching, but does not disambiguate the displayed English **correspondence** label.

**Minimal remedy:** Add `便り` directly to 往復’s `quiz_exclusions`.

**Confidence:** High.

## Optional:

None. No nonblocking expansion or stylistic change is necessary to resolve these findings.

## Limits:

- **File tools, not Git execution:** I could not independently verify HEAD, worktree cleanliness, the supplied diff against its parent, or the receipt’s hashes. The reviewed content’s frozen-commit identity rests on the supplied receipt.
- The selected JMdict/KANJIDIC2 records are evidence for the inspected combinations, not the whole dictionaries; omission was not treated as proof of absence. Original dictionary downloads and hashes were not independently reproduced.
- The nine embedded inspection receipts were treated as author assertions, not independent reviewer retrieval. I separately inspected their cited headword pages, using only definitions actually rendered; some Kotobank pages exposed Seisenban text but not Daijisen definitions.
- An initial 便り lookup failed and a Jisho fetch exposed no lexical results; neither was used as evidence. The successful 便り retrieval cited above supplied the relevant noun entry.
- Quiz findings are static assessments under the supplied symmetric, pairwise, non-transitive behavior contract; the app was not executed. No exhaustive dictionary, corpus-frequency or native-speaker certification is claimed.
- The N2 assignments are pinned **community-list** mappings, not an official modern JLPT syllabus or independent N2 classification of every secondary sense.
