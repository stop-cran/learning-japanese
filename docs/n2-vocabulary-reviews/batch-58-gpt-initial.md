## Snapshot: 65c98d9db417dd02abd5f24f1b48a5d95947a3f1 — committed content only

**Two actionable findings:** a missing direct 展開/成長 quiz exclusion and an unqualified rare spelling in 鉄砲.

The frozen manifest identifies parent `86c16b88ae91b6064c55d1d379d904b3121aa44c` and declares clean committed content. File tools cannot execute Git, so I could not independently verify the checkout’s commit, cleanliness, or correspondence to the manifest’s hashes.

## Scope:

**Actual model:** GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`. This was read-only: no edits, agents, or delegation.

I completely read all seventeen new articles, both reused articles, `kanji\鉄.md`, `kanji\橋.md`, `kanji\照.md`, and the supplied `related.patch`. I read the required repository instructions, `docs\content-format.md:18–103`, both permitted source snapshots, `docs\confusable-words.md`, `docs\jlpt-levels.md`, and the TSV header plus exactly N2:1142–N2:1161.

Private evidence reads comprised the complete mappings, principals, components, and labels JSONL files; complete `principal-reading.txt`; all eleven complete family-inspection renderings; complete support-comparison rendering; and both primary and supplemental public-body JSON/text files. These cover the supplied twenty mappings, nineteen principal families/forty senses, thirty component records, 243 labels, and twenty-one public capture receipts. I inspected restrictions, spelling flags, effective/inherited POS, raw source fields, and selected versus additional senses. The reported 220-family/537-sense union is the packet’s accounting, not an independently executed count or equivalence check. Only lines 1–100 of the large `review-evidence.json` were read directly; the bounded equivalent renderings supplied the remaining relevant evidence.

**Complete related-body reads:** 117 existing word articles, excluding the two assigned reuses:

- Completion: 仕上がる, 完成, 完了, 終わる, 終える, 終了, 済む, 済ませる, できる, しまう, 仕舞い, 終わり, 上がる, 出来上がり, 酔う.
- Accuracy, suitability, and writing: 正確, 正しい, 明確, 確か, 適切, 適当, 適する, 妥当, 相当, 便利, 安い, 適度, 嘘, ノート, 日記, メモ.
- Objects, procedures, and body parts: 橋, 順序, 方法, 過程, 処理, 銃, 武器, コート, テニス, タオル, 布, ハンカチ, 雑巾, 手, 腕, 指.
- Position and address: 前, 直前, 正面, 近く, こちら, こっち, 立場, 私, 僕, あなた, 君, おまえ, 顔.
- Arrivals and shining: 迎える, 迎え, 歓迎, 会う, 出会い, あいさつ, 応接, 受付, お帰り, 出会う, 光る, 輝く, 射す, 差す, 晴れる, 曇る, 送る.
- Development and biography comparisons: 発展, 発達, 拡大, 拡張, 拡充, 広がる, 伸ばす, 伸びる, 増加, 開く, 開ける, 進歩, 成長, 回り, 物語, 歴史, 記録, 小説, 電気.
- Other checks: 光, 明かり, 灯, 比べる, 比較, 参考, 人生, 揃う, 準備, 支度, 用意, 確実, もっとも, いらっしゃい, 流れ, 生長, ごつごつ, ざらざら, 粗い, 荷物, 豚肉.

This includes every directly declared exclusion target in the assigned articles. Other label records were not treated as full-body inspections. Prohibited ledgers, author rationale, reports, scripts, and inputs were not read.

A fresh Jisho API response supplied both 成長 senses as corroboration. Other fresh retrieval attempts returned encyclopedic material, an unrelated redirect, or an access gate; those were not counted as lexical verification.

## Verdicts:

**CLEAN** means no actionable defect established within the inspected scope—not exhaustive correctness or native-speaker certification. Correctness includes quiz-answer ambiguity.

| Source | Exact article association | Selected JMdict senses | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|---|---|
| N2:1142 | `words\出来上がる.md` — new | 1340610:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1143 | `words\的確.md` — new | 1437290:1 | CLEAN | CLEAN | CLEAN |
| N2:1144 | `words\的確.md` — same new article; raw 適確 | 1437290:1 | CLEAN | CLEAN | CLEAN |
| N2:1145 | `words\手首.md` — new | 1327770:1 | CLEAN | CLEAN | CLEAN |
| N2:1146 | `words\でこぼこ.md` — reused; raw 凸凹 | 1582410:1 | CLEAN | CLEAN | CLEAN |
| N2:1147 | `words\手頃.md` — new | 1327660:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1148 | `words\でたらめ.md` — new | 1339630:1–2 | CLEAN | CLEAN | CLEAN |
| N2:1149 | `words\手帳.md` — new | 1598330:1 | CLEAN | CLEAN | CLEAN |
| N2:1150 | `words\鉄橋.md` — new | 1437820:1 | CLEAN | CLEAN | CLEAN |
| N2:1151 | `words\手続き.md` — new | 1598350:1 | CLEAN | CLEAN | CLEAN |
| N2:1152 | `words\鉄砲.md` — new | 1438010:1 | **NEEDS FIX — F02** | CLEAN | CLEAN |
| N2:1153 | `words\テニスコート.md` — new | 1080030:1 | CLEAN | CLEAN | CLEAN |
| N2:1154 | `words\手拭い.md` — new | 1598400:1 | CLEAN | CLEAN | CLEAN |
| N2:1155 | `words\手前.md` — new | 1328030:1–3,6–7 | CLEAN | CLEAN | CLEAN |
| N2:1156 | `words\出迎え.md` — new | 1338710:1 | CLEAN | CLEAN | CLEAN |
| N2:1157 | `words\出迎える.md` — new | 1338720:1 | CLEAN | CLEAN | CLEAN |
| N2:1158 | `words\照らす.md` — reused | 1350840:1 | CLEAN | CLEAN | CLEAN |
| N2:1159 | `words\照る.md` — new | 1350860:1 | CLEAN | CLEAN | CLEAN |
| N2:1160 | `words\展開.md` — new | 1440600:1–2,5 | **NEEDS FIX — F01** | CLEAN | CLEAN |
| N2:1161 | `words\伝記.md` — new | 1441960:1 | CLEAN | CLEAN | CLEAN |

**Mapping assessment:** Article associations, entry IDs, readings, selected indices, and additional-sense allocations are **CLEAN for all twenty rows**. The N2:1152 narrative assertion that rare 鉄炮 “remains qualified” is not borne out by the article; see F02. This is not an entry/sense-selection error.

Additional allocations remain appropriately bounded: でこぼこ 1582410:2; 手帳 1598330:2–3; 鉄砲 1438010:2–3; 手前 1328030:4–5; 照らす 1350840:2; 照る 1350860:2; 展開 1440600:3–4,6. Their inclusion does not independently assign every meaning N2 status.

The consequential source distinctions are handled correctly: 的確/適確 and both recorded readings are recognized without invented restrictions; 出来上がる does not become a general “by definition” adverb; 手帳’s mixed reading follows the inspected native-first precedents; 手続き does not infer a universal verbalization ban; 手前 separates marked pronouns from spatial/social constructions and てめえ; 照る is godan and bounds its Noh-mask sense; 展開 confines the compression contrast to computing and resolves 解凍 sense 2; unrelated mixed public headings are not imported into 鉄橋, 手拭い, or 伝記.

| Edited kanji | Correctness | Scoped coverage | Comprehensibility | Reciprocity and preservation |
|---|---|---|---|---|
| `kanji\鉄.md` | CLEAN | CLEAN | CLEAN | テツ row at line 30 and Common words at 36–37 link 鉄橋 **てっきょう** and 鉄砲 **てっぽう**. Baseline metadata preserved in the supplied patch. |
| `kanji\橋.md` | CLEAN | CLEAN | CLEAN | キョウ row at line 28 and Common words at 34 link 鉄橋 **てっきょう**. Baseline metadata preserved. |
| `kanji\照.md` | CLEAN | CLEAN | CLEAN | Relevant rows at 31–32 and Common words at 37–38 link 照る **てる** and 照らす **てらす**. Baseline metadata preserved. |

All five required reciprocal pairs have substantive word-side component explanations and both required kanji-side surfaces. New-word primary-spelling kanji arrays are complete; existing component links are substantive. Missing component cards were not invented, and body variants were not incorrectly added to primary-spelling arrays.

**Reuse preservation: CLEAN against the supplied patch.** でこぼこ retains its ID, reading, title, type, empty kanji array, tags, and exclusion state; only sourced N2 and explicit 凸凹 recognition are added. Its restricted imbalance sense remains additional baseline teaching. 照らす retains its metadata and all eight original exclusions; the existing 照る comparison becomes a link, while its comparison/reference construction remains unchanged baseline content. Neither reuse overwrites an existing easier level: both previously lacked one.

Quiz review used complete titles and ordinary secondary senses, not POS exemptions or transitive exclusion chains. In particular, 出迎え/迎え and 鉄砲/銃 have identical titles and already receive exact-title deduplication. 差す’s actual sunlight sense supports its protection against 照る despite its umbrella-focused title.

## Findings:

**F01 — Medium — Quiz correctness: missing direct 展開/成長 exclusion**

**Location:** `words\展開.md:4,9,16–19`; related evidence in `words\成長.md:4,9,16–22,48–50`.

The complete titles are **“unfolding; development; expansion”** and **“growth; development.”** Their ordinary overlap is not merely topical: 展開 teaches developing a business, while 成長 explicitly covers company growth and organizational/economic expansion. Without sentence context, their development/expansion labels can produce defensible competing answers.

Neither article declares the pair. Existing protection through 発展 or 発達 does not propagate to 成長, and the unequal title strings do not deduplicate.

**Minimal remedy:** Add `成長` to 展開’s `quiz_exclusions`. One declaration protects both directions and co-occurrence among other choices; no title distortion or unrelated exclusion redesign is needed.

**Exact evidence:** The complete article bodies above; pinned JMdict 1440600 senses 1–2; the fresh Jisho 成長 result’s development and company/economy-growth senses; and `docs\content-format.md:85–96`, which specifies pairwise, nontransitive exclusions and semantic-title review.

**Confidence:** High.

**F02 — Low — Spelling/register correctness: 鉄炮 loses its explicit rarity qualification**

**Location:** `words\鉄砲.md:23`.

The article says only **“鉄炮 is another dictionary spelling.”** The complete principal record explicitly flags 鉄炮 **“rarely used kanji form.”** Presenting the alternative without that qualification can suggest an ordinary interchangeable writing choice.

The blind mapping’s N2:1152 source note additionally asserts **“Rare 鉄炮 remains qualified,”** but that qualification is absent from the article.

**Minimal remedy:** Change the sentence to **“鉄炮 is a rare dictionary spelling.”** Retain 鉄砲 as the primary spelling and leave its metadata and source association unchanged.

**Exact evidence:** `batch-58-review-principals.jsonl:13`, complete entry 1438010 spelling record; `batch-58-review-mappings.jsonl:11`; `words\鉄砲.md:23`.

**Confidence:** High.

## Optional:

At `words\手頃.md:33`, expand the JMdict citation from **sense 1** to **senses 1–2**. The mapping already selects both, and the body correctly teaches handy/convenient and suitable/reasonable/moderate applications. This is nonblocking citation polish, not missing teaching.

## Limits:

The committed-only target, clean state, file hashes, compact-rendering equivalence, and author inspection counts were not independently verified through Git or executable checks. Baseline preservation judgments therefore rest on the supplied patch plus the complete current articles.

The twenty-one supplied positive public captures are **one dictionary service**, Digital Daijisen via Weblio—not twenty-one independent dictionaries or fresh reviewer retrievals. The fresh Jisho 成長 result corroborates meaning but does not replace a frozen raw JMdict record. Failed, redirected, gated, encyclopedic, or partial fresh retrievals were not treated as lexical verification.

I did not execute the app or inspect its implementation; quiz behavior was assessed against the permitted documented contract. This is not an exhaustive audit of every repository word, every possible fallback choice, corpus frequency, pronunciation variation, or native-speaker naturalness. Bodies outside the stated inventory remain uninspected; label-only evidence was not promoted to full-body review.
