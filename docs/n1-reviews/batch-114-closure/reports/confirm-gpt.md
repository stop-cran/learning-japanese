Snapshot: `ac38b8e4427afc2c10a957871c5ec99e9cb92bda`, confirming the revision of `8c2bdc27e5d556e639a4d0e9239ae5f2009c400f`; run N1-B114-GPT-CONFIRM-001. Reviewer: GPT-6.1 Sol, model ID `gpt-6.1-sol`, identified by the serving runtime. No additional reviewers or agents were used.

Scope: One read-only confirmation, not a new first review or an implementation. I opened all 29 confirmation-chain segments, once each, in order: **1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29**. Re-views: **none**. Every read used the exact reached absolute filename, without a range.

All 53 chain sources were read: the confirmation instructions; the complete initial report; RESPONSE and CHANGES; all three diff listings; all fifteen revised cards in full; all twelve supplied counterpart cards in full (房, 庁, 部, 課, 集, 拾, 利, 績, 怪, 穂, 盤, 板); all ten confirmation checks; the evidence README, five complete newly cited JMdict entries and complete supplied QuizBuilder.kt; both original rubrics; original content-format.md **lines 1-139 only**; complete fifteen KANJIDIC2 records; all 65 complete original JMdict families; and the full title index, **lines 1-1221**. The index starts `一 one` and ends `齢 age; years lived`, supplied SHA-256 `7241a3ea93227a7298b51d6a4d14753302594c83e59e7455533b6d8956d99d8f`.

This pass's three public fetches, each publicly announced with its purpose before the call:

| URL | Purpose and evidence actually inspected |
| --- | --- |
| https://www.weblio.jp/content/碁 | Check the new game/board comparison and supplemental キ reading. Daijisen's character and ご/き headings describe the game played on a board, and list ゴ and キ; they do not gloss 碁 as the board object. |
| https://www.weblio.jp/content/穀 | Check the new grain/head comparison and supplementary source claims. Daijisen's コク headings describe food seed crops, including rice/wheat/beans; its たなつもの heading describes rice seed/rice and grains, with historical citations. |
| https://www.weblio.jp/content/魅 | Independently establish the sense underlying F3. Daijisen's み heading distinguishes supernatural beings from captivating attraction. Separately attributed Wiktionary/other dictionary material was not treated as Daijisen evidence. |

All three returned the relevant dictionary headings within the requested 7,000 characters. Their trailing truncation notices were not followed. No packet file, earlier report file, source checkout, history or other local artifact was opened directly. The initial report was read anew only as chain evidence, not used from memory. The report is the sole write, followed by its one authorized full readback.

Dispositions:

F1 - **RESOLVED** - All four requested direct pairs are present once on 寮: 房, 庁, 部, 課 (`confirm-packet/snapshot/kanji/寮.md:14,61-70`; `confirm-packet/diffs/fix.patch:1-30`). The reopened counterparts retain their actual labels and no reverse declaration or target-as-distractor conflict: `original-packet/repo/kanji/房.md:1-15,23-25`, `庁.md:1-11,21`, `部.md:1-11,21-25`, `課.md:1-11,21-23`. The independently read JMdict entries establish 寮's archaic bureau-beneath-ministry and tea-room senses, and 房's room/chamber senses (`confirm-packet/evidence/jmdict-cited-entries.xml:75-139`, entries 1554230 and 2222290). The added notes explicitly preserve historical qualification and disallow arbitrary modern institutional-name substitution. These are direct pairs, not reliance on 房-室 or 寮-局 transitivity.

