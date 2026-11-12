Snapshot: `30f2bd7c7b57e0d244a1cb86ba51e5b86121d4f8`, compared with `10d7965266b69ed81703ab69f20cff873a0526e9`. Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`. Client conclusions concern Android commit `10d98d0db61dcde621463460e6a1e59941b4042b`.

Scope:

Focused delta review of 嫌 and the manifest patch, including the author's response corrections. No other reviewer's report was consulted.

Path abbreviations:

- **D** = `C:\Users\stop-\n1-kanji-workspace\review-packets\confirm-110-30f2bd7c-gpt`
- **F** = `C:\Users\stop-\n1-kanji-workspace\review-packets\followup-110-10d79652-gpt`
- **C** = `C:\Users\stop-\n1-kanji-workspace\review-packets\confirm-110-10d79652-gpt`
- **O** = `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714`
- **A** = `F\evidence\android\app\src\main\java\io\github\stopcran\kanji`
- **K** = `F\evidence\android\core\src\main\kotlin\io\github\stopcran\kanji\core`
- **T** = the explicitly named cards `張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖`.

Files opened and depth:

- `D\INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `evidence\README.md`, `snapshot-identity.txt`, `packet-manifest.json`: full.
- `D\diffs\delta.patch`, `manifest-delta.patch`, `changed-files.txt`, `changed-lines.txt`, `checks-vs-followup.diff`, `reading-options-vs-confirm.diff`: full. Independently reconstructed the complete card diff and applied all five check-output comparisons in memory; they match their actual old/new files.
- `D\snapshot\kanji\嫌.md`: full linguistic review, including untouched surrounding text. Every `D\snapshot\kanji\<T>.md` and `F\snapshot\kanji\<T>.md`: complete bytes for comparison, normalized hashes and git-blob calculations. The other 14 cards are byte-identical; they were not linguistically re-reviewed.
- `D\evidence\cards-reading-metadata.tsv` and `F\evidence\cards-reading-metadata.tsv`: full programmatic parsing and row comparison. Only 嫌's `ask-kun` field differs. No corpus-directory scan was performed.
- `D\evidence\jmdict-cited-entries.xml`: full linguistic/source inspection; the complete bytes of the F copy were also compared and are identical.
- `A\data\ReadingData.kt`, `A\data\Padding.kt`, `K\srs\Stacks.kt`: full. `A\ui\KanjiReadingViewModel.kt`: lines 78-154; `A\data\SrsMapping.kt`: lines 30-45; `K\reading\KanjiReadings.kt`: lines 18-205; `K\words\Words.kt`: lines 209-240. Complete ViewModel and KanjiReadings bytes were additionally hashed against the values independently authenticated in the follow-up round; both match.
- `F\evidence\tools\reading_exposure.py`, `reading_options.py`, `reading_exposure_crosscheck.py`, `ScratchReadingExposureTest.kt.txt`: complete bytes for comparison with the four recorded tool hashes, not a fresh semantic review or execution.
- Under `D\checks\`, these files were opened completely for mechanical comparison, integrity checks or log inspection: `budget.txt`, `gradle-kotlin-reading.txt`, `gradle-kotlin-starter.txt`, `jvm.txt`, `jvm-readings.txt`, `kotlin-reading-run.txt`, `kotlin-starter-run.txt`, `kotlin-vs-exact.txt`, `link-targets.tsv`, `lint.txt`, `manifest.txt`, `quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`, `summary.txt`, `unittest.txt`, `validate.txt`, `vocabulary.txt`. In particular, RO lines 159-180, RX lines 163-188, the six retained 嫌 run records and the final crosscheck totals were inspected directly.
- `F\checks\reading-exposure.txt`, `kotlin-reading-run.txt`, `kotlin-starter-run.txt`, `kotlin-vs-exact.txt`, and `C\checks\reading-options.txt`: complete text for in-memory diff verification, not fresh linguistic assessment of every reported option.
- `O\repo\docs\content-format.md`: lines 105-150. `O\evidence\kanjidic2-records.xml`: lines 324-393. `O\evidence\public-source\weblio-嫌.txt`: full.
- These specifically named files under `O\repo\words\`: `機嫌.md`, `嫌う.md`, `嫌い.md`, `好き嫌い.md`, `嫌.md`, `嫌がる.md`: front matter only, for retained link identities and titles.
- My own `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\followup-gpt.md`: lines 35 through EOF. The initial and confirmation reports were not reopened.

Independent public verification inspected the actual [Digital Daijisen 嫌 page](https://www.weblio.jp/content/%E5%AB%8C), specifically the character entry and `や【▽嫌／×厭】`, through a bounded URL fetch, not a search snippet.

Dispositions:

- F1 - **RESOLVED** - The exact accepted mitigation is present at `嫌.md:12,37,43-45`: only いや was removed from `quizKunyomi`; the full source readings, teaching row and vocabulary remain. The two remaining screen prompts are protected against や in every production pool constructible from this snapshot by the pinned client, including arbitrary additional Starter borrowers. This resolves the scoped finding by content selection, not by claiming that the underlying client exclusion mechanism was repaired.
- FU1 - **RESOLVED** - RESPONSE D2 correctly withdraws the requirement that all three curated cards be absent. One or two filled curated slots can leave fallback exposure for the former いや prompt; absence of all three was only a sufficient example. Its replacement argument for the retained prompts is independently valid, rather than relying on that withdrawn precondition.
- FU2 - **RESOLVED** - RESPONSE D3 correctly distinguishes input length from generated-result length. `Words.kt:226-238` retains おう from one-kana input お. 嫌's metadata inputs and seven excluded keys remain unchanged; safety here is not being attributed to an exclusion of や.
- FU3 - **RESOLVED** - RESPONSE D4 correctly preserves the distinction in JMdict 1587610: いや and や are unrestricted readings of the kanji spellings; イヤ carries `re_nokanji` and is kana-only. The revised card relies only on the genuinely attested や spelling/reading pair.

Verdicts:

Correctness: **CLEAN** - The changed source-selection statements and contraction explanation are supported; the normalized card hash matches the manifest entry.

Scoped coverage: **CLEAN** - Complete KANJIDIC2 readings and いや vocabulary coverage remain. Removing one practice selection does not erase or mischaracterize the reading.

Consistency and quiz safety: **CLEAN for this delta and pinned client/content combination** - No contradictory current selection statement remains, and や cannot enter either retained production prompt. Titles, meaning distractors and meaning exclusions are unchanged.

Comprehensibility: **CLEAN** - The explanation first says that いや is not selected, gives the reason, then explicitly avoids calling it invalid, obsolete or rare. The revised selection paragraph and added explanation contain 39 and 62 whitespace-separated words respectively. “Wrong option” is understandable in context; replacing it with “wrong answer” is not required.

Earlier verdicts for unchanged material stand.

Claims:

- N1 - **VERIFIED within the supplied snapshot/diff evidence** - Opened both patches, change inventories, identity files and old/new card bytes. Independent complete-text comparison gives exactly five inserted and three deleted card lines, plus two inserted/two deleted manifest lines: seven/five in two files. All other 14 supplied cards are byte-identical, and their normalized blob IDs match the records. The complete repository-wide change inventory and parentage remain packet-provided, not independently authenticated against a checkout.
- N2 - **VERIFIED** - Compared complete old/new front matter, DP, FMT and my prior mitigation. The only changed front-matter key is `quizKunyomi`, now `[きら.う, きら.い]`, preserving order and exact membership in the unchanged full list. `quizOnyomi`, title, tags, distractors and exclusions are untouched.
- N3 - **VERIFIED** - Opened the complete card, FMT, link records and the six named word targets' front matter. Every selected raw reading retains its table row and existing linked example. All card link targets are unchanged. The two changed-row links resolve to the stated titles. Independently located all occurrences of いや at lines 10, 23, 25, 37, 39, 41, 45, 53 and 54: none still claims it is selected. Lines 37/45 explicitly withdraw selection; line 41 teaches its legitimate Joyo status, which is not contradictory. The lint/validation records contain the stated outcomes.
- N4 - **VERIFIED** - By hand from CARD, RD and KR: `askOn=[ゲン]`; `askKun=[きら.う,きら.い]`. Both kun entries have stem きら, so ordered stem deduplication retains きら.う only. The available screen prompt keys are therefore on `げん` and kun `きらう`, not `きらい` or `いや`. VM passes the queued key explicitly. Normal/extra eligibility starts from current `quizKeys`, and padding also checks those keys; even saved progress for いや does not reintroduce it. Independent metadata reconstruction gives 25 batch prompts. Full-source exclusion remains `{いや,きらい,きらう,ぎらい,ぎらう,けん,げん}`.
- N5 - **VERIFIED at source and supplied-record level** - Opened both run files, RO, RX, XC, their complete actual diffs and the primary sources. All six retained 嫌 records have 4,000 seeds, no null/bad-correct result, four options and no や. Distinct wrong-key counts are 55/9 in each full pool and 24/10 in Starter+嫌. The retained histograms are unchanged from the earlier records; only the withdrawn prompt's records disappear. The impossibility conclusion additionally follows from N6's source proof, not merely from sampling. No new Kotlin harness execution is claimed.
- N6 - **VERIFIED** - Opened metadata, KR, VM, RD, SRS mapping, ST and PAD. 嫌 is N1-only and not Starter-tagged; the only applicable displayed pools are N1/All, each containing all 1,161 cards, or the 118 Starter cards plus borrowed cards. All contain the full Starter base. Independently reconstructed first-best fallback candidates: for `げん`, Starter has 25 distinct score-3 keys, minus excluded `けん`, leaving 24; for `きらう`, it has ten safe score-3 keys: `あう おう おこなう かう かたらう きく きた きたる くう よう`. や scores only 2 against `げん` and 0 against `きらう`. Its only on donors are 冶/夜/野; kun donors are 八/家/屋. 八's best kun candidate is よう, not や; 家's is いえ; 屋's is や. Curated 兼/験/好 never contribute や. If curated selection has already added `j` distinct keys, with `j <= 3`, at least `24-j` or `10-j` superior Starter keys remain for only `3-j` slots. Thus the sorted fallback fills all slots before や's tier, and final fallback cannot add anything. Borrowing only adds cards and cannot remove these base candidates. This proves protection for every additive Starter pool, including multiple borrowers, and for N1/All; it does not require enumerating subsets.
- N7 - **VERIFIED** - Opened metadata, KR and the small-pool run records. By hand, `[嫌,屋]` with kun きらう still yields the sole wrong key や; `[嫌,夜]` or `[嫌,冶]` with on ゲン similarly permits や. 冶 supplies no kun candidate, so that kun two-card case returns null. These artificial pools lack the invariant Starter base and are not constructible shipped pools here. This correctly distinguishes the accepted mitigation from universal protection.
- N8 - **VERIFIED for the card's substantive assertions and learner framing** - Checked JMdict 1587610, the KANJIDIC2 record, saved/live Daijisen and the earlier source-level exposure. や is attested for 嫌, Daijisen calls it a sound change of いや, and the pinned KANJIDIC2 record lacks it. The conditional statement about a question on いや explains why it was withdrawn; it does not say that the revised screen still asks it. Keeping “wrong option” is acceptable: it describes the role the quiz would assign, not a dictionary judgment. The incidental whole-tree phrase-frequency claims were not independently checked and are unnecessary to this wording decision.
- N9 - **VERIFIED for the exact manifest delta and card hash** - Opened MP, identity records and raw old/new card bytes. `raw.replace(b"\r\n", b"\n")` converts the new 5,800-byte CRLF file to 5,736 LF bytes. Their SHA-256 is `033867582ec3df45d00a0311caf74d0594c22bfb8ff7f18428ed82ac94842312`, exactly the manifest `+` entry. The resulting git blob ID is `52a73a70028b01a97295820ff08eb78ee7487287`. The old normalized hash also matches its `-` entry. The patch changes only that entry and `contentVersion`, from `eb332dd7994dd3ba` to `18d0f3df4071aa30`. The complete content-version derivation was not independently rebuilt.
- N10 - **NOT VERIFIED as independent gate execution** - Opened every named gate log and checked the recorded outcomes against CHG: six summary exits are zero, lint has zero errors/17 existing word warnings, 431 tests are reported OK, validation and quiz safety report zero errors, vocabulary is 2122/2431, manifest reports the stated version, and all four Gradle logs report BUILD SUCCESSFUL. These records are internally consistent, but their execution was not independently rerun or authenticated from test artifacts. The necessary checkout, gate tools and complete inputs are not supplied/permitted. The direct card, hash, selection and all-production-pool checks above do not depend on assuming that execution.

Confirmation: **CONFIRMED** - F1's accepted content mitigation is implemented and independently established to protect both remaining prompts in the pinned client's production pools. FU1-FU3 are resolved, and no new actionable defect was established in this delta. This replaces the Confirmation line of the follow-up report; unchanged review results otherwise stand.

Findings: None.

Optional: No required wording polish; retaining “wrong option” is acceptable.

Limits:

- Confirmation is of this content delta with the pinned compatible Android source, not a physical-phone, APK-installation or general-release certification. Older clients that ignore `quizKunyomi` are not protected by this selection change; their installed identity and behavior remain unverified.
- N10's actual gate execution is not independently verified. Supplied logs were inspected and compared, not substituted for source-level reasoning. No APK, emulator, UI session, Gradle build or author script was run.
- Full manifest rebuilding/content-version calculation, complete git-tree provenance/ancestry and the claimed previous-publication history at `20f0db4c` were not independently verified. Normalized card SHA-256, git blob IDs, supplied patch completeness for the card, and the other 14 packet-card comparisons were independently checked.
- No complete linguistic inventory of all readings, corpus-wide phrase count or triage of the exploratory scan's other-card leads was attempted. The N6 proof concerns や for 嫌's two actual prompts with this fixed snapshot's metadata, normal four-option builder and constructible pools, not arbitrary future content or artificial tiny pools.
- Original word articles were used only as named link context. Unchanged teaching material, word/stroke reviews and previously disclosed review limits were not reopened. No content or client file was edited.
