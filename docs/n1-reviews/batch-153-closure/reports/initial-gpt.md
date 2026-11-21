Snapshot: cdab83b375e68d14d6d58a4866959611e949c41a — batch 153. Reviewer: ChatGPT, OpenAI GPT family; the exact deployed model/version is not exposed to this reviewer. The packet-manifest SHA-256 matches a6cf90a441161bb169e8ba911c593fb52ea20fc2506cbaa4f47ee7f29f0ac12c.

Scope:

Independent, blind review of all 15 new kanji cards, all 15 stroke files, and all 21 modified-file diffs. Facets 3 and 4 received the deepest attention. Existing articles were reviewed only for their scoped changes, not recertified in full.

All paths below are relative to `batch-153-cdab83b3`. “Full, programmatic” distinguishes parsing/checking the complete file from reading every line as prose.

- **Full:** `INSTRUCTIONS.md`, `mechanical-checks.md`, `rubric\copilot-instructions.md`.
- **Full, programmatic; opening sections also inspected as text:** `packet-manifest.json`.
- **Full:** `snapshot\kanji\醜.md`, `snapshot\kanji\酌.md`, `snapshot\kanji\酔.md`, `snapshot\kanji\酢.md`, `snapshot\kanji\釈.md`, `snapshot\kanji\釣.md`, `snapshot\kanji\鈴.md`, `snapshot\kanji\銃.md`, `snapshot\kanji\銭.md`, `snapshot\kanji\鎖.md`, `snapshot\kanji\鐘.md`, `snapshot\kanji\鑑.md`, `snapshot\kanji\附.md`, `snapshot\kanji\陥.md`, `snapshot\kanji\陰.md`.
- **Part:** `snapshot\kanji\属.md`, the changed Notes passage.
- **Full, programmatic:** `snapshot\strokes\醜.json`, `snapshot\strokes\酌.json`, `snapshot\strokes\酔.json`, `snapshot\strokes\酢.json`, `snapshot\strokes\釈.json`, `snapshot\strokes\釣.json`, `snapshot\strokes\鈴.json`, `snapshot\strokes\銃.json`, `snapshot\strokes\銭.json`, `snapshot\strokes\鎖.json`, `snapshot\strokes\鐘.json`, `snapshot\strokes\鑑.json`, `snapshot\strokes\附.json`, `snapshot\strokes\陥.json`, `snapshot\strokes\陰.json`.
- **Part, changed line and complete “How the kanji combine” section in each:** `snapshot\words\図鑑.md`, `snapshot\words\日陰.md`, `snapshot\words\欠陥.md`, `snapshot\words\解釈.md`, `snapshot\words\酌む.md`, `snapshot\words\酔う.md`, `snapshot\words\酔っ払い.md`, `snapshot\words\酢.md`, `snapshot\words\醜い.md`, `snapshot\words\金銭.md`, `snapshot\words\釣り.md`, `snapshot\words\釣り合う.md`, `snapshot\words\釣る.md`, `snapshot\words\鈴.md`, `snapshot\words\銃.md`, `snapshot\words\鎖.md`, `snapshot\words\鐘.md`, `snapshot\words\鑑賞.md`, `snapshot\words\附属.md`, `snapshot\words\陰.md`.
- **Full:** `diffs\kanji__属.md.diff`; `diffs\words__図鑑.md.diff`, `diffs\words__日陰.md.diff`, `diffs\words__欠陥.md.diff`, `diffs\words__解釈.md.diff`, `diffs\words__酌む.md.diff`, `diffs\words__酔う.md.diff`, `diffs\words__酔っ払い.md.diff`, `diffs\words__酢.md.diff`, `diffs\words__醜い.md.diff`, `diffs\words__金銭.md.diff`, `diffs\words__釣り.md.diff`, `diffs\words__釣り合う.md.diff`, `diffs\words__釣る.md.diff`, `diffs\words__鈴.md.diff`, `diffs\words__銃.md.diff`, `diffs\words__鎖.md.diff`, `diffs\words__鐘.md.diff`, `diffs\words__鑑賞.md.diff`, `diffs\words__附属.md.diff`, `diffs\words__陰.md.diff`.
- **Full:** `evidence\source-metadata.json`, `evidence\provenance.json`, `evidence\joyo-pages.md`, `evidence\kanjipedia-outside-readings.json`, `evidence\daijisen-heads.txt`, `evidence\okurigana-scan.txt`, `evidence\kanjivg-components.txt`.
- **Part, substantive inspection; complete XML parsed:** `evidence\kanjidic2-records.xml` — the 15 target records; `evidence\jmdict-families.xml` — card-cited entries and applicable sense, spelling and reading restrictions.
- **Part, targeted rows after reading the index programmatically:** `evidence\jmdict-digest.tsv`, including the consequential rare-form/register entries.
- **Full, programmatic; opening SVG text also inspected:** `evidence\kanjivg-svgs.txt`, all 15 SVG path sets.
- **Full:** `evidence\public-source\weblio-醜.txt`, `evidence\public-source\weblio-酌.txt`, `evidence\public-source\weblio-酔.txt`, `evidence\public-source\weblio-酢.txt`, `evidence\public-source\weblio-釈.txt`, `evidence\public-source\weblio-釣.txt`, `evidence\public-source\weblio-鈴.txt`, `evidence\public-source\weblio-銃.txt`, `evidence\public-source\weblio-銭.txt`, `evidence\public-source\weblio-鎖.txt`, `evidence\public-source\weblio-鐘.txt`, `evidence\public-source\weblio-鑑.txt`, `evidence\public-source\weblio-附.txt`, `evidence\public-source\weblio-陥.txt`, `evidence\public-source\weblio-陰.txt`.
- **Full:** `evidence\audits\quiz-safety.txt`, `evidence\audits\reading-exposure.txt`, `evidence\audits\reading-options.txt`, `evidence\audits\word-remarks.json`, `evidence\audits\kanji-remarks.json`.
- **Full:** `evidence\app-code\QuizBuilder.kt`. **Part:** `evidence\app-code\KanjiReadings.kt`, lines 1–185, including the reading-option builder.
- **Full, programmatic index checks with targeted entries inspected:** `titles\kanji-titles.tsv`, `titles\word-titles.tsv`.
- **Part:** `repo\docs\content-format.md`, lines 1–180; `repo\docs\confusable-words.md`, lines 1–39 and targeted search hits concerning exclusions/direct pairs.
- **Full:** `repo\kanji\捕.md`. **Part:** `repo\kanji\誘.md`, opening 55 lines.