F2 - **RESOLVED** - 穫 directly adds 集, 拾, 利 and 績, retaining all original guards (`confirm-packet/snapshot/kanji/穫.md:14,58-68`; `confirm-packet/diffs/fix.patch:100-129`). Actual counterpart titles/body senses support gathering, picking up/gathering, benefits and results (`original-packet/repo/kanji/集.md:3,21-23`, `拾.md:3,21,29-32`, `利.md:3,21-24`, `績.md:3,21,30-41`). The complete 収穫 family keeps harvest/ingathering, useful gains/results and catch as distinct senses (`original-packet/evidence/jmdict-families.xml:492-535`, entry 1330510). The revision expressly locates the extensions in 収穫, preserves the noun-versus-する warning, and does not turn bare 穫 into a general verb for all collecting or benefiting. None of the four is also a curated distractor or a duplicate reverse declaration.

F3 - **RESOLVED** - 魅 directly adds 怪 and changes “Both” to “These,” correctly accounting for its now three comparisons (`confirm-packet/snapshot/kanji/魅.md:14,60-64`; `confirm-packet/diffs/fix.patch:130-158`). The actual 怪 card displays suspicious/uncanny and teaches uncanny beings (`original-packet/repo/kanji/怪.md:3,21-22,30-31,37-41`). This pass's fetched Daijisen 魅 heading independently supports the supernatural sense; the added descriptive phrase matches 怪's actual title, not an invented generic “charm” title. The distinction among suspicion, supernatural beings and personal appeal remains explicit. The pair is effective without a reverse declaration and without transitivity through 妖.

O1 and L1-L6 have no disposition, as requested. Their continuing evidence limits are recorded below; no absent change is counted as resolving a limit.

Verdicts:

Correctness - **UNVERIFIED** overall. The selected core reading/word pairs and the revised F1-F3 descriptions are supported. 症's changed gloss is CLEAN. Supplementary, unchanged linguistic/source claims remain unverified on 娯, 寮, 砲, 糖 and 紺; exact modern community-level membership and fresh asset geometry remain unverified for all fifteen. 穀's Daijisen beans/classical-reading statements and 碁's additional キ are independently supported in this pass. The unsupported exclusion rationale on 穀 and 碁 is addressed under Finding 1, rather than described as an incorrect core definition.

Scoped coverage - **CLEAN** within confirmation scope for 娯, 寮, 廊, 栓, 汽, 症, 砲, 碁, 磁, 穀, 穫, 糖, 紺, 雰 and 魅. F1-F3 are resolved. No additional vocabulary, historical reconstruction, or omitted ordinary prerequisite was established as necessary. This does not certify every unread comparison-card body or the entire corpus.

Consistency and quiz safety - **NEEDS FIX** on **穀 and 碁**, Finding 1. The other thirteen cards are CLEAN for the inspected meaning options, new direct pairs, metadata and limited-pool audits. All fifteen retain UNVERIFIED broader reading-pool/client/native guarantees. The newly supplied reading-options audit is not a complete audit of extra attested readings.

Comprehensibility - **NEEDS FIX** on **穀 and 碁**, Finding 1's misleading exclusion criterion. The other thirteen cards are CLEAN within the inspected scope. The F1-F3 revisions preserve useful distinctions and readable explanations.

Confirmation: **NEEDS FIX**. F1, F2 and F3 are resolved, but the two additional meaning exclusions introduce a new unsupported selection criterion. This is a localized confirmation finding, not a claim that the current default meaning quizzes have two correct answers or that the original findings remain open.

Findings:

