**Snapshot:** Supplied frozen commit `aef958a3bccd96044d0af50e2da74b1b8cfe20da`; committed teaching content only, with no uncommitted teaching included as specified. Git identity, signature, worktree cleanliness and baseline preservation could not be independently verified using the permitted tools.

**Scope:** Independent initial read-only review by GPT-6.1 Sol (`gpt-6.1-sol`), covering correctness, scoped coverage and textual/phone-text comprehensibility:
- Complete `kanji\企.md` and `words\企てる.md`; the added component link in `words\企業.md`, with its complete article read as context.
- All **194 complete JMdict families**: 167 lexical, 16 comparison and 11 additional, including spelling/reading restrictions and sense-local labels.
- All seven complete supplied KANJIDIC2 records; all 11 assigned comparison kanji articles and 13 comparison word articles.
- All eight supplied Japanese dictionary article-node extracts and the complete 62-line KanjiVG SVG.
- All assigned guidance ranges, scoped `docs\confusable-words.md` material, and actual metadata for the twelve identified legacy fallback cards.
- Fresh retrieval of kanjiapi.dev’s **企** record, confirming N1, grade 8, six strokes and the supplied reading lists.

No author rationale, progress/evidence ledgers, other reviews or reconciliation records were consulted.

**Verdicts:**

| Teaching file | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| `kanji\企.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\企てる.md` | **CLEAN** | **CLEAN** | **CLEAN** |
| `words\企業.md` — changed component link/passage | **CLEAN** | **CLEAN** | **CLEAN** |

For `企業.md`, these verdicts concern the changed link in its existing component explanation. The unchanged article was read for context, not subjected to unrestricted reauthoring review. **CLEAN** means no actionable defect established within this scope, not exhaustive certification.

**Findings:** None.

Supporting assessment:

- **Metadata and reading allocation:** 企’s complete ordered readings match KANJIDIC2: `キ`; `くわだ.てる`, `たくら.む`. The explicit practice subsets retain `キ` and `くわだ.てる`, each with its own linked reading-table model. 企業 supplies the regular キ + ギョウ allocation; 企てる supplies くわだ with written てる. Both selected support articles link back to 企, including the reused 企業 article. No vocabulary JLPT level is inferred for 企てる.
- **Shape and origin:** The six-stroke SVG explicitly groups top 人 and bottom 止. The card clearly labels its stopping-to-plan explanation as a modern mnemonic, not etymology. Its 人 indexing radical and comparison with 全’s 入 indexing radical agree with the supplied records.
- **Verb teaching:** Ichidan forms, transitive を attachment, negative/past/progressive forms, complete example readings and English translations are sound. The business example does not manufacture a wrongdoing-only restriction; the unspecified-plan example naturally permits suspicion. Planning, undertaking and successful completion are appropriately distinguished.
- **Lexical/register qualifications:** JMdict 1218140 supports kana-usual たくらむ; the supplied 日本国語大辞典 extract explicitly says **多く** for undesirable planning. The articles appropriately present this as a tendency, distinguish the godan verb from ichidan 企てる, and avoid calling it a contraction. JMdict 1218120’s archaic label is correctly confined to its tiptoe sense.
- **企業 linkage:** The new link targets the correct kanji article without changing the existing business-enterprise explanation. The contextual business sense is supported by JMdict 1218190 and the supplied Japanese definitions. Its wording “in this card” appropriately bounds the contrast with 起業 rather than denying every historically recorded 企業 sense.

All **11 direct 企てる exclusions** were assessed independently against actual titles and ordinary senses, in both Japanese-to-English and English-to-Japanese directions:

| Direct partner | Basis for retaining the exclusion |
|---|---|
| 計画 | “plan; planning” overlaps the planning sense |
| 予定 | “plans; schedule” overlaps intended arrangements |
| プラン | “plan; package” includes the overlapping plan sense |
| 設計 | “design; planning” overlaps devising/planning |
| 計 | Its displayed label includes the ordinary “plan” sense |
| 引き受ける | “undertake” overlaps the undertaking sense |
| 案 | “proposal; draft” overlaps a contemplated plan/proposal |
| 提案 | “proposal; suggestion” overlaps proposing an undertaking |
| 言い出す | Its displayed “propose” sense overlaps |
| 試す | “try out; test” creates an English-label overlap with “attempt” |
| 試し | “trial; try” similarly overlaps the attempt label |

These safeguards do not assert unrestricted Japanese substitution, identical register or transitive exclusion cliques. Existing 企業/会社 protection remains declared on 企業; 商社 retains its direct exclusions against both 会社 and 企業.

For the default four-choice kanji quiz, 企’s three curated wrongs—危 “danger,” 休 “rest,” 全 “whole; complete”—are semantically distinct. I also inspected the actual 計/図/承/意/試 articles: their planning, undertaking, intention or trying senses make title-string inequality insufficient evidence of safe wrong answers, but none is a curated wrong for 企. The twelve identified two-distractor legacy cards—人/休/何/入/出/口/女/山/日/月/男/買—have no established meaning collision with 企’s “plan; undertake” fallback label.

**Optional:** One additional example showing an actual attempt, rather than planning alone, could reinforce 企てる’s second taught sense. This is nonblocking; the current explanation already states that distinction.

**Limits:** All assigned ranges were returned without truncation or failed reads. Japanese dictionary evidence was coordinator-supplied extraction, not my independent upstream retrieval; only the kanjiapi.dev lookup was freshly retrieved. Baseline metadata/readings/levels/exclusions preservation was not independently diff-verified.

Comprehensibility judgments are textual. No native acceptance, physical-phone inspection, glyph-rendering or drawing test was supplied or performed. The reported 52-Han cmap coverage is supplied mechanical evidence, not readability evidence. Reading curation requires the specified compatible Android `f9b59a2+`; this review does not certify runtime compatibility or general-release acceptance. The fallback assessment is bounded to the specified default case, not every larger/random/live pool.

All tools were invoked serially, one call per response, awaiting each result; this is self-observed session behavior, not an external execution audit. No files were edited and no commands, delegation, commits or issues were used.
