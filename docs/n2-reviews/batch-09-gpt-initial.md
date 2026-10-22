## Snapshot: d3166cb43733fa6c45908151ec3633044200d54f; committed files only

Snapshot identity and committed-only status are **as supplied**, not independently Git-verified. The supplied comparison baseline is `cd32544fdfeaa6ea81e107d42bedf0cf58f8f516`.

## Scope: gpt-6.1-sol; family gpt; independent read-only review

Read all 19 assigned teaching pages completely, named in the verdict table below. Reviewed the required instructions, `docs\content-format.md:18-109`, pinned metadata and restriction-aware dictionary evidence, relevant confusable-word comparisons, and supplementary public dictionary entries.

Inspected the substantive component-link passages in these existing articles, with surrounding context: `words\乗り換える.md`, `交換.md`, `尊敬.md`, `拾う.md`, `捨てる.md`, `掃除.md`, `換える.md`, `損.md`, `損害.md`, `改善.md`, `敬意.md`, `旧.md`, `星.md`, `直接.md`, and `衛星.md`. Also checked `kanji\上.md`’s answer label against 下, 中, and newly added 土.

**No assigned teaching page was omitted.** Unchanged material in the link-only articles was not comprehensively reviewed. Stroke drawing paths, generated-manifest integrity, and the Git diff were not audited. Forbidden ledgers, authoring inputs, and other reviewers’ outputs were not read. No delegation, file edits, or repository writes were performed.

## Verdicts:

**Two vocabulary pages need quiz-metadata fixes.** No actionable defect was established in the 15 new kanji pages, the four articles’ teaching explanations, or the narrowly assigned related edits.

All 15 kanji match the pinned readings, primary stroke counts, canonical radicals/numbers, and grade tags. The reading examples realize the indicated readings, including okurigana and bound forms; source-only readings are honestly qualified. All **45 curated new-kanji distractor assignments** are semantically wrong answers for their targets and reference existing cards. Each new kanji has useful linked vocabulary. 上’s three choices introduce no established ambiguity.

Correctness below includes quiz-answer validity; coverage includes necessary direct exclusions. Comprehensibility assesses the teaching explanation separately.

