# Batch 78 confirmation review: all twenty rows confirmed clean

## Snapshot
- **Revised commit:** f7271f70f15e702deaa369ae152a6fc2ba430635
- **Parent:** da41f6ef4025d64580008f97051637a74522025b
- I reviewed committed content only. My file tools cannot run Git, so the hash, equivalence and preservation checks are the author's, not mine.

## Scope
**Model:** claude-opus-5.5 (Claude family), resuming my original session. I made no edits and used no agents or shell.

**Fresh complete reads:**
- The correction snapshot, correction.patch, related.patch and the reconciliation.
- copilot-instructions.md, content-structure.instructions.md and content-format.md lines 18–103.
- All 20 current articles and all 6 kanji cards.
- The compact records: 20 mappings, 20 principal families (45 senses), 31 component records and 268 labels.
- The TSV header [1,1] and rows [1542,1561]. I requested these two ranges in one parallel call, which is a small departure from strictly serial reading.
- Both correction comparison renderings (11 families/36 senses and 10/41; 21/77 in total), the mining file (採掘, 1/1), public-bodies.txt through EOF and extra-public-bodies.txt.
- All 12 required older bodies: 止める, 中止, 愉快, 無視, 穴, 失敗, 開く, 角度, 安全, 祭, お祭り and 失う.

After those complete reads, I grepped six assigned articles plus 無視 for title and exclusion lines.

**Not read:**
- The two optional JSON files.
- The prepared 546-family union, the family-inspection chunks (I returned 0 chunks), the old-body-inspection renderings and public-bodies.json.

I made no web fetches. I accept the author's count of my original depth (21 families/46 senses; 4 bodies, 3 of them the assigned reuses). I did not compute an exact union with this pass.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1542 | 防犯 | CLEAN | CLEAN | CLEAN | Linked both ways with 防. No 安全 guard needed: line 35 says it "does not mean every kind of safety". |
| N2:1543 | 方面 | CLEAN | CLEAN | CLEAN | The 角度 guard is justified by 方面's "aspect; angle" sense and the viewpoint use taught in 角度. |
| N2:1544 | 坊や | CLEAN | CLEAN | CLEAN | Unchanged. 坊 stays plain text. |
| N2:1545 | 放る | CLEAN | CLEAN | CLEAN | New guards against 止める and 中止. |
| N2:1546 | ボーナス | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1547 | 朗らか | CLEAN | CLEAN | CLEAN | New guard against 愉快. |
| N2:1548 | 牧場 | CLEAN | CLEAN | CLEAN | Retitling is optional. |
| N2:1549 | 牧畜 | CLEAN | CLEAN | CLEAN | Linked both ways with 畜. |
| N2:1550 | 保健 | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1551 | 募集 | CLEAN | CLEAN | CLEAN | Reused card gains N2 and a 集金 guard; old guards intact; linked with 募. |
| N2:1552 | 干す | CLEAN | CLEAN | CLEAN | Reused card gains N2 and a 無視 guard; no 失う guard needed; linked with 干. |
| N2:1553 | ポスター | CLEAN | CLEAN | CLEAN | Unchanged. |
| N2:1554 | 北極 | CLEAN | CLEAN | CLEAN | Linked both ways with 極. |
| N2:1555 | 坊っちゃん | CLEAN | CLEAN | CLEAN | Lexical meaning comes from the 坊ちゃん/ぼっちゃん captures, not the novel. |
| N2:1556 | ほどく | CLEAN | CLEAN | CLEAN | Kept separate from 解く/とく (1198890). The 開く guard is justified. |
| N2:1557 | 濠 | CLEAN | CLEAN | CLEAN | F1 resolved. N3 level and the 濠 filename are kept. |
| N2:1558 | 掘る | CLEAN | CLEAN | CLEAN | Linked both ways with 掘. |
| N2:1559 | 彫る | CLEAN | CLEAN | CLEAN | F2 resolved. |
| N2:1560 | ぼろ | CLEAN | CLEAN | CLEAN | New guards against 穴 and 失敗. |
| N2:1561 | 盆 | CLEAN | CLEAN | CLEAN | Household guards kept; no 祭 guard needed. |

