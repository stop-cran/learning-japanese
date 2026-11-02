# Independent N1 pilot curation review

**Result: CLEAN within the assigned textual scope.** No actionable defect was established. This is not exhaustive certification of unchanged teaching or approval for publication.

## Snapshot and scope

Reviewed the supplied committed-teaching snapshot **`b43173e10f158f59df49137394e1ebbfb0821393`**, against base **`b43143f`**. Snapshot attribution follows the supplied frozen-review context; I did not independently verify Git state or recompute hashes. No uncommitted teaching was substituted into the packet-based assessment.

Model: **GPT-6.1 Sol**, model ID **`gpt-6.1-sol`**.

The assessment covers:
- Changed-passage/metadata integration for all twelve kanji.
- The entirety of the four new support articles.
- Changed passages and integration in the two reused support articles.
- Fifteen comparison articles solely as context for quiz ambiguity.

All tool invocations were read-only and strictly serial. No commands, edits, delegation, tasks, issues, or publication were performed.

### Material actually read

| Packet | Coverage |
|---|---|
| `packet-index.json` | Entire returned document; read first |
| `teaching-01.txt` | Entire packet, lines 1–204 |
| `teaching-02.txt` | Entire packet, lines 1–244 |
| `teaching-03.txt` | Entire packet, lines 1–282 |
| `teaching-04.txt` | Entire packet, lines 1–131 |
| `dictionary-01.txt` | Entire packet, lines 1–467 |
| `dictionary-02.txt` | Entire packet, lines 1–482 |
| `dictionary-03.txt` | Entire packet, lines 1–408 |
| `dictionary-04.txt` | Entire packet, lines 1–419 |
| `dictionary-05.txt` | Entire packet, lines 1–74 |
| `comparisons-01.txt` | Entire packet, lines 1–264 |
| `comparisons-02.txt` | Entire packet, lines 1–244 |
| `comparisons-03.txt` | Entire packet, lines 1–89 |
| `metadata-and-offered-keys.json` | Entire document, lines 1–470 |
| `teaching.diff` | Explicit ranges **1–240** and **241–478** |

**No required packet portions were omitted or truncated.**

I additionally read the complete repository articles `words\新幹線.md`, `words\扱う.md`, `words\乃至.md`, `words\凹む.md`, `words\矛盾.md`, `words\鷹.md`, `words\彗星.md`, `words\うがい.md`, `words\栞.md`, and `words\茉莉花.md` to inspect existing teaching anchors and reciprocal links. These were supplementary working-tree reads, not independently commit-verified exports.

I independently retrieved Kanjipedia’s **莉** entry, discussed below. I did not read other reviews, progress/curation files, ledgers, author notes, or other sessions.

## Per-file verdicts

“Comprehensibility” means textual phone comprehensibility, not observed rendering or physical-phone testing.

