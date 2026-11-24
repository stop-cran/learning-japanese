**All eight original quiz-exclusion findings are resolved in the card metadata.** Two issues remain in the revised text: 回忌 still explains its numbering unclearly and omits the specific source entries, and 弓 now overgeneralizes when to use 弓道.

**Snapshot and scope:** `e9b5df6bd6c6c9fed4cce91d5ac4c481d208007c`, compared with blind candidate `cbf5c2c5ca52758812aff3e61ae421e72fadd9e7`. Same reviewer, GPT-6.2 Sol. I read all five revised-text files and all five diffs in full: seven kanji cards and six word cards. I checked `followup-facts.txt`, `followup-evidence-diff.txt`, and `correction-evidence.txt` against those texts and the original local source and label extracts.

| Original finding | Disposition | What the revised text shows |
|---|---|---|
| 弔–忌, 弔–悔, 忌–悔, 忌–憎, 弥–継 | **Resolved** | All five direct pairs are declared. No pair relies on a shared exclusion. |
| 彰–賛, 征–克, 弊害–毒 | **Resolved** | All three direct pairs are declared. The older exclusions are preserved. |
| 弦楽 conflated the orchestra with orchestral music | **Resolved** | The card distinguishes オーケストラ, 管弦楽, and 弦楽, and no longer defines a string quartet only as its players. JMdict 1214130 and 1769460 support the revised glosses. |
| 弥 gave blanket advice to write 渡る | **Resolved** | The card distinguishes 渡る “cross” from kana わたる “span,” and keeps 弥る search-only, consistent with JMdict 1444680. |
| 弦 omitted the preferred spelling for the pot-handle sense | **Resolved** | The card now says “especially when written 鉉,” matching JMdict 1578400. |
| 回忌 first-anniversary usage, counting, and sourcing | **Partially resolved** | 一周忌 is now the usual form, 一回忌 a recorded alternative, and the annual-service implication is gone. 三回忌 and the new 七回忌 example are glossed correctly. The counting explanation and source locators still need repair. |

**Remaining actionable issues**

- `words/回忌.md:14,21,29–31` — The new “first occasion … third” sentence reads as one count with a skipped occasion. State the two conventions plainly: “In Buddhist memorial usage, the first anniversary is usually 一周忌. From 三回忌 onward, the count treats the death as year one: 三回忌 is two years after the death.” The card still lists only JMdict **1199390**, despite the reconciliation note saying 三回忌 was cited to **1814080**. Add **1161330** for the 一周忌 preference, **1814080** for 三回忌, and **1319250** for 七回忌. The local XML addition directly supports 七回忌（しちかいき） as the sixth anniversary.
- `words/弓.md:30` — “For archery as a sport or practice, 弓道 is the usual word” newly makes 弓道 sound like the generic term for the sport. The card’s own earlier explanation and JMdict **1228540** specify Japanese archery. Replace the sentence with “For traditional Japanese archery, use 弓道 (きゅうどう).” The new violin-bow example preserves the intended ゆみ sense.

**Facet verdicts** (correctness / scoped coverage / comprehensibility, for the revised scope): `words/回忌.md` **CLEAN / NEEDS FIX / NEEDS FIX**; `words/弓.md` **NEEDS FIX / CLEAN / CLEAN**; `kanji/弥.md` **CLEAN / UNVERIFIED / CLEAN**. Each of the other ten revised cards is **CLEAN / CLEAN / CLEAN** within the checked scope.

**Optional:** The 絃楽 wording suggestion was adopted (“alternative spelling”). Consolidating the duplicate 表 citations remains optional and unchanged. The isolated space in `ただの びほうさく` is nonblocking style polish.

**Counts and limits:** The revision adds ten direct pairs: the eight original findings plus two bow safeguards. That yields **46 kanji and 18 word exclusion declarations**. The diffs preserve the **20 required reciprocal links**, **23 reading rows**, and **10 offered keys**; the pinned source diff adds one family (**98 → 99**). The project accounting balances arithmetically, but I did not verify publication membership. The exhaustive no-tagged-candidate claim for 弥 remains **unverified**; the local entry supports the selected ビ reading, not the exhaustive search. Daijisen transcriptions, collocation and component checks, validator and manifest results, and reading-pool simulation are author-reported. I did not perform external-page, native-speaker, device, or fresh whole-deck verification.
