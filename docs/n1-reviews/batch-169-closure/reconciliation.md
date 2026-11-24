# Batch 169 review reconciliation

Snapshots: initial `dc46cc08608fa8714a68a36af77fb9ebd1b8fa37`, follow-up `cfef4688ebb87df5d3532cac45d372ccf502da34`, final `9ffbf4529ac7585ca28fd623dbd64883f4699e04`, all on base `894d30525e87a394b0b5a6de9767d2d1084b6ed3`. The reviewed teaching was then integrated with upstream `37404d7ecc1683e320bc82fa0a83ba0e575fd878` (two illustrated onomatopoeia cards) in `6ed51f5020519b07650e247cbb31ac2c4de210e2`. See `integration` in the batch ledger.

Reviewers were run serially, blind to one another at the initial stage: claude-sonnet-5.5 (correctness and scoped coverage), gpt-6.2-sol (consistency and quiz safety) and grok-4.7 (comprehensibility). The same original sessions received their own findings, the revised snapshot and the actual diff at each later stage. Reports are archived in `reports/`.

## Initial findings (snapshot dc46cc08)

Findings shared across reviewers are merged by underlying defect.

| Finding | Raised by | Disposition |
|---|---|---|
| Missing direct pairs 忍ぶ–潜る ("hide"), 忠実–ねっしん ("devoted"), 悼–愁 ("grieve; lament"), 追悼–嘆く ("grieve") | GPT (Claude listed exclusion symmetry as a limit) | **Resolved.** Declared once each, on 忍ぶ, 忠実, 悼 and 追悼. The 悼 notes keep the distinction between mourning a death and the broader sorrow or worry of 愁. |
| 満悦 omitted JMdict 1526740's "usu. as ご満悦" and explained ご only as a polite prefix | Claude F1, GPT, Grok 1 | **Resolved over two rounds.** The Meaning section gives the JMdict note, the ご満悦 example comes first, and 満悦する is kept as also used (Daijisen example). "Less typical" was not adopted because no source in hand states a comparative frequency. After follow-up, "with the prefix ご" and the plain-narration sentence were dropped. |
| 恥を忍んで example translated "Swallowing my pride" | Grok 2 | **Resolved.** Now "Swallowing my shame". |
| 惨 むご.い row taught 酷い as むごい | Grok 3 | **Resolved.** 酷い was removed; the row says JMdict marks 惨い as usually kana and that the standard-use table does not list this reading for 惨. |
| 恒 made 常に sound like the only spelling | GPT | **Resolved over two rounds.** The reading row and notes call 常に the ordinary spelling, record Kanjipedia's つね.に for 恒 as outside standard use, and say it is not used in practice questions. |
| 愁い given as a plain second spelling | GPT, Grok optional | **Resolved.** The row gives JMdict 1540740's sense-local preferences (sorrow or grief especially 愁い, worry especially 憂い) as preferences, not strict rules. |
| 満悦 recorded as an "untagged" exception despite news2, spec2 and nf37 | GPT | **Resolved over two rounds.** See the correction below. |
| In-text dictionary claims not traceable from citations | GPT | **Resolved.** 忍ぶ cites 2126560, 1321590 and 2154730; 郷愁 cites 1200550; 愚か cites 2832535. 忠実, 恒例 and 追悼 link the Daijisen character headings 実 sense 4, 例 sense 3 and 追 sense 4. |
| 忠実 might offer its valid alternate reading まめ as a wrong option | GPT (limit) | **Resolved on author-side evidence.** The word-quiz audit trace shows the generated look-alikes and corpus readings offered for 忠実; none is まめ, and the audit flags any offered option that is a JMdict reading of the written form. |
| 郷 metadata includes 1355850 (場所) | Claude F2 | **Withdrawn.** The ID predates B169 and supports the card's quoted Kanjipedia sense ③ ところ。場所。 (author assertion; the card body was outside the packet). |
| Optional items adopted | Claude, GPT, Grok | 忍ぶ gives JMdict's sense order, the 隠す contrast and …に(は)忍びない; 忠実 states な/に and 恒例 states の; readings added for 惰眠, 惰気, 愚鈍 and 暗愚; the みじ+め split is attributed to KANJIDIC2 on 惨 and みじめ; 懐古 reworded as a related word; kana added for the 恭しい definition and one attributive 恭しい example; 愚問 reworded as a modest way to refer to one's own question; "okurigana" glossed as the kana ending. |