Independent public verification inspected the actual Kanjipedia and Digital Daijisen character entries linked by all 15 cards, rather than relying solely on packet retrievals. Jisho/JMdict word responses covered:

醜, 醜い, 醜態, 酌む, 晩酌, 酔う, 酔い, 麻酔, 酔っ払い, 酢, 酢酸, 解釈, 釈然, 釣る, 釣り, 釣り合う, 釣果, 鈴, 予鈴, 風鈴, 銃, 銭, 金銭, 小銭, 銭ころ, 鎖, 鎖す, 鎖国, 鐘, 警鐘, 鐘楼, 鑑, 図鑑, 鑑賞, 鑑みる, 附属, 附ける, 附く, 附子, 附す, 附する, 欠陥, 陥る, 陥れる, 陰, 日陰, 陰気, 陰る, 陰うつ, 陰に, 陰にこもる. Relevant Jisho kanji pages and Digital Daijisen’s separate 陥れる headword were also inspected.

Verdicts:

- Correctness: **CLEAN**.
- Scoped coverage: **CLEAN**.
- Consistency and quiz safety: **NEEDS FIX** — G1, missing direct exclusions on 陥; the supplied default full-pool simulations do not exhibit that ambiguity.
- Comprehensibility: **CLEAN**, with optional shortening below.

