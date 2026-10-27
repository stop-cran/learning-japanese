**Snapshot:** `a73354e75917d4758b386c870a4284cd70dfacee` — committed-only snapshot requested; the local HEAD reference matches. Independent verification that the working files exactly match that commit was unavailable; see Limits. Baseline: `7a92dde23107173af8aabef51971dbc66b754a93`.

**Scope:** Sole reviewer: **GPT-6.1 Sol (`gpt-6.1-sol`)**. Read all 15 new cards completely: `kanji\並.md`, `丸.md`, `久.md`, `乱.md`, `乳.md`, `乾.md`, `了.md`, `介.md`, `仏.md`, `令.md`, `仲.md`, `伸.md`, `伺.md`, `低.md`, and `依.md`.

Reviewed the changed distractor metadata in `kanji\下.md` and `kanji\長.md`, and the changed “How the kanji combine” links in these 22 word files: `並ぶ`, `並べる`, `丸`, `丸い`, `久しぶり`, `乾く`, `仏`, `仲`, `仲間`, `伸ばす`, `伸びる`, `伺う`, `低い`, `依頼`, `厄介`, `命令`, `完了`, `最低`, `永久`, `混乱`, `牛乳`, and `紹介`—all under `words\`, with `.md` extensions. Inspected actual distractor titles and directly relevant old fallback candidates.

Read the assigned public rules, source snapshot, complete metadata records, and complete selected JMdict records used for the checks. **Not reviewed:** excluded authoring notes, review reports, adjudications, session inputs, unchanged teaching content in existing word pages, unrelated existing defects, or stroke drawing paths. No delegation or repository edits were performed.

**Verdicts:**

One quiz ambiguity needs correction. Two localized usage-qualification omissions need attention; two “Common words” classifications remain unverified.

| Card | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 並 | CLEAN | CLEAN | CLEAN |
| 丸 | CLEAN | UNVERIFIED | CLEAN |
| 久 | CLEAN | CLEAN | CLEAN |
| 乱 | CLEAN | CLEAN | CLEAN |
| 乳 | CLEAN | CLEAN | CLEAN |
| 乾 | CLEAN | NEEDS FIX | CLEAN |
| 了 | CLEAN | CLEAN | CLEAN |
| 介 | CLEAN | CLEAN | CLEAN |
| 仏 | CLEAN | CLEAN | CLEAN |
| 令 | CLEAN | CLEAN | CLEAN |
| 仲 | NEEDS FIX | NEEDS FIX | CLEAN |
| 伸 | CLEAN | CLEAN | CLEAN |
| 伺 | CLEAN | NEEDS FIX | CLEAN |
| 低 | CLEAN | CLEAN | CLEAN |
| 依 | CLEAN | UNVERIFIED | CLEAN |

All supplied reading inventories, radicals/numbers, primary stroke counts, and grade tags match the batch’s KANJIDIC2-derived records. The dictionary-paired reading examples realize their displayed readings with applicable senses; 仏教’s sound change is explicitly explained. The source-only qualifications on 並 and 乱 honestly distinguish recorded character readings from established word examples.

Every new card has useful existing word links and three existing distractor cards. The semantic exception is F01. The assigned backlink passages and the new third choices for 下 and 長 have no established defect within their narrow scope.

**Findings:**

**F01 — Moderate; correctness / scoped coverage — `kanji\仲.md:11`; `kanji\中.md:3`.**  
仲 includes 中 as a wrong option, whose displayed answer is **“middle, inside.”** However, “middle” is also an established meaning of 仲, not merely an inference from its shape. A learner recognizing that meaning can select a defensible answer and be marked wrong. Consequently, this card does not have three reliably wrong choices.

**Minimal remedy:** Replace 中 with an inspected existing card whose title does not describe 仲. Retain the useful 中 comparison in the mnemonic.

**Exact evidence:** [Kanjipedia’s 仲 entry](https://www.kanjipedia.jp/kanji/0004728900), meaning ③, gives “なか。四季それぞれのまんなか,” with 仲秋 and 仲春 as examples. Its other meanings also explicitly concern being between people. This is contemporary dictionary meaning evidence, not an etymological argument.  
**Confidence:** High.

**F02 — Minor; scoped coverage — `kanji\乾.md:34–35`.**  
The rows present **乾す ほす** and **乾る ひる** without explaining their orthographic status or showing the corresponding 干 spellings. The pairs are recognized and should remain; the omission is guidance about using and recognizing these alternatives, not an incorrect reading. The card otherwise carefully separates everyday drying verbs from specialized readings, making these two unqualified rows an inconsistent gap.

**Minimal remedy:** Retain both readings and examples, adding that these are readings outside the Jōyō reading list and that the words are also written **干す／干る**. Do not describe them as invalid or infer a numerical frequency from that status.

**Exact evidence:** Batch records `docs\n2-batch-sources\batch-01.json:1913–2035` establish the pairs and applicable senses. [Kanjipedia’s 乾 entry](https://www.kanjipedia.jp/kanji/0001056200) marks ほす and ひ as outside-list readings; its [legend, 音・訓](https://www.kanjipedia.jp/include/popup_kanji.html) defines that marking. Digital Daijisen heads the words as [干す／▽乾す](https://kotobank.jp/word/干す-630091) and [干る／▽乾る](https://kotobank.jp/word/干る-614125). These sources establish status and alternative spellings, not usage frequency.  
**Confidence:** High on the status and omission; medium on the pedagogical impact.

**F03 — Minor; scoped coverage — `kanji\伺.md:30`.**  
**“伺候 しこう — attendance upon someone”** leaves the example’s specifically high-status service/calling-on setting unexplained. The surrounding explanation correctly teaches 伺う’s humility, but does not identify this シ example as specialized vocabulary. A learner can mistake the row for a neutral expression for attending on any person.

**Minimal remedy:** Qualify the example as specialized/formal attendance or service upon a high-ranking person, rather than replacing or deleting the reading.

**Exact evidence:** The batch’s complete JMdict record at `docs\n2-batch-sources\batch-01.json:3166–3190` supports しこう and “waiting upon (someone).” [精選版日本国語大辞典, 伺候](https://kotobank.jp/word/伺候-512100), senses ①–②, specifies serving close to a 貴人 and presenting oneself before that person. The finding concerns missing contextual qualification; it does not establish a frequency threshold or claim that the word is obsolete.  
**Confidence:** High on the contextual restriction; medium on severity.

**F04 — Minor, unresolved evidence gap; scoped coverage — `kanji\丸.md:33–37`; `kanji\依.md:34–38`.**  
**丸薬** and standalone **依怙** appear under **“Common words.”** Their spellings, readings, and glosses are supported, but I could not substantiate the asserted commonness of these particular vocabulary items in present-day general usage. This is **not an established finding that either word is rare, incorrect, or unusable**.

**Minimal remedy:** Supply usage evidence supporting the classification, or qualify/move these items to an “Other reading examples” grouping while retaining their reading-table examples.

**Exact evidence:** Complete batch records at `docs\n2-batch-sources\batch-01.json:993–1015` and `3585–3611` establish lexical recognition, not frequency; the source snapshot explicitly states that limitation. [精選版日本国語大辞典’s 丸薬 entry](https://kotobank.jp/word/丸薬-471637) describes a spherical medicinal preparation; the accompanying encyclopedia discusses that dosage form’s limited current use, which is **not itself proof of word frequency**. [Kanjipedia’s 依怙 entry](https://www.kanjipedia.jp/kotoba/0000131600) confirms the favoritism sense but supplies no frequency assessment. Empty priority lists were not treated as proof of rarity.  
**Confidence:** High that the pairs and senses are valid; insufficient evidence to resolve commonness.

**Optional:** At `kanji\久.md:29`, brief Buddhist-context guidance for 久遠 could help learners prioritize the ク example; [精選版日本国語大辞典](https://kotobank.jp/word/久遠-476617) labels that entry 仏語. This is not evidence that broader literary uses are incorrect. At `kanji\依.md:32`, “uncommon kanji spelling; usually kana” would distinguish spelling from pronunciation more precisely than “rare spelling/reading”; the note at line 43 already largely resolves this ambiguity.

**Limits:** The available tools allowed file inspection but not `git status`, `git show`, or a baseline diff. The matching HEAD reference therefore does not independently establish byte-for-byte frozen-content provenance or exclude unnoticed working-tree changes; the findings apply to the local passages read under the supplied clean-snapshot assumption.

Commonness remains unresolved only as identified in F04. Illustrative sentence naturalness was assessed linguistically, not certified through a corpus or native-speaker review. The selected dictionary records were inspected completely, but upstream downloads, hashes, and transforms were not independently reproduced. **Stroke JSON’s pinned-converter provenance was noted; no full drawing-path audit was performed.** CLEAN means no established actionable defect in the assigned scope, not exhaustive truth or native-speaker certification.