1. **Minor; consistency/quiz safety and comprehensibility - Qualified labels and equipment/part relationships are promoted into direct meaning exclusions.**

   **Locations:** `confirm-packet/snapshot/kanji/穀.md:14,68-70`; `confirm-packet/snapshot/kanji/碁.md:14,59-62,65-67`; added hunks in `confirm-packet/diffs/fix.patch:47-76,78-99`.

   **Claim:** These two additional pairs are structurally valid but their newly stated semantic justification is not established by the actual choices. **穂's full label is “grain-bearing head,” not “grain.”** Its opened body explicitly makes it a plant part, not rice as food (`original-packet/repo/kanji/穂.md:3,23,39-40`). **盤's full label is “board; disc,” not “Go board game.”** Its supplied noun entry means the board used for games, whereas the 碁 entry means the game (`confirm-packet/evidence/jmdict-cited-entries.xml:3-21,46-74`; `original-packet/evidence/jmdict-families.xml:229-253`, entry 1270870). The independently fetched Daijisen headings agree with these distinctions.

   The extra 穀 bullet relies on proximity of the displayed “grain” wording; the extra 碁 bullet relies on the game's own equipment and the shared word “board.” Neither demonstrates that the **whole candidate title** is a defensible translation of the target's established ordinary meaning. A grain head is associated with grain, and a Go board is associated with Go, but these are qualified part/equipment labels. The text itself correctly says they remain different meanings. The relevant contract requires actual-label/ordinary-meaning evidence and says shared topics or different strings alone do not decide an exclusion (`original-packet/repo/docs/content-format.md:97-118`; `original-packet/rubric/copilot-instructions.md:114-116`).

   **Impact:** The explanations teach readers/authors that a shared word inside a qualified label or an equipment/part relationship warrants excluding a meaning choice even without demonstrated ambiguity. The declarations also remove otherwise distinct choices from target and among-option pools. From the inspected `QuizBuilder.kt:26-36`, a supplied two-card pool `[穀, 穂]` or `[碁, 盤]` loses its only wrong choice and returns only the target. This is a static consequence of those declarations, **not an executed Kotlin or Android test**. No new default-four-choice shortage is claimed; the supplied default three options remain available.

   **Remedy:** Remove **only the newly added 穀-穂 and 碁-盤 guards**, and remove the sentences making shared wording/equipment the exclusion reason. Retain the useful grain-versus-head and game-versus-board comparisons, their links and readings, and all F1-F3 fixes. If a separate ordinary target sense or full-label ambiguity is intended, supply evidence for that exact claim instead of using topic proximity. This recommendation does not ask to remove the pre-existing 稲/粒 or other guards wholesale.

   **Evidence:** Full revised and counterpart texts; complete supplied JMdict entries; fresh Daijisen 碁 and 穀 headings; full index; canonical authoring rule; complete supplied meaning-option builder. **Confidence:** high in the label/part/equipment distinction and static filtering consequence; no claim about unexamined historical senses, unusual metonymy or actual device behavior.

Optional: **None.** No unrelated wording polish, reading-inventory alteration, extra vocabulary or new etymology is requested.

Limits:

### Changed-hunk and new-pair accounting

Every changed card was read in full, and every revised hunk was checked across the four facets. `confirm-packet/diffs/changed-files.txt:1-7` lists precisely six card files plus generated manifest.json; `changed-lines.txt:1-7` and the complete patch agree with their revised text. The generated manifest itself is outside this confirmation's content review; its check output was read, not its full JSON.

| Card / changed lines | Independent hunk result |
| --- | --- |
| 寮 14, 63-64, 66-70 | F1 resolved. Room, agency and organizational-unit descriptions match actual counterpart labels/senses and complete JMdict evidence. Historical restrictions remain; title, readings, examples, origin and curated choices are unchanged. |
| 症 50 | CLEAN. The common-word row now gives 重症/じゅうしょう “serious illness,” exactly supported by JMdict 1336310 (`confirm-packet/evidence/jmdict-cited-entries.xml:23-44`). No broader sense is inferred, no required explanatory distinction is lost, and no metadata/link/quiz field changes. |
| 碁 14, 59-62 | Finding 1. 碁盤/ごばん and 盤/ばん board sense are supported; the descriptive “board/disc” matches actual title `board; disc`. 板's descriptive “plank” is present in its actual `plank; board` title and its opened body (`original-packet/repo/kanji/板.md:3,21,30`). This does not prove that a physical board cannot be used for Go; no unrestricted material-use prohibition is endorsed. The game/equipment facts do not establish the new meaning exclusion. Supplemental キ and game-versus-movement distinctions remain unchanged. |
| 穀 14, 69-72 | Finding 1. The full 穂 label is accurately referenced, but its qualifier does not disappear. Splitting the classical-key/Nelson sentence into its own bullet is CLEAN: the reopened KANJIDIC2 record explicitly has classical 115 and separate Nelson 79, so no indexing or etymological claim changed. |
| 穫 14, 58-66 | F2 resolved. Added gathering, gain and result comparisons fit the actual labels. The whole-word qualifications and noun warning remain unchanged; no new arbitrary character or reading substitution is taught. |
| 魅 14, 60-61, 63 | F3 resolved. “Suspicious/uncanny” faithfully describes 怪; “These” fixes the count; supernatural/attraction distinctions remain. |

