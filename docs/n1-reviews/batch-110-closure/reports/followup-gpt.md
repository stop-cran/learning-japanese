Snapshot: `10d7965266b69ed81703ab69f20cff873a0526e9`, unchanged revised content. Android source examined: `10d98d0db61dcde621463460e6a1e59941b4042b`, public repository `stop-cran/kanji-cards-android`. Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`.

Scope:

This is the focused F1/L1 follow-up, not a third full linguistic review. No other reviewer's report was consulted. The author's statements and generated outputs were checked against primary sources and independent, read-only reconstructions.

Path abbreviations:

- **F** = `C:\Users\stop-\n1-kanji-workspace\review-packets\followup-110-10d79652-gpt`
- **C** = `C:\Users\stop-\n1-kanji-workspace\review-packets\confirm-110-10d79652-gpt`
- **O** = `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714`
- **A** = `F\evidence\android\app\src\main\java\io\github\stopcran\kanji`
- **K** = `F\evidence\android\core\src\main\kotlin\io\github\stopcran\kanji\core`
- **T** = the explicitly named characters `張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖`.

Files actually opened in this round and depth:

- `F\INSTRUCTIONS.md`, `F\RESPONSE.md`, `F\evidence\README.md`: full.
- `F\evidence\android\SOURCES.tsv`, `call-sites.txt`, `routes.txt`, `compare-5c000bd-to-10d98d0d.txt`: full. `compare-5c000bd-to-10d98d0d.patch`: parts, lines 1-120, 370-451 and 650-755, plus its hunk-header index.
- `F\evidence\cards-reading-metadata.tsv`: full programmatic parsing for pool construction and targeted source-level checks; opening rows also inspected as text. No content-directory scan was performed.
- `F\evidence\jmdict-cited-entries.xml`: full, both entries.
- `A\ui\KanjiReadingViewModel.kt`, `A\ui\KanjiReadingScreen.kt`, `A\data\ReadingData.kt`, `A\data\Padding.kt`, `A\data\SrsMapping.kt`: full.
- `A\data\Database.kt`: lines 530-575. `A\data\KanjiReviews.kt`: lines 80 through EOF. `A\MainActivity.kt`: lines 354-418. `A\ui\DrawViewModel.kt`: lines 195-210. `A\ui\QuizViewModel.kt`: lines 122-136.
- `K\srs\Stacks.kt`, `K\srs\PracticePadding.kt`, `K\focus\FocusBatch.kt`: full. `K\reading\KanjiReadings.kt`: text through line 160, and complete bytes for public-source authentication. `K\words\Words.kt`: lines 150-242.
- `F\evidence\android\core\src\test\kotlin\io\github\stopcran\kanji\core\KanjiReadingsTest.kt`: lines 207 through EOF.
- `F\evidence\tools\ScratchReadingExposureTest.kt.txt`, `reading_exposure.py`, `reading_exposure_crosscheck.py`: full. `reading_options.py`: through line 180. These were inspected as method descriptions, not executed.
- `F\checks\reading-exposure.txt`: text at lines 160-197 and 315-349; complete file mechanically parsed to recount the reported exploratory hits. `kotlin-reading-run.txt`: text at lines 40-55 and 78-110; complete file mechanically checked. `kotlin-starter-run.txt`: text at lines 1-40; complete file mechanically checked. `kotlin-vs-exact.txt`: full.
- `F\snapshot\kanji\嫌.md`: full text. Every `F\snapshot\kanji\<T>.md` and corresponding `C\snapshot\kanji\<T>.md`: complete bytes compared; all 15 pairs identical. This byte check was not a fresh linguistic review of the other 14 cards.
- `O\evidence\public-source\weblio-嫌.txt`: full.
- My own `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\confirm-gpt.md`: full. The initial report was not reopened.

Independent public checks: the actual [Digital Daijisen 嫌 page](https://www.weblio.jp/content/%E5%AB%8C), specifically the character entry and `や【▽嫌／×厭】`; the pinned public Android ViewModel and reading-builder files, authenticated byte-for-byte against the packet; and Kotlin's public [XorWowRandom](https://raw.githubusercontent.com/JetBrains/kotlin/v1.9.0/libraries/stdlib/src/kotlin/random/XorWowRandom.kt) and [Random](https://raw.githubusercontent.com/JetBrains/kotlin/v1.9.0/libraries/stdlib/src/kotlin/random/Random.kt) sources for independent seeded reproduction. The authenticated Android SHA-256 values were `92a90bce8b6b8dcf292090086bb53455c8952ca8076cb1a873bf4e3be9e7bb76` and `0632fcbb014d8644fcf1ab8fe0bd7b22d89df70a4b6e3c4d0838b129f76e4d74`, respectively.

Dispositions:

- F1 - **DECLINE REJECTED** - The corrected explanation establishes a real production wrong-grading path; documentation and an unimplemented client proposal do not protect its answers. I would accept this temporary content mitigation for the pinned client: remove only `いや` from `quizKunyomi`, leaving `[きら.う, きら.い]`, and update the practice-selection paragraph accordingly. Preserve `kunyomi: [きら.う, きら.い, いや]`, the いや teaching row, and its vocabulary coverage. The remaining scheduled kun prompt is きらう because the two retained entries share a stem. This changes a curated practice subset, not the frozen KANJIDIC2 source record. The hypothetical `[嫌, 屋]` collision for きらう does not invalidate this mitigation for the actual pinned production pools. An implemented, regression-tested client exclusion for the attested contraction is the better permanent alternative.
- L1 - **RESOLVED as a bounded evidence/audit limitation** - The missing や attestation and actual caller/pool mechanics are now established, including smaller-pool and padded-production cases. I withdraw my confirmation report's “smaller studied pool” characterization: study state selects questions, not the ordinary answer-option pool. This resolution does not certify every dictionary attestation, every borrowed-card combination or an installed APK; the bounds below remain explicit. C4/C5 require source-description corrections, and the extra borrowed-card witnesses below correct one over-restrictive production condition.
- L3 - **Accepted, disclosed nonblocking limit** - The prior text-extract corroboration stands, as does the confirmation round's visual check of the shape-dependent 器 claim. No new contradiction makes independent visual inspection of every original PDF page necessary for this focused confirmation. I do not claim that inspection occurred.

Verdicts:

Consistency and quiz safety: **NEEDS FIX** - F1 remains exposed in a production reading session.

The other three confirmation facets stand: correctness, scoped coverage and comprehensibility remain **CLEAN within their previously reviewed content scope**. The C5 error below is in the author's verification response, not a newly changed teaching passage.

Claims:

- C1 - **VERIFIED** - Opened VM, RD, SRS, ST and the metadata TSV. VM:83-95 passes the entire `content.inStack(stack)` list to `readingData`, which maps every card, without a studied-only filter. `Stacks.includes` includes the selected JLPT level through N5. Independent TSV parsing found 1,161 unique cards, exactly one JLPT tag each, with N1/N2/N3/N4/N5 counts 170/374/371/166/80. Both N1 and All therefore supply 1,161 option-pool cards.
- C2 - **VERIFIED within the supplied production call-site inventory** - Opened `call-sites.txt`, VM, KRV, FB, WD, PAD, DrawViewModel and QuizViewModel. VM:151 is the displayed kanji-reading builder call. KRV:114-120 and FB:25 only test availability with `Random(0)` and a null check. The word, drawing and meaning paths are different exercises. This is not a new independent grep of a complete Android checkout.
- C3 - **VERIFIED** - Opened VM:78-159, PAD, DB:530-575, RD, ST, PP and the route sources. Only an extra/“Practice more” session with fewer than `max(10, focusSize)` ordinary items attempts padding. All and every JLPT stack return no padding candidates. Starter can borrow started readings of the same source/mode from another non-All stack, outside Starter; VM additionally checks that the reading remains an actual `quizKey`. It appends each borrowed kanji's entire ReadingCard to the 118-card Starter option pool. Ranking is not strictly raw retrievability: PP also applies the similarity boost and random jitter.
- C4 - **WRONG as worded** - Opened KR:46-116 and WD:209-238. The exclusion and three-stage option mechanism are otherwise correctly described, but the variant-length filter applies to the generated result, not to the input. A one-kana input can generate a retained two-kana variant: `mutations("お")` yields `おう`. This correction does not change 嫌's seven excluded keys.
- C5 - **WRONG as worded; the consequential や attestation is VERIFIED** - Opened the complete JMdict entries, 嫌 card, saved Daijisen extract and live Daijisen entry. JMdict 1587610 permits いや and や for the kanji spelling, but its イヤ reading has `re_nokanji`; all three cannot unqualifiedly be attributed as readings of that spelling. Daijisen independently identifies や as the sound-change form of いや, including adjectival uses. や is absent from the preserved card metadata.
- C6 - **VERIFIED** - Opened KR and both metadata rows; independently reconstructed the result. For `[嫌, 屋]`, Kun, `reading=いや`, the exclusion set is exactly `{いや, きらい, きらう, ぎらい, ぎらう, けん, げん}`. None of 兼/験/好 is present. 屋 contributes only や, which survives exclusion, so the builder returns the two options や and いや, shuffled, accepting only いや. Replacing the prompt with きらう produces the same wrong option. This is deterministic for every seed, hence also the reported 400/400 cases; it is not itself a shipped stack.
- C7 - **VERIFIED at source and supplied-run comparison level** - Opened RUN-N:44-51, RX:160-197, KR and metadata. Independent reachability reconstruction gives 55/9/9 wrong keys for ゲン/きらう/いや in both 1,161-card pools, none や. For ゲン, 兼/験 contribute excluded keys; 好 supplies こう, leaving two fallback slots filled by higher-scoring readings than や. For each kun prompt, all three curated cards supply distinct safe choices, filling the slots before fallback. The supplied 4,000-seed records agree and report four options, no nulls and no bad correct answers. I did not independently rerun the Kotlin harness.
- C8 - **VERIFIED for its explicitly specified pool** - Opened RUN-S, RX, KR, VM and metadata. Independently counted 118 Starter cards and reconstructed the 119-card pool with 嫌 alone: 24/10/9 wrong keys, with や only for いや. Its top-tier keys are `いき, いきる, いく, いつ, いでる, いぬ, いま, いる, や`. An independent in-memory implementation of the primary algorithm and Kotlin seeded PRNG reproduced every reported frequency for all three 嫌 prompts across seeds 0-3999, including や exactly 1,310 times. This is not an app-wide occurrence probability. Further borrowing can retain the exposure even when one or two curated cards are present; see finding 1.
- C9 - **VERIFIED** - Opened RUN-N:85-102, KR and the named TSV rows. Independent source reconstruction confirms kun や donors 屋/家/八 and on や donors 夜/冶/野 in these hypothetical two-card pools. With 冶, neither kun prompt has any wrong candidate, so the builder returns null for every seed. The source distinguishes these tiny-pool cases from actual shipped-stack exposure.
- C10 - **VERIFIED** - Opened RX:163-196, its inventory method, JMdict 1587610 and the live Daijisen entry. RX:167-168 now includes や with the correct JMdict identity; the original omission is corrected. This is verification of the identified inventory repair, not completeness of all possible attestations.
- C11 - **NOT VERIFIED as an independently reproduced corpus result** - Opened RX:315-349 and the complete scan/inventory method. Mechanical recount confirms 19 reported whole-stack lines, nine distinct prompts on eight cards, and 13 reported padded-session lines including 嫌. The complete dictionary/cache inputs needed to reproduce and linguistically validate that exploratory scan are not supplied here, and a fresh corpus scan is outside the mandate. These remain untriaged leads, not 32 established content defects and not evidence for accepting F1.
- C12 - **NOT VERIFIED in full** - Opened the supplied old/new comparison text and relevant patch hunks. They support the stated technical distinction: unchanged option-building sections, older exact-level rather than cumulative pools, and older JLPT padding permission. They do not establish which APK was last requested, built, copied, installed or currently runs on the phone. The claimed `2edbf36` historical boundary was not independently authenticated in this round. No safety conclusion about that older client is made.
- C13 - **VERIFIED as a bounded comparison of the supplied run files** - Opened XC, the scratch-test source, both complete run files mechanically, the analysis methods, metadata and primary builder/mutation sources. An independent source-based reconstruction checked all 52 whole-stack, 26 Starter and 32 small-pool cases, all 30 printed exclusion sets, option-count/frequency accounting and membership in the reachable sets: no mismatch. It independently reproduced exactly four superset-but-undrawn cases: 嫌+八/きらう/やっつ, 嫌+八/いや/よう, 張+割/はる/さく, 基+供/き/ぐ. XC's zero whole-stack HITs and one Starter PAD-HIT are relative to its inventory; PAD-HITs are deliberately not counted in its “0 problems” total. Neither that total nor deepest-fallback overapproximation proves linguistic safety.

Confirmation: **NEEDS FIX** - The evidence narrows and corrects the explanation, but does not fix F1. This replaces the previous Confirmation line; the prior content dispositions otherwise stand, with the L1/L3 statements above supplying this round's requested qualifications.

Findings:

1. **Minor - consistency and quiz safety; over-restrictive production preconditions.** `F\RESPONSE.md:87-96`, especially line 95; primary evidence `A\ui\KanjiReadingViewModel.kt:109-133` and `K\reading\KanjiReadings.kt:98-112`.

   **Claim and impact:** Absence of all three curated cards is presented among conditions required “all together.” That is too restrictive. A short Starter session can borrow both 嫌 and 兼, or 嫌/兼/験, while still offering や for いや. One or two filled curated slots do not suppress the remaining fallback slots.

   **Independent witnesses:** For the 118 Starter cards plus 嫌 and 兼, the source port with Kotlin `Random(2)` selects wrong keys `{かねる, いでる, や}`. With 嫌, 兼 and 験 added, `Random(15)` selects `{かねる, ためし, や}`. The correct key is いや in both cases. These pool additions are permitted by the same padding path: sufficient padding slots and eligible started foreign readings can supply both/all three kanji. No hypothetical custom stack is needed.

   **Remedy:** Describe the no-curated-card pool as a sufficient example, not a necessary condition. Record that exposure can survive one or two curated cards; all three usable curated choices are what eliminate kun fallback here. Retain the disclosure that arbitrary multiple-borrower combinations were not enumerated.

   **Confidence:** High for source reachability; no claim of a witnessed device session or exposure frequency. This corrects the author's new narrowing, rather than re-reporting unchanged F1 as a new defect.

2. **Minor - correctness of source interpretation.** `F\RESPONSE.md:193-194`; evidence `K\words\Words.kt:222-238`.

   **Claim and impact:** “Variants of one-kana readings are not generated” confuses input length with output length and misstates a boundary of the safety mechanism. For input お, the long-vowel insertion produces おう, which passes `length >= 2`.

   **Remedy:** Say that generated one-kana results are discarded, while one-kana inputs can still produce longer retained variants. The independent reconstruction confirmed this counterexample. No 嫌 card edit or changed reachability count follows from this correction.

   **Confidence:** High.

3. **Minor - correctness of dictionary attribution.** `F\RESPONSE.md:198-200`; evidence `F\evidence\jmdict-cited-entries.xml:22-29`.

   **Claim and impact:** イヤ belongs to the JMdict entry but is explicitly kana-only (`re_nokanji`), not an unrestricted reading of its 嫌 spelling. Ignoring that distinction overstates what the cited entry proves.

   **Remedy:** Attribute いや and や to the kanji spelling, and identify イヤ separately as the kana-only entry reading. The や attestation, F1 and all independently reproduced 嫌 counts remain intact.

   **Confidence:** High. This is a response correction, not a new defect in the unchanged card's teaching prose.

Optional: None.

Limits:

- This review establishes source-level production reachability, not an installed-phone reproduction. No APK, emulator, UI session or compiler/test-harness execution was used. The seeded independent port exactly matched the supplied 嫌 Starter histograms; that does not authenticate the provenance of every supplied run or the installed runtime.
- The temporary quiz-selection mitigation is accepted for the pinned client's actual content/pool construction, not as universal protection for arbitrary future pools or the unverified older phone build. Preserve the full source readings and teaching coverage. A meaning `quiz_exclusions` edge does not fix reading options.
- An unimplemented client proposal is not protection. A data-driven additional-attested-reading exclusion is the clearer permanent mechanism; a prefix/suffix heuristic can catch this contraction but is not a complete linguistic inventory.
- C11 remains independently unverified beyond output recount and method inspection. Dictionary completeness, every possible multiple-borrower state, the complete Android repository's call-site inventory and actual installed-build identity are not certified. The new witnesses do not purport to enumerate all such states.
- L3 remains an accepted disclosure: the original official PDF was not independently visually inspected in full. Earlier text corroboration and the confirmation round's supplied-image inspection are not being relabelled as full original-PDF verification.
- Snapshot commit identity/ancestry are taken from the packet. All 15 supplied card pairs were independently byte-compared. No other content, stroke or word article was reopened for a new full review, and no content or client file was edited.
- One oversized web-fetch response was automatically spooled by the tool; its local output file was not opened. The dictionary passage was instead verified through a subsequent bounded URL fetch.
