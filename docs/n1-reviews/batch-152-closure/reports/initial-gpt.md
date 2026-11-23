Snapshot: cdd8fd016161d54a3d21cbf46450a6219f5bbedb, batch 152. Reviewer: OpenAI GPT-family assistant; the exact serving model identifier is not exposed in this runtime. Independent, blind review.

Scope:

Examined all four facets, with greatest emphasis on consistency/quiz safety and beginner comprehensibility. Packet-manifest SHA-256 independently matched `03b97635d9bf6660c29ae8e9cbc7d94bf9998a15827814d766363584a0880345`.

The following inventory distinguishes human-readable review from programmatic inspection. Paths are relative to the packet unless stated otherwise.

- **Read in full:** `INSTRUCTIONS.md`; `mechanical-checks.md`; `evidence\provenance.json`; `evidence\joyo-pages.md`; `evidence\kanjivg-components.txt`; `evidence\daijisen-heads.txt`; `evidence\kanjipedia-outside-readings.json`; `evidence\okurigana-scan.txt`; `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji-remarks.json`; `evidence\audits\word-remarks.json`; `evidence\audits\kanji_remarks.py`; `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.
- **New cards read in full:** `snapshot\kanji\趣.md`, `跳.md`, `踏.md`, `躍.md`, `較.md`, `載.md`, `輝.md`, `輩.md`, `迫.md`, `逸.md`, `遂.md`, `遣.md`, `避.md`, `郡.md`, `郷.md`.
- **Captured dictionary extracts read in full:** `evidence\public-source\weblio-趣.txt`, `weblio-跳.txt`, `weblio-踏.txt`, `weblio-躍.txt`, `weblio-較.txt`, `weblio-載.txt`, `weblio-輝.txt`, `weblio-輩.txt`, `weblio-迫.txt`, `weblio-逸.txt`, `weblio-遂.txt`, `weblio-遣.txt`, `weblio-避.txt`, `weblio-郡.txt`, `weblio-郷.txt`.
- **All 23 diffs read in full:** `diffs\kanji__仮.md.diff`, `kanji__故.md.diff`, `kanji__響.md.diff`; and `diffs\words__仮名遣い.md.diff`, `words__先輩.md.diff`, `words__小遣い.md.diff`, `words__後輩.md.diff`, `words__故郷.md.diff`, `words__比較.md.diff`, `words__比較的.md.diff`, `words__活躍.md.diff`, `words__言葉遣い.md.diff`, `words__趣味.md.diff`, `words__跳ねる.md.diff`, `words__踏む.md.diff`, `words__踏切.md.diff`, `words__載る.md.diff`, `words__輝く.md.diff`, `words__迫る.md.diff`, `words__逸れる.md.diff`, `words__遂に.md.diff`, `words__避ける.md.diff`, `words__郡.md.diff`.
- **Existing-card snapshots inspected in part:** `snapshot\kanji\仮.md` (especially lines 48–62), `故.md` (53–67), `響.md` (21–43). Complete contents were also loaded for exact replacement checks; unrelated baseline prose was not independently re-reviewed.
- **Word snapshots loaded in full programmatically, with changed passages and their surrounding context reviewed through the diffs:** `snapshot\words\仮名遣い.md`, `先輩.md`, `小遣い.md`, `後輩.md`, `故郷.md`, `比較.md`, `比較的.md`, `活躍.md`, `言葉遣い.md`, `趣味.md`, `跳ねる.md`, `踏む.md`, `踏切.md`, `載る.md`, `輝く.md`, `迫る.md`, `逸れる.md`, `遂に.md`, `避ける.md`, `郡.md`.
- **All stroke files parsed in full:** `snapshot\strokes\趣.json`, `跳.json`, `踏.json`, `躍.json`, `較.json`, `載.json`, `輝.json`, `輩.json`, `迫.json`, `逸.json`, `遂.json`, `遣.json`, `避.json`, `郡.json`, `郷.json`.
- **Structured evidence loaded in full, with focused record/output review rather than an exhaustive prose reading:** `packet-manifest.json`; `evidence\source-metadata.json`; `evidence\kanjidic2-records.xml` (the 15 target records and comparison meanings); `evidence\jmdict-families.xml` (target reading examples, restrictions, and cited-gloss checks); `evidence\jmdict-digest.tsv` (priority-family coverage); `titles\kanji-titles.tsv`; `titles\word-titles.tsv`.
- **Part human-readable, part programmatic:** `evidence\kanjivg-svgs.txt` (lines 1–120 displayed; all 15 SVGs parsed for ordered paths, stroke types and endpoints).
- **Other partial reads:** `rubric\copilot-instructions.md` (lines 1–43 and 98–129, plus heading search); `repo\docs\content-format.md` (86–154, plus heading/kanji-rule search); `repo\docs\confusable-words.md` (1–39, plus heading search); `evidence\app-code\KanjiReadings.kt` (1–210); `repo\kanji\執.md`, `施.md`, `履.md`, `全.md`, `済.md`, `運.md` (front matter and selected meaning/comparison passages; not independent reviews of those baseline cards).

Independent public verification inspected actual entries, not search snippets:

- All 15 cards' cited Kanjipedia character entries and all 15 corresponding Digital Daijisen character entries on Weblio; also Daijisen entries for 執, 施, 履 and 運.
- Live Jisho dictionary data for 趣, 趣く, 趣味, 跳ぶ, 跳ねる, 跳躍, 縄跳び, 踏む, 踏まえる, 踏襲, 踏切, 躍る, 活躍, 比較, 比較的, 較べる, 較正, 載る, 載せる, 掲載, 千載一遇, 輝く, 光輝, 輩, 先輩, 後輩, 迫る, 迫害, 逸れる, 逸らす, 逸話, 逸する, 独逸, 遂に, 遂げる, 遂行, 遂せる, 遣い, 遣う, 遣わす, 遣る, 人形遣い, 仮名遣い, 小遣い, 言葉遣い, 派遣, 避ける, 避難, 郡, 郷, 故郷 and 近郷.
- Additional Jisho entries for 迫り, 逸す, 逸る, 遣す and 避わす; full Jisho word pages for 比べる, 遣る, 独逸, 迫る and 避ける to inspect rare-form/obsolete-reading notes; live kanjiapi.dev record for 輩, including source-only やかい.
- A Jisho numeric-ID search and a kana-only つい lookup did not independently verify their intended entries; neither was counted as verification.

Verdicts:

- **Correctness: CLEAN** within the reviewed scope and limits below.
- **Scoped coverage: CLEAN.**
- **Consistency and quiz safety: NEEDS FIX** — missing direct meaning exclusions in G1–G2. The supplied full-stack curated options themselves have no established ambiguity.
- **Comprehensibility: CLEAN**, with nonblocking suggestions below.

| New card | Correctness | Coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 趣 | CLEAN | CLEAN | CLEAN | CLEAN |
| 跳 | CLEAN | CLEAN | CLEAN | CLEAN |
| 踏 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN |
| 躍 | CLEAN | CLEAN | CLEAN | CLEAN |
| 較 | CLEAN | CLEAN | CLEAN | CLEAN |
| 載 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN |
| 輝 | CLEAN | CLEAN | CLEAN | CLEAN |
| 輩 | CLEAN | CLEAN | CLEAN | CLEAN |
| 迫 | CLEAN | CLEAN | CLEAN | CLEAN |
| 逸 | CLEAN | CLEAN | CLEAN | CLEAN |
| 遂 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN |
| 遣 | CLEAN | CLEAN | CLEAN | CLEAN |
| 避 | CLEAN | CLEAN | CLEAN | CLEAN |
| 郡 | CLEAN | CLEAN | CLEAN | CLEAN |
| 郷 | CLEAN | CLEAN | CLEAN | CLEAN |

All 15 stroke files and all 23 existing-file diffs are CLEAN for their scoped changes. This does not certify unrelated baseline content.

Specific conclusions supporting these verdicts:

- All 15 front-matter on/kun lists match the pinned metadata and target KANJIDIC2 records, including order. Stroke counts, grade tags and radical metadata agree. Every metadata reading is covered or qualified; all selected quiz readings have the required linked examples. Section order is correct. The title index contains each new title exactly once.
- All 201 JSON strokes have ordered IDs and 16 finite, bounded coordinate pairs. Counts, source revision, stroke types, and ordered start/end coordinates match the pinned SVG paths; endpoints agree within rounding tolerance. The mnemonic component descriptions match the supplied KanjiVG groups. All 15 mnemonics are explicitly modern-shape memory aids, not historical explanations.
- The Joyo reading/example claims match the supplied pages, including 飛ぶ/跳ぶ, 踊る/躍る, 乗る/載る, 遣う/使う, 郷's old form, and the absence of separate suffix rows for 遣. The outside-table and source-only qualifications are substantively sound.
- The important lexical distinctions are preserved: 較正 means calibration, not its spelling-restricted proofreading sense; 較べる and 遣る are qualified appropriately; 逸れる's two readings belong to separate JMdict entries; 避ける's reading restrictions are accurately described; 郡's こおり is historical; 郷's さと does not inherit the 里-only senses. The suffix `-づか.い` is a defensible quiz selection, is supported by three linked words, and is explained as an attached form rather than an independent pronunciation of bare 遣.
- I checked every listed exclusion pair against the displayed titles and the cited senses. I found no established over-exclusion or merely transitive addition among the authored pairs. This includes the less obvious 逸/外・楽・秀・傑・優・暇・悠, 載/年・駄・置・書・積, 趣/況・姿・容・粋・味, 遂/卒・果・成・達, 遣/用・費・授・施, 輩/人・類・党・属・達, 迫/督・圧, 避/免・除, 郷/国 and 較/競. G1–G2 concern additional direct pairs, not closure of these sets.
- The requested internal-batch comparisons are sound: 跳/躍, 郡/郷 and 逸/避 should be excluded. 跳/踏, 踏/躍, 遂/迫 and 迫/避 remain distinguishable; shared foot movement or opposite direction alone does not make their displayed answers synonymous.
- All 45 curated meaning distractors are defensibly wrong in both directions. In particular, 臣/師 describe roles rather than fellowship; 既 and 必 do not mean finally; 呼/頼 do not mean dispatch; 入 is entering rather than approaching; 道 is a route rather than deviation; 証 is proof rather than comparison; 浮 is floating rather than loading. The Starter-level sets for 迫 and 逸 are easy, but coherent enough to be usable wrong options, not established defects.
- The reading audits' accounting is consistent with the option-builder code: curated choices are attempted before fallback. Thus `reading-options.txt`'s 迫/せる HIT is not a reachable wrong option in its audited full pools: 出・入・休 fill the slots first, including Starter practice. The 20 latent collision lines are not 20 production failures. The exposure audit separately identifies the two name-only one-holder cases: 載/のり with 則・法・準, and 輝/ひかる with 光. Those are genuinely drawable labels in those padded scenarios, but name readings are not themselves alternative kun answers. I found no established non-name reading collision in the pools actually audited.
- Each word diff changes exactly one line, and removing only the newly added kanji-link wrapper restores the original line. The intended target exists in all 20 cases; no Dictionary line changes. All four kanji remark replacements match the declarations exactly, with no other changes in their diffs. The titles `dispatch; usage` and `hometown; village` are exact. 響's remaining sentence reads naturally after deletion.

Findings:

**G1 — minor; consistency and quiz safety; `snapshot\kanji\踏.md:14,23,48`; `snapshot\kanji\遂.md:14,32,46–53`. Missing direct “carry out / complete” exclusions.**

The following direct pairs remain unexcluded on either side:

- 踏/遂, 踏/執, 踏/施;
- 遂/執, 遂/施, 遂/履.

This is not an inference that all related actions form a clique. Each pair has direct answer-label evidence. 踏 explicitly includes KANJIDIC2 “carry through”; its cited JMdict 踏む entry 1450270 includes “to complete,” and Kanjipedia gives ふみ行う. 遂げる entry 1372620 directly includes “to carry out.” The existing displayed titles are 執 “take hold; carry out; cling,” 施 “carry out; give; alms,” and 履 “footwear; put on shoes; carry out.” Consequently, for example, “carry out; give; alms” is defensible for a 遂 prompt, and “accomplish; at last” is defensible for 踏's documented carry-through sense. The unrelated clauses in a multi-gloss label do not remove that ambiguity.

**Impact:** the default full-stack curated sets currently mask these omissions, but the semantic-exclusion contract does not protect these pairs in reduced pools. An independent, bounded Python reproduction of the supplied meaning builder admitted both answers for each two-card pair. This demonstrates the missing guard, not a claimed shipped-session failure.

**Remedy:** declare each direct pair once, preferably on the new cards: add 執・施・遂 to 踏, and 執・施・履 to 遂. Add a short explanation if exclusions are documented in the prose.

**Evidence:** the cited pinned entries; [live Jisho 踏む](https://jisho.org/word/踏む), [live Jisho 遂げる](https://jisho.org/word/遂げる); the inspected [Daijisen 執](https://www.weblio.jp/content/執), [施](https://www.weblio.jp/content/施) and [履](https://www.weblio.jp/content/履) entries; the existing cards' exact titles/exclusion lists; `QuizBuilder.kt`. **Confidence: high on direct semantic overlap and missing declarations; limited to reduced-pool reachability for the reproduction.**

**G2 — minor; consistency and quiz safety; `snapshot\kanji\載.md:14,32,45–53`. Missing 載/運 exclusion.**

The displayed title of 運 is “carry; luck,” but 載's exclusion list omits 運, and 運 has no reciprocal exclusion. This is a direct documented sense of 載, not just an association between vehicles: JMdict 1600270 sense 3, explicitly marked *esp. 載せる*, includes “to carry.” Digital Daijisen's 載 character entry says 車・船などに物をのせる。のせて運ぶ。

**Impact:** “carry; luck” can be a defensible wrong answer for 載. The supplied full-stack curated choices remain safe; the same bounded reduced-pool reproduction admits 載 and 運 together.

**Remedy:** add 運 to 載's `quiz_exclusions` and, if retaining the explanatory list, document the direct carrying sense. No transitive additions are implied.

**Evidence:** pinned JMdict 1600270; [live Jisho 載せる](https://jisho.org/word/乗せる), sense 3; [live Daijisen 載](https://www.weblio.jp/content/載), sense 1; `repo\kanji\運.md:3,11,20–31`; `QuizBuilder.kt`. **Confidence: high on the sense and missing declaration; no full-stack production collision claimed.**

Optional:

- Shorten or separate source-audit material from the learner's main Notes, especially the long exclusion explanations on 趣, 載, 逸 and 遣. The central explanations and concrete mnemonics are understandable, but the dictionary IDs, Japanese source quotations and repeated disclaimers increase phone scrolling. Translate source quotations when they add a distinction not already explained in English; gloss “ateji” as “phonetic kanji spelling.”
- On 迫 line 51, “going outside/going inside is different from drawing near” would be more precise than “going out moves away”: exiting an enclosure does not determine movement relative to every possible destination. This does not make 出 a valid answer for 迫.

Limits:

- The exact deployed GPT model/version could not be established; I have not invented a model identifier.
- I did not consult another review, author rationale, other sessions, other packets or repository checkouts. Execution was serial, with one tool call per execution turn; no parallel calls, agents, background jobs, recursive listings or corpus-file enumeration. Title indexes were used for corpus-level title checks.
- Several early combined reads exceeded the tool's output limit and were automatically redirected by the tool. I did not open the generated out-of-packet output files; relevant packet material was reread in bounded outputs. Structured XML/JSON/SVG evidence was parsed as individual complete packet files with selected records displayed, rather than manually reading every line of those large files.
- The packet omits `repo\articles\`. Therefore the three links to `../articles/compound-sound-changes.md` on 載, 輩 and 遣 could not be independently resolved locally. I do not label them broken; their existence/content remains unverified here. Kanji and word link targets were checked separately.
- I reviewed the supplied complete audit outputs and option-building code, but did not independently recreate the entire 1,532-card reading-pool audit or test arbitrary combinations of multiple borrowed Starter cards. The reduced-pool meaning reproductions in G1–G2 are deliberately identified as such, not presented as production-session observations.
- Stroke checks did not include a rendered animation or independent resampling of every interior SVG curve point. No Android/device execution is claimed. The packet's stated JVM/Kotlin test limitation is not a finding.
- Current Jisho data does not expose every pinned search-only spelling through the same endpoint; pinned XML governed those exact flags and restrictions. The failed/irrelevant public lookups noted in Scope were not treated as source verification. No consequential source disagreement was established.
- Only the requested report file was intentionally created or modified.
