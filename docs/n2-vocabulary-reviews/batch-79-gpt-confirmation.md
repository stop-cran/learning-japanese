## Snapshot

**Confirmed: no remaining actionable defect was established in the reviewed corrected content.**

Revised commit: **`fea8bc2e4234557b3ed0ccca4bb7f5af263c1985`**

Parent/authored snapshot: **`193c2cd87a3d78c1b2ea4e3fb680216cbdfaef46`**

This report concerns the supplied **committed-content-only snapshot**. I read the correction snapshot first. File-only tools cannot execute Git, so commit association, clean-worktree status, hashes and author-executed preservation checks were **not independently executed reviewer checks**.

## Scope

Actual model: **GPT-6.1 Sol**, model ID **`gpt-6.1-sol`**, family **gpt**, continuing the original native review session. **No edits, shell, agents or delegation. Fresh file reads were serial.**

Fresh complete reads covered:
- Both required instruction files; `docs\content-format.md:18–103`; the complete correction patch, original related-content patch and reconciliation.
- All **18 assigned current word articles**, all **3 related kanji bodies**, and all **12 required older comparison articles**, including unchanged articles.
- All **20 mappings**, **18 complete principal families/50 senses**, **22 component records** and **203 navigation labels**, including restrictions, flags and inherited POS.
- The TSV header and **exactly physical rows 1562–1581**, checking all twenty associations and raw fields.
- The complete correction comparison rendering (**25 families/66 senses**), supplement (**3/12**), extra comparison rendering (**4/17**) and public-bodies file through EOF. The overlapping fresh dictionary sets comprise **42 distinct families/123 senses**, excluding public captures.

