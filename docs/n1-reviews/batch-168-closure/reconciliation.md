# Batch 168 review reconciliation

Snapshots: initial `cbf5c2c5ca52758812aff3e61ae421e72fadd9e7`, follow-up `e9b5df6bd6c6c9fed4cce91d5ac4c481d208007c`, final `159207693284b0451beeb95e8b59dad2e6b5e28f`, all on base `ac5304bac6a9352c7e6d98526e932875e6445edf`. The reviewed teaching was then integrated with upstream `2f5cade160e8340705e7e980ae8c2fb3f5bd118a` (question-counting counters). See `integration` in the batch ledger.

Reviewers were run serially, blind to one another at the initial stage: claude-sonnet-5.5 (correctness and scoped coverage), gpt-6.2-sol (consistency and quiz safety) and grok-4.7 (comprehensibility). The same original sessions received their own findings, the revised snapshot and the actual diff at each later stage. Reports are archived in `reports/`.

## Initial findings (snapshot cbf5c2c5)

Findings shared across reviewers are merged by underlying defect.

| Finding | Raised by | Disposition |
|---|---|---|
| Missing direct pairs 弔–忌, 弔–悔, 忌–悔, 忌–憎, 弥–継 | Claude Q1–Q3, GPT | **Resolved.** 弔 excludes 忌 and 悔; 忌 excludes 憎 and 悔; 弥 excludes 継. The 弔–忌 pair is declared once, on 弔. |
| 征–克 (conquer/overcome) | Claude Q5, GPT | **Resolved.** 克 added to 征. |
| 彰–賛 (commend/praise) | GPT (Claude optional) | **Resolved.** 賛 added to 彰. |
| 弊害–毒 (harmful influence) | Claude Q6, GPT | **Resolved.** 毒 added to 弊害. |
| 弓 vs 礼 / お辞儀 ("bow") | Claude Q4 (GPT judged the qualifier sufficient) | **Resolved.** Kanji 弓 excludes 礼; after follow-up, word 弓 excludes お辞儀 and 礼. |
| 弦楽: 管弦楽 presented as the kanji word for オーケストラ | Claude F1, GPT, Grok | **Resolved.** オーケストラ is the ensemble; 管弦楽 is orchestral music; 弦楽 is music for strings. 弦楽四重奏 is glossed as a string quartet. |
| 回忌: 一回忌 treated as equal to 一周忌; the counting rule came too late; citations incomplete | Claude F2, GPT, Grok | **Resolved over two rounds.** Defined as a numbered death anniversary (short for 年回忌). 一周忌 is the usual first anniversary, with 一回忌 recorded but not usual. The counting rule sits beside the meaning, and entries 1161330, 1814080 and 1319250 are cited. |
| 弦 つる: pot-handle sense | Claude F4, GPT, Grok | **Resolved.** The pot-handle sense is now qualified with "especially when written 鉉" (JMdict 1578400). |
| 弥 わた.る: blanket "write 渡る" | GPT | **Resolved.** The card now says 渡る for crossing, or kana わたる for spanning or extending over. |
| 征服 example: 三日かけて translated "After three days" | Claude F5 | **Resolved.** Now "Taking three days, ...". |
| 弊害: 損害 contrast | Claude F6 | **Resolved.** 損害 is now "the damage or loss itself, often counted in money". |
| 弓 example: unattested 弓を習う used to prove the archery sense | Claude F3, Grok optional | **Resolved.** The examples no longer rely on that collocation. The note points to 弓道 for Japanese archery, and the wording was narrowed again after follow-up. |
| 弥縫策 kana reading ambiguity (ただのびほうさく) | Grok optional | **Resolved.** A space was added in the initial correction. After follow-up both reviewers found the spacing inconsistent, so example 1 was rewritten (値上げを先に延ばすのは、弥縫策にすぎない。) to avoid the ambiguity without special spacing. |
| 絃楽 called "older" | Claude, GPT optional | **Adopted.** Now an "alternative spelling". |
| 弥 shape note: 尔 vs 尓 | Claude optional | **Adopted.** The note uses 尓. |

## Follow-up residues (snapshot e9b5df6b)

- **回忌 counting sentence ambiguous** (GPT, Grok): **resolved.** It now reads: "The first anniversary, one year after the death, is usually 一周忌. 三回忌 is two years after the death, and from 三回忌 on the number is the years since the death plus one."
- **回忌 Dictionary line lacked 1161330, 1814080 and 1319250** (Claude, GPT): **resolved.** The numbered-form entries are now cited.
- **弓道 note overgeneralized** (GPT): **resolved.** It now reads "For traditional Japanese archery, use 弓道 (きゅうどう)."
- **Word 弓 should also exclude 礼** (Claude): **resolved.**
- **Inconsistent kana space in びほうさく** (Claude, GPT): **resolved** by rewriting the example, as above.

## Final confirmations (snapshot 15920769)

Claude, GPT and Grok each confirmed that no actionable residue remains. GPT rated every card CLEAN and counted 19 word and 46 kanji exclusion declarations. The parties agreed there were no remaining defects, so no further revision was made.

**Correction to an author note.** JMdict family 1002030 (お辞儀) is in the batch's family record because of the new 弓 exclusion. It is not cited on the 弓 card's Dictionary line, contrary to the author's note in the final packet (GPT).

## Optional items not adopted

- **Claude:** an active 表彰 example; 色彩 vs 紅葉/絵の具 and 弔問 vs 香典 exclusions; 法廷 polish; a sentence citing the Kanjipedia-only 弥 readings; extra 弦楽 citations; the 回忌 counting rule appearing twice; citing 1002030/1228540 on 弓; rewording "The quiz keeps...".
- **GPT:** consolidating the duplicate JMdict lists on 表.
- **Grok:** shortening the 弔問/表彰 examples; 色彩 example 2 being slightly tautological; a sharper 征服/克服 note.

These are editorial preferences. None is an established defect.

## Unverified claims and limits

- **UNVERIFIED:** the claim that no preferred tagged 弥 candidate supports ビ better than 弥縫策. This is author-side inventory evidence; reviewers could not establish the full candidate inventory.
- Daijisen, Kotobank and Kanjipedia page checks, the standard-use table rows, and the KanjiVG source blobs are author evidence recorded in the batch sources. Reviewers saw only the records. The Daijisen-attributed statements (法廷 usually inside a courthouse; the figurative use of 色彩; 回忌 as short for 年回忌) were not independently verified by reviewers.
- Reading-collision and quiz-pool results come from author-side static simulation, not observed app behavior.
- Upstream integration: `kanji/問.md` combines the reviewed B168 lines with the upstream counter note. Its reviewed additions are byte-identical; only their position relative to the upstream note was chosen. The ledger row for the Metadata line was re-anchored to match. Its 39 other reviewed article and stroke blobs are preserved byte-for-byte.
- These are packet-based blind facet reviews with bounded confirmations. There is no native-speaker, device, Android or whole-set acceptance.
