All **18 required reciprocal links** are present with the correct readings. I found one missing direct meaning-quiz exclusion and four localized teaching defects. The curated reading keys match the supplied sources; live quiz behavior remains unverified.

**Snapshot:** `0ac3eaad07b20ba50997f128dfb78bba7c99e70a`, based on `4dff7a1c46fa3b06de2f7a97004f9837ec2dc445`. No working-tree overlay was supplied.

**Scope and counts:** One blind reviewer, GPT-6.2 Sol. Read all eight numbered teaching files, `changed.txt`, all 26 comparison articles, `rubric.txt`, `sources.json`, `primary.xml`, `quiz.txt`, `labels.txt`, and all ten family extracts. The packet covers **10 kanji source rows, 10 new kanji, 10 distinct new words, and 6 changed constituent kanji**. The word files contain 12 article copies because 憤慨 and 遺憾 each appear twice. The 12 support mappings plus 6 supplementary mappings yield 18 distinct link pairs, all checked in both directions. No older word was reused as mapped support. All 26 metadata readings have a reading-table entry or a qualified source-only explanation; 10 are selected for quizzes (8 on, 2 kun).

**Verdicts** — Correctness includes consistency, evidence, and quiz safety within the packet; comprehensibility is limited to the reviewed labels and contrasts.

| Cards | Correctness | Scoped coverage | Comprehensibility |
|---|---|---|---|
| Kanji: 慈・慕・慶・憂・憤・憾・懇・遺 | CLEAN | CLEAN | CLEAN |
| Kanji: 慨 | UNVERIFIED | CLEAN | CLEAN |
| Kanji: 懲 | NEEDS FIX | CLEAN | NEEDS FIX |
| Words: 慕う・憤慨・慶弔・懲りる・遺産 | CLEAN | CLEAN | CLEAN |
| Words: 感慨・憂慮 | UNVERIFIED | CLEAN | CLEAN |
| Words: 慈善・懇談 | NEEDS FIX | CLEAN | CLEAN |
| Word: 遺憾 | NEEDS FIX | NEEDS FIX | NEEDS FIX |
| Changed kanji: 善・感・弔・慮・談・産, changed lines only | CLEAN | CLEAN | CLEAN |

**Consequential findings**

| Severity / facet | Location | Evidence, impact, and exact remedy |
|---|---|---|
| Moderate · meaning quiz | `words/遺憾.md:8,15` | **遺憾–不満 is not directly excluded in either supplied row.** The new card teaches dissatisfaction over an outcome, and the older 不満 card explicitly teaches dissatisfaction or discontent. That makes both defensible under a bare dissatisfaction gloss even though their uses differ. Add `不満` to 遺憾’s `quiz_exclusions`; retain the distinction between formal regret and dissatisfaction. Evidence: `labels.txt`, `quiz.txt`, JMdict 1159090 and 1494970, and the comparison article. High confidence in the missing pair; live exposure unverified. |
| Minor · grammar coverage | `words/遺憾.md:7,22` | The card gives only the `na-adjective` classification and treats its noun example as a set phrase, although JMdict 1159090 explicitly records both. Add the `noun` tag and show the two uses side by side: noun `遺憾の意`, adjectival `遺憾な結果`. `遺憾です` alone does not demonstrate な attachment. High confidence. |
| Minor · comparator consistency | `words/懇談.md:26` | “会議 is a formal meeting” and “話し合い is a discussion to settle something” are too categorical. The older cards distinguish organized deliberation and talking something over without requiring formality or resolution. Say that 会議 is a meeting for discussion, planning, or decisions; 話し合い is talking a matter over; 懇談 emphasizes a relaxed, friendly manner. High confidence from both comparison articles and JMdict 1198360, 1600910, and 1289900. |
| Minor · comparator consistency | `words/慈善.md:26` | The absolute “without seeking reward” overstates 奉仕 and obscures its separate retail use. In the charity contrast, say that 奉仕 emphasizes **service or work for others**, while 慈善 emphasizes **charitable aid or activity**. The older 奉仕 article and JMdict 1515950 support that narrower comparison. High confidence. |
| Minor · meaning explanation | `kanji/懲.md:42` | 課’s textbook “lesson” and 懲りる’s “learn a lesson” share English wording, not a Japanese sense; 習 and 学 likewise do not imply being deterred by a bad experience. Keep the quiz exclusions, but describe them as protection against misleading English cues, not as evidence of close meanings. High confidence from `labels.txt` and JMdict 1428190. |

**Unresolved evidence and limits:** The supplied JMdict entry 1418090 supports 嘆く and 歎く, not the dictionary-wide negative in `kanji/慨.md:32`. Narrow the statement to that entry or supply the pinned search result; keeping なげく out of quizzes is supported. Likewise, the extracts are consistent with 遺憾 being the only qualifying 憾 route, but do not independently establish the full scan’s result. For meaning quizzes, confirm live eligibility and direct exclusions for **憂慮–懸念** (JMdict 1257720 shares all three glosses) and **感慨–感じる** (1212260 sense 2, “be moved/touched”); their comparison-side runtime rows are absent. Add a direct exclusion where an eligible, unblocked candidate makes a bare prompt ambiguous.

For reading quizzes, six selected on-readings are shared by listed lookalikes: 慈–磁, 慨–概, 憂–優, 憤–噴/墳, 憾–感, and 懇–墾/恨/根. These are sound shape distractors, but not distinct answers to a kana-only prompt. Confirm that the reading mode filters shared valid readings or uses a disambiguating cue. The packet does not establish runtime candidate selection, manifest integration, or resolution of incidental targets outside the supplied articles. `sources.json` records the author’s checks of all ten Digital Daijisen word headings, eight character headings, four 実用日本語表現辞典 headings, and all ten standard-use rows. I did not independently verify external pages, native usage, a device, or the whole deck.

**Optional:** Mark 感概 as **search-only**, not an accepted alternate spelling of 感慨 (JMdict 1212310). Consolidate the overlapping JMdict citation lines in the changed 感・談・産 articles.
