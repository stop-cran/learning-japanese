Snapshot: `10d7965266b69ed81703ab69f20cff873a0526e9`, compared with `453af714d56aa573204d477ff863cb4da756b4c3`. Reviewer: **GPT-6.1 Sol**, model ID `gpt-6.1-sol`.

Scope:

Independently reviewed every changed hunk and the complete revised articles, with particular attention to quiz safety and beginner-phone comprehensibility. No other reviewer's report was consulted. The author's response was treated as claims, not proof.

The explicit character set **K** is:

```text
張 器 素 応 仮 基 価 激 嫌 縮 騒 統 級 整 暖
```

Confirmation-packet paths below are relative to `C:\Users\stop-\n1-kanji-workspace\review-packets\confirm-110-10d79652-gpt`.

- `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `evidence\README.md`: full.
- `diffs\changed-lines.txt`, `diffs\fix.patch`: full. Independently applied every supplied hunk in memory against the original packet and compared the result with the revised snapshot: all 16 files matched exactly. Nothing was written by that comparison.
- Each `snapshot\kanji\<K>.md`: full linguistic review, including untouched surrounding text.
- `snapshot\words\応援.md`: full.
- `checks\quiz-safety.txt`, `checks\reading-options.txt`, `checks\link-targets.tsv`: full.
- `evidence\QuizBuilder.kt`: full.
- `evidence\KanjiReadings.kt`: part, lines 1-230, including normalization, stem selection, exclusions, option construction and queue eligibility.
- `evidence\Words.kt`: part, lines 210-280, including the complete `ReadingOptions.mutations` implementation.
- `evidence\jmdict-cited-entries.xml`: full, all 18 supplied entries.
- `evidence\joyo\p33.txt`: full.
- `evidence\joyo-p33-utsuwa.png`, `evidence\joyo-p33-utsuwa-pair.png`: both complete images inspected visually.
- `evidence\kanjivg\05668.svg`, `evidence\kanjivg\06fc0.svg`: full.

Original-packet paths below are relative to `C:\Users\stop-\n1-kanji-workspace\review-packets\batch-110-453af714`.

- Each `snapshot\kanji\<K>.md` and `snapshot\words\応援.md`: complete files loaded for exact patch, metadata and text comparisons; the original articles were not all linguistically re-reviewed from scratch.
- `titles\kanji-titles.tsv`, `titles\word-titles.tsv`: parsed in full for targeted identity, title-uniqueness and link checks; relevant rows inspected. No corpus-directory scan was performed.
- `repo\kanji\怪.md`, `repo\kanji\料.md`, `repo\kanji\募.md`, `repo\kanji\校.md`, `repo\kanji\西.md`, `repo\kanji\屋.md`: full.
- These individually named files under `repo\kanji\`, each with extension `.md`: front matter reviewed for option construction; complete files loaded only to extract that front matter:

```text
充 兼 勘 化 吸 品 喜 坂 型 奇 好 宿 庁 広 弧 弱 扱 掃 撃 政 敗
敬 暗 期 板 欧 段 毒 滴 漱 紙 組 給 練 績 談 責 返 長 駐 験
```

Also read my own `C:\Users\stop-\n1-kanji-workspace\review-packets\reports-110-gpt\initial-gpt.md` in full. The former supplement was not opened.

Independent public checks inspected actual Digital Daijisen entries, delivered by Weblio, for [素敵](https://www.weblio.jp/content/素敵), [素晴らしい](https://www.weblio.jp/content/素晴らしい), [応じる](https://www.weblio.jp/content/応じる), its referenced [応ずる](https://www.weblio.jp/content/応ずる), [募](https://www.weblio.jp/content/募), [学級](https://www.weblio.jp/content/学級), [縮緬](https://www.weblio.jp/content/縮緬), [潮騒](https://www.weblio.jp/content/潮騒), [騒](https://www.weblio.jp/content/騒) and [嫌](https://www.weblio.jp/content/嫌). These were entry passages, not search snippets. The leading part of the [募る](https://www.weblio.jp/content/募る) page was also opened; its general-purpose explanation was not substituted for the Daijisen evidence.

The supplied 激 SVG was independently fetched from [the exact pinned public KanjiVG revision](https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/06fc0.svg) and was byte-identical, SHA-256 `9a2c447de06066111213a0182ce7579cd094bf3c9603bd45c750433eab525141`. No downloads were saved.

Dispositions:

#1 - **RESOLVED** - `snapshot\kanji\価.md:37` now assigns か to 価 and カク to 格. The surrounding breakdowns remain consistent.

#2 - **RESOLVED** - `snapshot\words\応援.md:30-33` links 応 and says only 援 lacks a card. Independent title-index checking confirms that distinction. No contrary statement remains in the article.

#3a - **RESOLVED** - `嫌.md:14,58` adds the direct 嫌/怪 edge and explains the suspicion overlap. 怪's actual title and suspecting sense support it. `QuizBuilder.kt` makes the declaration symmetric; neither endpoint uses the other as a curated distractor.

#3b - **RESOLVED** - `素.md:14,61` adds the direct 素/料 edge, justified by the material/ingredient sense and 料's actual title. The reverse direction need not be equally ambiguous for the pair to require protection. This adds one edge, not a transitive clique.

#4a - **RESOLVED** - `応.md:14,60-61` removes 募 and correctly contrasts recruiting with responding. The complete supplied JMdict 応じる entry includes applying in response to recruitment; the public 応ずる and 募 entries corroborate the distinction. 募 has no reverse exclusion.

#4b - **RESOLVED** - `級.md:14,55-56` removes 校 and correctly distinguishes a school from a class within it. The public 学級 entry supports the class-group meaning. 校 has no reverse exclusion.

#5 - **RESOLVED** - 基 and 素 have shorter openings and segmented reading explanations. Independent comparison confirms that their Readings tables and Common words sections are unchanged and that no old link target was lost. Independently reproduced paragraph counts are 45 to 93 overall, with the maximum falling from 264 to 99 words; 基's maximum is 88 and 素's 82. The new 素敵/素晴らしい paragraph agrees with the complete supplied JMdict entries, including their ateji flags and readings; the live entries corroborate the vocabulary and senses.

OA - **DECLINE ACCEPTED** - The optional reduction of the other 13 opening inventories was not fully adopted, but all long reading explanations were segmented. Retaining those inventories is an editorial choice, not a newly established blocking defect. The two mandatory density fixes were made without sacrificing coverage.

OB - **RESOLVED** - `激.md:27` accurately places 白 above 方 in the middle and 攵 at the far right. The independently authenticated SVG supports both the coordinates and the split 放 grouping. The mnemonic remains explicitly modern-shape, not etymology.

L1 - **PARTIALLY RESOLVED** - The supplied sources and audit now identify the selection algorithm, actual scheduled prompts and candidate behavior. However, the audit's unlisted-reading inventory is incomplete: it misses 嫌 や, which can be a wrong option for the actual kun prompt いや in a smaller studied pool. See new finding 1. The all-card, 200-seed result is not an all-studied-subsets safety proof.

L2 - **RESOLVED** - The supplied source settles the previously unavailable exclusion-aware meaning mechanics: symmetric direct edges, no transitive closure, and checks against both the target and already chosen wrong options. Reading quizzes use separate reading-key protection, not `quiz_exclusions`. This is source-level confirmation, not verification of any installed APK or the claimed historical compatibility boundary.

L3 - **PARTIALLY RESOLVED** - The new `器.md:27-29` claim is visually corroborated by both supplied p33 images: the bracketed form has the extra dot; the main form does not. The 器 SVG independently supports a modern 大 centre. The earlier limitation about independently viewing the original official PDF pages remains: the full PDF was not visually inspected, and the unchanged claims on other pages retain their first-round text-extract corroboration.

Verdicts:

Correctness: **CLEAN** within the revised-content scope - all 15 cards and 応援; no new factual or translation defect established in the changed teaching prose. The new 器 shape distinction, 応用 breakdown, まさに qualification, 嫌 wording, exceptional-word explanations and 素 vocabulary paragraph are supported. The primary-PDF limitation above is retained.

Scoped coverage: **CLEAN** - all 15 cards. Front matter differs only in the four declared exclusion lists. Full readings, selected readings, titles, tags, radicals and stroke counts are unchanged. 基/素 retain their existing reading and vocabulary coverage.

Consistency and quiz safety: **NEEDS FIX** - 嫌, because of finding 1. The meaning choices are **CLEAN for all 15 cards**: all 45 curated wrong titles survive the actual builder's pair checks and are defensibly wrong in both directions. All 15 titles remain unique, and all 109 changed-line link targets/titles independently match the indexes; all 472 internal-link occurrences in the revised cards identify indexed targets. No additional card-specific defect was established in the other 14 cards. A universal all-pools reading-safety claim remains unverified.

Comprehensibility: **CLEAN** - all 15 cards and the changed 応援 passage. The main ideas precede the reference qualifications, the mandatory walls of text are removed, the two revised mnemonics are concrete and honestly labelled, and no new sentence-level contradiction was established.

The actual reading queue has **26 prompts**, not the 32 raw selected-reading rows printed by `quiz-safety.txt`. `ReadingCard.quizReadings` collapses identical stems before scheduling. Independently derived prompts, checked against `reading-options.txt`, are:

| Card | On prompts | Kun prompts |
|---|---|---|
| 張 | チョウ | は.る |
| 器 | キ | none |
| 素 | ソ, ス | もと |
| 応 | オウ | none |
| 仮 | カ | none |
| 基 | キ | もと |
| 価 | カ | none |
| 激 | ゲキ | はげ.しい |
| 嫌 | ゲン | きら.う, いや |
| 縮 | シュク | ちぢ.む |
| 騒 | ソウ | さわ.ぐ |
| 統 | トウ | none |
| 級 | キュウ | none |
| 整 | セイ | ととの.う |
| 暖 | ダン | あたた.かい |

This count correction is a qualification of the simulation, not six additional content findings. All metadata readings, including unscheduled ones, still enter the builder's exclusion set.

Confirmation: **NEEDS FIX** - the original actionable findings are resolved, but newly established finding 1 prevents confirmation of reading-quiz safety.

Findings:

1. **Minor - consistency and quiz safety.** `snapshot\kanji\嫌.md:9-12`; `checks\reading-options.txt:150-179,294`; `evidence\KanjiReadings.kt:74-114`; original context `repo\kanji\屋.md:9-10`.

   **Claim and impact:** The new audit says there are no unlisted readings attested for 嫌 and finishes with "0 problem(s)". It omits the dictionary-attested contracted native reading **や**. The actual Daijisen 嫌 page has a separate `や【▽嫌／×厭】` entry, explicitly describing it as the sound-changed form of いや and illustrating ordinary adjectival uses. Thus や is not merely a name reading or an unrelated on reading.

   The supplied option builder can mark it wrong for the actual kun prompt いや. A minimal source-level case is `all=[嫌, 屋]`, `kind=Kun`, `reading=いや`, `count=4`. 屋 offers や; no curated distractor is present. 嫌's complete normalized exclusion set is `いや, きらい, きらう, ぎらい, ぎらう, けん, げん`, which does not include や. The fallback therefore returns the two labels **や / いや**, in random order, with only いや accepted. Returning two options is expressly supported by this implementation.

   I independently reproduced that deterministic option set with an in-memory port of the relevant source logic. This is a newly established source/audit problem, not a claim that the revision introduced the underlying client behavior. In the complete 1,161-card pool the three usable curated distractors hide the problem; testing only that pool cannot establish safety for the learner's smaller studied pool.

   **Remedy:** Protect the attested contraction in the reading-option exclusion mechanism and include smaller-pool cases in the audit. Preserve the pinned KANJIDIC2 metadata rather than silently presenting an extra value as part of that source record; this may require explicit additional-reading exclusion support in the client. A meaning `quiz_exclusions` edge would not fix this reading quiz. Update the audit's attested-reading inventory as well.

   **Evidence:** Actual [Daijisen 嫌 entry](https://www.weblio.jp/content/嫌), subsection や; 屋's supplied kun metadata; the cited exclusion and fallback implementation; and the deterministic source-level case above.

   **Confidence:** High for the dictionary attestation and builder result. No installed-phone reproduction is claimed.

Optional: None beyond the accepted editorial preference under OA.

Limits:

- The finding interprets an unrestricted "pick the kun'yomi" prompt as not permitting a dictionary-attested contracted native reading of the displayed kanji to be marked wrong. Neither the supplied reading-kind labels nor the builder contract states an "uncontracted KANJIDIC2 citation forms only" restriction. This is a quiz-protection issue, not a demand to add every contraction to the teaching table or required practice set.
- The reading audit uses all cards, a different random generator and 200 seeds per prompt. It does not certify every studied subset or exact device draw; several printed lower-tier candidate lists are abbreviated. I verified the algorithm, every scheduled prompt, the listed candidate behavior and targeted counterexamples, not an exhaustive 1,161-card linguistic inventory.
- Separately, a source-level pool `[騒, 西]` produces ソウ with セイ, サイ and ス as wrong labels. Thus the audit's "cannot be drawn from the full pool" note for さい cannot be generalized to all studied pools. However, さい is the exceptional native reading in 潮騒, not a second on'yomi of 騒; I do not count that example as another established same-kind ambiguous-answer finding. Likewise 応's name-only お is not automatically a valid on'yomi answer.
- The supplied source provenance, historical app-compatibility assertion and reported test totals were not independently authenticated against an Android checkout or rerun. No APK, live UI, animation or learner testing was performed. The source-level examples assume that the caller can supply a smaller studied pool, as the packet states; exact installed-client reachability was not observed.
- The new 器 statement was checked visually against the supplied crops and structurally against KanjiVG, not against an independently rendered original PDF. Other Joyo-page claims are unchanged and retain the prior extract-based limitation.
- The other 92 word articles and all 15 stroke files were not reopened in this confirmation round; they are outside the supplied revision patch and retain their first-round review results. Generated `manifest.json` was excluded by the packet contract. Snapshot identity and ancestry are taken from the packet, not independently checked in a repository.
- CLEAN is bounded to the reviewed claims and evidence, not exhaustive linguistic or runtime certification. Only the designated confirmation report was written.
