## Snapshot

Authenticated detached HEAD: **`6614e06e602f1cec6b894052812178b57c8890cb`**. Both required authentication reads succeeded serially in this new attempt. The canceled attempt was not treated as authentication.

Reviewer: **GPT-6.1 Sol**, model ID **`gpt-6.1-sol`**. Independent initial, read-only textual review; no edits or delegation.

## Scope

Read the complete common packet using the required single `view` call with `forceReadLargeFiles=true`. The returned material included all six affected articles, 54 complete comparison/legacy articles, the exact teaching diff, 134 distinct complete JMdict families, 18 raw character records, the Digital Daijisen extraction and receipt, KanjiVG/stroke material, and supplied format/source-policy context. **No returned truncation or known omitted ranges.**

Dictionary evidence was supplied frozen material, not independently retrieved upstream. The public dictionary evidence was specifically the coordinator-extracted first Digital Daijisen wrapper; other aggregator dictionaries were not adopted. Packet hashes were supplied provenance, not independently recomputed.

## Verdicts

**Overall: NEEDS FIX**, principally for two missing direct word-quiz exclusions. Two narrower, pre-existing reading-explanation gaps also remain in reused articles.

| Complete affected article | Correctness | Scoped coverage | Phone-text comprehensibility |
|---|---|---|---|
| `kanji\勘.md` | CLEAN | CLEAN | CLEAN |
| `words\勘.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\勘定.md` | NEEDS FIX | CLEAN | CLEAN |
| `words\勘違い.md` | CLEAN | CLEAN | CLEAN |
| `kanji\定.md` | CLEAN | NEEDS FIX | NEEDS FIX |
| `kanji\違.md` | CLEAN | NEEDS FIX | NEEDS FIX |

CLEAN means no established actionable defect within this scope, not exhaustive correctness.

The new 勘 article correctly separates intuition from examining/reckoning, identifies the mnemonic as modern shape rather than history, and matches the supplied 11-stroke/radical-19 record. Its sole sourced on reading カン has an appropriate own linked example. Supplementary かんがえる is supported by Digital Daijisen; JMdict 1281020 marks **the spelling 勘える**, not that pronunciation, “rarely used kanji form.” Linking the existing 考える identity is appropriate.

The reused word explanations, constructions and translations are coherent. 勘定’s カン＋ジョウ and 勘違い’s on＋native allocation are correct. Both new Common words bullets accurately teach those allocations. The mixed-reading `kango` classification follows the supplied repository convention without asserting two on readings.

All **five reciprocal pairs/ten directions** are present and coherent: 勘↔勘, 勘↔勘定, 勘↔勘違い, 定↔勘定, and 違↔勘違い. Existing word levels, primary readings and exclusions are preserved by the supplied diff. Different legacy KANJIDIC JLPT values do not disprove the separately sourced community levels.

## Findings

1. **Moderate; quiz correctness; `words\勘.md:2–9,15` and comparison `words\感覚.md:2–9,16`.**  
   勘 and 感覚 have no direct exclusion. 感覚’s displayed **“sense; sensation”** includes a defensible intuitive “sense” answer for 勘, while the displayed **“intuition; hunch”** is expressly supported for 感覚. This creates a semantic alternative despite different titles and tags.  
   **Minimal remedy:** declare the direct 勘/感覚 word exclusion on either card.  
   **Exact evidence:** JMdict **1210590, sense 1**: “perception; intuition; the sixth sense”; **1212330, sense 1**: “sense; sensation; feeling; intuition,” without a rare/register restriction. Neither current exclusion list names the other.  
   **Confidence: high.** This establishes an authored ambiguity risk, not an observed production question.

2. **Moderate; quiz correctness; `words\勘定.md:9,16,29` and comparison `words\支払う.md:2–9,15`.**  
   勘定 excludes 計算 and is directly excluded by 会計, but has no direct exclusion with 支払う. **“Pay”** is defensible for the payment use of 勘定する; a noun/suru-verb versus inflecting-verb distinction does not make the context-free English choice safe. The article itself recognizes the payment overlap.  
   **Minimal remedy:** declare the direct 勘定/支払う exclusion on either card. Do not rely on the 会計 exclusion transitively.  
   **Exact evidence:** JMdict **1210750, sense 2**, noun/suru-verb/transitive: “payment (of a bill); settlement (of an account)” alongside bill/check/account; **1310300, sense 1**, transitive godan: “to pay.” The 支 ateji note does not restrict that payment meaning.  
   **Confidence: high.** Actual candidate selection remains untested.

3. **Minor, pre-existing; coverage/comprehensibility; `kanji\定.md:9–10,26–33`.**  
   Raw さだ.か is preserved in metadata but receives neither a reading row nor a qualified explanation. Unlike 勘’s explicit quiz selection, this legacy card has no curated subset; preservation alone does not explain the reading a learner may encounter.  
   **Minimal remedy:** retain the metadata and provide a narrowly scoped, dictionary-verified explanation/example for さだ.か. No bulk curation or exhaustive compound expansion is necessary.  
   **Exact evidence:** the frozen KANJIDIC2 **定** record lists テイ, ジョウ, さだ.める, さだ.まる and **さだ.か**; the table explains only the first four. The supplied format requires explanations for raw kun readings.  
   **Confidence: high** for the omission. A specific replacement example was not verified from the supplied JMdict families.

4. **Minor, pre-existing; coverage/comprehensibility; `kanji\違.md:9–10,28–33,46`.**  
   The selective-table notice acknowledges omitted readings but does not explain **ちが.える, -ちが.える, たが.う or たが.える**. The preserved on reading イ is at least explicitly identified; the four omitted native forms have no comparable treatment. Legacy full-list behavior makes this more than a demand for exhaustive vocabulary.  
   **Minimal remedy:** retain the raw list and add concise, verified examples or appropriately qualified source-only explanations for those four forms, distinguishing the bound form from the independent verb.  
   **Exact evidence:** the frozen KANJIDIC2 **違** record contains all four forms. JMdict **2109290** independently establishes 違う **たがう**, including senses “to differ” and “to run counter to,” but the article supplies no explanation of that reading.  
   **Confidence: high** for the omissions; exact allocations/examples for the other omitted forms remain unverified.

## Optional

None. The selected 勘 vocabulary need not teach every frozen family, search-only spelling, historical sense or name reading.

## Limits

No other reviewer report, author adjudication, credentials or control history was accessed. No alternative authentication path, branch ref or shell command was used.

The supplied comparisons support 勘’s curated 勤/助/期 contrasts; no ordinary secondary sense established those displayed labels as equivalent to intuition/examining/reckoning. Existing direct exclusions were assessed symmetrically and nontransitively, not as semantic compartments or a universal guarantee.

This review does **not** verify actual N1/All/custom/reduced-pool options, either production word-quiz direction, client exclusion/curation enforcement, four-font rendering, native selection, reading/drawing/article/Back/offline behavior, handwriting recognition or physical-phone acceptance. Phone-text verdicts concern the explanations alone.