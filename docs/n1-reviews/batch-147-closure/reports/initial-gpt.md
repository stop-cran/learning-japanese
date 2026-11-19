Snapshot: `6a2323e759d4e4f2e78bc039c8b9eb8914ac2d0c` — batch 147. Reviewer: OpenAI GPT; the exact deployed model/version is not exposed to this reviewer. Independent, blind, read-only review.

Scope:

All paths below are relative to `batch-147-6a2323e7`, unless stated otherwise. Facets 3 and 4 received the deepest examination.

**Teaching content and patches**

- **Read in full:** `snapshot\kanji\瞬.md`, `瞳.md`, `矢.md`, `砕.md`, `礎.md`, `秀.md`, `秘.md`, `稚.md`, `稼.md`, `稿.md`, `穏.md`, `穴.md`, `笛.md`, `粋.md`, `糧.md` — each filename after the first has the same directory.
- **Read in part:** `snapshot\kanji\基.md:47–66`, `snapshot\kanji\密.md:45–59`, `snapshot\kanji\透.md:17–34`. These cover the changed sentences and their surroundings; their complete texts were also machine-read for link checks, not reviewed as additional scope.
- **Read in full:** `snapshot\words\一瞬.md`, `優秀.md`, `原稿.md`, `基礎.md`, `幼稚.md`, `幼稚園.md`, `瞬間.md`, `瞳.md`, `矢印.md`, `砕く.md`, `砕ける.md`, `秘密.md`, `稼ぐ.md`, `穏やか.md`, `穴.md`, `笛.md`, `純粋.md`, `食糧.md` — all under `snapshot\words`.
- **Full JSON parsed and structurally checked:** `snapshot\strokes\瞬.json`, `瞳.json`, `矢.json`, `砕.json`, `礎.json`, `秀.json`, `秘.json`, `稚.json`, `稼.json`, `稿.json`, `穏.json`, `穴.json`, `笛.json`, `粋.json`, `糧.json` — all under `snapshot\strokes`. Checks covered identities, counts, ordered IDs, sampling, finite coordinates and view-box bounds; component bounding boxes were additionally examined for 秀 and 粋. This was not an animated handwriting review.
- **Read all 21 diffs in full:** `diffs\kanji__基.md.diff`, `kanji__密.md.diff`, `kanji__透.md.diff`; `diffs\words__一瞬.md.diff`, `words__優秀.md.diff`, `words__原稿.md.diff`, `words__基礎.md.diff`, `words__幼稚.md.diff`, `words__幼稚園.md.diff`, `words__瞬間.md.diff`, `words__瞳.md.diff`, `words__矢印.md.diff`, `words__砕く.md.diff`, `words__砕ける.md.diff`, `words__秘密.md.diff`, `words__稼ぐ.md.diff`, `words__穏やか.md.diff`, `words__穴.md.diff`, `words__笛.md.diff`, `words__純粋.md.diff`, `words__食糧.md.diff` — all under `diffs`.

**Contracts, sources and implementation**

- **Read in full:** `INSTRUCTIONS.md`; `mechanical-checks.md`; `evidence\source-metadata.json`; `evidence\provenance.json`; `evidence\joyo-pages.md`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- **Read in full:** `evidence\audits\quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`, `kanji-remarks.json`, `word-remarks.json`, `kanji_remarks.py` — all under `evidence\audits`.
- **Read in full:** `evidence\public-source\weblio-瞬.txt`, `weblio-瞳.txt`, `weblio-矢.txt`, `weblio-砕.txt`, `weblio-礎.txt`, `weblio-秀.txt`, `weblio-秘.txt`, `weblio-稚.txt`, `weblio-稼.txt`, `weblio-稿.txt`, `weblio-穏.txt`, `weblio-穴.txt`, `weblio-笛.txt`, `weblio-粋.txt`, `weblio-糧.txt` — all under `evidence\public-source`.
- **Read in part:** `evidence\kanjidic2-records.xml` — the 15 new characters' metadata and reading records; `evidence\jmdict-families.xml` — all entries cited in the 15 cards' Metadata lines, examining written forms, reading restrictions, senses, parts of speech and register; `evidence\jmdict-digest.tsv` — opening rows and targeted priority-word rows for every new character. Large dictionary evidence was queried by relevant records rather than printed wholesale.
- **Read in part:** `rubric\copilot-instructions.md:1–129`; `repo\docs\content-format.md:86–205,289–304,1418–1434`; `repo\docs\confusable-words.md:1–39`, plus matching quiz-related lines/headings.
- **Read in full:** `evidence\app-code\QuizBuilder.kt`, `evidence\app-code\KanjiMeaningMetadata.kt`. **Read in part:** `evidence\app-code\KanjiReadings.kt:1–140`; `evidence\app-code\Words.kt:216–241`, plus matching declarations.
- **Read in full as targeted context:** `repo\kanji\目.md`, `美.md`, `恋.md`, `念.md`, `熟.md`, `備.md`, `貯.md` — all under `repo\kanji`.
- **Indexes:** `titles\kanji-titles.tsv` and `titles\word-titles.tsv` were fully parsed; headers and relevant records were inspected, not every row read as prose. The kanji index supplied title-uniqueness checks, semantic candidates and every curated distractor/exclusion's displayed title.
- **Read in part:** `packet-manifest.json:1–25`; the complete file was hashed. Its SHA-256 matches `39afd4115e2e68d2a09419c16590cdab000fb8351e08f68337903067b660952c`.