Per-file differences: `snapshot\kanji\陥.md` has consistency/quiz-safety **NEEDS FIX**. That facet on `snapshot\kanji\酢.md` is **UNVERIFIED only for the independently unresolved article-link target described in Limits**, not for its quiz options. Other facets on those cards, and all four facets on the other 13 new cards, are CLEAN within this review. All 21 scoped existing-file edits are CLEAN.

The following checks cover every new card; the options column records its three curated meaning distractors, judged in both directions.

| Card | Reading, sense and teaching checks | Curated meaning options |
|---|---|---|
| 醜 | みにく.い and シュウ examples agree with sources. しこ’s derogatory/rare and humble-use qualifications are supported. にくむ and たぐい are separately identified outside-table material. | 短・赤・新: easy but defensibly wrong. |
| 酌 | 酌む’s pouring and considering senses are supported; 晩酌 supplies シャク. The considering comparisons are not justified merely by sharing a drinking topic. | 煮・焼・絞: food/drink-adjacent actions, not pouring or ladling. |
| 酔 | よ.う, よ.い and よ are properly distinguished within the stated stem-grouping convention. 麻酔 supports スイ; “poisoned” and “spellbound” are sourced secondary meanings, not the central modern lesson. | 眠・疲・泣: distinguishable states/actions, not intoxication. |
| 酢 | す and サク/酢酸 are supported. ソ and すい remain qualified Notes material. The reciprocal-cup account supports the historical むくいる discussion. | 塩・麦・油: distinct ingredients/materials. |
| 釈 | 解釈 supports シャク; 釈然 has both しゃくぜん and せきぜん. とく, す.てる and ゆる.す are honestly source-only rather than furnished with invented examples. | 書・聞・学: easy but distinct from interpreting/explaining. |
| 釣 | つ.る, チョウ, つ.り and つ.り- have appropriate examples; the trailing dash is explained. The change-from-a-purchase sense is genuine but does not make “coin; sen” an equivalent definition. | 刈・掘・潜: plausible outdoor actions, not angling/luring. |
| 鈴 | すず, レイ/予鈴 and リン/風鈴 are supported. The small-bell versus hanging-bell contrast is appropriately conservative; the 鈴/鐘 exclusion is needed and need only be declared once. | 笛・琴・扇: distinct objects. |
| 銃 | ジュウ and archaic つつ are supported, including the cited JMdict register. Kanjipedia’s 鉄砲 description supports the firearm account. | 剣・矢・盾: distinct weapons/equipment. |
| 銭 | セン, ぜに and the sen unit are supported. ゼン/すき are not given fabricated productive examples; ぜぜ and ちゃん are qualified secondary material. | 鉢・針・税: neither containers, needles nor a tax is a coin/unit. |
| 鎖 | くさり and サ/鎖国 are sound. とざ.す is a rare kanji spelling; さす is separately sourced and register-qualified, not falsely attributed to KANJIDIC2. | 縄・針・帯: a rope/cord or sash can bind, but is not a chain or “shut.” |
| 鐘 | かね and ショウ are supported; シュ/鐘楼 しゅろう is correctly distinguished from the KANJIDIC2 list. The dictionary clock sense supports the time-related exclusions. | 旗・柱・瓶: distinct physical objects. |
| 鑑 | カン, かんが.みる and かがみ are supported. Model/appraisal/reference-book senses and the qualified 鏡 spelling account agree with the cited sources. | 層・頂・塔: distinct structural/positional concepts. |
| 附 | フ/附属 is correctly tied to the 付属 family. 附ける/附く are rare spellings; ブ/附子 is independently attested and not called a KANJIDIC2 reading. Attaching, accompanying, handing over and entrusting are sourced. | 外・出・間: easy spatial contrasts, not affixing/appending. |
| 陥 | カン/欠陥, おちい.る and おとしい.れる are supported. The lacking, pitfall and castle senses are real. Its taught active capture/lure sense creates G1’s missing direct pairs. | 昇・跳・浮: upward/remaining-up contrasts are defensibly wrong. |
| 陰 | かげ, イン and かげ.る are supported; outside-table オン, アン, くらい and ひそか are qualified. The 影 distinction, 陽 opposite and time/north dictionary senses are sourced. | 陽・光・炎: contrasting sunshine/light/flame, not shade or yin. |

