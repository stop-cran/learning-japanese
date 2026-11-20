Snapshot: `070b6f694216c7580346cc1b1432519b3284e919` — batch 149. Reviewer: GitHub Copilot, OpenAI GPT family; the exact runtime model/version identifier is not exposed to me.

Packet: `batch-149-070b6f69`. I independently computed the SHA-256 of `packet-manifest.json`; it matches `903d321fda8a6df1f46f014c26896a5516d78fc4ac37a5fd8f896882bc419c38`.

Scope:

All paths below are relative to the supplied packet. Facets 3, consistency/quiz safety, and 4, beginner/phone comprehensibility, received the deepest examination. “Structured” means that I consumed the specified records or geometry programmatically and inspected the resulting checks, not that I read every surrounding XML/JSON line as prose.

**Complete text read**

- `INSTRUCTIONS.md`
- `mechanical-checks.md`
- `rubric\copilot-instructions.md`
- `evidence\provenance.json`
- `evidence\joyo-pages.md`
- `evidence\kanjipedia-outside-readings.json`
- `evidence\daijisen-heads.txt`
- `evidence\okurigana-scan.txt`
- `evidence\kanjivg-components.txt`
- `evidence\audits\quiz-safety.txt`
- `evidence\audits\reading-exposure.txt`
- `evidence\audits\reading-options.txt`
- `evidence\audits\kanji-remarks.json`
- `evidence\audits\word-remarks.json`
- `evidence\app-code\QuizBuilder.kt`

**All 15 new kanji articles, complete**