- **Mappings:** CLEAN. All 20 associations and raw fields match. Source 堀 maps to the existing 濠 card: entry 1522060, reading ほり, level N3, with 堀 as the teaching spelling.
- **Component links:** CLEAN. Existing links are correct. Characters without cards (坊, 朗, 牧, 保, 健, 彫, 盆, 濠) stay plain text, with no invented cards.
- **Reciprocal N2 pairs:** CLEAN. All six are present in both directions, in each kanji's reading row and Common words: 防犯/防, 牧畜/畜, 北極/極, 掘る/掘, 募集/募 and 干す/干.
- **Baseline preservation:** CLEAN.
  - The correction changes six word files only. It adds guards and wording and removes nothing.
  - It makes no changes to kanji cards, titles, levels or metadata.
  - The total of 104 declarations is the author's count; I did not recount it.

## Findings
**B78-F1 (濠): resolved.** High confidence.
- Line 19 now shows 堀 in an example. Line 25 recommends 堀 and calls 濠/壕 marked alternatives, matching the Daijisen heading ほり【堀／×濠／×壕】.
- Line 33 gives both "moat" and "canal". Lines 35 and 38 keep N3 and the stable identity.

**B78-F2 (彫る): resolved.** High confidence. Line 16 now separates を, で and に, consistent with examples 18–19.

**Guards added from GPT's findings:**
- **B78-GPT-01: resolved, I agree.** High confidence.
  - The 止める card is titled "stop something; discontinue", and 中止 is "cancellation; discontinuation".
  - Daijisen ほうる gives 途中でやめる and あきらめて放棄する.
- **B78-GPT-02: resolved.** Medium-high confidence. The 愉快 body covers a cheerful character, and its family 1538560 includes "cheerful".
- **B78-GPT-03: resolved.** Medium-high confidence.
  - Daijisen ほす gives 故意に…ほうっておく。また、無視する.
  - JMdict sense 4 is also "deprive of role", but the 無視 clause appears only in Daijisen.
- **B78-GPT-04: resolved.** High confidence.
  - 穴 teaches the flaw sense (計画に穴がある; JMdict sense 6).
  - Daijisen ぼろ sense 3 gives 隠していた都合の悪い点。また、失敗.

**My original optional concerns:**
- **開く and 角度 guards: withdrawn.**
  - The 開く article teaches ひらく, including 本をひらく, and JMdict 1202440 gives "to undo; to unpack".
  - The 角度 article teaches the viewpoint sense (別の角度から).
- **防犯/安全, 盆/祭/お祭り and 干す/失う: withdrawn.**
  - 安全 is a state of being safe, while 防犯 is a crime-prevention measure.
  - 祭 is the broader festival category, while 盆 names the Obon observance.
  - 失う describes the subject losing something, while active 干す, titled "hang out to dry; air out", deprives someone else.
- **盆 household guards: keep.** JMdict sense 2 (family; household) is unmarked.

**Deferred items:** the 牧場 title, the はふる history, replacing the ぼろ and moat examples, and the 南極/乾 backlinks are optional, not defects.

**Qualification:** my original summary understated the kanji patch. It also adds reading-row examples and Common-words items.

**Remaining actionable defects:** none. I found no regressions.

## Optional
- **干す/放る guard.** Daijisen defines 干す sense 4 with ほうっておく, and 放る teaches 放っておく. I have not established a defect, because that definition is limited to withholding work or a role. Low confidence; worth considering.
- Retitling 牧場 as "ranch; pasture" and the 南極/乾 backlinks remain optional polish.

## Limits
- The 22 public captures come from one authority, Digital Daijisen via Weblio, and I retrieved nothing fresh. JMdict and KANJIDIC reached me only through the author's prepared records.
- I did not read the full 546-family prepared union, and leaving something out does not prove it is absent.
- I did not run the quiz or verify how exclusions are applied at runtime.
- I have no measured frequency evidence for 堀 over 濠; JMdict priority tags and Daijisen's marking are not measurements.
- This is not a guarantee of exhaustive correctness or a native-speaker certification.
