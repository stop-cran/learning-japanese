## Snapshot: 7359a791ab051c71c555a1931bfbaeea7ab07578 — committed content only

**Four missing quiz-exclusion pairs across three articles warrant fixes. No actionable prose, source-mapping, or scoped kanji-link defect was established.**

Parent: `7c56c36ac8ebd74f1e76ae486e05920be683de57`. I read `frozen-snapshot.json` first. Its clean-tree, commit, hash, and equivalence assertions are author-provided evidence: the available file tools cannot execute Git, so I could not independently authenticate the checkout against that commit. No uncommitted changes were intentionally included.

## Scope

Actual model: **gpt-6.1-sol**, family **gpt**. Independent, read-only review; no agents, delegation, edits, or access to another reviewer’s report.

Complete assigned reads covered all twenty word articles; `related.patch`; the four edited kanji cards 延・換・灰・鈍 and unchanged 伸; all twenty mappings and twenty complete principal families, including restrictions, flags, inherited POS, raw fields, and selected/additional senses; all 31 component records and 165 labels. I read the required instructions, `docs\content-format.md:18–103`, both permitted source snapshots, the TSV header and exactly `N2:1302–N2:1321`, plus the allowed JLPT and confusable-word guidance.

Comparison reads covered all twelve complete-family renderings and the 完全 supplement—the supplied 257-family/739-sense union—and all thirteen older-body renderings plus three supplemental bodies: **111 reproduced complete older articles**. These are actual reviewer reads, not inherited author scope. I additionally read the current complete articles 移る・掲示・お先に・じゃあ・じゃ・それでは・送別・皆さん・全般・スタンド・いちいち.

I read the complete original and canonical-lookup public bodies and capture records. Their 22 positive captures represent **one authority, Digital Daijisen via Weblio**, with the unsuccessful raw 乗換 request kept distinct from the successful 乗り換え lookup. Fresh Jisho JMdict retrievals supplied relevant complete lexical results for じゃあ/じゃ・それでは・いちいち・皆さん・スタンド; Takoboto corroborated the じゃあ result. These are further presentations of JMdict, not additional independent dictionaries.

The large `review-evidence.json` was read only through its opening 150 lines; the required records were inspected through the complete compact derivatives instead. Banned ledgers, author quiz rationale, private scripts/checks, and other reviewers’ reports were not read.

## Verdicts

**Correctness** concerns the teaching, examples, and metadata. **Scoped coverage** includes necessary quiz guards. **Comprehensibility** concerns learner-facing explanation. `CLEAN` means no actionable defect established within this scope.

For **each of the twenty mappings**, correctness, scoped coverage, and comprehensibility are **CLEAN**. The final column records the independently assessed entry/sense association: numbers before `+` are selected senses; numbers after it are the mapping’s additional recognition teaching—not independently established N2 membership.

| Source row and exact article association | Correctness | Scoped coverage | Comprehensibility | Mapping: entry; selected + additional |
|---|---|---|---|---|
| N2:1302 のこぎり → `words\のこぎり.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1232930:1 |
| N2:1303 残らず → `words\残らず.md` | CLEAN | **NEEDS FIX** | CLEAN | CLEAN — 1611130:1 |
| N2:1304 載せる → `words\乗せる.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1600270:1,3 +9 |
| N2:1305 覗く → `words\覗く.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1470840:1,3,4,5,6 |
| N2:1306 延ばす → `words\伸ばす.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1600290:2 +7,8 |
| N2:1307 延びる → `words\伸びる.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1358870:8 +9 |
| N2:1308 上り → `words\上り.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1352510:1,2 +3,4 |
| N2:1309 上る → `words\登る.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1352570:1 +2 |
| N2:1310 糊 → `words\糊.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1267400:1,2 |
| N2:1311 乗換 → `words\乗り換え.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1600460:1 +2 |
| N2:1312 載る → `words\載る.md` | CLEAN | CLEAN | CLEAN | CLEAN — 2649690:2 +1 |
| N2:1313 鈍い のろい → `words\のろい.md` | CLEAN | CLEAN | CLEAN | CLEAN — 2838553:1,2 |
| N2:1314 のろのろ → `words\のろのろ.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1010040:1 |
| N2:1315 呑気 → `words\のんき.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1600560:1 |
| N2:1316 灰色 → `words\灰色.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1201970:1 |
| N2:1317 俳句 → `words\俳句.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1471900:1 |
| N2:1318 売店 → `words\売店.md` | CLEAN | **NEEDS FIX** | CLEAN | CLEAN — 1474040:1 |
| N2:1319 バイバイ → `words\バイバイ.md` | CLEAN | **NEEDS FIX** | CLEAN | CLEAN — 1983760:1 +2 |
| N2:1320 売買 → `words\売買.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1474050:1 |
| N2:1321 這う → `words\這う.md` | CLEAN | CLEAN | CLEAN | CLEAN — 1474200:1,2 +3 |

