## Snapshot: `11d1b0ae8caf19e6aac628e1774a9f21d8ab503e` — committed content only

Parent: `8df57903f716932690acdff28f84b6e285924d94`. This is the frozen commit identified by the supplied receipt; independent Git verification was unavailable.

## Scope

Reviewer: **GPT-6.1 Sol**, model ID **gpt-6.1-sol**, family **gpt**. Review was sequential, read-only and independent, with no delegation or file edits.

I read all eighteen new articles completely, the actual nine-file related patch and changed passages in context. I assessed all twenty assigned source mappings, selected/additional sense qualifications, written-kanji metadata, relevant links, reciprocal N2 examples, English answer titles and quiz exclusions. The two reuse assessments concern exact spelling/reading/sense coverage, not whole-article recertification. Unchanged teaching in related files was not comprehensively reviewed.

## Verdicts

**Three articles need quiz-safety fixes.** No actionable error was established in their Japanese examples or mapped lexical teaching. Here, correctness includes whether the quiz can reject a defensible answer; scoped coverage and comprehensibility assess the practical teaching separately.

| New article | Source row; selected JMdict senses | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `words\各自.md` | N2:262; 1 | CLEAN | CLEAN | CLEAN |
| `words\拡充.md` | N2:263; 1 | CLEAN | CLEAN | CLEAN |
| `words\学術.md` | N2:264; 1 | CLEAN | CLEAN | CLEAN |
| `words\拡張.md` | N2:266; 1 | CLEAN | CLEAN | CLEAN |
| `words\角度.md` | N2:267; 1 | NEEDS FIX | CLEAN | CLEAN |
| `words\学年.md` | N2:268; 1–2 | NEEDS FIX | CLEAN | CLEAN |
| `words\学部.md` | N2:269; 1 | CLEAN | CLEAN | CLEAN |
| `words\格別.md` | N2:270; 1–2 | CLEAN | CLEAN | CLEAN |
| `words\確率.md` | N2:271; 1 | CLEAN | CLEAN | CLEAN |
| `words\学力.md` | N2:272; 1 | CLEAN | CLEAN | CLEAN |
| `words\掛け算.md` | N2:273; 1 | CLEAN | CLEAN | CLEAN |
| `words\可決.md` | N2:274; 1 | CLEAN | CLEAN | CLEAN |
| `words\火口.md` | N2:275; 1–2 | CLEAN | CLEAN | CLEAN |
| `words\下降.md` | N2:276; 1 | NEEDS FIX | CLEAN | CLEAN |
| `words\重なる.md` | N2:277; 1–3 | CLEAN | CLEAN | CLEAN |
| `words\重ねる.md` | N2:278; 1–2 | CLEAN | CLEAN | CLEAN |
| `words\飾り.md` | N2:279; 1 | CLEAN | CLEAN | CLEAN |
| `words\かしこまりました.md` | N2:281; 1 | CLEAN | CLEAN | CLEAN |

**Nine related changes**, assessed only within their stated narrow scope:

| File | Assessed change | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `kanji\各.md` | 各自 reciprocal example at かくじ; citation | CLEAN | CLEAN | CLEAN |
| `kanji\角.md` | 角度 reciprocal example at かくど; citation | CLEAN | CLEAN | CLEAN |
| `kanji\算.md` | 掛け算 reciprocal example; voiced ざん; citation | CLEAN | CLEAN | CLEAN |
| `words\各地.md` | Source-backed N2 field only | CLEAN | CLEAN | CLEAN |
| `words\火山.md` | Source-backed N2 field and existing 火口 comparison link | CLEAN | CLEAN | CLEAN |
| `words\積む.md` | Link to the taught stacking use of 重ねる | CLEAN | CLEAN | CLEAN |
| `words\級.md` | Link to the taught school-year use of 学年 | CLEAN | CLEAN | CLEAN |
| `words\アクセサリー.md` | Link to the decoration noun 飾り | CLEAN | CLEAN | CLEAN |
| `words\能力.md` | Inflected 重ねて link to 重ねる and its repeated-practice use | CLEAN | CLEAN | CLEAN |

**Mappings and reuse claims:** all twenty spelling/reading/applicable-meaning mappings are **CLEAN / CLEAN / CLEAN**, independently of the quiz defects above. The two reused mappings are N2:265 → 各地, JMdict 1205100:1, and N2:280 → 火山, 1193910:1. Their existing teaching supplies the claimed exact coverage. The supplied patch preserves their stable identities, readings and titles and overwrites no existing easier-level field.

The consequential source qualifications are defensible:

- 拡張 selects expansion/extension without promoting the specialist ESC gloss into general teaching.
- 学術, 学部 and 学力 appropriately qualify “science,” “undergraduate” and “scholarship/literary ability.”
- 火口 retains かこう and 1193860:1–2 while distinguishing ひぐち at 1724250:1 and ほくち at 2706740:1. It does not attach “origin of a fire” indiscriminately to かこう.
- The aliases, mixed native/on reading of 掛け算, and usually-kana expression かしこまりました are explicitly explained. Secondary meanings and additional readings do not independently acquire N2 status.

## Findings

**B14-GPT-01 — Moderate; correctness: quiz-answer ambiguity.**  
**Location:** `words\角度.md:4,9,16–19`; `words\立場.md:4,9,16–23`.

角度’s title is “angle; viewpoint,” while 立場’s is “position; standpoint.” Both words have the ordinary figurative viewpoint meaning, but neither article excludes the other. A Japanese-to-English question for 角度 can therefore offer the defensible alternative “position; standpoint”; an English-to-Japanese question containing “viewpoint” can likewise admit 立場.

**Minimal remedy:** add `立場` to 角度’s direct `quiz_exclusions`—one declaration suffices for both directions and candidate-to-candidate protection.

**Evidence:** the independently retrieved [角度 entry](https://kotobank.jp/word/%E8%A7%92%E5%BA%A6-460585), Seisenban definition ②, defines a figurative direction of viewing a matter, 観点. The independently retrieved [Jisho entry for 立場](https://jisho.org/api/v1/search/words?keyword=%E7%AB%8B%E5%A0%B4), at たちば, explicitly gives “viewpoint; standpoint; point of view.” The articles’ contrasting-perspective examples substantiate the overlap. **Confidence: high.**

**B14-GPT-02 — Moderate; correctness: incomplete direct quiz protection.**  
**Location:** `words\下降.md:4,9,16`; `words\下りる.md:4,15–17`; `words\断る.md:4,15–19`.

Two unprotected pairs remain:

- **下降 / 下りる:** “descent; decline” and “go down or get off” overlap in actual descending meanings. Excluding 降りる does not exclude the separate stable word ID 下りる.
- **下降 / 断る:** both titles contain unqualified English “decline.” This is English-label polysemy, not Japanese synonymy—the same kind of presentation risk already guarded by 角度/釣る.

These pairs can produce defensible alternative labels or answers. Existing exclusions do not protect them transitively.

**Minimal remedy:** add direct exclusions for `下りる` and `断る` on 下降. Alternatively, remove the second collision through sufficiently explicit English disambiguation.

**Evidence:** `docs\n2-vocabulary-batch-sources\batch-14.json:12859–13031` contains the complete 1589500 family: both 降りる and 下りる permit sense 1, “descend/go down/come down,” with the sense-local note “esp. 下りる.” Principal family 1184940 supplies descent/decline for 下降. The independently retrieved [断る entry](https://jisho.org/api/v1/search/words?keyword=%E6%96%AD%E3%82%8B), at ことわる, explicitly includes “to decline” in its refusal sense. The displayed titles establish the English collision. **Confidence: high.**

**B14-GPT-03 — Minor; correctness: English “grade” ambiguity.**  
**Location:** `words\学年.md:4,9,16`; `words\位.md:4,9,16`; `words\級.md:9`.

学年’s title, “school year; grade,” remains unprotected against 位’s “rank; grade.” Their Japanese meanings differ, but the unqualified English component “grade” permits the same school-grade versus classification-grade ambiguity that the batch already recognizes for assessed marks. 学年 excludes 級, and 級 excludes 位; that chain does **not** exclude 学年/位.

**Minimal remedy:** add `位` to 学年’s direct `quiz_exclusions`. No change to the Japanese distinction is necessary.

**Evidence:** principal family 1207030:2 identifies a grade **in school**. The independently retrieved [位 entry](https://jisho.org/api/v1/search/words?keyword=%E4%BD%8D), specifically くらい, identifies “grade (of quality, etc.); level; tier; rank.” The actual titles leave “grade” unqualified, and the two articles have no mutual exclusion. **Confidence: high.**

## Optional

None.

## Limits

I had **file and web tools, but no Git execution**. I could not independently compare the worktree with the frozen commit, reconstruct the parent diff or recompute receipt/source hashes. Snapshot identity and committed-content cleanliness therefore rely on the supplied frozen receipt.

The principal dictionary families and component records were inspected as supplied evidence, not independently re-extracted from the historical dictionary downloads. Author inspection receipts were not treated as independent reviewer retrieval. I independently fetched the nine article-cited Kotobank entries used for consequential qualifications and the additional dictionary entries cited in the findings; those live pages are not frozen artifacts.

In particular, the かこう boiler-burner sense is supported by the supplied pinned JMdict family; the fetched Japanese entry independently corroborates the crater meaning and reading distinctions, not that burner sense. Selected comparison evidence is not the whole dictionary. This review does not establish exhaustive fallback-quiz safety, measured usage frequency, attestation of every authored sentence or native-speaker certification.
