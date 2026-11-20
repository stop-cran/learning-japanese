Snapshot: `b624890f8aea8cfb6b5a08ee6beff21df5f8c807` — batch 151. Reviewer: OpenAI GPT-family GitHub Copilot; the exact deployed model/version identifier is not exposed to me. Independent, blind review. The packet-manifest SHA-256 matches `ca0ee534afc6a0ed9a73a0ccee7fc0ecf549017b2f1643dbe8c756fb3ab81cf1`; all 59 scoped snapshot files match their manifest hashes.

Scope:

Examined all four facets for every new card, all 15 stroke files, and all 29 existing-file changes. Consistency/quiz safety and beginner-phone comprehensibility received the deepest examination. Existing files were reviewed for their scoped changes, not re-reviewed as whole articles.

Files actually opened, with the extent inspected:

- **Full:** `INSTRUCTIONS.md`; `mechanical-checks.md`.
- **Part:** `rubric\copilot-instructions.md`, lines 1–129 and heading inventory; `repo\docs\content-format.md`, lines 86–154, 289–304 and heading inventory; `repo\docs\confusable-words.md`, lines 308–334 and heading inventory. Oversized initial requests are not counted as full substantive reads.
- **Full new-card prose and metadata**, within `snapshot\kanji\`: `訴.md`, `証.md`, `詩.md`, `詳.md`, `誇.md`, `誓.md`, `誘.md`, `謙.md`, `謡.md`, `譲.md`, `護.md`, `豆.md`, `豪.md`, `貢.md`, `貴.md`.
- **Full decoded JSON, including every stroke and point**, within `snapshot\strokes\`: `訴.json`, `証.json`, `詩.json`, `詳.json`, `誇.json`, `誓.json`, `誘.json`, `謙.json`, `謡.json`, `譲.json`, `護.json`, `豆.json`, `豪.json`, `貢.json`, `貴.json`.
- **Part: edited passages and adjacent context**, within `snapshot\kanji\`: `献.md` (58–60), `仮.md` (41–43), `推.md` (53–55), `縫.md` (74–76), `憩.md` (26–28), `熟.md` (50–52), `級.md` (53–55), `長.md` (39–40), `義.md` (50–52), `養.md` (28–30). Full contents were also loaded for replacement/hash checks, not for substantive review of unchanged material.
- **Part: “How the kanji combine” and adjacent context**, within `snapshot\words\`: `保証.md`, `歌謡.md`, `民謡.md`, `看護婦.md`, `訴える.md`, `証明.md`, `詩.md`, `詩人.md`, `詳しい.md`, `誇り.md`, `誓う.md`, `誘う.md`, `謙虚.md`, `謙遜.md`, `譲る.md`, `豆.md`, `豪華.md`, `貢献.md`, `貴重.md`. Full contents were additionally loaded for replacement/hash checks.
- **Full**, within `diffs\`: `kanji__献.md.diff`, `kanji__仮.md.diff`, `kanji__推.md.diff`, `kanji__縫.md.diff`, `kanji__憩.md.diff`, `kanji__熟.md.diff`, `kanji__級.md.diff`, `kanji__長.md.diff`, `kanji__義.md.diff`, `kanji__養.md.diff`; `words__保証.md.diff`, `words__歌謡.md.diff`, `words__民謡.md.diff`, `words__看護婦.md.diff`, `words__訴える.md.diff`, `words__証明.md.diff`, `words__詩.md.diff`, `words__詩人.md.diff`, `words__詳しい.md.diff`, `words__誇り.md.diff`, `words__誓う.md.diff`, `words__誘う.md.diff`, `words__謙虚.md.diff`, `words__謙遜.md.diff`, `words__譲る.md.diff`, `words__豆.md.diff`, `words__豪華.md.diff`, `words__貢献.md.diff`, `words__貴重.md.diff`.
- **Full:** `evidence\source-metadata.json`; `evidence\provenance.json`; `evidence\joyo-pages.md` (read in successive ranges); `evidence\kanjivg-components.txt`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- **Part:** `evidence\kanjidic2-records.xml` (the 15 new-kanji records); `evidence\jmdict-families.xml` (all 92 distinct families cited on the new cards, including their spelling/reading restrictions and sense notes); `evidence\jmdict-digest.tsv` (header and selected priority-bearing rows for each new kanji); `evidence\kanjivg-svgs.txt` (stroke path/type data for all 15 characters).
- **Full:** `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-exposure.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\kanji-remarks.json`; `evidence\audits\word-remarks.json`.
- **Full:** `evidence\public-source\weblio-証.txt`, `evidence\public-source\weblio-貴.txt`, `evidence\public-source\weblio-貢.txt`. Other public dictionary verification used independently retrieved live entries, not the coordinator’s extracts.
- **Full:** `evidence\app-code\QuizBuilder.kt`, `evidence\app-code\KanjiMeaningMetadata.kt`. **Part:** `evidence\app-code\KanjiReadings.kt` (1–119 and declaration inventory); `evidence\app-code\Words.kt` (216–241 and relevant declaration locations).
- **Full programmatic indexes, selected rows inspected:** `titles\kanji-titles.tsv`, `titles\word-titles.tsv`. **Part:** `packet-manifest.json` (snapshot identity, changed-file map, scoped hash records and export membership; its entire byte stream was hashed).
- **Part: title/header fields**, within `repo\kanji\`: `虚.md`, `薦.md`, `裁.md`, `舌.md`, `慮.md`, `及.md`, `羊.md`, `我.md`, `短.md`. **Part: first 45 lines**, `repo\kanji\訪.md`, `repo\kanji\満.md`, `repo\kanji\問.md`, `repo\kanji\聞.md`.

Independent public checks inspected actual entries: all 15 live Kanjipedia character entries and all 15 live Digital Daijisen character pages on Weblio; Jisho word entries covering every selected-reading example, the other reading-table examples, and consequential rare/alternative/register cases. These included 証す/証/しるし, 詩/うた, 詳らか, 誇らしい, 弘誓, 誘く, 謙る, 謡/謡う, 看護婦/看護師, 護る/護り, 豆’s prefix senses, 豪い, 年貢, 貴い/貴ぶ and 貴下/貴殿. Live Jisho character entries additionally checked the secondary meanings cited for 契 保 徴 標 密 微 請 惑 率 促 慎 救 援 剛 華 甚 献 納 幣 功. These were entry inspections, not search-snippet verification.

Verdicts:

- **Correctness: CLEAN** within the reviewed linguistic claims and changes.
- **Scoped coverage: CLEAN.** No metadata reading is silently lost, and no consequential common-use gap was established. This is not a demand for every related word.
- **Consistency and quiz safety: NEEDS FIX** — G1 and G2. Separately, 貢’s article-navigation target remains UNVERIFIED as explained below.
- **Comprehensibility: CLEAN**, with nonblocking reductions suggested under Optional.

Per-card verdicts and principal checks:

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility | Specific check |
|---|---|---|---|---|---|
| 訴 | CLEAN | CLEAN | CLEAN | CLEAN | ソ/うったえる and the grievance/legal senses check out. Default 迎/逃/戦 answers remain wrong in both directions. |
| 証 | CLEAN | CLEAN | CLEAN | CLEAN | あかし, Daijisen’s あかす and sense-qualified しるし are supported. 保証/証明 establish ショウ. |
| 詩 | CLEAN | CLEAN | CLEAN | CLEAN | The うた spelling is correctly limited to JMdict sense 3. 劇/琴/絵 are related arts, not alternative correct meanings. |
| 詳 | CLEAN | CLEAN | CLEAN | CLEAN | “Well-informed” is supported; つまびらか is qualified appropriately. No reachable attested wrong reading was found. |
| 誇 | CLEAN | CLEAN | CLEAN | CLEAN | The Joyo 誇り example legitimately illustrates the listed ほこる reading. 誇らしい’s quoted gloss matches the pinned entry. |
| 誓 | CLEAN | CLEAN | CLEAN | CLEAN | ゼイ in 弘誓 is correctly outside the official table and not selected. 断/壊/盗 do not mean vowing. |
| 誘 | CLEAN | CLEAN | NEEDS FIX — G1 | CLEAN | いざなう’s sense restriction and archaic おびく are correct. One exclusion conflates different meanings of English “call.” |
| 謙 | CLEAN | CLEAN | CLEAN | CLEAN | ケン has two valid linked examples; the kana-usual へりくだる and name readings are distinguished. |
| 謡 | CLEAN | CLEAN | CLEAN | CLEAN | ヨウ, うたい and うたう are supported; Noh chanting is accurately identified. 舞/笛/茶 remain wrong. |
| 譲 | CLEAN | CLEAN | NEEDS FIX — G2 | CLEAN | The five 譲る senses and source-only せめる are supported; the default meaning distractors are inadequately plausible. |
| 護 | CLEAN | CLEAN | CLEAN | CLEAN | 看護婦 really supplies ゴ despite its obsolete label. The warning and 看護師 pointer prevent presenting it as current usage. |
| 豆 | CLEAN | CLEAN | CLEAN | CLEAN | トウ/ズ, the まめ prefix and whole-word あずき are separated correctly; たかつき is explicitly source-only. |
| 豪 | CLEAN | CLEAN | CLEAN | CLEAN | 豪い is qualified as rare; コウ/つよい are source-only. Australia and the えら headword are supported. |
| 貢 | CLEAN | CLEAN | UNVERIFIED — article link only | CLEAN | コウ, ク→ぐ in 年貢, and みつぐ are supported. The linked sound-change article is absent from the packet. |
| 貴 | CLEAN | CLEAN | CLEAN | CLEAN | All four kun readings and the honorific use are supported. あて/むち headwords are not confused with the selected キ reading. |

Additional results applying across the batch:

- All new-card metadata matches the pinned source records, including grade, stroke count, radical and ordered on/kun lists. Every selected reading is an exact metadata subset and has the required linked example row. All 15 cards use the same appropriate section order and community-N1 qualification.
- The 15 new titles are unique in the supplied title index. I considered every declared distractor and exclusion pair against the displayed labels and ordinary secondary senses, rather than treating shared strings as sufficient evidence.
- The expressly raised within-batch distinctions are safe: 誇/豪 concern boasting versus power/excellence; 貴/豪 concern value/esteem versus power/excellence; 貢/譲 concern contributing tribute versus transferring/yielding; 証/誓 concern proof versus a vow. The 謙/譲 and 詩/謡 direct exclusions are supported. Sharing “giving something up” does not itself require a 貢/譲 exclusion.
- The broad sets generally have real supporting senses: notably 譲’s selling/postponement senses, 貢’s recommendation sense in Daijisen, 豆’s small/child prefix senses, 豪’s beyond-ordinary sense and 貴’s respectful-address use. G1 identifies a particular unsupported extension, not a request to discard all broad exclusions.
- The complete meaning simulation presents the documented three curated choices for every new card. Apart from G2’s plausibility problem, none is a second correct answer. The legal choices for 証, artistic choices for 詩/謡, food choices for 豆, and financial/coercive choices for 貢 are defensibly distinct.
- Reading accounting is internally consistent with the inspected Kotlin option builder. The reported three latent collisions are 詳/よし, 貴/ぎ and 譲/せめる, not production hits. Their curated slots or higher-closeness fallback tiers block them in the reported pools. 豆/ま and 豪/ご can occur in Starter fallback, but are explicitly KANJIDIC2 **name-only** readings, not valid answers to these kun/on questions; treating those two as informational rather than ordinary-reading failures is justified.
- The extra strings あかしとして, しょうす, しょうする, しょうとして and あてやか are word/expression forms, not automatically independent character kun readings. Their inclusion is conservative exposure checking. The obsolete つばひらか and archaic おびく are accounted for. I found no additional attested on/kun reading actually reachable as a wrong option in the supplied simulations.
- Every mnemonic is explicitly modern-shape, disclaims etymology and matches the pinned component evidence. In particular, the extra dot in 訴, hooked stroke in 誇, grouped 三 in 譲, compressed 缶 in 謡 and 中/貝 positions in 貴 are not unsupported historical claims. Linked component titles agree with the title index, allowing ordinary sentence punctuation.
- All 15 stroke files have the expected identity, revision, count, consecutive IDs, types and finite 16-point strokes. Independently resampling the raw SVG cubic paths gave a maximum point deviation of approximately 0.071 viewBox units, consistent with one-decimal rounding.
- All 19 word diffs contain exactly one removed and one added line. Removing the newly added link markup recovers the old prose; each link goes to the intended new kanji. No Dictionary line changes.
- All ten kanji edits match their declared old-to-new replacements exactly, occur in their snapshots, link existing cards and use exact quoted titles. Their new sentences read naturally. 縫’s declared replacement collapses two old physical lines into one; this is the declared remark edit, not an extra content change. Within their changed passages, all 29 existing files are CLEAN on all four facets.

Findings:

1. **G1 — minor; consistency and quiz safety; `snapshot\kanji\誘.md:14,45–52`.**

   **Claim and impact:** The 誘/訪 exclusion is justified by “call (for)” versus the displayed title “visit; call on.” These are different senses of English *call*: inviting someone to join an activity does not mean visiting that person. The actual 訪 card explicitly teaches paying a visit, whereas 誘 teaches inviting/tempting. This is an English-word association, not a direct synonym/confusable pair supported by those meanings. It unnecessarily suppresses a valid contrast and makes the explanatory list misleading.

   **Remedy:** Remove 訪 from this exclusion list, adjust the count, and remove the visiting comparison from the combined 呼/訪 bullet. Keep any independently justified 呼 comparison separate.

   **Evidence:** `repo\kanji\訪.md:19–22,37–39`; the displayed titles in `titles\kanji-titles.tsv`; live Jisho entries for [訪ねる](https://jisho.org/api/v1/search/words?keyword=%E8%A8%AA%E3%81%AD%E3%82%8B) (“to visit; to call on; to pay a visit to”) and [誘う](https://jisho.org/api/v1/search/words?keyword=%E8%AA%98%E3%81%86) (“to invite; to ask (someone to do)…”); the direct-pair rule in `repo\docs\content-format.md:122–128`.

   **Confidence:** High for the sense distinction; medium-high for the exclusion judgment.

2. **G2 — minor; consistency and quiz safety; `snapshot\kanji\譲.md:13,57`.**

   **Claim and impact:** All three default meaning distractors are remote basic actions: 食 “eat, food,” 行 “go,” and 来 “come.” They are wrong, but the set supplies no useful transfer, possession, concession or recognizable shape contrast for “hand over; yield.” This falls short of the format’s requirement for plausible wrong options; it is not a double-correct-answer bug.

   **Remedy:** Curate a more credible set of still-distinct contrasts from existing cards, without replacing them with synonyms already excluded. Recheck reading exposure after changing the list: the same field supplies reading distractors, and the current three cards also protect the Starter pool from fallback.

   **Evidence:** The actual displayed default choices in `evidence\audits\quiz-safety.txt`; `repo\docs\content-format.md:105,111–116`; `evidence\app-code\KanjiReadings.kt:107–113` and the 譲 section of `evidence\audits\reading-exposure.txt`.

   **Confidence:** Medium; this is an authored-option quality defect, not an empirical claim about learner error rates.

Optional:

- Shorten the audit-style Notes, particularly on 訴, 誘, 譲, 豪 and 貴. Keep the essential learner contrast, but move repeated dictionary-ID/exclusion justifications out of the phone reading flow where the publishing format permits. “Declaring word” could simply be “example word.” The central ideas and mnemonics are already understandable, so this is nonblocking polish.
- 看護婦 is valid evidence for ゴ and is responsibly labelled. If a suitable current linked example is available in a later authorized edit, prefer it as the primary learning example; no new word article is required to accept the present reading evidence.

Limits:

- `貢.md:32` links `..\articles\compound-sound-changes.md`. That article is not exported anywhere in this packet’s manifest, so I could not independently verify its existence/content at the snapshot. A tentative public raw-GitHub lookup returned 404 and does not establish a repository defect. The packet’s successful validator is supporting mechanical evidence, not an independent navigation check. This is why 貢’s consistency verdict is UNVERIFIED rather than CLEAN.
- This was a bounded packet review, not a whole-corpus semantic audit. Corpus-level checks used the supplied title indexes, not scans of `repo\kanji` or `repo\words`. Claims about dictionary-family coverage mean the reviewed readings, examples and selected priority rows, not exhaustive inspection of all 2,045 supplied families.
- Live sources can differ from the pinned 2026-11-17 JMdict and 2026-11-02 KANJIDIC2 records. Spelling-specific rarity and obsolete-reading flags were checked against the pinned full entries where the public API exposed less detail. Initial kanjiapi.dev requests returned HTTP 403; the relevant secondary glosses were instead verified through actual Jisho character entries.
- No device rendering, learner trial or fresh app-runtime result is claimed. I cross-read the supplied full simulations against the supplied option-building code and performed bounded read-only metadata, diff, link, hash and stroke-geometry checks.
- Some early combined reads exceeded the tool’s output limit. I did not open the generated output paths; relevant card prose and contract sections were subsequently retrieved in bounded reads. I have distinguished partial inspection from full reads above.
- All investigative tool calls were serial, with one call per tool-using assistant response. No parallel calls, subagents, other sessions, background jobs or other reviewer reports were used. No files were intentionally created or changed except this report.
- The exact runtime model identifier is unavailable; I have not invented a version number.