| Page | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\拾.md` | CLEAN | CLEAN | CLEAN |
| `kanji\挟.md` | CLEAN | CLEAN | CLEAN |
| `kanji\捜.md` | CLEAN | CLEAN | CLEAN |
| `kanji\捨.md` | CLEAN | CLEAN | CLEAN |
| `kanji\掃.md` | CLEAN | CLEAN | CLEAN |
| `kanji\掘.md` | CLEAN | CLEAN | CLEAN |
| `kanji\採.md` | CLEAN | CLEAN | CLEAN |
| `kanji\接.md` | CLEAN | CLEAN | CLEAN |
| `kanji\換.md` | CLEAN | CLEAN | CLEAN |
| `kanji\損.md` | CLEAN | CLEAN | CLEAN |
| `kanji\改.md` | CLEAN | CLEAN | CLEAN |
| `kanji\敬.md` | CLEAN | CLEAN | CLEAN |
| `kanji\旧.md` | CLEAN | CLEAN | CLEAN |
| `kanji\昇.md` | CLEAN | CLEAN | CLEAN |
| `kanji\星.md` | CLEAN | CLEAN | CLEAN |
| `words\挟む.md` | NEEDS FIX | NEEDS FIX | CLEAN |
| `words\捜す.md` | CLEAN | CLEAN | CLEAN |
| `words\採掘.md` | CLEAN | CLEAN | CLEAN |
| `words\昇る.md` | NEEDS FIX | NEEDS FIX | CLEAN |

## Findings:

### G09-001 — Medium; correctness / scoped coverage — Missing direct exclusions for 挟む

**Location:** `words\挟む.md:4-8`. Relevant existing labels: `words\掴む.md:4,9`, `words\捕まえる.md:5`, and `words\サンドイッチ.md:4-9`.

The exclusion list covers 握る and 持つ, but leaves three defensible English-answer collisions eligible:

| Unexcluded word | Displayed label | Relevant meaning of 挟む |
|---|---|---|
| 掴む | grasp; seize | Gripping something from both sides |
| 捕まえる | catch; capture | Catching or trapping something, such as a finger in a door |
| サンドイッチ | sandwich | Putting or sandwiching something between two things |

The last pair is an **English noun/verb ambiguity**, not Japanese synonymy. A context-free English prompt “sandwich” can reasonably admit 挟む as the verb as well as サンドイッチ as the food noun. Likewise, “sandwich” is a defensible English option for written 挟む. Different word types and tags influence selection but do not prohibit these pairs.

Excluding 挟む/握る and 掴む/握る does **not** exclude 挟む/掴む.

**Minimal remedy:** Add direct exclusions between 挟む and `掴む`, `捕まえる`, and `サンドイッチ`. This preserves the correct teaching distinctions without distorting any definition.

**Exact evidence:** `docs\n2-batch-sources\batch-09.json:929-1085`, JMdict entry **1600740**, はさむ: sense 1 includes “to grip (from both sides),” sense 2 “to sandwich between,” and sense 3 “to catch (e.g. a finger in a door).” Supplementary fetched entries confirm [掴む・つかむ](https://jisho.org/api/v1/search/words?keyword=%E6%8E%B4%E3%82%80), physical sense including “to grasp” and “to grip,” and [捕まえる・つかまえる](https://jisho.org/api/v1/search/words?keyword=%E6%8D%95%E3%81%BE%E3%81%88%E3%82%8B), including “to catch” and physical grasping. Oxford’s fetched [“sandwich between”](https://www.oxfordlearnersdictionaries.com/definition/english/sandwich-between) verifies the English verb construction. Pairwise exclusion behavior is documented at `docs\content-format.md:79-98`.

**Confidence:** High. These are eligible ambiguous pairs, not a claim that every default quiz will select them.

### G09-002 — Medium; correctness / scoped coverage — 昇る’s broad English label leaves additional ambiguous pairs

**Location:** `words\昇る.md:4-8`. Relevant labels and exclusions: `words\増える.md:5-9`, `words\増す.md:4-9`, `words\伸びる.md:4-9`, `words\起きる.md:5-9`, `words\立つ.md:4-9`, and `words\立ち上がる.md:4-9`.

The displayed label **“rise; ascend”** is correct for 昇る, but “rise” also conventionally means increasing in quantity and getting up or standing up. Consequently, it remains a defensible English answer for these unexcluded words:

- **増える, 増す, 伸びる:** increase or growth senses.
- **起きる, 立つ, 立ち上がる:** getting up or rising to one’s feet.

The existing exclusion for 増加 does not extend to 増える or 増す. Likewise, 立ち上がる’s exclusions for 立つ and 起きる do not establish any exclusion with 昇る. These are answer-label collisions; they do **not** make 昇る an interchangeable Japanese spelling for those meanings. The article correctly explains its narrower Japanese uses, but that explanation does not disambiguate the quiz’s isolated label.

**Minimal remedy:** Qualify the displayed title, for example **“rise (sun/moon); be promoted,”** while preserving the broader natural-rising explanation in the body. Alternatively, retain the current title and add direct exclusions for the six identified words.

**Exact evidence:** `docs\n2-batch-sources\batch-09.json:3649-3716`, JMdict entry **1352570**, restricts 昇る to natural rising and promotion in the selected record. The fetched [のぼる entry](https://jisho.org/api/v1/search/words?keyword=%E6%98%87%E3%82%8B) confirms the complete spelling-restricted sense distinction. Fetched entries for [増える・ふえる](https://jisho.org/api/v1/search/words?keyword=%E5%A2%97%E3%81%88%E3%82%8B), [増す・ます](https://jisho.org/api/v1/search/words?keyword=%E5%A2%97%E3%81%99), and [伸びる・のびる](https://jisho.org/api/v1/search/words?keyword=%E4%BC%B8%E3%81%B3%E3%82%8B) verify their increase senses; 伸びる’s applicable sense is explicitly restricted to that spelling. Oxford’s fetched [“rise” entry](https://www.oxfordlearnersdictionaries.com/definition/english/rise_1) separately defines “increase in amount or number” and getting up from a lying, sitting, or kneeling position, including “stand up” as a synonym. The existing posture articles teach precisely those physical uses.

**Confidence:** High for the missing direct edges and the English meanings establishing ambiguity.

## Optional:

None.

## Limits:

I have **file tools but no Git execution**. I therefore could not independently verify the commit checkout, clean worktree, exact 55-file change set, or baseline diff. Verdicts apply to the files read under the supplied snapshot assertion.

The **15 stroke files were supplied as converter-generated from the pinned repository**; exhaustive drawing-path review was not assigned or performed. Source-download hashes were not independently recomputed.

Quiz collisions were established from the actual titles/exclusions and documented app behavior, not by executing the app or measuring selection frequency. Comparison searches were targeted to relevant meanings, not a comprehensive review of every existing vocabulary article.

Dictionary recognition was not treated as evidence of frequency. Selected-evidence omissions were not treated as dictionary absence. Source-only qualifications were assessed as qualifications, not as proof that no example exists anywhere. Example-sentence naturalness received editorial assessment, not native-speaker certification or exhaustive corpus verification. No consequential linguistic claim remains unresolved within the assigned scope.