**Independent public verification**

Actual entries, not search snippets: all 15 live Kanjipedia character entries at the URLs in `kanjipedia-outside-readings.json`; Digital Daijisen on Weblio for 秀, 稼 and 稚い; live Jisho/JMdict entries for 一瞬, 瞬間, 優秀, 原稿, 基礎, 幼稚, 幼稚園, 瞳, 矢印, 砕く, 砕ける, 秘密, 稼ぐ, 穏やか, 穴, 笛, 純粋, 食糧, 瞬く, 瞬ぐ, 矢, 礎, 秀でる, 秘める, 密か, 稚い, 稼働, 稿, 平穏, 粋, 糧, 兵糧 and 温和. Live KANJIDIC-mirror requests failed with HTTP 403.

Verdicts:

- **Correctness: NEEDS FIX** — G1–G4.
- **Scoped coverage: CLEAN** — all 15 cards retain and account for their pinned metadata readings; each selected quiz reading has an appropriate linked example. No consequential common-usage omission established.
- **Consistency and quiz safety: NEEDS FIX** — G5–G6. No invalid answer among the three curated meaning distractors of any new card was established.
- **Comprehensibility: NEEDS FIX** — the concrete shape/spelling explanations in G1–G3 mislead the intended beginner. Other presentation suggestions are optional.

Per-card verdicts, including cards with no findings:

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 瞬 | CLEAN | CLEAN | CLEAN | CLEAN |
| 瞳 | CLEAN | CLEAN | CLEAN | CLEAN |
| 矢 | CLEAN | CLEAN | NEEDS FIX — G5 | CLEAN |
| 砕 | CLEAN | CLEAN | CLEAN | CLEAN |
| 礎 | CLEAN | CLEAN | CLEAN | CLEAN |
| 秀 | NEEDS FIX — G1 | CLEAN | CLEAN | NEEDS FIX — G1 |
| 秘 | CLEAN | CLEAN | NEEDS FIX — G6 | CLEAN |
| 稚 | NEEDS FIX — G3 | CLEAN | NEEDS FIX — G5 | NEEDS FIX — G3 |
| 稼 | CLEAN | CLEAN | CLEAN | CLEAN |
| 稿 | CLEAN | CLEAN | CLEAN | CLEAN |
| 穏 | NEEDS FIX — G4 | CLEAN | CLEAN | CLEAN |
| 穴 | CLEAN | CLEAN | NEEDS FIX — G6 | CLEAN |
| 笛 | CLEAN | CLEAN | CLEAN | CLEAN |
| 粋 | NEEDS FIX — G2 | CLEAN | CLEAN | NEEDS FIX — G2 |
| 糧 | CLEAN | CLEAN | NEEDS FIX — G5 | CLEAN |

The 18 word articles, 15 stroke files, and scoped changes to 基・密・透 are **CLEAN** within their respective reviewed scope. The 15 link-only word diffs introduce only the intended link wrappers. The other three word diffs and three kanji diffs match their declared remark changes; no additional change was found. All added links point to the intended cards. A bounded check of the scoped articles found **492 resolving relative links**, including every required declared-kanji link.

**Quiz and teaching judgments**

