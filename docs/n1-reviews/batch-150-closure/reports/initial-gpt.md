Snapshot: 2dd9d46bca2aa4cc2b439d08c2ef36e6d9067a41, batch 150. Reviewer: OpenAI ChatGPT, GPT family; the exact serving model identifier is not exposed to me. Packet-manifest SHA-256 independently matched 2b49b3f4f4c31756d984e28dfaf6e69fdfb6a1670764201e7b21f614fb7354f3.

Scope:

All paths below are relative to the assigned packet. “Full, computational” means the complete file was parsed and its relevant data checked, not that every byte was reproduced in a tool response. Facets 3 and 4 received the deepest examination.

- **Full:** `INSTRUCTIONS.md`; `mechanical-checks.md`.
- **Full, all 15 cards:** `snapshot\kanji\葬.md`, `蒔.md`, `蓄.md`, `薦.md`, `虚.md`, `融.md`, `衆.md`, `街.md`, `衝.md`, `裁.md`, `裂.md`, `裸.md`, `覆.md`, `視.md`, `覧.md`.
- **Full, computational, all 15 stroke files:** `snapshot\strokes\葬.json`, `蒔.json`, `蓄.json`, `薦.json`, `虚.json`, `融.json`, `衆.json`, `街.json`, `衝.json`, `裁.json`, `裂.json`, `裸.json`, `覆.json`, `視.json`, `覧.json`.
- **Full, all 18 word articles:** `snapshot\words\公衆.md`, `展覧会.md`, `御覧.md`, `推薦.md`, `無視.md`, `葬式.md`, `蒔く.md`, `蓄える.md`, `街角.md`, `衝突.md`, `裁判.md`, `裁縫.md`, `裂く.md`, `裸.md`, `覆う.md`, `謙虚.md`, `重視.md`, `金融.md`.
- **Full, all 18 diffs:** `diffs\words__公衆.md.diff`, `words__展覧会.md.diff`, `words__御覧.md.diff`, `words__推薦.md.diff`, `words__無視.md.diff`, `words__葬式.md.diff`, `words__蒔く.md.diff`, `words__蓄える.md.diff`, `words__街角.md.diff`, `words__衝突.md.diff`, `words__裁判.md.diff`, `words__裁縫.md.diff`, `words__裂く.md.diff`, `words__裸.md.diff`, `words__覆う.md.diff`, `words__謙虚.md.diff`, `words__重視.md.diff`, `words__金融.md.diff`.
- **Full:** `evidence\provenance.json`, `evidence\joyo-pages.md`, `evidence\kanjipedia-outside-readings.json`, `evidence\daijisen-heads.txt`, `evidence\okurigana-scan.txt`, `evidence\kanjivg-components.txt`.
- **Full, computational:** `evidence\source-metadata.json`; `evidence\kanjivg-svgs.txt` (all 16 SVG documents parsed; all 15 scoped characters' paths independently resampled).
- **Part:** `evidence\kanjidic2-records.xml` (parsed completely; inspected and compared the 15 target records); `evidence\jmdict-families.xml` (parsed completely to retrieve complete entries cited by the cards, including spelling/reading restrictions, usage information and senses); `evidence\jmdict-digest.tsv` (header and the first six priority-ordered family rows for each target).
- **Full:** `evidence\public-source\weblio-葬.txt`, `weblio-蒔.txt`, `weblio-蓄.txt`, `weblio-薦.txt`, `weblio-虚.txt`, `weblio-融.txt`, `weblio-衆.txt`, `weblio-街.txt`, `weblio-衝.txt`, `weblio-裁.txt`, `weblio-裂.txt`, `weblio-裸.txt`, `weblio-覆.txt`, `weblio-視.txt`, `weblio-覧.txt`.
- **Full:** `evidence\audits\quiz-safety.txt`, `reading-exposure.txt`, `reading-options.txt`, `kanji_remarks.py`, `kanji-remarks.json`, `word-remarks.json`. **Part:** `evidence\audits\extra-readings.json`, lines 1–150.
- **Full:** `evidence\app-code\QuizBuilder.kt`, `KanjiMeaningMetadata.kt`, `KanjiReadings.kt`. **Part:** `evidence\app-code\Words.kt`, the reading-option documentation, mutation implementation and nearby candidate-building lines around 210–258.
- **Part:** `rubric\copilot-instructions.md`, opening review instructions (lines 1–100 explicitly inspected; an earlier bounded read requested through 180); `repo\docs\content-format.md`, opening bounded read, kanji contract lines 86–154, stroke contract lines 289–304, and matched heading/link rules; `repo\docs\confusable-words.md`, opening rules and matched passages about direct, non-transitive relationships.
- **Part:** `titles\kanji-titles.tsv` and `titles\word-titles.tsv` (both parsed in full; inspected target rows, all declared exclusion titles, relevant semantic-neighbor rows, and the 18 scoped word rows). **Part:** `packet-manifest.json`, bytes read only to verify its hash.
- **Full context cards:** `repo\kanji\苗.md`, `捜.md`, `仰.md`, `殻.md`, `布.md`, `戦.md`. **Part:** `repo\kanji\監.md`, lines 1–65 of 176; `repo\kanji\冶.md`, lines 1–65 of 67.
- **Part, front matter only:** `repo\kanji\土.md`, `花.md`, `寺.md`, `咲.md`, `枯.md`, `掘.md`, `使.md`, `売.md`, `借.md`, `話.md`, `書.md`, `教.md`, `満.md`, `真.md`, `重.md`, `水.md`, `雪.md`, `氷.md`, `王.md`, `客.md`, `父.md`, `橋.md`, `庭.md`, `池.md`, `走.md`, `止.md`, `回.md`, `糸.md`, `針.md`, `法.md`, `縫.md`, `編.md`, `畳.md`, `靴.md`, `帯.md`, `傘.md`, `開.md`, `拾.md`, `投.md`, `聞.md`, `言.md`, `音.md`, `歌.md`, `絵.md`, `参.md`, `舞.md`, `巻.md`, `復.md`, `味.md`, `未.md`, `美.md`, `魅.md`.

Independent public verification used the actual Kanjipedia entries linked by all 15 cards and live Digital Daijisen character entries on Weblio. 蒔's Weblio page supplied no character entry, consistently with the card. I also inspected actual Jisho API dictionary results, including senses and restrictions, for:

葬る, 葬式, 蒔く, 蒔絵, 蓄える, 蓄積, 薦, 推薦, 虚しい, 虚空, 虚ろ, 謙虚, 虚無僧, 融かす, 融ける, 金融, 融和, 衆, 衆生, 公衆, 群衆, 街, 街角, 街頭, 街道, 巷, 衝突, 衝く, 要衝, 裁判, 裁縫, 裁つ, 断つ, 裁く, 体裁, 裂く, 裂ける, 古代裂れ, 切れ, 裸, 裸体, 裸足, 覆面, 覆う, 覆す, 覆る, 視る, 覧る, 無視, 重視, 展覧会, 御覧, 閲覧, 視する, 覆いかぶさる, 裂ぱく, 苗 and 捜す. The 覧る lookup did not expose a matching ordinary spelling; its search-only status was verified in the pinned full JMdict entry. Additional live Daijisen checks covered 苗, 捜, 布, 素, 教, 法, 氷 and 寺.

Verdicts:

- **Correctness: NEEDS FIX** — localized comparison claims in 蒔, 視 and 覧; otherwise CLEAN within the checks described.
- **Scoped coverage: CLEAN** — all 15 cards.
- **Consistency and quiz safety: NEEDS FIX** — unsupported exclusion edges on 蒔, 裁, 視 and 覧. No ambiguous answer was established in the current three-curated-distractor questions.
- **Comprehensibility: CLEAN** — all 15 cards; optional shortening below.

| Card | Correctness | Scoped coverage | Consistency / quiz safety | Comprehensibility |
|---|---|---|---|---|
| 葬 | CLEAN | CLEAN | CLEAN | CLEAN |
| 蒔 | NEEDS FIX, G1 | CLEAN | NEEDS FIX, G1 | CLEAN |
| 蓄 | CLEAN | CLEAN | CLEAN | CLEAN |
| 薦 | CLEAN | CLEAN | CLEAN | CLEAN |
| 虚 | CLEAN | CLEAN | CLEAN | CLEAN |
| 融 | CLEAN | CLEAN | CLEAN | CLEAN |
| 衆 | CLEAN | CLEAN | CLEAN | CLEAN |
| 街 | CLEAN | CLEAN | CLEAN | CLEAN |
| 衝 | CLEAN | CLEAN | CLEAN | CLEAN |
| 裁 | CLEAN | CLEAN | NEEDS FIX, G1 | CLEAN |
| 裂 | CLEAN | CLEAN | CLEAN | CLEAN |
| 裸 | CLEAN | CLEAN | CLEAN | CLEAN |
| 覆 | CLEAN | CLEAN | CLEAN | CLEAN |
| 視 | NEEDS FIX, G2 | CLEAN | NEEDS FIX, G2 | CLEAN |
| 覧 | NEEDS FIX, G2 | CLEAN | NEEDS FIX, G2 | CLEAN |

All 15 stroke files and all 18 scoped word changes are CLEAN.

Verification supporting these verdicts:

- Front-matter stroke counts, radicals/numbers, grades and complete on/kun lists match the pinned metadata and target KANJIDIC2 records. Quiz selections are exact subsets with the required linked examples. Titles are unique in the supplied index; checked links resolve and quoted linked card titles match, allowing normal quotation punctuation.
- Every mnemonic is explicitly modern-shape, disclaims etymology and matches the pinned component layout. This includes 薦's ungrouped middle strokes, 衆's nested 血/皿, the split 行 and 𢦏 frames, 覧's 臣/𠂉, and the grass crowns. Independent cubic-curve resampling matched every stroke file's 16-point arrays within 0.071 units in the 109-unit view box, consistent with one-decimal rounding. Counts, types, order, finite coordinates, source revision and character identity also match.
- Joyo claims match the supplied official-page extracts. The source-only/outside-table qualifications are supportable. In particular, 薦's こも is an attested ordinary noun reading despite KANJIDIC2 putting it under names; 視る is an ordinary listed spelling whereas 覧る is search-only in the pinned JMdict; 裸足 is correctly treated as a whole-word reading. The claims about 薦's mat sense, 虚's falsehood, 融's circulation, 衝's thrusting, 視's regard-as sense, 覆's repetition and 裂's cloth reading are sourced, not invented.
- The priority-family spot checks did not establish an important omission requiring expansion. The new kanji cards contain no invented Japanese example sentences. The existing word passages remain natural after their link wraps.
- All 18 diffs independently reduce to exactly one unchanged line with the intended character wrapped in its intended card link. No Dictionary line changes. Every declared kanji with an existing card is linked in the resulting word articles.
- I judged every declared exclusion against both displayed titles, rather than taking transitive closure. G1 and G2 identify the established excesses. Other specifically raised edges have meaningful direct support: for example 葬/悔 through mourning, 薦/献 and 薦/供 through KANJIDIC2's “offer,” 衝/推 through pushing/thrusting, 裂/爆 through bursting, 裂/砕 through breaking apart, 覆/復 through repetition, and 衆/組 through the attested group/bunch sense. 街/丁 has direct “block” evidence. The two covering/emptiness edges involving 殻 are conservative comparisons supported by its displayed covering/empty-shell senses; they do not imply that 虚 and 覆 are synonyms.
- Within-batch 視/覧 and 裁/裂 are correctly excluded once. 蓄/衆, 葬/蒔, 覆/裸 and 虚/裸 remain distinguishable in either direction: accumulating resources is not a multitude of people; burial is not sowing; covering is not bareness; emptiness/falsehood is not nakedness.

All 45 curated meaning distractors are plausible within their semantic fields but defensibly wrong in either direction:

| Target | Checked distractors | Selected reading |
|---|---|---|
| 葬 | 土・花・寺 | ソウ |
| 蒔 | 咲・枯・掘 | ま.く |
| 蓄 | 使・売・借 | たくわ.える |
| 薦 | 話・書・教 | セン |
| 虚 | 満・真・重 | キョ |
| 融 | 水・雪・氷 | ユウ |
| 衆 | 王・客・父 | シュウ |
| 街 | 橋・庭・池 | まち |
| 衝 | 走・止・回 | ショウ |
| 裁 | 糸・針・法 | サイ |
| 裂 | 縫・編・畳 | さ.く |
| 裸 | 靴・帯・傘 | はだか |
| 覆 | 開・拾・投 | おお.う |
| 視 | 聞・言・音 | シ |
| 覧 | 書・歌・絵 | ラン |

In particular, 法 supplies laws/methods, not judging; 氷 freezes rather than melts; 寺 names a temple, not a funeral; and 教's instruction/teaching is not 薦's recommendation. Association does not make these correct alternatives.

The complete reading audits, actual option-card headers and app builder agree on curated-first selection and protection of complete metadata readings. The four logged latent target/key collisions are 蒔/まい, 蒔/まき, 街/また and 視/み; all four are name-only **for the target character** in the pinned KANJIDIC2 records. The logs distinguish these from zero ordinary-reading production/padded hits. 街's また can become drawable when 復 is additionally borrowed, and the final one-holder summary explicitly reports that name-only case. Therefore the accounting does not warrant an unconditional “no attested reading can ever be drawn” claim.

The okurigana extras were included in the logged inputs. Expressions such as 虚をつく and 視する, and the partially kana-written 裂ぱく, should not be reinterpreted as new standalone kun readings merely because the scan represented them with dots. I found no demonstrated ordinary-reading wrong option in the supplied simulations.

Findings:

**G1 — minor; consistency and quiz safety; also correctness for 蒔.**

**Files:** `snapshot\kanji\蒔.md:14,50`; `snapshot\kanji\裁.md:14,51`.

**Claim and impact:** These two exclusion justifications confuse an action with its material or object. 蒔 says a “seedling” overlaps “seeds,” and a “young plant” overlaps “to plant.” A seedling is already a young plant, not a seed, and neither noun names sowing. 裁 excludes 布 merely because “cloth” occurs inside “cut out cloth.” Cloth does not mean cutting cloth, tailoring or judging. These are useful, distinguishable study contrasts in both directions, not established answer collisions. The 蒔 explanation additionally teaches an incorrect seed/seedling equivalence. The current default questions remain safe; the defect is unnecessary symmetric suppression and the accompanying explanation.

**Remedy:** Remove 苗 from 蒔's exclusions and 布 from 裁's exclusions. Delete or replace those justifications with accurate contrasts, without removing 蒔's separately sourced replanting sense.

**Evidence:** The displayed titles are “sow seeds” / “seedling; young plant” and “judge; cut out cloth” / “cloth; distribute.” JMdict 2611890 describes sowing/planting; 1296050 describes cutting cloth. The actual [苗 dictionary result](https://jisho.org/api/v1/search/words?keyword=苗) gives “seedling; young plant,” not sowing. [Daijisen 布](https://www.weblio.jp/content/布) distinguishes fabric, spreading and distribution; [Kanjipedia 裁](https://www.kanjipedia.jp/kanji/0002527700) describes cutting fabric and judging. None supplies the proposed action/object equivalence. The content-format contract requires direct evidence about actual labels and ordinary meanings.

**Confidence:** High for the semantic distinctions and the inaccurate seed/seedling explanation; medium-high for removing these conservative exclusion edges.

**G2 — minor; correctness; consistency and quiz safety.**

**Files:** `snapshot\kanji\視.md:14,49`; `snapshot\kanji\覧.md:14,50`.

**Claim and impact:** Both cards assert that 捜's “look for” overlaps their “look at” or “look over.” These are different English constructions and different actions. 捜 searches for something; 視 sees/regards something; 覧 surveys/peruses something. Sharing the word “look” does not establish a direct synonym edge. Neither card offers evidence that its character means searching for a missing object. The explanations blur a useful beginner distinction while symmetrically excluding a legitimate contrast.

**Remedy:** Remove 捜 from both exclusion lists and remove the asserted overlap. An optional contrast could say “look for” is searching, not merely looking at or looking over something. This finding does not ask to remove the independently defensible looking/observing/inspection exclusions.

**Evidence:** Actual [捜す dictionary result](https://jisho.org/api/v1/search/words?keyword=捜す): search for, look for, hunt for, seek; search through/rummage. [Daijisen 捜](https://www.weblio.jp/content/捜) defines searching thoroughly, すみずみまでさがし求める. JMdict 1259290 and the live [視る result](https://jisho.org/api/v1/search/words?keyword=視る) cover seeing, observing, examination and care, not searching for. [Kanjipedia 覧](https://www.kanjipedia.jp/kanji/0007055400) gives looking closely/widely. The supplied 捜 context card likewise explicitly distinguishes searching from finding.

**Confidence:** High.

Optional:

- Shorten repeated dictionary/process qualifications and the identical multi-sentence mnemonic disclaimers. The concrete images and central meanings are clear, but repeating “not selected for questions here” in almost every row and documenting every exclusion inline adds scrolling on a phone. Preserve the facts and honest mnemonic label.
- Briefly explain “Joyo” as the official standard-use kanji table, and explain “transitive” locally where used, rather than relying solely on linked word articles.
- A compact 虚偽 example could connect 虚's title word “false” to a common compound, but its absence is not a scoped-coverage defect.

Limits:

- Exact serving model/version identification was unavailable; I have not invented one.
- This was independent and blind. No other review, author rationale, repository checkout or unrelated local path was opened. No agent, session, parallel call, background job, recursive listing or repository-wide content scan was used. Each execution response contained one tool call.
- The packet is an export, not a Git history checkout. I independently checked every supplied word diff; the claim that no existing kanji card changed relies on the supplied mechanical result and inspected checker, not a new base-to-head Git comparison.
- I inspected the complete supplied simulations and relevant app code, but did not rebuild the full 1,502-card pool or independently rerun the global reachability audit. Its Python runner was not present in the audit directory. Seeded simulations are not proof for every hypothetical/custom pool.
- KANJIDIC2 name-only classifications were checked against the pinned records, not an independent name dictionary. Those readings are not selected questions. No ordinary-reading collision remains established by the reviewed evidence.
- The official Joyo PDF itself was not independently downloaded; its claims were checked against the supplied full cited-page extracts and front matter.
- KanjiAPI requests returned HTTP 403. I used actual Weblio/Kanjipedia entries and Jisho API results instead. A Jisho HTML request yielded navigation rather than an entry; it was not treated as dictionary verification.
- No Android/Kotlin/device execution or physical-phone rendering was performed or claimed. The packet's known JVM/Kotlin omissions and existing four lint warnings are not findings. No source file was changed; only this report was written.