Across all 15, the checked front matter matches the pinned metadata: on/kun lists, grade, radical, stroke count and selected quiz subsets. Each enabled quiz reading has a linked word example. Titles pass the index uniqueness check; card/word links and quoted card titles checked against the indexes resolve as intended, subject to the separate article-link limit below. Sections and headings follow the kanji format.

All 15 mnemonics are explicitly modern-shape memory aids, not historical derivations. The component positions and decompositions agree with the pinned KanjiVG groups, including the potentially misleading 鬼/甶/儿, 令, 戋, ⺌/貝, 𠂊/旧 and 今/云 cases. All 15 stroke files have matching stroke counts, revision, IDs/types, valid coordinates/bounds and SVG stroke endpoints. This was a structural/source comparison, not a phone-animation test.

The card prose distinguishes important rare/source-only forms rather than presenting them as ordinary productive readings. Applicable JMdict spelling restrictions were checked, including the 日陰 versus 日影 sunshine restriction and the separate 附子 readings/entries. No in-scope JMdict attribution lacking its cited entry ID was established. Words embedded in quoted Japanese dictionary definitions and fragments of longer words are not missing-example defects.

For meaning quizzes, all 45 curated distractors are defensibly wrong in both directions. The declared exclusions were considered as direct pairs against displayed titles and sourced secondary senses, not inferred transitively. No established unnecessary-clique defect was found. The specifically raised nonexcluded pairs 酔/酒, 銭/銅, 鈴/鳴 and 陰/陽 remain distinguishable; so do the other proposed within-batch pairs except the unlisted 陥/釣 overlap in G1.

For reading quizzes, the complete audits support zero production, padded-session or one-holder hits. Their eight latent collisions are 醜 にくむ/たぐい, 釈 しゃ/おく, 鎖 さす, 附 ぶ and 陰 おん/くらい. The two HIT labels in `reading-options.txt` do not establish reachable wrong answers: 醜’s and 釈’s curated options already fill the slots before those fallback holders are considered. No actual attested-reading collision was established in the supplied shipped-pool questions.

Some curated cards have no selected reading of the asked kind: 扇 for 鈴’s kun prompt, 矢 for 銃’s on prompt, and 跳 for 陥’s on prompt. These are handled by the actual builder’s fallback, not by displaying an empty or invented reading. The audited fallbacks are safe; for example, 銃 receives ケン・ジュン・ジョウ rather than a nonexistent on-reading from 矢.

The okurigana extras are grounded in the supplied headwords and public word entries. Historical 酔 variants and archaic 銭ころ are not silently promoted to ordinary readings. The 陰うつ/陰に/陰にこもる strings are conservative whole-headword audit inputs, not evidence that the whole string is a single-character kun reading.

The 20 word diffs each change exactly one line. Eighteen are link-wrap only; 附属 and 酌む additionally delete exactly their declared obsolete no-card sentence. No `Dictionary:` line changes. The 属 diff changes exactly its declared clause to `and [附](附.md), "affix; append," in 附属;`; the target exists, its title matches, and the resulting passage reads naturally. The other changed passages also retain their meaning and grammar.

Findings:

**G1 — Minor; facet 3, consistency and quiz safety; `snapshot\kanji\陥.md:14,33`. Missing direct exclusions allow two taught meanings to become “wrong” answers in custom pools.**