Eleven pairs were added. I checked each actual counterpart's frontmatter, distractors and displayed label, rather than accepting RESPONSE's corpus-script assertions:

| New pair | Actual counterpart title | Pair judgment |
| --- | --- | --- |
| 寮-房 | room; tassel; bunch | Direct room comparison; F1 resolved. |
| 寮-庁 | government agency | Direct qualified historical bureau/agency comparison; F1 resolved. |
| 寮-部 | section; department | Direct organizational-unit comparison; F1 resolved. |
| 寮-課 | lesson; organizational division | Direct organizational-unit comparison, not lesson equivalence; F1 resolved. |
| 穫-集 | gather | Direct gathering comparison; F2 resolved. |
| 穫-拾 | pick up; gather | Direct crop-gathering comparison; F2 resolved. |
| 穫-利 | benefit; advantage | Qualified useful-gain comparison; F2 resolved. |
| 穫-績 | achievements; results | Qualified productive-result comparison; F2 resolved. |
| 魅-怪 | suspicious; uncanny | Direct supernatural comparison; F3 resolved. |
| 穀-穂 | grain-bearing head | Qualified part, not grain itself; new exclusion not justified, Finding 1. |
| 碁-盤 | board; disc | Equipment, not the game; new exclusion not justified, Finding 1. |

All eleven are declared exactly once on the batch side in the inspected endpoints, retain three curated counterpart slots, and have no endpoint target-as-distractor or exclusion/distractor overlap. The new guards do not form transitive cliques. I did not freshly inspect the other 1,209 cards' distractor arrays to certify RESPONSE's stronger all-corpus assertion about every third card.

The full title index agrees with the eleven counterpart labels and 板. `confirm-packet/checks/link-targets.tsv:1-27` reports 25 changed-line links, all resolving, with descriptive rather than quoted glosses. I checked the new descriptions independently: 房/庁/部/課 support room/agency/organizational-unit wording; 集/拾/利/績 support gathering/gain/results; 怪's “suspicious/uncanny” and 盤's “board/disc” reproduce the actual title components; 板 “plank” is a true partial descriptor, not its whole title. The table's `n/a` equality column is not proof of semantic accuracy. Existing links rewrapped by the patch were checked against the index and output; their unsupplied actual bodies were not reopened.

### All fifteen post-fix meaning and reading prompts

`confirm-packet/evidence/QuizBuilder.kt:21-37` builds by exact IDs, filters exclusions symmetrically against the target **and already chosen options**, deduplicates exact titles, tries curated cards first, then shuffled tag-sorted fallback. It does not restore excluded cards to fill slots, implement transitivity, understand synonyms, or independently discover semantic ambiguity. Its doc comment's “exactly one correct answer” is not a semantic guarantee from different title strings.

The complete `confirm-packet/checks/quiz-safety.txt:1-30` gives all 45 curated meaning options below. I compared their full displayed labels with each revised target and the complete same-commit index. None of these default choices is an established ordinary target meaning:

