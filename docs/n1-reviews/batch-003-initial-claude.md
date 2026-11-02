**Snapshot:** `6ce567650e6663d712bac25bebd5bead0d0af655`, committed teaching only, with base `fd75a67`. The only added evidence is the input-metadata JSON I was given (`docs\n1-reviews\batch-003-input-metadata.json`). No uncommitted teaching was reviewed.

**Scope:** I'm Claude Opus 5.5 (`claude-opus-5.5`). I worked alone, made no edits, and used one tool call at a time.
- **Files read completely:** all ten in-scope files, both JMdict packets (the comparisons file came back whole in one read, not truncated) and the metadata JSON.
- **Other local reads:** `content-format.md` lines 40–157, a narrow search of word titles, the titles of 猫, 留, 畜, 半, 判, 久, 辺, 代, 育, 湖, 田, 名 and 字, and the reading lines of `kanji\辺.md`.
- **Live Kotobank fetches:** 畔, 苗代, 畝, 代 and 苗 (two pages), all successful.
- **Not fetched:** 湖畔 and 育苗. The claims that cite them are low-stakes and already supported by JMdict.
- **Not read:** other reports, progress ledgers or author records.

**Verdicts** (correctness / scoped coverage / comprehensibility)
- `kanji\苗.md`: CLEAN / CLEAN / CLEAN
- `kanji\畔.md`: CLEAN / CLEAN / CLEAN
- `kanji\畝.md`: CLEAN / CLEAN / CLEAN
- `words\苗.md`: CLEAN / CLEAN / CLEAN
- `words\育苗.md`: CLEAN / CLEAN / CLEAN
- `words\苗代.md`: CLEAN / CLEAN / CLEAN
- `words\畔.md`: CLEAN / CLEAN / CLEAN
- `words\湖畔.md`: CLEAN / CLEAN / CLEAN
- `words\畝.md`: CLEAN / CLEAN / CLEAN
- `words\名字.md`, changed passage only: CLEAN / CLEAN / CLEAN. The 苗 link gives navigation back to the kanji card, and the ミョウ allocation is correct (JMdict 1604730 lists 苗字 first, marked common).

**Checks behind the verdicts**
- **Metadata:** strokes, radicals, grade and the full on/kun lists match the raw KANJIDIC2 records, in source order. The selected quiz readings are exact subsets, and the mechanical key projection is consistent with them.
- **Kotobank evidence:**
  - Nikkoku 畔 says くろ is found in Kantō and northward, while あぜ is mainly Hokuriku/Chūbu westward. This supports "regional".
  - Nikkoku 苗代 says 「なは」は「なへ（苗）」の意, supporting the bound form なわ-.
  - Daijisen 代 しろ sense 5 reads 「田。田地。…苗代」.
  - The 畝 page has separate せ, ほ and うね headings, and Nipponica gives ホ or ボウ for the Chinese unit.
  - Nipponica 苗 lists 挿木苗 (seedlings from cuttings), supporting that claim.
- **Quiz distractors:** the meaning choices are cat, retain/stay, livestock, half, judge/seal and "a long time". None matches an ordinary sense of 苗, 畔 or 畝.
- **Word exclusions:** these work in both directions as single pairs (畔↔畝, 苗↔芽/植物/木, 苗代↔田/田んぼ, 湖畔↔岸/陸, 育苗↔育てる). I found no remaining title pair where a learner could reasonably accept both answers.
- **Links:** every selected support word links back to its kanji card, including 名字.

**Reading-key suitability**
- **苗:**
  - びょう (via 育苗) and みょう (via 苗字) are suitable.
  - なえ is the strongest key.
  - なわ is suitable but the weakest: it has one practical word, 苗代, and the exported key drops the dash that marks it as a bound form.
- **畔:** はん (湖畔, 河畔) and あぜ are suitable. Leaving out くろ (regional) and ほとり (rare spelling, usually kana) is justified.
- **畝:** turning off on-reading questions (`[]`) is appropriate. ホ is marked rare, and ボウ/モ/ム are source-only with no word example. うね is suitable, and leaving out せ (marked obsolete) is reasonable.

**Findings:** None.

**Optional** (all nonblocking)
1. In `kanji\畔.md` line 46, the clause "neither is the primary reading of the linked あぜ article" is confusing and could be simplified.
2. In `words\畔.md` line 36, "should not be replaced with 'rice field'" is unclear. "Do not translate あぜ as 'rice field'" would be clearer.
3. Two asides could go, since a learner would be unlikely to make either mistake: "the price of 苗" in `words\苗代.md` line 36, and "not an i-adjective" in `words\湖畔.md` line 20.
4. Every example sentence in `words\畔.md` writes あぜ in kana, which is natural. One phrase showing 畔 itself would help readers recognise the kanji.
5. Consider whether the なわ key should be shown with its bound-form context, or left out of the selected readings.
6. 苗 vs 稲 ("rice plant") carries a small word-quiz risk. It doesn't need an exclusion now.

**Limits**
- JMdict and KANJIDIC2 evidence came from the frozen coordinator packets. Only the Kotobank pages above were fetched live.
- How the app actually shows the dash-free key なわ was not verified.
- This review gives no native-speaker, phone-device or measured-learning certification, and doesn't cover fonts, stroke drawing or archive import.
