## Snapshot: a3f5bd39d72e1dfc5361a8d2c213ef0f7cb79cc5 — committed content only

Parent: `f0c4257b1097bb0cde57718096f0a1ecbb0e0d14`, matching the frozen receipt. Snapshot attribution and cleanliness rely on that receipt: **I have file/web tools, not Git execution**, and cannot independently inspect commit objects or recompute its hashes.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Read all twenty new articles completely, all twenty assigned mappings and principal dictionary families, the twelve-file related patch, and the changed passages in their current context. Also inspected the required instructions, format documentation, component evidence, relevant comparison-card titles/exclusions, selected complete comparison records, and supplemental public dictionary/teaching pages.

This was an independent, read-only review without delegation or edits. Unchanged teaching in related articles was contextual evidence, not comprehensively re-reviewed. The prohibited reports, ledgers, private inputs, and other reviewers’ outputs were not consulted.

## Verdicts

**Four localized quiz-exclusion issues need correction.** No separate defect was established in the articles’ explanatory prose, source mappings, written-kanji arrays, or the three required N2 reciprocal links.

“Correctness” below includes quiz labels and exclusions; coverage and comprehensibility assess the declared practical lesson. CLEAN does not mean exhaustive correctness or native-speaker certification.

| Source row; selected senses | Article and reading | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:302; 1–2 | `words\学科.md` — がっか | CLEAN | CLEAN | CLEAN |
| N2:303; 1 | `words\学会.md` — がっかい | NEEDS FIX | CLEAN | CLEAN |
| N2:304; 1 | `words\楽器.md` — がっき | CLEAN | CLEAN | CLEAN |
| N2:305; 1 | `words\学級.md` — がっきゅう | NEEDS FIX | CLEAN | CLEAN |
| N2:306; 1–4 | `words\担ぐ.md` — かつぐ | CLEAN | CLEAN | CLEAN |
| N2:307; 1 | `words\括弧.md` — かっこ | CLEAN | CLEAN | CLEAN |
| N2:308; 1–2 | `words\活字.md` — かつじ | CLEAN | CLEAN | CLEAN |
| N2:309; 1 | `words\活躍.md` — かつやく | NEEDS FIX | CLEAN | CLEAN |
| N2:310; 1 | `words\活力.md` — かつりょく | CLEAN | CLEAN | CLEAN |
| N2:311; 1 | `words\仮定.md` — かてい | CLEAN | CLEAN | CLEAN |
| N2:312; 1 | `words\過程.md` — かてい | CLEAN | CLEAN | CLEAN |
| N2:313; 1 | `words\課程.md` — かてい | CLEAN | CLEAN | CLEAN |
| N2:314; 1 | `words\仮名.md` — かな | CLEAN | CLEAN | CLEAN |
| N2:315; 1 | `words\仮名遣い.md` — かなづかい | CLEAN | CLEAN | CLEAN |
| N2:316; 1 | `words\鐘.md` — かね | CLEAN | CLEAN | CLEAN |
| N2:317; 1 | `words\加熱.md` — かねつ | CLEAN | CLEAN | CLEAN |
| N2:318; 1–3 | `words\兼ねる.md` — かねる | CLEAN | CLEAN | CLEAN |
| N2:319; 1–4 | `words\カバー.md` — カバー | CLEAN | CLEAN | CLEAN |
| N2:320; 1 | `words\過半数.md` — かはんすう | CLEAN | CLEAN | CLEAN |
| N2:321; 1–7 | `words\被せる.md` — かぶせる | NEEDS FIX | CLEAN | CLEAN |

**All twenty mappings: correctness CLEAN / scoped coverage CLEAN / comprehensibility CLEAN.** Each supplied spelling and reading is explicitly taught with its applicable selected meaning. In particular, 学級 appropriately qualifies the raw “grade” gloss as a class group. 仮名 appropriately resolves the conflicting alias gloss using the supplied かな reading and entry `1590540`, while distinguishing alias entry `1577090`. Usually-kana, kana-only, rare-spelling, obsolete-sense, and separate-reading qualifications are respected in the reviewed teaching; supplementary meanings are not independently assigned N2.

**Related changes, changed passages only:**