## Follow-up residues (snapshot cfef4688)

- **恭しい irony clause was an unsourced elaboration** (Claude R1): **resolved.** The card now says the 実用日本語表現辞典 entry notes "that it is sometimes used ironically, with a nuance of affected, more-than-necessary politeness", and the ledger quote includes 「必要以上に丁重っぽく」.
- **恒 reading row still lacked "ordinary"** (GPT): **resolved**, as above.
- **満悦 ledger still said "untagged route"; nf37 misattributed** (GPT; Claude optional): **resolved.** Both 悦 mapping records have no exceptionReason; nf37 appears only in the raw readingPriorityTags.
- **忠実 option trace not supplied** (GPT): **resolved** with the complete audit section and code excerpts.
- **Optional, adopted:** 忠実 stray double space; 恒例 "though not only" moved out of the Daijisen attribution, with a separate JMdict-gloss sentence ("established practice; custom") for the workplace example.

## Correction of an author disposition

In the initial correction the author kept 満悦 as a "no qualifying preferred-tier spelling" exception, treating news2 and spec2 as outside the preferred tier as in B158 and B159. That was wrong for B169. The owner decided in [issue #60 comment 7112026459](https://github.com/stop-cran/learning-japanese/issues/60#issuecomment-7112026459) that JMdict news2 and spec2 count as qualifying tags, and every news2/spec2-only support from B160 to B168 has no exception. 満悦 (news2, spec2, with nf37) therefore qualifies like any other tagged support. 恭 (恭しい, entry 1236790) is the batch's only untagged exception. No card text claimed that 満悦 was untagged.

## Final confirmations (snapshot 9ffbf452)

Claude, GPT and Grok each confirmed that no actionable residue remains. GPT counted 10 source rows, 9 new words, 1 N2 reuse, 16 reciprocal pairs, 25 reading rows, 10 offered keys, 30 fixed distractor slots, and 55 kanji and 49 new-word exclusion declarations. No further revision was made.

## Optional items not adopted

- **Claude:** shifted-sense clauses on the 実, 例 and 追 kanji cards (the word articles carry the sense and the linked character headings); aligning the card's "seldom calls for it" with the ledger's "seldom deliberately used" for 恭しい.
- **Grok:** shortening the dense exclusion lists in kanji notes; the unchanged pre-existing みじめ pity contrast; saying that the 御満悦 entry lists ご満悦 as 別表記; keeping the 恒例 company-meal example, now covered by the JMdict gloss.

These are editorial preferences. None is an established defect.

## Unverified claims and limits

- Daijisen, 実用日本語表現辞典, Kanjipedia, Weblio example and standard-use table checks are author evidence recorded in the batch sources; reviewers saw only those records. This covers the 恭しい register and irony note, the 満悦する Daijisen example, 恒例 "used mostly of ceremonies and events", the 悼む definition and the Kanjipedia つね.に row.
- The owner comment was quoted by the author; reviewers did not open it.
- The raw scan finding 満悦 to be the only spelling containing 悦 with any priority tag is an author observation. Claude confirmed from the packet that 恭しい carries no priority tag.
- Reading-collision, meaning-quiz and word-option results come from author-side static simulation, not observed app behavior.
- Lint reports eight pre-existing metadata-reading errors on 例, 実 and 満, unchanged at every snapshot.
- Upstream integration: no reviewed B169 file overlaps the upstream change; all 36 reviewed article and stroke blobs are byte-identical, and only `manifest.json` was regenerated.
- These are packet-based blind facet reviews with bounded confirmations. There is no native-speaker, device, Android or whole-set acceptance.
