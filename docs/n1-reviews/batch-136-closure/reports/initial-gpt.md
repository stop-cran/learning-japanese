Snapshot: `420a6669a2f1dafcc3a237e8b8604ff8cbc4201e` — batch 136. Reviewer: GPT (OpenAI; exact runtime model identifier unavailable). Independently computed `packet-manifest.json` SHA-256: `440ba2029aafbef24a1be4e90195bb8c673691fec29b8df228a0e963b6b7df58`, matching the assignment.

Scope:

All paths below are relative to the assigned packet. Brace lists name every individual file opened; they do not represent wildcard sampling. Facets 3 (consistency and quiz safety) and 4 (beginner/phone comprehensibility) received the deepest examination.

**Complete text reads**

- `INSTRUCTIONS.md`; `mechanical-checks.md`; `rubric\copilot-instructions.md`.
- All 15 cards: `snapshot\kanji\{炊,焦,異,端,筋,粗,納,脱,膨,致,請,透,鉢,隔,駄}.md`.
- All 34 word articles: `snapshot\words\{一致,下駄,先端,炊く,炊事,無駄,焦がす,焦げる,焦点,申請,異なる,異常,端,筋,筋肉,粗,粗い,粗末,納める,納得,脱ぐ,脱線,膨らます,膨らむ,膨大,致す,請う,請求,透き通る,透明,途端,鉢,間隔,隔てる}.md`.
- All 34 diffs: `diffs\words__{一致,下駄,先端,炊く,炊事,無駄,焦がす,焦げる,焦点,申請,異なる,異常,端,筋,筋肉,粗,粗い,粗末,納める,納得,脱ぐ,脱線,膨らます,膨らむ,膨大,致す,請う,請求,透き通る,透明,途端,鉢,間隔,隔てる}.md.diff`.
- `evidence\audits\quiz-safety.txt`; `evidence\audits\reading-options.txt`; `evidence\audits\reading-exposure.txt`, including their beginnings and conclusions, not just the mechanically retained tails.
- `evidence\joyo-pages.md`, including the front matter and appendix.
- `evidence\public-source\weblio-{炊,焦,異,端,筋,粗,納,脱,膨,致,請,透,鉢,隔,駄}.txt`.
- `evidence\provenance.json`; `evidence\kanjipedia-outside-readings.json`; `evidence\daijisen-heads.txt`; `evidence\okurigana-scan.txt`.
- `evidence\app-code\QuizBuilder.kt`; `evidence\app-code\KanjiMeaningMetadata.kt`.
- `repo\kanji\静.md`.

**Complete machine reads/parses, with inspected projections**