- **Claim:** 陥 explicitly teaches 陥れる as “to capture (a castle, fortress, etc.)”; its cited JMdict entry also explicitly gives “to lure (into a trap).” Nevertheless, neither 陥/捕 nor 陥/釣 is excluded on either side. The existing displayed titles are 捕 **“capture”** and 釣 **“angling; lure.”** These are direct overlaps with that taught verb, not a transitive inference through some third excluded card.
- **Demonstrated impact:** The default full-pool questions are protected by 陥’s three available curated distractors. However, the supplied builder also supports custom pools. Applying its selection/exclusion rules to the four-card pool `{陥, 捕, 酢, 鈴}` offers **“capture”** beside **“fall into; cave in”** for 陥. The pool `{陥, 釣, 酢, 鈴}` likewise offers **“angling; lure.”** All three eligible alternatives fit, so tie shuffling does not remove the overlap. A learner using the card’s taught おとしいれる sense has a defensible alternative answer. This is bounded custom-pool exposure, not a claim that the supplied full-pool simulation failed.
- **Remedy:** Add 捕 and 釣 to 陥’s `quiz_exclusions`, with a short explanation referring directly to 陥れる’s capture/lure senses. A declaration on 陥 alone suffices; retain its safe curated distractors.
- **Evidence:** `evidence\jmdict-families.xml`, entry **1216130**, senses 1–2 and their 陥れる spelling applicability; independently checked [Jisho/JMdict response](https://jisho.org/api/v1/search/words?keyword=%E9%99%A5%E3%82%8C%E3%82%8B) and [Digital Daijisen’s 陥れる entry](https://www.weblio.jp/content/%E9%99%A5%E3%82%8C%E3%82%8B); `snapshot\kanji\釣.md:3,14`; `repo\kanji\捕.md:3` and its front matter; `evidence\app-code\QuizBuilder.kt`; the documented custom-pool/exclusion contract in `repo\docs\content-format.md`.
- **Confidence:** High for the direct lexical overlaps and absent exclusions; high for the supplied-builder custom-pool exposure. Severity is minor because the default fully populated questions remain safe.

Optional:

- Shorten the provenance-heavy exclusion explanations, especially on 鑑 and 附. Their central explanations and labelled mnemonics are usable, and the bullets avoid an unbroken wall of text, but the long Notes sections impose substantial phone scrolling. Keep the useful learner contrasts and the exclusion metadata; compress repeated source quotations/entry-number explanations rather than adding more examples.
- The Starter-level distractors for 醜, 釈 and 附 are unusually easy. They are still plausible enough and unambiguously wrong; increasing difficulty is editorial polish, not a required correction, and should not compromise their reading-option safety.

Limits:

- The 酢 card’s link to `../articles/compound-sound-changes.md` cannot be independently resolved from this packet: its article text is not exported and the title indexes cover kanji/words, not articles. A public raw-file attempt did not supply the exact-snapshot target. The mechanical check reports successful links, but I have not independently verified this one article’s existence/content. This is an evidence limit, not an established broken-link finding.
- The runtime does not expose an exact model/version identifier; none is invented above.
- The custom-pool demonstration is an in-memory application of the supplied Kotlin selection rules, not an instrumented app run. Stroke checks did not render animations or independently reconstruct every interior resampling point.
- Whole XML/index files were sometimes parsed to select applicable evidence; that does not mean every unrelated dictionary entry or corpus card was linguistically reviewed. Existing word-article material outside the changed passages remains outside this review.
- Dictionary conclusions concern the cited senses and stated registers; archaic, name-only and source-only readings are not claims of present-day frequency.
- No other reviewer report or author rationale was sought. No agents, other sessions, background jobs, parallel tool calls, recursive listings or whole-corpus scans were used. Some long tool responses were truncated; relevant allowed packet evidence was reread in smaller portions. No automatically suggested temporary-output path was opened.