| File | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\担.md` | CLEAN | CLEAN | CLEAN |
| `kanji\課.md` | CLEAN | CLEAN | CLEAN |
| `kanji\被.md` | CLEAN | CLEAN | CLEAN |
| `words\学部.md` | CLEAN | CLEAN | CLEAN |
| `words\クラス.md` | CLEAN | CLEAN | CLEAN |
| `words\ベル.md` | CLEAN | CLEAN | CLEAN |
| `words\片仮名.md` | CLEAN | CLEAN | CLEAN |
| `words\送り仮名.md` | CLEAN | CLEAN | CLEAN |
| `words\漢字.md` | CLEAN | CLEAN | CLEAN |
| `words\ピアノ.md` | CLEAN | CLEAN | CLEAN |
| `words\バイオリン.md` | CLEAN | CLEAN | CLEAN |
| `words\被る.md` | CLEAN | CLEAN | CLEAN |

The reciprocal examples use the actual readings **担ぐ／かつぐ**, **課程／かてい**, and **被せる／かぶせる**. The 課程 citation identifies the matching entry. Navigation targets teach the linked uses, and the added 被る comparison clearly demonstrates the headwear viewpoint contrast. The supplied diff preserves existing identities, titles, readings, and easier levels.

## Findings

**B16-GPT-01 — Minor · correctness: missing 被せる／浴びせる quiz guard.**  
`words\被せる.md:9,34`; comparison `words\浴びせる.md:4,8,15–18`.

被せる explicitly teaches pouring something over an object, but does not exclude 浴びせる, whose displayed title is **“pour over; shower someone with.”** That title can correctly describe an ordinary taught sense of 被せる, producing a defensible alternative answer. Neither card declares the direct pair; their shared exclusions involving 注ぐ or 掛ける do not establish it.

**Minimal remedy:** add `浴びせる` to 被せる’s exclusions. **Evidence:** frozen JMdict entry `1484320`, sense 3, at `docs\n2-vocabulary-batch-sources\batch-16.json:1625–1646`; independently retrieved [Seisenban 被せる](https://kotobank.jp/word/%E8%A2%AB%E3%81%9B%E3%82%8B-465839), sense ②, and [Daijisen 浴びせる](https://kotobank.jp/word/%E6%B5%B4%E3%81%B3%E3%81%9B%E3%82%8B-426412), sense 1. **Confidence: high.**

**B16-GPT-02 — Minor · correctness: missing 学会／大会 quiz guard.**  
`words\学会.md:9,16–19`; comparison `words\大会.md:4,15–22`.

学会’s event sense overlaps 大会’s convention/conference sense. 大会’s displayed **“tournament; convention”** therefore supplies a defensible “convention” answer for an academic 学会. This is an attested event-sense overlap, not merely a shared research topic. There is no direct exclusion on either card; excluding 会議 does not protect this pair.

**Minimal remedy:** add `大会` to 学会’s exclusions. **Evidence:** frozen JMdict `1206610`, sense 1, explicitly includes academic meeting/conference; the independently retrieved [Jisho/JMdict 大会 entry](https://jisho.org/api/v1/search/words?keyword=%E5%A4%A7%E4%BC%9A) gives たいかい with “convention” and “conference” in its first sense. **Confidence: high.**

**B16-GPT-03 — Minor · correctness: 学級／授業 remains ambiguous through the English label.**  
`words\学級.md:9,16,29–33`; comparison `words\授業.md:5,15–18`.

The prose correctly distinguishes the student group from the teaching session. The quiz does not show that explanation, however: 授業’s title **“class, lesson”** retains unqualified English “class,” which also names a 学級. A learner can reasonably accept both that label and “school class group.” Neither card declares this pair.

**Minimal remedy:** add `授業` to 学級’s exclusions, preserving the useful distinction in the body. **Evidence:** the actual titles and explanations; frozen principal entry `1206680`, sense 1, and complete comparison entry `1330290` at `docs\n2-vocabulary-batch-sources\batch-16.json:7732–7786`. This is an English-label ambiguity, **not** a claim that the Japanese nouns are interchangeable. **Confidence: high.**

**B16-GPT-04 — Minor · correctness: missing 活躍／参加 quiz guard.**  
`words\活躍.md:9,16–19`; comparison `words\参加.md:4,15–20,37`.

活躍’s ordinary selected sense includes **active participation**, while 参加’s displayed answer is simply **“participation.”** That broader answer remains defensible for 活躍 despite the explanatory distinction between merely participating and making a prominent contribution. Neither card declares a direct exclusion.

**Minimal remedy:** add `参加` to 活躍’s exclusions; retain the distinction rather than broadening the definition of 活躍. **Evidence:** frozen entry `1208450`, sense 1, explicitly lists “active participation” at `docs\n2-vocabulary-batch-sources\batch-16.json:1172–1194`, without an obsolete or specialist restriction; the actual 参加 title is unqualified. **Confidence: medium-high.**

These guards would apply symmetrically, including when the affected words are other choices in an unrelated question; they do not assert unrestricted synonymy.

## Optional

None.

## Limits

Commit identity, cleanliness, and hashes were not independently Git-verified. The review evaluates the supplied frozen-file state, with no knowingly included uncommitted changes.

Comparison investigation was targeted, not an exhaustive reading of all 146 comparison families or a whole-repository quiz-pair audit. Quiz consequences were assessed from the documented title/exclusion behavior, not by running the app. Original example naturalness was assessed editorially, not corpus-attested sentence by sentence.

Both cited Agency for Cultural Affairs pages returned mojibake through the available fetcher, so their exact official wording was not independently re-inspected. The author’s decoded inspection receipts were treated as assertions, not fresh reviewer retrieval. Supplemental live dictionary/teaching lookups are not the pinned dictionary snapshot; heading-only or irrelevant results were not counted as lexical verification.