- All 15 stroke files: `snapshot\strokes\{炊,焦,異,端,筋,粗,納,脱,膨,致,請,透,鉢,隔,駄}.json`. All fields and coordinates were parsed; counts, identities, IDs, types, finite/in-bounds coordinates and endpoints were checked. `請.json` was also read as raw text. Each file was independently compared with its public KanjiVG SVG at revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`: stroke counts, order, types, endpoints and sampled-path geometry agreed. Maximum nearest-path discrepancy was about 0.071 units in the 109-unit view box, consistent with rounded coordinates.
- `evidence\source-metadata.json`: complete parse and comparison of all 15 cards; raw lines 1–240 also read.
- `evidence\kanjidic2-records.xml`: complete XML parse; the 15 target characters' metadata, readings and name readings inspected.
- `evidence\jmdict-families.xml`: complete XML parse; cited-family forms, readings, glosses and usage/spelling restrictions inspected through projections. Full raw target entries additionally displayed: 1596830, 1738100, 1656580, 2863007, 1530510, 1592920, 1589090, 1581610, 2841301 and 1586730. The whole 2,462-family context was not manually read.
- `evidence\jmdict-digest.tsv`: complete parse for target-family/priority comparisons; header, initial rows and bounded per-character priority projections read.
- `titles\kanji-titles.tsv`; `titles\word-titles.tsv`: complete parse for title uniqueness, referenced labels, readings and comparisons; selected projections read.
- `packet-manifest.json`: complete bytes read for the independent hash check, not a manual review of every manifest entry.

**Partial text reads**

- `repo\docs\content-format.md`: lines 71–139 and 274–289, plus targeted heading/keyword matches.
- `repo\docs\confusable-words.md`: lines 1–105.
- `evidence\app-code\KanjiReadings.kt`: lines 1–137 and targeted function-location matches.
- `evidence\app-code\Words.kt`: lines 205–310 and targeted location matches.

**Independent public verification**

Actual live Digital Daijisen entries on Weblio were inspected for all 15 characters, their consequential extra readings, and important example words. These included the regional sense of 炊く; 焦れる/焦らす/焦がれる; 異にする; 端 and 道端; 粗い/粗削り; 納得/納屋/納戸/出納/納まる/御用納め; 脱ぐ/脱げる; 膨らむ/膨らます/膨れる; 致す/おこす/おくす; 請う/請ける/普請/起請; 透く/透かす/透ける/透る/透す; 托鉢; 隔てる/隔たる; and 下駄/無駄/駄目/雪駄. Live Kanjipedia character entries were independently inspected for 14 characters; 膨 returned HTTP 500 twice. Live Jisho dictionary data independently corroborated rare 脱る とる, 炊ぐ かしぐ, 焦れる じれる, 焦らす じらす and the two senses of 追い炊き. These were entry inspections, not search-snippet verification.

Verdicts:

- **Correctness: NEEDS FIX** — G1 and G3 in new cards; G2 in newly affected word context.
- **Scoped coverage: NEEDS FIX** — G3 misdescribes the scope of a taught verb sense. No missing metadata-reading row or unjustified demand for additional vocabulary was established.
- **Consistency and quiz safety: NEEDS FIX** — G2 is a collection-consistency contradiction. No actionable ambiguity was established in the reviewed meaning options or reachable reading options.
- **Comprehensibility: CLEAN** — the central ideas, kana, contrasts and explicitly modern-shape mnemonics are understandable; shortening is optional below.

Per-card verdicts:

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 炊 | NEEDS FIX: G3 | NEEDS FIX: G3 | CLEAN | CLEAN |
| 焦 | CLEAN | CLEAN | CLEAN | CLEAN |
| 異 | CLEAN | CLEAN | CLEAN | CLEAN |
| 端 | CLEAN | CLEAN | CLEAN | CLEAN |
| 筋 | CLEAN | CLEAN | CLEAN | CLEAN |
| 粗 | CLEAN | CLEAN | CLEAN | CLEAN |
| 納 | CLEAN | CLEAN | CLEAN | CLEAN |
| 脱 | CLEAN | CLEAN | CLEAN | CLEAN |
| 膨 | CLEAN | CLEAN | CLEAN | CLEAN |
| 致 | CLEAN | CLEAN | CLEAN | CLEAN |
| 請 | NEEDS FIX: G1 | CLEAN | CLEAN | CLEAN |
| 透 | CLEAN | CLEAN | CLEAN | CLEAN |
| 鉢 | CLEAN | CLEAN | CLEAN | CLEAN |
| 隔 | CLEAN | CLEAN | CLEAN | CLEAN |
| 駄 | CLEAN | CLEAN | CLEAN | CLEAN |

For `snapshot\words\透明.md`, correctness and consistency are **NEEDS FIX: G2**; its coverage and comprehensibility are CLEAN. No actionable defect was established in the other 33 modified word articles. All 15 stroke files are CLEAN within the structural/source-geometry checks described above.

**Specific quiz and coverage conclusions**

- All 15 front-matter reading lists, grade/stroke/radical metadata and quiz selections matched the pinned evidence. Selected readings have appropriate linked examples; titles are unique; checked card links resolve. The official-table reading/example claims matched the supplied extracts, including distinctions between official rows, unlisted readings and appendix material.
- All 34 diffs change exactly one line, add exactly one link to the intended new kanji card, and preserve the visible passage text. None changes a Dictionary line. G2 concerns surrounding text made false by this batch, not a hidden substantive diff.
- The complete meaning simulation was assessed using the displayed labels and ordinary secondary senses, in both directions. 脱's 飲/読/聞 and 致's 話/買/学 are not visual look-alikes, but are defensibly wrong basic-verb contrasts; the cards do not pretend otherwise.
- I considered the weaker exclusion pairs directly, rather than demanding identical central glosses or accepting transitive cliques. The difference/change senses for 異–差/変, edge/tip senses for 端–刃/梢, line/order/reason senses for 筋–系/統/理, undertake/ask senses for 請–企/就/問, and the relevant secondary senses behind 致–因/及, 膨–太, 駄–履/劣, 隔–挟 and 透–明 provide defensible direct confusion/overlap grounds. No actionable pair error was established.
- 納得 genuinely exemplifies ナッ, not ノウ. The card preserves and illustrates ノウ/ナ/ナン/トウ and explicitly explains the linked-example limitation. 駄's タ is correctly illustrated by 下駄; its treatment of 無駄 as ateji, separate ダ example 駄目 and empty pinned kun list is defensible.
- Rare/source-only rows are not silently promoted into everyday quiz material. This includes 異 け, 透 とう.る/とう.す, 請 シン/ショウ, 粗 あら-, 炊 -だ.き, 納 -おさ.める and 焦 じ.れる/じ.らす/こ.がれる. 脱 とる is independently attested as rare; 致 おこす/おくす are old forms, not fabricated modern verbs.
- 炊's shared スイ with 吹 and 鉢's shared ハチ/ハツ with 八 are protected by the reading exclusion logic. 炊's name-only い is not thereby an alternative correct on/kun answer.
- The two `HIT` labels, はじめ for 端 and おこす for 致, are not demonstrated production defects: their relevant kun prompts always fill all three wrong slots from safe curated candidates in the audited pools, so those fallback readings are unreachable. Other prompts do use fallback; I did not assume curated saturation globally.
- The exposure audit distinguishes 17 latent collisions from drawable answers and reports zero production, padded-session or non-name one-holder padded hits. Its extra name-only case does not establish an on/kun collision. These conclusions are bounded to the studied pools, not a universal guarantee for hypothetical smaller decks.

Findings:

### G1 — Minor; correctness; incorrect component placement

- **Location:** `snapshot\kanji\請.md:54`.
- **Claim:** 清, 晴 and 静 “all have 青 at the right as 請 does.”
- **Defect and impact:** 静 has 青 on the **left**, with 争 on the right. The sentence teaches an incorrect visual comparison in a section intended to distinguish similar characters.
- **Remedy:** Say that 清 and 晴 share right-hand 青 with 請, while 静 places 青 on the left. The shared セイ observation need not be removed.
- **Evidence:** The glyph 静 itself; `repo\kanji\静.md:24–25,45`, which explicitly and correctly identifies the left/right components.
- **Confidence:** High.

### G2 — Minor; correctness and consistency; stale claim that the new card does not exist

- **Location:** `snapshot\words\透明.md:30–32`, particularly line 32.
- **Claim:** “There is no separate 透 card in this collection.”
- **Defect and impact:** This batch adds `snapshot\kanji\透.md` and turns 透 into a link two lines above that sentence. Following the newly added link directly contradicts the article's collection guidance.
- **Remedy:** Remove or update the stale sentence. This is a necessary surrounding-context correction; record it explicitly as an exception to the otherwise link-wrap-only word edits.
- **Evidence:** The new 透 card; the added link in `diffs\words__透明.md.diff`; the complete resulting word article.
- **Confidence:** High.

### G3 — Minor; correctness and scoped coverage; regional verb sense loses its qualification

- **Location:** `snapshot\kanji\炊.md:23`, reinforced at line 50.
- **Claim:** 炊く is presented with a second sense “to boil; to simmer; to stew; to seethe,” without its regional restriction.
- **Defect and impact:** The cited JMdict entry labels precisely this sense **Kansai-ben**. Omitting that restriction from the main explanation invites a beginner to generalize 炊く into an unrestricted standard verb for boiling or simmering. The linked word article correctly warns against that generalization, so the two teaching surfaces disagree.
- **Remedy:** Identify the broader verb sense as Kansai/regional where it is introduced, and retain the qualification when invoking “seethe” in Notes. Distinguish that restricted verb use from the character's broader dictionary meaning; the kanji gloss “boil” need not simply be deleted.
- **Evidence:** `evidence\jmdict-families.xml`, entry 1596830, second sense: `<dial>Kansai-ben</dial>` with those four glosses. Independent [Digital Daijisen, 炊く](https://www.weblio.jp/content/炊く), sense 2: “（西日本で）煮る。” `snapshot\words\炊く.md:45–48` already preserves the Kansai restriction.
- **Confidence:** High.

Optional:

- Move some source inventories and repeated “no word article yet / not selected” explanations into a compact reference block, while keeping every reading and consequential restriction visible. The current cards generally lead with a clear meaning and use short paragraphs, but the accumulated dictionary examples and exclusion justifications make them lengthy phone reads. This is nonblocking polish, not a finding that the source detail is wrong.

Limits:

- This was a blind, independent review. No other review, author rationale, other packet or repository checkout was consulted. No agents, other sessions, background jobs, parallel calls, recursive listings or whole-corpus filesystem scans were used.
- All intentional local access stayed within the packet and the authorized report path. Oversized tool results were sometimes truncated; their automatically generated capture files outside the packet were not opened. Necessary evidence was obtained through bounded rereads/projections.
- Public checks covered the characters' consequential reading claims and important examples, not every sense of every surrounding dictionary family. Pinned dictionary data, rather than present-day public coverage alone, controls snapshot comparisons. Kanjipedia's live 膨 page remained unavailable; its packet extract, the pinned metadata and independent Daijisen evidence were available.
- Stroke checks independently verified the pinned source geometry/order, not physical-phone animation, handwriting recognition or every pedagogically accepted stroke-order variant.
- Quiz conclusions apply to the supplied app logic and audited shipped-stack/session pools. Arbitrary future content, hypothetical tiny pools and different clients were not certified. Android JVM tests and the Kotlin audit cross-check were not run in this review; their absence was already an acknowledged packet limit, not a new finding.
- CLEAN means no actionable defect established within the stated review, not exhaustive linguistic or native-speaker certification. The exact GPT runtime version was not exposed.