| Target / on prompt | Default curated meaning choices | Reading audit result and limits |
| --- | --- | --- |
| 娯 / ゴ | mistake; error / younger sister / strange; exquisite | 誤's ご is excluded; まい and みょう remain, with fallback. |
| 寮 / リョウ | observe; infer / polite; peaceful / proposal; draft plan | さつ, ねい, あん fill the modeled shipped-pool slots. |
| 廊 / ロウ | garden; yard / floor; bed / urban prefecture; administration | てい, しょう, ふ fill modeled shipped-pool slots; administration is not passage. |
| 栓 / セン | whole; complete / pine tree / village | The detailed output excludes ぜん and fills after しょう/そん. I do not infer attested セン/ゼン equivalence or the precise implementation from the audit's excluded-key count. |
| 汽 / キ | river; watercourse / pond; reservoir / sea, ocean | か, ち, かい are distinct from キ; water features are not steam. |
| 症 / ショウ | correct, proper / politics / floor; bed | Full listed candidates include ショウ; detailed audit skips it. Duplicate せい cannot fill two distinct wrong slots, so the bounded model reports fallback and outcome-dependent deficits. |
| 砲 / ホウ | wrap; enclose / sand / hard; stiff | 包's ほう is skipped; さ/しゃ and こう plus fallback remain. Archaic つつ is recognized in complete JMdict but absent from the new reading-options extra-reading list. |
| 碁 / ゴ | eye / sun, day / rice field | Curated alternatives もく/ぼく, にち/じつ, でん fill all three slots in modeled shipped/one-borrow pools. Fresh Daijisen verifies キ; the new reading-options audit incorrectly provides no inventory evidence for that extra reading, and cannot certify its absence. |
| 磁 / ジ | hard; stiff / polish; study closely / sand | こう, けん, さ/しゃ differ from ジ. Hardness/polishing/sand are not magnetism or porcelain. |
| 穀 / コク | palace; lord / throw / step; level | でん/てん, とう, だん/たん fill modeled slots. Classical たなつもの is independently verified but absent from the new audit's extra-reading inventory. |
| 穫 / カク | extent / autumn / department; course | てい, しゅう, か differ from カク; a season or department is not harvesting. |
| 糖 / トウ | rice grain / number / kind; category | All listed 米/数/類 readings differ from トウ; rice/count/category are not sugar. |
| 紺 / コン | crimson; deep red / pay; bestow / tie; join; conclude | こう/く, きゅう, けつ differ from コン; the whole red label is not navy blue. |
| 雰 / フン | minute, part / snow / clear skies | The detailed audit skips ふん and ぶん, retains ぶ and the 雪/晴 choices; random selected outcomes can still require fallback. |
| 魅 / ミ | not yet / younger sister / end; tip | The detailed audit skips 未's み but allows び; random outcomes can require fallback. These meaning labels do not imply charm or supernatural beings. |

All fifteen revised cards keep the sole sourced on-reading selected with a linked example and explicit `quizKunyomi: []`. The reopened KANJIDIC2 records and complete JMdict families support the core word allocations, including compound sound change in 鉄砲, different 石 readings in 磁石, long vowels and sense-local qualifications. This pass did **not** reread the linked word articles or complete C bodies outside the supplied twelve counterparts; dictionary entries, current target text, audited candidate readings/titles and the title index are the fresh evidence available here.

The short quiz-safety line “2/3” or “3/3” is not a full stochastic reading audit. For example 症's identical セイ alternatives reduce distinct outcomes, and 雰/魅 can lose a randomly selected matching alternative. The detailed exposure model records these deficits; I did not turn the short tally into three always-usable options.

`confirm-packet/checks/reading-options.txt:1-219` reports 100 seeds per prompt, no undersized sampled outputs and zero problems. It inspects a 1,221-card pool but lists only its chosen “best”/curated candidates, truncates lower-tier candidate displays, and has incomplete extra-reading inputs. In particular its “none” claims for 碁, 娯, 寮 and 糖 and its name-only entry for 穀 are not independent linguistic completeness checks. The other exposure report already includes supplemental card/JMdict readings, and this pass independently confirms 碁 キ and 穀 たなつもの. The new audit's zeros cannot erase that evidence.

