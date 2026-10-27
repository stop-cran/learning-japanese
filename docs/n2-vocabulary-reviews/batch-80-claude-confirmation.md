## Snapshot
- **Revised commit:** `332aa13666c2a831e21038359680179730fdb1c6`
- **Authored parent:** `6102eb03c5be228d73a5584972bcbd88d138c60c`

I reviewed committed content only. My file tools can't run Git, so the hash, diff-equivalence and preservation claims are the author's. I didn't verify them independently.

## Scope
**Model:** claude-opus-5.5 (claude family). I worked read-only and serially, with no edits, agents or shell.

**Fresh complete reads:**
- The correction snapshot, `correction.patch`, `related.patch` and the reconciliation JSON.
- The two `.github` guidance files and `docs\content-format.md` lines 18–103.
- All 20 assigned articles and the three kanji (角, 祭, 混).
- The compact records, in bounded ranges:
  - mappings 1–20
  - principals 1–20
  - components 1–30
  - labels 1–262, through EOF
- TSV header row [1,1] and rows [1582,1601] only.
- The correction comparison file (lines 1–120 and 121–243, EOF; 36 families).
- The extra comparison file (5 families / 9 senses) and the public bodies file through EOF.
- All 15 required older bodies: 終わる, 敬う, 完了, 合同, 合流, 直に, 頭, 渡す, コレクション, 採る, 白, 白い, 終了, 合う, たちまち.

**Other evidence:**
- One fresh Weblio 跨がる fetch. It returned only Wiktionary text and machine-generated examples (鞍に跨がる, 馬に跨がる), with no Daijisen body. It counts as weak corroboration only.
- My original session evidence carries over: 25 families / 44 senses and three bodies, including 空.md.

**Not read:**
- The two optional private evidence files.
- The author's Kotobank checks, which I did not re-fetch.
- The 479/1231 prepared families beyond what I actually read. Labels are not bodies.

## Verdicts
| Source row | Article | Correctness | Scoped coverage | Comprehensibility | Note |
|---|---|---|---|---|---|
| N2:1582 | 混ぜる | CLEAN | CLEAN | CLEAN | Unchanged reuse; 交ぜる recognized; erroneous raw gloss not taught |
| N2:1583 | またぐ | CLEAN | CLEAN | CLEAN | Astride claim removed; spanning taught; またがる contrast explicit |
| N2:1584 | または | CLEAN | CLEAN | CLEAN | Unchanged N4; 又は written は, pronounced わ |
| N2:1585 | 待合室 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1586 | 待ち合わせる | CLEAN | CLEAN | CLEAN | Unchanged; no 打ち合わせ edge needed |
| N2:1587 | 街角 | CLEAN | CLEAN | CLEAN | 街 stays plain text (no card) |
| N2:1588 | 真っ暗 | CLEAN | CLEAN | CLEAN | Guard added: 終わる |
| N2:1589 | 真っ黒 | CLEAN | CLEAN | CLEAN | Tanning example is now unambiguous |
| N2:1590 | 真っ青 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1591 | 真っ先 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1592 | 真っ白 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1593 | 祭る | CLEAN | CLEAN | CLEAN | Guard added: 敬う |
| N2:1594 | 窓口 | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1595 | まとまる | CLEAN | CLEAN | CLEAN | Five guards added; お金 example; 纏まる taught |
| N2:1596 | まとめる | CLEAN | CLEAN | CLEAN | Four guards added; 纏める taught |
| N2:1597 | 真似る | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1598 | まぶしい | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1599 | まぶた | CLEAN | CLEAN | CLEAN | うわ/したまぶた sourced separately |
| N2:1600 | マフラー | CLEAN | CLEAN | CLEAN | Unchanged |
| N2:1601 | まもなく | CLEAN | CLEAN | CLEAN | Guards added: 直に, たちまち; 間も無く taught |

The separate checks are all CLEAN:
- **Mappings:** all 20 mappings and raw fields are unchanged and match.
- **Component links:** CLEAN, with no invented links.
- **Reciprocal N2 pairs:** the new pairs 街角/角 and 祭る/祭, and the rechecked 混ぜる/混.
- **Baseline preservation:**
  - The kanji are unchanged in this correction; the original 角/祭 edits were additive.
  - Both reuses (混ぜる and または) are unchanged, and または keeps its N4 level.
  - Titles, readings, levels and metadata are preserved.
  - All prior exclusions are kept, and the 13 new ones are additive (151 → 164).

