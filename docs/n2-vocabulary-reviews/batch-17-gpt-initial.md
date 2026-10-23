## Snapshot: 4fa37301b6863b299555ce1e9bc3e4855e0167d9 — committed content only

Parent: `84b5fd4ad97a514701bc1546fdd23ef34c81259d`. Snapshot identity and committed-content status are taken from the frozen receipt, subject to the verification limitation below.

## Scope: GPT-6.1 Sol (`gpt-6.1-sol`; family `gpt`)

Independent, sequential, read-only review of all nineteen new articles in full; all eight related changes against the supplied patch and surrounding context; the narrowly claimed reuse of `words\枯れる.md`; and mappings **N2:322–N2:341**, including their selected-sense qualifications.

Evidence included the required instructions and format reference, all twenty complete principal dictionary families, selected complete comparison records, component evidence, actual comparison-card titles/exclusions, and independently fetched dictionary and established reference pages. No agents were used and no files were edited. Unchanged teaching in related articles was not comprehensively recertified.

## Verdicts: two localized quiz-correctness fixes

Here, correctness includes whether quiz alternatives can admit another valid answer. Neither finding requires broadening the article’s declared teaching scope.

| Source row | New article | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| N2:322 | `words\釜.md` | CLEAN | CLEAN | CLEAN |
| N2:323 | `words\紙屑.md` | CLEAN | CLEAN | CLEAN |
| N2:324 | `words\神様.md` | CLEAN | CLEAN | CLEAN |
| N2:325 | `words\剃刀.md` | NEEDS FIX | CLEAN | CLEAN |
| N2:326 | `words\ガム.md` | CLEAN | CLEAN | CLEAN |
| N2:327 | `words\貨物.md` | CLEAN | CLEAN | CLEAN |
| N2:328 | `words\かゆい.md` | CLEAN | CLEAN | CLEAN |
| N2:329 | `words\歌謡.md` | CLEAN | CLEAN | CLEAN |
| N2:330 | `words\殻.md` | CLEAN | CLEAN | CLEAN |
| N2:331 | `words\カラー.md` | CLEAN | CLEAN | CLEAN |
| N2:332 | `words\からかう.md` | CLEAN | CLEAN | CLEAN |
| N2:333 | `words\空っぽ.md` | CLEAN | CLEAN | CLEAN |
| N2:334 | `words\かるた.md` | CLEAN | CLEAN | CLEAN |
| N2:336 | `words\カロリー.md` | CLEAN | CLEAN | CLEAN |
| N2:337 | `words\かわいがる.md` | CLEAN | CLEAN | CLEAN |
| N2:338 | `words\乾かす.md` | CLEAN | CLEAN | CLEAN |
| N2:339 | `words\渇く.md` | NEEDS FIX | CLEAN | CLEAN |
| N2:340 | `words\為替.md` | CLEAN | CLEAN | CLEAN |
| N2:341 | `words\瓦.md` | CLEAN | CLEAN | CLEAN |

**All twenty source mappings are CLEAN / CLEAN / CLEAN within the mapping scope:** each assigned spelling, reading and applicable meaning is explicitly taught. This includes N2:335 → `words\枯れる.md`, whose existing plant-withering explanation supports the source row and whose patch adds only `jlpt: 2`.

The important qualifications are supported: 釜 is not invariably iron; 歌謡 is not restricted to narrative ballads; かるた’s practical traditional-card scope is distinguished from generic cards; and カラー’s collar meaning is separately attributed to entry **2853151:1**, not incorrectly folded into color entry **1038500**. Unselected readings and secondary meanings are not automatically assigned N2.

| Related file | Assessed change only | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `kanji\貨.md` | Reciprocal 貨物 link at かもつ | CLEAN | CLEAN | CLEAN |
| `kanji\乾.md` | 乾かす links; qualified throat-spelling comparison | CLEAN | CLEAN | CLEAN |
| `kanji\替.md` | 為替 example; whole-word-reading warning | CLEAN | CLEAN | CLEAN |
| `words\乾く.md` | Qualified thirst spelling; counterpart links and particle contrast | CLEAN | CLEAN | CLEAN |
| `words\干す.md` | Navigation to 乾かす | CLEAN | CLEAN | CLEAN |
| `words\色.md` | Navigation to カラー | CLEAN | CLEAN | CLEAN |
| `words\いじめる.md` | Navigation to からかう | CLEAN | CLEAN | CLEAN |
| `words\枯れる.md` | Sourced level only; limited reuse claim | CLEAN | CLEAN | CLEAN |

