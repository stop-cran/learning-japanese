Snapshot: `d276f63b4d2adf4985f8bf929bdad1103987556b`. Reviewer model: OpenAI ChatGPT; my exact deployed model/version is not exposed to me.

Scope:

- Read this packet's INSTRUCTIONS, CHANGES, RESPONSE, exact cumulative patch, changed-line list, evidence README and revised `snapshot\kanji\牧.md` in full. Checked all four changed lines against correctness, scoped coverage, consistency/quiz safety and comprehensibility.
- Read my `reports-146\confirm3-gpt.md`, the earlier 牧 card's opening/meaning section, the original review rubric, and `repo\docs\content-format.md:98–154`. Checked the seventeen comparison titles on changed lines against actual card headers; read 僧 and 坊 in full.
- Inspected all fifteen revised cards' quiz metadata, all forty distinct curated meaning-option titles, `QuizBuilder.kt`, `quiz-safety.txt`, `link-targets.tsv` and `reading-options.txt`. Glanced at the opening and summary of `reading-exposure.txt`. Read `KanjiReadings.kt:1–160`, the reading-mutation implementation and the supplied 牧 Daijisen extract.
- Independently fetched and inspected the actual Digital Daijisen entries for 牧, 畜, 師, 僧, 坊 and 牧師. No other reviewer's report was opened.

Dispositions:

