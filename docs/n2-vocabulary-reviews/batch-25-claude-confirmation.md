**Snapshot:** The corrected commit is **272330a5b0ba79b56c8d03b7d8600f7ba2ccf32c**. Its parent is c6d44ce4b6dd2e8fceb2fa8ffae7c632ed87e801, which in turn has parent 3a3517322ec749d892e8fe5f97f4cac2a54431ae. I reviewed the committed content as it appears in the working files and the correction patch. I could only use file tools, not Git, so I did not run Git or compute hashes myself. The commit identity, the clean working tree, the file hashes and the equivalence of the evidence derivative (sha256 dbaea521…) are confirmed only by the author's receipt.

**Scope:** I am claude-opus-5.5 (Claude family). This was a bounded check of the changed passages, not another full review of the batch. I read:
- **Changed articles, in full:** 請う, 公共, 原始, 高級, 顕微鏡, 原産, 厳重.
- **Comparison cards, in full:** 拝む, 世の中, 天然, 一流, 生物, 生き物, 故郷, 押さえる.
- **Correction patch, all of it:** the seven word diffs, all ten appended comparison families and the whole `correctionEvidence` block.
- **Confirmation evidence:** only bounded parts — the original 原始, 請う and 公共 Daijisen inspection records, JMdict entry 1273510, and the start of `correctionEvidence`.
- **Public sources I fetched myself:** Kanjipedia 0003929100 just now, and Weblio Daijisen 請う during the original review.

I did not reread any kanji files, unchanged batch articles, source mappings or the rest of the comparison corpus.

**Verdicts:**

| Item | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| 請う | CLEAN | CLEAN | CLEAN |
| 公共 | CLEAN | CLEAN | CLEAN |
| 原始 | CLEAN | CLEAN | CLEAN |
| 高級 | CLEAN | CLEAN | CLEAN |
| 顕微鏡 | CLEAN | CLEAN | CLEAN |
| 原産 | CLEAN | CLEAN | CLEAN |
| 厳重 | CLEAN | CLEAN | CLEAN |
| Packet additions (10 families, `correctionEvidence`) | CLEAN | CLEAN | CLEAN |

**Findings:**
- **F1, resolved.** `請う.md:9` now excludes 拝む. The overlap is real: JMdict 1592920:1 includes "beg", 1472230:2 is "to beg", and the 拝む card is labelled "worship; beg".
- **F2, resolved.** `請う.md:16-17` now limits the particle rule to the request construction shown. The example at line 20 is now 心から許しを請います.
  - Kanjipedia confirms the source expression. Its entry reads 「人に対して、あることをしてくれるように求める。『心から許しを―う』」.
  - "Invite" stays in the title and at line 15. It is still supported by JMdict 1592920:1.
  - My earlier point that Daijisen lists no "invite" sense is narrowed. The author has superseded the receipt that wrongly credited "invite" to Daijisen. The fact that Daijisen leaves it out does not disprove the JMdict meaning.
- **F3, resolved.** `原始.md:9` now excludes 原産 and 天然. The reasons are the shared unqualified "origin" answer label and the "unmodified natural state" sense. The original Daijisen 原始 inspection record shows that sense, and the article's forest example teaches it.
- **F4, resolved.** `高級.md:9` now excludes 一流. JMdict 1167270:1 glosses 一流 as first-class and first-rate.
- **F5, resolved.** `顕微鏡.md:20` now reads 生物 as せいぶつ, supported by 1379430:1 and the 生物 card.
- **F6, withdrawn.** The 故郷 card already recognises ふるさと as another reading, and entry 1603050 supports it. So the old link label was not a contradiction. Aligning `原産.md:36` to こきょう is only navigation polish.
- **Optional 厳重/押さえる guard, resolved.** `厳重.md:9` now excludes 押さえる, because both cards' labels say "secure" without saying which kind.
- **Not adopted (still optional, not defects):**
  - an example of 原始 meaning "beginning", or adding 原始的;
  - noting that 原料 tends not to keep its original shape, unlike 材料;
  - a 恋しい/寂しい comparison;
  - a 公共/個人 link.
- **Regressions:** none.

**Optional:**
- 請う could later add a sourced example of the "invite" use.
- The `correctionEvidence` list of existing comparison labels shows the 請う and 原始 exclusions as they were before the correction. A note saying so would avoid confusion.
- The 公共/世の中 rationale cites JMdict 1273510:1, but that sense says only "public; communal". The "society" support really comes from 1373850:1 and the Daijisen 公共 inspection. The guard itself still holds.

**Limits:**
- I ran no Git commands and verified no hashes or clean-tree state.
- The Daijisen 原始 and 公共 inspections are the author's. I independently fetched only Kanjipedia (now) and Weblio Daijisen 請う (originally).
- I did not consult the Nihon Kokugo Daijiten.
- The removed 専門家を講師に請いました construction remains unverified, though it is no longer taught.
- There was no executed quiz draw, no frequency study and no native-speaker check.
- I did not reread the full comparison corpus.
