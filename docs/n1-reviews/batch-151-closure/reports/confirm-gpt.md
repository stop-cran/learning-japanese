Snapshot: `15441514ec9a0a3835921e2031f7d79bec6c8920`, compared with `b624890f8aea8cfb6b5a08ee6beff21df5f8c807`. Reviewer model: OpenAI GPT-family GitHub Copilot; the exact deployed model/version identifier is not exposed to me.

Scope:

- Read this packet's `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `evidence\README.md`, complete `diffs\fix.patch` and `diffs\changed-lines.txt`, and my complete `initial-gpt.md`. Read the original packet's complete `rubric\copilot-instructions.md` and `repo\docs\content-format.md:86–154`.
- Read all nine revised cards **in full**: 誓 誘 謙 譲 護 豆 豪 貢 貴. Assessed every hunk against correctness, scoped coverage, consistency/quiz safety and beginner comprehensibility, including its unchanged surrounding card.
- Checked all 15 cards' quiz metadata. Read all of `checks\quiz-safety.txt`, `checks\reading-exposure.txt`, `checks\reading-options.txt` and `checks\link-targets.tsv`. Independently reconstructed the 15 default meaning sets from target/distractor metadata, including symmetric target/distractor and distractor/distractor exclusions. All matched the supplied meaning options; no second correct meaning was established.
- Read complete `evidence\QuizBuilder.kt`, `evidence\KanjiReadings.kt:1–150` and `evidence\Words.kt:211–250`, covering the relevant option builders, normalization and mutations. Independently enumerated curated reading combinations from the actual cards, rather than accepting audit totals alone.
- Original-packet context: header/reading passages of 買 話 読 訪 呼 攻 舞 握; metadata of the remaining 29 distinct curated distractor cards; actual target headers for all 19 changed-line links. Consulted the word-title index for 護. The six unchanged batch cards received metadata/quiz review, not another full prose review.
- Read complete pinned JMdict entries 1266440, 1357030, 1213870, 1928100, 1450030, 1285520, 1282410, 1223520, 1381260, 1872960 and 1541900; relevant component/stroke passages of `kanjivg\08b19.svg` and `08cb4.svg`; complete `compound-sound-changes.md` and `distractor-trials.txt`.
- Inspected actual public [呼ぶ](https://jisho.org/api/v1/search/words?keyword=%E5%91%BC%E3%81%B6) and [譲る](https://jisho.org/api/v1/search/words?keyword=%E8%AD%B2%E3%82%8B) entries, both pinned-revision KanjiVG SVGs ([謙](https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/08b19.svg), [貴](https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/08cb4.svg)), and the [published sound-change article](https://raw.githubusercontent.com/stop-cran/learning-japanese/main/articles/compound-sound-changes.md). No search snippets were used as verification.

In-memory checks reconstructed every patched card exactly from the original text and supplied patch. All 15 snapshot Git blob IDs matched after LF normalization; the six unchanged cards matched the original text. All 19 changed-line link targets exist in the supplied context and have the reported titles.

Reading-option coverage:

| Card | Selected prompt | Minimum curated wrong slots |
|---|---|---|
| 訴 | うったえる | 3 |
| 証 | ショウ | 3 |
| 詩 | シ | 2; fallback required |
| 詳 | くわしい | 3 |
| 誇 | ほこる | 3 |
| 誓 | ちかう | 3 |
| 誘 | さそう | 3 |
| 謙 | ケン | 3 |
| 謡 | ヨウ | 2; fallback required |
| 譲 | ゆずる | 3 |
| 護 | ゴ | 2; fallback required |
| 豆 | まめ | 3 |
| 豪 | ゴウ | 3 |
| 貢 | コウ | 2; fallback required |
| 貴 | キ | 3 |

These are full-pool curated-slot results, not claims that every curated card belongs to Starter. For the four fallback-dependent prompts, the supplied candidate tiers and exposure results establish no additional valid answer among the inspected candidates.

Dispositions:

- G1 - RESOLVED - `誘.md:14,45,51,59` removes 訪, counts 13 exclusions, and replaces the ambiguous shared-English-word justification with 呼ぶ's actual third sense, “to invite.” Pinned entry 1266440, the actual 呼 card and the live entry agree. Visiting and inviting remain distinct. Meaning choices still fill from 攻/舞/握. Reading choices are unchanged: exclusions are not consulted by `KanjiReadingQuiz`; these distractors supply せめる, まう/まい and にぎる, not 誘's readings.
- G2 - RESOLVED - `譲.md:13,57` now supplies the commercially related opposite 買 and the recognizable 言-family contrasts 話/読. Their actual titles—“buy,” “talk, speak,” “read”—are wrong for handing over/yielding; none is excluded. JMdict 1357030 and the live entry support the selling comparison. Their selected kun readings independently produce exactly two three-option combinations: かう + はなす/はなし + よむ. All three cards are Starter members, so these slots also fill when Starter borrows 譲, without reaching fallback せめる. The revised set satisfies the original plausibility concern without creating a demonstrated reading collision.
- GO1 - DECLINE ACCEPTED - Retaining the longer Notes is acceptable: shortening was nonblocking polish, not a correctness requirement. The separate wording improvement was applied consistently at all eight specified occurrences across 護/豆/豪/貢/貴; “example word” is clearer and does not change the supported claims.
- GO2 - DECLINE ACCEPTED - 護 explicitly labels 看護婦 obsolete, identifies 看護師 as current, and supplies 保護 as another example. Pinned entries 1213870/1928100 confirm the distinction. The supplied word-title index contains only 看護婦 among articles containing 護; retaining its valid ゴ evidence does not require inventing a new article.
- L1 - RESOLVED - The previously unavailable article is now supplied and independently reachable publicly. Its content explains the relevant compound-voicing principle without claiming universal predictability. Its LF-normalized Git blob is `6d5e1f06fba93f5db9b3a518fd21ec854abe5f11`, matching the stated identity. The earlier packet-access limitation is removed; no card edit is required.

Verdicts:

- Correctness - CLEAN for all nine revised cards and all changed hunks; no differing card. 謙's added horizontal and final sweeps match strokes 10 and 16–17; 貴's added horizontal matches stroke 5. 誓's reordered rows preserve their supported readings and qualifications.
- Scoped coverage - CLEAN within the confirmation scope; no differing card. No changed passage removes necessary reading evidence, qualifications or learner distinctions.
- Consistency and quiz safety - CLEAN within the inspected default choices and supplied pool analyses for all 15 cards; no differing card. G1/G2 and the article-navigation limitation are closed.
- Comprehensibility - CLEAN for the revised cards; no differing card. Shape descriptions remain explicitly mnemonic, not etymological, and the wording replacements improve clarity.

Confirmation: CONFIRMED - Every response item is RESOLVED or DECLINE ACCEPTED, and no new actionable defect was established.

Findings: none.

Optional: none new.

Limits:

- Audit success does not prove linguistic correctness, distractor plausibility, exhaustive dictionary coverage or learner effectiveness. The meaning builder deduplicates titles, not senses. The reading builder protects metadata readings and their mutations, not every reading mentioned in prose or an external dictionary.
- The three reported latent collisions remain 詳/よし, 譲/せめる and 貴/ぎ. They are not reported as drawable in the inspected shipped pools. 豆/ま and 豪/ご are name-only readings, not additional correct answers to the respective kun/on prompts. This revision introduces no established regression.
- I independently checked curated combinations and the changed cards' Starter membership, but did not rebuild the entire 1,517-card pool or independently verify stack-construction code. Fallback reachability outside the inspected curated sets relies on the supplied analyses. Finite seed simulations are not proofs for arbitrary pools, future content, multiple borrowed-card combinations or changed clients; some declared fallback candidates were not observed in the sampled seeds.
- No Android/JVM execution, device rendering, learner trial or fresh official-Joyo-PDF inspection was performed. Unchanged articles and stroke data were not re-reviewed wholesale. The trial log corroborates the author's account but is not an independently rerun experiment.
- Exact byte hashes initially differed for CRLF-exported 詳/謡 and the sound-change article; LF normalization resolves those differences. This is not a content defect or a claim of byte-identical exports. Some oversized combined reads exceeded the tool output limit; relevant material was subsequently retrieved in bounded reads, and generated output paths were not opened.
- All investigative responses used exactly one tool call, serially. No parallel calls, subagents, background jobs, other sessions, recursive listings, corpus scans, other reviewer reports or unauthorized local paths were used. The only intentional file creation/change is this report.