The consequential mapping distinctions are handled correctly:

- **延びる** sense 8 is validated against the explicitly taught 延びる spelling and deadline-extension construction, not silently transferred to primary 伸びる. 延ばす’s shared extension sense and spelling tendencies are likewise distinguished from hard restrictions.
- **載せる** placement/loading and publication are explicitly taught under stable 乗せる. **上る** climbing and natural rising are taught under stable 登る; 昇る’s promotion sense is not assigned to source 上る.
- **のろい** remains distinct from にぶい. The misleading raw knife-dull gloss is preserved as provenance, not propagated into のろい teaching. **載る** remains distinct from the 乗る lexical record.
- Blank source spelling fields, including のこぎり・のろのろ・バイバイ, and バイバイ’s blank source gloss remain blank. Dictionary-supported teaching does not establish an otherwise unstated compiler intention.
- The articles appropriately qualify route direction for 上り, traditional haiku conventions, usual-kana/ateji treatment, modern versus historical readings, and additional plant-creeping or switching senses.

| Kanji surface | Correctness | Scoped coverage | Comprehensibility | Assessment |
|---|---|---|---|---|
| `kanji\延.md` edit | CLEAN | CLEAN | CLEAN | Both displayed aliases 延ばす **のばす** and 延びる **のびる** reach the shared articles from Readings and Common words. Word-side 延 links are substantive. Footer IDs 1600290/1358870 match. |
| `kanji\換.md` edit | CLEAN | CLEAN | CLEAN | 乗り換え **のりかえ** appears in Readings and Common words, reciprocates the word-side link, recognizes 乗換/乗換え, and has footer ID 1600460. |
| `kanji\灰.md` edit | CLEAN | CLEAN | CLEAN | 灰色 **はいいろ** appears in both required sections, reciprocates the word-side link, and has footer ID 1201970. |
| `kanji\鈍.md` edit | CLEAN | CLEAN | CLEAN | Common words/Notes distinguish kana-primary のろい from にぶい and link its article. Footer includes 2838553. No fabricated のろ reading row or kana-primary metadata change. |
| `kanji\伸.md` unchanged baseline | CLEAN | CLEAN | CLEAN | Existing reciprocal Readings/Common words links for 伸ばす **のばす** and 伸びる **のびる**, with matching 1600290/1358870 IDs, remain suitable. |

**Baseline preservation — correctness CLEAN; scoped coverage CLEAN; comprehensibility CLEAN**, based on the supplied patch and inspected bodies. Stable identities, primary metadata, existing exclusions, and easier N3 levels for 乗せる・伸ばす・伸びる and N5 for 登る are retained. のろのろ adds only `jlpt: 2`. The kanji headers are unchanged. Unchanged 乗せる/登る were read for claimed source coverage; this is not a claim that their whole bodies were newly authored or commissioned for revision.

No defect was established in primary written-Han metadata or substantive links to existing component cards. Nonexistent component cards were not demanded. Quiz exclusions were considered directly, including ordinary secondary meanings and both quiz directions; no actionable **excess exclusion** was established within the inspected scope.

## Findings

**N2-B66-GPT-01 — Minor; scoped coverage / quiz exclusions**

**Location:** `words\残らず.md:9`

**Claim and impact:** Two direct pairs remain unguarded: **残らず/いちいち** and **残らず/皆さん**. The first overlaps in exhaustive, omission-free coverage; the second overlaps when the relevant set is people. Neither counterpart declares the pair. Their titles differ, so exact-title deduplication does not resolve the ambiguity.

