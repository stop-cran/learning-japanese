# Batch 78 follow-up: the 干す/放る guard is justified and all twenty rows remain CLEAN

## Snapshot
- **Revised commit:** d925ea0a1c2814369415031ad85cd0b0b9386624
- **Parent:** f7271f70f15e702deaa369ae152a6fc2ba430635
- I reviewed committed content only. My file tools cannot run Git, so the commit, hash and preservation checks were done by the author, not by me.

## Scope
- **Model:** claude-opus-5.5 (Claude family), resuming my original session. I made no edits and used no shell, agents or delegation.
- **Fresh complete reads, in order:**
  - follow-up snapshot (read first), follow-up.patch and follow-up reconciliation
  - copilot-instructions.md, content-structure.instructions.md and content-format.md lines 18–103
  - words\干す.md and words\放る.md, complete
  - follow-up comparison reading (JMdict entries 1603510 and 1516530, six senses)
  - follow-up public reading through EOF
  - all twenty compact mappings
  - TSV header [1,1] and rows [1542,1561]
- **Deviation:** I requested the two TSV ranges in one parallel call instead of serially, as I did in the full confirmation. The row scope was exact. The reconciliation records `tsvScopeDeviation: null` for my earlier report; that seems to cover row scope only, not this ordering slip.
- **Not read:** the optional follow-up-review-evidence.json, docs\confusable-words.md (no title changed) and the six kanji cards. I made no web fetches.
- **Inherited:** the other eighteen article verdicts and the kanji, component-link and reciprocity assessments come from my full confirmation at f7271f70. This is not a new full-batch reread.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1542 | 防犯 | CLEAN | CLEAN | CLEAN | Inherited (f7271f70) |
| N2:1543 | 方面 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1544 | 坊や | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1545 | 放る | CLEAN | CLEAN | CLEAN | Fresh read; file unchanged; lines 9 and 21 support the 干す pair |
| N2:1546 | ボーナス | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1547 | 朗らか | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1548 | 牧場 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1549 | 牧畜 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1550 | 保健 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1551 | 募集 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1552 | 干す | CLEAN | CLEAN | CLEAN | Fresh read; only line 9 changed (adds 放る) |
| N2:1553 | ポスター | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1554 | 北極 | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1555 | 坊っちゃん | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1556 | ほどく | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1557 | 濠 | CLEAN | CLEAN | CLEAN | Inherited; fresh TSV/mapping read confirms 堀→濠, entry 1522060, level 3 |
| N2:1558 | 掘る | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1559 | 彫る | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1560 | ぼろ | CLEAN | CLEAN | CLEAN | Inherited |
| N2:1561 | 盆 | CLEAN | CLEAN | CLEAN | Inherited |

- **Mappings: CLEAN, freshly checked.** All twenty TSV rows match the compact mappings on entry, article, level and selected senses. The raw fields are as in my full confirmation; I did not compare them byte for byte.
- **Component links: CLEAN.** The 干 link in 干す and the 放 link in 放る are freshly seen; the rest are inherited.
- **Reciprocal N2 pairs (防犯/防, 牧畜/畜, 北極/極, 掘る/掘, 募集/募, 干す/干): CLEAN, inherited.** No kanji card changed.
- **Baseline preservation: CLEAN.** The patch changes only 干す.md line 9 and removes nothing. That no other file changed is the author's assertion.

## Findings
**Adopted guard 干す/放る (from my confirmation's Optional section): resolved.** Medium-high confidence.
- Daijisen gives ほす sense 4 as 故意に仕事や役割を与えないでほうっておく。また、無視する (deliberately leave someone without work or a role; also, ignore them).
- 放る.md:4 is titled "throw; neglect; abandon", and 放る.md:21 teaches 放っておく as "leave something or someone alone".
- JMdict 1516530 sense 2 includes "to neglect" and "to leave alone".
- In the other direction, the English idiom in 干す's title ("hang out to dry") can also suggest abandonment.

The guard rests on this direct overlap, not on both cards excluding 無視, a neglect cluster, or harmlessness. It claims nothing about drying, throwing or losing in general, and 干す.md:43–48 keeps the work/role qualification. No 失う guard was added.
- The declaration is valid: one top-level key, an existing target, no repeat, no self-reference, and neither card has `quiz_distractors`.
- The Daijisen neighbours were not used as evidence: the ひる (expel) and まる (excrete) headings next to ほうる, and ほす senses 5–6, which cite classical sources (源氏物語, 日葡辞書).

**Earlier findings (B78-F1, B78-F2, B78-GPT-01 to 04):** these stay resolved as concluded in my full confirmation and are not reverified here. The freshly read 干す/無視 and 放る/止める/中止 guards are still present.

**Regressions:** none.

## Optional
None.

## Limits
- This was not a fresh full-batch reread; the other eighteen verdicts are inherited.
- I did not independently run Git or hash checks, test runtime quiz behaviour, or check any frequency claim.
- The public evidence is one authority (Digital Daijisen via Weblio, frozen captures); I fetched nothing new.
- This is not a native-speaker or exhaustive-correctness certification.
