Snapshot: `453af714d56aa573204d477ff863cb4da756b4c3` — batch 110. Independent blind reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`.

Scope:

Reviewed all 15 kanji cards, all 15 stroke files, and all 93 word-article diffs. Facets **3, consistency and quiz safety**, and **4, comprehensibility**, received the deepest examination. No other reviewer's report or author rationale was sought or consulted.

The following inventory distinguishes complete review from targeted or mechanical reading. Packet-relative paths below refer to `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714`; supplement-relative paths refer to `C:\Users\stop-\n1-kanji-workspace\review-packets\supplement-110`.

Define the explicit character set **K** as:

```text
張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖
```

Define the explicit word set **W**, containing all 93 reviewed articles, as:

```text
一応 上級 主張 仮名 仮名遣い 仮定 伝統 価値 価格 出張
初級 刺激 受話器 器具 器用 圧縮 基 基づく 基地 基本
基準 基盤 基礎 大統領 好き嫌い 威張る 嫌 嫌い 嫌う 嫌がる
学級 定価 容器 平仮名 引っ張る 張り切る 応じる 応ずる 応対 応接
応援 応用 急激 恐縮 感激 拡張 振り仮名 整う 整備 整数
整理 暖かい 暖まる 暖める 暖房 楽器 機嫌 欲張り 武器 水素
温暖 激しい 激励 激増 片仮名 物価 物騒 系統 級 素
素人 素直 素質 統一 統計 緊張 縮む 縮める 縮れる 縮小
要素 評価 調整 送り仮名 酸素 食器 騒々しい 騒がしい 騒ぎ 騒ぐ 騒音 高価 高級
```

**Packet files opened:**

- `INSTRUCTIONS.md`: full.
- `mechanical-checks.md`: full supplied file, not the omitted beginnings of the underlying automatic logs.
- `rubric\copilot-instructions.md`: full, through overlapping range reads.
- `repo\docs\content-format.md`: part, lines 1–255, including the kanji, quiz, curated-reading and word-article contracts.
- `repo\docs\confusable-words.md`: part, opening sections through approximately line 157.
- `evidence\source-metadata.json`: full, read in ranges and parsed.
- `evidence\provenance.json`: part, lines 1–160.
- `evidence\kanjidic2-records.xml`: part: introductory lines 1–65; targeted metadata for every character in K; reading/meaning fields for all 116 distinct IDs referenced as distractors or exclusions.
- `evidence\jmdict-families.xml`: part: introductory lines 1–95, plus complete spelling, reading, restriction, sense, register and gloss fields for every entry cited by the 15 cards' Metadata paragraphs. Unrelated entries were not linguistically audited.
- `evidence\jmdict-digest.tsv`: part: lines 1–35 and the first ten listed family rows for each character in K.
- `titles\kanji-titles.tsv` and `titles\word-titles.tsv`: parsed in full for identity, title uniqueness and link checks; linguistic reading was limited to relevant and comparison rows.
- Every `snapshot\kanji\<K>.md`: full.
- Every `snapshot\strokes\<K>.json`: full structural/data review; 張 was also displayed as text.
- Every `diffs\words__<W>.md.diff`: full.
- Every `snapshot\words\<W>.md`: partial prose review, from front matter through the complete `How the kanji combine` section, including preceding examples. Complete files were also loaded for targeted mechanical diff/link checks; this was not a full audit of their later baseline sections.
- `repo\kanji\怪.md`, `repo\kanji\料.md`, `repo\kanji\募.md`, `repo\kanji\校.md`: full.
- The following exact context files under `repo\kanji\`, each with extension `.md`: **part, front matter only**:

```text
充 兼 勘 化 吸 品 喜 坂 型 奇 好 宿 庁 広 弧 弱 扱 掃 撃 政 敗
敬 暗 期 板 欧 段 毒 滴 漱 紙 組 給 練 績 西 談 責 返 長 駐 験
```

**Supplement files opened:**

- `README.md`: full.
- `quiz-safety-full.txt`: full.
- `joyo\p18.txt`, `joyo\p20.txt`, `joyo\p33.txt`, `joyo\p99.txt`: full.
- The following Joyo extracts: part, the indicated target passages: `joyo\p32.txt` lines 43–48; `p36.txt` 26–41; `p45.txt` 39–49; `p47.txt` 37–49; `p76.txt` 14–29; `p91.txt` 46–51; `p96.txt` 42–51; `p106.txt` 36–51; `p109.txt` 46–50; `p118.txt` 47–51.

**Independent public evidence inspected:**

Actual Digital Daijisen entries delivered by Weblio, including their readings, senses and qualifications, not search snippets. URLs follow `https://www.weblio.jp/content/<term>`. Terms were every character in K, plus `怪 料 募 校 劇 許`, and these 44 word terms:

