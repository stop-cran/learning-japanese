**Snapshot:** `9030d709018268d80be335165f0ff70c1de60d2e`, as identified by the supplied task; committed teaching only, no uncommitted changes included. Git identity and worktree cleanliness were not independently checked.

**Scope:** Independent initial review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage, and textual phone comprehensibility.
- Read both complete teaching files: `kanji\鳩.md` and `words\鳩.md`.
- Read all specified instruction and policy ranges, both complete metadata files—including raw 鳩 and 究 character elements—and the complete provenance snapshot.
- Read all **70 complete dictionary families**: 57 in `batch-027-jmdict.xml`, lines 1–1082, and 13 in `batch-027-comparisons-jmdict.xml`, lines 1–436. Every XML request used an explicit range of at most 200 lines; no returned range was truncated.
- Read complete comparison cards `kanji\九.md`, `kanji\丸.md`, `kanji\究.md`, and all seven assigned comparison word articles: 鳥, 動物, 鶴, 鷹, 集める, 公園, 見る. These were inspected for the bounded comparisons, not reopened for unrelated teaching review.
- Independently fetched and inspected the relevant Kotobank dictionary bodies for 鳩, 鳩舎, and 鳩首.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\鳩.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\鳩.md` | **CLEAN** | **CLEAN** | **CLEAN** |

CLEAN means no actionable defect established within this bounded review.

The kanji metadata preserves all four Japanese readings in source order: キュウ, ク, はと, あつ.める. The sole selected reading, はと, has its own row and a useful reciprocal word link. Recognition-only キュウ is supported by 鳩舎; ク and あつ.める are explicitly source-only **in this lesson**, without claiming lexical nonexistence. The Buddhist 鳩槃荼 family does not undermine that bounded disposition or justify allocating character readings from kana substrings.

JMdict entries 1478330 and 1442040 support the ordinary pigeon/dove noun, independent katakana spelling ハト, and complete compound reading でんしょばと. Both example sentences, their kana transcriptions, and English translations are sound; singular English translations are compatible with the explicitly number-neutral Japanese noun.

The independently inspected 精選版日本国語大辞典 鳩 sense 1 supports the family-level bird meaning. Digital Daijisen supports modern きゅうしゃ and 鳩首’s gathering/conference meaning. Neither historical キウ notation nor the qualified expression-origin note is incorrectly promoted into modern pronunciation or established etymology.

The modern-shape mnemonic is clearly separated from historical classification. The actual distractor titles—“nine,” “round; circle,” and “investigate thoroughly”—are semantically distinct from “pigeon; dove,” including the inspected secondary meanings. The two direct word exclusions, 鳩/鳥 and 鳩/動物, appropriately guard broader-category ambiguity. 鶴 and 鷹 remain different bird names, not synonymous alternatives; no transitive exclusion assumption is needed. The support word receives no inferred N1 vocabulary level.

**Findings:** None.

**Optional:** None.

**Limits:** The confusable-word inventory was inspected only through a scoped search for 鳩, 鳥, 動物, 鶴, and 鷹; it returned no matches. Frozen KANJIDIC2/JMdict packets and recorded hashes were supplied evidence, not fresh upstream downloads or independently recomputed hashes. The three Kotobank entry bodies were independently retrieved; empty dictionary headings supplied no evidence.

Comprehensibility assessment was textual, not physical-phone or fresh native-rendering certification. The supplied 28-Han/unchanged-three-font coverage remains inherited evidence only. Fresh batch-027 Android, combined-main, CI, public-ZIP, and physical-phone/general-release checks remain outstanding; this review neither certifies them nor establishes a bounded-owner-testing publication veto.

All visible tool calls were issued singly and awaited; no internal overlap was observed. No broader process evidence was inspected. No files were changed, and no other reviewer reports or author rationale were read.
