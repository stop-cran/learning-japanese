Snapshot: `3c5ef8450e38051682dab2bea5fce320b992e5ea`, compared with `c6afa16315d5a88b5045eeb85d429b8f7fd90b1f`. Reviewer: OpenAI ChatGPT, GPT-family; the exact serving-model identifier is not exposed.

Scope:

- Fully read this packet's `INSTRUCTIONS.md`, `CHANGES.md`, `RESPONSE.md`, `diffs\fix.patch`, `diffs\changed-lines.txt`, and `evidence\README.md`; also my authorized `reports-156-hold\initial-gpt.md`.
- Fully read all ten `snapshot\kanji\` cards, including every changed card, and revised `snapshot\words\甲乙.md`, `亜熱帯.md`, and `仁.md`. The deleted 乙 article was read completely in the deletion patch. All changed hunks were considered against all four facets and their surrounding text. All thirteen exported snapshot blobs match the packet-manifest Git blob identities after CRLF normalization.
- Fully read `checks\quiz-safety.txt`, `reading-options.txt`, `reading-exposure.txt`, `link-targets.tsv`, and `evidence\QuizBuilder.kt`, `compound-sound-changes.md`, `甲乙-daijisen.txt`, `distractor-use.tsv`, `corpus-attested.txt`, `wazaogi-scan.txt`, `wazaogi_scan.py`, and `gen_corpus_attested.py`. Read the revised distractor-sense evidence through its in-revision entries and relevant rejected candidates.
- Original-packet context: fully read `snapshot\kanji\潜.md`, `snapshot\words\伐採.md`, `evidence\app-code\Words.kt`, and the relevant `KanjiReadings.kt:1–142`, `WordQuizViewModel.kt:35–115`, and `evidence\audits\word_quiz_audit.py:1–185`. Read the rubric through line 180; inspected actual comparison-word articles and all seventeen revised distractor cards' titles, exclusions, and complete meaning sections.
- Parsed the supplied JMdict XML and inspected the seven changed cards' cited spellings, readings, senses, and restrictions; inspected complete consequential entries for 甲乙, its cited expressions/components, 仁, and the new exclusions. Checked KANJIDIC2 Japanese readings, English meanings, and name readings against the original records, Joyo quotations against the supplied table rows, and Kanjipedia/Daijisen quotations against their supplied extracts.
- Independently fetched actual public dictionary content, not search snippets: [Digital Daijisen 甲乙](https://www.weblio.jp/content/%E7%94%B2%E4%B9%99), [Digital Daijisen 仁](https://www.weblio.jp/content/%E4%BB%81), and [Jisho/KANJIDIC 甲](https://jisho.org/search/%E7%94%B2%20%23kanji). Inspected `word-quiz.txt` selectively: all 甲乙 forward options, its reverse labels, 仁's forward semantic-risk labels and all fifty reverse meaning targets, and the concluding audit summary.

Dispositions:

- G1 - RESOLVED - The deletion removes the bare-乙 word-reading question, not merely its meaning options. The replacement's four generated readings and nine corpus-tier readings contain neither かるめる nor another attested 甲乙 reading (`word-quiz.txt:89–92`; `Words.kt:250–261`). The kanji card still explicitly teaches おつ and the qualified おと use (`乙.md:23,31,33,42,53`).
- G2 - RESOLVED - 人物 is now directly excluded, symmetrically in the actual meaning builder. 個人 likewise overlaps the human sense; 芯 and 中心 have broad physical-core senses overlapping the taught kernel sense. These additions are direct target/option checks, not expansion through shared exclusions (`仁.md:8,38`; JMdict 1369620, 1369070, 1264770, 1595120, 1424550). No additional collision was established in the screened forward tier or fifty reverse targets.
- G3 - RESOLVED - Both revised sets include 供, a visually plausible 亻 card, and replace the exclusively concrete-object categories. The mixed action, self, and life meanings are safely distinct. All six revised sets were checked for semantic and reading regressions; none was established.
- O1 - DECLINE ACCEPTED - This was nonblocking layout polish. Keeping the existing layout is reasonable for this bounded revision; the revised distractor explanations are single sentences.
- O2 - RESOLVED - 亜流 retains verified, accessible glosses without “epigone”; 仙 now explains “ateji” immediately (`亜.md:31`; `仙.md:32`; JMdict 1149930, 1075090).
- O3 - RESOLVED - `words\仁.md:22` adopts the natural English translation without changing the Japanese or kana.
- L1 - RESOLVED - The actual destination is supplied. Its gemination explanation supports both ばっ/バツ links and ねっ/ネツ. Its explicit h-row-to-p-row explanation supports the limited ぷく/フク correspondence cited in 潜; it does not specifically explain the nasal environment. That narrower teaching improvement is optional below.
- L2 - RESOLVED - Complete entry 1002570 is supplied and agrees with the earlier citation; the deleted article was its only scoped citation. No revised article depends on it.

Revised-text adjudications:

- **甲乙, complete new article:** The two meanings, こうおつ reading, ten-stem derivation, component readings, set phrase, and quoted Daijisen example fragments agree with the evidence. Both original examples use the relative-merit construction naturally; their kana and translations are sound. 優劣 expresses relative merit; 前者/後者 select individual members rather than both; 丙 continues the label sequence. The かるめる paragraph accurately distinguishes the music word documented by Daijisen. Its presence does not create a reachable reading collision.
- **甲乙 quizzes:** 丙 is a plausible but incorrect rank-label answer. All eight exclusions have defensible direct relationships to the displayed written form's ordering or quality-distinction senses. The eight remaining scored candidates are not equivalent answers. In particular, 後者 selects only the latter, while 同格 asserts equal rank; neither means the pair or relative merit. No new collision was established among the inspected reverse labels.
- **乙 replacement/navigation:** The beginner still encounters おつ, its second-rank and stylish senses, an おとご example, and an explicit archaic sibling explanation. Removing the standalone article does not erase those distinctions. All sixteen changed-line links resolve in the supplied target check; the new word and comparison titles agree with the actual inspected articles. No scoped link still points to the deleted article.
- **仁 exclusions:** 人物 and 個人 directly cover human/person answers. 芯's physical inner material and 中心's “core” can describe the kernel sense broadly enough to justify exclusion; this does not make 仁 a synonym for abstract focus or every middle position. Remaining 中央 (“center; middle”) supplies position, not that inner material. 世話 (“care; assistance”) names assistance rather than the moral disposition. No further defensible answer was established.
- **Six distractor sets:** 王/硬/粗 contrast rank and qualities; 下/供/生 and 供/食/自 mix meanings and retain a person-radical look-alike; 起/座/伸 contrast posture or extension; 保/耕/育 contrast protective and cultivation actions; 迎/離/他 contrast reception, separation, and otherness. None of these sets preserves the former all-concrete-versus-abstract shortcut. Sitting is not prostration; stretching is not lying face down; greeting is not accompaniment; life is not immortality. No listed distractor is also a directly excluded target.
- **All ten kanji quizzes:** Inspected all displayed meaning sets and reading prompts, including unchanged 丹/仁/伯. No new multiple-correct-answer case was established. Curated readings fill all three wrong slots in N1/All; 仙 and 伎 now also do so in Starter practice. Starter fallback remains relevant for 乙/伏/伐/伴. The supplied exposure analysis finds no newly reachable attested reading.
- **Other-review changes, individually:** (1) 仁's added nucleolus sense and restriction of にん to the kernel sense match JMdict 1369620's sense-local restrictions. (2) “Any of the three characters” correctly counts 亜熱帯. (3) Leaving 伯's conservative HIT output unchanged creates no content defect: 自/物/毎 always fill its slots before fallback. (4) The supplied absence-scan method/results support the pinned-JMdict わざおぎ statement, subject to the limitation below. (5) The unsupported contract-compound sentence is gone; the replacement examples are grounded in Daijisen's relative-merit phrases. The separate component-party claims at line 39 remain supported by entries 1578730 and 1182940.

Verdicts:

- Correctness: CLEAN - No new actionable factual defect established in any changed card/article.
- Scoped coverage: CLEAN - Replacement 甲乙 and retained 乙 reading/sense coverage are adequate.
- Consistency and quiz safety: CLEAN - G1–G3 resolved; no new actionable option or navigation defect established.
- Comprehensibility: CLEAN - Revised specialist wording and translation improve accessibility; no new blocking beginner-facing ambiguity established.

Confirmation: CONFIRMED - Every response item is RESOLVED or DECLINE ACCEPTED, and no new actionable defect was established within this confirmation scope.

Findings: none.

Optional:

- Add a separate nasal-plus-/p/ example to the compound-sound-changes article, explicitly comparing せん + ふく with せんぷく. Its current h-to-p explanation names the right phenomenon, but its しっぱい example and section heading do not demonstrate /p/ after ん.

Limits:

- Exact serving-model version unavailable; no model identifier is invented.
- CLEAN is bounded, not exhaustive. The 1,409-member 仁 tier received targeted English-label semantic screening, not independent dictionary verification of every member. The screened reverse labels likewise do not establish exhaustive correctness for every secondary sense.
- Audits establish candidate mechanics and bounded reachability, not naturalness, semantic equivalence, or actual phone usability. The word audit uses the All stack and a Python port; it is not an executed Android session. Its generic tier summaries simplify distinct-key selection and interactions between selected exclusions. The kanji exposure analysis covers the named pools and one-holder padding cases, not every conceivable borrowed-card combination.
- The reported 112 pre-existing word-reading collisions remain a client follow-up, not a newly verified corpus-wide result or a defect introduced by this revision. I inspected the supplied result and method but ran no corpus scan. Similarly, absence of わざおぎ and all-repository references to the deleted article rests on supplied bounded evidence/checks, not a fresh complete-dictionary or repository scan.
- Quoted source checks used the supplied pinned records/extracts plus the public entries named above; not every quotation received a fresh public retrieval. The exact pinned 甲 KANJIDIC2 record was not supplied here; its consequential コウ reading was independently corroborated publicly.
- No native app, JVM tests, stroke rendering, or phone-layout review was performed. Unchanged content was not reopened as a new whole-batch linguistic audit.
- Exactly one tool call was issued per tool-bearing response; no parallel calls, delegation, background jobs, other sessions, recursive listings, or unauthorized local reads were used. Oversized command output was reread from authorized source paths in smaller selections; automatically generated tool-output captures were not opened. Only this authorized report file was created.
