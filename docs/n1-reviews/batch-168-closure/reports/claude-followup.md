**Snapshot:** e9b5df6bd6c6c9fed4cce91d5ac4c481d208007c, from the packet only. Initial blind snapshot: cbf5c2c5ca52758812aff3e61ae421e72fadd9e7. I could not check either hash. This is not a fresh whole-deck, native or device review.

**Scope:** My original facet only (correctness, readings, senses, grammar, scoped coverage). I read each file below once, one view call per turn:
- followup-diff-1..5 and followup-revision-1..5
- followup-facts.txt, followup-evidence-diff.txt, correction-evidence.txt

I compared these with my first-pass notes on the same packet (primary.xml, families-*, sources.json, quiz.txt, labels.txt). I did not open confirmation-task.txt. Unchanged cards (法廷, 弔問, 色彩, 表彰 and the ten changed kanji) are presumed identical to the first snapshot, because I have only the author-supplied diffs. Labels are `[S]` for source facts in the packet and `[A]` for author statements I cannot verify.

**Dispositions of my original findings**

| # | Finding | Status | Basis |
|---|---|---|---|
| Q1 | 弔 / 忌 / 悔 overlap | Resolved | 弔 now excludes 忌 and 悔. 忌 now excludes 憎 and 悔. Both notes explain the contrast. 忌 does not list 弔, so this relies on the author's claim that exclusions are symmetric `[A: content-format.md:120, not in packet]`. |
| Q2 | 忌 "abhor" vs 憎 | Resolved | 憎 added to 忌, with a note. |
| Q3 | 弥 "patch" vs 継 | Resolved | 継 added, with a note. |
| Q4 | 弓 vs 礼 / お辞儀 | Partially resolved | Kanji 弓 now excludes 礼 and says it is a bow of the head. Word 弓 now excludes お辞儀. Word 礼 "thanks; bow" is still not excluded (R1). |
| Q5 | 征 "conquer" vs 克 | Resolved | 克 added, with a note. |
| Q6 | 弊害 vs 毒 | Resolved | 毒 added. |
| F1 | 弦楽: 管弦楽 as the "kanji word" of オーケストラ | Resolved | It now reads "ensemble" vs "orchestral music", which matches `[S]` JMdict 1214130. 絃楽 is now "alternative spelling". |
| F2 | 回忌: 一回忌 / 一周忌 qualifier and citations | Partially resolved | 一周忌 is now "usual" and 一回忌 is given with its reading, matching `[S]` 1161330 "usu. 一周忌". 七回忌 (しちかいき, "sixth anniversary") is added and matches `[S]` 1319250, newly pinned in followup-evidence-diff. The +1 rule is still correct. The card's Dictionary line still cites only 1199390 (R2). |
| F3 | 弓: 弓を習う example | Resolved | Replaced by バイオリンの弓を新しいものに替えた, with a note that 弓道 is the usual word for archery. The grammar and reading are fine. |
| F4 | 弦: pot-handle つる | Resolved | Now "especially when written 鉉", which matches `[S]` 1578400. |
| F5 | 征服: "After three days" | Resolved | Now "Taking three days". |
| F6 | 弊害: 損害 "caused" | Resolved | Now "damage or loss itself, often counted in money". |

**Optional ideas from my first report**
- **Adopted:**
  - 弥縫策を講じる replaces 重ねる (`[A]` Kotobank attestation).
  - 尔 is corrected to 尓 in the 弥 card (`[A]` KanjiVG; consistent with my earlier guess, not independently verified).
  - 賛 is added to 彰.
  - 弥 わた.る now notes kana わたる for "span/extend" (consistent with `[S]` 1444680, which marks that sense usually-kana).
- **Still optional, not adopted:**
  - an active 表彰 example
  - 色彩 vs 紅葉 / 絵の具, and 弔問 vs 香典, exclusions
  - a note on the Kanjipedia-only readings of 弥
  - 法廷 translation polish
- **Previously unverified Daijisen claims:** the author now supplies transcribed quotes for 法廷, the 色彩 figurative use and the 回忌 account `[A]`. They match what the cards say. One nuance: the 法廷 quote includes "またはその支部", which the card omits. I cannot verify the quotes, and I keep them as author evidence.
- **弥 reading ビ exception:** unchanged. The author records it as an exception, and its exhaustiveness is `[A]`. I leave it to the adjudicator.

**Regression check:** I found no new reading, grammar or sense errors.
- 七回忌 = しちかいき, 講じる = こうじる and ばいおりん are correct.
- The new 回忌 example is natural.
- 兄も rendered "even my older brother" is a mild, acceptable rendering.
- Front matter still matches the curatedProjection in followup-facts.

**Remaining actionable issues (minor, none consequential)**
- **R1:** `words/弓` could also exclude word 礼 ("thanks; bow"). It shares the unqualified "bow" token, as お辞儀 did. Low to medium confidence. Under the author's symmetry claim it is a one-line guard.
- **R2:** `words/回忌` could append JMdict entries 1161330, 1814080 and 1319250 to its Dictionary line. The card says "as JMdict glosses it" for 三回忌 and 七回忌. The author says 三回忌 is cited to 1814080, but the card text I was given does not show it. The batch source record may hold it; I cannot see it.

**Optional or cosmetic:** The 弥縫策 example 1 reading now has a stray space ("ただの びほうさく"), unlike example 2 and the project's convention. The author says it is deliberate, with no rationale given. Remove it or apply it consistently. The cards for 弦楽 could also cite 1214130 and 1769460.

**Verdict:** Correctness and scoped coverage are CLEAN for all revised cards, with the minor residues R1 and R2 noted. No consequential unresolved claim remains in my facet.

**Limits:**
- Symmetry of exclusions, the Daijisen quotes, Kotobank, KanjiVG and the 弥 ビ exception all rest on the author's statements.
- I have no オーケストラ entry; "ensemble" is plain knowledge, not a packet fact.
- The mechanical-check results are the author's.