- All 15 titles are unique in the title index. The displayed curated alternatives in the full meaning simulation are defensibly wrong in both directions. Reusing 木・私・秒・税 is not itself a defect: the shape relationships are recognizable and their displayed meanings remain distinct. 穏's explanation honestly uses a mnemonic field/plant association for 田・花, rather than claiming they are components.
- The 砕 mnemonic says the right side *looks like* 九 over 十; this is an acceptable modern-shape description of 卆, unlike G2's identification with the full 卒. 礎's trees over an unnamed lower shape, 穴's 宀 over 八, 笛's ⺮ over 由 and 糧's 米 beside 量 are defensible.
- 瞬's blink/instant title and qualified kun discussion, 瞳's ドウ/トウ distinction, 矢's wedge sense, 稼's explicitly Daijisen-sourced 禾稼, and 笛's qualified ジャク/obsolete ちゃく account are supported. The live Kanjipedia page independently confirms ジャク; it need not become a quiz prompt.
- The declared 瞬/瞳 and 粋/秀 exclusions work symmetrically without reciprocal duplication. 礎/基 is likewise covered. 稼's harvested grain and 稿's straw are not interchangeable meanings, and do not establish another exclusion merely by agricultural association.
- The 13 砕 exclusions were considered individually against physical, simplifying and worry senses; the relevant verb-family senses are actually present in JMdict. They are not inferred merely by taking transitive closure through another card.
- The reading audits' accounting is sound within their documented pools. The seven latent lines concern 矢/さ, 秀/ほ, 稚/わく, 稼/うえる, 穏/やすらか, 穴/しし and 笛/う. They are not seven production failures. The separately reported drawable name-only しょう and な do not become on/kun defects.
- In particular, 穏's three curated cards 木・田・花 have usable kun options and fill all three wrong slots, including in the documented Starter pool. `KanjiReadings.kt` adds curated choices before fallback. The older reading-options `HIT` for 安's やすらか therefore does **not** establish a drawable wrong option. 稼's missing kun option on 秒 really does cause fallback; its audited fallback does not expose うえる.

Findings:

### G1 — Major; correctness and comprehensibility; `snapshot\kanji\秀.md:27`

**Claim and impact:** The mnemonic places 禾 “at the left” and 乃 “at the right.” 秀 is arranged vertically: 禾 above 乃. This gives a beginner an incorrect construction for the character and contradicts the correct description retained in `snapshot\kanji\透.md:27`.

**Remedy:** Say 禾 is at the top and 乃 below it; retain the modern-shape qualification.