## Findings
**My original findings**
- **Claude B80-01 — RESOLVED.** `words\またぐ.md:16-18,24-27` now teaches spanning and contrasts the separate verb またがる for sitting astride, including the conjugation point. I partly withdraw my original framing. JMdict 1267830 sense 2 ("saddle; straddle") and Daijisen sense 2 「かけ渡す。またがる」 support the "straddle" title. Only the unqualified sitting-astride claim was a defect.
- **Claude B80-02 — RESOLVED.** `words\真っ黒.md:20` now reads 「夏休みに海で遊んで、真っ黒に日焼けしました。」. The old sentence was ambiguous, not proven false.
- **Money example — ADOPTED.** `words\まとまる.md:22` (旅行のお金がまとまった) is natural and matches Daijisen sense 1.

**GPT's proposed exclusion pairs** (all at line 9 of the edited card)
- **GPT B80-01 — ACCEPTED.** 真っ暗/終わる: 1589600 sense 5 (colloquial 終わって(い)る, "hopeless") directly overlaps 真っ暗 sense 2, "utterly hopeless". The old body's focus on ending doesn't cancel that secondary sense.
- **GPT B80-02 — ACCEPTED.** 祭る/敬う: 1250700 ("revere; worship") overlaps 祭る sense 2 ("worship"). This rests on actual reverence, not religious topic.
- **GPT B80-03 — ACCEPTED.** まとまる/完了 and まとめる/完了: 1211630 かんりょう ("completion") overlaps 1611640 ("be completed") and 1440930 sense 3 ("bring to a conclusion"). The unrelated ワンラ entry is not used.
- **GPT B80-04 — ACCEPTED.** まとまる/合同, まとめる/合同 and まとまる/合流: the 合同 body (merging into one) and 1285390 sense 2 (groups joining) support them. No まとめる/合流 omission is established.
- **GPT B80-05 — ACCEPTED.** まもなく/直に: `直に.md:27,35` explicitly recognizes じきに 1430700 ("soon"), and Daijisen glosses まもなく as じきに. The card's primary じかに identity is preserved.

**Pairs the author found**
- **まとまる/合う and まとめる/合う — ACCEPTED (moderate confidence).** 1284430 sense 1 ("come together; unite") and `合う.md:15,42` (agreement; coming together) support them on their own, not through 合わせる.
- **まとまる/終了 and まとめる/終了 — ACCEPTED.** 1333040 ("end; conclusion") overlaps the selected senses "be completed" and "bring to a conclusion".
- **まもなく/たちまち — ACCEPTED (moderate confidence).** 1288480 sense 1 ("in a moment; immediately") and `たちまち.md:16-17` ("in a very short time") overlap まもなく's "in a short time". This rests on that overlap, not on harmlessness; it does not claim the words are interchangeable.

**Other items**
- **Guards kept from before:** these remain optional and defensible.
  - 真っ先/頭: 1582310, "beginning".
  - またぐ/渡す: 1444610 sense 2, "lay across".
  - まとまる/コレクション and まとまる/採る: actual collecting.
  - 真っ青/白 is the weakest. Pallor appears at `白い.md:15` (顔が白い), not in 白's own body or senses.
- **Regressions:** none found.
- **Remaining actionable defects:** none.
- **What my first review missed:** my shallower initial review left out all 13 accepted pairs. They were real low-severity gaps; the author found five of them, which neither reviewer is credited with.

## Optional
- Make clear that "straddle" in the またぐ title means spanning, not sitting astride.
- Deferred expansions still available: 年をまたぐ, 〜て間もなく, the street sense of 街角, and railway 待ち合わせる.
- Possibly reconsider whether 真っ青/白 should stay or have its rationale documented.

## Limits
- I did not inspect all 479/1231 prepared families exhaustively.
- I did not independently re-fetch Kotobank (NKJ) またがる or かんりょう. My one Weblio fetch had no lexical body.
- The public captures are a single authority (Daijisen via Weblio).
- I could not verify Git hashes or preservation myself.
- This is not exhaustive correctness, native-speaker certification, a frequency claim or a guarantee of runtime quiz behaviour.
