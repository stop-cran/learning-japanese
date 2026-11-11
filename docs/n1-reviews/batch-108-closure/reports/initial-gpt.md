## Snapshot

**Authenticated:** `9955ac122d1b4f1084f702d3d6d5afeb82d35e3a`.

Two separate serial `view` calls returned:
1. `.git`: the pointer to `auditor-compatibility-isolated\.git\worktrees\batch-108-review-9955ac`.
2. That Git directory’s `HEAD`: exactly the requested hash.

**Reviewer:** GPT-6.1 Sol, model ID `gpt-6.1-sol`; independent initial textual review. No successor-ref comparison or cryptographic signature verification performed.

## Scope

Read **all 19 common packet parts completely, in order**, using one serial `view` call per response with `forceReadLargeFiles=true`. No truncation, recovery reads, rereads, shell, edits, delegation, other review reports, author adjudication, session history, or qualification reports. No lock access.

Reviewed the four complete affected articles, their metadata and exact teaching diff, every supplied complete comparison/legacy-context article, all **64 complete frozen JMdict entries**, all **14 distinct complete raw character records**, public-dictionary extracts and retrieval receipts, source metadata, SVG, stroke JSON, and applicable public rules.

**Provenance:** article text was returned through the common packet, with original authoring filenames, line numbers and supplied SHA-256 labels. Its byte identity with the detached snapshot is supplied packet provenance, not an independently recomputed hash result. Public dictionary evidence was coordinator-retrieved extracted text—not a fresh upstream lookup by this reviewer.

## Verdicts

**Overall: CLEAN within the supplied textual scope.** No actionable defect or consequential unresolved textual claim established.

| Article | Correctness | Scoped coverage | Phone-TEXT comprehensibility |
|---|---|---|---|
| `kanji\勧.md` | CLEAN | CLEAN | CLEAN |
| `words\勧告.md` | CLEAN | CLEAN | CLEAN |
| `words\勧める.md` | CLEAN | CLEAN | CLEAN |
| `kanji\告.md` | CLEAN | CLEAN | CLEAN |

**勧:** The title and taught meanings match the supplied character record and word senses. Thirteen strokes, radical 力/no. 19, grade and full reading order agree with the frozen metadata. The SVG supports right-hand 力 and the 隹-like lower-left comparison. The mnemonic explicitly avoids historical derivation. カン and すす.める have their own linked examples and justified allocations; ケン remains source-only without an unsupported rarity or invalidity claim.

**勧告:** JMdict **1210970, sense 1** supports the exact spelling/reading, noun and transitive する classification, and advice/recommendation/remonstrance meanings. The supplied Daijisen extract supports action-directed advice and **辞職を勧告する**. Both complete examples, kana, translations and polarity are coherent. Recipient に and action-noun を are correctly distinguished. Institutional usage is illustrated without making it exclusive or asserting universal legal force. The component explanation is a meaning aid, not invented etymology.

**勧める:** JMdict **1595680** supports all three taught senses. Senses **1 and 3** restrict spelling to 勧める/奨める; sense **2** permits 薦める and particularly associates that spelling with recommendation. The article preserves those boundaries. The doctor/exercise and guest/tea examples are natural, with correct roles and translations. Ichidan forms and すす＋める allocation are correct. 進める remains a separate lexical identity despite identical pronunciation. Existing N3 metadata is preserved.

**告:** Seven strokes, radical 口/no. 30, コク and つ.げる agree with the raw record. The complete unchanged explanation, examples and shape comparisons remain coherent with reuse. The new Common words bullet correctly gives 勧告／かんこく and assigns コク to 告. Existing N3 classification is preserved; the packet policy distinguishes current community levels from historical KANJIDIC JLPT values.

### Quiz labels and guards

The three curated 勧 distractors—**観 “view; observe,” 確 “certain,” 権 “authority; rights”**—remain defensibly distinct in both target/label directions after considering their supplied secondary meanings, not merely their different strings. Their visual comparisons are accurate. 告’s existing 古/否/牛 distractors likewise establish no semantic collision with “announce; inform.”

All four direct kanji guards are justified: **勧–励, 勧–供, 勧–勉, 勧–支** address encouragement, offering, or supportive overlap, including meanings omitted from short titles.

The six **勧告** word guards—勧める, 推薦, 提案, 注意, 警告, 呼び掛ける—and the two added **勧める** guards—推薦, 提案—appropriately protect recommendation/advice/suggestion and relevant secondary senses. Incoming supplied guards from 励ます, 激励 and 呼び掛ける also protect 勧める’s encouragement/urging overlap. These judgments apply to both word orientations; POS differences alone would not resolve ambiguity.

The supplied older fallback/comparison context establishes no additional necessary direct exclusion. In particular, consultation versus giving advice, opinion versus recommending action, invitation versus recommendation, and recruiting versus recommending are not automatically equivalent answer labels. Specialized “offer” combinations likewise do not alone establish overlap. Exclusions were assessed as **direct, symmetric and nontransitive**, not as semantic cliques.

### Reciprocal mappings

All three required pairs have both directions, correct relative destinations, and coherent readings/component introductions:

| Pair | Kanji → word | Word → kanji |
|---|---|---|
| 勧 / 勧める | `kanji\勧.md:23,33,39` | `words\勧める.md:25` |
| 勧 / 勧告 | `kanji\勧.md:23,31,40` | `words\勧告.md:24` |
| 告 / 勧告 | `kanji\告.md:37` | `words\勧告.md:24` |

No incidental-mention backlinks are required.

## Findings

**None established.** No consequential unresolved claim or tentative hypothesis is promoted to a defect.

## Optional

None.

## Limits

CLEAN means **bounded no-actionable-defect**, not exhaustive correctness or universal semantic safety for uncurated choices.

This review does not verify signature validity, fresh upstream dictionary contents, runtime generation, native-font rendering, actual production All/N1/custom/reduced/guarded-older/short-pool options, either live word orientation, drawing recognition, Back/offline behavior, or physical-phone acceptance. Those remain separate gates; the comprehensibility verdicts concern supplied **text only**.