- **Finding 1 — RESOLVED.** 坊 is removed at `牧.md:14`, and line 54 no longer presents its displayed “Buddhist priest; boy” as a meaning of 牧. Its specifically qualified label remains distinguishable from “pastor”; the inspected [坊](https://www.weblio.jp/content/坊) and [牧師](https://www.weblio.jp/content/牧師) entries support that distinction.
- **Follow-up removal of 僧 (unnumbered item in RESPONSE.md) — NOT RESOLVED.** Treating 僧 as necessarily equivalent to 坊 overlooks 僧's broader dictionary sense and its unqualified displayed “priest.” The original finding did not require their exclusions to match. See new finding 1.
- **Wording changes at lines 26 and 53 — RESOLVED.** “Govern and guide people” accurately renders Daijisen's 人々を治め導く. “Kanji related to the first sense” avoids calling individual characters words. The animal/plant contrasts remain valid.

**All eleven retained exclusions are individually defensible**, but that does not establish that the revised list is sufficient:

| Direct pair | Displayed comparison label | Assessment under the displayed-label/ordinary-meaning rule |
|---|---|---|
| 牧–畜 | livestock; domestic animals | Defensible in reverse: 牧's displayed “raise livestock” answers 畜's attested verbal sense 牛馬などを飼う. This is not an assertion that 牧 means an animal. |
| 牧–養 | nourish; raise; adopt | Defensible: “raise” covers 牧's livestock-raising sense. |
| 牧–育 | grow up; raise | Defensible: the displayed “raise” overlaps livestock raising. |
| 牧–農 | agriculture; farming | Defensible: livestock farming is farming; this is an activity overlap, not merely a shared countryside setting. |
| 牧–野 | open field | Defensible: this broad land label can describe 牧's pasture/grazing-land sense. |
| 牧–治 | govern; heal | Defensible: “govern” directly matches 牧's second Daijisen sense. |
| 牧–御 | honorific; govern | Defensible through the displayed “govern,” not through honorific usage. |
| 牧–官 | government official | Defensible: 牧 also denotes an official/local governor. |
| 牧–司 | take charge; official; preside | Defensible through “official” and the governance sense. |
| 牧–導 | guide; conduct | Defensible: “guide” directly matches 導く in 牧's second sense. |
| 牧–師 | teacher; specialist | Defensible in reverse: 牧's displayed “pastor” answers 師's explicit respectful designation for a 牧師. |

Evidence: actual comparison headers; `content-format.md:110–132`; [Daijisen 牧](https://www.weblio.jp/content/牧), [畜](https://www.weblio.jp/content/畜) and [師](https://www.weblio.jp/content/師). These are direct pairs, not a transitive group. None overlaps 牧's curated distractors.

Verdicts:

- **Correctness: NEEDS FIX — 牧**, the new categorical explanation concerning 僧 at line 54.
- **Scoped coverage: CLEAN** within this revision; no additional necessary teaching distinction was established as missing.
- **Consistency and quiz safety: NEEDS FIX — 牧**, the newly removed direct 僧 pair. No new defect established in the other fourteen cards' checked quiz options.
- **Comprehensibility: CLEAN** within scope; the revised sense heading and “Kanji related” wording are understandable to a beginner.

Confirmation: **NEEDS FIX** — the original Finding 1 is resolved and all eleven retained pairs are defensible, but removing 僧 introduces the following distinct regression.

Findings:

**1. Minor; correctness and consistency/quiz safety; `snapshot\kanji\牧.md:14,54` — 僧 is not exclusively Buddhist, so its removal is not justified by equating it with 坊.**

- **Claim and impact:** Line 54 groups 僧 and 坊 as Buddhist clergy that cannot overlap 牧. However, the actual [Digital Daijisen 僧 entry](https://www.weblio.jp/content/僧), noun sense 2, also defines someone belonging to a religion who undertakes religious practice or propagation, explicitly illustrating Christian usage with カトリック僧. That sense is not marked archaic or rare in the inspected entry. The actual displayed label is “Buddhist monk; priest,” whereas 坊's is “Buddhist priest; boy.” In the reverse quiz direction, 牧's displayed “pastor” is defensible for 僧's broader religious-cleric sense. This is dictionary-supported secondary meaning, not merely an inference that all clergy share a topic.
- **Mechanism:** Neither revised 牧 nor the supplied 僧 card declares the pair. `QuizBuilder.kt` therefore no longer prevents their coexistence in meaning options when fallback/custom pools bring them together. The standard three curated wrong options for 牧 are unaffected; I am not claiming a collision was observed in that default set.
- **Remedy:** Restore the direct 僧 exclusion and distinguish its broader secondary sense in line 54. Keep 坊 removed: its explicitly Buddhist displayed label does not provide the same justification. Update the count/grouping accordingly.
- **Evidence:** Actual 僧 and 坊 headers/bodies; revised 牧 title and lines 14/54; `content-format.md:119–132`; `QuizBuilder.kt`'s symmetric `excluded`/`tryAdd` logic; actual [Daijisen 僧](https://www.weblio.jp/content/僧) and [牧師](https://www.weblio.jp/content/牧師) entries. The 僧 card itself says “usually” Buddhist and acknowledges wider compound uses; its body does not eliminate the dictionary-attested secondary meaning from the quiz rule.
- **Confidence:** High for the overcategorical explanation; medium-high for the resulting fallback ambiguity. This is newly introduced by removing 僧, not a reopening of the resolved 坊 finding.

Optional: None.

Limits:

- **Meaning audits:** All fifteen reported curated sets were checked against actual titles: 煮→火水肉; 熟→語木田; 牧→歌山雨; 狂→犬気風; 狭→道室店; 献→猫独状; 玄→率畜玉; 環→現理琴; 甚→甘匹基; 癖→疲痛療; 益→皿雨魚; 盛→山海店; 盾→目直真; 眺→相県省; 睡→真着直. These remain defensibly wrong. The builder checks direct symmetric exclusions against the target and between wrong choices, then uses curated/tag/random candidates. Exact-title deduplication and a zero-error audit cannot establish semantic uniqueness, justify exclusions or find every missing pair.
- **Reading audits:** Checked all seventeen selected prompts. No new wrong-option reading defect was established. 環 and 癖 require reading fallbacks because 琴 and 療 respectively lack the usable reading kind. The code protects normalized full metadata readings and generated variants, not every dictionary-attested reading. Meaning exclusions do not protect reading quizzes.
- The exposure summary reports zero production, padded-session and one-holder padded hits, with ten unchanged latent collisions. Reading-options reports zero problems across its supplied inventory and 100 seeds per prompt. These bounded simulations do not prove safety for arbitrary custom/future pools, multiple borrowed holders, or attested readings absent from the supplied inventory. For example, 牧's unlisted モク remains protected by current pool selection rather than by its metadata.
- All seventeen changed-line links resolve with matching quoted titles in the supplied audit and the inspected target headers. Structural checks do not verify the linguistic explanation attached to those links.
- No Android/JVM tests, installed-client execution, physical-phone rendering, independent commit-object verification or fresh official Joyo PDF verification was performed. Unchanged word articles and the other fourteen card bodies were not reviewed afresh in full. Supplied audits were inspected, not independently rerun. No frequency claim about broader 僧 usage is made.
- One combined read and one oversized public-page fetch were truncated by the tool. Relevant local material was subsequently obtained in bounded reads; the finding relies on the separately inspected Daijisen entry, not truncated output or a search snippet. Automatically saved tool-output files were not opened.
- All tool-bearing responses used exactly one serial call. No parallel calls, sub-agents, other sessions, background jobs, recursive directory listings or corpus scans were used. Only this report was created.