**Evidence:** The supplied seven-stroke geometry places strokes 1–5 across the upper character and strokes 6–7 below them. The [live Kanjipedia 秀 entry](https://www.kanjipedia.jp/kanji/0003100600) identifies the two components; the displayed glyph and packet geometry establish their positions.

**Confidence:** High.

### G2 — Major; correctness and comprehensibility; `snapshot\kanji\粋.md:33`

**Claim and impact:** “Find … 卒 … at the right” identifies the wrong modern shape. 粋 contains the four-stroke 卆-shaped part; full 卒 belongs to the old form 粹. A disclaimer about etymology does not make the visible-component identification true.

**Remedy:** Describe the right side as a 九-like shape above 十, or identify 卆 with an explicit explanation. Do not direct learners to find full 卒 in modern 粋.

**Evidence:** `snapshot\strokes\粋.json` has six 米 strokes followed by four right-side strokes. The [live Kanjipedia 粋 entry](https://www.kanjipedia.jp/kanji/0003745600) distinguishes ten-stroke 粋 from fourteen-stroke 粹 and explicitly discusses 卒 in the **old** form.

**Confidence:** High.

### G3 — Minor; correctness and comprehensibility; `snapshot\kanji\稚.md:40`

**Claim and impact:** For the written form 稚い, the card says “稚 writes いとけ and ない is the adjective ending.” That allocation would require a spelling ending in ない, not the displayed 稚い. It teaches the wrong kanji/kana boundary.

**Remedy:** For 稚い read いとけない, explain that 稚 writes いとけな and the written okurigana is い. Keep the pinned metadata reading unchanged; distinguish other spellings only if useful.

**Evidence:** JMdict entry **2863360** separately lists 稚い, 稚けない and search-only 稚ない. [Daijisen's actual 稚い entry](https://www.weblio.jp/content/稚い) reads いとけない, and [Kanjipedia](https://www.kanjipedia.jp/kanji/0004686000) gives the boundary いとけな・い.

**Confidence:** High.

### G4 — Minor; correctness; `snapshot\kanji\穏.md:39`

**Claim and impact:** The sentence attributes JMdict's “mild (climate); temperate; clement; pleasant; agreeable” sense to **穏和**. In the cited family, that sense is explicitly restricted to **温和**. This is a spelling-specific sense error, not merely failure to mention the family's first spelling.

**Remedy:** Illustrate 穏和 with the unrestricted gentle-personality or moderate-statement sense, or explicitly distinguish 温和 for the climate sense. Retain the genuine Joyo example 穏和.

**Evidence:** `evidence\jmdict-families.xml`, entry **1589620**, sense 1 has `<stagk>温和</stagk>`; senses 2–3 are unrestricted. The [independently retrieved live entry](https://jisho.org/api/v1/search/words?keyword=%E6%B8%A9%E5%92%8C) preserves that restriction.

**Confidence:** High.

### G5 — Minor; consistency and quiz safety; unjustified direct exclusions

**Files and lines:** `snapshot\kanji\矢.md:14,46`; `snapshot\kanji\稚.md:14,52`; `snapshot\kanji\糧.md:14,49`.

**Claim and impact:** Several edges substitute association or opposition for a direct answer ambiguity:

- **矢/恋 and 矢/念:** romantic interest and direction of attention are senses of the compound **矢印**, not established ordinary meanings of 矢 “arrow; wedge.” Neither “romantic love; longing” nor “thought; attention” becomes a correct answer for 矢 through that compound.
- **稚/熟:** “immature; childish; young” and “ripen; mature; skilled” are contrasting answers, not synonyms. Quoting “not yet mature” does not create overlap with “mature.”
- **糧/貯 and 糧/備:** food provisions can be stored or prepared, but 糧 does not thereby mean “save up; store” or “prepare; equip.”

These are unnecessary symmetric exclusions, including between potential wrong options, and the explanations teach inaccurate semantic equivalence.

**Remedy:** Remove these five edges unless direct sense evidence is supplied. Keep useful contrasts or associations in prose, expressly as contrasts or associations.

**Evidence:** The actual displayed titles in `titles\kanji-titles.tsv`; JMdict entries **1537760**, **1537770** and the cited 稚/糧 families; live Kanjipedia character senses; the full targeted context cards 恋・念・熟・貯・備. `content-format.md:118–125` and the review rubric require direct, evidence-based pairs rather than shared topics.

**Confidence:** High.

### G6 — Minor; consistency and quiz safety; `snapshot\kanji\穴.md:14,23` and `snapshot\kanji\秘.md:3,14`

**Claim and impact:** The converse problem is a missing direct English-answer overlap. 穴's own explanation cites its ordinary secondary sense **“good place not many people know about; well-kept secret,”** yet neither card excludes the other. 秘's displayed title begins **“secret.”** A learner who knows that cited sense can defend that option for 穴; the bare English choice supplies no place-versus-information qualification.

**Remedy:** Declare the direct 穴/秘 exclusion once, on either card. No title distortion or removal of 穴's genuine secondary sense is necessary.

**Evidence:** JMdict **1254480**, sense 7, and its [independently retrieved live entry](https://jisho.org/api/v1/search/words?keyword=%E7%A9%B4); Kanjipedia 穴 sense ③ independently supports the advantageous, little-known-place sense. The two headers lack the pair, and `QuizBuilder.kt` has no semantic filter beyond declared exclusions and exact-title deduplication.

**Exposure qualification:** The supplied default full-pool simulation fills both cards' three curated slots, so it does **not** demonstrate this pair currently displayed together. This is a missing semantic guard for fallback/narrowed meaning choices covered by the format contract, not a claimed production hit or a reading-quiz collision.

**Confidence:** High for the lexical overlap and missing guard; no production-frequency claim.

Optional:

- Shorten the learner-facing reference material, especially 瞬's alternative-reading paragraph, 秘's final Notes bullet, 稚's source-only catalogue, 稿's final Notes bullet and 糧's long reading-holder list. The central explanations are accessible, but repeated audit assurances and many unlinked advanced compounds interrupt phone-sized lessons. Keep the evidence, but separate concise teaching from reference detail.
- In `秀.md:46`, replace “its title and reading overlap this card” with “its title and the meaning of すぐれる overlap this card's meaning.” This avoids suggesting that 優's すぐれる is itself a listed reading of 秀.
- “The other kanji in 基礎 is 礎” would read more naturally than the revised 基 sentence's “礎 is the kanji in 基礎.” The current sentence is not an established factual defect.

Limits:

- Exact runtime model identification was unavailable; no specific GPT version is claimed.
- Review conclusions are bounded to this packet, targeted public entries and the documented quiz behavior. I did not run the app, Kotlin/JVM tests, repository-wide tests, or an exhaustive new simulation of every larger/custom or multi-borrowed session.
- Stroke files received full structural/numeric checks and targeted geometry inspection, not rendered animation or independent regeneration from the pinned KanjiVG revision.
- The unusual source-only KANJIDIC readings were checked as claims about the pinned records, not certified as ordinary modern vocabulary. Live `kanjiapi.dev` cross-checks returned HTTP 403. Kanjipedia and the relevant live word entries independently covered the taught readings and principal secondary examples.
- Public checks did not independently repeat every incidental compound's dictionary lookup; their complete cited pinned entries were examined. Claims of a negative JMdict result remain bounded to the packet's documented families.
- Three oversized tool outputs were truncated; relevant portions were subsequently retrieved in bounded form. Their automatically suggested spool paths were not opened.
- Tool calls were serial, with one call per working response. No parallel calls, agents, background jobs, other sessions, other reviewer reports, or author-rationale files were used. No content was edited; this report is the sole requested output file.