```text
張る 見張り 張り紙 縄張り 威張る 引っ張る 張り切る 器用 素直 素人
応える 反応 順応 応じる 仮名 仮病 虚仮 仮住まい 仮寝 仮借
基づく 価格 激する 嫌疑 機嫌 縮まる 縮らす 縮緬 恐縮 騒々しい
潮騒 統べる 級長 整える 整う 暖気 暖簾
嫌気 騒人 基因 元より しなのき 怪しむ 怪しい
```

Also inspected actual Jisho kanji entries for [応](https://jisho.org/search/%E5%BF%9C%20%23kanji), [価](https://jisho.org/search/%E4%BE%A1%20%23kanji) and [騒](https://jisho.org/search/%E9%A8%92%20%23kanji), including their additional source readings.

For every character in K, fetched the exact public KanjiVG SVG at revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`, under `https://raw.githubusercontent.com/KanjiVG/kanjivg/<revision>/kanji/<five-digit-lowercase-Unicode-codepoint>.svg`. Compared stroke order, count, types, endpoints and stored points against those paths. No public downloads were saved locally.

Verdicts:

Correctness: **NEEDS FIX** — the 価格 explanation, obsolete 応援 availability statement, and two false semantic-overlap claims.

Scoped coverage: **CLEAN** — every metadata reading has a row or explicit qualification; no consequential common-usage omission was established.

Consistency and quiz safety: **NEEDS FIX** — missing direct exclusions and unjustified exclusions; additionally **UNVERIFIED** for the actual fallback reading alternatives absent from the supplied simulation.

Comprehensibility: **NEEDS FIX** — the misleading 価格 explanation and the especially dense 基/素 reference paragraphs.

| Kanji card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 張 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 器 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 素 | CLEAN | CLEAN | NEEDS FIX (3) | NEEDS FIX (5) |
| 応 | NEEDS FIX (4) | CLEAN | NEEDS FIX (4) | CLEAN |
| 仮 | CLEAN | CLEAN | CLEAN | CLEAN |
| 基 | CLEAN | CLEAN | UNVERIFIED | NEEDS FIX (5) |
| 価 | NEEDS FIX (1) | CLEAN | UNVERIFIED | NEEDS FIX (1) |
| 激 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 嫌 | CLEAN | CLEAN | NEEDS FIX (3) | CLEAN |
| 縮 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 騒 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 統 | CLEAN | CLEAN | CLEAN | CLEAN |
| 級 | NEEDS FIX (4) | CLEAN | NEEDS FIX (4) | CLEAN |
| 整 | CLEAN | CLEAN | CLEAN | CLEAN |
| 暖 | CLEAN | CLEAN | UNVERIFIED | CLEAN |

Numbers refer to findings below. The affected cards can also retain an unresolved reading-fallback limitation; NEEDS FIX does not imply that every other quiz claim was verified.

For modified word articles, `snapshot\words\応援.md` needs a correctness/consistency fix (2). No additional introduced defect was established in the other 92 diffs and their reviewed surrounding passages. All 93 diffs satisfy the stated mechanical change boundary: 94 replaced lines, link-wraps only apart from the declared sentence removals in 整備 and 物騒. Added kanji links identify the intended cards. The 17 unchanged Dictionary-line lint warnings are not findings.

All 15 metadata sets match the pinned grade, stroke count, radical number and on/kun lists. Selected quiz readings belong to those lists and have linked examples. Titles are unique; checked links, tags and new-card section order are consistent. The modern-shape mnemonics are explicitly distinguished from etymology.

All 15 stroke files passed the bounded structural and public-source comparison. Maximum observed endpoint discrepancy was about 0.071 viewBox units; maximum stored-point distance to the densely sampled source curves was about 0.174 units in the 109-unit viewBox. This is data corroboration, not a phone-animation test.

The complete simulation's **45 displayed curated meaning distractors** are defensibly wrong; no ambiguity was established among those options after checking both directions and ordinary secondary senses. All 80 exclusion declarations were considered as direct edges, not transitive cliques. For readings, the nine rows reporting 3/3 curated slots have safe available curated reading candidates against the targets' full metadata. These include all reading prompts for 仮, 統 and 整. The other 23 reading rows require unspecified fallback alternatives.

Findings:

1. **Minor — correctness; comprehensibility.** `snapshot\kanji\価.md:35`.

   **Claim and impact:** “In 価格, 格 supplies カク, so 価 is か in both syllables of かかく” incorrectly attributes both occurrences of か to 価. The word is 価 カ + 格 カク; only the initial か comes from 価. This contradicts the preceding clause and misteaches character-to-reading alignment.

   **Remedy:** Replace the clause with a direct breakdown, for example: “価格 is 価 カ + 格 カク: かかく.”

   **Evidence:** Pinned JMdict entry 1189500; the actual [Daijisen 価格 entry](https://www.weblio.jp/content/価格), reading かかく; the supplied Joyo 価 passage; and the correct decomposition already present in `snapshot\words\価格.md:25`.

   **Confidence:** High.

2. **Minor — correctness; consistency.** `snapshot\words\応援.md:30–33`.

   **Claim and impact:** The section now links 応 to its new card but still says that “neither currently has a kanji card here.” 応 does have a card in this snapshot. This is a batch-caused contradiction in the exact surrounding passage the link-wrap review must preserve, although the stale sentence itself was not edited.

   **Remedy:** Remove the obsolete clause, or state specifically that only 援 lacks a card.

   **Evidence:** The new link at line 30, the contradictory statement at lines 32–33, `snapshot\kanji\応.md`, and the kanji title index.

   **Confidence:** High.

3. **Minor — consistency and quiz safety.** `snapshot\kanji\嫌.md:3,14,52`; `snapshot\kanji\素.md:14,44,51`.

   **Claim and impact:** Two direct semantic pairs remain unprotected:

   - **嫌 / 怪:** 嫌 is explicitly titled “dislike; suspicion”; 怪 is titled “suspicious; uncanny” and teaches ordinary suspicion, not only supernatural strangeness. Both directions therefore need protection at the broad English-label level. Excluding 嫌/疑 does not exclude 嫌/怪.
   - **素 / 料:** The ordinary 素 もと ingredient/material sense makes 料's displayed “materials, fee” answer defensible for 素. The reverse direction is weaker: “unadorned” is not an ordinary meaning of 料. That does not remove the forward ambiguity. Existing 素/材 and 素/具 exclusions do not protect 素/料.

   These pairs remain eligible under the documented direct-pair rules when a filtered or larger quiz needs fallback choices. **They are not ambiguous options actually shown in the supplied four-choice simulation**; severity is limited accordingly.

   **Remedy:** Declare the direct 嫌/怪 and 素/料 exclusions once each, on either member of each pair. Do not rely on transitivity or distort the titles.

   **Evidence:** `repo\kanji\怪.md:3,20–21,32–33`; `repo\kanji\料.md:3,20,37`; neither context card supplies the missing reverse declaration. JMdict 1260670 supplies the 素 material/ingredient sense. Independently inspected [嫌](https://www.weblio.jp/content/嫌), [怪しむ](https://www.weblio.jp/content/怪しむ), [怪しい](https://www.weblio.jp/content/怪しい), [素](https://www.weblio.jp/content/素) and [料](https://www.weblio.jp/content/料) entries confirm these ordinary senses. `repo\docs\content-format.md` specifies symmetric, nontransitive protection in custom and fallback pools.

   **Confidence:** High for the semantic gaps and missing edges; actual runtime selection was not reproduced.

4. **Minor — correctness; consistency and quiz safety.** `snapshot\kanji\応.md:14,54`; `snapshot\kanji\級.md:14,47`.

   **Claim and impact:** Two exclusions are justified as semantic overlaps when the displayed labels describe different things:

   - **応 / 募:** “respond; comply” is not “recruit; solicit.” Responding to recruitment in 応募 does not make recruiting a meaning of 応. In the reverse direction, 募 is seeking applicants, not responding or complying.
   - **級 / 校:** “grade; school class” is not “school.” A class/grade belongs to a school, but neither label is an interchangeable answer for the other character. 校's proofreading and officer senses do not establish that equivalence either.

   The Notes promote shared situations or compounds into false character-level synonym claims, and the exclusions unnecessarily suppress valid quiz contrasts.

   **Remedy:** Remove 募 from 応's exclusions and 校 from 級's exclusions. Retain them as useful contrasts if desired, but describe the distinctions rather than asserting overlapping meanings.

   **Evidence:** Actual [Daijisen 募](https://www.weblio.jp/content/募), [応](https://www.weblio.jp/content/応) and [校](https://www.weblio.jp/content/校) entries; the pinned JMdict 応じる and 学級 families. `repo\kanji\募.md:42` already explicitly distinguishes the recruiting side from the responding applicant. `repo\kanji\校.md:3` supplies the actual “school” title.

   **Confidence:** High.

5. **Minor — comprehensibility.** `snapshot\kanji\基.md:23,35`; `snapshot\kanji\素.md:23,35`.

   **Claim and impact:** These two cards most clearly breach the beginner-phone “no wall of text” requirement. After long introductory word catalogues and reading tables, single paragraphs of approximately **264 words for 基** and **244 words for 素** mix pronunciation breakdowns, spelling restrictions, official-table comparisons, rare readings, practice-selection administration and additional dictionary senses. The problem is the unsegmented switching between learner explanation and source audit, not the legitimacy of preserving rare readings. Important contrasts are difficult to locate or revisit on a small screen.

   **Remedy:** Separate the practical reading explanation from compact spelling/rare-reading reference notes, using short paragraphs or small labelled groups. Avoid repeating the complete Common words inventory in the opening. Preserve every sourced reading and its qualification; do not solve the density by silently deleting coverage.

   **Evidence:** The cited paragraphs themselves; approximate counts exclude Markdown link destinations. For example, 基:35 moves from seven word breakdowns through counters, chemistry, four spelling restrictions, quiz policy and 基督. 素:35 similarly combines mixed readings, 素人, もと, source policy, 素より and the separate noun 素 そ.

   **Confidence:** High that the material is densely unsegmented; medium for the degree of individual learner difficulty. This is an audience/structure defect, not a measured phone-usability result.

Optional:

The other cards could benefit from the same reduction of repeated word inventories and administrative boilerplate, without expanding vocabulary coverage. For a more literal visual cue, `snapshot\kanji\激.md:25` could describe 白 above 方 with 攵 alongside, rather than suggesting that the whole 放 sits below 白; the pinned KanjiVG grouping shows the distributed components. This is mnemonic precision, not an asserted etymological defect.

Limits:

- The supplement's “complete” quiz simulation is complete as supplied, but **does not name the reading alternatives or fallback card IDs**. It reports only curated-slot counts. Exact fallback alternatives for 23 of the 32 reading prompts therefore remain UNVERIFIED. Checking the full target metadata and all named distractor headers does not establish which other cards the app would actually choose.
- No APK, quiz implementation or running phone UI was available within the permitted evidence set. I did not reconstruct unidentified fallback options, claim an observed runtime ambiguity for finding 3, or infer older-client compatibility. Meaning-exclusion conclusions use the supplied format contract.
- Public dictionary checks independently covered every card's reading claims and selected consequential word readings, senses and register. Other ordinary examples were checked against the pinned complete cited JMdict families, not independently re-looked-up word by word. Source-only readings were checked as sourced metadata, not certified as common modern vocabulary.
- Joyo claims were compared with the supplied text extracts; the original PDF pages were not independently visually inspected. Public KanjiVG comparisons did not include rendered animation or physical handwriting testing.
- The 93 word articles were reviewed for their actual changes, complete changed sections and preceding examples, not for every pre-existing claim in their later sections. No Japanese example sentences occur in the new kanji cards themselves. Sentence judgments in the reviewed word passages are editorial, not native-speaker or learner testing.
- CLEAN means no actionable defect established in that bounded review, not exhaustive linguistic or runtime certification. Ambiguities were resolved using the current snapshot titles, ordinary modern senses and the documented exclusion-aware client behavior; no questions were asked.
