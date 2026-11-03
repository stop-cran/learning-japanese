**Snapshot:** `43428b813d563650223eeb4675c445a614aaa4b6`, as identified by the task; no uncommitted teaching included. Read-only review; no files changed.

**Scope:** GPT-6.1 Sol (`gpt-6.1-sol`). Reviewed both complete teaching files, `kanji\鮎.md` and `words\鮎.md`, for correctness, scoped coverage, and textual comprehensibility. Read all prescribed instruction/format ranges, complete input metadata including the raw KANJIDIC2 element, and all **28 complete dictionary families**: 14 in each frozen JMdict packet. All 731 XML lines returned in explicit ranges of at most 200 lines, without truncation.

Read all five complete comparison kanji articles—占, 店, 点, 魚, 鯉—and all five complete comparison word articles—魚, 鯉, 川, 焼く, 食べる. Inspected applicable confusable-word inventory matches through a scoped search. Independently fetched and inspected the actual Kotobank Seisenban and Jitsu entry bodies.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鮎.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\鮎.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review, not exhaustive certification or physical-phone acceptance.

**Findings:** None.

The inspected evidence supports the following review conclusions:

- The sourced reading order—デン, ネン; あゆ, なまず—is preserved exactly. Only あゆ is selected, with its own row and a reciprocal, dictionary-supported word link. The other readings receive explicit dispositions; 瓢鮎図 is correctly treated as a painting title rather than ordinary animal vocabulary.
- JMdict entry 1586720 supports 鮎／あゆ, standalone アユ, “ayu; sweetfish,” and the usually-kana qualification. The teaching does not promote rare or search-only alternative spellings, infer frequency from priorities, or infer constituent readings from unrelated whole fish names.
- Seisenban independently confirms river habitat, food use, and the Chinese catfish distinction. Jitsu confirms デン・ネン and なまず・あゆ. These facts support separating the Japanese ayu noun from the character’s catfish sense. Conflicting historical-origin explanations are appropriately not presented as settled etymology.
- Both Japanese example sentences, kana transcriptions, translations, particle explanations, and 焼いて linkage are sound. 鮎釣り’s two readings and 若鮎’s presented reading/gloss are supported; the omitted obsolete 若鮎 reading is not required for this scope.
- The default kanji choices actually display “divine fortunes; occupy,” “shop,” and “point; dot.” None is an ordinary meaning of 鮎. The broader “fish” label is correctly kept out of that curated set. The word exclusion 鮎／魚 directly guards the corresponding overlap; 鯉 remains a distinct animal, without relying on transitive exclusions.
- The shape comparisons match the actual characters, and the mnemonic is explicitly nonhistorical. The supporting word declares no vocabulary level inferred from its N1 kanji.

**Optional:** None.

**Limits:** Snapshot identity and clean teaching scope were supplied by the task, not independently checked with Git. The JMdict and KANJIDIC2 packets are frozen supplied evidence, not fresh upstream retrieval. Kotobank facts were initially supplied by the coordinator and subsequently independently confirmed through the fetched headings and bodies; image gaiji and historical reconstruction were not verified.

The confusable-word inventory received only the disclosed scoped search. This review does not certify larger quizzes, automatic fallback algorithms, or unrelated comparison-article claims.

Comprehensibility verdicts concern text, not device rendering. The supplied font audit reports 广 and 鯰 absent from all three bundled cmaps; absence does not establish glyph failure, and supported-native disposition remains pending. No fresh Android, physical-phone, combined-main, CI, or public-ZIP acceptance was performed or inferred from inherited evidence.

One tool call was issued per response and its result awaited; no internal call overlap was observed. No shell, delegation, other review reports, or author-rationale records were used.