**Exact evidence:** 残らず’s title is “all; without exception”; its explanation explicitly includes people, and line 19 translates the example as “Every participant … without exception.” `words\いちいち.md:4,16–24` supplies “every single” and complete individual attention; the fresh [JMdict result](https://jisho.org/api/v1/search/words?keyword=%E3%81%84%E3%81%A1%E3%81%84%E3%81%A1), relevant entry 1587320, sense 2, includes “each and every” and “without omission.” `words\皆さん.md:4,15–20,32–34` teaches “everyone” in the relevant group; its [JMdict result](https://jisho.org/api/v1/search/words?keyword=%E7%9A%86%E3%81%95%E3%82%93), entry 1202170:1, includes “all; everyone; everybody.” Thus いちいち or 皆さん can face a defensible “all; without exception” alternative.

**Minimal remedy:** Add `いちいち` and `皆さん` to 残らず’s exclusions. This does not assert unrestricted grammatical interchangeability or require excluding their other neighbors. **Confidence: high.**

**N2-B66-GPT-02 — Minor; scoped coverage / quiz exclusions**

**Location:** `words\売店.md:9`

**Claim and impact:** **売店/スタンド** is unguarded despite an ordinary shared sales-stand meaning. A 売店 question can offer both its intended “kiosk; facility shop” label and スタンド’s “stand; spectator stands; lamp” label, whose first alternative is also defensible.

**Exact evidence:** `words\売店.md:16` explicitly defines 売店 as a “shop, kiosk, or sales stand”; complete principal 1474040:1 includes “stand.” `words\スタンド.md:4,16–18,27` gives the displayed title, sales-stand/counter meaning, and newspaper-stand example. Its sole exclusion at line 9 is 台. The relevant complete lexical result in the fresh [JMdict retrieval](https://jisho.org/api/v1/search/words?keyword=%E3%82%B9%E3%82%BF%E3%83%B3%E3%83%89), entry 1069930:2, confirms “stand (e.g. newspaper stand); counter.”

**Minimal remedy:** Add `スタンド` to 売店’s exclusions. No expansion into a general shop/stall exclusion clique is justified by this finding. **Confidence: high.**

**N2-B66-GPT-03 — Minor; scoped coverage / quiz exclusions**

**Location:** `words\バイバイ.md:9`

**Claim and impact:** **バイバイ/それでは** is unguarded. In a Japanese-to-English question for それでは, “bye-bye; goodbye” can be a valid leave-taking answer alongside its own discourse-organizing title. The existing バイバイ/では guard does not cover this separate pair.

**Exact evidence:** `words\バイバイ.md:4,16–21` teaches goodbye and parting. `words\それでは.md:4,34–36` gives the different displayed title, explicitly teaches conversational closing, and cites entry 1406050, senses 1–4. The fresh [JMdict result](https://jisho.org/api/v1/search/words?keyword=%E3%81%9D%E3%82%8C%E3%81%A7%E3%81%AF) confirms sense 4, “bye then.” Neither article declares the pair.

**Minimal remedy:** Add `それでは` to バイバイ’s exclusions. This follows its own attested farewell sense—not transitivity through では, or an assumption that every conversational connector means goodbye. **Confidence: high.**

All three findings concern possible ambiguous choices under the documented quiz contract, not observed runtime questions. A single declaration per pair is sufficient because guards are symmetric; guards between other pairs do not propagate transitively.

## Optional

None. Additional dictionary senses, variants, historical details, or broader comparison inventories are not required for this practical scope.

## Limits

**Frozen-state authentication remains UNVERIFIED:** Git state, hashes, and compact-rendering equivalence were not independently executed. Content judgments rely on the supplied frozen-snapshot assertions and inspected evidence.

The complete reproduced older-body set is not every possible current comparison article. Unread candidate bodies were not treated as absent meanings, and label inspection was not counted as full-body inspection. Quiz coverage is therefore bounded, not repository-wide certification.

Fresh Weblio retrievals did not expose the relevant Daijisen lexical text; the Jisho HTML page was interface-only, and the attempted Kotobank URL returned 404. Those responses were not counted as verification. Four attempted comparison paths—記載・掲載・一切・それじゃ—did not exist; no semantic absence was inferred from that.

No corpus-frequency study, native-speaker certification, or exhaustive etymological review was performed. No additional consequential teaching claim remains unresolved within the stated review scope.
