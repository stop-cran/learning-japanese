Snapshot: 0a20f4bf2415d6b4d20644f518990e8c938259b1, batch 109. Independent blind reviewer: GPT-6.1 Sol (model ID: gpt-6.1-sol). Reviewed the packet's declared committed snapshot, not another checkout or another reviewer's findings.

Scope:

All four facets were considered for every kanji card. Consistency/quiz safety and beginner-phone comprehensibility received the deepest examination. The 18 existing word articles were checked particularly for link-wrap-only changes, correct destinations, and readable surrounding passages.

Files actually opened, relative to `batch-109-0a20f4bf`:

- **Full:** `INSTRUCTIONS.md`, `mechanical-checks.md`, `evidence\provenance.json`, `evidence\source-metadata.json`.
- **Full, all 15 cards:** under `snapshot\kanji\`, `催.md`, `促.md`, `摩.md`, `擦.md`, `括.md`, `弧.md`, `抵.md`, `抗.md`, `撮.md`, `影.md`, `攻.md`, `撃.md`, `掲.md`, `批.md`, `択.md`.
- **Full JSON parsed, all coordinates checked:** under `snapshot\strokes\`, `催.json`, `促.json`, `摩.json`, `擦.json`, `括.json`, `弧.json`, `抵.json`, `抗.json`, `撮.json`, `影.json`, `攻.json`, `撃.json`, `掲.json`, `批.json`, `択.json`. Also inspected each stroke's type and endpoints; compared ordered IDs, types, and initial coordinates against the exact public KanjiVG revision. `掲.json` was additionally read as complete raw text.
- **Full, all 18 word articles:** under `snapshot\words\`, `催し.md`, `催促.md`, `反抗.md`, `専攻.md`, `影.md`, `影響.md`, `批判.md`, `批評.md`, `抵抗.md`, `括弧.md`, `掲示.md`, `摩擦.md`, `撮る.md`, `撮影.md`, `擦る.md`, `攻める.md`, `攻撃.md`, `選択.md`.
- **Full, all 18 diffs:** under `diffs\`, `words__催し.md.diff`, `words__催促.md.diff`, `words__反抗.md.diff`, `words__専攻.md.diff`, `words__影.md.diff`, `words__影響.md.diff`, `words__批判.md.diff`, `words__批評.md.diff`, `words__抵抗.md.diff`, `words__括弧.md.diff`, `words__掲示.md.diff`, `words__摩擦.md.diff`, `words__撮る.md.diff`, `words__撮影.md.diff`, `words__擦る.md.diff`, `words__攻める.md.diff`, `words__攻撃.md.diff`, `words__選択.md.diff`.
- **Part:** `evidence\kanjidic2-records.xml` — extracted the 15 target characters' grade, stroke counts, radical numbers, Japanese reading lists, and English meanings.
- **Part:** `evidence\jmdict-families.xml` — inspected all 72 cited entries, including complete spelling/reading alternatives, restrictions, sense lists, and register flags; did not review all 1,413 families.
- **Part:** `evidence\jmdict-digest.tsv` — lines 1–100 and up to six priority-bearing rows per target character.
- **Part, with whole-table programmatic comparisons:** `titles\kanji-titles.tsv` and `titles\word-titles.tsv` — inspected relevant rows, checked kanji-title duplicates globally, and checked scoped word titles against the complete word-title table.
- **Part:** `rubric\copilot-instructions.md`, the returned opening range through approximately line 213; `repo\docs\content-format.md`, lines 71–191 and 274–289, plus heading/field search results; `repo\docs\confusable-words.md`, lines 1–52 and a target-character search, which returned no matches.
- **Full context articles:** `repo\words\責める.md`, `repo\words\打つ.md`, `repo\words\選ぶ.md`.
- **Part, front-matter inspection only:** under `repo\kanji\`, `京.md`, `人.md`, `低.md`, `側.md`, `傾.md`, `円.md`, `写.md`, `刊.md`, `判.md`, `功.md`, `励.md`, `勧.md`, `反.md`, `宅.md`, `察.md`, `対.md`, `山.md`, `工.md`, `席.md`, `底.md`, `引.md`, `弱.md`, `強.md`, `形.md`, `悲.md`, `戦.md`, `手.md`, `打.md`, `技.md`, `投.md`, `抜.md`, `抱.md`, `掃.md`, `掘.md`, `採.md`, `接.md`, `損.md`, `放.md`, `敗.md`, `日.md`, `映.md`, `景.md`, `曲.md`, `最.md`, `束.md`, `林.md`, `殺.md`, `比.md`, `氏.md`, `活.md`, `疲.md`, `磨.md`, `示.md`, `祭.md`, `結.md`, `置.md`, `航.md`, `被.md`, `設.md`, `訳.md`, `話.md`, `責.md`, `足.md`, `車.md`, `速.md`, `選.md`, `際.md`, `集.md`, `雇.md`, `馬.md`, `駅.md`, `包.md`, `囲.md`, `像.md`, `象.md`, `光.md`, `跡.md`, `当.md`, `研.md`, `刷.md`.

Independent public verification used actual Digital Daijisen entries on Weblio for the 15 characters and the cited example/comparison words, including multi-reading entries and the cross-reference destinations 制癌剤, 特殊撮影, and 盗撮. Also inspected KanjiPedia's actual 攻 and 撃 entries and all 15 original KanjiVG SVGs at revision `70a0b7ae0c18ceb5cb358274b029cce0234a43bc`. These were independent retrievals, not the coordinator's saved public-source text.

Verdicts:

Correctness: **CLEAN** within the reviewed linguistic and structural scope.

Scoped coverage: **CLEAN**. All 36 metadata readings are represented or explicitly qualified; all 20 selected quiz readings have linked examples. Disabled kun questions and the explicitly source-only もよう.す row are not defects.

Consistency and quiz safety: **NEEDS FIX**, with consequential **UNVERIFIED** cases identified below.

Comprehensibility: **CLEAN** as an editorial assessment for the stated audience; optional simplifications follow.

Per-card verdicts:

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
| --- | --- | --- | --- | --- |
| 催 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 促 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 摩 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 擦 | CLEAN | CLEAN | CLEAN | CLEAN |
| 括 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 弧 | CLEAN | CLEAN | CLEAN | CLEAN |
| 抵 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 抗 | CLEAN | CLEAN | CLEAN | CLEAN |
| 撮 | CLEAN | CLEAN | CLEAN | CLEAN |
| 影 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 攻 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 撃 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 掲 | CLEAN | CLEAN | NEEDS FIX | CLEAN |
| 批 | CLEAN | CLEAN | UNVERIFIED | CLEAN |
| 択 | CLEAN | CLEAN | CLEAN | CLEAN |

All 18 word diffs are **CLEAN for their link-wrap-only scope**: 24 added kanji-link wrappers, no other textual changes, correct labeled destinations, and intact surrounding passages. All 257 relative-link occurrences across the scoped cards/articles resolve. Every declared word kanji has a card link where the packet contains that kanji card. Kanji titles are exactly unique across the 1,146-row title table; the 18 scoped word titles have no exact-title collisions. Metadata, grade tags, radical assignments, section order, and the structural stroke checks produced no actionable defect.

Findings:

1. **Major; consistency and quiz safety; `snapshot\kanji\影.md:13,23,45`. The curated 形 option is a valid ordinary meaning of 影.** The simulated question offers “shadow; silhouette” versus “shape; form.” JMdict entry **1590145, sense 1** explicitly gives 影 as “shadow; silhouette; figure; shape,” and [Daijisen's 影 entry](https://www.weblio.jp/content/影?edc=SGKDJ) gives both the character sense 物の姿や形 and the modern noun sense 目に見える物の姿や形. Thus “shape; form” is not defensibly wrong merely because the intended title emphasizes shadow. This affects the displayed default four-choice question, not just hypothetical fallback choices. **Remedy:** replace 形 with a verified unrelated wrong option and add the direct 影/形 exclusion so fallback cannot restore it. **Evidence:** the actual simulation, `repo\kanji\形.md:3`, the complete pinned JMdict entry, and the independently inspected dictionary entry. **Confidence: high.**

2. **Major; consistency and quiz safety; missing direct `quiz_exclusions` edges in the following scoped cards.** The declared exclusions are genuine useful pairs, but they leave additional independently supported overlaps exposed. These are pair-specific omissions, not a request to turn connected groups into transitive cliques.

   | Scoped location | Missing direct pair(s) | Why the displayed labels overlap |
   | --- | --- | --- |
   | `snapshot\kanji\催.md:13`; `促.md:14` | 催/促 | “urge; prompt” is also a modern character sense of 催, explicitly taught through 催促. Daijisen 催 sense 1 is うながす・せきたてる. |
   | `snapshot\kanji\促.md:14` | 促/責 | 責's ordinary verb 責める also means to urge or press: JMdict **1383160, sense 2**; Daijisen 責める sense 2 explicitly describes pressing for action. Thus 促's “urge; prompt” can be correct for 責. |
   | `snapshot\kanji\括.md:14` | 括/包, 括/囲 | The titles directly share “enclose”: 括 “tie together; enclose,” 包 “wrap; enclose,” 囲 “surround; enclose.” Daijisen 括 sense 2 explicitly means enclosing what is inside. |
   | `snapshot\kanji\抵.md:14` | 抵/反, 抵/対 | “oppose” in the 反 and 対 titles is also a defensible description of 抵's resisting/acting-against sense. This is independently true of each pair, not inherited through 抗. |
   | `snapshot\kanji\影.md:14` | 影/像, 影/象, 影/光, 影/跡 | The other titles offer “image,” “shape,” “light,” and “trace.” These are directly supported 影 senses in JMdict **1590145, senses 1, 2, 4, 5**, and the card itself teaches image, moonlight, and trace. |
   | `snapshot\kanji\摩.md:14` | 摩/研 | 研's “polish; study closely” includes “polish,” also a sourced 摩 sense. The live 摩する entry explicitly includes みがく; the card itself discusses 研摩. |
   | `snapshot\kanji\攻.md:14` | 攻/研 | 研's “study closely” matches 攻's expressly taught working deeply at a subject/mastering sense, supported by [KanjiPedia 攻, sense 2](https://www.kanjipedia.jp/kanji/0002184100), まなぶ・おさめる, and 専攻. |
   | `snapshot\kanji\掲.md:14` | 掲/刷 | 刷 offers “print; brush.” “Print” is an expressly taught 掲げる sense in the card's reading row and JMdict **1250600, sense 4**, not merely an inference from the physical act of putting up a sign. |

   **Impact:** these pairs remain legal together in filtered/custom pools or fallback choices, including when the existing counterpart is the target. Except for Finding 1, I am not claiming they appear in the printed default four-choice simulations: those normally consume the curated meaning options first. **Remedy:** add each supported direct exclusion on one endpoint, preserving existing exclusions and non-overlapping distractors. Do not blanket-exclude all members of any larger semantic group.

   **Evidence:** the exact titles in `titles\kanji-titles.tsv`; front matter on both endpoints, neither of which declares these pairs; `repo\docs\content-format.md:94–116`; the cited complete JMdict entries; independently inspected [催](https://www.weblio.jp/content/催?edc=SGKDJ), [責める](https://www.weblio.jp/content/責める?edc=SGKDJ), [括](https://www.weblio.jp/content/括?edc=SGKDJ), [抵](https://www.weblio.jp/content/抵?edc=SGKDJ), [影](https://www.weblio.jp/content/影?edc=SGKDJ), [摩する](https://www.weblio.jp/content/摩する?edc=SGKDJ), and [掲げる](https://www.weblio.jp/content/掲げる?edc=SGKDJ) dictionary entries. **Confidence: high for the explicit shared glosses and modern prompting/enclosing/image senses; medium-high for the broader secondary-sense pair judgments.**

Optional:

- For phone reading, shorten synonym strings such as 抵当's “mortgage; security; hypothec; pledge,” explain “geminate consonant” as a doubled consonant, and gloss “Go-on” if retained. The main ideas already come first; these are polish, not comprehension blockers.
- Label 擦過傷 “formal” to carry JMdict **1298950**'s formal/literary flag into the learner-facing comparison with 擦り傷.
- In 掲's mnemonic, “a simplified variant of 曷, shaped as 日 over 匂” would be more precise than naming unqualified 曷. KanjiVG explicitly marks this component as a variant, so I did not classify the conventional component label as an established factual defect.

Limits:

- **Consequential unresolved quiz case: 撃/敗.** `snapshot\kanji\撃.md:13` curates 敗, displayed as “failure; defeat.” The pinned KANJIDIC2 meanings for 撃 include “defeat,” making that option suspect. However, the independently inspected [Daijisen 撃](https://www.weblio.jp/content/撃?edc=SGKDJ) and [KanjiPedia 撃](https://www.kanjipedia.jp/kanji/0001844000) describe hitting, shooting, attacking, and contact, without establishing successful defeat as an ordinary separate sense. I could not resolve the status of the English “defeat” gloss sufficiently to certify this option as defensibly wrong or report it as an established modern-Japanese synonym defect. Hence **UNVERIFIED**, not CLEAN. Replacing this foil would avoid depending on that unresolved gloss.
- **Consequential unresolved quiz case: 攻/批.** The pinned 攻 meanings include “criticize”; 批's displayed title is “criticize; critique,” and no direct edge excludes them. Modern dictionary evidence clearly supports verbal criticism for 攻撃, but the inspected character entries chiefly organize 攻 under attack and study. I did not establish the ordinary per-character scope of the English “criticize” gloss confidently enough to adjudicate this additional pair. 批's consistency verdict is therefore **UNVERIFIED**; 攻 already needs the independent 攻/研 fix.
- Stroke review covered full JSON structure and coordinates, source identity, counts, ordered types, initial coordinates, and component geometry. I did not independently regenerate every arc-length sample or run/render the app's animated stroke exercises.
- Sentence grammar, kana, translation, contrast, and naturalness were reviewed editorially and against the inspected dictionary constructions. No native-speaker panel or physical-phone usability trial was performed.
- The pinned dictionaries are the authority for preserved metadata; today's public entries sometimes include additional readings. Such differences were not silently treated as metadata errors. The source-only もよう.す row is explicitly qualified, not independently established as a productive modern reading.
- This was a bounded packet review, not exhaustive semantic verification of the entire corpus or every randomized quiz seed. Context articles were not expanded into new review scope. Supplied automatic test results were read, not rerun. Snapshot identity relies on the packet declaration; I did not open another checkout, original compressed input, author's rationale, or another review.