In `snapshot\kanji\`: `翻.md`, `翼.md`, `脈.md`, `腐.md`, `臨.md`, `臭.md`, `興.md`, `舌.md`, `舎.md`, `艶.md`, `芝.md`, `芽.md`, `茂.md`, `荘.md`, `華.md`.

**All 15 stroke files, complete structured checks**

In `snapshot\strokes\`: `翻.json`, `翼.json`, `脈.json`, `腐.json`, `臨.json`, `臭.json`, `興.json`, `舌.json`, `舎.json`, `艶.json`, `芝.json`, `芽.json`, `茂.json`, `荘.json`, `華.json`. The raw `芝.json` text was also inspected.

**All 17 modified word articles, complete**

In `snapshot\words\`: `別荘.md`, `文脈.md`, `校舎.md`, `田舎.md`, `翻訳.md`, `翼.md`, `腐る.md`, `臨時.md`, `臭い.md`, `興味.md`, `舌.md`, `艶.md`, `芝居.md`, `芝生.md`, `芽.md`, `茂る.md`, `豪華.md`.

**All 17 word diffs, complete**

In `diffs\`: `words__別荘.md.diff`, `words__文脈.md.diff`, `words__校舎.md.diff`, `words__田舎.md.diff`, `words__翻訳.md.diff`, `words__翼.md.diff`, `words__腐る.md.diff`, `words__臨時.md.diff`, `words__臭い.md.diff`, `words__興味.md.diff`, `words__舌.md.diff`, `words__艶.md.diff`, `words__芝居.md.diff`, `words__芝生.md.diff`, `words__芽.md.diff`, `words__茂る.md.diff`, `words__豪華.md.diff`.

**Context articles**

- Complete: `repo\kanji\復.md`, `repo\kanji\線.md`, `repo\kanji\口.md`, `repo\kanji\喜.md`, `repo\kanji\住.md`, `repo\kanji\盛.md`, `repo\kanji\密.md`.
- `repo\kanji\艶.md`: opened in a retrieval whose output was truncated; not substantively reviewed as a separate context article. The scoped snapshot article was read completely.

**Partial or structured evidence**

- `packet-manifest.json`: first 35 lines as text; complete bytes for its SHA-256.
- `evidence\source-metadata.json`: complete structured comparison for the 15 targets.
- `evidence\kanjidic2-records.xml`: opening 24 lines, all 15 target records, and relevant comparison records; not a prose review of every other record.
- `evidence\jmdict-families.xml`: opening 24 lines and complete cited-entry selections, including spelling/reading restrictions, senses, POS, register and usage annotations.
- `evidence\jmdict-digest.tsv`: opening 20 lines; structured selections for the 15 families, cited IDs and common-priority coverage candidates. Other rows were not individually reviewed.
- `evidence\kanjivg-svgs.txt`: lines 1–95 as raw text; ordered stroke types and complete path data for all 15 targets were parsed and independently compared with the stroke JSONs. Other raw SVG text was not read completely.
- `titles\kanji-titles.tsv`: indexed comparisons for all target, distractor, exclusion and mnemonic-component titles; additional semantic-neighbor checks and target-title uniqueness checks.
- `titles\word-titles.tsv`: header and exact relevant word rows.
- `repo\docs\content-format.md`: selected heading/keyword matches and lines 86–155 and 289–304.
- `repo\docs\confusable-words.md`: selected heading matches and lines 1–40.
- `evidence\app-code\KanjiReadings.kt`: lines 1–220 and selected function matches.
- `evidence\app-code\KanjiMeaningMetadata.kt`: selected metadata/exclusion-related matches only.
- `evidence\app-code\Words.kt`: selected model/link-related matches only.

**Independent public verification**

I inspected actual live Kanjipedia character entries and Digital Daijisen entries on Weblio for all 15 targets, rather than relying on search snippets or the packet’s cached public-source text. I also inspected actual Jisho/JMdict word entries/API responses for the selected quiz examples and consequential alternative readings, senses and register distinctions. These included the native verb families, the two readings of 臭い, the two 艶めく entries, 芝居/芝生/芝蘭, 芽ぐむ, 荘園, the mahjong readings, and 法華/香華/散華/蓮華. Live Jisho kanji entries supplied additional cross-checks, including 荘’s retained ほうき and the possible exclusion neighbors.

Verdicts:

- **Correctness: NEEDS FIX** — G1 and G2. No metadata, stroke-path or modern-shape mnemonic defect established.
- **Scoped coverage: CLEAN** — all 15 cards account for their metadata readings; the reviewed source-only/name/special-term distinctions are supported.
- **Consistency and quiz safety: NEEDS FIX** — G1 and G3. The displayed full-pool curated meaning options are safe; G3 concerns missing direct-pair protection in reduced/custom fallback pools.
- **Comprehensibility: NEEDS FIX** — G2 and G4. Central explanations and mnemonics generally work, but two Notes paragraphs are substantial beginner-facing walls of review bookkeeping.

Per-card verdicts follow. C = CLEAN; F = NEEDS FIX. A clean entry means no actionable defect established, not exhaustive certification.

| Kanji | Correctness | Coverage | Consistency / quiz | Comprehensibility | Exception |
|---|---|---|---|---|---|
| 翻 | C | C | C | C | — |
| 翼 | C | C | C | C | — |
| 脈 | C | C | C | C | Reading-pool qualification below |
| 腐 | C | C | C | C | — |
| 臨 | C | C | C | F | G4 |
| 臭 | C | C | C | C | — |
| 興 | C | C | F | C | G3 |
| 舌 | C | C | C | C | — |
| 舎 | C | C | C | C | — |
| 艶 | C | C | C | F | G4; the separate word article has G1 |
| 芝 | C | C | C | C | — |
| 芽 | C | C | C | C | — |
| 茂 | C | C | F | C | G3 |
| 荘 | F | C | C | F | G2 |
| 華 | C | C | C | C | — |

For the 17 word articles, all four facets are CLEAN except `snapshot\words\艶.md`, whose correctness and consistency NEED FIX under G1. All 17 diffs are genuinely link-wrap-only: independently stripping the added wrapper reproduces the previous line, exactly one intended target link is added, and no Dictionary line changes. The problem in G1 is the resulting surrounding passage, not a concealed extra edit.

**Meaning options actually displayed in the complete simulation**

I judged each of these individual wrong labels against the target, and the reverse target/label relationship. No defensible second answer was established among these curated choices.

| Target | Three displayed wrong options | Judgment |
|---|---|---|
| 翻 | open; unfold / talk, speak / stand; set up | Distinct from turning over or reversing |
| 翼 | bird / fish / insect; bug | Animals are not the wing itself |
| 脈 | eye / hand / foot, leg | Body parts, not pulse or vein |
| 腐 | bake; burn / wash / boil; simmer; stew | Processes distinct from rotting; possibly ruining food does not make these kanji mean “spoil” |
| 臨 | reside, dwell / know / use, employ | None gives facing a situation or attending an occasion |
| 臭 | snow / thread; yarn / bird | No smell/stink overlap |
| 興 | sky; empty / water / face; expression | No revival, interest or pleasure overlap |
| 舌 | mouth / ear / foot, leg | Distinct anatomical referents; see qualification below |
| 舎 | rain / tree, wood / mountain | Not houses or lodging |
| 艶 | ice; freeze / star; celestial point / fish | Not gloss, luster or allure |
| 芝 | dog / stone / mountain | Distinct concrete referents |
| 芽 | dog / mountain / water | None names a bud or sprout |
| 茂 | dog / mountain / water | None names luxuriant growth |
| 荘 | dog / sun, day / rain | None names a villa, manor or solemn quality |
| 華 | dog / moon, month / water | None names flower, splendor or showiness |

These are recognizable concrete alternatives, but several are only weakly diagnostic at N1; repetition is addressed under Optional.

**Readings, source labels and coverage**

All 15 front matters match the pinned target metadata for grade, stroke count, radical/number and complete on/kun lists. Every selected quiz reading is an exact metadata subset and has an appropriate linked word example:

| Kanji | Selected reading and linked evidence | Other consequential checks |
|---|---|---|
| 翻 | ホン — 翻訳 ほんやく | ひるがえる/ひるがえす distinguished; ハン is correctly confined to mahjong scoring; no ordinary-readings claim inferred from whole-word alternatives |
| 翼 | つばさ — 翼 つばさ | ヨク in 右翼; source-only たすける supported, not promoted into the quiz |
| 脈 | ミャク — 文脈 ぶんみゃく | すじ and バク qualifications supported; pulse/vein, connected-line and prospect senses distinguished |
| 腐 | くさ.る — 腐る くさる | All six metadata kun forms accounted for, including suffixal -くさる and the distinct くされる/くされ/くさらす/くさす forms |
| 臨 | リン — 臨時 りんじ | のぞむ supported by 臨む; み correctly identified as a name form |
| 臭 | くさ.い — 臭い くさい | Adjective くさい distinguished from noun におい; におう and fragrant-sense qualifications checked against the actual entries |
| 興 | キョウ — 興味 きょうみ | Correct segmentation; コウ in 興奮/復興 remains taught, not quizzed; 興る/興す distinguished from 起こる/起こす |
| 舌 | した — 舌 した | ゼツ examples valid; セツ/ことば source-only; じた and 百舌 treated as contextual/whole-word phenomena |
| 舎 | シャ — 校舎 こうしゃ | セキ/やどる/おく qualifications supported; irregular whole words and historical distance/family senses kept separate |
| 艶 | つや — 艶 つや | エン in 妖艶; なまめかしい/あでやか and both 艶めく readings distinguished, including archaic senses where applicable |
| 芝 | しば — 芝居 しばい | Official table supports 芝居 as the example; 芝生’s appendix treatment is accurately described; シ/source examples are not ordinary quiz evidence |
| 芽 | め — 芽 め | ガ in 発芽; めぐむ from 芽ぐむ correctly qualified as outside the ordinary quiz |
| 茂 | しげ.る — 茂る しげる | モ in 繁茂; additional ボウ/すぐれる and name forms properly qualified |
| 荘 | ソウ — 別荘 べっそう | ショウ in 荘園 is genuinely attested; チャン is a mahjong counter; ほうき/おごそか retained without pretending they are ordinary quiz material |
| 華 | カ — 豪華 ごうか | ケ/ゲ compound evidence and the official table’s 香華/散華 examples checked; はな retained; historical and name forms separated |

“Source-only” is not treated as synonymous with “nonexistent” or automatically “rare.” In particular, 荘園 genuinely supports ショウ, and the card does give that example.

The 臭 discussion accurately separates the unpleasant adjective from the smell noun and explains the shared dictionary entries without presenting fragrant 匂う usage as the default everyday meaning of 臭. 臭/腐 are odor versus decay, not interchangeable answers merely because decay can stink. Likewise, 茂 versus 芽 or 華 is abundant foliage versus a bud or flower/splendor, not an automatic exclusion.

For 舌/口, the anatomical labels “tongue” and “mouth” remain distinguishable in either direction. Both characters have speech associations, but that does not make the displayed organ names interchangeable. I interpret the last distractor sentence as describing those displayed labels, not as denying 口’s independently attested figurative speech uses.

**Exclusions and reading-audit accounting**

I checked declared exclusion pairs individually against the title indexes and the cited senses, rather than treating an exclusion neighborhood as a transitive clique. The broad sets have direct sense or displayed-label-confusion support. In particular:

- 臨/冒 has actual “face” evidence; 臨/写 has the copying-a-model sense.
- 翻/飛 and 翻/波 have flutter/fly and wave evidence, not merely a visual association.
- 興/設 and 興/起 have establish and arise/start senses.
- 舎/荘 is recorded once, on 舎, and has inn/cottage overlap.
- 艶/華 is recorded once, on 艶, with shared luster evidence.
- 艶/符 is an English-label ambiguity involving “charm,” not a claim that a talisman and attractiveness are the same Japanese sense. The prose explicitly distinguishes them.

The missing direct pairs I established are in G3; no blanket clique expansion is warranted.

The complete reading-exposure file correctly counts **16 latent collisions**, distributed as follows: 翼 1, 脈 1, 臨 1, 舌 1, 舎 2, 艶 2, 芽 2, 茂 3, 荘 1, 華 2. They are the holder-backed forms たすける; ばく; み; ことば; さ/おく; もろ/よし; じ/めぐむ; き/む/すぐれる; そ; わ/げ.

The reported **zero production, zero padded-session and zero one-holder padded hits** are consistent with the option-selection code and the audit’s documented pools. Full target metadata, including unquizzed readings, is protected; source-only extra readings outside that metadata are not universally protected.

The 脈 バク `HIT` in the option-tier report is therefore **not a demonstrated shipped-pool wrong answer**: 目/手/足 fill all three wrong slots before fallback is consulted. Conversely, “never drawable in any possible pool” would be false. The exposure file explicitly exhibits reduced hypothetical pools such as `[脈 暴]` and `[翼 助]`. Those are not pools the audit says the shipped stacks build. This distinction matters more than the isolated `HIT` label.

**Stroke files and mnemonics**

All 15 stroke JSONs have the correct identity/count, sequential stroke IDs, finite in-bounds point coordinates and 16 sampled points per stroke. Ordered stroke types and starts match the pinned SVGs. I independently flattened every target cubic SVG path and resampled its arc length: maximum point-distance deviation was below 0.071 viewbox units, consistent with the stored coordinate rounding.

All 15 mnemonic paragraphs are explicitly modern-shape memory aids, not etymology. Referenced card-title quotations match. Component/position checks passed, including 興’s central 同 and stroke-14 horizontal; 舎’s middle 士 strokes; 芽’s last two strokes; 華’s seven strokes below 艹; 脈’s right-side comparison with 派; and 茂’s 戈 comparison with 戦. No unsupported historical derivation was established.

Findings:

1. **G1 — minor; correctness and consistency; `snapshot\words\艶.md:29–31`.**

   **Claim and impact:** Immediately after the newly added link to the 艶 kanji card, the paragraph still says, “There is no separate 艶 card in the current collection.” The linked new card exists in this very snapshot. A learner is simultaneously offered that card and told it does not exist.

   **Remedy:** Remove or update the stale sentence. Because this requires more than the intended link wrap, declare the necessary remark edit rather than leaving the integration contradiction to preserve a link-only claim.

   **Evidence:** Complete word article, `diffs\words__艶.md.diff`, and `snapshot\kanji\艶.md`; the link resolves. No external linguistic judgment is needed.

   **Confidence:** High.

2. **G2 — minor; correctness and comprehensibility; `snapshot\kanji\荘.md:23`.**

   **Claim and impact:** 別荘 is correctly printed as べっそう, but the explanation says the word has a small っ “after ベツ.” The っ is not appended after ベツ: ベツ + ソウ becomes ベッソウ, with the final ツ becoming small ッ. The present wording can teach an extra segment, effectively ベツッソウ, while attempting to explain the pronunciation to a beginner.

   **Remedy:** Say, for example: “ベツ + ソウ becomes べっそう: the ツ changes to small っ before ソウ.”

   **Evidence:** Pinned JMdict entry 1509970; the correctly explained form in `snapshot\words\別荘.md`; independently inspected [Jisho entry response for 別荘](https://jisho.org/api/v1/search/words?keyword=%E5%88%A5%E8%8D%98).

   **Confidence:** High.

3. **G3 — minor; consistency and quiz safety; `snapshot\kanji\興.md:14` and `snapshot\kanji\茂.md:14`.**

   **Claim and impact:** Three direct overlapping pairs lack an exclusion on either side:

   - **興/復:** “revival; interest; pleasure” versus “restore; repeat.” Restoring/reviving something is an ordinary sense overlap, not just a connection through the compound 復興.
   - **茂/密:** “overgrown; lush” versus “secret; dense; close.” 茂’s own explanation says plants or foliage “grow dense”; 密’s “dense” is an ordinary, independently attested meaning.
   - **茂/盛:** “overgrown; lush” versus “thrive; heap up; serve food.” 茂 includes flourishing/thriving vegetation; this is not merely another plant-related character.

   Their full shipped-pool curated choices do not expose these pairs. However, the content-format contract explicitly covers custom and fallback pools. Using the visible `QuizBuilder` logic, the four-card pools `{興, 復, 芽, 翼}`, `{茂, 密, 芽, 翼}` and `{茂, 盛, 芽, 翼}` necessarily admit the overlapping alternative. I checked pairwise exclusions and both target directions; all fallback orderings admit it. These are bounded selection-logic counterexamples, not a claim that the current default-stack simulation failed.

   **Remedy:** Add 復 to 興’s exclusions and 密/盛 to 茂’s exclusions, or record each pair on the other side. One declaration per direct pair is enough. Do not also infer 密/盛 or any larger clique.

   **Evidence:** Exact titles in `titles\kanji-titles.tsv`; complete context cards `repo\kanji\復.md`, `密.md`, `盛.md`; `repo\docs\content-format.md:110–132`; `evidence\app-code\QuizBuilder.kt`; pinned 茂る/繁茂 entries. Independent public checks: [興](https://jisho.org/search/%E8%88%88%20%23kanji), [復](https://jisho.org/search/%E5%BE%A9%20%23kanji), [密](https://jisho.org/api/v1/search/words?keyword=%E5%AF%86), [盛ん](https://jisho.org/api/v1/search/words?keyword=%E7%9B%9B%E3%82%93), and [Kanjipedia 茂](https://www.kanjipedia.jp/kanji/0006716000), whose first sense describes branches/leaves growing vigorously and cites 繁茂.

   **Confidence:** High for missing declarations and selection reachability; medium-high for the semantic-confusability judgment.

4. **G4 — minor; comprehensibility; `snapshot\kanji\臨.md:40` and `snapshot\kanji\艶.md:51`.**

   **Claim and impact:** These single paragraphs contain approximately 240 and 182 whitespace-delimited words respectively, including Japanese strings. They mix reading/name qualifications with long dictionary quotations and the justifications for 13 or 12 exclusion partners. This is learner-facing audit bookkeeping, not a usable N5–N4 phone explanation. The useful reading distinctions become difficult to retrieve from the uninterrupted lists.

   **Remedy:** Separate the necessary reading/name qualifications into short bullets; retain only a small number of useful learner contrasts in the card. Preserve exhaustive exclusion provenance in maintainer evidence or a linked reference rather than the uninterrupted learner paragraph. The exclusions themselves need not be weakened.

   **Evidence:** Complete articles and direct paragraph counts; the packet’s explicit beginner/phone, no-wall-of-text requirement. This finding does not assert a failed physical-device rendering test.

   **Confidence:** High.

Optional:

- Rotate some safe concrete distractors across the five grass-crown cards. Repeating 犬 on 芝/芽/茂/荘/華, 山 on 舎/芝/芽/茂, and 水 on 興/芽/茂/華 is semantically safe but makes several questions predictable by elimination. This is a pedagogy improvement, not evidence that any listed choice is also correct.
- Consider the same Notes simplification for 舎:50, 荘:45 and 華:45; their exhaustive comparison lists are less severe examples of the same reading burden.
- On 舌, “none names the physical tongue” would make the intended anatomical contrast clearer than “none names the tongue, speech, or language.” [Daijisen’s くち entry](https://www.weblio.jp/content/%E5%8F%A3), sense 7, independently confirms ordinary speech-related uses of 口; the current sentence is acceptable only in its displayed-label context.
- Preserve the reading audits’ explicit pool boundary in future summaries. The 16 latent forms are useful future-hardening leads, not 16 demonstrated current production bugs.

Limits:

- The exact GPT runtime version is unavailable; I have not invented one.
- I worked alone and blind, without another reviewer’s report or the author’s rationale. Investigation calls were serial, one tool call per tool-taking turn; no parallel calls, subagents, other sessions, background jobs, recursive listings or corpus-directory scans were used. Corpus comparisons used the supplied title indexes.
- Public checks inspected actual entries. A failed kanjiapi request and unavailable optional HTML parser were replaced with successful direct dictionary retrievals; neither leaves a consequential reading claim unresolved.
- G3’s reduced-pool demonstrations used direct inspection and a bounded Python port of the visible selection logic, not execution of Kotlin. Reading conclusions distinguish the supplied audits’ shipped pools from explicitly hypothetical smaller pools.
- I did not run Android/JVM tests, the Kotlin cross-check, the repository build or a physical-phone preview. Their stated absence is not a finding. Phone comprehensibility judgments are textual.
- The packet has no working Git history to independently re-prove the complete unchanged existing-kanji tree. That claim rests on the supplied mechanical check and packet identity; the 17 supplied word diffs were independently verified.
- Some early combined retrievals were truncated; scoped card/diff evidence was subsequently read in bounded selections. The redundant `repo\kanji\艶.md` retrieval remains explicitly partial above.
- CLEAN is bounded to the reviewed evidence and stated pool assumptions, not a guarantee about every future client, content subset or dialect. No other consequential unresolved claim is being represented as verified.
- Only this report was intentionally written. No content, strokes, metadata, source evidence or other report was edited, staged, committed or pushed.
