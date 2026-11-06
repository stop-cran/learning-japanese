# Batch 086 visual confirmation: no proved defects; all eight articles CLEAN

## Snapshot
- **Evidence:** signed snapshot 81238670fbf9619a94454f81618ce1a68782981d.
- **Teaching content:** f59c65fde644ed36958d74495da59a66c1d82570, unchanged since my initial review.
- **Native archive:** attempt-605 (6667318d).
- **Model:** Claude Opus 5.5 (`claude-opus-5.5`).

## Scope and fresh reads
- I read my original report, then the whole visual packet in one view. No truncation marker appeared.
- I then viewed all 24 required images one at a time, in the required order: sheets 01–19, font panels 1–3, meaning-question and legend-02 at original size.
- I opened no extra originals. There was no access denial.
- "Supplied" below means taken from the packet's JSON, fixture or logs. "Observed" means I saw it in the images myself.

## Verdicts
CLEAN means no actionable defect was established. It does not mean everything was proved correct.

**凡.md**
- **Correctness:** CLEAN.
- **Scoped coverage:** CLEAN.
- **Text comprehensibility:** CLEAN.

What I observed:
- The facts line shows 3 strokes, radical 几 (no. 16) and "N1 (community list)".
- The mnemonic is labelled "Modern-shape mnemonic, not etymology".
- The five-row readings table scrolls sideways. The おうよ.そ row is marked "kun, source-only" with its caveat.
- The 凡そ→およそ and 凡て→全て recognition aliases appear, along with the はんれい/ぼんれい/判例 note, the 丸/九/凹 notes and the metadata and source links.

**凡例.md**
- **Correctness:** CLEAN.
- **Scoped coverage:** CLEAN.
- **Text comprehensibility:** CLEAN.

What I observed:
- The article explains book conventions and a map legend, "not a legendary story".
- Both examples (凡例を読む and 地図の凡例で記号の意味を確認) show kana and accurate English.
- It also covers synonyms (説明/解説/注), the はじめに boundary, the 判例 homophone, the ボン trap and the JMdict 1523690 and Daijisen sources.

**Six reused diffs** (bounded to the changed passages): all CLEAN.

| Article | Changed passage |
|---|---|
| 平凡 | 凡 (ボン) link in "How the kanji combine" |
| およそ | [凡]そ link |
| 全て | Rare-spelling note for 凡て |
| 平 | 平凡 entry in Common words |
| 例 | 凡例 entry in Common words |
| 全 | 全て link in Common words |

## Findings
None proved.

## Status of my original items
- **栞 quiz-guard hypothesis:** withdrawn.
- **Old-client and fallback exposure:** resolved as a stated limitation (the build requires client f9b59a2 or later). I have no independent proof of this.
- **Title uniqueness:** resolved by the coordinator's scan, not by me.
- **九 "dot" wording (凡.md:59-61):** stays optional and low. The images confirm that 九 has no dot in any of the four fonts, so "compare the position of the dot" applies only to 丸.
- **Other three optional suggestions:** stay optional (編述の方針/例言, the おおよそ note for 凡そ, and 凡人/非凡/凡庸).

## Other visual observations
- **Readings quiz:** both selected on'yomi keys, ハン and ボン, gave "Correct! — on'yomi". The done screen showed "2 of 2" and no kun'yomi question appeared.
- **Meaning quiz:** the four choices were 凹, 准, 凡 and 獣. None of the wrong answers overlaps the meaning of 凡.
- **Fonts:** 凡, 丸, 九, 凹 and 丶 are distinguishable in all four font families. In the Mincho and Textbook rows, 几 is drawn in a heavier, Gothic-like substitute face. This is a font-fallback limitation, not a teaching defect.
- **Navigation:** the links and system Back screens matched their expected destinations.
- **Drawing:** practice is labelled ungraded, and recall gives up correctly.

## Optional
- In the reading feedback, the line listing all readings shows "おうよそ" without the source-only caveat in that view. This is the app's layout, not the teaching text.

## Limits
- Emulator only (API 35). No physical phone, general release or whole-set check.
- The actual fallback font face is unknown.
- The drawing used injected strokes, so this says nothing about human handwriting or the MLKit handwriting model.
- I did not verify anything with Git or upstream dictionaries myself.
- Hashes and nonblank checks were not treated as readability evidence.
- Modern usage of おうよ.そ remains UNVERIFIED.
- One link in the unchanged Notes of the 例 article was not legible at sheet scale. I did not check it because that text is outside this batch's changes.
