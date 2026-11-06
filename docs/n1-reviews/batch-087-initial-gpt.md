## Snapshot

`f6391022356073dd3e53437be30885f9a09857d9`, as identified by the supplied signed-snapshot packet. No independent Git, signature, or hash verification.

## Scope

**Reviewer/model:** GPT-6.1 Sol (`gpt-6.1-sol`), without delegation.

Read exactly one resource: `C:\Users\stop-\n1-kanji-workspace\control\batch-087-initial-packet.txt`, using one full-file `view` call with `forceReadLargeFiles=true`. The packet was supplied as 146,190 bytes/2,830 lines; the response reached its final included passage, `docs\jlpt-levels.md:23`, without a visible truncation notice. No recovery reads or other resource access.

Reviewed all three complete new articles, their exact teaching diff, comparison articles, five raw character records (**凪・風・凡・凹・止**), metadata, textual SVG/stroke evidence, public dictionary extractions and provenance, and supplied format/quiz contracts. Unchanged articles served as comparison evidence, not rewrite targets.

Inspected all **25 complete JMdict families**, including their senses, restrictions and flags:

- Main: 1459650, 1459660, 1537050, 1696000, 1739920, 2068150, 2174040, 2174150, 2570420, 2871415.
- Comparison: 1179150, 1183590, 1310640, 1361130, 1381820, 1415050, 1499720, 1499730, 1557050, 1584280, 1589220, 1594270, 1816340, 2756450, 2859999.

## Verdicts

**CLEAN** means no established actionable defect within this bounded review, not exhaustive correctness.

| New article | Correctness | Scoped coverage | Phone-text comprehensibility |
|---|---|---|---|
| `kanji\凪.md` | CLEAN | CLEAN | CLEAN |
| `words\凪.md` | CLEAN | CLEAN | CLEAN |
| `words\凪ぐ.md` | CLEAN | CLEAN | CLEAN |

## Findings

**Proved defects: none. Consequential unresolved article claims: none identified.**

The following checks support those verdicts:

**Readings and character facts.** `kanji\凪.md:6–12,37–44` preserves the exact raw kun entries and order, **なぎ / な.ぐ**, selects both, and gives each its own correctly allocated linked example. The noun supplies なぎ; 凪 in 凪ぐ supplies な, with written ぐ outside it. Both on lists are explicitly empty; no on reading is invented. Radical **几, 16**, six strokes and source grade 9 agree with the supplied record. Lines 62–63 correctly distinguish name-use classification from name-only vocabulary. N1 is explicitly a community label; neither new word receives an inferred vocabulary level. The labelled modern-shape mnemonic is separate from the sourced **kokuji** definition, and omission of a phonetic field makes no denial about phonetic components.

**Constructions, meanings and translations.** The noun’s weather-state explanation and examples are natural and correctly translated (`words\凪.md:15–24,34–45`). The verb correctly teaches intransitive subjects with が, rather than an agent calming an object. Its modern forms **凪ぎます（なぎます）・凪がない（ながない）・凪いで（ないで）・凪いだ（ないだ）** are correct, including the attributive 凪いだ海 (`words\凪ぐ.md:15–25`). The English examples preserve the relevant state/change distinction.

The spelling boundary is adequately qualified (`words\凪ぐ.md:44–53`): supplied Daijisen assigns modern godan weather sense 1 to **凪ぐ** and mental-calming sense 2 to **和ぐ**, while separately listing classical 上二段 senses. The article does not import the classical fair-weather sense into its modern paradigm, recommend 心が凪ぐ as the ordinary weather spelling, or claim unrestricted substitution. Its limited modern-weather scope does not require teaching the classical conjugation or every figurative use.

**Dictionary scope and flags.** The articles do not promote search-only 朝なぎ/夕なぎ, kana-only bird readings, or alternative/rare spellings into unrestricted teaching examples. The usually-kana qualification for 時化 is accurate. Omission of specialist compounds, additional dictionary senses and meteorological mechanisms is consistent with the stated practical scope.

**All three kanji distractors.** The actual labels are **風 “wind; style,” 凡 “commonplace; mediocre,” 凹 “concave; sunken.”** Their supplied ordinary secondary meanings do not make them answers for 凪’s lull/calm-sea meaning. The All pool contains all three curated wrong cards, so the documented default four-choice construction needs no fallback for this target. **N1 excludes N4 風**, leaving only two curated wrong cards and requiring an actual production fallback check; that behavior is not certified here. 安・平・静 each already has three curated distractors, so adding 凪 does not by itself force it into their default full-pool choices. Filtered or larger quizzes can still expose fallback candidates.

**All seven direct wordguards.** Each required direct exclusion is present and semantically justified:

| Target | Directly guarded comparisons | Actual overlap |
|---|---|---|
| 凪 | 穏やか; 静か | Calm sea conditions; 静か also has an explicit calm/peaceful dictionary sense |
| 凪ぐ | 静まる; 止む; 落ち着く | Subsiding, wind ceasing, and becoming calm/stable or dying down |
| 凪ぐ | 穏やか; 静か | Calm-result descriptions can make these defensible competing labels |

These judgments use actual meanings and constructions—not merely different titles, parts of speech or topics. Under the supplied exclusion-aware contract, each declaration protects both directions without requiring reciprocal metadata. No transitive clique or universal synonym relation is inferred.

The noun and verb were also checked against each other: **“calm at sea; lull”** names a condition, whereas **“become calm (wind/sea)”** names a change. Their displayed labels and explanations do not establish a need for an additional mutual exclusion.

**Identity and reciprocal links.** The two mapped pairs have all four required directions: kanji→noun at `kanji\凪.md:39`, noun→kanji at `words\凪.md:28`, kanji→verb at `kanji\凪.md:40`, and verb→kanji at `words\凪ぐ.md:29`. Separate word IDs, readings なぎ/なぐ and complete written-kanji arrays `[凪]` are consistent. Comparison mentions do not activate baseline-pair or incidental-backlink quotas.

## Optional

None. No speculative defect or optional rewrite is proposed.

## Limits

This is a textual review of supplied evidence, **not independent upstream retrieval**. Public-page evidence consists of coordinator-extracted dictionary articles and supplied archive receipts; hashes and lossless-archive claims were not independently checked.

No native-speaker review, font rendering, historical-glyph inspection, drawing/animation evaluation, app execution, phone/UI observation or measured learning-effectiveness evidence was obtained. Phone-text verdicts concern wording and kana support only.

Production fallback choices—especially in the N1 pool—remain unverified. Older clients that ignore word exclusions are not certified semantically safe by this review. No files were edited.