The original review’s **313 families/816 senses** and **159 complete existing bodies, including reused 巻く**, remain inherited evidence, not fresh rereads of that entire union. The initial 399 prepared families were not all inspected. Current component-target existence was rechecked within `kanji\`; the nine other component bodies retain their inherited inspection status. No mandatory fresh read was omitted, and no prohibited ledger or other reviewer’s report was opened.

## Verdicts

**CLEAN** means no actionable defect established within this evidence scope—not exhaustive correctness or native-speaker certification.

| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1562 | 盆地 | CLEAN | CLEAN | CLEAN | Geographical basin is explicit; household and drainage-area overextension avoided. |
| N2:1563 | 本部 | CLEAN | CLEAN | CLEAN | Central organizational and temporary operational headquarters are covered. |
| N2:1564 | 本来 | CLEAN | CLEAN | CLEAN | Inherent meaning retained; revised はず example clearly expresses expectation. |
| N2:1565 | まあまあ | CLEAN | CLEAN | CLEAN | Passable evaluation and interjections distinguished; feminine label bounded. |
| N2:1566 | 枚数 | CLEAN | CLEAN | CLEAN | Flat-item count, counter and identifying number distinguished; sumo recognition separate. |
| N2:1567 | 毎度 | CLEAN | CLEAN | CLEAN | Frequency and customer greeting taught; familiar and regional uses qualified. |
| N2:1568 | マイナス | CLEAN | CLEAN | CLEAN | Arithmetic and additional recognition distinguished; existing プラス comparison linked. |
| N2:1569 | 巻く | CLEAN | CLEAN | CLEAN | Stable reuse preserved; godan constructions and physical/passive recognition bounded. |
| N2:1570 | 蒔く | CLEAN | CLEAN | CLEAN | Sowing, usual-kana flag and specialized recognition handled without merging identities. |
| N2:1571 | 撒く | CLEAN | CLEAN | CLEAN | Sprinkling, distribution and evasion distinguished; F01 guard added. |
| N2:1572 | 枕 | CLEAN | CLEAN | CLEAN | Applicable まくら identity covers pillow and introductory lead-in. |
| N2:1573 | 曲げる | CLEAN | CLEAN | CLEAN | Transitive ichidan; physical spelling restrictions and figurative uses preserved. |
| N2:1574 | まごまご | CLEAN | CLEAN | CLEAN | Confused, ineffective hesitation remains explicit; ためらう guard justified. |
| N2:1575 | 摩擦 | CLEAN | CLEAN | CLEAN | Physical friction, rubbing constructions and social discord distinguished. |
| N2:1576 | 混ざる | CLEAN | CLEAN | CLEAN | Material mixing and people joining retained; spelling tendency and F02 guard supplied. |
| N2:1577 | 混ざる | CLEAN | CLEAN | CLEAN | Raw 交ざる explicitly taught within the same-entry canonical article. |
| N2:1578 | 混じる | CLEAN | CLEAN | CLEAN | Godan まじる and association sense explicit; separate こんじる excluded from conjugation. |
| N2:1579 | 混じる | CLEAN | CLEAN | CLEAN | Raw 交じる explicitly recognized; its direct 付き合い guard is present. |
| N2:1580 | マスク | CLEAN | CLEAN | CLEAN | Face-mask, features and technical recognition separated from unrelated homographs. |
| N2:1581 | 混ぜる | CLEAN | CLEAN | CLEAN | Transitive ichidan, object/destination marking and intransitive contrasts are clear. |

**Mappings — CLEAN.** All twenty TSV rows agree with the complete mappings and applicable principal records. Raw labels, readings, glosses and entry IDs remain unchanged. 交ざる→混ざる **1603920/まざる** and 交じる→混じる **1603930/まじる** preserve same-entry identities rather than requiring duplicate cards. 蒔く **2611890**, 撒く **1303400** and 巻く **1211200** remain separate まく identities, unrelated to the 幕 card’s identity. Selected teaching and additional recognition were assessed separately; recognition senses were not independently assigned N2.

**Component links — CLEAN.** Every primary written Han remains in word metadata. Existing substantive links cover 地; 本・部; 本・来; 枚・数; 毎・度; 巻; 曲; and 混, with 交 linked in alternative-spelling discussion. No cards were found for 盆・蒔・撒・枕・摩・擦; their absence neither removes those characters from metadata nor warrants fabricated links. Whole-word readings and native-verb okurigana are appropriately distinguished.

**Reciprocal N2 links — CLEAN.** Both directions are present for all four new pairs—**枚数/枚, 混ざる/混, 混じる/混, 混ぜる/混**—and the existing **巻く/巻** pair. No additional reciprocal requirement was imposed on every lower-level component mention.

**Kanji and baseline preservation — CLEAN for correctness, scoped coverage and comprehensibility.** The original patch adds only the 枚数 examples/citation to 枚 and links/common-word entries to 混; their metadata and unrelated teaching remain intact. 巻 is unchanged. Reused 巻く retains its identity, reading, title, original teaching and four original guards while gaining the sourced N2 level, bounded recognition and additive guards.

The correction itself changes exactly **six cards**, adds **four direct exclusion pairs**, and preserves every old declaration. I counted **110 current declarations** across the eighteen articles. No correction changes to identity, title, primary reading, type, level, written-Han metadata, selected senses, raw source fields, TSV or kanji appear in the supplied diff.

## Findings

**All original actionable items below are resolved within the reviewed scope. No new actionable regression was established.**

| ID | Disposition | Evidence and adjudication | Confidence |
|---|---|---|---|
| **GPT F01** | **Resolved** — original medium correctness/quiz finding | `words\撒く.md:9` now directly excludes ぱらぱら. Complete **1102580 sense 1** explicitly includes sprinkling rain **and salt**; `words\ぱらぱら.md:4,15` supplies the full title and actual sprinkling teaching. This supports the direct pair, not merely a rain association or grammatical-class argument. No automatic 蒔く edge follows. | High |
| **GPT F02** | **Resolved** — original medium correctness/quiz finding | `words\混ざる.md:9` and `words\混じる.md:9` each directly exclude 付き合い. Complete **1603920 sense 1**, **1603930 sense 2** and **1495640 sense 1**, together with `words\付き合い.md:4,15`, establish association/socializing overlap. Existing 付き合う/交際 guards would not protect these pairs transitively. | High |
| **Claude B79-F1** | **Resolved as an expectation/translation clarification** | `words\本来.md:19,22,36` now uses **本来なら、今日は休みのはずです** with “should be a day off.” JMdict **1523270 senses 1–3** and the applicable Daijisen 本来 body support original/inherent and proper/expected uses. The improvement does **not** establish that the former 本来なら…です sentence was universally ungrammatical. | High |
| **Claude B79-F2** | **Resolved with a bounded tendency** | `words\混ざる.md:19,27,37,40` shows 交ざる in the people example, explains distinguishable versus blended constituents, and cites the applicable Daijisen **まじる 補説**, to which まざる refers. Canonical 混ざる and its reading remain intact. Neither an absolute solids/liquids law nor a universal ban on 混ざって is taught. | High |
| **Claude B79-F3** | **Resolved** — comprehensibility/navigation | `words\マイナス.md:28` now links the substantively compared existing プラス article. Its actual body and complete **1115630** family support the arithmetic/evaluative comparison. A reciprocal word-to-word backlink is not required. | High |
| **Claude B79-F4** | **Resolved** — correctness/quiz metadata | `words\まごまご.md:9` directly excludes ためらう while line 31 retains **confused, ineffective hesitation**. Complete **1012110**, **1573390**, and `words\ためらう.md:4,16` support the direct overlap. This does not equate every deliberate pause with まごまご or inherit an exclusion through 迷う/ぐずぐず. | Medium-high |

**Other consequential decisions independently retained:**

- **蒔く/散る:** retain. The complete 散る family includes ordinary scattering/dispersal in sense 2, and its actual body teaches that use (`words\散る.md:4,16`). 蒔く’s seed-scattering and lacquer-powder recognition support direct broad scatter overlap. Different transitivity does not establish unrestricted substitution, but neither automatically exempts this pair.
- **合同/組み合わせ with each of the three 混 verbs:** retain. Complete **1285140 sense 1** includes combination/union/amalgamation; **1592290 sense 1** includes combination/assortment. Their actual bodies (`words\合同.md:16` and `words\組み合わせ.md:16`) support those broad labels against actual mixing/being combined. No wider cooperation clique follows.
- **マイナス/欠陥 and マイナス/弱点:** retain. **1126980 senses 4 and 7**, the public “悪い面” teaching, and complete **1253950/1324870** support negative-aspect/drawback versus flaw/weak-point overlap. Both older bodies were freshly read; this does not extend to every physical-damage action.
- **No new 毎度/度, 本来/自然 or まあまあ/普通 guards:** no actionable omission established. The complete applicable families and bodies distinguish an occasion/counting construction from repeated frequency/thanks, natural/unforced/spontaneous from inherent/original/rightful, and ordinary/usual from passable evaluation/calming. Separate emphatic ど and じねん identities were not imported.

These judgments use full titles and ordinary secondary senses in both directions and among choices. Guards remain symmetric, pairwise and nontransitive; topic or POS alone was not treated as decisive.

## Optional

**撒く wording — adopted and resolved:** `words\撒く.md:36` now says “interpretation of the situation.” This is an English wording clarification, not a Japanese reading or lexical change.

**Separate けむにまく idiom — optional/deferred:** the explicitly physical/passive **けむりにまかれる** recognition in 巻く is supported by JMdict **1211200 sense 2** and Daijisen’s encompassing-smoke use. It need not be replaced or expanded into the separate idiom.

**枚数は何枚ですか — optional polish only:** possible redundancy is not an actionable defect; the article also provides straightforward counting examples. No further expansion is necessary for this scope.

## Limits

No required fresh evidence remains unread. Broader original comparison material was inherited rather than completely reread, and prepared or author-inspected material was not automatically counted as reviewer inspection.

The twenty public captures represent **one Digital Daijisen authority via Weblio**, not twenty independent authorities. This confirmation used frozen captures, not fresh public retrievals. Applicable headings were separated from unrelated ちん, こんじる, place/fragrance, にくい, じねん, emphatic ど and para-para dance identities; public numbering was not treated as pinned JMdict indexing.

Git/hash verification and runtime quiz execution were unavailable. Content conclusions therefore rely on the supplied snapshot association and visible files/diffs, not independent commit extraction or runtime guarantees. The review provides no exhaustive-correctness, native-speaker, frequency or unrestricted-substitution certification, and makes no claim of model superiority, measured bias reduction or equal comprehension.