| File | Scope | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|
| `kanji\幹.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\氏.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\扱.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\乃.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\凹.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\凸.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\矛.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\鷹.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\彗.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\漱.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\栞.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `kanji\莉.md` | Changed-passage/metadata integration | CLEAN | CLEAN | CLEAN |
| `words\幹.md` | Full new article | CLEAN | CLEAN | CLEAN |
| `words\凹凸.md` | Full new article | CLEAN | CLEAN | CLEAN |
| `words\矛.md` | Full new article | CLEAN | CLEAN | CLEAN |
| `words\鷹揚.md` | Full new article | CLEAN | CLEAN | CLEAN |
| `words\氏.md` | Changed-passage integration; reused identity | CLEAN | CLEAN | CLEAN |
| `words\でこぼこ.md` | Changed-passage integration; reused identity | CLEAN | CLEAN | CLEAN |

## Actual-reading-key suitability

**All 19 exported offered keys have defensible teaching anchors for this bounded kanji-recognition pilot.** This is a curation judgment separate from whether dictionary spellings exist.

| Kanji | Actual on keys | Actual kun keys | Teaching assessment |
|---|---|---|---|
| 幹 | `かん` | `みき` | 新幹線 explicitly allocates カン to 幹; the new standalone article teaches みき. |
| 氏 | `し` | `うじ` | Modern name-suffix し and separate family-name/lineage うじ are expressly distinguished in the reused article. |
| 扱 | — | `あつかう` | Practical handling verb, with the character supplying あつか and written ending う. |
| 乃 | `ない` | — | 乃至 teaches ナイ + シ and prioritizes ordinary kana ないし and its range/alternative uses. |
| 凹 | `おう` | `へこむ`, `ぼこ` | 凹凸 supplies オウ; 凹む supplies へこむ; 凸凹 explicitly allocates its sunken-part ぼこ to 凹. |
| 凸 | `とつ` | `でこ` | 凹凸 supplies トツ; 凸凹 allocates raised-part でこ to 凸, with the standalone forehead/bump use qualified. |
| 矛 | `む` | `ほこ` | 矛盾 explicitly allocates ム; the new noun article teaches ほこ without transferring restricted とかり. |
| 鷹 | `おう` | `たか` | 鷹揚 explicitly teaches オウ + ヨウ; the bird noun independently anchors たか. |
| 彗 | `すい` | — | 彗星 explicitly allocates スイ to 彗, not the following セイ. |
| 漱 | — | `うがい` | Defensible **rare-spelling recognition**, not an ordinary writing recommendation; both card and support article prioritize kana. |
| 栞 | — | `しおり` | Useful bookmark/guidebook identity; the support article distinguishes the senses and usual kana spelling. |
| 莉 | `り` | — | Explicit allocation within the plant-name unit 茉莉, reinforced by the inspected character-dictionary entry—not merely a kana-substring inference. |

The most constrained selection is **漱 → うがい**. JMdict 1577660 marks 漱 as a rare spelling and the word as usually kana. Its suitability here rests on the narrow recognition objective, explicit rarity warning, and linked teaching of the useful everyday noun—not on an assertion that written 漱 is common. It should not be presented as a high-frequency standalone spelling.

Every selected raw value has its own Readings-table row and a relative word-article link in a later column. The 氏 article’s different primary reading is not silently treated as interchangeable: its added うじ passage explicitly teaches the alternate identity.

The diff preserves full source reading lists and their order. Selected values are exact raw-string subsets, retaining dots and script where applicable. The exported questions agree with the stipulated folding, separator removal, stem deduplication, and maximum-three rule. Disabled kinds remain explicitly empty.

## Supporting assessment

**Correctness.** The new articles’ selected meanings, readings, examples, kana, translations, and grammatical descriptions are coherent. Particularly consequential restrictions are preserved: 凸凹’s abstract sense is restricted to でこぼこ in JMdict 1582410; とかり is restricted to 鋒 in 1603450; and おうよう／ようよう are restricted to 鷹揚 rather than 大様 in 1608970. No word JLPT levels are inferred for the four new articles.

**Coverage and ambiguity.** The new exclusions are defensible direct pairs, not transitive expansions:

- 幹 excludes the four foundation-related labels, consistent with its figurative sense and the comparison articles.
- 凹凸 excludes the three inspected unevenness/roughness comparisons.
- 矛 excludes 武器, supported by 1603450 sense 2 as well as the broader weapon category.
- 鷹揚 excludes all eight inspected composure/easygoing comparisons, including secondary senses obscured by labels such as しっとり and 平気.

The unchanged kanji distractors show no integration regression: each card retains three defensibly wrong alternatives. Reciprocal navigation is present for the new support and reused 氏／でこぼこ relationships. The reused articles retain their original headword identities, primary readings, easier levels, and existing exclusions or absence thereof.

**Comprehensibility.** The new support articles provide standalone English, readable examples with kana and translations, and meaningful contrasts. The additions to 氏 prevent mechanical substitution of うじ into modern name suffixes. The 凹凸／凸凹 distinction remains clear without suggesting that reversing characters licenses arbitrary reading substitution.

## Findings

**None established within the assigned scope.**

## Optional polish or expansion

None required.

## Evidence and limits

The 58 supplied JMdict families and metadata export were frozen evidence supplied for this review, not my own upstream dictionary downloads. Their stated creation dates and hashes were not independently validated.

The Kotobank observations for 鷹揚 and 氏 were **coordinator-supplied observations**, not independent live retrieval. They support the relevant reading allocation, manner/image explanation, and family-name/lineage recognition. I did not treat the reported Daijisen ようよう cross-reference as an extracted おうよう definition.

My live Kanjipedia retrieval returned the actual **莉** heading, explicitly listing **リ・レイ** and **茉莉（マツリ）**. It supports the selected リ allocation; it does not independently confirm every preserved KANJIDIC2 reading.

The compatible-client behavior was supplied context. Mechanical projection agreement is **not app execution**. Publication still requires a compatible client; older APKs ignoring curation are not covered by this textual result.

No native full-archive import, runtime navigation, quiz behavior, drawing, system-Back/offline behavior, font rendering, physical-phone, native-speaker, measured-learning, or general-release acceptance is certified. **CLEAN means no actionable defect established within this scope, not exhaustive correctness.**