Written-kanji metadata is complete for the new primary forms. The three required new N2 reciprocal pairs—貨/貨物, 乾/乾かす and 替/為替—are present with appropriate readings. The links to `words\空.md` genuinely target its explicitly taught **から**, “empty,” use, despite its primary **そら**, “sky,” identity.

## Findings: two actionable omissions

**B17-GPT-01 — Minor; correctness (quiz-choice semantics).**  
**Location:** `words\剃刀.md:4–9,32`; comparison `words\鋭い.md:4–9,15–24`.

剃刀 has no exclusion against 鋭い, whose displayed answer is **“sharp; keen; perceptive.”** Beyond the physical razor, 剃刀 has an established mental-sharpness use. Consequently, that alternative can be a defensible answer when the quiz displays 剃刀. The article’s tool-only teaching scope does not sense-restrict the quiz itself.

**Minimal remedy:** add `quiz_exclusions: [鋭い]` to 剃刀; the symmetric exclusion mechanism makes a reverse declaration unnecessary. No additional figurative lesson is required.

**Evidence:** pinned entry **1435180, sense 2**, in `docs\n2-vocabulary-batch-sources\batch-17.json:1392–1408`, explicitly gives “razor-sharp (mind, intellect, etc.),” “keen,” “astute” and “sharp.” Independently inspected [Seisenban, 剃刀, sense ③](https://kotobank.jp/word/%E5%89%83%E5%88%80-466505) describes sharp intelligence/judgment; the inspected [鋭い dictionary record, sense 3](https://jisho.org/api/v1/search/words?keyword=%E9%8B%AD%E3%81%84) confirms the overlapping mental sense. Neither card declares the pair. **Confidence: high.**

**B17-GPT-02 — Minor; correctness (quiz-choice semantics).**  
**Location:** `words\渇く.md:4–9,21`; comparisons `words\飢える.md:4–9,16–23` and `words\憧れる.md:4–9,16–18`.

The taught figurative **“crave/thirst for”** meaning remains unprotected against **飢える — “starve; hunger for”** and **憧れる — “yearn for; admire.”** These are direct overlaps in strong figurative longing, not merely shared bodily-need vocabulary. 飢える’s existing affection-deprivation example makes the first overlap particularly clear. The alternatives can therefore be defensible for 渇く’s figurative meaning. Existing exclusions through 望む do not protect either pair transitively.

**Minimal remedy:** append `飢える` and `憧れる` to 渇く’s `quiz_exclusions`. Preserve the distinctions between physical hunger, physical thirst, deprivation and aspirational admiration.

**Evidence:** pinned entry **1208520, sense 2**, at `docs\n2-vocabulary-batch-sources\batch-17.json:955–975`, gives “to thirst for; to crave,” often as **〜に渇いた**. Independently inspected [Daijisen, 渇く, sense 2](https://kotobank.jp/word/%E6%B8%87%E3%81%8F-468604) supplies **愛に渇く**. Inspected JMdict-derived records give [飢える, sense 2](https://jisho.org/api/v1/search/words?keyword=%E9%A3%A2%E3%81%88%E3%82%8B) as being starved of love or thirsty for knowledge, and [憧れる](https://jisho.org/api/v1/search/words?keyword=%E6%86%A7%E3%82%8C%E3%82%8B) as longing/yearning/hankering after something. Neither counterpart declares an exclusion against 渇く. **Confidence: high for 飢える; medium-high for 憧れる’s English-label overlap.**

## Optional: none

## Limits: snapshot verification and bounded lexical coverage

**File tools, not Git execution, were available.** I could not independently verify commit objects, checkout cleanliness, receipt hashes or patch provenance. This report treats the receipt-designated files as the committed snapshot; it does not certify their correspondence to Git independently.

Comparison evidence was selected, not an exhaustive review of all 141 comparison families or every repository quiz pairing. Public dictionary responses were live corroboration, not independently hash-matched copies of the pinned dictionary. Authored examples were assessed for grammar, meaning and naturalness, not individually corpus-attested or native-speaker-certified. Heading-only or unsuccessful lookups were not used as lexical proof.

No additional consequential linguistic uncertainty was identified within the declared scope. **CLEAN** means no actionable defect established there, not exhaustive correctness.