`confirm-packet/checks/reading-exposure.txt:1-238` models N1/All pools of 1,221 cards, a 118-card Starter set plus the target, and the stated single additional holder check for 碁. It reports zero modeled hits in those pools and a latent キ collision in tiny hypothetical pools. This is not a new regression in this revision: no full readings, selected readings or curated distractors changed, and the supplied meaning builder's exclusions do not affect reading questions.

The reading-option source implementation, parser, normalization helpers, stack/session construction and Kotlin reading-quiz execution are **not** supplied. Static meaning-builder code and host reading models cannot establish custom/caller-built, multi-borrow Starter, changed/partial accepted-content, Kotlin RNG, native or phone behavior. Nor can they establish enforcement by installed APK `5c000bd`, which predates kanji exclusions.

### Mechanical checks and continuing initial limits

All ten revised logs were read; none was rerun. Lint/validation report zero errors; unittest reports 431 tests OK (`confirm-packet/checks/lint.txt:1-2`, `validate.txt:1`, `unittest.txt:1-3`). The manifest output reports 8,664 files and content version `c78ebbacf53520b6` (`manifest.txt:1-2`). Budget is a local estimate: 8,686 entries, 45,954,320 inflated bytes and 30,855,046 local-ZIP bytes (`budget.txt:1`), not an exact downloaded publication ZIP. Vocabulary remains 2,122/2,431 reviewed prompts, pilot (`vocabulary.txt:1`).

The author says the older quiz-safety/exposure logs are byte-identical. Their current supplied contents and hashes were read, but the original raw logs are outside this pass's allowed sources; I did not independently hash or directly compare those files. Current model evidence is not proof of device execution or linguistic correctness.

| Initial limit | Status established in this confirmation |
| --- | --- |
| L1 | The full same-commit index still has no 銃/棋/陶 entry, and the actual patch adds no card or pair for them. Complete dictionary families retain their lexical relationships. No nonexistent-card guard is requested. |
| L2 | Twelve counterpart bodies were supplied and read, including newly supplied 板. The other candidate/guard bodies named in the original report remain outside the input set. Their index labels are visible, not full semantic audits. No new corpus scan or extended selection was performed. |
| L3 | Fresh Daijisen verifies 穀's beans/classical-reading statements and 碁 キ, and re-establishes 魅's supernatural sense. No fresh 寮 heading, 娯 supplementary kun heading, 糖 あめ heading, 紺 shade heading or bare-砲 baseball heading was fetched. Those unchanged supplementary claims remain UNVERIFIED; complete JMdict supports the primary senses and preserves restrictions, not every supplemental character claim. In 2251080, `usu. 官,司` qualifies office/official usage, while the religious-officiant sense is explicitly restricted to 司; neither should be generalized into ordinary 寮 usage. |
| L4 | Exact modern kanjiapi/community-level membership, source-row/provenance attestation, raw SVGs, stroke JSON geometry, binary Joyo pages, full generated manifest and exact immutable GitHub ZIP verification are not fresh evidence in this pass. The reopened historical KANJIDIC2 JLPT fields do not certify current community membership. Packet identity/hashes are supplied bindings, not independently recomputed attestations. Publication counts and acceptance are not advanced by this confirmation. |
| L5 | The current bounded audits and supplied meaning builder are fresh inputs, not Kotlin/JVM/emulator/phone execution. Extra-reading completeness, custom/caller pools, multi-borrow Starter and old-client compatibility remain UNVERIFIED. No outcome on installed APK `5c000bd` is claimed. |
| L6 | This is the separately authorized one-phase confirmation. Earlier observations were not substituted for evidence: the entire initial report and relevant sources were reread through this chain. No other review, author ledger, observation/audit record, session history, other packet, source checkout, directory listing or temporary file was read. No extra review pass or implementation was begun. |

The original word articles, stroke data, Joyo extracts/PDF, raw SVGs, source metadata/provenance, remaining comparison cards and earlier raw checks were deliberately **not** opened in this pass, because the narrower chain-only assignment excludes them. Their absence is an evidence limit, not permission to rely on the initial report's old conclusions as a fresh certification.
