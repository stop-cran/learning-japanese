## Snapshot: ae79da1aa5ea5b20c91d356f3490e1bababa46de

**Clean committed files only**, relying on the author-authenticated status and diff provenance. File tools cannot execute Git, so I could not independently verify the commit, cleanliness or diff completeness.

## Scope:

**GPT-6.1 Sol (`gpt-6.1-sol`), family `gpt`.** Read the complete supplied 59-line diff and reviewed all four hunks: two in `kanji\城.md`, one in `kanji\姓.md`, and one in `words\埋める.md`. Read all three current pages for context, relevant dictionary evidence, and the supporting `記入`, `詰める` and `姓` word articles. Independently fetched the precise Nipponica entry.

Read-only and sequential; no edits, delegation or other reviewer reports. The other 15 new pages and unchanged legacy passages were not re-reviewed; their initial coverage and verdicts carry forward. Stroke paths and unrelated content remain excluded.

## Verdicts:

| Page | Correctness | Scoped coverage | Comprehensibility |
| --- | --- | --- | --- |
| `kanji\城.md` | CLEAN | CLEAN | CLEAN |
| `kanji\姓.md` | CLEAN | CLEAN | CLEAN |
| `words\埋める.md` | CLEAN | CLEAN | CLEAN |

CLEAN means no actionable defect established within this bounded review.

## Findings:

**F01 — RESOLVED · Original severity: Minor · Scoped coverage · `kanji\城.md:29,39,45`.** The historical-register qualification now prevents presenting 傾城’s courtesan sense as an unqualified everyday expression. The exact セイ reading remains intact, and the usage claim is attributed to Nipponica rather than an absent JMdict rarity flag. **Evidence:** JMdict entry **1249540**, retained in `docs\n2-batch-sources\batch-05.json:2533-2583`; the external record at lines **493–501**; and the fetched [Nipponica entry](https://kotobank.jp/word/%E5%82%BE%E5%9F%8E-164172), specifically **傾城（花魁、娼妓）／けいせい**, containing **「明治以後はほとんど使われなくなった」**. This is not evidence taken from the separate けいせん or dance headings. **Remaining remedy:** none required for the original finding. **Confidence: high.**

**No new actionable defects or consequential evidence gaps.** The two additional changes were independently confirmed:

- `kanji\姓.md:39` correctly gives 名字 and 苗字 as **みょうじ**, meaning family name, while distinguishing full-name 姓名 **せいめい**. JMdict entries **1604730** and **1375210**, including the complete alias evidence in the packet, support this without a new frequency or register assertion.
- `words\埋める.md:29–31` supplies a natural, translated and correctly kana-supported request. The explanation accurately contrasts **空欄に名前を記入する**—information を, destination field に—with **空欄を埋める**—the blank itself を. It remains scoped to these constructions and preserves the broader non-interchangeability caution. Supporting evidence includes JMdict **1524500**, sense 3, the linked `記入` article, and the fetched *精選版 日本国語大辞典* **き‐にゅう【記入】** definition.

## Optional:

`kanji\城.md:39`: For closer translation of **明治以後**, prefer **“from the Meiji era onward”** over “after the Meiji period.” My initial report used the same loose paraphrase. This is nonblocking chronological precision; the historical-register warning is supported.

## Limits:

No consequential linguistic uncertainty remains in the changed passages. Git provenance remains externally authenticated rather than independently verified. This confirmation does not repeat the unchanged batch review, certify native-speaker naturalness exhaustively, or inspect generated stroke paths.
